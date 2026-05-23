# Renewals Reference: Data Sources, Flow, and Gaps

> **Last updated:** 2026-05-23
> **Scope:** The Renewals section — finding expiring customer services, reviewing current vs. new pricing, and calculating suggested renewal MRC with margin.
> **Code base:** `routes/renewals.py` + `db/mssql.py` + `lib/renewal_pricing.py` + `lib/overhead.py` + `cost_drivers.json` + `templates/renewals.html` + `templates/renewal.html`

---

## Table of Contents

1. [Data Sources](#1-data-sources)
2. [Renewal List Flow (`/renewals`)](#2-renewal-list-flow-renewals)
3. [Renewal Detail Flow (`/renewal/<service_id>`)](#3-renewal-detail-flow-renewalservice_id)
4. [Suggested MRC Formula](#4-suggested-mrc-formula)
5. [Known Gaps](#5-known-gaps)
6. [How This Data Gets Maintained](#6-how-this-data-gets-maintained)

---

## 1. Data Sources

All renewal data originates from MSSQL (`DM_BusinessInsights`). Fusion PostgreSQL is used only to look up current component pricing and DC metadata for overhead FX conversion.


| Data Item                      | Database          | Server / File                   | Table                                              | Key Columns                                                                                                                                  | Notes                                                                                                                                                                                                                      |
| ------------------------------ | ----------------- | ------------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Renewal service list**       | MSSQL             | `DM_BusinessInsights`           | `renewals.ocean_services_renewal_date`             | `client_id, company_name, service_id, expiration_date, m2m`                                                                                  | View/table maintained by the BI team. Joined to `dbo.dimServices`. `m2m` is a varchar (`'yes'`/`'no'`/`''`/NULL) — not a boolean. Sentinel date `1899-12-31` means "no expiration date set".                               |
| **Service detail**             | MSSQL             | `DM_BusinessInsights`           | `dbo.dimServices`                                  | `service_id, client_id, company_name, product, datacenter_code, currency, mrc, usd_mrc, cad_mrc, provision_date, service_status, service_type, fusion_id, nickname, contract_months_remaining, last_updated` | `fusion_id` maps to `product_catalog.id` in Fusion — the bridge for pricebook and HW CapEx lookups. May be null for older services. `mrc` is in the service's billing currency.                                           |
| **Service components**         | MSSQL             | `DM_BusinessInsights`           | `dbo.dimComponents`                                | `service_id, component_id, component, component_category, component_type, component_mrc, product_mrc, currency, is_online, datacenter_code, line_of_business, add_on` | `product_mrc` = base server MRC (same value repeated across all component rows for a service). `component_mrc` = per-component add-on charge (0 for included components). Total contracted MRC = `product_mrc` + Σ `component_mrc` = `dimServices.mrc`. |
| **Current pricebook prices**   | Fusion PostgreSQL | `db1.peer1.com` (via SSH tunnel) | `public.pricebook`                                 | `component_id, mrc, currency, is_available`                                                                                                  | Used to re-price SW/Support components at renewal. **No DC filter** — prices are treated as uniform across all DCs for the same currency. Currency fallback order: service currency → CAD → USD → GBP → EUR.               |
| **HW CapEx**                   | MSSQL             | `DM_BusinessInsights`           | `profitability.ocean_sku_cost`                     | `sku_id, sku_cost, cost_currency, sku_level`                                                                                                 | `sku_id = dimServices.fusion_id`, `sku_level = 'TLS'`. Returns the all-in hardware cost of the server. Zero or missing if `fusion_id` is null. Converted to service billing currency via FX.                              |
| **Power wattage**              | MSSQL             | `DM_BusinessInsights`           | `profitability.hardware_watts`                     | `fusion_id, watts`                                                                                                                           | `fusion_id = dimServices.fusion_id`. Used for power cost line in overhead. Shows N/A if row is missing or `fusion_id` is null.                                                                                             |
| **FX rates**                   | MSSQL             | `DM_BusinessInsights`           | `dbo.dimCurrencyExchangeRates`                     | `from_currency, to_currency, exchange_rate, start_date`                                                                                      | `SELECT TOP 1 … ORDER BY start_date DESC`. Used for pricebook currency fallbacks and for converting HW CapEx and overhead amounts to the service billing currency.                                                         |
| **Overhead rates**             | Local file        | —                               | `cost_drivers.json`                                | `data_centers[dc_code].costs.server[key]`, `overhead_constants.sga_pct`                                                                     | Amounts in DC native currency; 7 DCs covered (ATL, IAD, LAX, MIA, MTL, POR, TOR). Services in other DCs show $0 overhead. See the Settings reference for full details.                                                    |
| **DC info (overhead FX only)** | Fusion PostgreSQL | `db1.peer1.com` (via SSH tunnel) | `public.sb_datacenter` + `datacenter_available_currencies` | `dc_abbr, id, native_currency`                                                                                               | Used only to resolve the DC's native currency so overhead amounts from `cost_drivers.json` can be FX-converted to the service billing currency. Not used for pricebook lookups.                                            |

---

## 2. Renewal List Flow (`/renewals`)

### What the list shows

The renewals list (`GET /api/renewals`) returns customer services grouped by **(client_id + expiration_date)**. A client with three services all expiring on the same date appears as one expandable group row. A client with services on two different dates gets two separate rows.

### Filters

The list accepts these optional query parameters:

| Parameter   | Type    | Behavior                                                   |
| ----------- | ------- | ---------------------------------------------------------- |
| `company`   | string  | Case-insensitive contains match on `company_name`          |
| `client_id` | integer | Exact match                                                |
| `service_id`| integer | Exact match (returns a single-service result)              |
| `m2m_only`  | flag    | `=1` to show only month-to-month services                  |

### Sorting

Services are sorted in this order:
1. Real future expiration dates, ascending (soonest to expire at top)
2. M2M services and sentinel dates (1899-12-31, which means "no date set") sorted to the bottom

### Group row fields

Each group row shows:

| Field          | Value                                                     |
| -------------- | --------------------------------------------------------- |
| Company        | `company_name`                                            |
| Client ID      | `client_id`                                               |
| Services       | Count (e.g., "3 services")                                |
| DC             | Single DC code if all services are in the same DC, else "Mixed" |
| Product        | Single product name if all services are the same product, else "Mixed" |
| MRC            | Sum of all service MRCs in the group (in each service's own currency — see Gap #3) |
| Expires        | Formatted date, "m2m" badge, or "—"                       |

**Expiration display logic:**
- `expiration_date` is a real future date → formatted date shown
- `m2m = 'yes'` in the database → "m2m" badge
- Otherwise → "—"

### Navigating to a service

Clicking a group row expands it to show individual service rows. Clicking a service row navigates to `/renewal/<service_id>` for the full pricing detail.

---

## 3. Renewal Detail Flow (`/renewal/<service_id>`)

### What the page shows

The renewal detail page (`GET /api/renewals/<service_id>`) shows:

- The service's current contracted components and prices
- Each component's current pricebook price vs. what was contracted
- Four pre-calculated renewal scenarios: m2m, 12-month, 24-month, 36-month
- Full cost breakdown (HW CapEx, overhead, SG&A) and resulting margin per scenario

### Data assembly sequence

1. **Load service** — `dimServices WHERE service_id = ?` → gets `currency`, `datacenter_code`, `fusion_id`, `provision_date`, `mrc`
2. **Load components** — `dimComponents WHERE service_id = ?` → gets all contracted components with their current MRCs and categories
3. **Get DC info** — Fusion `sb_datacenter` → gets `native_currency` for overhead FX conversion only
4. **Get FX rates** — MSSQL `dimCurrencyExchangeRates` → rates for currency fallback chain (CAD, USD, GBP, EUR → service currency)
5. **Re-price components** — for each component with a `component_id`, query Fusion `pricebook WHERE component_id = ? AND currency = ? AND is_available = true` (no DC filter). Try service currency first; fall back through CAD → USD → GBP → EUR.
6. **Get HW CapEx** — MSSQL `ocean_sku_cost WHERE sku_id = fusion_id AND sku_level = 'TLS'`; convert to service currency via FX
7. **Get power wattage** — MSSQL `hardware_watts WHERE fusion_id = ?`; convert watts to kW
8. **Calculate overhead** — `cost_drivers.json` for the DC; convert native amounts to service currency via FX
9. **Pre-calculate all four term scenarios** server-side; return together so the term selector switches with zero round-trips

### Component re-pricing rules

| Component category    | How new MRC is determined                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------ |
| **Software, Support** | Re-priced at current Fusion pricebook MRC. If not found in pricebook: `in_pricebook = false`, `new_mrc = null`, falls back to contracted price for suggested MRC calculation. |
| **Hardware, Bandwidth, Network, Other** | Held flat at contracted MRC — no re-pricing applied.                            |

### HW paid-off rule

If `provision_date` is 36 months or more before today, the hardware is considered fully paid off and HW cost = $0 in all term scenarios. Otherwise HW CapEx is amortized over the term: `ocean_sku_cost.sku_cost ÷ term_months`.

### API response structure

```json
{
  "service": { ...dimServices fields... },
  "components": [
    {
      "component_id": 4904,
      "component": "Plesk Web Host Edition...",
      "component_category": "Software",
      "component_type": "Plesk",
      "component_mrc": 85.00,
      "new_mrc": 85.00,
      "delta": 0.00,
      "in_pricebook": true,
      "warning": null
    }
  ],
  "product_mrc": 1699.00,
  "hw_capex": 7569.00,
  "hw_capex_currency": "USD",
  "hw_paid_off": false,
  "provision_age_months": 13,
  "kw": 0.384,
  "sga_pct": 0.082,
  "pricing": {
    "m2m":  { "suggested_mrc": ..., "hw_cost_mo": ..., "overhead_lines": {...}, "overhead_total": ..., "total_cost": ..., "margin": ..., "margin_pct": ... },
    "12":   { ... },
    "24":   { ... },
    "36":   { ... }
  }
}
```

---

## 4. Suggested MRC Formula

All amounts are in the service's billing currency.

```
base_mrc = product_mrc                           ← base server MRC, held flat
         + Σ new_pricebook_mrc                   ← for Software/Support components
             (falls back to component_mrc if not in pricebook)
         + Σ component_mrc                       ← for Hardware/Bandwidth/Network components

suggested_mrc = base_mrc × 1.25                  ← if term = m2m
              = base_mrc × 1.0                   ← if term = 12/24/36 months

HW CapEx/mo   = 0                                ← if provision_date ≥ 36 months ago (paid off)
              = ocean_sku_cost[sku_level='TLS',
                  sku_id=fusion_id].sku_cost × fx
                ÷ term_months                    ← otherwise, amortized

Power/mo      = hardware_watts[fusion_id].watts
                ÷ 1000 × cost_drivers[dc].power_per_kw × fx_overhead
              = N/A if hardware_watts row missing or fusion_id null

Overhead/mo   = Σ cost_drivers[dc].costs.server[key] × fx_overhead
              + (suggested_mrc × sga_pct)        ← SG&A (currently 8.2%)

Total Cost/mo = HW CapEx/mo + Power/mo + Overhead/mo

Margin/mo     = Suggested MRC − Total Cost/mo
Margin %      = Margin ÷ Suggested MRC × 100
```

**FX notes:**
- `cost_drivers.json` amounts are in the DC's native currency. `fx_overhead = get_fx_rate(native_currency, service_currency)` converts them.
- `ocean_sku_cost.sku_cost` has its own `cost_currency` column. It is converted to service currency independently.
- Pricebook prices are returned in the matched currency and converted to service currency via `dimCurrencyExchangeRates` if needed.

---

## 5. Known Gaps


| #  | Gap                                         | Current behavior                                                                                                           | Correct / desired behavior                                                                                                            |
| -- | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| 1  | `fusion_id` null on older services          | HW CapEx = $0, power = N/A, pricebook re-pricing skipped for the server base                                               | `fusion_id` should be backfilled for all active services in `dimServices` — requires BI/Ocean data work                               |
| 2  | `m2m` is varchar, not boolean               | App converts `'yes'` → `True`, anything else → `False`. Values like `1`, `true`, `YES` would be treated as non-m2m.       | Ensure `ocean_services_renewal_date.m2m` only contains `'yes'`/`'no'`/NULL — BI team must validate and standardize                    |
| 3  | MRC summation in list is cross-currency     | Group MRC sums all service MRCs regardless of currency (e.g., USD + GBP summed as if equal)                                | Should convert to a common display currency before summing, or show each currency separately                                          |
| 4  | Pricebook lookup has no DC filter           | Prices assumed uniform by currency across all DCs. A component priced differently at CRO vs. IAD in the same currency would show the wrong price. | Confirm with Finance/Fusion team that pricebook prices are indeed uniform by currency across DCs, or add DC filter                    |
| 5  | Sentinel expiration date `1899-12-31`       | Normalized to `null` in API; displayed as "—". No warning surfaced to user that the date may be a data quality issue.      | Consider flagging sentinel dates visually so account teams know to investigate the contract record in Ocean                            |
| 6  | `hardware_watts` coverage gaps              | Services whose `fusion_id` has no row in `hardware_watts` show power = N/A                                                 | `hardware_watts` must be populated for all active server SKUs — see New Quotes reference for the same gap                             |
| 7  | `cost_drivers.json` DC coverage gaps        | Services at DCs outside the 7 covered (ATL, IAD, LAX, MIA, MTL, POR, TOR) show $0 overhead                                | Add overhead rates for all DCs where active services exist                                                                            |
| 8  | Components not in pricebook                 | `in_pricebook = false`, `new_mrc = null`, `warning = "not_in_pricebook"`. SW/Support components fall back to contracted price in suggested MRC calculation. | Investigate: is the component retired (and should be flagged as removed)? Or is it simply missing from Fusion's `product_allowed_components`? |
| 9  | No write-back to any system of record       | Renewal quotes are display-only — no way to submit or record a renewal decision from the tool                              | Future: integration with Ocean or CRM to record accepted renewal terms                                                                |
| 10 | Multi-service renewal quoting not supported | Each service is quoted individually; a client group cannot be quoted as one transaction                                     | Future: group-level renewal with a single suggested MRC across all services in a group                                                |

---

## 6. How This Data Gets Maintained

### `ocean_services_renewal_date` and `dimServices`

These are read-only data warehouse tables maintained by the BI team. They are populated automatically from Ocean (the billing/provisioning system) and the data warehouse ETL pipeline. **They cannot be edited through the CPQ tool.**

When a service contract is updated in Ocean (e.g., renewal date extended, MRC changed), those changes flow into `dimServices` and `ocean_services_renewal_date` on the next ETL cycle. The CPQ tool always reflects the current state of the DW.

If renewal dates or MRC values look wrong, the fix must happen in Ocean — not in the CPQ.

### `dimComponents`

Also read-only and ETL-populated from Ocean. Component MRCs in `dimComponents` reflect what the customer was contracted to pay at provisioning or last renewal. They are not updated when Fusion pricebook prices change — that's intentional: `dimComponents` is a historical record of the contracted price, while the Fusion pricebook is the current list price.

### `fusion_id` on `dimServices`

This is the bridge between the billing DW and Fusion's product catalog. It maps `dimServices.service_id` to `product_catalog.id` in Fusion, which enables pricebook lookups and HW CapEx retrieval. If `fusion_id` is null or wrong on a service record:

- Pricebook re-pricing works only at the component level (component_ids from `dimComponents` are still used)
- HW CapEx from `ocean_sku_cost` will be $0 (no server-level lookup possible)
- Power cost will be N/A

Backfilling `fusion_id` for affected services requires coordination between the BI team (who own `dimServices`) and the Ocean/provisioning team (who maintain `product_catalog`).

### Fusion pricebook

The Fusion pricebook is maintained by the Finance/Sales Ops team through Ocean. Changes to pricebook MRCs (for components) flow through automatically the next time a renewal detail page is loaded — there is no caching of component prices in the CPQ.

### `cost_drivers.json`

Overhead rates. Edited via the Settings page or directly in the file. See the Settings reference for full details on structure and maintenance.
