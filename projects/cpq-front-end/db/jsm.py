"""
JSM worklog hours from the jsm_sync PostgreSQL mirror.

jsm_sync DB is a near-real-time copy of the APTUM Jira Service Management project.
The assets table links Jira Asset objects to service_ids; ticket_assets joins
tickets to assets, so we can sum worklogs per service in one query.

Hours are divided by the number of assets on each ticket so that a ticket with
20h logged against 12 assets contributes 1.67h per asset (not 20h × 12).
Customer-level totals are the sum of per-service hours, which gives the correct
proportional attribution when tickets span services from multiple customers.

Connection: direct to 10.121.20.84:5432 (internal network, no tunnel needed).
"""

import logging
import os
from datetime import date

import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

_DSN = os.environ.get(
    "JSM_SYNC_DATABASE_URL",
    "postgresql://jsm_sync:00001111@10.121.20.84:5432/jsm_sync",
)

_conn = None

# Shared SQL fragment: divides each worklog's seconds by the number of assets
# on that ticket so multi-asset tickets don't inflate per-service hours.
_HOURS_CTE = """
WITH asset_counts AS (
    SELECT issue_key, COUNT(DISTINCT object_id) AS n
    FROM ticket_assets
    GROUP BY issue_key
)
"""

_HOURS_SELECT = """
    ROUND(SUM(w.time_spent_seconds::numeric / ac.n) / 3600.0, 4) AS hours
FROM ticket_worklogs w
JOIN ticket_assets ta  ON ta.issue_key = w.issue_key
JOIN assets a          ON a.object_id  = ta.object_id
JOIN asset_counts ac   ON ac.issue_key = w.issue_key
WHERE w.started_at >= %s
  AND w.started_at  < %s
  AND w.deleted_at IS NULL
  AND a.service_id = ANY(%s)
"""


def _configured() -> bool:
    return bool(_DSN)


def _get_conn():
    global _conn
    if _conn:
        try:
            with _conn.cursor() as c:
                c.execute("SELECT 1")
            return _conn
        except Exception:
            _conn = None
    _conn = psycopg2.connect(_DSN, cursor_factory=RealDictCursor)
    _conn.set_session(readonly=True, autocommit=True)
    return _conn


def _billing_period() -> tuple[str, str]:
    """Return (start_date, end_date) for the last complete calendar month."""
    today = date.today()
    year, month = (today.year - 1, 12) if today.month == 1 else (today.year, today.month - 1)
    next_y, next_m = (year + 1, 1) if month == 12 else (year, month + 1)
    return f"{year:04d}-{month:02d}-01", f"{next_y:04d}-{next_m:02d}-01"


def get_support_hours_batch(service_ids: list[int]) -> dict[int, dict] | None:
    """
    Return hours for the last 3 complete calendar months per service_id in one query.

    Returns dict[service_id → {"current": float, "prev": float, "prev2": float,
                                "periods": ["YYYY-MM", "YYYY-MM", "YYYY-MM"]}] on success.
    The "periods" list is oldest→newest and is identical for every entry (global metadata).
    Services absent from the dict had 0 hours in all three months.
    Returns None when JSM is unconfigured or the query fails.
    """
    if not _configured() or not service_ids:
        return None
    try:
        conn = _get_conn()
        curr_start, curr_end = _billing_period()
        y, m = int(curr_start[:4]), int(curr_start[5:7])
        pm,  py  = (m  - 1, y)  if m  > 1 else (12, y  - 1)
        pm2, py2 = (pm - 1, py) if pm > 1 else (12, py - 1)
        prev_start  = f"{py:04d}-{pm:02d}-01"
        prev2_start = f"{py2:04d}-{pm2:02d}-01"
        periods = [f"{py2:04d}-{pm2:02d}", f"{py:04d}-{pm:02d}", curr_start[:7]]

        str_ids = [str(sid) for sid in service_ids]
        with conn.cursor() as cur:
            cur.execute(
                _HOURS_CTE +
                """
                SELECT
                    a.service_id,
                    TO_CHAR(DATE_TRUNC('month', w.started_at), 'YYYY-MM') AS period,
                    """ + _HOURS_SELECT.replace("SELECT", "").strip() +
                " GROUP BY a.service_id, DATE_TRUNC('month', w.started_at)",
                (prev2_start, curr_end, str_ids),
            )
            rows = cur.fetchall()

        result: dict[int, dict] = {}
        for r in rows:
            sid = int(r["service_id"])
            if sid not in result:
                result[sid] = {"current": 0.0, "prev": 0.0, "prev2": 0.0, "periods": periods}
            p = r["period"]
            if p == periods[2]:
                result[sid]["current"] = float(r["hours"])
            elif p == periods[1]:
                result[sid]["prev"]    = float(r["hours"])
            else:
                result[sid]["prev2"]   = float(r["hours"])
        return result
    except Exception:
        logger.exception("get_support_hours_batch: error")
        return None


def get_support_hours_by_month(service_ids: list[int], months: int = 3) -> list[dict]:
    """
    Return per-asset-adjusted hours per month for the last N complete months.

    Returns list sorted oldest → newest:
        [{"period": "YYYY-MM", "hours": float}, ...]
    Months with no logged hours are included with hours=0.
    Returns [] if JSM is unavailable.
    """
    if not _configured() or not service_ids:
        return []
    today = date.today()
    periods = []
    for i in range(months, 0, -1):
        m = today.month - i
        y = today.year
        while m <= 0:
            m += 12
            y -= 1
        nm, ny = (m + 1, y) if m < 12 else (1, y + 1)
        periods.append({
            "period": f"{y:04d}-{m:02d}",
            "start":  f"{y:04d}-{m:02d}-01",
            "end":    f"{ny:04d}-{nm:02d}-01",
        })
    try:
        conn = _get_conn()
        str_ids = [str(sid) for sid in service_ids]
        with conn.cursor() as cur:
            cur.execute(
                _HOURS_CTE +
                "SELECT TO_CHAR(DATE_TRUNC('month', w.started_at), 'YYYY-MM') AS period," +
                _HOURS_SELECT + " GROUP BY 1 ORDER BY 1",
                (periods[0]["start"], periods[-1]["end"], str_ids),
            )
            rows = {r["period"]: float(r["hours"]) for r in cur.fetchall()}
        return [{"period": p["period"], "hours": rows.get(p["period"], 0.0)} for p in periods]
    except Exception:
        logger.exception("get_support_hours_by_month: error")
        return []
