# Fusion DB — People & Org

**Group:** `people-org`  
**Tables in group:** 26  
**Accessible:** 25  
**Approximate total rows:** 16,260,793  
**Generated:** 2026-05-08 15:54  

## Overview

Employee, contact, and relationship tables. These capture who at Aptum owns each account (client relations), the roles they hold, and the internal org structure. Essential for generating audience-specific briefs and identifying the right stakeholder contacts per account.

---

## Table Summary

| Table | Row Count | Columns | Description |
|-------|-----------|---------|-------------|
| `certificate_contacts` | ~867 | 26 | Records for certificate contacts |
| `client_permission_roles` | ~1,948,738 | 7 | Records for client permission roles |
| `client_permission_users` | ~750 | 7 | Records for client permission users |
| `client_relations` | ~25,713 | 5 | Records for client relations |
| `client_relations_roles` | ~5 | 3 | Lookup/reference table for client relations roles |
| `contact` | ~74,979 | 26 | Records for contact |
| `contact_attribute` | ~95,759 | 10 | Records for contact attribute |
| `contact_attribute_history` | ~529,079 | 10 | Records for contact attribute history |
| `contact_communication_method` | ~168,955 | 5 | Records for contact communication method |
| `contact_communication_method_bkup` | ~119 | 5 | Records for contact communication method bkup |
| `contact_ids_need_permissions` | ❌ denied | 1 | Records for contact ids need permissions |
| `contact_role` | ~107,173 | 3 | Records for contact role |
| `contact_role_type` | ~9 | 2 | Records for contact role type |
| `employee_client_relations_quotas` | ~192 | 16 | Records for employee client relations quotas |
| `employee_client_relations_roles_matrix` | ~103 | 6 | Records for employee client relations roles matrix |
| `employees` | ~5,327 | 12 | Records for employees |
| `history_client_permission_roles` | ~10,051,468 | 10 | Audit/history log for `client_permission_roles` |
| `history_client_permission_users` | ~6,144 | 10 | Audit/history log for `client_permission_users` |
| `history_contact` | ~387,329 | 26 | Audit/history log for `contact` |
| `history_contact_communication_method` | ~1,081,046 | 8 | Audit/history log for `contact_communication_method` |
| `history_contact_role` | ~651,681 | 6 | Audit/history log for `contact_role` |
| `history_template_permission_roles` | ~406 | 9 | Audit/history log for `template_permission_roles` |
| `roles` | ~23,143 | 3 | Lookup/reference table for roles |
| `template_permission_roles` | ~186 | 6 | Records for template permission roles |
| `xref_customer_rbac_roles` | ~1,090,638 | 4 | Cross-reference/join table |
| `xref_roles_employees` | ~10,984 | 3 | Cross-reference/join table |

---

## Column Detail

### `certificate_contacts`

**Status:** ✅ ~867 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `contact_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `customers_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `company` | `text` | yes |  |  |
| `first_name` | `text` | no | NOT NULL | Human-readable name |
| `last_name` | `text` | no | NOT NULL | Human-readable name |
| `street_address1` | `text` | yes |  | Address field |
| `street_address2` | `text` | yes |  | Address field |
| `street_address3` | `text` | yes |  | Address field |
| `postcode` | `text` | yes |  |  |
| `city` | `text` | yes |  | Address field |
| `country_id` | `int4` | yes |  | Identifier linking to related record |
| `zone_id` | `int4` | yes |  | Identifier linking to related record |
| `username` | `varchar(64)` | yes |  |  |
| `password` | `text` | yes |  |  |
| `security_question` | `varchar(255)` | yes |  |  |
| `security_answer` | `text` | yes |  |  |
| `subscribed` | `bool` | yes |  |  |
| `is_disabled` | `bool` | yes |  |  |
| `portal_user` | `bool` | yes |  |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | yes |  | Timestamp |
| `full_name` | `text` | yes |  | Human-readable name |
| `title` | `text` | yes |  |  |
| `department` | `text` | yes |  |  |

**Indexes:**
- `certificate_contacts_pkey` — UNIQUE (`contact_id`)

---

### `client_permission_roles`

**Status:** ✅ ~1,948,738 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | no | PK · NOT NULL | Primary key |
| `permissions_id` | `varchar(32)` | no | PK · NOT NULL | Primary key |
| `contact_role_type_id` | `int4` | no | PK · NOT NULL | Primary key |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `client_permission_roles_pkey` — UNIQUE (`client_id`, `permissions_id`, `contact_role_type_id`)
- `client_permission_roles_contact_role_type_id_idx` — (`contact_role_type_id`)

---

### `client_permission_users`

