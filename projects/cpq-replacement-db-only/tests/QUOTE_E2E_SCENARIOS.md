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

## Case 5 — **pro6m_usd_iad_12m** (PENDING)

- **Server:** Pro Series 6.0 - M  
- **Config:** Same defaults as Case 1  
- **Currency:** USD | **DC:** IAD (Washington DC) | **Term:** 12 months  

**→ Give me: MRC = ______  NRC = ______**

---

## Case 6 — **pro6m_gbp_por_24m** (PENDING)

- **Server:** Pro Series 6.0 - M  
- **Config:** Same defaults as Case 1  
- **Currency:** GBP | **DC:** POR (Portsmouth) | **Term:** 24 months  

**→ Give me: MRC = ______  NRC = ______**

---

## Case 7 — **promo_na_usd_iad_12m** (PENDING)

- **Server:** Promo Server - NA  
- **Config:** Default config only (no add-ons)  
- **Currency:** USD | **DC:** IAD | **Term:** 12 months (min term for promo)  

**→ Give me: MRC = ______  NRC = ______**

---

## Case 8 — **adv6m_sql_lm_standard_cad** (PENDING)

- **Server:** Advanced Series 6.0 - M  
- **Config:** Defaults + **SQL Server 2022 Standard Edition** (×1) + **LM Standard Monitoring** (×1)  
- **Currency:** CAD | **DC:** Toronto | **Term:** 12 months  

**→ Give me: MRC = ______  NRC = ______**

---

## Case 9 — **pro6m_storage_heavy_cad** (PENDING)

- **Server:** Pro Series 6.0 - M  
- **Config:** Defaults + **4× 1.92 TB SATA 2.5in SSD**  
- **Currency:** CAD | **DC:** Toronto | **Term:** 12 months  

**→ Give me: MRC = ______  NRC = ______**

---

## Case 10 — **pro6_vhost_cad_tor_12m** (PENDING)

- **Server:** Pro Series 6.0 **vHost** (not -M)  
- **Config:** Default config only  
- **Currency:** CAD | **DC:** Toronto | **Term:** 12 months  

**→ Give me: MRC = ______  NRC = ______**

---

The test run writes **component costs** and **overhead breakdown** into `tests/outputs/quote_e2e_results.json` and prints them in the console. Once you send MRC/NRC for a pending case, we set `expected_mrc` and `expected_nrc` in `QUOTE_CASES` in `test_quote_e2e.py` (and remove the `None` values) so that case starts passing.
