"""
Backfill APTUM tickets to Postgres.

Reads the sync cursor from sync_state to resume after a crash (ORDER BY updated ASC).
Checkpoints the cursor after each batch commit — safe to kill and restart.

Usage:
    python -m jsm_sync.backfill
    python -m jsm_sync.backfill --lookback-days 30
    python -m jsm_sync.backfill --lookback-days 30 --batch-size 20
"""

import argparse
import asyncio
import logging
from datetime import datetime, timezone

import httpx

from .config import settings
from .db import (
    close_pool,
    get_sync_cursor,
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
DEFAULT_BATCH_SIZE = 20


async def run_backfill(lookback_days: int, batch_size: int) -> None:
    await init_pool()
    try:
        cursor = await get_sync_cursor(SOURCE_NAME)

        if cursor:
            logger.info("Resuming backfill from cursor %s", cursor.isoformat())
            jql = build_project_jql(settings.jira_project, updated_since=cursor)
        else:
            logger.info("Starting fresh backfill — lookback %d days", lookback_days)
            jql = build_project_jql(settings.jira_project, lookback_days=lookback_days)

        # Mark as running. If cursor is None (fresh start), record now as the
        # starting point; actual checkpoints from batch max(updated_at) will
        # overwrite this immediately as processing begins.
        await set_sync_cursor(
            SOURCE_NAME,
            cursor or datetime.now(timezone.utc),
            status="running",
        )

        async with httpx.AsyncClient() as client:
            headers = _auth_headers()
            semaphore = asyncio.Semaphore(settings.jira_semaphore_limit)

            all_keys = await _fetch_all_keys_jql(client, jql, semaphore, headers)
            logger.info("Scout found %d tickets to process", len(all_keys))

            for i in range(0, len(all_keys), batch_size):
                batch = all_keys[i : i + batch_size]
                batch_num = i // batch_size + 1
                total_batches = (len(all_keys) + batch_size - 1) // batch_size
                logger.info(
                    "Batch %d/%d — keys %d-%d of %d",
                    batch_num,
                    total_batches,
                    i + 1,
                    min(i + batch_size, len(all_keys)),
                    len(all_keys),
                )

                tickets = await fetch_ticket_batch(client, batch, semaphore, headers)

                max_updated: datetime | None = None
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
                    logger.info("Checkpointed cursor at %s", max_updated.isoformat())

        await mark_sync_complete(SOURCE_NAME)
        logger.info("Backfill complete")

    except Exception:
        logger.exception("Backfill failed")
        await mark_sync_error(SOURCE_NAME, "Backfill failed — see logs")
        raise
    finally:
        await close_pool()


def main() -> None:
    p = argparse.ArgumentParser(description="Backfill APTUM JSM tickets into Postgres")
    p.add_argument(
        "--lookback-days",
        type=int,
        default=settings.jira_lookback_days,
        help="Days of history to pull on a fresh backfill (default: %(default)s)",
    )
    p.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help="Tickets per gather batch (default: %(default)s)",
    )
    args = p.parse_args()

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    )

    asyncio.run(run_backfill(args.lookback_days, args.batch_size))


if __name__ == "__main__":
    main()
