"""
test_quote_e2e.py — End-to-end quote tests
-------------------------------------------
Asserts that build_quote() returns expected MRC/NRC for known configs
(server + components, currency, DC, term). Ground truth from CPQ Excel / user-provided.

Usage:
    cd projects/cpq-replacement-db-only
    python tests/test_quote_e2e.py

Env: SUPABASE_URL, SUPABASE_KEY (same as validate_seed_phase2.py).
"""

import json
import os
import sys
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

# Project root so we can import quote
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from supabase import create_client

ROOT = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(ROOT / ".env")

from quote import build_quote

OUTPUTS = Path(__file__).parent / "outputs"
OUTPUTS.mkdir(parents=True, exist_ok=True)

# Tolerance for MRC/NRC (FX rounding when converting USD addons to CAD)
MRC_TOLERANCE = Decimal("10")
NRC_TOLERANCE = Decimal("1")


# ---------------------------------------------------------------------------
# E2E test cases (from user spec + CPQ v28)
# ---------------------------------------------------------------------------
# Cases with expected_mrc/expected_nrc set: assert against those values.
# Cases with expected_mrc=None/expected_nrc=None: FAIL until you provide
# values from Excel — run the config in CPQ, then set expected_mrc/expected_nrc
# below and remove the None sentinel. See QUOTE_E2E_SCENARIOS.md for config details.
# ---------------------------------------------------------------------------

PENDING_MSG = "PENDING: set expected_mrc and expected_nrc from Excel (see tests/QUOTE_E2E_SCENARIOS.md)"

# Ocean FX Rates (reference only; sheet uses spot rates, so Expected uses quote.usd_rate from DB).
# From Ocean FX Rates table: Convert From → Convert To.
OCEAN_FX = {
    "USD": {"USD": 1.0, "CAD": 1.41, "GBP": 0.76, "EUR": 0.91},
    "CAD": {"USD": 0.85, "CAD": 1.0, "GBP": 0.585, "EUR": 0.74},
    "GBP": {"USD": 1.40, "CAD": 2.07, "GBP": 1.0, "EUR": 1.23},
    "EUR": {"USD": None, "CAD": None, "GBP": None, "EUR": 1.0},
}


def _ocean_convert(amount: float, from_curr: str, to_curr: str) -> float | None:
    """Convert amount using Ocean FX. Used for Expected (sheet) column only."""
    if from_curr == to_curr or amount is None:
        return amount
    rate = (OCEAN_FX.get(from_curr) or {}).get(to_curr)
    if rate is None:
        return None
    return round(amount * rate, 2)

