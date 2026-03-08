---
type: thinking
status: active
tags: [cpq, database, supabase, architecture, pricing, infrastructure]
created: 2026-03-08
last_updated: 2026-03-08
---

# CPQ Replacement — Database Architecture & Migration

## The Idea

Replace the existing Excel-based CPQ (Configure, Price, Quote) tool — CPQ v28 — with a database-backed system in Supabase (Postgres) that allows pricing and product updates without releasing a new `.xlsm` file. The immediate goal is a POC that can be handed off as a portable Postgres artifact. Production architecture TBD after the POC validates the model.

## Why This Matters

- Every pricing change currently requires distributing a new version of the Excel file to all sales reps
- The file has ~20 sheets, complex VBA macros, formula dependencies that break silently, and no audit trail
- No one can see who changed what or when
- Sales reps are sometimes quoting from stale versions
- The underlying data (~1,200 rows of reference pricing) is small enough to live in a simple RDBMS, but it's buried in Excel structure that makes it hard to maintain
- The business needs to be able to update a server MRC price without a file release

## What I Know

### About the Current CPQ (v28)

- **20 sheets** across three functional zones:
  - **Reference/data** (hidden): FX, Named Ranges, Products - Hosting, Products - Colo, Options - Colo, Options - Firewalls, Server Data, Colo Data, Model - Drivers
  - **Calculation engines** (hidden): Model - MH, Model - DH
  - **User-facing** (visible): Home, Configurator - Hosting, Quote - Hosting, Configurator - DH, Quote - DH, Configurator - Colo, Quote - Colo, Hosting CSR, Connectivity Calculator

- **Three product lines**: Managed Hosting (MH), Dedicated Hosting (DH), Colocation (Colo)
  - MH and DH are being unified: DH = servers only, MH = servers + managed service add-ons
  - Colo available at MIA and POR only (not ATL, LAX, IAD, TOR)

- **6 data centers**: ATL (USD), MIA (USD), LAX (USD), IAD (USD), TOR (CAD), POR (GBP)

- **18 server SKUs** in scope (MH focus):
  - Pro Series 7.0, Cluster 5.0 (Dell R440), Atomic 5.0 (Dell R650xs)
  - Pro/Advanced/Storage/Essential Series 6.0 (M and vHost variants)
  - Pro/Advanced/Storage/Essential Series 5.0 (M and vHost variants)
  - Promo Server NA, Promo Server UK (special restrictions)

- **Pricing structure**: MRC per term (monthly/12m/24m/36m) × 3 currencies (USD/CAD/GBP). Not a multiplier off a base — each is a hardcoded flat rate. NRC is one-time setup fee.

- **Two-layer pricing system**:
  - Customer-facing: MRC/NRC (what they pay)
  - Internal: CapEx (hardware cost), DC cost drivers per kW/server (what it costs us)

- **Overhead constants** baked into financial model:
  - SG&A: 8.2% of revenue
  - Annual cost inflation: 3.0%
  - Software markup: 15% over wholesale
  - EBIT thresholds: Poor < -10% | Moderate 35% | Good 37.5% | Strong ≥ 40%
  - Capital Intensity threshold: 50%

- **FX approach**: Two rate tables in the CPQ — "Ocean FX" (locked, used for quotes) and "Spot FX" (current market, used in IRR/NPV model)

- **Data already extracted** from CPQ v28 (12 files in `/cpq_extracted/`):
  - `01_servers.csv` — 18 server SKUs with full pricing columns
  - `02_server_dc_availability.csv` — 88 rows (server × DC)
  - `03_server_default_components.csv` — 126 rows
  - `04_server_selectable_options.csv` — 655 rows (all upgrade options per server)
  - `05_hardware_components.csv` — 59 rows (CPU, RAM, Drive, PSU, NIC)
  - `06_software_licenses.csv` — 85 rows (OS, SQL, VMware, Backup, etc.)
  - `07_dc_colo_pricing.csv` — 41 rows
  - `08_dc_cost_drivers.csv` — 48 rows (internal per-DC overhead)
  - `09_overhead_constants.json` — ~12 key/value pairs
  - `10_fx_rates.csv` — 15 rows (Ocean + Spot)
  - `11_business_rules.json` — promo restrictions, lead times, VMware logic, Deal Desk triggers

