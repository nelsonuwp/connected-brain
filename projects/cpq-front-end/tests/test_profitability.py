from datetime import date
from db.profitability import calc_service_margin
from lib.overhead import COST_DRIVERS


def test_calc_service_margin_with_hw_not_paid_off():
    # ATL server: power=337/kW, network_eq=59, dc_ops=21, support_ops=40, sga=8.2%
    # 1200W = 1.2kW, power = 1.2 * 337 = 404.4
    # direct = 404.4 + 0 + 59 + 21 + 40 + 0 + 0 = 524.4
    # sga = 5000 * 0.082 = 410.0
    # hw_amortized = 72000 / 36 = 2000.0
    # total_cost = 2000.0 + 524.4 + 410.0 = 2934.4
    # margin = 5000 - 2934.4 = 2065.6
    result = calc_service_margin(
        mrc=5000.0,
        dc_code="ATL",
        hw_capex_in_currency=72000.0,
        watts=1200,
        fx_overhead=1.0,
        provision_date=date(2024, 1, 1),
    )
    assert result["hw_amortized"] == 2000.0
    assert result["total_cost"] == 2934.4
    assert result["margin"] == 2065.6
    assert result["margin_pct"] == 41.3
    assert result["hw_paid_off"] is False
    assert result["hw_months_remaining"] is not None
    assert result["biggest_cost_driver"] == "hw_amortized"


def test_calc_service_margin_hw_paid_off():
    # provision_date > 36 months ago — hw_amortized = 0
    result = calc_service_margin(
        mrc=5000.0,
        dc_code="ATL",
        hw_capex_in_currency=72000.0,
        watts=1200,
        fx_overhead=1.0,
        provision_date=date(2020, 1, 1),
    )
    assert result["hw_amortized"] == 0.0
    assert result["hw_paid_off"] is True


def test_calc_service_margin_no_watts():
    # Without watts, power_per_kw line is None, should be treated as 0 in total
    result = calc_service_margin(
        mrc=5000.0,
        dc_code="ATL",
        hw_capex_in_currency=0.0,
        watts=None,
        fx_overhead=1.0,
        provision_date=date(2024, 1, 1),
    )
    assert result["margin"] == round(5000.0 - result["total_cost"], 2)


def test_calc_service_margin_no_provision_date():
    # No provision date → hw not paid off (conservative assumption), age_months None
    result = calc_service_margin(
        mrc=5000.0,
        dc_code="ATL",
        hw_capex_in_currency=36000.0,
        watts=None,
        fx_overhead=1.0,
        provision_date=None,
    )
    assert result["hw_paid_off"] is False
    assert result["hw_months_remaining"] is None


def test_calc_service_margin_unknown_dc():
    # Unknown DC → calc_overhead returns {} → only sga and hw_amortized
    result = calc_service_margin(
        mrc=5000.0,
        dc_code="NOTADC",
        hw_capex_in_currency=36000.0,
        watts=None,
        fx_overhead=1.0,
        provision_date=date(2024, 1, 1),
    )
    sga = round(5000.0 * COST_DRIVERS["overhead_constants"]["sga_pct"], 2)
    hw = round(36000.0 / 36, 2)
    assert result["total_cost"] == round(hw + sga, 2)


def test_calc_service_margin_fx_overhead():
    # fx_overhead=1.3 should scale all overhead amounts (but not hw_amortized)
    r_1x = calc_service_margin(
        mrc=5000.0, dc_code="ATL", hw_capex_in_currency=0.0,
        watts=1200, fx_overhead=1.0, provision_date=date(2020, 1, 1),
    )
    r_fx = calc_service_margin(
        mrc=5000.0, dc_code="ATL", hw_capex_in_currency=0.0,
        watts=1200, fx_overhead=1.3, provision_date=date(2020, 1, 1),
    )
    # overhead lines (not sga, not hw) should be scaled
    assert r_fx["overhead"]["power_per_kw"] == round(r_1x["overhead"]["power_per_kw"] * 1.3, 2)
