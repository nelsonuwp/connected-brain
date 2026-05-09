# Fusion DB — Remaining Accessible Tables (A–H)

**Group:** `remaining-accessible-a-h`  
**Tables in group:** 95  
**Accessible:** 95  
**Approximate total rows:** 35,656,370  
**Generated:** 2026-05-08 15:54  

## Overview

Accessible tables that don't fit neatly into the domain groups above. May include audit logs, configuration tables, cross-reference tables, or legacy tables with low direct relevance to AccountIntel. Worth scanning for unexpected signals (e.g., feature flags, status history).

(Split at 'H' due to size)

---

## Table Summary

| Table | Row Count | Columns | Description |
|-------|-----------|---------|-------------|
| `app_config` | ~29 | 7 | Lookup/reference table for app config |
| `attribute_groupings` | ~35 | 3 | Records for attribute groupings |
| `attribute_groups` | ~7 | 2 | Lookup/reference table for attribute groups |
| `attributes` | ~154 | 3 | Lookup/reference table for attributes |
| `billable_ticket_invoicing` | ~5 | 6 | Records for billable ticket invoicing |
| `bu_alerts` | ~11,110 | 6 | Records for bu alerts |
| `bu_alerts_change_hist` | ~2,496 | 4 | Records for bu alerts change hist |
| `bu_events` | < 1 | 9 | Records for bu events |
| `bu_events_status` | ~8 | 2 | Records for bu events status |
| `bu_prices` | ~125 | 3 | Records for bu prices |
| `bu_usage` | ~18,325,188 | 7 | Records for bu usage |
| `byo_upsell` | ~18 | 3 | Records for byo upsell |
| `capabilities` | ~73 | 3 | Lookup/reference table for capabilities |
| `cart` | < 1 | 14 | Records for cart |
| `cart_order` | ~17 | 9 | Lookup/reference table for cart order |
| `cart_raid_array_drives` | < 1 | 2 | Records for cart raid array drives |
| `cart_raid_arrays` | < 1 | 4 | Records for cart raid arrays |
| `ce_pods` | ~10 | 2 | Records for ce pods |
| `certificate` | ~5,917 | 10 | Records for certificate |
| `certificate_attributes` | ~17,368 | 9 | Records for certificate attributes |
| `certificate_company` | ~5,672 | 10 | Records for certificate company |
| `client_bags` | ~1,119 | 9 | Lookup/reference table for client bags |
| `client_error_statuses` | ~86 | 3 | Records for client error statuses |
| `client_eula_acceptance` | ~20,512 | 6 | Records for client eula acceptance |
| `client_firewall_vlan` | ~623 | 7 | Records for client firewall vlan |
| `client_industries` | ~10 | 3 | Lookup/reference table for client industries |
| `client_loadbalancer_vlan` | < 1 | 7 | Records for client loadbalancer vlan |
| `client_news` | ~23 | 5 | Records for client news |
| `client_notes` | ~19,766 | 6 | Records for client notes |
| `client_order_statuses` | ~30 | 3 | Lookup/reference table for client order statuses |
| `client_order_types` | ~3 | 2 | Lookup/reference table for client order types |
| `client_orders` | ~273,467 | 17 | Records for client orders |
| `client_orders_attributes` | ~287,257 | 9 | Records for client orders attributes |
| `client_private_net` | ~1,215 | 10 | Records for client private net |
| `client_solutions` | ~17,040 | 9 | Lookup/reference table for client solutions |
| `client_tax_registrations` | ~482 | 4 | Records for client tax registrations |
| `client_tax_schedules` | ~8 | 2 | Lookup/reference table for client tax schedules |
| `client_tickets` | ~2,075,256 | 10 | Records for client tickets |
| `client_tickets_attributes` | ~99,785 | 9 | Records for client tickets attributes |
| `client_types_pl` | ~12 | 5 | Records for client types pl |
| `client_zones` | ~8,825 | 7 | Records for client zones |
| `clients_watchers` | ~1,603 | 3 | Records for clients watchers |
| `cloud_storage_attributes` | ~927 | 9 | Records for cloud storage attributes |
| `cloud_storage_bandwidth_types_pl` | ~3 | 3 | Lookup/reference table for cloud storage bandwidth types pl |
| `cloud_storage_tiered_discounts` | ~27 | 8 | Lookup/reference table for cloud storage tiered discounts |
| `communication_type` | ~9 | 2 | Records for communication type |
| `company_type` | ~10 | 2 | Records for company type |
| `config_code_pnet` | ~66 | 3 | Records for config code pnet |
| `config_code_raid_array_drives` | ~493 | 2 | Records for config code raid array drives |
| `config_code_raid_arrays` | ~219 | 4 | Records for config code raid arrays |
| `config_codes` | ~581 | 11 | Maps customers to their subscribed products |
| `contract_lengths` | ~6 | 1 | Records for contract lengths |
| `contract_types` | ~1,724 | 6 | Records for contract types |
| `countries` | ~247 | 5 | Records for countries |
| `countries_currencies` | ~7 | 2 | Records for countries currencies |
| `countries_intergovernmental_organizations` | ~151 | 2 | Records for countries intergovernmental organizations |
| `credit_card_types` | ~4 | 5 | Records for credit card types |
| `currencies` | ~4 | 7 | Records for currencies |
| `customer_support_faq` | ~272 | 6 | Records for customer support faq |
| `customer_support_faq_tags` | ~560 | 3 | Records for customer support faq tags |
| `customer_support_faq_type` | ~36 | 3 | Lookup/reference table for customer support faq type |
| `customer_support_handler` | ~206 | 2 | Lookup/reference table for customer support handler |
| `customer_support_sub_type` | ~330 | 3 | Lookup/reference table for customer support sub type |
| `customer_support_type` | ~62 | 2 | Lookup/reference table for customer support type |
| `customer_tam` | ~193 | 4 | Records for customer tam |
| `customers_attributes` | ~127,364 | 11 | Records for customers attributes |
| `customers_attributes_history` | ~485,984 | 11 | Records for customers attributes history |
| `customers_priority` | ~4 | 2 | Records for customers priority |
| `database_errors` | ~824,313 | 8 | Records for database errors |
| `databasechangelog` | ~184 | 11 | Records for databasechangelog |
| `databasechangeloglock` | ~1 | 4 | Records for databasechangeloglock |
| `email_recipients` | ~245 | 5 | Records for email recipients |
| `email_template_groupings` | ~119 | 3 | Records for email template groupings |
| `email_template_groups` | ~5 | 2 | Lookup/reference table for email template groups |
| `email_templates` | ~238 | 6 | Lookup/reference table for email templates |
| `error_status_types` | ~2 | 2 | Records for error status types |
| `error_statuses` | ~2 | 3 | Records for error statuses |
| `eula` | ~5 | 7 | Lookup/reference table for eula |
| `fraud_gateway_transactions` | ~45,577 | 8 | Records for fraud gateway transactions |
| `history_certificate` | ~31,373 | 13 | Audit/history log for `certificate` |
| `history_client_bags` | ~630,079 | 12 | Audit/history log for `client_bags` |
| `history_client_orders` | ~9,355,367 | 9 | Audit/history log for `client_orders` |
| `history_client_private_net` | ~4,198 | 13 | Audit/history log for `client_private_net` |
| `history_client_solutions` | ~59,510 | 12 | Audit/history log for `client_solutions` |
| `history_client_zones` | ~527,243 | 9 | Audit/history log for `client_zones` |
| `history_customers` | ~244,134 | 18 | Audit/history log for `customers` |
| `history_email_recipients` | ~3,695 | 8 | Audit/history log for `email_recipients` |
| `history_email_templates` | ~2,006 | 9 | Audit/history log for `email_templates` |
| `history_ocean_restrictions` | ~802 | 7 | Audit/history log for `ocean_restrictions` |
| `history_permission_categories` | ~12 | 10 | Audit/history log for `permission_categories` |
| `history_permissions` | ~136 | 12 | Audit/history log for `permissions` |
| `history_preconfigured_bundle_mapping` | ~220 | 4 | Audit/history log for `preconfigured_bundle_mapping` |
| `history_pricebook` | ~93,467 | 15 | Audit/history log for `pricebook` |
| `history_ticket_support_times` | ~2,038,556 | 11 | Audit/history log for `ticket_support_times` |
| `history_volume_discount_percentage` | ~38 | 10 | Audit/history log for `volume_discount_percentage` |

