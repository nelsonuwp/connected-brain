# Fusion DB — Remaining Accessible Tables (H–Z)

**Group:** `remaining-accessible-h-z`  
**Tables in group:** 95  
**Accessible:** 95  
**Approximate total rows:** 22,613,566  
**Generated:** 2026-05-08 15:54  

## Overview

Accessible tables that don't fit neatly into the domain groups above. May include audit logs, configuration tables, cross-reference tables, or legacy tables with low direct relevance to AccountIntel. Worth scanning for unexpected signals (e.g., feature flags, status history).

(Split at 'H' due to size)

---

## Table Summary

| Table | Row Count | Columns | Description |
|-------|-----------|---------|-------------|
| `history_workflow_notifications` | ~66,573 | 9 | Audit/history log for `workflow_notifications` |
| `intergovernmental_organizations` | ~3 | 3 | Lookup/reference table for intergovernmental organizations |
| `item_tax_schedule` | ~5,756 | 11 | Records for item tax schedule |
| `license_types` | ~8 | 4 | Lookup/reference table for license types |
| `line_sequence_mapping` | ~46,429 | 2 | Records for line sequence mapping |
| `login_history` | ~3,808,951 | 7 | Records for login history |
| `message_box` | ~1,695,041 | 3 | Records for message box |
| `mon_runbook_custom_notes` | ~169 | 5 | Records for mon runbook custom notes |
| `mon_runbook_default_notes` | ~61 | 3 | Records for mon runbook default notes |
| `my_rbac_pages` | ~263 | 5 | Records for my rbac pages |
| `my_rbac_sections` | ~15 | 2 | Records for my rbac sections |
| `node_types` | ~2 | 2 | Records for node types |
| `ocean_config` | ~2 | 5 | Records for ocean config |
| `ocean_restrictions` | ~269 | 4 | Records for ocean restrictions |
| `ocean_sessions` | ~7,246 | 7 | Records for ocean sessions |
| `options_licenses` | ~5,917 | 4 | Records for options licenses |
| `order_commission_split` | ~69,202 | 4 | Records for order commission split |
| `order_communications` | ~40,626 | 5 | Records for order communications |
| `order_entry_solution_link` | ~12,572 | 3 | Records for order entry solution link |
| `order_entry_solution_node` | ~11,333 | 2 | Records for order entry solution node |
| `order_line_item_attributes` | ~98,941 | 4 | Lookup/reference table for order line item attributes |
| `order_line_item_detail_attributes` | ~449,045 | 6 | Lookup/reference table for order line item detail attributes |
| `order_line_item_detail_workorder_tickets` | ~11,366 | 4 | Records for order line item detail workorder tickets |
| `order_line_item_details` | ~5,390,359 | 21 | Records for order line item details |
| `order_line_item_types` | ~4 | 2 | Lookup/reference table for order line item types |
| `order_line_item_workorder_tickets` | ~4,734 | 4 | Records for order line item workorder tickets |
| `order_line_items` | ~375,211 | 37 | Records for order line items |
| `order_notes` | < 1 | 5 | Records for order notes |
| `p1_zones` | ~395 | 1 | Records for p1 zones |
| `package` | < 1 | 7 | Records for package |
| `partition_details` | ~55,051 | 14 | Records for partition details |
| `partition_object_types` | ~2 | 2 | Records for partition object types |
| `partitions` | ~18,146 | 8 | Records for partitions |
| `permission_categories` | ~4 | 7 | Records for permission categories |
| `permissions` | ~58 | 9 | Records for permissions |
| `portal_login` | ~204,312 | 5 | Records for portal login |
| `preconfigured_bundle_categories` | ~6 | 6 | Lookup/reference table for preconfigured bundle categories |
| `preconfigured_bundle_mapping` | ~216 | 11 | Records for preconfigured bundle mapping |
| `pricebook` | ~43,198 | 12 | Records for pricebook |
| `promotion_contract_length_criteria` | ~2 | 7 | Records for promotion contract length criteria |
| `promotion_criteria_types` | ~7 | 3 | Lookup/reference table for promotion criteria types |
| `promotion_customer_type_criteria` | ~10 | 7 | Records for promotion customer type criteria |
| `promotion_effect_amounts` | ~2,094 | 5 | Records for promotion effect amounts |
| `promotion_effect_target_amount_types` | ~3 | 2 | Lookup/reference table for promotion effect target amount types |
| `promotion_effect_target_types` | ~3 | 2 | Lookup/reference table for promotion effect target types |
| `promotion_effect_types` | ~4 | 2 | Lookup/reference table for promotion effect types |
| `promotion_effects` | ~1,411 | 6 | Records for promotion effects |
| `promotion_location_criteria` | ~42 | 7 | Records for promotion location criteria |
| `promotion_types` | ~2 | 3 | Lookup/reference table for promotion types |
| `promotions` | ~155 | 10 | Records for promotions |
| `provisioning_tickets` | ~5,216 | 4 | Records for provisioning tickets |
| `queue_messages` | ~1,792,446 | 5 | Records for queue messages |
| `queues` | ~68 | 3 | Records for queues |
| `raid_levels` | ~11 | 6 | Lookup/reference table for raid levels |
| `resource_use_operators` | ~6 | 3 | Records for resource use operators |
| `resource_use_types` | ~2 | 3 | Lookup/reference table for resource use types |
| `resources` | ~35 | 4 | Lookup/reference table for resources |
| `rss_feed_spotlight` | < 1 | 4 | Records for rss feed spotlight |
| `rss_feeds` | < 1 | 6 | Records for rss feeds |
| `sb_customer_log` | ~6,316,303 | 7 | Records for sb customer log |
| `sb_log_type` | ~16 | 2 | Lookup/reference table for sb log type |
| `secret_questions_pl` | ~5 | 2 | Records for secret questions pl |
| `sessions` | ~3,156 | 5 | Records for sessions |
| `solution_connection_property_types` | ~3 | 2 | Records for solution connection property types |
| `task_status_pl` | ~6 | 5 | Records for task status pl |
| `tax_registration_types` | ~3 | 5 | Records for tax registration types |
| `ticket_support_time_types` | ~4 | 5 | Lookup/reference table for ticket support time types |
| `ticket_support_times` | ~2,038,533 | 9 | Records for ticket support times |
| `tls_workorder_templates` | ~22 | 3 | Records for tls workorder templates |
| `transactions_pending_client_approval` | < 1 | 5 | Records for transactions pending client approval |
| `unit_of_measure` | ~30 | 5 | Lookup/reference table for unit of measure |
| `vam_admin_account` | ~973 | 5 | Records for vam admin account |
| `vam_agent` | ~2,786 | 4 | Records for vam agent |
| `vam_agent_account` | ~2,896 | 5 | Records for vam agent account |
| `vam_cache` | ~11,623 | 5 | Records for vam cache |
| `vam_client` | ~979 | 4 | Records for vam client |
| `vam_configuration` | ~2,786 | 4 | Records for vam configuration |
| `vam_escalation_definition` | ~2,785 | 4 | Records for vam escalation definition |
| `vam_resources` | ~12 | 5 | Records for vam resources |
| `vmware_clusters` | ~418 | 3 | Records for vmware clusters |
| `vmware_guests` | ~4,374 | 3 | Records for vmware guests |
| `vmware_vcenters` | ~497 | 2 | Records for vmware vcenters |
| `volume_discount_percentage` | ~20 | 7 | Records for volume discount percentage |
| `wallet_responses_pl` | ~20 | 2 | Records for wallet responses pl |
| `widget_input_parameters` | ~321 | 5 | Records for widget input parameters |
| `widget_output_parameters` | ~357 | 5 | Records for widget output parameters |
| `widget_transaction_states` | < 1 | 3 | Lookup/reference table for widget transaction states |
| `widget_types_pl` | ~42 | 5 | Records for widget types pl |
| `widgets` | ~187 | 10 | Records for widgets |
| `workflow_event_types` | ~16 | 4 | Lookup/reference table for workflow event types |
| `workflow_notifications` | < 1 | 8 | Records for workflow notifications |
| `xref_cloud_storage_policy_concession` | ~1 | 8 | Cross-reference/join table |
| `xref_customer_support_type_sub_type` | ~435 | 9 | Cross-reference/join table |
| `xref_rbac_pages_to_sections` | ~218 | 3 | Cross-reference/join table |
| `zones` | ~736 | 4 | Records for zones |

