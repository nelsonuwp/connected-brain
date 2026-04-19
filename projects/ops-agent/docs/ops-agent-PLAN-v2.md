# ops-agent PLAN v2 — T-shaped ticket analyst

**Status:** spec (supersedes `docs/ops-agent-PLAN.md`)
**Mode:** written in Think/Specify; to be executed after user approval
**Author:** session 2026-04-18

---

## Why v2

v1 assumed that drafting a good reply = "pick a pattern, mimic the assignee's voice." In practice:

1. Tickets rarely match a single pre-registered pattern.
2. Many tickets have no assignee, so per-person voice examples don't exist.
3. The real leverage is **T-shaped context** (customer history + same-hardware history) combined with **role-based personas** the user picks at draft time.

v2 drops per-engineer imitation and automatic classification. Replaces with:

- User-driven action buttons (no auto-classification).
- Canned role-based personas (L2 / L3 / Account Manager / Executive), editable at request time.
- T-shaped "prior art" sidebar populated from Fusion PG + MSSQL BI + local `jsm_sync`.

---

## Data sources

| Source | Connection | Used for |
|---|---|---|
| `jsm_sync` Postgres (local) | `asyncpg` pool (already in place) | Ticket history: vertical (same `ocean_client_id`) + horizontal (via `assets.service_id`) |
| **MSSQL BI** `DM_BusinessInsights` | `pymssql` direct (corporate LAN) | `dimComponents` — the only source for flat component detail. No Fusion equivalent accessible to `sb_readonly`. |
| **Fusion PG** `fusion` on `db1.peer1.com` | `psycopg2` behind a persistent `sshtunnel.SSHTunnelForwarder` started in FastAPI lifespan | Source-of-truth for customer identity, **all services including cancelled** (`customer_products`), TAM/CSM, cancel reasons |

**Authority split (confirmed in `AccountIntelV2/docs/reference/schemas/cross-source-mapping.md`):**

- Customer identity / full service list (active + cancelled) → Fusion (`customers` + `customer_products`)
- Component fingerprint → MSSQL (`dimComponents`)
- Ticket history → local `jsm_sync`

`jsm_sync.tickets.ocean_client_id` (int) == Fusion `customers.customers_id` (int) == MSSQL `dimServices.client_id` (int). Same value, no cast required.

`jsm_sync.assets.service_id` (text) == Fusion `customer_products.id` (int, cast needed) == MSSQL `dimServices.service_id` (int, cast needed).

---

## `.env` contract (already updated)

```
# MSSQL BI
MSSQL_BI_SERVER, MSSQL_BI_NAME, MSSQL_BI_USER, MSSQL_BI_PASS

# Fusion PG
FUSION_DB_SERVER, FUSION_DB_PORT, FUSION_DB_NAME, FUSION_DB_USER, FUSION_DB_PASS

# SSH tunnel for Fusion
SSH_HOST, SSH_PORT, SSH_USER, SSH_PASS
```

Root `.env` uses the names above. `projects/_shared/config.py`, `db-sync`, and `cpq-replacement-db-only` accept **MSSQL_BI_*** first and fall back to legacy **OCEAN_DB_*** so older local `.env` copies keep working. **SSH_USER** / **SSH_PASS** are canonical; **SSH_USERNAME** / **SSH_PASSWORD** are still read as fallbacks.

Spec and diagrams for this project live under `projects/ops-agent/docs/` (not a nested `ops-agent/` folder — the Python package is `ops_agent/` with an underscore).

---

## T-shaped context

New module: `ops_agent/context/t_context.py`.

```python
@dataclass
class TContext:
    # VERTICAL — customer
    client_id: int | None
    client_name: str | None
    client_status: str | None            # "Active" | "Cancelled" | None
    account_manager: str | None          # TAM from Fusion client_relations
    customer_service_count_active: int
    customer_service_count_cancelled: int
    customer_tickets: list[TicketBrief]  # last N from jsm_sync, same ocean_client_id

    # HORIZONTAL — hardware
    ticket_services: list[ServiceRow]    # services attached to this ticket, Fusion-sourced
    ticket_components: list[ComponentRow] # dimComponents for those services
    neighbor_services: list[NeighborRow]  # services sharing component_ids, ranked by Jaccard
    neighbor_tickets: list[TicketBrief]   # tickets referencing those services (any customer)
```

### Algorithm

1. Read ticket from `jsm_sync.tickets` + `jsm_sync.assets` → list of `service_id` strings.
2. Resolve `client_id` from Fusion `customer_products` by joining on `customer_products.id ∈ service_ids`. If `ocean_client_id` on the ticket already set, prefer that.
3. **Vertical query** — `jsm_sync.tickets WHERE ocean_client_id = :cid ORDER BY updated_at DESC LIMIT :N` (default N=30).
4. **Horizontal fingerprint** — MSSQL:
   ```sql
   SELECT component_id FROM dbo.dimComponents
   WHERE service_id IN (:service_ids) AND is_online = 'Yes'
   ```
