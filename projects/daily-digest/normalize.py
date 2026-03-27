#!/usr/bin/env python3
"""
normalize.py
------------
Reads all source_*.json artifacts → produces a flat list of InboundItem dicts.

Each source has its own normalizer function that handles source-specific
field mapping. The output is source-agnostic.

Key decisions:
  - Email: grouped by conversationId → one InboundItem per conversation thread
  - Teams: grouped by chatId → one InboundItem per chat thread
  - Slack: grouped by thread_ts (or channel for unthreaded) → one InboundItem per thread
  - Body text: HTML stripped, messages concatenated newest-first, de-duped

Input:  outputs/source_email.json, outputs/source_teams.json, outputs/source_slack.json
Output: outputs/items_normalized.json
"""

import json
import os
import re
from collections import defaultdict
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Optional

from schemas.inbound_item import (
    InboundItem, Participant, Attachment,
    make_item_id, utc_now, snippet,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
OUTPUT_PATH = OUTPUT_DIR / "items_normalized.json"


# ── HTML stripping ────────────────────────────────────────────────────────────

class _HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip = True
        elif tag in ("br", "p", "div", "li", "tr"):
            self.text.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            self.text.append(data)

    def get_text(self) -> str:
        return "".join(self.text)


def strip_html(html: str) -> str:
    if not html:
        return ""
    stripper = _HTMLStripper()
    try:
        stripper.feed(html)
        text = stripper.get_text()
    except Exception:
        text = re.sub(r"<[^>]+>", " ", html)
    # Collapse whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


# ── User identity ─────────────────────────────────────────────────────────────

def _load_user_identity() -> dict:
    """Load user identity from config/user.yaml or env vars."""
    config_path = Path(__file__).resolve().parent / "config" / "user.yaml"
    identity = {
        "email_patterns": [],
        "display_names": [],
    }

    # Env-based (always available)
    digest_email = os.getenv("DIGEST_USER_EMAIL", "").lower().strip()
    if digest_email:
        identity["email_patterns"].append(digest_email)

    display_names = os.getenv("DIGEST_USER_DISPLAY_NAMES", "")
    if display_names:
        identity["display_names"] = [n.strip() for n in display_names.split(",") if n.strip()]

    # YAML-based (if pyyaml available)
    try:
        import yaml  # type: ignore[reportMissingImports]
        if config_path.exists():
            with open(config_path, encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
            id_cfg = cfg.get("identity", {})
            for ep in id_cfg.get("email_patterns", []):
                if ep.lower() not in identity["email_patterns"]:
                    identity["email_patterns"].append(ep.lower())
            for dn in id_cfg.get("display_names", []):
                if dn not in identity["display_names"]:
                    identity["display_names"].append(dn)
    except ImportError:
        pass

    return identity


_USER = None

def _user() -> dict:
    global _USER
    if _USER is None:
        _USER = _load_user_identity()
    return _USER


def _is_me_email(address: str) -> bool:
    addr = (address or "").lower().strip()
    return any(pat in addr for pat in _user()["email_patterns"])


def _is_me_name(name: str) -> bool:
    n = (name or "").strip().lower()
    return any(dn.lower() == n for dn in _user()["display_names"])


def _is_me(name: str, handle: str) -> bool:
    return _is_me_email(handle) or _is_me_name(name)


# ── Email normalizer ──────────────────────────────────────────────────────────

def _normalize_email(source_data: dict) -> List[InboundItem]:
    """
    Groups emails by conversationId → one InboundItem per conversation.
    """
    messages = ((source_data.get("objects") or {}).get("messages") or {}).get("data", [])
    if not messages:
        return []

    # Group by conversationId
    threads: Dict[str, list] = defaultdict(list)
    for msg in messages:
        conv_id = msg.get("conversationId") or msg.get("id", "")
        threads[conv_id].append(msg)

    items = []
    for conv_id, msgs in threads.items():
        # Sort by sentDateTime, newest first
        msgs.sort(key=lambda m: m.get("sentDateTime", ""), reverse=True)
        newest = msgs[0]
        oldest = msgs[-1]

        # Subject
        subject = (newest.get("subject") or "").strip()

        # Forward detection
        is_forwarded = bool(re.match(r"(?i)^(fw|fwd):", subject))

        # Body: concatenate all messages, newest first
        body_parts = []
        for msg in msgs:
            body_raw = (msg.get("body") or {}).get("content", "")
            body_text = strip_html(body_raw) if msg.get("body", {}).get("contentType") == "html" else body_raw
            if body_text.strip():
                sender = (msg.get("from") or {}).get("emailAddress", {})
                sender_name = sender.get("name", "Unknown")
                body_parts.append(f"[{sender_name}]\n{body_text.strip()}")
        full_body = "\n\n---\n\n".join(body_parts)

        # Author (most recent sender)
        from_field = (newest.get("from") or {}).get("emailAddress", {})
        author: Participant = {
            "name": from_field.get("name", ""),
            "handle": (from_field.get("address") or "").lower(),
            "role": "from",
        }

        # Participants
        participants = []
        seen_handles = set()
        for msg in msgs:
            # From
            f = (msg.get("from") or {}).get("emailAddress", {})
            h = (f.get("address") or "").lower()
            if h and h not in seen_handles:
                seen_handles.add(h)
                participants.append({"name": f.get("name", ""), "handle": h, "role": "from"})
            # To
            for r in msg.get("toRecipients", []):
                ea = r.get("emailAddress", {})
                h = (ea.get("address") or "").lower()
                if h and h not in seen_handles:
                    seen_handles.add(h)
                    participants.append({"name": ea.get("name", ""), "handle": h, "role": "to"})
            # CC
            for r in msg.get("ccRecipients", []):
                ea = r.get("emailAddress", {})
                h = (ea.get("address") or "").lower()
                if h and h not in seen_handles:
                    seen_handles.add(h)
                    participants.append({"name": ea.get("name", ""), "handle": h, "role": "cc"})

        # My relationship
        newest_to = [(r.get("emailAddress") or {}).get("address", "").lower()
                     for r in newest.get("toRecipients", [])]
        newest_cc = [(r.get("emailAddress") or {}).get("address", "").lower()
                     for r in newest.get("ccRecipients", [])]

        am_in_to = any(_is_me_email(a) for a in newest_to)
        am_in_cc = any(_is_me_email(a) for a in newest_cc)
        is_from_me = _is_me(author["name"], author["handle"])
        is_direct = len(newest_to) == 1 and am_in_to and not newest_cc

        # Attachments
        has_att = any(m.get("hasAttachments") for m in msgs)

        # URL (most recent message)
        url = newest.get("webLink", "")

        item_id = make_item_id("email", conv_id)

        items.append({
            "id": item_id,
            "source": "email",
            "subject": subject,
            "body_text": full_body,
            "body_snippet": snippet(full_body),
            "thread_key": conv_id,
            "message_count": len(msgs),
            "first_timestamp": oldest.get("sentDateTime", ""),
            "last_timestamp": newest.get("sentDateTime", ""),
            "author": author,
            "participants": participants,
            "participant_count": len(participants),
            "is_from_me": is_from_me,
            "mentions_me": am_in_to,
            "am_in_to": am_in_to,
            "am_in_cc": am_in_cc,
            "is_direct_message": is_direct,
            "is_forwarded": is_forwarded,
            "attachments": [],
            "has_attachments": has_att,
            "url": url,
            "source_meta": {
                "conversationId": conv_id,
                "message_ids": [m.get("id", "") for m in msgs],
            },
        })

    print(f"  [normalize] Email: {len(messages)} messages → {len(items)} threads")
    return items


# ── Teams normalizer ──────────────────────────────────────────────────────────

def _normalize_teams(source_data: dict) -> List[InboundItem]:
    """
    Groups Teams messages by chatId → one InboundItem per chat thread.
    Filters out system messages (messageType != "message").
    """
    objects = source_data.get("objects") or {}
    messages = (objects.get("messages") or {}).get("data", [])
    if not messages:
        return []

    # Group by chatId
    threads: Dict[str, list] = defaultdict(list)
    for msg in messages:
        chat_id = msg.get("_chatId") or msg.get("chatId", "")
        # Skip system messages
        if msg.get("messageType", "message") != "message":
            continue
        if not msg.get("body", {}).get("content", "").strip():
            continue
        threads[chat_id].append(msg)

    items = []
    for chat_id, msgs in threads.items():
        msgs.sort(key=lambda m: m.get("createdDateTime", ""), reverse=True)
        newest = msgs[0]
        oldest = msgs[-1]

        # Subject / topic
        subject = newest.get("_chatTopic") or None
        chat_type = newest.get("_chatType", "unknown")

        # Body: concatenate messages newest first
        body_parts = []
        for msg in msgs:
            body_raw = (msg.get("body") or {}).get("content", "")
            content_type = (msg.get("body") or {}).get("contentType", "text")
            body_text = strip_html(body_raw) if content_type == "html" else body_raw
            if body_text.strip():
                sender = (msg.get("from") or {}).get("user") or msg.get("from") or {}
                sender_name = sender.get("displayName", "Unknown")
                body_parts.append(f"[{sender_name}]\n{body_text.strip()}")
        full_body = "\n\n---\n\n".join(body_parts)

        # Author (most recent)
        from_user = (newest.get("from") or {}).get("user") or newest.get("from") or {}
        author: Participant = {
            "name": from_user.get("displayName", ""),
            "handle": (from_user.get("email") or from_user.get("id") or "").lower(),
            "role": "from",
        }

        # Participants (de-duped)
        participants = []
        seen = set()
        for msg in msgs:
            fu = (msg.get("from") or {}).get("user") or msg.get("from") or {}
            name = fu.get("displayName", "")
            handle = (fu.get("email") or fu.get("id") or "").lower()
            if handle and handle not in seen:
                seen.add(handle)
                participants.append({"name": name, "handle": handle, "role": "from"})

        # Mentions
        all_mentions = []
        for msg in msgs:
            for mention in msg.get("mentions", []):
                m = mention.get("mentioned", {})
                all_mentions.append(m.get("user", {}).get("displayName", ""))

        mentions_me = any(_is_me_name(m) for m in all_mentions)
        is_from_me = _is_me(author["name"], author["handle"])
        is_direct = chat_type == "oneOnOne"

        item_id = make_item_id("teams", chat_id)

        items.append({
            "id": item_id,
            "source": "teams",
            "subject": subject,
            "body_text": full_body,
            "body_snippet": snippet(full_body),
            "thread_key": chat_id,
            "message_count": len(msgs),
            "first_timestamp": oldest.get("createdDateTime", ""),
            "last_timestamp": newest.get("createdDateTime", ""),
            "author": author,
            "participants": participants,
            "participant_count": len(participants),
            "is_from_me": is_from_me,
            "mentions_me": mentions_me,
            "am_in_to": True,       # you're always "in" a Teams chat
            "am_in_cc": False,
            "is_direct_message": is_direct,
            "is_forwarded": False,
            "attachments": [],
            "has_attachments": False,
            "url": newest.get("_chatWebUrl", None),
            "source_meta": {
                "chatId": chat_id,
                "chatType": chat_type,
            },
        })

    print(f"  [normalize] Teams: {len(messages)} messages → {len(items)} threads")
    return items


# ── Slack normalizer ──────────────────────────────────────────────────────────

def _normalize_slack(source_data: dict) -> List[InboundItem]:
    """
    Groups Slack messages by thread_ts (threaded) or channel (unthreaded).
    STUB — matches the expected source artifact shape from slack.py.
    """
    objects = source_data.get("objects") or {}
    messages = (objects.get("messages") or {}).get("data", [])
    if not messages:
        return []

    # Group by thread_ts if available, otherwise by channel
    threads: Dict[str, list] = defaultdict(list)
    for msg in messages:
        thread_key = msg.get("thread_ts") or msg.get("ts", "")
        channel = msg.get("_channel_id", "")
        key = f"{channel}::{thread_key}" if thread_key else f"{channel}::unthreaded"
        threads[key].append(msg)
        # Also include thread replies
        for reply in msg.get("_thread_replies", []):
            reply["_channel_id"] = msg.get("_channel_id", "")
            reply["_channel_name"] = msg.get("_channel_name", "")
            threads[key].append(reply)

    items = []
    for thread_key, msgs in threads.items():
        msgs.sort(key=lambda m: float(m.get("ts", "0")), reverse=True)
        newest = msgs[0]
        oldest = msgs[-1]

        channel_name = newest.get("_channel_name", "")
        is_im = newest.get("_is_im", False)

        body_parts = []
        for msg in msgs:
            text = (msg.get("text") or "").strip()
            user_name = msg.get("_user_name") or msg.get("user", "Unknown")
            if text:
                body_parts.append(f"[{user_name}]\n{text}")
        full_body = "\n\n---\n\n".join(body_parts)

        author: Participant = {
            "name": newest.get("_user_name") or newest.get("user", ""),
            "handle": newest.get("user", ""),
            "role": "from",
        }

        participants = []
        seen = set()
        for msg in msgs:
            u = msg.get("user", "")
            if u and u not in seen:
                seen.add(u)
                participants.append(
                    {"name": msg.get("_user_name") or u, "handle": u, "role": "from"}
                )

        slack_user_id = os.getenv("SLACK_USER_ID", "")
        is_from_me = _is_me(author["name"], author["handle"]) or (
            slack_user_id and author["handle"] == slack_user_id
        )

        mention_token = f"<@{slack_user_id}>" if slack_user_id else ""
        # Mentions detection: slack mention token OR display name substring (helps when text includes names).
        display_names = _user().get("display_names", [])
        full_body_lower = (full_body or "").lower()
        mentions_by_name = any((dn or "").lower() in full_body_lower for dn in display_names)
        mentions_me = (mention_token and mention_token in full_body) or mentions_by_name

        item_id = make_item_id("slack", thread_key)

        items.append({
            "id": item_id,
            "source": "slack",
            "subject": f"#{channel_name}" if channel_name else None,
            "body_text": full_body,
            "body_snippet": snippet(full_body),
            "thread_key": thread_key,
            "message_count": len(msgs),
            "first_timestamp": oldest.get("ts", ""),
            "last_timestamp": newest.get("ts", ""),
            "author": author,
            "participants": participants,
            "participant_count": len(participants),
            "is_from_me": is_from_me,
            "mentions_me": mentions_me,
            "am_in_to": True,
            "am_in_cc": False,
            "is_direct_message": is_im,
            "is_forwarded": False,
            "attachments": [],
            "has_attachments": False,
            "url": newest.get("permalink"),
            "source_meta": {
                "channel_id": newest.get("_channel_id", ""),
                "channel_name": channel_name,
            },
        })

    print(f"  [normalize] Slack: {len(messages)} messages → {len(items)} threads")
    return items


# ── Orchestrator ──────────────────────────────────────────────────────────────

NORMALIZERS = {
    "source_email.json":  _normalize_email,
    "source_teams.json":  _normalize_teams,
    "source_slack.json":  _normalize_slack,
}


def main() -> int:
    """
    Read all source artifacts, normalize into InboundItems, write output.
    """
    print("  [normalize] Reading source artifacts...")

    all_items: List[InboundItem] = []
    sources_found = []

    for filename, normalizer in NORMALIZERS.items():
        path = OUTPUT_DIR / filename
        if not path.exists():
            print(f"  [normalize] {filename} not found, skipping.")
            continue

        try:
            with open(path, encoding="utf-8") as f:
                source_data = json.load(f)
        except Exception as e:
            print(f"  [normalize] Failed to read {filename}: {e}")
            continue

        if source_data.get("status") in ("fail",):
            print(f"  [normalize] {filename} status=fail, skipping.")
            continue
        if source_data.get("status") == "skipped":
            print(f"  [normalize] {filename} status=skipped, skipping.")
            continue

        items = normalizer(source_data)
        all_items.extend(items)
        sources_found.append(filename.replace("source_", "").replace(".json", ""))

    # Sort all items by last_timestamp, newest first
    all_items.sort(key=lambda i: i.get("last_timestamp", ""), reverse=True)

    output = {
        "normalized_at": utc_now(),
        "sources": sources_found,
        "item_count": len(all_items),
        "items": all_items,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"  [normalize] Total: {len(all_items)} items from {sources_found}")
    print(f"  [normalize] Wrote → {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
