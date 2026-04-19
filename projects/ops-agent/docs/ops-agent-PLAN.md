# ops-agent — Build Plan

## Purpose

A local-first web app that reads from the `jsm-sync` Postgres mirror and lets Adam:

1. Browse APTUM tickets and explore their threads.
2. Classify tickets into known workflow patterns (firewall upgrades, monthly validations, etc.).
3. Generate persona-drafted responses using per-engineer voice examples pulled from historical comments.

`ops-agent` is a **consumer** of the `jsm-sync` database. It never talks to Jira directly for reads. The only writes back to Jira (posting a comment) happen much later — v1 is preview-only with copy-to-clipboard.

## How this relates to jsm-sync

```
       ┌──────────────────┐
       │  jsm-sync        │   writes tickets, comments,
       │  (sync layer)    │   users, orgs, assets
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │   PostgreSQL     │   single source of truth
       │   (localhost     │
       │    :5432)        │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │  ops-agent       │   reads, classifies, drafts
       │  (viewer + LLM)  │
       └──────────────────┘
```

Both projects live under `/connected-brain/projects/` and share the same Postgres instance. The viewer never holds a connection to Jira. The sync never talks to the LLM. Clean separation.

## Scope for v1

- Single-page web app, no framework complexity. FastAPI backend, lightweight HTML/HTMX or plain React frontend. Whichever Claude Code picks based on your preference.
- Three screens: ticket list, ticket detail, persona draft preview.
- One persona to start: **Firewall Upgrade Close-out**. Once that works end-to-end, adding other patterns is copy-paste.
- Anthropic API for LLM calls (you already have the token pattern from AccountIntel).
- No authentication. It runs on localhost only.
- No Jira write-back yet. Drafts are previewed and copy-to-clipboard only.
- No vector search, no embeddings, no pgvector.

## Guiding principles

1. **Postgres is the only data source.** If you catch yourself wanting to call the Jira API from `ops-agent`, stop — either the data should be synced into Postgres, or it's truly on-demand (e.g. worklog) and belongs in a separate, clearly-marked `jira_direct.py` module.

2. **Classifier is rules first, LLM later.** Start with explicit SQL pattern matching. An LLM classifier can come later as a fallback for unmatched tickets.

3. **Persona drafts are few-shot from real comments.** No clever prompt engineering. The voice match comes from showing the LLM 3-5 real past comments by the same engineer on the same pattern and saying "write another one."

4. **Preview, don't post.** The app never writes to Jira in v1. User copies the draft, pastes into Jira themselves. This removes an entire class of risk and makes the app easy to show to others without worrying about permissions.

5. **Read-only on the `jsm-sync` schema.** `ops-agent` only SELECTs from the tables `jsm-sync` owns. If ops-agent needs its own state (draft logs, pattern definitions, user prefs), it creates its own tables in a separate schema.

---

## Directory structure

```
ops-agent/
├── .env                          # gitignored
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── PLAN.md                       # this file
├── schema/
│   └── 001_ops_agent_tables.sql  # ops-agent's own tables in 'ops' schema
├── ops_agent/
│   ├── __init__.py
│   ├── config.py                 # typed settings
│   ├── db.py                     # read-only pool against jsm_sync
│   ├── classifier.py             # rule-based ticket classification
│   ├── llm.py                    # Anthropic API wrapper
│   ├── patterns/                 # one file per known workflow pattern
│   │   ├── __init__.py
│   │   ├── base.py               # Pattern base class
│   │   └── firewall_upgrade.py   # the first concrete pattern
│   ├── drafter.py                # orchestrates: ticket → pattern → draft
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── tickets.py            # GET /tickets, GET /tickets/{key}
│   │   └── drafts.py             # POST /drafts
│   ├── templates/                # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── ticket_list.html
│   │   ├── ticket_detail.html
│   │   └── draft_preview.html
│   ├── static/
│   │   └── styles.css
│   └── main.py                   # FastAPI app entry point
└── run.sh                        # convenience launcher
```

