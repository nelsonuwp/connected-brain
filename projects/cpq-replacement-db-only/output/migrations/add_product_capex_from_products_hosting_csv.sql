-- Add product_capex from Products - Hosting.csv (CapEx to Allocate USD, Residual 12m/24m)
-- Source: Products - Hosting.csv
-- Only for products in product_catalog that do not already have a product_capex row.

BEGIN;

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 160.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Intel Xeon Bronze 3106 1.7 GHz 8 Cores/8T'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 160.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Default Xeon Bronze 3106 1.7 GHz 8 Cores/8T'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 200.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Intel Xeon Silver 4110 2.1 GHz 8 Cores/16T'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 1300.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Intel Xeon Gold 5118 2.3 GHz 12 Cores/24T'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 1300.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Default Xeon Gold 5118 2.3 GHz 12 Cores/24T'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 1100.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Intel Xeon Gold 5122 3.6 GHz 4 Cores/8T (MTO)'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 1600.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Intel Xeon Gold 6130 2.1 GHz 16 Cores/32T (MTO)'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 1800.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Intel Xeon Gold 6138 2.0 GHz 20 Cores/40T (MTO)'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 890.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Intel Xeon Silver 4514Y 2G, 16C/32T'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 890.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Default Intel Xeon Silver 4514Y 2G, 16C/32T'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 3190.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Intel Xeon Gold 6534 4G, 8C/16T'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 1725.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Intel Xeon Gold 6526Y 2.9G, 16/32T'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 1725.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Default Intel Xeon Gold 6526Y 2.9G, 16/32T'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 4220.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Intel Xeon Gold 6548Y+ 2.5G, 32C/64T'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 4215.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Intel Xeon Platinum 8558U 2G, 48C/96T'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 160.0, 'USD', '2024-01-01', true, NULL, NULL, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '16 GB DDR4 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 320.0, 'USD', '2024-01-01', true, NULL, NULL, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '32 GB DDR4 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 640.0, 'USD', '2024-01-01', true, NULL, NULL, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '64 GB DDR4 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 960.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '96 GB DDR4 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 1280.0, 'USD', '2024-01-01', true, NULL, NULL, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '128 GB DDR4 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 1920.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '192 GB DDR4 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 2560.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '256 GB DDR4 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 3840.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '384 GB DDR4 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 5120.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '512 GB DDR4 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 7680.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '768 GB DDR4 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 15360.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '1536 GB DDR4 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 67.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '16 GB DDR5 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 107.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '32 GB DDR5 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 268.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '64 GB DDR5 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 536.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '128 GB DDR5 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 804.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '192 GB DDR5 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 856.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '256 GB DDR5 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 1284.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '384 GB DDR5 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 1768.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '512 GB DDR5 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 2652.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '768 GB DDR5 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 3536.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '1024 GB DDR5 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 5304.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '1536 GB DDR5 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 7072.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '2048 GB DDR5 RAM'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 80.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '1 TB 7200 6 Gb/s SATA'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 145.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '2 TB 7200 6 Gb/s SATA'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 180.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '4 TB 7200 6 Gb/s SATA'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 300.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '12 TB 7200 6 Gb/s SATA'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 85.0, 'USD', '2024-01-01', true, 0.0, 0.0, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '480 GB SSD'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 149.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '480 GB SATA 2.5in SSD'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 185.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '960 GB SATA 2.5in SSD'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 379.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '3.84 TB SATA 2.5in SSD'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 430.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '7.6 TB Micron 9400 SSD'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 300.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '960 GB NVMe u.2 2.5in'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 680.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '3.84 TB NVMe u.2 2.5in'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 1260.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '6.4 TB NVMe u.2 2.5in'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 2100.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '15.36 TB NVMe u.2 2.5in'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 150.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '750W Redundant Power Supply'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 295.0, 'USD', '2024-01-01', true, NULL, NULL, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Intel X710-DA2 10 GbE NIC with 2 x SFP+'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 530.0, 'USD', '2024-01-01', true, NULL, NULL, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Intel X710 Quad Port 10Gb DA/SFP+ Ethernet, NDC'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

COMMIT;
