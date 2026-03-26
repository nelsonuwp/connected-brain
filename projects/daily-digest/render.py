#!/usr/bin/env python3
"""
render.py
---------
Reads daily_summary.json → formats markdown → injects into an Obsidian daily note.

Idempotent: replaces an existing '## Yesterday in Review' section instead of appending.

Output format uses Obsidian Tasks plugin syntax:
  - [ ] action text #action
  - tracked item #tracking

Input:  outputs/daily_summary.json
Output: Obsidian daily note (vault/00-daily/{year}/{month}/{date}.md)
"""

import json
import os
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

DEFAULT_INPUT = Path(__file__).resolve().parent / "outputs" / "daily_summary.json"
CALENDAR_OUTPUT = Path(__file__).resolve().parent / "outputs" / "source_calendar.json"
CALENDAR_FILTER_PATH = Path(__file__).resolve().parent / "config" / "calendar_filter.yaml"


# ── Paths ─────────────────────────────────────────────────────────────────────

def _default_vault_path() -> Path:
    return Path(__file__).resolve().parents[2] / "vault"


def _resolve_daily_note_path(note_date: date) -> Path:
    vault = Path(os.getenv("VAULT_PATH", str(_default_vault_path())))
    month_folder = note_date.strftime("%m-%b")
    return vault / "00-daily" / str(note_date.year) / month_folder / f"{note_date.isoformat()}.md"


# ── Rendering ─────────────────────────────────────────────────────────────────

def _source_tag(sources: list) -> str:
    """Render source tags like: email, teams, email` `teams for multi-source."""
    return "` `".join(sorted(sources))


def _load_calendar_filter() -> dict:
    default = {"filter": {"company_wide_threshold": 15}}
    if not CALENDAR_FILTER_PATH.exists():
        return default
    try:
        parsed = yaml.safe_load(CALENDAR_FILTER_PATH.read_text(encoding="utf-8")) or {}
        if not isinstance(parsed, dict):
            return default
        return parsed
    except Exception:
        return default


def _slugify_meeting_name(subject: str) -> str:
    subject_lower = (subject or "meeting").lower()
    slug = re.sub(r"[^a-z0-9-]+", "-", subject_lower)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "meeting"


def _format_attendees(event: dict, user_email: str, company_wide_threshold: int) -> str:
    attendees = event.get("attendees") or []
    names: List[str] = []
    user_email_norm = (user_email or "").strip().lower()

    for attendee in attendees:
        email = (((attendee or {}).get("emailAddress") or {}).get("address") or "").strip().lower()
        if user_email_norm and email == user_email_norm:
            continue
        raw_name = (((attendee or {}).get("emailAddress") or {}).get("name") or "").strip()
        if not raw_name:
            continue
        first_name = raw_name.split()[0]
        if first_name:
            names.append(first_name)

    if not names:
        return "Solo"
    if len(names) > company_wide_threshold:
        return "Company-wide"
    return ", ".join(sorted(names))


def _render_schedule_rows(events: list, note_date: date, user_email: str) -> List[str]:
    cfg = _load_calendar_filter()
    threshold = int(((cfg.get("filter") or {}).get("company_wide_threshold")) or 15)
    month_folder = note_date.strftime("%m-%b")
    rows: List[str] = []

    for event in events:
        start_str = (((event.get("start") or {}).get("dateTime")) or "").strip()
        end_str = (((event.get("end") or {}).get("dateTime")) or "").strip()
        if not start_str or not end_str:
            continue
        try:
            start_dt = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
        except ValueError:
            continue

        time_label = f"{start_dt.strftime('%H:%M')}–{end_dt.strftime('%H:%M')}"
        short_name = _slugify_meeting_name(event.get("subject") or "")
        meeting_link = (
            f"[[90-meeting-notes/{note_date.year}/{month_folder}/"
            f"{note_date.isoformat()}-{short_name}\\|{short_name}]]"
        )
        attendees_text = _format_attendees(event, user_email, threshold)
        rows.append(f"| {time_label} | {meeting_link} | {attendees_text} | |")

    return rows


def render_markdown(summary: dict) -> List[str]:
    items = summary["output"]["items"]
    discard_count = summary["output"]["discard_count"]

    lines = ["## Yesterday in Review", ""]

    for item in items:
        primary_url = item["urls"][0]["url"] if item.get("urls") else ""
        source_tag = _source_tag(item["sources"])

        if primary_url:
            lines.append(f'#### [{item["title"]}]({primary_url}) `{source_tag}`')
        else:
            lines.append(f'#### {item["title"]} `{source_tag}`')

        lines.append(item["summary"])

        for action in item.get("actions", []):
            if action.get("completed") and action.get("completed_proof_url"):
                lines.append(f'- [x] {action["text"]} — [proof]({action["completed_proof_url"]}) #action')
            elif action.get("completed"):
                lines.append(f'- [x] {action["text"]} #action')
            else:
                lines.append(f'- [ ] {action["text"]} #action')

        for tracked in item.get("tracked_items", []):
            lines.append(f'- {tracked} #tracking')

        ind_sources = item.get("individual_sources", [])
        if len(ind_sources) > 1:
            source_links = " · ".join(f'[{s["label"]}]({s["url"]})' for s in ind_sources)
            lines.append(f"Sources: {source_links}")

        stats = item.get("source_stats", {})
        parts = []
        if stats.get("email_count"):
            parts.append(f'{stats["email_count"]} emails')
        if stats.get("teams_count"):
            parts.append(f'{stats["teams_count"]} teams')
        if stats.get("slack_count"):
            parts.append(f'{stats["slack_count"]} slack')
        date_range = stats.get("date_range", "")
        lines.append(f'`{" · ".join(parts)} · {date_range}`')
        lines.append("")

    total_items = len(items)
    email_total = sum(i.get("source_stats", {}).get("email_count", 0) for i in items)
    teams_total = sum(i.get("source_stats", {}).get("teams_count", 0) for i in items)
    lines.append(f"> {total_items} items · {email_total} emails · {teams_total} teams · {discard_count} discarded")

    return lines


