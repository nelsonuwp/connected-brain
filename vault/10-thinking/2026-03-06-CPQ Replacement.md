---
type: thinking
status: active
tags: [cpq, database, supabase, architecture, pricing, infrastructure]
created: 2026-03-08
last_updated: 2026-03-08
---

# CPQ Replacement — Database Architecture & Migration

## The Idea

Replace the existing Excel-based CPQ (Configure, Price, Quote) tool — CPQ v28 — with a database-backed system in Supabase (Postgres) that allows pricing and product updates without distributing a new `.xlsm` file to sales reps.

The immediate goal is a POC that can be handed off as a portable Postgres artifact. Production architecture TBD after the POC validates the model.

**POC success criteria (testable):**

1. Finance updates the Pro Series 6.0-M MRC (36-month, CAD) in the Supabase table editor. A sales rep runs a SQL query and gets the correct updated price for TOR within 1 minute.
2. A SQL query for "Pro Series 6.0-M, 36-month, CAD, TOR" returns MRC/NRC values that exactly match CPQ v28 output for the same configuration.
3. The full schema + seed data can be exported via `pg_dump` and restored on a separate Postgres instance with no errors and the validation query returns the same result.

## Why This Matters

- Every pricing change currently requires distributing a new version of the Excel file to all sales reps.
- The file has ~20 sheets, complex VBA macros, formula dependencies that break silently, and no audit trail.
- No one can see who changed what or when.
- Sales reps are sometimes quoting from stale versions.
- The underlying data (~1,200 rows of reference pricing) is small enough to live in a simple RDBMS, but buried in Excel structure that is hard to maintain.
- The business needs to update a server MRC without a file release.

## What I Know

### About the Current CPQ (v28)

- **20 sheets** across three functional zones:
  - **Reference/data** (hidden): FX, Named Ranges, Products - Hosting, Products - Colo, Options - Colo, Options - Firewalls, Server Data, Colo Data, Model - Drivers
  - **Calculation engines** (hidden): Model - MH, Model - DH
  - **User-facing** (visible): Home, Configurator - Hosting, Quote - Hosting, Configurator - DH, Quote - DH, Configurator - Colo, Quote - Colo, Hosting CSR, Connectivity Calculator

- **Three product lines**: Managed Hosting (MH), Dedicated Hosting (DH), Colocation (Colo).
  - MH and DH unified under "Hosting": DH = servers only, MH = servers + managed service add-ons.
  - Colo available at MIA and POR only.

- **6 data centers**: ATL (USD), MIA (USD), LAX (USD), IAD (USD), TOR (CAD), POR (GBP).

- **18 server SKUs in POC scope** — all Hosting (MH/DH unified); Colo servers excluded:
  - MH managed variants: Pro 7.0-M, Pro 6.0-M, Advanced 6.0-M, Storage 6.0-M, Essential 6.0-M, Pro 5.0-M, Advanced 5.0-M, Storage 5.0-M, Essential 5.0-M
  - vHost variants: Pro 6.0-vHost, Advanced 6.0-vHost, Pro 5.0-vHost, Advanced 5.0-vHost
  - Specialty: Cluster 5.0 (Dell R440), Atomic 5.0 (Dell R650xs)
  - Promo: Promo Server NA, Promo Server UK
  - DH 5.0-D series (from v27.4): absent from v28 — deprecated, out of scope.

- **Pricing structure**: MRC per term (monthly/12m/24m/36m) × 3 currencies (USD/CAD/GBP). Each is a hardcoded flat rate — not a multiplier. NRC is one-time setup fee.

- **Two-layer pricing system**:
  - Customer-facing: MRC/NRC
  - Internal: CapEx (hardware cost) + DC cost drivers per kW/server

- **Overhead constants**: SG&A 8.2%, inflation 3.0%, software markup 15%, EBIT thresholds (Poor < -10% | Moderate 35% | Good 37.5% | Strong ≥ 40%), Capital Intensity 50%.

- **FX approach**: Two rate tables — "Ocean FX" (locked, used for quotes), "Spot FX" (current market, IRR/NPV model).

