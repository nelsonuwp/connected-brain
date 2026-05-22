# Renewals Section Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the monolithic CPQ app into a modular structure and add a fully functional Renewals section with filterable service list and per-service renewal pricing detail.

**Architecture:** Option B — Jinja2 template inheritance + modular backend. `app.py` becomes a thin wiring file; logic splits into `db/`, `lib/`, and `routes/` packages. A shared `base.html` provides navigation. Two new templates (`renewals.html`, `renewal.html`) implement the renewals UI.

**Tech Stack:** Python 3.14, Flask 3.0, pymssql, psycopg2, sshtunnel, pytest, vanilla JS (no new frontend deps)

---

## File Map

```
# Created
db/__init__.py
db/fusion.py          ← Postgres tunnel, DC registry, FX via Fusion (currently in app.py)
db/mssql.py           ← MSSQL helpers + new renewal queries (currently in app.py)
lib/__init__.py
lib/overhead.py       ← COST_DRIVERS loader + calc_overhead (currently in app.py)
lib/renewal_pricing.py ← pure pricing functions (hw_paid_off, calc_suggested_mrc)
routes/__init__.py
routes/cpq.py         ← existing CPQ routes (currently in app.py)
routes/renewals.py    ← new /renewals + /renewal/<id> + /api/renewals*
routes/settings.py    ← existing settings routes (currently in app.py)
templates/base.html   ← shared header, nav, theme
templates/renewals.html ← filterable grouped renewals table
templates/renewal.html  ← renewal detail + sidebar
tests/__init__.py
tests/test_overhead.py
tests/test_renewal_pricing.py

# Modified
app.py                ← shrinks to ~20 lines
templates/index.html  ← add {% extends "base.html" %}
templates/product.html ← add {% extends "base.html" %}
templates/settings.html ← add {% extends "base.html" %}
```

---

## Task 1: Project scaffolding + pytest setup

**Files:**
- Create: `db/__init__.py`, `lib/__init__.py`, `routes/__init__.py`, `tests/__init__.py`
- Create: `pytest.ini`

- [ ] **Create empty package init files**

```bash
mkdir -p db lib routes tests
touch db/__init__.py lib/__init__.py routes/__init__.py tests/__init__.py
```

- [ ] **Create `pytest.ini`**

```ini
[pytest]
testpaths = tests
```

- [ ] **Verify pytest runs (zero tests is fine)**

```bash
cd /Users/anelson-macbook-air/connected-brain/projects/cpq-front-end
python3 -m pytest -v
```

Expected: `no tests ran` or `0 passed`

- [ ] **Commit**

```bash
git add db/__init__.py lib/__init__.py routes/__init__.py tests/__init__.py pytest.ini
git commit -m "chore: scaffold db/, lib/, routes/, tests/ packages"
```

---

## Task 2: Extract `lib/overhead.py` + tests

**Files:**
- Create: `lib/overhead.py`
- Create: `tests/test_overhead.py`

- [ ] **Write failing tests first**

`tests/test_overhead.py`:
```python
import json
from lib.overhead import calc_overhead, COST_DRIVERS


def test_cost_drivers_loads():
    assert "overhead_constants" in COST_DRIVERS
    assert "data_centers" in COST_DRIVERS


def test_sga_calculation():
    # SGA is a percentage of MRC — verify it scales linearly
    result = calc_overhead("ATL", 1000.0, fx_rate=1.0)
    assert "sga" in result
    sga_pct = COST_DRIVERS["overhead_constants"]["sga_pct"]
    assert result["sga"]["amount"] == round(1000.0 * sga_pct, 2)


def test_unknown_dc_returns_empty():
    result = calc_overhead("NOTADC", 1000.0)
    assert result == {}


def test_fx_rate_applied_to_fixed_costs():
    result_1x = calc_overhead("ATL", 1000.0, fx_rate=1.0)
    result_2x = calc_overhead("ATL", 1000.0, fx_rate=2.0)
    for key in result_1x:
        if key == "sga":
            continue  # SGA is based on MRC, not a fixed amount
        if result_1x[key]["amount"] and result_1x[key]["amount"] > 0:
            assert result_2x[key]["amount"] == round(result_1x[key]["amount"] * 2, 2)
```

- [ ] **Run tests — verify they fail**

```bash
python3 -m pytest tests/test_overhead.py -v
```

Expected: `ModuleNotFoundError: No module named 'lib.overhead'`

- [ ] **Create `lib/overhead.py`**

```python
import json
from pathlib import Path

_COST_DRIVERS_PATH = Path(__file__).parent.parent / "cost_drivers.json"
COST_DRIVERS = {}


def _load():
    global COST_DRIVERS
    with open(_COST_DRIVERS_PATH) as f:
        COST_DRIVERS = json.load(f)


def reload():
    _load()


_load()


def calc_overhead(dc_code: str, mrc_display: float, fx_rate: float = 1.0,
                  kw: float | None = None, service_type: str = "server") -> dict:
    dc = COST_DRIVERS["data_centers"].get(dc_code)
    if not dc:
        return {}
    dc_costs = dc["costs"]
    if isinstance(next(iter(dc_costs.values())), dict) and "amount" not in next(iter(dc_costs.values())):
        costs = dc_costs.get(service_type) or dc_costs.get("server") or {}
    else:
        costs = dc_costs
    const = COST_DRIVERS["overhead_constants"]
    native = dc["native_currency"]
    lines = {}

    for key, entry in costs.items():
        amt = entry["amount"]
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
                formula = f"{amt} {native}/kW × kW unknown = N/A"
            else:
                native_val = round(amt * kw, 2)
                formula = f"{amt} {native}/kW × {kw} kW = {native_val} {native}"
        elif measure in ("per_device", "per_server"):
            native_val = round(amt, 2)
            formula = f"{amt} {native}/device"
        else:
            native_val = round(amt, 2)
            formula = str(amt)

        display_val = round(native_val * fx_rate, 2) if native_val is not None else None
        if fx_rate != 1.0 and native_val is not None:
            formula += f" × {fx_rate} FX = {display_val}"

        lines[key] = {
            "amount": display_val,
            "currency": native,
            "measure": measure,
            "provenance": {
                "source": "cost_drivers.json",
                "path": f"data_centers.{dc_code}.costs.{service_type}.{key}",
                "native_amount": native_val,
                "native_currency": native,
                "measure": measure,
                "formula": formula,
                "fx_rate": fx_rate,
            },
        }

    sga_pct = const["sga_pct"]
    sga_val = round(mrc_display * sga_pct, 2) if mrc_display else 0
    lines["sga"] = {
        "amount": sga_val,
        "currency": native,
        "measure": "pct_of_mrc",
        "provenance": {
            "source": "cost_drivers.json",
            "path": "overhead_constants.sga_pct",
            "formula": f"Total MRC {mrc_display} × {sga_pct} (SG&A %) = {sga_val}",
            "fx_rate": fx_rate,
        },
    }
    return lines
```

- [ ] **Run tests — verify they pass**

```bash
python3 -m pytest tests/test_overhead.py -v
```

Expected: 4 passed

- [ ] **Commit**

```bash
git add lib/overhead.py tests/test_overhead.py
git commit -m "feat: extract lib/overhead.py with tests"
```

---

## Task 3: Create `lib/renewal_pricing.py` + tests

**Files:**
- Create: `lib/renewal_pricing.py`
- Create: `tests/test_renewal_pricing.py`

- [ ] **Write failing tests**

`tests/test_renewal_pricing.py`:
```python
from datetime import date
from lib.renewal_pricing import hw_paid_off, provision_age_months, calc_suggested_mrc


def test_hw_paid_off_exactly_36_months():
    today = date(2026, 5, 22)
    prov = date(2023, 5, 22)
    assert hw_paid_off(prov, today=today) is True


def test_hw_not_paid_off_35_months():
    today = date(2026, 5, 22)
    prov = date(2023, 6, 22)
    assert hw_paid_off(prov, today=today) is False


def test_hw_paid_off_none_provision():
    assert hw_paid_off(None) is False


def test_provision_age_months():
    today = date(2026, 5, 22)
    prov = date(2024, 5, 22)
    assert provision_age_months(prov, today=today) == 24


def test_calc_suggested_mrc_term_no_multiplier():
    components = [
        {"component_category": "Hardware", "component_mrc": 40.0, "new_mrc": 40.0},
        {"component_category": "Software", "component_mrc": 85.0, "new_mrc": 185.0},
    ]
    result = calc_suggested_mrc(323.0, components, "36")
    # 323 + 40 (HW held flat) + 185 (new SW price) = 548, × 1.0
    assert result == 548.0


def test_calc_suggested_mrc_m2m_multiplier():
    components = [
        {"component_category": "Software", "component_mrc": 85.0, "new_mrc": 85.0},
    ]
    result = calc_suggested_mrc(323.0, components, "m2m")
    # (323 + 85) × 1.25 = 510.0
    assert result == 510.0


def test_calc_suggested_mrc_missing_new_price_falls_back():
    components = [
        {"component_category": "Software", "component_mrc": 85.0, "new_mrc": None},
    ]
    result = calc_suggested_mrc(323.0, components, "36")
    # Falls back to current_mrc when new_mrc is None
    assert result == 408.0


def test_calc_suggested_mrc_support_repriced():
    components = [
        {"component_category": "Support", "component_mrc": 0.0, "new_mrc": 50.0},
    ]
    result = calc_suggested_mrc(500.0, components, "12")
    assert result == 550.0
```

- [ ] **Run — verify failure**

```bash
python3 -m pytest tests/test_renewal_pricing.py -v
```

Expected: `ModuleNotFoundError`

- [ ] **Create `lib/renewal_pricing.py`**

```python
from datetime import date, datetime

_SW_SUPPORT_CATS = {"Software", "Support"}


def hw_paid_off(provision_date, today: date | None = None) -> bool:
    if provision_date is None:
        return False
    if today is None:
        today = date.today()
    if isinstance(provision_date, datetime):
        provision_date = provision_date.date()
    months = (today.year - provision_date.year) * 12 + (today.month - provision_date.month)
    return months >= 36


def provision_age_months(provision_date, today: date | None = None) -> int | None:
    if provision_date is None:
        return None
    if today is None:
        today = date.today()
    if isinstance(provision_date, datetime):
        provision_date = provision_date.date()
    return (today.year - provision_date.year) * 12 + (today.month - provision_date.month)


def calc_suggested_mrc(product_mrc: float, components: list, term: str) -> float:
    """
    Calculate suggested renewal MRC.

    product_mrc: base server MRC (unchanged in renewal)
    components: list of dicts with component_category, component_mrc, new_mrc
    term: 'm2m' | '12' | '24' | '36'

    SW/Support components re-priced at new_mrc (falls back to component_mrc if None).
    Hardware/Bandwidth/Network components held at component_mrc.
    m2m applies 1.25× multiplier.
    """
    total = float(product_mrc)
    for c in components:
        if c["component_category"] in _SW_SUPPORT_CATS:
            total += c["new_mrc"] if c["new_mrc"] is not None else c["component_mrc"]
        else:
            total += float(c["component_mrc"])
    multiplier = 1.25 if term == "m2m" else 1.0
    return round(total * multiplier, 2)
```

- [ ] **Run — verify all pass**

```bash
python3 -m pytest tests/test_renewal_pricing.py -v
```

Expected: 8 passed

- [ ] **Commit**

```bash
git add lib/renewal_pricing.py tests/test_renewal_pricing.py
git commit -m "feat: add renewal pricing pure functions with tests"
```

