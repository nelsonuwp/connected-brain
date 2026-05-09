# Fusion DB — Billing & Finance

**Group:** `billing-finance`  
**Tables in group:** 21  
**Accessible:** 21  
**Approximate total rows:** 5,698,692  
**Generated:** 2026-05-08 15:54  

## Overview

Billing detail, exchange rate, and financial tables. These records capture what customers are charged, in which currency, and at what rates. Key for MRR/ARR estimates, growth signals, and revenue health indicators in account briefs.

---

## Table Summary

| Table | Row Count | Columns | Description |
|-------|-----------|---------|-------------|
| `accountid_payment_method` | ~7,884 | 2 | Records for accountid payment method |
| `client_payment_methods` | ~99,075 | 18 | Records for client payment methods |
| `exchange_rates` | ~15 | 6 | Records for exchange rates |
| `history_client_payment_methods` | ~488,274 | 20 | Audit/history log for `client_payment_methods` |
| `history_exchange_rates` | ~320 | 8 | Audit/history log for `exchange_rates` |
| `history_service_billing_details` | ~638,528 | 12 | Audit/history log for `service_billing_details` |
| `history_tax_rates` | ~111 | 9 | Audit/history log for `tax_rates` |
| `nbt_invoices` | ~5,317 | 7 | Records for nbt invoices |
| `order_line_item_migrated_services` | ~27,850 | 2 | Records for order line item migrated services |
| `payment_gateway_providers` | ~3 | 3 | Records for payment gateway providers |
| `payment_gateway_transaction_log_details` | ~28 | 4 | Records for payment gateway transaction log details |
| `payment_gateway_transaction_logs` | ~14 | 2 | Records for payment gateway transaction logs |
| `payment_merchant_accounts` | ~25 | 14 | Records for payment merchant accounts |
| `payment_terms` | ~11 | 1 | Records for payment terms |
| `payment_transaction_documents` | ~2,185,546 | 6 | Records for payment transaction documents |
| `payment_transactions` | ~2,081,949 | 31 | Records for payment transactions |
| `payment_transactions_paypal` | < 1 | 7 | Records for payment transactions paypal |
| `payment_types` | ~6 | 6 | Records for payment types |
| `service_billing_details` | ~162,715 | 9 | Records for service billing details |
| `tax_rates` | ~45 | 7 | Records for tax rates |
| `vam_billing_account` | ~976 | 5 | Records for vam billing account |

---

## Column Detail

### `accountid_payment_method`

**Status:** ✅ ~7,884 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `accountid` | `int4` | no | PK · NOT NULL | Primary key |
| `payment_method_id` | `int4` | yes |  | Identifier linking to related record |

**Indexes:**
- `accountid_payment_method_pkey` — UNIQUE (`accountid`)

---

### `client_payment_methods`

**Status:** ✅ ~99,075 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `client_id` | `int4` | yes |  | Foreign key → `customers.customers_id` |
| `payment_type_id` | `int4` | no | NOT NULL | Foreign key → `payment_types.id` |
| `wallet_id` | `varchar(256)` | no | NOT NULL | Identifier linking to related record |
| `is_active` | `bool` | no | NOT NULL | Boolean state flag |
| `display_info` | `varchar(32)` | no | NOT NULL |  |
| `code` | `int4` | yes |  | Foreign key → `wallet_responses_pl.code` |
| `response` | `varchar` | yes |  |  |
| `created` | `timestamptz` | yes |  | Timestamp |
| `auth_code` | `varchar` | yes |  | Short code or identifier |
| `transaction_id` | `varchar` | yes |  | Identifier linking to related record |
| `message_id` | `varchar` | yes |  | Identifier linking to related record |
| `message_text` | `varchar` | yes |  |  |
| `transaction_date` | `varchar` | yes |  | Date value |
| `disabled` | `bool` | yes |  |  |
| `disabled_reason` | `varchar(256)` | yes |  |  |
| `card_type` | `varchar` | yes |  | Type or category classifier |
| `fraud_review_required` | `bool` | yes |  |  |

