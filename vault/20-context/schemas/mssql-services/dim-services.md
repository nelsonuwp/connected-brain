---
type: schema
object: dimServices
updated: 2026-03-28
---

# dimServices

**Source:** DM_BusinessInsights / dbo
**Description:** All active services per client. Join to dimComponents on service_id.

## Columns

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| client_id | int(10) | NO |  |
| company_name | nvarchar(255) | YES |  |
| service_id | int(10) | NO |  |
| nickname | nvarchar(64) | NO |  |
| server_name | nvarchar(255) | YES |  |
| product | nvarchar(255) | YES |  |
| service_status | nvarchar(255) | YES |  |
| os | nvarchar(255) | YES |  |
| currency | nvarchar(3) | NO |  |
| provision_date | datetime2 | YES |  |
| datacenter_name | nvarchar(100) | YES |  |
| datacenter_city | nvarchar(100) | YES |  |
| datacenter_code | nvarchar(15) | YES |  |
| line_of_business | nvarchar(255) | YES |  |
| device_id | nvarchar(64) | YES |  |
| service_type | nvarchar(64) | YES |  |
| mrc | numeric(38,4) | YES |  |
| usd_mrc | numeric(38,4) | YES |  |
| cad_mrc | numeric(38,4) | YES |  |
| contract_length | int(10) | YES |  |
| contract_months_remaining | int(10) | YES |  |
| last_updated | datetime2 | NO |  |
| cad_budget_mrc | numeric(38,4) | YES |  |
| fusion_id | int(10) | YES |  |
| adjusted_line_of_business | nvarchar(255) | YES |  |

## Sample Data

| client_id | company_name | service_id | nickname | server_name | product | service_status | os | currency | provision_date | datacenter_name | datacenter_city | datacenter_code | line_of_business | device_id | service_type | mrc | usd_mrc | cad_mrc | contract_length | contract_months_remaining | last_updated | cad_budget_mrc | fusion_id | adjusted_line_of_business |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7008089 | Mosaic Online Systems Ltd | -7008600 |  |  | B/W-TRAFFIC                     | Online |  | GBP | 1999-01-01 00:00:00 | Croydon | London | CRO | Colocation |  | colocation | 0.0000 | 0.0000 | 0.0000 | -1 | -1 | 2026-03-27 07:48:15.080000 | 0.0000 | 0 | Colocation |
| 7008089 | Mosaic Online Systems Ltd | -7008510 |  |  | CONNECT-CROSS CONNECT           | Online |  | GBP | 1999-01-01 00:00:00 | Croydon | London | CRO | Colocation |  | colocation | 236.2700 | 318.3923 | 389.8455 | -1 | -1 | 2026-03-27 07:48:15.080000 | 389.8455 | 0 | Colocation |
| 7008089 | Mosaic Online Systems Ltd | -7008399 |  |  | B/W-COMMIT                      | Online |  | GBP | 1999-01-01 00:00:00 | Croydon | London | CRO | Colocation |  | colocation | 2205.1000 | 2971.5442 | 3638.4150 | -1 | -1 | 2026-03-27 07:48:15.080000 | 3638.4150 | 0 | Colocation |
| 7008089 | Mosaic Online Systems Ltd | -7008298 |  |  | COLO-FULL                       | Online |  | GBP | 1999-01-01 00:00:00 | Croydon | London | CRO | Colocation |  | colocation | 2598.8800 | 3502.1935 | 4288.1520 | -1 | -1 | 2026-03-27 07:48:15.080000 | 4288.1520 | 0 | Colocation |
| 7008089 | Mosaic Online Systems Ltd | -7008198 |  |  | COLO-FULL                       | Online |  | GBP | 1999-01-01 00:00:00 | Croydon | London | CRO | Colocation |  | colocation | 2598.8800 | 3502.1935 | 4288.1520 | -1 | -1 | 2026-03-27 07:48:15.080000 | 4288.1520 | 0 | Colocation |

## Usage Notes

- **Primary key:** service_id (int)
- **Always filter by client_id** — table contains all clients
- Active services only: `WHERE service_status = 'Online'`
- Join to dimComponents on `service_id` (LEFT JOIN — not all services have components)
- Join to ocean_services_renewal_date on `service_id` (LEFT JOIN — not all services have a renewal row)
- Join to finance_revenue_mapping on `client_id AND CAST(service_id AS varchar) = f.service_id` — type mismatch, CAST required
- Join to dimProductAttributes on `CAST(fusion_id AS nvarchar) = p.fusion_id` — type mismatch, CAST required
- Join to dimdatacenterattributes on `datacenter_code`
- `currency` varies per client (GBP, USD, CAD) — use `cad_mrc` for cross-client comparisons
- `contract_months_remaining = -1` means month-to-month or no fixed term
