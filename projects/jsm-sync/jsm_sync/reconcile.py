"""
Reconcile — weekly full-list diff to catch soft-deletes.

Fetches all current issue keys from Jira (no lookback), compares against
Postgres, and sets deleted_at on any rows that no longer exist in Jira.

Status: stub for v1. Not called automatically; run manually when needed.

Worklogs: v1 reconcile does not cascade-soft-delete `ticket_worklogs` for removed
tickets; orphan worklog rows are unlikely in practice (ticket FK CASCADE on hard
delete). A follow-up pass can be added later if needed.

Usage:
    python -m jsm_sync.reconcile
"""

import asyncio
import logging

import httpx

from .config import settings
from .db import close_pool, get_pool, init_pool
from .jira_client import _auth_headers, _fetch_all_keys_jql, build_project_jql

logger = logging.getLogger(__name__)


async def run_reconcile() -> None:
    logger.info("Reconcile starting — fetching all current Jira keys for project %s", settings.jira_project)
    await init_pool()
    try:
        async with httpx.AsyncClient() as client:
            headers = _auth_headers()
            semaphore = asyncio.Semaphore(settings.jira_semaphore_limit)
            jql = build_project_jql(settings.jira_project)
            jira_keys = set(await _fetch_all_keys_jql(client, jql, semaphore, headers))

        logger.info("Jira returned %d total keys", len(jira_keys))

        pool = await get_pool()
        pg_rows = await pool.fetch(
            "SELECT issue_key FROM tickets WHERE deleted_at IS NULL"
        )
        pg_keys = {r["issue_key"] for r in pg_rows}

        to_delete = pg_keys - jira_keys
        if not to_delete:
            logger.info("No deleted tickets detected — Postgres is clean")
            return

        logger.warning(
            "%d tickets in Postgres not found in Jira — soft-deleting: %s",
            len(to_delete),
            sorted(to_delete)[:20],
        )
        await pool.execute(
            "UPDATE tickets SET deleted_at = NOW() WHERE issue_key = ANY($1::text[])",
            list(to_delete),
        )
        logger.info("Reconcile complete — %d rows soft-deleted", len(to_delete))

    finally:
        await close_pool()


def main() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    )
    asyncio.run(run_reconcile())


if __name__ == "__main__":
    main()
