"""
validate_seed_phase2.py
------------------------
Phase 2 validation suite — runs after seed_data.sql + seed_data_phase2.sql are applied.
Covers: component catalog, component specs, component pricing, product capex,
        server default components, server selectable options, lifecycle dates.

Also re-runs all Phase 1 row count assertions with updated totals.

Usage:
    cd projects/cpq-replacement-db-only
    python tests/validate_seed_phase2.py

Env vars:
    SUPABASE_URL   — https://<project-ref>.supabase.co
    SUPABASE_KEY   — anon or service-role key

Exit codes:
    0 — all assertions passed
    1 — one or more assertions failed
"""

import json
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT    = Path(__file__).parent.parent.parent.parent
OUTPUTS = Path(__file__).parent / "outputs"
OUTPUTS.mkdir(parents=True, exist_ok=True)

load_dotenv(ROOT / ".env")


# ---------------------------------------------------------------------------
# Ground-truth reference values  (sourced directly from CPQ v28 CSVs)
# ---------------------------------------------------------------------------
REFERENCE = {

    # -- Phase 1 (unchanged tables) ----------------------------------------
    "row_counts_phase1": {
        "fx_rates":               330,
        "server_specs":            18,
        "server_dc_availability":  88,
        "dc_cost_drivers":         54,
        "overhead_constants":       8,
        "pending_fusion_id":        2,
    },

    # -- Phase 2 row counts ------------------------------------------------
    "row_counts_phase2": {
        # 18 servers (phase1) + 59 hardware + 85 software + 11 bundled stubs
        "product_catalog":              173,
        # 204 server pricing (phase1) + 476 component pricing
        "product_pricing":              680,
        # CPU/RAM/Drive/NIC — PSU has no applicable spec columns
        "component_specs":               58,
        # 16 server SKUs with capex_usd > 0
        "product_capex":                 16,
        # 03_server_default_components minus Monitoring rows, deduped
        "server_default_components":    108,
        # 04_server_selectable_options minus No Upgrades/IPMI, deduped
        "server_selectable_options":    604,
    },

    # -- Component catalog spot checks -------------------------------------
    "component_catalog": {
        "processor_count":    21,   # 19 from 05 + 2 stubs (6517P, Gold 6326)
        "ram_count":          23,
        "drive_count":        16,   # 14 from 05 + 2 stubs (960 GB SSD, 8 TB SATA)
        "psu_count":           6,   # 1 from 05 + 5 stubs (Dual/Single/Redundant PSUs)
        "nic_count":           2,
        "os_count":           25,
        "sql_count":           5,
        "backup_count":       43,
        "monitoring_count":    4,
        "stub_skus": {
            "Hardware RAID Controller",
            "1000 Mbit Connection - GigE",
            "960 GB SSD",
            "8 TB SATA",
            "Dual 550W PSU",
            "Dual 800W PSU",
            "Redundant 1100W Power Supply",
            "Redundant Power Supply (750W / 1100W)",
            "Single Power Supply",
            "Default Intel Xeon 6517P 16 core",
            "Intel Xeon Gold 6326 2.9GHz 16 Cores/32T",
        },
    },

    # -- Component specs spot checks ---------------------------------------
    "component_specs": {
        "gold_6226": {
            "sku":       "Intel Xeon Gold 6226 2.7GHz 12 Cores/24T",
            "cores":     12,
            "watts":     125,
            "clock_ghz": 2.7,
        },
        "bronze_3106": {
            "sku":   "Intel Xeon Bronze 3106 1.7 GHz 8 Cores/8T",
            "cores": 8,
            "watts": 85,
        },
        "ram_64gb_ddr4": {
            "sku":    "64 GB DDR4 RAM",
            "ram_gb": 64,
        },
    },

    # -- Component pricing spot checks ------------------------------------
    "component_pricing": {
        "bronze_3106": {
            "sku":         "Intel Xeon Bronze 3106 1.7 GHz 8 Cores/8T",
            "currency":    "USD",
            "term_12_mrc": 58.0,
        },
        "default_bronze_3106_no_price": {
            "sku": "Default Xeon Bronze 3106 1.7 GHz 8 Cores/8T",
        },
        "lm_standard": {
            "sku":        "LM Standard Monitoring",
            "currency":   "USD",
            "term_0_mrc": 25.0,
        },
    },

    # -- Product capex spot checks ----------------------------------------
    "product_capex": {
        "pro_6_m": {
            "sku":              "Pro Series 6.0 - M",
            "procured_price":   7569.0,
            "currency":         "USD",
            "residual_pct_12m": 0.4,
            "residual_pct_24m": 0.2,
        },
        "no_capex_skus": {
            "Cluster 5.0 (Dell R440)",
            "Atomic 5.0 (Dell R650xs)",
        },
    },

    # -- Server default components ----------------------------------------
    "server_defaults": {
        "pro_7": {
            "sku":   "Pro Series 7.0",
            "count": 6,
            "must_include": {
                "Default Intel Xeon 6517P 16 core",
                "256 GB DDR5 RAM",
                "Hardware RAID Controller",
                "1000 Mbit Connection - GigE",
            },
        },
        "essential_6": {
            "sku":   "Essential Series 6.0 - M",
            "count": 6,
        },
    },

    # -- Selectable options -----------------------------------------------
    "selectable_options": {
        "adv_6_vhost_cpus": {
            "sku":      "Advanced Series 6.0 vHost",
            "category": "cpu",
            "count":    3,
            "must_include": {
                "Intel Xeon Silver 4514Y 2G, 16C/32T",
                "Intel Xeon Gold 6534 4G, 8C/16T",
                "Intel Xeon Gold 6526Y 2.9G, 16/32T",
            },
        },
        "forbidden_values": {"No Upgrades Available", "IPMI Card"},
    },

    # -- Lifecycle dates --------------------------------------------------
    "lifecycle": {
        "sql_2022_std": {
            "sku":  "SQL Server 2022 Standard Edition",
            "eoss": "2028-01-11",
            "eol":  "2033-01-11",
        },
        "ws_2019_std": {
            "sku":  "Windows Server 2019 Standard Edition",
            "eoss": "2024-01-09",
            "eol":  "2029-01-09",
        },
        "ubuntu_2204": {
            "sku":    "Ubuntu 22.04 LTS",
            "launch": "2022-04-21",
            "eol":    "2032-04-09",
        },
        "centos_8": {
            "sku": "CentOS 8",
            "eol": "2021-12-31",
        },
        "bronze_3106_eol": {
            "sku":  "Intel Xeon Bronze 3106 1.7 GHz 8 Cores/8T",
            "eoss": "2023-12-31",
        },
        "granite_rapids_no_eol": {
            "sku":         "Intel Xeon Gold 6526Y 2.9G, 16/32T",
            "has_launch":  True,
            "eol_is_null": True,
        },
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def json_serial(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def _result(test, desc, failures, rows=None):
    return {
        "test":        test,
        "description": desc,
        "passed":      len(failures) == 0,
        "failures":    failures,
        "rows":        rows or [],
    }


# ---------------------------------------------------------------------------
# Phase 1 regression
# ---------------------------------------------------------------------------

def test_phase1_row_counts(client):
    ref = REFERENCE["row_counts_phase1"]
    failures, rows = [], []
    for table, exp in ref.items():
        resp = client.table(table).select("*", count="exact").limit(0).execute()
        actual = resp.count
        ok = actual == exp
        rows.append({"table": table, "expected": exp, "actual": actual, "ok": ok})
        if not ok:
            failures.append(f"{table}: expected {exp}, got {actual}")
    return _result("phase1_row_counts",
                   "Phase 1 tables unchanged after Phase 2 seed", failures, rows)


# ---------------------------------------------------------------------------
# Phase 2 row counts
# ---------------------------------------------------------------------------

def test_phase2_row_counts(client):
    ref = REFERENCE["row_counts_phase2"]
    failures, rows = [], []
    for table, exp in ref.items():
        resp = client.table(table).select("*", count="exact").limit(0).execute()
        actual = resp.count
        ok = actual == exp
        rows.append({"table": table, "expected": exp, "actual": actual, "ok": ok})
        if not ok:
            failures.append(f"{table}: expected {exp}, got {actual}")
    return _result("phase2_row_counts",
                   "All Phase 2 tables have expected row counts", failures, rows)


# ---------------------------------------------------------------------------
# Component catalog
# ---------------------------------------------------------------------------

def test_component_catalog_categories(client):
    ref = REFERENCE["component_catalog"]
    checks = {
        "cpu": ref["processor_count"], "ram": ref["ram_count"],
        "drive": ref["drive_count"],   "psu": ref["psu_count"],
        "nic": ref["nic_count"],       "os": ref["os_count"],
        "sql": ref["sql_count"],       "backup": ref["backup_count"],
        "monitoring": ref["monitoring_count"],
    }
    failures, rows = [], []
    for type_code, exp in checks.items():
        resp = (client.table("product_catalog")
                .select("*", count="exact")
                .eq("product_type_code", type_code)
                .eq("level", "Component")
                .limit(0).execute())
        actual = resp.count
        ok = actual == exp
        rows.append({"type_code": type_code, "expected": exp, "actual": actual, "ok": ok})
        if not ok:
            failures.append(f"type_code={type_code}: expected {exp}, got {actual}")
    return _result("component_catalog_categories",
                   "Component catalog counts match 05/06 source per category", failures, rows)


def test_stub_components_exist(client):
    stubs = REFERENCE["component_catalog"]["stub_skus"]
    failures, rows = [], []
    for sku in sorted(stubs):
        resp = (client.table("product_catalog")
                .select("sku_name").eq("sku_name", sku).limit(1).execute())
        found = len(resp.data) > 0
        rows.append({"sku": sku, "found": found})
        if not found:
            failures.append(f"Missing stub: '{sku}'")
    return _result("stub_components_exist",
                   "All 11 bundled stub component SKUs exist in product_catalog", failures, rows)


def test_no_component_filed_as_tls(client):
    resp = (client.table("product_catalog")
            .select("sku_name, product_type_code")
            .eq("level", "TLS")
            .not_.in_("product_type_code", ["server"])
            .execute())
    bad = resp.data
    failures = [f"TLS but not server: {r['sku_name']} ({r['product_type_code']})" for r in bad]
    return _result("no_component_filed_as_tls",
                   "No component-type products incorrectly filed as TLS", failures, bad)


# ---------------------------------------------------------------------------
# Component specs
# ---------------------------------------------------------------------------

def test_component_specs_spot_checks(client):
    failures, rows = [], []

    # Gold 6226
    ref = REFERENCE["component_specs"]["gold_6226"]
    resp = (client.table("component_specs")
            .select("cores, watts, clock_ghz, product_catalog!inner(sku_name)")
            .eq("product_catalog.sku_name", ref["sku"]).limit(1).execute())
    if not resp.data:
        failures.append(f"No spec row for: {ref['sku']}")
    else:
        r = resp.data[0]
        rows.append({"sku": ref["sku"], **{k: v for k, v in r.items() if k != "product_catalog"}})
        if r["cores"] != ref["cores"]:
            failures.append(f"Gold 6226 cores={r['cores']} expected={ref['cores']}")
        if r["watts"] != ref["watts"]:
            failures.append(f"Gold 6226 watts={r['watts']} expected={ref['watts']}")
        if abs(float(r["clock_ghz"] or 0) - ref["clock_ghz"]) > 0.01:
            failures.append(f"Gold 6226 clock_ghz={r['clock_ghz']} expected={ref['clock_ghz']}")

    # Bronze 3106
    ref = REFERENCE["component_specs"]["bronze_3106"]
    resp = (client.table("component_specs")
            .select("cores, watts, product_catalog!inner(sku_name)")
            .eq("product_catalog.sku_name", ref["sku"]).limit(1).execute())
    if not resp.data:
        failures.append(f"No spec row for: {ref['sku']}")
    else:
        r = resp.data[0]
        rows.append({"sku": ref["sku"], **{k: v for k, v in r.items() if k != "product_catalog"}})
        if r["cores"] != ref["cores"]:
            failures.append(f"Bronze 3106 cores={r['cores']} expected={ref['cores']}")
        if r["watts"] != ref["watts"]:
            failures.append(f"Bronze 3106 watts={r['watts']} expected={ref['watts']}")

    # 64 GB DDR4
    ref = REFERENCE["component_specs"]["ram_64gb_ddr4"]
    resp = (client.table("component_specs")
            .select("ram_gb, product_catalog!inner(sku_name)")
            .eq("product_catalog.sku_name", ref["sku"]).limit(1).execute())
    if not resp.data:
        failures.append(f"No spec row for: {ref['sku']}")
    else:
        r = resp.data[0]
        rows.append({"sku": ref["sku"], "ram_gb": r["ram_gb"]})
        if r["ram_gb"] != ref["ram_gb"]:
            failures.append(f"64 GB DDR4 ram_gb={r['ram_gb']} expected={ref['ram_gb']}")

    return _result("component_specs_spot_checks",
                   "CPU core/watt/clock and RAM capacity match Intel ARK / CPQ v28", failures, rows)


def test_no_psu_spec_rows(client):
    resp = (client.table("component_specs")
            .select("product_catalog!inner(sku_name, product_type_code)")
            .eq("product_catalog.product_type_code", "psu").execute())
    bad = resp.data
    failures = [f"Unexpected PSU spec row: {r['product_catalog']['sku_name']}" for r in bad]
    return _result("no_psu_spec_rows",
                   "PSU components have no component_specs rows (no applicable columns)",
                   failures, bad)


# ---------------------------------------------------------------------------
# Component pricing
# ---------------------------------------------------------------------------

def test_component_pricing_spot_checks(client):
    failures, rows = [], []

    # Bronze 3106 MRC $58 at 12m
    ref = REFERENCE["component_pricing"]["bronze_3106"]
    resp = (client.table("product_pricing")
            .select("term_months, mrc, product_catalog!inner(sku_name)")
            .eq("product_catalog.sku_name", ref["sku"])
            .eq("currency_code", ref["currency"])
            .eq("term_months", 12).limit(1).execute())
    if not resp.data:
        failures.append(f"No pricing row for {ref['sku']} term=12")
    else:
        r = resp.data[0]
        rows.append(r)
        if abs(float(r["mrc"]) - ref["term_12_mrc"]) > 0.01:
            failures.append(f"Bronze 3106 12m mrc={r['mrc']} expected={ref['term_12_mrc']}")

    # LM Standard Monitoring MRC $25 MTM
    ref = REFERENCE["component_pricing"]["lm_standard"]
    resp = (client.table("product_pricing")
            .select("term_months, mrc, product_catalog!inner(sku_name)")
            .eq("product_catalog.sku_name", ref["sku"])
            .eq("currency_code", ref["currency"])
            .eq("term_months", 0).limit(1).execute())
    if not resp.data:
        failures.append(f"No pricing row for {ref['sku']} term=0")
    else:
        r = resp.data[0]
        rows.append(r)
        if abs(float(r["mrc"]) - ref["term_0_mrc"]) > 0.01:
            failures.append(f"LM Standard MTM mrc={r['mrc']} expected={ref['term_0_mrc']}")

    return _result("component_pricing_spot_checks",
                   "Component MRC values match 05/06 source for Bronze 3106 and LM Standard",
                   failures, rows)


def test_zero_price_defaults_not_seeded(client):
    sku = REFERENCE["component_pricing"]["default_bronze_3106_no_price"]["sku"]
    resp = (client.table("product_pricing")
            .select("mrc, nrc, product_catalog!inner(sku_name)")
            .eq("product_catalog.sku_name", sku).execute())
    bad = [r for r in resp.data if (float(r["mrc"] or 0) + float(r["nrc"] or 0)) > 0]
    failures = [f"Non-zero price for zero-price default {sku}: mrc={r['mrc']} nrc={r['nrc']}"
                for r in bad]
    return _result("zero_price_defaults_not_seeded",
                   "Default Xeon Bronze 3106 (zero-price default) has no non-zero pricing rows",
                   failures, resp.data)


# ---------------------------------------------------------------------------
# Product capex
# ---------------------------------------------------------------------------

def test_product_capex_spot_checks(client):
    failures, rows = [], []

    ref = REFERENCE["product_capex"]["pro_6_m"]
    resp = (client.table("product_capex")
            .select("procured_price, procured_currency, residual_pct_12m, residual_pct_24m, "
                    "product_catalog!inner(sku_name)")
            .eq("product_catalog.sku_name", ref["sku"]).limit(1).execute())
    if not resp.data:
        failures.append(f"No capex row for {ref['sku']}")
    else:
        r = resp.data[0]
        rows.append(r)
        if abs(float(r["procured_price"]) - ref["procured_price"]) > 1.0:
            failures.append(f"Pro 6.0-M capex={r['procured_price']} expected≈{ref['procured_price']}")
        if r["procured_currency"] != ref["currency"]:
            failures.append(f"Pro 6.0-M currency={r['procured_currency']} expected={ref['currency']}")
        if abs(float(r["residual_pct_12m"] or 0) - ref["residual_pct_12m"]) > 0.001:
            failures.append(f"Pro 6.0-M residual_12m={r['residual_pct_12m']} expected={ref['residual_pct_12m']}")
        if abs(float(r["residual_pct_24m"] or 0) - ref["residual_pct_24m"]) > 0.001:
            failures.append(f"Pro 6.0-M residual_24m={r['residual_pct_24m']} expected={ref['residual_pct_24m']}")

    for sku in REFERENCE["product_capex"]["no_capex_skus"]:
        resp = (client.table("product_capex")
                .select("id, product_catalog!inner(sku_name)")
                .eq("product_catalog.sku_name", sku).execute())
        if resp.data:
            failures.append(f"{sku} has capex rows but capex_usd=0 in source")

    return _result("product_capex_spot_checks",
                   "Capex amounts and residual percentages match 01_servers.csv", failures, rows)


def test_capex_use_as_baseline(client):
    resp = (client.table("product_capex")
            .select("id, product_catalog!inner(sku_name)")
            .eq("use_as_baseline", False).execute())
    bad = resp.data
    failures = [f"use_as_baseline=false: {r['product_catalog']['sku_name']}" for r in bad]
    return _result("capex_use_as_baseline",
                   "All seeded product_capex rows have use_as_baseline=true", failures, bad)


# ---------------------------------------------------------------------------
# Server default components
# ---------------------------------------------------------------------------

def test_server_default_components_spot_checks(client):
    failures, rows = [], []
    for key, ref in REFERENCE["server_defaults"].items():
        sku = ref["sku"]
        cat_resp = (client.table("product_catalog")
                    .select("id").eq("sku_name", sku).limit(1).execute())
        if not cat_resp.data:
            failures.append(f"{sku}: server not found in product_catalog")
            rows.append({"server": sku, "count": 0})
            continue
        server_product_id = cat_resp.data[0]["id"]
        resp = (client.table("server_default_components")
                .select("component_type, "
                        "server:product_catalog!server_default_components_server_product_id_fkey(sku_name), "
                        "component:product_catalog!server_default_components_component_product_id_fkey(sku_name)")
                .eq("server_product_id", server_product_id).execute())
        count = len(resp.data)
        rows.append({"server": sku, "count": count})
        if count != ref["count"]:
            failures.append(f"{sku}: expected {ref['count']} defaults, got {count}")
        if "must_include" in ref:
            actual_skus = {r["component"]["sku_name"] for r in resp.data}
            missing = ref["must_include"] - actual_skus
            if missing:
                failures.append(f"{sku} missing defaults: {sorted(missing)}")
    return _result("server_default_components_spot_checks",
                   "Pro 7.0 and Essential 6.0-M default component counts and SKUs match CPQ v28",
                   failures, rows)


def test_no_monitoring_in_defaults(client):
    resp = (client.table("server_default_components")
            .select("component_type, component:component_product_id(sku_name)")
            .eq("component_type", "monitoring").execute())
    bad = resp.data
    failures = [f"Monitoring in defaults: {r['component']['sku_name']}" for r in bad]
    return _result("no_monitoring_in_defaults",
                   "Monitoring not in server_default_components (handled via software licensing)",
                   failures, bad)


# ---------------------------------------------------------------------------
# Selectable options
# ---------------------------------------------------------------------------

def test_selectable_options_spot_checks(client):
    failures, rows = [], []
    ref = REFERENCE["selectable_options"]["adv_6_vhost_cpus"]
    cat_resp = (client.table("product_catalog")
                .select("id").eq("sku_name", ref["sku"]).limit(1).execute())
    if not cat_resp.data:
        failures.append(f"{ref['sku']}: server not found in product_catalog")
        rows.append({"server": ref["sku"], "category": ref["category"], "count": 0, "skus": []})
        return _result("selectable_options_spot_checks",
                       "Advanced Series 6.0 vHost CPU options match CPQ v28", failures, rows)
    server_product_id = cat_resp.data[0]["id"]
    resp = (client.table("server_selectable_options")
            .select("category, "
                    "server:product_catalog!server_selectable_options_server_product_id_fkey(sku_name), "
                    "component:product_catalog!server_selectable_options_component_product_id_fkey(sku_name)")
            .eq("server_product_id", server_product_id)
            .eq("category", ref["category"]).execute())
    count = len(resp.data)
    actual_skus = {r["component"]["sku_name"] for r in resp.data}
    rows.append({"server": ref["sku"], "category": ref["category"],
                 "count": count, "skus": sorted(actual_skus)})
    if count != ref["count"]:
        failures.append(f"Advanced 6.0 vHost CPU options: expected {ref['count']}, got {count}")
    missing = ref["must_include"] - actual_skus
    if missing:
        failures.append(f"Advanced 6.0 vHost missing CPU options: {sorted(missing)}")
    return _result("selectable_options_spot_checks",
                   "Advanced Series 6.0 vHost CPU options match CPQ v28", failures, rows)


def test_no_placeholder_options(client):
    forbidden = REFERENCE["selectable_options"]["forbidden_values"]
    failures, rows = [], []
    for val in forbidden:
        # Look up the catalog id for this placeholder sku first
        cat_resp = (client.table("product_catalog")
                    .select("id").eq("sku_name", val).limit(1).execute())
        if not cat_resp.data:
            continue  # placeholder not in catalog at all — pass
        comp_id = cat_resp.data[0]["id"]
        resp = (client.table("server_selectable_options")
                .select("id, component_product_id")
                .eq("component_product_id", comp_id).execute())
        if resp.data:
            failures.append(f"Placeholder in selectable options: '{val}' ({len(resp.data)} rows)")
            rows.extend(resp.data)
    return _result("no_placeholder_options",
                   "No 'No Upgrades Available' or 'IPMI Card' rows in server_selectable_options",
                   failures, rows)


def test_selectable_options_display_order(client):
    resp = (client.table("server_selectable_options")
            .select("id, server:product_catalog!server_selectable_options_server_product_id_fkey(sku_name)")
            .is_("display_order", "null").execute())
    bad = resp.data
    failures = [f"NULL display_order: id={r['id']} server={r['server']['sku_name']}"
                for r in bad]
    return _result("selectable_options_display_order",
                   "All server_selectable_options rows have a non-null display_order",
                   failures, bad)


# ---------------------------------------------------------------------------
# Lifecycle dates
# ---------------------------------------------------------------------------

def test_lifecycle_date_spot_checks(client):
    failures, rows = [], []

    checks = [
        ("sql_2022_std",    "end_of_support_date",      "eoss"),
        ("sql_2022_std",    "end_of_service_life_date",  "eol"),
        ("ws_2019_std",     "end_of_support_date",      "eoss"),
        ("ws_2019_std",     "end_of_service_life_date",  "eol"),
        ("ubuntu_2204",     "release_date",              "launch"),
        ("ubuntu_2204",     "end_of_service_life_date",  "eol"),
        ("centos_8",        "end_of_service_life_date",  "eol"),
        ("bronze_3106_eol", "end_of_support_date",      "eoss"),
    ]

    for ref_key, db_field, ref_field in checks:
        ref = REFERENCE["lifecycle"][ref_key]
        sku = ref["sku"]
        expected = ref.get(ref_field)
        if expected is None:
            continue
        resp = (client.table("product_catalog")
                .select(f"sku_name, {db_field}")
                .eq("sku_name", sku).limit(1).execute())
        if not resp.data:
            failures.append(f"No product_catalog row for: {sku}")
            continue
        r = resp.data[0]
        rows.append({"sku": sku, "field": db_field, "value": r.get(db_field)})
        actual = str(r.get(db_field) or "")[:10]
        if actual != expected:
            failures.append(f"{sku} {db_field}={actual!r} expected={expected!r}")

    return _result("lifecycle_date_spot_checks",
                   "SQL Server, Windows Server, Ubuntu, CentOS 8, Bronze 3106 lifecycle dates correct",
                   failures, rows)


def test_granite_rapids_no_eol(client):
    ref = REFERENCE["lifecycle"]["granite_rapids_no_eol"]
    resp = (client.table("product_catalog")
            .select("sku_name, release_date, end_of_service_life_date")
            .eq("sku_name", ref["sku"]).limit(1).execute())
    failures = []
    if not resp.data:
        failures.append(f"No product_catalog row for: {ref['sku']}")
    else:
        r = resp.data[0]
        if ref["has_launch"] and not r.get("release_date"):
            failures.append(f"{ref['sku']} has no release_date — expected one")
        if ref["eol_is_null"] and r.get("end_of_service_life_date"):
            failures.append(f"{ref['sku']} has EOL {r['end_of_service_life_date']} — expected NULL (current gen)")
    return _result("granite_rapids_no_eol",
                   "Granite Rapids (Gold 6526Y) has launch date but no EOL — current generation",
                   failures, resp.data)


def test_skipped_drives_no_lifecycle(client):
    skipped = ["1 TB 7200 6 Gb/s SATA", "480 GB SATA 2.5in SSD", "960 GB NVMe u.2 2.5in"]
    failures, rows = [], []
    for sku in skipped:
        resp = (client.table("product_catalog")
                .select("sku_name, release_date, end_of_sale_date, "
                        "end_of_support_date, end_of_service_life_date")
                .eq("sku_name", sku).limit(1).execute())
        if not resp.data:
            continue
        r = resp.data[0]
        rows.append(r)
        for f in ["release_date", "end_of_sale_date", "end_of_support_date", "end_of_service_life_date"]:
            if r.get(f):
                failures.append(f"{sku}.{f}={r[f]} — generic drive should have NULL dates")
    return _result("skipped_drives_no_lifecycle",
                   "Generic drive SKUs have NULL lifecycle dates",
                   failures, rows)


# ---------------------------------------------------------------------------
# Referential integrity
# ---------------------------------------------------------------------------

def test_fk_component_specs(client):
    resp = (client.table("component_specs")
            .select("product_id, product_catalog!inner(sku_name)")
            .limit(200).execute())
    failures = [] if resp.data is not None else ["component_specs FK query failed"]
    return _result("fk_component_specs",
                   "component_specs.product_id FK intact — all rows join to product_catalog",
                   failures, [{"count": len(resp.data)}])


def test_fk_server_default_components(client):
    resp = (client.table("server_default_components")
            .select("component:component_product_id(sku_name)")
            .limit(200).execute())
    broken = [r for r in resp.data if r.get("component") is None]
    failures = [f"Broken FK in server_default_components: {r}" for r in broken]
    return _result("fk_server_default_components",
                   "All server_default_components.component_product_id FKs valid",
                   failures, [{"broken": len(broken)}])


def test_fk_server_selectable_options(client):
    resp = (client.table("server_selectable_options")
            .select("component:component_product_id(sku_name)")
            .limit(700).execute())
    broken = [r for r in resp.data if r.get("component") is None]
    failures = [f"Broken FK in server_selectable_options: {r}" for r in broken]
    return _result("fk_server_selectable_options",
                   "All server_selectable_options.component_product_id FKs valid",
                   failures, [{"broken": len(broken)}])


# ---------------------------------------------------------------------------
# Phase 1 carry-forward tests
# ---------------------------------------------------------------------------

def test_pro6_cad_pricing(client):
    sku = "Pro Series 6.0 - M"
    ref = {0: (1249.0, 1249.0), 12: (1249.0, 1249.0), 24: (969.0, 1249.0), 36: (829.0, 1249.0)}
    resp = (client.table("product_pricing")
            .select("term_months, mrc, nrc, product_catalog!inner(sku_name)")
            .eq("product_catalog.sku_name", sku)
            .eq("currency_code", "CAD")
            .order("term_months").execute())
    rows = [{"term_months": r["term_months"], "mrc": r["mrc"], "nrc": r["nrc"]} for r in resp.data]
    failures = []
    for row in rows:
        term = row["term_months"]
        if term in ref:
            exp_mrc, exp_nrc = ref[term]
            if abs(float(row["mrc"]) - exp_mrc) > 0.01:
                failures.append(f"term={term} mrc={row['mrc']} expected={exp_mrc}")
    return _result("pro6_cad_pricing",
                   "Pro Series 6.0 - M CAD pricing unchanged after Phase 2 seed", failures, rows)


def test_cluster_atomic_no_por(client):
    failures, rows = [], {}
    for sku in ("Cluster 5.0 (Dell R440)", "Atomic 5.0 (Dell R650xs)"):
        resp = (client.table("server_dc_availability")
                .select("dc_code, product_catalog!inner(sku_name)")
                .eq("product_catalog.sku_name", sku).execute())
        dcs = {r["dc_code"] for r in resp.data}
        rows[sku] = sorted(dcs)
        if "POR" in dcs:
            failures.append(f"{sku} has POR — NA-only hardware")
    return _result("cluster_atomic_no_por",
                   "Cluster 5.0 and Atomic 5.0 not available in POR", failures, rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

TESTS = [
    # Phase 1 regression
    test_phase1_row_counts,
    test_pro6_cad_pricing,
    test_cluster_atomic_no_por,
    # Phase 2 counts
    test_phase2_row_counts,
    # Component catalog
    test_component_catalog_categories,
    test_stub_components_exist,
    test_no_component_filed_as_tls,
    # Specs
    test_component_specs_spot_checks,
    test_no_psu_spec_rows,
    # Pricing
    test_component_pricing_spot_checks,
    test_zero_price_defaults_not_seeded,
    # Capex
    test_product_capex_spot_checks,
    test_capex_use_as_baseline,
    # Default components
    test_server_default_components_spot_checks,
    test_no_monitoring_in_defaults,
    # Selectable options
    test_selectable_options_spot_checks,
    test_no_placeholder_options,
    test_selectable_options_display_order,
    # Lifecycle
    test_lifecycle_date_spot_checks,
    test_granite_rapids_no_eol,
    test_skipped_drives_no_lifecycle,
    # FK integrity
    test_fk_component_specs,
    test_fk_server_default_components,
    test_fk_server_selectable_options,
]


def main():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        print("ERROR: SUPABASE_URL and SUPABASE_KEY must be set in .env")
        sys.exit(1)
    try:
        client = create_client(url, key)
    except Exception as e:
        print(f"ERROR: Could not create Supabase client: {e}")
        sys.exit(1)

    print(f"Running {len(TESTS)} tests...\n")
    results = []
    for fn in TESTS:
        try:
            result = fn(client)
        except Exception as e:
            result = {"test": fn.__name__, "passed": False,
                      "failures": [f"Exception: {e}"], "rows": []}
        status = "✓ PASS" if result["passed"] else "✗ FAIL"
        print(f"  {status}  {result['test']}")
        for f in result.get("failures", []):
            print(f"           → {f}")
        results.append(result)

    passed = sum(1 for r in results if r["passed"])
    total  = len(results)
    summary = {
        "run_at":     datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "passed":     passed,
        "failed":     total - passed,
        "total":      total,
        "all_passed": passed == total,
        "tests":      results,
    }

    out_path = OUTPUTS / "validation_results_phase2.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2, default=json_serial)

    print()
    print(f"{'ALL PASSED' if summary['all_passed'] else 'FAILURES FOUND'}  ({passed}/{total})")
    print(f"Results → {out_path}")
    sys.exit(0 if summary["all_passed"] else 1)


if __name__ == "__main__":
    main()
