# jsm-sync — Visual Guide

Companion to PLAN.md. Shows what's being built, how pieces connect, and what flows where.

---

## 1. The big picture — why this exists

```
BEFORE (current pain)
─────────────────────
  [Your app / script]  ──────────► [Jira API]
         │                              │
         │         every query          │ rate limit
         └──────────────────────────────┘ ~500 req/hr
                                           slow, fragile


AFTER (what jsm-sync builds)
────────────────────────────
  [Jira API]
       │
       │  periodic sync (pull)
       ▼
  [Postgres mirror]  ◄──────── [Your app / script]
       ▲                              │
       │                              │  any query, any time
       │  on-demand fetch for         │  SQL, no rate limits
       │  nuanced data (worklogs,     │
       │  live SLAs, attachments)     │
       └──────────────────────────────┘
```

---

## 2. The project on disk

```
jsm-sync/
│
├── .env                  🔒 secrets — NEVER commit
├── .env.example          ✅ committed template
├── .gitignore
├── docker-compose.yml    🐳 Postgres container definition
├── requirements.txt      📦 Python deps
├── README.md
├── PLAN.md               📋 the detailed build plan
│
├── postgres_data/        💾 Postgres stores all data here
│                            (gitignored, survives container restarts)
│
├── schema/
│   └── 001_initial.sql   📜 auto-runs on Postgres first boot
│
├── config/
│   └── jira_automation_users.json   🤖 role detection overrides
│
└── jsm_sync/             🐍 the Python package
    ├── __init__.py
    ├── config.py         ⚙️  typed settings from .env
    ├── jira_client.py    🔌 ported from your existing code
    ├── transform.py      🔄 Jira JSON → DB-ready dicts
    ├── db.py             🗄️  asyncpg pool + upsert helpers
    ├── backfill.py       ⏬ one-shot: pull last 30d
    ├── incremental.py    🔁 cron job: pull deltas
    └── reconcile.py      🧹 weekly: catch deletes
```

---

## 3. Database schema — the tables and how they link

```
                ┌────────────────────┐
                │   organizations    │
                │────────────────────│
                │ jira_org_id  (PK)  │
                │ name               │
                │ ocean_client_id    │
                └──────────┬─────────┘
                           │
                           │ many tickets per org
                           │
┌─────────────────┐        ▼         ┌────────────────────┐
│   jira_users    │  ┌────────────┐  │   thread_events    │
│─────────────────│  │  tickets   │  │────────────────────│
│ account_id (PK) │◄─┤────────────├─►│ id           (PK)  │
│ display_name    │  │issue_key PK│  │ issue_key    (FK)  │
│ email           │  │summary     │  │ author_acct  (FK)──┼──► jira_users
│ role            │  │description │  │ kind               │
│ account_type    │  │status      │  │ is_public ✨       │
└─────────────────┘  │priority    │  │ body               │
    ▲                │creator  FK─┼─►│ created_at         │
    │                │reporter FK─┼─►└────────────────────┘
    │                │assignee FK─┼─►
    │                │org      FK─┼─►
    │                │labels[]    │
    │                │SLAs        │
    │                │created_at  │
    │                │updated_at  │
    │                │resolved_at │
    │                │synced_at   │
    │                │deleted_at  │
    │                └──────┬─────┘
    │                       │
    │                       │ many assets per ticket
    │                       │
    │                ┌──────▼──────────┐    ┌──────────────┐
    │                │ ticket_assets   │    │    assets    │
    │                │─────────────────│    │──────────────│
    │                │ issue_key (FK)  │───►│ object_id PK │
    │                │ object_id (FK)  │    │ workspace_id │
    │                │ PK = (both)     │    │ asset_name   │
    │                └─────────────────┘    │ service_id ⭐│
    │                                       └──────────────┘
    │
    └─── referenced by tickets (creator, reporter, assignee)


                    ┌────────────────────┐
                    │   sync_state       │   tracks progress
                    │────────────────────│   for resumability
                    │ source       (PK)  │
                    │ last_cursor        │
                    │ status             │
                    │ last_error         │
                    └────────────────────┘

✨ = new vs AccountIntel (captures jsdPublic)
⭐ = the numeric Fusion TLS ID we extract from JSM Assets
```

---

