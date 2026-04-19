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

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from datetime import datetime, timedelta, timezone

import httpx
from rich.console import Console

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
from .progress import SyncProgress, install_rich_logging
from .transform import transform_ticket
from .worklog_sync import run_worklog_sweep

logger = logging.getLogger(__name__)

SOURCE_NAME = "jira_tickets"
BATCH_SIZE = 50
CURSOR_SLOP = timedelta(minutes=1)


async def run_incremental(*, no_worklogs: bool = False, console: Console | None = None) -> None:
    con = console or Console()

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

            with SyncProgress("Incremental sync", console=con) as p:
                scout_task = p.add_task("Scouting updated tickets", total=None)
                all_keys = await _fetch_all_keys_jql(client, jql, semaphore, headers)
                p.update(scout_task, total=len(all_keys), completed=len(all_keys))
                logger.info("Scout found %d tickets since last cursor", len(all_keys))

                max_updated: datetime | None = None

                if all_keys:
                    process_task = p.add_task(
                        f"Processing {len(all_keys):,} tickets",
                        total=len(all_keys),
                    )

                    for i in range(0, len(all_keys), BATCH_SIZE):
                        batch = all_keys[i : i + BATCH_SIZE]
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

                    final_cursor = (max_updated or cursor) + CURSOR_SLOP
                    await set_sync_cursor(SOURCE_NAME, final_cursor, status="running")
                    logger.info(
                        "Ticket cursor advanced to %s",
                        final_cursor.isoformat(),
                    )
                else:
                    logger.info("No updated tickets in JQL window")

                if not no_worklogs:
                    logger.info("Starting global worklog sweep (Phase B)")
                    sweep_task = p.add_task("Worklog sweep", total=None)
                    try:
                        touched = await run_worklog_sweep(
                            client,
                            semaphore,
                            headers,
                            progress=p,
                            task_id=sweep_task,
                        )
                        logger.info(
                            "Global worklog sweep complete — %d entries touched",
                            touched,
                        )
                    except Exception:
                        logger.exception(
                            "Worklog sweep failed — ticket sync already committed"
                        )

        await mark_sync_complete(SOURCE_NAME)
        logger.info("Incremental sync complete")

    except Exception:
        logger.exception("Incremental sync failed")
        await mark_sync_error(SOURCE_NAME, "Incremental sync failed — see logs")
        raise
    finally:
        await close_pool()


async def _embed_pending() -> None:
    """
    Embed any tickets that are missing/stale for our current model.
    Opens its own short-lived pool (with pgvector codec registered) to keep
    the main sync pool free of vector-typed concerns.
    """
    import asyncpg

    from .embed_db import (
        fetch_text_for_issue_keys,
        list_issue_keys_needing_embedding,
        register_pgvector,
        upsert_embeddings,
    )
    from .embedder import MODEL_NAME, build_embed_text, embed_texts, text_hash

    pool = await asyncpg.create_pool(
        dsn=settings.database_url,
        min_size=1,
        max_size=2,
        command_timeout=120,
        init=register_pgvector,
    )
    try:
        async with pool.acquire() as conn:
            keys = await list_issue_keys_needing_embedding(conn, MODEL_NAME)
        if not keys:
            logger.info("Embedding catch-up: nothing to do")
            return
        logger.info("Embedding catch-up: %d ticket(s) need embedding", len(keys))

        BATCH = 64
        for start in range(0, len(keys), BATCH):
            batch_keys = keys[start : start + BATCH]
            async with pool.acquire() as conn:
                rows = await fetch_text_for_issue_keys(conn, batch_keys)
            texts = [build_embed_text(s, d) for (_, s, d) in rows]
            vectors = embed_texts(texts, batch_size=BATCH)
            write_rows = [
                (rows[i][0], text_hash(texts[i]), vectors[i])
                for i in range(len(rows))
            ]
            async with pool.acquire() as conn:
                await upsert_embeddings(conn, write_rows)
        logger.info("Embedding catch-up complete (%d tickets)", len(keys))
    finally:
        await pool.close()


def main() -> None:
    p = argparse.ArgumentParser(description="Incremental APTUM JSM ticket sync")
    p.add_argument(
        "--no-worklogs",
        action="store_true",
        help="Skip per-ticket worklogs and the global worklog sweep",
    )
    args = p.parse_args()

    console = install_rich_logging(settings.log_level)

    async def _runner() -> None:
        await run_incremental(no_worklogs=args.no_worklogs, console=console)
        try:
            await _embed_pending()
        except Exception:
            logger.exception("Embedding catch-up failed (non-fatal)")

    asyncio.run(_runner())


if __name__ == "__main__":
    main()