---

## Column Detail

### `history_workflow_notifications`

**Status:** ✅ ~66,573 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `workflow_instance_id` | `int4` | yes |  | Identifier linking to related record |
| `event_type` | `varchar` | yes |  | Type or category classifier |
| `created` | `timestamptz` | yes |  | Timestamp |
| `resolved` | `timestamptz` | yes |  |  |
| `status` | `varchar` | yes |  |  |
| `message` | `varchar` | yes |  |  |
| `history_workflow_notifications_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_workflow_notifications_pkey` — UNIQUE (`history_workflow_notifications_id`)

---

### `intergovernmental_organizations`

**Status:** ✅ ~3 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `text` | yes |  |  |
| `abbr` | `varchar(16)` | yes |  |  |

**Indexes:**
- `intergovernmental_organizations_pkey` — UNIQUE (`id`)

---

### `item_tax_schedule`

**Status:** ✅ ~5,756 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `product_class_id` | `int4` | yes |  | Foreign key → `product_classes.id` |
| `component_category` | `int4` | yes |  | Foreign key → `component_categories.id` |
| `datacenter` | `int4` | no | NOT NULL | Foreign key → `sb_datacenter.id` |
| `client_countries_id` | `int4` | yes |  | Foreign key → `countries.countries_id` |
| `client_state` | `varchar(255)` | yes |  |  |
| `contract_type` | `varchar(255)` | no | NOT NULL | Type or category classifier |
| `mrc_tax_id` | `int4` | yes |  | Foreign key → `tax_rates.id` |
| `nrc_tax_id` | `int4` | yes |  | Foreign key → `tax_rates.id` |
| `setup_tax_id` | `int4` | yes |  | Foreign key → `tax_rates.id` |
| `rate_tax_id` | `int4` | yes |  | Foreign key → `tax_rates.id` |

**Indexes:**
- `item_tax_schedule_pkey` — UNIQUE (`id`)
- `component_tax_idx` — (`component_category`, `datacenter`, `client_countries_id`, `client_state`)
- `product_tax_idx` — (`product_class_id`, `datacenter`, `client_countries_id`, `client_state`)

---

### `license_types`

**Status:** ✅ ~8 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `uri` | `varchar(256)` | no | NOT NULL |  |
| `type` | `varchar(32)` | yes |  |  |

**Indexes:**
- `license_types_pkey` — UNIQUE (`id`)
- `license_types_name_key` — UNIQUE (`name`)

---

### `line_sequence_mapping`

**Status:** ✅ ~46,429 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `old_line_sequence_number` | `float8` | no | NOT NULL |  |
| `new_line_sequence_number` | `float8` | no | NOT NULL |  |

**Indexes:**
- `line_sequence_mapping_new_line_sequence_number_key` — UNIQUE (`new_line_sequence_number`)
- `line_sequence_mapping_old_line_sequence_number_key` — UNIQUE (`old_line_sequence_number`)

---

### `login_history`

**Status:** ✅ ~3,808,951 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `ip_address` | `inet` | yes |  | Address field |
| `client_id` | `int4` | yes |  | Foreign key → `customers.customers_id` |
| `session_id` | `bpchar` | yes |  | Identifier linking to related record |
| `date_entered` | `timestamp` | yes |  |  |
| `user_agent` | `text` | yes |  |  |
| `contact_id` | `int4` | yes |  | Foreign key → `contact.contact_id` |

**Indexes:**
- `login_history_pkey` — UNIQUE (`id`)

---

### `message_box`

**Status:** ✅ ~1,695,041 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `message_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `message` | `varchar` | yes |  |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |

**Indexes:**
- `message_box_pkey` — UNIQUE (`message_id`)
- `message_box_created_idx` — (`created`)

---

### `mon_runbook_custom_notes`

**Status:** ✅ ~169 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `check_type` | `varchar(128)` | yes |  | Type or category classifier |
| `note_type` | `int4` | yes |  | Type or category classifier |
| `notes` | `varchar(1024)` | yes |  |  |

**Indexes:**
- `mon_runbook_custom_notes_pkey` — UNIQUE (`id`)

---

### `mon_runbook_default_notes`

**Status:** ✅ ~61 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `check_type` | `varchar(128)` | yes |  | Type or category classifier |
| `notes` | `varchar(1024)` | yes |  |  |

**Indexes:**
- `mon_runbook_default_notes_pkey` — UNIQUE (`id`)

---

### `my_rbac_pages`

**Status:** ✅ ~263 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `file_name` | `varchar(128)` | no | NOT NULL | Human-readable name |
| `hidden` | `int4` | no | NOT NULL |  |
| `edit_only` | `int4` | no | NOT NULL |  |
| `unrestricted` | `int4` | no | NOT NULL |  |

**Indexes:**
- `my_rbac_pages_pkey` — UNIQUE (`id`)
- `my_rbac_pages_file_name_key` — UNIQUE (`file_name`)

---

### `my_rbac_sections`

**Status:** ✅ ~15 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `section_name` | `varchar(48)` | no | NOT NULL | Human-readable name |

**Indexes:**
- `my_rbac_sections_pkey` — UNIQUE (`id`)
- `my_rbac_sections_section_name_key` — UNIQUE (`section_name`)

---

### `node_types`

**Status:** ✅ ~2 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | no | PK · NOT NULL | Primary key |
| `description` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `node_types_pkey` — UNIQUE (`id`)

---

### `ocean_config`

**Status:** ✅ ~2 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `key` | `varchar(64)` | no | NOT NULL |  |
| `value` | `text` | no | NOT NULL |  |
| `lastchange` | `timestamp` | no | NOT NULL |  |
| `changedby` | `varchar(64)` | no | NOT NULL |  |

**Indexes:**
- `ocean_config_pkey` — UNIQUE (`id`)
- `ocean_config_key_key` — UNIQUE (`key`)

---

### `ocean_restrictions`

**Status:** ✅ ~269 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `resource` | `varchar(128)` | yes |  |  |
| `group_name` | `varchar` | yes |  | Human-readable name |
| `modified_by` | `int4` | yes |  | Timestamp |

**Indexes:**
- `ocean_restrictions_pkey` — UNIQUE (`id`)

---

### `ocean_sessions`

**Status:** ✅ ~7,246 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `session_id` | `bpchar` | no | PK · NOT NULL | Primary key |
| `username` | `varchar(32)` | yes |  |  |
| `active` | `bool` | yes |  | Boolean state flag |
| `last_active` | `timestamptz` | yes |  | Boolean state flag |
| `login_time` | `timestamptz` | yes |  |  |
| `ip_address` | `inet` | no | NOT NULL | Address field |
| `user_agent` | `text` | no | NOT NULL |  |

**Indexes:**
- `ocean_sessions_pkey` — UNIQUE (`session_id`)

---

### `options_licenses`

**Status:** ✅ ~5,917 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `lkg_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `options_id` | `int4` | yes |  | Foreign key → `service_options.id` |
| `license_type_id` | `int4` | no | NOT NULL | Foreign key → `license_types.id` |

**Indexes:**
- `options_licenses_pkey` — UNIQUE (`id`)
- `options_licenses_options_id_key` — UNIQUE (`options_id`, `lkg_id`)

---

### `order_commission_split`

**Status:** ✅ ~69,202 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `order_id` | `int4` | no | NOT NULL | Foreign key → `client_orders.id` |
| `employee_id` | `int4` | no | NOT NULL | Foreign key → `employees.id` |
| `percentage` | `numeric` | no | NOT NULL |  |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `order_commission_split_pkey` — UNIQUE (`id`)
- `order_commission_split_employee_id_idx` — (`employee_id`)
- `order_commission_split_order_id_idx` — (`order_id`)
- `order_commission_split_unique` — UNIQUE (`order_id`, `employee_id`)

