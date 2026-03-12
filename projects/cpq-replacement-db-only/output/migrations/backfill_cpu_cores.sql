-- Migration: backfill NULL cores/threads in component_specs
-- Source: 07_component_specs.csv + SKU name parsing
-- Affected products: Intel Xeon Gold 6526Y (default + non-default),
--                    Intel Xeon Gold 6326, Default Intel Xeon 6517P

UPDATE component_specs
SET cores = 16,
    threads = 32
WHERE product_id IN (
    SELECT id
    FROM product_catalog
    WHERE sku_name IN (
        'Intel Xeon Gold 6526Y 2.9G, 16/32T',
        'Default Intel Xeon Gold 6526Y 2.9G, 16/32T'
    )
);

UPDATE component_specs
SET cores = 16,
    threads = 32
WHERE product_id = (
    SELECT id
    FROM product_catalog
    WHERE sku_name = 'Intel Xeon Gold 6326 2.9GHz 16 Cores/32T'
);

UPDATE component_specs
SET cores = 16,
    threads = 32
WHERE product_id = (
    SELECT id
    FROM product_catalog
    WHERE sku_name = 'Default Intel Xeon 6517P 16 core'
);

