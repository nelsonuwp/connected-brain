"""
generate_seed_phase2.py
-----------------------
Generates seed_data_phase2.sql covering all component-level data.

Reads from:
    cpq-extracted/03_server_default_components.csv
    cpq-extracted/04_server_selectable_options.csv
    cpq-extracted/05_hardware_components.csv
    cpq-extracted/06_software_licenses.csv
    cpq-extracted/07_component_specs.csv
    cpq-extracted/01_servers.csv
    output/07c_product_lifecycle.csv

Emits:
    product_types          — new type_code rows (ON CONFLICT DO NOTHING)
    product_catalog        — 59 hardware + 85 software + stub rows for bundled
                             components (RAID card, GigE, extra PSUs) only in 03
    component_specs        — sparse CPU/RAM/Drive/NIC rows from 07_component_specs
    product_pricing        — MRC/NRC from 05/06 hardware/software
    product_capex          — server-level CapEx from 01_servers.csv
    server_default_components  — from 03, joined by sku_name
    server_selectable_options  — from 04, skipping "No Upgrades Available"/"IPMI Card"
    UPDATE product_catalog — lifecycle dates from 07c_product_lifecycle.csv

Apply order:
    psql -f schema.sql
    psql -f output/seed_data.sql           (Phase 1)
    psql -f output/seed_data_phase2.sql    (Phase 2 — this file)

Usage:
    cd projects/cpq-replacement-db-only
    python generate_seed_phase2.py [--dry-run]
"""

import argparse
import csv
import json
import math
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR   = PROJECT_ROOT / "output"
CPQ_DIR      = PROJECT_ROOT / "cpq-extracted"

OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# SQL helpers (duplicated from generate_seed.py to keep this file standalone)
# ---------------------------------------------------------------------------

class RawSQL:
    def __init__(self, expr: str):
        self.expr = expr
    def __str__(self):
        return self.expr


def subselect(table: str, col: str, val: str) -> RawSQL:
    return RawSQL(f"(SELECT id FROM {table} WHERE {col} = '{val}')")


def sql_val(v) -> str:
    if isinstance(v, RawSQL):
        return str(v)
    if v is None or v == "" or (isinstance(v, float) and math.isnan(v)):
        return "NULL"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


def insert(table: str, row: dict, comment: str = None) -> str:
    cols = ", ".join(row.keys())
    vals = ", ".join(sql_val(v) for v in row.values())
    comment_str = f"  -- {comment}" if comment else ""
    return f"INSERT INTO {table} ({cols}) VALUES ({vals});{comment_str}"


def section(title: str) -> str:
    bar = "-" * 77
    return f"\n-- {bar}\n-- {title}\n-- {bar}\n"


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_csv(path: Path) -> list:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def clean_num(v) -> float | None:
    """Strip currency symbols and return float, or None if empty/zero."""
    if v is None:
        return None
    s = str(v).strip().lstrip("$£").replace(",", "").strip()
    if not s or s == "-" or s == "N/A":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def clean_str(v) -> str | None:
    s = str(v).strip() if v else ""
    return s if s else None


def clean_bool(v) -> bool:
    return str(v).strip().lower() in ("true", "1", "yes")


# ---------------------------------------------------------------------------
# Category → product_type_code mapping
# ---------------------------------------------------------------------------

CATEGORY_TYPE_CODE = {
    # Hardware
    "Processor":    "cpu",
    "RAM":          "ram",
    "Drive":        "drive",
    "PSU":          "psu",
    "Network Card": "nic",
    "RAID Card":    "raid_card",
    "Network":      "network_component",  # bundled GigE
    # Software
    "OS":           "os",
    "SQL":          "sql",
    "Monitoring":   "monitoring",
    "Remote Access":"remote_access",
    "Backup":       "backup",
    "VMWare":       "vmware",
    "Proxmox":      "proxmox",
    # 04 option_category aliases
    "Standard OS":  "os",
    "vHost OS":     "os",
    "CPU":          "cpu",
    "IPMI Card":    "ipmi",   # skipped in selectable options but typed for completeness
}

# product_types rows to ensure exist (ON CONFLICT DO NOTHING)
PRODUCT_TYPES = [
    # code,              label,                 parent,    level
    ("cpu",              "Processor",            None,      "Component"),
    ("ram",              "RAM",                  None,      "Component"),
    ("drive",            "Drive",                None,      "Component"),
    ("psu",              "Power Supply",         None,      "Component"),
    ("nic",              "Network Card",         None,      "Component"),
    ("raid_card",        "RAID Card",            None,      "Component"),
    ("network_component","Network Component",    None,      "Component"),
    ("os",               "Operating System",     None,      "Component"),
    ("sql",              "SQL Server",           None,      "Component"),
    ("monitoring",       "Monitoring",           None,      "Component"),
    ("remote_access",    "Remote Access",        None,      "Component"),
    ("backup",           "Backup",               None,      "Component"),
    ("vmware",           "VMware",               None,      "Component"),
    ("proxmox",          "Proxmox",              None,      "Component"),
]

