"""
One-time migration: cost_drivers.json flat-per-DC → service-type-nested.

Changes:
- Each DC's `costs` becomes { "server": {...}, "firewall": {...}, "switch": {...} }
- 8 cost keys kept; billing_collections, supply_chain, support_tech_rate dropped
- support_cost added: amount = support_tech_rate.amount * support_hours_per_server
- All per_server measures renamed to per_device
- overhead_constants.support_hours_per_server removed
"""

import json
import os
from pathlib import Path

SRC = Path(__file__).parent / "cost_drivers.json"
DST = Path(__file__).parent / "cost_drivers.json"
TMP = Path(__file__).parent / "cost_drivers.json.tmp"

KEEP_KEYS = [
    "power_per_kw",
    "dc_rm_supplies",
    "network",
    "dc_infra_operations",
    "dc_people",
    "network_people",
    "compute_team",
]
SERVICE_TYPES = ["server", "firewall", "switch"]


def migrate(old: dict) -> dict:
    hours = old["overhead_constants"].get("support_hours_per_server", 0.5)

    new_constants = {k: v for k, v in old["overhead_constants"].items()
                     if k != "support_hours_per_server"}

    new_dcs = {}
    for dc_abbr, dc in old["data_centers"].items():
        old_costs = dc["costs"]
        support_rate = old_costs.get("support_tech_rate", {}).get("amount", 0)
        support_amount = round(support_rate * hours, 2)

        per_type = {}
        for key in KEEP_KEYS:
            entry = old_costs.get(key, {})
            per_type[key] = {
                "amount":  entry.get("amount", 0),
                "measure": "per_kw" if entry.get("measure") == "per_kw" else "per_device",
            }
        per_type["support_cost"] = {"amount": support_amount, "measure": "per_device"}

        # Canonical key order
        ordered = {k: per_type[k] for k in [
            "power_per_kw", "dc_rm_supplies", "network", "dc_infra_operations",
            "support_cost", "dc_people", "network_people", "compute_team",
        ]}

        new_dcs[dc_abbr] = {
            k: v for k, v in dc.items() if k != "costs"
        }
        new_dcs[dc_abbr]["costs"] = {
            svc: {k: dict(v) for k, v in ordered.items()}
            for svc in SERVICE_TYPES
        }

    return {
        "version":           old.get("version", ""),
        "notes":             old.get("notes", ""),
        "overhead_constants": new_constants,
        "data_centers":       new_dcs,
    }


if __name__ == "__main__":
    with open(SRC) as f:
        old = json.load(f)

    new = migrate(old)

    # Preview one DC before writing
    sample_dc = next(iter(new["data_centers"]))
    print(f"=== Preview: {sample_dc} ===")
    print(json.dumps({sample_dc: new["data_centers"][sample_dc]}, indent=2))
    print("\n=== overhead_constants ===")
    print(json.dumps(new["overhead_constants"], indent=2))

    confirm = input("\nWrite to cost_drivers.json? [y/N] ").strip().lower()
    if confirm != "y":
        print("Aborted.")
    else:
        with open(TMP, "w") as f:
            json.dump(new, f, indent=2)
            f.write("\n")
        os.replace(TMP, DST)
        print(f"Written to {DST}")
