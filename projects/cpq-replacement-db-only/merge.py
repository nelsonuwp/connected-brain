"""
merge.py
--------
Reconciles CPQ v28 extracted server data (01_servers.csv) with
dimProductAttributes from the Ocean DB (output/dim_product_attributes.csv).

Match strategy (in order):
  1. exact      — sku_name matches exactly (case-insensitive, trimmed)
  2. fuzzy      — rapidfuzz similarity >= FUZZY_THRESHOLD (default 85)
  3. unmatched  — no match found; fusion_id assigned as TEMP-<slug>

Outputs:
  output/merged_products.csv   — all CPQ servers with fusion_id + match metadata
  output/merge_report.csv      — only non-exact rows (your manual review list)

Usage:
    python merge.py [--fuzzy-threshold 85] [--dry-run]

After running, open merge_report.csv and set match_confidence = 'manual'
for any fuzzy row you've verified by hand, or 'unmatched' for ones that are
genuinely new products.
"""

import argparse
import re
import sys
from pathlib import Path

import pandas as pd
from rapidfuzz import fuzz, process

PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR   = PROJECT_ROOT / "output"
CPQ_DIR      = PROJECT_ROOT / "cpq-extracted"

FUZZY_THRESHOLD = 85  # 0-100; scores below this → unmatched


def slugify(text: str) -> str:
    """Convert a sku_name to a TEMP- placeholder ID."""
    slug = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return f"TEMP-{slug}"


def load_cpq_servers() -> pd.DataFrame:
    path = CPQ_DIR / "01_servers.csv"
    if not path.exists():
        sys.exit(f"ERROR: {path} not found. Run from project root.")
    df = pd.read_csv(path)
    # Primary key column is 'sku' in the extracted CSV
    df["sku_name"] = df["sku"].astype(str).str.strip()
    print(f"  CPQ servers loaded:         {len(df):>4} rows")
    return df


def load_dim_attributes() -> pd.DataFrame:
    path = OUTPUT_DIR / "dim_product_attributes.csv"
    if not path.exists():
        sys.exit(f"ERROR: {path} not found. Run extract.py first.")
    df = pd.read_csv(path, dtype=str)
    df["sku_name"]  = df["sku_name"].astype(str).str.strip()
    df["fusion_id"] = df["fusion_id"].astype(str).str.strip()
    print(f"  dimProductAttributes loaded: {len(df):>4} rows (active TLS)")
    return df


def normalise_cpq_name(name: str) -> str:
    """
    Strip CPQ-specific suffixes before matching against dimProductAttributes.
    Examples:
      "Pro Series 6.0 - M"       → "pro series 6.0"
      "Pro Series 6.0 vHost"     → "pro series 6.0 vhost"
      "Cluster 5.0 (Dell R440)"  → "cluster 5.0"
      "Advanced Series 6.0 - D"  → "advanced series 6.0"
    """
    n = name.strip().lower()
    # Remove " - M" and " - D" managed/dedicated suffixes
    n = re.sub(r"\s*-\s*[md]\s*$", "", n)
    # Remove parenthetical hardware specs e.g. "(Dell R440)"
    n = re.sub(r"\s*\([^)]+\)\s*$", "", n)
    return n.strip()


