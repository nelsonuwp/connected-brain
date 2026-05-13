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

# Map fusion_dc_id → our DC code for fast lookup
_FUSION_DC_ID_TO_CODE = {
    v["fusion_dc_id"]: k for k, v in COST_DRIVERS["data_centers"].items()
}

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
# MSSQL connection (per-request, lazy)
# ---------------------------------------------------------------------------
def get_mssql_costs(component_ids: list[int]) -> dict[int, float]:
    """Return {component_id: sku_cost_usd} for the given ids. Returns {} on failure."""
    if not component_ids or not all([MSSQL_SERVER, MSSQL_DB, MSSQL_USER, MSSQL_PASSWORD]):
        return {}
    try:
        import pymssql
        conn = pymssql.connect(
            server=MSSQL_SERVER, user=MSSQL_USER,
            password=MSSQL_PASSWORD, database=MSSQL_DB,
        )
        cur = conn.cursor(as_dict=True)
        placeholders = ",".join(["%d"] * len(component_ids))
        cur.execute(
            f"SELECT sku_id, sku_cost, cost_currency FROM profitability.ocean_sku_cost "
            f"WHERE sku_id IN ({placeholders})",
            tuple(component_ids),
        )
        result = {r["sku_id"]: float(r["sku_cost"] or 0) for r in cur.fetchall()}
        cur.close()
        conn.close()
        return result
    except Exception:
        return {}


def get_fx_rate(from_currency: str, to_currency: str) -> float:
    """Return exchange rate from_currency → to_currency from MSSQL DM_BusinessInsights.
    Falls back to 1.0 if unavailable or same currency."""
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
            "SELECT TOP 1 ExchangeRate FROM dbo.dimCurrencyExchangeRates "
            "WHERE FromCurrencyCode = %s AND ToCurrencyCode = %s "
            "ORDER BY EffectiveDate DESC",
            (from_currency, to_currency),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row and row.get("ExchangeRate"):
            return float(row["ExchangeRate"])
    except Exception:
        pass
    return 1.0


# ---------------------------------------------------------------------------
# Cost calculation helpers
# ---------------------------------------------------------------------------
def calc_overhead(dc_code: str, mrc: float, kw: float | None = None) -> dict:
    dc = COST_DRIVERS["data_centers"].get(dc_code)
    if not dc:
        return {}
    costs = dc["costs"]
    const = COST_DRIVERS["overhead_constants"]
    lines = {}

    for key, entry in costs.items():
        amt = entry["amount"]
        measure = entry["measure"]
        if amt == 0:
            lines[key] = {"amount": 0, "currency": entry["currency"], "measure": measure}
            continue
        if measure == "per_kw":
            val = round(amt * kw, 2) if kw is not None else None
        elif measure == "per_server":
            val = round(amt, 2)
        elif measure == "per_hour":
            val = round(amt * const["support_hours_per_server"], 2)
        else:
            val = round(amt, 2)
        lines[key] = {"amount": val, "currency": entry["currency"], "measure": measure}

    sga = round(mrc * const["sga_pct"], 2) if mrc else 0
    lines["sga"] = {"amount": sga, "currency": dc["native_currency"], "measure": "pct_of_mrc"}
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
    return render_template("index.html", cost_drivers=COST_DRIVERS)


@app.route("/product/<int:product_id>")
def product_page(product_id):
    return render_template("product.html", product_id=product_id)


# ---------------------------------------------------------------------------
# Routes — API
# ---------------------------------------------------------------------------
@app.route("/api/product-classes")
def product_classes():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM public.product_classes ORDER BY sort_order, name")
        return jsonify([dict(r) for r in cur.fetchall()])


@app.route("/api/products/<int:class_id>")
def products_legacy(class_id):
    show_inactive = request.args.get("show_inactive", "false").lower() == "true"
    conn = get_conn()
    with conn.cursor() as cur:
        if show_inactive:
            cur.execute(
                "SELECT id, name, description, is_active, sku, available_in_shop, sold_out, "
                "limited_availability, release_date FROM public.product_catalog "
                "WHERE product_class = %s ORDER BY name", (class_id,))
        else:
            cur.execute(
                "SELECT id, name, description, is_active, sku, available_in_shop, sold_out, "
                "limited_availability, release_date FROM public.product_catalog "
                "WHERE product_class = %s AND is_active = true ORDER BY name", (class_id,))
        return jsonify([dict(r) for r in cur.fetchall()])


@app.route("/api/datacenters")
def datacenters():
    """Return the 7 DCs from cost_drivers.json enriched with Fusion abbr."""
    return jsonify([
        {
            "code": code,
            "name": dc["name"],
            "native_currency": dc["native_currency"],
            "fusion_dc_id": dc["fusion_dc_id"],
        }
        for code, dc in COST_DRIVERS["data_centers"].items()
    ])


@app.route("/api/fx-rate")
def fx_rate():
    """Return exchange rate between two currencies."""
    from_cur = request.args.get("from", "USD").upper()
    to_cur   = request.args.get("to", "USD").upper()
    rate = get_fx_rate(from_cur, to_cur)
    return jsonify({"from": from_cur, "to": to_cur, "rate": rate})


