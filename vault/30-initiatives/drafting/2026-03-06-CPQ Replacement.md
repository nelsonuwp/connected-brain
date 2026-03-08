---
type: initiative
status: drafting
---

# CPQ Replacement — Database Architecture & Migration

## One-Line Purpose
Replace the Excel-based CPQ v28 with a Supabase (Postgres) database that allows pricing and product updates without distributing new files to sales reps.

## Context
The current CPQ is a 20-sheet Excel file with VBA macros, formula dependencies that break silently, and no audit trail. Every pricing change requires distributing a new version to all sales reps, who sometimes quote from stale versions. The underlying reference data (~1,200 rows) is small enough for a simple RDBMS but buried in unmaintainable Excel structure. This POC validates the database model before committing to production architecture.

## Success Looks Like
1. Finance updates the Pro Series 6.0-M MRC (36-month, CAD) in the Supabase table editor; a sales rep runs a SQL query and gets the correct updated price for TOR within 1 minute.
2. A SQL query for "Pro Series 6.0-M, 36-month, CAD, TOR" returns MRC/NRC values that exactly match CPQ v28 output for the same configuration.
3. The full schema + seed data can be exported via `pg_dump` and restored on a separate Postgres instance with no errors, and the validation query returns the same result.

## Constraints
- POC scope: server pricing lookups, DC availability, component relationships only — not financial modeling, quote generation, or Salesforce integration
- Supabase free tier (pauses after 1 week inactivity)
- CPQ v28 remains read-only fallback for entire POC phase
- Cannot promote to production until all TEMP- placeholder fusion_ids are resolved
- No DELETE operations — soft-delete only (is_active = false)
- CAD is root currency; FX direction is "units of foreign currency per 1 CAD"

## Open Questions
- **Promo server NRC (null vs. zero)**: Both Promo Server NA and UK have `nrc = null` in extracted data. Must confirm with Sales Ops whether this is genuinely zero or a data gap — blocks seed data generation.
- **RACI named owners**: Finance rows are confirmed (CFO). Product/Sales Ops/Procurement owners TBD — not blocking POC but required before production go-live.
- **FX budget rate backfill**: Need 12+ months of historical budget rates for CapEx CAD derivation to work on existing assets — source and completeness unknown.

## Work Breakdown

### Files / Deliverables
1. `schema.sql` — all CREATE TABLE statements, indexes, constraints, comments
2. `seed_data.sql` — INSERTs from 12 CSV/JSON files + dimProductAttributes active rows
3. `validation.md` — validation queries and expected outputs from CPQ v28
4. `README.md` — restore instructions, table descriptions, known gaps (TEMP- IDs, colo excluded, financial model deferred)

### Sequence
1. Generate DDL (`schema.sql`) — schema design is decided, needs implementation
2. Load seed data (`seed_data.sql`) — depends on schema; blocked on Promo NRC confirmation
3. Run validation query ("Pro Series 6.0-M, 36-month, CAD, TOR") — depends on seed data
4. If validation fails: compare SQL logic against CPQ v28 "Model - MH" sheet formula; document discrepancies in `formula_mapping.md`
5. Sales Ops compatibility validation: test-configure 5 servers (Pro 6.0-M, Advanced 6.0-M, Cluster 5.0, Atomic 5.0, Promo NA) in CPQ v28; compare against `04_server_selectable_options.csv`
6. RACI confirmation: lock named owners for Product/Sales Ops/Procurement before prod go-live

## Decisions Made
- Database: Supabase (Postgres) — portable via pg_dump; standard SQL; table editor for non-technical users
- ID type: BIGSERIAL integers — simpler, smaller, faster joins
- Root currency: CAD = 1 (is_base = true; never appears in fx_rates as target)
- FX direction: 1 CAD = N foreign (multiply CAD→foreign, divide foreign→CAD); confirmed by Finance: 1 CAD = 1.3651 USD
- CAD pricing: Stored explicitly in product_pricing, not derived — prevents quoted prices shifting when FX moves
- FX governance: Finance-maintained with cad_pricing_rebased audit flag for intentional repricing vs. passive drift
- CapEx model: Time-series with procured_price/currency/date; CAD derived via LATERAL join to fx_rates; use_as_baseline flag for excluding discounted batches
- Specs structure: One table per category (server_specs, component_specs, future firewall_specs/switch_specs); drive_type column handles SSD/NVMe/HDD/SAS distinctions
- Component compatibility: Via server_selectable_options only; no separate matrix for POC
- MH/DH: Unified as "Hosting" in product_catalog; configurator decides what's included
- Product types: Self-referencing lookup table with parent_code for hierarchy
- Lifecycle: Queryable date columns (release_date, end_of_sale_date, end_of_support_date, end_of_service_life_date)
- Deprecated products: Soft-delete (is_active = false) — preserves history and FK safety
- Colo: Out of scope for POC; include as inactive rows so schema is ready when colo work begins
- Financial model (EBIT/IRR/NPV): Out of scope — computation, not data; stays in Excel during POC
- fusion_id gaps: TEMP- placeholders tracked in pending_fusion_id table; POC unblocked but prod blocked until resolved
- Rollback: CPQ v28 not retired until one full sales cycle completed, Finance validates prices, and all RACI rows have named owners

## Delegation State
| Person | Owns | By When | Level | Status |
| ------ | ---- | ------- | ----- | ------ |
| CFO (or delegate) | fx_rates, overhead_constants maintenance | Ongoing | Owner | Confirmed |
| Sales Ops (TBD) | Promo NRC confirmation | Before seed data | Consulted | Pending |
| Sales Ops (TBD) | Compatibility validation (5 servers) | Before POC complete | Responsible | Pending |
| Product (TBD) | Lifecycle dates, new product additions | Before prod | Owner | Pending |
| Procurement (TBD) | product_capex entries | Before prod | Owner | Pending |