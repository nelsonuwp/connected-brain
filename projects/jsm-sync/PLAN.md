# jsm-sync — Build Plan

## Purpose

Mirror the APTUM Jira Service Management project into a local Postgres database so downstream tools (persona-drafting assistant, AccountIntel, ad-hoc SQL analysis) can run rapid queries without hitting Jira rate limits.

The split: bulk, append-mostly data (tickets, comments, users, orgs, assets) lives in Postgres. Nuanced per-ticket data (worklogs, live SLA timers, attachments) stays in Jira and gets fetched on-demand when a specific ticket key is already known.

## Scope for v1

- Backfill the last 30 days of APTUM tickets into Postgres.
- Incremental sync runs on a cron/timer and keeps Postgres fresh with Jira deltas.
- No embeddings, no pgvector, no tsvector yet — those come after the raw data is flowing.
- No Fusion DB integration yet — that's a parallel sync job added later.
- No webhooks — polling only for v1.
- No FastAPI frontend yet — this project is the data layer. The persona-drafting app is a separate project that reads from this Postgres.

## Guiding principles for implementation

1. **Reuse the existing `jiraClient.py`.** Adam has a working async Jira client with Scout/Plan/Gather pattern, retry with backoff, semaphore throttling, role determination, ADF flattening, and asset hydration. Port it, clean it, do not rewrite it.

2. **Resumability.** Backfill must be safe to kill and restart. JQL is ordered `updated ASC` and the cursor is checkpointed after each batch commit. If the laptop sleeps mid-backfill, re-running continues from where it stopped.

3. **Idempotency.** Every write is an upsert with `ON CONFLICT DO UPDATE`. Running the sync twice produces the same database state as running it once.

4. **Keep raw noise.** Zabbix/PagerDuty automated tickets get synced too. Filter at the read layer, not at sync time. The `is_customer_originated` flag (derived from creator role) makes this cheap.

5. **No secrets in Git.** `.env` is gitignored from commit zero. Rotating credentials means editing `.env`, not rewriting history.

6. **Bind-mounted Postgres data.** The database files live in `./postgres_data/` on the host filesystem, not inside the Docker volume. This makes the data survive container rebuilds and makes backup a simple folder copy.

---

## Directory structure to create

```
jsm-sync/
├── .env                        # gitignored, real secrets
├── .env.example                # committed, template
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── README.md
├── PLAN.md                     # this file
├── DIAGRAMS.md                 # visual companion
├── postgres_data/              # gitignored, Postgres data dir (bind mount)
├── schema/
│   └── 001_initial.sql         # auto-run by Postgres on first boot
├── config/
│   └── jira_automation_users.json
└── jsm_sync/
    ├── __init__.py
    ├── config.py               # typed settings loaded from .env
    ├── db.py                   # asyncpg pool + upsert helpers
    ├── jira_client.py          # ported from Adam's existing client
    ├── transform.py            # Jira dict → upsert tuples
    ├── backfill.py             # one-shot entry point with resumability
    ├── incremental.py          # cursor-based delta sync
    └── reconcile.py            # weekly full-list diff to catch deletes
```

---

## Files to create — exact contents

### `.gitignore`

```
# Secrets
.env
.env.local

# Python
.venv/
venv/
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.mypy_cache/
*.egg-info/

# Postgres
postgres_data/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# IDE
.vscode/
.idea/
```

### `.env.example`

```
# Postgres (local dev defaults)
POSTGRES_PASSWORD=localdev
DATABASE_URL=postgresql://jsm_sync:localdev@localhost:5432/jsm_sync

# Jira
JIRA_BASE_URL=https://aptum.atlassian.net
JIRA_USERNAME=
JIRA_API_TOKEN=

# Sync config
JIRA_PROJECT=APTUM
JIRA_LOOKBACK_DAYS=30
JIRA_SEMAPHORE_LIMIT=5

# Logging
LOG_LEVEL=INFO
```

### `docker-compose.yml`