- **Data extracted** from CPQ v28 (12 files in `/cpq_extracted/`): 01_servers.csv (18 SKUs), 02_server_dc_availability.csv (88 rows), 03_server_default_components.csv (126 rows), 04_server_selectable_options.csv (655 rows), 05_hardware_components.csv (59 rows), 06_software_licenses.csv (85 rows), 07_dc_colo_pricing.csv (41 rows), 08_dc_cost_drivers.csv (48 rows), 09_overhead_constants.json, 10_fx_rates.csv (15 rows), 11_business_rules.json.

### About the Product Catalog Source

- `dimProductAttributes`: ~2,172 rows total; ~547 active (`lifecycle = Active Inventory`).
- Key fields: `fusion_id` (join key to Salesforce, billing, all internal systems), `sku_name`, `level` (TLS | Component), `lifecycle`, `type`, `adjusted_line_of_business`, `vendor`.
- **Newer CPQ server SKUs** (Pro 7.0, Cluster 5.0, Atomic 5.0): In `dimProductAttributes` with blank `lifecycle`. Referenced in CPQ v28 by SKU name only — `fusion_id` has not been assigned because it is only locked in at formal product release. POC uses TEMP- placeholder IDs (e.g. `TEMP-7.0-PRO`) tracked in a `pending_fusion_id` table. Cannot promote to production until real IDs are assigned.

### About the Target Architecture

- **Database**: Supabase (hosted Postgres) for POC.
- **Rationale**: Standard Postgres SQL — `pg_dump` produces a portable `.sql` file. Any Postgres instance (Docker, RDS, Neon, Supabase Pro) can restore it. Supabase table editor lets non-technical users update prices without SQL.
- **Long-term prod home**: TBD after POC validation.

## The Schema Design (Decided)

### Core decisions:

**IDs**: `BIGSERIAL` integers. Simpler, smaller, faster joins; no distributed-merge need.

**CAD as root currency**: CAD = 1 (is_base = true; never appears in fx_rates as a target).
All FX rates = "units of foreign currency per 1 CAD."
- **CAD → foreign**: `cad_amount × rate` (e.g. $1,000 CAD × 1.3651 = $1,365.10 USD)
- **Foreign → CAD**: `foreign_amount ÷ rate` (e.g. $1,000 USD ÷ 1.3651 = $732.51 CAD)

*Note: An earlier draft of this note had the direction inverted ("1 CAD = $0.69 USD"). Finance confirmed: 1 CAD = 1.3651 USD at current ocean rate. All examples use the confirmed direction.*

**Explicit CAD prices in `product_pricing`**: Stored, not derived. Prevents quoted prices shifting when FX moves. When finance chooses to rebase CAD prices after a major FX move, they update `product_pricing` and flip `cad_pricing_rebased = true` on the corresponding `fx_rates` row (audit trail of intentional repricing vs. passive drift).

**FX rate types** (finance-maintained, become canon for the period):
- `ocean` — locked rates for customer-facing quotes
- `spot` — current market, used in financial model
- `budget` — internal planning rate; used for CapEx CAD derivation

**CapEx time-series model**: `product_capex` stores `procured_price + procured_currency + procured_date`. CAD equivalent derived at query time via LATERAL join to `fx_rates` (most recent budget rate ≤ procurement date). Multiple rows per product allowed (one per procurement batch). `use_as_baseline BOOLEAN DEFAULT true` — financial model uses the most recent row where `use_as_baseline = true AND procured_date <= quote_date`. Discounted/unusual batches get `use_as_baseline = false`.

**Product types as lookup table** with self-referencing hierarchy:
```sql
product_types: type_code PK, type_label, parent_code (self-ref), level ('TLS'|'Component'|'Both')
```
Example: `nvme` → parent `drive` → parent `storage_component`.

**Specs tables**:
- `server_specs` — TLS servers (promo flags, sockets, drive_bays, min_contract_months, allow_customization)
- `component_specs` — CPU/RAM/Drive/PSU/NIC in one table; `drive_type` ('SSD'|'NVMe'|'HDD'|'SAS') handles distinctions
- `firewall_specs`, `switch_specs` — added when that work begins; zero changes to existing tables

**Component compatibility**: Via `server_selectable_options` only. No separate matrix for POC. NIC-to-processor and advanced compatibility rules are application logic (deferred).

**Lifecycle as queryable date columns**: `release_date`, `end_of_sale_date`, `end_of_support_date`, `end_of_service_life_date`.

**MH/DH unified**: No `line_of_business` on `product_catalog`. Configurator decides what's included.

**Soft-delete**: `is_active = false`, never DELETE.

