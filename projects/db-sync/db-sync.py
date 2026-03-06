#!/usr/bin/env python3
"""
db-sync.py

Usage:
  python db-sync.py                        # sync everything in databases.json
  python db-sync.py --group ocean          # one group
  python db-sync.py --table dimServices    # one table (requires --group)
  python db-sync.py --dry-run              # print output, no file writes
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Ensure the project directory is on the path regardless of where script is invoked from
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dotenv import load_dotenv

# .env lives at ~/connected-brain/.env — two levels up from projects/db-sync/
_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_ENV_PATH)


# region agent log helper
def _agent_debug_log(hypothesis_id, message, data=None, run_id="pre-fix"):
    try:
        # Repo root: db-sync.py -> parents[2] = connected-brain
        _log_path = Path(__file__).resolve().parents[2] / ".cursor" / "debug-4ea72c.log"
        _log_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "sessionId": "4ea72c",
            "runId": run_id,
            "hypothesisId": str(hypothesis_id),
            "location": "projects/db-sync/db-sync.py",
            "message": str(message),
            "data": data or {},
            "timestamp": int(time.time() * 1000),
        }
        with open(_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
    except Exception:
        # Swallow logging errors to avoid impacting main flow
        pass


# endregion


def load_connector(group_type: str, group_config: dict):
    if group_type == "mssql":
        from connectors.mssql import MSSQLConnector
        return MSSQLConnector(group_config)
    raise ValueError(f"Unknown connector type: '{group_type}'")


def resolve_vault_root() -> Path:
    env = os.environ.get("BRAIN_VAULT_ROOT")
    if env:
        return Path(env)
    return Path.home() / "connected-brain" / "vault"


def entry_label(entry: dict) -> str:
    return entry.get("table") or entry.get("object") or "unknown"


def sync_entry(connector, entry: dict, vault_root: Path, dry_run: bool) -> bool:
    label = entry_label(entry)
    target_path = vault_root / entry["target"]

    print(f"  → {label} ... ", end="", flush=True)
    try:
        schema = connector.get_schema(entry)
        sample = connector.get_sample(entry)
        new_content = connector.render(entry, schema, sample)

        if target_path.exists():
            existing = target_path.read_text(encoding="utf-8")
            final_content = connector.merge(existing, new_content)
        else:
            final_content = new_content

        if dry_run:
            print("DRY RUN")
            print("─" * 60)
            print(final_content[:3000])
            if len(final_content) > 3000:
                print(f"  ... ({len(final_content) - 3000} more chars)")
            print("─" * 60)
        else:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(final_content, encoding="utf-8")
            print("✓")

        return True

    except Exception as e:
        print(f"✗  {type(e).__name__}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--group",   help="Only sync this group")
    parser.add_argument("--table",   help="Only sync this table/object (requires --group)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--config",  default="databases.json")
    args = parser.parse_args()

    if args.table and not args.group:
        print("ERROR: --table requires --group", file=sys.stderr)
        sys.exit(1)

    config_path = Path(args.config)
    manifest = json.loads(config_path.read_text())

    vault_root = resolve_vault_root()
    print(f"Vault:  {vault_root}")
    print(f"Config: {config_path}")
    print(f"Mode:   {'DRY RUN' if args.dry_run else 'WRITE'}\n")

    groups = manifest["groups"]
    if args.group:
        if args.group not in groups:
            print(f"ERROR: Group '{args.group}' not found. Available: {', '.join(groups)}", file=sys.stderr)
            sys.exit(1)
        groups = {args.group: groups[args.group]}

    total_ok = total_err = 0
    now_iso = datetime.now(timezone.utc).isoformat()

    for group_name, group_config in groups.items():
        group_type = group_config.get("type", "")
        print(f"[{group_name}]  type={group_type}")

        entries = group_config.get("tables", [])

        # region agent log
        _agent_debug_log(
            "H3",
            "Attempting to load connector",
            {
                "group_name": group_name,
                "group_type": group_type,
                "env_prefix": group_config.get("env_prefix"),
                "entries_count": len(entries),
            },
        )
        # endregion
        if args.table:
            entries = [e for e in entries if entry_label(e) == args.table]
            if not entries:
                print(f"  No table '{args.table}' in group '{group_name}'")
                continue

        try:
            connector = load_connector(group_type, group_config)
            # region agent log
            _agent_debug_log(
                "H3",
                "Connector loaded successfully",
                {
                    "group_name": group_name,
                    "group_type": group_type,
                },
            )
            # endregion
        except Exception as e:
            # region agent log
            _agent_debug_log(
                "H3",
                "Connector load failed",
                {
                    "group_name": group_name,
                    "group_type": group_type,
                    "error_type": type(e).__name__,
                    "error": str(e),
                },
            )
            # endregion
            print(f"  ✗ Connection failed: {type(e).__name__}: {e}")
            total_err += len(entries)
            continue

        for entry in entries:
            ok = sync_entry(connector, entry, vault_root, args.dry_run)
            if ok:
                total_ok += 1
                if not args.dry_run:
                    entry["last_synced"] = now_iso
            else:
                total_err += 1

        connector.close()
        print()

    if not args.dry_run and total_ok > 0:
        config_path.write_text(json.dumps(manifest, indent=2))

    symbol = "✓" if total_err == 0 else "⚠"
    print(f"{symbol}  {total_ok} succeeded, {total_err} failed.")
    sys.exit(0 if total_err == 0 else 1)


if __name__ == "__main__":
    main()