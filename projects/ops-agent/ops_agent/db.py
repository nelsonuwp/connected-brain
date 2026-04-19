"""
asyncpg pool + read helpers against jsm_sync tables + write helpers for ops schema.

ops-agent only SELECTs from jsm_sync's tables. If it needs its own state
it writes to the 'ops' schema (e.g. ops.draft_log).
"""

import logging
from typing import Optional

import asyncpg

from .config import settings
from .embedder import MODEL_NAME

logger = logging.getLogger(__name__)

_pool: Optional[asyncpg.Pool] = None


# ---------------------------------------------------------------------------
# Pool lifecycle
# ---------------------------------------------------------------------------

async def _register_pgvector_on_conn(conn: asyncpg.Connection) -> None:
    """Register pgvector codec on each acquired connection. Best-effort —
    if pgvector isn't installed yet (e.g. during initial migration) we
    log and continue."""
    try:
        from pgvector.asyncpg import register_vector

        await register_vector(conn)
    except Exception as e:
        logger.warning("pgvector.asyncpg.register_vector failed: %s", e)


async def init_pool() -> None:
    global _pool
    if _pool is not None:
        return
    _pool = await asyncpg.create_pool(
        dsn=settings.database_url,
        min_size=1,
        max_size=10,
        command_timeout=30,
        init=_register_pgvector_on_conn,
    )
    logger.info("DB pool ready → %s", settings.database_url)


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


async def get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("DB pool not initialized — call init_pool() first")
    return _pool


# ---------------------------------------------------------------------------
# Read helpers — jsm_sync tables
# ---------------------------------------------------------------------------

