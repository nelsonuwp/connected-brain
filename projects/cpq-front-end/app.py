import json
import os
import sys
from decimal import Decimal
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from sshtunnel import SSHTunnelForwarder

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")

# ---------------------------------------------------------------------------
# Fusion DB (SSH tunnel)
# ---------------------------------------------------------------------------
SSH_HOST     = os.environ.get("SSH_HOST", "10.121.21.20")
SSH_PORT     = int(os.environ.get("SSH_PORT", "22"))
SSH_USER     = os.environ.get("SSH_USER", "")
SSH_PASSWORD = os.environ.get("SSH_PASS", "")

DB_REMOTE_HOST = os.environ.get("FUSION_DB_SERVER", "db1.peer1.com")
DB_REMOTE_PORT = int(os.environ.get("FUSION_DB_PORT", "5432"))
DB_NAME        = os.environ.get("FUSION_DB_NAME", "fusion")
DB_USER        = os.environ.get("FUSION_DB_USER", "sb_readonly")
DB_PASSWORD    = os.environ.get("FUSION_DB_PASS", "")

# ---------------------------------------------------------------------------
# MSSQL (DM_BusinessInsights)
# ---------------------------------------------------------------------------
MSSQL_SERVER   = os.environ.get("MSSQL_BI_SERVER") or os.environ.get("OCEAN_DB_SERVER", "")
MSSQL_DB       = os.environ.get("MSSQL_BI_NAME")   or os.environ.get("OCEAN_DB_NAME", "")
MSSQL_USER     = os.environ.get("MSSQL_BI_USER")   or os.environ.get("OCEAN_DB_USERNAME", "")
MSSQL_PASSWORD = os.environ.get("MSSQL_BI_PASS")   or os.environ.get("OCEAN_DB_PASSWORD", "")

# ---------------------------------------------------------------------------
# Static data — overhead rates ONLY (not authoritative for DC list or currencies)
# ---------------------------------------------------------------------------
_COST_DRIVERS_PATH = Path(__file__).parent / "cost_drivers.json"
with open(_COST_DRIVERS_PATH) as f:
    COST_DRIVERS = json.load(f)

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Fusion connection (persistent tunnel)
# ---------------------------------------------------------------------------
_tunnel = None
_conn   = None


def get_conn():
    global _tunnel, _conn
    if _conn:
        try:
            _conn.cursor().execute("SELECT 1")
            return _conn
        except Exception:
            _conn = None
    if _tunnel and not _tunnel.is_active:
        _tunnel = None
    if not _tunnel:
        _tunnel = SSHTunnelForwarder(
            (SSH_HOST, SSH_PORT),
            ssh_username=SSH_USER,
            ssh_password=SSH_PASSWORD,
            remote_bind_address=(DB_REMOTE_HOST, DB_REMOTE_PORT),
        )
        _tunnel.start()
    _conn = psycopg2.connect(
        host="127.0.0.1", port=_tunnel.local_bind_port,
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
        gssencmode="disable", cursor_factory=RealDictCursor,
    )
    _conn.set_session(readonly=True, autocommit=True)
    return _conn


# ---------------------------------------------------------------------------
# DC registry — authoritative source: Fusion sb_datacenter
# Merged with cost_drivers.json for native_currency (needed for overhead FX).
# ---------------------------------------------------------------------------
_dc_registry = None  # {dc_abbr: {id, dc_abbr, name, currencies, native_currency}}


def _build_registry_from_cost_drivers() -> dict:
    """Fallback registry built from cost_drivers.json when Fusion is unavailable."""
    result = {}
    for code, dc in COST_DRIVERS["data_centers"].items():
        native = dc["native_currency"]
        result[code] = {
            "id":             dc["fusion_dc_id"],
            "dc_abbr":        code,
            "name":           dc["name"],
            "city":           None,
            "state":          None,
            "currencies":     [native],
            "native_currency": native,
        }
    return result