**`pending_fusion_id` table**: Any product with a TEMP- placeholder gets a row here. Blocks production promotion until all rows are resolved.

### Table structure summary:

```
currencies                  4 rows       CAD(base)/USD/GBP/EUR
fx_rates                    grows        ocean/spot/budget × date; cad_pricing_rebased + confirmed_override flags
product_types               ~30 rows     lookup with self-ref hierarchy
data_centers                6 rows       ATL/MIA/LAX/IAD/TOR/POR
overhead_constants          ~12 rows     key/value

product_catalog             ~500+ rows   fusion_id = external anchor; BIGSERIAL id = internal FK
  ├── server_specs                        promo flags, sockets, drive_bays, min_contract_months
  ├── component_specs                     cores, ram_gb, drive_capacity_tb, watts, drive_type
  ├── [firewall_specs]                    future
  └── [switch_specs]                      future

product_pricing             ~1,200 rows  product × currency × term_months → mrc, nrc, pricing_model
product_capex               grows        procured batches; use_as_baseline flag; CAD derived via fx_rates

server_dc_availability      88 rows
server_default_components   126 rows
server_selectable_options   655 rows

dc_cost_drivers             48 rows
pending_fusion_id           small        TEMP- placeholder tracker; blocks prod promotion
```

## Data Ownership (RACI-lite)

| Table | Owner | Cadence | Status |
|-------|-------|---------|--------|
| `fx_rates` | Finance (CFO or delegate) | Monthly or quarterly | CFO confirmed |
| `product_pricing` (MRC/NRC) | Product / Sales Ops | On pricing change | Owner TBD before prod |
| `product_capex` | Finance / Procurement | On hardware purchase | Owner TBD before prod |
| Lifecycle dates | Product | On release / EOL | Owner TBD before prod |
| New product additions | Product | On release | Must clear pending_fusion_id |
| `overhead_constants` | Finance | Annually or on model change | CFO confirmed |

## What I Don't Know / Open Questions

- **Promo server NRC**: Both Promo Server NA and UK have `nrc = null` in extracted data. Is it genuinely zero, or a data gap? Blocking for seed data.
- **Colo products**: Insert with `is_active = false` (so schema is ready when colo work begins) vs. exclude entirely. Recommend: include inactive.
- **RACI named owners**: Finance rows are confirmed. Product/Sales Ops/Procurement owners TBD — required before production go-live.

## Assumptions

- POC scope: server pricing lookups + DC availability + component relationships. Not: financial modeling, quote generation, Salesforce integration.
- Supabase free tier is acceptable (pauses after 1 week inactivity — documented).
- `fusion_id` is stable and authoritative across all internal systems.
- CAD is the correct root currency.
- Finance owns FX rate maintenance; it is not automated.
- CPQ v28 remains a read-only fallback for the entire POC phase. Not retired until production is validated.

## Risks and Constraints

- **fusion_id gaps**: TEMP- placeholders via `pending_fusion_id` table. Mid-POC additions: same process.
- **Price staleness**: Finance must confirm extracted pricing matches current before treating seed data as authoritative.
- **FX backfill**: `budget` rate type is new. Need 12+ months of historical budget rates for CapEx derivation to work on existing assets.
- **CapEx rate override risk**: Wrong budget rate silently corrupts CapEx CAD calculations. Mitigation: app-layer warning when new rate differs from prior by >±10%. `confirmed_override BOOLEAN` column on `fx_rates` serves as override acknowledgment.
- **No financial model in POC**: EBIT/IRR/NPV still runs in Excel during POC.
- **Component compatibility validation**: Sales ops to test-configure 5 representative servers (Pro 6.0-M, Advanced 6.0-M, Cluster 5.0, Atomic 5.0, Promo NA) in CPQ v28 and compare valid option sets against `04_server_selectable_options.csv`. Flag mismatches before seed data load.

## Decisions Made