### About the Product Catalog Source

- `dimProductAttributes` CSV exists with ~2,172 rows (but most are deprecated)
- Active/relevant rows: ~547 with `lifecycle = Active Inventory`
- Key columns: `fusion_id` (primary key across all internal systems), `sku_name`, `level` (TLS = top-level sellable | Component = goes into something else), `type` (Server, Firewall, Switch, Intel, etc.), `lifecycle`, `product_type`, `adjusted_line_of_business`, `vendor`, `search_keywords`
- `fusion_id` is the join key back to Salesforce, billing, and all other internal systems
- Newer CPQ server SKUs (6.0 series, 7.0, Cluster 5.0, Atomic 5.0) exist in the attributes data but with blank `lifecycle` — they're newly added

### About the Target Architecture

- **Database**: Supabase (hosted Postgres) for POC
- **Why Supabase over MSSQL**: Standard Postgres SQL = `pg_dump` produces a portable `.sql` file. Recipient runs `psql -f cpq_poc.sql` against any Postgres instance. MSSQL dialect would require rewriting to migrate.
- **Why not MSSQL**: T-SQL dialect (IDENTITY, NVARCHAR, TOP vs LIMIT) creates migration debt if/when prod goes cloud or non-Microsoft
- **Why not local Postgres/Docker**: Less friction for sharing and updating; Supabase table editor lets non-technical users update a price without writing SQL
- **Long-term prod home**: TBD — but any of: Supabase Pro, AWS RDS Postgres, Azure Database for PostgreSQL, Neon, on-prem Postgres — all accept the same dump

## The Schema Design (Decided)

### Core decisions locked in:

**IDs**: `BIGSERIAL` integers (not UUIDs). UUIDs are 16 bytes vs 8, harder to debug, and the distributed-merge benefit doesn't apply here. Supabase supports either.

**CAD as root currency**: CAD = 1. All FX rates expressed as "units of foreign currency per 1 CAD." To convert from foreign to CAD: divide. Example: USD rate = 0.69 → $1,000 USD ÷ 0.69 = $1,449 CAD.

**Explicit CAD prices stored in `product_pricing`**: CAD prices are stored as columns, not derived at query time from USD × FX. This matches the CPQ's behaviour and ensures quoted prices don't shift underneath a live proposal when FX moves. When FX rates change, finance decides separately whether to rebase the CAD prices.

**Three FX rate types** — finance enters these, they become canon for that period:
- `ocean` — locked rates used in customer-facing quotes
- `spot` — current market rates, used in financial model (IRR/NPV)
- `budget` — internal planning rate, what procurement uses for CapEx CAD calculations
- CFO aligned to updating at Bank of Canada rates, first of month or first of quarter

**CapEx time-series model**: `product_capex` stores `procured_price` + `procured_currency` + `procured_date`. CAD equivalent is derived at query time by joining to `fx_rates` using a LATERAL join to find the most recent `budget` rate on or before the procurement date. This means:
- No stale stored CAD amounts
- Historical cost snapshots are re-derivable from first principles forever
- Adding a new FX rate row retroactively updates any procurement between that date and the prior rate date

**Product types as lookup table** (`product_types`), not inline text. Schema:
```sql
CREATE TABLE product_types (
  type_code    TEXT PRIMARY KEY,   -- 'server', 'cpu', 'firewall', 'switch', 'os', ...
  type_label   TEXT NOT NULL,
  parent_code  TEXT REFERENCES product_types(type_code),  -- hierarchy via self-reference
  level        TEXT NOT NULL   -- 'TLS' | 'Component' | 'Both'
);
```
Hierarchy example: `nvme` → parent `drive` → parent `storage_component`. Query all drive types: `WHERE parent_code = 'drive'`.

