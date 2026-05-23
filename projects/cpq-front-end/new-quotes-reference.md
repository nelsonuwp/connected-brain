# New Quotes Reference: Data Sources, Quoting Flow, and Roadmap

> **Last updated:** 2026-05-23
> **Replaces:** `cpq-reference.md`, `cpq-data-flow.md`, `cpq-quoting-flow.md`
> **Code base:** `app.py` (Flask wiring) + `routes/cpq.py` + `db/fusion.py` + `db/mssql.py` + `lib/overhead.py` + `cost_drivers.json` + `templates/index.html` + `templates/product.html`

---

## Table of Contents

1. [Data Sources](#1-data-sources)
2. [Active / Available Filtering](#2-active--available-filtering)
3. [Current State — Quoting Flow](#3-current-state--quoting-flow)
4. [Cost Calculation Formula](#4-cost-calculation-formula)
5. [Known Gaps](#5-known-gaps)
6. [Future Work / To-Do](#6-future-work--to-do)
7. [Product Catalog Changes — -D and -vHost Deprecation](#7-product-catalog-changes---d-and--vhost-deprecation)
8. [Production Readiness Assessment](#8-production-readiness-assessment)

---

## 1. Data Sources

**Largely correct. Two additions: there is a second MSSQL table (`hardware_watts`) used for power cost, and the DC list now comes from Fusion, not a static file.**


| Data Item                        | Database          | Server                                                  | Table / File                                            | Key Columns                                                                          | Notes                                                                                                                                                                              |
| -------------------------------- | ----------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **DC list**                      | Fusion PostgreSQL | `db1.peer1.com` (via SSH tunnel through `10.121.21.20`) | `public.sb_datacenter`                                  | `id, dc_abbr, name, city, state, active`                                             | Queried live; falls back to `cost_drivers.json` if Fusion unreachable                                                                                                              |
| **DC currencies**                | Fusion PostgreSQL | `db1.peer1.com` (via SSH tunnel through `10.121.21.20`) | `public.datacenter_available_currencies`                | `datacenter_id, currency_code`                                                       | Joined with `sb_datacenter` at startup; all available currencies per DC                                                                                                            |
| **DC native currency**           | Fusion PostgreSQL | `db1.peer1.com` (via SSH tunnel through `10.121.21.20`) | `public.datacenter_available_currencies`                | `datacenter_id, currency_code`                                                       | Single-currency DCs: sole DB entry is native. Multi-currency DCs (e.g., TOR: CAD + USD): `cost_drivers.json` provides the explicit override; falls back to first DB entry          |
| **FX rates**                     | MSSQL             | `DM_BusinessInsights`                                   | `dbo.dimCurrencyExchangeRates`                          | `from_currency, to_currency, exchange_rate, start_date`                              | `SELECT TOP 1 … ORDER BY start_date DESC`                                                                                                                                          |
| **Server list (pricing)**        | Fusion PostgreSQL | `db1.peer1.com` (via SSH tunnel through `10.121.21.20`) | `public.product_catalog` JOIN `public.pricebook`        | `pc.id, pc.name, pb.mrc, pb.nrc, pb.setup, pb.is_available`                          | `component_id IS NULL` identifies server-level rows                                                                                                                                |
| **Default components**           | Fusion PostgreSQL | `db1.peer1.com` (via SSH tunnel through `10.121.21.20`) | `public.product_templates`                              | `product_id, component_id, quantity`                                                 | Joined to `components`, `component_types`, `component_categories`, `pricebook`                                                                                                     |
| **Available components**         | Fusion PostgreSQL | `db1.peer1.com` (via SSH tunnel through `10.121.21.20`) | `public.product_allowed_components`                     | `product_id, component_id`                                                           | Same joins as default components                                                                                                                                                   |
| **Component metadata**           | Fusion PostgreSQL | `db1.peer1.com` (via SSH tunnel through `10.121.21.20`) | `public.components`                                     | `id, display_name, description, is_active, component_type_id`                        | No slot/bay/socket count field                                                                                                                                                     |
| **Component types / categories** | Fusion PostgreSQL | `db1.peer1.com` (via SSH tunnel through `10.121.21.20`) | `public.component_types`, `public.component_categories` | `name, parent_component_id, category_id, sort_order`                                 | Used for grouping in UI                                                                                                                                                            |
| **Pricebook (MRC)**              | Fusion PostgreSQL | `db1.peer1.com` (via SSH tunnel through `10.121.21.20`) | `public.pricebook`                                      | `mrc, nrc, setup, currency, datacenter, product_line_id, component_id, is_available` | Always queried in DC native currency; FX applied if display ≠ native                                                                                                               |
| **Contract terms**               | Fusion PostgreSQL | `db1.peer1.com` (via SSH tunnel through `10.121.21.20`) | `public.contract_lengths`                               | `contract_length`                                                                    | **Not currently queried** — UI uses hardcoded 12/24/36                                                                                                                             |
| **Term discounts**               | Fusion PostgreSQL | `db1.peer1.com` (via SSH tunnel through `10.121.21.20`) | `public.product_class_contract_length_discounts`        | `product_class, product_line, contract_length, *_discount`                           | **Not currently queried** — all discounts are 0% for servers                                                                                                                       |
| **HW CapEx — server level**      | MSSQL             | `DM_BusinessInsights`                                   | `profitability.ocean_sku_cost`                          | `sku_id, sku_name, sku_cost, cost_currency, sku_type, sku_level`                     | Queried with `sku_level='TLS'`; `sku_id = product_catalog.id`. Server-level entry takes priority over component sum                                                                |
| **HW CapEx — component level**   | MSSQL             | `DM_BusinessInsights`                                   | `profitability.ocean_sku_cost`                          | `sku_id, sku_name, sku_cost, cost_currency, sku_type, sku_level`                     | Queried with `sku_level='Component'`; used as fallback when server-level row is missing or $0. **Note:** the same `sku_id` can exist at both levels — always filter by `sku_level` |
| **HW cost type**                 | MSSQL             | `DM_BusinessInsights`                                   | `profitability.ocean_sku_cost`                          | `sku_type`                                                                           | `sku_type = 'HW'/'Hardware'` = one-time CapEx; anything else = recurring (software/licensing). App exposes this as `cost_kind: "hw"` vs `"sw"`                                     |
| **Power wattage**                | MSSQL             | `DM_BusinessInsights`                                   | `profitability.hardware_watts`                          | `fusion_id, watts`                                                                   | `fusion_id = product_catalog.id`; enables live power cost (`watts ÷ 1000 × $/kW`). Power shows as N/A if row is missing                                                            |
| **Overhead rates**               | Local file        | —                                                       | `cost_drivers.json`                                     | `data_centers[dc].costs[service_type][key]`                                          | Amounts in DC native currency; 7 DCs covered; SG&A = 8.2% of total MRC                                                                                                             |


---

## 2. Active / Available Filtering

### Server list (`/api/servers`)

```sql
-- All active servers that have ANY pricebook row for this DC
-- Pricing problems surface as warnings, not silent exclusions
SELECT pc.id, pc.name, ...
FROM public.product_catalog pc
LEFT JOIN LATERAL (
    SELECT id, mrc, nrc, setup, is_available FROM public.pricebook
    WHERE product_catalog_id = pc.id AND currency = [display_currency]
      AND datacenter = %s AND product_line_id = %s AND component_id IS NULL
    LIMIT 1
) pb_disp ON true
LEFT JOIN LATERAL (
    SELECT id, mrc, nrc, setup, is_available FROM public.pricebook
    WHERE product_catalog_id = pc.id AND currency = [native_currency]
      AND datacenter = %s AND product_line_id = %s AND component_id IS NULL
    LIMIT 1
) pb_nat ON true
WHERE pc.product_class = 1
  AND pc.is_active = true
  AND EXISTS (
      SELECT 1 FROM public.pricebook
      WHERE product_catalog_id = pc.id
        AND datacenter = %s AND product_line_id = %s AND component_id IS NULL
  )
ORDER BY COALESCE(pb_disp.mrc, pb_nat.mrc) ASC NULLS LAST
```

**Pricing resolution per server (in order):**
1. Pricebook row in display currency → `fx = 1.0`, no warning
2. Pricebook row in native currency only → FX conversion applied, `warnings: ["no_pricebook_in_display_currency"]`
3. No pricebook row in any currency → `mrc: null`, `warnings: ["no_pricebook_row"]`

**Additional warnings added when applicable:**
- `"mrc_is_zero"` — pricebook row exists but `mrc = 0`
- `"not_available_in_pricebook"` — pricebook row has `is_available = false`

Servers with data problems are returned in the list with warnings rather than silently hidden. Fix the data in Ocean/Fusion to resolve the warnings.

**For cost coverage auditing** — active servers with no `ocean_sku_cost` TLS row:

```sql
-- Servers visible in the New Quotes tool that have NO ocean_sku_cost TLS row
SELECT pc.id, pc.name
FROM public.product_catalog pc
WHERE pc.product_class = 1
  AND pc.is_active = true
  AND EXISTS (
      SELECT 1 FROM public.pricebook
      WHERE product_catalog_id = pc.id AND component_id IS NULL
  )
  AND pc.id NOT IN (
      SELECT sku_id FROM profitability.ocean_sku_cost WHERE sku_level = 'TLS'
  )
```

### Default components (`product_templates`)

```sql
SELECT t.component_id, t.quantity, c.display_name, ...
FROM public.product_templates t
JOIN public.components c ON c.id = t.component_id
-- NO c.is_active = true filter here
WHERE t.product_id = %s
```

**Important:** The app does NOT filter `c.is_active` for default components. An inactive component in `product_templates` will still appear in the default config. This is intentional (the template defines "what ships with the server") but means inactive components can be visible.

### Allowed components (`product_allowed_components`)

```sql
SELECT t.component_id, c.display_name, ...
FROM public.product_allowed_components t
JOIN public.components c ON c.id = t.component_id
WHERE t.product_id = %s
  AND c.is_active = true            -- only active components shown as upgrade options
```

**Allowed upgrades ARE filtered** to `c.is_active = true`. Inactive components will not appear as upgrade options.

### Summary for the cost audit


| List               | `is_active` filter    | `is_available` filter                       | Impact for cost audit                                       |
| ------------------ | --------------------- | ------------------------------------------- | ----------------------------------------------------------- |
| Servers            | `pc.is_active = true` | `pb.is_available = true` + `pb.mrc > 0`     | All listed servers must have cost rows                      |
| Default components | **None**              | `pb.is_available = true` (via LATERAL join) | Inactive defaults can appear — check if they have cost rows |
| Allowed components | `c.is_active = true`  | `pb.is_available = true` (via LATERAL join) | Only active components shown — still need cost row coverage |


---

## 3. Current State — Quoting Flow

```
User picks DC  →  picks currency  →  picks term  →  picks product line
Available servers listed (priced in display currency)
User selects server  →  sees default config + cost breakdown
User swaps/adds components  →  live margin recalculates
Copy quote summary
```

### Step 1 — Filter Setup (page load)

#### Data Centers

**Source in app:** `get_dc_registry()` — queries Fusion `sb_datacenter` + `datacenter_available_currencies` on first call, caches result in memory. Falls back to `cost_drivers.json` if Fusion is unreachable.

```sql
-- Fusion: public.sb_datacenter + datacenter_available_currencies
SELECT sd.id, sd.dc_abbr, sd.name, sd.city, sd.state,
       array_agg(dac.currency_code ORDER BY dac.currency_code)
         FILTER (WHERE dac.currency_code IS NOT NULL) AS currencies
FROM public.sb_datacenter sd
LEFT JOIN public.datacenter_available_currencies dac ON dac.datacenter_id = sd.id
WHERE sd.active = true
GROUP BY sd.id, sd.dc_abbr, sd.name, sd.city, sd.state
ORDER BY sd.dc_abbr
```

Native currency preference: `cost_drivers.json[dc_abbr].native_currency` → falls back to first currency from `datacenter_available_currencies` → falls back to `"USD"`.

**DCs with overhead rates in `cost_drivers.json` (7 total):**


| CPQ code | Fusion dc_abbr | Fusion dc_id | Name                    | Native currency |
| -------- | -------------- | ------------ | ----------------------- | --------------- |
| ATL      | ATL            | 1            | Atlanta                 | USD             |
| IAD      | IAD2           | 8            | Herndon (Washington DC) | USD             |
| LAX      | LAX1           | 7            | Los Angeles             | USD             |
| MIA      | MIA            | 2            | Miami                   | USD             |
| MTL      | MTL-BH         | 42           | Montreal                | CAD             |
| POR      | POR            | 13           | Portsmouth              | GBP             |
| TOR      | TOR            | 12           | Toronto                 | CAD             |


DCs present in Fusion `sb_datacenter` (active) but NOT in `cost_drivers.json` will appear in the DC dropdown but will return empty overhead lines (no network, dc_infra, or support costs).

#### Currency

**Source in UI:** Hardcoded dropdown in `index.html`: USD, CAD, GBP, EUR.

The API (`/api/servers`, `/api/product/<id>/config`) accepts any currency string and handles FX conversion. The UI restriction to 4 currencies is a frontend decision only.

**FX conversion logic (routes/cpq.py):**

1. Try pricebook directly in the display currency (`pb.currency = display_currency`).
2. If no rows found, query in native currency and multiply by `get_fx_rate(native, display)`.

FX rate source: `MSSQL DM_BusinessInsights.dbo.dimCurrencyExchangeRates WHERE from_currency=%s AND to_currency=%s ORDER BY start_date DESC` — always the most recent rate.

#### Term

**Source in UI:** Hardcoded dropdown in `index.html`: 12 / 24 / 36 months (36 selected by default).

The term value is passed to `/api/product/<id>/config` as a query param and echoed back in the response (`term_months`). The backend does NOT apply any pricebook discount for term — `product_class_contract_length_discounts` is all zeros for servers. Term is used only by the frontend to amortize CapEx (`total_hw_capex ÷ term_months = CapEx/mo`).

#### Product Line

**Source in UI:** Dropdown in `index.html` with two options:

- `4` — Dedicated Hosting
- `3` — Managed Hosting

Both product lines query the same Fusion tables. The `product_line_id` filter is applied to both pricebook rows and the component pricebook lateral join.

### Step 2 — Server List (`/api/servers`)

Queries `product_catalog JOIN pricebook` with the filters described in [Section 2](#2-active--available-filtering). Results are ordered by `pb.mrc ASC`. MRC is converted to display currency via FX if needed.

### Step 3 — Product Config (`/api/product/<id>/config`)

On server selection, the frontend calls `/api/product/<id>/config?dc=&currency=&product_line=&term=`.

The response contains:

- `server_mrc` — base server MRC in display currency
- `defaults` — list of default components (from `product_templates`) with MRC, HW cost, and provenance
- `allowed` — list of available upgrade components (from `product_allowed_components`) with MRC, HW cost, and provenance
- `total_mrc` — server MRC + sum of default component MRCs > 0
- `total_hw_capex` — one-time hardware cost in display currency (server-level from `ocean_sku_cost`)
- `overhead` — per-line overhead costs from `cost_drivers.json`, converted to display currency
- `server_watts` / `server_kw` — from `profitability.hardware_watts`; `null` if no row exists

### Step 4 — Component Swap / Add (frontend only)

The UI reads `allowed` components and renders swap dropdowns per component type. Margin recalculation is entirely client-side using the `addon_mrc`, `hw_cost_display`, and `cost_kind` values already returned in the config response. No additional API call is made on swap.

---

## 4. Cost Calculation Formula

All amounts are in display currency.

```
Total Customer MRC  = server_mrc + Σ (default_component_mrc × quantity, where mrc > 0)

HW CapEx (total)    = ocean_sku_cost[sku_level='TLS', sku_id=product_id].sku_cost × fx_rate
                      (fallback: Σ ocean_sku_cost[sku_level='Component', sku_id=component_id].sku_cost × quantity)

HW CapEx / mo       = HW CapEx ÷ term_months   (frontend calculation)

Power cost / mo     = hardware_watts[fusion_id=product_id].watts ÷ 1000 × $/kW × fx_overhead
                      (N/A if hardware_watts row missing)

Overhead / mo       = Σ cost_drivers[dc].costs.server[key] × fx_overhead
                      + (Total MRC × 0.082)   ← SG&A

Total Internal Cost / mo  = HW CapEx/mo + Power/mo + Overhead/mo   (frontend calculation)

Gross Margin / mo         = Total Customer MRC − Total Internal Cost/mo
Gross Margin %            = Gross Margin ÷ Total Customer MRC × 100
```

**FX note:** `cost_drivers.json` amounts are stored in the DC's native currency. The app applies `fx_overhead = get_fx_rate(native_currency, display_currency)` to convert them. Server-level `ocean_sku_cost.sku_cost` has its own `cost_currency` column (typically USD) and is converted independently via `fx_cost_map`.

---

## 5. Known Gaps


| #   | Gap                                  | Current behavior                                                                                                                                                       | Correct behavior                                                                                                                                                      |
| --- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Multi-currency DC native currency    | For DCs with multiple currencies in `datacenter_available_currencies` (e.g., TOR: CAD + USD), native is resolved via `cost_drivers.json` override, then first DB entry | Confirm whether `datacenter_available_currencies` has an `is_default` or ordering column that could replace the `cost_drivers.json` dependency for multi-currency DCs |
| 2   | Currency dropdown source             | Hardcoded USD/CAD/GBP/EUR in `index.html`                                                                                                                              | Should be driven by `datacenter_available_currencies` for the selected DC                                                                                             |
| 3   | Term dropdown source                 | Hardcoded 12/24/36 in `index.html`                                                                                                                                     | Should come from `contract_lengths` (values: 1, 3, 6, 12, 24, 36) — though all discounts are 0% for servers today                                                     |
| 4   | Default component `is_active` filter | Missing — inactive components in `product_templates` still appear                                                                                                      | Decide: filter them out, or intentionally show (template = "what shipped") and flag visually                                                                          |
| 5   | `cost_drivers.json` DC coverage      | 7 DCs have overhead rates                                                                                                                                              | All active DCs with pricebook rows need overhead data; DCs outside the 7 return $0 overhead                                                                           |
| 6   | Power cost coverage                  | Depends on `profitability.hardware_watts` having a row per server                                                                                                      | Incomplete — many servers may show power as N/A; `hardware_watts` needs to be populated for all active servers                                                        |
| 7   | Physical slot/bay/socket counts      | Not in any DB                                                                                                                                                          | Dell R-660: 2 CPU sockets, 32 DIMM slots, 10× 2.5" bays — not modelled in Fusion; would need a spec table or external lookup to surface in the tool                   |
| 8   | `ocean_sku_cost` component coverage  | Some components show `hw_cost_display: null`                                                                                                                           | All components returned by `product_allowed_components` (active, with pricebook rows) need a `Component`-level row in `ocean_sku_cost` to show accurate margin        |
| 9   | SKU restrictions not enforced        | Users can add any combination of components                                                                                                                            | Ocean enforces per-category min/max limits and dependency rules (see [Section 6](#6-future-work--to-do))                                                              |
| 10  | Multiple base configs not supported  | One default config per product                                                                                                                                         | Ocean supports multiple named base configs per SKU; the tool always loads the single `product_templates` set                                                           |


---

## 6. Future Work / To-Do

### 6a. Ocean SKU Restrictions (priority: high)

Ocean's product Framework tab configures per-SKU component rules that the tool does not yet enforce:

- **Category limits:** A SKU can define min/max number of components from a given category (e.g., "must have 1–50 Azure Subscriptions", "at most 1 discount"). These are stored in Ocean but not exposed in any Fusion table the tool currently reads.
- **Dependency rules:** Some components cannot be added without another (e.g., "cannot add minimum commits without an Azure Subscription"). Ocean shows a warning and can block the order.
- **Warning vs. hard block:** Ocean presents a warning first; users can proceed past the warning but it is logged.

**What needs to happen:**

1. Identify which Ocean tables store these rules (product Framework tab data — likely not in `public.product_allowed_components`; may be a separate Ocean schema).
2. Surface min/max limits in the UI — show count badges per category, highlight violations.
3. Decide whether to hard-block (prevent quote completion) or warn-only (match Ocean behavior).

### 6b. Multiple Base Configs

Ocean allows multiple named default component presets per SKU, so Sales can choose between configurations (e.g., "Standard" vs "High Memory" starting point).

**What needs to happen:**

1. Check whether `product_templates` has a config-name/group field, or whether these alternatives are in a separate table.
2. Add a config-preset selector to the product page (before the component breakdown loads).

### 6c. DC List / Currency / Term — Drive from Fusion

- DC list: already driven from Fusion (done). Ensure all newly activated DCs in Fusion get overhead rates added to `cost_drivers.json`.
- Currency dropdown: replace hardcoded list with currencies from `datacenter_available_currencies` for the selected DC, plus all FX-convertible currencies if desired.
- Term dropdown: replace hardcoded 12/24/36 with a query to `contract_lengths` (filtered by `product_class=1, product_line=4`).

### 6d. Power Cost Coverage

`profitability.hardware_watts` needs a row for every active server (`fusion_id = product_catalog.id`). Without it, power cost is N/A and internal cost is understated. This table needs to be populated and kept current when new server SKUs are added.

### 6e. `cost_drivers.json` Expansion

DCs active in Fusion but missing from `cost_drivers.json` (LDN1, SAT5, CRO, GOS, and others) show $0 overhead. The finance overhead rates for these DCs need to be added to `cost_drivers.json` — or the overhead data needs to move to a proper DB table.

---

## 7. Product Catalog Changes — -D and -vHost Deprecation

> **Approved by:** Adam Nelson
> **Status:** In progress (disable in Ocean; tool reflects Ocean data automatically via `pc.is_active` filter)

### Products being disabled

The following server products are to be disabled (`pc.is_active = false` or `pb.is_available = false`):


| Product Name                       | Notes         |
| ---------------------------------- | ------------- |
| Advanced Series 5.0 - D            | -D variant    |
| Advanced Series 5.0 vHost          | vHost variant |
| Advanced Series 6.0 vHost          | vHost variant |
| Essential Series 5.0 - D           | -D variant    |
| Fusion Series 5.0 UK vHost         | vHost variant |
| Fusion Series 5.0 vHost            | vHost variant |
| Pro Dell PE 650xs vHost - Non NVMe | vHost variant |
| Pro Series 5.0 - D                 | -D variant    |
| Pro Series 5.0 vHost               | vHost variant |
| Pro Series 6.0 vHost               | vHost variant |
| Storage Series 5.0 - D             | -D variant    |


> Note: "Advanced Series 5.0" (base, no suffix) is also listed for disablement in the original request — confirm with Adam Nelson whether the base non-suffixed product should be disabled or retained.

Once these are set inactive in Ocean/Fusion, the server list will automatically exclude them via `pc.is_active = true AND pb.is_available = true`.

### Add-ons enabled on all default servers

The following components are to be enabled on all default server products (all DCs, all lines of business):

**Hypervisor OS:**

- VMware ESXi 8.0
- Proxmox VE
- Proxmox VE 8.x
- Proxmox VE 9.x

**VMware Licensing:**

- VMware Licensing - 16 Cores per Proc - 1 Year Commit
- VMware Licensing - 2 Additional Cores - 1 Year Commit
- VMware Licensing - 16 Cores per Proc - 2 Year Commit
- VMware Licensing - 2 Additional Cores - 2 Year Commit
- VMware Licensing - 16 Cores per Proc - 3 Year Commit
- VMware Licensing - 2 Additional Cores - 3 Year Commit

These will appear in `product_allowed_components` once enabled in Ocean. No code changes required — the allowed component query will pick them up automatically.

### Dedicated and Managed Hosting convergence

The goal is to standardize on a single default server product across both Dedicated Hosting (`product_line_id = 4`) and Managed Hosting (`product_line_id = 3`). The -D and -vHost variants were the mechanism for separating these; removing them means the same base product should appear under both product lines.

**Tool impact:**

- The product line dropdown (Dedicated / Managed) already exists in the UI.
- Pricebook rows must exist for both `product_line_id = 3` and `product_line_id = 4` for a server to appear under each line.
- `product_allowed_components` is not filtered by product line — if the component is in the table, it appears under both.
- Action: verify in Ocean that default server products have active pricebook rows for both product lines after the -D/-vHost products are disabled.

---

## 8. Production Readiness Assessment

### What works accurately today

- **Pricing:** Server MRC and component add-on pricing are read live from `Fusion.public.pricebook`. FX conversion uses the latest rate from `DM_BusinessInsights`. Pricing is accurate as long as Fusion pricebook rows are current.
- **Default configs:** `product_templates` reflects the actual default component set in Fusion.
- **Available upgrades:** `product_allowed_components` with `c.is_active = true` reflects what Ocean allows. Correct once Ocean is kept current.
- **Active product filtering:** Only `pc.is_active = true` and `pb.is_available = true` products appear. Disabling products in Ocean removes them automatically.
- **Margin calculation:** Structurally correct — MRC, CapEx amortization, overhead, SG&A, FX all wired up. Accuracy depends on the cost data below.

### Where cost accuracy depends on data completeness


| Cost line           | Coverage today                                                   | What's needed to be production-accurate                                                                          |
| ------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Server HW CapEx     | Only servers with a `TLS`-level row in `ocean_sku_cost`          | Every active server needs a `TLS` row; verify with the audit query in Section 2                                  |
| Component HW cost   | Only components with a `Component`-level row in `ocean_sku_cost` | Every component in `product_allowed_components` ideally needs a row; missing = zero cost shown = inflated margin |
| Power cost          | Only servers with a row in `profitability.hardware_watts`        | Incomplete; many servers show N/A for power — understates internal cost                                          |
| Overhead (non-SG&A) | Only 7 DCs in `cost_drivers.json`                                | Other DCs show $0 overhead — not safe for margin decisions                                                       |


### Recommendation

**The New Quotes tool can replace Excel-CPQ for quoting (price to customer) today** — pricing is live from Fusion and accurate.

**It should not yet be used as the authoritative margin/profitability tool** until:

1. `ocean_sku_cost` coverage is audited and gaps filled for all active servers and key components.
2. `hardware_watts` is populated for all active servers.
3. `cost_drivers.json` overhead rates are added for DCs beyond the current 7.

**To keep data aligned going forward (replacing the Excel-CPQ process):**

- Pricebook changes in Ocean flow through automatically.
- When new server SKUs are added to Ocean: add `ocean_sku_cost` TLS row + `hardware_watts` row + verify `cost_drivers.json` has the DC.
- When components are added/removed in Ocean: `product_allowed_components` and `product_templates` update automatically; add `ocean_sku_cost` Component row for new components.
- When DCs are added: add entry to `cost_drivers.json` with overhead rates.