def get_dc_registry() -> dict:
    """
    Return cached DC registry keyed by dc_abbr.
    Queries Fusion: sb_datacenter + datacenter_available_currencies.
    Merges native_currency from cost_drivers.json where available.
    Falls back to cost_drivers.json if Fusion is unreachable.
    """
    global _dc_registry
    if _dc_registry is not None:
        return _dc_registry

    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT sd.id, sd.dc_abbr, sd.name, sd.city, sd.state,
                       array_agg(dac.currency_code ORDER BY dac.currency_code)
                         FILTER (WHERE dac.currency_code IS NOT NULL) AS currencies
                FROM public.sb_datacenter sd
                LEFT JOIN public.datacenter_available_currencies dac
                       ON dac.datacenter_id = sd.id
                WHERE sd.active = true
                GROUP BY sd.id, sd.dc_abbr, sd.name, sd.city, sd.state
                ORDER BY sd.dc_abbr
            """)
            rows = cur.fetchall()

        registry = {}
        for r in rows:
            abbr      = r["dc_abbr"]
            currencies = r["currencies"] or []
            # Prefer native_currency from cost_drivers.json; fall back to first pricebook currency
            cd_entry  = COST_DRIVERS["data_centers"].get(abbr, {})
            native    = cd_entry.get("native_currency") or (currencies[0] if currencies else "USD")
            registry[abbr] = {
                "id":              r["id"],
                "dc_abbr":         abbr,
                "name":            r["name"],
                "city":            r.get("city"),
                "state":           r.get("state"),
                "currencies":      currencies,
                "native_currency": native,
            }
        _dc_registry = registry
    except Exception:
        _dc_registry = _build_registry_from_cost_drivers()

    return _dc_registry


def get_dc_info(dc_abbr: str) -> dict | None:
    return get_dc_registry().get(dc_abbr.upper())


# ---------------------------------------------------------------------------
# MSSQL: hardware costs
# Returns {sku_id: {"cost": float, "currency": str, "name": str}}
# sku_level must be 'TLS' (server-level) or 'Component' — same sku_id can
# appear in both rows, so the level discriminator is mandatory.
# ---------------------------------------------------------------------------
_HW_SKU_TYPES = {"HW", "Hardware", "hw", "hardware"}

def get_mssql_costs(sku_ids: list[int], sku_level: str) -> dict[int, dict]:
    if not sku_ids or not all([MSSQL_SERVER, MSSQL_DB, MSSQL_USER, MSSQL_PASSWORD]):
        return {}
    try:
        import pymssql
        conn = pymssql.connect(
            server=MSSQL_SERVER, user=MSSQL_USER,
            password=MSSQL_PASSWORD, database=MSSQL_DB,
            tds_version="7.0",
        )
        cur = conn.cursor(as_dict=True)
        placeholders = ",".join(["%d"] * len(sku_ids))
        cur.execute(
            f"SELECT sku_id, sku_name, sku_cost, cost_currency, sku_type, sku_category "
            f"FROM profitability.ocean_sku_cost "
            f"WHERE sku_level = %s AND sku_id IN ({placeholders})",
            (sku_level, *sku_ids),
        )
        result = {}
        for r in cur.fetchall():
            raw_type = (r.get("sku_type") or "").strip()
            is_hw    = raw_type in _HW_SKU_TYPES or raw_type.upper().startswith("HW")
            result[r["sku_id"]] = {
                "cost":         float(r["sku_cost"] or 0),
                "currency":     r["cost_currency"] or "USD",
                "name":         r["sku_name"] or "",
                "sku_type":     raw_type,
                "sku_category": (r.get("sku_category") or "").strip(),
                "cost_kind":    "hw" if is_hw else "sw",
            }
        cur.close()
        conn.close()
        return result
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# MSSQL: hardware wattage
# Returns watts (int) for a given fusion_id, or None if not found.
# ---------------------------------------------------------------------------
def get_mssql_watts(fusion_id: int) -> int | None:
    if not all([MSSQL_SERVER, MSSQL_DB, MSSQL_USER, MSSQL_PASSWORD]):
        return None
    try:
        import pymssql
        conn = pymssql.connect(
            server=MSSQL_SERVER, user=MSSQL_USER,
            password=MSSQL_PASSWORD, database=MSSQL_DB,
            tds_version="7.0",
        )
        cur = conn.cursor(as_dict=True)
        cur.execute(
            "SELECT watts FROM profitability.hardware_watts WHERE fusion_id = %d",
            (fusion_id,),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row and row.get("watts") is not None:
            return int(row["watts"])
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# MSSQL: FX rates
# Columns: from_currency, to_currency, exchange_rate, start_date
# ---------------------------------------------------------------------------
def get_fx_rate(from_currency: str, to_currency: str) -> float:
    """Return exchange rate from_currency → to_currency. Falls back to 1.0."""
    if from_currency == to_currency:
        return 1.0
    if not all([MSSQL_SERVER, MSSQL_DB, MSSQL_USER, MSSQL_PASSWORD]):
        return 1.0
    try:
        import pymssql
        conn = pymssql.connect(
            server=MSSQL_SERVER, user=MSSQL_USER,
            password=MSSQL_PASSWORD, database=MSSQL_DB,
        )
        cur = conn.cursor(as_dict=True)
        cur.execute(
            "SELECT TOP 1 exchange_rate FROM dbo.dimCurrencyExchangeRates "
            "WHERE from_currency = %s AND to_currency = %s "
            "ORDER BY start_date DESC",
            (from_currency, to_currency),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row and row.get("exchange_rate"):
            return float(row["exchange_rate"])
    except Exception:
        pass
    return 1.0


# ---------------------------------------------------------------------------
# Overhead calculation
# Amounts in cost_drivers.json are in DC native_currency.
# Pass fx_rate = get_fx_rate(native_currency, display_currency) to convert.
# service_type: "server" | "firewall" | "switch" — selects cost tier.
# ---------------------------------------------------------------------------
def calc_overhead(dc_code: str, mrc_display: float, fx_rate: float = 1.0,
                  kw: float | None = None, service_type: str = "server") -> dict:
    dc = COST_DRIVERS["data_centers"].get(dc_code)
    if not dc:
        return {}
    dc_costs = dc["costs"]
    # Support both old flat schema and new service-type-nested schema
    if isinstance(next(iter(dc_costs.values())), dict) and "amount" not in next(iter(dc_costs.values())):
        costs = dc_costs.get(service_type) or dc_costs.get("server") or {}
    else:
        costs = dc_costs
    const  = COST_DRIVERS["overhead_constants"]
    native = dc["native_currency"]
    lines  = {}

    for key, entry in costs.items():
        amt     = entry["amount"]
        measure = entry["measure"]
        if amt == 0:
            lines[key] = {
                "amount": 0, "currency": native, "measure": measure,
                "provenance": {
                    "source": "cost_drivers.json",
                    "path": f"data_centers.{dc_code}.costs.{service_type}.{key}",
                    "native_amount": 0, "native_currency": native,
                    "formula": "0 — not configured",
                },
            }
            continue

        if measure == "per_kw":
            if kw is None:
                native_val = None
                formula    = f"{amt} {native}/kW × kW unknown = N/A"
            else:
                native_val = round(amt * kw, 2)
                formula    = f"{amt} {native}/kW × {kw} kW = {native_val} {native}"
        elif measure in ("per_device", "per_server"):
            native_val = round(amt, 2)
            formula    = f"{amt} {native}/device"
        else:
            native_val = round(amt, 2)
            formula    = str(amt)

        display_val = round(native_val * fx_rate, 2) if native_val is not None else None
        if fx_rate != 1.0 and native_val is not None:
            formula += f" × {fx_rate} FX = {display_val}"

        lines[key] = {
            "amount":   display_val,
            "currency": native,
            "measure":  measure,
            "provenance": {
                "source":          "cost_drivers.json",
                "path":            f"data_centers.{dc_code}.costs.{service_type}.{key}",
                "native_amount":   native_val,
                "native_currency": native,
                "measure":         measure,
                "formula":         formula,
                "fx_rate":         fx_rate,
            },
        }

    sga_pct = const["sga_pct"]
    sga_val = round(mrc_display * sga_pct, 2) if mrc_display else 0
    lines["sga"] = {
        "amount":   sga_val,
        "currency": native,
        "measure":  "pct_of_mrc",
        "provenance": {
            "source":  "cost_drivers.json",
            "path":    "overhead_constants.sga_pct",
            "formula": f"Total MRC {mrc_display} × {sga_pct} (SG&A %) = {sga_val}",
            "fx_rate": fx_rate,
        },
    }
    return lines


def _dec(v) -> float:
    if v is None:
        return 0.0
    if isinstance(v, Decimal):
        return float(v)
    return float(v)


# ---------------------------------------------------------------------------
# Routes — pages
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/product/<int:product_id>")
def product_page(product_id):
    return render_template("product.html", product_id=product_id)


# ---------------------------------------------------------------------------
# Routes — API
# ---------------------------------------------------------------------------
@app.route("/api/datacenters")
def datacenters():
    """
    Returns active DCs from Fusion (sb_datacenter + datacenter_available_currencies).
    Falls back to cost_drivers.json if Fusion is unreachable.
    """
    registry = get_dc_registry()
    return jsonify([
        {
            "code":            info["dc_abbr"],
            "name":            info["name"],
            "fusion_dc_id":    info["id"],
            "currencies":      info["currencies"],
            "native_currency": info["native_currency"],
        }
        for info in sorted(registry.values(), key=lambda x: x["dc_abbr"])
    ])


@app.route("/api/fx-rate")
def fx_rate_endpoint():
    from_cur = request.args.get("from", "USD").upper()
    to_cur   = request.args.get("to",   "USD").upper()
    rate     = get_fx_rate(from_cur, to_cur)
    return jsonify({"from": from_cur, "to": to_cur, "rate": rate})


@app.route("/api/servers")
def servers():
    """
    Active servers with pricebook pricing in display currency.
    Query params: dc (dc_abbr), currency (display), product_line

    Pricing strategy:
      1. Try pricebook WHERE currency = display_currency → fx_pricing = 1.0
      2. Fall back to native_currency → fx_pricing = get_fx_rate(native, display)
    """
    dc_abbr      = request.args.get("dc", "").upper()
    currency     = request.args.get("currency", "USD").upper()
    product_line = request.args.get("product_line", "4")

    dc_info = get_dc_info(dc_abbr)
    if not dc_info:
        return jsonify({"error": f"Unknown DC: {dc_abbr}"}), 400

    fusion_dc_id    = dc_info["id"]
    native_currency = dc_info["native_currency"]

    conn = get_conn()

    def _query_servers(pb_currency: str):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT pc.id, pc.name, pc.description, pc.sku,
                       pc.available_in_shop, pc.sold_out, pc.limited_availability,
                       pb.mrc, pb.nrc, pb.setup, pb.is_available,
                       pb.id AS pricebook_id
                FROM public.product_catalog pc
                JOIN public.pricebook pb ON pb.product_catalog_id = pc.id
                WHERE pc.product_class = 1
                  AND pc.is_active = true
                  AND pb.currency = %s
                  AND pb.datacenter = %s
                  AND pb.product_line_id = %s
                  AND pb.component_id IS NULL
                  AND pb.mrc > 0
                  AND pb.is_available = true
                ORDER BY pb.mrc ASC
            """, (pb_currency, fusion_dc_id, product_line))
            return cur.fetchall()

    # Step 1: try target currency directly
    rows = _query_servers(currency)
    if rows:
        pricing_currency = currency
        fx_pricing       = 1.0
    else:
        # Step 2: fall back to native currency + FX
        rows             = _query_servers(native_currency)
        pricing_currency = native_currency
        fx_pricing       = get_fx_rate(native_currency, currency)

    return jsonify([
        {
            **dict(r),
            "mrc":              round(_dec(r["mrc"]) * fx_pricing, 2),
            "nrc":              round(_dec(r["nrc"]) * fx_pricing, 2),
            "setup":            round(_dec(r["setup"]) * fx_pricing, 2),
            "pricing_currency": pricing_currency,
            "display_currency": currency,
            "fx_pricing":       fx_pricing,
        }
        for r in rows
    ])


