# Profitability Page — Design Spec

**Date:** 2026-05-26  
**Status:** Awaiting user approval

---

## Overview

A new "Profitability" page added to the CPQ front-end nav alongside New Quotes, Renewals, and Settings. Provides an executive-level view of margin across all customers, with drill-down to the service level and a cost breakdown sidebar matching the Renewals detail page. All calculations use the same CPQ cost model already used by New Quotes and Renewals — no FinancialReporting or Profit_Analysis tables.

---

## Navigation

Add `Profitability` as a nav link in `base.html`, positioned between New Quotes and Renewals:

```
New Quotes | Profitability | Renewals | Settings
```

Active state uses `active_page == 'profitability'`, same pattern as existing pages.

---

## Data Sources

### Revenue (MRC)
- **Primary:** Fusion PostgreSQL — `public.customer_products` joined to `public.customers` and `public.sb_datacenter`
- **Fallback:** `DM_BusinessInsights.dbo.dimServices` + `dbo.dimComponents` when a service has no Fusion record

### Hardware Cost
- `DM_BusinessInsights.profitability.ocean_sku_cost` — CapEx per SKU (same query used in Renewals)
- Amortization: `CapEx / term_months`. If service age > 36 months, hardware cost = $0 (paid off)
- Service age measured from `first_online` in Fusion `customer_products`; fall back to `provision_date` in `dimServices` if no Fusion record — same logic as `lib/renewal_pricing.py`
- SKU matched at TLS (server) level first, component level as fallback

### Power / Overhead
- `DM_BusinessInsights.profitability.hardware_watts` — watts per `fusion_id`
- `cost_drivers.json` — power rate per kW, DC ops, network equipment, support ops, network ops per device, SG&A % — all keyed by DC code
- Reuses `lib/overhead.py` `calc_overhead()` unchanged

### Customer / AM Master
- `DM_BusinessInsights.dbo.dimClientsActive` — `client_id`, `company_name`, `account_manager`

### FX Rates
- `DM_BusinessInsights.dbo.dimCurrencyExchangeRates` — same table used by New Quotes
- Exposed via existing `/api/fx-rate?from=CAD&to=USD` endpoint; no new endpoint needed

---

## Cost Calculation (per service)

```
margin_$ = mrc - total_cost

total_cost = hw_amortized + direct_overhead + sga

hw_amortized  = capex / term_months          (0 if service_age > 36 months)
direct_overhead = power_cost + dc_ops + network_equipment + support_ops + network_ops
power_cost    = (watts / 1000) * power_per_kw[dc]
sga           = mrc * sga_pct                (from cost_drivers.json)

margin_pct = margin_$ / mrc * 100
```

This is identical to the logic in `lib/overhead.py` and `lib/renewal_pricing.py`.

---

## Currency Handling

- **Default view:** each service/customer displayed in its native billing currency (USD, CAD, GBP, etc.)
- **KPI rollup cards:** show "—" when currencies are mixed (no single display currency selected). A customer with services billed in both CAD and USD is `currency_mixed: true`; its MRC/cost/margin fields in the API response are `null` until the caller requests a display currency via `?display_currency=USD`.
- **Display currency selector:** dropdown in the page header (not the global nav), same style as the DC/currency selectors in New Quotes. Options: USD, CAD, GBP, EUR (whatever currencies exist in the FX table)
- **Conversion:** done client-side in JavaScript using rates fetched once on page load from `/api/fx-rate`. Same pattern as New Quotes product configurator.
- When a display currency is active: all MRC, cost, and margin values are multiplied by the fetched rate; KPI rollup cards become live totals.

---

## Pages

### 1. `/profitability` — Landing Page

**Layout:** `page-body` with 2rem padding, consistent with all other pages.

**KPI cards (4-up row):**
- Total MRC
- Total Cost
- Net Margin ($)
- At-Risk count (services with margin < 10%)

Cards show "—" when currencies are mixed. Populate when display currency is selected.

**Filter bar** — identical card/component to Renewals (`filter-bar` class):
- Account Manager — multi-select combo (data from `dimClientsActive.account_manager`)
- Data Center — multi-select combo (data from `sb_datacenter`)
- Service Type — multi-select combo (data from `dimServices.service_type`)
- Customer — free-text search input

**Segment toggle** — pill-style toggle above the table:
- By Customer *(default)*
- By Data Center
- By Service Type

Switching segment changes the table rows and the first column header. Filters remain applied across all segments.

**Table columns (By Customer):**

| Column | Notes |
|--------|-------|
| Customer | links to `/profitability/<client_id>` |
| Account Manager | from `dimClientsActive` |
| Services | count of active services |
| MRC | native currency or converted |
| Total Cost | native currency or converted |
| Margin $ | native currency or converted; red if negative |
| Margin % | colored text only — green (≥20%), orange (10–19%), red (<10%) |