---

### `order_communications`

**Status:** ✅ ~40,626 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `order_id` | `int4` | yes |  | Foreign key → `client_orders.id` |
| `order_status_id` | `int4` | yes |  | Foreign key → `client_order_statuses.id` |
| `date_sent` | `timestamp` | no | NOT NULL |  |
| `sent_to` | `varchar(128)` | no | NOT NULL |  |

**Indexes:**
- `order_communications_pkey` — UNIQUE (`id`)
- `order_communications_order_id_idx` — (`order_id`)

---

### `order_entry_solution_link`

**Status:** ✅ ~12,572 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `child_node` | `int4` | yes |  | Foreign key → `order_entry_solution_node.id` |
| `parent_node` | `int4` | yes |  | Foreign key → `order_entry_solution_node.id` |

**Indexes:**
- `order_entry_solution_link_pkey` — UNIQUE (`id`)

---

### `order_entry_solution_node`

**Status:** ✅ ~11,333 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `service_id` | `int4` | yes |  | Foreign key → `customer_products.id` |

**Indexes:**
- `order_entry_solution_node_pkey` — UNIQUE (`id`)

---

### `order_line_item_attributes`

**Status:** ✅ ~98,941 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `line_item_id` | `int4` | no | NOT NULL | Foreign key → `order_line_items.id` |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `value` | `text` | no | NOT NULL |  |

**Indexes:**
- `order_line_item_attributes_pkey` — UNIQUE (`id`)
- `order_line_attributes_line_item_idx` — (`line_item_id`)
- `order_line_item_attributes_line_item_id_name_idx` — (`line_item_id`, `name`)

---

### `order_line_item_detail_attributes`

**Status:** ✅ ~449,045 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `line_item_id` | `int4` | no | NOT NULL | Foreign key → `order_line_item_details.order_line_item_id` |
| `detail_id` | `int4` | no | NOT NULL | Foreign key → `order_line_item_details.id` |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `value` | `text` | no | NOT NULL |  |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `order_line_item_detail_attributes_id` | `serial` | no | auto · NOT NULL | Identifier linking to related record |

**Indexes:**
- `order_line_item_detail_attributes_pkey` — UNIQUE (`id`)
- `order_line_item_detail_attributes_detail_idx` — (`line_item_id`, `detail_id`)
- `order_line_item_detail_attributes_line_item_id_key` — UNIQUE (`line_item_id`, `detail_id`, `name`)

---

### `order_line_item_detail_workorder_tickets`

**Status:** ✅ ~11,366 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `order_line_item_detail_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `workorder_id` | `int4` | yes |  | Identifier linking to related record |
| `ticket_id` | `int4` | yes |  | Identifier linking to related record |

**Indexes:**
- `order_line_item_detail_workorder_tickets_pkey` — UNIQUE (`id`)
- `order_line_item_detail_workorder__order_line_item_detail_id_key` — UNIQUE (`order_line_item_detail_id`)

---

### `order_line_item_details`

**Status:** ✅ ~5,390,359 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `order_line_item_id` | `int4` | no | PK · NOT NULL | Primary key |
| `component_id` | `int4` | yes |  | Foreign key → `components.id` |
| `action` | `bpchar` | no | NOT NULL |  |
| `setup_fee` | `numeric` | no | NOT NULL |  |
| `nrc` | `numeric` | no | NOT NULL |  |
| `mrc` | `numeric` | no | NOT NULL |  |
| `component_name` | `varchar(128)` | no | NOT NULL | Human-readable name |
| `default_setup_fee` | `numeric` | no | NOT NULL |  |
| `default_nrc` | `numeric` | no | NOT NULL |  |
| `default_mrc` | `numeric` | no | NOT NULL |  |
| `service_option_type` | `varchar(64)` | no | NOT NULL | Type or category classifier |
| `promotion_id` | `int4` | yes |  | Foreign key → `promotions.id` |
| `service_option_id` | `int4` | yes |  | Foreign key → `service_options.id` |
| `currency` | `varchar(3)` | no | NOT NULL | Foreign key → `currencies.code` |
| `setup_fee_discount` | `numeric` | yes |  |  |
| `mrc_discount` | `numeric` | yes |  |  |
| `nrc_discount` | `numeric` | yes |  |  |
| `exchange_rate` | `numeric` | no | NOT NULL |  |
| `quantity` | `int4` | no | NOT NULL |  |
| `rate` | `numeric` | yes |  |  |

**Indexes:**
- `order_line_item_details_pkey` — UNIQUE (`id`, `order_line_item_id`)
- `index_component_name` — (`component_name`)
- `index_order_line_item_id_component_name` — (`order_line_item_id`, `component_name`)

---

### `order_line_item_types`

**Status:** ✅ ~4 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `order_line_item_types_pkey` — UNIQUE (`id`)
- `order_line_item_types_name_key` — UNIQUE (`name`)

---

### `order_line_item_workorder_tickets`

**Status:** ✅ ~4,734 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `order_line_item_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `workorder_id` | `int4` | yes |  | Identifier linking to related record |
| `ticket_id` | `int4` | yes |  | Identifier linking to related record |

**Indexes:**
- `order_line_item_workorder_tickets_pkey` — UNIQUE (`id`)
- `order_line_item_workorder_tickets_order_line_item_id_key` — UNIQUE (`order_line_item_id`)

---

### `order_line_items`

**Status:** ✅ ~375,211 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `order_id` | `int4` | yes |  | Foreign key → `client_orders.id` |
| `order_line_item_type_id` | `int4` | yes |  | Foreign key → `order_line_item_types.id` |
| `contract_id` | `varchar(32)` | yes |  | Identifier linking to related record |
| `purchase_order` | `varchar(32)` | yes |  |  |
| `tls_id` | `int4` | yes |  | Foreign key → `product_catalog.id` |
| `location_id` | `int4` | yes |  | Foreign key → `sb_datacenter.id` |
| `payment_type` | `int4` | yes |  | Foreign key → `payment_types.id` |
| `payment_method_id` | `int4` | yes |  | Foreign key → `client_payment_methods.id` |
| `nickname` | `varchar(64)` | no | NOT NULL |  |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `contract_length` | `int4` | yes |  | Foreign key → `contract_lengths.contract_length` |
| `billing_day` | `int4` | yes |  |  |
| `billing_cycle` | `int4` | yes |  |  |
| `setup_fee` | `numeric` | no | NOT NULL |  |
| `mrc` | `numeric` | no | NOT NULL |  |
| `notes` | `text` | yes |  |  |
| `product_name` | `varchar(128)` | no | NOT NULL | Human-readable name |
| `default_setup_fee` | `numeric` | no | NOT NULL |  |
| `default_mrc` | `numeric` | no | NOT NULL |  |
| `tls` | `varchar(64)` | no | NOT NULL |  |
| `provision_date` | `timestamp` | yes |  | Date value |
| `provision_required` | `bool` | no | NOT NULL |  |
| `old_line_item_id` | `int4` | yes |  | Foreign key → `order_line_items.id` |
| `status` | `varchar` | yes |  |  |
| `message` | `varchar` | yes |  |  |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `promotion_id` | `int4` | yes |  | Foreign key → `promotions.id` |
| `product_line_id` | `int4` | yes |  | Foreign key → `product_lines.id` |
| `currency` | `varchar(3)` | no | NOT NULL | Foreign key → `currencies.code` |
| `setup_fee_discount` | `numeric` | yes |  |  |
| `mrc_discount` | `numeric` | yes |  |  |
| `exchange_rate` | `numeric` | no | NOT NULL |  |
| `is_virtual` | `bool` | no | NOT NULL |  |
| `hide_in_portal` | `bool` | no | NOT NULL |  |
| `rate` | `numeric` | yes |  |  |
| `default_rate` | `numeric` | yes |  |  |

**Indexes:**
- `order_line_items_pkey` — UNIQUE (`id`)
- `index_order_id` — (`order_id`)
- `index_service_id` — (`service_id`)

---

