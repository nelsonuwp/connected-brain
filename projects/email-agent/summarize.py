#!/usr/bin/env python3
"""
3_summarize_emails.py

Reads emails_processed.json (SourceArtifact), sends ONLY important + useful
emails to the LLM via OpenRouter, and writes a single LLMResponse artifact.

Message structure follows llm-io.md:
  system role  → executive assistant persona + output schema rules
  user role    → assembled via build_user_message(); email body is [NOTE:],
                 metadata (from/to/cc/subject/category) is a [CONTEXT:] block

spam + not_important are passed through untouched in output — no LLM call.

LLMResponse.output shape:
  {
    "important":     [ { ...email fields, "llm_summary": {...} }, ... ],
    "useful":        [ { ...email fields, "llm_summary": {...} }, ... ],
    "not_important": [ { ...email fields }, ... ],   # no llm_summary
    "spam":          [ { ...email fields }, ... ],   # no llm_summary
  }

Output: outputs/emails_summary.json

Usage:
  python 3_summarize_emails.py
  python 3_summarize_emails.py -i outputs/emails_processed.json -o outputs/emails_summary.json
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))  # email-agent root
from connectors.llm_io import (
    build_user_message,
    make_llm_response,
    write_llm_response,
)
from connectors.openrouter import call_json

# ── Env loading ───────────────────────────────────────────────────────────────

def _strip_quotes(v: str) -> str:
    v = v.strip()
    return v[1:-1] if len(v) >= 2 and v[0] == v[-1] in ('"', "'") else v

def load_env() -> None:
    root = Path(__file__).resolve().parents[2]  # .../connected-brain
    for path in (Path.cwd() / ".env", root / ".env"):
        try:
            for raw in path.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                if k and k not in os.environ:
                    os.environ[k] = _strip_quotes(v)
        except OSError:
            pass

# ── Config ────────────────────────────────────────────────────────────────────

MODE                  = "inbox_triage"
CATEGORIES_TO_PROCESS = {"important", "useful"}

# ── Prompt ────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """\
You are an executive assistant for Adam Nelson. Adam is in a senior sales and \
operations leadership role at Aptum (a managed cloud services company) and CloudOps.

Your job is to read a single email and return a structured JSON object. \
Be direct and concise. Do not pad. Do not add preamble or sign-offs.

Rules:
- Internal emails from @aptum.com or @cloudops.com are work-critical.
- "my_actions" = things Adam himself must do or decide.
- "tracked_actions" = things others are doing that Adam should monitor or follow up on.
- "suggested_reply" = a short draft reply (2–5 sentences) only when my_actions is \
non-empty and a reply is appropriate. Otherwise null.
- "sentiment" must be exactly one of: neutral, positive, negative, urgent.

