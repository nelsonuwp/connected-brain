-- Migration: Set fusion_id from dimProductAttributes (sku_name -> fusion_id, level TLS/Component)
-- Source: dimProductAttributes_202603080743.csv
-- Apply after seed_data.sql and seed_data_phase2.sql.

BEGIN;

-- -----------------------------------------------------------------------------
-- TLS (5 matches in dimProductAttributes)
-- -----------------------------------------------------------------------------

UPDATE product_catalog SET fusion_id = '959' WHERE level = 'TLS' AND sku_name = 'Advanced Series 5.0 vHost';
UPDATE product_catalog SET fusion_id = '1258' WHERE level = 'TLS' AND sku_name = 'Advanced Series 6.0 vHost';
UPDATE product_catalog SET fusion_id = '944' WHERE level = 'TLS' AND sku_name = 'Pro Series 5.0 vHost';
UPDATE product_catalog SET fusion_id = '1259' WHERE level = 'TLS' AND sku_name = 'Pro Series 6.0 vHost';
UPDATE product_catalog SET fusion_id = '1290' WHERE level = 'TLS' AND sku_name = 'Pro Series 7.0';

-- -----------------------------------------------------------------------------
-- COMPONENTS (53 matches in dimProductAttributes)
-- -----------------------------------------------------------------------------

