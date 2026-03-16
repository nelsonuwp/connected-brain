#!/usr/bin/env python3
"""
process_emails.py

Reads emails_capture.json, strips HTML/noise, enhances each record,
and writes two outputs:
  - emails_clean.json        : lean enriched records ready for LLM ingestion
  - emails_clean.digest.txt  : human-readable plain-text digest (--digest flag)

Enhancement fields added per email:
  source_system     : detected origin (jira, github, salesforce, automated, human, ...)
  is_reply          : subject starts with Re:
  is_forward        : subject starts with Fwd: / FW:
  body_word_count   : word count of cleaned body text
  has_thread_history: bool

Filtering:
  - Drops any meeting/calendar/event item (defense-in-depth after capture filter)
  - Drops noise emails unless --keep-noise

Usage:
  python process_emails.py
  python process_emails.py -i outputs/emails_capture.json -o outputs/emails_clean.json --digest
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# HTML → plain text (robust, no external deps)
# ---------------------------------------------------------------------------

# Pre-processing: nuke entire tag blocks that only add noise
_STRIP_BLOCKS = re.compile(
    r"<(style|script|head)[^>]*>.*?</\1>",
    re.IGNORECASE | re.DOTALL,
)
# Self-closing tags and remaining tags after block removal
_STRIP_TAGS = re.compile(r"<[^>]+>")
# Collapse whitespace
_MULTI_SPACE = re.compile(r"[ \t]+")
_MULTI_NEWLINE = re.compile(r"\n{3,}")

# Tags that should become newlines before stripping
_BLOCK_TAGS = re.compile(
    r"<(br\s*/?\s*|/?(p|div|tr|li|h[1-6]|blockquote|pre|table|hr)(\s[^>]*)?)\s*/?>",
    re.IGNORECASE,
)


def html_to_text(html: str) -> str:
    # 1. Remove <style>, <script>, <head> blocks entirely
    text = _STRIP_BLOCKS.sub("", html)
    # 2. Replace block-level tags with newlines
    text = _BLOCK_TAGS.sub("\n", text)
    # 3. Strip all remaining tags
    text = _STRIP_TAGS.sub("", text)
    # 4. Decode common HTML entities
    text = (text
            .replace("&nbsp;", " ")
            .replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&quot;", '"')
            .replace("&#39;", "'")
            .replace("&apos;", "'"))
    # 5. Clean up whitespace
    lines = [_MULTI_SPACE.sub(" ", ln).strip() for ln in text.splitlines()]
    # Dedupe consecutive blank lines
    cleaned: List[str] = []
    prev_blank = False
    for ln in lines:
        is_blank = ln == ""
        if is_blank and prev_blank:
            continue
        cleaned.append(ln)
        prev_blank = is_blank
    return "\n".join(cleaned).strip()


# ---------------------------------------------------------------------------
# Email body + thread extraction
# ---------------------------------------------------------------------------

def extract_body(body: Dict[str, Any]) -> str:
    content_type = (body.get("contentType") or "").lower()
    content = body.get("content") or ""
    if not content:
        return ""
    if content_type == "html" or content.lstrip().startswith("<"):
        return html_to_text(content)
    return content.strip()


# Matches the start of a quoted/forwarded section in plain text
_THREAD_BOUNDARY = re.compile(
    r"(?:^|\n)[ \t]*[-_]{3,}[ \t]*(?:\n|$)"          # --- divider ---
    r"|(?:^|\n)From:\s+\S.*?\nSent:\s+\S",             # Outlook quote header
    re.IGNORECASE | re.DOTALL,
)


def split_thread(text: str) -> List[str]:
    """Return [latest_message, thread_history] or just [full_text]."""
    match = _THREAD_BOUNDARY.search(text)
    if match:
        latest = text[:match.start()].strip()
        history = text[match.start():].strip()
        parts = [latest, history] if latest else [history]
    else:
        parts = [text]
    return [p for p in parts if p.strip()]


# ---------------------------------------------------------------------------
# Participant normalization
# ---------------------------------------------------------------------------

def norm_addr(obj: Dict) -> Dict[str, str]:
    ea = obj.get("emailAddress") or {}
    return {"name": ea.get("name", ""), "address": ea.get("address", "")}


def norm_addr_list(lst: List[Dict]) -> List[Dict[str, str]]:
    return [norm_addr(x) for x in (lst or [])]


# ---------------------------------------------------------------------------
# Message type detection (via @odata.type — Graph v1.0 doesn't expose itemClass)
# ---------------------------------------------------------------------------

# Graph sets @odata.type on eventMessage subclass for all meeting/calendar items.
# Regular emails have no @odata.type (or a non-event type).
_EVENT_MESSAGE_TYPE = "#microsoft.graph.eventMessage"

_NON_EMAIL_ODATA_TYPES = {
    "#microsoft.graph.eventMessage",
    "#microsoft.graph.calendarSharingMessage",
}

def is_meeting_or_event(raw: Dict) -> bool:
    """Return True for any meeting request, calendar item, or event message."""
    odata_type = (raw.get("@odata.type") or "").strip().lower()
    return any(t.lower() in odata_type for t in _NON_EMAIL_ODATA_TYPES)

def classify_item(raw: Dict) -> str:
    odata_type = (raw.get("@odata.type") or "").strip()
    if "#microsoft.graph.eventMessage" in odata_type:
        return "meeting_invite"
    return "email"


# ---------------------------------------------------------------------------
# Source system detection
# ---------------------------------------------------------------------------

_SOURCE_PATTERNS = [
    (re.compile(r"atlassian\.net|jira@", re.I),           "jira"),
    (re.compile(r"github\.com|noreply@github",   re.I),   "github"),
    (re.compile(r"salesforce\.com",              re.I),   "salesforce"),
    (re.compile(r"servicenow\.com",              re.I),   "servicenow"),
    (re.compile(r"zendesk\.com",                 re.I),   "zendesk"),
    (re.compile(r"slack\.com",                   re.I),   "slack"),
    (re.compile(r"reports?@|noreply@|no-reply@|donotreply@|automated@|"
                r"notifications?@|alerts?@|mailer@|bounce@",
                re.I),                                     "automated"),
    (re.compile(r"@linkedin\.com|@twitter\.com|@facebook\.com", re.I), "social"),
]

def detect_source_system(raw: Dict) -> str:
    sender = (raw.get("from") or {}).get("emailAddress", {}).get("address", "")
    for pattern, label in _SOURCE_PATTERNS:
        if pattern.search(sender):
            return label
    return "human"


# ---------------------------------------------------------------------------
# Noise filtering
# ---------------------------------------------------------------------------

_NOISE_SENDERS = re.compile(
    r"(noreply|no-reply|donotreply|notifications?@|alerts?@|"
    r"glassdoor\.com|atlassian\.net|reports@)",
    re.IGNORECASE,
)
_NOISE_SUBJECTS = re.compile(
    r"(unsubscribe|newsletter|digest|bowl buzz|"
    r"was executed at|daily sales|payout notification)",
    re.IGNORECASE,
)


def is_noise(raw: Dict) -> bool:
    sender = (raw.get("from") or {}).get("emailAddress", {}).get("address", "")
    subject = raw.get("subject") or ""
    return bool(_NOISE_SENDERS.search(sender) or _NOISE_SUBJECTS.search(subject))


# ---------------------------------------------------------------------------
# Main cleaning
# ---------------------------------------------------------------------------

def clean_email(raw: Dict, keep_noise: bool = False) -> Optional[Dict]:
    # Defense-in-depth: drop meeting/calendar items even if capture didn't
    if is_meeting_or_event(raw):
        return None

    noise = is_noise(raw)
    if noise and not keep_noise:
        return None

    subject = raw.get("subject") or ""
    subj_lower = subject.lstrip().lower()
    is_reply   = subj_lower.startswith("re:")
    is_forward = subj_lower.startswith("fwd:") or subj_lower.startswith("fw:")

    body_text   = extract_body(raw.get("body") or {})
    thread_parts = split_thread(body_text)
    body        = thread_parts[0] if thread_parts else ""
    thread_hist = thread_parts[1] if len(thread_parts) > 1 else None

    return {
        "id":               raw.get("id"),
        "sent_at":          raw.get("sentDateTime"),
        "subject":          subject,
        "message_type":     classify_item(raw),
        "source_system":    detect_source_system(raw),
        "is_reply":         is_reply,
        "is_forward":       is_forward,
        "is_noise":         noise,
        "from":             norm_addr(raw.get("from") or {}),
        "to":               norm_addr_list(raw.get("toRecipients") or []),
        "cc":               norm_addr_list(raw.get("ccRecipients") or []),
        "bcc":              norm_addr_list(raw.get("bccRecipients") or []),
        "body":             body,
        "body_word_count":  len(body.split()) if body else 0,
        "has_thread_history": thread_hist is not None,
        "thread_history":   thread_hist,
    }


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------

def process(input_path: Path, output_path: Path, keep_noise: bool, write_digest: bool) -> None:
    raw_emails: List[Dict] = json.loads(input_path.read_text(encoding="utf-8"))
    print(f"Loaded {len(raw_emails)} raw emails from {input_path}")

    cleaned, skipped_noise, skipped_meeting = [], 0, 0
    for raw in raw_emails:
        if is_meeting_or_event(raw):
            skipped_meeting += 1
            continue
        result = clean_email(raw, keep_noise=keep_noise)
        if result is None:
            skipped_noise += 1
        else:
            cleaned.append(result)

    print(f"  → kept {len(cleaned)}, "
          f"dropped {skipped_meeting} meeting/event(s), "
          f"dropped {skipped_noise} noise email(s)")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(cleaned, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  → wrote {output_path}")

    if write_digest:
        digest_path = output_path.with_suffix(".digest.txt")
        _write_digest(cleaned, digest_path)
        print(f"  → wrote digest: {digest_path}")


def _write_digest(emails: List[Dict], path: Path) -> None:
    lines = ["=== EMAIL DIGEST ===", f"Total emails: {len(emails)}", ""]
    for i, e in enumerate(emails, 1):
        from_str = f"{e['from']['name']} <{e['from']['address']}>"
        to_str   = ", ".join(f"{a['name']} <{a['address']}>" for a in e["to"])
        cc_str   = ", ".join(f"{a['name']} <{a['address']}>" for a in e["cc"])
        tags = []
        if e.get("is_reply"):    tags.append("REPLY")
        if e.get("is_forward"):  tags.append("FWD")
        if e.get("is_noise"):    tags.append("NOISE")
        tag_str = f" [{', '.join(tags)}]" if tags else ""
        lines += [
            f"--- EMAIL {i} | {e['source_system'].upper()}{tag_str} ---",
            f"Date:    {e['sent_at']}",
            f"Subject: {e['subject']}",
            f"From:    {from_str}",
            f"To:      {to_str}",
            f"Words:   {e.get('body_word_count', 0)}",
        ]
        if cc_str:
            lines.append(f"CC:      {cc_str}")
        lines += ["", e["body"] or "(no body extracted)"]
        if e.get("thread_history"):
            lines += ["", "[Prior thread history]", e["thread_history"]]
        lines += ["", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    default_input  = Path(__file__).resolve().parent / "outputs" / "emails_capture.json"
    default_output = Path(__file__).resolve().parent / "outputs" / "emails_clean.json"

    p = argparse.ArgumentParser(description="Clean raw Graph API emails for LLM ingestion.")
    p.add_argument("-i", "--input",      default=str(default_input))
    p.add_argument("-o", "--output",     default=str(default_output))
    p.add_argument("--keep-noise",       action="store_true")
    p.add_argument("--digest",           action="store_true")
    args = p.parse_args()

    process(Path(args.input), Path(args.output), args.keep_noise, args.digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())