QUOTE_CASES = [
    # --- Locked (values from MH Financial Summary) ---
    {
        "id": "pro6m_cad_tor_12m",
        "description": "Pro Series 6.0 - M, default config, CAD, Toronto, 12 mo",
        "server_sku": "Pro Series 6.0 - M",
        "addons": [],
        "currency": "CAD",
        "dc_code": "TOR",
        "term_months": 12,
        "expected_mrc": Decimal("1249"),   # MH Financial Summary: Total MRC $1,249
        "expected_nrc": Decimal("1249"),   # MH Financial Summary: Total NRC $1,249
        "expected_sheet": {
            "currency": "CAD",
            "server_mrc": 1249,
            "server_nrc": 1249,
            "addon_mrc": 0,
            "addon_nrc": 0,
            "total_mrc": 1249,
            "total_nrc": 1249,
            "revenue_12m": 16237,  # TCV from MH Financial Summary
            "capex_server_usd": 7569,
            "capex_addons_usd": 0,
            "cost_capex_12m": 10837,  # CapEx from MH Financial Summary
            "watts": 400,
            "power_monthly_cad": 87.31,
            "network_cad": 58.70,
            "billing_cad": 4.63,
            "supply_chain_cad": 6.40,
            "dc_ops_cad": 6.76,
            "support_cad": 40.14,
            "colo_cad": 17.79,
            "cost_overhead_12m": 2661.72,  # ~221.81/mo × 12 from sheet overhead
        },
    },
    {
        "id": "pro6m_cad_tor_24m",
        "description": "Pro Series 6.0 - M, default config, CAD, Toronto, 24 mo",
        "server_sku": "Pro Series 6.0 - M",
        "addons": [],
        "currency": "CAD",
        "dc_code": "TOR",
        "term_months": 24,
        "expected_mrc": Decimal("969"),
        "expected_nrc": Decimal("1249"),
    },
    {
        "id": "pro6m_cad_tor_36m",
        "description": "Pro Series 6.0 - M, default config, CAD, Toronto, 36 mo",
        "server_sku": "Pro Series 6.0 - M",
        "addons": [],
        "currency": "CAD",
        "dc_code": "TOR",
        "term_months": 36,
        "expected_mrc": Decimal("829"),
        "expected_nrc": Decimal("1249"),
    },
    {
        "id": "adv6m_cpu_drives_cad",
        "description": "Advanced Series 6.0 - M + 2x Gold 6526Y CPU + 2x 1.92 TB SSD, CAD",
        "server_sku": "Advanced Series 6.0 - M",
        "addons": [
            {"sku": "Intel Xeon Gold 6526Y 2.9G, 16/32T", "quantity": 2},
            {"sku": "1.92 TB SATA 2.5in SSD", "quantity": 2},
        ],
        "currency": "CAD",
        "dc_code": "TOR",
        "term_months": 12,
        "expected_mrc": Decimal("1789"),
        "expected_nrc": Decimal("969"),
        "mrc_tolerance": MRC_TOLERANCE,
        "nrc_tolerance": NRC_TOLERANCE,
    },
    # --- Pending: provide MRC/NRC from Excel (will FAIL until set) ---
    {
        "id": "pro6m_usd_iad_12m",
        "description": "Pro Series 6.0 - M, default config, USD, IAD, 12 mo",
        "server_sku": "Pro Series 6.0 - M",
        "addons": [],
        "currency": "USD",
        "dc_code": "IAD",
        "term_months": 12,
        "expected_mrc": Decimal("1079"),
        "expected_nrc": Decimal("1079"),
    },
    {
        "id": "pro6m_gbp_por_24m",
        "description": "Pro Series 6.0 - M, default config, GBP, Portsmouth, 24 mo",
        "server_sku": "Pro Series 6.0 - M",
        "addons": [],
        "currency": "GBP",
        "dc_code": "POR",
        "term_months": 24,
        "expected_mrc": Decimal("659"),
        "expected_nrc": Decimal("899"),
    },
    {
        "id": "cluster5_cad_tor_12m",
        "description": "Cluster 5.0 (Dell R440), default config, CAD, Toronto, 12 mo",
        "server_sku": "Cluster 5.0 (Dell R440)",
        "addons": [],
        "currency": "CAD",
        "dc_code": "TOR",
        "term_months": 12,
        "expected_mrc": None,
        "expected_nrc": None,
    },
    {
        "id": "atomic5_cad_tor_12m",
        "description": "Atomic 5.0 (Dell R650xs), default config, CAD, Toronto, 12 mo",
        "server_sku": "Atomic 5.0 (Dell R650xs)",
        "addons": [],
        "currency": "CAD",
        "dc_code": "TOR",
        "term_months": 12,
        "expected_mrc": None,
        "expected_nrc": None,
    },
    {
        "id": "adv6m_sql_lm_standard_cad",
        "description": "Advanced 6.0 - M defaults + SQL Server 2022 Standard + LM Standard Monitoring, CAD TOR 12 mo",
        "server_sku": "Advanced Series 6.0 - M",
        "addons": [
            {"sku": "SQL Server 2022 Standard Edition", "quantity": 1},
            {"sku": "LM Standard Monitoring", "quantity": 1},
        ],
        "currency": "CAD",
        "dc_code": "TOR",
        "term_months": 12,
        "expected_mrc": None,
        "expected_nrc": None,
    },
    {
        "id": "pro6m_storage_heavy_cad",
        "description": "Pro Series 6.0 - M + 4x 1.92 TB SATA 2.5in SSD, CAD TOR 12 mo",
        "server_sku": "Pro Series 6.0 - M",
        "addons": [
            {"sku": "1.92 TB SATA 2.5in SSD", "quantity": 4},
        ],
        "currency": "CAD",
        "dc_code": "TOR",
        "term_months": 12,
        "expected_mrc": Decimal("1529"),
        "expected_nrc": Decimal("1249"),
        "expected_sheet": {
            "currency": "CAD",
            # Component (sheet)
            "server_mrc": 1249,
            "server_nrc": 1249,
            "addon_mrc": 280,
            "addon_nrc": 0,
            "total_mrc": 1529,
            "total_nrc": 1249,
            # Capex (server + addons; Products - Hosting.csv col AG row 193 = $349 per 1.92 TB drive)
            "capex_server_usd": 7569,
            "capex_addons_usd": 1396,
            # Overhead
            "watts": 400,
            "power_monthly_cad": 87.31,
            "network_cad": 58.33,
            "billing_cad": 4.63,
            "supply_chain_cad": 6.35,
            "dc_ops_cad": 6.76,
            "support_cad": 40.14,
            "colo_cad": 17.79,
            # 12m financial (revenue/overhead from sheet; margin computed = revenue − capex − overhead, not EBIT)
            "revenue_12m": 19597,
            "cost_overhead_12m": 3143.28,
        },
        "mrc_tolerance": Decimal("10"),
        "nrc_tolerance": Decimal("0"),
    },
    {
        "id": "pro6_vhost_cad_tor_12m",
        "description": "Pro Series 6.0 vHost (not -M), default config, CAD, Toronto, 12 mo",
        "server_sku": "Pro Series 6.0 vHost",
        "addons": [],
        "currency": "CAD",
        "dc_code": "TOR",
        "term_months": 12,
        "expected_mrc": None,
        "expected_nrc": None,
    },
]


