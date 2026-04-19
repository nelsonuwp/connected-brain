# Worklog Sync — Implementation Plan

**Scope:** Extend jsm-sync to persist Jira worklogs (per-entry) into Postgres during both backfill and incremental runs. No separate cron job — worklog sync is folded into the existing launchd-driven pipeline.

**Handoff target:** Composer 2. Execute tasks in order. Each task has acceptance criteria. Do not skip ahead.

---

## 1. Design summary (locked)

| Decision | Choice |
|---|---|
| Storage grain | Normalized per-entry table `ticket_worklogs`. One row per Jira worklog entry. |
| Worklog comment body | Raw ADF as `jsonb` (field: `comment_adf`). Preserves formatting; no ADF parsing on write. |
| Incremental mechanism | Global `/rest/api/3/worklog/updated?since=<epoch-ms>` + `/rest/api/3/worklog/list` bulk fetch, plus `/rest/api/3/worklog/deleted?since=<epoch-ms>` for deletes. Independent cursor from ticket sync. |
| Deletes | Soft-delete via `deleted_at` column, driven by `/worklog/deleted` sweep. |
| Default behavior | Backfill and incremental BOTH sync worklogs by default. Opt-out via `--no-worklogs` flag only. |
| Embedding impact | None in this plan. Worklog comments are not embedded. |

### Why a second cursor

A ticket's `updated` does not reliably bump when a worklog is edited or deleted. It also bumps for reasons unrelated to work logged (automation, comment edits, field changes). Using `/worklog/updated` as the source of truth for worklog changes is decoupled from ticket activity — required by the user's stated concern that "just because a ticket is updated it doesn't mean that time was entered."

### Why `issue_id` must be added to `tickets`

`/worklog/updated` → `/worklog/list` returns worklog entries keyed by numeric `issueId`, **not** `issueKey`. Our current `tickets` table has no way to map `issueId → issueKey` without a round-trip to Jira per worklog. Adding `issue_id BIGINT UNIQUE` to `tickets` solves this with one column. Populated on every issue fetch; old rows get it on next sync touch.

### Why backfill still does per-ticket `/issue/{key}/worklog`

For the initial historical load (~600 days, ~55k tickets), calling `/worklog/updated?since=0` would return every worklog across the entire Jira instance — including non-APTUM projects and pre-history data. Filtering by our issueId set works but has no pagination guarantees for that volume. The per-ticket fetch during backfill is bounded, parallelizable under the existing semaphore, and gives us a deterministic "DB fully in sync with Jira for these tickets" checkpoint. Once backfill completes, the worklog cursor is set to backfill start time, and incremental takes over using the global sweep endpoints.

---

## 2. Jira API — validated against official docs

Validated against https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-worklogs/ on 2026-04-19. Endpoint shapes below are confirmed; code in Section 4 reflects them.

### 2.1 `GET /rest/api/3/issue/{issueIdOrKey}/worklog`
- Paginated via `startAt` / `maxResults` / `total`. Use `maxResults=100` (doc-max is instance-configurable; 100 is safe).
- Returns `PageOfWorklogs`: `{startAt, maxResults, total, worklogs[]}`.
- Each `worklogs[i]` has: `id` (string, numeric), `issueId` (string, numeric), `author` (full user object with accountId/displayName/emailAddress/accountType), `started` (ISO 8601), `timeSpent` (human), `timeSpentSeconds` (int), `updateAuthor`, `updated` (ISO), `comment` (ADF doc or absent), `visibility` (`{identifier, type, value}` or absent), `self` (URL).
- **`created` field**: shown in the Add Worklog (POST) 201 response schema but **NOT in the GET response example**. Treat `created` as optional; if absent, fall back to `started` for `jira_created_at`. Code in Task 5 must tolerate both.
- The existing `_fetch_worklog` in `jira_client.py` does NOT paginate — **this is a latent bug**; tickets with >20 worklogs would be silently truncated. Task 3 replaces it.

### 2.2 `GET /rest/api/3/worklog/updated?since=<epoch-ms>`
- Returns `ChangedWorklogs`: `{since, until, lastPage, nextPage, self, values[]}`.
- `values[i]` = `{worklogId: int, updatedTime: epoch-ms, properties: []}`. We only need `worklogId`.
- **1000 items per page.** If `lastPage=false`, fetch next page with `?since=<until>` (equivalent to the `nextPage` URL Jira provides).
- **1-minute lag gotcha**: "This resource does not return worklogs updated during the minute preceding the request." Acceptable — the launchd-driven incremental runs on a cadence longer than 1 minute, and the cursor only advances to `until`, which is already clamped by Jira to ≥60s ago. Document in README.
- `since` is required epoch-ms.

### 2.3 `GET /rest/api/3/worklog/deleted?since=<epoch-ms>`
- Same response shape and same pagination semantics as `/updated`.
- Same 1-minute lag.

### 2.4 `POST /rest/api/3/worklog/list`
- Request body: `{ids: array<integer>}`. **Hard limit of 1000 IDs per call** — batch accordingly.
- Response: `array<Worklog>` (the same Worklog object shape described in 2.1).
- **Visibility gotcha**: "worklogs are only returned where... the worklog is set as _Viewable by All Users_, or the user is a member of a project role or group with permission to view the worklog." A group-restricted worklog can therefore be silently omitted from the response if the API user isn't in the allowed group. Our API token has admin scope, so we expect full visibility; if a future audit shows missing rows, check token permissions first.

### 2.5 Implications for the plan

- **Timestamps in milliseconds** — `since` and `until` are epoch-ms, not seconds. Existing `sync_state.last_cursor` stores ISO datetimes, so helpers in `db.py` must convert: `int(dt.timestamp() * 1000)` on read, `datetime.fromtimestamp(ms/1000, tz=UTC)` on write.
- **Cursor advancement** — advance to `until` from the last page of `/updated`. Do NOT advance past `until` manually. Since Jira already trims worklogs newer than ~60s ago, `until` is safe to use directly.
- **Hard-delete detection for per-ticket Phase A** — `/issue/{key}/worklog` does not flag deletes; it just omits the row. The diff-based `soft_delete_missing_worklogs` in Task 6 is therefore the correct approach for per-ticket mode.

