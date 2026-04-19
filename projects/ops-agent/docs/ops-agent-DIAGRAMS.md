# ops-agent — Visual Guide

Companion to PLAN.md. Shows the app's architecture and flows.

---

## 1. Where this fits in the overall system

```
  ┌──────────────────────────────────────────────────────────────┐
  │                  /connected-brain/projects/                  │
  │                                                              │
  │  ┌──────────────────┐              ┌──────────────────┐      │
  │  │    jsm-sync      │              │   ops-agent      │      │
  │  │                  │              │                  │      │
  │  │  • backfill      │              │  • ticket viewer │      │
  │  │  • incremental   │              │  • classifier    │      │
  │  │  • reconcile     │              │  • persona       │      │
  │  │                  │              │    drafter       │      │
  │  └────────┬─────────┘              └────────┬─────────┘      │
  │           │ writes                          │ reads (mostly) │
  │           │                                 │                │
  │           ▼                                 ▼                │
  │   ┌─────────────────────────────────────────────────┐        │
  │   │              PostgreSQL (local)                 │        │
  │   │   ┌──────────────────────┐ ┌────────────────┐   │        │
  │   │   │ jsm_sync schema      │ │ ops schema     │   │        │
  │   │   │ • tickets            │ │ • draft_log    │   │        │
  │   │   │ • thread_events      │ │                │   │        │
  │   │   │ • jira_users         │ │                │   │        │
  │   │   │ • organizations      │ │                │   │        │
  │   │   │ • assets             │ │                │   │        │
  │   │   │ • ticket_assets      │ │                │   │        │
  │   │   │ • sync_state         │ │                │   │        │
  │   │   └──────────────────────┘ └────────────────┘   │        │
  │   └─────────────────────────────────────────────────┘        │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘
                                │
                                ▼
                     ┌────────────────────┐
                     │  Anthropic API     │
                     │  (ops-agent only)  │
                     └────────────────────┘

  Key rule: ops-agent never reads from Jira directly. All data comes
  from Postgres. If you need it in the UI, it has to be in Postgres.
```

---

## 2. Project tree

```
ops-agent/
│
├── .env                       🔒 secrets (API key)
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── PLAN.md
├── DIAGRAMS.md               (this file)
├── run.sh                    🚀 convenience launcher
│
├── schema/
│   └── 001_ops_agent_tables.sql   📜 ops.draft_log
│
└── ops_agent/                🐍 the Python package
    ├── __init__.py
    ├── config.py             ⚙️  settings
    ├── db.py                 🗄️  asyncpg pool + helpers
    ├── llm.py                🧠 Anthropic SDK wrapper
    ├── classifier.py         🔍 ticket → pattern slug
    ├── drafter.py            ✍️  orchestrates draft generation
    │
    ├── patterns/             📚 one file per workflow pattern
    │   ├── __init__.py
    │   ├── base.py           (abstract Pattern class)
    │   └── firewall_upgrade.py  ⭐ v1's only pattern
    │
    ├── routes/               🌐 FastAPI endpoints
    │   ├── __init__.py
    │   ├── tickets.py        (list + detail pages)
    │   └── drafts.py         (generate + mark-used)
    │
    ├── templates/            📄 Jinja2 HTML
    │   ├── base.html
    │   ├── ticket_list.html
    │   ├── ticket_detail.html
    │   └── draft_preview.html
    │
    ├── static/
    │   └── styles.css
    │
    └── main.py               🎯 FastAPI app entry point
```

---

## 3. The request flow when a user clicks "Generate Draft"

```
  Browser (HTMX)
      │
      │  POST /tickets/APTUM-57145/draft
      │
      ▼
  FastAPI route: drafts.py
      │
      ├─► Fetch ticket from Postgres
      │     SELECT * FROM tickets WHERE issue_key = $1
      │
      ├─► classifier.classify(ticket)
      │     └─► for pattern in REGISTERED_PATTERNS:
      │           if pattern.matches(ticket): return pattern.slug
      │
      │     Result: "firewall_upgrade"
      │
      ├─► pattern.fetch_examples(conn, ticket)
      │     └─► SELECT body FROM thread_events
      │           JOIN tickets ON ...
      │           WHERE author_account_id = <assignee>
      │             AND summary ILIKE 'Firewall%'
      │             AND is_public = true
      │           ORDER BY created_at DESC LIMIT 5
      │
      │     Result: [5 past close-outs by David Smith]
      │
      ├─► pattern.build_prompt(ticket, examples)
      │     └─► (system_prompt, user_prompt)
      │
      ├─► llm.generate_draft(system_prompt, user_prompt)
      │     └─► Anthropic API call
      │         Result: {text, tokens, model}
      │
      ├─► db.log_draft(...)
      │     └─► INSERT INTO ops.draft_log (...) VALUES (...)
      │
      └─► Render templates/draft_preview.html
            with {pattern, examples_used, generated_text, tokens}
            
  Browser (HTMX)
      │
      │  Receives HTML fragment
      │  Replaces #draft-area innerHTML
      │
      ▼
  User sees the draft, clicks "Copy to clipboard"
```