def test_compute_licensed_units():
    """Unit tests for compute_licensed_units -- no DB needed."""
    from quote import compute_licensed_units

    # VMware: 8-core CPU, 1 socket -> floor to 16
    rule_vmware = {
        "cost_driver": "licensed_cores",
        "min_units_per_socket": 16,
        "min_units_per_server": None,
        "unit_increment": 2,
        "mrc_represents": "per_unit",
    }
    assert compute_licensed_units(rule_vmware, cores_per_socket=8, num_sockets=1) == 16

    # VMware: 16-core CPU, 2 sockets -> 32
    assert compute_licensed_units(rule_vmware, cores_per_socket=16, num_sockets=2) == 32

    # VMware: 20-core CPU, 1 socket -> 20 (already above 16, already even)
    assert compute_licensed_units(rule_vmware, cores_per_socket=20, num_sockets=1) == 20

    # VMware: 21-core CPU, 1 socket -> 22 (round up to nearest 2)
    assert compute_licensed_units(rule_vmware, cores_per_socket=21, num_sockets=1) == 22

    # SQL Server: 12-core CPU, 2 sockets -> 24 cores -> 12 packs
    rule_sql = {
        "cost_driver": "raw_cores",
        "min_units_per_socket": 4,
        "min_units_per_server": None,
        "unit_increment": 2,
        "mrc_represents": "per_pack",
    }
    assert compute_licensed_units(rule_sql, cores_per_socket=12, num_sockets=2) == 12

    # SQL Server: 4-core CPU, 1 socket -> floor 4 -> 2 packs
    assert compute_licensed_units(rule_sql, cores_per_socket=4, num_sockets=1) == 2

    # SQL Server: 2-core CPU, 1 socket -> floor to 4 -> 2 packs
    assert compute_licensed_units(rule_sql, cores_per_socket=2, num_sockets=1) == 2

    # Windows Server: 8-core, 1 socket -> floor to 16 (server min) -> 8 packs
    rule_win = {
        "cost_driver": "core_packs",
        "min_units_per_socket": 8,
        "min_units_per_server": 16,
        "unit_increment": 2,
        "mrc_represents": "per_pack",
    }
    assert compute_licensed_units(rule_win, cores_per_socket=8, num_sockets=1) == 8

    # Windows Server: 16-core, 2 sockets -> 32 cores -> 16 packs
    assert compute_licensed_units(rule_win, cores_per_socket=16, num_sockets=2) == 16

    # RHEL for VMs: 4 vCPUs
    rule_rhel = {
        "cost_driver": "vcpu_count",
        "min_units_per_socket": None,
        "min_units_per_server": None,
        "unit_increment": 1,
        "mrc_represents": "per_tier_unit",
    }
    assert (
        compute_licensed_units(
            rule_rhel, cores_per_socket=0, num_sockets=0, vcpu_count=4
        )
        == 4
    )

    # Flat: always 1
    rule_flat = {
        "cost_driver": "flat",
        "min_units_per_socket": None,
        "min_units_per_server": None,
        "unit_increment": None,
        "mrc_represents": "flat_total",
    }
    assert compute_licensed_units(rule_flat, cores_per_socket=48, num_sockets=2) == 1

    print("  compute_licensed_units: all assertions passed")