**One specs table per product category** (not per subtype — avoids the rathole):
- `server_specs` — TLS servers only
- `component_specs` — handles CPU, RAM, Drive, PSU, NIC in one table (shared columns: watts, form_factor; type-specific: cores, ram_gb, drive_capacity_tb, drive_type)
- `firewall_specs`, `switch_specs`, etc. added later as needed — zero changes to existing tables
- Do NOT create `ssd_specs` vs `nvme_specs` vs `hdd_specs` — use `drive_type` column on `component_specs`

**Component compatibility via `server_selectable_options`**: If a component is in that table for a given server, it's compatible. No separate hardware compatibility matrix for POC. NIC-to-processor compatibility is application logic, not DB.

**Lifecycle dates stored as proper columns** (harmonised from both `dimProductAttributes` and the hardware lifecycle JSON format):
```sql
release_date            DATE,
end_of_sale_date        DATE,
end_of_support_date     DATE,
end_of_service_life_date DATE
```
This replaces the single `lifecycle` text field with queryable dates. Enables: "show me all components going end-of-life in the next 6 months."

**MH and DH unified under Hosting**: No `line_of_business` column on `product_catalog`. DH = servers + OS. MH = same servers + managed service add-ons (managed backup, managed monitoring, OS management). The configurator decides what's included; the DB just stores products.

**Soft-delete always**: `is_active = false` rather than DELETE. Keeps history, prevents FK breakage, allows "show deprecated" filter in UI.

### Table structure summary:

```
currencies             4 rows       CAD/USD/GBP/EUR, CAD is root
fx_rates               grows        ocean/spot/budget rates × date; finance-maintained
product_types          ~30 rows     lookup with self-referencing hierarchy
data_centers           6 rows       ATL/MIA/LAX/IAD/TOR/POR
overhead_constants     ~12 rows     key/value (SG&A, inflation, software_markup, EBIT thresholds)

product_catalog        ~500+ rows   fusion_id is external anchor; id is internal FK
  ├── server_specs                  processor_sockets, drive_bays, promo flags, etc.
  ├── component_specs               cores, ram_gb, drive_capacity_tb, watts, etc.
  ├── [firewall_specs]              added when FW work begins
  └── [switch_specs]                added when switch work begins

product_pricing        ~1,200 rows  product × currency × term_months → mrc, nrc
product_capex          grows        procured_price + currency + date; CAD derived via fx_rates

server_dc_availability 88 rows      server × DC availability
server_default_components 126 rows  server → included component × qty
server_selectable_options 655 rows  server → available upgrade options

dc_cost_drivers        48 rows      internal per-DC overhead costs
```

## What I Don't Know / Open Questions

### Schema questions not yet resolved:

- **`fusion_id` for CPQ-only new products** (Pro Series 7.0, Cluster 5.0, Atomic 5.0 — in `dimProductAttributes` but with blank lifecycle): Do they get `fusion_id` assigned by whoever manages that system before they can be inserted? Or do we allow a nullable `fusion_id` temporarily? Risk: if we allow nulls, we lose the external join guarantee.
	- Answer: fusion_id will only be locked in when we release a new product. We will not be able to have a fusion_id that is null.