### 2.6 Live validation (write-cycle smoke test, 2026-04-19)

Every detection path was verified end-to-end against production Jira (APTUM-1) before codification. Test worklog id `211705` was created, edited (60s → 120s), and deleted. All four detection paths fired correctly:

| Event | Path | Result |
|---|---|---|
| Create | Path A (`/issue/{key}/worklog`) — immediate | ✅ |
| Create | Path B (`/worklog/updated`) — after 65s lag | ✅ |
| Edit   | Path B (`updatedTime` bumps) | ✅ advanced by ~66s |
| Delete | Path A (diff against DB set) — immediate | ✅ |
| Delete | Path B (`/worklog/deleted`) — after 65s lag | ✅ |

APTUM-1 was returned to its pre-test state (1 pre-existing worklog, no leftover). The two smoke scripts — `scripts/_smoke_worklog_observe.py` (read-only, no side effects) and `scripts/_smoke_worklog_writecycle.py` (write-edit-delete cycle with safety cleanup) — should be **kept in the repo as regression tools**. If worklog sync ever starts missing events in production, running these two scripts isolates whether the fault is Jira-side, API-shape-side, or sync-code-side within ~4 minutes.

### 2.7 Duplicate-work acknowledgement (design choice)

`/worklog/updated` reports every mutation of a worklog at its current `updatedTime`, which means a worklog edited N times in a day will be re-upserted N times across incremental runs. For Aptum's volume (~24 changes/day across the project), this is trivial and has been accepted. The `ON CONFLICT (worklog_id) DO UPDATE` statement guarantees the **last sweep wins** — the DB row always reflects the latest Jira state, never a stale intermediate edit. No version tracking or edit history is kept by design (see 4.3 `upsert_worklogs`).

If volume ever grows an order of magnitude, add a short-circuit inside Path B: `WHERE excluded.jira_updated_at > ticket_worklogs.jira_updated_at` on the conflict clause. Out of scope for v1.

---

## 3. Schema changes — `schema/003_worklogs.sql`

Create a new migration file. It must be idempotent (`IF NOT EXISTS`) and safe to run on a live database.

```sql
-- ============================================================
-- 003_worklogs.sql — per-entry worklog storage + sync cursor
-- ============================================================

-- Add issue_id to tickets so we can resolve /worklog/list results
-- (which key off numeric issueId, not issueKey) back to issue_key.
ALTER TABLE tickets
    ADD COLUMN IF NOT EXISTS issue_id BIGINT;

CREATE UNIQUE INDEX IF NOT EXISTS tickets_issue_id
    ON tickets (issue_id)
    WHERE issue_id IS NOT NULL;

-- Per-entry worklog rows. Mirrors thread_events structure.
CREATE TABLE IF NOT EXISTS ticket_worklogs (
    worklog_id           BIGINT PRIMARY KEY,
    issue_key            TEXT NOT NULL REFERENCES tickets(issue_key) ON DELETE CASCADE,
    issue_id             BIGINT NOT NULL,
    author_account_id    TEXT REFERENCES jira_users(account_id),
    time_spent_seconds   INTEGER NOT NULL CHECK (time_spent_seconds >= 0),
    started_at           TIMESTAMPTZ NOT NULL,
    comment_adf          JSONB,
    visibility           JSONB,
    jira_created_at      TIMESTAMPTZ NOT NULL,
    jira_updated_at      TIMESTAMPTZ NOT NULL,
    synced_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at           TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ticket_worklogs_issue_key
    ON ticket_worklogs (issue_key) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS ticket_worklogs_issue_id
    ON ticket_worklogs (issue_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS ticket_worklogs_author
    ON ticket_worklogs (author_account_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS ticket_worklogs_started
    ON ticket_worklogs (started_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS ticket_worklogs_updated
    ON ticket_worklogs (jira_updated_at DESC) WHERE deleted_at IS NULL;

-- Seed a second sync_state row for the worklog-updated cursor.
-- Keeps the existing jira_tickets row untouched.
INSERT INTO sync_state (source, status)
VALUES ('jira_worklogs', 'idle')
ON CONFLICT (source) DO NOTHING;

-- Optional convenience view: per-ticket aggregates, computed on read.
-- If downstream dashboards need this, uncomment. For v1 we keep it out.
-- CREATE OR REPLACE VIEW ticket_worklog_totals AS
-- SELECT
--     issue_key,
--     SUM(time_spent_seconds) AS total_seconds,
--     COUNT(*) AS entry_count,
--     COUNT(DISTINCT author_account_id) AS distinct_authors,
--     MIN(started_at) AS first_entry_at,
--     MAX(started_at) AS last_entry_at
-- FROM ticket_worklogs
-- WHERE deleted_at IS NULL
-- GROUP BY issue_key;
```

**Schema notes:**
- `worklog_id` is the PK. Jira worklog IDs are numeric and globally unique within the instance.
- `comment_adf JSONB` stores the raw ADF. NULL if no comment.
- `visibility JSONB` preserves the `{type, value}` visibility restriction if present (used by some tenants for role-restricted worklogs).
- `jira_created_at` / `jira_updated_at` are Jira's timestamps, distinct from `synced_at` (DB write time).
- `author_account_id` references `jira_users` — same FK pattern as `thread_events`. Persist layer must upsert the user first.
- CASCADE from `tickets` means a hard-delete of a ticket clears its worklogs. We don't hard-delete tickets in v1 (we soft-delete via `deleted_at`), so this is defensive.

**Migration execution**: the Docker init runs `/docker-entrypoint-initdb.d/*.sql` only on first boot, so this file won't apply to the existing running DB automatically. The task list includes an explicit `psql -f schema/003_worklogs.sql` step.

---

## 4. Code changes — file-by-file

### 4.1 `jsm_sync/jira_client.py`

**Delete / replace:**
- `_fetch_worklog` — rename to `_fetch_worklog_page` and fix pagination (currently reads only first page). Or delete and replace with the new `_fetch_issue_worklogs` below.

**Add:**