```yaml
services:
  postgres:
    image: postgres:16
    container_name: jsm-sync-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: jsm_sync
      POSTGRES_USER: jsm_sync
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-localdev}
    ports:
      - "5432:5432"
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
      - ./schema:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U jsm_sync -d jsm_sync"]
      interval: 5s
      timeout: 5s
      retries: 5
```

### `requirements.txt`

```
httpx>=0.27
asyncpg>=0.29
python-dotenv>=1.0
python-dateutil>=2.8
pydantic>=2.0
pydantic-settings>=2.0
```

### `schema/001_initial.sql`

```sql
-- ============================================================
-- jsm-sync initial schema
-- Runs automatically on first Postgres boot via docker-entrypoint-initdb.d
-- ============================================================

-- === Reference tables ===

CREATE TABLE jira_users (
    account_id          TEXT PRIMARY KEY,
    display_name        TEXT NOT NULL,
    email               TEXT,
    role                TEXT NOT NULL CHECK (role IN ('Customer','Aptum','Automation','Unknown')),
    account_type        TEXT,
    first_seen_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX jira_users_role ON jira_users (role);

CREATE TABLE organizations (
    jira_org_id         TEXT PRIMARY KEY,
    name                TEXT NOT NULL,
    ocean_client_id     INTEGER,
    first_seen_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX organizations_ocean_client ON organizations (ocean_client_id);
CREATE INDEX organizations_name ON organizations (name);

-- === Tickets ===

CREATE TABLE tickets (
    issue_key           TEXT PRIMARY KEY,
    summary             TEXT NOT NULL,
    description         TEXT NOT NULL DEFAULT '',
    status              TEXT NOT NULL,
    priority            TEXT,
    issue_type          TEXT,
    request_type        TEXT,
    is_customer_originated BOOLEAN NOT NULL DEFAULT FALSE,

    creator_account_id  TEXT REFERENCES jira_users(account_id),
    reporter_account_id TEXT REFERENCES jira_users(account_id),
    assignee_account_id TEXT REFERENCES jira_users(account_id),
    jira_org_id         TEXT REFERENCES organizations(jira_org_id),
    ocean_client_id     INTEGER,

    labels              TEXT[] NOT NULL DEFAULT '{}',

    sla_first_response_breached   BOOLEAN,
    sla_first_response_elapsed_s  INTEGER,
    sla_first_response_threshold_s INTEGER,
    sla_resolution_breached       BOOLEAN,
    sla_resolution_elapsed_s      INTEGER,
    sla_resolution_threshold_s    INTEGER,

    created_at          TIMESTAMPTZ NOT NULL,
    updated_at          TIMESTAMPTZ NOT NULL,
    resolved_at         TIMESTAMPTZ,

    synced_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at          TIMESTAMPTZ
);

CREATE INDEX tickets_org           ON tickets (jira_org_id);
CREATE INDEX tickets_ocean_client  ON tickets (ocean_client_id);
CREATE INDEX tickets_status        ON tickets (status) WHERE deleted_at IS NULL;
CREATE INDEX tickets_updated       ON tickets (updated_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX tickets_created       ON tickets (created_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX tickets_customer_orig ON tickets (is_customer_originated) WHERE deleted_at IS NULL;
CREATE INDEX tickets_creator       ON tickets (creator_account_id);
CREATE INDEX tickets_assignee      ON tickets (assignee_account_id) WHERE deleted_at IS NULL;

-- === Thread events (comments, later: changelog) ===

CREATE TABLE thread_events (
    id                  TEXT PRIMARY KEY,
    issue_key           TEXT NOT NULL REFERENCES tickets(issue_key) ON DELETE CASCADE,
    kind                TEXT NOT NULL CHECK (kind IN ('comment','changelog')),
    author_account_id   TEXT REFERENCES jira_users(account_id),
    is_public           BOOLEAN,
    body                TEXT NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL,
    synced_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at          TIMESTAMPTZ
);

CREATE INDEX thread_events_issue   ON thread_events (issue_key, created_at);
CREATE INDEX thread_events_author  ON thread_events (author_account_id);
CREATE INDEX thread_events_public  ON thread_events (issue_key, is_public) WHERE kind = 'comment';

-- === Assets ===

CREATE TABLE assets (
    object_id           TEXT PRIMARY KEY,
    workspace_id        TEXT NOT NULL,
    asset_name          TEXT,
    service_id          TEXT,
    last_hydrated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX assets_service_id ON assets (service_id);
CREATE INDEX assets_workspace ON assets (workspace_id);

CREATE TABLE ticket_assets (
    issue_key           TEXT NOT NULL REFERENCES tickets(issue_key) ON DELETE CASCADE,
    object_id           TEXT NOT NULL REFERENCES assets(object_id),
    PRIMARY KEY (issue_key, object_id)
);

CREATE INDEX ticket_assets_object ON ticket_assets (object_id);

-- === Sync state ===

CREATE TABLE sync_state (
    source              TEXT PRIMARY KEY,
    last_sync_at        TIMESTAMPTZ,
    last_cursor         TEXT,
    status              TEXT NOT NULL DEFAULT 'idle'
                            CHECK (status IN ('idle','running','error','completed')),
    last_error          TEXT,
    metadata            JSONB NOT NULL DEFAULT '{}'::jsonb,
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Seed the sync_state row for the Jira ticket sync
INSERT INTO sync_state (source, status) VALUES ('jira_tickets', 'idle')
ON CONFLICT (source) DO NOTHING;
```