---

## Column Detail

### `app_config`

**Status:** ✅ ~29 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar` | yes |  |  |
| `type` | `varchar` | yes |  |  |
| `default_value` | `varchar` | yes |  |  |
| `value` | `varchar` | yes |  |  |
| `created` | `timestamp` | yes |  | Timestamp |
| `version` | `varchar(4)` | yes |  |  |

**Indexes:**
- `app_config_pkey` — UNIQUE (`id`)
- `app_config_name_key` — UNIQUE (`name`)

---

### `attribute_groupings`

**Status:** ✅ ~35 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `attribute_group_id` | `int4` | no | NOT NULL | Foreign key → `attribute_groups.id` |
| `attribute_id` | `int4` | no | NOT NULL | Foreign key → `attributes.id` |

**Indexes:**
- `attribute_groupings_pkey` — UNIQUE (`id`)

---

### `attribute_groups`

**Status:** ✅ ~7 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(500)` | no | NOT NULL |  |

**Indexes:**
- `attribute_groups_pkey` — UNIQUE (`id`)
- `attribute_groups_name_idx` — UNIQUE (`name`)

---

### `attributes`

**Status:** ✅ ~154 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(500)` | no | NOT NULL |  |
| `data_type` | `varchar(500)` | no | NOT NULL | Type or category classifier |

**Indexes:**
- `attributes_pkey` — UNIQUE (`id`)
- `attributes_name_idx` — UNIQUE (`name`)

---

### `billable_ticket_invoicing`

**Status:** ✅ ~5 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | yes |  | Foreign key → `customers.customers_id` |
| `ticket_id` | `int4` | yes |  | Identifier linking to related record |
| `username` | `text` | yes |  | Foreign key → `employees.username` |
| `bill_amount` | `float8` | yes |  | Monetary amount |
| `original_estimate` | `float8` | yes |  |  |

**Indexes:**
- `billable_ticket_invoicing_pkey` — UNIQUE (`id`)

---

### `bu_alerts`

**Status:** ✅ ~11,110 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `node_name` | `varchar(128)` | yes |  | Human-readable name |
| `threshold` | `int4` | yes |  |  |
| `status` | `varchar(128)` | yes |  |  |
| `customer_products_id` | `int4` | yes |  | Identifier linking to related record |
| `email` | `text` | yes |  | Email address |

**Indexes:**
- `bu_alerts_pkey` — UNIQUE (`id`)
- `unique_customer_products_id` — UNIQUE (`customer_products_id`)

---

### `bu_alerts_change_hist`

**Status:** ✅ ~2,496 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `alert_id` | `int4` | yes |  | Identifier linking to related record |
| `description` | `varchar(128)` | yes |  |  |
| `dt_stamp` | `date` | yes |  |  |

**Indexes:**
- `bu_alerts_change_hist_pkey` — UNIQUE (`id`)

---

### `bu_events`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `node_name` | `varchar(128)` | yes |  | Human-readable name |
| `schedule_start` | `timestamp` | yes |  |  |
| `actual_start` | `timestamp` | yes |  |  |
| `actual_finish` | `timestamp` | yes |  |  |
| `total_time` | `time` | yes |  |  |
| `status_id` | `int4` | yes |  | Identifier linking to related record |
| `node_type_id` | `int4` | yes |  | Identifier linking to related record |
| `customer_products_id` | `int4` | yes |  | Identifier linking to related record |

**Indexes:**
- `bu_events_pkey` — UNIQUE (`id`)

---

### `bu_events_status`

**Status:** ✅ ~8 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `status_id` | `int4` | no | PK · NOT NULL | Primary key |
| `description` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `bu_events_status_pkey` — UNIQUE (`status_id`)

---

### `bu_prices`

**Status:** ✅ ~125 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `service_options_id` | `int4` | yes |  | Identifier linking to related record |
| `price_per_gig` | `float8` | yes |  |  |

**Indexes:**
- `bu_prices_pkey` — UNIQUE (`id`)

---

### `bu_usage`

**Status:** ✅ ~18,325,188 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `node_name` | `varchar(128)` | yes |  | Human-readable name |
| `total_files_stored` | `int4` | yes |  |  |
| `total_mbs_stored` | `numeric` | yes |  |  |
| `dt_stamp` | `date` | yes |  |  |
| `node_type_id` | `int4` | yes |  | Identifier linking to related record |
| `customer_products_id` | `int4` | yes |  | Identifier linking to related record |

**Indexes:**
- `bu_usage_pkey` — UNIQUE (`id`)
- `bu_usage_idx` — (`node_name`)
- `bu_usage_idx2` — (`customer_products_id`)
- `bu_usage_unique_node_idx` — UNIQUE (`node_name`, `dt_stamp`, `node_type_id`)

---

### `byo_upsell`

**Status:** ✅ ~18 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `product_id` | `int4` | no | NOT NULL | Foreign key → `product_catalog.id` |
| `upsell_product_id` | `int4` | no | NOT NULL | Foreign key → `product_catalog.id` |

**Indexes:**
- `byo_upsell_pkey` — UNIQUE (`id`)

---

### `capabilities`

**Status:** ✅ ~73 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `capability_type_id` | `int4` | yes |  | Identifier linking to related record |

**Indexes:**
- `capabilities_pkey` — UNIQUE (`id`)
- `capabilities_name_key` — UNIQUE (`name`)

---

### `cart`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `session_id` | `bpchar` | no | NOT NULL | Foreign key → `sessions.session_id` |
| `product_id` | `int4` | yes |  | Foreign key → `product_catalog.id` |
| `datacenter_id` | `int4` | yes |  | Foreign key → `sb_datacenter.id` |
| `contract_length` | `int4` | no | NOT NULL | Foreign key → `contract_lengths.contract_length` |
| `fqdn` | `varchar(128)` | yes |  |  |
| `setup` | `numeric` | no | NOT NULL |  |
| `mrc` | `numeric` | no | NOT NULL |  |
| `functional_currency` | `varchar(3)` | no | NOT NULL | Foreign key → `currencies.code` |
| `promotion_id` | `int4` | yes |  | Foreign key → `promotions.id` |
| `setup_discount` | `numeric` | yes |  |  |
| `mrc_discount` | `numeric` | yes |  |  |
| `originating_currency` | `varchar(3)` | no | NOT NULL | Foreign key → `currencies.code` |
| `assisted_by` | `int4` | yes |  | Foreign key → `employees.id` |

**Indexes:**
- `cart_pkey` — UNIQUE (`id`)
- `cart_id_session_idx` — (`id`, `session_id`)
- `cart_session_idx` — (`session_id`)

---

### `cart_order`

**Status:** ✅ ~17 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | yes |  |  |
| `description` | `text` | yes |  |  |
| `page` | `int4` | yes |  |  |
| `sort_order` | `int4` | yes |  |  |
| `display_type` | `varchar(16)` | no | NOT NULL | Type or category classifier |
| `unselect_text` | `varchar(64)` | yes |  |  |
| `editable` | `bool` | no | NOT NULL |  |
| `component_type` | `int4` | yes |  | Foreign key → `component_types.id` |

**Indexes:**
- `cart_order_pkey` — UNIQUE (`id`)

---

### `cart_raid_array_drives`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `array_id` | `int4` | no | PK · NOT NULL | Primary key |
| `drive_id` | `int4` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `cart_raid_array_drives_pkey` — UNIQUE (`array_id`, `drive_id`)

---

### `cart_raid_arrays`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `cart_id` | `int4` | yes |  | Foreign key → `cart.id` |
| `level` | `int4` | yes |  | Foreign key → `raid_levels.id` |
| `array_name` | `varchar(32)` | yes |  | Human-readable name |

**Indexes:**
- `cart_raid_arrays_pkey` — UNIQUE (`id`)

---

### `ce_pods`

**Status:** ✅ ~10 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | auto · NOT NULL |  |
| `value` | `varchar(25)` | no | NOT NULL |  |

---

### `certificate`

**Status:** ✅ ~5,917 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `options_licenses_id` | `int4` | no | NOT NULL | Foreign key → `options_licenses.id` |
| `certificate_contact_id` | `int4` | yes |  | Foreign key → `certificate_contacts.contact_id` |
| `certificate_company_id` | `int4` | yes |  | Foreign key → `certificate_company.id` |
| `status` | `varchar(255)` | no | NOT NULL |  |
| `domain` | `text` | yes |  |  |
| `os` | `varchar(32)` | no | NOT NULL |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `text` | yes |  | Timestamp |

**Indexes:**
- `certificate_pkey` — UNIQUE (`id`)

---

### `certificate_attributes`

**Status:** ✅ ~17,368 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `certificate_id` | `int4` | no | NOT NULL | Foreign key → `certificate.id` |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `attribute_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `attribute_group_id` | `int4` | yes |  | Identifier linking to related record |
| `value` | `text` | yes |  |  |

