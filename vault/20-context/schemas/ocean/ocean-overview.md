---
type: schema-overview
updated: 2026-03-06
---

# Ocean — Database Overview

**Server:** 10.121.21.211  
**Databases:** DM_BusinessInsights, FinancialReporting (same server, same credentials)  
**Purpose:** Customer account intelligence — active services, components, renewals, churn, and revenue.  
**Primary filter:** Always scope queries to a single `client_id` (integer).

---

## Table Map

```
DM_BusinessInsights
├── dbo
│   ├── dimServices                  ← one row per active service per client
│   │     ↓ service_id (int)         → dimComponents (many components per service)
│   │     ↓ service_id (int)         → ocean_services_renewal_date (one renewal row per service)
│   │     ↓ CAST(fusion_id AS nvarchar) → dimProductAttributes (product/SKU metadata)
│   │     ↓ datacenter_code          → dimdatacenterattributes (datacenter metadata)
│   │     ↓ client_id + CAST(service_id AS varchar) → finance_revenue_mapping
│   ├── dimComponents                ← component-level detail per service
│   ├── dimProductAttributes         ← product/SKU dimension (fusion_id is nvarchar here)
│   ├── dimdatacenterattributes      ← datacenter dimension (datacenter_code is the key)
│   └── Churn                        ← cancelled services (standalone, not joined to dimServices)
└── renewals
    └── ocean_services_renewal_date  ← expiration dates + m2m flag per service

FinancialReporting
└── dbo
    └── finance_revenue_mapping      ← billing line items (service_id is varchar here)
```

---

## Join Patterns

### Services + Components
```sql
SELECT s.*, c.component_category, c.component_type, c.component, c.cad_component_mrc
FROM [DM_BusinessInsights].[dbo].[dimServices] s
LEFT JOIN [DM_BusinessInsights].[dbo].[dimComponents] c
  ON s.service_id = c.service_id
WHERE s.client_id = :client_id
  AND s.service_status = 'Online'
```

### Services + Renewal Dates
```sql
SELECT s.*, r.expiration_date, r.m2m
FROM [DM_BusinessInsights].[dbo].[dimServices] s
LEFT JOIN [DM_BusinessInsights].[renewals].[ocean_services_renewal_date] r
  ON s.service_id = r.service_id
WHERE s.client_id = :client_id
  AND s.service_status = 'Online'
```

### Services + Financial Revenue (current period only)
```sql
-- service_id type mismatch: int in dimServices, varchar(20) in finance — CAST required
SELECT s.nickname, s.product, s.cad_mrc, f.xtndprce_period_nx, f.Category, f.revenue_period
FROM [DM_BusinessInsights].[dbo].[dimServices] s
LEFT JOIN [FinancialReporting].[dbo].[finance_revenue_mapping] f
  ON s.client_id = f.client_id
  AND CAST(s.service_id AS varchar) = f.service_id
  AND f.revenue_period = (
      SELECT MAX(revenue_period)
      FROM [FinancialReporting].[dbo].[finance_revenue_mapping]
      WHERE client_id = :client_id
  )
WHERE s.client_id = :client_id
  AND s.service_status = 'Online'
```

### Renewals + Financial (expiring services and what they bill)
```sql
SELECT r.service_id, r.expiration_date, r.m2m, s.product, s.cad_mrc,
       f.xtndprce_period_nx AS billed_amount, f.Category
FROM [DM_BusinessInsights].[renewals].[ocean_services_renewal_date] r
JOIN [DM_BusinessInsights].[dbo].[dimServices] s
  ON r.service_id = s.service_id
LEFT JOIN [FinancialReporting].[dbo].[finance_revenue_mapping] f
  ON r.client_id = f.client_id
  AND CAST(r.service_id AS varchar) = f.service_id
  AND f.revenue_period = (
      SELECT MAX(revenue_period)
      FROM [FinancialReporting].[dbo].[finance_revenue_mapping]
      WHERE client_id = :client_id
  )
WHERE r.client_id = :client_id
  AND r.expiration_date BETWEEN GETDATE() AND DATEADD(day, 90, GETDATE())
```

### Services + Product Attributes
```sql
-- fusion_id type mismatch: int in dimServices, nvarchar in dimProductAttributes — CAST required
SELECT s.service_id, s.product, p.product_group, p.lifecycle, p.functional_group_bi
FROM [DM_BusinessInsights].[dbo].[dimServices] s
LEFT JOIN [DM_BusinessInsights].[dbo].[dimProductAttributes] p
  ON CAST(s.fusion_id AS nvarchar) = p.fusion_id
WHERE s.client_id = :client_id
```

### Services + Datacenter Info
```sql
SELECT s.service_id, s.product, d.country, d.datacenter_region, d.datacenter_status
FROM [DM_BusinessInsights].[dbo].[dimServices] s
LEFT JOIN [DM_BusinessInsights].[dbo].[dimdatacenterattributes] d
  ON s.datacenter_code = d.datacenter_code
WHERE s.client_id = :client_id
```

---

## Type Gotchas — Read Before Writing Any Join

| Tables | Column | Issue | Fix |
|--------|--------|-------|-----|
| dimServices → finance_revenue_mapping | service_id | int vs varchar(20) | CAST(s.service_id AS varchar) = f.service_id |
| dimServices → dimProductAttributes | fusion_id | int vs nvarchar(255) | CAST(s.fusion_id AS nvarchar) = p.fusion_id |
| Churn.service_id | service_id | nvarchar (not int) | Do not join Churn to dimServices on service_id — treat as standalone |

---

## Common Filters

| Goal | Filter |
|------|--------|
| Active services only | WHERE service_status = 'Online' |
| Current billing period | WHERE revenue_period = (SELECT MAX(revenue_period) FROM ... WHERE client_id = :client_id) |
| Month-to-month services | WHERE m2m = 'yes' (on ocean_services_renewal_date) |
| Expiring within 90 days | WHERE expiration_date BETWEEN GETDATE() AND DATEADD(day, 90, GETDATE()) |
| Cross-currency comparison | Use cad_mrc / cad_component_mrc — always CAD regardless of client currency |
| Legacy/M2M contracts | contract_months_remaining = -1 in dimServices means no fixed term |

---

## Tables Quick Reference

| Table | Database | Schema | Grain | Key |
|-------|----------|--------|-------|-----|
| dimServices | DM_BusinessInsights | dbo | 1 row per active service | client_id, service_id (int) |
| dimComponents | DM_BusinessInsights | dbo | 1+ rows per service | client_id, service_id (int) |
| ocean_services_renewal_date | DM_BusinessInsights | renewals | 1 row per service | client_id, service_id (int) |
| Churn | DM_BusinessInsights | dbo | 1 row per cancelled service | client_id (standalone) |
| dimProductAttributes | DM_BusinessInsights | dbo | 1 row per SKU | fusion_id (nvarchar) |
| dimdatacenterattributes | DM_BusinessInsights | dbo | 1 row per datacenter | datacenter_code |
| finance_revenue_mapping | FinancialReporting | dbo | 1 row per billing line | client_id, service_id (varchar) |
