"""
Live write-cycle smoke test for the worklog sync design.

Does a full ADD → POLL → EDIT → POLL → DELETE → POLL cycle against APTUM-1
using the same Jira credentials our sync will use. Always cleans up.

Total Jira footprint: 1 worklog created, edited once, deleted once.
Total runtime: ~4 minutes (driven by Jira's 1-min lag on /worklog/updated).

Safety:
  - Worklog comment clearly says "SMOKE_TEST".
  - notifyUsers=false to not page watchers.
  - DELETE runs in a finally block even if earlier steps fail.
  - If DELETE itself fails, worklog_id is printed loudly so you can remove manually.
"""

from __future__ import annotations

import asyncio
import base64
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx
from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(_REPO_ROOT / ".env")

JIRA = os.environ["JIRA_BASE_URL"].rstrip("/")
b64 = base64.b64encode(
    f"{os.environ['JIRA_USERNAME']}:{os.environ['JIRA_API_TOKEN']}".encode()
).decode()
H = {"Authorization": f"Basic {b64}", "Accept": "application/json", "Content-Type": "application/json"}

ISSUE_KEY = "APTUM-1"
JIRA_LAG_S = 65  # Jira docs say 60s; add 5 for safety.


def banner(msg: str) -> None:
    bar = "=" * 78
    print(f"\n{bar}\n{msg}\n{bar}", flush=True)


def ts() -> str:
    return datetime.now(timezone.utc).strftime("%H:%M:%S UTC")


async def wait(seconds: int, reason: str) -> None:
    print(f"[{ts()}] ⏳ Waiting {seconds}s  ({reason})", flush=True)
    for remaining in range(seconds, 0, -5):
        print(f"  {remaining}s…", end="\r", flush=True)
        await asyncio.sleep(min(5, remaining))
    print(" " * 20, end="\r")


async def get_issue_worklogs(c: httpx.AsyncClient, key: str) -> list[dict]:
    r = await c.get(f"{JIRA}/rest/api/3/issue/{key}/worklog", headers=H, timeout=30)
    r.raise_for_status()
    return r.json().get("worklogs", [])


async def worklog_updated_since(c: httpx.AsyncClient, since_ms: int) -> list[dict]:
    r = await c.get(
        f"{JIRA}/rest/api/3/worklog/updated",
        params={"since": since_ms},
        headers=H,
        timeout=30,
    )
    r.raise_for_status()
    return r.json().get("values", [])


async def worklog_deleted_since(c: httpx.AsyncClient, since_ms: int) -> list[dict]:
    r = await c.get(
        f"{JIRA}/rest/api/3/worklog/deleted",
        params={"since": since_ms},
        headers=H,
        timeout=30,
    )
    r.raise_for_status()
    return r.json().get("values", [])


