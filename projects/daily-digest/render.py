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
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_INPUT = Path(__file__).resolve().parent / "outputs" / "daily_summary.json"


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

    rendered = render_markdown(summary)

    if file_override:
        note_path = Path(file_override)
    elif note_date:
        note_path = _resolve_daily_note_path(note_date)
    else:
        note_path = _resolve_daily_note_path(date.today())

    if not note_path.exists():
        print(f"  [render] Daily note not found: {note_path}")
        return 1

    try:
        mode = inject_digest(note_path, rendered)
        print(f"  [render] Wrote → {note_path} ({mode})")
        return 0
    except Exception as e:
        print(f"  [render] Failed: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
