# Profitability Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `/profitability` page to the CPQ front-end that shows margin (MRC minus CPQ-modelled cost) across all active services, grouped by customer / DC / service type, with a customer drill-down that shows per-service cost breakdowns.

**Architecture:** New Flask blueprint (`routes/profitability.py`) + data layer (`db/profitability.py`) + two Jinja2 templates. Cost calculation reuses `lib/overhead.py` and `lib/renewal_pricing.py` unchanged. All DB calls are batched — one SQL query for services, one for HW costs, one for watts. Currency conversion happens client-side via existing `/api/fx-rate` endpoint.

**Tech Stack:** Python/Flask, pymssql, psycopg2 (via existing db modules), Jinja2, vanilla JS (Fetch API), same CSS variable system as all other pages.

---

### Task 1: Wire up nav link and empty blueprint

**Files:**
- Modify: `templates/base.html:77-80`
- Create: `routes/profitability.py`
- Modify: `app.py:8-15`

- [ ] **Step 1: Add Profitability to the nav in base.html**

In `templates/base.html`, find the `<nav class="top-nav">` block (lines 77-80) and replace it with:

```html
  <nav class="top-nav">
    <a href="/" class="{{ 'active' if active_page == 'quotes' else '' }}">New Quotes</a>
    <a href="/profitability" class="{{ 'active' if active_page == 'profitability' else '' }}">Profitability</a>
    <a href="/renewals" class="{{ 'active' if active_page == 'renewals' else '' }}">Renewals</a>
    <a href="/settings" class="{{ 'active' if active_page == 'settings' else '' }}">Settings</a>
  </nav>
```

- [ ] **Step 2: Create empty blueprint at `routes/profitability.py`**

```python
from flask import Blueprint, jsonify, render_template, request

profitability_bp = Blueprint("profitability", __name__)


@profitability_bp.route("/profitability")
def profitability_page():
    return render_template("profitability.html", active_page="profitability")


@profitability_bp.route("/profitability/<int:client_id>")
def profitability_customer_page(client_id):
    return render_template(
        "profitability_customer.html",
        client_id=client_id,
        active_page="profitability",
    )


@profitability_bp.route("/api/profitability/filter-options")
def api_profitability_filter_options():
    return jsonify({"account_managers": [], "dc_codes": [], "service_types": []})


@profitability_bp.route("/api/profitability")
def api_profitability():
    return jsonify({"by_customer": [], "by_dc": [], "by_service_type": [], "totals": {}})


@profitability_bp.route("/api/profitability/<int:client_id>")
def api_profitability_customer(client_id):
    return jsonify({"services": [], "summary": {}})
```

- [ ] **Step 3: Register blueprint in `app.py`**

```python
from dotenv import load_dotenv

load_dotenv(".env")
load_dotenv(".env.local", override=True)

from flask import Flask

from routes.cpq import cpq_bp
from routes.profitability import profitability_bp
from routes.renewals import renewals_bp
from routes.settings import settings_bp

app = Flask(__name__)
app.register_blueprint(cpq_bp)
app.register_blueprint(profitability_bp)
app.register_blueprint(renewals_bp)
app.register_blueprint(settings_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
```

- [ ] **Step 4: Create placeholder templates**

Create `templates/profitability.html`:
```html
{% extends "base.html" %}
{% block title %}CPQ — Profitability · Aptum{% endblock %}
{% block body %}
<div class="page-body">
  <p style="color:var(--text-2)">Profitability — coming soon</p>
</div>
{% endblock %}
```

Create `templates/profitability_customer.html`:
```html
{% extends "base.html" %}
{% block title %}CPQ — Profitability · Aptum{% endblock %}
{% block body %}
<div class="page-body">
  <p style="color:var(--text-2)">Customer detail — coming soon (id: {{ client_id }})</p>
</div>
{% endblock %}
```

- [ ] **Step 5: Smoke-test the routes**

Run: `make run` (or `make` to build first)

Open http://127.0.0.1:5050/profitability — should show "Profitability — coming soon" and the nav should have the Profitability link highlighted.

Open http://127.0.0.1:5050/profitability/1 — should show the customer detail placeholder.

- [ ] **Step 6: Commit**

```bash
git add templates/base.html routes/profitability.py app.py templates/profitability.html templates/profitability_customer.html
git commit -m "feat: wire up profitability blueprint and nav link"
```

---

### Task 2: Add `get_mssql_watts_batch()` to `db/mssql.py`

The existing `get_mssql_watts()` fetches watts for a single `fusion_id`. We need a batch version to avoid N+1 queries when loading all active services.

**Files:**
- Modify: `db/mssql.py`

- [ ] **Step 1: Add the batch function after `get_mssql_watts()` (around line 73)**

```python
def get_mssql_watts_batch(fusion_ids: list[int]) -> dict[int, int]:
    """Returns {fusion_id: watts} for all given fusion_ids."""
    if not fusion_ids or not _configured():
        return {}
    try:
        conn = _connect()
        cur = conn.cursor(as_dict=True)
        placeholders = ",".join(["%d"] * len(fusion_ids))
        cur.execute(
            f"SELECT fusion_id, watts FROM profitability.hardware_watts "
            f"WHERE fusion_id IN ({placeholders})",
            tuple(fusion_ids),
        )
        result = {r["fusion_id"]: int(r["watts"]) for r in cur.fetchall() if r.get("watts") is not None}
        cur.close()
        conn.close()
        return result
    except Exception:
        return {}
```

- [ ] **Step 2: Commit**

```bash
git add db/mssql.py
git commit -m "feat: add get_mssql_watts_batch for bulk profitability queries"
```

---

### Task 3: `db/profitability.py` — data fetching + cost calculation

**Files:**
- Create: `db/profitability.py`
- Create: `tests/test_profitability.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_profitability.py`:

```python
from datetime import date
from db.profitability import calc_service_margin
from lib.overhead import COST_DRIVERS


def test_calc_service_margin_with_hw_not_paid_off():
    # ATL server: power=337/kW, network_eq=59, dc_ops=21, support_ops=40, sga=8.2%
    # 1200W = 1.2kW, power = 1.2 * 337 = 404.4
    # direct = 404.4 + 0 + 59 + 21 + 40 + 0 + 0 = 524.4
    # sga = 5000 * 0.082 = 410.0
    # hw_amortized = 72000 / 36 = 2000.0
    # total_cost = 2000.0 + 524.4 + 410.0 = 2934.4
    # margin = 5000 - 2934.4 = 2065.6
    result = calc_service_margin(
        mrc=5000.0,
        dc_code="ATL",
        hw_capex_in_currency=72000.0,
        watts=1200,
        fx_overhead=1.0,
        provision_date=date(2024, 1, 1),
    )
    assert result["hw_amortized"] == 2000.0
    assert result["total_cost"] == 2934.4
    assert result["margin"] == 2065.6
    assert result["margin_pct"] == 41.3
    assert result["hw_paid_off"] is False
    assert result["hw_months_remaining"] is not None
    assert result["biggest_cost_driver"] == "hw_amortized"


def test_calc_service_margin_hw_paid_off():
    # provision_date > 36 months ago — hw_amortized = 0
    result = calc_service_margin(
        mrc=5000.0,
        dc_code="ATL",
        hw_capex_in_currency=72000.0,
        watts=1200,
        fx_overhead=1.0,
        provision_date=date(2020, 1, 1),
    )
    assert result["hw_amortized"] == 0.0
    assert result["hw_paid_off"] is True


def test_calc_service_margin_no_watts():
    # Without watts, power_per_kw line is None, should be treated as 0 in total
    result = calc_service_margin(
        mrc=5000.0,
        dc_code="ATL",
        hw_capex_in_currency=0.0,
        watts=None,
        fx_overhead=1.0,
        provision_date=date(2024, 1, 1),
    )
    assert result["margin"] == round(5000.0 - result["total_cost"], 2)


def test_calc_service_margin_no_provision_date():
    # No provision date → hw not paid off (conservative assumption), age_months None
    result = calc_service_margin(
        mrc=5000.0,
        dc_code="ATL",
        hw_capex_in_currency=36000.0,
        watts=None,
        fx_overhead=1.0,
        provision_date=None,
    )
    assert result["hw_paid_off"] is False
    assert result["hw_months_remaining"] is None


def test_calc_service_margin_unknown_dc():
    # Unknown DC → calc_overhead returns {} → only sga and hw_amortized
    result = calc_service_margin(
        mrc=5000.0,
        dc_code="NOTADC",
        hw_capex_in_currency=36000.0,
        watts=None,
        fx_overhead=1.0,
        provision_date=date(2024, 1, 1),
    )
    sga = round(5000.0 * COST_DRIVERS["overhead_constants"]["sga_pct"], 2)
    hw = round(36000.0 / 36, 2)
    assert result["total_cost"] == round(hw + sga, 2)


def test_calc_service_margin_fx_overhead():
    # fx_overhead=1.3 should scale all overhead amounts (but not hw_amortized)
    r_1x = calc_service_margin(
        mrc=5000.0, dc_code="ATL", hw_capex_in_currency=0.0,
        watts=1200, fx_overhead=1.0, provision_date=date(2020, 1, 1),
    )
    r_fx = calc_service_margin(
        mrc=5000.0, dc_code="ATL", hw_capex_in_currency=0.0,
        watts=1200, fx_overhead=1.3, provision_date=date(2020, 1, 1),
    )
    # overhead lines (not sga, not hw) should be scaled
    assert r_fx["overhead"]["power_per_kw"] == round(r_1x["overhead"]["power_per_kw"] * 1.3, 2)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /path/to/cpq-front-end && pytest tests/test_profitability.py -v
```

