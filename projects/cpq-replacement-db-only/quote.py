"""
quote.py — CPQ quote calculator (Supabase)
------------------------------------------
Builds a quote from: server SKU + addon components, currency, DC, term.
Returns: totals (MRC, NRC), line items (server + each addon), capex, overhead breakdown.

Component pricing is stored in USD; for CAD/GBP quotes we convert using latest spot fx_rates.

Usage (programmatic):
    from quote import build_quote
    result = build_quote(client, server_sku="Pro Series 6.0 - M", ...)

Usage (CLI):
    python quote.py "Pro Series 6.0 - M" --currency CAD --dc TOR --term 12
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any, Optional
import math

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

AddonLine = dict  # {"sku": str, "quantity": int}


def _decimal(n: Any) -> Decimal:
    if n is None:
        return Decimal("0")
    return Decimal(str(n))


def _round2(d: Decimal) -> Decimal:
    return d.quantize(Decimal("0.01"))


# ---------------------------------------------------------------------------
# Lookups
# ---------------------------------------------------------------------------


def _get_product_id(client, sku: str) -> Optional[int]:
    resp = client.table("product_catalog").select("id").eq("sku_name", sku).limit(1).execute()
    if not resp.data:
        return None
    return resp.data[0]["id"]


def _get_server_pricing(client, product_id: int, currency: str, term_months: int) -> tuple[Decimal, Decimal]:
    resp = (
        client.table("product_pricing")
        .select("mrc, nrc")
        .eq("product_id", product_id)
        .eq("currency_code", currency)
        .eq("term_months", term_months)
        .limit(1)
        .execute()
    )
    if not resp.data:
        return Decimal("0"), Decimal("0")
    r = resp.data[0]
    return _decimal(r.get("mrc")), _decimal(r.get("nrc"))


def _get_component_pricing(client, product_id: int, term_months: int, currency: str = "USD") -> tuple[Decimal, Decimal]:
    # Components are seeded in USD only; try requested currency first, then USD
    for try_curr in (currency, "USD"):
        resp = (
            client.table("product_pricing")
            .select("mrc, nrc")
            .eq("product_id", product_id)
            .eq("currency_code", try_curr)
            .eq("term_months", term_months)
            .limit(1)
            .execute()
        )
        if resp.data:
            r = resp.data[0]
            return _decimal(r.get("mrc")), _decimal(r.get("nrc"))
    return Decimal("0"), Decimal("0")


def _get_spot_rate(client, from_currency: str, as_of: date) -> Optional[Decimal]:
    if from_currency == "CAD":
        return Decimal("1")
    resp = (
        client.table("fx_rates")
        .select("rate")
        .eq("currency_code", from_currency)
        .eq("rate_type", "spot")
        .lte("rate_date", as_of.isoformat())
        .order("rate_date", desc=True)
        .limit(1)
        .execute()
    )
    if not resp.data:
        return None
    return _decimal(resp.data[0]["rate"])


def _get_default_component_ids(client, server_product_id: int) -> set[int]:
    resp = (
        client.table("server_default_components")
        .select("component_product_id")
        .eq("server_product_id", server_product_id)
        .execute()
    )
    return {r["component_product_id"] for r in resp.data}


def _get_capex(client, product_id: int, currency: str = "USD") -> Optional[dict]:
    resp = (
        client.table("product_capex")
        .select("procured_price, procured_currency")
        .eq("product_id", product_id)
        .eq("use_as_baseline", True)
        .order("procured_date", desc=True)
        .limit(1)
        .execute()
    )
    if not resp.data:
        return None
    r = resp.data[0]
    return {"amount": _decimal(r["procured_price"]), "currency": r["procured_currency"]}


def _get_server_watts(client, server_product_id: int) -> Optional[int]:
    """Server nameplate watts from server_specs (per CPQ sheet). Used for power costing when set."""
    resp = client.table("server_specs").select("watts").eq("product_id", server_product_id).limit(1).execute()
    if not resp.data or resp.data[0].get("watts") is None:
        return None
    return int(resp.data[0]["watts"]) or None


def _get_component_watts(client, product_id: int) -> int:
    resp = client.table("component_specs").select("watts").eq("product_id", product_id).limit(1).execute()
    if not resp.data or resp.data[0].get("watts") is None:
        return 0
    return int(resp.data[0]["watts"]) or 0


def _get_pricing_rule(client, product_id: int) -> Optional[dict]:
    """Fetch pricing rule for a product. Returns None if product uses flat pricing."""
    resp = (
        client.table("pricing_rules")
        .select("cost_driver, min_units_per_socket, min_units_per_server, unit_increment, mrc_represents")
        .eq("product_id", product_id)
        .limit(1)
        .execute()
    )
    if not resp.data:
        return None
    return resp.data[0]


def _get_server_cpu_config(client, server_product_id: int) -> dict:
    """Resolve cores-per-socket and socket count for a server's CPU config.

    Returns {"cores_per_socket": int, "num_sockets": int, "total_physical_cores": int}.
    Uses server_default_components to find the default CPU, then component_specs for cores.
    Falls back to server_specs.default_cpu_qty / processor_sockets for socket count.
    """
    ss_resp = (
        client.table("server_specs")
        .select("default_cpu_qty, processor_sockets")
        .eq("product_id", server_product_id)
        .limit(1)
        .execute()
    )
    num_sockets = 1
    if ss_resp.data:
        num_sockets = (
            ss_resp.data[0].get("processor_sockets")
            or ss_resp.data[0].get("default_cpu_qty")
            or 1
        )

    sdc_resp = (
        client.table("server_default_components")
        .select("component_product_id, quantity")
        .eq("server_product_id", server_product_id)
        .eq("component_type", "cpu")
        .limit(1)
        .execute()
    )
    cores_per_socket = 0
    if sdc_resp.data:
        cpu_id = sdc_resp.data[0]["component_product_id"]
        cs_resp = (
            client.table("component_specs")
            .select("cores")
            .eq("product_id", cpu_id)
            .limit(1)
            .execute()
        )
        if cs_resp.data and cs_resp.data[0].get("cores"):
            cores_per_socket = int(cs_resp.data[0]["cores"])

    return {
        "cores_per_socket": cores_per_socket,
        "num_sockets": int(num_sockets) if num_sockets is not None else 1,
        "total_physical_cores": (int(cores_per_socket) if cores_per_socket else 0)
        * (int(num_sockets) if num_sockets else 1),
    }


def compute_licensed_units(
    rule: dict, cores_per_socket: int, num_sockets: int, vcpu_count: int = 0
) -> int:
    """Given a pricing rule and server CPU config, return the billable unit count."""
    driver = rule["cost_driver"]

    if driver == "flat":
        return 1

    if driver == "vcpu_count":
        return max(int(vcpu_count or 0), 0)

    # Core-based drivers: licensed_cores, raw_cores, core_packs
    floor_per_socket = int(rule.get("min_units_per_socket") or 0)
    floor_per_server = int(rule.get("min_units_per_server") or 0)
    increment = int(rule.get("unit_increment") or 1)

    effective_per_socket = max(int(cores_per_socket or 0), floor_per_socket)
    total = effective_per_socket * max(int(num_sockets or 0), 1)
    total = max(total, floor_per_server)

    if increment > 1:
        total = int(math.ceil(total / increment) * increment)

    mrc_repr = rule.get("mrc_represents", "per_unit")
    if mrc_repr == "per_pack" and increment > 0:
        return int(total // increment)

    return int(total)


def _get_overhead_constants(client) -> dict[str, Decimal]:
    resp = client.table("overhead_constants").select("key, value").execute()
    return {r["key"]: _decimal(r["value"]) for r in resp.data}


def _get_dc_cost_drivers(client, dc_code: str) -> list[dict]:
    resp = (
        client.table("dc_cost_drivers")
        .select("cost_category, amount, currency_code")
        .eq("dc_code", dc_code)
        .execute()
    )
    return resp.data or []


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def build_quote(
    client,
    server_sku: str,
    addons: list[AddonLine],
    currency: str,
    dc_code: str,
    term_months: int,
    quote_date: Optional[date] = None,
    include_capex: bool = True,
    include_overhead: bool = True,
) -> dict[str, Any]:
    """
    Build a quote. addons = [{"sku": "Intel Xeon Gold 6526Y...", "quantity": 2}, ...].
    Returns dict with totals_mrc, totals_nrc, line_items, addon_lines, capex, overhead_breakdown, errors.
    """
    if quote_date is None:
        quote_date = date.today()
    errors: list[str] = []
    line_items: list[dict] = []
    addon_lines: list[dict] = []

    # Resolve server
    server_id = _get_product_id(client, server_sku)
    if not server_id:
        errors.append(f"Server not found: {server_sku}")
        return {
            "totals_mrc": Decimal("0"),
            "totals_nrc": Decimal("0"),
            "currency": currency,
            "line_items": [],
            "addon_lines": [],
            "capex": None,
            "overhead_breakdown": None,
            "errors": errors,
        }
    server_mrc, server_nrc = _get_server_pricing(client, server_id, currency, term_months)
    line_items.append({"sku": server_sku, "quantity": 1, "mrc": server_mrc, "nrc": server_nrc, "currency": currency})
    total_mrc = server_mrc
    total_nrc = server_nrc

    # FX for component USD → quote currency
    usd_rate = _get_spot_rate(client, "USD", quote_date) if currency != "USD" else Decimal("1")
    if currency != "USD" and usd_rate is None:
        errors.append("No spot FX rate for USD; addon pricing may be wrong")

    default_ids = _get_default_component_ids(client, server_id)
    # CPU config is only needed for core-driven addons (VMware, SQL, Windows, RHEL for VMs).
    # Fetch lazily to avoid 3 extra round-trips on quotes with no core-driven software.
    _cpu_config_cache: Optional[dict] = None

    def _cpu_config() -> dict:
        nonlocal _cpu_config_cache
        if _cpu_config_cache is None:
            _cpu_config_cache = _get_server_cpu_config(client, server_id)
        return _cpu_config_cache

    # Use server nameplate watts (per CPQ sheet) when set; else sum default component watts
    server_watts = _get_server_watts(client, server_id)
    if server_watts is not None:
        total_watts = server_watts
    else:
        total_watts = 0
        default_watts_resp = (
            client.table("server_default_components")
            .select("component_product_id")
            .eq("server_product_id", server_id)
            .execute()
        )
        for r in default_watts_resp.data or []:
            total_watts += _get_component_watts(client, r["component_product_id"])

    for addon in addons:
        sku = addon.get("sku") or ""
        qty = max(1, int(addon.get("quantity") or 1))
        comp_id = _get_product_id(client, sku)
        if not comp_id:
            errors.append(f"Addon not found: {sku}")
            continue
        rule = _get_pricing_rule(client, comp_id)
        mrc, nrc = _get_component_pricing(client, comp_id, term_months, "USD")
        if currency != "USD" and usd_rate:
            mrc = _round2(mrc * usd_rate)
            nrc = _round2(nrc * usd_rate)

        licensed_units = None
        if rule and rule.get("cost_driver") and rule["cost_driver"] != "flat":
            vcpu_count = int(addon.get("vcpu_count") or 0)
            config = _cpu_config()
            if (
                rule["cost_driver"] not in ("flat", "vcpu_count")
                and config["cores_per_socket"] == 0
            ):
                errors.append(
                    f"Warning: {sku} uses core-driven pricing ({rule['cost_driver']}) but "
                    f"server '{server_sku}' has no CPU core count resolved — "
                    f"defaulting to floor ({rule.get('min_units_per_socket') or 0} cores/socket)"
                )
            licensed_units = compute_licensed_units(
                rule,
                cores_per_socket=config["cores_per_socket"],
                num_sockets=config["num_sockets"],
                vcpu_count=vcpu_count,
            )
            mrc_total = _round2(mrc * licensed_units)
            nrc_total = _round2(nrc * qty)
        else:
            mrc_total = _round2(mrc * qty)
            nrc_total = _round2(nrc * qty)

        addon_lines.append({
            "sku": sku,
            "quantity": qty,
            "unit_mrc": mrc,
            "unit_nrc": nrc,
            "mrc": mrc_total,
            "nrc": nrc_total,
            "currency": currency,
            "licensed_units": licensed_units,
            "pricing_rule": (rule or {}).get("cost_driver", "flat"),
        })
        line_items.append({"sku": sku, "quantity": qty, "mrc": mrc_total, "nrc": nrc_total, "currency": currency})
        total_mrc += mrc_total
        total_nrc += nrc_total
        total_watts += _get_component_watts(client, comp_id) * qty

    total_mrc = _round2(total_mrc)
    total_nrc = _round2(total_nrc)

    # Capex (server + optional addon hardware)
    capex_out = None
    if include_capex:
        server_capex = _get_capex(client, server_id)
        if server_capex:
            capex_out = {"server": {"sku": server_sku, **server_capex}, "addons": []}
            for addon in addon_lines:
                comp_id = _get_product_id(client, addon["sku"])
                if comp_id:
                    cap = _get_capex(client, comp_id)
                    if cap:
                        capex_out["addons"].append({"sku": addon["sku"], "quantity": addon["quantity"], **cap})

    # Overhead breakdown (DC cost drivers + constants)
    overhead_out = None
    power_per_kw_rate = None
    power_per_kw_currency = None
    if include_overhead and dc_code:
        constants = _get_overhead_constants(client)
        drivers = _get_dc_cost_drivers(client, dc_code)
        total_kw = (Decimal(total_watts) / 1000) if total_watts else Decimal("0")
        by_category = []
        for d in drivers:
            amt = _decimal(d["amount"])
            curr = d["currency_code"]
            cat = d["cost_category"]
            if "per_kw" in cat or "power" in cat.lower():
                value = _round2(amt * total_kw)
                if "power" in cat.lower() or cat == "power_per_kw":
                    power_per_kw_rate = amt
                    power_per_kw_rate_currency = curr
            elif "support" in cat.lower() and "tech" in cat.lower():
                # Tech time: rate (e.g. 80.27) × 0.5 hours per server for -M devices
                value = _round2(amt * Decimal("0.5"))
            elif "per_server" in cat:
                value = amt  # 1 server
            else:
                value = amt
            by_category.append({"category": cat, "amount": value, "currency": curr})
        overhead_out = {
            "dc_code": dc_code,
            "total_watts": int(total_watts),
            "total_kw": float(total_kw),
            "by_category": by_category,
            "power_per_kw_rate": float(power_per_kw_rate) if power_per_kw_rate is not None else None,
            "power_per_kw_rate_currency": power_per_kw_currency,
            "overhead_constants": {k: float(v) for k, v in constants.items()},
        }

    # 12-month financial summary (revenue, costs, margin)
    financial_12m = None
    if term_months == 12 and currency:
        revenue_12m = _round2(total_mrc * 12 + total_nrc)
        cost_capex_quote = Decimal("0")
        if capex_out and capex_out.get("server"):
            cap_amt = capex_out["server"].get("amount") or Decimal("0")
            cap_curr = capex_out["server"].get("currency", "USD")
            if cap_curr == currency:
                cost_capex_quote = cap_amt
            elif cap_curr != currency and usd_rate:
                cost_capex_quote = _round2(cap_amt * usd_rate) if cap_curr == "USD" else cap_amt
            else:
                cost_capex_quote = cap_amt  # leave in source currency for display
        for a in ((capex_out or {}).get("addons") or []):
            cap_amt = (a.get("amount") or Decimal("0")) * (a.get("quantity") or 1)
            cap_curr = a.get("currency", "USD")
            if cap_curr == currency:
                cost_capex_quote += cap_amt
            elif cap_curr == "USD" and usd_rate:
                cost_capex_quote += _round2(cap_amt * usd_rate)
            else:
                cost_capex_quote += cap_amt
        cost_overhead_12m = Decimal("0")
        if overhead_out and overhead_out.get("by_category"):
            monthly_overhead = sum(_decimal(b["amount"]) for b in overhead_out["by_category"])
            cost_overhead_12m = _round2(monthly_overhead * 12)
        margin_12m = _round2(revenue_12m - cost_capex_quote - cost_overhead_12m)
        margin_pct = (float(margin_12m / revenue_12m * 100) if revenue_12m else 0)
        financial_12m = {
            "revenue_12m": float(revenue_12m),
            "cost_capex": float(cost_capex_quote),
            "cost_overhead_12m": float(cost_overhead_12m),
            "margin_12m": float(margin_12m),
            "margin_pct": round(margin_pct, 1),
            "currency": currency,
        }

    return {
        "totals_mrc": total_mrc,
        "totals_nrc": total_nrc,
        "currency": currency,
        "dc_code": dc_code,
        "term_months": term_months,
        "line_items": line_items,
        "addon_lines": addon_lines,
        "capex": capex_out,
        "overhead_breakdown": overhead_out,
        "financial_summary_12m": financial_12m,
        "usd_rate": float(usd_rate) if usd_rate is not None else None,
        "errors": errors,
    }


def format_quote(result: dict) -> str:
    """Human-readable quote summary (for CLI)."""
    lines = [
        "--- Quote ---",
        f"Total MRC: {result['currency']} {result['totals_mrc']}",
        f"Total NRC: {result['currency']} {result['totals_nrc']}",
        f"Term: {result['term_months']} mo  DC: {result.get('dc_code', '')}",
        "",
        "Line items:",
    ]
    for li in result["line_items"]:
        lines.append(f"  {li['sku']} x{li['quantity']}  MRC {li['mrc']}  NRC {li['nrc']}")
    if result.get("addon_lines"):
        lines.append("")
        lines.append("Add-on breakdown:")
        for a in result["addon_lines"]:
            units_info = ""
            if a.get("licensed_units") is not None:
                units_info = f"  [{a.get('pricing_rule', 'flat')}: {a['licensed_units']} units]"
            lines.append(
                f"  {a['sku']} x{a['quantity']}  unit MRC {a['unit_mrc']}  →  MRC {a['mrc']}  NRC {a['nrc']}{units_info}"
            )
    if result.get("capex"):
        lines.append("")
        lines.append("CapEx:")
        c = result["capex"]
        if c.get("server"):
            s = c["server"]
            lines.append(f"  Server {s.get('sku', '')}: {s.get('amount')} {s.get('currency', '')}")
        for a in c.get("addons", []):
            lines.append(f"  {a.get('sku', '')} x{a.get('quantity', 1)}: {a.get('amount')} {a.get('currency', '')}")
    if result.get("overhead_breakdown"):
        lines.append("")
        lines.append("Overhead (internal cost breakdown):")
        o = result["overhead_breakdown"]
        lines.append(f"  Total wattage: {o.get('total_watts')} W ({o.get('total_kw')} kW)")
        if o.get("power_per_kw_rate") is not None:
            lines.append(f"  power_per_kw rate: {o['power_per_kw_rate']} {o.get('power_per_kw_rate_currency', '')}")
        for b in o.get("by_category", []):
            lines.append(f"  {b['category']}: {b['amount']} {b['currency']}")
        lines.append("  Constants: " + ", ".join(f"{k}={v}" for k, v in o.get("overhead_constants", {}).items()))
    if result.get("financial_summary_12m"):
        f = result["financial_summary_12m"]
        lines.append("")
        lines.append("12-month financial summary:")
        lines.append(f"  Revenue (12m): {f['currency']} {f['revenue_12m']}")
        lines.append(f"  Cost Capex: {f['currency']} {f['cost_capex']}")
        lines.append(f"  Cost Overhead (12m): {f['currency']} {f['cost_overhead_12m']}")
        lines.append(f"  Margin (12m): {f['currency']} {f['margin_12m']}  ({f['margin_pct']}%)")
    if result.get("errors"):
        lines.append("")
        lines.append("Errors: " + "; ".join(result["errors"]))
    return "\n".join(lines)


if __name__ == "__main__":
    import os
    import sys
    from pathlib import Path

    # Allow running from repo root or project dir
    root = Path(__file__).resolve().parent
    sys.path.insert(0, str(root.parent.parent))
    load_dotenv = getattr(__import__("dotenv", fromlist=["load_dotenv"]), "load_dotenv", None)
    if load_dotenv:
        load_dotenv(root.parent.parent / ".env")

    from supabase import create_client

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        print("Set SUPABASE_URL and SUPABASE_KEY")
        sys.exit(1)
    client = create_client(url, key)

    # Simple CLI: server_sku [--currency CAD] [--dc TOR] [--term 12] [--addon "SKU" [--qty 2] ...]
    server_sku = "Pro Series 6.0 - M"
    currency = "CAD"
    dc_code = "TOR"
    term = 12
    addons = []
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--currency" and i + 1 < len(sys.argv):
            currency = sys.argv[i + 1]
            i += 2
        elif arg == "--dc" and i + 1 < len(sys.argv):
            dc_code = sys.argv[i + 1]
            i += 2
        elif arg == "--term" and i + 1 < len(sys.argv):
            term = int(sys.argv[i + 1])
            i += 2
        elif arg == "--addon" and i + 1 < len(sys.argv):
            sku = sys.argv[i + 1]
            qty = 1
            i += 2
            if i + 1 < len(sys.argv) and sys.argv[i] == "--qty":
                qty = int(sys.argv[i + 1])
                i += 2
            addons.append({"sku": sku, "quantity": qty})
        else:
            if not arg.startswith("-"):
                server_sku = arg
            i += 1

    result = build_quote(client, server_sku, addons, currency, dc_code, term)
    print(format_quote(result))
