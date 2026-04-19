# ops-agent

Local web app that reads from the `jsm-sync` Postgres mirror, loads **T-shaped context** (customer ticket history from Postgres, hardware components and neighbors from MSSQL `dimComponents`, service/customer facts from Fusion PostgreSQL), and runs **OpenRouter**-backed drafts: potential fix analysis, internal comment, or public customer reply with a **role persona** you choose (editable system prompt).

## Project layout

- **`ops_agent/`** (underscore) — Python package (FastAPI app, routes, templates).
- **`docs/`** — specs and diagrams (`docs/ops-agent-PLAN-v2.md` is the current v2 plan). There is no `ops-agent/ops-agent/` nested project folder; hyphen vs underscore distinguishes the repo folder from the importable package.

## Prerequisites

- `jsm-sync` Postgres container running (`docker compose -f ../jsm-sync/docker-compose.yml up -d`)
- `jsm-sync` backfill has run at least once (`python -m jsm_sync.backfill --lookback-days 30`)
- `OPENROUTER_API_KEY` set in `connected-brain/.env`
- Python 3.12+ with deps installed

## Setup

```bash
cd projects/ops-agent

# Install deps
pip install -r requirements.txt

# Apply ops-agent's own schema to the shared Postgres
docker compose -f ../jsm-sync/docker-compose.yml exec -T postgres \
    psql -U jsm_sync -d jsm_sync < schema/001_ops_agent_tables.sql

# Verify + apply v2 draft_log columns
docker compose -f ../jsm-sync/docker-compose.yml exec postgres \
    psql -U jsm_sync -d jsm_sync -c "\dt ops.*"
# → ops.draft_log

docker compose -f ../jsm-sync/docker-compose.yml exec -T postgres \
    psql -U jsm_sync -d jsm_sync < schema/002_draft_log_v2.sql
```

## Running

```bash
./run.sh
```

Open http://127.0.0.1:8080/tickets

## Connection smoke tests (option 3)

After `pip install -r requirements.txt`, from `projects/ops-agent`:

```bash
# MSSQL BI (DM_BusinessInsights) — direct LAN; needs MSSQL_BI_* in root .env
python3 -m ops_agent.mssql

# Fusion PostgreSQL — SSH tunnel + Fusion creds + SSH_USER/SSH_PASS
python3 -m ops_agent.fusion
```

These are read-only probes. They exit `0` on success and `1` on failure (missing env, network, or auth).

## What you get

- **Ticket list** — browse APTUM tickets from Postgres (filters: status, customer-originated, search)
- **Ticket detail** — two-column layout: thread + **Related context** sidebar (HTMX-loaded): customer history, `dimComponents` slice, neighbor services, tickets on similar hardware, Fusion `customer_products` rows for linked services
- **LLM actions** — (1) Identify potential fix, (2) Generate internal comment, (3) Generate public comment with persona dropdown + editable system prompt; all logged to `ops.draft_log` with `draft_type`
- **Copy to clipboard** on generated drafts

## Validate T-context (CLI)

```bash
cd projects/ops-agent
python3 -m ops_agent.validate_context APTUM-38273
```

Requires running Postgres (`jsm_sync`), Fusion SSH + creds, and MSSQL BI in root `.env`.

## LLM

Uses OpenRouter with `MODEL_WORKHORSE` (default: `anthropic/claude-sonnet-4-5`) and `TEMPERATURE_WORKHORSE` from the root `.env`. No streaming — full response rendered at once.

## Troubleshooting

**`Connection refused` on DATABASE_URL** — jsm-sync Postgres isn't running. `docker compose -f ../jsm-sync/docker-compose.yml up -d`

**`OPENROUTER_API_KEY not set`** — Fill in the key in `connected-brain/.env`

**Related context stuck on “Loading”** — Check browser devtools / server logs; Fusion tunnel or MSSQL must be reachable.

**`INSERT` into `draft_log` fails** — Apply `schema/002_draft_log_v2.sql` (adds nullable `pattern_slug` + new columns).
