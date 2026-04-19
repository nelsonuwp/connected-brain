from typing import Optional

from .patterns import REGISTERED_PATTERNS


def classify(ticket: dict) -> Optional[str]:
    """Return the slug of the first matching pattern, or None."""
    for pattern in REGISTERED_PATTERNS:
        if pattern.matches(ticket):
            return pattern.slug
    return None