### `jsm_sync/__init__.py`

Empty file. Just makes it a package.

### `jsm_sync/config.py`

```python
"""Typed settings loaded from environment / .env file."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Postgres
    database_url: str

    # Jira
    jira_base_url: str
    jira_username: str
    jira_api_token: str

    # Sync config
    jira_project: str = "APTUM"
    jira_lookback_days: int = 30
    jira_semaphore_limit: int = 5

    # Logging
    log_level: str = "INFO"


settings = Settings()  # singleton
```

### `jsm_sync/jira_client.py`

This is the largest file. It's a port of Adam's existing `jiraClient.py` with these specific changes:

**Remove:**
- All imports from `core.utils` (`log`, `make_source_object`, `record_count_from_data`, `save_source_artifact`)
- The `save_source_artifact` call in `fetch_jira_data`
- The sync `fetch_jira_data_sync` function (we use async only)
- The `fetch_organization_users` function (not needed for v1; maybe later)
- The `make_source_object` / artifact-shaped return values
- Do NOT extract or persist `security_level` — Adam doesn't use it.

**Change:**
- Replace `log("⚠️", "...")` etc. with `logger.warning("...")` using stdlib logging
- `create_history_trail` reads `comment.get("jsdPublic")` into each event and does NOT truncate body text to 800 chars. The Pydantic-visible field is `body`, not `details`.
- The event dict schema becomes:
  ```python
  {
      "id": comment.get("id"),              # Jira comment ID, new
      "date": created.isoformat(),          # ISO not YYYY-MM-DD
      "created_at": created,                 # full datetime, new
      "role": role,
      "author": author.get("displayName"),
      "author_account_id": author.get("accountId"),
      "author_email": author.get("emailAddress"),
      "is_public": comment.get("jsdPublic"),  # new
      "body": text,                           # full, untruncated
      "kind": "comment",                      # new, always "comment" for now
  }
  ```

