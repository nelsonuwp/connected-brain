#!/usr/bin/env python3
"""
render.py

Reads outputs/emails_summary.json → formats markdown → injects into an Obsidian daily note.

Idempotent: replaces an existing '## Email Summary' section instead of appending.
"""

import argparse
import json
import os
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ── Env ───────────────────────────────────────────────────────────────────────

def _sq(v: str) -> str:
    v = v.strip()
    return v[1:-1] if len(v) >= 2 and v[0] == v[-1] in ('"', "'") else v


def load_env() -> None:
    root = Path(__file__).resolve().parents[1]
    for p in (Path.cwd() / ".env", root / ".env"):
        try:
            for raw in p.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                if k and (k not in os.environ or os.environ[k] == ""):
                    os.environ[k] = _sq(v)
        except OSError:
            pass


# ── Paths ─────────────────────────────────────────────────────────────────────

DEFAULT_INPUT = Path(__file__).resolve().parent / "outputs" / "emails_summary.json"


def _default_vault_path() -> Path:
    return Path(__file__).resolve().parents[2] / "vault"


def _resolve_daily_note_path(date_str: str) -> Path:
    vault = Path(os.getenv("VAULT_PATH", str(_default_vault_path())))
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    month_folder = d.strftime("%m-%b")  # e.g. "03-Mar"
    return vault / "00-daily" / str(d.year) / month_folder / f"{date_str}.md"


# ── Rendering helpers ─────────────────────────────────────────────────────────

def _linked_subject(thread: Dict[str, Any]) -> str:
    """Subject as an Outlook deep link."""
    subject = (thread.get("subject") or "").strip()
    url = thread.get("thread_url") or ""
    if url:
        return f"[{subject}]({url})"
    return subject


def _render_thread_block(thread: Dict[str, Any]) -> List[str]:
    llm = thread.get("llm_summary") or {}
    lines: List[str] = []

    # Subject as linked header
    lines.append(f"#### {_linked_subject(thread)}")

    # Full summary
    summary = (llm.get("summary") or "").strip()
    if summary:
        lines.append(summary)

    # My Actions — explicit sub-header with task checkboxes
    my_actions = [str(a).strip() for a in (llm.get("my_actions") or []) if str(a).strip()]
    if my_actions:
        lines.append("")
        lines.append("##### My Actions")
        for action in my_actions:
            lines.append(f"- [ ] {action} #action")

    # Tracked Actions — explicit sub-header
    tracked = [str(a).strip() for a in (llm.get("tracked_actions") or []) if str(a).strip()]
    if tracked:
        lines.append("")
        lines.append("##### Tracking")
        for ta in tracked:
            lines.append(f"- {ta} #tracking")

    # Suggested reply — full text, no truncation
    suggested = (llm.get("suggested_reply") or "").strip() if llm.get("suggested_reply") else ""
    if suggested:
        lines.append("")
        lines.append(f'> *"{suggested}"*')

    # Thread metadata
    lines.append("")
    lines.append(f'`{thread.get("email_count", 0)} emails · {thread.get("last_sent", "")}`')
    return lines


def _render_new_info_block(thread: Dict[str, Any]) -> List[str]:
    """New information threads — plain readable sections."""
    llm = thread.get("llm_summary") or {}
    lines: List[str] = []

    # Subject as linked header
    lines.append(f"#### {_linked_subject(thread)}")

    # Full summary
    summary = (llm.get("summary") or "").strip()
    if summary:
        lines.append(summary)

    # Tracked Actions if any
    tracked = [str(a).strip() for a in (llm.get("tracked_actions") or []) if str(a).strip()]
    if tracked:
        lines.append("")
        lines.append("##### Tracking")
        for ta in tracked:
            lines.append(f"- {ta} #tracking")

    # Thread metadata
    lines.append("")
    lines.append(f'`{thread.get("email_count", 0)} emails · {thread.get("last_sent", "")}`')
    return lines


