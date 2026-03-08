"""
generate_seed.py
----------------
Reads the merged product data (output/merged_products.csv) and all CPQ
extracted CSVs, then writes output/seed_data.sql ready to run against
a Postgres / Supabase instance that already has schema.sql applied.

Run order:
    1. python extract.py
    2. python merge.py          (review merge_report.csv before continuing)
    3. python generate_seed.py

Usage:
    python generate_seed.py [--skip-unmatched] [--dry-run]

    --skip-unmatched    Exclude TEMP- rows from seed output (strict mode)
    --dry-run           Print row counts but do not write seed_data.sql

Warnings:
    - Rows with match_confidence = 'fuzzy' are included but flagged in a
      SQL comment so you can grep for them in the output.
    - Rows with match_confidence = 'unmatched' generate TEMP- fusion_ids
      AND insert a row into pending_fusion_id automatically.
"""

import argparse
import json
import math
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR   = PROJECT_ROOT / "output"
CPQ_DIR      = PROJECT_ROOT / "cpq-extracted"

OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# SQL helpers
# ---------------------------------------------------------------------------

class RawSQL:
    """Wrapper for SQL expressions that should not be quoted (e.g. subselects)."""
    def __init__(self, expr: str):
        self.expr = expr

    def __str__(self):
        return self.expr


def subselect(table: str, col: str, val: str) -> RawSQL:
    """Return a subselect expression for FK lookups."""
    return RawSQL(f"(SELECT id FROM {table} WHERE {col} = '{val}')")


def sql_val(v) -> str:
    """Render a Python value as a SQL literal."""
    if isinstance(v, RawSQL):
        return str(v)
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "NULL"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    # Escape single quotes
    return "'" + str(v).replace("'", "''") + "'"


def insert(table: str, row: dict, comment: str = None) -> str:
    cols = ", ".join(row.keys())
    vals = ", ".join(sql_val(v) for v in row.values())
    comment_str = f"  -- {comment}" if comment else ""
    return f"INSERT INTO {table} ({cols}) VALUES ({vals});{comment_str}"


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_merged() -> pd.DataFrame:
    path = OUTPUT_DIR / "merged_products.csv"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found — run merge.py first.")
    return pd.read_csv(path)


def load_csv(filename: str) -> pd.DataFrame:
    path = CPQ_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"{path} not found.")
    return pd.read_csv(path)


def load_json(filename: str) -> dict:
    path = CPQ_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"{path} not found.")
    with open(path) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Section generators
# ---------------------------------------------------------------------------

def section(title: str) -> str:
    bar = "-" * 77
    return f"\n-- {bar}\n-- {title}\n-- {bar}\n"


def gen_fx_rates(lines: list) -> None:
    lines.append(section("FX RATES (ocean → spot; budget rates need manual backfill)"))
    lines.append("-- Rate direction: units of foreign currency per 1 CAD")
    lines.append("-- 1 CAD = rate USD  |  CAD→foreign: × rate  |  foreign→CAD: ÷ rate")
    lines.append("-- NOTE: 'ocean' rate type removed — Finance confirmed spot = quote rate.\n")

    fx_path = CPQ_DIR / "10_fx_rates.csv"
    if not fx_path.exists():
        lines.append("-- WARNING: 10_fx_rates.csv not found — fx_rates table not seeded.")
        lines.append("-- Add spot and budget rates manually before production go-live.\n")
        return

    df = pd.read_csv(fx_path)

    if df.empty:
        lines.append("-- WARNING: 10_fx_rates.csv is empty — fx_rates table not seeded.\n")
        return

    # Normalise: drop 'ocean', rename to 'spot' if present; keep 'budget'
    type_map = {"ocean": "spot", "spot": "spot", "budget": "budget"}

    seen = set()
    for _, row in df.iterrows():
        raw_type = str(row.get("rate_type", "")).strip().lower()
        rate_type = type_map.get(raw_type)
        if rate_type is None:
            continue
        currency = str(row.get("currency_code", "")).strip().upper()
        if not currency or currency == "CAD":
            continue  # CAD is root; never inserted. Skip blank rows.

        key = (currency, rate_type)
        if key in seen:
            continue
        seen.add(key)

        rate = row.get("rate")
        rate_date = row.get("rate_date", "2026-01-01")

        lines.append(insert("fx_rates", {
            "currency_code": currency,
            "rate_type":     rate_type,
            "rate_date":     rate_date,
            "rate":          rate,
            "notes":         f"Seeded from CPQ v28 extraction; original type was '{raw_type}'",
        }))

    lines.append("\n-- TODO: backfill 12+ months of 'budget' rates for CapEx CAD derivation.")


