"""
Familiarity tooltip: merged semantic neighbors + time-to-close + worklog stats.
"""

from __future__ import annotations

import logging
from statistics import median
from typing import Any, Optional

import asyncpg

from ..db import get_ticket, get_ticket_assets
from .semantic import (
    embed_current_ticket,
    similar_customer_tickets,
    similar_neighbor_tickets,
)

logger = logging.getLogger(__name__)

TOP_MERGE = 10
TOP_SHOW = 3
FETCH_EACH = 10


def _format_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{max(1, int(round(seconds)))}s"
    if seconds < 3600:
        m = int(seconds // 60)
        return f"{m}m"
    if seconds < 86400:
        h = int(seconds // 3600)
        rem_m = int((seconds % 3600) // 60)
        if rem_m and h < 12:
            return f"{h}h {rem_m}m"
        return f"{h}h"
    d = int(seconds // 86400)
    h = int((seconds % 86400) // 3600)
    if h:
        return f"{d}d {h}h"
    return f"{d}d"


def _median(vals: list[float]) -> float:
    if not vals:
        return 0.0
    return float(median(vals))


def _range_bar(seconds: list[float]) -> Optional[dict[str, Any]]:
    if not seconds:
        return None
    lo = min(seconds)
    hi = max(seconds)
    med = _median(seconds)
    if hi <= lo:
        return {
            "flat": True,
            "min_label": _format_duration(lo),
            "median_label": _format_duration(med),
            "max_label": _format_duration(hi),
            "median_pct": 50.0,
        }
    med_pct = (med - lo) / (hi - lo) * 100.0
    med_pct = max(0.0, min(100.0, med_pct))
    return {
        "flat": False,
        "min_label": _format_duration(lo),
        "median_label": _format_duration(med),
        "max_label": _format_duration(hi),
        "median_pct": med_pct,
    }


async def build_familiarity_tooltip_context(
    pool: asyncpg.Pool,
    issue_key: str,
) -> dict[str, Any]:
    async with pool.acquire() as conn:
        ticket = await get_ticket(conn, issue_key)
        if not ticket:
            return {"error": "not_found", "issue_key": issue_key}

        assets = await get_ticket_assets(conn, issue_key)
        service_ids = [
            str(a["service_id"])
            for a in assets
            if a.get("service_id") is not None and str(a["service_id"]).strip() != ""
        ]

        qvec = embed_current_ticket(ticket.get("summary") or "", ticket.get("description") or "")

        cust: list[dict[str, Any]] = []
        oid = ticket.get("ocean_client_id")
        if oid is not None:
            cust = await similar_customer_tickets(
                conn, qvec, int(oid), exclude_issue_key=issue_key, limit=FETCH_EACH
            )

        nbr: list[dict[str, Any]] = []
        if service_ids:
            nbr = await similar_neighbor_tickets(
                conn, qvec, service_ids, exclude_issue_key=issue_key, limit=FETCH_EACH
            )

    merged: dict[str, dict[str, Any]] = {}
    for row in cust + nbr:
        key = row["issue_key"]
        sim = row.get("similarity_score")
        if sim is None:
            continue
        prev = merged.get(key)
        if prev is None or float(prev["similarity_score"]) < float(sim):
            merged[key] = dict(row)

    ranked = sorted(
        merged.values(),
        key=lambda r: float(r["similarity_score"]),
        reverse=True,
    )[:TOP_MERGE]

    if not ranked:
        return {
            "error": None,
            "issue_key": issue_key,
            "top3": [],
            "close_bar": None,
            "worklog_bar": None,
            "empty": True,
        }

    keys = [r["issue_key"] for r in ranked]
    async with pool.acquire() as conn:
        trows = await conn.fetch(
            """
            SELECT issue_key, created_at, resolved_at
            FROM tickets
            WHERE issue_key = ANY($1::text[])
            """,
            keys,
        )
        tmap = {r["issue_key"]: dict(r) for r in trows}

        wrows = await conn.fetch(
            """
            SELECT issue_key, COALESCE(SUM(time_spent_seconds), 0)::bigint AS work_seconds
            FROM ticket_worklogs
            WHERE issue_key = ANY($1::text[])
              AND deleted_at IS NULL
            GROUP BY issue_key
            """,
            keys,
        )
        wmap = {r["issue_key"]: int(r["work_seconds"]) for r in wrows}

    close_seconds: list[float] = []
    work_seconds: list[float] = []

    for r in ranked:
        tr = tmap.get(r["issue_key"])
        if not tr:
            continue
        created = tr.get("created_at")
        resolved = tr.get("resolved_at")
        if created is not None and resolved is not None:
            close_seconds.append(max(0.0, (resolved - created).total_seconds()))

        ws = float(wmap.get(r["issue_key"], 0))
        if ws > 0:
            work_seconds.append(ws)

    top3_out: list[dict[str, Any]] = []
    for r in ranked[:TOP_SHOW]:
        sim = float(r["similarity_score"])
        top3_out.append(
            {
                "issue_key": r["issue_key"],
                "summary": r.get("summary") or "",
                "similarity_pct": int(round(sim * 100)),
            }
        )

    return {
        "error": None,
        "issue_key": issue_key,
        "empty": False,
        "top3": top3_out,
        "close_bar": _range_bar(close_seconds),
        "worklog_bar": _range_bar(work_seconds),
    }
