#!/usr/bin/env python3
"""
run_pipeline.py

Orchestrates the full email pipeline: capture → process → summarize → render.

Usage:
  python run_pipeline.py                    # full run
  python run_pipeline.py --from process     # skip capture
  python run_pipeline.py --from summarize   # just re-summarize + render
  python run_pipeline.py --from render      # just re-render the daily note
"""

import argparse
import time


STAGES = ["capture", "process", "summarize", "render"]


def main() -> int:
    p = argparse.ArgumentParser(description="Run email pipeline stages.")
    p.add_argument(
        "--from",
        dest="from_stage",
        choices=STAGES,
        default="capture",
        help="Stage to start from (skips earlier stages)",
    )
    args = p.parse_args()

    start_idx = STAGES.index(args.from_stage)
    stages_to_run = STAGES[start_idx:]

    for stage_name in stages_to_run:
        print(f"\n{'='*60}")
        print(f"  STAGE: {stage_name}")
        print(f"{'='*60}\n")

        t0 = time.time()

        if stage_name == "capture":
            from capture import main as capture_main
            rc = capture_main()
        elif stage_name == "process":
            from process import main as process_main
            rc = process_main()
        elif stage_name == "summarize":
            from summarize import main as summarize_main
            rc = summarize_main()
        elif stage_name == "render":
            from render import main as render_main
            rc = render_main(file_override="auto")
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

