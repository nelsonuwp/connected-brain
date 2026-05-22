from datetime import date, datetime

_SW_SUPPORT_CATS = {"Software", "Support"}


def hw_paid_off(provision_date, today: date | None = None) -> bool:
    if provision_date is None:
        return False
    if today is None:
        today = date.today()
    if isinstance(provision_date, datetime):
        provision_date = provision_date.date()
    months = (today.year - provision_date.year) * 12 + (today.month - provision_date.month)
    return months >= 36


def provision_age_months(provision_date, today: date | None = None) -> int | None:
    if provision_date is None:
        return None
    if today is None:
        today = date.today()
    if isinstance(provision_date, datetime):
        provision_date = provision_date.date()
    return (today.year - provision_date.year) * 12 + (today.month - provision_date.month)


def calc_suggested_mrc(product_mrc: float, components: list, term: str) -> float:
    """
    Calculate suggested renewal MRC.

    product_mrc: base server MRC (unchanged in renewal)
    components: list of dicts with component_category, component_mrc, new_mrc
    term: 'm2m' | '12' | '24' | '36'

    SW/Support components re-priced at new_mrc (falls back to component_mrc if None).
    Hardware/Bandwidth/Network components held at component_mrc.
    m2m applies 1.25× multiplier.
    """
    total = float(product_mrc)
    for c in components:
        if c["component_category"] in _SW_SUPPORT_CATS:
            total += c["new_mrc"] if c["new_mrc"] is not None else c["component_mrc"]
        else:
            total += float(c["component_mrc"])
    multiplier = 1.25 if term == "m2m" else 1.0
    return round(total * multiplier, 2)
