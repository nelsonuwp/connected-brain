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

# 3. Verify schema loaded (7 tables expected)
docker compose exec postgres psql -U jsm_sync -d jsm_sync -c "\dt"

# 4. Create Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the backfill

```bash
# Activate venv first
source .venv/bin/activate

# Quick sanity check — last 1 day
python -m jsm_sync.backfill --lookback-days 1

# Full 30-day backfill (30-90 min depending on volume)
python -m jsm_sync.backfill --lookback-days 30

# Safe to kill and re-run — resumes from last checkpoint
python -m jsm_sync.backfill --lookback-days 30
```

## Running incremental sync

```bash
# Run once manually
python -m jsm_sync.incremental

# Schedule via cron (every 10 min)
*/10 * * * * cd /path/to/connected-brain/projects/jsm-sync && .venv/bin/python -m jsm_sync.incremental >> logs/incremental.log 2>&1
```

## Checking progress

```sql
-- Overall counts
SELECT
  (SELECT COUNT(*) FROM tickets) AS tickets,
  (SELECT COUNT(*) FROM tickets WHERE is_customer_originated) AS customer_tickets,
  (SELECT COUNT(*) FROM thread_events) AS comments,
  (SELECT COUNT(*) FROM thread_events WHERE is_public = true) AS public_comments,
  (SELECT COUNT(*) FROM jira_users) AS users,
  (SELECT COUNT(*) FROM organizations) AS orgs;

-- Sync state
SELECT status, last_sync_at, last_cursor FROM sync_state;

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

Or from any SQL client: `host=localhost port=5432 dbname=jsm_sync user=jsm_sync`

## Troubleshooting

**Backfill stalls / 429 errors** — Jira rate limit. Reduce `JIRA_SEMAPHORE_LIMIT` in `.env` (default 5). The retry-with-backoff logic handles transient 429s automatically.

**`Connection refused` on DATABASE_URL** — Postgres container isn't running. `docker compose up -d`.

**Schema not loaded** — Only runs on first boot. If `postgres_data/` already exists, the init scripts are skipped. To re-run: `docker compose down -v && rm -rf postgres_data/ && docker compose up -d`.

**`ModuleNotFoundError: No module named 'jsm_sync'`** — Must run from `projects/jsm-sync/` with the venv activated.
