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
    # Author
    author = item.get("author", {})
    if author.get("name"):
        parts.append(f"from: {author['name']}")
    # Snippet
    if item.get("body_snippet"):
        parts.append(item["body_snippet"][:300])
    return " ".join(parts)


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
    threshold = config.get("merge_threshold", 0.72)

    embedder = _get_embedder(model_name, use_fallback)

    # Build texts and embed
    texts = [_item_to_embed_text(item) for item in items]
    embeddings = embedder.encode(texts)

    # Normalize for cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    normalized = embeddings / norms

    # Cosine similarity matrix
    sim_matrix = normalized @ normalized.T

    # Greedy clustering: merge pairs above threshold
    n = len(items)
    cluster_labels = list(range(n))  # each item starts as its own cluster

    # Find pairs above threshold, prioritize cross-source pairs
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            score = float(sim_matrix[i, j])
            if score >= threshold:
                # Bonus for cross-source pairs (the whole point)
                is_cross = items[i]["source"] != items[j]["source"]
                pairs.append((score + (0.05 if is_cross else 0.0), i, j))

    pairs.sort(reverse=True)  # highest similarity first

    # Union-find merge
    def find(x):
        while cluster_labels[x] != x:
            cluster_labels[x] = cluster_labels[cluster_labels[x]]
            x = cluster_labels[x]
        return x

    for _, i, j in pairs:
        ri, rj = find(i), find(j)
        if ri != rj:
            cluster_labels[ri] = rj

    # Resolve cluster assignments
    cluster_groups: Dict[int, list] = {}
    for i in range(n):
        root = find(i)
        cluster_groups.setdefault(root, []).append(i)

    # Assign cluster_id and cluster_items
    cluster_counter = 0
    for root, members in cluster_groups.items():
        if len(members) == 1:
            items[members[0]]["cluster_id"] = None
            items[members[0]]["cluster_items"] = []
        else:
            cid = f"cluster_{cluster_counter}"
            cluster_counter += 1
            member_ids = [items[m]["id"] for m in members]
            for m in members:
                items[m]["cluster_id"] = cid
                items[m]["cluster_items"] = [mid for mid in member_ids if mid != items[m]["id"]]

    cross_source = sum(1 for g in cluster_groups.values()
                       if len(g) > 1 and len(set(items[i]["source"] for i in g)) > 1)
    total_clusters = sum(1 for g in cluster_groups.values() if len(g) > 1)
    print(f"  [process] Clusters: {total_clusters} total, {cross_source} cross-source")

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

    # Step 2: Embedding + clustering
    if len(kept) >= 2:
        kept = cluster_items(kept, cluster_config)
    else:
        for item in kept:
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
