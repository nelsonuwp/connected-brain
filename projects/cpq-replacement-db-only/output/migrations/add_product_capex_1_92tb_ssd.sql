-- Add product_capex for 1.92 TB SATA 2.5in SSD (Products - Hosting.csv col AG, row 193 = $349)
INSERT INTO product_capex (product_id, procured_price, procured_currency, procured_date, use_as_baseline, residual_pct_12m, residual_pct_24m, notes)
SELECT id, 349.0, 'USD', '2024-01-01', true, 0.5, 0.2, 'Products - Hosting.csv col AG (CapEx to Allocate USD)'
FROM product_catalog
WHERE sku_name = '1.92 TB SATA 2.5in SSD'
  AND NOT EXISTS (SELECT 1 FROM product_capex pc WHERE pc.product_id = product_catalog.id);
