# Fusion DB — Inaccessible Tables

**Group:** `inaccessible`  
**Tables in group:** 19  
**Accessible:** 0  
**Approximate total rows:** 0  
**Generated:** 2026-05-08 15:54  

## Overview

Tables present in the Fusion DB schema but not readable by the `sb_readonly` user. Listed here for completeness. If a table you need is in this group, access must be granted at the DB level before it can be used in the pipeline.

---

## Table Summary

| Table | Row Count | Columns | Description |
|-------|-----------|---------|-------------|
| `c2ouat` | ❌ denied | 3 | Records for c2ouat |
| `capability_types` | ❌ denied | 2 | Lookup/reference table for capability types |
| `cloud_external_entities` | ❌ denied | 3 | Lookup/reference table for cloud external entities |
| `cloud_external_entity_identifiers` | ❌ denied | 4 | Records for cloud external entity identifiers |
| `cloud_external_entity_types` | ❌ denied | 3 | Lookup/reference table for cloud external entity types |
| `cloud_external_field_types` | ❌ denied | 3 | Lookup/reference table for cloud external field types |
| `cloud_option_statuses` | ❌ denied | 2 | Lookup/reference table for cloud option statuses |
| `cloud_option_types` | ❌ denied | 2 | Lookup/reference table for cloud option types |
| `cloud_options` | ❌ denied | 13 | Lookup/reference table for cloud options |
| `cloud_options_external_entities` | ❌ denied | 2 | Records for cloud options external entities |
| `cloud_profiles` | ❌ denied | 5 | Lookup/reference table for cloud profiles |
| `cloud_profiles_external_entities` | ❌ denied | 2 | Records for cloud profiles external entities |
| `cloud_types` | ❌ denied | 2 | Lookup/reference table for cloud types |
| `connectivity_carriers` | ❌ denied | 3 | Lookup/reference table for connectivity carriers |
| `order_line_item_details_removed` | ❌ denied | 5 | Records for order line item details removed |
| `order_status_audit` | ❌ denied | 11 | Records for order status audit |
| `overage_report` | ❌ denied | 12 | Records for overage report |
| `overage_report_custom` | ❌ denied | 12 | Records for overage report custom |
| `tags` | ❌ denied | 3 | Lookup/reference table for tags |

---

## Column Detail

### `c2ouat`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `order_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `contract_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `service_id` | `int4` | no | NOT NULL | Identifier linking to related record |

---

### `capability_types`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | yes |  |  |

**Indexes:**
- `capability_types_pkey` — UNIQUE (`id`)

---

### `cloud_external_entities`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(255)` | no | NOT NULL |  |
| `external_entity_type_id` | `int4` | no | NOT NULL | Foreign key → `cloud_external_entity_types.id` |

**Indexes:**
- `cloud_external_entities_pkey` — UNIQUE (`id`)
- `cloud_external_entities_id` — (`id`)

---

### `cloud_external_entity_identifiers`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `external_entity_id` | `int4` | no | NOT NULL | Foreign key → `cloud_external_entities.id` |
| `external_field_type_id` | `int4` | no | NOT NULL | Foreign key → `cloud_external_field_types.id` |
| `external_identifier` | `varchar(128)` | yes |  |  |

**Indexes:**
- `cloud_external_entity_identifiers_pkey` — UNIQUE (`id`)
- `cloud_external_entity_identifiers_id` — (`id`)

---

### `cloud_external_entity_types`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `cloud_type_id` | `int4` | no | NOT NULL | Foreign key → `cloud_types.id` |

**Indexes:**
- `cloud_external_entity_types_pkey` — UNIQUE (`id`)
- `cloud_external_entity_types_id` — (`id`)

---

### `cloud_external_field_types`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `cloud_type_id` | `int4` | no | NOT NULL | Foreign key → `cloud_types.id` |

**Indexes:**
- `cloud_external_field_types_pkey` — UNIQUE (`id`)
- `cloud_external_field_types_id` — (`id`)

---

### `cloud_option_statuses`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |

**Indexes:**
- `cloud_option_statuses_pkey` — UNIQUE (`id`)
- `cloud_option_statuses_id` — (`id`)

---

### `cloud_option_types`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |

**Indexes:**
- `cloud_option_types_pkey` — UNIQUE (`id`)
- `cloud_option_types_id` — (`id`)

---

