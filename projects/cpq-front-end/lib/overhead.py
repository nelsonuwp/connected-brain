import json
from pathlib import Path

_COST_DRIVERS_PATH = Path(__file__).parent.parent / "cost_drivers.json"
COST_DRIVERS = {}


def _load():
    global COST_DRIVERS
    with open(_COST_DRIVERS_PATH) as f:
        COST_DRIVERS = json.load(f)


def reload():
    _load()


_load()


def calc_overhead(dc_code: str, mrc_display: float, fx_rate: float = 1.0,
                  kw: float | None = None, service_type: str = "server") -> dict:
    dc = COST_DRIVERS["data_centers"].get(dc_code)
    if not dc:
        return {}
    dc_costs = dc["costs"]
    if isinstance(next(iter(dc_costs.values())), dict) and "amount" not in next(iter(dc_costs.values())):
        # Multi-type schema: try exact match, then case-insensitive substring match
        costs = dc_costs.get(service_type)
        if costs is None and service_type:
            lower = service_type.lower()
            for key in dc_costs:
                if key in lower or lower in key:
                    costs = dc_costs[key]
                    break
        costs = costs or {}
    else:
        costs = dc_costs
    const = COST_DRIVERS["overhead_constants"]
    native = dc["native_currency"]
    lines = {}

    for key, entry in costs.items():
        amt = entry["amount"]
        measure = entry["measure"]
        if amt == 0:
            lines[key] = {
                "amount": 0, "currency": native, "measure": measure,
                "provenance": {
                    "source": "cost_drivers.json",
                    "path": f"data_centers.{dc_code}.costs.{service_type}.{key}",
                    "native_amount": 0, "native_currency": native,
                    "formula": "0 — not configured",
                },
            }
            continue

        if measure == "per_kw":
            if kw is None:
                native_val = None
                formula = f"{amt} {native}/kW × kW unknown = N/A"
            else:
                native_val = round(amt * kw, 2)
                formula = f"{amt} {native}/kW × {kw} kW = {native_val} {native}"
        elif measure in ("per_device", "per_server"):
            native_val = round(amt, 2)
            formula = f"{amt} {native}/device"
        else:
            native_val = round(amt, 2)
            formula = str(amt)

        display_val = round(native_val * fx_rate, 2) if native_val is not None else None
        if fx_rate != 1.0 and native_val is not None:
            formula += f" × {fx_rate} FX = {display_val}"

        lines[key] = {
            "amount": display_val,
            "currency": native,
            "measure": measure,
            "provenance": {
                "source": "cost_drivers.json",
                "path": f"data_centers.{dc_code}.costs.{service_type}.{key}",
                "native_amount": native_val,
                "native_currency": native,
                "formula": formula,
                "fx_rate": fx_rate,
            },
        }

    sga_pct = const["sga_pct"]
    sga_val = round(mrc_display * sga_pct, 2) if mrc_display else 0
    lines["sga"] = {
        "amount": sga_val,
        "currency": native,
        "measure": "pct_of_mrc",
        "provenance": {
            "source": "cost_drivers.json",
            "path": "overhead_constants.sga_pct",
            "formula": f"Total MRC {mrc_display} × {sga_pct} (SG&A %) = {sga_val}",
            "fx_rate": fx_rate,
        },
    }
    return lines