def _decimal(n):
    if n is None:
        return Decimal("0")
    return Decimal(str(n))


def _quote_to_json(quote: dict) -> dict:
    """Serialize build_quote result for JSON (Decimal -> float)."""
    out = {
        "totals_mrc": float(quote["totals_mrc"]),
        "totals_nrc": float(quote["totals_nrc"]),
        "currency": quote["currency"],
        "dc_code": quote.get("dc_code"),
        "term_months": quote["term_months"],
        "line_items": [
            {k: (float(v) if isinstance(v, Decimal) else v) for k, v in li.items()}
            for li in quote["line_items"]
        ],
        "addon_lines": [
            {k: (float(v) if isinstance(v, Decimal) else v) for k, v in a.items()}
            for a in quote.get("addon_lines", [])
        ],
        "capex": None,
        "overhead_breakdown": None,
        "financial_summary_12m": None,
    }
    if quote.get("capex"):
        c = quote["capex"]
        out["capex"] = {"server": None, "addons": []}
        if c.get("server"):
            s = c["server"].copy()
            if isinstance(s.get("amount"), Decimal):
                s["amount"] = float(s["amount"])
            out["capex"]["server"] = s
        for a in c.get("addons", []):
            aa = a.copy()
            if isinstance(aa.get("amount"), Decimal):
                aa["amount"] = float(aa["amount"])
            out["capex"]["addons"].append(aa)
    if quote.get("overhead_breakdown"):
        o = quote["overhead_breakdown"].copy()
        o["by_category"] = [
            {k: (float(v) if isinstance(v, Decimal) else v) for k, v in b.items()}
            for b in o.get("by_category", [])
        ]
        out["overhead_breakdown"] = o
    if quote.get("financial_summary_12m"):
        out["financial_summary_12m"] = quote["financial_summary_12m"]
    return out


def _by_category_amount(quote: dict, category_substring: str) -> tuple[float | None, str]:
    """Get amount and currency for first by_category entry whose category contains substring."""
    for b in quote.get("overhead_breakdown", {}).get("by_category", []) or []:
        if category_substring in b.get("category", "").lower():
            amt = b.get("amount")
            return (float(amt) if amt is not None else None, b.get("currency", ""))
    return (None, "")