def _derive_date_label(threads: List[Dict[str, Any]]) -> str:
    """Derive a date or date range string from thread last_sent fields."""
    dates = sorted(set(
        (t.get("last_sent") or "")[:10]
        for t in threads
        if (t.get("last_sent") or "")[:10]
    ))
    if not dates:
        return ""
    if len(dates) == 1:
        return dates[0]
    return f"{dates[0]} → {dates[-1]}"


def render_markdown(summary_json: Dict[str, Any]) -> List[str]:
    output = summary_json.get("output") or {}
    threads = output.get("threads") or []
    signals = output.get("system_notifications") or []
    discard_count = int(output.get("discard_count") or 0)
    total_tokens = int((summary_json.get("tokens") or {}).get("total") or 0)

    waiting_on_me = [t for t in threads if (t.get("llm_summary") or {}).get("category") == "waiting_on_me"]
    waiting_on_others = [t for t in threads if (t.get("llm_summary") or {}).get("category") == "waiting_on_others"]
    new_information = [t for t in threads if (t.get("llm_summary") or {}).get("category") == "new_information"]

    date_label = _derive_date_label(threads)

    lines: List[str] = []
    lines.append(f"## Email Summary — {date_label}")
    lines.append(f"> {len(threads)} threads · {len(signals)} signals · {discard_count} discarded · {total_tokens:,} tokens")

    if waiting_on_me:
        lines.append("")
        lines.append(f"### Waiting on Me ({len(waiting_on_me)})")
        for t in waiting_on_me:
            lines.append("")
            lines.extend(_render_thread_block(t))

    if waiting_on_others:
        lines.append("")
        lines.append(f"### Waiting on Others ({len(waiting_on_others)})")
        for t in waiting_on_others:
            lines.append("")
            lines.extend(_render_thread_block(t))

    if new_information:
        lines.append("")
        lines.append(f"### New Information ({len(new_information)})")
        for t in new_information:
            lines.append("")
            lines.extend(_render_new_info_block(t))

    return lines


# ── Injection ─────────────────────────────────────────────────────────────────

def inject_email_summary(note_path: Path, rendered_lines: List[str]) -> None:
    content = note_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    start_idx: Optional[int] = None
    for i, line in enumerate(lines):
        if line.strip().startswith("## Email Summary"):
            start_idx = i
            break

    if start_idx is not None:
        end_idx: Optional[int] = None
        for i in range(start_idx + 1, len(lines)):
            if lines[i].startswith("## ") and not lines[i].strip().startswith("## Email Summary"):
                end_idx = i
                break
        if end_idx is None:
            end_idx = len(lines)
        new_lines = lines[:start_idx] + rendered_lines + lines[end_idx:]
    else:
        eod_idx: Optional[int] = None
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

def main(file_override: str = None) -> int:
    load_env()

    p = argparse.ArgumentParser(description="Render emails_summary.json → Obsidian daily note.")
    p.add_argument(
        "--file",
        required=False,
        help="Path to daily note .md file, or 'auto' to use today's daily note",
    )
    p.add_argument("-i", "--input", default=str(DEFAULT_INPUT))

    if file_override:
        target_file_arg = file_override
        input_path = DEFAULT_INPUT
    else:
        args = p.parse_args()
        if not args.file:
            p.print_usage()
            return 1
        target_file_arg = args.file
        input_path = Path(args.input)

    try:
        summary_json = json.loads(Path(input_path).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  render failed reading input: {e}")
        return 1

    rendered_lines = render_markdown(summary_json)

    if target_file_arg == "auto":
        # Auto resolves to today's daily note
        note_path = _resolve_daily_note_path(date.today().isoformat())
    else:
        note_path = Path(target_file_arg)

    if not note_path.exists():
        print(f"  render failed: daily note not found: {note_path}")
        return 1

    try:
        inject_email_summary(note_path, rendered_lines)
        print(f"  Wrote → {note_path}")
        return 0
    except Exception as e:
        print(f"  render failed writing note: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())