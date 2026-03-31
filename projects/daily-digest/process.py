#!/usr/bin/env python3
"""
process.py
----------
Deterministic processing of normalized InboundItems:
  1. Discard filtering (rules from config/discard_rules.yaml)
  2. Embedding + cosine similarity clustering (cross-source grouping)
  3. Output: items_processed.json

No LLM calls. All logic is deterministic or embedding-based.

Input:  outputs/items_normalized.json
Output: outputs/items_processed.json
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

OUTPUT_DIR  = Path(__file__).resolve().parent / "outputs"
INPUT_PATH  = OUTPUT_DIR / "items_normalized.json"
OUTPUT_PATH = OUTPUT_DIR / "items_processed.json"


# ── Config loading ────────────────────────────────────────────────────────────

def _load_discard_rules() -> dict:
    config_path = Path(__file__).resolve().parent / "config" / "discard_rules.yaml"
    try:
        import yaml
        with open(config_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        print("  [process] WARNING: pyyaml not installed, no discard rules loaded.")
        return {}
    except FileNotFoundError:
        print(f"  [process] WARNING: {config_path} not found.")
        return {}


def _load_cluster_config(rules: dict) -> dict:
    return rules.get("clustering", {})


# ── Discard filtering ─────────────────────────────────────────────────────────

def _domain_matches(handle: str, patterns: list) -> bool:
    """Check if a handle's domain matches any pattern (supports *.domain.com)."""
    handle = (handle or "").lower()
    domain = handle.split("@")[-1] if "@" in handle else handle
    for pat in patterns:
        pat = pat.lower()
        if pat.startswith("*."):
            # Wildcard: *.example.com matches example.com and sub.example.com
            base = pat[2:]
            if domain == base or domain.endswith("." + base):
                return True
        elif domain == pat:
            return True
    return False


def _substring_match(text: str, patterns: list) -> Optional[str]:
    """Return the first matching pattern substring, or None."""
    text = (text or "").lower()
    for pat in patterns:
        if pat.lower() in text:
            return pat
    return None


def apply_discard_rules(items: list, rules: dict) -> Tuple[list, list]:
    """
    Apply discard rules to items. Returns (kept, discarded) where each
    discarded item has a discard_reason attached.
    """
    discard_cfg = rules.get("discard", {})
    sender_domains = discard_cfg.get("sender_domains", [])
    sender_patterns = discard_cfg.get("sender_patterns", [])
    subject_patterns = discard_cfg.get("subject_patterns", [])
    body_patterns = discard_cfg.get("body_patterns", [])
    teams_patterns = discard_cfg.get("teams_sender_patterns", [])
    slack_patterns = discard_cfg.get("slack_sender_patterns", [])

    # Load internal domains for body-pattern scoping
    try:
        import yaml
        user_cfg_path = Path(__file__).resolve().parent / "config" / "user.yaml"
        with open(user_cfg_path, encoding="utf-8") as f:
            user_cfg = yaml.safe_load(f) or {}
        internal_domains = [d.lower() for d in user_cfg.get("internal_domains", [])]
    except Exception:
        internal_domains = []

    kept = []
    discarded = []

    for item in items:
        reason = None
        handle = (item.get("author") or {}).get("handle", "")
        name = (item.get("author") or {}).get("name", "")
        subject = item.get("subject") or ""
        body = item.get("body_snippet") or ""
        source = item.get("source", "")

        # Sender domain
        if _domain_matches(handle, sender_domains):
            reason = f"sender_domain:{handle.split('@')[-1] if '@' in handle else handle}"

        # Sender pattern
        if not reason:
            m = _substring_match(handle, sender_patterns)
            if m:
                reason = f"sender_pattern:{m}"

        # Source-specific sender patterns
        if not reason and source == "teams":
            m = _substring_match(name, teams_patterns)
            if m:
                reason = f"teams_sender:{m}"

        if not reason and source == "slack":
            m = _substring_match(name, slack_patterns)
            if m:
                reason = f"slack_sender:{m}"

        # Subject pattern
        if not reason:
            m = _substring_match(subject, subject_patterns)
            if m:
                reason = f"subject_pattern:{m}"

        # Body pattern (external senders only)
        if not reason and body_patterns:
            is_internal = any(
                handle.endswith(f"@{d}") for d in internal_domains
            ) if "@" in handle else False
            if not is_internal:
                m = _substring_match(body, body_patterns)
                if m:
                    reason = f"body_pattern:{m}"

        if reason:
            discarded.append({
                "id": item["id"],
                "source": item["source"],
                "subject": subject,
                "sender": handle,
                "discard_reason": reason,
            })
        else:
            kept.append(item)

    return kept, discarded


