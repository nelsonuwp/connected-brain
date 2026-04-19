"""
Global worklog sweep using /rest/api/3/worklog/updated and /worklog/deleted.

Called AFTER the main ticket sweep in both backfill.py and incremental.py to
catch worklog changes on tickets whose issue.updated did not move.

Independent cursor: sync_state.source = 'jira_worklogs'.
Cursor is epoch-ms (stored as ISO in sync_state.last_cursor).
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Optional

import httpx

from .db import (
    get_pool,
    get_worklog_cursor_ms,
    map_issue_ids_to_keys,
    set_worklog_cursor_ms,
    soft_delete_worklogs_by_id,
    upsert_user,
    upsert_worklogs,
)
from .jira_client import (
    determine_role,
    fetch_worklog_deletes_since,
    fetch_worklog_updates_since,
    fetch_worklogs_bulk,
)
from .transform import parse_iso

logger = logging.getLogger(__name__)
WORKLOG_SOURCE = "jira_worklogs"


async def run_worklog_sweep(
    client: httpx.AsyncClient,
    semaphore: Any,
    headers: dict,
    initial_cursor_ms: int | None = None,
    progress: Any | None = None,
    task_id: Any | None = None,
) -> int:
    """
    Sweep /worklog/updated and /worklog/deleted since the stored cursor,
    upsert/soft-delete in DB, advance the cursor. Returns count of worklogs touched.

    If initial_cursor_ms is provided AND no stored cursor exists, use it
    (used by backfill's first run to pin the cursor to "backfill started at").
    """
    cursor_ms = await get_worklog_cursor_ms(WORKLOG_SOURCE)
    if cursor_ms is None:
        if initial_cursor_ms is None:
            logger.warning("No worklog cursor and no initial provided. Skipping sweep.")
            return 0
        cursor_ms = initial_cursor_ms

    logger.info(
        "Worklog sweep since %d (%s)",
        cursor_ms,
        datetime.fromtimestamp(cursor_ms / 1000, tz=timezone.utc).isoformat(),
    )

    updated_ids, until_updated = await fetch_worklog_updates_since(
        client, cursor_ms, semaphore, headers
    )
    deleted_ids, until_deleted = await fetch_worklog_deletes_since(
        client, cursor_ms, semaphore, headers
    )
    logger.info(
        "Jira reported %d updated, %d deleted worklogs",
        len(updated_ids),
        len(deleted_ids),
    )

    touched = 0

    if progress is not None and task_id is not None and (updated_ids or deleted_ids):
        progress.update(task_id, total=len(updated_ids) + len(deleted_ids))

    batch_size = 1000
    if updated_ids:
        pool = await get_pool()
        for i in range(0, len(updated_ids), batch_size):
            chunk = updated_ids[i : i + batch_size]
            full = await fetch_worklogs_bulk(client, chunk, semaphore, headers)

            async with pool.acquire() as conn:
                issue_ids_seen = list({int(w["issueId"]) for w in full if w.get("issueId")})
                id_to_key = await map_issue_ids_to_keys(conn, issue_ids_seen)

            relevant = [w for w in full if w.get("issueId") and int(w["issueId"]) in id_to_key]
            logger.info(
                "Chunk %d-%d: fetched %d, %d belong to tickets we track",
                i,
                min(i + batch_size, len(updated_ids)),
                len(full),
                len(relevant),
            )

            rows: list[dict] = []
            authors_by_id: dict[str, dict] = {}
            for w in relevant:
                issue_id = int(w["issueId"])
                issue_key = id_to_key[issue_id]
                author = w.get("author") or {}
                aid = author.get("accountId")
                if aid:
                    authors_by_id[aid] = {
                        "account_id": aid,
                        "display_name": author.get("displayName") or "",
                        "email": author.get("emailAddress"),
                        "role": determine_role(author),
                        "account_type": author.get("accountType"),
                    }
                jira_created = parse_iso(w.get("created")) or parse_iso(w.get("started"))
                jira_updated = parse_iso(w.get("updated")) or jira_created
                started_at = parse_iso(w.get("started")) or jira_created
                if jira_created is None or jira_updated is None or started_at is None:
                    continue
                rows.append(
                    {
                        "worklog_id": int(w["id"]),
                        "issue_key": issue_key,
                        "issue_id": issue_id,
                        "author_account_id": aid,
                        "time_spent_seconds": int(w.get("timeSpentSeconds") or 0),
                        "started_at": started_at,
                        "comment_adf": w.get("comment"),
                        "visibility": w.get("visibility"),
                        "jira_created_at": jira_created,
                        "jira_updated_at": jira_updated,
                    }
                )

            async with pool.acquire() as conn:
                async with conn.transaction():
                    for u in authors_by_id.values():
                        await upsert_user(conn, u)
                    await upsert_worklogs(conn, rows)

            touched += len(rows)
            if progress is not None and task_id is not None:
                progress.advance(task_id, len(chunk))

    if deleted_ids:
        pool = await get_pool()
        async with pool.acquire() as conn:
            n = await soft_delete_worklogs_by_id(conn, deleted_ids)
        logger.info("Soft-deleted %d worklogs", n)
        touched += n
        if progress is not None and task_id is not None:
            progress.advance(task_id, len(deleted_ids))

    next_cursor = min(until_updated, until_deleted)
    await set_worklog_cursor_ms(next_cursor, WORKLOG_SOURCE)
    logger.info("Worklog cursor advanced to %d", next_cursor)

    return touched
