from datetime import date
from lib.renewal_pricing import hw_paid_off, provision_age_months, calc_suggested_mrc


def test_hw_paid_off_exactly_36_months():
    today = date(2026, 5, 22)
    prov = date(2023, 5, 22)
    assert hw_paid_off(prov, today=today) is True


def test_hw_not_paid_off_35_months():
    today = date(2026, 5, 22)
    prov = date(2023, 6, 22)
    assert hw_paid_off(prov, today=today) is False


def test_hw_paid_off_none_provision():
    assert hw_paid_off(None) is False


def test_provision_age_months():
    today = date(2026, 5, 22)
    prov = date(2024, 5, 22)
    assert provision_age_months(prov, today=today) == 24


def test_calc_suggested_mrc_term_no_multiplier():
    components = [
        {"component_category": "Hardware", "component_mrc": 40.0, "new_mrc": 40.0},
        {"component_category": "Software", "component_mrc": 85.0, "new_mrc": 185.0},
    ]
    result = calc_suggested_mrc(323.0, components, "36")
    # 323 + 40 (HW held flat) + 185 (new SW price) = 548, × 1.0
    assert result == 548.0


def test_calc_suggested_mrc_m2m_multiplier():
    components = [
        {"component_category": "Software", "component_mrc": 85.0, "new_mrc": 85.0},
    ]
    result = calc_suggested_mrc(323.0, components, "m2m")
    # (323 + 85) × 1.25 = 510.0
    assert result == 510.0


def test_calc_suggested_mrc_missing_new_price_falls_back():
    components = [
        {"component_category": "Software", "component_mrc": 85.0, "new_mrc": None},
    ]
    result = calc_suggested_mrc(323.0, components, "36")
    # Falls back to current_mrc when new_mrc is None
    assert result == 408.0


def test_calc_suggested_mrc_support_repriced():
    components = [
        {"component_category": "Support", "component_mrc": 0.0, "new_mrc": 50.0},
    ]
    result = calc_suggested_mrc(500.0, components, "12")
    assert result == 550.0