# ---------------------------------------------------------------------------
# 03 stubs — SKUs referenced in server_default_components not in 05/06
# ---------------------------------------------------------------------------

STUB_COMPONENTS = [
    # sku, category, type_code, notes
    ("Hardware RAID Controller",            "RAID Card",    "raid_card",          "Bundled RAID controller — included in server base price"),
    ("1000 Mbit Connection - GigE",         "Network",      "network_component",  "Bundled 1GbE connection — included in server base price"),
    ("960 GB SSD",                          "Drive",        "drive",              "Generic 960 GB SSD stub — no standalone pricing"),
    ("8 TB SATA",                           "Drive",        "drive",              "Generic 8 TB SATA stub — Promo Server default"),
    ("Dual 550W PSU",                       "PSU",          "psu",                "Bundled dual 550W PSU — included in server base price"),
    ("Dual 800W PSU",                       "PSU",          "psu",                "Bundled dual 800W PSU — included in server base price"),
    ("Redundant 1100W Power Supply",        "PSU",          "psu",                "Bundled redundant 1100W PSU — included in server base price"),
    ("Redundant Power Supply (750W / 1100W)","PSU",         "psu",                "Bundled redundant PSU — included in server base price"),
    ("Single Power Supply",                 "PSU",          "psu",                "Bundled single PSU — included in server base price"),
    ("Default Intel Xeon 6517P 16 core",    "Processor",    "cpu",                "Default CPU stub for Pro Series 7.0 — verify part number"),
    ("Intel Xeon Gold 6326 2.9GHz 16 Cores/32T", "Processor", "cpu",             "CPU stub for Atomic 5.0 default config"),
]

# 04 option_values to skip entirely — no data value
SKIP_OPTION_VALUES = {"No Upgrades Available", "IPMI Card"}

# Map 04 option_category → component_specs category for FK lookup
OPTION_CATEGORY_TO_HW_CATEGORY = {
    "CPU":          "Processor",
    "RAM":          "RAM",
    "Drive":        "Drive",
    "PSU":          "PSU",
    "Network Card": "Network Card",
    "Standard OS":  "OS",
    "vHost OS":     "OS",
}

# drive_type inference from drive interface/sku
def infer_drive_type(sku: str, interface: str) -> str | None:
    sku_l = sku.lower()
    iface = (interface or "").lower()
    if "nvme" in sku_l or "nvme" in iface:
        return "NVMe"
    if "ssd" in sku_l or "sata" in iface:
        return "SSD"
    if "7200" in sku_l or "hdd" in sku_l:
        return "HDD"
    if "sas" in iface:
        return "SAS"
    return None


# ---------------------------------------------------------------------------
# Section generators
# ---------------------------------------------------------------------------

def gen_product_types(lines: list) -> None:
    lines.append(section("PRODUCT TYPES — Component type hierarchy"))
    lines.append("-- ON CONFLICT DO NOTHING — safe to re-run\n")
    for code, label, parent, level in PRODUCT_TYPES:
        lines.append(
            f"INSERT INTO product_types (type_code, type_label, parent_code, level) "
            f"VALUES ({sql_val(code)}, {sql_val(label)}, {sql_val(parent)}, {sql_val(level)}) "
            f"ON CONFLICT (type_code) DO NOTHING;"
        )


