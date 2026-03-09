# Quote E2E — What to put for each case

Run each config below in your Excel/CPQ. Send the **MRC** and **NRC** (screenshot or numbers).  
Cases 1–4 are already filled in. Cases 5–10 are **pending**: they are in the test and **fail until** you provide expected MRC/NRC — then we set `expected_mrc` / `expected_nrc` in `test_quote_e2e.py` and remove the `None` sentinel.

---

## Case 1 — **pro6m_cad_tor_12m** ✓

- **Server:** Pro Series 6.0 - M  
- **Config:** Defaults only (Default Intel Xeon Gold 6526Y 2.9G 16/32T, 128 GB DDR5 RAM, 480 GB SSD, Hardware RAID Controller, Redundant 1100W Power Supply, 1000 Mbit GigE, LM Basic Monitoring)  
- **Currency:** CAD | **DC:** Toronto | **Term:** 12 months  
- Expected: MRC 1249, NRC 1249  

---

## Case 2 — **pro6m_cad_tor_24m** ✓

- Same as Case 1, **Term:** 24 months  
- Expected: MRC 969, NRC 1249  

---

## Case 3 — **pro6m_cad_tor_36m** ✓

- Same as Case 1, **Term:** 36 months  
- Expected: MRC 829, NRC 1249  

---

## Case 4 — **adv6m_cpu_drives_cad** ✓

- **Server:** Advanced Series 6.0 - M  
- **Config:** Default CPU (Default Intel Xeon Silver 4514Y 2G 16C/32T), 64 GB DDR5 RAM, 480 GB SSD, Hardware RAID Controller, Redundant 1100W Power Supply, 1000 Mbit GigE, LM Basic Monitoring  
- **Add-ons:** 2× Intel Xeon Gold 6526Y 2.9G, 16/32T | 2× 1.92 TB SATA 2.5in SSD  
- **Currency:** CAD | **DC:** Toronto | **Term:** 12 months  
- Expected: MRC 1789, NRC 969  

---

## Case 5 — **pro6m_usd_iad_12m** ✓

- **Server:** Pro Series 6.0 - M  
- **Config:** Same defaults as Case 1  
- **Currency:** USD | **DC:** IAD (Washington DC) | **Term:** 12 months  
- Expected: MRC 1079, NRC 1079 (from screenshot)

---

## Case 6 — **pro6m_gbp_por_24m** ✓

- **Server:** Pro Series 6.0 - M  
- **Config:** Same defaults as Case 1  
- **Currency:** GBP | **DC:** POR (Portsmouth) | **Term:** 24 months  
- Expected: MRC 659, NRC 899 (from screenshot). *No tolerance — test fails until seed/quote matches (quote returns 699 MRC).*

---

## Case 7 — **cluster5_cad_tor_12m** (PENDING)

- **Server:** Cluster 5.0 (Dell R440)  
- **Config:** Default config only  
- **Currency:** CAD | **DC:** Toronto | **Term:** 12 months  

**→ Give me: MRC = ______  NRC = ______**

---

## Case 7b — **atomic5_cad_tor_12m** (PENDING)

- **Server:** Atomic 5.0 (Dell R650xs)  
- **Config:** Default config only  
- **Currency:** CAD | **DC:** Toronto | **Term:** 12 months  

**→ Give me: MRC = ______  NRC = ______**

---

## Case 8 — **adv6m_sql_lm_standard_cad** (PENDING)  
*(SQL Server value under review — do not update test expected yet.)*

- **Server:** Advanced Series 6.0 - M  
- **Config:** Defaults + **SQL Server 2022 Standard Edition** (×1) + **LM Standard Monitoring** (×1)  
- **Currency:** CAD | **DC:** Toronto | **Term:** 12 months  

**→ Give me: MRC = ______  NRC = ______**

---

## Case 9 — **pro6m_storage_heavy_cad** ✓ (Sheet vs DB + 12m margin)

- **Server:** Pro Series 6.0 - M  
- **Config:** Defaults + **4× 1.92 TB SATA 2.5in SSD**  
- **Currency:** CAD | **DC:** Toronto | **Term:** 12 months  
- **Expected (from sheet):** MRC 1,529  NRC 1,249  (mrc_tolerance 10; quote ~1522 vs sheet 1529)
- **expected_sheet** used for Sheet vs DB: Capex (server) USD, Watts, Power (monthly) CAD. E2E run prints **Sheet vs DB** and **12-month financial summary** (revenue, capex, overhead, margin $ and %) for this case.

---

## Case 10 — **pro6_vhost_cad_tor_12m** (PENDING)

- **Server:** Pro Series 6.0 **vHost** (not -M)  
- **Config:** Default config only  
- **Currency:** CAD | **DC:** Toronto | **Term:** 12 months  

**→ Give me: MRC = ______  NRC = ______**

---

The test run writes **component costs** and **overhead breakdown** into `tests/outputs/quote_e2e_results.json` and prints them in the console. Once you send MRC/NRC for a pending case, we set `expected_mrc` and `expected_nrc` in `QUOTE_CASES` in `test_quote_e2e.py` (and remove the `None` values) so that case starts passing.

---

**Notes (from CPQ sheet review):**

- **Watts:** Quote now uses server-level watts from `server_specs.watts` (per CPQ sheet, e.g. 400 for Pro 6.0 - M) when set; otherwise falls back to sum of component watts. Seed/migration backfills watts from 01_servers.
- **Invalid config:** The sheet can flag invalid configs (e.g. CPU/drive count vs sockets/bays). Quote builder does not yet enforce these; consider adding validation so invalid configs are rejected or flagged.
- **VMware licensing:** vHost orders include VMware (per-core, etc.). Not yet modeled in the quote builder; add when tackling VMware complexity.