### `order_notes`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `order_id` | `int4` | no | NOT NULL | Foreign key → `client_orders.id` |
| `message` | `text` | no | NOT NULL |  |
| `date` | `timestamptz` | no | NOT NULL |  |
| `who` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `order_notes_pkey` — UNIQUE (`id`)

---

### `p1_zones`

**Status:** ✅ ~395 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `zone` | `text` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `p1_zones_pkey` — UNIQUE (`zone`)
- `p1_zones_zone_key` — UNIQUE (`zone`)

---

### `package`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `service_option_id` | `int4` | yes |  | Identifier linking to related record |
| `description` | `text` | no | NOT NULL |  |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `username` | `varchar(64)` | no | NOT NULL |  |
| `password` | `varchar(64)` | no | NOT NULL |  |
| `service_id` | `int4` | yes |  | Identifier linking to related record |

**Indexes:**
- `package_pkey` — UNIQUE (`id`)

---

### `partition_details`

**Status:** ✅ ~55,051 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `partitions_id` | `int4` | no | NOT NULL | Foreign key → `partitions.id` |
| `mount_point` | `varchar(256)` | no | NOT NULL |  |
| `fstype` | `varchar(256)` | no | NOT NULL |  |
| `size` | `varchar(256)` | no | NOT NULL |  |
| `label` | `varchar(256)` | no | NOT NULL |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `is_data_partition` | `bool` | yes |  |  |
| `maxsize` | `varchar(256)` | yes |  |  |
| `partition_type` | `varchar(256)` | no | NOT NULL | Type or category classifier |
| `grow` | `bool` | no | NOT NULL |  |

**Indexes:**
- `partition_details_pkey` — UNIQUE (`id`)

---

### `partition_object_types`

**Status:** ✅ ~2 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `value` | `varchar(16)` | no | NOT NULL |  |

**Indexes:**
- `partition_object_types_pkey` — UNIQUE (`id`)

---

### `partitions`

**Status:** ✅ ~18,146 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `object_type_id` | `int4` | no | NOT NULL | Foreign key → `partition_object_types.id` |
| `object_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `device_id` | `int4` | yes |  | Identifier linking to related record |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `partitions_pkey` — UNIQUE (`id`)

---

### `permission_categories`

**Status:** ✅ ~4 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `permission_categories_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `sort_order` | `int4` | yes |  |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `permission_categories_pkey` — UNIQUE (`permission_categories_id`)

---

### `permissions`

**Status:** ✅ ~58 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `permissions_id` | `varchar(32)` | no | PK · NOT NULL | Primary key |
| `permission_categories_id` | `int4` | no | NOT NULL | Foreign key → `permission_categories.permission_categories_id` |
| `permission_title` | `varchar(128)` | no | NOT NULL |  |
| `full_description` | `varchar` | no | NOT NULL |  |
| `sort_order` | `int4` | yes |  |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `permissions_pkey` — UNIQUE (`permissions_id`)

---

### `portal_login`

**Status:** ✅ ~204,312 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `hash` | `varchar(1024)` | no | PK · NOT NULL | Primary key |
| `client_id` | `int4` | no | NOT NULL | Foreign key → `customers.customers_id` |
| `username` | `varchar(64)` | no | NOT NULL | Foreign key → `employees.username` |
| `expiration` | `timestamptz` | no | NOT NULL |  |
| `contact_id` | `int4` | yes |  | Foreign key → `contact.contact_id` |

**Indexes:**
- `portal_login_pkey` — UNIQUE (`hash`)

---

### `preconfigured_bundle_categories`

**Status:** ✅ ~6 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(256)` | no | NOT NULL |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `preconfigured_bundle_categories_pkey` — UNIQUE (`id`)
- `preconfigured_bundle_categories_name_key` — UNIQUE (`name`)

---

### `preconfigured_bundle_mapping`

**Status:** ✅ ~216 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `preconfigured_bundle_categories_id` | `int4` | no | NOT NULL | Foreign key → `preconfigured_bundle_categories.id` |
| `datacenter_id` | `int4` | no | NOT NULL | Foreign key → `sb_datacenter.id` |
| `operating_system` | `varchar` | no | NOT NULL |  |
| `rating` | `int4` | no | NOT NULL |  |
| `product_id` | `int4` | no | NOT NULL | Foreign key → `product_catalog.id` |
| `product_configuration_id` | `int4` | yes |  | Foreign key → `product_configurations.id` |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `preconfigured_bundle_mapping_pkey` — UNIQUE (`id`)
- `preconfigured_bundle_mapping_preconfigured_bundle_categorie_key` — UNIQUE (`preconfigured_bundle_categories_id`, `datacenter_id`, `operating_system`, `rating`)

---

### `pricebook`

**Status:** ✅ ~43,198 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `product_catalog_id` | `int4` | yes |  | Foreign key → `product_catalog.id` |
| `component_id` | `int4` | yes |  | Foreign key → `components.id` |
| `nrc` | `numeric` | yes |  |  |
| `mrc` | `numeric` | yes |  |  |
| `modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `setup` | `numeric` | no | NOT NULL |  |
| `currency` | `varchar(3)` | no | NOT NULL | Foreign key → `currencies.code` |
| `product_line_id` | `int4` | no | NOT NULL | Foreign key → `product_lines.id` |
| `datacenter` | `int4` | no | NOT NULL | Foreign key → `sb_datacenter.id` |
| `rate` | `numeric` | yes |  |  |
| `is_available` | `bool` | yes |  |  |

**Indexes:**
- `pricebook_pk` — UNIQUE (`id`)
- `pricebook_component_id_idx` — (`component_id`)
- `pricebook_product_catalog_id_idx` — (`product_catalog_id`)

---

### `promotion_contract_length_criteria`

**Status:** ✅ ~2 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `promo_id` | `int4` | no | NOT NULL | Foreign key → `promotions.id` |
| `contract_length` | `int4` | no | NOT NULL | Foreign key → `contract_lengths.contract_length` |
| `minimum_quantity` | `int4` | no | NOT NULL |  |
| `depth` | `int4` | no | NOT NULL |  |
| `operator` | `varchar(3)` | no | NOT NULL | Foreign key → `resource_use_operators.operator` |
| `scope` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `promotion_contract_length_criteria_pkey` — UNIQUE (`id`)
- `promotion_contract_length_criteria_promo_id_key` — UNIQUE (`promo_id`, `contract_length`)

---

### `promotion_criteria_types`

**Status:** ✅ ~7 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `source` | `varchar(64)` | yes |  |  |

**Indexes:**
- `promotion_criteria_types_pkey` — UNIQUE (`id`)

---

### `promotion_customer_type_criteria`

**Status:** ✅ ~10 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `promo_id` | `int4` | no | NOT NULL | Foreign key → `promotions.id` |
| `customer_type_id` | `int4` | no | NOT NULL | Foreign key → `client_types_pl.client_type_id` |
| `minimum_quantity` | `int4` | no | NOT NULL |  |
| `depth` | `int4` | no | NOT NULL |  |
| `operator` | `varchar(3)` | no | NOT NULL | Foreign key → `resource_use_operators.operator` |
| `scope` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `promotion_customer_type_criteria_pkey` — UNIQUE (`id`)
- `promotion_customer_type_criteria_promo_id_key` — UNIQUE (`promo_id`, `customer_type_id`)

---

### `promotion_effect_amounts`

**Status:** ✅ ~2,094 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `effect_id` | `int4` | no | NOT NULL | Foreign key → `promotion_effects.id` |
| `currency_code` | `varchar(3)` | no | NOT NULL | Foreign key → `currencies.code` |
| `amount` | `float8` | no | NOT NULL |  |
| `amount_type_id` | `int4` | no | NOT NULL | Foreign key → `promotion_effect_target_amount_types.id` |

**Indexes:**
- `promotion_effect_amounts_pkey` — UNIQUE (`id`)
- `promotion_effect_amounts_effect_id_key` — UNIQUE (`effect_id`, `currency_code`)

---

### `promotion_effect_target_amount_types`

**Status:** ✅ ~3 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `promotion_effect_target_amount_types_pkey` — UNIQUE (`id`)

