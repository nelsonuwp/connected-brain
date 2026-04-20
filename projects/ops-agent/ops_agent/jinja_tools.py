"""Shared Jinja helpers for ops-agent templates."""

from __future__ import annotations

import math
from typing import Any, Optional


def sla_remaining_filter(threshold_s: Optional[int], elapsed_s: Optional[int]) -> Optional[str]:
    """Return human-readable time remaining for an SLA, or None if not applicable."""
    if threshold_s is None or elapsed_s is None:
        return None
    remaining = int(threshold_s) - int(elapsed_s)
    if remaining <= 0:
        return None
    hours = remaining // 3600
    minutes = (remaining % 3600) // 60
    if hours >= 48:
        return f"{hours // 24}d"
    if hours >= 1:
        return f"{hours}h {minutes:02d}m"
    return f"{minutes}m"

# Ring: grey #a0a0a8 -> lavender #b497ff
_GREY = (160, 160, 168)
_LAV = (180, 151, 255)

# Scores 50-64 stay grey (but show number); lavender fade kicks in at 65.
# This avoids the "muddy zone" where 50-65 were nearly indistinguishable.
_FADE_LO = 65
_FADE_HI = 90


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
            "show_arc": False,
            "show_number": False,
        }
    pct = max(0.0, min(100.0, float(score)))
    arc_len = pct / 100.0 * circumference
    dash = f"{arc_len} {circumference}"

    if score <= 0:
        # Omit arc entirely to avoid the round-linecap dot artifact at zero.
        return {
            **base,
            "track_color": "#e8e8ee",
            "arc_color": "#a0a0a8",
            "dash": dash,
            "show_arc": False,
            "show_number": False,
        }

    if score < 50:
        return {
            **base,
            "track_color": "#e8e8ee",
            "arc_color": "#a0a0a8",
            "dash": dash,
            "show_arc": True,
            "show_number": False,
        }

    if score >= _FADE_HI:
        return {
            **base,
            "track_color": "#e8e8ee",
            "arc_color": _hex(_LAV),
            "dash": dash,
            "show_arc": True,
            "show_number": True,
            "number": str(int(score)),
        }

    if score < _FADE_LO:
        # 50-64: grey arc, number shown so the score is readable, no colour hint yet.
        return {
            **base,
            "track_color": "#e8e8ee",
            "arc_color": _hex(_GREY),
            "dash": dash,
            "show_arc": True,
            "show_number": True,
            "number": str(int(score)),
        }

    # 65-89: linear grey → lavender fade over a 25-point window.
    t = (score - _FADE_LO) / float(_FADE_HI - _FADE_LO)
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
        "show_arc": True,
        "show_number": True,
        "number": str(int(score)),
    }
