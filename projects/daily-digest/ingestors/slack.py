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
  SLACK_WORKSPACE_ID    optional — for logging
"""

import os
from datetime import date
from pathlib import Path
from typing import Any, Dict, List

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from connectors.source_artifact import (
    make_source_artifact, record_count, write_artifact
)

OUTPUT_DIR  = Path(__file__).resolve().parents[1] / "outputs"
OUTPUT_PATH = OUTPUT_DIR / "source_slack.json"


def _get_bot_token() -> str:
    token = os.getenv("SLACK_BOT_TOKEN", "")
    if not token:
        raise RuntimeError(
            "SLACK_BOT_TOKEN not set. See ingestors/slack.py header for setup instructions."
        )
    return token


def fetch_channels(token: str) -> List[Dict[str, Any]]:
    """
    TODO: Fetch list of channels the bot has access to.

    Use: https://api.slack.com/methods/conversations.list
    Params: types=public_channel,private_channel,mpim,im

    Returns list of channel dicts with id, name, is_im, is_mpim, etc.
    """
    # import requests
    # resp = requests.get("https://slack.com/api/conversations.list", params={
    #     "types": "public_channel,private_channel,mpim,im",
    #     "limit": 200,
    # }, headers={"Authorization": f"Bearer {token}"})
    # data = resp.json()
    # if not data.get("ok"):
    #     raise RuntimeError(f"Slack API error: {data.get('error')}")
    # return data.get("channels", [])
    return []


def fetch_channel_messages(
    channel_id: str, start: date, end: date, token: str
) -> List[Dict[str, Any]]:
    """
    TODO: Fetch messages from a channel within the date range.

    Use: https://api.slack.com/methods/conversations.history
    Params: channel, oldest (unix ts), latest (unix ts), limit

    For threaded messages, also call conversations.replies for each
    parent message that has reply_count > 0.
    """
    # import time
    # oldest = str(int(time.mktime(start.timetuple())))
    # latest = str(int(time.mktime(end.timetuple())) + 86400)  # end of day
    # resp = requests.get("https://slack.com/api/conversations.history", params={
    #     "channel": channel_id,
    #     "oldest": oldest,
    #     "latest": latest,
    #     "limit": 200,
    # }, headers={"Authorization": f"Bearer {token}"})
    # data = resp.json()
    # if not data.get("ok"):
    #     return []
    # messages = data.get("messages", [])
    # # Fetch thread replies for each parent
    # for msg in messages:
    #     if msg.get("reply_count", 0) > 0:
    #         thread_resp = requests.get("https://slack.com/api/conversations.replies", params={
    #             "channel": channel_id,
    #             "ts": msg["ts"],
    #             "limit": 100,
    #         }, headers={"Authorization": f"Bearer {token}"})
    #         thread_data = thread_resp.json()
    #         if thread_data.get("ok"):
    #             msg["_thread_replies"] = thread_data.get("messages", [])[1:]  # skip parent
    # return messages
    return []


def main(start: date, end: date) -> int:
    """
    Called by run_pipeline.py with explicit date range.
    Returns 0 (success) even when stub — allows pipeline to continue.
    """
    print(f"  [slack] Capturing Slack messages {start} → {end}")

    artifact = make_source_artifact("slack")
    artifact["date_range"] = {"start": start.isoformat(), "end": end.isoformat()}

    bot_token = os.getenv("SLACK_BOT_TOKEN", "")

    if not bot_token:
        artifact["status"] = "skipped"
        artifact["objects"] = {
            "messages": {
                "status": "skipped",
                "record_count": 0,
                "error": "SLACK_BOT_TOKEN not configured",
                "data": [],
            }
        }
        print("  [slack] Skipped — SLACK_BOT_TOKEN not set.")
        write_artifact(artifact, OUTPUT_PATH)
        return 0  # Not a failure — just not configured yet

    try:
        channels = fetch_channels(bot_token)
        all_messages = []

        for channel in channels:
            ch_id = channel.get("id", "")
            messages = fetch_channel_messages(ch_id, start, end, bot_token)
            for msg in messages:
                msg["_channel_id"] = ch_id
                msg["_channel_name"] = channel.get("name", "")
                msg["_is_im"] = channel.get("is_im", False)
            all_messages.extend(messages)

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
        artifact["status"] = "success"
        print(f"  [slack] Captured {len(all_messages)} messages across {len(channels)} channels.")

    except Exception as e:
        artifact["status"] = "fail"
        artifact["error"] = {"type": type(e).__name__, "message": str(e), "retryable": False}
        print(f"  [slack] Capture failed: {e}")

    finally:
        write_artifact(artifact, OUTPUT_PATH)
        print(f"  [slack] Wrote → {OUTPUT_PATH}")

    return 0 if artifact["status"] in ("success", "skipped") else 1
