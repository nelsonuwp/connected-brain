#!/usr/bin/env python3
"""Daily Garmin health snapshot — sleep, body battery, training readiness, strength workouts.

Requirements:
  pip install garminconnect

Environment variables (loaded from /Users/anelson-macbook-air/connected-brain/.env):
  GARMIN_EMAIL       Garmin Connect account email
  GARMIN_PASSWORD    Garmin Connect account password
  GARMIN_TOKEN_PATH  Token cache path (default: ~/.garminconnect)
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

DEFAULT_ENV_PATH = "/Users/anelson-macbook-air/connected-brain/.env"
DEFAULT_STRENGTH_TYPE_KEYS = {"strength_training", "strength", "fitness_equipment"}


def load_dotenv_if_present(path: str = DEFAULT_ENV_PATH) -> None:
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
        description="Export daily Garmin health snapshot as LLM-optimized markdown."
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Target date in YYYY-MM-DD format (default: today).",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=1,
        help="Number of days ending on --date to include (default: 1).",
    )
    parser.add_argument(
        "--out-dir",
        default=".",
        help="Output directory for markdown files (default: current directory).",
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

    def _mfa_prompt() -> str:
        return input("Garmin MFA code: ").strip()

    def _save_tokens(c: Garmin, path: str) -> None:
        token_dir = Path(path).expanduser()
        token_dir.parent.mkdir(parents=True, exist_ok=True)
        dumper = getattr(c, "garth", None) or getattr(c, "client", None)
        if dumper:
            dumper.dump(str(token_dir))

    # Try cached tokens first.
    client = Garmin(email=email, password=password, prompt_mfa=_mfa_prompt)
    try:
        client.login(expanded_token_path)
        return client
    except FileNotFoundError:
        pass
    except (GarminConnectAuthenticationError, Exception):
        # Stale or incompatible token cache — fall through to full login.
        pass

    if not email or not password:
        raise RuntimeError(
            "GARMIN_EMAIL/GARMIN_PASSWORD are required when no valid token cache exists."
        )

    attempts = max(1, login_retries)
    for attempt in range(1, attempts + 1):
        try:
            client.login()
            _save_tokens(client, expanded_token_path)
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


def _safe(fn, *args, **kwargs) -> Any:
    try:
        return fn(*args, **kwargs)
    except Exception as exc:
        print(f"  [warning] {fn.__name__} failed: {exc}", file=sys.stderr)
        return None


def seconds_to_hm(seconds: Any) -> str:
    if seconds is None:
        return "N/A"
    try:
        s = int(seconds)
        h = s // 3600
        m = (s % 3600) // 60
        return f"{h}h {m:02d}m"
    except (TypeError, ValueError):
        return "N/A"


def fmt(value: Any, suffix: str = "") -> str:
    if value is None:
        return "N/A"
    return f"{value}{suffix}"


def build_sleep_section(client: Garmin, date_str: str) -> str:
    raw = _safe(client.get_sleep_data, date_str)
    lines = ["### Sleep"]
    if not raw:
        lines += [
            "- Sleep Score: N/A",
            "- Duration: N/A",
            "- Light Sleep: N/A",
            "- Deep Sleep: N/A",
            "- REM Sleep: N/A",
            "- Awake: N/A",
        ]
        return "\n".join(lines)

    dto = raw.get("dailySleepDTO") or {}
    score_block = dto.get("sleepScores") or {}
    overall = score_block.get("overall") or {}
    score_val = overall.get("value") if isinstance(overall, dict) else None
    # Some API versions put score directly on the sleepScores dict
    if score_val is None and isinstance(score_block, dict):
        score_val = score_block.get("value")

    lines += [
        f"- Sleep Score: {fmt(score_val, '/100')}",
        f"- Duration: {seconds_to_hm(dto.get('sleepTimeSeconds'))}",
        f"- Light Sleep: {seconds_to_hm(dto.get('lightSleepSeconds'))}",
        f"- Deep Sleep: {seconds_to_hm(dto.get('deepSleepSeconds'))}",
        f"- REM Sleep: {seconds_to_hm(dto.get('remSleepSeconds'))}",
        f"- Awake: {seconds_to_hm(dto.get('awakeSleepSeconds'))}",
    ]
    return "\n".join(lines)


def build_body_battery_section(client: Garmin, date_str: str) -> str:
    raw = _safe(client.get_body_battery, date_str, date_str)
    lines = ["### Body Battery"]
    if not raw or not isinstance(raw, list):
        lines += [
            "- Start of Day: N/A",
            "- End of Day: N/A",
            "- Lowest Point: N/A",
        ]
        return "\n".join(lines)

    entry = raw[0] if isinstance(raw[0], dict) else {}
    stat_list = entry.get("bodyBatteryStatList") or []
    values = [
        s.get("bodyBatteryValue")
        for s in stat_list
        if s.get("bodyBatteryValue") is not None
    ]

    start_val = values[0] if values else None
    end_val = values[-1] if values else None
    low_val = min(values) if values else None

    lines += [
        f"- Start of Day: {fmt(start_val)}",
        f"- End of Day: {fmt(end_val)}",
        f"- Lowest Point: {fmt(low_val)}",
    ]
    return "\n".join(lines)


def build_training_readiness_section(client: Garmin, date_str: str) -> str:
    raw = _safe(client.get_training_readiness, date_str)
    lines = ["### Training Readiness"]
    if not raw:
        lines += [
            "- Score: N/A",
            "- Level: N/A",
            "- Key Factors: N/A",
        ]
        return "\n".join(lines)

    entry = raw[0] if isinstance(raw, list) and raw else (raw if isinstance(raw, dict) else {})
    score = entry.get("score") or entry.get("trainingReadinessScore")
    level = entry.get("levelCode") or entry.get("level") or entry.get("trainingReadinessLevel")

    factors_raw = entry.get("contributors") or entry.get("factorList") or []
    factor_names = []
    for f in factors_raw[:3]:
        name = f.get("factorCode") or f.get("name") or f.get("type")
        if name:
            factor_names.append(str(name).replace("_", " ").title())

    lines += [
        f"- Score: {fmt(score, '/100')}",
        f"- Level: {fmt(level)}",
        f"- Key Factors: {', '.join(factor_names) if factor_names else 'N/A'}",
    ]
    return "\n".join(lines)


def _grams_to_lbs(grams: Any) -> str:
    if grams is None:
        return "N/A"
    try:
        return f"{round(int(grams) / 1000 * 2.20462, 1)} lbs"
    except (TypeError, ValueError):
        return "N/A"


def build_strength_section(client: Garmin, date_str: str) -> str:
    lines = ["### Strength Training"]

    activities_raw = _safe(client.get_activities_by_date, date_str, date_str)
    if not activities_raw:
        lines.append("No strength workouts recorded.")
        return "\n".join(lines)

    strength_activities = [
        a for a in activities_raw
        if ((a.get("activityType") or {}).get("typeKey") or "").strip().lower()
        in DEFAULT_STRENGTH_TYPE_KEYS
    ]

    if not strength_activities:
        lines.append("No strength workouts recorded.")
        return "\n".join(lines)

    for activity in strength_activities:
        activity_id = activity.get("activityId")
        name = activity.get("activityName") or "Strength Workout"
        start_time = activity.get("startTimeLocal") or "N/A"
        duration_str = seconds_to_hm(activity.get("duration"))
        calories = fmt(activity.get("calories"))
        avg_hr = fmt(activity.get("averageHR"), " bpm")
        max_hr = fmt(activity.get("maxHR"), " bpm")

        lines += [
            "",
            f"**{name}**",
            f"- Start: {start_time}",
            f"- Duration: {duration_str}",
            f"- Calories: {calories}",
            f"- Avg HR: {avg_hr}",
            f"- Max HR: {max_hr}",
        ]

        if activity_id:
            sets_raw = _safe(client.get_activity_exercise_sets, activity_id)
            if sets_raw:
                exercise_sets = sets_raw.get("exerciseSets") or []
                exercises: dict[str, list[dict]] = {}
                for s in exercise_sets:
                    if s.get("setType") != "ACTIVE":
                        continue
                    ex_list = s.get("exercises") or []
                    ex_name = "Unknown"
                    if ex_list:
                        ex = ex_list[0]
                        ex_name = (
                            ex.get("name") or ex.get("category") or "Unknown"
                        ).replace("_", " ").title()
                    exercises.setdefault(ex_name, []).append(s)

                if exercises:
                    lines += ["", "| Exercise | Sets | Reps | Weight |", "|----------|------|------|--------|"]
                    for ex_name, ex_sets in exercises.items():
                        num_sets = len(ex_sets)
                        reps_list = [s["repetitionCount"] for s in ex_sets if s.get("repetitionCount")]
                        weight_list = [s["weight"] for s in ex_sets if s.get("weight")]

                        if reps_list:
                            unique_reps = set(reps_list)
                            reps_str = str(reps_list[0]) if len(unique_reps) == 1 else f"{min(reps_list)}-{max(reps_list)}"
                        else:
                            reps_str = "N/A"

                        if weight_list:
                            unique_w = set(weight_list)
                            if len(unique_w) == 1:
                                weight_str = _grams_to_lbs(weight_list[0])
                            else:
                                weight_str = f"{_grams_to_lbs(min(weight_list))}-{_grams_to_lbs(max(weight_list))}"
                        else:
                            weight_str = "N/A"

                        lines.append(f"| {ex_name} | {num_sets} | {reps_str} | {weight_str} |")

    return "\n".join(lines)


def build_day_section(client: Garmin, target_date: date) -> str:
    date_str = target_date.isoformat()
    return "\n".join([
        f"## {date_str}",
        "",
        build_sleep_section(client, date_str),
        "",
        build_body_battery_section(client, date_str),
        "",
        build_training_readiness_section(client, date_str),
        "",
        build_strength_section(client, date_str),
    ])


def main() -> None:
    logging.getLogger("garminconnect").setLevel(logging.ERROR)
    logging.getLogger("garth").setLevel(logging.ERROR)
    load_dotenv_if_present()

    args = parse_args()

    end_date = date.fromisoformat(args.date)
    days = max(1, args.days)
    start_date = end_date - timedelta(days=days - 1)
    date_range = [start_date + timedelta(days=i) for i in range(days)]

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if days == 1:
        filename = f"garmin_{end_date.isoformat()}.md"
    else:
        filename = f"garmin_{start_date.isoformat()}_to_{end_date.isoformat()}.md"

    out_path = out_dir / filename

    client = build_client(
        login_retries=args.login_retries,
        login_backoff_seconds=args.login_backoff_seconds,
    )

    generated_ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    date_range_str = (
        end_date.isoformat() if days == 1
        else f"{start_date.isoformat()} to {end_date.isoformat()}"
    )

    output_lines = [f"<!-- garmin snapshot: {date_range_str}, generated: {generated_ts} -->", ""]
    for d in date_range:
        output_lines.append(build_day_section(client, d))
        output_lines.append("")

    out_path.write_text("\n".join(output_lines), encoding="utf-8")
    print(f"Wrote: {out_path}")


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
