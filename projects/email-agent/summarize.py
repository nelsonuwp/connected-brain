#!/usr/bin/env python3
"""
summarize.py

Reads emails_processed.json → calls LLM once per thread → writes a lean
LLMResponse JSON with no email bodies.

Changes vs v1:
  - System prompt includes TO-cardinality decision tree for action routing
  - Context block includes SOLE_RECIPIENT and ADAM_IN_TO flags
  - Schema adds unified_subject for merged threads
  - Merged thread handling: both source thread contents sent to LLM
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from connectors.llm_io import (
    build_user_message, make_llm_response, write_llm_response,
)
from connectors.openrouter import call_structured

# ── Env ───────────────────────────────────────────────────────────────────────

def _sq(v: str) -> str:
    v = v.strip()
    return v[1:-1] if len(v) >= 2 and v[0] == v[-1] in ('"', "'") else v

def load_env() -> None:
    root = Path(__file__).resolve().parents[1]
    for p in (Path.cwd() / ".env", root / ".env"):
        try:
            for raw in p.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                if k and (k not in os.environ or os.environ[k] == ""):
                    os.environ[k] = _sq(v)
        except OSError:
            pass


# ── Config ────────────────────────────────────────────────────────────────────

MODE = "inbox_triage"


# ── Prompt variants ───────────────────────────────────────────────────────────

_SYSTEM_BASE = """\
You are an executive assistant for Adam Nelson, VP of Operations at Aptum and \
CloudOps (managed cloud services: colocation, managed hosting, compute, cloud).

Internal domains: @aptum.com  @cloudops.com

Semantic rules:

category — exactly one of: waiting_on_me | waiting_on_others | new_information
  waiting_on_me:     thread needs Adam's response, decision, or action
  waiting_on_others: Adam already replied or is tracking; others must act next
  new_information:   report, announcement, FYI — no response expected from Adam