---

## 4. Data flow — how a firewall ticket becomes a draft

```
  APTUM-57145 in Postgres
  ─────────────────────────────────────────────────────
  summary:         "Firewall Firmware Upgrade – Maintenance"
  assignee:        David Smith (account_id: 712020:5858...)
  jira_org_name:   SomeCompany LLC
  is_customer_originated: true
                              │
                              ▼
                     classifier.classify()
                              │
                              │  pattern = "firewall_upgrade"
                              ▼
                 pattern.fetch_examples(david_smith_id)
                              │
                              ▼
  David Smith's last 5 firewall close-outs in Postgres
  ─────────────────────────────────────────────────────
  • "We have completed the firewall cutover and all our
    network checks are looking correct..."
  • "The firewall cutover has been completed and all of
    our network checks are looking correct..."
  • "To confirm the firewall cutover is completed and
    all network checks are looking good..."
  • (2 more)
                              │
                              ▼
                     pattern.build_prompt()
                              │
                              ▼
  System prompt
  ─────────────
  "You are David Smith, an Aptum engineer. You have just
   finished a firewall upgrade for SomeCompany LLC. Write
   the customer-facing close-out comment. Match the voice
   of your past close-outs.
   
   Past close-out #1: We have completed the firewall...
   Past close-out #2: The firewall cutover has been...
   [etc]"
   
  User prompt
  ───────────
  "The ticket is:
   Summary: Firewall Firmware Upgrade – Maintenance
   Organization: SomeCompany LLC
   
   Write the close-out comment."
                              │
                              ▼
                     Anthropic API
                              │
                              ▼
  Generated draft
  ───────────────
  "The firewall cutover has been completed and all our
   network checks are looking correct. Should you
   experience any unexpected effects please don't
   hesitate to let us know."
                              │
                              ▼
                   Logged to ops.draft_log
                              │
                              ▼
                 Rendered in draft_preview.html
                              │
                              ▼
                     User copies and pastes into Jira
```

---

## 5. The pattern registration system

```
  ┌─────────────────────────────────────────────────────┐
  │        ops_agent/patterns/__init__.py               │
  │                                                     │
  │   from .firewall_upgrade import FirewallUpgradePattern │
  │   from .dco_qa import DCOQAPattern     (future)     │
  │   from .vpn_fix import VPNFixPattern   (future)     │
  │                                                     │
  │   REGISTERED_PATTERNS = [                           │
  │       FirewallUpgradePattern(),                     │
  │       DCOQAPattern(),      (future)                 │
  │       VPNFixPattern(),     (future)                 │
  │   ]                                                 │
  └─────────────────────────────────────────────────────┘
                          │
                          │ classifier walks this list
                          │ first match wins
                          ▼
  ┌─────────────────────────────────────────────────────┐
  │        classifier.classify(ticket)                   │
  │                                                     │
  │   for pattern in REGISTERED_PATTERNS:               │
  │       if pattern.matches(ticket):                   │
  │           return pattern.slug                       │
  │   return None                                       │
  └─────────────────────────────────────────────────────┘

  Adding a new pattern = one file + one import line.
  Nothing else changes.
```

---

## 6. Build order — 10 steps with checkpoints

