# Fusion DB — Products & Services

**Group:** `products-services`  
**Tables in group:** 87  
**Accessible:** 85  
**Approximate total rows:** 22,478,297  
**Generated:** 2026-05-08 15:54  

## Overview

Product catalog, service type, and component tables. These define what Aptum sells — product lines, service categories, and the components that make up each offering. Used to cross-reference what a customer has against what exists in the catalog, and to identify upsell or EOL exposure.

---

## Table Summary

| Table | Row Count | Columns | Description |
|-------|-----------|---------|-------------|
| `cart_component_private_net` | < 1 | 2 | Records for cart component private net |
| `cart_component_private_rack` | < 1 | 2 | Records for cart component private rack |
| `cart_components` | < 1 | 10 | Records for cart components |
| `cart_default_removed_components` | < 1 | 4 | Records for cart default removed components |
| `client_bag_allowed_service_statuses` | ~10 | 1 | Records for client bag allowed service statuses |
| `client_bag_allowed_service_types` | ~9 | 1 | Records for client bag allowed service types |
| `client_bag_services` | ~7,979 | 3 | Records for client bag services |
| `client_relations_product_line_independent` | ~1,325 | 4 | Records for client relations product line independent |
| `client_solution_services` | ~44,683 | 5 | Records for client solution services |
| `component_capabilities` | ~2,711 | 7 | Records for component capabilities |
| `component_categories` | ~18 | 5 | Lookup/reference table for component categories |
| `component_hashes` | ~4 | 3 | Records for component hashes |
| `component_license_key_node_data` | ~390 | 3 | Records for component license key node data |
| `component_license_keys` | ~227 | 4 | Records for component license keys |
| `component_provided_resources` | ~1,120 | 10 | Records for component provided resources |
| `component_required_resources` | ~684 | 13 | Records for component required resources |
| `component_type_capabilities` | ~105 | 5 | Records for component type capabilities |
| `component_types` | ~386 | 7 | Lookup/reference table for component types |
| `component_workorder_templates` | ~116 | 3 | Records for component workorder templates |
| `components` | ~5,906 | 9 | Lookup/reference table for components |
| `components_attributes` | ~445 | 11 | Records for components attributes |
| `components_tags` | ❌ denied | 2 | Records for components tags |
| `config_code_components` | ~6,401 | 5 | Records for config code components |
| `customer_products_attributes` | ~114,376 | 11 | Records for customer products attributes |
| `customer_products_mercury_services` | ~3,228 | 4 | Records for customer products mercury services |
| `customer_products_status_history` | ~1,514,021 | 5 | Records for customer products status history |
| `customer_products_status_options` | ~13 | 3 | Lookup/reference table for customer products status options |
| `customer_support_faq_product_lines` | ~425 | 3 | Records for customer support faq product lines |
| `employee_client_relations_roles_product_line_independent_matrix` | ~4 | 3 | Records for employee client relations roles product line independent matrix |
| `history_client_bag_services` | ~323,986 | 6 | Audit/history log for `client_bag_services` |
| `history_client_solution_services` | ~661,702 | 5 | Audit/history log for `client_solution_services` |
| `history_components` | ~30,101 | 11 | Audit/history log for `components` |
| `history_product_allowed_components` | ~483,025 | 10 | Audit/history log for `product_allowed_components` |
| `history_product_catalog` | ~8,879 | 12 | Audit/history log for `product_catalog` |
| `history_service_inventory_unavailable` | ~504 | 9 | Audit/history log for `service_inventory_unavailable` |
| `history_service_options` | ~6,127,824 | 20 | Audit/history log for `service_options` |
| `history_xref_customer_products_dcc` | ~371,492 | 6 | Audit/history log for `xref_customer_products_dcc` |
| `history_xref_services_private_net` | ~27,011 | 10 | Audit/history log for `xref_services_private_net` |
| `history_xref_services_private_rack` | ~5,746 | 10 | Audit/history log for `xref_services_private_rack` |
| `kickstart_component_keys` | ~1,234 | 8 | Records for kickstart component keys |
| `olid_service_option_link` | ~263,880 | 4 | Records for olid service option link |
| `product_allowed_components` | ~233,576 | 6 | Records for product allowed components |
| `product_catalog` | ~1,148 | 17 | Lookup/reference table for product catalog |
| `product_catalog_attributes` | ~228 | 11 | Records for product catalog attributes |
| `product_catalog_tags` | ❌ denied | 2 | Records for product catalog tags |
| `product_categories` | ~10 | 7 | Lookup/reference table for product categories |
| `product_class_client_type_discounts` | ~1,857 | 7 | Records for product class client type discounts |
| `product_class_contract_length_discounts` | ~918 | 7 | Records for product class contract length discounts |
| `product_classes` | ~20 | 5 | Lookup/reference table for product classes |
| `product_configuration_changesets` | ~689 | 8 | Records for product configuration changesets |
| `product_configurations` | ~72 | 7 | Records for product configurations |
| `product_frameworks` | ~23,482 | 5 | Records for product frameworks |
| `product_lines` | ~8 | 5 | Lookup/reference table for product lines |
| `product_templates` | ~4,539 | 5 | Records for product templates |
| `promotion_component_criteria` | ~2 | 7 | Records for promotion component criteria |
| `promotion_component_type_criteria` | ~1 | 7 | Records for promotion component type criteria |
| `promotion_component_types` | ~5 | 2 | Records for promotion component types |
| `promotion_effect_component_criteria` | ~3 | 7 | Records for promotion effect component criteria |
| `promotion_effect_component_type_criteria` | < 1 | 7 | Records for promotion effect component type criteria |
| `promotion_effect_product_class_criteria` | < 1 | 7 | Records for promotion effect product class criteria |
| `promotion_effect_product_criteria` | < 1 | 7 | Records for promotion effect product criteria |
| `promotion_product_class_criteria` | ~20 | 7 | Records for promotion product class criteria |
| `promotion_product_classes` | ~98 | 2 | Records for promotion product classes |
| `promotion_product_criteria` | ~42 | 7 | Records for promotion product criteria |
| `sb_customer_product_log` | ~9,703,099 | 7 | Records for sb customer product log |
| `service_account` | < 1 | 5 | Records for service account |
| `service_cancellation_queue` | ~189 | 6 | Records for service cancellation queue |
| `service_inventory_unavailable` | ~312 | 4 | Records for service inventory unavailable |
| `service_licenses` | ~1,158 | 4 | Records for service licenses |
| `service_notes` | ~295,267 | 5 | Records for service notes |
| `service_option_raid_arrays` | ~42,594 | 3 | Records for service option raid arrays |
| `service_option_raid_configuration` | ~103,935 | 4 | Records for service option raid configuration |
| `service_option_types_pl` | ~51 | 5 | Records for service option types pl |
| `service_options` | ~1,850,910 | 17 | Records for service options |
| `service_options_attributes` | ~9,363 | 11 | Records for service options attributes |
| `service_options_mercury_services` | ~1,646 | 4 | Records for service options mercury services |
| `service_type_capabilities` | ~6 | 3 | Records for service type capabilities |
| `service_type_pl` | ~22 | 5 | Records for service type pl |
| `service_workflow_matrix` | ~351 | 9 | Records for service workflow matrix |
| `solution_service_connection_properties` | < 1 | 4 | Records for solution service connection properties |
| `solution_service_connections` | ~4,473 | 7 | Records for solution service connections |
| `xref_cloud_storage_policy_component` | ~10 | 5 | Cross-reference/join table |
| `xref_cloud_storage_subtenants_services` | ~1,111 | 3 | Cross-reference/join table |
| `xref_customer_products_dcc` | ~162,726 | 4 | Cross-reference/join table |
| `xref_services_private_net` | ~20,089 | 7 | Cross-reference/join table |
| `xref_services_private_rack` | ~3,584 | 7 | Cross-reference/join table |
| `xref_ticket_routing_by_product_line` | ~713 | 3 | Cross-reference/join table |

