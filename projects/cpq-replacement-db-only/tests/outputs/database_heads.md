---
type: schema
source: Supabase (public schema)
generated: 2026-03-08
---

# CPQ Replacement DB — Table & View Heads

Column names, datatypes, and **pandas-style head**: first few rows of real data. When a table or view is empty, **No data.** is shown explicitly.

---

## Tables

### currencies

**Description:** ISO 4217 currencies in use. CAD is root (is_base=true); never appears as a target in fx_rates.

| Column | Type | Nullable |
|--------|------|----------|
| currency_code | character(3) | NO |
| currency_name | text | NO |
| symbol | text | NO |
| is_base | boolean | NO |

#### Head (first 4 rows)

| currency_code | currency_name | symbol | is_base |
|---------------|----------------|--------|---------|
| CAD | Canadian Dollar | $ | true |
| USD | US Dollar | $ | false |
| GBP | British Pound | £ | false |
| EUR | Euro | € | false |

---

### data_centers

**Description:** 6 active data centers for server hosting. Colo available at MIA and POR only.

| Column | Type | Nullable |
|--------|------|----------|
| dc_code | character(3) | NO |
| dc_name | text | NO |
| city | text | NO |
| country | text | NO |
| native_currency | character(3) | NO |
| is_active | boolean | NO |
| notes | text | YES |

#### Head (first 5 rows)

| dc_code | dc_name | city | country | native_currency | is_active | notes |
|---------|---------|------|---------|------------------|-----------|-------|
| ATL | Atlanta | Atlanta | US | USD | true | — |
| MIA | Miami | Miami | US | USD | true | — |
| LAX | Los Angeles | Los Angeles | US | USD | true | — |
| IAD | Washington DC | Ashburn | US | USD | true | — |
| TOR | Toronto | Toronto | CA | CAD | true | — |

---

### dc_cost_drivers

**Description:** Internal per-DC cost overheads (power, rack, connectivity, etc.). 48 rows from CPQ v28. NOT billed to customers.

| Column | Type | Nullable |
|--------|------|----------|
| id | bigint | NO |
| dc_code | character(3) | NO |
| cost_category | text | NO |
| amount | numeric | NO |
| currency_code | character(3) | NO |
| notes | text | YES |

#### Head (first 5 rows)

| id | dc_code | cost_category | amount | currency_code | notes |
|----|---------|----------------|--------|---------------|-------|
| 1 | ATL | power_per_kw | 63.6233 | USD | measure=$ / kW; source=Model-Drivers CPQ v28 |
| 2 | MIA | power_per_kw | 99.1613 | USD | measure=$ / kW; source=Model-Drivers CPQ v28 |
| 3 | LAX | power_per_kw | 80.3576 | USD | measure=$ / kW; source=Model-Drivers CPQ v28 |
| 4 | IAD | power_per_kw | 72.7266 | USD | measure=$ / kW; source=Model-Drivers CPQ v28 |
| 5 | TOR | power_per_kw | 218.2749 | CAD | measure=$ / kW; source=Model-Drivers CPQ v28 |

---

### fx_rates

**Description:** Finance-maintained FX rates. Append-only — never update rows, always insert new. Rate = units of CAD per 1 foreign currency (as displayed on bankofcanada.ca).

| Column | Type | Nullable |
|--------|------|----------|
| id | bigint | NO |
| currency_code | character(3) | NO |
| rate_type | text | NO |
| rate_date | date | NO |
| rate | numeric | NO |
| cad_pricing_rebased | boolean | NO |
| confirmed_override | boolean | NO |
| notes | text | YES |
| created_at | timestamp with time zone | NO |

#### Head (first 5 rows, total 330)

| id | currency_code | rate_type | rate_date | rate | cad_pricing_rebased | confirmed_override | notes |
|----|---------------|-----------|-----------|------|---------------------|--------------------|-------|
| 330 | EUR | spot | 2026-02-01 | 1.613800 | false | false | Bank of Canada monthly average; 1 EUR = 1.6138 CAD |
| 329 | GBP | spot | 2026-02-01 | 1.853300 | false | false | Bank of Canada monthly average; 1 GBP = 1.8533 CAD |
| 328 | USD | spot | 2026-02-01 | 1.365100 | false | false | Bank of Canada monthly average; 1 USD = 1.3651 CAD |
| 325 | USD | spot | 2026-01-01 | 1.377800 | false | false | Bank of Canada monthly average; 1 USD = 1.3778 CAD |
| 327 | EUR | spot | 2026-01-01 | 1.617200 | false | false | Bank of Canada monthly average; 1 EUR = 1.6172 CAD |

---

### overhead_constants

**Description:** Global financial model constants. Finance-owned. ~12 rows.

| Column | Type | Nullable |
|--------|------|----------|
| key | text | NO |
| value | numeric | NO |
| description | text | YES |
| updated_at | timestamp with time zone | NO |

#### Head (first 5 rows, total 8)