def gen_component_catalog(lines: list, hw: list, sw: list) -> None:
    """
    Insert product_catalog rows for all hardware + software components,
    plus stub rows for bundled components only referenced in 03.
    """
    lines.append(section("PRODUCT CATALOG — Hardware components (05)"))
    lines.append("-- level=Component, no fusion_id (components have no Salesforce anchor)\n")

    for row in hw:
        sku      = row["sku"].strip()
        category = row["category"].strip()
        type_code = CATEGORY_TYPE_CODE.get(category, category.lower())
        lines.append(insert("product_catalog", {
            "sku_name":          sku,
            "product_type_code": type_code,
            "level":             "Component",
            "is_active":         True,
            "notes":             f"Hardware component — seeded from CPQ v28 05_hardware_components.csv",
        }))

    lines.append(section("PRODUCT CATALOG — Software licenses (06)"))
    lines.append("-- OS, SQL, Monitoring, Backup, Remote Access, VMware, Proxmox\n")

    for row in sw:
        sku      = row["sku"].strip()
        category = row["category"].strip()
        type_code = CATEGORY_TYPE_CODE.get(category, category.lower())
        lines.append(insert("product_catalog", {
            "sku_name":          sku,
            "product_type_code": type_code,
            "level":             "Component",
            "is_active":         True,
            "notes":             f"Software license — seeded from CPQ v28 06_software_licenses.csv",
        }))

    lines.append(section("PRODUCT CATALOG — Bundled component stubs"))
    lines.append("-- Referenced in 03_server_default_components but not in 05/06.")
    lines.append("-- These are included in server base price — no standalone pricing.\n")

    for sku, category, type_code, notes in STUB_COMPONENTS:
        lines.append(insert("product_catalog", {
            "sku_name":          sku,
            "product_type_code": type_code,
            "level":             "Component",
            "is_active":         True,
            "notes":             notes,
        }))


def gen_component_specs(lines: list, specs: list) -> None:
    """
    Insert component_specs rows — sparse, only relevant fields per category.
    Schema columns: product_id, cores, threads, clock_ghz, ram_gb,
                    drive_capacity_tb, drive_type, watts, form_factor
    """
    lines.append(section("COMPONENT SPECS — CPU / RAM / Drive / NIC"))
    lines.append("-- Sparse table — only columns relevant to each category are populated.")
    lines.append("-- Enriched via Perplexity sonar-pro (see 07_component_specs.csv).\n")

    for row in specs:
        sku      = row["sku"].strip()
        category = row["category"].strip()

        # Resolve product_id via subselect
        product_ref = subselect("product_catalog", "sku_name", sku)

        spec = {"product_id": product_ref}

        if category == "Processor":
            spec["cores"]      = clean_num(row.get("cores"))     or None
            spec["threads"]    = clean_num(row.get("threads"))   or None
            spec["clock_ghz"]  = clean_num(row.get("clock_ghz")) or None
            # Schema 'watts' = TDP. Use tdp_watts from enrichment, fall back to watts col.
            tdp = clean_num(row.get("tdp_watts")) or clean_num(row.get("watts"))
            spec["watts"]      = int(tdp) if tdp else None

        elif category == "RAM":
            spec["ram_gb"]     = clean_num(row.get("ram_gb")) or None

        elif category == "Drive":
            spec["drive_capacity_tb"] = clean_num(row.get("drive_capacity_tb")) or None
            spec["drive_type"]        = infer_drive_type(sku, row.get("interface", ""))
            spec["form_factor"]       = clean_str(row.get("form_factor"))

        elif category == "Network Card":
            spec["form_factor"] = clean_str(row.get("connector_type"))

        # Skip PSU — no spec columns applicable

        # Only insert if we have at least one non-null spec field beyond product_id
        non_null = [v for k, v in spec.items() if k != "product_id" and v is not None]
        if non_null:
            lines.append(insert("component_specs", spec))


def gen_component_pricing(lines: list, hw: list, sw: list) -> None:
    """
    Insert product_pricing for hardware (05) and software (06).
    Same structure as server pricing — USD only (components are quoted in USD).
    """
    lines.append(section("PRODUCT PRICING — Component MRC/NRC (USD)"))
    lines.append("-- Components are USD-denominated; server-level pricing handles currency conversion.\n")

    term_cols = {
        0:  "mrc_monthly_usd",
        12: "mrc_12m_usd",
        24: "mrc_24m_usd",
        36: "mrc_36m_usd",
    }

    for row in (hw + sw):
        sku = row["sku"].strip()
        product_ref = subselect("product_catalog", "sku_name", sku)
        nrc = clean_num(row.get("nrc_usd"))

        for term, col in term_cols.items():
            mrc = clean_num(row.get(col))
            if mrc is None and nrc is None:
                continue
            # Skip rows where everything is zero — no pricing to store
            if (mrc or 0) == 0 and (nrc or 0) == 0:
                continue
            lines.append(insert("product_pricing", {
                "product_id":    product_ref,
                "currency_code": "USD",
                "term_months":   term,
                "mrc":           mrc,
                "nrc":           nrc,
                "pricing_model": "flat",
            }))


