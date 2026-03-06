---
type: schema
object: Churn
updated: 2026-03-06
---

# Churn

**Source:** DM_BusinessInsights / dbo
**Description:** Churned services with cancel_date, product, cad_mrc, line_of_business.

## Columns

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| integer_key | int(10) | NO |  |
| churn_class | nvarchar(255) | YES |  |
| cancel_date | datetime2 | YES |  |
| client_type | nvarchar(255) | YES |  |
| client_id_company | nvarchar(255) | YES |  |
| service_id | nvarchar(255) | YES |  |
| nickname | nvarchar(255) | YES |  |
| product | nvarchar(255) | YES |  |
| os | nvarchar(255) | YES |  |
| cancel_reason | nvarchar(255) | YES |  |
| start_date | datetime2 | YES |  |
| accounts_left | int(10) | YES |  |
| line_of_business | nvarchar(255) | YES |  |
| months_online | int(10) | YES |  |
| datacenter_code | nvarchar(15) | YES |  |
| is_emea | nvarchar(3) | YES |  |
| migration_start | datetime2 | YES |  |
| tam | nvarchar(255) | YES |  |
| last_45_days | nvarchar(255) | YES |  |
| is_migration | nvarchar(255) | YES |  |
| bdc | nvarchar(255) | YES |  |
| currency | nvarchar(255) | YES |  |
| original_currency_mrc | numeric(38,2) | YES |  |
| contract_term | nvarchar(255) | YES |  |
| service_type | nvarchar(255) | YES |  |
| shopping_cart | nvarchar(255) | YES |  |
| promotion | nvarchar(255) | YES |  |
| comments | nvarchar(MAX) | YES |  |
| usd_mrc | numeric(38,2) | YES |  |
| client_id | int(10) | YES |  |
| short_term | int(10) | YES |  |
| cad_mrc | numeric(38,2) | YES |  |
| cad_budget_mrc | numeric(38,4) | YES |  |
| adjusted_line_of_business | nvarchar(255) | YES |  |
| date_captured | datetime2 | YES |  |

## Sample Data

| integer_key | churn_class | cancel_date | client_type | client_id_company | service_id | nickname | product | os | cancel_reason | start_date | accounts_left | line_of_business | months_online | datacenter_code | is_emea | migration_start | tam | last_45_days | is_migration | bdc | currency | original_currency_mrc | contract_term | service_type | shopping_cart | promotion | comments | usd_mrc | client_id | short_term | cad_mrc | cad_budget_mrc | adjusted_line_of_business | date_captured |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 140169 | Non-Pay | 2022-03-23 09:50:07.262107 | Retail | 4028779 RxHealthcareMagic | 3339003 | energy.healthcaremagic.com | Pro Dell PE R-410 | Ubuntu 12.04 64 bit | Non-Payment | 2013-05-24 14:20:46.903714 | 0 | Dedicated Hosting | 107 | IAD2 | No |  |  |  | No | gcouture | USD | 423.59 | 12 | server | No | ONE Month FREE |  | 423.59 | 4028779 |  | 549.76 | 563.3747 | Hosting | 2022-03-31 08:46:00.683333 |
| 140171 | Other | 2022-03-18 10:05:02.523609 | Retail | 7014572 Centro Internacional de Mejoramiento de Maíz y Trigo | 5363599 | Dev.Adapt Beta.CIMMYT | Guest Virtual | CentOS 7.x 64 MH Virtual Server | OTHER (See Comments) | 2018-05-08 06:10:50.698567 | 35 | Managed Hosting | 47 | POR | No |  |  |  | No | dalfaro | USD | 42.50 | 36 | Virtual | No | TWO Months FREE | Cherwell ticket 1226643
 Offline date March 15, 2022 | 42.50 | 7014572 |  | 55.16 | 56.5250 | Hosting | 2022-03-31 08:46:00.683333 |
| 140172 | Other | 2022-03-26 19:55:12.883268 | Retail | 7012772 ResearchGATE GmbH | 4093087 | prd-solr-11-tor.rgcloud.net | Pro E5v3 - M | Customer Supplied OS | Not leaving, just moving to another Product | 2015-04-10 11:09:55.697555 | 403 | Managed Hosting | 84 | TOR | Yes |  | mjulier |  | No | swilliams | USD | 976.01 | 12 | server | No | TWO Months FREE |  | 976.01 | 7012772 |  | 1266.71 | 1298.0933 | Hosting | 2022-03-31 08:46:00.683333 |
| 140173 | Other | 2022-03-26 19:55:13.479765 | Retail | 7012772 ResearchGATE GmbH | 4093088 | prd-solr-10-tor.rgcloud.net | Pro E5v3 - M | Customer Supplied OS | Not leaving, just moving to another Product | 2015-04-10 11:09:49.993146 | 403 | Managed Hosting | 84 | TOR | Yes |  | mjulier |  | No | swilliams | USD | 976.01 | 12 | server | No | TWO Months FREE |  | 976.01 | 7012772 |  | 1266.71 | 1298.0933 | Hosting | 2022-03-31 08:46:00.683333 |
| 140174 | Other | 2022-03-26 19:55:14.173360 | Retail | 7012772 ResearchGATE GmbH | 4093089 | prd-solr-09-tor.rgcloud.net | Pro E5v3 - M | Customer Supplied OS | Not leaving, just moving to another Product | 2015-04-10 11:09:43.001855 | 403 | Managed Hosting | 84 | TOR | Yes |  | mjulier |  | No | swilliams | USD | 942.91 | 12 | server | No | TWO Months FREE |  | 942.91 | 7012772 |  | 1223.75 | 1254.0703 | Hosting | 2022-03-31 08:46:00.683333 |

## Usage Notes

- **Standalone table** — service_id is nvarchar here, do NOT join to dimServices.service_id (int type mismatch)
- Filter by `client_id` (int)
- `cancel_date` is the churn event date
- `cancel_reason` describes why the service was cancelled
- `churn_class` categorises the type of churn (Non-Pay, Other, etc.)
- `cad_mrc` is the CAD value of the cancelled service — use for churn revenue impact
- `accounts_left` = number of services the client still had at time of churn event
- `months_online` = tenure of the cancelled service in months
- `is_migration = 'Yes'` means the cancellation was part of a migration, not true churn