# ── Embedding + clustering ────────────────────────────────────────────────────

_embedder = None


class _FallbackEmbedder:
    """TF-IDF fallback when sentence-transformers is unavailable."""

    def __init__(self, dim: int = 384):
        self.dim = dim

    def encode(self, texts: list) -> np.ndarray:
        if not texts:
            return np.zeros((0, self.dim), dtype=np.float32)
        from sklearn.feature_extraction.text import TfidfVectorizer
        vec = TfidfVectorizer(max_features=self.dim, token_pattern=r"(?u)\b\w+\b")
        X = vec.fit_transform(texts).toarray()
        if X.shape[1] < self.dim:
            X = np.hstack([X, np.zeros((X.shape[0], self.dim - X.shape[1]), dtype=np.float32)])
        return X[:, :self.dim].astype(np.float32)


def _get_embedder(model_name: str, use_fallback: bool = False):
    global _embedder
    if _embedder is not None:
        return _embedder

    if use_fallback:
        print("  [process] Using TF-IDF fallback embedder.")
        _embedder = _FallbackEmbedder()
        return _embedder

    try:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer(model_name)
        print(f"  [process] Loaded embedding model: {model_name}")
        return _embedder
    except Exception as e:
        print(f"  [process] sentence-transformers unavailable ({e}), using TF-IDF fallback.")
        _embedder = _FallbackEmbedder()
        return _embedder


def _item_to_embed_text(item: dict) -> str:
    """Build a text representation for embedding."""
    parts = []
    if item.get("subject"):
        parts.append(item["subject"])
    author = item.get("author", {})
    if author.get("name"):
        parts.append(f"from: {author['name']}")
    for p in item.get("participants", []):
        pname = p.get("name", "")
        if pname and pname != author.get("name", ""):
            parts.append(pname)
    if item.get("body_snippet"):
        parts.append(item["body_snippet"][:500])
    return " ".join(parts)


def _participant_overlap(item_a: dict, item_b: dict) -> int:
    """Count shared participants by full display name (lowercased), not handle."""
    names_a = {
        p.get("name", "").strip().lower()
        for p in item_a.get("participants", [])
        if p.get("name", "").strip()
    }
    names_b = {
        p.get("name", "").strip().lower()
        for p in item_b.get("participants", [])
        if p.get("name", "").strip()
    }
    return len(names_a & names_b)


def _parse_timestamp(ts_str: str) -> Optional[float]:
    """Parse timestamp to Unix epoch seconds (Slack float or ISO 8601)."""
    if not ts_str:
        return None
    try:
        val = float(ts_str)
        if val > 1_000_000_000:
            return val
    except ValueError:
        pass
    try:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        return dt.timestamp()
    except (ValueError, TypeError):
        return None


def _time_proximity(item_a: dict, item_b: dict, max_gap_hours: float = 2.0) -> bool:
    """True if time ranges overlap or are within max_gap_hours of each other."""
    a_start = _parse_timestamp(item_a.get("first_timestamp", ""))
    a_end = _parse_timestamp(item_a.get("last_timestamp", ""))
    b_start = _parse_timestamp(item_b.get("first_timestamp", ""))
    b_end = _parse_timestamp(item_b.get("last_timestamp", ""))
    if not all([a_start, a_end, b_start, b_end]):
        return False
    gap = max(0.0, max(a_start, b_start) - min(a_end, b_end))
    return gap <= max_gap_hours * 3600


# ── O365 notification pre-clustering ─────────────────────────────────────────

_O365_VERB_RE = re.compile(
    r"\b(left\s+a\s+comment\s+in|assigned\s+you\s+a\s+task\s+in|shared|invited\s+you\s+to)\b",
    re.IGNORECASE,
)
_O365_QUOTED_RE = re.compile(r'"([^"]{3,})"')