# ── Injection ─────────────────────────────────────────────────────────────────

def inject_schedule(note_path: Path, schedule_rows: List[str]) -> str:
    content = note_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    schedule_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("## Today's Schedule"):
            schedule_idx = i
            break
    if schedule_idx is None:
        return "schedule: skipped -- no schedule section"

    header_idx = None
    for i in range(schedule_idx + 1, len(lines)):
        line = lines[i].strip()
        if line.startswith("## "):
            break
        if line.startswith("|") and "Time" in line and "Meeting" in line:
            header_idx = i
            break
    if header_idx is None or header_idx + 1 >= len(lines):
        return "schedule: skipped -- no schedule table"

    separator_idx = header_idx + 1
    end_idx = separator_idx + 1
    while end_idx < len(lines):
        s = lines[end_idx].strip()
        if not s:
            break
        if s.startswith("## "):
            break
        if not s.startswith("|"):
            break
        end_idx += 1

    new_lines = lines[: separator_idx + 1] + schedule_rows + lines[end_idx:]
    note_path.write_text("\n".join(new_lines), encoding="utf-8")
    return f"schedule: {len(schedule_rows)} events"


def inject_digest(note_path: Path, rendered_lines: List[str]) -> None:
    """
    Idempotent injection: replaces existing '## Yesterday in Review' section,
    or inserts before '## End of Day' if present, or appends.
    """
    content = note_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    start_idx = None
    for marker in ["## Yesterday in Review", "## Daily Digest"]:
        for i, line in enumerate(lines):
            if line.strip().startswith(marker):
                start_idx = i
                break
        if start_idx is not None:
            break

    if start_idx is not None:
        end_idx = None
        for i in range(start_idx + 1, len(lines)):
            if (
                lines[i].startswith("## ")
                and not lines[i].strip().startswith("## Yesterday in Review")
                and not lines[i].strip().startswith("## Daily Digest")
            ):
                end_idx = i
                break
        end_idx = end_idx if end_idx is not None else len(lines)
        new_lines = lines[:start_idx] + rendered_lines + lines[end_idx:]
        mode = "replaced"
    else:
        eod_idx = None
        for i, line in enumerate(lines):
            if line.strip() == "## End of Day":
                eod_idx = i
                break
        if eod_idx is not None:
            new_lines = lines[:eod_idx] + [""] + rendered_lines + [""] + lines[eod_idx:]
            mode = "inserted before End of Day"
        else:
            new_lines = lines + [""] + rendered_lines
            mode = "appended"

    note_path.write_text("\n".join(new_lines), encoding="utf-8")
    return mode


# ── Main ──────────────────────────────────────────────────────────────────────

def main(note_date: date = None, file_override: str = None) -> int:
    """
    Called by run_pipeline.py with note_date.
    Can also be called standalone with file_override for testing.
    """
    try:
        summary = json.loads(DEFAULT_INPUT.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  [render] Failed to read input: {e}")
        return 1

    output = summary.get("output", {})
    items = output.get("items", [])
    discard_count = output.get("discard_count", 0)
    action_count = sum(len(i.get("actions", [])) for i in items)
    tracking_count = sum(len(i.get("tracked_items", [])) for i in items)
    print(f"  [render] {len(items)} items to render, {discard_count} discarded")
    print(f"  [render] {action_count} actions, {tracking_count} tracked items")

    if file_override:
        note_path = Path(file_override)
    elif note_date:
        note_path = _resolve_daily_note_path(note_date)
    else:
        note_path = _resolve_daily_note_path(date.today())

    if not note_path.exists():
        print(f"  [render] Daily note not found: {note_path}")
        return 1

    # Schedule injection
    if CALENDAR_OUTPUT.exists():
        try:
            cal_artifact = json.loads(CALENDAR_OUTPUT.read_text(encoding="utf-8"))
            events_obj = (cal_artifact.get("objects") or {}).get("events", {})
            events = events_obj.get("data") or []
            user_email = os.getenv("DIGEST_USER_EMAIL") or os.getenv("MS_EMAIL", "")
            target_date = note_date or date.today()
            schedule_rows = _render_schedule_rows(events, target_date, user_email)
            schedule_mode = inject_schedule(note_path, schedule_rows)
            print(f"  [render] {schedule_mode}")
        except Exception as e:
            print(f"  [render] Schedule injection failed: {e}")
    else:
        print("  [render] No source_calendar.json found, skipping schedule")

    rendered = render_markdown(summary)

    try:
        mode = inject_digest(note_path, rendered)
        print(f"  [render] Wrote → {note_path} ({mode})")
        return 0
    except Exception as e:
        print(f"  [render] Failed: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