Expected: `ImportError` — `db/profitability.py` does not exist yet.

- [ ] **Step 3: Create `db/profitability.py`**

```python
from datetime import date

from db.fusion import get_dc_info
from db.mssql import get_fx_rate, get_mssql_costs, get_mssql_watts_batch, _configured
from lib.overhead import COST_DRIVERS, calc_overhead
from lib.renewal_pricing import hw_paid_off, provision_age_months


def _parse_date(value) -> date | None:
    if value is None:
        return None
    if isinstance(value, str):
        s = value[:10]
        if s <= "1900-01-01":
            return None
        try:
            return date.fromisoformat(s)
        except ValueError:
            return None
    if hasattr(value, "date"):
        return value.date() if value.year > 1900 else None
    return None


def calc_service_margin(
    mrc: float,
    dc_code: str,
    hw_capex_in_currency: float,
    watts: int | None,
    fx_overhead: float,
    provision_date,
) -> dict:
    """Pure calculation — no DB calls. All inputs must be pre-fetched by caller.

    Returns dict with hw_amortized, overhead (dict), sga, total_cost,
    margin, margin_pct, hw_paid_off, hw_months_remaining, biggest_cost_driver.
    """
    prov = provision_date if isinstance(provision_date, date) else _parse_date(provision_date)

    paid_off = hw_paid_off(prov)
    age_months = provision_age_months(prov)
    hw_amortized = 0.0 if paid_off else round(hw_capex_in_currency / 36, 2)
    hw_months_remaining = max(0, 36 - age_months) if age_months is not None else None

    # Normalize dc_code to match cost_drivers.json keys (e.g. IAD2 → IAD)
    overhead_dc = dc_code
    dc_info = get_dc_info(dc_code) if dc_code else None
    if dc_code not in COST_DRIVERS["data_centers"] and dc_info:
        fid = dc_info.get("id")
        for code, entry in COST_DRIVERS["data_centers"].items():
            if entry.get("fusion_dc_id") == fid:
                overhead_dc = code
                break

    kw = round(watts / 1000, 3) if watts else None
    overhead_lines = calc_overhead(overhead_dc, mrc, fx_rate=fx_overhead, kw=kw)

    # Split overhead into per-device lines and SGA
    overhead_amounts: dict[str, float] = {}
    sga = 0.0
    for k, v in overhead_lines.items():
        amount = v["amount"] or 0
        if k == "sga":
            sga = amount
        else:
            overhead_amounts[k] = amount

    direct_total = round(sum(overhead_amounts.values()), 2)
    total_cost = round(hw_amortized + direct_total + sga, 2)
    margin = round(mrc - total_cost, 2)
    margin_pct = round(margin / mrc * 100, 1) if mrc > 0 else 0.0

    all_components = {"hw_amortized": hw_amortized, **overhead_amounts, "sga": sga}
    biggest = max(all_components, key=lambda k: all_components[k]) if any(v > 0 for v in all_components.values()) else None

    return {
        "hw_amortized": hw_amortized,
        "overhead": overhead_amounts,
        "sga": sga,
        "total_cost": total_cost,
        "margin": margin,
        "margin_pct": margin_pct,
        "hw_paid_off": paid_off,
        "hw_months_remaining": hw_months_remaining,
        "biggest_cost_driver": biggest,
    }


def get_active_services(
    account_managers: list[str] | None = None,
    dc_codes: list[str] | None = None,
    service_types: list[str] | None = None,
    company_search: str | None = None,
) -> list[dict]:
    """Fetch all active services from dimServices + dimClientsActive."""
    if not _configured():
        return []
    try:
        from db.mssql import _connect
        conn = _connect()
        cur = conn.cursor(as_dict=True)

        conditions = ["ds.service_status = 'Active'"]
        params = []

        if account_managers:
            placeholders = ",".join(["%s"] * len(account_managers))
            conditions.append(f"dca.account_manager IN ({placeholders})")
            params.extend(account_managers)
        if dc_codes:
            placeholders = ",".join(["%s"] * len(dc_codes))
            conditions.append(f"ds.datacenter_code IN ({placeholders})")
            params.extend(dc_codes)
        if service_types:
            placeholders = ",".join(["%s"] * len(service_types))
            conditions.append(f"ds.service_type IN ({placeholders})")
            params.extend(service_types)
        if company_search:
            conditions.append("dca.company_name LIKE %s")
            params.append(f"%{company_search}%")

        where = " AND ".join(conditions)
        sql = f"""
            SELECT
                ds.service_id, ds.client_id, ds.datacenter_code,
                ds.currency, ds.mrc, ds.provision_date,
                ds.service_type, ds.fusion_id, ds.nickname,
                ds.product, ds.service_status,
                dca.company_name, dca.account_manager
            FROM DM_BusinessInsights.dbo.dimServices ds
            LEFT JOIN DM_BusinessInsights.dbo.dimClientsActive dca
                ON dca.client_id = ds.client_id
            WHERE {where}
            ORDER BY dca.company_name, ds.service_id
        """
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        result = []
        for r in rows:
            row = dict(r)
            row["mrc"] = float(row.get("mrc") or 0)
            row["provision_date"] = _parse_date(row.get("provision_date"))
            row["company_name"] = (row.get("company_name") or "").strip()
            row["account_manager"] = (row.get("account_manager") or "").strip() or None
            result.append(row)
        return result
    except Exception:
        return []


def get_profitability_filter_options() -> dict:
    """Distinct values for filter dropdowns."""
    if not _configured():
        return {"account_managers": [], "dc_codes": [], "service_types": []}
    try:
        from db.mssql import _connect
        conn = _connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT DISTINCT TOP 200 account_manager AS val
            FROM DM_BusinessInsights.dbo.dimClientsActive
            WHERE account_manager IS NOT NULL AND account_manager != ''
            ORDER BY account_manager
        """)
        ams = [r[0] for r in cur.fetchall() if r[0]]

        cur.execute("""
            SELECT DISTINCT TOP 200 datacenter_code AS val
            FROM DM_BusinessInsights.dbo.dimServices
            WHERE datacenter_code IS NOT NULL AND service_status = 'Active'
            ORDER BY datacenter_code
        """)
        dcs = [r[0] for r in cur.fetchall() if r[0]]

        cur.execute("""
            SELECT DISTINCT TOP 200 service_type AS val
            FROM DM_BusinessInsights.dbo.dimServices
            WHERE service_type IS NOT NULL AND service_status = 'Active'
            ORDER BY service_type
        """)
        types = [r[0] for r in cur.fetchall() if r[0]]

        cur.close()
        conn.close()
        return {"account_managers": ams, "dc_codes": dcs, "service_types": types}
    except Exception:
        return {"account_managers": [], "dc_codes": [], "service_types": []}


def build_profitability_data(services: list[dict]) -> list[dict]:
    """Enrich each service dict with its cost breakdown and margin.

    Makes two batched MSSQL calls (HW costs + watts) then computes
    margin for every service using calc_service_margin.
    """
    if not services:
        return []

    fusion_ids = [s["fusion_id"] for s in services if s.get("fusion_id")]

    hw_costs = get_mssql_costs(fusion_ids, "TLS") if fusion_ids else {}
    watts_map = get_mssql_watts_batch(fusion_ids) if fusion_ids else {}

    # Cache FX rates — at most a handful of currency pairs across all services
    fx_cache: dict[tuple[str, str], float] = {}

    def get_fx(from_c: str, to_c: str) -> float:
        if from_c == to_c:
            return 1.0
        key = (from_c, to_c)
        if key not in fx_cache:
            fx_cache[key] = get_fx_rate(from_c, to_c)
        return fx_cache[key]

    result = []
    for service in services:
        fid = service.get("fusion_id")
        currency = (service.get("currency") or "USD").upper()
        dc_code = (service.get("datacenter_code") or "").upper()

        dc_info = get_dc_info(dc_code) if dc_code else None
        native_currency = dc_info["native_currency"] if dc_info else currency

        # HW capex → service billing currency
        hw_capex_in_currency = 0.0
        if fid and fid in hw_costs:
            hw = hw_costs[fid]
            hw_capex_in_currency = round(hw["cost"] * get_fx(hw["currency"], currency), 2)

        fx_overhead = get_fx(native_currency, currency)
        watts = watts_map.get(fid) if fid else None
        mrc = float(service.get("mrc") or 0)

        margin_data = calc_service_margin(
            mrc=mrc,
            dc_code=dc_code,
            hw_capex_in_currency=hw_capex_in_currency,
            watts=watts,
            fx_overhead=fx_overhead,
            provision_date=service.get("provision_date"),
        )

        result.append({**service, **margin_data})

    return result
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_profitability.py -v
```

