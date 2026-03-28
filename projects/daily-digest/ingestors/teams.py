#!/usr/bin/env python3
"""
ingestors/teams.py
------------------
Fetches Teams chat messages from Microsoft Graph for a date range.
Writes a SourceArtifact JSON — raw payload, never reshaped.

Uses the same OAuth token as email.py (shared via _ms_auth.py).
Requires Chat.Read scope.

Output: outputs/source_teams.json

MS Graph endpoints:
  GET /me/chats                         → list all chats (1:1, group, meeting)
  GET /me/chats/{chatId}/messages       → messages in a chat

Approach:
  1. List all chats that have activity in the date range
  2. For each active chat, fetch messages within the date range
  3. Write as SourceArtifact with objects.chats (chat metadata) and objects.messages (all messages)
"""

import os
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, List

import requests

from ._ms_auth import get_access_token

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from connectors.source_artifact import (
    make_source_artifact, record_count, write_artifact
)

OUTPUT_DIR  = Path(__file__).resolve().parents[1] / "outputs"
OUTPUT_PATH = OUTPUT_DIR / "source_teams.json"

# Maximum chats to scan for messages (safety valve)
MAX_CHATS = 100
# Maximum messages per chat
MAX_MESSAGES_PER_CHAT = 100


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def fetch_active_chats(token: str) -> List[Dict[str, Any]]:
    """
    Fetch list of chats, ordered by most recent activity.
    Returns up to MAX_CHATS chats.
    """
    url = "https://graph.microsoft.com/v1.0/me/chats"
    params = {
        "$expand": "members",
        "$top": 50,
        "$orderby": "lastMessagePreview/createdDateTime desc",
    }

    chats = []
    resp = requests.get(url, headers=_headers(token), params=params)
    resp.raise_for_status()
    data = resp.json()
    chats.extend(data.get("value", []))

    # Paginate
    while (next_link := data.get("@odata.nextLink")) and len(chats) < MAX_CHATS:
        resp = requests.get(next_link, headers=_headers(token))
        resp.raise_for_status()
        data = resp.json()
        chats.extend(data.get("value", []))

    print(f"  [teams] Found {len(chats)} chats.")
    return chats[:MAX_CHATS]


def fetch_chat_messages(
    chat_id: str, start: date, end: date, token: str
) -> List[Dict[str, Any]]:
    """
    Fetch messages from a specific chat within the date range.
    """
    url = f"https://graph.microsoft.com/v1.0/me/chats/{chat_id}/messages"
    # Graph doesn't support $filter on chat messages directly.
    # We fetch recent messages and filter client-side.
    params = {"$top": MAX_MESSAGES_PER_CHAT}

    messages = []
    resp = requests.get(url, headers=_headers(token), params=params)

    if resp.status_code == 403:
        # Some chats may not be accessible (e.g., channel chats without permission)
        return []
    resp.raise_for_status()

    data = resp.json()
    all_msgs = data.get("value", [])

    # Client-side date filter
    start_iso = f"{start.isoformat()}T00:00:00Z"
    end_iso = f"{(end + timedelta(days=1)).isoformat()}T00:00:00Z"

    for msg in all_msgs:
        created = msg.get("createdDateTime", "")
        if start_iso <= created < end_iso:
            messages.append(msg)

    return messages


def main(start: date, end: date) -> int:
    """
    Called by run_pipeline.py with explicit date range.
    """
    print(f"  [teams] Capturing Teams messages {start} → {end}")

    artifact = make_source_artifact("teams")
    artifact["date_range"] = {"start": start.isoformat(), "end": end.isoformat()}

    try:
        token = get_access_token()
        chats = fetch_active_chats(token)

        all_messages = []
        active_chats = []

        for chat in chats:
            chat_id = chat.get("id", "")
            if not chat_id:
                continue

            messages = fetch_chat_messages(chat_id, start, end, token)
            if messages:
                active_chats.append(chat)
                for msg in messages:
                    msg["_chatId"] = chat_id
                    msg["_chatType"] = chat.get("chatType", "unknown")
                    msg["_chatTopic"] = chat.get("topic", None)
                    msg["_chatWebUrl"] = chat.get("webUrl", None)
                all_messages.extend(messages)

        artifact["objects"] = {
            "chats": {
                "status": "success",
                "record_count": record_count(active_chats),
                "error": None,
                "data": active_chats,
            },
            "messages": {
                "status": "success",
                "record_count": record_count(all_messages),
                "error": None,
                "data": all_messages,
            },
        }
        artifact["status"] = "success"
        print(f"  [teams] Captured {len(all_messages)} messages across {len(active_chats)} active chats.")

    except Exception as e:
        artifact["status"] = "fail"
        artifact["error"] = {"type": type(e).__name__, "message": str(e), "retryable": False}
        print(f"  [teams] Capture failed: {e}")

    finally:
        write_artifact(artifact, OUTPUT_PATH)
        print(f"  [teams] Wrote → {OUTPUT_PATH}")

    return 0 if artifact["status"] == "success" else 1
