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

-- -----------------------------------------------------------------------------
-- COMPONENTS (aliases: seed sku_name -> fusion_id from dimProductAttributes)
-- CSV uses different wording (e.g. "32 GB DDR4 RAM - Total", "10 pack Windows...")
-- -----------------------------------------------------------------------------

UPDATE product_catalog SET fusion_id = '1245' WHERE level = 'Component' AND sku_name = '1 pack - Windows Remote Desktop Service SAL';
UPDATE product_catalog SET fusion_id = '1246' WHERE level = 'Component' AND sku_name = '5 pack - Windows Remote Desktop Service SAL';
UPDATE product_catalog SET fusion_id = '1247' WHERE level = 'Component' AND sku_name = '10 pack - Windows Remote Desktop Service SAL';
UPDATE product_catalog SET fusion_id = '1248' WHERE level = 'Component' AND sku_name = '20 pack - Windows Remote Desktop Service SAL';
UPDATE product_catalog SET fusion_id = '3057' WHERE level = 'Component' AND sku_name = '16 GB DDR4 RAM';
UPDATE product_catalog SET fusion_id = '3034' WHERE level = 'Component' AND sku_name = '32 GB DDR4 RAM';
UPDATE product_catalog SET fusion_id = '3027' WHERE level = 'Component' AND sku_name = '64 GB DDR4 RAM';
UPDATE product_catalog SET fusion_id = '6237' WHERE level = 'Component' AND sku_name = '96 GB DDR4 RAM';
UPDATE product_catalog SET fusion_id = '2953' WHERE level = 'Component' AND sku_name = '128 GB DDR4 RAM';
UPDATE product_catalog SET fusion_id = '2952' WHERE level = 'Component' AND sku_name = '192 GB DDR4 RAM';
UPDATE product_catalog SET fusion_id = '3041' WHERE level = 'Component' AND sku_name = '256 GB DDR4 RAM';
UPDATE product_catalog SET fusion_id = '3068' WHERE level = 'Component' AND sku_name = '384 GB DDR4 RAM';
UPDATE product_catalog SET fusion_id = '3079' WHERE level = 'Component' AND sku_name = '512 GB DDR4 RAM';
UPDATE product_catalog SET fusion_id = '3080' WHERE level = 'Component' AND sku_name = '768 GB DDR4 RAM';
UPDATE product_catalog SET fusion_id = '3082' WHERE level = 'Component' AND sku_name = '1536 GB DDR4 RAM';
UPDATE product_catalog SET fusion_id = '6144' WHERE level = 'Component' AND sku_name = '16 GB DDR5 RAM';
UPDATE product_catalog SET fusion_id = '6150' WHERE level = 'Component' AND sku_name = '32 GB DDR5 RAM';
UPDATE product_catalog SET fusion_id = '6105' WHERE level = 'Component' AND sku_name = '64 GB DDR5 RAM';
UPDATE product_catalog SET fusion_id = '6022' WHERE level = 'Component' AND sku_name = '128 GB DDR5 RAM';
UPDATE product_catalog SET fusion_id = '6184' WHERE level = 'Component' AND sku_name = '192 GB DDR5 RAM';
UPDATE product_catalog SET fusion_id = '6115' WHERE level = 'Component' AND sku_name = '256 GB DDR5 RAM';
UPDATE product_catalog SET fusion_id = '6108' WHERE level = 'Component' AND sku_name = '384 GB DDR5 RAM';
UPDATE product_catalog SET fusion_id = '6109' WHERE level = 'Component' AND sku_name = '512 GB DDR5 RAM';
UPDATE product_catalog SET fusion_id = '6110' WHERE level = 'Component' AND sku_name = '768 GB DDR5 RAM';
UPDATE product_catalog SET fusion_id = '6111' WHERE level = 'Component' AND sku_name = '1024 GB DDR5 RAM';
UPDATE product_catalog SET fusion_id = '6112' WHERE level = 'Component' AND sku_name = '1536 GB DDR5 RAM';
UPDATE product_catalog SET fusion_id = '6113' WHERE level = 'Component' AND sku_name = '2048 GB DDR5 RAM';
UPDATE product_catalog SET fusion_id = '3028' WHERE level = 'Component' AND sku_name = 'Hardware RAID Controller';
UPDATE product_catalog SET fusion_id = '3182' WHERE level = 'Component' AND sku_name = 'Intel X710-DA2 10 GbE NIC with 2 x SFP+';
UPDATE product_catalog SET fusion_id = '4039' WHERE level = 'Component' AND sku_name = 'Intel Xeon Bronze 3106 1.7 GHz 8 Cores/8T';
UPDATE product_catalog SET fusion_id = '4030' WHERE level = 'Component' AND sku_name = 'Intel Xeon Silver 4110 2.1 GHz 8 Cores/16T';
UPDATE product_catalog SET fusion_id = '4040' WHERE level = 'Component' AND sku_name = 'Intel Xeon Gold 5118 2.3 GHz 12 Cores/24T';
UPDATE product_catalog SET fusion_id = '6092' WHERE level = 'Component' AND sku_name = 'RHEL 8.x';
UPDATE product_catalog SET fusion_id = '6091' WHERE level = 'Component' AND sku_name = 'RHEL 9.x';
UPDATE product_catalog SET fusion_id = '5882' WHERE level = 'Component' AND sku_name = 'SQL Server 2019 Standard Edition';
UPDATE product_catalog SET fusion_id = '5904' WHERE level = 'Component' AND sku_name = 'SQL Server 2019 Enterprise Edition';
UPDATE product_catalog SET fusion_id = '5883' WHERE level = 'Component' AND sku_name = 'SQL Server 2022 Standard Edition';
UPDATE product_catalog SET fusion_id = '5902' WHERE level = 'Component' AND sku_name = 'SQL Server 2022 Enterprise Edition';
UPDATE product_catalog SET fusion_id = '4525' WHERE level = 'Component' AND sku_name = 'Windows Server 2019 Standard Edition';
UPDATE product_catalog SET fusion_id = '4510' WHERE level = 'Component' AND sku_name = 'Windows Server 2019 Data Center Edition';
UPDATE product_catalog SET fusion_id = '6204' WHERE level = 'Component' AND sku_name = 'Windows Server 2022 Standard Edition';
UPDATE product_catalog SET fusion_id = '6238' WHERE level = 'Component' AND sku_name = 'Windows Server 2022 Data Center Edition';
UPDATE product_catalog SET fusion_id = '6262' WHERE level = 'Component' AND sku_name = 'Windows Server 2025 Standard Edition';
UPDATE product_catalog SET fusion_id = '6260' WHERE level = 'Component' AND sku_name = 'Windows Server 2025 Data Center Edition';