```python
async def _fetch_issue_worklogs(
    client: httpx.AsyncClient,
    issue_key: str,
    semaphore: asyncio.Semaphore,
    headers: dict,
) -> list[dict]:
    """
    Fetch ALL worklog entries for an issue, paginated.
    Returns raw Jira worklog objects (not processed).
    Used by backfill and by per-ticket refresh in incremental Phase A.
    """
    base_url = settings.jira_base_url.rstrip("/")
    url = f"{base_url}/rest/api/3/issue/{issue_key}/worklog"
    all_worklogs: list[dict] = []
    start_at = 0

    while True:
        _start = start_at
        async with semaphore:
            async def _do_page() -> Any:
                r = await client.get(
                    url,
                    params={"startAt": _start, "maxResults": 100},
                    headers=headers,
                    timeout=30.0,
                )
                r.raise_for_status()
                return r.json()
            data = await retry_with_backoff(_do_page, max_retries=3)

        worklogs = data.get("worklogs", [])
        all_worklogs.extend(worklogs)
        total = data.get("total", 0)
        if start_at + len(worklogs) >= total or not worklogs:
            break
        start_at += 100

    return all_worklogs


async def fetch_worklog_updates_since(
    client: httpx.AsyncClient,
    since_ms: int,
    semaphore: asyncio.Semaphore,
    headers: dict,
) -> tuple[list[int], int]:
    """
    Walk /rest/api/3/worklog/updated pagination.
    Returns (list of worklog IDs, the 'until' epoch-ms watermark from Jira).
    """
    base_url = settings.jira_base_url.rstrip("/")
    url = f"{base_url}/rest/api/3/worklog/updated"
    all_ids: list[int] = []
    current_since = since_ms
    last_until = since_ms

    while True:
        _since = current_since
        async with semaphore:
            async def _do_page() -> Any:
                r = await client.get(
                    url,
                    params={"since": _since},
                    headers=headers,
                    timeout=30.0,
                )
                r.raise_for_status()
                return r.json()
            data = await retry_with_backoff(_do_page, max_retries=3)

        values = data.get("values", [])
        all_ids.extend(int(v["worklogId"]) for v in values)
        last_until = int(data.get("until", current_since))
        if data.get("lastPage", True):
            break
        current_since = last_until  # Jira advances `since` to `until` for next page

    return all_ids, last_until


async def fetch_worklog_deletes_since(
    client: httpx.AsyncClient,
    since_ms: int,
    semaphore: asyncio.Semaphore,
    headers: dict,
) -> tuple[list[int], int]:
    """Same shape as fetch_worklog_updates_since but hits /worklog/deleted."""
    # implementation mirrors fetch_worklog_updates_since, URL is /rest/api/3/worklog/deleted


async def fetch_worklogs_bulk(
    client: httpx.AsyncClient,
    worklog_ids: list[int],
    semaphore: asyncio.Semaphore,
    headers: dict,
    batch_size: int = 1000,
) -> list[dict]:
    """
    POST /rest/api/3/worklog/list in batches of up to 1000 IDs.
    Returns full worklog objects (with issueId, author, comment, etc.).
    """
    base_url = settings.jira_base_url.rstrip("/")
    url = f"{base_url}/rest/api/3/worklog/list"
    all_worklogs: list[dict] = []

    for i in range(0, len(worklog_ids), batch_size):
        chunk = worklog_ids[i : i + batch_size]
        async with semaphore:
            async def _do_batch() -> Any:
                r = await client.post(
                    url,
                    json={"ids": chunk},
                    headers=headers,
                    timeout=60.0,
                )
                r.raise_for_status()
                return r.json()
            data = await retry_with_backoff(_do_batch, max_retries=3)
        all_worklogs.extend(data if isinstance(data, list) else [])

    return all_worklogs
```

**Modify `_fetch_one_ticket`:**

```python
async def _fetch_one_ticket(
    client: httpx.AsyncClient,
    issue_key: str,
    semaphore: asyncio.Semaphore,
    headers: dict,
    include_worklogs: bool = True,      # new
) -> Optional[dict]:
    # ... existing fetch of issue, comments, assets ...
    # Add:
    worklogs: list[dict] = []
    if include_worklogs:
        worklogs = await _fetch_issue_worklogs(client, issue_key, semaphore, headers)

    return _process_issue_to_ticket(issue, comments, asset_details, worklogs)
```

**Modify `_process_issue_to_ticket`:**
- Accept a new `worklogs: list[dict]` argument.
- Extract `issue_id` from the raw issue (`issue.get("id")`, cast to int). Add to the returned ticket dict as `"issue_id": int | None`.
- Pass the raw worklog list through to the returned dict as `"worklogs": worklogs` (raw Jira shape — transform layer does the shaping).

**Modify `fetch_ticket_batch` signature:**
```python
async def fetch_ticket_batch(
    client, keys, semaphore, headers,
    include_worklogs: bool = True,   # new
) -> list[dict]:
    tasks = [
        _fetch_one_ticket(client, k, semaphore, headers, include_worklogs=include_worklogs)
        for k in keys
    ]
    # ... rest unchanged
```

---

### 4.2 `jsm_sync/transform.py`

**Add to `TransformedTicket`:**

```python
@dataclass
class TransformedTicket:
    ticket_row: dict
    users: list[dict]
    organization: Optional[dict]
    thread_events: list[dict]
    assets: list[dict]
    ticket_asset_links: list[tuple[str, str]]
    worklogs: list[dict]                    # new
    worklog_author_ids_seen: set[str]       # new, for diff-based soft-delete in per-ticket mode
```

**In `transform_ticket`:**

