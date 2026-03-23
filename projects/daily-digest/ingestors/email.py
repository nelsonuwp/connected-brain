#!/usr/bin/env python3
"""
ingestors/email.py
------------------
Fetches emails from Microsoft Graph for a date range.
Writes a SourceArtifact JSON — raw payload, never reshaped.

Output: outputs/source_email.json
"""

import os
from datetime import date
from pathlib import Path
from typing import Any, Dict, List

import requests

from ._ms_auth import get_access_token

# Lazy import — connectors are at the project level
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from connectors.source_artifact import (
    make_source_artifact, record_count, write_artifact
)

OUTPUT_DIR  = Path(__file__).resolve().parents[1] / "outputs"
OUTPUT_PATH = OUTPUT_DIR / "source_email.json"


def fetch_messages(start: date, end: date, token: str) -> List[Dict[str, Any]]:
    """
    Fetch emails from MS Graph. Returns up to 1000 messages.
    """
    user_email = os.getenv("DIGEST_USER_EMAIL") or os.getenv("MS_EMAIL")
    if not user_email:
        raise RuntimeError("DIGEST_USER_EMAIL or MS_EMAIL must be set.")

    url = f"https://graph.microsoft.com/v1.0/users/{user_email}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    params = {
        "$select": "id,subject,sentDateTime,body,from,toRecipients,ccRecipients,webLink,hasAttachments,conversationId",
        "$filter": (
            f"sentDateTime ge {start.isoformat()}T00:00:00Z "
            f"and sentDateTime le {end.isoformat()}T23:59:59Z"
        ),
        "$top": 1000,
    }

    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    messages = data.get("value", [])

    # Optional pagination for high-volume inboxes
    while next_link := data.get("@odata.nextLink"):
        resp = requests.get(next_link, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        messages.extend(data.get("value", []))

    print(f"  [email] Fetched {len(messages)} messages from Graph.")
    return messages


def main(start: date, end: date) -> int:
    """
    Called by run_pipeline.py with explicit date range.
    """
    print(f"  [email] Capturing emails {start} → {end}")

    artifact = make_source_artifact("email")
    artifact["date_range"] = {"start": start.isoformat(), "end": end.isoformat()}

    try:
        token = get_access_token()
        messages = fetch_messages(start, end, token)

        artifact["objects"] = {
            "messages": {
                "status": "success",
                "record_count": record_count(messages),
                "error": None,
                "data": messages,
            }
        }
        artifact["status"] = "success"
        print(f"  [email] Captured {len(messages)} messages.")

    except Exception as e:
        artifact["status"] = "fail"
        artifact["error"] = {"type": type(e).__name__, "message": str(e), "retryable": False}
        print(f"  [email] Capture failed: {e}")

    finally:
        write_artifact(artifact, OUTPUT_PATH)
        print(f"  [email] Wrote → {OUTPUT_PATH}")

    return 0 if artifact["status"] == "success" else 1