**Indexes:**
- `certificate_attributes_pkey` — UNIQUE (`id`)

---

### `certificate_company`

**Status:** ✅ ~5,672 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `customers_id` | `int4` | no | NOT NULL | Foreign key → `customers.customers_id` |
| `legal_company_name` | `varchar(255)` | yes |  | Human-readable name |
| `duns_number` | `text` | yes |  |  |
| `street_address` | `text` | yes |  | Address field |
| `city` | `text` | yes |  | Address field |
| `state` | `text` | yes |  |  |
| `postal_code` | `text` | yes |  | Short code or identifier |
| `countries_id` | `int4` | yes |  | Foreign key → `countries.countries_id` |
| `company_type_id` | `int4` | yes |  | Foreign key → `company_type.id` |

**Indexes:**
- `certificate_company_pkey` — UNIQUE (`id`)

---

### `client_bags`

**Status:** ✅ ~1,119 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | no | NOT NULL | Foreign key → `customers.customers_id` |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `description` | `text` | yes |  |  |
| `is_active` | `bool` | no | NOT NULL | Boolean state flag |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `client_bags_pkey` — UNIQUE (`id`)
- `unique_client_bag_name` — UNIQUE (`client_id`, `name`)

---

### `client_error_statuses`

**Status:** ✅ ~86 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | yes |  | Foreign key → `customers.customers_id` |
| `error_status_id` | `int4` | yes |  | Foreign key → `error_statuses.id` |

**Indexes:**
- `client_error_statuses_pkey` — UNIQUE (`id`)

---

### `client_eula_acceptance`

**Status:** ✅ ~20,512 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | no | PK · NOT NULL | Primary key |
| `eula_id` | `int4` | no | NOT NULL | Foreign key → `eula.id` |
| `digital_signature` | `varchar(16)` | no | PK · NOT NULL | Primary key |
| `date_accepted` | `timestamp` | yes |  |  |
| `ip_address` | `varchar(50)` | yes |  | Address field |
| `user_agent` | `text` | yes |  |  |

**Indexes:**
- `client_eula_acceptance_pkay` — UNIQUE (`client_id`, `digital_signature`)
- `client_eula_acceptance_client_id_idx` — (`client_id`)

---

### `client_firewall_vlan`

**Status:** ✅ ~623 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `service_id` | `int4` | yes |  | Foreign key → `customer_products.id` |
| `vlan_id` | `int4` | yes |  | Identifier linking to related record |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `text` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `text` | yes |  | Timestamp |

**Indexes:**
- `client_firewall_vlan_pkey` — UNIQUE (`id`)

---

### `client_industries`

**Status:** ✅ ~10 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `active` | `bool` | yes |  | Boolean state flag |

**Indexes:**
- `client_industries_pkey` — UNIQUE (`id`)

---

### `client_loadbalancer_vlan`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `service_id` | `int4` | yes |  | Foreign key → `customer_products.id` |
| `vlan_id` | `int4` | yes |  | Identifier linking to related record |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `text` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `text` | yes |  | Timestamp |

**Indexes:**
- `client_loadbalancer_vlan_pkey` — UNIQUE (`id`)

---

### `client_news`

**Status:** ✅ ~23 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `title` | `varchar(64)` | yes |  |  |
| `description` | `varchar` | yes |  |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `who` | `int4` | yes |  | Foreign key → `employees.id` |

**Indexes:**
- `client_news_pkey` — UNIQUE (`id`)

---

### `client_notes`

**Status:** ✅ ~19,766 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | no | NOT NULL | Foreign key → `customers.customers_id` |
| `message` | `varchar` | no | NOT NULL |  |
| `date` | `timestamptz` | no | NOT NULL |  |
| `who` | `varchar(32)` | no | NOT NULL |  |
| `is_important` | `bool` | no | NOT NULL |  |

**Indexes:**
- `client_notes_pkey` — UNIQUE (`id`)

---

### `client_order_statuses`

**Status:** ✅ ~30 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `description` | `varchar(256)` | yes |  |  |

**Indexes:**
- `client_order_statuses_pkey` — UNIQUE (`id`)
- `client_order_statuses_name_key` — UNIQUE (`name`)

---

### `client_order_types`

**Status:** ✅ ~3 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `client_order_types_pkey` — UNIQUE (`id`)
- `client_order_types_name_key` — UNIQUE (`name`)

---

### `client_orders`

**Status:** ✅ ~273,467 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | yes |  | Foreign key → `customers.customers_id` |
| `status` | `int4` | yes |  | Foreign key → `client_order_statuses.id` |
| `entered_by` | `text` | yes |  | Foreign key → `employees.username` |
| `date` | `timestamptz` | yes |  |  |
| `message` | `varchar` | yes |  |  |
| `order_type_id` | `int4` | no | NOT NULL | Foreign key → `client_order_types.id` |
| `currency` | `varchar(3)` | no | NOT NULL | Foreign key → `currencies.code` |
| `short_term` | `int4` | yes |  |  |
| `release_date` | `date` | yes |  | Date value |
| `sla_days` | `int4` | yes |  |  |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `text` | yes |  | Timestamp |
| `one_off` | `bool` | yes |  |  |
| `effective_date` | `date` | yes |  | Date value |
| `is_qtc` | `bool` | yes |  |  |
| `track_removals` | `bool` | no | NOT NULL |  |

**Indexes:**
- `client_orders_pkey` — UNIQUE (`id`)
- `client_orders_date_idx` — (`date`)

---

### `client_orders_attributes`

**Status:** ✅ ~287,257 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `object_id` | `int4` | no | NOT NULL | Foreign key → `client_orders.id` |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `attribute_id` | `int4` | no | NOT NULL | Foreign key → `attributes.id` |
| `attribute_group_id` | `int4` | yes |  | Identifier linking to related record |
| `value` | `text` | yes |  |  |

**Indexes:**
- `client_orders_attributes_pkey` — UNIQUE (`id`)
- `client_orders_attributes_attribute_id_object_id_idx` — (`object_id`, `attribute_id`)

---

### `client_private_net`

