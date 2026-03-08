# Quote E2E — Test scenarios

The suite in `test_quote_e2e.py` asserts expected MRC/NRC for fixed configs. Add new cases to `QUOTE_CASES` and set `expected_mrc` / `expected_nrc` from your Excel/CPQ output.

## Current cases (from user spec)

| # | Config | Currency | DC | Term | Expected MRC | Expected NRC |
|---|--------|----------|-----|------|--------------|--------------|
| 1 | Pro Series 6.0 - M (defaults only) | CAD | TOR | 12 mo | 1249 | 1249 |
| 2 | Same | CAD | TOR | 24 mo | 969 | 1249 |
| 3 | Same | CAD | TOR | 36 mo | 829 | 1249 |
| 4 | Advanced Series 6.0 - M + 2× Gold 6526Y CPU + 2× 1.92 TB SSD | CAD | TOR | 12 mo | 1789 | 969 |

## Suggested stress tests (add to Excel, then add here)

- **Different DCs** — Same server/config in USD (e.g. IAD) and GBP (POR); confirm server pricing and FX for addons.
- **Promo / min term** — Promo Server - NA or UK, 12 mo only; NRC vs MRC.
- **Software add-ons** — e.g. SQL Server 2022 Standard, LM Standard Monitoring; confirm MRC and that software markup is applied if applicable.
- **Multi-currency** — Pro 6.0 - M in GBP, 24 mo; expected from Excel.
- **Storage-heavy** — Same server with multiple large drives (e.g. 4× 7.6 TB) to stress addon sum and wattage.
- **vHost vs -M** — Pro Series 6.0 vHost vs Pro Series 6.0 - M same config; different base price.

To add a case: run the config in Excel, note MRC/NRC, then append to `QUOTE_CASES` in `test_quote_e2e.py` with the same structure. Use `mrc_tolerance` / `nrc_tolerance` if FX rounding is needed for converted addons.