**Indexes:**
- `client_payment_methods_pkey` — UNIQUE (`id`)
- `client_payment_methods_wallet_id_key` — UNIQUE (`client_id`, `wallet_id`)

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

### `history_client_payment_methods`

**Status:** ✅ ~488,274 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | yes |  |  |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `payment_type_id` | `int4` | yes |  | Identifier linking to related record |
| `wallet_id` | `varchar(256)` | yes |  | Identifier linking to related record |
| `is_active` | `bool` | yes |  | Boolean state flag |
| `display_info` | `varchar(32)` | yes |  |  |
| `action` | `varchar(16)` | yes |  |  |
| `archive_date` | `timestamp` | yes |  | Date value |
| `code` | `int4` | yes |  | Foreign key → `wallet_responses_pl.code` |
| `response` | `varchar` | yes |  |  |
| `auth_code` | `varchar` | yes |  | Short code or identifier |
| `transaction_id` | `varchar` | yes |  | Identifier linking to related record |
| `message_id` | `varchar` | yes |  | Identifier linking to related record |
| `message_text` | `varchar` | yes |  |  |
| `transaction_date` | `varchar` | yes |  | Date value |
| `disabled` | `bool` | yes |  |  |
| `disabled_reason` | `varchar(256)` | yes |  |  |
| `history_client_payment_methods_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `card_type` | `varchar(20)` | yes |  | Type or category classifier |
| `fraud_review_required` | `bool` | yes |  |  |

**Indexes:**
- `history_client_payment_methods_pkey` — UNIQUE (`history_client_payment_methods_id`)
- `index_history_client_payment_methods_client_id` — (`client_id`)
- `index_history_client_payment_methods_id` — (`id`)

---

### `history_exchange_rates`

**Status:** ✅ ~320 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `ocean_exchange_rate_id` | `varchar(15)` | yes |  | Identifier linking to related record |
| `gp_exchange_rate_id` | `varchar(15)` | yes |  | Identifier linking to related record |
| `functional_currency` | `varchar(3)` | no | PK · NOT NULL | Primary key |
| `originating_currency` | `varchar(3)` | no | PK · NOT NULL | Primary key |
| `exchange_rate` | `numeric` | no | NOT NULL |  |
| `last_modified` | `timestamp` | no | PK · NOT NULL | Primary key |
| `action` | `varchar(20)` | no | NOT NULL |  |
| `archive_date` | `timestamp` | no | NOT NULL | Date value |

**Indexes:**
- `history_exchange_rates_pkey` — UNIQUE (`functional_currency`, `originating_currency`, `last_modified`)

---

### `history_service_billing_details`

**Status:** ✅ ~638,528 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `service_id` | `int4` | yes |  | Identifier linking to related record |
| `contract_id` | `varchar(32)` | yes |  | Identifier linking to related record |
| `billing_day` | `int4` | yes |  |  |
| `billing_frequency` | `int4` | yes |  |  |
| `contract_length` | `int4` | yes |  | Foreign key → `contract_lengths.contract_length` |
| `payment_method_id` | `int4` | yes |  | Identifier linking to related record |
| `purchase_order` | `varchar(32)` | yes |  |  |
| `promotion_id` | `int4` | yes |  | Identifier linking to related record |
| `on_hold` | `bool` | yes |  |  |
| `archive_date` | `timestamptz` | no | NOT NULL | Date value |
| `action` | `varchar(20)` | yes |  |  |
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `history_service_billing_details_pkey` — UNIQUE (`id`)
- `service_payment_method_id_archive_idx` — (`service_id`, `payment_method_id`, `archive_date`)

---

### `history_tax_rates`

**Status:** ✅ ~111 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | no | PK · NOT NULL | Primary key |
| `tax_schedule_id` | `varchar(15)` | no | NOT NULL | Identifier linking to related record |
| `country` | `varchar(2)` | no | NOT NULL | Address field |
| `tax_rate` | `numeric` | no | NOT NULL |  |
| `tax_portion` | `numeric` | no | NOT NULL |  |
| `description` | `varchar(31)` | no | NOT NULL |  |
| `last_modified` | `timestamp` | no | PK · NOT NULL | Primary key |
| `action` | `varchar(20)` | no | NOT NULL |  |
| `archive_date` | `timestamp` | no | NOT NULL | Date value |

**Indexes:**
- `history_tax_rates_pkey` — UNIQUE (`id`, `last_modified`)

---

### `nbt_invoices`

**Status:** ✅ ~5,317 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `customer_id` | `int4` | no | PK · NOT NULL | Primary key |
| `document_id` | `varchar(128)` | no | PK · NOT NULL | Primary key |
| `document_type` | `varchar(16)` | no | NOT NULL | Type or category classifier |
| `due_date` | `timestamp` | yes |  | Date value |
| `amount` | `numeric` | yes |  |  |
| `status` | `varchar(4)` | no | NOT NULL |  |
| `filename` | `varchar(128)` | yes |  |  |

**Indexes:**
- `nbt_invoices_pkey` — UNIQUE (`customer_id`, `document_id`)

---

### `order_line_item_migrated_services`

**Status:** ✅ ~27,850 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `order_line_item_id` | `int4` | no | PK · NOT NULL | Primary key |
| `service_id` | `int4` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `order_line_item_migrated_services_pkey` — UNIQUE (`order_line_item_id`, `service_id`)

---

### `payment_gateway_providers`

**Status:** ✅ ~3 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `payment_gateway_id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `name` | `varchar` | no | NOT NULL |  |
| `is_active` | `bool` | yes |  | Boolean state flag |

