"""
asyncpg connection pool + upsert helpers for all jsm-sync tables.

Design:
  - Single module-level pool, initialized once via init_pool().
  - persist_ticket() wraps all table upserts in one transaction per ticket.
  - All writes are idempotent (ON CONFLICT DO UPDATE).
  - synced_at is always NOW() on upsert.
  - tickets upsert is guarded by updated_at to avoid unnecessary writes.
"""

import json
import logging
from datetime import datetime, timezone
from typing import Any, Optional

import asyncpg

from .config import settings
from .transform import TransformedTicket

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
        command_timeout=60,
    )
    logger.info("asyncpg pool initialized → %s", settings.database_url)


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
        logger.info("asyncpg pool closed")


async def get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("Pool not initialized — call await init_pool() first")
    return _pool


# ---------------------------------------------------------------------------
# Per-table upserts (take a connection, not the pool, for transaction use)
# ---------------------------------------------------------------------------

async def upsert_user(conn: asyncpg.Connection, user: dict) -> None:
    await conn.execute(
        """
        INSERT INTO jira_users (account_id, display_name, email, role, account_type,
                                first_seen_at, last_seen_at)
        VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
        ON CONFLICT (account_id) DO UPDATE SET
            display_name  = EXCLUDED.display_name,
            email         = EXCLUDED.email,
            role          = EXCLUDED.role,
            account_type  = EXCLUDED.account_type,
            last_seen_at  = NOW()
        """,
        user["account_id"],
        user.get("display_name", ""),
        user.get("email"),
        user.get("role", "Unknown"),
        user.get("account_type"),
    )


async def upsert_organization(conn: asyncpg.Connection, org: dict) -> None:
    await conn.execute(
        """
        INSERT INTO organizations (jira_org_id, name, ocean_client_id,
                                   first_seen_at, last_seen_at)
        VALUES ($1, $2, $3, NOW(), NOW())
        ON CONFLICT (jira_org_id) DO UPDATE SET
            name            = EXCLUDED.name,
            ocean_client_id = COALESCE(EXCLUDED.ocean_client_id,
                                       organizations.ocean_client_id),
            last_seen_at    = NOW()
        """,
        org["jira_org_id"],
        org.get("name", org["jira_org_id"]),
        org.get("ocean_client_id"),
    )


async def upsert_ticket(conn: asyncpg.Connection, row: dict) -> None:
    await conn.execute(
        """
        INSERT INTO tickets (
            issue_key, summary, description, status, priority, issue_type,
            request_type, is_customer_originated,
            creator_account_id, reporter_account_id, assignee_account_id,
            jira_org_id, ocean_client_id, labels, issue_id,
            sla_first_response_breached, sla_first_response_elapsed_s,
            sla_first_response_threshold_s,
            sla_resolution_breached, sla_resolution_elapsed_s,
            sla_resolution_threshold_s,
            created_at, updated_at, resolved_at, synced_at
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15,
            $16, $17, $18, $19, $20, $21, $22, $23, $24, NOW()
        )
        ON CONFLICT (issue_key) DO UPDATE SET
            summary                       = EXCLUDED.summary,
            description                   = EXCLUDED.description,
            status                        = EXCLUDED.status,
            priority                      = EXCLUDED.priority,
            issue_type                    = EXCLUDED.issue_type,
            request_type                  = EXCLUDED.request_type,
            is_customer_originated        = EXCLUDED.is_customer_originated,
            creator_account_id            = EXCLUDED.creator_account_id,
            reporter_account_id           = EXCLUDED.reporter_account_id,
            assignee_account_id           = EXCLUDED.assignee_account_id,
            jira_org_id                   = EXCLUDED.jira_org_id,
            ocean_client_id               = EXCLUDED.ocean_client_id,
            labels                        = EXCLUDED.labels,
            issue_id                      = COALESCE(EXCLUDED.issue_id, tickets.issue_id),
            sla_first_response_breached   = EXCLUDED.sla_first_response_breached,
            sla_first_response_elapsed_s  = EXCLUDED.sla_first_response_elapsed_s,
            sla_first_response_threshold_s = EXCLUDED.sla_first_response_threshold_s,
            sla_resolution_breached       = EXCLUDED.sla_resolution_breached,
            sla_resolution_elapsed_s      = EXCLUDED.sla_resolution_elapsed_s,
            sla_resolution_threshold_s    = EXCLUDED.sla_resolution_threshold_s,
            updated_at                    = EXCLUDED.updated_at,
            resolved_at                   = EXCLUDED.resolved_at,
            synced_at                     = NOW(),
            deleted_at                    = NULL
        WHERE tickets.updated_at <= EXCLUDED.updated_at
        """,
        row["issue_key"],
        row["summary"],
        row.get("description", ""),
        row["status"],
        row.get("priority"),
        row.get("issue_type"),
        row.get("request_type"),
        row.get("is_customer_originated", False),
        row.get("creator_account_id"),
        row.get("reporter_account_id"),
        row.get("assignee_account_id"),
        row.get("jira_org_id"),
        row.get("ocean_client_id"),
        row.get("labels", []),
        row.get("issue_id"),
        row.get("sla_first_response_breached"),
        row.get("sla_first_response_elapsed_s"),
        row.get("sla_first_response_threshold_s"),
        row.get("sla_resolution_breached"),
        row.get("sla_resolution_elapsed_s"),
        row.get("sla_resolution_threshold_s"),
        row["created_at"],
        row["updated_at"],
        row.get("resolved_at"),
    )