def gen_product_catalog(lines: list, merged: pd.DataFrame, skip_unmatched: bool) -> dict:
    """
    Insert product_catalog rows for TLS servers.
    Returns a dict: sku_name → catalog_id placeholder string for FK references.
    """
    lines.append(section("PRODUCT CATALOG — TLS Servers"))
    lines.append("-- fusion_id is the external anchor. TEMP- values tracked in pending_fusion_id.\n")

    sku_to_var = {}  # sku_name → postgres variable name (used in FK inserts)

    for i, (_, row) in enumerate(merged.iterrows(), start=1):
        confidence = str(row.get("match_confidence", "unmatched"))

        if skip_unmatched and confidence == "unmatched":
            lines.append(f"-- SKIPPED (unmatched, --skip-unmatched): {row['sku_name']}")
            continue

        fusion_id = str(row.get("fusion_id", "")).strip()
        sku_name  = str(row["sku_name"]).strip()

        comment = None
        if confidence == "fuzzy":
            score = row.get("fuzzy_score", "?")
            matched = row.get("matched_dim_sku", "?")
            comment = f"FUZZY MATCH (score={score}) against '{matched}' — verify before prod"
        elif confidence == "unmatched":
            comment = f"UNMATCHED — TEMP- placeholder; resolve fusion_id before prod go-live"

        # Lifecycle dates from dim (may be blank for new products)
        lines.append(insert("product_catalog", {
            "fusion_id":         fusion_id,
            "sku_name":          sku_name,
            "sku_nickname":      row.get("sku_nickname") or None,
            "product_type_code": "server",
            "level":             "TLS",
            "vendor":            row.get("dim_vendor") or "Dell",
            "is_active":         True,
            "notes":             f"Seeded from CPQ v28; match_confidence={confidence}",
        }, comment=comment))

    return sku_to_var


def gen_pending_fusion_ids(lines: list, merged: pd.DataFrame) -> None:
    unmatched = merged[merged["match_confidence"] == "unmatched"]
    if unmatched.empty:
        return

    lines.append(section("PENDING FUSION IDs — TEMP- placeholders"))
    lines.append("-- These rows must be resolved before production go-live.\n")

    for _, row in unmatched.iterrows():
        sku_name = str(row["sku_name"]).strip()
        fusion_id = str(row.get("fusion_id", "")).strip()
        lines.append(insert("pending_fusion_id", {
            "product_id":     subselect("product_catalog", "fusion_id", fusion_id),
            "placeholder_id": fusion_id,
            "sku_name":       sku_name,
            "reason":         "Product not yet formally released; fusion_id pending assignment",
        }))


def gen_server_specs(lines: list, merged: pd.DataFrame) -> None:
    lines.append(section("SERVER SPECS"))
    lines.append("-- is_promo and min_contract_months set based on CPQ v28 business rules.\n")

    for _, row in merged.iterrows():
        fusion_id = str(row.get("fusion_id", "")).strip()

        is_promo = "promo" in str(row.get("sku_name", "")).lower()
        # Read is_vhost directly from the CSV boolean column
        is_vhost = bool(row.get("is_vhost", False))

        lines.append(insert("server_specs", {
            "product_id":           subselect("product_catalog", "fusion_id", fusion_id),
            "drive_bays":           row.get("drive_bays") or None,
            "default_cpu_qty":      row.get("default_cpu_qty") or None,
            "is_vhost":             is_vhost,
            "is_promo":             is_promo,
            "min_contract_months":  12 if is_promo else None,
            "allow_customization":  not is_promo,
        }))


def gen_pricing(lines: list, merged: pd.DataFrame) -> None:
    lines.append(section("PRODUCT PRICING — Server MRC/NRC"))
    lines.append("-- term_months: 0=MTM, 12, 24, 36. Flat rates — NOT multipliers.\n")

    # Columns in 01_servers.csv (new naming convention)
    # mrc_mtm_*, mrc_12m_*, mrc_24m_*, mrc_36m_*, nrc_*
    currency_term_cols = {
        "USD": {0:  ("mrc_mtm_usd", "nrc_usd"), 12: ("mrc_12m_usd", "nrc_usd"),
                24: ("mrc_24m_usd", "nrc_usd"), 36: ("mrc_36m_usd", "nrc_usd")},
        "CAD": {0:  ("mrc_mtm_cad", "nrc_cad"), 12: ("mrc_12m_cad", "nrc_cad"),
                24: ("mrc_24m_cad", "nrc_cad"), 36: ("mrc_36m_cad", "nrc_cad")},
        "GBP": {0:  ("mrc_mtm_gbp", "nrc_gbp"), 12: ("mrc_12m_gbp", "nrc_gbp"),
                24: ("mrc_24m_gbp", "nrc_gbp"), 36: ("mrc_36m_gbp", "nrc_gbp")},
    }

    for _, row in merged.iterrows():
        fusion_id = str(row.get("fusion_id", "")).strip()
        product_ref = subselect("product_catalog", "fusion_id", fusion_id)

        for currency, terms in currency_term_cols.items():
            for term_months, (mrc_col, nrc_col) in terms.items():
                mrc = row.get(mrc_col)
                nrc = row.get(nrc_col)

                # Skip rows where the column doesn't exist in this CSV at all
                if mrc_col not in row.index and nrc_col not in row.index:
                    continue

                mrc_val = mrc if (mrc is not None and pd.notna(mrc)) else None
                nrc_val = nrc if (nrc is not None and pd.notna(nrc)) else None

                # Skip entirely if both are NULL — no pricing to seed
                if mrc_val is None and nrc_val is None:
                    continue

                lines.append(insert("product_pricing", {
                    "product_id":     product_ref,
                    "currency_code":  currency,
                    "term_months":    term_months,
                    "mrc":            mrc_val,
                    "nrc":            nrc_val,
                    "pricing_model":  "flat",
                }))


