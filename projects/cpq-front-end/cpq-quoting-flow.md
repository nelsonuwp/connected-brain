# CPQ Quoting Flow

> **Generated:** 2026-05-15 · Live data from Fusion PostgreSQL + MSSQL DM_BusinessInsights  
> **Purpose:** End-to-end quoting process reference for human review and future sessions.

---

## Overview

```
1. User picks DC  →  picks target currency (any: USD/CAD/GBP/EUR)  →  picks term
2. Available servers are listed (priced in target currency)
3. User selects a server → sees default config + cost breakdown
4. User swaps/adds components → live margin recalculates
5. Copy quote summary
```

Currency is **free choice** — not restricted to what the DC has pricebook rows for.
The app queries pricebook in the target currency first; if no rows exist for that DC+currency,
it falls back to the native currency and converts via `dbo.dimCurrencyExchangeRates`.

---

## Step 1 — Filter Setup

### 1a. Data Center

Source: `Fusion.public.sb_datacenter` WHERE active = true.

| dc_abbr | Name | City | Overhead in cost_drivers.json |
|---|---|---|---|
| AMS | Amsterdam | Amsterdam | — |
| ATL | Atlanta | Atlanta | ✓ |
| AWS-CA | AWS Canada | Canada | — |
| AWS-EMEA | AWS EMEA | Europe | — |
| AWS-UK | AWS United Kingdom | United Kingdom | — |
| AWS-US | AWS United States | United States | — |
| AZURE-CAN | AZURE-CAN | Canada | — |
| AZURE-FRN | AZURE-FRN | France | — |
| AZURE-UK | AZURE-UK | United Kingdom | — |
| AZURE-US | AZURE-US | United States | — |
| BAR-612W | Barrie | Barrie | — |
| CLOUD-CA | Cloud Canada | Canada | — |
| CLOUD-EU | Cloud Europe | Europe | — |
| CLOUD-LA | Cloud Latin America | Latin America | — |
| CLOUD-UK | Cloud United Kingdom | United Kingdom | — |
| CLOUD-US | Cloud United States | United States | — |
| CRO | Croydon | London | — |
| FMT | Fremont | Fremont | — |
| FRK | Frankfurt | Frankfurt | — |
| GOS | Goswell | London | — |
| IAD2 | South Pointe | Herndon | ✓ |
| LAX1 | Malibu | Los Angeles | ✓ |
| LDN1 | London | Fleet | — |
| MIA | Miami | Miami | ✓ |
| MTL-17500TC | Kirkland | Kirkland | — |
| MTL-BH | Montreal | Montreal | ✓ |
| MUN | Munich | Munich | — |
| NYC-BR | New York | New York | — |
| OFF-NCA | Off net CA | Canada | — |
| OFF-NUK | Off net UK | United Kingdom | — |
| OFF-NUS | Off net US | United States | — |
| POR | Portsmouth | Portsmouth | ✓ |
| SAT5 | Vicar | San Antonio | — |
| SEA-WES | Seattle | Seattle | — |
| SJ-MP | San Jose | San Jose | — |
| T3-AU1 | Sydney (MCC) | Sydney | — |
| T3-CA3 | Toronto (MCC) | Toronto | — |
| T3-GB3 | Slough (MCC) | Slough | — |
| T3-IL1 | Chicago (MCC) | Chicago | — |
| T3-NY1 | New York (MCC) | New York | — |
| T3-SG1 | Singapore | Singapore | — |
| T3-UC1 | Santa Clara (MCC) | Santa Clara | — |
| T3-UT1 | Salt Lake City (MCC) | Salt Lake City | — |
| T3-VA1 | Sterling (MCC) | Sterling | — |
| T3-VA2 | Sterling (MCC-VA2) | Sterling | — |
| T3-WA1 | Seattle (MCC) | Seattle | — |
| TOR | Toronto | Toronto | ✓ |
| TOR-145K | King St | King | — |
| TOR-1YG | 1 Yonge | Toronto | — |
| TOR-431H | Horner | Horner | — |
| TOR-FR | 151 Front Street | Toronto | — |
| VAN | Vancouver | Vancouver | — |
| VAN-SP | Spencer Building | Vancouver | — |

> DCs without a ✓ show $0 overhead in the CPQ — no cost_drivers.json entry exists for them yet.

### 1b. Currency (target)

Options: **USD · CAD · GBP · EUR** — free choice, independent of DC.

The app handles currency transparency: if the pricebook has rows in the target currency for that DC, they're used directly. If not, prices are fetched in the DC's native currency and converted via `dbo.dimCurrencyExchangeRates`. The user never needs to know which path was taken — everything is returned in the currency they selected.

### 1c. Term

Options (UI): **12 months · 24 months · 36 months · Month-to-month (m2m) · Custom (any integer)**

| What term affects | What term does NOT affect |
|---|---|
| CapEx amortization divisor (CapEx ÷ term_months = CapEx/mo) | Server MRC |
| Gross margin % shown in the CPQ | Component MRC |
| | NRC / Setup fees |
| | Pricebook pricing (all server discounts = 0%) |

> `Fusion.public.product_class_contract_length_discounts WHERE product_class=1, product_line=4`
> returns 0% for setup_discount, mrc_discount, nrc_discount across all 6 contract lengths.
> Term selection has **zero effect on quoted price** — only on internal cost amortization.

---

## Step 2 — Available Servers (DC-Agnostic View)

Source: `product_catalog` JOIN `pricebook` JOIN `sb_datacenter`
Filters: `product_class=1, is_active=true, product_line_id=4, component_id IS NULL, mrc>0, is_available=true`

