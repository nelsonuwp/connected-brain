"""
sku_matcher.py
--------------
Lives in:  cpq-replacement-db-only/scripts/sku_matcher.py
Connector: cpq-replacement-db-only/connectors/mssql.py
.env:      connected-brain/.env  (two levels up from project root)

Runs 5 independent fuzzy algorithms against ALL dimProductAttributes
(not filtered to active), then aggregates into a single FMA result.

Output columns (in order)
--------------------------
hardware_sku          – Product SKU from Hosting_SKUs.xlsx
fma_sku_name          – Fuzzy Match Aggregate: winning sku_name
fma_fusion_id         – Fuzzy Match Aggregate: winning fusion_id
active                – is_active value from dim (0 or 1); "direct" rows pulled from match
fma_votes             – e.g. 4/5  (blank if direct)
fma_confidence        – "direct" | 0-100 | "" (no_match)
fm1_sku_name          – Normalised Ratio best match
fm2_sku_name          – Token Sort best match
fm3_sku_name          – Token Set best match
fm4_sku_name          – Partial (substring) Ratio best match
fm5_sku_name          – Jaro-Winkler best match
match_type            – direct | fuzzy | no_match

FMA confidence formula
----------------------
  votes     = how many of the 5 methods agreed on the winning fusion_id
  avg_score = mean score of the agreeing methods
  confidence = round((votes/5 * 0.5 + avg_score/100 * 0.5) * 100, 1)

  5/5 @ 90  → 95.0     3/5 @ 80  → 70.0     1/5 @ 65  → 42.5

Usage
-----
  python scripts/sku_matcher.py
  python scripts/sku_matcher.py --live
  python scripts/sku_matcher.py --threshold 50
  python scripts/sku_matcher.py --hosting-skus '/path/to/Hosting SKUs.xlsx' --live
"""

import argparse
import csv
import difflib
import os
import re
import sys
import time
from pathlib import Path

import openpyxl

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------

SCRIPT_DIR   = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONNECTORS   = PROJECT_ROOT / "connectors"
ENV_FILE     = PROJECT_ROOT.parent.parent / ".env"

HOSTING_SKUS_FILE = PROJECT_ROOT / "Hosting_SKUs.xlsx"
DIM_PRODUCT_CSV   = PROJECT_ROOT / "dimProductAttributes_202603100849.csv"
OUTPUT_FILE       = PROJECT_ROOT / "output" / "sku_matches.csv"

FUZZY_THRESHOLD = 55
SHEET_NAME      = "Hosting SKUs"
SKU_COL_IDX     = 2    # 0-based: column C = "Product SKU"


# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------

def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def log_progress(current: int, total: int, sku: str, interval: int = 10):
    """Print progress every `interval` items."""
    if current == 1 or current % interval == 0 or current == total:
        pct = round(current / total * 100, 1)
        print(f"[{time.strftime('%H:%M:%S')}]   {current}/{total} ({pct}%)  → {sku[:60]}", flush=True)


# ---------------------------------------------------------------------------
# NORMALISATION
# ---------------------------------------------------------------------------

