#!/usr/bin/env python3
"""
summarize.py

Reads emails_processed.json → calls LLM once per thread → writes a lean
LLMResponse JSON with no email bodies.

Three prompt variants (selected per thread via routing hints):
  NEEDS_RESPONSE  — last_sender_is_adam=False: someone is waiting on Adam
  TRACKING        — last_sender_is_adam=True:  Adam replied, track others
  INFORMATION     — single email or forward:   extract key info, no reply

Token efficiency (from LLMOps research):
  Prompt caching   — cache_control on system messages (Anthropic native,
                      ~90% token discount on system prompt after first call
                      per variant; OpenRouter passes through to Anthropic)
  Model routing    — MODEL_NANO for simple single-email threads,
                      MODEL_WORKHORSE for multi-email conversations
  Body already capped at 1500 chars/email in process.py

Output categories (Option C — conversation state):
  waiting_on_me     Thread needs Adam's response or decision
  waiting_on_others Adam already acted; others must move
  new_information   FYI / report / announcement; no reply expected

Output: outputs/emails_summary.json
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
                if k and k not in os.environ:
                    os.environ[k] = _sq(v)
        except OSError:
            pass

# ── Config ────────────────────────────────────────────────────────────────────

MODE = "inbox_triage"

# ── Prompt variants ───────────────────────────────────────────────────────────
# Shared base is the same for all three variants. Each variant is cached
# independently — after the first call of each type, Anthropic caches the
# system prompt and all subsequent calls of that type skip those tokens.

_SYSTEM_BASE = """\
You are an executive assistant for Adam Nelson, VP of Operations at Aptum and \
CloudOps (managed cloud services: colocation, managed hosting, compute, cloud).

Internal domains: @aptum.com  @cloudops.com

Semantic rules:
- category: exactly one of waiting_on_me | waiting_on_others | new_information
    waiting_on_me:     thread needs Adam's response, decision, or action
    waiting_on_others: Adam already replied or is tracking; others must act next
    new_information:   report, announcement, FYI — no response expected from Adam
- my_actions:      things Adam himself must explicitly do, respond to, or decide
- tracked_actions: things others are doing that Adam should monitor or follow up on
- sentiment:       urgent (time-sensitive) | negative (problem/complaint) | \
positive (good news) | neutral\
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
    """
    Build a system message using Anthropic's prompt caching format.
    content must be an array (not a string) for cache_control to work.
    OpenRouter passes cache_control through to Anthropic natively.
    """
    return {
        "role": "system",
        "content": [{
            "type":          "text",
            "text":          _SYSTEM_BASE + addendum,
            "cache_control": {"type": "ephemeral"},
        }],
    }

# Pre-built once; reused across all calls of each type
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
            "description": "Explicit action items for Adam. Empty array if none.",
        },
        "tracked_actions": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Things others are doing that Adam should monitor. Empty if none.",
        },
        "sentiment": {
            "type": "string",
            "enum": ["neutral", "positive", "negative", "urgent"],
        },
        "suggested_reply": {
            "type": ["string", "null"],
            "description": "Draft reply (2–5 sentences) only if my_actions is non-empty "
                           "and a reply is clearly appropriate. Null otherwise.",
        },
    },
    "required": [
        "category", "one_line", "summary",
        "my_actions", "tracked_actions", "sentiment", "suggested_reply",
    ],
}

# ── Routing helpers ───────────────────────────────────────────────────────────

def _is_forward(thread: Dict) -> bool:
    """True if the originating email is a forward (no back-and-forth yet)."""
    for e in thread.get("emails", []):
        subj = (e.get("from", {}).get("address", "") or "").lower()  # wrong field
        # Check via thread subject instead
        break
    # Check the first email subject in the thread for Fw:/Fwd:
    first_email = thread.get("emails", [{}])[0]
    first_raw_subj = first_email.get("from", {})  # not right
    # Actually check thread email_count and last_sender_is_adam
    # A forward is typically: email_count == 1, subject came in as Fw:
    # We don't store original raw subject here, so use email_count as proxy
    return thread.get("email_count", 1) == 1