**Status:** ✅ ~1,215 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | no | NOT NULL | Foreign key → `customers.customers_id` |
| `vlan_id` | `int4` | yes |  | Identifier linking to related record |
| `alias` | `text` | no | NOT NULL |  |
| `datacenter_id` | `int4` | no | NOT NULL | Foreign key → `sb_datacenter.id` |
| `netmask` | `int4` | no | NOT NULL |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `text` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `text` | no | NOT NULL | Timestamp |

**Indexes:**
- `client_private_net_pkey` — UNIQUE (`id`)
- `client_private_net_client_id_key` — UNIQUE (`client_id`, `alias`)
- `client_private_net_vlan_id_key` — UNIQUE (`vlan_id`)

---

### `client_solutions`

**Status:** ✅ ~17,040 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | no | NOT NULL | Foreign key → `customers.customers_id` |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `description` | `text` | yes |  |  |
| `attachment` | `varchar` | yes |  |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `client_solutions_pkey` — UNIQUE (`id`)
- `client_solutions_id_key` — UNIQUE (`id`, `name`)

---

### `client_tax_registrations`

**Status:** ✅ ~482 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | no | PK · NOT NULL | Primary key |
| `tax_registration_type_id` | `varchar(16)` | no | PK · NOT NULL | Primary key |
| `tax_registration_value` | `varchar` | no | NOT NULL |  |
| `certificate_received` | `bool` | no | NOT NULL |  |

**Indexes:**
- `client_tax_registrations_pkey` — UNIQUE (`client_id`, `tax_registration_type_id`)
- `client_tax_registrations_client_id_idx` — (`client_id`)

---

### `client_tax_schedules`

**Status:** ✅ ~8 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `varbit` | no | PK · NOT NULL | Primary key |
| `name` | `varchar(16)` | no | NOT NULL |  |

**Indexes:**
- `client_tax_schedules_pkey` — UNIQUE (`id`)
- `client_tax_schedules_name_key` — UNIQUE (`name`)

---

### `client_tickets`

**Status:** ✅ ~2,075,256 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | yes |  | Foreign key → `customers.customers_id` |
| `service_id` | `int4` | yes |  | Foreign key → `customer_products.id` |
| `ticket_id` | `int4` | yes |  | Identifier linking to related record |
| `status` | `varchar(16)` | yes |  |  |
| `location` | `varchar(64)` | yes |  |  |
| `public` | `bool` | yes |  |  |
| `subject` | `varchar(500)` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |
| `last_updated` | `timestamptz` | yes |  | Timestamp |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `client_tickets_pkey` — UNIQUE (`id`)
- `client_tickets_client_id_key` — UNIQUE (`client_id`, `ticket_id`)
- `client_tickets_ticket_id_idx` — UNIQUE (`ticket_id`)
- `unique_ticket_id_location` — UNIQUE (`ticket_id`, `location`)

---

### `client_tickets_attributes`

**Status:** ✅ ~99,785 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `object_id` | `int4` | no | NOT NULL | Foreign key → `client_tickets.ticket_id` |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `attribute_id` | `int4` | no | NOT NULL | Foreign key → `attributes.id` |
| `attribute_group_id` | `int4` | yes |  | Identifier linking to related record |
| `value` | `text` | yes |  |  |

**Indexes:**
- `client_tickets_attributes_pkey` — UNIQUE (`id`)

---

### `client_types_pl`

**Status:** ✅ ~12 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_type_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `description` | `varchar(255)` | no | NOT NULL |  |
| `sort_order` | `int4` | yes |  |  |
| `is_active` | `bool` | yes |  | Boolean state flag |

**Indexes:**
- `client_type_pl_pkey` — UNIQUE (`client_type_id`)

---

### `client_zones`

**Status:** ✅ ~8,825 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | no | NOT NULL | Foreign key → `customers.customers_id` |
| `zone` | `varchar(256)` | no | NOT NULL |  |
| `created` | `timestamp` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `client_zones_pkey` — UNIQUE (`id`)
- `client_zones_client_id_key` — UNIQUE (`client_id`, `zone`)
- `client_zones_idx` — UNIQUE (`zone`)

---

### `clients_watchers`

**Status:** ✅ ~1,603 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | no | NOT NULL | Foreign key → `customers.customers_id` |
| `employee_id` | `int4` | no | NOT NULL | Foreign key → `employees.id` |

**Indexes:**
- `clients_watchers_pkey` — UNIQUE (`id`)
- `clients_watchers_key` — UNIQUE (`client_id`, `employee_id`)

---

### `cloud_storage_attributes`

**Status:** ✅ ~927 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `object_id` | `int4` | no | NOT NULL | Foreign key → `customer_products.id` |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `attribute_id` | `int4` | no | NOT NULL | Foreign key → `attributes.id` |
| `attribute_group_id` | `int4` | yes |  | Identifier linking to related record |
| `value` | `text` | yes |  |  |

**Indexes:**
- `cloud_storage_attributes_pkey` — UNIQUE (`id`)

---

### `cloud_storage_bandwidth_types_pl`

**Status:** ✅ ~3 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(32)` | no | NOT NULL |  |
| `description` | `varchar(200)` | yes |  |  |

**Indexes:**
- `cloud_storage_bandwidth_types_pl_pkey` — UNIQUE (`id`)

---

### `cloud_storage_tiered_discounts`

**Status:** ✅ ~27 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `tier` | `int4` | yes |  |  |
| `discount_amount` | `float8` | yes |  | Monetary amount |
| `threshold` | `int4` | yes |  |  |
| `unit_of_measure_id` | `int4` | yes |  | Foreign key → `unit_of_measure.id` |
| `name` | `varchar(64)` | yes |  |  |
| `component_id` | `int4` | yes |  | Foreign key → `components.id` |
| `currency` | `varchar(4)` | yes |  | Foreign key → `currencies.code` |

**Indexes:**
- `cloud_storage_tiered_discounts_pkey` — UNIQUE (`id`)
- `cloud_storage_tiered_discounts_tier_key` — UNIQUE (`tier`, `currency`, `component_id`)

---

### `communication_type`

**Status:** ✅ ~9 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `communication_type_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(255)` | yes |  |  |

**Indexes:**
- `communication_type_pkey` — UNIQUE (`communication_type_id`)

---

### `company_type`

**Status:** ✅ ~10 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `company_type` | `varchar(64)` | no | NOT NULL | Type or category classifier |

**Indexes:**
- `company_type_pkey` — UNIQUE (`id`)
- `company_type_company_type_key` — UNIQUE (`company_type`)

---

### `config_code_pnet`

**Status:** ✅ ~66 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `config_id` | `int4` | no | PK · NOT NULL | Primary key |
| `config_component_id` | `int4` | no | PK · NOT NULL | Primary key |
| `alias` | `varchar(128)` | no | NOT NULL |  |

**Indexes:**
- `config_code_pnet_pkey` — UNIQUE (`config_id`, `config_component_id`)

---

### `config_code_raid_array_drives`

**Status:** ✅ ~493 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `array_id` | `int4` | no | PK · NOT NULL | Primary key |
| `drive_id` | `int4` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `config_code_raid_array_drives_pkey` — UNIQUE (`array_id`, `drive_id`)

---

### `config_code_raid_arrays`

**Status:** ✅ ~219 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | no | PK · NOT NULL | Primary key |
| `config_id` | `int4` | yes |  | Foreign key → `config_codes.id` |
| `level` | `int4` | yes |  | Foreign key → `raid_levels.id` |
| `array_name` | `varchar(32)` | yes |  | Human-readable name |

**Indexes:**
- `config_code_raid_arrays_pkey` — UNIQUE (`id`)

---

### `config_codes`

**Status:** ✅ ~581 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `code` | `varchar(128)` | no | NOT NULL |  |
| `name` | `varchar(128)` | no | NOT NULL |  |
| `customer_id` | `int4` | no | NOT NULL | Foreign key → `customers.customers_id` |
| `datacenter_id` | `int4` | yes |  | Identifier linking to related record |
| `currency` | `varchar(3)` | no | NOT NULL |  |
| `contract_length` | `int4` | yes |  | Foreign key → `contract_lengths.contract_length` |
| `fqdn` | `varchar(128)` | yes |  |  |
| `product_id` | `int4` | no | NOT NULL | Foreign key → `product_catalog.id` |
| `is_saved` | `bool` | no | NOT NULL |  |
| `is_active` | `bool` | no | NOT NULL | Boolean state flag |

**Indexes:**
- `config_code_pkey` — UNIQUE (`id`)
- `config_codes_code_key` — UNIQUE (`code`)

---

### `contract_lengths`

**Status:** ✅ ~6 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `contract_length` | `int4` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `contract_lengths_pkey` — UNIQUE (`contract_length`)

---

### `contract_types`

**Status:** ✅ ~1,724 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `product_class_id` | `int4` | yes |  | Foreign key → `product_classes.id` |
| `component_category` | `int4` | yes |  | Foreign key → `component_categories.id` |
| `datacenter` | `int4` | no | NOT NULL | Foreign key → `sb_datacenter.id` |
| `product_line_id` | `int4` | no | NOT NULL | Foreign key → `product_lines.id` |
| `contract_type` | `varchar(16)` | no | NOT NULL | Type or category classifier |

**Indexes:**
- `contract_types_pkey` — UNIQUE (`id`)
- `component_category_datacenter_product_line` — UNIQUE (`component_category`, `datacenter`, `product_line_id`)
- `product_class_datacenter_product_line` — UNIQUE (`product_class_id`, `datacenter`, `product_line_id`)

---

### `countries`

**Status:** ✅ ~247 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `countries_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `countries_name` | `text` | no | NOT NULL | Human-readable name |
| `countries_iso_code_2` | `bpchar` | no | NOT NULL |  |
| `countries_iso_code_3` | `bpchar` | no | NOT NULL |  |
| `address_format_id` | `int4` | no | NOT NULL | Identifier linking to related record |