- **FX rate direction double-check**: Schema uses "units of foreign per 1 CAD" (USD ≈ 0.69, meaning 1 CAD buys $0.69 USD). Need to verify this matches how CFO/finance team wants to enter and read rates. If they think "1 USD = 1.45 CAD," the direction is inverted — the math changes from divide to multiply.
	- Answer: Fixing on CAD always 1:1. Then everything will go from the bank of canada exchange rates (https://www.bankofcanada.ca/rates/exchange/monthly-exchange-rates/)
		- E.g. US Dollar = 1.3651 for 2026-02

- **Multiple CapEx records per product**: Right now `product_capex` allows multiple rows per product (each procurement batch gets its own record). This is correct for asset tracking. But does the financial model need the "current" CapEx or a weighted average across batches? The CPQ uses a single CapEx figure per product SKU, not per physical unit.
	- When they procure. Add a 

- **Lifecycle date source of truth**: We have dates in `dimProductAttributes` (spotty), the hardware lifecycle JSON (more complete for hardware), and vendor documentation. Who owns keeping these current? Is there a feed from somewhere, or manual maintenance?

- **Who updates what in Supabase**:
  - FX rates → Finance (CFO or team)
  - Server MRC/NRC pricing → ??? (Sales ops? Finance? Product?)
  - Product lifecycle dates → ??? (whoever manages the product catalog)
  - CapEx records → Procurement or Finance
  - New product additions → needs a defined workflow

### Architecture questions not yet resolved:

- **What does the front-end look like for POC?** Options: (a) raw Supabase table editor for internal use only, (b) simple React/Next.js form using Supabase auto-generated REST API, (c) nothing yet — just validate the data with queries
- **Quote generation**: The CPQ produces a formatted customer-facing quote. Does the replacement need to generate a PDF/Word doc, or just produce structured data that gets pasted somewhere?
- **Financial model (EBIT/IRR/NPV)**: The CPQ has a multi-period financial model. Does the POC need this, or just pricing lookups?
- **Who uses this**: Internal only (sales reps, sales ops, finance)? Or does it eventually face the customer?
- **Integration with Salesforce**: The CPQ apparently connects to Salesforce (there's a "Deal Desk request in Salesforce" reference in the Connectivity Calculator). What data flows between them now, and what should flow in the replacement?

### Product catalog questions:

- **Colo scope**: Colo is currently out of scope for POC, but `dimProductAttributes` has colo products (cabinets, cross-connects, power). Leave them in the catalog with `is_active = false`, or exclude entirely?
- **Firewall SKUs**: Juniper SRX 300/340/345/380 are in `dimProductAttributes` with `fusion_id`. They're not in scope for the server POC but will be needed soon. Include the rows, just don't build the configurator logic yet?
- **Promo server NRC**: Both Promo Server NA and Promo Server UK have `nrc_usd = null` and `nrc_gbp = null` in the extracted data. Is there genuinely no setup fee, or is it bundled/zero?

## Assumptions I'm Making

- The POC scope is: server pricing lookups + DC availability + component relationships. Not: financial modeling (IRR/NPV), quote document generation, Salesforce integration.
- Supabase free tier is acceptable for POC (pauses after 1 week of inactivity — this is a known trade-off)
- `fusion_id` is the authoritative product identifier across all internal systems and will remain stable
- CAD is the correct root currency for all financial planning (confirmed: Canadian company, hardware procured in USD but all cost modeling anchored to CAD)
- The CFO and finance team will own FX rate maintenance; it is not automated
- "Lift and shift to someone else" means: another person can run a Postgres instance (Docker, Supabase, RDS) and restore the schema + data from a `pg_dump` file

## Risks and Constraints

- **`fusion_id` gaps**: Newer server SKUs in the CPQ don't have assigned `fusion_ids` yet. POC can proceed with placeholder IDs, but production requires reconciliation with whatever system manages the `fusion_id` namespace.
- **Price staleness**: The extracted data is from CPQ v28. If pricing has changed since the last file version, the seed data will be wrong. Need a "day zero" validation where finance confirms current pricing before go-live.
- **FX rate gap at go-live**: The CPQ has Ocean/Spot rates. The new schema adds `budget` as a third type. Someone needs to backfill historical budget rates (at least 12 months) for the CapEx CAD derivation to work on existing assets.
- **Supabase free tier pausing**: If the POC isn't actively used, the project pauses after 1 week. Not a problem for active development, but could surprise someone picking it up after a holiday week.
- **No financial model in POC**: The CPQ's EBIT/IRR/NPV calculations are real business logic that sales and finance depend on. The POC won't replicate this. There will be a gap period where pricing comes from the new system but EBIT modeling still uses Excel.
- **Colo deprioritized**: Scoped out for POC. Colo clients at MIA and POR will still need the Excel tool during the POC phase.
- **Component compatibility depth**: The CPQ's `server_selectable_options` table (655 rows) drives what components are valid for each server. Getting this wrong produces invalid quotes. This data needs careful validation against what's actually configurable today, not just what was configurable when CPQ v28 was built.

## Decisions Made

| Decision | Choice | Rationale |
|---|---|---|
| Database | Supabase (Postgres) | Portable via pg_dump; standard SQL; table editor for non-technical updates |
| ID type | BIGSERIAL integers | Simpler, smaller, faster joins; UUIDs add cost without benefit at this scale |
| Root currency | CAD = 1 | We're a Canadian company; all cost modeling anchors to CAD |
| FX direction | Units of foreign per 1 CAD (divide to convert) | CAD is base; 1 CAD = $0.69 USD |
| CAD pricing stored or derived | Stored explicitly in product_pricing | Prevents quoted prices shifting when FX moves; matches CPQ behaviour |
| FX rate types | ocean / spot / budget | Ocean = quotes; spot = model; budget = CapEx CAD derivation |
| FX governance | Finance enters monthly/quarterly at Bank of Canada rates | CFO aligned; becomes canon for that period |
| CapEx CAD | Derived at query time via LATERAL join to fx_rates | Time-series model; historical cost snapshots always re-derivable |
| Specs table depth | One per category (server_specs, component_specs) | Avoids rathole; drive_type column handles SSD/NVMe/HDD distinctions |
| Component compatibility | Via server_selectable_options only | No separate compatibility matrix for POC |
| MH vs DH | Unified as Hosting; managed services are add-on products | DH = bare servers; MH = servers + managed service SKUs |
| product_type | Separate lookup table with self-referencing hierarchy | Extensible without schema changes |
| Lifecycle | Structured date columns (release, EOS, EOSupport, EOSL) | Queryable; better than a text status |
| Deprecated products | Soft-delete (is_active = false) | Keeps history; prevents FK breakage |
| Colo scope | Out of scope for POC | MIA and POR colo clients use Excel during POC phase |
| Financial model (EBIT/IRR) | Out of scope for POC | Computation, not data; implement as application logic later |
| Quote generation | Out of scope for POC | Validate data model first |

## Decisions Still Open

| Decision | Options | Blocking? |
|---|---|---|
| FX rate direction confirmation | "units of foreign per 1 CAD" vs "units of CAD per 1 foreign" | Yes — determines all conversion math |
| fusion_id for new SKUs (7.0, Cluster, Atomic) | Block on fusion_id assignment vs. allow nullable temporarily | Yes — affects seed data |
| Multiple CapEx records per product | Allow many (per procurement batch) vs. one current row | No — can change later |
| CapEx model uses latest vs. weighted average | Latest row only vs. weighted average of batches | No — affects financial model which is out of POC scope |
| Front-end for POC | Raw Supabase table editor vs. minimal web UI | No — can start with table editor |
| Who owns each table for updates | RACI for pricing, FX, lifecycle, CapEx | No for POC, yes before prod |
| Salesforce integration | Scope and direction of sync | No for POC |

## Next Step

1. **Confirm FX rate direction** with someone from finance — "1 CAD = $0.69 USD" (divide) vs "1 USD = $1.45 CAD" (multiply). One conversation, five minutes.
2. **Confirm fusion_id assignment** for the CPQ-only new server SKUs — can these be requested from whoever manages that namespace, or do we use placeholder IDs for POC?
3. **Generate the DDL** — `schema.sql` with all CREATE TABLE statements, seed data, and indexes. Ready to run against a fresh Supabase project.
4. **Run validation query**: "What is the MRC for Pro Series 6.0 - M, 36-month term, CAD, available at TOR?" Expected: matches the value currently in CPQ v28. If it matches, the data model is correct.