-- TLS aliases (strip " - M" to match CSV e.g. "Pro Series 6.0")
UPDATE product_catalog SET fusion_id = '957' WHERE level = 'TLS' AND sku_name = 'Advanced Series 5.0 - M';
UPDATE product_catalog SET fusion_id = '1255' WHERE level = 'TLS' AND sku_name = 'Advanced Series 6.0 - M';
UPDATE product_catalog SET fusion_id = '1262' WHERE level = 'TLS' AND sku_name = 'Essential Series 6.0 - M';
UPDATE product_catalog SET fusion_id = '943' WHERE level = 'TLS' AND sku_name = 'Pro Series 5.0 - M';
UPDATE product_catalog SET fusion_id = '1254' WHERE level = 'TLS' AND sku_name = 'Pro Series 6.0 - M';
UPDATE product_catalog SET fusion_id = '945' WHERE level = 'TLS' AND sku_name = 'Storage Series 5.0 - M';
UPDATE product_catalog SET fusion_id = '1263' WHERE level = 'TLS' AND sku_name = 'Storage Series 6.0 - M';

-- -----------------------------------------------------------------------------
-- COMPONENTS (drive/OS aliases: same product, different label in CSV)
-- -----------------------------------------------------------------------------

UPDATE product_catalog SET fusion_id = '1810' WHERE level = 'Component' AND sku_name = '1 TB 7200 6 Gb/s SATA';
UPDATE product_catalog SET fusion_id = '1782' WHERE level = 'Component' AND sku_name = '2 TB 7200 6 Gb/s SATA';
UPDATE product_catalog SET fusion_id = '2742' WHERE level = 'Component' AND sku_name = '4 TB 7200 6 Gb/s SATA';
UPDATE product_catalog SET fusion_id = '4036' WHERE level = 'Component' AND sku_name = '12 TB 7200 6 Gb/s SATA';
UPDATE product_catalog SET fusion_id = '6090' WHERE level = 'Component' AND sku_name = '1.92 TB SATA 2.5in SSD';
UPDATE product_catalog SET fusion_id = '5178' WHERE level = 'Component' AND sku_name = '3.84 TB SATA 2.5in SSD';
UPDATE product_catalog SET fusion_id = '6116' WHERE level = 'Component' AND sku_name = '7.6 TB Micron 9400 SSD';
UPDATE product_catalog SET fusion_id = '6147' WHERE level = 'Component' AND sku_name = '8 TB SATA';
UPDATE product_catalog SET fusion_id = '6023' WHERE level = 'Component' AND sku_name = 'Debian 12';
UPDATE product_catalog SET fusion_id = '5745' WHERE level = 'Component' AND sku_name = 'Ubuntu 22.04 LTS';
UPDATE product_catalog SET fusion_id = '4029' WHERE level = 'Component' AND sku_name = 'Default Xeon Bronze 3106 1.7 GHz 8 Cores/8T';
UPDATE product_catalog SET fusion_id = '6106' WHERE level = 'Component' AND sku_name = 'Default Intel Xeon Silver 4514Y 2G, 16C/32T';
UPDATE product_catalog SET fusion_id = '6021' WHERE level = 'Component' AND sku_name = 'Default Intel Xeon Gold 6526Y 2.9G, 16/32T';
UPDATE product_catalog SET fusion_id = '4031' WHERE level = 'Component' AND sku_name = 'Intel Xeon Gold 5122 3.6 GHz 4 Cores/8T (MTO)';
UPDATE product_catalog SET fusion_id = '4032' WHERE level = 'Component' AND sku_name = 'Intel Xeon Gold 6130 2.1 GHz 16 Cores/32T (MTO)';
UPDATE product_catalog SET fusion_id = '5156' WHERE level = 'Component' AND sku_name = 'Intel Xeon Gold 6238R 2.2 GHz 28C/56T';
UPDATE product_catalog SET fusion_id = '6083' WHERE level = 'Component' AND sku_name = 'Intel Xeon Gold 6548Y+ 2.5G, 32C/64T';
UPDATE product_catalog SET fusion_id = '6084' WHERE level = 'Component' AND sku_name = 'Intel Xeon Platinum 8558U 2G, 48C/96T';
UPDATE product_catalog SET fusion_id = '945' WHERE level = 'TLS' AND sku_name = 'Storage Series 5.0 vHost';
UPDATE product_catalog SET fusion_id = '1371' WHERE level = 'Component' AND sku_name = 'Tivoli Backup - Daily Incremental Offsite to Atlanta - Low';
UPDATE product_catalog SET fusion_id = '1371' WHERE level = 'Component' AND sku_name = 'Tivoli Backup - Daily Incremental with Offsite to Toronto';
UPDATE product_catalog SET fusion_id = '1397' WHERE level = 'Component' AND sku_name = 'Tivoli Backup - Weekly Incremental with Offsite to Toronto';
UPDATE product_catalog SET fusion_id = '6277' WHERE level = 'Component' AND sku_name = 'Debian 13';
UPDATE product_catalog SET fusion_id = '5941' WHERE level = 'Component' AND sku_name = 'VMWare ESXi 8.x';
UPDATE product_catalog SET fusion_id = '6275' WHERE level = 'Component' AND sku_name = 'Proxmox VE License';
UPDATE product_catalog SET fusion_id = '6117' WHERE level = 'Component' AND sku_name = '3.84 TB NVMe u.2 2.5in';
UPDATE product_catalog SET fusion_id = '5935' WHERE level = 'Component' AND sku_name = '6.4 TB NVMe u.2 2.5in';
UPDATE product_catalog SET fusion_id = '6118' WHERE level = 'Component' AND sku_name = '960 GB NVMe u.2 2.5in';
UPDATE product_catalog SET fusion_id = '3752' WHERE level = 'Component' AND sku_name = '960 GB SATA 2.5in SSD';

COMMIT;