def gen_dc_availability(lines: list) -> None:
    lines.append(section("SERVER DC AVAILABILITY"))
    df = load_csv("02_server_dc_availability.csv")
    for _, row in df.iterrows():
        sku = str(row.get("sku_name", "")).strip()
        dc  = str(row.get("dc_code", "")).strip().upper()
        lines.append(insert("server_dc_availability", {
            "server_product_id": subselect("product_catalog", "sku_name", sku),
            "dc_code":           dc,
        }))


def gen_dc_cost_drivers(lines: list) -> None:
    lines.append(section("DC COST DRIVERS"))
    df = load_csv("08_dc_cost_drivers.csv")
    for _, row in df.iterrows():
        lines.append(insert("dc_cost_drivers", {
            "dc_code":       str(row.get("dc_code", "")).strip().upper(),
            "cost_category": row.get("cost_category"),
            "amount":        row.get("amount"),
            "currency_code": str(row.get("currency_code", "USD")).strip().upper(),
            "notes":         row.get("notes") or None,
        }))


def gen_overhead_constants(lines: list) -> None:
    lines.append(section("OVERHEAD CONSTANTS — update from 09_overhead_constants.json"))
    lines.append("-- Schema already seeds defaults. This block updates with CPQ v28 values.\n")
    constants = load_json("09_overhead_constants.json")
    for key, value in constants.items():
        lines.append(
            f"INSERT INTO overhead_constants (key, value, description) "
            f"VALUES ({sql_val(key)}, {sql_val(value)}, 'From CPQ v28 extraction') "
            f"ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate seed_data.sql from merged CPQ data")
    parser.add_argument("--skip-unmatched", action="store_true",
                        help="Exclude TEMP- rows from output")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show counts only; do not write output file")
    args = parser.parse_args()

    print("Loading merged products...")
    merged = load_merged()

    confidence_counts = merged["match_confidence"].value_counts()
    print(f"  exact:     {confidence_counts.get('exact', 0)}")
    print(f"  fuzzy:     {confidence_counts.get('fuzzy', 0)}")
    print(f"  unmatched: {confidence_counts.get('unmatched', 0)}")

    if confidence_counts.get("fuzzy", 0) > 0:
        print("\nWARNING: fuzzy-matched rows are included.")
        print("  Review merge_report.csv and update match_confidence before treating as final.\n")

    lines = [
        "-- =============================================================",
        "-- CPQ Replacement — Seed Data",
        "-- Generated by generate_seed.py",
        "-- Apply AFTER schema.sql: psql -f schema.sql && psql -f seed_data.sql",
        "-- =============================================================",
        "\nBEGIN;",
    ]

    gen_fx_rates(lines)
    gen_product_catalog(lines, merged, args.skip_unmatched)
    gen_pending_fusion_ids(lines, merged)
    gen_server_specs(lines, merged)
    gen_pricing(lines, merged)
    gen_dc_availability(lines)
    gen_dc_cost_drivers(lines)
    gen_overhead_constants(lines)

    lines.append("\nCOMMIT;")
    lines.append("\n-- Run validation.md queries to confirm correctness.")

    sql = "\n".join(lines)

    if args.dry_run:
        print("--dry-run: SQL not written.")
        print(f"  Approximate line count: {len(lines)}")
        return

    out_path = OUTPUT_DIR / "seed_data.sql"
    out_path.write_text(sql, encoding="utf-8")
    print(f"\nWritten → {out_path}")
    print("Next step: psql -f schema.sql && psql -f output/seed_data.sql")
    print("Then run validation queries from validation.md.")


if __name__ == "__main__":
    main()