def _extract_o365_doc_name(subject: str) -> Optional[str]:
    """
    If the subject is a Microsoft 365 document notification, return the
    canonical document name (the quoted string in the subject). Otherwise None.

    Matches subjects like:
      - 'Ian Rae assigned you a task in "Apt Cloud - Demo 2026-03-30"'
      - 'Marc Forget left a comment in "Apt Cloud - Demo 2026-03-30"'
      - 'Adam Nelson shared "Apt Cloud - Demo 2026-03-30" with you'
      - 'Adam Nelson shared the folder "Centrilogic-Aptum" with you'
    """
    if not subject:
        return None
    if not _O365_VERB_RE.search(subject):
        return None
    m = _O365_QUOTED_RE.search(subject)
    if not m:
        return None
    return m.group(1).strip()


def pre_cluster_o365_notifications(items: list) -> list:
    """
    First pass: group email items that are Microsoft 365 document notifications
    for the same document into a deterministic cluster, before embedding runs.

    Items that get a cluster assigned here are flagged with
    source_meta['o365_pre_clustered'] = True so that cluster_items() can
    skip re-processing them.

    Returns the items list with cluster_id and cluster_items pre-filled for
    any O365 notification groups of 2 or more.
    """
    from collections import defaultdict

    # Only look at email items that don't already have a cluster
    doc_groups: Dict[str, List[int]] = defaultdict(list)
    for idx, item in enumerate(items):
        if item.get("source") != "email":
            continue
        doc_name = _extract_o365_doc_name(item.get("subject") or "")
        if doc_name:
            # Normalise: lowercase, strip trailing date patterns like " 2026-03-30"
            key = re.sub(r"\s+\d{4}-\d{2}-\d{2}$", "", doc_name).strip().lower()
            doc_groups[key].append(idx)

    pre_cluster_counter = 0
    pre_clustered_count = 0

    for doc_key, indices in doc_groups.items():
        if len(indices) < 2:
            continue  # singleton — leave for embedding clustering

        cid = f"o365_{pre_cluster_counter}"
        pre_cluster_counter += 1
        member_ids = [items[i]["id"] for i in indices]

        for i in indices:
            items[i]["cluster_id"] = cid
            items[i]["cluster_items"] = [mid for mid in member_ids if mid != items[i]["id"]]
            # Flag so cluster_items() skips these
            if "source_meta" not in items[i] or items[i]["source_meta"] is None:
                items[i]["source_meta"] = {}
            items[i]["source_meta"]["o365_pre_clustered"] = True

        pre_clustered_count += len(indices)
        print(f"  [process] O365 pre-cluster '{doc_key}': {len(indices)} items -> {cid}")

    if pre_clustered_count:
        print(f"  [process] O365 pre-clustering: {pre_clustered_count} items in {pre_cluster_counter} groups.")

    return items


