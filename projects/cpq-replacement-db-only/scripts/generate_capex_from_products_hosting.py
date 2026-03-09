"""
Generate product_capex INSERTs from "Products - Hosting.csv" for products that:
- Exist in product_catalog (by sku_name = CSV "Product SKU")
- Do not already have a product_capex row

CSV columns: Product SKU (1), CapEx to Allocate (USD) (32), Residual Value 12 Months (33), Residual Value 24 Months (34)
Values: strip $/£, commas; percentages as 40 -> 0.4.

Usage:
  python scripts/generate_capex_from_products_hosting.py [path_to_Products_Hosting.csv]
  Default: ~/Downloads/Products - Hosting.csv
"""

import csv
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SEED_PHASE2 = PROJECT_ROOT / "output" / "seed_data_phase2.sql"
OUT_MIGRATION = PROJECT_ROOT / "output" / "migrations" / "add_product_capex_from_products_hosting_csv.sql"


def find_csv(path_arg: str | None) -> Path:
    if path_arg:
        p = Path(path_arg).expanduser().resolve()
        if p.is_file():
            return p
        raise FileNotFoundError(path_arg)
    for name in ["Products - Hosting.csv", "Products-Hosting.csv"]:
        p = Path.home() / "Downloads" / name
        if p.is_file():
            return p
    raise FileNotFoundError("No Products - Hosting.csv in ~/Downloads. Pass path.")


def clean_currency(s: str) -> float | None:
    if not s or not isinstance(s, str):
        return None
    s = s.strip().strip("$").strip("£").replace(",", "").replace("-", "").strip()
    if not s or s.upper() == "N/A":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def clean_pct(s: str) -> float | None:
    if not s or not isinstance(s, str):
        return None
    s = s.strip().strip("%").strip()
    if not s:
        return None
    try:
        v = float(s)
        return round(v / 100.0, 4) if v > 1 else v
    except ValueError:
        return None


def seed_product_sku_names() -> set[str]:
    """All product_catalog.sku_name from seed_data_phase2 (Component/TLS inserts)."""
    text = SEED_PHASE2.read_text()
    # INSERT INTO product_catalog ... VALUES ('sku_name', ...
    return set(re.findall(r"VALUES\s*\('([^']+)',\s*'[^']+',\s*'(?:Component|TLS)'", text)) | set(
        re.findall(r"VALUES\s*\('[^']*',\s*'([^']+)',[^)]*'TLS'", text)
    )


def main() -> None:
    csv_path = find_csv(sys.argv[1] if len(sys.argv) > 1 else None)
    print("Using:", csv_path)

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        next(r)
        rows = list(r)

    in_catalog = seed_product_sku_names()
    seed_sql = (PROJECT_ROOT / "output" / "seed_data.sql").read_text()
    in_catalog |= set(re.findall(r"VALUES\s*\('[^']*',\s*'([^']+)',[^)]*'TLS'", seed_sql))

    # product_capex already in seed_data_phase2 (skip these so we only output "new" INSERTs)
    seed_text = SEED_PHASE2.read_text()
    existing_capex = set(re.findall(r"product_capex.*?sku_name = '([^']+)'", seed_text))

    to_add = []
    for row in rows:
        if len(row) <= 32:
            continue
        sku = (row[1] or "").strip()
        if not sku or sku not in in_catalog:
            continue
        if sku in existing_capex:
            continue
        cap = clean_currency(row[32])
        if cap is None or cap <= 0:
            continue
        r12 = clean_pct(row[33]) if len(row) > 33 else None
        r24 = clean_pct(row[34]) if len(row) > 34 else None
        to_add.append({"sku": sku, "capex_usd": cap, "r12": r12, "r24": r24})

    def esc(s: str) -> str:
        return s.replace("'", "''")

    lines = [
        "-- Add product_capex from Products - Hosting.csv (CapEx to Allocate USD, Residual 12m/24m)",
        f"-- Source: {csv_path.name}",
        "-- Only for products in product_catalog that do not already have a product_capex row.",
        "",
        "BEGIN;",
        "",
    ]
    for p in to_add:
        r12 = p["r12"] if p["r12"] is not None else "NULL"
        r24 = p["r24"] if p["r24"] is not None else "NULL"
        if r12 != "NULL":
            r12 = str(p["r12"])
        if r24 != "NULL":
            r24 = str(p["r24"])
        lines.append(
            f"INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)"
        )
        lines.append(
            f"SELECT id, {p['capex_usd']}, 'USD', '2024-01-01', true, {r12}, {r24}, 'Products - Hosting.csv CapEx to Allocate (USD)'"
        )
        lines.append(f"FROM product_catalog")
        lines.append(f"WHERE sku_name = '{esc(p['sku'])}'")
        lines.append("  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);")
        lines.append("")
    lines.append("COMMIT;")
    lines.append("")

    OUT_MIGRATION.parent.mkdir(parents=True, exist_ok=True)
    OUT_MIGRATION.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_MIGRATION} ({len(to_add)} product_capex INSERTs).")
    for p in to_add:
        print(" ", p["sku"][:50], "->", p["capex_usd"], "USD")


if __name__ == "__main__":
    main()
