---
type: schema-reference
generated: 2026-04-14 07:45
source: live audit via APTUM_USER
---

# MSSQL Services — Schema Reference

**Server:** `10.121.21.211`  
**Database:** `DM_businessinsights`  
**Note:** 'Ocean' is the web portal application name — the database is `DM_BusinessInsights`.  
**Total tables/views discovered:** 58  
**Accessible:** 58  
**Denied:** 0  

---

## Contents

- [Priority Tables (AccountIntel)](#priority-tables-accountintel)
- [All Accessible Tables](#all-accessible-tables)
- [Inaccessible Tables](#inaccessible-tables)
- [Cross-Database Access (FinancialReporting)](#cross-database-access)

---

## Priority Tables (AccountIntel)

### `[dbo].[Churn]`

**Status:** ✅ accessible  
**Rows:** 7,695  
**Size:** 6.0 MB  

| Column | Type | Nullable | PK |
|--------|------|----------|-----|
| `integer_key` | `int` | NO | ✓ |
| `churn_class` | `nvarchar(255)` | YES |  |
| `cancel_date` | `datetime2` | YES |  |
| `client_type` | `nvarchar(255)` | YES |  |
| `client_id_company` | `nvarchar(255)` | YES |  |
| `service_id` | `nvarchar(255)` | YES |  |
| `nickname` | `nvarchar(255)` | YES |  |
| `product` | `nvarchar(255)` | YES |  |
| `os` | `nvarchar(255)` | YES |  |
| `cancel_reason` | `nvarchar(255)` | YES |  |
| `start_date` | `datetime2` | YES |  |
| `accounts_left` | `int` | YES |  |
| `line_of_business` | `nvarchar(255)` | YES |  |
| `months_online` | `int` | YES |  |
| `datacenter_code` | `nvarchar(15)` | YES |  |
| `is_emea` | `nvarchar(3)` | YES |  |
| `migration_start` | `datetime2` | YES |  |
| `tam` | `nvarchar(255)` | YES |  |
| `last_45_days` | `nvarchar(255)` | YES |  |
| `is_migration` | `nvarchar(255)` | YES |  |
| `bdc` | `nvarchar(255)` | YES |  |
| `currency` | `nvarchar(255)` | YES |  |
| `original_currency_mrc` | `numeric(38,2)` | YES |  |
| `contract_term` | `nvarchar(255)` | YES |  |
| `service_type` | `nvarchar(255)` | YES |  |
| `shopping_cart` | `nvarchar(255)` | YES |  |
| `promotion` | `nvarchar(255)` | YES |  |
| `comments` | `nvarchar(MAX)` | YES |  |
| `usd_mrc` | `numeric(38,2)` | YES |  |
| `client_id` | `int` | YES |  |
| `short_term` | `int` | YES |  |
| `cad_mrc` | `numeric(38,2)` | YES |  |
| `cad_budget_mrc` | `numeric(38,4)` | YES |  |
| `adjusted_line_of_business` | `nvarchar(255)` | YES |  |
| `date_captured` | `datetime2` | YES |  |

**Sample rows (3):**

| integer_key | churn_class | cancel_date | client_type | client_id_company | service_id | nickname | product | os | cancel_reason | start_date | accounts_left | line_of_business | months_online | datacenter_code | is_emea | migration_start | tam | last_45_days | is_migration | bdc | currency | original_currency_mrc | contract_term | service_type | shopping_cart | promotion | comments | usd_mrc | client_id | short_term | cad_mrc | cad_budget_mrc | adjusted_line_of_business | date_captured |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 140304 | Other | 2022-04-09 19:55:03.408665 | Retail | 7011301 Hoolai Games | 3565820 | Hoolai-US24 | Essential SATA 2.0. | CentOS 6.x 64 | We are taking it in-house | 2014-03-01 10:16:47.548046 | 42 | Dedicated Hosting | 98 | IAD2 | No | NULL | NULL | NULL | No | SNadarajah | USD | 349.50 | 12 | server | No | ONE Month FREE | Cherwell ticket 1225860
Offline date April 09, 2022 | 349.50 | 7011301 | NULL | 452.45 | 464.8350 | Hosting | 2022-04-30 08:46:01.140000 |
| 140305 | Other | 2022-04-09 19:55:03.756043 | Retail | 7011301 Hoolai Games | 3565834 | Hoolai-US27 | Essential SATA 2.0. | CentOS 6.x 64 | We are taking it in-house | 2014-03-02 21:07:53.632448 | 42 | Dedicated Hosting | 98 | IAD2 | No | NULL | NULL | NULL | No | SNadarajah | USD | 349.50 | 12 | server | No | ONE Month FREE | Cherwell ticket 1225860
Offline date April 09, 2022 | 349.50 | 7011301 | NULL | 452.45 | 464.8350 | Hosting | 2022-04-30 08:46:01.140000 |
| 140306 | Other | 2022-04-01 19:55:05.320244 | Retail | 5620352 Barker Specialty Company | 4903370 | barkerspecialty.com | Pro E5v3 - M | Windows Server 2012 R2 Standard Edition x64 (Dual Proc) | We are taking it in-house | 2016-09-07 07:55:38.807605 | 3 | Managed Hosting | 67 | MIA | No | NULL | NULL | NULL | No | llongoria | USD | 1585.99 | 36 | server | No | ONE Month FREE | Cherwell ticket 1224789
Offline date April 04, 2022 | 1585.99 | 5620352 | NULL | 2053.18 | 2109.3667 | Hosting | 2022-04-30 08:46:01.140000 |

---

### `[dbo].[MRCTrend]`

**Status:** ✅ accessible  
**Rows:** 323,611  
**Size:** 134.2 MB  

| Column | Type | Nullable | PK |
|--------|------|----------|-----|
| `integer_key` | `int` | NO | ✓ |
| `client_id` | `int` | YES |  |
| `company_name` | `nvarchar(255)` | YES |  |
| `client_created` | `datetime2` | YES |  |
| `service_id` | `int` | YES |  |
| `service_name` | `nvarchar(50)` | YES |  |
| `service_type` | `nvarchar(255)` | YES |  |
| `product` | `nvarchar(255)` | YES |  |
| `os` | `nvarchar(255)` | YES |  |
| `service_status` | `nvarchar(255)` | YES |  |
| `datacenter_code` | `nvarchar(15)` | YES |  |
| `datacenter_name` | `nvarchar(100)` | YES |  |
| `datacenter_city` | `nvarchar(100)` | YES |  |
| `mrc` | `numeric(38,4)` | YES |  |
| `sales_rep` | `nvarchar(255)` | YES |  |
| `tam` | `nvarchar(255)` | YES |  |
| `provision_date` | `datetime2` | YES |  |
| `line_of_business` | `nvarchar(255)` | YES |  |
| `currency` | `nvarchar(3)` | YES |  |
| `usd_mrc` | `numeric(38,4)` | YES |  |
| `cad_mrc` | `numeric(38,4)` | YES |  |
| `archive_date` | `datetime` | YES |  |
| `cad_budget_mrc` | `numeric(38,4)` | YES |  |
| `adjusted_line_of_business` | `nvarchar(50)` | YES |  |

**Sample rows (3):**

| integer_key | client_id | company_name | client_created | service_id | service_name | service_type | product | os | service_status | datacenter_code | datacenter_name | datacenter_city | mrc | sales_rep | tam | provision_date | line_of_business | currency | usd_mrc | cad_mrc | archive_date | cad_budget_mrc | adjusted_line_of_business |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4446753 | 4006121 | Diagnostic Systems Associates Inc. | 2003-08-07 16:14:50.906529 | 25143 | 25143 | server | Powerline 2100 | RHEL 3 ES | Online | IAD2 | South Pointe | Herndon | 181.2300 |  | NULL | 2004-05-12 15:33:56.301640 | Dedicated Hosting | USD | 181.2300 | 234.6153 | 2022-04-30 00:00:00 | 241.0359 | Hosting |
| 4446754 | 4016714 | Dtm Systems, Inc. | 2005-05-20 14:24:45.971385 | 38498 | 38498 | server | Powerline 2100 | Debian 3.0 Stable | Online | IAD2 | South Pointe | Herndon | 161.6200 |  | NULL | 2005-05-20 19:00:17.912864 | Dedicated Hosting | USD | 161.6200 | 209.2287 | 2022-04-30 00:00:00 | 214.9546 | Hosting |
| 4446755 | 4022044 | NetAlerts Inc. | 2007-03-30 17:18:18.679601 | 61370 | 61370 | server | Powerline 2200 | CentOS | Online | IAD2 | South Pointe | Herndon | 141.6300 |  | NULL | 2007-03-30 18:40:17.375540 | Dedicated Hosting | USD | 141.6300 | 183.3502 | 2022-04-30 00:00:00 | 188.3679 | Hosting |

---

### `[dbo].[dimClientsActive]`

**Status:** ✅ accessible  
**Rows:** 772  
**Size:** 5.5 MB  

| Column | Type | Nullable | PK |
|--------|------|----------|-----|
| `source_system` | `varchar(5)` | NO |  |
| `client_id` | `int` | NO |  |
| `company_name` | `nvarchar(255)` | NO |  |
| `client_type` | `nvarchar(64)` | YES |  |
| `city` | `nvarchar(50)` | YES |  |
| `state` | `nvarchar(50)` | YES |  |
| `zip_code` | `nvarchar(100)` | YES |  |
| `country` | `nvarchar(50)` | YES |  |
| `account_manager` | `nvarchar(50)` | YES |  |
| `account_executive` | `nvarchar(50)` | YES |  |
| `tam` | `nvarchar(50)` | YES |  |
| `crm` | `nvarchar(50)` | YES |  |
| `region` | `nvarchar(50)` | YES |  |
| `is_ecommerce` | `nvarchar(3)` | NO |  |
| `is_nbt` | `nvarchar(3)` | NO |  |
| `is_french_entity` | `nvarchar(3)` | NO |  |
| `customer_tier` | `nvarchar(11)` | NO |  |
| `ocean_tier` | `nvarchar(11)` | YES |  |
| `ce_pod` | `nvarchar(50)` | YES |  |
| `market_segment` | `nvarchar(50)` | YES |  |
| `referred_by` | `int` | YES |  |
| `created_on` | `datetime2` | NO |  |
| `datacenter_count` | `int` | YES |  |
| `datacenter_codes` | `nvarchar(201)` | YES |  |
| `original_currency_mrc` | `numeric(38,4)` | YES |  |
| `current_usd_mrc` | `numeric(38,4)` | YES |  |
| `usd_cloud_charges` | `numeric(38,4)` | YES |  |
| `usd_mrc_cloud_combined` | `numeric(38,4)` | YES |  |
| `current_cad_mrc` | `numeric(38,4)` | YES |  |
| `cad_cloud_charges` | `numeric(38,4)` | YES |  |
| `cad_mrc_cloud_combined` | `numeric(38,4)` | YES |  |
| `cad_budget_mrc` | `numeric(38,4)` | YES |  |
| `cad_budget_cloud_charges` | `numeric(38,4)` | YES |  |
| `cad_budget_mrc_cloud_combined` | `numeric(38,4)` | YES |  |
| `prev_month_usd_mrc` | `numeric(38,4)` | YES |  |
| `prev_year_usd_mrc` | `numeric(38,4)` | YES |  |
| `prev_month_cad_mrc` | `numeric(38,4)` | YES |  |
| `prev_year_cad_mrc` | `numeric(38,4)` | YES |  |
| `managed_hosting_usd_mrc` | `numeric(38,4)` | YES |  |
| `dedicated_hosting_usd_mrc` | `numeric(38,4)` | YES |  |
| `colocation_usd_mrc` | `numeric(38,4)` | YES |  |
| `managed_hosting_cad_mrc` | `numeric(38,4)` | YES |  |
| `dedicated_hosting_cad_mrc` | `numeric(38,4)` | YES |  |
| `colocation_cad_mrc` | `numeric(38,4)` | YES |  |
| `usd_mcc_charges` | `numeric(38,4)` | YES |  |
| `usd_cloudone_charges` | `numeric(38,4)` | YES |  |
| `usd_ondemand_charges` | `numeric(38,4)` | YES |  |
| `cad_mcc_charges` | `numeric(38,4)` | YES |  |
| `cad_cloudone_charges` | `numeric(38,4)` | YES |  |
| `cad_ondemand_charges` | `numeric(38,4)` | YES |  |
| `last_updated` | `datetime2` | NO |  |
| `salesforce_account_id` | `nvarchar(255)` | YES |  |
| `is_at_risk` | `nvarchar(255)` | YES |  |

**Sample rows (3):**

| source_system | client_id | company_name | client_type | city | state | zip_code | country | account_manager | account_executive | tam | crm | region | is_ecommerce | is_nbt | is_french_entity | customer_tier | ocean_tier | ce_pod | market_segment | referred_by | created_on | datacenter_count | datacenter_codes | original_currency_mrc | current_usd_mrc | usd_cloud_charges | usd_mrc_cloud_combined | current_cad_mrc | cad_cloud_charges | cad_mrc_cloud_combined | cad_budget_mrc | cad_budget_cloud_charges | cad_budget_mrc_cloud_combined | prev_month_usd_mrc | prev_year_usd_mrc | prev_month_cad_mrc | prev_year_cad_mrc | managed_hosting_usd_mrc | dedicated_hosting_usd_mrc | colocation_usd_mrc | managed_hosting_cad_mrc | dedicated_hosting_cad_mrc | colocation_cad_mrc | usd_mcc_charges | usd_cloudone_charges | usd_ondemand_charges | cad_mcc_charges | cad_cloudone_charges | cad_ondemand_charges | last_updated | salesforce_account_id | is_at_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ocean | 5714091 | Destination Freight Pty Ltd. | Retail | Hendra | Queensland | 4011 | Australia | Darren Wells | NULL | NULL | NULL | APAC | No | No | No | Standard | Standard | Enhanced and Standard | SMB - Inside | NULL | 2003-07-09 09:40:57.187000 | 1 | MIA | 431.1300 | 431.1300 | NULL | 431.1300 | 584.4680 | NULL | 584.4680 | 573.4029 | NULL | 573.4029 | 431.1300 | 421.1300 | 580.6868 | 575.1303 | 431.1300 | NULL | NULL | 584.4680 | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | 2026-04-13 07:54:45.666666 | 0013000000Gkf1oAAB | No |
| Ocean | 7036692 | The Regional Group of Companies Inc. | Retail | Ottawa | Ontario | K2C 0P9 | Canada | Roland Gonzales | NULL | NULL | NULL | Canada | No | No | No | Standard | NULL | NULL | Enterprise - Field | NULL | 2025-01-15 07:29:30.114872 | 1 | CLOUD-CA | 0.0000 | 0.0000 | 502.3960 | 502.3960 | 0.0000 | 691.4800 | 691.4800 | 0.0000 | 691.4800 | 691.4800 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | 2026-04-13 07:54:45.666666 | 001OF00000FysphYAB | No |
| Ocean | 7006129 | My World Info Local Information Cooperative | Retail | Anchorage | Alaska | 99508 | United States | Elizabeth Perez | NULL | NULL | NULL | US | No | No | No | Standard | Standard | Enhanced and Standard | Customer Care - Inside | NULL | 2011-09-23 16:06:28.802292 | 1 | IAD2 | 431.5800 | 431.5800 | NULL | 431.5800 | 585.0780 | NULL | 585.0780 | 574.0014 | NULL | 574.0014 | 431.5800 | 431.5800 | 581.2930 | 589.4017 | NULL | 431.5800 | NULL | NULL | 585.0780 | NULL | NULL | NULL | NULL | NULL | NULL | NULL | 2026-04-13 07:54:45.666666 | 0018000000rfvl3AAA | No |

---

### `[dbo].[dimComponents]`

**Status:** ✅ accessible  
**Rows:** 1,619,210  
**Size:** 702.4 MB  

| Column | Type | Nullable | PK |
|--------|------|----------|-----|
| `integer_key` | `int` | NO | ✓ |
| `client_id` | `int` | NO |  |
| `component_category` | `nvarchar(32)` | NO |  |
| `service_option_type` | `nvarchar(64)` | NO |  |
| `component_type` | `nvarchar(64)` | NO |  |
| `component` | `nvarchar(64)` | NO |  |
| `add_on` | `int` | YES |  |
| `currency` | `nvarchar(3)` | NO |  |
| `component_mrc` | `numeric(38,4)` | NO |  |
| `product_mrc` | `numeric(38,4)` | YES |  |
| `product` | `nvarchar(255)` | YES |  |
| `component_date` | `datetime2` | NO |  |
| `provision_date` | `datetime2` | YES |  |
| `is_online` | `varchar(3)` | NO |  |
| `service_id` | `int` | NO |  |
| `is_virtual` | `int` | YES |  |
| `datacenter_city` | `nvarchar(100)` | YES |  |
| `datacenter_code` | `nvarchar(MAX)` | YES |  |
| `line_of_business` | `nvarchar(255)` | YES |  |
| `component_id` | `int` | NO |  |
| `usd_component_mrc` | `numeric(38,4)` | YES |  |
| `usd_product_mrc` | `numeric(38,4)` | YES |  |
| `is_emea` | `varchar(3)` | NO |  |
| `last_updated` | `datetime2` | YES |  |
| `cad_component_mrc` | `numeric(38,4)` | YES |  |
| `cad_product_mrc` | `numeric(38,4)` | YES |  |
| `cad_budget_component_mrc` | `numeric(38,4)` | YES |  |
| `cad_budget_product_mrc` | `numeric(38,4)` | YES |  |
| `adjusted_line_of_business` | `nvarchar(255)` | YES |  |

**Sample rows (3):**

| integer_key | client_id | component_category | service_option_type | component_type | component | add_on | currency | component_mrc | product_mrc | product | component_date | provision_date | is_online | service_id | is_virtual | datacenter_city | datacenter_code | line_of_business | component_id | usd_component_mrc | usd_product_mrc | is_emea | last_updated | cad_component_mrc | cad_product_mrc | cad_budget_component_mrc | cad_budget_product_mrc | adjusted_line_of_business |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5754786 | Backup & Storage | backup | Daily | Tivoli Backup - Daily Incremental | 1 | USD | 81.3600 | 299.0000 | High Performance 100a | 2008-07-12 00:00:00 | 2003-06-12 15:28:00 | No | 178648 | 0 | Atlanta | ATL | Managed Hosting | 262 | 81.3600 | 299.0000 | No | 2026-04-13 07:54:47.966666 | 110.2969 | 405.3439 | 108.2088 | 397.6700 | Hosting |
| 2 | 5754786 | Hardware | ram | Generic | 512MB Generic RAM | 0 | USD | 0.0000 | 299.0000 | High Performance 100a | 2003-06-12 00:00:00 | 2003-06-12 15:28:00 | No | 178648 | 0 | Atlanta | ATL | Managed Hosting | 44 | 0.0000 | 299.0000 | No | 2026-04-13 07:54:47.966666 | 0.0000 | 405.3439 | 0.0000 | 397.6700 | Hosting |
| 3 | 5751415 | Software | ssl | SSL | P1 - Verisign Global Server ID - 128 bit 1year | 0 | USD | 0.0000 | 399.9500 | Enterprise Plan | 2008-01-09 00:00:00 | 2000-05-16 00:00:00 | No | 224927 | 0 | Atlanta | ATL | Managed Hosting | 166 | 0.0000 | 399.9500 | No | 2026-04-13 07:54:47.966666 | 0.0000 | 542.1983 | 0.0000 | 531.9335 | Hosting |

---

### `[dbo].[dimCustomerAttributes]`

**Status:** ✅ accessible  
**Rows:** 25,199  
**Size:** 10.9 MB  

| Column | Type | Nullable | PK |
|--------|------|----------|-----|
| `client_id` | `int` | NO |  |
| `company_name` | `nvarchar(255)` | NO |  |
| `client_type` | `nvarchar(64)` | YES |  |
| `city` | `nvarchar(50)` | YES |  |
| `state` | `nvarchar(50)` | YES |  |
| `zip_code` | `nvarchar(100)` | YES |  |
| `country` | `nvarchar(50)` | YES |  |
| `is_active` | `nvarchar(3)` | NO |  |
| `is_emea` | `nvarchar(3)` | NO |  |
| `is_french_entity` | `nvarchar(3)` | NO |  |
| `is_ecommerce` | `nvarchar(3)` | NO |  |
| `is_nbt` | `nvarchar(3)` | NO |  |
| `is_pci` | `nvarchar(3)` | NO |  |
| `is_blacklisted` | `nvarchar(3)` | YES |  |
| `date_blacklisted` | `datetime2` | YES |  |
| `referred_by` | `int` | YES |  |
| `created_on` | `datetime2` | NO |  |
| `tam` | `nvarchar(50)` | YES |  |
| `crm` | `nvarchar(50)` | YES |  |
| `mh_bdc` | `nvarchar(50)` | YES |  |
| `dh_bdc` | `nvarchar(50)` | YES |  |
| `colo_bdc` | `nvarchar(50)` | YES |  |
| `cloud_bdc` | `nvarchar(50)` | YES |  |
| `account_manager` | `nvarchar(50)` | YES |  |
| `account_executive` | `nvarchar(50)` | YES |  |
| `channel_sales_exec` | `nvarchar(50)` | YES |  |
| `region` | `nvarchar(50)` | YES |  |
| `subregion` | `nvarchar(50)` | YES |  |
| `microsoft_region` | `nvarchar(50)` | YES |  |
| `sales_rep_region` | `nvarchar(50)` | YES |  |
| `customer_tier` | `nvarchar(11)` | YES |  |
| `ocean_tier` | `nvarchar(11)` | YES |  |
| `ce_pod` | `nvarchar(50)` | YES |  |
| `sales_pod` | `nvarchar(50)` | YES |  |
| `market_segment` | `nvarchar(50)` | YES |  |
| `business_unit` | `nvarchar(50)` | YES |  |
| `last_updated` | `datetime2` | NO |  |
| `salesforce_account_id` | `nvarchar(255)` | YES |  |
| `tax_types` | `nvarchar(200)` | YES |  |
| `tax_codes` | `nvarchar(400)` | YES |  |
| `industry` | `nvarchar(50)` | YES |  |
| `sub_industry` | `nvarchar(50)` | YES |  |

**Sample rows (3):**

| client_id | company_name | client_type | city | state | zip_code | country | is_active | is_emea | is_french_entity | is_ecommerce | is_nbt | is_pci | is_blacklisted | date_blacklisted | referred_by | created_on | tam | crm | mh_bdc | dh_bdc | colo_bdc | cloud_bdc | account_manager | account_executive | channel_sales_exec | region | subregion | microsoft_region | sales_rep_region | customer_tier | ocean_tier | ce_pod | sales_pod | market_segment | business_unit | last_updated | salesforce_account_id | tax_types | tax_codes | industry | sub_industry |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7036470 | BJS Distribution Storage and Couriers Limited | Retail | Wednesbury | NULL | WS10 8RR | United Kingdom | Yes | Yes | No | No | No | No | No | NULL | NULL | 2021-04-15 09:46:52.641219 | NULL | NULL | NULL | NULL | Darren Wells | Darren Wells | Darren Wells | NULL | NULL | EMEA | NULL | UK | NULL | Standard | NULL | NULL | NULL | Enterprise - Field | Data Center | 2026-04-13 07:50:41.963333 | 0011E00001nNxeAQAS | VAT | GB 979489625 | Transportation | Freight & Logistics Services |
| 7014921 | Digitcom Telecommunications Canada Inc | Retail | North York | Ontario | M3J 3A6 | Canada | No | No | No | No | No | No | No | NULL | NULL | 2020-04-24 11:48:40.975601 | NULL | NULL | Steven Lyew | NULL | NULL | NULL | Steven Lyew | NULL | NULL | Canada | NULL | Canada | NULL | NULL | NULL | NULL | NULL | Enterprise - Field | NULL | 2026-04-13 07:50:41.963333 | NULL |  |  |  |  |
| 7014927 | CCS MEDIA LIMITED | Retail | Nottingham | NULL | NG1 6HH | United Kingdom | No | Yes | No | No | No | No | No | NULL | NULL | 2020-05-14 15:40:25.964061 | NULL | NULL | NULL | NULL | DCSalesOPS  | NULL | Caroline Searle | NULL | NULL | EMEA | NULL | UK | NULL | NULL | NULL | NULL | NULL | Enterprise - Field | Data Center | 2026-04-13 07:50:41.963333 | 0018000000wXwVXAA0 |  |  | Business Services | NULL |

---

### `[dbo].[dimJIRATickets]`

**Status:** ✅ accessible  
**Rows:** 124,083  
**Size:** 37.2 MB  

| Column | Type | Nullable | PK |
|--------|------|----------|-----|
| `jira_number` | `int` | YES |  |
| `reporter` | `nvarchar(500)` | YES |  |
| `summary` | `nvarchar(500)` | YES |  |
| `priority_id` | `nvarchar(500)` | YES |  |
| `date_opened` | `datetime2` | YES |  |
| `last_updated` | `datetime2` | YES |  |
| `creator` | `nvarchar(500)` | YES |  |
| `issue_type` | `nvarchar(500)` | YES |  |
| `issue_status` | `nvarchar(500)` | YES |  |
| `priority` | `nvarchar(500)` | YES |  |
| `resolution` | `nvarchar(500)` | YES |  |
| `resolution_date` | `datetime2` | YES |  |
| `reporter_department` | `nvarchar(500)` | YES |  |
| `project_name` | `nvarchar(500)` | YES |  |
| `project_code` | `nvarchar(500)` | YES |  |
| `last_update` | `datetime2` | YES |  |
| `issuenum` | `numeric(18,0)` | YES |  |

**Sample rows (3):**

| jira_number | reporter | summary | priority_id | date_opened | last_updated | creator | issue_type | issue_status | priority | resolution | resolution_date | reporter_department | project_name | project_code | last_update | issuenum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 63821 | amoon | VPN setup | 4 | 2012-08-13 14:12:15 | 2012-08-13 20:14:08 | amoon | Task | PdM WIP | Minor | Fixed | 2012-08-13 20:14:08 | NULL | OLD IT Support 2 - Do not use | ITSUPPORTNEW | 2023-07-18 01:30:04.560000 | 3073 |
| 63822 | devbugteam | FW: MIA  - Add node tool. | 1 | 2012-08-13 14:24:17 | 2015-06-25 09:58:02 | gpeck | Incident | Closed | Blocker | Duplicate | 2012-08-13 15:20:28 | Customer Experience | Development Service and Support | DSS | 2023-07-18 01:30:04.560000 | 955 |
| 63823 | cromero | IT Meeting 8/13 | 8 | 2012-08-13 14:29:22 | 2012-11-15 12:57:20 | cromero | Maintenance | Closed | Unknown | Complete | 2012-08-13 14:29:43 | NULL | OLD - IT Infrastructure - Project Deprecated | ITINF | 2023-07-18 01:30:04.560000 | 1953 |

---

### `[dbo].[dimProductAttributes]`

**Status:** ✅ accessible  
**Rows:** 7,107  
**Size:** 4.4 MB  

| Column | Type | Nullable | PK |
|--------|------|----------|-----|
| `fusion_id` | `nvarchar(255)` | YES |  |
| `sku_name` | `nvarchar(4000)` | YES |  |
| `level` | `nvarchar(255)` | YES |  |
| `is_active` | `nvarchar(255)` | YES |  |
| `type` | `nvarchar(255)` | YES |  |
| `service_type` | `nvarchar(255)` | YES |  |
| `category` | `nvarchar(255)` | YES |  |
| `functional_group` | `nvarchar(255)` | YES |  |
| `lifecycle` | `nvarchar(255)` | YES |  |
| `product_group` | `nvarchar(255)` | YES |  |
| `license_cost_cad` | `numeric(38,4)` | YES |  |
| `functional_group_bi` | `nvarchar(255)` | YES |  |
| `sku_nickname` | `nvarchar(255)` | YES |  |
| `search_keywords` | `nvarchar(4000)` | YES |  |
| `adjusted_line_of_business` | `nvarchar(255)` | YES |  |
| `technology_group` | `nvarchar(255)` | YES |  |
| `product_type` | `nvarchar(255)` | YES |  |
| `product_line` | `nvarchar(255)` | YES |  |
| `product_part` | `nvarchar(255)` | YES |  |
| `vendor` | `nvarchar(255)` | YES |  |
| `product_cost_cad` | `numeric(38,4)` | YES |  |
| `release_date` | `datetime2` | YES |  |
| `product` | `nvarchar(255)` | YES |  |
| `product_category` | `nvarchar(255)` | YES |  |
| `product_detail` | `nvarchar(255)` | YES |  |
| `new_lob_2021` | `nvarchar(MAX)` | YES |  |

**Sample rows (3):**

| fusion_id | sku_name | level | is_active | type | service_type | category | functional_group | lifecycle | product_group | license_cost_cad | functional_group_bi | sku_nickname | search_keywords | adjusted_line_of_business | technology_group | product_type | product_line | product_part | vendor | product_cost_cad | release_date | product | product_category | product_detail | new_lob_2021 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | .NET extensions (unmanaged) | Component | 0 | Other | Software | Software | Software Misc | End of Sale | Software | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | 2008-08-02 02:11:51 | Microsoft | Infrastructure Services | None | Legacy Managed Hosting |
| 1 | Business - 2.2 | TLS | 0 | Server | NULL | NULL | Server | End of Life | Servers | NULL | NULL | NULL | NULL | Hosting | Infrastructure | Dedicated Hosting | Hosting | N-6 | NULL | NULL | 2008-08-02 02:11:52 | Managed Servers | NULL | Servers - EOL | IaaS |
| 10 | 146GB SCSI (15K) | Component | 0 | SCSI | Hard Drive | Hardware | Server HDD | End of Sale | Servers | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | 2008-08-02 02:11:51 | Server Components | Infrastructure Services | Hardware Component | Legacy Managed Hosting |

---

### `[dbo].[dimServiceAttributes]`

**Status:** ✅ accessible  
**Rows:** 162,782  
**Size:** 62.1 MB  

| Column | Type | Nullable | PK |
|--------|------|----------|-----|
| `service_id` | `int` | NO | ✓ |
| `client_id` | `int` | NO |  |
| `service_status` | `nvarchar(255)` | YES |  |
| `is_active` | `nvarchar(3)` | NO |  |
| `provision_date` | `datetime2` | YES |  |
| `cancel_date` | `datetime2` | YES |  |
| `deprovision_date` | `datetime2` | YES |  |
| `offline_date` | `datetime2` | YES |  |
| `product` | `nvarchar(255)` | YES |  |
| `nickname` | `nvarchar(64)` | YES |  |
| `server_name` | `nvarchar(255)` | YES |  |
| `OS` | `nvarchar(255)` | YES |  |
| `is_pci` | `nvarchar(3)` | NO |  |
| `is_magento` | `nvarchar(3)` | NO |  |
| `datacenter_name` | `nvarchar(100)` | YES |  |
| `datacenter_city` | `nvarchar(100)` | YES |  |
| `datacenter_code` | `nvarchar(15)` | YES |  |
| `contract_length` | `int` | YES |  |
| `contract_months_remaining` | `int` | YES |  |
| `service_type` | `nvarchar(64)` | YES |  |
| `line_of_business` | `nvarchar(255)` | YES |  |
| `last_updated` | `datetime2` | NO |  |
| `fusion_id` | `int` | YES |  |
| `adjusted_line_of_business` | `nvarchar(255)` | YES |  |

**Sample rows (3):**

| service_id | client_id | service_status | is_active | provision_date | cancel_date | deprovision_date | offline_date | product | nickname | server_name | OS | is_pci | is_magento | datacenter_name | datacenter_city | datacenter_code | contract_length | contract_months_remaining | service_type | line_of_business | last_updated | fusion_id | adjusted_line_of_business |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 282 | 4000268 | Deprovision | No | 2002-07-10 22:43:57.430000 | 2012-01-31 18:55:08.426666 | 2012-02-07 18:57:29.813333 | NULL | Starter Server | 268-1 | 282 | CentOS | No | No | Vicar | San Antonio | SAT5 | 1 | NULL | server | Dedicated Hosting | 2026-04-13 07:48:17.253333 | 128 | Hosting |
| 1301 | 4000943 | Deprovision | No | 2002-09-23 14:08:49.460000 | 2011-01-07 11:15:02.950000 | 2011-01-14 11:18:03.550000 | NULL | Powerline 2200 | 943-1 | 1301 | Debian | No | No | Vicar | San Antonio | SAT5 | 1 | NULL | server | Dedicated Hosting | 2026-04-13 07:48:17.253333 | 286 | Hosting |
| 2529 | 4001872 | Deprovision | No | 2002-12-18 12:13:27.746666 | 2010-07-13 20:00:38.536666 | 2010-07-20 20:10:40.286666 | NULL | Starter Server | 1872-1 | 2529 | RedHat 7.3 OS | No | No | Vicar | San Antonio | SAT5 | 1 | NULL | server | Dedicated Hosting | 2026-04-13 07:48:17.253333 | 128 | Hosting |

---

### `[dbo].[dimServices]`

**Status:** ✅ accessible  
**Rows:** 5,732  
**Size:** 27.4 MB  

| Column | Type | Nullable | PK |
|--------|------|----------|-----|
| `client_id` | `int` | NO |  |
| `company_name` | `nvarchar(255)` | YES |  |
| `service_id` | `int` | NO | ✓ |
| `nickname` | `nvarchar(64)` | NO |  |
| `server_name` | `nvarchar(255)` | YES |  |
| `product` | `nvarchar(255)` | YES |  |
| `service_status` | `nvarchar(255)` | YES |  |
| `os` | `nvarchar(255)` | YES |  |
| `currency` | `nvarchar(3)` | NO |  |
| `provision_date` | `datetime2` | YES |  |
| `datacenter_name` | `nvarchar(100)` | YES |  |
| `datacenter_city` | `nvarchar(100)` | YES |  |
| `datacenter_code` | `nvarchar(15)` | YES |  |
| `line_of_business` | `nvarchar(255)` | YES |  |
| `device_id` | `nvarchar(64)` | YES |  |
| `service_type` | `nvarchar(64)` | YES |  |
| `mrc` | `numeric(38,4)` | YES |  |
| `usd_mrc` | `numeric(38,4)` | YES |  |
| `cad_mrc` | `numeric(38,4)` | YES |  |
| `contract_length` | `int` | YES |  |
| `contract_months_remaining` | `int` | YES |  |
| `last_updated` | `datetime2` | NO |  |
| `cad_budget_mrc` | `numeric(38,4)` | YES |  |
| `fusion_id` | `int` | YES |  |
| `adjusted_line_of_business` | `nvarchar(255)` | YES |  |

**Sample rows (3):**

| client_id | company_name | service_id | nickname | server_name | product | service_status | os | currency | provision_date | datacenter_name | datacenter_city | datacenter_code | line_of_business | device_id | service_type | mrc | usd_mrc | cad_mrc | contract_length | contract_months_remaining | last_updated | cad_budget_mrc | fusion_id | adjusted_line_of_business |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7008089 | Mosaic Online Systems Ltd | -7008600 |  |  | B/W-TRAFFIC                     | Online | NULL | GBP | 1999-01-01 00:00:00 | Croydon | London | CRO | Colocation | NULL | colocation | 0.0000 | 0.0000 | 0.0000 | -1 | -1 | 2026-04-13 07:48:11.980000 | 0.0000 | 0 | Colocation |
| 7008089 | Mosaic Online Systems Ltd | -7008510 |  |  | CONNECT-CROSS CONNECT           | Online | NULL | GBP | 1999-01-01 00:00:00 | Croydon | London | CRO | Colocation | NULL | colocation | 236.2700 | 313.1389 | 389.8455 | -1 | -1 | 2026-04-13 07:48:11.980000 | 389.8455 | 0 | Colocation |
| 7008089 | Mosaic Online Systems Ltd | -7008399 |  |  | B/W-COMMIT                      | Online | NULL | GBP | 1999-01-01 00:00:00 | Croydon | London | CRO | Colocation | NULL | colocation | 2205.1000 | 2922.5145 | 3638.4150 | -1 | -1 | 2026-04-13 07:48:11.980000 | 3638.4150 | 0 | Colocation |

---

### `[dbo].[dimdatacenterattributes]`

**Status:** ✅ accessible  
**Rows:** 53  
**Size:** 0.0 MB  

| Column | Type | Nullable | PK |
|--------|------|----------|-----|
| `datacenter_code` | `nvarchar(255)` | YES |  |
| `datacenter_city` | `nvarchar(255)` | YES |  |
| `datacenter_name` | `nvarchar(255)` | YES |  |
| `country` | `nvarchar(255)` | YES |  |
| `datacenter_region` | `nvarchar(255)` | YES |  |
| `cp1_datacenter_code` | `nvarchar(255)` | YES |  |
| `datacenter_nickname` | `nvarchar(255)` | YES |  |
| `address` | `nvarchar(255)` | YES |  |
| `legacy_entity` | `nvarchar(255)` | YES |  |
| `previous_references` | `nvarchar(255)` | YES |  |
| `datacenter_status` | `nvarchar(255)` | YES |  |
| `datacenter_report_name` | `nvarchar(255)` | YES |  |

**Sample rows (3):**

| datacenter_code | datacenter_city | datacenter_name | country | datacenter_region | cp1_datacenter_code | datacenter_nickname | address | legacy_entity | previous_references | datacenter_status | datacenter_report_name |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T3-AU1 | Sydney | Sydney (MCC) | Australia | Canada | NULL | NULL | NULL | NULL | NULL | Decommissioned | NULL |
| AZURE-CAN | NULL | AZURE-CAN | Canada | Canada | NULL | Azure Canada | NULL | NULL | NULL | Active | Azure Canada (AZURE-CAN) |
| AZURE-US | NULL | AZURE-US | United States | US | NULL | Azure United States | NULL | NULL | NULL | Active | Azure United States (AZURE-US) |

---

### `[dbo].[run_rate_by_customer]`

**Status:** ✅ accessible  
**Rows:** 249,830  
**Size:** 90.7 MB  

| Column | Type | Nullable | PK |
|--------|------|----------|-----|
| `data_source` | `nvarchar(255)` | YES |  |
| `kpi_type` | `nvarchar(255)` | YES |  |
| `change_type` | `nvarchar(255)` | YES |  |
| `archive_date` | `nvarchar(255)` | YES |  |
| `client_id` | `nvarchar(255)` | YES |  |
| `company_name` | `nvarchar(255)` | YES |  |
| `line_of_business` | `nvarchar(255)` | YES |  |
| `region` | `nvarchar(255)` | YES |  |
| `datacenter_name` | `nvarchar(255)` | YES |  |
| `currency` | `nvarchar(255)` | YES |  |
| `is_french_entity` | `nvarchar(255)` | YES |  |
| `mrc` | `numeric(38,4)` | YES |  |
| `cad_budget_mrc` | `numeric(38,4)` | YES |  |
| `adjusted_line_of_business` | `nvarchar(255)` | YES |  |
| `datacenter_city` | `nvarchar(255)` | YES |  |
| `Revenue Entity` | `nvarchar(255)` | YES |  |
| `Sales Region` | `nvarchar(255)` | YES |  |
| `Sales Rep` | `nvarchar(255)` | YES |  |
| `Sales Director` | `nvarchar(255)` | YES |  |
| `business_unit` | `nvarchar(255)` | YES |  |

**Sample rows (3):**

| data_source | kpi_type | change_type | archive_date | client_id | company_name | line_of_business | region | datacenter_name | currency | is_french_entity | mrc | cad_budget_mrc | adjusted_line_of_business | datacenter_city | Revenue Entity | Sales Region | Sales Rep | Sales Director | business_unit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BI Report | CHURN | NULL | 2017-09-01 00:00:00 | 4000928 | Unfiction.com | Dedicated Hosting | US | Malibu | USD | No | -278.0000 | -369.7400 | Hosting | Los Angeles | US/LATAM | US/LATAM | Daniel Morgan | Aaron Delagarza | NULL |
| BI Report | CHURN | NULL | 2017-09-01 00:00:00 | 4002497 | Webhosting.net. Inc | Dedicated Hosting | US | Vicar | USD | No | -101.3900 | -134.8487 | Hosting | San Antonio | US/LATAM | US/LATAM | Daniel Morgan | Aaron Delagarza | NULL |
| BI Report | CHURN | NULL | 2017-09-01 00:00:00 | 4003242 | Yenni Digital | Dedicated Hosting | US | Malibu | USD | No | -99.0000 | -131.6700 | Hosting | Los Angeles | US/LATAM | US/LATAM | Customer Experience AM | Meagan Agnew | NULL |

---

### `[profitability].[ocean_sku_cost]`

**Status:** ✅ accessible  
**Rows:** 680  
**Size:** 0.2 MB  

| Column | Type | Nullable | PK |
|--------|------|----------|-----|
| `sku_level` | `varchar(255)` | YES |  |
| `sku_category` | `varchar(255)` | YES |  |
| `sku_id` | `int` | YES |  |
| `sku_name` | `varchar(255)` | YES |  |
| `sku_type` | `varchar(255)` | YES |  |
| `sku_cost` | `float` | YES |  |
| `cost_currency` | `varchar(255)` | YES |  |
| `vendor` | `varchar(255)` | YES |  |
| `comments` | `varchar(255)` | YES |  |

**Sample rows (3):**

| sku_level | sku_category | sku_id | sku_name | sku_type | sku_cost | cost_currency | vendor | comments |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Component | Hardware | 3258 | 1 TB 7200 3.5 Inch SATA | hdd | 16.0 | USD | NULL | NULL |
| Component | Hardware | 1810 | 1 TB 7200 SATA | hdd | 16.0 | USD | NULL | NULL |
| Component | Hardware | 6090 | 1.92 TB SSD | hdd | 349.0 | USD | NULL | NULL |

---

### `[renewals].[ocean_services_renewal_date]`

**Status:** ✅ accessible  
**Rows:** 5,667  
**Size:** 0.7 MB  

| Column | Type | Nullable | PK |
|--------|------|----------|-----|
| `client_id` | `int` | NO |  |
| `company_name` | `nvarchar(255)` | YES |  |
| `service_id` | `int` | NO |  |
| `expiration_date` | `datetime2` | YES |  |
| `m2m` | `varchar(255)` | YES |  |
| `cad_budget_mrc` | `numeric(38,4)` | YES |  |
| `service_status` | `nvarchar(255)` | YES |  |
| `first_term` | `varchar(3)` | NO |  |
| `last_updated` | `datetime` | NO |  |

**Sample rows (3):**

| client_id | company_name | service_id | expiration_date | m2m | cad_budget_mrc | service_status | first_term | last_updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7008089 | Mosaic Online Systems Ltd | -7008600 | 2025-07-13 00:00:00 | no | 0.0000 | Online | no | 2026-04-13 10:15:02.703000 |
| 7008089 | Mosaic Online Systems Ltd | -7008510 | 2000-01-30 03:12:09 | yes | 389.8455 | Online | no | 2026-04-13 10:15:02.703000 |
| 7008089 | Mosaic Online Systems Ltd | -7008399 | 2025-07-13 00:00:00 | no | 3638.4150 | Online | no | 2026-04-13 10:15:02.703000 |

---

## All Accessible Tables

| Schema | Table | Rows | Size | Type |
|--------|-------|------|------|------|
| `dbo` | `Churn` ⭐ | 7,695 | 6.0 MB | BASE TABLE |
| `dbo` | `DateDimension` | 11,688 | 1.7 MB | BASE TABLE |
| `dbo` | `DimCustomerContacts` | 99,479 | 12.5 MB | BASE TABLE |
| `dbo` | `DimDCIMAssets` | 0 | 0.0 MB | BASE TABLE |
| `dbo` | `DimDCIMAssets_old` | 10,000 | 29.9 MB | BASE TABLE |
| `dbo` | `DimTLSAttributes` | 222 | 0.1 MB | BASE TABLE |
| `dbo` | `MRCTrend` ⭐ | 323,611 | 134.2 MB | BASE TABLE |
| `dbo` | `MRCTrend_TTSSiteScout` | 63,359 | 26.6 MB | BASE TABLE |
| `dbo` | `MrcTrendColo` | 132,248 | 57.6 MB | BASE TABLE |
| `dbo` | `PopularSalesInventoryTrend` | 5,759,052 | 1873.5 MB | BASE TABLE |
| `dbo` | `Sales` | 10,918 | 8.2 MB | BASE TABLE |
| `dbo` | `SalesBookOfBusiness` | 13,245 | 2.3 MB | BASE TABLE |
| `dbo` | `Tickets` | 851,065 | 785.3 MB | BASE TABLE |
| `dbo` | `Tickets_JSM` | 0 | 0.0 MB | BASE TABLE |
| `dbo` | `at_risk_sfdc` | 51 | 0.1 MB | BASE TABLE |
| `dbo` | `churn_month_to_date` | 23 | 0.2 MB | BASE TABLE |
| `dbo` | `cost_software_skus` | 391 | 0.1 MB | BASE TABLE |
| `dbo` | `dimChangeControl` | 21,788 | 16.1 MB | BASE TABLE |
| `dbo` | `dimClientsActive` ⭐ | 772 | 5.5 MB | BASE TABLE |
| `dbo` | `dimClientsActive_historical` | 5,052,281 | 4272.8 MB | BASE TABLE |
| `dbo` | `dimCloud_OtherUsageCharges` | 35,924 | 49.1 MB | BASE TABLE |
| `dbo` | `dimComponents` ⭐ | 1,619,210 | 702.4 MB | BASE TABLE |
| `dbo` | `dimComponents_TTSSiteScout` | 176,660 | 78.5 MB | BASE TABLE |
| `dbo` | `dimCredits` | 168,322 | 212.1 MB | BASE TABLE |
| `dbo` | `dimCurrencyExchangeRates` | 4,146 | 1.3 MB | BASE TABLE |
| `dbo` | `dimCustomerAttributes` ⭐ | 25,199 | 10.9 MB | BASE TABLE |
| `dbo` | `dimDCIMAssetsTrend` | 25,214 | 170.6 MB | BASE TABLE |
| `dbo` | `dimDevices` | 3,111 | 11.6 MB | BASE TABLE |
| `dbo` | `dimJIRATickets` ⭐ | 124,083 | 37.2 MB | BASE TABLE |
| `dbo` | `dimNotes` | 9,489 | 5.7 MB | BASE TABLE |
| `dbo` | `dimOpportunities` | 13,719 | 25.7 MB | BASE TABLE |
| `dbo` | `dimProduct` | 17 | 0.1 MB | BASE TABLE |
| `dbo` | `dimProductAttributes` ⭐ | 7,107 | 4.4 MB | BASE TABLE |
| `dbo` | `dimProductRevenue` | 1,943,906 | 825.0 MB | BASE TABLE |
| `dbo` | `dimServiceAttributes` ⭐ | 162,782 | 62.1 MB | BASE TABLE |
| `dbo` | `dimServices` ⭐ | 5,732 | 27.4 MB | BASE TABLE |
| `dbo` | `dimServices_TTSSiteScout` | 1,046 | 0.6 MB | BASE TABLE |
| `dbo` | `dimdatacenterattributes` ⭐ | 53 | 0.0 MB | BASE TABLE |
| `dbo` | `dimproductattributes_extended` | 0 | 0.0 MB | VIEW |
| `dbo` | `dimsalesrepscp1` | 11 | 0.1 MB | BASE TABLE |
| `dbo` | `last_thirty_days_avg_exchange_rate` | 0 | 0.0 MB | VIEW |
| `dbo` | `mrc_changes` | 477,009 | 74.7 MB | BASE TABLE |
| `dbo` | `order_notes_sharepoint_raw` | 0 | 0.1 MB | BASE TABLE |
| `dbo` | `product_special_attributes` | 279 | 0.1 MB | BASE TABLE |
| `dbo` | `run_rate_by_customer` ⭐ | 249,830 | 90.7 MB | BASE TABLE |
| `dbo` | `sales_month_to_date` | 18 | 0.1 MB | BASE TABLE |
| `dbo` | `sales_salestracker` | 34,318 | 54.2 MB | BASE TABLE |
| `dbo` | `salesforce_open_opportunities_trend` | 5,534,469 | 2409.6 MB | BASE TABLE |
| `dbo` | `salesforce_opportunity_trend` | 13,551,981 | 13124.5 MB | BASE TABLE |
| `dbo` | `software_skus` | 569 | 0.1 MB | BASE TABLE |
| `dbo` | `tasks` | 504,296 | 439.3 MB | BASE TABLE |
| `dbo` | `tasks_history` | 658,955 | 91.3 MB | BASE TABLE |
| `dbo` | `utility_billing_tracker` | 246 | 0.1 MB | BASE TABLE |
| `profitability` | `alertlogic_invoice_details` | 294 | 0.1 MB | BASE TABLE |
| `profitability` | `imperva_invoice_details` | 552 | 0.1 MB | BASE TABLE |
| `profitability` | `ocean_sku_cost` ⭐ | 680 | 0.2 MB | BASE TABLE |
| `renewals` | `ocean_services_renewal_date` ⭐ | 5,667 | 0.7 MB | BASE TABLE |
| `renewals` | `ocean_services_renewal_date_new` | 5,667 | 0.7 MB | BASE TABLE |

---

## Inaccessible Tables

| Schema | Table | Rows | Error |
|--------|-------|------|-------|

---

## Cross-Database Access

Queries from a `DM_BusinessInsights` connection to `FinancialReporting.*` tables.

| Database | Schema | Table | Accessible |
|----------|--------|-------|------------|
| `FinancialReporting` | `dbo` | `finance_revenue_mapping` | ✅ |
| `FinancialReporting` | `dbo` | `ARAgingSnapshot` | ❌ (pymssql.exceptions.ProgrammingError) (208, b"Invalid object name 'FinancialReporting.dbo.ARAgingSnapshot'.DB-Lib error message 20018, severity 16:\nGeneral SQL Server error: Check messages from the S |