def cluster_items(items: list, config: dict) -> list:
    """
    Embed items and find cross-source clusters via cosine similarity.

    Returns items with cluster_id and cluster_items fields added.
    Items that don't cluster with anything get cluster_id=None.
    """
    if len(items) < 2:
        for item in items:
            item["cluster_id"] = None
            item["cluster_items"] = []
        return items

    model_name = config.get("embedding_model", "all-MiniLM-L6-v2")
    use_fallback = config.get("use_fallback_embedding", False)
    threshold = config.get("merge_threshold", 0.68)
    max_cluster_size = int(config.get("max_cluster_size", 4))

    embedder = _get_embedder(model_name, use_fallback)

    # Exclude items already assigned by O365 pre-clustering
    free_indices = [
        i for i, item in enumerate(items)
        if not (item.get("source_meta") or {}).get("o365_pre_clustered")
    ]
    free_items = [items[i] for i in free_indices]

    if len(free_items) < 2:
        # Nothing left to cluster via embedding
        for item in free_items:
            if item.get("cluster_id") is None:
                item["cluster_id"] = None
                item["cluster_items"] = []
        return items

    # Build texts and embed (free items only)
    texts = [_item_to_embed_text(item) for item in free_items]
    embeddings = embedder.encode(texts)

    # Normalize for cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    normalized = embeddings / norms

    # Cosine similarity matrix
    sim_matrix = normalized @ normalized.T

    n = len(free_items)

    # Phase 1: boosted similarity matrix
    boost_matrix = np.zeros((n, n), dtype=np.float32)
    for i in range(n):
        for j in range(i + 1, n):
            boost = 0.0
            if free_items[i]["source"] != free_items[j]["source"]:
                boost += 0.05
            if _participant_overlap(free_items[i], free_items[j]) >= 2:
                boost += 0.08
            if _time_proximity(free_items[i], free_items[j]) and _participant_overlap(free_items[i], free_items[j]) >= 1:
                boost += 0.05
            boost_matrix[i, j] = boost
            boost_matrix[j, i] = boost

    boosted_sim = sim_matrix + boost_matrix

    # Phase 2: candidate pairs above threshold
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            if float(boosted_sim[i, j]) >= threshold:
                pairs.append((float(boosted_sim[i, j]), i, j))

    pairs.sort(reverse=True)

    # Phase 3: average-linkage merge with cluster size cap
    clusters: Dict[int, list] = {i: [i] for i in range(n)}
    item_to_cluster = list(range(n))

    for _, i, j in pairs:
        ci = item_to_cluster[i]
        cj = item_to_cluster[j]
        if ci == cj:
            continue

        members_i = clusters[ci]
        members_j = clusters[cj]

        if len(members_i) + len(members_j) > max_cluster_size:
            continue

        cross_scores = [
            float(boosted_sim[mi, mj])
            for mi in members_i
            for mj in members_j
        ]
        avg_score = sum(cross_scores) / len(cross_scores)
        if avg_score < threshold:
            continue

        merged = members_i + members_j
        clusters[ci] = merged
        del clusters[cj]
        for m in members_j:
            item_to_cluster[m] = ci

    # Assign cluster_id and cluster_items
    cluster_counter = 0
    for _root, members in clusters.items():
        if len(members) == 1:
            free_items[members[0]]["cluster_id"] = None
            free_items[members[0]]["cluster_items"] = []
        else:
            cid = f"cluster_{cluster_counter}"
            cluster_counter += 1
            member_ids = [free_items[m]["id"] for m in members]
            for m in members:
                free_items[m]["cluster_id"] = cid
                free_items[m]["cluster_items"] = [mid for mid in member_ids if mid != free_items[m]["id"]]

    cross_source = sum(
        1 for g in clusters.values()
        if len(g) > 1 and len(set(free_items[i]["source"] for i in g)) > 1
    )
    total_clusters = sum(1 for g in clusters.values() if len(g) > 1)
    print(f"  [process] Clusters: {total_clusters} total, {cross_source} cross-source")

    # Ensure all free items have cluster fields set
    for item in free_items:
        if "cluster_id" not in item:
            item["cluster_id"] = None
            item["cluster_items"] = []

    return items


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    print("  [process] Loading normalized items...")

    try:
        with open(INPUT_PATH, encoding="utf-8") as f:
            normalized = json.load(f)
    except Exception as e:
        print(f"  [process] Failed to read {INPUT_PATH}: {e}")
        return 1

    items = normalized.get("items", [])
    print(f"  [process] Loaded {len(items)} items.")

    # Load config
    rules = _load_discard_rules()
    cluster_config = _load_cluster_config(rules)

    # Step 1: Discard filtering
    kept, discarded = apply_discard_rules(items, rules)
    print(f"  [process] Discard: {len(discarded)} items filtered, {len(kept)} kept.")

    # Step 2a: Deterministic O365 notification pre-clustering
    kept = pre_cluster_o365_notifications(kept)

    # Step 2b: Embedding + clustering (skips pre-clustered items)
    if len(kept) >= 2:
        kept = cluster_items(kept, cluster_config)
    else:
        for item in kept:
            if item.get("cluster_id") is None:
                item["cluster_id"] = None
                item["cluster_items"] = []

    # Write output
    output = {
        "processed_at": normalized.get("normalized_at", ""),
        "sources": normalized.get("sources", []),
        "item_count": len(kept),
        "discard_count": len(discarded),
        "items": kept,
        "discarded": discarded,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"  [process] Wrote → {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