---

## Task 4: Extract `db/fusion.py`

**Files:**
- Create: `db/fusion.py`

- [ ] **Create `db/fusion.py`** — move all Postgres/Fusion functions from `app.py`

```python
import os
from decimal import Decimal
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor
from sshtunnel import SSHTunnelForwarder

from lib.overhead import COST_DRIVERS

SSH_HOST     = os.environ.get("SSH_HOST", "10.121.21.20")
SSH_PORT     = int(os.environ.get("SSH_PORT", "22"))
SSH_USER     = os.environ.get("SSH_USER", "")
SSH_PASSWORD = os.environ.get("SSH_PASS", "")

DB_REMOTE_HOST = os.environ.get("FUSION_DB_SERVER", "db1.peer1.com")
DB_REMOTE_PORT = int(os.environ.get("FUSION_DB_PORT", "5432"))
DB_NAME        = os.environ.get("FUSION_DB_NAME", "fusion")
DB_USER        = os.environ.get("FUSION_DB_USER", "sb_readonly")
DB_PASSWORD    = os.environ.get("FUSION_DB_PASS", "")

_tunnel = None
_conn   = None
_USE_TUNNEL = bool(SSH_USER and SSH_PASSWORD)

if _USE_TUNNEL:
    print(f"[fusion] SSH tunnel via {SSH_HOST}")
else:
    print("[fusion] direct connection mode")


def get_conn():
    global _tunnel, _conn
    if _conn:
        try:
            _conn.cursor().execute("SELECT 1")
            return _conn
        except Exception:
            _conn = None
    if _USE_TUNNEL:
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
        db_host = "127.0.0.1"
        db_port = _tunnel.local_bind_port
    else:
        db_host = DB_REMOTE_HOST
        db_port = DB_REMOTE_PORT
    _conn = psycopg2.connect(
        host=db_host, port=db_port,
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
        gssencmode="disable", cursor_factory=RealDictCursor,
    )
    _conn.set_session(readonly=True, autocommit=True)
    return _conn


_dc_registry = None


def _build_registry_from_cost_drivers() -> dict:
    result = {}
    for code, dc in COST_DRIVERS["data_centers"].items():
        native = dc["native_currency"]
        result[code] = {
            "id": dc["fusion_dc_id"], "dc_abbr": code, "name": dc["name"],
            "city": None, "state": None, "currencies": [native], "native_currency": native,
        }
    return result


def get_dc_registry() -> dict:
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
                LEFT JOIN public.datacenter_available_currencies dac ON dac.datacenter_id = sd.id
                WHERE sd.active = true
                GROUP BY sd.id, sd.dc_abbr, sd.name, sd.city, sd.state
                ORDER BY sd.dc_abbr
            """)
            rows = cur.fetchall()
        registry = {}
        for r in rows:
            abbr = r["dc_abbr"]
            currencies = r["currencies"] or []
            cd_entry = COST_DRIVERS["data_centers"].get(abbr, {})
            if len(currencies) == 1:
                native = currencies[0]
            else:
                native = cd_entry.get("native_currency") or (currencies[0] if currencies else "USD")
            registry[abbr] = {
                "id": r["id"], "dc_abbr": abbr, "name": r["name"],
                "city": r.get("city"), "state": r.get("state"),
                "currencies": currencies, "native_currency": native,
            }
        _dc_registry = registry
    except Exception:
        _dc_registry = _build_registry_from_cost_drivers()
    return _dc_registry


def get_dc_info(dc_abbr: str) -> dict | None:
    return get_dc_registry().get(dc_abbr.upper())


def dec(v) -> float:
    if v is None:
        return 0.0
    if isinstance(v, Decimal):
        return float(v)
    return float(v)
```

- [ ] **Verify import works**

```bash
python3 -c "from db.fusion import get_dc_info; print('ok')"
```

Expected: `ok` (may also print `[fusion] SSH tunnel via ...`)

- [ ] **Commit**

```bash
git add db/fusion.py
git commit -m "refactor: extract db/fusion.py from app.py"
```

---

## Task 5: Extract `db/mssql.py`

**Files:**
- Create: `db/mssql.py`

- [ ] **Create `db/mssql.py`** with existing MSSQL functions

```python
import os

MSSQL_SERVER   = os.environ.get("MSSQL_BI_SERVER") or os.environ.get("OCEAN_DB_SERVER", "")
MSSQL_DB       = os.environ.get("MSSQL_BI_NAME")   or os.environ.get("OCEAN_DB_NAME", "")
MSSQL_USER     = os.environ.get("MSSQL_BI_USER")   or os.environ.get("OCEAN_DB_USERNAME", "")
MSSQL_PASSWORD = os.environ.get("MSSQL_BI_PASS")   or os.environ.get("OCEAN_DB_PASSWORD", "")

_HW_SKU_TYPES = {"HW", "Hardware", "hw", "hardware"}


def _connect():
    import pymssql
    return pymssql.connect(
        server=MSSQL_SERVER, user=MSSQL_USER,
        password=MSSQL_PASSWORD, database=MSSQL_DB,
        tds_version="7.0",
    )


def _configured() -> bool:
    return all([MSSQL_SERVER, MSSQL_DB, MSSQL_USER, MSSQL_PASSWORD])


def get_mssql_costs(sku_ids: list[int], sku_level: str) -> dict[int, dict]:
    if not sku_ids or not _configured():
        return {}
    try:
        conn = _connect()
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
            is_hw = raw_type in _HW_SKU_TYPES or raw_type.upper().startswith("HW")
            result[r["sku_id"]] = {
                "cost": float(r["sku_cost"] or 0),
                "currency": r["cost_currency"] or "USD",
                "name": r["sku_name"] or "",
                "sku_type": raw_type,
                "sku_category": (r.get("sku_category") or "").strip(),
                "cost_kind": "hw" if is_hw else "sw",
            }
        cur.close()
        conn.close()
        return result
    except Exception:
        return {}


def get_mssql_watts(fusion_id: int) -> int | None:
    if not _configured():
        return None
    try:
        conn = _connect()
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


def get_fx_rate(from_currency: str, to_currency: str) -> float:
    if from_currency == to_currency:
        return 1.0
    if not _configured():
        return 1.0
    try:
        conn = _connect()
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
```

- [ ] **Verify import works**

```bash
python3 -c "from dotenv import load_dotenv; load_dotenv('.env'); load_dotenv('.env.local', override=True); from db.mssql import get_fx_rate; print(get_fx_rate('USD','USD'))"
```

Expected: `1.0`

- [ ] **Commit**

```bash
git add db/mssql.py
git commit -m "refactor: extract db/mssql.py from app.py"
```

---

## Task 6: Add renewal queries to `db/mssql.py`

**Files:**
- Modify: `db/mssql.py` — append three new functions

- [ ] **Append `get_renewal_services` to `db/mssql.py`**

```python
def get_renewal_services(
    company: str | None = None,
    client_id: int | None = None,
    service_id: int | None = None,
) -> list[dict]:
    """
    Returns services from ocean_services_renewal_date JOIN dimServices.
    Sorted: real future dates first (ascending), then m2m/sentinel dates.
    Expiration dates of 1899-12-31 are normalized to None.
    """
    if not _configured():
        return []
    try:
        conn = _connect()
        cur = conn.cursor(as_dict=True)

        conditions = []
        params = []
        if company:
            conditions.append("osrd.company_name LIKE %s")
            params.append(f"%{company}%")
        if client_id is not None:
            conditions.append("osrd.client_id = %d")
            params.append(int(client_id))
        if service_id is not None:
            conditions.append("osrd.service_id = %d")
            params.append(int(service_id))

        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = f"""
            SELECT
                osrd.client_id, osrd.company_name, osrd.service_id,
                osrd.expiration_date, osrd.m2m,
                ds.product, ds.datacenter_code, ds.currency,
                ds.mrc, ds.provision_date, ds.contract_months_remaining,
                ds.service_type, ds.fusion_id, ds.nickname,
                ds.service_status
            FROM DM_BusinessInsights.renewals.ocean_services_renewal_date osrd
            JOIN DM_BusinessInsights.dbo.dimServices ds
              ON ds.service_id = osrd.service_id
            {where}
            ORDER BY
                CASE
                    WHEN osrd.expiration_date > '1900-01-01'
                         AND (osrd.m2m IS NULL OR osrd.m2m != 'yes')
                    THEN 0 ELSE 1
                END,
                osrd.expiration_date ASC
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
            exp = row.get("expiration_date")
            row["expiration_date"] = (
                exp.date().isoformat()
                if exp and hasattr(exp, "date") and exp.year > 1900
                else None
            )
            prov = row.get("provision_date")
            row["provision_date"] = (
                prov.date().isoformat() if prov and hasattr(prov, "date") else None
            )
            row["m2m"] = row.get("m2m") == "yes"
            row["mrc"] = float(row.get("mrc") or 0)
            result.append(row)
        return result
    except Exception:
        return []


def get_service(service_id: int) -> dict | None:
    """Returns one dimServices row for service_id, or None."""
    if not _configured():
        return None
    try:
        conn = _connect()
        cur = conn.cursor(as_dict=True)
        cur.execute(
            "SELECT * FROM DM_BusinessInsights.dbo.dimServices WHERE service_id = %d",
            (service_id,),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            return None
        row = dict(row)
        for k in ("provision_date", "last_updated"):
            v = row.get(k)
            row[k] = v.date().isoformat() if v and hasattr(v, "date") else None
        row["mrc"] = float(row.get("mrc") or 0)
        row["usd_mrc"] = float(row.get("usd_mrc") or 0)
        row["cad_mrc"] = float(row.get("cad_mrc") or 0)
        return row
    except Exception:
        return None


def get_service_components(service_id: int) -> list[dict]:
    """Returns all dimComponents rows for service_id, ordered by category/type."""
    if not _configured():
        return []
    try:
        conn = _connect()
        cur = conn.cursor(as_dict=True)
        cur.execute("""
            SELECT
                integer_key, client_id, component_category, service_option_type,
                component_type, component, add_on, currency,
                component_mrc, product_mrc, component_id,
                is_online, service_id, datacenter_code, line_of_business
            FROM DM_BusinessInsights.dbo.dimComponents
            WHERE service_id = %d
            ORDER BY component_category, component_type, component
        """, (service_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        result = []
        for r in rows:
            row = dict(r)
            row["component_mrc"] = float(row.get("component_mrc") or 0)
            row["product_mrc"] = float(row.get("product_mrc") or 0)
            result.append(row)
        return result
    except Exception:
        return []
```

- [ ] **Verify queries return data**

```bash
python3 -c "
from dotenv import load_dotenv
load_dotenv('.env'); load_dotenv('.env.local', override=True)
from db.mssql import get_renewal_services, get_service, get_service_components
svcs = get_renewal_services(company='YANDAV')
print('renewal rows:', len(svcs))
svc = get_service(7981507)
print('service mrc:', svc['mrc'] if svc else 'NOT FOUND')
comps = get_service_components(7981507)
print('components:', len(comps))
"
```

Expected:
```
renewal rows: 1
service mrc: 448.0
components: 18
```

- [ ] **Commit**

```bash
git add db/mssql.py
git commit -m "feat: add renewal DB queries to db/mssql.py"
```

---

## Task 7: Extract `routes/settings.py`

**Files:**
- Create: `routes/settings.py`

- [ ] **Create `routes/settings.py`**

