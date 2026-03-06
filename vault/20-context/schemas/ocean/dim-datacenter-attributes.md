---
type: schema
object: dimdatacenterattributes
updated: 2026-03-06
---

# dimdatacenterattributes

**Source:** DM_BusinessInsights / dbo
**Description:** Datacenter attribute dimension.

## Columns

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| datacenter_code | nvarchar(255) | YES |  |
| datacenter_city | nvarchar(255) | YES |  |
| datacenter_name | nvarchar(255) | YES |  |
| country | nvarchar(255) | YES |  |
| datacenter_region | nvarchar(255) | YES |  |
| cp1_datacenter_code | nvarchar(255) | YES |  |
| datacenter_nickname | nvarchar(255) | YES |  |
| address | nvarchar(255) | YES |  |
| legacy_entity | nvarchar(255) | YES |  |
| previous_references | nvarchar(255) | YES |  |
| datacenter_status | nvarchar(255) | YES |  |
| datacenter_report_name | nvarchar(255) | YES |  |

## Sample Data

| datacenter_code | datacenter_city | datacenter_name | country | datacenter_region | cp1_datacenter_code | datacenter_nickname | address | legacy_entity | previous_references | datacenter_status | datacenter_report_name |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T3-AU1 | Sydney | Sydney (MCC) | Australia | Canada |  |  |  |  |  | Decommissioned |  |
| AZURE-CAN |  | AZURE-CAN | Canada | Canada |  | Azure Canada |  |  |  | Active | Azure Canada (AZURE-CAN) |
| AZURE-US |  | AZURE-US | United States | US |  | Azure United States |  |  |  | Active | Azure United States (AZURE-US) |
| AZURE-UK |  | AZURE-UK | United Kingdom | EMEA |  | Azure United Kingdom |  |  |  | Active | Azure United Kingdom (AZURE-UK) |
| AZURE-FRN |  | AZURE-FRN | France | EMEA |  | Azure France |  |  |  | Active | Azure France (AZURE-FRN) |

## Usage Notes

- **Primary key:** datacenter_code — join from dimServices or dimComponents on `datacenter_code`
- `datacenter_status = 'Active'` or `'Decommissioned'` — filter to Active for current footprint queries
- `datacenter_region` groups datacenters for regional analysis (Canada, US, EMEA, etc.)
- Includes Azure virtual datacenters (AZURE-CAN, AZURE-US, AZURE-UK, etc.)
- `cp1_datacenter_code` is the legacy Peer 1 code for historical cross-reference