| product_id | Name | SKU | MRC Range (native) | # DCs | Available At | Currencies |
|---|---|---|---|---|---|---|
| 974 | Essential Series 5.0 - D | — | $239.00–$409.00 | 4 | IAD2, LAX1, POR, TOR | CAD, GBP, USD |
| 1271 | Fusion Series 5.0 UK | — | $269.00 | 2 | CRO, POR | GBP |
| 1282 | Pro Dell PE R-660XS - Non NVMe | — | $345.00 | 2 | IAD2, LAX1 | USD |
| 958 | Advanced Series 5.0 - D | — | $360.00–$648.00 | 4 | IAD2, LAX1, POR, TOR | CAD, GBP, USD |
| 1288 | Cluster 5.0 | — | $399.00–$549.00 | 5 | ATL, IAD2, LAX1, MIA, TOR | CAD, USD |
| 1270 | Fusion Series 5.0 | — | $399.00–$529.00 | 5 | ATL, IAD2, LAX1, MIA, TOR | CAD, USD |
| 1289 | Atomix 5.0 | — | $449.00–$620.00 | 5 | ATL, IAD2, LAX1, MIA, TOR | CAD, USD |
| 950 | Storage Series 5.0 - D | — | $502.00–$904.00 | 5 | IAD2, LAX1, MIA, POR, TOR | CAD, GBP, USD |
| 949 | Pro Series 5.0 - D | — | $577.00–$1,039.00 | 4 | IAD2, LAX1, POR, TOR | CAD, GBP, USD |
| 1238 | Pro Dell PE 650xs - Non NVMe | — | $810.00–$1,055.00 | 3 | IAD2, LAX1, TOR | CAD, USD |
| 1299 | R470 - Advanced Series | — | $929.00–$1,309.00 | 7 | ATL, CRO, IAD2, LAX1, MIA, POR, TOR | CAD, GBP, USD |
| 1258 | Advanced Series 6.0 vHost | — | $959.00–$1,399.00 | 7 | ATL, CRO, IAD2, LAX1, MIA, POR, TOR | CAD, GBP, USD |
| 1255 | Advanced Series 6.0 | — | $959.00–$1,399.00 | 7 | ATL, CRO, IAD2, LAX1, MIA, POR, TOR | CAD, GBP, USD |
| 1252 | Pro Dell PE R-660 - Non NVMe | — | $1,019.00 | 5 | IAD2, LAX1, MIA, POR, TOR | CAD, GBP, USD |
| 1272 | Pro Dell PE R-660XS - NVMe | — | $1,019.00 | 7 | ATL, CRO, IAD2, LAX1, MIA, POR, TOR | CAD, GBP, USD |
| 1263 | Storage Series 6.0 | — | $1,199.00–$1,749.00 | 7 | ATL, CRO, IAD2, LAX1, MIA, POR, TOR | CAD, GBP, USD |
| 1240 | Pro Dell PE R-650 - NVMe | — | $1,205.00–$1,575.00 | 3 | IAD2, LAX1, TOR | CAD, USD |
| 1300 | R670 - Pro Series | — | $1,429.00–$1,989.00 | 7 | ATL, CRO, IAD2, LAX1, MIA, POR, TOR | CAD, GBP, USD |
| 1254 | Pro Series 6.0 | — | $1,429.00–$2,089.00 | 7 | ATL, CRO, IAD2, LAX1, MIA, POR, TOR | CAD, GBP, USD |
| 1259 | Pro Series 6.0 vHost | — | $1,429.00–$2,089.00 | 7 | ATL, CRO, IAD2, LAX1, MIA, POR, TOR | CAD, GBP, USD |

> MRC range spans all DCs and all pricebook currencies — direct comparison requires fixing one DC+currency.

---

## Step 3 — Default Configuration

**Example server:** Pro Series 6.0 (product_id=1254) · DC: IAD (fusion_dc_id=8) · Currency: USD

**Server base MRC:** $1,699.00/mo
**Source:** `pricebook WHERE product_catalog_id=1254, currency='USD', datacenter=8, component_id IS NULL`

**Default components** (`product_templates`):

| component_id | Component | Type | Category | Qty | MRC (USD) |
|---|---|---|---|---|---|
| 6028 | 2 TB Bandwidth Included with Host Plan | Included | Bandwidth | 1 | included |
| 6029 | Dell R-660 Chassis | Chassis | Hardware | 1 | included |
| 6022 | 128 GB DDR5 RAM - Included | Included RAM | Hardware | 1 | included |
| 6021 | Default Intel Xeon Gold 6526Y 2.8 GHz 16 Cores/32T (195W TDP) | Intel | Hardware | 1 | included |
| 6021 | Default Intel Xeon Gold 6526Y 2.8 GHz 16 Cores/32T (195W TDP) | Intel | Hardware | 1 | included |
| 6025 | Dual Port 10/25GbE NIC | NICs | Hardware | 1 | included |
| 6024 | Dual Port 1 GbE NIC | NICs | Hardware | 1 | included |
| 6026 | 1100 Watt Power Supply | Power Supply | Hardware | 1 | included |
| 6027 | RAID 1 | RAID Configuration | Hardware | 1 | included |
| 3697 | 1100W Redundant Power Supply | Redundant Power Supply | Hardware | 1 | $30.00 |
| 6023 | Hardware RAID Controller 8 GB Cache with BBU | SAS/SATA Controllers | Hardware | 1 | included |
| 3960 | IPMI Card | Security | Hardware | 1 | included |
| 3704 | 480 GB SSD | SSD | Hardware | 1 | $20.00 |
| 3704 | 480 GB SSD | SSD | Hardware | 1 | $20.00 |
| 3698 | 1000 Mbit Connection - GigE | Network | Network | 1 | included |
| 3721 | Aptum Essential Monitoring | Zabbix | Software | 1 | included |
| 4167 | Managed OS Patching | Support | Support | 1 | included |
| 5974 | SmartKey Opt-in | Support | Support | 1 | included |

**Default component MRC total:** $70.00/mo
**Total customer MRC (default config):** $1,699.00 + $70.00 = **$1,769.00/mo**

**HW CapEx (one-time): $7,569.00 USD**
- Source: `MSSQL: profitability.ocean_sku_cost WHERE sku_id=1254` (server-level entry)
- This is the **all-in** hardware cost for the fully configured base server — CPUs, RAM, storage, PSU, chassis, all default components included
- Per-component entries in `ocean_sku_cost` (e.g. RAM, PSU) exist but are partial and unreliable — the server-level entry is always used
- Convert to display currency via `dbo.dimCurrencyExchangeRates` when needed

---

## Step 4 — Available Upgrades

Source: `product_allowed_components` WHERE product_id=1254, joined to `pricebook` at IAD in USD.

### Backup & Storage