```python
import json
import os

from flask import Blueprint, jsonify, render_template, request

from lib.overhead import COST_DRIVERS, reload as reload_cost_drivers

settings_bp = Blueprint("settings", __name__)

_COST_DRIVERS_PATH = None  # set at import time below


def _get_path():
    from pathlib import Path
    return Path(__file__).parent.parent / "cost_drivers.json"


@settings_bp.route("/settings")
def settings_page():
    return render_template("settings.html", active_page="settings")


@settings_bp.route("/api/settings/overhead", methods=["GET"])
def settings_overhead_get():
    return jsonify(COST_DRIVERS)


@settings_bp.route("/api/settings/overhead", methods=["POST"])
def settings_overhead_post():
    data = request.get_json(force=True)

    try:
        sga = float(data.get("overhead_constants", {}).get("sga_pct", -1))
        if not (0 <= sga <= 1):
            return jsonify({"error": "sga_pct must be between 0 and 1"}), 400
    except (TypeError, ValueError):
        return jsonify({"error": "sga_pct must be a number"}), 400

    service_types = ["server", "firewall", "switch"]
    for dc_abbr, dc in data.get("data_centers", {}).items():
        for svc in service_types:
            for key, entry in dc.get("costs", {}).get(svc, {}).items():
                try:
                    if float(entry.get("amount", -1)) < 0:
                        return jsonify({"error": f"{dc_abbr}.{svc}.{key}: amount must be >= 0"}), 400
                except (TypeError, ValueError):
                    return jsonify({"error": f"{dc_abbr}.{svc}.{key}: amount must be a number"}), 400

    path = _get_path()
    tmp = path.with_suffix(".json.tmp")
    try:
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        os.replace(tmp, path)
    except Exception as e:
        return jsonify({"error": f"Write failed: {e}"}), 500

    reload_cost_drivers()
    return jsonify({"ok": True})
```

- [ ] **Commit**

```bash
git add routes/settings.py
git commit -m "refactor: extract routes/settings.py from app.py"
```

---

## Task 8: Extract `routes/cpq.py`

**Files:**
- Create: `routes/cpq.py`

- [ ] **Create `routes/cpq.py`**

```python
from flask import Blueprint, jsonify, render_template, request

from db.fusion import dec, get_conn, get_dc_info, get_dc_registry
from db.mssql import get_fx_rate, get_mssql_costs, get_mssql_watts
from lib.overhead import calc_overhead

cpq_bp = Blueprint("cpq", __name__)


@cpq_bp.route("/")
def index():
    return render_template("index.html", active_page="quotes")


@cpq_bp.route("/product/<int:product_id>")
def product_page(product_id):
    return render_template("product.html", product_id=product_id, active_page="quotes")


@cpq_bp.route("/api/datacenters")
def datacenters():
    registry = get_dc_registry()
    return jsonify([
        {
            "code": info["dc_abbr"], "name": info["name"],
            "fusion_dc_id": info["id"], "currencies": info["currencies"],
            "native_currency": info["native_currency"],
        }
        for info in sorted(registry.values(), key=lambda x: x["dc_abbr"])
    ])


@cpq_bp.route("/api/fx-rate")
def fx_rate_endpoint():
    from_cur = request.args.get("from", "USD").upper()
    to_cur   = request.args.get("to",   "USD").upper()
    rate     = get_fx_rate(from_cur, to_cur)
    return jsonify({"from": from_cur, "to": to_cur, "rate": rate})


@cpq_bp.route("/api/servers")
def servers():
    dc_abbr      = request.args.get("dc", "").upper()
    currency     = request.args.get("currency", "USD").upper()
    product_line = request.args.get("product_line", "4")

    dc_info = get_dc_info(dc_abbr)
    if not dc_info:
        return jsonify({"error": f"Unknown DC: {dc_abbr}"}), 400

    fusion_dc_id    = dc_info["id"]
    native_currency = dc_info["native_currency"]

    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT pc.id, pc.name, pc.description, pc.sku,
                   pc.available_in_shop, pc.sold_out, pc.limited_availability,
                   pb_disp.id   AS pb_disp_id,
                   pb_disp.mrc  AS disp_mrc,  pb_disp.nrc  AS disp_nrc,
                   pb_disp.setup AS disp_setup, pb_disp.is_available AS disp_available,
                   pb_nat.id    AS pb_nat_id,
                   pb_nat.mrc   AS nat_mrc,   pb_nat.nrc   AS nat_nrc,
                   pb_nat.setup  AS nat_setup,  pb_nat.is_available  AS nat_available
            FROM public.product_catalog pc
            LEFT JOIN LATERAL (
                SELECT id, mrc, nrc, setup, is_available
                FROM public.pricebook
                WHERE product_catalog_id = pc.id AND currency = %s
                  AND datacenter = %s AND product_line_id = %s AND component_id IS NULL
                LIMIT 1
            ) pb_disp ON true
            LEFT JOIN LATERAL (
                SELECT id, mrc, nrc, setup, is_available
                FROM public.pricebook
                WHERE product_catalog_id = pc.id AND currency = %s
                  AND datacenter = %s AND product_line_id = %s AND component_id IS NULL
                LIMIT 1
            ) pb_nat ON true
            WHERE pc.product_class = 1 AND pc.is_active = true
              AND EXISTS (
                  SELECT 1 FROM public.pricebook
                  WHERE product_catalog_id = pc.id AND datacenter = %s
                    AND product_line_id = %s AND component_id IS NULL
              )
            ORDER BY COALESCE(pb_disp.mrc, pb_nat.mrc) ASC NULLS LAST
        """, (
            currency, fusion_dc_id, product_line,
            native_currency, fusion_dc_id, product_line,
            fusion_dc_id, product_line,
        ))
        rows = cur.fetchall()

    fx_native_to_display = (
        get_fx_rate(native_currency, currency) if native_currency != currency else 1.0
    )

    result = []
    for r in rows:
        warnings = []
        if r["pb_disp_id"] is not None:
            mrc_pb = dec(r["disp_mrc"]); nrc_pb = dec(r["disp_nrc"])
            setup_pb = dec(r["disp_setup"]); fx = 1.0
            pb_id = r["pb_disp_id"]; is_avail = r["disp_available"]
            pricing_cur = currency
        elif r["pb_nat_id"] is not None:
            mrc_pb = dec(r["nat_mrc"]); nrc_pb = dec(r["nat_nrc"])
            setup_pb = dec(r["nat_setup"]); fx = fx_native_to_display
            pb_id = r["pb_nat_id"]; is_avail = r["nat_available"]
            pricing_cur = native_currency
            if native_currency != currency:
                warnings.append("no_pricebook_in_display_currency")
        else:
            mrc_pb = nrc_pb = setup_pb = fx = 0.0
            pb_id = is_avail = pricing_cur = None
            warnings.append("no_pricebook_row")

        if pb_id is not None and mrc_pb == 0:
            warnings.append("mrc_is_zero")
        if is_avail is False:
            warnings.append("not_available_in_pricebook")

        result.append({
            "id": r["id"], "name": r["name"], "description": r["description"],
            "sku": r["sku"], "available_in_shop": r["available_in_shop"],
            "sold_out": r["sold_out"], "limited_availability": r["limited_availability"],
            "pricebook_id": pb_id,
            "mrc": round(mrc_pb * fx, 2) if pb_id is not None else None,
            "nrc": round(nrc_pb * fx, 2), "setup": round(setup_pb * fx, 2),
            "is_available": is_avail, "pricing_currency": pricing_cur,
            "display_currency": currency, "fx_pricing": fx, "warnings": warnings,
        })

    return jsonify(result)


@cpq_bp.route("/api/product/<int:product_id>")
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


@cpq_bp.route("/api/product/<int:product_id>/config")
def product_config(product_id):
    dc_abbr      = request.args.get("dc", "ATL").upper()
    currency     = request.args.get("currency", "USD").upper()
    product_line = request.args.get("product_line", "4")
    term_months  = int(request.args.get("term", "36"))

    dc_info = get_dc_info(dc_abbr)
    if not dc_info:
        return jsonify({"error": f"Unknown DC: {dc_abbr}"}), 400

    fusion_dc_id    = dc_info["id"]
    native_currency = dc_info["native_currency"]
    fx_overhead     = get_fx_rate(native_currency, currency)

    conn = get_conn()

    def _query_server_pb(pb_currency):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT pb.id AS pricebook_id, pb.mrc, pb.nrc, pb.setup
                FROM public.pricebook pb
                WHERE pb.product_catalog_id = %s AND pb.component_id IS NULL
                  AND pb.currency = %s AND pb.datacenter = %s
                  AND pb.product_line_id = %s AND pb.is_available = true
                LIMIT 1
            """, (product_id, pb_currency, fusion_dc_id, product_line))
            return cur.fetchone()

    pb_row = _query_server_pb(currency)
    if pb_row:
        pricing_currency = currency; fx_pricing = 1.0
    else:
        pb_row = _query_server_pb(native_currency)
        pricing_currency = native_currency
        fx_pricing = get_fx_rate(native_currency, currency)

    server_mrc_pb   = dec(pb_row["mrc"])   if pb_row else 0
    server_nrc_pb   = dec(pb_row["nrc"])   if pb_row else 0
    server_setup_pb = dec(pb_row["setup"]) if pb_row else 0
    server_mrc      = round(server_mrc_pb   * fx_pricing, 2)
    server_nrc      = round(server_nrc_pb   * fx_pricing, 2)
    server_setup    = round(server_setup_pb * fx_pricing, 2)
    pricebook_id    = pb_row["pricebook_id"] if pb_row else None

    pb_provenance = {
        "source": "Fusion: public.pricebook",
        "filters": (
            f"product_catalog_id={product_id}, currency={pricing_currency}, "
            f"datacenter={fusion_dc_id} ({dc_abbr}), product_line_id={product_line}, "
            f"component_id IS NULL, is_available=true"
        ),
        "pricebook_id": pricebook_id, "field": "pricebook.mrc",
        "pb_value": server_mrc_pb, "pricing_currency": pricing_currency,
        "fx_pricing": fx_pricing,
        "fx_source": (
            f"MSSQL: dbo.dimCurrencyExchangeRates "
            f"WHERE from_currency='{pricing_currency}' AND to_currency='{currency}'"
        ) if fx_pricing != 1.0 else "direct — no conversion needed",
        "display_value": server_mrc, "display_currency": currency,
    }

    def _query_components(table, id_col, pb_currency):
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT t.{id_col} AS component_id,
                       {'t.quantity,' if table == 'public.product_templates' else '1 AS quantity,'}
                       c.display_name AS name, c.description, c.is_active,
                       ct.name AS component_type, pct.name AS parent_type,
                       cc.name AS category, cc.sort_order AS cat_sort,
                       pb.id AS pricebook_id,
                       pb.mrc AS component_mrc, pb.nrc AS component_nrc,
                       pb.setup AS component_setup, pb.product_line_id AS pb_product_line_id
                FROM {table} t
                JOIN public.components c ON c.id = t.{id_col}
                JOIN public.component_types ct ON ct.id = c.component_type_id
                LEFT JOIN public.component_types pct ON pct.id = ct.parent_component_id
                JOIN public.component_categories cc ON cc.id = ct.category_id
                LEFT JOIN LATERAL (
                    SELECT id, mrc, nrc, setup, product_line_id FROM public.pricebook
                    WHERE component_id = t.{id_col} AND currency = %s
                      AND datacenter = %s AND is_available = true
                    ORDER BY (product_line_id = %s) DESC, product_line_id
                    LIMIT 1
                ) pb ON true
                WHERE t.product_id = %s
                {'AND c.is_active = true' if table == 'public.product_allowed_components' else ''}
                ORDER BY cc.sort_order, cc.name, ct.name, c.display_name
            """, (pb_currency, fusion_dc_id, product_line, product_id))
            return cur.fetchall()

    defaults_raw = _query_components("public.product_templates", "component_id", pricing_currency)
    allowed_raw  = _query_components("public.product_allowed_components", "component_id", pricing_currency)

    component_ids = list(
        {r["component_id"] for r in defaults_raw} | {r["component_id"] for r in allowed_raw}
    )
    hw_costs_comp = get_mssql_costs(component_ids, "Component") if component_ids else {}
    hw_costs_tls  = get_mssql_costs([product_id], "TLS")
    hw_costs      = {**hw_costs_comp, **hw_costs_tls}

    cost_currencies = {v["currency"] for v in hw_costs.values() if v.get("currency")}
    fx_cost_map     = {c: get_fx_rate(c, currency) for c in cost_currencies}

    def _fmt_component(r, is_default=False, quantity=1):
        cid = r["component_id"]
        mrc_pb = dec(r["component_mrc"])
        nrc_pb = dec(r["component_nrc"])
        addon_mrc_display   = round(mrc_pb * fx_pricing, 2)
        addon_nrc_display   = round(nrc_pb * fx_pricing, 2)
        setup_pb            = dec(r.get("component_setup") or 0)
        addon_setup_display = round(setup_pb * fx_pricing, 2)
        mrc_display   = 0.0 if is_default else addon_mrc_display
        nrc_display   = 0.0 if is_default else addon_nrc_display
        setup_display = 0.0 if is_default else addon_setup_display
        pb_id = r.get("pricebook_id")

        hw = hw_costs.get(cid)
        if hw:
            hw_cost_raw = hw["cost"]; hw_cost_currency = hw["currency"]
            fx_cost = fx_cost_map.get(hw_cost_currency, 1.0)
            hw_cost_display = round(hw_cost_raw * fx_cost, 2)
            cost_kind = hw.get("cost_kind", "hw")
        else:
            hw_cost_raw = hw_cost_currency = fx_cost = hw_cost_display = cost_kind = None

        return {
            "component_id": cid, "name": r["name"],
            "description": r["description"] or "", "is_active": r["is_active"],
            "component_type": r["component_type"], "parent_type": r.get("parent_type"),
            "category": r["category"], "cat_sort": r["cat_sort"], "quantity": quantity,
            "component_mrc": mrc_display, "component_nrc": nrc_display,
            "component_setup": setup_display, "addon_mrc": addon_mrc_display,
            "addon_setup": addon_setup_display, "hw_cost_raw": hw_cost_raw,
            "hw_cost_currency": hw_cost_currency, "hw_cost_display": hw_cost_display,
            "cost_kind": cost_kind, "is_default": is_default,
            "pricebook_provenance": {
                "source": "Fusion: public.pricebook", "pricebook_id": pb_id,
                "field": "pricebook.mrc",
                "filters": (
                    f"component_id={cid}, currency={pricing_currency}, "
                    f"datacenter={fusion_dc_id} ({dc_abbr}), "
                    f"product_line_id={product_line}, is_available=true"
                ),
                "pb_value": mrc_pb, "pricing_currency": pricing_currency,
                "fx_pricing": fx_pricing, "display_value": addon_mrc_display,
                "display_currency": currency, "included_in_base": is_default,
            } if pb_id else None,
            "hw_provenance": {
                "source": "MSSQL: DM_BusinessInsights.profitability.ocean_sku_cost",
                "field": "sku_cost", "sku_id": cid,
                "sku_name": hw["name"] if hw else None,
                "cost_value": hw_cost_raw, "cost_currency": hw_cost_currency,
                "fx_cost": fx_cost,
                "fx_source": (
                    f"dbo.dimCurrencyExchangeRates WHERE from_currency='{hw_cost_currency}' "
                    f"AND to_currency='{currency}' ORDER BY start_date DESC"
                ) if hw_cost_currency and hw_cost_currency != currency else None,
                "display_value": hw_cost_display, "display_currency": currency,
                "formula": (
                    f"{hw_cost_raw} {hw_cost_currency} × {fx_cost} = {hw_cost_display} {currency}"
                    if hw_cost_raw else "Not in ocean_sku_cost"
                ),
            } if hw else None,
        }

    defaults    = [_fmt_component(r, is_default=True, quantity=r["quantity"]) for r in defaults_raw]
    allowed     = [_fmt_component(r, is_default=False) for r in allowed_raw]
    default_ids = {r["component_id"] for r in defaults_raw}

    total_mrc = server_mrc + sum(
        d["component_mrc"] * d["quantity"] for d in defaults if d["component_mrc"] > 0
    )

    server_hw = hw_costs.get(product_id)
    if server_hw and server_hw["cost"] > 0:
        hw_capex_raw = server_hw["cost"]; hw_capex_currency = server_hw["currency"]
        fx_cost_server = fx_cost_map.get(hw_capex_currency, 1.0)
        total_hw_capex = round(hw_capex_raw * fx_cost_server, 2)
        hw_capex_method = "server-level"; hw_capex_sku_name = server_hw["name"]
    else:
        hw_capex_raw = sum(
            hw_costs[d["component_id"]]["cost"] * d["quantity"]
            if d["component_id"] in hw_costs else 0
            for d in defaults
        )
        first_hw = next((hw_costs[d["component_id"]] for d in defaults if d["component_id"] in hw_costs), None)
        hw_capex_currency = first_hw["currency"] if first_hw else "USD"
        fx_cost_server = fx_cost_map.get(hw_capex_currency, 1.0)
        total_hw_capex = round(hw_capex_raw * fx_cost_server, 2)
        hw_capex_method = "component-sum"; hw_capex_sku_name = None

    server_watts = get_mssql_watts(product_id)
    server_kw    = round(server_watts / 1000, 4) if server_watts is not None else None
    overhead     = calc_overhead(dc_abbr, total_mrc, fx_rate=fx_overhead, kw=server_kw)

    return jsonify({
        "product_id": product_id, "server_mrc": server_mrc,
        "server_nrc": server_nrc, "server_setup": server_setup,
        "currency": currency, "native_currency": native_currency,
        "pricing_currency": pricing_currency, "dc_code": dc_abbr,
        "fusion_dc_id": fusion_dc_id, "product_line": int(product_line),
        "term_months": term_months, "fx_pricing": fx_pricing,
        "fx_overhead": fx_overhead,
        "fx_source": "MSSQL: DM_BusinessInsights.dbo.dimCurrencyExchangeRates",
        "defaults": defaults, "allowed": allowed,
        "default_ids": list(default_ids),
        "server_watts": server_watts, "server_kw": server_kw,
        "overhead": overhead, "total_hw_capex": total_hw_capex,
        "hw_capex_cost": hw_capex_raw, "hw_capex_currency": hw_capex_currency,
        "hw_capex_provenance": {
            "source": "MSSQL: DM_BusinessInsights.profitability.ocean_sku_cost",
            "field": "sku_cost",
            "sku_id": product_id if hw_capex_method == "server-level" else "multiple",
            "sku_name": hw_capex_sku_name, "method": hw_capex_method,
            "cost_value": hw_capex_raw, "cost_currency": hw_capex_currency,
            "fx_cost": fx_cost_server,
            "fx_source": (
                f"dbo.dimCurrencyExchangeRates WHERE from_currency='{hw_capex_currency}' "
                f"AND to_currency='{currency}' ORDER BY start_date DESC"
            ) if hw_capex_currency != currency else "same currency — no conversion",
            "display_value": total_hw_capex, "display_currency": currency,
            "formula": f"{hw_capex_raw} {hw_capex_currency} × {fx_cost_server} = {total_hw_capex} {currency}",
        },
        "total_mrc": round(total_mrc, 2),
        "server_mrc_provenance": pb_provenance,
    })
```

