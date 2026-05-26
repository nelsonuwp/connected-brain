import logging
from datetime import date, datetime as _dt

from db.fusion import get_dc_info
from db.mssql import _connect, get_fx_rate, get_mssql_costs, get_mssql_watts_batch, _configured
from lib.overhead import COST_DRIVERS, calc_overhead
from lib.renewal_pricing import hw_paid_off, provision_age_months


def _parse_date(value) -> date | None:
    if value is None:
        return None
    if isinstance(value, _dt):
        return value.date() if value.year > 1900 else None
    if isinstance(value, date):
        return value if value.year > 1900 else None
    if isinstance(value, str):
        s = value[:10]
        if s <= "1900-01-01":
            return None
        try:
            return date.fromisoformat(s)
        except ValueError:
            return None
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

    kw = round(watts / 1000, 3) if watts is not None else None
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

    # If calc_overhead returned nothing (unknown DC), still apply SGA from constants
    if not overhead_lines:
        sga_pct = COST_DRIVERS["overhead_constants"]["sga_pct"]
        sga = round(mrc * sga_pct, 2) if mrc else 0.0

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
    conn = cur = None
    try:
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
        logging.exception("get_active_services: db error")
        return []
    finally:
        if cur:
            try: cur.close()
            except Exception: pass
        if conn:
            try: conn.close()
            except Exception: pass


def get_profitability_filter_options() -> dict:
    """Distinct values for filter dropdowns."""
    if not _configured():
        return {"account_managers": [], "dc_codes": [], "service_types": []}
    conn = cur = None
    try:
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

        return {"account_managers": ams, "dc_codes": dcs, "service_types": types}
    except Exception:
        logging.exception("get_profitability_filter_options: db error")
        return {"account_managers": [], "dc_codes": [], "service_types": []}
    finally:
        if cur:
            try: cur.close()
            except Exception: pass
        if conn:
            try: conn.close()
            except Exception: pass


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