| Component | MRC Upcharge (USD) | HW Cost (USD) |
|---|---|---|
| Aptum Managed Backup BMR Service | +$50.00/mo | — |
| Aptum Managed Backup Daily 30d + 12m retention | included | — |
| Aptum Managed Backup Daily 30d + 12m retention with Offsite Copy | included | — |
| Aptum Managed Backup Daily 30d retention | included | — |
| Aptum Managed Backup Daily 30d retention with Offsite Copy | included | — |
| Aptum Managed Backup Daily 7d retention | included | — |
| Aptum Managed Backup Daily 7d retention with Offsite Copy | included | — |
| Aptum Managed Backup SQL Log Hourly Backup | included | — |
| Aptum Managed Backup Weekly 4w retention | included | — |
| Aptum Managed Backup Weekly 4w retention with Offsite Copy | included | — |
| 1000 GB Backup Block | included | $56.00 |
| 100 GB Backup Block | +$50.00/mo | $5.60 |
| 10 GB Backup Blocks | +$5.00/mo | $0.56 |
| 1100 GB Backup Block | included | $61.60 |
| 1200 GB Backup Block | included | $67.20 |
| 1300 GB Backup Block | included | $72.80 |
| 1400 GB Backup Block | included | $78.40 |
| 1500 GB Backup Block | included | $84.00 |
| 150 GB Backup Block | +$75.00/mo | $8.40 |
| 1600 GB Backup Block | included | $89.60 |
| 1700 GB Backup Block | included | $95.20 |
| 1800 GB Backup Block | included | $100.80 |
| 1900 GB Backup Block | included | $106.40 |
| 2000 GB Backup Block | included | $112.00 |
| 200 GB Backup Block | +$100.00/mo | $11.20 |
| 250 GB Backup Block | +$125.00/mo | $14.00 |
| 25 GB Backup Blocks | +$12.50/mo | $1.40 |
| 300 GB Backup Block | included | $16.80 |
| 400 GB Backup Block | included | $22.40 |
| 500 GB Backup Block | included | $28.00 |
| 50 GB Backup Block | +$25.00/mo | $2.80 |
| 600 GB Backup Block | included | $33.60 |
| 700 GB Backup Block | included | $39.20 |
| 800 GB Backup Block | included | $44.80 |
| 900 GB Backup Block | included | $50.40 |
| 6 Gb/s SAS Controller Dual Port  for MD3220 | included | — |
| Dual Port 32Gb/s Fibre Channel HBA with SFPs | included | — |
| Dual Port 8Gb/s Fibre Channel HBA | included | — |
| Fiber Port | included | — |
| Fiber Run | included | — |
| PowerPath | included | — |

### Bandwidth

| Component | MRC Upcharge (USD) | HW Cost (USD) |
|---|---|---|
| 2 TB Bandwidth Included with Host Plan | included | — |

### Hardware

| Component | MRC Upcharge (USD) | HW Cost (USD) |
|---|---|---|
| 1024 GB DDR5 RAM Total (128 GB Included) - Upgrade | +$505.00/mo | — |
| 1536 GB DDR5 RAM Total (128 GB Included) - Upgrade | +$760.00/mo | — |
| 192 GB DDR5 RAM Total (128 GB Included) - Upgrade | +$115.00/mo | $804.00 |
| 2048 GB DDR5 RAM Total (128 GB Included) - Upgrade | +$1,010.00/mo | — |
| 256 GB DDR5 RAM Total (128 GB Included) - Upgrade | +$120.00/mo | $856.00 |
| 384 GB DDR5 RAM Total (128 GB Included) - Upgrade | +$185.00/mo | $1,284.00 |
| 512 GB DDR5 RAM Total (128 GB Included) - Upgrade | +$255.00/mo | $1,768.00 |
| 768 GB DDR5 RAM Total (128 GB Included) - Upgrade | +$380.00/mo | — |
| 192 GB DDR5 RAM Total (64 GB Included) - Upgrade | +$115.00/mo | $804.00 |
| Dell R-660 Chassis | included | — |
| 128 GB DDR5 RAM - Included | included | $536.00 |
| Default Intel Xeon Gold 6526Y 2.8 GHz 16 Cores/32T (195W TDP) | included | — |
| Intel Xeon Gold 6326 2.9 GHz 16 Cores/32T (185W TDP) | included | $-1.00 |
| Intel Xeon Gold 6534 4.0 GHz 8 Cores/16T (195W TDP) | +$460.00/mo | $3,190.00 |
| Intel Xeon Gold 6548Y+ 2.5 GHz  32 Cores/64T (250W TDP) | +$600.00/mo | — |
| Intel Xeon Platinum 8558U 2.0 GHz 48 Cores/96T (300W TDP) | +$600.00/mo | — |
| Dual Port 10/25GbE NIC | included | — |
| Dual Port 10GbE BASE-T NIC | included | — |
| Dual Port 1 GbE NIC | included | — |
| Intel  X710-DA2 10 GbE NIC with  2 x SFP+ | +$100.00/mo | $140.00 |
| Quad Port 1 GbE NIC | included | $120.00 |
| 15.36 TB SSD NVMe | +$3,110.00/mo | — |
| 1.92 TB SSD NVMe | +$475.00/mo | — |
| 3.2 TB SSD NVMe | +$900.00/mo | — |
| 3.84 TB SSD PCIe NVMe | +$500.00/mo | — |
| 6.4 TB SSD NVMe | +$930.00/mo | — |
| 7.68 TB SSD NVMe | +$1,660.00/mo | — |
| 960 GB SSD NVMe | +$115.00/mo | $300.00 |
| 1100 Watt Power Supply | included | — |
| RAID 0 | included | — |
| RAID 1 | included | — |
| RAID 10 | included | — |
| RAID 5 | included | — |
| RAID 6 | included | — |
| 1100W  Redundant Power Supply | +$30.00/mo | $12,056.00 |
| Hardware RAID Controller 8 GB Cache with BBU | included | — |
| 1 TB 7200 SATA | included | $16.00 |
| IPMI Card | included | $-1.00 |
| Link Service to Firewall | included | $6,560.00 |
| Link Service to Load Balancer | included | $-1.00 |
| 1.92 TB SSD | +$50.00/mo | $349.00 |
| 3.84 TB SSD | +$55.00/mo | $379.00 |
| 480 GB SSD | +$20.00/mo | $149.00 |
| 7.6 TB SSD | +$60.00/mo | $430.00 |
| 8 TB SSD | +$200.00/mo | — |
| 960 GB  SSD | +$25.00/mo | $185.00 |

