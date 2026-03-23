"""
ingestors/_ms_auth.py
---------------------
Shared Microsoft Graph OAuth + PKCE authentication.

Used by both email.py and teams.py ingestors.
Caches the access token for the duration of a pipeline run so we only
authenticate once even when fetching both email and Teams.
"""

import base64
import hashlib
import http.server
import os
import random
import string
import subprocess
import sys
import threading
import time
import urllib.parse
import webbrowser
from typing import Optional, Tuple

import requests

# ── Token cache (process-lifetime) ───────────────────────────────────────────
_cached_token: Optional[str] = None

# ── Required scopes ──────────────────────────────────────────────────────────
# Email: Mail.Read
# Teams: Chat.Read, Chat.ReadBasic
# Both:  User.Read
ALL_SCOPES = "Mail.Read Chat.Read Chat.ReadBasic User.Read"

# ── OAuth / PKCE ──────────────────────────────────────────────────────────────

_auth_code: Optional[str] = None


def _generate_pkce() -> Tuple[str, str]:
    verifier = "".join(random.choices(string.ascii_letters + string.digits, k=128))
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()
    ).decode().rstrip("=")
    return verifier, challenge


class _OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global _auth_code
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/auth/login/callback" and "code=" in parsed.query:
            _auth_code = urllib.parse.parse_qs(parsed.query).get("code", [None])[0]
            self.wfile.write(b"<html><body><h1>Auth successful - close this window.</h1></body></html>")
        else:
            self.wfile.write(b"<html><body><h1>Auth failed - no code received.</h1></body></html>")

    def log_message(self, *_):
        pass


def _open_auth_url(url: str) -> None:
    print("Opening browser for authentication...")
    print(f"If it does not open automatically, paste this URL:\n{url}")
    try:
        if webbrowser.open(url):
            return
    except Exception:
        pass
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", url], check=False)
        elif sys.platform.startswith("linux"):
            subprocess.run(["xdg-open", url], check=False)
        elif os.name == "nt":
            subprocess.run(["cmd", "/c", "start", "", url], check=False)
    except Exception:
        pass


def get_access_token(force_refresh: bool = False) -> str:
    """
    Get an MS Graph access token. Caches for the process lifetime.
    Both email and teams ingestors call this — only authenticates once.
    """
    global _cached_token, _auth_code

    if _cached_token and not force_refresh:
        return _cached_token

    client_id = os.getenv("MS_CLIENT_ID")
    tenant_id = os.getenv("MS_TENANT_ID")
    client_secret = os.getenv("MS_CLIENT_SECRET")
    redirect_uri = os.getenv("MS_REDIRECT_URI", "http://localhost:3000/auth/login/callback")

    if not client_id or not tenant_id:
        raise RuntimeError("MS_CLIENT_ID and MS_TENANT_ID must be set.")

    auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    verifier, challenge = _generate_pkce()

    _auth_code = None
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": ALL_SCOPES,
        "response_mode": "query",
        "state": "12345",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }

    port = urllib.parse.urlparse(redirect_uri).port or 3000
    httpd = http.server.HTTPServer(("localhost", port), _OAuthHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    full_auth_url = f"{auth_url}?{urllib.parse.urlencode(params)}"
    _open_auth_url(full_auth_url)

    deadline = time.time() + 300
    while _auth_code is None and time.time() < deadline:
        time.sleep(0.5)
    httpd.shutdown()
    thread.join(timeout=5)

    if not _auth_code:
        raise RuntimeError("Authentication timed out or failed.")

    resp = requests.post(token_url, data={
        "client_id": client_id,
        "scope": ALL_SCOPES,
        "code": _auth_code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        "code_verifier": verifier,
        **({"client_secret": client_secret} if client_secret else {}),
    })

    token = resp.json().get("access_token") if resp.status_code == 200 else None
    if not token:
        raise RuntimeError(f"Token exchange failed: {resp.status_code} {resp.text[:200]}")

    _cached_token = token
    return token
