"""
extract.py
----------
Pulls dimProductAttributes from the Ocean MSSQL database and writes it to
output/dim_product_attributes.csv for use by merge.py.

Usage:
    python extract.py [--all]

    By default, only pulls active TLS rows (level = 'TLS' AND is_active = '1').
    Pass --all to pull every row (useful for debugging or auditing).

Env vars (in .env at connected-brain root):
    MSSQL_BI_USER, MSSQL_BI_PASS, MSSQL_BI_SERVER, MSSQL_BI_NAME
    (legacy OCEAN_DB_* still accepted by the connector)
"""

import argparse
import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import text

# ---------------------------------------------------------------------------
# Resolve paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent
REPO_ROOT    = PROJECT_ROOT.parent.parent  # connected-brain root
OUTPUT_DIR   = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)
load_dotenv(REPO_ROOT / ".env")

# Add connectors/ to path so the local copy of mssql.py is importable
sys.path.insert(0, str(PROJECT_ROOT / "connectors"))
from mssql import MSSQLConnector  # noqa: E402  (copied from _reference/clients)


# ---------------------------------------------------------------------------
# Query
# ---------------------------------------------------------------------------
QUERY_ACTIVE_TLS = """
    SELECT
        fusion_id,
        sku_name,
        sku_nickname,
        level,
        is_active,
        type,
        service_type,
        category,
        functional_group,
        lifecycle,
        product_group,
        functional_group_bi,
        search_keywords,
        adjusted_line_of_business,
        technology_group,
        product_type,
        product_line,
        product_part,
        vendor,
        product_cost_cad,
        license_cost_cad,
        release_date,
        product,
        product_category,
        product_detail,
        new_lob_2021
    FROM DM_BusinessInsights.dbo.dimProductAttributes
    WHERE level = 'TLS'
      AND is_active = '1'
    ORDER BY fusion_id
"""

QUERY_ALL = """
    SELECT *
    FROM DM_BusinessInsights.dbo.dimProductAttributes
    ORDER BY fusion_id, level
"""


def main():
    parser = argparse.ArgumentParser(description="Extract dimProductAttributes from Ocean DB")
    parser.add_argument("--all", action="store_true", help="Pull all rows, not just active TLS")
    args = parser.parse_args()

    print("Connecting to Ocean DB...")
    connector = MSSQLConnector("OCEAN")

    query = QUERY_ALL if args.all else QUERY_ACTIVE_TLS
    label = "all rows" if args.all else "active TLS rows"

    print(f"Running query ({label})...")
    with connector._engine.connect() as conn:
        result = conn.execute(text(query))
        columns = list(result.keys())
        rows = result.fetchall()

    df = pd.DataFrame(rows, columns=columns)
    print(f"  Fetched {len(df):,} rows, {len(df.columns)} columns")

    # Basic normalisation
    df["fusion_id"] = df["fusion_id"].astype(str).str.strip()
    df["sku_name"]  = df["sku_name"].astype(str).str.strip()

    out_path = OUTPUT_DIR / "dim_product_attributes.csv"
    df.to_csv(out_path, index=False)
    print(f"  Written → {out_path}")

    # Quick summary
    if not args.all:
        lob_counts = df["adjusted_line_of_business"].value_counts()
        print("\nRow counts by adjusted_line_of_business:")
        for lob, count in lob_counts.items():
            print(f"  {lob or '(blank)':<40} {count:>5}")

    connector.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
