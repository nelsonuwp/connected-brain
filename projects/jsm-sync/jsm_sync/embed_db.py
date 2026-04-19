"""
asyncpg helpers for the `ticket_embeddings` table.

Every connection that will pass `vector`-typed parameters must first have
`pgvector.asyncpg.register_vector(conn)` called on it. We use asyncpg's
`init` hook on the pool to do this once per acquired connection.
"""
from __future__ import annotations

import logging
from typing import Optional, Sequence

import asyncpg
import numpy as np
from pgvector.asyncpg import register_vector

from .embedder import MODEL_NAME

logger = logging.getLogger(__name__)


async def register_pgvector(conn: asyncpg.Connection) -> None:
    """Register the vector codec on a connection. Call this from pool `init=`."""
    await register_vector(conn)


async def list_issue_keys_needing_embedding(
    conn: asyncpg.Connection,
    model: str = MODEL_NAME,
    limit: Optional[int] = None,
) -> list[str]:
    """
    Return issue_keys whose embedding is missing OR stale.

    "Stale" = the tickets row has been updated more recently than the
    embedding was computed. We use `tickets.updated_at > ticket_embeddings.embedded_at`
    as the freshness predicate; cheap and good enough.
    """
    sql = """
        SELECT t.issue_key
        FROM tickets t
        LEFT JOIN ticket_embeddings e
               ON e.issue_key = t.issue_key AND e.model = $1
        WHERE t.deleted_at IS NULL
          AND (
                e.issue_key IS NULL
             OR t.updated_at > e.embedded_at
          )
        ORDER BY t.updated_at DESC
    """
    if limit is not None:
        sql += f" LIMIT {int(limit)}"
    rows = await conn.fetch(sql, model)
    return [r["issue_key"] for r in rows]


async def fetch_text_for_issue_keys(
    conn: asyncpg.Connection,
    issue_keys: Sequence[str],
) -> list[tuple[str, str, str]]:
    """Return a list of (issue_key, summary, description) for the given keys."""
    if not issue_keys:
        return []
    rows = await conn.fetch(
        """
        SELECT issue_key, summary, COALESCE(description, '') AS description
        FROM tickets
        WHERE issue_key = ANY($1::text[])
        """,
        list(issue_keys),
    )
    return [(r["issue_key"], r["summary"], r["description"]) for r in rows]


async def upsert_embeddings(
    conn: asyncpg.Connection,
    rows: Sequence[tuple[str, str, np.ndarray]],
    model: str = MODEL_NAME,
) -> int:
    """
    Upsert (issue_key, text_hash, vector) triples.

    Returns the number of rows written. Uses executemany for batch throughput.
    """
    if not rows:
        return 0
    await conn.executemany(
        """
        INSERT INTO ticket_embeddings (issue_key, model, text_hash, embedding, embedded_at)
        VALUES ($1, $2, $3, $4, NOW())
        ON CONFLICT (issue_key, model) DO UPDATE SET
            text_hash   = EXCLUDED.text_hash,
            embedding   = EXCLUDED.embedding,
            embedded_at = NOW()
        """,
        [(ik, model, h, vec) for (ik, h, vec) in rows],
    )
    return len(rows)


async def count_embeddings(conn: asyncpg.Connection, model: str = MODEL_NAME) -> int:
    row = await conn.fetchrow(
        "SELECT COUNT(*) AS c FROM ticket_embeddings WHERE model = $1",
        model,
    )
    return int(row["c"])
