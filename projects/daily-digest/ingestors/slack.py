#!/usr/bin/env python3
"""
ingestors/slack.py
------------------
Fetches Slack messages from the Slack API for a date range.
Writes a SourceArtifact JSON — raw payload, never reshaped.

STUB — API calls are TODO. Structure is complete.

Output: outputs/source_slack.json

Slack API endpoints (once you have a Bot Token):
  conversations.list          → list channels the bot is in
  conversations.history       → messages in a channel (date-filtered via oldest/latest)
  conversations.replies       → thread replies for a parent message

Setup:
  1. Create a Slack App at https://api.slack.com/apps
  2. Add Bot Token Scopes: channels:history, channels:read, groups:history,
     groups:read, im:history, im:read, mpim:history, mpim:read, users:read
  3. Install to workspace
  4. Copy Bot Token (xoxb-...) to .env as SLACK_BOT_TOKEN
  5. Optionally copy User Token (xoxp-...) for user-level message access

Env vars:
  SLACK_BOT_TOKEN       required — xoxb-...
  SLACK_USER_TOKEN      optional — xoxp-... (for DM access)
  SLACK_WORKSPACE       required for permalinks — workspace subdomain (e.g. "aptum" from aptum.slack.com)
  SLACK_WORKSPACE_ID    optional — for logging
"""

import os
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import requests
from connectors.source_artifact import (
    make_source_artifact, record_count, write_artifact
)

OUTPUT_DIR  = Path(__file__).resolve().parents[1] / "outputs"
OUTPUT_PATH = OUTPUT_DIR / "source_slack.json"


def _get_bot_token() -> str:
    token = os.getenv("SLACK_BOT_TOKEN", "")
    token = (token or "").strip()
    # Common failure mode: .env contains a placeholder/comment value like:
    #   SLACK_BOT_TOKEN=           # xoxb-... from Slack App
    # `_load_env()` will parse that as the token value unless you remove the duplicate.
    if not token or token.startswith("#"):
        raise RuntimeError(
            "SLACK_BOT_TOKEN not set (or contains placeholder/comment). Fix .env and re-run. See ingestors/slack.py header."
        )
    return token


def _to_unix_ts(d: date) -> int:
    """Date -> unix epoch seconds (UTC midnight)."""
    dt = datetime.combine(d, time.min, tzinfo=timezone.utc)
    return int(dt.timestamp())


def _slack_mention(slack_user_id: str) -> str:
    return f"<@{slack_user_id}>" if slack_user_id else ""


def fetch_channels(token: str) -> List[Dict[str, Any]]:
    """
    Fetch list of channels the bot is a member of (via users.conversations).
    """
    all_channels: List[Dict[str, Any]] = []
    cursor = None
    while True:
        params = {
            "types": "public_channel,private_channel,mpim,im",
            "limit": 200,
            "exclude_archived": "true",
        }
        if cursor:
            params["cursor"] = cursor

        resp = requests.get(
            "https://slack.com/api/users.conversations",
            headers={"Authorization": f"Bearer {token}"},
            params=params,
        )
        data = resp.json()
        if not data.get("ok"):
            raise RuntimeError(f"Slack users.conversations error: {data.get('error')}")

        all_channels.extend(data.get("channels", []))
        cursor = (data.get("response_metadata") or {}).get("next_cursor")
        if not cursor:
            break

    return all_channels


def fetch_channel_messages(
    channel_id: str, start: date, end: date, token: str
) -> List[Dict[str, Any]]:
    """
    Fetch messages from a channel within the date range.
    """
    oldest_ts = _to_unix_ts(start)
    latest_ts = _to_unix_ts(end + timedelta(days=1))

    all_messages: List[Dict[str, Any]] = []
    cursor = None

    while True:
        params = {
            "channel": channel_id,
            "oldest": str(oldest_ts),
            "latest": str(latest_ts),
            "limit": 200,
        }
        if cursor:
            params["cursor"] = cursor

        resp = requests.get(
            "https://slack.com/api/conversations.history",
            headers={"Authorization": f"Bearer {token}"},
            params=params,
        )
        data = resp.json()
        if not data.get("ok"):
            # e.g. missing_scope / not_in_channel
            print(f"    [slack] conversations.history error for {channel_id}: {data.get('error')}")
            return all_messages

        all_messages.extend(data.get("messages", []))
        cursor = (data.get("response_metadata") or {}).get("next_cursor")
        if not cursor:
            break

    # Fetch thread replies for parents with replies
    for msg in all_messages:
        if msg.get("reply_count", 0) > 0 and msg.get("ts"):
            thread_resp = requests.get(
                "https://slack.com/api/conversations.replies",
                headers={"Authorization": f"Bearer {token}"},
                params={"channel": channel_id, "ts": msg["ts"], "limit": 200},
            )
            thread_data = thread_resp.json()
            if thread_data.get("ok"):
                # Skip the parent message (index 0) to avoid duplication.
                msg["_thread_replies"] = thread_data.get("messages", [])[1:]

    return all_messages


