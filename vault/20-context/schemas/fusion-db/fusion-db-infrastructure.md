# Fusion DB — Infrastructure

**Group:** `infrastructure`  
**Tables in group:** 9  
**Accessible:** 8  
**Approximate total rows:** 4,814  
**Generated:** 2026-05-08 15:54  

## Overview

Datacenter and physical infrastructure tables. These map customers and services to physical locations — datacenters, racks, networks, and hosts. Useful for understanding geographic footprint and infrastructure complexity per account.

---

## Table Summary

| Table | Row Count | Columns | Description |
|-------|-----------|---------|-------------|
| `client_private_rack` | ~135 | 11 | Records for client private rack |
| `datacenter_attributes` | ~248 | 9 | Records for datacenter attributes |
| `datacenter_available_currencies` | ~73 | 2 | Records for datacenter available currencies |
| `history_client_private_rack` | ~313 | 14 | Audit/history log for `client_private_rack` |
| `overage_report_new_sflow_servers` | ❌ denied | 12 | Records for overage report new sflow servers |
| `sb_datacenter` | ~54 | 8 | Lookup/reference table for sb datacenter |
| `vam_host` | ~2,908 | 5 | Records for vam host |
| `vmware_hosts` | ~1,056 | 3 | Records for vmware hosts |
| `web_server_types` | ~27 | 3 | Records for web server types |

---

## Column Detail

### `client_private_rack`

**Status:** ✅ ~135 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | no | NOT NULL | Foreign key → `customers.customers_id` |
| `service_id` | `int4` | no | NOT NULL | Foreign key → `customer_products.id` |
| `vlan_id` | `int4` | yes |  | Identifier linking to related record |
| `alias` | `text` | no | NOT NULL |  |
| `datacenter_id` | `int4` | no | NOT NULL | Foreign key → `sb_datacenter.id` |
| `netmask` | `int4` | no | NOT NULL |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `text` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `text` | no | NOT NULL | Timestamp |

**Indexes:**
- `client_private_rack_pkey` — UNIQUE (`id`)
- `client_private_rack_client_id_key` — UNIQUE (`client_id`, `alias`)
- `client_private_rack_vlan_id_key` — UNIQUE (`vlan_id`)

---

### `datacenter_attributes`

**Status:** ✅ ~248 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `object_id` | `int4` | no | NOT NULL | Foreign key → `sb_datacenter.id` |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `attribute_id` | `int4` | no | NOT NULL | Foreign key → `attributes.id` |
| `attribute_group_id` | `int4` | yes |  | Identifier linking to related record |
| `value` | `text` | yes |  |  |

**Indexes:**
- `datacenter_attributes_pkey` — UNIQUE (`id`)

---

### `datacenter_available_currencies`

**Status:** ✅ ~73 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `datacenter_id` | `int4` | no | PK · NOT NULL | Primary key |
| `currency_code` | `varchar(3)` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `datacenter_available_currencies_pkey` — UNIQUE (`datacenter_id`, `currency_code`)

---

### `history_client_private_rack`

**Status:** ✅ ~313 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `service_id` | `int4` | yes |  | Identifier linking to related record |
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
| `history_client_private_rack_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_client_private_rack_pkey` — UNIQUE (`history_client_private_rack_id`)

---

### `overage_report_new_sflow_servers`

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
- `overage_report_new_sflow_servers_pkey` — UNIQUE (`overage_index`)

---

### `sb_datacenter`

**Status:** ✅ ~54 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `text` | no | NOT NULL |  |
| `city` | `text` | yes |  | Address field |
| `state` | `text` | yes |  |  |
| `dc_abbr` | `text` | no | NOT NULL |  |
| `active` | `bool` | yes |  | Boolean state flag |
| `url` | `varchar(64)` | no | NOT NULL |  |
| `countries_id` | `int4` | no | NOT NULL | Foreign key → `countries.countries_id` |

**Indexes:**
- `sb_datacenter_pkey` — UNIQUE (`id`)
- `sb_datacenter_name_key` — UNIQUE (`name`)

---

### `vam_host`

**Status:** ✅ ~2,908 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `service_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `sspc_url` | `varchar(255)` | yes |  |  |
| `creation_phase` | `int4` | no | NOT NULL |  |
| `resource_name` | `varchar(80)` | yes |  | Human-readable name |

**Indexes:**
- `vam_host_ukey` — UNIQUE (`service_id`)

---

### `vmware_hosts`

**Status:** ✅ ~1,056 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `service_id` | `int4` | yes |  | Foreign key → `customer_products.id` |
| `parent_service_id` | `int4` | yes |  | Foreign key → `customer_products.id` |

**Indexes:**
- `vmware_hosts_pkey` — UNIQUE (`id`)

---

### `web_server_types`

**Status:** ✅ ~27 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `code` | `text` | no | NOT NULL |  |
| `description` | `text` | no | NOT NULL |  |

**Indexes:**
- `web_server_types_pkey` — UNIQUE (`id`)

---

## Relationships

| From | | To |
|------|---|-----|
| `client_private_rack`.`client_id` | → | `customers`.`customers_id` |
| `client_private_rack`.`service_id` | → | `customer_products`.`id` |
| `datacenter_attributes`.`attribute_id` | → | `attributes`.`id` |
| `datacenter_available_currencies`.`currency_code` | → | `currencies`.`code` |
| `sb_datacenter`.`countries_id` | → | `countries`.`countries_id` |
| `vmware_hosts`.`service_id` | → | `customer_products`.`id` |
| `vmware_hosts`.`parent_service_id` | → | `customer_products`.`id` |
| `xref_services_private_rack`.`private_rack_id` | → | `client_private_rack`.`id` |
| `cart`.`datacenter_id` | → | `sb_datacenter`.`id` |
| `client_private_net`.`datacenter_id` | → | `sb_datacenter`.`id` |
| `contract_types`.`datacenter` | → | `sb_datacenter`.`id` |
| `item_tax_schedule`.`datacenter` | → | `sb_datacenter`.`id` |
| `order_line_items`.`location_id` | → | `sb_datacenter`.`id` |
| `preconfigured_bundle_mapping`.`datacenter_id` | → | `sb_datacenter`.`id` |
| `pricebook`.`datacenter` | → | `sb_datacenter`.`id` |
| `promotion_location_criteria`.`location_id` | → | `sb_datacenter`.`id` |
| `service_inventory_unavailable`.`datacenter_id` | → | `sb_datacenter`.`id` |
| `service_workflow_matrix`.`datacenter_id` | → | `sb_datacenter`.`id` |
| `xref_customer_products_dcc`.`datacenter_id` | → | `sb_datacenter`.`id` |
