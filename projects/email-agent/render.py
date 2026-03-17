#!/usr/bin/env python3
"""
render.py

Reads outputs/emails_summary.json → formats markdown → injects into an Obsidian daily note.

Idempotent: replaces an existing '## Email Summary' section instead of appending.
"""

import argparse
import json
import os
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
    # connected-brain/vault (repo root is parents[2] from projects/email-agent/render.py)
    return Path(__file__).resolve().parents[2] / "vault"


def _resolve_daily_note_path(date_str: str) -> Path:
    vault = Path(os.getenv("VAULT_PATH", str(_default_vault_path())))
    return vault / "00-daily" / f"{date_str}.md"


# ── Rendering helpers ─────────────────────────────────────────────────────────

_SIGNAL_EMOJI = {
    "it_ticket": "ticket",
    "doc_share": "doc",
    "crm_lead": "lead",
    "hr_report": "HR",
    "jira_notification": "JIRA",
    "auto_reply": "auto-reply",
    "scheduled_report": "report",
    "partner_notification": "partner",
    "crm_notification": "CRM",
    "it_notification": "IT",
    "auto_forward": "fwd",
}


def _signal_detail(sig: Dict[str, Any]) -> str:
    ext = sig.get("extracted") or {}
    if isinstance(ext, dict):
        if ext.get("ticket_id"):
            desc = (ext.get("description") or "").strip()
            return f"{ext.get('ticket_id')} {desc}".strip()
        if ext.get("contact") and ext.get("company"):
            return f"{ext.get('contact')} @ {ext.get('company')}".strip()
        if ext.get("document"):
            return str(ext.get("document"))
        if ext.get("original_subject"):
            return str(ext.get("original_subject"))
        if ext.get("subject"):
            return str(ext.get("subject"))
    return (sig.get("subject") or "")[:100]


def _truncate_reply(text: str, limit: int = 150) -> str:
    t = (text or "").strip()
    if not t:
        return ""
    if len(t) <= limit:
        return t
    return t[:limit].rstrip() + "..."


def _render_thread_block(thread: Dict[str, Any]) -> List[str]:
    llm = thread.get("llm_summary") or {}
    lines: List[str] = []

    lines.append(f"#### {thread.get('subject', '').strip()}")
    one_line = (llm.get("one_line") or "").strip()
    if one_line:
        lines.append(f"**{one_line}**")

    for action in (llm.get("my_actions") or []):
        a = str(action).strip()
        if a:
            lines.append(f"- [ ] {a}")

    for taction in (llm.get("tracked_actions") or []):
        ta = str(taction).strip()
        if ta:
            lines.append(f"- {ta}")

    suggested = (llm.get("suggested_reply") or "").strip() if llm.get("suggested_reply") else ""
    if suggested:
        url = thread.get("thread_url") or ""
        preview = _truncate_reply(suggested, 150)
        if url:
            lines.append(f'> *"{preview}"* → [Open in Outlook]({url})')
        else:
            lines.append(f'> *"{preview}"*')

    lines.append(f'> `{thread.get("email_count", 0)} emails · {thread.get("last_sent", "")}`')
    return lines


def _render_new_info_callout(thread: Dict[str, Any]) -> List[str]:
    llm = thread.get("llm_summary") or {}
    subject = (thread.get("subject") or "").strip()
    one_line = (llm.get("one_line") or "").strip()
    summary = (llm.get("summary") or "").strip()

    lines: List[str] = []
    lines.append(f"> [!info]- {subject}")
    if one_line:
        lines.append(f"> **{one_line}**")

    if summary:
        # Ensure every line remains in the callout
        for ln in summary.splitlines():
            lines.append(f"> {ln}")

    for taction in (llm.get("tracked_actions") or []):
        ta = str(taction).strip()
        if ta:
            lines.append(f"> - {ta}")

    url = thread.get("thread_url") or ""
    if url:
        lines.append(f"> [Open in Outlook]({url})")

    return lines


def render_markdown(summary_json: Dict[str, Any]) -> Tuple[List[str], Dict[str, Any]]:
    output = summary_json.get("output") or {}
    threads = output.get("threads") or []
    signals = output.get("system_notifications") or []
    discard_count = int(output.get("discard_count") or 0)
    total_tokens = int((summary_json.get("tokens") or {}).get("total") or 0)

    waiting_on_me = [t for t in threads if (t.get("llm_summary") or {}).get("category") == "waiting_on_me"]
    waiting_on_others = [t for t in threads if (t.get("llm_summary") or {}).get("category") == "waiting_on_others"]
    new_information = [t for t in threads if (t.get("llm_summary") or {}).get("category") == "new_information"]

    lines: List[str] = []
    lines.append("## Email Summary")
    lines.append(f"> {len(threads)} threads · {len(signals)} signals · {discard_count} discarded · {total_tokens:,} tokens")

    if waiting_on_me:
        lines.append("")
        lines.append(f"### Waiting on Me ({len(waiting_on_me)})")
        lines.append("")
        for idx, t in enumerate(waiting_on_me):
            lines.extend(_render_thread_block(t))
            if idx < len(waiting_on_me) - 1:
                lines.append("")

    if waiting_on_others:
        lines.append("")
        lines.append(f"### Waiting on Others ({len(waiting_on_others)})")
        lines.append("")
        for idx, t in enumerate(waiting_on_others):
            lines.extend(_render_thread_block(t))
            if idx < len(waiting_on_others) - 1:
                lines.append("")

    if new_information:
        lines.append("")
        lines.append(f"### New Information ({len(new_information)})")
        lines.append("")
        for idx, t in enumerate(new_information):
            # No blank lines inside callout blocks; callout lines are contiguous.
            lines.extend(_render_new_info_callout(t))
            if idx < len(new_information) - 1:
                lines.append("")

    if signals:
        lines.append("")
        lines.append("### Signals")
        lines.append("| Type | Detail | Link |")
        lines.append("|------|--------|------|")
        for sig in signals:
            stype = (sig.get("signal_type") or "").strip()
            label = _SIGNAL_EMOJI.get(stype, stype or "signal")
            detail = _signal_detail(sig).replace("\n", " ").strip()
            url = sig.get("outlook_url") or ""
            link = f"[link]({url})" if url else ""
            lines.append(f"| {label} | {detail} | {link} |")

    meta = {
        "threads": threads,
        "signals": signals,
        "discard_count": discard_count,
        "total_tokens": total_tokens,
    }
    return lines, meta


# ── Injection ─────────────────────────────────────────────────────────────────

def inject_email_summary(note_path: Path, rendered_lines: List[str]) -> None:
    content = note_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    start_idx: Optional[int] = None
    for i, line in enumerate(lines):
        if line.strip() == "## Email Summary":
            start_idx = i
            break

    if start_idx is not None:
        end_idx: Optional[int] = None
        for i in range(start_idx + 1, len(lines)):
            if lines[i].startswith("## ") and lines[i].strip() != "## Email Summary":
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
        help="Path to daily note .md file, or 'auto' to derive from summary date range",
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

    rendered_lines, _ = render_markdown(summary_json)

    if target_file_arg == "auto":
        threads = (summary_json.get("output") or {}).get("threads") or []
        if not threads:
            print("  render failed: no threads in summary JSON (cannot derive date)")
            return 1
        date_str = (threads[0].get("last_sent") or "")[:10]
        if not date_str:
            print("  render failed: missing last_sent on first thread")
            return 1
        note_path = _resolve_daily_note_path(date_str)
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

