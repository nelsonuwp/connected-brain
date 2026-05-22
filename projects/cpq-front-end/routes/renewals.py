from collections import OrderedDict

from flask import Blueprint, jsonify, render_template, request

from db.fusion import get_conn, get_dc_info
from db.mssql import (get_fx_rate, get_mssql_costs, get_mssql_watts,
                      get_renewal_services, get_service, get_service_components)
from lib.overhead import COST_DRIVERS, calc_overhead
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
    m2m_only   = request.args.get("m2m_only") == "1"
    try:
        client_id  = int(client_id)  if client_id  else None
        service_id = int(service_id) if service_id else None
    except ValueError:
        return jsonify({"error": "client_id and service_id must be integers"}), 400

    rows   = get_renewal_services(company=company, client_id=client_id, service_id=service_id, m2m_only=m2m_only)
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

    # DC info is used only for overhead FX; pricebook lookups no longer need fusion_dc_id
    # because prices are uniform across all DCs within the same currency.
    dc_info         = get_dc_info(dc_code) if dc_code else None
    native_currency = dc_info["native_currency"] if dc_info else currency

    # Pre-fetch FX rates for pricebook currency fallbacks (avoids per-component MSSQL calls).
    # Priority order when service currency not found: CAD → USD → GBP → EUR.
    _CURRENCY_PRIORITY = ["CAD", "USD", "GBP", "EUR"]
    _fx_from: dict[str, float] = {
        fc: get_fx_rate(fc, currency)
        for fc in _CURRENCY_PRIORITY
        if fc != currency
    }

    # Enrich each component with current pricebook price from Fusion.
    # No datacenter filter — prices are identical across DCs for the same currency.
    conn = get_conn()
    enriched = []
    for comp in components:
        cid     = comp.get("component_id")
        new_mrc = None
        in_pb   = False
        warning = None

        if cid:
            # Try service currency first, then fallback order
            for fc in [currency] + [c for c in _CURRENCY_PRIORITY if c != currency]:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT mrc FROM public.pricebook
                        WHERE component_id = %s AND currency = %s AND is_available = true
                        LIMIT 1
                    """, (cid, fc))
                    pb = cur.fetchone()
                if pb:
                    raw = float(pb["mrc"] or 0)
                    new_mrc = round(raw * _fx_from.get(fc, 1.0), 2)
                    in_pb   = True
                    break
            if not in_pb:
                warning = "not_in_pricebook"

        delta = round((new_mrc - comp["component_mrc"]), 2) if new_mrc is not None else None
        enriched.append({**comp, "new_mrc": new_mrc, "delta": delta,
                          "in_pricebook": in_pb, "warning": warning})

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

    # Normalize dc_code to match cost_drivers.json keys.
    # MSSQL uses "IAD2"; cost_drivers.json uses "IAD". Resolve via fusion_dc_id.
    overhead_dc = dc_code
    if dc_code not in COST_DRIVERS["data_centers"] and dc_info:
        fid = dc_info.get("id")
        for code, entry in COST_DRIVERS["data_centers"].items():
            if entry.get("fusion_dc_id") == fid:
                overhead_dc = code
                break

    # Watts for power-cost line (convert to kW)
    watts = get_mssql_watts(fusion_pid) if fusion_pid else None
    kw    = round(watts / 1000, 3) if watts else None

    # Overhead FX: native DC currency → service billing currency
    fx_overhead = get_fx_rate(native_currency, currency) if native_currency != currency else 1.0

    # SGA % for client-side overhead recalculation when user adjusts prices
    sga_pct = COST_DRIVERS["overhead_constants"].get("sga_pct", 0.0)

    # Pre-calculate all four term scenarios
    pricing = {}
    for term in ("m2m", "12", "24", "36"):
        term_months_val = {"m2m": 1, "12": 12, "24": 24, "36": 36}[term]
        suggested       = calc_suggested_mrc(product_mrc, enriched, term)
        hw_cost_mo      = 0.0 if paid_off else round(hw_capex_display / term_months_val, 2)
        overhead_lines  = calc_overhead(overhead_dc, suggested, fx_rate=fx_overhead, kw=kw)
        overhead_amounts = {k: (v["amount"] or 0) for k, v in overhead_lines.items()}
        overhead_total  = round(sum(overhead_amounts.values()), 2)
        total_cost = round(hw_cost_mo + overhead_total, 2)
        margin     = round(suggested - total_cost, 2)
        margin_pct = round(margin / suggested * 100, 1) if suggested > 0 else 0.0

        pricing[term] = {
            "suggested_mrc":  suggested,
            "hw_cost_mo":     hw_cost_mo,
            "overhead_lines": overhead_amounts,
            "overhead_total": overhead_total,
            "total_cost":     total_cost,
            "margin":         margin,
            "margin_pct":     margin_pct,
        }

    return jsonify({
        "service":              service,
        "components":           enriched,
        "product_mrc":          product_mrc,
        "hw_capex":             hw_capex_display,
        "hw_capex_currency":    hw_capex_currency,
        "hw_paid_off":          paid_off,
        "provision_age_months": age_months,
        "pricing":              pricing,
        "sga_pct":              sga_pct,
        "kw":                   kw,
    })