def select_system_prompt(thread: Dict) -> Dict:
    if thread.get("last_sender_is_adam"):
        return _SYSTEM_TRACKING
    if _is_forward(thread) or thread.get("email_count", 1) == 1:
        return _SYSTEM_INFORMATION
    return _SYSTEM_NEEDS_RESPONSE

def select_model(thread: Dict) -> Tuple[str, float]:
    """
    Route to nano for simple single-email threads, workhorse for conversations.
    Temperature is intentionally low (0.1) for both — this is extraction, not
    generation. We want the most probable interpretation, not creative variation.
    """
    total_body = sum(len(e.get("body") or "") for e in thread.get("emails", []))
    if thread.get("email_count", 1) == 1 and total_body < 800:
        return (
            os.getenv("MODEL_NANO", "anthropic/claude-haiku-4-5"),
            0.1,
        )
    return (
        os.getenv("MODEL_WORKHORSE", "anthropic/claude-sonnet-4-5"),
        0.1,
    )

# ── Message builders ──────────────────────────────────────────────────────────

def _context_block(thread: Dict) -> str:
    participants = ", ".join(
        p.get("name") or p.get("address", "")
        for p in thread.get("participants", [])
    )
    last = thread.get("last_sender") or {}
    return "\n".join([
        f"THREAD:        {thread.get('subject')}",
        f"EMAIL_COUNT:   {thread.get('email_count')}",
        f"DATE_RANGE:    {(thread.get('first_sent') or '')[:10]} → {(thread.get('last_sent') or '')[:10]}",
        f"LAST_SENDER:   {last.get('name', '')} <{last.get('address', '')}>",
        f"LAST_IS_ADAM:  {thread.get('last_sender_is_adam', False)}",
        f"PARTICIPANTS:  {participants}",
    ])

def _note_content(thread: Dict) -> str:
    """
    Format thread as a numbered conversation for the [NOTE:] block.

    Outlook embeds the entire prior thread in every reply, so a 7-email thread
    would send the same paragraphs 6 times at full length. Instead:
      - Last 2 emails: full body (up to 1500 chars) — these are current and relevant
      - Earlier emails: header + first 200 chars — enough for context, not repetition

    This cuts input tokens on long threads by ~60% while keeping the LLM focused
    on what's actually new.
    """
    emails  = thread.get("emails", [])
    n       = len(emails)
    cutoff  = max(0, n - 2)   # index at which "full body" emails begin
    parts   = []

    for i, e in enumerate(emails):
        f        = e.get("from") or {}
        sender   = f.get("name") or f.get("address", "Unknown")
        date_str = (e.get("sent_at") or "")[:10]
        body     = e.get("body") or "(no body)"

        if i >= cutoff:
            # Recent email — full body
            snippet = body[:1500]
        else:
            # Older email — header + brief excerpt for context only
            snippet = body[:200] + ("…" if len(body) > 200 else "")

        label = "[FULL]" if i >= cutoff else "[SUMMARY]"
        parts.append(
            f"[{i+1}/{n}] {label} {date_str}  {sender}\n{snippet}"
        )

    return "\n\n---\n\n".join(parts)