---

## Column Detail

### `cart_component_private_net`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `cart_component_id` | `int4` | no | PK · NOT NULL | Primary key |
| `alias` | `varchar(255)` | no | NOT NULL |  |

**Indexes:**
- `cart_component_private_net_pkey` — UNIQUE (`cart_component_id`)

---

### `cart_component_private_rack`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `cart_component_id` | `int4` | no | PK · NOT NULL | Primary key |
| `alias` | `varchar(255)` | yes |  |  |

**Indexes:**
- `cart_component_private_rack_pkey` — UNIQUE (`cart_component_id`)

---

### `cart_components`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `cart_id` | `int4` | no | NOT NULL | Foreign key → `cart.id` |
| `component_id` | `int4` | yes |  | Foreign key → `components.id` |
| `setup` | `numeric` | no | NOT NULL |  |
| `nrc` | `numeric` | yes |  |  |
| `mrc` | `numeric` | yes |  |  |
| `setup_discount` | `numeric` | yes |  |  |
| `nrc_discount` | `numeric` | yes |  |  |
| `mrc_discount` | `numeric` | yes |  |  |
| `is_default` | `bool` | no | NOT NULL |  |

**Indexes:**
- `cart_components_pkey` — UNIQUE (`id`)
- `cart_components_cart_idx` — (`cart_id`)

---

### `cart_default_removed_components`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | no | PK · NOT NULL | Primary key |
| `cart_id` | `int4` | yes |  | Foreign key → `cart.id` |
| `component_id` | `int4` | yes |  | Foreign key → `components.id` |
| `mrc` | `numeric` | no | NOT NULL |  |

**Indexes:**
- `cart_default_removed_components_pkey` — UNIQUE (`id`)

---

### `client_bag_allowed_service_statuses`

**Status:** ✅ ~10 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `service_status_id` | `int4` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `client_bag_allowed_service_statuses_pkey` — UNIQUE (`service_status_id`)

---

### `client_bag_allowed_service_types`

**Status:** ✅ ~9 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `service_type_id` | `int4` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `client_bag_allowed_service_types_pkey` — UNIQUE (`service_type_id`)

---

### `client_bag_services`

**Status:** ✅ ~7,979 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_bag_id` | `int4` | no | NOT NULL | Foreign key → `client_bags.id` |
| `service_id` | `int4` | no | NOT NULL | Foreign key → `customer_products.id` |

**Indexes:**
- `client_bag_services_pkey` — UNIQUE (`id`)
- `client_bag_services_client_bag_id_key` — UNIQUE (`client_bag_id`, `service_id`)

---

### `client_relations_product_line_independent`

**Status:** ✅ ~1,325 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | no | NOT NULL | Foreign key → `customers.customers_id` |
| `employee_id` | `int4` | no | NOT NULL | Foreign key → `employees.id` |
| `client_relations_role_id` | `int4` | no | NOT NULL | Foreign key → `client_relations_roles.id` |

**Indexes:**
- `client_relations_product_line_independent_pkey` — UNIQUE (`id`)

---

### `client_solution_services`

**Status:** ✅ ~44,683 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_solution_id` | `int4` | no | NOT NULL | Foreign key → `client_solutions.id` |
| `service_id` | `int4` | no | NOT NULL | Foreign key → `customer_products.id` |
| `x` | `int4` | yes |  |  |
| `y` | `int4` | yes |  |  |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `client_solution_services_pkey` — UNIQUE (`id`)
- `client_solution_services_client_solution_id_key` — UNIQUE (`client_solution_id`, `service_id`)

---

### `component_capabilities`

**Status:** ✅ ~2,711 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `component_id` | `int4` | no | PK · NOT NULL | Primary key |
| `component_type_capabilities_id` | `int4` | no | PK · NOT NULL | Primary key |
| `value` | `text` | no | NOT NULL |  |
| `tolerance_min` | `text` | yes |  |  |
| `tolerance_max` | `text` | yes |  |  |
| `is_primary` | `bool` | no | NOT NULL |  |
| `match_required` | `bool` | no | NOT NULL |  |

**Indexes:**
- `component_capabilities_pkey` — UNIQUE (`component_id`, `component_type_capabilities_id`)
- `component_capabilities_component_idx` — (`component_id`)

---

### `component_categories`

**Status:** ✅ ~18 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(32)` | no | NOT NULL |  |
| `description` | `varchar(256)` | no | NOT NULL |  |
| `sort_order` | `int4` | no | NOT NULL |  |
| `is_active` | `bool` | no | NOT NULL | Boolean state flag |

**Indexes:**
- `component_categories_pk` — UNIQUE (`id`)
- `component_categories_name_key` — UNIQUE (`name`)

---

### `component_hashes`

**Status:** ✅ ~4 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `component_id` | `int4` | no | NOT NULL | Foreign key → `components.id` |
| `hash` | `varchar` | no | NOT NULL |  |

**Indexes:**
- `component_hashes_pkey` — UNIQUE (`id`)
- `component_id_idx` — UNIQUE (`component_id`)

---

### `component_license_key_node_data`

**Status:** ✅ ~390 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `component_license_key_id` | `int4` | no | PK · NOT NULL | Primary key |
| `node_name` | `text` | no | PK · NOT NULL | Primary key |
| `node_value` | `text` | no | NOT NULL |  |

**Indexes:**
- `component_license_key_node_data_pkey` — UNIQUE (`component_license_key_id`, `node_name`)

---

### `component_license_keys`

**Status:** ✅ ~227 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `component_id` | `int4` | no | NOT NULL | Foreign key → `components.id` |
| `license_type_id` | `int4` | no | NOT NULL | Foreign key → `license_types.id` |
| `base` | `bool` | no | NOT NULL |  |

**Indexes:**
- `component_license_keys_pkey` — UNIQUE (`id`)
- `component_license_keys_component_id_key` — UNIQUE (`component_id`, `license_type_id`)

---

### `component_provided_resources`

**Status:** ✅ ~1,120 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `component_type_id` | `int4` | yes |  | Foreign key → `component_types.id` |
| `component_id` | `int4` | yes |  | Foreign key → `components.id` |
| `resource_id` | `int4` | no | NOT NULL | Foreign key → `resources.id` |
| `resource_quantity` | `float8` | no | NOT NULL |  |
| `resource_stacking_priority` | `int4` | no | NOT NULL |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `component_provided_resources_pkey` — UNIQUE (`id`)
- `component_provided_resources_component_id_key` — UNIQUE (`component_id`, `resource_id`)
- `component_provided_resources_component_idx` — (`component_id`)
- `component_provided_resources_component_type_id_key` — UNIQUE (`component_type_id`, `resource_id`)
- `component_provided_resources_component_type_idx` — (`component_type_id`)

---

### `component_required_resources`

**Status:** ✅ ~684 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `component_type_id` | `int4` | yes |  | Foreign key → `component_types.id` |
| `component_id` | `int4` | yes |  | Foreign key → `components.id` |
| `use_type_id` | `int4` | yes |  | Foreign key → `resource_use_types.id` |
| `resource_id` | `int4` | yes |  | Foreign key → `resources.id` |
| `operator` | `varchar(3)` | yes |  | Foreign key → `resource_use_operators.operator` |
| `resource_quantity` | `float8` | no | NOT NULL |  |
| `precheck` | `bool` | no | NOT NULL |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `message` | `text` | yes |  |  |

**Indexes:**
- `component_required_resources_pkey` — UNIQUE (`id`)
- `component_required_resources_component_id_key` — UNIQUE (`component_id`, `resource_id`)
- `component_required_resources_component_idx` — (`component_id`)
- `component_required_resources_component_type_id_key` — UNIQUE (`component_type_id`, `resource_id`)
- `component_required_resources_component_type_idx` — (`component_type_id`)

---

### `component_type_capabilities`

**Status:** ✅ ~105 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `component_type_id` | `int4` | no | NOT NULL | Foreign key → `component_types.id` |
| `capabilities_id` | `int4` | no | NOT NULL | Foreign key → `capabilities.id` |
| `datatype` | `text` | no | NOT NULL |  |
| `uom_id` | `int4` | yes |  | Foreign key → `unit_of_measure.id` |

**Indexes:**
- `component_type_capabilities_pkey` — UNIQUE (`id`)
- `component_type_capabilities_component_type_id_key` — UNIQUE (`component_type_id`, `capabilities_id`)

---

### `component_types`

**Status:** ✅ ~386 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `category_id` | `int4` | no | NOT NULL | Foreign key → `component_categories.id` |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `description` | `varchar(256)` | no | NOT NULL |  |
| `is_active` | `bool` | no | NOT NULL | Boolean state flag |
| `parent_component_id` | `int4` | yes |  | Identifier linking to related record |
| `service_option_types_id` | `int4` | no | NOT NULL | Foreign key → `service_option_types_pl.service_option_types_id` |

**Indexes:**
- `component_types_pk` — UNIQUE (`id`)
- `component_types_name_key` — UNIQUE (`name`, `parent_component_id`)

---

### `component_workorder_templates`

**Status:** ✅ ~116 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `component_id` | `int4` | no | NOT NULL | Foreign key → `components.id` |
| `workorder_template` | `text` | yes |  |  |

**Indexes:**
- `component_workorder_templates_pkey` — UNIQUE (`id`)

---

### `components`

**Status:** ✅ ~5,906 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `description` | `varchar(256)` | yes |  |  |
| `is_active` | `bool` | no | NOT NULL | Boolean state flag |
| `modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `component_type_id` | `int4` | no | NOT NULL | Foreign key → `component_types.id` |
| `cost` | `numeric` | yes |  |  |
| `display_name` | `varchar(64)` | no | NOT NULL | Human-readable name |
| `discountable` | `bool` | no | NOT NULL |  |

