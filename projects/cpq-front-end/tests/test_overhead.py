import json
from lib.overhead import calc_overhead, COST_DRIVERS


def test_cost_drivers_loads():
    assert "overhead_constants" in COST_DRIVERS
    assert "data_centers" in COST_DRIVERS


def test_sga_calculation():
    # SGA is a percentage of MRC — verify it scales linearly
    result = calc_overhead("ATL", 1000.0, fx_rate=1.0)
    assert "sga" in result
    sga_pct = COST_DRIVERS["overhead_constants"]["sga_pct"]
    assert result["sga"]["amount"] == round(1000.0 * sga_pct, 2)


def test_unknown_dc_returns_empty():
    result = calc_overhead("NOTADC", 1000.0)
    assert result == {}


def test_fx_rate_applied_to_fixed_costs():
    result_1x = calc_overhead("ATL", 1000.0, fx_rate=1.0)
    result_2x = calc_overhead("ATL", 1000.0, fx_rate=2.0)
    for key in result_1x:
        if key == "sga":
            continue  # SGA is based on MRC, not a fixed amount
        if result_1x[key]["amount"] and result_1x[key]["amount"] > 0:
            assert result_2x[key]["amount"] == round(result_1x[key]["amount"] * 2, 2)