```
┌─── STEP 1 ─────────────────────────────────────────┐
│ Scaffold directories + stub files                  │
│ ✓ tree shows expected layout                       │
└────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 2 ─────────────────────────────────────────┐
│ git init + first commit                            │
│ ✓ no .env in git status                            │
└────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 3 ─────────────────────────────────────────┐
│ Python venv + pip install + copy .env              │
│ ✓ pip list shows fastapi, asyncpg, anthropic       │
└────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 4 ─────────────────────────────────────────┐
│ Apply ops schema to jsm-sync's Postgres            │
│ ✓ \dt ops.* shows draft_log                        │
└────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 5 ─────────────────────────────────────────┐
│ db.py read layer                                   │
│ ✓ scratch script lists 5 tickets, fetches one      │
└────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 6 ─────────────────────────────────────────┐
│ Web layer: main.py, routes/tickets.py, templates   │
│ ✓ ./run.sh starts, localhost:8080/tickets works    │
│ ✓ Clicking a ticket shows detail                   │
└────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 7 ─────────────────────────────────────────┐
│ Classifier + firewall_upgrade pattern              │
│ ✓ scratch script classifies known firewall tickets │
│ ✓ VPN error ticket classifies to None              │
└────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 8 ─────────────────────────────────────────┐
│ llm.py + drafter.py                                │
│ ✓ scratch script generates a David-Smith-voice     │
│   draft on APTUM-57145                             │
└────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 9 ─────────────────────────────────────────┐
│ Draft route + HTMX wiring + draft_preview.html     │
│ ✓ Click "Generate Draft" in UI → draft appears     │
│ ✓ Copy to clipboard button works                   │
└────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── STEP 10 ────────────────────────────────────────┐
│ Polish + commit                                    │
│ ✓ App is usable                                    │
│ ✓ git log shows working v1                         │
└────────────────────────────────────────────────────┘
```

---

## 7. The three screens — quick sketches

```
  ┌─────────────────────────────────────────────────────────────┐
  │ ops-agent                                                    │
  │─────────────────────────────────────────────────────────────│
  │                                                              │
  │  Filters: [status ▼] [☐ customer only] [search _________]   │
  │                                                              │
  │  ┌────────────┬───────────────────────┬─────────────┬──────┐│
  │  │ Key        │ Summary               │ Org         │ ...  ││
  │  ├────────────┼───────────────────────┼─────────────┼──────┤│
  │  │ APTUM-57617│ juniper vpn error     │ Agile Fleet │ Done ││
  │  │ APTUM-57176│ Firewall Firmware U...│ SomeCo      │ Done ││
  │  │ APTUM-57145│ Firewall Firmware U...│ OtherCo     │ Done ││
  │  │ ...        │ ...                   │ ...         │ ...  ││
  │  └────────────┴───────────────────────┴─────────────┴──────┘│
  │                                                              │
  │  Ticket List — /tickets                                      │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │ APTUM-57145 · Firewall Firmware Upgrade – Maintenance        │
  │─────────────────────────────────────────────────────────────│
  │ Org: SomeCompany LLC   Assignee: David Smith   Status: Done │
  │ Pattern: [firewall_upgrade]  ← classified automatically      │
  │                                                              │
  │ Assets:                                                      │
  │   • SRX Cluster (service_id: 1234567)                        │
  │                                                              │
  │ Thread:                                                      │
  │   [2026-04-11 14:30] David Smith (Aptum, public)             │
  │     "Starting firewall cutover maintenance window..."        │
  │   [2026-04-11 15:02] David Smith (Aptum, public)             │
  │     "We have completed the firewall cutover..."              │
  │                                                              │
  │  ┌────────────────────────┐                                  │
  │  │  Generate Draft   ⚡   │  ← click this                    │
  │  └────────────────────────┘                                  │
  │                                                              │
  │  [#draft-area]   ← HTMX replaces this div                    │
  │                                                              │
  │  Ticket Detail — /tickets/APTUM-57145                        │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │ ... (ticket detail above) ...                                │
  │                                                              │
  │  ┌───────────────────────────────────────────────────────┐  │
  │  │ Pattern: Firewall Upgrade Close-out                   │  │
  │  │ 5 examples from David Smith used                      │  │
  │  │                                                       │  │
  │  │ ┌─────────────────────────────────────────────────┐   │  │
  │  │ │ The firewall cutover has been completed and    │   │  │
  │  │ │ all our network checks are looking correct.    │   │  │
  │  │ │ Should you experience any unexpected effects   │   │  │
  │  │ │ please don't hesitate to let us know.          │   │  │
  │  │ └─────────────────────────────────────────────────┘   │  │
  │  │                                                       │  │
  │  │ [Copy to clipboard]   [Generate another]              │  │
  │  │                                                       │  │
  │  │ Tokens: 612 in / 34 out                               │  │
  │  └───────────────────────────────────────────────────────┘  │
  │                                                              │
  │  Draft Preview (rendered into #draft-area by HTMX)           │
  └─────────────────────────────────────────────────────────────┘
```

---

## 8. The mental model

```
  jsm-sync                         ops-agent
  ────────                         ─────────
  
  "Get the data in"                "Make the data useful"
  
  Runs as cron/script              Runs as web app
  Writes to Postgres               Reads from Postgres
  No LLM                           Uses LLM
  No frontend                      Has frontend
  Headless                         Interactive
  
  Stable data layer.               Evolves as personas grow.
  Rarely changes after v1.         Most new patterns land here.
```
