# Fusion DB — Database Views

**Group:** `views`  
**Tables in group:** 80  
**Accessible:** 77  
**Approximate total rows:** 0  
**Generated:** 2026-05-08 15:54  

## Overview

Database views expose pre-joined or aggregated projections of the underlying tables. Views are read-only and useful for quick joins without needing to write complex queries. Many views here expose product, customer, or service data in a flattened form.

---

## Table Summary

| Table | Row Count | Columns | Description |
|-------|-----------|---------|-------------|
| `customer_support_type_list` | < 1 | 11 | Records for customer support type list |
| `view_active_pricebook` | < 1 | 18 | Database view |
| `view_active_promotions` | < 1 | 5 | Database view |
| `view_attribute_groups` | < 1 | 5 | Database view |
| `view_client_bag_services` | < 1 | 3 | Database view |
| `view_client_bags` | < 1 | 10 | Database view |
| `view_client_bandwidth_allowance` | < 1 | 3 | Database view |
| `view_client_bandwidth_allowance_by_bag` | < 1 | 4 | Database view |
| `view_client_bandwidth_allowance_by_datacenter` | < 1 | 6 | Database view |
| `view_client_bandwidth_allowance_by_service` | < 1 | 7 | Database view |
| `view_client_contact_roles` | < 1 | 35 | Database view |
| `view_client_contacts` | < 1 | 31 | Database view |
| `view_client_error_statuses` | < 1 | 4 | Database view |
| `view_client_events` | < 1 | 6 | Database view |
| `view_client_orders` | < 1 | 13 | Database view |
| `view_client_payment_methods` | < 1 | 14 | Database view |
| `view_client_relations` | < 1 | 11 | Database view |
| `view_client_service_options` | < 1 | 17 | Database view |
| `view_client_services` | < 1 | 23 | Database view |
| `view_client_solution_services` | < 1 | 3 | Database view |
| `view_client_solutions` | < 1 | 8 | Database view |
| `view_client_tax_registration` | < 1 | 7 | Database view |
| `view_client_types` | < 1 | 3 | Database view |
| `view_clients` | < 1 | 18 | Database view |
| `view_clients_watchers` | < 1 | 6 | Database view |
| `view_cloud_storage_tiered_discounts` | < 1 | 9 | Database view |
| `view_component_capabilities` | < 1 | 17 | Database view |
| `view_component_license_keys` | < 1 | 10 | Database view |
| `view_component_provided_resources` | < 1 | 9 | Database view |
| `view_component_required_resources` | < 1 | 12 | Database view |
| `view_component_type_capabilities` | < 1 | 9 | Database view |
| `view_component_types` | < 1 | 9 | Database view |
| `view_components` | < 1 | 18 | Database view |
| `view_contract_types` | < 1 | 6 | Database view |
| `view_control_scan_ip_addresses` | < 1 | 8 | Database view |
| `view_countries_intergovernmental_organizations` | < 1 | 7 | Database view |
| `view_customer_support_faq` | < 1 | 7 | Database view |
| `view_customer_support_faq_product_lines` | < 1 | 5 | Database view |
| `view_customers_attributes` | < 1 | 6 | Database view |
| `view_customers_controlscan_credentials` | < 1 | 6 | Database view |
| `view_employee_client_relations_roles_matrix` | < 1 | 11 | Database view |
| `view_employee_roles` | < 1 | 4 | Database view |
| `view_employee_username` | < 1 | 3 | Database view |
| `view_item_tax_schedule` | < 1 | 16 | Database view |
| `view_multicurrency_pricebook` | < 1 | 20 | Database view |
| `view_oc_cart` | < 1 | 15 | Database view |
| `view_oc_cart_components` | < 1 | 12 | Database view |
| `view_oc_cart_default_removed_components` | < 1 | 4 | Database view |
| `view_order_commission_split` | < 1 | 5 | Database view |
| `view_order_entry_solution_details` | < 1 | 6 | Database view |
| `view_order_line_item_details` | ❌ denied | 15 | Database view |
| `view_order_line_items` | ❌ denied | 25 | Database view |
| `view_payment_transactions` | ❌ denied | 33 | Database view |
| `view_preconfigured_bundle_mapping` | < 1 | 11 | Database view |
| `view_pricebook` | < 1 | 18 | Database view |
| `view_product_allowed_components` | < 1 | 9 | Database view |
| `view_product_catalog` | < 1 | 20 | Database view |
| `view_product_frameworks` | < 1 | 6 | Database view |
| `view_product_templates` | < 1 | 8 | Database view |
| `view_promotion_criteria_details` | < 1 | 9 | Database view |
| `view_promotion_effect_criteria_details` | < 1 | 10 | Database view |
| `view_promotion_effects_details` | < 1 | 10 | Database view |
| `view_queue_messages` | < 1 | 8 | Database view |
| `view_resources` | < 1 | 3 | Database view |
| `view_service_cancellation_queue` | < 1 | 10 | Database view |
| `view_service_events` | < 1 | 6 | Database view |
| `view_service_option_raid_configuration` | < 1 | 9 | Database view |
| `view_service_options_capacity_as_gb` | < 1 | 8 | Database view |
| `view_service_payment_methods` | < 1 | 4 | Database view |
| `view_service_workflow_matrix` | < 1 | 12 | Database view |
| `view_services_without_device` | < 1 | 2 | Database view |
| `view_statistics_orders` | < 1 | 2 | Database view |
| `view_statistics_orders_by_status` | < 1 | 2 | Database view |
| `view_statistics_services` | < 1 | 2 | Database view |
| `view_statistics_services_by_datacenter` | < 1 | 2 | Database view |
| `view_statistics_services_by_status` | < 1 | 2 | Database view |
| `view_statistics_services_by_type` | < 1 | 2 | Database view |
| `view_ticket_routing_by_product_line` | < 1 | 12 | Database view |
| `view_xref_cloud_storage_policy_component` | < 1 | 5 | Database view |
| `view_xref_cloud_storage_policy_concession` | < 1 | 6 | Database view |

---

## Column Detail

### `customer_support_type_list`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `customer_support_type_id` | `int4` | yes |  | Identifier linking to related record |
| `customer_support_type` | `text` | yes |  | Type or category classifier |
| `customer_support_sub_type_id` | `int4` | yes |  | Identifier linking to related record |
| `customer_support_sub_type` | `text` | yes |  | Type or category classifier |
| `support_handler_id` | `int4` | yes |  | Identifier linking to related record |
| `support_handler` | `text` | yes |  |  |
| `is_customer_facing` | `bool` | yes |  |  |
| `notes` | `text` | yes |  |  |
| `num_tickets_required` | `int4` | yes |  |  |
| `hours_for_resolution` | `int4` | yes |  |  |
| `special_form_command` | `text` | yes |  |  |

