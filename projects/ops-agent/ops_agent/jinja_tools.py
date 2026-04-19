"""Shared Jinja helpers for ops-agent templates."""

from __future__ import annotations

import math
from typing import Any, Optional

# Ring: grey #a0a0a8 -> lavender #b497ff
_GREY = (160, 160, 168)
_LAV = (180, 151, 255)


def _hex(rgb: tuple[int, int, int]) -> str:
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def familiarity_ring_filter(score: Optional[int]) -> dict[str, Any]:
    """Build SVG parameters for the familiarity ring (server-side only)."""
    r = 14.0
    circumference = 2 * math.pi * r
    cx, cy, sw, view = 18.0, 18.0, 4.0, 36
    base: dict[str, Any] = {
        "cx": cx,
        "cy": cy,
        "r": r,
        "sw": sw,
        "circumference": circumference,
        "view": view,
    }
    if score is None:
        return {
            **base,
            "track_color": "#d8d8e0",
            "arc_color": "#a0a0a8",
            "dash": f"0 {circumference}",
            "show_number": False,
        }
    pct = max(0.0, min(100.0, float(score)))
    arc_len = pct / 100.0 * circumference
    dash = f"{arc_len} {circumference}"

    if score < 50:
        return {
            **base,
            "track_color": "#e8e8ee",
            "arc_color": "#a0a0a8",
            "dash": dash,
            "show_number": False,
        }
    if score >= 90:
        return {
            **base,
            "track_color": "#e8e8ee",
            "arc_color": _hex(_LAV),
            "dash": dash,
            "show_number": True,
            "number": str(int(score)),
        }
    t = (score - 50) / 40.0
    rgb = (
        int(round(_lerp(_GREY[0], _LAV[0], t))),
        int(round(_lerp(_GREY[1], _LAV[1], t))),
        int(round(_lerp(_GREY[2], _LAV[2], t))),
    )
    return {
        **base,
        "track_color": "#e8e8ee",
        "arc_color": _hex(rgb),
        "dash": dash,
        "show_number": True,
        "number": str(int(score)),
    }