@app.route("/api/servers")
def servers():
    """
    Active servers with pricebook pricing.
    Query params: dc (our code e.g. ATL), currency (USD/CAD/GBP), product_line (3 or 4)
    """
    dc_code      = request.args.get("dc", "")
    currency     = request.args.get("currency", "USD").upper()
    product_line = request.args.get("product_line", "4")

    dc_info = COST_DRIVERS["data_centers"].get(dc_code)
    if not dc_info:
        return jsonify({"error": f"Unknown DC: {dc_code}"}), 400

    fusion_dc_id = dc_info["fusion_dc_id"]

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
        """, (currency, fusion_dc_id, product_line))
        rows = cur.fetchall()

    return jsonify([
        {**dict(r), "mrc": _dec(r["mrc"]), "nrc": _dec(r["nrc"]), "setup": _dec(r["setup"])}
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
    Returns defaults, allowed components, pricebook MRCs, hardware costs, overhead.
    Query params: dc, currency, product_line
    """
    dc_code      = request.args.get("dc", "ATL")
    currency     = request.args.get("currency", "USD").upper()
    product_line = request.args.get("product_line", "4")

    dc_info = COST_DRIVERS["data_centers"].get(dc_code)
    if not dc_info:
        return jsonify({"error": f"Unknown DC: {dc_code}"}), 400

    fusion_dc_id = dc_info["fusion_dc_id"]
    conn = get_conn()

    # -- Server base price
    with conn.cursor() as cur:
        cur.execute("""
            SELECT pb.mrc, pb.nrc, pb.setup
            FROM public.pricebook pb
            WHERE pb.product_catalog_id = %s
              AND pb.component_id IS NULL
              AND pb.currency = %s
              AND pb.datacenter = %s
              AND pb.product_line_id = %s
              AND pb.is_available = true
            LIMIT 1
        """, (product_id, currency, fusion_dc_id, product_line))
        pb_row = cur.fetchone()
    server_mrc = _dec(pb_row["mrc"]) if pb_row else 0

    # -- Default components (product_templates)
    with conn.cursor() as cur:
        cur.execute("""
            SELECT pt.component_id, pt.quantity,
                   c.display_name AS name, c.description, c.is_active,
                   ct.name AS component_type,
                   cc.name AS category, cc.sort_order AS cat_sort,
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
        """, (currency, fusion_dc_id, product_line, product_id))
        defaults_raw = cur.fetchall()

    # -- Allowed components (product_allowed_components)
    with conn.cursor() as cur:
        cur.execute("""
            SELECT pac.component_id, pac.available_in_shop,
                   c.display_name AS name, c.description, c.is_active,
                   ct.name AS component_type,
                   cc.name AS category, cc.sort_order AS cat_sort,
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
        """, (currency, fusion_dc_id, product_line, product_id))
        allowed_raw = cur.fetchall()

    # -- Hardware costs from MSSQL
    all_ids = list({r["component_id"] for r in defaults_raw} |
                   {r["component_id"] for r in allowed_raw})
    hw_costs = get_mssql_costs(all_ids)

    def _fmt_component(r, is_default=False, quantity=1):
        cid = r["component_id"]
        return {
            "component_id":    cid,
            "name":            r["name"],
            "description":     r["description"] or "",
            "is_active":       r["is_active"],
            "component_type":  r["component_type"],
            "category":        r["category"],
            "cat_sort":        r["cat_sort"],
            "quantity":        quantity,
            "component_mrc":   _dec(r["component_mrc"]),
            "component_nrc":   _dec(r["component_nrc"]),
            "hw_cost_usd":     hw_costs.get(cid),
            "is_default":      is_default,
        }

    defaults = [_fmt_component(r, is_default=True, quantity=r["quantity"]) for r in defaults_raw]
    allowed  = [_fmt_component(r, is_default=False) for r in allowed_raw]

    # Default component_ids for quick lookup in frontend
    default_ids = {r["component_id"] for r in defaults_raw}

    # -- Overhead calculation
    # Total MRC = server base + sum of default component MRCs that have a price
    total_mrc = server_mrc + sum(
        d["component_mrc"] * d["quantity"] for d in defaults if d["component_mrc"] > 0
    )
    overhead = calc_overhead(dc_code, total_mrc, kw=None)

    # Total hardware CapEx (sum of default component costs, stored in USD in MSSQL)
    total_hw_capex = sum(
        (hw_costs.get(d["component_id"]) or 0) * d["quantity"]
        for d in defaults
    )

    # FX rate: hw_costs are USD; overhead costs are in DC native currency
    native_currency = dc_info["native_currency"]
    fx_to_selected  = get_fx_rate(native_currency, currency)   # overhead → display currency
    fx_usd_to_selected = get_fx_rate("USD", currency)          # hw cost → display currency

    return jsonify({
        "server_mrc":          server_mrc,
        "server_nrc":          _dec(pb_row["nrc"]) if pb_row else 0,
        "currency":            currency,
        "native_currency":     native_currency,
        "dc_code":             dc_code,
        "product_line":        int(product_line),
        "defaults":            defaults,
        "allowed":             allowed,
        "default_ids":         list(default_ids),
        "overhead":            overhead,
        "total_hw_capex":      total_hw_capex,
        "total_mrc":           round(total_mrc, 2),
        "fx_native_to_display": fx_to_selected,
        "fx_usd_to_display":    fx_usd_to_selected,
    })


if __name__ == "__main__":
    if not SSH_USER or not DB_PASSWORD:
        print("ERROR: SSH_USER or FUSION_DB_PASS not set", file=sys.stderr)
        sys.exit(1)
    app.run(debug=True, port=5050)
