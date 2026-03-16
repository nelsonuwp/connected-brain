#!/usr/bin/env python3
import argparse
import os
from datetime import datetime, date, timedelta
import json
import requests


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


def get_access_token() -> str:
    """
    Placeholder for auth – wire this up to your real Email Agent auth flow.
    For now, expects ACCESS_TOKEN in the environment.
    """
    token = os.getenv("ACCESS_TOKEN")
    if not token:
        raise RuntimeError("ACCESS_TOKEN environment variable must be set.")
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