---

### `view_active_pricebook`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `product` | `varchar(64)` | yes |  |  |
| `product_catalog_id` | `int4` | yes |  | Identifier linking to related record |
| `component` | `varchar(64)` | yes |  |  |
| `component_id` | `int4` | yes |  | Identifier linking to related record |
| `product_line` | `varchar(255)` | yes |  |  |
| `product_line_id` | `int4` | yes |  | Identifier linking to related record |
| `product_class` | `varchar(32)` | yes |  |  |
| `product_class_id` | `int4` | yes |  | Identifier linking to related record |
| `setup` | `numeric` | yes |  |  |
| `nrc` | `numeric` | yes |  |  |
| `mrc` | `numeric` | yes |  |  |
| `rate` | `numeric` | yes |  |  |
| `currency` | `varchar(3)` | yes |  |  |
| `dc_abbr` | `text` | yes |  |  |
| `datacenter` | `int4` | yes |  |  |
| `discountable` | `bool` | yes |  |  |
| `available` | `bool` | yes |  |  |

---

### `view_active_promotions`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `promo_code` | `varchar(32)` | yes |  | Short code or identifier |
| `description` | `varchar` | yes |  |  |
| `start_date` | `date` | yes |  | Date value |
| `end_date` | `date` | yes |  | Date value |

---

### `view_attribute_groups`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `attribute_group_id` | `int4` | yes |  | Identifier linking to related record |
| `attribute_group_name` | `varchar(500)` | yes |  | Human-readable name |
| `attribute_id` | `int4` | yes |  | Identifier linking to related record |
| `attribute_name` | `varchar(500)` | yes |  | Human-readable name |
| `attribute_data_type` | `varchar(500)` | yes |  | Type or category classifier |

---

### `view_client_bag_services`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `bag_id` | `int4` | yes |  | Identifier linking to related record |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `nickname` | `varchar(64)` | yes |  |  |

---

### `view_client_bags`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `bag_id` | `int4` | yes |  | Identifier linking to related record |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `name` | `varchar(64)` | yes |  |  |
| `description` | `text` | yes |  |  |
| `product_line_id` | `int4` | yes |  | Identifier linking to related record |
| `active` | `bool` | yes |  | Boolean state flag |
| `created` | `timestamptz` | yes |  | Timestamp |
| `createdby` | `varchar(32)` | yes |  | Timestamp |
| `lastupdated` | `timestamptz` | yes |  | Timestamp |
| `lastupdatedby` | `varchar(32)` | yes |  | Timestamp |

---

### `view_client_bandwidth_allowance`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `customers_id` | `int4` | yes |  | Identifier linking to related record |
| `num_bags` | `int8` | yes |  |  |
| `bandwidth` | `numeric` | yes |  |  |

---

### `view_client_bandwidth_allowance_by_bag`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `customers_id` | `int4` | yes |  | Identifier linking to related record |
| `bag_id` | `int4` | yes |  | Identifier linking to related record |
| `bandwidth` | `numeric` | yes |  |  |
| `salesperson` | `text` | yes |  |  |

---

### `view_client_bandwidth_allowance_by_datacenter`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `customers_id` | `int4` | yes |  | Identifier linking to related record |
| `dc_id` | `int4` | yes |  | Identifier linking to related record |
| `dc_name` | `text` | yes |  | Human-readable name |
| `products_status_id` | `int4` | yes |  | Identifier linking to related record |
| `name` | `text` | yes |  |  |
| `bandwidth` | `numeric` | yes |  |  |

---

### `view_client_bandwidth_allowance_by_service`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `customers_id` | `int4` | yes |  | Identifier linking to related record |
| `products_name` | `text` | yes |  | Human-readable name |
| `id` | `int4` | yes |  |  |
| `products_status_id` | `int4` | yes |  | Identifier linking to related record |
| `name` | `text` | yes |  |  |
| `bandwidth` | `numeric` | yes |  |  |
| `createdby` | `text` | yes |  | Timestamp |

---

### `view_client_contact_roles`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `contact_id` | `int4` | yes |  | Identifier linking to related record |
| `contact_role_id` | `int4` | yes |  | Identifier linking to related record |
| `contact_role_type_id` | `int4` | yes |  | Identifier linking to related record |
| `role_name` | `varchar(255)` | yes |  | Human-readable name |
| `customers_id` | `int4` | yes |  | Identifier linking to related record |
| `company` | `text` | yes |  |  |
| `first_name` | `text` | yes |  | Human-readable name |
| `last_name` | `text` | yes |  | Human-readable name |
| `street_address1` | `text` | yes |  | Address field |
| `street_address2` | `text` | yes |  | Address field |
| `street_address3` | `text` | yes |  | Address field |
| `postcode` | `text` | yes |  |  |
| `city` | `text` | yes |  | Address field |
| `zone_id` | `int4` | yes |  | Identifier linking to related record |
| `zone_name` | `text` | yes |  | Human-readable name |
| `zone_code` | `text` | yes |  | Short code or identifier |
| `country_id` | `int4` | yes |  | Identifier linking to related record |
| `countries_name` | `text` | yes |  | Human-readable name |
| `countries_code` | `bpchar` | yes |  | Short code or identifier |
| `email` | `text` | yes |  | Email address |
| `home` | `text` | yes |  |  |
| `work` | `text` | yes |  |  |
| `mobile` | `text` | yes |  |  |
| `fax` | `text` | yes |  | Phone number |
| `username` | `varchar(64)` | yes |  |  |
| `password` | `text` | yes |  |  |
| `security_question` | `varchar(255)` | yes |  |  |
| `security_answer` | `text` | yes |  |  |
| `subscribed` | `bool` | yes |  |  |
| `is_disabled` | `bool` | yes |  |  |
| `portal_user` | `bool` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `varchar(32)` | yes |  | Timestamp |

---

