"""
LLM draft flows: fix suggestion, internal note, public customer comment.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from .context.t_context import build_t_context
from .db import get_thread, get_ticket, log_draft
from .llm import generate_draft
from .personas import load_personas, persona_system_prompt

if TYPE_CHECKING:
    import asyncpg

logger = logging.getLogger(__name__)

FIX_SYSTEM = """You are a senior operations analyst. Your job is to suggest a likely
resolution path for the CURRENT ticket using ONLY the ticket text, thread, and the
RELATED CONTEXT sections (customer history, hardware components, neighbor services,
and similar tickets). Output Markdown with sections: Summary, Similar incidents,
Suggested next steps, Confidence (Low/Medium/High) with one sentence why.
If context is thin, say so explicitly. Do not fabricate tool output or ticket IDs
that are not in the context."""

INTERNAL_SYSTEM = """You are writing an internal note for the operations team (not
the customer). Be concise and technical. Reference only the ticket, thread, and
RELATED CONTEXT. Use bullets where helpful. No marketing tone."""


def _thread_digest(thread: list[dict], limit: int = 12) -> str:
    lines = []
    for ev in thread[-limit:]:
        who = ev.get("author_display_name") or ev.get("author_account_id") or "?"
        pub = "public" if ev.get("is_public") else "internal"
        body = (ev.get("body") or "").replace("\n", " ")[:400]
        lines.append(f"- [{pub}] {who}: {body}")
    return "\n".join(lines) if lines else "(no thread events)"


def _ticket_digest(ticket: dict) -> str:
    parts = [
        f"Issue: {ticket.get('issue_key')}",
        f"Summary: {ticket.get('summary')}",
        f"Status: {ticket.get('status')}  Priority: {ticket.get('priority')}",
        f"Type: {ticket.get('request_type') or ticket.get('issue_type')}",
    ]
    desc = ticket.get("description") or ""
    if desc.strip():
        parts.append(f"Description:\n{desc[:4000]}")
    return "\n".join(parts)


async def draft_fix_suggestion(conn: "asyncpg.Connection", pool, issue_key: str) -> dict:
    ticket = await get_ticket(conn, issue_key)
    if not ticket:
        return {"status": "error", "issue_key": issue_key, "message": "Ticket not found"}

    tctx = await build_t_context(pool, issue_key)
    if tctx.get("error") == "ticket_not_found":
        return {"status": "error", "issue_key": issue_key, "message": "Ticket not found"}

    thread = await get_thread(conn, issue_key)
    user_prompt = (
        _ticket_digest(ticket)
        + "\n\n=== THREAD (recent) ===\n"
        + _thread_digest(thread)
        + "\n\n=== RELATED CONTEXT ===\n"
        + tctx.get("prompt_block", "")
    )

    llm = await generate_draft(FIX_SYSTEM, user_prompt, max_tokens=2048)
    draft_id = await log_draft(
        conn,
        {
            "issue_key": issue_key,
            "pattern_slug": "t_context",
            "engineer_account_id": None,
            "prompt_tokens": llm["input_tokens"],
            "completion_tokens": llm["output_tokens"],
            "model": llm["model"],
            "system_prompt": FIX_SYSTEM,
            "user_prompt": user_prompt,
            "generated_text": llm["text"],
            "draft_type": "fix_suggestion",
            "persona_slug": None,
            "system_prompt_override": None,
        },
    )
    return {
        "status": "ok",
        "draft_type": "fix_suggestion",
        "draft_id": draft_id,
        "issue_key": issue_key,
        "title": "Potential fix analysis",
        "generated_text": llm["text"],
        "tokens": {"input": llm["input_tokens"], "output": llm["output_tokens"]},
    }


async def draft_internal_comment(conn: "asyncpg.Connection", pool, issue_key: str) -> dict:
    ticket = await get_ticket(conn, issue_key)
    if not ticket:
        return {"status": "error", "issue_key": issue_key, "message": "Ticket not found"}

    tctx = await build_t_context(pool, issue_key)
    thread = await get_thread(conn, issue_key)
    user_prompt = (
        _ticket_digest(ticket)
        + "\n\n=== THREAD (recent) ===\n"
        + _thread_digest(thread)
        + "\n\n=== RELATED CONTEXT ===\n"
        + tctx.get("prompt_block", "")
    )

    llm = await generate_draft(INTERNAL_SYSTEM, user_prompt, max_tokens=1024)
    draft_id = await log_draft(
        conn,
        {
            "issue_key": issue_key,
            "pattern_slug": "t_context",
            "engineer_account_id": None,
            "prompt_tokens": llm["input_tokens"],
            "completion_tokens": llm["output_tokens"],
            "model": llm["model"],
            "system_prompt": INTERNAL_SYSTEM,
            "user_prompt": user_prompt,
            "generated_text": llm["text"],
            "draft_type": "internal",
            "persona_slug": None,
            "system_prompt_override": None,
        },
    )
    return {
        "status": "ok",
        "draft_type": "internal",
        "draft_id": draft_id,
        "issue_key": issue_key,
        "title": "Internal comment draft",
        "generated_text": llm["text"],
        "tokens": {"input": llm["input_tokens"], "output": llm["output_tokens"]},
    }


async def draft_public_comment(
    conn: "asyncpg.Connection",
    pool,
    issue_key: str,
    persona_slug: str,
    system_prompt_override: Optional[str] = None,
) -> dict:
    personas = load_personas()
    persona = personas.get(persona_slug)
    if not persona:
        return {
            "status": "error",
            "issue_key": issue_key,
            "message": f"Unknown persona: {persona_slug}",
        }

    base_system = persona_system_prompt(persona)
    system_prompt = (system_prompt_override or "").strip() or base_system

    ticket = await get_ticket(conn, issue_key)
    if not ticket:
        return {"status": "error", "issue_key": issue_key, "message": "Ticket not found"}

    tctx = await build_t_context(pool, issue_key)
    thread = await get_thread(conn, issue_key)
    user_prompt = (
        "Write a single customer-facing reply (plain text or light Markdown) "
        "as the next public comment on this ticket.\n\n"
        + _ticket_digest(ticket)
        + "\n\n=== THREAD (recent, respect public vs internal) ===\n"
        + _thread_digest(thread)
        + "\n\n=== RELATED CONTEXT (use only to inform accuracy; do not mention internal systems by name unless customer already did) ===\n"
        + tctx.get("prompt_block", "")
    )

    llm = await generate_draft(system_prompt, user_prompt, max_tokens=1200)
    override_logged = system_prompt if system_prompt != base_system else None
    draft_id = await log_draft(
        conn,
        {
            "issue_key": issue_key,
            "pattern_slug": persona_slug,
            "engineer_account_id": ticket.get("assignee_account_id"),
            "prompt_tokens": llm["input_tokens"],
            "completion_tokens": llm["output_tokens"],
            "model": llm["model"],
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "generated_text": llm["text"],
            "draft_type": "public",
            "persona_slug": persona_slug,
            "system_prompt_override": override_logged,
        },
    )
    return {
        "status": "ok",
        "draft_type": "public",
        "draft_id": draft_id,
        "issue_key": issue_key,
        "title": f"Public comment ({persona.label})",
        "persona_label": persona.label,
        "generated_text": llm["text"],
        "tokens": {"input": llm["input_tokens"], "output": llm["output_tokens"]},
    }