def _build_quote_table(quote: dict, expected_sheet: dict | None) -> list[dict]:
    """Build Cost | Expected (sheet) | Calculated (DB) table with section headers (12m: Revenue, Capex, Overhead, Margin) and sub-items."""
    curr = (expected_sheet or {}).get("currency", quote.get("currency", ""))
    rows = []
    es = expected_sheet or {}

    def section(title: str):
        rows.append({"cost": title, "expected": None, "expected_unit": "", "calculated": None, "calculated_unit": "", "is_section": True})

    def row(cost: str, exp, exp_unit: str, calc, calc_unit: str):
        rows.append({
            "cost": cost,
            "expected": exp,
            "expected_unit": exp_unit or "",
            "calculated": calc,
            "calculated_unit": calc_unit or "",
            "is_section": False,
        })

    # --- 12m: Revenue (header then revenue items) ---
    section("12m: Revenue")
    if quote.get("line_items"):
        li = quote["line_items"][0]
        row("  Server MRC", es.get("server_mrc"), curr, float(li.get("mrc")), curr)
        row("  Server NRC", es.get("server_nrc"), curr, float(li.get("nrc")), curr)
    addon_mrc_sum = sum(float(a.get("mrc", 0)) for a in quote.get("addon_lines", []))
    addon_nrc_sum = sum(float(a.get("nrc", 0)) for a in quote.get("addon_lines", []))
    row("  Addon MRC", es.get("addon_mrc"), curr, addon_mrc_sum, curr)
    row("  Addon NRC", es.get("addon_nrc"), curr, addon_nrc_sum, curr)
    row("  Total MRC", es.get("total_mrc"), curr, float(quote.get("totals_mrc", 0)), curr)
    row("  Total NRC", es.get("total_nrc"), curr, float(quote.get("totals_nrc", 0)), curr)
    f = quote.get("financial_summary_12m")
    if f:
        row("  Total (12m Revenue)", es.get("revenue_12m"), curr, f.get("revenue_12m"), f.get("currency", curr))

    # --- 12m: Cost Capex (header then capex items) ---
    section("12m: Cost Capex")
    if (quote.get("capex") or {}).get("server"):
        s = quote["capex"]["server"]
        row("  Capex (server)", es.get("capex_server_usd"), "USD", float(s.get("amount")), s.get("currency", "USD"))
    addon_cap = 0.0
    addon_cap_curr = "USD"
    for a in (quote.get("capex") or {}).get("addons", []) or []:
        addon_cap += float(a.get("amount", 0) or 0) * int(a.get("quantity", 1))
        addon_cap_curr = a.get("currency", "USD")
    row("  Capex (addons)", es.get("capex_addons_usd"), "USD", addon_cap, addon_cap_curr)
    if f:
        # Expected Total (12m Cost Capex): use same spot rate as quote (sheet uses spot)
        exp_capex_usd = (es.get("capex_server_usd") or 0) + (es.get("capex_addons_usd") or 0)
        spot_rate = quote.get("usd_rate")
        if exp_capex_usd and curr and curr != "USD" and spot_rate is not None:
            exp_capex_quote = round(exp_capex_usd * spot_rate, 2)
        elif exp_capex_usd and curr == "USD":
            exp_capex_quote = exp_capex_usd
        else:
            exp_capex_quote = es.get("cost_capex_12m")
        row("  Total (12m Cost Capex)", exp_capex_quote, curr, f.get("cost_capex"), f.get("currency", curr))

    # --- 12m: Cost Overhead (header then overhead items) ---
    section("12m: Cost Overhead")
    if quote.get("overhead_breakdown"):
        row("  Watts", es.get("watts"), "W", quote["overhead_breakdown"].get("total_watts"), "W")
    power_amt, power_c = _by_category_amount(quote, "power_per_kw")
    row("  Power (monthly)", es.get("power_monthly_cad"), curr, power_amt, power_c or curr)
    amt, c = _by_category_amount(quote, "network")
    row("  Network", es.get("network_cad"), curr, amt, c or curr)
    amt, c = _by_category_amount(quote, "billing")
    row("  Billing & Collections", es.get("billing_cad"), curr, amt, c or curr)
    amt, c = _by_category_amount(quote, "supply_chain")
    row("  Supply Chain", es.get("supply_chain_cad"), curr, amt, c or curr)
    amt, c = _by_category_amount(quote, "dc_infra")
    row("  DC Ops / Infrastructure", es.get("dc_ops_cad"), curr, amt, c or curr)
    amt, c = _by_category_amount(quote, "support")
    row("  Support (0.5h × rate)", es.get("support_cad"), curr, amt, c or curr)
    amt, c = _by_category_amount(quote, "colo")
    row("  Colo (space)", es.get("colo_cad"), curr, amt, c or curr)
    if f:
        row("  Total (12m Cost Overhead)", es.get("cost_overhead_12m"), curr, f.get("cost_overhead_12m"), f.get("currency", curr))

    # --- 12m: Margin (header then margin items). Sheet doesn't call out margin — compute from revenue − capex − overhead. ---
    section("12m: Margin")
    if f:
        # Expected margin = revenue − cost capex − cost overhead (calculated from sheet inputs, not EBIT/EBITA)
        exp_capex_usd = (es.get("capex_server_usd") or 0) + (es.get("capex_addons_usd") or 0)
        spot_rate = quote.get("usd_rate")
        if exp_capex_usd and curr and curr != "USD" and spot_rate is not None:
            exp_capex = round(exp_capex_usd * spot_rate, 2)
        elif exp_capex_usd and curr == "USD":
            exp_capex = exp_capex_usd
        else:
            exp_capex = es.get("cost_capex_12m") or 0
        exp_revenue = es.get("revenue_12m") or 0
        exp_overhead = es.get("cost_overhead_12m") or 0
        exp_margin = round(exp_revenue - exp_capex - exp_overhead, 2) if exp_revenue else None
        exp_margin_pct = round(exp_margin / exp_revenue * 100, 1) if (exp_revenue and exp_margin is not None) else None
        row("  Margin", exp_margin, curr, f.get("margin_12m"), f.get("currency", curr))
        row("  Margin %", exp_margin_pct, "%", f.get("margin_pct"), "%")

    return rows


