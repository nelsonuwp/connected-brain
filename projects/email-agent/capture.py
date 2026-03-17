#!/usr/bin/env python3
"""
1_capture_emails.py

Fetches emails from Microsoft Graph for a date range.
Writes a SourceArtifact JSON — raw payload, never reshaped.

Output: outputs/source_emails.json

Usage:
  python 1_capture_emails.py
  python 1_capture_emails.py --start-date 2026-03-10 --end-date 2026-03-15
"""

import argparse
import base64
import hashlib
import http.server
import json
import os
import random
import string
import threading
import time
import urllib.parse
import webbrowser
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

# ── Project imports ───────────────────────────────────────────────────────────
import sys
_SCRIPT_DIR = Path(__file__).resolve().parent  # .../projects/email-agent
_REPO_ROOT = _SCRIPT_DIR.parents[2]            # .../connected-brain
# Ensure local project modules (connectors/) are importable even when executed via importlib.
sys.path.insert(0, str(_SCRIPT_DIR))
# Also allow loading shared repo-level modules if needed.
sys.path.insert(0, str(_REPO_ROOT))
from connectors.source_artifact import (
    make_source_artifact, record_count, utc_now, write_artifact
)

OUTPUT_DIR  = Path(__file__).resolve().parent / "outputs"
OUTPUT_PATH = OUTPUT_DIR / "source_emails.json"

# ── Env loading ───────────────────────────────────────────────────────────────

def _strip_optional_quotes(v: str) -> str:
    v = v.strip()
    return v[1:-1] if len(v) >= 2 and v[0] == v[-1] in ('"', "'") else v

def _load_env_file(path: Path) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        if k.startswith("export "):
            k = k[len("export ") :].strip()
        if not k:
            continue
        # Only set if missing OR present-but-empty (common when shells export empty vars).
        if os.environ.get(k) in (None, ""):
            os.environ[k] = _strip_optional_quotes(v.strip())

def load_env() -> None:
    script_dir = Path(__file__).resolve().parent
    repo_root  = script_dir.parents[2]
    _load_env_file(Path.cwd() / ".env")
    _load_env_file(repo_root / ".env")

# ── Date helpers ──────────────────────────────────────────────────────────────

def parse_yyyymmdd(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date '{value}'. Expected YYYY-MM-DD.")

def compute_date_range(start_arg, end_arg) -> Tuple[date, date]:
    today = date.today()
    if start_arg is None and end_arg is None:
        yesterday = today - timedelta(days=1)
        return yesterday, yesterday
    start = parse_yyyymmdd(start_arg) if start_arg else today
    end   = parse_yyyymmdd(end_arg)   if end_arg   else today
    if end < start:
        raise ValueError(f"End date {end} cannot be before start date {start}.")
    return start, end

# ── OAuth / PKCE ──────────────────────────────────────────────────────────────

_auth_code: Optional[str] = None

def _generate_pkce() -> Tuple[str, str]:
    verifier  = "".join(random.choices(string.ascii_letters + string.digits, k=128))
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()
    ).decode().rstrip("=")
    return verifier, challenge

class _OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global _auth_code
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        if parsed.path == "/auth/login/callback" and qs.get("code"):
            _auth_code = qs["code"][0]
            html = "<html><body><h1>Auth successful — close this window.</h1></body></html>"
            self.wfile.write(html.encode("utf-8"))
        else:
            html = "<html><body><h1>Auth failed — no code received.</h1></body></html>"
            self.wfile.write(html.encode("utf-8"))
    def log_message(self, *_): pass

