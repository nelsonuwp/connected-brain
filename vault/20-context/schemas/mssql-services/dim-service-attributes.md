---
type: schema
object: dimServiceAttributes
updated: 2026-03-28
---

# dimServiceAttributes

**Source:** DM_BusinessInsights / dbo
**Description:** More granular attribues of ALL services ever created with attributes such as deprovision_date.

## Columns

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| service_id | int(10) | NO |  |
| client_id | int(10) | NO |  |
| service_status | nvarchar(255) | YES |  |
| is_active | nvarchar(3) | NO |  |
| provision_date | datetime2 | YES |  |
| cancel_date | datetime2 | YES |  |
| deprovision_date | datetime2 | YES |  |
| offline_date | datetime2 | YES |  |
| product | nvarchar(255) | YES |  |
| nickname | nvarchar(64) | YES |  |
| server_name | nvarchar(255) | YES |  |
| OS | nvarchar(255) | YES |  |
| is_pci | nvarchar(3) | NO |  |
| is_magento | nvarchar(3) | NO |  |
| datacenter_name | nvarchar(100) | YES |  |
| datacenter_city | nvarchar(100) | YES |  |
| datacenter_code | nvarchar(15) | YES |  |
| contract_length | int(10) | YES |  |
| contract_months_remaining | int(10) | YES |  |
| service_type | nvarchar(64) | YES |  |
| line_of_business | nvarchar(255) | YES |  |
| last_updated | datetime2 | NO |  |
| fusion_id | int(10) | YES |  |
| adjusted_line_of_business | nvarchar(255) | YES |  |

## Sample Data

| service_id | client_id | service_status | is_active | provision_date | cancel_date | deprovision_date | offline_date | product | nickname | server_name | OS | is_pci | is_magento | datacenter_name | datacenter_city | datacenter_code | contract_length | contract_months_remaining | service_type | line_of_business | last_updated | fusion_id | adjusted_line_of_business |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 282 | 4000268 | Deprovision | No | 2002-07-10 22:43:57.430000 | 2012-01-31 18:55:08.426666 | 2012-02-07 18:57:29.813333 |  | Starter Server | 268-1 | 282 | CentOS | No | No | Vicar | San Antonio | SAT5 | 1 |  | server | Dedicated Hosting | 2026-03-27 07:48:20.276666 | 128 | Hosting |
| 1301 | 4000943 | Deprovision | No | 2002-09-23 14:08:49.460000 | 2011-01-07 11:15:02.950000 | 2011-01-14 11:18:03.550000 |  | Powerline 2200 | 943-1 | 1301 | Debian | No | No | Vicar | San Antonio | SAT5 | 1 |  | server | Dedicated Hosting | 2026-03-27 07:48:20.276666 | 286 | Hosting |
| 2529 | 4001872 | Deprovision | No | 2002-12-18 12:13:27.746666 | 2010-07-13 20:00:38.536666 | 2010-07-20 20:10:40.286666 |  | Starter Server | 1872-1 | 2529 | RedHat 7.3 OS | No | No | Vicar | San Antonio | SAT5 | 1 |  | server | Dedicated Hosting | 2026-03-27 07:48:20.276666 | 128 | Hosting |
| 2942 | 4002109 | Deprovision | No | 2003-01-14 22:21:16.300000 | 2011-12-03 18:55:02.666666 | 2011-12-10 19:05:43.233333 |  | Starter Server | 2109-1 | 2942 | Debian 3.0 Woody | No | No | Vicar | San Antonio | SAT5 | 1 |  | server | Dedicated Hosting | 2026-03-27 07:48:20.276666 | 128 | Hosting |
| 3341 | 4000943 | Deprovision | No | 2003-01-19 00:09:26.816666 | 2011-01-07 11:30:03.616666 | 2011-01-14 11:32:16.996666 |  | Powerline 2200 | 943-3 | 3341 | Debian | No | No | Vicar | San Antonio | SAT5 | 1 |  | server | Dedicated Hosting | 2026-03-27 07:48:20.276666 | 286 | Hosting |

## Usage Notes

<!-- Hand-written: join keys, gotchas, common filters. Preserved on sync. -->