**Indexes:**
- `payment_gateway_providers_pkey` — UNIQUE (`payment_gateway_id`)

---

### `payment_gateway_transaction_log_details`

**Status:** ✅ ~28 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `log_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `name` | `text` | yes |  |  |
| `value` | `text` | yes |  |  |
| `attribute_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `payment_gateway_transaction_log_details_pkey` — UNIQUE (`attribute_id`)

---

### `payment_gateway_transaction_logs`

**Status:** ✅ ~14 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `transaction_id` | `int4` | no | PK · NOT NULL | Primary key |
| `log_id` | `serial` | no | PK · auto · NOT NULL | Primary key |

**Indexes:**
- `payment_gateway_transaction_logs_pkey1` — UNIQUE (`transaction_id`, `log_id`)

---

### `payment_merchant_accounts`

**Status:** ✅ ~25 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `payment_merchant_id` | `varchar` | no | PK · NOT NULL | Primary key |
| `payment_user` | `varchar` | yes |  |  |
| `payment_pass` | `varchar` | yes |  |  |
| `payment_processing_url` | `varchar` | yes |  |  |
| `payment_gateway_url` | `varchar` | yes |  |  |
| `payment_gateway_id` | `int4` | no | PK · NOT NULL | Primary key |
| `company` | `varchar(3)` | no | PK · NOT NULL | Primary key |
| `functional_currency` | `varchar(3)` | no | PK · NOT NULL | Primary key |
| `originating_currency` | `varchar(3)` | no | PK · NOT NULL | Primary key |
| `environment` | `varchar` | no | PK · NOT NULL | Primary key |
| `is_active` | `bool` | yes |  | Boolean state flag |
| `payment_signature` | `varchar` | yes |  |  |
| `payment_profile_url` | `varchar` | yes |  |  |
| `payment_webform_url` | `varchar` | yes |  |  |

**Indexes:**
- `payment_merchant_accounts_pkey` — UNIQUE (`payment_merchant_id`, `company`, `functional_currency`, `originating_currency`, `environment`, `payment_gateway_id`)

---

### `payment_terms`