**Keep verbatim:**
- `retry_with_backoff`
- `parse_adf_to_text`
- `_load_automation_config` and config file semantics
- `determine_role`
- `extract_sla_details`
- `_get_closure_info`
- `_fetch_all_keys_jql` (but update the JQL construction — see below)
- `_fetch_comments`
- `_fetch_worklog` (keep for future on-demand use; don't call it in backfill)
- `_fetch_asset_details_sync`
- `_fetch_one_ticket` (will modify slightly — no worklog in backfill path)

**Add:**
- `_process_issue_to_ticket` returns a richer dict including the new fields listed below
- Top-level async function `fetch_ticket_batch(keys: list[str]) -> list[dict]` that takes keys and returns fully-processed ticket dicts ready for `transform.py`

**JQL construction** — don't use `cf[11709]` like AccountIntel. This app scopes by project, not by customer:
```python
def build_project_jql(project: str, updated_since: datetime | None = None,
                     lookback_days: int | None = None) -> str:
    parts = [f'project = {project}']
    if updated_since:
        iso = updated_since.strftime("%Y-%m-%d %H:%M")
        parts.append(f'updated >= "{iso}"')
    elif lookback_days:
        parts.append(f'updated >= -{lookback_days}d')
    return " AND ".join(parts) + " ORDER BY updated ASC"
```

Note: `ORDER BY updated ASC` is critical for resumability.

**Ticket dict returned by `_process_issue_to_ticket`** should have these fields (matching the DB schema — note no `security_level`):

```python
{
    "issue_key": str,
    "summary": str,
    "description": str,
    "status": str,
    "priority": str | None,
    "issue_type": str | None,
    "request_type": str | None,
    "is_customer_originated": bool,        # creator role == "Customer"
    "creator": {account_id, display_name, email, role, account_type},
    "reporter": {...same shape...},
    "assignee": {...same shape... or None},
    "jira_org_id": str | None,
    "jira_org_name": str | None,
    "ocean_client_id": int | None,          # from customfield_11709
    "labels": list[str],
    "sla_first_response": {breached, elapsed_seconds, threshold_seconds} | None,
    "sla_resolution": {...same...} | None,
    "created_at": datetime,
    "updated_at": datetime,
    "resolved_at": datetime | None,         # from _get_closure_info
    "thread_events": [
        {id, created_at, role, author, author_account_id, author_email,
         is_public, body, kind}
    ],
    "assets": [
        {object_id, workspace_id, asset_name, service_id}
    ],
}
```

### `jsm_sync/transform.py`

Thin module that converts the dict from `_process_issue_to_ticket` into the specific tuples/records needed by `db.py` upserts. Main function:

```python
from dataclasses import dataclass


@dataclass
class TransformedTicket:
    ticket_row: dict             # fields for tickets table
    users: list[dict]            # creator, reporter, assignee (dedup'd)
    organization: dict | None    # from jira_org_id + name + ocean_client_id
    thread_events: list[dict]    # rows for thread_events
    assets: list[dict]           # rows for assets
    ticket_asset_links: list[tuple[str, str]]  # (issue_key, object_id)


def transform_ticket(raw: dict) -> TransformedTicket:
    """Convert a processed Jira ticket dict into DB-ready records."""
    # Build the ticket_row dict matching tickets table columns
    # Deduplicate users (creator + reporter + assignee, skipping None)
    # Extract org
    # Flatten thread_events — each event already matches the schema
    # Flatten assets
    # Build link list
    ...
```

The transform layer exists so `db.py` upsert functions can take simple dicts, not raw Jira JSON. Makes the sync code easier to test without hitting Jira.

### `jsm_sync/db.py`

asyncpg connection pool and one upsert function per table. Key design choices:

- **Single connection pool as a module-level singleton.** Initialize once, reuse.
- **Transaction per ticket.** Each ticket (plus its users, org, comments, assets) is one transaction. If the transaction fails, that ticket gets logged and skipped; other tickets continue.
- **Upsert uses `ON CONFLICT DO UPDATE` with a `WHERE updated_at <= EXCLUDED.updated_at` guard where it makes sense.** Prevents unnecessary writes if the row hasn't actually changed.
- **`synced_at` is always set to `NOW()` on upsert.**

Functions to implement:

```python
async def init_pool() -> None: ...
async def close_pool() -> None: ...
async def get_pool() -> asyncpg.Pool: ...

async def upsert_user(conn, user: dict) -> None: ...
async def upsert_organization(conn, org: dict) -> None: ...
async def upsert_ticket(conn, ticket_row: dict) -> None: ...
async def upsert_thread_events(conn, issue_key: str, events: list[dict]) -> None: ...
async def upsert_assets(conn, assets: list[dict]) -> None: ...
async def upsert_ticket_asset_links(conn, links: list[tuple[str, str]]) -> None: ...

async def persist_ticket(transformed: TransformedTicket) -> None:
    """One transaction: users, org, ticket, thread_events, assets, links."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            for u in transformed.users:
                await upsert_user(conn, u)
            if transformed.organization:
                await upsert_organization(conn, transformed.organization)
            await upsert_ticket(conn, transformed.ticket_row)
            await upsert_thread_events(conn, transformed.ticket_row["issue_key"],
                                       transformed.thread_events)
            await upsert_assets(conn, transformed.assets)
            await upsert_ticket_asset_links(conn, transformed.ticket_asset_links)

async def get_sync_cursor(source: str) -> datetime | None: ...
async def set_sync_cursor(source: str, cursor: datetime, status: str = "running") -> None: ...
async def mark_sync_complete(source: str) -> None: ...
async def mark_sync_error(source: str, error: str) -> None: ...
```

#### Example upsert SQL for tickets

```sql
INSERT INTO tickets (
    issue_key, summary, description, status, priority, issue_type,
    request_type, is_customer_originated,
    creator_account_id, reporter_account_id, assignee_account_id,
    jira_org_id, ocean_client_id, labels,
    sla_first_response_breached, sla_first_response_elapsed_s, sla_first_response_threshold_s,
    sla_resolution_breached, sla_resolution_elapsed_s, sla_resolution_threshold_s,
    created_at, updated_at, resolved_at, synced_at
) VALUES (
    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14,
    $15, $16, $17, $18, $19, $20, $21, $22, $23, NOW()
)
ON CONFLICT (issue_key) DO UPDATE SET
    summary = EXCLUDED.summary,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    priority = EXCLUDED.priority,
    issue_type = EXCLUDED.issue_type,
    request_type = EXCLUDED.request_type,
    is_customer_originated = EXCLUDED.is_customer_originated,
    creator_account_id = EXCLUDED.creator_account_id,
    reporter_account_id = EXCLUDED.reporter_account_id,
    assignee_account_id = EXCLUDED.assignee_account_id,
    jira_org_id = EXCLUDED.jira_org_id,
    ocean_client_id = EXCLUDED.ocean_client_id,
    labels = EXCLUDED.labels,
    sla_first_response_breached = EXCLUDED.sla_first_response_breached,
    sla_first_response_elapsed_s = EXCLUDED.sla_first_response_elapsed_s,
    sla_first_response_threshold_s = EXCLUDED.sla_first_response_threshold_s,
    sla_resolution_breached = EXCLUDED.sla_resolution_breached,
    sla_resolution_elapsed_s = EXCLUDED.sla_resolution_elapsed_s,
    sla_resolution_threshold_s = EXCLUDED.sla_resolution_threshold_s,
    updated_at = EXCLUDED.updated_at,
    resolved_at = EXCLUDED.resolved_at,
    synced_at = NOW(),
    deleted_at = NULL
WHERE tickets.updated_at <= EXCLUDED.updated_at;
```

`upsert_user` should bump `last_seen_at` on every upsert but preserve `first_seen_at`. Similar for `organizations`. `upsert_thread_events` should batch-insert using `executemany` or `copy_records_to_table`.

### `jsm_sync/backfill.py`

Main orchestrator. Rough structure:

```python
"""
Backfill APTUM tickets to Postgres.

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
from .db import init_pool, close_pool, persist_ticket, \
    get_sync_cursor, set_sync_cursor, mark_sync_complete, mark_sync_error
from .jira_client import _auth_headers, fetch_ticket_batch, _fetch_all_keys_jql, \
    build_project_jql
from .transform import transform_ticket

logger = logging.getLogger(__name__)

SOURCE_NAME = "jira_tickets"
BATCH_SIZE = 20


async def run_backfill(lookback_days: int, batch_size: int) -> None:
    await init_pool()
    try:
        cursor = await get_sync_cursor(SOURCE_NAME)
        if cursor:
            logger.info(f"Resuming from cursor {cursor}")
            jql = build_project_jql(settings.jira_project, updated_since=cursor)
        else:
            logger.info(f"Starting fresh backfill with {lookback_days}d lookback")
            jql = build_project_jql(settings.jira_project, lookback_days=lookback_days)

        await set_sync_cursor(SOURCE_NAME, cursor or datetime.now(timezone.utc),
                              status="running")

        async with httpx.AsyncClient() as client:
            headers = _auth_headers()
            semaphore = asyncio.Semaphore(settings.jira_semaphore_limit)

            all_keys = await _fetch_all_keys_jql(client, jql, semaphore, headers)
            logger.info(f"Scout found {len(all_keys)} tickets to process")

            for i in range(0, len(all_keys), batch_size):
                batch = all_keys[i:i + batch_size]
                logger.info(f"Processing batch {i // batch_size + 1} "
                            f"({i + 1}-{min(i + batch_size, len(all_keys))} of {len(all_keys)})")

                tickets = await fetch_ticket_batch(client, batch, semaphore, headers)

                max_updated = None
                for ticket in tickets:
                    if not ticket:
                        continue
                    try:
                        transformed = transform_ticket(ticket)
                        await persist_ticket(transformed)
                        if max_updated is None or ticket["updated_at"] > max_updated:
                            max_updated = ticket["updated_at"]
                    except Exception as e:
                        logger.error(f"Failed to persist {ticket.get('issue_key')}: {e}",
                                     exc_info=True)

                if max_updated:
                    await set_sync_cursor(SOURCE_NAME, max_updated, status="running")
                    logger.info(f"Checkpointed cursor at {max_updated}")

        await mark_sync_complete(SOURCE_NAME)
        logger.info("Backfill complete")

    except Exception as e:
        logger.error(f"Backfill failed: {e}", exc_info=True)
        await mark_sync_error(SOURCE_NAME, str(e))
        raise
    finally:
        await close_pool()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--lookback-days", type=int, default=settings.jira_lookback_days)
    p.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    args = p.parse_args()

    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    asyncio.run(run_backfill(args.lookback_days, args.batch_size))


if __name__ == "__main__":
    main()
```

### `jsm_sync/incremental.py`

Very similar to `backfill.py` but always resumes from cursor, and doesn't have a `--lookback-days` option.

Key additional behavior vs backfill:

- If `sync_state.status == "running"`, log a warning and exit (another instance is active).
- If cursor is NULL (meaning backfill never ran), log an error and exit with hint to run `python -m jsm_sync.backfill` first.
- After successful run, always set cursor to `max(updated_at seen) + some slop` (1 minute) to handle Jira eventual consistency.

### `jsm_sync/reconcile.py`

Weekly full-list diff to catch deletes. Low priority for v1; stub it out but don't block on implementing.

### `README.md`

Brief, practical. Should cover:

- What this is (one paragraph)
- Prerequisites (Docker, Python 3.12+, a Jira API token)
- Setup steps (clone, cp .env.example .env, edit .env, docker compose up -d, pip install -r requirements.txt)
- How to run the backfill
- How to run incremental (and a sample crontab line)
- How to check progress (sample SQL queries)
- Troubleshooting tips

### `config/jira_automation_users.json`

Copy verbatim from Adam's existing file. The content is also available as the fallback dict in `_load_automation_config` inside the original `jiraClient.py`.

---

## Step-by-step execution order for Claude Code

Execute in this exact order. After each step, stop and verify before moving to the next.

### Step 1 — Scaffold the repo

Create all directories and empty files. Create `.gitignore`, `.env.example`, `docker-compose.yml`, `requirements.txt`, `README.md`, `schema/001_initial.sql`.

**Verify:** `tree -L 2 -I 'postgres_data|__pycache__|.venv'` shows the expected structure.

### Step 2 — First Git commit

```bash
git init
git add .gitignore .env.example docker-compose.yml requirements.txt README.md PLAN.md DIAGRAMS.md schema/
git status   # verify no .env, no postgres_data
git commit -m "Initial project scaffold"
```

**Verify:** `git log --oneline` shows one commit. `git status` is clean.

### Step 3 — Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Verify:** `pip list` shows httpx, asyncpg, pydantic, pydantic-settings, python-dotenv, python-dateutil.

### Step 4 — Postgres container and schema

Adam copies `.env.example` to `.env`, fills in real Jira credentials, sets `JIRA_USERNAME=adam.nelson@aptum.com`.

```bash
docker compose up -d
docker compose logs -f postgres   # wait for "database system is ready to accept connections", then Ctrl-C
```

**Verify:**
```bash
docker compose exec postgres psql -U jsm_sync -d jsm_sync -c "\dt"
```
Should list: `assets`, `jira_users`, `organizations`, `sync_state`, `thread_events`, `ticket_assets`, `tickets`.

```bash
docker compose exec postgres psql -U jsm_sync -d jsm_sync -c "SELECT * FROM sync_state;"
```
Should show one row: `jira_tickets | NULL | NULL | idle | NULL`.

### Step 5 — Port the Jira client

Create `jsm_sync/__init__.py`, `jsm_sync/config.py`, then `jsm_sync/jira_client.py`. Port from Adam's existing `jiraClient.py` following the "Remove / Change / Keep / Add" instructions above. Create `config/jira_automation_users.json` in the project root.

**Verify with a throwaway script:**
```python
# scratch_verify_client.py
import asyncio, httpx, logging
logging.basicConfig(level=logging.INFO)
from jsm_sync.config import settings
from jsm_sync.jira_client import _auth_headers, _fetch_one_ticket

async def main():
    async with httpx.AsyncClient() as c:
        sem = asyncio.Semaphore(1)
        ticket = await _fetch_one_ticket(c, "APTUM-57617", sem, _auth_headers())
        print(ticket["summary"], ticket["is_customer_originated"])
        print("Thread events:", len(ticket["thread_events"]))
        for e in ticket["thread_events"]:
            print(f"  [{e['role']}] is_public={e['is_public']} - {e['body'][:60]}")

asyncio.run(main())
```

Expected output: `juniper vpn error True`, three thread events all public.

Then delete `scratch_verify_client.py` — don't commit it.

### Step 6 — Transform and DB layers

Create `jsm_sync/transform.py` and `jsm_sync/db.py`.

**Verify db.py independently:**
```python
# scratch_verify_db.py
import asyncio
from jsm_sync.db import init_pool, close_pool, get_pool, upsert_user

async def main():
    await init_pool()
    pool = await get_pool()
    async with pool.acquire() as conn:
        await upsert_user(conn, {
            "account_id": "test:dummy",
            "display_name": "Test User",
            "email": "test@example.com",
            "role": "Customer",
            "account_type": "customer",
        })
        row = await conn.fetchrow("SELECT * FROM jira_users WHERE account_id = 'test:dummy'")
        print(dict(row))
        await conn.execute("DELETE FROM jira_users WHERE account_id = 'test:dummy'")
    await close_pool()

asyncio.run(main())
```

Then delete the scratch file.

### Step 7 — Wire up backfill

Create `jsm_sync/backfill.py` and `jsm_sync/incremental.py` (stub the latter is fine).

**Verify with a tiny lookback first:**
```bash
python -m jsm_sync.backfill --lookback-days 1
```

This should complete in a couple of minutes. Watch the logs for errors.

Spot check:
```sql
SELECT COUNT(*) FROM tickets;
SELECT COUNT(*) FROM thread_events;
SELECT COUNT(*) FROM jira_users;
SELECT COUNT(*) FROM organizations;
SELECT COUNT(*) FROM assets;

SELECT issue_key, summary, status, is_customer_originated, jira_org_id
FROM tickets
WHERE issue_key = 'APTUM-57617';

SELECT t.issue_key, t.summary, COUNT(te.id) AS thread_count
FROM tickets t LEFT JOIN thread_events te ON te.issue_key = t.issue_key
GROUP BY t.issue_key, t.summary
ORDER BY thread_count DESC LIMIT 10;
```

### Step 8 — Full 30-day backfill

```bash
python -m jsm_sync.backfill --lookback-days 30
```

This is the real run. Expect it to take 30-90 minutes. If it crashes, re-run — resumability picks up from the cursor.

Verify final state:
```sql
SELECT
  (SELECT COUNT(*) FROM tickets) AS tickets,
  (SELECT COUNT(*) FROM tickets WHERE is_customer_originated) AS customer_tickets,
  (SELECT COUNT(*) FROM thread_events) AS comments,
  (SELECT COUNT(*) FROM thread_events WHERE is_public = true) AS public_comments,
  (SELECT COUNT(*) FROM jira_users) AS users,
  (SELECT COUNT(*) FROM organizations) AS orgs,
  (SELECT COUNT(*) FROM assets WHERE service_id IS NOT NULL) AS assets_with_service_id;

SELECT status, last_sync_at, last_cursor FROM sync_state;
```

### Step 9 — Second commit

```bash
git add jsm_sync/ config/
git status
git commit -m "Initial 30-day APTUM backfill working"
```

### Step 10 — Incremental sync

Flesh out `incremental.py` following the same pattern as `backfill.py` but always cursor-driven.

Document the cron line in README:

```
*/10 * * * * cd /path/to/jsm-sync && /path/to/.venv/bin/python -m jsm_sync.incremental >> logs/incremental.log 2>&1
```

---

## Verification queries Adam might want

**How many APTUM tickets in the last 30 days, split by originator:**
```sql
SELECT
  CASE WHEN is_customer_originated THEN 'Customer' ELSE 'Internal/Auto' END AS source,
  COUNT(*)
FROM tickets
WHERE created_at >= NOW() - INTERVAL '30 days'
  AND deleted_at IS NULL
GROUP BY 1;
```

**Top 10 most active orgs in the last 30 days:**
```sql
SELECT o.name, COUNT(t.issue_key) AS tickets
FROM organizations o
JOIN tickets t ON t.jira_org_id = o.jira_org_id
WHERE t.created_at >= NOW() - INTERVAL '30 days'
  AND t.deleted_at IS NULL
GROUP BY o.name
ORDER BY tickets DESC
LIMIT 10;
```

**Full thread for a specific ticket:**
```sql
SELECT te.created_at, u.role, u.display_name, te.is_public,
       SUBSTRING(te.body, 1, 100) AS snippet
FROM thread_events te
LEFT JOIN jira_users u ON u.account_id = te.author_account_id
WHERE te.issue_key = 'APTUM-57617'
ORDER BY te.created_at;
```

**Tickets that mention a specific service ID anywhere:**
```sql
SELECT DISTINCT t.issue_key, t.summary
FROM tickets t
JOIN thread_events te ON te.issue_key = t.issue_key
WHERE te.body ILIKE '%7931672%' OR t.description ILIKE '%7931672%'
ORDER BY t.created_at DESC;
```

---

## What to NOT do in v1

- Do not add pgvector, tsvector, or trigram indexes yet. Add in `002_search_indexes.sql` later.
- Do not add Fusion DB sync yet. Separate project.
- Do not add FastAPI frontend. Data layer only.
- Do not add Prefect, Airflow, or any orchestrator. Cron is enough.
- Do not add webhooks. Polling works.
- Do not parse ADF beyond what `parse_adf_to_text` already does.
- Do not fetch worklogs during backfill.
- Do not over-index `tickets`.
- Do not use `alembic` for schema migrations yet.
- Do not add a `security_level` column. Adam doesn't use it. If internal-only filtering is ever needed, derive it from `request_type = 'Internal Incident'` at query time.

---

## Success criteria

1. `docker compose up -d` starts Postgres with the schema loaded.
2. `python -m jsm_sync.backfill --lookback-days 30` successfully populates Postgres with 30 days of APTUM tickets.
3. The backfill is resumable.
4. `python -m jsm_sync.incremental` runs idempotently on a schedule and keeps the mirror within ~15 minutes of Jira.
5. All the verification queries above return sensible results.
6. Adam can SSH into Postgres and run arbitrary SQL.
7. The repo is clean: no secrets, no `postgres_data/`, no `__pycache__/` in Git.

At that point, the next projects (persona-drafting app, AccountIntel refactor) can start — they just become Postgres consumers.