- [ ] **Commit**

```bash
git add routes/cpq.py
git commit -m "refactor: extract routes/cpq.py from app.py"
```

---

## Task 9: Create `routes/renewals.py`

**Files:**
- Create: `routes/renewals.py`

- [ ] **Create `routes/renewals.py`**

```python
from collections import OrderedDict

from flask import Blueprint, jsonify, render_template, request

from db.fusion import get_conn, get_dc_info
from db.mssql import (get_fx_rate, get_mssql_costs, get_renewal_services,
                      get_service, get_service_components)
from lib.overhead import calc_overhead
from lib.renewal_pricing import (calc_suggested_mrc, hw_paid_off,
                                 provision_age_months)

renewals_bp = Blueprint("renewals", __name__)


def _group_renewals(rows: list[dict]) -> list[dict]:
    groups: dict = OrderedDict()
    for row in rows:
        key = (row["client_id"], row.get("expiration_date"))
        if key not in groups:
            groups[key] = {
                "client_id": row["client_id"],
                "company_name": row["company_name"],
                "expiration_date": row.get("expiration_date"),
                "m2m": row["m2m"],
                "total_mrc": 0.0,
                "service_count": 0,
                "services": [],
            }
        g = groups[key]
        g["total_mrc"] += row["mrc"]
        g["service_count"] += 1
        g["services"].append({
            "service_id": row["service_id"],
            "product": row.get("product"),
            "datacenter_code": row.get("datacenter_code"),
            "mrc": row["mrc"],
            "currency": row.get("currency"),
            "service_status": row.get("service_status"),
            "service_type": row.get("service_type"),
            "nickname": row.get("nickname"),
        })

    result = []
    for g in groups.values():
        services = g["services"]
        dcs = {s["datacenter_code"] for s in services if s["datacenter_code"]}
        products = {s["product"] for s in services if s["product"]}
        g["dc"] = list(dcs)[0] if len(dcs) == 1 else "Mixed"
        g["product"] = list(products)[0] if len(products) == 1 else "Mixed"
        g["total_mrc"] = round(g["total_mrc"], 2)
        result.append(g)
    return result


@renewals_bp.route("/renewals")
def renewals_page():
    return render_template("renewals.html", active_page="renewals")


@renewals_bp.route("/renewal/<int:service_id>")
def renewal_page(service_id):
    return render_template("renewal.html", service_id=service_id, active_page="renewals")


@renewals_bp.route("/api/renewals")
def api_renewals():
    company    = request.args.get("company", "").strip() or None
    client_id  = request.args.get("client_id", "").strip() or None
    service_id = request.args.get("service_id", "").strip() or None
    try:
        client_id  = int(client_id)  if client_id  else None
        service_id = int(service_id) if service_id else None
    except ValueError:
        return jsonify({"error": "client_id and service_id must be integers"}), 400

    rows   = get_renewal_services(company=company, client_id=client_id, service_id=service_id)
    groups = _group_renewals(rows)
    return jsonify({"groups": groups, "total_services": len(rows)})


@renewals_bp.route("/api/renewals/<int:service_id>")
def api_renewal_detail(service_id):
    service = get_service(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    components   = get_service_components(service_id)
    currency     = (service.get("currency") or "USD").upper()
    dc_code      = (service.get("datacenter_code") or "").upper()
    fusion_pid   = service.get("fusion_id")  # maps to product_catalog.id in Fusion

    # Fusion DC lookup for pricebook queries
    dc_info         = get_dc_info(dc_code) if dc_code else None
    fusion_dc_id    = dc_info["id"] if dc_info else None
    native_currency = dc_info["native_currency"] if dc_info else currency
    fx_pricing      = get_fx_rate(native_currency, currency) if native_currency != currency else 1.0

    # Enrich each component with current pricebook price from Fusion
    enriched = []
    if fusion_dc_id and fusion_pid:
        conn = get_conn()
        for comp in components:
            cid     = comp.get("component_id")
            new_mrc = None
            in_pb   = False
            warning = None

            if cid:
                # Check allowed components
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT 1 FROM public.product_allowed_components "
                        "WHERE product_id = %s AND component_id = %s",
                        (fusion_pid, cid),
                    )
                    allowed = cur.fetchone() is not None

                if allowed:
                    # Try display currency first
                    with conn.cursor() as cur:
                        cur.execute("""
                            SELECT mrc FROM public.pricebook
                            WHERE component_id = %s AND currency = %s
                              AND datacenter = %s AND is_available = true
                            LIMIT 1
                        """, (cid, currency, fusion_dc_id))
                        pb = cur.fetchone()

                    if pb:
                        new_mrc = round(float(pb["mrc"] or 0), 2)
                        in_pb   = True
                    elif native_currency != currency:
                        # Fallback: native currency + FX
                        with conn.cursor() as cur:
                            cur.execute("""
                                SELECT mrc FROM public.pricebook
                                WHERE component_id = %s AND currency = %s
                                  AND datacenter = %s AND is_available = true
                                LIMIT 1
                            """, (cid, native_currency, fusion_dc_id))
                            pb = cur.fetchone()
                        if pb:
                            new_mrc = round(float(pb["mrc"] or 0) * fx_pricing, 2)
                            in_pb   = True
                        else:
                            warning = "not_in_pricebook"
                    else:
                        warning = "not_in_pricebook"
                else:
                    warning = "not_in_pricebook"

            delta = round((new_mrc - comp["component_mrc"]), 2) if new_mrc is not None else None
            enriched.append({**comp, "new_mrc": new_mrc, "delta": delta,
                              "in_pricebook": in_pb, "warning": warning})
    else:
        enriched = [{**c, "new_mrc": None, "delta": None,
                     "in_pricebook": False, "warning": "dc_not_in_fusion"}
                    for c in components]

    # HW CapEx from MSSQL
    hw_capex_display = 0.0
    hw_capex_currency = currency
    if fusion_pid:
        hw = get_mssql_costs([fusion_pid], "TLS").get(fusion_pid)
        if hw:
            fx_cap = get_fx_rate(hw["currency"], currency) if hw["currency"] != currency else 1.0
            hw_capex_display  = round(hw["cost"] * fx_cap, 2)
            hw_capex_currency = currency

    # HW paid-off
    from datetime import date as _date
    prov_str  = service.get("provision_date")
    prov_date = None
    if prov_str:
        try:
            prov_date = _date.fromisoformat(prov_str[:10])
        except ValueError:
            pass
    paid_off   = hw_paid_off(prov_date)
    age_months = provision_age_months(prov_date)

    # product_mrc = base server MRC (same across all component rows)
    product_mrc = float(components[0]["product_mrc"]) if components else 0.0

    # Overhead FX
    fx_overhead = get_fx_rate(native_currency, currency) if native_currency != currency else 1.0

    # Pre-calculate all four term scenarios
    pricing = {}
    for term in ("m2m", "12", "24", "36"):
        term_months_val = {"m2m": 1, "12": 12, "24": 24, "36": 36}[term]
        suggested       = calc_suggested_mrc(product_mrc, enriched, term)
        hw_cost_mo      = 0.0 if paid_off else round(hw_capex_display / term_months_val, 2)
        overhead_lines  = calc_overhead(dc_code, suggested, fx_rate=fx_overhead)
        overhead_total  = round(sum(
            v["amount"] for v in overhead_lines.values() if v.get("amount")
        ), 2)
        total_cost = round(hw_cost_mo + overhead_total, 2)
        margin     = round(suggested - total_cost, 2)
        margin_pct = round(margin / suggested * 100, 1) if suggested > 0 else 0.0

        sw_delta = round(sum(
            (c["delta"] or 0)
            for c in enriched
            if c["component_category"] in {"Software", "Support"} and c["delta"] is not None
        ), 2)

        pricing[term] = {
            "suggested_mrc":  suggested,
            "hw_cost_mo":     hw_cost_mo,
            "overhead_total": overhead_total,
            "total_cost":     total_cost,
            "margin":         margin,
            "margin_pct":     margin_pct,
            "sw_support_delta": sw_delta,
        }

    return jsonify({
        "service":            service,
        "components":         enriched,
        "product_mrc":        product_mrc,
        "hw_capex":           hw_capex_display,
        "hw_capex_currency":  hw_capex_currency,
        "hw_paid_off":        paid_off,
        "provision_age_months": age_months,
        "pricing":            pricing,
    })
```

