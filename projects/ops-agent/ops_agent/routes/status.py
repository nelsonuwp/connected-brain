"""
Lightweight status endpoint — returns an HTML fragment polled by HTMX.
Checks: Postgres pool, Fusion SSH tunnel, JSM sync freshness.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from ..db import get_pool
from ..fusion_conn import fusion_env_ready, fusion_pool

logger = logging.getLogger(__name__)
router = APIRouter()

_STALE_WARN = timedelta(minutes=20)
_STALE_ERR  = timedelta(hours=1)


async def _postgres_ok() -> bool:
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return True
    except Exception:
        return False


async def _jira_sync_state() -> tuple[str, str]:
    """Returns (status_class, label) for the JSM indicator."""
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT status, updated_at FROM sync_state WHERE source = 'jira_tickets'"
            )
        if row is None:
            return "status-unknown", "JSM: no data"

        db_status: str = row["status"]
        updated_at: datetime = row["updated_at"]
        if updated_at.tzinfo is None:
            updated_at = updated_at.replace(tzinfo=timezone.utc)

        age = datetime.now(timezone.utc) - updated_at
        mins = int(age.total_seconds() / 60)
        label = f"JSM {mins}m ago" if mins < 60 else f"JSM {mins // 60}h ago"

        if db_status == "error":
            return "status-error", f"JSM error"
        if db_status == "running":
            return "status-ok", f"JSM syncing…"
        if age > _STALE_ERR:
            return "status-error", label
        if age > _STALE_WARN:
            return "status-warn", label
        return "status-ok", label
    except Exception:
        return "status-error", "JSM ?"


def _fusion_state() -> tuple[str, str]:
    if not fusion_env_ready():
        return "status-disabled", "Fusion off"
    if fusion_pool() is not None:
        return "status-ok", "Fusion"
    return "status-error", "Fusion down"


def _render(pg: bool, fusion_cls: str, fusion_lbl: str, jsm_cls: str, jsm_lbl: str) -> str:
    pg_cls = "status-ok" if pg else "status-error"
    return f"""
<div class="status-cluster" id="status-cluster"
     hx-get="/api/status" hx-trigger="every 30s" hx-swap="outerHTML">
  <span class="status-pill {pg_cls}"><span class="status-dot"></span>Postgres</span>
  <span class="status-pill {fusion_cls}"><span class="status-dot"></span>{fusion_lbl}</span>
  <span class="status-pill {jsm_cls}"><span class="status-dot"></span>{jsm_lbl}</span>
</div>
""".strip()


@router.get("/api/status", response_class=HTMLResponse)
async def status():
    pg = await _postgres_ok()
    fusion_cls, fusion_lbl = _fusion_state()
    jsm_cls, jsm_lbl = await _jira_sync_state()
    return HTMLResponse(_render(pg, fusion_cls, fusion_lbl, jsm_cls, jsm_lbl))
