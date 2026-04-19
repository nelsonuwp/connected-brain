# jsm-sync

Mirrors the APTUM Jira Service Management project into a local Postgres database so downstream tools (persona-drafting assistant, AccountIntel, ad-hoc SQL analysis) can run rapid queries without hitting Jira rate limits.

## Prerequisites

- Docker (for Postgres)
- Python 3.12+
- A Jira API token for `adam.nelson@aptum.com`

## Setup

```bash
# 1. Copy .env template (lives at repo root, shared with other projects)
#    Fill in POSTGRES_PASSWORD and confirm Jira creds are present
#    The .env is already at connected-brain/.env — no copy needed

# 2. Start Postgres
cd projects/jsm-sync
docker compose up -d
docker compose logs -f postgres   # wait for "ready to accept connections", then Ctrl-C

# 3. Verify schema loaded (expect tickets, thread_events, ticket_worklogs, …)
docker compose exec postgres psql -U jsm_sync -d jsm_sync -c "\dt"

# If postgres_data/ already existed before ticket_worklogs, apply migrations manually:
# docker compose exec postgres psql -U jsm_sync -d jsm_sync -f /docker-entrypoint-initdb.d/003_worklogs.sql
# (from host:) psql "postgresql://jsm_sync:…@localhost:5433/jsm_sync" -f schema/003_worklogs.sql

# 4. Install Python dependencies
pip install -r requirements.txt
```

## Running the backfill

```bash
# Quick sanity check — last 1 day
python -m jsm_sync.backfill --lookback-days 1

# Full 30-day backfill (30-90 min depending on volume)
python -m jsm_sync.backfill --lookback-days 30

# Safe to kill and re-run — resumes from last checkpoint
python -m jsm_sync.backfill --lookback-days 30

# Skip worklogs (faster; ticket_worklogs / global sweep stay stale)
python -m jsm_sync.backfill --lookback-days 30 --no-worklogs
```

## Worklog sync

Worklogs are stored per entry in `ticket_worklogs` (raw ADF in `comment_adf`). **Backfill** fetches `/issue/{key}/worklog` for every ticket. **Incremental** re-fetches worklogs for tickets in the JQL window **and** runs a global sweep (`/worklog/updated`, `/worklog/list`, `/worklog/deleted`) under a second cursor `sync_state.source = jira_worklogs`, so edits that do not bump the parent issue still sync.

- **Opt out:** `--no-worklogs` on both `backfill` and `incremental`.
- **First run after upgrading:** if `jira_worklogs.last_cursor` is null, run a backfill once (or your usual lookback) so the worklog cursor is pinned; incremental’s Phase B is a no-op until then.
- **Jira lag:** `/worklog/updated` and `/worklog/deleted` omit changes from roughly the last 60 seconds; combined with your incremental interval, expect worst-case ~interval+60s before a row appears in Postgres.
- **Progress / logs:** backfill and incremental use Rich for a progress bar; `httpx` request lines are suppressed to WARNING so logs stay readable (including under launchd when stdout is a file).

## Running incremental sync

```bash
# Run once manually
python -m jsm_sync.incremental

# Opt out of worklogs for this run only
python -m jsm_sync.incremental --no-worklogs

# Schedule via cron (every 10 min)
*/10 * * * * cd /path/to/connected-brain/projects/jsm-sync && python3 -m jsm_sync.incremental >> logs/incremental.log 2>&1
```

## Checking progress

```sql
-- Overall counts
SELECT
  (SELECT COUNT(*) FROM tickets) AS tickets,
  (SELECT COUNT(*) FROM tickets WHERE is_customer_originated) AS customer_tickets,
  (SELECT COUNT(*) FROM thread_events) AS comments,
  (SELECT COUNT(*) FROM thread_events WHERE is_public = true) AS public_comments,
  (SELECT COUNT(*) FROM ticket_worklogs WHERE deleted_at IS NULL) AS worklogs,
  (SELECT COUNT(*) FROM jira_users) AS users,
  (SELECT COUNT(*) FROM organizations) AS orgs;

-- Sync state
SELECT source, status, last_sync_at, last_cursor FROM sync_state;

-- Top 10 orgs by ticket volume (last 30 days)
SELECT o.name, COUNT(t.issue_key) AS tickets
FROM organizations o
JOIN tickets t ON t.jira_org_id = o.jira_org_id
WHERE t.created_at >= NOW() - INTERVAL '30 days' AND t.deleted_at IS NULL
GROUP BY o.name ORDER BY tickets DESC LIMIT 10;
```

## Connect to Postgres

```bash
docker compose exec postgres psql -U jsm_sync -d jsm_sync
```

Or from any SQL client: `host=localhost port=5433 dbname=jsm_sync user=jsm_sync` (see `docker-compose.yml` for the published port).

## Troubleshooting

**Backfill stalls / 429 errors** — Jira rate limit. Reduce `JIRA_SEMAPHORE_LIMIT` in `.env` (default 5). The retry-with-backoff logic handles transient 429s automatically.

**`Connection refused` on DATABASE_URL** — Postgres container isn't running. `docker compose up -d`.

**Schema not loaded** — Only runs on first boot. If `postgres_data/` already exists, the init scripts are skipped. To re-run: `docker compose down -v && rm -rf postgres_data/ && docker compose up -d`.

**`ModuleNotFoundError: No module named 'jsm_sync'`** — Must run from `projects/jsm-sync/` with the venv activated.
