"""
Generate output/migrations/add_fusion_ids_from_dim_services_components.sql
from dimProductAttributes CSV (columns: fusion_id, sku_name, level).

Usage:
  python generate_fusion_id_migration.py [path_to_dimProductAttributes.csv]
  Default path: ~/Downloads/dimProductAttributes_*.csv (most recent) or first .csv in cwd.
"""

import csv
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SEED_SQL = PROJECT_ROOT / "output" / "seed_data.sql"
SEED_PHASE2_SQL = PROJECT_ROOT / "output" / "seed_data_phase2.sql"
OUT_MIGRATION = PROJECT_ROOT / "output" / "migrations" / "add_fusion_ids_from_dim_services_components.sql"


def find_csv(path_arg: str | None) -> Path:
    if path_arg:
        p = Path(path_arg).expanduser().resolve()
        if p.is_file():
            return p
        raise FileNotFoundError(path_arg)
    downloads = Path.home() / "Downloads"
    if downloads.exists():
        candidates = sorted(downloads.glob("dimProductAttributes_*.csv"), key=lambda x: x.stat().st_mtime, reverse=True)
        if candidates:
            return candidates[0]
    for c in PROJECT_ROOT.glob("dimProductAttributes_*.csv"):
        return c
    raise FileNotFoundError("No dimProductAttributes_*.csv found in ~/Downloads or project root. Pass path.")


def load_attr_map(csv_path: Path) -> dict[str, str]:
    with open(csv_path, encoding="utf-8") as f:
        r = csv.DictReader(f)
        attr_map = {}
        for row in r:
            sku = (row.get("sku_name") or "").strip()
            fid = (row.get("fusion_id") or "").strip()
            if sku and fid and fid.isdigit():
                attr_map[sku] = fid
        return attr_map


def seed_tls_skus() -> set[str]:
    text = SEED_SQL.read_text()
    return set(re.findall(r"VALUES\s*\('[^']*',\s*'([^']+)',[^)]*'TLS'", text))


def seed_component_skus() -> set[str]:
    text = SEED_PHASE2_SQL.read_text()
    return set(re.findall(r"VALUES\s*\('([^']+)',\s*'[^']+',\s*'Component'", text))


def main() -> None:
    csv_path = find_csv(sys.argv[1] if len(sys.argv) > 1 else None)
    print("Using:", csv_path)

    attr_map = load_attr_map(csv_path)
    tls_skus = seed_tls_skus()
    comp_skus = seed_component_skus()

    tls_matches = [(s, attr_map[s]) for s in sorted(tls_skus) if s in attr_map]
    comp_matches = [(s, attr_map[s]) for s in sorted(comp_skus) if s in attr_map]

    def esc(s: str) -> str:
        return s.replace("'", "''")

    lines = [
        "-- Migration: Set fusion_id from dimProductAttributes (sku_name -> fusion_id, level TLS/Component)",
        f"-- Source: {csv_path.name}",
        "-- Apply after seed_data.sql and seed_data_phase2.sql.",
        "",
        "BEGIN;",
        "",
        "-- -----------------------------------------------------------------------------",
        f"-- TLS ({len(tls_matches)} matches in dimProductAttributes)",
        "-- -----------------------------------------------------------------------------",
        "",
    ]
    for sku, fid in tls_matches:
        lines.append(f"UPDATE product_catalog SET fusion_id = '{fid}' WHERE level = 'TLS' AND sku_name = '{esc(sku)}';")
    lines.extend([
        "",
        "-- -----------------------------------------------------------------------------",
        f"-- COMPONENTS ({len(comp_matches)} matches in dimProductAttributes)",
        "-- -----------------------------------------------------------------------------",
        "",
    ])
    for sku, fid in comp_matches:
        lines.append(f"UPDATE product_catalog SET fusion_id = '{fid}' WHERE level = 'Component' AND sku_name = '{esc(sku)}';")
    lines.extend(["", "COMMIT;", ""])

    OUT_MIGRATION.parent.mkdir(parents=True, exist_ok=True)
    OUT_MIGRATION.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_MIGRATION} ({len(tls_matches)} TLS, {len(comp_matches)} Component updates).")


if __name__ == "__main__":
    main()
