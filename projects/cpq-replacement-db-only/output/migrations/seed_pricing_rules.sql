-- Migration: seed pricing_rules for core-driven products
-- Run AFTER create_pricing_rules.sql

-- VMware License: per licensed core
INSERT INTO pricing_rules (product_id, cost_driver, min_units_per_socket, min_units_per_server, unit_increment, mrc_represents, notes)
SELECT id, 'licensed_cores', 16, NULL, 2, 'per_unit',
       'VMware: min 16 cores/socket, round up to 2. MRC = price_per_core x licensed_cores. Source: CPQ v28 Configurator-Hosting rows 17-20.'
FROM product_catalog
WHERE sku_name = 'VMWare License'
ON CONFLICT (product_id) DO NOTHING;

-- SQL Server editions: per 2-core pack, raw cores
INSERT INTO pricing_rules (product_id, cost_driver, min_units_per_socket, min_units_per_server, unit_increment, mrc_represents, notes)
SELECT id, 'raw_cores', 4, NULL, 2, 'per_pack',
       'MS SQL: min 4 cores/socket, sold in 2-core packs. MRC = price_per_pack x packs.'
FROM product_catalog
WHERE sku_name IN (
    'SQL Server 2022 Standard Edition',
    'SQL Server 2022 Enterprise Edition',
    'SQL Server 2019 Standard Edition',
    'SQL Server 2019 Enterprise Edition',
    'SQL Server 2019 Web Edition'
)
ON CONFLICT (product_id) DO NOTHING;

-- Windows Server Standard editions: per 2-core pack
INSERT INTO pricing_rules (product_id, cost_driver, min_units_per_socket, min_units_per_server, unit_increment, mrc_represents, notes)
SELECT id, 'core_packs', 8, 16, 2, 'per_pack',
       'Windows Server Standard: min 8/socket, min 16/server, 2-core packs.'
FROM product_catalog
WHERE sku_name IN (
    'Windows Server 2025 Standard Edition',
    'Windows Server 2022 Standard Edition',
    'Windows Server 2019 Standard Edition'
)
ON CONFLICT (product_id) DO NOTHING;

-- Windows Server Data Center editions: per 2-core pack
INSERT INTO pricing_rules (product_id, cost_driver, min_units_per_socket, min_units_per_server, unit_increment, mrc_represents, notes)
SELECT id, 'core_packs', 8, 16, 2, 'per_pack',
       'Windows Server DC: min 8/socket, min 16/server, 2-core packs.'
FROM product_catalog
WHERE sku_name IN (
    'Windows Server 2025 Data Center Edition',
    'Windows Server 2022 Data Center Edition',
    'Windows Server 2019 Data Center Edition'
)
ON CONFLICT (product_id) DO NOTHING;

-- RHEL for VMs tiered products: per vCPU
INSERT INTO pricing_rules (product_id, cost_driver, min_units_per_socket, min_units_per_server, unit_increment, mrc_represents, notes)
SELECT id, 'vcpu_count', NULL, NULL, 1, 'per_tier_unit',
       'RHEL for VMs: MRC is per-vCPU at the selected tier. Source: 06_software_licenses.csv notes.'
FROM product_catalog
WHERE sku_name IN (
    'RHEL for VMs - 1 to 8 vCPUs',
    'RHEL for VMs - 9 to 127 vCPUs',
    'RHEL for VMs - 128 to Unlimited vCPUs'
)
ON CONFLICT (product_id) DO NOTHING;

-- Mark core-driven products as per_core pricing model
UPDATE product_pricing
SET pricing_model = 'per_core'
WHERE product_id IN (SELECT product_id FROM pricing_rules WHERE cost_driver <> 'flat');

