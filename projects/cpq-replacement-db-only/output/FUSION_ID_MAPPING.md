# Fusion ID mapping from dimProductAttributes

**Source:** `dimProductAttributes_202603080743.csv` — columns `fusion_id`, `sku_name`, `level` (TLS or Component). One file for both TLS and components; match on `sku_name` and set `product_catalog.fusion_id`.

## Applied in migration

**`output/migrations/add_fusion_ids_from_dim_services_components.sql`**

- **TLS (5 rows):** Pro Series 7.0 → 1290, Pro Series 6.0 vHost → 1259, Advanced Series 6.0 vHost → 1258, Pro Series 5.0 vHost → 944, Advanced Series 5.0 vHost → 959.
- **Components (53 rows):** All seed components whose `sku_name` appears in dimProductAttributes get the corresponding `fusion_id` (e.g. 480 GB SSD → 3704, LM Basic Monitoring → 3352, backup blocks, Tivoli, RHEL/Rocky/Alma, etc.).

## Regenerating from dimProductAttributes

1. Place `dimProductAttributes_YYYYMMDDHHMMSS.csv` (with columns `fusion_id`, `sku_name`, `level`) in Downloads or set path in script.
2. Run a script that: loads the CSV; extracts seed TLS sku_names from `seed_data.sql` and Component sku_names from `seed_data_phase2.sql`; for each match, emit `UPDATE product_catalog SET fusion_id = '<fusion_id>' WHERE level = '<TLS|Component>' AND sku_name = '<sku_name>';`
3. Replace the migration body or append new UPDATEs.

## Adding more IDs

Match `product_catalog.sku_name` to `dimProductAttributes.sku_name` (exact). Add an `UPDATE product_catalog SET fusion_id = '<fusion_id>' WHERE level = '...' AND sku_name = '<sku_name>';` to the migration or a new migration.
