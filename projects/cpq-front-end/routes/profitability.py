import json
import queue as _queue
import threading

from flask import Blueprint, Response, jsonify, render_template, request, stream_with_context

from db.profitability import (build_profitability_data, get_active_services,
                              get_profitability_filter_options)
from db.mssql import get_fx_rate
from db.jsm import get_support_hours_by_month
from lib.overhead import COST_DRIVERS

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
    company_names    = request.args.getlist("company") or None
    display_currency = request.args.get("display_currency", "").strip().upper() or None

    services = get_active_services(
        account_managers=account_managers,
        dc_codes=dc_codes,
        service_types=service_types,
        company_names=company_names,
    )
    enriched = build_profitability_data(services)

    # Auto-convert to CAD when currencies are mixed and no explicit display currency
    auto_currency = None
    effective_currency = display_currency
    if not effective_currency:
        currencies = {(s.get("currency") or "USD").upper() for s in enriched}
        if len(currencies) > 1:
            effective_currency = "CAD"
            auto_currency = "CAD"

    if effective_currency:
        fx_cache: dict[tuple, float] = {}
        converted = []
        for svc in enriched:
            svc_currency = (svc.get("currency") or "USD").upper()
            key = (svc_currency, effective_currency)
            if key not in fx_cache:
                fx_cache[key] = get_fx_rate(svc_currency, effective_currency) if svc_currency != effective_currency else 1.0
            fx = fx_cache[key]
            converted.append({
                **svc,
                "mrc":        round(svc["mrc"] * fx, 2),
                "total_cost": round(svc["total_cost"] * fx, 2),
                "margin":     round(svc["margin"] * fx, 2),
                "currency":   effective_currency,
            })
        enriched = converted

    by_customer     = _aggregate_by_customer(enriched, effective_currency)
    by_dc           = _aggregate_by_field(enriched, "datacenter_code", effective_currency)
    by_service_type = _aggregate_by_field(enriched, "service_type", effective_currency)
    totals          = _compute_totals(enriched, effective_currency)

    return jsonify({
        "by_customer":     by_customer,
        "by_dc":           by_dc,
        "by_service_type": by_service_type,
        "totals":          totals,
        "auto_currency":   auto_currency,
    })


@profitability_bp.route("/api/profitability/<int:client_id>")
def api_profitability_customer(client_id):
    display_currency = request.args.get("display_currency", "").strip().upper() or None

    services = get_active_services(client_ids=[client_id])

    if not services:
        return jsonify({"error": "Customer not found or has no active services"}), 404

    enriched = build_profitability_data(services)

    # Auto-convert to CAD when currencies are mixed and no explicit display currency
    auto_currency = None
    effective_currency = display_currency
    if not effective_currency:
        currencies = {(s.get("currency") or "USD").upper() for s in enriched}
        if len(currencies) > 1:
            effective_currency = "CAD"
            auto_currency = "CAD"

    if effective_currency:
        fx_cache: dict[tuple, float] = {}
        converted = []
        for svc in enriched:
            svc_currency = (svc.get("currency") or "USD").upper()
            key = (svc_currency, effective_currency)
            if key not in fx_cache:
                fx_cache[key] = get_fx_rate(svc_currency, effective_currency) if svc_currency != effective_currency else 1.0
            fx = fx_cache[key]
            entry = {
                **svc,
                "mrc":        round(svc["mrc"] * fx, 2),
                "total_cost": round(svc["total_cost"] * fx, 2),
                "margin":     round(svc["margin"] * fx, 2),
                "currency":   effective_currency,
            }
            if not svc.get("is_cloud"):
                entry["hw_amortized"] = round(svc["hw_amortized"] * fx, 2)
                entry["sga"]          = round(svc["sga"] * fx, 2)
                entry["overhead"]     = {k: round(v * fx, 2) for k, v in svc["overhead"].items()}
            else:
                entry["consumption_revenue"] = round(svc.get("consumption_revenue", 0) * fx, 2)
                entry["consumption_cost"]    = round(svc.get("consumption_cost", 0) * fx, 2)
            converted.append(entry)
        enriched = converted

    summary = _compute_totals(enriched, effective_currency)
    info = services[0]
    summary["company_name"]    = info.get("company_name") or ""
    summary["account_manager"] = info.get("account_manager") or ""
    summary["client_id"]       = client_id
    summary["auto_currency"]   = auto_currency

    # Rolling 3-month support cost for the summary card
    phys_ids = [s["service_id"] for s in services if not (s.get("service_type") or "").strip() == "Public Cloud"]
    monthly_hours = get_support_hours_by_month(phys_ids, months=3) if phys_ids else []
    if monthly_hours:
        rate_cad = COST_DRIVERS["overhead_constants"].get("service_desk_rate_cad", 0) or 0
        disp_cur = effective_currency or "USD"
        fx_cad = get_fx_rate("CAD", disp_cur) if disp_cur != "CAD" else 1.0
        support_monthly = [
            {"period": m["period"], "hours": round(m["hours"], 2),
             "cost": round(m["hours"] * rate_cad * fx_cad, 2)}
            for m in monthly_hours
        ]
        avg_cost  = round(sum(m["cost"]  for m in support_monthly) / len(support_monthly), 2)
        avg_hours = round(sum(m["hours"] for m in support_monthly) / len(support_monthly), 2)
        summary["support_cost_monthly"] = {
            "months": support_monthly,
            "avg_cost": avg_cost,
            "avg_hours": avg_hours,
            "currency": disp_cur,
        }
    else:
        summary["support_cost_monthly"] = None

    serialized = []
    for svc in enriched:
        s = dict(svc)
        if hasattr(s.get("provision_date"), "isoformat"):
            s["provision_date"] = s["provision_date"].isoformat()
        serialized.append(s)

    # Attach Azure billing detail for cloud customers
    cloud_detail = {}
    has_cloud = any(s.get("is_cloud") for s in enriched)
    if has_cloud:
        try:
            from db.azure_billing import get_cloud_billing_detail
            cloud_detail = get_cloud_billing_detail(client_id)
        except Exception:
            pass

    return jsonify({"services": serialized, "summary": summary, "cloud_detail": cloud_detail})