- [ ] **Commit**

```bash
git add routes/renewals.py
git commit -m "feat: add routes/renewals.py with list and detail endpoints"
```

---

## Task 10: Refactor `app.py` to thin wiring

**Files:**
- Modify: `app.py`

- [ ] **Replace `app.py` entirely**

```python
from dotenv import load_dotenv

load_dotenv(".env")
load_dotenv(".env.local", override=True)

from flask import Flask

from routes.cpq import cpq_bp
from routes.renewals import renewals_bp
from routes.settings import settings_bp

app = Flask(__name__)
app.register_blueprint(cpq_bp)
app.register_blueprint(renewals_bp)
app.register_blueprint(settings_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
```

- [ ] **Start the app and verify existing routes still work**

```bash
python3 app.py &
sleep 2
curl -s http://localhost:5050/api/datacenters | python3 -m json.tool | head -20
```

Expected: JSON array of datacenters

```bash
curl -s http://localhost:5050/ | grep -o '<title>[^<]*</title>'
```

Expected: `<title>CPQ — Server Pricing · Aptum</title>`

- [ ] **Stop the dev server**

```bash
kill %1
```

- [ ] **Commit**

```bash
git add app.py
git commit -m "refactor: slim app.py to blueprint wiring, all logic in routes/db/lib"
```

---

## Task 11: Create `base.html`

**Files:**
- Create: `templates/base.html`

- [ ] **Create `templates/base.html`**

```html
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{% block title %}CPQ · Aptum{% endblock %}</title>
  <style>
    @font-face { font-family:'Geist'; src:url('https://aptumlogos.pages.dev/Geist-Light.ttf') format('truetype'); font-weight:300; font-display:swap; }
    @font-face { font-family:'Geist'; src:url('https://aptumlogos.pages.dev/Geist-Regular.ttf') format('truetype'); font-weight:400; font-display:swap; }
    @font-face { font-family:'Geist'; src:url('https://aptumlogos.pages.dev/Geist-Medium.ttf') format('truetype'); font-weight:500; font-display:swap; }
    @font-face { font-family:'Geist'; src:url('https://aptumlogos.pages.dev/Geist-Bold.ttf') format('truetype'); font-weight:700; font-display:swap; }
    @font-face { font-family:'Geist Mono'; src:url('https://aptumlogos.pages.dev/GeistMono-Regular.ttf') format('truetype'); font-weight:400; font-display:swap; }

    :root {
      --bg:#081820; --bg-dot:#142233; --surface:#0d1f2d; --surface-2:#060f15;
      --border:#142233; --border-mid:#1e3547; --text-1:#F8F7FA; --text-2:#88898D;
      --text-3:#515357; --accent:#7D7AE8; --accent-dim:#2A1F6E; --accent-text:#D4D3FF;
      --green:#BED6A8; --green-dim:#1a3d1f; --green-text:#BED6A8;
      --orange:#FFBE81; --orange-dim:#3d1a06; --orange-text:#FFBE81;
      --red:#ef4444; --red-dim:#3b1220; --red-text:#fca5a5;
      --shadow:rgba(0,0,0,.25);
    }
    [data-theme="light"] {
      --bg:#F8F7FA; --bg-dot:#D0D1DE; --surface:#FFFFFF; --surface-2:#F0EFF5;
      --border:#D0D1DE; --border-mid:#88898D; --text-1:#081820; --text-2:#515357;
      --text-3:#88898D; --accent:#655BD9; --accent-dim:#E7E6FF; --accent-text:#3A2699;
      --green:#2d6e1f; --green-dim:#E9FEDF; --green-text:#1a4a10;
      --orange:#a05000; --orange-dim:#FFEBD9; --orange-text:#7a3a00;
      --red:#c41c1c; --red-dim:#FEE8E8; --red-text:#9b1515;
      --shadow:rgba(0,0,0,.06);
    }
    *, *::before, *::after { box-sizing:border-box; margin:0; padding:0; }
    body {
      font-family:'Geist', system-ui, sans-serif;
      background-color:var(--bg);
      background-image:radial-gradient(var(--bg-dot) 1px, transparent 0);
      background-size:28px 28px;
      color:var(--text-2); min-height:100vh;
      transition:background-color .25s, color .25s;
    }
    header {
      display:flex; align-items:center; gap:1rem;
      padding:1.25rem 2rem; border-bottom:1px solid var(--border);
    }
    header img.logo { height:28px; width:auto; display:block; }
    .hdr-divider { width:1px; height:22px; background:var(--border); }
    nav.top-nav { display:flex; align-items:center; gap:.25rem; }
    nav.top-nav a {
      font-size:.8rem; font-weight:500; color:var(--text-2);
      text-decoration:none; padding:.35rem .75rem; border-radius:7px;
      border:1px solid transparent;
      transition:color .15s, border-color .15s;
    }
    nav.top-nav a:hover { color:var(--text-1); border-color:var(--border); }
    nav.top-nav a.active {
      color:var(--accent); border-color:var(--accent);
      background:var(--accent-dim);
    }
    .hdr-right { margin-left:auto; display:flex; align-items:center; gap:.75rem; }
    .theme-btn {
      background:var(--surface); border:1px solid var(--border);
      color:var(--text-2); font-size:.9rem; line-height:1;
      width:34px; height:34px; border-radius:8px;
      cursor:pointer; display:flex; align-items:center; justify-content:center;
      transition:border-color .15s, background .2s;
    }
    .theme-btn:hover { border-color:var(--accent); color:var(--accent); }
    .page-body { padding:2rem; }
    {% block extra_styles %}{% endblock %}
  </style>
</head>
<body>
<header>
  <img id="main-logo" class="logo"
       src="https://aptumlogos.pages.dev/Aptum-Logo-Horizontal-Lockup-White.png" alt="Aptum" />
  <div class="hdr-divider"></div>
  <nav class="top-nav">
    <a href="/" class="{{ 'active' if active_page == 'quotes' else '' }}">New Quotes</a>
    <a href="/renewals" class="{{ 'active' if active_page == 'renewals' else '' }}">Renewals</a>
    <a href="/settings" class="{{ 'active' if active_page == 'settings' else '' }}">Settings</a>
  </nav>
  <div class="hdr-right">
    <button class="theme-btn" id="theme-btn" onclick="toggleTheme()" aria-label="Toggle colour scheme">☀</button>
  </div>
</header>
{% block body %}{% endblock %}
<script>
  const THEME_KEY = 'aptum-cpq-theme';
  function initTheme() {
    const saved = localStorage.getItem(THEME_KEY);
    const preferred = matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
    applyTheme(saved || preferred);
  }
  function toggleTheme() {
    applyTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
  }
  function applyTheme(t) {
    document.documentElement.dataset.theme = t;
    localStorage.setItem(THEME_KEY, t);
    const btn  = document.getElementById('theme-btn');
    const logo = document.getElementById('main-logo');
    if (btn)  btn.textContent = t === 'dark' ? '☀' : '☽';
    if (logo) logo.src = t === 'dark'
      ? 'https://aptumlogos.pages.dev/Aptum-Logo-Horizontal-Lockup-White.png'
      : 'https://aptumlogos.pages.dev/Horizontal-Lockup-Black.png';
  }
  initTheme();
</script>
{% block extra_scripts %}{% endblock %}
</body>
</html>
```

