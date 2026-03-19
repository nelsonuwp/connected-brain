#!/usr/bin/env python3
"""
process.py

Reads source_emails.json → groups into threads, extracts system notification
signals, and builds a compact SourceArtifact ready for the LLM step.

Output objects:
  threads              — human conversations clustered by normalized subject,
                         with cross-thread similarity merging for related topics
  system_notifications — tool/automated signals with deterministically extracted data
  discard              — audit list only (subject + sender + date, no bodies)

Output: outputs/emails_processed.json

Changes vs v1:
  - All discard + signal patterns live in config/discard_rules.yaml (no hardcoding)
  - Cross-thread similarity merging (stopword-stripped token Jaccard + sender weight)
  - Thread metadata: sole_recipient, adam_in_to flags for LLM action-routing
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
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from connectors.source_artifact import make_source_artifact, record_count, write_artifact

INTERNAL_DOMAINS  = {"aptum.com", "cloudops.com"}
CONFIG_PATH       = Path(__file__).resolve().parent / "config" / "discard_rules.yaml"
DEFAULT_INPUT     = Path(__file__).resolve().parent / "outputs" / "source_emails.json"
DEFAULT_OUTPUT    = Path(__file__).resolve().parent / "outputs" / "emails_processed.json"

# Module-level rules cache — populated once in main()
_RULES: Optional[Dict] = None


# ── Env ───────────────────────────────────────────────────────────────────────

def _sq(v: str) -> str:
    v = v.strip()
    return v[1:-1] if len(v) >= 2 and v[0] == v[-1] in ('"', "'") else v

def load_env() -> None:
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
                if k and (k not in os.environ or os.environ[k] == ""):
                    os.environ[k] = _sq(v)
        except OSError:
            pass


# ── Rule loading ──────────────────────────────────────────────────────────────

def load_rules(config_path: Path = CONFIG_PATH) -> Dict:
    """
    Load and compile all discard + signal + merge rules from YAML.
    Falls back to empty rules on missing/broken file — pipeline degrades
    gracefully rather than crashing.
    """
    try:
        data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        print(f"  Loaded rules from {config_path}")
    except FileNotFoundError:
        print(f"  [config] discard_rules.yaml not found at {config_path} — using empty rules")
        data = {}
    except Exception as e:
        print(f"  [config] Failed to load discard_rules.yaml: {e} — using empty rules")
        data = {}

    discard = data.get("discard") or {}
    signals = data.get("signals") or {}
    merge   = data.get("merge")   or {}

    def _compile(patterns, flags=re.I):
        compiled = []
        for p in (patterns or []):
            try:
                compiled.append(re.compile(p, flags))
            except re.error as e:
                print(f"  [config] Bad pattern '{p}': {e} — skipped")
        return compiled

    return {
        # Discard
        "sender_domains":          [str(d).lower() for d in (discard.get("sender_domains") or [])],
        "sender_patterns":         _compile(discard.get("sender_patterns")),
        "subject_patterns":        _compile(discard.get("subject_patterns")),
        "body_patterns":           _compile(discard.get("body_patterns")),
        # Signals — list of (compiled_pattern, type_str)
        "signal_subject_patterns": [
            (re.compile(p["pattern"], re.I), p["type"])
            for p in (signals.get("subject_patterns") or [])
            if "pattern" in p and "type" in p
        ],
        "signal_sender_patterns":  [
            (re.compile(p["pattern"], re.I), p["type"])
            for p in (signals.get("sender_patterns") or [])
            if "pattern" in p and "type" in p
        ],
        # Merge
        "merge_sensitivity": float(merge.get("merge_sensitivity", 0.25)),
        "same_sender_bonus": float(merge.get("same_sender_bonus", 0.12)),
    }


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

def outlook_url(msg_id: str, web_link: str = None) -> Optional[str]:
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

def _domain_matches(sender_domain: str, pattern: str) -> bool:
    """Match *.example.com (any subdomain) or exact example.com."""
    d = sender_domain.lower()
    p = pattern.lower()
    if p.startswith("*."):
        base = p[2:]
        return d == base or d.endswith("." + base)
    return d == p

def is_discard(raw: Dict, body: str, rules: Dict) -> bool:
    addr     = sender_addr_str(raw)
    subj     = raw.get("subject") or ""
    domain   = sender_domain_str(raw)
    internal = domain in INTERNAL_DOMAINS

    for pat in rules["sender_domains"]:
        if _domain_matches(domain, pat):
            return True
    for pat in rules["sender_patterns"]:
        if pat.search(addr):
            return True
    for pat in rules["subject_patterns"]:
        if pat.search(subj):
            return True
    if not internal:
        for pat in rules["body_patterns"]:
            if pat.search(body[:500]):
                return True
    return False


# ── Signal detection ──────────────────────────────────────────────────────────

def _extract_signal_data(sig_type: str, subject: str) -> Dict:
    """Type-specific extraction — lives in code; types defined in YAML."""
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

def detect_signal(raw: Dict, rules: Dict) -> Optional[Tuple[str, Dict]]:
    """Returns (signal_type, extracted_data) or None. Patterns loaded from YAML."""
    addr  = sender_addr_str(raw)
    subj  = raw.get("subject") or ""
    adam  = os.getenv("USER_EMAIL", "").lower()

    if adam and addr == adam:
        return "auto_forward", {"subject": subj[:100]}

    for pat, sig_type in rules["signal_subject_patterns"]:
        if pat.search(subj):
            return sig_type, _extract_signal_data(sig_type, subj)

    for pat, sig_type in rules["signal_sender_patterns"]:
        if pat.search(addr):
            return sig_type, {"subject": subj[:100]}

    return None


# ── Per-message router ────────────────────────────────────────────────────────

def route_message(raw: Dict, rules: Dict) -> Tuple[str, Any]:
    """Returns ('thread' | 'signal' | 'discard', data)."""
    subject = raw.get("subject") or ""
    body    = extract_body(raw)
    addr    = sender_addr_str(raw)
    sent_at = raw.get("sentDateTime") or ""
    odata   = (raw.get("@odata.type") or "").lower()

    if "eventmessage" in odata:
        return "discard", {"subject": subject, "sender": addr, "sent_at": sent_at}

    if is_discard(raw, body, rules):
        return "discard", {"subject": subject, "sender": addr, "sent_at": sent_at}

    sig = detect_signal(raw, rules)
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
        "web_link": raw.get("webLink"),
        "sent_at":  sent_at,
        "subject":  subject,
        "from":     norm_addr(raw.get("from") or {}),
        "to":       norm_addr_list(raw.get("toRecipients") or []),
        "cc":       norm_addr_list(raw.get("ccRecipients") or []),
        "body":     body[:1500],
    }


# ── Thread building ───────────────────────────────────────────────────────────

def build_threads(candidates: List[Dict]) -> List[Dict]:
    """
    Cluster email dicts by normalized subject, sort chronologically within each
    thread. Adds sole_recipient and adam_in_to flags for LLM action routing.
    """
    adam   = os.getenv("USER_EMAIL", "").lower()
    groups: Dict[str, List[Dict]] = defaultdict(list)

    for e in candidates:
        groups[thread_key(e.get("subject") or "")].append(e)

    threads = []
    for tid, emails in groups.items():
        emails.sort(key=lambda x: x.get("sent_at") or "")

        first_raw_subj = emails[0].get("subject", "")
        is_forward = bool(re.match(r"^(fw|fwd)\s*:", first_raw_subj, re.I))

        # Unique participants (excluding Adam)
        seen: Dict[str, str] = {}
        for e in emails:
            f = e.get("from") or {}
            a = f.get("address", "").lower()
            if a and a != adam:
                seen[a] = f.get("name") or a
            for field in ("to", "cc"):
                for r in (e.get(field) or []):
                    ra = (r.get("address") or "").lower()
                    if ra and ra != adam:
                        seen[ra] = r.get("name") or ra

        # ── TO-cardinality flags ──────────────────────────────────────────────
        # Collected across ALL emails in the thread (any email triggers the flag)
        all_to_addresses: List[str] = []
        for e in emails:
            all_to_addresses.extend(
                (r.get("address") or "").lower()
                for r in (e.get("to") or [])
            )
        adam_in_to    = bool(adam and adam in all_to_addresses)
        non_adam_to   = [a for a in all_to_addresses if a and a != adam]
        sole_recipient = adam_in_to and len(non_adam_to) == 0

        last   = emails[-1]
        l_from = last.get("from") or {}
        l_addr = l_from.get("address", "").lower()

        # Clean display subject
        s = (emails[0].get("subject") or "").strip()
        while True:
            s2 = re.sub(r"^\[.*?\]\s*", "", s).strip()
            s2 = re.sub(r"^(re|fw|fwd)\s*:\s*", "", s2, flags=re.I).strip()
            if s2 == s:
                break
            s = s2
        display = s if s else (emails[0].get("subject") or "")

        threads.append({
            "thread_id":           tid,
            "subject":             display,
            "is_forward":          is_forward,
            "is_merged":           False,
            "source_threads":      [],
            "email_count":         len(emails),
            "first_sent":          emails[0].get("sent_at"),
            "last_sent":           last.get("sent_at"),
            "last_sender":         l_from,
            "last_sender_is_adam": bool(adam and l_addr == adam),
            "participants":        [{"name": n, "address": a} for a, n in seen.items()],
            "thread_url":          outlook_url(last.get("id"), last.get("web_link")),
            "sole_recipient":      sole_recipient,
            "adam_in_to":          adam_in_to,
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

    threads = [
        t for t in threads
        if t.get("subject") or any(e.get("body") for e in t.get("emails", []))
    ]
    threads.sort(key=lambda t: t.get("last_sent") or "", reverse=True)
    return threads


# ── Cross-thread similarity merging ──────────────────────────────────────────

_STOPWORDS = frozenset({
    "re", "fw", "fwd", "the", "a", "an", "is", "are", "was", "were",
    "and", "or", "for", "to", "in", "on", "at", "by", "of", "from",
    "your", "my", "our", "his", "her", "their", "its", "please", "hi",
    "hello", "thanks", "thank", "you", "i", "we", "they", "it", "this",
    "that", "with", "have", "has", "had", "will", "be", "do", "not",
    "can", "could", "would", "should", "may", "might", "get", "got",
    "need", "about", "regarding", "per", "as", "if", "up", "out",
    "just", "also", "well", "all", "any", "some", "no", "more", "new",
    "email", "message", "follow", "update", "here", "attached", "see",
    "below", "above", "forward", "sent", "received", "dear", "kindly",
    "best", "regards", "sincerely", "team", "everyone", "all",
})

def _tokenize(subject: str, sender_addr: str) -> Set[str]:
    """
    Meaningful tokens from normalized subject + weighted sender domain.
    Sender domain is added 3× to weight it above any single subject word —
    two threads from the same sender need less subject overlap to merge.
    """
    normalized = normalize_subject(subject)
    tokens = set(re.findall(r'\b[a-z0-9]+\b', normalized)) - _STOPWORDS
    # Remove pure stopword strings and very short tokens (< 3 chars)
    tokens = {t for t in tokens if len(t) >= 3}
    # Weighted sender domain
    if "@" in sender_addr:
        domain_root = sender_addr.split("@")[-1].split(".")[0].lower()
        if len(domain_root) >= 3 and domain_root not in _STOPWORDS:
            sender_token = f"__sender_{domain_root}"
            tokens.update([sender_token, sender_token, sender_token])
    return tokens

def _jaccard(a: Set[str], b: Set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

def _combined_similarity(
    thread_a: Dict, thread_b: Dict,
    tok_a: Set[str], tok_b: Set[str],
    same_sender_bonus: float,
) -> float:
    """
    Token Jaccard + optional same-sender bonus.
    Bonus applies when both threads share the exact same sender address —
    two emails from the same person about loosely related topics are much
    more likely to be related than the token overlap alone implies.
    """
    jaccard = _jaccard(tok_a, tok_b)

    addr_a = (thread_a.get("last_sender") or {}).get("address", "").lower()
    addr_b = (thread_b.get("last_sender") or {}).get("address", "").lower()
    bonus  = same_sender_bonus if (addr_a and addr_a == addr_b) else 0.0

    return jaccard + bonus

def _union_find(n: int) -> List[int]:
    return list(range(n))

def _find(parent: List[int], i: int) -> int:
    while parent[i] != i:
        parent[i] = parent[parent[i]]
        i = parent[i]
    return i

def _union(parent: List[int], i: int, j: int) -> None:
    parent[_find(parent, i)] = _find(parent, j)

def _do_merge(threads: List[Dict], sensitivity: float, same_sender_bonus: float = 0.12) -> List[Dict]:
    """
    Find thread pairs above the combined similarity threshold, merge transitively
    using union-find, return the new thread list with merged entries substituted.

    similarity = token_jaccard + same_sender_bonus (if senders match exactly)
    """
    n = len(threads)
    if n < 2:
        return threads

    token_sets = [
        _tokenize(
            t.get("subject", ""),
            (t.get("last_sender") or {}).get("address", ""),
        )
        for t in threads
    ]

    parent = _union_find(n)
    for i in range(n):
        for j in range(i + 1, n):
            sim = _combined_similarity(
                threads[i], threads[j],
                token_sets[i], token_sets[j],
                same_sender_bonus,
            )
            if sim >= sensitivity:
                print(f"  [merge] '{threads[i]['subject'][:40]}' + '{threads[j]['subject'][:40]}' "
                      f"(sim={sim:.2f})")
                _union(parent, i, j)

    # Group indices by root
    groups: Dict[int, List[int]] = defaultdict(list)
    for i in range(n):
        groups[_find(parent, i)].append(i)

    result = []
    for root, indices in groups.items():
        if len(indices) == 1:
            result.append(threads[indices[0]])
        else:
            result.append(_combine_threads([threads[i] for i in indices]))

    result.sort(key=lambda t: t.get("last_sent") or "", reverse=True)
    return result

def _combine_threads(group: List[Dict]) -> Dict:
    """Merge a group of threads into one combined thread dict."""
    adam = os.getenv("USER_EMAIL", "").lower()

    # Sort group by first_sent so oldest thread leads
    group = sorted(group, key=lambda t: t.get("first_sent") or "")

    # Combine and sort all emails chronologically; tag each with its source thread
    all_emails = []
    for t in group:
        for e in t.get("emails", []):
            all_emails.append({**e, "_source_thread": t["subject"]})
    all_emails.sort(key=lambda e: e.get("sent_at") or "")

    last_email  = all_emails[-1]
    l_from      = last_email.get("from") or {}
    l_addr      = (l_from.get("address") or "").lower()

    # Union of participants
    seen: Dict[str, str] = {}
    for t in group:
        for p in t.get("participants", []):
            a = (p.get("address") or "").lower()
            if a:
                seen[a] = p.get("name") or a

    merged_id = "merged_" + hashlib.md5(
        "_".join(t["thread_id"] for t in group).encode()
    ).hexdigest()[:8]

    # TO-cardinality: conservative union — sole_recipient only if ALL were sole
    sole_recipient = all(t.get("sole_recipient", False) for t in group)
    adam_in_to     = any(t.get("adam_in_to", False) for t in group)

    return {
        "thread_id":           merged_id,
        "subject":             "[Merged]",         # LLM generates unified_subject
        "is_merged":           True,
        "source_threads": [
            {"subject": t["subject"], "thread_url": t.get("thread_url")}
            for t in group
        ],
        "is_forward":          False,
        "email_count":         len(all_emails),
        "first_sent":          all_emails[0].get("sent_at"),
        "last_sent":           last_email.get("sent_at"),
        "last_sender":         l_from,
        "last_sender_is_adam": bool(adam and l_addr == adam),
        "participants":        [{"name": n, "address": a} for a, n in seen.items()],
        "thread_url":          last_email.get("outlook_url"),
        "sole_recipient":      sole_recipient,
        "adam_in_to":          adam_in_to,
        "emails":              all_emails,
    }


# ── Signal dedup ──────────────────────────────────────────────────────────────

def _dedup_signals(signals: List[Dict]) -> List[Dict]:
    seen: Dict[tuple, Dict] = {}
    for s in signals:
        day   = (s.get("sent_at") or "")[:10]
        stype = s.get("signal_type", "")
        ext   = s.get("extracted") or {}
        cid   = (ext.get("ticket_id")
                 or (ext.get("contact", "") + "|" + ext.get("company", ""))
                 or ext.get("document", "")
                 or (s.get("subject") or "")[:40])
        key        = (stype, day, cid.lower())
        seen[key]  = s
    return list(seen.values())


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    load_env()
    p = argparse.ArgumentParser(description="Group + clean emails → SourceArtifact JSON.")
    p.add_argument("-i", "--input",  default=str(DEFAULT_INPUT))
    p.add_argument("-o", "--output", default=str(DEFAULT_OUTPUT))
    p.add_argument("--config", default=str(CONFIG_PATH),
                   help="Path to discard_rules.yaml")
    args = p.parse_args()

    rules = load_rules(Path(args.config))

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
            bucket, data = route_message(raw, rules)
            if   bucket == "thread":  thread_candidates.append(data)
            elif bucket == "signal":  signals.append(data)
            else:                     discards.append(data)

        threads = build_threads(thread_candidates)

        # Cross-thread similarity merge
        sensitivity        = rules["merge_sensitivity"]
        same_sender_bonus  = rules["same_sender_bonus"]
        print(f"  Running cross-thread merge (sensitivity={sensitivity}, sender_bonus={same_sender_bonus}) on {len(threads)} threads …")
        threads = _do_merge(threads, sensitivity, same_sender_bonus)

        merged_count = sum(1 for t in threads if t.get("is_merged"))
        if merged_count:
            print(f"  Merged {merged_count} thread group(s)")

        signals = _dedup_signals(signals)

        print(f"  threads              → {len(threads):3d}")
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