- Add `ticket_row["issue_id"] = raw.get("issue_id")` (may be None for legacy rows that haven't been re-fetched yet).
- Process `raw.get("worklogs", [])` into DB-ready rows:

```python
from dateutil import parser as _dparser

worklog_rows: list[dict] = []
worklog_author_ids: set[str] = set()

for w in raw.get("worklogs", []):
    wid = w.get("id")
    if not wid:
        continue
    author = w.get("author") or {}
    author_account_id = author.get("accountId")

    # Ensure author is added to users list so FK upsert works
    if author_account_id:
        worklog_author_ids.add(author_account_id)
        if author_account_id not in users_by_id:
            users_by_id[author_account_id] = {
                "account_id": author_account_id,
                "display_name": author.get("displayName") or "",
                "email": author.get("emailAddress"),
                "role": determine_role(author),  # import from jira_client
                "account_type": author.get("accountType"),
            }

    def _parse_iso(s):
        try:
            return _dparser.parse(s) if s else None
        except (ValueError, TypeError):
            return None

    # `created` may be absent on GET responses (docs only show it on POST 201).
    # Fall back to `started` so the NOT NULL column is satisfied.
    jira_created = _parse_iso(w.get("created")) or _parse_iso(w.get("started"))
    jira_updated = _parse_iso(w.get("updated")) or jira_created

    worklog_rows.append({
        "worklog_id": int(wid),
        "issue_key": issue_key,
        "issue_id": int(w.get("issueId")) if w.get("issueId") else raw.get("issue_id"),
        "author_account_id": author_account_id,
        "time_spent_seconds": int(w.get("timeSpentSeconds") or 0),
        "started_at": _parse_iso(w.get("started")),
        "comment_adf": w.get("comment"),       # keep as dict, asyncpg will JSONB it
        "visibility": w.get("visibility"),
        "jira_created_at": jira_created,
        "jira_updated_at": jira_updated,
    })
```

- `users = list(users_by_id.values())` — unchanged, but now also includes worklog authors.

---

### 4.3 `jsm_sync/db.py`

**Add column binding** in `upsert_ticket` — add `issue_id` between `labels` and `sla_first_response_breached`:

```python
INSERT INTO tickets (
    issue_key, ..., labels, issue_id,
    sla_first_response_breached, ...
) VALUES (..., $14, $15, $16, ...)
ON CONFLICT (issue_key) DO UPDATE SET
    ...
    labels   = EXCLUDED.labels,
    issue_id = COALESCE(EXCLUDED.issue_id, tickets.issue_id),  -- don't regress to NULL
    ...
```

Shift the positional parameters accordingly and add `row.get("issue_id")` to the call.

**Add new helpers:**

```python
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
                w["worklog_id"], w["issue_key"], w.get("issue_id"),
                w.get("author_account_id"),
                w["time_spent_seconds"], w["started_at"],
                json.dumps(w["comment_adf"]) if w.get("comment_adf") is not None else None,
                json.dumps(w["visibility"]) if w.get("visibility") is not None else None,
                w["jira_created_at"], w["jira_updated_at"],
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
    return await conn.fetchval(
        """
        WITH deleted AS (
            UPDATE ticket_worklogs
            SET deleted_at = NOW(), synced_at = NOW()
            WHERE issue_key = $1
              AND deleted_at IS NULL
              AND NOT (worklog_id = ANY($2::bigint[]))
            RETURNING 1
        )
        SELECT COUNT(*) FROM deleted
        """,
        issue_key,
        present_worklog_ids,
    )


async def soft_delete_worklogs_by_id(
    conn: asyncpg.Connection,
    worklog_ids: list[int],
) -> int:
    """For global sweep: mark specific worklog IDs deleted."""
    if not worklog_ids:
        return 0
    return await conn.fetchval(
        """
        WITH deleted AS (
            UPDATE ticket_worklogs
            SET deleted_at = NOW(), synced_at = NOW()
            WHERE worklog_id = ANY($1::bigint[])
              AND deleted_at IS NULL
            RETURNING 1
        )
        SELECT COUNT(*) FROM deleted
        """,
        worklog_ids,
    )


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
    return {r["issue_id"]: r["issue_key"] for r in rows}
```

**Modify `persist_ticket`:** extend the transaction to include worklog writes and per-ticket diff-soft-delete:

```python
async def persist_ticket(transformed: TransformedTicket) -> None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            for u in transformed.users:
                await upsert_user(conn, u)
            if transformed.organization:
                await upsert_organization(conn, transformed.organization)
            await upsert_ticket(conn, transformed.ticket_row)
            await upsert_thread_events(conn, transformed.ticket_row["issue_key"], transformed.thread_events)
            await upsert_assets(conn, transformed.assets)
            await upsert_ticket_asset_links(conn, transformed.ticket_asset_links)

            # New: worklog upsert + diff-based soft-delete
            await upsert_worklogs(conn, transformed.worklogs)
            present_ids = [w["worklog_id"] for w in transformed.worklogs]
            await soft_delete_missing_worklogs(
                conn,
                transformed.ticket_row["issue_key"],
                present_ids,
            )
```

**Add sync_state helpers for the worklog cursor:**

The existing `get_sync_cursor` / `set_sync_cursor` already accept a `source` arg — reuse them with `source="jira_worklogs"`. No new functions needed, but:

```python
async def get_worklog_cursor_ms(source: str = "jira_worklogs") -> Optional[int]:
    """Return worklog cursor as epoch milliseconds (the format /worklog/updated wants)."""
    dt = await get_sync_cursor(source)
    if dt is None:
        return None
    return int(dt.timestamp() * 1000)


async def set_worklog_cursor_ms(since_ms: int, source: str = "jira_worklogs") -> None:
    dt = datetime.fromtimestamp(since_ms / 1000, tz=timezone.utc)
    await set_sync_cursor(source, dt, status="idle")
```

---

### 4.4 `jsm_sync/worklog_sync.py` (new file)

New module that owns the global `/worklog/updated` + `/worklog/deleted` sweep. Called by both `backfill.py` and `incremental.py`.

```python
"""
Global worklog sweep using /rest/api/3/worklog/updated and /worklog/deleted.

Called AFTER the main ticket sweep in both backfill.py and incremental.py to
catch worklog changes on tickets whose issue.updated did not move.

Independent cursor: sync_state.source = 'jira_worklogs'.
Cursor is epoch-ms (stored as ISO in sync_state.last_cursor).
"""
import asyncio
import logging
from datetime import datetime, timezone

import asyncpg
import httpx

from .config import settings
from .db import (
    get_pool,
    get_worklog_cursor_ms,
    map_issue_ids_to_keys,
    set_worklog_cursor_ms,
    soft_delete_worklogs_by_id,
    upsert_worklogs,
    upsert_user,
)
from .jira_client import (
    _auth_headers,
    determine_role,
    fetch_worklog_updates_since,
    fetch_worklog_deletes_since,
    fetch_worklogs_bulk,
)
from .transform import _parse_iso  # extract helper or inline

logger = logging.getLogger(__name__)
WORKLOG_SOURCE = "jira_worklogs"


async def run_worklog_sweep(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    headers: dict,
    initial_cursor_ms: int | None = None,
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

    logger.info("Worklog sweep since %d (%s)", cursor_ms,
                datetime.fromtimestamp(cursor_ms/1000, tz=timezone.utc).isoformat())

    # 1. Get updated IDs and bulk-fetch details
    updated_ids, until_updated = await fetch_worklog_updates_since(
        client, cursor_ms, semaphore, headers
    )
    deleted_ids, until_deleted = await fetch_worklog_deletes_since(
        client, cursor_ms, semaphore, headers
    )
    logger.info("Jira reported %d updated, %d deleted worklogs", len(updated_ids), len(deleted_ids))

    touched = 0

    if updated_ids:
        full = await fetch_worklogs_bulk(client, updated_ids, semaphore, headers)

        # Filter to OUR tickets by mapping issueId → issue_key
        pool = await get_pool()
        async with pool.acquire() as conn:
            issue_ids_seen = list({int(w["issueId"]) for w in full if w.get("issueId")})
            id_to_key = await map_issue_ids_to_keys(conn, issue_ids_seen)

        relevant = [w for w in full if int(w.get("issueId", 0)) in id_to_key]
        logger.info("Of %d fetched, %d belong to tickets we track", len(full), len(relevant))

        # Transform and upsert
        async with pool.acquire() as conn:
            async with conn.transaction():
                for w in relevant:
                    issue_id = int(w["issueId"])
                    issue_key = id_to_key[issue_id]
                    author = w.get("author") or {}
                    aid = author.get("accountId")
                    if aid:
                        await upsert_user(conn, {
                            "account_id": aid,
                            "display_name": author.get("displayName") or "",
                            "email": author.get("emailAddress"),
                            "role": determine_role(author),
                            "account_type": author.get("accountType"),
                        })
                    await upsert_worklogs(conn, [{
                        "worklog_id": int(w["id"]),
                        "issue_key": issue_key,
                        "issue_id": issue_id,
                        "author_account_id": aid,
                        "time_spent_seconds": int(w.get("timeSpentSeconds") or 0),
                        "started_at": _parse_iso(w.get("started")),
                        "comment_adf": w.get("comment"),
                        "visibility": w.get("visibility"),
                        "jira_created_at": _parse_iso(w.get("created")),
                        "jira_updated_at": _parse_iso(w.get("updated")),
                    }])
                    touched += 1

    # 2. Soft-delete
    if deleted_ids:
        async with (await get_pool()).acquire() as conn:
            n = await soft_delete_worklogs_by_id(conn, deleted_ids)
            logger.info("Soft-deleted %d worklogs", n)
            touched += n

    # 3. Advance cursor to the smaller of the two 'until's (conservative)
    next_cursor = min(until_updated, until_deleted)
    await set_worklog_cursor_ms(next_cursor, WORKLOG_SOURCE)
    logger.info("Worklog cursor advanced to %d", next_cursor)

    return touched
```

---

### 4.5 `jsm_sync/backfill.py`

Minimal change. Backfill uses the per-ticket worklog fetch path (already wired via `_fetch_one_ticket`). After the ticket sweep, if this was a first-ever backfill (worklog cursor is NULL), pin the worklog cursor to the backfill start time so incremental takes over from there without re-fetching everything.

```python
# At top of run_backfill():
backfill_start_ms = int(datetime.now(timezone.utc).timestamp() * 1000)

# ... existing ticket loop (unchanged except for the --no-worklogs flag) ...
# Pass include_worklogs down into fetch_ticket_batch:
tickets = await fetch_ticket_batch(
    client, batch, semaphore, headers,
    include_worklogs=not args.no_worklogs,
)

# After the batch loop, before mark_sync_complete:
if not args.no_worklogs:
    existing_cursor = await get_worklog_cursor_ms(WORKLOG_SOURCE)
    if existing_cursor is None:
        await set_worklog_cursor_ms(backfill_start_ms, WORKLOG_SOURCE)
        logger.info("Pinned initial worklog cursor to backfill start: %d", backfill_start_ms)
    else:
        # Incremental-style top-up: anything created/updated DURING the long backfill
        await run_worklog_sweep(client, semaphore, headers)
```

Add CLI flag:
```python
p.add_argument("--no-worklogs", action="store_true",
               help="Skip worklog fetching (faster backfill, but ticket_worklogs will be stale)")
```

---

### 4.6 `jsm_sync/incremental.py`

Add both a per-ticket refresh (already implicit through the modified `_fetch_one_ticket`) AND a global sweep after the ticket phase.

```python
# In run_incremental(), after the ticket batch loop:

# Phase B: global worklog sweep
if not args.no_worklogs:
    logger.info("Starting global worklog sweep (Phase B)")
    try:
        touched = await run_worklog_sweep(client, semaphore, headers)
        logger.info("Global worklog sweep complete — %d entries touched", touched)
    except Exception:
        logger.exception("Worklog sweep failed — ticket sync already committed")
        # Don't fail the whole run — the next incremental will catch up
```

Add CLI flag identical to backfill.

Also: update the call to `fetch_ticket_batch` to pass `include_worklogs=not args.no_worklogs`.

---

### 4.7 `jsm_sync/reconcile.py`

Optional in v1 — if the weekly reconcile runs, consider adding a post-step that checks for orphan worklogs (rows where `issue_key` points to a soft-deleted ticket) and cascades soft-deletion. Low priority; document as a known gap if skipped.

---

## 5. Progress display (new — addresses "massive stream of http requests")

The current backfill emits a flood of per-batch log lines and relies on `LOG_LEVEL` to control httpx's request-level chatter. Replace with a single live progress bar using [`rich`](https://rich.readthedocs.io/) so the user sees count, rate, ETA, and elapsed time at a glance. Logs keep scrolling ABOVE the bar.

### 5.1 Dependency

Add `rich>=13.7` to the project's dependency manifest (check if `pyproject.toml` or `requirements.txt` is the source of truth before editing — likely `pyproject.toml` per the project's layout). Also ensure `httpx` logging is quieted:

