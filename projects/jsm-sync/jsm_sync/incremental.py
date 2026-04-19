"""
Incremental sync — always cursor-driven, designed to run on a cron every ~10 minutes.

Safety rules:
  - Exits with a warning if sync_state.status == 'running' (another instance active).
  - Exits with an error if cursor is NULL — run backfill.py first.
  - Advances cursor to max(updated_at) + 1 minute after a successful run
    (the slop handles Jira eventual consistency on updated_at).

Cron example:
    */10 * * * * cd /path/to/jsm-sync && .venv/bin/python -m jsm_sync.incremental >> logs/incremental.log 2>&1
"""

import asyncio
import logging
import sys
from datetime import datetime, timedelta, timezone

import httpx

from .config import settings
from .db import (
    close_pool,
    get_sync_cursor,
    get_sync_status,
    init_pool,
    mark_sync_complete,
    mark_sync_error,
    persist_ticket,
    set_sync_cursor,
)
from .jira_client import (
    _auth_headers,
    _fetch_all_keys_jql,
    build_project_jql,
    fetch_ticket_batch,
)
from .transform import transform_ticket

logger = logging.getLogger(__name__)

SOURCE_NAME = "jira_tickets"
BATCH_SIZE = 50
CURSOR_SLOP = timedelta(minutes=1)


async def run_incremental() -> None:
    await init_pool()
    try:
        status = await get_sync_status(SOURCE_NAME)
        if status == "running":
            logger.warning(
                "sync_state.status is 'running' — another instance may be active. Exiting."
            )
            return

        cursor = await get_sync_cursor(SOURCE_NAME)
        if cursor is None:
            logger.error(
                "No cursor found in sync_state. Run 'python -m jsm_sync.backfill' first."
            )
            sys.exit(1)

        logger.info("Incremental sync from cursor %s", cursor.isoformat())
        jql = build_project_jql(settings.jira_project, updated_since=cursor)

        await set_sync_cursor(SOURCE_NAME, cursor, status="running")

        async with httpx.AsyncClient() as client:
            headers = _auth_headers()
            semaphore = asyncio.Semaphore(settings.jira_semaphore_limit)

            all_keys = await _fetch_all_keys_jql(client, jql, semaphore, headers)
            logger.info("Scout found %d tickets since last cursor", len(all_keys))

            if not all_keys:
                await mark_sync_complete(SOURCE_NAME)
                logger.info("No new tickets — incremental sync complete")
                return

            max_updated: datetime | None = None

            for i in range(0, len(all_keys), BATCH_SIZE):
                batch = all_keys[i : i + BATCH_SIZE]
                logger.info(
                    "Batch %d — keys %d-%d of %d",
                    i // BATCH_SIZE + 1,
                    i + 1,
                    min(i + BATCH_SIZE, len(all_keys)),
                    len(all_keys),
                )

                tickets = await fetch_ticket_batch(client, batch, semaphore, headers)

                for ticket in tickets:
                    try:
                        transformed = transform_ticket(ticket)
                        await persist_ticket(transformed)
                        ticket_updated = ticket.get("updated_at")
                        if ticket_updated and (
                            max_updated is None or ticket_updated > max_updated
                        ):
                            max_updated = ticket_updated
                    except Exception:
                        logger.error(
                            "Failed to persist %s",
                            ticket.get("issue_key", "?"),
                            exc_info=True,
                        )

                if max_updated:
                    await set_sync_cursor(SOURCE_NAME, max_updated, status="running")

        # Advance cursor by slop to handle Jira eventual consistency
        final_cursor = (max_updated or cursor) + CURSOR_SLOP
        await set_sync_cursor(SOURCE_NAME, final_cursor, status="running")
        await mark_sync_complete(SOURCE_NAME)
        logger.info(
            "Incremental sync complete — cursor advanced to %s",
            final_cursor.isoformat(),
        )

    except Exception:
        logger.exception("Incremental sync failed")
        await mark_sync_error(SOURCE_NAME, "Incremental sync failed — see logs")
        raise
    finally:
        await close_pool()


def main() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    )
    asyncio.run(run_incremental())


if __name__ == "__main__":
    main()