By Data Center and By Service Type use the same columns minus Account Manager.

Table is sortable by any column. Default sort: Margin % ascending (worst first).

No pills, no bar charts — margin % plain text with color only.

---

### 2. `/profitability/<client_id>` — Customer Detail Page

**Layout:** same two-column layout as Renewal detail — `1fr 360px` grid with a sticky sidebar.

**Back link:** `← All Customers` → `/profitability`

**Page header:** Customer name, client_id, account manager, total active service count.

**KPI cards (4-up):** same as landing page but scoped to this customer.

**Service table** — one row per active service:

| Column | Notes |
|--------|-------|
| Service / Nickname | fusion service nickname or service_id |
| DC | `dc-badge` (ATL, TOR, etc.) |
| Type | service_type |
| MRC | native or converted |
| Cost | native or converted |
| Margin $ | red if negative |
| Margin % | colored text, same thresholds |

Clicking a row loads the cost breakdown in the sidebar. First row selected by default.

**Sidebar — Cost Breakdown:**
- Section: Revenue → MRC
- Section: Costs → itemized: HW amortization (with CapEx / term callout), Power (with watts · rate callout), DC Ops, Network Equipment, Support Ops, Network Ops, subtotal, SG&A, Total Cost
- Section: Margin → Margin $, Margin %, biggest cost driver (which line item is the largest %), HW paid-off countdown ("HW paid off in N months" or "HW fully amortized")
- Button: `Open Renewal →` → links to `/renewal/<service_id>` (existing page)

Sidebar uses `surface-card` + `cost-table` styles identical to the Renewal detail sidebar.

---

## New Files

| File | Purpose |
|------|---------|
| `routes/profitability.py` | Blueprint: `/profitability` and `/profitability/<client_id>` HTML routes + `/api/profitability` and `/api/profitability/<client_id>` JSON endpoints |
| `templates/profitability.html` | Landing page template |
| `templates/profitability_customer.html` | Customer detail template |
| `db/profitability.py` | Data access: fetch all active services with MRC + cost components; aggregate by customer/DC/service type |

## Modified Files

| File | Change |
|------|--------|
| `app.py` | Register `profitability` blueprint |
| `templates/base.html` | Add Profitability nav link |

---

## API Endpoints

### `GET /api/profitability`
Returns all active services with precomputed cost breakdown. Query params: `am`, `dc`, `service_type`, `customer` (filter). Response shape:

```json
{
  "by_customer": [
    {
      "client_id": 4821,
      "company_name": "GlobalBank Financial",
      "account_manager": "Sarah Chen",
      "service_count": 7,
      "currency": "USD",
      "currency_mixed": false,
      "mrc": 31800,
      "total_cost": 24500,
      "margin": 7300,
      "margin_pct": 23.0
    }
  ],
  "by_dc": [...],
  "by_service_type": [...]
}
```

### `GET /api/profitability/<client_id>`
Returns all services for one customer with per-service cost breakdown:

```json
{
  "client_id": 4821,
  "company_name": "GlobalBank Financial",
  "account_manager": "Sarah Chen",
  "services": [
    {
      "service_id": "SRV-003",
      "nickname": "Backup Node",
      "dc": "TOR",
      "service_type": "Dedicated Server",
      "currency": "CAD",
      "mrc": 4400,
      "costs": {
        "hw_amortized": 2150,
        "power": 487,
        "dc_ops": 312,
        "network_equipment": 59,
        "support_ops": 580,
        "network_ops": 0,
        "sga": 360.80,
        "total": 3948.80
      },
      "margin": 451.20,
      "margin_pct": 10.3,
      "hw_months_remaining": 22,
      "biggest_cost_driver": "hw_amortized"
    }
  ]
}
```

---

## Design Consistency Rules

- All styles inherit from `base.html` CSS variables — no new variables introduced
- Filter bar: copy `filter-bar`, `filter-group`, `combo-trigger`, `combo-chip` classes from `renewals.html`
- Tables: `prof-table` follows exact same `th`/`td` patterns as `comp-table` in `renewal.html`
- Sidebar: `surface-card` + `cost-table` + `section-title` — identical to `renewal.html` sidebar
- Margin color thresholds: green ≥ 20%, orange 10–19%, red < 10% (plain text, no pills or bars)
- Currency display: `Geist Mono` font, right-aligned, 2 decimal places

---

## Out of Scope

- FinancialReporting tables (`Profit_Analysis`, `Profit_Cost`, `finance_revenue_mapping`) — not used
- Historical trending / time-series charts
- Export to CSV/Excel
- Editing MRC or costs from this page (use Renewals for repricing)