```python
# In the basicConfig block of backfill.py and incremental.py
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
```

### 5.2 New module `jsm_sync/progress.py`

Centralize the progress-display logic so backfill, incremental, and the worklog sweep all share the same UX.

```python
"""
Rich-based progress display for long-running sync operations.

Usage:
    async with SyncProgress("Backfill") as p:
        scout_task = p.add_task("Scouting ticket keys", total=None)   # indeterminate
        # ... do scout work ...
        p.update(scout_task, total=count, completed=count)

        process_task = p.add_task("Processing tickets", total=len(keys))
        for batch in batches:
            # ...
            p.advance(process_task, len(batch))
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

from rich.console import Console
from rich.logging import RichHandler
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


def install_rich_logging(level: str = "INFO") -> Console:
    """
    Replace basicConfig with a Rich handler. Call ONCE early in main().
    Returns the shared Console so the Progress can render on it.
    """
    console = Console(stderr=False)
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(
            console=console,
            show_time=True,
            show_level=True,
            show_path=False,
            markup=False,
            rich_tracebacks=True,
        )],
    )
    # Quiet the HTTP noise
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    return console


class SyncProgress:
    """Thin wrapper around rich.progress.Progress with sensible defaults for sync work."""

    def __init__(self, title: str, console: Optional[Console] = None) -> None:
        self.title = title
        self.console = console or Console()
        self._progress: Optional[Progress] = None

    def __enter__(self) -> "SyncProgress":
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            MofNCompleteColumn(),
            TextColumn("•"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("•"),
            TimeElapsedColumn(),
            TextColumn("•"),
            TimeRemainingColumn(),
            console=self.console,
            transient=False,
            refresh_per_second=4,
        )
        self._progress.__enter__()
        self.console.rule(f"[bold]{self.title}")
        return self

    def __exit__(self, *exc) -> None:
        assert self._progress is not None
        self._progress.__exit__(*exc)
        self._progress = None

    def add_task(self, description: str, total: Optional[int] = None) -> TaskID:
        assert self._progress is not None
        return self._progress.add_task(description, total=total)

    def advance(self, task_id: TaskID, n: int = 1) -> None:
        assert self._progress is not None
        self._progress.advance(task_id, n)

    def update(self, task_id: TaskID, **kwargs) -> None:
        assert self._progress is not None
        self._progress.update(task_id, **kwargs)

    def stop_task(self, task_id: TaskID) -> None:
        assert self._progress is not None
        self._progress.update(task_id, visible=True)
        # Progress auto-shows completed when total is set; no special action needed.
```

