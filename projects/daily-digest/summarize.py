#!/usr/bin/env python3
"""
summarize.py
------------
LLM-based triage of processed InboundItems.

Reads items_processed.json → sends to LLM for categorization → writes daily_summary.json.

The LLM receives source-agnostic items and produces a flat list of digest entries,
each with: title, summary, actions (with completion tracking), tracked_items,
and individual_sources. Source counts and date ranges are filled in after the LLM
call from original item metadata. Items tagged discard are filtered out.

Input:  outputs/items_processed.json
Output: outputs/daily_summary.json
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo

from connectors.source_artifact import utc_now

OUTPUT_DIR   = Path(__file__).resolve().parent / "outputs"
INPUT_PATH   = OUTPUT_DIR / "items_processed.json"
OUTPUT_PATH  = OUTPUT_DIR / "daily_summary.json"
PEOPLE_PATH  = Path(__file__).resolve().parent / "config" / "people.yaml"


# ── People roster ─────────────────────────────────────────────────────────────

def _load_people_roster() -> list:
    """Load people roster from config/people.yaml. Returns [] if not found."""
    if not PEOPLE_PATH.exists():
        return []
    try:
        import re
        text = PEOPLE_PATH.read_text(encoding="utf-8")
        # Simple YAML parse: extract slug/name/aliases blocks without a full YAML dep
        people = []
        current = {}
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("- slug:"):
                if current:
                    people.append(current)
                current = {"slug": stripped.split(":", 1)[1].strip()}
            elif stripped.startswith("name:") and current:
                current["name"] = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("aliases:") and current:
                raw = stripped.split(":", 1)[1].strip()
                aliases = re.findall(r"[\w\-]+", raw)
                current["aliases"] = aliases
        if current:
            people.append(current)
        return people
    except Exception:
        return []


def _build_roster_prompt(people: list) -> str:
    """Format the people roster as a concise LLM prompt section."""
    if not people:
        return ""
    lines = ["", "Known people roster (use these exact vault slugs for the person field):"]
    for p in people:
        aliases = p.get("aliases", [])
        alias_str = f" (also known as: {', '.join(aliases)})" if aliases else ""
        lines.append(f"  - {p['name']}{alias_str} → slug: \"{p['slug']}\"")
    lines.append("")
    return "\n".join(lines)


# ── LLM prompt ────────────────────────────────────────────────────────────────

_SYSTEM_PROMPT_BASE = """You are a personal assistant preparing a daily communication digest for a senior technology executive. You will receive a JSON array of communication items (emails, Teams messages, Slack messages) from the previous business day. Some items are grouped into clusters — these are related conversations across different platforms about the same topic.

For each item or cluster, produce a digest entry with:

1. **title**: A short, descriptive title that summarizes the topic (5-10 words). This will become a clickable link — make it scannable and informative. Examples: "AWS Marketplace — TDSynnex Program Docs", "Credit Review Board — Items for Tomorrow", "CPQ v28 Pricing Bug Resolved"

2. **summary**: 1-3 sentences of context. Enough to understand without opening the source. Include key names, numbers, dates, and decisions. Do NOT pad with filler.

3. **actions**: Things the executive needs to do. Each action is an object:
   - "text": clear, specific action description
   - "completed": true if evidence shows this action was already done — either by the executive themselves (e.g., they sent a reply, signed the document, approved the request) OR confirmed by someone else. Look for signals like: a later message from Adam confirming he did it, a system confirmation (e.g., "Your signature was received"), or a reply from a third party confirming receipt of something Adam sent.
   - "completed_proof_url": URL to the message that proves completion — link to Adam's own reply if he did it, or to the confirmation message (null if not completed)

4. **tracked_items**: Things others are doing that the executive should monitor. Each is an object:
   - "text": clear, specific tracking description (e.g., "Marc Pare to get AWS program language for amendment")
   - "completed": true if a later message shows this was finished
   - "completed_proof_url": URL to the message proving completion (null if not completed)
   - "person": the vault slug of the primary person responsible for this item — use the Known people roster below. Set to null if the person is not in the roster (external contact, unknown, or multiple people).