- [ ] **Commit**

```bash
git add templates/base.html
git commit -m "feat: add base.html with shared nav and theme"
```

---

## Task 12: Update existing templates to extend `base.html`

**Files:**
- Modify: `templates/index.html`
- Modify: `templates/product.html`
- Modify: `templates/settings.html`

For each template, the transformation is:
1. Remove everything from `<!DOCTYPE html>` through `</style>` and replace with `{% extends "base.html" %} {% block extra_styles %}`
2. Close the styles block with `{% endblock %}`
3. Remove the `<header>...</header>` block (now in base.html)
4. Wrap the remaining body content in `{% block body %}<div class="page-body">...</div>{% endblock %}`
5. Move the `<script>` tags (minus theme JS) to `{% block extra_scripts %}...{% endblock %}`

- [ ] **Update `templates/index.html`**

Replace the entire file with:

```html
{% extends "base.html" %}
{% block title %}CPQ — Server Pricing · Aptum{% endblock %}

{% block extra_styles %}
    /* ── Filter bar ──────────────────────────────────────────────────────── */
    .filter-bar {
      display: flex; align-items: flex-start; gap: 1.5rem; flex-wrap: wrap;
      background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
      padding: 1.25rem 1.5rem; margin-bottom: 1.5rem;
      box-shadow: 0 2px 8px var(--shadow);
      transition: background .2s, border-color .2s;
    }
    .filter-group { display: flex; flex-direction: column; gap: .3rem; }
    .filter-group label { font-size: .63rem; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: var(--text-3); }
    .filter-hint { font-size: .65rem; height: .9rem; margin-top: .15rem; }
    .filter-group.is-primary label { color: var(--accent); }
    .filter-group.is-primary select { border-color: var(--accent); background: var(--accent-dim); color: var(--accent-text); min-width: 230px; font-weight: 500; }
    .filter-group.is-primary .filter-hint { color: var(--accent); }
    .select-wrap { position: relative; }
    select {
      appearance: none; background: var(--bg); border: 1px solid var(--border);
      color: var(--text-1); font-family: 'Geist', sans-serif; font-size: .875rem;
      padding: .5rem 2.2rem .5rem .85rem; border-radius: 8px;
      min-width: 160px; cursor: pointer; outline: none;
      transition: border-color .15s, background .2s;
    }
    select:focus { border-color: var(--accent); }
    .select-wrap::after { content:"▾"; position:absolute; right:.7rem; top:50%; transform:translateY(-50%); pointer-events:none; color:var(--text-3); font-size:.75rem; }
    #status-bar { font-size:.78rem; color:var(--text-2); margin-bottom:1rem; min-height:1.1rem; }
    .server-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem; }
    .server-card {
      background: var(--surface); border: 1px solid var(--border);
      border-left: 3px solid transparent; border-radius: 12px;
      padding: 1.25rem; cursor: pointer;
      transition: border-color .15s, border-left-color .15s, box-shadow .15s;
      text-decoration: none; display: flex; flex-direction: column; color: inherit;
    }
    .server-card:hover { border-color: var(--accent); border-left-color: var(--accent); box-shadow: 0 4px 20px rgba(125,122,232,.15); }
    .card-header { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:.5rem; gap:.5rem; }
    .card-name { font-size:.9rem; font-weight:600; color:var(--text-1); line-height:1.3; }
    .card-sku { font-family:'Geist Mono',monospace; font-size:.67rem; color:var(--accent); background:var(--accent-dim); padding:2px 6px; border-radius:4px; white-space:nowrap; flex-shrink:0; }
    .card-desc { font-size:.75rem; color:var(--text-3); line-height:1.55; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; flex:1; padding-bottom:.85rem; }
    .card-footer { display:flex; justify-content:space-between; align-items:center; padding-top:.75rem; border-top:1px solid var(--border); margin-top:auto; }
    .card-mrc { font-size:1.3rem; font-weight:700; color:var(--accent); font-family:'Geist Mono',monospace; }
    .card-mrc span { font-size:.67rem; font-weight:400; color:var(--text-3); margin-left:2px; font-family:'Geist',sans-serif; }
    .pill { display:inline-block; padding:2px 8px; border-radius:999px; font-size:.63rem; font-weight:600; text-transform:uppercase; letter-spacing:.05em; }
    .pill.soldout  { background:var(--orange-dim); color:var(--orange); }
    .pill.limited  { background:var(--accent-dim); color:var(--accent-text); }
    .pill.available{ background:var(--green-dim);  color:var(--green); }
    .empty { text-align:center; padding:4rem 1rem; color:var(--text-3); font-size:.875rem; }
    .error-pane { text-align:center; padding:3rem 1rem; }
    .error-pane p { color:var(--text-3); font-size:.875rem; margin-bottom:1rem; }
    .btn-retry { background:var(--surface); border:1px solid var(--border); color:var(--text-2); font-family:'Geist',sans-serif; font-size:.8rem; font-weight:500; padding:.45rem 1.2rem; border-radius:8px; cursor:pointer; transition:border-color .15s, color .15s; }
    .btn-retry:hover { border-color:var(--accent); color:var(--accent); }
    .spinner { display:inline-block; width:18px; height:18px; border:2px solid var(--border); border-top-color:var(--accent); border-radius:50%; animation:spin .7s linear infinite; vertical-align:middle; margin-right:6px; }
    @keyframes spin { to { transform:rotate(360deg); } }
{% endblock %}

{% block body %}
<div class="page-body">
  <div class="filter-bar">
    <div class="filter-group is-primary">
      <label for="dc-select">Data Center</label>
      <div class="select-wrap">
        <select id="dc-select"><option value="">Loading…</option></select>
      </div>
      <div class="filter-hint" id="dc-hint" style="color:var(--accent)">← Start here</div>
    </div>
    <div class="filter-group">
      <label for="product-line">Product Line</label>
      <div class="select-wrap">
        <select id="product-line">
          <option value="4">Dedicated Hosting</option>
          <option value="3">Managed Hosting</option>
        </select>
      </div>
      <div class="filter-hint"></div>
    </div>
    <div class="filter-group">
      <label for="currency-select">Currency</label>
      <div class="select-wrap">
        <select id="currency-select">
          <option value="USD">USD — US Dollar</option>
          <option value="CAD">CAD — Canadian Dollar</option>
          <option value="GBP">GBP — British Pound</option>
          <option value="EUR">EUR — Euro</option>
        </select>
      </div>
      <div class="filter-hint" id="currency-hint"></div>
    </div>
    <div class="filter-group">
      <label for="term-select">Term</label>
      <div class="select-wrap">
        <select id="term-select">
          <option value="12">12 months</option>
          <option value="24">24 months</option>
          <option value="36" selected>36 months</option>
        </select>
      </div>
      <div class="filter-hint"></div>
    </div>
  </div>
  <div id="status-bar" role="status" aria-live="polite"></div>
  <div id="server-grid" class="server-grid">
    <div class="empty">Select a data center to load available servers.</div>
  </div>
</div>
{% endblock %}

{% block extra_scripts %}
<script>
  const dcSelect       = document.getElementById('dc-select');
  const currencySelect = document.getElementById('currency-select');
  const plSelect       = document.getElementById('product-line');
  const termSelect     = document.getElementById('term-select');
  const grid           = document.getElementById('server-grid');
  const statusBar      = document.getElementById('status-bar');
  const dcHint         = document.getElementById('dc-hint');
  const currencyHint   = document.getElementById('currency-hint');
  const sym = { USD:'$', CAD:'$', GBP:'£', EUR:'€' };

  fetch('/api/datacenters')
    .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
    .then(dcs => {
      dcSelect.innerHTML = '<option value="">— select data center —</option>';
      dcs.forEach(dc => {
        const opt = document.createElement('option');
        opt.value = dc.code;
        opt.textContent = `${dc.code} — ${dc.name}`;
        dcSelect.appendChild(opt);
      });
    })
    .catch(() => { dcSelect.innerHTML = '<option value="">Failed to load — refresh</option>'; });

  dcSelect.addEventListener('change', () => {
    dcHint.textContent = dcSelect.value ? '' : '← Start here';
    dcHint.style.color = dcSelect.value ? '' : 'var(--accent)';
    currencyHint.textContent = '';
    loadServers();
  });
  currencySelect.addEventListener('change', loadServers);
  plSelect.addEventListener('change', loadServers);
  termSelect.addEventListener('change', loadServers);

  let loadToken = 0;
  function loadServers() {
    const dc = dcSelect.value, currency = currencySelect.value;
    const pl = plSelect.value, term = termSelect.value;
    if (!dc) {
      grid.innerHTML = '<div class="empty">Select a data center to load available servers.</div>';
      statusBar.textContent = '';
      return;
    }
    const token = ++loadToken;
    grid.innerHTML = '<div class="empty"><span class="spinner"></span>Loading servers…</div>';
    statusBar.textContent = '';
    fetch(`/api/servers?dc=${dc}&currency=${currency}&product_line=${pl}`)
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then(data => { if (token === loadToken) renderGrid(data, currency, dc, pl, term); })
      .catch(() => {
        if (token !== loadToken) return;
        grid.innerHTML = `<div class="error-pane"><p>Couldn't load servers.</p><button class="btn-retry" onclick="loadServers()">Try again</button></div>`;
      });
  }

  function renderGrid(servers, currency, dc, pl, term) {
    if (!Array.isArray(servers) || !servers.length || servers.error) {
      grid.innerHTML = '<div class="empty">No servers available for this selection.</div>';
      statusBar.textContent = '0 results';
      return;
    }
    const dcLabel = dcSelect.options[dcSelect.selectedIndex].text;
    const plLabel = plSelect.options[plSelect.selectedIndex].text;
    let statusText = `${servers.length} servers · ${dcLabel} · ${currency} · ${plLabel} · ${term}mo`;
    const fx = servers[0]?.fx_pricing, nc = servers[0]?.pricing_currency;
    if (fx && nc && nc !== currency && fx !== 1.0)
      statusText += ` · Converted from ${nc} @ ${fx.toFixed(4)}`;
    statusBar.textContent = statusText;
    const s = sym[currency] || '$';
    grid.innerHTML = servers.map(sv => {
      let badge = '';
      if (sv.sold_out)                  badge = '<span class="pill soldout">Sold Out</span>';
      else if (sv.limited_availability) badge = '<span class="pill limited">Limited</span>';
      else if (sv.available_in_shop)    badge = '<span class="pill available">Available</span>';
      const sku  = sv.sku ? `<span class="card-sku">${esc(sv.sku)}</span>` : '';
      const desc = (sv.description || '').substring(0, 140);
      return `
        <a class="server-card" href="/product/${sv.id}?dc=${dc}&currency=${currency}&product_line=${pl}&term=${term}">
          <div class="card-header"><div class="card-name">${esc(sv.name)}</div>${sku}</div>
          <div class="card-desc">${esc(desc)}</div>
          <div class="card-footer">
            <div class="card-mrc">${s}${sv.mrc.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2})}<span>/mo</span></div>
            ${badge}
          </div>
        </a>`;
    }).join('');
  }

  function esc(s) {
    return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }
</script>
{% endblock %}
```

- [ ] **Update `templates/settings.html`** — add `{% extends "base.html" %}` at top, wrap styles in `{% block extra_styles %}`, remove the `<header>` block, wrap body content in `{% block body %}<div class="page-body">...</div>{% endblock %}`, move scripts to `{% block extra_scripts %}`. Remove font-face, CSS token, and theme JS (all now in base.html).

- [ ] **Update `templates/product.html`** — same transformation as settings.html. Remove font-face, CSS tokens, `<header>` block, and theme JS. Wrap remaining content in appropriate blocks.

- [ ] **Start app and verify index page renders with nav**

```bash
python3 app.py &
sleep 2
curl -s http://localhost:5050/ | grep -o 'New Quotes'
```

Expected: `New Quotes`

```bash
kill %1
```

- [ ] **Commit**

```bash
git add templates/
git commit -m "refactor: all templates extend base.html with shared nav"
```

---

## Task 13: Create `templates/renewals.html`

**Files:**
- Create: `templates/renewals.html`

- [ ] **Create `templates/renewals.html`**

```html
{% extends "base.html" %}
{% block title %}CPQ — Renewals · Aptum{% endblock %}

{% block extra_styles %}
    .page-body { padding: 2rem; }
    .filter-bar {
      display:flex; align-items:flex-end; gap:1rem; flex-wrap:wrap;
      background:var(--surface); border:1px solid var(--border); border-radius:12px;
      padding:1.25rem 1.5rem; margin-bottom:1.5rem;
      box-shadow:0 2px 8px var(--shadow);
    }
    .filter-group { display:flex; flex-direction:column; gap:.3rem; min-width:180px; }
    .filter-group label { font-size:.63rem; font-weight:700; text-transform:uppercase; letter-spacing:.08em; color:var(--text-3); }
    .filter-group input {
      appearance:none; background:var(--bg); border:1px solid var(--border);
      color:var(--text-1); font-family:'Geist',sans-serif; font-size:.875rem;
      padding:.5rem .85rem; border-radius:8px; outline:none;
      transition:border-color .15s;
    }
    .filter-group input:focus { border-color:var(--accent); }
    #status-bar { font-size:.78rem; color:var(--text-2); margin-bottom:1rem; min-height:1.1rem; }
    .renewals-table { width:100%; border-collapse:collapse; }
    .renewals-table th {
      font-size:.63rem; font-weight:700; text-transform:uppercase; letter-spacing:.06em;
      color:var(--text-3); padding:.5rem .75rem; text-align:left;
      border-bottom:1px solid var(--border);
    }
    .group-row {
      background:var(--surface); cursor:pointer;
      transition:background .15s;
    }
    .group-row:hover { background:var(--surface-2); }
    .group-row td {
      padding:.75rem; font-size:.82rem; color:var(--text-1);
      border-bottom:1px solid var(--border);
    }
    .group-row td.muted { color:var(--text-2); }
    .chevron { display:inline-block; transition:transform .2s; margin-right:.5rem; color:var(--text-3); font-size:.7rem; }
    .chevron.open { transform:rotate(90deg); }
    .child-row { display:none; background:var(--surface-2); }
    .child-row.visible { display:table-row; }
    .child-row td { padding:.5rem .75rem .5rem 2.5rem; font-size:.78rem; color:var(--text-2); border-bottom:1px solid var(--border); cursor:pointer; }
    .child-row:hover td { color:var(--text-1); background:var(--border); }
    .badge {
      display:inline-block; padding:1px 7px; border-radius:999px;
      font-size:.6rem; font-weight:700; text-transform:uppercase; letter-spacing:.05em;
    }
    .badge.m2m   { background:var(--orange-dim); color:var(--orange); }
    .badge.soon  { background:var(--red-dim); color:var(--red-text); }
    .badge.mixed { background:var(--surface); color:var(--text-3); border:1px solid var(--border); }
    .mono { font-family:'Geist Mono',monospace; }
    .empty { text-align:center; padding:4rem 1rem; color:var(--text-3); font-size:.875rem; }
    .spinner { display:inline-block; width:18px; height:18px; border:2px solid var(--border); border-top-color:var(--accent); border-radius:50%; animation:spin .7s linear infinite; vertical-align:middle; margin-right:6px; }
    @keyframes spin { to { transform:rotate(360deg); } }
{% endblock %}

{% block body %}
<div class="page-body">
  <div class="filter-bar">
    <div class="filter-group">
      <label for="f-company">Company Name</label>
      <input id="f-company" type="text" placeholder="Search…" autocomplete="off" />
    </div>
    <div class="filter-group">
      <label for="f-client">Client ID</label>
      <input id="f-client" type="text" placeholder="e.g. 5634313" autocomplete="off" />
    </div>
    <div class="filter-group">
      <label for="f-service">Service ID</label>
      <input id="f-service" type="text" placeholder="e.g. 7981507" autocomplete="off" />
    </div>
  </div>
  <div id="status-bar" role="status" aria-live="polite"></div>
  <div id="table-wrap">
    <div class="empty"><span class="spinner"></span>Loading renewals…</div>
  </div>
</div>
{% endblock %}

{% block extra_scripts %}
<script>
  const sym = { USD:'$', CAD:'$', GBP:'£', EUR:'€' };

  function fmt(n, cur) {
    const s = sym[cur] || '$';
    return s + Number(n).toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2});
  }

  function esc(s) {
    return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function fmtDate(d) {
    if (!d) return '—';
    const dt = new Date(d + 'T00:00:00');
    return dt.toLocaleDateString('en-CA'); // YYYY-MM-DD
  }

  function expDisplay(group) {
    if (group.m2m)             return '<span class="badge m2m">m2m</span>';
    if (!group.expiration_date) return '—';
    const days = Math.ceil((new Date(group.expiration_date) - Date.now()) / 86400000);
    const label = fmtDate(group.expiration_date);
    if (days < 90) return `<span class="badge soon">${label}</span>`;
    return label;
  }

  let debounceTimer;
  function onFilter() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(load, 300);
  }

  document.getElementById('f-company').addEventListener('input', onFilter);
  document.getElementById('f-client').addEventListener('input', onFilter);
  document.getElementById('f-service').addEventListener('input', onFilter);

  function load() {
    const company   = document.getElementById('f-company').value.trim();
    const clientId  = document.getElementById('f-client').value.trim();
    const serviceId = document.getElementById('f-service').value.trim();
    const params = new URLSearchParams();
    if (company)   params.set('company',    company);
    if (clientId)  params.set('client_id',  clientId);
    if (serviceId) params.set('service_id', serviceId);

    document.getElementById('table-wrap').innerHTML =
      '<div class="empty"><span class="spinner"></span>Loading…</div>';

    fetch('/api/renewals?' + params)
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(render)
      .catch(() => {
        document.getElementById('table-wrap').innerHTML =
          '<div class="empty">Failed to load — try again.</div>';
      });
  }

  function render(data) {
    const groups = data.groups || [];
    const wrap = document.getElementById('table-wrap');
    document.getElementById('status-bar').textContent =
      `${data.total_services} services in ${groups.length} groups`;

    if (!groups.length) {
      wrap.innerHTML = '<div class="empty">No renewals match your filters.</div>';
      return;
    }

    let html = `
      <table class="renewals-table">
        <thead><tr>
          <th>Company</th><th>Client ID</th><th>Services</th>
          <th>DC</th><th>Product</th><th>Total MRC</th><th>Expires</th><th>Status</th>
        </tr></thead>
        <tbody>`;

    groups.forEach((g, gi) => {
      const multi   = g.service_count > 1;
      const chevron = multi
        ? `<span class="chevron" id="chv-${gi}">▶</span>`
        : '<span style="margin-right:1.25rem"></span>';
      const dcBadge = g.dc === 'Mixed'
        ? '<span class="badge mixed">Mixed</span>'
        : esc(g.dc || '—');
      const prodBadge = g.product === 'Mixed'
        ? '<span class="badge mixed">Mixed</span>'
        : esc(g.product || '—');
      const firstSvc = g.services[0];
      const cur = firstSvc?.currency || 'USD';

      html += `
        <tr class="group-row" onclick="${multi ? `toggleGroup(${gi})` : `nav(${g.services[0].service_id})`}">
          <td>${chevron}<strong>${esc(g.company_name)}</strong></td>
          <td class="muted mono">${g.client_id}</td>
          <td class="muted">${multi ? g.service_count + ' services' : (firstSvc?.nickname ? esc(firstSvc.nickname) : '1 service')}</td>
          <td>${dcBadge}</td>
          <td>${prodBadge}</td>
          <td class="mono">${fmt(g.total_mrc, cur)}<span style="font-size:.65rem;color:var(--text-3)">/mo</span></td>
          <td>${expDisplay(g)}</td>
          <td class="muted">${esc(firstSvc?.service_status || '—')}</td>
        </tr>`;

      if (multi) {
        g.services.forEach(svc => {
          html += `
            <tr class="child-row" id="child-${gi}" onclick="nav(${svc.service_id})">
              <td>${esc(svc.nickname || String(svc.service_id))}</td>
              <td class="mono">${svc.service_id}</td>
              <td>${esc(svc.service_type || '—')}</td>
              <td>${esc(svc.datacenter_code || '—')}</td>
              <td>${esc(svc.product || '—')}</td>
              <td class="mono">${fmt(svc.mrc, svc.currency || 'USD')}/mo</td>
              <td>—</td>
              <td>${esc(svc.service_status || '—')}</td>
            </tr>`;
        });
      }
    });

    html += '</tbody></table>';
    wrap.innerHTML = html;
  }

  function toggleGroup(gi) {
    const rows    = document.querySelectorAll(`#child-${gi}`);
    const chevron = document.getElementById(`chv-${gi}`);
    const open    = chevron.classList.contains('open');
    rows.forEach(r => r.classList.toggle('visible', !open));
    chevron.classList.toggle('open', !open);
  }

  function nav(serviceId) {
    window.location.href = `/renewal/${serviceId}`;
  }

  load();
</script>
{% endblock %}
```

- [ ] **Commit**

```bash
git add templates/renewals.html
git commit -m "feat: add renewals.html filterable grouped table"
```

---

## Task 14: Create `templates/renewal.html`

**Files:**
- Create: `templates/renewal.html`

- [ ] **Create `templates/renewal.html`**

```html
{% extends "base.html" %}
{% block title %}Renewal · Aptum{% endblock %}