**Indexes:**
- `countries_pkey` — UNIQUE (`countries_id`)
- `countries_countries_iso_code_2_key` — UNIQUE (`countries_iso_code_2`)
- `countries_countries_iso_code_3_key` — UNIQUE (`countries_iso_code_3`)
- `idx_countries_name` — (`countries_name`)

---

### `countries_currencies`

**Status:** ✅ ~7 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `countries_id` | `int4` | no | PK · NOT NULL | Primary key |
| `currency_code` | `varchar(3)` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `countries_currencies_pkey` — UNIQUE (`countries_id`, `currency_code`)

---

### `countries_intergovernmental_organizations`

**Status:** ✅ ~151 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `countries_id` | `int4` | no | PK · NOT NULL | Primary key |
| `igo_id` | `int4` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `countries_intergovernmental_organizations_pkey` — UNIQUE (`countries_id`, `igo_id`)

---

### `credit_card_types`

**Status:** ✅ ~4 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `display_name` | `varchar(100)` | yes |  | Human-readable name |
| `beanstream_value` | `varchar(10)` | yes |  |  |
| `description` | `varchar(100)` | yes |  |  |
| `is_active` | `varchar(100)` | yes |  | Boolean state flag |

**Indexes:**
- `credit_card_types_pkey` — UNIQUE (`id`)

---

### `currencies`

**Status:** ✅ ~4 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `code` | `varchar(3)` | no | PK · NOT NULL | Primary key |
| `currency_name` | `varchar(255)` | no | NOT NULL | Human-readable name |
| `currency_symbol` | `varchar(16)` | no | NOT NULL |  |
| `thousands_separator` | `varchar(1)` | no | NOT NULL |  |
| `decimal_point` | `varchar(1)` | no | NOT NULL |  |
| `display_decimals` | `int4` | no | NOT NULL |  |
| `display_format` | `varchar(32)` | yes |  |  |

**Indexes:**
- `currencies_pkey` — UNIQUE (`code`)

---

### `customer_support_faq`

**Status:** ✅ ~272 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `type_id` | `int4` | yes |  | Foreign key → `customer_support_faq_type.id` |
| `question` | `text` | yes |  |  |
| `answer` | `text` | yes |  |  |
| `order_number` | `int4` | yes |  |  |
| `is_active` | `bool` | no | NOT NULL | Boolean state flag |

**Indexes:**
- `customer_support_faq_pkey` — UNIQUE (`id`)

---

### `customer_support_faq_tags`

**Status:** ✅ ~560 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `customer_support_faq_id` | `int4` | no | NOT NULL | Foreign key → `customer_support_faq.id` |
| `tag` | `text` | no | NOT NULL |  |

**Indexes:**
- `customer_support_faq_tags_pkey` — UNIQUE (`id`)
- `customer_support_faq_tags_customer_support_faq_id_idx` — (`customer_support_faq_id`)

---

### `customer_support_faq_type`

**Status:** ✅ ~36 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(128)` | yes |  |  |
| `is_active` | `bool` | no | NOT NULL | Boolean state flag |

**Indexes:**
- `customer_support_faq_type_pkey` — UNIQUE (`id`)
- `customer_support_faq_type_id_key` — UNIQUE (`id`)

---

### `customer_support_handler`

**Status:** ✅ ~206 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `text` | no | NOT NULL |  |

**Indexes:**
- `customer_support_handler_pkey` — UNIQUE (`id`)
- `customer_support_handler_name_key` — UNIQUE (`name`)

---

### `customer_support_sub_type`

**Status:** ✅ ~330 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `text` | no | NOT NULL |  |
| `default_note` | `text` | yes |  |  |

**Indexes:**
- `customer_support_sub_type_pkey` — UNIQUE (`id`)
- `customer_support_sub_type_name_key` — UNIQUE (`name`)

---

### `customer_support_type`

**Status:** ✅ ~62 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `text` | no | NOT NULL |  |

**Indexes:**
- `customer_support_type_pkey` — UNIQUE (`id`)
- `customer_support_type_name_key` — UNIQUE (`name`)

---

### `customer_tam`

**Status:** ✅ ~193 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `customers_id` | `int4` | yes |  | Foreign key → `customers.customers_id` |
| `employees_id` | `int4` | yes |  | Foreign key → `employees.id` |
| `created_date` | `timestamptz` | yes |  | Date value |

**Indexes:**
- `customer_tam_pkey` — UNIQUE (`id`)
- `customer_tam_idx` — UNIQUE (`customers_id`)

---

### `customers_attributes`

**Status:** ✅ ~127,364 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `object_id` | `int4` | no | NOT NULL | Foreign key → `customers.customers_id` |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `attribute_id` | `int4` | no | NOT NULL | Foreign key → `attributes.id` |
| `attribute_group_id` | `int4` | yes |  | Identifier linking to related record |
| `value` | `text` | yes |  |  |
| `visibility_group` | `varchar(255)` | yes |  |  |
| `visibility_user` | `varchar(255)` | yes |  |  |

**Indexes:**
- `customers_attributes_pkey` — UNIQUE (`id`)
- `customers_attributes_object_id_attribute_id_idx` — (`object_id`, `attribute_id`)

---

### `customers_attributes_history`

**Status:** ✅ ~485,984 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `customers_attributes_history_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `id` | `int4` | no | NOT NULL |  |
| `object_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `attribute_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `attribute_group_id` | `int4` | yes |  | Identifier linking to related record |
| `value` | `text` | yes |  |  |
| `last_action` | `text` | yes |  |  |

**Indexes:**
- `customers_attributes_history_pkey` — UNIQUE (`customers_attributes_history_id`)

---

### `customers_priority`