def resolve_users(messages: List[Dict[str, Any]], token: str) -> Dict[str, str]:
    """Resolve Slack user IDs to display names. Returns {user_id: display_name}."""
    user_ids = set()
    for msg in messages:
        if msg.get("user"):
            user_ids.add(msg["user"])
        for reply in msg.get("_thread_replies", []) or []:
            if reply.get("user"):
                user_ids.add(reply["user"])

    user_map: Dict[str, str] = {}
    for uid in user_ids:
        resp = requests.get(
            "https://slack.com/api/users.info",
            headers={"Authorization": f"Bearer {token}"},
            params={"user": uid},
        )
        data = resp.json()
        if data.get("ok"):
            profile = (data.get("user") or {}).get("profile", {}) or {}
            name = profile.get("real_name") or profile.get("display_name") or uid
            user_map[uid] = name
        else:
            user_map[uid] = uid

    # Attach resolved names back onto the message objects (used by normalize.py).
    for msg in messages:
        u = msg.get("user", "")
        msg["_user_name"] = user_map.get(u, u)
        for reply in msg.get("_thread_replies", []) or []:
            ru = reply.get("user", "")
            reply["_user_name"] = user_map.get(ru, ru)

    return user_map


def main(start: date, end: date) -> int:
    """
    Called by run_pipeline.py with explicit date range.
    Returns 0 (success) even when stub — allows pipeline to continue.
    """
    print(f"  [slack] Capturing Slack messages {start} → {end}")

    artifact = make_source_artifact("slack")
    artifact["date_range"] = {"start": start.isoformat(), "end": end.isoformat()}

    bot_token = (os.getenv("SLACK_BOT_TOKEN", "") or "").strip()
    slack_user_id = (os.getenv("SLACK_USER_ID", "") or "").strip()
    mention = _slack_mention(slack_user_id)

    if not bot_token or bot_token.startswith("#"):
        artifact["status"] = "skipped"
        artifact["objects"] = {
            "messages": {
                "status": "skipped",
                "record_count": 0,
                "error": "SLACK_BOT_TOKEN missing or placeholder/comment value (check .env duplicate SLACK section).",
                "data": [],
            }
        }
        print("  [slack] Skipped — SLACK_BOT_TOKEN missing or placeholder/comment value. Check .env duplicate SLACK section.")
        write_artifact(artifact, OUTPUT_PATH)
        return 0  # Not a failure — just not configured yet

    try:
        channels = fetch_channels(bot_token)
        all_messages = []

        fetched_count = 0
        kept_count = 0
        resolved_user_ids = set()

        for channel in channels:
            ch_id = channel.get("id", "")
            is_im = bool(channel.get("is_im", False))
            is_mpim = bool(channel.get("is_mpim", False))
            ch_name = channel.get("name", "") or ch_id

            messages = fetch_channel_messages(ch_id, start, end, bot_token)
            fetched_count += len(messages)

            for msg in messages:
                msg["_channel_id"] = ch_id
                msg["_channel_name"] = ch_name
                msg["_is_im"] = is_im
                msg["_is_mpim"] = is_mpim

            def is_relevant_thread(parent_msg: Dict[str, Any]) -> bool:
                # For DMs and group DMs, keep everything the bot can read.
                if is_im or is_mpim:
                    return True
                if not slack_user_id:
                    # If we don't know who "me" is, don't filter aggressively.
                    return True

                if parent_msg.get("user") == slack_user_id:
                    return True
                if mention and mention in (parent_msg.get("text") or ""):
                    return True
                for reply in parent_msg.get("_thread_replies", []) or []:
                    if reply.get("user") == slack_user_id:
                        return True
                    if mention and mention in (reply.get("text") or ""):
                        return True
                return False

            kept_messages = [m for m in messages if is_relevant_thread(m)]
            kept_count += len(kept_messages)
            all_messages.extend(kept_messages)

        artifact["objects"] = {
            "channels": {
                "status": "success",
                "record_count": record_count(channels),
                "error": None,
                "data": channels,
            },
            "messages": {
                "status": "success",
                "record_count": record_count(all_messages),
                "error": None,
                "data": all_messages,
            },
        }

        # Resolve user IDs to names AFTER filtering (keeps API usage down).
        user_map = resolve_users(all_messages, bot_token) if all_messages else {}
        resolved_user_ids = set(user_map.keys())

        artifact["status"] = "success"
        print(
            f"  [slack] Bot is member of {len(channels)} channel(s)."
            f" Fetched {fetched_count} messages, kept {kept_count} relevant messages."
        )
        if slack_user_id:
            print(f"  [slack] Resolved {len(resolved_user_ids)} user IDs to display names.")
        else:
            print("  [slack] SLACK_USER_ID not set; relevance filtering may be less accurate.")
        print(f"  [slack] Captured {len(all_messages)} messages across {len(channels)} channels.")

    except Exception as e:
        artifact["status"] = "fail"
        artifact["error"] = {"type": type(e).__name__, "message": str(e), "retryable": False}
        print(f"  [slack] Capture failed: {e}")

    finally:
        write_artifact(artifact, OUTPUT_PATH)
        print(f"  [slack] Wrote → {OUTPUT_PATH}")

    return 0 if artifact["status"] in ("success", "skipped") else 1
