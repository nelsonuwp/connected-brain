---
type: schema
object: MRCTrend
updated: 2026-03-28
---

# MRCTrend

**Source:** DM_BusinessInsights / dbo
**Description:** Historical snapshot of dimServices which captures dimServices as of a given date (archive_date).

## Columns

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| integer_key | int(10) | NO |  |
| client_id | int(10) | YES |  |
| company_name | nvarchar(255) | YES |  |
| client_created | datetime2 | YES |  |
| service_id | int(10) | YES |  |
| service_name | nvarchar(50) | YES |  |
| service_type | nvarchar(255) | YES |  |
| product | nvarchar(255) | YES |  |
| os | nvarchar(255) | YES |  |
| service_status | nvarchar(255) | YES |  |
| datacenter_code | nvarchar(15) | YES |  |
| datacenter_name | nvarchar(100) | YES |  |
| datacenter_city | nvarchar(100) | YES |  |
| mrc | numeric(38,4) | YES |  |
| sales_rep | nvarchar(255) | YES |  |
| tam | nvarchar(255) | YES |  |
| provision_date | datetime2 | YES |  |
| line_of_business | nvarchar(255) | YES |  |
| currency | nvarchar(3) | YES |  |
| usd_mrc | numeric(38,4) | YES |  |
| cad_mrc | numeric(38,4) | YES |  |
| archive_date | datetime | YES |  |
| cad_budget_mrc | numeric(38,4) | YES |  |
| adjusted_line_of_business | nvarchar(50) | YES |  |

## Sample Data

| integer_key | client_id | company_name | client_created | service_id | service_name | service_type | product | os | service_status | datacenter_code | datacenter_name | datacenter_city | mrc | sales_rep | tam | provision_date | line_of_business | currency | usd_mrc | cad_mrc | archive_date | cad_budget_mrc | adjusted_line_of_business |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4437472 | 4006121 | Diagnostic Systems Associates Inc. | 2003-08-07 16:14:50.906529 | 25143 | 25143 | server | Powerline 2100 | RHEL 3 ES | Online | IAD2 | South Pointe | Herndon | 181.2300 |  |  | 2004-05-12 15:33:56.301640 | Dedicated Hosting | USD | 181.2300 | 235.2089 | 2022-03-31 00:00:00 | 241.0359 | Hosting |
| 4437473 | 4016714 | Dtm Systems, Inc. | 2005-05-20 14:24:45.971385 | 38498 | 38498 | server | Powerline 2100 | Debian 3.0 Stable | Online | IAD2 | South Pointe | Herndon | 129.6600 |  |  | 2005-05-20 19:00:17.912864 | Dedicated Hosting | USD | 129.6600 | 168.2789 | 2022-03-31 00:00:00 | 172.4478 | Hosting |
| 4437474 | 4022044 | NetAlerts Inc. | 2007-03-30 17:18:18.679601 | 61370 | 61370 | server | Powerline 2200 | CentOS | Online | IAD2 | South Pointe | Herndon | 141.6300 |  |  | 2007-03-30 18:40:17.375540 | Dedicated Hosting | USD | 141.6300 | 183.8141 | 2022-03-31 00:00:00 | 188.3679 | Hosting |
| 4437475 | 4024941 | The Rensselaerville Institute | 2008-04-01 15:06:13.451703 | 76442 | 76442 | server | Core 2 Duo E6750 | Fedora 8 64 bit | Online | IAD2 | South Pointe | Herndon | 199.2600 |  |  | 2008-04-02 17:56:04.471645 | Dedicated Hosting | USD | 199.2600 | 258.6091 | 2022-03-31 00:00:00 | 265.0158 | Hosting |
| 4437476 | 4024979 | GlobalMD | 2008-04-07 23:11:53.691192 | 76654 | 76654 | server | Core 2 Duo E6750 | Ded Windows 2003 Standard Edition (per CPU) | Online | IAD2 | South Pointe | Herndon | 231.7400 |  |  | 2008-04-08 22:50:34.541384 | Dedicated Hosting | USD | 231.7400 | 300.7632 | 2022-03-31 00:00:00 | 308.2142 | Hosting |

## Usage Notes

<!-- Hand-written: join keys, gotchas, common filters. Preserved on sync. -->