5. **Neighbor search** — MSSQL:
   ```sql
   -- find services that share ≥ MIN_SHARED component_ids
   SELECT service_id, COUNT(DISTINCT component_id) AS shared
   FROM dbo.dimComponents
   WHERE component_id IN (:component_ids)
     AND service_id NOT IN (:source_service_ids)
     AND is_online = 'Yes'
   GROUP BY service_id
   HAVING COUNT(DISTINCT component_id) >= :MIN_SHARED
   ORDER BY shared DESC
   LIMIT :K;
   ```
6. **Jaccard re-rank** — for each neighbor, fetch its component_ids, compute `|A∩B| / |A∪B|`, keep top K.
7. **Neighbor tickets** — `jsm_sync.tickets t JOIN assets a ON a.issue_key = t.issue_key WHERE a.service_id IN (:neighbor_service_ids) ORDER BY t.updated_at DESC LIMIT :M`.

### Tunables (top of `t_context.py`)

```python
CUSTOMER_TICKET_LIMIT = 30
K_TOP_NEIGHBORS = 25
N_MIN_SHARED_COMPONENTS = 2
NEIGHBOR_TICKET_LIMIT = 20
```

Start conservative, easy to tune from observed noise.

---

## Personas (YAML-defined, editable at request time)

`ops_agent/personas/` — one YAML per persona:

```yaml
slug: l2_support
label: L2 Support Engineer
voice: |
  You are an L2 support engineer at a managed hosting provider.
  Your tone is technical but deferential. You confirm scope before
  acting. For invasive changes, you propose specific maintenance
  windows. You do not speculate on root cause without evidence.
style_rules:
  - Always propose a specific maintenance window slot
  - Never promise resolution before investigation
  - End with: "Please confirm to proceed."
default_temperature: 0.4
```

Starter set (v2 ships with these):

- `l2_support.yaml`
- `l3_engineer.yaml` — root-cause language, deep technical
- `account_manager.yaml` — outcome/impact framing, no jargon
- `executive.yaml` — one paragraph, risk + next action

Adding personas = drop a new YAML file, no code change.

**UX contract:** when user picks a persona, the rendered `voice + style_rules` block is loaded into an editable `<textarea>` in the ticket detail page. User can tweak before clicking Generate. If they edited it, the override is persisted in `ops.draft_log.system_prompt_override`.

---

## UI — ticket detail page v2

```
┌─────────────────────────────────────────────┬──────────────────────────┐
│ APTUM-12345 · Firmware Upgrade Request      │ RELATED CONTEXT          │
│ ──────────────────────────────────────────  │ ──────────────────────── │
│ Customer: Winston Data SA DE CV [Active]    │ Customer History (12)    │
│ TAM: Jane Doe                                │ ├ APTUM-9872 Resolved   │
│ Services: 5254077 Advanced E5v3 - M         │ │  Reboot completed...   │
│ Status: Open | Priority: High               │ ├ APTUM-8841 Resolved   │
│                                             │ │  Added failover rule   │
│ Description / Thread events...              │ └ [see all 12]          │
│                                             │                          │
│ ── Actions ────────────────────────────     │ Same-Hardware Tickets    │
│ [ 🔍 Identify Potential Fix ]               │ (8 neighbor services)    │
│ [ 🔒 Generate Internal Comment ]            │ ├ APTUM-7712 (Acme) ✓    │
│ [ 💬 Generate Public Comment ▾ ]            │ │  Upgraded iOS, clean   │
│   Persona: [ L2 Support ▾ ]                 │ ├ APTUM-6109 (Zeta) ✓    │
│   System prompt (editable):                 │ │  Rollback required     │
│   ┌─────────────────────────────────────┐   │ └ [see all 8]           │
│   │ You are an L2 support engineer...   │   │                          │
│   └─────────────────────────────────────┘   │                          │
│   [ Generate ]                              │                          │
│                                             │                          │
│ ── Generated Draft ─────────────────────    │                          │
│ (HTMX target — persona output appears here) │                          │
└─────────────────────────────────────────────┴──────────────────────────┘
```

Sidebar is an HTMX-lazy-loaded fragment: `GET /tickets/{issue_key}/related` returns HTML. Page skeleton loads fast; T-context builds in parallel with the main page render.

---

## Three generator flows

| Button | Persona? | System prompt | Output | Route |
|---|---|---|---|---|
| 🔍 **Identify Potential Fix** | No | Fixed "diagnostic engineer" prompt. Synthesize: *given these similar tickets and their resolutions, what's the likely fix and confidence level?* | Markdown analysis, not a customer comment. Internal only. | `POST /tickets/{key}/draft/fix-suggestion` |
| 🔒 **Generate Internal Comment** | No | Fixed "internal ops note" prompt. Terse, technical, private. | Short internal comment. | `POST /tickets/{key}/draft/internal` |
| 💬 **Generate Public Comment** | Yes (user picks + edits) | Persona YAML `voice` + `style_rules`; editable by user. | Customer-facing comment. | `POST /tickets/{key}/draft/public` |

