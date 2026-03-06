---
type: schema
object: ocean_services_renewal_date
updated: 2026-03-06
---

# ocean_services_renewal_date

**Source:** DM_BusinessInsights / renewals
**Description:** Renewal dates and m2m flag per service. Left-join to dimServices on service_id.

## Columns

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| client_id | int(10) | NO |  |
| company_name | nvarchar(255) | YES |  |
| service_id | int(10) | NO |  |
| expiration_date | datetime2 | YES |  |
| m2m | varchar(255) | YES |  |
| cad_budget_mrc | numeric(38,4) | YES |  |
| service_status | nvarchar(255) | YES |  |
| first_term | varchar(3) | NO |  |
| last_updated | datetime | NO |  |

## Sample Data

| client_id | company_name | service_id | expiration_date | m2m | cad_budget_mrc | service_status | first_term | last_updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7008089 | Mosaic Online Systems Ltd | -7008600 | 2025-07-13 04:00:00 | no | 0.0000 | Online | no | 2026-03-05 09:15:52.613000 |
| 7008089 | Mosaic Online Systems Ltd | -7008510 | 2000-01-30 08:12:09 | yes | 389.8455 | Online | no | 2026-03-05 09:15:52.613000 |
| 7008089 | Mosaic Online Systems Ltd | -7008399 | 2025-07-13 04:00:00 | no | 3638.4150 | Online | no | 2026-03-05 09:15:52.613000 |
| 7008089 | Mosaic Online Systems Ltd | -7008298 | 2000-01-30 08:12:09 | yes | 4288.1520 | Online | no | 2026-03-05 09:15:52.613000 |
| 7008089 | Mosaic Online Systems Ltd | -7008198 | 2025-07-13 04:00:00 | no | 4288.1520 | Online | no | 2026-03-05 09:15:52.613000 |

## Usage Notes

<!-- Hand-written: join keys, gotchas, common filters. Preserved on sync. -->
