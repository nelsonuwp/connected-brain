# Fusion ID / Component ID mapping from dimServices and dimComponents

**Sources:** `dimServices_202603031607.csv` (TLS: `product` → `fusion_id`), `dimComponents_202603031607.csv` (components: `component` → `component_id`).

- **TLS (top-level):** Use `fusion_id` from dimServices. Current seed TLS names (e.g. Pro Series 6.0 - M) come from CPQ v28 and do not match dimServices product names; dimServices has legacy names (Pro Series 2.0, Advanced SATA, etc.). The migration still applies updates for any TLS whose `sku_name` matches a dimServices product.
- **Components:** Use `component_id` from dimComponents; stored in `product_catalog.fusion_id` for Components.

## Applied in migration

- **Components (5 rows):** Exact match or alias → `fusion_id` set.
  - `480 GB SSD` → 3704  
  - `LM Basic Monitoring` → 3352  
  - `LM Standard Monitoring` → 3353  
  - `16 GB DDR4 RAM` → 3057 (alias from "16 GB DDR4 RAM - Total")  
  - `64 GB DDR4 RAM` → 3137 (alias from "64 GB DDR4 RAM Total (32 GB Included) - Upgrade")

- **TLS:** Migration includes all 10 dimServices products; only rows with matching `sku_name` are updated (none with current seed).

## Full mapping (for manual aliases or future seed)

- **`output/fusion_mapping_from_dim.json`** — Full `services_product_to_fusion_id` and `components_component_to_component_id` from the CSVs. Use this to add more `UPDATE product_catalog SET fusion_id = ? WHERE level = 'Component' AND sku_name = ?` (or TLS) when you align dim names to seed `sku_name` (e.g. "2 TB 7200 3.5 Inch SATA" → "2 TB 7200 6 Gb/s SATA" if you treat them as same).

## Adding more component IDs

1. Match `product_catalog.sku_name` (Component) to `dimComponents.component` (exact or by alias).
2. Add an `UPDATE product_catalog SET fusion_id = '<component_id>' WHERE level = 'Component' AND sku_name = '<sku_name>';` to the migration (or a new migration).