async def list_tickets(
    conn: asyncpg.Connection,
    limit: int = 50,
    customer_originated: Optional[bool] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
) -> list[dict]:
    conditions = ["t.deleted_at IS NULL"]
    params: list = [MODEL_NAME]
    idx = 2

    if customer_originated is not None:
        conditions.append(f"t.is_customer_originated = ${idx}")
        params.append(customer_originated)
        idx += 1

    if status:
        conditions.append(f"t.status = ${idx}")
        params.append(status)
        idx += 1

    if search:
        conditions.append(f"t.summary ILIKE ${idx}")
        params.append(f"%{search}%")
        idx += 1

    where = " AND ".join(conditions)
    limit_param = idx
    params.append(limit)

    rows = await conn.fetch(
        f"""
        WITH anchors AS (
            SELECT
                t.issue_key,
                t.summary,
                t.status,
                t.priority,
                t.is_customer_originated,
                t.created_at,
                t.updated_at,
                t.request_type,
                t.ocean_client_id,
                o.name AS jira_org_name,
                u.display_name AS assignee_display_name
            FROM tickets t
            LEFT JOIN organizations o ON o.jira_org_id = t.jira_org_id
            LEFT JOIN jira_users u ON u.account_id = t.assignee_account_id
            WHERE {where}
            ORDER BY t.updated_at DESC
            LIMIT ${limit_param}
        ),
        anchor_services AS (
            SELECT
                a.issue_key,
                COALESCE(
                    ARRAY_AGG(DISTINCT ast.service_id::text) FILTER (
                        WHERE ast.service_id IS NOT NULL
                          AND btrim(ast.service_id::text) <> ''
                    ),
                    ARRAY[]::text[]
                ) AS service_ids
            FROM anchors a
            LEFT JOIN ticket_assets ta ON ta.issue_key = a.issue_key
            LEFT JOIN assets ast ON ast.object_id = ta.object_id
            GROUP BY a.issue_key
        ),
        cust AS (
            SELECT
                a.issue_key,
                COALESCE(SUM((s.sim >= 0.90)::int), 0)::int AS c90,
                COALESCE(SUM((s.sim >= 0.70)::int), 0)::int AS c70
            FROM anchors a
            INNER JOIN ticket_embeddings ae
                ON ae.issue_key = a.issue_key AND ae.model = $1
            LEFT JOIN LATERAL (
                SELECT (1 - (oe.embedding <=> ae.embedding))::double precision AS sim
                FROM tickets ot
                INNER JOIN ticket_embeddings oe
                    ON oe.issue_key = ot.issue_key AND oe.model = $1
                WHERE a.ocean_client_id IS NOT NULL
                  AND ot.ocean_client_id = a.ocean_client_id
                  AND ot.issue_key <> a.issue_key
                  AND ot.deleted_at IS NULL
                ORDER BY oe.embedding <=> ae.embedding
                LIMIT 20
            ) s ON TRUE
            GROUP BY a.issue_key
        ),
        nbr AS (
            SELECT
                a.issue_key,
                COALESCE(SUM((s.sim >= 0.90)::int), 0)::int AS n90,
                COALESCE(SUM((s.sim >= 0.70)::int), 0)::int AS n70
            FROM anchors a
            INNER JOIN ticket_embeddings ae
                ON ae.issue_key = a.issue_key AND ae.model = $1
            LEFT JOIN anchor_services svc ON svc.issue_key = a.issue_key
            LEFT JOIN LATERAL (
                SELECT (1 - (oe.embedding <=> ae.embedding))::double precision AS sim
                FROM tickets ot
                INNER JOIN ticket_embeddings oe
                    ON oe.issue_key = ot.issue_key AND oe.model = $1
                WHERE ot.deleted_at IS NULL
                  AND ot.issue_key <> a.issue_key
                  AND cardinality(COALESCE(svc.service_ids, ARRAY[]::text[])) > 0
                  AND EXISTS (
                      SELECT 1
                      FROM ticket_assets ta
                      INNER JOIN assets ast ON ast.object_id = ta.object_id
                      WHERE ta.issue_key = ot.issue_key
                        AND ast.service_id = ANY(svc.service_ids)
                  )
                ORDER BY oe.embedding <=> ae.embedding
                LIMIT 20
            ) s ON TRUE
            GROUP BY a.issue_key
        )
        SELECT
            a.issue_key,
            a.summary,
            a.status,
            a.priority,
            a.is_customer_originated,
            a.created_at,
            a.updated_at,
            a.request_type,
            a.jira_org_name,
            a.assignee_display_name,
            CASE
                WHEN ae.embedding IS NULL THEN NULL
                ELSE LEAST(
                    100,
                    COALESCE(c.c90, 0) * 5
                    + (COALESCE(c.c70, 0) - COALESCE(c.c90, 0)) * 2
                    + COALESCE(n.n90, 0) * 3
                    + (COALESCE(n.n70, 0) - COALESCE(n.n90, 0))
                )::int
            END AS familiarity_score
        FROM anchors a
        LEFT JOIN ticket_embeddings ae
            ON ae.issue_key = a.issue_key AND ae.model = $1
        LEFT JOIN cust c ON c.issue_key = a.issue_key
        LEFT JOIN nbr n ON n.issue_key = a.issue_key
        """,
        *params,
    )
    return [dict(r) for r in rows]


async def get_ticket(conn: asyncpg.Connection, issue_key: str) -> Optional[dict]:
    row = await conn.fetchrow(
        """
        SELECT
            t.*,
            o.name AS jira_org_name,
            u_a.display_name AS assignee_display_name,
            u_c.display_name AS creator_display_name,
            u_r.display_name AS reporter_display_name
        FROM tickets t
        LEFT JOIN organizations o    ON o.jira_org_id = t.jira_org_id
        LEFT JOIN jira_users u_a     ON u_a.account_id = t.assignee_account_id
        LEFT JOIN jira_users u_c     ON u_c.account_id = t.creator_account_id
        LEFT JOIN jira_users u_r     ON u_r.account_id = t.reporter_account_id
        WHERE t.issue_key = $1 AND t.deleted_at IS NULL
        """,
        issue_key,
    )
    return dict(row) if row else None


async def get_thread(conn: asyncpg.Connection, issue_key: str) -> list[dict]:
    rows = await conn.fetch(
        """
        SELECT
            te.id, te.kind, te.is_public, te.body, te.created_at,
            te.author_account_id,
            u.display_name AS author_display_name,
            u.role AS author_role
        FROM thread_events te
        LEFT JOIN jira_users u ON u.account_id = te.author_account_id
        WHERE te.issue_key = $1 AND te.deleted_at IS NULL
        ORDER BY te.created_at ASC
        """,
        issue_key,
    )
    return [dict(r) for r in rows]