**Status:** ✅ ~4 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `customers_priority_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `customers_priority_name` | `varchar(32)` | no | NOT NULL | Human-readable name |

**Indexes:**
- `customers_priority_pkey` — UNIQUE (`customers_priority_id`)

---

### `database_errors`

**Status:** ✅ ~824,313 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `error_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `code` | `int4` | yes |  | Foreign key → `wallet_responses_pl.code` |
| `message` | `varchar` | yes |  |  |
| `file` | `varchar` | yes |  |  |
| `line` | `int4` | yes |  |  |
| `context` | `varchar` | yes |  |  |
| `source` | `varchar` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |

**Indexes:**
- `database_errors_pkey` — UNIQUE (`error_id`)

---

### `databasechangelog`

**Status:** ✅ ~184 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `varchar(255)` | no | NOT NULL |  |
| `author` | `varchar(255)` | no | NOT NULL |  |
| `filename` | `varchar(255)` | no | NOT NULL |  |
| `dateexecuted` | `timestamptz` | no | NOT NULL |  |
| `orderexecuted` | `int4` | no | NOT NULL |  |
| `exectype` | `varchar(10)` | no | NOT NULL |  |
| `md5sum` | `varchar(35)` | yes |  |  |
| `description` | `varchar(255)` | yes |  |  |
| `comments` | `varchar(255)` | yes |  |  |
| `tag` | `varchar(255)` | yes |  |  |
| `liquibase` | `varchar(20)` | yes |  |  |

---

### `databasechangeloglock`

**Status:** ✅ ~1 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | no | PK · NOT NULL | Primary key |
| `locked` | `bool` | no | NOT NULL |  |
| `lockgranted` | `timestamptz` | yes |  |  |
| `lockedby` | `varchar(255)` | yes |  |  |

**Indexes:**
- `pk_databasechangeloglock` — UNIQUE (`id`)

---

### `email_recipients`

**Status:** ✅ ~245 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `email_text_id` | `int4` | yes |  | Foreign key → `email_templates.id` |
| `recipient_type` | `varchar(8)` | yes |  | Type or category classifier |
| `recipient` | `varchar(64)` | yes |  |  |
| `modified_by` | `int4` | yes |  | Timestamp |

**Indexes:**
- `email_recipients_pkey` — UNIQUE (`id`)

---

### `email_template_groupings`

**Status:** ✅ ~119 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `email_template_id` | `int4` | yes |  | Foreign key → `email_templates.id` |
| `email_template_group_id` | `int4` | yes |  | Foreign key → `email_template_groups.id` |

**Indexes:**
- `email_template_groupings_pkey` — UNIQUE (`id`)
- `email_template_groupings_email_template_id_key` — UNIQUE (`email_template_id`, `email_template_group_id`)

---

### `email_template_groups`

**Status:** ✅ ~5 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(500)` | no | NOT NULL |  |

**Indexes:**
- `email_template_groups_pkey` — UNIQUE (`id`)

---

### `email_templates`

**Status:** ✅ ~238 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `default_subject` | `text` | yes |  |  |
| `body` | `text` | yes |  |  |
| `sender` | `text` | yes |  |  |
| `name` | `varchar(64)` | yes |  |  |
| `modified_by` | `int4` | yes |  | Timestamp |

**Indexes:**
- `email_templates_pkey` — UNIQUE (`id`)
- `email_templates_name_key` — UNIQUE (`name`)

---

### `error_status_types`

**Status:** ✅ ~2 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `type` | `varchar(40)` | yes |  |  |

**Indexes:**
- `error_status_types_pkey` — UNIQUE (`id`)

---

### `error_statuses`

**Status:** ✅ ~2 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `error_status_type_id` | `int4` | yes |  | Foreign key → `error_status_types.id` |
| `description` | `text` | yes |  |  |

**Indexes:**
- `error_statuses_pkey` — UNIQUE (`id`)

---

### `eula`

**Status:** ✅ ~5 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | yes |  |  |
| `eula_text` | `text` | no | NOT NULL |  |
| `date_created` | `timestamp` | no | NOT NULL | Timestamp |
| `client_id` | `int4` | yes |  | Foreign key → `customers.customers_id` |
| `url` | `varchar(255)` | yes |  |  |
| `type` | `varchar(6)` | yes |  |  |

**Indexes:**
- `eula_pkey` — UNIQUE (`id`)

---

### `fraud_gateway_transactions`

**Status:** ✅ ~45,577 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | yes |  | Foreign key → `customers.customers_id` |
| `payment_method_id` | `int4` | yes |  | Foreign key → `client_payment_methods.id` |
| `score` | `int2` | no | NOT NULL |  |
| `date` | `timestamptz` | no | NOT NULL |  |
| `fraud_gateway` | `varchar(20)` | no | NOT NULL |  |
| `gateway_transaction` | `varchar` | no | NOT NULL |  |
| `status_code` | `bpchar` | yes |  | Short code or identifier |

**Indexes:**
- `fraud_gateway_transactions_pkey` — UNIQUE (`id`)
- `fraud_gateway_transactions_client_id_idx` — (`client_id`)
- `fraud_gateway_transactions_payment_method_id_idx` — (`payment_method_id`)

---

### `history_certificate`

**Status:** ✅ ~31,373 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `history_certificate_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `id` | `int4` | yes |  |  |
| `options_licenses_id` | `int4` | yes |  | Identifier linking to related record |
| `certificate_contact_id` | `int4` | yes |  | Identifier linking to related record |
| `certificate_company_id` | `int4` | yes |  | Identifier linking to related record |
| `status` | `varchar(255)` | yes |  |  |
| `domain` | `text` | yes |  |  |
| `os` | `varchar(32)` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `text` | yes |  | Timestamp |
| `archive_date` | `timestamptz` | yes |  | Date value |
| `action` | `varchar(16)` | yes |  |  |

**Indexes:**
- `history_certificate_pkey` — UNIQUE (`history_certificate_id`)

---

### `history_client_bags`

**Status:** ✅ ~630,079 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `name` | `varchar(64)` | yes |  |  |
| `description` | `text` | yes |  |  |
| `is_active` | `bool` | yes |  | Boolean state flag |
| `action` | `varchar(20)` | yes |  |  |
| `archive_date` | `timestamp` | yes |  | Date value |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `varchar(32)` | yes |  | Timestamp |
| `history_client_bags_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_client_bags_pkey` — UNIQUE (`history_client_bags_id`)

---

### `history_client_orders`

**Status:** ✅ ~9,355,367 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `status` | `int4` | yes |  |  |
| `entered_by` | `text` | yes |  |  |
| `order_created` | `timestamptz` | yes |  | Timestamp |
| `action` | `varchar(16)` | yes |  |  |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `text` | yes |  | Timestamp |
| `history_client_orders_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_client_orders_pkey` — UNIQUE (`history_client_orders_id`)
- `history_client_orders_client_id_status` — (`client_id`, `status`)
- `history_client_orders_last_modified_desc_idx` — (`id`, `last_modified`)

---

### `history_client_private_net`

**Status:** ✅ ~4,198 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `vlan_id` | `int4` | yes |  | Identifier linking to related record |
| `alias` | `text` | yes |  |  |
| `datacenter` | `text` | yes |  |  |
| `netmask` | `int4` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `text` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `text` | yes |  | Timestamp |
| `archive_date` | `timestamptz` | yes |  | Date value |
| `action` | `text` | yes |  |  |
| `history_client_private_net_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_client_private_net_pkey` — UNIQUE (`history_client_private_net_id`)

---

### `history_client_solutions`

**Status:** ✅ ~59,510 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `name` | `varchar(64)` | yes |  |  |
| `description` | `text` | yes |  |  |
| `action` | `varchar(20)` | yes |  |  |
| `archive_date` | `timestamp` | yes |  | Date value |
| `attachment` | `varchar` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `varchar(32)` | yes |  | Timestamp |
| `history_client_solutions_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_client_solutions_pkey` — UNIQUE (`history_client_solutions_id`)

