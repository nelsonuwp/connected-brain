"""
Orchestrates: ticket → classify → fetch examples → build prompt → LLM → log.
"""

import logging

from .classifier import classify
from .db import get_ticket, log_draft
from .llm import generate_draft
from .patterns import REGISTERED_PATTERNS

logger = logging.getLogger(__name__)


async def draft_for_ticket(conn, issue_key: str) -> dict:
    """
    Classify a ticket, generate a draft, log it.

    Returns a dict with status and draft metadata. Possible statuses:
      - "ok"              — draft generated and logged
      - "no_pattern_match"— no pattern matched this ticket
      - "no_examples"     — pattern matched but assignee has no past examples
    """
    ticket = await get_ticket(conn, issue_key)
    if not ticket:
        raise ValueError(f"Ticket not found: {issue_key}")

    slug = classify(ticket)
    if not slug:
        return {
            "status": "no_pattern_match",
            "issue_key": issue_key,
            "message": "No pattern matched this ticket. Manual drafting required.",
        }

    pattern = next(p for p in REGISTERED_PATTERNS if p.slug == slug)
    examples = await pattern.fetch_examples(conn, ticket)

    if not examples:
        return {
            "status": "no_examples",
            "issue_key": issue_key,
            "pattern_slug": slug,
            "pattern_display_name": pattern.display_name,
            "message": (
                "Pattern matched, but no past examples found for the assigned engineer. "
                "A generic draft would be low-quality. "
                "Consider assigning the ticket to an engineer with prior history, "
                "or widening the lookback window in jsm-sync."
            ),
        }

    system_prompt, user_prompt = pattern.build_prompt(ticket, examples)

    logger.info(
        "Generating draft for %s via pattern=%s model=%s",
        issue_key, slug, "workhorse",
    )
    llm_result = await generate_draft(system_prompt, user_prompt)

    draft_id = await log_draft(conn, {
        "issue_key": issue_key,
        "pattern_slug": slug,
        "engineer_account_id": ticket.get("assignee_account_id"),
        "prompt_tokens": llm_result["input_tokens"],
        "completion_tokens": llm_result["output_tokens"],
        "model": llm_result["model"],
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "generated_text": llm_result["text"],
    })

    return {
        "status": "ok",
        "draft_id": draft_id,
        "issue_key": issue_key,
        "pattern_slug": slug,
        "pattern_display_name": pattern.display_name,
        "examples_used": len(examples),
        "generated_text": llm_result["text"],
        "tokens": {
            "input": llm_result["input_tokens"],
            "output": llm_result["output_tokens"],
        },
    }
