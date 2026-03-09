-- Add product_capex for products that appear in "Products - Hosting.csv" (CapEx to Allocate USD, Residual 12m/24m)
-- but do not yet have a product_capex row. Match by product_catalog.sku_name = CSV "Product SKU".
-- Source: Products - Hosting.csv columns: Product SKU (B), CapEx to Allocate (USD) (AG), Residual 12 Months (AH), Residual 24 Months (AI)
-- Only inserts for products that exist in product_catalog; skips Juniper SRX / 10 GbE Connection if not in catalog.

BEGIN;

-- Intel Xeon Gold 6526Y 2.9G, 16/32T — CapEx $1,725, 50% / 20%
INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 1725.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Intel Xeon Gold 6526Y 2.9G, 16/32T'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

-- Default Intel Xeon Gold 6526Y 2.9G, 16/32T — same
INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 1725.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Default Intel Xeon Gold 6526Y 2.9G, 16/32T'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

-- 750W Redundant Power Supply — $150, 50% / 20%
INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 150.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = '750W Redundant Power Supply'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

-- Intel X710-DA2 10 GbE NIC with 2 x SFP+ — $295
INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 295.0, 'USD', '2024-01-01', true, NULL, NULL, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Intel X710-DA2 10 GbE NIC with 2 x SFP+'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

-- Intel X710 Quad Port 10Gb DA/SFP+ Ethernet, NDC — $530
INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 530.0, 'USD', '2024-01-01', true, NULL, NULL, 'Products - Hosting.csv CapEx to Allocate (USD)'
FROM product_catalog
WHERE sku_name = 'Intel X710 Quad Port 10Gb DA/SFP+ Ethernet, NDC'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);

COMMIT;
