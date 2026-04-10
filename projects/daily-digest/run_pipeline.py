#!/usr/bin/env python3
"""
run_pipeline.py
---------------
Orchestrates the daily digest pipeline:

  ingest (email, teams, slack) → normalize → process → summarize → render

The --date flag drives everything:
  - Determines which daily note to render into
  - Derives the email/message fetch range (previous business day through yesterday)

Usage:
  python run_pipeline.py                    # today's note, yesterday's messages
  python run_pipeline.py --date 2026-03-17  # specific note date
  python run_pipeline.py --from normalize   # skip ingest, reuse existing captures
  python run_pipeline.py --from summarize   # just re-run LLM + render
  python run_pipeline.py --sources email,teams  # only ingest specific sources
"""

import argparse
import os
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path


STAGES = ["ingest", "normalize", "process", "summarize", "render"]

# Sources to ingest. Each maps to an ingestor module.
INGESTORS = {
    "email": "ingestors.email",
    "teams": "ingestors.teams",
    "slack": "ingestors.slack",
    "calendar": "ingestors.calendar",
}


def _parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date '{value}'. Expected YYYY-MM-DD.")


def message_range_for(note_date: date) -> tuple:
    """
    Derive the message fetch window from the note date.

    Start = most recent business day before note_date.
    End   = yesterday (note_date - 1).

    Monday    → fetches Fri + Sat + Sun
    Tuesday   → fetches Mon
    Wednesday → fetches Tue
    """
    yesterday = note_date - timedelta(days=1)
    start = yesterday
    while start.weekday() >= 5:  # Saturday=5, Sunday=6
        start -= timedelta(days=1)
    return start, yesterday


def _resolve_note_path(note_date: date) -> Path:
    script_dir = Path(__file__).resolve().parent
    default_vault = script_dir.parents[1] / "vault"
    vault = Path(os.getenv("VAULT_PATH", str(default_vault)))
    month_folder = note_date.strftime("%m-%b")
    return vault / "00-daily" / str(note_date.year) / month_folder / f"{note_date.isoformat()}.md"


def _load_env():
    """Load .env from repo root and project dir."""
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parents[1]
    for env_path in [repo_root / ".env", script_dir / ".env"]:
        if env_path.exists():
            try:
                for line in env_path.read_text().splitlines():
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k and k not in os.environ:
                        os.environ[k] = v
            except Exception:
                pass


def main() -> int:
    _load_env()

    p = argparse.ArgumentParser(description="Run daily digest pipeline.")
    p.add_argument("--date", type=_parse_date, default=date.today(),
                   help="Note date (default: today).")
    p.add_argument("--from", dest="from_stage", choices=STAGES, default="ingest",
                   help="Stage to start from (skips earlier stages).")
    p.add_argument("--sources", default=None,
                   help="Comma-separated sources to ingest (default: all). e.g. email,teams")
    p.add_argument("--mode", choices=["full", "digest", "calendar"], default="full",
                   help="Pipeline mode: 'full' (default), 'digest' (messages only), 'calendar' (schedule only).")
    args = p.parse_args()

    note_date = args.date
    msg_start, msg_end = message_range_for(note_date)
    note_path = _resolve_note_path(note_date)

    # Determine which sources to ingest
    if args.sources:
        source_list = [s.strip() for s in args.sources.split(",")]
    elif args.mode == "digest":
        source_list = [s for s in INGESTORS.keys() if s != "calendar"]
    elif args.mode == "calendar":
        source_list = ["calendar"]
    else:
        source_list = list(INGESTORS.keys())

    print(f"  Note date:     {note_date} ({note_date.strftime('%A')})")
    print(f"  Message range: {msg_start} → {msg_end}")
    print(f"  Daily note:    {note_path}")
    print(f"  Sources:       {', '.join(source_list)}")

    start_idx = STAGES.index(args.from_stage)
    all_stages = STAGES[start_idx:]
    if args.mode == "calendar":
        # Calendar mode only needs ingestion + schedule render.
        stages_to_run = [s for s in all_stages if s in ("ingest", "render")]
    else:
        stages_to_run = all_stages

    saved_argv = sys.argv
    pipeline_start = time.time()

    for stage_name in stages_to_run:
        print(f"\n{'='*60}")
        print(f"  STAGE: {stage_name}")
        print(f"{'='*60}\n")

        sys.argv = [stage_name + ".py"]
        t0 = time.time()

        if stage_name == "ingest":
            rc = _run_ingest(source_list, msg_start, msg_end, note_date)

        elif stage_name == "normalize":
            from normalize import main as normalize_main
            rc = normalize_main()

        elif stage_name == "process":
            from process import main as process_main
            rc = process_main()

        elif stage_name == "summarize":
            from summarize import main as summarize_main
            rc = summarize_main()

        elif stage_name == "render":
            from render import main as render_main
            rc = render_main(note_date=note_date, mode=args.mode)

        else:
            print(f"  Unknown stage: {stage_name}")
            sys.argv = saved_argv
            return 1

        elapsed = time.time() - t0
        print(f"\n  {stage_name} finished in {elapsed:.1f}s (exit code {rc})")

        if rc != 0:
            print(f"\n  Pipeline stopped: {stage_name} failed with exit code {rc}")
            sys.argv = saved_argv
            return rc

    sys.argv = saved_argv
    total = time.time() - pipeline_start

    print(f"\n{'='*60}")
    print(f"  Pipeline complete in {total:.1f}s")
    print(f"{'='*60}")
    return 0


def _run_ingest(sources: list, start: date, end: date, note_date: date) -> int:
    """
    Run all configured ingestors. Fails immediately if any source fails.
    """
    for source_name in sources:
        if source_name not in INGESTORS:
            print(f"  [ingest] Unknown source: {source_name}, skipping.")
            continue

        print(f"\n  --- Ingesting: {source_name} ---")
        try:
            if source_name == "email":
                from ingestors.email import main as ingest_email
                rc = ingest_email(start, end)
            elif source_name == "teams":
                from ingestors.teams import main as ingest_teams
                rc = ingest_teams(start, end)
            elif source_name == "slack":
                from ingestors.slack import main as ingest_slack
                rc = ingest_slack(start, end)
            elif source_name == "calendar":
                from ingestors.calendar import main as ingest_calendar
                rc = ingest_calendar(note_date)
            else:
                rc = 1
        except Exception as e:
            print(f"\n  [ingest] CRITICAL: {source_name} raised an unexpected error: {type(e).__name__}: {e}")
            return 1

        if rc != 0:
            print(f"\n  [ingest] CRITICAL: {source_name} failed.")
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