---

### `promotion_effect_target_types`

**Status:** ✅ ~3 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `promotion_effect_target_types_pkey` — UNIQUE (`id`)

---

### `promotion_effect_types`

**Status:** ✅ ~4 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `promotion_effect_types_pkey` — UNIQUE (`id`)

---

### `promotion_effects`

**Status:** ✅ ~1,411 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `promo_id` | `int4` | no | NOT NULL | Foreign key → `promotions.id` |
| `effect_type_id` | `int4` | no | NOT NULL | Foreign key → `promotion_effect_types.id` |
| `target_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `target_type_id` | `int4` | no | NOT NULL | Foreign key → `promotion_effect_target_types.id` |
| `target_max_quantity` | `int4` | no | NOT NULL |  |

**Indexes:**
- `promotion_effects_pkey` — UNIQUE (`id`)

---

### `promotion_location_criteria`

**Status:** ✅ ~42 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `promo_id` | `int4` | no | NOT NULL | Foreign key → `promotions.id` |
| `location_id` | `int4` | no | NOT NULL | Foreign key → `sb_datacenter.id` |
| `minimum_quantity` | `int4` | no | NOT NULL |  |
| `depth` | `int4` | no | NOT NULL |  |
| `operator` | `varchar(3)` | no | NOT NULL | Foreign key → `resource_use_operators.operator` |
| `scope` | `varchar(32)` | no | NOT NULL |  |

**Indexes:**
- `promotion_location_criteria_pkey` — UNIQUE (`id`)
- `promotion_location_criteria_promo_id_key` — UNIQUE (`promo_id`, `location_id`)

---

### `promotion_types`

**Status:** ✅ ~2 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(32)` | no | NOT NULL |  |
| `description` | `varchar(255)` | yes |  |  |

**Indexes:**
- `promotion_types_pkey` — UNIQUE (`id`)

---

### `promotions`

**Status:** ✅ ~155 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `promo_code` | `varchar(32)` | no | NOT NULL | Short code or identifier |
| `description` | `varchar` | no | NOT NULL |  |
| `start_date` | `date` | no | NOT NULL | Date value |
| `end_date` | `date` | no | NOT NULL | Date value |
| `promo_type_id` | `int4` | no | NOT NULL | Foreign key → `promotion_types.id` |
| `available_in_shop` | `bool` | no | NOT NULL |  |
| `available_in_oes` | `bool` | no | NOT NULL |  |
| `has_gift_item` | `bool` | no | NOT NULL |  |
| `gift_item_description` | `varchar(255)` | yes |  |  |

**Indexes:**
- `promotions_pkey` — UNIQUE (`id`)

---

### `provisioning_tickets`

**Status:** ✅ ~5,216 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `order_id` | `int4` | no | NOT NULL | Foreign key → `client_orders.id` |
| `service_id` | `int4` | no | NOT NULL | Foreign key → `customer_products.id` |
| `ticket_id` | `int4` | no | PK · NOT NULL | Primary key |
| `color` | `ticket_colors` | no | NOT NULL |  |

**Indexes:**
- `provisioning_tickets_pkey` — UNIQUE (`ticket_id`)
- `order_service_color` — UNIQUE (`order_id`, `service_id`, `color`)

---

### `queue_messages`

**Status:** ✅ ~1,792,446 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `queue_id` | `int4` | no | PK · NOT NULL | Primary key |
| `message_id` | `int4` | no | PK · NOT NULL | Primary key |
| `consumed` | `timestamptz` | yes |  |  |
| `locked` | `timestamptz` | no | NOT NULL |  |
| `token` | `varchar` | yes |  |  |

**Indexes:**
- `queue_messages_pkey` — UNIQUE (`queue_id`, `message_id`)
- `queue_lock_idx2` — (`queue_id`, `locked`)
- `queue_messages_consumed_idx` — (`consumed`)

---

### `queues`

**Status:** ✅ ~68 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `queue_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `queue_name` | `varchar` | yes |  | Human-readable name |
| `description` | `varchar` | yes |  |  |

**Indexes:**
- `queues_pkey` — UNIQUE (`queue_id`)
- `queues_queue_name_key` — UNIQUE (`queue_name`)

---

### `raid_levels`

**Status:** ✅ ~11 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `level` | `varchar(4)` | no | NOT NULL |  |
| `name` | `varchar(32)` | no | NOT NULL |  |
| `description` | `text` | no | NOT NULL |  |
| `min_drives` | `int4` | no | NOT NULL |  |
| `allow_hotspare` | `bool` | no | NOT NULL |  |

**Indexes:**
- `raid_levels_pkey` — UNIQUE (`id`)
- `raid_levels_level_key` — UNIQUE (`level`)
- `raid_levels_name_key` — UNIQUE (`name`)

---

### `resource_use_operators`

**Status:** ✅ ~6 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `operator` | `varchar(3)` | no | PK · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `description` | `varchar(256)` | yes |  |  |

**Indexes:**
- `resource_use_operators_pkey` — UNIQUE (`operator`)

---

### `resource_use_types`

**Status:** ✅ ~2 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(32)` | yes |  |  |
| `description` | `varchar(512)` | yes |  |  |

**Indexes:**
- `resource_use_types_pkey` — UNIQUE (`id`)
- `resource_use_types_name_key` — UNIQUE (`name`)

---

### `resources`

**Status:** ✅ ~35 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(32)` | yes |  |  |
| `uom` | `int4` | yes |  | Foreign key → `unit_of_measure.id` |
| `description` | `varchar(512)` | yes |  |  |

**Indexes:**
- `resources_pkey` — UNIQUE (`id`)
- `resources_name_key` — UNIQUE (`name`)

---

### `rss_feed_spotlight`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `alt_text` | `text` | yes |  |  |
| `img_link` | `varchar(128)` | yes |  |  |
| `img_data` | `bytea` | yes |  |  |

**Indexes:**
- `rss_feed_spotlight_pkey` — UNIQUE (`id`)

---

### `rss_feeds`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `body` | `text` | no | NOT NULL |  |
| `link` | `varchar(128)` | yes |  |  |
| `image` | `int4` | yes |  | Foreign key → `rss_feed_spotlight.id` |
| `category` | `varchar(64)` | yes |  |  |
| `published_date` | `timestamptz` | yes |  | Date value |

**Indexes:**
- `rss_feeds_pkey` — UNIQUE (`id`)

---

### `sb_customer_log`

**Status:** ✅ ~6,316,303 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `customers_id` | `int4` | yes |  | Foreign key → `customers.customers_id` |
| `log_type_id` | `int4` | yes |  | Foreign key → `sb_log_type.id` |
| `message` | `text` | yes |  |  |
| `logged_by` | `text` | yes |  |  |
| `logged_on` | `timestamptz` | yes |  |  |
| `ticket_id` | `int4` | yes |  | Identifier linking to related record |

**Indexes:**
- `sb_customer_log_pkey` — UNIQUE (`id`)
- `sb_customer_log_customers_id_idx` — (`customers_id`)

---

### `sb_log_type`

**Status:** ✅ ~16 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `text` | yes |  |  |

**Indexes:**
- `sb_log_type_pkey` — UNIQUE (`id`)
- `log_type_id_log_type` — (`id`)

---

### `secret_questions_pl`

**Status:** ✅ ~5 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `question` | `text` | no | NOT NULL |  |

**Indexes:**
- `secret_questions_pl_pkey` — UNIQUE (`id`)

---

### `sessions`

**Status:** ✅ ~3,156 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `session_id` | `bpchar` | no | PK · NOT NULL | Primary key |
| `client_id` | `int4` | yes |  | Foreign key → `customers.customers_id` |
| `active` | `bool` | yes |  | Boolean state flag |
| `last_login` | `timestamp` | yes |  |  |
| `contact_id` | `int4` | yes |  | Foreign key → `contact.contact_id` |

**Indexes:**
- `sessions_pkey` — UNIQUE (`session_id`)

---

### `solution_connection_property_types`

**Status:** ✅ ~3 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `connection_property_name` | `varchar(32)` | no | PK · NOT NULL | Primary key |
| `description` | `varchar` | yes |  |  |

**Indexes:**
- `solution_connection_property_types_pkey` — UNIQUE (`connection_property_name`)

---

### `task_status_pl`

**Status:** ✅ ~6 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `status_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `description` | `varchar(255)` | no | NOT NULL |  |
| `sort_order` | `int4` | no | NOT NULL |  |
| `is_active` | `bool` | no | NOT NULL | Boolean state flag |

