"""
sku_matcher.py
--------------
Lives in:  cpq-replacement-db-only/scripts/sku_matcher.py
Connector: cpq-replacement-db-only/connectors/mssql.py   (../connectors)
.env:      connected-brain/.env                           (../../../.env rel. to this file)

Matches Product SKUs from Hosting_SKUs.xlsx against dimProductAttributes
(loaded from CSV export or live MSSQL via mssql.py).

Output columns:
    product_sku   – from Hosting_SKUs.xlsx
    fusion_id     – from dimProductAttributes
    sku_name      – from dimProductAttributes
    match_type    – "direct", "fuzzy", or "no_match"
    fuzzy_score   – 0-100 (100 = exact after normalisation; blank for direct)

Usage
-----
# From CSV export (default – no DB connection needed):
    python scripts/sku_matcher.py

# From live MSSQL (reads OCEAN_* vars from connected-brain/.env):
    python scripts/sku_matcher.py --live

Tuning
------
FUZZY_THRESHOLD  : minimum score (0-100) to accept a fuzzy match (default 65)
"""

import argparse
import csv
import difflib
import os
import re
import sys
from pathlib import Path

import openpyxl

# ---------------------------------------------------------------------------
# PATHS  (all resolved relative to this file so the script runs from anywhere)
# ---------------------------------------------------------------------------

SCRIPT_DIR   = Path(__file__).resolve().parent          # .../scripts/
PROJECT_ROOT = SCRIPT_DIR.parent                        # .../cpq-replacement-db-only/
CONNECTORS   = PROJECT_ROOT / "connectors"              # .../connectors/
ENV_FILE     = PROJECT_ROOT.parent.parent / ".env"      # .../connected-brain/.env

# Default I/O  (override via CLI args if needed)
HOSTING_SKUS_FILE = PROJECT_ROOT / "Hosting_SKUs.xlsx"
DIM_PRODUCT_CSV   = PROJECT_ROOT / "dimProductAttributes_202603100849.csv"
OUTPUT_FILE       = PROJECT_ROOT / "output" / "sku_matches.csv"

FUZZY_THRESHOLD    = 65   # 0-100; lower = more permissive fuzzy matches
SHEET_NAME         = "Hosting SKUs"
SKU_COL_IDX        = 2    # 0-based: column C = "Product SKU"


# ---------------------------------------------------------------------------
# NORMALISATION
# ---------------------------------------------------------------------------

def normalise(text: str) -> str:
    """
    Lowercase, collapse whitespace, remove punctuation noise.
    Treats ' - ', '-', and spaces interchangeably so that
    'Pro Series 6.0 - vHost'  ==  'Pro Series 6.0 vHost'.
    """
    t = text.lower().strip()
    t = re.sub(r"\s*-\s*", " ", t)          # dash/hyphen → space
    t = re.sub(r"[^\w\s\.]", " ", t)        # drop other punctuation
    t = re.sub(r"\s+", " ", t).strip()
    return t


def token_sort(text: str) -> str:
    """Sort tokens alphabetically – helps with word-order differences."""
    return " ".join(sorted(normalise(text).split()))


# ---------------------------------------------------------------------------
# FUZZY SCORE (0-100)
# ---------------------------------------------------------------------------

def similarity(a: str, b: str) -> float:
    """
    Returns the best of:
      • plain normalised ratio
      • token-sort ratio  (handles reordered words)
    Result is 0-100.
    """
    na, nb = normalise(a), normalise(b)
    plain = difflib.SequenceMatcher(None, na, nb).ratio() * 100

    ta, tb = token_sort(a), token_sort(b)
    tsort = difflib.SequenceMatcher(None, ta, tb).ratio() * 100

    return round(max(plain, tsort), 1)


# ---------------------------------------------------------------------------
# DATA LOADERS
# ---------------------------------------------------------------------------

def load_hosting_skus(path: str) -> list[str]:
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[SHEET_NAME]
    skus = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        val = row[SKU_COL_IDX]
        if val and str(val).strip():
            skus.append(str(val).strip())
    return skus


