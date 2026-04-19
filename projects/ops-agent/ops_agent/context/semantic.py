"""
Semantic-similarity queries for the related-panel sidebar.

Strategy:
  1. Embed the current ticket's (summary, description) once.
  2. For each panel, run a filtered KNN against ticket_embeddings with
     ORDER BY embedding <=> $query_vec.
  3. If the result set is smaller than the desired limit (few or no
     embeddings exist for the filter group — e.g. a brand-new ticket),
     top up with recency-ordered tickets that don't yet have an embedding.

Rows returned always carry:
  - similarity_score: float in [-1, 1] (cosine sim; ~1 = very similar), or None for recency-padded rows
  - ranked_by:        "semantic" | "recency"
"""
from __future__ import annotations

import logging
from typing import Any, Optional

import asyncpg
import numpy as np

from ..embedder import MODEL_NAME, build_embed_text, embed_one

logger = logging.getLogger(__name__)


SEMANTIC_LIMIT_CUSTOMER = 15
SEMANTIC_LIMIT_NEIGHBOR = 15


def embed_current_ticket(summary: str, description: str) -> np.ndarray:
    return embed_one(build_embed_text(summary, description))


async def similar_customer_tickets(
    conn: asyncpg.Connection,
    query_vec: np.ndarray,
    ocean_client_id: int,
    *,
    exclude_issue_key: str,
    limit: int = SEMANTIC_LIMIT_CUSTOMER,
) -> list[dict[str, Any]]:
    """
    Vertical panel: tickets from the SAME customer, ranked by semantic
    similarity to the current ticket.
    """
    rows = await conn.fetch(
        """
        SELECT
            t.issue_key, t.summary, t.status, t.ocean_client_id,
            t.updated_at, t.resolved_at,
            org.name AS jira_org_name,
            1 - (e.embedding <=> $1) AS similarity_score
        FROM tickets t
        JOIN ticket_embeddings e
             ON e.issue_key = t.issue_key AND e.model = $4
        LEFT JOIN organizations org ON org.jira_org_id = t.jira_org_id
        WHERE t.ocean_client_id = $2
          AND t.deleted_at IS NULL
          AND t.issue_key <> $3
        ORDER BY e.embedding <=> $1
        LIMIT $5
        """,
        query_vec, ocean_client_id, exclude_issue_key, MODEL_NAME, limit,
    )
    out = []
    for r in rows:
        d = dict(r)
        d["ranked_by"] = "semantic"
        out.append(d)
    return out


async def similar_neighbor_tickets(
    conn: asyncpg.Connection,
    query_vec: np.ndarray,
    service_ids: list[str],
    *,
    exclude_issue_key: str,
    limit: int = SEMANTIC_LIMIT_NEIGHBOR,
) -> list[dict[str, Any]]:
    """
    Horizontal panel: tickets on neighbor services (similar hardware),
    ranked by semantic similarity to the current ticket.
    """
    if not service_ids:
        return []
    rows = await conn.fetch(
        """
        SELECT
            t.issue_key, t.summary, t.status, t.ocean_client_id,
            t.updated_at, t.resolved_at,
            org.name AS jira_org_name,
            1 - (e.embedding <=> $1) AS similarity_score
        FROM tickets t
        JOIN ticket_embeddings e
             ON e.issue_key = t.issue_key AND e.model = $4
        LEFT JOIN organizations org ON org.jira_org_id = t.jira_org_id
        WHERE t.deleted_at IS NULL
          AND t.issue_key <> $3
          AND EXISTS (
                SELECT 1
                FROM ticket_assets ta
                JOIN assets a ON a.object_id = ta.object_id
                WHERE ta.issue_key = t.issue_key
                  AND a.service_id = ANY($2::text[])
          )
        ORDER BY e.embedding <=> $1
        LIMIT $5
        """,
        query_vec, service_ids, exclude_issue_key, MODEL_NAME, limit,
    )
    out = []
    for r in rows:
        d = dict(r)
        d["ranked_by"] = "semantic"
        out.append(d)
    return out


def merge_with_recency_fallback(
    semantic_rows: list[dict[str, Any]],
    recency_rows: list[dict[str, Any]],
    *,
    target: int,
) -> list[dict[str, Any]]:
    """
    Pad `semantic_rows` up to `target` using `recency_rows`, skipping any
    issue_keys already present. Preserves order: semantic first, then recency.

    Recency-padded rows are tagged ranked_by="recency", similarity_score=None.
    """
    seen = {r["issue_key"] for r in semantic_rows}
    out = list(semantic_rows)
    for r in recency_rows:
        if len(out) >= target:
            break
        if r["issue_key"] in seen:
            continue
        rr = dict(r)
        rr.setdefault("similarity_score", None)
        rr.setdefault("ranked_by", "recency")
        out.append(rr)
        seen.add(r["issue_key"])
    return out