---

## Architecture decisions

### Frontend approach: HTMX + Jinja2

Not React. Not Vue. Not a Next.js app. Just server-rendered HTML with HTMX for interactivity. Reasons:

- No build step. You edit an HTML template, reload the browser, done.
- No separate JS bundle or deploy step. Everything runs in one FastAPI process.
- Fits a local tool perfectly. If you ever want a "real" frontend later, the backend JSON endpoints are already there.
- Claude Code produces reliable HTML+HTMX quickly. React codebases tend to accrete complexity.

If this doesn't fit your preference, the alternative is a minimal Vite+React frontend calling the same FastAPI endpoints. Both are valid. HTMX is faster to ship.

### Database access pattern

Two pools:

```python
# Read-only against jsm_sync tables
JSM_SYNC_DB_URL = "postgresql://jsm_sync:localdev@localhost:5432/jsm_sync"

# Read-write against ops_agent's own tables (same database, different schema)
OPS_AGENT_SCHEMA = "ops"
```

Both point to the same Postgres instance on port 5432. The `ops` schema is where `ops-agent` writes its own state (draft history, pattern definitions, etc.). The `jsm_sync` tables remain untouched — `ops-agent` only SELECTs from them.

This keeps the two projects' concerns cleanly separated even though they share a database.

### LLM choice

Anthropic Claude Sonnet 4.5 or Haiku 4.5 via the official SDK. Draft generation is one call per button click, ~2-3k tokens input, ~500 tokens output. Cheap at either tier. Use Sonnet for v1 and downshift to Haiku if cost becomes an issue.

No streaming for v1 — it complicates the HTMX flow. Full response, then render. Drafts complete in 3-5 seconds, no streaming UI needed.

### Pattern system

Each persona pattern is a single Python file implementing a simple interface:

```python
class Pattern:
    slug: str                    # "firewall_upgrade"
    display_name: str            # "Firewall Upgrade Close-out"
    
    def matches(self, ticket: dict) -> bool:
        """Does this pattern apply to this ticket?"""
        ...
    
    def build_prompt(self, ticket: dict, examples: list[dict]) -> tuple[str, str]:
        """Return (system_prompt, user_prompt) for the LLM."""
        ...
    
    def fetch_examples(self, conn, ticket: dict) -> list[dict]:
        """Pull relevant few-shot examples from the database."""
        ...
```

Register patterns in `patterns/__init__.py`. The classifier walks the registered patterns and returns the first match. Adding a new pattern = creating one file + adding an import.

---

## Files to create

### `.gitignore`

```
.env
.env.local
.venv/
venv/
__pycache__/
*.pyc
.pytest_cache/
.DS_Store
*.log
logs/
```

### `.env.example`

```
# Postgres (same DB as jsm-sync)
DATABASE_URL=postgresql://jsm_sync:localdev@localhost:5432/jsm_sync

# Anthropic
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-sonnet-4-5

# Server
HOST=127.0.0.1
PORT=8080

# Logging
LOG_LEVEL=INFO
```

### `requirements.txt`

```
fastapi>=0.115
uvicorn[standard]>=0.32
asyncpg>=0.29
pydantic>=2.0
pydantic-settings>=2.0
python-dotenv>=1.0
jinja2>=3.1
anthropic>=0.40
python-multipart>=0.0.12
```

### `schema/001_ops_agent_tables.sql`

```sql
-- ============================================================
-- ops-agent's own tables, in a separate schema to keep
-- jsm_sync's tables untouched.
-- ============================================================

CREATE SCHEMA IF NOT EXISTS ops;

-- Log every draft generated, for analysis and iteration
CREATE TABLE IF NOT EXISTS ops.draft_log (
    id                  SERIAL PRIMARY KEY,
    issue_key           TEXT NOT NULL,
    pattern_slug        TEXT NOT NULL,
    engineer_account_id TEXT,
    prompt_tokens       INTEGER,
    completion_tokens   INTEGER,
    model               TEXT,
    system_prompt       TEXT,
    user_prompt         TEXT,
    generated_text      TEXT NOT NULL,
    generated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    was_used            BOOLEAN  -- set by frontend if user clicks "Copy"
);

CREATE INDEX draft_log_issue ON ops.draft_log (issue_key);
CREATE INDEX draft_log_pattern ON ops.draft_log (pattern_slug);
CREATE INDEX draft_log_generated_at ON ops.draft_log (generated_at DESC);
```

