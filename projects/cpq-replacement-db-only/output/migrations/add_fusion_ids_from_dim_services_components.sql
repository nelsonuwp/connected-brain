-- Migration: Set fusion_id from dimServices (TLS) and dimComponents (components)
-- Source: dimServices_202603031607.csv (product -> fusion_id), dimComponents_202603031607.csv (component -> component_id)
-- Apply after seed_data.sql and seed_data_phase2.sql.
-- Components store the external ID in product_catalog.fusion_id (same column as TLS).

BEGIN;

-- -----------------------------------------------------------------------------
-- COMPONENTS: Set fusion_id = component_id from dimComponents where sku_name matches
-- (Exact match + agreed aliases: dim "16 GB DDR4 RAM - Total" -> our "16 GB DDR4 RAM", etc.)
-- -----------------------------------------------------------------------------

UPDATE product_catalog
SET fusion_id = '3704'
WHERE level = 'Component' AND sku_name = '480 GB SSD';

UPDATE product_catalog
SET fusion_id = '3352'
WHERE level = 'Component' AND sku_name = 'LM Basic Monitoring';

UPDATE product_catalog
SET fusion_id = '3353'
WHERE level = 'Component' AND sku_name = 'LM Standard Monitoring';

-- Alias: dim "16 GB DDR4 RAM - Total" -> our "16 GB DDR4 RAM"
UPDATE product_catalog
SET fusion_id = '3057'
WHERE level = 'Component' AND sku_name = '16 GB DDR4 RAM';

-- Alias: dim "64 GB DDR4 RAM Total (32 GB Included) - Upgrade" -> our "64 GB DDR4 RAM"
UPDATE product_catalog
SET fusion_id = '3137'
WHERE level = 'Component' AND sku_name = '64 GB DDR4 RAM';

-- -----------------------------------------------------------------------------
-- TLS: Set fusion_id from dimServices where product name matches
-- Current seed TLS names (Pro Series 6.0 - M, etc.) do not appear in dimServices;
-- dimServices has legacy names (Pro Series 2.0, Advanced SATA, etc.). No rows updated below.
-- If you add TLS rows that match dimServices product names, they will get fusion_id here.
-- Reference: dimServices product -> fusion_id
--   12 Port Managed Switch -> 145,  8 Port Managed GigE Switch -> 157,
--   Advanced E5v3 - M -> 795,  Advanced SATA -> 356,  Alertlogic IDS Threat Manager 1540 -> 302,
--   Essential E3v5 - M -> 887,  Juniper SSG 5 -> 19,  Managed Load Balancing Service -> 155,
--   Microsoft Cloud -> 911,  Pro Series 2.0 -> 498
-- -----------------------------------------------------------------------------

UPDATE product_catalog SET fusion_id = '19'   WHERE level = 'TLS' AND sku_name = 'Juniper SSG 5';
UPDATE product_catalog SET fusion_id = '155'  WHERE level = 'TLS' AND sku_name = 'Managed Load Balancing Service';
UPDATE product_catalog SET fusion_id = '302'  WHERE level = 'TLS' AND sku_name = 'Alertlogic IDS Threat Manager 1540';
UPDATE product_catalog SET fusion_id = '145'  WHERE level = 'TLS' AND sku_name = '12 Port Managed Switch';
UPDATE product_catalog SET fusion_id = '356'  WHERE level = 'TLS' AND sku_name = 'Advanced SATA';
UPDATE product_catalog SET fusion_id = '157'  WHERE level = 'TLS' AND sku_name = '8 Port Managed GigE Switch';
UPDATE product_catalog SET fusion_id = '498'  WHERE level = 'TLS' AND sku_name = 'Pro Series 2.0';
UPDATE product_catalog SET fusion_id = '887'  WHERE level = 'TLS' AND sku_name = 'Essential E3v5 - M';
UPDATE product_catalog SET fusion_id = '795'  WHERE level = 'TLS' AND sku_name = 'Advanced E5v3 - M';
UPDATE product_catalog SET fusion_id = '911'  WHERE level = 'TLS' AND sku_name = 'Microsoft Cloud';

COMMIT;