my_actions — things Adam himself must explicitly do, respond to, or decide.
  ONLY populate if there is a direct or clearly implied ask directed at Adam.
  Use this decision tree, in order:

  1. SOLE_RECIPIENT=True (Adam is the only person in TO):
     → Any request or question in the thread is directed at him.
       Add to my_actions if a reply or action is clearly needed.

  2. SOLE_RECIPIENT=False, ADAM_IN_TO=True (Adam is one of several TO recipients):
     → Only add to my_actions if the email names Adam explicitly, or the
       request is clearly personal to him (not a group ask).
     → If the question is ambiguous or addressed to the group with no clear
       owner, add to tracked_actions as: "Sent to group — owner unclear"
       Do NOT add to my_actions.

  3. ADAM_IN_TO=False (Adam is CC'd only):
     → Do NOT add to my_actions unless the body explicitly names Adam with
       a direct ask. Prefer tracked_actions or new_information.

  When in doubt, leave my_actions empty. An empty list is correct for FYI
  emails, group announcements, and anything where Adam is not the named owner.

tracked_actions — things others are doing that Adam should monitor.
  Only track items that are time-sensitive or have consequence if missed.
  For ambiguous group asks with no clear owner: "Sent to group — owner unclear"

unified_subject — for merged threads only: a short (≤8 words) subject that
  captures what both source threads are about. Null for non-merged threads.

sentiment — urgent | negative | positive | neutral\
"""

_ADDENDUM_NEEDS_RESPONSE = """

ROUTING HINT: The last message was NOT sent by Adam. Someone is waiting on him.
Focus on: what decision or response Adam must provide, and by when if implied.
Provide a suggested_reply when a reply is clearly warranted."""

_ADDENDUM_TRACKING = """

ROUTING HINT: Adam was the last sender. Others must act next.
Focus on: what others are doing, any risks or blockers, and whether Adam should
follow up if things have stalled. suggested_reply is likely null."""

_ADDENDUM_INFORMATION = """

ROUTING HINT: This is a forwarded report, single FYI, or automated dispatch.
Focus on: the key information Adam needs to retain and any implicit action items.
suggested_reply is almost certainly null."""

def _cached_system_msg(addendum: str) -> Dict:
    return {
        "role": "system",
        "content": [{
            "type":          "text",
            "text":          _SYSTEM_BASE + addendum,
            "cache_control": {"type": "ephemeral"},
        }],
    }

_SYSTEM_NEEDS_RESPONSE = _cached_system_msg(_ADDENDUM_NEEDS_RESPONSE)
_SYSTEM_TRACKING       = _cached_system_msg(_ADDENDUM_TRACKING)
_SYSTEM_INFORMATION    = _cached_system_msg(_ADDENDUM_INFORMATION)


# ── Schema ────────────────────────────────────────────────────────────────────

THREAD_SUMMARY_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "enum": ["waiting_on_me", "waiting_on_others", "new_information"],
            "description": "Current state of this thread from Adam's perspective.",
        },
        "unified_subject": {
            "type": ["string", "null"],
            "description": (
                "For IS_MERGED=True threads: a short (≤8 words) subject capturing "
                "what both source threads share. Null for non-merged threads."
            ),
        },
        "one_line": {
            "type": "string",
            "description": "TL;DR — 15 words maximum.",
        },
        "summary": {
            "type": "string",
            "description": "2–4 sentences: what this thread is about and where it stands.",
        },
        "my_actions": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Explicit action items for Adam — only when directly asked. "
                "Apply the SOLE_RECIPIENT/ADAM_IN_TO decision tree. Empty array if none."
            ),
        },
        "tracked_actions": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Things others are doing that Adam should monitor. "
                "Use 'Sent to group — owner unclear' for ambiguous group asks."
            ),
        },
        "sentiment": {
            "type": "string",
            "enum": ["neutral", "positive", "negative", "urgent"],
        },
        "suggested_reply": {
            "type": ["string", "null"],
            "description": (
                "Draft reply (2–5 sentences) only if my_actions is non-empty "
                "and a reply is clearly appropriate. Null otherwise."
            ),
        },
    },
    "required": [
        "category", "unified_subject", "one_line", "summary",
        "my_actions", "tracked_actions", "sentiment", "suggested_reply",
    ],
}


# ── Routing helpers ───────────────────────────────────────────────────────────

def _is_forward(thread: Dict) -> bool:
    return thread.get("is_forward", False)

def select_system_prompt(thread: Dict) -> Dict:
    if thread.get("last_sender_is_adam"):
        return _SYSTEM_TRACKING
    if _is_forward(thread):
        return _SYSTEM_INFORMATION
    return _SYSTEM_NEEDS_RESPONSE

def select_model(thread: Dict) -> Tuple[str, float]:
    total_body = sum(len(e.get("body") or "") for e in thread.get("emails", []))
    # Merged threads always get the workhorse — they contain multiple conversations
    if thread.get("is_merged"):
        return (os.getenv("MODEL_WORKHORSE", "anthropic/claude-sonnet-4-5"), 0.1)
    if thread.get("email_count", 1) == 1 and total_body < 800:
        return (os.getenv("MODEL_NANO", "anthropic/claude-haiku-4-5"), 0.1)
    return (os.getenv("MODEL_WORKHORSE", "anthropic/claude-sonnet-4-5"), 0.1)


# ── Message builders ──────────────────────────────────────────────────────────

def _context_block(thread: Dict) -> str:
    participants = ", ".join(
        p.get("name") or p.get("address", "")
        for p in thread.get("participants", [])
    )
    last = thread.get("last_sender") or {}
    lines = [
        f"THREAD:          {thread.get('subject')}",
        f"IS_MERGED:       {thread.get('is_merged', False)}",
        f"EMAIL_COUNT:     {thread.get('email_count')}",
        f"DATE_RANGE:      {(thread.get('first_sent') or '')[:10]} → {(thread.get('last_sent') or '')[:10]}",
        f"LAST_SENDER:     {last.get('name', '')} <{last.get('address', '')}>",
        f"LAST_IS_ADAM:    {thread.get('last_sender_is_adam', False)}",
        f"PARTICIPANTS:    {participants}",
        f"SOLE_RECIPIENT:  {thread.get('sole_recipient', False)}",
        f"ADAM_IN_TO:      {thread.get('adam_in_to', False)}",
    ]
    # For merged threads, list the original source threads so the LLM can
    # generate an informed unified_subject
    if thread.get("is_merged"):
        for st in (thread.get("source_threads") or []):
            lines.append(f"SOURCE_THREAD:   {st.get('subject', '')}")
    return "\n".join(lines)

def _note_content(thread: Dict) -> str:
    """
    Format thread emails as a numbered conversation.
    For merged threads, each email is labelled with its source thread subject.
    Last 2 emails: full body. Earlier emails: header + 200 chars.
    """
    emails  = thread.get("emails", [])
    n       = len(emails)
    cutoff  = max(0, n - 2)
    parts   = []

    for i, e in enumerate(emails):
        f        = e.get("from") or {}
        sender   = f.get("name") or f.get("address", "Unknown")
        date_str = (e.get("sent_at") or "")[:10]
        body     = e.get("body") or "(no body)"

        snippet  = body[:1500] if i >= cutoff else body[:200] + ("…" if len(body) > 200 else "")
        label    = "[FULL]" if i >= cutoff else "[SUMMARY]"

        # For merged threads, show which source thread each email belongs to
        source_note = ""
        if thread.get("is_merged") and e.get("_source_thread"):
            source_note = f" [from: {e['_source_thread'][:50]}]"

        parts.append(f"[{i+1}/{n}] {label}{source_note} {date_str}  {sender}\n{snippet}")

    return "\n\n---\n\n".join(parts)

def build_messages(thread: Dict) -> List[Dict]:
    user_content = build_user_message(
        note_content   = _note_content(thread),
        context_blocks = {"thread_metadata": _context_block(thread)},
        note_path      = f"thread/{thread.get('thread_id', 'unknown')}",
    )
    return [
        select_system_prompt(thread),
        {"role": "user", "content": user_content},
    ]


# ── LLM skip heuristics ───────────────────────────────────────────────────────

def _skip_llm(thread: Dict) -> Optional[Dict]:
    """
    Deterministically assign category for threads where the LLM adds no value.
    Merged threads always go to the LLM — no skip.
    """
    if thread.get("is_merged"):
        return None

    adam   = os.getenv("USER_EMAIL", "").lower()
    emails = thread.get("emails", [])
    n      = thread.get("email_count", 1)

    # Single email where Adam is the sender (self-forward)
    if n == 1 and emails:
        sender = (emails[0].get("from") or {}).get("address", "").lower()
        if adam and sender == adam:
            return {
                "category":        "new_information",
                "unified_subject": None,
                "one_line":        "Report or forward — no reply needed.",
                "summary":         "Adam forwarded this to himself for reference.",
                "my_actions":      [],
                "tracked_actions": [],
                "sentiment":       "neutral",
                "suggested_reply": None,
            }

    # No internal participants at all
    internal_domains = {"aptum.com", "cloudops.com"}
    participants     = thread.get("participants", [])
    has_internal     = any(
        (p.get("address") or "").lower().split("@")[-1] in internal_domains
        for p in participants
    )
    last_sender_addr = (thread.get("last_sender") or {}).get("address", "").lower()
    last_is_internal = last_sender_addr.split("@")[-1] in internal_domains if last_sender_addr else False

    if not has_internal and not last_is_internal:
        return {
            "category":        "new_information",
            "unified_subject": None,
            "one_line":        "External-only thread — no internal action expected.",
            "summary":         "All participants are external. No response expected from Adam.",
            "my_actions":      [],
            "tracked_actions": [],
            "sentiment":       "neutral",
            "suggested_reply": None,
        }

    return None


# ── LLM call ──────────────────────────────────────────────────────────────────

def summarize_thread(thread: Dict) -> Tuple[Dict, Optional[Dict], str]:
    model, temp = select_model(thread)

    lean = {
        "thread_id":           thread["thread_id"],
        "subject":             thread["subject"],
        "is_merged":           thread.get("is_merged", False),
        "source_threads":      thread.get("source_threads", []),
        "email_count":         thread["email_count"],
        "last_sent":           (thread.get("last_sent") or "")[:10],
        "last_sender_is_adam": thread.get("last_sender_is_adam", False),
        "participants":        thread.get("participants", []),
        "thread_url":          thread.get("thread_url"),
        "model_used":          model,
    }

    skip = _skip_llm(thread)
    if skip:
        lean["llm_summary"] = skip
        lean["llm_status"]  = "skipped"
        return lean, None, "skipped"

    parsed, raw = call_structured(
        model             = model,
        messages          = build_messages(thread),
        schema            = THREAD_SUMMARY_SCHEMA,
        schema_name       = "thread_summary",
        temperature       = temp,
        max_tokens        = 600,   # slightly more for merged threads
        verbosity         = "low",
        frequency_penalty = 0.1,
        seed              = 42,
    )

    if parsed:
        lean["llm_summary"] = {
            "category":        parsed.get("category",        "new_information"),
            "unified_subject": parsed.get("unified_subject"),
            "one_line":        parsed.get("one_line",        ""),
            "summary":         parsed.get("summary",         ""),
            "my_actions":      parsed.get("my_actions",      []),
            "tracked_actions": parsed.get("tracked_actions", []),
            "sentiment":       parsed.get("sentiment",       "neutral"),
            "suggested_reply": parsed.get("suggested_reply"),
        }
        lean["llm_status"] = "success"
        return lean, (raw.get("tokens") if raw else None), model

    lean["llm_summary"] = None
    lean["llm_status"]  = "failed"
    return lean, None, model


# ── Main ──────────────────────────────────────────────────────────────────────

_CATEGORY_ORDER = {"waiting_on_me": 0, "waiting_on_others": 1, "new_information": 2}

DEFAULT_INPUT  = Path(__file__).resolve().parent / "outputs" / "emails_processed.json"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "outputs" / "emails_summary.json"

def main() -> int:
    load_env()
    p = argparse.ArgumentParser(description="LLM summarize threads → LLMResponse JSON.")
    p.add_argument("-i", "--input",  default=str(DEFAULT_INPUT))
    p.add_argument("-o", "--output", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    try:
        processed = json.loads(Path(args.input).read_text(encoding="utf-8"))
        run_id_in = processed.get("run_id", "")
    except Exception:
        processed, run_id_in = {}, ""

    response = make_llm_response(
        model  = os.getenv("MODEL_WORKHORSE", "anthropic/claude-sonnet-4-5"),
        mode   = MODE,
        run_id = run_id_in,
    )

    try:
        objects  = processed.get("objects") or {}
        threads  = (objects.get("threads")              or {}).get("data") or []
        signals  = (objects.get("system_notifications") or {}).get("data") or []
        discards = (objects.get("discard")              or {}).get("data") or []

        print(f"  Summarizing {len(threads)} threads …\n")

        summarized   = []
        total_tokens = {"prompt": 0, "completion": 0, "total": 0}
        any_failure  = False
        nano_ct = workhorse_ct = skipped_ct = 0

        for i, thread in enumerate(threads):
            model, _ = select_model(thread)
            is_nano  = any(x in model.lower() for x in ("haiku", "nano", "flash"))
            tag      = "NANO   " if is_nano else "SONNET "
            merged_tag = " [MERGED]" if thread.get("is_merged") else ""
            print(f"  [{i+1:02d}/{len(threads)}] [{tag}]{merged_tag} {thread.get('subject', '?')[:50]}")

            lean, tokens, used_model = summarize_thread(thread)
            summarized.append(lean)

            if used_model == "skipped":
                skipped_ct += 1
            elif tokens:
                for k in total_tokens:
                    total_tokens[k] += tokens.get(k, 0)
                if is_nano: nano_ct      += 1
                else:       workhorse_ct += 1

            if lean.get("llm_status") == "failed":
                any_failure = True

            if i < len(threads) - 1:
                time.sleep(0.05)

        summarized.sort(key=lambda t: t.get("last_sent", ""), reverse=True)
        summarized.sort(key=lambda t: _CATEGORY_ORDER.get(
            (t.get("llm_summary") or {}).get("category", "new_information"), 2
        ))

        response["output"] = {
            "threads":              summarized,
            "system_notifications": signals,
            "discard_count":        len(discards),
        }
        response["sources_used"] = ["threads"]
        response["tokens"]       = total_tokens
        response["status"]       = "partial" if any_failure else "success"

        wom = sum(1 for t in summarized if (t.get("llm_summary") or {}).get("category") == "waiting_on_me")
        woo = sum(1 for t in summarized if (t.get("llm_summary") or {}).get("category") == "waiting_on_others")
        ni  = sum(1 for t in summarized if (t.get("llm_summary") or {}).get("category") == "new_information")

        print(f"\n  Categories:    waiting_on_me={wom}  waiting_on_others={woo}  new_information={ni}")
        print(f"  Model routing: {skipped_ct} skipped  +  {nano_ct} nano  +  {workhorse_ct} workhorse")
        print(f"  Tokens:        prompt={total_tokens['prompt']}  "
              f"completion={total_tokens['completion']}  total={total_tokens['total']}")

    except Exception as e:
        response["status"] = "fail"
        response["error"]  = {"type": type(e).__name__, "message": str(e), "retryable": False}
        print(f"  Summarize failed: {e}")
        import traceback; traceback.print_exc()

    finally:
        write_llm_response(response, Path(args.output))
        print(f"  Wrote → {args.output}")

    return 0 if response["status"] in ("success", "partial") else 1


if __name__ == "__main__":
    raise SystemExit(main())