**Indexes:**
- `components_pk` — UNIQUE (`id`)
- `components_component_type_idx` — (`component_type_id`)
- `components_name_key` — UNIQUE (`name`, `component_type_id`)

---

### `components_attributes`

**Status:** ✅ ~445 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `object_id` | `int4` | no | NOT NULL | Foreign key → `components.id` |
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
- `components_attributes_pkey` — UNIQUE (`id`)

---

### `components_tags`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `component_id` | `int4` | no | PK · NOT NULL | Primary key |
| `tag_id` | `int4` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `components_tags_pkey` — UNIQUE (`component_id`, `tag_id`)
- `components_tags_component_id_idx` — (`component_id`)

---

### `config_code_components`

**Status:** ✅ ~6,401 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `config_id` | `int4` | no | NOT NULL | Foreign key → `config_codes.id` |
| `component_id` | `int4` | no | NOT NULL | Foreign key → `components.id` |
| `is_default` | `bool` | no | NOT NULL |  |
| `removed_component_id` | `int4` | yes |  | Foreign key → `components.id` |

**Indexes:**
- `config_code_components_pkey` — UNIQUE (`id`)

---

### `customer_products_attributes`

**Status:** ✅ ~114,376 rows  
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
| `visibility_group` | `varchar(255)` | yes |  |  |
| `visibility_user` | `varchar(255)` | yes |  |  |

**Indexes:**
- `customer_products_attributes_pkey` — UNIQUE (`id`)
- `customer_products_attributes_object_id_attribute_id_idx` — (`object_id`, `attribute_id`)
- `customer_products_attributes_object_id_idx` — (`object_id`)

---

### `customer_products_mercury_services`

**Status:** ✅ ~3,228 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `customer_products_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `service_num` | `int4` | no | NOT NULL |  |
| `order_line_item_id` | `int4` | yes |  | Identifier linking to related record |

**Indexes:**
- `customer_products_mercury_services_pkey` — UNIQUE (`id`)
- `customer_products_mercury_services_customer_products_id_key` — UNIQUE (`customer_products_id`, `service_num`)

---

### `customer_products_status_history`

**Status:** ✅ ~1,514,021 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `customer_product_id` | `int4` | yes |  | Foreign key → `customer_products.id` |
| `new_value` | `int4` | no | NOT NULL |  |
| `old_value` | `int4` | yes |  |  |
| `date_added` | `timestamptz` | no | NOT NULL |  |

**Indexes:**
- `customer_products_status_history_pkey` — UNIQUE (`id`)
- `customer_products_status_history_customer_product_id_id_idx` — (`customer_product_id`, `id`)
- `customer_products_status_history_customer_proudct_id` — (`customer_product_id`)
- `customer_products_status_history_customer_proudct_id_new_value` — (`customer_product_id`, `new_value`)
- `customer_products_status_history_new_value` — (`new_value`)

---

### `customer_products_status_options`

**Status:** ✅ ~13 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `order_number` | `int4` | no | NOT NULL |  |
| `name` | `text` | no | NOT NULL |  |

**Indexes:**
- `customer_products_status_options_pkey` — UNIQUE (`id`)
- `customer_products_status_options_name_key` — UNIQUE (`name`)
- `customer_products_status_options_order_number_key` — UNIQUE (`order_number`)

---

### `customer_support_faq_product_lines`

**Status:** ✅ ~425 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `customer_support_faq_id` | `int4` | no | NOT NULL | Foreign key → `customer_support_faq.id` |
| `product_line_id` | `int4` | no | NOT NULL | Foreign key → `product_lines.id` |

**Indexes:**
- `customer_support_faq_product_lines_pkey` — UNIQUE (`id`)
- `customer_support_faq_product_lines_customer_support_faq_id_idx` — (`customer_support_faq_id`)

---

### `employee_client_relations_roles_product_line_independent_matrix`

**Status:** ✅ ~4 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `employee_id` | `int4` | no | PK · NOT NULL | Primary key |
| `client_relations_role_id` | `int4` | no | PK · NOT NULL | Primary key |
| `igo_id` | `int4` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `employee_client_relations_roles_product_line_indep_mtx_pkey` — UNIQUE (`employee_id`, `client_relations_role_id`, `igo_id`)

---

### `history_client_bag_services`

**Status:** ✅ ~323,986 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `client_bag_id` | `int4` | yes |  | Identifier linking to related record |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `action` | `varchar(20)` | yes |  |  |
| `archive_date` | `timestamp` | yes |  | Date value |
| `history_client_bag_services_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_client_bag_services_pkey` — UNIQUE (`history_client_bag_services_id`)

---

### `history_client_solution_services`

**Status:** ✅ ~661,702 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_solution_id` | `int4` | yes |  | Identifier linking to related record |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `action` | `varchar(20)` | yes |  |  |
| `archive_date` | `timestamp` | yes |  | Date value |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_client_solution_services_pkey` — UNIQUE (`id`)

---

### `history_components`

**Status:** ✅ ~30,101 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `name` | `varchar(64)` | yes |  |  |
| `description` | `varchar(256)` | yes |  |  |
| `is_active` | `bool` | yes |  | Boolean state flag |
| `modified_by` | `varchar(32)` | yes |  | Timestamp |
| `component_type_id` | `int4` | yes |  | Identifier linking to related record |
| `action` | `varchar(16)` | yes |  |  |
| `archive_date` | `timestamp` | yes |  | Date value |
| `cost` | `numeric` | yes |  |  |
| `discountable` | `bool` | yes |  |  |
| `history_components_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_components_pkey` — UNIQUE (`history_components_id`)
- `history_components_id` — (`id`)

---

### `history_product_allowed_components`

**Status:** ✅ ~483,025 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `product_id` | `int4` | yes |  | Identifier linking to related record |
| `product_name` | `varchar(64)` | yes |  | Human-readable name |
| `component_id` | `int4` | yes |  | Identifier linking to related record |
| `component_name` | `varchar(64)` | yes |  | Human-readable name |
| `available_in_shop` | `bool` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `action` | `varchar(16)` | yes |  |  |
| `archive_date` | `timestamptz` | yes |  | Date value |
| `history_product_allowed_components_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_product_allowed_components_pkey` — UNIQUE (`history_product_allowed_components_id`)

---

### `history_product_catalog`

**Status:** ✅ ~8,879 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `product_class` | `int4` | yes |  |  |
| `name` | `varchar(64)` | yes |  |  |
| `description` | `varchar(1024)` | yes |  |  |
| `is_active` | `bool` | yes |  | Boolean state flag |
| `modified_by` | `varchar(32)` | yes |  | Timestamp |
| `action` | `varchar(16)` | yes |  |  |
| `archive_date` | `timestamp` | yes |  | Date value |
| `available_in_shop` | `bool` | yes |  |  |
| `sold_out` | `bool` | yes |  |  |
| `history_product_catalog_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `discountable` | `bool` | no | NOT NULL |  |