All three inject the full `TContext` as structured sections in the user prompt. The fix-suggestion button is the highest-value one — it's where the T-context really earns its keep.

---

## `ops.draft_log` schema changes (additive)

```sql
ALTER TABLE ops.draft_log
    ADD COLUMN IF NOT EXISTS draft_type            TEXT,   -- 'fix_suggestion' | 'internal' | 'public'
    ADD COLUMN IF NOT EXISTS persona_slug          TEXT,   -- nullable for non-public
    ADD COLUMN IF NOT EXISTS system_prompt_override TEXT;  -- set if user edited the textarea
```

No breaking changes, no migrations required beyond the `ADD COLUMN IF NOT EXISTS`.

---

## File map (deltas from v1)

```
ops_agent/
├── mssql.py                  NEW — pymssql pool for DM_BusinessInsights
├── fusion.py                 NEW — psycopg2 + sshtunnel, managed in FastAPI lifespan
├── context/
│   ├── __init__.py           NEW
│   └── t_context.py          NEW — build_t_context(issue_key) -> TContext
├── personas/
│   ├── __init__.py           NEW — load_personas() / Persona dataclass
│   ├── l2_support.yaml       NEW
│   ├── l3_engineer.yaml      NEW
│   ├── account_manager.yaml  NEW
│   └── executive.yaml        NEW
├── generators/
│   ├── __init__.py           NEW
│   ├── fix_suggestion.py     NEW
│   ├── internal_comment.py   NEW
│   └── public_comment.py     NEW
├── routes/
│   ├── tickets.py            MODIFIED — drop classifier, load personas for dropdown
│   ├── context.py            NEW — GET /tickets/{key}/related (sidebar HTMX fragment)
│   └── drafts.py             REWRITTEN — three POST endpoints, persona support
├── templates/
│   ├── ticket_detail.html    REWRITTEN — two-column layout, 3 buttons, persona selector + editable textarea
│   ├── related_panel.html    NEW — sidebar HTMX fragment
│   ├── draft_preview.html    MODIFIED — supports 3 output types
│   └── ... (others unchanged)
├── db.py                     MODIFIED — add list_customer_tickets(), list_neighbor_tickets(); remove get_engineer_past_comments()
├── classifier.py             DELETED
├── patterns/                 DELETED
├── drafter.py                DELETED (replaced by generators/)
├── main.py                   MODIFIED — lifespan opens Fusion SSH tunnel + pools
└── schema/
    └── 002_draft_log_additions.sql  NEW — additive ALTERs
```

---

## Build order

1. **MSSQL smoke test** — `mssql.py` with a "SELECT TOP 1 * FROM dimComponents" probe, runnable via `python3 -m ops_agent.mssql`. Verify pymssql + corporate-LAN access works from the dev box.
2. **Fusion smoke test** — `fusion.py` with SSH tunnel + `SELECT current_user, current_database()`. Verify tunnel stays up.
3. **`t_context.py`** — build standalone, testable with a script that takes `issue_key` and prints the TContext as JSON. No UI dependency.
4. **Personas** — YAML files + loader. Add a `GET /personas` debug route to verify parsing.
5. **Sidebar route + template** — `GET /tickets/{key}/related` returns HTML fragment; hook into `ticket_detail.html` via `hx-get ... hx-trigger="load"`.
6. **Three generator endpoints** + new `draft_preview.html` wiring.
7. **Ticket detail page rewrite** — 2-column layout, 3 buttons, persona selector.
8. **Delete v1 code** — classifier, patterns, drafter, old routes, old templates.
9. **`002_draft_log_additions.sql`** — applied via `docker compose exec postgres psql`.
10. **README update** — new architecture, new env vars, new buttons.

Each step is independently demoable. If Fusion tunnel proves unreliable on the dev box, steps 3-7 still work with just MSSQL + jsm_sync (customer identity degrades gracefully).

---

## Open questions (defer until Execute mode)

- **Persona defaults**: do we want TAM name injected into Account Manager persona's system prompt automatically? (probably yes, makes it personal)
- **Caching**: should `t_context` results be cached per issue_key for the session? (low priority — TTL 5 min likely fine)
- **Multi-service tickets**: if a ticket references 5 services, do we union all components or score separately? (v2: union, simple)
- **Cancelled services in sidebar**: should cancelled services' tickets still show in horizontal neighbors? (default yes, flag them visually)

---

## Out of scope for v2

- Auto-classification (removed)
- Per-engineer voice examples (removed)
- Live Fusion writes (read-only always)
- FusionBridge REST API integration (not needed given direct DB access)
- Cost / margin data (dimComponents cost fields available but not used yet)
- Salesforce enrichment
- Feedback loop on drafts (was_used flag stays but no UI yet)