### `view_client_contacts`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `contact_id` | `int4` | yes |  | Identifier linking to related record |
| `customers_id` | `int4` | yes |  | Identifier linking to related record |
| `company` | `text` | yes |  |  |
| `first_name` | `text` | yes |  | Human-readable name |
| `last_name` | `text` | yes |  | Human-readable name |
| `street_address1` | `text` | yes |  | Address field |
| `street_address2` | `text` | yes |  | Address field |
| `street_address3` | `text` | yes |  | Address field |
| `postcode` | `text` | yes |  |  |
| `city` | `text` | yes |  | Address field |
| `zone_id` | `int4` | yes |  | Identifier linking to related record |
| `zone_name` | `text` | yes |  | Human-readable name |
| `zone_code` | `text` | yes |  | Short code or identifier |
| `country_id` | `int4` | yes |  | Identifier linking to related record |
| `countries_name` | `text` | yes |  | Human-readable name |
| `countries_code` | `bpchar` | yes |  | Short code or identifier |
| `email` | `text` | yes |  | Email address |
| `home` | `text` | yes |  |  |
| `work` | `text` | yes |  |  |
| `fax` | `text` | yes |  | Phone number |
| `username` | `varchar(64)` | yes |  |  |
| `password` | `text` | yes |  |  |
| `security_question` | `varchar(255)` | yes |  |  |
| `security_answer` | `text` | yes |  |  |
| `subscribed` | `bool` | yes |  |  |
| `portal_user` | `bool` | yes |  |  |
| `is_disabled` | `bool` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `varchar(32)` | yes |  | Timestamp |

---

### `view_client_error_statuses`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `error_status` | `text` | yes |  | Status code or label |
| `error_status_type` | `varchar(40)` | yes |  | Type or category classifier |

---

### `view_client_events`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `logged_by` | `text` | yes |  |  |
| `logged_on` | `timestamptz` | yes |  |  |
| `type` | `text` | yes |  |  |
| `message` | `text` | yes |  |  |

---

### `view_client_orders`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `client` | `varchar(255)` | yes |  |  |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `status` | `varchar(64)` | yes |  |  |
| `order_type` | `varchar(32)` | yes |  | Type or category classifier |
| `salesperson` | `text` | yes |  |  |
| `date` | `timestamptz` | yes |  |  |
| `message` | `varchar` | yes |  |  |
| `currency` | `varchar(3)` | yes |  |  |
| `effective_date` | `date` | yes |  | Date value |
| `sla_days` | `int4` | yes |  |  |
| `one_off` | `bool` | yes |  |  |
| `last_modified` | `timestamptz` | yes |  | Timestamp |

---

### `view_client_payment_methods`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `payment_type` | `varchar(32)` | yes |  | Type or category classifier |
| `cc_type` | `varchar(100)` | yes |  | Type or category classifier |
| `wallet_id` | `varchar(256)` | yes |  | Identifier linking to related record |
| `is_active` | `bool` | yes |  | Boolean state flag |
| `display_info` | `varchar(32)` | yes |  |  |
| `code` | `int4` | yes |  | Foreign key → `wallet_responses_pl.code` |
| `disabled` | `bool` | yes |  |  |
| `disabled_reason` | `varchar(256)` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |
| `type` | `varchar(32)` | yes |  |  |
| `response` | `varchar` | yes |  |  |
| `fraud_review_required` | `bool` | yes |  |  |

---

### `view_client_relations`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `client` | `varchar(255)` | yes |  |  |
| `employee_id` | `int4` | yes |  | Identifier linking to related record |
| `employee_email` | `text` | yes |  | Email address |
| `employee_name` | `text` | yes |  | Human-readable name |
| `employee_username` | `text` | yes |  |  |
| `product_line_id` | `int4` | yes |  | Identifier linking to related record |
| `product_line` | `varchar` | yes |  |  |
| `role_id` | `int4` | yes |  | Identifier linking to related record |
| `role` | `varchar(64)` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |

---

### `view_client_service_options`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `physicalname` | `text` | yes |  |  |
| `option_id` | `int4` | yes |  | Identifier linking to related record |
| `option_value` | `text` | yes |  |  |
| `quantity` | `int4` | yes |  |  |
| `setup` | `numeric` | yes |  |  |
| `nrc` | `numeric` | yes |  |  |
| `mrc` | `numeric` | yes |  |  |
| `rate` | `numeric` | yes |  |  |
| `currency` | `varchar(3)` | yes |  |  |
| `option_type_id` | `int4` | yes |  | Identifier linking to related record |
| `option_type` | `varchar(64)` | yes |  | Type or category classifier |
| `capacity` | `numeric` | yes |  | Address field |
| `unit_of_measure` | `varchar(10)` | yes |  |  |
| `add_on` | `bool` | yes |  |  |
| `create_date` | `date` | yes |  | Date value |
| `createdby` | `text` | yes |  | Timestamp |

---

### `view_client_services`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `nickname` | `varchar(64)` | yes |  |  |
| `physicalname` | `text` | yes |  |  |
| `name` | `text` | yes |  |  |
| `is_virtual` | `bool` | yes |  |  |
| `hide_in_portal` | `bool` | yes |  |  |
| `type` | `varchar(64)` | yes |  |  |
| `status` | `text` | yes |  |  |
| `setup` | `numeric` | yes |  |  |
| `mrc` | `numeric` | yes |  |  |
| `currency` | `varchar(3)` | yes |  |  |
| `provision_date` | `timestamptz` | yes |  | Date value |
| `createdby` | `text` | yes |  | Timestamp |
| `lastupdated` | `timestamptz` | yes |  | Timestamp |
| `lastupdatedby` | `text` | yes |  | Timestamp |
| `datacenter` | `text` | yes |  |  |
| `countries_id` | `int4` | yes |  | Identifier linking to related record |
| `resource` | `text` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |
| `product_line` | `varchar(255)` | yes |  |  |
| `is_qtc` | `bool` | yes |  |  |
| `product_catalog_id` | `int4` | yes |  | Identifier linking to related record |

---

### `view_client_solution_services`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `solution_id` | `int4` | yes |  | Identifier linking to related record |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `nickname` | `varchar(64)` | yes |  |  |

---

### `view_client_solutions`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `solution_id` | `int4` | yes |  | Identifier linking to related record |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `name` | `varchar(64)` | yes |  |  |
| `description` | `text` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |
| `createdby` | `varchar(32)` | yes |  | Timestamp |
| `lastupdated` | `timestamptz` | yes |  | Timestamp |
| `lastupdatedby` | `varchar(32)` | yes |  | Timestamp |

---

### `view_client_tax_registration`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `name` | `varchar` | yes |  |  |
| `registration_type` | `varchar(16)` | yes |  | Type or category classifier |
| `registration_value` | `varchar` | yes |  |  |
| `certificate_required` | `bool` | yes |  |  |
| `certificate_received` | `bool` | yes |  |  |
| `bitmask` | `varbit` | yes |  |  |

---

### `view_client_types`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `name` | `text` | yes |  |  |
| `link` | `text` | yes |  |  |
| `count` | `int8` | yes |  |  |

---