### 5.3 Wire into `backfill.py`

Replace the ad-hoc `logger.info("Batch %d/%d …")` noise with a three-phase progress display:

```python
from .progress import SyncProgress, install_rich_logging

async def run_backfill(lookback_days, batch_size, force_lookback=False):
    console = install_rich_logging(settings.log_level)  # moved from main()
    await init_pool()
    try:
        # ... cursor resolution (same as today) ...
        await mark_sync_running(SOURCE_NAME)

        async with httpx.AsyncClient() as client:
            headers = _auth_headers()
            semaphore = asyncio.Semaphore(settings.jira_semaphore_limit)

            with SyncProgress("Backfill", console=console) as p:
                # Phase 1: scout (indeterminate — we don't know count upfront)
                scout_task = p.add_task("Scouting ticket keys", total=None)
                all_keys = await _fetch_all_keys_jql(client, jql, semaphore, headers)
                p.update(scout_task, total=len(all_keys), completed=len(all_keys))

                # Phase 2: process tickets
                process_task = p.add_task(
                    f"Fetching & persisting {len(all_keys):,} tickets",
                    total=len(all_keys),
                )

                for i in range(0, len(all_keys), batch_size):
                    batch = all_keys[i : i + batch_size]
                    tickets = await fetch_ticket_batch(
                        client, batch, semaphore, headers,
                        include_worklogs=not args.no_worklogs,
                    )
                    # ... persist loop (same as today) ...
                    for ticket in tickets:
                        try:
                            transformed = transform_ticket(ticket)
                            await persist_ticket(transformed)
                            # cursor tracking unchanged
                        except Exception:
                            logger.exception("Failed %s", ticket.get("issue_key"))
                    p.advance(process_task, len(batch))
                    if max_updated:
                        await set_sync_cursor(SOURCE_NAME, max_updated, status="running")

                # Phase 3: worklog cursor pinning / top-up sweep
                if not args.no_worklogs:
                    existing_cursor = await get_worklog_cursor_ms(WORKLOG_SOURCE)
                    if existing_cursor is None:
                        await set_worklog_cursor_ms(backfill_start_ms, WORKLOG_SOURCE)
                        logger.info("Pinned worklog cursor to backfill start")
                    else:
                        sweep_task = p.add_task("Worklog top-up sweep", total=None)
                        await run_worklog_sweep(client, semaphore, headers, progress=p, task_id=sweep_task)

        await mark_sync_complete(SOURCE_NAME)
```

### 5.4 Wire into `worklog_sync.py` (pass-through progress)

`run_worklog_sweep` takes optional `progress` and `task_id` kwargs so both backfill and incremental can attach it to their existing Progress display:

```python
async def run_worklog_sweep(
    client, semaphore, headers,
    initial_cursor_ms=None,
    progress: Optional["SyncProgress"] = None,
    task_id=None,
) -> int:
    # ... fetch updated_ids / deleted_ids as before ...
    if progress and task_id is not None:
        progress.update(task_id, total=len(updated_ids) + len(deleted_ids))

    # During bulk fetch & upsert:
    for i in range(0, len(updated_ids), 1000):
        batch = updated_ids[i:i+1000]
        # ... fetch + transform + persist ...
        if progress and task_id is not None:
            progress.advance(task_id, len(batch))

    # After soft-deletes:
    if progress and task_id is not None:
        progress.advance(task_id, len(deleted_ids))
```

### 5.5 Wire into `incremental.py`

Same `SyncProgress` wrapper, two phases:

```python
with SyncProgress("Incremental sync", console=console) as p:
    scout_task = p.add_task("Scouting updated tickets", total=None)
    all_keys = await _fetch_all_keys_jql(...)
    p.update(scout_task, total=len(all_keys), completed=len(all_keys))

    if all_keys:
        process_task = p.add_task(
            f"Processing {len(all_keys)} tickets", total=len(all_keys),
        )
        # ... loop with p.advance(process_task, len(batch)) ...

    if not args.no_worklogs:
        sweep_task = p.add_task("Worklog sweep", total=None)
        await run_worklog_sweep(client, semaphore, headers, progress=p, task_id=sweep_task)
```

