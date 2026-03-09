# Fusion ID mapping from dimProductAttributes

**Source:** `dimProductAttributes_202603080743.csv` — columns `fusion_id`, `sku_name`, `level` (TLS or Component). One file for both TLS and components; match on `sku_name` and set `product_catalog.fusion_id`.

## Applied in migration

**`output/migrations/add_fusion_ids_from_dim_services_components.sql`**

- **Exact match:** TLS and Components whose `sku_name` appears in dimProductAttributes (5 TLS, 53 Components).
- **Aliases:** Seed names that differ from CSV (e.g. "32 GB DDR4 RAM" vs "32 GB DDR4 RAM - Total", "1 pack - Windows Remote Desktop..." vs "1 Windows Remote Desktop Service  SAL", strip " - M" for server names). Covers RAM, Windows RDS packs, CPUs, SQL/Windows Server, RHEL, Tivoli Toronto variants, drives, OS (Debian, Ubuntu), VMware ESXi 8.x, Proxmox VE License, Default CPUs, etc.
- **Total:** 12 TLS and ~120+ Component rows updated. Remaining NULL: Promo Server - NA/UK (TEMP placeholders), plus a few components not present in dimProductAttributes (e.g. CentOS 8, some NVMe/CPU variants, VMWare ESXi 7.x, Veeam - Local/Offsite, Single Power Supply, Dual PSUs) — add manually if you have a mapping.

## Regenerating from dimProductAttributes

1. Place `dimProductAttributes_YYYYMMDDHHMMSS.csv` (with columns `fusion_id`, `sku_name`, `level`) in Downloads or set path in script.
2. Run a script that: loads the CSV; extracts seed TLS sku_names from `seed_data.sql` and Component sku_names from `seed_data_phase2.sql`; for each match, emit `UPDATE product_catalog SET fusion_id = '<fusion_id>' WHERE level = '<TLS|Component>' AND sku_name = '<sku_name>';`
3. Replace the migration body or append new UPDATEs.

## Adding more IDs

Match `product_catalog.sku_name` to `dimProductAttributes.sku_name` (exact). Add an `UPDATE product_catalog SET fusion_id = '<fusion_id>' WHERE level = '...' AND sku_name = '<sku_name>';` to the migration or a new migration.