### `view_clients`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `name` | `varchar(255)` | yes |  |  |
| `industry` | `int4` | yes |  |  |
| `type` | `varchar(64)` | yes |  |  |
| `tam` | `text` | yes |  |  |
| `cse` | `text` | yes |  |  |
| `msa_accepted` | `bool` | yes |  |  |
| `blacklisted` | `bool` | yes |  |  |
| `referred_by` | `int4` | yes |  |  |
| `payment_term` | `varchar(21)` | yes |  | Foreign key → `payment_terms.payment_term` |
| `preferred_currency` | `varchar(3)` | yes |  |  |
| `overage_rate` | `numeric` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |
| `createdby` | `varchar(32)` | yes |  | Timestamp |
| `lastupdated` | `timestamptz` | yes |  | Timestamp |
| `lastupdatedby` | `varchar(32)` | yes |  | Timestamp |
| `disabled` | `timestamptz` | yes |  |  |
| `disabledby` | `varchar(32)` | yes |  |  |

---

### `view_clients_watchers`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `company_name` | `varchar(255)` | yes |  | Human-readable name |
| `employee_id` | `int4` | yes |  | Identifier linking to related record |
| `username` | `text` | yes |  |  |
| `employee_name` | `text` | yes |  | Human-readable name |

---

### `view_cloud_storage_tiered_discounts`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `tier` | `int4` | yes |  |  |
| `discount_amount` | `float8` | yes |  | Monetary amount |
| `threshold` | `int4` | yes |  |  |
| `unit_of_measure` | `varchar(10)` | yes |  |  |
| `name` | `varchar(64)` | yes |  |  |
| `currency` | `varchar(4)` | yes |  |  |
| `component_id` | `int4` | yes |  | Identifier linking to related record |
| `display_name` | `varchar(64)` | yes |  | Human-readable name |

---

### `view_component_capabilities`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `component_id` | `int4` | yes |  | Identifier linking to related record |
| `component` | `varchar(64)` | yes |  |  |
| `capability_id` | `int4` | yes |  | Identifier linking to related record |
| `capability` | `varchar(64)` | yes |  |  |
| `datatype` | `text` | yes |  |  |
| `value` | `text` | yes |  |  |
| `uom_id` | `int4` | yes |  | Identifier linking to related record |
| `uom` | `varchar(10)` | yes |  |  |
| `uom_base_value` | `text` | yes |  |  |
| `uom_base_abbr` | `varchar(10)` | yes |  |  |
| `is_primary` | `bool` | yes |  |  |
| `minimum` | `text` | yes |  |  |
| `maximum` | `text` | yes |  |  |
| `minimum_base` | `text` | yes |  |  |
| `maximum_base` | `text` | yes |  |  |
| `match_required` | `bool` | yes |  |  |
| `capability_type` | `varchar(64)` | yes |  | Type or category classifier |

---

### `view_component_license_keys`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `component_id` | `int4` | yes |  | Identifier linking to related record |
| `component_name` | `varchar(64)` | yes |  | Human-readable name |
| `component_type_id` | `int4` | yes |  | Identifier linking to related record |
| `component_type` | `varchar(64)` | yes |  | Type or category classifier |
| `component_category_id` | `int4` | yes |  | Identifier linking to related record |
| `component_category` | `varchar(32)` | yes |  |  |
| `license_type_id` | `int4` | yes |  | Identifier linking to related record |
| `license_type` | `varchar(64)` | yes |  | Type or category classifier |
| `base` | `bool` | yes |  |  |

---

### `view_component_provided_resources`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `component_type_id` | `int4` | yes |  | Identifier linking to related record |
| `component_type` | `varchar(64)` | yes |  | Type or category classifier |
| `component_id` | `int4` | yes |  | Identifier linking to related record |
| `component` | `varchar(64)` | yes |  |  |
| `resource` | `varchar(32)` | yes |  |  |
| `quantity` | `float8` | yes |  |  |
| `unit_of_measure` | `varchar(10)` | yes |  |  |
| `priority` | `int4` | yes |  |  |

---

### `view_component_required_resources`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `component_type_id` | `int4` | yes |  | Identifier linking to related record |
| `component_type` | `varchar(64)` | yes |  | Type or category classifier |
| `component_id` | `int4` | yes |  | Identifier linking to related record |
| `component` | `varchar(64)` | yes |  |  |
| `use_type` | `varchar(32)` | yes |  | Type or category classifier |
| `operator` | `varchar(3)` | yes |  | Foreign key → `resource_use_operators.operator` |
| `resource` | `varchar(32)` | yes |  |  |
| `quantity` | `float8` | yes |  |  |
| `message` | `text` | yes |  |  |
| `unit_of_measure` | `varchar(10)` | yes |  |  |
| `precheck` | `bool` | yes |  |  |

---

### `view_component_type_capabilities`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `component_type_id` | `int4` | yes |  | Identifier linking to related record |
| `component_type` | `varchar(64)` | yes |  | Type or category classifier |
| `capabilities_id` | `int4` | yes |  | Identifier linking to related record |
| `capability_name` | `varchar(64)` | yes |  | Human-readable name |
| `datatype` | `text` | yes |  |  |
| `uom_id` | `int4` | yes |  | Identifier linking to related record |
| `uom` | `varchar(10)` | yes |  |  |
| `capability_type` | `varchar(64)` | yes |  | Type or category classifier |

---

### `view_component_types`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `type` | `varchar(64)` | yes |  |  |
| `description` | `varchar(256)` | yes |  |  |
| `parent_id` | `int4` | yes |  | Identifier linking to related record |
| `parent_type` | `varchar(64)` | yes |  | Type or category classifier |
| `category_id` | `int4` | yes |  | Identifier linking to related record |
| `category` | `varchar(32)` | yes |  |  |
| `service_option_type` | `varchar(64)` | yes |  | Type or category classifier |
| `is_active` | `bool` | yes |  | Boolean state flag |

---

### `view_components`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `name` | `varchar(64)` | yes |  |  |
| `display_name` | `varchar(64)` | yes |  | Human-readable name |
| `description` | `varchar(256)` | yes |  |  |
| `cost` | `numeric` | yes |  |  |
| `type_id` | `int4` | yes |  | Identifier linking to related record |
| `type` | `varchar(64)` | yes |  |  |
| `category_id` | `int4` | yes |  | Identifier linking to related record |
| `category` | `varchar(32)` | yes |  |  |
| `is_active` | `bool` | yes |  | Boolean state flag |
| `discountable` | `bool` | yes |  |  |
| `service_option_type` | `varchar(64)` | yes |  | Type or category classifier |
| `kickstart_key` | `varchar(64)` | yes |  |  |
| `created` | `timestamp` | yes |  | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `last_updated` | `timestamp` | yes |  | Timestamp |
| `last_updated_by` | `varchar(32)` | yes |  | Timestamp |
| `template_name` | `varchar(64)` | yes |  | Human-readable name |