| Decision | Choice | Rationale |
|---|---|---|
| Database | Supabase (Postgres) | Portable via pg_dump; standard SQL; table editor |
| ID type | BIGSERIAL | Simple, small, fast |
| Root currency | CAD = 1 | Canadian company |
| FX direction | 1 CAD = N foreign (×rate for CAD→foreign, ÷rate for foreign→CAD) | Finance confirmed: 1 CAD = 1.3651 USD |
| CAD pricing | Stored in product_pricing | Quote stability |
| FX governance | Finance-maintained; cad_pricing_rebased audit flag | CFO aligned |
| CapEx model | Time-series; LATERAL join; use_as_baseline flag | Re-derivable; discounted batches excluded |
| Specs depth | One table per category | drive_type handles subtypes |
| Compatibility | server_selectable_options only | No matrix for POC |
| MH/DH | Unified as Hosting | Configurator handles distinction |
| product_type | Self-referencing lookup table | Extensible |
| Lifecycle | Date columns | Queryable |
| Deprecated products | Soft-delete | History + FK safety |
| Colo | Out of scope for POC; inactive rows in catalog | MIA/POR use Excel during POC |
| Financial model | Out of scope | Computation, not data |
| fusion_id gaps | TEMP- + pending_fusion_id table | POC unblocked; prod blocked until resolved |
| RACI | Defined above; named owners required pre-prod | Not blocking POC |

## Decisions Still Open

| Decision | Options | Blocking? |
|---|---|---|
| Promo server NRC (null vs zero) | Confirm with Sales Ops | Yes — seed data |
| Colo products: include inactive vs. exclude | Include inactive (recommended) vs. skip | No |
| RACI named owners (Product/Sales Ops/Procurement) | TBD | No for POC, yes for prod |

## POC Handoff Criteria

Deliverable is four files:
1. `schema.sql` — all CREATE TABLE statements, indexes, constraints, comments
2. `seed_data.sql` — INSERTs from the 12 CSV/JSON files + dimProductAttributes active rows
3. `validation.md` — validation queries and expected outputs from CPQ v28
4. `README.md` — restore instructions, table descriptions, known gaps (TEMP- IDs, colo excluded, financial model deferred)

Anyone with a Postgres instance can: `psql -f schema.sql && psql -f seed_data.sql` and run queries. No application code required.

## Rollback Plan

CPQ v28 kept as read-only fallback throughout POC and production validation. Not retired until:
1. At least one full sales cycle completed using the new system.
2. Finance confirmed price data is correct via validation queries.
3. All RACI rows have named owners.

If wrong prices are sent to a client: (1) revert to CPQ v28 for all new quotes immediately, (2) flag affected quotes to Sales Ops, (3) fix seed data and re-run validation before re-enabling.

## Next Steps

1. ✅ FX direction confirmed: 1 CAD = 1.3651 USD (multiply CAD→foreign, divide foreign→CAD)
2. ✅ fusion_id for new SKUs: TEMP- placeholders in POC; locked at product release
3. ✅ CapEx model: multiple rows; use_as_baseline flag; latest non-discounted wins
4. **Generate DDL** — `schema.sql` *(in progress)*
5. **Load seed data** — `seed_data.sql` from 12 CSV/JSON files + dimProductAttributes
6. **Run validation query** — "Pro Series 6.0-M, 36-month, CAD, TOR" → must match CPQ v28
7. **If validation fails** — compare SQL query logic against CPQ v28 "Model - MH" sheet formula. Document discrepancies in `formula_mapping.md`. Common failure modes: wrong term_months value, wrong currency_code filter, wrong DC join.
8. **RACI**: confirm named owners for Product/Sales Ops/Procurement rows before prod go-live.
9. **Compatibility validation**: sales ops test 5 servers in CPQ v28; compare against `04_server_selectable_options.csv`.

---

## Critique History

### Critique — 2026-03-08 08:54 ET
**Score: 7/10** — Approach clear; fixes applied to note body above. Key issues resolved: POC success criteria made testable; MH/DH breakdown clarified; FX direction corrected (1 CAD = 1.3651 USD throughout); cad_pricing_rebased flag added; use_as_baseline flag added; pending_fusion_id table added; RACI-lite defined; compatibility validation process defined; rollback plan added; handoff criteria defined; Decisions Still Open pruned of resolved items.


My questions:
OK, reading through the schema's the currencies looks good. The FX rates. I have a question on I will first statement is the right type. Let's just keep spot and budget and get rid of ocean I've been told by finance that the spot will be the affordable rate and then they do need a budget rate for like beginning of the year type stuff for how to report to the board or investors. I'm curious about the CAD pricing rebased confirm override in the product types I don't see any reference diffusion ID that seems to be our main unique identifier here, but I think it might be handled in the product catalogue. I see servers.