---
type: schema
object: dimProductAttributes
updated: 2026-03-06
---

# dimProductAttributes

**Source:** DM_BusinessInsights / dbo
**Description:** Product attribute dimension.

## Columns

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| fusion_id | nvarchar(255) | YES |  |
| sku_name | nvarchar(4000) | YES |  |
| level | nvarchar(255) | YES |  |
| is_active | nvarchar(255) | YES |  |
| type | nvarchar(255) | YES |  |
| service_type | nvarchar(255) | YES |  |
| category | nvarchar(255) | YES |  |
| functional_group | nvarchar(255) | YES |  |
| lifecycle | nvarchar(255) | YES |  |
| product_group | nvarchar(255) | YES |  |
| license_cost_cad | numeric(38,4) | YES |  |
| functional_group_bi | nvarchar(255) | YES |  |
| sku_nickname | nvarchar(255) | YES |  |
| search_keywords | nvarchar(4000) | YES |  |
| adjusted_line_of_business | nvarchar(255) | YES |  |
| technology_group | nvarchar(255) | YES |  |
| product_type | nvarchar(255) | YES |  |
| product_line | nvarchar(255) | YES |  |
| product_part | nvarchar(255) | YES |  |
| vendor | nvarchar(255) | YES |  |
| product_cost_cad | numeric(38,4) | YES |  |
| release_date | datetime2 | YES |  |
| product | nvarchar(255) | YES |  |
| product_category | nvarchar(255) | YES |  |
| product_detail | nvarchar(255) | YES |  |
| new_lob_2021 | nvarchar(MAX) | YES |  |

## Sample Data

| fusion_id | sku_name | level | is_active | type | service_type | category | functional_group | lifecycle | product_group | license_cost_cad | functional_group_bi | sku_nickname | search_keywords | adjusted_line_of_business | technology_group | product_type | product_line | product_part | vendor | product_cost_cad | release_date | product | product_category | product_detail | new_lob_2021 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | .NET extensions (unmanaged) | Component | 0 | Other | Software | Software | Software Misc | End of Sale | Software |  |  |  |  |  |  |  |  |  |  |  | 2008-08-02 02:11:51 | Microsoft | Infrastructure Services | None | Legacy Managed Hosting |
| 1 | Business - 2.2 | TLS | 0 | Server |  |  | Server | End of Life | Servers |  |  |  |  | Hosting | Infrastructure | Dedicated Hosting | Hosting | N-6 |  |  | 2008-08-02 02:11:52 | Managed Servers |  | Servers - EOL | IaaS |
| 10 | 146GB SCSI (15K) | Component | 0 | SCSI | Hard Drive | Hardware | Server HDD | End of Sale | Servers |  |  |  |  |  |  |  |  |  |  |  | 2008-08-02 02:11:51 | Server Components | Infrastructure Services | Hardware Component | Legacy Managed Hosting |
| 10 | Business Professional - L2 | TLS | 0 | Server |  |  | Server | Discontinuation of Support | Servers |  |  |  |  | Hosting | Infrastructure | Dedicated Hosting | Hosting |  |  |  | 2008-08-02 02:11:52 | Managed Servers | Infrastructure Services | Servers - EOL | Legacy Managed Hosting |
| 100 | Ensim Pro v3.6 500 Domain | Component | 0 | Ensim | Control Panel | Software | Control Panel | End of Life | Software |  |  |  |  |  |  |  |  |  |  |  | 2008-08-02 02:11:51 | Control Panels | Infrastructure Services | Other Control Panel Licensing | Legacy Managed Hosting |

## Usage Notes

<!-- Hand-written: join keys, gotchas, common filters. Preserved on sync. -->