---

### `view_contract_types`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `product_class` | `varchar(32)` | yes |  |  |
| `component_category` | `varchar(32)` | yes |  |  |
| `datacenter` | `text` | yes |  |  |
| `product_line` | `varchar(255)` | yes |  |  |
| `contract_type` | `varchar(16)` | yes |  | Type or category classifier |

---

### `view_control_scan_ip_addresses`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `service_option_id` | `int4` | yes |  | Identifier linking to related record |
| `control_scan` | `text` | yes |  |  |
| `service_options_attributes_id` | `int4` | yes |  | Identifier linking to related record |
| `service_options_attributes_name` | `varchar(500)` | yes |  | Human-readable name |
| `ip_address` | `text` | yes |  | Address field |
| `value` | `text` | yes |  |  |

---

### `view_countries_intergovernmental_organizations`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `countries_id` | `int4` | yes |  | Identifier linking to related record |
| `country` | `text` | yes |  | Address field |
| `countries_iso_code_2` | `bpchar` | yes |  |  |
| `countries_iso_code_3` | `bpchar` | yes |  |  |
| `igo_id` | `int4` | yes |  | Identifier linking to related record |
| `organization` | `text` | yes |  |  |
| `abbr` | `varchar(16)` | yes |  |  |

---

### `view_customer_support_faq`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `type_id` | `int4` | yes |  | Identifier linking to related record |
| `type` | `varchar(128)` | yes |  |  |
| `question` | `text` | yes |  |  |
| `answer` | `text` | yes |  |  |
| `order_number` | `int4` | yes |  |  |
| `is_active` | `bool` | yes |  | Boolean state flag |

---

### `view_customer_support_faq_product_lines`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `customer_support_faq_id` | `int4` | yes |  | Identifier linking to related record |
| `question` | `text` | yes |  |  |
| `product_line_id` | `int4` | yes |  | Identifier linking to related record |
| `product_line` | `varchar(255)` | yes |  |  |

---

### `view_customers_attributes`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `customers_attribute_id` | `int4` | yes |  | Identifier linking to related record |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `attribute_id` | `int4` | yes |  | Identifier linking to related record |
| `attribute_name` | `varchar(500)` | yes |  | Human-readable name |
| `attribute_data_type` | `varchar(500)` | yes |  | Type or category classifier |
| `attribute_value` | `text` | yes |  |  |

---

### `view_customers_controlscan_credentials`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `customers_attribute_id` | `int4` | yes |  | Identifier linking to related record |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `attribute_id` | `int4` | yes |  | Identifier linking to related record |
| `attribute_name` | `varchar(500)` | yes |  | Human-readable name |
| `attribute_data_type` | `varchar(500)` | yes |  | Type or category classifier |
| `attribute_value` | `text` | yes |  |  |

---

### `view_employee_client_relations_roles_matrix`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `employee_id` | `int4` | yes |  | Identifier linking to related record |
| `employee_username` | `text` | yes |  |  |
| `employee_name` | `text` | yes |  | Human-readable name |
| `product_line_id` | `int4` | yes |  | Identifier linking to related record |
| `round_robin` | `bool` | yes |  |  |
| `product_line` | `varchar` | yes |  |  |
| `client_relations_role_id` | `int4` | yes |  | Identifier linking to related record |
| `role` | `varchar(64)` | yes |  |  |
| `igo_id` | `int4` | yes |  | Identifier linking to related record |
| `region` | `varchar(16)` | yes |  |  |
| `last_assigned` | `timestamptz` | yes |  |  |

---

### `view_employee_roles`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `name` | `text` | yes |  |  |
| `username` | `text` | yes |  |  |
| `role` | `text` | yes |  |  |

---

### `view_employee_username`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `employee_id` | `int4` | yes |  | Identifier linking to related record |
| `employee_name` | `text` | yes |  | Human-readable name |
| `username` | `text` | yes |  |  |

---

### `view_item_tax_schedule`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `product_class_id` | `int4` | yes |  | Identifier linking to related record |
| `product_class` | `varchar(32)` | yes |  |  |
| `component_category_id` | `int4` | yes |  | Identifier linking to related record |
| `component_category` | `varchar(32)` | yes |  |  |
| `datacenter` | `text` | yes |  |  |
| `countries_id` | `int4` | yes |  | Identifier linking to related record |
| `client_country` | `text` | yes |  | Address field |
| `state_id` | `int4` | yes |  | Identifier linking to related record |
| `client_state` | `varchar(255)` | yes |  |  |
| `setup_tax_schedule` | `varchar(15)` | yes |  |  |
| `setup_tax` | `numeric` | yes |  |  |
| `mrc_tax_schedule` | `varchar(15)` | yes |  |  |
| `mrc_tax` | `numeric` | yes |  |  |
| `nrc_tax_schedule` | `varchar(15)` | yes |  |  |
| `nrc_tax` | `numeric` | yes |  |  |

---

### `view_multicurrency_pricebook`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `product` | `varchar(64)` | yes |  |  |
| `product_catalog_id` | `int4` | yes |  | Identifier linking to related record |
| `component` | `varchar(64)` | yes |  |  |
| `component_id` | `int4` | yes |  | Identifier linking to related record |
| `product_line` | `varchar(255)` | yes |  |  |
| `product_line_id` | `int4` | yes |  | Identifier linking to related record |
| `product_class` | `varchar(32)` | yes |  |  |
| `product_class_id` | `int4` | yes |  | Identifier linking to related record |
| `setup` | `numeric` | yes |  |  |
| `nrc` | `numeric` | yes |  |  |
| `mrc` | `numeric` | yes |  |  |
| `rate` | `numeric` | yes |  |  |
| `functional_currency` | `varchar(3)` | yes |  |  |
| `originating_currency` | `varchar(3)` | yes |  |  |
| `exchange_rate` | `numeric` | yes |  |  |
| `dc_abbr` | `text` | yes |  |  |
| `datacenter` | `int4` | yes |  |  |
| `discountable` | `bool` | yes |  |  |
| `available` | `bool` | yes |  |  |

---