def gen_product_capex(lines: list, servers: list) -> None:
    """
    Insert product_capex for server SKUs that have capex_usd > 0.
    Procured date is a placeholder — update from actual procurement records.
    """
    lines.append(section("PRODUCT CAPEX — Server hardware procurement cost"))
    lines.append("-- procured_date='2024-01-01' is a placeholder — update from actual PO dates.")
    lines.append("-- CAD equivalent derived at query time via fx_rates budget rate.\n")

    for row in servers:
        sku   = row["sku"].strip()
        capex = clean_num(row.get("capex_usd"))
        if not capex or capex <= 0:
            continue

        res12 = clean_num(row.get("residual_value_12m"))
        res24 = clean_num(row.get("residual_value_24m"))

        lines.append(insert("product_capex", {
            "product_id":       subselect("product_catalog", "sku_name", sku),
            "procured_price":   capex,
            "procured_currency":"USD",
            "procured_date":    "2024-01-01",   # placeholder — update from PO records
            "use_as_baseline":  True,
            "residual_pct_12m": res12,
            "residual_pct_24m": res24,
            "notes":            "Seeded from CPQ v28 — procured_date is placeholder",
        }))


def gen_server_default_components(lines: list, defaults: list) -> None:
    """
    Insert server_default_components from 03_server_default_components.csv.
    Skips types: Monitoring (not a hardware component),
                 and any default_value that resolves to a skip.
    """
    SKIP_TYPES = {"Monitoring"}  # Monitoring defaults handled via software licensing, not components

    lines.append(section("SERVER DEFAULT COMPONENTS"))
    lines.append("-- One row per server × default component. 126 rows from CPQ v28.")
    lines.append("-- Quantity=1 for all (CPQ v28 doesn't encode qty separately from default_qty).\n")

    # Map 03 component_type → product_catalog product_type_code for category column
    TYPE_TO_CATEGORY = {
        "CPU":      "cpu",
        "RAM":      "ram",
        "Drive":    "drive",
        "RAID Card":"raid_card",
        "PSU":      "psu",
        "Network":  "network_component",
    }

    seen = set()
    for row in defaults:
        server_sku     = row["server_sku"].strip()
        component_type = row["component_type"].strip()
        component_sku  = row["default_value"].strip()

        if component_type in SKIP_TYPES:
            continue
        if not component_sku:
            continue

        key = (server_sku, component_sku)
        if key in seen:
            continue
        seen.add(key)

        category = TYPE_TO_CATEGORY.get(component_type, component_type.lower())

        lines.append(insert("server_default_components", {
            "server_product_id":    subselect("product_catalog", "sku_name", server_sku),
            "component_product_id": subselect("product_catalog", "sku_name", component_sku),
            "component_type":       category,
            "quantity":             1,
        }))


def gen_server_selectable_options(lines: list, options: list) -> None:
    """
    Insert server_selectable_options from 04_server_selectable_options.csv.
    Skips: 'No Upgrades Available', 'IPMI Card' (51 rows, no data value).
    """
    lines.append(section("SERVER SELECTABLE OPTIONS"))
    lines.append("-- Source of truth for component compatibility — 655 rows from CPQ v28.")
    lines.append("-- Skipped: 'No Upgrades Available' and 'IPMI Card' rows (no data value).\n")

    CATEGORY_MAP = {
        "CPU":          "cpu",
        "RAM":          "ram",
        "Drive":        "drive",
        "PSU":          "psu",
        "Network Card": "nic",
        "Standard OS":  "os",
        "vHost OS":     "os",
        "IPMI Card":    "ipmi",  # will be skipped anyway
    }

    seen = set()
    display_order_counter = {}

    for row in options:
        server_sku     = row["server_sku"].strip()
        option_category= row["option_category"].strip()
        option_value   = row["option_value"].strip()

        # Skip non-data rows
        if option_value in SKIP_OPTION_VALUES:
            continue
        if option_category == "IPMI Card":
            continue

        key = (server_sku, option_value)
        if key in seen:
            continue
        seen.add(key)

        category = CATEGORY_MAP.get(option_category, option_category.lower())

        # Per-server per-category display order
        order_key = (server_sku, category)
        display_order_counter[order_key] = display_order_counter.get(order_key, 0) + 1
        display_order = display_order_counter[order_key]

        lines.append(insert("server_selectable_options", {
            "server_product_id":    subselect("product_catalog", "sku_name", server_sku),
            "component_product_id": subselect("product_catalog", "sku_name", option_value),
            "category":             category,
            "is_included_default":  False,
            "display_order":        display_order,
        }))


