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
# 1. Pro Series 6.0 - M, default config, CAD, Toronto, 12 mo → MRC 1249, NRC 1249
# 2. Same, 24 mo → MRC 969, NRC 1249
# 3. Same, 36 mo → MRC 829, NRC 1249
# 4. Advanced Series 6.0 - M, base + 2x CPU (Intel Xeon Gold 6526Y) + 2x 1.92 TB drive, LM Basic (included) → MRC 1789, NRC 969
# 5. (User to add more from Excel)
# ---------------------------------------------------------------------------

QUOTE_CASES = [
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
        "mrc_tolerance": MRC_TOLERANCE,  # FX on USD addons
        "nrc_tolerance": NRC_TOLERANCE,
    },
]


def _decimal(n):
    if n is None:
        return Decimal("0")
    return Decimal(str(n))


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
        expected_mrc = case["expected_mrc"]
        expected_nrc = case["expected_nrc"]
        mrc_tol = case.get("mrc_tolerance", Decimal("0"))
        nrc_tol = case.get("nrc_tolerance", Decimal("0"))
        actual_mrc = _decimal(result["totals_mrc"])
        actual_nrc = _decimal(result["totals_nrc"])
        mrc_ok = abs(actual_mrc - expected_mrc) <= mrc_tol
        nrc_ok = abs(actual_nrc - expected_nrc) <= nrc_tol
        passed = mrc_ok and nrc_ok and not result.get("errors")
        results.append({
            "id": case["id"],
            "description": case["description"],
            "passed": passed,
            "expected_mrc": float(expected_mrc),
            "expected_nrc": float(expected_nrc),
            "actual_mrc": float(actual_mrc),
            "actual_nrc": float(actual_nrc),
            "errors": result.get("errors", []),
            "quote": {
                "totals_mrc": float(result["totals_mrc"]),
                "totals_nrc": float(result["totals_nrc"]),
                "line_items_count": len(result["line_items"]),
                "addon_lines_count": len(result.get("addon_lines", [])),
                "has_capex": result.get("capex") is not None,
                "has_overhead": result.get("overhead_breakdown") is not None,
            },
        })
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

    print("Running quote E2E tests...\n")
    results = run_quote_e2e(client)
    passed = sum(1 for r in results if r["passed"])
    total = len(results)

    for r in results:
        status = "✓ PASS" if r["passed"] else "✗ FAIL"
        print(f"  {status}  {r['id']}")
        if not r["passed"]:
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
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2, default=lambda x: float(x) if isinstance(x, Decimal) else x)

    print()
    print(f"{'ALL PASSED' if summary['all_passed'] else 'FAILURES FOUND'}  ({passed}/{total})")
    print(f"Results → {out_path}")
    sys.exit(0 if summary["all_passed"] else 1)


if __name__ == "__main__":
    main()