Expected: all 6 tests pass.

- [ ] **Step 5: Commit**

```bash
git add db/profitability.py db/mssql.py tests/test_profitability.py
git commit -m "feat: add profitability data layer with calc_service_margin and batch service fetching"
```

---

### Task 4: Fill in the API endpoints in `routes/profitability.py`

**Files:**
- Modify: `routes/profitability.py`

- [ ] **Step 1: Replace the stub endpoints with full implementations**

Replace the entire file content of `routes/profitability.py`:

```python
from collections import defaultdict

from flask import Blueprint, jsonify, render_template, request

from db.profitability import (build_profitability_data, get_active_services,
                              get_profitability_filter_options)
from db.mssql import get_fx_rate

profitability_bp = Blueprint("profitability", __name__)


# ── HTML routes ──────────────────────────────────────────────────────────────

@profitability_bp.route("/profitability")
def profitability_page():
    return render_template("profitability.html", active_page="profitability")


@profitability_bp.route("/profitability/<int:client_id>")
def profitability_customer_page(client_id):
    return render_template(
        "profitability_customer.html",
        client_id=client_id,
        active_page="profitability",
    )


# ── API ───────────────────────────────────────────────────────────────────────

@profitability_bp.route("/api/profitability/filter-options")
def api_profitability_filter_options():
    return jsonify(get_profitability_filter_options())


@profitability_bp.route("/api/profitability")
def api_profitability():
    account_managers = request.args.getlist("am") or None
    dc_codes         = request.args.getlist("dc") or None
    service_types    = request.args.getlist("service_type") or None
    company_search   = request.args.get("company", "").strip() or None
    display_currency = request.args.get("display_currency", "").strip().upper() or None

    services = get_active_services(
        account_managers=account_managers,
        dc_codes=dc_codes,
        service_types=service_types,
        company_search=company_search,
    )
    enriched = build_profitability_data(services)

    # If display_currency requested, pre-convert all service values
    if display_currency:
        fx_cache: dict[tuple, float] = {}
        converted = []
        for svc in enriched:
            svc_currency = (svc.get("currency") or "USD").upper()
            key = (svc_currency, display_currency)
            if key not in fx_cache:
                fx_cache[key] = get_fx_rate(svc_currency, display_currency) if svc_currency != display_currency else 1.0
            fx = fx_cache[key]
            converted.append({
                **svc,
                "mrc":        round(svc["mrc"] * fx, 2),
                "total_cost": round(svc["total_cost"] * fx, 2),
                "margin":     round(svc["margin"] * fx, 2),
                "currency":   display_currency,
            })
        enriched = converted

    by_customer    = _aggregate_by_customer(enriched, display_currency)
    by_dc          = _aggregate_by_field(enriched, "datacenter_code", display_currency)
    by_service_type = _aggregate_by_field(enriched, "service_type", display_currency)
    totals         = _compute_totals(enriched, display_currency)

    return jsonify({
        "by_customer":    by_customer,
        "by_dc":          by_dc,
        "by_service_type": by_service_type,
        "totals":         totals,
    })


@profitability_bp.route("/api/profitability/<int:client_id>")
def api_profitability_customer(client_id):
    display_currency = request.args.get("display_currency", "").strip().upper() or None

    services = get_active_services()
    services = [s for s in services if s["client_id"] == client_id]

    if not services:
        return jsonify({"error": "Customer not found or has no active services"}), 404

    enriched = build_profitability_data(services)

    if display_currency:
        fx_cache: dict[tuple, float] = {}
        converted = []
        for svc in enriched:
            svc_currency = (svc.get("currency") or "USD").upper()
            key = (svc_currency, display_currency)
            if key not in fx_cache:
                fx_cache[key] = get_fx_rate(svc_currency, display_currency) if svc_currency != display_currency else 1.0
            fx = fx_cache[key]
            converted.append({
                **svc,
                "mrc":        round(svc["mrc"] * fx, 2),
                "total_cost": round(svc["total_cost"] * fx, 2),
                "margin":     round(svc["margin"] * fx, 2),
                "hw_amortized": round(svc["hw_amortized"] * fx, 2),
                "sga":        round(svc["sga"] * fx, 2),
                "overhead":   {k: round(v * fx, 2) for k, v in svc["overhead"].items()},
                "currency":   display_currency,
            })
        enriched = converted

    summary = _compute_totals(enriched, display_currency)
    info = services[0]
    summary["company_name"]    = info.get("company_name") or ""
    summary["account_manager"] = info.get("account_manager") or ""
    summary["client_id"]       = client_id

    # Serialize services — convert provision_date (date object) to string
    serialized = []
    for svc in enriched:
        s = dict(svc)
        if hasattr(s.get("provision_date"), "isoformat"):
            s["provision_date"] = s["provision_date"].isoformat()
        serialized.append(s)

    return jsonify({"services": serialized, "summary": summary})


# ── Aggregation helpers ───────────────────────────────────────────────────────

def _aggregate_by_customer(enriched: list[dict], display_currency: str | None) -> list[dict]:
    groups: dict[int, dict] = {}
    for svc in enriched:
        cid = svc["client_id"]
        if cid not in groups:
            groups[cid] = {
                "client_id":       cid,
                "company_name":    svc.get("company_name") or "",
                "account_manager": svc.get("account_manager") or "",
                "service_count":   0,
                "currencies":      set(),
                "mrc":        0.0,
                "total_cost": 0.0,
                "margin":     0.0,
            }
        g = groups[cid]
        g["service_count"] += 1
        g["currencies"].add((svc.get("currency") or "USD").upper())
        g["mrc"]        += svc["mrc"]
        g["total_cost"] += svc["total_cost"]
        g["margin"]     += svc["margin"]

    result = []
    for g in groups.values():
        mixed = len(g["currencies"]) > 1 and not display_currency
        mrc   = round(g["mrc"], 2)        if not mixed else None
        cost  = round(g["total_cost"], 2) if not mixed else None
        margin = round(g["margin"], 2)    if not mixed else None
        mpct   = round(margin / mrc * 100, 1) if (mrc and margin is not None and mrc > 0) else None
        result.append({
            "client_id":       g["client_id"],
            "company_name":    g["company_name"],
            "account_manager": g["account_manager"],
            "service_count":   g["service_count"],
            "currency":        display_currency or (list(g["currencies"])[0] if len(g["currencies"]) == 1 else "mixed"),
            "currency_mixed":  mixed,
            "mrc":        mrc,
            "total_cost": cost,
            "margin":     margin,
            "margin_pct": mpct,
        })
    result.sort(key=lambda x: (x["margin_pct"] is None, x["margin_pct"] or 0))
    return result


def _aggregate_by_field(enriched: list[dict], field: str, display_currency: str | None) -> list[dict]:
    groups: dict[str, dict] = {}
    for svc in enriched:
        key = (svc.get(field) or "Unknown").strip()
        if key not in groups:
            groups[key] = {"label": key, "service_count": 0, "currencies": set(),
                           "mrc": 0.0, "total_cost": 0.0, "margin": 0.0}
        g = groups[key]
        g["service_count"] += 1
        g["currencies"].add((svc.get("currency") or "USD").upper())
        g["mrc"]        += svc["mrc"]
        g["total_cost"] += svc["total_cost"]
        g["margin"]     += svc["margin"]

    result = []
    for g in groups.values():
        mixed = len(g["currencies"]) > 1 and not display_currency
        mrc   = round(g["mrc"], 2)        if not mixed else None
        cost  = round(g["total_cost"], 2) if not mixed else None
        margin = round(g["margin"], 2)    if not mixed else None
        mpct   = round(margin / mrc * 100, 1) if (mrc and margin is not None and mrc > 0) else None
        result.append({
            "label":          g["label"],
            "service_count":  g["service_count"],
            "currency":       display_currency or (list(g["currencies"])[0] if len(g["currencies"]) == 1 else "mixed"),
            "currency_mixed": mixed,
            "mrc":        mrc,
            "total_cost": cost,
            "margin":     margin,
            "margin_pct": mpct,
        })
    result.sort(key=lambda x: (x["margin_pct"] is None, x["margin_pct"] or 0))
    return result


def _compute_totals(enriched: list[dict], display_currency: str | None) -> dict:
    if not enriched:
        return {"service_count": 0, "customer_count": 0, "at_risk_count": 0,
                "currency": None, "currency_mixed": False,
                "mrc": None, "total_cost": None, "margin": None, "margin_pct": None}

    currencies = {(s.get("currency") or "USD").upper() for s in enriched}
    mixed = len(currencies) > 1 and not display_currency
    customer_ids = {s["client_id"] for s in enriched}
    at_risk = sum(1 for s in enriched if (s.get("margin_pct") or 0) < 10)

    if mixed:
        return {
            "service_count": len(enriched), "customer_count": len(customer_ids),
            "at_risk_count": at_risk, "currency": "mixed", "currency_mixed": True,
            "mrc": None, "total_cost": None, "margin": None, "margin_pct": None,
        }

    mrc   = round(sum(s["mrc"] for s in enriched), 2)
    cost  = round(sum(s["total_cost"] for s in enriched), 2)
    margin = round(sum(s["margin"] for s in enriched), 2)
    mpct   = round(margin / mrc * 100, 1) if mrc > 0 else 0.0
    return {
        "service_count": len(enriched), "customer_count": len(customer_ids),
        "at_risk_count": at_risk,
        "currency": display_currency or list(currencies)[0],
        "currency_mixed": False,
        "mrc": mrc, "total_cost": cost, "margin": margin, "margin_pct": mpct,
    }
```

