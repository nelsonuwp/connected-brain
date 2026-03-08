"""
validate_seed.py
-----------------
Runs validation queries against the CPQ Supabase DB after schema + seed are applied.
Writes results to tests/outputs/validation_results.json.

Usage:
    cd projects/cpq-replacement-db-only
    python tests/validate_seed.py

Env vars (same .env as the rest of the project):
    SUPABASE_DB_URL   — full postgres:// connection string (session pooler, port 6543)
                        e.g. postgresql://postgres.xxxx:PASSWORD@aws-1-us-east-1.pooler.supabase.com:6543/postgres

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
from sqlalchemy import create_engine, text

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


def run_query(conn, sql, params=None):
    result = conn.execute(text(sql), params or {})
    cols = list(result.keys())
    rows = [dict(zip(cols, row)) for row in result.fetchall()]
    return rows


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_pro6_cad_pricing(conn):
    rows = run_query(conn, """
        SELECT pp.term_months, pp.mrc, pp.nrc
        FROM product_catalog pc
        JOIN product_pricing pp ON pp.product_id = pc.id
        WHERE pc.sku_name    = :sku
          AND pp.currency_code = 'CAD'
        ORDER BY pp.term_months
    """, {"sku": REFERENCE["pro_6_cad"]["sku"]})

    ref = REFERENCE["pro_6_cad"]["pricing"]
    failures = []
    for row in rows:
        term = row["term_months"]
        if term in ref:
            exp_mrc, exp_nrc = ref[term]
            if row["mrc"] != exp_mrc:
                failures.append(f"term={term} mrc={row['mrc']} expected={exp_mrc}")
            if row["nrc"] != exp_nrc:
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


def test_cluster_atomic_no_por(conn):
    failures = []
    rows_out = {}
    for key in ("cluster_no_por", "atomic_no_por"):
        ref = REFERENCE[key]
        rows = run_query(conn, """
            SELECT sda.dc_code
            FROM product_catalog pc
            JOIN server_dc_availability sda ON sda.server_product_id = pc.id
            WHERE pc.sku_name = :sku
            ORDER BY sda.dc_code
        """, {"sku": ref["sku"]})
        dcs = {r["dc_code"] for r in rows}
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


def test_fx_usd_feb2026(conn):
    ref = REFERENCE["fx_usd_feb2026"]
    rows = run_query(conn, """
        SELECT currency_code, rate_date, rate, rate_type
        FROM fx_rates
        WHERE currency_code = :ccy AND rate_date = :dt
        ORDER BY rate_type
    """, {"ccy": ref["currency"], "dt": ref["date"]})

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


def test_view_capex_math(conn):
    """v_product_capex_cad: capex_cad should = procured_price * rate, not / rate."""
    rows = run_query(conn, """
        SELECT sku_name, procured_price, procured_currency, rate, capex_cad
        FROM v_product_capex_cad
        WHERE procured_currency IS NOT NULL
          AND procured_price IS NOT NULL
          AND procured_currency != 'CAD'
        LIMIT 5
    """)

    failures = []
    for row in rows:
        if row["rate"] and row["procured_price"] and row["capex_cad"]:
            expected = round(float(row["procured_price"]) * float(row["rate"]), 2)
            actual   = round(float(row["capex_cad"]), 2)
            if abs(expected - actual) > 0.10:
                failures.append(
                    f"{row['sku_name']}: {row['procured_price']} × {row['rate']} "
                    f"= {expected} but capex_cad={actual}"
                )

    return {
        "test": "view_capex_math",
        "description": "v_product_capex_cad uses multiply (foreign × rate = CAD), not divide",
        "passed": len(failures) == 0,
        "failures": failures,
        "rows": rows,
        "note": "No rows = procured_price/currency not yet populated in product_catalog (expected at this stage)",
    }


def test_overhead_constants(conn):
    rows = run_query(conn, "SELECT key, value FROM overhead_constants ORDER BY key")
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


def test_pro6_dc_availability(conn):
    ref = REFERENCE["pro6_dcs"]
    rows = run_query(conn, """
        SELECT sda.dc_code
        FROM product_catalog pc
        JOIN server_dc_availability sda ON sda.server_product_id = pc.id
        WHERE pc.sku_name = :sku
        ORDER BY sda.dc_code
    """, {"sku": ref["sku"]})

    actual = {r["dc_code"] for r in rows}
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


def test_tor_power_driver(conn):
    ref = REFERENCE["tor_power"]
    rows = run_query(conn, """
        SELECT dc_code, cost_category, amount, currency_code
        FROM dc_cost_drivers
        WHERE dc_code = :dc AND cost_category = :cat
    """, {"dc": ref["dc"], "cat": ref["category"]})

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


def test_row_counts(conn):
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
        result = run_query(conn, f"SELECT COUNT(*) AS n FROM {table}")
        actual = result[0]["n"]
        passed = actual == exp
        rows.append({"table": table, "expected": exp, "actual": actual, "ok": passed})
        if not passed:
            failures.append(f"{table}: expected {exp}, got {actual}")

    return {
        "test": "row_counts",
        "description": "All seeded tables have expected row counts",
        "passed": len(failures) == 0,
        "failures": failures,
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    db_url = os.getenv("SUPABASE_DB_URL")
    if not db_url:
        print("ERROR: SUPABASE_DB_URL not set in .env")
        sys.exit(1)

    engine = create_engine(db_url, connect_args={"sslmode": "require"})

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
    with engine.connect() as conn:
        for fn in tests:
            try:
                result = fn(conn)
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
        "run_at": datetime.utcnow().isoformat() + "Z",
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
