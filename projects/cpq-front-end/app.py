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
# Static data
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
# MSSQL: hardware costs
# Returns {sku_id: {"cost": float, "currency": str, "name": str}}
# sku_id = product_catalog.id (server-level) OR component.id (component-level)
# ---------------------------------------------------------------------------
def get_mssql_costs(sku_ids: list[int]) -> dict[int, dict]:
    if not sku_ids or not all([MSSQL_SERVER, MSSQL_DB, MSSQL_USER, MSSQL_PASSWORD]):
        return {}
    try:
        import pymssql
        conn = pymssql.connect(
            server=MSSQL_SERVER, user=MSSQL_USER,
            password=MSSQL_PASSWORD, database=MSSQL_DB,
        )
        cur = conn.cursor(as_dict=True)
        placeholders = ",".join(["%d"] * len(sku_ids))
        cur.execute(
            f"SELECT sku_id, sku_name, sku_cost, cost_currency "
            f"FROM profitability.ocean_sku_cost "
            f"WHERE sku_id IN ({placeholders})",
            tuple(sku_ids),
        )
        result = {
            r["sku_id"]: {
                "cost":     float(r["sku_cost"] or 0),
                "currency": r["cost_currency"] or "USD",
                "name":     r["sku_name"] or "",
            }
            for r in cur.fetchall()
        }
        cur.close()
        conn.close()
        return result
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# MSSQL: FX rates
# Columns confirmed: from_currency, to_currency, exchange_rate, start_date
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
# All amounts returned are already in display_currency (after fx_rate applied).
# native_amount is preserved in provenance for tooltip display.
# ---------------------------------------------------------------------------
def calc_overhead(dc_code: str, mrc_display: float, fx_rate: float = 1.0,
                  kw: float | None = None) -> dict:
    dc = COST_DRIVERS["data_centers"].get(dc_code)
    if not dc:
        return {}
    costs  = dc["costs"]
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
                    "path": f"data_centers.{dc_code}.costs.{key}",
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
        elif measure == "per_server":
            native_val = round(amt, 2)
            formula    = f"{amt} {native}/server"
        elif measure == "per_hour":
            hrs        = const["support_hours_per_server"]
            native_val = round(amt * hrs, 2)
            formula    = f"{amt} {native}/hr × {hrs} hrs/server = {native_val} {native}"
        else:
            native_val = round(amt, 2)
            formula    = str(amt)

        display_val = round(native_val * fx_rate, 2) if native_val is not None else None
        if fx_rate != 1.0 and native_val is not None:
            formula += f" × {fx_rate} FX = {display_val}"

        lines[key] = {
            "amount":   display_val,
            "currency": native,       # kept for label reference
            "measure":  measure,
            "provenance": {
                "source":          "cost_drivers.json",
                "path":            f"data_centers.{dc_code}.costs.{key}",
                "native_amount":   native_val,
                "native_currency": native,
                "measure":         measure,
                "formula":         formula,
                "fx_rate":         fx_rate,
            },
        }

    sga_pct    = const["sga_pct"]
    sga_val    = round(mrc_display * sga_pct, 2) if mrc_display else 0
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
    return jsonify([
        {
            "code":            code,
            "name":            dc["name"],
            "native_currency": dc["native_currency"],
            "fusion_dc_id":    dc["fusion_dc_id"],
        }
        for code, dc in COST_DRIVERS["data_centers"].items()
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
    Active servers with pricebook pricing.
    Query params: dc, currency (display), product_line
    Always queries pricebook in native DC currency, converts to display currency.
    """
    dc_code      = request.args.get("dc", "")
    currency     = request.args.get("currency", "USD").upper()
    product_line = request.args.get("product_line", "4")

    dc_info = COST_DRIVERS["data_centers"].get(dc_code)
    if not dc_info:
        return jsonify({"error": f"Unknown DC: {dc_code}"}), 400

    fusion_dc_id    = dc_info["fusion_dc_id"]
    native_currency = dc_info["native_currency"]

    # Always query pricebook in native DC currency
    fx = get_fx_rate(native_currency, currency)

    conn = get_conn()
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
        """, (native_currency, fusion_dc_id, product_line))
        rows = cur.fetchall()

    return jsonify([
        {
            **dict(r),
            "mrc":             round(_dec(r["mrc"]) * fx, 2),
            "nrc":             round(_dec(r["nrc"]) * fx, 2),
            "setup":           round(_dec(r["setup"]) * fx, 2),
            "native_currency": native_currency,
            "display_currency": currency,
            "fx_rate":         fx,
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
    Query params: dc, currency (display), product_line, term (12/24/36, display only)
    """
    dc_code      = request.args.get("dc", "ATL")
    currency     = request.args.get("currency", "USD").upper()
    product_line = request.args.get("product_line", "4")
    term_months  = int(request.args.get("term", "36"))

    dc_info = COST_DRIVERS["data_centers"].get(dc_code)
    if not dc_info:
        return jsonify({"error": f"Unknown DC: {dc_code}"}), 400

    fusion_dc_id    = dc_info["fusion_dc_id"]
    native_currency = dc_info["native_currency"]

    # FX rates (both needed for provenance)
    fx_native = get_fx_rate(native_currency, currency)   # pricebook + overhead → display
    fx_usd    = get_fx_rate("USD", currency)             # MSSQL hw costs (always USD) → display
    conn = get_conn()

    # -- Server base price (queried in native DC currency)
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
        """, (product_id, native_currency, fusion_dc_id, product_line))
        pb_row = cur.fetchone()

    server_mrc_native = _dec(pb_row["mrc"])  if pb_row else 0
    server_nrc_native = _dec(pb_row["nrc"])  if pb_row else 0
    server_mrc        = round(server_mrc_native * fx_native, 2)
    server_nrc        = round(server_nrc_native * fx_native, 2)
    pricebook_id      = pb_row["pricebook_id"] if pb_row else None

    pb_provenance = {
        "source":  "Fusion: public.pricebook",
        "filters": (
            f"product_catalog_id={product_id}, currency={native_currency}, "
            f"datacenter={fusion_dc_id} ({dc_code}), product_line_id={product_line}, "
            f"component_id IS NULL, is_available=true"
        ),
        "pricebook_id":    pricebook_id,
        "field":           "pricebook.mrc",
        "native_value":    server_mrc_native,
        "native_currency": native_currency,
        "fx_rate":         fx_native,
        "fx_source":       f"MSSQL: dbo.dimCurrencyExchangeRates WHERE from_currency='{native_currency}' AND to_currency='{currency}' ORDER BY start_date DESC",
        "display_value":   server_mrc,
        "display_currency": currency,
    }

    # -- Default components (queried in native DC currency)
    with conn.cursor() as cur:
        cur.execute("""
            SELECT pt.component_id, pt.quantity,
                   c.display_name AS name, c.description, c.is_active,
                   ct.name AS component_type,
                   cc.name AS category, cc.sort_order AS cat_sort,
                   pb.id AS pricebook_id,
                   pb.mrc AS component_mrc, pb.nrc AS component_nrc
            FROM public.product_templates pt
            JOIN public.components c ON c.id = pt.component_id
            JOIN public.component_types ct ON ct.id = c.component_type_id
            JOIN public.component_categories cc ON cc.id = ct.category_id
            LEFT JOIN public.pricebook pb
                ON pb.component_id = pt.component_id
               AND pb.currency = %s
               AND pb.datacenter = %s
               AND pb.product_line_id = %s
               AND pb.is_available = true
            WHERE pt.product_id = %s
            ORDER BY cc.sort_order, cc.name, ct.name, c.display_name
        """, (native_currency, fusion_dc_id, product_line, product_id))
        defaults_raw = cur.fetchall()

    # -- Allowed components (queried in native DC currency)
    with conn.cursor() as cur:
        cur.execute("""
            SELECT pac.component_id, pac.available_in_shop,
                   c.display_name AS name, c.description, c.is_active,
                   ct.name AS component_type,
                   cc.name AS category, cc.sort_order AS cat_sort,
                   pb.id AS pricebook_id,
                   pb.mrc AS component_mrc, pb.nrc AS component_nrc
            FROM public.product_allowed_components pac
            JOIN public.components c ON c.id = pac.component_id
            JOIN public.component_types ct ON ct.id = c.component_type_id
            JOIN public.component_categories cc ON cc.id = ct.category_id
            LEFT JOIN public.pricebook pb
                ON pb.component_id = pac.component_id
               AND pb.currency = %s
               AND pb.datacenter = %s
               AND pb.product_line_id = %s
               AND pb.is_available = true
            WHERE pac.product_id = %s
              AND c.is_active = true
            ORDER BY cc.sort_order, cc.name, ct.name, c.display_name
        """, (native_currency, fusion_dc_id, product_line, product_id))
        allowed_raw = cur.fetchall()

    # -- Hardware costs from MSSQL
    # Include product_id itself — server-level sku_cost is the authoritative CapEx
    component_ids = list(
        {r["component_id"] for r in defaults_raw} |
        {r["component_id"] for r in allowed_raw}
    )
    all_sku_ids = component_ids + [product_id]
    hw_costs = get_mssql_costs(all_sku_ids)

    def _fmt_component(r, is_default=False, quantity=1):
        cid          = r["component_id"]
        mrc_native   = _dec(r["component_mrc"])
        nrc_native   = _dec(r["component_nrc"])
        mrc_display  = round(mrc_native * fx_native, 2)
        nrc_display  = round(nrc_native * fx_native, 2)
        hw           = hw_costs.get(cid)
        hw_cost_usd  = hw["cost"] if hw else None
        hw_cost_disp = round(hw_cost_usd * fx_usd, 2) if hw_cost_usd is not None else None
        pb_id        = r.get("pricebook_id")
        return {
            "component_id":    cid,
            "name":            r["name"],
            "description":     r["description"] or "",
            "is_active":       r["is_active"],
            "component_type":  r["component_type"],
            "category":        r["category"],
            "cat_sort":        r["cat_sort"],
            "quantity":        quantity,
            "component_mrc":   mrc_display,
            "component_nrc":   nrc_display,
            "hw_cost_usd":     hw_cost_usd,   # raw USD for reference
            "hw_cost_display": hw_cost_disp,  # converted to display currency
            "is_default":      is_default,
            "pricebook_provenance": {
                "source":          "Fusion: public.pricebook",
                "pricebook_id":    pb_id,
                "field":           "pricebook.mrc",
                "filters":         (
                    f"component_id={cid}, currency={native_currency}, "
                    f"datacenter={fusion_dc_id} ({dc_code}), "
                    f"product_line_id={product_line}, is_available=true"
                ),
                "native_value":    mrc_native,
                "native_currency": native_currency,
                "fx_rate":         fx_native,
                "display_value":   mrc_display,
                "display_currency": currency,
            } if pb_id else None,
            "hw_provenance": {
                "source":          "MSSQL: DM_BusinessInsights.profitability.ocean_sku_cost",
                "field":           "sku_cost",
                "sku_id":          cid,
                "sku_name":        hw["name"] if hw else None,
                "usd_value":       hw_cost_usd,
                "fx_rate":         fx_usd,
                "fx_source":       f"dbo.dimCurrencyExchangeRates WHERE from_currency='USD' AND to_currency='{currency}'",
                "display_value":   hw_cost_disp,
                "display_currency": currency,
                "formula":         f"{hw_cost_usd} USD × {fx_usd} = {hw_cost_disp} {currency}" if hw_cost_usd else "Not in ocean_sku_cost",
            } if hw else None,
        }

    defaults = [_fmt_component(r, is_default=True, quantity=r["quantity"]) for r in defaults_raw]
    allowed  = [_fmt_component(r, is_default=False) for r in allowed_raw]
    default_ids = {r["component_id"] for r in defaults_raw}

    # -- Total MRC (in display currency)
    total_mrc = server_mrc + sum(
        d["component_mrc"] * d["quantity"] for d in defaults if d["component_mrc"] > 0
    )

    # -- CapEx: use server-level sku_cost from ocean_sku_cost as authoritative total
    server_hw = hw_costs.get(product_id)
    if server_hw and server_hw["cost"] > 0:
        total_hw_capex_usd = server_hw["cost"]
        hw_capex_method    = "server-level"
        hw_capex_sku_name  = server_hw["name"]
    else:
        # Fallback: sum component costs
        total_hw_capex_usd = sum(
            (hw_costs[d["component_id"]]["cost"] if d["component_id"] in hw_costs else 0)
            * d["quantity"]
            for d in defaults
        )
        hw_capex_method    = "component-sum"
        hw_capex_sku_name  = None

    total_hw_capex_display = round(total_hw_capex_usd * fx_usd, 2)

    hw_capex_provenance = {
        "source":          "MSSQL: DM_BusinessInsights.profitability.ocean_sku_cost",
        "field":           "sku_cost",
        "sku_id":          product_id if hw_capex_method == "server-level" else "multiple",
        "sku_name":        hw_capex_sku_name,
        "method":          hw_capex_method,
        "usd_value":       total_hw_capex_usd,
        "fx_rate":         fx_usd,
        "fx_source":       f"dbo.dimCurrencyExchangeRates WHERE from_currency='USD' AND to_currency='{currency}' ORDER BY start_date DESC",
        "display_value":   total_hw_capex_display,
        "display_currency": currency,
        "formula":         f"{total_hw_capex_usd} USD × {fx_usd} = {total_hw_capex_display} {currency}",
    }

    # -- Overhead (all amounts already converted to display currency inside calc_overhead)
    overhead = calc_overhead(dc_code, total_mrc, fx_rate=fx_native, kw=None)

    return jsonify({
        "product_id":        product_id,
        "server_mrc":        server_mrc,
        "server_nrc":        server_nrc,
        "currency":          currency,
        "native_currency":   native_currency,
        "dc_code":           dc_code,
        "fusion_dc_id":      fusion_dc_id,
        "product_line":      int(product_line),
        "term_months":       term_months,
        "fx_native":         fx_native,
        "fx_usd":            fx_usd,
        "fx_source":         "MSSQL: DM_BusinessInsights.dbo.dimCurrencyExchangeRates",
        "fx_query":          f"from_currency → to_currency, ORDER BY start_date DESC",
        "defaults":          defaults,
        "allowed":           allowed,
        "default_ids":       list(default_ids),
        "overhead":          overhead,
        "total_hw_capex":    total_hw_capex_display,
        "hw_capex_usd":      total_hw_capex_usd,
        "hw_capex_provenance": hw_capex_provenance,
        "total_mrc":         round(total_mrc, 2),
        "server_mrc_provenance": pb_provenance,
    })


if __name__ == "__main__":
    if not SSH_USER or not DB_PASSWORD:
        print("ERROR: SSH_USER or FUSION_DB_PASS not set", file=sys.stderr)
        sys.exit(1)
    app.run(debug=True, port=5050)
