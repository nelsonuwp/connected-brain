#!/usr/bin/env python3
"""
run_pipeline.py

Orchestrates the full email pipeline: capture → process → summarize → render.

The --date flag drives everything:
  - Determines which daily note to render into (vault/00-daily/{date}.md)
  - Derives the email fetch range: previous business day through yesterday
    Monday  → fetches Fri + Sat + Sun
    Tuesday → fetches Mon
    Wednesday → fetches Tue
    ...

Usage:
  python run_pipeline.py                    # today's note, yesterday's emails
  python run_pipeline.py --date 2026-03-17  # specific note date
  python run_pipeline.py --from process     # skip capture, reuse existing fetch
  python run_pipeline.py --from render      # just re-render the daily note
"""

import argparse
import os
import time
from datetime import date, datetime, timedelta
from pathlib import Path


STAGES = ["capture", "process", "summarize", "render"]


def _parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date '{value}'. Expected YYYY-MM-DD.")


def email_range_for(note_date: date) -> tuple:
    """
    Derive the email fetch window from the note date.

    Start = most recent business day before note_date (inclusive of yesterday).
    End   = yesterday (note_date - 1).

    Examples (note_date → start, end):
      Monday    2026-03-17 → Friday    2026-03-14, Sunday   2026-03-16
      Tuesday   2026-03-18 → Monday    2026-03-17, Monday   2026-03-17
      Wednesday 2026-03-19 → Tuesday   2026-03-18, Tuesday  2026-03-18
    """
    yesterday = note_date - timedelta(days=1)
    # Walk back from yesterday to find the most recent business day
    start = yesterday
    while start.weekday() >= 5:  # Saturday=5, Sunday=6
        start -= timedelta(days=1)
    return start, yesterday


def _resolve_note_path(note_date: date) -> Path:
    """Resolve the daily note path from the note date."""
    script_dir = Path(__file__).resolve().parent
    default_vault = script_dir.parents[1] / "vault"
    vault = Path(os.getenv("VAULT_PATH", str(default_vault)))
    return vault / "00-daily" / f"{note_date.isoformat()}.md"


def main() -> int:
    p = argparse.ArgumentParser(description="Run email pipeline stages.")
    p.add_argument(
        "--date",
        type=_parse_date,
        default=date.today(),
        help="Note date (default: today). Emails fetched from previous business day through yesterday.",
    )
    p.add_argument(
        "--from",
        dest="from_stage",
        choices=STAGES,
        default="capture",
        help="Stage to start from (skips earlier stages)",
    )
    args = p.parse_args()

    note_date = args.date
    email_start, email_end = email_range_for(note_date)
    note_path = _resolve_note_path(note_date)

    print(f"  Note date:   {note_date} ({note_date.strftime('%A')})")
    print(f"  Email range: {email_start} → {email_end}")
    print(f"  Daily note:  {note_path}")

    start_idx = STAGES.index(args.from_stage)
    stages_to_run = STAGES[start_idx:]

    for stage_name in stages_to_run:
        print(f"\n{'='*60}")
        print(f"  STAGE: {stage_name}")
        print(f"{'='*60}\n")

        t0 = time.time()

        if stage_name == "capture":
            from capture import main as capture_main
            rc = capture_main(
                start_date_override=email_start.isoformat(),
                end_date_override=email_end.isoformat(),
            )
        elif stage_name == "process":
            from process import main as process_main
            rc = process_main()
        elif stage_name == "summarize":
            from summarize import main as summarize_main
            rc = summarize_main()
        elif stage_name == "render":
            from render import main as render_main
            rc = render_main(file_override=str(note_path))
        else:
            print(f"  Unknown stage: {stage_name}")
            return 1

        elapsed = time.time() - t0
        print(f"\n  {stage_name} finished in {elapsed:.1f}s (exit code {rc})")

        if rc != 0:
            print(f"\n  Pipeline stopped: {stage_name} failed with exit code {rc}")
            return rc

    print(f"\n{'='*60}")
    print("  Pipeline complete")
    print(f"{'='*60}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())