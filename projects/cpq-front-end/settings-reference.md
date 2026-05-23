# Settings Reference: Overhead Rate Configuration

> **Last updated:** 2026-05-23
> **Scope:** The Settings page — viewing and editing the overhead cost rates used by both New Quotes and Renewals.
> **Code base:** `routes/settings.py` + `lib/overhead.py` + `cost_drivers.json` + `templates/settings.html`

---

## Table of Contents

1. [What Settings Controls](#1-what-settings-controls)
2. [Data Source: `cost_drivers.json`](#2-data-source-cost_driversjson)
3. [File Structure](#3-file-structure)
4. [DC Coverage](#4-dc-coverage)
5. [How to Update](#5-how-to-update)
6. [Known Gaps](#6-known-gaps)

---

## 1. What Settings Controls

The Settings page (`/settings`) is the in-app UI for viewing and editing `cost_drivers.json` — the single file that defines overhead cost rates for every DC. These rates feed into the cost breakdown in both:

- **New Quotes** — the overhead / cost section on the product configurator page
- **Renewals** — the overhead lines in every renewal scenario (m2m, 12, 24, 36 months)

Changes saved through the Settings UI take effect **immediately** — no app restart is needed. The app reloads the file into memory the moment a save is confirmed.

The Settings page does **not** connect to any external database. It reads and writes `cost_drivers.json` only.

---

## 2. Data Source: `cost_drivers.json`

`cost_drivers.json` is a local file at the root of the project. It is **not stored in any database**. It is the single source of truth for:

- Per-DC overhead rates (broken down by cost line and service type)
- Native currency per DC (used to FX-convert overhead amounts when the service/quote currency differs)
- The global SG&A percentage applied to all MRC totals

The file is version-controlled in the project repository. The Settings UI writes changes to this file atomically (writes to a `.tmp` file first, then renames it to `cost_drivers.json`) so a failed save never corrupts the existing data.

---

## 3. File Structure

The file has four top-level keys:

```
{
  "version":            "2026-05-13",
  "notes":              "Human-readable notes...",
  "overhead_constants": { "sga_pct": 0.082 },
  "data_centers":       { "ATL": {...}, "IAD": {...}, ... }
}
```

### `overhead_constants`

| Key       | Type    | Meaning                                                                                 | Example      |
| --------- | ------- | --------------------------------------------------------------------------------------- | ------------ |
| `sga_pct` | decimal | SG&A as a fraction of total MRC. Applied to every quote and renewal, all DCs.           | `0.082` = 8.2% |

This is the only global constant. It is not per-DC. Changing it affects all cost calculations immediately.

### `data_centers`

Each key is a **DC code** used internally by the app (e.g., `"ATL"`, `"IAD"`, `"TOR"`). These codes must match the DC abbreviations used in `cost_drivers.json` lookups — they are **not always the same as Fusion's `dc_abbr`**. See the DC Coverage table below for the mapping.

Each DC entry has:

| Field            | Type    | Meaning                                                                                                                           |
| ---------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `name`           | string  | Human-readable DC name (display only)                                                                                             |
| `native_currency`| string  | The DC's billing currency (e.g., `"USD"`, `"CAD"`, `"GBP"`). All `costs` amounts are expressed in this currency.                 |
| `fusion_dc_id`   | integer | The `id` from Fusion's `public.sb_datacenter`. Used in Renewals to match MSSQL DC codes (e.g., `"IAD2"`) to this file's DC code (e.g., `"IAD"`). Must be correct or overhead won't apply to Renewals services in that DC. |
| `fusion_dc_abbr` | string  | The `dc_abbr` from Fusion (only present where it differs from the file key). Documentation only — not used in code.               |
| `costs`          | object  | Cost lines per service type. See below.                                                                                           |

### `costs` — service types

Each DC has three service types: `server`, `firewall`, `switch`. Each service type has the same set of cost lines:

| Key                 | Measure      | Meaning                                                                                           |
| ------------------- | ------------ | ------------------------------------------------------------------------------------------------- |
| `power_per_kw`      | `per_kw`     | Power cost per kilowatt of draw. Multiplied by the server's wattage (from `hardware_watts` ÷ 1000). Shows N/A if wattage unknown. |
| `dc_equipment`      | `per_device` | DC equipment/supplies cost per device per month.                                                  |
| `network_equipment` | `per_device` | Network equipment cost per device per month.                                                      |
| `dc_ops`            | `per_device` | DC operations/infrastructure cost per device per month.                                           |
| `support_ops`       | `per_device` | Technical support labor cost per device per month.                                                |
| `network_ops`       | `per_device` | Network operations people cost per device per month. (Currently $0 — pending data.)              |
| `compute_ops`       | `per_device` | Compute team people cost per device per month. (Currently $0 — pending data.)                    |

Each line item has:

```json
{
  "amount":  59,
  "measure": "per_device"
}
```

- `amount`: the cost in the DC's **native currency** (not USD unless the DC's native currency is USD)
- `measure`: how the amount is applied (`per_kw` or `per_device`)

**Zero-amount lines** are valid and intentional — they mean "this cost exists but the rate hasn't been determined yet." They display as $0 in the cost breakdown, not as N/A.

### Example: IAD (Herndon, USD)

```json
"IAD": {
  "name": "Herndon (Washington DC)",
  "native_currency": "USD",
  "fusion_dc_id": 8,
  "fusion_dc_abbr": "IAD2",
  "costs": {
    "server": {
      "power_per_kw":      { "amount": 110, "measure": "per_kw" },
      "dc_equipment":      { "amount": 0,   "measure": "per_device" },
      "network_equipment": { "amount": 59,  "measure": "per_device" },
      "dc_ops":            { "amount": 19,  "measure": "per_device" },
      "support_ops":       { "amount": 40,  "measure": "per_device" },
      "network_ops":       { "amount": 0,   "measure": "per_device" },
      "compute_ops":       { "amount": 0,   "measure": "per_device" }
    },
    "firewall": { ...same structure... },
    "switch":   { ...same structure... }
  }
}
```

For a server quoted at IAD in CAD, the app would:
1. Look up `cost_drivers.json["IAD"]`
2. Apply each `server` cost line in USD (native)
3. FX-convert the total from USD → CAD using the live rate from `dimCurrencyExchangeRates`
4. Add SG&A: `suggested_mrc × 0.082`

---

## 4. DC Coverage

7 DCs currently have overhead rates in `cost_drivers.json`. Services or quotes for any other DC will show **$0 overhead** in all cost breakdowns — this understates internal cost and inflates apparent margin.


| File key | Fusion `dc_abbr` | Fusion `dc_id` | City                    | Native currency | Power rate ($/kW) | Network equip ($/device) | DC Ops ($/device) | Support ($/device) |
| -------- | ---------------- | -------------- | ----------------------- | --------------- | ----------------- | ------------------------ | ----------------- | ------------------- |
| ATL      | ATL              | 1              | Atlanta, GA             | USD             | $337              | $59                      | $21               | $40                 |
| IAD      | IAD2             | 8              | Herndon (Washington DC) | USD             | $110              | $59                      | $19               | $40                 |
| LAX      | LAX1             | 7              | Los Angeles, CA         | USD             | $457              | $59                      | $21               | $40                 |
| MIA      | MIA              | 2              | Miami, FL               | USD             | $48               | $59                      | $28               | $40                 |
| MTL      | MTL-BH           | 42             | Montreal, QC            | CAD             | $253 CAD          | $0                       | $0                | $40 CAD             |
| POR      | POR              | 13             | Portsmouth, UK          | GBP             | £46               | £59                      | £27               | £40                 |
| TOR      | TOR              | 12             | Toronto, ON             | CAD             | $253 CAD          | $0                       | $0                | $40 CAD             |

> Notes: MTL and TOR currently have $0 for `network_equipment` and `dc_ops`. These are pending data, not absent costs.

DCs with active services or pricebook rows that are **not** in this table (LDN1, CRO, GOS, SAT5, and others) will show $0 overhead until rates are added.

---

## 5. How to Update

### Via the Settings UI (`/settings`)

1. Navigate to the Settings tab in the app
2. Edit the rate values in the form fields
3. Click Save
4. Changes take effect immediately — no restart needed

The UI validates:
- `sga_pct` must be between 0 and 1 (e.g., enter `0.082` for 8.2%, not `8.2`)
- All `amount` values must be ≥ 0

### Via direct file edit

Open `cost_drivers.json` at the project root in any text editor. Changes take effect after the next save through the Settings UI (which triggers a reload), or on the next app restart.

### Adding a new DC

Adding a DC requires a direct file edit — the Settings UI does not support adding new DC entries.

1. Add a new key under `data_centers` using the **app DC code** (the short abbreviation the app uses internally, e.g., `"CRO"` not `"Croydon"`)
2. Set `fusion_dc_id` to match `public.sb_datacenter.id` in Fusion — this is critical for Renewals to correctly match MSSQL DC codes to overhead rates
3. Set `native_currency` to the DC's billing currency
4. Add all seven cost line items under `costs.server`, `costs.firewall`, and `costs.switch`
5. Set any unknown rates to `0` rather than omitting them — omitting a key may cause errors

### Changing overhead line key names

**Do not rename the existing line item keys** (`power_per_kw`, `dc_equipment`, `network_equipment`, `dc_ops`, `support_ops`, `network_ops`, `compute_ops`). The calculation code in `lib/overhead.py` iterates over whatever keys are present in the file — renaming a key doesn't break it, but the Settings UI displays them by key name, so any rename would require a corresponding UI update to display correctly.

---

## 6. Known Gaps


| #  | Gap                                                | Current behavior                                                                                                   | Correct / desired behavior                                                                                                                          |
| -- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1  | Only 7 DCs have overhead rates                     | All other DCs show $0 overhead — margin calculations are understated for any service or quote in those DCs         | Finance overhead rates need to be collected and added for all DCs where active services or pricebook rows exist (LDN1, CRO, GOS, SAT5, and others) |
| 2  | No UI for adding a new DC entry                    | Adding a DC requires a direct JSON edit                                                                            | Settings UI could support adding/removing DC entries without requiring file-level access                                                            |
| 3  | No audit trail                                     | There is no log of who changed which rate and when                                                                 | Overhead rate changes should be audited — at minimum, changes should be committed to version control with a descriptive message                     |
| 4  | `fusion_dc_id` not validated on save               | A wrong `fusion_dc_id` silently breaks DC-to-overhead matching in Renewals (MSSQL uses `dc_abbr` like `"IAD2"`; the app looks up `fusion_dc_id` to match the right cost_drivers.json entry) | Settings UI or save validation could check that `fusion_dc_id` values match a known Fusion DC                                                       |
| 5  | People cost lines are all $0                       | `network_ops` and `compute_ops` are $0 for all DCs — these are real costs not yet quantified                       | Finance team to provide per-DC people cost allocations so internal cost totals are accurate                                                          |
| 6  | `dc_equipment` is $0 for most DCs                  | Likely a placeholder — may represent real costs not yet allocated                                                  | Finance to confirm whether these should be $0 or populated                                                                                          |
| 7  | Overhead data lives in a local file, not a database | If multiple app instances ran in different environments, they could have different overhead rates                   | Long-term: move overhead rates to a database table so they are environment-independent and properly audited                                          |