| key | value | description |
|-----|-------|-------------|
| sga_pct | 0.082 | SG&A as % of revenue — CPQ v28 Model-Drivers row 10 |
| annual_cost_inflation | 0.03 | Annual cost inflation rate — CPQ v28 Model-Drivers |
| software_markup_pct | 0.15 | Markup over wholesale software cost — CPQ v28 Model-Hosting C72 |
| ebit_poor_threshold | -0.1 | EBIT % below which deal is Poor — CPQ v28 |
| ebit_moderate_target | 0.35 | EBIT % for Moderate rating — CPQ v28 |

---

### pending_fusion_id

**Description:** Tracks product_catalog rows with TEMP- placeholder fusion_ids. Every placeholder must be resolved (real fusion_id assigned and this row deleted) before production go-live.

| Column | Type | Nullable |
|--------|------|----------|
| id | bigint | NO |
| product_id | bigint | NO |
| placeholder_id | text | NO |
| sku_name | text | NO |
| reason | text | YES |
| created_at | timestamp with time zone | NO |
| resolved_at | timestamp with time zone | YES |
| resolved_fusion_id | text | YES |

#### Head (first 2 rows, total 2)

| id | product_id | placeholder_id | sku_name | reason | created_at | resolved_at | resolved_fusion_id |
|----|------------|----------------|----------|--------|------------|-------------|--------------------|
| 1 | 1 | TEMP-promo-server-na | Promo Server - NA | Product not yet formally released; fusion_id pending assignment | 2026-03-08 15:28:51+00 | — | — |
| 2 | 2 | TEMP-promo-server-uk | Promo Server - UK | Product not yet formally released; fusion_id pending assignment | 2026-03-08 15:28:51+00 | — | — |

---

### product_capex

**Description:** Hardware procurement cost tracking. One row per procurement batch. CAD equivalent derived at query time via LATERAL join to fx_rates (budget rate).

| Column | Type | Nullable |
|--------|------|----------|
| id | bigint | NO |
| product_id | bigint | NO |
| procured_price | numeric | NO |
| procured_currency | character(3) | NO |
| procured_date | date | NO |
| use_as_baseline | boolean | NO |
| residual_pct_12m | numeric | YES |
| residual_pct_24m | numeric | YES |
| notes | text | YES |
| created_at | timestamp with time zone | NO |

**No data.** (0 rows)

---

### product_catalog

**Description:** Master product list. fusion_id is the join key to Salesforce, billing, and all internal systems. BIGSERIAL id is the internal FK used by all other tables.

| Column | Type | Nullable |
|--------|------|----------|
| id | bigint | NO |
| fusion_id | text | YES |
| sku_name | text | NO |
| sku_nickname | text | YES |
| product_type_code | text | NO |
| level | text | NO |
| release_date | date | YES |
| end_of_sale_date | date | YES |
| end_of_support_date | date | YES |
| end_of_service_life_date | date | YES |
| vendor | text | YES |
| is_active | boolean | NO |
| notes | text | YES |
| search_keywords | text | YES |
| created_at | timestamp with time zone | NO |
| updated_at | timestamp with time zone | NO |

#### Head (first 5 rows, total 18)

| id | fusion_id | sku_name | product_type_code | level | is_active |
|----|-----------|----------|-------------------|-------|-----------|
| 1 | TEMP-promo-server-na | Promo Server - NA | server | TLS | true |
| 2 | TEMP-promo-server-uk | Promo Server - UK | server | TLS | true |
| 3 | 1290 | Pro Series 7.0 | server | TLS | true |
| 4 | 1288 | Cluster 5.0 (Dell R440) | server | TLS | true |
| 5 | 1289 | Atomic 5.0 (Dell R650xs) | server | TLS | true |

---

### product_pricing

**Description:** Customer-facing pricing. One row per product × currency × contract term. ~1,200 rows for server POC.

| Column | Type | Nullable |
|--------|------|----------|
| id | bigint | NO |
| product_id | bigint | NO |
| currency_code | character(3) | NO |
| term_months | smallint | NO |
| mrc | numeric | YES |
| nrc | numeric | YES |
| pricing_model | text | NO |
| effective_from | date | YES |
| notes | text | YES |

#### Head (first 5 rows, total 204)

| id | product_id | currency_code | term_months | mrc | nrc | pricing_model | effective_from | notes |
|----|------------|---------------|-------------|-----|-----|---------------|----------------|-------|
| 1 | 1 | USD | 0 | — | 0.00 | flat | — | — |
| 2 | 1 | USD | 12 | 399.00 | 0.00 | flat | — | — |
| 3 | 1 | USD | 24 | 349.00 | 0.00 | flat | — | — |
| 4 | 1 | USD | 36 | 299.00 | 0.00 | flat | — | — |
| 5 | 1 | CAD | 0 | — | 0.00 | flat | — | — |

---

### product_types

**Description:** Self-referencing product type hierarchy. Example: nvme → drive → storage_component.

| Column | Type | Nullable |
|--------|------|----------|
| type_code | text | NO |
| type_label | text | NO |
| parent_code | text | YES |
| level | text | NO |