### 5.6 launchd / non-TTY behavior

Rich auto-detects TTY. When launchd runs `jsm_sync.incremental` and pipes stdout to a log file, the Progress display degrades to occasional "elapsed: Xs, Y/Z completed" lines rather than ANSI cursor control — clean in the log file, still useful. No special handling needed, but the implementer should confirm by running:
```bash
python -m jsm_sync.incremental > /tmp/test.log 2>&1
```
and verifying the log file is readable (no stray ANSI escape sequences).

---

## 6. Task list (execute in order)

Each task is a discrete commit-sized unit. Mark complete only when acceptance criteria are met.

API shapes were already validated in Section 2 against the official Atlassian docs — no additional verification task needed. If any real-world response deviates during implementation, record it in a new `WORKLOGS_PLAN_NOTES.md` and adjust.

### Task 1 — Create schema migration `schema/003_worklogs.sql`
**Actions:**
- Write the SQL from Section 3 verbatim.
- Apply to running Postgres: `docker exec -i <pg-container> psql -U <user> -d <db> < schema/003_worklogs.sql`.
- Verify: `\d ticket_worklogs`, `\d tickets` (shows new `issue_id` column), `SELECT * FROM sync_state WHERE source='jira_worklogs';` returns one row.

**Acceptance:** All three verification queries return expected output. No errors.

---

### Task 2 — Add worklog fetchers to `jira_client.py`
**Actions:**
- Implement `_fetch_issue_worklogs` (paginated).
- Implement `fetch_worklog_updates_since`, `fetch_worklog_deletes_since`, `fetch_worklogs_bulk`.
- Remove or rename the broken existing `_fetch_worklog`.

**Acceptance:** Unit test (or scripted smoke test in a throwaway `scripts/_probe_worklogs.py`) pulls worklogs for one known issue_key with >0 entries and one with >20 (verifies pagination). Prints count; matches Jira UI count.

---

### Task 3 — Wire worklogs into `_fetch_one_ticket` / `_process_issue_to_ticket` / `fetch_ticket_batch`
**Actions:**
- Extend signatures per Section 4.1.
- `_process_issue_to_ticket` now emits `issue_id` and `worklogs` fields.

**Acceptance:** Calling `fetch_ticket_batch` on a list with one known issue returns a ticket dict containing `"issue_id": <int>` and `"worklogs": [...]` with the right entry count.

---

### Task 4 — Extend `transform.py`
**Actions:**
- Add `worklogs` and `worklog_author_ids_seen` to `TransformedTicket`.
- Add `issue_id` to `ticket_row`.
- Add worklog authors to the `users_by_id` dict so FK upsert works.
- Implement the worklog row builder per Section 4.2.

**Acceptance:** Unit test passes a fake raw ticket with two worklogs (different authors, one with ADF comment, one without) and asserts: `len(transformed.worklogs) == 2`, both authors are in `transformed.users`, and ADF is preserved as a dict on the row.

---

### Task 5 — Extend `db.py`
**Actions:**
- Modify `upsert_ticket` to write `issue_id` with the `COALESCE` guard on conflict.
- Add `upsert_worklogs`, `soft_delete_missing_worklogs`, `soft_delete_worklogs_by_id`, `map_issue_ids_to_keys`.
- Add `get_worklog_cursor_ms` / `set_worklog_cursor_ms`.
- Extend `persist_ticket` to include worklog upsert + per-ticket diff soft-delete inside the existing transaction.

**Acceptance:** Integration test (throwaway script) persists a ticket with 3 worklogs, re-persists same ticket with only 2 (one removed from the input), and confirms the missing row now has `deleted_at IS NOT NULL`.

---

