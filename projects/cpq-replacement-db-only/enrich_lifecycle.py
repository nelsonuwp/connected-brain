"""
enrich_lifecycle.py
--------------------
Fetches EOL / lifecycle dates for all product_catalog items — both servers
(from 01_servers.csv) and components (from 05/06 CSVs).

Source priority per category:

    OS (Windows, SQL)   → Microsoft Lifecycle API   deterministic  confidence 1.00
    OS (RHEL)           → Red Hat lifecycle API      deterministic  confidence 1.00
    OS (Linux other)    → Perplexity MODEL_SEARCH    grounded       confidence 0.85
    Processor           → Perplexity MODEL_SEARCH    grounded       confidence 0.85
    Servers             → Perplexity MODEL_SEARCH    grounded       confidence 0.85
    Drive / NIC / PSU   → Perplexity MODEL_SEARCH    grounded       confidence 0.85
    Software (other)    → Perplexity MODEL_SEARCH    grounded       confidence 0.85
    RAM                 → skip (no industry EOL tracking)

Outputs:
    output/07c_product_lifecycle.csv    consumed by generate_seed.py phase 2

Schema columns populated in product_catalog:
    launch_date, end_of_sale_date, end_of_standard_support_date, end_of_life_date

Field naming rationale (vs Intel's terminology):
    launch_date                   = Intel "Launch Date" / MS "startDate"
    end_of_sale_date              = universal EOS — vendor stops selling
    end_of_standard_support_date  = Intel ESU / MS "maintenanceEndDate" / RHEL "Full support"
    end_of_life_date              = Intel EOSL / MS "extendedEndDate" / RHEL "Maintenance"

Usage:
    cd projects/cpq-replacement-db-only
    python enrich_lifecycle.py [--dry-run] [--category CATEGORY] [--sku SKU] [--force]

    --dry-run         Show what would be enriched, no API calls
    --category NAME   Process only this category (e.g. OS, Processor, server)
    --sku NAME        Process only this specific sku (exact match)
    --force           Re-fetch even if output row already exists

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

import requests
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
# I/O
# ---------------------------------------------------------------------------
HARDWARE_CSV  = EXTRACTED / "05_hardware_components.csv"
SOFTWARE_CSV  = EXTRACTED / "06_software_licenses.csv"
LIFECYCLE_CSV = OUTPUT / "07c_product_lifecycle.csv"

LIFECYCLE_FIELDS = [
    "sku", "product_category",
    "launch_date", "end_of_sale_date",
    "end_of_standard_support_date", "end_of_life_date",
    "source_method", "source_url",
    "confidence", "needs_review", "notes",
]

# ---------------------------------------------------------------------------
# Confidence
# ---------------------------------------------------------------------------
CONF_DETERMINISTIC = 1.00
CONF_GROUNDED      = 0.85
CONF_INFERRED      = 0.60
REVIEW_THRESHOLD   = 0.80

# ---------------------------------------------------------------------------
# Categories to skip (no meaningful EOL)
# ---------------------------------------------------------------------------
SKIP_CATEGORIES = {"RAM", "PSU"}

# Drive skus that are too generic to have published EOL dates
# (manufacturer-specific drives like "7.6 TB Micron 9400 SSD" are ok)
GENERIC_DRIVE_PATTERNS = [
    r"^\d+[\d.]* ?(GB|TB) ?7200",       # e.g. "1 TB 7200 6 Gb/s SATA"
    r"^\d+[\d.]* ?(GB|TB) ?SATA 2\.5",  # e.g. "480 GB SATA 2.5in SSD"
    r"^\d+[\d.]* ?(GB|TB) ?NVMe u\.2",  # e.g. "960 GB NVMe u.2 2.5in"
    r"^\d+[\d.]* ?(GB|TB) SSD$",        # e.g. "480 GB SSD"
]


def _is_generic_drive(sku: str) -> bool:
    import re as _re
    for pattern in GENERIC_DRIVE_PATTERNS:
        if _re.match(pattern, sku, _re.IGNORECASE):
            return True
    return False


def _is_default_variant(sku: str) -> bool:
    """Returns True for 'Default Xeon ...' style SKUs that duplicate a real SKU."""
    return sku.lower().startswith("default ")


def _base_sku(sku: str) -> str:
    """Strip 'Default ' prefix to get the canonical SKU for cache lookup.

    Handles the naming inconsistency where some SKUs are stored as
    'Default Xeon Bronze 3106...' but the base SKU is 'Intel Xeon Bronze 3106...'.
    """
    if sku.lower().startswith("default "):
        stripped = sku[8:].strip()
        # Re-add "Intel" prefix if the SKU starts with a known Intel brand name
        # e.g. "Default Xeon Bronze 3106" -> "Intel Xeon Bronze 3106"
        intel_brands = ("xeon", "celeron", "core i", "pentium", "itanium")
        if stripped.lower().startswith(intel_brands):
            return "Intel " + stripped
        return stripped
    return sku


def _clean_date(value: str) -> str:
    """
    Extract ISO date from LLM responses that may include explanatory text.
    e.g. "End of support: 2024-12-31" -> "2024-12-31"
         "2024-12-31 (extended)" -> "2024-12-31"
         "December 31, 2024" -> "2024-12-31" (best effort)
    Returns "" if no valid date found.
    """
    import re as _re
    if not value:
        return ""
    # Already clean ISO
    m = _re.search(r"(\d{4}-\d{2}-\d{2})", str(value))
    if m:
        return m.group(1)
    # Try "Month DD, YYYY" or "Month YYYY"
    months = {"january":"01","february":"02","march":"03","april":"04",
              "may":"05","june":"06","july":"07","august":"08",
              "september":"09","october":"10","november":"11","december":"12"}
    m = _re.search(
        r"(january|february|march|april|may|june|july|august|"
        r"september|october|november|december)\s+(\d{1,2}),?\s+(\d{4})",
        str(value).lower()
    )
    if m:
        mon, day, year = m.group(1), m.group(2).zfill(2), m.group(3)
        return f"{year}-{months[mon]}-{day}"
    # "Q4 2025" → last day of that quarter (approximate)
    m = _re.search(r"Q([1-4])\s+(\d{4})", str(value), _re.IGNORECASE)
    if m:
        q, yr = int(m.group(1)), m.group(2)
        last_month = {1:"03",2:"06",3:"09",4:"12"}[q]
        last_day = {1:"31",2:"30",3:"30",4:"31"}[q]
        return f"{yr}-{last_month}-{last_day}"
    return ""

# Categories routed to Microsoft Lifecycle API
MS_LIFECYCLE_CATEGORIES = {"OS", "SQL"}
MS_LIFECYCLE_SKUS = {
    # Patterns that indicate Windows / SQL — everything else in OS goes to Perplexity
    "windows", "sql server",
}


# ---------------------------------------------------------------------------
# Source 1: Microsoft Lifecycle API
# ---------------------------------------------------------------------------
MS_API = "https://learn.microsoft.com/api/lifecycle/search"


def _fetch_ms_lifecycle(sku: str) -> dict:
    """
    Query Microsoft Lifecycle Policy API.
    Returns normalized lifecycle dict or empty dict on failure.
    """
    try:
        resp = requests.get(
            MS_API,
            params={"query": sku, "locale": "en-us"},
            timeout=15,
        )
        if resp.status_code != 200:
            return {}

        data    = resp.json()
        results = data.get("result") or data.get("results") or []
        if not results:
            return {}

        # Take the best match — first result Microsoft returns
        item = results[0]
        return {
            "launch_date":                    _clean_date(item.get("startDate") or item.get("releaseDate") or ""),
            "end_of_sale_date":               "",   # MS API doesn't surface EOS directly
            "end_of_standard_support_date":   _clean_date(item.get("maintenanceEndDate") or ""),
            "end_of_life_date":               _clean_date(item.get("extendedEndDate") or ""),
            "source_method":                  "ms_lifecycle_api",
            "source_url":                     f"https://learn.microsoft.com/en-us/lifecycle/products/?terms={sku.replace(' ', '+')}",
            "confidence":                     CONF_DETERMINISTIC,
            "needs_review":                   False,
            "notes":                          f"MS Lifecycle API: {item.get('product', '')}",
        }
    except Exception as e:
        print(f"  [ms_api] Error for '{sku}': {e}")
        return {}


def _is_ms_product(sku: str) -> bool:
    sku_lower = sku.lower()
    return any(kw in sku_lower for kw in MS_LIFECYCLE_SKUS)


# ---------------------------------------------------------------------------
# Source 2: Red Hat lifecycle
# ---------------------------------------------------------------------------
RHEL_LIFECYCLE_URL = "https://access.redhat.com/product-life-cycles/raw_data"

_rhel_cache: dict = {}


def _fetch_rhel_cache():
    global _rhel_cache
    if _rhel_cache:
        return _rhel_cache

    try:
        resp = requests.get(RHEL_LIFECYCLE_URL, timeout=15)
        if resp.status_code != 200:
            return {}
        data = resp.json()
        # Structure: list of products with "name", "phases" array
        for product in (data if isinstance(data, list) else []):
            name = product.get("name", "")
            _rhel_cache[name.lower()] = product
        return _rhel_cache
    except Exception as e:
        print(f"  [rhel_api] Error fetching lifecycle data: {e}")
        return {}


def _parse_rhel_dates(product: dict) -> dict:
    """Extract dates from Red Hat lifecycle product record."""
    phases = product.get("phases") or []
    full_support_end   = ""
    maintenance_end    = ""
    launch             = product.get("ga_date") or ""

    for phase in phases:
        name = (phase.get("name") or "").lower()
        end  = phase.get("date_end") or ""
        if "full support" in name:
            full_support_end = end
        elif "maintenance" in name or "extended" in name:
            maintenance_end = end

    return {
        "launch_date":                  launch,
        "end_of_sale_date":             full_support_end,   # approximate
        "end_of_standard_support_date": full_support_end,
        "end_of_life_date":             maintenance_end,
    }


def _fetch_rhel_lifecycle(sku: str) -> dict:
    cache = _fetch_rhel_cache()
    if not cache:
        return {}

    sku_lower = sku.lower()
    # Try progressively looser matches
    for key, product in cache.items():
        if sku_lower in key or key in sku_lower:
            dates = _parse_rhel_dates(product)
            return {
                **dates,
                "source_method": "rhel_lifecycle_api",
                "source_url":    RHEL_LIFECYCLE_URL,
                "confidence":    CONF_DETERMINISTIC,
                "needs_review":  False,
                "notes":         f"Red Hat Lifecycle: {product.get('name', '')}",
            }

    return {}


def _is_rhel(sku: str) -> bool:
    return "rhel" in sku.lower() or "red hat" in sku.lower()


# ---------------------------------------------------------------------------
# Source 3: Perplexity grounded lookup (all other categories)
# ---------------------------------------------------------------------------

LIFECYCLE_SYSTEM = (
    "You are a product lifecycle database assistant. "
    "Your entire response must be a single raw JSON object — no markdown, no code fences, "
    "no explanation before or after. Start your response with { and end with }. "
    "All dates must be ISO format YYYY-MM-DD. "
    "If you cannot find a specific date with confidence, omit that field entirely — do not guess. "
    "Set grounded=true only if you found a primary vendor source (Dell, Intel ARK, "
    "Microsoft, manufacturer site). "
    "Include source_url pointing to the primary source."
)


def _build_lifecycle_prompt(sku: str, category: str) -> str:
    return (
        f'Find the product lifecycle dates for: "{sku}"\n'
        f"Category: {category}\n\n"
        f"Return JSON with these fields (omit any you cannot confirm):\n"
        f"{{\n"
        f'  "grounded": true/false,\n'
        f'  "source_url": "https://...",\n'
        f'  "launch_date": "YYYY-MM-DD",\n'
        f'  "end_of_sale_date": "YYYY-MM-DD",\n'
        f'  "end_of_standard_support_date": "YYYY-MM-DD",\n'
        f'  "end_of_life_date": "YYYY-MM-DD",\n'
        f'  "notes": "brief context"\n'
        f"}}\n\n"
        f"For servers: check Dell product lifecycle page.\n"
        f"For CPUs: check Intel ARK (ark.intel.com) or Intel support articles.\n"
        f"For OS: check vendor lifecycle pages.\n"
        f"For drives/NICs: check manufacturer product pages."
    )


def _fetch_perplexity_lifecycle(sku: str, category: str) -> dict:
    messages = [
        {"role": "system", "content": LIFECYCLE_SYSTEM},
        {"role": "user",   "content": _build_lifecycle_prompt(sku, category)},
    ]

    parsed, raw = openrouter.search_call_json(messages=messages, max_tokens=512)

    if parsed is None:
        return {}

    grounded   = bool(parsed.get("grounded", False))
    confidence = CONF_GROUNDED if grounded else CONF_INFERRED
    source_url = parsed.get("source_url") or (
        (raw.get("source_urls") or [None])[0] if raw else None
    )

    dates = {}
    for field in ("launch_date", "end_of_sale_date",
                  "end_of_standard_support_date", "end_of_life_date"):
        val = parsed.get(field, "")
        cleaned = _clean_date(str(val)) if val else ""
        if cleaned:
            dates[field] = cleaned

    if not dates:
        return {}

    return {
        "launch_date":                  dates.get("launch_date", ""),
        "end_of_sale_date":             dates.get("end_of_sale_date", ""),
        "end_of_standard_support_date": dates.get("end_of_standard_support_date", ""),
        "end_of_life_date":             dates.get("end_of_life_date", ""),
        "source_method":                "perplexity_grounded" if grounded else "perplexity_inferred",
        "source_url":                   source_url or "",
        "confidence":                   confidence,
        "needs_review":                 not grounded or confidence < REVIEW_THRESHOLD,
        "notes":                        parsed.get("notes", ""),
    }


# ---------------------------------------------------------------------------
# Route to correct source
# ---------------------------------------------------------------------------

def fetch_lifecycle(sku: str, category: str, dry_run: bool) -> dict:
    """
    Route sku to the appropriate lifecycle source.
    Returns a normalized lifecycle dict or empty dict.
    """
    if dry_run:
        return _dry_run_result(sku, category)

    # Skip categories with no EOL concept
    if category in SKIP_CATEGORIES:
        return {}

    # Skip generic drives — no manufacturer-specific EOL data published
    if category == "Drive" and _is_generic_drive(sku):
        return {}

    # Microsoft API — Windows Server, SQL Server
    if category in MS_LIFECYCLE_CATEGORIES and _is_ms_product(sku):
        result = _fetch_ms_lifecycle(sku)
        if result:
            return result

    # Red Hat lifecycle API — RHEL
    if _is_rhel(sku):
        result = _fetch_rhel_lifecycle(sku)
        if result:
            return result

    # Everything else → Perplexity
    return _fetch_perplexity_lifecycle(sku, category)


def _dry_run_result(sku: str, category: str) -> dict:
    """Placeholder for dry-run mode — shows routing without API calls."""
    if category in SKIP_CATEGORIES:
        route = "SKIP"
    elif category in MS_LIFECYCLE_CATEGORIES and _is_ms_product(sku):
        route = "ms_lifecycle_api"
    elif _is_rhel(sku):
        route = "rhel_lifecycle_api"
    else:
        route = "perplexity_grounded"

    return {
        "launch_date": "", "end_of_sale_date": "",
        "end_of_standard_support_date": "", "end_of_life_date": "",
        "source_method": f"dry_run:{route}", "source_url": "",
        "confidence": 0, "needs_review": True, "notes": "dry-run",
    }


# ---------------------------------------------------------------------------
# Load items
# ---------------------------------------------------------------------------

def load_items() -> list:
    """Load all skus that need lifecycle enrichment across all sources."""
    items = []

    # Hardware components (05)
    if HARDWARE_CSV.exists():
        with open(HARDWARE_CSV, newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                sku      = row.get("sku", "").strip()
                category = row.get("category", "").strip()
                if sku and category not in SKIP_CATEGORIES:
                    items.append({"sku": sku, "category": category})

    # Software (06) — OS and SQL only (others have no EOL concept worth tracking)
    if SOFTWARE_CSV.exists():
        with open(SOFTWARE_CSV, newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                sku      = row.get("sku", "").strip()
                category = row.get("category", "").strip()
                if sku and category in {"OS", "SQL"}:
                    items.append({"sku": sku, "category": category})

    return items


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def load_existing() -> dict:
    if not LIFECYCLE_CSV.exists():
        return {}
    existing = {}
    with open(LIFECYCLE_CSV, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            existing[row["sku"]] = row
    return existing


def write_lifecycle_csv(results: list):
    with open(LIFECYCLE_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LIFECYCLE_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)

    flagged = sum(1 for r in results if str(r.get("needs_review")).lower() == "true")
    print(f"  Wrote {len(results)} rows → {LIFECYCLE_CSV.relative_to(REPO_ROOT)}")
    print(f"  Flagged needs_review: {flagged}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Enrich CPQ product lifecycle dates")
    ap.add_argument("--dry-run",  action="store_true", help="Show routing, no API calls")
    ap.add_argument("--category", default=None,        help="Process only this category")
    ap.add_argument("--sku",      default=None,        help="Process only this sku (exact)")
    ap.add_argument("--force",    action="store_true", help="Re-fetch even if cached")
    args = ap.parse_args()

    if not args.dry_run and not os.getenv("OPENROUTER_API_KEY"):
        print("ERROR: OPENROUTER_API_KEY not set in .env (use --dry-run to skip API calls)")
        sys.exit(1)

    existing = load_existing() if (not args.force and not args.dry_run) else {}
    if existing:
        print(f"  Loaded {len(existing)} cached lifecycle rows (--force to re-fetch all)")

    items = load_items()

    if args.category:
        items = [i for i in items if i["category"] == args.category]
    if args.sku:
        items = [i for i in items if i["sku"] == args.sku]

    print(f"\nFetching lifecycle dates for {len(items)} items...\n")

    results      = list(existing.values())   # start with cached
    seen         = set(existing.keys())
    total_tokens = 0
    by_source    = {}

    # Build a result lookup for dedup (base_sku → result)
    base_sku_results = {}

    for i, item in enumerate(items, 1):
        sku      = item["sku"]
        category = item["category"]

        if sku in seen and not args.force:
            continue

        # Default variants: inherit from base SKU instead of separate API call
        if _is_default_variant(sku):
            base = _base_sku(sku)
            if base in base_sku_results:
                inherited = {**base_sku_results[base], "sku": sku,
                             "notes": f"Inherited from '{base}'"}
                results.append(inherited)
                seen.add(sku)
                print(f"  [{i:3d}/{len(items)}] [inherit      ] {sku}")
                continue

        # Route label for display
        if category in SKIP_CATEGORIES:
            route = "SKIP"
        elif category in MS_LIFECYCLE_CATEGORIES and _is_ms_product(sku):
            route = "ms_api"
        elif _is_rhel(sku):
            route = "rhel_api"
        else:
            route = "perplexity"

        print(f"  [{i:3d}/{len(items)}] [{route:12s}] {sku}")

        lifecycle = fetch_lifecycle(sku, category, args.dry_run)

        if not lifecycle:
            print(f"    → no data found")
            lifecycle = {
                "launch_date": "", "end_of_sale_date": "",
                "end_of_standard_support_date": "", "end_of_life_date": "",
                "source_method": "not_found", "source_url": "",
                "confidence": 0, "needs_review": True, "notes": "",
            }

        row = {
            "sku":              sku,
            "product_category": category,
            **lifecycle,
        }
        # Ensure all fields present
        for f in LIFECYCLE_FIELDS:
            row.setdefault(f, "")

        results.append(row)
        seen.add(sku)
        # Register for Default variant inheritance
        if not _is_default_variant(sku) and lifecycle:
            base_sku_results[sku] = row

        by_source[lifecycle.get("source_method", "unknown")] = (
            by_source.get(lifecycle.get("source_method", "unknown"), 0) + 1
        )

        if not args.dry_run and route == "perplexity":
            time.sleep(0.5)   # rate limit courtesy

    print()
    if not args.dry_run:
        write_lifecycle_csv(results)
    else:
        flagged = sum(1 for r in results if str(r.get("needs_review")).lower() == "true")
        print(f"  Dry-run complete — {len(results)} items routed, nothing written to disk")
        print(f"  (would flag {flagged} for review on a real run)")

    print(f"\n{'='*60}")
    print(f"  Total rows     : {len(results)}")
    print(f"  By source:")
    for src, count in sorted(by_source.items(), key=lambda x: -x[1]):
        print(f"    {src:35s} {count}")

    flagged = [r for r in results if str(r.get("needs_review")).lower() == "true"]
    if flagged:
        print(f"\n  Review queue ({len(flagged)} rows):")
        for r in flagged[:10]:
            print(f"    [{r['product_category']:15s}] {r['sku']}")
        if len(flagged) > 10:
            print(f"    ... and {len(flagged) - 10} more")
    print()


if __name__ == "__main__":
    main()