### Network

| Component | MRC Upcharge (USD) | HW Cost (USD) |
|---|---|---|
| 1 IP Address | +$1.00/mo | — |
| /24 IPv4 block (256 total, 253 customer usable addresses) | included | — |
| /25 IPv4 block (128 total, 125 customer usable addresses) | +$128.00/mo | — |
| /26 IPv4 block (64 total,61 customer-usable addresses) | +$64.00/mo | — |
| /27 IPv4 block (32 total,29 customer-usable addresses) | +$32.00/mo | — |
| /28 IPv4 block (16 total,13 customer-usable addresses) | +$16.00/mo | — |
| /29 IPv4 block (8 total,5 customer-usable addresses) | +$8.00/mo | — |
| 1000 Mbit Connection - GigE | included | — |
| 10 GbE Connection | +$35.00/mo | — |
| PCI Compliance | included | — |
| Private Net 1000 Mbps | +$60.00/mo | — |
| Private Net 10 GbE | +$35.00/mo | — |
| Switches - Per port - Private | included | — |
| Switches - Per port - Public | included | — |
| Upgrade to GigE | included | — |

### Other

| Component | MRC Upcharge (USD) | HW Cost (USD) |
|---|---|---|
| Rush order | included | — |
| AlwaysOn Availiability Group Member | included | — |
| Domain Name | included | — |
| Link to Active Directory Domain | included | — |
| Link to Linux Cluster | included | — |
| Link to Windows Cluster | included | — |

### Security

| Component | MRC Upcharge (USD) | HW Cost (USD) |
|---|---|---|
| Alert Logic Remote Collector | included | $-1.00 |

### Software