def _skip_llm(thread: Dict) -> Optional[Dict]:
    """
    Deterministically assign category for threads where the LLM adds no value.
    Returns a pre-built llm_summary dict if skippable, None if LLM is needed.

    Skip cases:
      1. Single-email forward/report FROM Adam to himself — always new_information,
         no actions. These are Adam forwarding something to his own inbox.
      2. No internal participants at all — external sender, Adam didn't initiate.
         These are unsolicited external contacts that slipped past discard.
    """
    adam    = os.getenv("USER_EMAIL", "").lower()
    emails  = thread.get("emails", [])
    n       = thread.get("email_count", 1)

    # Case 1: Single email where Adam is the sender (self-forward / FYI forward)
    if n == 1 and emails:
        sender = (emails[0].get("from") or {}).get("address", "").lower()
        if adam and sender == adam:
            return {
                "category":        "new_information",
                "one_line":        "Report or forward — no reply needed.",
                "summary":         "Adam forwarded this to himself for reference.",
                "my_actions":      [],
                "tracked_actions": [],
                "sentiment":       "neutral",
                "suggested_reply": None,
            }

    # Case 2: No internal participants (external-only thread)
    internal_domains = {"aptum.com", "cloudops.com"}
    participants = thread.get("participants", [])
    has_internal = any(
        (p.get("address") or "").lower().split("@")[-1] in internal_domains
        for p in participants
    )
    last_sender_addr = (thread.get("last_sender") or {}).get("address", "").lower()
    last_is_internal = last_sender_addr.split("@")[-1] in internal_domains if last_sender_addr else False

    if not has_internal and not last_is_internal:
        return {
            "category":        "new_information",
            "one_line":        "External-only thread — no internal action expected.",
            "summary":         "All participants are external. No response expected from Adam.",
            "my_actions":      [],
            "tracked_actions": [],
            "sentiment":       "neutral",
            "suggested_reply": None,
        }

    return None

def build_messages(thread: Dict) -> List[Dict]:
    """
    Build chat messages for the structured LLM call.

    Uses a cached system prompt variant plus a single user [NOTE:] payload that
    includes the thread metadata block and a trimmed conversation transcript.
    """
    user_content = build_user_message(
        note_content=_note_content(thread),
        context_blocks={"thread_metadata": _context_block(thread)},
        note_path=f"thread/{thread.get('thread_id', 'unknown')}",
    )
    return [
        select_system_prompt(thread),
        {"role": "user", "content": user_content},
    ]

# ── LLM call ─────────────────────────────────────────────────────────────────

def summarize_thread(thread: Dict) -> Tuple[Dict, Optional[Dict], str]:
    """Returns (lean_output, token_dict | None, model_used)."""
    model, temp = select_model(thread)

    lean = {
        "thread_id":           thread["thread_id"],
        "subject":             thread["subject"],
        "email_count":         thread["email_count"],
        "last_sent":           (thread.get("last_sent") or "")[:10],
        "last_sender_is_adam": thread.get("last_sender_is_adam", False),
        "participants":        thread.get("participants", []),
        "thread_url":          thread.get("thread_url"),
        "model_used":          model,
    }

    # Check if we can skip the LLM entirely
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
        max_tokens        = 500,
        verbosity         = "low",
        frequency_penalty = 0.1,
        seed              = 42,     # reproducibility — same input → same output
    )

    if parsed:
        lean["llm_summary"] = {
            "category":        parsed.get("category",        "new_information"),
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
            print(f"  [{i+1:02d}/{len(threads)}] [{tag}] {thread.get('subject', '?')[:55]}")

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
                time.sleep(0.2)

        # Sort: category priority ASC, then last_sent DESC within each category
        # Two stable sorts (Python guarantees stability)
        summarized.sort(key=lambda t: t.get("last_sent", ""), reverse=True)
        summarized.sort(key=lambda t: _CATEGORY_ORDER.get(
            (t.get("llm_summary") or {}).get("category", "new_information"), 2
        ))

        response["output"] = {
            "threads":              summarized,   # lean — no bodies
            "system_notifications": signals,      # passthrough from process.py
            "discard_count":        len(discards),
        }
        response["sources_used"] = ["threads"]
        response["tokens"]       = total_tokens
        response["status"]       = "partial" if any_failure else "success"

        wom = sum(1 for t in summarized
                  if (t.get("llm_summary") or {}).get("category") == "waiting_on_me")
        woo = sum(1 for t in summarized
                  if (t.get("llm_summary") or {}).get("category") == "waiting_on_others")
        ni  = sum(1 for t in summarized
                  if (t.get("llm_summary") or {}).get("category") == "new_information")

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