- [ ] **Step 2: Smoke-test the API**

Run the app and open:
- http://127.0.0.1:5050/api/profitability/filter-options — should return JSON with `account_managers`, `dc_codes`, `service_types` arrays
- http://127.0.0.1:5050/api/profitability — should return JSON with `by_customer`, `by_dc`, `by_service_type`, `totals`
- http://127.0.0.1:5050/api/profitability?display_currency=USD — same but with numbers in the `totals` card

- [ ] **Step 3: Commit**

```bash
git add routes/profitability.py
git commit -m "feat: implement profitability API endpoints with aggregation"
```

---

### Task 5: `templates/profitability.html` — landing page

**Files:**
- Modify: `templates/profitability.html`

- [ ] **Step 1: Replace the placeholder with the full template**

Replace the entire content of `templates/profitability.html`:

```html
{% extends "base.html" %}
{% block title %}CPQ — Profitability · Aptum{% endblock %}

{% block extra_styles %}
  /* ── Filter bar ─────────────────────────────────────────────── */
  .filter-bar {
    display:flex; align-items:flex-end; gap:1rem; flex-wrap:wrap;
    background:var(--surface); border:1px solid var(--border); border-radius:12px;
    padding:1.25rem 1.5rem; margin-bottom:1.5rem;
    box-shadow:0 2px 8px var(--shadow);
  }
  .filter-group { display:flex; flex-direction:column; gap:.3rem; min-width:160px; position:relative; }
  .filter-group label { font-size:.63rem; font-weight:700; text-transform:uppercase; letter-spacing:.08em; color:var(--text-3); }
  .filter-group input[type="text"] {
    appearance:none; background:var(--bg); border:1px solid var(--border);
    color:var(--text-1); font-family:'Geist',sans-serif; font-size:.875rem;
    padding:.5rem .85rem; border-radius:8px; outline:none; transition:border-color .15s;
  }
  .filter-group input:focus { border-color:var(--accent); }
  .combo-trigger {
    display:flex; align-items:center; justify-content:space-between; gap:4px;
    background:var(--bg); border:1px solid var(--border); border-radius:8px;
    padding:4px 10px 4px 8px; min-height:36px; cursor:pointer; transition:border-color .15s; user-select:none;
  }
  .combo-trigger:focus { outline:none; }
  .combo-trigger.open, .combo-trigger:focus-visible { border-color:var(--accent); }
  .combo-chips { display:flex; flex-wrap:wrap; gap:4px; flex:1; align-items:center; min-height:24px; }
  .combo-placeholder { color:var(--text-3); font-size:.875rem; line-height:1.4; }
  .combo-chevron { color:var(--text-3); font-size:.6rem; flex-shrink:0; transition:transform .15s; }
  .combo-trigger.open .combo-chevron { transform:rotate(180deg); }
  .combo-chip {
    display:inline-flex; align-items:center; gap:3px;
    background:var(--accent-dim); color:var(--accent-text);
    border-radius:4px; padding:2px 6px; font-size:.72rem; font-weight:600; white-space:nowrap;
  }
  .combo-chip-rm { background:none; border:none; color:inherit; cursor:pointer; font-size:.85rem; line-height:1; padding:0; opacity:.65; }
  .combo-chip-rm:hover { opacity:1; }
  .combo-dropdown {
    position:absolute; top:calc(100% + 4px); left:0; right:0; z-index:300;
    background:var(--surface); border:1px solid var(--border); border-radius:8px;
    box-shadow:0 6px 16px var(--shadow);
  }
  .combo-search-wrap { padding:.5rem .65rem; border-bottom:1px solid var(--border); }
  .combo-search { width:100%; background:transparent; border:none; outline:none; color:var(--text-1); font-family:'Geist',sans-serif; font-size:.82rem; }
  .combo-search::placeholder { color:var(--text-3); }
  .combo-list { max-height:210px; overflow-y:auto; padding:.25rem 0; }
  .combo-item { display:flex; align-items:center; gap:.5rem; padding:.42rem .75rem; font-size:.82rem; color:var(--text-1); cursor:pointer; transition:background .1s; }
  .combo-item:hover { background:var(--surface-2); }
  .combo-check { width:14px; height:14px; border:1.5px solid var(--border); border-radius:3px; flex-shrink:0; display:flex; align-items:center; justify-content:center; font-size:.6rem; color:var(--accent); }
  .combo-item.selected .combo-check { background:var(--accent-dim); border-color:var(--accent); }
  .combo-empty { padding:.5rem .75rem; font-size:.82rem; color:var(--text-3); }
  .filter-clear { font-size:.75rem; color:var(--text-3); background:none; border:none; cursor:pointer; padding:.35rem .5rem; border-radius:6px; font-family:'Geist',sans-serif; align-self:flex-end; margin-bottom:1px; }
  .filter-clear:hover { color:var(--text-1); }

  /* ── KPI cards ──────────────────────────────────────────────── */
  .kpi-row { display:grid; grid-template-columns:repeat(4,1fr); gap:.75rem; margin-bottom:1.5rem; }
  .kpi-card { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:.9rem 1.1rem; box-shadow:0 2px 6px var(--shadow); }
  .kpi-label { font-size:.6rem; font-weight:700; text-transform:uppercase; letter-spacing:.07em; color:var(--text-3); margin-bottom:.35rem; }
  .kpi-value { font-size:1.4rem; font-weight:700; color:var(--text-1); font-family:'Geist Mono',monospace; }
  .kpi-sub { font-size:.68rem; color:var(--text-3); margin-top:.2rem; }

  /* ── Controls + table ───────────────────────────────────────── */
  .controls { display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem; }
  .seg-toggle { display:flex; border:1px solid var(--border); border-radius:8px; overflow:hidden; }
  .seg-btn { padding:.38rem 1rem; font-size:.78rem; font-weight:500; font-family:'Geist',sans-serif; background:var(--surface); color:var(--text-2); border:none; cursor:pointer; border-right:1px solid var(--border); transition:background .12s, color .12s; }
  .seg-btn:last-child { border-right:none; }
  .seg-btn.active { background:var(--accent); color:#fff; }
  .sort-hint { font-size:.7rem; color:var(--text-3); }

  .currency-select { appearance:none; background:var(--bg); border:1px solid var(--border); color:var(--text-1); font-family:'Geist',sans-serif; font-size:.78rem; padding:.35rem .75rem; border-radius:8px; cursor:pointer; outline:none; }
  .currency-select:focus { border-color:var(--accent); }

  .table-wrap { background:var(--surface); border:1px solid var(--border); border-radius:12px; overflow:hidden; box-shadow:0 2px 8px var(--shadow); }
  .prof-table { width:100%; border-collapse:collapse; }
  .prof-table th { font-size:.6rem; font-weight:700; text-transform:uppercase; letter-spacing:.06em; color:var(--text-3); padding:.45rem .75rem; text-align:left; border-bottom:2px solid var(--border); white-space:nowrap; cursor:pointer; user-select:none; }
  .prof-table th:hover { color:var(--text-1); }
  .prof-table th.r { text-align:right; }
  .prof-table th.sorted { color:var(--accent); }
  .prof-table td { padding:.6rem .75rem; font-size:.8rem; color:var(--text-2); border-bottom:1px solid var(--border); vertical-align:middle; }
  .prof-table td.name { color:var(--text-1); font-weight:500; }
  .prof-table td.mono { font-family:'Geist Mono',monospace; text-align:right; }
  .prof-table td.pct  { font-family:'Geist Mono',monospace; text-align:right; font-weight:600; }
  .prof-table td.pct.pos  { color:var(--green); }
  .prof-table td.pct.warn { color:var(--orange); }
  .prof-table td.pct.neg  { color:var(--red); }
  .prof-table tr:last-child td { border-bottom:none; }
  .prof-table tr:hover { background:var(--surface-2); cursor:pointer; }
  .empty-state { padding:3rem; text-align:center; color:var(--text-3); font-size:.85rem; }
{% endblock %}

{% block body %}
<div class="page-body">

  <!-- Filter bar -->
  <div class="filter-bar">
    <div class="filter-group">
      <label>Account Manager</label>
      <div id="f-am"></div>
    </div>
    <div class="filter-group">
      <label>Data Center</label>
      <div id="f-dc"></div>
    </div>
    <div class="filter-group">
      <label>Service Type</label>
      <div id="f-svctype"></div>
    </div>
    <div class="filter-group" style="min-width:140px">
      <label>Customer</label>
      <input type="text" id="f-company" placeholder="Search…" autocomplete="off"/>
    </div>
    <div class="filter-group" style="min-width:120px">
      <label>Display Currency</label>
      <select class="currency-select" id="f-currency">
        <option value="">Native</option>
      </select>
    </div>
    <button class="filter-clear" onclick="clearFilters()">Clear filters</button>
  </div>

  <!-- KPI cards -->
  <div class="kpi-row">
    <div class="kpi-card">
      <div class="kpi-label">Total MRC</div>
      <div class="kpi-value" id="kpi-mrc">—</div>
      <div class="kpi-sub" id="kpi-mrc-sub">loading…</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Total Cost</div>
      <div class="kpi-value" id="kpi-cost">—</div>
      <div class="kpi-sub">HW amort + overhead + SG&amp;A</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Net Margin</div>
      <div class="kpi-value" id="kpi-margin">—</div>
      <div class="kpi-sub" id="kpi-margin-sub">—</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">At Risk</div>
      <div class="kpi-value" id="kpi-risk">—</div>
      <div class="kpi-sub">services below 10% margin</div>
    </div>
  </div>

  <!-- Segment toggle + sort hint -->
  <div class="controls">
    <div style="display:flex;align-items:center;gap:.75rem">
      <div class="seg-toggle">
        <button class="seg-btn active" data-seg="customer" onclick="setSeg(this)">By Customer</button>
        <button class="seg-btn" data-seg="dc" onclick="setSeg(this)">By Data Center</button>
        <button class="seg-btn" data-seg="type" onclick="setSeg(this)">By Service Type</button>
      </div>
    </div>
    <span class="sort-hint">↕ Click column headers to sort · Click row to drill in</span>
  </div>

  <!-- Table -->
  <div class="table-wrap">
    <table class="prof-table">
      <thead id="thead">
        <tr>
          <th id="th-name" data-col="name" onclick="sortBy('name')">Customer</th>
          <th id="th-am" data-col="am" onclick="sortBy('am')">Account Manager</th>
          <th class="r" data-col="count" onclick="sortBy('count')">Services</th>
          <th class="r" data-col="mrc" onclick="sortBy('mrc')">MRC</th>
          <th class="r" data-col="cost" onclick="sortBy('cost')">Total Cost</th>
          <th class="r" data-col="margin" onclick="sortBy('margin')">Margin $</th>
          <th class="r sorted" id="th-pct" data-col="pct" onclick="sortBy('pct')">Margin %</th>
        </tr>
      </thead>
      <tbody id="tbody">
        <tr><td colspan="7" class="empty-state">Loading…</td></tr>
      </tbody>
    </table>
  </div>

</div>
{% endblock %}

{% block extra_scripts %}
<script>
  let _data       = null;  // full API response
  let _seg        = 'customer';
  let _sortCol    = 'pct';
  let _sortAsc    = true;
  let _debounce   = null;
  let _currencies = [];

  // ── ComboSelect (same implementation as renewals.html) ─────────────────────
  class ComboSelect {
    constructor(mountId, placeholder, loadAll, options = []) {
      this.placeholder = placeholder;
      this.selected    = [];
      this.allOptions  = options;
      this._open       = false;

      const mount = document.getElementById(mountId);
      const group = mount.closest('.filter-group');

      this.trigger = document.createElement('div');
      this.trigger.className = 'combo-trigger';
      this.trigger.setAttribute('tabindex', '0');

      this.chipsArea = document.createElement('div');
      this.chipsArea.className = 'combo-chips';
      this.chevron = document.createElement('span');
      this.chevron.className = 'combo-chevron';
      this.chevron.textContent = '▾';
      this.trigger.appendChild(this.chipsArea);
      this.trigger.appendChild(this.chevron);

      this.dropdown = document.createElement('div');
      this.dropdown.className = 'combo-dropdown';
      this.dropdown.style.display = 'none';

      const sw = document.createElement('div');
      sw.className = 'combo-search-wrap';
      this.searchInput = document.createElement('input');
      this.searchInput.className = 'combo-search';
      this.searchInput.placeholder = 'Filter…';
      this.searchInput.autocomplete = 'off';
      sw.appendChild(this.searchInput);

      this.list = document.createElement('div');
      this.list.className = 'combo-list';

      this.dropdown.appendChild(sw);
      this.dropdown.appendChild(this.list);

      mount.replaceWith(this.trigger);
      group.appendChild(this.dropdown);

      this._renderTrigger();
      this._bind();
    }

    values() { return [...this.selected]; }

    setOptions(opts) {
      this.allOptions = opts;
    }

    _bind() {
      this.trigger.addEventListener('click', () => this._toggle());
      this.trigger.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); this._toggle(); }
        if (e.key === 'Escape') this._close();
      });
      this.searchInput.addEventListener('input', () => {
        const q = this.searchInput.value.toLowerCase();
        this._renderList(q ? this.allOptions.filter(v => v.toLowerCase().includes(q)) : this.allOptions);
      });
      this.searchInput.addEventListener('keydown', e => { if (e.key === 'Escape') this._close(); });
      document.addEventListener('click', e => {
        if (!this.trigger.contains(e.target) && !this.dropdown.contains(e.target)) this._close();
      });
    }

    _toggle() { this._open ? this._close() : this._open_(); }

    _open_() {
      this._open = true;
      this.trigger.classList.add('open');
      this.dropdown.style.display = 'block';
      this.searchInput.value = '';
      this._renderList(this.allOptions);
      requestAnimationFrame(() => this.searchInput.focus());
    }

    _close() {
      this._open = false;
      this.trigger.classList.remove('open');
      this.dropdown.style.display = 'none';
    }

    _renderList(items) {
      this.list.innerHTML = '';
      if (!items.length) {
        const el = document.createElement('div');
        el.className = 'combo-empty';
        el.textContent = 'No options';
        this.list.appendChild(el);
        return;
      }
      const frag = document.createDocumentFragment();
      items.forEach(v => {
        const isSelected = this.selected.includes(v);
        const item = document.createElement('div');
        item.className = 'combo-item' + (isSelected ? ' selected' : '');
        const check = document.createElement('div');
        check.className = 'combo-check';
        if (isSelected) check.textContent = '✓';
        const label = document.createElement('span');
        label.textContent = v;
        item.appendChild(check);
        item.appendChild(label);
        item.addEventListener('click', () => {
          if (this.selected.includes(v)) {
            this.selected = this.selected.filter(x => x !== v);
          } else {
            this.selected.push(v);
          }
          this._renderTrigger();
          this._renderList(items);
          load();
        });
        frag.appendChild(item);
      });
      this.list.appendChild(frag);
    }

    _renderTrigger() {
      this.chipsArea.innerHTML = '';
      if (!this.selected.length) {
        const ph = document.createElement('span');
        ph.className = 'combo-placeholder';
        ph.textContent = this.placeholder;
        this.chipsArea.appendChild(ph);
      } else {
        this.selected.forEach(v => {
          const chip = document.createElement('span');
          chip.className = 'combo-chip';
          chip.textContent = v + ' ';
          const rm = document.createElement('button');
          rm.className = 'combo-chip-rm';
          rm.textContent = '×';
          rm.addEventListener('click', e => {
            e.stopPropagation();
            this.selected = this.selected.filter(x => x !== v);
            this._renderTrigger();
            load();
          });
          chip.appendChild(rm);
          this.chipsArea.appendChild(chip);
        });
      }
    }

    clear() { this.selected = []; this._renderTrigger(); }
  }

  // ── Init combos ───────────────────────────────────────────────────────────
  const amSelect   = new ComboSelect('f-am',      'All managers', true);
  const dcSelect   = new ComboSelect('f-dc',      'All DCs',      true);
  const typeSelect = new ComboSelect('f-svctype', 'All types',    true);

  // Load filter options
  fetch('/api/profitability/filter-options')
    .then(r => r.json())
    .then(d => {
      amSelect.setOptions(d.account_managers || []);
      dcSelect.setOptions(d.dc_codes || []);
      typeSelect.setOptions(d.service_types || []);
      _currencies = ['USD', 'CAD', 'GBP', 'EUR'];
      const sel = document.getElementById('f-currency');
      _currencies.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c;
        sel.appendChild(opt);
      });
    });

  // Company search input
  document.getElementById('f-company').addEventListener('input', () => {
    clearTimeout(_debounce);
    _debounce = setTimeout(load, 350);
  });

  document.getElementById('f-currency').addEventListener('change', load);

  // ── Data loading ──────────────────────────────────────────────────────────
  function buildParams() {
    const p = new URLSearchParams();
    amSelect.values().forEach(v => p.append('am', v));
    dcSelect.values().forEach(v => p.append('dc', v));
    typeSelect.values().forEach(v => p.append('service_type', v));
    const co = document.getElementById('f-company').value.trim();
    if (co) p.set('company', co);
    const dc = document.getElementById('f-currency').value;
    if (dc) p.set('display_currency', dc);
    return p;
  }

  async function load() {
    document.getElementById('tbody').innerHTML = '<tr><td colspan="7" class="empty-state">Loading…</td></tr>';
    try {
      const res = await fetch('/api/profitability?' + buildParams());
      _data = await res.json();
      renderKpis(_data.totals);
      renderTable();
    } catch (e) {
      document.getElementById('tbody').innerHTML = '<tr><td colspan="7" class="empty-state">Error loading data</td></tr>';
    }
  }

  // ── KPI rendering ─────────────────────────────────────────────────────────
  function renderKpis(t) {
    const cur = t.currency && t.currency !== 'mixed' ? t.currency : '';
    document.getElementById('kpi-mrc').textContent    = t.mrc    != null ? fmt(t.mrc, cur) : '—';
    document.getElementById('kpi-cost').textContent   = t.total_cost != null ? fmt(t.total_cost, cur) : '—';
    document.getElementById('kpi-margin').textContent = t.margin  != null ? fmt(t.margin, cur) : '—';
    document.getElementById('kpi-risk').textContent   = t.at_risk_count != null ? t.at_risk_count + ' services' : '—';
    document.getElementById('kpi-mrc-sub').textContent =
      `${t.service_count || 0} services · ${t.customer_count || 0} customers`;
    const mpct = t.margin_pct != null ? t.margin_pct + '% blended avg' : 'select a currency to see totals';
    document.getElementById('kpi-margin-sub').textContent = mpct;
    document.getElementById('kpi-margin').style.color = t.margin == null ? '' :
      (t.margin < 0 ? 'var(--red)' : t.margin_pct >= 20 ? 'var(--green)' : '');
  }

  // ── Table rendering ───────────────────────────────────────────────────────
  function setSeg(btn) {
    document.querySelectorAll('.seg-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    _seg = btn.dataset.seg;
    const thName = document.getElementById('th-name');
    const thAm   = document.getElementById('th-am');
    if (_seg === 'customer') {
      thName.textContent = 'Customer';
      thAm.textContent = 'Account Manager';
      thAm.style.display = '';
    } else if (_seg === 'dc') {
      thName.textContent = 'Data Center';
      thAm.style.display = 'none';
    } else {
      thName.textContent = 'Service Type';
      thAm.style.display = 'none';
    }
    renderTable();
  }

  function sortBy(col) {
    if (_sortCol === col) { _sortAsc = !_sortAsc; }
    else { _sortCol = col; _sortAsc = col === 'pct'; }
    document.querySelectorAll('.prof-table th').forEach(th => th.classList.remove('sorted'));
    document.getElementById('th-' + col)?.classList.add('sorted');
    renderTable();
  }

  function renderTable() {
    if (!_data) return;
    const rows = _seg === 'customer' ? _data.by_customer
               : _seg === 'dc'       ? _data.by_dc
               : _data.by_service_type;

    const sorted = [...rows].sort((a, b) => {
      let av, bv;
      if (_sortCol === 'name')   { av = (a.company_name || a.label || '').toLowerCase(); bv = (b.company_name || b.label || '').toLowerCase(); }
      else if (_sortCol === 'am')    { av = (a.account_manager || '').toLowerCase(); bv = (b.account_manager || '').toLowerCase(); }
      else if (_sortCol === 'count') { av = a.service_count; bv = b.service_count; }
      else if (_sortCol === 'mrc')   { av = a.mrc ?? -Infinity; bv = b.mrc ?? -Infinity; }
      else if (_sortCol === 'cost')  { av = a.total_cost ?? -Infinity; bv = b.total_cost ?? -Infinity; }
      else if (_sortCol === 'margin'){ av = a.margin ?? -Infinity; bv = b.margin ?? -Infinity; }
      else /* pct */                 { av = a.margin_pct ?? -Infinity; bv = b.margin_pct ?? -Infinity; }
      if (av === bv) return 0;
      const cmp = av < bv ? -1 : 1;
      return _sortAsc ? cmp : -cmp;
    });

    const cur = document.getElementById('f-currency').value;
    const tbody = document.getElementById('tbody');
    if (!sorted.length) {
      tbody.innerHTML = '<tr><td colspan="7" class="empty-state">No services match the current filters.</td></tr>';
      return;
    }

    tbody.innerHTML = sorted.map(r => {
      const name  = r.company_name || r.label || '';
      const am    = r.account_manager || '';
      const link  = r.client_id ? `/profitability/${r.client_id}` : '#';
      const rowCur = r.currency && r.currency !== 'mixed' ? r.currency : (cur || '');
      const mixed  = r.currency_mixed;

      const mrcCell    = mixed ? '—' : (r.mrc    != null ? fmt(r.mrc, rowCur)    : '—');
      const costCell   = mixed ? '—' : (r.total_cost != null ? fmt(r.total_cost, rowCur) : '—');
      const marginCell = mixed ? '—' : (r.margin != null ? `<span style="${r.margin < 0 ? 'color:var(--red)' : ''}">${fmt(r.margin, rowCur)}</span>` : '—');
      const pctClass   = r.margin_pct == null ? '' : r.margin_pct >= 20 ? 'pos' : r.margin_pct >= 10 ? 'warn' : 'neg';
      const pctCell    = r.margin_pct != null ? r.margin_pct.toFixed(1) + '%' : '—';
      const amCell     = _seg === 'customer' ? `<td>${am}</td>` : '';

      return `<tr onclick="window.location='${link}'">
        <td class="name">${name}</td>
        ${amCell}
        <td class="mono">${r.service_count}</td>
        <td class="mono">${mrcCell}</td>
        <td class="mono">${costCell}</td>
        <td class="mono">${marginCell}</td>
        <td class="pct ${pctClass}">${pctCell}</td>
      </tr>`;
    }).join('');
  }

  // ── Helpers ───────────────────────────────────────────────────────────────
  function fmt(val, cur) {
    if (val == null) return '—';
    const n = new Intl.NumberFormat('en-US', {
      style: 'currency', currency: cur || 'USD',
      minimumFractionDigits: 0, maximumFractionDigits: 0,
    }).format(val);
    return cur && cur !== 'USD' ? n + ' ' + cur : n;
  }

  function clearFilters() {
    amSelect.clear(); dcSelect.clear(); typeSelect.clear();
    document.getElementById('f-company').value = '';
    document.getElementById('f-currency').value = '';
    load();
  }

  // Initial load
  load();
</script>
{% endblock %}
```