## 4. How data flows through the sync

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                       BACKFILL FLOW                              │
  │                 (run once, or after a crash)                     │
  └─────────────────────────────────────────────────────────────────┘

  backfill.py
      │
      ├─► 1. Read sync_state.last_cursor
      │      │
      │      ├─ NULL ────► start fresh: updated >= -30d
      │      └─ present ─► resume: updated >= <cursor>
      │
      ├─► 2. Scout:  _fetch_all_keys_jql()
      │             POST /rest/api/3/search/jql
      │             returns: [APTUM-57617, APTUM-57384, ...]
      │
      ├─► 3. For each batch of 20 keys:
      │      │
      │      ├─► Gather in parallel (semaphore=5):
      │      │      _fetch_one_ticket(key)
      │      │        ├─► GET /issue/{key}?expand=changelog
      │      │        ├─► GET /issue/{key}/comment
      │      │        └─► for each asset in customfield_12173:
      │      │              _fetch_asset_details_sync(objectId)
      │      │              → GET /jsm/assets/.../object/{objectId}
      │      │              → extract service_id attribute
      │      │
      │      ├─► transform.py:
      │      │      raw Jira dict → TransformedTicket
      │      │        .ticket_row
      │      │        .users[]
      │      │        .organization
      │      │        .thread_events[]
      │      │        .assets[]
      │      │        .ticket_asset_links[]
      │      │
      │      ├─► db.persist_ticket() — ONE TRANSACTION:
      │      │      ├─► upsert users
      │      │      ├─► upsert organization
      │      │      ├─► upsert ticket
      │      │      ├─► upsert thread_events
      │      │      ├─► upsert assets
      │      │      └─► upsert ticket_asset_links
      │      │
      │      └─► CHECKPOINT: sync_state.last_cursor = max(updated_at)
      │         (if process dies here, next run resumes from cursor)
      │
      └─► 4. Mark sync_state.status = 'completed'


  ┌─────────────────────────────────────────────────────────────────┐
  │                    INCREMENTAL FLOW                              │
  │                (every 10 min via cron)                           │
  └─────────────────────────────────────────────────────────────────┘

  incremental.py
      │
      ├─► Read sync_state.last_cursor (must exist; else error out)
      │
      ├─► JQL: project = APTUM AND updated >= <cursor> ORDER BY updated ASC
      │
      ├─► Same batch + transform + persist loop as backfill
      │      (usually just a handful of tickets)
      │
      └─► Update cursor to max(updated_at) + 1 minute slop
         (the slop handles Jira's eventual consistency on updated_at)
```

---

## 5. The step-by-step build order (with checkpoints)

```
┌─── STEP 1 ──────────────────────────────────────────┐
│ Scaffold directories + config files                  │
│ → .gitignore, .env.example, docker-compose.yml,     │
│   requirements.txt, README.md, schema SQL           │
│                                                      │
│ ✓ tree shows expected structure                      │
└──────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 2 ──────────────────────────────────────────┐
│ git init + first commit                              │
│                                                      │
│ ✓ no .env, no postgres_data/ in git status           │
└──────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 3 ──────────────────────────────────────────┐
│ Python venv + pip install -r requirements.txt        │
│                                                      │
│ ✓ pip list shows all deps                            │
└──────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 4 ──────────────────────────────────────────┐
│ cp .env.example → .env, fill in real Jira creds      │
│ docker compose up -d                                 │
│                                                      │
│ ✓ psql shows 7 tables                                │
│ ✓ sync_state has one row: jira_tickets | idle        │
└──────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 5 ──────────────────────────────────────────┐
│ Port jira_client.py from existing code               │
│                                                      │
│ ✓ scratch script fetches APTUM-57617                 │
│ ✓ is_public flags present on comments                │
│ ✓ body is NOT truncated to 800 chars                 │
└──────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 6 ──────────────────────────────────────────┐
│ Write transform.py + db.py                           │
│                                                      │
│ ✓ scratch upsert test succeeds                       │
│ ✓ row visible in psql, then cleaned up               │
└──────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 7 ──────────────────────────────────────────┐
│ Write backfill.py                                    │
│ Run with --lookback-days 1 (sanity check)            │
│                                                      │
│ ✓ Small row counts in all tables                     │
│ ✓ Cursor present in sync_state                       │
└──────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 8 ──────────────────────────────────────────┐
│ Full backfill: --lookback-days 30                    │
│ Expect 30-90 min depending on volume                 │
│                                                      │
│ ✓ Ticket counts match Jira UI for last 30d           │
│ ✓ APTUM-57617 present with is_public flags intact    │
│ ✓ Spot-checked orgs and assets look right            │
└──────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 9 ──────────────────────────────────────────┐
│ git commit the whole working thing                   │
└──────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 10 ─────────────────────────────────────────┐
│ Flesh out incremental.py                             │
│ Schedule via cron every 10 min                       │
└──────────────────────────────────────────────────────┘
```

---

## 6. What's in Postgres vs. what stays in Jira

```
  ┌──────────────────────────┬──────────────────────────┐
  │    IN POSTGRES (bulk)    │   ONLY IN JIRA (nuance)  │
  ├──────────────────────────┼──────────────────────────┤
  │ ✓ issue_key              │ × Worklog / time entries │
  │ ✓ summary                │ × Live SLA timers        │
  │ ✓ description (plain)    │ × Attachments (blobs)    │
  │ ✓ status, priority       │ × Full ADF formatting    │
  │ ✓ request_type           │ × Changelog history      │
  │ ✓ creator/reporter/      │ × Watchers list          │
  │   assignee account_ids   │                          │
  │ ✓ org + ocean_client_id  │                          │
  │ ✓ labels                 │                          │
  │ ✓ SLA outcomes (numbers) │                          │
  │ ✓ created/updated/       │                          │
  │   resolved timestamps    │                          │
  │ ✓ ALL comment bodies     │                          │
  │   with public/private    │                          │
  │   flag                   │                          │
  │ ✓ comment authors        │                          │
  │ ✓ asset objectIds →      │                          │
  │   service_ids            │                          │
  │ ✓ users: name, email,    │                          │
  │   role                   │                          │
  │ ✓ orgs: name, ocean_id   │                          │
  └──────────────────────────┴──────────────────────────┘

  Strategy:
    "Run SQL against everything on the left.
     When a user clicks a specific ticket and
     wants to see worklog or full timeline,
     THEN hit Jira for that one ticket."
```

---

## 7. The 10,000-foot lifecycle

```
     DAY 0            DAY 1                 ONGOING
  ────────────    ──────────────      ──────────────────

  docker up       python -m                cron every 10 min:
  (schema         jsm_sync.backfill        python -m
   auto-loads)    --lookback-days 30       jsm_sync.incremental
       │                │                         │
       │                │                         │
       ▼                ▼                         ▼
  ┌─────────┐     ┌─────────┐              ┌─────────┐
  │ Empty   │────►│ 30 days │─────────────►│ Always  │
  │ Postgres│     │ of data │              │ current │
  │ schema  │     │ loaded  │              │ (±10min)│
  └─────────┘     └─────────┘              └─────────┘
                       │                         │
                       │                         │
                       ▼                         ▼
                  git commit              SQL queries,
                                          persona app,
                                          AccountIntel
                                          all read from
                                          Postgres
```

---

## 8. Key files, one-line purpose each

```
config.py        Settings() reads .env into typed Python object

jira_client.py   Talks to Jira API. Ported from your existing code,
                 minus artifact writes, plus is_public + full body.

transform.py     Jira dict → (ticket_row, users[], org, events[],
                 assets[], links[]). No side effects, testable alone.

db.py            asyncpg pool + one upsert_* function per table.
                 persist_ticket() wraps all upserts in one transaction.

backfill.py      Read cursor → scout keys → gather tickets →
                 transform → persist → checkpoint cursor. Resumable.

incremental.py   Same as backfill but always cursor-driven, no
                 lookback option. Safe to run on cron.

reconcile.py     Weekly: diff Jira key list vs Postgres, soft-
                 delete rows for tickets that no longer exist in
                 Jira. Low-priority, stub for v1.
```

---

## Notes on this update

- `security_level` has been removed from the schema per your request.
  If you ever need to filter out internal-only tickets later, you can
  derive it from `request_type = 'Internal Incident'` which works well
  enough for the cases we saw in the WeirFoulds data.

- Everything else in PLAN.md stays as-is. This file is a navigation
  aid — PLAN.md remains the executable spec for Claude Code.