# ── SSE streaming endpoint ───────────────────────────────────────────────────

@profitability_bp.route("/api/profitability/stream")
def api_profitability_stream():
    """Server-Sent Events version of /api/profitability.
    Streams progress messages then a final 'done' event with the full result.
    """
    account_managers = request.args.getlist("am") or None
    dc_codes         = request.args.getlist("dc") or None
    service_types    = request.args.getlist("service_type") or None
    company_names    = request.args.getlist("company") or None
    display_currency = request.args.get("display_currency", "").strip().upper() or None

    q = _queue.Queue()
    result_box: dict = {}

    def worker():
        try:
            q.put({"msg": "Fetching active services…", "src": "MSSQL · DM_BusinessInsights"})
            services = get_active_services(
                account_managers=account_managers,
                dc_codes=dc_codes,
                service_types=service_types,
                company_names=company_names,
            )
            n_cloud = sum(1 for s in services if (s.get("service_type") or "") == "Public Cloud")
            n_phys  = len(services) - n_cloud
            n_cust  = len({s["client_id"] for s in services})
            q.put({"msg": f"Found {len(services)} services ({n_phys} physical, {n_cloud} cloud) across {n_cust} customers", "src": ""})

            def cb(msg, src=None):
                q.put({"msg": msg, "src": src or ""})

            enriched = build_profitability_data(services, progress_cb=cb)

            q.put({"msg": "Computing aggregations…", "src": ""})

            auto_currency = None
            effective_currency = display_currency
            if not effective_currency:
                currencies = {(s.get("currency") or "USD").upper() for s in enriched}
                if len(currencies) > 1:
                    effective_currency = "CAD"
                    auto_currency = "CAD"

            if effective_currency:
                fx_cache: dict[tuple, float] = {}
                converted = []
                for svc in enriched:
                    svc_currency = (svc.get("currency") or "USD").upper()
                    key = (svc_currency, effective_currency)
                    if key not in fx_cache:
                        fx_cache[key] = get_fx_rate(svc_currency, effective_currency) if svc_currency != effective_currency else 1.0
                    fx = fx_cache[key]
                    entry = {**svc, "mrc": round(svc["mrc"] * fx, 2),
                             "total_cost": round(svc["total_cost"] * fx, 2),
                             "margin": round(svc["margin"] * fx, 2),
                             "currency": effective_currency}
                    if not svc.get("is_cloud"):
                        entry["hw_amortized"] = round(svc["hw_amortized"] * fx, 2)
                        entry["sga"]          = round(svc["sga"] * fx, 2)
                        entry["overhead"]     = {k: round(v * fx, 2) for k, v in svc["overhead"].items()}
                    else:
                        entry["consumption_revenue"] = round(svc.get("consumption_revenue", 0) * fx, 2)
                        entry["consumption_cost"]    = round(svc.get("consumption_cost", 0) * fx, 2)
                    converted.append(entry)
                enriched = converted

            result_box["data"] = {
                "by_customer":     _aggregate_by_customer(enriched, effective_currency),
                "by_dc":           _aggregate_by_field(enriched, "datacenter_code", effective_currency),
                "by_service_type": _aggregate_by_field(enriched, "service_type", effective_currency),
                "totals":          _compute_totals(enriched, effective_currency),
                "auto_currency":   auto_currency,
            }
        except Exception as e:
            result_box["error"] = str(e)
        finally:
            q.put(None)

    threading.Thread(target=worker, daemon=True).start()

    def generate():
        while True:
            item = q.get()
            if item is None:
                break
            yield f"data: {json.dumps(item)}\n\n"
        if "error" in result_box:
            yield f"data: {json.dumps({'done': True, 'error': result_box['error']})}\n\n"
        else:
            yield f"data: {json.dumps({'done': True, 'result': result_box['data']})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── Aggregation helpers ───────────────────────────────────────────────────────