Apply it manually once:

```bash
docker compose -f ../jsm-sync/docker-compose.yml exec -T postgres \
    psql -U jsm_sync -d jsm_sync < schema/001_ops_agent_tables.sql
```

(It's fine to reuse `jsm-sync`'s Postgres container. The schema `ops` is just a namespace within the same DB.)

### `ops_agent/config.py`

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str
    anthropic_api_key: str
    anthropic_model: str = "claude-sonnet-4-5"
    host: str = "127.0.0.1"
    port: int = 8080
    log_level: str = "INFO"


settings = Settings()
```

### `ops_agent/db.py`

asyncpg pool, opened once at app startup, closed at shutdown. Connection strings for both read-only JSM data and read-write ops schema use the same DATABASE_URL — Postgres handles schema permissions at the query level.

Key helpers to implement:

```python
async def init_pool() -> None: ...
async def close_pool() -> None: ...
async def get_pool() -> asyncpg.Pool: ...

# Read helpers against jsm_sync tables
async def list_tickets(
    conn, 
    limit: int = 50, 
    customer_originated: bool | None = None,
    status: str | None = None,
    search: str | None = None  # ILIKE on summary
) -> list[dict]: ...

async def get_ticket(conn, issue_key: str) -> dict | None: ...

async def get_thread(conn, issue_key: str) -> list[dict]: ...

async def get_ticket_assignee(conn, issue_key: str) -> dict | None: ...

async def get_engineer_past_comments(
    conn,
    account_id: str,
    summary_pattern: str,     # e.g. 'Firewall Firmware Upgrade%'
    limit: int = 5,
    min_body_length: int = 50,
    max_body_length: int = 500,
) -> list[dict]: ...

async def get_organization(conn, jira_org_id: str) -> dict | None: ...

# Write helpers against ops schema
async def log_draft(conn, draft: dict) -> int: ...
async def mark_draft_used(conn, draft_id: int) -> None: ...
```

### `ops_agent/classifier.py`

Rules-based classifier. One function that takes a ticket dict and returns a pattern slug (or None).

```python
from typing import Optional

from .patterns import REGISTERED_PATTERNS


def classify(ticket: dict) -> Optional[str]:
    """Return the slug of the first matching pattern, or None."""
    for pattern in REGISTERED_PATTERNS:
        if pattern.matches(ticket):
            return pattern.slug
    return None
```

Pattern matching happens inside each pattern class's `matches()` method. Keep the logic there, not in a giant if/elif chain.

### `ops_agent/patterns/base.py`

```python
from abc import ABC, abstractmethod


class Pattern(ABC):
    slug: str
    display_name: str
    description: str

    @abstractmethod
    def matches(self, ticket: dict) -> bool:
        """Whether this pattern applies to the given ticket."""

    @abstractmethod
    async def fetch_examples(self, conn, ticket: dict) -> list[dict]:
        """Retrieve few-shot examples for this ticket. Typically pulls
        the assigned engineer's past public comments on tickets matching
        this same pattern."""

    @abstractmethod
    def build_prompt(self, ticket: dict, examples: list[dict]) -> tuple[str, str]:
        """Return (system_prompt, user_prompt) for the LLM call."""
```

### `ops_agent/patterns/firewall_upgrade.py`

```python
from .base import Pattern
from ..db import get_engineer_past_comments


