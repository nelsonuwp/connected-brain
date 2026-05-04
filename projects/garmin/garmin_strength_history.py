#!/usr/bin/env python3
"""Export Garmin strength workout history for the last year.

Requirements:
  pip install garminconnect

Environment variables:
  GARMIN_EMAIL       Garmin Connect account email
  GARMIN_PASSWORD    Garmin Connect account password
  GARMIN_TOKEN_PATH  Optional token cache path (default: ~/.garminconnect)
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys
import time
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)


DEFAULT_STRENGTH_TYPE_KEYS = {
    "strength_training",
    "strength",
    "fitness_equipment",
}


def load_dotenv_if_present(path: str = ".env") -> None:
    dotenv_path = Path(path)
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


def is_rate_limited_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return "429" in message or "too many requests" in message


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export Garmin strength workout history for a date range."
    )
    parser.add_argument(
        "--days",
        type=int,
        default=365,
        help="How many days back to fetch (default: 365).",
    )
    parser.add_argument(
        "--json-out",
        default="garmin_strength_history.json",
        help="Path to JSON output file.",
    )
    parser.add_argument(
        "--csv-out",
        default="garmin_strength_history.csv",
        help="Path to CSV output file.",
    )
    parser.add_argument(
        "--type-key",
        action="append",
        dest="type_keys",
        default=[],
        help=(
            "Activity typeKey to include. "
            "Repeat this flag to add more values. "
            "Defaults to strength_training,strength,fitness_equipment."
        ),
    )
    parser.add_argument(
        "--login-retries",
        type=int,
        default=3,
        help="Login retry count for rate limits (default: 3).",
    )
    parser.add_argument(
        "--login-backoff-seconds",
        type=int,
        default=30,
        help="Initial backoff seconds between login retries (default: 30).",
    )
    return parser.parse_args()


def build_client(login_retries: int, login_backoff_seconds: int) -> Garmin:
    email = os.getenv("GARMIN_EMAIL", "").strip()
    password = os.getenv("GARMIN_PASSWORD", "").strip()
    token_path = os.getenv("GARMIN_TOKEN_PATH", "~/.garminconnect")
    expanded_token_path = str(Path(token_path).expanduser())

    # Try token-based login first to avoid frequent credential prompts.
    client = Garmin()
    try:
        client.login(expanded_token_path)
        return client
    except FileNotFoundError:
        pass
    except GarminConnectAuthenticationError:
        # Fall back to credential login and refresh token cache.
        pass

    if not email or not password:
        raise RuntimeError(
            "GARMIN_EMAIL/GARMIN_PASSWORD are required when no valid token cache exists."
        )

    client = Garmin(email=email, password=password)

    attempts = max(1, login_retries)
    for attempt in range(1, attempts + 1):
        try:
            client.login()
            token_dir = Path(expanded_token_path).expanduser()
            token_dir.parent.mkdir(parents=True, exist_ok=True)
            client.garth.dump(str(token_dir))
            return client
        except (
            GarminConnectAuthenticationError,
            GarminConnectConnectionError,
            GarminConnectTooManyRequestsError,
            RuntimeError,
            ValueError,
        ) as exc:
            if not is_rate_limited_error(exc) or attempt >= attempts:
                raise
            delay = max(1, login_backoff_seconds) * (2 ** (attempt - 1))
            print(
                f"Garmin rate limited login (attempt {attempt}/{attempts}). "
                f"Waiting {delay}s before retry...",
                file=sys.stderr,
            )
            time.sleep(delay)

    raise RuntimeError("Unable to log in to Garmin Connect after retries.")


def extract_record(activity: dict[str, Any]) -> dict[str, Any]:
    activity_type = activity.get("activityType") or {}
    return {
        "activityId": activity.get("activityId"),
        "activityName": activity.get("activityName"),
        "typeKey": activity_type.get("typeKey"),
        "startTimeLocal": activity.get("startTimeLocal"),
        "durationSeconds": activity.get("duration"),
        "calories": activity.get("calories"),
        "averageHR": activity.get("averageHR"),
        "maxHR": activity.get("maxHR"),
    }


def main() -> None:
    # Reduce noisy traceback-style logging from underlying libraries.
    logging.getLogger("garminconnect").setLevel(logging.ERROR)
    logging.getLogger("garth").setLevel(logging.ERROR)
    load_dotenv_if_present()

    args = parse_args()

    type_keys = {key.strip().lower() for key in args.type_keys if key.strip()}
    if not type_keys:
        type_keys = set(DEFAULT_STRENGTH_TYPE_KEYS)

    end_date = date.today()
    start_date = end_date - timedelta(days=max(args.days, 1))

    client = build_client(
        login_retries=args.login_retries,
        login_backoff_seconds=args.login_backoff_seconds,
    )
    activities = client.get_activities_by_date(
        startdate=start_date.isoformat(),
        enddate=end_date.isoformat(),
    )

    filtered = []
    for activity in activities:
        type_key = (
            ((activity.get("activityType") or {}).get("typeKey") or "").strip().lower()
        )
        if type_key in type_keys:
            filtered.append(extract_record(activity))

    json_path = Path(args.json_out)
    csv_path = Path(args.csv_out)

    json_path.write_text(json.dumps(filtered, indent=2), encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "activityId",
            "activityName",
            "typeKey",
            "startTimeLocal",
            "durationSeconds",
            "calories",
            "averageHR",
            "maxHR",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered)

    print(
        f"Fetched {len(activities)} activities from {start_date} to {end_date}. "
        f"Strength matches: {len(filtered)}."
    )
    print(f"Wrote: {json_path}")
    print(f"Wrote: {csv_path}")


if __name__ == "__main__":
    try:
        main()
    except (
        GarminConnectAuthenticationError,
        GarminConnectConnectionError,
        GarminConnectTooManyRequestsError,
        RuntimeError,
        ValueError,
    ) as exc:
        if is_rate_limited_error(exc):
            print(
                "Error: Garmin login is currently rate-limited (429). "
                "Wait 15-60 minutes and retry.",
                file=sys.stderr,
            )
        else:
            print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
