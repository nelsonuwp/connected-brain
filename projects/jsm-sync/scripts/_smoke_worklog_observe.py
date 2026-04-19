"""
Read-only smoke test for the worklog sync design.

Does NOT modify Jira. Does NOT modify the database. Only reads.

Demonstrates:
  1. What /worklog/updated returns for the last 24h (raw Jira data).
  2. For one recent worklog ID: what /worklog/list returns (the full object).
  3. For one existing APTUM ticket in our DB: what /issue/{key}/worklog returns
     and what our code would do about it (per-ticket Path A simulation).
  4. What the issueId → issue_key resolution would look like against our DB.

Run:
    cd projects/jsm-sync && .venv/bin/python scripts/_smoke_worklog_observe.py
"""

from __future__ import annotations

import asyncio
import base64
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import asyncpg
import httpx
from dotenv import load_dotenv

# Load .env from repo root
_REPO_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(_REPO_ROOT / ".env")

JIRA_BASE = os.environ["JIRA_BASE_URL"].rstrip("/")
JIRA_USER = os.environ["JIRA_USERNAME"]
JIRA_TOKEN = os.environ["JIRA_API_TOKEN"]
DATABASE_URL = os.environ["DATABASE_URL"]


def _auth_headers() -> dict:
    b64 = base64.b64encode(f"{JIRA_USER}:{JIRA_TOKEN}".encode()).decode()
    return {
        "Authorization": f"Basic {b64}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _short_iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def _trim_adf(adf) -> str:
    """Flatten ADF to a short string for display."""
    if not adf:
        return "<no comment>"
    if isinstance(adf, dict) and "content" in adf:
        parts = []
        for node in adf["content"]:
            if node.get("type") == "text":
                parts.append(node.get("text", ""))
            elif "content" in node:
                parts.append(_trim_adf(node))
        s = " ".join(parts).strip()
        return (s[:120] + "…") if len(s) > 120 else s
    return str(adf)[:120]


# ---------------------------------------------------------------------------
# STEP 1 — /worklog/updated for the last 24h
# ---------------------------------------------------------------------------

async def step_1_updated_since(client: httpx.AsyncClient) -> list[int]:
    print("\n" + "=" * 78)
    print("STEP 1 — GET /rest/api/3/worklog/updated  (last 24 hours)")
    print("=" * 78)

    since_dt = datetime.now(timezone.utc) - timedelta(hours=24)
    since_ms = int(since_dt.timestamp() * 1000)
    print(f"since = {since_ms}  ({_short_iso(since_dt)})")

    all_ids: list[int] = []
    current_since = since_ms
    page = 0

    while True:
        page += 1
        r = await client.get(
            f"{JIRA_BASE}/rest/api/3/worklog/updated",
            params={"since": current_since},
            headers=_auth_headers(),
            timeout=30.0,
        )
        r.raise_for_status()
        data = r.json()

        values = data.get("values", [])
        until = int(data.get("until", current_since))
        last_page = data.get("lastPage", True)

        print(
            f"  page {page}: {len(values):4d} changed worklogs  "
            f"until={until}  lastPage={last_page}"
        )
        all_ids.extend(int(v["worklogId"]) for v in values)

        if last_page:
            break
        current_since = until

    print(f"\nTotal changed worklogs (last 24h): {len(all_ids)}")
    if all_ids:
        print(f"  First 10 IDs: {all_ids[:10]}")
    return all_ids


# ---------------------------------------------------------------------------
# STEP 2 — /worklog/list for the most recent worklog
# ---------------------------------------------------------------------------

async def step_2_bulk_details(client: httpx.AsyncClient, ids: list[int]) -> list[dict]:
    print("\n" + "=" * 78)
    print("STEP 2 — POST /rest/api/3/worklog/list  (sample 1 ID)")
    print("=" * 78)

    if not ids:
        print("  (no IDs to fetch — nobody logged work in last 24h)")
        return []

    sample = ids[-1:]  # most recent one
    print(f"Fetching body for worklog id = {sample[0]}")

    r = await client.post(
        f"{JIRA_BASE}/rest/api/3/worklog/list",
        json={"ids": sample},
        headers=_auth_headers(),
        timeout=30.0,
    )
    r.raise_for_status()
    worklogs = r.json()

    for w in worklogs:
        print(f"\n  id            = {w.get('id')}")
        print(f"  issueId       = {w.get('issueId')}")
        print(f"  author        = {(w.get('author') or {}).get('displayName')} "
              f"<{(w.get('author') or {}).get('emailAddress')}>")
        print(f"  started       = {w.get('started')}")
        print(f"  timeSpent     = {w.get('timeSpent')}  ({w.get('timeSpentSeconds')}s)")
        print(f"  created       = {w.get('created', '<absent in GET>')}")
        print(f"  updated       = {w.get('updated')}")
        print(f"  comment       = {_trim_adf(w.get('comment'))}")
        print(f"  visibility    = {w.get('visibility')}")

    return worklogs


# ---------------------------------------------------------------------------
# STEP 3 — issueId → issue_key resolution against our DB
# ---------------------------------------------------------------------------

async def step_3_resolve_ids(worklogs: list[dict]) -> dict[int, str]:
    print("\n" + "=" * 78)
    print("STEP 3 — Resolve issueId → issue_key against our Postgres DB")
    print("=" * 78)

    if not worklogs:
        print("  (nothing to resolve)")
        return {}

    issue_ids = [int(w["issueId"]) for w in worklogs if w.get("issueId")]
    print(f"  Looking up {len(issue_ids)} issueId(s) in tickets table…")

    # NOTE: our current schema doesn't have tickets.issue_id yet (that's the
    # column we're adding in schema/003_worklogs.sql). So this lookup will
    # be empty today — but we can simulate it by pulling issue_key from
    # the live Jira API.
    conn = await asyncpg.connect(dsn=DATABASE_URL)
    try:
        # Probe: does tickets.issue_id exist?
        has_issue_id = await conn.fetchval(
            "SELECT EXISTS (SELECT 1 FROM information_schema.columns "
            "WHERE table_name='tickets' AND column_name='issue_id')"
        )
        print(f"  tickets.issue_id column exists? {has_issue_id}")

        if has_issue_id:
            rows = await conn.fetch(
                "SELECT issue_id, issue_key FROM tickets "
                "WHERE issue_id = ANY($1::bigint[])",
                issue_ids,
            )
            mapping = {r["issue_id"]: r["issue_key"] for r in rows}
            print(f"  Resolved in DB: {len(mapping)}/{len(issue_ids)}")
            for iid, key in mapping.items():
                print(f"    {iid} → {key}")
            missing = [i for i in issue_ids if i not in mapping]
            if missing:
                print(f"  {len(missing)} issueIds NOT in our DB "
                      "(other project, or not synced yet — we'd skip these)")
        else:
            print("  Column doesn't exist yet → this is the schema change "
                  "003_worklogs.sql will add.")
            print("  Simulating via live Jira /issue/{id} calls instead:")
            mapping = {}
            async with httpx.AsyncClient() as c:
                for iid in issue_ids[:3]:
                    r = await c.get(
                        f"{JIRA_BASE}/rest/api/3/issue/{iid}",
                        params={"fields": "issuetype"},
                        headers=_auth_headers(),
                        timeout=15.0,
                    )
                    if r.status_code == 200:
                        key = r.json().get("key")
                        mapping[iid] = key
                        # Is this ticket in our DB?
                        in_db = await conn.fetchval(
                            "SELECT EXISTS (SELECT 1 FROM tickets WHERE issue_key=$1)",
                            key,
                        )
                        print(f"    issueId {iid} → {key}  "
                              f"{'(in our DB)' if in_db else '(NOT in our DB — would skip)'}")
                    else:
                        print(f"    issueId {iid} → HTTP {r.status_code}")
        return mapping
    finally:
        await conn.close()


# ---------------------------------------------------------------------------
# STEP 4 — Per-ticket Path A simulation
# ---------------------------------------------------------------------------

async def step_4_path_a_simulation(client: httpx.AsyncClient) -> None:
    print("\n" + "=" * 78)
    print("STEP 4 — Path A simulation: pick one APTUM ticket with worklogs and")
    print("         show what the per-ticket sweep would do.")
    print("=" * 78)

    conn = await asyncpg.connect(dsn=DATABASE_URL)
    try:
        # Pick the most recently updated APTUM ticket that has no worklogs in DB
        # (since we haven't implemented yet, all tickets qualify — pick any recent one)
        row = await conn.fetchrow(
            """
            SELECT issue_key, updated_at
            FROM tickets
            WHERE deleted_at IS NULL
              AND status NOT IN ('Closed','Done','Resolved','Complete','Completed')
            ORDER BY updated_at DESC
            LIMIT 1
            """
        )
        if not row:
            row = await conn.fetchrow(
                "SELECT issue_key, updated_at FROM tickets "
                "ORDER BY updated_at DESC LIMIT 1"
            )

        if not row:
            print("  No tickets in DB yet — backfill is still populating.")
            return

        issue_key = row["issue_key"]
        print(f"  Target ticket: {issue_key}  (updated_at={row['updated_at']})")
    finally:
        await conn.close()

    # Hit /issue/{key}/worklog
    print(f"\n  Fetching /rest/api/3/issue/{issue_key}/worklog …")
    r = await client.get(
        f"{JIRA_BASE}/rest/api/3/issue/{issue_key}/worklog",
        headers=_auth_headers(),
        timeout=30.0,
    )
    r.raise_for_status()
    data = r.json()

    worklogs = data.get("worklogs", [])
    total = data.get("total", 0)
    print(f"  Jira reports {total} worklogs on {issue_key}:")

    for w in worklogs[:5]:
        print(f"    • id={w.get('id')}  "
              f"{(w.get('author') or {}).get('displayName')}  "
              f"{w.get('timeSpentSeconds')}s  "
              f"started={w.get('started')}  "
              f"updated={w.get('updated')}")
        print(f"      comment: {_trim_adf(w.get('comment'))}")

    if total > 5:
        print(f"    … ({total - 5} more)")

    print("\n  What Path A would do RIGHT NOW if it ran:")
    if total == 0:
        print("    - Jira set: {} (empty)")
        print("    - DB set:   {} (empty, table doesn't exist yet)")
        print("    - Action:   nothing.")
    else:
        print(f"    - Jira set: {{{', '.join(str(w['id']) for w in worklogs[:5])}"
              f"{', …' if total > 5 else ''}}}")
        print("    - DB set:   {} (table doesn't exist yet — every row is an INSERT)")
        print(f"    - Action:   INSERT {total} row(s) into ticket_worklogs.")
        print(f"    - Diff:     no DB-side IDs to soft-delete (DB is empty).")

    print("\n  To simulate a DELETE cycle later: the script would snapshot")
    print("  the current worklog set, you'd delete one in Jira UI, and re-run.")
    print("  The 'missing' ID would be the one Path A soft-deletes.")


# ---------------------------------------------------------------------------
# STEP 5 — /worklog/deleted for the last 24h
# ---------------------------------------------------------------------------

async def step_5_deleted_since(client: httpx.AsyncClient) -> None:
    print("\n" + "=" * 78)
    print("STEP 5 — GET /rest/api/3/worklog/deleted  (last 24 hours)")
    print("=" * 78)

    since_dt = datetime.now(timezone.utc) - timedelta(hours=24)
    since_ms = int(since_dt.timestamp() * 1000)

    r = await client.get(
        f"{JIRA_BASE}/rest/api/3/worklog/deleted",
        params={"since": since_ms},
        headers=_auth_headers(),
        timeout=30.0,
    )
    r.raise_for_status()
    data = r.json()

    values = data.get("values", [])
    print(f"  since={since_ms}  until={data.get('until')}  "
          f"lastPage={data.get('lastPage')}")
    print(f"  {len(values)} worklogs deleted in the last 24h")

    for v in values[:5]:
        print(f"    • worklogId={v.get('worklogId')}  "
              f"deletedTime={datetime.fromtimestamp(v['updatedTime']/1000, tz=timezone.utc)}")

    if not values:
        print("  (nobody deleted a worklog in the last 24h — normal)")

    print("\n  If any of these IDs exist in our ticket_worklogs table,")
    print("  Path B would run:")
    print("    UPDATE ticket_worklogs SET deleted_at = NOW()")
    print(f"    WHERE worklog_id = ANY({[v['worklogId'] for v in values[:5]]}::bigint[])")


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

async def main() -> None:
    print(f"\nJira:     {JIRA_BASE}")
    print(f"Postgres: {DATABASE_URL.split('@')[-1]}  (redacted creds)")

    async with httpx.AsyncClient() as client:
        updated_ids = await step_1_updated_since(client)
        worklogs = await step_2_bulk_details(client, updated_ids)
        await step_3_resolve_ids(worklogs)
        await step_4_path_a_simulation(client)
        await step_5_deleted_since(client)

    print("\n" + "=" * 78)
    print("Smoke observation complete. No writes performed anywhere.")
    print("=" * 78)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(130)
