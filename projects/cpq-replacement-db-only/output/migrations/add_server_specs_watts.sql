-- Migration: add server_specs.watts (nameplate watts per CPQ sheet)
-- Run this if your DB was created before watts was added to schema.
-- Then quote overhead will use 400W for Pro 6.0 - M etc. instead of sum of component watts.

ALTER TABLE server_specs ADD COLUMN IF NOT EXISTS watts SMALLINT;

UPDATE server_specs s
SET watts = v.watts
FROM product_catalog pc,
     (VALUES
       ('Pro Series 7.0', 400),
       ('Cluster 5.0 (Dell R440)', 200),
       ('Atomic 5.0 (Dell R650xs)', 300),
       ('Pro Series 6.0 - M', 400),
       ('Pro Series 6.0 vHost', 400),
       ('Advanced Series 6.0 - M', 280),
       ('Advanced Series 6.0 vHost', 280),
       ('Storage Series 6.0 - M', 280),
       ('Essential Series 6.0 - M', 147),
       ('Pro Series 5.0 - M', 224),
       ('Pro Series 5.0 vHost', 224),
       ('Storage Series 5.0 - M', 120),
       ('Storage Series 5.0 vHost', 120),
       ('Advanced Series 5.0 - M', 120),
       ('Advanced Series 5.0 vHost', 120),
       ('Essential Series 5.0 - M', 85),
       ('Promo Server - NA', 224),
       ('Promo Server - UK', 224)
     ) AS v(sku_name, watts)
WHERE s.product_id = pc.id AND pc.sku_name = v.sku_name;