def match_servers(cpq: pd.DataFrame, dim: pd.DataFrame, fuzzy_threshold: int) -> pd.DataFrame:
    """
    For each CPQ server row, attempt to find a matching dim row.
    Returns cpq with additional columns:
        fusion_id, match_confidence, matched_dim_sku, dim_lifecycle,
        dim_adjusted_lob, dim_vendor, dim_product_type
    """
    # Build lookup: normalised sku_name → dim row
    dim_lookup = {row["sku_name"].lower(): row for _, row in dim.iterrows()}
    dim_names  = list(dim_lookup.keys())

    results = []

    for _, cpq_row in cpq.iterrows():
        cpq_name_lower = normalise_cpq_name(cpq_row["sku_name"])
        result = {
            "sku_name":          cpq_row["sku_name"],
            "fusion_id":         None,
            "match_confidence":  None,
            "matched_dim_sku":   None,
            "fuzzy_score":       None,
            "dim_lifecycle":     None,
            "dim_adjusted_lob":  None,
            "dim_vendor":        None,
            "dim_product_type":  None,
        }

        # 1. Exact match
        if cpq_name_lower in dim_lookup:
            dim_row = dim_lookup[cpq_name_lower]
            result.update({
                "fusion_id":        dim_row["fusion_id"],
                "match_confidence": "exact",
                "matched_dim_sku":  dim_row["sku_name"],
                "dim_lifecycle":    dim_row.get("lifecycle"),
                "dim_adjusted_lob": dim_row.get("adjusted_line_of_business"),
                "dim_vendor":       dim_row.get("vendor"),
                "dim_product_type": dim_row.get("product_type"),
            })
            results.append(result)
            continue

        # 2. Fuzzy match
        best = process.extractOne(
            cpq_name_lower,
            dim_names,
            scorer=fuzz.token_sort_ratio,
        )

        if best and best[1] >= fuzzy_threshold:
            matched_name = best[0]
            dim_row = dim_lookup[matched_name]
            result.update({
                "fusion_id":        dim_row["fusion_id"],
                "match_confidence": "fuzzy",
                "matched_dim_sku":  dim_row["sku_name"],
                "fuzzy_score":      best[1],
                "dim_lifecycle":    dim_row.get("lifecycle"),
                "dim_adjusted_lob": dim_row.get("adjusted_line_of_business"),
                "dim_vendor":       dim_row.get("vendor"),
                "dim_product_type": dim_row.get("product_type"),
            })
        else:
            # 3. Unmatched — assign TEMP- placeholder
            result.update({
                "fusion_id":        slugify(cpq_row["sku_name"]),
                "match_confidence": "unmatched",
                "fuzzy_score":      best[1] if best else None,
                "matched_dim_sku":  best[0] if best else None,  # closest miss, for reference
            })

        results.append(result)

    match_df = pd.DataFrame(results)

    # Merge back with full CPQ row data
    merged = cpq.merge(
        match_df.drop(columns=["sku_name"]),
        left_index=True,
        right_index=True,
    )

    return merged


def print_summary(merged: pd.DataFrame) -> None:
    counts = merged["match_confidence"].value_counts()
    print("\nMatch summary:")
    for confidence in ["exact", "fuzzy", "unmatched"]:
        n = counts.get(confidence, 0)
        print(f"  {confidence:<12} {n:>4}")
    print(f"  {'TOTAL':<12} {len(merged):>4}")


def main():
    parser = argparse.ArgumentParser(description="Merge CPQ servers with dimProductAttributes")
    parser.add_argument("--fuzzy-threshold", type=int, default=FUZZY_THRESHOLD,
                        help=f"Fuzzy match score threshold 0-100 (default: {FUZZY_THRESHOLD})")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print summary but do not write output files")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(exist_ok=True)

    print("Loading data...")
    cpq = load_cpq_servers()
    dim = load_dim_attributes()

    print(f"\nMatching (fuzzy threshold: {args.fuzzy_threshold})...")
    merged = match_servers(cpq, dim, args.fuzzy_threshold)

    print_summary(merged)

    if args.dry_run:
        print("\n--dry-run: no files written.")
        return

    # Full merged output
    merged_path = OUTPUT_DIR / "merged_products.csv"
    merged.to_csv(merged_path, index=False)
    print(f"\nWritten → {merged_path}")

    # Review report: everything that isn't an exact match
    review = merged[merged["match_confidence"] != "exact"].copy()
    review_cols = [
        "sku_name", "match_confidence", "fuzzy_score",
        "matched_dim_sku", "fusion_id",
        "dim_lifecycle", "dim_adjusted_lob", "dim_vendor",
    ]
    review = review[[c for c in review_cols if c in review.columns]]
    report_path = OUTPUT_DIR / "merge_report.csv"
    review.to_csv(report_path, index=False)
    print(f"Written → {report_path}  ({len(review)} rows need review)")

    if len(review) > 0:
        print("\nRows requiring manual review:")
        print(review[["sku_name", "match_confidence", "fuzzy_score", "matched_dim_sku"]].to_string(index=False))
        print(f"\nOpen {report_path} and:")
        print("  - Set match_confidence = 'manual' for fuzzy rows you've verified")
        print("  - Set match_confidence = 'unmatched' for genuine new products")
        print("  - Update fusion_id manually where you know the correct value")
        print("  Then re-run generate_seed.py.")

    print("\nDone.")


if __name__ == "__main__":
    main()
