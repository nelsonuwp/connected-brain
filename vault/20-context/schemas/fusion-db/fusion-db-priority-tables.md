# Fusion DB — Priority Tables (AccountIntel)

**Group:** `priority-tables`  
**Tables in group:** 11  
**Accessible:** 11  
**Approximate total rows:** 312,178,031  
**Generated:** 2026-05-08 15:54  

## Overview

All 14 tables identified as high-value for the AccountIntel pipeline. This file is a single-stop reference for the core data model — includes customer records, products, billing, people, and infrastructure anchors. Most pipeline stages will touch at least one table listed here.

---

## Table Summary

| Table | Row Count | Columns | Description |
|-------|-----------|---------|-------------|
| `cancellation_category` | ~29 | 4 | Records for cancellation category |
| `client_relations` | ~25,713 | 5 | Records for client relations |
| `client_relations_roles` | ~5 | 3 | Lookup/reference table for client relations roles |
| `customer_products` | ~162,775 | 24 | Records for customer products |
| `customers` | ~25,182 | 17 | Records for customers |
| `employees` | ~5,327 | 12 | Records for employees |
| `exchange_rates` | ~15 | 6 | Records for exchange rates |
| `history_customer_products` | ~311,633,536 | 20 | Audit/history log for `customer_products` |
| `product_lines` | ~8 | 5 | Lookup/reference table for product lines |
| `service_billing_details` | ~162,715 | 9 | Records for service billing details |
| `xref_customer_products_dcc` | ~162,726 | 4 | Cross-reference/join table |

---

## Column Detail

### `cancellation_category`

**Status:** ✅ ~29 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `category` | `text` | yes |  |  |
| `sort_order` | `int4` | yes |  |  |
| `in_portal` | `bool` | yes |  |  |

**Indexes:**
- `cancellation_category_pkey` — UNIQUE (`id`)

---

### `client_relations`

**Status:** ✅ ~25,713 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | no | PK · NOT NULL | Primary key |
| `employee_id` | `int4` | no | PK · NOT NULL | Primary key |
| `product_line_id` | `int4` | no | PK · NOT NULL | Primary key |
| `client_relations_role_id` | `int4` | no | PK · NOT NULL | Primary key |
| `created_date` | `timestamptz` | no | NOT NULL | Date value |

**Indexes:**
- `client_relations_pkey` — UNIQUE (`client_id`, `employee_id`, `product_line_id`, `client_relations_role_id`)
- `client_relations_client_idx` — (`client_id`)

---

### `client_relations_roles`

**Status:** ✅ ~5 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `description` | `text` | yes |  |  |

**Indexes:**
- `client_relations_roles_pkey` — UNIQUE (`id`)
- `client_relations_roles_name_key` — UNIQUE (`name`)

---

### `customer_products`