def _fmt_val(v, unit: str) -> str:
    if v is None:
        return "—"
    if isinstance(v, float) and unit == "%":
        return f"{v}%"
    if unit in ("W", "%"):
        return f"{v} {unit}"
    return f"{v} {unit}"


def _print_quote_breakdown(case_id: str, quote: dict, table: list[dict]) -> None:
    """Print the Cost | Expected (sheet) | Calculated (DB) table with section headers. Expected shows — when no sheet."""
    print(f"\n  ─── {case_id}: Expected (sheet) vs Calculated (DB) ───")
    print("  Cost                              | Expected (sheet)     | Calculated (DB)")
    print("  " + "-" * 72)
    for r in table:
        if r.get("is_section"):
            print("  " + "-" * 72)
            print(f"  {r.get('cost', '')}")
            print("  " + "-" * 72)
            continue
        exp_str = _fmt_val(r.get("expected"), r.get("expected_unit", ""))
        calc_str = _fmt_val(r.get("calculated"), r.get("calculated_unit", ""))
        cost = (r.get("cost") or "").ljust(33)
        print(f"  {cost} | {exp_str:<20} | {calc_str}")
    f = quote.get("financial_summary_12m")
    if f:
        print("  " + "-" * 72)
        print(f"  Profitability margin (12m):   {f.get('currency', '')} {f.get('margin_12m')}  ({f.get('margin_pct')}%)")
    print()


