"""
Backfill APTUM tickets to Postgres.

Reads the sync cursor from sync_state to resume after a crash (ORDER BY updated ASC).
Checkpoints the cursor after each batch commit — safe to kill and restart.

Usage:
    python -m jsm_sync.backfill
    python -m jsm_sync.backfill --lookback-days 30
    python -m jsm_sync.backfill --lookback-days 30 --batch-size 20
"""

from __future__ import annotations

import argparse
import asyncio
import logging
from datetime import datetime, timezone

import httpx
from rich.console import Console

from .config import settings
from .db import (
    close_pool,
    get_sync_cursor,
    get_worklog_cursor_ms,
    init_pool,
    mark_sync_complete,
    mark_sync_error,
    mark_sync_running,
    persist_ticket,
    set_sync_cursor,
    set_worklog_cursor_ms,
)
from .jira_client import (
    _auth_headers,
    _fetch_all_keys_jql,
    build_project_jql,
    fetch_ticket_batch,
)
from .progress import SyncProgress, install_rich_logging
from .transform import transform_ticket
from .worklog_sync import WORKLOG_SOURCE, run_worklog_sweep

logger = logging.getLogger(__name__)

SOURCE_NAME = "jira_tickets"
DEFAULT_BATCH_SIZE = 50


async def run_backfill(
    lookback_days: int,
    batch_size: int,
    force_lookback: bool = False,
    *,
    no_worklogs: bool = False,
    console: Console | None = None,
) -> None:
    backfill_start_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    con = console or Console()

    await init_pool()
    try:
        cursor = await get_sync_cursor(SOURCE_NAME)

        if cursor and not force_lookback:
            logger.info("Resuming backfill from cursor %s", cursor.isoformat())
            jql = build_project_jql(settings.jira_project, updated_since=cursor)
        else:
            if force_lookback and cursor:
                logger.info(
                    "--lookback-days explicitly set — ignoring cursor %s",
                    cursor.isoformat(),
                )
            logger.info("Starting fresh backfill — lookback %d days", lookback_days)
            jql = build_project_jql(settings.jira_project, lookback_days=lookback_days)

        await mark_sync_running(SOURCE_NAME)

        async with httpx.AsyncClient() as client:
            headers = _auth_headers()
            semaphore = asyncio.Semaphore(settings.jira_semaphore_limit)

            with SyncProgress("Backfill", console=con) as p:
                scout_task = p.add_task("Scouting ticket keys", total=None)
                all_keys = await _fetch_all_keys_jql(client, jql, semaphore, headers)
                p.update(scout_task, total=len(all_keys), completed=len(all_keys))
                logger.info("Scout found %d tickets to process", len(all_keys))

                process_task = p.add_task(
                    f"Fetching & persisting {len(all_keys):,} tickets",
                    total=len(all_keys),
                )

                max_updated: datetime | None = None
                for i in range(0, len(all_keys), batch_size):
                    batch = all_keys[i : i + batch_size]
                    tickets = await fetch_ticket_batch(
                        client,
                        batch,
                        semaphore,
                        headers,
                        include_worklogs=not no_worklogs,
                    )

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

                    p.advance(process_task, len(batch))

                    if max_updated:
                        await set_sync_cursor(SOURCE_NAME, max_updated, status="running")
                        logger.info("Checkpointed cursor at %s", max_updated.isoformat())

                if not no_worklogs:
                    existing_cursor = await get_worklog_cursor_ms(WORKLOG_SOURCE)
                    if existing_cursor is None:
                        await set_worklog_cursor_ms(backfill_start_ms, WORKLOG_SOURCE)
                        logger.info(
                            "Pinned initial worklog cursor to backfill start: %d",
                            backfill_start_ms,
                        )
                    else:
                        sweep_task = p.add_task("Worklog top-up sweep", total=None)
                        try:
                            await run_worklog_sweep(
                                client,
                                semaphore,
                                headers,
                                progress=p,
                                task_id=sweep_task,
                            )
                        except Exception:
                            logger.exception(
                                "Worklog top-up sweep failed — ticket backfill already checkpointed"
                            )

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
        default=None,
        help="Days of history to pull — overrides resume cursor when explicitly set",
    )
    p.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help="Tickets per gather batch (default: %(default)s)",
    )
    p.add_argument(
        "--no-worklogs",
        action="store_true",
        help="Skip worklog fetching (faster backfill, but ticket_worklogs will be stale)",
    )
    args = p.parse_args()

    console = install_rich_logging(settings.log_level)

    force_lookback = args.lookback_days is not None
    lookback_days = args.lookback_days if force_lookback else settings.jira_lookback_days
    asyncio.run(
        run_backfill(
            lookback_days,
            args.batch_size,
            force_lookback=force_lookback,
            no_worklogs=args.no_worklogs,
            console=console,
        )
    )


if __name__ == "__main__":
    main()