**Status:** ✅ ~11 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `payment_term` | `varchar(21)` | no | PK · NOT NULL | Primary key |

**Indexes:**
- `payment_terms_pkey` — UNIQUE (`payment_term`)

---

### `payment_transaction_documents`

**Status:** ✅ ~2,185,546 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `payment_transaction_id` | `int4` | no | PK · NOT NULL | Primary key |
| `document_type` | `varchar` | yes |  | Type or category classifier |
| `document_id` | `varchar` | no | PK · NOT NULL | Primary key |
| `amount` | `numeric` | yes |  |  |
| `sales_tax` | `numeric` | yes |  |  |
| `id` | `serial` | no | auto · NOT NULL |  |

**Indexes:**
- `payment_transaction_documents_pkey` — UNIQUE (`document_id`, `payment_transaction_id`)
- `payment_transaction_documents_payment_idx` — (`payment_transaction_id`)

---

### `payment_transactions`

**Status:** ✅ ~2,081,949 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `date` | `timestamptz` | yes |  |  |
| `client_wallet` | `varchar(32)` | yes |  |  |
| `amount` | `numeric` | yes |  |  |
| `type` | `varchar(32)` | yes |  |  |
| `billing_name` | `varchar(256)` | yes |  | Human-readable name |
| `billing_phone` | `varchar(20)` | yes |  | Phone number |
| `billing_email` | `varchar(256)` | yes |  | Email address |
| `billing_street` | `varchar(256)` | yes |  | Address field |
| `billing_suburb` | `varchar(256)` | yes |  |  |
| `billing_city` | `varchar(256)` | yes |  | Address field |
| `billing_province` | `varchar(256)` | yes |  |  |
| `billing_postal_code` | `varchar(10)` | yes |  | Short code or identifier |
| `billing_country` | `varchar(2)` | yes |  | Address field |
| `status` | `varchar(30)` | yes |  |  |
| `last_modified` | `timestamptz` | yes |  | Timestamp |
| `originating_currency` | `varchar(5)` | yes |  |  |
| `comments` | `varchar` | yes |  |  |
| `authcode` | `varchar(32)` | yes |  |  |
| `token` | `varchar(32)` | yes |  |  |
| `message` | `varchar` | yes |  |  |
| `display_info` | `varchar(32)` | yes |  |  |
| `payment_type` | `varchar(32)` | yes |  | Type or category classifier |
| `created_by` | `varchar(256)` | yes |  | Timestamp |
| `sales_tax` | `numeric` | yes |  |  |
| `company` | `varchar(3)` | yes |  |  |
| `functional_currency` | `varchar(3)` | yes |  |  |
| `client_id` | `int4` | yes |  | Identifier linking to related record |
| `card_type` | `varchar` | yes |  | Type or category classifier |
| `payment_gateway_name` | `varchar(32)` | yes |  | Human-readable name |
| `receipt` | `varchar(50)` | yes |  |  |

**Indexes:**
- `payment_transactions_pkey1` — UNIQUE (`id`)
- `payment_transaction_client_idx` — (`client_id`)
- `payment_transactions_receipt_idx` — (`receipt`)

---

### `payment_transactions_paypal`

**Status:** ✅ < 1 row  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `payment_transaction_id` | `int4` | yes |  | Foreign key → `payment_transactions.id` |
| `transaction_id` | `varchar(32)` | yes |  | Identifier linking to related record |
| `correlation_id` | `varchar(32)` | yes |  | Identifier linking to related record |
| `payment_status` | `varchar(32)` | yes |  | Status code or label |
| `pending_reason` | `varchar(256)` | yes |  |  |
| `email` | `varchar(256)` | yes |  | Email address |

**Indexes:**
- `payment_transactions_paypal_pkey` — UNIQUE (`id`)

---

### `payment_types`

