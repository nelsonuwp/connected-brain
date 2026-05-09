---
type: schema
object: dimComponents
updated: 2026-03-28
---

# dimComponents

**Source:** DM_BusinessInsights / dbo
**Description:** Component-level breakdown per service. Grouped by service_id.

## Columns

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| integer_key | int(10) | NO |  |
| client_id | int(10) | NO |  |
| component_category | nvarchar(32) | NO |  |
| service_option_type | nvarchar(64) | NO |  |
| component_type | nvarchar(64) | NO |  |
| component | nvarchar(64) | NO |  |
| add_on | int(10) | YES |  |
| currency | nvarchar(3) | NO |  |
| component_mrc | numeric(38,4) | NO |  |
| product_mrc | numeric(38,4) | YES |  |
| product | nvarchar(255) | YES |  |
| component_date | datetime2 | NO |  |
| provision_date | datetime2 | YES |  |
| is_online | varchar(3) | NO |  |
| service_id | int(10) | NO |  |
| is_virtual | int(10) | YES |  |
| datacenter_city | nvarchar(100) | YES |  |
| datacenter_code | nvarchar(MAX) | YES |  |
| line_of_business | nvarchar(255) | YES |  |
| component_id | int(10) | NO |  |
| usd_component_mrc | numeric(38,4) | YES |  |
| usd_product_mrc | numeric(38,4) | YES |  |
| is_emea | varchar(3) | NO |  |
| last_updated | datetime2 | YES |  |
| cad_component_mrc | numeric(38,4) | YES |  |
| cad_product_mrc | numeric(38,4) | YES |  |
| cad_budget_component_mrc | numeric(38,4) | YES |  |
| cad_budget_product_mrc | numeric(38,4) | YES |  |
| adjusted_line_of_business | nvarchar(255) | YES |  |

## Sample Data

| integer_key | client_id | component_category | service_option_type | component_type | component | add_on | currency | component_mrc | product_mrc | product | component_date | provision_date | is_online | service_id | is_virtual | datacenter_city | datacenter_code | line_of_business | component_id | usd_component_mrc | usd_product_mrc | is_emea | last_updated | cad_component_mrc | cad_product_mrc | cad_budget_component_mrc | cad_budget_product_mrc | adjusted_line_of_business |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5754786 | Backup & Storage | backup | Daily | Tivoli Backup - Daily Incremental | 1 | USD | 81.3600 | 299.0000 | High Performance 100a | 2008-07-12 00:00:00 | 2003-06-12 15:28:00 | No | 178648 | 0 | Atlanta | ATL | Managed Hosting | 262 | 81.3600 | 299.0000 | No | 2026-03-27 07:54:47.506666 | 109.6051 | 402.8015 | 108.2088 | 397.6700 | Hosting |
| 2 | 5754786 | Hardware | ram | Generic | 512MB Generic RAM | 0 | USD | 0.0000 | 299.0000 | High Performance 100a | 2003-06-12 00:00:00 | 2003-06-12 15:28:00 | No | 178648 | 0 | Atlanta | ATL | Managed Hosting | 44 | 0.0000 | 299.0000 | No | 2026-03-27 07:54:47.506666 | 0.0000 | 402.8015 | 0.0000 | 397.6700 | Hosting |
| 3 | 5751415 | Software | ssl | SSL | P1 - Verisign Global Server ID - 128 bit 1year | 0 | USD | 0.0000 | 399.9500 | Enterprise Plan | 2008-01-09 00:00:00 | 2000-05-16 00:00:00 | No | 224927 | 0 | Atlanta | ATL | Managed Hosting | 166 | 0.0000 | 399.9500 | No | 2026-03-27 07:54:47.506666 | 0.0000 | 538.7976 | 0.0000 | 531.9335 | Hosting |
| 4 | 5713729 | Hardware | chassis | Chassis | Accelerator 100 | 1 | USD | 549.9500 | 0.0000 | Accelerator Plan | 2008-07-10 00:00:00 | 2000-05-17 00:00:00 | No | 231113 | 0 | Atlanta | ATL | Managed Hosting | 329 | 549.9500 | 0.0000 | No | 2026-03-27 07:54:47.506666 | 740.8719 | 0.0000 | 731.4335 | 0.0000 | Hosting |
| 5 | 5713729 | Network | IPv4 | IPs | Dedicated IPs - Base 2 (Tier I) | 0 | USD | 0.0000 | 0.0000 | Accelerator Plan | 2002-10-10 00:00:00 | 2000-05-17 00:00:00 | No | 231113 | 0 | Atlanta | ATL | Managed Hosting | 82 | 0.0000 | 0.0000 | No | 2026-03-27 07:54:47.506666 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | Hosting |

## Usage Notes

- **Foreign key:** service_id (int) → dimServices.service_id
- Many rows per service — always GROUP BY or nest when joining to dimServices
- Use `cad_component_mrc` for cross-currency comparisons
- `component_category` groups components (Hardware, Software, Network, Backup & Storage, etc.)
- `add_on = 1` means this is an add-on component, not the base service
- `is_online = 'Yes'` for active components — filter to this when you only want live components
- Does not need client_id filter if already joined to dimServices with client_id filter
