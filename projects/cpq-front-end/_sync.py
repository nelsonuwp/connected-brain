#!/usr/bin/env python3
"""
_sync.py — bidirectional sync between dev workspace and git repo

Workspace : ~/connected-brain/projects/cpq-front-end  (here, dev in Claude)
Git repo  : ~/Code/cpq-front-end                       (git remote on sgit)

Any file/dir prefixed with _ stays in the workspace only (never synced to /Code or git).

Usage:
  python _sync.py push "commit message"   # workspace → git repo → remote
  python _sync.py pull                    # remote → git repo → workspace
  python _sync.py status                  # diff workspace vs git repo (dry-run)
"""

import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).parent.resolve()
REPO      = Path.home() / "Code" / "cpq-front-end"

# Files/dirs excluded from rsync in both directions.
# Anything prefixed with _ stays in the workspace only (never synced to /Code or git).
EXCLUDES = [
    "_*",           # workspace-only files (this script, scratch notes, etc.)
    "__pycache__/",
    "*.pyc",
    ".DS_Store",
    ".env.local",   # personal secrets — never committed, never synced
    ".git/",
]

_EXCLUDE_ARGS = [arg for ex in EXCLUDES for arg in ("--exclude", ex)]


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    return subprocess.run(cmd, cwd=cwd, check=check)


def rsync(src: Path, dst: Path, delete: bool = True, dry_run: bool = False) -> subprocess.CompletedProcess:
    """rsync src/ → dst/ with standard excludes."""
    flags = ["-av", "--delete"] if delete else ["-av"]
    if dry_run:
        flags.append("--dry-run")
    cmd = ["rsync", *flags, *_EXCLUDE_ARGS, f"{src}/", f"{dst}/"]
    return run(cmd)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_push(message: str) -> None:
    """Workspace → git repo → remote."""
    print(f"\n[push] workspace → {REPO} → remote")

    # 1. Sync files to repo (--delete so removals propagate)
    print("\n── rsync ──")
    rsync(WORKSPACE, REPO)

    # 2. Stage everything (respects .gitignore, so .env.local stays out)
    print("\n── git ──")
    run(["git", "add", "-A"], cwd=REPO)

    result = subprocess.run(
        ["git", "diff", "--cached", "--stat"],
        cwd=REPO, capture_output=True, text=True,
    )
    if not result.stdout.strip():
        print("  nothing to commit — repo already matches workspace")
        return

    print(result.stdout)
    run(["git", "commit", "-m", message], cwd=REPO)
    run(["git", "push"], cwd=REPO)
    print("\n[push] done.")


def cmd_pull() -> None:
    """Remote → git repo → workspace."""
    print(f"\n[pull] remote → {REPO} → workspace")

    # 1. Pull latest from remote
    print("\n── git pull ──")
    run(["git", "pull"], cwd=REPO)

    # 2. Sync repo → workspace (--delete so removals propagate)
    print("\n── rsync ──")
    rsync(REPO, WORKSPACE)

    print("\n[pull] done.")


def cmd_status() -> None:
    """Show what push would change (rsync dry-run) and current git status."""
    print(f"\n[status] workspace vs {REPO}")

    print("\n── rsync dry-run (workspace → repo) ──")
    rsync(WORKSPACE, REPO, dry_run=True)

    print("\n── git status in repo ──")
    run(["git", "status", "--short"], cwd=REPO, check=False)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(0)

    if not REPO.exists():
        print(f"ERROR: git repo not found at {REPO}", file=sys.stderr)
        sys.exit(1)

    command = args[0].lower()

    if command == "push":
        if len(args) < 2:
            print("Usage: sync.py push \"commit message\"", file=sys.stderr)
            sys.exit(1)
        cmd_push(args[1])

    elif command == "pull":
        cmd_pull()

    elif command == "status":
        cmd_status()

    else:
        print(f"Unknown command: {command}\nUse push, pull, or status.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