---

### `history_client_zones`

**Status:** ✅ ~527,243 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `zone` | `varchar(256)` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `varchar(32)` | yes |  | Timestamp |
| `action` | `varchar(20)` | yes |  |  |
| `history_client_zones_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_client_zones_pkey` — UNIQUE (`history_client_zones_id`)

---

### `history_customers`

**Status:** ✅ ~244,134 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `customers_id` | `int4` | yes |  | Identifier linking to related record |
| `type` | `varchar(64)` | yes |  |  |
| `company_name` | `varchar(255)` | yes |  | Human-readable name |
| `blacklisted` | `bool` | yes |  |  |
| `referred_by` | `int4` | yes |  |  |
| `overage_rate` | `numeric` | yes |  |  |
| `shopping_cart_only` | `bool` | yes |  |  |
| `payment_term` | `varchar(21)` | yes |  | Foreign key → `payment_terms.payment_term` |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `varchar(32)` | yes |  | Timestamp |
| `archive_date` | `timestamptz` | no | NOT NULL | Date value |
| `action` | `varchar(16)` | yes |  |  |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `preferred_currency` | `varchar(3)` | yes |  |  |
| `disabled` | `timestamptz` | yes |  |  |
| `disabled_by` | `varchar(32)` | yes |  |  |

**Indexes:**
- `history_customers_pkey` — UNIQUE (`id`)

---

### `history_email_recipients`

**Status:** ✅ ~3,695 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `email_text_id` | `int4` | yes |  | Identifier linking to related record |
| `recipient_type` | `varchar(8)` | yes |  | Type or category classifier |
| `recipient` | `varchar(64)` | yes |  |  |
| `modified_by` | `int4` | yes |  | Timestamp |
| `action` | `varchar(16)` | yes |  |  |
| `archive_date` | `timestamp` | yes |  | Date value |
| `history_email_recipients_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_email_recipients_pkey` — UNIQUE (`history_email_recipients_id`)

---

### `history_email_templates`

**Status:** ✅ ~2,006 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `default_subject` | `text` | yes |  |  |
| `body` | `text` | yes |  |  |
| `sender` | `text` | yes |  |  |
| `name` | `varchar(64)` | yes |  |  |
| `modified_by` | `int4` | yes |  | Timestamp |
| `action` | `varchar(16)` | yes |  |  |
| `archive_date` | `timestamp` | yes |  | Date value |
| `history_email_templates_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_email_templates_pkey` — UNIQUE (`history_email_templates_id`)

---

### `history_ocean_restrictions`

**Status:** ✅ ~802 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | no | NOT NULL |  |
| `resource` | `varchar(128)` | yes |  |  |
| `group_name` | `varchar(255)` | yes |  | Human-readable name |
| `modified_by` | `int4` | yes |  | Timestamp |
| `action` | `varchar(16)` | yes |  |  |
| `archive_date` | `timestamp` | yes |  | Date value |
| `history_ocean_restrictions_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_ocean_restrictions_pkey` — UNIQUE (`history_ocean_restrictions_id`)

---

### `history_permission_categories`

**Status:** ✅ ~12 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `permission_categories_id` | `int4` | yes |  | Identifier linking to related record |
| `name` | `varchar(64)` | yes |  |  |
| `sort_order` | `int4` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `varchar(32)` | yes |  | Timestamp |
| `archive_date` | `timestamptz` | yes |  | Date value |
| `action` | `varchar(16)` | yes |  |  |

**Indexes:**
- `history_permission_categories_pkey` — UNIQUE (`id`)

---

### `history_permissions`

**Status:** ✅ ~136 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `permissions_id` | `varchar(32)` | yes |  | Foreign key → `permissions.permissions_id` |
| `permission_categories_id` | `int4` | yes |  | Identifier linking to related record |
| `permission_title` | `varchar(128)` | yes |  |  |
| `full_description` | `varchar` | yes |  |  |
| `sort_order` | `int4` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `varchar(32)` | yes |  | Timestamp |
| `archive_date` | `timestamptz` | yes |  | Date value |
| `action` | `varchar(16)` | yes |  |  |

**Indexes:**
- `history_permissions_pkey` — UNIQUE (`id`)

---

### `history_preconfigured_bundle_mapping`

**Status:** ✅ ~220 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `preconfigured_bundle_mapping_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `last_modified` | `timestamp` | yes |  | Timestamp |
| `action` | `varchar(30)` | yes |  |  |
| `history_preconfigured_bundle_mapping_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_preconfigured_bundle_mapping_pkey` — UNIQUE (`history_preconfigured_bundle_mapping_id`)

---

### `history_pricebook`

**Status:** ✅ ~93,467 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `nrc` | `numeric` | yes |  |  |
| `mrc` | `numeric` | yes |  |  |
| `modified_by` | `varchar(32)` | yes |  | Timestamp |
| `action` | `varchar(16)` | yes |  |  |
| `archive_date` | `timestamp` | yes |  | Date value |
| `setup` | `numeric` | yes |  |  |
| `product_catalog` | `varchar(64)` | yes |  |  |
| `component` | `varchar(64)` | yes |  |  |
| `currency` | `varchar(255)` | yes |  |  |
| `product_line` | `varchar(255)` | yes |  |  |
| `datacenter` | `text` | yes |  |  |
| `pricing_category` | `varchar(64)` | yes |  |  |
| `history_pricebook_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `rate` | `numeric` | yes |  |  |

**Indexes:**
- `history_pricebook_pkey` — UNIQUE (`history_pricebook_id`)
- `history_pricebook_id` — (`id`)

---

### `history_ticket_support_times`

**Status:** ✅ ~2,038,556 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `times_id` | `int4` | yes |  | Identifier linking to related record |
| `ticket_id` | `int4` | yes |  | Identifier linking to related record |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `username` | `text` | yes |  |  |
| `type` | `varchar(100)` | yes |  |  |
| `time_worked_old` | `int4` | yes |  |  |
| `time_worked_new` | `int4` | yes |  |  |
| `action` | `varchar(20)` | yes |  |  |
| `archive_date` | `timestamptz` | yes |  | Date value |

**Indexes:**
- `history_ticket_support_times_pkey` — UNIQUE (`id`)

---

### `history_volume_discount_percentage`