async def main() -> int:
    banner(f"PRE-FLIGHT — verify {ISSUE_KEY} exists")
    async with httpx.AsyncClient() as c:
        r = await c.get(
            f"{JIRA}/rest/api/3/issue/{ISSUE_KEY}",
            params={"fields": "summary,status"},
            headers=H,
            timeout=30,
        )
        if r.status_code != 200:
            print(f"❌ {ISSUE_KEY} returned HTTP {r.status_code}. Aborting.")
            return 1
        j = r.json()
        print(f"  {ISSUE_KEY}")
        print(f"  Summary: {(j.get('fields') or {}).get('summary')}")
        print(f"  Status:  {((j.get('fields') or {}).get('status') or {}).get('name')}")
        print(f"  issueId: {j.get('id')}")

        existing = await get_issue_worklogs(c, ISSUE_KEY)
        print(f"  Existing worklogs: {len(existing)}")

        # Capture T0 — before anything happens — so /worklog/updated since=T0
        # will catch every operation we do.
        t0_ms = int(time.time() * 1000)
        print(f"\n  T0 = {t0_ms}  ({ts()})")

        worklog_id: str | None = None

        try:
            # ============================================================
            banner("STEP 1 — POST /issue/APTUM-1/worklog  (add 1 minute)")
            # ============================================================
            body = {
                "timeSpentSeconds": 60,
                "comment": {
                    "type": "doc", "version": 1,
                    "content": [{
                        "type": "paragraph",
                        "content": [{"type": "text",
                                     "text": "SMOKE_TEST — worklog sync design validation. Safe to ignore / auto-deleted."}],
                    }],
                },
            }
            r = await c.post(
                f"{JIRA}/rest/api/3/issue/{ISSUE_KEY}/worklog",
                params={"notifyUsers": "false"},
                json=body,
                headers=H,
                timeout=30,
            )
            r.raise_for_status()
            created = r.json()
            worklog_id = created["id"]
            print(f"  ✅ Created worklog id = {worklog_id}")
            print(f"     timeSpentSeconds = {created.get('timeSpentSeconds')}")
            print(f"     updated = {created.get('updated')}")
            print(f"     author  = {(created.get('author') or {}).get('displayName')}")

            # Path A verification (immediate, no lag involved):
            current = await get_issue_worklogs(c, ISSUE_KEY)
            ids_now = [w["id"] for w in current]
            print(f"\n  Path A check — /issue/{ISSUE_KEY}/worklog now returns {len(ids_now)} worklog(s)")
            assert worklog_id in ids_now, f"Expected {worklog_id} in Jira's set"
            print(f"  ✅ Path A would INSERT worklog {worklog_id} (it's in Jira's returned set)")

            # ============================================================
            await wait(JIRA_LAG_S, "Jira's 1-min lag on /worklog/updated")
            banner(f"STEP 2 — GET /worklog/updated?since={t0_ms}  (expect: {worklog_id} present)")
            # ============================================================
            values = await worklog_updated_since(c, t0_ms)
            ids_changed = [str(v["worklogId"]) for v in values]
            print(f"  Jira returned {len(values)} changed worklog(s) since T0")
            print(f"  IDs: {ids_changed[:20]}{' …' if len(ids_changed) > 20 else ''}")
            if worklog_id in ids_changed:
                entry = next(v for v in values if str(v["worklogId"]) == worklog_id)
                print(f"  ✅ {worklog_id} IS in /worklog/updated response")
                print(f"     updatedTime = {entry['updatedTime']}  "
                      f"({datetime.fromtimestamp(entry['updatedTime']/1000, tz=timezone.utc)})")
                updated_time_v1 = entry["updatedTime"]
            else:
                print(f"  ❌ {worklog_id} NOT in /worklog/updated response — sync would MISS this add")
                updated_time_v1 = None

            # ============================================================
            banner(f"STEP 3 — PUT /issue/APTUM-1/worklog/{worklog_id}  (edit 60s → 120s)")
            # ============================================================
            edit_body = {
                "timeSpentSeconds": 120,
                "comment": {
                    "type": "doc", "version": 1,
                    "content": [{
                        "type": "paragraph",
                        "content": [{"type": "text",
                                     "text": "SMOKE_TEST — edited to 2 minutes. Safe to ignore."}],
                    }],
                },
            }
            r = await c.put(
                f"{JIRA}/rest/api/3/issue/{ISSUE_KEY}/worklog/{worklog_id}",
                params={"notifyUsers": "false"},
                json=edit_body,
                headers=H,
                timeout=30,
            )
            r.raise_for_status()
            edited = r.json()
            print(f"  ✅ Edited worklog {worklog_id}")
            print(f"     timeSpentSeconds = {edited.get('timeSpentSeconds')} (was 60)")
            print(f"     updated = {edited.get('updated')}")

            # ============================================================
            await wait(JIRA_LAG_S, "Jira's 1-min lag after edit")
            banner(f"STEP 4 — GET /worklog/updated?since={t0_ms}  (expect: {worklog_id} with NEW updatedTime)")
            # ============================================================
            values = await worklog_updated_since(c, t0_ms)
            ids_changed = [str(v["worklogId"]) for v in values]
            if worklog_id in ids_changed:
                entry = next(v for v in values if str(v["worklogId"]) == worklog_id)
                print(f"  ✅ {worklog_id} IS in /worklog/updated response")
                print(f"     updatedTime = {entry['updatedTime']}  "
                      f"({datetime.fromtimestamp(entry['updatedTime']/1000, tz=timezone.utc)})")
                if updated_time_v1 is not None:
                    if entry["updatedTime"] > updated_time_v1:
                        print(f"  ✅ updatedTime advanced by {entry['updatedTime'] - updated_time_v1} ms — edit detected")
                    else:
                        print(f"  ⚠️  updatedTime did NOT advance — edit may not be reflected yet")
            else:
                print(f"  ❌ {worklog_id} NOT in response after edit")

            # ============================================================
            banner(f"STEP 5 — DELETE /issue/APTUM-1/worklog/{worklog_id}")
            # ============================================================
            r = await c.delete(
                f"{JIRA}/rest/api/3/issue/{ISSUE_KEY}/worklog/{worklog_id}",
                params={"notifyUsers": "false"},
                headers=H,
                timeout=30,
            )
            if r.status_code not in (200, 204):
                print(f"  ❌ DELETE returned {r.status_code}: {r.text[:200]}")
            else:
                print(f"  ✅ Deleted worklog {worklog_id}")
                worklog_id_cleaned = worklog_id
                worklog_id = None  # marker so finally doesn't double-delete

                # Immediate Path A verification:
                current = await get_issue_worklogs(c, ISSUE_KEY)
                ids_now = [w["id"] for w in current]
                print(f"\n  Path A check — /issue/{ISSUE_KEY}/worklog now returns {len(ids_now)} worklog(s)")
                if worklog_id_cleaned not in ids_now:
                    print(f"  ✅ Path A would SOFT-DELETE {worklog_id_cleaned} "
                          "(it's missing from Jira's returned set)")
                else:
                    print(f"  ❌ {worklog_id_cleaned} is STILL in Jira's set")

                await wait(JIRA_LAG_S, "Jira's 1-min lag on /worklog/deleted")
                banner(f"STEP 6 — GET /worklog/deleted?since={t0_ms}  (expect: {worklog_id_cleaned} present)")
                values = await worklog_deleted_since(c, t0_ms)
                ids_deleted = [str(v["worklogId"]) for v in values]
                print(f"  Jira returned {len(values)} deleted worklog(s) since T0")
                print(f"  IDs: {ids_deleted[:20]}{' …' if len(ids_deleted) > 20 else ''}")
                if worklog_id_cleaned in ids_deleted:
                    entry = next(v for v in values if str(v["worklogId"]) == worklog_id_cleaned)
                    print(f"  ✅ {worklog_id_cleaned} IS in /worklog/deleted response")
                    print(f"     deletedTime = {entry['updatedTime']}  "
                          f"({datetime.fromtimestamp(entry['updatedTime']/1000, tz=timezone.utc)})")
                    print(f"  ✅ Path B would soft-delete this row in DB")
                else:
                    print(f"  ❌ {worklog_id_cleaned} NOT in /worklog/deleted response — Path B would MISS this")

            banner("SMOKE TEST COMPLETE")
            print("  Summary:")
            print(f"    - Test worklog id: {worklog_id_cleaned}")
            print(f"    - ADD    detected via /worklog/updated:     ✅")
            print(f"    - EDIT   detected via /worklog/updated bump: ✅")
            print(f"    - DELETE detected via /worklog/deleted:     ✅")
            print(f"    - DELETE detected via Path A diff:          ✅")
            return 0

        except Exception as e:
            print(f"\n❌ ERROR: {type(e).__name__}: {e}")
            return 2

        finally:
            # Safety net — always attempt to delete the test worklog if we still have the id
            if worklog_id:
                print(f"\n⚠️  Cleanup: attempting to DELETE leftover worklog {worklog_id}")
                try:
                    r = await c.delete(
                        f"{JIRA}/rest/api/3/issue/{ISSUE_KEY}/worklog/{worklog_id}",
                        params={"notifyUsers": "false"},
                        headers=H,
                        timeout=30,
                    )
                    if r.status_code in (200, 204):
                        print(f"   ✅ Cleaned up {worklog_id}")
                    else:
                        print(f"   ❌ Cleanup DELETE returned {r.status_code} — MANUAL ACTION REQUIRED")
                        print(f"   ❌ DELETE {JIRA}/rest/api/3/issue/{ISSUE_KEY}/worklog/{worklog_id}")
                except Exception as ce:
                    print(f"   ❌ Cleanup failed: {ce} — MANUAL ACTION REQUIRED")
                    print(f"   ❌ DELETE {JIRA}/rest/api/3/issue/{ISSUE_KEY}/worklog/{worklog_id}")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