def get_access_token() -> str:
    client_id    = os.getenv("MS_CLIENT_ID")
    tenant_id    = os.getenv("MS_TENANT_ID")
    client_secret= os.getenv("MS_CLIENT_SECRET")
    redirect_uri = os.getenv("MS_REDIRECT_URI", "http://localhost:3000/auth/login/callback")
    if not client_id or not tenant_id:
        raise RuntimeError("MS_CLIENT_ID and MS_TENANT_ID must be set.")

    auth_url  = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    verifier, challenge = _generate_pkce()

    global _auth_code
    _auth_code = None
    params = {
        "client_id": client_id, "response_type": "code",
        "redirect_uri": redirect_uri, "scope": "Mail.Read User.Read",
        "response_mode": "query", "state": "12345",
        "code_challenge": challenge, "code_challenge_method": "S256",
    }
    port   = urllib.parse.urlparse(redirect_uri).port or 3000
    httpd  = http.server.HTTPServer(("localhost", port), _OAuthHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    print("Opening browser for authentication...")
    webbrowser.open(f"{auth_url}?{urllib.parse.urlencode(params)}")
    deadline = time.time() + 300
    while _auth_code is None and time.time() < deadline:
        time.sleep(0.5)
    httpd.shutdown()
    thread.join(timeout=5)
    if not _auth_code:
        raise RuntimeError("Authentication timed out or failed.")

    resp = requests.post(token_url, data={
        "client_id": client_id, "scope": "Mail.Read User.Read",
        "code": _auth_code, "redirect_uri": redirect_uri,
        "grant_type": "authorization_code", "code_verifier": verifier,
        **({"client_secret": client_secret} if client_secret else {}),
    })
    token = resp.json().get("access_token") if resp.status_code == 200 else None
    if not token:
        raise RuntimeError(f"Token exchange failed: {resp.status_code} {resp.text[:200]}")
    return token

# ── Graph fetch ───────────────────────────────────────────────────────────────

def fetch_messages(start: date, end: date, token: str) -> List[Dict[str, Any]]:
    """
    One API call per run — returns up to 1000 messages.
    Graph paginates via @odata.nextLink if >1000; uncomment the loop below
    to handle high-volume days (not needed for typical daily runs).
    """
    user_email = os.getenv("USER_EMAIL") or os.getenv("MS_EMAIL")
    if not user_email:
        raise RuntimeError("USER_EMAIL or MS_EMAIL must be set.")

    url     = f"https://graph.microsoft.com/v1.0/users/{user_email}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    params  = {
        "$select": "id,subject,sentDateTime,body,from,toRecipients,ccRecipients,meetingMessageType",
        "$filter": f"sentDateTime ge {start.isoformat()}T00:00:00Z and sentDateTime le {end.isoformat()}T23:59:59Z",
        "$top":    1000,
    }

    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    messages = data.get("value", [])

    # ── Optional pagination (uncomment for high-volume inboxes) ──────────────
    # while next_link := data.get("@odata.nextLink"):
    #     resp  = requests.get(next_link, headers=headers)
    #     resp.raise_for_status()
    #     data  = resp.json()
    #     messages.extend(data.get("value", []))

    print(f"  Fetched {len(messages)} raw messages from Graph.")
    return messages

# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    load_env()

    parser = argparse.ArgumentParser(description="Capture emails → SourceArtifact JSON.")
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("-o", "--output", default=str(OUTPUT_PATH))
    args = parser.parse_args()

    try:
        start, end = compute_date_range(args.start_date, args.end_date)
    except (argparse.ArgumentTypeError, ValueError) as e:
        print(f"Date error: {e}")
        return 1

    print(f"Capturing emails {start} → {end}")

    artifact = make_source_artifact("microsoft_graph_email")
    # Domain-level extension fields
    artifact["date_range"] = {"start": start.isoformat(), "end": end.isoformat()}
    output_path = Path(args.output)

    try:
        token    = get_access_token()
        messages = fetch_messages(start, end, token)

        artifact["objects"] = {
            "messages": {
                "status":       "success",
                "record_count": record_count(messages),
                "error":        None,
                "data":         messages,
            }
        }
        artifact["status"] = "success"
        print(f"  Captured {len(messages)} messages.")

    except Exception as e:
        artifact["status"] = "fail"
        artifact["error"]  = {"type": type(e).__name__, "message": str(e), "retryable": False}
        print(f"  Capture failed: {e}")

    finally:
        write_artifact(artifact, output_path)
        print(f"  Wrote → {output_path}")

    return 0 if artifact["status"] == "success" else 1

if __name__ == "__main__":
    raise SystemExit(main())