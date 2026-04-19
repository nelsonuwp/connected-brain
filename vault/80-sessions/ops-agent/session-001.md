---
type: re-anchor
project: jsm-sync + ops-agent
session: 001
date: 2026-04-18
previous: none
context-blocks-used: []
---

# Re-anchor — jsm-sync + ops-agent (T-context v2)

> Read this **before** touching either project. The next LLM is likely to
> assume these projects are early-stage — they are not. Both are built,
> running, and architecturally past several rounds of redesign. Do not
> re-litigate decisions marked "**DO NOT CHANGE**" below without explicit
> user approval.

---

## TL;DR

Two cooperating projects live at the repo root:

- `projects/jsm-sync/` — Python service that mirrors Jira Service Management
  (tickets, comments, users, orgs, assets) into a local Postgres container.
  Bypasses Jira rate limits. Has `backfill.py`, `incremental.py`,
  `reconcile.py`.
- `projects/ops-agent/` — FastAPI + HTMX web app that consumes the
  `jsm-sync` Postgres data, enriches each ticket with a **T-shaped context**
  (vertical = customer history, horizontal = similar hardware), and drafts
  LLM responses using **role-based personas** via **OpenRouter**.

Both projects read the **root `.env`** at `/Users/anelson-macbook-air/connected-brain/.env`.
Nothing uses `venv` — everything runs native Python 3.14 from Homebrew.

State right now: the code is complete for v2 and validated with a live
ticket (`APTUM-38273`). The app runs, the related-context sidebar renders
enriched data, and drafts generate successfully via OpenRouter. The **only
pending work** is running the 18-month historical backfill and wiring the
incremental sync to cron.

---

## Architecture — DO NOT CHANGE without asking

### Data authority (which system is the source of truth for what)

| Thing | Source of truth | Notes |
|---|---|---|
| Tickets, comments, thread events, users, orgs, assets | Local Postgres `jsm_sync` schema (mirrored from Jira) | Fast, rate-limit-free reads. |
| Customer identity, company name, all services (active AND cancelled), TAM/CSM | Fusion PG (`fusion` db on `db1.peer1.com` via SSH tunnel) | `customer_products` is **the** services table. `dimServices` in MSSQL hides cancelled services — do not use it for service lookup. |
| Hardware component details (CPU, RAM, disk, model, etc.) | MSSQL BI `DM_BusinessInsights.dimComponents` (`10.121.21.211`) | Component rows keyed by `component_id` (= "fusion_id" in the user's mental model). |
| LLM calls | **OpenRouter** (`OPENROUTER_API_KEY` in root `.env`) | Model = `MODEL_WORKHORSE`, temp = `TEMPERATURE_WORKHORSE`. **Not Anthropic direct.** |

### T-shaped context (the core idea behind ops-agent v2)

For any open ticket, we build a `TContextView` that contains:

- **Vertical** — last N tickets from the same customer (`ocean_client_id`).
- **Horizontal** — services whose component fingerprint overlaps the
  current ticket's services (Jaccard similarity on the set of
  `component_id`s in `dimComponents`). Then the tickets against those
  neighbor services.
- **Customer facts from Fusion** — company name, all services (active +
  cancelled), TAM/CSM if the TAM join succeeds.
- **Hardware facts from MSSQL** — the component rows for this ticket's
  services, plus labels (product name, company name) applied from Fusion.

This all lives in `ops_agent/context/t_context.py`. The entry point is
`build_t_context(issue_key)`. Use the CLI `python3 -m ops_agent.validate_context <ISSUE_KEY>`
to inspect without starting the web server.

### Personas (not per-engineer voice)

v1 used per-engineer past-comment corpora to mimic individual voices. That
was dropped. v2 uses **canned role personas** defined in YAML at
`ops_agent/personas/*.yaml`:

- `l2_support`
- `l3_engineer`
- `account_manager`
- `executive`

The persona system prompt is built from YAML and **displayed in the UI as
an editable textarea** for the public-comment flow, so the user can tweak
tone per draft. Do not re-add per-engineer classification.

### Three draft flows

Not one "generate response" button. Three distinct actions:

1. **Identify potential fix** (`POST /tickets/{key}/draft/fix`) — internal
   diagnostic suggestion. No persona.
2. **Draft internal comment** (`POST /tickets/{key}/draft/internal`) —
   private engineering note. No persona.
3. **Draft public comment** (`POST /tickets/{key}/draft/public`) — customer-
   facing. **Takes `persona_slug` and an editable `system_prompt` from the form.**