**Status:** ✅ ~38 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `history_volume_discount_percentage_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `id` | `int4` | yes |  |  |
| `threshold` | `int4` | no | NOT NULL |  |
| `discount` | `numeric` | no | NOT NULL |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `archive_date` | `timestamptz` | no | NOT NULL | Date value |
| `action` | `varchar(16)` | yes |  |  |

**Indexes:**
- `history_volume_discount_percentage_pkey` — UNIQUE (`history_volume_discount_percentage_id`)

---

## Relationships

| From | | To |
|------|---|-----|
| `billable_ticket_invoicing`.`client_id` | → | `customers`.`customers_id` |
| `billable_ticket_invoicing`.`username` | → | `employees`.`username` |
| `byo_upsell`.`product_id` | → | `product_catalog`.`id` |
| `byo_upsell`.`upsell_product_id` | → | `product_catalog`.`id` |
| `cart`.`session_id` | → | `sessions`.`session_id` |
| `cart`.`product_id` | → | `product_catalog`.`id` |
| `cart`.`datacenter_id` | → | `sb_datacenter`.`id` |
| `cart`.`promotion_id` | → | `promotions`.`id` |
| `cart`.`assisted_by` | → | `employees`.`id` |
| `cart_order`.`component_type` | → | `component_types`.`id` |
| `cart_raid_array_drives`.`drive_id` | → | `cart_components`.`id` |
| `cart_raid_arrays`.`level` | → | `raid_levels`.`id` |
| `certificate`.`options_licenses_id` | → | `options_licenses`.`id` |
| `certificate`.`certificate_contact_id` | → | `certificate_contacts`.`contact_id` |
| `certificate_company`.`customers_id` | → | `customers`.`customers_id` |
| `client_bags`.`client_id` | → | `customers`.`customers_id` |
| `client_error_statuses`.`client_id` | → | `customers`.`customers_id` |
| `client_eula_acceptance`.`client_id` | → | `customers`.`customers_id` |
| `client_firewall_vlan`.`service_id` | → | `customer_products`.`id` |
| `client_loadbalancer_vlan`.`service_id` | → | `customer_products`.`id` |
| `client_news`.`who` | → | `employees`.`id` |
| `client_notes`.`client_id` | → | `customers`.`customers_id` |
| `client_orders`.`client_id` | → | `customers`.`customers_id` |
| `client_orders`.`entered_by` | → | `employees`.`username` |
| `client_private_net`.`client_id` | → | `customers`.`customers_id` |
| `client_private_net`.`datacenter_id` | → | `sb_datacenter`.`id` |
| `client_solutions`.`client_id` | → | `customers`.`customers_id` |
| `client_tax_registrations`.`client_id` | → | `customers`.`customers_id` |
| `client_tax_registrations`.`tax_registration_type_id` | → | `tax_registration_types`.`tax_registration_type_id` |
| `client_tickets`.`client_id` | → | `customers`.`customers_id` |
| `client_tickets`.`service_id` | → | `customer_products`.`id` |
| `client_zones`.`client_id` | → | `customers`.`customers_id` |
| `clients_watchers`.`client_id` | → | `customers`.`customers_id` |
| `clients_watchers`.`employee_id` | → | `employees`.`id` |
| `cloud_storage_attributes`.`object_id` | → | `customer_products`.`id` |
| `cloud_storage_tiered_discounts`.`unit_of_measure_id` | → | `unit_of_measure`.`id` |
| `cloud_storage_tiered_discounts`.`component_id` | → | `components`.`id` |
| `config_code_pnet`.`config_component_id` | → | `config_code_components`.`id` |
| `config_code_raid_arrays`.`level` | → | `raid_levels`.`id` |
| `config_codes`.`customer_id` | → | `customers`.`customers_id` |
| `config_codes`.`product_id` | → | `product_catalog`.`id` |
| `contract_types`.`product_class_id` | → | `product_classes`.`id` |
| `contract_types`.`component_category` | → | `component_categories`.`id` |
| `contract_types`.`datacenter` | → | `sb_datacenter`.`id` |
| `contract_types`.`product_line_id` | → | `product_lines`.`id` |
| `countries_intergovernmental_organizations`.`igo_id` | → | `intergovernmental_organizations`.`id` |
| `customer_tam`.`customers_id` | → | `customers`.`customers_id` |
| `customer_tam`.`employees_id` | → | `employees`.`id` |
| `customers_attributes`.`object_id` | → | `customers`.`customers_id` |
| `database_errors`.`code` | → | `wallet_responses_pl`.`code` |
| `eula`.`client_id` | → | `customers`.`customers_id` |
| `fraud_gateway_transactions`.`client_id` | → | `customers`.`customers_id` |
| `fraud_gateway_transactions`.`payment_method_id` | → | `client_payment_methods`.`id` |
| `history_customers`.`payment_term` | → | `payment_terms`.`payment_term` |
| `history_permissions`.`permissions_id` | → | `permissions`.`permissions_id` |
| `xref_cloud_storage_policy_concession`.`app_config_id` | → | `app_config`.`id` |
| `components_attributes`.`attribute_id` | → | `attributes`.`id` |
| `contact_attribute`.`attribute_id` | → | `attributes`.`id` |
| `customer_products_attributes`.`attribute_id` | → | `attributes`.`id` |
| `datacenter_attributes`.`attribute_id` | → | `attributes`.`id` |
| `product_catalog_attributes`.`attribute_id` | → | `attributes`.`id` |
| `service_options_attributes`.`attribute_id` | → | `attributes`.`id` |
| `component_type_capabilities`.`capabilities_id` | → | `capabilities`.`id` |
| `service_type_capabilities`.`capabilities_id` | → | `capabilities`.`id` |
| `cart_components`.`cart_id` | → | `cart`.`id` |
| `cart_default_removed_components`.`cart_id` | → | `cart`.`id` |
| `client_bag_services`.`client_bag_id` | → | `client_bags`.`id` |
| `customers`.`client_industries_id` | → | `client_industries`.`id` |
| `order_communications`.`order_status_id` | → | `client_order_statuses`.`id` |
| `order_commission_split`.`order_id` | → | `client_orders`.`id` |
| `order_communications`.`order_id` | → | `client_orders`.`id` |
| `order_line_items`.`order_id` | → | `client_orders`.`id` |
| `order_notes`.`order_id` | → | `client_orders`.`id` |
| `provisioning_tickets`.`order_id` | → | `client_orders`.`id` |
| `xref_services_private_net`.`private_net_id` | → | `client_private_net`.`id` |
| `client_solution_services`.`client_solution_id` | → | `client_solutions`.`id` |
| `provisioning_tickets`.`ticket_id` | → | `client_tickets`.`ticket_id` |
| `customers`.`type_id` | → | `client_types_pl`.`client_type_id` |
| `product_class_client_type_discounts`.`client_type_id` | → | `client_types_pl`.`client_type_id` |
| `promotion_customer_type_criteria`.`customer_type_id` | → | `client_types_pl`.`client_type_id` |
| `contact_communication_method`.`communication_type_id` | → | `communication_type`.`communication_type_id` |
| `config_code_components`.`config_id` | → | `config_codes`.`id` |
| `history_service_billing_details`.`contract_length` | → | `contract_lengths`.`contract_length` |
| `order_line_items`.`contract_length` | → | `contract_lengths`.`contract_length` |
| `product_class_contract_length_discounts`.`contract_length` | → | `contract_lengths`.`contract_length` |
| `promotion_contract_length_criteria`.`contract_length` | → | `contract_lengths`.`contract_length` |
| `service_billing_details`.`contract_length` | → | `contract_lengths`.`contract_length` |
| `view_oc_cart`.`contract_length` | → | `contract_lengths`.`contract_length` |
| `view_order_line_items`.`contract_length` | → | `contract_lengths`.`contract_length` |
| `contact`.`country_id` | → | `countries`.`countries_id` |
| `item_tax_schedule`.`client_countries_id` | → | `countries`.`countries_id` |
| `sb_datacenter`.`countries_id` | → | `countries`.`countries_id` |
| `tax_rates`.`country` | → | `countries`.`countries_iso_code_2` |
| `customer_products`.`currency` | → | `currencies`.`code` |
| `customers`.`preferred_currency` | → | `currencies`.`code` |
| `datacenter_available_currencies`.`currency_code` | → | `currencies`.`code` |
| `exchange_rates`.`functional_currency` | → | `currencies`.`code` |
| `exchange_rates`.`originating_currency` | → | `currencies`.`code` |
| `order_line_item_details`.`currency` | → | `currencies`.`code` |
| `order_line_items`.`currency` | → | `currencies`.`code` |
| `pricebook`.`currency` | → | `currencies`.`code` |
| `promotion_effect_amounts`.`currency_code` | → | `currencies`.`code` |
| `service_options`.`currency` | → | `currencies`.`code` |
| `view_promotion_effects_details`.`currency_code` | → | `currencies`.`code` |
| `customer_support_faq_product_lines`.`customer_support_faq_id` | → | `customer_support_faq`.`id` |
| `xref_customer_support_type_sub_type`.`support_handler_id` | → | `customer_support_handler`.`id` |
| `xref_customer_support_type_sub_type`.`customer_support_sub_type_id` | → | `customer_support_sub_type`.`id` |
| `xref_customer_support_type_sub_type`.`customer_support_type_id` | → | `customer_support_type`.`id` |