@app.route("/api/product/<int:product_id>")
def product_detail(product_id):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, name, description, sku, is_active,
                   available_in_shop, sold_out, limited_availability, release_date
            FROM public.product_catalog WHERE id = %s
        """, (product_id,))
        row = cur.fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(row))


@app.route("/api/product/<int:product_id>/config")
def product_config(product_id):
    """
    Returns server config with all monetary values in display currency.
    Query params: dc (dc_abbr), currency (display), product_line, term (12/24/36)

    Pricing strategy (pricebook):
      1. Try currency = display_currency directly → fx_pricing = 1.0
      2. Fall back to native_currency → fx_pricing = get_fx_rate(native, display)

    Cost strategy (ocean_sku_cost):
      Each row has its own cost_currency (typically USD).
      fx_cost_map = {cost_currency: get_fx_rate(cost_currency, display_currency)}
    """
    dc_abbr      = request.args.get("dc", "ATL").upper()
    currency     = request.args.get("currency", "USD").upper()
    product_line = request.args.get("product_line", "4")
    term_months  = int(request.args.get("term", "36"))

    dc_info = get_dc_info(dc_abbr)
    if not dc_info:
        return jsonify({"error": f"Unknown DC: {dc_abbr}"}), 400

    fusion_dc_id    = dc_info["id"]
    native_currency = dc_info["native_currency"]

    # Overhead FX: cost_drivers.json amounts are in native_currency
    fx_overhead = get_fx_rate(native_currency, currency)

    conn = get_conn()

    def _query_server_pb(pb_currency: str):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT pb.id AS pricebook_id, pb.mrc, pb.nrc, pb.setup
                FROM public.pricebook pb
                WHERE pb.product_catalog_id = %s
                  AND pb.component_id IS NULL
                  AND pb.currency = %s
                  AND pb.datacenter = %s
                  AND pb.product_line_id = %s
                  AND pb.is_available = true
                LIMIT 1
            """, (product_id, pb_currency, fusion_dc_id, product_line))
            return cur.fetchone()

    # Step 1: try target currency directly
    pb_row = _query_server_pb(currency)
    if pb_row:
        pricing_currency = currency
        fx_pricing       = 1.0
    else:
        # Step 2: fall back to native currency
        pb_row           = _query_server_pb(native_currency)
        pricing_currency = native_currency
        fx_pricing       = get_fx_rate(native_currency, currency)

    server_mrc_pb   = _dec(pb_row["mrc"])   if pb_row else 0
    server_nrc_pb   = _dec(pb_row["nrc"])   if pb_row else 0
    server_setup_pb = _dec(pb_row["setup"]) if pb_row else 0
    server_mrc      = round(server_mrc_pb   * fx_pricing, 2)
    server_nrc      = round(server_nrc_pb   * fx_pricing, 2)
    server_setup    = round(server_setup_pb * fx_pricing, 2)
    pricebook_id    = pb_row["pricebook_id"] if pb_row else None

    pb_provenance = {
        "source":           "Fusion: public.pricebook",
        "filters": (
            f"product_catalog_id={product_id}, currency={pricing_currency}, "
            f"datacenter={fusion_dc_id} ({dc_abbr}), product_line_id={product_line}, "
            f"component_id IS NULL, is_available=true"
        ),
        "pricebook_id":     pricebook_id,
        "field":            "pricebook.mrc",
        "pb_value":         server_mrc_pb,
        "pricing_currency": pricing_currency,
        "fx_pricing":       fx_pricing,
        "fx_source":        (
            f"MSSQL: dbo.dimCurrencyExchangeRates "
            f"WHERE from_currency='{pricing_currency}' AND to_currency='{currency}' "
            f"ORDER BY start_date DESC"
        ) if fx_pricing != 1.0 else "direct — no conversion needed",
        "display_value":    server_mrc,
        "display_currency": currency,
    }

    # -- Default components
    def _query_components(table: str, id_col: str, pb_currency: str):
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT t.{id_col} AS component_id,
                       {'t.quantity,' if table == 'public.product_templates' else '1 AS quantity,'}
                       c.display_name AS name, c.description, c.is_active,
                       ct.name AS component_type,
                       pct.name AS parent_type,
                       cc.name AS category, cc.sort_order AS cat_sort,
                       pb.id AS pricebook_id,
                       pb.mrc AS component_mrc, pb.nrc AS component_nrc, pb.setup AS component_setup
                FROM {table} t
                JOIN public.components c ON c.id = t.{id_col}
                JOIN public.component_types ct ON ct.id = c.component_type_id
                LEFT JOIN public.component_types pct ON pct.id = ct.parent_component_id
                JOIN public.component_categories cc ON cc.id = ct.category_id
                LEFT JOIN public.pricebook pb
                    ON pb.component_id = t.{id_col}
                   AND pb.currency = %s
                   AND pb.datacenter = %s
                   AND pb.product_line_id = %s
                   AND pb.is_available = true
                WHERE t.{'product_id' if table == 'public.product_templates' else 'product_id'} = %s
                {'AND c.is_active = true' if table == 'public.product_allowed_components' else ''}
                ORDER BY cc.sort_order, cc.name, ct.name, c.display_name
            """, (pb_currency, fusion_dc_id, product_line, product_id))
            return cur.fetchall()

    # Query defaults + allowed, trying target currency first
    defaults_raw = _query_components("public.product_templates",       "component_id", pricing_currency)
    allowed_raw  = _query_components("public.product_allowed_components", "component_id", pricing_currency)

    # -- Hardware costs from MSSQL
    # Same sku_id can appear as both 'TLS' (server) and 'Component' rows —
    # must query each level separately to avoid mixing them.
    component_ids  = list(
        {r["component_id"] for r in defaults_raw} |
        {r["component_id"] for r in allowed_raw}
    )
    hw_costs_comp  = get_mssql_costs(component_ids, "Component") if component_ids else {}
    hw_costs_tls   = get_mssql_costs([product_id],  "TLS")
    hw_costs       = {**hw_costs_comp, **hw_costs_tls}  # TLS wins on any overlap

    # Build FX rate map for all unique cost currencies found in ocean_sku_cost
    cost_currencies = {v["currency"] for v in hw_costs.values() if v.get("currency")}
    fx_cost_map     = {c: get_fx_rate(c, currency) for c in cost_currencies}

    def _fmt_component(r, is_default=False, quantity=1):
        cid        = r["component_id"]
        mrc_pb     = _dec(r["component_mrc"])  # in pricing_currency
        nrc_pb     = _dec(r["component_nrc"])  # in pricing_currency
        # Default (included) components: pricebook MRC is the add-on price, not an
        # additional charge — the component is already covered by the server base MRC.
        addon_mrc_display   = round(mrc_pb * fx_pricing, 2)
        addon_nrc_display   = round(nrc_pb * fx_pricing, 2)
        # Setup fee for this component (pricebook.setup column)
        setup_pb            = _dec(r.get("component_setup") or 0)
        addon_setup_display = round(setup_pb * fx_pricing, 2)
        mrc_display   = 0.0 if is_default else addon_mrc_display
        nrc_display   = 0.0 if is_default else addon_nrc_display
        setup_display = 0.0 if is_default else addon_setup_display
        pb_id       = r.get("pricebook_id")

        hw = hw_costs.get(cid)
        if hw:
            hw_cost_raw      = hw["cost"]
            hw_cost_currency = hw["currency"]
            fx_cost          = fx_cost_map.get(hw_cost_currency, 1.0)
            hw_cost_display  = round(hw_cost_raw * fx_cost, 2)
        else:
            hw_cost_raw      = None
            hw_cost_currency = None
            fx_cost          = None
            hw_cost_display  = None

        return {
            "component_id":     cid,
            "name":             r["name"],
            "description":      r["description"] or "",
            "is_active":        r["is_active"],
            "component_type":   r["component_type"],
            "parent_type":      r.get("parent_type"),
            "category":         r["category"],
            "cat_sort":         r["cat_sort"],
            "quantity":         quantity,
            "component_mrc":    mrc_display,
            "component_nrc":    nrc_display,
            "component_setup":  setup_display,
            "addon_mrc":        addon_mrc_display,   # pricebook price if added as upgrade
            "addon_setup":      addon_setup_display, # pricebook setup if added as upgrade
            "hw_cost_raw":      hw_cost_raw,
            "hw_cost_currency": hw_cost_currency,
            "hw_cost_display":  hw_cost_display,
            "is_default":       is_default,
            "pricebook_provenance": {
                "source":           "Fusion: public.pricebook",
                "pricebook_id":     pb_id,
                "field":            "pricebook.mrc",
                "filters": (
                    f"component_id={cid}, currency={pricing_currency}, "
                    f"datacenter={fusion_dc_id} ({dc_abbr}), "
                    f"product_line_id={product_line}, is_available=true"
                ),
                "pb_value":         mrc_pb,
                "pricing_currency": pricing_currency,
                "fx_pricing":       fx_pricing,
                "display_value":    addon_mrc_display,
                "display_currency": currency,
                "included_in_base": is_default,
            } if pb_id else None,
            "hw_provenance": {
                "source":          "MSSQL: DM_BusinessInsights.profitability.ocean_sku_cost",
                "field":           "sku_cost",
                "sku_id":          cid,
                "sku_name":        hw["name"] if hw else None,
                "cost_value":      hw_cost_raw,
                "cost_currency":   hw_cost_currency,
                "fx_cost":         fx_cost,
                "fx_source": (
                    f"dbo.dimCurrencyExchangeRates "
                    f"WHERE from_currency='{hw_cost_currency}' AND to_currency='{currency}' "
                    f"ORDER BY start_date DESC"
                ) if hw_cost_currency and hw_cost_currency != currency else None,
                "display_value":    hw_cost_display,
                "display_currency": currency,
                "formula": (
                    f"{hw_cost_raw} {hw_cost_currency} × {fx_cost} = {hw_cost_display} {currency}"
                    if hw_cost_raw else "Not in ocean_sku_cost"
                ),
            } if hw else None,
        }

    defaults    = [_fmt_component(r, is_default=True, quantity=r["quantity"]) for r in defaults_raw]
    allowed     = [_fmt_component(r, is_default=False) for r in allowed_raw]
    default_ids = {r["component_id"] for r in defaults_raw}

    # -- Total MRC (display currency)
    total_mrc = server_mrc + sum(
        d["component_mrc"] * d["quantity"] for d in defaults if d["component_mrc"] > 0
    )

    # -- CapEx: server-level ocean_sku_cost is authoritative; sum components as fallback
    server_hw = hw_costs.get(product_id)
    if server_hw and server_hw["cost"] > 0:
        hw_capex_raw      = server_hw["cost"]
        hw_capex_currency = server_hw["currency"]
        fx_cost_server    = fx_cost_map.get(hw_capex_currency, 1.0)
        total_hw_capex    = round(hw_capex_raw * fx_cost_server, 2)
        hw_capex_method   = "server-level"
        hw_capex_sku_name = server_hw["name"]
    else:
        hw_capex_raw      = sum(
            hw_costs[d["component_id"]]["cost"] * d["quantity"]
            if d["component_id"] in hw_costs else 0
            for d in defaults
        )
        # Use first cost_currency found among components, or USD
        first_hw = next((hw_costs[d["component_id"]] for d in defaults if d["component_id"] in hw_costs), None)
        hw_capex_currency = first_hw["currency"] if first_hw else "USD"
        fx_cost_server    = fx_cost_map.get(hw_capex_currency, 1.0)
        total_hw_capex    = round(hw_capex_raw * fx_cost_server, 2)
        hw_capex_method   = "component-sum"
        hw_capex_sku_name = None

    hw_capex_provenance = {
        "source":          "MSSQL: DM_BusinessInsights.profitability.ocean_sku_cost",
        "field":           "sku_cost",
        "sku_id":          product_id if hw_capex_method == "server-level" else "multiple",
        "sku_name":        hw_capex_sku_name,
        "method":          hw_capex_method,
        "cost_value":      hw_capex_raw,
        "cost_currency":   hw_capex_currency,
        "fx_cost":         fx_cost_server,
        "fx_source": (
            f"dbo.dimCurrencyExchangeRates "
            f"WHERE from_currency='{hw_capex_currency}' AND to_currency='{currency}' "
            f"ORDER BY start_date DESC"
        ) if hw_capex_currency != currency else "same currency — no conversion",
        "display_value":    total_hw_capex,
        "display_currency": currency,
        "formula":          f"{hw_capex_raw} {hw_capex_currency} × {fx_cost_server} = {total_hw_capex} {currency}",
    }

    # -- Wattage (hardware_watts keyed by fusion product_id)
    server_watts = get_mssql_watts(product_id)
    server_kw    = round(server_watts / 1000, 4) if server_watts is not None else None

    # -- Overhead (amounts in native_currency, converted via fx_overhead)
    overhead = calc_overhead(dc_abbr, total_mrc, fx_rate=fx_overhead, kw=server_kw)

    return jsonify({
        "product_id":          product_id,
        "server_mrc":          server_mrc,
        "server_nrc":          server_nrc,
        "server_setup":        server_setup,
        "currency":            currency,
        "native_currency":     native_currency,
        "pricing_currency":    pricing_currency,
        "dc_code":             dc_abbr,
        "fusion_dc_id":        fusion_dc_id,
        "product_line":        int(product_line),
        "term_months":         term_months,
        "fx_pricing":          fx_pricing,
        "fx_overhead":         fx_overhead,
        "fx_source":           "MSSQL: DM_BusinessInsights.dbo.dimCurrencyExchangeRates",
        "defaults":            defaults,
        "allowed":             allowed,
        "default_ids":         list(default_ids),
        "server_watts":        server_watts,
        "server_kw":           server_kw,
        "overhead":            overhead,
        "total_hw_capex":      total_hw_capex,
        "hw_capex_cost":       hw_capex_raw,
        "hw_capex_currency":   hw_capex_currency,
        "hw_capex_provenance": hw_capex_provenance,
        "total_mrc":           round(total_mrc, 2),
        "server_mrc_provenance": pb_provenance,
    })


# ---------------------------------------------------------------------------
# Routes — Settings
# ---------------------------------------------------------------------------
@app.route("/settings")
def settings_page():
    return render_template("settings.html")


@app.route("/api/settings/overhead", methods=["GET"])
def settings_overhead_get():
    return jsonify(COST_DRIVERS)


@app.route("/api/settings/overhead", methods=["POST"])
def settings_overhead_post():
    global COST_DRIVERS
    data = request.get_json(force=True)

    # Validate sga_pct
    try:
        sga = float(data.get("overhead_constants", {}).get("sga_pct", -1))
        if not (0 <= sga <= 1):
            return jsonify({"error": "sga_pct must be between 0 and 1"}), 400
    except (TypeError, ValueError):
        return jsonify({"error": "sga_pct must be a number"}), 400

    # Validate all cost amounts are non-negative numbers
    service_types = ["server", "firewall", "switch"]
    for dc_abbr, dc in data.get("data_centers", {}).items():
        for svc in service_types:
            for key, entry in dc.get("costs", {}).get(svc, {}).items():
                try:
                    if float(entry.get("amount", -1)) < 0:
                        return jsonify({"error": f"{dc_abbr}.{svc}.{key}: amount must be >= 0"}), 400
                except (TypeError, ValueError):
                    return jsonify({"error": f"{dc_abbr}.{svc}.{key}: amount must be a number"}), 400

    # Atomic write
    path = _COST_DRIVERS_PATH
    tmp  = path.with_suffix(".json.tmp")
    try:
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        os.replace(tmp, path)
    except Exception as e:
        return jsonify({"error": f"Write failed: {e}"}), 500

    # Reload in-memory cache
    with open(path) as f:
        COST_DRIVERS = json.load(f)

    return jsonify({"ok": True})


if __name__ == "__main__":
    if not SSH_USER or not DB_PASSWORD:
        print("ERROR: SSH_USER or FUSION_DB_PASS not set", file=sys.stderr)
        sys.exit(1)
    app.run(debug=True, port=5050)