All three write to `ops.draft_log` with `draft_type`, `persona_slug`, and
`system_prompt_override`. `pattern_slug` is nullable now (v1 leftover).

### Folder layout — the "reciprocal" gotcha

There is a deliberate difference that looks like a duplicate:

- `projects/ops-agent/` — the project root (dashes).
- `projects/ops-agent/ops_agent/` — the Python package (underscores).

This is correct and Pythonic. Earlier in the session the user flagged a
genuinely duplicated `ops-agent/ops-agent/` — that was fixed by moving
planning docs into `projects/ops-agent/docs/`. Don't "fix" the dash-vs-
underscore pair.

### No venv. Ever.

Explicit user rule: **do not create or reference any `venv`/`.venv`** for
any project in this repo. Everything runs with system Python 3
(`/opt/homebrew/bin/python3`, 3.14.1). Package installs are global.
`.gitignore` intentionally omits `venv` entries.

### Root .env is shared; project .env.example stubs the subset each project needs

All secrets live in `/Users/anelson-macbook-air/connected-brain/.env`. Both
`jsm-sync` and `ops-agent` use `pydantic-settings` with `env_file` pointed
at the repo root. Do not create per-project `.env` files.

---

## Key naming renames (critical, recent, easy to miss)

These were renamed during this session. Both names still work via
`AliasChoices`, but **write new code against the new names**:

| Old (avoid) | New (use this) | Where |
|---|---|---|
| `OCEAN_DB_SERVER` / `_NAME` / `_USERNAME` / `_PASSWORD` | `MSSQL_BI_SERVER` / `_NAME` / `_USER` / `_PASS` | root `.env`, `ops_agent/config.py`, `projects/_shared/config.py`, MSSQL connectors in `db-sync` and `cpq-replacement-db-only` |
| `SSH_USERNAME` / `SSH_PASSWORD` | `SSH_USER` / `SSH_PASS` | root `.env`, any SSH tunnel code |

"Ocean" as a term is **dead**. The actual data source is MSSQL BI. Fusion
is a separate Postgres.

New additions (no alias, new only):

- `FUSION_DB_SERVER`, `FUSION_DB_PORT`, `FUSION_DB_NAME`, `FUSION_DB_USER`, `FUSION_DB_PASS`
  — Fusion PG readonly (`sb_readonly` user). Reached via SSH tunnel using
  the `SSH_*` creds.

---

## What works (confirmed)

### jsm-sync

- Docker Postgres container runs (`docker compose up -d` from
  `projects/jsm-sync/`).
- Schema at `schema/001_initial.sql` applied.
- `jsm_sync.backfill`, `jsm_sync.incremental`, `jsm_sync.reconcile` all
  import and run under Python 3.14.
- Cursor-based resumable backfill with checkpointing into `sync_state`.
- `.env` lives at repo root; `config.py` reads it with
  `env_file=_REPO_ROOT / ".env"`.

### ops-agent

- FastAPI app boots at `http://127.0.0.1:8080`. Start with:
  ```
  cd projects/ops-agent
  ./run.sh
  ```
- Ticket list and detail pages render (`/tickets`, `/tickets/{key}`).
- The right-hand sidebar lazy-loads via HTMX (`hx-get="/tickets/{key}/related"`)
  and shows: Customer, Customer ticket history, Hardware components,
  Neighbor services, Tickets on similar hardware, Fusion services for the
  current ticket. **Each row is enriched with product name + company name**
  where Fusion returns them.
- Three draft flows call OpenRouter and write to `ops.draft_log`. Verified
  end-to-end on `APTUM-38273`.
- MSSQL BI connection via `pymssql` — smoke-tested through
  `python3 -m ops_agent.mssql`.
- Fusion PG connection via `sshtunnel` + `psycopg2` pool, managed by
  FastAPI `lifespan` (`fusion_conn.start_fusion()` / `stop_fusion()`).
  Paramiko `TripleDES` deprecation warning is intentionally suppressed in
  `fusion_conn.py`.
- `schema/002_draft_log_v2.sql` applied: adds `draft_type`, `persona_slug`,
  `system_prompt_override`; drops NOT NULL on `pattern_slug`.

### Root-level

- `.gitignore`, `.env`, `.env.example` live at the repo root only — not
  inside any subproject.
- `projects/_shared/config.py`, `projects/db-sync/connectors/mssql.py`, and
  `projects/cpq-replacement-db-only/connectors/mssql.py` all updated to
  prefer the new `MSSQL_BI_*` / `SSH_USER` / `SSH_PASS` names while keeping
  aliases for the old names.