- [ ] **Step 2: Test the landing page**

Run the app and open http://127.0.0.1:5050/profitability

Verify:
- Filter bar renders with all four combos and the currency selector
- KPI cards update after load (show "—" if currencies are mixed, numbers if display_currency=USD selected)
- Segment toggle switches the table between customer/DC/service type views
- Clicking a column header sorts the table
- Clicking a customer row navigates to `/profitability/<client_id>`
- Selecting a display currency converts all values

- [ ] **Step 3: Commit**

```bash
git add templates/profitability.html
git commit -m "feat: implement profitability landing page with filter bar and segment table"
```

---

### Task 6: `templates/profitability_customer.html` — customer detail page

**Files:**
- Modify: `templates/profitability_customer.html`

- [ ] **Step 1: Replace the placeholder with the full template**

Replace the entire content of `templates/profitability_customer.html`:

```html
{% extends "base.html" %}
{% block title %}CPQ — Profitability · Aptum{% endblock %}

{% block extra_styles %}
  .layout { display:grid; grid-template-columns:1fr 360px; min-height:calc(100vh - 70px); }
  .main   { padding:2rem; overflow-y:auto; border-right:1px solid var(--border); }
  .sidebar { padding:1.5rem; display:flex; flex-direction:column; gap:1.25rem; position:sticky; top:0; max-height:calc(100vh - 70px); overflow-y:auto; }

  .back-link { font-size:.75rem; color:var(--accent); text-decoration:none; display:inline-flex; align-items:center; gap:.3rem; margin-bottom:1.25rem; }
  .page-header { margin-bottom:1.5rem; }
  .page-header h2 { font-size:1.1rem; font-weight:700; color:var(--text-1); margin-bottom:.2rem; }
  .page-header .sub { font-size:.78rem; color:var(--text-2); }

  .kpi-row { display:grid; grid-template-columns:repeat(4,1fr); gap:.75rem; margin-bottom:1.75rem; }
  .kpi-card { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:.9rem 1rem; box-shadow:0 2px 6px var(--shadow); }
  .kpi-label { font-size:.6rem; font-weight:700; text-transform:uppercase; letter-spacing:.07em; color:var(--text-3); margin-bottom:.35rem; }
  .kpi-value { font-size:1.3rem; font-weight:700; color:var(--text-1); font-family:'Geist Mono',monospace; }
  .kpi-sub { font-size:.68rem; color:var(--text-3); margin-top:.2rem; }

  .section-title { font-size:.65rem; font-weight:700; text-transform:uppercase; letter-spacing:.08em; color:var(--text-3); margin:0 0 .5rem; }

  /* Service table */
  .svc-table { width:100%; border-collapse:collapse; }
  .svc-table th { font-size:.6rem; font-weight:700; text-transform:uppercase; letter-spacing:.06em; color:var(--text-3); padding:.4rem .6rem; text-align:left; border-bottom:2px solid var(--border); white-space:nowrap; }
  .svc-table th.r { text-align:right; }
  .svc-table td { padding:.55rem .6rem; font-size:.8rem; color:var(--text-2); border-bottom:1px solid var(--border); vertical-align:middle; }
  .svc-table td.name { color:var(--text-1); font-weight:500; }
  .svc-table td.mono { font-family:'Geist Mono',monospace; text-align:right; }
  .svc-table tr.active-row { background:var(--accent-dim); }
  .svc-table tr.active-row td { color:var(--text-1); }
  .svc-table tr:hover:not(.active-row) { background:var(--surface-2); cursor:pointer; }
  .svc-table tr:last-child td { border-bottom:none; }

  .dc-badge { display:inline-block; font-size:.58rem; font-weight:700; text-transform:uppercase; letter-spacing:.05em; padding:1px 6px; border-radius:3px; background:var(--surface-2); color:var(--text-3); border:1px solid var(--border); }
  .pct-pos  { color:var(--green); }
  .pct-warn { color:var(--orange); }
  .pct-neg  { color:var(--red); }

  /* Sidebar */
  .surface-card { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:1rem 1.1rem; box-shadow:0 2px 6px var(--shadow); }
  .svc-detail-header h3 { font-size:.9rem; font-weight:700; color:var(--text-1); margin-bottom:.15rem; }
  .svc-detail-header .sub { font-size:.72rem; color:var(--text-2); }

  .cost-table { width:100%; border-collapse:collapse; }
  .cost-table td { padding:.35rem .2rem; font-size:.82rem; }
  .cost-table td:last-child { text-align:right; font-family:'Geist Mono',monospace; color:var(--text-1); white-space:nowrap; }
  .cost-table tr.sep td { border-top:1px solid var(--border); padding-top:.55rem; }
  .cost-table tr.highlight td { color:var(--accent); font-weight:700; font-size:.95rem; }
  .cost-table tr.highlight td:last-child { color:var(--accent); }
  .cost-table tr.dim td { color:var(--text-3); font-size:.75rem; }
  .cost-table tr.indent td:first-child { padding-left:.9rem; }
  .cost-table tr.margin-pos td { color:var(--green) !important; }
  .cost-table tr.margin-neg td { color:var(--red) !important; }

  .open-renewal-btn { width:100%; padding:.6rem; border-radius:8px; border:1px solid var(--accent); background:var(--accent-dim); color:var(--accent-text); font-family:'Geist',sans-serif; font-size:.85rem; font-weight:600; cursor:pointer; text-align:center; text-decoration:none; display:block; }
  .empty-state { padding:3rem; text-align:center; color:var(--text-3); font-size:.85rem; }
{% endblock %}

{% block body %}
<div class="layout">

  <!-- MAIN -->
  <div class="main">
    <a class="back-link" href="/profitability">← All Customers</a>

    <div class="page-header">
      <h2 id="cust-name">Loading…</h2>
      <div class="sub" id="cust-sub"></div>
    </div>

    <div class="kpi-row">
      <div class="kpi-card">
        <div class="kpi-label">Total MRC</div>
        <div class="kpi-value" id="kpi-mrc">—</div>
        <div class="kpi-sub">across all services</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Total Cost</div>
        <div class="kpi-value" id="kpi-cost">—</div>
        <div class="kpi-sub">HW + overhead + SG&amp;A</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Net Margin</div>
        <div class="kpi-value" id="kpi-margin">—</div>
        <div class="kpi-sub" id="kpi-margin-sub">—</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">At Risk</div>
        <div class="kpi-value" id="kpi-risk" style="color:var(--red)">—</div>
        <div class="kpi-sub">services below 10%</div>
      </div>
    </div>

    <div class="section-title">Services — click a row for cost breakdown</div>
    <table class="svc-table">
      <thead>
        <tr>
          <th>Service / Nickname</th>
          <th>DC</th>
          <th>Type</th>
          <th class="r">MRC</th>
          <th class="r">Cost</th>
          <th class="r">Margin $</th>
          <th class="r">Margin %</th>
        </tr>
      </thead>
      <tbody id="svc-tbody">
        <tr><td colspan="7" class="empty-state">Loading…</td></tr>
      </tbody>
    </table>
  </div>

  <!-- SIDEBAR -->
  <div class="sidebar">
    <div>
      <div class="section-title">Cost Breakdown</div>
      <div class="svc-detail-header" id="sb-header">
        <h3>—</h3>
        <div class="sub">Select a service</div>
      </div>
    </div>
    <div class="surface-card" id="sb-revenue" style="display:none">
      <div class="section-title" style="margin-bottom:.75rem">Revenue</div>
      <table class="cost-table" id="sb-revenue-table"></table>
    </div>
    <div class="surface-card" id="sb-costs" style="display:none">
      <div class="section-title" style="margin-bottom:.75rem">Costs</div>
      <table class="cost-table" id="sb-costs-table"></table>
    </div>
    <div class="surface-card" id="sb-margin-card" style="display:none">
      <div class="section-title" style="margin-bottom:.75rem">Margin</div>
      <table class="cost-table" id="sb-margin-table"></table>
    </div>
    <a class="open-renewal-btn" id="sb-renewal-link" href="#" style="display:none">Open Renewal →</a>
  </div>

</div>
{% endblock %}

{% block extra_scripts %}
<script>
  const CLIENT_ID = {{ client_id }};
  let _services   = [];

  async function load() {
    try {
      const res = await fetch(`/api/profitability/${CLIENT_ID}`);
      const data = await res.json();
      if (data.error) { showError(data.error); return; }

      _services = data.services || [];
      const s   = data.summary  || {};

      document.getElementById('cust-name').textContent = s.company_name || `Client ${CLIENT_ID}`;
      document.getElementById('cust-sub').textContent  =
        `client_id ${CLIENT_ID}` +
        (s.account_manager ? ` · Account Manager: ${s.account_manager}` : '') +
        ` · ${_services.length} active services`;

      const cur = _services.length && !s.currency_mixed
        ? (_services[0].currency || 'USD') : '';
      document.getElementById('kpi-mrc').textContent    = s.mrc    != null ? fmtMoney(s.mrc, cur) : '—';
      document.getElementById('kpi-cost').textContent   = s.total_cost != null ? fmtMoney(s.total_cost, cur) : '—';
      document.getElementById('kpi-margin').textContent = s.margin  != null ? fmtMoney(s.margin, cur) : '—';
      if (s.margin != null) document.getElementById('kpi-margin').style.color = s.margin < 0 ? 'var(--red)' : 'var(--green)';
      document.getElementById('kpi-margin-sub').textContent = s.margin_pct != null ? s.margin_pct.toFixed(1) + '% avg' : '';
      document.getElementById('kpi-risk').textContent = (s.at_risk_count ?? 0) + ' services';

      renderTable();
      if (_services.length) selectRow(0);
    } catch (e) {
      showError('Failed to load profitability data.');
    }
  }

  function renderTable() {
    const tbody = document.getElementById('svc-tbody');
    if (!_services.length) {
      tbody.innerHTML = '<tr><td colspan="7" class="empty-state">No active services found.</td></tr>';
      return;
    }
    tbody.innerHTML = _services.map((s, i) => {
      const name = s.nickname ? `${s.service_id} · ${s.nickname}` : String(s.service_id);
      const cur  = s.currency || '';
      const pctClass = s.margin_pct == null ? '' : s.margin_pct >= 20 ? 'pct-pos' : s.margin_pct >= 10 ? 'pct-warn' : 'pct-neg';
      return `<tr onclick="selectRow(${i})">
        <td class="name">${name}</td>
        <td><span class="dc-badge">${s.datacenter_code || '—'}</span></td>
        <td>${s.service_type || '—'}</td>
        <td class="mono">${fmtMoney(s.mrc, cur)}</td>
        <td class="mono">${fmtMoney(s.total_cost, cur)}</td>
        <td class="mono" style="${s.margin < 0 ? 'color:var(--red)' : ''}">${fmtMoney(s.margin, cur)}</td>
        <td class="mono ${pctClass}">${s.margin_pct != null ? s.margin_pct.toFixed(1) + '%' : '—'}</td>
      </tr>`;
    }).join('');
  }

  function selectRow(idx) {
    const rows = document.getElementById('svc-tbody').querySelectorAll('tr');
    rows.forEach((r, i) => r.classList.toggle('active-row', i === idx));
    const s = _services[idx];
    if (!s) return;
    renderSidebar(s);
  }

  function renderSidebar(s) {
    const cur = s.currency || 'USD';
    const name = s.nickname ? `${s.service_id} · ${s.nickname}` : String(s.service_id);

    document.getElementById('sb-header').innerHTML = `
      <h3>${name}</h3>
      <div class="sub">${s.service_type || ''} · ${s.datacenter_code || ''}</div>`;

    // Revenue
    document.getElementById('sb-revenue-table').innerHTML = `
      <tr class="highlight"><td>MRC</td><td>${fmtMoney(s.mrc, cur)}</td></tr>`;
    document.getElementById('sb-revenue').style.display = '';

    // Costs
    const oh = s.overhead || {};
    const kw  = s.watts ? (s.watts / 1000).toFixed(3) : null;
    let costRows = '';

    costRows += `<tr><td>HW amortization</td><td>${fmtMoney(s.hw_amortized, cur)}</td></tr>`;
    if (s.hw_paid_off) {
      costRows += `<tr class="dim indent"><td>Fully amortized</td><td></td></tr>`;
    } else if (s.hw_months_remaining != null) {
      costRows += `<tr class="dim indent"><td>Paid off in ${s.hw_months_remaining} months</td><td></td></tr>`;
    }

    if (oh.power_per_kw != null) {
      costRows += `<tr><td>Power</td><td>${fmtMoney(oh.power_per_kw, cur)}</td></tr>`;
      if (kw) costRows += `<tr class="dim indent"><td>${kw} kW</td><td></td></tr>`;
    }
    if (oh.dc_equipment != null) costRows += `<tr><td>DC Equipment</td><td>${fmtMoney(oh.dc_equipment, cur)}</td></tr>`;
    if (oh.network_equipment != null) costRows += `<tr><td>Network Equipment</td><td>${fmtMoney(oh.network_equipment, cur)}</td></tr>`;
    if (oh.dc_ops != null) costRows += `<tr><td>DC Operations</td><td>${fmtMoney(oh.dc_ops, cur)}</td></tr>`;
    if (oh.support_ops != null) costRows += `<tr><td>Support Ops</td><td>${fmtMoney(oh.support_ops, cur)}</td></tr>`;
    if (oh.network_ops != null) costRows += `<tr><td>Network Ops</td><td>${fmtMoney(oh.network_ops, cur)}</td></tr>`;
    if (oh.compute_ops != null) costRows += `<tr><td>Compute Ops</td><td>${fmtMoney(oh.compute_ops, cur)}</td></tr>`;

    const directTotal = Object.values(oh).reduce((a, v) => a + (v || 0), 0);
    costRows += `<tr class="sep"><td>Subtotal Direct</td><td>${fmtMoney(directTotal, cur)}</td></tr>`;
    costRows += `<tr><td>SG&amp;A</td><td>${fmtMoney(s.sga, cur)}</td></tr>`;
    costRows += `<tr class="sep"><td><strong>Total Cost</strong></td><td><strong>${fmtMoney(s.total_cost, cur)}</strong></td></tr>`;

    document.getElementById('sb-costs-table').innerHTML = costRows;
    document.getElementById('sb-costs').style.display = '';

    // Margin
    const pctClass = s.margin_pct == null ? '' : s.margin_pct >= 10 ? 'margin-pos' : 'margin-neg';
    const biggestLabel = {
      hw_amortized: 'HW Amortization', power_per_kw: 'Power', dc_equipment: 'DC Equipment',
      network_equipment: 'Network Equipment', dc_ops: 'DC Ops', support_ops: 'Support Ops',
      network_ops: 'Network Ops', compute_ops: 'Compute Ops', sga: 'SG&A',
    }[s.biggest_cost_driver] || s.biggest_cost_driver || '—';

    document.getElementById('sb-margin-table').innerHTML = `
      <tr class="${pctClass}"><td>Margin $</td><td>${fmtMoney(s.margin, cur)}</td></tr>
      <tr class="${pctClass}"><td>Margin %</td><td>${s.margin_pct != null ? s.margin_pct.toFixed(1) + '%' : '—'}</td></tr>
      <tr class="dim sep"><td>Biggest cost driver</td><td>${biggestLabel}</td></tr>`;
    document.getElementById('sb-margin-card').style.display = '';

    // Renewal link
    const link = document.getElementById('sb-renewal-link');
    link.href = `/renewal/${s.service_id}`;
    link.style.display = '';
  }

  function fmtMoney(val, cur) {
    if (val == null) return '—';
    return new Intl.NumberFormat('en-US', {
      style: 'currency', currency: cur || 'USD',
      minimumFractionDigits: 2, maximumFractionDigits: 2,
    }).format(val);
  }

  function showError(msg) {
    document.getElementById('cust-name').textContent = 'Error';
    document.getElementById('svc-tbody').innerHTML = `<tr><td colspan="7" class="empty-state">${msg}</td></tr>`;
  }

  load();
</script>
{% endblock %}
```

