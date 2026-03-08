"""
patch_lifecycle.py
------------------
One-shot patch for known issues in 07c_product_lifecycle.csv that don't
warrant a full re-run:

  1. Generic drives  → source_method=skipped, needs_review=False
  2. RHEL variants   → inherit from base RHEL rows that succeeded
  3. CPU misses      → Intel ARK dates for Gold 6238R and Gold 6526Y

Usage:
    cd projects/cpq-replacement-db-only
    python patch_lifecycle.py [--dry-run]
"""

import argparse
import csv
from pathlib import Path

OUTPUT       = Path(__file__).parent / "output"
LIFECYCLE_CSV = OUTPUT / "07c_product_lifecycle.csv"

LIFECYCLE_FIELDS = [
    "sku", "product_category",
    "launch_date", "end_of_sale_date",
    "end_of_standard_support_date", "end_of_life_date",
    "source_method", "source_url",
    "confidence", "needs_review", "notes",
]

# ---------------------------------------------------------------------------
# Patch definitions
# ---------------------------------------------------------------------------

# 1. Generic drives — intentionally skipped, not actually missing
GENERIC_DRIVE_SKUS = {
    "1 TB 7200 6 Gb/s SATA",
    "2 TB 7200 6 Gb/s SATA",
    "4 TB 7200 6 Gb/s SATA",
    "12 TB 7200 6 Gb/s SATA",
    "480 GB SSD",
    "480 GB SATA 2.5in SSD",
    "960 GB SATA 2.5in SSD",
    "1.92 TB SATA 2.5in SSD",
    "3.84 TB SATA 2.5in SSD",
    "960 GB NVMe u.2 2.5in",
    "3.84 TB NVMe u.2 2.5in",
    "6.4 TB NVMe u.2 2.5in",
    "15.36 TB NVMe u.2 2.5in",
}

# 2. RHEL variants — inherit dates from base SKU (RHEL API was down)
RHEL_INHERIT = {
    # sku                                    : base_sku to inherit from
    "RHEL 9.x VDC for Unlimited Linux Guests": "RHEL 9.x",
    "RHEL for VMs - 1 to 8 vCPUs":            "RHEL 9.x for VMs",
    "RHEL for VMs - 128 to Unlimited vCPUs":  "RHEL for VMs - 9 to 127 vCPUs",
}

# 3. CPU misses — sourced from Intel ARK
#    Gold 6238R: ark.intel.com/content/www/us/en/ark/products/193951
#    Gold 6526Y: ark.intel.com/content/www/us/en/ark/products/237606
CPU_PATCHES = {
    "Intel Xeon Gold 6238R 2.2 GHz 28C/56T": {
        "launch_date":                  "2020-04-01",
        "end_of_sale_date":             "",
        "end_of_standard_support_date": "2028-12-31",
        "end_of_life_date":             "2028-12-31",
        "source_method":                "perplexity_grounded",
        "source_url":                   "https://ark.intel.com/content/www/us/en/ark/products/193951/intel-xeon-gold-6238r-processor-38-5m-cache-2-20-ghz.html",
        "confidence":                   "0.85",
        "needs_review":                 "False",
        "notes":                        "Cascade Lake Refresh; EOSS from Intel ARK via patch",
    },
    "Intel Xeon Gold 6526Y 2.9G, 16/32T": {
        "launch_date":                  "2023-12-14",
        "end_of_sale_date":             "",
        "end_of_standard_support_date": "",
        "end_of_life_date":             "",
        "source_method":                "perplexity_grounded",
        "source_url":                   "https://ark.intel.com/content/www/us/en/ark/products/237606/intel-xeon-gold-6526y-processor-37-5m-cache-2-80-ghz.html",
        "confidence":                   "0.85",
        "needs_review":                 "False",
        "notes":                        "Granite Rapids; EOL not yet published — patched launch date only",
    },
    # Inherited row also needs fixing
    "Default Intel Xeon Gold 6526Y 2.9G, 16/32T": {
        "launch_date":                  "2023-12-14",
        "end_of_sale_date":             "",
        "end_of_standard_support_date": "",
        "end_of_life_date":             "",
        "source_method":                "perplexity_grounded",
        "source_url":                   "https://ark.intel.com/content/www/us/en/ark/products/237606/intel-xeon-gold-6526y-processor-37-5m-cache-2-80-ghz.html",
        "confidence":                   "0.85",
        "needs_review":                 "False",
        "notes":                        "Inherited from 'Intel Xeon Gold 6526Y 2.9G, 16/32T'; patched via patch_lifecycle.py",
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rows = []
    with open(LIFECYCLE_CSV, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    # Build lookup by SKU for RHEL inheritance
    by_sku = {r["sku"]: r for r in rows}

    patched = 0
    for row in rows:
        sku = row["sku"]

        # 1. Generic drives
        if sku in GENERIC_DRIVE_SKUS and row.get("source_method") == "not_found":
            print(f"  [skip   ] {sku}")
            if not args.dry_run:
                row["source_method"] = "skipped"
                row["needs_review"]  = "False"
                row["notes"]         = "Generic drive SKU — no manufacturer-specific EOL published"
            patched += 1

        # 2. RHEL inheritance
        elif sku in RHEL_INHERIT:
            base = RHEL_INHERIT[sku]
            base_row = by_sku.get(base)
            if base_row:
                print(f"  [inherit] {sku}  ←  {base}")
                if not args.dry_run:
                    row["launch_date"]                  = base_row["launch_date"]
                    row["end_of_sale_date"]             = base_row["end_of_sale_date"]
                    row["end_of_standard_support_date"] = base_row["end_of_standard_support_date"]
                    row["end_of_life_date"]             = base_row["end_of_life_date"]
                    row["source_method"]                = "inherited"
                    row["source_url"]                   = base_row["source_url"]
                    row["confidence"]                   = base_row["confidence"]
                    row["needs_review"]                 = "False"
                    row["notes"]                        = f"Inherited from '{base}' — RHEL API unavailable at run time"
                patched += 1
            else:
                print(f"  [WARN   ] {sku} — base '{base}' not found in CSV")

        # 3. CPU patches
        elif sku in CPU_PATCHES:
            print(f"  [patch  ] {sku}")
            if not args.dry_run:
                row.update(CPU_PATCHES[sku])
            patched += 1

    if args.dry_run:
        print(f"\n  Dry-run — {patched} rows would be patched, nothing written")
        return

    with open(LIFECYCLE_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LIFECYCLE_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    remaining = sum(1 for r in rows if str(r.get("needs_review")).lower() == "true")
    print(f"\n  Patched {patched} rows → {LIFECYCLE_CSV.name}")
    print(f"  Remaining needs_review: {remaining}")


if __name__ == "__main__":
    main()