class FirewallUpgradePattern(Pattern):
    slug = "firewall_upgrade"
    display_name = "Firewall Upgrade Close-out"
    description = "Drafts the customer-facing close-out comment after a firewall upgrade or cutover."

    def matches(self, ticket: dict) -> bool:
        summary = (ticket.get("summary") or "").lower()
        return (
            "firewall" in summary
            and ("upgrade" in summary or "cutover" in summary or "firmware" in summary)
        )

    async def fetch_examples(self, conn, ticket: dict) -> list[dict]:
        assignee = ticket.get("assignee_account_id")
        if not assignee:
            return []
        
        # Pull the engineer's last 5 public close-out comments on similar tickets
        return await get_engineer_past_comments(
            conn,
            account_id=assignee,
            summary_pattern="Firewall%",  # loose match on summary
            limit=5,
        )

    def build_prompt(self, ticket: dict, examples: list[dict]) -> tuple[str, str]:
        org_name = ticket.get("jira_org_name", "the customer")
        assignee_name = ticket.get("assignee_display_name", "the engineer")

        example_text = "\n\n---\n\n".join(
            f"Past close-out #{i+1}:\n{ex['body']}" for i, ex in enumerate(examples)
        ) if examples else "(no past examples available)"

        system_prompt = (
            f"You are {assignee_name}, an Aptum engineer. You have just finished a "
            f"firewall upgrade or cutover for {org_name}. Write the customer-facing "
            f"close-out comment for the Jira ticket.\n\n"
            f"Match the voice, length, and formality of your past close-out comments. "
            f"Be concise. Do not invent details not present in the past examples or "
            f"the ticket summary.\n\n"
            f"Here are your {len(examples)} most recent close-outs on similar tickets:\n\n"
            f"{example_text}"
        )

        user_prompt = (
            f"The ticket is:\n"
            f"Summary: {ticket['summary']}\n"
            f"Organization: {org_name}\n\n"
            f"Write the close-out comment. Output only the comment text, no preamble."
        )

        return system_prompt, user_prompt
```

### `ops_agent/patterns/__init__.py`

```python
from .firewall_upgrade import FirewallUpgradePattern

REGISTERED_PATTERNS = [
    FirewallUpgradePattern(),
]
```

### `ops_agent/llm.py`

Thin wrapper around the Anthropic SDK. Key functions:

```python
from anthropic import AsyncAnthropic

from .config import settings


_client: AsyncAnthropic | None = None


def get_client() -> AsyncAnthropic:
    global _client
    if _client is None:
        _client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


