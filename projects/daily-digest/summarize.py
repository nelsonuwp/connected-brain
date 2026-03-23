#!/usr/bin/env python3
"""
summarize.py
------------
LLM-based triage of processed InboundItems.

Reads items_processed.json → sends to LLM for categorization → writes daily_summary.json.

The LLM receives source-agnostic items and categorizes each as:
  - waiting_on_me:   someone needs something from me
  - tracking:        I'm waiting on someone else, or monitoring progress
  - new_information: FYI / no action needed
  - discard:         noise the deterministic filter missed

Clustered items (cross-source groups) are sent together so the LLM
sees the full context and produces a unified summary.

Input:  outputs/items_processed.json
Output: outputs/daily_summary.json
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from connectors.source_artifact import utc_now

OUTPUT_DIR  = Path(__file__).resolve().parent / "outputs"
INPUT_PATH  = OUTPUT_DIR / "items_processed.json"
OUTPUT_PATH = OUTPUT_DIR / "daily_summary.json"


# ── LLM prompt ────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a personal assistant triaging yesterday's incoming messages for a senior technology executive.

You will receive a JSON array of communication items (emails, Teams messages, Slack messages).
Some items are grouped into clusters — these are related conversations across different platforms about the same topic.

For each item or cluster, determine:
1. **category**: exactly one of: "waiting_on_me", "tracking", "new_information", "discard"
   - waiting_on_me: someone explicitly needs something from me (approval, reply, signature, decision, info)
   - tracking: I'm waiting on someone else, or monitoring something in progress
   - new_information: useful FYI but no action needed from me
   - discard: noise, automated notifications, or marketing that got past filters

2. **summary**: 1-2 concise sentences describing what this is about

3. **my_actions**: list of specific things I need to do (empty for tracking/info/discard)

4. **tracked_actions**: things others are doing that I should monitor (empty if none)

5. **suggested_reply**: optional short reply draft IF a quick response would be appropriate (null otherwise)

Context about the user:
- Their identity information is reflected in the is_from_me and mentions_me fields
- If is_from_me is true on the most recent message, this is likely "tracking" (I already responded)
- If mentions_me or am_in_to is true and is_from_me is false, likely "waiting_on_me"
- Items in CC only (am_in_cc=true, am_in_to=false) are more likely "new_information"

Respond with a JSON object:
{
  "items": [
    {
      "id": "item_id or cluster_id",
      "item_ids": ["list", "of", "item", "ids", "in", "this", "group"],
      "category": "waiting_on_me",
      "unified_subject": "Clean subject line for display",
      "summary": "Brief summary",
      "my_actions": ["action 1", "action 2"],
      "tracked_actions": ["thing to track"],
      "suggested_reply": "Quick reply draft or null"
    }
  ]
}

Respond ONLY with valid JSON. No markdown fences, no preamble."""


def _build_llm_payload(items: list) -> list:
    """
    Build the payload to send to the LLM.
    Groups clustered items together, sends standalone items individually.
    Strips body_text to a reasonable size for token efficiency.
    """
    # Group items by cluster
    clusters: Dict[str, list] = {}
    standalone = []

    for item in items:
        cid = item.get("cluster_id")
        if cid:
            clusters.setdefault(cid, []).append(item)
        else:
            standalone.append(item)

    payload = []

    # Clustered items: send as groups
    for cid, cluster_items in clusters.items():
        group = {
            "cluster_id": cid,
            "is_cluster": True,
            "items": [],
        }
        for item in cluster_items:
            group["items"].append(_slim_item(item))
        payload.append(group)

    # Standalone items
    for item in standalone:
        payload.append({
            "cluster_id": None,
            "is_cluster": False,
            "items": [_slim_item(item)],
        })

    return payload


def _slim_item(item: dict) -> dict:
    """Strip an item down to what the LLM needs for triage."""
    return {
        "id": item["id"],
        "source": item["source"],
        "subject": item.get("subject"),
        "body_snippet": (item.get("body_snippet") or "")[:400],
        "message_count": item.get("message_count", 1),
        "last_timestamp": item.get("last_timestamp", ""),
        "author": {
            "name": (item.get("author") or {}).get("name", ""),
            "handle": (item.get("author") or {}).get("handle", ""),
        },
        "participant_count": item.get("participant_count", 0),
        "is_from_me": item.get("is_from_me", False),
        "mentions_me": item.get("mentions_me", False),
        "am_in_to": item.get("am_in_to", False),
        "am_in_cc": item.get("am_in_cc", False),
        "is_direct_message": item.get("is_direct_message", False),
        "is_forwarded": item.get("is_forwarded", False),
        "has_attachments": item.get("has_attachments", False),
    }


