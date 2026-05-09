---
type: schema-reference
generated: 2026-04-14 07:21
source: live audit via cross-DB from DM_businessinsights
---

# MSSQL Finance — Schema Reference

**Server:** `10.121.21.211`  
**Database:** `FinancialReporting`  
**Access method:** Cross-database queries from `DM_businessinsights` connection  
**Note:** Same server and credentials as DM_BusinessInsights. Queries use `[FinancialReporting].[dbo].[table]` notation.  
**Total tables discovered:** 43  
**Accessible:** 43  
**Denied/Unavailable:** 0  

---

## Contents

- [Priority Tables (AccountIntel)](#priority-tables-accountintel)
- [All Tables](#all-tables)
- [Inaccessible Tables](#inaccessible-tables)

---

## Priority Tables (AccountIntel)

### `[FinancialReporting].[dbo].[ARAgingSnapshot]`

**Status:** ❌ not audited  
**Rows:** —  
**Size:** —  

---

### `[FinancialReporting].[dbo].[BadDebt_Review]`

**Status:** ❌ not audited  
**Rows:** —  
**Size:** —  

---

### `[FinancialReporting].[dbo].[Colo_Churn]`

**Status:** ✅ accessible  
**Rows:** 3,759,782  
**Size:** 2099.1 MB  

| Column | Type | Nullable | PK |
|--------|------|----------|-----|
| `gpinstance` | `varchar(5)` | NO |  |
| `SERVICE_ID` | `char(21)` | YES |  |
| `Customer` | `varchar(81)` | YES |  |
| `Doc Status` | `varchar(5)` | NO |  |
| `Void Date` | `datetime` | NO |  |
| `GLPOSTDT` | `datetime` | NO |  |
| `PeriodStart` | `datetime` | YES |  |
| `PeriodEnd` | `datetime` | YES |  |
| `xtndprce_period` | `numeric(38,6)` | YES |  |
| `xtndprce_period_nx` | `numeric(38,6)` | YES |  |
| `Entity` | `varchar(99)` | YES |  |
| `Location` | `varchar(99)` | YES |  |
| `Cost Centre` | `varchar(99)` | YES |  |
| `Natural Account` | `varchar(39)` | YES |  |
| `Original Posting Accounting` | `varchar(181)` | YES |  |
| `Account Description` | `varchar(181)` | YES |  |
| `Customer Class` | `varchar(15)` | YES |  |
| `Category` | `varchar(51)` | YES |  |
| `Class` | `varchar(21)` | YES |  |
| `ITEMNMBR` | `char(31)` | NO |  |
| `ITEMDESC` | `char(101)` | NO |  |

**Sample rows (3):**

| gpinstance | SERVICE_ID | Customer | Doc Status | Void Date | GLPOSTDT | PeriodStart | PeriodEnd | xtndprce_period | xtndprce_period_nx | Entity | Location | Cost Centre | Natural Account | Original Posting Accounting | Account Description | Customer Class | Category | Class | ITEMNMBR | ITEMDESC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1USA | 2677128               | 4002307 TL Tech Services                                     | Valid | 1900-01-01 00:00:00 | 2013-11-20 00:00:00 | 2013-12-15 00:00:00 | 2013-12-31 00:00:00 | 42.638355 | 42.638355 | 20 Peer 1 Network (USA) Inc. | 330 San Antonio | 030 Revenue - DH | 400500 Revenue                         | 20-330-030-400500 Dedicated Hosting - SAT | 20-330-030-400500 Dedicated Hosting - SAT | SMART | Revenue - Dedicated Hosting | Dedicated Hosting | P265                            | Core 2 Duo E8400                                             |
| P1USA | 2677128               | 4002307 TL Tech Services                                     | Valid | 1900-01-01 00:00:00 | 2013-11-20 00:00:00 | 2014-01-01 00:00:00 | 2014-01-14 00:00:00 | 4.602740 | 4.602740 | 20 Peer 1 Network (USA) Inc. | 330 San Antonio | 030 Revenue - DH | 400500 Revenue                         | 20-330-030-400500 Dedicated Hosting - SAT | 20-330-030-400500 Dedicated Hosting - SAT | SMART | Revenue - Dedicated Hosting | Dedicated Hosting | C41                             | 500 GB 7200 3 Gb/s 3.5 inch SA                               |
| P1USA | 2677128               | 4002307 TL Tech Services                                     | Valid | 1900-01-01 00:00:00 | 2013-11-20 00:00:00 | 2014-01-01 00:00:00 | 2014-01-14 00:00:00 | 4.602740 | 4.602740 | 20 Peer 1 Network (USA) Inc. | 330 San Antonio | 030 Revenue - DH | 400500 Revenue                         | 20-330-030-400500 Dedicated Hosting - SAT | 20-330-030-400500 Dedicated Hosting - SAT | SMART | Revenue - Dedicated Hosting | Dedicated Hosting | C5                              | 100 Mbit Connection                                          |

---

### `[FinancialReporting].[dbo].[CustomerCredits]`

**Status:** ✅ accessible  
**Rows:** 461,622  
**Size:** 278.8 MB  

| Column | Type | Nullable | PK |
|--------|------|----------|-----|
| `CUSTNMBR` | `varchar(15)` | YES |  |
| `Customer Name` | `varchar(81)` | YES |  |
| `Doc number` | `char(21)` | NO |  |
| `Type` | `smallint` | NO |  |
| `Document Date` | `char(10)` | YES |  |
| `RM GLPOST` | `char(10)` | YES |  |
| `VOIDSTTS` | `smallint` | NO |  |
| `Item` | `char(31)` | NO |  |
| `Description` | `char(101)` | NO |  |
| `Orginal Price` | `numeric(19,5)` | YES |  |
| `Extended Price` | `numeric(19,5)` | YES |  |
| `Currency` | `varchar(15)` | YES |  |
| `Start Date` | `char(10)` | YES |  |
| `End Date` | `char(10)` | YES |  |
| `Contract number` | `char(11)` | NO |  |
| `Account` | `varchar(129)` | YES |  |
| `RMVOID` | `char(10)` | YES |  |
| `Natural Account` | `varchar(7)` | YES |  |
| `Voided Month` | `int` | YES |  |
| `Posted Month` | `int` | YES |  |
| `Category` | `varchar(51)` | YES |  |
| `Account Description` | `varchar(181)` | YES |  |
| `Entity` | `varchar(99)` | YES |  |
| `Location` | `varchar(99)` | YES |  |
| `Cost Centre` | `varchar(99)` | YES |  |
| `gl_Natural_Account` | `varchar(39)` | YES |  |
| `Department` | `varchar(21)` | YES |  |
| `Class` | `varchar(21)` | YES |  |
| `EBITDA` | `varchar(31)` | YES |  |
| `Budget Group` | `varchar(31)` | YES |  |
| `Country` | `nvarchar(128)` | YES |  |
| `CMMTTEXT` | `text(2147483647)` | YES |  |
| `PSTUSRID` | `char(15)` | NO |  |

**Sample rows (3):**

| CUSTNMBR | Customer Name | Doc number | Type | Document Date | RM GLPOST | VOIDSTTS | Item | Description | Orginal Price | Extended Price | Currency | Start Date | End Date | Contract number | Account | RMVOID | Natural Account | Voided Month | Posted Month | Category | Account Description | Entity | Location | Cost Centre | gl_Natural_Account | Department | Class | EBITDA | Budget Group | Country | CMMTTEXT | PSTUSRID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7000643 | 7000643 Blackhawk Network (Europe) Ltd.d.b.a BES | CNU086132             | 4 | 08/16/2017 | 08/16/2017 | 0 | MB8                             | System Error                                                 | -3675.84000 | -3675.84000 | Z-US$ | 05/29/2017 | 07/28/2017 |             | 20-240-040-400520 | 01/01/1900 | 400520 | 190001 | 201708 | Revenue - Managed Hosting | 20-240-040-400520 MH Billing Adjustments - Miami | 20 Peer 1 Network (USA) Inc. | 240 Miami | 040 Revenue - MH | 400520 Billing Adjustments             | Revenue | Managed Hosting | Yes | Billing Adjustments | P1USA | Svc. ID #2432879 Request #178436 Credit for billing for inac | ksalonga2       |
| 7000643 | 7000643 Blackhawk Network (Europe) Ltd.d.b.a BES | CNU086132             | 4 | 08/16/2017 | 08/16/2017 | 0 | MB8                             | System Error                                                 | -3675.84000 | -3675.84000 | Z-US$ | 05/29/2017 | 07/28/2017 |             | 20-240-040-400520 | 01/01/1900 | 400520 | 190001 | 201708 | Revenue - Managed Hosting | 20-240-040-400520 MH Billing Adjustments - Miami | 20 Peer 1 Network (USA) Inc. | 240 Miami | 040 Revenue - MH | 400520 Billing Adjustments             | Revenue | Managed Hosting | Yes | Billing Adjustments | P1USA | Svc. ID #2432881 Request #178436 Credit for billing for inac | ksalonga2       |
| 7000643 | 7000643 Blackhawk Network (Europe) Ltd.d.b.a BES | CNU086132             | 4 | 08/16/2017 | 08/16/2017 | 0 | MB8                             | System Error                                                 | -2029.34000 | -2029.34000 | Z-US$ | 05/08/2017 | 07/07/2017 |             | 20-240-040-400520 | 01/01/1900 | 400520 | 190001 | 201708 | Revenue - Managed Hosting | 20-240-040-400520 MH Billing Adjustments - Miami | 20 Peer 1 Network (USA) Inc. | 240 Miami | 040 Revenue - MH | 400520 Billing Adjustments             | Revenue | Managed Hosting | Yes | Billing Adjustments | P1USA | Svc. ID #2065486 Request #178436 Credit for billing for inac | ksalonga2       |

---

### `[FinancialReporting].[dbo].[finance_revenue_mapping]`

**Status:** ✅ accessible  
**Rows:** 4,625,795  
**Size:** 2849.8 MB  

| Column | Type | Nullable | PK |
|--------|------|----------|-----|
| `index_` | `bigint` | YES |  |
| `client_id` | `int` | YES |  |
| `revenue_date` | `int` | YES |  |
| `service_id` | `varchar(20)` | YES |  |
| `ITEMNMBR` | `varchar(31)` | NO |  |
| `lnitmseq` | `int` | NO |  |
| `product` | `nvarchar(255)` | YES |  |
| `xtndprce_period` | `numeric(38,4)` | YES |  |
| `xtndprce_period_nx` | `numeric(38,4)` | YES |  |
| `lob` | `nvarchar(255)` | YES |  |
| `segment` | `nvarchar(4000)` | YES |  |
| `datacenter_city` | `nvarchar(100)` | YES |  |
| `datacenter_name` | `nvarchar(100)` | YES |  |
| `Customer` | `nvarchar(255)` | YES |  |
| `GLPOSTDT` | `datetime` | YES |  |
| `Location` | `varchar(99)` | YES |  |
| `Cost Centre` | `varchar(99)` | YES |  |
| `Natural Account` | `varchar(39)` | YES |  |
| `Account Description` | `varchar(181)` | YES |  |
| `Category` | `varchar(51)` | YES |  |
| `DOCNUMBR` | `varchar(21)` | NO |  |
| `client_type` | `nvarchar(64)` | YES |  |
| `DOCDATE` | `datetime` | YES |  |
| `Doc Status` | `varchar(5)` | NO |  |
| `gpinstance` | `varchar(5)` | NO |  |
| `revenue_period` | `date` | YES |  |

**Sample rows (3):**

| index_ | client_id | revenue_date | service_id | ITEMNMBR | lnitmseq | product | xtndprce_period | xtndprce_period_nx | lob | segment | datacenter_city | datacenter_name | Customer | GLPOSTDT | Location | Cost Centre | Natural Account | Account Description | Category | DOCNUMBR | client_type | DOCDATE | Doc Status | gpinstance | revenue_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4328675 | 7014791 | 202404 | 7730300              | P930                            | 884736 | Juniper SRX 300 | 3.7808 | 3.7808 | Private Cloud | VMWARE Private Cloud | Atlanta | Atlanta | 7014791 Chestnut Health System, Inc.                         | 2024-03-05 00:00:00 | 230 Atlanta | 040 Revenue - MH | 400500 Revenue                         | 20-230-040-400500 Managed Hosting - Atlanta | Revenue - Managed Hosting | 6194001               | Aptum | 2024-03-01 00:00:00 | Valid | P1USA | 2024-04-01 |
| 4328691 | 7014791 | 202407 | 7256344              | C244                            | 3588096 | Juniper SRX 300 | 3.4247 | 3.4247 | Private Cloud | VMWARE Private Cloud | Miami | Miami | 7014791 Chestnut Health System, Inc.                         | 2024-07-03 00:00:00 | 240 Miami | 040 Revenue - MH | 400500 Revenue                         | 20-240-040-400500 Managed Hosting - Miami | Revenue - Managed Hosting | 6197380               | Aptum | 2024-07-01 00:00:00 | Valid | P1USA | 2024-07-01 |
| 4328723 | 7014791 | 202404 | 7730284              | C3353                           | 2031616 | Guest Virtual | 0.8219 | 0.8219 | Private Cloud | VMWARE Private Cloud | Atlanta | Atlanta | 7014791 Chestnut Health System, Inc.                         | 2024-03-05 00:00:00 | 230 Atlanta | 040 Revenue - MH | 400500 Revenue                         | 20-230-040-400500 Managed Hosting - Atlanta | Revenue - Managed Hosting | 6194001               | Aptum | 2024-03-01 00:00:00 | Valid | P1USA | 2024-04-01 |

---

## All Tables

| Schema | Table | Rows | Size | Accessible |
|--------|-------|------|------|------------|
| `dbo` | `CAPEX_cashflow` | 51,391 | 24.6 MB | ✅ |
| `dbo` | `Colo_Churn` ⭐ | 3,759,782 | 2099.1 MB | ✅ |
| `dbo` | `Colo_Churn_ALL` | 1,174,658 | 655.6 MB | ✅ |
| `dbo` | `CustomerCredits` ⭐ | 461,622 | 278.8 MB | ✅ |
| `dbo` | `DateDimension` | 11,688 | 0.9 MB | ✅ |
| `dbo` | `Depreciation_Projections_jq` | 199,296 | 65.1 MB | ✅ |
| `dbo` | `EBITDA` | 362 | 0.0 MB | ✅ |
| `dbo` | `EBITDA20120206` | 358 | 0.0 MB | ✅ |
| `dbo` | `INVCOST` | 2,511 | 0.5 MB | ✅ |
| `dbo` | `IncomeStatement_details_Filtered_Cogeco` | 118,467 | 65.8 MB | ✅ |
| `dbo` | `Invoices` | 20,657,489 | 1098.0 MB | ✅ |
| `dbo` | `MYIS_Games` | 1,167 | 0.3 MB | ✅ |
| `dbo` | `MYIS_Invoices` | 20,078 | 8.2 MB | ✅ |
| `dbo` | `Outages` | 12,465 | 9.3 MB | ✅ |
| `dbo` | `PPE_Continuity_Cogeco_jq` | 40,063 | 10.0 MB | ✅ |
| `dbo` | `PPE_Continuity_jq` | 59,595 | 15.0 MB | ✅ |
| `dbo` | `Profit_Analysis` | 730,484 | 187.1 MB | ✅ |
| `dbo` | `Profit_Analysis_ROA` | 490,427 | 127.0 MB | ✅ |
| `dbo` | `Profit_Cost` | 942,603 | 631.9 MB | ✅ |
| `dbo` | `Profit_HWSWCost_disabled` | 86,983 | 8.3 MB | ✅ |
| `dbo` | `Profit_LicenseCost` | 40,168 | 1.2 MB | ✅ |
| `dbo` | `Profit_OnlineDays` | 942,603 | 491.0 MB | ✅ |
| `dbo` | `SKU_HWSWCost` | 38,183 | 4.3 MB | ✅ |
| `dbo` | `SLA_Credits_jq` | 1,451 | 1.3 MB | ✅ |
| `dbo` | `WaterFall_MRC_Summary_Normalized_disabled` | 417,078 | 103.3 MB | ✅ |
| `dbo` | `WaterFall_Revenue_Summary_Normalized` | 648,895 | 266.4 MB | ✅ |
| `dbo` | `Waterfall_Revenue_Normalized` | 7,744,934 | 4224.5 MB | ✅ |
| `dbo` | `Waterfall_Revenue_Normalized_Invoice` | 2,914,196 | 1323.6 MB | ✅ |
| `dbo` | `Waterfall_Revenue_Normalized_Invoice_Details` | 227,065 | 24.3 MB | ✅ |
| `dbo` | `Waterfall_Revenue_Normalized_NewLOB` | 0 | 0.1 MB | ✅ |
| `dbo` | `atbar_sop30300_deferred_normalized` | 29,338 | 10.4 MB | ✅ |
| `dbo` | `atkir_sop30300_deferred_normalized` | 28,846 | 10.3 MB | ✅ |
| `dbo` | `azure_aptum_invoices` | 55,552 | 2.8 MB | ✅ |
| `dbo` | `colo` | 244,255 | 181.9 MB | ✅ |
| `dbo` | `finance_revenue_mapping` ⭐ | 4,625,795 | 2849.8 MB | ✅ |
| `dbo` | `finance_revenue_mapping2` | 2,150,445 | 1275.6 MB | ✅ |
| `dbo` | `finance_revenue_mapping_networking` | 4,437,284 | 2726.8 MB | ✅ |
| `dbo` | `finance_revenue_mapping_prod` | 4,109,560 | 2502.9 MB | ✅ |
| `dbo` | `nbf_sop30300_deferred_normalized` | 246,638 | 87.8 MB | ✅ |
| `dbo` | `p1cdn_sop30300_deferred_normalized` | 8,202,185 | 2912.9 MB | ✅ |
| `dbo` | `p1uk_sop30300_deferred_normalized` | 5,509,054 | 1956.5 MB | ✅ |
| `dbo` | `p1usa_sop30300_deferred_normalized` | 26,257,146 | 9324.5 MB | ✅ |
| `dbo` | `temp_sop30300_deferred_normalized` | 4,158,315 | 1476.7 MB | ✅ |

---