**Indexes:**
- `history_product_catalog_pkey` — UNIQUE (`history_product_catalog_id`)
- `history_product_catalog_id` — (`id`)
- `history_product_catalog_id_date` — (`id`, `archive_date`)

---

### `history_service_inventory_unavailable`

**Status:** ✅ ~504 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `product_id` | `int4` | yes |  | Identifier linking to related record |
| `product_name` | `varchar(64)` | yes |  | Human-readable name |
| `datacenter_id` | `int4` | yes |  | Identifier linking to related record |
| `dc_abbr` | `text` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `action` | `varchar(16)` | yes |  |  |
| `archive_date` | `timestamptz` | yes |  | Date value |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_service_inventory_unavailable_pkey` — UNIQUE (`id`)

---

### `history_service_options`

**Status:** ✅ ~6,127,824 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `options_name` | `text` | yes |  | Human-readable name |
| `options_type_id` | `int4` | yes |  | Identifier linking to related record |
| `created` | `date` | yes |  | Timestamp |
| `add_on` | `bool` | yes |  |  |
| `who` | `int4` | yes |  |  |
| `customer_products_id` | `int4` | yes |  | Identifier linking to related record |
| `action` | `varchar(20)` | yes |  |  |
| `archive_date` | `timestamptz` | yes |  | Date value |
| `component_id` | `int4` | yes |  | Identifier linking to related record |
| `setup` | `numeric` | yes |  |  |
| `nrc` | `numeric` | yes |  |  |
| `mrc` | `numeric` | yes |  |  |
| `currency` | `varchar(3)` | yes |  |  |
| `exchange_rate` | `numeric` | yes |  |  |
| `capacity` | `numeric` | yes |  | Address field |
| `uom_id` | `int4` | yes |  | Identifier linking to related record |
| `history_service_options_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `quantity` | `int4` | yes |  |  |
| `rate` | `numeric` | yes |  |  |

**Indexes:**
- `history_service_options_pkey` — UNIQUE (`history_service_options_id`)

---

### `history_xref_customer_products_dcc`

**Status:** ✅ ~371,492 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `customer_products_id` | `int4` | yes |  | Identifier linking to related record |
| `datacenter_id` | `int4` | yes |  | Identifier linking to related record |
| `device_id` | `varchar(64)` | yes |  | Identifier linking to related record |
| `action` | `varchar(20)` | yes |  |  |
| `archive_date` | `timestamp` | yes |  | Date value |
| `history_xref_customer_products_dcc_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_xref_customer_products_dcc_pkey` — UNIQUE (`history_xref_customer_products_dcc_id`)

---

### `history_xref_services_private_net`

**Status:** ✅ ~27,011 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `private_net_id` | `int4` | yes |  | Identifier linking to related record |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `text` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `text` | yes |  | Timestamp |
| `archive_date` | `timestamptz` | yes |  | Date value |
| `action` | `text` | yes |  |  |
| `history_xref_services_private_net_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_xref_services_private_net_pkey` — UNIQUE (`history_xref_services_private_net_id`)

---

### `history_xref_services_private_rack`

**Status:** ✅ ~5,746 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `private_rack_id` | `int4` | yes |  | Identifier linking to related record |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `text` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `text` | yes |  | Timestamp |
| `archive_date` | `timestamptz` | yes |  | Date value |
| `action` | `text` | yes |  |  |
| `history_xref_services_private_rack_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_xref_services_private_rack_pkey` — UNIQUE (`history_xref_services_private_rack_id`)

---

### `kickstart_component_keys`

**Status:** ✅ ~1,234 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `component_id` | `int4` | no | NOT NULL | Foreign key → `components.id` |
| `key` | `varchar(64)` | no | NOT NULL |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `template_name` | `varchar(64)` | yes |  | Human-readable name |

**Indexes:**
- `kickstart_component_keys_pkey` — UNIQUE (`id`)

---

### `olid_service_option_link`

**Status:** ✅ ~263,880 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `order_line_item_detail_id` | `int4` | no | NOT NULL | Foreign key → `order_line_item_details.id` |
| `order_line_item_id` | `int4` | no | NOT NULL | Foreign key → `order_line_item_details.order_line_item_id` |
| `service_option_id` | `int4` | no | NOT NULL | Foreign key → `service_options.id` |

**Indexes:**
- `olid_service_option_link_pkey` — UNIQUE (`id`)

---

### `product_allowed_components`

**Status:** ✅ ~233,576 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `product_id` | `int4` | no | PK · NOT NULL | Primary key |
| `component_id` | `int4` | no | PK · NOT NULL | Primary key |
| `available_in_shop` | `bool` | no | NOT NULL |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `id` | `int8` | yes |  |  |

**Indexes:**
- `product_allowed_components_pkey` — UNIQUE (`product_id`, `component_id`)
- `product_allowed_components_product_idx` — (`product_id`)

---

### `product_catalog`