5. **individual_sources**: Array of individual source links when an item spans multiple threads/channels. Each has:
   - "label": Human-readable label (e.g., "Re: Q2 Board Deck — Draft", "Teams: Project Delivery")
   - "url": Direct link to the message/thread
   Only include this when there are 2+ distinct threads or channels. Omit (empty array) for single-source items.

Context about the user:
- If is_from_me is true on the most recent message, they already responded — actions are less likely
- If mentions_me or am_in_to is true and is_from_me is false, they probably need to act
- Items in CC only (am_in_cc=true, am_in_to=false) are more likely informational
- The user is Adam Nelson, a senior technology executive at Aptum

Discard items that are pure noise the deterministic filter missed (automated notifications, marketing, system alerts with no action needed). Set discard: true on these.

Respond with a JSON object. No markdown fences, no preamble:
{
  "items": [
    {
      "id": "item_id or cluster_id",
      "item_ids": ["id1", "id2"],
      "discard": false,
      "title": "Short Descriptive Title",
      "summary": "1-3 sentence summary.",
      "actions": [
        {"text": "Review the attachment before tomorrow's call", "completed": false, "completed_proof_url": null}
      ],
      "tracked_items": [
        {"text": "Jorge to amend the BI report filter", "completed": false, "completed_proof_url": null, "person": "jorge-quintero"}
      ],
      "individual_sources": [
        {"label": "Re: AWS Cloud Marketplace — Gina Tammo", "url": "https://..."},
        {"label": "Teams: Basis Discussion", "url": "https://..."}
      ]
    }
  ]
}"""


def _build_system_prompt() -> str:
    """Build the full system prompt, injecting the people roster if available."""
    people = _load_people_roster()
    roster_section = _build_roster_prompt(people)
    return _SYSTEM_PROMPT_BASE + roster_section


# Compute once at import time
SYSTEM_PROMPT = _build_system_prompt()

LLM_OUTPUT_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "item_ids": {"type": "array", "items": {"type": "string"}},
                    "discard": {"type": "boolean"},
                    "title": {"type": "string"},
                    "summary": {"type": "string"},
                    "actions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string"},
                                "completed": {"type": "boolean"},
                                "completed_proof_url": {"type": ["string", "null"]},
                            },
                            "required": ["text", "completed"],
                        },
                    },
                    "tracked_items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string"},
                                "completed": {"type": "boolean"},
                                "completed_proof_url": {"type": ["string", "null"]},
                                "person": {"type": ["string", "null"]},
                            },
                            "required": ["text", "completed"],
                        },
                    },
                    "individual_sources": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "label": {"type": "string"},
                                "url": {"type": "string"},
                            },
                        },
                    },
                },
                "required": [
                    "id",
                    "item_ids",
                    "discard",
                    "title",
                    "summary",
                    "actions",
                    "tracked_items",
                ],
            },
        }
    },
    "required": ["items"],
}


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
        "body_snippet": (item.get("body_snippet") or "")[:600],
        "message_count": item.get("message_count", 1),
        "first_timestamp": item.get("first_timestamp", ""),
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
        "url": item.get("url", ""),
    }


def _call_llm(payload: list) -> Optional[dict]:
    """
    Call the LLM via OpenRouter for triage.

    Uses call_structured from your existing openrouter.py connector.
    """
    from connectors.openrouter import call_structured

    model = os.getenv("DIGEST_LLM_MODEL", "anthropic/claude-sonnet-4-5")

    payload_json = json.dumps(payload, indent=2)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": payload_json},
    ]

    parsed, raw = call_structured(
        model=model,
        messages=messages,
        schema=LLM_OUTPUT_SCHEMA,
        schema_name="digest_output",
        temperature=0.1,
        max_tokens=14000,
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
    payload_json = json.dumps(payload, indent=2)
    print(f"  [summarize] Sending {len(payload)} groups to LLM ({len(payload_json):,} chars)...")

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

    llm_discarded = sum(1 for li in llm_items if li.get("discard"))

    action_count = sum(len(e.get("actions", [])) for e in enriched)
    tracking_count = sum(len(e.get("tracked_items", [])) for e in enriched)
    print(f"  [summarize] Model:    {model}")
    print(
        f"  [summarize] Tokens:   {tokens.get('prompt', 0):,} prompt + {tokens.get('completion', 0):,} completion = {tokens.get('total', 0):,} total"
    )
    print(f"  [summarize] Results:  {len(enriched)} items kept, {llm_discarded} discarded by LLM")
    print(f"  [summarize] Actions:  {action_count} actions, {tracking_count} tracked items")

    # Write output
    output = {
        "generated_at": utc_now(),
        "model": model,
        "tokens": tokens,
        "sources": processed.get("sources", []),
        "output": {
            "items": enriched,
            "discard_count": discard_count + llm_discarded,
        },
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"  [summarize] Wrote → {OUTPUT_PATH}")
    return 0


def _compute_source_stats(item_ids: list, id_to_item: dict) -> dict:
    """Deterministically compute source_stats from original item metadata (ET)."""
    et = ZoneInfo("America/New_York")
    counts: Dict[str, int] = {"email": 0, "teams": 0, "slack": 0}
    timestamps = []

    for iid in item_ids:
        orig = id_to_item.get(iid)
        if not orig:
            continue
        src = orig.get("source", "")
        counts[src] = counts.get(src, 0) + orig.get("message_count", 1)
        for key in ("first_timestamp", "last_timestamp"):
            ts = orig.get(key, "")
            if not ts:
                continue
            try:
                dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
                timestamps.append(dt.astimezone(et))
            except (ValueError, TypeError):
                try:
                    dt = datetime.fromtimestamp(float(ts), tz=timezone.utc).astimezone(et)
                    timestamps.append(dt)
                except (ValueError, TypeError):
                    continue

    if timestamps:
        earliest = min(timestamps)
        latest = max(timestamps)
        if earliest == latest:
            date_range = earliest.strftime("%Y-%m-%d %H:%M")
        elif earliest.date() == latest.date():
            date_range = f"{earliest.strftime('%Y-%m-%d %H:%M')}–{latest.strftime('%H:%M')}"
        else:
            date_range = f"{earliest.strftime('%Y-%m-%d %H:%M')}–{latest.strftime('%Y-%m-%d %H:%M')}"
    else:
        date_range = ""

    return {
        "email_count": counts.get("email", 0),
        "teams_count": counts.get("teams", 0),
        "slack_count": counts.get("slack", 0),
        "date_range": date_range,
    }


def _merge_llm_output(items: list, llm_items: list) -> list:
    """
    Merge LLM triage output back with original item metadata.
    """
    # Index original items by ID
    id_to_item = {item["id"]: item for item in items}

    enriched = []
    for llm_item in llm_items:
        if llm_item.get("discard"):
            continue

        item_ids = llm_item.get("item_ids", [])

        urls = []
        sources_set = set()
        for iid in item_ids:
            orig = id_to_item.get(iid)
            if not orig:
                continue
            sources_set.add(orig["source"])
            if orig.get("url"):
                urls.append({"source": orig["source"], "url": orig["url"], "subject": orig.get("subject")})

        stats = _compute_source_stats(item_ids, id_to_item)

        enriched.append({
            **llm_item,
            "urls": urls,
            "sources": list(sources_set),
            "source_stats": stats,
        })

    return enriched


def _write_empty_output(discard_count: int):
    output = {
        "generated_at": utc_now(),
        "model": "none",
        "tokens": {},
        "sources": [],
        "output": {
            "items": [],
            "discard_count": discard_count,
        },
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    raise SystemExit(main())