### Task 6 — Create `worklog_sync.py`
**Actions:**
- Implement `run_worklog_sweep` per Section 4.4.
- Make sure `_parse_iso` is imported or copy-pasted (it's trivial — do NOT introduce a circular import).

**Acceptance:** Manually invoke with a recent cursor (e.g. `now - 1h` in ms). Verify the function completes, logs "N fetched, M belong to tickets we track", and updates `sync_state.jira_worklogs.last_cursor`.

---

### Task 7 — Add `progress.py` and install Rich logging
**Actions:**
- Add `rich>=13.7` to the project's dependency file (check `pyproject.toml` first, fall back to `requirements.txt`).
- Create `jsm_sync/progress.py` per Section 5.2.
- Verify it runs standalone: `python -c "from jsm_sync.progress import SyncProgress; import time; p=SyncProgress('test');
p.__enter__(); t=p.add_task('work', total=10); [p.advance(t) or time.sleep(0.1) for _ in range(10)]; p.__exit__()"` — should display a filling bar.

**Acceptance:** Smoke test shows a working progress bar in the terminal. `pip install -e .` (or equivalent) picks up `rich` without errors.

---

### Task 8 — Wire into `backfill.py`
**Actions:**
- Replace `logging.basicConfig` call with `install_rich_logging(settings.log_level)`.
- Add `--no-worklogs` flag.
- Capture `backfill_start_ms = int(datetime.now(timezone.utc).timestamp() * 1000)` at start.
- Wrap the existing ticket loop in `with SyncProgress("Backfill") as p:` per Section 5.3.
- Replace the per-batch `logger.info("Batch …")` with `p.advance(process_task, len(batch))`. KEEP the checkpoint cursor log (important for resumability debugging) but demote from info to debug if it's too chatty.
- Pass `include_worklogs=not args.no_worklogs` into `fetch_ticket_batch`.
- After ticket loop: pin cursor on first backfill OR run sweep on re-backfill (with progress attached).

**Acceptance:**
1. Running `python -m jsm_sync.backfill --lookback-days 1` shows ONE persistent progress bar for the full run (scout → process), NOT a wall of per-batch log lines. Bar shows count, percentage, elapsed, ETA.
2. httpx request logs are silent.
3. `ticket_worklogs` is populated for the window, and `sync_state.jira_worklogs.last_cursor` is set to a timestamp within the last few minutes.

---

### Task 9 — Wire into `incremental.py`
**Actions:**
- Same logging swap (`install_rich_logging`).
- Add `--no-worklogs` flag.
- Wrap work in `SyncProgress("Incremental sync")` per Section 5.5.
- Pass `include_worklogs` into `fetch_ticket_batch`.
- Call `run_worklog_sweep(..., progress=p, task_id=sweep_task)` after the ticket loop, wrapped in try/except (non-fatal).

**Acceptance:**
1. Adding a worklog in Jira UI, then running `python -m jsm_sync.incremental`, results in exactly one new row in `ticket_worklogs`.
2. Output is a clean progress bar, not a log flood.
3. When piped to a file (simulating launchd), the log is ANSI-clean and readable.

---

### Task 10 — Full historical worklog backfill
**Actions:**
- Current production DB has ~600 days of tickets with no worklogs. These tickets' rows exist but have no `issue_id` and no `ticket_worklogs` entries.
- Option A (recommended): clear `sync_state.jira_tickets.last_cursor`, re-run `python -m jsm_sync.backfill --lookback-days 600`. Upserts are idempotent, so tickets/comments/assets are re-written but not multiplied. Worklogs populate from scratch. Estimate: same runtime as original backfill plus ~1 extra request per ticket.
- Option B: add a dedicated one-shot script `scripts/worklog_historical_backfill.py` that iterates all existing tickets in DB, fetches `_fetch_issue_worklogs` for each, upserts — does NOT re-fetch the issue. Faster, but does not populate the new `issue_id` column for old tickets.

**Decision rule:** If Option A completes within an acceptable window (check how long previous backfill took — see `terminals/12.txt`), use A. Otherwise use B and schedule a separate `issue_id` backfill via `UPDATE tickets SET issue_id = ... FROM (SELECT id FROM jira ...)`.

**Acceptance:** `SELECT COUNT(*) FROM ticket_worklogs WHERE deleted_at IS NULL;` returns a number consistent with manual spot-check of 5 random tickets against their Jira UI worklog counts.

---

### Task 11 — launchd agent verification
**Actions:**
- User has an existing launchd agent running `python -m jsm_sync.incremental` on a cadence.
- No changes required — incremental now handles worklogs internally.
- Verify by tailing its log after the next scheduled run: should see "Starting global worklog sweep (Phase B)" and "cursor advanced to X".

**Acceptance:** Next launchd run logs both the ticket sweep AND the worklog sweep without errors. The log file is free of ANSI escape sequences (Rich auto-detected non-TTY).

---

### Task 12 — Update `PLAN.md` and docs
**Actions:**
- Update the "Do not fetch worklogs during backfill" line in `PLAN.md` (line ~915) to reflect the new behavior.
- Update the schema section and `DIAGRAMS.md` (lines ~29, 298, 324) to show worklogs are now in DB.
- Add a short README section: "Worklog sync" — how it works, how to opt out (`--no-worklogs`), how to manually re-run the sweep, the 1-minute lag caveat, and the progress bar UX.

**Acceptance:** `rg -i worklog PLAN.md DIAGRAMS.md README.md` shows descriptions consistent with actual behavior.

---

## 7. Guardrails & rollback

- **Schema rollback:** worklogs are additive — `DROP TABLE ticket_worklogs; ALTER TABLE tickets DROP COLUMN issue_id; DELETE FROM sync_state WHERE source='jira_worklogs';` restores pre-state. The `tickets` table is unaffected for non-worklog reads.
- **Code rollback:** if Task 9 (incremental wiring) breaks the cron, flip the `--no-worklogs` flag in the launchd plist. Ticket sync continues unaffected.
- **Transaction safety:** worklog writes are inside `persist_ticket`'s transaction. If the worklog upsert fails, the whole ticket upsert rolls back — no half-state. The global sweep is non-transactional per-batch; a crash mid-sweep means the cursor is not advanced, so the next run re-sweeps the same window. All upserts are idempotent.
- **Rate limiting:** per-ticket worklog fetch adds one request per ticket (N+2 per ticket total: issue + comments + worklog, plus assets). The existing `settings.jira_semaphore_limit` bounds concurrency. If 429s spike, lower the semaphore before lowering batch size.
- **Cursor slip:** the global sweep advances the cursor to `min(until_updated, until_deleted)` — the conservative watermark. A race between Jira indexing and our read may leave a small window double-processed on the next run; harmless due to idempotency.

---

## 8. Out of scope for v1

- Embedding worklog comments.
- Per-ticket aggregate columns on `tickets` (use a view if needed later).
- Reconcile-worklog support.
- Historical backfill of `issue_id` for pre-existing tickets if Option B is chosen in Task 10 (separate one-shot SQL task).
- Metrics / alerting on worklog sweep latency.
- Multi-panel Rich Live display (e.g. current ticket key, last HTTP status code, in-flight request count). Single bar is enough for v1.

---

## 9. Files touched (summary)

| File | Change type |
|---|---|
| `schema/003_worklogs.sql` | NEW |
| `jsm_sync/jira_client.py` | MODIFY — 4 new fetchers, modified `_fetch_one_ticket`/`_process_issue_to_ticket`/`fetch_ticket_batch` |
| `jsm_sync/transform.py` | MODIFY — worklog rows, issue_id, extended users |
| `jsm_sync/db.py` | MODIFY — new upserts, modified `upsert_ticket`, extended `persist_ticket` |
| `jsm_sync/worklog_sync.py` | NEW |
| `jsm_sync/progress.py` | NEW — Rich-based progress bar + log handler |
| `jsm_sync/backfill.py` | MODIFY — flag, cursor pinning, progress bar, Rich logging |
| `jsm_sync/incremental.py` | MODIFY — flag, Phase B sweep, progress bar, Rich logging |
| `pyproject.toml` (or `requirements.txt`) | MODIFY — add `rich>=13.7` |
| `PLAN.md`, `DIAGRAMS.md`, `README.md` | MODIFY — doc updates |
| `scripts/_smoke_worklog_observe.py` | KEEP — read-only regression tool (already on disk) |
| `scripts/_smoke_worklog_writecycle.py` | KEEP — write-cycle regression tool (already on disk) |
