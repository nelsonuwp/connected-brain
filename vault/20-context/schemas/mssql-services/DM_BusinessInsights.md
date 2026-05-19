# Database Report — `DM_BusinessInsights`

> Generated: 2026-03-07 07:22:59  
> Tables: 56  |  Views: 2  |  Procedures: 0  |  Functions: 5  |  Triggers: 0

---

## Table of Contents

**Tables**

- [dbo.at_risk_sfdc](#dbo-at-risk-sfdc) — 51 rows  `0.1 MB`
- [dbo.Churn](#dbo-churn) — 7,667 rows  `5.9 MB`
- [dbo.churn_month_to_date](#dbo-churn-month-to-date) — 9 rows  `0.2 MB`
- [dbo.cost_software_skus](#dbo-cost-software-skus) — 391 rows  `0.1 MB`
- [dbo.DateDimension](#dbo-datedimension) — 11,688 rows  `1.7 MB`
- [dbo.dimChangeControl](#dbo-dimchangecontrol) — 21,788 rows  `16.1 MB`
- [dbo.dimClientsActive](#dbo-dimclientsactive) — 778 rows  `5.5 MB`
- [dbo.dimClientsActive_historical](#dbo-dimclientsactive-historical) — 5,051,942 rows  `4.2 GB`
- [dbo.dimCloud_OtherUsageCharges](#dbo-dimcloud-otherusagecharges) — 34,284 rows  `47.9 MB`
- [dbo.dimComponents](#dbo-dimcomponents) — 1,618,569 rows  `702.0 MB`
- [dbo.dimComponents_TTSSiteScout](#dbo-dimcomponents-ttssitescout) — 176,660 rows  `78.5 MB`
- [dbo.dimCredits](#dbo-dimcredits) — 168,071 rows  `211.6 MB`
- [dbo.dimCurrencyExchangeRates](#dbo-dimcurrencyexchangerates) — 4,086 rows  `1.2 MB`
- [dbo.dimCustomerAttributes](#dbo-dimcustomerattributes) — 25,188 rows  `10.9 MB`
- [dbo.DimCustomerContacts](#dbo-dimcustomercontacts) — 99,479 rows  `12.5 MB`
- [dbo.dimdatacenterattributes](#dbo-dimdatacenterattributes) — 53 rows  `0.0 MB`
- [dbo.DimDCIMAssets](#dbo-dimdcimassets) — 0 rows  `0.0 MB`
- [dbo.DimDCIMAssets_old](#dbo-dimdcimassets-old) — 10,000 rows  `29.9 MB`
- [dbo.dimDCIMAssetsTrend](#dbo-dimdcimassetstrend) — 25,214 rows  `170.6 MB`
- [dbo.dimDevices](#dbo-dimdevices) — 3,224 rows  `11.6 MB`
- [dbo.dimJIRATickets](#dbo-dimjiratickets) — 124,083 rows  `37.2 MB`
- [dbo.dimNotes](#dbo-dimnotes) — 9,489 rows  `5.7 MB`
- [dbo.dimOpportunities](#dbo-dimopportunities) — 14,216 rows  `28.9 MB`
- [dbo.dimProduct](#dbo-dimproduct) — 17 rows  `0.1 MB`
- [dbo.dimProductAttributes](#dbo-dimproductattributes) — 7,101 rows  `4.4 MB`
- [dbo.dimProductRevenue](#dbo-dimproductrevenue) — 1,901,954 rows  `807.9 MB`
- [dbo.dimsalesrepscp1](#dbo-dimsalesrepscp1) — 11 rows  `0.1 MB`
- [dbo.dimServiceAttributes](#dbo-dimserviceattributes) — 162,720 rows  `62.0 MB`
- [dbo.dimServices](#dbo-dimservices) — 5,831 rows  `27.1 MB`
- [dbo.dimServices_TTSSiteScout](#dbo-dimservices-ttssitescout) — 1,046 rows  `0.6 MB`
- [dbo.DimTLSAttributes](#dbo-dimtlsattributes) — 222 rows  `0.1 MB`
- [dbo.mrc_changes](#dbo-mrc-changes) — 476,409 rows  `74.6 MB`
- [dbo.MRCTrend](#dbo-mrctrend) — 327,457 rows  `135.7 MB`
- [dbo.MRCTrend_TTSSiteScout](#dbo-mrctrend-ttssitescout) — 63,911 rows  `26.8 MB`
- [dbo.MrcTrendColo](#dbo-mrctrendcolo) — 131,000 rows  `57.6 MB`
- [dbo.order_notes_sharepoint_raw](#dbo-order-notes-sharepoint-raw) — 0 rows  `0.1 MB`
- [dbo.PopularSalesInventoryTrend](#dbo-popularsalesinventorytrend) — 5,693,844 rows  `1.8 GB`
- [dbo.product_special_attributes](#dbo-product-special-attributes) — 279 rows  `0.1 MB`
- [dbo.run_rate_by_customer](#dbo-run-rate-by-customer) — 249,830 rows  `90.7 MB`
- [dbo.Sales](#dbo-sales) — 11,073 rows  `8.2 MB`
- [dbo.sales_month_to_date](#dbo-sales-month-to-date) — 64 rows  `0.1 MB`
- [dbo.sales_salestracker](#dbo-sales-salestracker) — 34,318 rows  `54.2 MB`
- [dbo.SalesBookOfBusiness](#dbo-salesbookofbusiness) — 13,245 rows  `2.3 MB`
- [dbo.salesforce_open_opportunities_trend](#dbo-salesforce-open-opportunities-trend) — 5,495,524 rows  `2.3 GB`
- [dbo.salesforce_opportunity_trend](#dbo-salesforce-opportunity-trend) — 13,427,219 rows  `12.7 GB`
- [dbo.software_skus](#dbo-software-skus) — 569 rows  `0.1 MB`
- [dbo.tasks](#dbo-tasks) — 504,296 rows  `439.3 MB`
- [dbo.tasks_history](#dbo-tasks-history) — 658,955 rows  `91.3 MB`
- [dbo.Tickets](#dbo-tickets) — 851,065 rows  `785.4 MB`
- [dbo.Tickets_JSM](#dbo-tickets-jsm) — 0 rows  `0.0 MB`
- [dbo.utility_billing_tracker](#dbo-utility-billing-tracker) — 246 rows  `0.1 MB`
- [profitability.alertlogic_invoice_details](#profitability-alertlogic-invoice-details) — 242 rows  `0.1 MB`
- [profitability.imperva_invoice_details](#profitability-imperva-invoice-details) — 552 rows  `0.1 MB`
- [profitability.hardware_watts](#profitability-hardware-watts) — 20 rows  `0.0 MB`
- [profitability.ocean_sku_cost](#profitability-ocean-sku-cost) — 680 rows  `0.2 MB`
- [renewals.ocean_services_renewal_date](#renewals-ocean-services-renewal-date) — 5,735 rows  `0.8 MB`
- [renewals.ocean_services_renewal_date_new](#renewals-ocean-services-renewal-date-new) — 5,735 rows  `0.8 MB`

**Views**

- [dbo.dimproductattributes_extended](#view-dbo-dimproductattributes-extended)
- [dbo.last_thirty_days_avg_exchange_rate](#view-dbo-last-thirty-days-avg-exchange-rate)

**Stored Procedures**


**Functions**

- [dbo.SplitString](#func-dbo-splitstring) `SQL_TABLE_VALUED_FUNCTION`
- [dbo.tvf_client_active_history_view](#func-dbo-tvf-client-active-history-view) `SQL_INLINE_TABLE_VALUED_FUNCTION`
- [dbo.tvf_mrc_charges](#func-dbo-tvf-mrc-charges) `SQL_TABLE_VALUED_FUNCTION`
- [dbo.view_product_mrc](#func-dbo-view-product-mrc) `SQL_INLINE_TABLE_VALUED_FUNCTION`
- [dbo.view_product_skus](#func-dbo-view-product-skus) `SQL_INLINE_TABLE_VALUED_FUNCTION`

---

## Tables

### dbo.at_risk_sfdc {#dbo-at-risk-sfdc}

| Property | Value |
|---|---|
| Full name | `[dbo].[at_risk_sfdc]` |
| Row count | 51 |
| Total size | 0.1 MB |
| Used size | 0.0 MB |
| Created | 2025-09-04 06:01 |
| Schema modified | 2025-09-04 06:01 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column         | Type         | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max   |
|----------------|--------------|------------|------------|-----------|---------------|---------|------------|-------|-------|
| client_id      | nvarchar(50) | YES        |            |           |               | 0%      |         51 | —     | —     |
| at_risk_record | varchar(3)   | NO         |            |           |               | 0%      |          1 | —     | —     |

---

### dbo.Churn {#dbo-churn}

| Property | Value |
|---|---|
| Full name | `[dbo].[Churn]` |
| Row count | 7,667 |
| Total size | 5.9 MB |
| Used size | 5.3 MB |
| Created | 2015-06-04 14:21 |
| Schema modified | 2022-08-01 11:13 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                    | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|---------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| integer_key               | int           | NO         |            |           |               | 0%      |       7667 | 140169                     | 149067                     |
| churn_class               | nvarchar(255) | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| cancel_date               | datetime2     | YES        |            |           |               | 0%      |       7386 | 2022-03-01 18:55:02.932876 | 2026-02-28 18:55:43.055569 |
| client_type               | nvarchar(255) | YES        |            |           |               | 0%      |          8 | —                          | —                          |
| client_id_company         | nvarchar(255) | YES        |            |           |               | 0%      |        970 | —                          | —                          |
| service_id                | nvarchar(255) | YES        |            |           |               | 0%      |       6615 | —                          | —                          |
| nickname                  | nvarchar(255) | YES        |            |           |               | 0%      |       6334 | —                          | —                          |
| product                   | nvarchar(255) | YES        |            |           |               | 0%      |        288 | —                          | —                          |
| os                        | nvarchar(255) | YES        |            |           |               | 33%     |        196 | —                          | —                          |
| cancel_reason             | nvarchar(255) | YES        |            |           |               | 1%      |         25 | —                          | —                          |
| start_date                | datetime2     | YES        |            |           |               | 1%      |       6490 | 2004-05-12 15:33:56.301640 | 2025-12-03 10:10:26.549423 |
| accounts_left             | int           | YES        |            |           |               | 0%      |        180 | 0                          | 1757                       |
| line_of_business          | nvarchar(255) | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| months_online             | int           | YES        |            |           |               | 1%      |        183 | 0                          | 260                        |
| datacenter_code           | nvarchar(15)  | YES        |            |           |               | 0%      |         38 | —                          | —                          |
| is_emea                   | nvarchar(3)   | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| migration_start           | datetime2     | YES        |            |           |               | 100%    |          2 | 2020-01-09 06:02:06.231307 | 2021-12-06 11:54:05.292793 |
| tam                       | nvarchar(255) | YES        |            |           |               | 54%     |         14 | —                          | —                          |
| last_45_days              | nvarchar(255) | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| is_migration              | nvarchar(255) | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| bdc                       | nvarchar(255) | YES        |            |           |               | 2%      |         49 | —                          | —                          |
| currency                  | nvarchar(255) | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| original_currency_mrc     | numeric(38,2) | YES        |            |           |               | 0%      |       2747 | 0.00                       | 22711.38                   |
| contract_term             | nvarchar(255) | YES        |            |           |               | 0%      |         31 | —                          | —                          |
| service_type              | nvarchar(255) | YES        |            |           |               | 0%      |         18 | —                          | —                          |
| shopping_cart             | nvarchar(255) | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| promotion                 | nvarchar(255) | YES        |            |           |               | 97%     |          4 | —                          | —                          |
| comments                  | nvarchar(MAX) | YES        |            |           |               | 24%     |       1539 | —                          | —                          |
| usd_mrc                   | numeric(38,2) | YES        |            |           |               | 0%      |       3040 | 0.00                       | 24103.49                   |
| client_id                 | int           | YES        |            |           |               | 0%      |        959 | 1000329                    | 7036692                    |
| short_term                | int           | YES        |            |           |               | 80%     |          1 | 0                          | 0                          |
| cad_mrc                   | numeric(38,2) | YES        |            |           |               | 0%      |       3163 | 0.00                       | 31702.89                   |
| cad_budget_mrc            | numeric(38,4) | YES        |            |           |               | 0%      |       2896 | 0.0000                     | 29700.0000                 |
| adjusted_line_of_business | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| date_captured             | datetime2     | YES        |            |           |               | 0%      |         49 | 2022-03-31 08:46:00.683333 | 2026-02-28 08:46:00.606666 |

#### Indexes

| Name     | Type      | Unique   | PK   | Columns     |
|----------|-----------|----------|------|-------------|
| PK_Churn | CLUSTERED | YES      | ✓    | integer_key |

---

### dbo.churn_month_to_date {#dbo-churn-month-to-date}

| Property | Value |
|---|---|
| Full name | `[dbo].[churn_month_to_date]` |
| Row count | 9 |
| Total size | 0.2 MB |
| Used size | 0.1 MB |
| Created | 2015-06-04 14:32 |
| Schema modified | 2020-04-17 10:25 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                    | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|---------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| integer_key               | int           | NO         |            |           |               | 0%      |          9 | 5                          | 23                         |
| churn_class               | nvarchar(255) | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| cancel_date               | datetime2     | YES        |            |           |               | 0%      |          9 | 2026-03-02 15:00:03.786279 | 2026-03-05 18:55:25.294760 |
| client_type               | nvarchar(255) | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| service_id                | nvarchar(255) | YES        |            |           |               | 0%      |          9 | —                          | —                          |
| nickname                  | nvarchar(255) | YES        |            |           |               | 0%      |          9 | —                          | —                          |
| product                   | nvarchar(255) | YES        |            |           |               | 0%      |          7 | —                          | —                          |
| os                        | nvarchar(255) | YES        |            |           |               | 89%     |          1 | —                          | —                          |
| cancel_reason             | nvarchar(255) | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| start_date                | datetime2     | YES        |            |           |               | 0%      |          9 | 2021-02-12 12:20:06.408747 | 2025-01-10 14:20:55.427107 |
| accounts_left             | int           | YES        |            |           |               | 0%      |          4 | 0                          | 202                        |
| line_of_business          | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| months_online             | int           | YES        |            |           |               | 0%      |          8 | 13                         | 61                         |
| datacenter_code           | nvarchar(15)  | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| is_emea                   | nvarchar(3)   | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| migration_start           | datetime2     | YES        |            |           |               | 100%    |          0 | NULL                       | NULL                       |
| tam                       | nvarchar(255) | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| last_45_days              | nvarchar(255) | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| is_migration              | nvarchar(255) | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| bdc                       | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| currency                  | nvarchar(255) | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| original_currency_mrc     | numeric(38,2) | YES        |            |           |               | 0%      |          7 | 0.00                       | 1273.50                    |
| contract_length           | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| service_type              | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| shopping_cart             | nvarchar(255) | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| promotion                 | nvarchar(255) | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| comments                  | nvarchar(MAX) | YES        |            |           |               | 11%     |          7 | —                          | —                          |
| exchange_rate             | numeric(38,7) | YES        |            |           |               | 0%      |          2 | 0.7294452                  | 1.0000000                  |
| usd_mrc                   | numeric(38,2) | YES        |            |           |               | 0%      |          7 | 0.00                       | 928.95                     |
| client_id                 | int           | YES        |            |           |               | 0%      |          4 | 4004309                    | 7036477                    |
| short_term                | int           | YES        |            |           |               | 100%    |          0 | NULL                       | NULL                       |
| cad_exchange_rate         | numeric(38,7) | YES        |            |           |               | 0%      |          2 | 1.0000000                  | 1.3473391                  |
| cad_mrc                   | numeric(38,2) | YES        |            |           |               | 0%      |          7 | 0.00                       | 1273.50                    |
| cad_budget_mrc            | numeric(38,4) | YES        |            |           |               | 0%      |          7 | 0.0000                     | 1273.5000                  |
| last_updated              | datetime2     | YES        |            |           |               | 0%      |          1 | 2026-03-07 06:42:41.993333 | 2026-03-07 06:42:41.993333 |
| adjusted_line_of_business | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |

#### Indexes

| Name                   | Type      | Unique   | PK   | Columns     |
|------------------------|-----------|----------|------|-------------|
| PK_churn_month_to_date | CLUSTERED | YES      | ✓    | integer_key |

---

### dbo.cost_software_skus {#dbo-cost-software-skus}

| Property | Value |
|---|---|
| Full name | `[dbo].[cost_software_skus]` |
| Row count | 391 |
| Total size | 0.1 MB |
| Used size | 0.1 MB |
| Created | 2025-05-16 09:25 |
| Schema modified | 2025-05-16 09:25 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column       | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min    | Max       |
|--------------|---------------|------------|------------|-----------|---------------|---------|------------|--------|-----------|
| Software SKU | nvarchar(255) | YES        |            |           |               | 1%      |        388 | —      | —         |
| USD          | money         | YES        |            |           |               | 1%      |         67 | 0.0000 | 3279.9000 |
| CAD          | money         | YES        |            |           |               | 1%      |         67 | 0.0000 | 4690.2600 |
| GBP          | money         | YES        |            |           |               | 1%      |         67 | 0.0000 | 2659.6700 |
| EUR          | money         | YES        |            |           |               | 2%      |         63 | 0.0000 | 3147.7200 |
| Comments     | nvarchar(255) | YES        |            |           |               | 1%      |         57 | —      | —         |

---

### dbo.DateDimension {#dbo-datedimension}

| Property | Value |
|---|---|
| Full name | `[dbo].[DateDimension]` |
| Row count | 11,688 |
| Total size | 1.7 MB |
| Used size | 1.7 MB |
| Created | 2014-11-10 11:24 |
| Schema modified | 2023-07-19 14:48 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                | Type       | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-----------------------|------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| integer_key           | smallint   | NO         |            |           |               | 0%      |      11688 | 1                   | 11688               |
| date_key              | datetime   | YES        |            |           |               | 0%      |      11688 | 1999-01-01 00:00:00 | 2030-12-31 00:00:00 |
| day_number_of_week    | smallint   | YES        |            |           |               | 0%      |          7 | 1                   | 7                   |
| day_name_of_week      | varchar(9) | YES        |            |           |               | 0%      |          7 | —                   | —                   |
| day_number_of_month   | smallint   | YES        |            |           |               | 0%      |         31 | 1                   | 31                  |
| week_number_of_year   | smallint   | YES        |            |           |               | 0%      |         54 | 1                   | 54                  |
| month_name            | varchar(9) | YES        |            |           |               | 0%      |         12 | —                   | —                   |
| calendar_month        | smallint   | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| calendar_quarter      | varchar(2) | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| calendar_year         | smallint   | YES        |            |           |               | 0%      |         32 | 1999                | 2030                |
| fiscal_period         | smallint   | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| fiscal_quarter        | varchar(2) | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| fiscal_year           | smallint   | YES        |            |           |               | 0%      |         33 | 1999                | 2031                |
| fiscal_year_cogeco    | smallint   | YES        |            |           |               | 0%      |         33 | 1999                | 2031                |
| fiscal_period_cogeco  | smallint   | YES        |            |           |               | 0%      |         12 | 1                   | 12                  |
| fiscal_quarter_cogeco | varchar(2) | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| date_short            | date       | YES        |            |           |               | 0%      |      11688 | 1999-01-01          | 2030-12-31          |
| fiscal_week_cogeco    | tinyint    | YES        |            |           |               | 0%      |         54 | 1                   | 54                  |

#### Indexes

| Name             | Type      | Unique   | PK   | Columns     |
|------------------|-----------|----------|------|-------------|
| PK_DateDimension | CLUSTERED | YES      | ✓    | integer_key |

---

### dbo.dimChangeControl {#dbo-dimchangecontrol}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimChangeControl]` |
| Row count | 21,788 |
| Total size | 16.1 MB |
| Used size | 13.8 MB |
| Created | 2017-11-07 11:45 |
| Schema modified | 2018-09-11 20:06 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                     | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| creation_date_time         | datetime2     | YES        |            |           |               | 0%      |      21788 | 2015-07-13 09:17:34.287000 | 2025-04-01 04:01:46.020000 |
| created_by                 | nvarchar(50)  | YES        |            |           |               | 0%      |        434 | —                          | —                          |
| last_modified              | datetime2     | YES        |            |           |               | 0%      |      21709 | 2015-07-13 11:40:48.230000 | 2025-05-01 14:12:02.420000 |
| last_modified_by           | nvarchar(50)  | YES        |            |           |               | 0%      |        293 | —                          | —                          |
| owned_by_team              | nvarchar(100) | YES        |            |           |               | 0%      |         56 | —                          | —                          |
| change_control_id          | nvarchar(20)  | YES        |            |           |               | 0%      |      21788 | —                          | —                          |
| change_category            | nvarchar(50)  | YES        |            |           |               | 15%     |        188 | —                          | —                          |
| change_control_status      | nvarchar(100) | YES        |            |           |               | 0%      |         16 | —                          | —                          |
| requested_by               | nvarchar(50)  | YES        |            |           |               | 0%      |        792 | —                          | —                          |
| requested_date_time        | datetime2     | YES        |            |           |               | 0%      |      21788 | 2015-07-13 09:17:34.287000 | 2025-04-01 04:01:46.123000 |
| change_authorization_level | nvarchar(25)  | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| change_title               | nvarchar(255) | YES        |            |           |               | 0%      |      16898 | —                          | —                          |
| service_area               | nvarchar(50)  | YES        |            |           |               | 0%      |         16 | —                          | —                          |
| request_date_time          | datetime2     | YES        |            |           |               | 0%      |      21650 | 2012-09-05 19:27:00        | 2032-03-29 20:16:00        |
| close_date_time            | datetime2     | YES        |            |           |               | 11%     |      19082 | 1900-01-01 00:00:00        | 2025-04-28 14:40:07.193000 |
| change_source              | nvarchar(30)  | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| environment                | nvarchar(15)  | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| maintenance_start          | datetime2     | YES        |            |           |               | 0%      |      16032 | 1900-01-01 00:00:00        | 2025-09-19 15:00:00        |
| maintenance_end            | datetime2     | YES        |            |           |               | 0%      |      16174 | 1899-12-30 21:00:00        | 2025-09-19 17:00:00        |
| change_type                | nvarchar(50)  | YES        |            |           |               | 0%      |         11 | —                          | —                          |
| change_impact              | nvarchar(15)  | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| requested_by_department    | nvarchar(50)  | YES        |            |           |               | 12%     |        188 | —                          | —                          |
| created_culture            | nvarchar(20)  | YES        |            |           |               | 11%     |          4 | —                          | —                          |
| change_process             | nvarchar(50)  | YES        |            |           |               | 0%      |          5 | —                          | —                          |
| impact_matrix              | nvarchar(50)  | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| risk_matrix                | nvarchar(50)  | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| last_updated               | datetime2     | YES        |            |           |               | 0%      |          1 | 2025-05-15 04:00:03.107000 | 2025-05-15 04:00:03.107000 |

---

### dbo.dimClientsActive {#dbo-dimclientsactive}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimClientsActive]` |
| Row count | 778 |
| Total size | 5.5 MB |
| Used size | 5.4 MB |
| Created | 2016-06-08 11:37 |
| Schema modified | 2023-04-19 10:44 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                        | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|-------------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| source_system                 | varchar(5)    | NO         |            |           |               | 0%      |          1 | —                          | —                          |
| client_id                     | int           | NO         |            |           |               | 0%      |        778 | 1000002                    | 7036716                    |
| company_name                  | nvarchar(255) | NO         |            |           |               | 0%      |        778 | —                          | —                          |
| client_type                   | nvarchar(64)  | YES        |            |           |               | 0%      |          7 | —                          | —                          |
| city                          | nvarchar(50)  | YES        |            |           |               | 0%      |        503 | —                          | —                          |
| state                         | nvarchar(50)  | YES        |            |           |               | 22%     |         77 | —                          | —                          |
| zip_code                      | nvarchar(100) | YES        |            |           |               | 0%      |        728 | —                          | —                          |
| country                       | nvarchar(50)  | YES        |            |           |               | 0%      |         40 | —                          | —                          |
| account_manager               | nvarchar(50)  | YES        |            |           |               | 0%      |         13 | —                          | —                          |
| account_executive             | nvarchar(50)  | YES        |            |           |               | 97%     |         10 | —                          | —                          |
| tam                           | nvarchar(50)  | YES        |            |           |               | 95%     |          3 | —                          | —                          |
| crm                           | nvarchar(50)  | YES        |            |           |               | 94%     |          5 | —                          | —                          |
| region                        | nvarchar(50)  | YES        |            |           |               | 0%      |          5 | —                          | —                          |
| is_ecommerce                  | nvarchar(3)   | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| is_nbt                        | nvarchar(3)   | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| is_french_entity              | nvarchar(3)   | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| customer_tier                 | nvarchar(11)  | NO         |            |           |               | 0%      |          3 | —                          | —                          |
| ocean_tier                    | nvarchar(11)  | YES        |            |           |               | 28%     |          3 | —                          | —                          |
| ce_pod                        | nvarchar(50)  | YES        |            |           |               | 24%     |          8 | —                          | —                          |
| market_segment                | nvarchar(50)  | YES        |            |           |               | 0%      |          6 | —                          | —                          |
| referred_by                   | int           | YES        |            |           |               | 94%     |         39 | 1000376                    | 7014879                    |
| created_on                    | datetime2     | NO         |            |           |               | 0%      |        743 | 1998-08-28 00:00:00        | 2025-12-09 17:13:16.596373 |
| datacenter_count              | int           | YES        |            |           |               | 0%      |          5 | 1                          | 6                          |
| datacenter_codes              | nvarchar(201) | YES        |            |           |               | 0%      |         84 | —                          | —                          |
| original_currency_mrc         | numeric(38,4) | YES        |            |           |               | 0%      |        657 | 0.0000                     | 425740.1200                |
| current_usd_mrc               | numeric(38,4) | YES        |            |           |               | 0%      |        658 | 0.0000                     | 425740.1200                |
| usd_cloud_charges             | numeric(38,4) | YES        |            |           |               | 77%     |        171 | -6.1050                    | 113930.3125                |
| usd_mrc_cloud_combined        | numeric(38,4) | YES        |            |           |               | 0%      |        769 | -6.1050                    | 428266.7800                |
| current_cad_mrc               | numeric(38,4) | YES        |            |           |               | 0%      |        658 | 0.0000                     | 573600.7538                |
| cad_cloud_charges             | numeric(38,4) | YES        |            |           |               | 77%     |        171 | -8.2253                    | 147597.0404                |
| cad_mrc_cloud_combined        | numeric(38,4) | YES        |            |           |               | 0%      |        769 | -8.2253                    | 577004.9291                |
| cad_budget_mrc                | numeric(38,4) | YES        |            |           |               | 0%      |        658 | 0.0000                     | 566234.3596                |
| cad_budget_cloud_charges      | numeric(38,4) | YES        |            |           |               | 77%     |        171 | -8.1197                    | 139724.7550                |
| cad_budget_mrc_cloud_combined | numeric(38,4) | YES        |            |           |               | 0%      |        769 | -8.1197                    | 569594.8174                |
| prev_month_usd_mrc            | numeric(38,4) | YES        |            |           |               | 0%      |        658 | 0.0000                     | 425740.1200                |
| prev_year_usd_mrc             | numeric(38,4) | YES        |            |           |               | 1%      |        645 | 0.0000                     | 424750.5200                |
| prev_month_cad_mrc            | numeric(38,4) | YES        |            |           |               | 0%      |        658 | 0.0000                     | 573072.7265                |
| prev_year_cad_mrc             | numeric(38,4) | YES        |            |           |               | 1%      |        645 | 0.0000                     | 587911.6916                |
| managed_hosting_usd_mrc       | numeric(38,4) | YES        |            |           |               | 51%     |        366 | 0.0000                     | 216897.8440                |
| dedicated_hosting_usd_mrc     | numeric(38,4) | YES        |            |           |               | 73%     |        208 | 110.7240                   | 425260.1200                |
| colocation_usd_mrc            | numeric(38,4) | YES        |            |           |               | 84%     |        118 | 0.0000                     | 85007.7360                 |
| managed_hosting_cad_mrc       | numeric(38,4) | YES        |            |           |               | 51%     |        366 | 0.0000                     | 292227.0060                |
| dedicated_hosting_cad_mrc     | numeric(38,4) | YES        |            |           |               | 73%     |        208 | 143.4432                   | 572954.0486                |
| colocation_cad_mrc            | numeric(38,4) | YES        |            |           |               | 84%     |        118 | 0.0000                     | 116535.3800                |
| usd_mcc_charges               | numeric(38,4) | YES        |            |           |               | 99%     |          1 | 0.0000                     | 0.0000                     |
| usd_cloudone_charges          | numeric(38,4) | YES        |            |           |               | 99%     |          4 | 17.0910                    | 167.1233                   |
| usd_ondemand_charges          | numeric(38,4) | YES        |            |           |               | 99%     |          1 | 0.0000                     | 0.0000                     |
| cad_mcc_charges               | numeric(38,4) | YES        |            |           |               | 99%     |          1 | 0.0000                     | 0.0000                     |
| cad_cloudone_charges          | numeric(38,4) | YES        |            |           |               | 99%     |          4 | 23.0267                    | 225.1657                   |
| cad_ondemand_charges          | numeric(38,4) | YES        |            |           |               | 99%     |          1 | 0.0000                     | 0.0000                     |
| last_updated                  | datetime2     | NO         |            |           |               | 0%      |          1 | 2026-03-06 07:53:43.386666 | 2026-03-06 07:53:43.386666 |
| salesforce_account_id         | nvarchar(255) | YES        |            |           |               | 0%      |        774 | —                          | —                          |
| is_at_risk                    | nvarchar(255) | YES        |            |           |               | 0%      |          2 | —                          | —                          |

---

### dbo.dimClientsActive_historical {#dbo-dimclientsactive-historical}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimClientsActive_historical]` |
| Row count | 5,051,942 |
| Total size | 4.2 GB |
| Used size | 4.2 GB |
| Created | 2020-01-16 15:27 |
| Schema modified | 2023-04-10 13:08 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                        | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                        |
|-------------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|----------------------------|
| source_system                 | varchar(5)    | NO         |            |           |               | 0%      |          1 | —                   | —                          |
| client_id                     | int           | NO         |            |           |               | 0%      |       6213 | 1000002             | 7036716                    |
| company_name                  | nvarchar(255) | NO         |            |           |               | 0%      |       6793 | —                   | —                          |
| client_type                   | nvarchar(64)  | YES        |            |           |               | 0%      |          9 | —                   | —                          |
| city                          | nvarchar(50)  | YES        |            |           |               | 0%      |       2564 | —                   | —                          |
| state                         | nvarchar(50)  | YES        |            |           |               | 23%     |        112 | —                   | —                          |
| zip_code                      | nvarchar(100) | YES        |            |           |               | 0%      |       5788 | —                   | —                          |
| country                       | nvarchar(50)  | YES        |            |           |               | 0%      |         93 | —                   | —                          |
| account_manager               | nvarchar(50)  | YES        |            |           |               | 1%      |        176 | —                   | —                          |
| account_executive             | nvarchar(50)  | YES        |            |           |               | 87%     |         90 | —                   | —                          |
| tam                           | nvarchar(50)  | YES        |            |           |               | 96%     |         34 | —                   | —                          |
| crm                           | nvarchar(50)  | YES        |            |           |               | 95%     |         39 | —                   | —                          |
| region                        | nvarchar(50)  | YES        |            |           |               | 0%      |          6 | —                   | —                          |
| is_ecommerce                  | nvarchar(3)   | NO         |            |           |               | 0%      |          2 | —                   | —                          |
| is_nbt                        | nvarchar(3)   | NO         |            |           |               | 0%      |          2 | —                   | —                          |
| is_french_entity              | nvarchar(3)   | NO         |            |           |               | 0%      |          2 | —                   | —                          |
| customer_tier                 | nvarchar(11)  | NO         |            |           |               | 0%      |          3 | —                   | —                          |
| ocean_tier                    | nvarchar(11)  | YES        |            |           |               | 25%     |          3 | —                   | —                          |
| ce_pod                        | nvarchar(50)  | YES        |            |           |               | 14%     |          8 | —                   | —                          |
| market_segment                | nvarchar(50)  | YES        |            |           |               | 1%      |          6 | —                   | —                          |
| referred_by                   | int           | YES        |            |           |               | 90%     |        310 | 1000053             | 7014879                    |
| created_on                    | datetime2     | NO         |            |           |               | 0%      |       5841 | 1997-08-22 00:00:00 | 2025-12-09 17:13:16.596373 |
| datacenter_count              | int           | YES        |            |           |               | 1%      |         13 | 0                   | 13                         |
| datacenter_codes              | nvarchar(201) | YES        |            |           |               | 1%      |        623 | —                   | —                          |
| original_currency_mrc         | numeric(38,4) | YES        |            |           |               | 10%     |      23844 | 0.0000              | 2685382.1600               |
| current_usd_mrc               | numeric(38,4) | YES        |            |           |               | 10%     |    1527215 | 0.0000              | 2685382.1600               |
| usd_cloud_charges             | numeric(38,4) | YES        |            |           |               | 86%     |     208588 | -10103.5622         | 512081.3900                |
| usd_mrc_cloud_combined        | numeric(38,4) | YES        |            |           |               | 0%      |    1669489 | -10103.5622         | 2685382.1600               |
| current_cad_mrc               | numeric(38,4) | YES        |            |           |               | 10%     |    2829138 | 0.0000              | 3514492.7433               |
| cad_cloud_charges             | numeric(38,4) | YES        |            |           |               | 86%     |     615537 | -13501.7033         | 684364.7726                |
| cad_mrc_cloud_combined        | numeric(38,4) | YES        |            |           |               | 0%      |    3277188 | -13501.7033         | 3514492.7433               |
| cad_budget_mrc                | numeric(38,4) | YES        |            |           |               | 10%     |      29773 | 0.0000              | 3571558.2728               |
| cad_budget_cloud_charges      | numeric(38,4) | YES        |            |           |               | 86%     |      39174 | -13501.7033         | 681068.2487                |
| cad_budget_mrc_cloud_combined | numeric(38,4) | YES        |            |           |               | 0%      |      69499 | -13501.7033         | 3571558.2728               |
| prev_month_usd_mrc            | numeric(38,4) | YES        |            |           |               | 10%     |      67627 | 0.0000              | 3141838.0800               |
| prev_year_usd_mrc             | numeric(38,4) | YES        |            |           |               | 13%     |      62947 | 0.0000              | 3141838.0800               |
| prev_month_cad_mrc            | numeric(38,4) | YES        |            |           |               | 10%     |     111288 | 0.0000              | 4136331.9548               |
| prev_year_cad_mrc             | numeric(38,4) | YES        |            |           |               | 13%     |     107747 | 0.0000              | 4136331.9548               |
| managed_hosting_usd_mrc       | numeric(38,4) | YES        |            |           |               | 59%     |     706726 | 0.0000              | 2678182.1600               |
| dedicated_hosting_usd_mrc     | numeric(38,4) | YES        |            |           |               | 68%     |     151544 | 0.0000              | 1124203.3000               |
| colocation_usd_mrc            | numeric(38,4) | YES        |            |           |               | 80%     |     742359 | 0.0000              | 679943.1194                |
| managed_hosting_cad_mrc       | numeric(38,4) | YES        |            |           |               | 59%     |    1704753 | 0.0000              | 3505068.5409               |
| dedicated_hosting_cad_mrc     | numeric(38,4) | YES        |            |           |               | 68%     |    1081610 | 0.0000              | 1514255.5284               |
| colocation_cad_mrc            | numeric(38,4) | YES        |            |           |               | 80%     |     268291 | 0.0000              | 822371.2579                |
| usd_mcc_charges               | numeric(38,4) | YES        |            |           |               | 90%     |      69156 | 0.0000              | 18241.5584                 |
| usd_cloudone_charges          | numeric(38,4) | YES        |            |           |               | 90%     |       3519 | 0.0000              | 1017.0371                  |
| usd_ondemand_charges          | numeric(38,4) | YES        |            |           |               | 90%     |      38161 | 0.0000              | 2514.3509                  |
| cad_mcc_charges               | numeric(38,4) | YES        |            |           |               | 90%     |     421203 | 0.0000              | 23947.6524                 |
| cad_cloudone_charges          | numeric(38,4) | YES        |            |           |               | 90%     |      12634 | 0.0000              | 1345.8020                  |
| cad_ondemand_charges          | numeric(38,4) | YES        |            |           |               | 90%     |      62090 | 0.0000              | 3087.7300                  |
| current_record                | nvarchar(3)   | YES        |            |           |               | 0%      |          2 | —                   | —                          |
| record_start_date             | datetime2     | YES        |            |           |               | 0%      |       2947 | 2017-08-03 00:00:00 | 2026-03-05 00:00:00        |
| record_end_date               | datetime2     | YES        |            |           |               | 0%      |       3081 | 2017-08-05 00:00:00 | 2026-03-05 00:00:00        |

---

### dbo.dimCloud_OtherUsageCharges {#dbo-dimcloud-otherusagecharges}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimCloud_OtherUsageCharges]` |
| Row count | 34,284 |
| Total size | 47.9 MB |
| Used size | 22.5 MB |
| Created | 2020-02-27 20:56 |
| Schema modified | 2024-02-13 17:56 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column               | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|----------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| integer_key          | int           | NO         |            |           |               | 0%      |      34284 | 1                          | 34284                      |
| cloud_product        | nvarchar(255) | YES        |            |           |               | 0%      |         19 | —                          | —                          |
| client_id            | int           | YES        |            |           |               | 0%      |        799 | 1000002                    | 7036716                    |
| company_name         | nvarchar(500) | YES        |            |           |               | 0%      |        799 | —                          | —                          |
| sales_rep_region     | nvarchar(255) | YES        |            |           |               | 99%     |          1 | —                          | —                          |
| cad_usage_billed     | numeric(38,4) | YES        |            |           |               | 0%      |      21829 | -102359.7900               | 2981711.0400               |
| usage_billed         | numeric(38,4) | YES        |            |           |               | 0%      |      18768 | -102359.7900               | 2381443.0000               |
| bill_period          | datetime      | YES        |            |           |               | 0%      |         31 | 2023-10-01 00:00:00        | 2026-11-01 00:00:00        |
| bill                 | numeric(38,4) | YES        |            |           |               | 0%      |      18623 | -102359.7900               | 2381443.0000               |
| country              | nvarchar(255) | YES        |            |           |               | 0%      |         35 | —                          | —                          |
| region               | nvarchar(255) | YES        |            |           |               | 0%      |          5 | —                          | —                          |
| is_active            | nvarchar(255) | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| currency             | nvarchar(15)  | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| is_managed_azure     | nvarchar(15)  | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| is_cloud             | bit           | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| last_updated         | datetime2     | YES        |            |           |               | 0%      |          1 | 2026-03-06 07:53:00.423333 | 2026-03-06 07:53:00.423333 |
| item_description     | nvarchar(255) | YES        |            |           |               | 0%      |         75 | —                          | —                          |
| item_number          | nvarchar(255) | YES        |            |           |               | 0%      |         58 | —                          | —                          |
| invoice_number       | nvarchar(25)  | YES        |            |           |               | 0%      |      12202 | —                          | —                          |
| invoice_created_date | datetime      | YES        |            |           |               | 0%      |        423 | 2023-02-20 00:00:00        | 2026-03-01 00:00:00        |

---

### dbo.dimComponents {#dbo-dimcomponents}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimComponents]` |
| Row count | 1,618,569 |
| Total size | 702.0 MB |
| Used size | 700.2 MB |
| Created | 2014-11-10 14:36 |
| Schema modified | 2020-04-06 19:00 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                    | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|---------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| integer_key               | int           | NO         |            |           |               | 0%      |    1618569 | 1                          | 43887572                   |
| client_id                 | int           | NO         |            |           |               | 0%      |      19923 | 101                        | 7036720                    |
| component_category        | nvarchar(32)  | NO         |            |           |               | 0%      |         17 | —                          | —                          |
| service_option_type       | nvarchar(64)  | NO         |            |           |               | 0%      |         44 | —                          | —                          |
| component_type            | nvarchar(64)  | NO         |            |           |               | 0%      |        297 | —                          | —                          |
| component                 | nvarchar(64)  | NO         |            |           |               | 0%      |       4991 | —                          | —                          |
| add_on                    | int           | YES        |            |           |               | 0%      |          2 | 0                          | 1                          |
| currency                  | nvarchar(3)   | NO         |            |           |               | 0%      |          4 | —                          | —                          |
| component_mrc             | numeric(38,4) | NO         |            |           |               | 0%      |       8824 | -499.0000                  | 717509.9979                |
| product_mrc               | numeric(38,4) | YES        |            |           |               | 0%      |      12661 | -3049.0000                 | 63900.0000                 |
| product                   | nvarchar(255) | YES        |            |           |               | 0%      |        786 | —                          | —                          |
| component_date            | datetime2     | NO         |            |           |               | 0%      |       7176 | 2001-05-08 00:00:00        | 2026-03-05 00:00:00        |
| provision_date            | datetime2     | YES        |            |           |               | 2%      |     124933 | 1999-05-17 00:00:00        | 2026-03-05 10:30:59.714956 |
| is_online                 | varchar(3)    | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| service_id                | int           | NO         |            |           |               | 0%      |     137418 | 282                        | 7981441                    |
| is_virtual                | int           | YES        |            |           |               | 0%      |          2 | 0                          | 1                          |
| datacenter_city           | nvarchar(100) | YES        |            |           |               | 0%      |         34 | —                          | —                          |
| datacenter_code           | nvarchar(MAX) | YES        |            |           |               | 0%      |         46 | —                          | —                          |
| line_of_business          | nvarchar(255) | YES        |            |           |               | 0%      |          6 | —                          | —                          |
| component_id              | int           | NO         |            |           |               | 0%      |       4000 | 1                          | 6364                       |
| usd_component_mrc         | numeric(38,4) | YES        |            |           |               | 0%      |      12058 | -677.3403                  | 523393.8386                |
| usd_product_mrc           | numeric(38,4) | YES        |            |           |               | 0%      |      14974 | -3049.0000                 | 46612.4045                 |
| is_emea                   | varchar(3)    | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| last_updated              | datetime2     | YES        |            |           |               | 0%      |          1 | 2026-03-06 07:53:45.966666 | 2026-03-06 07:53:45.966666 |
| cad_component_mrc         | numeric(38,4) | YES        |            |           |               | 0%      |      12047 | -873.8229                  | 717509.9979                |
| cad_product_mrc           | numeric(38,4) | YES        |            |           |               | 0%      |      14978 | -4107.9253                 | 63900.0000                 |
| cad_budget_component_mrc  | numeric(38,4) | YES        |            |           |               | 0%      |      11866 | -823.3500                  | 717509.9979                |
| cad_budget_product_mrc    | numeric(38,4) | YES        |            |           |               | 0%      |      14887 | -4055.1700                 | 63900.0000                 |
| adjusted_line_of_business | nvarchar(255) | YES        |            |           |               | 0%      |          4 | —                          | —                          |

#### Indexes

| Name             | Type      | Unique   | PK   | Columns     |
|------------------|-----------|----------|------|-------------|
| PK_DimComponents | CLUSTERED | YES      | ✓    | integer_key |

---

### dbo.dimComponents_TTSSiteScout {#dbo-dimcomponents-ttssitescout}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimComponents_TTSSiteScout]` |
| Row count | 176,660 |
| Total size | 78.5 MB |
| Used size | 78.5 MB |
| Created | 2020-11-12 09:13 |
| Schema modified | 2020-11-12 09:13 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                    | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|---------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| integer_key               | int           | NO         |            |           |               | 0%      |     176660 | 1596699                    | 43766587                   |
| client_id                 | int           | NO         |            |           |               | 0%      |          2 | 7007480                    | 7007612                    |
| component_category        | nvarchar(32)  | NO         |            |           |               | 0%      |         10 | —                          | —                          |
| service_option_type       | nvarchar(64)  | NO         |            |           |               | 0%      |         25 | —                          | —                          |
| component_type            | nvarchar(64)  | NO         |            |           |               | 0%      |         65 | —                          | —                          |
| component                 | nvarchar(64)  | NO         |            |           |               | 0%      |        439 | —                          | —                          |
| add_on                    | int           | YES        |            |           |               | 0%      |          2 | 0                          | 1                          |
| currency                  | nvarchar(3)   | NO         |            |           |               | 0%      |          1 | —                          | —                          |
| component_mrc             | numeric(38,4) | NO         |            |           |               | 0%      |        218 | 0.0000                     | 3250.0000                  |
| product_mrc               | numeric(38,4) | YES        |            |           |               | 0%      |        521 | 0.0000                     | 25200.0000                 |
| product                   | nvarchar(255) | YES        |            |           |               | 0%      |         82 | —                          | —                          |
| component_date            | datetime2     | NO         |            |           |               | 0%      |        639 | 2012-02-28 00:00:00        | 2025-11-10 00:00:00        |
| provision_date            | datetime2     | YES        |            |           |               | 1%      |       8614 | 2012-03-16 10:15:58.576358 | 2026-03-04 11:19:20.940797 |
| is_online                 | varchar(3)    | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| service_id                | int           | NO         |            |           |               | 0%      |       8710 | 2643806                    | 7963585                    |
| is_virtual                | int           | YES        |            |           |               | 0%      |          1 | 0                          | 0                          |
| datacenter_city           | nvarchar(100) | YES        |            |           |               | 0%      |          6 | —                          | —                          |
| datacenter_code           | nvarchar(MAX) | YES        |            |           |               | 0%      |          6 | —                          | —                          |
| line_of_business          | nvarchar(255) | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| component_id              | int           | NO         |            |           |               | 0%      |        405 | 5                          | 6268                       |
| usd_component_mrc         | numeric(38,4) | YES        |            |           |               | 0%      |        218 | 0.0000                     | 3250.0000                  |
| usd_product_mrc           | numeric(38,4) | YES        |            |           |               | 0%      |        521 | 0.0000                     | 25200.0000                 |
| is_emea                   | varchar(3)    | NO         |            |           |               | 0%      |          1 | —                          | —                          |
| last_updated              | datetime2     | YES        |            |           |               | 0%      |          1 | 2026-03-06 07:53:45.966666 | 2026-03-06 07:53:45.966666 |
| cad_component_mrc         | numeric(38,4) | YES        |            |           |               | 0%      |        218 | 0.0000                     | 4378.7331                  |
| cad_product_mrc           | numeric(38,4) | YES        |            |           |               | 0%      |        521 | 0.0000                     | 33952.0230                 |
| cad_budget_component_mrc  | numeric(38,4) | YES        |            |           |               | 0%      |        218 | 0.0000                     | 4322.5000                  |
| cad_budget_product_mrc    | numeric(38,4) | YES        |            |           |               | 0%      |        521 | 0.0000                     | 33516.0000                 |
| adjusted_line_of_business | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |

#### Indexes

| Name                          | Type      | Unique   | PK   | Columns     |
|-------------------------------|-----------|----------|------|-------------|
| PK_dimComponents_TTSSiteScout | CLUSTERED | YES      | ✓    | integer_key |

---

### dbo.dimCredits {#dbo-dimcredits}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimCredits]` |
| Row count | 168,071 |
| Total size | 211.6 MB |
| Used size | 197.2 MB |
| Created | 2018-07-11 14:30 |
| Schema modified | 2020-04-06 10:03 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                    | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|---------------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| integer_key               | int           | NO         |            |           |               | 0%      |     168071 | 1                   | 168071              |
| client_id                 | int           | YES        |            |           |               | 0%      |       6430 | 1000002             | 7036707             |
| company_name              | nvarchar(255) | YES        |            |           |               | 0%      |       6430 | —                   | —                   |
| region                    | nvarchar(50)  | YES        |            |           |               | 0%      |          5 | —                   | —                   |
| tam                       | nvarchar(50)  | YES        |            |           |               | 89%     |         23 | —                   | —                   |
| post_date                 | date          | YES        |            |           |               | 0%      |       2049 | 2015-09-01          | 2026-03-04          |
| credit_code               | nvarchar(50)  | YES        |            |           |               | 0%      |       2622 | —                   | —                   |
| comments                  | varchar(MAX)  | YES        |            |           |               | 91%     |      13640 | —                   | —                   |
| description               | nvarchar(255) | YES        |            |           |               | 0%      |       2235 | —                   | —                   |
| category                  | nvarchar(60)  | YES        |            |           |               | 0%      |         12 | —                   | —                   |
| cost_center               | nvarchar(100) | YES        |            |           |               | 0%      |         19 | —                   | —                   |
| line_of_business          | nvarchar(50)  | YES        |            |           |               | 0%      |         13 | —                   | —                   |
| budget_group              | nvarchar(50)  | YES        |            |           |               | 0%      |         21 | —                   | —                   |
| entity                    | nvarchar(100) | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| location                  | nvarchar(100) | YES        |            |           |               | 0%      |         29 | —                   | —                   |
| system_entity             | nvarchar(150) | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| cad_budget_mrc            | numeric(38,4) | YES        |            |           |               | 0%      |      53813 | 0.0000              | 289984.8343         |
| credit_category           | varchar(50)   | YES        |            |           |               | 0%      |         16 | —                   | —                   |
| credit_type               | varchar(50)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| is_addressable            | varchar(3)    | NO         |            |           |               | 0%      |          2 | —                   | —                   |
| document_date             | date          | YES        |            |           |               | 0%      |       2247 | 2015-06-22          | 2026-03-04          |
| last_updated              | datetime2     | YES        |            |           |               | 0%      |          1 | 2026-03-06 00:00:00 | 2026-03-06 00:00:00 |
| document_number           | nvarchar(25)  | YES        |            |           |               | 0%      |      27725 | —                   | —                   |
| posting_user              | nvarchar(15)  | YES        |            |           |               | 0%      |         14 | —                   | —                   |
| EBITDA                    | nvarchar(35)  | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| original_price            | numeric(19,5) | YES        |            |           |               | 0%      |      38888 | 0.00000             | 218033.71000        |
| extended_price            | numeric(19,5) | YES        |            |           |               | 0%      |      39436 | 0.01000             | 218033.71000        |
| currency                  | nvarchar(15)  | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| start_date                | date          | YES        |            |           |               | 0%      |       3519 | 2010-01-08          | 2105-08-12          |
| end_date                  | date          | YES        |            |           |               | 0%      |       3177 | 2013-11-30          | 2107-07-31          |
| contract_number           | nvarchar(15)  | YES        |            |           |               | 0%      |      50853 | —                   | —                   |
| account                   | nvarchar(129) | YES        |            |           |               | 0%      |        424 | —                   | —                   |
| voided_date               | nvarchar(10)  | YES        |            |           |               | 0%      |          1 | —                   | —                   |
| natural_account           | nvarchar(10)  | YES        |            |           |               | 0%      |         10 | —                   | —                   |
| voided_month              | int           | YES        |            |           |               | 0%      |          1 | 190001              | 190001              |
| posted_month              | int           | YES        |            |           |               | 0%      |        127 | 201509              | 202603              |
| account_description       | nvarchar(190) | YES        |            |           |               | 0%      |        424 | —                   | —                   |
| gl_natural_account        | nvarchar(40)  | YES        |            |           |               | 0%      |         10 | —                   | —                   |
| department                | nvarchar(25)  | YES        |            |           |               | 0%      |          5 | —                   | —                   |
| class                     | nvarchar(25)  | YES        |            |           |               | 0%      |         13 | —                   | —                   |
| type                      | smallint      | NO         |            |           |               | 0%      |          1 | 4                   | 4                   |
| approver                  | nvarchar(50)  | YES        |            |           |               | 1%      |        614 | —                   | —                   |
| adjusted_line_of_business | nvarchar(255) | YES        |            |           |               | 6%      |          2 | —                   | —                   |

---

### dbo.dimCurrencyExchangeRates {#dbo-dimcurrencyexchangerates}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimCurrencyExchangeRates]` |
| Row count | 4,086 |
| Total size | 1.2 MB |
| Used size | 0.6 MB |
| Created | 2015-11-24 19:47 |
| Schema modified | 2018-09-11 09:30 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column               | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|----------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| integer_key          | int           | NO         |            |           |               | 0%      |       4086 | 713                        | 10914                      |
| currency_pair        | varchar(7)    | YES        |            |           |               | 0%      |         13 | —                          | —                          |
| gp_exchange_table_id | char(15)      | NO         |            |           |               | 0%      |         13 | —                          | —                          |
| gp_currency_id       | char(15)      | NO         |            |           |               | 0%      |          4 | —                          | —                          |
| from_currency        | varchar(3)    | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| to_currency          | varchar(3)    | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| exchange_rate        | numeric(19,7) | NO         |            |           |               | 0%      |       3990 | 0.5307600                  | 1.8809900                  |
| start_date           | datetime      | NO         |            |           |               | 0%      |        343 | 2019-09-01 00:00:00        | 2026-03-02 00:00:00        |
| expiration_date      | datetime      | NO         |            |           |               | 0%      |        343 | 2019-09-08 00:00:00        | 9999-12-31 00:00:00        |
| exchange_rate_source | varchar(50)   | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| last_updated         | datetime2     | YES        |            |           |               | 0%      |          2 | 2026-03-06 07:46:00.743333 | 2026-03-06 07:46:00.803333 |

#### Indexes

| Name                        | Type      | Unique   | PK   | Columns     |
|-----------------------------|-----------|----------|------|-------------|
| PK_dimCurrencyExchangeRates | CLUSTERED | YES      | ✓    | integer_key |

---

### dbo.dimCustomerAttributes {#dbo-dimcustomerattributes}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimCustomerAttributes]` |
| Row count | 25,188 |
| Total size | 10.9 MB |
| Used size | 10.1 MB |
| Created | 2019-09-09 20:03 |
| Schema modified | 2023-05-23 15:13 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|-----------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| client_id             | int           | NO         |            |           |               | 0%      |      25188 | 100                        | 7999999                    |
| company_name          | nvarchar(255) | NO         |            |           |               | 0%      |      25188 | —                          | —                          |
| client_type           | nvarchar(64)  | YES        |            |           |               | 0%      |         11 | —                          | —                          |
| city                  | nvarchar(50)  | YES        |            |           |               | 2%      |       6018 | —                          | —                          |
| state                 | nvarchar(50)  | YES        |            |           |               | 23%     |        281 | —                          | —                          |
| zip_code              | nvarchar(100) | YES        |            |           |               | 2%      |      14047 | —                          | —                          |
| country               | nvarchar(50)  | YES        |            |           |               | 2%      |        151 | —                          | —                          |
| is_active             | nvarchar(3)   | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| is_emea               | nvarchar(3)   | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| is_french_entity      | nvarchar(3)   | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| is_ecommerce          | nvarchar(3)   | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| is_nbt                | nvarchar(3)   | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| is_pci                | nvarchar(3)   | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| is_blacklisted        | nvarchar(3)   | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| date_blacklisted      | datetime2     | YES        |            |           |               | 87%     |       3248 | 2003-02-11 12:19:55.561224 | 2026-03-03 09:10:40.499386 |
| referred_by           | int           | YES        |            |           |               | 94%     |        567 | 1000376                    | 7014879                    |
| created_on            | datetime2     | NO         |            |           |               | 0%      |      23466 | 1997-02-24 00:00:00        | 2026-02-26 11:48:48.709086 |
| tam                   | nvarchar(50)  | YES        |            |           |               | 99%     |         43 | —                          | —                          |
| crm                   | nvarchar(50)  | YES        |            |           |               | 99%     |         30 | —                          | —                          |
| mh_bdc                | nvarchar(50)  | YES        |            |           |               | 62%     |        142 | —                          | —                          |
| dh_bdc                | nvarchar(50)  | YES        |            |           |               | 69%     |        130 | —                          | —                          |
| colo_bdc              | nvarchar(50)  | YES        |            |           |               | 92%     |         89 | —                          | —                          |
| cloud_bdc             | nvarchar(50)  | YES        |            |           |               | 89%     |        123 | —                          | —                          |
| account_manager       | nvarchar(50)  | YES        |            |           |               | 43%     |        164 | —                          | —                          |
| account_executive     | nvarchar(50)  | YES        |            |           |               | 89%     |        104 | —                          | —                          |
| channel_sales_exec    | nvarchar(50)  | YES        |            |           |               | 95%     |         22 | —                          | —                          |
| region                | nvarchar(50)  | YES        |            |           |               | 0%      |          6 | —                          | —                          |
| subregion             | nvarchar(50)  | YES        |            |           |               | 42%     |          2 | —                          | —                          |
| microsoft_region      | nvarchar(50)  | YES        |            |           |               | 0%      |          5 | —                          | —                          |
| sales_rep_region      | nvarchar(50)  | YES        |            |           |               | 100%    |          1 | —                          | —                          |
| customer_tier         | nvarchar(11)  | YES        |            |           |               | 97%     |          3 | —                          | —                          |
| ocean_tier            | nvarchar(11)  | YES        |            |           |               | 30%     |          3 | —                          | —                          |
| ce_pod                | nvarchar(50)  | YES        |            |           |               | 26%     |          8 | —                          | —                          |
| sales_pod             | nvarchar(50)  | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| market_segment        | nvarchar(50)  | YES        |            |           |               | 63%     |          6 | —                          | —                          |
| business_unit         | nvarchar(50)  | YES        |            |           |               | 79%     |          2 | —                          | —                          |
| last_updated          | datetime2     | NO         |            |           |               | 0%      |          1 | 2026-03-06 07:49:00.190000 | 2026-03-06 07:49:00.190000 |
| salesforce_account_id | nvarchar(255) | YES        |            |           |               | 79%     |       5228 | —                          | —                          |
| tax_types             | nvarchar(200) | YES        |            |           |               | 0%      |          6 | —                          | —                          |
| tax_codes             | nvarchar(400) | YES        |            |           |               | 0%      |        460 | —                          | —                          |
| industry              | nvarchar(50)  | YES        |            |           |               | 0%      |         21 | —                          | —                          |
| sub_industry          | nvarchar(50)  | YES        |            |           |               | 0%      |         60 | —                          | —                          |

---

### dbo.DimCustomerContacts {#dbo-dimcustomercontacts}

| Property | Value |
|---|---|
| Full name | `[dbo].[DimCustomerContacts]` |
| Row count | 99,479 |
| Total size | 12.5 MB |
| Used size | 12.2 MB |
| Created | 2025-10-01 11:40 |
| Schema modified | 2025-10-01 11:40 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column       | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max     |
|--------------|---------------|------------|------------|-----------|---------------|---------|------------|-------|---------|
| contact_id   | int           | YES        |            |           |               | 0%      |      67315 | 1     | 185869  |
| role_name    | nvarchar(255) | YES        |            |           |               | 0%      |          9 | —     | —       |
| customers_id | int           | YES        |            |           |               | 0%      |      24427 | 100   | 7999999 |
| company      | nvarchar(MAX) | YES        |            |           |               | 51%     |      12796 | —     | —       |
| first_name   | nvarchar(MAX) | YES        |            |           |               | 0%      |      10362 | —     | —       |
| last_name    | nvarchar(MAX) | YES        |            |           |               | 0%      |      25733 | —     | —       |
| email        | nvarchar(MAX) | YES        |            |           |               | 0%      |      48774 | —     | —       |

---

### dbo.dimdatacenterattributes {#dbo-dimdatacenterattributes}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimdatacenterattributes]` |
| Row count | 53 |
| Total size | 0.0 MB |
| Used size | 0.0 MB |
| Created | 2016-12-02 17:06 |
| Schema modified | 2024-09-30 15:56 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                 | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max   |
|------------------------|---------------|------------|------------|-----------|---------------|---------|------------|-------|-------|
| datacenter_code        | nvarchar(255) | YES        |            |           |               | 0%      |         53 | —     | —     |
| datacenter_city        | nvarchar(255) | YES        |            |           |               | 8%      |         34 | —     | —     |
| datacenter_name        | nvarchar(255) | YES        |            |           |               | 0%      |         50 | —     | —     |
| country                | nvarchar(255) | YES        |            |           |               | 0%      |          8 | —     | —     |
| datacenter_region      | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —     | —     |
| cp1_datacenter_code    | nvarchar(255) | YES        |            |           |               | 38%     |         23 | —     | —     |
| datacenter_nickname    | nvarchar(255) | YES        |            |           |               | 36%     |         34 | —     | —     |
| address                | nvarchar(255) | YES        |            |           |               | 38%     |         23 | —     | —     |
| legacy_entity          | nvarchar(255) | YES        |            |           |               | 13%     |          3 | —     | —     |
| previous_references    | nvarchar(255) | YES        |            |           |               | 40%     |         22 | —     | —     |
| datacenter_status      | nvarchar(255) | YES        |            |           |               | 0%      |          2 | —     | —     |
| datacenter_report_name | nvarchar(255) | YES        |            |           |               | 40%     |         32 | —     | —     |

---

### dbo.DimDCIMAssets {#dbo-dimdcimassets}

| Property | Value |
|---|---|
| Full name | `[dbo].[DimDCIMAssets]` |
| Row count | 0 |
| Total size | 0.0 MB |
| Used size | 0.0 MB |
| Created | 2023-06-27 19:12 |
| Schema modified | 2025-05-05 16:22 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                                 | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max   |
|----------------------------------------|----------------|------------|------------|-----------|---------------|---------|------------|-------|-------|
| P__metadata_total                      | bigint         | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| id                                     | nvarchar(144)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| status                                 | nvarchar(24)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| parentId                               | nvarchar(144)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| productId                              | nvarchar(144)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| productName                            | nvarchar(136)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| manufacturerId                         | nvarchar(144)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| manufacturerName                       | nvarchar(80)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| assetLifecycleState                    | nvarchar(44)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| monitoringState                        | nvarchar(12)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| P__metadata_limit                      | bigint         | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| P__metadata_offset                     | bigint         | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| tabDelimitedPath                       | nvarchar(344)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| __FileName                             | nvarchar(600)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| displayName                            | nvarchar(180)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| displayNameLowerCase                   | nvarchar(180)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| statusSearchableProperty               | nvarchar(24)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| createdDateTime                        | datetime       | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| updatedDateTime                        | datetime       | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| commissionDate                         | nvarchar(80)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| retirementDate                         | nvarchar(80)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| endOfLifeDate                          | nvarchar(1020) | YES        |            |           |               | 0%      |          0 | —     | —     |
| nameDataSource                         | nvarchar(16)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| assetTypeDataSource                    | nvarchar(22)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| assetType                              | nvarchar(56)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| assetTypeSearchableProperty            | nvarchar(56)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| monitoringProfileType                  | nvarchar(1020) | YES        |            |           |               | 0%      |          0 | —     | —     |
| assetAccessPolicyId                    | nvarchar(144)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| assetTrackerMasterModuleSerialNumber   | nvarchar(8)    | YES        |            |           |               | 0%      |          0 | —     | —     |
| assetTrackerTagSerialNumber            | nvarchar(80)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| serialNumber                           | nvarchar(400)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| componentSerialNumber                  | nvarchar(400)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| boardSerialNumber                      | nvarchar(34)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| enclosureSerialNumber                  | nvarchar(50)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| macAddressValue                        | nvarchar(246)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| ipAddressValue                         | nvarchar(150)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| assetTag                               | nvarchar(160)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| firmwareVersion                        | nvarchar(68)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| hardwareVersion                        | nvarchar(64)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| bayLocation                            | nvarchar(8)    | YES        |            |           |               | 0%      |          0 | —     | —     |
| designValue                            | nvarchar(56)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| ratedCurrent                           | nvarchar(255)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| ratedPower                             | nvarchar(255)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| ratedVoltage                           | nvarchar(1020) | YES        |            |           |               | 0%      |          0 | —     | —     |
| ratedInputVoltage                      | nvarchar(8)    | YES        |            |           |               | 0%      |          0 | —     | —     |
| ratedVa                                | nvarchar(12)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| consumedRackUnits                      | nvarchar(80)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| providedRackUnits                      | nvarchar(255)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| weight                                 | nvarchar(100)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| manufacturerNameSearchableProperty     | nvarchar(80)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| productNameSearchableProperty          | nvarchar(136)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| parentDisplayName                      | nvarchar(80)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| parentPath                             | nvarchar(356)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| rackSide                               | nvarchar(80)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| rackPosition                           | nvarchar(80)   | YES        |            |           |               | 0%      |          0 | —     | —     |
| rackULocation                          | bigint         | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| locationDisplayValue                   | nvarchar(356)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| locationDisplayValueSearchableProperty | nvarchar(356)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| stringCustomProperties                 | nvarchar(3660) | YES        |            |           |               | 0%      |          0 | —     | —     |
| numericCustomProperties                | nvarchar(1288) | YES        |            |           |               | 0%      |          0 | —     | —     |
| dateTimeCustomProperties               | nvarchar(8)    | YES        |            |           |               | 0%      |          0 | —     | —     |
| componentAssets                        | nvarchar(MAX)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| numericSensors                         | nvarchar(MAX)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| stringSensors                          | nvarchar(MAX)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| searchComplexDataFields                | nvarchar(1020) | YES        |            |           |               | 0%      |          0 | —     | —     |
| Path1                                  | nvarchar(344)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| Path2                                  | nvarchar(344)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| Path3                                  | nvarchar(344)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| Path4                                  | nvarchar(344)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| Path5                                  | nvarchar(344)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| Path6                                  | nvarchar(344)  | YES        |            |           |               | 0%      |          0 | —     | —     |

---

### dbo.DimDCIMAssets_old {#dbo-dimdcimassets-old}

| Property | Value |
|---|---|
| Full name | `[dbo].[DimDCIMAssets_old]` |
| Row count | 10,000 |
| Total size | 29.9 MB |
| Used size | 29.0 MB |
| Created | 2022-12-02 21:04 |
| Schema modified | 2023-06-27 17:12 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                                          | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|-------------------------------------------------|----------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| P__metadata_total                               | bigint         | YES        |            |           |               | 0%      |          1 | 10000                      | 10000                      |
| hasChildren                                     | bit            | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| locationData                                    | nvarchar(1020) | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| baseInformationLastUpdated                      | datetime       | YES        |            |           |               | 100%    |          0 | NULL                       | NULL                       |
| accessState                                     | nvarchar(16)   | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| id                                              | nvarchar(144)  | YES        |            |           |               | 0%      |      10000 | —                          | —                          |
| name                                            | nvarchar(160)  | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| status                                          | nvarchar(24)   | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| assetTypeId                                     | nvarchar(56)   | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| assetTypeCategory                               | nvarchar(72)   | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| parentId                                        | nvarchar(144)  | YES        |            |           |               | 0%      |       1020 | —                          | —                          |
| parentName                                      | nvarchar(80)   | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| productId                                       | nvarchar(144)  | YES        |            |           |               | 0%      |        356 | —                          | —                          |
| productName                                     | nvarchar(68)   | YES        |            |           |               | 2%      |        352 | —                          | —                          |
| manufacturerId                                  | nvarchar(144)  | YES        |            |           |               | 0%      |         58 | —                          | —                          |
| manufacturerName                                | nvarchar(64)   | YES        |            |           |               | 2%      |         57 | —                          | —                          |
| dimension                                       | nvarchar(1020) | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| assetLifecycleState                             | nvarchar(44)   | YES        |            |           |               | 0%      |          5 | —                          | —                          |
| discoveryState                                  | nvarchar(60)   | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| monitoringState                                 | nvarchar(12)   | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| locationData.parentId                           | nvarchar(144)  | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| locationData.rackULocation                      | bigint         | YES        |            |           |               | 100%    |          0 | NULL                       | NULL                       |
| locationData.rackSide                           | nvarchar(20)   | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| locationData.updatedDateTime                    | datetime       | YES        |            |           |               | 100%    |          0 | NULL                       | NULL                       |
| P__metadata_limit                               | bigint         | YES        |            |           |               | 0%      |          1 | 200                        | 200                        |
| P__metadata_offset                              | bigint         | YES        |            |           |               | 0%      |         50 | 0                          | 9800                       |
| locationData.rackPosition                       | nvarchar(80)   | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| locationData.locationAccessPolicyChangeStrategy | nvarchar(80)   | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| tabDelimitedPath                                | nvarchar(380)  | YES        |            |           |               | 0%      |       9998 | —                          | —                          |
| accessPolicyId                                  | nvarchar(144)  | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| sensorMonitoringProfileType                     | nvarchar(40)   | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| __FileName                                      | nvarchar(600)  | YES        |            |           |               | 0%      |         50 | —                          | —                          |
| Path1                                           | nvarchar(380)  | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| Path2                                           | nvarchar(380)  | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| Path3                                           | nvarchar(380)  | YES        |            |           |               | 0%      |         24 | —                          | —                          |
| Path4                                           | nvarchar(380)  | YES        |            |           |               | 0%      |         48 | —                          | —                          |
| Path5                                           | nvarchar(380)  | YES        |            |           |               | 1%      |       1622 | —                          | —                          |
| Path6                                           | nvarchar(380)  | YES        |            |           |               | 16%     |       8148 | —                          | —                          |
| displayName                                     | nvarchar(112)  | YES        |            |           |               | 0%      |       9737 | —                          | —                          |
| displayNameLowerCase                            | nvarchar(112)  | YES        |            |           |               | 0%      |       9737 | —                          | —                          |
| statusSearchableProperty                        | nvarchar(24)   | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| createdDateTime                                 | datetime       | YES        |            |           |               | 0%      |       9266 | 2020-04-02 14:09:35.190000 | 2023-05-24 13:39:12.880000 |
| updatedDateTime                                 | datetime       | YES        |            |           |               | 0%      |       9572 | 2020-06-16 08:09:51.430000 | 2023-05-24 13:39:12.880000 |
| commissionDate                                  | nvarchar(1020) | YES        |            |           |               | 100%    |          5 | —                          | —                          |
| retirementDate                                  | nvarchar(80)   | YES        |            |           |               | 99%     |         29 | —                          | —                          |
| endOfLifeDate                                   | nvarchar(1020) | YES        |            |           |               | 100%    |          7 | —                          | —                          |
| nameDataSource                                  | nvarchar(16)   | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| assetTypeDataSource                             | nvarchar(16)   | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| assetType                                       | nvarchar(52)   | YES        |            |           |               | 0%      |         17 | —                          | —                          |
| assetTypeSearchableProperty                     | nvarchar(52)   | YES        |            |           |               | 0%      |         17 | —                          | —                          |
| monitoringProfileType                           | nvarchar(1020) | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| assetAccessPolicyId                             | nvarchar(144)  | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| assetTrackerMasterModuleSerialNumber            | nvarchar(8)    | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| assetTrackerTagSerialNumber                     | nvarchar(8)    | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| serialNumber                                    | nvarchar(108)  | YES        |            |           |               | 0%      |       8860 | —                          | —                          |
| componentSerialNumber                           | nvarchar(8)    | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| boardSerialNumber                               | nvarchar(8)    | YES        |            |           |               | 0%      |         22 | —                          | —                          |
| enclosureSerialNumber                           | nvarchar(8)    | YES        |            |           |               | 0%      |         10 | —                          | —                          |
| macAddressValue                                 | nvarchar(8)    | YES        |            |           |               | 0%      |          5 | —                          | —                          |
| ipAddressValue                                  | nvarchar(8)    | YES        |            |           |               | 0%      |          7 | —                          | —                          |
| assetTag                                        | nvarchar(64)   | YES        |            |           |               | 0%      |       7513 | —                          | —                          |
| firmwareVersion                                 | nvarchar(8)    | YES        |            |           |               | 0%      |         18 | —                          | —                          |
| hardwareVersion                                 | nvarchar(8)    | YES        |            |           |               | 0%      |          5 | —                          | —                          |
| bayLocation                                     | nvarchar(8)    | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| designValue                                     | nvarchar(8)    | YES        |            |           |               | 0%      |          9 | —                          | —                          |
| ratedCurrent                                    | nvarchar(8)    | YES        |            |           |               | 0%      |         12 | —                          | —                          |
| ratedPower                                      | nvarchar(8)    | YES        |            |           |               | 0%      |         47 | —                          | —                          |
| ratedVoltage                                    | nvarchar(8)    | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| ratedInputVoltage                               | nvarchar(8)    | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| ratedVa                                         | nvarchar(8)    | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| consumedRackUnits                               | nvarchar(36)   | YES        |            |           |               | 0%      |         14 | —                          | —                          |
| providedRackUnits                               | nvarchar(8)    | YES        |            |           |               | 0%      |         17 | —                          | —                          |
| weight                                          | nvarchar(100)  | YES        |            |           |               | 0%      |        176 | —                          | —                          |
| manufacturerNameSearchableProperty              | nvarchar(64)   | YES        |            |           |               | 2%      |         57 | —                          | —                          |
| productNameSearchableProperty                   | nvarchar(68)   | YES        |            |           |               | 2%      |        352 | —                          | —                          |
| parentDisplayName                               | nvarchar(76)   | YES        |            |           |               | 0%      |        841 | —                          | —                          |
| parentPath                                      | nvarchar(356)  | YES        |            |           |               | 0%      |       1020 | —                          | —                          |
| rackSide                                        | nvarchar(80)   | YES        |            |           |               | 30%     |          3 | —                          | —                          |
| rackPosition                                    | nvarchar(80)   | YES        |            |           |               | 30%     |          5 | —                          | —                          |
| rackULocation                                   | bigint         | YES        |            |           |               | 32%     |         52 | 1                          | 52                         |
| locationDisplayValue                            | nvarchar(356)  | YES        |            |           |               | 0%      |       7421 | —                          | —                          |
| locationDisplayValueSearchableProperty          | nvarchar(356)  | YES        |            |           |               | 0%      |       7421 | —                          | —                          |
| stringCustomProperties                          | nvarchar(3584) | YES        |            |           |               | 0%      |       7152 | —                          | —                          |
| numericCustomProperties                         | nvarchar(1304) | YES        |            |           |               | 0%      |       6332 | —                          | —                          |
| dateTimeCustomProperties                        | nvarchar(8)    | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| componentAssets                                 | nvarchar(8)    | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| numericSensors                                  | nvarchar(8)    | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| stringSensors                                   | nvarchar(8)    | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| searchComplexDataFields                         | nvarchar(1020) | YES        |            |           |               | 100%    |          0 | —                          | —                          |

---

### dbo.dimDCIMAssetsTrend {#dbo-dimdcimassetstrend}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimDCIMAssetsTrend]` |
| Row count | 25,214 |
| Total size | 170.6 MB |
| Used size | 170.5 MB |
| Created | 2024-04-18 01:52 |
| Schema modified | 2024-04-18 01:52 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                                              | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|-----------------------------------------------------|----------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| record_id                                           | int            | NO         | ✓          |           |               | 0%      |      25214 | 1                          | 25214                      |
| source_system_record_id                             | nvarchar(144)  | YES        |            |           |               | 0%      |      12607 | —                          | —                          |
| asset_alert_status                                  | nvarchar(24)   | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| asset_location_record_id                            | nvarchar(144)  | YES        |            |           |               | 0%      |       1130 | —                          | —                          |
| asset_model_id                                      | nvarchar(144)  | YES        |            |           |               | 0%      |        523 | —                          | —                          |
| asset_name                                          | nvarchar(136)  | YES        |            |           |               | 0%      |        517 | —                          | —                          |
| manufacturer_id                                     | nvarchar(144)  | YES        |            |           |               | 0%      |         71 | —                          | —                          |
| manufacturer_name                                   | nvarchar(80)   | YES        |            |           |               | 0%      |         71 | —                          | —                          |
| asset_lifecycle_state                               | nvarchar(44)   | YES        |            |           |               | 0%      |          5 | —                          | —                          |
| asset_monitoring_state                              | nvarchar(12)   | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| asset_display_name                                  | nvarchar(180)  | YES        |            |           |               | 0%      |      12131 | —                          | —                          |
| asset_created_datetime                              | datetime       | YES        |            |           |               | 0%      |      11414 | 2020-04-01 09:59:50.637000 | 2024-03-08 08:30:43.300000 |
| asset_last_updated_datetime                         | datetime       | YES        |            |           |               | 0%      |      11613 | 2020-06-23 15:22:49.970000 | 2024-03-12 22:06:38.237000 |
| asset_end_of_life_date                              | nvarchar(1020) | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| asset_data_source                                   | nvarchar(16)   | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| asset_type_data_source                              | nvarchar(22)   | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| asset_type_name                                     | nvarchar(56)   | YES        |            |           |               | 0%      |         16 | —                          | —                          |
| asset_access_policy_id                              | nvarchar(144)  | YES        |            |           |               | 0%      |          5 | —                          | —                          |
| asset_serial_number                                 | nvarchar(400)  | YES        |            |           |               | 0%      |      11065 | —                          | —                          |
| component_serial_number                             | nvarchar(400)  | YES        |            |           |               | 0%      |        117 | —                          | —                          |
| board_serial_number                                 | nvarchar(34)   | YES        |            |           |               | 0%      |         20 | —                          | —                          |
| enclosure_serial_number                             | nvarchar(50)   | YES        |            |           |               | 0%      |         11 | —                          | —                          |
| asset_MAC_address                                   | nvarchar(246)  | YES        |            |           |               | 0%      |         26 | —                          | —                          |
| asset_ip_address                                    | nvarchar(150)  | YES        |            |           |               | 0%      |        760 | —                          | —                          |
| asset_tag                                           | nvarchar(160)  | YES        |            |           |               | 0%      |       9339 | —                          | —                          |
| asset_firmware_version                              | nvarchar(68)   | YES        |            |           |               | 0%      |         77 | —                          | —                          |
| asset_hardware_version                              | nvarchar(64)   | YES        |            |           |               | 0%      |         11 | —                          | —                          |
| asset_rack_units_used                               | nvarchar(80)   | YES        |            |           |               | 0%      |         17 | —                          | —                          |
| available_rack_units                                | nvarchar(255)  | YES        |            |           |               | 0%      |         18 | —                          | —                          |
| asset_location_name                                 | nvarchar(80)   | YES        |            |           |               | 0%      |        919 | —                          | —                          |
| asset_location_path                                 | nvarchar(356)  | YES        |            |           |               | 0%      |       1130 | —                          | —                          |
| asset_full_path_location                            | nvarchar(356)  | YES        |            |           |               | 0%      |       8834 | —                          | —                          |
| asset_rack_side_position                            | nvarchar(80)   | YES        |            |           |               | 32%     |          3 | —                          | —                          |
| asset_position                                      | nvarchar(80)   | YES        |            |           |               | 32%     |          7 | —                          | —                          |
| asset_rack_unit_location                            | bigint         | YES        |            |           |               | 36%     |         52 | 1                          | 52                         |
| asset_component_details                             | nvarchar(MAX)  | YES        |            |           |               | 0%      |      10675 | —                          | —                          |
| asset_sensor_numeric_id                             | nvarchar(MAX)  | YES        |            |           |               | 0%      |       2206 | —                          | —                          |
| asset_rack_PDU                                      | nvarchar(MAX)  | YES        |            |           |               | 0%      |         16 | —                          | —                          |
| asset_top_level1_in_location_hierarchy              | nvarchar(344)  | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| asset_building_type_level2_in_location_hierarchy    | nvarchar(344)  | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| asset_code_level3_in_location_hierarchy             | nvarchar(344)  | YES        |            |           |               | 0%      |         20 | —                          | —                          |
| asset_room_type_level4_in_location_hierarchy        | nvarchar(344)  | YES        |            |           |               | 0%      |         53 | —                          | —                          |
| asset_cabinet_or_floor_level5_in_location_hierarchy | nvarchar(344)  | YES        |            |           |               | 0%      |       1927 | —                          | —                          |
| service_id_or_hostname                              | nvarchar(344)  | YES        |            |           |               | 18%     |       9445 | —                          | —                          |
| source_system                                       | nvarchar(25)   | NO         |            |           |               | 0%      |          1 | —                          | —                          |
| archive_date                                        | datetime       | NO         |            |           |               | 0%      |          2 | 2024-03-19 11:01:32.330000 | 2024-04-01 13:45:57.847000 |

---

### dbo.dimDevices {#dbo-dimdevices}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimDevices]` |
| Row count | 3,224 |
| Total size | 11.6 MB |
| Used size | 8.9 MB |
| Created | 2015-12-09 13:58 |
| Schema modified | 2015-12-09 13:58 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column          | Type             | Nullable   | Identity   | Default   | Description   | NULL%   | Distinct   | Min                        | Max                        |
|-----------------|------------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| datacenter_code | nvarchar(15)     | YES        |            |           |               | 0%      | 8          | —                          | —                          |
| device_id       | uniqueidentifier | YES        |            |           |               | 0%      | 3220       | —                          | —                          |
| device_type     | nvarchar(64)     | YES        |            |           |               | 0%      | 13         | —                          | —                          |
| device_name     | nvarchar(64)     | YES        |            |           |               | 0%      | 104        | —                          | —                          |
| location_id     | int              | YES        |            |           |               | 14%     | 2281       | 1                          | 344572                     |
| model           | nvarchar(128)    | YES        |            |           |               | 0%      | 199        | —                          | —                          |
| description     | ntext            | YES        |            |           |               | ?       | ?          | —                          | —                          |
| device_status   | nvarchar(32)     | YES        |            |           |               | 0%      | 10         | —                          | —                          |
| building        | nvarchar(128)    | YES        |            |           |               | 14%     | 12         | —                          | —                          |
| section         | nvarchar(64)     | YES        |            |           |               | 14%     | 21         | —                          | —                          |
| floor           | int              | YES        |            |           |               | 14%     | 4          | 1                          | 4                          |
| row             | nvarchar(32)     | YES        |            |           |               | 14%     | 44         | —                          | —                          |
| slot            | nvarchar(32)     | YES        |            |           |               | 19%     | 53         | —                          | —                          |
| cabinet         | nvarchar(32)     | YES        |            |           |               | 15%     | 80         | —                          | —                          |
| shared          | int              | YES        |            |           |               | 0%      | 2          | 0                          | 1                          |
| use_type        | nvarchar(32)     | YES        |            |           |               | 0%      | 3          | —                          | —                          |
| ownership_type  | nvarchar(32)     | YES        |            |           |               | 0%      | 3          | —                          | —                          |
| owner_id        | nvarchar(255)    | YES        |            |           |               | 1%      | 11         | —                          | —                          |
| service_id      | int              | NO         |            |           |               | 0%      | 3224       | 61370                      | 7981404                    |
| nickname        | nvarchar(64)     | NO         |            |           |               | 0%      | 3199       | —                          | —                          |
| service_name    | nvarchar(255)    | YES        |            |           |               | 0%      | 3224       | —                          | —                          |
| mrc             | numeric(38,2)    | YES        |            |           |               | 0%      | 1519       | 0.00                       | 6958.27                    |
| product         | nvarchar(255)    | NO         |            |           |               | 0%      | 142        | —                          | —                          |
| service_status  | nvarchar(255)    | NO         |            |           |               | 0%      | 7          | —                          | —                          |
| client_id       | int              | NO         |            |           |               | 0%      | 533        | 1000343                    | 7036700                    |
| last_updated    | datetime2        | NO         |            |           |               | 0%      | 1          | 2026-03-06 07:56:53.356666 | 2026-03-06 07:56:53.356666 |

---

### dbo.dimJIRATickets {#dbo-dimjiratickets}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimJIRATickets]` |
| Row count | 124,083 |
| Total size | 37.2 MB |
| Used size | 36.7 MB |
| Created | 2017-12-05 15:43 |
| Schema modified | 2022-06-24 20:25 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column              | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|---------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| jira_number         | int           | YES        |            |           |               | 0%      |     124083 | 10033                      | 2736191                    |
| reporter            | nvarchar(500) | YES        |            |           |               | 0%      |       1809 | —                          | —                          |
| summary             | nvarchar(500) | YES        |            |           |               | 0%      |     102737 | —                          | —                          |
| priority_id         | nvarchar(500) | YES        |            |           |               | 23%     |         16 | —                          | —                          |
| date_opened         | datetime2     | YES        |            |           |               | 0%      |     119830 | 2008-07-10 11:19:35        | 2023-03-21 17:36:00        |
| last_updated        | datetime2     | YES        |            |           |               | 0%      |      86626 | 2008-08-29 12:17:10        | 2023-03-22 01:40:10        |
| creator             | nvarchar(500) | YES        |            |           |               | 0%      |       1643 | —                          | —                          |
| issue_type          | nvarchar(500) | YES        |            |           |               | 0%      |         87 | —                          | —                          |
| issue_status        | nvarchar(500) | YES        |            |           |               | 0%      |         63 | —                          | —                          |
| priority            | nvarchar(500) | YES        |            |           |               | 23%     |         16 | —                          | —                          |
| resolution          | nvarchar(500) | YES        |            |           |               | 6%      |         20 | —                          | —                          |
| resolution_date     | datetime2     | YES        |            |           |               | 8%      |     108382 | 2008-08-20 22:37:20        | 2023-03-21 21:58:24        |
| reporter_department | nvarchar(500) | YES        |            |           |               | 81%     |         26 | —                          | —                          |
| project_name        | nvarchar(500) | YES        |            |           |               | 0%      |        258 | —                          | —                          |
| project_code        | nvarchar(500) | YES        |            |           |               | 0%      |        258 | —                          | —                          |
| last_update         | datetime2     | YES        |            |           |               | 0%      |          1 | 2023-07-18 01:30:04.560000 | 2023-07-18 01:30:04.560000 |
| issuenum            | numeric(18,0) | YES        |            |           |               | 0%      |      57007 | 1                          | 1649603                    |

---

### dbo.dimNotes {#dbo-dimnotes}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimNotes]` |
| Row count | 9,489 |
| Total size | 5.7 MB |
| Used size | 5.6 MB |
| Created | 2021-06-11 17:57 |
| Schema modified | 2021-06-11 17:57 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column            | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|-------------------|----------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| integer_key       | int            | NO         | ✓          |           |               | 0%      |       9489 | 1                          | 9489                       |
| source_system     | varchar(5)     | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| record_id         | int            | NO         |            |           |               | 0%      |       9489 | 15996                      | 7570596                    |
| record_type_id    | int            | NO         |            |           |               | 0%      |       6497 | 59252                      | 7077477                    |
| record_type_level | varchar(8)     | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| company_name      | nvarchar(255)  | NO         |            |           |               | 0%      |       1746 | —                          | —                          |
| user_first_name   | nvarchar(MAX)  | YES        |            |           |               | 0%      |        173 | —                          | —                          |
| user_last_name    | nvarchar(MAX)  | YES        |            |           |               | 0%      |        212 | —                          | —                          |
| note_entry_date   | datetime2      | NO         |            |           |               | 0%      |       9488 | 2018-01-02 09:36:02.482860 | 2021-06-10 17:58:19.450308 |
| user_note         | nvarchar(2000) | YES        |            |           |               | 0%      |       7118 | —                          | —                          |

#### Indexes

| Name                           | Type      | Unique   | PK   | Columns     |
|--------------------------------|-----------|----------|------|-------------|
| PK__dimNotes__93BEB6171FF4BD0B | CLUSTERED | YES      | ✓    | integer_key |

---

### dbo.dimOpportunities {#dbo-dimopportunities}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimOpportunities]` |
| Row count | 14,216 |
| Total size | 28.9 MB |
| Used size | 26.2 MB |
| Created | 2023-06-07 09:51 |
| Schema modified | 2025-07-02 13:38 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                                  | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|-----------------------------------------|----------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| sf_record_id                            | nvarchar(18)   | NO         |            |           |               | 0%      |      14216 | —                          | —                          |
| sf_account_id                           | nvarchar(25)   | NO         |            |           |               | 0%      |       2631 | —                          | —                          |
| account_name                            | nvarchar(255)  | NO         |            |           |               | 0%      |       2620 | —                          | —                          |
| ocean_client_ids                        | nvarchar(255)  | YES        |            |           |               | 0%      |       1729 | —                          | —                          |
| active_client_ids                       | nvarchar(25)   | YES        |            |           |               | 0%      |         11 | —                          | —                          |
| opp_contact_name                        | nvarchar(512)  | YES        |            |           |               | 0%      |       2774 | —                          | —                          |
| opp_contact_email                       | nvarchar(3000) | YES        |            |           |               | 0%      |       1962 | —                          | —                          |
| opportunity_id                          | nvarchar(18)   | NO         |            |           |               | 0%      |      14216 | —                          | —                          |
| opportunity_number                      | nvarchar(30)   | YES        |            |           |               | 0%      |      14216 | —                          | —                          |
| opp_record_type                         | nvarchar(80)   | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| opp_owner_name                          | nvarchar(121)  | YES        |            |           |               | 0%      |         95 | —                          | —                          |
| opp_owner_geography                     | nvarchar(255)  | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| opp_owner_role                          | nvarchar(80)   | YES        |            |           |               | 0%      |         17 | —                          | —                          |
| created_date                            | datetime2      | YES        |            |           |               | 0%      |       1369 | 2021-03-01 00:00:00        | 2026-03-06 00:00:00        |
| created_by                              | nvarchar(121)  | YES        |            |           |               | 0%      |        113 | —                          | —                          |
| intended_close_date                     | datetime2      | YES        |            |           |               | 0%      |       1620 | 2021-02-03 00:00:00        | 2030-09-11 00:00:00        |
| last_modified_date                      | datetime2      | YES        |            |           |               | 0%      |        338 | 2023-05-31 00:00:00        | 2026-03-06 00:00:00        |
| cad_budget_nominal_value                | decimal(12,2)  | YES        |            |           |               | 1%      |       4942 | -61727.00                  | 1800000.00                 |
| cad_budget_adjusted_value               | decimal(12,2)  | YES        |            |           |               | 1%      |       3949 | 0.00                       | 1781901.00                 |
| probability_to_close_in_perc            | decimal(6,2)   | YES        |            |           |               | 0%      |         10 | 0.00                       | 100.00                     |
| cad_budget_nominal_NRC                  | decimal(12,2)  | YES        |            |           |               | 0%      |        549 | 0.00                       | 633850.00                  |
| cad_budget_adjusted_NRC                 | decimal(12,2)  | YES        |            |           |               | 0%      |        364 | 0.00                       | 633850.00                  |
| cad_budget_other_NRC                    | decimal(12,2)  | YES        |            |           |               | 10%     |        507 | 0.00                       | 1281690.00                 |
| cad_budget_TCV                          | decimal(12,2)  | YES        |            |           |               | 0%      |       5871 | -4156.35                   | 4788020253.24              |
| opp_contract_term_months                | decimal(6,2)   | YES        |            |           |               | 1%      |         61 | 0.00                       | 136.00                     |
| opp_comments                            | nvarchar(MAX)  | YES        |            |           |               | 64%     |       4581 | —                          | —                          |
| opp_name                                | nvarchar(120)  | YES        |            |           |               | 0%      |      12976 | —                          | —                          |
| customer_rejection_reason               | nvarchar(30)   | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| campaign_name                           | nvarchar(80)   | YES        |            |           |               | 0%      |         85 | —                          | —                          |
| opp_is_closed                           | nvarchar(5)    | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| opp_is_won                              | nvarchar(5)    | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| initial_stage_name                      | nvarchar(255)  | YES        |            |           |               | 0%      |         14 | —                          | —                          |
| forecast_category                       | nvarchar(255)  | YES        |            |           |               | 0%      |          6 | —                          | —                          |
| line_of_business                        | nvarchar(255)  | YES        |            |           |               | 0%      |         17 | —                          | —                          |
| Cloud_line_of_business                  | nvarchar(255)  | YES        |            |           |               | 0%      |         19 | —                          | —                          |
| cloud_type                              | nvarchar(255)  | YES        |            |           |               | 0%      |         26 | —                          | —                          |
| opp_next_step                           | nvarchar(255)  | YES        |            |           |               | 0%      |       8647 | —                          | —                          |
| next_activity_scheduled_date            | datetime2      | YES        |            |           |               | 100%    |          0 | NULL                       | NULL                       |
| next_step_last_modified_date            | datetime2      | YES        |            |           |               | 57%     |       1216 | 2021-03-01 00:00:00        | 2026-03-06 00:00:00        |
| days_since_next_activity_scheduled_date | decimal(12,2)  | YES        |            |           |               | 100%    |          0 | NULL                       | NULL                       |
| days_closed                             | decimal(12,2)  | YES        |            |           |               | 0%      |       6338 | 0.00                       | 1831.83                    |
| opp_age_in_days                         | decimal(12,2)  | YES        |            |           |               | 0%      |       1074 | 0.00                       | 1711.00                    |
| converted_lead_source                   | nvarchar(255)  | YES        |            |           |               | 0%      |         10 | —                          | —                          |
| push_count                              | decimal(12,2)  | YES        |            |           |               | 50%     |         30 | 1.00                       | 33.00                      |
| opp_type                                | nvarchar(255)  | YES        |            |           |               | 0%      |          7 | —                          | —                          |
| partner_referring_opp                   | nvarchar(255)  | YES        |            |           |               | 0%      |         79 | —                          | —                          |
| deal_desk_requests_associated           | int            | YES        |            |           |               | 0%      |          9 | 0                          | 11                         |
| is_reseller_deal                        | nvarchar(5)    | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| lost_reason                             | nvarchar(255)  | YES        |            |           |               | 0%      |          6 | —                          | —                          |
| lost_reason_details                     | nvarchar(255)  | YES        |            |           |               | 0%      |         15 | —                          | —                          |
| current_stage_name                      | nvarchar(255)  | YES        |            |           |               | 0%      |         15 | —                          | —                          |
| opp_current_stage_change_date           | datetime2      | YES        |            |           |               | 0%      |      13344 | 2021-03-01 10:31:59        | 2026-03-06 17:06:21        |
| is_CloudOpps_opp                        | nvarchar(5)    | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| archive_date                            | datetime2      | NO         |            |           |               | 0%      |          1 | 2026-03-07 06:30:46.040000 | 2026-03-07 06:30:46.040000 |
| cad_budget_setup_cost                   | decimal(12,2)  | YES        |            |           |               | 14%     |        251 | 0.00                       | 831250.00                  |
| opp_is_a_partner_deal                   | nvarchar(5)    | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| total_renewal_mrc                       | decimal(12,2)  | YES        |            |           |               | 24%     |       1330 | 0.00                       | 477600.00                  |
| gseid                                   | nchar(10)      | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| gseid1                                  | nvarchar(50)   | YES        |            |           |               | 86%     |       2042 | —                          | —                          |

#### Indexes

| Name                           | Type      | Unique   | PK   | Columns      |
|--------------------------------|-----------|----------|------|--------------|
| PK__dimOppor__F1AAD65382040696 | CLUSTERED | YES      | ✓    | sf_record_id |

---

### dbo.dimProduct {#dbo-dimproduct}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimProduct]` |
| Row count | 17 |
| Total size | 0.1 MB |
| Used size | 0.0 MB |
| Created | 2020-06-02 16:34 |
| Schema modified | 2020-06-04 15:40 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max   |
|-----------------------|----------------|------------|------------|-----------|---------------|---------|------------|-------|-------|
| product_group_id      | int            | NO         | ✓          |           |               | 0%      |         17 | 1     | 17    |
| product_name          | nvarchar(255)  | YES        |            |           |               | 0%      |         17 | —     | —     |
| definition            | nvarchar(4000) | YES        |            |           |               | 0%      |         17 | —     | —     |
| cad_budget_mrc        | numeric(38,4)  | YES        |            |           |               | 100%    |          0 | NULL  | NULL  |
| active_customer_count | numeric(38,4)  | YES        |            |           |               | 100%    |          0 | NULL  | NULL  |
| release_date          | datetime2      | YES        |            |           |               | 100%    |          0 | NULL  | NULL  |

#### Indexes

| Name          | Type      | Unique   | PK   | Columns          |
|---------------|-----------|----------|------|------------------|
| PK_dimproduct | CLUSTERED | YES      | ✓    | product_group_id |

---

### dbo.dimProductAttributes {#dbo-dimproductattributes}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimProductAttributes]` |
| Row count | 7,101 |
| Total size | 4.4 MB |
| Used size | 3.5 MB |
| Created | 2019-01-08 10:55 |
| Schema modified | 2021-03-18 20:07 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                    | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                        |
|---------------------------|----------------|------------|------------|-----------|---------------|---------|------------|---------------------|----------------------------|
| fusion_id                 | nvarchar(255)  | YES        |            |           |               | 0%      |       6063 | —                   | —                          |
| sku_name                  | nvarchar(4000) | YES        |            |           |               | 0%      |       6979 | —                   | —                          |
| level                     | nvarchar(255)  | YES        |            |           |               | 0%      |          2 | —                   | —                          |
| is_active                 | nvarchar(255)  | YES        |            |           |               | 0%      |          2 | —                   | —                          |
| type                      | nvarchar(255)  | YES        |            |           |               | 0%      |        324 | —                   | —                          |
| service_type              | nvarchar(255)  | YES        |            |           |               | 16%     |         47 | —                   | —                          |
| category                  | nvarchar(255)  | YES        |            |           |               | 16%     |         17 | —                   | —                          |
| functional_group          | nvarchar(255)  | YES        |            |           |               | 36%     |        153 | —                   | —                          |
| lifecycle                 | nvarchar(255)  | YES        |            |           |               | 44%     |          7 | —                   | —                          |
| product_group             | nvarchar(255)  | YES        |            |           |               | 28%     |         21 | —                   | —                          |
| license_cost_cad          | numeric(38,4)  | YES        |            |           |               | 100%    |          0 | NULL                | NULL                       |
| functional_group_bi       | nvarchar(255)  | YES        |            |           |               | 78%     |         20 | —                   | —                          |
| sku_nickname              | nvarchar(255)  | YES        |            |           |               | 80%     |         14 | —                   | —                          |
| search_keywords           | nvarchar(4000) | YES        |            |           |               | 86%     |         16 | —                   | —                          |
| adjusted_line_of_business | nvarchar(255)  | YES        |            |           |               | 66%     |          4 | —                   | —                          |
| technology_group          | nvarchar(255)  | YES        |            |           |               | 61%     |          5 | —                   | —                          |
| product_type              | nvarchar(255)  | YES        |            |           |               | 62%     |         24 | —                   | —                          |
| product_line              | nvarchar(255)  | YES        |            |           |               | 84%     |          5 | —                   | —                          |
| product_part              | nvarchar(255)  | YES        |            |           |               | 99%     |          5 | —                   | —                          |
| vendor                    | nvarchar(255)  | YES        |            |           |               | 73%     |         28 | —                   | —                          |
| product_cost_cad          | numeric(38,4)  | YES        |            |           |               | 100%    |          0 | NULL                | NULL                       |
| release_date              | datetime2      | YES        |            |           |               | 0%      |       6294 | 2008-08-02 02:11:51 | 2026-03-05 15:38:35.384646 |
| product                   | nvarchar(255)  | YES        |            |           |               | 27%     |        108 | —                   | —                          |
| product_category          | nvarchar(255)  | YES        |            |           |               | 61%     |          4 | —                   | —                          |
| product_detail            | nvarchar(255)  | YES        |            |           |               | 5%      |         27 | —                   | —                          |
| new_lob_2021              | nvarchar(MAX)  | YES        |            |           |               | 15%     |          8 | —                   | —                          |

---

### dbo.dimProductRevenue {#dbo-dimproductrevenue}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimProductRevenue]` |
| Row count | 1,901,954 |
| Total size | 807.9 MB |
| Used size | 807.8 MB |
| Created | 2021-04-06 19:20 |
| Schema modified | 2021-04-06 19:20 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column           | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|------------------|----------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| gp_entity        | varchar(5)     | NO         |            |           |               | 0%      |          6 | —                   | —                   |
| client_id        | char(15)       | NO         |            |           |               | 0%      |       1828 | —                   | —                   |
| document_number  | char(21)       | NO         |            |           |               | 0%      |      95453 | —                   | —                   |
| lnitmseq         | int            | NO         |            |           |               | 0%      |      16476 | 8192                | 313344000           |
| document_type    | smallint       | NO         |            |           |               | 0%      |          2 | 3                   | 4                   |
| item_number      | char(31)       | NO         |            |           |               | 0%      |       2084 | —                   | —                   |
| product_line     | nvarchar(255)  | YES        |            |           |               | 8%      |          5 | —                   | —                   |
| product_group    | nvarchar(255)  | YES        |            |           |               | 2%      |         14 | —                   | —                   |
| product          | nvarchar(255)  | YES        |            |           |               | 2%      |         64 | —                   | —                   |
| product_category | nvarchar(255)  | YES        |            |           |               | 91%     |          5 | —                   | —                   |
| product_detail   | nvarchar(255)  | YES        |            |           |               | 1%      |         52 | —                   | —                   |
| sku_name         | nvarchar(4000) | YES        |            |           |               | 0%      |       1674 | —                   | —                   |
| amount           | numeric(38,6)  | YES        |            |           |               | 0%      |     146641 | -596043.756000      | 2981711.040000      |
| period_start     | datetime       | YES        |            |           |               | 0%      |       1700 | 2021-09-01 00:00:00 | 4748-05-24 00:00:00 |
| original_lob     | nvarchar(255)  | YES        |            |           |               | 0%      |          6 | —                   | —                   |
| level            | nvarchar(255)  | YES        |            |           |               | 0%      |          6 | —                   | —                   |
| product_taxonomy | nvarchar(255)  | YES        |            |           |               | 2%      |         47 | —                   | —                   |
| service_id       | varchar(21)    | NO         |            |           |               | 0%      |      13009 | —                   | —                   |
| new_lob          | nvarchar(255)  | YES        |            |           |               | 3%      |          7 | —                   | —                   |
| CURNCYID         | char(15)       | NO         |            |           |               | 0%      |          4 | —                   | —                   |
| datacenter       | nvarchar(15)   | YES        |            |           |               | 0%      |         26 | —                   | —                   |
| XTNDPRCE         | numeric(38,6)  | YES        |            |           |               | 0%      |     124831 | -448153.200000      | 2381443.000000      |
| OXTNDPRC         | numeric(38,6)  | YES        |            |           |               | 0%      |     100870 | -330000.000000      | 2381443.000000      |

---

### dbo.dimsalesrepscp1 {#dbo-dimsalesrepscp1}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimsalesrepscp1]` |
| Row count | 11 |
| Total size | 0.1 MB |
| Used size | 0.1 MB |
| Created | 2020-01-14 16:36 |
| Schema modified | 2020-01-14 16:36 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column           | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| general_manager  | nvarchar(255) | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| director         | nvarchar(255) | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| director_role    | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| director_sf_id   | nvarchar(50)  | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| manager          | nvarchar(255) | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| manager_role     | nvarchar(255) | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| manager_sf_id    | nvarchar(50)  | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| sales_rep        | nvarchar(255) | YES        |            |           |               | 0%      |          7 | —                          | —                          |
| sales_rep_role   | nvarchar(255) | YES        |            |           |               | 0%      |          6 | —                          | —                          |
| sales_rep_sf_id  | nvarchar(50)  | YES        |            |           |               | 0%      |          7 | —                          | —                          |
| sales_rep_region | nvarchar(50)  | YES        |            |           |               | 82%     |          1 | —                          | —                          |
| sales_rep_level  | nvarchar(50)  | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| last_updated     | datetime      | NO         |            |           |               | 0%      |          1 | 2026-03-06 07:46:02.497000 | 2026-03-06 07:46:02.497000 |

---

### dbo.dimServiceAttributes {#dbo-dimserviceattributes}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimServiceAttributes]` |
| Row count | 162,720 |
| Total size | 62.0 MB |
| Used size | 61.0 MB |
| Created | 2016-03-31 09:37 |
| Schema modified | 2019-12-05 19:00 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                    | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|---------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| service_id                | int           | NO         |            |           |               | 0%      |     162720 | 282                        | 7981445                    |
| client_id                 | int           | NO         |            |           |               | 0%      |      20370 | 101                        | 7036720                    |
| service_status            | nvarchar(255) | YES        |            |           |               | 0%      |         11 | —                          | —                          |
| is_active                 | nvarchar(3)   | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| provision_date            | datetime2     | YES        |            |           |               | 0%      |     150008 | 1999-05-17 00:00:00        | 2026-03-05 10:30:59.713333 |
| cancel_date               | datetime2     | YES        |            |           |               | 19%     |     131080 | 2008-08-12 00:08:02.246666 | 2026-03-05 18:55:25.293333 |
| deprovision_date          | datetime2     | YES        |            |           |               | 18%     |     131983 | 2008-08-22 11:05:04.063333 | 2026-03-05 15:19:53.840000 |
| offline_date              | datetime2     | YES        |            |           |               | 86%     |      12255 | 2009-04-08 15:34:22.990000 | 2026-01-06 10:40:48.513333 |
| product                   | nvarchar(255) | YES        |            |           |               | 0%      |       1001 | —                          | —                          |
| nickname                  | nvarchar(64)  | YES        |            |           |               | 0%      |     156360 | —                          | —                          |
| server_name               | nvarchar(255) | YES        |            |           |               | 0%      |     159693 | —                          | —                          |
| OS                        | nvarchar(255) | YES        |            |           |               | 27%     |        875 | —                          | —                          |
| is_pci                    | nvarchar(3)   | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| is_magento                | nvarchar(3)   | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| datacenter_name           | nvarchar(100) | YES        |            |           |               | 0%      |         47 | —                          | —                          |
| datacenter_city           | nvarchar(100) | YES        |            |           |               | 0%      |         34 | —                          | —                          |
| datacenter_code           | nvarchar(15)  | YES        |            |           |               | 0%      |         47 | —                          | —                          |
| contract_length           | int           | YES        |            |           |               | 0%      |         67 | 1                          | 120                        |
| contract_months_remaining | int           | YES        |            |           |               | 96%     |         36 | 1                          | 36                         |
| service_type              | nvarchar(64)  | YES        |            |           |               | 0%      |         22 | —                          | —                          |
| line_of_business          | nvarchar(255) | YES        |            |           |               | 0%      |          7 | —                          | —                          |
| last_updated              | datetime2     | NO         |            |           |               | 0%      |          1 | 2026-03-06 07:46:20.863333 | 2026-03-06 07:46:20.863333 |
| fusion_id                 | int           | YES        |            |           |               | 0%      |        923 | 1                          | 1293                       |
| adjusted_line_of_business | nvarchar(255) | YES        |            |           |               | 0%      |          5 | —                          | —                          |

#### Indexes

| Name                    | Type      | Unique   | PK   | Columns    |
|-------------------------|-----------|----------|------|------------|
| PK_dimServiceAttributes | CLUSTERED | YES      | ✓    | service_id |

---

### dbo.dimServices {#dbo-dimservices}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimServices]` |
| Row count | 5,831 |
| Total size | 27.1 MB |
| Used size | 7.2 MB |
| Created | 2016-03-29 10:34 |
| Schema modified | 2020-04-06 19:00 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                    | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|---------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| client_id                 | int           | NO         |            |           |               | 0%      |        789 | 1000002                    | 7036720                    |
| company_name              | nvarchar(255) | YES        |            |           |               | 0%      |        789 | —                          | —                          |
| service_id                | int           | NO         |            |           |               | 0%      |       5831 | -7008600                   | 7981445                    |
| nickname                  | nvarchar(64)  | NO         |            |           |               | 0%      |       5646 | —                          | —                          |
| server_name               | nvarchar(255) | YES        |            |           |               | 0%      |       5691 | —                          | —                          |
| product                   | nvarchar(255) | YES        |            |           |               | 0%      |        243 | —                          | —                          |
| service_status            | nvarchar(255) | YES        |            |           |               | 0%      |          8 | —                          | —                          |
| os                        | nvarchar(255) | YES        |            |           |               | 45%     |        162 | —                          | —                          |
| currency                  | nvarchar(3)   | NO         |            |           |               | 0%      |          4 | —                          | —                          |
| provision_date            | datetime2     | YES        |            |           |               | 2%      |       5681 | 1999-01-01 00:00:00        | 2026-03-05 10:30:59.713333 |
| datacenter_name           | nvarchar(100) | YES        |            |           |               | 0%      |         27 | —                          | —                          |
| datacenter_city           | nvarchar(100) | YES        |            |           |               | 0%      |         21 | —                          | —                          |
| datacenter_code           | nvarchar(15)  | YES        |            |           |               | 0%      |         26 | —                          | —                          |
| line_of_business          | nvarchar(255) | YES        |            |           |               | 0%      |          5 | —                          | —                          |
| device_id                 | nvarchar(64)  | YES        |            |           |               | 37%     |       3669 | —                          | —                          |
| service_type              | nvarchar(64)  | YES        |            |           |               | 0%      |         18 | —                          | —                          |
| mrc                       | numeric(38,4) | YES        |            |           |               | 0%      |       2353 | 0.0000                     | 32838.3500                 |
| usd_mrc                   | numeric(38,4) | YES        |            |           |               | 0%      |       2449 | 0.0000                     | 32679.2918                 |
| cad_mrc                   | numeric(38,4) | YES        |            |           |               | 0%      |       2449 | 0.0000                     | 42158.8881                 |
| contract_length           | int           | YES        |            |           |               | 0%      |         48 | -1                         | 63                         |
| contract_months_remaining | int           | YES        |            |           |               | 1%      |         37 | -1                         | 36                         |
| last_updated              | datetime2     | NO         |            |           |               | 0%      |          2 | 2026-03-06 07:46:07.846666 | 2026-03-06 07:46:14.166666 |
| cad_budget_mrc            | numeric(38,4) | YES        |            |           |               | 0%      |       2444 | 0.0000                     | 39723.7500                 |
| fusion_id                 | int           | YES        |            |           |               | 0%      |        233 | 0                          | 1293                       |
| adjusted_line_of_business | nvarchar(255) | YES        |            |           |               | 0%      |          4 | —                          | —                          |

#### Indexes

| Name           | Type      | Unique   | PK   | Columns    |
|----------------|-----------|----------|------|------------|
| PK_DimServices | CLUSTERED | YES      | ✓    | service_id |

---

### dbo.dimServices_TTSSiteScout {#dbo-dimservices-ttssitescout}

| Property | Value |
|---|---|
| Full name | `[dbo].[dimServices_TTSSiteScout]` |
| Row count | 1,046 |
| Total size | 0.6 MB |
| Used size | 0.6 MB |
| Created | 2020-11-12 09:12 |
| Schema modified | 2020-11-12 09:12 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                    | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|---------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| client_id                 | int           | NO         |            |           |               | 0%      |          1 | 7007612                    | 7007612                    |
| company_name              | nvarchar(255) | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| service_id                | int           | NO         |            |           |               | 0%      |       1046 | 4879547                    | 7963585                    |
| nickname                  | nvarchar(64)  | NO         |            |           |               | 0%      |       1046 | —                          | —                          |
| server_name               | nvarchar(255) | YES        |            |           |               | 0%      |       1046 | —                          | —                          |
| product                   | nvarchar(255) | YES        |            |           |               | 0%      |         21 | —                          | —                          |
| service_status            | nvarchar(255) | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| os                        | nvarchar(255) | YES        |            |           |               | 10%     |          2 | —                          | —                          |
| currency                  | nvarchar(3)   | NO         |            |           |               | 0%      |          1 | —                          | —                          |
| provision_date            | datetime2     | YES        |            |           |               | 0%      |       1046 | 2016-08-09 15:37:25.376666 | 2026-03-04 11:19:20.940000 |
| datacenter_name           | nvarchar(100) | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| datacenter_city           | nvarchar(100) | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| datacenter_code           | nvarchar(15)  | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| line_of_business          | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| device_id                 | nvarchar(64)  | YES        |            |           |               | 7%      |        970 | —                          | —                          |
| service_type              | nvarchar(64)  | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| mrc                       | numeric(38,4) | YES        |            |           |               | 0%      |         84 | 0.0000                     | 5900.0000                  |
| usd_mrc                   | numeric(38,4) | YES        |            |           |               | 0%      |         84 | 0.0000                     | 5900.0000                  |
| cad_mrc                   | numeric(38,4) | YES        |            |           |               | 0%      |         84 | 0.0000                     | 7949.0848                  |
| contract_length           | int           | YES        |            |           |               | 0%      |          8 | 1                          | 36                         |
| contract_months_remaining | int           | YES        |            |           |               | 0%      |          9 | 1                          | 30                         |
| last_updated              | datetime2     | NO         |            |           |               | 0%      |          1 | 2026-03-06 07:46:07.846666 | 2026-03-06 07:46:07.846666 |
| cad_budget_mrc            | numeric(38,4) | YES        |            |           |               | 0%      |         84 | 0.0000                     | 7847.0000                  |
| fusion_id                 | int           | YES        |            |           |               | 0%      |         21 | 807                        | 1282                       |
| adjusted_line_of_business | nvarchar(255) | YES        |            |           |               | 0%      |          2 | —                          | —                          |

#### Indexes

| Name                        | Type      | Unique   | PK   | Columns    |
|-----------------------------|-----------|----------|------|------------|
| PK_dimServices_TTSSiteScout | CLUSTERED | YES      | ✓    | service_id |

---

### dbo.DimTLSAttributes {#dbo-dimtlsattributes}

| Property | Value |
|---|---|
| Full name | `[dbo].[DimTLSAttributes]` |
| Row count | 222 |
| Total size | 0.1 MB |
| Used size | 0.0 MB |
| Created | 2025-02-20 11:09 |
| Schema modified | 2025-02-20 11:09 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                 | Type         | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max   |
|------------------------|--------------|------------|------------|-----------|---------------|---------|------------|-------|-------|
| product                | varchar(MAX) | YES        |            |           |               | 0%      |        222 | —     | —     |
| type                   | varchar(MAX) | YES        |            |           |               | 0%      |         11 | —     | —     |
| hardware_model         | varchar(MAX) | YES        |            |           |               | 0%      |         23 | —     | —     |
| generation             | varchar(MAX) | YES        |            |           |               | 0%      |          9 | —     | —     |
| rmu_consumtion         | varchar(MAX) | YES        |            |           |               | 0%      |         10 | —     | —     |
| provisioning_effort_hr | float(53)    | YES        |            |           |               | 0%      |          7 | 0.0   | 10.0  |
| eol_status             | varchar(MAX) | YES        |            |           |               | 0%      |          3 | —     | —     |
| power_usage_estimate   | varchar(MAX) | YES        |            |           |               | 0%      |         41 | —     | —     |
| dual_psu_capable       | varchar(MAX) | YES        |            |           |               | 0%      |          2 | —     | —     |

---

### dbo.mrc_changes {#dbo-mrc-changes}

| Property | Value |
|---|---|
| Full name | `[dbo].[mrc_changes]` |
| Row count | 476,409 |
| Total size | 74.6 MB |
| Used size | 72.3 MB |
| Created | 2019-09-26 13:28 |
| Schema modified | 2019-09-26 13:28 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column            | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|-------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| integer_key       | int           | YES        |            |           |               | 0%      |     476409 | 1                   | 2518251             |
| sku_id            | int           | YES        |            |           |               | 0%      |       3175 | 1                   | 6364                |
| sku_level         | nvarchar(10)  | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| mrc               | numeric(38,4) | YES        |            |           |               | 0%      |      20163 | -2948.9222          | 717509.9979         |
| currency          | nvarchar(3)   | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| service_id        | nvarchar(255) | YES        |            |           |               | 0%      |      37538 | —                   | —                   |
| source_record_id  | nvarchar(255) | YES        |            |           |               | 0%      |     396671 | —                   | —                   |
| record_start_date | datetime2     | YES        |            |           |               | 0%      |       1743 | 2019-09-23 00:00:00 | 2026-03-06 00:00:00 |
| record_end_date   | datetime2     | YES        |            |           |               | 14%     |       2061 | 2019-09-25 00:00:00 | 2026-03-06 00:00:00 |
| start_reason      | nvarchar(50)  | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| end_reason        | nvarchar(50)  | YES        |            |           |               | 14%     |          2 | —                   | —                   |
| current_record    | nvarchar(1)   | YES        |            |           |               | 0%      |          2 | —                   | —                   |

---

### dbo.MRCTrend {#dbo-mrctrend}

| Property | Value |
|---|---|
| Full name | `[dbo].[MRCTrend]` |
| Row count | 327,457 |
| Total size | 135.7 MB |
| Used size | 134.8 MB |
| Created | 2016-05-09 09:59 |
| Schema modified | 2021-07-01 19:01 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                    | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|---------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| integer_key               | int           | NO         |            |           |               | 0%      |     327457 | 4437472                    | 4802601                    |
| client_id                 | int           | YES        |            |           |               | 0%      |       1735 | 1000329                    | 7036716                    |
| company_name              | nvarchar(255) | YES        |            |           |               | 0%      |       1788 | —                          | —                          |
| client_created            | datetime2     | YES        |            |           |               | 0%      |       1643 | 1998-08-17 00:00:00        | 2025-12-09 17:13:16.596373 |
| service_id                | int           | YES        |            |           |               | 0%      |      12221 | 25143                      | 7981405                    |
| service_name              | nvarchar(50)  | YES        |            |           |               | 0%      |      12087 | —                          | —                          |
| service_type              | nvarchar(255) | YES        |            |           |               | 0%      |         18 | —                          | —                          |
| product                   | nvarchar(255) | YES        |            |           |               | 0%      |        295 | —                          | —                          |
| os                        | nvarchar(255) | YES        |            |           |               | 36%     |        288 | —                          | —                          |
| service_status            | nvarchar(255) | YES        |            |           |               | 0%      |          9 | —                          | —                          |
| datacenter_code           | nvarchar(15)  | YES        |            |           |               | 0%      |         35 | —                          | —                          |
| datacenter_name           | nvarchar(100) | YES        |            |           |               | 0%      |         35 | —                          | —                          |
| datacenter_city           | nvarchar(100) | YES        |            |           |               | 0%      |         27 | —                          | —                          |
| mrc                       | numeric(38,4) | YES        |            |           |               | 0%      |      10831 | 0.0000                     | 22640.0000                 |
| sales_rep                 | nvarchar(255) | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| tam                       | nvarchar(255) | YES        |            |           |               | 63%     |         14 | —                          | —                          |
| provision_date            | datetime2     | YES        |            |           |               | 1%      |      16980 | 2004-05-12 15:33:56.301640 | 2026-02-24 13:29:43.486666 |
| line_of_business          | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| currency                  | nvarchar(3)   | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| usd_mrc                   | numeric(38,4) | YES        |            |           |               | 0%      |      51360 | 0.0000                     | 22640.0000                 |
| cad_mrc                   | numeric(38,4) | YES        |            |           |               | 0%      |     109567 | 0.0000                     | 30953.6978                 |
| archive_date              | datetime      | YES        |            |           |               | 0%      |         48 | 2022-03-31 00:00:00        | 2026-02-28 00:00:00        |
| cad_budget_mrc            | numeric(38,4) | YES        |            |           |               | 0%      |      11664 | 0.0000                     | 30111.2000                 |
| adjusted_line_of_business | nvarchar(50)  | YES        |            |           |               | 0%      |          2 | —                          | —                          |

#### Indexes

| Name                           | Type      | Unique   | PK   | Columns     |
|--------------------------------|-----------|----------|------|-------------|
| PK__MRCTrend__93BEB617173876EA | CLUSTERED | YES      | ✓    | integer_key |

---

### dbo.MRCTrend_TTSSiteScout {#dbo-mrctrend-ttssitescout}

| Property | Value |
|---|---|
| Full name | `[dbo].[MRCTrend_TTSSiteScout]` |
| Row count | 63,911 |
| Total size | 26.8 MB |
| Used size | 26.8 MB |
| Created | 2020-11-12 11:06 |
| Schema modified | 2020-11-12 11:06 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                    | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|---------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| integer_key               | int           | NO         |            |           |               | 0%      |      63911 | 4443230                    | 4799668                    |
| client_id                 | int           | YES        |            |           |               | 0%      |          1 | 7007612                    | 7007612                    |
| company_name              | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| client_created            | datetime2     | YES        |            |           |               | 0%      |          1 | 2012-03-07 16:36:03.677227 | 2012-03-07 16:36:03.677227 |
| service_id                | int           | YES        |            |           |               | 0%      |       2563 | 4494932                    | 7963585                    |
| service_name              | nvarchar(50)  | YES        |            |           |               | 0%      |       2563 | —                          | —                          |
| service_type              | nvarchar(255) | YES        |            |           |               | 0%      |          5 | —                          | —                          |
| product                   | nvarchar(255) | YES        |            |           |               | 0%      |         28 | —                          | —                          |
| os                        | nvarchar(255) | YES        |            |           |               | 11%     |          7 | —                          | —                          |
| service_status            | nvarchar(255) | YES        |            |           |               | 0%      |          5 | —                          | —                          |
| datacenter_code           | nvarchar(15)  | YES        |            |           |               | 0%      |          6 | —                          | —                          |
| datacenter_name           | nvarchar(100) | YES        |            |           |               | 0%      |          6 | —                          | —                          |
| datacenter_city           | nvarchar(100) | YES        |            |           |               | 0%      |          6 | —                          | —                          |
| mrc                       | numeric(38,4) | YES        |            |           |               | 0%      |        231 | 0.0000                     | 7375.0000                  |
| sales_rep                 | nvarchar(255) | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| tam                       | nvarchar(255) | YES        |            |           |               | 27%     |          3 | —                          | —                          |
| provision_date            | datetime2     | YES        |            |           |               | 2%      |       3592 | 2015-10-20 18:13:51.859322 | 2025-11-05 12:13:06.923333 |
| line_of_business          | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| currency                  | nvarchar(3)   | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| usd_mrc                   | numeric(38,4) | YES        |            |           |               | 0%      |        231 | 0.0000                     | 7375.0000                  |
| cad_mrc                   | numeric(38,4) | YES        |            |           |               | 0%      |       5156 | 0.0000                     | 10222.7862                 |
| archive_date              | datetime      | YES        |            |           |               | 0%      |         48 | 2022-03-31 00:00:00        | 2026-02-28 00:00:00        |
| cad_budget_mrc            | numeric(38,4) | YES        |            |           |               | 0%      |        231 | 0.0000                     | 9808.7500                  |
| adjusted_line_of_business | nvarchar(50)  | YES        |            |           |               | 0%      |          2 | —                          | —                          |

#### Indexes

| Name                                        | Type      | Unique   | PK   | Columns     |
|---------------------------------------------|-----------|----------|------|-------------|
| PK__MRCTrend_TTSSiteScout__93BEB617173876EA | CLUSTERED | YES      | ✓    | integer_key |

---

### dbo.MrcTrendColo {#dbo-mrctrendcolo}

| Property | Value |
|---|---|
| Full name | `[dbo].[MrcTrendColo]` |
| Row count | 131,000 |
| Total size | 57.6 MB |
| Used size | 38.1 MB |
| Created | 2016-05-16 12:18 |
| Schema modified | 2020-02-24 13:27 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                    | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min        | Max          |
|---------------------------|---------------|------------|------------|-----------|---------------|---------|------------|------------|--------------|
| integer_key               | int           | NO         |            |           |               | 0%      |     131000 | 811914     | 944151       |
| client_id                 | int           | YES        |            |           |               | 0%      |        211 | 1000002    | 7036712      |
| contract_number           | int           | YES        |            |           |               | 0%      |       3035 | 326291     | 3000530      |
| item_number               | varchar(31)   | YES        |            |           |               | 0%      |        350 | —          | —            |
| quantity                  | numeric(19,5) | YES        |            |           |               | 0%      |         21 | 0.00000    | 200000.00000 |
| currency                  | varchar(15)   | YES        |            |           |               | 0%      |          4 | —          | —            |
| contract_type             | varchar(11)   | YES        |            |           |               | 0%      |         60 | —          | —            |
| mrc                       | numeric(38,6) | YES        |            |           |               | 0%      |       1716 | 0.000000   | 29532.000000 |
| cad_mrc                   | numeric(38,6) | YES        |            |           |               | 0%      |      20114 | 0.000000   | 50908.298173 |
| archive_date              | date          | YES        |            |           |               | 0%      |         48 | 2022-03-31 | 2026-02-28   |
| cad_budget_mrc            | numeric(38,4) | YES        |            |           |               | 0%      |       1951 | 0.0000     | 48727.8000   |
| usd_mrc                   | numeric(38,4) | YES        |            |           |               | 0%      |      18798 | 0.0000     | 38938.6390   |
| datacenter_code           | nvarchar(15)  | YES        |            |           |               | 8%      |         12 | —          | —            |
| datacenter_name           | nvarchar(100) | YES        |            |           |               | 8%      |         12 | —          | —            |
| datacenter_city           | nvarchar(100) | YES        |            |           |               | 8%      |         11 | —          | —            |
| service_id                | nvarchar(255) | YES        |            |           |               | 0%      |       1317 | —          | —            |
| adjusted_line_of_business | nvarchar(255) | YES        |            |           |               | 0%      |          1 | —          | —            |

---

### dbo.order_notes_sharepoint_raw {#dbo-order-notes-sharepoint-raw}

| Property | Value |
|---|---|
| Full name | `[dbo].[order_notes_sharepoint_raw]` |
| Row count | 0 |
| Total size | 0.1 MB |
| Used size | 0.1 MB |
| Created | 2022-05-18 13:53 |
| Schema modified | 2022-05-18 13:53 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                     | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max   |
|----------------------------|----------------|------------|------------|-----------|---------------|---------|------------|-------|-------|
| sharepoint_id              | int            | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| order_id                   | int            | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| company_name               | nvarchar(255)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| customer_tier              | nvarchar(255)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| line_of_business           | nvarchar(255)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| datacenter_code            | nvarchar(255)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| usd_extended_mrc           | numeric(24,5)  | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| sla_days                   | int            | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| approval_date              | datetime2      | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| revised_due_date           | datetime2      | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| current_owner              | nvarchar(255)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| order_status               | nvarchar(255)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| order_provisioning_actions | nvarchar(4000) | YES        |            |           |               | 0%      |          0 | —     | —     |
| order_source               | nvarchar(255)  | YES        |            |           |               | 0%      |          0 | —     | —     |

---

### dbo.PopularSalesInventoryTrend {#dbo-popularsalesinventorytrend}

| Property | Value |
|---|---|
| Full name | `[dbo].[PopularSalesInventoryTrend]` |
| Row count | 5,693,844 |
| Total size | 1.8 GB |
| Used size | 1.8 GB |
| Created | 2016-11-07 14:51 |
| Schema modified | 2016-11-07 14:51 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column           | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| item_number      | nvarchar(31)  | YES        |            |           |               | 0%      |        817 | —                   | —                   |
| item_description | nvarchar(101) | YES        |            |           |               | 0%      |        813 | —                   | —                   |
| datacenter_code  | nvarchar(15)  | YES        |            |           |               | 0%      |         17 | —                   | —                   |
| city             | nvarchar(MAX) | YES        |            |           |               | 0%      |         17 | —                   | —                   |
| quantity_on_hand | numeric(38,5) | YES        |            |           |               | 0%      |        518 | -100.00000          | 2760.00000          |
| archive_date     | datetime2     | NO         |            |           |               | 0%      |       3391 | 2016-11-06 00:00:00 | 2026-03-05 00:00:00 |

---

### dbo.product_special_attributes {#dbo-product-special-attributes}

| Property | Value |
|---|---|
| Full name | `[dbo].[product_special_attributes]` |
| Row count | 279 |
| Total size | 0.1 MB |
| Used size | 0.0 MB |
| Created | 2019-06-10 10:53 |
| Schema modified | 2019-06-10 10:53 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column          | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max   |
|-----------------|---------------|------------|------------|-----------|---------------|---------|------------|-------|-------|
| integer_key     | int           | NO         | ✓          |           |               | 0%      |        279 | 1     | 279   |
| fusion_id       | int           | YES        |            |           |               | 0%      |         93 | 1926  | 4335  |
| level           | nvarchar(50)  | YES        |            |           |               | 0%      |          1 | —     | —     |
| attribute_name  | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —     | —     |
| attribute_value | nvarchar(255) | YES        |            |           |               | 0%      |         86 | —     | —     |

---

### dbo.run_rate_by_customer {#dbo-run-rate-by-customer}

| Property | Value |
|---|---|
| Full name | `[dbo].[run_rate_by_customer]` |
| Row count | 249,830 |
| Total size | 90.7 MB |
| Used size | 90.7 MB |
| Created | 2018-03-13 15:48 |
| Schema modified | 2019-08-08 11:26 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                    | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min          | Max          |
|---------------------------|---------------|------------|------------|-----------|---------------|---------|------------|--------------|--------------|
| data_source               | nvarchar(255) | YES        |            |           |               | 0%      |         10 | —            | —            |
| kpi_type                  | nvarchar(255) | YES        |            |           |               | 0%      |          4 | —            | —            |
| change_type               | nvarchar(255) | YES        |            |           |               | 88%     |         19 | —            | —            |
| archive_date              | nvarchar(255) | YES        |            |           |               | 0%      |         53 | —            | —            |
| client_id                 | nvarchar(255) | YES        |            |           |               | 18%     |       6482 | —            | —            |
| company_name              | nvarchar(255) | YES        |            |           |               | 0%      |       6964 | —            | —            |
| line_of_business          | nvarchar(255) | YES        |            |           |               | 0%      |         10 | —            | —            |
| region                    | nvarchar(255) | YES        |            |           |               | 48%     |          7 | —            | —            |
| datacenter_name           | nvarchar(255) | YES        |            |           |               | 9%      |         44 | —            | —            |
| currency                  | nvarchar(255) | YES        |            |           |               | 0%      |          4 | —            | —            |
| is_french_entity          | nvarchar(255) | YES        |            |           |               | 51%     |          2 | —            | —            |
| mrc                       | numeric(38,4) | YES        |            |           |               | 0%      |      32176 | -649724.6900 | 1648670.1800 |
| cad_budget_mrc            | numeric(38,4) | YES        |            |           |               | 0%      |      35615 | -864133.8377 | 1913962.9670 |
| adjusted_line_of_business | nvarchar(255) | YES        |            |           |               | 0%      |          6 | —            | —            |
| datacenter_city           | nvarchar(255) | YES        |            |           |               | 0%      |         23 | —            | —            |
| Revenue Entity            | nvarchar(255) | YES        |            |           |               | 0%      |          5 | —            | —            |
| Sales Region              | nvarchar(255) | YES        |            |           |               | 2%      |          4 | —            | —            |
| Sales Rep                 | nvarchar(255) | YES        |            |           |               | 2%      |        149 | —            | —            |
| Sales Director            | nvarchar(255) | YES        |            |           |               | 2%      |         29 | —            | —            |
| business_unit             | nvarchar(255) | YES        |            |           |               | 48%     |          5 | —            | —            |

---

### dbo.Sales {#dbo-sales}

| Property | Value |
|---|---|
| Full name | `[dbo].[Sales]` |
| Row count | 11,073 |
| Total size | 8.2 MB |
| Used size | 7.4 MB |
| Created | 2015-12-09 13:47 |
| Schema modified | 2020-04-17 19:00 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                          | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|---------------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| integer_key                     | int           | NO         |            |           |               | 0%      |      11073 | 180815                     | 191891                     |
| company_name                    | nvarchar(255) | YES        |            |           |               | 0%      |        748 | —                          | —                          |
| service_id                      | int           | YES        |            |           |               | 0%      |       5582 | 2356417                    | 7981411                    |
| product                         | nvarchar(255) | YES        |            |           |               | 0%      |        737 | —                          | —                          |
| order_id                        | int           | YES        |            |           |               | 0%      |       4306 | 245953                     | 279878                     |
| order_type                      | nvarchar(255) | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| order_date                      | datetime2     | YES        |            |           |               | 0%      |       4247 | 2021-05-20 12:53:36.164598 | 2026-02-27 10:10:27.319228 |
| approval_date                   | datetime      | YES        |            |           |               | 0%      |       4306 | 2022-03-01 03:49:56.537000 | 2026-02-27 14:58:04.340000 |
| mrc                             | numeric(38,2) | YES        |            |           |               | 0%      |       2021 | -27048.00                  | 29532.00                   |
| line_of_business                | nvarchar(255) | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| new_existing_customer           | nvarchar(50)  | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| sales_rep                       | nvarchar(255) | YES        |            |           |               | 0%      |         47 | —                          | —                          |
| migrated_service_id             | int           | YES        |            |           |               | 81%     |       1094 | 0                          | 7963429                    |
| migrated_service_provision_date | datetime2     | YES        |            |           |               | 90%     |        555 | 2008-02-21 17:20:00        | 2025-10-28 12:00:29.992922 |
| promotion                       | nvarchar(255) | YES        |            |           |               | 100%    |          3 | —                          | —                          |
| month                           | datetime2     | YES        |            |           |               | 0%      |         49 | 2022-03-31 08:31:06.520000 | 2026-02-28 08:31:01.513333 |
| is_emea                         | nvarchar(3)   | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| currency                        | nvarchar(3)   | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| usd_mrc                         | numeric(38,2) | YES        |            |           |               | 0%      |       2887 | -34228.36                  | 37371.78                   |
| usd_quota_mrc                   | numeric(38,2) | YES        |            |           |               | 0%      |       2828 | -34228.36                  | 37371.78                   |
| usd_nrc                         | numeric(38,2) | YES        |            |           |               | 0%      |        732 | 0.00                       | 390063.71                  |
| datacenter_name                 | nvarchar(255) | YES        |            |           |               | 0%      |         22 | —                          | —                          |
| sales_rep_lob                   | nvarchar(255) | YES        |            |           |               | 0%      |          5 | —                          | —                          |
| service_type                    | nvarchar(64)  | YES        |            |           |               | 0%      |         15 | —                          | —                          |
| contract_length                 | int           | YES        |            |           |               | 0%      |         44 | 1                          | 60                         |
| gbp_mrc                         | numeric(38,2) | YES        |            |           |               | 0%      |       3242 | -27048.00                  | 29532.00                   |
| gbp_nrc                         | numeric(38,2) | YES        |            |           |               | 0%      |        881 | 0.00                       | 297783.71                  |
| short_term                      | int           | YES        |            |           |               | 100%    |          2 | 1                          | 3                          |
| client_id                       | int           | YES        |            |           |               | 0%      |        722 | 1000002                    | 7036717                    |
| cad_mrc                         | numeric(38,2) | YES        |            |           |               | 0%      |       3399 | -45296.10                  | 49455.95                   |
| cad_nrc                         | numeric(38,2) | YES        |            |           |               | 0%      |        893 | 0.00                       | 546988.00                  |
| cad_quota_mrc                   | numeric(38,2) | YES        |            |           |               | 0%      |       3396 | -45296.10                  | 49455.95                   |
| cad_budget_mrc                  | numeric(38,4) | YES        |            |           |               | 0%      |       2331 | -44629.2000                | 48727.8000                 |
| usd_TCV                         | numeric(38,4) | YES        |            |           |               | 0%      |       3759 | -410740.3144               | 448461.3636                |
| gbp_TCV                         | numeric(38,4) | YES        |            |           |               | 0%      |       4347 | -324576.0000               | 354384.0000                |
| cad_TCV                         | numeric(38,4) | YES        |            |           |               | 0%      |       4476 | -543553.2432               | 593471.3982                |
| eur_TCV                         | numeric(38,4) | YES        |            |           |               | 0%      |       4673 | -376892.9773               | 411505.5977                |
| migration_full_order_mrc        | numeric(38,4) | YES        |            |           |               | 90%     |        586 | 0.0000                     | 7600.0000                  |
| adjusted_line_of_business       | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |

#### Indexes

| Name                        | Type      | Unique   | PK   | Columns     |
|-----------------------------|-----------|----------|------|-------------|
| PK__Sales__93BEB6170CBAE877 | CLUSTERED | YES      | ✓    | integer_key |

---

### dbo.sales_month_to_date {#dbo-sales-month-to-date}

| Property | Value |
|---|---|
| Full name | `[dbo].[sales_month_to_date]` |
| Row count | 64 |
| Total size | 0.1 MB |
| Used size | 0.1 MB |
| Created | 2015-03-19 15:03 |
| Schema modified | 2020-06-19 12:35 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                          | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|---------------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| integer_key                     | int           | NO         |            |           |               | 0%      |         64 | 1                          | 64                         |
| company_name                    | nvarchar(255) | YES        |            |           |               | 0%      |         13 | —                          | —                          |
| service_id                      | int           | YES        |            |           |               | 0%      |         46 | 5328819                    | 7981454                    |
| product                         | nvarchar(255) | YES        |            |           |               | 0%      |         21 | —                          | —                          |
| order_id                        | int           | YES        |            |           |               | 0%      |         17 | 278798                     | 279918                     |
| order_type                      | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| order_date                      | datetime2     | YES        |            |           |               | 0%      |         17 | 2025-09-11 10:50:47.578267 | 2026-03-06 15:10:41.493269 |
| approval_date                   | datetime      | YES        |            |           |               | 0%      |         17 | 2026-03-02 00:15:56.050000 | 2026-03-06 17:54:04.927000 |
| mrc                             | numeric(38,2) | YES        |            |           |               | 0%      |         19 | -201.60                    | 5600.00                    |
| nrc                             | numeric(38,2) | YES        |            |           |               | 0%      |          8 | 0.00                       | 24660.00                   |
| line_of_business                | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| new_existing_customer           | nvarchar(50)  | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| sales_rep                       | nvarchar(255) | YES        |            |           |               | 0%      |          9 | —                          | —                          |
| sales_rep_role                  | nvarchar(15)  | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| sales_rep_region                | nvarchar(15)  | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| migrated_service_id             | int           | YES        |            |           |               | 91%     |          6 | 6096494                    | 7249930                    |
| migrated_service_provision_date | datetime2     | YES        |            |           |               | 91%     |          3 | 2019-04-11 15:34:18.336391 | 2021-09-14 21:52:04.806944 |
| promotion                       | nvarchar(255) | YES        |            |           |               | 97%     |          1 | —                          | —                          |
| is_emea                         | nvarchar(3)   | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| currency                        | nvarchar(3)   | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| usd_mrc                         | numeric(38,2) | YES        |            |           |               | 0%      |         20 | -147.06                    | 4084.89                    |
| exchange_rate                   | numeric(38,7) | YES        |            |           |               | 100%    |          0 | NULL                       | NULL                       |
| usd_nrc                         | numeric(38,2) | YES        |            |           |               | 0%      |          8 | 0.00                       | 17988.12                   |
| datacenter_name                 | nvarchar(255) | YES        |            |           |               | 0%      |          8 | —                          | —                          |
| sales_rep_lob                   | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| service_type                    | nvarchar(64)  | YES        |            |           |               | 0%      |          9 | —                          | —                          |
| contract_length                 | int           | YES        |            |           |               | 0%      |          6 | 1                          | 37                         |
| gbp_mrc                         | numeric(38,2) | YES        |            |           |               | 0%      |         20 | -108.74                    | 3020.46                    |
| gbp_nrc                         | numeric(38,2) | YES        |            |           |               | 0%      |          8 | 0.00                       | 13300.80                   |
| short_term                      | int           | YES        |            |           |               | 100%    |          0 | NULL                       | NULL                       |
| client_id                       | int           | YES        |            |           |               | 0%      |         13 | 1000669                    | 7036720                    |
| cad_mrc                         | numeric(38,2) | YES        |            |           |               | 0%      |         20 | -201.60                    | 5600.00                    |
| cad_nrc                         | numeric(38,2) | YES        |            |           |               | 0%      |          8 | 0.00                       | 24660.00                   |
| cad_budget_mrc                  | numeric(38,4) | YES        |            |           |               | 0%      |         20 | -201.6020                  | 5600.0000                  |
| last_updated                    | datetime2     | YES        |            |           |               | 0%      |          1 | 2026-03-07 06:42:42.820000 | 2026-03-07 06:42:42.820000 |
| adjusted_line_of_business       | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| migration_full_order_mrc        | numeric(38,4) | YES        |            |           |               | 91%     |          3 | 0.0000                     | 3096.0000                  |

#### Indexes

| Name                           | Type      | Unique   | PK   | Columns     |
|--------------------------------|-----------|----------|------|-------------|
| PK__sales_mo__93BEB61747DBAE45 | CLUSTERED | YES      | ✓    | integer_key |

---

### dbo.sales_salestracker {#dbo-sales-salestracker}

| Property | Value |
|---|---|
| Full name | `[dbo].[sales_salestracker]` |
| Row count | 34,318 |
| Total size | 54.2 MB |
| Used size | 53.0 MB |
| Created | 2017-12-13 10:36 |
| Schema modified | 2020-04-17 10:45 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                                           | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|--------------------------------------------------|----------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| integer_key                                      | int            | NO         |            |           |               | 0%      |      34318 | 1                          | 69344                      |
| company_name                                     | nvarchar(255)  | YES        |            |           |               | 0%      |       3822 | —                          | —                          |
| service_id                                       | nvarchar(255)  | YES        |            |           |               | 5%      |      17913 | —                          | —                          |
| product                                          | nvarchar(255)  | YES        |            |           |               | 1%      |       1604 | —                          | —                          |
| order_id                                         | nvarchar(255)  | YES        |            |           |               | 6%      |       9924 | —                          | —                          |
| order_type                                       | nvarchar(255)  | YES        |            |           |               | 0%      |         29 | —                          | —                          |
| approval_date                                    | datetime       | YES        |            |           |               | 0%      |       8661 | 2017-01-19 00:00:00        | 2019-10-19 00:00:00        |
| mrc                                              | numeric(38,2)  | YES        |            |           |               | 0%      |       3823 | -10219.00                  | 500000.00                  |
| nrc                                              | numeric(38,2)  | YES        |            |           |               | 9%      |        491 | -500.00                    | 2473954.00                 |
| line_of_business                                 | nvarchar(255)  | YES        |            |           |               | 0%      |         18 | —                          | —                          |
| new_existing_customer                            | nvarchar(50)   | YES        |            |           |               | 0%      |          5 | —                          | —                          |
| sales_rep                                        | nvarchar(255)  | YES        |            |           |               | 0%      |        119 | —                          | —                          |
| sales_rep_role                                   | nvarchar(15)   | YES        |            |           |               | 39%     |         12 | —                          | —                          |
| sales_rep_region                                 | nvarchar(15)   | YES        |            |           |               | 17%     |          3 | —                          | —                          |
| migrated_service_id                              | nvarchar(255)  | YES        |            |           |               | 83%     |        439 | —                          | —                          |
| migrated_service_provision_date                  | datetime2      | YES        |            |           |               | 84%     |       1026 | 2005-03-03 12:40:13        | 9999-01-01 00:00:00        |
| promotion                                        | nvarchar(255)  | YES        |            |           |               | 100%    |          9 | —                          | —                          |
| currency                                         | nvarchar(3)    | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| service_type                                     | nvarchar(64)   | YES        |            |           |               | 16%     |         70 | —                          | —                          |
| contract_length                                  | int            | YES        |            |           |               | 7%      |         62 | 0                          | 120                        |
| short_term                                       | int            | YES        |            |           |               | 86%     |          4 | 0                          | 3                          |
| client_id                                        | nvarchar(255)  | YES        |            |           |               | 2%      |       3467 | —                          | —                          |
| source_system                                    | nvarchar(255)  | YES        |            |           |               | 0%      |          1 | —                          | —                          |
| data_source                                      | nvarchar(255)  | YES        |            |           |               | 0%      |          9 | —                          | —                          |
| sales_region                                     | nvarchar(255)  | YES        |            |           |               | 0%      |          5 | —                          | —                          |
| reported_quarter                                 | nvarchar(255)  | YES        |            |           |               | 39%     |          4 | —                          | —                          |
| class                                            | nvarchar(255)  | YES        |            |           |               | 15%     |          4 | —                          | —                          |
| reported_month                                   | datetime2      | YES        |            |           |               | 0%      |         24 | 2017-09-01 00:00:00        | 2019-08-01 00:00:00        |
| order_completed                                  | datetime2      | YES        |            |           |               | 44%     |       6459 | 2017-01-30 00:00:00        | 2019-09-01 06:40:04        |
| sales_pod                                        | nvarchar(255)  | YES        |            |           |               | 28%     |         16 | —                          | —                          |
| sales_manager                                    | nvarchar(255)  | YES        |            |           |               | 6%      |         19 | —                          | —                          |
| sales_director                                   | nvarchar(255)  | YES        |            |           |               | 2%      |         20 | —                          | —                          |
| sales_general_manager                            | nvarchar(255)  | YES        |            |           |               | 17%     |          7 | —                          | —                          |
| datacenter_city                                  | nvarchar(255)  | YES        |            |           |               | 1%      |       1737 | —                          | —                          |
| cancel_reason                                    | nvarchar(4000) | YES        |            |           |               | 79%     |         20 | —                          | —                          |
| original_mrc                                     | numeric(38,4)  | YES        |            |           |               | 22%     |       2634 | -10219.0000                | 43000.0000                 |
| original_new_mrc                                 | numeric(38,4)  | YES        |            |           |               | 9%      |       2904 | -5835.2000                 | 150000.0000                |
| existing_mrc                                     | nvarchar(255)  | YES        |            |           |               | 39%     |        843 | —                          | —                          |
| cost_mrc                                         | nvarchar(255)  | YES        |            |           |               | 99%     |        131 | —                          | —                          |
| cost_nrc                                         | nvarchar(255)  | YES        |            |           |               | 100%    |         79 | —                          | —                          |
| new_tcv                                          | numeric(38,4)  | YES        |            |           |               | 0%      |       7448 | -182230.7864               | 5400000.0000               |
| existing_order_id                                | nvarchar(255)  | YES        |            |           |               | 39%     |       1065 | —                          | —                          |
| existing_end_date                                | datetime2      | YES        |            |           |               | 77%     |       3419 | 1900-01-29 00:00:00        | 2025-03-19 00:00:00        |
| existing_contract_remaining_term                 | nvarchar(255)  | YES        |            |           |               | 0%      |       2320 | —                          | —                          |
| existing_3rd_party_mrc                           | nvarchar(255)  | YES        |            |           |               | 100%    |         36 | —                          | —                          |
| existing_contract_remaining_total_contract_value | numeric(38,4)  | YES        |            |           |               | 0%      |        806 | -7280.0000                 | 630345.3947                |
| total_contract_value                             | numeric(38,4)  | YES        |            |           |               | 0%      |       8092 | -182230.7864               | 5400000.0000               |
| change_in_mrc                                    | numeric(38,4)  | YES        |            |           |               | 0%      |       4135 | -216475.0000               | 500000.0000                |
| run_rate_type                                    | nvarchar(255)  | YES        |            |           |               | 39%     |          8 | —                          | —                          |
| notes                                            | nvarchar(4000) | YES        |            |           |               | 97%     |        187 | —                          | —                          |
| net_new_mrc_cad                                  | numeric(38,4)  | YES        |            |           |               | 0%      |       4682 | -13591.2700                | 500000.0000                |
| net_new_mrc_usd                                  | numeric(38,4)  | YES        |            |           |               | 0%      |       4685 | -10219.0000                | 375939.8496                |
| net_new_mrc_gbp                                  | numeric(38,4)  | YES        |            |           |               | 0%      |       4897 | -8237.1333                 | 303030.3030                |
| net_new_mrc_eur                                  | numeric(38,4)  | YES        |            |           |               | 0%      |       4925 | -9373.2896                 | 344827.5862                |
| tcv_cad                                          | numeric(38,4)  | YES        |            |           |               | 0%      |       9174 | -182230.7864               | 6804000.0000               |
| tcv_usd                                          | numeric(38,4)  | YES        |            |           |               | 0%      |       9294 | -137015.6289               | 5400000.0000               |
| tcv_gbp                                          | numeric(38,4)  | YES        |            |           |               | 0%      |       9464 | -110442.9008               | 4002352.9411               |
| tcv_eur                                          | numeric(38,4)  | YES        |            |           |               | 0%      |       9504 | -125676.4044               | 4536000.0000               |
| quota_mrc_cad                                    | numeric(38,4)  | YES        |            |           |               | 0%      |       5892 | -13417.5469                | 500000.0000                |
| quota_mrc_usd                                    | numeric(38,4)  | YES        |            |           |               | 0%      |       5725 | -10219.0000                | 152557.6030                |
| quota_mrc_gbp                                    | numeric(38,4)  | YES        |            |           |               | 0%      |       6638 | -7759.3956                 | 110351.1835                |
| quota_mrc_eur                                    | numeric(38,4)  | YES        |            |           |               | 0%      |       6845 | -8742.7816                 | 125013.7377                |
| quota_tcv_cad                                    | numeric(38,4)  | YES        |            |           |               | 0%      |      10367 | -182230.7864               | 2878200.0000               |
| quota_tcv_usd                                    | numeric(38,4)  | YES        |            |           |               | 0%      |      10272 | -138800.2029               | 2316085.9419               |
| quota_tcv_gbp                                    | numeric(38,4)  | YES        |            |           |               | 0%      |      10889 | -104472.1587               | 2473954.0000               |
| quota_tcv_eur                                    | numeric(38,4)  | YES        |            |           |               | 0%      |      11287 | -118879.7615               | 1897922.8486               |
| lead_development_rep                             | nvarchar(255)  | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| channel_rep                                      | nvarchar(255)  | YES        |            |           |               | 100%    |          0 | —                          | —                          |
| channel_split_sales_rep                          | nvarchar(255)  | YES        |            |           |               | 100%    |          3 | —                          | —                          |
| channel_split_channel_rep                        | nvarchar(255)  | YES        |            |           |               | 100%    |          3 | —                          | —                          |
| channel_split_total                              | nvarchar(255)  | YES        |            |           |               | 91%     |          3 | —                          | —                          |
| billing_platform                                 | nvarchar(255)  | YES        |            |           |               | 0%      |          7 | —                          | —                          |
| expected_provision_date_lookup                   | nvarchar(255)  | YES        |            |           |               | 55%     |         85 | —                          | —                          |
| expected_provision_date                          | nvarchar(255)  | YES        |            |           |               | 91%     |         63 | —                          | —                          |
| expected_provision_month                         | nvarchar(255)  | YES        |            |           |               | 51%     |         15 | —                          | —                          |
| completed_month                                  | datetime2      | YES        |            |           |               | 61%     |         12 | 2017-01-01 00:00:00        | 2018-10-01 00:00:00        |
| completion_lookup                                | nvarchar(255)  | YES        |            |           |               | 71%     |       2434 | —                          | —                          |
| billing_start_date                               | nvarchar(255)  | YES        |            |           |               | 97%     |        150 | —                          | —                          |
| first_invoice_number                             | nvarchar(255)  | YES        |            |           |               | 98%     |        358 | —                          | —                          |
| contract_length_from                             | nvarchar(255)  | YES        |            |           |               | 83%     |         16 | —                          | —                          |
| contract_start_date                              | datetime2      | YES        |            |           |               | 41%     |       8905 | 2001-07-19 00:00:00        | 2019-08-29 00:00:00        |
| Contract_term                                    | numeric(38,4)  | YES        |            |           |               | 0%      |       1919 | 0.0000                     | 240.0000                   |
| total_new_mrc                                    | numeric(38,4)  | YES        |            |           |               | 39%     |       2091 | -5600.0000                 | 500000.0000                |
| expedite_fee_etf                                 | nvarchar(255)  | YES        |            |           |               | 100%    |         10 | —                          | —                          |
| cloud_activation                                 | nvarchar(255)  | YES        |            |           |               | 100%    |          1 | —                          | —                          |
| 3rd_party_vendor_cost_type                       | nvarchar(255)  | YES        |            |           |               | 99%     |         36 | —                          | —                          |
| cost_term                                        | nvarchar(255)  | YES        |            |           |               | 99%     |         29 | —                          | —                          |
| last_updated                                     | datetime2      | YES        |            |           |               | 0%      |         19 | 2018-03-23 13:03:39.690000 | 2019-09-13 13:26:35.377000 |
| datacenter_code                                  | nvarchar(255)  | YES        |            |           |               | 63%     |         21 | —                          | —                          |
| cad_budget_mrc                                   | numeric(38,4)  | YES        |            |           |               | 0%      |       4336 | -12875.9400                | 500000.0000                |
| usd_budget_mrc                                   | numeric(38,4)  | YES        |            |           |               | 0%      |       4674 | -10219.0000                | 375939.8496                |
| gbp_budget_mrc                                   | numeric(38,4)  | YES        |            |           |               | 0%      |       4670 | -8237.1333                 | 303030.3030                |
| eur_budget_mrc                                   | numeric(38,4)  | YES        |            |           |               | 0%      |       4661 | -9373.2896                 | 344827.5862                |
| cad_budget_nrc                                   | numeric(38,4)  | YES        |            |           |               | 24%     |        552 | -500.0000                  | 73875.1860                 |
| usd_budget_nrc                                   | numeric(38,4)  | YES        |            |           |               | 24%     |        552 | -375.9398                  | 55545.2526                 |
| gbp_budget_nrc                                   | numeric(38,4)  | YES        |            |           |               | 24%     |        552 | -303.0303                  | 44772.8400                 |
| eur_budget_nrc                                   | numeric(38,4)  | YES        |            |           |               | 24%     |        552 | -344.8275                  | 50948.4041                 |
| cad_budget_tcv                                   | numeric(38,4)  | YES        |            |           |               | 0%      |       9115 | -182230.7864               | 6804000.0000               |
| usd_budget_tcv                                   | numeric(38,4)  | YES        |            |           |               | 0%      |       9067 | -137015.6288               | 5115789.4736               |
| gbp_budget_tcv                                   | numeric(38,4)  | YES        |            |           |               | 0%      |       9041 | -110442.9008               | 4123636.3636               |
| eur_budget_tcv                                   | numeric(38,4)  | YES        |            |           |               | 0%      |       9039 | -125676.4044               | 4692413.7931               |
| business_unit                                    | nvarchar(255)  | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| adjusted_line_of_business                        | nvarchar(255)  | YES        |            |           |               | 0%      |          5 | —                          | —                          |

---

### dbo.SalesBookOfBusiness {#dbo-salesbookofbusiness}

| Property | Value |
|---|---|
| Full name | `[dbo].[SalesBookOfBusiness]` |
| Row count | 13,245 |
| Total size | 2.3 MB |
| Used size | 2.2 MB |
| Created | 2025-11-15 10:18 |
| Schema modified | 2025-11-15 10:20 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                    | Type         | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|---------------------------|--------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| client_id                 | int          | YES        |            |           |               | 0%      |        809 | 1000002             | 42050550            |
| company_name              | varchar(255) | YES        |            |           |               | 0%      |        803 | —                   | —                   |
| service_id                | int          | YES        |            |           |               | 0%      |       4624 | 0                   | 47367363            |
| product                   | varchar(255) | YES        |            |           |               | 0%      |        223 | —                   | —                   |
| service_status            | varchar(255) | YES        |            |           |               | 0%      |          8 | —                   | —                   |
| provision_date            | datetime     | YES        |            |           |               | 0%      |       7712 | 2005-06-03 00:00:00 | 2025-11-27 00:00:00 |
| service_type              | varchar(255) | YES        |            |           |               | 0%      |         18 | —                   | —                   |
| currency                  | varchar(255) | YES        |            |           |               | 0%      |          8 | —                   | —                   |
| mrc                       | money        | YES        |            |           |               | 0%      |       3544 | -314.6100           | 126423.9300         |
| cad_budget_mrc            | money        | YES        |            |           |               | 0%      |       3984 | -418.4313           | 169848.1554         |
| adjusted_line_of_business | varchar(255) | YES        |            |           |               | 0%      |          3 | —                   | —                   |
| account_manager           | varchar(255) | YES        |            |           |               | 0%      |          8 | —                   | —                   |
| archive_date              | datetime     | YES        |            |           |               | 0%      |          3 | 2025-09-30 00:00:00 | 2025-11-30 00:00:00 |
| weight                    | float(53)    | YES        |            |           |               | 0%      |          3 | 0.6                 | 1.0                 |
| weight_cad                | money        | YES        |            |           |               | 0%      |       4059 | -251.0588           | 101908.8932         |

---

### dbo.salesforce_open_opportunities_trend {#dbo-salesforce-open-opportunities-trend}

| Property | Value |
|---|---|
| Full name | `[dbo].[salesforce_open_opportunities_trend]` |
| Row count | 5,495,524 |
| Total size | 2.3 GB |
| Used size | 2.3 GB |
| Created | 2019-11-27 09:45 |
| Schema modified | 2022-04-22 19:59 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                   | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|--------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| opportunity_id           | nchar(18)     | NO         |            |           |               | 0%      |      19459 | —                          | —                          |
| stage_name               | nvarchar(40)  | NO         |            |           |               | 0%      |         17 | —                          | —                          |
| opportunity_close_date   | datetime2     | NO         |            |           |               | 0%      |       2197 | 1900-01-01 00:00:00        | 2030-12-31 00:00:00        |
| opportunity_owner_id     | nchar(18)     | NO         |            |           |               | 0%      |        178 | —                          | —                          |
| mrc                      | numeric(18,2) | YES        |            |           |               | 6%      |       5519 | -61727.00                  | 1000000.00                 |
| currency                 | nvarchar(3)   | NO         |            |           |               | 0%      |          4 | —                          | —                          |
| salesforce_account_id    | nchar(18)     | YES        |            |           |               | 0%      |       5002 | —                          | —                          |
| opportunity_created_date | datetime2     | NO         |            |           |               | 0%      |      18863 | 2014-04-14 10:09:31        | 2026-03-06 13:57:37        |
| current_probability      | numeric(18,0) | YES        |            |           |               | 0%      |         12 | 0                          | 100                        |
| opportunity_name         | nvarchar(120) | NO         |            |           |               | 0%      |      23597 | —                          | —                          |
| forecast_category        | nvarchar(40)  | NO         |            |           |               | 0%      |          6 | —                          | —                          |
| forecast_category_name   | nvarchar(40)  | NO         |            |           |               | 0%      |          7 | —                          | —                          |
| deleted_opportunity      | varchar(5)    | NO         |            |           |               | 0%      |          3 | —                          | —                          |
| opportunity_number       | nvarchar(30)  | YES        |            |           |               | 0%      |      19459 | —                          | —                          |
| probability              | numeric(18,0) | NO         |            |           |               | 0%      |         12 | 0                          | 100                        |
| opportunity_type         | nvarchar(40)  | YES        |            |           |               | 1%      |          9 | —                          | —                          |
| last_modified_date       | datetime2     | NO         |            |           |               | 0%      |     109243 | 2016-07-07 11:21:24        | 2026-03-06 17:06:21        |
| archive_date             | datetime      | NO         |            |           |               | 0%      |       4948 | 2019-11-26 09:36:41.857000 | 2026-03-07 06:30:01.320000 |
| nrc                      | numeric(18,2) | YES        |            |           |               | 2%      |        690 | -66.08                     | 12000000.00                |
| push_count               | numeric(18,0) | YES        |            |           |               | 68%     |         34 | 1                          | 34                         |

---

### dbo.salesforce_opportunity_trend {#dbo-salesforce-opportunity-trend}

| Property | Value |
|---|---|
| Full name | `[dbo].[salesforce_opportunity_trend]` |
| Row count | 13,427,219 |
| Total size | 12.7 GB |
| Used size | 12.7 GB |
| Created | 2017-06-29 21:04 |
| Schema modified | 2020-05-14 16:59 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                             | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|------------------------------------|----------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| integer_key                        | int            | NO         |            |           |               | 0%      |   13427219 | 1                   | 13521872            |
| account_country                    | nvarchar(4000) | YES        |            |           |               | 8%      |        333 | —                   | —                   |
| account_state                      | nvarchar(4000) | YES        |            |           |               | 24%     |       2577 | —                   | —                   |
| account_id                         | nvarchar(255)  | YES        |            |           |               | 0%      |      53493 | —                   | —                   |
| account_active                     | nvarchar(255)  | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| active_mrc                         | numeric(38,4)  | YES        |            |           |               | 0%      |       5058 | -61727.0000         | 600000.0000         |
| amount                             | numeric(38,4)  | YES        |            |           |               | 2%      |      22655 | -61727.0000         | 3000000.0000        |
| closed_won_mrc                     | numeric(38,4)  | YES        |            |           |               | 0%      |      17639 | -9507.0000          | 1781901.0000        |
| close_date                         | datetime2      | NO         |            |           |               | 0%      |       6866 | 1900-01-01 00:00:00 | 2042-04-30 00:00:00 |
| cp1_division                       | nvarchar(4000) | YES        |            |           |               | 71%     |          5 | —                   | —                   |
| cp1_renewal_amount_report_value    | numeric(38,4)  | YES        |            |           |               | 0%      |       4881 | -15619.0500         | 964879.1600         |
| cp1_renewal_delta                  | numeric(38,4)  | YES        |            |           |               | 0%      |       4079 | -1127147.3500       | 1478213.0000        |
| created_date_date_only             | datetime2      | YES        |            |           |               | 0%      |       6198 | 2005-01-04 00:00:00 | 2026-02-27 00:00:00 |
| created_date_time                  | nvarchar(4000) | YES        |            |           |               | 0%      |     139571 | —                   | —                   |
| created_date                       | datetime2      | NO         |            |           |               | 0%      |     139572 | 2005-01-04 03:33:00 | 2026-02-27 16:57:50 |
| currency_iso_code                  | nvarchar(3)    | NO         |            |           |               | 0%      |          4 | —                   | —                   |
| current_close_date                 | datetime2      | YES        |            |           |               | 0%      |       6866 | 1900-01-01 00:00:00 | 2042-04-30 00:00:00 |
| current_possibility                | numeric(38,4)  | YES        |            |           |               | 0%      |         18 | 0.0000              | 100.0000            |
| current_stage                      | nvarchar(4000) | YES        |            |           |               | 0%      |         21 | —                   | —                   |
| customer_type                      | nvarchar(255)  | YES        |            |           |               | 92%     |          7 | —                   | —                   |
| data_quality_score                 | numeric(38,4)  | YES        |            |           |               | 0%      |          5 | 20.0000             | 100.0000            |
| expected_revenue                   | numeric(38,4)  | YES        |            |           |               | 2%      |      21801 | -9507.0000          | 1781901.0000        |
| fiscal_quarter                     | int            | YES        |            |           |               | 0%      |          4 | 1                   | 4                   |
| fiscal_year                        | int            | YES        |            |           |               | 0%      |         29 | 1900                | 2042                |
| forecast_category                  | nvarchar(255)  | YES        |            |           |               | 0%      |          6 | —                   | —                   |
| Id                                 | nvarchar(255)  | YES        |            |           |               | 0%      |     159461 | —                   | —                   |
| is_created_from_lead               | nvarchar(255)  | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| is_closed                          | nvarchar(255)  | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| is_won                             | nvarchar(255)  | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| last_activity_date                 | datetime2      | YES        |            |           |               | 62%     |       5686 | 2006-01-03 00:00:00 | 4501-01-01 00:00:00 |
| last_modified_date                 | datetime2      | NO         |            |           |               | 0%      |     158332 | 2011-11-08 19:12:07 | 2026-02-27 16:57:50 |
| lead_type                          | nvarchar(255)  | YES        |            |           |               | 1%      |         36 | —                   | —                   |
| lead_source                        | nvarchar(255)  | YES        |            |           |               | 13%     |        234 | —                   | —                   |
| loss_reason                        | nvarchar(255)  | YES        |            |           |               | 84%     |         44 | —                   | —                   |
| loss_reason_final_customer_outcome | nvarchar(255)  | YES        |            |           |               | 88%     |          4 | —                   | —                   |
| lost                               | nvarchar(255)  | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| lost_mrc                           | numeric(38,4)  | YES        |            |           |               | 0%      |       6931 | -61727.0000         | 3000000.0000        |
| manager_forecast                   | nvarchar(255)  | YES        |            |           |               | 100%    |          5 | —                   | —                   |
| marketing_source                   | nvarchar(4000) | YES        |            |           |               | 68%     |         17 | —                   | —                   |
| MRR                                | numeric(38,4)  | YES        |            |           |               | 100%    |       1878 | -18000.0000         | 340000.0000         |
| Name                               | nvarchar(255)  | YES        |            |           |               | 0%      |     143518 | —                   | —                   |
| number_of_products                 | numeric(38,4)  | YES        |            |           |               | 0%      |         16 | 0.0000              | 20.0000             |
| open_duration                      | numeric(38,4)  | YES        |            |           |               | 0%      |       4343 | -43736.0000         | 10222.0000          |
| opportunity_number                 | nvarchar(255)  | YES        |            |           |               | 0%      |     159461 | —                   | —                   |
| owner_id                           | nvarchar(255)  | YES        |            |           |               | 0%      |        547 | —                   | —                   |
| Probability                        | numeric(38,4)  | YES        |            |           |               | 0%      |         18 | 0.0000              | 100.0000            |
| sales_geography                    | nvarchar(255)  | YES        |            |           |               | 62%     |          6 | —                   | —                   |
| stage_name                         | nvarchar(255)  | YES        |            |           |               | 0%      |         21 | —                   | —                   |
| text                               | nvarchar(4000) | YES        |            |           |               | 0%      |          7 | —                   | —                   |
| Type                               | nvarchar(255)  | YES        |            |           |               | 14%     |         18 | —                   | —                   |
| aging                              | nvarchar(4000) | YES        |            |           |               | 0%      |          4 | —                   | —                   |
| colo_location                      | nvarchar(255)  | YES        |            |           |               | 92%     |         48 | —                   | —                   |
| lead_number                        | nvarchar(255)  | YES        |            |           |               | 88%     |      24635 | —                   | —                   |
| next_step                          | nvarchar(255)  | YES        |            |           |               | 62%     |      78988 | —                   | —                   |
| owner_manager                      | nvarchar(255)  | YES        |            |           |               | 53%     |        112 | —                   | —                   |
| push_count                         | numeric(38,4)  | YES        |            |           |               | 88%     |         34 | 1.0000              | 34.0000             |
| archive_date                       | datetime2      | YES        |            |           |               | 0%      |        113 | 2016-10-31 00:00:00 | 2026-02-28 00:00:00 |
| record_type                        | nvarchar(255)  | YES        |            |           |               | 39%     |          6 | —                   | —                   |

---

### dbo.software_skus {#dbo-software-skus}

| Property | Value |
|---|---|
| Full name | `[dbo].[software_skus]` |
| Row count | 569 |
| Total size | 0.1 MB |
| Used size | 0.0 MB |
| Created | 2025-06-12 16:55 |
| Schema modified | 2025-06-12 16:55 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column      | Type        | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max   |
|-------------|-------------|------------|------------|-----------|---------------|---------|------------|-------|-------|
| componet_id | int         | NO         |            |           |               | 0%      |        568 | 60    | 6222  |
| vendor      | varchar(12) | NO         |            |           |               | 0%      |         20 | —     | —     |
| class       | varchar(14) | NO         |            |           |               | 0%      |         13 | —     | —     |

---

### dbo.tasks {#dbo-tasks}

| Property | Value |
|---|---|
| Full name | `[dbo].[tasks]` |
| Row count | 504,296 |
| Total size | 439.3 MB |
| Used size | 437.4 MB |
| Created | 2020-02-27 22:31 |
| Schema modified | 2020-02-27 22:31 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column               | Type           | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|----------------------|----------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| task_id              | int            | YES        |            |           |               | 0%      |     504296 | 102                        | 539229                     |
| created_date         | datetime2      | YES        |            |           |               | 0%      |     504246 | 2015-07-13 08:38:30.533000 | 2025-05-01 04:00:55.590000 |
| created_by           | nvarchar(255)  | YES        |            |           |               | 0%      |       4800 | —                          | —                          |
| owned_by             | nvarchar(255)  | YES        |            |           |               | 0%      |        975 | —                          | —                          |
| owned_by_team        | nvarchar(255)  | YES        |            |           |               | 0%      |        109 | —                          | —                          |
| resolved_by          | nvarchar(255)  | YES        |            |           |               | 0%      |        879 | —                          | —                          |
| closed_by            | nvarchar(255)  | YES        |            |           |               | 0%      |        883 | —                          | —                          |
| parent_ticket_id     | varchar(255)   | YES        |            |           |               | 0%      |     264915 | —                          | —                          |
| parent_ticket_type   | nvarchar(255)  | YES        |            |           |               | 10%     |          5 | —                          | —                          |
| resolved_date        | datetime2      | YES        |            |           |               | 0%      |     496456 | 1899-12-30 00:00:00        | 2025-05-13 16:55:21.900000 |
| closed_date          | datetime2      | YES        |            |           |               | 0%      |     503718 | 1899-12-30 00:00:00        | 2025-05-13 20:55:21.900000 |
| next_action          | nvarchar(255)  | YES        |            |           |               | 4%      |         34 | —                          | —                          |
| next_action_due_date | datetime2      | YES        |            |           |               | 4%      |     473668 | 1899-12-30 00:00:00        | 2917-06-27 06:29:00        |
| task_status          | nvarchar(255)  | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| task_state           | nvarchar(255)  | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| task_instruction     | nvarchar(4000) | YES        |            |           |               | 2%      |     357222 | —                          | —                          |

---

### dbo.tasks_history {#dbo-tasks-history}

| Property | Value |
|---|---|
| Full name | `[dbo].[tasks_history]` |
| Row count | 658,955 |
| Total size | 91.3 MB |
| Used size | 91.3 MB |
| Created | 2020-02-28 17:26 |
| Schema modified | 2020-02-28 17:26 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column               | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|----------------------|---------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| task_id              | int           | YES        |            |           |               | 0%      |     504296 | 102                 | 539229              |
| owned_by             | nvarchar(255) | YES        |            |           |               | 0%      |        977 | —                   | —                   |
| next_action          | nvarchar(255) | YES        |            |           |               | 3%      |         41 | —                   | —                   |
| next_action_due_date | datetime2     | YES        |            |           |               | 3%      |     545442 | 1899-12-30 00:00:00 | 9021-07-29 12:00:00 |
| task_status          | nvarchar(255) | YES        |            |           |               | 0%      |          5 | —                   | —                   |
| task_state           | nvarchar(255) | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| current_record       | nvarchar(3)   | YES        |            |           |               | 0%      |          2 | —                   | —                   |
| record_start_date    | datetime2     | YES        |            |           |               | 0%      |       1840 | 2020-02-26 00:00:00 | 2025-05-15 00:00:00 |
| record_end_date      | datetime2     | YES        |            |           |               | 77%     |       1828 | 2020-02-28 00:00:00 | 2025-05-15 00:00:00 |

---

### dbo.Tickets {#dbo-tickets}

| Property | Value |
|---|---|
| Full name | `[dbo].[Tickets]` |
| Row count | 851,065 |
| Total size | 785.4 MB |
| Used size | 785.3 MB |
| Created | 2017-09-19 09:36 |
| Schema modified | 2020-05-26 09:35 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                     | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|----------------------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| ticket_number              | nvarchar(50)  | NO         |            |           |               | 0%      |     850986 | —                          | —                          |
| open_date                  | datetime2     | YES        |            |           |               | 0%      |     850756 | 2010-01-01 04:00:00        | 2025-08-05 12:41:13.833333 |
| opened_by                  | nvarchar(50)  | YES        |            |           |               | 0%      |       9622 | —                          | —                          |
| ticket_status              | nvarchar(50)  | YES        |            |           |               | 0%      |          9 | —                          | —                          |
| line_of_business           | nvarchar(50)  | YES        |            |           |               | 0%      |         62 | —                          | —                          |
| ticket_priority            | nvarchar(15)  | YES        |            |           |               | 0%      |          7 | —                          | —                          |
| owned_by_team              | nvarchar(100) | YES        |            |           |               | 0%      |        109 | —                          | —                          |
| incident_duration_in_days  | numeric(38,4) | YES        |            |           |               | 0%      |      19929 | -0.0800                    | 3055.9700                  |
| sla_name                   | nvarchar(30)  | YES        |            |           |               | 0%      |          8 | —                          | —                          |
| first_call_resolution      | nvarchar(15)  | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| ticket_source              | nvarchar(50)  | YES        |            |           |               | 0%      |         21 | —                          | —                          |
| incident_duration_in_hours | numeric(38,4) | YES        |            |           |               | 0%      |     122606 | -1.9900                    | 73343.3700                 |
| service_id                 | nvarchar(100) | YES        |            |           |               | 19%     |      44838 | —                          | —                          |
| close_date                 | datetime2     | YES        |            |           |               | 0%      |     847757 | 1899-12-30 00:00:00        | 2025-05-05 19:26:05.356666 |
| ticket_type                | nvarchar(30)  | YES        |            |           |               | 0%      |          4 | —                          | —                          |
| subject                    | nvarchar(100) | YES        |            |           |               | 0%      |     483589 | —                          | —                          |
| area_of_failure            | nvarchar(50)  | YES        |            |           |               | 5%      |        257 | —                          | —                          |
| area_of_failure_detail     | nvarchar(50)  | YES        |            |           |               | 5%      |        416 | —                          | —                          |
| task_count                 | int           | YES        |            |           |               | 0%      |         46 | 0                          | 110                        |
| closed_by_team             | nvarchar(50)  | YES        |            |           |               | 5%      |         94 | —                          | —                          |
| ticket_customer_type       | nvarchar(15)  | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| ticket_resolution_area     | nvarchar(50)  | YES        |            |           |               | 5%      |         29 | —                          | —                          |
| ticket_created_by_team     | nvarchar(50)  | YES        |            |           |               | 0%      |        102 | —                          | —                          |
| ticket_resolved_by_team    | nvarchar(50)  | YES        |            |           |               | 1%      |        101 | —                          | —                          |
| ticket_responded_by_team   | nvarchar(50)  | YES        |            |           |               | 2%      |         95 | —                          | —                          |
| ticket_respond_by_date     | datetime2     | YES        |            |           |               | 0%      |     831880 | 1899-12-30 00:00:00        | 2207-01-23 21:18:48.103333 |
| techtime_minutes           | numeric(38,4) | YES        |            |           |               | 59%     |       2054 | 0.0000                     | 100011.0000                |
| techtime_hours             | numeric(38,4) | YES        |            |           |               | 58%     |       2709 | 0.0000                     | 1666.8500                  |
| resolve_date               | datetime2     | YES        |            |           |               | 1%      |     818616 | 1899-12-30 00:00:00        | 2025-06-27 19:16:17.450000 |
| MTTR                       | numeric(38,4) | YES        |            |           |               | 6%      |      56850 | 0.0000                     | 2845672.0000               |
| category                   | nvarchar(75)  | YES        |            |           |               | 0%      |        378 | —                          | —                          |
| subcategory                | nvarchar(75)  | YES        |            |           |               | 0%      |        747 | —                          | —                          |
| client_id                  | nvarchar(35)  | YES        |            |           |               | 1%      |       9717 | —                          | —                          |
| client_support_tier        | nvarchar(30)  | YES        |            |           |               | 1%      |         13 | —                          | —                          |
| client_ce_pod              | nvarchar(30)  | YES        |            |           |               | 1%      |         26 | —                          | —                          |
| is_master_ticket           | bit           | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| master_ticket_number       | nvarchar(42)  | YES        |            |           |               | 8%      |          1 | —                          | —                          |
| ticket_impact              | nvarchar(100) | YES        |            |           |               | 5%      |          9 | —                          | —                          |
| ticket_urgency             | nvarchar(100) | YES        |            |           |               | 5%      |          8 | —                          | —                          |
| client_source_system       | nvarchar(50)  | YES        |            |           |               | 27%     |          5 | —                          | —                          |
| initiator_email            | nvarchar(50)  | YES        |            |           |               | 2%      |      37282 | —                          | —                          |
| customer_contact           | nvarchar(75)  | YES        |            |           |               | 0%      |      33129 | —                          | —                          |
| ticket_state               | varchar(15)   | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| ticket_visibility          | nvarchar(255) | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| cherwell_bug_identified    | nvarchar(255) | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| cherwell_bug_details       | nvarchar(255) | YES        |            |           |               | 97%     |          3 | —                          | —                          |
| ticket_responded_date      | datetime2     | YES        |            |           |               | 2%      |     525980 | 1899-12-30 00:00:00        | 2025-03-04 21:30:34        |
| ticket_resolve_by_date     | nvarchar(255) | YES        |            |           |               | 0%      |     686629 | —                          | —                          |
| respond_slo_met            | nvarchar(5)   | YES        |            |           |               | 0%      |          2 | —                          | —                          |
| resolve_slo_met            | nvarchar(5)   | YES        |            |           |               | 2%      |          3 | —                          | —                          |
| ticket_owned_since         | datetime2     | YES        |            |           |               | 20%     |     105815 | 1899-12-30 00:00:00        | 2025-03-04 21:09:14.733333 |
| reopened_times             | int           | YES        |            |           |               | 98%     |         30 | 1                          | 77                         |
| last_reopen_date           | datetime2     | YES        |            |           |               | 98%     |      17815 | 2015-12-11 08:44:28.733333 | 2025-03-03 17:16:05.316666 |

---

### dbo.Tickets_JSM {#dbo-tickets-jsm}

| Property | Value |
|---|---|
| Full name | `[dbo].[Tickets_JSM]` |
| Row count | 0 |
| Total size | 0.0 MB |
| Used size | 0.0 MB |
| Created | 2025-05-14 09:19 |
| Schema modified | 2025-05-14 09:19 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                  | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max   |
|-------------------------|---------------|------------|------------|-----------|---------------|---------|------------|-------|-------|
| customer_id             | int           | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| organization_name       | nvarchar(224) | YES        |            |           |               | 0%      |          0 | —     | —     |
| time_spent              | nvarchar(60)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| reporter_name           | nvarchar(120) | YES        |            |           |               | 0%      |          0 | —     | —     |
| ticket_number           | nvarchar(30)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| ticket_type             | nvarchar(93)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| ticket_status           | nvarchar(72)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| ticket_status_category  | nvarchar(39)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| status_date             | datetime      | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| time_to_done            | nvarchar(765) | YES        |            |           |               | 0%      |          0 | —     | —     |
| billable_time           | nvarchar(60)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| resolution_date         | nvarchar(60)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| ticket_last_viewed      | nvarchar(765) | YES        |            |           |               | 0%      |          0 | —     | —     |
| ticket_created          | datetime      | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| affected_hardware       | nvarchar(230) | YES        |            |           |               | 0%      |          0 | —     | —     |
| priority                | nvarchar(54)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| labels                  | nvarchar(350) | YES        |            |           |               | 0%      |          0 | —     | —     |
| satisfaction            | bigint        | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| satisfaction_date       | nvarchar(60)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| ticket_last_updated     | datetime      | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |
| status_name             | nvarchar(72)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| status_category_key     | nvarchar(39)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| color_name              | nvarchar(27)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| summary                 | nvarchar(660) | YES        |            |           |               | 0%      |          0 | —     | —     |
| summary_short           | nvarchar(660) | YES        |            |           |               | 0%      |          0 | —     | —     |
| creator_name            | nvarchar(120) | YES        |            |           |               | 0%      |          0 | —     | —     |
| timezone                | nvarchar(51)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| creator_account_type    | nvarchar(27)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| is_billable             | varchar(3)    | NO         |            |           |               | 0%      |          0 | —     | —     |
| recorded_time           | varchar(3)    | NO         |            |           |               | 0%      |          0 | —     | —     |
| team_                   | nvarchar(105) | YES        |            |           |               | 0%      |          0 | —     | —     |
| has_client_id           | varchar(3)    | NO         |            |           |               | 0%      |          0 | —     | —     |
| data_last_updated       | datetime      | NO         |            |           |               | 0%      |          0 | NULL  | NULL  |
| issue_type              | nvarchar(45)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| smart_hands             | nvarchar(60)  | YES        |            |           |               | 0%      |          0 | —     | —     |
| smart_hands_after_hours | nvarchar(765) | YES        |            |           |               | 0%      |          0 | —     | —     |
| first_response_minutes  | int           | YES        |            |           |               | 0%      |          0 | NULL  | NULL  |

---

### dbo.utility_billing_tracker {#dbo-utility-billing-tracker}

| Property | Value |
|---|---|
| Full name | `[dbo].[utility_billing_tracker]` |
| Row count | 246 |
| Total size | 0.1 MB |
| Used size | 0.0 MB |
| Created | 2025-02-12 09:43 |
| Schema modified | 2025-02-12 09:57 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column       | Type        | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max   |
|--------------|-------------|------------|------------|-----------|---------------|---------|------------|-------|-------|
| month        | varchar(50) | YES        |            |           |               | 0%      |         57 | —     | —     |
| period_start | varchar(50) | YES        |            |           |               | 0%      |         99 | —     | —     |
| period_end   | varchar(50) | YES        |            |           |               | 0%      |        100 | —     | —     |
| quantity     | varchar(50) | YES        |            |           |               | 0%      |        196 | —     | —     |
| daily_avg_kw | varchar(50) | YES        |            |           |               | 0%      |        198 | —     | —     |
| currency     | varchar(50) | YES        |            |           |               | 0%      |          2 | —     | —     |
| days         | varchar(50) | YES        |            |           |               | 0%      |         11 | —     | —     |
| kw_hr_rate   | varchar(50) | YES        |            |           |               | 0%      |        207 | —     | —     |
| total_cost   | varchar(50) | YES        |            |           |               | 0%      |        209 | —     | —     |
| site         | varchar(50) | YES        |            |           |               | 0%      |          5 | —     | —     |

---

### profitability.alertlogic_invoice_details {#profitability-alertlogic-invoice-details}

| Property | Value |
|---|---|
| Full name | `[profitability].[alertlogic_invoice_details]` |
| Row count | 242 |
| Total size | 0.1 MB |
| Used size | 0.1 MB |
| Created | 2025-10-09 11:59 |
| Schema modified | 2025-10-09 11:59 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column                 | Type         | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|------------------------|--------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| invoice_id             | varchar(255) | YES        |            |           |               | 0%      |          9 | —                   | —                   |
| client_id              | int          | YES        |            |           |               | 0%      |         33 | 1000343             | 7036659             |
| company                | varchar(255) | YES        |            |           |               | 0%      |         33 | —                   | —                   |
| al_order_number        | float(53)    | YES        |            |           |               | 0%      |         49 | 33875.0             | 42672.0             |
| al_product_description | varchar(255) | YES        |            |           |               | 0%      |         16 | —                   | —                   |
| quantity               | varchar(255) | YES        |            |           |               | 0%      |         16 | —                   | —                   |
| service_period         | datetime     | YES        |            |           |               | 0%      |         13 | 2025-07-01 00:00:00 | 2026-07-01 00:00:00 |
| amount                 | money        | YES        |            |           |               | 0%      |         39 | 0.0000              | 3439.8000           |
| currency               | varchar(255) | YES        |            |           |               | 0%      |          1 | —                   | —                   |

---

### profitability.imperva_invoice_details {#profitability-imperva-invoice-details}

| Property | Value |
|---|---|
| Full name | `[profitability].[imperva_invoice_details]` |
| Row count | 552 |
| Total size | 0.1 MB |
| Used size | 0.0 MB |
| Created | 2025-10-10 11:38 |
| Schema modified | 2025-10-10 11:38 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column         | Type         | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                 | Max                 |
|----------------|--------------|------------|------------|-----------|---------------|---------|------------|---------------------|---------------------|
| client_id      | int          | YES        |            |           |               | 0%      |         33 | 1715629             | 7015093             |
| amount         | money        | YES        |            |           |               | 0%      |        134 | 220.7300            | 121564.7256         |
| service_period | datetime     | YES        |            |           |               | 0%      |         21 | 2024-01-01 00:00:00 | 2025-09-01 00:00:00 |
| currency       | varchar(255) | YES        |            |           |               | 0%      |          1 | —                   | —                   |

---

### profitability.hardware_watts {#profitability-hardware-watts}

| Property | Value |
|---|---|
| Full name | `[profitability].[hardware_watts]` |
| Row count | 20 |
| Total size | 0.0 MB |
| Created | 2026-05-19 |
| Schema modified | 2026-05-19 |

Wattage lookup keyed by Fusion `product_catalog.id` / component `id`. Used in CPQ overhead calculations for power-cost line items (`per_kw` measures in `cost_drivers.json`). Convert to kW: `watts / 1000`.

#### Columns

| Column       | Type         | Nullable | Notes |
|--------------|--------------|----------|-------|
| fusion_id    | int          | YES      | FK → Fusion `product_catalog.id` or `components.id` |
| sku_name     | varchar(255) | YES      | Human-readable label matching Fusion product name |
| sku_category | varchar(255) | YES      | `Server` or `Firewall` |
| watts        | int          | YES      | Peak power draw in watts |

#### Notes

- No PK or FK constraints defined — it is a plain lookup table.
- `fusion_id` maps to the same ID space used by `ocean_sku_cost.sku_id`.
- Servers range from 85 W (Essential 5.0) to 400 W (Pro 6.0 / Pro 7.0). Firewalls: 75–122 W.
- 20 rows as of 2026-05-19; covers Series 5, 6, 7 servers and Juniper SRX firewalls.

#### Sample rows (as of 2026-05-19)

| fusion_id | sku_name | sku_category | watts |
|-----------|----------|--------------|-------|
| 930 | Juniper SRX 300 | Firewall | 75 |
| 943 | Pro Series 5.0 | Server | 224 |
| 975 | Essential Series 5.0 | Server | 85 |
| 1254 | Pro Series 6.0 | Server | 400 |
| 1299 | R470 - Advanced Series 7.0 | Server | 280 |
| 1300 | R670 - Pro Series 7.0 | Server | 400 |

---

### profitability.ocean_sku_cost {#profitability-ocean-sku-cost}

| Property | Value |
|---|---|
| Full name | `[profitability].[ocean_sku_cost]` |
| Row count | 680 |
| Total size | 0.2 MB |
| Used size | 0.1 MB |
| Created | 2025-10-09 10:56 |
| Schema modified | 2025-10-09 10:56 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column        | Type         | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min   | Max     |
|---------------|--------------|------------|------------|-----------|---------------|---------|------------|-------|---------|
| sku_level     | varchar(255) | YES        |            |           |               | 0%      |          2 | —     | —       |
| sku_category  | varchar(255) | YES        |            |           |               | 0%      |          6 | —     | —       |
| sku_id        | int          | YES        |            |           |               | 0%      |        676 | 23    | 6241    |
| sku_name      | varchar(255) | YES        |            |           |               | 0%      |        660 | —     | —       |
| sku_type      | varchar(255) | YES        |            |           |               | 0%      |         25 | —     | —       |
| sku_cost      | float(53)    | YES        |            |           |               | 0%      |        207 | -1.0  | 7554.62 |
| cost_currency | varchar(255) | YES        |            |           |               | 0%      |          1 | —     | —       |
| vendor        | varchar(255) | YES        |            |           |               | 16%     |         27 | —     | —       |
| comments      | varchar(255) | YES        |            |           |               | 44%     |         35 | —     | —       |

---

### renewals.ocean_services_renewal_date {#renewals-ocean-services-renewal-date}

| Property | Value |
|---|---|
| Full name | `[renewals].[ocean_services_renewal_date]` |
| Row count | 5,735 |
| Total size | 0.8 MB |
| Used size | 0.7 MB |
| Created | 2026-03-06 09:16 |
| Schema modified | 2026-03-06 09:16 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column          | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|-----------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| client_id       | int           | NO         |            |           |               | 0%      |        785 | 1000002                    | 7036717                    |
| company_name    | nvarchar(255) | YES        |            |           |               | 0%      |        785 | —                          | —                          |
| service_id      | int           | NO         |            |           |               | 0%      |       5735 | -7008600                   | 7981441                    |
| expiration_date | datetime2     | YES        |            |           |               | 0%      |       3824 | 1899-12-31 08:12:09        | 2030-12-29 23:00:00        |
| m2m             | varchar(255)  | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| cad_budget_mrc  | numeric(38,4) | YES        |            |           |               | 0%      |       2418 | 0.0000                     | 39723.7500                 |
| service_status  | nvarchar(255) | YES        |            |           |               | 0%      |          6 | —                          | —                          |
| first_term      | varchar(3)    | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| last_updated    | datetime      | NO         |            |           |               | 0%      |          1 | 2026-03-06 09:16:07.070000 | 2026-03-06 09:16:07.070000 |

---

### renewals.ocean_services_renewal_date_new {#renewals-ocean-services-renewal-date-new}

| Property | Value |
|---|---|
| Full name | `[renewals].[ocean_services_renewal_date_new]` |
| Row count | 5,735 |
| Total size | 0.8 MB |
| Used size | 0.7 MB |
| Created | 2026-03-06 09:16 |
| Schema modified | 2026-03-06 09:16 |
| Last read | — |
| Last write | — |

> ⚠️ Last read/write reset on server restart. 'Who' requires SQL Audit.

#### Columns

| Column          | Type          | Nullable   | Identity   | Default   | Description   | NULL%   |   Distinct | Min                        | Max                        |
|-----------------|---------------|------------|------------|-----------|---------------|---------|------------|----------------------------|----------------------------|
| client_id       | int           | NO         |            |           |               | 0%      |        785 | 1000002                    | 7036717                    |
| company_name    | nvarchar(255) | YES        |            |           |               | 0%      |        785 | —                          | —                          |
| service_id      | int           | NO         |            |           |               | 0%      |       5735 | -7008600                   | 7981441                    |
| expiration_date | datetime2     | YES        |            |           |               | 0%      |       3824 | 1899-12-31 08:12:09        | 2030-12-29 23:00:00        |
| m2m             | varchar(255)  | YES        |            |           |               | 0%      |          3 | —                          | —                          |
| cad_budget_mrc  | numeric(38,4) | YES        |            |           |               | 0%      |       2418 | 0.0000                     | 39723.7500                 |
| service_status  | nvarchar(255) | YES        |            |           |               | 0%      |          6 | —                          | —                          |
| first_term      | varchar(3)    | NO         |            |           |               | 0%      |          2 | —                          | —                          |
| last_updated    | datetime      | NO         |            |           |               | 0%      |          1 | 2026-03-06 09:16:07.070000 | 2026-03-06 09:16:07.070000 |

---

## Views

### dbo.dimproductattributes_extended {#view-dbo-dimproductattributes-extended}

Created: 2019-07-05 14:33  |  Modified: 2019-07-05 14:33

```sql
(definition unavailable)
```

### dbo.last_thirty_days_avg_exchange_rate {#view-dbo-last-thirty-days-avg-exchange-rate}

Created: 2017-10-03 15:18  |  Modified: 2017-10-03 15:18

```sql
(definition unavailable)
```

---

## Stored Procedures

_(none)_

---

## Functions

### dbo.SplitString {#func-dbo-splitstring}

Type: `SQL_TABLE_VALUED_FUNCTION`  |  Created: 2015-05-20 11:02  |  Modified: 2015-05-20 11:02

```sql
(definition unavailable)
```

### dbo.tvf_client_active_history_view {#func-dbo-tvf-client-active-history-view}

Type: `SQL_INLINE_TABLE_VALUED_FUNCTION`  |  Created: 2020-01-14 08:43  |  Modified: 2020-01-16 17:22

```sql
(definition unavailable)
```

### dbo.tvf_mrc_charges {#func-dbo-tvf-mrc-charges}

Type: `SQL_TABLE_VALUED_FUNCTION`  |  Created: 2023-10-19 11:05  |  Modified: 2024-06-14 15:26

```sql
(definition unavailable)
```

### dbo.view_product_mrc {#func-dbo-view-product-mrc}

Type: `SQL_INLINE_TABLE_VALUED_FUNCTION`  |  Created: 2020-06-15 08:48  |  Modified: 2020-06-15 08:48

```sql
(definition unavailable)
```

### dbo.view_product_skus {#func-dbo-view-product-skus}

Type: `SQL_INLINE_TABLE_VALUED_FUNCTION`  |  Created: 2020-06-15 08:27  |  Modified: 2020-06-15 08:27

```sql
(definition unavailable)
```

---

## Triggers

_(none)_

---

## SQL Agent Jobs

_(none or access denied)_

---

## Cross-Database References

_(none detected)_