### `view_oc_cart`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `session_id` | `bpchar` | yes |  | Identifier linking to related record |
| `product_id` | `int4` | yes |  | Identifier linking to related record |
| `datacenter_id` | `int4` | yes |  | Identifier linking to related record |
| `contract_length` | `int4` | yes |  | Foreign key → `contract_lengths.contract_length` |
| `fqdn` | `varchar(128)` | yes |  |  |
| `setup` | `numeric` | yes |  |  |
| `mrc` | `numeric` | yes |  |  |
| `functional_currency` | `varchar(3)` | yes |  |  |
| `promotion_id` | `int4` | yes |  | Identifier linking to related record |
| `setup_discount` | `numeric` | yes |  |  |
| `mrc_discount` | `numeric` | yes |  |  |
| `originating_currency` | `varchar(3)` | yes |  |  |
| `assisted_by` | `int4` | yes |  |  |
| `assisted_by_username` | `text` | yes |  |  |

---

### `view_oc_cart_components`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `cart_id` | `int4` | yes |  | Identifier linking to related record |
| `component_id` | `int4` | yes |  | Identifier linking to related record |
| `setup` | `numeric` | yes |  |  |
| `nrc` | `numeric` | yes |  |  |
| `mrc` | `numeric` | yes |  |  |
| `setup_discount` | `numeric` | yes |  |  |
| `nrc_discount` | `numeric` | yes |  |  |
| `mrc_discount` | `numeric` | yes |  |  |
| `is_default` | `bool` | yes |  |  |
| `functional_currency` | `varchar(3)` | yes |  |  |
| `originating_currency` | `varchar(3)` | yes |  |  |

---

### `view_oc_cart_default_removed_components`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `cart_id` | `int4` | yes |  | Identifier linking to related record |
| `component_id` | `int4` | yes |  | Identifier linking to related record |
| `mrc` | `numeric` | yes |  |  |

---

### `view_order_commission_split`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `order_id` | `int4` | yes |  | Identifier linking to related record |
| `order_date` | `timestamptz` | yes |  | Date value |
| `employee_id` | `int4` | yes |  | Identifier linking to related record |
| `username` | `text` | yes |  |  |
| `percentage` | `numeric` | yes |  |  |

---

### `view_order_entry_solution_details`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `link_id` | `int4` | yes |  | Identifier linking to related record |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `node_id` | `int4` | yes |  | Identifier linking to related record |
| `service_type` | `varchar(64)` | yes |  | Type or category classifier |
| `parent_service_id` | `int4` | yes |  | Identifier linking to related record |
| `parent_node_id` | `int4` | yes |  | Identifier linking to related record |

---

### `view_order_line_item_details`

**Status:** ❌ ❌ permission denied  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `detail_id` | `int4` | yes |  | Identifier linking to related record |
| `line_item_id` | `int4` | yes |  | Identifier linking to related record |
| `order_id` | `int4` | yes |  | Identifier linking to related record |
| `service_option_type` | `varchar(64)` | yes |  | Type or category classifier |
| `component` | `varchar(128)` | yes |  |  |
| `default_setup_fee` | `numeric` | yes |  |  |
| `default_nrc` | `numeric` | yes |  |  |
| `default_mrc` | `numeric` | yes |  |  |
| `action` | `bpchar` | yes |  |  |
| `setup_fee` | `numeric` | yes |  |  |
| `nrc` | `numeric` | yes |  |  |
| `mrc` | `numeric` | yes |  |  |
| `currency` | `varchar(3)` | yes |  |  |
| `service_option_id` | `int4` | yes |  | Identifier linking to related record |
| `rate` | `numeric` | yes |  |  |

---

### `view_order_line_items`

**Status:** ❌ ❌ permission denied  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `order_id` | `int4` | yes |  | Identifier linking to related record |
| `line_item_id` | `int4` | yes |  | Identifier linking to related record |
| `contract_id` | `varchar(32)` | yes |  | Identifier linking to related record |
| `purchase_order` | `varchar(32)` | yes |  |  |
| `payment_type` | `varchar(32)` | yes |  | Type or category classifier |
| `payment_method_id` | `int4` | yes |  | Identifier linking to related record |
| `product` | `varchar(128)` | yes |  |  |
| `product_category` | `varchar(64)` | yes |  |  |
| `tls` | `varchar(64)` | yes |  |  |
| `is_virtual` | `bool` | yes |  |  |
| `hide_in_portal` | `bool` | yes |  |  |
| `payment_method` | `varchar(32)` | yes |  |  |
| `location` | `text` | yes |  |  |
| `product_line` | `varchar(255)` | yes |  |  |
| `line_item_type` | `varchar(32)` | yes |  | Type or category classifier |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `nickname` | `varchar(64)` | yes |  |  |
| `billing_day` | `int4` | yes |  |  |
| `billing_cycle` | `int4` | yes |  |  |
| `contract_length` | `int4` | yes |  | Foreign key → `contract_lengths.contract_length` |
| `setup` | `numeric` | yes |  |  |
| `mrc` | `numeric` | yes |  |  |
| `currency` | `varchar(3)` | yes |  |  |
| `notes` | `text` | yes |  |  |
| `old_line_item_id` | `int4` | yes |  | Identifier linking to related record |

---

### `view_payment_transactions`

**Status:** ❌ ❌ permission denied  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `type` | `varchar(32)` | yes |  |  |
| `status` | `varchar(30)` | yes |  |  |
| `message` | `varchar` | yes |  |  |
| `authcode` | `varchar(32)` | yes |  |  |
| `token` | `varchar(32)` | yes |  |  |
| `client_wallet` | `varchar(32)` | yes |  |  |
| `display_info` | `varchar(32)` | yes |  |  |
| `card_type` | `varchar` | yes |  | Type or category classifier |
| `payment_type` | `varchar(32)` | yes |  | Type or category classifier |
| `company` | `varchar(3)` | yes |  |  |
| `originating_currency` | `varchar(5)` | yes |  |  |
| `functional_currency` | `varchar(3)` | yes |  |  |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `total` | `numeric` | yes |  |  |
| `total_sales_tax` | `numeric` | yes |  |  |
| `comments` | `varchar` | yes |  |  |
| `billing_name` | `varchar(256)` | yes |  | Human-readable name |
| `billing_phone` | `varchar(20)` | yes |  | Phone number |
| `billing_email` | `varchar(256)` | yes |  | Email address |
| `billing_street` | `varchar(256)` | yes |  | Address field |
| `billing_suburb` | `varchar(256)` | yes |  |  |
| `billing_city` | `varchar(256)` | yes |  | Address field |
| `billing_province` | `varchar(256)` | yes |  |  |
| `billing_postal_code` | `varchar(10)` | yes |  | Short code or identifier |
| `billing_country` | `varchar(2)` | yes |  | Address field |
| `date` | `timestamptz` | yes |  |  |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `varchar(256)` | yes |  | Timestamp |
| `document_type` | `varchar` | yes |  | Type or category classifier |
| `document_id` | `varchar` | yes |  | Identifier linking to related record |
| `amount` | `numeric` | yes |  |  |
| `sales_tax` | `numeric` | yes |  |  |

