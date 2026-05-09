# Fusion DB — Schema Reference Index

This is the **entry point** for navigating the Fusion DB schema documentation.
Load this file first, then open the specific group file(s) relevant to your task.

**Database:** `fusion` on `db1.peer1.com:5432`  
**Access:** SSH tunnel via `10.121.21.20`  
**Generated:** 2026-05-08 15:54  

---

## Group Files

| File | Group | Tables | Description |
|------|-------|--------|-------------|
| [fusion-db-billing-finance.md](fusion-db-billing-finance.md) | `billing-finance` | 21 | Billing details, invoices, exchange rates, and financial records |
| [fusion-db-customer-core.md](fusion-db-customer-core.md) | `customer-core` | 4 | Core customer identity, product subscriptions, history, and churn reasons |
| [fusion-db-inaccessible.md](fusion-db-inaccessible.md) | `inaccessible` | 19 | Tables that exist in schema but are not readable by sb_readonly |
| [fusion-db-infrastructure.md](fusion-db-infrastructure.md) | `infrastructure` | 9 | Datacenters, racks, networks, servers, and physical hosting infrastructure |
| [fusion-db-people-org.md](fusion-db-people-org.md) | `people-org` | 26 | Employees, account owners, client relations, and organizational roles |
| [fusion-db-priority-tables.md](fusion-db-priority-tables.md) | `priority-tables` | 11 | All 14 high-value tables used directly by the AccountIntel pipeline |
| [fusion-db-products-services.md](fusion-db-products-services.md) | `products-services` | 87 | Product catalog, service types, components, and offering definitions |
| [fusion-db-remaining-accessible-a-h.md](fusion-db-remaining-accessible-a-h.md) | `remaining-accessible-a-h` | 190 | Accessible tables not covered by the groups above |
| [fusion-db-remaining-accessible-h-z.md](fusion-db-remaining-accessible-h-z.md) | `remaining-accessible-h-z` | 190 | Accessible tables not covered by the groups above |
| [fusion-db-views.md](fusion-db-views.md) | `views` | 80 | Database views (pre-joined or aggregated read-only projections) |

---

## Priority Tables — Where to Find Them

These 14 tables are used directly by AccountIntel pipeline stages.
Each is in the `priority-tables` group file, and may also appear in its domain group.

| Table | Domain Group File | Priority Tables File |
|-------|-------------------|----------------------|
| `cancellation_category` | `fusion-db-customer-core.md` | `fusion-db-priority-tables.md` |
| `client_relations` | `fusion-db-people-org.md` | `fusion-db-priority-tables.md` |
| `client_relations_roles` | `fusion-db-people-org.md` | `fusion-db-priority-tables.md` |
| `customer_products` | `fusion-db-customer-core.md` | `fusion-db-priority-tables.md` |
| `customer_products_status` | `fusion-db-remaining-accessible*.md` | `fusion-db-priority-tables.md` |
| `customers` | `fusion-db-customer-core.md` | `fusion-db-priority-tables.md` |
| `datacenter` | `fusion-db-remaining-accessible*.md` | `fusion-db-priority-tables.md` |
| `employees` | `fusion-db-people-org.md` | `fusion-db-priority-tables.md` |
| `exchange_rates` | `fusion-db-billing-finance.md` | `fusion-db-priority-tables.md` |
| `history_customer_products` | `fusion-db-customer-core.md` | `fusion-db-priority-tables.md` |
| `product_lines` | `fusion-db-products-services.md` | `fusion-db-priority-tables.md` |
| `service_billing_details` | `fusion-db-billing-finance.md` | `fusion-db-priority-tables.md` |
| `service_types` | `fusion-db-remaining-accessible*.md` | `fusion-db-priority-tables.md` |
| `xref_customer_products_dcc` | `fusion-db-products-services.md` | `fusion-db-priority-tables.md` |

---

## All Tables — Quick Reference