| Component | MRC Upcharge (USD) | HW Cost (USD) |
|---|---|---|
| Alert Logic agent for Linux | included | — |
| Alert Logic agent for Windows | included | — |
| Additional UC/SAN – 1 year | included | — |
| Additional UC/SAN – 2 year | included | — |
| P1 SSL Correction Fee | included | — |
| Plesk Obsidian Add-on - 1 Language Pack | +$6.95/mo | — |
| Plesk Obsidian Add-on - Email Security Pack (Linux) | +$34.95/mo | — |
| Plesk Obsidian Add-on - Hosting Pack | +$24.50/mo | — |
| Plesk Obsidian Add-on - Power Pack | +$20.00/mo | $12.74 |
| cPanel Premier Metal 100 | +$62.00/mo | $43.24 |
| cPanel Premier Metal 1000 Users - Linux | +$171.00/mo | $305.74 |
| cPanel Premier Metal 1100 Users - Linux | +$185.00/mo | — |
| cPanel Premier Metal 1200 Users - Linux | +$200.00/mo | — |
| cPanel Premier Metal 1300 Users - Linux | +$214.00/mo | — |
| cPanel Premier Metal 150 | +$50.00/mo | $50.74 |
| cPanel Premier Metal 200 | +$57.00/mo | $65.74 |
| cPanel Premier Metal 250 Users - Linux | +$64.00/mo | $80.74 |
| cPanel Premier Metal 300 Users - Linux | +$71.00/mo | $95.74 |
| cPanel Premier Metal 350 Users - Linux | +$78.00/mo | $110.74 |
| cPanel Premier Metal 400 Users - Linux | +$85.00/mo | $125.74 |
| cPanel Premier Metal 450 Users - Linux | +$93.00/mo | — |
| cPanel Premier Metal 500 Users - Linux | +$100.00/mo | — |
| cPanel Premier Metal 550 Users - Linux | +$107.00/mo | $170.74 |
| cPanel Premier Metal 600 Users - Linux | +$114.00/mo | — |
| cPanel Premier Metal 650 Users - Linux | +$121.00/mo | — |
| cPanel Premier Metal 700 Users - Linux | +$128.00/mo | — |
| cPanel Premier Metal 750 Users - Linux | +$135.00/mo | — |
| cPanel Premier Metal 800 Users - Linux | +$143.00/mo | — |
| cPanel Premier Metal 850 Users - Linux | +$150.00/mo | — |
| cPanel Premier Metal 900 Users - Linux | +$157.00/mo | — |
| cPanel Premier Metal 950 Users - Linux | +$164.00/mo | — |
| SQL Server 2019 Enterprise Edition 10 Core license (4 x 2 pack) | +$3,905.00/mo | — |
| SQL Server 2019 Enterprise Edition 12 Core license (6 x 2 pack) | +$4,686.00/mo | $3,279.90 |
| SQL Server 2019 Enterprise Edition 14 Core license (7 x 2 pack) | +$5,579.00/mo | — |
| SQL Server 2019 Enterprise Edition 16 Core license (8 x 2 pack) | +$6,375.00/mo | — |
| SQL Server 2019 Enterprise Edition 20 Core license (10 x 2 pack) | +$7,969.00/mo | — |
| SQL Server 2019 Enterprise Edition 22 Core license (11 x 2 pack) | +$8,766.00/mo | — |
| SQL Server 2019 Enterprise Edition 24 Core license (12 x 2 pack) | +$9,563.00/mo | — |
| SQL Server 2019 Enterprise Edition 26 Core license (13 x 2 pack) | +$10,360.00/mo | — |
| SQL Server 2019 Enterprise Edition 28 Core license (14 x 2 pack) | +$11,157.00/mo | — |
| SQL Server 2019 Enterprise Edition 30 Core license (15 x 2 pack) | +$11,954.00/mo | — |
| SQL Server 2019 Enterprise Edition 32 Core license (16 x 2 pack) | +$12,750.00/mo | — |
| SQL Server 2019 Enterprise Edition 34 Core license (17 x 2 pack) | +$13,547.00/mo | — |
| SQL Server 2019 Enterprise Edition 36 Core license (18 x 2 pack) | +$14,344.00/mo | — |
| SQL Server 2019 Enterprise Edition 38 Core license (19 x 2 pack) | +$15,141.00/mo | — |
| SQL Server 2019 Enterprise Edition 40 Core license (20 x 2 pack) | +$15,938.00/mo | — |
| SQL Server 2019 Enterprise Edition 4 Core license (2 x 2 pack) | +$1,562.00/mo | — |
| SQL Server 2019 Enterprise Edition 6 Core license (3 x 2 pack) | +$2,343.00/mo | — |
| SQL Server 2019 Enterprise Edition 8 Core license (4 x 2 pack) | +$3,124.00/mo | — |
| SQL Server 2022 Enterprise Edition 10 Core license (4 x 2 pack) | +$3,905.00/mo | — |
| SQL Server 2022 Enterprise Edition 12 Core license (6 x 2 pack) | +$4,686.00/mo | $3,279.90 |
| SQL Server 2022 Enterprise Edition 14 Core license (7 x 2 pack) | +$5,579.00/mo | — |
| SQL Server 2022 Enterprise Edition 16 Core license (8 x 2 pack) | +$6,375.00/mo | — |
| SQL Server 2022 Enterprise Edition 18 Core license (9 x 2 pack) | +$7,172.00/mo | — |
| SQL Server 2022 Enterprise Edition 20 Core license (10 x 2 pack) | +$7,969.00/mo | — |
| SQL Server 2022 Enterprise Edition 22 Core license (11 x 2 pack) | +$8,766.00/mo | — |
| SQL Server 2022 Enterprise Edition 24 Core license (12 x 2 pack) | +$9,563.00/mo | — |
| SQL Server 2022 Enterprise Edition 26 Core license (13 x 2 pack) | +$10,360.00/mo | — |
| SQL Server 2022 Enterprise Edition 28 Core license (14 x 2 pack) | +$11,157.00/mo | — |
| SQL Server 2022 Enterprise Edition 30 Core license (15 x 2 pack) | +$11,954.00/mo | — |
| SQL Server 2022 Enterprise Edition 32 Core license (16 x 2 pack) | +$12,750.00/mo | — |
| SQL Server 2022 Enterprise Edition 34 Core license (17 x 2 pack) | +$13,547.00/mo | — |
| SQL Server 2022 Enterprise Edition 36 Core license (18 x 2 pack) | +$14,344.00/mo | — |
| SQL Server 2022 Enterprise Edition 38 Core license (19 x 2 pack) | +$15,141.00/mo | — |
| SQL Server 2022 Enterprise Edition 40 Core license (20 x 2 pack) | +$15,938.00/mo | — |
| SQL Server 2022 Enterprise Edition 4 Core license (2 x 2 pack) | +$1,562.00/mo | — |
| SQL Server 2022 Enterprise Edition 6 Core license (3 x 2 pack) | +$2,343.00/mo | — |
| SQL Server 2022 Enterprise Edition 8 Core license (4 x 2 pack) | +$3,124.00/mo | $2,186.60 |
| Internal Systems OS | included | — |
| Alma Linux 8 | included | — |
| Alma Linux 9 | included | — |
| Debian 12.x Bookworm | included | — |
| Debian 13.x Trixie | included | — |
| RedHat ES 7.x 64-bit | included | $-1.00 |
| RHEL 8.x (1-2 proc) MH | included | $86.90 |
| RHEL 9.x (1-2 proc) | +$113.00/mo | $86.90 |
| RHEL 9.x (1-2 proc) MH | included | $86.90 |
| Rocky Linux 8 | included | — |
| Rocky Linux 9 | included | — |
| Ubuntu 20.04 64 bit | included | — |
| Ubuntu 22.04 64 bit | included | — |
| Ubuntu 24.04 64 bit | included | — |
| Minimal Red Hat Build | included | — |
| RHEL High Availability addon per Server (not virtualized) | included | $10.00 |
| Aptum Advanced Monitoring | +$25.00/mo | — |
| Monitoring Opt-out | included | — |
| Custom Provisioning Script – Trade Desk Only | included | — |
| Hardened OS | included | — |
| Active Directory Server | included | — |
| Custom Partitioning | included | — |
| Nginx | included | — |
| P1 - CSR Generation | included | — |
| Plesk Obsidian - Web Admin Edition (10 Domains) Linux | +$21.00/mo | $12.75 |
| Plesk Obsidian - Web Admin Edition (10 Domains) Windows | +$21.00/mo | $12.75 |
| Plesk Obsidian - Web Host Edition (Unlimited Domains) Linux | +$85.00/mo | $55.76 |
| Plesk Obsidian - Web Host Edition (Unlimited Domains) Windows | +$74.00/mo | $55.76 |
| Plesk Obsidian - Web Pro Edition (30 Domains) Linux | +$37.00/mo | $19.13 |
| Plesk Obsidian - Web Pro Edition (30 Domains) Windows | +$37.00/mo | $19.13 |
| RHEL 7 - ELS - Server or VM License | +$47.00/mo | $34.95 |
| RHEL 7 - ELS - VM License (Host Licensed) | included | $34.95 |
| Thawte SSL123 DV 1 Additional Domain (1 Year) | included | — |
| Thawte SSL123 DV 1 Additional Wildcard Domain (1 Year) | included | — |
| Thawte SSL123 DV  (1 Year) | included | — |
| Thawte SSL123 DV 5 Additional Domains (1 Year) | included | — |
| Thawte SSL123 DV 5 Additional Wildcard Domains (1 Year) | included | — |
| Thawte SSL Web Server EV 1 Additional Domain (1 Year) | included | — |
| Thawte SSL Web Server EV (1 Year) | included | — |
| Thawte SSL Web Server EV 5 Additional Domains (1 Year) | included | — |
| Thawte SSL Web Server OV 1 Additional Domain (1 Year) | included | — |
| Thawte SSL Web Server OV 1 Additional Wildcard Domain (1 Year) | included | — |
| Thawte SSL Web Server OV (1 Year) | included | — |
| Thawte SSL Web Server OV 5 Additional Domains (1 Year) | included | — |
| Thawte SSL Web Server OV 5 Additional Wildcard Domains (1 Year) | included | — |
| SQL Server 2019 Standard Edition 10 Core license (5 x 2 pack) | +$1,038.00/mo | — |
| SQL Server 2019 Standard Edition 12 Core license (6 x 2 pack) | +$1,245.00/mo | $871.14 |
| SQL Server 2019 Standard Edition 14 Core license (7 x 2 pack) | +$1,452.00/mo | — |
| SQL Server 2019 Standard Edition 16 Core license (8 x 2 pack) | +$1,660.00/mo | $1,161.52 |
| SQL Server 2019 Standard Edition 18 Core license (9 x 2 pack) | +$1,867.00/mo | — |
| SQL Server 2019 Standard Edition 20 Core license (10 x 2 pack) | +$2,075.00/mo | — |
| SQL Server 2019 Standard Edition 24 Core license (12 x 2 pack) | +$2,489.00/mo | $1,742.28 |
| SQL Server 2019 Standard Edition 4 Core license (2 x 2 pack) | +$415.00/mo | $290.38 |
| SQL Server 2019 Standard Edition 6 Core license (3 x 2 pack) | +$623.00/mo | $435.57 |
| SQL Server 2019 Standard Edition 8 Core license (4 x 2 pack) | +$830.00/mo | $580.76 |
| SQL Server 2019 Standard  (Passive) | included | — |
| SQL Server 2019 Standard  (Passive) | included | — |
| SQL Server 2022 Standard Edition 10 Core license (5 x 2 pack) | +$1,038.00/mo | — |
| SQL Server 2022 Standard Edition 12 Core license (6 x 2 pack) | +$1,245.00/mo | $871.14 |
| SQL Server 2022 Standard Edition 14 Core license (7 x 2 pack) | +$1,452.00/mo | — |
| SQL Server 2022 Standard Edition 16 Core license (8 x 2 pack) | +$1,660.00/mo | $1,161.52 |
| SQL Server 2022 Standard Edition 18 Core license (9 x 2 pack) | +$1,867.00/mo | — |
| SQL Server 2022 Standard Edition 20 Core license (10 x 2 pack) | +$2,075.00/mo | — |
| SQL Server 2022 Standard Edition 22 Core license (11 x 2 pack) | +$2,282.00/mo | — |
| SQL Server 2022 Standard Edition 24 Core license (12 x 2 pack) | +$2,489.00/mo | $1,742.28 |
| SQL Server 2022 Standard Edition 4 Core license (2 x 2 pack) | +$415.00/mo | $290.38 |
| SQL Server 2022 Standard Edition 6 Core license (3 x 2 pack) | +$623.00/mo | $435.57 |
| SQL Server 2022 Standard Edition 8 Core license (4 x 2 pack) | +$830.00/mo | $580.76 |
| Customer Supplied OS | included | — |
| SQL Server 2019 Web Edition 8 Core license (4 x 2 pack) | +$52.00/mo | $36.32 |
| Windows Server 2016 Data Center Edition 10 Core (5 x 2 pack) | +$197.00/mo | — |
| Windows Server 2016 Data Center Edition 12 Core (6 x 2 pack) | +$237.00/mo | — |
| Windows Server 2016 Data Center Edition 16 Core (8 x 2 pack) | +$315.00/mo | — |
| Windows Server 2016 Data Center Edition 20 Core (10 x 2 pack) | +$394.00/mo | — |
| Windows Server 2016 Data Center Edition 24 Core (12 x 2 pack) | +$473.00/mo | $407.36 |
| Windows Server 2016 Data Center Edition 28 Core (14 x 2 pack) | +$552.00/mo | — |
| Windows Server 2016 Data Center Edition 32 Core (16 x 2 pack) | +$630.00/mo | — |
| Windows Server 2016 Data Center Edition 36 Core (18 x 2 pack) | +$709.00/mo | — |
| Windows Server 2016 Data Center Edition 40 Core (20 x 2 pack) | +$788.00/mo | — |
| Windows Server 2016 Data Center Edition 44 Core (22 x 2 pack) | +$866.00/mo | — |
| Windows Server 2016 Data Center Edition 48 Core (24 x 2 pack) | +$945.00/mo | — |
| Windows Server 2016 Data Center Edition 8 Core (min per cpu) | +$194.00/mo | — |
| Windows Server 2016 Standard Edition 10 Core (5 x 2 pack) | +$29.00/mo | $24.48 |
| Windows Server 2016 Standard Edition 12 Core (6 x 2 pack) | +$35.00/mo | $29.37 |
| Windows Server 2016 Standard Edition 14 Core (7 x 2 pack) | +$40.00/mo | — |
| Windows Server 2016 Standard Edition 16 Core (8 x 2 pack) | +$46.00/mo | $39.16 |
| Windows Server 2016 Standard Edition 18 Core (9 x 2 pack) | +$52.00/mo | — |
| Windows Server 2016 Standard Edition 20 Core (10 x 2 pack) | +$57.00/mo | — |
| Windows Server 2016 Standard Edition 24 Core (12 x 2 pack) | +$69.00/mo | $58.74 |
| Windows Server 2016 Standard Edition 28 Core (14 x 2 pack) | +$80.00/mo | — |
| Windows Server 2016 Standard Edition 32 Core (16 x 2 pack) | +$91.00/mo | $78.32 |
| Windows Server 2016 Standard Edition 36 Core (18 x 2 pack) | +$103.00/mo | — |
| Windows Server 2016 Standard Edition 40 Core (20 x 2 pack) | +$114.00/mo | — |
| Windows Server 2016 Standard Edition 44 Core (22 x 2 pack) | +$125.00/mo | — |
| Windows Server 2016 Standard Edition 56 Core (28 x 2 Pack) | +$196.00/mo | — |
| Windows Server 2016 Standard Edition 8 Core  (4 x 2 pack) | +$28.00/mo | $19.60 |
| Windows Server 2019 Data Center Edition 10 Core (5 x 2 pack) | +$197.00/mo | — |
| Windows Server 2019 Data Center Edition 12 Core (6 x 2 pack) | +$237.00/mo | — |
| Windows Server 2019 Data Center Edition 14 Core (7 x 2 pack) | +$276.00/mo | — |
| Windows Server 2019 Data Center Edition 16 Core (8 x 2 pack) | +$315.00/mo | $271.57 |
| Windows Server 2019 Data Center Edition 18 Core (9 x 2 pack) | +$355.00/mo | — |
| Windows Server 2019 Data Center Edition 20 Core (10 x 2 pack) | +$485.00/mo | — |
| Windows Server 2019 Data Center Edition 24 Core (12 x 2 pack) | +$473.00/mo | $407.36 |
| Windows Server 2019 Data Center Edition 28 Core (14 x 2 pack) | +$552.00/mo | — |
| Windows Server 2019 Data Center Edition 32 Core (16 x 2 pack) | +$630.00/mo | — |
| Windows Server 2019 Data Center Edition 36 Core (18 x 2 pack) | +$709.00/mo | — |
| Windows Server 2019 Data Center Edition 40 Core (20 x 2 pack) | +$788.00/mo | — |
| Windows Server 2019 Data Center Edition 44 Core (22 x 2 pack) | +$866.00/mo | — |
| Windows Server 2019 Data Center Edition 48 Core (24 x 2 pack) | +$945.00/mo | — |
| Windows Server 2019 Data Center Edition 8 Core (4 x 2 pack) | +$194.00/mo | $135.79 |
| Windows Server 2019 Standard Edition 10 Core (5 x 2 pack) | +$29.00/mo | $24.48 |
| Windows Server 2019 Standard Edition 12 Core (6 x 2 pack) | +$35.00/mo | $29.37 |
| Windows Server 2019 Standard Edition 14 Core (7 x 2 pack) | +$40.00/mo | — |
| Windows Server 2019 Standard Edition 16 Core (8 x 2 pack) | +$46.00/mo | $39.16 |
| Windows Server 2019 Standard Edition 18 Core (9 x 2 pack) | +$52.00/mo | — |
| Windows Server 2019 Standard Edition 20 Core (10 x 2 pack) | +$57.00/mo | — |
| Windows Server 2019 Standard Edition 22 Core (11 x 2 pack) | +$63.00/mo | — |
| Windows Server 2019 Standard Edition 24 Core (12 x 2 pack) | +$69.00/mo | $58.74 |
| Windows Server 2019 Standard Edition 28 Core (14 x 2 pack) | +$80.00/mo | — |
| Windows Server 2019 Standard Edition 32 Core (16 x 2 pack) | +$91.00/mo | $78.32 |
| Windows Server 2019 Standard Edition 36 Core (18 x 2 pack) | +$103.00/mo | $88.11 |
| Windows Server 2019 Standard Edition 40 Core (20 x 2 pack) | +$114.00/mo | $97.90 |
| Windows Server 2019 Standard Edition 44 Core (22 x 2 pack) | +$125.00/mo | — |
| Windows Server 2019 Standard Edition 48 Core (24 x 2 pack) | +$137.00/mo | — |
| Windows Server 2019 Standard Edition 56 Core (28 x 2 Pack) | +$196.00/mo | — |
| Windows Server 2019 Standard Edition 8 Core (4 x 2 pack) | +$28.00/mo | $19.58 |
| Windows Server DC 2019 for Internal Systems (IT LIcense) | included | — |
| Windows Server  Standard 2019 for Internal Systems (IT LIcense) | included | — |
| Windows Server 2022 Data Center Edition 10 Core (5 x 2 pack) | +$197.00/mo | — |
| Windows Server 2022 Data Center Edition 12 Core (6 x 2 pack) | +$237.00/mo | $203.68 |
| Windows Server 2022 Data Center Edition 14 Core (7 x 2 pack) | +$276.00/mo | — |
| Windows Server 2022 Data Center Edition 16 Core (8 x 2 pack) | +$388.00/mo | — |
| Windows Server 2022 Data Center Edition 16 Core (8 x 2 pack) | +$437.00/mo | — |
| Windows Server 2022 Data Center Edition 20 Core (10 x 2 pack) | +$485.00/mo | $339.40 |
| Windows Server 2022 Data Center Edition 24 Core (12 x 2 pack) | +$473.00/mo | — |
| Windows Server 2022 Data Center Edition 28 Core (14 x 2 pack) | +$552.00/mo | — |
| Windows Server 2022 Data Center Edition 32 Core (16 x 2 pack) | +$630.00/mo | $543.14 |
| Windows Server 2022 Data Center Edition 36 Core (18 x 2 pack) | +$709.00/mo | — |
| Windows Server 2022 Data Center Edition 40 Core (20 x 2 pack) | +$788.00/mo | — |
| Windows Server 2022 Data Center Edition 44 Core (22 x 2 pack) | +$866.00/mo | — |
| Windows Server 2022 Data Center Edition 56 Core (28 x 2 Pack) | +$1,358.00/mo | — |
| Windows Server 2022 Data Center Edition 8 Core (4 x 2 pack) | +$194.00/mo | $135.79 |
| Windows Server 2022 Standard Edition 10 Core (5 x 2 pack) | +$29.00/mo | — |
| Windows Server 2022 Standard Edition 12 Core (6 x 2 pack) | +$35.00/mo | $29.37 |
| Windows Server 2022 Standard Edition 16 Core (8 x 2 pack) | +$46.00/mo | $39.16 |
| Windows Server 2022 Standard Edition 20 Core (10 x 2 pack) | +$57.00/mo | — |
| Windows Server 2022 Standard Edition 24 Core (12 x 2 pack) | +$69.00/mo | $58.74 |
| Windows Server 2022 Standard Edition 28 Core (14 x 2 pack) | +$80.00/mo | $68.53 |
| Windows Server 2022 Standard Edition 32 Core (16 x 2 pack) | +$91.00/mo | $112.00 |
| Windows Server 2022 Standard Edition 36 Core (18 x 2 pack) | +$103.00/mo | — |
| Windows Server 2022 Standard Edition 40 Core (20 x 2 pack) | +$114.00/mo | $140.00 |
| Windows Server 2022 Standard Edition 44 Core (22 x 2 pack) | +$125.00/mo | — |
| Windows Server 2022 Standard Edition 56 Core (28 x 2 Pack) | +$196.00/mo | $196.00 |
| Windows Server 2022 Standard Edition 8 Core (4 x 2 pack) | +$28.00/mo | $19.58 |
| Windows Server 2025 Data Center Edition 10 Core (5 x 2 pack) | +$243.00/mo | — |
| Windows Server 2025 Data Center Edition 12 Core (6 x 2 pack) | included | — |
| Windows Server 2025 Data Center Edition 14 Core (7 x 2 pack) | included | — |
| Windows Server 2025 Data Center Edition 16 Core (8 x 2 Pack) | included | — |
| Windows Server 2025 Data Center Edition 18 Core (9 x 2 Pack) | included | — |
| Windows Server 2025 Data Center Edition 20 Core (10 x 2 pack) | +$485.00/mo | — |
| Windows Server 2025 Data Center Edition 24 Core (12 x 2 pack) | included | — |
| Windows Server 2025 Data Center Edition 28 Core (14 x 2 pack) | included | — |
| Windows Server 2025 Data Center Edition 32 Core (16 x 2 pack) | included | — |
| Windows Server 2025 Data Center Edition 36 Core (18 x 2 pack) | included | — |
| Windows Server 2025 Data Center Edition 40 Core (20 x 2 pack) | included | — |
| Windows Server 2025 Data Center Edition 44 Core (22 x 2 pack) | included | — |
| Windows Server 2025 Data Center Edition 56 Core (28 x 2 Pack) | included | — |
| Windows Server 2025 Data Center Edition 8 Core (4 x 2 pack) | +$194.00/mo | — |
| Windows Server 2025 Standard Edition 10 Core (5 x 2 pack) | included | — |
| Windows Server 2025 Standard Edition 12 Core (6 x 2 pack) | included | — |
| Windows Server 2025 Standard Edition 16 Core (8 x 2 pack) | included | — |
| Windows Server 2025 Standard Edition 18 Core (9 x 2 pack) | included | — |
| Windows Server 2025 Standard Edition 20 Core (10 x 2 pack) | included | — |
| Windows Server 2025 Standard Edition 24 Core (12 x 2 pack) | included | — |
| Windows Server 2025 Standard Edition 28 Core (14 x 2 pack) | included | — |
| Windows Server 2025 Standard Edition 32 Core (16 x 2 pack) | included | — |
| Windows Server 2025 Standard Edition 36 Core (18 x 2 pack) | included | — |
| Windows Server 2025 Standard Edition 40 Core (20 x 2 pack) | included | — |
| Windows Server 2025 Standard Edition 44 Core (22 x 2 pack) | included | — |
| Windows Server 2025 Standard Edition 56 Core (28 x 2 Pack) | +$196.00/mo | — |
| Windows Server 2025 Standard Edition 8 Core (4 x 2 pack) | +$28.00/mo | $28.00 |
| SQL 2016 Enterprise - Passive | included | — |
| SQL 2017 Enterprise - Passive | included | $-1.00 |
| SQL 2017 Enterprise - Passive | included | — |
| 10 pack Windows Remote Desktop Service SAL | +$96.00/mo | $66.90 |
| 1 Windows Remote Desktop Service  SAL | +$10.00/mo | $7.36 |
| 20 pack Windows Remote Desktop Service SAL | +$192.00/mo | $147.18 |
| 5 pack Windows Remote Desktop Service SAL | +$48.00/mo | $36.80 |
| Aptum Essential Monitoring | included | — |