**Status:** ✅ ~750 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | no | PK · NOT NULL | Primary key |
| `permissions_id` | `varchar(32)` | no | PK · NOT NULL | Primary key |
| `contact_id` | `int4` | no | PK · NOT NULL | Primary key |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `client_permission_users_pkey` — UNIQUE (`client_id`, `permissions_id`, `contact_id`)
- `client_permission_users_contact_id_idx` — (`contact_id`)

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

### `contact`

**Status:** ✅ ~74,979 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `contact_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `customers_id` | `int4` | no | NOT NULL | Foreign key → `customers.customers_id` |
| `company` | `text` | yes |  |  |
| `first_name` | `text` | no | NOT NULL | Human-readable name |
| `last_name` | `text` | no | NOT NULL | Human-readable name |
| `street_address1` | `text` | yes |  | Address field |
| `street_address2` | `text` | yes |  | Address field |
| `street_address3` | `text` | yes |  | Address field |
| `postcode` | `text` | yes |  |  |
| `city` | `text` | yes |  | Address field |
| `country_id` | `int4` | yes |  | Foreign key → `countries.countries_id` |
| `zone_id` | `int4` | yes |  | Foreign key → `zones.zone_id` |
| `username` | `varchar(64)` | yes |  |  |
| `password` | `text` | yes |  |  |
| `security_question` | `varchar(255)` | yes |  |  |
| `security_answer` | `text` | yes |  |  |
| `subscribed` | `bool` | yes |  |  |
| `is_disabled` | `bool` | yes |  |  |
| `portal_user` | `bool` | yes |  |  |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | yes |  | Timestamp |
| `full_name` | `text` | yes |  | Human-readable name |
| `title` | `text` | yes |  |  |
| `department` | `text` | yes |  |  |

**Indexes:**
- `contact_pkey` — UNIQUE (`contact_id`)
- `contact_customers_id_key` — UNIQUE (`customers_id`, `contact_id`)
- `contact_username_key` — UNIQUE (`username`)

---

### `contact_attribute`

**Status:** ✅ ~95,759 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `object_id` | `int4` | no | NOT NULL | Foreign key → `contact.contact_id` |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `attribute_id` | `int4` | no | NOT NULL | Foreign key → `attributes.id` |
| `value` | `varchar(1024)` | yes |  |  |
| `visibility_group` | `varchar(255)` | yes |  |  |
| `visibility_user` | `varchar(255)` | yes |  |  |

**Indexes:**
- `contact_attribute_pkey` — UNIQUE (`id`)

---

### `contact_attribute_history`

**Status:** ✅ ~529,079 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `contact_attributes_history_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `id` | `int4` | no | NOT NULL |  |
| `object_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `attribute_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `value` | `varchar(1024)` | yes |  |  |
| `last_action` | `varchar(64)` | no | NOT NULL |  |

**Indexes:**
- `contact_attributes_history_pkey` — UNIQUE (`contact_attributes_history_id`)

---

### `contact_communication_method`

**Status:** ✅ ~168,955 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `contact_communication_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `contact_id` | `int4` | no | NOT NULL | Foreign key → `contact.contact_id` |
| `communication_type_id` | `int4` | no | NOT NULL | Foreign key → `communication_type.communication_type_id` |
| `value` | `text` | yes |  |  |
| `is_primary` | `bool` | yes |  |  |

**Indexes:**
- `contact_communication_method_pkey` — UNIQUE (`contact_communication_id`)
- `contact_communication_method_primary_idx` — (`communication_type_id`, `is_primary`)

---

### `contact_communication_method_bkup`

**Status:** ✅ ~119 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `contact_communication_id` | `int4` | yes |  | Identifier linking to related record |
| `contact_id` | `int4` | yes |  | Identifier linking to related record |
| `communication_type_id` | `int4` | yes |  | Identifier linking to related record |
| `value` | `text` | yes |  |  |
| `is_primary` | `bool` | yes |  |  |

---

### `contact_ids_need_permissions`

**Status:** ❌ ❌ permission denied  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `contact_id` | `int4` | yes |  | Identifier linking to related record |

---

### `contact_role`

**Status:** ✅ ~107,173 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `contact_role_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `contact_id` | `int4` | yes |  | Foreign key → `contact.contact_id` |
| `contact_role_type_id` | `int4` | yes |  | Foreign key → `contact_role_type.contact_role_type_id` |

**Indexes:**
- `contact_role_pkey` — UNIQUE (`contact_role_id`)
- `contact_role_contact_id_key` — UNIQUE (`contact_id`, `contact_role_type_id`)

---

### `contact_role_type`

