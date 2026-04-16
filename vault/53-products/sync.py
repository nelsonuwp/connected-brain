#!/usr/bin/env python3
"""
sync.py — bidirectional sync between vault/53-products and the product-strategy git repo.

Usage:
    python sync.py pull   # git pull in product-strategy, then sync → 53-products
    python sync.py push   # sync 53-products → product-strategy, then git commit + push
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

VAULT_DIR = Path(__file__).parent.resolve()
REPO_DIR = Path("/Users/anelson-macbook-air/Code/product-strategy")

# These paths (relative to the source) are never synced in either direction.
EXCLUDES = [
    "sync.py",
    "supplemental-data/",
    ".DS_Store",
    ".git/",
]


def rsync(src: Path, dst: Path):
    exclude_args = []
    for pattern in EXCLUDES:
        exclude_args += ["--exclude", pattern]

    cmd = [
        "rsync",
        "-av",          # archive mode + verbose
        "--delete",     # remove files in dst that are gone from src
        *exclude_args,
        f"{src}/",      # trailing slash = sync contents, not the dir itself
        f"{dst}/",
    ]
    print(f"  rsync {src}/ → {dst}/")
    run(cmd)


def run(cmd: list[str], cwd: Path | None = None):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.stdout.strip():
        print(result.stdout.rstrip())
    if result.returncode != 0:
        print(f"ERROR: {' '.join(str(c) for c in cmd)}", file=sys.stderr)
        if result.stderr.strip():
            print(result.stderr.rstrip(), file=sys.stderr)
        sys.exit(1)
    return result.stdout


def pull():
    print("=== PULL ===")
    print(f"[1/2] git pull in {REPO_DIR}")
    run(["git", "pull", "origin", "main"], cwd=REPO_DIR)

    print(f"[2/2] syncing product-strategy → vault/53-products")
    rsync(REPO_DIR, VAULT_DIR)

    print("\nDone. Vault is up to date.")


def push():
    print("=== PUSH ===")
    print(f"[1/3] syncing vault/53-products → product-strategy")
    rsync(VAULT_DIR, REPO_DIR)

    print(f"[2/3] staging changes in {REPO_DIR}")
    run(["git", "add", "."], cwd=REPO_DIR)

    # Check if there's anything to commit
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO_DIR, text=True, capture_output=True
    )
    if not status.stdout.strip():
        print("Nothing to commit — repo is already up to date.")
        return

    changed_files = len(status.stdout.strip().splitlines())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"vault sync: {changed_files} file{'s' if changed_files != 1 else ''} changed — {timestamp}"

    print(f"[3/3] committing and pushing: \"{message}\"")
    run(["git", "commit", "-m", message], cwd=REPO_DIR)
    run(["git", "push", "origin", "main"], cwd=REPO_DIR)

    print("\nDone. product-strategy is up to date.")


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("pull", "push"):
        print("Usage: python sync.py [pull|push]")
        sys.exit(1)

    if not REPO_DIR.exists():
        print(f"ERROR: repo directory not found: {REPO_DIR}", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "pull":
        pull()
    else:
        push()


if __name__ == "__main__":
    main()