**Indexes:**
- `task_status_pl_pk` — UNIQUE (`status_id`)

---

### `tax_registration_types`

**Status:** ✅ ~3 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `tax_registration_type_id` | `varchar(16)` | no | PK · NOT NULL | Primary key |
| `name` | `varchar` | no | NOT NULL |  |
| `certificate_required` | `bool` | no | NOT NULL |  |
| `bitmask` | `varbit` | no | NOT NULL |  |
| `fieldname_remote` | `varchar` | yes |  |  |

**Indexes:**
- `tax_registration_types_pkey` — UNIQUE (`tax_registration_type_id`)

---

### `ticket_support_time_types`

**Status:** ✅ ~4 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(100)` | yes |  |  |
| `rate` | `float8` | yes |  |  |
| `gp_item_id` | `varchar(32)` | yes |  | Identifier linking to related record |
| `billable` | `bool` | yes |  |  |

**Indexes:**
- `ticket_support_time_types_pkey` — UNIQUE (`id`)

---

### `ticket_support_times`

**Status:** ✅ ~2,038,533 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `ticket_id` | `int4` | yes |  | Identifier linking to related record |
| `client_id` | `int4` | no | NOT NULL | Foreign key → `customers.customers_id` |
| `service_id` | `int4` | yes |  | Foreign key → `customer_products.id` |
| `username` | `text` | yes |  |  |
| `type_id` | `int4` | yes |  | Foreign key → `ticket_support_time_types.id` |
| `minutes_worked` | `int4` | yes |  |  |
| `created_on` | `timestamptz` | yes |  | Timestamp |
| `executed_on` | `timestamptz` | yes |  |  |

**Indexes:**
- `ticket_support_times_pkey` — UNIQUE (`id`)

---

### `tls_workorder_templates`

**Status:** ✅ ~22 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `product_id` | `int4` | no | NOT NULL | Foreign key → `product_catalog.id` |
| `workorder_template` | `text` | yes |  |  |

**Indexes:**
- `tls_workorder_templates_pkey` — UNIQUE (`id`)

---

### `transactions_pending_client_approval`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `created` | `timestamptz` | yes |  | Timestamp |
| `token` | `varchar(128)` | yes |  |  |
| `payment_gateway_name` | `varchar(32)` | yes |  | Human-readable name |
| `transaction` | `text` | yes |  |  |

**Indexes:**
- `transactions_pending_client_approval_pkey` — UNIQUE (`id`)

---

### `unit_of_measure`

**Status:** ✅ ~30 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(32)` | no | NOT NULL |  |
| `abbr` | `varchar(10)` | no | NOT NULL |  |
| `base_unit_id` | `int4` | yes |  | Foreign key → `unit_of_measure.id` |
| `conversion_factor` | `numeric` | yes |  |  |

**Indexes:**
- `unit_of_measure_pk` — UNIQUE (`id`)
- `unit_of_measure_abbr_key` — UNIQUE (`abbr`)
- `unit_of_measure_name_key` — UNIQUE (`name`)

---

### `vam_admin_account`

**Status:** ✅ ~973 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `sspc_url` | `varchar(255)` | yes |  |  |
| `initial_address_url` | `varchar(255)` | yes |  | Address field |
| `login` | `varchar(80)` | yes |  |  |
| `password` | `varchar(80)` | yes |  |  |

**Indexes:**
- `vam_admin_account_ukey` — UNIQUE (`client_id`)

---

### `vam_agent`

**Status:** ✅ ~2,786 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `sspc_url` | `varchar(255)` | yes |  |  |
| `resource_name` | `varchar(80)` | yes |  | Human-readable name |

**Indexes:**
- `vam_agent_ukey` — UNIQUE (`service_id`)

---

### `vam_agent_account`

**Status:** ✅ ~2,896 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `sspc_url` | `varchar(255)` | yes |  |  |
| `login` | `varchar(80)` | yes |  |  |
| `password` | `varchar(80)` | yes |  |  |

**Indexes:**
- `vam_agent_account_ukey` — UNIQUE (`service_id`)

---

### `vam_cache`

**Status:** ✅ ~11,623 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `href` | `varchar(255)` | yes |  |  |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `content` | `text` | yes |  |  |
| `type` | `varchar(80)` | yes |  |  |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `vam_cache_pkey` — UNIQUE (`id`)

---

### `vam_client`

**Status:** ✅ ~979 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `sspc_url` | `varchar(255)` | yes |  |  |
| `creation_phase` | `int4` | no | NOT NULL |  |
| `resource_name` | `varchar(80)` | yes |  | Human-readable name |

**Indexes:**
- `vam_client_ukey` — UNIQUE (`client_id`)

---

### `vam_configuration`

**Status:** ✅ ~2,786 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `sspc_url` | `varchar(255)` | yes |  |  |
| `resource_name` | `varchar(80)` | yes |  | Human-readable name |

**Indexes:**
- `vam_configuration_ukey` — UNIQUE (`service_id`)

---

### `vam_escalation_definition`

**Status:** ✅ ~2,785 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `sspc_url` | `varchar(255)` | yes |  |  |
| `resource_name` | `varchar(80)` | yes |  | Human-readable name |

**Indexes:**
- `vam_escalation_definition_ukey` — UNIQUE (`service_id`)

---

### `vam_resources`

**Status:** ✅ ~12 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `resource` | `varchar(80)` | yes |  |  |
| `parent_resource` | `varchar(80)` | yes |  |  |
| `resource_property` | `varchar(80)` | yes |  |  |
| `list_container` | `varchar(80)` | yes |  |  |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `vam_resources_pkey` — UNIQUE (`id`)

---

### `vmware_clusters`

**Status:** ✅ ~418 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `service_id` | `int4` | yes |  | Foreign key → `customer_products.id` |
| `parent_service_id` | `int4` | yes |  | Foreign key → `customer_products.id` |

**Indexes:**
- `vmware_clusters_pkey` — UNIQUE (`id`)

---

### `vmware_guests`

**Status:** ✅ ~4,374 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `service_id` | `int4` | yes |  | Foreign key → `customer_products.id` |
| `parent_service_id` | `int4` | yes |  | Foreign key → `customer_products.id` |

**Indexes:**
- `vmware_guests_pkey` — UNIQUE (`id`)

---

### `vmware_vcenters`

**Status:** ✅ ~497 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `service_id` | `int4` | yes |  | Foreign key → `customer_products.id` |

**Indexes:**
- `vmware_vcenters_pkey` — UNIQUE (`id`)

---

### `volume_discount_percentage`

**Status:** ✅ ~20 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `threshold` | `int4` | no | NOT NULL |  |
| `discount` | `numeric` | no | NOT NULL |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `volume_discount_percentage_pkey` — UNIQUE (`id`)
- `volume_discount_percentage_server_num_key` — UNIQUE (`threshold`)

---

### `wallet_responses_pl`

**Status:** ✅ ~20 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `code` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `response` | `varchar` | yes |  |  |

**Indexes:**
- `wallet_resposnes_pkey` — UNIQUE (`code`)

---

### `widget_input_parameters`