| Table | Type | Row Count | Group |
|-------|------|-----------|-------|
| `accountid_payment_method` | TABLE | ~7,884 | `billing-finance` |
| `app_config` | TABLE | ~29 | `remaining-accessible` |
| `attribute_groupings` | TABLE | ~35 | `remaining-accessible` |
| `attribute_groups` | TABLE | ~7 | `remaining-accessible` |
| `attributes` | TABLE | ~154 | `remaining-accessible` |
| `billable_ticket_invoicing` | TABLE | ~5 | `remaining-accessible` |
| `bu_alerts` | TABLE | ~11,110 | `remaining-accessible` |
| `bu_alerts_change_hist` | TABLE | ~2,496 | `remaining-accessible` |
| `bu_events` | TABLE | < 1 | `remaining-accessible` |
| `bu_events_status` | TABLE | ~8 | `remaining-accessible` |
| `bu_prices` | TABLE | ~125 | `remaining-accessible` |
| `bu_usage` | TABLE | ~18,325,188 | `remaining-accessible` |
| `byo_upsell` | TABLE | ~18 | `remaining-accessible` |
| `c2ouat` | TABLE | ❌ | `inaccessible` |
| `cancellation_category` | TABLE | ~29 | `customer-core` |
| `capabilities` | TABLE | ~73 | `remaining-accessible` |
| `capability_types` | TABLE | ❌ | `inaccessible` |
| `cart` | TABLE | < 1 | `remaining-accessible` |
| `cart_component_private_net` | TABLE | < 1 | `products-services` |
| `cart_component_private_rack` | TABLE | < 1 | `products-services` |
| `cart_components` | TABLE | < 1 | `products-services` |
| `cart_default_removed_components` | TABLE | < 1 | `products-services` |
| `cart_order` | TABLE | ~17 | `remaining-accessible` |
| `cart_raid_array_drives` | TABLE | < 1 | `remaining-accessible` |
| `cart_raid_arrays` | TABLE | < 1 | `remaining-accessible` |
| `ce_pods` | TABLE | ~10 | `remaining-accessible` |
| `certificate` | TABLE | ~5,917 | `remaining-accessible` |
| `certificate_attributes` | TABLE | ~17,368 | `remaining-accessible` |
| `certificate_company` | TABLE | ~5,672 | `remaining-accessible` |
| `certificate_contacts` | TABLE | ~867 | `people-org` |
| `client_bag_allowed_service_statuses` | TABLE | ~10 | `products-services` |
| `client_bag_allowed_service_types` | TABLE | ~9 | `products-services` |
| `client_bag_services` | TABLE | ~7,979 | `products-services` |
| `client_bags` | TABLE | ~1,119 | `remaining-accessible` |
| `client_error_statuses` | TABLE | ~86 | `remaining-accessible` |
| `client_eula_acceptance` | TABLE | ~20,512 | `remaining-accessible` |
| `client_firewall_vlan` | TABLE | ~623 | `remaining-accessible` |
| `client_industries` | TABLE | ~10 | `remaining-accessible` |
| `client_loadbalancer_vlan` | TABLE | < 1 | `remaining-accessible` |
| `client_news` | TABLE | ~23 | `remaining-accessible` |
| `client_notes` | TABLE | ~19,766 | `remaining-accessible` |
| `client_order_statuses` | TABLE | ~30 | `remaining-accessible` |
| `client_order_types` | TABLE | ~3 | `remaining-accessible` |
| `client_orders` | TABLE | ~273,467 | `remaining-accessible` |
| `client_orders_attributes` | TABLE | ~287,257 | `remaining-accessible` |
| `client_payment_methods` | TABLE | ~99,075 | `billing-finance` |
| `client_permission_roles` | TABLE | ~1,948,738 | `people-org` |
| `client_permission_users` | TABLE | ~750 | `people-org` |
| `client_private_net` | TABLE | ~1,215 | `remaining-accessible` |
| `client_private_rack` | TABLE | ~135 | `infrastructure` |
| `client_relations` | TABLE | ~25,713 | `people-org` |
| `client_relations_product_line_independent` | TABLE | ~1,325 | `products-services` |
| `client_relations_roles` | TABLE | ~5 | `people-org` |
| `client_solution_services` | TABLE | ~44,683 | `products-services` |
| `client_solutions` | TABLE | ~17,040 | `remaining-accessible` |
| `client_tax_registrations` | TABLE | ~482 | `remaining-accessible` |
| `client_tax_schedules` | TABLE | ~8 | `remaining-accessible` |
| `client_tickets` | TABLE | ~2,075,256 | `remaining-accessible` |
| `client_tickets_attributes` | TABLE | ~99,785 | `remaining-accessible` |
| `client_types_pl` | TABLE | ~12 | `remaining-accessible` |
| `client_zones` | TABLE | ~8,825 | `remaining-accessible` |
| `clients_watchers` | TABLE | ~1,603 | `remaining-accessible` |
| `cloud_external_entities` | TABLE | ❌ | `inaccessible` |
| `cloud_external_entity_identifiers` | TABLE | ❌ | `inaccessible` |
| `cloud_external_entity_types` | TABLE | ❌ | `inaccessible` |
| `cloud_external_field_types` | TABLE | ❌ | `inaccessible` |
| `cloud_option_statuses` | TABLE | ❌ | `inaccessible` |
| `cloud_option_types` | TABLE | ❌ | `inaccessible` |
| `cloud_options` | TABLE | ❌ | `inaccessible` |
| `cloud_options_external_entities` | TABLE | ❌ | `inaccessible` |
| `cloud_profiles` | TABLE | ❌ | `inaccessible` |
| `cloud_profiles_external_entities` | TABLE | ❌ | `inaccessible` |
| `cloud_storage_attributes` | TABLE | ~927 | `remaining-accessible` |
| `cloud_storage_bandwidth_types_pl` | TABLE | ~3 | `remaining-accessible` |
| `cloud_storage_tiered_discounts` | TABLE | ~27 | `remaining-accessible` |
| `cloud_types` | TABLE | ❌ | `inaccessible` |
| `communication_type` | TABLE | ~9 | `remaining-accessible` |
| `company_type` | TABLE | ~10 | `remaining-accessible` |
| `component_capabilities` | TABLE | ~2,711 | `products-services` |
| `component_categories` | TABLE | ~18 | `products-services` |
| `component_hashes` | TABLE | ~4 | `products-services` |
| `component_license_key_node_data` | TABLE | ~390 | `products-services` |
| `component_license_keys` | TABLE | ~227 | `products-services` |
| `component_provided_resources` | TABLE | ~1,120 | `products-services` |
| `component_required_resources` | TABLE | ~684 | `products-services` |
| `component_type_capabilities` | TABLE | ~105 | `products-services` |
| `component_types` | TABLE | ~386 | `products-services` |
| `component_workorder_templates` | TABLE | ~116 | `products-services` |
| `components` | TABLE | ~5,906 | `products-services` |
| `components_attributes` | TABLE | ~445 | `products-services` |
| `components_tags` | TABLE | ❌ | `products-services` |
| `config_code_components` | TABLE | ~6,401 | `products-services` |
| `config_code_pnet` | TABLE | ~66 | `remaining-accessible` |
| `config_code_raid_array_drives` | TABLE | ~493 | `remaining-accessible` |
| `config_code_raid_arrays` | TABLE | ~219 | `remaining-accessible` |
| `config_codes` | TABLE | ~581 | `remaining-accessible` |
| `connectivity_carriers` | TABLE | ❌ | `inaccessible` |
| `contact` | TABLE | ~74,979 | `people-org` |
| `contact_attribute` | TABLE | ~95,759 | `people-org` |
| `contact_attribute_history` | TABLE | ~529,079 | `people-org` |
| `contact_communication_method` | TABLE | ~168,955 | `people-org` |
| `contact_communication_method_bkup` | TABLE | ~119 | `people-org` |
| `contact_ids_need_permissions` | TABLE | ❌ | `people-org` |
| `contact_role` | TABLE | ~107,173 | `people-org` |
| `contact_role_type` | TABLE | ~9 | `people-org` |
| `contract_lengths` | TABLE | ~6 | `remaining-accessible` |
| `contract_types` | TABLE | ~1,724 | `remaining-accessible` |
| `countries` | TABLE | ~247 | `remaining-accessible` |
| `countries_currencies` | TABLE | ~7 | `remaining-accessible` |
| `countries_intergovernmental_organizations` | TABLE | ~151 | `remaining-accessible` |
| `credit_card_types` | TABLE | ~4 | `remaining-accessible` |
| `currencies` | TABLE | ~4 | `remaining-accessible` |
| `customer_products` | TABLE | ~162,775 | `customer-core` |
| `customer_products_attributes` | TABLE | ~114,376 | `products-services` |
| `customer_products_mercury_services` | TABLE | ~3,228 | `products-services` |
| `customer_products_status_history` | TABLE | ~1,514,021 | `products-services` |
| `customer_products_status_options` | TABLE | ~13 | `products-services` |
| `customer_support_faq` | TABLE | ~272 | `remaining-accessible` |
| `customer_support_faq_product_lines` | TABLE | ~425 | `products-services` |
| `customer_support_faq_tags` | TABLE | ~560 | `remaining-accessible` |
| `customer_support_faq_type` | TABLE | ~36 | `remaining-accessible` |
| `customer_support_handler` | TABLE | ~206 | `remaining-accessible` |
| `customer_support_sub_type` | TABLE | ~330 | `remaining-accessible` |
| `customer_support_type` | TABLE | ~62 | `remaining-accessible` |
| `customer_support_type_list` | VIEW | < 1 | `views` |
| `customer_tam` | TABLE | ~193 | `remaining-accessible` |
| `customers` | TABLE | ~25,182 | `customer-core` |
| `customers_attributes` | TABLE | ~127,364 | `remaining-accessible` |
| `customers_attributes_history` | TABLE | ~485,984 | `remaining-accessible` |
| `customers_priority` | TABLE | ~4 | `remaining-accessible` |
| `database_errors` | TABLE | ~824,313 | `remaining-accessible` |
| `databasechangelog` | TABLE | ~184 | `remaining-accessible` |
| `databasechangeloglock` | TABLE | ~1 | `remaining-accessible` |
| `datacenter_attributes` | TABLE | ~248 | `infrastructure` |
| `datacenter_available_currencies` | TABLE | ~73 | `infrastructure` |
| `email_recipients` | TABLE | ~245 | `remaining-accessible` |
| `email_template_groupings` | TABLE | ~119 | `remaining-accessible` |
| `email_template_groups` | TABLE | ~5 | `remaining-accessible` |
| `email_templates` | TABLE | ~238 | `remaining-accessible` |
| `employee_client_relations_quotas` | TABLE | ~192 | `people-org` |
| `employee_client_relations_roles_matrix` | TABLE | ~103 | `people-org` |
| `employee_client_relations_roles_product_line_independent_matrix` | TABLE | ~4 | `products-services` |
| `employees` | TABLE | ~5,327 | `people-org` |
| `error_status_types` | TABLE | ~2 | `remaining-accessible` |
| `error_statuses` | TABLE | ~2 | `remaining-accessible` |
| `eula` | TABLE | ~5 | `remaining-accessible` |
| `exchange_rates` | TABLE | ~15 | `billing-finance` |
| `fraud_gateway_transactions` | TABLE | ~45,577 | `remaining-accessible` |
| `history_certificate` | TABLE | ~31,373 | `remaining-accessible` |
| `history_client_bag_services` | TABLE | ~323,986 | `products-services` |
| `history_client_bags` | TABLE | ~630,079 | `remaining-accessible` |
| `history_client_orders` | TABLE | ~9,355,367 | `remaining-accessible` |
| `history_client_payment_methods` | TABLE | ~488,274 | `billing-finance` |
| `history_client_permission_roles` | TABLE | ~10,051,468 | `people-org` |
| `history_client_permission_users` | TABLE | ~6,144 | `people-org` |
| `history_client_private_net` | TABLE | ~4,198 | `remaining-accessible` |
| `history_client_private_rack` | TABLE | ~313 | `infrastructure` |
| `history_client_solution_services` | TABLE | ~661,702 | `products-services` |
| `history_client_solutions` | TABLE | ~59,510 | `remaining-accessible` |
| `history_client_zones` | TABLE | ~527,243 | `remaining-accessible` |
| `history_components` | TABLE | ~30,101 | `products-services` |
| `history_contact` | TABLE | ~387,329 | `people-org` |
| `history_contact_communication_method` | TABLE | ~1,081,046 | `people-org` |
| `history_contact_role` | TABLE | ~651,681 | `people-org` |
| `history_customer_products` | TABLE | ~311,633,536 | `customer-core` |
| `history_customers` | TABLE | ~244,134 | `remaining-accessible` |
| `history_email_recipients` | TABLE | ~3,695 | `remaining-accessible` |
| `history_email_templates` | TABLE | ~2,006 | `remaining-accessible` |
| `history_exchange_rates` | TABLE | ~320 | `billing-finance` |
| `history_ocean_restrictions` | TABLE | ~802 | `remaining-accessible` |
| `history_permission_categories` | TABLE | ~12 | `remaining-accessible` |
| `history_permissions` | TABLE | ~136 | `remaining-accessible` |
| `history_preconfigured_bundle_mapping` | TABLE | ~220 | `remaining-accessible` |
| `history_pricebook` | TABLE | ~93,467 | `remaining-accessible` |
| `history_product_allowed_components` | TABLE | ~483,025 | `products-services` |
| `history_product_catalog` | TABLE | ~8,879 | `products-services` |
| `history_service_billing_details` | TABLE | ~638,528 | `billing-finance` |
| `history_service_inventory_unavailable` | TABLE | ~504 | `products-services` |
| `history_service_options` | TABLE | ~6,127,824 | `products-services` |
| `history_tax_rates` | TABLE | ~111 | `billing-finance` |
| `history_template_permission_roles` | TABLE | ~406 | `people-org` |
| `history_ticket_support_times` | TABLE | ~2,038,556 | `remaining-accessible` |
| `history_volume_discount_percentage` | TABLE | ~38 | `remaining-accessible` |
| `history_workflow_notifications` | TABLE | ~66,573 | `remaining-accessible` |
| `history_xref_customer_products_dcc` | TABLE | ~371,492 | `products-services` |
| `history_xref_services_private_net` | TABLE | ~27,011 | `products-services` |
| `history_xref_services_private_rack` | TABLE | ~5,746 | `products-services` |
| `intergovernmental_organizations` | TABLE | ~3 | `remaining-accessible` |
| `item_tax_schedule` | TABLE | ~5,756 | `remaining-accessible` |
| `kickstart_component_keys` | TABLE | ~1,234 | `products-services` |
| `license_types` | TABLE | ~8 | `remaining-accessible` |
| `line_sequence_mapping` | TABLE | ~46,429 | `remaining-accessible` |
| `login_history` | TABLE | ~3,808,951 | `remaining-accessible` |
| `message_box` | TABLE | ~1,695,041 | `remaining-accessible` |
| `mon_runbook_custom_notes` | TABLE | ~169 | `remaining-accessible` |
| `mon_runbook_default_notes` | TABLE | ~61 | `remaining-accessible` |
| `my_rbac_pages` | TABLE | ~263 | `remaining-accessible` |
| `my_rbac_sections` | TABLE | ~15 | `remaining-accessible` |
| `nbt_invoices` | TABLE | ~5,317 | `billing-finance` |
| `node_types` | TABLE | ~2 | `remaining-accessible` |
| `ocean_config` | TABLE | ~2 | `remaining-accessible` |
| `ocean_restrictions` | TABLE | ~269 | `remaining-accessible` |
| `ocean_sessions` | TABLE | ~7,246 | `remaining-accessible` |
| `olid_service_option_link` | TABLE | ~263,880 | `products-services` |
| `options_licenses` | TABLE | ~5,917 | `remaining-accessible` |
| `order_commission_split` | TABLE | ~69,202 | `remaining-accessible` |
| `order_communications` | TABLE | ~40,626 | `remaining-accessible` |
| `order_entry_solution_link` | TABLE | ~12,572 | `remaining-accessible` |
| `order_entry_solution_node` | TABLE | ~11,333 | `remaining-accessible` |
| `order_line_item_attributes` | TABLE | ~98,941 | `remaining-accessible` |
| `order_line_item_detail_attributes` | TABLE | ~449,045 | `remaining-accessible` |
| `order_line_item_detail_workorder_tickets` | TABLE | ~11,366 | `remaining-accessible` |
| `order_line_item_details` | TABLE | ~5,390,359 | `remaining-accessible` |
| `order_line_item_details_removed` | TABLE | ❌ | `inaccessible` |
| `order_line_item_migrated_services` | TABLE | ~27,850 | `billing-finance` |
| `order_line_item_types` | TABLE | ~4 | `remaining-accessible` |
| `order_line_item_workorder_tickets` | TABLE | ~4,734 | `remaining-accessible` |
| `order_line_items` | TABLE | ~375,211 | `remaining-accessible` |
| `order_notes` | TABLE | < 1 | `remaining-accessible` |
| `order_status_audit` | TABLE | ❌ | `inaccessible` |
| `overage_report` | TABLE | ❌ | `inaccessible` |
| `overage_report_custom` | TABLE | ❌ | `inaccessible` |
| `overage_report_new_sflow_servers` | TABLE | ❌ | `infrastructure` |
| `p1_zones` | TABLE | ~395 | `remaining-accessible` |
| `package` | TABLE | < 1 | `remaining-accessible` |
| `partition_details` | TABLE | ~55,051 | `remaining-accessible` |
| `partition_object_types` | TABLE | ~2 | `remaining-accessible` |
| `partitions` | TABLE | ~18,146 | `remaining-accessible` |
| `payment_gateway_providers` | TABLE | ~3 | `billing-finance` |
| `payment_gateway_transaction_log_details` | TABLE | ~28 | `billing-finance` |
| `payment_gateway_transaction_logs` | TABLE | ~14 | `billing-finance` |
| `payment_merchant_accounts` | TABLE | ~25 | `billing-finance` |
| `payment_terms` | TABLE | ~11 | `billing-finance` |
| `payment_transaction_documents` | TABLE | ~2,185,546 | `billing-finance` |
| `payment_transactions` | TABLE | ~2,081,949 | `billing-finance` |
| `payment_transactions_paypal` | TABLE | < 1 | `billing-finance` |
| `payment_types` | TABLE | ~6 | `billing-finance` |
| `permission_categories` | TABLE | ~4 | `remaining-accessible` |
| `permissions` | TABLE | ~58 | `remaining-accessible` |
| `portal_login` | TABLE | ~204,312 | `remaining-accessible` |
| `preconfigured_bundle_categories` | TABLE | ~6 | `remaining-accessible` |
| `preconfigured_bundle_mapping` | TABLE | ~216 | `remaining-accessible` |
| `pricebook` | TABLE | ~43,198 | `remaining-accessible` |
| `product_allowed_components` | TABLE | ~233,576 | `products-services` |
| `product_catalog` | TABLE | ~1,148 | `products-services` |
| `product_catalog_attributes` | TABLE | ~228 | `products-services` |
| `product_catalog_tags` | TABLE | ❌ | `products-services` |
| `product_categories` | TABLE | ~10 | `products-services` |
| `product_class_client_type_discounts` | TABLE | ~1,857 | `products-services` |
| `product_class_contract_length_discounts` | TABLE | ~918 | `products-services` |
| `product_classes` | TABLE | ~20 | `products-services` |
| `product_configuration_changesets` | TABLE | ~689 | `products-services` |
| `product_configurations` | TABLE | ~72 | `products-services` |
| `product_frameworks` | TABLE | ~23,482 | `products-services` |
| `product_lines` | TABLE | ~8 | `products-services` |
| `product_templates` | TABLE | ~4,539 | `products-services` |
| `promotion_component_criteria` | TABLE | ~2 | `products-services` |
| `promotion_component_type_criteria` | TABLE | ~1 | `products-services` |
| `promotion_component_types` | TABLE | ~5 | `products-services` |
| `promotion_contract_length_criteria` | TABLE | ~2 | `remaining-accessible` |
| `promotion_criteria_types` | TABLE | ~7 | `remaining-accessible` |
| `promotion_customer_type_criteria` | TABLE | ~10 | `remaining-accessible` |
| `promotion_effect_amounts` | TABLE | ~2,094 | `remaining-accessible` |
| `promotion_effect_component_criteria` | TABLE | ~3 | `products-services` |
| `promotion_effect_component_type_criteria` | TABLE | < 1 | `products-services` |
| `promotion_effect_product_class_criteria` | TABLE | < 1 | `products-services` |
| `promotion_effect_product_criteria` | TABLE | < 1 | `products-services` |
| `promotion_effect_target_amount_types` | TABLE | ~3 | `remaining-accessible` |
| `promotion_effect_target_types` | TABLE | ~3 | `remaining-accessible` |
| `promotion_effect_types` | TABLE | ~4 | `remaining-accessible` |
| `promotion_effects` | TABLE | ~1,411 | `remaining-accessible` |
| `promotion_location_criteria` | TABLE | ~42 | `remaining-accessible` |
| `promotion_product_class_criteria` | TABLE | ~20 | `products-services` |
| `promotion_product_classes` | TABLE | ~98 | `products-services` |
| `promotion_product_criteria` | TABLE | ~42 | `products-services` |
| `promotion_types` | TABLE | ~2 | `remaining-accessible` |
| `promotions` | TABLE | ~155 | `remaining-accessible` |
| `provisioning_tickets` | TABLE | ~5,216 | `remaining-accessible` |
| `queue_messages` | TABLE | ~1,792,446 | `remaining-accessible` |
| `queues` | TABLE | ~68 | `remaining-accessible` |
| `raid_levels` | TABLE | ~11 | `remaining-accessible` |
| `resource_use_operators` | TABLE | ~6 | `remaining-accessible` |
| `resource_use_types` | TABLE | ~2 | `remaining-accessible` |
| `resources` | TABLE | ~35 | `remaining-accessible` |
| `roles` | TABLE | ~23,143 | `people-org` |
| `rss_feed_spotlight` | TABLE | < 1 | `remaining-accessible` |
| `rss_feeds` | TABLE | < 1 | `remaining-accessible` |
| `sb_customer_log` | TABLE | ~6,316,303 | `remaining-accessible` |
| `sb_customer_product_log` | TABLE | ~9,703,099 | `products-services` |
| `sb_datacenter` | TABLE | ~54 | `infrastructure` |
| `sb_log_type` | TABLE | ~16 | `remaining-accessible` |
| `secret_questions_pl` | TABLE | ~5 | `remaining-accessible` |
| `service_account` | TABLE | < 1 | `products-services` |
| `service_billing_details` | TABLE | ~162,715 | `billing-finance` |
| `service_cancellation_queue` | TABLE | ~189 | `products-services` |
| `service_inventory_unavailable` | TABLE | ~312 | `products-services` |
| `service_licenses` | TABLE | ~1,158 | `products-services` |
| `service_notes` | TABLE | ~295,267 | `products-services` |
| `service_option_raid_arrays` | TABLE | ~42,594 | `products-services` |
| `service_option_raid_configuration` | TABLE | ~103,935 | `products-services` |
| `service_option_types_pl` | TABLE | ~51 | `products-services` |
| `service_options` | TABLE | ~1,850,910 | `products-services` |
| `service_options_attributes` | TABLE | ~9,363 | `products-services` |
| `service_options_mercury_services` | TABLE | ~1,646 | `products-services` |
| `service_type_capabilities` | TABLE | ~6 | `products-services` |
| `service_type_pl` | TABLE | ~22 | `products-services` |
| `service_workflow_matrix` | TABLE | ~351 | `products-services` |
| `sessions` | TABLE | ~3,156 | `remaining-accessible` |
| `solution_connection_property_types` | TABLE | ~3 | `remaining-accessible` |
| `solution_service_connection_properties` | TABLE | < 1 | `products-services` |
| `solution_service_connections` | TABLE | ~4,473 | `products-services` |
| `tags` | TABLE | ❌ | `inaccessible` |
| `task_status_pl` | TABLE | ~6 | `remaining-accessible` |
| `tax_rates` | TABLE | ~45 | `billing-finance` |
| `tax_registration_types` | TABLE | ~3 | `remaining-accessible` |
| `template_permission_roles` | TABLE | ~186 | `people-org` |
| `ticket_support_time_types` | TABLE | ~4 | `remaining-accessible` |
| `ticket_support_times` | TABLE | ~2,038,533 | `remaining-accessible` |
| `tls_workorder_templates` | TABLE | ~22 | `remaining-accessible` |
| `transactions_pending_client_approval` | TABLE | < 1 | `remaining-accessible` |
| `unit_of_measure` | TABLE | ~30 | `remaining-accessible` |
| `vam_admin_account` | TABLE | ~973 | `remaining-accessible` |
| `vam_agent` | TABLE | ~2,786 | `remaining-accessible` |
| `vam_agent_account` | TABLE | ~2,896 | `remaining-accessible` |
| `vam_billing_account` | TABLE | ~976 | `billing-finance` |
| `vam_cache` | TABLE | ~11,623 | `remaining-accessible` |
| `vam_client` | TABLE | ~979 | `remaining-accessible` |
| `vam_configuration` | TABLE | ~2,786 | `remaining-accessible` |
| `vam_escalation_definition` | TABLE | ~2,785 | `remaining-accessible` |
| `vam_host` | TABLE | ~2,908 | `infrastructure` |
| `vam_resources` | TABLE | ~12 | `remaining-accessible` |
| `view_active_pricebook` | VIEW | < 1 | `views` |
| `view_active_promotions` | VIEW | < 1 | `views` |
| `view_attribute_groups` | VIEW | < 1 | `views` |
| `view_client_bag_services` | VIEW | < 1 | `views` |
| `view_client_bags` | VIEW | < 1 | `views` |
| `view_client_bandwidth_allowance` | VIEW | < 1 | `views` |
| `view_client_bandwidth_allowance_by_bag` | VIEW | < 1 | `views` |
| `view_client_bandwidth_allowance_by_datacenter` | VIEW | < 1 | `views` |
| `view_client_bandwidth_allowance_by_service` | VIEW | < 1 | `views` |
| `view_client_contact_roles` | VIEW | < 1 | `views` |
| `view_client_contacts` | VIEW | < 1 | `views` |
| `view_client_error_statuses` | VIEW | < 1 | `views` |
| `view_client_events` | VIEW | < 1 | `views` |
| `view_client_orders` | VIEW | < 1 | `views` |
| `view_client_payment_methods` | VIEW | < 1 | `views` |
| `view_client_relations` | VIEW | < 1 | `views` |
| `view_client_service_options` | VIEW | < 1 | `views` |
| `view_client_services` | VIEW | < 1 | `views` |
| `view_client_solution_services` | VIEW | < 1 | `views` |
| `view_client_solutions` | VIEW | < 1 | `views` |
| `view_client_tax_registration` | VIEW | < 1 | `views` |
| `view_client_types` | VIEW | < 1 | `views` |
| `view_clients` | VIEW | < 1 | `views` |
| `view_clients_watchers` | VIEW | < 1 | `views` |
| `view_cloud_storage_tiered_discounts` | VIEW | < 1 | `views` |
| `view_component_capabilities` | VIEW | < 1 | `views` |
| `view_component_license_keys` | VIEW | < 1 | `views` |
| `view_component_provided_resources` | VIEW | < 1 | `views` |
| `view_component_required_resources` | VIEW | < 1 | `views` |
| `view_component_type_capabilities` | VIEW | < 1 | `views` |
| `view_component_types` | VIEW | < 1 | `views` |
| `view_components` | VIEW | < 1 | `views` |
| `view_contract_types` | VIEW | < 1 | `views` |
| `view_control_scan_ip_addresses` | VIEW | < 1 | `views` |
| `view_countries_intergovernmental_organizations` | VIEW | < 1 | `views` |
| `view_customer_support_faq` | VIEW | < 1 | `views` |
| `view_customer_support_faq_product_lines` | VIEW | < 1 | `views` |
| `view_customers_attributes` | VIEW | < 1 | `views` |
| `view_customers_controlscan_credentials` | VIEW | < 1 | `views` |
| `view_employee_client_relations_roles_matrix` | VIEW | < 1 | `views` |
| `view_employee_roles` | VIEW | < 1 | `views` |
| `view_employee_username` | VIEW | < 1 | `views` |
| `view_item_tax_schedule` | VIEW | < 1 | `views` |
| `view_multicurrency_pricebook` | VIEW | < 1 | `views` |
| `view_oc_cart` | VIEW | < 1 | `views` |
| `view_oc_cart_components` | VIEW | < 1 | `views` |
| `view_oc_cart_default_removed_components` | VIEW | < 1 | `views` |
| `view_order_commission_split` | VIEW | < 1 | `views` |
| `view_order_entry_solution_details` | VIEW | < 1 | `views` |
| `view_order_line_item_details` | VIEW | ❌ | `views` |
| `view_order_line_items` | VIEW | ❌ | `views` |
| `view_payment_transactions` | VIEW | ❌ | `views` |
| `view_preconfigured_bundle_mapping` | VIEW | < 1 | `views` |
| `view_pricebook` | VIEW | < 1 | `views` |
| `view_product_allowed_components` | VIEW | < 1 | `views` |
| `view_product_catalog` | VIEW | < 1 | `views` |
| `view_product_frameworks` | VIEW | < 1 | `views` |
| `view_product_templates` | VIEW | < 1 | `views` |
| `view_promotion_criteria_details` | VIEW | < 1 | `views` |
| `view_promotion_effect_criteria_details` | VIEW | < 1 | `views` |
| `view_promotion_effects_details` | VIEW | < 1 | `views` |
| `view_queue_messages` | VIEW | < 1 | `views` |
| `view_resources` | VIEW | < 1 | `views` |
| `view_service_cancellation_queue` | VIEW | < 1 | `views` |
| `view_service_events` | VIEW | < 1 | `views` |
| `view_service_option_raid_configuration` | VIEW | < 1 | `views` |
| `view_service_options_capacity_as_gb` | VIEW | < 1 | `views` |
| `view_service_payment_methods` | VIEW | < 1 | `views` |
| `view_service_workflow_matrix` | VIEW | < 1 | `views` |
| `view_services_without_device` | VIEW | < 1 | `views` |
| `view_statistics_orders` | VIEW | < 1 | `views` |
| `view_statistics_orders_by_status` | VIEW | < 1 | `views` |
| `view_statistics_services` | VIEW | < 1 | `views` |
| `view_statistics_services_by_datacenter` | VIEW | < 1 | `views` |
| `view_statistics_services_by_status` | VIEW | < 1 | `views` |
| `view_statistics_services_by_type` | VIEW | < 1 | `views` |
| `view_ticket_routing_by_product_line` | VIEW | < 1 | `views` |
| `view_xref_cloud_storage_policy_component` | VIEW | < 1 | `views` |
| `view_xref_cloud_storage_policy_concession` | VIEW | < 1 | `views` |
| `vmware_clusters` | TABLE | ~418 | `remaining-accessible` |
| `vmware_guests` | TABLE | ~4,374 | `remaining-accessible` |
| `vmware_hosts` | TABLE | ~1,056 | `infrastructure` |
| `vmware_vcenters` | TABLE | ~497 | `remaining-accessible` |
| `volume_discount_percentage` | TABLE | ~20 | `remaining-accessible` |
| `wallet_responses_pl` | TABLE | ~20 | `remaining-accessible` |
| `web_server_types` | TABLE | ~27 | `infrastructure` |
| `widget_input_parameters` | TABLE | ~321 | `remaining-accessible` |
| `widget_output_parameters` | TABLE | ~357 | `remaining-accessible` |
| `widget_transaction_states` | TABLE | < 1 | `remaining-accessible` |
| `widget_types_pl` | TABLE | ~42 | `remaining-accessible` |
| `widgets` | TABLE | ~187 | `remaining-accessible` |
| `workflow_event_types` | TABLE | ~16 | `remaining-accessible` |
| `workflow_notifications` | TABLE | < 1 | `remaining-accessible` |
| `xref_cloud_storage_policy_component` | TABLE | ~10 | `products-services` |
| `xref_cloud_storage_policy_concession` | TABLE | ~1 | `remaining-accessible` |
| `xref_cloud_storage_subtenants_services` | TABLE | ~1,111 | `products-services` |
| `xref_customer_products_dcc` | TABLE | ~162,726 | `products-services` |
| `xref_customer_rbac_roles` | TABLE | ~1,090,638 | `people-org` |
| `xref_customer_support_type_sub_type` | TABLE | ~435 | `remaining-accessible` |
| `xref_rbac_pages_to_sections` | TABLE | ~218 | `remaining-accessible` |
| `xref_roles_employees` | TABLE | ~10,984 | `people-org` |
| `xref_services_private_net` | TABLE | ~20,089 | `products-services` |
| `xref_services_private_rack` | TABLE | ~3,584 | `products-services` |
| `xref_ticket_routing_by_product_line` | TABLE | ~713 | `products-services` |
| `zones` | TABLE | ~736 | `remaining-accessible` |
