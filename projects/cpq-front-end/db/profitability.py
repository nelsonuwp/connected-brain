import logging
from datetime import date, datetime as _dt

from db.fusion import get_dc_info
from db.mssql import _connect, get_fx_rate, get_mssql_costs, get_mssql_watts_batch, _configured
from lib.overhead import COST_DRIVERS, calc_overhead
from lib.renewal_pricing import hw_paid_off, provision_age_months
from db.jsm import get_support_hours_batch


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
    service_type: str = "server",
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
    overhead_lines = calc_overhead(overhead_dc, mrc, fx_rate=fx_overhead, kw=kw, service_type=service_type)

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
    company_names: list[str] | None = None,
    client_ids: list[int] | None = None,
) -> list[dict]:
    """Fetch all active services from dimServices + dimClientsActive."""
    if not _configured():
        return []
    conn = cur = None
    try:
        conn = _connect()
        cur = conn.cursor(as_dict=True)

        conditions = ["ds.service_status = 'Online'"]
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
            conditions.append("ds.company_name LIKE %s")
            params.append(f"%{company_search}%")
        if company_names:
            placeholders = ",".join(["%s"] * len(company_names))
            conditions.append(f"ds.company_name IN ({placeholders})")
            params.extend(company_names)
        if client_ids:
            placeholders = ",".join(["%d"] * len(client_ids))
            conditions.append(f"ds.client_id IN ({placeholders})")
            params.extend(int(c) for c in client_ids)

        where = " AND ".join(conditions)
        sql = f"""
            SELECT
                ds.service_id, ds.client_id, ds.datacenter_code,
                ds.currency, ds.mrc, ds.provision_date,
                ds.service_type, ds.fusion_id, ds.nickname,
                ds.product, ds.service_status,
                ds.company_name,
                dca.account_manager
            FROM DM_BusinessInsights.dbo.dimServices ds
            LEFT JOIN DM_BusinessInsights.dbo.dimClientsActive dca
                ON dca.client_id = ds.client_id
            WHERE {where}
            ORDER BY ds.company_name, ds.service_id
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
            WHERE datacenter_code IS NOT NULL AND service_status = 'Online'
            ORDER BY datacenter_code
        """)
        dcs = [r[0] for r in cur.fetchall() if r[0]]

        cur.execute("""
            SELECT DISTINCT TOP 200 service_type AS val
            FROM DM_BusinessInsights.dbo.dimServices
            WHERE service_type IS NOT NULL AND service_status = 'Online'
            ORDER BY service_type
        """)
        types = [r[0] for r in cur.fetchall() if r[0]]

        cur.execute("""
            SELECT DISTINCT TOP 500 ds.company_name AS val
            FROM DM_BusinessInsights.dbo.dimServices ds
            WHERE ds.service_status = 'Online'
              AND ds.company_name IS NOT NULL AND ds.company_name != ''
            ORDER BY ds.company_name
        """)
        companies = [r[0].strip() for r in cur.fetchall() if r[0]]

        return {"account_managers": ams, "dc_codes": dcs, "service_types": types, "company_names": companies}
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


def _is_cloud_service(service: dict) -> bool:
    return (service.get("service_type") or "").strip() == "Public Cloud"


