# Fusion DB — Customer Core

**Group:** `customer-core`  
**Tables in group:** 4  
**Accessible:** 4  
**Approximate total rows:** 311,821,522  
**Generated:** 2026-05-08 15:54  

## Overview

Core customer identity and lifecycle tables. These are the foundational records for any account — the customer row, their active and historical products, and the reasons products were cancelled. Start here when building account context, churn risk signals, or product adoption timelines.

---

## Table Summary

| Table | Row Count | Columns | Description |
|-------|-----------|---------|-------------|
| `cancellation_category` | ~29 | 4 | Records for cancellation category |
| `customer_products` | ~162,775 | 24 | Records for customer products |
| `customers` | ~25,182 | 17 | Records for customers |
| `history_customer_products` | ~311,633,536 | 20 | Audit/history log for `customer_products` |

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

## Relationships

| From | | To |
|------|---|-----|
| `customer_products`.`customer_order_id` | → | `order_line_items`.`id` |
| `customer_products`.`product_catalog_id` | → | `product_catalog`.`id` |
| `customer_products`.`products_status_id` | → | `customer_products_status_options`.`id` |
| `customer_products`.`service_type_id` | → | `service_type_pl`.`service_type_id` |
| `customer_products`.`modified_by` | → | `employees`.`id` |
| `customer_products`.`currency` | → | `currencies`.`code` |
| `customer_products`.`product_line_id` | → | `product_lines`.`id` |
| `customers`.`type_id` | → | `client_types_pl`.`client_type_id` |
| `customers`.`payment_term` | → | `payment_terms`.`payment_term` |
| `customers`.`preferred_currency` | → | `currencies`.`code` |
| `customers`.`client_industries_id` | → | `client_industries`.`id` |
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
| `service_billing_details`.`service_id` | → | `customer_products`.`id` |
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
| `xref_customer_products_dcc`.`customer_products_id` | → | `customer_products`.`id` |
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
| `client_relations`.`client_id` | → | `customers`.`customers_id` |
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