**Status:** ✅ ~1,148 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `product_class` | `int4` | no | NOT NULL | Foreign key → `product_classes.id` |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `description` | `varchar(1024)` | no | NOT NULL |  |
| `is_active` | `bool` | no | NOT NULL | Boolean state flag |
| `modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `available_in_shop` | `bool` | no | NOT NULL |  |
| `sold_out` | `bool` | no | NOT NULL |  |
| `category_id` | `int4` | yes |  | Foreign key → `product_categories.id` |
| `product_summary` | `text` | yes |  |  |
| `is_virtual` | `bool` | no | NOT NULL |  |
| `hide_in_portal` | `bool` | no | NOT NULL |  |
| `limited_availability` | `bool` | no | NOT NULL |  |
| `use_picker` | `bool` | no | NOT NULL |  |
| `discountable` | `bool` | no | NOT NULL |  |
| `sku` | `varchar(64)` | yes |  |  |
| `release_date` | `date` | yes |  | Date value |

**Indexes:**
- `product_catalog_pk` — UNIQUE (`id`)
- `product_catalog_name_key` — UNIQUE (`name`)

---

### `product_catalog_attributes`

**Status:** ✅ ~228 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `object_id` | `int4` | no | NOT NULL | Foreign key → `product_catalog.id` |
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
- `product_catalog_attributes_pkey` — UNIQUE (`id`)

---

### `product_catalog_tags`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `product_catalog_id` | `int4` | no | PK · NOT NULL | Primary key |
| `tag_id` | `int4` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `product_catalog_tags_pkey` — UNIQUE (`product_catalog_id`, `tag_id`)
- `product_catalog_tags_product_catalog_id_idx` — (`product_catalog_id`)

---

### `product_categories`

**Status:** ✅ ~10 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `description` | `varchar(1024)` | no | NOT NULL |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `product_categories_pkey` — UNIQUE (`id`)

---

### `product_class_client_type_discounts`

**Status:** ✅ ~1,857 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `product_line` | `int4` | no | PK · NOT NULL | Primary key |
| `product_class` | `int4` | no | PK · NOT NULL | Primary key |
| `client_type_id` | `int4` | no | PK · NOT NULL | Primary key |
| `setup_discount` | `numeric` | no | NOT NULL |  |
| `mrc_discount` | `numeric` | no | NOT NULL |  |
| `nrc_discount` | `numeric` | no | NOT NULL |  |
| `rate_discount` | `numeric` | no | NOT NULL |  |

**Indexes:**
- `product_class_client_type_pkey` — UNIQUE (`product_line`, `product_class`, `client_type_id`)

---

### `product_class_contract_length_discounts`

**Status:** ✅ ~918 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `product_line` | `int4` | no | PK · NOT NULL | Primary key |
| `product_class` | `int4` | no | PK · NOT NULL | Primary key |
| `contract_length` | `int4` | no | PK · NOT NULL | Primary key |
| `setup_discount` | `numeric` | no | NOT NULL |  |
| `mrc_discount` | `numeric` | no | NOT NULL |  |
| `nrc_discount` | `numeric` | no | NOT NULL |  |
| `rate_discount` | `numeric` | no | NOT NULL |  |

**Indexes:**
- `product_class_contract_length_pkey` — UNIQUE (`product_line`, `product_class`, `contract_length`)

---

### `product_classes`

**Status:** ✅ ~20 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(32)` | no | NOT NULL |  |
| `description` | `varchar(256)` | no | NOT NULL |  |
| `sort_order` | `int4` | no | NOT NULL |  |
| `is_active` | `bool` | no | NOT NULL | Boolean state flag |

**Indexes:**
- `product_classes_pk` — UNIQUE (`id`)
- `product_classes_name_key` — UNIQUE (`name`)

---

### `product_configuration_changesets`

**Status:** ✅ ~689 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `configuration_id` | `int4` | no | NOT NULL | Foreign key → `product_configurations.id` |
| `template_component_id` | `int4` | yes |  | Foreign key → `product_templates.id` |
| `new_component_id` | `int4` | no | NOT NULL | Foreign key → `components.id` |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `product_configuration_changesets_pkey` — UNIQUE (`id`)
- `product_configuration_changesets_configuration_id_key` — UNIQUE (`configuration_id`, `template_component_id`)

---

### `product_configurations`

**Status:** ✅ ~72 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `product_id` | `int4` | yes |  | Foreign key → `product_catalog.id` |
| `configuration_name` | `varchar(256)` | no | NOT NULL | Human-readable name |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `product_configurations_pkey` — UNIQUE (`id`)
- `product_configurations_product_id_key` — UNIQUE (`product_id`, `configuration_name`)

---

### `product_frameworks`

**Status:** ✅ ~23,482 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `product_id` | `int4` | no | PK · NOT NULL | Primary key |
| `component_type_id` | `int4` | no | PK · NOT NULL | Primary key |
| `minimum_required` | `int4` | no | NOT NULL |  |
| `maximum_allowed` | `int4` | yes |  |  |
| `modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `product_component_types_pk` — UNIQUE (`product_id`, `component_type_id`)

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

### `product_templates`

**Status:** ✅ ~4,539 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `product_id` | `int4` | no | NOT NULL | Foreign key → `product_catalog.id` |
| `component_id` | `int4` | no | NOT NULL | Foreign key → `components.id` |
| `modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `quantity` | `int4` | no | NOT NULL |  |

**Indexes:**
- `product_templates_pk` — UNIQUE (`id`)
- `product_templates_product_id_idx` — (`product_id`)

---

### `promotion_component_criteria`

**Status:** ✅ ~2 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `promo_id` | `int4` | no | NOT NULL | Foreign key → `promotions.id` |
| `component_id` | `int4` | no | NOT NULL | Foreign key → `components.id` |
| `minimum_quantity` | `int4` | no | NOT NULL |  |
| `depth` | `int4` | no | NOT NULL |  |
| `operator` | `varchar(3)` | no | NOT NULL | Foreign key → `resource_use_operators.operator` |
| `scope` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `promotion_component_criteria_pkey` — UNIQUE (`id`)
- `promotion_component_criteria_promo_id_key` — UNIQUE (`promo_id`, `component_id`)

---

### `promotion_component_type_criteria`

**Status:** ✅ ~1 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `promo_id` | `int4` | no | NOT NULL | Foreign key → `promotions.id` |
| `component_type_id` | `int4` | no | NOT NULL | Foreign key → `component_types.id` |
| `minimum_quantity` | `int4` | no | NOT NULL |  |
| `depth` | `int4` | no | NOT NULL |  |
| `operator` | `varchar(3)` | no | NOT NULL | Foreign key → `resource_use_operators.operator` |
| `scope` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `promotion_component_type_criteria_pkey` — UNIQUE (`id`)
- `promotion_component_type_criteria_promo_id_key` — UNIQUE (`promo_id`, `component_type_id`)

---

### `promotion_component_types`

**Status:** ✅ ~5 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `promotion_id` | `int4` | no | PK · NOT NULL | Primary key |
| `component_type_id` | `int4` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `promotion_component_types_pkey` — UNIQUE (`promotion_id`, `component_type_id`)

---

### `promotion_effect_component_criteria`

**Status:** ✅ ~3 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `effect_id` | `int4` | no | NOT NULL | Foreign key → `promotion_effects.id` |
| `component_id` | `int4` | no | NOT NULL | Foreign key → `components.id` |
| `minimum_quantity` | `int4` | no | NOT NULL |  |
| `depth` | `int4` | no | NOT NULL |  |
| `operator` | `varchar(3)` | no | NOT NULL | Foreign key → `resource_use_operators.operator` |
| `scope` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `promotion_effect_component_criteria_pkey` — UNIQUE (`id`)
- `promotion_effect_component_criteria_effect_id_key` — UNIQUE (`effect_id`, `component_id`)

---

### `promotion_effect_component_type_criteria`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `effect_id` | `int4` | no | NOT NULL | Foreign key → `promotion_effects.id` |
| `component_type_id` | `int4` | no | NOT NULL | Foreign key → `component_types.id` |
| `minimum_quantity` | `int4` | no | NOT NULL |  |
| `depth` | `int4` | no | NOT NULL |  |
| `operator` | `varchar(3)` | no | NOT NULL | Foreign key → `resource_use_operators.operator` |
| `scope` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `promotion_effect_component_type_criteria_pkey` — UNIQUE (`id`)
- `promotion_effect_component_type_criteria_effect_id_key` — UNIQUE (`effect_id`, `component_type_id`)

---

### `promotion_effect_product_class_criteria`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `effect_id` | `int4` | no | NOT NULL | Foreign key → `promotion_effects.id` |
| `product_class_id` | `int4` | no | NOT NULL | Foreign key → `product_classes.id` |
| `minimum_quantity` | `int4` | no | NOT NULL |  |
| `depth` | `int4` | no | NOT NULL |  |
| `operator` | `varchar(3)` | no | NOT NULL | Foreign key → `resource_use_operators.operator` |
| `scope` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `promotion_effect_product_class_criteria_pkey` — UNIQUE (`id`)
- `promotion_effect_product_class_criteria_effect_id_key` — UNIQUE (`effect_id`, `product_class_id`)

