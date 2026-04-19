# ops-agent

Local web app that reads from the `jsm-sync` Postgres mirror and lets you browse APTUM tickets, auto-classify them into workflow patterns, and generate persona-matched draft responses using OpenRouter (Claude Sonnet via the workhorse model).

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

# Verify
docker compose -f ../jsm-sync/docker-compose.yml exec postgres \
    psql -U jsm_sync -d jsm_sync -c "\dt ops.*"
# → ops.draft_log
```

## Running

```bash
./run.sh
```

Open http://127.0.0.1:8080/tickets

## What you get

- **Ticket list** — browse all APTUM tickets from Postgres with filters (status, customer-originated, search)
- **Ticket detail** — full thread with author roles and public/private flags, assets, linked org
- **Generate Draft** — one click on a matched pattern ticket produces a persona-matched close-out comment in the assigned engineer's voice, logged to `ops.draft_log`
- **Copy to clipboard** — paste directly into Jira

## Patterns (v1)

| Pattern | Slug | Matches |
|---|---|---|
| Firewall Upgrade Close-out | `firewall_upgrade` | Summary contains "firewall" + "upgrade"/"cutover"/"firmware" |

Adding a new pattern = one new file in `ops_agent/patterns/` + one import line in `__init__.py`.

## LLM

Uses OpenRouter with `MODEL_WORKHORSE` (default: `anthropic/claude-sonnet-4-5`) and `TEMPERATURE_WORKHORSE` from the root `.env`. No streaming — full response rendered at once.

## Troubleshooting

**`Connection refused` on DATABASE_URL** — jsm-sync Postgres isn't running. `docker compose -f ../jsm-sync/docker-compose.yml up -d`

**`OPENROUTER_API_KEY not set`** — Fill in the key in `connected-brain/.env`

**`No pattern matched`** — Expected for tickets that don't fit any known pattern. The classifier badge shows `(unclassified)`.

**`No examples found`** — The assigned engineer has no past public comments on matching tickets in the 30-day corpus. Run a longer backfill or assign a different engineer.