Respond ONLY with a valid JSON object — no markdown fences, no commentary:
{
  "one_line":        "<max 15-word TL;DR>",
  "summary":         "<2–4 sentence narrative of what this email is about>",
  "my_actions":      ["<action item for Adam>"],
  "tracked_actions": ["<thing someone else is doing that Adam should watch>"],
  "sentiment":       "neutral|positive|negative|urgent",
  "suggested_reply": "<draft reply or null>"
}\
"""

# ── Message builders ──────────────────────────────────────────────────────────

def _email_context_block(email: Dict) -> str:
    """
    Metadata for the [CONTEXT:] block — structured header info only.
    Body text goes into the [NOTE:] block via build_user_message().
    """
    from_str = f"{email['from']['name']} <{email['from']['address']}>"
    to_str   = ", ".join(f"{a['name']} <{a['address']}>" for a in email.get("to", []))
    cc_str   = ", ".join(f"{a['name']} <{a['address']}>" for a in email.get("cc", []))
    lines    = [
        f"DATE:     {email.get('sent_at', 'unknown')}",
        f"SUBJECT:  {email.get('subject', '(no subject)')}",
        f"FROM:     {from_str}",
        f"TO:       {to_str}",
        f"CATEGORY: {email.get('category', 'unknown')} — {email.get('category_reason', '')}",
        f"IS_REPLY: {email.get('is_reply', False)}",
    ]
    if cc_str:
        lines.append(f"CC:       {cc_str}")
    return "\n".join(lines)


def _email_note_content(email: Dict) -> str:
    """
    The note content — latest message body + optional thread history.
    This becomes the [NOTE: ...] block in the assembled user message.
    """
    body    = email.get("body") or "(no body)"
    history = email.get("thread_history")
    parts   = ["--- LATEST MESSAGE ---", body]
    if history:
        # Cap thread history to avoid blowing context on long chains
        parts += ["", "--- PRIOR THREAD ---", history[:3000]]
    return "\n".join(parts)


def build_messages_for_email(email: Dict) -> list:
    """
    Assembles the full messages[] array following llm-io.md pattern 1
    (single-shot: one system, one user).

    system  → persona + output schema (SYSTEM_PROMPT)
    user    → build_user_message() with:
                context_blocks = { "email_metadata": header fields }
                note_path      = "email/<id>"
                note_content   = latest body + thread history
    """
    context_blocks = {
        "email_metadata": _email_context_block(email)
    }
    note_path    = f"email/{email.get('id', 'unknown')[:16]}"
    note_content = _email_note_content(email)

    user_content = build_user_message(
        note_content   = note_content,
        context_blocks = context_blocks,
        note_path      = note_path,
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": user_content},
    ]

# ── Per-email LLM call ────────────────────────────────────────────────────────

def summarize_one(email: Dict, model: str, temperature: float) -> tuple[Dict, Optional[Dict]]:
    """
    Calls LLM for a single email.
    Returns (enriched_email, token_dict | None).
    enriched_email always has llm_summary (or None) and llm_status.
    """
    messages            = build_messages_for_email(email)
    parsed, raw         = call_json(model=model, messages=messages,
                                    temperature=temperature, max_tokens=600)
    enriched            = {**email}

    if parsed:
        enriched["llm_summary"] = {
            "one_line":        parsed.get("one_line",        ""),
            "summary":         parsed.get("summary",         ""),
            "my_actions":      parsed.get("my_actions",      []),
            "tracked_actions": parsed.get("tracked_actions", []),
            "sentiment":       parsed.get("sentiment",       "neutral"),
            "suggested_reply": parsed.get("suggested_reply", None),
        }
        enriched["llm_status"] = "success"
        return enriched, raw.get("tokens") if raw else None
    else:
        enriched["llm_summary"] = None
        enriched["llm_status"]  = "failed"
        return enriched, None

# ── Main ──────────────────────────────────────────────────────────────────────

DEFAULT_INPUT  = Path(__file__).resolve().parent / "outputs" / "emails_processed.json"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "outputs" / "emails_summary.json"

def main() -> int:
    load_env()

    p = argparse.ArgumentParser(description="LLM summarize emails → LLMResponse JSON.")
    p.add_argument("-i", "--input",  default=str(DEFAULT_INPUT))
    p.add_argument("-o", "--output", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    input_path  = Path(args.input)
    output_path = Path(args.output)

    model       = os.getenv("MODEL_WORKHORSE",         "anthropic/claude-sonnet-4-5")
    temperature = float(os.getenv("TEMPERATURE_WORKHORSE", "0.4"))
    print(f"  Model: {model}  temp={temperature}")

    # Pull run_id from upstream artifact if present (keeps the chain traceable)
    try:
        upstream   = json.loads(input_path.read_text(encoding="utf-8"))
        run_id_in  = upstream.get("run_id", "")
    except Exception:
        upstream, run_id_in = {}, ""

    response = make_llm_response(model=model, mode=MODE, run_id=run_id_in)

    try:
        objects = upstream.get("objects") or {}
        output_buckets: Dict[str, List] = {}
        total_tokens   = {"prompt": 0, "completion": 0, "total": 0}
        sources_used: list[str] = []
        any_failure    = False

        for cat, obj in objects.items():
            emails = obj.get("data") or []

            if cat not in CATEGORIES_TO_PROCESS:
                # Pass through — audit trail preserved, no LLM spend
                output_buckets[cat] = emails
                print(f"  {cat:15s} → {len(emails):3d} passed through (no LLM)")
                continue

            print(f"  {cat:15s} → {len(emails):3d} to summarize …")
            sources_used.append(cat)
            summarized = []

            for i, email in enumerate(emails):
                label = (email.get("subject") or "?")[:60]
                print(f"    [{i+1}/{len(emails)}] {label}")

                enriched, tokens = summarize_one(email, model, temperature)
                summarized.append(enriched)

                if tokens:
                    for k in total_tokens:
                        total_tokens[k] += tokens.get(k, 0)
                if enriched["llm_status"] == "failed":
                    any_failure = True

                if i < len(emails) - 1:
                    time.sleep(0.3)  # gentle rate-limit

            output_buckets[cat] = summarized

        response["output"]       = output_buckets
        response["sources_used"] = sources_used
        response["tokens"]       = total_tokens
        response["status"]       = "partial" if any_failure else "success"

    except Exception as e:
        response["status"] = "fail"
        response["error"]  = {"type": type(e).__name__, "message": str(e), "retryable": False}
        print(f"  Summarize failed: {e}")

    finally:
        write_llm_response(response, output_path)
        print(f"  Wrote → {output_path}")
        if response["status"] == "success":
            t = response["tokens"]
            print(f"  Tokens: prompt={t['prompt']}  completion={t['completion']}  total={t['total']}")

    return 0 if response["status"] in ("success", "partial") else 1

if __name__ == "__main__":
    raise SystemExit(main())