def gen_lifecycle_updates(lines: list, lifecycle: list) -> None:
    """
    UPDATE product_catalog with lifecycle dates from 07c_product_lifecycle.csv.

    Schema column mapping:
        launch_date                   → release_date
        end_of_sale_date              → end_of_sale_date
        end_of_standard_support_date  → end_of_support_date
        end_of_life_date              → end_of_service_life_date
    """
    lines.append(section("PRODUCT CATALOG — Lifecycle date updates"))
    lines.append("-- Updates release_date, end_of_sale_date, end_of_support_date,")
    lines.append("-- end_of_service_life_date from 07c_product_lifecycle.csv.")
    lines.append("-- Skipped rows have no sourced dates (generic drives, needs_review stubs).\n")

    updated = 0
    skipped = 0

    for row in lifecycle:
        sku = row["sku"].strip()

        # Only update rows that have at least one real date
        launch = clean_str(row.get("launch_date"))
        eos    = clean_str(row.get("end_of_sale_date"))
        eoss   = clean_str(row.get("end_of_standard_support_date"))
        eol    = clean_str(row.get("end_of_life_date"))

        if not any([launch, eos, eoss, eol]):
            skipped += 1
            continue

        sets = []
        if launch: sets.append(f"release_date = {sql_val(launch)}")
        if eos:    sets.append(f"end_of_sale_date = {sql_val(eos)}")
        if eoss:   sets.append(f"end_of_support_date = {sql_val(eoss)}")
        if eol:    sets.append(f"end_of_service_life_date = {sql_val(eol)}")

        source = row.get("source_method", "")
        comment = f"source: {source}" if source else None
        comment_str = f"  -- {comment}" if comment else ""

        lines.append(
            f"UPDATE product_catalog SET {', '.join(sets)} "
            f"WHERE sku_name = {sql_val(sku)};{comment_str}"
        )
        updated += 1

    lines.append(f"\n-- Lifecycle updates: {updated} rows updated, {skipped} skipped (no dates).")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Generate Phase 2 seed SQL for CPQ components")
    ap.add_argument("--dry-run", action="store_true", help="Show counts only, do not write file")
    args = ap.parse_args()

    # Load all sources
    print("Loading source files...")
    hw        = load_csv(CPQ_DIR / "05_hardware_components.csv")
    sw        = load_csv(CPQ_DIR / "06_software_licenses.csv")
    specs     = load_csv(CPQ_DIR / "07_component_specs.csv")
    servers   = load_csv(CPQ_DIR / "01_servers.csv")
    defaults  = load_csv(CPQ_DIR / "03_server_default_components.csv")
    options   = load_csv(CPQ_DIR / "04_server_selectable_options.csv")
    lifecycle = load_csv(OUTPUT_DIR / "07c_product_lifecycle.csv")

    # Validation counts
    skippable_opts = sum(1 for r in options if r["option_value"].strip() in SKIP_OPTION_VALUES
                         or r["option_category"].strip() == "IPMI Card")
    active_opts    = len(options) - skippable_opts

    print(f"  Hardware components : {len(hw)}")
    print(f"  Software licenses   : {len(sw)}")
    print(f"  Component specs     : {len(specs)}")
    print(f"  Server default rows : {len(defaults)}")
    print(f"  Selectable options  : {active_opts} active, {skippable_opts} skipped")
    print(f"  Lifecycle rows      : {len(lifecycle)}")
    print(f"  Stub rows           : {len(STUB_COMPONENTS)}")

    if args.dry_run:
        print("\n--dry-run: nothing written.")
        return

    lines = [
        "-- =================================================================",
        "-- CPQ Replacement — Phase 2 Seed Data",
        "-- Generated by generate_seed_phase2.py",
        "-- Apply AFTER seed_data.sql (Phase 1)",
        "-- =================================================================",
        "\nBEGIN;",
    ]

    gen_product_types(lines)
    gen_component_catalog(lines, hw, sw)
    gen_component_specs(lines, specs)
    gen_component_pricing(lines, hw, sw)
    gen_product_capex(lines, servers)
    gen_server_default_components(lines, defaults)
    gen_server_selectable_options(lines, options)
    gen_lifecycle_updates(lines, lifecycle)

    lines.append("\nCOMMIT;")
    lines.append("\n-- Run tests/validate_seed.py after applying to verify counts.")

    sql = "\n".join(lines)
    out = OUTPUT_DIR / "seed_data_phase2.sql"
    out.write_text(sql, encoding="utf-8")

    # Summary
    inserts  = sql.count("\nINSERT INTO")
    updates  = sql.count("\nUPDATE ")
    print(f"\nWritten → {out}")
    print(f"  INSERT statements : {inserts}")
    print(f"  UPDATE statements : {updates}")
    print("\nNext step:")
    print("  psql $SUPABASE_DB_URL -f output/seed_data_phase2.sql")
    print("  python tests/validate_seed.py")


if __name__ == "__main__":
    main()