### Support

| Component | MRC Upcharge (USD) | HW Cost (USD) |
|---|---|---|
| Managed OS Patching | included | — |
| SmartKey Opt-in | included | — |
| SmartKey Opt-out | included | — |

---

## Step 5 — Quote Output

### Worked Example: Pro Series 6.0 · IAD · USD · 36 months

| Item | Value | Source |
|---|---|---|
| Server base MRC | $1,699.00/mo | pricebook |
| Default component MRC | $70.00/mo | pricebook (component rows) |
| **Total Customer MRC** | **$1,769.00/mo** | |
| HW CapEx (one-time) | $7,569.00 | ocean_sku_cost sku_id=1254 |
| HW CapEx ÷ 36mo | $210.25/mo | amortization |
| Power (kW) | N/A — kW not in Fusion | cost_drivers.json |
| DC R&M / Supplies | N/A — kW not in Fusion | cost_drivers.json |
| Network | $59.00/mo | cost_drivers.json |
| DC Infra / Ops | $19.00/mo | cost_drivers.json |
| Support (Tech Time) | $40.00/mo | cost_drivers.json |
| SG&A (8.2% of MRC) | $145.06/mo | cost_drivers.json |
| **Total Internal Cost / mo** | **$473.31/mo** | HW amort + overhead |
| **Gross Margin / mo** | **$1,295.69/mo** | MRC − cost |
| **Gross Margin %** | **73.2%** | |