- [ ] **Step 2: Test the customer detail page**

Navigate to any customer row on the profitability landing page (click a row) or go directly to http://127.0.0.1:5050/profitability/1 (replace 1 with a real client_id from the API).

Verify:
- Customer name, account manager, service count shown in page header
- KPI cards show MRC/cost/margin/at-risk for this customer
- Service table rows are clickable, switching the sidebar
- Sidebar shows Revenue → Costs itemized → Margin summary
- "HW paid off in N months" or "Fully amortized" shown correctly
- "Open Renewal →" links to `/renewal/<service_id>`
- First row is selected by default when page loads

- [ ] **Step 3: Run full test suite**

```bash
pytest tests/ -v
```

Expected: all tests pass (test_overhead.py + test_renewal_pricing.py + test_profitability.py).

- [ ] **Step 4: Commit**

```bash
git add templates/profitability_customer.html
git commit -m "feat: implement profitability customer detail page with cost breakdown sidebar"
```

---

## Self-Review

**Spec coverage check:**
- ✅ Nav link between New Quotes and Renewals — Task 1
- ✅ `/profitability` landing page with KPI cards — Tasks 4, 5
- ✅ Filter bar identical to Renewals (AM, DC, service type, customer search) — Task 5
- ✅ Segment toggle (By Customer / By DC / By Service Type) — Tasks 4, 5
- ✅ Table sortable, default sort margin % asc — Task 5
- ✅ Currency selector, native default, JS client-side conversion via `/api/fx-rate` — Tasks 4, 5
- ✅ Mixed-currency customers show "—" until display currency selected — Tasks 4, 5
- ✅ `/profitability/<client_id>` customer detail — Tasks 4, 6
- ✅ Service table + cost breakdown sidebar — Task 6
- ✅ HW amortization (36-month, paid-off if age > 36mo, date from provision_date) — Task 3
- ✅ Overhead via `calc_overhead` from `lib/overhead.py` — Task 3
- ✅ `ocean_sku_cost` + `hardware_watts` as cost sources — Tasks 2, 3
- ✅ `dimClientsActive` for AM — Task 3
- ✅ "Open Renewal →" links to `/renewal/<service_id>` — Task 6
- ✅ Margin color thresholds: green ≥20%, orange 10–19%, red <10% — Tasks 5, 6
- ✅ No pills, no bars, plain colored % — Tasks 5, 6
- ✅ CSS variables from `base.html`, no new variables — Tasks 5, 6

**Placeholder scan:** None found.

**Type consistency:** `calc_service_margin` signature in Task 3 matches usage in `build_profitability_data` in Task 3. API response shape in Task 4 matches rendering in Tasks 5, 6. `overhead` is a dict keyed by cost line name throughout.