async def generate_draft(system_prompt: str, user_prompt: str) -> dict:
    """Call Claude and return {text, input_tokens, output_tokens, model}."""
    client = get_client()
    response = await client.messages.create(
        model=settings.anthropic_model,
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return {
        "text": response.content[0].text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "model": settings.anthropic_model,
    }
```

### `ops_agent/drafter.py`

```python
from .classifier import classify
from .db import get_ticket, log_draft
from .llm import generate_draft
from .patterns import REGISTERED_PATTERNS


async def draft_for_ticket(conn, issue_key: str) -> dict:
    """Classify a ticket, generate a draft, log it. Returns draft metadata."""
    ticket = await get_ticket(conn, issue_key)
    if not ticket:
        raise ValueError(f"Ticket not found: {issue_key}")

    slug = classify(ticket)
    if not slug:
        return {
            "status": "no_pattern_match",
            "issue_key": issue_key,
            "message": "No pattern matched this ticket. Manual drafting required.",
        }

    pattern = next(p for p in REGISTERED_PATTERNS if p.slug == slug)
    examples = await pattern.fetch_examples(conn, ticket)

    if not examples:
        return {
            "status": "no_examples",
            "issue_key": issue_key,
            "pattern_slug": slug,
            "message": (
                "This pattern matched, but no past examples were found for the "
                "assigned engineer. A generic draft would be low-quality. "
                "Consider assigning the ticket first, or widening the example query."
            ),
        }

    system_prompt, user_prompt = pattern.build_prompt(ticket, examples)
    llm_result = await generate_draft(system_prompt, user_prompt)

    draft_id = await log_draft(conn, {
        "issue_key": issue_key,
        "pattern_slug": slug,
        "engineer_account_id": ticket.get("assignee_account_id"),
        "prompt_tokens": llm_result["input_tokens"],
        "completion_tokens": llm_result["output_tokens"],
        "model": llm_result["model"],
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "generated_text": llm_result["text"],
    })

    return {
        "status": "ok",
        "draft_id": draft_id,
        "issue_key": issue_key,
        "pattern_slug": slug,
        "pattern_display_name": pattern.display_name,
        "examples_used": len(examples),
        "generated_text": llm_result["text"],
        "tokens": {
            "input": llm_result["input_tokens"],
            "output": llm_result["output_tokens"],
        },
    }
```

### `ops_agent/routes/tickets.py`

FastAPI router with two HTML-returning endpoints:

- `GET /` → redirects to `/tickets`
- `GET /tickets` → ticket list page with optional filters (query params: status, customer_originated, q for search)
- `GET /tickets/{issue_key}` → ticket detail page, showing summary, thread, asset info, and a "Generate Draft" button

### `ops_agent/routes/drafts.py`

- `POST /tickets/{issue_key}/draft` → triggers `draft_for_ticket`, returns the draft HTML fragment (HTMX replaces the button area)
- `POST /drafts/{draft_id}/used` → marks the draft as used (called when user clicks Copy)

### `ops_agent/templates/base.html`

Minimal shell. Just enough to not look hostile:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}ops-agent{% endblock %}</title>
    <script src="https://unpkg.com/htmx.org@2.0.3"></script>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <header>
        <h1><a href="/tickets">ops-agent</a></h1>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

### `ops_agent/templates/ticket_list.html`

Table showing recent tickets. Columns: key, summary (truncated), org, status, created, customer-originated flag. Each row links to the detail page.

Top of page: simple filter form (status dropdown, customer-originated checkbox, search box — submits to same URL with query params).

### `ops_agent/templates/ticket_detail.html`

Shows:
- Summary, status, priority, request type
- Org and ocean_client_id
- Creator, reporter, assignee
- Full thread of comments, with author + role + is_public flag visible
- List of linked assets with service_ids
- Big "Generate Draft" button that does `hx-post="/tickets/{key}/draft"` and puts the result in a div below

### `ops_agent/templates/draft_preview.html`

Rendered into the page below the button when HTMX returns. Shows:
- Pattern matched (e.g., "Firewall Upgrade Close-out")
- Number of examples used
- Generated text in a styled block
- "Copy to clipboard" button with small JS snippet
- Token count
- "Generate another" button to re-roll

### `ops_agent/static/styles.css`

Minimal, clean, no framework. Think "well-designed markdown page" not "enterprise dashboard." Plain system fonts, generous whitespace, one accent color for links/buttons. Fit for a personal tool.

### `ops_agent/main.py`

```python
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import settings
from .db import init_pool, close_pool
from .routes import tickets, drafts


logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool()
    logger.info("ops-agent started")
    yield
    await close_pool()
    logger.info("ops-agent shut down")


app = FastAPI(title="ops-agent", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="ops_agent/static"), name="static")
app.include_router(tickets.router)
app.include_router(drafts.router)


def main():
    import uvicorn
    uvicorn.run("ops_agent.main:app", host=settings.host, port=settings.port, reload=True)


if __name__ == "__main__":
    main()
```

### `run.sh`

```bash
#!/usr/bin/env bash
set -e
source .venv/bin/activate
python -m ops_agent.main
```

---

## Step-by-step execution order

### Step 1 — Scaffold

Create the directory structure, `.gitignore`, `.env.example`, `requirements.txt`, `README.md`, `PLAN.md`, and the empty Python package files.

**Verify:** `tree -L 3 -I '__pycache__|.venv'` shows the expected layout.

### Step 2 — First commit

```bash
git init
git add .gitignore .env.example requirements.txt README.md PLAN.md schema/ ops_agent/
git commit -m "Initial ops-agent scaffold"
```

### Step 3 — Python env

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Adam edits .env: fills in ANTHROPIC_API_KEY
```

