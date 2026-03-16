#!/usr/bin/env python3
import argparse
import os
from datetime import datetime, date, timedelta
import json
import requests
import webbrowser
import http.server
import threading
import urllib.parse
import time
import random
import string
import base64
import hashlib


def parse_yyyymmdd(value: str) -> date:
    """Parse a YYYY-MM-DD string into a date, raising argparse error on failure."""
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid date '{value}'. Expected format: YYYY-MM-DD (e.g. 2026-03-10)."
        )


def compute_date_range(start_arg: str | None, end_arg: str | None) -> tuple[date, date]:
    """
    Decide start/end dates based on CLI args.

    Rules:
    - If both are omitted: default to yesterday (start=end=yesterday).
    - Otherwise:
      - Any missing boundary defaults to today.
    """
    today = date.today()

    if start_arg is None and end_arg is None:
        yesterday = today - timedelta(days=1)
        return yesterday, yesterday

    start = parse_yyyymmdd(start_arg) if start_arg is not None else today
    end = parse_yyyymmdd(end_arg) if end_arg is not None else today

    if end < start:
        raise ValueError(
            f"End date {end.isoformat()} cannot be before start date {start.isoformat()}."
        )

    return start, end


def get_user_email() -> str:
    user_email = os.getenv("USER_EMAIL") or os.getenv("MS_EMAIL")
    if not user_email:
        raise RuntimeError("USER_EMAIL or MS_EMAIL environment variable must be set.")
    return user_email


_auth_code: str | None = None


def _generate_pkce() -> tuple[str, str]:
    code_verifier = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(128)
    )
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode("utf-8")).digest()
    ).decode("utf-8")
    code_challenge = code_challenge.replace("=", "")
    return code_verifier, code_challenge


class _OAuthRedirectHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 (BaseHTTPRequestHandler convention)
        global _auth_code
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/auth/login/callback" and "code=" in parsed_path.query:
            query_components = urllib.parse.parse_qs(parsed_path.query)
            _auth_code = query_components.get("code", [None])[0]
            self.wfile.write(
                b"<html><body><h1>Authentication successful!</h1>"
                b"<p>You can close this window now.</p></body></html>"
            )
        else:
            self.wfile.write(
                b"<html><body><h1>Authentication failed!</h1>"
                b"<p>No authorization code received.</p></body></html>"
            )

    def log_message(self, format, *args):  # noqa: A002 (shadowing built-in)
        return


def _get_auth_code(
    *,
    auth_url: str,
    client_id: str,
    redirect_uri: str,
    code_challenge: str,
) -> str | None:
    global _auth_code
    _auth_code = None

    scope = "Mail.Read User.Read"
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope,
        "response_mode": "query",
        "state": "12345",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    auth_request_url = f"{auth_url}?{urllib.parse.urlencode(params)}"

    server_address = ("localhost", 3000)
    httpd = http.server.HTTPServer(server_address, _OAuthRedirectHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    print(f"Opening browser for authentication...")
    webbrowser.open(auth_request_url)

    timeout_s = 300
    start_time = time.time()
    while _auth_code is None:
        if time.time() - start_time > timeout_s:
            print("Authentication timed out.")
            break
        time.sleep(0.5)

    httpd.shutdown()
    server_thread.join(timeout=5)
    return _auth_code


def _exchange_code_for_token(
    *,
    token_url: str,
    client_id: str,
    client_secret: str | None,
    redirect_uri: str,
    code: str,
    code_verifier: str,
) -> str | None:
    token_data = {
        "client_id": client_id,
        "scope": "Mail.Read User.Read",
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
    }
    if client_secret:
        token_data["client_secret"] = client_secret

    resp = requests.post(token_url, data=token_data)
    if resp.status_code == 200:
        return resp.json().get("access_token")

    print(f"Error getting token: {resp.status_code} - {resp.text}")
    return None


def get_access_token() -> str:
    client_id = os.getenv("MS_CLIENT_ID")
    tenant_id = os.getenv("MS_TENANT_ID")
    client_secret = os.getenv("MS_CLIENT_SECRET")
    redirect_uri = os.getenv("MS_REDIRECT_URI") or "http://localhost:3000/auth/login/callback"

    if not client_id or not tenant_id:
        raise RuntimeError("MS_CLIENT_ID and MS_TENANT_ID must be set.")

    auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    code_verifier, code_challenge = _generate_pkce()
    code = _get_auth_code(
        auth_url=auth_url,
        client_id=client_id,
        redirect_uri=redirect_uri,
        code_challenge=code_challenge,
    )
    if not code:
        raise RuntimeError("Failed to get authorization code.")

    token = _exchange_code_for_token(
        token_url=token_url,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        code=code,
        code_verifier=code_verifier,
    )
    if not token:
        raise RuntimeError("Failed to get access token.")
    return token


def fetch_messages_for_range(
    start_date: date,
    end_date: date,
    access_token: str,
) -> list[dict]:
    """
    Fetch messages from Microsoft Graph for an inclusive date range [start_date, end_date].
    Uses sentDateTime filter with UTC midnights.
    """
    user_email = get_user_email()

    start_str = start_date.isoformat()
    # end of the end_date day
    end_str = end_date.isoformat()
    start_of_range = f"{start_str}T00:00:00Z"
    end_of_range = f"{end_str}T23:59:59Z"

    url = f"https://graph.microsoft.com/v1.0/users/{user_email}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    params = {
        "$select": "id,subject,sentDateTime,body,from,toRecipients,ccRecipients",
        "$filter": (
            f"sentDateTime ge {start_of_range} and "
            f"sentDateTime le {end_of_range}"
        ),
        "$top": 1000,
    }

    try:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data.get("value", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching messages from Graph API: {e}")
        try:
            print("Error details:")
            print(json.dumps(resp.json(), indent=2))
        except Exception:
            # best-effort; response body may not be JSON
            pass
        return []


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Capture emails from Microsoft Graph for a date range.\n\n"
            "- Default: yesterday only\n"
            "- Dates are inclusive and must be in YYYY-MM-DD format."
        )
    )
    parser.add_argument(
        "--start-date",
        help="Start date (YYYY-MM-DD). Defaults to today if only end-date is provided.",
    )
    parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD). Defaults to today if only start-date is provided.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="emails_capture.json",
        help="Output JSON file for captured emails (default: emails_capture.json).",
    )

    args = parser.parse_args()

    try:
        start, end = compute_date_range(args.start_date, args.end_date)
    except (argparse.ArgumentTypeError, ValueError) as e:
        print(f"Date error: {e}")
        return 1

    print(f"Capturing emails from {start.isoformat()} to {end.isoformat()} (inclusive)")

    try:
        token = get_access_token()
    except RuntimeError as e:
        print(f"Auth error: {e}")
        return 1

    messages = fetch_messages_for_range(start, end, token)
    print(f"Fetched {len(messages)} messages.")

    try:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        print(f"Wrote messages to {args.output}")
    except OSError as e:
        print(f"Failed to write output file {args.output}: {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

