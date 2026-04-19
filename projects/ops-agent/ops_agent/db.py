"""
asyncpg pool + read helpers against jsm_sync tables + write helpers for ops schema.

ops-agent only SELECTs from jsm_sync's tables. If it needs its own state
it writes to the 'ops' schema (e.g. ops.draft_log).
"""

import logging
from typing import Optional

import asyncpg

from .config import settings

logger = logging.getLogger(__name__)

_pool: Optional[asyncpg.Pool] = None


# ---------------------------------------------------------------------------
# Pool lifecycle
# ---------------------------------------------------------------------------

async def init_pool() -> None:
    global _pool
    if _pool is not None:
        return
    _pool = await asyncpg.create_pool(
        dsn=settings.database_url,
        min_size=1,
        max_size=10,
        command_timeout=30,
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
    params: list = []
    idx = 1

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
    params.append(limit)

    rows = await conn.fetch(
        f"""
        SELECT
            t.issue_key, t.summary, t.status, t.priority,
            t.is_customer_originated, t.created_at, t.updated_at,
            t.request_type,
            o.name AS jira_org_name,
            u.display_name AS assignee_display_name
        FROM tickets t
        LEFT JOIN organizations o ON o.jira_org_id = t.jira_org_id
        LEFT JOIN jira_users u ON u.account_id = t.assignee_account_id
        WHERE {where}
        ORDER BY t.updated_at DESC
        LIMIT ${idx}
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


async def get_engineer_past_comments(
    conn: asyncpg.Connection,
    account_id: str,
    summary_pattern: str,
    limit: int = 5,
    min_body_length: int = 50,
    max_body_length: int = 500,
) -> list[dict]:
    """
    Pull the engineer's recent public close-out comments on tickets whose
    summary matches the given ILIKE pattern. Used as few-shot examples.
    """
    rows = await conn.fetch(
        """
        SELECT te.body, te.created_at, t.summary, t.issue_key
        FROM thread_events te
        JOIN tickets t ON t.issue_key = te.issue_key
        WHERE te.author_account_id = $1
          AND t.summary ILIKE $2
          AND te.is_public = true
          AND te.kind = 'comment'
          AND length(te.body) >= $3
          AND length(te.body) <= $4
          AND te.deleted_at IS NULL
          AND t.deleted_at IS NULL
        ORDER BY te.created_at DESC
        LIMIT $5
        """,
        account_id,
        summary_pattern,
        min_body_length,
        max_body_length,
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
             system_prompt, user_prompt, generated_text)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        RETURNING id
        """,
        draft["issue_key"],
        draft["pattern_slug"],
        draft.get("engineer_account_id"),
        draft.get("prompt_tokens"),
        draft.get("completion_tokens"),
        draft.get("model"),
        draft.get("system_prompt"),
        draft.get("user_prompt"),
        draft["generated_text"],
    )
    return row["id"]


async def mark_draft_used(conn: asyncpg.Connection, draft_id: int) -> None:
    await conn.execute(
        "UPDATE ops.draft_log SET was_used = true WHERE id = $1",
        draft_id,
    )