#### Head (first 10 rows, total 31)

| type_code | type_label | parent_code | level |
|-----------|------------|-------------|-------|
| server | Server | — | TLS |
| colocation | Colocation | — | TLS |
| firewall | Firewall | — | TLS |
| switch | Network Switch | — | TLS |
| hardware_component | Hardware Component | — | Component |
| software | Software | — | Component |
| network_component | Network Component | — | Component |
| cpu | CPU / Processor | hardware_component | Component |
| ram | RAM | hardware_component | Component |
| storage_component | Storage | hardware_component | Component |

---

### server_dc_availability

**Description:** Which servers are available at which data centers. 88 rows from CPQ v28.

| Column | Type | Nullable |
|--------|------|----------|
| server_product_id | bigint | NO |
| dc_code | character(3) | NO |

#### Head (first 5 rows, total 88)

| server_product_id | dc_code |
|-------------------|---------|
| 3 | ATL |
| 3 | MIA |
| 3 | LAX |
| 3 | IAD |
| 3 | TOR |

---

### server_specs

**Description:** 1:1 with product_catalog for TLS server products.

| Column | Type | Nullable |
|--------|------|----------|
| product_id | bigint | NO |
| processor_sockets | smallint | YES |
| drive_bays | smallint | YES |
| default_cpu_qty | smallint | YES |
| default_drive_qty | smallint | YES |
| is_vhost | boolean | NO |
| is_promo | boolean | NO |
| min_contract_months | smallint | YES |
| allow_customization | boolean | NO |
| notes | text | YES |

#### Head (first 5 rows, total 18)

| product_id | processor_sockets | drive_bays | default_cpu_qty | default_drive_qty | is_vhost | is_promo | min_contract_months | allow_customization | notes |
|------------|-------------------|------------|-----------------|-------------------|----------|----------|---------------------|---------------------|-------|
| 1 | — | 16 | 2 | — | false | true | 12 | false | — |
| 2 | — | 8 | 2 | — | false | true | 12 | false | — |
| 3 | — | 10 | 2 | — | false | false | — | true | — |
| 4 | — | 4 | 2 | — | true | false | — | true | — |
| 5 | — | 8 | 1 | — | true | false | — | true | — |

---

### component_specs

**Description:** 1:1 with product_catalog for Component products (CPU, RAM, Drive, PSU, NIC). Sparse columns — only relevant fields populated per component type.

| Column | Type | Nullable |
|--------|------|----------|
| product_id | bigint | NO |
| cores | smallint | YES |
| threads | smallint | YES |
| clock_ghz | numeric | YES |
| ram_gb | smallint | YES |
| drive_capacity_tb | numeric | YES |
| drive_type | text | YES |
| watts | smallint | YES |
| form_factor | text | YES |

**No data.** (0 rows)

---

### server_default_components

**Description:** Components included by default in each server SKU. 126 rows from CPQ v28.

| Column | Type | Nullable |
|--------|------|----------|
| id | bigint | NO |
| server_product_id | bigint | NO |
| component_product_id | bigint | NO |
| component_type | text | NO |
| quantity | smallint | NO |

**No data.** (0 rows)

---

### server_selectable_options

**Description:** All components that can be selected or upgraded on each server. 655 rows from CPQ v28. This table is the source of truth for component compatibility.

| Column | Type | Nullable |
|--------|------|----------|
| id | bigint | NO |
| server_product_id | bigint | NO |
| component_product_id | bigint | NO |
| category | text | NO |
| is_included_default | boolean | NO |
| display_order | smallint | YES |

**No data.** (0 rows)

---

## Views

### v_pending_fusion_ids

| Column | Type | Nullable |
|--------|------|----------|
| id | bigint | YES |
| placeholder_id | text | YES |
| sku_name | text | YES |
| reason | text | YES |
| created_at | timestamp with time zone | YES |
| is_active | boolean | YES |

#### Head (first 2 rows, total 2)

| id | placeholder_id | sku_name | reason | created_at | is_active |
|----|----------------|----------|--------|------------|-----------|
| 1 | TEMP-promo-server-na | Promo Server - NA | Product not yet formally released; fusion_id pending assignment | 2026-03-08 15:28:51+00 | true |
| 2 | TEMP-promo-server-uk | Promo Server - UK | Product not yet formally released; fusion_id pending assignment | 2026-03-08 15:28:51+00 | true |

---

### v_product_capex_cad

CAD equivalent of each CapEx row, derived at query time from the most recent budget FX rate on or before the procurement date.

| Column | Type | Nullable |
|--------|------|----------|
| id | bigint | YES |
| product_id | bigint | YES |
| procured_price | numeric | YES |
| procured_currency | character(3) | YES |
| procured_date | date | YES |
| use_as_baseline | boolean | YES |
| residual_pct_12m | numeric | YES |
| residual_pct_24m | numeric | YES |
| procured_price_cad | numeric | YES |
| fx_budget_rate_used | numeric | YES |
| fx_rate_date | date | YES |

**No data.** (0 rows)
