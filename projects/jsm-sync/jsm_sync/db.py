"""
asyncpg connection pool + upsert helpers for all jsm-sync tables.

Design:
  - Single module-level pool, initialized once via init_pool().
  - persist_ticket() wraps all table upserts in one transaction per ticket.
  - All writes are idempotent (ON CONFLICT DO UPDATE).
  - synced_at is always NOW() on upsert.
  - tickets upsert is guarded by updated_at to avoid unnecessary writes.
"""

import logging
from datetime import datetime, timezone
from typing import Optional

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
            jira_org_id, ocean_client_id, labels,
            sla_first_response_breached, sla_first_response_elapsed_s,
            sla_first_response_threshold_s,
            sla_resolution_breached, sla_resolution_elapsed_s,
            sla_resolution_threshold_s,
            created_at, updated_at, resolved_at, synced_at
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14,
            $15, $16, $17, $18, $19, $20, $21, $22, $23, NOW()
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


# ---------------------------------------------------------------------------
# Sync state helpers
# ---------------------------------------------------------------------------

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