def _support_trend(curr: float, prev: float) -> str:
    """5-level trend: more hours = more cost = bad direction."""
    if prev == 0:
        return "up" if curr > 0 else "flat"
    pct = (curr - prev) / prev * 100
    if pct > 50:    return "up"
    if pct > 10:    return "slight-up"
    if pct >= -10:  return "flat"
    if pct >= -50:  return "slight-down"
    return "down"

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
                "mrc":             0.0,
                "total_cost":      0.0,
                "margin":          0.0,
                "support_hours":        0.0,
                "support_hours_prev":   0.0,
                "support_hours_prev2":  0.0,
                "support_hours_periods": None,
                "support_hours_available": False,
                "warnings":        set(),
            }
        g = groups[cid]
        g["service_count"] += 1
        g["currencies"].add((svc.get("currency") or "USD").upper())
        g["mrc"]        += svc["mrc"]
        g["total_cost"] += svc["total_cost"]
        g["margin"]     += svc["margin"]
        h = svc.get("support_ops_hours")
        if h is not None:
            g["support_hours"]       += h
            g["support_hours_prev"]  += svc.get("support_ops_hours_prev")  or 0.0
            g["support_hours_prev2"] += svc.get("support_ops_hours_prev2") or 0.0
            g["support_hours_available"] = True
            if g["support_hours_periods"] is None:
                g["support_hours_periods"] = svc.get("support_ops_periods")
        for w in (svc.get("missing_data") or []):
            g["warnings"].add(w)

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
            "mrc":             mrc,
            "total_cost":      cost,
            "margin":          margin,
            "margin_pct":      mpct,
            "support_hours":        round(g["support_hours"], 2) if g["support_hours_available"] else None,
            "support_hours_prev":   round(g["support_hours_prev"], 2) if g["support_hours_available"] else None,
            "support_hours_trend":  _support_trend(g["support_hours"], g["support_hours_prev"]) if g["support_hours_available"] else None,
            "support_hours_months": (
                [
                    {"period": p, "hours": h}
                    for p, h in zip(
                        g["support_hours_periods"] or ["", "", ""],
                        [round(g["support_hours_prev2"], 2), round(g["support_hours_prev"], 2), round(g["support_hours"], 2)],
                    )
                ] if g["support_hours_available"] and g["support_hours_periods"] else None
            ),
            "warnings":            sorted(g["warnings"]),
        })
    result.sort(key=lambda x: (x["margin_pct"] is None, x["margin_pct"] or 0))
    return result


def _aggregate_by_field(enriched: list[dict], field: str, display_currency: str | None) -> list[dict]:
    groups: dict[str, dict] = {}
    for svc in enriched:
        key = (svc.get(field) or "Unknown").strip()
        if key not in groups:
            groups[key] = {"label": key, "service_count": 0, "currencies": set(),
                           "mrc": 0.0, "total_cost": 0.0, "margin": 0.0, "warnings": set()}
        g = groups[key]
        g["service_count"] += 1
        g["currencies"].add((svc.get("currency") or "USD").upper())
        g["mrc"]        += svc["mrc"]
        g["total_cost"] += svc["total_cost"]
        g["margin"]     += svc["margin"]
        for w in (svc.get("missing_data") or []):
            g["warnings"].add(w)

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
            "warnings":   sorted(g["warnings"]),
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