def _call_llm(payload: list) -> Optional[dict]:
    """
    Call the LLM via OpenRouter for triage.

    Uses call_json from your existing openrouter.py connector.
    """
    from connectors.openrouter import call_json

    model = os.getenv("DIGEST_LLM_MODEL", "anthropic/claude-sonnet-4-5")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(payload, indent=2)},
    ]

    parsed, raw = call_json(
        model=model,
        messages=messages,
        temperature=0.1,
        max_tokens=4096,
        verbosity="low",
    )

    if parsed is None:
        print("  [summarize] LLM call failed — no response.")
        return None

    return {
        "parsed": parsed,
        "tokens": raw.get("tokens", {}) if raw else {},
        "model": raw.get("model", model) if raw else model,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    print("  [summarize] Loading processed items...")

    try:
        with open(INPUT_PATH, encoding="utf-8") as f:
            processed = json.load(f)
    except Exception as e:
        print(f"  [summarize] Failed to read {INPUT_PATH}: {e}")
        return 1

    items = processed.get("items", [])
    discard_count = processed.get("discard_count", 0)
    print(f"  [summarize] {len(items)} items to triage, {discard_count} pre-filtered.")

    if not items:
        print("  [summarize] No items to summarize.")
        _write_empty_output(discard_count)
        return 0

    # Build LLM payload
    payload = _build_llm_payload(items)
    print(f"  [summarize] Sending {len(payload)} groups to LLM...")

    # Call LLM
    result = _call_llm(payload)
    if result is None:
        print("  [summarize] LLM call failed.")
        _write_empty_output(discard_count)
        return 1

    parsed = result["parsed"]
    tokens = result["tokens"]
    model = result["model"]

    llm_items = parsed.get("items", [])
    print(f"  [summarize] LLM returned {len(llm_items)} triaged items.")

    # Merge LLM output back with original items for the render
    enriched = _merge_llm_output(items, llm_items)

    # Categorize
    waiting_on_me = [e for e in enriched if e.get("category") == "waiting_on_me"]
    tracking = [e for e in enriched if e.get("category") == "tracking"]
    new_information = [e for e in enriched if e.get("category") == "new_information"]
    llm_discarded = [e for e in enriched if e.get("category") == "discard"]

    print(f"  [summarize] Triage: {len(waiting_on_me)} waiting, "
          f"{len(tracking)} tracking, {len(new_information)} info, "
          f"{len(llm_discarded)} discarded by LLM")

    # Write output
    output = {
        "generated_at": utc_now(),
        "model": model,
        "tokens": tokens,
        "sources": processed.get("sources", []),
        "output": {
            "waiting_on_me": waiting_on_me,
            "tracking": tracking,
            "new_information": new_information,
            "discard_count": discard_count + len(llm_discarded),
        },
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"  [summarize] Wrote → {OUTPUT_PATH}")
    return 0


def _merge_llm_output(items: list, llm_items: list) -> list:
    """
    Merge LLM triage output back with original item metadata.
    """
    # Index original items by ID
    id_to_item = {item["id"]: item for item in items}

    enriched = []
    for llm_item in llm_items:
        item_ids = llm_item.get("item_ids", [])
        # Find the primary item (first in list, or by id)
        primary = None
        for iid in item_ids:
            if iid in id_to_item:
                primary = id_to_item[iid]
                break
        if not primary:
            # Try the id field directly
            iid = llm_item.get("id", "")
            primary = id_to_item.get(iid)

        # Build source URLs for all items in cluster
        urls = []
        for iid in item_ids:
            item = id_to_item.get(iid)
            if item and item.get("url"):
                urls.append({"source": item["source"], "url": item["url"], "subject": item.get("subject")})

        enriched.append({
            "id": llm_item.get("id", ""),
            "item_ids": item_ids,
            "category": llm_item.get("category", "new_information"),
            "unified_subject": llm_item.get("unified_subject", ""),
            "summary": llm_item.get("summary", ""),
            "my_actions": llm_item.get("my_actions", []),
            "tracked_actions": llm_item.get("tracked_actions", []),
            "suggested_reply": llm_item.get("suggested_reply"),
            # Preserved from original items
            "source": primary.get("source", "unknown") if primary else "unknown",
            "sources": list(set(id_to_item[iid]["source"] for iid in item_ids if iid in id_to_item)),
            "last_timestamp": primary.get("last_timestamp", "") if primary else "",
            "participant_count": primary.get("participant_count", 0) if primary else 0,
            "is_from_me": primary.get("is_from_me", False) if primary else False,
            "has_attachments": primary.get("has_attachments", False) if primary else False,
            "urls": urls,
            "is_cluster": len(item_ids) > 1,
        })

    return enriched


def _write_empty_output(discard_count: int):
    output = {
        "generated_at": utc_now(),
        "model": "none",
        "tokens": {},
        "sources": [],
        "output": {
            "waiting_on_me": [],
            "tracking": [],
            "new_information": [],
            "discard_count": discard_count,
        },
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    raise SystemExit(main())
