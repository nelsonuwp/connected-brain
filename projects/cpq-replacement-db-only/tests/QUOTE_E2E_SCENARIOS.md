# Quote E2E — What to put for each case

Run each config below in your Excel/CPQ. Send the **MRC** and **NRC** (screenshot or numbers) and we’ll plug them in as `expected_mrc` / `expected_nrc` in `test_quote_e2e.py`.

---

## Case 1 — **pro6m_cad_tor_12m**

- **Server:** Pro Series 6.0 - M  
- **Config:** Defaults only (Default Intel Xeon Gold 6526Y 2.9G 16/32T, 128 GB DDR5 RAM, 480 GB SSD, Hardware RAID Controller, Redundant 1100W Power Supply, 1000 Mbit GigE, LM Basic Monitoring)  
- **Currency:** CAD  
- **DC:** Toronto  
- **Term:** 12 months  

**→ Give me: MRC = ______  NRC = ______**

---

## Case 2 — **pro6m_cad_tor_24m**

- Same as Case 1, **Term:** 24 months  

**→ Give me: MRC = ______  NRC = ______**

---

## Case 3 — **pro6m_cad_tor_36m**

- Same as Case 1, **Term:** 36 months  

**→ Give me: MRC = ______  NRC = ______**

---

## Case 4 — **adv6m_cpu_drives_cad**

- **Server:** Advanced Series 6.0 - M  
- **Config:** Default CPU (Default Intel Xeon Silver 4514Y 2G 16C/32T), 64 GB DDR5 RAM, 480 GB SSD, Hardware RAID Controller, Redundant 1100W Power Supply, 1000 Mbit GigE, LM Basic Monitoring  
- **Add-ons:**  
  - CPU upgrade: **2×** Intel Xeon Gold 6526Y 2.9G, 16/32T  
  - Drives: **2×** 1.92 TB SATA 2.5in SSD (raid 1.92 TB)  
- **Currency:** CAD  
- **DC:** Toronto  
- **Term:** 12 months  

**→ Give me: MRC = ______  NRC = ______**

---

## Adding more cases

For any new scenario:

1. Run the exact config in Excel (server + components + currency + DC + term).  
2. Send MRC and NRC (and a short label, e.g. “Pro 6 vHost GBP 24mo”).  
3. I’ll add a new entry to `QUOTE_CASES` in `test_quote_e2e.py` with that config and your expected values.

The test run writes **component costs** (each line item and addon) and **overhead breakdown** (wattage, power, network, colo, etc.) into `tests/outputs/quote_e2e_results.json` and prints them in the console.
