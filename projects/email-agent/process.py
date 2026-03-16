#!/usr/bin/env python3
"""
2_process_emails.py

Reads source_emails.json (SourceArtifact), cleans HTML, and deterministically
categorizes every email into one of four buckets:

  important     — needs Adam's attention or a response
  useful        — worth reading, no action required
  not_important — informational; Adam is peripherally involved
  spam          — cold outreach, automated noise, marketing

Writes a SourceArtifact JSON.  The LLM step (script 3) only reads
important + useful — the rest is retained for audit trail only.

Output: outputs/emails_processed.json

Usage:
  python 2_process_emails.py
  python 2_process_emails.py -i outputs/source_emails.json -o outputs/emails_processed.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from connectors.source_artifact import (
    make_source_artifact, record_count, write_artifact
)

# ── Config ────────────────────────────────────────────────────────────────────

# Adam's internal domains — emails from these are never spam
INTERNAL_DOMAINS = {"aptum.com", "cloudops.com"}

# Domains that are definitionally noise regardless of content
NOISE_SENDER_RE = re.compile(
    r"(noreply|no-reply|donotreply|notifications?@|alerts?@|reports?@|"
    r"mailer@|bounce@|glassdoor\.com|atlassian\.net|microsoft-noreply)",
    re.I,
)
NOISE_SUBJECT_RE = re.compile(
    r"(newsletter|digest|bowl buzz|was executed at|daily sales|payout notification|"
    r"unsubscribe)",
    re.I,
)

# Body patterns that indicate cold outreach (not just automated noise)
COLD_OUTREACH_RE = re.compile(
    r"(opt.?out|reply.{0,10}stop|unsubscribe|pilot project|free hours?|intro call|"
    r"book a (call|demo|meeting)|reach out to see if)",
    re.I,
)

# Source system detection
_SOURCE_PATTERNS = [
    (re.compile(r"atlassian\.net|jira@",         re.I), "jira"),
    (re.compile(r"github\.com|noreply@github",   re.I), "github"),
    (re.compile(r"salesforce\.com",              re.I), "salesforce"),
    (re.compile(r"servicenow\.com",              re.I), "servicenow"),
    (re.compile(r"zendesk\.com",                 re.I), "zendesk"),
    (re.compile(r"slack\.com",                   re.I), "slack"),
    (re.compile(r"reports?@|noreply@|no-reply@|donotreply@|notifications?@|"
                r"alerts?@|mailer@|bounce@",     re.I), "automated"),
    (re.compile(r"@linkedin|@twitter|@facebook|glassdoor",  re.I), "social"),
]

# ── HTML → text ───────────────────────────────────────────────────────────────

_STRIP_BLOCKS = re.compile(r"<(style|script|head)[^>]*>.*?</\1>", re.I | re.S)
_BLOCK_TAGS   = re.compile(
    r"<(br\s*/?\s*|/?(p|div|tr|li|h[1-6]|blockquote|pre|table|hr)(\s[^>]*)?)[\s/]*>",
    re.I,
)
_STRIP_TAGS   = re.compile(r"<[^>]+>")
_MULTI_SPACE  = re.compile(r"[ \t]+")

def html_to_text(html: str) -> str:
    t = _STRIP_BLOCKS.sub("", html)
    t = _BLOCK_TAGS.sub("\n", t)
    t = _STRIP_TAGS.sub("", t)
    t = (t.replace("&nbsp;", " ").replace("&amp;", "&")
          .replace("&lt;", "<").replace("&gt;", ">")
          .replace("&quot;", '"').replace("&#39;", "'"))
    lines = [_MULTI_SPACE.sub(" ", ln).strip() for ln in t.splitlines()]
    out, prev_blank = [], False
    for ln in lines:
        blank = ln == ""
        if blank and prev_blank:
            continue
        out.append(ln)
        prev_blank = blank
    return "\n".join(out).strip()

# ── Thread splitting ──────────────────────────────────────────────────────────

_THREAD_BOUNDARY = re.compile(
    r"(?:^|\n)[ \t]*[-_]{3,}[ \t]*(?:\n|$)"
    r"|(?:^|\n)From:\s+\S.*?\nSent:\s+\S",
    re.I | re.S,
)

def split_thread(text: str):
    m = _THREAD_BOUNDARY.search(text)
    if m:
        latest  = text[:m.start()].strip()
        history = text[m.start():].strip()
        parts   = [latest, history] if latest else [history]
    else:
        parts   = [text]
    return [p for p in parts if p.strip()]

# ── Address helpers ───────────────────────────────────────────────────────────

def norm_addr(obj: Dict) -> Dict:
    ea = obj.get("emailAddress") or {}
    return {"name": ea.get("name", ""), "address": ea.get("address", "")}

def norm_addr_list(lst: List) -> List:
    return [norm_addr(x) for x in (lst or [])]

def sender_domain(raw: Dict) -> str:
    addr = (raw.get("from") or {}).get("emailAddress", {}).get("address", "")
    return addr.split("@")[-1].lower() if "@" in addr else ""

def is_internal(raw: Dict) -> bool:
    return sender_domain(raw) in INTERNAL_DOMAINS

def adam_is_to(raw: Dict, adam_domains: set) -> bool:
    to_addrs = [r.get("emailAddress", {}).get("address", "").lower()
                for r in (raw.get("toRecipients") or [])]
    return any(a.split("@")[-1] in adam_domains for a in to_addrs)

def adam_is_cc(raw: Dict, adam_domains: set) -> bool:
    cc_addrs = [r.get("emailAddress", {}).get("address", "").lower()
                for r in (raw.get("ccRecipients") or [])]
    return any(a.split("@")[-1] in adam_domains for a in cc_addrs)

# ── Source system ─────────────────────────────────────────────────────────────

def detect_source_system(raw: Dict) -> str:
    addr = (raw.get("from") or {}).get("emailAddress", {}).get("address", "")
    for pat, label in _SOURCE_PATTERNS:
        if pat.search(addr):
            return label
    return "human"

# ── Classification ────────────────────────────────────────────────────────────

CATEGORIES = ("important", "useful", "not_important", "spam")

def classify(raw: Dict, body_text: str) -> tuple[str, str]:
    """
    Returns (category, reason).

    Decision tree — first match wins:
    1. Meeting/event items → not_important (handled by capture filter already,
       but keep as defence-in-depth)
    2. Noise sender / noise subject → spam
    3. Automated system (jira, servicenow, etc.) → spam
    4. Social digest → spam
    5. Cold outreach patterns in body → spam
    6. Internal sender + Adam in TO + has thread history → important
    7. Internal sender + Adam in TO → useful (might need response, LLM decides)
    8. Internal sender + Adam in CC → useful
    9. External human sender + Adam in TO → not_important (no prior relationship)
    10. Everything else → not_important
    """
    subject    = raw.get("subject") or ""
    subj_lower = subject.lower()
    source_sys = detect_source_system(raw)
    internal   = is_internal(raw)
    in_to      = adam_is_to(raw, INTERNAL_DOMAINS)
    in_cc      = adam_is_cc(raw, INTERNAL_DOMAINS)
    is_reply   = subj_lower.lstrip().startswith("re:")
    is_fwd     = subj_lower.lstrip().startswith(("fw:", "fwd:"))
    odata_type = (raw.get("@odata.type") or "").lower()

    # 1. Meeting/event items
    if "eventmessage" in odata_type:
        return "not_important", "Meeting/calendar item"

    # 2. Noise sender or noise subject
    sender_addr = (raw.get("from") or {}).get("emailAddress", {}).get("address", "")
    if NOISE_SENDER_RE.search(sender_addr) or NOISE_SUBJECT_RE.search(subject):
        return "spam", "Automated notification or marketing digest"

    # 3. Automated system source
    if source_sys in ("jira", "github", "servicenow", "zendesk", "automated", "social"):
        return "spam", f"Automated message from {source_sys}"

    # 4. Cold outreach patterns
    if COLD_OUTREACH_RE.search(body_text) and not internal:
        return "spam", "Cold outreach / unsolicited sales email"

    # 5. Internal sender, Adam in TO, ongoing thread → important
    if internal and in_to and (is_reply or is_fwd):
        return "important", "Active internal thread requiring awareness or response"

    # 6. Internal sender, Adam in TO, new thread → useful (LLM will decide)
    if internal and in_to:
        return "useful", "Internal email addressed to Adam"

    # 7. Internal sender, Adam in CC → useful
    if internal and in_cc:
        return "useful", "Internal thread; Adam copied for visibility"

    # 8. External human, in TO → not_important (unknown relationship)
    if not internal and in_to and source_sys == "human":
        return "not_important", "External sender, no established internal relationship"

    return "not_important", "Peripheral or unclassified"

# ── Email cleaning ────────────────────────────────────────────────────────────

def clean_email(raw: Dict) -> Dict:
    subject    = raw.get("subject") or ""
    body_raw   = raw.get("body") or {}
    content    = body_raw.get("content") or ""
    ctype      = (body_raw.get("contentType") or "").lower()
    body_text  = html_to_text(content) if (ctype == "html" or content.lstrip().startswith("<")) else content.strip()
    parts      = split_thread(body_text)
    body       = parts[0] if parts else ""
    history    = parts[1] if len(parts) > 1 else None
    category, reason = classify(raw, body_text)

    return {
        "id":              raw.get("id"),
        "sent_at":         raw.get("sentDateTime"),
        "subject":         subject,
        "category":        category,
        "category_reason": reason,
        "source_system":   detect_source_system(raw),
        "is_reply":        subject.lstrip().lower().startswith("re:"),
        "is_forward":      subject.lstrip().lower().startswith(("fw:", "fwd:")),
        "from":            norm_addr(raw.get("from") or {}),
        "to":              norm_addr_list(raw.get("toRecipients") or []),
        "cc":              norm_addr_list(raw.get("ccRecipients") or []),
        "bcc":             norm_addr_list(raw.get("bccRecipients") or []),
        "body":            body,
        "body_word_count": len(body.split()) if body else 0,
        "has_thread":      history is not None,
        "thread_history":  history,
    }

# ── Main ──────────────────────────────────────────────────────────────────────

DEFAULT_INPUT  = Path(__file__).resolve().parent / "outputs" / "source_emails.json"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "outputs" / "emails_processed.json"

def main() -> int:
    p = argparse.ArgumentParser(description="Clean + categorize emails → SourceArtifact JSON.")
    p.add_argument("-i", "--input",  default=str(DEFAULT_INPUT))
    p.add_argument("-o", "--output", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    input_path  = Path(args.input)
    output_path = Path(args.output)

    artifact = make_source_artifact("email_processor")
    artifact["input_file"] = str(input_path)

    try:
        raw_artifact: Dict = json.loads(input_path.read_text(encoding="utf-8"))
        raw_messages: List = (raw_artifact.get("objects") or {}).get("messages", {}).get("data") or []
        print(f"  Processing {len(raw_messages)} raw messages from {input_path.name}")

        buckets: Dict[str, List] = {cat: [] for cat in CATEGORIES}
        for raw in raw_messages:
            cleaned = clean_email(raw)
            buckets[cleaned["category"]].append(cleaned)

        for cat, items in buckets.items():
            print(f"  {cat:15s} → {len(items)}")

        artifact["objects"] = {
            cat: {
                "status":       "success",
                "record_count": record_count(items),
                "error":        None,
                "data":         items,
            }
            for cat, items in buckets.items()
        }
        artifact["status"] = "success"

    except Exception as e:
        artifact["status"] = "fail"
        artifact["error"]  = {"type": type(e).__name__, "message": str(e), "retryable": False}
        print(f"  Processing failed: {e}")

    finally:
        write_artifact(artifact, output_path)
        print(f"  Wrote → {output_path}")

    return 0 if artifact["status"] == "success" else 1

if __name__ == "__main__":
    raise SystemExit(main())
