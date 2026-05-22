# Renewals Section Design

**Date:** 2026-05-22  
**Status:** Approved  
**Scope:** Add a Renewals section to the CPQ front-end alongside the existing New Quotes section, and refactor the app structure to support both.

---

## Background

The current CPQ app is CPQ-specific (new quotes only): a server list page and a configurator page, backed by a single monolithic `app.py`. This design adds a Renewals section for quoting contract renewals against existing customer services, and reorganizes the codebase to cleanly support both sections.

---

## Architecture

### Approach: Option B — Jinja2 template inheritance + modular backend

`app.py` becomes a thin wiring file (~20 lines). Logic is split into focused modules.

### File Structure

```
app.py                          ← Flask init + blueprint registration only
db/
  fusion.py                     ← Postgres tunnel, get_conn(), get_dc_registry(),
                                   get_dc_info(), get_fx_rate()
  mssql.py                      ← get_mssql_costs(), get_mssql_watts(),
                                   renewal queries (dimServices, dimComponents,
                                   ocean_services_renewal_date)
lib/
  overhead.py                   ← calc_overhead(), COST_DRIVERS loader
routes/
  cpq.py                        ← existing CPQ routes: /api/datacenters,
                                   /api/servers, /api/product/*
  renewals.py                   ← new renewal routes: /api/renewals,
                                   /api/renewals/<service_id>
  settings.py                   ← /settings, /api/settings/overhead
templates/
  base.html                     ← shared: font-faces, CSS tokens, header,
                                   top nav, theme toggle JS
  index.html                    ← extends base.html (new quotes list)
  product.html                  ← extends base.html (CPQ configurator)
  renewals.html                 ← extends base.html (renewals list table)
  renewal.html                  ← extends base.html (renewal detail)
  settings.html                 ← extends base.html (overhead settings)
cost_drivers.json
```

---

## Navigation

`base.html` adds a top nav bar to the shared header:

```
[Aptum logo]  |  New Quotes    Renewals    Settings        [theme toggle]
                  ──────────
                  (active underline)
```

- Active section highlighted with accent-color underline.
- Active state set server-side via `active_page` template variable — no JS flash.
- The static "Server Pricing" label next to the logo is removed; the active nav item provides that context.
- Font-face declarations, CSS token definitions (`:root` / `[data-theme]`), and `toggleTheme()` / `initTheme()` JS move to `base.html` — currently duplicated across all templates.

---

## Renewals List Page (`/renewals`)

### API

`GET /api/renewals?company=&client_id=&service_id=&page=1&per_page=50`

**Response fields per row:** `service_id`, `client_id`, `company_name`, `product`, `datacenter_code`, `currency`, `mrc`, `provision_date`, `expiration_date`, `m2m`, `contract_months_remaining`, `service_status`, `service_type`

**Sorting:** expiration_date ascending (soonest first); sentinel dates (1899-12-31) and NULLs sorted to bottom.

**Filtering:** `company` = case-insensitive contains match on `company_name`; `client_id` and `service_id` = exact match.

### Grouping

Rows are grouped by **(client_id + expiration_date)**. A client with multiple services sharing the same expiration date collapses into one expandable group row. A client with services on two different dates gets two separate group rows.

**Group row columns:**

| Column | Value |
|---|---|
| Company | company_name |
| Client ID | client_id |
| Services | "3 services" |
| DC | single DC code if all same, else "Mixed" |
| Product | single product name if all same, else "Mixed" |
| MRC | sum of all service MRCs in the group |
| Expires | expiration_date (formatted), "m2m" badge, or "—" |
| Status | "Online" / mixed |

Single-service rows show flat (no chevron, no expand).

**Expand behavior:** clicking the ▶ chevron expands inline child rows showing individual service details. Clicking a child row navigates to `/renewal/<service_id>`.

**Expiration display logic:**
- `expiration_date > 1900-01-01` → formatted date
- `m2m = 'yes'` → "m2m" badge
- Otherwise → "—"

---

## Renewal Detail Page (`/renewal/<service_id>`)

### API

`GET /api/renewals/<service_id>`

**Data sources:**
- `DM_BusinessInsights.dbo.dimServices` — service metadata, `provision_date`, `fusion_id`, `mrc`, `currency`, `datacenter_code`
- `DM_BusinessInsights.dbo.dimComponents` — current contracted components and prices
- `Fusion.public.pricebook` + `product_allowed_components` — current pricebook prices per component
- `DM_BusinessInsights.profitability.ocean_sku_cost` — HW CapEx cost (via `fusion_id`)
- `cost_drivers.json` — DC overhead rates