**Status:** ✅ ~162,775 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `customers_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `customer_order_id` | `int4` | yes |  | Foreign key → `order_line_items.id` |
| `customer_product_idnum` | `int4` | no | NOT NULL |  |
| `product_catalog_id` | `int4` | no | NOT NULL | Foreign key → `product_catalog.id` |
| `products_model` | `text` | yes |  |  |
| `products_name` | `text` | no | NOT NULL | Human-readable name |
| `mrc` | `numeric` | yes |  |  |
| `products_status_id` | `int4` | no | NOT NULL | Foreign key → `customer_products_status_options.id` |
| `first_online` | `timestamptz` | yes |  |  |
| `hide_in_portal` | `bool` | yes |  |  |
| `cancellation_category` | `int4` | yes |  | Foreign key → `cancellation_category.id` |
| `cancellation_comments` | `text` | yes |  |  |
| `products_nickname` | `varchar(64)` | no | NOT NULL |  |
| `service_type_id` | `int4` | no | NOT NULL | Foreign key → `service_type_pl.service_type_id` |
| `modified_by` | `int4` | no | NOT NULL | Foreign key → `employees.id` |
| `setup` | `numeric` | no | NOT NULL |  |
| `billable` | `bool` | no | NOT NULL |  |
| `currency` | `varchar(3)` | no | NOT NULL | Foreign key → `currencies.code` |
| `product_line_id` | `int4` | no | NOT NULL | Foreign key → `product_lines.id` |
| `exchange_rate` | `numeric` | no | NOT NULL |  |
| `is_virtual` | `bool` | no | NOT NULL |  |
| `rate` | `numeric` | yes |  |  |
| `is_qtc` | `bool` | yes |  |  |

**Indexes:**
- `customer_products_pkey` — UNIQUE (`id`)
- `customer_product_id_status` — (`id`, `products_status_id`)
- `customer_products_client_id_status_id_product_line_id_id` — (`customers_id`, `products_status_id`, `product_line_id`)
- `customer_products_order_id` — UNIQUE (`customer_order_id`)
- `unique_customer_id_customer_product_idnum` — UNIQUE (`customers_id`, `customer_product_idnum`)
- `unique_customer_products_nickname` — UNIQUE (`customers_id`, `products_nickname`)

---

### `customers`

**Status:** ✅ ~25,182 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `customers_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `type_id` | `int4` | no | NOT NULL | Foreign key → `client_types_pl.client_type_id` |
| `company_name` | `varchar(255)` | no | NOT NULL | Human-readable name |
| `blacklisted` | `bool` | no | NOT NULL |  |
| `referred_by` | `int4` | yes |  | Foreign key → `customers.customers_id` |
| `overage_rate` | `numeric` | no | NOT NULL |  |
| `error_status` | `bool` | no | NOT NULL | Status code or label |
| `shopping_cart_only` | `bool` | no | NOT NULL |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | yes |  | Timestamp |
| `payment_term` | `varchar(21)` | yes |  | Foreign key → `payment_terms.payment_term` |
| `preferred_currency` | `varchar(3)` | yes |  | Foreign key → `currencies.code` |
| `disabled` | `timestamptz` | yes |  |  |
| `disabled_by` | `varchar(32)` | yes |  |  |
| `client_industries_id` | `int4` | yes |  | Foreign key → `client_industries.id` |

**Indexes:**
- `customers_pkey` — UNIQUE (`customers_id`)
- `customers_customers_id_company_name_idx` — (`customers_id`, `company_name`)

---

### `employees`

**Status:** ✅ ~5,327 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `first_name` | `text` | no | NOT NULL | Human-readable name |
| `middle_initial` | `bpchar` | yes |  |  |
| `last_name` | `text` | no | NOT NULL | Human-readable name |
| `suffix_name` | `text` | yes |  | Human-readable name |
| `email_address` | `text` | no | NOT NULL | Email address |
| `title` | `text` | no | NOT NULL |  |
| `username` | `text` | no | NOT NULL |  |
| `logged_on` | `bool` | yes |  |  |
| `phone_local` | `varchar(30)` | yes |  | Phone number |
| `phone_toll_free` | `varchar(30)` | yes |  | Phone number |
| `phone_extension` | `varchar(10)` | yes |  | Phone number |

**Indexes:**
- `employees_pkey` — UNIQUE (`id`)
- `employees_username_key` — UNIQUE (`username`)

---

### `exchange_rates`

**Status:** ✅ ~15 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `ocean_exchange_rate_id` | `varchar(15)` | yes |  | Identifier linking to related record |
| `gp_exchange_rate_id` | `varchar(15)` | yes |  | Identifier linking to related record |
| `functional_currency` | `varchar(3)` | no | PK · NOT NULL | Primary key |
| `originating_currency` | `varchar(3)` | no | PK · NOT NULL | Primary key |
| `exchange_rate` | `numeric` | no | NOT NULL |  |
| `last_modified` | `timestamp` | no | NOT NULL | Timestamp |

