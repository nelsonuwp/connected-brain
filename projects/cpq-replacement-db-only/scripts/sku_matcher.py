"""
sku_matcher.py
--------------
Lives in:  cpq-replacement-db-only/scripts/sku_matcher.py
Connector: cpq-replacement-db-only/connectors/mssql.py
.env:      connected-brain/.env  (two levels up from project root)

Runs 5 independent fuzzy algorithms, then aggregates into FMA.

Output columns
--------------
product_sku
fm1_fusion_id / fm1_sku_name / fm1_score   – Normalised Ratio
fm2_fusion_id / fm2_sku_name / fm2_score   – Token Sort Ratio
fm3_fusion_id / fm3_sku_name / fm3_score   – Token Set Ratio
fm4_fusion_id / fm4_sku_name / fm4_score   – Partial (substring) Ratio
fm5_fusion_id / fm5_sku_name / fm5_score   – Jaro-Winkler
fma_fusion_id / fma_sku_name               – aggregate winner
fma_confidence   "direct" | 0-100 score | "" (no_match)
fma_votes        n/5 agreements (blank for direct/no_match)
match_type       direct | fuzzy | no_match

FMA confidence formula
----------------------
  votes     = methods that agree on winning fusion_id
  avg_score = mean score of agreeing methods
  confidence = round((votes/5 * 0.5 + avg_score/100 * 0.5) * 100, 1)

  5/5 @ 90  → 95.0     3/5 @ 80  → 70.0     1/5 @ 65  → 42.5

Usage
-----
  python scripts/sku_matcher.py
  python scripts/sku_matcher.py --live
  python scripts/sku_matcher.py --threshold 50
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
SKU_COL_IDX     = 2


# ---------------------------------------------------------------------------
# NORMALISATION
# ---------------------------------------------------------------------------

def normalise(text: str) -> str:
    t = text.lower().strip()
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
    """Sliding-window best substring match — good for names embedded in longer strings."""
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
    prefix = sum(1 for x, y in zip(na[:4], nb[:4]) if x == y and all(na[k] == nb[k] for k in range(list(zip(na[:4], nb[:4])).index((x, y)) + 1)))
    # simpler prefix count
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
        score = fn(sku, r["sku_name"])
        if score > best_score:
            best_score, best_row = score, r
    if best_row and best_score >= threshold:
        return {"fusion_id": best_row["fusion_id"], "sku_name": best_row["sku_name"], "score": best_score}
    return None


# ---------------------------------------------------------------------------
# FMA AGGREGATOR
# ---------------------------------------------------------------------------

def aggregate(method_results: list) -> dict:
    valid = [m for m in method_results if m is not None]
    if not valid:
        return {"fma_fusion_id": "", "fma_sku_name": "", "fma_confidence": "", "fma_votes": "0/5", "match_type": "no_match"}

    vote_map: dict = {}
    for m in valid:
        vote_map.setdefault(m["fusion_id"], []).append(m)

    winner_id = max(
        vote_map,
        key=lambda fid: (len(vote_map[fid]), sum(m["score"] for m in vote_map[fid]) / len(vote_map[fid]))
    )
    entries    = vote_map[winner_id]
    votes      = len(entries)
    avg_score  = sum(m["score"] for m in entries) / votes
    confidence = round((votes / 5 * 0.5 + avg_score / 100 * 0.5) * 100, 1)

    return {
        "fma_fusion_id":  winner_id,
        "fma_sku_name":   entries[0]["sku_name"],
        "fma_confidence": confidence,
        "fma_votes":      f"{votes}/5",
        "match_type":     "fuzzy",
    }


# ---------------------------------------------------------------------------
# MAIN MATCHING LOOP
# ---------------------------------------------------------------------------

def match_skus(hosting_skus: list, dim_rows: list, threshold: float) -> list:
    norm_to_dim: dict = {}
    for r in dim_rows:
        norm_to_dim.setdefault(normalise(r["sku_name"]), []).append(r)

    rows_out = []

    for sku in hosting_skus:
        # DIRECT
        if normalise(sku) in norm_to_dim:
            for c in norm_to_dim[normalise(sku)]:
                rows_out.append({
                    "product_sku":    sku,
                    "fm1_fusion_id":  "", "fm1_sku_name": "", "fm1_score": "",
                    "fm2_fusion_id":  "", "fm2_sku_name": "", "fm2_score": "",
                    "fm3_fusion_id":  "", "fm3_sku_name": "", "fm3_score": "",
                    "fm4_fusion_id":  "", "fm4_sku_name": "", "fm4_score": "",
                    "fm5_fusion_id":  "", "fm5_sku_name": "", "fm5_score": "",
                    "fma_fusion_id":  c["fusion_id"],
                    "fma_sku_name":   c["sku_name"],
                    "fma_confidence": "direct",
                    "fma_votes":      "",
                    "match_type":     "direct",
                })
            continue

        # FUZZY
        results = [best_for_method(sku, dim_rows, fn, threshold) for fn in METHODS]
        agg     = aggregate(results)
        row     = {"product_sku": sku}
        for i, res in enumerate(results, 1):
            row[f"fm{i}_fusion_id"] = res["fusion_id"] if res else ""
            row[f"fm{i}_sku_name"]  = res["sku_name"]  if res else ""
            row[f"fm{i}_score"]     = res["score"]      if res else ""
        row.update(agg)
        rows_out.append(row)

    return rows_out


# ---------------------------------------------------------------------------
# DATA LOADERS
# ---------------------------------------------------------------------------

def load_hosting_skus(path: str) -> list:
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[SHEET_NAME]
    return [str(row[SKU_COL_IDX]).strip()
            for row in ws.iter_rows(min_row=2, values_only=True)
            if row[SKU_COL_IDX] and str(row[SKU_COL_IDX]).strip()]


def load_dim_from_csv(path: str) -> list:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_dim_from_mssql() -> list:
    if ENV_FILE.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(dotenv_path=ENV_FILE)
            print(f"  Loaded env from: {ENV_FILE}")
        except ImportError:
            with open(ENV_FILE) as ef:
                for line in ef:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, _, v = line.partition("=")
                        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            print(f"  Loaded env manually from: {ENV_FILE}")
    else:
        print(f"  Warning: .env not found at {ENV_FILE}")

    sys.path.insert(0, str(CONNECTORS))
    from mssql import MSSQLConnector
    from sqlalchemy import text

    connector = MSSQLConnector("OCEAN")
    rows = []
    with connector._engine.connect() as conn:
        for r in conn.execute(text(
            "SELECT fusion_id, sku_name FROM DM_BusinessInsights.dbo.dimProductAttributes WHERE is_active = N'1'"
        )):
            rows.append({"fusion_id": str(r.fusion_id), "sku_name": r.sku_name})
    connector.close()
    return rows


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

FIELDNAMES = [
    "product_sku",
    "fm1_fusion_id", "fm1_sku_name", "fm1_score",
    "fm2_fusion_id", "fm2_sku_name", "fm2_score",
    "fm3_fusion_id", "fm3_sku_name", "fm3_score",
    "fm4_fusion_id", "fm4_sku_name", "fm4_score",
    "fm5_fusion_id", "fm5_sku_name", "fm5_score",
    "fma_fusion_id", "fma_sku_name", "fma_confidence", "fma_votes",
    "match_type",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live",         action="store_true")
    parser.add_argument("--threshold",    type=float, default=FUZZY_THRESHOLD,
                        help=f"Per-method min score (default {FUZZY_THRESHOLD})")
    parser.add_argument("--hosting-skus", default=str(HOSTING_SKUS_FILE))
    parser.add_argument("--dim-csv",      default=str(DIM_PRODUCT_CSV))
    parser.add_argument("--output",       default=str(OUTPUT_FILE))
    args = parser.parse_args()

    print(f"Loading hosting SKUs: {args.hosting_skus}")
    skus = load_hosting_skus(args.hosting_skus)
    print(f"  → {len(skus)} SKUs")

    if args.live:
        print("Loading dimProductAttributes from MSSQL …")
        dim_rows = load_dim_from_mssql()
    else:
        print(f"Loading dimProductAttributes from CSV: {args.dim_csv}")
        dim_rows = load_dim_from_csv(args.dim_csv)
    print(f"  → {len(dim_rows)} active products")

    print(f"Running 5-method FMA (threshold={args.threshold}) …")
    print(f"  FM1={METHOD_NAMES[0]}  FM2={METHOD_NAMES[1]}  FM3={METHOD_NAMES[2]}")
    print(f"  FM4={METHOD_NAMES[3]}  FM5={METHOD_NAMES[4]}")
    results = match_skus(skus, dim_rows, threshold=args.threshold)

    direct   = sum(1 for r in results if r["match_type"] == "direct")
    fuzzy    = sum(1 for r in results if r["match_type"] == "fuzzy")
    no_match = sum(1 for r in results if r["match_type"] == "no_match")
    print(f"  direct={direct}  fuzzy={fuzzy}  no_match={no_match}  total_rows={len(results)}")

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(results)

    print(f"Written: {out_path}")


if __name__ == "__main__":
    main()