---

### `promotion_effect_product_criteria`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `effect_id` | `int4` | no | NOT NULL | Foreign key → `promotion_effects.id` |
| `product_id` | `int4` | no | NOT NULL | Foreign key → `product_catalog.id` |
| `minimum_quantity` | `int4` | no | NOT NULL |  |
| `depth` | `int4` | no | NOT NULL |  |
| `operator` | `varchar(3)` | no | NOT NULL | Foreign key → `resource_use_operators.operator` |
| `scope` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `promotion_effect_product_criteria_pkey` — UNIQUE (`id`)
- `promotion_effect_product_criteria_effect_id_key` — UNIQUE (`effect_id`, `product_id`)

---

### `promotion_product_class_criteria`

**Status:** ✅ ~20 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `promo_id` | `int4` | no | NOT NULL | Foreign key → `promotions.id` |
| `product_class_id` | `int4` | no | NOT NULL | Foreign key → `product_classes.id` |
| `minimum_quantity` | `int4` | no | NOT NULL |  |
| `depth` | `int4` | no | NOT NULL |  |
| `operator` | `varchar(3)` | no | NOT NULL | Foreign key → `resource_use_operators.operator` |
| `scope` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `promotion_product_class_criteria_pkey` — UNIQUE (`id`)
- `promotion_product_class_criteria_promo_id_key` — UNIQUE (`promo_id`, `product_class_id`)

---

### `promotion_product_classes`

**Status:** ✅ ~98 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `promotion_id` | `int4` | no | PK · NOT NULL | Primary key |
| `product_class_id` | `int4` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `promotion_product_classes_pkey` — UNIQUE (`promotion_id`, `product_class_id`)

---

### `promotion_product_criteria`

**Status:** ✅ ~42 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `promo_id` | `int4` | no | NOT NULL | Foreign key → `promotions.id` |
| `product_id` | `int4` | no | NOT NULL | Foreign key → `product_catalog.id` |
| `minimum_quantity` | `int4` | no | NOT NULL |  |
| `depth` | `int4` | no | NOT NULL |  |
| `operator` | `varchar(3)` | no | NOT NULL | Foreign key → `resource_use_operators.operator` |
| `scope` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `promotion_product_criteria_pkey` — UNIQUE (`id`)
- `promotion_product_criteria_promo_id_key` — UNIQUE (`promo_id`, `product_id`)

---

### `sb_customer_product_log`

**Status:** ✅ ~9,703,099 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `customer_product_id` | `int4` | yes |  | Foreign key → `customer_products.id` |
| `log_type_id` | `int4` | yes |  | Foreign key → `sb_log_type.id` |
| `message` | `text` | yes |  |  |
| `logged_by` | `text` | yes |  |  |
| `logged_on` | `timestamptz` | yes |  |  |
| `ticket_id` | `int4` | yes |  | Identifier linking to related record |

**Indexes:**
- `sb_customer_product_log_pkey` — UNIQUE (`id`)
- `customer_product_log_log_type_id` — (`log_type_id`)
- `id_log_type_customer_product_log` — (`id`, `log_type_id`)
- `logged_on_log` — (`logged_on`)
- `sb_customer_product_log_customer_product_idx` — (`customer_product_id`)

---

### `service_account`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `username` | `varchar(64)` | no | NOT NULL |  |
| `password` | `varchar(64)` | no | NOT NULL |  |
| `description` | `varchar(256)` | no | NOT NULL |  |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `service_account_pkey` — UNIQUE (`id`)

---

### `service_cancellation_queue`

**Status:** ✅ ~189 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `service_id` | `int4` | no | PK · NOT NULL | Primary key |
| `queue_date` | `timestamptz` | no | NOT NULL | Date value |
| `cancellation_date` | `timestamptz` | no | NOT NULL | Date value |
| `last_email_date` | `timestamptz` | yes |  | Date value |
| `ticket_id` | `int4` | yes |  | Identifier linking to related record |
| `reason` | `varchar(1024)` | yes |  |  |

**Indexes:**
- `service_cancellation_queue_pkey` — UNIQUE (`service_id`)

---

### `service_inventory_unavailable`

**Status:** ✅ ~312 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `product_id` | `int4` | no | PK · NOT NULL | Primary key |
| `datacenter_id` | `int4` | no | PK · NOT NULL | Primary key |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `service_inventory_unavailable_pkey` — UNIQUE (`product_id`, `datacenter_id`)

---

### `service_licenses`

**Status:** ✅ ~1,158 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `lkg_id` | `int4` | yes |  | Identifier linking to related record |
| `service_id` | `int4` | yes |  | Foreign key → `customer_products.id` |
| `license_type_id` | `int4` | yes |  | Foreign key → `license_types.id` |

**Indexes:**
- `service_licenses_pkey` — UNIQUE (`id`)
- `unique_lkg_id_service_id` — UNIQUE (`lkg_id`, `service_id`)

---

### `service_notes`

**Status:** ✅ ~295,267 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `service_id` | `int4` | no | NOT NULL | Foreign key → `customer_products.id` |
| `message` | `varchar` | no | NOT NULL |  |
| `date` | `timestamptz` | no | NOT NULL |  |
| `who` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `service_notes_pkey` — UNIQUE (`id`)

---

### `service_option_raid_arrays`

**Status:** ✅ ~42,594 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `raid_card_id` | `int4` | no | NOT NULL | Foreign key → `service_options.id` |
| `raid_level_id` | `int4` | no | NOT NULL | Foreign key → `raid_levels.id` |

**Indexes:**
- `service_option_raid_arrays_pkey` — UNIQUE (`id`)
- `service_option_raid_arrays_raid_card_idx` — (`raid_card_id`)
- `service_option_raid_configuration_raid_service_option_idx` — (`raid_card_id`)

---

### `service_option_raid_configuration`

**Status:** ✅ ~103,935 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `raid_option_id` | `int4` | no | PK · NOT NULL | Primary key |
| `raid_card_id` | `int4` | no | NOT NULL | Foreign key → `service_options.id` |
| `raid_array_id` | `int4` | yes |  | Foreign key → `service_option_raid_arrays.id` |
| `role` | `raid_roles` | no | NOT NULL |  |

**Indexes:**
- `service_option_raid_configuration_pkey` — UNIQUE (`raid_option_id`)

---

### `service_option_types_pl`