def build_profitability_data(services: list[dict], progress_cb=None) -> list[dict]:
    """Enrich each service dict with its cost breakdown and margin.

    Physical services: batched MSSQL HW cost + watts + calc_service_margin.
    Cloud (Public Cloud) services: Azure billing DB via SSH tunnel.
    progress_cb(msg, source) is called at key stages for streaming status.
    """
    def _progress(msg, source=None):
        if progress_cb:
            progress_cb(msg, source)

    if not services:
        return []

    physical = [s for s in services if not _is_cloud_service(s)]
    cloud    = [s for s in services if _is_cloud_service(s)]

    result_map: dict[int, dict] = {}

    # ── Physical services ──────────────────────────────────────────────────────
    fusion_ids  = [s["fusion_id"] for s in physical if s.get("fusion_id")]
    service_ids = [s["service_id"] for s in physical if s.get("service_id")]

    _progress(f"Loading hardware costs for {len(fusion_ids)} services…", "MSSQL · ocean_sku_cost")
    hw_costs   = get_mssql_costs(fusion_ids, "TLS") if fusion_ids else {}
    _progress(f"Hardware costs found for {len(hw_costs)} of {len(fusion_ids)} services", None)

    _progress(f"Loading power consumption data…", "MSSQL · hardware_watts")
    watts_map  = get_mssql_watts_batch(fusion_ids) if fusion_ids else {}
    _progress(f"Power data found for {sum(1 for v in watts_map.values() if v)} services", None)

    _progress(f"Loading JSM support hours…", "PostgreSQL · jsm_sync")
    jsm_hours = get_support_hours_batch(service_ids) if service_ids else {}
    _progress(f"Support hours found for {len(jsm_hours)} of {len(service_ids)} services", None)

    fx_cache: dict[tuple[str, str], float] = {}

    def get_fx(from_c: str, to_c: str) -> float:
        if from_c == to_c:
            return 1.0
        key = (from_c, to_c)
        if key not in fx_cache:
            fx_cache[key] = get_fx_rate(from_c, to_c)
        return fx_cache[key]

    for service in physical:
        fid      = service.get("fusion_id")
        currency = (service.get("currency") or "USD").upper()
        dc_code  = (service.get("datacenter_code") or "").upper()

        dc_info         = get_dc_info(dc_code) if dc_code else None
        native_currency = dc_info["native_currency"] if dc_info else currency

        hw_capex_in_currency = 0.0
        if fid and fid in hw_costs:
            hw = hw_costs[fid]
            hw_capex_in_currency = round(hw["cost"] * get_fx(hw["currency"], currency), 2)

        fx_overhead = get_fx(native_currency, currency)
        watts       = watts_map.get(fid) if fid else None
        mrc         = float(service.get("mrc") or 0)
        svc_type    = (service.get("service_type") or "server").strip()

        margin_data = calc_service_margin(
            mrc=mrc,
            dc_code=dc_code,
            hw_capex_in_currency=hw_capex_in_currency,
            watts=watts,
            fx_overhead=fx_overhead,
            provision_date=service.get("provision_date"),
            service_type=svc_type,
        )

        # Override support_ops with actual JSM hours if available
        sid = service["service_id"]
        jsm_h = jsm_hours.get(sid)
        support_ops_hours = None
        if jsm_h is not None and "support_ops" in (margin_data.get("overhead") or {}):
            rate_cad = COST_DRIVERS["overhead_constants"].get("service_desk_rate_cad", 0) or 0
            fx_cad = get_fx("CAD", currency) if currency != "CAD" else 1.0
            actual_support_cost = round(jsm_h * rate_cad * fx_cad, 2)
            old_support_cost = margin_data["overhead"].get("support_ops") or 0
            margin_data["overhead"]["support_ops"] = actual_support_cost
            delta = actual_support_cost - old_support_cost
            margin_data["total_cost"] = round(margin_data["total_cost"] + delta, 2)
            margin_data["margin"]     = round(margin_data["margin"] - delta, 2)
            margin_data["margin_pct"] = round(margin_data["margin"] / mrc * 100, 1) if mrc > 0 else 0.0
            support_ops_hours = round(jsm_h, 2)

        missing: list[str] = []
        if not fid:
            missing.append("No Fusion ID — HW cost and power data unavailable")
        else:
            if fid not in hw_costs:
                missing.append("Hardware cost data not found")
            if watts is None:
                missing.append("Power consumption data missing")
        if service.get("provision_date") is None:
            missing.append("Provision date unknown")
        if not margin_data.get("overhead"):
            missing.append("Overhead rates unavailable for this DC")

        result_map[service["service_id"]] = {
            **service, **margin_data,
            "is_cloud": False,
            "support_ops_hours": support_ops_hours,
            "missing_data": missing,
        }

    _progress(f"Computing margins for {len(physical)} physical services…", None)

    # ── Cloud (Public Cloud) services ──────────────────────────────────────────
    if cloud:
        cloud_client_ids = list({s["client_id"] for s in cloud})
        _progress(
            f"Fetching Azure billing for {len(cloud_client_ids)} cloud customers…",
            "PostgreSQL · azurebilling (SSH tunnel)",
        )
        billing_batch: dict[int, dict] = {}
        try:
            from db.azure_billing import get_cloud_billing_batch
            billing_batch = get_cloud_billing_batch(cloud_client_ids)
            _progress(
                f"Azure billing data received for {len(billing_batch)} of {len(cloud_client_ids)} customers",
                None,
            )
        except Exception:
            logging.exception("build_profitability_data: azure billing fetch failed")
            _progress("Azure billing unavailable — cloud costs will be missing", None)

        # Per-client: first cloud service carries consumption; subsequent carry only their MRC.
        seen_cloud_clients: set[int] = set()
        for service in cloud:
            client_id = service["client_id"]
            mrc_base  = float(service.get("mrc") or 0)
            billing   = billing_batch.get(client_id, {})
            is_first  = client_id not in seen_cloud_clients
            seen_cloud_clients.add(client_id)

            if is_first and billing:
                cons_revenue = billing.get("consumption_revenue", 0.0)
                cons_cost    = billing.get("consumption_cost", 0.0)
                # Prefer management fee from billing DB over dimServices MRC when billing
                # has data — dimServices MRC is often $0 for cloud services even though
                # a real management fee is billed (product codes 5799/5801/5803).
                mgmt_fee  = billing.get("management_fee_revenue", 0.0)
                total_mrc = (mgmt_fee if mgmt_fee > 0 else mrc_base) + cons_revenue
                total_cost   = cons_cost
                missing      = []
            else:
                cons_revenue = 0.0
                cons_cost    = 0.0
                total_mrc    = mrc_base
                total_cost   = 0.0
                missing      = [] if billing or not is_first else ["Azure billing data unavailable"]

            margin     = round(total_mrc - total_cost, 2)
            margin_pct = round(margin / total_mrc * 100, 1) if total_mrc > 0 else 0.0

            result_map[service["service_id"]] = {
                **service,
                "is_cloud":             True,
                "hw_amortized":         0.0,
                "overhead":             {},
                "sga":                  0.0,
                "mrc":                  total_mrc,
                "total_cost":           total_cost,
                "margin":               margin,
                "margin_pct":           margin_pct,
                "hw_paid_off":          None,
                "hw_months_remaining":  None,
                "biggest_cost_driver":  "azure_consumption" if cons_cost > 0 else None,
                "consumption_revenue":  cons_revenue,
                "consumption_cost":     cons_cost,
                "billing_period_label": billing.get("billing_period_label", ""),
                "missing_data":         missing,
            }

    # Preserve original order
    order = {s["service_id"]: i for i, s in enumerate(services)}
    return sorted(result_map.values(), key=lambda s: order.get(s["service_id"], 999999))