def _jsonb_or_none(val: Any) -> str | None:
    if val is None:
        return None
    return json.dumps(val)


async def upsert_worklogs(
    conn: asyncpg.Connection,
    worklogs: list[dict],
) -> None:
    if not worklogs:
        return
    await conn.executemany(
        """
        INSERT INTO ticket_worklogs (
            worklog_id, issue_key, issue_id, author_account_id,
            time_spent_seconds, started_at, comment_adf, visibility,
            jira_created_at, jira_updated_at, synced_at, deleted_at
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7::jsonb, $8::jsonb, $9, $10, NOW(), NULL)
        ON CONFLICT (worklog_id) DO UPDATE SET
            issue_key          = EXCLUDED.issue_key,
            issue_id           = EXCLUDED.issue_id,
            author_account_id  = EXCLUDED.author_account_id,
            time_spent_seconds = EXCLUDED.time_spent_seconds,
            started_at         = EXCLUDED.started_at,
            comment_adf        = EXCLUDED.comment_adf,
            visibility         = EXCLUDED.visibility,
            jira_created_at    = EXCLUDED.jira_created_at,
            jira_updated_at    = EXCLUDED.jira_updated_at,
            synced_at          = NOW(),
            deleted_at         = NULL
        """,
        [
            (
                w["worklog_id"],
                w["issue_key"],
                w["issue_id"],
                w.get("author_account_id"),
                w["time_spent_seconds"],
                w["started_at"],
                _jsonb_or_none(w.get("comment_adf")),
                _jsonb_or_none(w.get("visibility")),
                w["jira_created_at"],
                w["jira_updated_at"],
            )
            for w in worklogs
        ],
    )


async def soft_delete_missing_worklogs(
    conn: asyncpg.Connection,
    issue_key: str,
    present_worklog_ids: list[int],
) -> int:
    """
    For per-ticket sync mode (Phase A): mark any DB worklogs for this issue_key
    that were NOT in the latest Jira response as deleted. Returns count.
    """
    n = await conn.fetchval(
        """
        WITH deleted AS (
            UPDATE ticket_worklogs
            SET deleted_at = NOW(), synced_at = NOW()
            WHERE issue_key = $1
              AND deleted_at IS NULL
              AND NOT (worklog_id = ANY($2::bigint[]))
            RETURNING 1
        )
        SELECT COUNT(*)::bigint FROM deleted
        """,
        issue_key,
        present_worklog_ids or [],
    )
    return int(n or 0)


async def soft_delete_worklogs_by_id(
    conn: asyncpg.Connection,
    worklog_ids: list[int],
) -> int:
    """For global sweep: mark specific worklog IDs deleted."""
    if not worklog_ids:
        return 0
    n = await conn.fetchval(
        """
        WITH deleted AS (
            UPDATE ticket_worklogs
            SET deleted_at = NOW(), synced_at = NOW()
            WHERE worklog_id = ANY($1::bigint[])
              AND deleted_at IS NULL
            RETURNING 1
        )
        SELECT COUNT(*)::bigint FROM deleted
        """,
        worklog_ids,
    )
    return int(n or 0)


async def map_issue_ids_to_keys(
    conn: asyncpg.Connection,
    issue_ids: list[int],
) -> dict[int, str]:
    """For global worklog sweep: filter worklogs to our project by resolving issueId→issueKey."""
    if not issue_ids:
        return {}
    rows = await conn.fetch(
        "SELECT issue_id, issue_key FROM tickets WHERE issue_id = ANY($1::bigint[])",
        issue_ids,
    )
    return {int(r["issue_id"]): r["issue_key"] for r in rows}


async def upsert_thread_events(
    conn: asyncpg.Connection,
    issue_key: str,
    events: list[dict],
) -> None:
    if not events:
        return
    await conn.executemany(
        """
        INSERT INTO thread_events
            (id, issue_key, kind, author_account_id, is_public, body, created_at, synced_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, NOW())
        ON CONFLICT (id) DO UPDATE SET
            is_public         = EXCLUDED.is_public,
            body              = EXCLUDED.body,
            author_account_id = EXCLUDED.author_account_id,
            synced_at         = NOW(),
            deleted_at        = NULL
        """,
        [
            (
                e["id"],
                issue_key,
                e.get("kind", "comment"),
                e.get("author_account_id"),
                e.get("is_public"),
                e.get("body", ""),
                e["created_at"],
            )
            for e in events
        ],
    )


