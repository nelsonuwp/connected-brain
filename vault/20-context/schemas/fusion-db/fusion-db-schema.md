---
type: schema-reference
generated: 2026-04-14 07:34
source: fusion.public.xml + live audit (sb_readonly)
---

# Fusion DB — Schema Reference

**Database:** `fusion` (PostgreSQL 9.3.25) on `db1.peer1.com:5432`  
**Access:** SSH tunnel through `ocean-upi1.peer1.com` (10.121.21.20)  
**Total tables in schema:** 436  
**Accessible to `sb_readonly`:** 333  
**Denied:** 103  

---

## Contents

- [Priority Tables (AccountIntel)](#priority-tables-accountintel)
- [All Accessible Tables](#all-accessible-tables)
- [Inaccessible Tables](#inaccessible-tables)
- [Access Audit Summary](#access-audit-summary)

---

## Priority Tables (AccountIntel)

These tables are directly used or highly relevant to AccountIntel pipeline stages.

### `cancellation_category`

**Status:** ✅ accessible  
**Row count:** ~29  

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `category` | `text` |  |
| `sort_order` | `int4` |  |
| `in_portal` | `bool` |  |

**Indexes:**
- `cancellation_category_pkey` — UNIQUE (id)

**Referenced by:** `customer_products`.`cancellation_category`  

**Sample rows (3):**

| id | category | sort_order | in_portal |
| --- | --- | --- | --- |
| 1 | You don't have the products I need | 1 | True |
| 2 | You need to lower your prices | 1 | True |
| 5 | Dissatisfied with Hardware | 1 | True |

---

### `client_relations`

**Status:** ✅ accessible  
**Row count:** ~25,713  

| Column | Type | Flags |
|--------|------|-------|
| `client_id` | `int4` | PK · NOT NULL · → customers.customers_id |
| `employee_id` | `int4` | PK · NOT NULL · → employees.id |
| `product_line_id` | `int4` | PK · NOT NULL · → product_lines.id |
| `client_relations_role_id` | `int4` | PK · NOT NULL · → client_relations_roles.id |
| `created_date` | `timestamptz` | NOT NULL |

**Indexes:**
- `client_relations_pkey` — UNIQUE (client_id, employee_id, product_line_id, client_relations_role_id)
- `client_relations_client_idx` — (client_id)

**Sample rows (3):**

| client_id | employee_id | product_line_id | client_relations_role_id | created_date |
| --- | --- | --- | --- | --- |
| 7001862 | 15869 | 4 | 1 | 2010-04-05 21:12:03.177583-04:00 |
| 7001547 | 15869 | 4 | 1 | 2010-04-05 21:12:03.177583-04:00 |
| 7001695 | 1647411 | 4 | 1 | 2010-04-05 21:12:03.177583-04:00 |

---

### `client_relations_roles`

**Status:** ✅ accessible  
**Row count:** ~5  

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(64)` | NOT NULL |
| `description` | `text` |  |

**Indexes:**
- `client_relations_roles_pkey` — UNIQUE (id)
- `client_relations_roles_name_key` — UNIQUE (name)

**Referenced by:** `client_relations_product_line_independent`.`client_relations_role_id`, `client_relations`.`client_relations_role_id`, `employee_client_relations_roles_matrix`.`client_relations_role_id`  

**Sample rows (3):**

| id | name | description |
| --- | --- | --- |
| 1 | nas | New Acquisition Sales |
| 2 | bdc | Business Development Consultant |
| 3 | cse | Channel Sales Executive |

---

### `customer_products`

**Status:** ✅ accessible  
**Row count:** ~162,775  

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `customers_id` | `int4` | NOT NULL |
| `customer_order_id` | `int4` | → order_line_items.id |
| `customer_product_idnum` | `int4` | NOT NULL |
| `product_catalog_id` | `int4` | NOT NULL · → product_catalog.id |
| `products_model` | `text` |  |
| `products_name` | `text` | NOT NULL |
| `mrc` | `numeric` |  |
| `products_status_id` | `int4` | NOT NULL · → customer_products_status_options.id |
| `first_online` | `timestamptz` |  |
| `hide_in_portal` | `bool` |  |
| `cancellation_category` | `int4` | → cancellation_category.id |
| `cancellation_comments` | `text` |  |
| `products_nickname` | `varchar(64)` | NOT NULL |
| `service_type_id` | `int4` | NOT NULL · → service_type_pl.service_type_id |
| `modified_by` | `int4` | NOT NULL · → employees.id |
| `setup` | `numeric` | NOT NULL |
| `billable` | `bool` | NOT NULL |
| `currency` | `varchar(3)` | NOT NULL · → currencies.code |
| `product_line_id` | `int4` | NOT NULL · → product_lines.id |
| `exchange_rate` | `numeric` | NOT NULL |
| `is_virtual` | `bool` | NOT NULL |
| `rate` | `numeric` |  |
| `is_qtc` | `bool` |  |

**Indexes:**
- `customer_products_pkey` — UNIQUE (id)
- `customer_product_id_status` — (id, products_status_id)
- `customer_products_client_id_status_id_product_line_id_id` — (customers_id, products_status_id, product_line_id)
- `customer_products_order_id` — UNIQUE (customer_order_id)
- `unique_customer_id_customer_product_idnum` — UNIQUE (customers_id, customer_product_idnum)
- `unique_customer_products_nickname` — UNIQUE (customers_id, products_nickname)

**Referenced by:** `client_bag_services`.`service_id`, `client_firewall_vlan`.`service_id`, `client_loadbalancer_vlan`.`service_id`, `client_private_rack`.`service_id`, `client_solution_services`.`service_id`, `client_tickets`.`service_id`, `cloud_storage_attributes`.`object_id`, `customer_products_attributes`.`object_id`, `customer_products_status_history`.`customer_product_id`, `order_entry_solution_node`.`service_id`, `order_line_item_migrated_services`.`service_id`, `provisioning_tickets`.`service_id`, `sb_customer_product_log`.`customer_product_id`, `service_billing_details`.`service_id`, `service_cancellation_queue`.`service_id`, `service_licenses`.`service_id`, `service_notes`.`service_id`, `service_options`.`customer_products_id`, `ticket_support_times`.`service_id`, `vmware_clusters`.`parent_service_id`, `vmware_clusters`.`service_id`, `vmware_guests`.`parent_service_id`, `vmware_guests`.`service_id`, `vmware_hosts`.`parent_service_id`, `vmware_hosts`.`service_id`, `vmware_vcenters`.`service_id`, `workflow_notifications`.`service_id`, `xref_cloud_storage_subtenants_services`.`service_id`, `xref_customer_products_dcc`.`customer_products_id`, `xref_services_private_net`.`service_id`, `xref_services_private_rack`.`service_id`  

**Sample rows (3):**

| id | customers_id | customer_order_id | customer_product_idnum | product_catalog_id | products_model | products_name | mrc | products_status_id | first_online | hide_in_portal | cancellation_category | cancellation_comments | products_nickname | service_type_id | modified_by | setup | billable | currency | product_line_id | exchange_rate | is_virtual | rate | is_qtc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5262610 | 7011316 | NULL | 58 | 696 | CA2SCOTOIL01 | Mission Critical Cloud | 0.00000 | 18 | 2017-11-24 16:22:36.974602-05:00 | False | NULL |  | CA2SCOTOIL01 | 21 | 956742 | 0.00 | True | USD | 5 | 1.0000000 | True | NULL | False |
| 2704036 | 1000025 | 108732 | 18 | 336 | 2704036 | Guest Virtual | 0.00000 | 32 | 2012-04-27 23:14:21.208012-04:00 | False | 19 | cherwerll 221664

Hello,

We would like to decommission  | adnet.alt1 | 1 | 1924029 | 0.00 | True | CAD | 3 | 1.0000000 | True | NULL | False |
| 2980306 | 5000445 | 130505 | 1317 | 454 | 2980306 | MD1220 Dell PV SAS Storage Array Expansion Chassis | 600.00000 | 32 | 2012-12-04 19:18:00.748298-05:00 | False | 8 | PUBLIC Ticket #1976404 | storage23.mogilefs.sat.wordpress.com md1220b | 18 | 25470 | 0.00 | True | USD | 4 | 1.0000000 | False | NULL | False |

---

### `customers`

**Status:** ✅ accessible  
**Row count:** ~25,182  

| Column | Type | Flags |
|--------|------|-------|
| `customers_id` | `serial` | PK · auto · NOT NULL |
| `type_id` | `int4` | NOT NULL · → client_types_pl.client_type_id |
| `company_name` | `varchar(255)` | NOT NULL |
| `blacklisted` | `bool` | NOT NULL |
| `referred_by` | `int4` | → customers.customers_id |
| `overage_rate` | `numeric` | NOT NULL |
| `error_status` | `bool` | NOT NULL |
| `shopping_cart_only` | `bool` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` |  |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` |  |
| `payment_term` | `varchar(21)` | → payment_terms.payment_term |
| `preferred_currency` | `varchar(3)` | → currencies.code |
| `disabled` | `timestamptz` |  |
| `disabled_by` | `varchar(32)` |  |
| `client_industries_id` | `int4` | → client_industries.id |

**Indexes:**
- `customers_pkey` — UNIQUE (customers_id)
- `customers_customers_id_company_name_idx` — (customers_id, company_name)

**Referenced by:** `billable_ticket_invoicing`.`client_id`, `certificate_company`.`customers_id`, `client_bags`.`client_id`, `client_error_statuses`.`client_id`, `client_eula_acceptance`.`client_id`, `client_notes`.`client_id`, `client_orders`.`client_id`, `client_payment_methods`.`client_id`, `client_permission_roles`.`client_id`, `client_permission_users`.`client_id`, `client_private_net`.`client_id`, `client_private_rack`.`client_id`, `client_relations_product_line_independent`.`client_id`, `client_relations`.`client_id`, `client_solutions`.`client_id`, `client_tax_registrations`.`client_id`, `client_tickets`.`client_id`, `client_zones`.`client_id`, `clients_watchers`.`client_id`, `config_codes`.`customer_id`, `contact`.`customers_id`, `customer_tam`.`customers_id`, `customers_attributes`.`object_id`, `customers`.`referred_by`, `eula`.`client_id`, `fraud_gateway_transactions`.`client_id`, `login_history`.`client_id`, `nbt_invoices`.`customer_id`, `portal_login`.`client_id`, `sb_customer_log`.`customers_id`, `sessions`.`client_id`, `ticket_support_times`.`client_id`  

**Sample rows (3):**

| customers_id | type_id | company_name | blacklisted | referred_by | overage_rate | error_status | shopping_cart_only | created | created_by | last_modified | last_modified_by | payment_term | preferred_currency | disabled | disabled_by | client_industries_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | 3 | Unknown PEER 1 Client | False | NULL | 0.30 | True | False | 2011-09-25 20:54:34.535298-04:00 | NULL | 2012-09-14 10:27:06.690917-04:00 | jquintero | Net 30 | NULL | NULL | NULL | NULL |
| 200 | 10 | MH Support | False | NULL | 0.30 | False | False | 2012-11-15 23:14:14.481988-05:00 | hdawood | 2012-11-15 23:16:38.585151-05:00 | ocean_user | Net 30 | NULL | NULL | NULL | NULL |
| 1000003 | 1 | 22201936 Ontario LTD Talk Canada Home Phone | False | NULL | 0.30 | False | False | 2006-08-29 00:00:00-04:00 | NULL | 2010-07-24 20:43:05.244208-04:00 | cbrown | Net 15 | NULL | NULL | NULL | NULL |

---

### `employees`

**Status:** ✅ accessible  
**Row count:** ~5,324  

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `first_name` | `text` | NOT NULL |
| `middle_initial` | `bpchar` |  |
| `last_name` | `text` | NOT NULL |
| `suffix_name` | `text` |  |
| `email_address` | `text` | NOT NULL |
| `title` | `text` | NOT NULL |
| `username` | `text` | NOT NULL |
| `logged_on` | `bool` |  |
| `phone_local` | `varchar(30)` |  |
| `phone_toll_free` | `varchar(30)` |  |
| `phone_extension` | `varchar(10)` |  |

**Indexes:**
- `employees_pkey` — UNIQUE (id)
- `employees_username_key` — UNIQUE (username)

**Referenced by:** `billable_ticket_invoicing`.`username`, `cart`.`assisted_by`, `client_news`.`who`, `client_orders`.`entered_by`, `client_relations_product_line_independent`.`employee_id`, `client_relations`.`employee_id`, `clients_watchers`.`employee_id`, `customer_products`.`modified_by`, `customer_tam`.`employees_id`, `employee_client_relations_quotas`.`employee_id`, `employee_client_relations_roles_matrix`.`employee_id`, `order_commission_split`.`employee_id`, `portal_login`.`username`, `xref_roles_employees`.`employees_id`  

**Sample rows (3):**

| id | first_name | middle_initial | last_name | suffix_name | email_address | title | username | logged_on | phone_local | phone_toll_free | phone_extension |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 14283 | Tamara | NULL | Hossack | NULL | tbackus@peer1.com |  | thossack | False | NULL | NULL | NULL |
| 618594 | Libby | NULL | Sharp | NULL | lsharp@peer1.com |  | lsharp | False | NULL | NULL | NULL |
| 1024789 | s | NULL | ram | NULL | sram@peer1.com |  | sram | False | NULL | NULL | NULL |

---

### `exchange_rates`

**Status:** ✅ accessible  
**Row count:** ~15  

| Column | Type | Flags |
|--------|------|-------|
| `ocean_exchange_rate_id` | `varchar(15)` |  |
| `gp_exchange_rate_id` | `varchar(15)` |  |
| `functional_currency` | `varchar(3)` | PK · NOT NULL · → currencies.code |
| `originating_currency` | `varchar(3)` | PK · NOT NULL · → currencies.code |
| `exchange_rate` | `numeric` | NOT NULL |
| `last_modified` | `timestamp` | NOT NULL |

**Indexes:**
- `exchange_rates_pkey` — UNIQUE (functional_currency, originating_currency)

**Sample rows (3):**

| ocean_exchange_rate_id | gp_exchange_rate_id | functional_currency | originating_currency | exchange_rate | last_modified |
| --- | --- | --- | --- | --- | --- |
| NULL | NULL | GBP | GBP | 1.0000000 | 2009-10-11 22:03:41.587966 |
| NULL | NULL | CAD | CAD | 1.0000000 | 2009-10-11 22:03:41.587966 |
| NULL | NULL | USD | USD | 1.0000000 | 2009-10-11 22:03:41.587966 |

---

### `history_customer_products`

**Status:** ✅ accessible  
**Row count:** ~311,633,536  

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `customers_id` | `int4` |  |
| `customer_product_idnum` | `int4` |  |
| `products_model` | `text` |  |
| `products_name` | `text` |  |
| `products_status_id` | `int4` |  |
| `cancellation_category` | `int4` |  |
| `cancellation_comments` | `text` |  |
| `products_nickname` | `varchar(100)` |  |
| `service_type_id` | `int4` |  |
| `modified_by` | `int4` |  |
| `archive_date` | `timestamptz` |  |
| `mrc` | `numeric` |  |
| `setup` | `numeric` |  |
| `billable` | `bool` |  |
| `currency` | `varchar(3)` |  |
| `product_line_id` | `int4` |  |
| `exchange_rate` | `numeric` |  |
| `history_customer_products_id` | `serial` | PK · auto · NOT NULL |
| `rate` | `numeric` |  |

**Indexes:**
- `history_customer_products_pkey` — UNIQUE (history_customer_products_id)
- `history_customer_products_archive_date_idx` — (id, archive_date)
- `history_customer_products_id` — (id)
- `history_customer_products_modified_idx` — (id, modified_by, archive_date)

**Sample rows (3):**

| id | customers_id | customer_product_idnum | products_model | products_name | products_status_id | cancellation_category | cancellation_comments | products_nickname | service_type_id | modified_by | archive_date | mrc | setup | billable | currency | product_line_id | exchange_rate | history_customer_products_id | rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4177576 | 7012699 | 9 | CA3CG1EVNTPRE01 | Mission Critical Cloud | 32 | NULL |  | CA3CG1EVNTPRE01 | 21 | 956742 | 2019-11-03 13:17:04.209925-05:00 | 0.00000 | 0.00 | True | USD | 5 | 1.0000000 | 167706017 | NULL |
| 4979964 | 7012699 | 33 | CA3CG1QQPROD01 | Mission Critical Cloud | 32 | NULL |  | CA3CG1QQPROD01 | 21 | 956742 | 2019-11-03 13:17:04.744122-05:00 | 0.00000 | 0.00 | True | USD | 5 | 1.0000000 | 167706018 | NULL |
| 3965898 | 7012699 | 6 | CA3CG1REPORTR01 | Mission Critical Cloud | 32 | NULL |  | CA3CG1REPORTR01 | 21 | 956742 | 2019-11-03 13:17:05.244701-05:00 | 0.00000 | 0.00 | True | USD | 5 | 1.0000000 | 167706019 | NULL |

---

### `product_lines`

**Status:** ✅ accessible  
**Row count:** ~8  

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(255)` | NOT NULL |
| `in_order_entry` | `bool` | NOT NULL |
| `in_shopping_cart` | `bool` | NOT NULL |
| `abbr` | `varchar(64)` |  |

**Indexes:**
- `product_lines_pkey` — UNIQUE (id)
- `product_lines_name_key` — UNIQUE (name)

**Referenced by:** `client_relations`.`product_line_id`, `contract_types`.`product_line_id`, `customer_products`.`product_line_id`, `customer_support_faq_product_lines`.`product_line_id`, `employee_client_relations_roles_matrix`.`product_line_id`, `order_line_items`.`product_line_id`, `pricebook`.`product_line_id`, `product_class_client_type_discounts`.`product_line`, `product_class_contract_length_discounts`.`product_line`, `service_workflow_matrix`.`product_line_id`, `xref_ticket_routing_by_product_line`.`product_line_id`  

**Sample rows (3):**

| id | name | in_order_entry | in_shopping_cart | abbr |
| --- | --- | --- | --- | --- |
| 1 | Colocation | True | False | Colo |
| 2 | Network | False | False | Net |
| 3 | Managed Hosting | True | False | MH |

---

### `service_billing_details`

**Status:** ✅ accessible  
**Row count:** ~162,382  

| Column | Type | Flags |
|--------|------|-------|
| `service_id` | `int4` | PK · NOT NULL · → customer_products.id |
| `contract_id` | `varchar(32)` |  |
| `billing_day` | `int4` |  |
| `billing_frequency` | `int4` | NOT NULL |
| `contract_length` | `int4` | NOT NULL · → contract_lengths.contract_length |
| `payment_method_id` | `int4` | → client_payment_methods.id |
| `purchase_order` | `varchar(32)` |  |
| `promotion_id` | `int4` | → promotions.id |
| `on_hold` | `bool` | NOT NULL |

**Indexes:**
- `service_billing_details_pkey` — UNIQUE (service_id)
- `service_billing_details_contract_id_key` — UNIQUE (service_id, contract_id)

**Sample rows (3):**

| service_id | contract_id | billing_day | billing_frequency | contract_length | payment_method_id | purchase_order | promotion_id | on_hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 282 | 0000532472 | 17 | 1 | 1 | 22137 | NULL | NULL | False |
| 1301 | 0000532457 | 13 | 1 | 1 | 21913 | NULL | NULL | False |
| 2529 | 0000532336 | 13 | 1 | 1 | 19637 | NULL | NULL | False |

---

### `xref_customer_products_dcc`

**Status:** ✅ accessible  
**Row count:** ~162,397  

| Column | Type | Flags |
|--------|------|-------|
| `customer_products_id` | `int4` | → customer_products.id |
| `datacenter_id` | `int4` | → sb_datacenter.id |
| `device_id` | `varchar(64)` |  |
| `id` | `serial` | PK · auto · NOT NULL |

**Indexes:**
- `xref_customer_products_dcc_pkey` — UNIQUE (id)
- `xref_customer_products_dcc_customer_products_id_key` — UNIQUE (customer_products_id, datacenter_id, device_id)
- `xref_customer_products_dcc_datacenter_idx` — (datacenter_id)
- `xref_customer_products_dcc_service_idx` — (customer_products_id)

**Sample rows (3):**

| customer_products_id | datacenter_id | device_id | id |
| --- | --- | --- | --- |
| 282 | 6 |  | 30874 |
| 1301 | 6 | NULL | 30946 |
| 2529 | 6 | NULL | 30868 |

---

### `customer_products_status`

_Not found in XML schema._

### `datacenter`

_Not found in XML schema._

### `service_types`

_Not found in XML schema._

## All Accessible Tables

The following 333 tables are accessible to `sb_readonly`.
Priority tables above are not repeated here.

| Table | XML Row Count | Live Estimate | Columns |
|-------|--------------|---------------|---------|
| `accountid_payment_method` | 7,884 | ~7,884 | 2 |
| `app_config` | 29 | ~29 | 7 |
| `attribute_groupings` | 35 | ~35 | 3 |
| `attribute_groups` | 7 | ~7 | 2 |
| `attributes` | 154 | ~154 | 3 |
| `billable_ticket_invoicing` | 6 | ~5 | 6 |
| `bu_alerts` | 8,628 | ~11,110 | 6 |
| `bu_alerts_change_hist` | 975 | ~2,496 | 4 |
| `bu_events` | 0 | ~0 | 9 |
| `bu_events_status` | 8 | ~8 | 2 |
| `bu_prices` | 125 | ~125 | 3 |
| `bu_usage` | 11,883,427 | ~18,325,188 | 7 |
| `byo_upsell` | 18 | ~18 | 3 |
| `capabilities` | 73 | ~73 | 3 |
| `cart` | 0 | ~0 | 14 |
| `cart_component_private_net` | 0 | ~0 | 2 |
| `cart_component_private_rack` | 0 | ~0 | 2 |
| `cart_components` | 0 | ~0 | 10 |
| `cart_default_removed_components` | 0 | ~0 | 4 |
| `cart_order` | 17 | ~17 | 9 |
| `cart_raid_array_drives` | 0 | ~0 | 2 |
| `cart_raid_arrays` | 0 | ~0 | 4 |
| `ce_pods` | 10 | ~10 | 2 |
| `certificate` | 2,374 | ~5,917 | 10 |
| `certificate_attributes` | 7,296 | ~17,368 | 9 |
| `certificate_company` | 2,375 | ~5,672 | 10 |
| `certificate_contacts` | 622 | ~867 | 26 |
| `client_bag_allowed_service_statuses` | 10 | ~10 | 1 |
| `client_bag_allowed_service_types` | 9 | ~9 | 1 |
| `client_bag_services` | 2,677 | ~8,170 | 3 |
| `client_bags` | 787 | ~1,119 | 9 |
| `client_error_statuses` | 86 | ~86 | 3 |
| `client_eula_acceptance` | 18,886 | ~20,512 | 6 |
| `client_firewall_vlan` | 501 | ~623 | 7 |
| `client_industries` | 10 | ~10 | 3 |
| `client_loadbalancer_vlan` | 0 | ~0 | 7 |
| `client_news` | 23 | ~23 | 5 |
| `client_notes` | 15,944 | ~19,766 | 6 |
| `client_order_statuses` | 30 | ~30 | 3 |
| `client_order_types` | 3 | ~3 | 2 |
| `client_orders` | 159,683 | ~273,370 | 17 |
| `client_orders_attributes` | 291,720 | ~287,257 | 9 |
| `client_payment_methods` | 96,485 | ~99,075 | 18 |
| `client_permission_roles` | 852,326 | ~1,948,738 | 7 |
| `client_permission_users` | 307 | ~750 | 7 |
| `client_private_net` | 1,103 | ~1,215 | 10 |
| `client_private_rack` | 131 | ~135 | 11 |
| `client_relations_product_line_independent` | 1,580 | ~1,325 | 4 |
| `client_solution_services` | 17,406 | ~44,683 | 5 |
| `client_solutions` | 13,912 | ~17,040 | 9 |
| `client_tax_registrations` | 785 | ~482 | 4 |
| `client_tax_schedules` | 8 | ~8 | 2 |
| `client_tickets` | 1,664,414 | ~2,074,880 | 10 |
| `client_tickets_attributes` | 81,559 | ~99,785 | 9 |
| `client_types_pl` | 19 | ~12 | 5 |
| `client_zones` | 160,284 | ~8,825 | 7 |
| `clients_watchers` | 1,117 | ~1,603 | 3 |
| `cloud_storage_attributes` | 927 | ~927 | 9 |
| `cloud_storage_bandwidth_types_pl` | 3 | ~3 | 3 |
| `cloud_storage_tiered_discounts` | 27 | ~27 | 8 |
| `communication_type` | 9 | ~9 | 2 |
| `company_type` | 10 | ~10 | 2 |
| `component_capabilities` | 1,145 | ~2,711 | 7 |
| `component_categories` | 19 | ~18 | 5 |
| `component_hashes` | 4 | ~4 | 3 |
| `component_license_key_node_data` | 181 | ~390 | 3 |
| `component_license_keys` | 108 | ~227 | 4 |
| `component_provided_resources` | 665 | ~1,120 | 10 |
| `component_required_resources` | 529 | ~684 | 13 |
| `component_type_capabilities` | 106 | ~105 | 5 |
| `component_types` | 378 | ~386 | 7 |
| `component_workorder_templates` | 74 | ~116 | 3 |
| `components` | 3,634 | ~5,876 | 9 |
| `components_attributes` | 370 | ~445 | 11 |
| `config_code_components` | 6,401 | ~6,401 | 5 |
| `config_code_pnet` | 66 | ~66 | 3 |
| `config_code_raid_array_drives` | 493 | ~493 | 2 |
| `config_code_raid_arrays` | 219 | ~219 | 4 |
| `config_codes` | 581 | ~581 | 11 |
| `contact` | 72,386 | ~74,979 | 26 |
| `contact_attribute` | 127,350 | ~95,759 | 10 |
| `contact_attribute_history` | 373,107 | ~529,079 | 10 |
| `contact_communication_method` | 158,612 | ~168,955 | 5 |
| `contact_communication_method_bkup` | 12 | ~119 | 5 |
| `contact_role` | 96,207 | ~107,093 | 3 |
| `contact_role_type` | 9 | ~9 | 2 |
| `contract_lengths` | 6 | ~6 | 1 |
| `contract_types` | 1,688 | ~1,724 | 6 |
| `countries` | 247 | ~247 | 5 |
| `countries_currencies` | 7 | ~7 | 2 |
| `countries_intergovernmental_organizations` | 151 | ~151 | 2 |
| `credit_card_types` | 4 | ~4 | 5 |
| `currencies` | 4 | ~4 | 7 |
| `customer_products_attributes` | 59,304 | ~114,006 | 11 |
| `customer_products_mercury_services` | 805 | ~3,228 | 4 |
| `customer_products_status_history` | 1,178,689 | ~1,514,021 | 5 |
| `customer_products_status_options` | 13 | ~13 | 3 |
| `customer_support_faq` | 272 | ~272 | 6 |
| `customer_support_faq_product_lines` | 423 | ~425 | 3 |
| `customer_support_faq_tags` | 559 | ~560 | 3 |
| `customer_support_faq_type` | 37 | ~36 | 3 |
| `customer_support_handler` | 218 | ~206 | 2 |
| `customer_support_sub_type` | 329 | ~330 | 3 |
| `customer_support_type` | 112 | ~62 | 2 |
| `customer_tam` | 518 | ~193 | 4 |
| `customers_attributes` | 111,042 | ~127,364 | 11 |
| `customers_attributes_history` | 378,777 | ~485,984 | 11 |
| `customers_priority` | 4 | ~4 | 2 |
| `database_errors` | 803,064 | ~824,313 | 8 |
| `databasechangelog` | 178 | ~184 | 11 |
| `databasechangeloglock` | 1 | ~1 | 4 |
| `datacenter_attributes` | 244 | ~248 | 9 |
| `datacenter_available_currencies` | 70 | ~73 | 2 |
| `email_recipients` | 212 | ~245 | 5 |
| `email_template_groupings` | 52 | ~119 | 3 |
| `email_template_groups` | 5 | ~5 | 2 |
| `email_templates` | 209 | ~238 | 6 |
| `employee_client_relations_quotas` | 400 | ~192 | 16 |
| `employee_client_relations_roles_matrix` | 304 | ~103 | 6 |
| `employee_client_relations_roles_product_line_independent_matrix` | 12 | ~4 | 3 |
| `error_status_types` | 2 | ~2 | 2 |
| `error_statuses` | 2 | ~2 | 3 |
| `eula` | 610 | ~5 | 7 |
| `fraud_gateway_transactions` | 22,468 | ~45,577 | 8 |
| `history_certificate` | 7,925 | ~31,373 | 13 |
| `history_client_bag_services` | 247,509 | ~323,986 | 6 |
| `history_client_bags` | 623,014 | ~629,951 | 12 |
| `history_client_orders` | 10,940,129 | ~9,355,367 | 9 |
| `history_client_payment_methods` | 294,637 | ~488,274 | 20 |
| `history_client_permission_roles` | 1,440,502 | ~10,051,468 | 10 |
| `history_client_permission_users` | 1,159 | ~6,144 | 10 |
| `history_client_private_net` | 3,772 | ~4,198 | 13 |
| `history_client_private_rack` | 284 | ~313 | 14 |
| `history_client_solution_services` | 172,182 | ~661,702 | 5 |
| `history_client_solutions` | 44,186 | ~59,311 | 12 |
| `history_client_zones` | 343,918 | ~527,243 | 9 |
| `history_components` | 16,047 | ~30,101 | 11 |
| `history_contact` | 221,493 | ~387,329 | 26 |
| `history_contact_communication_method` | 886,832 | ~1,081,046 | 8 |
| `history_contact_role` | 361,650 | ~651,681 | 6 |
| `history_customers` | 81,974 | ~244,134 | 18 |
| `history_email_recipients` | 2,076 | ~3,695 | 8 |
| `history_email_templates` | 8,422 | ~2,006 | 9 |
| `history_exchange_rates` | 225 | ~320 | 8 |
| `history_ocean_restrictions` | 825 | ~802 | 7 |
| `history_permission_categories` | 12 | ~12 | 10 |
| `history_permissions` | 136 | ~136 | 12 |
| `history_preconfigured_bundle_mapping` | 220 | ~220 | 4 |
| `history_pricebook` | 50,476 | ~93,467 | 15 |
| `history_product_allowed_components` | 421,578 | ~483,025 | 10 |
| `history_product_catalog` | 14,934 | ~8,879 | 12 |
| `history_service_billing_details` | 435,849 | ~636,855 | 12 |
| `history_service_inventory_unavailable` | 505 | ~504 | 9 |
| `history_service_options` | 3,890,811 | ~6,127,824 | 20 |
| `history_tax_rates` | 106 | ~111 | 9 |
| `history_template_permission_roles` | 6,730 | ~406 | 9 |
| `history_ticket_support_times` | 1,391,530 | ~2,038,556 | 11 |
| `history_volume_discount_percentage` | 46 | ~38 | 10 |
| `history_workflow_notifications` | 51,158 | ~66,573 | 9 |
| `history_xref_customer_products_dcc` | 249,484 | ~371,492 | 6 |
| `history_xref_services_private_net` | 20,109 | ~27,011 | 10 |
| `history_xref_services_private_rack` | 4,590 | ~5,746 | 10 |
| `intergovernmental_organizations` | 3 | ~3 | 3 |
| `item_tax_schedule` | 5,747 | ~5,756 | 11 |
| `kickstart_component_keys` | 668 | ~1,234 | 8 |
| `license_types` | 8 | ~8 | 4 |
| `line_sequence_mapping` | 46,429 | ~46,429 | 2 |
| `login_history` | 3,020,280 | ~3,808,951 | 7 |
| `message_box` | 727,718 | ~1,609,695 | 3 |
| `mon_runbook_custom_notes` | 69 | ~169 | 5 |
| `mon_runbook_default_notes` | 61 | ~61 | 3 |
| `my_rbac_pages` | 277 | ~263 | 5 |
| `my_rbac_sections` | 16 | ~15 | 2 |
| `nbt_invoices` | 5,317 | ~5,317 | 7 |
| `node_types` | 2 | ~2 | 2 |
| `ocean_config` | 2 | ~2 | 5 |
| `ocean_restrictions` | 246 | ~269 | 4 |
| `ocean_sessions` | 402 | ~7,291 | 7 |
| `olid_service_option_link` | 22,020 | ~263,880 | 4 |
| `options_licenses` | 2,374 | ~5,917 | 4 |
| `order_commission_split` | 35,660 | ~69,202 | 4 |
| `order_communications` | 23,247 | ~40,626 | 5 |
| `order_entry_solution_link` | 3,048 | ~12,572 | 3 |
| `order_entry_solution_node` | 3,659 | ~11,283 | 2 |
| `order_line_item_attributes` | 31,373 | ~98,941 | 4 |
| `order_line_item_detail_attributes` | 175,056 | ~449,045 | 6 |
| `order_line_item_detail_workorder_tickets` | 1,881 | ~11,366 | 4 |
| `order_line_item_details` | 2,956,865 | ~5,390,359 | 21 |
| `order_line_item_migrated_services` | 14,461 | ~27,850 | 2 |
| `order_line_item_types` | 4 | ~4 | 2 |
| `order_line_item_workorder_tickets` | 865 | ~4,734 | 4 |
| `order_line_items` | 219,638 | ~375,211 | 37 |
| `order_notes` | 0 | ~0 | 5 |
| `p1_zones` | 396 | ~395 | 1 |
| `package` | 0 | ~0 | 7 |
| `partition_details` | 20,198 | ~55,051 | 14 |
| `partition_object_types` | 2 | ~2 | 2 |
| `partitions` | 5,254 | ~18,146 | 8 |
| `payment_gateway_providers` | 3 | ~3 | 3 |
| `payment_gateway_transaction_log_details` | 28 | ~28 | 4 |
| `payment_gateway_transaction_logs` | 14 | ~14 | 2 |
| `payment_merchant_accounts` | 28 | ~25 | 14 |
| `payment_terms` | 11 | ~11 | 1 |
| `payment_transaction_documents` | 1,737,227 | ~2,185,546 | 6 |
| `payment_transactions` | 1,680,635 | ~2,081,949 | 31 |
| `payment_transactions_paypal` | 0 | ~0 | 7 |
| `payment_types` | 6 | ~6 | 6 |
| `permission_categories` | 4 | ~4 | 7 |
| `permissions` | 58 | ~58 | 9 |
| `portal_login` | 107,309 | ~204,312 | 5 |
| `preconfigured_bundle_categories` | 6 | ~6 | 6 |
| `preconfigured_bundle_mapping` | 216 | ~216 | 11 |
| `pricebook` | 22,002 | ~43,198 | 12 |
| `product_allowed_components` | 157,911 | ~233,576 | 6 |
| `product_catalog` | 947 | ~1,148 | 17 |
| `product_catalog_attributes` | 178 | ~228 | 11 |
| `product_categories` | 10 | ~10 | 7 |
| `product_class_client_type_discounts` | 2,402 | ~1,857 | 7 |
| `product_class_contract_length_discounts` | 492 | ~918 | 7 |
| `product_classes` | 20 | ~20 | 5 |
| `product_configuration_changesets` | 689 | ~689 | 8 |
| `product_configurations` | 76 | ~72 | 7 |
| `product_frameworks` | 16,572 | ~23,482 | 5 |
| `product_templates` | 3,440 | ~4,539 | 5 |
| `promotion_component_criteria` | 2 | ~2 | 7 |
| `promotion_component_type_criteria` | 2 | ~1 | 7 |
| `promotion_component_types` | 5 | ~5 | 2 |
| `promotion_contract_length_criteria` | 2 | ~2 | 7 |
| `promotion_criteria_types` | 7 | ~7 | 3 |
| `promotion_customer_type_criteria` | 11 | ~10 | 7 |
| `promotion_effect_amounts` | 2,098 | ~2,094 | 5 |
| `promotion_effect_component_criteria` | 3 | ~3 | 7 |
| `promotion_effect_component_type_criteria` | 0 | ~0 | 7 |
| `promotion_effect_product_class_criteria` | 0 | ~0 | 7 |
| `promotion_effect_product_criteria` | 0 | ~0 | 7 |
| `promotion_effect_target_amount_types` | 3 | ~3 | 2 |
| `promotion_effect_target_types` | 3 | ~3 | 2 |
| `promotion_effect_types` | 4 | ~4 | 2 |
| `promotion_effects` | 1,412 | ~1,411 | 6 |
| `promotion_location_criteria` | 41 | ~42 | 7 |
| `promotion_product_class_criteria` | 22 | ~20 | 7 |
| `promotion_product_classes` | 98 | ~98 | 2 |
| `promotion_product_criteria` | 42 | ~42 | 7 |
| `promotion_types` | 2 | ~2 | 3 |
| `promotions` | 144 | ~155 | 10 |
| `provisioning_tickets` | 6,730 | ~5,216 | 4 |
| `queue_messages` | 732,462 | ~1,712,439 | 5 |
| `queues` | 68 | ~68 | 3 |
| `raid_levels` | 11 | ~11 | 6 |
| `resource_use_operators` | 6 | ~6 | 3 |
| `resource_use_types` | 2 | ~2 | 3 |
| `resources` | 35 | ~35 | 4 |
| `roles` | 20,005 | ~23,119 | 3 |
| `rss_feed_spotlight` | 0 | ~0 | 4 |
| `rss_feeds` | 0 | ~0 | 6 |
| `sb_customer_log` | 4,281,240 | ~6,316,303 | 7 |
| `sb_customer_product_log` | 5,261,389 | ~9,703,099 | 7 |
| `sb_datacenter` | 54 | ~54 | 8 |
| `sb_log_type` | 16 | ~16 | 2 |
| `secret_questions_pl` | 5 | ~5 | 2 |
| `service_account` | 0 | ~0 | 5 |
| `service_cancellation_queue` | 2 | ~131 | 6 |
| `service_inventory_unavailable` | 312 | ~312 | 4 |
| `service_licenses` | 4,222 | ~1,158 | 4 |
| `service_notes` | 186,275 | ~295,267 | 5 |
| `service_option_raid_arrays` | 21,753 | ~42,499 | 3 |
| `service_option_raid_configuration` | 56,082 | ~103,935 | 4 |
| `service_option_types_pl` | 51 | ~51 | 5 |
| `service_options` | 1,431,529 | ~1,850,910 | 17 |
| `service_options_attributes` | 7,001 | ~9,363 | 11 |
| `service_options_mercury_services` | 505 | ~1,646 | 4 |
| `service_type_capabilities` | 6 | ~6 | 3 |
| `service_type_pl` | 22 | ~22 | 5 |
| `service_workflow_matrix` | 380 | ~351 | 9 |
| `sessions` | 43 | ~3,186 | 5 |
| `solution_connection_property_types` | 3 | ~3 | 2 |
| `solution_service_connection_properties` | 0 | ~0 | 4 |
| `solution_service_connections` | 79 | ~14,971 | 7 |
| `task_status_pl` | 6 | ~6 | 5 |
| `tax_rates` | 45 | ~45 | 7 |
| `tax_registration_types` | 3 | ~3 | 5 |
| `template_permission_roles` | 158 | ~186 | 6 |
| `ticket_support_time_types` | 4 | ~4 | 5 |
| `ticket_support_times` | 1,391,493 | ~2,038,533 | 9 |
| `tls_workorder_templates` | 23 | ~22 | 3 |
| `transactions_pending_client_approval` | 3 | ~0 | 5 |
| `unit_of_measure` | 30 | ~30 | 5 |
| `vam_admin_account` | 976 | ~973 | 5 |
| `vam_agent` | 2,789 | ~2,786 | 4 |
| `vam_agent_account` | 2,900 | ~2,896 | 5 |
| `vam_billing_account` | 978 | ~976 | 5 |
| `vam_cache` | 11,626 | ~11,623 | 5 |
| `vam_client` | 980 | ~979 | 4 |
| `vam_configuration` | 2,786 | ~2,786 | 4 |
| `vam_escalation_definition` | 2,785 | ~2,785 | 4 |
| `vam_host` | 2,909 | ~2,908 | 5 |
| `vam_resources` | 12 | ~12 | 5 |
| `vmware_clusters` | 182 | ~418 | 3 |
| `vmware_guests` | 2,126 | ~4,338 | 3 |
| `vmware_hosts` | 530 | ~1,056 | 3 |
| `vmware_vcenters` | 218 | ~497 | 2 |
| `volume_discount_percentage` | 22 | ~20 | 7 |
| `wallet_responses_pl` | 20 | ~20 | 2 |
| `web_server_types` | 27 | ~27 | 3 |
| `widget_input_parameters` | 321 | ~321 | 5 |
| `widget_output_parameters` | 357 | ~357 | 5 |
| `widget_transaction_states` | 0 | ~0 | 3 |
| `widget_types_pl` | 42 | ~42 | 5 |
| `widgets` | 187 | ~187 | 10 |
| `workflow_event_types` | 16 | ~16 | 4 |
| `workflow_notifications` | 0 | ~0 | 8 |
| `xref_cloud_storage_policy_component` | 10 | ~10 | 5 |
| `xref_cloud_storage_policy_concession` | 1 | ~1 | 8 |
| `xref_cloud_storage_subtenants_services` | 1,095 | ~1,111 | 3 |
| `xref_customer_rbac_roles` | 1,040,881 | ~1,090,638 | 4 |
| `xref_customer_support_type_sub_type` | 430 | ~435 | 9 |
| `xref_rbac_pages_to_sections` | 248 | ~218 | 3 |
| `xref_roles_employees` | 15,262 | ~10,736 | 3 |
| `xref_services_private_net` | 14,869 | ~20,078 | 7 |
| `xref_services_private_rack` | 3,376 | ~3,584 | 7 |
| `xref_ticket_routing_by_product_line` | 688 | ~713 | 3 |
| `zones` | 739 | ~736 | 4 |

### Column Detail — Accessible Non-Priority Tables

#### `accountid_payment_method`

| Column | Type | Flags |
|--------|------|-------|
| `accountid` | `int4` | PK · NOT NULL |
| `payment_method_id` | `int4` |  |

#### `app_config`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar` |  |
| `type` | `varchar` |  |
| `default_value` | `varchar` |  |
| `value` | `varchar` |  |
| `created` | `timestamp` |  |
| `version` | `varchar(4)` |  |

#### `attribute_groupings`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `attribute_group_id` | `int4` | NOT NULL · → attribute_groups.id |
| `attribute_id` | `int4` | NOT NULL · → attributes.id |

#### `attribute_groups`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(500)` | NOT NULL |

#### `attributes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(500)` | NOT NULL |
| `data_type` | `varchar(500)` | NOT NULL |

#### `billable_ticket_invoicing`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `client_id` | `int4` | → customers.customers_id |
| `ticket_id` | `int4` |  |
| `username` | `text` | → employees.username |
| `bill_amount` | `float8` |  |
| `original_estimate` | `float8` |  |

#### `bu_alerts`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `node_name` | `varchar(128)` |  |
| `threshold` | `int4` |  |
| `status` | `varchar(128)` |  |
| `customer_products_id` | `int4` |  |
| `email` | `text` |  |

#### `bu_alerts_change_hist`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `alert_id` | `int4` |  |
| `description` | `varchar(128)` |  |
| `dt_stamp` | `date` |  |

#### `bu_events`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `node_name` | `varchar(128)` |  |
| `schedule_start` | `timestamp` |  |
| `actual_start` | `timestamp` |  |
| `actual_finish` | `timestamp` |  |
| `total_time` | `time` |  |
| `status_id` | `int4` |  |
| `node_type_id` | `int4` |  |
| `customer_products_id` | `int4` |  |

#### `bu_events_status`

| Column | Type | Flags |
|--------|------|-------|
| `status_id` | `int4` | PK · NOT NULL |
| `description` | `varchar(32)` | NOT NULL |

#### `bu_prices`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `service_options_id` | `int4` |  |
| `price_per_gig` | `float8` |  |

#### `bu_usage`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `node_name` | `varchar(128)` |  |
| `total_files_stored` | `int4` |  |
| `total_mbs_stored` | `numeric` |  |
| `dt_stamp` | `date` |  |
| `node_type_id` | `int4` |  |
| `customer_products_id` | `int4` |  |

#### `byo_upsell`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `product_id` | `int4` | NOT NULL · → product_catalog.id |
| `upsell_product_id` | `int4` | NOT NULL · → product_catalog.id |

#### `capabilities`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(64)` | NOT NULL |
| `capability_type_id` | `int4` |  |

#### `cart`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `session_id` | `bpchar` | NOT NULL · → sessions.session_id |
| `product_id` | `int4` | → product_catalog.id |
| `datacenter_id` | `int4` | → sb_datacenter.id |
| `contract_length` | `int4` | NOT NULL · → contract_lengths.contract_length |
| `fqdn` | `varchar(128)` |  |
| `setup` | `numeric` | NOT NULL |
| `mrc` | `numeric` | NOT NULL |
| `functional_currency` | `varchar(3)` | NOT NULL · → currencies.code |
| `promotion_id` | `int4` | → promotions.id |
| `setup_discount` | `numeric` |  |
| `mrc_discount` | `numeric` |  |
| `originating_currency` | `varchar(3)` | NOT NULL · → currencies.code |
| `assisted_by` | `int4` | → employees.id |

#### `cart_component_private_net`

| Column | Type | Flags |
|--------|------|-------|
| `cart_component_id` | `int4` | PK · NOT NULL · → cart_components.id |
| `alias` | `varchar(255)` | NOT NULL |

#### `cart_component_private_rack`

| Column | Type | Flags |
|--------|------|-------|
| `cart_component_id` | `int4` | PK · NOT NULL · → cart_components.id |
| `alias` | `varchar(255)` |  |

#### `cart_components`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `cart_id` | `int4` | NOT NULL · → cart.id |
| `component_id` | `int4` | → components.id |
| `setup` | `numeric` | NOT NULL |
| `nrc` | `numeric` |  |
| `mrc` | `numeric` |  |
| `setup_discount` | `numeric` |  |
| `nrc_discount` | `numeric` |  |
| `mrc_discount` | `numeric` |  |
| `is_default` | `bool` | NOT NULL |

#### `cart_default_removed_components`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` | PK · NOT NULL |
| `cart_id` | `int4` | → cart.id |
| `component_id` | `int4` | → components.id |
| `mrc` | `numeric` | NOT NULL |

#### `cart_order`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(64)` |  |
| `description` | `text` |  |
| `page` | `int4` |  |
| `sort_order` | `int4` |  |
| `display_type` | `varchar(16)` | NOT NULL |
| `unselect_text` | `varchar(64)` |  |
| `editable` | `bool` | NOT NULL |
| `component_type` | `int4` | → component_types.id |

#### `cart_raid_array_drives`

| Column | Type | Flags |
|--------|------|-------|
| `array_id` | `int4` | PK · NOT NULL · → cart_raid_arrays.id |
| `drive_id` | `int4` | PK · NOT NULL · → cart_components.id |

#### `cart_raid_arrays`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `cart_id` | `int4` | → cart.id |
| `level` | `int4` | → raid_levels.id |
| `array_name` | `varchar(32)` |  |

#### `ce_pods`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | auto · NOT NULL |
| `value` | `varchar(25)` | NOT NULL |

#### `certificate`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `options_licenses_id` | `int4` | NOT NULL · → options_licenses.id |
| `certificate_contact_id` | `int4` | → certificate_contacts.contact_id |
| `certificate_company_id` | `int4` | → certificate_company.id |
| `status` | `varchar(255)` | NOT NULL |
| `domain` | `text` |  |
| `os` | `varchar(32)` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `text` |  |

#### `certificate_attributes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `certificate_id` | `int4` | NOT NULL · → certificate.id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `attribute_id` | `int4` | NOT NULL |
| `attribute_group_id` | `int4` |  |
| `value` | `text` |  |

#### `certificate_company`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `customers_id` | `int4` | NOT NULL · → customers.customers_id |
| `legal_company_name` | `varchar(255)` |  |
| `duns_number` | `text` |  |
| `street_address` | `text` |  |
| `city` | `text` |  |
| `state` | `text` |  |
| `postal_code` | `text` |  |
| `countries_id` | `int4` | → countries.countries_id |
| `company_type_id` | `int4` | → company_type.id |

#### `certificate_contacts`

| Column | Type | Flags |
|--------|------|-------|
| `contact_id` | `serial` | PK · auto · NOT NULL |
| `customers_id` | `int4` | NOT NULL |
| `company` | `text` |  |
| `first_name` | `text` | NOT NULL |
| `last_name` | `text` | NOT NULL |
| `street_address1` | `text` |  |
| `street_address2` | `text` |  |
| `street_address3` | `text` |  |
| `postcode` | `text` |  |
| `city` | `text` |  |
| `country_id` | `int4` |  |
| `zone_id` | `int4` |  |
| `username` | `varchar(64)` |  |
| `password` | `text` |  |
| `security_question` | `varchar(255)` |  |
| `security_answer` | `text` |  |
| `subscribed` | `bool` |  |
| `is_disabled` | `bool` |  |
| `portal_user` | `bool` |  |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` |  |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` |  |
| `full_name` | `text` |  |
| `title` | `text` |  |
| `department` | `text` |  |

#### `client_bag_allowed_service_statuses`

| Column | Type | Flags |
|--------|------|-------|
| `service_status_id` | `int4` | PK · NOT NULL · → customer_products_status_options.id |

#### `client_bag_allowed_service_types`

| Column | Type | Flags |
|--------|------|-------|
| `service_type_id` | `int4` | PK · NOT NULL · → service_type_pl.service_type_id |

#### `client_bag_services`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `client_bag_id` | `int4` | NOT NULL · → client_bags.id |
| `service_id` | `int4` | NOT NULL · → customer_products.id |

#### `client_bags`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `client_id` | `int4` | NOT NULL · → customers.customers_id |
| `name` | `varchar(64)` | NOT NULL |
| `description` | `text` |  |
| `is_active` | `bool` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `client_error_statuses`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `client_id` | `int4` | → customers.customers_id |
| `error_status_id` | `int4` | → error_statuses.id |

#### `client_eula_acceptance`

| Column | Type | Flags |
|--------|------|-------|
| `client_id` | `int4` | PK · NOT NULL · → customers.customers_id |
| `eula_id` | `int4` | NOT NULL · → eula.id |
| `digital_signature` | `varchar(16)` | PK · NOT NULL |
| `date_accepted` | `timestamp` |  |
| `ip_address` | `varchar(50)` |  |
| `user_agent` | `text` |  |

#### `client_firewall_vlan`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `service_id` | `int4` | → customer_products.id |
| `vlan_id` | `int4` |  |
| `created` | `timestamptz` |  |
| `created_by` | `text` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `text` |  |

#### `client_industries`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(64)` | NOT NULL |
| `active` | `bool` |  |

#### `client_loadbalancer_vlan`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `service_id` | `int4` | → customer_products.id |
| `vlan_id` | `int4` |  |
| `created` | `timestamptz` |  |
| `created_by` | `text` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `text` |  |

#### `client_news`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `title` | `varchar(64)` |  |
| `description` | `varchar` |  |
| `created` | `timestamptz` | NOT NULL |
| `who` | `int4` | → employees.id |

#### `client_notes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `client_id` | `int4` | NOT NULL · → customers.customers_id |
| `message` | `varchar` | NOT NULL |
| `date` | `timestamptz` | NOT NULL |
| `who` | `varchar(32)` | NOT NULL |
| `is_important` | `bool` | NOT NULL |

#### `client_order_statuses`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(64)` | NOT NULL |
| `description` | `varchar(256)` |  |

#### `client_order_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(32)` | NOT NULL |

#### `client_orders`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `client_id` | `int4` | → customers.customers_id |
| `status` | `int4` | → client_order_statuses.id |
| `entered_by` | `text` | → employees.username |
| `date` | `timestamptz` |  |
| `message` | `varchar` |  |
| `order_type_id` | `int4` | NOT NULL · → client_order_types.id |
| `currency` | `varchar(3)` | NOT NULL · → currencies.code |
| `short_term` | `int4` |  |
| `release_date` | `date` |  |
| `sla_days` | `int4` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `text` |  |
| `one_off` | `bool` |  |
| `effective_date` | `date` |  |
| `is_qtc` | `bool` |  |
| `track_removals` | `bool` | NOT NULL |

#### `client_orders_attributes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `object_id` | `int4` | NOT NULL · → client_orders.id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `attribute_id` | `int4` | NOT NULL · → attributes.id |
| `attribute_group_id` | `int4` |  |
| `value` | `text` |  |

#### `client_payment_methods`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `client_id` | `int4` | → customers.customers_id |
| `payment_type_id` | `int4` | NOT NULL · → payment_types.id |
| `wallet_id` | `varchar(256)` | NOT NULL |
| `is_active` | `bool` | NOT NULL |
| `display_info` | `varchar(32)` | NOT NULL |
| `code` | `int4` | → wallet_responses_pl.code |
| `response` | `varchar` |  |
| `created` | `timestamptz` |  |
| `auth_code` | `varchar` |  |
| `transaction_id` | `varchar` |  |
| `message_id` | `varchar` |  |
| `message_text` | `varchar` |  |
| `transaction_date` | `varchar` |  |
| `disabled` | `bool` |  |
| `disabled_reason` | `varchar(256)` |  |
| `card_type` | `varchar` |  |
| `fraud_review_required` | `bool` |  |

#### `client_permission_roles`

| Column | Type | Flags |
|--------|------|-------|
| `client_id` | `int4` | PK · NOT NULL · → customers.customers_id |
| `permissions_id` | `varchar(32)` | PK · NOT NULL · → permissions.permissions_id |
| `contact_role_type_id` | `int4` | PK · NOT NULL · → contact_role_type.contact_role_type_id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `client_permission_users`

| Column | Type | Flags |
|--------|------|-------|
| `client_id` | `int4` | PK · NOT NULL · → customers.customers_id |
| `permissions_id` | `varchar(32)` | PK · NOT NULL · → permissions.permissions_id |
| `contact_id` | `int4` | PK · NOT NULL · → contact.contact_id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `client_private_net`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `client_id` | `int4` | NOT NULL · → customers.customers_id |
| `vlan_id` | `int4` |  |
| `alias` | `text` | NOT NULL |
| `datacenter_id` | `int4` | NOT NULL · → sb_datacenter.id |
| `netmask` | `int4` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `text` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `text` | NOT NULL |

#### `client_private_rack`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `client_id` | `int4` | NOT NULL · → customers.customers_id |
| `service_id` | `int4` | NOT NULL · → customer_products.id |
| `vlan_id` | `int4` |  |
| `alias` | `text` | NOT NULL |
| `datacenter_id` | `int4` | NOT NULL · → sb_datacenter.id |
| `netmask` | `int4` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `text` | NOT NULL |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `text` | NOT NULL |

#### `client_relations_product_line_independent`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `client_id` | `int4` | NOT NULL · → customers.customers_id |
| `employee_id` | `int4` | NOT NULL · → employees.id |
| `client_relations_role_id` | `int4` | NOT NULL · → client_relations_roles.id |

#### `client_solution_services`

| Column | Type | Flags |
|--------|------|-------|
| `client_solution_id` | `int4` | NOT NULL · → client_solutions.id |
| `service_id` | `int4` | NOT NULL · → customer_products.id |
| `x` | `int4` |  |
| `y` | `int4` |  |
| `id` | `serial` | PK · auto · NOT NULL |

#### `client_solutions`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `client_id` | `int4` | NOT NULL · → customers.customers_id |
| `name` | `varchar(64)` | NOT NULL |
| `description` | `text` |  |
| `attachment` | `varchar` |  |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `client_tax_registrations`

| Column | Type | Flags |
|--------|------|-------|
| `client_id` | `int4` | PK · NOT NULL · → customers.customers_id |
| `tax_registration_type_id` | `varchar(16)` | PK · NOT NULL · → tax_registration_types.tax_registration_type_id |
| `tax_registration_value` | `varchar` | NOT NULL |
| `certificate_received` | `bool` | NOT NULL |

#### `client_tax_schedules`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `varbit` | PK · NOT NULL |
| `name` | `varchar(16)` | NOT NULL |

#### `client_tickets`

| Column | Type | Flags |
|--------|------|-------|
| `client_id` | `int4` | → customers.customers_id |
| `service_id` | `int4` | → customer_products.id |
| `ticket_id` | `int4` |  |
| `status` | `varchar(16)` |  |
| `location` | `varchar(64)` |  |
| `public` | `bool` |  |
| `subject` | `varchar(500)` |  |
| `created` | `timestamptz` |  |
| `last_updated` | `timestamptz` |  |
| `id` | `serial` | PK · auto · NOT NULL |

#### `client_tickets_attributes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `object_id` | `int4` | NOT NULL · → client_tickets.ticket_id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `attribute_id` | `int4` | NOT NULL · → attributes.id |
| `attribute_group_id` | `int4` |  |
| `value` | `text` |  |

#### `client_types_pl`

| Column | Type | Flags |
|--------|------|-------|
| `client_type_id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(64)` | NOT NULL |
| `description` | `varchar(255)` | NOT NULL |
| `sort_order` | `int4` |  |
| `is_active` | `bool` |  |

#### `client_zones`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `client_id` | `int4` | NOT NULL · → customers.customers_id |
| `zone` | `varchar(256)` | NOT NULL |
| `created` | `timestamp` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `clients_watchers`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `client_id` | `int4` | NOT NULL · → customers.customers_id |
| `employee_id` | `int4` | NOT NULL · → employees.id |

#### `cloud_storage_attributes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `object_id` | `int4` | NOT NULL · → customer_products.id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `attribute_id` | `int4` | NOT NULL · → attributes.id |
| `attribute_group_id` | `int4` |  |
| `value` | `text` |  |

#### `cloud_storage_bandwidth_types_pl`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(32)` | NOT NULL |
| `description` | `varchar(200)` |  |

#### `cloud_storage_tiered_discounts`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `tier` | `int4` |  |
| `discount_amount` | `float8` |  |
| `threshold` | `int4` |  |
| `unit_of_measure_id` | `int4` | → unit_of_measure.id |
| `name` | `varchar(64)` |  |
| `component_id` | `int4` | → components.id |
| `currency` | `varchar(4)` | → currencies.code |

#### `communication_type`

| Column | Type | Flags |
|--------|------|-------|
| `communication_type_id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(255)` |  |

#### `company_type`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `company_type` | `varchar(64)` | NOT NULL |

#### `component_capabilities`

| Column | Type | Flags |
|--------|------|-------|
| `component_id` | `int4` | PK · NOT NULL · → components.id |
| `component_type_capabilities_id` | `int4` | PK · NOT NULL · → component_type_capabilities.id |
| `value` | `text` | NOT NULL |
| `tolerance_min` | `text` |  |
| `tolerance_max` | `text` |  |
| `is_primary` | `bool` | NOT NULL |
| `match_required` | `bool` | NOT NULL |

#### `component_categories`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(32)` | NOT NULL |
| `description` | `varchar(256)` | NOT NULL |
| `sort_order` | `int4` | NOT NULL |
| `is_active` | `bool` | NOT NULL |

#### `component_hashes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `component_id` | `int4` | NOT NULL · → components.id |
| `hash` | `varchar` | NOT NULL |

#### `component_license_key_node_data`

| Column | Type | Flags |
|--------|------|-------|
| `component_license_key_id` | `int4` | PK · NOT NULL · → component_license_keys.id |
| `node_name` | `text` | PK · NOT NULL |
| `node_value` | `text` | NOT NULL |

#### `component_license_keys`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `component_id` | `int4` | NOT NULL · → components.id |
| `license_type_id` | `int4` | NOT NULL · → license_types.id |
| `base` | `bool` | NOT NULL |

#### `component_provided_resources`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `component_type_id` | `int4` | → component_types.id |
| `component_id` | `int4` | → components.id |
| `resource_id` | `int4` | NOT NULL · → resources.id |
| `resource_quantity` | `float8` | NOT NULL |
| `resource_stacking_priority` | `int4` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `component_required_resources`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `component_type_id` | `int4` | → component_types.id |
| `component_id` | `int4` | → components.id |
| `use_type_id` | `int4` | → resource_use_types.id |
| `resource_id` | `int4` | → resources.id |
| `operator` | `varchar(3)` | → resource_use_operators.operator |
| `resource_quantity` | `float8` | NOT NULL |
| `precheck` | `bool` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `message` | `text` |  |

#### `component_type_capabilities`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `component_type_id` | `int4` | NOT NULL · → component_types.id |
| `capabilities_id` | `int4` | NOT NULL · → capabilities.id |
| `datatype` | `text` | NOT NULL |
| `uom_id` | `int4` | → unit_of_measure.id |

#### `component_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `category_id` | `int4` | NOT NULL · → component_categories.id |
| `name` | `varchar(64)` | NOT NULL |
| `description` | `varchar(256)` | NOT NULL |
| `is_active` | `bool` | NOT NULL |
| `parent_component_id` | `int4` |  |
| `service_option_types_id` | `int4` | NOT NULL · → service_option_types_pl.service_option_types_id |

#### `component_workorder_templates`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `component_id` | `int4` | NOT NULL · → components.id |
| `workorder_template` | `text` |  |

#### `components`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(64)` | NOT NULL |
| `description` | `varchar(256)` |  |
| `is_active` | `bool` | NOT NULL |
| `modified_by` | `varchar(32)` | NOT NULL |
| `component_type_id` | `int4` | NOT NULL · → component_types.id |
| `cost` | `numeric` |  |
| `display_name` | `varchar(64)` | NOT NULL |
| `discountable` | `bool` | NOT NULL |

#### `components_attributes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `object_id` | `int4` | NOT NULL · → components.id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `attribute_id` | `int4` | NOT NULL · → attributes.id |
| `attribute_group_id` | `int4` |  |
| `value` | `text` |  |
| `visibility_group` | `varchar(255)` |  |
| `visibility_user` | `varchar(255)` |  |

#### `config_code_components`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `config_id` | `int4` | NOT NULL · → config_codes.id |
| `component_id` | `int4` | NOT NULL · → components.id |
| `is_default` | `bool` | NOT NULL |
| `removed_component_id` | `int4` | → components.id |

#### `config_code_pnet`

| Column | Type | Flags |
|--------|------|-------|
| `config_id` | `int4` | PK · NOT NULL · → config_codes.id |
| `config_component_id` | `int4` | PK · NOT NULL · → config_code_components.id |
| `alias` | `varchar(128)` | NOT NULL |

#### `config_code_raid_array_drives`

| Column | Type | Flags |
|--------|------|-------|
| `array_id` | `int4` | PK · NOT NULL · → config_code_raid_arrays.id |
| `drive_id` | `int4` | PK · NOT NULL |

#### `config_code_raid_arrays`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` | PK · NOT NULL |
| `config_id` | `int4` | → config_codes.id |
| `level` | `int4` | → raid_levels.id |
| `array_name` | `varchar(32)` |  |

#### `config_codes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `code` | `varchar(128)` | NOT NULL |
| `name` | `varchar(128)` | NOT NULL |
| `customer_id` | `int4` | NOT NULL · → customers.customers_id |
| `datacenter_id` | `int4` |  |
| `currency` | `varchar(3)` | NOT NULL |
| `contract_length` | `int4` | → contract_lengths.contract_length |
| `fqdn` | `varchar(128)` |  |
| `product_id` | `int4` | NOT NULL · → product_catalog.id |
| `is_saved` | `bool` | NOT NULL |
| `is_active` | `bool` | NOT NULL |

#### `contact`

| Column | Type | Flags |
|--------|------|-------|
| `contact_id` | `serial` | PK · auto · NOT NULL |
| `customers_id` | `int4` | NOT NULL · → customers.customers_id |
| `company` | `text` |  |
| `first_name` | `text` | NOT NULL |
| `last_name` | `text` | NOT NULL |
| `street_address1` | `text` |  |
| `street_address2` | `text` |  |
| `street_address3` | `text` |  |
| `postcode` | `text` |  |
| `city` | `text` |  |
| `country_id` | `int4` | → countries.countries_id |
| `zone_id` | `int4` | → zones.zone_id |
| `username` | `varchar(64)` |  |
| `password` | `text` |  |
| `security_question` | `varchar(255)` |  |
| `security_answer` | `text` |  |
| `subscribed` | `bool` |  |
| `is_disabled` | `bool` |  |
| `portal_user` | `bool` |  |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` |  |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` |  |
| `full_name` | `text` |  |
| `title` | `text` |  |
| `department` | `text` |  |

#### `contact_attribute`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `object_id` | `int4` | NOT NULL · → contact.contact_id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `attribute_id` | `int4` | NOT NULL · → attributes.id |
| `value` | `varchar(1024)` |  |
| `visibility_group` | `varchar(255)` |  |
| `visibility_user` | `varchar(255)` |  |

#### `contact_attribute_history`

| Column | Type | Flags |
|--------|------|-------|
| `contact_attributes_history_id` | `serial` | PK · auto · NOT NULL |
| `id` | `int4` | NOT NULL |
| `object_id` | `int4` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `attribute_id` | `int4` | NOT NULL |
| `value` | `varchar(1024)` |  |
| `last_action` | `varchar(64)` | NOT NULL |

#### `contact_communication_method`

| Column | Type | Flags |
|--------|------|-------|
| `contact_communication_id` | `serial` | PK · auto · NOT NULL |
| `contact_id` | `int4` | NOT NULL · → contact.contact_id |
| `communication_type_id` | `int4` | NOT NULL · → communication_type.communication_type_id |
| `value` | `text` |  |
| `is_primary` | `bool` |  |

#### `contact_communication_method_bkup`

| Column | Type | Flags |
|--------|------|-------|
| `contact_communication_id` | `int4` |  |
| `contact_id` | `int4` |  |
| `communication_type_id` | `int4` |  |
| `value` | `text` |  |
| `is_primary` | `bool` |  |

#### `contact_role`

| Column | Type | Flags |
|--------|------|-------|
| `contact_role_id` | `serial` | PK · auto · NOT NULL |
| `contact_id` | `int4` | → contact.contact_id |
| `contact_role_type_id` | `int4` | → contact_role_type.contact_role_type_id |

#### `contact_role_type`

| Column | Type | Flags |
|--------|------|-------|
| `contact_role_type_id` | `serial` | PK · auto · NOT NULL |
| `role_name` | `varchar(255)` |  |

#### `contract_lengths`

| Column | Type | Flags |
|--------|------|-------|
| `contract_length` | `int4` | PK · NOT NULL |

#### `contract_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `product_class_id` | `int4` | → product_classes.id |
| `component_category` | `int4` | → component_categories.id |
| `datacenter` | `int4` | NOT NULL · → sb_datacenter.id |
| `product_line_id` | `int4` | NOT NULL · → product_lines.id |
| `contract_type` | `varchar(16)` | NOT NULL |

#### `countries`

| Column | Type | Flags |
|--------|------|-------|
| `countries_id` | `serial` | PK · auto · NOT NULL |
| `countries_name` | `text` | NOT NULL |
| `countries_iso_code_2` | `bpchar` | NOT NULL |
| `countries_iso_code_3` | `bpchar` | NOT NULL |
| `address_format_id` | `int4` | NOT NULL |

#### `countries_currencies`

| Column | Type | Flags |
|--------|------|-------|
| `countries_id` | `int4` | PK · NOT NULL · → countries.countries_id |
| `currency_code` | `varchar(3)` | PK · NOT NULL · → currencies.code |

#### `countries_intergovernmental_organizations`

| Column | Type | Flags |
|--------|------|-------|
| `countries_id` | `int4` | PK · NOT NULL · → countries.countries_id |
| `igo_id` | `int4` | PK · NOT NULL · → intergovernmental_organizations.id |

#### `credit_card_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `display_name` | `varchar(100)` |  |
| `beanstream_value` | `varchar(10)` |  |
| `description` | `varchar(100)` |  |
| `is_active` | `varchar(100)` |  |

#### `currencies`

| Column | Type | Flags |
|--------|------|-------|
| `code` | `varchar(3)` | PK · NOT NULL |
| `currency_name` | `varchar(255)` | NOT NULL |
| `currency_symbol` | `varchar(16)` | NOT NULL |
| `thousands_separator` | `varchar(1)` | NOT NULL |
| `decimal_point` | `varchar(1)` | NOT NULL |
| `display_decimals` | `int4` | NOT NULL |
| `display_format` | `varchar(32)` |  |

#### `customer_products_attributes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `object_id` | `int4` | NOT NULL · → customer_products.id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `attribute_id` | `int4` | NOT NULL · → attributes.id |
| `attribute_group_id` | `int4` |  |
| `value` | `text` |  |
| `visibility_group` | `varchar(255)` |  |
| `visibility_user` | `varchar(255)` |  |

#### `customer_products_mercury_services`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `customer_products_id` | `int4` | NOT NULL |
| `service_num` | `int4` | NOT NULL |
| `order_line_item_id` | `int4` |  |

#### `customer_products_status_history`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `customer_product_id` | `int4` | → customer_products.id |
| `new_value` | `int4` | NOT NULL |
| `old_value` | `int4` |  |
| `date_added` | `timestamptz` | NOT NULL |

#### `customer_products_status_options`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `order_number` | `int4` | NOT NULL |
| `name` | `text` | NOT NULL |

#### `customer_support_faq`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `type_id` | `int4` | → customer_support_faq_type.id |
| `question` | `text` |  |
| `answer` | `text` |  |
| `order_number` | `int4` |  |
| `is_active` | `bool` | NOT NULL |

#### `customer_support_faq_product_lines`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `customer_support_faq_id` | `int4` | NOT NULL · → customer_support_faq.id |
| `product_line_id` | `int4` | NOT NULL · → product_lines.id |

#### `customer_support_faq_tags`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `customer_support_faq_id` | `int4` | NOT NULL · → customer_support_faq.id |
| `tag` | `text` | NOT NULL |

#### `customer_support_faq_type`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(128)` |  |
| `is_active` | `bool` | NOT NULL |

#### `customer_support_handler`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `text` | NOT NULL |

#### `customer_support_sub_type`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `text` | NOT NULL |
| `default_note` | `text` |  |

#### `customer_support_type`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `text` | NOT NULL |

#### `customer_tam`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `customers_id` | `int4` | → customers.customers_id |
| `employees_id` | `int4` | → employees.id |
| `created_date` | `timestamptz` |  |

#### `customers_attributes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `object_id` | `int4` | NOT NULL · → customers.customers_id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `attribute_id` | `int4` | NOT NULL · → attributes.id |
| `attribute_group_id` | `int4` |  |
| `value` | `text` |  |
| `visibility_group` | `varchar(255)` |  |
| `visibility_user` | `varchar(255)` |  |

#### `customers_attributes_history`

| Column | Type | Flags |
|--------|------|-------|
| `customers_attributes_history_id` | `serial` | PK · auto · NOT NULL |
| `id` | `int4` | NOT NULL |
| `object_id` | `int4` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `attribute_id` | `int4` | NOT NULL |
| `attribute_group_id` | `int4` |  |
| `value` | `text` |  |
| `last_action` | `text` |  |

#### `customers_priority`

| Column | Type | Flags |
|--------|------|-------|
| `customers_priority_id` | `serial` | PK · auto · NOT NULL |
| `customers_priority_name` | `varchar(32)` | NOT NULL |

#### `database_errors`

| Column | Type | Flags |
|--------|------|-------|
| `error_id` | `serial` | PK · auto · NOT NULL |
| `code` | `int4` | → wallet_responses_pl.code |
| `message` | `varchar` |  |
| `file` | `varchar` |  |
| `line` | `int4` |  |
| `context` | `varchar` |  |
| `source` | `varchar` |  |
| `created` | `timestamptz` |  |

#### `databasechangelog`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `varchar(255)` | NOT NULL |
| `author` | `varchar(255)` | NOT NULL |
| `filename` | `varchar(255)` | NOT NULL |
| `dateexecuted` | `timestamptz` | NOT NULL |
| `orderexecuted` | `int4` | NOT NULL |
| `exectype` | `varchar(10)` | NOT NULL |
| `md5sum` | `varchar(35)` |  |
| `description` | `varchar(255)` |  |
| `comments` | `varchar(255)` |  |
| `tag` | `varchar(255)` |  |
| `liquibase` | `varchar(20)` |  |

#### `databasechangeloglock`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` | PK · NOT NULL |
| `locked` | `bool` | NOT NULL |
| `lockgranted` | `timestamptz` |  |
| `lockedby` | `varchar(255)` |  |

#### `datacenter_attributes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `object_id` | `int4` | NOT NULL · → sb_datacenter.id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `attribute_id` | `int4` | NOT NULL · → attributes.id |
| `attribute_group_id` | `int4` |  |
| `value` | `text` |  |

#### `datacenter_available_currencies`

| Column | Type | Flags |
|--------|------|-------|
| `datacenter_id` | `int4` | PK · NOT NULL · → sb_datacenter.id |
| `currency_code` | `varchar(3)` | PK · NOT NULL · → currencies.code |

#### `email_recipients`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `email_text_id` | `int4` | → email_templates.id |
| `recipient_type` | `varchar(8)` |  |
| `recipient` | `varchar(64)` |  |
| `modified_by` | `int4` |  |

#### `email_template_groupings`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `email_template_id` | `int4` | → email_templates.id |
| `email_template_group_id` | `int4` | → email_template_groups.id |

#### `email_template_groups`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(500)` | NOT NULL |

#### `email_templates`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `default_subject` | `text` |  |
| `body` | `text` |  |
| `sender` | `text` |  |
| `name` | `varchar(64)` |  |
| `modified_by` | `int4` |  |

#### `employee_client_relations_quotas`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `employee_id` | `int4` | NOT NULL · → employees.id |
| `year` | `int4` | NOT NULL |
| `variable` | `numeric` |  |
| `july_quota` | `numeric` |  |
| `august_quota` | `numeric` |  |
| `september_quota` | `numeric` |  |
| `october_quota` | `numeric` |  |
| `november_quota` | `numeric` |  |
| `december_quota` | `numeric` |  |
| `january_quota` | `numeric` |  |
| `february_quota` | `numeric` |  |
| `march_quota` | `numeric` |  |
| `april_quota` | `numeric` |  |
| `may_quota` | `numeric` |  |
| `june_quota` | `numeric` |  |

#### `employee_client_relations_roles_matrix`

| Column | Type | Flags |
|--------|------|-------|
| `employee_id` | `int4` | PK · NOT NULL · → employees.id |
| `product_line_id` | `int4` | PK · NOT NULL · → product_lines.id |
| `client_relations_role_id` | `int4` | PK · NOT NULL · → client_relations_roles.id |
| `last_assigned` | `timestamptz` | NOT NULL |
| `igo_id` | `int4` | NOT NULL · → intergovernmental_organizations.id |
| `round_robin` | `bool` | NOT NULL |

#### `employee_client_relations_roles_product_line_independent_matrix`

| Column | Type | Flags |
|--------|------|-------|
| `employee_id` | `int4` | PK · NOT NULL |
| `client_relations_role_id` | `int4` | PK · NOT NULL |
| `igo_id` | `int4` | PK · NOT NULL |

#### `error_status_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `type` | `varchar(40)` |  |

#### `error_statuses`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `error_status_type_id` | `int4` | → error_status_types.id |
| `description` | `text` |  |

#### `eula`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(64)` |  |
| `eula_text` | `text` | NOT NULL |
| `date_created` | `timestamp` | NOT NULL |
| `client_id` | `int4` | → customers.customers_id |
| `url` | `varchar(255)` |  |
| `type` | `varchar(6)` |  |

#### `fraud_gateway_transactions`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `client_id` | `int4` | → customers.customers_id |
| `payment_method_id` | `int4` | → client_payment_methods.id |
| `score` | `int2` | NOT NULL |
| `date` | `timestamptz` | NOT NULL |
| `fraud_gateway` | `varchar(20)` | NOT NULL |
| `gateway_transaction` | `varchar` | NOT NULL |
| `status_code` | `bpchar` |  |

#### `history_certificate`

| Column | Type | Flags |
|--------|------|-------|
| `history_certificate_id` | `serial` | PK · auto · NOT NULL |
| `id` | `int4` |  |
| `options_licenses_id` | `int4` |  |
| `certificate_contact_id` | `int4` |  |
| `certificate_company_id` | `int4` |  |
| `status` | `varchar(255)` |  |
| `domain` | `text` |  |
| `os` | `varchar(32)` |  |
| `created` | `timestamptz` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `text` |  |
| `archive_date` | `timestamptz` |  |
| `action` | `varchar(16)` |  |

#### `history_client_bag_services`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `client_bag_id` | `int4` |  |
| `service_id` | `int4` |  |
| `action` | `varchar(20)` |  |
| `archive_date` | `timestamp` |  |
| `history_client_bag_services_id` | `serial` | PK · auto · NOT NULL |

#### `history_client_bags`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `client_id` | `int4` |  |
| `name` | `varchar(64)` |  |
| `description` | `text` |  |
| `is_active` | `bool` |  |
| `action` | `varchar(20)` |  |
| `archive_date` | `timestamp` |  |
| `created` | `timestamptz` |  |
| `created_by` | `varchar(32)` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `varchar(32)` |  |
| `history_client_bags_id` | `serial` | PK · auto · NOT NULL |

#### `history_client_orders`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `client_id` | `int4` |  |
| `status` | `int4` |  |
| `entered_by` | `text` |  |
| `order_created` | `timestamptz` |  |
| `action` | `varchar(16)` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `text` |  |
| `history_client_orders_id` | `serial` | PK · auto · NOT NULL |

#### `history_client_payment_methods`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `client_id` | `int4` |  |
| `payment_type_id` | `int4` |  |
| `wallet_id` | `varchar(256)` |  |
| `is_active` | `bool` |  |
| `display_info` | `varchar(32)` |  |
| `action` | `varchar(16)` |  |
| `archive_date` | `timestamp` |  |
| `code` | `int4` | → wallet_responses_pl.code |
| `response` | `varchar` |  |
| `auth_code` | `varchar` |  |
| `transaction_id` | `varchar` |  |
| `message_id` | `varchar` |  |
| `message_text` | `varchar` |  |
| `transaction_date` | `varchar` |  |
| `disabled` | `bool` |  |
| `disabled_reason` | `varchar(256)` |  |
| `history_client_payment_methods_id` | `serial` | PK · auto · NOT NULL |
| `card_type` | `varchar(20)` |  |
| `fraud_review_required` | `bool` |  |

#### `history_client_permission_roles`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `client_id` | `int4` |  |
| `permissions_id` | `varchar(32)` | → permissions.permissions_id |
| `contact_role_type_id` | `int4` |  |
| `created` | `timestamptz` |  |
| `created_by` | `varchar(32)` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `varchar(32)` |  |
| `archive_date` | `timestamptz` |  |
| `action` | `varchar(16)` |  |

#### `history_client_permission_users`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `client_id` | `int4` |  |
| `permissions_id` | `varchar(32)` | → permissions.permissions_id |
| `contact_id` | `int4` |  |
| `created` | `timestamptz` |  |
| `created_by` | `varchar(32)` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `varchar(32)` |  |
| `archive_date` | `timestamptz` |  |
| `action` | `varchar(16)` |  |

#### `history_client_private_net`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `client_id` | `int4` |  |
| `vlan_id` | `int4` |  |
| `alias` | `text` |  |
| `datacenter` | `text` |  |
| `netmask` | `int4` |  |
| `created` | `timestamptz` |  |
| `created_by` | `text` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `text` |  |
| `archive_date` | `timestamptz` |  |
| `action` | `text` |  |
| `history_client_private_net_id` | `serial` | PK · auto · NOT NULL |

#### `history_client_private_rack`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `client_id` | `int4` |  |
| `service_id` | `int4` |  |
| `vlan_id` | `int4` |  |
| `alias` | `text` |  |
| `datacenter` | `text` |  |
| `netmask` | `int4` |  |
| `created` | `timestamptz` |  |
| `created_by` | `text` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `text` |  |
| `archive_date` | `timestamptz` |  |
| `action` | `text` |  |
| `history_client_private_rack_id` | `serial` | PK · auto · NOT NULL |

#### `history_client_solution_services`

| Column | Type | Flags |
|--------|------|-------|
| `client_solution_id` | `int4` |  |
| `service_id` | `int4` |  |
| `action` | `varchar(20)` |  |
| `archive_date` | `timestamp` |  |
| `id` | `serial` | PK · auto · NOT NULL |

#### `history_client_solutions`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `client_id` | `int4` |  |
| `name` | `varchar(64)` |  |
| `description` | `text` |  |
| `action` | `varchar(20)` |  |
| `archive_date` | `timestamp` |  |
| `attachment` | `varchar` |  |
| `created` | `timestamptz` |  |
| `created_by` | `varchar(32)` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `varchar(32)` |  |
| `history_client_solutions_id` | `serial` | PK · auto · NOT NULL |

#### `history_client_zones`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `client_id` | `int4` |  |
| `zone` | `varchar(256)` |  |
| `created` | `timestamptz` |  |
| `created_by` | `varchar(32)` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `varchar(32)` |  |
| `action` | `varchar(20)` |  |
| `history_client_zones_id` | `serial` | PK · auto · NOT NULL |

#### `history_components`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `name` | `varchar(64)` |  |
| `description` | `varchar(256)` |  |
| `is_active` | `bool` |  |
| `modified_by` | `varchar(32)` |  |
| `component_type_id` | `int4` |  |
| `action` | `varchar(16)` |  |
| `archive_date` | `timestamp` |  |
| `cost` | `numeric` |  |
| `discountable` | `bool` |  |
| `history_components_id` | `serial` | PK · auto · NOT NULL |

#### `history_contact`

| Column | Type | Flags |
|--------|------|-------|
| `contact_id` | `int4` |  |
| `customers_id` | `int4` |  |
| `company` | `text` |  |
| `first_name` | `text` |  |
| `last_name` | `text` |  |
| `street_address1` | `text` |  |
| `street_address2` | `text` |  |
| `street_address3` | `text` |  |
| `postcode` | `text` |  |
| `city` | `text` |  |
| `country` | `text` |  |
| `zone` | `text` | → p1_zones.zone |
| `username` | `varchar(64)` |  |
| `password` | `text` |  |
| `security_question` | `varchar(255)` |  |
| `security_answer` | `text` |  |
| `subscribed` | `bool` |  |
| `is_disabled` | `bool` |  |
| `portal_user` | `bool` |  |
| `created` | `timestamptz` |  |
| `created_by` | `varchar(32)` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `varchar(32)` |  |
| `archive_date` | `timestamptz` | NOT NULL |
| `action` | `varchar(16)` |  |
| `id` | `serial` | PK · auto · NOT NULL |

#### `history_contact_communication_method`

| Column | Type | Flags |
|--------|------|-------|
| `contact_communication_id` | `int4` |  |
| `contact_id` | `int4` |  |
| `communication_type` | `varchar(255)` |  |
| `value` | `text` |  |
| `is_primary` | `bool` |  |
| `archive_date` | `timestamptz` | NOT NULL |
| `action` | `varchar(16)` |  |
| `id` | `serial` | PK · auto · NOT NULL |

#### `history_contact_role`

| Column | Type | Flags |
|--------|------|-------|
| `contact_role_id` | `int4` |  |
| `contact_id` | `int4` |  |
| `contact_role_type` | `varchar(255)` |  |
| `archive_date` | `timestamptz` | NOT NULL |
| `action` | `varchar(16)` |  |
| `id` | `serial` | PK · auto · NOT NULL |

#### `history_customers`

| Column | Type | Flags |
|--------|------|-------|
| `customers_id` | `int4` |  |
| `type` | `varchar(64)` |  |
| `company_name` | `varchar(255)` |  |
| `blacklisted` | `bool` |  |
| `referred_by` | `int4` |  |
| `overage_rate` | `numeric` |  |
| `shopping_cart_only` | `bool` |  |
| `payment_term` | `varchar(21)` | → payment_terms.payment_term |
| `created` | `timestamptz` |  |
| `created_by` | `varchar(32)` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `varchar(32)` |  |
| `archive_date` | `timestamptz` | NOT NULL |
| `action` | `varchar(16)` |  |
| `id` | `serial` | PK · auto · NOT NULL |
| `preferred_currency` | `varchar(3)` |  |
| `disabled` | `timestamptz` |  |
| `disabled_by` | `varchar(32)` |  |

#### `history_email_recipients`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `email_text_id` | `int4` |  |
| `recipient_type` | `varchar(8)` |  |
| `recipient` | `varchar(64)` |  |
| `modified_by` | `int4` |  |
| `action` | `varchar(16)` |  |
| `archive_date` | `timestamp` |  |
| `history_email_recipients_id` | `serial` | PK · auto · NOT NULL |

#### `history_email_templates`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `default_subject` | `text` |  |
| `body` | `text` |  |
| `sender` | `text` |  |
| `name` | `varchar(64)` |  |
| `modified_by` | `int4` |  |
| `action` | `varchar(16)` |  |
| `archive_date` | `timestamp` |  |
| `history_email_templates_id` | `serial` | PK · auto · NOT NULL |

#### `history_exchange_rates`

| Column | Type | Flags |
|--------|------|-------|
| `ocean_exchange_rate_id` | `varchar(15)` |  |
| `gp_exchange_rate_id` | `varchar(15)` |  |
| `functional_currency` | `varchar(3)` | PK · NOT NULL |
| `originating_currency` | `varchar(3)` | PK · NOT NULL |
| `exchange_rate` | `numeric` | NOT NULL |
| `last_modified` | `timestamp` | PK · NOT NULL |
| `action` | `varchar(20)` | NOT NULL |
| `archive_date` | `timestamp` | NOT NULL |

#### `history_ocean_restrictions`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` | NOT NULL |
| `resource` | `varchar(128)` |  |
| `group_name` | `varchar(255)` |  |
| `modified_by` | `int4` |  |
| `action` | `varchar(16)` |  |
| `archive_date` | `timestamp` |  |
| `history_ocean_restrictions_id` | `serial` | PK · auto · NOT NULL |

#### `history_permission_categories`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `permission_categories_id` | `int4` |  |
| `name` | `varchar(64)` |  |
| `sort_order` | `int4` |  |
| `created` | `timestamptz` |  |
| `created_by` | `varchar(32)` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `varchar(32)` |  |
| `archive_date` | `timestamptz` |  |
| `action` | `varchar(16)` |  |

#### `history_permissions`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `permissions_id` | `varchar(32)` | → permissions.permissions_id |
| `permission_categories_id` | `int4` |  |
| `permission_title` | `varchar(128)` |  |
| `full_description` | `varchar` |  |
| `sort_order` | `int4` |  |
| `created` | `timestamptz` |  |
| `created_by` | `varchar(32)` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `varchar(32)` |  |
| `archive_date` | `timestamptz` |  |
| `action` | `varchar(16)` |  |

#### `history_preconfigured_bundle_mapping`

| Column | Type | Flags |
|--------|------|-------|
| `preconfigured_bundle_mapping_id` | `int4` | NOT NULL |
| `last_modified` | `timestamp` |  |
| `action` | `varchar(30)` |  |
| `history_preconfigured_bundle_mapping_id` | `serial` | PK · auto · NOT NULL |

#### `history_pricebook`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `nrc` | `numeric` |  |
| `mrc` | `numeric` |  |
| `modified_by` | `varchar(32)` |  |
| `action` | `varchar(16)` |  |
| `archive_date` | `timestamp` |  |
| `setup` | `numeric` |  |
| `product_catalog` | `varchar(64)` |  |
| `component` | `varchar(64)` |  |
| `currency` | `varchar(255)` |  |
| `product_line` | `varchar(255)` |  |
| `datacenter` | `text` |  |
| `pricing_category` | `varchar(64)` |  |
| `history_pricebook_id` | `serial` | PK · auto · NOT NULL |
| `rate` | `numeric` |  |

#### `history_product_allowed_components`

| Column | Type | Flags |
|--------|------|-------|
| `product_id` | `int4` |  |
| `product_name` | `varchar(64)` |  |
| `component_id` | `int4` |  |
| `component_name` | `varchar(64)` |  |
| `available_in_shop` | `bool` |  |
| `created` | `timestamptz` |  |
| `created_by` | `varchar(32)` |  |
| `action` | `varchar(16)` |  |
| `archive_date` | `timestamptz` |  |
| `history_product_allowed_components_id` | `serial` | PK · auto · NOT NULL |

#### `history_product_catalog`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `product_class` | `int4` |  |
| `name` | `varchar(64)` |  |
| `description` | `varchar(1024)` |  |
| `is_active` | `bool` |  |
| `modified_by` | `varchar(32)` |  |
| `action` | `varchar(16)` |  |
| `archive_date` | `timestamp` |  |
| `available_in_shop` | `bool` |  |
| `sold_out` | `bool` |  |
| `history_product_catalog_id` | `serial` | PK · auto · NOT NULL |
| `discountable` | `bool` | NOT NULL |

#### `history_service_billing_details`

| Column | Type | Flags |
|--------|------|-------|
| `service_id` | `int4` |  |
| `contract_id` | `varchar(32)` |  |
| `billing_day` | `int4` |  |
| `billing_frequency` | `int4` |  |
| `contract_length` | `int4` | → contract_lengths.contract_length |
| `payment_method_id` | `int4` |  |
| `purchase_order` | `varchar(32)` |  |
| `promotion_id` | `int4` |  |
| `on_hold` | `bool` |  |
| `archive_date` | `timestamptz` | NOT NULL |
| `action` | `varchar(20)` |  |
| `id` | `serial` | PK · auto · NOT NULL |

#### `history_service_inventory_unavailable`

| Column | Type | Flags |
|--------|------|-------|
| `product_id` | `int4` |  |
| `product_name` | `varchar(64)` |  |
| `datacenter_id` | `int4` |  |
| `dc_abbr` | `text` |  |
| `created` | `timestamptz` |  |
| `created_by` | `varchar(32)` |  |
| `action` | `varchar(16)` |  |
| `archive_date` | `timestamptz` |  |
| `id` | `serial` | PK · auto · NOT NULL |

#### `history_service_options`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `options_name` | `text` |  |
| `options_type_id` | `int4` |  |
| `created` | `date` |  |
| `add_on` | `bool` |  |
| `who` | `int4` |  |
| `customer_products_id` | `int4` |  |
| `action` | `varchar(20)` |  |
| `archive_date` | `timestamptz` |  |
| `component_id` | `int4` |  |
| `setup` | `numeric` |  |
| `nrc` | `numeric` |  |
| `mrc` | `numeric` |  |
| `currency` | `varchar(3)` |  |
| `exchange_rate` | `numeric` |  |
| `capacity` | `numeric` |  |
| `uom_id` | `int4` |  |
| `history_service_options_id` | `serial` | PK · auto · NOT NULL |
| `quantity` | `int4` |  |
| `rate` | `numeric` |  |

#### `history_tax_rates`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` | PK · NOT NULL |
| `tax_schedule_id` | `varchar(15)` | NOT NULL |
| `country` | `varchar(2)` | NOT NULL |
| `tax_rate` | `numeric` | NOT NULL |
| `tax_portion` | `numeric` | NOT NULL |
| `description` | `varchar(31)` | NOT NULL |
| `last_modified` | `timestamp` | PK · NOT NULL |
| `action` | `varchar(20)` | NOT NULL |
| `archive_date` | `timestamp` | NOT NULL |

#### `history_template_permission_roles`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `permissions_id` | `varchar(32)` | → permissions.permissions_id |
| `contact_role_type_id` | `int4` |  |
| `created` | `timestamptz` |  |
| `created_by` | `varchar(32)` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `varchar(32)` |  |
| `archive_date` | `timestamptz` |  |
| `action` | `varchar(16)` |  |

#### `history_ticket_support_times`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `times_id` | `int4` |  |
| `ticket_id` | `int4` |  |
| `client_id` | `int4` |  |
| `service_id` | `int4` |  |
| `username` | `text` |  |
| `type` | `varchar(100)` |  |
| `time_worked_old` | `int4` |  |
| `time_worked_new` | `int4` |  |
| `action` | `varchar(20)` |  |
| `archive_date` | `timestamptz` |  |

#### `history_volume_discount_percentage`

| Column | Type | Flags |
|--------|------|-------|
| `history_volume_discount_percentage_id` | `serial` | PK · auto · NOT NULL |
| `id` | `int4` |  |
| `threshold` | `int4` | NOT NULL |
| `discount` | `numeric` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `archive_date` | `timestamptz` | NOT NULL |
| `action` | `varchar(16)` |  |

#### `history_workflow_notifications`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `service_id` | `int4` |  |
| `workflow_instance_id` | `int4` |  |
| `event_type` | `varchar` |  |
| `created` | `timestamptz` |  |
| `resolved` | `timestamptz` |  |
| `status` | `varchar` |  |
| `message` | `varchar` |  |
| `history_workflow_notifications_id` | `serial` | PK · auto · NOT NULL |

#### `history_xref_customer_products_dcc`

| Column | Type | Flags |
|--------|------|-------|
| `customer_products_id` | `int4` |  |
| `datacenter_id` | `int4` |  |
| `device_id` | `varchar(64)` |  |
| `action` | `varchar(20)` |  |
| `archive_date` | `timestamp` |  |
| `history_xref_customer_products_dcc_id` | `serial` | PK · auto · NOT NULL |

#### `history_xref_services_private_net`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `private_net_id` | `int4` |  |
| `service_id` | `int4` |  |
| `created` | `timestamptz` |  |
| `created_by` | `text` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `text` |  |
| `archive_date` | `timestamptz` |  |
| `action` | `text` |  |
| `history_xref_services_private_net_id` | `serial` | PK · auto · NOT NULL |

#### `history_xref_services_private_rack`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` |  |
| `private_rack_id` | `int4` |  |
| `service_id` | `int4` |  |
| `created` | `timestamptz` |  |
| `created_by` | `text` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `text` |  |
| `archive_date` | `timestamptz` |  |
| `action` | `text` |  |
| `history_xref_services_private_rack_id` | `serial` | PK · auto · NOT NULL |

#### `intergovernmental_organizations`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `text` |  |
| `abbr` | `varchar(16)` |  |

#### `item_tax_schedule`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `product_class_id` | `int4` | → product_classes.id |
| `component_category` | `int4` | → component_categories.id |
| `datacenter` | `int4` | NOT NULL · → sb_datacenter.id |
| `client_countries_id` | `int4` | → countries.countries_id |
| `client_state` | `varchar(255)` |  |
| `contract_type` | `varchar(255)` | NOT NULL |
| `mrc_tax_id` | `int4` | → tax_rates.id |
| `nrc_tax_id` | `int4` | → tax_rates.id |
| `setup_tax_id` | `int4` | → tax_rates.id |
| `rate_tax_id` | `int4` | → tax_rates.id |

#### `kickstart_component_keys`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `component_id` | `int4` | NOT NULL · → components.id |
| `key` | `varchar(64)` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `template_name` | `varchar(64)` |  |

#### `license_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(64)` | NOT NULL |
| `uri` | `varchar(256)` | NOT NULL |
| `type` | `varchar(32)` |  |

#### `line_sequence_mapping`

| Column | Type | Flags |
|--------|------|-------|
| `old_line_sequence_number` | `float8` | NOT NULL |
| `new_line_sequence_number` | `float8` | NOT NULL |

#### `login_history`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `ip_address` | `inet` |  |
| `client_id` | `int4` | → customers.customers_id |
| `session_id` | `bpchar` |  |
| `date_entered` | `timestamp` |  |
| `user_agent` | `text` |  |
| `contact_id` | `int4` | → contact.contact_id |

#### `message_box`

| Column | Type | Flags |
|--------|------|-------|
| `message_id` | `serial` | PK · auto · NOT NULL |
| `message` | `varchar` |  |
| `created` | `timestamptz` | NOT NULL |

#### `mon_runbook_custom_notes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `service_id` | `int4` |  |
| `check_type` | `varchar(128)` |  |
| `note_type` | `int4` |  |
| `notes` | `varchar(1024)` |  |

#### `mon_runbook_default_notes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `check_type` | `varchar(128)` |  |
| `notes` | `varchar(1024)` |  |

#### `my_rbac_pages`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `file_name` | `varchar(128)` | NOT NULL |
| `hidden` | `int4` | NOT NULL |
| `edit_only` | `int4` | NOT NULL |
| `unrestricted` | `int4` | NOT NULL |

#### `my_rbac_sections`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `section_name` | `varchar(48)` | NOT NULL |

#### `nbt_invoices`

| Column | Type | Flags |
|--------|------|-------|
| `customer_id` | `int4` | PK · NOT NULL · → customers.customers_id |
| `document_id` | `varchar(128)` | PK · NOT NULL |
| `document_type` | `varchar(16)` | NOT NULL |
| `due_date` | `timestamp` |  |
| `amount` | `numeric` |  |
| `status` | `varchar(4)` | NOT NULL |
| `filename` | `varchar(128)` |  |

#### `node_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` | PK · NOT NULL |
| `description` | `varchar(32)` | NOT NULL |

#### `ocean_config`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `key` | `varchar(64)` | NOT NULL |
| `value` | `text` | NOT NULL |
| `lastchange` | `timestamp` | NOT NULL |
| `changedby` | `varchar(64)` | NOT NULL |

#### `ocean_restrictions`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `resource` | `varchar(128)` |  |
| `group_name` | `varchar` |  |
| `modified_by` | `int4` |  |

#### `ocean_sessions`

| Column | Type | Flags |
|--------|------|-------|
| `session_id` | `bpchar` | PK · NOT NULL |
| `username` | `varchar(32)` |  |
| `active` | `bool` |  |
| `last_active` | `timestamptz` |  |
| `login_time` | `timestamptz` |  |
| `ip_address` | `inet` | NOT NULL |
| `user_agent` | `text` | NOT NULL |

#### `olid_service_option_link`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `order_line_item_detail_id` | `int4` | NOT NULL · → order_line_item_details.id |
| `order_line_item_id` | `int4` | NOT NULL · → order_line_item_details.order_line_item_id |
| `service_option_id` | `int4` | NOT NULL · → service_options.id |

#### `options_licenses`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `lkg_id` | `int4` | NOT NULL |
| `options_id` | `int4` | → service_options.id |
| `license_type_id` | `int4` | NOT NULL · → license_types.id |

#### `order_commission_split`

| Column | Type | Flags |
|--------|------|-------|
| `order_id` | `int4` | NOT NULL · → client_orders.id |
| `employee_id` | `int4` | NOT NULL · → employees.id |
| `percentage` | `numeric` | NOT NULL |
| `id` | `serial` | PK · auto · NOT NULL |

#### `order_communications`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `order_id` | `int4` | → client_orders.id |
| `order_status_id` | `int4` | → client_order_statuses.id |
| `date_sent` | `timestamp` | NOT NULL |
| `sent_to` | `varchar(128)` | NOT NULL |

#### `order_entry_solution_link`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `child_node` | `int4` | → order_entry_solution_node.id |
| `parent_node` | `int4` | → order_entry_solution_node.id |

#### `order_entry_solution_node`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `service_id` | `int4` | → customer_products.id |

#### `order_line_item_attributes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `line_item_id` | `int4` | NOT NULL · → order_line_items.id |
| `name` | `varchar(64)` | NOT NULL |
| `value` | `text` | NOT NULL |

#### `order_line_item_detail_attributes`

| Column | Type | Flags |
|--------|------|-------|
| `line_item_id` | `int4` | NOT NULL · → order_line_item_details.order_line_item_id |
| `detail_id` | `int4` | NOT NULL · → order_line_item_details.id |
| `name` | `varchar(64)` | NOT NULL |
| `value` | `text` | NOT NULL |
| `id` | `serial` | PK · auto · NOT NULL |
| `order_line_item_detail_attributes_id` | `serial` | auto · NOT NULL |

#### `order_line_item_detail_workorder_tickets`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `order_line_item_detail_id` | `int4` | NOT NULL |
| `workorder_id` | `int4` |  |
| `ticket_id` | `int4` |  |

#### `order_line_item_details`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `order_line_item_id` | `int4` | PK · NOT NULL · → order_line_items.id |
| `component_id` | `int4` | → components.id |
| `action` | `bpchar` | NOT NULL |
| `setup_fee` | `numeric` | NOT NULL |
| `nrc` | `numeric` | NOT NULL |
| `mrc` | `numeric` | NOT NULL |
| `component_name` | `varchar(128)` | NOT NULL |
| `default_setup_fee` | `numeric` | NOT NULL |
| `default_nrc` | `numeric` | NOT NULL |
| `default_mrc` | `numeric` | NOT NULL |
| `service_option_type` | `varchar(64)` | NOT NULL |
| `promotion_id` | `int4` | → promotions.id |
| `service_option_id` | `int4` | → service_options.id |
| `currency` | `varchar(3)` | NOT NULL · → currencies.code |
| `setup_fee_discount` | `numeric` |  |
| `mrc_discount` | `numeric` |  |
| `nrc_discount` | `numeric` |  |
| `exchange_rate` | `numeric` | NOT NULL |
| `quantity` | `int4` | NOT NULL |
| `rate` | `numeric` |  |

#### `order_line_item_migrated_services`

| Column | Type | Flags |
|--------|------|-------|
| `order_line_item_id` | `int4` | PK · NOT NULL · → order_line_items.id |
| `service_id` | `int4` | PK · NOT NULL · → customer_products.id |

#### `order_line_item_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(32)` | NOT NULL |

#### `order_line_item_workorder_tickets`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `order_line_item_id` | `int4` | NOT NULL |
| `workorder_id` | `int4` |  |
| `ticket_id` | `int4` |  |

#### `order_line_items`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `order_id` | `int4` | → client_orders.id |
| `order_line_item_type_id` | `int4` | → order_line_item_types.id |
| `contract_id` | `varchar(32)` |  |
| `purchase_order` | `varchar(32)` |  |
| `tls_id` | `int4` | → product_catalog.id |
| `location_id` | `int4` | → sb_datacenter.id |
| `payment_type` | `int4` | → payment_types.id |
| `payment_method_id` | `int4` | → client_payment_methods.id |
| `nickname` | `varchar(64)` | NOT NULL |
| `service_id` | `int4` |  |
| `contract_length` | `int4` | → contract_lengths.contract_length |
| `billing_day` | `int4` |  |
| `billing_cycle` | `int4` |  |
| `setup_fee` | `numeric` | NOT NULL |
| `mrc` | `numeric` | NOT NULL |
| `notes` | `text` |  |
| `product_name` | `varchar(128)` | NOT NULL |
| `default_setup_fee` | `numeric` | NOT NULL |
| `default_mrc` | `numeric` | NOT NULL |
| `tls` | `varchar(64)` | NOT NULL |
| `provision_date` | `timestamp` |  |
| `provision_required` | `bool` | NOT NULL |
| `old_line_item_id` | `int4` | → order_line_items.id |
| `status` | `varchar` |  |
| `message` | `varchar` |  |
| `last_modified` | `timestamptz` |  |
| `promotion_id` | `int4` | → promotions.id |
| `product_line_id` | `int4` | → product_lines.id |
| `currency` | `varchar(3)` | NOT NULL · → currencies.code |
| `setup_fee_discount` | `numeric` |  |
| `mrc_discount` | `numeric` |  |
| `exchange_rate` | `numeric` | NOT NULL |
| `is_virtual` | `bool` | NOT NULL |
| `hide_in_portal` | `bool` | NOT NULL |
| `rate` | `numeric` |  |
| `default_rate` | `numeric` |  |

#### `order_notes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `order_id` | `int4` | NOT NULL · → client_orders.id |
| `message` | `text` | NOT NULL |
| `date` | `timestamptz` | NOT NULL |
| `who` | `varchar(32)` | NOT NULL |

#### `p1_zones`

| Column | Type | Flags |
|--------|------|-------|
| `zone` | `text` | PK · NOT NULL |

#### `package`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `service_option_id` | `int4` |  |
| `description` | `text` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `username` | `varchar(64)` | NOT NULL |
| `password` | `varchar(64)` | NOT NULL |
| `service_id` | `int4` |  |

#### `partition_details`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `partitions_id` | `int4` | NOT NULL · → partitions.id |
| `mount_point` | `varchar(256)` | NOT NULL |
| `fstype` | `varchar(256)` | NOT NULL |
| `size` | `varchar(256)` | NOT NULL |
| `label` | `varchar(256)` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `is_data_partition` | `bool` |  |
| `maxsize` | `varchar(256)` |  |
| `partition_type` | `varchar(256)` | NOT NULL |
| `grow` | `bool` | NOT NULL |

#### `partition_object_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `value` | `varchar(16)` | NOT NULL |

#### `partitions`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `object_type_id` | `int4` | NOT NULL · → partition_object_types.id |
| `object_id` | `int4` | NOT NULL |
| `device_id` | `int4` |  |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `payment_gateway_providers`

| Column | Type | Flags |
|--------|------|-------|
| `payment_gateway_id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar` | NOT NULL |
| `is_active` | `bool` |  |

#### `payment_gateway_transaction_log_details`

| Column | Type | Flags |
|--------|------|-------|
| `log_id` | `int4` | NOT NULL |
| `name` | `text` |  |
| `value` | `text` |  |
| `attribute_id` | `serial` | PK · auto · NOT NULL |

#### `payment_gateway_transaction_logs`

| Column | Type | Flags |
|--------|------|-------|
| `transaction_id` | `int4` | PK · NOT NULL |
| `log_id` | `serial` | PK · auto · NOT NULL |

#### `payment_merchant_accounts`

| Column | Type | Flags |
|--------|------|-------|
| `payment_merchant_id` | `varchar` | PK · NOT NULL |
| `payment_user` | `varchar` |  |
| `payment_pass` | `varchar` |  |
| `payment_processing_url` | `varchar` |  |
| `payment_gateway_url` | `varchar` |  |
| `payment_gateway_id` | `int4` | PK · NOT NULL · → payment_gateway_providers.payment_gateway_id |
| `company` | `varchar(3)` | PK · NOT NULL |
| `functional_currency` | `varchar(3)` | PK · NOT NULL |
| `originating_currency` | `varchar(3)` | PK · NOT NULL |
| `environment` | `varchar` | PK · NOT NULL |
| `is_active` | `bool` |  |
| `payment_signature` | `varchar` |  |
| `payment_profile_url` | `varchar` |  |
| `payment_webform_url` | `varchar` |  |

#### `payment_terms`

| Column | Type | Flags |
|--------|------|-------|
| `payment_term` | `varchar(21)` | PK · NOT NULL |

#### `payment_transaction_documents`

| Column | Type | Flags |
|--------|------|-------|
| `payment_transaction_id` | `int4` | PK · NOT NULL · → payment_transactions.id |
| `document_type` | `varchar` |  |
| `document_id` | `varchar` | PK · NOT NULL |
| `amount` | `numeric` |  |
| `sales_tax` | `numeric` |  |
| `id` | `serial` | auto · NOT NULL |

#### `payment_transactions`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `date` | `timestamptz` |  |
| `client_wallet` | `varchar(32)` |  |
| `amount` | `numeric` |  |
| `type` | `varchar(32)` |  |
| `billing_name` | `varchar(256)` |  |
| `billing_phone` | `varchar(20)` |  |
| `billing_email` | `varchar(256)` |  |
| `billing_street` | `varchar(256)` |  |
| `billing_suburb` | `varchar(256)` |  |
| `billing_city` | `varchar(256)` |  |
| `billing_province` | `varchar(256)` |  |
| `billing_postal_code` | `varchar(10)` |  |
| `billing_country` | `varchar(2)` |  |
| `status` | `varchar(30)` |  |
| `last_modified` | `timestamptz` |  |
| `originating_currency` | `varchar(5)` |  |
| `comments` | `varchar` |  |
| `authcode` | `varchar(32)` |  |
| `token` | `varchar(32)` |  |
| `message` | `varchar` |  |
| `display_info` | `varchar(32)` |  |
| `payment_type` | `varchar(32)` |  |
| `created_by` | `varchar(256)` |  |
| `sales_tax` | `numeric` |  |
| `company` | `varchar(3)` |  |
| `functional_currency` | `varchar(3)` |  |
| `client_id` | `int4` |  |
| `card_type` | `varchar` |  |
| `payment_gateway_name` | `varchar(32)` |  |
| `receipt` | `varchar(50)` |  |

#### `payment_transactions_paypal`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `payment_transaction_id` | `int4` | → payment_transactions.id |
| `transaction_id` | `varchar(32)` |  |
| `correlation_id` | `varchar(32)` |  |
| `payment_status` | `varchar(32)` |  |
| `pending_reason` | `varchar(256)` |  |
| `email` | `varchar(256)` |  |

#### `payment_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `int4` | PK · NOT NULL |
| `type` | `varchar(32)` | NOT NULL |
| `description` | `varchar(256)` |  |
| `mgr_approval_required` | `bool` | NOT NULL |
| `wallet_id_required` | `bool` |  |
| `is_active` | `bool` | NOT NULL |

#### `permission_categories`

| Column | Type | Flags |
|--------|------|-------|
| `permission_categories_id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(64)` | NOT NULL |
| `sort_order` | `int4` |  |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `permissions`

| Column | Type | Flags |
|--------|------|-------|
| `permissions_id` | `varchar(32)` | PK · NOT NULL |
| `permission_categories_id` | `int4` | NOT NULL · → permission_categories.permission_categories_id |
| `permission_title` | `varchar(128)` | NOT NULL |
| `full_description` | `varchar` | NOT NULL |
| `sort_order` | `int4` |  |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `portal_login`

| Column | Type | Flags |
|--------|------|-------|
| `hash` | `varchar(1024)` | PK · NOT NULL |
| `client_id` | `int4` | NOT NULL · → customers.customers_id |
| `username` | `varchar(64)` | NOT NULL · → employees.username |
| `expiration` | `timestamptz` | NOT NULL |
| `contact_id` | `int4` | → contact.contact_id |

#### `preconfigured_bundle_categories`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(256)` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `preconfigured_bundle_mapping`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `preconfigured_bundle_categories_id` | `int4` | NOT NULL · → preconfigured_bundle_categories.id |
| `datacenter_id` | `int4` | NOT NULL · → sb_datacenter.id |
| `operating_system` | `varchar` | NOT NULL |
| `rating` | `int4` | NOT NULL |
| `product_id` | `int4` | NOT NULL · → product_catalog.id |
| `product_configuration_id` | `int4` | → product_configurations.id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `pricebook`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `product_catalog_id` | `int4` | → product_catalog.id |
| `component_id` | `int4` | → components.id |
| `nrc` | `numeric` |  |
| `mrc` | `numeric` |  |
| `modified_by` | `varchar(32)` | NOT NULL |
| `setup` | `numeric` | NOT NULL |
| `currency` | `varchar(3)` | NOT NULL · → currencies.code |
| `product_line_id` | `int4` | NOT NULL · → product_lines.id |
| `datacenter` | `int4` | NOT NULL · → sb_datacenter.id |
| `rate` | `numeric` |  |
| `is_available` | `bool` |  |

#### `product_allowed_components`

| Column | Type | Flags |
|--------|------|-------|
| `product_id` | `int4` | PK · NOT NULL · → product_catalog.id |
| `component_id` | `int4` | PK · NOT NULL · → components.id |
| `available_in_shop` | `bool` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `id` | `int8` |  |

#### `product_catalog`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `product_class` | `int4` | NOT NULL · → product_classes.id |
| `name` | `varchar(64)` | NOT NULL |
| `description` | `varchar(1024)` | NOT NULL |
| `is_active` | `bool` | NOT NULL |
| `modified_by` | `varchar(32)` | NOT NULL |
| `available_in_shop` | `bool` | NOT NULL |
| `sold_out` | `bool` | NOT NULL |
| `category_id` | `int4` | → product_categories.id |
| `product_summary` | `text` |  |
| `is_virtual` | `bool` | NOT NULL |
| `hide_in_portal` | `bool` | NOT NULL |
| `limited_availability` | `bool` | NOT NULL |
| `use_picker` | `bool` | NOT NULL |
| `discountable` | `bool` | NOT NULL |
| `sku` | `varchar(64)` |  |
| `release_date` | `date` |  |

#### `product_catalog_attributes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `object_id` | `int4` | NOT NULL · → product_catalog.id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `attribute_id` | `int4` | NOT NULL · → attributes.id |
| `attribute_group_id` | `int4` |  |
| `value` | `text` |  |
| `visibility_group` | `varchar(255)` |  |
| `visibility_user` | `varchar(255)` |  |

#### `product_categories`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(64)` | NOT NULL |
| `description` | `varchar(1024)` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `product_class_client_type_discounts`

| Column | Type | Flags |
|--------|------|-------|
| `product_line` | `int4` | PK · NOT NULL · → product_lines.id |
| `product_class` | `int4` | PK · NOT NULL · → product_classes.id |
| `client_type_id` | `int4` | PK · NOT NULL · → client_types_pl.client_type_id |
| `setup_discount` | `numeric` | NOT NULL |
| `mrc_discount` | `numeric` | NOT NULL |
| `nrc_discount` | `numeric` | NOT NULL |
| `rate_discount` | `numeric` | NOT NULL |

#### `product_class_contract_length_discounts`

| Column | Type | Flags |
|--------|------|-------|
| `product_line` | `int4` | PK · NOT NULL · → product_lines.id |
| `product_class` | `int4` | PK · NOT NULL · → product_classes.id |
| `contract_length` | `int4` | PK · NOT NULL · → contract_lengths.contract_length |
| `setup_discount` | `numeric` | NOT NULL |
| `mrc_discount` | `numeric` | NOT NULL |
| `nrc_discount` | `numeric` | NOT NULL |
| `rate_discount` | `numeric` | NOT NULL |

#### `product_classes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(32)` | NOT NULL |
| `description` | `varchar(256)` | NOT NULL |
| `sort_order` | `int4` | NOT NULL |
| `is_active` | `bool` | NOT NULL |

#### `product_configuration_changesets`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `configuration_id` | `int4` | NOT NULL · → product_configurations.id |
| `template_component_id` | `int4` | → product_templates.id |
| `new_component_id` | `int4` | NOT NULL · → components.id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `product_configurations`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `product_id` | `int4` | → product_catalog.id |
| `configuration_name` | `varchar(256)` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `product_frameworks`

| Column | Type | Flags |
|--------|------|-------|
| `product_id` | `int4` | PK · NOT NULL · → product_catalog.id |
| `component_type_id` | `int4` | PK · NOT NULL · → component_types.id |
| `minimum_required` | `int4` | NOT NULL |
| `maximum_allowed` | `int4` |  |
| `modified_by` | `varchar(32)` | NOT NULL |

#### `product_templates`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `product_id` | `int4` | NOT NULL · → product_catalog.id |
| `component_id` | `int4` | NOT NULL · → components.id |
| `modified_by` | `varchar(32)` | NOT NULL |
| `quantity` | `int4` | NOT NULL |

#### `promotion_component_criteria`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `promo_id` | `int4` | NOT NULL · → promotions.id |
| `component_id` | `int4` | NOT NULL · → components.id |
| `minimum_quantity` | `int4` | NOT NULL |
| `depth` | `int4` | NOT NULL |
| `operator` | `varchar(3)` | NOT NULL · → resource_use_operators.operator |
| `scope` | `varchar(32)` | NOT NULL |

#### `promotion_component_type_criteria`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `promo_id` | `int4` | NOT NULL · → promotions.id |
| `component_type_id` | `int4` | NOT NULL · → component_types.id |
| `minimum_quantity` | `int4` | NOT NULL |
| `depth` | `int4` | NOT NULL |
| `operator` | `varchar(3)` | NOT NULL · → resource_use_operators.operator |
| `scope` | `varchar(32)` | NOT NULL |

#### `promotion_component_types`

| Column | Type | Flags |
|--------|------|-------|
| `promotion_id` | `int4` | PK · NOT NULL · → promotions.id |
| `component_type_id` | `int4` | PK · NOT NULL · → component_types.id |

#### `promotion_contract_length_criteria`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `promo_id` | `int4` | NOT NULL · → promotions.id |
| `contract_length` | `int4` | NOT NULL · → contract_lengths.contract_length |
| `minimum_quantity` | `int4` | NOT NULL |
| `depth` | `int4` | NOT NULL |
| `operator` | `varchar(3)` | NOT NULL · → resource_use_operators.operator |
| `scope` | `varchar(32)` | NOT NULL |

#### `promotion_criteria_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(64)` | NOT NULL |
| `source` | `varchar(64)` |  |

#### `promotion_customer_type_criteria`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `promo_id` | `int4` | NOT NULL · → promotions.id |
| `customer_type_id` | `int4` | NOT NULL · → client_types_pl.client_type_id |
| `minimum_quantity` | `int4` | NOT NULL |
| `depth` | `int4` | NOT NULL |
| `operator` | `varchar(3)` | NOT NULL · → resource_use_operators.operator |
| `scope` | `varchar(32)` | NOT NULL |

#### `promotion_effect_amounts`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `effect_id` | `int4` | NOT NULL · → promotion_effects.id |
| `currency_code` | `varchar(3)` | NOT NULL · → currencies.code |
| `amount` | `float8` | NOT NULL |
| `amount_type_id` | `int4` | NOT NULL · → promotion_effect_target_amount_types.id |

#### `promotion_effect_component_criteria`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `effect_id` | `int4` | NOT NULL · → promotion_effects.id |
| `component_id` | `int4` | NOT NULL · → components.id |
| `minimum_quantity` | `int4` | NOT NULL |
| `depth` | `int4` | NOT NULL |
| `operator` | `varchar(3)` | NOT NULL · → resource_use_operators.operator |
| `scope` | `varchar(32)` | NOT NULL |

#### `promotion_effect_component_type_criteria`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `effect_id` | `int4` | NOT NULL · → promotion_effects.id |
| `component_type_id` | `int4` | NOT NULL · → component_types.id |
| `minimum_quantity` | `int4` | NOT NULL |
| `depth` | `int4` | NOT NULL |
| `operator` | `varchar(3)` | NOT NULL · → resource_use_operators.operator |
| `scope` | `varchar(32)` | NOT NULL |

#### `promotion_effect_product_class_criteria`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `effect_id` | `int4` | NOT NULL · → promotion_effects.id |
| `product_class_id` | `int4` | NOT NULL · → product_classes.id |
| `minimum_quantity` | `int4` | NOT NULL |
| `depth` | `int4` | NOT NULL |
| `operator` | `varchar(3)` | NOT NULL · → resource_use_operators.operator |
| `scope` | `varchar(32)` | NOT NULL |

#### `promotion_effect_product_criteria`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `effect_id` | `int4` | NOT NULL · → promotion_effects.id |
| `product_id` | `int4` | NOT NULL · → product_catalog.id |
| `minimum_quantity` | `int4` | NOT NULL |
| `depth` | `int4` | NOT NULL |
| `operator` | `varchar(3)` | NOT NULL · → resource_use_operators.operator |
| `scope` | `varchar(32)` | NOT NULL |

#### `promotion_effect_target_amount_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(32)` | NOT NULL |

#### `promotion_effect_target_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(32)` | NOT NULL |

#### `promotion_effect_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(32)` | NOT NULL |

#### `promotion_effects`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `promo_id` | `int4` | NOT NULL · → promotions.id |
| `effect_type_id` | `int4` | NOT NULL · → promotion_effect_types.id |
| `target_id` | `int4` | NOT NULL |
| `target_type_id` | `int4` | NOT NULL · → promotion_effect_target_types.id |
| `target_max_quantity` | `int4` | NOT NULL |

#### `promotion_location_criteria`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `promo_id` | `int4` | NOT NULL · → promotions.id |
| `location_id` | `int4` | NOT NULL · → sb_datacenter.id |
| `minimum_quantity` | `int4` | NOT NULL |
| `depth` | `int4` | NOT NULL |
| `operator` | `varchar(3)` | NOT NULL · → resource_use_operators.operator |
| `scope` | `varchar(32)` | NOT NULL |

#### `promotion_product_class_criteria`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `promo_id` | `int4` | NOT NULL · → promotions.id |
| `product_class_id` | `int4` | NOT NULL · → product_classes.id |
| `minimum_quantity` | `int4` | NOT NULL |
| `depth` | `int4` | NOT NULL |
| `operator` | `varchar(3)` | NOT NULL · → resource_use_operators.operator |
| `scope` | `varchar(32)` | NOT NULL |

#### `promotion_product_classes`

| Column | Type | Flags |
|--------|------|-------|
| `promotion_id` | `int4` | PK · NOT NULL · → promotions.id |
| `product_class_id` | `int4` | PK · NOT NULL · → product_classes.id |

#### `promotion_product_criteria`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `promo_id` | `int4` | NOT NULL · → promotions.id |
| `product_id` | `int4` | NOT NULL · → product_catalog.id |
| `minimum_quantity` | `int4` | NOT NULL |
| `depth` | `int4` | NOT NULL |
| `operator` | `varchar(3)` | NOT NULL · → resource_use_operators.operator |
| `scope` | `varchar(32)` | NOT NULL |

#### `promotion_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(32)` | NOT NULL |
| `description` | `varchar(255)` |  |

#### `promotions`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `promo_code` | `varchar(32)` | NOT NULL |
| `description` | `varchar` | NOT NULL |
| `start_date` | `date` | NOT NULL |
| `end_date` | `date` | NOT NULL |
| `promo_type_id` | `int4` | NOT NULL · → promotion_types.id |
| `available_in_shop` | `bool` | NOT NULL |
| `available_in_oes` | `bool` | NOT NULL |
| `has_gift_item` | `bool` | NOT NULL |
| `gift_item_description` | `varchar(255)` |  |

#### `provisioning_tickets`

| Column | Type | Flags |
|--------|------|-------|
| `order_id` | `int4` | NOT NULL · → client_orders.id |
| `service_id` | `int4` | NOT NULL · → customer_products.id |
| `ticket_id` | `int4` | PK · NOT NULL · → client_tickets.ticket_id |
| `color` | `ticket_colors` | NOT NULL |

#### `queue_messages`

| Column | Type | Flags |
|--------|------|-------|
| `queue_id` | `int4` | PK · NOT NULL |
| `message_id` | `int4` | PK · NOT NULL |
| `consumed` | `timestamptz` |  |
| `locked` | `timestamptz` | NOT NULL |
| `token` | `varchar` |  |

#### `queues`

| Column | Type | Flags |
|--------|------|-------|
| `queue_id` | `serial` | PK · auto · NOT NULL |
| `queue_name` | `varchar` |  |
| `description` | `varchar` |  |

#### `raid_levels`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `level` | `varchar(4)` | NOT NULL |
| `name` | `varchar(32)` | NOT NULL |
| `description` | `text` | NOT NULL |
| `min_drives` | `int4` | NOT NULL |
| `allow_hotspare` | `bool` | NOT NULL |

#### `resource_use_operators`

| Column | Type | Flags |
|--------|------|-------|
| `operator` | `varchar(3)` | PK · NOT NULL |
| `name` | `varchar(64)` | NOT NULL |
| `description` | `varchar(256)` |  |

#### `resource_use_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(32)` |  |
| `description` | `varchar(512)` |  |

#### `resources`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(32)` |  |
| `uom` | `int4` | → unit_of_measure.id |
| `description` | `varchar(512)` |  |

#### `roles`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `text` | NOT NULL |
| `description` | `text` | NOT NULL |

#### `rss_feed_spotlight`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `alt_text` | `text` |  |
| `img_link` | `varchar(128)` |  |
| `img_data` | `bytea` |  |

#### `rss_feeds`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `body` | `text` | NOT NULL |
| `link` | `varchar(128)` |  |
| `image` | `int4` | → rss_feed_spotlight.id |
| `category` | `varchar(64)` |  |
| `published_date` | `timestamptz` |  |

#### `sb_customer_log`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `customers_id` | `int4` | → customers.customers_id |
| `log_type_id` | `int4` | → sb_log_type.id |
| `message` | `text` |  |
| `logged_by` | `text` |  |
| `logged_on` | `timestamptz` |  |
| `ticket_id` | `int4` |  |

#### `sb_customer_product_log`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `customer_product_id` | `int4` | → customer_products.id |
| `log_type_id` | `int4` | → sb_log_type.id |
| `message` | `text` |  |
| `logged_by` | `text` |  |
| `logged_on` | `timestamptz` |  |
| `ticket_id` | `int4` |  |

#### `sb_datacenter`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `text` | NOT NULL |
| `city` | `text` |  |
| `state` | `text` |  |
| `dc_abbr` | `text` | NOT NULL |
| `active` | `bool` |  |
| `url` | `varchar(64)` | NOT NULL |
| `countries_id` | `int4` | NOT NULL · → countries.countries_id |

#### `sb_log_type`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `text` |  |

#### `secret_questions_pl`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `question` | `text` | NOT NULL |

#### `service_account`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `username` | `varchar(64)` | NOT NULL |
| `password` | `varchar(64)` | NOT NULL |
| `description` | `varchar(256)` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `service_cancellation_queue`

| Column | Type | Flags |
|--------|------|-------|
| `service_id` | `int4` | PK · NOT NULL · → customer_products.id |
| `queue_date` | `timestamptz` | NOT NULL |
| `cancellation_date` | `timestamptz` | NOT NULL |
| `last_email_date` | `timestamptz` |  |
| `ticket_id` | `int4` |  |
| `reason` | `varchar(1024)` |  |

#### `service_inventory_unavailable`

| Column | Type | Flags |
|--------|------|-------|
| `product_id` | `int4` | PK · NOT NULL · → product_catalog.id |
| `datacenter_id` | `int4` | PK · NOT NULL · → sb_datacenter.id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |

#### `service_licenses`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `lkg_id` | `int4` |  |
| `service_id` | `int4` | → customer_products.id |
| `license_type_id` | `int4` | → license_types.id |

#### `service_notes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `service_id` | `int4` | NOT NULL · → customer_products.id |
| `message` | `varchar` | NOT NULL |
| `date` | `timestamptz` | NOT NULL |
| `who` | `varchar(32)` | NOT NULL |

#### `service_option_raid_arrays`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `raid_card_id` | `int4` | NOT NULL · → service_options.id |
| `raid_level_id` | `int4` | NOT NULL · → raid_levels.id |

#### `service_option_raid_configuration`

| Column | Type | Flags |
|--------|------|-------|
| `raid_option_id` | `int4` | PK · NOT NULL · → service_options.id |
| `raid_card_id` | `int4` | NOT NULL · → service_options.id |
| `raid_array_id` | `int4` | → service_option_raid_arrays.id |
| `role` | `raid_roles` | NOT NULL |

#### `service_option_types_pl`

| Column | Type | Flags |
|--------|------|-------|
| `service_option_types_id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(64)` | NOT NULL |
| `description` | `varchar(255)` | NOT NULL |
| `sort_order` | `int4` | NOT NULL |
| `is_active` | `bool` | NOT NULL |

#### `service_options`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `options_name` | `text` |  |
| `options_type_id` | `int4` | → service_option_types_pl.service_option_types_id |
| `created` | `date` | NOT NULL |
| `add_on` | `bool` |  |
| `who` | `int4` |  |
| `customer_products_id` | `int4` | → customer_products.id |
| `capacity` | `numeric` |  |
| `uom_id` | `int4` | → unit_of_measure.id |
| `component_id` | `int4` | → components.id |
| `setup` | `numeric` | NOT NULL |
| `nrc` | `numeric` | NOT NULL |
| `mrc` | `numeric` | NOT NULL |
| `currency` | `varchar(3)` | NOT NULL · → currencies.code |
| `exchange_rate` | `numeric` | NOT NULL |
| `quantity` | `int4` | NOT NULL |
| `rate` | `numeric` |  |

#### `service_options_attributes`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `object_id` | `int4` | NOT NULL · → service_options.id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |
| `attribute_id` | `int4` | NOT NULL · → attributes.id |
| `attribute_group_id` | `int4` |  |
| `value` | `text` |  |
| `visibility_group` | `varchar(255)` |  |
| `visibility_user` | `varchar(255)` |  |

#### `service_options_mercury_services`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `service_options_id` | `int4` | NOT NULL |
| `service_num` | `int4` | NOT NULL |
| `order_line_item_detail_id` | `int4` |  |

#### `service_type_capabilities`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `service_type_id` | `int4` | NOT NULL · → service_type_pl.service_type_id |
| `capabilities_id` | `int4` | NOT NULL · → capabilities.id |

#### `service_type_pl`

| Column | Type | Flags |
|--------|------|-------|
| `service_type_id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(64)` | NOT NULL |
| `description` | `varchar(255)` | NOT NULL |
| `sort_order` | `int4` |  |
| `is_active` | `bool` |  |

#### `service_workflow_matrix`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `product` | `varchar(64)` |  |
| `tls_type` | `varchar(64)` | NOT NULL |
| `option` | `varchar(64)` |  |
| `option_class` | `varchar(64)` |  |
| `workflow_id` | `int4` | NOT NULL |
| `datacenter_id` | `int4` | → sb_datacenter.id |
| `workflow_event_type_id` | `int4` | NOT NULL · → workflow_event_types.id |
| `product_line_id` | `int4` | → product_lines.id |

#### `sessions`

| Column | Type | Flags |
|--------|------|-------|
| `session_id` | `bpchar` | PK · NOT NULL |
| `client_id` | `int4` | → customers.customers_id |
| `active` | `bool` |  |
| `last_login` | `timestamp` |  |
| `contact_id` | `int4` | → contact.contact_id |

#### `solution_connection_property_types`

| Column | Type | Flags |
|--------|------|-------|
| `connection_property_name` | `varchar(32)` | PK · NOT NULL |
| `description` | `varchar` |  |

#### `solution_service_connection_properties`

| Column | Type | Flags |
|--------|------|-------|
| `solution_service_connection_id` | `int4` | NOT NULL · → solution_service_connections.solution_service_connection_id |
| `connection_property_name` | `varchar(32)` | NOT NULL · → solution_connection_property_types.connection_property_name |
| `connection_property_value` | `varchar(256)` | NOT NULL |
| `id` | `serial` | PK · auto · NOT NULL |

#### `solution_service_connections`

| Column | Type | Flags |
|--------|------|-------|
| `solution_service_connection_id` | `serial` | PK · auto · NOT NULL |
| `client_solution_id` | `int4` | NOT NULL · → client_solution_services.client_solution_id |
| `service1` | `int4` | NOT NULL · → client_solution_services.service_id |
| `service1_vertex` | `int4` | NOT NULL |
| `service2` | `int4` | NOT NULL · → client_solution_services.service_id |
| `service2_vertex` | `int4` | NOT NULL |
| `directed` | `bool` | NOT NULL |

#### `task_status_pl`

| Column | Type | Flags |
|--------|------|-------|
| `status_id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(64)` | NOT NULL |
| `description` | `varchar(255)` | NOT NULL |
| `sort_order` | `int4` | NOT NULL |
| `is_active` | `bool` | NOT NULL |

#### `tax_rates`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `tax_schedule_id` | `varchar(15)` | NOT NULL |
| `country` | `varchar(2)` | NOT NULL · → countries.countries_iso_code_2 |
| `tax_rate` | `numeric` | NOT NULL |
| `tax_portion` | `numeric` | NOT NULL |
| `description` | `varchar(31)` | NOT NULL |
| `last_modified` | `timestamp` | NOT NULL |

#### `tax_registration_types`

| Column | Type | Flags |
|--------|------|-------|
| `tax_registration_type_id` | `varchar(16)` | PK · NOT NULL |
| `name` | `varchar` | NOT NULL |
| `certificate_required` | `bool` | NOT NULL |
| `bitmask` | `varbit` | NOT NULL |
| `fieldname_remote` | `varchar` |  |

#### `template_permission_roles`

| Column | Type | Flags |
|--------|------|-------|
| `permissions_id` | `varchar(32)` | PK · NOT NULL · → permissions.permissions_id |
| `contact_role_type_id` | `int4` | PK · NOT NULL · → contact_role_type.contact_role_type_id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `ticket_support_time_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(100)` |  |
| `rate` | `float8` |  |
| `gp_item_id` | `varchar(32)` |  |
| `billable` | `bool` |  |

#### `ticket_support_times`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `ticket_id` | `int4` |  |
| `client_id` | `int4` | NOT NULL · → customers.customers_id |
| `service_id` | `int4` | → customer_products.id |
| `username` | `text` |  |
| `type_id` | `int4` | → ticket_support_time_types.id |
| `minutes_worked` | `int4` |  |
| `created_on` | `timestamptz` |  |
| `executed_on` | `timestamptz` |  |

#### `tls_workorder_templates`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `product_id` | `int4` | NOT NULL · → product_catalog.id |
| `workorder_template` | `text` |  |

#### `transactions_pending_client_approval`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `created` | `timestamptz` |  |
| `token` | `varchar(128)` |  |
| `payment_gateway_name` | `varchar(32)` |  |
| `transaction` | `text` |  |

#### `unit_of_measure`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(32)` | NOT NULL |
| `abbr` | `varchar(10)` | NOT NULL |
| `base_unit_id` | `int4` | → unit_of_measure.id |
| `conversion_factor` | `numeric` |  |

#### `vam_admin_account`

| Column | Type | Flags |
|--------|------|-------|
| `client_id` | `int4` | NOT NULL |
| `sspc_url` | `varchar(255)` |  |
| `initial_address_url` | `varchar(255)` |  |
| `login` | `varchar(80)` |  |
| `password` | `varchar(80)` |  |

#### `vam_agent`

| Column | Type | Flags |
|--------|------|-------|
| `client_id` | `int4` |  |
| `service_id` | `int4` |  |
| `sspc_url` | `varchar(255)` |  |
| `resource_name` | `varchar(80)` |  |

#### `vam_agent_account`

| Column | Type | Flags |
|--------|------|-------|
| `client_id` | `int4` |  |
| `service_id` | `int4` |  |
| `sspc_url` | `varchar(255)` |  |
| `login` | `varchar(80)` |  |
| `password` | `varchar(80)` |  |

#### `vam_billing_account`

| Column | Type | Flags |
|--------|------|-------|
| `client_id` | `int4` | NOT NULL |
| `sspc_url` | `varchar(255)` |  |
| `initial_address_url` | `varchar(255)` |  |
| `login` | `varchar(80)` |  |
| `password` | `varchar(80)` |  |

#### `vam_cache`

| Column | Type | Flags |
|--------|------|-------|
| `href` | `varchar(255)` |  |
| `last_modified` | `timestamptz` |  |
| `content` | `text` |  |
| `type` | `varchar(80)` |  |
| `id` | `serial` | PK · auto · NOT NULL |

#### `vam_client`

| Column | Type | Flags |
|--------|------|-------|
| `client_id` | `int4` | NOT NULL |
| `sspc_url` | `varchar(255)` |  |
| `creation_phase` | `int4` | NOT NULL |
| `resource_name` | `varchar(80)` |  |

#### `vam_configuration`

| Column | Type | Flags |
|--------|------|-------|
| `client_id` | `int4` |  |
| `service_id` | `int4` |  |
| `sspc_url` | `varchar(255)` |  |
| `resource_name` | `varchar(80)` |  |

#### `vam_escalation_definition`

| Column | Type | Flags |
|--------|------|-------|
| `client_id` | `int4` |  |
| `service_id` | `int4` |  |
| `sspc_url` | `varchar(255)` |  |
| `resource_name` | `varchar(80)` |  |

#### `vam_host`

| Column | Type | Flags |
|--------|------|-------|
| `client_id` | `int4` | NOT NULL |
| `service_id` | `int4` | NOT NULL |
| `sspc_url` | `varchar(255)` |  |
| `creation_phase` | `int4` | NOT NULL |
| `resource_name` | `varchar(80)` |  |

#### `vam_resources`

| Column | Type | Flags |
|--------|------|-------|
| `resource` | `varchar(80)` |  |
| `parent_resource` | `varchar(80)` |  |
| `resource_property` | `varchar(80)` |  |
| `list_container` | `varchar(80)` |  |
| `id` | `serial` | PK · auto · NOT NULL |

#### `vmware_clusters`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `service_id` | `int4` | → customer_products.id |
| `parent_service_id` | `int4` | → customer_products.id |

#### `vmware_guests`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `service_id` | `int4` | → customer_products.id |
| `parent_service_id` | `int4` | → customer_products.id |

#### `vmware_hosts`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `service_id` | `int4` | → customer_products.id |
| `parent_service_id` | `int4` | → customer_products.id |

#### `vmware_vcenters`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `service_id` | `int4` | → customer_products.id |

#### `volume_discount_percentage`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `threshold` | `int4` | NOT NULL |
| `discount` | `numeric` | NOT NULL |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `wallet_responses_pl`

| Column | Type | Flags |
|--------|------|-------|
| `code` | `serial` | PK · auto · NOT NULL |
| `response` | `varchar` |  |

#### `web_server_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `code` | `text` | NOT NULL |
| `description` | `text` | NOT NULL |

#### `widget_input_parameters`

| Column | Type | Flags |
|--------|------|-------|
| `widget_id` | `int4` | PK · NOT NULL · → widgets.widget_id |
| `parameter_id` | `serial` | PK · auto · NOT NULL |
| `parameter_name` | `varchar(64)` | NOT NULL |
| `parameter_description` | `varchar(255)` | NOT NULL |
| `data_type_id` | `int4` | NOT NULL |

#### `widget_output_parameters`

| Column | Type | Flags |
|--------|------|-------|
| `widget_id` | `int4` | PK · NOT NULL · → widgets.widget_id |
| `parameter_id` | `int4` | PK · NOT NULL |
| `parameter_name` | `varchar(64)` | NOT NULL |
| `parameter_description` | `varchar(255)` | NOT NULL |
| `data_type_id` | `int4` | NOT NULL |

#### `widget_transaction_states`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `state` | `varchar` |  |
| `name` | `varchar` |  |

#### `widget_types_pl`

| Column | Type | Flags |
|--------|------|-------|
| `widget_type_id` | `serial` | PK · auto · NOT NULL |
| `name` | `varchar(64)` | NOT NULL |
| `description` | `varchar(255)` | NOT NULL |
| `sort_order` | `int4` | NOT NULL |
| `is_active` | `bool` | NOT NULL |

#### `widgets`

| Column | Type | Flags |
|--------|------|-------|
| `widget_id` | `serial` | PK · auto · NOT NULL |
| `widget_name` | `varchar(64)` | NOT NULL |
| `widget_description` | `varchar(255)` | NOT NULL |
| `widget_author` | `varchar(64)` | NOT NULL |
| `date_created` | `timestamp` | NOT NULL |
| `widget_type_id` | `int4` | NOT NULL · → widget_types_pl.widget_type_id |
| `is_active` | `bool` | NOT NULL |
| `widget_url` | `varchar` |  |
| `widget_role` | `varchar(64)` |  |
| `hide_role` | `bool` |  |

#### `workflow_event_types`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `name` | `text` | NOT NULL |
| `tracked` | `bool` | NOT NULL |
| `allow_duplicates` | `bool` | NOT NULL |

#### `workflow_notifications`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `service_id` | `int4` | NOT NULL · → customer_products.id |
| `workflow_instance_id` | `int4` |  |
| `event_type_id` | `int4` | NOT NULL · → workflow_event_types.id |
| `created` | `timestamptz` | NOT NULL |
| `last_updated` | `timestamptz` | NOT NULL |
| `status` | `varchar` | NOT NULL |
| `message` | `varchar` |  |

#### `xref_cloud_storage_policy_component`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `atmos_key` | `varchar(32)` | NOT NULL |
| `description` | `varchar(200)` |  |
| `type` | `varchar(32)` | NOT NULL |
| `component_id` | `int4` | → components.id |

#### `xref_cloud_storage_policy_concession`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `type` | `varchar(32)` | NOT NULL |
| `app_config_id` | `int4` | NOT NULL · → app_config.id |
| `component_id` | `int4` | NOT NULL · → components.id |
| `created` | `timestamp` | NOT NULL |
| `created_by` | `varchar(32)` | NOT NULL |
| `last_modified` | `timestamp` | NOT NULL |
| `last_modified_by` | `varchar(32)` | NOT NULL |

#### `xref_cloud_storage_subtenants_services`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `subtenant_id` | `varchar(50)` | NOT NULL |
| `service_id` | `int4` | NOT NULL · → customer_products.id |

#### `xref_customer_rbac_roles`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `contact_id` | `int4` | NOT NULL · → contact.contact_id |
| `section_id` | `int4` | NOT NULL · → my_rbac_sections.id |
| `permissions` | `int4` | NOT NULL |

#### `xref_customer_support_type_sub_type`

| Column | Type | Flags |
|--------|------|-------|
| `customer_support_type_id` | `int4` | NOT NULL · → customer_support_type.id |
| `customer_support_sub_type_id` | `int4` | NOT NULL · → customer_support_sub_type.id |
| `num_tickets_required` | `int4` |  |
| `hours_for_resolution` | `int4` |  |
| `support_handler_id` | `int4` | NOT NULL · → customer_support_handler.id |
| `notes` | `text` |  |
| `special_form_command` | `text` |  |
| `is_customer_facing` | `bool` |  |
| `id` | `serial` | PK · auto · NOT NULL |

#### `xref_rbac_pages_to_sections`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `page_id` | `int4` | NOT NULL · → my_rbac_pages.id |
| `section_id` | `int4` | NOT NULL · → my_rbac_sections.id |

#### `xref_roles_employees`

| Column | Type | Flags |
|--------|------|-------|
| `roles_id` | `int4` |  |
| `employees_id` | `int4` | → employees.id |
| `id` | `serial` | PK · auto · NOT NULL |

#### `xref_services_private_net`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `private_net_id` | `int4` | NOT NULL · → client_private_net.id |
| `service_id` | `int4` | NOT NULL · → customer_products.id |
| `created` | `timestamptz` | NOT NULL |
| `created_by` | `text` | NOT NULL |
| `last_modified` | `timestamptz` | NOT NULL |
| `last_modified_by` | `text` | NOT NULL |

#### `xref_services_private_rack`

| Column | Type | Flags |
|--------|------|-------|
| `id` | `serial` | PK · auto · NOT NULL |
| `private_rack_id` | `int4` | → client_private_rack.id |
| `service_id` | `int4` | → customer_products.id |
| `created` | `timestamptz` |  |
| `created_by` | `text` |  |
| `last_modified` | `timestamptz` |  |
| `last_modified_by` | `text` |  |

#### `xref_ticket_routing_by_product_line`

| Column | Type | Flags |
|--------|------|-------|
| `xref_customer_support_type_sub_type_id` | `int4` | NOT NULL · → xref_customer_support_type_sub_type.id |
| `product_line_id` | `int4` | → product_lines.id |
| `id` | `serial` | PK · auto · NOT NULL |

#### `zones`

| Column | Type | Flags |
|--------|------|-------|
| `zone_id` | `serial` | PK · auto · NOT NULL |
| `zone_country_id` | `int4` | NOT NULL |
| `zone_code` | `text` | NOT NULL |
| `zone_name` | `text` | NOT NULL |

---

## Inaccessible Tables

103 tables were found in the XML schema but returned `permission denied` (or another error) when queried as `sb_readonly`.

| Table | XML Row Count | Error |
|-------|--------------|-------|
| `c2ouat` | 218 | permission denied |
| `capability_types` | 3 | permission denied |
| `cloud_external_entities` | 262 | permission denied |
| `cloud_external_entity_identifiers` | 524 | permission denied |
| `cloud_external_entity_types` | 2 | permission denied |
| `cloud_external_field_types` | 4 | permission denied |
| `cloud_option_statuses` | 5 | permission denied |
| `cloud_option_types` | 3 | permission denied |
| `cloud_options` | 190 | permission denied |
| `cloud_options_external_entities` | 175 | permission denied |
| `cloud_profiles` | 109 | permission denied |
| `cloud_profiles_external_entities` | 109 | permission denied |
| `cloud_types` | 1 | permission denied |
| `components_tags` | 210 | permission denied |
| `connectivity_carriers` | 14 | permission denied |
| `contact_ids_need_permissions` | 44,081 | permission denied |
| `customer_support_type_list` | 0 | permission denied |
| `order_line_item_details_removed` | 29 | permission denied |
| `order_status_audit` | 547 | permission denied |
| `overage_report` | 1 | permission denied |
| `overage_report_custom` | 0 | permission denied |
| `overage_report_new_sflow_servers` | 1 | permission denied |
| `product_catalog_tags` | 144 | permission denied |
| `tags` | 32 | permission denied |
| `view_active_pricebook` | 0 | permission denied |
| `view_active_promotions` | 0 | permission denied |
| `view_attribute_groups` | 0 | permission denied |
| `view_client_bag_services` | 0 | permission denied |
| `view_client_bags` | 0 | permission denied |
| `view_client_bandwidth_allowance` | 0 | permission denied |
| `view_client_bandwidth_allowance_by_bag` | 0 | permission denied |
| `view_client_bandwidth_allowance_by_datacenter` | 0 | permission denied |
| `view_client_bandwidth_allowance_by_service` | 0 | permission denied |
| `view_client_contact_roles` | 0 | permission denied |
| `view_client_contacts` | 0 | permission denied |
| `view_client_error_statuses` | 0 | permission denied |
| `view_client_events` | 0 | permission denied |
| `view_client_orders` | 0 | permission denied |
| `view_client_payment_methods` | 0 | permission denied |
| `view_client_relations` | 0 | permission denied |
| `view_client_service_options` | 0 | permission denied |
| `view_client_services` | 0 | permission denied |
| `view_client_solution_services` | 0 | permission denied |
| `view_client_solutions` | 0 | permission denied |
| `view_client_tax_registration` | 0 | permission denied |
| `view_client_types` | 0 | permission denied |
| `view_clients` | 0 | permission denied |
| `view_clients_watchers` | 0 | permission denied |
| `view_cloud_storage_tiered_discounts` | 0 | permission denied |
| `view_component_capabilities` | 0 | permission denied |
| `view_component_license_keys` | 0 | permission denied |
| `view_component_provided_resources` | 0 | permission denied |
| `view_component_required_resources` | 0 | permission denied |
| `view_component_type_capabilities` | 0 | permission denied |
| `view_component_types` | 0 | permission denied |
| `view_components` | 0 | permission denied |
| `view_contract_types` | 0 | permission denied |
| `view_control_scan_ip_addresses` | 0 | permission denied |
| `view_countries_intergovernmental_organizations` | 0 | permission denied |
| `view_customer_support_faq` | 0 | permission denied |
| `view_customer_support_faq_product_lines` | 0 | permission denied |
| `view_customers_attributes` | 0 | permission denied |
| `view_customers_controlscan_credentials` | 0 | permission denied |
| `view_employee_client_relations_roles_matrix` | 0 | permission denied |
| `view_employee_roles` | 0 | permission denied |
| `view_employee_username` | 0 | permission denied |
| `view_item_tax_schedule` | 0 | permission denied |
| `view_multicurrency_pricebook` | 0 | permission denied |
| `view_oc_cart` | 0 | permission denied |
| `view_oc_cart_components` | 0 | permission denied |
| `view_oc_cart_default_removed_components` | 0 | permission denied |
| `view_order_commission_split` | 0 | permission denied |
| `view_order_entry_solution_details` | 0 | permission denied |
| `view_order_line_item_details` | 0 | permission denied |
| `view_order_line_items` | 0 | permission denied |
| `view_payment_transactions` | 0 | permission denied |
| `view_preconfigured_bundle_mapping` | 0 | permission denied |
| `view_pricebook` | 0 | permission denied |
| `view_product_allowed_components` | 0 | permission denied |
| `view_product_catalog` | 0 | permission denied |
| `view_product_frameworks` | 0 | permission denied |
| `view_product_templates` | 0 | permission denied |
| `view_promotion_criteria_details` | 0 | permission denied |
| `view_promotion_effect_criteria_details` | 0 | permission denied |
| `view_promotion_effects_details` | 0 | permission denied |
| `view_queue_messages` | 0 | permission denied |
| `view_resources` | 0 | permission denied |
| `view_service_cancellation_queue` | 0 | permission denied |
| `view_service_events` | 0 | permission denied |
| `view_service_option_raid_configuration` | 0 | permission denied |
| `view_service_options_capacity_as_gb` | 0 | permission denied |
| `view_service_payment_methods` | 0 | permission denied |
| `view_service_workflow_matrix` | 0 | permission denied |
| `view_services_without_device` | 0 | permission denied |
| `view_statistics_orders` | 0 | permission denied |
| `view_statistics_orders_by_status` | 0 | permission denied |
| `view_statistics_services` | 0 | permission denied |
| `view_statistics_services_by_datacenter` | 0 | permission denied |
| `view_statistics_services_by_status` | 0 | permission denied |
| `view_statistics_services_by_type` | 0 | permission denied |
| `view_ticket_routing_by_product_line` | 0 | permission denied |
| `view_xref_cloud_storage_policy_component` | 0 | permission denied |
| `view_xref_cloud_storage_policy_concession` | 0 | permission denied |

---

## Access Audit Summary

| Metric | Value |
|--------|-------|
| Total tables in schema | 436 |
| Accessible | 333 |
| Denied | 103 |
| DB user | `sb_readonly` |
| DB host | `db1.peer1.com:5432` |
| SSH tunnel via | `10.121.21.20` |
| Generated | 2026-04-14 07:34 |