---

### `view_preconfigured_bundle_mapping`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `category_id` | `int4` | yes |  | Identifier linking to related record |
| `category_name` | `varchar(256)` | yes |  | Human-readable name |
| `datacenter_id` | `int4` | yes |  | Identifier linking to related record |
| `datacenter_abbr` | `text` | yes |  |  |
| `operating_system` | `varchar` | yes |  |  |
| `rating` | `int4` | yes |  |  |
| `product_id` | `int4` | yes |  | Identifier linking to related record |
| `product_name` | `varchar(64)` | yes |  | Human-readable name |
| `product_configuration_id` | `int4` | yes |  | Identifier linking to related record |
| `configuration_name` | `varchar(256)` | yes |  | Human-readable name |

---

### `view_pricebook`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `product` | `varchar(64)` | yes |  |  |
| `product_catalog_id` | `int4` | yes |  | Identifier linking to related record |
| `component` | `varchar(64)` | yes |  |  |
| `component_id` | `int4` | yes |  | Identifier linking to related record |
| `product_line` | `varchar(255)` | yes |  |  |
| `product_line_id` | `int4` | yes |  | Identifier linking to related record |
| `product_class` | `varchar(32)` | yes |  |  |
| `product_class_id` | `int4` | yes |  | Identifier linking to related record |
| `setup` | `numeric` | yes |  |  |
| `nrc` | `numeric` | yes |  |  |
| `mrc` | `numeric` | yes |  |  |
| `rate` | `numeric` | yes |  |  |
| `currency` | `varchar(3)` | yes |  |  |
| `dc_abbr` | `text` | yes |  |  |
| `datacenter` | `int4` | yes |  |  |
| `discountable` | `bool` | yes |  |  |
| `available` | `bool` | yes |  |  |

---

### `view_product_allowed_components`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int8` | yes |  |  |
| `product_id` | `int4` | yes |  | Identifier linking to related record |
| `product_name` | `varchar(64)` | yes |  | Human-readable name |
| `component_id` | `int4` | yes |  | Identifier linking to related record |
| `available_in_shop` | `bool` | yes |  |  |
| `component_name` | `varchar(64)` | yes |  | Human-readable name |
| `component_type` | `varchar(64)` | yes |  | Type or category classifier |
| `component_active` | `bool` | yes |  | Boolean state flag |
| `category` | `varchar(32)` | yes |  |  |

---

### `view_product_catalog`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `name` | `varchar(64)` | yes |  |  |
| `tls` | `varchar(32)` | yes |  |  |
| `tls_id` | `int4` | yes |  | Identifier linking to related record |
| `description` | `varchar(1024)` | yes |  |  |
| `is_active` | `bool` | yes |  | Boolean state flag |
| `available_in_shop` | `bool` | yes |  |  |
| `sold_out` | `bool` | yes |  |  |
| `limited_availability` | `bool` | yes |  |  |
| `is_virtual` | `bool` | yes |  |  |
| `hide_in_portal` | `bool` | yes |  |  |
| `use_picker` | `bool` | yes |  |  |
| `discountable` | `bool` | yes |  |  |
| `sku` | `varchar(64)` | yes |  |  |
| `category` | `varchar(64)` | yes |  |  |
| `product_summary` | `text` | yes |  |  |
| `created` | `timestamp` | yes |  | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `last_updated` | `timestamp` | yes |  | Timestamp |
| `last_updated_by` | `varchar(32)` | yes |  | Timestamp |

---

### `view_product_frameworks`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `product_id` | `int4` | yes |  | Identifier linking to related record |
| `product` | `varchar(64)` | yes |  |  |
| `component_type_id` | `int4` | yes |  | Identifier linking to related record |
| `component_type` | `varchar(64)` | yes |  | Type or category classifier |
| `minimum` | `int4` | yes |  |  |
| `maximum` | `int4` | yes |  |  |

---

### `view_product_templates`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `product` | `varchar(64)` | yes |  |  |
| `product_id` | `int4` | yes |  | Identifier linking to related record |
| `component` | `varchar(64)` | yes |  |  |
| `component_id` | `int4` | yes |  | Identifier linking to related record |
| `component_type` | `varchar(64)` | yes |  | Type or category classifier |
| `component_type_id` | `int4` | yes |  | Identifier linking to related record |
| `quantity` | `int4` | yes |  |  |

---

### `view_promotion_criteria_details`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `promo_id` | `int4` | yes |  | Identifier linking to related record |
| `promo_code` | `varchar(32)` | yes |  | Short code or identifier |
| `criteria_id` | `int4` | yes |  | Identifier linking to related record |
| `criteria` | `int4` | yes |  |  |
| `type` | `text` | yes |  |  |
| `quantity` | `int4` | yes |  |  |
| `depth` | `int4` | yes |  |  |
| `operator` | `varchar(3)` | yes |  | Foreign key → `resource_use_operators.operator` |
| `scope` | `varchar(32)` | yes |  |  |

---

### `view_promotion_effect_criteria_details`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `promo_id` | `int4` | yes |  | Identifier linking to related record |
| `effect_id` | `int4` | yes |  | Identifier linking to related record |
| `effect_criteria_id` | `int4` | yes |  | Identifier linking to related record |
| `effect_criteria_value` | `varchar` | yes |  |  |
| `type` | `text` | yes |  |  |
| `quantity` | `int4` | yes |  |  |
| `depth` | `int4` | yes |  |  |
| `operator` | `varchar(3)` | yes |  | Foreign key → `resource_use_operators.operator` |
| `scope` | `varchar(32)` | yes |  |  |

---

### `view_promotion_effects_details`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `promo_id` | `int4` | yes |  | Identifier linking to related record |
| `promo_code` | `varchar(32)` | yes |  | Short code or identifier |
| `effect_type` | `varchar(32)` | yes |  | Type or category classifier |
| `target_id` | `int4` | yes |  | Identifier linking to related record |
| `amount` | `float8` | yes |  |  |
| `currency_code` | `varchar(3)` | yes |  | Foreign key → `currencies.code` |
| `target_amount_type` | `varchar(32)` | yes |  | Type or category classifier |
| `effect_target_type` | `varchar(32)` | yes |  | Type or category classifier |
| `target_max_quantity` | `int4` | yes |  |  |

---