---

## What doesn't / what's pending

### 1. 18-month jsm-sync backfill (in progress / may not have started)

The user attempted the backfill kickoff, but a zsh paste got stuck in a
`dquote>` continuation and **nothing actually ran** (`jsm-sync/logs/` may
still be empty or only have prior small-lookback runs).

The intended command sequence is:

```bash
cd /Users/anelson-macbook-air/connected-brain/projects/jsm-sync

# reset the cursor so --lookback-days is honored
docker compose exec -T postgres psql -U jsm_sync -d jsm_sync -c \
  "UPDATE sync_state SET last_cursor=NULL, status='idle', last_error=NULL, updated_at=NOW() WHERE source='jira_tickets';"

mkdir -p logs
nohup python3 -m jsm_sync.backfill --lookback-days 540 --batch-size 50 \
  > logs/backfill-18mo.log 2>&1 &
```

Verify running: `pgrep -fl jsm_sync.backfill` and `tail -f logs/backfill-18mo.log`.

Only flip to incremental/cron **after** the backfill completes
(`sync_state.status = 'idle'` and `last_cursor` populated).

### 2. Cron job for `jsm_sync.incremental` — not yet installed

Plan given to the user, not yet installed in their crontab:

```cron
*/10 * * * * cd /Users/anelson-macbook-air/connected-brain/projects/jsm-sync && /opt/homebrew/bin/python3 -m jsm_sync.incremental >> logs/incremental.log 2>&1
```

macOS gotchas to warn about:
- `/usr/sbin/cron` needs Full Disk Access in System Settings → Privacy &
  Security → Full Disk Access (press Cmd+Shift+G, add `/usr/sbin/cron`).
- Docker Desktop must auto-start at login (otherwise Postgres is down when
  cron fires).
- Use **absolute** `/opt/homebrew/bin/python3` — cron's PATH is minimal.

Open offer to the user: "add a `--reset-cursor` flag to `jsm_sync.backfill`
so they don't have to run the SQL reset by hand next time". Unanswered.

### 3. No systematic hardware-family similarity beyond Jaccard

Horizontal context is Jaccard similarity on shared `component_id`s. Good
enough for v2, but obvious future work: family-level grouping by product
name, weighting by component criticality (CPU > fan), etc. Don't do this
proactively — wait for a user ask.

---

## Things that already cost real time — read these before coding

1. **Starlette `TemplateResponse` API changed in 1.0.0.** The signature is
   `TemplateResponse(request, "name.html", context_dict)` — request is
   positional-first. Any new route that uses Jinja must use this form.
2. **`ops.draft_log.pattern_slug` was NOT NULL in v1.** v2 migration
   (`schema/002_draft_log_v2.sql`) drops that constraint. If you fork a new
   DB, apply both `001_ops_agent_tables.sql` and `002_draft_log_v2.sql`.
3. **Fusion `employees` columns** are `first_name`, `last_name`,
   `email_address` — **not** `employees_firstname` etc. The TAM join in
   `t_context._fusion_slice` is wrapped in try/except so a bad join doesn't
   kill the whole context view. Keep it that way.
4. **Package-relative imports everywhere** (`from .config import settings`).
   You MUST run these as modules (`python3 -m jsm_sync.incremental`,
   `python3 -m ops_agent.main` via uvicorn, etc.). Running the files
   directly by path will `ImportError`.
5. **Paramiko DeprecationWarning spam** about TripleDES is suppressed in
   `fusion_conn.py`. Don't "clean that up" — Paramiko still hasn't fixed
   it upstream.
6. **Do not add Anthropic SDK.** LLM calls go through OpenRouter
   (`ops_agent/llm.py`, async httpx wrapper). The model slug in `.env`
   happens to be `anthropic/claude-sonnet-4-5`, but it's via OpenRouter.

---

## Next session starts with

1. **Check if the 18-month backfill actually ran**:
   ```bash
   cd /Users/anelson-macbook-air/connected-brain/projects/jsm-sync
   pgrep -fl jsm_sync.backfill
   docker compose exec -T postgres psql -U jsm_sync -d jsm_sync -c \
     "SELECT source, status, last_cursor, last_sync_at FROM sync_state; \
      SELECT COUNT(*) FROM tickets;"
   tail -n 50 logs/backfill-18mo.log 2>/dev/null || echo "no log yet"
   ```
   If no process + cursor still NULL + no/old log → kick it off using the
   commands in **What doesn't → #1** above.

