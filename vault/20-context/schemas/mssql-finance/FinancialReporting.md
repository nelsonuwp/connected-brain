# Database Report — `FinancialReporting`

> Generated: 2026-03-07 07:24:08  
> Tables: 68  |  Views: 0  |  Procedures: 0  |  Functions: 0  |  Triggers: 0

---

## Table of Contents

**Tables**

- [dbo.ABC_Revenue](#dbo-abc-revenue) — 7,706 rows  `2.6 MB`
- [dbo.atbar_sop30300_deferred_normalized](#dbo-atbar-sop30300-deferred-normalized) — 29,338 rows  `10.4 MB`
- [dbo.atkir_sop30300_deferred_normalized](#dbo-atkir-sop30300-deferred-normalized) — 28,522 rows  `10.2 MB`
- [dbo.azure_aptum_invoices](#dbo-azure-aptum-invoices) — 55,552 rows  `2.8 MB`
- [dbo.BadDebt_Review](#dbo-baddebt-review) — 281,471 rows  `107.7 MB`
- [dbo.Budget_rate](#dbo-budget-rate) — 276 rows  `0.1 MB`
- [dbo.Budget_rate_Cogeco](#dbo-budget-rate-cogeco) — 84 rows  `0.0 MB`
- [dbo.Budget_rate_old](#dbo-budget-rate-old) — 180 rows  `0.0 MB`
- [dbo.Budgetvsactual](#dbo-budgetvsactual) — 189,346 rows  `69.9 MB`
- [dbo.Budgetvsactual_Cogeco](#dbo-budgetvsactual-cogeco) — 170,027 rows  `62.9 MB`
- [dbo.CAPEX](#dbo-capex) — 81,885 rows  `87.5 MB`
- [dbo.CAPEX_cashflow](#dbo-capex-cashflow) — 51,391 rows  `24.6 MB`
- [dbo.CAPEX_Cogeco](#dbo-capex-cogeco) — 81,885 rows  `87.5 MB`
- [dbo.CAPEX_Cogeco1](#dbo-capex-cogeco1) — 46,665 rows  `51.4 MB`
- [dbo.colo](#dbo-colo) — 244,255 rows  `181.9 MB`
- [dbo.Colo_Churn](#dbo-colo-churn) — 3,759,782 rows  `2.0 GB`
- [dbo.Colo_Churn_ALL](#dbo-colo-churn-all) — 1,174,658 rows  `655.6 MB`
- [dbo.CustomerCredits](#dbo-customercredits) — 461,282 rows  `278.6 MB`
- [dbo.DateDimension](#dbo-datedimension) — 11,688 rows  `0.9 MB`
- [dbo.Depreciation_Projections](#dbo-depreciation-projections) — 199,296 rows  `65.1 MB`
- [dbo.EBITDA](#dbo-ebitda) — 362 rows  `0.0 MB`
- [dbo.EBITDA20120206](#dbo-ebitda20120206) — 358 rows  `0.0 MB`
- [dbo.finance_revenue_mapping](#dbo-finance-revenue-mapping) — 4,614,197 rows  `2.8 GB`
- [dbo.finance_revenue_mapping_networking](#dbo-finance-revenue-mapping-networking) — 4,437,284 rows  `2.7 GB`
- [dbo.finance_revenue_mapping_prod](#dbo-finance-revenue-mapping-prod) — 4,109,560 rows  `2.4 GB`
- [dbo.finance_revenue_mapping2](#dbo-finance-revenue-mapping2) — 2,150,445 rows  `1.2 GB`
- [dbo.IncomeStatement_details](#dbo-incomestatement-details) — 2,721,958 rows  `1.5 GB`
- [dbo.IncomeStatement_details_cogeco](#dbo-incomestatement-details-cogeco) — 2,378,459 rows  `1.3 GB`
- [dbo.IncomeStatement_details_Filtered](#dbo-incomestatement-details-filtered) — 240,641 rows  `129.8 MB`
- [dbo.IncomeStatement_details_Filtered_Cogeco](#dbo-incomestatement-details-filtered-cogeco) — 115,183 rows  `63.9 MB`
- [dbo.Intercompany](#dbo-intercompany) — 36,795 rows  `18.3 MB`
- [dbo.INVCOST](#dbo-invcost) — 2,511 rows  `0.5 MB`
- [dbo.Invoices](#dbo-invoices) — 20,641,179 rows  `1.1 GB`
- [dbo.MYIS_Games](#dbo-myis-games) — 1,167 rows  `0.3 MB`
- [dbo.MYIS_Invoices](#dbo-myis-invoices) — 20,078 rows  `8.2 MB`
- [dbo.nbf_sop30300_deferred_normalized](#dbo-nbf-sop30300-deferred-normalized) — 246,455 rows  `87.7 MB`
- [dbo.OPEX](#dbo-opex) — 27,605 rows  `29.4 MB`
- [dbo.OPEX_Cogeco](#dbo-opex-cogeco) — 673,508 rows  `690.6 MB`
- [dbo.Outages](#dbo-outages) — 12,464 rows  `9.3 MB`
- [dbo.p1cdn_sop30300_deferred_normalized](#dbo-p1cdn-sop30300-deferred-normalized) — 8,187,877 rows  `2.8 GB`
- [dbo.p1uk_sop30300_deferred_normalized](#dbo-p1uk-sop30300-deferred-normalized) — 5,502,397 rows  `1.9 GB`
- [dbo.p1usa_sop30300_deferred_normalized](#dbo-p1usa-sop30300-deferred-normalized) — 26,235,739 rows  `9.1 GB`
- [dbo.PPE_Continuity](#dbo-ppe-continuity) — 59,595 rows  `15.0 MB`
- [dbo.PPE_Continuity_Cogeco](#dbo-ppe-continuity-cogeco) — 40,063 rows  `10.1 MB`
- [dbo.Profit_Analysis](#dbo-profit-analysis) — 730,484 rows  `187.1 MB`
- [dbo.Profit_Analysis_ROA](#dbo-profit-analysis-roa) — 490,427 rows  `127.0 MB`
- [dbo.Profit_Cost](#dbo-profit-cost) — 942,603 rows  `631.9 MB`
- [dbo.Profit_HWSWCost_disabled](#dbo-profit-hwswcost-disabled) — 86,983 rows  `8.3 MB`
- [dbo.Profit_LicenseCost](#dbo-profit-licensecost) — 40,168 rows  `1.2 MB`
- [dbo.Profit_OnlineDays](#dbo-profit-onlinedays) — 942,603 rows  `491.0 MB`
- [dbo.SKU_HWSWCost](#dbo-sku-hwswcost) — 38,183 rows  `4.3 MB`
- [dbo.SLA_Credits](#dbo-sla-credits) — 1,450 rows  `1.3 MB`
- [dbo.temp_sop30300_deferred_normalized](#dbo-temp-sop30300-deferred-normalized) — 4,158,315 rows  `1.4 GB`
- [dbo.WaterFall_MRC_Summary_Normalized_disabled](#dbo-waterfall-mrc-summary-normalized-disabled) — 417,078 rows  `103.3 MB`
- [dbo.Waterfall_Normalized_disabled](#dbo-waterfall-normalized-disabled) — 1,169,760 rows  `408.0 MB`
- [dbo.Waterfall_Normalized_old](#dbo-waterfall-normalized-old) — 1,712,292 rows  `658.2 MB`
- [dbo.Waterfall_Normalized_removed_2025-09-10_JQ](#dbo-waterfall-normalized-removed-2025-09-10-jq) — 1,692,347 rows  `648.3 MB`
- [dbo.Waterfall_Revenue_Normalized](#dbo-waterfall-revenue-normalized) — 7,721,416 rows  `4.1 GB`
- [dbo.Waterfall_Revenue_Normalized_Compressed](#dbo-waterfall-revenue-normalized-compressed) — 60,049 rows  `18.4 MB`
- [dbo.Waterfall_Revenue_Normalized_Invoice](#dbo-waterfall-revenue-normalized-invoice) — 2,914,196 rows  `1.3 GB`
- [dbo.Waterfall_Revenue_Normalized_Invoice_Details](#dbo-waterfall-revenue-normalized-invoice-details) — 227,065 rows  `24.3 MB`
- [dbo.Waterfall_Revenue_Normalized_NewLOB](#dbo-waterfall-revenue-normalized-newlob) — 0 rows  `0.1 MB`
- [dbo.WaterFall_Revenue_Summary_Normalized](#dbo-waterfall-revenue-summary-normalized) — 646,814 rows  `265.5 MB`
- [dbo.zunicore_credits](#dbo-zunicore-credits) — 11,753 rows  `2.5 MB`
- [dbo.zunicore_credits_deferred_normalized](#dbo-zunicore-credits-deferred-normalized) — 12,609 rows  `3.5 MB`
- [dbo.zunicore_invoices](#dbo-zunicore-invoices) — 115,936 rows  `26.5 MB`
- [dbo.zunicore_invoices_deferred_normalized](#dbo-zunicore-invoices-deferred-normalized) — 226,411 rows  `62.0 MB`
- [dbo.zunicore_revenue](#dbo-zunicore-revenue) — 247,092 rows  `17.4 MB`

**Views**


**Stored Procedures**


**Functions**


---

## Tables

### dbo.ABC_Revenue {#dbo-abc-revenue}

| Property | Value |
|---|---|
| Full name | `[dbo].[ABC_Revenue]` |
| Row count | 7,706 |
| Total size | 2.6 MB |
| Used size | 2.4 MB |
| Created | 2026-03-06 09:14 |
| Schema modified | 2026-03-06 09:14 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column              | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min             | Max            |
|---------------------|---------------|------------|------------|-----------|---------------|---------|------------|-----------------|----------------|
| Country             | varchar(5)    | NO         |            |           |               | 0%      |          6 | —               | —              |
| Budget ID           | varchar(2)    | NO         |            |           |               | 0%      |          1 | —               | —              |
| EBITDA              | varchar(31)   | YES        |            |           |               | 0%      |          2 | —               | —              |
| Category            | varchar(51)   | YES        |            |           |               | 0%      |          6 | —               | —              |
| Account Description | varchar(181)  | YES        |            |           |               | 0%      |        381 | —               | —              |
| Entity              | varchar(99)   | YES        |            |           |               | 0%      |          6 | —               | —              |
| Location            | varchar(99)   | YES        |            |           |               | 0%      |         29 | —               | —              |
| Cost Centre         | varchar(99)   | YES        |            |           |               | 0%      |         16 | —               | —              |
| Natural Account     | varchar(39)   | YES        |            |           |               | 0%      |         10 | —               | —              |
| Budget Group        | varchar(31)   | YES        |            |           |               | 0%      |         18 | —               | —              |
| Department          | varchar(21)   | YES        |            |           |               | 0%      |          2 | —               | —              |
| Class               | varchar(21)   | YES        |            |           |               | 0%      |         10 | —               | —              |
| CLass Modified      | varchar(21)   | YES        |            |           |               | 0%      |          9 | —               | —              |
| Functional Amount   | numeric(38,5) | YES        |            |           |               | 0%      |       6795 | -2168478.94000  | 2758333.88000  |
| USD Amount          | numeric(38,6) | YES        |            |           |               | 0%      |       7165 | -1787964.447460 | 2073779.404284 |
| Currency ID         | varchar(15)   | YES        |            |           |               | 0%      |          4 | —               | —              |
| FiscalYear          | smallint      | YES        |            |           |               | 0%      |          4 | 2019            | 2022           |
| FiscalQuarter       | varchar(2)    | YES        |            |           |               | 0%      |          4 | —               | —              |
| FiscalPeriod        | smallint      | YES        |            |           |               | 0%      |         12 | 1               | 12             |
| Batch Source        | varchar(15)   | YES        |            |           |               | 99%     |          1 | —               | —              |

---

### dbo.atbar_sop30300_deferred_normalized {#dbo-atbar-sop30300-deferred-normalized}

| Property | Value |
|---|---|
| Full name | `[dbo].[atbar_sop30300_deferred_normalized]` |
| Row count | 29,338 |
| Total size | 10.4 MB |
| Used size | 10.4 MB |
| Created | 2026-03-07 04:43 |
| Schema modified | 2026-03-07 04:43 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column          | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| soptype         | smallint      | NO         |            |           |               | 0%      |          2 | 3                   | 4                   |
| sopnumbe        | char(21)      | NO         |            |           |               | 0%      |       1405 | —                   | —                   |
| lnitmseq        | int           | NO         |            |           |               | 0%      |        224 | 8192                | 3653632             |
| cmpntseq        | int           | NO         |            |           |               | 0%      |          1 | 0                   | 0                   |
| xtndprce        | numeric(19,5) | NO         |            |           |               | 0%      |        997 | 0.00000             | 1315262.70000       |
| oxtndprc        | numeric(19,5) | NO         |            |           |               | 0%      |        958 | 0.00000             | 1315262.70000       |
| remprice        | numeric(19,5) | NO         |            |           |               | 0%      |        997 | 0.00000             | 1315262.70000       |
| oreprice        | numeric(19,5) | NO         |            |           |               | 0%      |        958 | 0.00000             | 1315262.70000       |
| extdcost        | numeric(19,5) | NO         |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| orextcst        | numeric(19,5) | NO         |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| mrkdnamt        | numeric(19,5) | NO         |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| ormrkdam        | numeric(19,5) | NO         |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| mrkdnpct        | smallint      | NO         |            |           |               | 0%      |          1 | 0                   | 0                   |
| mrkdntyp        | smallint      | NO         |            |           |               | 0%      |          1 | 0                   | 0                   |
| taxamnt         | numeric(19,5) | NO         |            |           |               | 0%      |        966 | 0.00000             | 170984.15000        |
| ortaxamt        | numeric(19,5) | NO         |            |           |               | 0%      |        932 | 0.00000             | 170984.15000        |
| contstartdte    | datetime      | NO         |            |           |               | 0%      |        165 | 1900-01-01 00:00:00 | 2025-02-28 00:00:00 |
| contenddte      | datetime      | NO         |            |           |               | 0%      |        139 | 1900-01-01 00:00:00 | 2026-07-31 00:00:00 |
| totaldays       | numeric(24,6) | YES        |            |           |               | 0%      |         66 | 1.000000            | 1826.000000         |
| PeriodStart     | datetime      | YES        |            |           |               | 0%      |        199 | 1900-01-01 00:00:00 | 2026-07-01 00:00:00 |
| PeriodEnd       | datetime      | YES        |            |           |               | 0%      |        167 | 1900-01-01 00:00:00 | 2026-07-31 00:00:00 |
| PeriodDays      | numeric(26,6) | YES        |            |           |               | 0%      |         31 | 1.000000            | 31.000000           |
| xtndprce_period | numeric(38,6) | YES        |            |           |               | 0%      |       1411 | 0.000000            | 1315262.700000      |
| oxtndprc_period | numeric(38,6) | YES        |            |           |               | 0%      |       1350 | 0.000000            | 1315262.700000      |
| remprice_period | numeric(38,6) | YES        |            |           |               | 0%      |       1411 | 0.000000            | 1315262.700000      |
| oreprice_period | numeric(38,6) | YES        |            |           |               | 0%      |       1350 | 0.000000            | 1315262.700000      |
| extdcost_period | numeric(38,6) | YES        |            |           |               | 0%      |          1 | 0.000000            | 0.000000            |
| orextcst_period | numeric(38,6) | YES        |            |           |               | 0%      |          1 | 0.000000            | 0.000000            |
| mrkdnamt_period | numeric(38,6) | YES        |            |           |               | 0%      |          1 | 0.000000            | 0.000000            |
| ormrkdam_period | numeric(38,6) | YES        |            |           |               | 0%      |          1 | 0.000000            | 0.000000            |
| taxamnt_period  | numeric(38,6) | YES        |            |           |               | 0%      |       1378 | 0.000000            | 170984.150000       |
| ortaxamt_period | numeric(38,6) | YES        |            |           |               | 0%      |       1333 | 0.000000            | 170984.150000       |

---

### dbo.atkir_sop30300_deferred_normalized {#dbo-atkir-sop30300-deferred-normalized}

| Property | Value |
|---|---|
| Full name | `[dbo].[atkir_sop30300_deferred_normalized]` |
| Row count | 28,522 |
| Total size | 10.2 MB |
| Used size | 10.1 MB |
| Created | 2026-03-07 04:43 |
| Schema modified | 2026-03-07 04:43 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column          | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| soptype         | smallint      | NO         |            |           |               | 0%      |          2 | 3                   | 4                   |
| sopnumbe        | char(21)      | NO         |            |           |               | 0%      |       1822 | —                   | —                   |
| lnitmseq        | int           | NO         |            |           |               | 0%      |        151 | 16384               | 2473984             |
| cmpntseq        | int           | NO         |            |           |               | 0%      |          1 | 0                   | 0                   |
| xtndprce        | numeric(19,5) | NO         |            |           |               | 0%      |       1422 | -23247.04000        | 5000000.00000       |
| oxtndprc        | numeric(19,5) | NO         |            |           |               | 0%      |       1115 | -23247.04000        | 5000000.00000       |
| remprice        | numeric(19,5) | NO         |            |           |               | 0%      |       1421 | -23247.04000        | 5000000.00000       |
| oreprice        | numeric(19,5) | NO         |            |           |               | 0%      |       1088 | -23247.04000        | 5000000.00000       |
| extdcost        | numeric(19,5) | NO         |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| orextcst        | numeric(19,5) | NO         |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| mrkdnamt        | numeric(19,5) | NO         |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| ormrkdam        | numeric(19,5) | NO         |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| mrkdnpct        | smallint      | NO         |            |           |               | 0%      |          1 | 0                   | 0                   |
| mrkdntyp        | smallint      | NO         |            |           |               | 0%      |          1 | 0                   | 0                   |
| taxamnt         | numeric(19,5) | NO         |            |           |               | 0%      |        844 | -3481.24000         | 748750.00000        |
| ortaxamt        | numeric(19,5) | NO         |            |           |               | 0%      |        784 | -3481.24000         | 748750.00000        |
| contstartdte    | datetime      | NO         |            |           |               | 0%      |        170 | 1900-01-01 00:00:00 | 2026-03-01 00:00:00 |
| contenddte      | datetime      | NO         |            |           |               | 0%      |        157 | 1900-01-01 00:00:00 | 2029-06-30 00:00:00 |
| totaldays       | numeric(24,6) | YES        |            |           |               | 0%      |         58 | 1.000000            | 3103.000000         |
| PeriodStart     | datetime      | YES        |            |           |               | 0%      |        208 | 1900-01-01 00:00:00 | 2029-05-01 00:00:00 |
| PeriodEnd       | datetime      | YES        |            |           |               | 0%      |        192 | 1900-01-01 00:00:00 | 2029-05-31 00:00:00 |
| PeriodDays      | numeric(26,6) | YES        |            |           |               | 0%      |         23 | 1.000000            | 31.000000           |
| xtndprce_period | numeric(38,6) | YES        |            |           |               | 0%      |       1580 | -23247.040000       | 5000000.000000      |
| oxtndprc_period | numeric(38,6) | YES        |            |           |               | 0%      |       1277 | -23247.040000       | 5000000.000000      |
| remprice_period | numeric(38,6) | YES        |            |           |               | 0%      |       1579 | -23247.040000       | 5000000.000000      |
| oreprice_period | numeric(38,6) | YES        |            |           |               | 0%      |       1250 | -23247.040000       | 5000000.000000      |
| extdcost_period | numeric(38,6) | YES        |            |           |               | 0%      |          1 | 0.000000            | 0.000000            |
| orextcst_period | numeric(38,6) | YES        |            |           |               | 0%      |          1 | 0.000000            | 0.000000            |
| mrkdnamt_period | numeric(38,6) | YES        |            |           |               | 0%      |          1 | 0.000000            | 0.000000            |
| ormrkdam_period | numeric(38,6) | YES        |            |           |               | 0%      |          1 | 0.000000            | 0.000000            |
| taxamnt_period  | numeric(38,6) | YES        |            |           |               | 0%      |        971 | -3481.240000        | 748750.000000       |
| ortaxamt_period | numeric(38,6) | YES        |            |           |               | 0%      |        911 | -3481.240000        | 748750.000000       |

---

### dbo.azure_aptum_invoices {#dbo-azure-aptum-invoices}

| Property | Value |
|---|---|
| Full name | `[dbo].[azure_aptum_invoices]` |
| Row count | 55,552 |
| Total size | 2.8 MB |
| Used size | 2.8 MB |
| Created | 2026-02-23 15:28 |
| Schema modified | 2026-02-23 15:28 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column        | Type     | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max   |
|---------------|----------|------------|------------|-----------|---------------|---------|------------|-------|-------|
| aptum_invoice | char(21) | NO         |            |           |               | 0%      |      55512 | —     | —     |
| gp_invoice    | char(21) | NO         |            |           |               | 0%      |      16448 | —     | —     |

---

### dbo.BadDebt_Review {#dbo-baddebt-review}

| Property | Value |
|---|---|
| Full name | `[dbo].[BadDebt_Review]` |
| Row count | 281,471 |
| Total size | 107.7 MB |
| Used size | 107.6 MB |
| Created | 2026-03-06 08:02 |
| Schema modified | 2026-03-06 08:02 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                          | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|---------------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| Country                         | varchar(6)    | NO         |            |           |               | 0%      |          4 | —                   | —                   |
| Customer Number                 | varchar(15)   | YES        |            |           |               | 0%      |      47036 | —                   | —                   |
| Customer Name                   | varchar(65)   | YES        |            |           |               | 0%      |      46884 | —                   | —                   |
| Current                         | numeric(19,5) | YES        |            |           |               | 0%      |        789 | 0.00000             | 651997.28000        |
| 0-30 Days                       | numeric(19,5) | YES        |            |           |               | 0%      |        292 | -31897.96000        | 713710.01000        |
| 31-60 Days                      | numeric(19,5) | YES        |            |           |               | 0%      |        170 | -31675.33000        | 19331.77000         |
| 61-90 Days                      | numeric(19,5) | YES        |            |           |               | 0%      |        121 | -8293.09000         | 19393.47000         |
| 90+ Days                        | numeric(19,5) | YES        |            |           |               | 0%      |        264 | -45081.58000        | 148671.91000        |
| Average Days To Pay - Life      | smallint      | YES        |            |           |               | 0%      |        507 | 0                   | 1611                |
| Average Days To Pay - Year      | smallint      | YES        |            |           |               | 0%      |        111 | 0                   | 2192                |
| Average Days to Pay - LYR       | smallint      | YES        |            |           |               | 0%      |        158 | 0                   | 533                 |
| Currency ID                     | varchar(15)   | YES        |            |           |               | 0%      |          5 | —                   | —                   |
| Customer Balance                | numeric(19,5) | YES        |            |           |               | 0%      |        908 | -25764.00000        | 1320625.71000       |
| Customer Class                  | varchar(15)   | YES        |            |           |               | 0%      |         13 | —                   | —                   |
| First Invoice Date              | datetime      | NO         |            |           |               | 0%      |          1 | 1900-01-01 00:00:00 | 1900-01-01 00:00:00 |
| High Balance LTD                | numeric(19,5) | YES        |            |           |               | 0%      |      16940 | 0.00000             | 753484009387.93000  |
| High Balance LYR                | numeric(19,5) | YES        |            |           |               | 0%      |       1074 | 0.00000             | 2189590.48000       |
| High Balance YTD                | numeric(19,5) | YES        |            |           |               | 0%      |        910 | 0.00000             | 4022858.65000       |
| Hold                            | varchar(100)  | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| Inactive                        | varchar(100)  | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| Last Payment Amount             | numeric(19,5) | YES        |            |           |               | 0%      |      13247 | -672.00000          | 4022858.65000       |
| Last Payment Date               | datetime      | YES        |            |           |               | 0%      |       5035 | 1900-01-01 00:00:00 | 2026-03-04 00:00:00 |
| Payment Terms ID                | varchar(21)   | YES        |            |           |               | 0%      |         10 | —                   | —                   |
| Total # Invoices LTD            | int           | YES        |            |           |               | 0%      |        614 | 0                   | 2306                |
| Total # Invoices LYR            | int           | YES        |            |           |               | 0%      |         53 | 0                   | 74                  |
| Total # Invoices YTD            | int           | YES        |            |           |               | 0%      |         36 | 0                   | 42                  |
| Total Amount Of NSF Checks Life | numeric(19,5) | YES        |            |           |               | 0%      |        120 | 0.00000             | 54509.49000         |
| Total Amount Of NSF Checks YTD  | numeric(19,5) | YES        |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| Total Bad Deb LYR               | numeric(19,5) | YES        |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| Total Bad Debt LTD              | numeric(19,5) | YES        |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| Total Bad Debt YTD              | numeric(19,5) | YES        |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| Total Cash Received LTD         | numeric(19,5) | YES        |            |           |               | 0%      |      19802 | 0.00000             | 120141217.36000     |
| Total Cash Received LYR         | numeric(19,5) | YES        |            |           |               | 0%      |       1029 | 0.00000             | 7630002.99000       |
| Total Cash Received YTD         | numeric(19,5) | YES        |            |           |               | 0%      |        867 | -1643.07000         | 4022858.65000       |
| Total Returns LTD               | numeric(19,5) | YES        |            |           |               | 0%      |      18628 | 0.00000             | 3562576.98000       |
| Total Returns LYR               | numeric(19,5) | YES        |            |           |               | 0%      |        291 | 0.00000             | 278726.88000        |
| Total Returns YTD               | numeric(19,5) | YES        |            |           |               | 0%      |        347 | 0.00000             | 119435.25000        |
| Total Sales LTD                 | numeric(19,5) | YES        |            |           |               | 0%      |      21571 | -2350.14000         | 121174375.55000     |
| Total Sales LYR                 | numeric(19,5) | YES        |            |           |               | 0%      |       1105 | -9502.30000         | 7323346.02000       |
| Total Sales YTD                 | numeric(19,5) | YES        |            |           |               | 0%      |       1054 | -92736.83000        | 4315272.52000       |
| Unposted Cash Amount            | numeric(19,5) | YES        |            |           |               | 0%      |        244 | -629.02000          | 169008.86000        |
| Unposted Other Cash Amount      | numeric(19,5) | YES        |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| Unposted Other Sales Amount     | numeric(19,5) | YES        |            |           |               | 0%      |        114 | -32535.46000        | 398841.47000        |
| Unposted Sales Amount           | numeric(19,5) | YES        |            |           |               | 0%      |          2 | 0.00000             | 0.01000             |
| User Defined 1                  | varchar(21)   | YES        |            |           |               | 0%      |       1176 | —                   | —                   |
| User Defined 2                  | varchar(21)   | YES        |            |           |               | 0%      |        497 | —                   | —                   |
| Write Offs LIFE                 | numeric(19,5) | YES        |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| Write Offs LYR                  | numeric(19,5) | YES        |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| Write Offs YTD                  | numeric(19,5) | YES        |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |

---

### dbo.Budget_rate {#dbo-budget-rate}

| Property | Value |
|---|---|
| Full name | `[dbo].[Budget_rate]` |
| Row count | 276 |
| Total size | 0.1 MB |
| Used size | 0.1 MB |
| Created | 2010-12-29 18:49 |
| Schema modified | 2010-12-29 18:49 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min       | Max       |
|-------------|---------------|------------|------------|-----------|---------------|---------|------------|-----------|-----------|
| Country     | nchar(10)     | NO         |            |           |               | 0%      |          7 | —         | —         |
| BUDGETID    | char(15)      | NO         |            |           |               | 0%      |         22 | —         | —         |
| Fiscal Year | smallint      | NO         |            |           |               | 0%      |          5 | 2010      | 2014      |
| Period      | smallint      | NO         |            |           |               | 0%      |         14 | 1         | 14        |
| PL_Rate     | numeric(19,7) | NO         |            |           |               | 0%      |         11 | 0.8000000 | 1.6400000 |
| BS_Rate     | numeric(19,7) | NO         |            |           |               | 0%      |          1 | 0E-7      | 0E-7      |

#### Indexes

| Name           | Type      | Unique   | PK   | Columns                                |
|----------------|-----------|----------|------|----------------------------------------|
| PK_Budget_rate | CLUSTERED | YES      | ✓    | Country, BUDGETID, Fiscal Year, Period |

---

### dbo.Budget_rate_Cogeco {#dbo-budget-rate-cogeco}

| Property | Value |
|---|---|
| Full name | `[dbo].[Budget_rate_Cogeco]` |
| Row count | 84 |
| Total size | 0.0 MB |
| Used size | 0.0 MB |
| Created | 2013-02-27 17:41 |
| Schema modified | 2013-02-27 18:19 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min       | Max       |
|-------------|---------------|------------|------------|-----------|---------------|---------|------------|-----------|-----------|
| Country     | nchar(10)     | NO         |            |           |               | 0%      |          7 | —         | —         |
| BUDGETID    | char(15)      | NO         |            |           |               | 0%      |          7 | —         | —         |
| Fiscal Year | smallint      | NO         |            |           |               | 0%      |          2 | 2013      | 2014      |
| Period      | smallint      | NO         |            |           |               | 0%      |         12 | 1         | 12        |
| PL_Rate     | numeric(19,7) | NO         |            |           |               | 0%      |          6 | 1.0000000 | 1.5816330 |
| BS_Rate     | numeric(19,7) | NO         |            |           |               | 0%      |          1 | 0E-7      | 0E-7      |

---

### dbo.Budget_rate_old {#dbo-budget-rate-old}

| Property | Value |
|---|---|
| Full name | `[dbo].[Budget_rate_old]` |
| Row count | 180 |
| Total size | 0.0 MB |
| Used size | 0.0 MB |
| Created | 2012-08-10 13:10 |
| Schema modified | 2012-08-10 13:10 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min       | Max       |
|-------------|---------------|------------|------------|-----------|---------------|---------|------------|-----------|-----------|
| Country     | nchar(10)     | NO         |            |           |               | 0%      |          3 | —         | —         |
| BUDGETID    | char(15)      | NO         |            |           |               | 0%      |         15 | —         | —         |
| Fiscal Year | smallint      | NO         |            |           |               | 0%      |          3 | 2010      | 2012      |
| Period      | smallint      | NO         |            |           |               | 0%      |         12 | 1         | 12        |
| PL_Rate     | numeric(19,7) | NO         |            |           |               | 0%      |          6 | 0.8000000 | 1.6400000 |
| BS_Rate     | numeric(19,7) | NO         |            |           |               | 0%      |          1 | 0E-7      | 0E-7      |

---

### dbo.Budgetvsactual {#dbo-budgetvsactual}

| Property | Value |
|---|---|
| Full name | `[dbo].[Budgetvsactual]` |
| Row count | 189,346 |
| Total size | 69.9 MB |
| Used size | 69.9 MB |
| Created | 2026-03-06 08:02 |
| Schema modified | 2026-03-06 08:02 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column              | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min              | Max             |
|---------------------|---------------|------------|------------|-----------|---------------|---------|------------|------------------|-----------------|
| Country             | varchar(5)    | NO         |            |           |               | 0%      |          7 | —                | —               |
| Year                | smallint      | YES        |            |           |               | 0%      |         21 | 2006             | 2026            |
| Period ID           | smallint      | NO         |            |           |               | 0%      |         14 | 1                | 14              |
| Fiscal Period       | int           | YES        |            |           |               | 0%      |        237 | 200612           | 202606          |
| Quarter             | varchar(2)    | NO         |            |           |               | 0%      |          4 | —                | —               |
| Source              | varchar(6)    | NO         |            |           |               | 0%      |          2 | —                | —               |
| Budget ID           | varchar(15)   | NO         |            |           |               | 0%      |         27 | —                | —               |
| FC Variance         | numeric(19,5) | YES        |            |           |               | 0%      |     111661 | -32464000.00000  | 8365585.17000   |
| RC Variance         | numeric(38,6) | YES        |            |           |               | 0%      |     130401 | -24876056.177600 | 7703166.676339  |
| Filter              | varchar(12)   | YES        |            |           |               | 0%      |        309 | —                | —               |
| EBITDA              | varchar(31)   | YES        |            |           |               | 0%      |          4 | —                | —               |
| FC Period Balance   | numeric(19,5) | NO         |            |           |               | 0%      |     111083 | -8365585.17000   | 32464000.00000  |
| RC Period Balance   | numeric(38,6) | YES        |            |           |               | 0%      |     130059 | -7703166.676339  | 24876056.177600 |
| Category            | varchar(51)   | YES        |            |           |               | 0%      |         39 | —                | —               |
| Account Description | varchar(181)  | YES        |            |           |               | 0%      |       5755 | —                | —               |
| Entity              | varchar(99)   | YES        |            |           |               | 0%      |         17 | —                | —               |
| Location            | varchar(99)   | YES        |            |           |               | 0%      |         39 | —                | —               |
| Cost Centre         | varchar(99)   | YES        |            |           |               | 0%      |        113 | —                | —               |
| Natural Account     | varchar(39)   | YES        |            |           |               | 0%      |        241 | —                | —               |
| Budget Group        | varchar(31)   | YES        |            |           |               | 0%      |        163 | —                | —               |
| Department          | varchar(21)   | YES        |            |           |               | 0%      |         45 | —                | —               |
| Class               | varchar(21)   | YES        |            |           |               | 0%      |         28 | —                | —               |
| Posting Type        | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                | —               |
| Account Type        | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                | —               |
| ACTIVE              | tinyint       | NO         |            |           |               | 0%      |          2 | 0                | 1               |

---

### dbo.Budgetvsactual_Cogeco {#dbo-budgetvsactual-cogeco}

| Property | Value |
|---|---|
| Full name | `[dbo].[Budgetvsactual_Cogeco]` |
| Row count | 170,027 |
| Total size | 62.9 MB |
| Used size | 62.8 MB |
| Created | 2026-03-06 08:02 |
| Schema modified | 2026-03-06 08:02 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column              | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min              | Max             |
|---------------------|---------------|------------|------------|-----------|---------------|---------|------------|------------------|-----------------|
| Country             | varchar(5)    | NO         |            |           |               | 0%      |          5 | —                | —               |
| Year                | smallint      | YES        |            |           |               | 0%      |         20 | 2007             | 2026            |
| Period ID           | smallint      | NO         |            |           |               | 0%      |         14 | 1                | 14              |
| Fiscal Period       | int           | YES        |            |           |               | 0%      |        236 | 200701           | 202606          |
| Quarter             | varchar(2)    | NO         |            |           |               | 0%      |          4 | —                | —               |
| Source              | varchar(6)    | NO         |            |           |               | 0%      |          2 | —                | —               |
| Budget ID           | varchar(15)   | NO         |            |           |               | 0%      |         27 | —                | —               |
| FC Variance         | numeric(19,5) | YES        |            |           |               | 0%      |      99545 | -32464000.00000  | 8365585.17000   |
| RC Variance         | numeric(38,6) | YES        |            |           |               | 14%     |     119059 | -32464000.000000 | 8365585.170000  |
| Filter              | varchar(12)   | YES        |            |           |               | 0%      |        308 | —                | —               |
| EBITDA              | varchar(31)   | YES        |            |           |               | 0%      |          4 | —                | —               |
| FC Period Balance   | numeric(19,5) | NO         |            |           |               | 0%      |      98992 | -8365585.17000   | 32464000.00000  |
| RC Period Balance   | numeric(38,6) | YES        |            |           |               | 14%     |     118872 | -8365585.170000  | 32464000.000000 |
| Category            | varchar(51)   | YES        |            |           |               | 0%      |         36 | —                | —               |
| Account Description | varchar(181)  | YES        |            |           |               | 0%      |       5564 | —                | —               |
| Entity              | varchar(99)   | YES        |            |           |               | 0%      |         15 | —                | —               |
| Location            | varchar(99)   | YES        |            |           |               | 0%      |         36 | —                | —               |
| Cost Centre         | varchar(99)   | YES        |            |           |               | 0%      |        109 | —                | —               |
| Natural Account     | varchar(39)   | YES        |            |           |               | 0%      |        237 | —                | —               |
| Budget Group        | varchar(31)   | YES        |            |           |               | 0%      |        156 | —                | —               |
| Department          | varchar(21)   | YES        |            |           |               | 0%      |         45 | —                | —               |
| Class               | varchar(21)   | YES        |            |           |               | 0%      |         24 | —                | —               |
| Posting Type        | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                | —               |
| Account Type        | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                | —               |
| ACTIVE              | tinyint       | NO         |            |           |               | 0%      |          2 | 0                | 1               |

---

### dbo.CAPEX {#dbo-capex}

| Property | Value |
|---|---|
| Full name | `[dbo].[CAPEX]` |
| Row count | 81,885 |
| Total size | 87.5 MB |
| Used size | 87.5 MB |
| Created | 2026-03-06 09:20 |
| Schema modified | 2026-03-06 09:20 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| Country                     | varchar(5)    | NO         |            |           |               | 0%      |          4 | —                   | —                   |
| Budget ID                   | varchar(2)    | NO         |            |           |               | 0%      |          1 | —                   | —                   |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |         48 | —                   | —                   |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |          7 | —                   | —                   |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |         10 | —                   | —                   |
| Journal Entry               | int           | NO         |            |           |               | 0%      |      52917 | 0                   | 2670029             |
| Series                      | varchar(100)  | YES        |            |           |               | 0%      |          5 | —                   | —                   |
| TRX Date                    | datetime      | YES        |            |           |               | 0%      |       2591 | 2008-01-10 00:00:00 | 2025-08-31 00:00:00 |
| Last Date Edited            | datetime      | YES        |            |           |               | 0%      |         25 | 1900-01-01 00:00:00 | 2025-08-31 00:00:00 |
| Credit Amount               | numeric(19,5) | NO         |            |           |               | 0%      |       9111 | 0.00000             | 24718861.20000      |
| Debit Amount                | numeric(19,5) | NO         |            |           |               | 0%      |      34045 | 0.00000             | 22697502.40000      |
| FC Amount                   | numeric(20,5) | YES        |            |           |               | 0%      |      43155 | -24718861.20000     | 22697502.40000      |
| RC Amount                   | numeric(38,6) | YES        |            |           |               | 0%      |      50826 | -24718861.200000    | 22697502.400000     |
| Batch Source                | varchar(15)   | YES        |            |           |               | 99%     |          1 | —                   | —                   |
| Currency ID                 | varchar(15)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Description                 | varchar(31)   | YES        |            |           |               | 0%      |      36555 | —                   | —                   |
| Document Status             | varchar(100)  | YES        |            |           |               | 0%      |          3 | —                   | —                   |
| Intercompany ID             | varchar(5)    | YES        |            |           |               | 99%     |          3 | —                   | —                   |
| Originating Company ID      | varchar(5)    | YES        |            |           |               | 0%      |          5 | —                   | —                   |
| Last User                   | varchar(15)   | YES        |            |           |               | 0%      |         51 | —                   | —                   |
| User Who Posted             | varchar(15)   | YES        |            |           |               | 0%      |         47 | —                   | —                   |
| Modified Date               | datetime      | YES        |            |           |               | 0%      |         20 | 2011-11-05 00:00:00 | 2017-02-27 00:00:00 |
| Originating Control Number  | varchar(21)   | YES        |            |           |               | 0%      |      44159 | —                   | —                   |
| Originating Document Number | varchar(21)   | YES        |            |           |               | 0%      |      44395 | —                   | —                   |
| Originating Journal Entry   | int           | YES        |            |           |               | 0%      |       1285 | 0                   | 2339673             |
| Sequence Number             | numeric(19,5) | NO         |            |           |               | 0%      |        465 | 0.00000             | 5014976.00000       |
| Source Document             | varchar(11)   | YES        |            |           |               | 0%      |         18 | —                   | —                   |
| Transaction Type            | varchar(100)  | YES        |            |           |               | 99%     |          1 | —                   | —                   |
| Voided                      | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Batch Number                | varchar(15)   | YES        |            |           |               | 99%     |        106 | —                   | —                   |
| Originating TRX Source      | varchar(13)   | YES        |            |           |               | 0%      |      13700 | —                   | —                   |
| TRX Source                  | varchar(13)   | YES        |            |           |               | 0%      |      17515 | —                   | —                   |
| Originating Source          | varchar(15)   | YES        |            |           |               | 100%    |          1 | —                   | —                   |
| Reference                   | varchar(31)   | YES        |            |           |               | 0%      |      10868 | —                   | —                   |
| Originating Master ID       | varchar(31)   | YES        |            |           |               | 0%      |        728 | —                   | —                   |
| Originating Master Name     | varchar(65)   | YES        |            |           |               | 0%      |        941 | —                   | —                   |
| Originating Sequence Number | int           | NO         |            |           |               | 0%      |         68 | 0                   | 1163264             |
| Originating TRX Type        | varchar(100)  | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Fiscal_Year                 | smallint      | YES        |            |           |               | 0%      |         19 | 2008                | 2026                |
| Fiscal_Quarter              | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Fiscal_Period               | smallint      | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| Calendar_Year               | smallint      | YES        |            |           |               | 0%      |         18 | 2008                | 2025                |
| Calendar_Quarter            | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Calendar_Month              | smallint      | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| Month_Name                  | varchar(9)    | YES        |            |           |               | 0%      |         12 | —                   | —                   |
| PONUMBER                    | char(17)      | YES        |            |           |               | 52%     |      13553 | —                   | —                   |
| ITEMNMBR                    | char(31)      | YES        |            |           |               | 52%     |       5913 | —                   | —                   |
| ITEMDESC                    | char(101)     | YES        |            |           |               | 52%     |       7601 | —                   | —                   |
| VNDITDSC                    | char(101)     | YES        |            |           |               | 52%     |       7469 | —                   | —                   |
| COMMNTID                    | char(15)      | YES        |            |           |               | 52%     |          2 | —                   | —                   |
| LOCNCODE                    | char(11)      | YES        |            |           |               | 52%     |         71 | —                   | —                   |
| Project ID                  | char(31)      | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Project Description         | char(51)      | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| aaTrxDimCodeDescr2          | char(51)      | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Filter                      | varchar(6)    | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Assigned Original Amount    | numeric(38,5) | YES        |            |           |               | 100%    |          0 | NULL                | NULL                |
| Assigned FC Amount          | numeric(38,5) | YES        |            |           |               | 100%    |          0 | NULL                | NULL                |
| Assigned RC Amount          | numeric(38,5) | YES        |            |           |               | 100%    |          0 | NULL                | NULL                |
| GP FC Amount                | numeric(38,5) | YES        |            |           |               | 0%      |      43155 | -24718861.20000     | 22697502.40000      |
| GP RC Amount                | numeric(38,5) | YES        |            |           |               | 0%      |      50820 | -24718861.20000     | 22697502.40000      |

---

### dbo.CAPEX_cashflow {#dbo-capex-cashflow}

| Property | Value |
|---|---|
| Full name | `[dbo].[CAPEX_cashflow]` |
| Row count | 51,391 |
| Total size | 24.6 MB |
| Used size | 24.6 MB |
| Created | 2012-05-02 15:38 |
| Schema modified | 2012-05-02 15:38 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min              | Max              |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|------------------|------------------|
| GL Source                   | varchar(7)    | NO         |            |           |               | 0%      |          2 | —                | —                |
| Country                     | varchar(5)    | NO         |            |           |               | 0%      |          3 | —                | —                |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |          2 | —                | —                |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |         27 | —                | —                |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |          9 | —                | —                |
| Journal Entry               | int           | NO         |            |           |               | 0%      |      25259 | 0                | 1228137          |
| Series                      | varchar(100)  | YES        |            |           |               | 0%      |          4 | —                | —                |
| GL Post Trx Date            | date          | YES        |            |           |               | 0%      |       1141 | 2007-06-30       | 2012-05-01       |
| FC Amount                   | numeric(20,5) | YES        |            |           |               | 0%      |      32694 | -24718861.20000  | 22697502.40000   |
| RC Amount                   | numeric(38,6) | YES        |            |           |               | 0%      |      34296 | -24718861.200000 | 22697502.400000  |
| Currency ID                 | varchar(15)   | YES        |            |           |               | 0%      |          4 | —                | —                |
| Description                 | varchar(31)   | YES        |            |           |               | 0%      |      20885 | —                | —                |
| Document Status             | varchar(100)  | YES        |            |           |               | 0%      |          3 | —                | —                |
| Originating Control Number  | varchar(21)   | YES        |            |           |               | 0%      |      22151 | —                | —                |
| Originating Document Number | varchar(21)   | YES        |            |           |               | 0%      |      22164 | —                | —                |
| Sequence Number             | numeric(19,5) | NO         |            |           |               | 0%      |        129 | 0.00000          | 5003500.00000    |
| Source Document             | varchar(11)   | YES        |            |           |               | 0%      |         14 | —                | —                |
| Originating TRX Source      | varchar(13)   | YES        |            |           |               | 0%      |       5519 | —                | —                |
| GL TRX Source               | varchar(13)   | YES        |            |           |               | 0%      |       6810 | —                | —                |
| Originating Source          | varchar(15)   | YES        |            |           |               | 77%     |       1302 | —                | —                |
| Reference                   | varchar(31)   | YES        |            |           |               | 0%      |       3211 | —                | —                |
| Originating Master ID       | varchar(31)   | YES        |            |           |               | 0%      |        436 | —                | —                |
| Originating Master Name     | varchar(65)   | YES        |            |           |               | 0%      |        471 | —                | —                |
| Originating Sequence Number | int           | NO         |            |           |               | 0%      |         32 | 0                | 540672           |
| Originating TRX Type        | varchar(100)  | YES        |            |           |               | 0%      |          4 | —                | —                |
| FiscalYear                  | smallint      | YES        |            |           |               | 0%      |          6 | 2007             | 2012             |
| FiscalQuarter               | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                | —                |
| FiscalPeriod                | smallint      | YES        |            |           |               | 0%      |         12 | 1                | 12               |
| From Doc Date               | date          | YES        |            |           |               | 0%      |        512 | 1900-01-01       | 2012-04-26       |
| From GL PAID POST Date      | date          | YES        |            |           |               | 0%      |        468 | 1900-01-01       | 2012-04-26       |
| From Voucher                | varchar(21)   | NO         |            |           |               | 0%      |       3600 | —                | —                |
| DOCTYPE                     | smallint      | NO         |            |           |               | 0%      |          3 | 0                | 6                |
| FROMDOCTYPE                 | varchar(100)  | YES        |            |           |               | 0%      |          3 | —                | —                |
| APFRDCNM                    | varchar(21)   | NO         |            |           |               | 0%      |       3708 | —                | —                |
| APFRMAPLYAMT                | numeric(19,5) | NO         |            |           |               | 0%      |      11017 | 0.00000          | 2969177.31000    |
| ActualApplyToAmount         | numeric(19,5) | NO         |            |           |               | 0%      |      10872 | 0.00000          | 2969177.31000    |
| FC AMT PAID                 | decimal(12,2) | YES        |            |           |               | 0%      |      14061 | -76791.97        | 2969177.31       |
| RC AMT Paid                 | decimal(38,8) | YES        |            |           |               | 0%      |      14246 | -74859.17754867  | 4815708.67908900 |

---

### dbo.CAPEX_Cogeco {#dbo-capex-cogeco}

| Property | Value |
|---|---|
| Full name | `[dbo].[CAPEX_Cogeco]` |
| Row count | 81,885 |
| Total size | 87.5 MB |
| Used size | 87.5 MB |
| Created | 2026-03-06 09:08 |
| Schema modified | 2026-03-06 09:08 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| Country                     | varchar(5)    | NO         |            |           |               | 0%      |          4 | —                   | —                   |
| Budget ID                   | varchar(2)    | NO         |            |           |               | 0%      |          1 | —                   | —                   |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |         48 | —                   | —                   |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |          7 | —                   | —                   |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |         10 | —                   | —                   |
| Journal Entry               | int           | NO         |            |           |               | 0%      |      52917 | 0                   | 2670029             |
| Series                      | varchar(100)  | YES        |            |           |               | 0%      |          5 | —                   | —                   |
| TRX Date                    | datetime      | YES        |            |           |               | 0%      |       2591 | 2008-01-10 00:00:00 | 2025-08-31 00:00:00 |
| Last Date Edited            | datetime      | YES        |            |           |               | 0%      |         25 | 1900-01-01 00:00:00 | 2025-08-31 00:00:00 |
| Credit Amount               | numeric(19,5) | NO         |            |           |               | 0%      |       9111 | 0.00000             | 24718861.20000      |
| Debit Amount                | numeric(19,5) | NO         |            |           |               | 0%      |      34045 | 0.00000             | 22697502.40000      |
| FC Amount                   | numeric(20,5) | YES        |            |           |               | 0%      |      43155 | -24718861.20000     | 22697502.40000      |
| RC Amount                   | numeric(38,6) | YES        |            |           |               | 16%     |      50958 | -19412804.210000    | 19580911.147100     |
| Batch Source                | varchar(15)   | YES        |            |           |               | 99%     |          1 | —                   | —                   |
| Currency ID                 | varchar(15)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Description                 | varchar(31)   | YES        |            |           |               | 0%      |      36555 | —                   | —                   |
| Document Status             | varchar(100)  | YES        |            |           |               | 0%      |          3 | —                   | —                   |
| Intercompany ID             | varchar(5)    | YES        |            |           |               | 99%     |          3 | —                   | —                   |
| Originating Company ID      | varchar(5)    | YES        |            |           |               | 0%      |          5 | —                   | —                   |
| Last User                   | varchar(15)   | YES        |            |           |               | 0%      |         51 | —                   | —                   |
| User Who Posted             | varchar(15)   | YES        |            |           |               | 0%      |         47 | —                   | —                   |
| Modified Date               | datetime      | YES        |            |           |               | 0%      |         20 | 2011-11-05 00:00:00 | 2017-02-27 00:00:00 |
| Originating Control Number  | varchar(21)   | YES        |            |           |               | 0%      |      44159 | —                   | —                   |
| Originating Document Number | varchar(21)   | YES        |            |           |               | 0%      |      44395 | —                   | —                   |
| Originating Journal Entry   | int           | YES        |            |           |               | 0%      |       1285 | 0                   | 2339673             |
| Sequence Number             | numeric(19,5) | NO         |            |           |               | 0%      |        465 | 0.00000             | 5014976.00000       |
| Source Document             | varchar(11)   | YES        |            |           |               | 0%      |         18 | —                   | —                   |
| Transaction Type            | varchar(100)  | YES        |            |           |               | 99%     |          1 | —                   | —                   |
| Voided                      | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Batch Number                | varchar(15)   | YES        |            |           |               | 99%     |        106 | —                   | —                   |
| Originating TRX Source      | varchar(13)   | YES        |            |           |               | 0%      |      13700 | —                   | —                   |
| TRX Source                  | varchar(13)   | YES        |            |           |               | 0%      |      17515 | —                   | —                   |
| Originating Source          | varchar(15)   | YES        |            |           |               | 100%    |          1 | —                   | —                   |
| Reference                   | varchar(31)   | YES        |            |           |               | 0%      |      10868 | —                   | —                   |
| Originating Master ID       | varchar(31)   | YES        |            |           |               | 0%      |        728 | —                   | —                   |
| Originating Master Name     | varchar(65)   | YES        |            |           |               | 0%      |        941 | —                   | —                   |
| Originating Sequence Number | int           | NO         |            |           |               | 0%      |         68 | 0                   | 1163264             |
| Originating TRX Type        | varchar(100)  | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| FiscalYear                  | smallint      | YES        |            |           |               | 0%      |         18 | 2008                | 2025                |
| FiscalQuarter               | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| FiscalPeriod                | smallint      | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| CalendarYear                | smallint      | YES        |            |           |               | 0%      |         18 | 2008                | 2025                |
| CalendarQuarter             | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| CalendarMonth               | smallint      | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| MonthName                   | varchar(9)    | YES        |            |           |               | 0%      |         12 | —                   | —                   |
| PONUMBER                    | char(17)      | YES        |            |           |               | 52%     |      13553 | —                   | —                   |
| ITEMNMBR                    | char(31)      | YES        |            |           |               | 52%     |       5913 | —                   | —                   |
| ITEMDESC                    | char(101)     | YES        |            |           |               | 52%     |       7601 | —                   | —                   |
| VNDITDSC                    | char(101)     | YES        |            |           |               | 52%     |       7469 | —                   | —                   |
| COMMNTID                    | char(15)      | YES        |            |           |               | 52%     |          2 | —                   | —                   |
| LOCNCODE                    | char(11)      | YES        |            |           |               | 52%     |         71 | —                   | —                   |
| Project ID                  | char(31)      | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Project Description         | char(51)      | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| aaTrxDimCodeDescr2          | char(51)      | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Filter                      | varchar(6)    | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Assigned Original Amount    | numeric(38,5) | YES        |            |           |               | 100%    |          0 | NULL                | NULL                |
| Assigned FC Amount          | numeric(38,5) | YES        |            |           |               | 100%    |          0 | NULL                | NULL                |
| Assigned RC Amount          | numeric(38,5) | YES        |            |           |               | 100%    |          0 | NULL                | NULL                |
| GP FC Amount                | numeric(38,5) | YES        |            |           |               | 0%      |      43155 | -24718861.20000     | 22697502.40000      |
| GP RC Amount                | numeric(38,5) | YES        |            |           |               | 16%     |      50955 | -19412804.21000     | 19580911.14710      |

---

### dbo.CAPEX_Cogeco1 {#dbo-capex-cogeco1}

| Property | Value |
|---|---|
| Full name | `[dbo].[CAPEX_Cogeco1]` |
| Row count | 46,665 |
| Total size | 51.4 MB |
| Used size | 51.4 MB |
| Created | 2015-03-03 14:46 |
| Schema modified | 2015-03-03 14:46 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| Country                     | varchar(5)    | NO         |            |           |               | 0%      |          4 | —                   | —                   |
| Budget ID                   | varchar(2)    | NO         |            |           |               | 0%      |          1 | —                   | —                   |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |         44 | —                   | —                   |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |          7 | —                   | —                   |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |         10 | —                   | —                   |
| Journal Entry               | int           | NO         |            |           |               | 0%      |      39667 | 0                   | 1963890             |
| Series                      | varchar(100)  | YES        |            |           |               | 0%      |          5 | —                   | —                   |
| TRX Date                    | datetime      | YES        |            |           |               | 0%      |       1892 | 2008-01-10 00:00:00 | 2015-03-28 00:00:00 |
| Last Date Edited            | datetime      | YES        |            |           |               | 0%      |         74 | 1900-01-01 00:00:00 | 2015-03-02 00:00:00 |
| Credit Amount               | numeric(19,5) | NO         |            |           |               | 0%      |       4427 | 0.00000             | 24718861.20000      |
| Debit Amount                | numeric(19,5) | NO         |            |           |               | 0%      |      26374 | 0.00000             | 22697502.40000      |
| FC Amount                   | numeric(20,5) | YES        |            |           |               | 0%      |      30800 | -24718861.20000     | 22697502.40000      |
| RC Amount                   | numeric(38,6) | YES        |            |           |               | 29%     |      29936 | -15892759.350923    | 13671267.700000     |
| Batch Source                | varchar(15)   | YES        |            |           |               | 100%    |          1 | —                   | —                   |
| Currency ID                 | varchar(15)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Description                 | varchar(31)   | YES        |            |           |               | 0%      |      31082 | —                   | —                   |
| Document Status             | varchar(100)  | YES        |            |           |               | 0%      |          3 | —                   | —                   |
| Intercompany ID             | varchar(5)    | YES        |            |           |               | 100%    |          3 | —                   | —                   |
| Originating Company ID      | varchar(5)    | YES        |            |           |               | 0%      |          5 | —                   | —                   |
| Last User                   | varchar(15)   | YES        |            |           |               | 0%      |         37 | —                   | —                   |
| User Who Posted             | varchar(15)   | YES        |            |           |               | 0%      |         32 | —                   | —                   |
| Modified Date               | datetime      | YES        |            |           |               | 0%      |         16 | 2011-11-05 00:00:00 | 2014-03-28 00:00:00 |
| Originating Control Number  | varchar(21)   | YES        |            |           |               | 0%      |      33132 | —                   | —                   |
| Originating Document Number | varchar(21)   | YES        |            |           |               | 0%      |      33247 | —                   | —                   |
| Originating Journal Entry   | int           | YES        |            |           |               | 0%      |       1094 | 0                   | 1962156             |
| Sequence Number             | numeric(19,5) | NO         |            |           |               | 0%      |        222 | 0.00000             | 5004500.00000       |
| Source Document             | varchar(11)   | YES        |            |           |               | 0%      |         18 | —                   | —                   |
| Transaction Type            | varchar(100)  | YES        |            |           |               | 100%    |          2 | —                   | —                   |
| Voided                      | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Batch Number                | varchar(15)   | YES        |            |           |               | 100%    |         28 | —                   | —                   |
| Originating TRX Source      | varchar(13)   | YES        |            |           |               | 0%      |       9258 | —                   | —                   |
| TRX Source                  | varchar(13)   | YES        |            |           |               | 0%      |      12304 | —                   | —                   |
| Originating Source          | varchar(15)   | YES        |            |           |               | 94%     |        944 | —                   | —                   |
| Reference                   | varchar(31)   | YES        |            |           |               | 0%      |       6340 | —                   | —                   |
| Originating Master ID       | varchar(31)   | YES        |            |           |               | 0%      |        628 | —                   | —                   |
| Originating Master Name     | varchar(65)   | YES        |            |           |               | 0%      |        790 | —                   | —                   |
| Originating Sequence Number | int           | NO         |            |           |               | 0%      |         67 | 0                   | 1163264             |
| Originating TRX Type        | varchar(100)  | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| FiscalYear                  | smallint      | YES        |            |           |               | 0%      |          8 | 2008                | 2015                |
| FiscalQuarter               | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| FiscalPeriod                | smallint      | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| CalendarYear                | smallint      | YES        |            |           |               | 0%      |          8 | 2008                | 2015                |
| CalendarQuarter             | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| CalendarMonth               | smallint      | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| MonthName                   | varchar(9)    | YES        |            |           |               | 0%      |         12 | —                   | —                   |
| PONUMBER                    | char(17)      | YES        |            |           |               | 30%     |      10755 | —                   | —                   |
| ITEMNMBR                    | char(31)      | YES        |            |           |               | 30%     |       5602 | —                   | —                   |
| ITEMDESC                    | char(101)     | YES        |            |           |               | 30%     |       7070 | —                   | —                   |
| VNDITDSC                    | char(101)     | YES        |            |           |               | 30%     |       7101 | —                   | —                   |
| COMMNTID                    | char(15)      | YES        |            |           |               | 30%     |          2 | —                   | —                   |
| LOCNCODE                    | char(11)      | YES        |            |           |               | 30%     |         56 | —                   | —                   |
| Project ID                  | char(31)      | YES        |            |           |               | 99%     |         70 | —                   | —                   |
| Project Description         | char(51)      | YES        |            |           |               | 99%     |         62 | —                   | —                   |
| aaTrxDimCodeDescr2          | char(51)      | YES        |            |           |               | 99%     |          1 | —                   | —                   |
| Filter                      | varchar(6)    | YES        |            |           |               | 99%     |          2 | —                   | —                   |
| Assigned Original Amount    | numeric(38,5) | YES        |            |           |               | 99%     |        380 | -417008.12000       | 45120.00000         |
| Assigned FC Amount          | numeric(38,5) | YES        |            |           |               | 99%     |        380 | -417008.12000       | 45120.00000         |
| Assigned RC Amount          | numeric(38,5) | YES        |            |           |               | 99%     |        388 | -459201.41859       | 45120.00000         |
| GP FC Amount                | numeric(38,5) | YES        |            |           |               | 0%      |      30803 | -24718861.20000     | 22697502.40000      |
| GP RC Amount                | numeric(38,5) | YES        |            |           |               | 29%     |      29937 | -15892759.35092     | 13671267.70000      |

---

### dbo.colo {#dbo-colo}

| Property | Value |
|---|---|
| Full name | `[dbo].[colo]` |
| Row count | 244,255 |
| Total size | 181.9 MB |
| Used size | 181.9 MB |
| Created | 2011-11-16 10:20 |
| Schema modified | 2011-11-16 10:20 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column              | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min           | Max            |
|---------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------|----------------|
| EXtended            | numeric(38,6) | YES        |            |           |               | 0%      |      43682 | -80112.500000 | 193125.000000  |
| GL_Service_Account  | int           | YES        |            |           |               | 36%     |         25 | 616           | 1162           |
| Category            | varchar(51)   | YES        |            |           |               | 36%     |          4 | —             | —              |
| Account Description | varchar(181)  | YES        |            |           |               | 36%     |         25 | —             | —              |
| Natural Account     | varchar(39)   | YES        |            |           |               | 36%     |          2 | —             | —              |
| VOIDSTTS            | smallint      | NO         |            |           |               | 0%      |          1 | 0             | 0              |
| LN CT               | char(11)      | YES        |            |           |               | 36%     |         38 | —             | —              |
| QUANTITY            | numeric(19,5) | YES        |            |           |               | 36%     |        158 | 1.00000       | 45000000.00000 |
| DSCRIPTN            | char(31)      | YES        |            |           |               | 36%     |        480 | —             | —              |
| ITEMNMBR            | char(31)      | NO         |            |           |               | 0%      |        551 | —             | —              |
| ITEMDESC            | char(101)     | NO         |            |           |               | 0%      |       2563 | —             | —              |
| USRDEF04            | char(21)      | YES        |            |           |               | 36%     |       2281 | —             | —              |
| PRODUCT_LINE        | char(255)     | YES        |            |           |               | 46%     |          3 | —             | —              |
| Customer            | varchar(80)   | YES        |            |           |               | 0%      |       2104 | —             | —              |
| HDR CT              | char(11)      | YES        |            |           |               | 36%     |         12 | —             | —              |
| CalendarYear        | smallint      | YES        |            |           |               | 0%      |         12 | 2006          | 2020           |
| CalendarQuarter     | varchar(2)    | YES        |            |           |               | 0%      |          4 | —             | —              |
| CalendarMonth       | smallint      | YES        |            |           |               | 0%      |         12 | 1             | 12             |
| MonthName           | varchar(9)    | YES        |            |           |               | 0%      |         12 | —             | —              |
| Expr1               | varchar(51)   | YES        |            |           |               | 0%      |         12 | —             | —              |
| Expr2               | varchar(181)  | YES        |            |           |               | 0%      |        125 | —             | —              |
| Expr3               | varchar(39)   | YES        |            |           |               | 0%      |         43 | —             | —              |
| Location            | varchar(99)   | YES        |            |           |               | 0%      |          8 | —             | —              |

---

### dbo.Colo_Churn {#dbo-colo-churn}

| Property | Value |
|---|---|
| Full name | `[dbo].[Colo_Churn]` |
| Row count | 3,759,782 |
| Total size | 2.0 GB |
| Used size | 2.0 GB |
| Created | 2014-11-24 09:21 |
| Schema modified | 2014-11-24 09:21 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| gpinstance                  | varchar(5)    | NO         |            |           |               | 0%      |          3 | —                   | —                   |
| SERVICE_ID                  | char(21)      | YES        |            |           |               | 0%      |      50215 | —                   | —                   |
| Customer                    | varchar(81)   | YES        |            |           |               | 0%      |      11551 | —                   | —                   |
| Doc Status                  | varchar(5)    | NO         |            |           |               | 0%      |          2 | —                   | —                   |
| Void Date                   | datetime      | NO         |            |           |               | 0%      |        261 | 1900-01-01 00:00:00 | 2015-01-01 00:00:00 |
| GLPOSTDT                    | datetime      | NO         |            |           |               | 0%      |        816 | 2011-06-07 00:00:00 | 2014-12-04 00:00:00 |
| PeriodStart                 | datetime      | YES        |            |           |               | 0%      |        958 | 2012-07-01 00:00:00 | 2019-05-01 00:00:00 |
| PeriodEnd                   | datetime      | YES        |            |           |               | 0%      |       1477 | 2012-07-01 00:00:00 | 2019-05-31 00:00:00 |
| xtndprce_period             | numeric(38,6) | YES        |            |           |               | 1%      |     555871 | -100594.270037      | 502371640389.000000 |
| xtndprce_period_nx          | numeric(38,6) | YES        |            |           |               | 0%      |     308388 | -91936.547175       | 549690000000.000000 |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |         23 | —                   | —                   |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |         13 | —                   | —                   |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |          5 | —                   | —                   |
| Original Posting Accounting | varchar(181)  | YES        |            |           |               | 0%      |        283 | —                   | —                   |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |        283 | —                   | —                   |
| Customer Class              | varchar(15)   | YES        |            |           |               | 0%      |          7 | —                   | —                   |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |          5 | —                   | —                   |
| Class                       | varchar(21)   | YES        |            |           |               | 0%      |          7 | —                   | —                   |
| ITEMNMBR                    | char(31)      | NO         |            |           |               | 0%      |       1636 | —                   | —                   |
| ITEMDESC                    | char(101)     | NO         |            |           |               | 0%      |       2567 | —                   | —                   |

---

### dbo.Colo_Churn_ALL {#dbo-colo-churn-all}

| Property | Value |
|---|---|
| Full name | `[dbo].[Colo_Churn_ALL]` |
| Row count | 1,174,658 |
| Total size | 655.6 MB |
| Used size | 655.5 MB |
| Created | 2012-07-11 09:37 |
| Schema modified | 2012-07-11 14:40 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| gpinstance                  | varchar(5)    | NO         |            |           |               | 0%      |          3 | —                   | —                   |
| SERVICE_ID                  | char(21)      | YES        |            |           |               | 0%      |      33262 | —                   | —                   |
| Customer                    | varchar(81)   | YES        |            |           |               | 0%      |      10362 | —                   | —                   |
| Doc Status                  | varchar(5)    | NO         |            |           |               | 0%      |          2 | —                   | —                   |
| Void Date                   | datetime      | NO         |            |           |               | 0%      |        103 | 1900-01-01 00:00:00 | 2013-03-01 00:00:00 |
| GLPOSTDT                    | datetime      | NO         |            |           |               | 0%      |        420 | 2010-02-03 00:00:00 | 2013-03-01 00:00:00 |
| PeriodStart                 | datetime      | YES        |            |           |               | 0%      |        293 | 2012-01-01 00:00:00 | 2016-06-01 00:00:00 |
| PeriodEnd                   | datetime      | YES        |            |           |               | 0%      |        882 | 2012-01-01 00:00:00 | 2016-06-30 00:00:00 |
| xtndprce_period             | numeric(38,6) | YES        |            |           |               | 2%      |     160274 | -23449.056158       | 194558.895187       |
| xtndprce_period_nx          | numeric(38,6) | YES        |            |           |               | 0%      |     115533 | -23304.950000       | 193125.000000       |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |         16 | —                   | —                   |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |         13 | —                   | —                   |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |          7 | —                   | —                   |
| Original Posting Accounting | varchar(181)  | YES        |            |           |               | 0%      |        236 | —                   | —                   |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |        235 | —                   | —                   |
| Customer Class              | varchar(15)   | YES        |            |           |               | 0%      |          7 | —                   | —                   |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |          5 | —                   | —                   |
| Class                       | varchar(21)   | YES        |            |           |               | 0%      |          5 | —                   | —                   |
| ITEMNMBR                    | char(31)      | NO         |            |           |               | 0%      |       1064 | —                   | —                   |
| ITEMDESC                    | char(101)     | NO         |            |           |               | 0%      |       1080 | —                   | —                   |

---

### dbo.CustomerCredits {#dbo-customercredits}

| Property | Value |
|---|---|
| Full name | `[dbo].[CustomerCredits]` |
| Row count | 461,282 |
| Total size | 278.6 MB |
| Used size | 278.5 MB |
| Created | 2026-03-06 08:08 |
| Schema modified | 2026-03-06 08:08 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column              | Type          | Nullable   | Identity   | Default   | Description   | NULL%   | Distinct   | Min           | Max       |
|---------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------|-----------|
| CUSTNMBR            | varchar(15)   | YES        |            |           |               | 0%      | 14076      | —             | —         |
| Customer Name       | varchar(81)   | YES        |            |           |               | 0%      | 14076      | —             | —         |
| Doc number          | char(21)      | NO         |            |           |               | 0%      | 68735      | —             | —         |
| Type                | smallint      | NO         |            |           |               | 0%      | 1          | 4             | 4         |
| Document Date       | char(10)      | YES        |            |           |               | 0%      | 3587       | —             | —         |
| RM GLPOST           | char(10)      | YES        |            |           |               | 0%      | 3389       | —             | —         |
| VOIDSTTS            | smallint      | NO         |            |           |               | 0%      | 2          | 0             | 1         |
| Item                | char(31)      | NO         |            |           |               | 0%      | 3173       | —             | —         |
| Description         | char(101)     | NO         |            |           |               | 0%      | 2851       | —             | —         |
| Orginal Price       | numeric(19,5) | YES        |            |           |               | 0%      | 52339      | -293979.36000 | 410.74000 |
| Extended Price      | numeric(19,5) | YES        |            |           |               | 0%      | 53310      | -293979.36000 | 410.74000 |
| Currency            | varchar(15)   | YES        |            |           |               | 0%      | 4          | —             | —         |
| Start Date          | char(10)      | YES        |            |           |               | 0%      | 5260       | —             | —         |
| End Date            | char(10)      | YES        |            |           |               | 0%      | 4921       | —             | —         |
| Contract number     | char(11)      | NO         |            |           |               | 0%      | 101999     | —             | —         |
| Account             | varchar(129)  | YES        |            |           |               | 0%      | 529        | —             | —         |
| RMVOID              | char(10)      | YES        |            |           |               | 0%      | 385        | —             | —         |
| Natural Account     | varchar(7)    | YES        |            |           |               | 0%      | 11         | —             | —         |
| Voided Month        | int           | YES        |            |           |               | 0%      | 95         | 190001        | 202502    |
| Posted Month        | int           | YES        |            |           |               | 0%      | 190        | 201006        | 202603    |
| Category            | varchar(51)   | YES        |            |           |               | 0%      | 13         | —             | —         |
| Account Description | varchar(181)  | YES        |            |           |               | 0%      | 529        | —             | —         |
| Entity              | varchar(99)   | YES        |            |           |               | 0%      | 11         | —             | —         |
| Location            | varchar(99)   | YES        |            |           |               | 0%      | 29         | —             | —         |
| Cost Centre         | varchar(99)   | YES        |            |           |               | 0%      | 22         | —             | —         |
| gl_Natural_Account  | varchar(39)   | YES        |            |           |               | 0%      | 11         | —             | —         |
| Department          | varchar(21)   | YES        |            |           |               | 0%      | 10         | —             | —         |
| Class               | varchar(21)   | YES        |            |           |               | 0%      | 14         | —             | —         |
| EBITDA              | varchar(31)   | YES        |            |           |               | 0%      | 4          | —             | —         |
| Budget Group        | varchar(31)   | YES        |            |           |               | 0%      | 22         | —             | —         |
| Country             | nvarchar(128) | YES        |            |           |               | 0%      | 4          | —             | —         |
| CMMTTEXT            | text          | YES        |            |           |               | ?       | ?          | —             | —         |
| PSTUSRID            | char(15)      | NO         |            |           |               | 0%      | 34         | —             | —         |

---

### dbo.DateDimension {#dbo-datedimension}

| Property | Value |
|---|---|
| Full name | `[dbo].[DateDimension]` |
| Row count | 11,688 |
| Total size | 0.9 MB |
| Used size | 0.9 MB |
| Created | 2014-12-02 12:39 |
| Schema modified | 2014-12-02 12:39 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column               | Type       | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|----------------------|------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| IntegerKey           | smallint   | YES        |            |           |               | 0%      |      11688 | 1                   | 11688               |
| DateKey              | datetime   | YES        |            |           |               | 0%      |      11688 | 1999-01-01 00:00:00 | 2030-12-31 00:00:00 |
| DayNumberOfWeek      | smallint   | YES        |            |           |               | 0%      |          7 | 1                   | 7                   |
| DayNameOfWeek        | varchar(9) | YES        |            |           |               | 0%      |          7 | —                   | —                   |
| DayNumberOfMonth     | smallint   | YES        |            |           |               | 0%      |         31 | 1                   | 31                  |
| WeekNumberOfYear     | smallint   | YES        |            |           |               | 0%      |         54 | 1                   | 54                  |
| MonthName            | varchar(9) | YES        |            |           |               | 0%      |         12 | —                   | —                   |
| CalendarMonth        | smallint   | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| CalendarQuarter      | varchar(2) | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| CalendarYear         | smallint   | YES        |            |           |               | 0%      |         32 | 1999                | 2030                |
| FiscalPeriod         | smallint   | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| FiscalQuarter        | varchar(2) | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| FiscalYear           | smallint   | YES        |            |           |               | 0%      |         33 | 1999                | 2031                |
| FiscalYear_Cogeco    | smallint   | YES        |            |           |               | 0%      |         33 | 1999                | 2031                |
| FiscalPeriod_Cogeco  | smallint   | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| FiscalQuarter_Cogeco | varchar(2) | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Dateshort            | date       | YES        |            |           |               | 0%      |      11688 | 1999-01-01          | 2030-12-31          |

---

### dbo.Depreciation_Projections {#dbo-depreciation-projections}

| Property | Value |
|---|---|
| Full name | `[dbo].[Depreciation_Projections]` |
| Row count | 199,296 |
| Total size | 65.1 MB |
| Used size | 64.9 MB |
| Created | 2026-03-06 08:02 |
| Schema modified | 2026-03-06 08:02 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column           | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| ASSETID          | char(15)      | NO         |            |           |               | 0%      |      11916 | —                   | —                   |
| ASSETDESC        | char(41)      | NO         |            |           |               | 0%      |       7402 | —                   | —                   |
| Acquisition_Cost | numeric(19,5) | NO         |            |           |               | 0%      |      12860 | 0.01000             | 10058836.66000      |
| ACQDATE          | datetime      | NO         |            |           |               | 0%      |       2540 | 2002-08-28 00:00:00 | 2017-03-31 00:00:00 |
| ASSETCLASSID     | char(15)      | NO         |            |           |               | 0%      |         23 | —                   | —                   |
| FAPERIOD         | smallint      | NO         |            |           |               | 0%      |         12 | 1                   | 12                  |
| FAYEAR           | smallint      | NO         |            |           |               | 0%      |          8 | 2011                | 2018                |
| YTDDEPRAMT       | numeric(19,5) | NO         |            |           |               | 0%      |      19859 | -0.04000            | 84679.69000         |
| Account          | char(129)     | NO         |            |           |               | 0%      |        109 | —                   | —                   |
| ACTDESCR         | char(51)      | NO         |            |           |               | 0%      |         98 | —                   | —                   |
| Location         | char(31)      | NO         |            |           |               | 0%      |         19 | —                   | —                   |
| Currency         | varchar(3)    | NO         |            |           |               | 0%      |          3 | —                   | —                   |

---

### dbo.EBITDA {#dbo-ebitda}

| Property | Value |
|---|---|
| Full name | `[dbo].[EBITDA]` |
| Row count | 362 |
| Total size | 0.0 MB |
| Used size | 0.0 MB |
| Created | 2010-08-12 15:16 |
| Schema modified | 2010-08-12 15:17 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column       | Type       | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max   |
|--------------|------------|------------|------------|-----------|---------------|---------|------------|-------|-------|
| Main Segment | char(67)   | NO         |            |           |               | 0%      |        362 | —     | —     |
| Filter       | varchar(3) | NO         |            |           |               | 0%      |          2 | —     | —     |

---

### dbo.EBITDA20120206 {#dbo-ebitda20120206}

| Property | Value |
|---|---|
| Full name | `[dbo].[EBITDA20120206]` |
| Row count | 358 |
| Total size | 0.0 MB |
| Used size | 0.0 MB |
| Created | 2012-02-06 15:49 |
| Schema modified | 2012-02-06 15:49 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column       | Type       | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max   |
|--------------|------------|------------|------------|-----------|---------------|---------|------------|-------|-------|
| Main Segment | char(67)   | NO         |            |           |               | 0%      |        358 | —     | —     |
| Filter       | varchar(3) | NO         |            |           |               | 0%      |          2 | —     | —     |

---

### dbo.finance_revenue_mapping {#dbo-finance-revenue-mapping}

| Property | Value |
|---|---|
| Full name | `[dbo].[finance_revenue_mapping]` |
| Row count | 4,614,197 |
| Total size | 2.8 GB |
| Used size | 2.8 GB |
| Created | 2026-03-05 11:00 |
| Schema modified | 2026-03-05 11:00 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column              | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|---------------------|----------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| index_              | bigint         | YES        |            |           |               | 0%      |    4614197 | 1                   | 4614197             |
| client_id           | int            | YES        |            |           |               | 0%      |       4086 | 1000002             | 7036717             |
| revenue_date        | int            | YES        |            |           |               | 0%      |        146 | 201701              | 202902              |
| service_id          | varchar(20)    | YES        |            |           |               | 5%      |      28963 | —                   | —                   |
| ITEMNMBR            | varchar(31)    | NO         |            |           |               | 0%      |       2931 | —                   | —                   |
| lnitmseq            | int            | NO         |            |           |               | 0%      |      23113 | 8192                | 378896384           |
| product             | nvarchar(255)  | YES        |            |           |               | 0%      |        860 | —                   | —                   |
| xtndprce_period     | numeric(38,4)  | YES        |            |           |               | 0%      |     597823 | -334225.7102        | 2241888.0000        |
| xtndprce_period_nx  | numeric(38,4)  | YES        |            |           |               | 0%      |     236182 | -448153.2000        | 2500000.0000        |
| lob                 | nvarchar(255)  | YES        |            |           |               | 0%      |         11 | —                   | —                   |
| segment             | nvarchar(4000) | YES        |            |           |               | 0%      |         31 | —                   | —                   |
| datacenter_city     | nvarchar(100)  | YES        |            |           |               | 5%      |         21 | —                   | —                   |
| datacenter_name     | nvarchar(100)  | YES        |            |           |               | 5%      |         23 | —                   | —                   |
| Customer            | nvarchar(255)  | YES        |            |           |               | 0%      |       4086 | —                   | —                   |
| GLPOSTDT            | datetime       | YES        |            |           |               | 0%      |       1820 | 2019-01-01 00:00:00 | 2026-03-07 00:00:00 |
| Location            | varchar(99)    | YES        |            |           |               | 0%      |         30 | —                   | —                   |
| Cost Centre         | varchar(99)    | YES        |            |           |               | 0%      |         22 | —                   | —                   |
| Natural Account     | varchar(39)    | YES        |            |           |               | 0%      |         11 | —                   | —                   |
| Account Description | varchar(181)   | YES        |            |           |               | 0%      |        391 | —                   | —                   |
| Category            | varchar(51)    | YES        |            |           |               | 0%      |         12 | —                   | —                   |
| DOCNUMBR            | varchar(21)    | NO         |            |           |               | 0%      |     217223 | —                   | —                   |
| client_type         | nvarchar(64)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| DOCDATE             | datetime       | YES        |            |           |               | 0%      |       2417 | 2018-01-01 00:00:00 | 2026-03-05 00:00:00 |
| Doc Status          | varchar(5)     | NO         |            |           |               | 0%      |          2 | —                   | —                   |
| gpinstance          | varchar(5)     | NO         |            |           |               | 0%      |          6 | —                   | —                   |
| revenue_period      | date           | YES        |            |           |               | 0%      |        146 | 2017-01-01          | 2029-02-01          |

---

### dbo.finance_revenue_mapping_networking {#dbo-finance-revenue-mapping-networking}

| Property | Value |
|---|---|
| Full name | `[dbo].[finance_revenue_mapping_networking]` |
| Row count | 4,437,284 |
| Total size | 2.7 GB |
| Used size | 2.7 GB |
| Created | 2025-08-11 15:30 |
| Schema modified | 2025-08-11 15:30 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column              | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|---------------------|----------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| index_              | bigint         | YES        |            |           |               | 0%      |    4437284 | 1                   | 4437284             |
| client_id           | int            | YES        |            |           |               | 0%      |       4078 | 1000002             | 7036707             |
| revenue_date        | int            | YES        |            |           |               | 0%      |        138 | 201701              | 202806              |
| service_id          | varchar(20)    | YES        |            |           |               | 5%      |      28195 | —                   | —                   |
| ITEMNMBR            | varchar(31)    | NO         |            |           |               | 0%      |       2870 | —                   | —                   |
| lnitmseq            | int            | NO         |            |           |               | 0%      |      23113 | 8192                | 378896384           |
| product             | nvarchar(255)  | YES        |            |           |               | 0%      |        844 | —                   | —                   |
| xtndprce_period     | numeric(38,4)  | YES        |            |           |               | 0%      |     571809 | -334225.7102        | 2241888.0000        |
| xtndprce_period_nx  | numeric(38,4)  | YES        |            |           |               | 0%      |     228437 | -448153.2000        | 2500000.0000        |
| lob                 | nvarchar(255)  | YES        |            |           |               | 0%      |         11 | —                   | —                   |
| segment             | nvarchar(4000) | YES        |            |           |               | 0%      |         39 | —                   | —                   |
| datacenter_city     | nvarchar(100)  | YES        |            |           |               | 5%      |         21 | —                   | —                   |
| datacenter_name     | nvarchar(100)  | YES        |            |           |               | 5%      |         23 | —                   | —                   |
| Customer            | nvarchar(255)  | YES        |            |           |               | 0%      |       4078 | —                   | —                   |
| GLPOSTDT            | datetime       | YES        |            |           |               | 0%      |       1689 | 2019-01-01 00:00:00 | 2025-08-07 00:00:00 |
| Location            | varchar(99)    | YES        |            |           |               | 0%      |         30 | —                   | —                   |
| Cost Centre         | varchar(99)    | YES        |            |           |               | 0%      |         22 | —                   | —                   |
| Natural Account     | varchar(39)    | YES        |            |           |               | 0%      |         11 | —                   | —                   |
| Account Description | varchar(181)   | YES        |            |           |               | 0%      |        388 | —                   | —                   |
| Category            | varchar(51)    | YES        |            |           |               | 0%      |         12 | —                   | —                   |
| DOCNUMBR            | varchar(21)    | NO         |            |           |               | 0%      |     207495 | —                   | —                   |
| client_type         | nvarchar(64)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| DOCDATE             | datetime       | YES        |            |           |               | 0%      |       2257 | 2018-01-01 00:00:00 | 2025-08-06 00:00:00 |
| Doc Status          | varchar(5)     | NO         |            |           |               | 0%      |          2 | —                   | —                   |
| gpinstance          | varchar(5)     | NO         |            |           |               | 0%      |          6 | —                   | —                   |
| revenue_period      | date           | YES        |            |           |               | 0%      |        138 | 2017-01-01          | 2028-06-01          |

---

### dbo.finance_revenue_mapping_prod {#dbo-finance-revenue-mapping-prod}

| Property | Value |
|---|---|
| Full name | `[dbo].[finance_revenue_mapping_prod]` |
| Row count | 4,109,560 |
| Total size | 2.4 GB |
| Used size | 2.4 GB |
| Created | 2024-08-03 22:15 |
| Schema modified | 2024-08-03 22:15 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column              | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|---------------------|----------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| index_              | bigint         | YES        |            |           |               | 0%      |    4109560 | 1                   | 4109560             |
| client_id           | int            | YES        |            |           |               | 0%      |       4050 | 1000002             | 7036683             |
| revenue_date        | int            | YES        |            |           |               | 0%      |        121 | 201701              | 202701              |
| service_id          | varchar(20)    | YES        |            |           |               | 4%      |      27711 | —                   | —                   |
| ITEMNMBR            | varchar(31)    | NO         |            |           |               | 0%      |       2784 | —                   | —                   |
| lnitmseq            | int            | NO         |            |           |               | 0%      |      23113 | 8192                | 378896384           |
| product             | nvarchar(255)  | YES        |            |           |               | 0%      |        894 | —                   | —                   |
| xtndprce_period     | numeric(38,4)  | YES        |            |           |               | 0%      |     527116 | -334225.7102        | 1998465.2500        |
| xtndprce_period_nx  | numeric(38,4)  | YES        |            |           |               | 0%      |     215571 | -448153.2000        | 2500000.0000        |
| lob                 | nvarchar(255)  | YES        |            |           |               | 0%      |         11 | —                   | —                   |
| segment             | nvarchar(4000) | YES        |            |           |               | 0%      |         30 | —                   | —                   |
| datacenter_city     | nvarchar(100)  | YES        |            |           |               | 5%      |         22 | —                   | —                   |
| datacenter_name     | nvarchar(100)  | YES        |            |           |               | 5%      |         23 | —                   | —                   |
| Customer            | nvarchar(255)  | YES        |            |           |               | 0%      |       4050 | —                   | —                   |
| GLPOSTDT            | datetime       | YES        |            |           |               | 0%      |       1458 | 2019-01-01 00:00:00 | 2024-08-02 00:00:00 |
| Location            | varchar(99)    | YES        |            |           |               | 0%      |         30 | —                   | —                   |
| Cost Centre         | varchar(99)    | YES        |            |           |               | 0%      |         22 | —                   | —                   |
| Natural Account     | varchar(39)    | YES        |            |           |               | 0%      |         11 | —                   | —                   |
| Account Description | varchar(181)   | YES        |            |           |               | 0%      |        381 | —                   | —                   |
| Category            | varchar(51)    | YES        |            |           |               | 0%      |         12 | —                   | —                   |
| DOCNUMBR            | varchar(21)    | NO         |            |           |               | 0%      |     190155 | —                   | —                   |
| client_type         | nvarchar(64)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| DOCDATE             | datetime       | YES        |            |           |               | 0%      |       1982 | 2018-01-01 00:00:00 | 2024-08-02 00:00:00 |
| Doc Status          | varchar(5)     | NO         |            |           |               | 0%      |          2 | —                   | —                   |
| gpinstance          | varchar(5)     | NO         |            |           |               | 0%      |          6 | —                   | —                   |
| revenue_period      | date           | YES        |            |           |               | 0%      |        121 | 2017-01-01          | 2027-01-01          |

---

### dbo.finance_revenue_mapping2 {#dbo-finance-revenue-mapping2}

| Property | Value |
|---|---|
| Full name | `[dbo].[finance_revenue_mapping2]` |
| Row count | 2,150,445 |
| Total size | 1.2 GB |
| Used size | 1.2 GB |
| Created | 2022-04-01 12:50 |
| Schema modified | 2022-04-01 12:50 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column              | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|---------------------|----------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| index_              | bigint         | YES        |            |           |               | 0%      |    2150445 | 1                   | 2150445             |
| client_id           | int            | YES        |            |           |               | 0%      |       3942 | 1000002             | 7036549             |
| revenue_date        | int            | YES        |            |           |               | 0%      |        117 | 201701              | 202609              |
| service_id          | varchar(20)    | YES        |            |           |               | 0%      |      27443 | —                   | —                   |
| ITEMNMBR            | varchar(31)    | NO         |            |           |               | 0%      |       2519 | —                   | —                   |
| product             | nvarchar(255)  | YES        |            |           |               | 1%      |        514 | —                   | —                   |
| xtndprce_period     | numeric(38,4)  | YES        |            |           |               | 0%      |     399379 | -229750.2589        | 1998465.2500        |
| xtndprce_period_nx  | numeric(38,4)  | YES        |            |           |               | 0%      |     176379 | -291674.8400        | 2500000.0000        |
| lob                 | nvarchar(255)  | YES        |            |           |               | 0%      |          7 | —                   | —                   |
| segment             | nvarchar(4000) | YES        |            |           |               | 0%      |         16 | —                   | —                   |
| datacenter_city     | nvarchar(100)  | YES        |            |           |               | 1%      |         28 | —                   | —                   |
| datacenter_name     | nvarchar(100)  | YES        |            |           |               | 1%      |         37 | —                   | —                   |
| Customer            | nvarchar(255)  | YES        |            |           |               | 0%      |       4284 | —                   | —                   |
| GLPOSTDT            | datetime       | YES        |            |           |               | 0%      |        933 | 2019-01-01 00:00:00 | 2022-03-31 00:00:00 |
| Location            | varchar(99)    | YES        |            |           |               | 0%      |         29 | —                   | —                   |
| Cost Centre         | varchar(99)    | YES        |            |           |               | 0%      |         17 | —                   | —                   |
| Natural Account     | varchar(39)    | YES        |            |           |               | 0%      |         12 | —                   | —                   |
| Account Description | varchar(181)   | YES        |            |           |               | 0%      |        340 | —                   | —                   |
| Category            | varchar(51)    | YES        |            |           |               | 0%      |          9 | —                   | —                   |
| DOCNUMBR            | varchar(21)    | NO         |            |           |               | 0%      |     140614 | —                   | —                   |
| client_type         | nvarchar(64)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| DOCDATE             | datetime       | YES        |            |           |               | 0%      |       1188 | 2018-01-01 00:00:00 | 2022-03-31 00:00:00 |
| Doc Status          | varchar(5)     | NO         |            |           |               | 0%      |          3 | —                   | —                   |
| gpinstance          | varchar(5)     | NO         |            |           |               | 0%      |          7 | —                   | —                   |
| revenue_period      | date           | YES        |            |           |               | 0%      |        117 | 2017-01-01          | 2026-09-01          |

---

### dbo.IncomeStatement_details {#dbo-incomestatement-details}

| Property | Value |
|---|---|
| Full name | `[dbo].[IncomeStatement_details]` |
| Row count | 2,721,958 |
| Total size | 1.5 GB |
| Used size | 1.5 GB |
| Created | 2026-03-06 08:49 |
| Schema modified | 2026-03-06 08:49 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                  | Max                 |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------|---------------------|
| Country                     | varchar(5)    | NO         |            |           |               | 0%      |          7 | —                    | —                   |
| Budget ID                   | varchar(2)    | NO         |            |           |               | 0%      |          1 | —                    | —                   |
| EBITDA                      | varchar(31)   | YES        |            |           |               | 0%      |          4 | —                    | —                   |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |         39 | —                    | —                   |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |       5706 | —                    | —                   |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |         17 | —                    | —                   |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |         39 | —                    | —                   |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |        113 | —                    | —                   |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |        237 | —                    | —                   |
| Budget Group                | varchar(31)   | YES        |            |           |               | 0%      |        162 | —                    | —                   |
| Department                  | varchar(21)   | YES        |            |           |               | 0%      |         45 | —                    | —                   |
| Class                       | varchar(21)   | YES        |            |           |               | 0%      |         28 | —                    | —                   |
| Posting Type                | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                    | —                   |
| Account Type                | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                    | —                   |
| ACTIVE                      | tinyint       | NO         |            |           |               | 0%      |          2 | 0                    | 1                   |
| Journal Entry               | int           | NO         |            |           |               | 0%      |    1702298 | 1                    | 2678557             |
| Series                      | varchar(100)  | YES        |            |           |               | 0%      |          5 | —                    | —                   |
| TRX Date                    | datetime      | YES        |            |           |               | 0%      |       6865 | 2006-06-30 00:00:00  | 2026-03-04 00:00:00 |
| Last Date Edited            | datetime      | YES        |            |           |               | 0%      |        151 | 1900-01-01 00:00:00  | 2026-03-05 00:00:00 |
| FC Amount                   | numeric(20,5) | YES        |            |           |               | 0%      |     367011 | -666800000933.32000  | 666800000933.32000  |
| RC Amount                   | numeric(38,6) | YES        |            |           |               | 0%      |     943473 | -600334377040.288062 | 600334377040.288062 |
| Batch Source                | varchar(15)   | YES        |            |           |               | 100%    |          1 | —                    | —                   |
| Currency ID                 | varchar(15)   | YES        |            |           |               | 0%      |          4 | —                    | —                   |
| Description                 | varchar(31)   | YES        |            |           |               | 0%      |     182823 | —                    | —                   |
| Document Status             | varchar(100)  | YES        |            |           |               | 0%      |          3 | —                    | —                   |
| Intercompany ID             | varchar(5)    | YES        |            |           |               | 100%    |          7 | —                    | —                   |
| Originating Company ID      | varchar(5)    | YES        |            |           |               | 0%      |          7 | —                    | —                   |
| Last User                   | varchar(15)   | YES        |            |           |               | 0%      |        100 | —                    | —                   |
| User Who Posted             | varchar(15)   | YES        |            |           |               | 0%      |         80 | —                    | —                   |
| Modified Date               | datetime      | YES        |            |           |               | 0%      |        221 | 2011-11-03 00:00:00  | 2025-07-08 00:00:00 |
| Originating Control Number  | varchar(21)   | YES        |            |           |               | 0%      |    1810962 | —                    | —                   |
| Originating Document Number | varchar(21)   | YES        |            |           |               | 0%      |    1820293 | —                    | —                   |
| Originating Journal Entry   | int           | YES        |            |           |               | 0%      |      22821 | 0                    | 2677617             |
| Sequence Number             | numeric(19,5) | NO         |            |           |               | 0%      |       2859 | 15.00000             | 5040500.00000       |
| Source Document             | varchar(11)   | YES        |            |           |               | 0%      |         25 | —                    | —                   |
| Transaction Type            | varchar(100)  | YES        |            |           |               | 100%    |          2 | —                    | —                   |
| Voided                      | varchar(100)  | YES        |            |           |               | 0%      |          2 | —                    | —                   |
| Batch Number                | varchar(15)   | YES        |            |           |               | 100%    |        241 | —                    | —                   |
| Originating TRX Source      | varchar(13)   | YES        |            |           |               | 0%      |     141648 | —                    | —                   |
| TRX Source                  | varchar(13)   | YES        |            |           |               | 0%      |     131945 | —                    | —                   |
| Originating Source          | varchar(15)   | YES        |            |           |               | 100%    |       1405 | —                    | —                   |
| Reference                   | varchar(31)   | YES        |            |           |               | 0%      |     285158 | —                    | —                   |
| Originating Master ID       | varchar(31)   | YES        |            |           |               | 0%      |      24888 | —                    | —                   |
| Originating Master Name     | varchar(65)   | YES        |            |           |               | 0%      |      36872 | —                    | —                   |
| Originating Sequence Number | int           | NO         |            |           |               | 0%      |        443 | 0                    | 5636096             |
| Originating TRX Type        | varchar(100)  | YES        |            |           |               | 0%      |          4 | —                    | —                   |
| fiscal_year                 | smallint      | YES        |            |           |               | 0%      |         21 | 2006                 | 2026                |
| fiscal_quarter              | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                    | —                   |
| fiscal_period               | smallint      | YES        |            |           |               | 0%      |         12 | 1                    | 12                  |
| calendar_year               | smallint      | YES        |            |           |               | 0%      |         21 | 2006                 | 2026                |
| calendar_quarter            | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                    | —                   |
| calendar_month              | smallint      | YES        |            |           |               | 0%      |         12 | 1                    | 12                  |
| month_name                  | varchar(9)    | YES        |            |           |               | 0%      |         12 | —                    | —                   |

---

### dbo.IncomeStatement_details_cogeco {#dbo-incomestatement-details-cogeco}

| Property | Value |
|---|---|
| Full name | `[dbo].[IncomeStatement_details_cogeco]` |
| Row count | 2,378,459 |
| Total size | 1.3 GB |
| Used size | 1.3 GB |
| Created | 2026-03-06 08:50 |
| Schema modified | 2026-03-06 08:50 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                  | Max                 |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------|---------------------|
| Country                     | varchar(5)    | NO         |            |           |               | 0%      |          5 | —                    | —                   |
| Budget ID                   | varchar(2)    | NO         |            |           |               | 0%      |          1 | —                    | —                   |
| EBITDA                      | varchar(31)   | YES        |            |           |               | 0%      |          4 | —                    | —                   |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |         36 | —                    | —                   |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |       5486 | —                    | —                   |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |         15 | —                    | —                   |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |         36 | —                    | —                   |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |        109 | —                    | —                   |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |        232 | —                    | —                   |
| Budget Group                | varchar(31)   | YES        |            |           |               | 0%      |        155 | —                    | —                   |
| Department                  | varchar(21)   | YES        |            |           |               | 0%      |         45 | —                    | —                   |
| Class                       | varchar(21)   | YES        |            |           |               | 0%      |         24 | —                    | —                   |
| Posting Type                | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                    | —                   |
| Account Type                | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                    | —                   |
| ACTIVE                      | tinyint       | NO         |            |           |               | 0%      |          2 | 0                    | 1                   |
| Journal Entry               | int           | NO         |            |           |               | 0%      |    1612942 | 1                    | 2678557             |
| Series                      | varchar(100)  | YES        |            |           |               | 0%      |          5 | —                    | —                   |
| TRX Date                    | datetime      | YES        |            |           |               | 0%      |       6792 | 2006-07-01 00:00:00  | 2026-03-07 00:00:00 |
| Last Date Edited            | datetime      | YES        |            |           |               | 0%      |        144 | 1900-01-01 00:00:00  | 2026-03-05 00:00:00 |
| FC Amount                   | numeric(20,5) | YES        |            |           |               | 0%      |     333913 | -666800000933.32000  | 666800000933.32000  |
| RC Amount                   | numeric(38,6) | YES        |            |           |               | 0%      |    1121785 | -666800000933.320000 | 666800000933.320000 |
| Batch Source                | varchar(15)   | YES        |            |           |               | 100%    |          1 | —                    | —                   |
| Currency ID                 | varchar(15)   | YES        |            |           |               | 0%      |          4 | —                    | —                   |
| Description                 | varchar(31)   | YES        |            |           |               | 0%      |     152488 | —                    | —                   |
| Document Status             | varchar(100)  | YES        |            |           |               | 0%      |          3 | —                    | —                   |
| Intercompany ID             | varchar(5)    | YES        |            |           |               | 100%    |          5 | —                    | —                   |
| Originating Company ID      | varchar(5)    | YES        |            |           |               | 0%      |          7 | —                    | —                   |
| Last User                   | varchar(15)   | YES        |            |           |               | 0%      |         99 | —                    | —                   |
| User Who Posted             | varchar(15)   | YES        |            |           |               | 0%      |         79 | —                    | —                   |
| Modified Date               | datetime      | YES        |            |           |               | 0%      |        218 | 2011-11-03 00:00:00  | 2025-07-08 00:00:00 |
| Originating Control Number  | varchar(21)   | YES        |            |           |               | 0%      |    1578852 | —                    | —                   |
| Originating Document Number | varchar(21)   | YES        |            |           |               | 0%      |    1581478 | —                    | —                   |
| Originating Journal Entry   | int           | YES        |            |           |               | 0%      |      13052 | 0                    | 2677617             |
| Sequence Number             | numeric(19,5) | NO         |            |           |               | 0%      |       2631 | 15.00000             | 5033500.00000       |
| Source Document             | varchar(11)   | YES        |            |           |               | 0%      |         25 | —                    | —                   |
| Transaction Type            | varchar(100)  | YES        |            |           |               | 100%    |          2 | —                    | —                   |
| Voided                      | varchar(100)  | YES        |            |           |               | 0%      |          2 | —                    | —                   |
| Batch Number                | varchar(15)   | YES        |            |           |               | 100%    |        277 | —                    | —                   |
| Originating TRX Source      | varchar(13)   | YES        |            |           |               | 0%      |     135923 | —                    | —                   |
| TRX Source                  | varchar(13)   | YES        |            |           |               | 0%      |     127518 | —                    | —                   |
| Originating Source          | varchar(15)   | YES        |            |           |               | 99%     |       1337 | —                    | —                   |
| Reference                   | varchar(31)   | YES        |            |           |               | 0%      |     241707 | —                    | —                   |
| Originating Master ID       | varchar(31)   | YES        |            |           |               | 0%      |      22425 | —                    | —                   |
| Originating Master Name     | varchar(65)   | YES        |            |           |               | 0%      |      32576 | —                    | —                   |
| Originating Sequence Number | int           | NO         |            |           |               | 0%      |        443 | 0                    | 5636096             |
| Originating TRX Type        | varchar(100)  | YES        |            |           |               | 0%      |          4 | —                    | —                   |
| FIscalYear                  | smallint      | YES        |            |           |               | 0%      |         21 | 2006                 | 2026                |
| FiscalQuarter               | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                    | —                   |
| FiscalPeriod                | smallint      | YES        |            |           |               | 0%      |         12 | 1                    | 12                  |
| CalendarYear                | smallint      | YES        |            |           |               | 0%      |         21 | 2006                 | 2026                |
| CalendarQuarter             | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                    | —                   |
| CalendarMonth               | smallint      | YES        |            |           |               | 0%      |         12 | 1                    | 12                  |
| MonthName                   | varchar(9)    | YES        |            |           |               | 0%      |         12 | —                    | —                   |

---

### dbo.IncomeStatement_details_Filtered {#dbo-incomestatement-details-filtered}

| Property | Value |
|---|---|
| Full name | `[dbo].[IncomeStatement_details_Filtered]` |
| Row count | 240,641 |
| Total size | 129.8 MB |
| Used size | 129.8 MB |
| Created | 2026-03-06 08:02 |
| Schema modified | 2026-03-06 08:02 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| Country                     | varchar(5)    | NO         |            |           |               | 0%      |          6 | —                   | —                   |
| Budget ID                   | varchar(2)    | NO         |            |           |               | 0%      |          1 | —                   | —                   |
| EBITDA                      | varchar(31)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |         13 | —                   | —                   |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |        469 | —                   | —                   |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |          6 | —                   | —                   |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |         29 | —                   | —                   |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |         19 | —                   | —                   |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |         24 | —                   | —                   |
| Budget Group                | varchar(31)   | YES        |            |           |               | 0%      |         30 | —                   | —                   |
| Department                  | varchar(21)   | YES        |            |           |               | 0%      |          7 | —                   | —                   |
| Class                       | varchar(21)   | YES        |            |           |               | 0%      |         13 | —                   | —                   |
| Posting Type                | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Account Type                | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| ACTIVE                      | tinyint       | NO         |            |           |               | 0%      |          2 | 0                   | 1                   |
| Journal Entry               | int           | NO         |            |           |               | 0%      |     171875 | 1                   | 2575732             |
| Series                      | varchar(100)  | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| TRX Date                    | datetime      | YES        |            |           |               | 0%      |       1095 | 2018-09-02 00:00:00 | 2021-08-31 00:00:00 |
| Last Date Edited            | datetime      | YES        |            |           |               | 0%      |         11 | 1900-01-01 00:00:00 | 2021-08-31 00:00:00 |
| FC Amount                   | numeric(20,5) | YES        |            |           |               | 0%      |      59688 | -3380154.81000      | 3380154.81000       |
| RC Amount                   | numeric(38,6) | YES        |            |           |               | 0%      |     124046 | -2764998.070019     | 2764998.070019      |
| Batch Source                | varchar(15)   | YES        |            |           |               | 100%    |          1 | —                   | —                   |
| Currency ID                 | varchar(15)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Description                 | varchar(31)   | YES        |            |           |               | 0%      |       8896 | —                   | —                   |
| Document Status             | varchar(100)  | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| Intercompany ID             | varchar(5)    | YES        |            |           |               | 100%    |          3 | —                   | —                   |
| Originating Company ID      | varchar(5)    | YES        |            |           |               | 0%      |          6 | —                   | —                   |
| Last User                   | varchar(15)   | YES        |            |           |               | 0%      |         22 | —                   | —                   |
| User Who Posted             | varchar(15)   | YES        |            |           |               | 0%      |         14 | —                   | —                   |
| Modified Date               | datetime      | YES        |            |           |               | 0%      |         49 | 2011-11-03 00:00:00 | 2025-07-08 00:00:00 |
| Originating Control Number  | varchar(21)   | YES        |            |           |               | 0%      |     152043 | —                   | —                   |
| Originating Document Number | varchar(21)   | YES        |            |           |               | 0%      |     152134 | —                   | —                   |
| Originating Journal Entry   | int           | YES        |            |           |               | 0%      |       1818 | 0                   | 2574088             |
| Sequence Number             | numeric(19,5) | NO         |            |           |               | 0%      |        116 | 100.00000           | 5016000.00000       |
| Source Document             | varchar(11)   | YES        |            |           |               | 0%      |          6 | —                   | —                   |
| Transaction Type            | varchar(100)  | YES        |            |           |               | 100%    |          2 | —                   | —                   |
| Voided                      | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Batch Number                | varchar(15)   | YES        |            |           |               | 100%    |         75 | —                   | —                   |
| Originating TRX Source      | varchar(13)   | YES        |            |           |               | 0%      |      22040 | —                   | —                   |
| TRX Source                  | varchar(13)   | YES        |            |           |               | 0%      |      20927 | —                   | —                   |
| Originating Source          | varchar(15)   | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Reference                   | varchar(31)   | YES        |            |           |               | 0%      |      24547 | —                   | —                   |
| Originating Master ID       | varchar(31)   | YES        |            |           |               | 0%      |       4221 | —                   | —                   |
| Originating Master Name     | varchar(65)   | YES        |            |           |               | 0%      |       4643 | —                   | —                   |
| Originating Sequence Number | int           | NO         |            |           |               | 0%      |        185 | 0                   | 5636096             |
| Originating TRX Type        | varchar(100)  | YES        |            |           |               | 0%      |          3 | —                   | —                   |
| FiscalYear                  | smallint      | YES        |            |           |               | 0%      |          4 | 2019                | 2022                |
| FiscalQuarter               | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| FiscalPeriod                | smallint      | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| CalendarYear                | smallint      | YES        |            |           |               | 0%      |          4 | 2018                | 2021                |
| CalendarQuarter             | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| CalendarMonth               | smallint      | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| MonthName                   | varchar(9)    | YES        |            |           |               | 0%      |         12 | —                   | —                   |

---

### dbo.IncomeStatement_details_Filtered_Cogeco {#dbo-incomestatement-details-filtered-cogeco}

| Property | Value |
|---|---|
| Full name | `[dbo].[IncomeStatement_details_Filtered_Cogeco]` |
| Row count | 115,183 |
| Total size | 63.9 MB |
| Used size | 63.9 MB |
| Created | 2026-03-06 08:02 |
| Schema modified | 2026-03-06 08:02 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| Country                     | varchar(5)    | NO         |            |           |               | 0%      |          6 | —                   | —                   |
| Budget ID                   | varchar(2)    | NO         |            |           |               | 0%      |          1 | —                   | —                   |
| EBITDA                      | varchar(31)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |         14 | —                   | —                   |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |        325 | —                   | —                   |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |          6 | —                   | —                   |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |         29 | —                   | —                   |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |         23 | —                   | —                   |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |         24 | —                   | —                   |
| Budget Group                | varchar(31)   | YES        |            |           |               | 0%      |         28 | —                   | —                   |
| Department                  | varchar(21)   | YES        |            |           |               | 0%      |          6 | —                   | —                   |
| Class                       | varchar(21)   | YES        |            |           |               | 0%      |         15 | —                   | —                   |
| Posting Type                | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Account Type                | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| ACTIVE                      | tinyint       | NO         |            |           |               | 0%      |          1 | 1                   | 1                   |
| Journal Entry               | int           | NO         |            |           |               | 0%      |      95255 | 6                   | 2678557             |
| Series                      | varchar(100)  | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| TRX Date                    | datetime      | YES        |            |           |               | 0%      |       1397 | 2022-05-01 00:00:00 | 2026-03-07 00:00:00 |
| Last Date Edited            | datetime      | YES        |            |           |               | 0%      |         60 | 1900-01-01 00:00:00 | 2026-03-05 00:00:00 |
| FC Amount                   | numeric(20,5) | YES        |            |           |               | 0%      |      44553 | -3498898.59000      | 2456019.25000       |
| RC Amount                   | numeric(38,6) | YES        |            |           |               | 0%      |      92155 | -3498898.590000     | 3312187.560550      |
| Batch Source                | varchar(15)   | YES        |            |           |               | 99%     |          1 | —                   | —                   |
| Currency ID                 | varchar(15)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Description                 | varchar(31)   | YES        |            |           |               | 0%      |       5393 | —                   | —                   |
| Document Status             | varchar(100)  | YES        |            |           |               | 0%      |          3 | —                   | —                   |
| Intercompany ID             | varchar(5)    | YES        |            |           |               | 99%     |          6 | —                   | —                   |
| Originating Company ID      | varchar(5)    | YES        |            |           |               | 0%      |          7 | —                   | —                   |
| Last User                   | varchar(15)   | YES        |            |           |               | 0%      |         17 | —                   | —                   |
| User Who Posted             | varchar(15)   | YES        |            |           |               | 0%      |         13 | —                   | —                   |
| Modified Date               | datetime      | YES        |            |           |               | 0%      |         43 | 2011-11-03 00:00:00 | 2025-07-08 00:00:00 |
| Originating Control Number  | varchar(21)   | YES        |            |           |               | 0%      |      81916 | —                   | —                   |
| Originating Document Number | varchar(21)   | YES        |            |           |               | 0%      |      81932 | —                   | —                   |
| Originating Journal Entry   | int           | YES        |            |           |               | 0%      |       1163 | 0                   | 2677617             |
| Sequence Number             | numeric(19,5) | NO         |            |           |               | 0%      |         54 | 100.00000           | 5003000.00000       |
| Source Document             | varchar(11)   | YES        |            |           |               | 0%      |          6 | —                   | —                   |
| Transaction Type            | varchar(100)  | YES        |            |           |               | 99%     |          2 | —                   | —                   |
| Voided                      | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Batch Number                | varchar(15)   | YES        |            |           |               | 99%     |         65 | —                   | —                   |
| Originating TRX Source      | varchar(13)   | YES        |            |           |               | 0%      |      15074 | —                   | —                   |
| TRX Source                  | varchar(13)   | YES        |            |           |               | 0%      |      16133 | —                   | —                   |
| Originating Source          | varchar(15)   | YES        |            |           |               | 89%     |       1405 | —                   | —                   |
| Reference                   | varchar(31)   | YES        |            |           |               | 0%      |      15620 | —                   | —                   |
| Originating Master ID       | varchar(31)   | YES        |            |           |               | 0%      |       1695 | —                   | —                   |
| Originating Master Name     | varchar(65)   | YES        |            |           |               | 0%      |       1924 | —                   | —                   |
| Originating Sequence Number | int           | NO         |            |           |               | 0%      |         67 | 0                   | 1671168             |
| Originating TRX Type        | varchar(100)  | YES        |            |           |               | 0%      |          3 | —                   | —                   |
| FIscalYear                  | smallint      | YES        |            |           |               | 0%      |          5 | 2022                | 2026                |
| FiscalQuarter               | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| FiscalPeriod                | smallint      | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| CalendarYear                | smallint      | YES        |            |           |               | 0%      |          5 | 2022                | 2026                |
| CalendarQuarter             | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| CalendarMonth               | smallint      | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| MonthName                   | varchar(9)    | YES        |            |           |               | 0%      |         12 | —                   | —                   |
| dh_mapping                  | varchar(255)  | YES        |            |           |               | 0%      |          4 | —                   | —                   |

---

### dbo.Intercompany {#dbo-intercompany}

| Property | Value |
|---|---|
| Full name | `[dbo].[Intercompany]` |
| Row count | 36,795 |
| Total size | 18.3 MB |
| Used size | 18.2 MB |
| Created | 2026-03-06 09:08 |
| Schema modified | 2026-03-06 09:08 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| Country                     | varchar(5)    | NO         |            |           |               | 0%      |          3 | —                   | —                   |
| Budget ID                   | varchar(2)    | NO         |            |           |               | 0%      |          1 | —                   | —                   |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |          3 | —                   | —                   |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |          3 | —                   | —                   |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Budget Group                | varchar(31)   | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| EBITDA                      | varchar(31)   | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Department                  | varchar(21)   | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Class                       | varchar(21)   | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Posting Type                | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Account Type                | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| ACTIVE                      | tinyint       | NO         |            |           |               | 0%      |          2 | 0                   | 1                   |
| Journal Entry               | int           | NO         |            |           |               | 0%      |      32809 | 1                   | 1780438             |
| Series                      | varchar(100)  | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| TRX Date                    | datetime      | YES        |            |           |               | 0%      |       1442 | 2006-06-30 00:00:00 | 2017-03-07 00:00:00 |
| Last Date Edited            | datetime      | YES        |            |           |               | 0%      |         14 | 1900-01-01 00:00:00 | 2017-08-31 00:00:00 |
| FC Amount                   | numeric(20,5) | YES        |            |           |               | 0%      |      24725 | -74358544.61000     | 33599936.24000      |
| RC Amount                   | numeric(38,6) | YES        |            |           |               | 0%      |      26331 | -72631017.158202    | 33828928.020745     |
| Batch Source                | varchar(15)   | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Currency ID                 | varchar(15)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Description                 | varchar(31)   | YES        |            |           |               | 0%      |       6872 | —                   | —                   |
| Document Status             | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Intercompany ID             | varchar(5)    | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Originating Company ID      | varchar(5)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Corresponding Unit          | varchar(5)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Last User                   | varchar(15)   | YES        |            |           |               | 0%      |         18 | —                   | —                   |
| User Who Posted             | varchar(15)   | YES        |            |           |               | 0%      |         19 | —                   | —                   |
| Modified Date               | datetime      | YES        |            |           |               | 0%      |          3 | 2013-10-24 00:00:00 | 2017-03-20 00:00:00 |
| Originating Control Number  | varchar(21)   | YES        |            |           |               | 0%      |       4777 | —                   | —                   |
| Originating Document Number | varchar(21)   | YES        |            |           |               | 0%      |       4692 | —                   | —                   |
| Originating Journal Entry   | int           | YES        |            |           |               | 0%      |      12594 | 0                   | 1128671             |
| Sequence Number             | numeric(19,5) | NO         |            |           |               | 0%      |       9395 | 500.00000           | 5080500.00000       |
| Source Document             | varchar(11)   | YES        |            |           |               | 0%      |         17 | —                   | —                   |
| Transaction Type            | varchar(100)  | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Voided                      | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Batch Number                | varchar(15)   | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Originating TRX Source      | varchar(13)   | YES        |            |           |               | 0%      |       7545 | —                   | —                   |
| TRX Source                  | varchar(13)   | YES        |            |           |               | 0%      |       6988 | —                   | —                   |
| Originating Source          | varchar(15)   | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Reference                   | varchar(31)   | YES        |            |           |               | 0%      |      11547 | —                   | —                   |
| Originating Master ID       | varchar(31)   | YES        |            |           |               | 0%      |        101 | —                   | —                   |
| Originating Master Name     | varchar(65)   | YES        |            |           |               | 0%      |       2073 | —                   | —                   |
| Originating Sequence Number | int           | NO         |            |           |               | 0%      |         18 | 0                   | 344064              |
| Originating TRX Type        | varchar(100)  | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Originating Amt             | numeric(20,5) | YES        |            |           |               | 0%      |      18212 | -74358544.61000     | 33599936.24000      |
| fiscal_period               | smallint      | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| fiscal_quarter              | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| fiscal_year                 | smallint      | YES        |            |           |               | 0%      |         10 | 2006                | 2017                |

---

### dbo.INVCOST {#dbo-invcost}

| Property | Value |
|---|---|
| Full name | `[dbo].[INVCOST]` |
| Row count | 2,511 |
| Total size | 0.5 MB |
| Used size | 0.4 MB |
| Created | 2011-02-28 13:44 |
| Schema modified | 2011-02-28 13:44 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column   | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min     | Max         |
|----------|---------------|------------|------------|-----------|---------------|---------|------------|---------|-------------|
| ITEMNMBR | char(31)      | NO         |            |           |               | 0%      |       2511 | —       | —           |
| ITEMDESC | char(101)     | NO         |            |           |               | 0%      |       2406 | —       | —           |
| STNDCOST | numeric(19,5) | NO         |            |           |               | 0%      |        319 | 0.00000 | 47500.00000 |
| CURRCOST | numeric(19,5) | NO         |            |           |               | 0%      |        363 | 0.00000 | 47500.00000 |

---

### dbo.Invoices {#dbo-invoices}

| Property | Value |
|---|---|
| Full name | `[dbo].[Invoices]` |
| Row count | 20,641,179 |
| Total size | 1.1 GB |
| Used size | 1.1 GB |
| Created | 2026-03-05 10:22 |
| Schema modified | 2026-03-05 10:22 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column     | Type     | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max       |
|------------|----------|------------|------------|-----------|---------------|---------|------------|-------|-----------|
| sopnumbe   | char(21) | NO         |            |           |               | 0%      |     988189 | —     | —         |
| lnitmseq   | int      | NO         |            |           |               | 0%      |      27111 | 8192  | 444006400 |
| service_id | char(21) | NO         |            |           |               | 0%      |      76712 | —     | —         |

---

### dbo.MYIS_Games {#dbo-myis-games}

| Property | Value |
|---|---|
| Full name | `[dbo].[MYIS_Games]` |
| Row count | 1,167 |
| Total size | 0.3 MB |
| Used size | 0.2 MB |
| Created | 2011-05-31 11:01 |
| Schema modified | 2011-05-31 11:01 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column          | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min     | Max       |
|-----------------|---------------|------------|------------|-----------|---------------|---------|------------|---------|-----------|
| service_id      | float(53)     | YES        |            |           |               | 0%      |       1167 | 94300.0 | 2399493.0 |
| nickname        | nvarchar(255) | YES        |            |           |               | 0%      |       1167 | —       | —         |
| city            | nvarchar(255) | YES        |            |           |               | 0%      |          7 | —       | —         |
| Game Studio     | nvarchar(255) | YES        |            |           |               | 0%      |          9 | —       | —         |
| Game            | nvarchar(255) | YES        |            |           |               | 1%      |         19 | —       | —         |
| Server Function | nvarchar(255) | YES        |            |           |               | 7%      |          5 | —       | —         |
| F7              | nvarchar(255) | YES        |            |           |               | 100%    |          1 | —       | —         |

---

### dbo.MYIS_Invoices {#dbo-myis-invoices}

| Property | Value |
|---|---|
| Full name | `[dbo].[MYIS_Invoices]` |
| Row count | 20,078 |
| Total size | 8.2 MB |
| Used size | 8.2 MB |
| Created | 2011-06-28 15:30 |
| Schema modified | 2011-06-28 15:30 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column               | Type          | Nullable   | Identity   | Default   | Description   | NULL%   | Distinct   | Min                 | Max                 |
|----------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| Customer Number      | varchar(15)   | YES        |            |           |               | 0%      | 1          | —                   | —                   |
| Document Type        | varchar(11)   | NO         |            |           |               | 0%      | 2          | —                   | —                   |
| Document Number      | varchar(21)   | YES        |            |           |               | 0%      | 847        | —                   | —                   |
| Current Server Name  | varchar(255)  | YES        |            |           |               | 10%     | 2909       | —                   | —                   |
| Invoice Start Date   | datetime      | NO         |            |           |               | 0%      | 527        | 2009-06-09 00:00:00 | 2011-07-24 00:00:00 |
| Invoice End Date     | datetime      | NO         |            |           |               | 0%      | 514        | 2009-07-08 00:00:00 | 2011-08-23 00:00:00 |
| Contract Number      | varchar(11)   | YES        |            |           |               | 0%      | 3631       | —                   | —                   |
| Paid                 | varchar(3)    | NO         |            |           |               | 0%      | 2          | —                   | —                   |
| SalesAmount          | numeric(38,5) | YES        |            |           |               | 0%      | 628        | -6216.00000         | 2082.17000          |
| TaxAmount            | numeric(38,5) | YES        |            |           |               | 0%      | 1          | 0.00000             | 0.00000             |
| TotalAmount          | numeric(38,5) | YES        |            |           |               | 0%      | 628        | -6216.00000         | 2082.17000          |
| ID                   | char(21)      | YES        |            |           |               | 10%     | 2596       | —                   | —                   |
| Due Date             | datetime      | NO         |            |           |               | 0%      | 427        | 2009-06-30 00:00:00 | 2011-07-23 00:00:00 |
| Amount Due           | numeric(19,5) | YES        |            |           |               | 0%      | 63         | -909.55000          | 78770.99000         |
| COMMENT_1            | char(51)      | YES        |            |           |               | 26%     | 1894       | —                   | —                   |
| Online_Date          | date          | YES        |            |           |               | 10%     | 163        | 2009-06-09          | 2011-06-10          |
| location             | ntext         | YES        |            |           |               | ?       | ?          | —                   | —                   |
| Cancel_Date          | date          | YES        |            |           |               | 56%     | 56         | 2009-09-01          | 2011-06-25          |
| Current Status       | varchar(9)    | NO         |            |           |               | 0%      | 2          | —                   | —                   |
| Original Server Name | nvarchar(255) | YES        |            |           |               | 46%     | 1154       | —                   | —                   |
| Game Studio          | nvarchar(255) | YES        |            |           |               | 46%     | 9          | —                   | —                   |
| Service Type         | nvarchar(255) | YES        |            |           |               | 51%     | 5          | —                   | —                   |
| Game_Location        | nvarchar(278) | YES        |            |           |               | 54%     | 33         | —                   | —                   |
| Game                 | nvarchar(255) | YES        |            |           |               | 46%     | 18         | —                   | —                   |

---

### dbo.nbf_sop30300_deferred_normalized {#dbo-nbf-sop30300-deferred-normalized}

| Property | Value |
|---|---|
| Full name | `[dbo].[nbf_sop30300_deferred_normalized]` |
| Row count | 246,455 |
| Total size | 87.7 MB |
| Used size | 87.5 MB |
| Created | 2026-03-07 04:37 |
| Schema modified | 2026-03-07 04:37 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column          | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| soptype         | smallint      | NO         |            |           |               | 0%      |          2 | 3                   | 4                   |
| sopnumbe        | char(21)      | NO         |            |           |               | 0%      |      25803 | —                   | —                   |
| lnitmseq        | int           | NO         |            |           |               | 0%      |        285 | 1024                | 6029312             |
| cmpntseq        | int           | NO         |            |           |               | 0%      |          1 | 0                   | 0                   |
| xtndprce        | numeric(19,5) | NO         |            |           |               | 0%      |      20779 | -3330.27000         | 944999999999.99000  |
| oxtndprc        | numeric(19,5) | NO         |            |           |               | 0%      |      17498 | -4040.41000         | 944999999999.99000  |
| remprice        | numeric(19,5) | NO         |            |           |               | 0%      |      20777 | -3330.27000         | 944999999999.99000  |
| oreprice        | numeric(19,5) | NO         |            |           |               | 0%      |      17497 | -4040.41000         | 944999999999.99000  |
| extdcost        | numeric(19,5) | NO         |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| orextcst        | numeric(19,5) | NO         |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| mrkdnamt        | numeric(19,5) | NO         |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| ormrkdam        | numeric(19,5) | NO         |            |           |               | 0%      |          1 | 0.00000             | 0.00000             |
| mrkdnpct        | smallint      | NO         |            |           |               | 0%      |          1 | 0                   | 0                   |
| mrkdntyp        | smallint      | NO         |            |           |               | 0%      |          1 | 0                   | 0                   |
| taxamnt         | numeric(19,5) | NO         |            |           |               | 0%      |       8972 | -429.24000          | 189000000000.00000  |
| ortaxamt        | numeric(19,5) | NO         |            |           |               | 0%      |       8908 | -512.05000          | 189000000000.00000  |
| contstartdte    | datetime      | NO         |            |           |               | 0%      |       2124 | 1900-01-01 00:00:00 | 2026-03-01 00:00:00 |
| contenddte      | datetime      | NO         |            |           |               | 0%      |       2037 | 1900-01-01 00:00:00 | 2103-08-31 00:00:00 |
| totaldays       | numeric(24,6) | YES        |            |           |               | 0%      |        217 | -6.000000           | 32902.000000        |
| PeriodStart     | datetime      | YES        |            |           |               | 0%      |       2148 | 1900-01-01 00:00:00 | 2027-01-01 00:00:00 |
| PeriodEnd       | datetime      | YES        |            |           |               | 0%      |       2067 | 1900-01-01 00:00:00 | 2027-01-19 00:00:00 |
| PeriodDays      | numeric(26,6) | YES        |            |           |               | 0%      |         61 | -6.000000           | 31.000000           |
| xtndprce_period | numeric(38,6) | YES        |            |           |               | 0%      |      30531 | -3330.270000        | 944999999999.990000 |
| oxtndprc_period | numeric(38,6) | YES        |            |           |               | 0%      |      27144 | -4040.410000        | 944999999999.990000 |
| remprice_period | numeric(38,6) | YES        |            |           |               | 0%      |      30530 | -3330.270000        | 944999999999.990000 |
| oreprice_period | numeric(38,6) | YES        |            |           |               | 0%      |      27141 | -4040.410000        | 944999999999.990000 |
| extdcost_period | numeric(38,6) | YES        |            |           |               | 0%      |          1 | 0.000000            | 0.000000            |
| orextcst_period | numeric(38,6) | YES        |            |           |               | 0%      |          1 | 0.000000            | 0.000000            |
| mrkdnamt_period | numeric(38,6) | YES        |            |           |               | 0%      |          1 | 0.000000            | 0.000000            |
| ormrkdam_period | numeric(38,6) | YES        |            |           |               | 0%      |          1 | 0.000000            | 0.000000            |
| taxamnt_period  | numeric(38,6) | YES        |            |           |               | 0%      |      18821 | -374.270000         | 189000000000.000000 |
| ortaxamt_period | numeric(38,6) | YES        |            |           |               | 0%      |      18743 | -512.050000         | 189000000000.000000 |

---

### dbo.OPEX {#dbo-opex}

| Property | Value |
|---|---|
| Full name | `[dbo].[OPEX]` |
| Row count | 27,605 |
| Total size | 29.4 MB |
| Used size | 29.4 MB |
| Created | 2026-03-06 09:20 |
| Schema modified | 2026-03-06 09:20 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| Country                     | varchar(5)    | NO         |            |           |               | 0%      |          4 | —                   | —                   |
| Budget ID                   | varchar(2)    | NO         |            |           |               | 0%      |          1 | —                   | —                   |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |         12 | —                   | —                   |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |        332 | —                   | —                   |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |         11 | —                   | —                   |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |         18 | —                   | —                   |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |         63 | —                   | —                   |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |         11 | —                   | —                   |
| Journal Entry               | int           | NO         |            |           |               | 0%      |      22573 | 4                   | 2348093             |
| Series                      | varchar(100)  | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| TRX Date                    | datetime      | YES        |            |           |               | 0%      |       2736 | 2006-07-01 00:00:00 | 2025-11-03 00:00:00 |
| Last Date Edited            | datetime      | YES        |            |           |               | 0%      |         22 | 2007-06-30 00:00:00 | 2025-11-04 00:00:00 |
| Credit Amount               | numeric(19,5) | NO         |            |           |               | 0%      |       2276 | 0.00000             | 3864142.62000       |
| Debit Amount                | numeric(19,5) | NO         |            |           |               | 0%      |      11801 | 0.00000             | 3832587.05000       |
| FC Amount                   | numeric(20,5) | YES        |            |           |               | 0%      |      14075 | -3864142.62000      | 3832587.05000       |
| RC Amount                   | numeric(38,6) | YES        |            |           |               | 0%      |      19313 | -3788898.489246     | 3862981.764858      |
| Batch Source                | varchar(15)   | YES        |            |           |               | 100%    |          1 | —                   | —                   |
| Currency ID                 | varchar(15)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Description                 | varchar(31)   | YES        |            |           |               | 0%      |      18490 | —                   | —                   |
| Document Status             | varchar(100)  | YES        |            |           |               | 0%      |          3 | —                   | —                   |
| Intercompany ID             | varchar(5)    | YES        |            |           |               | 100%    |          3 | —                   | —                   |
| Originating Company ID      | varchar(5)    | YES        |            |           |               | 0%      |          5 | —                   | —                   |
| Last User                   | varchar(15)   | YES        |            |           |               | 0%      |         49 | —                   | —                   |
| User Who Posted             | varchar(15)   | YES        |            |           |               | 0%      |         49 | —                   | —                   |
| Modified Date               | datetime      | YES        |            |           |               | 0%      |         25 | 2011-11-03 00:00:00 | 2017-09-01 00:00:00 |
| Originating Control Number  | varchar(21)   | YES        |            |           |               | 0%      |      15403 | —                   | —                   |
| Originating Document Number | varchar(21)   | YES        |            |           |               | 0%      |      15456 | —                   | —                   |
| Originating Journal Entry   | int           | YES        |            |           |               | 0%      |       1692 | 0                   | 2672788             |
| Sequence Number             | numeric(19,5) | NO         |            |           |               | 0%      |        278 | 100.00000           | 5023000.00000       |
| Source Document             | varchar(11)   | YES        |            |           |               | 0%      |         13 | —                   | —                   |
| Transaction Type            | varchar(100)  | YES        |            |           |               | 100%    |          2 | —                   | —                   |
| Voided                      | varchar(100)  | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| Batch Number                | varchar(15)   | YES        |            |           |               | 100%    |          9 | —                   | —                   |
| Originating TRX Source      | varchar(13)   | YES        |            |           |               | 0%      |       9995 | —                   | —                   |
| TRX Source                  | varchar(13)   | YES        |            |           |               | 0%      |      11421 | —                   | —                   |
| Originating Source          | varchar(15)   | YES        |            |           |               | 100%    |          1 | —                   | —                   |
| Reference                   | varchar(31)   | YES        |            |           |               | 0%      |      18509 | —                   | —                   |
| Originating Master ID       | varchar(31)   | YES        |            |           |               | 0%      |       1466 | —                   | —                   |
| Originating Master Name     | varchar(65)   | YES        |            |           |               | 0%      |       1672 | —                   | —                   |
| Originating Sequence Number | int           | NO         |            |           |               | 0%      |        126 | 0                   | 2572288             |
| Originating TRX Type        | varchar(100)  | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| fiscal_Year                 | smallint      | YES        |            |           |               | 0%      |         14 | 2007                | 2026                |
| fiscal_Quarter              | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| fiscal_Period               | smallint      | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| calendar_Year               | smallint      | YES        |            |           |               | 0%      |         15 | 2006                | 2025                |
| calendar_Quarter            | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| calendar_Month              | smallint      | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| month_name                  | varchar(9)    | YES        |            |           |               | 0%      |         12 | —                   | —                   |
| PONUMBER                    | char(17)      | YES        |            |           |               | 95%     |        720 | —                   | —                   |
| ITEMNMBR                    | char(31)      | YES        |            |           |               | 95%     |        171 | —                   | —                   |
| ITEMDESC                    | char(101)     | YES        |            |           |               | 95%     |        211 | —                   | —                   |
| VNDITDSC                    | char(101)     | YES        |            |           |               | 95%     |        230 | —                   | —                   |
| COMMNTID                    | char(15)      | YES        |            |           |               | 95%     |          1 | —                   | —                   |
| LOCNCODE                    | char(11)      | YES        |            |           |               | 95%     |         33 | —                   | —                   |
| Project ID                  | char(31)      | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Project Description         | char(51)      | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| aaTrxDimCodeDescr2          | char(51)      | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Filter                      | varchar(6)    | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Assigned Original Amount    | numeric(38,5) | YES        |            |           |               | 100%    |          0 | NULL                | NULL                |
| Assigned FC Amount          | numeric(38,5) | YES        |            |           |               | 100%    |          0 | NULL                | NULL                |
| Assigned RC Amount          | numeric(38,5) | YES        |            |           |               | 100%    |          0 | NULL                | NULL                |
| GP FC Amount                | numeric(38,5) | YES        |            |           |               | 0%      |      14075 | -3864142.62000      | 3832587.05000       |
| GP RC Amount                | numeric(38,5) | YES        |            |           |               | 0%      |      19312 | -3788898.48925      | 3862981.76486       |

---

### dbo.OPEX_Cogeco {#dbo-opex-cogeco}

| Property | Value |
|---|---|
| Full name | `[dbo].[OPEX_Cogeco]` |
| Row count | 673,508 |
| Total size | 690.6 MB |
| Used size | 690.5 MB |
| Created | 2026-03-06 09:08 |
| Schema modified | 2026-03-06 09:08 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| Country                     | varchar(5)    | NO         |            |           |               | 0%      |          5 | —                   | —                   |
| Budget ID                   | varchar(2)    | NO         |            |           |               | 0%      |          1 | —                   | —                   |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |         27 | —                   | —                   |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |       4763 | —                   | —                   |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |         14 | —                   | —                   |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |         23 | —                   | —                   |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |         88 | —                   | —                   |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |        196 | —                   | —                   |
| Journal Entry               | int           | NO         |            |           |               | 0%      |     371174 | 1                   | 2678557             |
| Series                      | varchar(100)  | YES        |            |           |               | 0%      |          5 | —                   | —                   |
| TRX Date                    | datetime      | YES        |            |           |               | 0%      |       6709 | 2006-06-30 00:00:00 | 2026-03-05 00:00:00 |
| Last Date Edited            | datetime      | YES        |            |           |               | 0%      |        133 | 1900-01-01 00:00:00 | 2026-03-05 00:00:00 |
| Credit Amount               | numeric(19,5) | NO         |            |           |               | 0%      |      53081 | 0.00000             | 301789021.03000     |
| Debit Amount                | numeric(19,5) | NO         |            |           |               | 0%      |     134627 | 0.00000             | 301789021.03000     |
| FC Amount                   | numeric(20,5) | YES        |            |           |               | 0%      |     187707 | -301789021.03000    | 301789021.03000     |
| RC Amount                   | numeric(38,6) | YES        |            |           |               | 12%     |     365562 | -301789021.030000   | 301789021.030000    |
| Batch Source                | varchar(15)   | YES        |            |           |               | 100%    |          1 | —                   | —                   |
| Currency ID                 | varchar(15)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Description                 | varchar(31)   | YES        |            |           |               | 0%      |     179229 | —                   | —                   |
| Document Status             | varchar(100)  | YES        |            |           |               | 0%      |          3 | —                   | —                   |
| Intercompany ID             | varchar(5)    | YES        |            |           |               | 100%    |          5 | —                   | —                   |
| Originating Company ID      | varchar(5)    | YES        |            |           |               | 0%      |          7 | —                   | —                   |
| Last User                   | varchar(15)   | YES        |            |           |               | 0%      |         99 | —                   | —                   |
| User Who Posted             | varchar(15)   | YES        |            |           |               | 0%      |         80 | —                   | —                   |
| Modified Date               | datetime      | YES        |            |           |               | 0%      |        168 | 2011-11-03 00:00:00 | 2025-02-03 00:00:00 |
| Originating Control Number  | varchar(21)   | YES        |            |           |               | 0%      |     213601 | —                   | —                   |
| Originating Document Number | varchar(21)   | YES        |            |           |               | 0%      |     223730 | —                   | —                   |
| Originating Journal Entry   | int           | YES        |            |           |               | 0%      |      17352 | 0                   | 2677617             |
| Sequence Number             | numeric(19,5) | NO         |            |           |               | 0%      |       2782 | 15.00000            | 5040500.00000       |
| Source Document             | varchar(11)   | YES        |            |           |               | 0%      |         25 | —                   | —                   |
| Transaction Type            | varchar(100)  | YES        |            |           |               | 100%    |          2 | —                   | —                   |
| Voided                      | varchar(100)  | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| Batch Number                | varchar(15)   | YES        |            |           |               | 100%    |        257 | —                   | —                   |
| Originating TRX Source      | varchar(13)   | YES        |            |           |               | 0%      |     112833 | —                   | —                   |
| TRX Source                  | varchar(13)   | YES        |            |           |               | 0%      |     111198 | —                   | —                   |
| Originating Source          | varchar(15)   | YES        |            |           |               | 100%    |        750 | —                   | —                   |
| Reference                   | varchar(31)   | YES        |            |           |               | 0%      |     175616 | —                   | —                   |
| Originating Master ID       | varchar(31)   | YES        |            |           |               | 0%      |      15779 | —                   | —                   |
| Originating Master Name     | varchar(65)   | YES        |            |           |               | 0%      |      25053 | —                   | —                   |
| Originating Sequence Number | int           | NO         |            |           |               | 0%      |        443 | 0                   | 5636096             |
| Originating TRX Type        | varchar(100)  | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| FiscalYear                  | smallint      | YES        |            |           |               | 0%      |         21 | 2006                | 2026                |
| FiscalQuarter               | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| FiscalPeriod                | smallint      | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| CalendarYear                | smallint      | YES        |            |           |               | 0%      |         21 | 2006                | 2026                |
| CalendarQuarter             | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| CalendarMonth               | smallint      | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| MonthName                   | varchar(9)    | YES        |            |           |               | 0%      |         12 | —                   | —                   |
| PONUMBER                    | char(17)      | YES        |            |           |               | 98%     |       6965 | —                   | —                   |
| ITEMNMBR                    | char(31)      | YES        |            |           |               | 98%     |       3836 | —                   | —                   |
| ITEMDESC                    | char(101)     | YES        |            |           |               | 98%     |       4586 | —                   | —                   |
| VNDITDSC                    | char(101)     | YES        |            |           |               | 98%     |       4534 | —                   | —                   |
| COMMNTID                    | char(15)      | YES        |            |           |               | 98%     |          1 | —                   | —                   |
| LOCNCODE                    | char(11)      | YES        |            |           |               | 98%     |         49 | —                   | —                   |
| Project ID                  | char(31)      | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Project Description         | char(51)      | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| aaTrxDimCodeDescr2          | char(51)      | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Filter                      | varchar(6)    | YES        |            |           |               | 100%    |          0 | —                   | —                   |
| Assigned Original Amount    | numeric(38,5) | YES        |            |           |               | 100%    |          0 | NULL                | NULL                |
| Assigned FC Amount          | numeric(38,5) | YES        |            |           |               | 100%    |          0 | NULL                | NULL                |
| Assigned RC Amount          | numeric(38,5) | YES        |            |           |               | 100%    |          0 | NULL                | NULL                |
| GP FC Amount                | numeric(38,5) | YES        |            |           |               | 0%      |     187707 | -301789021.03000    | 301789021.03000     |
| GP RC Amount                | numeric(38,5) | YES        |            |           |               | 12%     |     364839 | -301789021.03000    | 301789021.03000     |

---

### dbo.Outages {#dbo-outages}

| Property | Value |
|---|---|
| Full name | `[dbo].[Outages]` |
| Row count | 12,464 |
| Total size | 9.3 MB |
| Used size | 9.2 MB |
| Created | 2026-03-06 08:08 |
| Schema modified | 2026-03-06 08:08 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column              | Type          | Nullable   | Identity   | Default   | Description   | NULL%   | Distinct   | Min           | Max      |
|---------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------|----------|
| CUSTNMBR            | varchar(15)   | YES        |            |           |               | 0%      | 6833       | —             | —        |
| Customer Name       | varchar(81)   | YES        |            |           |               | 0%      | 6833       | —             | —        |
| Doc number          | char(21)      | NO         |            |           |               | 0%      | 10495      | —             | —        |
| Type                | smallint      | NO         |            |           |               | 0%      | 1          | 4             | 4        |
| Document Date       | char(10)      | YES        |            |           |               | 0%      | 1147       | —             | —        |
| RM GLPOST           | char(10)      | YES        |            |           |               | 0%      | 1149       | —             | —        |
| VOIDSTTS            | smallint      | NO         |            |           |               | 0%      | 2          | 0             | 1        |
| Item                | char(31)      | NO         |            |           |               | 0%      | 12         | —             | —        |
| Description         | char(101)     | NO         |            |           |               | 0%      | 11         | —             | —        |
| Orginal Price       | numeric(19,5) | YES        |            |           |               | 0%      | 5870       | -140000.00000 | 0.00000  |
| Extended Price      | numeric(19,5) | YES        |            |           |               | 0%      | 5966       | -180770.80000 | -0.60000 |
| Currency            | varchar(15)   | YES        |            |           |               | 0%      | 4          | —             | —        |
| Start Date          | char(10)      | YES        |            |           |               | 0%      | 1189       | —             | —        |
| End Date            | char(10)      | YES        |            |           |               | 0%      | 1192       | —             | —        |
| Contract number     | char(11)      | NO         |            |           |               | 0%      | 2          | —             | —        |
| Account             | varchar(129)  | YES        |            |           |               | 0%      | 88         | —             | —        |
| RMVOID              | char(10)      | YES        |            |           |               | 0%      | 36         | —             | —        |
| Natural Account     | varchar(7)    | YES        |            |           |               | 0%      | 2          | —             | —        |
| Voided Month        | int           | YES        |            |           |               | 0%      | 29         | 190001        | 202409   |
| Posted Month        | int           | YES        |            |           |               | 0%      | 171        | 201006        | 202603   |
| Category            | varchar(51)   | YES        |            |           |               | 0%      | 6          | —             | —        |
| Account Description | varchar(181)  | YES        |            |           |               | 0%      | 88         | —             | —        |
| Entity              | varchar(99)   | YES        |            |           |               | 0%      | 11         | —             | —        |
| Location            | varchar(99)   | YES        |            |           |               | 0%      | 22         | —             | —        |
| Cost Centre         | varchar(99)   | YES        |            |           |               | 0%      | 13         | —             | —        |
| gl_Natural_Account  | varchar(39)   | YES        |            |           |               | 0%      | 2          | —             | —        |
| Department          | varchar(21)   | YES        |            |           |               | 0%      | 4          | —             | —        |
| Class               | varchar(21)   | YES        |            |           |               | 0%      | 8          | —             | —        |
| EBITDA              | varchar(31)   | YES        |            |           |               | 0%      | 2          | —             | —        |
| Budget Group        | varchar(31)   | YES        |            |           |               | 0%      | 3          | —             | —        |
| Country             | nvarchar(128) | YES        |            |           |               | 0%      | 4          | —             | —        |
| CMMTTEXT            | text          | YES        |            |           |               | ?       | ?          | —             | —        |
| PSTUSRID            | char(15)      | NO         |            |           |               | 0%      | 25         | —             | —        |

---

### dbo.p1cdn_sop30300_deferred_normalized {#dbo-p1cdn-sop30300-deferred-normalized}

| Property | Value |
|---|---|
| Full name | `[dbo].[p1cdn_sop30300_deferred_normalized]` |
| Row count | 8,187,877 |
| Total size | 2.8 GB |
| Used size | 2.8 GB |
| Created | 2026-03-07 04:25 |
| Schema modified | 2026-03-07 04:25 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column          | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| soptype         | smallint      | NO         |            |           |               | 0%      |          2 | 3                   | 4                   |
| sopnumbe        | char(21)      | NO         |            |           |               | 0%      |     322690 | —                   | —                   |
| lnitmseq        | int           | NO         |            |           |               | 0%      |      27125 | 1                   | 444006400           |
| cmpntseq        | int           | NO         |            |           |               | 0%      |          1 | 0                   | 0                   |
| xtndprce        | numeric(19,5) | NO         |            |           |               | 0%      |     104329 | -95334.62000        | 997761395100.00000  |
| oxtndprc        | numeric(19,5) | NO         |            |           |               | 0%      |      61779 | -94705.77000        | 714990000000.00000  |
| remprice        | numeric(19,5) | NO         |            |           |               | 0%      |     104345 | -95334.62000        | 997761395100.00000  |
| oreprice        | numeric(19,5) | NO         |            |           |               | 0%      |      61787 | -94705.77000        | 714990000000.00000  |
| extdcost        | numeric(19,5) | NO         |            |           |               | 0%      |      13107 | -1.98000            | 40208598.05000      |
| orextcst        | numeric(19,5) | NO         |            |           |               | 0%      |      13048 | -1.98000            | 40208598.05000      |
| mrkdnamt        | numeric(19,5) | NO         |            |           |               | 0%      |         10 | 0.00000             | 300.00000           |
| ormrkdam        | numeric(19,5) | NO         |            |           |               | 0%      |          8 | 0.00000             | 300.00000           |
| mrkdnpct        | smallint      | NO         |            |           |               | 0%      |          3 | 0                   | 3500                |
| mrkdntyp        | smallint      | NO         |            |           |               | 0%      |          2 | 0                   | 1                   |
| taxamnt         | numeric(19,5) | NO         |            |           |               | 0%      |      29223 | -6669.00000         | 71459700000.00000   |
| ortaxamt        | numeric(19,5) | NO         |            |           |               | 0%      |      24688 | -6669.00000         | 71459700000.00000   |
| contstartdte    | datetime      | NO         |            |           |               | 0%      |       6306 | 1900-01-01 00:00:00 | 4748-05-24 00:00:00 |
| contenddte      | datetime      | NO         |            |           |               | 0%      |       6354 | 1900-01-01 00:00:00 | 4748-05-24 00:00:00 |
| totaldays       | numeric(24,6) | YES        |            |           |               | 0%      |        906 | -23.000000          | 364951.000000       |
| PeriodStart     | datetime      | YES        |            |           |               | 0%      |       6358 | 1900-01-01 00:00:00 | 4748-05-24 00:00:00 |
| PeriodEnd       | datetime      | YES        |            |           |               | 0%      |       6371 | 1900-01-01 00:00:00 | 4748-05-24 00:00:00 |
| PeriodDays      | numeric(26,6) | YES        |            |           |               | 0%      |         72 | -23.000000          | 31.000000           |
| xtndprce_period | numeric(38,6) | YES        |            |           |               | 0%      |     450714 | -54413.840000       | 964502681930.000000 |
| oxtndprc_period | numeric(38,6) | YES        |            |           |               | 0%      |     161485 | -51300.000000       | 691157000000.000000 |
| remprice_period | numeric(38,6) | YES        |            |           |               | 0%      |     451126 | -54413.840000       | 964502681930.000000 |
| oreprice_period | numeric(38,6) | YES        |            |           |               | 0%      |     161496 | -51300.000000       | 691157000000.000000 |
| extdcost_period | numeric(38,6) | YES        |            |           |               | 0%      |      13282 | -1.980000           | 40208598.050000     |
| orextcst_period | numeric(38,6) | YES        |            |           |               | 0%      |      13293 | -1.980000           | 40208598.050000     |
| mrkdnamt_period | numeric(38,6) | YES        |            |           |               | 0%      |         14 | 0.000000            | 300.000000          |
| ormrkdam_period | numeric(38,6) | YES        |            |           |               | 0%      |         12 | 0.000000            | 300.000000          |
| taxamnt_period  | numeric(38,6) | YES        |            |           |               | 0%      |     143212 | -6669.000000        | 71459700000.000000  |
| ortaxamt_period | numeric(38,6) | YES        |            |           |               | 0%      |      97407 | -6669.000000        | 71459700000.000000  |

---

### dbo.p1uk_sop30300_deferred_normalized {#dbo-p1uk-sop30300-deferred-normalized}

| Property | Value |
|---|---|
| Full name | `[dbo].[p1uk_sop30300_deferred_normalized]` |
| Row count | 5,502,397 |
| Total size | 1.9 GB |
| Used size | 1.9 GB |
| Created | 2026-03-07 04:37 |
| Schema modified | 2026-03-07 04:37 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column          | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| soptype         | smallint      | NO         |            |           |               | 0%      |          2 | 3                   | 4                   |
| sopnumbe        | char(21)      | NO         |            |           |               | 0%      |     141751 | —                   | —                   |
| lnitmseq        | int           | NO         |            |           |               | 0%      |       6335 | 8192                | 103366656           |
| cmpntseq        | int           | NO         |            |           |               | 0%      |          1 | 0                   | 0                   |
| xtndprce        | numeric(19,5) | NO         |            |           |               | 0%      |      51923 | -28080402951.81000  | 387700000000.00000  |
| oxtndprc        | numeric(19,5) | NO         |            |           |               | 0%      |      38151 | -28080402951.81000  | 387700000000.00000  |
| remprice        | numeric(19,5) | NO         |            |           |               | 0%      |      51920 | -28080402951.81000  | 387700000000.00000  |
| oreprice        | numeric(19,5) | NO         |            |           |               | 0%      |      38151 | -28080402951.81000  | 387700000000.00000  |
| extdcost        | numeric(19,5) | NO         |            |           |               | 0%      |        141 | 0.00000             | 7403.58000          |
| orextcst        | numeric(19,5) | NO         |            |           |               | 0%      |        141 | 0.00000             | 7403.58000          |
| mrkdnamt        | numeric(19,5) | NO         |            |           |               | 0%      |         20 | 0.00000             | 67.30000            |
| ormrkdam        | numeric(19,5) | NO         |            |           |               | 0%      |          3 | 0.00000             | 82.08000            |
| mrkdnpct        | smallint      | NO         |            |           |               | 0%      |          2 | 0                   | 4082                |
| mrkdntyp        | smallint      | NO         |            |           |               | 0%      |          2 | 0                   | 1                   |
| taxamnt         | numeric(19,5) | NO         |            |           |               | 0%      |      18785 | -5616080590.36000   | 77540000000.00000   |
| ortaxamt        | numeric(19,5) | NO         |            |           |               | 0%      |      18024 | -5616080590.36000   | 77540000000.00000   |
| contstartdte    | datetime      | NO         |            |           |               | 0%      |       6143 | 1900-01-01 00:00:00 | 2900-01-01 00:00:00 |
| contenddte      | datetime      | NO         |            |           |               | 0%      |       6236 | 1900-01-01 00:00:00 | 2900-01-01 00:00:00 |
| totaldays       | numeric(24,6) | YES        |            |           |               | 0%      |        571 | -26.000000          | 68666.000000        |
| PeriodStart     | datetime      | YES        |            |           |               | 0%      |       6188 | 1900-01-01 00:00:00 | 2900-01-01 00:00:00 |
| PeriodEnd       | datetime      | YES        |            |           |               | 0%      |       6254 | 1900-01-01 00:00:00 | 2900-01-01 00:00:00 |
| PeriodDays      | numeric(26,6) | YES        |            |           |               | 0%      |         67 | -26.000000          | 31.000000           |
| xtndprce_period | numeric(38,6) | YES        |            |           |               | 0%      |     241007 | -11305097292.287143 | 387700000000.000000 |
| oxtndprc_period | numeric(38,6) | YES        |            |           |               | 0%      |     133332 | -11305097292.287143 | 387700000000.000000 |
| remprice_period | numeric(38,6) | YES        |            |           |               | 0%      |     240918 | -11305097292.287143 | 387700000000.000000 |
| oreprice_period | numeric(38,6) | YES        |            |           |               | 0%      |     133270 | -11305097292.287143 | 387700000000.000000 |
| extdcost_period | numeric(38,6) | YES        |            |           |               | 0%      |        141 | 0.000000            | 7403.580000         |
| orextcst_period | numeric(38,6) | YES        |            |           |               | 0%      |        141 | 0.000000            | 7403.580000         |
| mrkdnamt_period | numeric(38,6) | YES        |            |           |               | 0%      |         39 | 0.000000            | 64.165481           |
| ormrkdam_period | numeric(38,6) | YES        |            |           |               | 0%      |          7 | 0.000000            | 79.344000           |
| taxamnt_period  | numeric(38,6) | YES        |            |           |               | 0%      |     101474 | -2261019458.456623  | 77540000000.000000  |
| ortaxamt_period | numeric(38,6) | YES        |            |           |               | 0%      |      94664 | -2261019458.456623  | 77540000000.000000  |

---

### dbo.p1usa_sop30300_deferred_normalized {#dbo-p1usa-sop30300-deferred-normalized}

| Property | Value |
|---|---|
| Full name | `[dbo].[p1usa_sop30300_deferred_normalized]` |
| Row count | 26,235,739 |
| Total size | 9.1 GB |
| Used size | 9.1 GB |
| Created | 2026-03-07 04:02 |
| Schema modified | 2026-03-07 04:02 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column          | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| soptype         | smallint      | NO         |            |           |               | 0%      |          2 | 3                   | 4                   |
| sopnumbe        | char(21)      | NO         |            |           |               | 0%      |    1312050 | —                   | —                   |
| lnitmseq        | int           | NO         |            |           |               | 0%      |      16814 | 1024                | 273809408           |
| cmpntseq        | int           | NO         |            |           |               | 0%      |          1 | 0                   | 0                   |
| xtndprce        | numeric(19,5) | NO         |            |           |               | 0%      |      74126 | -184065.00000       | 995000000000.00000  |
| oxtndprc        | numeric(19,5) | NO         |            |           |               | 0%      |      73951 | -184065.00000       | 995000000000.00000  |
| remprice        | numeric(19,5) | NO         |            |           |               | 0%      |      74124 | -184065.00000       | 995000000000.00000  |
| oreprice        | numeric(19,5) | NO         |            |           |               | 0%      |      73950 | -184065.00000       | 995000000000.00000  |
| extdcost        | numeric(19,5) | NO         |            |           |               | 0%      |       2346 | 0.00000             | 29747.20000         |
| orextcst        | numeric(19,5) | NO         |            |           |               | 0%      |       2346 | 0.00000             | 29747.20000         |
| mrkdnamt        | numeric(19,5) | NO         |            |           |               | 0%      |         76 | 0.00000             | 1079.79000          |
| ormrkdam        | numeric(19,5) | NO         |            |           |               | 0%      |         76 | 0.00000             | 1079.79000          |
| mrkdnpct        | smallint      | NO         |            |           |               | 0%      |         21 | 0                   | 10000               |
| mrkdntyp        | smallint      | NO         |            |           |               | 0%      |          2 | 0                   | 1                   |
| taxamnt         | numeric(19,5) | NO         |            |           |               | 0%      |       5400 | -47.25000           | 25386570000.00000   |
| ortaxamt        | numeric(19,5) | NO         |            |           |               | 0%      |       5390 | -47.25000           | 25386570000.00000   |
| contstartdte    | datetime      | NO         |            |           |               | 0%      |       7246 | 1899-12-31 00:00:00 | 2998-12-01 00:00:00 |
| contenddte      | datetime      | NO         |            |           |               | 0%      |       7332 | 1899-12-31 00:00:00 | 4205-02-01 00:00:00 |
| totaldays       | numeric(24,6) | YES        |            |           |               | 0%      |        757 | -28.000000          | 800219.000000       |
| PeriodStart     | datetime      | YES        |            |           |               | 0%      |       7399 | 1899-12-31 00:00:00 | 2998-12-01 00:00:00 |
| PeriodEnd       | datetime      | YES        |            |           |               | 0%      |       7461 | 1899-12-31 00:00:00 | 2998-12-31 00:00:00 |
| PeriodDays      | numeric(26,6) | YES        |            |           |               | 0%      |         66 | -28.000000          | 31.000000           |
| xtndprce_period | numeric(38,6) | YES        |            |           |               | 0%      |     461457 | -42600.000000       | 995000000000.000000 |
| oxtndprc_period | numeric(38,6) | YES        |            |           |               | 0%      |     460398 | -42600.000000       | 995000000000.000000 |
| remprice_period | numeric(38,6) | YES        |            |           |               | 0%      |     461425 | -42600.000000       | 995000000000.000000 |
| oreprice_period | numeric(38,6) | YES        |            |           |               | 0%      |     460366 | -42600.000000       | 995000000000.000000 |
| extdcost_period | numeric(38,6) | YES        |            |           |               | 0%      |       2417 | 0.000000            | 29747.200000        |
| orextcst_period | numeric(38,6) | YES        |            |           |               | 0%      |       2417 | 0.000000            | 29747.200000        |
| mrkdnamt_period | numeric(38,6) | YES        |            |           |               | 0%      |        215 | 0.000000            | 1029.450762         |
| ormrkdam_period | numeric(38,6) | YES        |            |           |               | 0%      |        215 | 0.000000            | 1029.450762         |
| taxamnt_period  | numeric(38,6) | YES        |            |           |               | 0%      |      21387 | -15.921196          | 25386570000.000000  |
| ortaxamt_period | numeric(38,6) | YES        |            |           |               | 0%      |      21368 | -15.921196          | 25386570000.000000  |

---

### dbo.PPE_Continuity {#dbo-ppe-continuity}

| Property | Value |
|---|---|
| Full name | `[dbo].[PPE_Continuity]` |
| Row count | 59,595 |
| Total size | 15.0 MB |
| Used size | 15.0 MB |
| Created | 2026-03-06 08:02 |
| Schema modified | 2026-03-06 08:02 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column               | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min              | Max             |
|----------------------|---------------|------------|------------|-----------|---------------|---------|------------|------------------|-----------------|
| Country              | varchar(5)    | NO         |            |           |               | 0%      |          6 | —                | —               |
| Category             | varchar(51)   | YES        |            |           |               | 0%      |         12 | —                | —               |
| Account Description  | varchar(181)  | YES        |            |           |               | 0%      |        269 | —                | —               |
| Natural Account      | varchar(39)   | YES        |            |           |               | 0%      |         74 | —                | —               |
| Transaction Date     | date          | YES        |            |           |               | 0%      |       2954 | 2006-06-30       | 2025-08-31      |
| FC Amount            | numeric(38,5) | YES        |            |           |               | 0%      |      37156 | -258418436.00000 | 351825482.20000 |
| Class                | varchar(21)   | YES        |            |           |               | 0%      |         21 | —                | —               |
| Department           | varchar(21)   | YES        |            |           |               | 0%      |          3 | —                | —               |
| Transaction Type     | varchar(100)  | YES        |            |           |               | 54%     |          2 | —                | —               |
| Source Document      | varchar(11)   | YES        |            |           |               | 0%      |         20 | —                | —               |
| fiscal_quarter       | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                | —               |
| fiscal_year          | smallint      | YES        |            |           |               | 0%      |         21 | 2006             | 2026            |
| fiscal_period        | smallint      | YES        |            |           |               | 0%      |         12 | 1                | 12              |
| BS_Rate              | numeric(19,7) | YES        |            |           |               | 0%      |        241 | 0.7139797        | 1.7114339       |
| PL_Rate              | numeric(19,7) | YES        |            |           |               | 0%      |        241 | 0.7030791        | 3.0000000       |
| RC amount            | numeric(38,5) | YES        |            |           |               | 0%      |      40939 | -253675863.33700 | 345368675.40302 |
| Transaction Grouping | varchar(9)    | NO         |            |           |               | 0%      |          3 | —                | —               |
| Ledger Name          | varchar(100)  | YES        |            |           |               | 0%      |          3 | —                | —               |

---

### dbo.PPE_Continuity_Cogeco {#dbo-ppe-continuity-cogeco}

| Property | Value |
|---|---|
| Full name | `[dbo].[PPE_Continuity_Cogeco]` |
| Row count | 40,063 |
| Total size | 10.1 MB |
| Used size | 10.0 MB |
| Created | 2026-03-06 08:03 |
| Schema modified | 2026-03-06 08:03 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column               | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min              | Max             |
|----------------------|---------------|------------|------------|-----------|---------------|---------|------------|------------------|-----------------|
| Country              | varchar(5)    | NO         |            |           |               | 0%      |          3 | —                | —               |
| Category             | varchar(51)   | YES        |            |           |               | 0%      |         12 | —                | —               |
| Account Description  | varchar(181)  | YES        |            |           |               | 0%      |        203 | —                | —               |
| Natural Account      | varchar(39)   | YES        |            |           |               | 0%      |         72 | —                | —               |
| Transaction Date     | date          | YES        |            |           |               | 0%      |       1271 | 2013-02-01       | 2025-08-31      |
| FC Amount            | numeric(38,5) | YES        |            |           |               | 0%      |      22781 | -258418436.00000 | 351825482.20000 |
| Class                | varchar(21)   | YES        |            |           |               | 0%      |         21 | —                | —               |
| Department           | varchar(21)   | YES        |            |           |               | 0%      |          3 | —                | —               |
| Transaction Type     | varchar(100)  | YES        |            |           |               | 39%     |          2 | —                | —               |
| Source Document      | varchar(11)   | YES        |            |           |               | 0%      |         20 | —                | —               |
| fiscal_quarter       | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                | —               |
| fiscal_year          | smallint      | YES        |            |           |               | 0%      |         13 | 2013             | 2025            |
| fiscal_period        | smallint      | YES        |            |           |               | 0%      |         12 | 1                | 12              |
| BS_Rate              | numeric(19,7) | YES        |            |           |               | 0%      |        129 | 0.9949000        | 2.0426000       |
| PL_Rate              | numeric(19,7) | YES        |            |           |               | 0%      |        129 | 0.9895684        | 2.0533810       |
| RC amount            | numeric(38,5) | YES        |            |           |               | 0%      |      25084 | -258418436.00000 | 351825482.20000 |
| Transaction Grouping | varchar(9)    | NO         |            |           |               | 0%      |          3 | —                | —               |
| Ledger Name          | varchar(100)  | YES        |            |           |               | 0%      |          3 | —                | —               |

---

### dbo.Profit_Analysis {#dbo-profit-analysis}

| Property | Value |
|---|---|
| Full name | `[dbo].[Profit_Analysis]` |
| Row count | 730,484 |
| Total size | 187.1 MB |
| Used size | 187.1 MB |
| Created | 2011-04-05 12:57 |
| Schema modified | 2011-04-05 12:57 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column          | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                    | Max                 |
|-----------------|----------------|------------|------------|-----------|---------------|---------|------------|------------------------|---------------------|
| Type            | varchar(7)     | NO         |            |           |               | 0%      |          2 | —                      | —                   |
| customers_id    | nvarchar(256)  | YES        |            |           |               | 0%      |      14239 | —                      | —                   |
| lob             | nvarchar(255)  | YES        |            |           |               | 0%      |          5 | —                      | —                   |
| Period          | datetime       | YES        |            |           |               | 0%      |      16758 | 1999-05-31 00:00:00    | 2015-12-31 23:59:59 |
| Revenue         | numeric(38,6)  | YES        |            |           |               | 0%      |     117822 | -50691.620614          | 209714.689997       |
| SoftwareCost    | numeric(38,5)  | YES        |            |           |               | 0%      |       4404 | -26106.25000           | 0.00000             |
| HardwareCost    | money          | YES        |            |           |               | 0%      |       9607 | -1859024.2500          | 0.0000              |
| CoS             | int            | YES        |            |           |               | 0%      |        286 | -61860                 | 0                   |
| Opex            | int            | YES        |            |           |               | 0%      |        265 | -20620                 | 0                   |
| Enterprise      | int            | YES        |            |           |               | 0%      |        280 | -61860                 | 0                   |
| Depretiation    | money          | YES        |            |           |               | 0%      |       9890 | -51639.4850            | 0.0000              |
| SoftwareCost_pr | numeric(38,6)  | YES        |            |           |               | 0%      |      11883 | -24230.960024          | 0.000000            |
| CoS_pr          | numeric(38,14) | YES        |            |           |               | 0%      |       4160 | -57222.58064516129025  | 0E-14               |
| Opex_pr         | numeric(38,15) | YES        |            |           |               | 0%      |       4132 | -19074.193548387096692 | 0E-15               |
| Enterprise_pr   | numeric(38,14) | YES        |            |           |               | 0%      |       4011 | -57222.58064516129025  | 0E-14               |
| Depretiation_pr | numeric(38,6)  | YES        |            |           |               | 0%      |      20991 | -47900.928542          | 0.000000            |

---

### dbo.Profit_Analysis_ROA {#dbo-profit-analysis-roa}

| Property | Value |
|---|---|
| Full name | `[dbo].[Profit_Analysis_ROA]` |
| Row count | 490,427 |
| Total size | 127.0 MB |
| Used size | 127.0 MB |
| Created | 2011-04-05 17:32 |
| Schema modified | 2011-04-05 17:32 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column          | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|-----------------|----------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| customers_id    | nvarchar(256)  | YES        |            |           |               | 0%      |      11833 | —                          | —                          |
| serviceid       | int            | NO         |            |           |               | 0%      |      39551 | 17480                      | 2391110                    |
| product         | varchar(200)   | YES        |            |           |               | 0%      |        241 | —                          | —                          |
| first_online    | datetime2      | YES        |            |           |               | 0%      |      37340 | 2002-09-09 13:59:00        | 2011-04-04 08:56:59.847384 |
| enddate         | datetime2      | NO         |            |           |               | 0%      |      16048 | 2008-08-21 00:00:06.130166 | 2011-04-05 12:14:24.646998 |
| Period          | datetime       | YES        |            |           |               | 0%      |      14068 | 2008-08-21 00:00:06.130000 | 2011-04-05 12:14:24.647000 |
| Revenue         | numeric(38,6)  | YES        |            |           |               | 0%      |      95764 | -11496.070000              | 22725.063929               |
| SoftwareCost    | numeric(38,5)  | YES        |            |           |               | 0%      |       2139 | -6027.21000                | 0.00000                    |
| HardwareCost    | money          | YES        |            |           |               | 0%      |       5141 | -26071.1500                | 0.0000                     |
| CoS             | int            | YES        |            |           |               | 0%      |         14 | -910                       | -60                        |
| Opex            | int            | YES        |            |           |               | 0%      |         13 | -350                       | -20                        |
| Enterprise      | int            | YES        |            |           |               | 0%      |         13 | -980                       | -60                        |
| Depretiation    | money          | YES        |            |           |               | 0%      |       5187 | -724.1983                  | 0.0000                     |
| SoftwareCost_pr | numeric(38,6)  | YES        |            |           |               | 0%      |       5564 | -6027.210000               | 0.000000                   |
| CoS_pr          | numeric(38,14) | YES        |            |           |               | 0%      |        389 | -910.00000000000000        | -1.93548387096774          |
| Opex_pr         | numeric(38,15) | YES        |            |           |               | 0%      |        374 | -350.000000000000000       | -0.645161290322581         |
| Enterprise_pr   | numeric(38,14) | YES        |            |           |               | 0%      |        373 | -980.00000000000000        | -1.93548387096774          |
| Depretiation_pr | numeric(38,6)  | YES        |            |           |               | 0%      |      11455 | -724.198608                | 0.000000                   |

---

### dbo.Profit_Cost {#dbo-profit-cost}

| Property | Value |
|---|---|
| Full name | `[dbo].[Profit_Cost]` |
| Row count | 942,603 |
| Total size | 631.9 MB |
| Used size | 631.8 MB |
| Created | 2011-04-05 12:06 |
| Schema modified | 2011-04-05 12:06 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column           | Type           | Nullable   | Identity   | Default   | Description   | NULL%   | Distinct   | Min                        | Max                        |
|------------------|----------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| customers_id     | nvarchar(256)  | YES        |            |           |               | 0%      | 12563      | —                          | —                          |
| serviceid        | int            | NO         |            |           |               | 0%      | 43084      | 282                        | 2391236                    |
| servicestatus    | ntext          | NO         |            |           |               | ?       | ?          | —                          | —                          |
| first_online     | datetime2      | YES        |            |           |               | 0%      | 40344      | 1999-05-17 00:00:00        | 2011-04-04 22:42:47.086574 |
| products_name    | ntext          | NO         |            |           |               | ?       | ?          | —                          | —                          |
| dc               | ntext          | YES        |            |           |               | ?       | ?          | —                          | —                          |
| lob              | nvarchar(255)  | NO         |            |           |               | 0%      | 3          | —                          | —                          |
| OS               | nvarchar(255)  | YES        |            |           |               | 0%      | 2          | —                          | —                          |
| enddate          | datetime2      | NO         |            |           |               | 0%      | 17778      | 2008-08-12 00:08:02.245825 | 2011-04-05 12:14:24.646998 |
| totaldays        | numeric(24,6)  | YES        |            |           |               | 0%      | 2757       | 1.000000                   | 4219.000000                |
| PeriodStart      | datetime2      | YES        |            |           |               | 0%      | 40484      | 1999-05-17 00:00:00        | 2011-04-04 22:42:47.086574 |
| PeriodEnd        | datetime2      | YES        |            |           |               | 0%      | 16660      | 1999-05-31 00:00:00        | 2011-04-05 12:14:24.646998 |
| PeriodDays       | numeric(26,6)  | YES        |            |           |               | 0%      | 31         | 1.000000                   | 31.000000                  |
| SoftwareCost     | numeric(38,5)  | YES        |            |           |               | 26%     | 863        | -2009.07000                | 0.00000                    |
| SoftwareCost_pr  | numeric(38,6)  | YES        |            |           |               | 26%     | 6180       | -2009.070000               | 0.000000                   |
| HardwareWCost    | money          | YES        |            |           |               | 26%     | 2311       | -10639.9800                | -135.0500                  |
| HardwareWCost_pr | numeric(38,6)  | YES        |            |           |               | 26%     | 11909      | -10639.980000              | -8.064516                  |
| CoS              | int            | NO         |            |           |               | 0%      | 2          | -130                       | -60                        |
| CoS_pr           | numeric(38,14) | YES        |            |           |               | 0%      | 352        | -130.00000000000000        | -1.93548387096774          |
| Opex             | int            | NO         |            |           |               | 0%      | 2          | -50                        | -20                        |
| Opex_pr          | numeric(38,15) | YES        |            |           |               | 0%      | 333        | -50.000000000000000        | -0.645161290322581         |
| Enterprise       | int            | NO         |            |           |               | 0%      | 2          | -140                       | -60                        |
| Enterprise_pr    | numeric(38,14) | YES        |            |           |               | 0%      | 336        | -140.00000000000000        | -1.93548387096774          |
| Depretiation     | money          | YES        |            |           |               | 26%     | 2311       | -295.5550                  | -3.7513                    |
| Depretiation_pr  | numeric(38,6)  | YES        |            |           |               | 26%     | 11909      | -295.555000                | -0.224014                  |

---

### dbo.Profit_HWSWCost_disabled {#dbo-profit-hwswcost-disabled}

| Property | Value |
|---|---|
| Full name | `[dbo].[Profit_HWSWCost_disabled]` |
| Row count | 86,983 |
| Total size | 8.3 MB |
| Used size | 8.3 MB |
| Created | 2019-12-18 06:59 |
| Schema modified | 2020-01-06 14:04 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column         | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min         | Max         |
|----------------|---------------|------------|------------|-----------|---------------|---------|------------|-------------|-------------|
| service_id     | int           | NO         |            |           |               | 0%      |      85891 | 282         | 6229792     |
| products_name  | varchar(200)  | YES        |            |           |               | 0%      |        324 | —           | —           |
| Modified Price | money         | YES        |            |           |               | 44%     |         64 | 250.0000    | 6989.2000   |
| SoftwareCost   | numeric(38,5) | YES        |            |           |               | 0%      |       1274 | 0.00000     | 12117.03000 |
| Components     | money         | YES        |            |           |               | 0%      |       3517 | -5436.0000  | 12324.2000  |
| HwSwCost       | numeric(38,5) | YES        |            |           |               | 0%      |      12882 | -5436.00000 | 14210.20000 |
| Status         | nvarchar(255) | YES        |            |           |               | 35%     |          5 | —           | —           |

---

### dbo.Profit_LicenseCost {#dbo-profit-licensecost}

| Property | Value |
|---|---|
| Full name | `[dbo].[Profit_LicenseCost]` |
| Row count | 40,168 |
| Total size | 1.2 MB |
| Used size | 1.2 MB |
| Created | 2011-05-07 16:08 |
| Schema modified | 2011-05-07 16:08 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column       | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct |   Min |            Max |
|--------------|---------------|------------|------------|-----------|---------------|---------|------------|-------|----------------|
| serviceid    | int           | NO         |            |           |               | 0%      |      40168 |   282 |    2.39621e+06 |
| SoftwareCost | numeric(38,5) | YES        |            |           |               | 0%      |        890 |     0 | 2009.07        |

---

### dbo.Profit_OnlineDays {#dbo-profit-onlinedays}

| Property | Value |
|---|---|
| Full name | `[dbo].[Profit_OnlineDays]` |
| Row count | 942,603 |
| Total size | 491.0 MB |
| Used size | 491.0 MB |
| Created | 2011-04-05 12:04 |
| Schema modified | 2011-04-05 12:04 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column        | Type          | Nullable   | Identity   | Default   | Description   | NULL%   | Distinct   | Min                        | Max                        |
|---------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| customers_id  | nvarchar(256) | YES        |            |           |               | 0%      | 12563      | —                          | —                          |
| serviceid     | int           | NO         |            |           |               | 0%      | 43084      | 282                        | 2391236                    |
| servicestatus | ntext         | NO         |            |           |               | ?       | ?          | —                          | —                          |
| first_online  | datetime2     | YES        |            |           |               | 0%      | 40344      | 1999-05-17 00:00:00        | 2011-04-04 22:42:47.086574 |
| products_name | ntext         | NO         |            |           |               | ?       | ?          | —                          | —                          |
| dc            | ntext         | YES        |            |           |               | ?       | ?          | —                          | —                          |
| lob           | nvarchar(255) | NO         |            |           |               | 0%      | 3          | —                          | —                          |
| OS            | nvarchar(255) | YES        |            |           |               | 0%      | 2          | —                          | —                          |
| enddate       | datetime2     | NO         |            |           |               | 0%      | 17778      | 2008-08-12 00:08:02.245825 | 2011-04-05 12:14:24.646998 |
| totaldays     | numeric(24,6) | YES        |            |           |               | 0%      | 2757       | 1.000000                   | 4219.000000                |
| PeriodStart   | datetime2     | YES        |            |           |               | 0%      | 40484      | 1999-05-17 00:00:00        | 2011-04-04 22:42:47.086574 |
| PeriodEnd     | datetime2     | YES        |            |           |               | 0%      | 16660      | 1999-05-31 00:00:00        | 2011-04-05 12:14:24.646998 |
| PeriodDays    | numeric(26,6) | YES        |            |           |               | 0%      | 31         | 1.000000                   | 31.000000                  |

---

### dbo.SKU_HWSWCost {#dbo-sku-hwswcost}

| Property | Value |
|---|---|
| Full name | `[dbo].[SKU_HWSWCost]` |
| Row count | 38,183 |
| Total size | 4.3 MB |
| Used size | 4.2 MB |
| Created | 2011-08-09 17:20 |
| Schema modified | 2011-08-09 17:20 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column         | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min         | Max         |
|----------------|---------------|------------|------------|-----------|---------------|---------|------------|-------------|-------------|
| service_id     | int           | NO         |            |           |               | 0%      |      38183 | 282         | 2429248     |
| products_name  | varchar(200)  | YES        |            |           |               | 0%      |        208 | —           | —           |
| Modified Price | numeric(19,5) | NO         |            |           |               | 0%      |         67 | 0.00000     | 6989.20000  |
| SoftwareCost   | numeric(38,5) | YES        |            |           |               | 0%      |        656 | 0.00000     | 2442.13000  |
| Components     | numeric(38,5) | YES        |            |           |               | 0%      |       1836 | -2538.08000 | 12324.20000 |
| HwSwCost       | numeric(38,5) | YES        |            |           |               | 0%      |       7436 | 0.00000     | 14190.20000 |
| Status         | nvarchar(255) | YES        |            |           |               | 0%      |          5 | —           | —           |

---

### dbo.SLA_Credits {#dbo-sla-credits}

| Property | Value |
|---|---|
| Full name | `[dbo].[SLA_Credits]` |
| Row count | 1,450 |
| Total size | 1.3 MB |
| Used size | 1.2 MB |
| Created | 2026-03-06 08:05 |
| Schema modified | 2026-03-06 08:05 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                | Type          | Nullable   | Identity   | Default   | Description   | NULL%   | Distinct   | Min                 | Max                 |
|-----------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| Customer Name         | varchar(81)   | YES        |            |           |               | 0%      | 878        | —                   | —                   |
| Doc number            | char(21)      | NO         |            |           |               | 0%      | 1348       | —                   | —                   |
| Type                  | smallint      | NO         |            |           |               | 0%      | 2          | 3                   | 4                   |
| Document Date         | char(10)      | YES        |            |           |               | 0%      | 447        | —                   | —                   |
| RM GLPOST             | char(10)      | YES        |            |           |               | 0%      | 445        | —                   | —                   |
| VOIDSTTS              | smallint      | NO         |            |           |               | 0%      | 2          | 0                   | 1                   |
| Item                  | char(31)      | NO         |            |           |               | 0%      | 9          | —                   | —                   |
| Description           | char(101)     | NO         |            |           |               | 0%      | 5          | —                   | —                   |
| Orginal Price         | numeric(19,5) | YES        |            |           |               | 0%      | 1324       | -140000.00000       | 2000.00000          |
| Extended Price        | numeric(19,5) | YES        |            |           |               | 0%      | 1331       | -180770.80000       | 2000.00000          |
| Currency              | varchar(15)   | YES        |            |           |               | 0%      | 4          | —                   | —                   |
| Start Date            | char(10)      | YES        |            |           |               | 0%      | 427        | —                   | —                   |
| End Date              | char(10)      | YES        |            |           |               | 0%      | 437        | —                   | —                   |
| Contract number       | char(11)      | NO         |            |           |               | 0%      | 2          | —                   | —                   |
| Account               | varchar(129)  | YES        |            |           |               | 0%      | 57         | —                   | —                   |
| RMVOID                | char(10)      | YES        |            |           |               | 0%      | 6          | —                   | —                   |
| Natural Account Code  | varchar(7)    | YES        |            |           |               | 0%      | 2          | —                   | —                   |
| Voided Month          | int           | YES        |            |           |               | 0%      | 6          | 190001              | 202409              |
| Posted Month          | int           | YES        |            |           |               | 0%      | 125        | 200907              | 202603              |
| Category              | varchar(51)   | YES        |            |           |               | 0%      | 6          | —                   | —                   |
| Account Description   | varchar(181)  | YES        |            |           |               | 0%      | 57         | —                   | —                   |
| Entity                | varchar(99)   | YES        |            |           |               | 0%      | 5          | —                   | —                   |
| Location              | varchar(99)   | YES        |            |           |               | 0%      | 19         | —                   | —                   |
| Cost Centre           | varchar(99)   | YES        |            |           |               | 0%      | 11         | —                   | —                   |
| Natural Account       | varchar(39)   | YES        |            |           |               | 0%      | 2          | —                   | —                   |
| Department            | varchar(21)   | YES        |            |           |               | 0%      | 3          | —                   | —                   |
| Class                 | varchar(21)   | YES        |            |           |               | 0%      | 7          | —                   | —                   |
| EBITDA                | varchar(31)   | YES        |            |           |               | 0%      | 2          | —                   | —                   |
| Budget Group          | varchar(31)   | YES        |            |           |               | 0%      | 3          | —                   | —                   |
| Country               | nvarchar(128) | YES        |            |           |               | 0%      | 4          | —                   | —                   |
| CMMTTEXT              | text          | YES        |            |           |               | ?       | ?          | —                   | —                   |
| integer_key           | smallint      | NO         |            |           |               | 0%      | 445        | 3837                | 9924                |
| date_key              | datetime      | YES        |            |           |               | 0%      | 445        | 2009-07-03 00:00:00 | 2026-03-03 00:00:00 |
| day_number_of_week    | smallint      | YES        |            |           |               | 0%      | 7          | 1                   | 7                   |
| day_name_of_week      | varchar(9)    | YES        |            |           |               | 0%      | 7          | —                   | —                   |
| day_number_of_month   | smallint      | YES        |            |           |               | 0%      | 31         | 1                   | 31                  |
| week_number_of_year   | smallint      | YES        |            |           |               | 0%      | 53         | 1                   | 53                  |
| month_name            | varchar(9)    | YES        |            |           |               | 0%      | 12         | —                   | —                   |
| calendar_month        | smallint      | YES        |            |           |               | 0%      | 12         | 1                   | 12                  |
| calendar_quarter      | varchar(2)    | YES        |            |           |               | 0%      | 4          | —                   | —                   |
| calendar_year         | smallint      | YES        |            |           |               | 0%      | 18         | 2009                | 2026                |
| fiscal_period         | smallint      | YES        |            |           |               | 0%      | 12         | 1                   | 12                  |
| fiscal_quarter        | varchar(2)    | YES        |            |           |               | 0%      | 4          | —                   | —                   |
| fiscal_year           | smallint      | YES        |            |           |               | 0%      | 17         | 2010                | 2026                |
| fiscal_year_cogeco    | smallint      | YES        |            |           |               | 0%      | 17         | 2009                | 2026                |
| fiscal_period_cogeco  | smallint      | YES        |            |           |               | 0%      | 12         | 1                   | 12                  |
| fiscal_quarter_cogeco | varchar(2)    | YES        |            |           |               | 0%      | 4          | —                   | —                   |
| date_short            | date          | YES        |            |           |               | 0%      | 445        | 2009-07-03          | 2026-03-03          |
| fiscal_week_cogeco    | tinyint       | YES        |            |           |               | 0%      | 53         | 1                   | 53                  |

---

### dbo.temp_sop30300_deferred_normalized {#dbo-temp-sop30300-deferred-normalized}

| Property | Value |
|---|---|
| Full name | `[dbo].[temp_sop30300_deferred_normalized]` |
| Row count | 4,158,315 |
| Total size | 1.4 GB |
| Used size | 1.4 GB |
| Created | 2011-02-23 16:11 |
| Schema modified | 2011-02-23 16:11 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column          | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| soptype         | smallint      | NO         |            |           |               | 0%      |          2 | 3                   | 4                   |
| sopnumbe        | char(21)      | NO         |            |           |               | 0%      |     340417 | —                   | —                   |
| lnitmseq        | int           | NO         |            |           |               | 0%      |       2885 | 1024                | 45645824            |
| cmpntseq        | int           | NO         |            |           |               | 0%      |          1 | 0                   | 0                   |
| xtndprce        | numeric(19,5) | NO         |            |           |               | 0%      |      32381 | -8727.30000         | 148536.00000        |
| oxtndprc        | numeric(19,5) | NO         |            |           |               | 0%      |      32378 | -8727.30000         | 148536.00000        |
| remprice        | numeric(19,5) | NO         |            |           |               | 0%      |      32377 | -8727.30000         | 148536.00000        |
| oreprice        | numeric(19,5) | NO         |            |           |               | 0%      |      32374 | -8727.30000         | 148536.00000        |
| extdcost        | numeric(19,5) | NO         |            |           |               | 0%      |       1347 | 0.00000             | 12031.60000         |
| orextcst        | numeric(19,5) | NO         |            |           |               | 0%      |       1347 | 0.00000             | 12031.60000         |
| mrkdnamt        | numeric(19,5) | NO         |            |           |               | 0%      |         20 | 0.00000             | 865.99000           |
| ormrkdam        | numeric(19,5) | NO         |            |           |               | 0%      |         20 | 0.00000             | 865.99000           |
| mrkdnpct        | smallint      | NO         |            |           |               | 0%      |          2 | 0                   | 10000               |
| mrkdntyp        | smallint      | NO         |            |           |               | 0%      |          2 | 0                   | 1                   |
| taxamnt         | numeric(19,5) | NO         |            |           |               | 0%      |       2619 | 0.00000             | 19133.66000         |
| ortaxamt        | numeric(19,5) | NO         |            |           |               | 0%      |       2617 | 0.00000             | 19133.66000         |
| contstartdte    | datetime      | NO         |            |           |               | 0%      |       1857 | 1900-01-01 00:00:00 | 2998-12-01 00:00:00 |
| contenddte      | datetime      | NO         |            |           |               | 0%      |       2195 | 1900-01-01 00:00:00 | 2998-12-31 00:00:00 |
| totaldays       | numeric(24,6) | YES        |            |           |               | 0%      |        362 | 1.000000            | 1827.000000         |
| PeriodStart     | datetime      | YES        |            |           |               | 0%      |       1913 | 1900-01-01 00:00:00 | 2998-12-01 00:00:00 |
| PeriodEnd       | datetime      | YES        |            |           |               | 0%      |       2237 | 1900-01-01 00:00:00 | 2998-12-31 00:00:00 |
| PeriodDays      | numeric(26,6) | YES        |            |           |               | 0%      |         61 | 0.416666            | 31.000000           |
| xtndprce_period | numeric(38,6) | YES        |            |           |               | 0%      |     175733 | -8727.300000        | 148536.000000       |
| oxtndprc_period | numeric(38,6) | YES        |            |           |               | 0%      |     175728 | -8727.300000        | 148536.000000       |
| remprice_period | numeric(38,6) | YES        |            |           |               | 0%      |     175726 | -8727.300000        | 148536.000000       |
| oreprice_period | numeric(38,6) | YES        |            |           |               | 0%      |     175721 | -8727.300000        | 148536.000000       |
| extdcost_period | numeric(38,6) | YES        |            |           |               | 0%      |       1351 | 0.000000            | 12031.600000        |
| orextcst_period | numeric(38,6) | YES        |            |           |               | 0%      |       1351 | 0.000000            | 12031.600000        |
| mrkdnamt_period | numeric(38,6) | YES        |            |           |               | 0%      |        116 | 0.000000            | 865.990000          |
| ormrkdam_period | numeric(38,6) | YES        |            |           |               | 0%      |        116 | 0.000000            | 865.990000          |
| taxamnt_period  | numeric(38,6) | YES        |            |           |               | 0%      |       9340 | 0.000000            | 19133.660000        |
| ortaxamt_period | numeric(38,6) | YES        |            |           |               | 0%      |       9338 | 0.000000            | 19133.660000        |

---

### dbo.WaterFall_MRC_Summary_Normalized_disabled {#dbo-waterfall-mrc-summary-normalized-disabled}

| Property | Value |
|---|---|
| Full name | `[dbo].[WaterFall_MRC_Summary_Normalized_disabled]` |
| Row count | 417,078 |
| Total size | 103.3 MB |
| Used size | 103.1 MB |
| Created | 2020-01-07 05:48 |
| Schema modified | 2020-01-08 09:44 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|-----------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| gpinstance            | varchar(5)    | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| SERVICE_ID            | char(21)      | YES        |            |           |               | 0%      |      17731 | —                          | —                          |
| CUSTNMBR              | char(15)      | YES        |            |           |               | 0%      |       7775 | —                          | —                          |
| lastdate              | datetime      | YES        |            |           |               | 0%      |        184 | 2011-07-31 23:59:59        | 2026-10-31 23:59:59        |
| MRR                   | numeric(38,6) | YES        |            |           |               | 0%      |     186342 | -144751.308587             | 1417819.129084             |
| Location              | varchar(7)    | YES        |            |           |               | 0%      |         25 | —                          | —                          |
| Customer Class        | varchar(15)   | YES        |            |           |               | 0%      |          8 | —                          | —                          |
| orderstatus           | nvarchar(64)  | YES        |            |           |               | 56%     |          2 | —                          | —                          |
| ProvisionDate         | datetime      | YES        |            |           |               | 56%     |      17664 | 2003-05-30 00:00:00        | 2020-01-02 16:54:42.363000 |
| order_service_id      | varchar(20)   | YES        |            |           |               | 56%     |      17693 | —                          | —                          |
| products_name         | varchar(50)   | YES        |            |           |               | 56%     |        337 | —                          | —                          |
| currency              | nvarchar(3)   | YES        |            |           |               | 56%     |          4 | —                          | —                          |
| MRC                   | float(53)     | YES        |            |           |               | 56%     |       3515 | 0.0                        | 43000.0                    |
| NRC                   | float(53)     | YES        |            |           |               | 56%     |        425 | 0.0                        | 250000.0                   |
| type                  | nvarchar(64)  | YES        |            |           |               | 56%     |         17 | —                          | —                          |
| DC                    | varchar(75)   | YES        |            |           |               | 56%     |         25 | —                          | —                          |
| product_line          | nvarchar(255) | YES        |            |           |               | 56%     |          5 | —                          | —                          |
| order_id              | int           | YES        |            |           |               | 56%     |       7890 | 240                        | 228264                     |
| name                  | nvarchar(32)  | YES        |            |           |               | 56%     |          2 | —                          | —                          |
| OrderDate             | datetime      | YES        |            |           |               | 56%     |       7556 | 2003-05-30 00:00:00        | 2019-12-26 13:13:26.700000 |
| promo_code            | nvarchar(32)  | YES        |            |           |               | 96%     |         34 | —                          | —                          |
| description           | varchar(75)   | YES        |            |           |               | 96%     |         32 | —                          | —                          |
| CancelDate            | datetime      | YES        |            |           |               | 87%     |       4956 | 2014-10-05 17:40:50.683000 | 2020-01-06 18:55:04.673000 |
| PendingClientApproval | datetime      | YES        |            |           |               | 64%     |       6934 | 2008-08-26 14:29:35.543000 | 2019-12-30 13:11:39.860000 |
| ClientApproved        | datetime      | YES        |            |           |               | 63%     |       7260 | 2008-08-26 16:09:03.603000 | 2019-12-30 16:22:05.257000 |
| OrderCanceled         | datetime      | YES        |            |           |               | 100%    |         29 | 2011-01-25 12:12:55.037000 | 2019-09-23 06:52:13.260000 |
| Customer              | varchar(65)   | YES        |            |           |               | 0%      |       7716 | —                          | —                          |

---

### dbo.Waterfall_Normalized_disabled {#dbo-waterfall-normalized-disabled}

| Property | Value |
|---|---|
| Full name | `[dbo].[Waterfall_Normalized_disabled]` |
| Row count | 1,169,760 |
| Total size | 408.0 MB |
| Used size | 407.8 MB |
| Created | 2020-01-07 05:22 |
| Schema modified | 2020-01-08 09:41 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                | Type          | Nullable   | Identity   | Default   | Description   | NULL%   | Distinct   | Min                        | Max                        |
|-----------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| gpinstance            | varchar(5)    | YES        |            |           |               | 10%     | 3          | —                          | —                          |
| SERVICE_ID            | char(21)      | YES        |            |           |               | 10%     | 17731      | —                          | —                          |
| CUSTNMBR              | char(15)      | YES        |            |           |               | 10%     | 7904       | —                          | —                          |
| GLPOSTDT              | datetime      | YES        |            |           |               | 10%     | 2017       | 2008-08-08 00:00:00        | 2020-01-06 00:00:00        |
| PeriodStart           | datetime      | YES        |            |           |               | 10%     | 2601       | 2008-01-01 00:00:00        | 2026-10-01 00:00:00        |
| PeriodEnd             | datetime      | YES        |            |           |               | 10%     | 2872       | 2008-01-31 00:00:00        | 2026-10-31 00:00:00        |
| xtndprce_period       | numeric(38,6) | YES        |            |           |               | 10%     | 367373     | -150684.970000             | 1406015.115552             |
| xtndprce_period_nx    | numeric(38,6) | YES        |            |           |               | 10%     | 190931     | -184744.100000             | 1818258.740000             |
| Location              | varchar(7)    | YES        |            |           |               | 10%     | 25         | —                          | —                          |
| Cost Center           | varchar(7)    | YES        |            |           |               | 10%     | 22         | —                          | —                          |
| Natural Account       | varchar(7)    | YES        |            |           |               | 10%     | 32         | —                          | —                          |
| Account               | varchar(51)   | YES        |            |           |               | 10%     | 424        | —                          | —                          |
| Customer Class        | varchar(15)   | YES        |            |           |               | 10%     | 8          | —                          | —                          |
| Customer              | varchar(65)   | YES        |            |           |               | 10%     | 7843       | —                          | —                          |
| orderstatus           | nvarchar(64)  | YES        |            |           |               | 62%     | 3          | —                          | —                          |
| ProvisionDate         | datetime      | YES        |            |           |               | 62%     | 117562     | 1999-05-17 00:00:00        | 2020-01-06 13:36:16.320000 |
| Order_service_id      | int           | YES        |            |           |               | 62%     | 128875     | 282                        | 6229911                    |
| products_name         | ntext         | YES        |            |           |               | ?       | ?          | —                          | —                          |
| currency              | nvarchar(3)   | YES        |            |           |               | 62%     | 4          | —                          | —                          |
| MRC                   | float(53)     | YES        |            |           |               | 62%     | 15166      | -26.36                     | 45000.0                    |
| NRC                   | float(53)     | YES        |            |           |               | 62%     | 1656       | -49.0                      | 250000.0                   |
| type                  | nvarchar(64)  | YES        |            |           |               | 62%     | 20         | —                          | —                          |
| DC                    | varchar(75)   | YES        |            |           |               | 62%     | 37         | —                          | —                          |
| product_line          | nvarchar(255) | YES        |            |           |               | 62%     | 5          | —                          | —                          |
| order_id              | int           | YES        |            |           |               | 62%     | 65998      | 1                          | 228350                     |
| name                  | nvarchar(32)  | YES        |            |           |               | 62%     | 2          | —                          | —                          |
| OrderDate             | datetime      | YES        |            |           |               | 62%     | 53056      | 1999-05-17 00:00:00        | 2020-01-06 11:57:33.853000 |
| promo_code            | nvarchar(32)  | YES        |            |           |               | 97%     | 96         | —                          | —                          |
| description           | varchar(75)   | YES        |            |           |               | 97%     | 93         | —                          | —                          |
| CancelDate            | datetime      | YES        |            |           |               | 80%     | 102126     | 2008-08-12 00:08:02.247000 | 2020-01-06 18:55:15.050000 |
| PendingClientApproval | datetime      | YES        |            |           |               | 74%     | 36646      | 2008-08-09 17:16:37.403000 | 2020-01-06 14:02:44.833000 |
| ClientApproved        | datetime      | YES        |            |           |               | 73%     | 44015      | 2008-08-10 00:06:30.750000 | 2020-01-06 15:30:07.430000 |
| OrderCanceled         | datetime      | YES        |            |           |               | 100%    | 142        | 2010-01-17 15:30:48.710000 | 2019-10-29 03:26:32.247000 |
| company_name          | nvarchar(255) | YES        |            |           |               | 62%     | 18946      | —                          | —                          |

---

### dbo.Waterfall_Normalized_old {#dbo-waterfall-normalized-old}

| Property | Value |
|---|---|
| Full name | `[dbo].[Waterfall_Normalized_old]` |
| Row count | 1,712,292 |
| Total size | 658.2 MB |
| Used size | 658.1 MB |
| Created | 2025-12-16 04:56 |
| Schema modified | 2025-12-16 15:05 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                | Type          | Nullable   | Identity   | Default   | Description   | NULL%   | Distinct   | Min                        | Max                        |
|-----------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| gpinstance            | varchar(5)    | YES        |            |           |               | 7%      | 3          | —                          | —                          |
| SERVICE_ID            | char(21)      | YES        |            |           |               | 7%      | 20170      | —                          | —                          |
| CUSTNMBR              | char(15)      | YES        |            |           |               | 7%      | 8315       | —                          | —                          |
| GLPOSTDT              | datetime      | YES        |            |           |               | 7%      | 3405       | 2008-08-08 00:00:00        | 2025-12-15 00:00:00        |
| PeriodStart           | datetime      | YES        |            |           |               | 7%      | 4733       | 2008-01-01 00:00:00        | 2030-04-01 00:00:00        |
| PeriodEnd             | datetime      | YES        |            |           |               | 7%      | 4809       | 2008-01-31 00:00:00        | 2030-04-30 00:00:00        |
| xtndprce_period       | numeric(38,6) | YES        |            |           |               | 7%      | 542538     | -184065.000000             | 2241888.000000             |
| xtndprce_period_nx    | numeric(38,6) | YES        |            |           |               | 7%      | 265920     | -184744.100000             | 2241888.000000             |
| Location              | varchar(7)    | YES        |            |           |               | 7%      | 29         | —                          | —                          |
| Cost Center           | varchar(7)    | YES        |            |           |               | 7%      | 26         | —                          | —                          |
| Natural Account       | varchar(7)    | YES        |            |           |               | 7%      | 33         | —                          | —                          |
| Account               | varchar(51)   | YES        |            |           |               | 7%      | 483        | —                          | —                          |
| Customer Class        | varchar(15)   | YES        |            |           |               | 7%      | 11         | —                          | —                          |
| Customer              | varchar(65)   | YES        |            |           |               | 7%      | 8315       | —                          | —                          |
| orderstatus           | nvarchar(64)  | YES        |            |           |               | 52%     | 3          | —                          | —                          |
| ProvisionDate         | datetime      | YES        |            |           |               | 52%     | 130312     | 1999-05-17 00:00:00        | 2025-12-15 14:13:56.613000 |
| Order_service_id      | int           | YES        |            |           |               | 52%     | 141878     | 282                        | 7976644                    |
| products_name         | ntext         | YES        |            |           |               | ?       | ?          | —                          | —                          |
| currency              | nvarchar(3)   | YES        |            |           |               | 52%     | 4          | —                          | —                          |
| MRC                   | float(53)     | YES        |            |           |               | 52%     | 16258      | -26.36                     | 717509.9979                |
| NRC                   | float(53)     | YES        |            |           |               | 52%     | 1942       | -49.0                      | 546988.0                   |
| type                  | nvarchar(64)  | YES        |            |           |               | 52%     | 21         | —                          | —                          |
| DC                    | varchar(75)   | YES        |            |           |               | 52%     | 46         | —                          | —                          |
| product_line          | nvarchar(255) | YES        |            |           |               | 52%     | 5          | —                          | —                          |
| order_id              | int           | YES        |            |           |               | 52%     | 73351      | 1                          | 279323                     |
| name                  | nvarchar(32)  | YES        |            |           |               | 52%     | 2          | —                          | —                          |
| OrderDate             | datetime      | YES        |            |           |               | 52%     | 60354      | 1999-05-17 00:00:00        | 2025-12-11 16:05:41.380000 |
| promo_code            | nvarchar(32)  | YES        |            |           |               | 95%     | 99         | —                          | —                          |
| description           | varchar(75)   | YES        |            |           |               | 95%     | 96         | —                          | —                          |
| CancelDate            | datetime      | YES        |            |           |               | 65%     | 118621     | 2008-08-12 00:08:02.247000 | 2025-12-13 18:55:35.247000 |
| PendingClientApproval | datetime      | YES        |            |           |               | 56%     | 40977      | 2008-08-09 17:16:37.403000 | 2025-12-15 12:19:32.710000 |
| ClientApproved        | datetime      | YES        |            |           |               | 55%     | 48450      | 2008-08-10 00:06:30.750000 | 2025-12-15 13:50:04.230000 |
| OrderCanceled         | datetime      | YES        |            |           |               | 100%    | 162        | 2010-01-17 15:30:48.710000 | 2023-10-11 11:22:23.423000 |
| company_name          | nvarchar(255) | YES        |            |           |               | 52%     | 19715      | —                          | —                          |

---

### dbo.Waterfall_Normalized_removed_2025-09-10_JQ {#dbo-waterfall-normalized-removed-2025-09-10-jq}

| Property | Value |
|---|---|
| Full name | `[dbo].[Waterfall_Normalized_removed_2025-09-10_JQ]` |
| Row count | 1,692,347 |
| Total size | 648.3 MB |
| Used size | 648.2 MB |
| Created | 2025-09-08 05:29 |
| Schema modified | 2025-09-10 13:14 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                | Type          | Nullable   | Identity   | Default   | Description   | NULL%   | Distinct   | Min                        | Max                        |
|-----------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| gpinstance            | varchar(5)    | YES        |            |           |               | 7%      | 3          | —                          | —                          |
| SERVICE_ID            | char(21)      | YES        |            |           |               | 7%      | 19969      | —                          | —                          |
| CUSTNMBR              | char(15)      | YES        |            |           |               | 7%      | 8311       | —                          | —                          |
| GLPOSTDT              | datetime      | YES        |            |           |               | 7%      | 3346       | 2008-08-08 00:00:00        | 2025-09-07 00:00:00        |
| PeriodStart           | datetime      | YES        |            |           |               | 7%      | 4639       | 2008-01-01 00:00:00        | 2030-04-01 00:00:00        |
| PeriodEnd             | datetime      | YES        |            |           |               | 7%      | 4722       | 2008-01-31 00:00:00        | 2030-04-30 00:00:00        |
| xtndprce_period       | numeric(38,6) | YES        |            |           |               | 7%      | 535018     | -184065.000000             | 2241888.000000             |
| xtndprce_period_nx    | numeric(38,6) | YES        |            |           |               | 7%      | 263569     | -184744.100000             | 2241888.000000             |
| Location              | varchar(7)    | YES        |            |           |               | 7%      | 29         | —                          | —                          |
| Cost Center           | varchar(7)    | YES        |            |           |               | 7%      | 26         | —                          | —                          |
| Natural Account       | varchar(7)    | YES        |            |           |               | 7%      | 33         | —                          | —                          |
| Account               | varchar(51)   | YES        |            |           |               | 7%      | 483        | —                          | —                          |
| Customer Class        | varchar(15)   | YES        |            |           |               | 7%      | 11         | —                          | —                          |
| Customer              | varchar(65)   | YES        |            |           |               | 7%      | 8311       | —                          | —                          |
| orderstatus           | nvarchar(64)  | YES        |            |           |               | 53%     | 3          | —                          | —                          |
| ProvisionDate         | datetime      | YES        |            |           |               | 53%     | 130092     | 1999-05-17 00:00:00        | 2025-09-05 15:11:57.280000 |
| Order_service_id      | int           | YES        |            |           |               | 53%     | 141687     | 282                        | 7931652                    |
| products_name         | ntext         | YES        |            |           |               | ?       | ?          | —                          | —                          |
| currency              | nvarchar(3)   | YES        |            |           |               | 53%     | 4          | —                          | —                          |
| MRC                   | float(53)     | YES        |            |           |               | 53%     | 16235      | -26.36                     | 717509.9979                |
| NRC                   | float(53)     | YES        |            |           |               | 53%     | 1928       | -49.0                      | 546988.0                   |
| type                  | nvarchar(64)  | YES        |            |           |               | 53%     | 21         | —                          | —                          |
| DC                    | varchar(75)   | YES        |            |           |               | 53%     | 46         | —                          | —                          |
| product_line          | nvarchar(255) | YES        |            |           |               | 53%     | 5          | —                          | —                          |
| order_id              | int           | YES        |            |           |               | 53%     | 73222      | 1                          | 278743                     |
| name                  | nvarchar(32)  | YES        |            |           |               | 53%     | 2          | —                          | —                          |
| OrderDate             | datetime      | YES        |            |           |               | 53%     | 60225      | 1999-05-17 00:00:00        | 2025-09-02 14:53:07.430000 |
| promo_code            | nvarchar(32)  | YES        |            |           |               | 95%     | 99         | —                          | —                          |
| description           | varchar(75)   | YES        |            |           |               | 95%     | 96         | —                          | —                          |
| CancelDate            | datetime      | YES        |            |           |               | 65%     | 118853     | 2008-08-12 00:08:02.247000 | 2025-09-06 20:00:46.923000 |
| PendingClientApproval | datetime      | YES        |            |           |               | 57%     | 40848      | 2008-08-09 17:16:37.403000 | 2025-09-03 09:21:17.147000 |
| ClientApproved        | datetime      | YES        |            |           |               | 56%     | 48321      | 2008-08-10 00:06:30.750000 | 2025-09-05 07:46:04.023000 |
| OrderCanceled         | datetime      | YES        |            |           |               | 100%    | 162        | 2010-01-17 15:30:48.710000 | 2023-10-11 11:22:23.423000 |
| company_name          | nvarchar(255) | YES        |            |           |               | 53%     | 19712      | —                          | —                          |

---

### dbo.Waterfall_Revenue_Normalized {#dbo-waterfall-revenue-normalized}

| Property | Value |
|---|---|
| Full name | `[dbo].[Waterfall_Revenue_Normalized]` |
| Row count | 7,721,416 |
| Total size | 4.1 GB |
| Used size | 4.1 GB |
| Created | 2026-03-07 04:44 |
| Schema modified | 2026-03-07 04:44 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| ITEMNMBR                    | char(31)      | NO         |            |           |               | 0%      |       3317 | —                   | —                   |
| DOCDATE                     | datetime      | NO         |            |           |               | 0%      |       3147 | 2017-01-01 00:00:00 | 2026-03-06 00:00:00 |
| DOCNUMBR                    | char(21)      | NO         |            |           |               | 0%      |     376564 | —                   | —                   |
| gpinstance                  | varchar(5)    | NO         |            |           |               | 0%      |          6 | —                   | —                   |
| SERVICE_ID                  | char(21)      | YES        |            |           |               | 0%      |      21214 | —                   | —                   |
| Customer                    | varchar(81)   | YES        |            |           |               | 0%      |       6073 | —                   | —                   |
| client_id                   | varchar(15)   | YES        |            |           |               | 0%      |       6073 | —                   | —                   |
| Doc Status                  | varchar(5)    | NO         |            |           |               | 0%      |          2 | —                   | —                   |
| Void Date                   | datetime      | NO         |            |           |               | 0%      |        170 | 1900-01-01 00:00:00 | 2025-12-08 00:00:00 |
| GLPOSTDT                    | datetime      | NO         |            |           |               | 0%      |       2521 | 2017-01-01 00:00:00 | 2026-03-07 00:00:00 |
| PeriodStart                 | datetime      | YES        |            |           |               | 0%      |       3426 | 2017-01-01 00:00:00 | 2030-04-01 00:00:00 |
| PeriodEnd                   | datetime      | YES        |            |           |               | 0%      |       3480 | 2017-01-01 00:00:00 | 2030-04-30 00:00:00 |
| origprce_period             | numeric(38,6) | YES        |            |           |               | 0%      |    1038592 | -246108.885000      | 2241888.000000      |
| origprce_period_nx          | numeric(38,6) | YES        |            |           |               | 0%      |     259409 | -330000.000000      | 2500000.000000      |
| xtndprce_period             | numeric(38,6) | YES        |            |           |               | 0%      |    1094932 | -334225.710185      | 2241888.000000      |
| xtndprce_period_nx          | numeric(38,6) | YES        |            |           |               | 0%      |     389207 | -448153.200000      | 2500000.000000      |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |          8 | —                   | —                   |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |         31 | —                   | —                   |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |         28 | —                   | —                   |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |         18 | —                   | —                   |
| Original Posting Accounting | varchar(181)  | YES        |            |           |               | 0%      |        482 | —                   | —                   |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |        479 | —                   | —                   |
| Customer Class              | varchar(15)   | YES        |            |           |               | 0%      |         10 | —                   | —                   |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |         20 | —                   | —                   |
| Class                       | varchar(21)   | YES        |            |           |               | 0%      |         18 | —                   | —                   |
| lnitmseq                    | int           | NO         |            |           |               | 0%      |      26496 | 8192                | 444006400           |

---

### dbo.Waterfall_Revenue_Normalized_Compressed {#dbo-waterfall-revenue-normalized-compressed}

| Property | Value |
|---|---|
| Full name | `[dbo].[Waterfall_Revenue_Normalized_Compressed]` |
| Row count | 60,049 |
| Total size | 18.4 MB |
| Used size | 18.3 MB |
| Created | 2026-03-07 05:09 |
| Schema modified | 2026-03-07 05:09 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| gpinstance                  | varchar(5)    | NO         |            |           |               | 0%      |          6 | —                   | —                   |
| Posted Month                | int           | YES        |            |           |               | 0%      |        111 | 201701              | 202603              |
| Revenue Month               | datetime      | YES        |            |           |               | 0%      |        160 | 2017-01-31 23:59:59 | 2030-04-30 23:59:59 |
| USD MRR                     | numeric(38,6) | YES        |            |           |               | 0%      |      48458 | -229750.258911      | 3201120.000000      |
| FC MRR                      | numeric(38,6) | YES        |            |           |               | 0%      |      34346 | -291674.840000      | 3498898.590000      |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |          8 | —                   | —                   |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |         31 | —                   | —                   |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |         28 | —                   | —                   |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |         18 | —                   | —                   |
| Original Posting Accounting | varchar(181)  | YES        |            |           |               | 0%      |        482 | —                   | —                   |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |        479 | —                   | —                   |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |         20 | —                   | —                   |
| FiscalYear                  | smallint      | YES        |            |           |               | 0%      |         14 | 2017                | 2030                |
| FiscalPeriod                | smallint      | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| FiscalQuarter               | varchar(2)    | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| Doc Status                  | varchar(5)    | NO         |            |           |               | 0%      |          2 | —                   | —                   |
| is_EMEA                     | varchar(3)    | NO         |            |           |               | 0%      |          2 | —                   | —                   |

---

### dbo.Waterfall_Revenue_Normalized_Invoice {#dbo-waterfall-revenue-normalized-invoice}

| Property | Value |
|---|---|
| Full name | `[dbo].[Waterfall_Revenue_Normalized_Invoice]` |
| Row count | 2,914,196 |
| Total size | 1.3 GB |
| Used size | 1.3 GB |
| Created | 2013-03-06 09:18 |
| Schema modified | 2013-03-06 09:18 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| DOCNUMBR                    | char(21)      | NO         |            |           |               | 0%      |     726196 | —                   | —                   |
| gpinstance                  | varchar(5)    | NO         |            |           |               | 0%      |          3 | —                   | —                   |
| SERVICE_ID                  | char(21)      | YES        |            |           |               | 5%      |      68550 | —                   | —                   |
| Customer                    | varchar(81)   | YES        |            |           |               | 0%      |      17313 | —                   | —                   |
| Doc Status                  | varchar(5)    | NO         |            |           |               | 0%      |          2 | —                   | —                   |
| Void Date                   | datetime      | NO         |            |           |               | 0%      |        731 | 1900-01-01 00:00:00 | 2013-03-01 00:00:00 |
| GLPOSTDT                    | datetime      | NO         |            |           |               | 0%      |       1458 | 2008-01-01 00:00:00 | 2013-03-05 00:00:00 |
| PeriodStart                 | datetime      | YES        |            |           |               | 0%      |       2020 | 2007-11-01 00:00:00 | 2016-06-01 00:00:00 |
| PeriodEnd                   | datetime      | YES        |            |           |               | 0%      |       2701 | 2007-11-01 00:00:00 | 2016-06-30 00:00:00 |
| xtndprce_period             | numeric(38,6) | YES        |            |           |               | 1%      |     483896 | -69607.355884       | 215026.199000       |
| xtndprce_period_nx          | numeric(38,6) | YES        |            |           |               | 0%      |     312623 | -80112.500000       | 198076.330000       |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |         11 | —                   | —                   |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |         19 | —                   | —                   |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |         22 | —                   | —                   |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |         80 | —                   | —                   |
| Original Posting Accounting | varchar(181)  | YES        |            |           |               | 0%      |        562 | —                   | —                   |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |        559 | —                   | —                   |
| Customer Class              | varchar(15)   | YES        |            |           |               | 0%      |          6 | —                   | —                   |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |         17 | —                   | —                   |
| Class                       | varchar(21)   | YES        |            |           |               | 0%      |         11 | —                   | —                   |
| FiscalYear                  | smallint      | YES        |            |           |               | 0%      |          9 | 2008                | 2016                |

---

### dbo.Waterfall_Revenue_Normalized_Invoice_Details {#dbo-waterfall-revenue-normalized-invoice-details}

| Property | Value |
|---|---|
| Full name | `[dbo].[Waterfall_Revenue_Normalized_Invoice_Details]` |
| Row count | 227,065 |
| Total size | 24.3 MB |
| Used size | 24.3 MB |
| Created | 2011-08-05 14:12 |
| Schema modified | 2011-08-05 14:12 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column         | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min     | Max          |
|----------------|---------------|------------|------------|-----------|---------------|---------|------------|---------|--------------|
| GPInstance     | varchar(5)    | NO         |            |           |               | 0%      |          3 | —       | —            |
| CUSTNMBR       | char(15)      | NO         |            |           |               | 0%      |      11969 | —       | —            |
| Customer Name  | varchar(65)   | YES        |            |           |               | 0%      |      11800 | —       | —            |
| DOCNUMBR       | char(21)      | NO         |            |           |               | 0%      |     227065 | —       | —            |
| GL Posted Date | char(10)      | YES        |            |           |               | 0%      |        628 | —       | —            |
| AMOUNT         | numeric(19,5) | NO         |            |           |               | 0%      |      35113 | 0.01000 | 230857.86000 |
| DUE Date       | char(10)      | YES        |            |           |               | 0%      |        889 | —       | —            |
| Currency       | varchar(15)   | YES        |            |           |               | 0%      |          4 | —       | —            |

---

### dbo.Waterfall_Revenue_Normalized_NewLOB {#dbo-waterfall-revenue-normalized-newlob}

| Property | Value |
|---|---|
| Full name | `[dbo].[Waterfall_Revenue_Normalized_NewLOB]` |
| Row count | 0 |
| Total size | 0.1 MB |
| Used size | 0.0 MB |
| Created | 2021-04-06 19:35 |
| Schema modified | 2021-04-06 19:35 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max   |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|-------|-------|
| DOCDATE                     | datetime      | NO         |            |           |               | 0%      |          0 | NULL  | NULL  |
| DOCNUMBR                    | char(21)      | NO         |            |           |               | 0%      |          0 | —     | —     |
| gpinstance                  | varchar(5)    | NO         |            |           |               | 0%      |          0 | —     | —     |
| SERVICE_ID                  | char(21)      | YES        |            |           |               | 0%      |          0 | —     | —     |
| Customer                    | varchar(81)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| client_id                   | varchar(15)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| Doc Status                  | varchar(5)    | NO         |            |           |               | 0%      |          0 | —     | —     |
| Void Date                   | datetime      | NO         |            |           |               | 0%      |          0 | NULL  | NULL  |
| GLPOSTDT                    | datetime      | NO         |            |           |               | 0%      |          0 | NULL  | NULL  |
| PeriodStart                 | datetime      | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| PeriodEnd                   | datetime      | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| origprce_period             | numeric(38,6) | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| origprce_period_nx          | numeric(38,6) | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| xtndprce_period             | numeric(38,6) | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| xtndprce_period_nx          | numeric(38,6) | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| Original Posting Accounting | varchar(181)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| Customer Class              | varchar(15)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| Class                       | varchar(21)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| new_lob                     | nvarchar(255) | YES        |            |           |               | 0%      |          0 | —     | —     |

---

### dbo.WaterFall_Revenue_Summary_Normalized {#dbo-waterfall-revenue-summary-normalized}

| Property | Value |
|---|---|
| Full name | `[dbo].[WaterFall_Revenue_Summary_Normalized]` |
| Row count | 646,814 |
| Total size | 265.5 MB |
| Used size | 265.5 MB |
| Created | 2026-03-07 05:06 |
| Schema modified | 2026-03-07 05:06 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| gpinstance                  | varchar(5)    | NO         |            |           |               | 0%      |          6 | —                   | —                   |
| Posted Month                | int           | YES        |            |           |               | 0%      |        111 | 201701              | 202603              |
| Revenue Month               | datetime      | YES        |            |           |               | 0%      |        160 | 2017-01-31 23:59:59 | 2030-04-30 23:59:59 |
| USD MRR                     | numeric(38,6) | YES        |            |           |               | 0%      |     316079 | -229750.258911      | 3201120.000000      |
| FC MRR                      | numeric(38,6) | YES        |            |           |               | 0%      |     167520 | -291674.840000      | 3498898.590000      |
| client_id                   | varchar(15)   | YES        |            |           |               | 0%      |       6073 | —                   | —                   |
| Customer                    | varchar(81)   | YES        |            |           |               | 0%      |       6073 | —                   | —                   |
| CLass                       | varchar(21)   | YES        |            |           |               | 0%      |         18 | —                   | —                   |
| Doc Status                  | varchar(5)    | NO         |            |           |               | 0%      |          2 | —                   | —                   |
| Void Date                   | datetime      | NO         |            |           |               | 0%      |        170 | 1900-01-01 00:00:00 | 2025-12-08 00:00:00 |
| Entity                      | varchar(99)   | YES        |            |           |               | 0%      |          8 | —                   | —                   |
| Location                    | varchar(99)   | YES        |            |           |               | 0%      |         31 | —                   | —                   |
| Cost Centre                 | varchar(99)   | YES        |            |           |               | 0%      |         28 | —                   | —                   |
| Natural Account             | varchar(39)   | YES        |            |           |               | 0%      |         18 | —                   | —                   |
| Original Posting Accounting | varchar(181)  | YES        |            |           |               | 0%      |        482 | —                   | —                   |
| Account Description         | varchar(181)  | YES        |            |           |               | 0%      |        479 | —                   | —                   |
| Customer Class              | varchar(15)   | YES        |            |           |               | 0%      |         10 | —                   | —                   |
| Category                    | varchar(51)   | YES        |            |           |               | 0%      |         20 | —                   | —                   |
| is_EMEA                     | varchar(3)    | NO         |            |           |               | 0%      |          2 | —                   | —                   |

---

### dbo.zunicore_credits {#dbo-zunicore-credits}

| Property | Value |
|---|---|
| Full name | `[dbo].[zunicore_credits]` |
| Row count | 11,753 |
| Total size | 2.5 MB |
| Used size | 2.4 MB |
| Created | 2018-06-05 04:00 |
| Schema modified | 2018-06-05 04:00 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column        | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|---------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| invid         | int           | YES        |            |           |               | 0%      |       5128 | 790                 | 37336               |
| clientid      | int           | NO         |            |           |               | 0%      |       1269 | 1051                | 36655               |
| paid          | int           | NO         |            |           |               | 0%      |          3 | 0                   | 2                   |
| creditdate    | datetime2     | YES        |            |           |               | 0%      |        804 | 2011-11-08 00:00:00 | 2016-01-28 01:00:00 |
| creditapplied | float(53)     | NO         |            |           |               | 0%      |       3752 | -2438.64            | -0.01               |
| reason        | nvarchar(255) | NO         |            |           |               | 0%      |       1841 | —                   | —                   |
| period_start  | datetime2     | YES        |            |           |               | 0%      |       3840 | 2011-11-17 01:39:03 | 2016-03-25 04:30:02 |
| period_end    | datetime2     | YES        |            |           |               | 0%      |       3835 | 2011-12-16 01:39:03 | 2016-04-24 04:30:02 |
| deferred      | nvarchar(3)   | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| ispaid        | varchar(11)   | YES        |            |           |               | 0%      |          3 | —                   | —                   |

---

### dbo.zunicore_credits_deferred_normalized {#dbo-zunicore-credits-deferred-normalized}

| Property | Value |
|---|---|
| Full name | `[dbo].[zunicore_credits_deferred_normalized]` |
| Row count | 12,609 |
| Total size | 3.5 MB |
| Used size | 3.4 MB |
| Created | 2018-06-05 04:00 |
| Schema modified | 2018-06-05 04:00 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column        | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                    |
|---------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|------------------------|
| invid         | int           | YES        |            |           |               | 0%      |       2818 | 790                 | 36712                  |
| creditdate    | datetime2     | YES        |            |           |               | 0%      |        667 | 2011-11-08 00:00:00 | 2016-01-15 01:00:00    |
| clientid      | int           | NO         |            |           |               | 0%      |       1196 | 1051                | 36655                  |
| period_start  | datetime2     | YES        |            |           |               | 0%      |       2703 | 2011-11-17 01:39:03 | 2016-01-24 04:30:01    |
| period_end    | datetime2     | YES        |            |           |               | 0%      |       2699 | 2011-12-16 01:39:03 | 2016-02-23 04:30:01    |
| creditapplied | float(53)     | NO         |            |           |               | 0%      |       2523 | -2438.64            | -0.01                  |
| reason        | nvarchar(255) | NO         |            |           |               | 0%      |       1310 | —                   | —                      |
| deferred      | nvarchar(3)   | YES        |            |           |               | 0%      |          1 | —                   | —                      |
| ispaid        | varchar(11)   | YES        |            |           |               | 0%      |          3 | —                   | —                      |
| totaldays     | numeric(24,6) | YES        |            |           |               | 0%      |          4 | 29.000000           | 31.000000              |
| PeriodStart   | datetime2     | YES        |            |           |               | 0%      |       2754 | 2011-11-17 01:39:03 | 2016-02-01 00:00:00    |
| PeriodEnd     | datetime2     | YES        |            |           |               | 0%      |       2716 | 2011-11-30 00:00:00 | 2016-02-23 04:30:01    |
| PeriodDays    | numeric(26,6) | YES        |            |           |               | 0%      |         61 | 0.416666            | 31.000000              |
| value_period  | float(53)     | YES        |            |           |               | 0%      |       9488 | -1692.105584982917  | -0.0006849304259710779 |

---

### dbo.zunicore_invoices {#dbo-zunicore-invoices}

| Property | Value |
|---|---|
| Full name | `[dbo].[zunicore_invoices]` |
| Row count | 115,936 |
| Total size | 26.5 MB |
| Used size | 26.4 MB |
| Created | 2018-06-05 04:00 |
| Schema modified | 2018-06-05 04:00 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column       | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|--------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| invid        | int           | YES        |            |           |               | 0%      |      22865 | 790                 | 37362               |
| packid       | int           | NO         |            |           |               | 0%      |      29039 | 57                  | 58790               |
| invoice_date | datetime2     | YES        |            |           |               | 0%      |       8917 | 2011-11-17 01:39:03 | 2016-03-27 04:30:01 |
| duedate      | datetime2     | YES        |            |           |               | 0%      |       1539 | 2011-12-03 00:00:00 | 2016-03-27 01:00:00 |
| clientid     | int           | NO         |            |           |               | 0%      |       1889 | 1018                | 36665               |
| ispaid       | varchar(11)   | YES        |            |           |               | 0%      |          3 | —                   | —                   |
| datepaid     | datetime2     | YES        |            |           |               | 0%      |      10235 | 1969-12-31 19:00:00 | 2016-05-12 06:39:40 |
| section      | nvarchar(255) | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| desserv      | nvarchar(255) | YES        |            |           |               | 0%      |        458 | —                   | —                   |
| servtype     | nvarchar(255) | YES        |            |           |               | 0%      |         18 | —                   | —                   |
| period_start | datetime2     | YES        |            |           |               | 0%      |       1900 | 2011-11-17 00:00:00 | 2016-03-27 01:00:00 |
| period_end   | datetime2     | YES        |            |           |               | 0%      |       1584 | 1969-12-31 19:00:00 | 2016-04-27 01:00:00 |
| quantity     | float(53)     | NO         |            |           |               | 0%      |        411 | 0.0                 | 176128.0            |
| value        | float(53)     | NO         |            |           |               | 0%      |       1793 | 0.0                 | 4453.07             |
| unpaid       | float(53)     | NO         |            |           |               | 0%      |        845 | 0.0                 | 4453.07             |
| paid         | float(53)     | NO         |            |           |               | 0%      |       1806 | 0.0                 | 4158.0              |
| duedays      | int           | YES        |            |           |               | 0%      |       1537 | 800                 | 2376                |

---

### dbo.zunicore_invoices_deferred_normalized {#dbo-zunicore-invoices-deferred-normalized}

| Property | Value |
|---|---|
| Full name | `[dbo].[zunicore_invoices_deferred_normalized]` |
| Row count | 226,411 |
| Total size | 62.0 MB |
| Used size | 62.0 MB |
| Created | 2018-06-05 04:00 |
| Schema modified | 2018-06-05 04:00 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column       | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|--------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| invid        | int           | YES        |            |           |               | 0%      |      22615 | 790                 | 37362               |
| packid       | int           | NO         |            |           |               | 0%      |      26395 | 57                  | 58790               |
| invoice_date | datetime2     | YES        |            |           |               | 0%      |       8679 | 2011-11-17 01:39:03 | 2016-03-27 04:30:01 |
| duedate      | datetime2     | YES        |            |           |               | 0%      |       1539 | 2011-12-03 00:00:00 | 2016-03-27 01:00:00 |
| clientid     | int           | NO         |            |           |               | 0%      |       1888 | 1018                | 36665               |
| ispaid       | varchar(11)   | YES        |            |           |               | 0%      |          3 | —                   | —                   |
| datepaid     | datetime2     | YES        |            |           |               | 0%      |       9995 | 1969-12-31 19:00:00 | 2016-05-12 06:39:40 |
| section      | nvarchar(255) | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| desserv      | nvarchar(255) | YES        |            |           |               | 0%      |        199 | —                   | —                   |
| servtype     | nvarchar(255) | YES        |            |           |               | 0%      |         13 | —                   | —                   |
| period_start | datetime2     | YES        |            |           |               | 0%      |       1900 | 2011-11-17 00:00:00 | 2016-03-27 01:00:00 |
| period_end   | datetime2     | YES        |            |           |               | 0%      |       1583 | 2011-12-07 00:00:00 | 2016-04-27 01:00:00 |
| quantity     | float(53)     | NO         |            |           |               | 0%      |        360 | 0.0                 | 176128.0            |
| value        | float(53)     | NO         |            |           |               | 0%      |       1712 | 0.0                 | 3522.56             |
| unpaid       | float(53)     | NO         |            |           |               | 0%      |        836 | 0.0                 | 921.6               |
| paid         | float(53)     | NO         |            |           |               | 0%      |       1740 | 0.0                 | 3522.56             |
| totaldays    | numeric(24,6) | YES        |            |           |               | 0%      |         36 | -10.000000          | 33.000000           |
| PeriodStart  | datetime2     | YES        |            |           |               | 0%      |       1949 | 2011-11-17 00:00:00 | 2016-04-01 00:00:00 |
| PeriodEnd    | datetime2     | YES        |            |           |               | 0%      |       1617 | 2011-11-30 00:00:00 | 2016-04-27 01:00:00 |
| PeriodDays   | numeric(26,6) | YES        |            |           |               | 0%      |         63 | -10.000000          | 31.000000           |
| value_period | float(53)     | YES        |            |           |               | 0%      |      10865 | 0.0                 | 2993.548387096774   |

---

### dbo.zunicore_revenue {#dbo-zunicore-revenue}

| Property | Value |
|---|---|
| Full name | `[dbo].[zunicore_revenue]` |
| Row count | 247,092 |
| Total size | 17.4 MB |
| Used size | 17.4 MB |
| Created | 2018-06-05 04:01 |
| Schema modified | 2018-06-05 04:01 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column      | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| invid       | int           | YES        |            |           |               | 0%      |      22865 | 790                 | 37362               |
| clientid    | int           | NO         |            |           |               | 0%      |       1889 | 1018                | 36665               |
| ispaid      | varchar(11)   | YES        |            |           |               | 0%      |          3 | —                   | —                   |
| servtype    | nvarchar(255) | YES        |            |           |               | 0%      |         19 | —                   | —                   |
| PeriodStart | datetime2     | YES        |            |           |               | 0%      |       4663 | 2011-11-08 00:00:00 | 2016-04-01 00:00:00 |
| revenue     | float(53)     | YES        |            |           |               | 0%      |      22701 | -2370.6             | 4453.07             |
| type        | varchar(7)    | NO         |            |           |               | 0%      |          2 | —                   | —                   |

---

## Views

_(none)_

---

## Stored Procedures

_(none)_

---

## Functions

_(none)_

---

## Triggers

_(none)_

---

## SQL Agent Jobs

_(none or access denied)_

---

## Cross-Database References

_(none detected)_