**Status:** ✅ ~9 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `contact_role_type_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `role_name` | `varchar(255)` | yes |  | Human-readable name |

**Indexes:**
- `contact_role_type_pkey` — UNIQUE (`contact_role_type_id`)

---

### `employee_client_relations_quotas`

**Status:** ✅ ~192 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `employee_id` | `int4` | no | NOT NULL | Foreign key → `employees.id` |
| `year` | `int4` | no | NOT NULL |  |
| `variable` | `numeric` | yes |  |  |
| `july_quota` | `numeric` | yes |  |  |
| `august_quota` | `numeric` | yes |  |  |
| `september_quota` | `numeric` | yes |  |  |
| `october_quota` | `numeric` | yes |  |  |
| `november_quota` | `numeric` | yes |  |  |
| `december_quota` | `numeric` | yes |  |  |
| `january_quota` | `numeric` | yes |  |  |
| `february_quota` | `numeric` | yes |  |  |
| `march_quota` | `numeric` | yes |  |  |
| `april_quota` | `numeric` | yes |  |  |
| `may_quota` | `numeric` | yes |  |  |
| `june_quota` | `numeric` | yes |  |  |

**Indexes:**
- `employee_client_relations_quotas_pkey` — UNIQUE (`id`)
- `employee_client_relations_quotas_employee_id_key` — UNIQUE (`employee_id`, `year`)

---

### `employee_client_relations_roles_matrix`

**Status:** ✅ ~103 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `employee_id` | `int4` | no | PK · NOT NULL | Primary key |
| `product_line_id` | `int4` | no | PK · NOT NULL | Primary key |
| `client_relations_role_id` | `int4` | no | PK · NOT NULL | Primary key |
| `last_assigned` | `timestamptz` | no | NOT NULL |  |
| `igo_id` | `int4` | no | NOT NULL | Foreign key → `intergovernmental_organizations.id` |
| `round_robin` | `bool` | no | NOT NULL |  |

**Indexes:**
- `employee_client_relations_roles_matrix_pkey` — UNIQUE (`employee_id`, `product_line_id`, `client_relations_role_id`)
- `employee_client_relations_roles_matrix_roles_idx` — (`product_line_id`, `client_relations_role_id`)

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

### `history_client_permission_roles`

**Status:** ✅ ~10,051,468 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `permissions_id` | `varchar(32)` | yes |  | Foreign key → `permissions.permissions_id` |
| `contact_role_type_id` | `int4` | yes |  | Identifier linking to related record |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `varchar(32)` | yes |  | Timestamp |
| `archive_date` | `timestamptz` | yes |  | Date value |
| `action` | `varchar(16)` | yes |  |  |

**Indexes:**
- `history_client_permission_roles_pkey` — UNIQUE (`id`)

---

### `history_client_permission_users`

**Status:** ✅ ~6,144 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `permissions_id` | `varchar(32)` | yes |  | Foreign key → `permissions.permissions_id` |
| `contact_id` | `int4` | yes |  | Identifier linking to related record |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `varchar(32)` | yes |  | Timestamp |
| `archive_date` | `timestamptz` | yes |  | Date value |
| `action` | `varchar(16)` | yes |  |  |

**Indexes:**
- `history_client_permission_users_pkey` — UNIQUE (`id`)

---

### `history_contact`

**Status:** ✅ ~387,329 rows  
**Type:** TABLE  

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
| `country` | `text` | yes |  | Address field |
| `zone` | `text` | yes |  | Foreign key → `p1_zones.zone` |
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
| `archive_date` | `timestamptz` | no | NOT NULL | Date value |
| `action` | `varchar(16)` | yes |  |  |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_contact_pkey` — UNIQUE (`id`)

---

### `history_contact_communication_method`

**Status:** ✅ ~1,081,046 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `contact_communication_id` | `int4` | yes |  | Identifier linking to related record |
| `contact_id` | `int4` | yes |  | Identifier linking to related record |
| `communication_type` | `varchar(255)` | yes |  | Type or category classifier |
| `value` | `text` | yes |  |  |
| `is_primary` | `bool` | yes |  |  |
| `archive_date` | `timestamptz` | no | NOT NULL | Date value |
| `action` | `varchar(16)` | yes |  |  |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_contact_communication_method_pkey` — UNIQUE (`id`)

---

### `history_contact_role`

**Status:** ✅ ~651,681 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `contact_role_id` | `int4` | yes |  | Identifier linking to related record |
| `contact_id` | `int4` | yes |  | Identifier linking to related record |
| `contact_role_type` | `varchar(255)` | yes |  | Type or category classifier |
| `archive_date` | `timestamptz` | no | NOT NULL | Date value |
| `action` | `varchar(16)` | yes |  |  |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_contact_role_pkey` — UNIQUE (`id`)

---

### `history_template_permission_roles`

**Status:** ✅ ~406 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `permissions_id` | `varchar(32)` | yes |  | Foreign key → `permissions.permissions_id` |
| `contact_role_type_id` | `int4` | yes |  | Identifier linking to related record |
| `created` | `timestamptz` | yes |  | Timestamp |
| `created_by` | `varchar(32)` | yes |  | Timestamp |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `last_modified_by` | `varchar(32)` | yes |  | Timestamp |
| `archive_date` | `timestamptz` | yes |  | Date value |
| `action` | `varchar(16)` | yes |  |  |