**Status:** ✅ ~51 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `service_option_types_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `description` | `varchar(255)` | no | NOT NULL |  |
| `sort_order` | `int4` | no | NOT NULL |  |
| `is_active` | `bool` | no | NOT NULL | Boolean state flag |

**Indexes:**
- `service_option_types_pl_pkey` — UNIQUE (`service_option_types_id`)
- `unique_name` — UNIQUE (`name`)

---

### `service_options`

**Status:** ✅ ~1,850,910 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `options_name` | `text` | yes |  | Human-readable name |
| `options_type_id` | `int4` | yes |  | Foreign key → `service_option_types_pl.service_option_types_id` |
| `created` | `date` | no | NOT NULL | Timestamp |
| `add_on` | `bool` | yes |  |  |
| `who` | `int4` | yes |  |  |
| `customer_products_id` | `int4` | yes |  | Foreign key → `customer_products.id` |
| `capacity` | `numeric` | yes |  | Address field |
| `uom_id` | `int4` | yes |  | Foreign key → `unit_of_measure.id` |
| `component_id` | `int4` | yes |  | Foreign key → `components.id` |
| `setup` | `numeric` | no | NOT NULL |  |
| `nrc` | `numeric` | no | NOT NULL |  |
| `mrc` | `numeric` | no | NOT NULL |  |
| `currency` | `varchar(3)` | no | NOT NULL | Foreign key → `currencies.code` |
| `exchange_rate` | `numeric` | no | NOT NULL |  |
| `quantity` | `int4` | no | NOT NULL |  |
| `rate` | `numeric` | yes |  |  |

**Indexes:**
- `service_options_pk` — UNIQUE (`id`)
- `customer_products_options_names` — (`customer_products_id`, `options_name`)
- `service_options_pci_index` — (`options_name`)

---

### `service_options_attributes`

**Status:** ✅ ~9,363 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `object_id` | `int4` | no | NOT NULL | Foreign key → `service_options.id` |
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
- `service_options_attributes_pkey` — UNIQUE (`id`)

---

### `service_options_mercury_services`

**Status:** ✅ ~1,646 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `service_options_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `service_num` | `int4` | no | NOT NULL |  |
| `order_line_item_detail_id` | `int4` | yes |  | Identifier linking to related record |

**Indexes:**
- `service_options_mercury_services_pkey` — UNIQUE (`id`)
- `service_options_mercury_services_service_options_id_key` — UNIQUE (`service_options_id`, `service_num`)

---

### `service_type_capabilities`

**Status:** ✅ ~6 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `service_type_id` | `int4` | no | NOT NULL | Foreign key → `service_type_pl.service_type_id` |
| `capabilities_id` | `int4` | no | NOT NULL | Foreign key → `capabilities.id` |

**Indexes:**
- `service_type_capabilities_pkey` — UNIQUE (`id`)

---

### `service_type_pl`

**Status:** ✅ ~22 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `service_type_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `description` | `varchar(255)` | no | NOT NULL |  |
| `sort_order` | `int4` | yes |  |  |
| `is_active` | `bool` | yes |  | Boolean state flag |

**Indexes:**
- `service_type_pl_pkey` — UNIQUE (`service_type_id`)

---

### `service_workflow_matrix`

**Status:** ✅ ~351 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `product` | `varchar(64)` | yes |  |  |
| `tls_type` | `varchar(64)` | no | NOT NULL | Type or category classifier |
| `option` | `varchar(64)` | yes |  |  |
| `option_class` | `varchar(64)` | yes |  |  |
| `workflow_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `datacenter_id` | `int4` | yes |  | Foreign key → `sb_datacenter.id` |
| `workflow_event_type_id` | `int4` | no | NOT NULL | Foreign key → `workflow_event_types.id` |
| `product_line_id` | `int4` | yes |  | Foreign key → `product_lines.id` |

**Indexes:**
- `service_workflow_matrix_pkey` — UNIQUE (`id`)
- `service_workflow_matrix_product_key` — UNIQUE (`product`, `tls_type`, `option`, `option_class`, `workflow_event_type_id`, `workflow_id`)

---

### `solution_service_connection_properties`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `solution_service_connection_id` | `int4` | no | NOT NULL | Foreign key → `solution_service_connections.solution_service_connection_id` |
| `connection_property_name` | `varchar(32)` | no | NOT NULL | Foreign key → `solution_connection_property_types.connection_property_name` |
| `connection_property_value` | `varchar(256)` | no | NOT NULL |  |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `solution_service_connection_properties_pkey` — UNIQUE (`id`)

---

### `solution_service_connections`

**Status:** ✅ ~4,473 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `solution_service_connection_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_solution_id` | `int4` | no | NOT NULL | Foreign key → `client_solution_services.client_solution_id` |
| `service1` | `int4` | no | NOT NULL | Foreign key → `client_solution_services.service_id` |
| `service1_vertex` | `int4` | no | NOT NULL |  |
| `service2` | `int4` | no | NOT NULL | Foreign key → `client_solution_services.service_id` |
| `service2_vertex` | `int4` | no | NOT NULL |  |
| `directed` | `bool` | no | NOT NULL |  |

**Indexes:**
- `solution_service_connections_pkey` — UNIQUE (`solution_service_connection_id`)

---

### `xref_cloud_storage_policy_component`

**Status:** ✅ ~10 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `atmos_key` | `varchar(32)` | no | NOT NULL |  |
| `description` | `varchar(200)` | yes |  |  |
| `type` | `varchar(32)` | no | NOT NULL |  |
| `component_id` | `int4` | yes |  | Foreign key → `components.id` |

**Indexes:**
- `xref_cloud_storage_policy_component_pkey` — UNIQUE (`id`)
- `xref_cloud_storage_policy_component_component_id_key` — UNIQUE (`component_id`)

---

### `xref_cloud_storage_subtenants_services`

**Status:** ✅ ~1,111 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `subtenant_id` | `varchar(50)` | no | NOT NULL | Identifier linking to related record |
| `service_id` | `int4` | no | NOT NULL | Foreign key → `customer_products.id` |

**Indexes:**
- `xref_cloud_storage_subtenants_services_pkey` — UNIQUE (`id`)
- `xref_cloud_storage_subtenants_services_subtenant_id_key` — UNIQUE (`subtenant_id`)

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

### `xref_services_private_net`

**Status:** ✅ ~20,089 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `private_net_id` | `int4` | no | NOT NULL | Foreign key → `client_private_net.id` |
| `service_id` | `int4` | no | NOT NULL | Foreign key → `customer_products.id` |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `text` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `text` | no | NOT NULL | Timestamp |

**Indexes:**
- `xref_services_private_net_pkey` — UNIQUE (`id`)
- `xref_services_private_net_service_id_key` — UNIQUE (`service_id`)

---

### `xref_services_private_rack`

**Status:** ✅ ~3,584 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `private_rack_id` | `int4` | yes |  | Foreign key → `client_private_rack.id` |
| `service_id` | `int4` | yes |  | Foreign key → `customer_products.id` |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `text` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `text` | yes |  | Timestamp |

**Indexes:**
- `xref_services_private_rack_pkey` — UNIQUE (`id`)
- `xref_services_private_rack_service_id_key` — UNIQUE (`service_id`)

---

### `xref_ticket_routing_by_product_line`

**Status:** ✅ ~713 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `xref_customer_support_type_sub_type_id` | `int4` | no | NOT NULL | Foreign key → `xref_customer_support_type_sub_type.id` |
| `product_line_id` | `int4` | yes |  | Foreign key → `product_lines.id` |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `xref_ticket_routing_by_product_line_pkey` — UNIQUE (`id`)
- `unique_type_sub_type_handler_brand` — UNIQUE (`xref_customer_support_type_sub_type_id`, `product_line_id`)

---

## Relationships