{% block extra_styles %}
    .layout { display:grid; grid-template-columns:1fr 340px; min-height:calc(100vh - 70px); }
    .main   { padding:2rem; overflow-y:auto; border-right:1px solid var(--border); }
    .sidebar { padding:1.5rem; display:flex; flex-direction:column; gap:1.25rem; position:sticky; top:0; max-height:calc(100vh - 70px); overflow-y:auto; }

    .service-meta { margin-bottom:1.5rem; }
    .service-meta h2 { font-size:1.1rem; font-weight:700; color:var(--text-1); margin-bottom:.25rem; }
    .service-meta .sub { font-size:.78rem; color:var(--text-2); }
    .current-mrc { font-size:1.4rem; font-weight:700; color:var(--accent); font-family:'Geist Mono',monospace; margin-top:.5rem; }
    .current-mrc span { font-size:.7rem; color:var(--text-3); font-family:'Geist',sans-serif; }

    .section-title { font-size:.65rem; font-weight:700; text-transform:uppercase; letter-spacing:.08em; color:var(--text-3); margin:1.25rem 0 .5rem; }

    .comp-table { width:100%; border-collapse:collapse; margin-bottom:1rem; }
    .comp-table th { font-size:.6rem; font-weight:700; text-transform:uppercase; letter-spacing:.06em; color:var(--text-3); padding:.35rem .5rem; text-align:left; border-bottom:1px solid var(--border); }
    .comp-table td { padding:.45rem .5rem; font-size:.78rem; color:var(--text-2); border-bottom:1px solid var(--border-mid); }
    .comp-table td.name { color:var(--text-1); max-width:260px; }
    .comp-table td.mono { font-family:'Geist Mono',monospace; }
    .comp-table td.pos  { color:var(--orange); }
    .comp-table td.neg  { color:var(--green); }
    .warn-badge { display:inline-block; padding:1px 6px; border-radius:4px; font-size:.6rem; font-weight:700; background:var(--orange-dim); color:var(--orange); margin-left:.4rem; }

    .term-selector { display:flex; gap:.4rem; }
    .term-btn {
      flex:1; padding:.45rem; border-radius:8px; border:1px solid var(--border);
      background:var(--bg); color:var(--text-2); font-family:'Geist',sans-serif;
      font-size:.8rem; font-weight:500; cursor:pointer; text-align:center;
      transition:border-color .15s, background .15s, color .15s;
    }
    .term-btn:hover  { border-color:var(--accent); color:var(--accent); }
    .term-btn.active { border-color:var(--accent); background:var(--accent-dim); color:var(--accent-text); }

    .summary-table { width:100%; border-collapse:collapse; }
    .summary-table td { padding:.4rem .25rem; font-size:.82rem; }
    .summary-table td:last-child { text-align:right; font-family:'Geist Mono',monospace; color:var(--text-1); }
    .summary-table tr.sep td { border-top:1px solid var(--border); padding-top:.6rem; }
    .summary-table tr.highlight td { color:var(--accent); font-weight:700; font-size:.95rem; }
    .summary-table tr.highlight td:last-child { color:var(--accent); }
    .summary-table tr.dim td { color:var(--text-3); font-size:.75rem; }

    .copy-btn {
      width:100%; padding:.6rem; border-radius:8px;
      border:1px solid var(--accent); background:var(--accent-dim);
      color:var(--accent-text); font-family:'Geist',sans-serif;
      font-size:.85rem; font-weight:600; cursor:pointer;
      transition:background .15s;
    }
    .copy-btn:hover { background:var(--accent); color:#fff; }

    .empty { text-align:center; padding:4rem 1rem; color:var(--text-3); font-size:.875rem; }
    .spinner { display:inline-block; width:18px; height:18px; border:2px solid var(--border); border-top-color:var(--accent); border-radius:50%; animation:spin .7s linear infinite; vertical-align:middle; margin-right:6px; }
    @keyframes spin { to { transform:rotate(360deg); } }
{% endblock %}

{% block body %}
<div class="layout">
  <div class="main" id="main-content">
    <div class="empty"><span class="spinner"></span>Loading…</div>
  </div>
  <div class="sidebar" id="sidebar-content">
    <div class="empty" style="padding:2rem 0"></div>
  </div>
</div>
{% endblock %}

{% block extra_scripts %}
<script>
  const SERVICE_ID = {{ service_id }};
  const sym = { USD:'$', CAD:'$', GBP:'£', EUR:'€' };
  let DATA = null;
  let activeTerm = '36';

  function fmt(n, cur) {
    if (n === null || n === undefined) return '—';
    const s = sym[cur] || '$';
    return s + Number(n).toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2});
  }
  function esc(s) {
    return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  fetch(`/api/renewals/${SERVICE_ID}`)
    .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(data => { DATA = data; render(); })
    .catch(() => {
      document.getElementById('main-content').innerHTML =
        '<div class="empty">Failed to load service data.</div>';
    });

  function render() {
    renderMain();
    renderSidebar();
  }

  function renderMain() {
    const d = DATA;
    const svc = d.service;
    const cur = (svc.currency || 'USD').toUpperCase();

    // Group components by category
    const cats = {};
    d.components.forEach(c => {
      const cat = c.component_category || 'Other';
      if (!cats[cat]) cats[cat] = [];
      cats[cat].push(c);
    });

    let html = `
      <div class="service-meta">
        <h2>${esc(svc.company_name)} &mdash; ${svc.service_id}</h2>
        <div class="sub">
          ${esc(svc.product || '—')} &middot; ${esc(svc.datacenter_code || '—')} &middot; ${cur}
          &middot; Provisioned ${svc.provision_date ? svc.provision_date.slice(0,10) : '—'}
          ${d.hw_paid_off ? ' &middot; <span style="color:var(--green)">HW paid off</span>' : ''}
        </div>
        <div class="current-mrc">${fmt(svc.mrc, cur)}<span>/mo current</span></div>
      </div>`;

    // Base server MRC row
    html += `
      <div class="section-title">Base Server MRC</div>
      <table class="comp-table">
        <tr>
          <td class="name">${esc(svc.product || 'Server')}</td>
          <td class="mono">${fmt(d.product_mrc, cur)}/mo</td>
          <td class="mono">—</td><td></td>
        </tr>
      </table>`;

    Object.entries(cats).forEach(([cat, comps]) => {
      html += `<div class="section-title">${esc(cat)}</div>
        <table class="comp-table">
          <thead><tr>
            <th style="width:50%">Component</th>
            <th>Current MRC</th><th>New MRC</th><th>Δ</th>
          </tr></thead><tbody>`;

      comps.forEach(c => {
        const deltaClass = c.delta > 0 ? 'pos' : (c.delta < 0 ? 'neg' : '');
        const deltaStr   = c.delta !== null
          ? (c.delta > 0 ? `+${fmt(c.delta, cur)}` : fmt(c.delta, cur))
          : '—';
        const warnHtml   = c.warning
          ? `<span class="warn-badge" title="${esc(c.warning)}">⚠</span>` : '';
        html += `<tr>
          <td class="name">${esc(c.component)}${warnHtml}</td>
          <td class="mono">${c.component_mrc > 0 ? fmt(c.component_mrc, cur) + '/mo' : 'incl.'}</td>
          <td class="mono">${c.new_mrc !== null ? fmt(c.new_mrc, cur) + '/mo' : '—'}</td>
          <td class="mono ${deltaClass}">${deltaStr}</td>
        </tr>`;
      });

      html += '</tbody></table>';
    });

    document.getElementById('main-content').innerHTML = html;
  }

  function renderSidebar() {
    const d = DATA;
    const svc = d.service;
    const cur = (svc.currency || 'USD').toUpperCase();
    const p = d.pricing[activeTerm];

    const termLabels = { m2m:'m2m', '12':'12 mo', '24':'24 mo', '36':'36 mo' };
    const termBtns = Object.keys(termLabels).map(t => `
      <button class="term-btn ${t === activeTerm ? 'active' : ''}"
              onclick="setTerm('${t}')">${termLabels[t]}</button>
    `).join('');

    const upliftRow = activeTerm === 'm2m' ? `
      <tr class="dim"><td>M2M uplift</td><td>×1.25</td></tr>` : '';

    document.getElementById('sidebar-content').innerHTML = `
      <div>
        <div class="section-title" style="margin-top:0">Renewal Term</div>
        <div class="term-selector">${termBtns}</div>
      </div>
      <table class="summary-table">
        <tr><td>Current MRC</td><td>${fmt(svc.mrc, cur)}</td></tr>
        <tr><td>SW / Support Δ</td><td style="color:${p.sw_support_delta > 0 ? 'var(--orange)' : 'var(--text-1)'}">
          ${p.sw_support_delta > 0 ? '+' : ''}${fmt(p.sw_support_delta, cur)}
        </td></tr>
        ${upliftRow}
        <tr class="highlight sep"><td>Suggested MRC</td><td>${fmt(p.suggested_mrc, cur)}</td></tr>
        <tr class="sep dim"><td>HW cost/mo</td><td>${d.hw_paid_off ? '$0.00 (paid off)' : fmt(p.hw_cost_mo, cur)}</td></tr>
        <tr class="dim"><td>Overhead</td><td>${fmt(p.overhead_total, cur)}</td></tr>
        <tr class="dim"><td>Total cost</td><td>${fmt(p.total_cost, cur)}</td></tr>
        <tr class="sep"><td>Margin</td><td>${fmt(p.margin, cur)}</td></tr>
        <tr><td>Margin %</td><td>${p.margin_pct}%</td></tr>
      </table>
      <button class="copy-btn" onclick="copyQuote()">Copy Quote Summary</button>`;
  }

  function setTerm(t) {
    activeTerm = t;
    renderSidebar();
  }

  function copyQuote() {
    if (!DATA) return;
    const svc = DATA.service;
    const cur = (svc.currency || 'USD').toUpperCase();
    const p = DATA.pricing[activeTerm];
    const termLabel = { m2m:'Month-to-Month', '12':'12 months', '24':'24 months', '36':'36 months' }[activeTerm];
    const text = [
      `Renewal Quote — ${svc.company_name} (${svc.service_id})`,
      `Product: ${svc.product || '—'} · DC: ${svc.datacenter_code || '—'} · ${cur}`,
      `Term: ${termLabel}`,
      ``,
      `Current MRC:   ${fmt(svc.mrc, cur)}/mo`,
      `Suggested MRC: ${fmt(p.suggested_mrc, cur)}/mo`,
      `Margin:        ${fmt(p.margin, cur)}/mo (${p.margin_pct}%)`,
    ].join('\n');
    navigator.clipboard.writeText(text).catch(() => {});
  }
</script>
{% endblock %}
```

- [ ] **Commit**

```bash
git add templates/renewal.html
git commit -m "feat: add renewal.html detail page with term selector and margin sidebar"
```

---

## Task 15: End-to-end smoke test

- [ ] **Start the app**

```bash
python3 app.py
```

- [ ] **Open `http://localhost:5050/` — verify:**
  - Nav bar shows "New Quotes" (active), "Renewals", "Settings"
  - Server list loads when you select a DC

- [ ] **Open `http://localhost:5050/renewals` — verify:**
  - "Renewals" nav item is active
  - Table loads with renewal groups
  - Typing "YANDAV" in Company filter reduces results to that client
  - Clicking the YANDAV row navigates to `/renewal/7981507`

- [ ] **On `/renewal/7981507` — verify:**
  - Service header shows "YANDAV — 7981507", MIA, USD, provision date
  - Components are grouped by category with current/new MRC columns
  - Plesk shows $85.00 → $85.00 (or current pricebook price)
  - Any component not in pricebook shows ⚠ badge
  - Sidebar shows suggested MRC for the active term
  - Switching between m2m/12/24/36 updates the sidebar numbers
  - M2M shows ×1.25 uplift row
  - "Copy Quote Summary" copies text to clipboard

- [ ] **Verify settings page still works at `http://localhost:5050/settings`**

- [ ] **Final commit (if any fixups needed)**

```bash
git add -p  # stage only what changed
git commit -m "fix: smoke test fixups"
```