### Step 4 — Apply ops schema

Make sure the `jsm-sync` Postgres container is running, then:

```bash
docker compose -f ../jsm-sync/docker-compose.yml exec -T postgres \
    psql -U jsm_sync -d jsm_sync < schema/001_ops_agent_tables.sql
```

**Verify:**
```bash
docker compose -f ../jsm-sync/docker-compose.yml exec postgres \
    psql -U jsm_sync -d jsm_sync -c "\dt ops.*"
```
Should show `ops.draft_log`.

### Step 5 — Minimum viable read layer

Implement `config.py`, `db.py` (just `init_pool`, `close_pool`, `list_tickets`, `get_ticket`, `get_thread`).

Write a scratch verifier:
```python
# scratch_verify_db.py
import asyncio
from ops_agent.db import init_pool, close_pool, get_pool, list_tickets, get_ticket

async def main():
    await init_pool()
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await list_tickets(conn, limit=5)
        for r in rows:
            print(r["issue_key"], "-", r["summary"][:60])
        
        t = await get_ticket(conn, "APTUM-57617")
        print("\nAPTUM-57617:", t["summary"], "| customer?", t["is_customer_originated"])
    await close_pool()

asyncio.run(main())
```

Delete the scratch file after it works.

### Step 6 — Minimum viable web layer

Implement `main.py`, `routes/tickets.py`, and the HTML templates `base.html` + `ticket_list.html` + `ticket_detail.html`.

Start the app:
```bash
./run.sh
```

Open http://127.0.0.1:8080/tickets. You should see the ticket list. Click a ticket. You should see its detail page with the full thread.

The "Generate Draft" button is there but does nothing yet — that's fine.

### Step 7 — Classifier + first pattern

Implement `patterns/base.py`, `patterns/firewall_upgrade.py`, `patterns/__init__.py`, `classifier.py`.

Write a scratch verifier:
```python
# scratch_verify_classifier.py
import asyncio
from ops_agent.db import init_pool, close_pool, get_pool, get_ticket
from ops_agent.classifier import classify

async def main():
    await init_pool()
    pool = await get_pool()
    async with pool.acquire() as conn:
        # Pick a known firewall upgrade ticket from the data we saw in the exploration
        for key in ["APTUM-57145", "APTUM-57176", "APTUM-57617"]:
            t = await get_ticket(conn, key)
            if t:
                print(f"{key}: {t['summary'][:50]!r} -> {classify(t)}")
    await close_pool()

asyncio.run(main())
```

Expected: the firewall tickets classify to `firewall_upgrade`; APTUM-57617 (VPN error) classifies to None.

### Step 8 — LLM wrapper + drafter

Implement `llm.py`, `drafter.py`, and the `db.py` helpers `get_engineer_past_comments`, `log_draft`, `mark_draft_used`, `get_ticket_assignee`.

Scratch verify:
```python
# scratch_verify_drafter.py
import asyncio
from ops_agent.db import init_pool, close_pool, get_pool
from ops_agent.drafter import draft_for_ticket

async def main():
    await init_pool()
    pool = await get_pool()
    async with pool.acquire() as conn:
        result = await draft_for_ticket(conn, "APTUM-57145")  # David Smith firewall cutover
        print(result)
    await close_pool()

asyncio.run(main())
```

Expected: a draft that sounds like David Smith saying "firewall cutover completed, please let us know if any issues." Short, matching his style.

### Step 9 — Wire the draft route into the UI

Implement `routes/drafts.py` and `templates/draft_preview.html`.

In `ticket_detail.html`, the "Generate Draft" button does:
```html
<button hx-post="/tickets/{{ ticket.issue_key }}/draft"
        hx-target="#draft-area"
        hx-swap="innerHTML">
    Generate draft
</button>
<div id="draft-area"></div>
```