| From | | To |
|------|---|-----|
| `cart_components`.`cart_id` | → | `cart`.`id` |
| `cart_default_removed_components`.`cart_id` | → | `cart`.`id` |
| `client_bag_services`.`client_bag_id` | → | `client_bags`.`id` |
| `client_bag_services`.`service_id` | → | `customer_products`.`id` |
| `client_relations_product_line_independent`.`client_id` | → | `customers`.`customers_id` |
| `client_relations_product_line_independent`.`employee_id` | → | `employees`.`id` |
| `client_relations_product_line_independent`.`client_relations_role_id` | → | `client_relations_roles`.`id` |
| `client_solution_services`.`client_solution_id` | → | `client_solutions`.`id` |
| `client_solution_services`.`service_id` | → | `customer_products`.`id` |
| `component_license_keys`.`license_type_id` | → | `license_types`.`id` |
| `component_provided_resources`.`resource_id` | → | `resources`.`id` |
| `component_required_resources`.`use_type_id` | → | `resource_use_types`.`id` |
| `component_required_resources`.`resource_id` | → | `resources`.`id` |
| `component_required_resources`.`operator` | → | `resource_use_operators`.`operator` |
| `component_type_capabilities`.`capabilities_id` | → | `capabilities`.`id` |
| `component_type_capabilities`.`uom_id` | → | `unit_of_measure`.`id` |
| `components_attributes`.`attribute_id` | → | `attributes`.`id` |
| `config_code_components`.`config_id` | → | `config_codes`.`id` |
| `customer_products_attributes`.`object_id` | → | `customer_products`.`id` |
| `customer_products_attributes`.`attribute_id` | → | `attributes`.`id` |
| `customer_products_status_history`.`customer_product_id` | → | `customer_products`.`id` |
| `customer_support_faq_product_lines`.`customer_support_faq_id` | → | `customer_support_faq`.`id` |
| `olid_service_option_link`.`order_line_item_detail_id` | → | `order_line_item_details`.`id` |
| `olid_service_option_link`.`order_line_item_id` | → | `order_line_item_details`.`order_line_item_id` |
| `product_catalog_attributes`.`attribute_id` | → | `attributes`.`id` |
| `product_class_client_type_discounts`.`client_type_id` | → | `client_types_pl`.`client_type_id` |
| `product_class_contract_length_discounts`.`contract_length` | → | `contract_lengths`.`contract_length` |
| `promotion_component_criteria`.`promo_id` | → | `promotions`.`id` |
| `promotion_component_criteria`.`operator` | → | `resource_use_operators`.`operator` |
| `promotion_component_type_criteria`.`promo_id` | → | `promotions`.`id` |
| `promotion_component_type_criteria`.`operator` | → | `resource_use_operators`.`operator` |
| `promotion_component_types`.`promotion_id` | → | `promotions`.`id` |
| `promotion_effect_component_criteria`.`effect_id` | → | `promotion_effects`.`id` |
| `promotion_effect_component_criteria`.`operator` | → | `resource_use_operators`.`operator` |
| `promotion_effect_component_type_criteria`.`effect_id` | → | `promotion_effects`.`id` |
| `promotion_effect_component_type_criteria`.`operator` | → | `resource_use_operators`.`operator` |
| `promotion_effect_product_class_criteria`.`effect_id` | → | `promotion_effects`.`id` |
| `promotion_effect_product_class_criteria`.`operator` | → | `resource_use_operators`.`operator` |
| `promotion_effect_product_criteria`.`effect_id` | → | `promotion_effects`.`id` |
| `promotion_effect_product_criteria`.`operator` | → | `resource_use_operators`.`operator` |
| `promotion_product_class_criteria`.`promo_id` | → | `promotions`.`id` |
| `promotion_product_class_criteria`.`operator` | → | `resource_use_operators`.`operator` |
| `promotion_product_classes`.`promotion_id` | → | `promotions`.`id` |
| `promotion_product_criteria`.`promo_id` | → | `promotions`.`id` |
| `promotion_product_criteria`.`operator` | → | `resource_use_operators`.`operator` |
| `sb_customer_product_log`.`customer_product_id` | → | `customer_products`.`id` |
| `sb_customer_product_log`.`log_type_id` | → | `sb_log_type`.`id` |
| `service_cancellation_queue`.`service_id` | → | `customer_products`.`id` |
| `service_inventory_unavailable`.`datacenter_id` | → | `sb_datacenter`.`id` |
| `service_licenses`.`service_id` | → | `customer_products`.`id` |
| `service_licenses`.`license_type_id` | → | `license_types`.`id` |
| `service_notes`.`service_id` | → | `customer_products`.`id` |
| `service_option_raid_arrays`.`raid_level_id` | → | `raid_levels`.`id` |
| `service_options`.`customer_products_id` | → | `customer_products`.`id` |
| `service_options`.`uom_id` | → | `unit_of_measure`.`id` |
| `service_options`.`currency` | → | `currencies`.`code` |
| `service_options_attributes`.`attribute_id` | → | `attributes`.`id` |
| `service_type_capabilities`.`capabilities_id` | → | `capabilities`.`id` |
| `service_workflow_matrix`.`datacenter_id` | → | `sb_datacenter`.`id` |
| `service_workflow_matrix`.`workflow_event_type_id` | → | `workflow_event_types`.`id` |
| `solution_service_connection_properties`.`connection_property_name` | → | `solution_connection_property_types`.`connection_property_name` |
| `xref_cloud_storage_subtenants_services`.`service_id` | → | `customer_products`.`id` |
| `xref_customer_products_dcc`.`customer_products_id` | → | `customer_products`.`id` |
| `xref_customer_products_dcc`.`datacenter_id` | → | `sb_datacenter`.`id` |
| `xref_services_private_net`.`private_net_id` | → | `client_private_net`.`id` |
| `xref_services_private_net`.`service_id` | → | `customer_products`.`id` |
| `xref_services_private_rack`.`private_rack_id` | → | `client_private_rack`.`id` |
| `xref_services_private_rack`.`service_id` | → | `customer_products`.`id` |
| `xref_ticket_routing_by_product_line`.`xref_customer_support_type_sub_type_id` | → | `xref_customer_support_type_sub_type`.`id` |
| `cart_raid_array_drives`.`drive_id` | → | `cart_components`.`id` |
| `contract_types`.`component_category` | → | `component_categories`.`id` |
| `item_tax_schedule`.`component_category` | → | `component_categories`.`id` |
| `cart_order`.`component_type` | → | `component_types`.`id` |
| `cloud_storage_tiered_discounts`.`component_id` | → | `components`.`id` |
| `order_line_item_details`.`component_id` | → | `components`.`id` |
| `pricebook`.`component_id` | → | `components`.`id` |
| `xref_cloud_storage_policy_concession`.`component_id` | → | `components`.`id` |
| `config_code_pnet`.`config_component_id` | → | `config_code_components`.`id` |
| `customer_products`.`products_status_id` | → | `customer_products_status_options`.`id` |
| `byo_upsell`.`product_id` | → | `product_catalog`.`id` |
| `byo_upsell`.`upsell_product_id` | → | `product_catalog`.`id` |
| `cart`.`product_id` | → | `product_catalog`.`id` |
| `config_codes`.`product_id` | → | `product_catalog`.`id` |
| `customer_products`.`product_catalog_id` | → | `product_catalog`.`id` |
| `order_line_items`.`tls_id` | → | `product_catalog`.`id` |
| `preconfigured_bundle_mapping`.`product_id` | → | `product_catalog`.`id` |
| `pricebook`.`product_catalog_id` | → | `product_catalog`.`id` |
| `tls_workorder_templates`.`product_id` | → | `product_catalog`.`id` |
| `contract_types`.`product_class_id` | → | `product_classes`.`id` |
| `item_tax_schedule`.`product_class_id` | → | `product_classes`.`id` |
| `preconfigured_bundle_mapping`.`product_configuration_id` | → | `product_configurations`.`id` |
| `client_relations`.`product_line_id` | → | `product_lines`.`id` |
| `contract_types`.`product_line_id` | → | `product_lines`.`id` |
| `customer_products`.`product_line_id` | → | `product_lines`.`id` |
| `employee_client_relations_roles_matrix`.`product_line_id` | → | `product_lines`.`id` |
| `order_line_items`.`product_line_id` | → | `product_lines`.`id` |
| `pricebook`.`product_line_id` | → | `product_lines`.`id` |
| `options_licenses`.`options_id` | → | `service_options`.`id` |
| `order_line_item_details`.`service_option_id` | → | `service_options`.`id` |
| `customer_products`.`service_type_id` | → | `service_type_pl`.`service_type_id` |
