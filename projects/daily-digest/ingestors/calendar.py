#!/usr/bin/env python3
"""
ingestors/calendar.py
---------------------
Fetches calendar events from Microsoft Graph for the target note date.
Writes a SourceArtifact JSON — raw payload, never reshaped.

Output: outputs/source_calendar.json
"""

import os
import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests
import yaml

from ._ms_auth import get_access_token

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from connectors.source_artifact import make_source_artifact, record_count, write_artifact

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"
OUTPUT_PATH = OUTPUT_DIR / "source_calendar.json"
CALENDAR_FILTER_PATH = Path(__file__).resolve().parents[1] / "config" / "calendar_filter.yaml"


def _load_calendar_filter() -> set[str]:
    if not CALENDAR_FILTER_PATH.exists():
        return {"free", "tentative"}
    try:
        parsed = yaml.safe_load(CALENDAR_FILTER_PATH.read_text(encoding="utf-8")) or {}
        values = ((parsed.get("filter") or {}).get("exclude_show_as") or [])
        return {str(v).strip().lower() for v in values if str(v).strip()}
    except Exception:
        return {"free", "tentative"}


def _event_filter_reason(event: dict, excluded_show_as: set[str]) -> str | None:
    if event.get("isCancelled"):
        return "cancelled"
    if event.get("isAllDay"):
        return "all_day"
    response = ((event.get("responseStatus") or {}).get("response") or "").strip().lower()
    if response == "declined":
        return "declined"
    show_as = (event.get("showAs") or "").strip().lower()
    if show_as in excluded_show_as:
        return show_as
    return None


def fetch_events(note_date: date, token: str) -> Tuple[List[Dict[str, Any]], dict]:
    user_email = os.getenv("DIGEST_USER_EMAIL") or os.getenv("MS_EMAIL")
    if not user_email:
        raise RuntimeError("DIGEST_USER_EMAIL or MS_EMAIL must be set.")

    start_dt = f"{note_date.isoformat()}T00:00:00"
    end_dt = f"{note_date.isoformat()}T23:59:59"
    url = f"https://graph.microsoft.com/v1.0/users/{user_email}/calendarView"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": 'outlook.timezone="Eastern Standard Time"',
    }
    params = {
        "startDateTime": start_dt,
        "endDateTime": end_dt,
        "$select": (
            "id,subject,start,end,attendees,organizer,isAllDay,isCancelled,"
            "showAs,responseStatus,sensitivity,onlineMeetingUrl"
        ),
        "$top": 50,
        "$orderby": "start/dateTime",
    }

    all_events: List[Dict[str, Any]] = []
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    all_events.extend(data.get("value", []))

    while next_link := data.get("@odata.nextLink"):
        resp = requests.get(next_link, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        all_events.extend(data.get("value", []))

    excluded_show_as = _load_calendar_filter()
    kept: List[Dict[str, Any]] = []
    counts = {"cancelled": 0, "all_day": 0, "declined": 0}
    for event in all_events:
        reason = _event_filter_reason(event, excluded_show_as)
        if reason:
            counts[reason] = counts.get(reason, 0) + 1
            continue
        kept.append(event)

    counts["total_fetched"] = len(all_events)
    counts["total_kept"] = len(kept)
    return kept, counts


def main(note_date: date) -> int:
    print(f"  [calendar] Fetching events for {note_date}")

    artifact = make_source_artifact("calendar")
    artifact["note_date"] = note_date.isoformat()

    try:
        token = get_access_token()
        events, counts = fetch_events(note_date, token)

        excluded_total = counts.get("total_fetched", 0) - counts.get("total_kept", 0)
        print(
            "  [calendar] Fetched "
            f"{counts.get('total_fetched', 0)} events, "
            f"{counts.get('total_kept', 0)} kept after filtering "
            f"({excluded_total} excluded: "
            f"{counts.get('free', 0)} free, "
            f"{counts.get('tentative', 0)} tentative, "
            f"{counts.get('all_day', 0)} all-day, "
            f"{counts.get('declined', 0)} declined, "
            f"{counts.get('cancelled', 0)} cancelled)"
        )

        artifact["objects"] = {
            "events": {
                "status": "success",
                "record_count": record_count(events),
                "error": None,
                "data": events,
            }
        }
        artifact["status"] = "success"

    except Exception as e:
        artifact["status"] = "fail"
        artifact["error"] = {"type": type(e).__name__, "message": str(e), "retryable": False}
        print(f"  [calendar] Capture failed: {e}")

    finally:
        write_artifact(artifact, OUTPUT_PATH)
        print(f"  [calendar] Wrote -> {OUTPUT_PATH}")

    return 0 if artifact["status"] == "success" else 1