**Indexes:**
- `history_template_permission_roles_pkey` — UNIQUE (`id`)

---

### `roles`

**Status:** ✅ ~23,143 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `text` | no | NOT NULL |  |
| `description` | `text` | no | NOT NULL |  |

**Indexes:**
- `roles_pkey` — UNIQUE (`id`)
- `roles_id` — (`id`)

---

### `template_permission_roles`

**Status:** ✅ ~186 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `permissions_id` | `varchar(32)` | no | PK · NOT NULL | Primary key |
| `contact_role_type_id` | `int4` | no | PK · NOT NULL | Primary key |
| `created` | `timestamptz` | no | NOT NULL | Timestamp |
| `created_by` | `varchar(32)` | no | NOT NULL | Timestamp |
| `last_modified` | `timestamptz` | no | NOT NULL | Timestamp |
| `last_modified_by` | `varchar(32)` | no | NOT NULL | Timestamp |

**Indexes:**
- `template_permission_roles_pkey` — UNIQUE (`permissions_id`, `contact_role_type_id`)

---

### `xref_customer_rbac_roles`

**Status:** ✅ ~1,090,638 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `contact_id` | `int4` | no | NOT NULL | Foreign key → `contact.contact_id` |
| `section_id` | `int4` | no | NOT NULL | Foreign key → `my_rbac_sections.id` |
| `permissions` | `int4` | no | NOT NULL |  |

**Indexes:**
- `xref_customer_rbac_roles_pkey` — UNIQUE (`id`)
- `xref_rr_contact_id` — (`contact_id`)

---

### `xref_roles_employees`

**Status:** ✅ ~10,984 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `roles_id` | `int4` | yes |  | Identifier linking to related record |
| `employees_id` | `int4` | yes |  | Foreign key → `employees.id` |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `xref_roles_employees_pkey` — UNIQUE (`id`)

---

## Relationships

| From | | To |
|------|---|-----|
| `client_permission_roles`.`client_id` | → | `customers`.`customers_id` |
| `client_permission_roles`.`permissions_id` | → | `permissions`.`permissions_id` |
| `client_permission_users`.`client_id` | → | `customers`.`customers_id` |
| `client_permission_users`.`permissions_id` | → | `permissions`.`permissions_id` |
| `client_relations`.`client_id` | → | `customers`.`customers_id` |
| `client_relations`.`product_line_id` | → | `product_lines`.`id` |
| `contact`.`customers_id` | → | `customers`.`customers_id` |
| `contact`.`country_id` | → | `countries`.`countries_id` |
| `contact`.`zone_id` | → | `zones`.`zone_id` |
| `contact_attribute`.`attribute_id` | → | `attributes`.`id` |
| `contact_communication_method`.`communication_type_id` | → | `communication_type`.`communication_type_id` |
| `employee_client_relations_roles_matrix`.`product_line_id` | → | `product_lines`.`id` |
| `employee_client_relations_roles_matrix`.`igo_id` | → | `intergovernmental_organizations`.`id` |
| `history_client_permission_roles`.`permissions_id` | → | `permissions`.`permissions_id` |
| `history_client_permission_users`.`permissions_id` | → | `permissions`.`permissions_id` |
| `history_contact`.`zone` | → | `p1_zones`.`zone` |
| `history_template_permission_roles`.`permissions_id` | → | `permissions`.`permissions_id` |
| `template_permission_roles`.`permissions_id` | → | `permissions`.`permissions_id` |
| `xref_customer_rbac_roles`.`section_id` | → | `my_rbac_sections`.`id` |
| `certificate`.`certificate_contact_id` | → | `certificate_contacts`.`contact_id` |
| `client_relations_product_line_independent`.`client_relations_role_id` | → | `client_relations_roles`.`id` |
| `login_history`.`contact_id` | → | `contact`.`contact_id` |
| `portal_login`.`contact_id` | → | `contact`.`contact_id` |
| `sessions`.`contact_id` | → | `contact`.`contact_id` |
| `cart`.`assisted_by` | → | `employees`.`id` |
| `client_news`.`who` | → | `employees`.`id` |
| `client_relations_product_line_independent`.`employee_id` | → | `employees`.`id` |
| `clients_watchers`.`employee_id` | → | `employees`.`id` |
| `customer_products`.`modified_by` | → | `employees`.`id` |
| `customer_tam`.`employees_id` | → | `employees`.`id` |
| `order_commission_split`.`employee_id` | → | `employees`.`id` |
| `billable_ticket_invoicing`.`username` | → | `employees`.`username` |
| `client_orders`.`entered_by` | → | `employees`.`username` |
| `portal_login`.`username` | → | `employees`.`username` |