**Indexes:**
- `exchange_rates_pkey` — UNIQUE (`functional_currency`, `originating_currency`)

---

### `history_customer_products`

**Status:** ✅ ~311,633,536 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `customers_id` | `int4` | yes |  | Identifier linking to related record |
| `customer_product_idnum` | `int4` | yes |  |  |
| `products_model` | `text` | yes |  |  |
| `products_name` | `text` | yes |  | Human-readable name |
| `products_status_id` | `int4` | yes |  | Identifier linking to related record |
| `cancellation_category` | `int4` | yes |  |  |
| `cancellation_comments` | `text` | yes |  |  |
| `products_nickname` | `varchar(100)` | yes |  |  |
| `service_type_id` | `int4` | yes |  | Identifier linking to related record |
| `modified_by` | `int4` | yes |  | Timestamp |
| `archive_date` | `timestamptz` | yes |  | Date value |
| `mrc` | `numeric` | yes |  |  |
| `setup` | `numeric` | yes |  |  |
| `billable` | `bool` | yes |  |  |
| `currency` | `varchar(3)` | yes |  |  |
| `product_line_id` | `int4` | yes |  | Identifier linking to related record |
| `exchange_rate` | `numeric` | yes |  |  |
| `history_customer_products_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `rate` | `numeric` | yes |  |  |

**Indexes:**
- `history_customer_products_pkey` — UNIQUE (`history_customer_products_id`)
- `history_customer_products_archive_date_idx` — (`id`, `archive_date`)
- `history_customer_products_id` — (`id`)
- `history_customer_products_modified_idx` — (`id`, `modified_by`, `archive_date`)

---

### `product_lines`

**Status:** ✅ ~8 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(255)` | no | NOT NULL |  |
| `in_order_entry` | `bool` | no | NOT NULL |  |
| `in_shopping_cart` | `bool` | no | NOT NULL |  |
| `abbr` | `varchar(64)` | yes |  |  |

**Indexes:**
- `product_lines_pkey` — UNIQUE (`id`)
- `product_lines_name_key` — UNIQUE (`name`)

---

### `service_billing_details`

**Status:** ✅ ~162,715 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `service_id` | `int4` | no | PK · NOT NULL | Primary key |
| `contract_id` | `varchar(32)` | yes |  | Identifier linking to related record |
| `billing_day` | `int4` | yes |  |  |
| `billing_frequency` | `int4` | no | NOT NULL |  |
| `contract_length` | `int4` | no | NOT NULL | Foreign key → `contract_lengths.contract_length` |
| `payment_method_id` | `int4` | yes |  | Foreign key → `client_payment_methods.id` |
| `purchase_order` | `varchar(32)` | yes |  |  |
| `promotion_id` | `int4` | yes |  | Foreign key → `promotions.id` |
| `on_hold` | `bool` | no | NOT NULL |  |

**Indexes:**
- `service_billing_details_pkey` — UNIQUE (`service_id`)
- `service_billing_details_contract_id_key` — UNIQUE (`service_id`, `contract_id`)

---

### `xref_customer_products_dcc`

**Status:** ✅ ~162,726 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `customer_products_id` | `int4` | yes |  | Foreign key → `customer_products.id` |
| `datacenter_id` | `int4` | yes |  | Foreign key → `sb_datacenter.id` |
| `device_id` | `varchar(64)` | yes |  | Identifier linking to related record |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `xref_customer_products_dcc_pkey` — UNIQUE (`id`)
- `xref_customer_products_dcc_customer_products_id_key` — UNIQUE (`customer_products_id`, `datacenter_id`, `device_id`)
- `xref_customer_products_dcc_datacenter_idx` — (`datacenter_id`)
- `xref_customer_products_dcc_service_idx` — (`customer_products_id`)

---

## Relationships

