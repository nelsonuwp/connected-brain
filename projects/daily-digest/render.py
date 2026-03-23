#!/usr/bin/env python3
"""
render.py
---------
Reads daily_summary.json → formats markdown → injects into an Obsidian daily note.

Idempotent: replaces an existing '## Daily Digest' section instead of appending.

Output format uses Obsidian Tasks plugin syntax:
  - [ ] action text #action
  - tracked item #tracking

Clustered items (cross-source) show source badges: [email] [teams]

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

def _source_badge(sources: list) -> str:
    """Render source badges like [email][teams]."""
    if not sources or len(sources) <= 1:
        return ""
    return " " + "".join(f"`{s}`" for s in sorted(sources))


def _linked_subject(item: dict) -> str:
    """Subject as Outlook/Teams link if URL available."""
    subject = item.get("unified_subject") or "(no subject)"
    urls = item.get("urls", [])
    if urls and urls[0].get("url"):
        return f"[{subject}]({urls[0]['url']})"
    return subject


def _render_item_block(item: dict, include_actions: bool = True) -> List[str]:
    """Render a single triaged item as markdown lines."""
    lines = []
    sources = item.get("sources", [item.get("source", "unknown")])
    badge = _source_badge(sources)

    lines.append(f"#### {_linked_subject(item)}{badge}")

    summary = (item.get("summary") or "").strip()
    if summary:
        lines.append(summary)

    if include_actions:
        my_actions = [a.strip() for a in item.get("my_actions", []) if a.strip()]
        if my_actions:
            lines.append("")
            lines.append("##### My Actions")
            for action in my_actions:
                lines.append(f"- [ ] {action} #action")

    tracked = [a.strip() for a in item.get("tracked_actions", []) if a.strip()]
    if tracked:
        lines.append("")
        lines.append("##### Tracking")
        for ta in tracked:
            lines.append(f"- {ta} #tracking")

    suggested = (item.get("suggested_reply") or "").strip()
    if suggested:
        lines.append("")
        lines.append(f'> *"{suggested}"*')

    # Source links for clusters
    if item.get("is_cluster") and len(item.get("urls", [])) > 1:
        lines.append("")
        lines.append("Sources:")
        for u in item["urls"]:
            if u.get("url"):
                lines.append(f"- [{u.get('source', '?')}: {u.get('subject', 'link')}]({u['url']})")

    ts = item.get("last_timestamp", "")[:16].replace("T", " ")
    lines.append("")
    lines.append(f'`{ts}`')

    return lines


def render_markdown(summary: dict) -> List[str]:
    output = summary.get("output", {})
    waiting = output.get("waiting_on_me", [])
    tracking = output.get("tracking", [])
    info = output.get("new_information", [])
    discard_count = output.get("discard_count", 0)
    tokens = summary.get("tokens", {})
    total_tokens = tokens.get("total", 0)
    sources = summary.get("sources", [])

    total_items = len(waiting) + len(tracking) + len(info)

    lines = []
    lines.append(f"## Daily Digest")
    lines.append(f"> {total_items} items · {', '.join(sources)} · {discard_count} discarded · {total_tokens:,} tokens")

    if waiting:
        lines.append("")
        lines.append(f"### Waiting on Me ({len(waiting)})")
        for item in waiting:
            lines.append("")
            lines.extend(_render_item_block(item, include_actions=True))

    if tracking:
        lines.append("")
        lines.append(f"### Tracking ({len(tracking)})")
        for item in tracking:
            lines.append("")
            lines.extend(_render_item_block(item, include_actions=False))

    if info:
        lines.append("")
        lines.append(f"### New Information ({len(info)})")
        for item in info:
            lines.append("")
            lines.extend(_render_item_block(item, include_actions=False))

    return lines


# ── Injection ─────────────────────────────────────────────────────────────────

def inject_digest(note_path: Path, rendered_lines: List[str]) -> None:
    """
    Idempotent injection: replaces existing '## Daily Digest' section,
    or inserts before '## End of Day' if present, or appends.
    """
    content = note_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    start_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("## Daily Digest"):
            start_idx = i
            break

    if start_idx is not None:
        end_idx = None
        for i in range(start_idx + 1, len(lines)):
            if lines[i].startswith("## ") and not lines[i].strip().startswith("## Daily Digest"):
                end_idx = i
                break
        end_idx = end_idx if end_idx is not None else len(lines)
        new_lines = lines[:start_idx] + rendered_lines + lines[end_idx:]
    else:
        eod_idx = None
        for i, line in enumerate(lines):
            if line.strip() == "## End of Day":
                eod_idx = i
                break
        if eod_idx is not None:
            new_lines = lines[:eod_idx] + [""] + rendered_lines + [""] + lines[eod_idx:]
        else:
            new_lines = lines + [""] + rendered_lines

    note_path.write_text("\n".join(new_lines), encoding="utf-8")


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
        inject_digest(note_path, rendered)
        print(f"  [render] Wrote → {note_path}")
        return 0
    except Exception as e:
        print(f"  [render] Failed: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