### `cloud_options`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `cloud_option_type_id` | `int4` | no | NOT NULL | Foreign key → `cloud_option_types.id` |
| `cloud_profile_id` | `int4` | no | NOT NULL | Foreign key → `cloud_profiles.id` |
| `service_option_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `uom_id` | `int4` | yes |  | Identifier linking to related record |
| `capability_value` | `varchar(32)` | no | NOT NULL |  |
| `cloud_option_status_id` | `int4` | no | NOT NULL | Foreign key → `cloud_option_statuses.id` |
| `provisioned_date` | `timestamp` | yes |  | Date value |
| `is_active` | `bool` | no | NOT NULL | Boolean state flag |
| `deprovisioned_date` | `timestamp` | yes |  | Date value |
| `billing_start_date` | `timestamp` | yes |  | Date value |
| `old_cloud_option_id` | `int4` | yes |  | Identifier linking to related record |

**Indexes:**
- `cloud_options_pkey` — UNIQUE (`id`)
- `cloud_options_id` — (`id`)

---

### `cloud_options_external_entities`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `cloud_option_id` | `int4` | no | PK · NOT NULL | Primary key |
| `external_entity_id` | `int4` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `cloud_options_external_entities_pk` — UNIQUE (`cloud_option_id`, `external_entity_id`)

---

### `cloud_profiles`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |
| `cloud_type_id` | `int4` | no | NOT NULL | Foreign key → `cloud_types.id` |
| `service_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `provisioned_date` | `timestamp` | yes |  | Date value |

**Indexes:**
- `cloud_profiles_pkey` — UNIQUE (`id`)
- `cloud_profiles_id` — (`id`)

---

### `cloud_profiles_external_entities`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `cloud_profile_id` | `int4` | no | PK · NOT NULL | Primary key |
| `external_entity_id` | `int4` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `cloud_profiles_external_entities_pk` — UNIQUE (`cloud_profile_id`, `external_entity_id`)

---

### `cloud_types`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(64)` | no | NOT NULL |  |

**Indexes:**
- `cloud_types_pkey` — UNIQUE (`id`)
- `cloud_types_id` — (`id`)

---

### `connectivity_carriers`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(128)` | yes |  |  |
| `description` | `text` | yes |  |  |

**Indexes:**
- `connectivity_carriers_pkey` — UNIQUE (`id`)

---

### `order_line_item_details_removed`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `order_line_item_id` | `int4` | no | PK · NOT NULL | Primary key |
| `component_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `component_name` | `varchar(64)` | no | NOT NULL | Human-readable name |
| `mrc` | `numeric` | no | NOT NULL |  |
| `service_option_id` | `int4` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `order_line_item_details_removed_pk` — UNIQUE (`order_line_item_id`, `service_option_id`)

---

### `order_status_audit`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `order_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `order_status_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `contact_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `first_name` | `text` | yes |  | Human-readable name |
| `last_name` | `text` | yes |  | Human-readable name |
| `username` | `varchar(64)` | yes |  |  |
| `ip` | `varchar(16)` | no | NOT NULL |  |
| `x_forwarded_for` | `text` | yes |  |  |
| `user_agent` | `text` | no | NOT NULL |  |
| `created_at` | `timestamptz` | yes |  | Timestamp |

**Indexes:**
- `order_status_audit_pkey` — UNIQUE (`id`)
- `idx_order_status_audit` — (`order_id`)

---

### `overage_report`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `overage_index` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `client_name` | `text` | no | NOT NULL | Human-readable name |
| `salesperson` | `text` | no | NOT NULL |  |
| `nas` | `text` | yes |  |  |
| `bag_id` | `text` | yes |  | Identifier linking to related record |
| `bag_name` | `text` | yes |  | Human-readable name |
| `service_id` | `text` | no | NOT NULL | Identifier linking to related record |
| `bandwidth` | `text` | no | NOT NULL |  |
| `usedbandwidth` | `text` | no | NOT NULL |  |
| `overage_rate` | `text` | no | NOT NULL |  |
| `product_line` | `text` | no | NOT NULL |  |

**Indexes:**
- `overage_report_pkey` — UNIQUE (`overage_index`)

---

### `overage_report_custom`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `overage_index` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `client_name` | `text` | no | NOT NULL | Human-readable name |
| `salesperson` | `text` | no | NOT NULL |  |
| `nas` | `text` | yes |  |  |
| `bag_id` | `text` | yes |  | Identifier linking to related record |
| `bag_name` | `text` | yes |  | Human-readable name |
| `service_id` | `text` | no | NOT NULL | Identifier linking to related record |
| `bandwidth` | `text` | no | NOT NULL |  |
| `usedbandwidth` | `text` | no | NOT NULL |  |
| `overage_rate` | `text` | no | NOT NULL |  |
| `product_line` | `text` | no | NOT NULL |  |

**Indexes:**
- `overage_report_custom_pkey` — UNIQUE (`overage_index`)

---

### `tags`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar(128)` | yes |  |  |
| `description` | `text` | yes |  |  |

**Indexes:**
- `tags_pkey` — UNIQUE (`id`)
- `tag_name_idx` — UNIQUE (`name`)

---

## Relationships

_No cross-group foreign key relationships found._