def load_dim_from_csv(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_dim_from_mssql() -> list[dict]:
    """
    Loads OCEAN_* env vars from connected-brain/.env, then connects via
    cpq-replacement-db-only/connectors/mssql.py.
    """
    # Load .env (graceful – won't crash if python-dotenv isn't installed)
    if ENV_FILE.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(dotenv_path=ENV_FILE)
            print(f"  Loaded env from: {ENV_FILE}")
        except ImportError:
            # Fallback: parse .env manually (no third-party dep needed)
            with open(ENV_FILE) as ef:
                for line in ef:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, _, v = line.partition("=")
                        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            print(f"  Loaded env manually from: {ENV_FILE}")
    else:
        print(f"  Warning: .env not found at {ENV_FILE} — relying on shell environment")

    sys.path.insert(0, str(CONNECTORS))
    from mssql import MSSQLConnector
    from sqlalchemy import text

    connector = MSSQLConnector("OCEAN")
    query = """
        SELECT fusion_id, sku_name
        FROM DM_BusinessInsights.dbo.dimProductAttributes
        WHERE is_active = N'1'
    """
    rows = []
    with connector._engine.connect() as conn:
        for r in conn.execute(text(query)):
            rows.append({"fusion_id": str(r.fusion_id), "sku_name": r.sku_name})
    connector.close()
    return rows


# ---------------------------------------------------------------------------
# MATCHING
# ---------------------------------------------------------------------------

def match_skus(
    hosting_skus: list[str],
    dim_rows: list[dict],
    threshold: int = FUZZY_THRESHOLD,
) -> list[dict]:
    """
    For every hosting SKU, try:
      1. Direct match  – normalised strings are equal
      2. Fuzzy match   – best similarity score above threshold
      3. No match      – nothing found
    """
    # Pre-build lookup: normalised_name → list of (fusion_id, sku_name)
    norm_to_dim: dict[str, list[dict]] = {}
    for r in dim_rows:
        key = normalise(r["sku_name"])
        norm_to_dim.setdefault(key, []).append(r)

    dim_sku_names = [r["sku_name"] for r in dim_rows]

    results = []

    for sku in hosting_skus:
        norm_sku = normalise(sku)

        # ---- 1. Direct match ----
        if norm_sku in norm_to_dim:
            candidates = norm_to_dim[norm_sku]
            # If multiple, list them all (e.g. fusion IDs that share a name)
            for c in candidates:
                results.append({
                    "product_sku": sku,
                    "fusion_id":   c["fusion_id"],
                    "sku_name":    c["sku_name"],
                    "match_type":  "direct",
                    "fuzzy_score": "",
                })
            continue

        # ---- 2. Fuzzy match ----
        best_score   = -1.0
        best_matches: list[dict] = []

        for r in dim_rows:
            score = similarity(sku, r["sku_name"])
            if score > best_score:
                best_score   = score
                best_matches = [r]
            elif score == best_score:
                best_matches.append(r)

        if best_score >= threshold:
            for m in best_matches:
                results.append({
                    "product_sku": sku,
                    "fusion_id":   m["fusion_id"],
                    "sku_name":    m["sku_name"],
                    "match_type":  "fuzzy",
                    "fuzzy_score": best_score,
                })
        else:
            results.append({
                "product_sku": sku,
                "fusion_id":   "",
                "sku_name":    "",
                "match_type":  "no_match",
                "fuzzy_score": best_score if best_score >= 0 else "",
            })

    return results


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Match Hosting SKUs to dimProductAttributes")
    parser.add_argument("--live", action="store_true", help="Pull from MSSQL instead of CSV")
    parser.add_argument("--threshold", type=int, default=FUZZY_THRESHOLD,
                        help=f"Fuzzy match threshold 0-100 (default {FUZZY_THRESHOLD})")
    parser.add_argument("--hosting-skus",  default=str(HOSTING_SKUS_FILE))
    parser.add_argument("--dim-csv",       default=str(DIM_PRODUCT_CSV))
    parser.add_argument("--output",        default=str(OUTPUT_FILE))
    args = parser.parse_args()

    print(f"Loading hosting SKUs from: {args.hosting_skus}")
    hosting_skus = load_hosting_skus(args.hosting_skus)
    print(f"  → {len(hosting_skus)} SKUs")

    if args.live:
        print("Loading dimProductAttributes from MSSQL …")
        dim_rows = load_dim_from_mssql()
    else:
        print(f"Loading dimProductAttributes from CSV: {args.dim_csv}")
        dim_rows = load_dim_from_csv(args.dim_csv)
    print(f"  → {len(dim_rows)} active products")

    print(f"Matching (fuzzy threshold={args.threshold}) …")
    results = match_skus(hosting_skus, dim_rows, threshold=args.threshold)

    # Stats
    direct   = sum(1 for r in results if r["match_type"] == "direct")
    fuzzy    = sum(1 for r in results if r["match_type"] == "fuzzy")
    no_match = sum(1 for r in results if r["match_type"] == "no_match")
    print(f"  direct={direct}  fuzzy={fuzzy}  no_match={no_match}  rows={len(results)}")

    fieldnames = ["product_sku", "fusion_id", "sku_name", "match_type", "fuzzy_score"]
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Output written to: {args.output}")


if __name__ == "__main__":
    main()