**Status:** ✅ ~321 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `widget_id` | `int4` | no | PK · NOT NULL | Primary key |
| `parameter_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `parameter_name` | `varchar(64)` | no | NOT NULL | Human-readable name |
| `parameter_description` | `varchar(255)` | no | NOT NULL |  |
| `data_type_id` | `int4` | no | NOT NULL | Identifier linking to related record |

**Indexes:**
- `widget_input_parameters_pk` — UNIQUE (`widget_id`, `parameter_id`)

---

### `widget_output_parameters`

**Status:** ✅ ~357 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `widget_id` | `int4` | no | PK · NOT NULL | Primary key |
| `parameter_id` | `int4` | no | PK · NOT NULL | Primary key |
| `parameter_name` | `varchar(64)` | no | NOT NULL | Human-readable name |
| `parameter_description` | `varchar(255)` | no | NOT NULL |  |
| `data_type_id` | `int4` | no | NOT NULL | Identifier linking to related record |

**Indexes:**
- `widget_output_parameters_pk` — UNIQUE (`widget_id`, `parameter_id`)

---

### `widget_transaction_states`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `state` | `varchar` | yes |  |  |
| `name` | `varchar` | yes |  |  |

**Indexes:**
- `widget_transaction_states_pkey` — UNIQUE (`id`)

---

### `widget_types_pl`

**Status:** ✅ ~42 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `widget_type_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `description` | `varchar(255)` | no | NOT NULL |  |
| `sort_order` | `int4` | no | NOT NULL |  |
| `is_active` | `bool` | no | NOT NULL | Boolean state flag |

**Indexes:**
- `widget_types_pl_pk` — UNIQUE (`widget_type_id`)

---

### `widgets`

**Status:** ✅ ~187 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `widget_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `widget_name` | `varchar(64)` | no | NOT NULL | Human-readable name |
| `widget_description` | `varchar(255)` | no | NOT NULL |  |
| `widget_author` | `varchar(64)` | no | NOT NULL |  |
| `date_created` | `timestamp` | no | NOT NULL | Timestamp |
| `widget_type_id` | `int4` | no | NOT NULL | Foreign key → `widget_types_pl.widget_type_id` |
| `is_active` | `bool` | no | NOT NULL | Boolean state flag |
| `widget_url` | `varchar` | yes |  |  |
| `widget_role` | `varchar(64)` | yes |  |  |
| `hide_role` | `bool` | yes |  |  |

**Indexes:**
- `widgets_pk` — UNIQUE (`widget_id`)
- `widgets_widget_name_key` — UNIQUE (`widget_name`)

---

### `workflow_event_types`

**Status:** ✅ ~16 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `text` | no | NOT NULL |  |
| `tracked` | `bool` | no | NOT NULL |  |
| `allow_duplicates` | `bool` | no | NOT NULL |  |

**Indexes:**
- `workflow_event_types_pkey` — UNIQUE (`id`)
- `workflow_event_types_name_key` — UNIQUE (`name`)

---

### `workflow_notifications`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `service_id` | `int4` | no | NOT NULL | Foreign key → `customer_products.id` |
| `workflow_instance_id` | `int4` | yes |  | Identifier linking to related record |
| `event_type_id` | `int4` | no | NOT NULL | Foreign key → `workflow_event_types.id` |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_updated` | `timestamptz` | no | NOT NULL | Timestamp |
| `status` | `varchar` | no | NOT NULL |  |
| `message` | `varchar` | yes |  |  |

**Indexes:**
- `workflow_notifications_pkey` — UNIQUE (`id`)

---

### `xref_cloud_storage_policy_concession`

