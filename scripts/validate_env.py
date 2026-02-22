#!/usr/bin/env python3
"""
Validate that .env matches .env.example (config contract).

- Missing required variables -> fail
- Unknown variables in .env (not in .env.example) -> fail
- Empty required values -> fail

Usage:
  python scripts/validate_env.py
  # or from repo root:
  python -m scripts.validate_env

Expects .env.example and .env at repo root (parent of scripts/).
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
ENV_EXAMPLE = ROOT / ".env.example"
ENV_FILE = ROOT / ".env"


def parse_env_example(path: Path):
    """Parse .env.example; return (all_keys, required_keys)."""
    text = path.read_text()
    all_keys = set()
    required_keys = set()
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("#") and "| required" in line and "optional" not in line:
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                if next_line.strip() and not next_line.strip().startswith("#"):
                    if "=" in next_line:
                        key = next_line.split("=", 1)[0].strip()
                        if key and re.match(r"^[A-Z][A-Z0-9_]*$", key):
                            all_keys.add(key)
                            required_keys.add(key)
                    break
                j += 1
            i += 1
            continue
        if "=" in line and not line.strip().startswith("#"):
            key = line.split("=", 1)[0].strip()
            if key and re.match(r"^[A-Z][A-Z0-9_]*$", key):
                all_keys.add(key)
        i += 1
    return all_keys, required_keys


def parse_env(path: Path):
    """Parse .env into key -> value."""
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if key and re.match(r"^[A-Z][A-Z0-9_]*$", key):
                if len(value) >= 2 and value[0] == value[-1] and value[0] in '"\'':
                    value = value[1:-1]
                out[key] = value
    return out


def main():
    if not ENV_EXAMPLE.exists():
        print("Error: .env.example not found at", ENV_EXAMPLE, file=sys.stderr)
        return 1

    all_keys, required_keys = parse_env_example(ENV_EXAMPLE)

    if not ENV_FILE.exists():
        print("Error: .env not found at", ENV_FILE, file=sys.stderr)
        return 1

    env = parse_env(ENV_FILE)
    errors = []

    unknown = set(env) - all_keys
    if unknown:
        errors.append("Unknown variables in .env (not in .env.example): " + ", ".join(sorted(unknown)))

    missing = required_keys - set(env)
    if missing:
        errors.append("Missing required variables: " + ", ".join(sorted(missing)))

    empty_required = [k for k in required_keys if k in env and env[k].strip() == ""]
    if empty_required:
        errors.append("Required variables are empty: " + ", ".join(sorted(empty_required)))

    if errors:
        for e in errors:
            print("Error:", e, file=sys.stderr)
        return 1

    print("OK: .env matches .env.example (required vars present, no unknown vars).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
