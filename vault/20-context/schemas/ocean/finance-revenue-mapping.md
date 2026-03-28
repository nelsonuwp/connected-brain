---
type: schema
object: finance_revenue_mapping
updated: 2026-03-28
---

# finance_revenue_mapping

**Source:** FinancialReporting / dbo
**Description:** Revenue line items by client_id and revenue_period. Most queries filter to MAX(revenue_period).

## Columns

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| index_ | bigint(19) | YES |  |
| client_id | int(10) | YES |  |
| revenue_date | int(10) | YES |  |
| service_id | varchar(20) | YES |  |
| ITEMNMBR | varchar(31) | NO |  |
| lnitmseq | int(10) | NO |  |
| product | nvarchar(255) | YES |  |
| xtndprce_period | numeric(38,4) | YES |  |
| xtndprce_period_nx | numeric(38,4) | YES |  |
| lob | nvarchar(255) | YES |  |
| segment | nvarchar(4000) | YES |  |
| datacenter_city | nvarchar(100) | YES |  |
| datacenter_name | nvarchar(100) | YES |  |
| Customer | nvarchar(255) | YES |  |
| GLPOSTDT | datetime | YES |  |
| Location | varchar(99) | YES |  |
| Cost Centre | varchar(99) | YES |  |
| Natural Account | varchar(39) | YES |  |
| Account Description | varchar(181) | YES |  |
| Category | varchar(51) | YES |  |
| DOCNUMBR | varchar(21) | NO |  |
| client_type | nvarchar(64) | YES |  |
| DOCDATE | datetime | YES |  |
| Doc Status | varchar(5) | NO |  |
| gpinstance | varchar(5) | NO |  |
| revenue_period | date | YES |  |

## Sample Data

| index_ | client_id | revenue_date | service_id | ITEMNMBR | lnitmseq | product | xtndprce_period | xtndprce_period_nx | lob | segment | datacenter_city | datacenter_name | Customer | GLPOSTDT | Location | Cost Centre | Natural Account | Account Description | Category | DOCNUMBR | client_type | DOCDATE | Doc Status | gpinstance | revenue_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3909845 | 7013372 | 202512 | 6819483              | C3353                           | 1966080 | Pro Series 5.0 | 32.5294 | 24.2900 | Private Cloud | VMWARE Private Cloud | Portsmouth | Portsmouth | 7013372 Waterstones Booksellers Ltd                                       | 2025-11-07 00:00:00 | 620 Portsmouth | 040 Revenue - MH | 400500 Revenue                         | 90-620-040-400500 Managed Hosting - Portsmouth | Revenue - Managed Hosting | 9124792               | Aptum | 2025-11-01 00:00:00 | Valid | P1UK | 2025-12-01 |
| 3909981 | 7013372 | 202104 | 5378826              | C3772                           | 49152 | Pro E5v3 - M | -49.9948 | -36.1308 | Private Cloud | VMWARE Private Cloud | Portsmouth | Portsmouth | 7013372 Waterstones Booksellers Ltd                                       | 2021-04-30 00:00:00 | 620 Portsmouth | 040 Revenue - MH | 400500 Revenue                         | 90-620-040-400500 Managed Hosting - Portsmouth | Revenue - Managed Hosting | CNE37230              | Aptum | 2021-04-30 00:00:00 | Valid | P1UK | 2021-04-01 |
| 3910165 | 7013372 | 201905 | 5264324              | P887                            | 704512 | Essential E3v5 - M | 236.1797 | 183.8274 | Private Cloud | VMWARE Private Cloud | Portsmouth | Portsmouth | 7013372 Waterstones Booksellers Ltd                                       | 2019-05-03 00:00:00 | 620 Portsmouth | 040 Revenue - MH | 400500 Revenue                         | 90-620-040-400500 Managed Hosting - Portsmouth | Revenue - Managed Hosting | 9094949               | Aptum | 2019-05-01 00:00:00 | Valid | P1UK | 2019-05-01 |
| 3910281 | 7013372 | 202011 | 5244837              | C756                            | 1490944 | Essential E3v5 - M | 20.6993 | 15.6712 | Private Cloud | VMWARE Private Cloud | Portsmouth | Portsmouth | 7013372 Waterstones Booksellers Ltd                                       | 2020-11-03 00:00:00 | 620 Portsmouth | 040 Revenue - MH | 400500 Revenue                         | 90-620-040-400500 Managed Hosting - Portsmouth | Revenue - Managed Hosting | 9103666               | Aptum | 2020-11-01 00:00:00 | Valid | P1UK | 2020-11-01 |
| 3910413 | 7013372 | 201908 | 4487196              | C2943                           | 393216 | Advanced Series 3.0 | 17.1598 | 14.1151 | Private Cloud | VMWARE Private Cloud | Portsmouth | Portsmouth | 7013372 Waterstones Booksellers Ltd                                       | 2019-08-06 00:00:00 | 620 Portsmouth | 040 Revenue - MH | 400500 Revenue                         | 90-620-040-400500 Managed Hosting - Portsmouth | Revenue - Managed Hosting | 9096537               | Aptum | 2019-08-01 00:00:00 | Valid | P1UK | 2019-08-01 |

## Usage Notes

- **service_id is varchar(20) here** — always `CAST(dimServices.service_id AS varchar)` when joining
- Join to dimServices: `ON s.client_id = f.client_id AND CAST(s.service_id AS varchar) = f.service_id`
- Always filter to current period: `WHERE revenue_period = (SELECT MAX(revenue_period) FROM [FinancialReporting].[dbo].[finance_revenue_mapping] WHERE client_id = :client_id)`
- `xtndprce_period_nx` is the **next-period** billed amount — use this for current MRC reporting
- `xtndprce_period` is the current-period billed amount
- `revenue_period` is a date column formatted as first-of-month (e.g. 2025-12-01)
- `Category` is the GL revenue category (e.g. 'Revenue - Managed Hosting')
- Multiple rows per service per period are possible — `SUM(xtndprce_period_nx)` when aggregating
- `gpinstance` identifies the GP instance (P1UK, P1USA, etc.) — useful for multi-region clients