def run_quote_e2e(client) -> list[dict]:
    results = []
    for case in QUOTE_CASES:
        result = build_quote(
            client,
            server_sku=case["server_sku"],
            addons=case.get("addons", []),
            currency=case["currency"],
            dc_code=case["dc_code"],
            term_months=case["term_months"],
            include_capex=True,
            include_overhead=True,
        )
        expected_mrc = case.get("expected_mrc")
        expected_nrc = case.get("expected_nrc")
        pending = expected_mrc is None or expected_nrc is None
        if pending:
            passed = False
            failure_reason = PENDING_MSG
        else:
            mrc_tol = case.get("mrc_tolerance", Decimal("0"))
            nrc_tol = case.get("nrc_tolerance", Decimal("0"))
            actual_mrc = _decimal(result["totals_mrc"])
            actual_nrc = _decimal(result["totals_nrc"])
            mrc_ok = abs(actual_mrc - expected_mrc) <= mrc_tol
            nrc_ok = abs(actual_nrc - expected_nrc) <= nrc_tol
            passed = mrc_ok and nrc_ok and not result.get("errors")
            failure_reason = None
            if not mrc_ok:
                failure_reason = f"MRC expected {expected_mrc} got {actual_mrc}"
            elif not nrc_ok:
                failure_reason = f"NRC expected {expected_nrc} got {actual_nrc}"
            elif result.get("errors"):
                failure_reason = "; ".join(result["errors"])

        actual_mrc = _decimal(result["totals_mrc"])
        actual_nrc = _decimal(result["totals_nrc"])
        quote_json = _quote_to_json(result)
        table = _build_quote_table(result, case.get("expected_sheet"))
        results.append({
            "id": case["id"],
            "description": case["description"],
            "passed": passed,
            "pending": pending,
            "failure_reason": failure_reason,
            "expected_mrc": float(expected_mrc) if expected_mrc is not None else None,
            "expected_nrc": float(expected_nrc) if expected_nrc is not None else None,
            "actual_mrc": float(actual_mrc),
            "actual_nrc": float(actual_nrc),
            "errors": result.get("errors", []),
            "quote": quote_json,
            "sheet_vs_db": table,
        })
        _print_quote_breakdown(case["id"], result, table)
    return results


def main():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        print("ERROR: SUPABASE_URL and SUPABASE_KEY must be set in .env")
        sys.exit(1)
    try:
        client = create_client(url, key)
    except Exception as e:
        print(f"ERROR: Could not create Supabase client: {e}")
        sys.exit(1)

    # Run core licensing unit tests first (no Supabase calls inside).
    test_compute_licensed_units()

    print("Running quote E2E tests...")
    results = run_quote_e2e(client)
    passed = sum(1 for r in results if r["passed"])
    print("")
    total = len(results)

    for r in results:
        status = "✓ PASS" if r["passed"] else "✗ FAIL"
        pending_tag = " (PENDING)" if r.get("pending") else ""
        print(f"  {status}  {r['id']}{pending_tag}")
        if not r["passed"]:
            if r.get("failure_reason"):
                print(f"           → {r['failure_reason']}")
            if r.get("expected_mrc") is not None and r.get("expected_nrc") is not None:
                print(f"           expected MRC={r['expected_mrc']} NRC={r['expected_nrc']}")
            print(f"           actual   MRC={r['actual_mrc']} NRC={r['actual_nrc']}")
            if r.get("errors"):
                print(f"           errors: {r['errors']}")

    summary = {
        "run_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "passed": passed,
        "failed": total - passed,
        "total": total,
        "all_passed": passed == total,
        "results": results,
    }
    out_path = OUTPUTS / "quote_e2e_results.json"
    def _json_default(x):
        if isinstance(x, Decimal):
            return float(x)
        raise TypeError(type(x))
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2, default=_json_default)

    print()
    print(f"{'ALL PASSED' if summary['all_passed'] else 'FAILURES FOUND'}  ({passed}/{total})")
    print(f"Results → {out_path}")
    sys.exit(0 if summary["all_passed"] else 1)


if __name__ == "__main__":
    main()
