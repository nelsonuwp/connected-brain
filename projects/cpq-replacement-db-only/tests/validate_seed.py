"""
validate_seed.py
-----------------
Runs validation queries against the CPQ Supabase DB after schema + seed are applied.
Writes results to tests/outputs/validation_results.json.

Usage:
    cd projects/cpq-replacement-db-only
    python tests/validate_seed.py

Env vars (same .env as the rest of the project):
    SUPABASE_URL   — project REST URL, e.g. https://xxxx.supabase.co
    SUPABASE_KEY   — anon key (or service-role key if RLS blocks anon reads)

Exit codes:
    0 — all assertions passed
    1 — one or more assertions failed (see JSON output for details)
"""

import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent.parent.parent.parent  # tests/ -> cpq-replacement-db-only/ -> projects/ -> connected-brain/
OUTPUTS = Path(__file__).parent / "outputs"
OUTPUTS.mkdir(parents=True, exist_ok=True)

load_dotenv(ROOT / ".env")

# ---------------------------------------------------------------------------
# CPQ v28 reference values — update here if CPQ changes
# These are the ground-truth numbers pulled directly from Products-Hosting
# and Model-Drivers in CPQ_v28_0_.xlsm
# ---------------------------------------------------------------------------
REFERENCE = {
    # Products-Hosting: Pro Series 6.0 - M, CAD pricing column
    "pro_6_cad": {
        "sku": "Pro Series 6.0 - M",
        "currency": "CAD",
        "pricing": {0: (1249.0, 1249.0), 12: (1249.0, 1249.0), 24: (969.0, 1249.0), 36: (829.0, 1249.0)},
        # key = term_months, value = (mrc, nrc)
    },
    # Server Data: Cluster and Atomic should NOT have POR
    "cluster_no_por": {"sku": "Cluster 5.0 (Dell R440)", "forbidden_dc": "POR"},
    "atomic_no_por":  {"sku": "Atomic 5.0 (Dell R650xs)", "forbidden_dc": "POR"},
    # Bank of Canada Feb 2026 monthly average
    "fx_usd_feb2026": {"currency": "USD", "date": "2026-02-01", "rate": 1.3651},
    # Overhead: 8 rows, spot-check 3 key values
    "overhead": {
        "expected_count": 8,
        "spot_checks": {
            "sga_pct": 0.082,                  # within 0.001 tolerance
            "annual_cost_inflation": 0.03,
            "capital_intensity_threshold": 0.5,
        },
    },
    # DC availability: Pro Series 6.0 - M should have all 6 DCs
    "pro6_dcs": {
        "sku": "Pro Series 6.0 - M",
        "expected_dcs": {"ATL", "MIA", "LAX", "IAD", "TOR", "POR"},
    },
    # DC cost drivers: TOR power should be CAD ~218.27
    "tor_power": {"dc": "TOR", "category": "power_per_kw", "expected": 218.27, "currency": "CAD"},
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def json_serial(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


# ---------------------------------------------------------------------------
# Tests  (each receives `client` — a supabase.Client)
# ---------------------------------------------------------------------------
def test_row_counts(client):
    """Sanity check expected row counts for every seeded table."""
    expected = {
        "fx_rates":               330,
        "product_catalog":         18,
        "server_specs":            18,
        "product_pricing":        204,
        "server_dc_availability":  88,
        "dc_cost_drivers":         54,
        "overhead_constants":       8,
        "pending_fusion_id":        2,
    }
    rows = []
    failures = []
    for table, exp in expected.items():
        resp = client.table(table).select("*", count="exact").limit(0).execute()
        actual = resp.count
        ok = actual == exp
        rows.append({"table": table, "expected": exp, "actual": actual, "ok": ok})
        if not ok:
            failures.append(f"{table}: expected {exp}, got {actual}")

    return {
        "test": "row_counts",
        "description": "All seeded tables have expected row counts",
        "passed": len(failures) == 0,
        "failures": failures,
        "rows": rows,
    }


def test_pro6_cad_pricing(client):
    sku = REFERENCE["pro_6_cad"]["sku"]
    resp = (
        client.table("product_pricing")
        .select("term_months, mrc, nrc, product_catalog!inner(sku_name)")
        .eq("product_catalog.sku_name", sku)
        .eq("currency_code", "CAD")
        .order("term_months")
        .execute()
    )
    rows = [{"term_months": r["term_months"], "mrc": r["mrc"], "nrc": r["nrc"]} for r in resp.data]

    ref = REFERENCE["pro_6_cad"]["pricing"]
    failures = []
    for row in rows:
        term = row["term_months"]
        if term in ref:
            exp_mrc, exp_nrc = ref[term]
            if float(row["mrc"]) != exp_mrc:
                failures.append(f"term={term} mrc={row['mrc']} expected={exp_mrc}")
            if float(row["nrc"]) != exp_nrc:
                failures.append(f"term={term} nrc={row['nrc']} expected={exp_nrc}")
        else:
            failures.append(f"Unexpected term_months={term} in result")

    missing = [t for t in ref if t not in {r["term_months"] for r in rows}]
    if missing:
        failures.append(f"Missing term_months rows: {missing}")

    return {
        "test": "pro6_cad_pricing",
        "description": "Pro Series 6.0 - M CAD pricing matches CPQ v28 Products-Hosting",
        "passed": len(failures) == 0,
        "failures": failures,
        "rows": rows,
    }


def test_cluster_atomic_no_por(client):
    failures = []
    rows_out = {}
    for key in ("cluster_no_por", "atomic_no_por"):
        ref = REFERENCE[key]
        resp = (
            client.table("server_dc_availability")
            .select("dc_code, product_catalog!inner(sku_name)")
            .eq("product_catalog.sku_name", ref["sku"])
            .order("dc_code")
            .execute()
        )
        dcs = {r["dc_code"] for r in resp.data}
        rows_out[ref["sku"]] = sorted(dcs)
        if ref["forbidden_dc"] in dcs:
            failures.append(f"{ref['sku']} has {ref['forbidden_dc']} — should be NA-only hardware")

    return {
        "test": "cluster_atomic_no_por",
        "description": "Cluster 5.0 and Atomic 5.0 must NOT be available in POR (NA hardware only)",
        "passed": len(failures) == 0,
        "failures": failures,
        "rows": rows_out,
    }


def test_fx_usd_feb2026(client):
    ref = REFERENCE["fx_usd_feb2026"]
    resp = (
        client.table("fx_rates")
        .select("currency_code, rate_date, rate, rate_type")
        .eq("currency_code", ref["currency"])
        .eq("rate_date", ref["date"])
        .order("rate_type")
        .execute()
    )
    rows = resp.data

    failures = []
    if not rows:
        failures.append(f"No row found for USD {ref['date']}")
    else:
        spot = next((r for r in rows if r["rate_type"] == "spot"), None)
        if not spot:
            failures.append("No 'spot' row found")
        elif abs(float(spot["rate"]) - ref["rate"]) > 0.0001:
            failures.append(f"rate={spot['rate']} expected={ref['rate']}")

    return {
        "test": "fx_usd_feb2026",
        "description": "USD Feb 2026 spot rate matches Bank of Canada (1.3651)",
        "passed": len(failures) == 0,
        "failures": failures,
        "rows": rows,
    }


def test_view_capex_math(client):
    """v_product_capex_cad: procured_price_cad should = procured_price * fx_budget_rate_used."""
    resp = (
        client.table("v_product_capex_cad")
        .select("product_id, procured_price, procured_currency, fx_budget_rate_used, procured_price_cad")
        .not_.is_("procured_currency", "null")
        .not_.is_("procured_price", "null")
        .neq("procured_currency", "CAD")
        .limit(5)
        .execute()
    )
    rows = resp.data

    failures = []
    for row in rows:
        if row["fx_budget_rate_used"] and row["procured_price"] and row["procured_price_cad"]:
            expected = round(float(row["procured_price"]) * float(row["fx_budget_rate_used"]), 2)
            actual   = round(float(row["procured_price_cad"]), 2)
            if abs(expected - actual) > 0.10:
                failures.append(
                    f"product_id={row['product_id']}: {row['procured_price']} × {row['fx_budget_rate_used']} "
                    f"= {expected} but procured_price_cad={actual}"
                )

    return {
        "test": "view_capex_math",
        "description": "v_product_capex_cad uses multiply (foreign × rate = CAD), not divide",
        "passed": len(failures) == 0,
        "failures": failures,
        "rows": rows,
        "note": "No rows = procured_price/currency not yet populated in product_catalog (expected at this stage)",
    }


def test_overhead_constants(client):
    resp = (
        client.table("overhead_constants")
        .select("key, value")
        .order("key")
        .execute()
    )
    rows = resp.data
    kv = {r["key"]: float(r["value"]) for r in rows}

    failures = []
    if len(rows) != REFERENCE["overhead"]["expected_count"]:
        failures.append(f"Expected {REFERENCE['overhead']['expected_count']} rows, got {len(rows)}")

    for key, expected in REFERENCE["overhead"]["spot_checks"].items():
        if key not in kv:
            failures.append(f"Missing key: {key}")
        elif abs(kv[key] - expected) > 0.001:
            failures.append(f"{key}={kv[key]} expected≈{expected}")

    return {
        "test": "overhead_constants",
        "description": "8 overhead rows present; sga_pct, inflation, capital_intensity match CPQ v28",
        "passed": len(failures) == 0,
        "failures": failures,
        "rows": rows,
    }


def test_pro6_dc_availability(client):
    ref = REFERENCE["pro6_dcs"]
    resp = (
        client.table("server_dc_availability")
        .select("dc_code, product_catalog!inner(sku_name)")
        .eq("product_catalog.sku_name", ref["sku"])
        .order("dc_code")
        .execute()
    )
    actual = {r["dc_code"] for r in resp.data}
    missing = ref["expected_dcs"] - actual
    extra   = actual - ref["expected_dcs"]
    failures = []
    if missing: failures.append(f"Missing DCs: {sorted(missing)}")
    if extra:   failures.append(f"Unexpected DCs: {sorted(extra)}")

    return {
        "test": "pro6_dc_availability",
        "description": "Pro Series 6.0 - M available in all 6 DCs (ATL MIA LAX IAD TOR POR)",
        "passed": len(failures) == 0,
        "failures": failures,
        "rows": sorted(actual),
    }


def test_tor_power_driver(client):
    ref = REFERENCE["tor_power"]
    resp = (
        client.table("dc_cost_drivers")
        .select("dc_code, cost_category, amount, currency_code")
        .eq("dc_code", ref["dc"])
        .eq("cost_category", ref["category"])
        .execute()
    )
    rows = resp.data

    failures = []
    if not rows:
        failures.append(f"No row found for {ref['dc']} / {ref['category']}")
    else:
        row = rows[0]
        if row["currency_code"] != ref["currency"]:
            failures.append(f"currency={row['currency_code']} expected={ref['currency']}")
        if abs(float(row["amount"]) - ref["expected"]) > 0.01:
            failures.append(f"amount={row['amount']} expected≈{ref['expected']}")

    return {
        "test": "tor_power_driver",
        "description": "TOR power_per_kw ≈ 218.27 CAD (highest-cost NA DC)",
        "passed": len(failures) == 0,
        "failures": failures,
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        print("ERROR: SUPABASE_URL and SUPABASE_KEY must be set in .env")
        print("  SUPABASE_URL  — https://<project-ref>.supabase.co")
        print("  SUPABASE_KEY  — anon key from Dashboard → API Settings")
        sys.exit(1)

    try:
        client = create_client(url, key)
    except Exception as e:
        print(f"ERROR: Could not create Supabase client: {e}")
        sys.exit(1)

    tests = [
        test_row_counts,
        test_pro6_cad_pricing,
        test_cluster_atomic_no_por,
        test_fx_usd_feb2026,
        test_view_capex_math,
        test_overhead_constants,
        test_pro6_dc_availability,
        test_tor_power_driver,
    ]

    results = []
    for fn in tests:
        try:
            result = fn(client)
        except Exception as e:
            result = {
                "test": fn.__name__,
                "passed": False,
                "failures": [f"Exception: {e}"],
                "rows": [],
            }
        status = "✓ PASS" if result["passed"] else "✗ FAIL"
        print(f"  {status}  {result['test']}")
        if result["failures"]:
            for f in result["failures"]:
                print(f"           → {f}")
        results.append(result)

    passed = sum(1 for r in results if r["passed"])
    total  = len(results)
    summary = {
        "run_at": datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"),
        "passed": passed,
        "failed": total - passed,
        "total":  total,
        "all_passed": passed == total,
        "tests": results,
    }

    out_path = OUTPUTS / "validation_results.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2, default=json_serial)

    print()
    print(f"{'ALL PASSED' if summary['all_passed'] else 'FAILURES FOUND'}  ({passed}/{total})")
    print(f"Results written to {out_path}")

    sys.exit(0 if summary["all_passed"] else 1)


if __name__ == "__main__":
    main()