async def upsert_assets(conn: asyncpg.Connection, assets: list[dict]) -> None:
    if not assets:
        return
    await conn.executemany(
        """
        INSERT INTO assets (object_id, workspace_id, asset_name, service_id, last_hydrated_at)
        VALUES ($1, $2, $3, $4, NOW())
        ON CONFLICT (object_id) DO UPDATE SET
            workspace_id     = EXCLUDED.workspace_id,
            asset_name       = COALESCE(EXCLUDED.asset_name, assets.asset_name),
            service_id       = COALESCE(EXCLUDED.service_id, assets.service_id),
            last_hydrated_at = NOW()
        """,
        [
            (
                a["object_id"],
                a.get("workspace_id", ""),
                a.get("asset_name"),
                a.get("service_id"),
            )
            for a in assets
        ],
    )


async def upsert_ticket_asset_links(
    conn: asyncpg.Connection,
    links: list[tuple[str, str]],
) -> None:
    if not links:
        return
    await conn.executemany(
        """
        INSERT INTO ticket_assets (issue_key, object_id)
        VALUES ($1, $2)
        ON CONFLICT (issue_key, object_id) DO NOTHING
        """,
        links,
    )


# ---------------------------------------------------------------------------
# Transaction wrapper
# ---------------------------------------------------------------------------

async def persist_ticket(transformed: TransformedTicket) -> None:
    """Write one ticket and all related rows in a single transaction."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            for u in transformed.users:
                await upsert_user(conn, u)
            if transformed.organization:
                await upsert_organization(conn, transformed.organization)
            await upsert_ticket(conn, transformed.ticket_row)
            await upsert_thread_events(
                conn,
                transformed.ticket_row["issue_key"],
                transformed.thread_events,
            )
            await upsert_assets(conn, transformed.assets)
            await upsert_ticket_asset_links(conn, transformed.ticket_asset_links)

            await upsert_worklogs(conn, transformed.worklogs)
            present_ids = [w["worklog_id"] for w in transformed.worklogs]
            await soft_delete_missing_worklogs(
                conn,
                transformed.ticket_row["issue_key"],
                present_ids,
            )


# ---------------------------------------------------------------------------
# Sync state helpers
# ---------------------------------------------------------------------------


async def get_worklog_cursor_ms(source: str = "jira_worklogs") -> Optional[int]:
    """Return worklog cursor as epoch milliseconds (the format /worklog/updated wants)."""
    dt = await get_sync_cursor(source)
    if dt is None:
        return None
    return int(dt.timestamp() * 1000)


async def set_worklog_cursor_ms(since_ms: int, source: str = "jira_worklogs") -> None:
    dt = datetime.fromtimestamp(since_ms / 1000, tz=timezone.utc)
    await set_sync_cursor(source, dt, status="idle")


async def get_sync_cursor(source: str) -> Optional[datetime]:
    pool = await get_pool()
    row = await pool.fetchrow(
        "SELECT last_cursor FROM sync_state WHERE source = $1", source
    )
    if row and row["last_cursor"]:
        raw = row["last_cursor"]
        if isinstance(raw, datetime):
            return raw
        try:
            from dateutil import parser as dparser
            return dparser.parse(raw)
        except (ValueError, TypeError):
            return None
    return None


async def get_sync_status(source: str) -> Optional[str]:
    pool = await get_pool()
    row = await pool.fetchrow(
        "SELECT status FROM sync_state WHERE source = $1", source
    )
    return row["status"] if row else None


async def set_sync_cursor(
    source: str,
    cursor: datetime,
    status: str = "running",
) -> None:
    pool = await get_pool()
    await pool.execute(
        """
        UPDATE sync_state
        SET last_cursor = $1, status = $2, updated_at = NOW()
        WHERE source = $3
        """,
        cursor.isoformat(),
        status,
        source,
    )


async def mark_sync_running(source: str) -> None:
    pool = await get_pool()
    await pool.execute(
        """
        UPDATE sync_state
        SET status = 'running', updated_at = NOW()
        WHERE source = $1
        """,
        source,
    )


async def mark_sync_complete(source: str) -> None:
    pool = await get_pool()
    await pool.execute(
        """
        UPDATE sync_state
        SET status = 'completed', last_sync_at = NOW(), last_error = NULL, updated_at = NOW()
        WHERE source = $1
        """,
        source,
    )


async def mark_sync_error(source: str, error: str) -> None:
    pool = await get_pool()
    await pool.execute(
        """
        UPDATE sync_state
        SET status = 'error', last_error = $1, updated_at = NOW()
        WHERE source = $2
        """,
        error,
        source,
    )