**Response structure:**
```json
{
  "service": { ...dimServices fields... },
  "components": [
    {
      "component_id": 4904,
      "component": "Plesk Web Host Edition...",
      "component_category": "Software",
      "component_type": "Plesk",
      "current_mrc": 85.00,
      "new_mrc": 85.00,
      "delta": 0.00,
      "in_pricebook": true,
      "warning": null
    },
    ...
  ],
  "hw_capex": 7569.00,
  "hw_capex_currency": "USD",
  "provision_age_months": 13,
  "hw_paid_off": false,
  "overhead": { ...same shape as CPQ overhead... },
  "pricing": {
    "m2m":  { "suggested_mrc": ..., "hw_cost": ..., "sw_cost": ..., "overhead_total": ..., "margin": ..., "margin_pct": ... },
    "12mo": { ... },
    "24mo": { ... },
    "36mo": { ... }
  }
}
```

All four term scenarios are pre-calculated server-side and returned together so the term selector in the UI switches with zero round-trips.

### Page Layout

Two-column layout (same pattern as CPQ configurator):

**Left column — component list:**
- Grouped by `component_category` (Hardware, Bandwidth, Network, Software, Support, etc.)
- Each component row: name | current MRC → new MRC | delta (orange if increase, green if decrease, neutral if same)
- ⚠ warning badge if `component_id` not found in `product_allowed_components` for this DC — component is still displayed, not hidden
- `product_mrc` (base server MRC) shown as a header row above components

**Right column — sidebar:**
- Service header: company name, service ID, product, DC, currency, provision date, current MRC
- Term selector buttons: `m2m` / `12mo` / `24mo` / `36mo` — switches active term, recalculates display from pre-loaded data (no API round-trip)
- Summary table:

| Line | Value |
|---|---|
| Current MRC | current contracted total |
| SW/Support Δ | sum of increases on Software + Support components only |
| New base MRC | current product_mrc + new SW/Support prices + unchanged HW add-on prices |
| M2M uplift | ×1.25 (shown only when m2m selected) |
| **Suggested MRC** | **final recommended renewal price** |
| HW cost | $0 if hw_paid_off, else amortized CapEx/mo |
| SW cost | sum of pricebook costs for SW components |
| Overhead | from cost_drivers.json |
| Total cost | HW + SW + overhead |
| Margin | Suggested MRC − Total cost |
| Margin % | Margin ÷ Suggested MRC |

- "Copy quote" button (same pattern as CPQ)

### Business Logic

**Hardware paid-off rule:** if `provision_date` is ≥ 36 months before today, HW cost = $0. Otherwise HW CapEx is amortized: `ocean_sku_cost (sku_id = fusion_id, sku_level='TLS') ÷ remaining_months`.

**Suggested MRC formula:**
```
base = product_mrc (unchanged)
     + Σ new_pricebook_mrc for Software/Support components
     + Σ current_mrc for Hardware/Bandwidth/Network components  ← HW add-on prices held flat
suggested = base × (1.25 if m2m else 1.0)
```

**Component pricebook lookup:** `Fusion.public.pricebook WHERE component_id = ? AND datacenter = fusion_dc_id AND currency = service_currency AND is_available = true`. Falls back to native currency + FX if no direct-currency row exists (same pattern as CPQ).

**Missing component handling:** if `component_id` is not in `product_allowed_components` for this DC, `in_pricebook = false`, `new_mrc = null`, `warning = "not_in_pricebook"`. The component still appears in the UI with a warning.

---

## Data Notes

- `dimServices.fusion_id` maps to `product_catalog.id` in Fusion — this is the bridge for pricebook and CapEx lookups.
- `dimComponents.product_mrc` = base server MRC (same value repeated across all component rows for a service).
- `dimComponents.component_mrc` = per-component add-on charge (0 for included components).
- Total contracted MRC = `product_mrc` + Σ `component_mrc` = `dimServices.mrc` ✓
- `ocean_services_renewal_date.m2m` is a varchar (`'yes'`/`'no'`/`''`/NULL) — not a boolean.
- Sentinel expiration date `1899-12-31` should be treated as "no specific date" in display logic.
- The renewals table covers all service types (not filtered to servers only).

---

## Out of Scope

- Fixing/updating the term handling in the New Quotes section (noted as future work).
- Writing the quote back to any system of record.
- Multi-service renewal quoting (quoting a group of services as one transaction).