UPDATE product_catalog SET fusion_id = '55' WHERE level = 'Component' AND sku_name = '10 GB Backup Blocks';
UPDATE product_catalog SET fusion_id = '385' WHERE level = 'Component' AND sku_name = '100 GB Backup Block';
UPDATE product_catalog SET fusion_id = '395' WHERE level = 'Component' AND sku_name = '1000 GB Backup Block';
UPDATE product_catalog SET fusion_id = '461' WHERE level = 'Component' AND sku_name = '1000 Mbit Connection - GigE';
UPDATE product_catalog SET fusion_id = '397' WHERE level = 'Component' AND sku_name = '1100 GB Backup Block';
UPDATE product_catalog SET fusion_id = '398' WHERE level = 'Component' AND sku_name = '1200 GB Backup Block';
UPDATE product_catalog SET fusion_id = '399' WHERE level = 'Component' AND sku_name = '1300 GB Backup Block';
UPDATE product_catalog SET fusion_id = '400' WHERE level = 'Component' AND sku_name = '1400 GB Backup Block';
UPDATE product_catalog SET fusion_id = '401' WHERE level = 'Component' AND sku_name = '1500 GB Backup Block';
UPDATE product_catalog SET fusion_id = '402' WHERE level = 'Component' AND sku_name = '1600 GB Backup Block';
UPDATE product_catalog SET fusion_id = '403' WHERE level = 'Component' AND sku_name = '1700 GB Backup Block';
UPDATE product_catalog SET fusion_id = '404' WHERE level = 'Component' AND sku_name = '1800 GB Backup Block';
UPDATE product_catalog SET fusion_id = '405' WHERE level = 'Component' AND sku_name = '1900 GB Backup Block';
UPDATE product_catalog SET fusion_id = '386' WHERE level = 'Component' AND sku_name = '200 GB Backup Block';
UPDATE product_catalog SET fusion_id = '396' WHERE level = 'Component' AND sku_name = '2000 GB Backup Block';
UPDATE product_catalog SET fusion_id = '342' WHERE level = 'Component' AND sku_name = '25 GB Backup Blocks';
UPDATE product_catalog SET fusion_id = '387' WHERE level = 'Component' AND sku_name = '300 GB Backup Block';
UPDATE product_catalog SET fusion_id = '388' WHERE level = 'Component' AND sku_name = '400 GB Backup Block';
UPDATE product_catalog SET fusion_id = '3704' WHERE level = 'Component' AND sku_name = '480 GB SSD';
UPDATE product_catalog SET fusion_id = '343' WHERE level = 'Component' AND sku_name = '50 GB Backup Block';
UPDATE product_catalog SET fusion_id = '389' WHERE level = 'Component' AND sku_name = '500 GB Backup Block';
UPDATE product_catalog SET fusion_id = '390' WHERE level = 'Component' AND sku_name = '600 GB Backup Block';
UPDATE product_catalog SET fusion_id = '391' WHERE level = 'Component' AND sku_name = '700 GB Backup Block';
UPDATE product_catalog SET fusion_id = '1778' WHERE level = 'Component' AND sku_name = '750W Redundant Power Supply';
UPDATE product_catalog SET fusion_id = '393' WHERE level = 'Component' AND sku_name = '800 GB Backup Block';
UPDATE product_catalog SET fusion_id = '394' WHERE level = 'Component' AND sku_name = '900 GB Backup Block';
UPDATE product_catalog SET fusion_id = '3752' WHERE level = 'Component' AND sku_name = '960 GB SSD';
UPDATE product_catalog SET fusion_id = '5784' WHERE level = 'Component' AND sku_name = 'Alma Linux 8';
UPDATE product_catalog SET fusion_id = '5785' WHERE level = 'Component' AND sku_name = 'Alma Linux 9';
UPDATE product_catalog SET fusion_id = '949' WHERE level = 'Component' AND sku_name = 'Cristie - Bare Metal Recovery Service';
UPDATE product_catalog SET fusion_id = '4042' WHERE level = 'Component' AND sku_name = 'Intel X710 Quad Port 10Gb DA/SFP+ Ethernet, NDC';
UPDATE product_catalog SET fusion_id = '3352' WHERE level = 'Component' AND sku_name = 'LM Basic Monitoring';
UPDATE product_catalog SET fusion_id = '3353' WHERE level = 'Component' AND sku_name = 'LM Standard Monitoring';
UPDATE product_catalog SET fusion_id = '4433' WHERE level = 'Component' AND sku_name = 'Monitoring Opt-out';
UPDATE product_catalog SET fusion_id = '4693' WHERE level = 'Component' AND sku_name = 'RHEL 8.x VDC for Unlimited Linux Guests';
UPDATE product_catalog SET fusion_id = '6092' WHERE level = 'Component' AND sku_name = 'RHEL 8.x for VMs';
UPDATE product_catalog SET fusion_id = '5792' WHERE level = 'Component' AND sku_name = 'RHEL 9.x VDC for Unlimited Linux Guests';
UPDATE product_catalog SET fusion_id = '6091' WHERE level = 'Component' AND sku_name = 'RHEL 9.x for VMs';
UPDATE product_catalog SET fusion_id = '5786' WHERE level = 'Component' AND sku_name = 'Rocky Linux 8';
UPDATE product_catalog SET fusion_id = '5787' WHERE level = 'Component' AND sku_name = 'Rocky Linux 9';
UPDATE product_catalog SET fusion_id = '262' WHERE level = 'Component' AND sku_name = 'Tivoli Backup - Daily Incremental';
UPDATE product_catalog SET fusion_id = '553' WHERE level = 'Component' AND sku_name = 'Tivoli Backup - Daily Incremental Remote';
UPDATE product_catalog SET fusion_id = '1371' WHERE level = 'Component' AND sku_name = 'Tivoli Backup - Daily Incremental with Offsite to Atlanta';
UPDATE product_catalog SET fusion_id = '1396' WHERE level = 'Component' AND sku_name = 'Tivoli Backup - Daily Incremental with Offsite to Miami';
UPDATE product_catalog SET fusion_id = '1394' WHERE level = 'Component' AND sku_name = 'Tivoli Backup - Daily Low';
UPDATE product_catalog SET fusion_id = '263' WHERE level = 'Component' AND sku_name = 'Tivoli Backup - Weekly Incremental';
UPDATE product_catalog SET fusion_id = '554' WHERE level = 'Component' AND sku_name = 'Tivoli Backup - Weekly Incremental Remote';
UPDATE product_catalog SET fusion_id = '1398' WHERE level = 'Component' AND sku_name = 'Tivoli Backup - Weekly Incremental with Offsite to Atlanta';
UPDATE product_catalog SET fusion_id = '1397' WHERE level = 'Component' AND sku_name = 'Tivoli Backup - Weekly Incremental with Offsite to Miami';
UPDATE product_catalog SET fusion_id = '84' WHERE level = 'Component' AND sku_name = 'Tivoli TDP for MS-SQL - Daily 1Hr Logs';
UPDATE product_catalog SET fusion_id = '763' WHERE level = 'Component' AND sku_name = 'Tivoli TDP for MS-SQL - Daily 2Hr Logs';
UPDATE product_catalog SET fusion_id = '764' WHERE level = 'Component' AND sku_name = 'Tivoli TDP for MS-SQL - Daily 4Hr Logs';
UPDATE product_catalog SET fusion_id = '85' WHERE level = 'Component' AND sku_name = 'Tivoli TDP for MS-SQL - Weekly 4Hr Logs';

COMMIT;