### `view_queue_messages`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `queue_id` | `int4` | yes |  | Identifier linking to related record |
| `queue_name` | `varchar` | yes |  | Human-readable name |
| `consumed` | `timestamptz` | yes |  |  |
| `locked` | `timestamptz` | yes |  |  |
| `token` | `varchar` | yes |  |  |
| `message_id` | `int4` | yes |  | Identifier linking to related record |
| `message` | `varchar` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |

---

### `view_resources`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `name` | `varchar(32)` | yes |  |  |
| `unit_of_measure` | `varchar(10)` | yes |  |  |

---

### `view_service_cancellation_queue`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `status` | `text` | yes |  |  |
| `product_line` | `varchar(255)` | yes |  |  |
| `cancellation_date` | `timestamptz` | yes |  | Date value |
| `cancellation_category` | `text` | yes |  |  |
| `cancellation_comments` | `text` | yes |  |  |
| `contract_id` | `varchar(32)` | yes |  | Identifier linking to related record |
| `last_email_date` | `timestamptz` | yes |  | Date value |
| `ticket_id` | `int4` | yes |  | Identifier linking to related record |
| `reason` | `varchar(1024)` | yes |  |  |

---

### `view_service_events`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `logged_by` | `text` | yes |  |  |
| `logged_on` | `timestamptz` | yes |  |  |
| `type` | `text` | yes |  |  |
| `message` | `text` | yes |  |  |

---

### `view_service_option_raid_configuration`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `raid_card_id` | `int4` | yes |  | Identifier linking to related record |
| `card` | `text` | yes |  |  |
| `raid_option_id` | `int4` | yes |  | Identifier linking to related record |
| `option` | `text` | yes |  |  |
| `role` | `raid_roles` | yes |  |  |
| `raid_level_id` | `int4` | yes |  | Identifier linking to related record |
| `raid_array_id` | `int4` | yes |  | Identifier linking to related record |
| `raid_array_level` | `varchar(4)` | yes |  |  |

---

### `view_service_options_capacity_as_gb`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `options_name` | `text` | yes |  | Human-readable name |
| `options_type_id` | `int4` | yes |  | Identifier linking to related record |
| `created` | `date` | yes |  | Timestamp |
| `add_on` | `bool` | yes |  |  |
| `who` | `int4` | yes |  |  |
| `customer_products_id` | `int4` | yes |  | Identifier linking to related record |
| `capacity` | `numeric` | yes |  | Address field |

---

### `view_service_payment_methods`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `payment_method_id` | `int4` | yes |  | Identifier linking to related record |
| `display_info` | `varchar(32)` | yes |  |  |
| `last_updated` | `timestamptz` | yes |  | Timestamp |

---

### `view_service_workflow_matrix`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `product` | `varchar(64)` | yes |  |  |
| `tls_type` | `varchar(64)` | yes |  | Type or category classifier |
| `option` | `varchar(64)` | yes |  |  |
| `option_class` | `varchar(64)` | yes |  |  |
| `workflow_id` | `int4` | yes |  | Identifier linking to related record |
| `location` | `text` | yes |  |  |
| `workflow_event_type_id` | `int4` | yes |  | Identifier linking to related record |
| `workflow_event_type` | `text` | yes |  | Type or category classifier |
| `product_line` | `varchar(255)` | yes |  |  |
| `tracked` | `bool` | yes |  |  |
| `allow_duplicates` | `bool` | yes |  |  |

---

### `view_services_without_device`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `service_name` | `text` | yes |  | Human-readable name |

---

### `view_statistics_orders`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `stat` | `text` | yes |  |  |
| `count` | `int8` | yes |  |  |

---

### `view_statistics_orders_by_status`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `stat` | `varchar(64)` | yes |  |  |
| `count` | `int8` | yes |  |  |

---

### `view_statistics_services`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `stat` | `text` | yes |  |  |
| `count` | `int8` | yes |  |  |

---

### `view_statistics_services_by_datacenter`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `stat` | `text` | yes |  |  |
| `count` | `int8` | yes |  |  |

---

### `view_statistics_services_by_status`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `stat` | `text` | yes |  |  |
| `count` | `int8` | yes |  |  |

---

### `view_statistics_services_by_type`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `stat` | `varchar(64)` | yes |  |  |
| `count` | `int8` | yes |  |  |

---

### `view_ticket_routing_by_product_line`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `product_line` | `varchar(255)` | yes |  |  |
| `category_id` | `int4` | yes |  | Identifier linking to related record |
| `category_name` | `text` | yes |  | Human-readable name |
| `sub_category_id` | `int4` | yes |  | Identifier linking to related record |
| `sub_category_name` | `text` | yes |  | Human-readable name |
| `num_tickets_required` | `int4` | yes |  |  |
| `hours_for_resolution` | `int4` | yes |  |  |
| `support_handler_id` | `int4` | yes |  | Identifier linking to related record |
| `support_handler_name` | `text` | yes |  | Human-readable name |
| `notes` | `text` | yes |  |  |
| `special_form_command` | `text` | yes |  |  |
| `is_customer_facing` | `bool` | yes |  |  |

---

### `view_xref_cloud_storage_policy_component`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `atmos_key` | `varchar(32)` | yes |  |  |
| `type` | `varchar(32)` | yes |  |  |
| `component_id` | `int4` | yes |  | Identifier linking to related record |
| `name` | `varchar(64)` | yes |  |  |

---

### `view_xref_cloud_storage_policy_concession`

**Status:** ✅ < 1 row  
**Type:** VIEW  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `type` | `varchar(32)` | yes |  |  |
| `component_id` | `int4` | yes |  | Identifier linking to related record |
| `app_config_id` | `int4` | yes |  | Identifier linking to related record |
| `value` | `varchar` | yes |  |  |
| `name` | `varchar(64)` | yes |  |  |

---

## Relationships

| From | | To |
|------|---|-----|
| `view_client_payment_methods`.`code` | → | `wallet_responses_pl`.`code` |
| `view_clients`.`payment_term` | → | `payment_terms`.`payment_term` |
| `view_component_required_resources`.`operator` | → | `resource_use_operators`.`operator` |
| `view_oc_cart`.`contract_length` | → | `contract_lengths`.`contract_length` |
| `view_order_line_items`.`contract_length` | → | `contract_lengths`.`contract_length` |
| `view_promotion_criteria_details`.`operator` | → | `resource_use_operators`.`operator` |
| `view_promotion_effect_criteria_details`.`operator` | → | `resource_use_operators`.`operator` |
| `view_promotion_effects_details`.`currency_code` | → | `currencies`.`code` |