### Formula
```
Customer MRC  = server_mrc + Σ(component_mrc × qty)                [pricebook, target currency]
HW CapEx      = ocean_sku_cost[sku_id=product_id].sku_cost          [MSSQL, cost_currency]
              → converted to display via dimCurrencyExchangeRates
HW CapEx/mo   = HW CapEx ÷ term_months
Overhead      = Σ cost_driver_lines + (MRC × 0.082 SG&A)            [cost_drivers.json, FX-converted]
Total Cost/mo = HW CapEx/mo + Overhead
Margin        = Customer MRC − Total Cost/mo
Margin %      = Margin ÷ Customer MRC × 100
```

---

## Business Rules Cheat Sheet

- **Currency is a free choice** — USD/CAD/GBP/EUR regardless of DC. App queries pricebook in target currency first; FX fallback if no rows.
- **Term never changes MRC or NRC** — all `product_class_contract_length_discounts` are 0% for servers.
- **Term only changes CapEx amortization** — any positive integer works (12/24/36/m2m=1/custom).
- **HW CapEx source:** `ocean_sku_cost WHERE sku_id = product_catalog.id` (server-level) is authoritative. Component-level entries exist but are partial — used as fallback only.
- **Cost currency is not always USD** — `ocean_sku_cost.cost_currency` stores the actual currency; always FX-converted to display.
- **Power cost is always N/A** — kW not stored in Fusion on `product_catalog`.
- **Overhead coverage:** cost_drivers.json covers 7 DCs (ATL, IAD, LAX, MIA, MTL, POR, TOR). All other DCs show $0 overhead.
- **Physical constraints** (CPU sockets, DIMM slots, drive bays) are not in Fusion — hardware spec only.
- **Pricebook queries** must specify `component_id IS NULL` for server rows; component rows join on `component_id`.
