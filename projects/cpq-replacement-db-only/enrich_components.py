"""
enrich_components.py
---------------------
Enriches hardware component specs from CPQ extracted CSVs.

Three-layer pipeline per component:
  1. Deterministic parse  — regex on sku name + CSV columns        (confidence 1.0)
  2. LLM grounded         — Perplexity sonar-pro with web search   (confidence 0.85)
  3. LLM inferred         — fallback if grounding finds no source  (confidence 0.60)

Outputs:
  output/component_specs_enriched.json   full enrichment record with confidence metadata
  cpq-extracted/07_component_specs.csv   clean values only, consumed by generate_seed.py

Usage:
    cd projects/cpq-replacement-db-only
    python enrich_components.py [--dry-run] [--category CATEGORY] [--force]

    --dry-run         Parse only, no LLM calls. Good for validating regex layer first.
    --category NAME   Process only one category (e.g. Processor, RAM, Drive)
    --force           Re-enrich even if output already exists (default: skip cached)

Env vars (connected-brain root .env):
    OPENROUTER_API_KEY   required unless --dry-run
    MODEL_SEARCH         optional, default perplexity/sonar-pro
    TEMPERATURE_SEARCH   optional, default 0.1
    LLM_MAX_RETRIES      optional, default 3
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent
REPO_ROOT    = PROJECT_ROOT.parent.parent.parent   # connected-brain/
EXTRACTED    = PROJECT_ROOT / "cpq-extracted"
OUTPUT       = PROJECT_ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

load_dotenv(REPO_ROOT / ".env")

sys.path.insert(0, str(PROJECT_ROOT / "connectors"))
import openrouter  # noqa: E402

# ---------------------------------------------------------------------------
# I/O paths
# ---------------------------------------------------------------------------
HARDWARE_CSV  = EXTRACTED / "05_hardware_components.csv"
SOFTWARE_CSV  = EXTRACTED / "06_software_licenses.csv"
ENRICHED_JSON = OUTPUT     / "component_specs_enriched.json"
SPECS_CSV     = EXTRACTED  / "07_component_specs.csv"

# ---------------------------------------------------------------------------
# Confidence levels
# ---------------------------------------------------------------------------
CONFIDENCE = {
    "csv":            1.00,
    "parsed":         1.00,
    "llm_grounded":   0.85,
    "llm_correction": 0.75,
    "llm_inferred":   0.60,
}
REVIEW_THRESHOLD = 0.75   # any field below this sets needs_review=True

# Categories that get component_specs rows
HW_CATEGORIES = {"Processor", "RAM", "Drive", "PSU", "Network Card"}
SW_CATEGORIES = {"Monitoring", "SQL", "Remote Access", "OS", "VMWare", "Proxmox", "Backup"}

CATEGORY_TO_TYPE = {
    "Processor":    "cpu",
    "RAM":          "ram",
    "Drive":        "drive",
    "PSU":          "psu",
    "Network Card": "network_component",
    "Monitoring":   "software",
    "SQL":          "software",
    "Remote Access":"software",
    "OS":           "software",
    "VMWare":       "software",
    "Proxmox":      "software",
    "Backup":       "software",
}


# ---------------------------------------------------------------------------
# Layer 1: Deterministic parse
# ---------------------------------------------------------------------------

def _field(value, source: str) -> dict:
    return {"value": value, "source": source, "confidence": CONFIDENCE[source]}


def _safe_float(val) -> float:
    if val is None or str(val).strip() == "":
        return None
    try:
        return float(val)
    except ValueError:
        return None


def _parse_processor(sku: str, row: dict) -> dict:
    specs = {}

    # Cores / threads: "16 Cores/32T" or "16C/32T" or "16 core"
    m = re.search(r'(\d+)\s*[Cc]ores?(?:/(\d+)[Tt])?', sku)
    if not m:
        m = re.search(r'(\d+)[Cc]/(\d+)[Tt]', sku)
    if m:
        specs["cores"] = _field(int(m.group(1)), "parsed")
        if m.lastindex and m.lastindex >= 2 and m.group(2):
            specs["threads"] = _field(int(m.group(2)), "parsed")

    # Clock: "2.7GHz" or "2.7G,"
    m = re.search(r'(\d+\.\d+)\s*G(?:Hz)?', sku)
    if m:
        specs["clock_ghz"] = _field(float(m.group(1)), "parsed")

    # TDP watts from CSV
    w = _safe_float(row.get("watts_added"))
    if w and w != 0:
        specs["tdp_watts"] = _field(int(w), "csv")

    c = _safe_float(row.get("capex_usd"))
    if c and c != 0:
        specs["capex_usd"] = _field(c, "csv")

    return specs


def _parse_ram(sku: str, row: dict) -> dict:
    specs = {}
    m = re.search(r'(\d+)\s*GB\s*(DDR\d)?', sku)
    if m:
        specs["ram_gb"] = _field(int(m.group(1)), "parsed")
        if m.group(2):
            specs["ram_type"] = _field(m.group(2), "parsed")

    c = _safe_float(row.get("capex_usd"))
    if c and c != 0:
        specs["capex_usd"] = _field(c, "csv")

    return specs


def _parse_drive(sku: str, row: dict) -> dict:
    specs = {}

    m = re.search(r'([\d.]+)\s*(TB|GB)', sku, re.IGNORECASE)
    if m:
        cap  = float(m.group(1))
        unit = m.group(2).upper()
        tb   = cap if unit == "TB" else cap / 1024
        specs["drive_capacity_tb"] = _field(round(tb, 4), "parsed")

    if re.search(r'NVMe', sku, re.IGNORECASE):
        specs["drive_type"] = _field("nvme", "parsed")
    elif re.search(r'7200', sku):
        specs["drive_type"] = _field("hdd", "parsed")
    elif re.search(r'SSD|SATA', sku, re.IGNORECASE):
        specs["drive_type"] = _field("ssd", "parsed")

    c = _safe_float(row.get("capex_usd"))
    if c and c != 0:
        specs["capex_usd"] = _field(c, "csv")

    return specs


def _parse_psu(sku: str, row: dict) -> dict:
    specs = {}
    m = re.search(r'(\d+)\s*W', sku)
    if m:
        specs["watts"] = _field(int(m.group(1)), "parsed")

    c = _safe_float(row.get("capex_usd"))
    if c and c != 0:
        specs["capex_usd"] = _field(c, "csv")

    return specs


def _parse_nic(sku: str, row: dict) -> dict:
    specs = {}
    m = re.search(r'(\d+)\s*GbE', sku, re.IGNORECASE)
    if m:
        specs["speed_gbe"] = _field(int(m.group(1)), "parsed")

    m = re.search(r'(\d+)\s*[xX]\s*SFP', sku)
    if m:
        specs["ports"] = _field(int(m.group(1)), "parsed")

    c = _safe_float(row.get("capex_usd"))
    if c and c != 0:
        specs["capex_usd"] = _field(c, "csv")

    return specs


PARSERS = {
    "Processor":    _parse_processor,
    "RAM":          _parse_ram,
    "Drive":        _parse_drive,
    "PSU":          _parse_psu,
    "Network Card": _parse_nic,
}


# ---------------------------------------------------------------------------
# Layer 2: LLM grounded enrichment
# ---------------------------------------------------------------------------

LLM_FIELDS = {
    "Processor":    ["generation", "architecture", "socket", "tdp_watts",
                     "boost_ghz", "ecc_support"],
    "Drive":        ["interface", "form_factor", "sequential_read_mbps",
                     "sequential_write_mbps", "endurance_tbw"],
    "Network Card": ["chipset", "connector_type"],
}

SYSTEM_PROMPT = (
    "You are a hardware specification database. "
    "Your entire response must be a single raw JSON object — no markdown, no code fences, "
    "no explanation before or after. Start your response with { and end with }. "
    "All numeric values must be numbers, not strings. "
    "Omit any field you cannot find a reliable source for — do not guess. "
    "Include source_url (Intel ARK, manufacturer spec page, etc.). "
    "Set grounded=true if you found a primary source, false otherwise."
)


def _build_prompt(category: str, sku: str, parsed: dict) -> str:
    parsed_summary = {k: v["value"] for k, v in parsed.items() if k != "capex_usd"}
    missing = [f for f in LLM_FIELDS.get(category, []) if f not in parsed]
    return (
        f'Look up hardware specifications for: "{sku}"\n'
        f"Category: {category}\n\n"
        f"Already confirmed from product name:\n{json.dumps(parsed_summary, indent=2)}\n\n"
        f"Find these additional fields if available: {missing}\n"
        f"Also flag any parsed values above that appear incorrect.\n\n"
        f"Return JSON:\n"
        f'{{"grounded": true/false, "source_url": "...", '
        f'"fields": {{"field": value}}, "corrections": {{"field": corrected_value}}}}'
    )


def enrich_with_llm(category: str, sku: str, parsed: dict, dry_run: bool) -> dict:
    empty = {"fields": {}, "corrections": {}, "source_url": None, "grounded": False, "tokens": {}}

    if dry_run or category not in LLM_FIELDS:
        return empty

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": _build_prompt(category, sku, parsed)},
    ]

    parsed_data, raw = openrouter.search_call_json(messages=messages, max_tokens=1024)

    if parsed_data is None:
        return empty

    grounded   = bool(parsed_data.get("grounded", False))
    source_url = parsed_data.get("source_url") or (
        (raw.get("source_urls") or [None])[0] if raw else None
    )
    confidence = CONFIDENCE["llm_grounded"] if grounded else CONFIDENCE["llm_inferred"]
    src_tag    = "llm_grounded" if grounded else "llm_inferred"

    enriched = {}
    for field, value in (parsed_data.get("fields") or {}).items():
        if value is not None:
            enriched[field] = {"value": value, "source": src_tag, "confidence": confidence}

    return {
        "fields":      enriched,
        "corrections": parsed_data.get("corrections") or {},
        "source_url":  source_url,
        "grounded":    grounded,
        "tokens":      raw.get("tokens", {}) if raw else {},
    }


# ---------------------------------------------------------------------------
# Merge
# ---------------------------------------------------------------------------

def merge_specs(parsed: dict, enrichment: dict):
    merged = dict(parsed)

    for field, corrected in (enrichment.get("corrections") or {}).items():
        if field in merged and merged[field]["value"] != corrected:
            merged[field] = {
                "value":           corrected,
                "source":          "llm_correction",
                "confidence":      CONFIDENCE["llm_correction"],
                "original_parsed": merged[field]["value"],
            }

    for field, spec in (enrichment.get("fields") or {}).items():
        if field not in merged:
            merged[field] = spec

    needs_review = any(
        v.get("confidence", 1) < REVIEW_THRESHOLD
        for v in merged.values()
        if isinstance(v, dict)
    )
    return merged, needs_review


# ---------------------------------------------------------------------------
# Load CSVs
# ---------------------------------------------------------------------------

def load_components():
    rows = []
    with open(HARDWARE_CSV, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            row = {k: v.strip() for k, v in row.items()}
            if row.get("category") in HW_CATEGORIES:
                rows.append(row)
    return rows


def load_software():
    rows = []
    with open(SOFTWARE_CSV, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            row = {k: v.strip() for k, v in row.items()}
            if row.get("category") in SW_CATEGORIES:
                rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

SPECS_FIELDS = [
    "category", "sku", "product_type",
    "cores", "threads", "clock_ghz", "boost_ghz", "tdp_watts",
    "generation", "architecture", "socket", "ecc_support",
    "ram_gb", "ram_type",
    "drive_capacity_tb", "drive_type", "interface", "form_factor",
    "sequential_read_mbps", "sequential_write_mbps", "endurance_tbw",
    "watts",
    "speed_gbe", "ports", "chipset", "connector_type",
    "capex_usd",
    "source_url", "overall_confidence", "needs_review",
]


def write_enriched_json(results):
    with open(ENRICHED_JSON, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Wrote {len(results)} records → {ENRICHED_JSON.relative_to(REPO_ROOT)}")


def write_specs_csv(results):
    with open(SPECS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SPECS_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for r in results:
            if r.get("is_software"):
                continue
            flat = {
                "category":           r["category"],
                "sku":                r["sku"],
                "product_type":       r["product_type"],
                "source_url":         r.get("source_url", ""),
                "overall_confidence": r.get("overall_confidence", ""),
                "needs_review":       r.get("needs_review", False),
            }
            for field, spec in r.get("specs", {}).items():
                if isinstance(spec, dict) and "value" in spec:
                    flat[field] = spec["value"]
            writer.writerow(flat)

    flagged = sum(1 for r in results if r.get("needs_review") and not r.get("is_software"))
    print(f"  Wrote {SPECS_CSV.relative_to(REPO_ROOT)}  ({flagged} rows need review)")


# ---------------------------------------------------------------------------
# Enrichment per row
# ---------------------------------------------------------------------------

def enrich_component(row: dict, dry_run: bool) -> dict:
    category = row["category"]
    sku      = row["sku"]

    parser = PARSERS.get(category)
    parsed = parser(sku, row) if parser else {}

    enrichment = enrich_with_llm(category, sku, parsed, dry_run)
    specs, needs_review = merge_specs(parsed, enrichment)

    confidences = [v["confidence"] for v in specs.values()
                   if isinstance(v, dict) and "confidence" in v]
    overall = round(min(confidences), 2) if confidences else None

    return {
        "category":           category,
        "sku":                sku,
        "product_type":       CATEGORY_TO_TYPE.get(category, "hardware_component"),
        "is_software":        False,
        "specs":              specs,
        "source_url":         enrichment.get("source_url"),
        "grounded":           enrichment.get("grounded", False),
        "overall_confidence": overall,
        "needs_review":       needs_review,
        "tokens":             enrichment.get("tokens", {}),
    }


def enrich_software(row: dict) -> dict:
    return {
        "category":           row["category"],
        "sku":                row["sku"],
        "product_type":       CATEGORY_TO_TYPE.get(row["category"], "software"),
        "is_software":        True,
        "specs":              {},
        "pricing": {
            "nrc_usd":                   _safe_float(row.get("nrc_usd")),
            "mrc_mtm":                   _safe_float(row.get("mrc_monthly_usd")),
            "mrc_12m":                   _safe_float(row.get("mrc_12m_usd")),
            "mrc_24m":                   _safe_float(row.get("mrc_24m_usd")),
            "mrc_36m":                   _safe_float(row.get("mrc_36m_usd")),
            "software_cost_actual_usd":  _safe_float(row.get("software_cost_actual_usd")),
        },
        "notes":              row.get("notes", ""),
        "needs_review":       False,
        "overall_confidence": 1.0,
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Enrich CPQ component specs")
    ap.add_argument("--dry-run",  action="store_true", help="Parse only, skip LLM calls")
    ap.add_argument("--category", default=None,        help="Process only this category")
    ap.add_argument("--force",    action="store_true", help="Re-enrich even if cached")
    args = ap.parse_args()

    if not args.dry_run and not os.getenv("OPENROUTER_API_KEY"):
        print("ERROR: OPENROUTER_API_KEY not set in .env (use --dry-run to skip LLM)")
        sys.exit(1)

    # Load existing results unless --force
    existing = {}
    if ENRICHED_JSON.exists() and not args.force:
        with open(ENRICHED_JSON) as f:
            for r in json.load(f):
                existing[r["sku"]] = r
        print(f"  Loaded {len(existing)} cached records (--force to re-enrich all)")

    hardware = load_components()
    software = load_software()

    if args.category:
        hardware = [r for r in hardware if r["category"] == args.category]
        software = [r for r in software if r["category"] == args.category]

    results      = []
    total_tokens = {"prompt": 0, "completion": 0, "total": 0}

    print(f"\nEnriching {len(hardware)} hardware components...")
    for i, row in enumerate(hardware, 1):
        sku = row["sku"]
        if sku in existing and not args.force:
            results.append(existing[sku])
            print(f"  [{i:3d}/{len(hardware)}] SKIP  {sku}")
            continue

        mode = "dry-run" if args.dry_run else "enrich"
        print(f"  [{i:3d}/{len(hardware)}] {mode}  {sku}")
        result = enrich_component(row, args.dry_run)
        results.append(result)
        for k in total_tokens:
            total_tokens[k] += result.get("tokens", {}).get(k, 0)
        if not args.dry_run:
            time.sleep(0.5)

    print(f"\nProcessing {len(software)} software components...")
    for row in software:
        sku = row["sku"]
        results.append(existing[sku] if sku in existing and not args.force
                        else enrich_software(row))

    print()
    write_enriched_json(results)
    write_specs_csv(results)

    hw      = [r for r in results if not r.get("is_software")]
    flagged = [r for r in hw if r.get("needs_review")]
    grounded = [r for r in hw if r.get("grounded")]

    print(f"\n{'='*60}")
    print(f"  Hardware : {len(hw)}")
    print(f"  Software : {len(results) - len(hw)}")
    print(f"  Grounded : {len(grounded)}/{len(hw)}")
    print(f"  Review   : {len(flagged)}")
    if total_tokens["total"]:
        print(f"  Tokens   : {total_tokens['total']:,}")
    if flagged:
        print(f"\n  Needs review:")
        for r in flagged:
            low = [k for k, v in r.get("specs", {}).items()
                   if isinstance(v, dict) and v.get("confidence", 1) < REVIEW_THRESHOLD]
            print(f"    [{r['category']}] {r['sku']}  low: {low}")
    print()


if __name__ == "__main__":
    main()
