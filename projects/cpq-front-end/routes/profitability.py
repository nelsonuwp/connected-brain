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

    by_customer     = _aggregate_by_customer(enriched, display_currency)
    by_dc           = _aggregate_by_field(enriched, "datacenter_code", display_currency)
    by_service_type = _aggregate_by_field(enriched, "service_type", display_currency)
    totals          = _compute_totals(enriched, display_currency)

    return jsonify({
        "by_customer":     by_customer,
        "by_dc":           by_dc,
        "by_service_type": by_service_type,
        "totals":          totals,
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
                "mrc":          round(svc["mrc"] * fx, 2),
                "total_cost":   round(svc["total_cost"] * fx, 2),
                "margin":       round(svc["margin"] * fx, 2),
                "hw_amortized": round(svc["hw_amortized"] * fx, 2),
                "sga":          round(svc["sga"] * fx, 2),
                "overhead":     {k: round(v * fx, 2) for k, v in svc["overhead"].items()},
                "currency":     display_currency,
            })
        enriched = converted

    summary = _compute_totals(enriched, display_currency)
    info = services[0]
    summary["company_name"]    = info.get("company_name") or ""
    summary["account_manager"] = info.get("account_manager") or ""
    summary["client_id"]       = client_id

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
        mixed  = len(g["currencies"]) > 1 and not display_currency
        mrc    = round(g["mrc"], 2)        if not mixed else None
        cost   = round(g["total_cost"], 2) if not mixed else None
        margin = round(g["margin"], 2)     if not mixed else None
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
        mixed  = len(g["currencies"]) > 1 and not display_currency
        mrc    = round(g["mrc"], 2)        if not mixed else None
        cost   = round(g["total_cost"], 2) if not mixed else None
        margin = round(g["margin"], 2)     if not mixed else None
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

    currencies   = {(s.get("currency") or "USD").upper() for s in enriched}
    mixed        = len(currencies) > 1 and not display_currency
    customer_ids = {s["client_id"] for s in enriched}
    at_risk      = sum(1 for s in enriched if (s.get("margin_pct") or 0) < 10)

    if mixed:
        return {
            "service_count": len(enriched), "customer_count": len(customer_ids),
            "at_risk_count": at_risk, "currency": "mixed", "currency_mixed": True,
            "mrc": None, "total_cost": None, "margin": None, "margin_pct": None,
        }

    mrc    = round(sum(s["mrc"] for s in enriched), 2)
    cost   = round(sum(s["total_cost"] for s in enriched), 2)
    margin = round(sum(s["margin"] for s in enriched), 2)
    mpct   = round(margin / mrc * 100, 1) if mrc > 0 else 0.0
    return {
        "service_count": len(enriched), "customer_count": len(customer_ids),
        "at_risk_count": at_risk,
        "currency":      display_currency or list(currencies)[0],
        "currency_mixed": False,
        "mrc": mrc, "total_cost": cost, "margin": margin, "margin_pct": mpct,
    }