| From | | To |
|------|---|-----|
| `customer_products`.`customer_order_id` | → | `order_line_items`.`id` |
| `customer_products`.`product_catalog_id` | → | `product_catalog`.`id` |
| `customer_products`.`products_status_id` | → | `customer_products_status_options`.`id` |
| `customer_products`.`service_type_id` | → | `service_type_pl`.`service_type_id` |
| `customer_products`.`currency` | → | `currencies`.`code` |
| `customers`.`type_id` | → | `client_types_pl`.`client_type_id` |
| `customers`.`payment_term` | → | `payment_terms`.`payment_term` |
| `customers`.`preferred_currency` | → | `currencies`.`code` |
| `customers`.`client_industries_id` | → | `client_industries`.`id` |
| `exchange_rates`.`functional_currency` | → | `currencies`.`code` |
| `exchange_rates`.`originating_currency` | → | `currencies`.`code` |
| `service_billing_details`.`contract_length` | → | `contract_lengths`.`contract_length` |
| `service_billing_details`.`payment_method_id` | → | `client_payment_methods`.`id` |
| `service_billing_details`.`promotion_id` | → | `promotions`.`id` |
| `xref_customer_products_dcc`.`datacenter_id` | → | `sb_datacenter`.`id` |
| `client_relations_product_line_independent`.`client_relations_role_id` | → | `client_relations_roles`.`id` |
| `employee_client_relations_roles_matrix`.`client_relations_role_id` | → | `client_relations_roles`.`id` |
| `client_bag_services`.`service_id` | → | `customer_products`.`id` |
| `client_firewall_vlan`.`service_id` | → | `customer_products`.`id` |
| `client_loadbalancer_vlan`.`service_id` | → | `customer_products`.`id` |
| `client_private_rack`.`service_id` | → | `customer_products`.`id` |
| `client_solution_services`.`service_id` | → | `customer_products`.`id` |
| `client_tickets`.`service_id` | → | `customer_products`.`id` |
| `cloud_storage_attributes`.`object_id` | → | `customer_products`.`id` |
| `customer_products_attributes`.`object_id` | → | `customer_products`.`id` |
| `customer_products_status_history`.`customer_product_id` | → | `customer_products`.`id` |
| `order_entry_solution_node`.`service_id` | → | `customer_products`.`id` |
| `order_line_item_migrated_services`.`service_id` | → | `customer_products`.`id` |
| `provisioning_tickets`.`service_id` | → | `customer_products`.`id` |
| `sb_customer_product_log`.`customer_product_id` | → | `customer_products`.`id` |
| `service_cancellation_queue`.`service_id` | → | `customer_products`.`id` |
| `service_licenses`.`service_id` | → | `customer_products`.`id` |
| `service_notes`.`service_id` | → | `customer_products`.`id` |
| `service_options`.`customer_products_id` | → | `customer_products`.`id` |
| `ticket_support_times`.`service_id` | → | `customer_products`.`id` |
| `vmware_clusters`.`parent_service_id` | → | `customer_products`.`id` |
| `vmware_clusters`.`service_id` | → | `customer_products`.`id` |
| `vmware_guests`.`parent_service_id` | → | `customer_products`.`id` |
| `vmware_guests`.`service_id` | → | `customer_products`.`id` |
| `vmware_hosts`.`parent_service_id` | → | `customer_products`.`id` |
| `vmware_hosts`.`service_id` | → | `customer_products`.`id` |
| `vmware_vcenters`.`service_id` | → | `customer_products`.`id` |
| `workflow_notifications`.`service_id` | → | `customer_products`.`id` |
| `xref_cloud_storage_subtenants_services`.`service_id` | → | `customer_products`.`id` |
| `xref_services_private_net`.`service_id` | → | `customer_products`.`id` |
| `xref_services_private_rack`.`service_id` | → | `customer_products`.`id` |
| `billable_ticket_invoicing`.`client_id` | → | `customers`.`customers_id` |
| `certificate_company`.`customers_id` | → | `customers`.`customers_id` |
| `client_bags`.`client_id` | → | `customers`.`customers_id` |
| `client_error_statuses`.`client_id` | → | `customers`.`customers_id` |
| `client_eula_acceptance`.`client_id` | → | `customers`.`customers_id` |
| `client_notes`.`client_id` | → | `customers`.`customers_id` |
| `client_orders`.`client_id` | → | `customers`.`customers_id` |
| `client_payment_methods`.`client_id` | → | `customers`.`customers_id` |
| `client_permission_roles`.`client_id` | → | `customers`.`customers_id` |
| `client_permission_users`.`client_id` | → | `customers`.`customers_id` |
| `client_private_net`.`client_id` | → | `customers`.`customers_id` |
| `client_private_rack`.`client_id` | → | `customers`.`customers_id` |
| `client_relations_product_line_independent`.`client_id` | → | `customers`.`customers_id` |
| `client_solutions`.`client_id` | → | `customers`.`customers_id` |
| `client_tax_registrations`.`client_id` | → | `customers`.`customers_id` |
| `client_tickets`.`client_id` | → | `customers`.`customers_id` |
| `client_zones`.`client_id` | → | `customers`.`customers_id` |
| `clients_watchers`.`client_id` | → | `customers`.`customers_id` |
| `config_codes`.`customer_id` | → | `customers`.`customers_id` |
| `contact`.`customers_id` | → | `customers`.`customers_id` |
| `customer_tam`.`customers_id` | → | `customers`.`customers_id` |
| `customers_attributes`.`object_id` | → | `customers`.`customers_id` |
| `eula`.`client_id` | → | `customers`.`customers_id` |
| `fraud_gateway_transactions`.`client_id` | → | `customers`.`customers_id` |
| `login_history`.`client_id` | → | `customers`.`customers_id` |
| `nbt_invoices`.`customer_id` | → | `customers`.`customers_id` |
| `portal_login`.`client_id` | → | `customers`.`customers_id` |
| `sb_customer_log`.`customers_id` | → | `customers`.`customers_id` |
| `sessions`.`client_id` | → | `customers`.`customers_id` |
| `ticket_support_times`.`client_id` | → | `customers`.`customers_id` |
| `cart`.`assisted_by` | → | `employees`.`id` |
| `client_news`.`who` | → | `employees`.`id` |
| `client_relations_product_line_independent`.`employee_id` | → | `employees`.`id` |
| `clients_watchers`.`employee_id` | → | `employees`.`id` |
| `customer_tam`.`employees_id` | → | `employees`.`id` |
| `employee_client_relations_quotas`.`employee_id` | → | `employees`.`id` |
| `employee_client_relations_roles_matrix`.`employee_id` | → | `employees`.`id` |
| `order_commission_split`.`employee_id` | → | `employees`.`id` |
| `xref_roles_employees`.`employees_id` | → | `employees`.`id` |
| `billable_ticket_invoicing`.`username` | → | `employees`.`username` |
| `client_orders`.`entered_by` | → | `employees`.`username` |
| `portal_login`.`username` | → | `employees`.`username` |
| `contract_types`.`product_line_id` | → | `product_lines`.`id` |
| `customer_support_faq_product_lines`.`product_line_id` | → | `product_lines`.`id` |
| `employee_client_relations_roles_matrix`.`product_line_id` | → | `product_lines`.`id` |
| `order_line_items`.`product_line_id` | → | `product_lines`.`id` |
| `pricebook`.`product_line_id` | → | `product_lines`.`id` |
| `product_class_client_type_discounts`.`product_line` | → | `product_lines`.`id` |
| `product_class_contract_length_discounts`.`product_line` | → | `product_lines`.`id` |
| `service_workflow_matrix`.`product_line_id` | → | `product_lines`.`id` |
| `xref_ticket_routing_by_product_line`.`product_line_id` | → | `product_lines`.`id` |