async def get_ticket_assets(conn: asyncpg.Connection, issue_key: str) -> list[dict]:
    rows = await conn.fetch(
        """
        SELECT a.object_id, a.asset_name, a.service_id, a.workspace_id
        FROM assets a
        JOIN ticket_assets ta ON ta.object_id = a.object_id
        WHERE ta.issue_key = $1
        ORDER BY a.asset_name
        """,
        issue_key,
    )
    return [dict(r) for r in rows]


async def get_organization(conn: asyncpg.Connection, jira_org_id: str) -> Optional[dict]:
    row = await conn.fetchrow(
        "SELECT * FROM organizations WHERE jira_org_id = $1",
        jira_org_id,
    )
    return dict(row) if row else None


async def get_ticket_assignee(conn: asyncpg.Connection, issue_key: str) -> Optional[dict]:
    row = await conn.fetchrow(
        """
        SELECT u.*
        FROM jira_users u
        JOIN tickets t ON t.assignee_account_id = u.account_id
        WHERE t.issue_key = $1
        """,
        issue_key,
    )
    return dict(row) if row else None


async def list_customer_tickets(
    conn: asyncpg.Connection,
    ocean_client_id: int,
    *,
    exclude_issue_key: str,
    limit: int = 30,
) -> list[dict]:
    rows = await conn.fetch(
        """
        SELECT
            t.issue_key, t.summary, t.status, t.ocean_client_id, t.updated_at, t.resolved_at,
            org.name AS jira_org_name
        FROM tickets t
        LEFT JOIN organizations org ON org.jira_org_id = t.jira_org_id
        WHERE t.ocean_client_id = $1
          AND t.deleted_at IS NULL
          AND t.issue_key <> $2
        ORDER BY t.updated_at DESC
        LIMIT $3
        """,
        ocean_client_id,
        exclude_issue_key,
        limit,
    )
    return [dict(r) for r in rows]


async def list_tickets_for_service_ids(
    conn: asyncpg.Connection,
    service_ids: list[str],
    *,
    exclude_issue_key: str,
    limit: int = 25,
) -> list[dict]:
    if not service_ids:
        return []
    rows = await conn.fetch(
        """
        SELECT
            t.issue_key, t.summary, t.status, t.ocean_client_id, t.updated_at, t.resolved_at,
            org.name AS jira_org_name
        FROM tickets t
        LEFT JOIN organizations org ON org.jira_org_id = t.jira_org_id
        WHERE t.deleted_at IS NULL
          AND t.issue_key <> $2
          AND EXISTS (
            SELECT 1
            FROM ticket_assets ta
            JOIN assets a ON a.object_id = ta.object_id
            WHERE ta.issue_key = t.issue_key
              AND a.service_id = ANY($1::text[])
          )
        ORDER BY t.updated_at DESC
        LIMIT $3
        """,
        service_ids,
        exclude_issue_key,
        limit,
    )
    return [dict(r) for r in rows]


async def get_distinct_statuses(conn: asyncpg.Connection) -> list[str]:
    rows = await conn.fetch(
        "SELECT DISTINCT status FROM tickets WHERE deleted_at IS NULL ORDER BY status"
    )
    return [r["status"] for r in rows]


# ---------------------------------------------------------------------------
# Write helpers — ops schema
# ---------------------------------------------------------------------------

async def log_draft(conn: asyncpg.Connection, draft: dict) -> int:
    row = await conn.fetchrow(
        """
        INSERT INTO ops.draft_log
            (issue_key, pattern_slug, engineer_account_id,
             prompt_tokens, completion_tokens, model,
             system_prompt, user_prompt, generated_text,
             draft_type, persona_slug, system_prompt_override)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        RETURNING id
        """,
        draft["issue_key"],
        draft.get("pattern_slug"),
        draft.get("engineer_account_id"),
        draft.get("prompt_tokens"),
        draft.get("completion_tokens"),
        draft.get("model"),
        draft.get("system_prompt"),
        draft.get("user_prompt"),
        draft["generated_text"],
        draft.get("draft_type"),
        draft.get("persona_slug"),
        draft.get("system_prompt_override"),
    )
    return row["id"]


async def mark_draft_used(conn: asyncpg.Connection, draft_id: int) -> None:
    await conn.execute(
        "UPDATE ops.draft_log SET was_used = true WHERE id = $1",
        draft_id,
    )
