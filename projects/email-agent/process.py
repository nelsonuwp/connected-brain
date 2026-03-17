#!/usr/bin/env python3
"""
process.py

Reads source_emails.json → groups into threads, extracts system notification
signals, and builds a compact SourceArtifact ready for the LLM step.

Output objects:
  threads              — human conversations clustered by normalized subject
  system_notifications — tool/automated signals with deterministically extracted data
  discard              — audit list only (subject + sender + date, no bodies)

Output: outputs/emails_processed.json
"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.parse
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from connectors.source_artifact import make_source_artifact, record_count, write_artifact

# ── Env ───────────────────────────────────────────────────────────────────────

def _sq(v: str) -> str:
    v = v.strip()
    return v[1:-1] if len(v) >= 2 and v[0] == v[-1] in ('"', "'") else v

def load_env() -> None:
    # .parent  → .../connected-brain/projects/email-agent  (directory)
    # parents[1] → .../connected-brain                     (repo root)
    script_dir = Path(__file__).resolve().parent
    repo_root  = script_dir.parents[1]
    for p in (Path.cwd() / ".env", repo_root / ".env"):
        try:
            for raw in p.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                if k and k not in os.environ:
                    os.environ[k] = _sq(v)
        except OSError:
            pass

# ── HTML → plain text ─────────────────────────────────────────────────────────

_STRIP_BLOCKS = re.compile(r"<(style|script|head)[^>]*>.*?</\1>", re.I | re.S)
_BLOCK_TAGS   = re.compile(
    r"<(br\s*/?\s*|/?(p|div|tr|li|h[1-6]|blockquote|pre|table|hr)(\s[^>]*)?)[\s/]*>", re.I)
_STRIP_TAGS   = re.compile(r"<[^>]+>")
_MULTI_SPACE  = re.compile(r"[ \t]+")

def html_to_text(html: str) -> str:
    t = _STRIP_BLOCKS.sub("", html)
    t = _BLOCK_TAGS.sub("\n", t)
    t = _STRIP_TAGS.sub("", t)
    t = (t.replace("&nbsp;", " ").replace("&amp;", "&")
          .replace("&lt;",   "<").replace("&gt;",  ">")
          .replace("&quot;", '"').replace("&#39;",  "'"))
    lines, out, prev = [_MULTI_SPACE.sub(" ", ln).strip() for ln in t.splitlines()], [], False
    for ln in lines:
        b = ln == ""
        if b and prev:
            continue
        out.append(ln)
        prev = b
    return "\n".join(out).strip()

def extract_body(raw: Dict) -> str:
    body    = raw.get("body") or {}
    content = body.get("content") or ""
    ctype   = (body.get("contentType") or "").lower()
    if not content:
        return ""
    return html_to_text(content) if (ctype == "html" or content.lstrip().startswith("<")) else content.strip()

# ── Subject normalization ─────────────────────────────────────────────────────

_PREFIX_RE = re.compile(r'^(re|fw|fwd)\s*:\s*', re.I)
_TAG_RE    = re.compile(r'^\[.*?\]\s*')

def normalize_subject(subject: str) -> str:
    """Strip Re:/Fw:/[TAGS] prefixes for clustering. Multi-level aware."""
    s = subject.strip()
    while True:
        s2 = _PREFIX_RE.sub("", _TAG_RE.sub("", s)).strip()
        if s2 == s:
            break
        s = s2
    return s.lower()

def thread_key(subject: str) -> str:
    return hashlib.md5(normalize_subject(subject).encode()).hexdigest()[:8]

# ── Address helpers ───────────────────────────────────────────────────────────

# ── Outlook deep-link builder ─────────────────────────────────────────────────

def outlook_url(msg_id: str, web_link: str = None) -> Optional[str]:
    """
    Return the Outlook web deep link for a message.

    Prefers webLink from the Graph API response — this is a pre-built OWA URL
    using the correct EWS ID format (AAQk...) that opens the exact message.

    Falls back to constructing a URL from the REST ID (AAMk...) only if webLink
    is absent, but note: this fallback opens the mailbox root, not the message,
    because OWA and Graph use different ID encoding schemes.
    """
    if web_link:
        return web_link
    if not msg_id:
        return None
    base    = os.getenv("OUTLOOK_BASE_URL", "https://outlook.office.com").rstrip("/")
    encoded = urllib.parse.quote(msg_id, safe="")
    return f"{base}/mail/inbox/id/{encoded}"


def norm_addr(obj: Dict) -> Dict:
    ea = obj.get("emailAddress") or {}
    return {"name": ea.get("name", ""), "address": ea.get("address", "")}

def norm_addr_list(lst: List) -> List:
    return [norm_addr(x) for x in (lst or [])]

def sender_addr_str(raw: Dict) -> str:
    return (raw.get("from") or {}).get("emailAddress", {}).get("address", "").lower()

def sender_domain_str(raw: Dict) -> str:
    addr = sender_addr_str(raw)
    return addr.split("@")[-1] if "@" in addr else ""

# ── Discard detection ─────────────────────────────────────────────────────────

INTERNAL_DOMAINS = {"aptum.com", "cloudops.com"}

_DISCARD_SENDERS = re.compile(
    r"(noreply|no-reply|donotreply|mailer@|bounce@|glassdoor\.com|microsoft-noreply|"
    r"adpdonotreply|@connect\.media|@contex\.ca|@groupecontex|communications@now\.|"
    r"support@wheniwork|mscnm@microsoft\.com|@salesforce\.com|@marketo|@hubspot\.com|"
    r"@mailchimp|@constantcontact|evenements)", re.I)
_DISCARD_SUBJECTS = re.compile(
    r"(newsletter|digest|bowl buzz|unsubscribe|daily sales|payout notification|"
    r"breaking news:|statement of account|it.s account check in|last chance!|"
    r"webinar|free .*(session|training)|you.re invited to)", re.I)
_COLD_OUTREACH = re.compile(
    r"(opt.?out|reply.{0,10}stop|pilot project|free hours?|intro call|"
    r"book a (call|demo|meeting)|reach out to see if)", re.I)
# Outlook external-sender warning — reliable signal for external marketing
_OUTLOOK_EXTERNAL_WARNING = re.compile(
    r"you don.t often get email from", re.I)

def is_discard(raw: Dict, body: str) -> bool:
    addr     = sender_addr_str(raw)
    subj     = raw.get("subject") or ""
    domain   = sender_domain_str(raw)
    internal = domain in INTERNAL_DOMAINS
    if _DISCARD_SENDERS.search(addr):    return True
    if _DISCARD_SUBJECTS.search(subj):   return True
    if not internal and _COLD_OUTREACH.search(body): return True
    # Any external sender that triggers Outlook's "you don't often get email from"
    # banner is definitionally low-trust / marketing / cold contact
    if not internal and _OUTLOOK_EXTERNAL_WARNING.search(body[:500]): return True
    return False

# ── System notification detection ─────────────────────────────────────────────

_SIG_SUBJECT: List[Tuple[re.Pattern, str]] = [
    (re.compile(r'^automatic reply:',                                  re.I), "auto_reply"),
    (re.compile(r'\b(ITSUPPORT|INC|CHG|PRB|REQ|TASK|SD)-\d+\b',      re.I), "it_ticket"),
    (re.compile(r'created a lead for',                                 re.I), "crm_lead"),
    (re.compile(r'shared\s+"[^"]+"',                                   re.I), "doc_share"),
    (re.compile(r'time off requested report',                          re.I), "hr_report"),
    (re.compile(r'was executed at',                                    re.I), "scheduled_report"),
    (re.compile(r'distributor transfer|dsa.?cta sponsorship',         re.I), "partner_notification"),
]
_SIG_SENDER: List[Tuple[re.Pattern, str]] = [
    (re.compile(r'hubspot|@hs-',          re.I), "crm_notification"),
    (re.compile(r'servicenow',            re.I), "it_notification"),
    (re.compile(r'atlassian\.net|jira@',  re.I), "jira_notification"),
    (re.compile(r'reports?@',             re.I), "scheduled_report"),
]

def _extract_signal_data(sig_type: str, subject: str) -> Dict:
    if sig_type == "it_ticket":
        m = re.search(r'((ITSUPPORT|INC|CHG|PRB|REQ|TASK|SD)-\d+)\s*(.*)', subject, re.I)
        return {"ticket_id": m.group(1) if m else "", "description": (m.group(3) or "").strip()[:100]}
    if sig_type == "crm_lead":
        m = re.search(r'([\w][\w\s]+?)\s+created a lead for\s+([\w\s]+?)\s+at\s+(.+)', subject, re.I)
        return {
            "created_by": m.group(1).strip() if m else "",
            "contact":    m.group(2).strip() if m else "",
            "company":    m.group(3).strip()[:80] if m else "",
        }
    if sig_type == "doc_share":
        m = re.search(r'"([^"]+)"', subject)
        return {"document": m.group(1)[:100] if m else subject[:80]}
    if sig_type == "auto_reply":
        return {"original_subject": re.sub(r'^automatic reply:\s*', '', subject, flags=re.I)[:100]}
    return {"subject": subject[:100]}

def detect_signal(raw: Dict) -> Optional[Tuple[str, Dict]]:
    """Returns (signal_type, extracted_data) or None."""
    addr  = sender_addr_str(raw)
    subj  = raw.get("subject") or ""
    adam  = os.getenv("USER_EMAIL", "").lower()

    if adam and addr == adam:
        return "auto_forward", {"subject": subj[:100]}

    for pat, sig_type in _SIG_SUBJECT:
        if pat.search(subj):
            return sig_type, _extract_signal_data(sig_type, subj)

    for pat, sig_type in _SIG_SENDER:
        if pat.search(addr):
            return sig_type, {"subject": subj[:100]}

    return None

# ── Thread building ───────────────────────────────────────────────────────────

def build_threads(candidates: List[Dict]) -> List[Dict]:
    """Cluster email dicts by normalized subject, sort chronologically within each thread."""
    adam   = os.getenv("USER_EMAIL", "").lower()
    groups: Dict[str, List[Dict]] = defaultdict(list)

    for e in candidates:
        groups[thread_key(e.get("subject") or "")].append(e)

    threads = []
    for tid, emails in groups.items():
        emails.sort(key=lambda x: x.get("sent_at") or "")

        # Unique participants (excluding Adam) — from senders AND recipients
        seen: Dict[str, str] = {}
        for e in emails:
            # Sender
            f = e.get("from") or {}
            a = f.get("address", "").lower()
            if a and a != adam:
                seen[a] = f.get("name") or a
            # TO and CC recipients — needed to detect internal threads
            # where the sender is external but the recipients are internal
            for field in ("to", "cc"):
                for r in (e.get(field) or []):
                    ra = (r.get("address") or "").lower()
                    if ra and ra != adam:
                        seen[ra] = r.get("name") or ra

        last   = emails[-1]
        l_from = last.get("from") or {}
        l_addr = l_from.get("address", "").lower()

        # Display subject: normalize the first raw subject, then title-case
        display = normalize_subject(emails[0].get("subject") or "").title()

        threads.append({
            "thread_id":           tid,
            "subject":             display,
            "email_count":         len(emails),
            "first_sent":          emails[0].get("sent_at"),
            "last_sent":           last.get("sent_at"),
            "last_sender":         l_from,
            "last_sender_is_adam": bool(adam and l_addr == adam),
            "participants":        [{"name": n, "address": a} for a, n in seen.items()],
            # Deeplink to the most recent email in the thread
            "thread_url":          outlook_url(last.get("id"), last.get("web_link")),
            "emails": [
                {
                    "id":          e.get("id"),
                    "sent_at":     e.get("sent_at"),
                    "from":        e.get("from"),
                    "body":        (e.get("body") or "")[:1500],
                    "outlook_url": outlook_url(e.get("id"), e.get("web_link")),
                }
                for e in emails
            ],
        })

    # Filter threads with no usable content (empty Graph responses)
    threads = [
        t for t in threads
        if t.get("subject") or any(e.get("body") for e in t.get("emails", []))
    ]
    threads.sort(key=lambda t: t.get("last_sent") or "", reverse=True)
    return threads

def _dedup_signals(signals: List[Dict]) -> List[Dict]:
    """
    Remove duplicate system notifications.
    Dedup key: (signal_type, day, canonical_id)
    where canonical_id = ticket_id | contact+company | document | subject[:40]
    Keep the latest occurrence of each key.
    """
    seen: Dict[tuple, Dict] = {}
    for s in signals:
        day     = (s.get("sent_at") or "")[:10]
        stype   = s.get("signal_type", "")
        ext     = s.get("extracted") or {}
        cid     = (ext.get("ticket_id")
                   or (ext.get("contact", "") + "|" + ext.get("company", ""))
                   or ext.get("document", "")
                   or (s.get("subject") or "")[:40])
        key     = (stype, day, cid.lower())
        # later occurrence wins (keeps last update of the day)
        seen[key] = s
    return list(seen.values())


# ── Per-message router ────────────────────────────────────────────────────────

def route_message(raw: Dict) -> Tuple[str, Any]:
    """Returns ('thread' | 'signal' | 'discard', data)."""
    subject = raw.get("subject") or ""
    body    = extract_body(raw)
    addr    = sender_addr_str(raw)
    sent_at = raw.get("sentDateTime") or ""
    odata   = (raw.get("@odata.type") or "").lower()

    if "eventmessage" in odata:
        return "discard", {"subject": subject, "sender": addr, "sent_at": sent_at}

    if is_discard(raw, body):
        return "discard", {"subject": subject, "sender": addr, "sent_at": sent_at}

    sig = detect_signal(raw)
    if sig:
        sig_type, extracted = sig
        return "signal", {
            "signal_type": sig_type,
            "sent_at":     sent_at,
            "subject":     subject,
            "from":        norm_addr(raw.get("from") or {}),
            "outlook_url": outlook_url(raw.get("id"), raw.get("webLink")),
            "extracted":   extracted,
        }

    return "thread", {
        "id":       raw.get("id"),
        "web_link": raw.get("webLink"),   # pre-built OWA URL with correct ID format
        "sent_at":  sent_at,
        "subject":  subject,
        "from":     norm_addr(raw.get("from") or {}),
        "to":       norm_addr_list(raw.get("toRecipients") or []),
        "cc":       norm_addr_list(raw.get("ccRecipients") or []),
        "body":     body[:1500],
    }

# ── Main ──────────────────────────────────────────────────────────────────────

DEFAULT_INPUT  = Path(__file__).resolve().parent / "outputs" / "source_emails.json"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "outputs" / "emails_processed.json"

def main() -> int:
    load_env()
    p = argparse.ArgumentParser(description="Group + clean emails → SourceArtifact JSON.")
    p.add_argument("-i", "--input",  default=str(DEFAULT_INPUT))
    p.add_argument("-o", "--output", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    artifact = make_source_artifact("email_processor")
    artifact["input_file"] = str(args.input)

    try:
        raw_artifact = json.loads(Path(args.input).read_text(encoding="utf-8"))
        raw_messages = (raw_artifact.get("objects") or {}).get("messages", {}).get("data") or []
        print(f"  Processing {len(raw_messages)} raw messages")

        thread_candidates: List[Dict] = []
        signals:           List[Dict] = []
        discards:          List[Dict] = []

        for raw in raw_messages:
            bucket, data = route_message(raw)
            if   bucket == "thread":  thread_candidates.append(data)
            elif bucket == "signal":  signals.append(data)
            else:                     discards.append(data)

        threads = build_threads(thread_candidates)
        signals = _dedup_signals(signals)

        print(f"  threads              → {len(threads):3d}  ({len(thread_candidates)} emails)")
        print(f"  system_notifications → {len(signals):3d}  (before dedup: raw count)")
        print(f"  system_notifications → {len(signals):3d}")
        print(f"  discard              → {len(discards):3d}")

        artifact["objects"] = {
            "threads": {
                "status": "success", "record_count": record_count(threads),
                "error": None, "data": threads,
            },
            "system_notifications": {
                "status": "success", "record_count": record_count(signals),
                "error": None, "data": signals,
            },
            "discard": {
                "status": "success", "record_count": record_count(discards),
                "error": None, "data": discards,
            },
        }
        artifact["status"] = "success"

    except Exception as e:
        artifact["status"] = "fail"
        artifact["error"]  = {"type": type(e).__name__, "message": str(e), "retryable": False}
        print(f"  Processing failed: {e}")
        import traceback; traceback.print_exc()

    finally:
        write_artifact(artifact, Path(args.output))
        print(f"  Wrote → {args.output}")

    return 0 if artifact["status"] == "success" else 1

if __name__ == "__main__":
    raise SystemExit(main())