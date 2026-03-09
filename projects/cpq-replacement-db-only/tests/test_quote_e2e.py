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

QUOTE_CASES = [
    # --- Locked (values from user) ---
    {
        "id": "pro6m_cad_tor_12m",
        "description": "Pro Series 6.0 - M, default config, CAD, Toronto, 12 mo",
        "server_sku": "Pro Series 6.0 - M",
        "addons": [],
        "currency": "CAD",
        "dc_code": "TOR",
        "term_months": 12,
        "expected_mrc": Decimal("1249"),
        "expected_nrc": Decimal("1249"),
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
            # Capex
            "capex_server_usd": 7569,
            "capex_addons_cad": 1296,
            # Overhead
            "watts": 400,
            "power_monthly_cad": 87.31,
            "network_cad": 58.33,
            "billing_cad": 4.63,
            "supply_chain_cad": 6.35,
            "dc_ops_cad": 6.76,
            "support_cad": 40.14,
            "colo_cad": 17.79,
            # 12m financial
            "revenue_12m": 19597,
            "cost_capex_12m": 10332.44,
            "cost_overhead_12m": 3143.28,
            "margin_12m": 4777,
            "margin_pct": 41.0,
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


def _build_sheet_vs_db(quote: dict, expected_sheet: dict) -> list[dict]:
    """Build Sheet vs DB comparison rows from quote output and expected_sheet (from CPQ screenshot)."""
    rows = []
    # Server Capex
    if expected_sheet.get("capex_server_usd") is not None and quote.get("capex", {}).get("server"):
        db_val = quote["capex"]["server"].get("amount")
        db_curr = quote["capex"]["server"].get("currency", "USD")
        rows.append({
            "item": "Capex (server)",
            "expected": expected_sheet["capex_server_usd"],
            "expected_unit": "USD",
            "db": float(db_val) if db_val is not None else None,
            "db_unit": db_curr,
        })
    # Watts
    if expected_sheet.get("watts") is not None and quote.get("overhead_breakdown"):
        db_val = quote["overhead_breakdown"].get("total_watts")
        rows.append({
            "item": "Watts",
            "expected": expected_sheet["watts"],
            "expected_unit": "W",
            "db": db_val,
            "db_unit": "W",
        })
    # power_per_kw rate ($/kW) if provided
    if expected_sheet.get("power_per_kw_rate_cad") is not None and quote.get("overhead_breakdown"):
        db_val = quote["overhead_breakdown"].get("power_per_kw_rate")
        db_curr = quote["overhead_breakdown"].get("power_per_kw_rate_currency", "")
        rows.append({
            "item": "power_per_kw (rate)",
            "expected": expected_sheet["power_per_kw_rate_cad"],
            "expected_unit": "CAD",
            "db": float(db_val) if db_val is not None else None,
            "db_unit": db_curr,
        })
    # Power monthly cost (sheet "Driven by Power Usage - Power" = 87.31 CAD)
    if expected_sheet.get("power_monthly_cad") is not None and quote.get("overhead_breakdown"):
        power_cat = next(
            (b for b in quote["overhead_breakdown"].get("by_category", []) if "power" in b.get("category", "").lower()),
            None,
        )
        db_val = float(power_cat["amount"]) if power_cat else None
        db_curr = power_cat["currency"] if power_cat else ""
        rows.append({
            "item": "Power (monthly)",
            "expected": expected_sheet["power_monthly_cad"],
            "expected_unit": "CAD",
            "db": db_val,
            "db_unit": db_curr,
        })
    return rows


def _print_quote_breakdown(case_id: str, quote: dict, *, sheet_vs_db: list | None = None) -> None:
    """Print component and overhead breakdown for one case."""
    print(f"\n  --- {case_id} (component + overhead) ---")
    print("  Line items:")
    for li in quote["line_items"]:
        print(f"    {li['sku']} x{li['quantity']}  MRC {li['mrc']}  NRC {li['nrc']} {quote.get('currency', '')}")
    if quote.get("addon_lines"):
        print("  Add-on breakdown:")
        for a in quote["addon_lines"]:
            print(f"    {a['sku']} x{a['quantity']}  unit MRC {a['unit_mrc']}  →  MRC {a['mrc']}  NRC {a['nrc']}")
    if quote.get("capex"):
        c = quote["capex"]
        if c.get("server"):
            s = c["server"]
            print(f"  CapEx server: {s.get('sku')}  {s.get('amount')} {s.get('currency')}")
        for a in c.get("addons", []):
            print(f"  CapEx addon: {a.get('sku')} x{a.get('quantity', 1)}  {a.get('amount')} {a.get('currency')}")
    if quote.get("overhead_breakdown"):
        o = quote["overhead_breakdown"]
        print(f"  Overhead: {o.get('dc_code')}  wattage {o.get('total_watts')} W ({o.get('total_kw')} kW)")
        if o.get("power_per_kw_rate") is not None:
            print(f"    power_per_kw rate: {o['power_per_kw_rate']} {o.get('power_per_kw_rate_currency', '')}")
        for b in o.get("by_category", []):
            print(f"    {b['category']}: {b['amount']} {b['currency']}")
        print("    Constants: " + ", ".join(f"{k}={v}" for k, v in o.get("overhead_constants", {}).items()))
    if quote.get("financial_summary_12m"):
        f = quote["financial_summary_12m"]
        print("  12-month financial summary:")
        print(f"    Revenue (12m): {f['currency']} {f['revenue_12m']}  |  Capex: {f['currency']} {f['cost_capex']}  |  Overhead (12m): {f['currency']} {f['cost_overhead_12m']}")
        print(f"    Margin (12m): {f['currency']} {f['margin_12m']}  ({f['margin_pct']}%)")
    if sheet_vs_db:
        print("  Sheet vs DB:")
        for row in sheet_vs_db:
            print(f"    {row['item']}:  Expected {row['expected']} {row['expected_unit']}  |  DB {row['db']} {row['db_unit']}")


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
        sheet_vs_db = None
        if case.get("expected_sheet"):
            sheet_vs_db = _build_sheet_vs_db(result, case["expected_sheet"])
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
            "sheet_vs_db": sheet_vs_db,
        })
        _print_quote_breakdown(case["id"], result, sheet_vs_db=sheet_vs_db)
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