def normalise(text) -> str:
    if not text:
        return ""
    t = str(text).lower().strip()
    t = re.sub(r"\s*-\s*", " ", t)
    t = re.sub(r"[^\w\s\.]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


# ---------------------------------------------------------------------------
# FIVE FUZZY ALGORITHMS  (all return 0-100)
# ---------------------------------------------------------------------------

def fm1_normalised_ratio(a: str, b: str) -> float:
    """Plain SequenceMatcher on normalised strings."""
    return round(difflib.SequenceMatcher(None, normalise(a), normalise(b)).ratio() * 100, 1)


def fm2_token_sort(a: str, b: str) -> float:
    """Sort tokens alphabetically — handles reordered words."""
    sa = " ".join(sorted(normalise(a).split()))
    sb = " ".join(sorted(normalise(b).split()))
    return round(difflib.SequenceMatcher(None, sa, sb).ratio() * 100, 1)


def fm3_token_set(a: str, b: str) -> float:
    """
    Token-set: compare intersection vs each remainder.
    Handles subset names like 'Pro Series 6.0' inside 'Pro Series 6.0 vHost'.
    """
    ta = set(normalise(a).split())
    tb = set(normalise(b).split())
    inter  = sorted(ta & tb)
    rest_a = sorted(ta - tb)
    rest_b = sorted(tb - ta)
    si  = " ".join(inter)
    sia = " ".join(inter + rest_a)
    sib = " ".join(inter + rest_b)
    scores = [
        difflib.SequenceMatcher(None, si, sia).ratio(),
        difflib.SequenceMatcher(None, si, sib).ratio(),
        difflib.SequenceMatcher(None, sia, sib).ratio(),
    ]
    return round(max(scores) * 100, 1)


def fm4_partial_ratio(a: str, b: str) -> float:
    """Sliding-window substring match — finds the SKU embedded in a longer name."""
    na, nb = normalise(a), normalise(b)
    shorter, longer = (na, nb) if len(na) <= len(nb) else (nb, na)
    n = len(shorter)
    if n == 0:
        return 0.0
    best = 0.0
    for i in range(len(longer) - n + 1):
        score = difflib.SequenceMatcher(None, shorter, longer[i:i + n]).ratio()
        if score > best:
            best = score
    return round(best * 100, 1)


def _jaro(s: str, t: str) -> float:
    if s == t:
        return 1.0
    ls, lt = len(s), len(t)
    if ls == 0 or lt == 0:
        return 0.0
    md = max(max(ls, lt) // 2 - 1, 0)
    sm = [False] * ls
    tm = [False] * lt
    matches = 0
    for i in range(ls):
        for j in range(max(0, i - md), min(i + md + 1, lt)):
            if not tm[j] and s[i] == t[j]:
                sm[i] = tm[j] = True
                matches += 1
                break
    if matches == 0:
        return 0.0
    ss = [s[i] for i in range(ls) if sm[i]]
    ts = [t[j] for j in range(lt) if tm[j]]
    transpositions = sum(1 for x, y in zip(ss, ts) if x != y) // 2
    return (matches / ls + matches / lt + (matches - transpositions) / matches) / 3


def fm5_jaro_winkler(a: str, b: str) -> float:
    """Jaro-Winkler — rewards shared prefixes; good for product codes."""
    na, nb = normalise(a), normalise(b)
    jaro = _jaro(na, nb)
    prefix = 0
    for ca, cb in zip(na[:4], nb[:4]):
        if ca == cb:
            prefix += 1
        else:
            break
    return round(min((jaro + prefix * 0.1 * (1 - jaro)) * 100, 100), 1)


METHODS      = [fm1_normalised_ratio, fm2_token_sort, fm3_token_set, fm4_partial_ratio, fm5_jaro_winkler]
METHOD_NAMES = ["Normalised Ratio", "Token Sort", "Token Set", "Partial Ratio", "Jaro-Winkler"]


# ---------------------------------------------------------------------------
# BEST MATCH PER METHOD
# ---------------------------------------------------------------------------

def best_for_method(sku: str, dim_rows: list, fn, threshold: float) -> dict | None:
    best_score, best_row = -1.0, None
    for r in dim_rows:
        if not r.get("sku_name"):
            continue
        score = fn(sku, r["sku_name"])
        if score > best_score:
            best_score, best_row = score, r
    if best_row and best_score >= threshold:
        return {
            "fusion_id": best_row["fusion_id"],
            "sku_name":  best_row["sku_name"],
            "active":    best_row.get("is_active", ""),
            "score":     best_score,
        }
    return None


# ---------------------------------------------------------------------------
# FMA AGGREGATOR
# ---------------------------------------------------------------------------

def aggregate(method_results: list) -> dict:
    valid = [m for m in method_results if m is not None]
    if not valid:
        return {
            "fma_fusion_id":  "",
            "fma_sku_name":   "",
            "fma_active":     "",
            "fma_confidence": "",
            "fma_votes":      "0/5",
            "match_type":     "no_match",
        }

    vote_map: dict = {}
    for m in valid:
        vote_map.setdefault(m["fusion_id"], []).append(m)

    winner_id = max(
        vote_map,
        key=lambda fid: (
            len(vote_map[fid]),
            sum(m["score"] for m in vote_map[fid]) / len(vote_map[fid])
        )
    )
    entries    = vote_map[winner_id]
    votes      = len(entries)
    avg_score  = sum(m["score"] for m in entries) / votes
    confidence = round((votes / 5 * 0.5 + avg_score / 100 * 0.5) * 100, 1)

    return {
        "fma_fusion_id":  winner_id,
        "fma_sku_name":   entries[0]["sku_name"],
        "fma_active":     entries[0].get("active", ""),
        "fma_confidence": confidence,
        "fma_votes":      f"{votes}/5",
        "match_type":     "fuzzy",
    }


# ---------------------------------------------------------------------------
# MAIN MATCHING LOOP
# ---------------------------------------------------------------------------

def match_skus(hosting_skus: list, dim_rows: list, threshold: float) -> list:
    log(f"Building direct-match lookup …")
    norm_to_dim: dict = {}
    for r in dim_rows:
        if not r.get("sku_name"):
            continue
        norm_to_dim.setdefault(normalise(r["sku_name"]), []).append(r)
    log(f"  {len(norm_to_dim)} unique normalised dim names indexed")

    rows_out = []
    total = len(hosting_skus)
    log(f"Matching {total} hosting SKUs …")

    for idx, sku in enumerate(hosting_skus, 1):
        log_progress(idx, total, sku, interval=25)

        # ---- DIRECT ----
        if normalise(sku) in norm_to_dim:
            for c in norm_to_dim[normalise(sku)]:
                rows_out.append({
                    "hardware_sku":   sku,
                    "fma_sku_name":   c["sku_name"],
                    "fma_fusion_id":  c["fusion_id"],
                    "active":         c.get("is_active", ""),
                    "fma_votes":      "",
                    "fma_confidence": "direct",
                    "fm1_sku_name":   "",
                    "fm2_sku_name":   "",
                    "fm3_sku_name":   "",
                    "fm4_sku_name":   "",
                    "fm5_sku_name":   "",
                    "match_type":     "direct",
                })
            continue

        # ---- FUZZY ----
        results = [best_for_method(sku, dim_rows, fn, threshold) for fn in METHODS]
        agg     = aggregate(results)

        rows_out.append({
            "hardware_sku":   sku,
            "fma_sku_name":   agg["fma_sku_name"],
            "fma_fusion_id":  agg["fma_fusion_id"],
            "active":         agg["fma_active"],
            "fma_votes":      agg["fma_votes"],
            "fma_confidence": agg["fma_confidence"],
            "fm1_sku_name":   results[0]["sku_name"] if results[0] else "",
            "fm2_sku_name":   results[1]["sku_name"] if results[1] else "",
            "fm3_sku_name":   results[2]["sku_name"] if results[2] else "",
            "fm4_sku_name":   results[3]["sku_name"] if results[3] else "",
            "fm5_sku_name":   results[4]["sku_name"] if results[4] else "",
            "match_type":     agg["match_type"],
        })

    return rows_out


# ---------------------------------------------------------------------------
# DATA LOADERS
# ---------------------------------------------------------------------------

def load_hosting_skus(path: str) -> list:
    log(f"Opening: {path}")
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[SHEET_NAME]
    skus = [
        str(row[SKU_COL_IDX]).strip()
        for row in ws.iter_rows(min_row=2, values_only=True)
        if row[SKU_COL_IDX] and str(row[SKU_COL_IDX]).strip()
    ]
    log(f"  {len(skus)} SKUs loaded from sheet '{SHEET_NAME}'")
    return skus


def load_dim_from_csv(path: str) -> list:
    log(f"Opening: {path}")
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    log(f"  {len(rows)} dim rows loaded (all active statuses)")
    return rows


def load_dim_from_mssql() -> list:
    log(f"Looking for .env at: {ENV_FILE}")
    if ENV_FILE.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(dotenv_path=ENV_FILE)
            log("  Loaded via python-dotenv")
        except ImportError:
            with open(ENV_FILE) as ef:
                for line in ef:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, _, v = line.partition("=")
                        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            log("  Loaded via manual parse")
    else:
        log("  WARNING: .env not found — relying on shell environment")

    sys.path.insert(0, str(CONNECTORS))
    from mssql import MSSQLConnector
    from sqlalchemy import text

    log("Connecting to MSSQL …")
    connector = MSSQLConnector("OCEAN")

    # NOTE: no WHERE is_active filter — we pull everything and expose is_active as a column
    query = """
        SELECT fusion_id, sku_name, is_active
        FROM DM_BusinessInsights.dbo.dimProductAttributes
    """
    log(f"Running query …")
    rows = []
    with connector._engine.connect() as conn:
        for r in conn.execute(text(query)):
            rows.append({
                "fusion_id": str(r.fusion_id),
                "sku_name":  r.sku_name,
                "is_active": str(r.is_active),
            })
    connector.close()
    log(f"  {len(rows)} dim rows returned (all active statuses)")
    return rows


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

FIELDNAMES = [
    "hardware_sku",
    "fma_sku_name",
    "fma_fusion_id",
    "active",
    "fma_votes",
    "fma_confidence",
    "fm1_sku_name",
    "fm2_sku_name",
    "fm3_sku_name",
    "fm4_sku_name",
    "fm5_sku_name",
    "match_type",
]


def main():
    parser = argparse.ArgumentParser(description="Match Hosting SKUs → dimProductAttributes (5-method FMA)")
    parser.add_argument("--live",         action="store_true",
                        help="Pull from MSSQL instead of CSV")
    parser.add_argument("--threshold",    type=float, default=FUZZY_THRESHOLD,
                        help=f"Per-method minimum score to count (default {FUZZY_THRESHOLD})")
    parser.add_argument("--hosting-skus", default=str(HOSTING_SKUS_FILE),
                        help="Path to Hosting_SKUs.xlsx")
    parser.add_argument("--dim-csv",      default=str(DIM_PRODUCT_CSV),
                        help="Path to dimProductAttributes CSV (ignored if --live)")
    parser.add_argument("--output",       default=str(OUTPUT_FILE),
                        help="Output CSV path")
    args = parser.parse_args()

    log("=" * 60)
    log("SKU Matcher — 5-method Fuzzy Match Aggregate")
    log("=" * 60)
    log(f"Methods: {', '.join(f'FM{i+1}={n}' for i, n in enumerate(METHOD_NAMES))}")
    log(f"Per-method threshold: {args.threshold}")
    log("")

    hosting_skus = load_hosting_skus(args.hosting_skus)
    log("")

    if args.live:
        dim_rows = load_dim_from_mssql()
    else:
        dim_rows = load_dim_from_csv(args.dim_csv)
    log("")

    t0 = time.time()
    results = match_skus(hosting_skus, dim_rows, threshold=args.threshold)
    elapsed = round(time.time() - t0, 1)

    direct   = sum(1 for r in results if r["match_type"] == "direct")
    fuzzy    = sum(1 for r in results if r["match_type"] == "fuzzy")
    no_match = sum(1 for r in results if r["match_type"] == "no_match")

    log("")
    log(f"Done in {elapsed}s — direct={direct}  fuzzy={fuzzy}  no_match={no_match}  total_rows={len(results)}")
    log("")

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(results)

    log(f"Output written to: {out_path}")
    log("=" * 60)


if __name__ == "__main__":
    main()