The endpoint returns the HTML fragment from `draft_preview.html`.

Restart, reload the UI, click a firewall upgrade ticket, click Generate Draft. Watch the magic.

### Step 10 — Polish and commit

- Pretty up the CSS a bit.
- Add a "classified as" badge to the ticket detail header.
- Add a tiny "status: no pattern match" message when no pattern matches.
- Commit.

```bash
git add -A
git commit -m "v1 working: ticket viewer + firewall upgrade persona draft"
```

---

## What to NOT do in v1

- Do not add a database of ticket classifications. Classify on-demand; it's instant.
- Do not build a pattern editor UI. Patterns are code for v1; edit the Python file and restart.
- Do not add authentication. The app runs on localhost. If you want to password-protect it later, stick nginx or Caddy in front.
- Do not stream LLM responses. Wait for the full response, render it. Simpler, fast enough.
- Do not post to Jira. Preview-only. Adam copies and pastes for now.
- Do not add pgvector, embeddings, or semantic search. The rules-based classifier + few-shot prompting covers the firewall case perfectly. Add complexity when a specific pattern *demands* it, not preemptively.
- Do not build a separate React frontend. HTMX + Jinja2 is plenty.
- Do not build out more patterns in v1. Get firewall_upgrade perfect first. Additional patterns are a separate, much smaller project once the plumbing works.

---

## Success criteria for v1

1. `./run.sh` starts the app at http://127.0.0.1:8080.
2. The ticket list shows recent APTUM tickets from Postgres.
3. Clicking a ticket shows its full thread, assets, and org.
4. On a firewall upgrade ticket (e.g. APTUM-57145, APTUM-57176), clicking "Generate Draft" produces a close-out comment that sounds like the assigned engineer — ideally indistinguishable from their real past comments in the 30-day corpus.
5. The draft is logged to `ops.draft_log`.
6. Copy-to-clipboard works.
7. The `jsm-sync` project and its Postgres container remain unchanged.

---

## What comes after v1

Once firewall_upgrade works end-to-end, the followup work is additive:

1. **More patterns** — one file each. DCO QA hosting orders, DCO monthly validation, VPN quick-fix, backup alert triage. Each is 30-60 minutes of work: write the `matches()` rule, write the prompt, pick the example query.

2. **Pattern coverage analytics** — a view at `/patterns` showing classified-ticket counts per pattern, and a "uncovered" list of recent tickets where no pattern matched. Drives what to build next.

3. **Draft feedback loop** — "was this useful" thumbs up/down per draft, logged into `ops.draft_log`. Review low-scoring drafts to improve prompts.

4. **Post-to-Jira action** — once drafts are consistently good, add an "Approve and post to Jira" button that writes the comment back via the Jira API. Needs a service account or the user's API token. Becomes the first time this project writes to Jira.

5. **On-demand Jira fetches** — for worklog, live SLA state, etc. A `jira_direct.py` module with clearly-scoped functions.

6. **Pattern library in DB** — move patterns from code into `ops.pattern_definitions` so they can be edited in-app without redeploying.

7. **Semantic similarity** — only then, and only for patterns where it's proven necessary (e.g., the "same problem, different words" case). pgvector migration + embedding pipeline in the `jsm-sync` project.

---

## One key design decision to flag

There's a subtle choice hidden in the plan: **examples are fetched per-engineer, not per-team**. The firewall upgrade pattern fetches David Smith's past close-outs if David is the assignee. If David is new to these tickets and has no past comments, the draft fails gracefully with "no examples."

The alternative is to pool examples across all Aptum engineers for a pattern and then say "write this in David's voice" with minimal samples. That's weaker — you lose the style match.

For v1, stick with per-engineer. The failure case ("no examples for this assignee") is actually a feature: it tells you when a ticket has been assigned to someone who doesn't typically do that kind of work, which is useful information on its own.

Later, you can add a fallback chain: engineer's own comments → their team's comments → company-wide comments, with decreasing weight.