**Status:** ✅ ~6 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `int4` | no | PK · NOT NULL | Primary key |
| `type` | `varchar(32)` | no | NOT NULL |  |
| `description` | `varchar(256)` | yes |  |  |
| `mgr_approval_required` | `bool` | no | NOT NULL |  |
| `wallet_id_required` | `bool` | yes |  |  |
| `is_active` | `bool` | no | NOT NULL | Boolean state flag |

**Indexes:**
- `payment_types_pkey` — UNIQUE (`id`)
- `payment_types_type_key` — UNIQUE (`type`)

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

### `tax_rates`

**Status:** ✅ ~45 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `id` | `serial` | no | PK · auto · NOT NULL | Primary key |
| `tax_schedule_id` | `varchar(15)` | no | NOT NULL | Identifier linking to related record |
| `country` | `varchar(2)` | no | NOT NULL | Foreign key → `countries.countries_iso_code_2` |
| `tax_rate` | `numeric` | no | NOT NULL |  |
| `tax_portion` | `numeric` | no | NOT NULL |  |
| `description` | `varchar(31)` | no | NOT NULL |  |
| `last_modified` | `timestamp` | no | NOT NULL | Timestamp |

**Indexes:**
- `tax_rates_pkey` — UNIQUE (`id`)
- `tax_rates_tax_schedule_id_key` — UNIQUE (`tax_schedule_id`, `country`)

---

### `vam_billing_account`

**Status:** ✅ ~976 rows  
**Type:** TABLE  

| Column | Type | Nullable | Flags | Description |
|--------|------|----------|-------|-------------|
| `client_id` | `int4` | no | NOT NULL | Identifier linking to related record |
| `sspc_url` | `varchar(255)` | yes |  |  |
| `initial_address_url` | `varchar(255)` | yes |  | Address field |
| `login` | `varchar(80)` | yes |  |  |
| `password` | `varchar(80)` | yes |  |  |

**Indexes:**
- `vam_billing_account_ukey` — UNIQUE (`client_id`)

---

## Relationships

| From | | To |
|------|---|-----|
| `client_payment_methods`.`client_id` | → | `customers`.`customers_id` |
| `client_payment_methods`.`code` | → | `wallet_responses_pl`.`code` |
| `exchange_rates`.`functional_currency` | → | `currencies`.`code` |
| `exchange_rates`.`originating_currency` | → | `currencies`.`code` |
| `history_client_payment_methods`.`code` | → | `wallet_responses_pl`.`code` |
| `history_service_billing_details`.`contract_length` | → | `contract_lengths`.`contract_length` |
| `nbt_invoices`.`customer_id` | → | `customers`.`customers_id` |
| `order_line_item_migrated_services`.`order_line_item_id` | → | `order_line_items`.`id` |
| `order_line_item_migrated_services`.`service_id` | → | `customer_products`.`id` |
| `service_billing_details`.`service_id` | → | `customer_products`.`id` |
| `service_billing_details`.`contract_length` | → | `contract_lengths`.`contract_length` |
| `service_billing_details`.`promotion_id` | → | `promotions`.`id` |
| `tax_rates`.`country` | → | `countries`.`countries_iso_code_2` |
| `fraud_gateway_transactions`.`payment_method_id` | → | `client_payment_methods`.`id` |
| `order_line_items`.`payment_method_id` | → | `client_payment_methods`.`id` |
| `customers`.`payment_term` | → | `payment_terms`.`payment_term` |
| `history_customers`.`payment_term` | → | `payment_terms`.`payment_term` |
| `view_clients`.`payment_term` | → | `payment_terms`.`payment_term` |
| `order_line_items`.`payment_type` | → | `payment_types`.`id` |
| `item_tax_schedule`.`mrc_tax_id` | → | `tax_rates`.`id` |
| `item_tax_schedule`.`nrc_tax_id` | → | `tax_rates`.`id` |
| `item_tax_schedule`.`rate_tax_id` | → | `tax_rates`.`id` |
| `item_tax_schedule`.`setup_tax_id` | → | `tax_rates`.`id` |