2. **Once backfill completes**, install the cron entry from **What
   doesn't → #2** via `crontab -e`. Watch `logs/incremental.log` for one
   or two cycles to confirm.

3. **Optional polish if user asks**: add `--reset-cursor` flag to
   `jsm_sync.backfill`. When present, it should run the `UPDATE
   sync_state SET last_cursor=NULL …` itself before the main loop, so the
   user doesn't need the SQL incantation. ~10 lines.

4. **Only if user raises it**: the MSSQL `dimComponents` horizontal-match
   is basic Jaccard. Family-level matching by product name is the obvious
   next step, but do not volunteer this — the v2 design is working and the
   user wants to stabilize it.

---

## Open questions

- Is Docker Desktop set to auto-start at login? (Needed for cron reliability.)
- Has the user granted Full Disk Access to `/usr/sbin/cron`? (Same reason.)
- Should we add a healthcheck endpoint to ops-agent that verifies MSSQL +
  Fusion + local PG are all reachable, so the user gets a fast smoke-test?
  (Not proactively — wait for an ask.)
- Does the user want launchd instead of cron for the incremental sync? I
  offered both; they haven't picked.

---

## Files the next LLM must know about

### jsm-sync
- `projects/jsm-sync/PLAN.md`, `DIAGRAMS.md`, `README.md`
- `projects/jsm-sync/jsm_sync/config.py` — settings, reads root .env
- `projects/jsm-sync/jsm_sync/jira_client.py` — adapted from `projects/_reference/clients/jiraClient.py`
- `projects/jsm-sync/jsm_sync/backfill.py`, `incremental.py`, `reconcile.py`
- `projects/jsm-sync/jsm_sync/db.py`, `transform.py`
- `projects/jsm-sync/schema/001_initial.sql`
- `projects/jsm-sync/docker-compose.yml`

### ops-agent
- `projects/ops-agent/docs/ops-agent-PLAN.md` (v1, historical)
- `projects/ops-agent/docs/ops-agent-PLAN-v2.md` (the v2 redesign; **current**)
- `projects/ops-agent/docs/ops-agent-DIAGRAMS.md`
- `projects/ops-agent/README.md`
- `projects/ops-agent/ops_agent/config.py`
- `projects/ops-agent/ops_agent/db.py`
- `projects/ops-agent/ops_agent/llm.py` — OpenRouter async client
- `projects/ops-agent/ops_agent/main.py` — FastAPI app + lifespan
- `projects/ops-agent/ops_agent/mssql.py` — MSSQL BI sync helpers + smoke test
- `projects/ops-agent/ops_agent/fusion_conn.py` — SSH tunnel + PG pool
- `projects/ops-agent/ops_agent/context/t_context.py` — **the T-shaped context builder**
- `projects/ops-agent/ops_agent/personas/{l2_support,l3_engineer,account_manager,executive}.yaml`
- `projects/ops-agent/ops_agent/personas/__init__.py`
- `projects/ops-agent/ops_agent/generators.py` — three draft flows
- `projects/ops-agent/ops_agent/routes/{tickets,drafts,context}.py`
- `projects/ops-agent/ops_agent/templates/{ticket_detail,related_panel,draft_preview}.html`
- `projects/ops-agent/ops_agent/validate_context.py` — CLI to print T-context for a ticket
- `projects/ops-agent/schema/001_ops_agent_tables.sql`
- `projects/ops-agent/schema/002_draft_log_v2.sql`

### Shared / root
- `/Users/anelson-macbook-air/connected-brain/.env` (source of truth for all creds — do NOT commit)
- `/Users/anelson-macbook-air/connected-brain/.env.example` (committed template)
- `projects/_shared/config.py`
- `projects/_reference/clients/jiraClient.py` (the baseline Jira client; jsm-sync's client was adapted from this)
- `projects/_reference/clients/openrouter.py` (the OpenRouter baseline; ops-agent's `llm.py` uses the same pattern)

---

## Context blocks used

None formally injected. If resuming and doing code work, the following
should be loaded if they exist:
- Any `vault/20-context/apis/` block for Jira or OpenRouter
- Any `vault/20-context/schemas/` block for the Fusion or MSSQL BI schemas
  (the user referenced `/Users/anelson-macbook-air/Code/python scripts/AccountIntelV2/docs/reference`
  during this session as the Fusion schema source of truth — not inside
  the vault yet)