**Status:** ✅ ~1 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `type` | `varchar(32)` | no | NOT NULL |  |
| `app_config_id` | `int4` | no | NOT NULL | Foreign key → `app_config.id` |
| `component_id` | `int4` | no | NOT NULL | Foreign key → `components.id` |
| `created` | `timestamp` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamp` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `xref_cloud_storage_policy_concession_pkey` — UNIQUE (`id`)

---

### `xref_customer_support_type_sub_type`

**Status:** ✅ ~435 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `customer_support_type_id` | `int4` | no | NOT NULL | Foreign key → `customer_support_type.id` |
| `customer_support_sub_type_id` | `int4` | no | NOT NULL | Foreign key → `customer_support_sub_type.id` |
| `num_tickets_required` | `int4` | yes |  |  |
| `hours_for_resolution` | `int4` | yes |  |  |
| `support_handler_id` | `int4` | no | NOT NULL | Foreign key → `customer_support_handler.id` |
| `notes` | `text` | yes |  |  |
| `special_form_command` | `text` | yes |  |  |
| `is_customer_facing` | `bool` | yes |  |  |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `xref_customer_support_type_sub_type_pkey` — UNIQUE (`id`)
- `unique_type_sub_type_handler` — UNIQUE (`customer_support_type_id`, `customer_support_sub_type_id`, `support_handler_id`)
- `xref_customer_support_type_sub_type_id_key` — UNIQUE (`id`)

---

### `xref_rbac_pages_to_sections`

**Status:** ✅ ~218 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `page_id` | `int4` | no | NOT NULL | Foreign key → `my_rbac_pages.id` |
| `section_id` | `int4` | no | NOT NULL | Foreign key → `my_rbac_sections.id` |

**Indexes:**
- `xref_rbac_pages_to_sections_pkey` — UNIQUE (`id`)

---

### `zones`

**Status:** ✅ ~736 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `zone_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `zone_country_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `zone_code` | `text` | no | NOT NULL | Short code or identifier |
| `zone_name` | `text` | no | NOT NULL | Human-readable name |

**Indexes:**
- `zones_pkey` — UNIQUE (`zone_id`)
- `unique_zone_idx` — UNIQUE (`zone_code`, `zone_country_id`)

---

## Relationships

| From | | To |
|------|---|-----|
| `item_tax_schedule`.`product_class_id` | → | `product_classes`.`id` |
| `item_tax_schedule`.`component_category` | → | `component_categories`.`id` |
| `item_tax_schedule`.`datacenter` | → | `sb_datacenter`.`id` |
| `item_tax_schedule`.`client_countries_id` | → | `countries`.`countries_id` |
| `item_tax_schedule`.`mrc_tax_id` | → | `tax_rates`.`id` |
| `item_tax_schedule`.`nrc_tax_id` | → | `tax_rates`.`id` |
| `item_tax_schedule`.`setup_tax_id` | → | `tax_rates`.`id` |
| `item_tax_schedule`.`rate_tax_id` | → | `tax_rates`.`id` |
| `login_history`.`client_id` | → | `customers`.`customers_id` |
| `login_history`.`contact_id` | → | `contact`.`contact_id` |
| `options_licenses`.`options_id` | → | `service_options`.`id` |
| `order_commission_split`.`order_id` | → | `client_orders`.`id` |
| `order_commission_split`.`employee_id` | → | `employees`.`id` |
| `order_communications`.`order_id` | → | `client_orders`.`id` |
| `order_communications`.`order_status_id` | → | `client_order_statuses`.`id` |
| `order_entry_solution_node`.`service_id` | → | `customer_products`.`id` |
| `order_line_item_details`.`component_id` | → | `components`.`id` |
| `order_line_item_details`.`service_option_id` | → | `service_options`.`id` |
| `order_line_item_details`.`currency` | → | `currencies`.`code` |
| `order_line_items`.`order_id` | → | `client_orders`.`id` |
| `order_line_items`.`tls_id` | → | `product_catalog`.`id` |
| `order_line_items`.`location_id` | → | `sb_datacenter`.`id` |
| `order_line_items`.`payment_type` | → | `payment_types`.`id` |
| `order_line_items`.`payment_method_id` | → | `client_payment_methods`.`id` |
| `order_line_items`.`contract_length` | → | `contract_lengths`.`contract_length` |
| `order_line_items`.`product_line_id` | → | `product_lines`.`id` |
| `order_line_items`.`currency` | → | `currencies`.`code` |
| `order_notes`.`order_id` | → | `client_orders`.`id` |
| `portal_login`.`client_id` | → | `customers`.`customers_id` |
| `portal_login`.`username` | → | `employees`.`username` |
| `portal_login`.`contact_id` | → | `contact`.`contact_id` |
| `preconfigured_bundle_mapping`.`datacenter_id` | → | `sb_datacenter`.`id` |
| `preconfigured_bundle_mapping`.`product_id` | → | `product_catalog`.`id` |
| `preconfigured_bundle_mapping`.`product_configuration_id` | → | `product_configurations`.`id` |
| `pricebook`.`product_catalog_id` | → | `product_catalog`.`id` |
| `pricebook`.`component_id` | → | `components`.`id` |
| `pricebook`.`currency` | → | `currencies`.`code` |
| `pricebook`.`product_line_id` | → | `product_lines`.`id` |
| `pricebook`.`datacenter` | → | `sb_datacenter`.`id` |
| `promotion_contract_length_criteria`.`contract_length` | → | `contract_lengths`.`contract_length` |
| `promotion_customer_type_criteria`.`customer_type_id` | → | `client_types_pl`.`client_type_id` |
| `promotion_effect_amounts`.`currency_code` | → | `currencies`.`code` |
| `promotion_location_criteria`.`location_id` | → | `sb_datacenter`.`id` |
| `provisioning_tickets`.`order_id` | → | `client_orders`.`id` |
| `provisioning_tickets`.`service_id` | → | `customer_products`.`id` |
| `provisioning_tickets`.`ticket_id` | → | `client_tickets`.`ticket_id` |
| `sb_customer_log`.`customers_id` | → | `customers`.`customers_id` |
| `sessions`.`client_id` | → | `customers`.`customers_id` |
| `sessions`.`contact_id` | → | `contact`.`contact_id` |
| `ticket_support_times`.`client_id` | → | `customers`.`customers_id` |
| `ticket_support_times`.`service_id` | → | `customer_products`.`id` |
| `tls_workorder_templates`.`product_id` | → | `product_catalog`.`id` |
| `vmware_clusters`.`service_id` | → | `customer_products`.`id` |
| `vmware_clusters`.`parent_service_id` | → | `customer_products`.`id` |
| `vmware_guests`.`service_id` | → | `customer_products`.`id` |
| `vmware_guests`.`parent_service_id` | → | `customer_products`.`id` |
| `vmware_vcenters`.`service_id` | → | `customer_products`.`id` |
| `workflow_notifications`.`service_id` | → | `customer_products`.`id` |
| `xref_cloud_storage_policy_concession`.`app_config_id` | → | `app_config`.`id` |
| `xref_cloud_storage_policy_concession`.`component_id` | → | `components`.`id` |
| `xref_customer_support_type_sub_type`.`customer_support_type_id` | → | `customer_support_type`.`id` |
| `xref_customer_support_type_sub_type`.`customer_support_sub_type_id` | → | `customer_support_sub_type`.`id` |
| `xref_customer_support_type_sub_type`.`support_handler_id` | → | `customer_support_handler`.`id` |
| `countries_intergovernmental_organizations`.`igo_id` | → | `intergovernmental_organizations`.`id` |
| `employee_client_relations_roles_matrix`.`igo_id` | → | `intergovernmental_organizations`.`id` |
| `component_license_keys`.`license_type_id` | → | `license_types`.`id` |
| `service_licenses`.`license_type_id` | → | `license_types`.`id` |
| `xref_customer_rbac_roles`.`section_id` | → | `my_rbac_sections`.`id` |
| `certificate`.`options_licenses_id` | → | `options_licenses`.`id` |
| `olid_service_option_link`.`order_line_item_detail_id` | → | `order_line_item_details`.`id` |
| `olid_service_option_link`.`order_line_item_id` | → | `order_line_item_details`.`order_line_item_id` |
| `customer_products`.`customer_order_id` | → | `order_line_items`.`id` |
| `order_line_item_migrated_services`.`order_line_item_id` | → | `order_line_items`.`id` |
| `history_contact`.`zone` | → | `p1_zones`.`zone` |
| `client_permission_roles`.`permissions_id` | → | `permissions`.`permissions_id` |
| `client_permission_users`.`permissions_id` | → | `permissions`.`permissions_id` |
| `history_client_permission_roles`.`permissions_id` | → | `permissions`.`permissions_id` |
| `history_client_permission_users`.`permissions_id` | → | `permissions`.`permissions_id` |
| `history_permissions`.`permissions_id` | → | `permissions`.`permissions_id` |
| `history_template_permission_roles`.`permissions_id` | → | `permissions`.`permissions_id` |
| `template_permission_roles`.`permissions_id` | → | `permissions`.`permissions_id` |
| `promotion_effect_component_criteria`.`effect_id` | → | `promotion_effects`.`id` |
| `promotion_effect_component_type_criteria`.`effect_id` | → | `promotion_effects`.`id` |
| `promotion_effect_product_class_criteria`.`effect_id` | → | `promotion_effects`.`id` |
| `promotion_effect_product_criteria`.`effect_id` | → | `promotion_effects`.`id` |
| `cart`.`promotion_id` | → | `promotions`.`id` |
| `promotion_component_criteria`.`promo_id` | → | `promotions`.`id` |
| `promotion_component_type_criteria`.`promo_id` | → | `promotions`.`id` |
| `promotion_component_types`.`promotion_id` | → | `promotions`.`id` |
| `promotion_product_class_criteria`.`promo_id` | → | `promotions`.`id` |
| `promotion_product_classes`.`promotion_id` | → | `promotions`.`id` |
| `promotion_product_criteria`.`promo_id` | → | `promotions`.`id` |
| `service_billing_details`.`promotion_id` | → | `promotions`.`id` |
| `cart_raid_arrays`.`level` | → | `raid_levels`.`id` |
| `config_code_raid_arrays`.`level` | → | `raid_levels`.`id` |
| `service_option_raid_arrays`.`raid_level_id` | → | `raid_levels`.`id` |
| `component_required_resources`.`operator` | → | `resource_use_operators`.`operator` |
| `promotion_component_criteria`.`operator` | → | `resource_use_operators`.`operator` |
| `promotion_component_type_criteria`.`operator` | → | `resource_use_operators`.`operator` |
| `promotion_effect_component_criteria`.`operator` | → | `resource_use_operators`.`operator` |
| `promotion_effect_component_type_criteria`.`operator` | → | `resource_use_operators`.`operator` |
| `promotion_effect_product_class_criteria`.`operator` | → | `resource_use_operators`.`operator` |
| `promotion_effect_product_criteria`.`operator` | → | `resource_use_operators`.`operator` |
| `promotion_product_class_criteria`.`operator` | → | `resource_use_operators`.`operator` |
| `promotion_product_criteria`.`operator` | → | `resource_use_operators`.`operator` |
| `view_component_required_resources`.`operator` | → | `resource_use_operators`.`operator` |
| `view_promotion_criteria_details`.`operator` | → | `resource_use_operators`.`operator` |
| `view_promotion_effect_criteria_details`.`operator` | → | `resource_use_operators`.`operator` |
| `component_required_resources`.`use_type_id` | → | `resource_use_types`.`id` |
| `component_provided_resources`.`resource_id` | → | `resources`.`id` |
| `component_required_resources`.`resource_id` | → | `resources`.`id` |
| `sb_customer_product_log`.`log_type_id` | → | `sb_log_type`.`id` |
| `cart`.`session_id` | → | `sessions`.`session_id` |
| `solution_service_connection_properties`.`connection_property_name` | → | `solution_connection_property_types`.`connection_property_name` |
| `client_tax_registrations`.`tax_registration_type_id` | → | `tax_registration_types`.`tax_registration_type_id` |
| `cloud_storage_tiered_discounts`.`unit_of_measure_id` | → | `unit_of_measure`.`id` |
| `component_type_capabilities`.`uom_id` | → | `unit_of_measure`.`id` |
| `service_options`.`uom_id` | → | `unit_of_measure`.`id` |
| `client_payment_methods`.`code` | → | `wallet_responses_pl`.`code` |
| `database_errors`.`code` | → | `wallet_responses_pl`.`code` |
| `history_client_payment_methods`.`code` | → | `wallet_responses_pl`.`code` |
| `view_client_payment_methods`.`code` | → | `wallet_responses_pl`.`code` |
| `service_workflow_matrix`.`workflow_event_type_id` | → | `workflow_event_types`.`id` |
| `xref_ticket_routing_by_product_line`.`xref_customer_support_type_sub_type_id` | → | `xref_customer_support_type_sub_type`.`id` |
| `contact`.`zone_id` | → | `zones`.`zone_id` |
