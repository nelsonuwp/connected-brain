"""
Jira client: async fetch with Scout (all keys) → Gather (semaphore, retry on 429/5xx).
Ported from projects/_reference/clients/jiraClient.py.

Removed vs reference:
  - core.utils imports (log, make_source_object, save_source_artifact, record_count_from_data)
  - fetch_jira_data / fetch_jira_data_sync (artifact-shaped orchestrators)
  - fetch_organization_users
  - pandas import
  - worklog fetch in backfill path (_fetch_worklog kept for on-demand use)

Changed vs reference:
  - All log("⚠️", ...) / log("✗", ...) → stdlib logger calls
  - create_history_trail: new event schema with id, created_at, is_public, body (full, untruncated)
  - _process_issue_to_ticket: new schema matching DB columns (no time_entries, no closed_by)
  - _fetch_asset_details_sync: returns {object_id, workspace_id, asset_name, service_id}
  - _load_automation_config: path resolves to jsm-sync/config/ (parent.parent of this file)
  - Config vars sourced from settings, not os.getenv at module level

Added vs reference:
  - build_project_jql — project-scoped JQL (no cf[11709])
  - fetch_ticket_batch — public entry point for backfill/incremental
"""

import asyncio
import base64
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Optional, TypeVar

import httpx
import requests
from dateutil import parser

from .config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T")

PAGE_SIZE = 100
_JIRA_SEARCH_URL = "/rest/api/3/search/jql"
_AUTOMATION_CONFIG = None


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def _auth_headers() -> Dict[str, str]:
    username = settings.jira_username
    token = settings.jira_api_token
    if not username or not token:
        return {}
    b64 = base64.b64encode(f"{username}:{token}".encode()).decode()
    return {"Authorization": f"Basic {b64}", "Content-Type": "application/json"}


def _jsm_assets_headers() -> Dict[str, str]:
    username = settings.jira_username
    token = settings.jira_api_token
    if not username or not token:
        return {"Accept": "application/json"}
    b64 = base64.b64encode(f"{username}:{token}".encode()).decode()
    return {"Accept": "application/json", "Authorization": f"Basic {b64}"}


# ---------------------------------------------------------------------------
# Retry with backoff
# ---------------------------------------------------------------------------

async def retry_with_backoff(
    func: Callable[[], Awaitable[T]],
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
) -> T:
    """Retry async function with exponential backoff for rate limits and transient errors."""
    last_exception: Optional[Exception] = None
    delay = initial_delay

    for attempt in range(max_retries + 1):
        try:
            return await func()
        except httpx.HTTPStatusError as e:
            last_exception = e
            if e.response.status_code == 429:
                retry_after = e.response.headers.get("Retry-After")
                if retry_after:
                    try:
                        wait_time = min(float(retry_after), max_delay)
                    except ValueError:
                        wait_time = min(delay, max_delay)
                else:
                    wait_time = min(delay, max_delay)
                if attempt < max_retries:
                    logger.warning(
                        "Rate limited (429), retrying in %.1fs (attempt %d/%d)",
                        wait_time, attempt + 1, max_retries,
                    )
                    await asyncio.sleep(wait_time)
                    delay = min(delay * backoff_factor, max_delay)
                    continue
                logger.error("All %d retry attempts exhausted (429)", max_retries)
                raise
            elif 500 <= e.response.status_code < 600:
                if attempt < max_retries:
                    wait_time = min(delay, max_delay)
                    logger.warning(
                        "Server error %d, retrying in %.1fs (attempt %d/%d)",
                        e.response.status_code, wait_time, attempt + 1, max_retries,
                    )
                    await asyncio.sleep(wait_time)
                    delay = min(delay * backoff_factor, max_delay)
                    continue
                logger.error("All %d retry attempts exhausted (%d)", max_retries, e.response.status_code)
                raise
            raise
        except (httpx.TimeoutException, httpx.NetworkError) as e:
            last_exception = e
            if attempt < max_retries:
                wait_time = min(delay, max_delay)
                logger.warning(
                    "Network/timeout error, retrying in %.1fs (attempt %d/%d)",
                    wait_time, attempt + 1, max_retries,
                )
                await asyncio.sleep(wait_time)
                delay = min(delay * backoff_factor, max_delay)
                continue
            logger.error("All %d retry attempts exhausted (network/timeout)", max_retries)
            raise

    logger.error("All %d retry attempts exhausted", max_retries)
    raise last_exception  # type: ignore[misc]


# ---------------------------------------------------------------------------
# ADF parser
# ---------------------------------------------------------------------------

def parse_adf_to_text(adf: Any) -> str:
    if not adf or not isinstance(adf, dict) or "content" not in adf:
        return str(adf) if adf else ""
    parts = []
    for node in adf["content"]:
        if node.get("type") == "text":
            parts.append(node.get("text", ""))
        elif "content" in node:
            parts.append(parse_adf_to_text(node))
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Automation config + role detection
# ---------------------------------------------------------------------------

def _load_automation_config() -> dict:
    """Load automation users config from config/jira_automation_users.json (cached)."""
    global _AUTOMATION_CONFIG
    if _AUTOMATION_CONFIG is not None:
        return _AUTOMATION_CONFIG

    # jsm_sync/jira_client.py → parent = jsm_sync/ → parent.parent = jsm-sync/ (project root)
    config_path = Path(__file__).resolve().parents[1] / "config" / "jira_automation_users.json"

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            _AUTOMATION_CONFIG = json.load(f)
            logger.info("Loaded automation config from %s", config_path)
    except FileNotFoundError:
        logger.info("Config file not found at %s, using defaults", config_path)
        _AUTOMATION_CONFIG = {
            "email_patterns": [
                "noreply@", "no-reply@", "-scraper@", "automation@",
                "notifications.", "alerts@", "monitoring@", "veeam", "alertlogic",
            ],
            "specific_users": {"by_email": [], "by_display_name": []},
        }
    except json.JSONDecodeError as e:
        logger.warning("Invalid JSON in automation config: %s, using defaults", e)
        _AUTOMATION_CONFIG = {
            "email_patterns": [
                "noreply@", "no-reply@", "-scraper@", "automation@",
                "notifications.", "alerts@", "monitoring@", "veeam", "alertlogic",
            ],
            "specific_users": {"by_email": [], "by_display_name": []},
        }

    return _AUTOMATION_CONFIG


def determine_role(author_obj: Any) -> str:
    """
    Determine role (Automation, Customer, Aptum, Unknown) based on:
    1. Email substring patterns (noreply@, automation@, etc.)
    2. Specific emails from config
    3. Display names from config (PagerDuty, Automation for Jira, etc.)
    4. Jira accountType as final fallback
    """
    if not author_obj or not isinstance(author_obj, dict):
        return "Unknown"

    config = _load_automation_config()
    email = (author_obj.get("emailAddress") or "").strip().lower()

    if email and any(p in email for p in config.get("email_patterns", [])):
        return "Automation"

    normalized_emails = [e.strip().lower() for e in config.get("specific_users", {}).get("by_email", [])]
    if email and email in normalized_emails:
        return "Automation"

    display_name = (author_obj.get("displayName") or "").strip()
    normalized_names = {n.strip().lower() for n in config.get("specific_users", {}).get("by_display_name", [])}
    if display_name and display_name.lower() in normalized_names:
        return "Automation"

    acc_type = author_obj.get("accountType", "unknown")
    return "Customer" if acc_type == "customer" else "Aptum"


# ---------------------------------------------------------------------------
# SLA helpers
# ---------------------------------------------------------------------------

def extract_sla_details(sla_field: Any) -> Optional[dict]:
    if not sla_field or not isinstance(sla_field, dict):
        return None
    cycle = sla_field.get("completedCycles")
    if cycle and isinstance(cycle, list) and len(cycle) > 0:
        cycle = cycle[-1]
    elif sla_field.get("ongoingCycle"):
        cycle = sla_field.get("ongoingCycle")
    else:
        return None
    elapsed = (cycle.get("elapsedTime") or {}).get("millis", 0)
    goal = (cycle.get("goalDuration") or {}).get("millis", 0)
    return {
        "elapsed_seconds": int(elapsed / 1000),
        "breached": cycle.get("breached", False),
        "threshold_seconds": int(goal / 1000),
    }


# ---------------------------------------------------------------------------
# Closure info (resolved_at)
# ---------------------------------------------------------------------------

_CLOSED_STATUSES = {"Done", "Resolved", "Closed", "Complete", "Completed"}


def _get_closure_info(changelog: dict) -> dict:
    """Walk changelog histories in reverse, find first transition to a closed status."""
    if not changelog or not isinstance(changelog, dict):
        return {}
    histories = changelog.get("histories")
    if not histories:
        return {}
    for h in reversed(histories):
        for item in h.get("items", []):
            if item.get("field") == "status" and item.get("toString") in _CLOSED_STATUSES:
                author = h.get("author") or {}
                return {
                    "closed_date": h.get("created"),
                    "closed_by": {
                        "name": author.get("displayName"),
                        "email": author.get("emailAddress"),
                        "role": determine_role(author),
                        "id": author.get("accountId"),
                    },
                    "previous_status": item.get("fromString"),
                    "closure_status": item.get("toString"),
                }
    return {}


# ---------------------------------------------------------------------------
# History trail (thread_events)
# ---------------------------------------------------------------------------

def create_history_trail(issue: dict, comments: list) -> list:
    """Build thread_events list from Jira comment objects."""
    events = []
    for comment in comments:
        try:
            created = parser.parse(comment.get("created"))
        except (ValueError, TypeError):
            created = datetime.min.replace(tzinfo=timezone.utc)
        author = comment.get("author", {})
        role = determine_role(author)
        text = " ".join(parse_adf_to_text(comment.get("body")).split())
        events.append({
            "id": comment.get("id"),
            "date": created.isoformat(),
            "created_at": created,
            "role": role,
            "author": author.get("displayName"),
            "author_account_id": author.get("accountId"),
            "author_email": author.get("emailAddress"),
            "account_type": author.get("accountType"),
            "is_public": comment.get("jsdPublic"),
            "body": text,
            "kind": "comment",
        })
    return events


_CHANGELOG_SKIP_FIELDS = frozenset({
    "timeestimate", "timespent", "WorklogId", "Sentiment",
    "remoteIssueLink", "Rank", "rank",
})

_CHANGELOG_FIELD_LABELS = {
    "status": "Status",
    "resolution": "Resolution",
    "reporter": "Reporter",
    "assignee": "Assignee",
    "Request Type": "Request type",
    "security": "Visibility",
    "Organizations": "Organization",
    "CustomerID": "Customer ID",
    "Team": "Team",
    "Link": "Link",
    "priority": "Priority",
    "summary": "Summary",
    "issuetype": "Issue type",
}


def _format_changelog_body(items: list[dict]) -> str:
    """Format changelog items into a human-readable single line."""
    parts = []
    for item in items:
        field = item.get("field", "")
        if field in _CHANGELOG_SKIP_FIELDS:
            continue
        label = _CHANGELOG_FIELD_LABELS.get(field, field)
        from_str = item.get("fromString") or ""
        to_str = item.get("toString") or ""
        if from_str and to_str and from_str != to_str:
            parts.append(f"{label}: {from_str} → {to_str}")
        elif to_str:
            parts.append(f"{label}: {to_str}")
        elif from_str:
            parts.append(f"{label} removed: {from_str}")
    return " · ".join(parts)


def create_changelog_events(issue: dict) -> list:
    """Build thread_events list from Jira changelog histories."""
    changelog = issue.get("changelog") or {}
    histories = changelog.get("histories") or []
    events = []
    for history in histories:
        items = history.get("items") or []
        body = _format_changelog_body(items)
        if not body:
            continue
        try:
            created = parser.parse(history.get("created"))
        except (ValueError, TypeError):
            created = datetime.min.replace(tzinfo=timezone.utc)
        author = history.get("author") or {}
        role = determine_role(author)
        events.append({
            "id": f"changelog-{history['id']}",
            "date": created.isoformat(),
            "created_at": created,
            "role": role,
            "author": author.get("displayName"),
            "author_account_id": author.get("accountId"),
            "author_email": author.get("emailAddress"),
            "account_type": author.get("accountType"),
            "is_public": None,
            "body": body,
            "kind": "changelog",
        })
    return events


# ---------------------------------------------------------------------------
# Issue processing
# ---------------------------------------------------------------------------

def _build_user_dict(field: dict) -> Optional[dict]:
    """Convert a Jira user field object to the canonical user shape."""
    if not field or not isinstance(field, dict):
        return None
    account_id = field.get("accountId")
    if not account_id:
        return None
    return {
        "account_id": account_id,
        "display_name": field.get("displayName") or "",
        "email": field.get("emailAddress"),
        "role": determine_role(field),
        "account_type": field.get("accountType"),
    }


def _process_issue_to_ticket(
    issue: dict,
    comments: list,
    asset_details: list,
    worklogs: list[dict] | None = None,
) -> Optional[dict]:
    """Build one ticket dict from raw issue + comments + hydrated assets + worklogs."""
    key = issue.get("key")
    if not key:
        return None

    issue_id: int | None = None
    raw_id = issue.get("id")
    if raw_id is not None:
        try:
            issue_id = int(raw_id)
        except (ValueError, TypeError):
            issue_id = None

    fields = issue.get("fields") or {}

    # Organisation
    jira_org_id = None
    jira_org_name = None
    org_field = fields.get("customfield_11100")
    if org_field and isinstance(org_field, list) and len(org_field) > 0:
        first_org = org_field[0]
        if isinstance(first_org, dict):
            jira_org_id = str(first_org.get("id")) if first_org.get("id") else None
            jira_org_name = first_org.get("name")

    # Request type
    request_type = None
    req_type_field = fields.get("customfield_11200")
    if isinstance(req_type_field, dict):
        rt_obj = req_type_field.get("requestType")
        if isinstance(rt_obj, dict):
            request_type = rt_obj.get("name")
    elif isinstance(req_type_field, str):
        request_type = req_type_field

    # ocean_client_id from customfield_11709
    ocean_client_id = None
    ocean_raw = fields.get("customfield_11709")
    if ocean_raw is not None:
        try:
            ocean_client_id = int(ocean_raw)
        except (ValueError, TypeError):
            pass

    # Users
    creator = _build_user_dict(fields.get("creator") or {})
    reporter = _build_user_dict(fields.get("reporter") or {})
    assignee = _build_user_dict(fields.get("assignee") or {})

    # Issue type
    issue_type = (fields.get("issuetype") or {}).get("name")

    # Status / priority / labels
    status = (fields.get("status") or {}).get("name", "Unknown")
    priority = (fields.get("priority") or {}).get("name")
    labels = fields.get("labels") or []

    # Closure / resolved_at
    closure = _get_closure_info(issue.get("changelog") or {})
    resolved_at = None
    if closure.get("closed_date"):
        try:
            resolved_at = parser.parse(closure["closed_date"])
        except (ValueError, TypeError):
            pass

    # Timestamps
    created_at = None
    updated_at = None
    try:
        created_at = parser.parse(fields.get("created"))
    except (ValueError, TypeError):
        created_at = datetime.now(timezone.utc)
    try:
        updated_at = parser.parse(fields.get("updated"))
    except (ValueError, TypeError):
        updated_at = datetime.now(timezone.utc)

    # is_customer_originated: creator role == "Customer"
    is_customer_originated = (creator or {}).get("role") == "Customer"

    return {
        "issue_key": key,
        "summary": fields.get("summary", ""),
        "description": parse_adf_to_text(fields.get("description")),
        "status": status,
        "priority": priority,
        "issue_type": issue_type,
        "request_type": request_type,
        "is_customer_originated": is_customer_originated,
        "creator": creator,
        "reporter": reporter,
        "assignee": assignee,
        "jira_org_id": jira_org_id,
        "jira_org_name": jira_org_name,
        "ocean_client_id": ocean_client_id,
        "labels": labels,
        "sla_first_response": extract_sla_details(fields.get("customfield_11312")),
        "sla_resolution": extract_sla_details(fields.get("customfield_11311")),
        "created_at": created_at,
        "updated_at": updated_at,
        "resolved_at": resolved_at,
        "issue_id": issue_id,
        "thread_events": sorted(
            create_history_trail(issue, comments) + create_changelog_events(issue),
            key=lambda e: e["created_at"],
        ),
        "assets": asset_details,
        "worklogs": worklogs or [],
    }


# ---------------------------------------------------------------------------
# Asset hydration (sync, runs in thread)
# ---------------------------------------------------------------------------

def _fetch_asset_details_sync(asset_data: dict) -> Optional[dict]:
    """JSM Assets: sync request (external Atlassian API). Returns DB-ready asset dict."""
    workspace_id = asset_data.get("workspaceId")
    object_id = asset_data.get("objectId")
    if not workspace_id or not object_id:
        return None
    url = f"https://api.atlassian.com/jsm/assets/workspace/{workspace_id}/v1/object/{object_id}"
    try:
        r = requests.get(url, headers=_jsm_assets_headers(), timeout=15)
        r.raise_for_status()
        data = r.json()
        asset_name = data.get("label")
        service_id = None
        for attr in data.get("attributes", []):
            name = (attr.get("objectTypeAttribute") or {}).get("name")
            if name == "Service ID":
                vals = attr.get("objectAttributeValues", [])
                if vals:
                    service_id = str(vals[0].get("value"))
        return {
            "object_id": object_id,
            "workspace_id": workspace_id,
            "asset_name": asset_name,
            "service_id": service_id,
        }
    except Exception as e:
        logger.debug("Asset fetch failed for %s: %s", object_id, e)
        return None


# ---------------------------------------------------------------------------
# Async fetchers
# ---------------------------------------------------------------------------

async def _fetch_all_keys_jql(
    client: httpx.AsyncClient,
    jql: str,
    semaphore: asyncio.Semaphore,
    headers: dict,
) -> List[str]:
    """Fetch all issue keys matching JQL using nextPageToken pagination."""
    base_url = settings.jira_base_url.rstrip("/")
    url = f"{base_url}{_JIRA_SEARCH_URL}"
    all_keys: List[str] = []
    next_token: Optional[str] = None

    while True:
        async with semaphore:
            _token = next_token  # capture for closure

            async def _do_page() -> Any:
                payload: Dict[str, Any] = {
                    "jql": jql,
                    "maxResults": PAGE_SIZE,
                    "fields": ["key"],
                }
                if _token:
                    payload["nextPageToken"] = _token
                r = await client.post(url, json=payload, headers=headers, timeout=60.0)
                r.raise_for_status()
                return r.json()

            data = await retry_with_backoff(_do_page, max_retries=3)

        issues = data.get("issues", [])
        all_keys.extend([i["key"] for i in issues])
        next_token = data.get("nextPageToken")
        if not next_token:
            break

    return all_keys


async def _fetch_comments(
    client: httpx.AsyncClient,
    issue_key: str,
    semaphore: asyncio.Semaphore,
    headers: dict,
) -> list:
    base_url = settings.jira_base_url.rstrip("/")
    url = f"{base_url}/rest/api/3/issue/{issue_key}/comment"
    all_comments = []
    start_at = 0

    while True:
        _start = start_at  # capture for closure

        async with semaphore:
            async def _do_page() -> Any:
                r = await client.get(
                    url,
                    params={"startAt": _start, "maxResults": 100, "orderBy": "created"},
                    headers=headers,
                    timeout=30.0,
                )
                r.raise_for_status()
                return r.json()

            data = await retry_with_backoff(_do_page, max_retries=3)

        comments = data.get("comments", [])
        all_comments.extend(comments)
        if data.get("total", 0) <= start_at + len(comments):
            break
        start_at += 100

    return all_comments


async def _fetch_issue_worklogs(
    client: httpx.AsyncClient,
    issue_key: str,
    semaphore: asyncio.Semaphore,
    headers: dict,
) -> list[dict]:
    """
    Fetch ALL worklog entries for an issue, paginated.
    Returns raw Jira worklog objects (not processed).
    """
    base_url = settings.jira_base_url.rstrip("/")
    url = f"{base_url}/rest/api/3/issue/{issue_key}/worklog"
    all_worklogs: list[dict] = []
    start_at = 0

    while True:
        _start = start_at
        async with semaphore:
            async def _do_page() -> Any:
                r = await client.get(
                    url,
                    params={"startAt": _start, "maxResults": 100},
                    headers=headers,
                    timeout=30.0,
                )
                r.raise_for_status()
                return r.json()

            data = await retry_with_backoff(_do_page, max_retries=3)

        worklogs = data.get("worklogs", [])
        all_worklogs.extend(worklogs)
        total = data.get("total", 0)
        if start_at + len(worklogs) >= total or not worklogs:
            break
        start_at += 100

    return all_worklogs


async def fetch_worklog_updates_since(
    client: httpx.AsyncClient,
    since_ms: int,
    semaphore: asyncio.Semaphore,
    headers: dict,
) -> tuple[list[int], int]:
    """
    Walk /rest/api/3/worklog/updated pagination.
    Returns (deduped list of worklog IDs, the 'until' epoch-ms watermark from Jira).
    """
    base_url = settings.jira_base_url.rstrip("/")
    url = f"{base_url}/rest/api/3/worklog/updated"
    all_ids: list[int] = []
    current_since = since_ms
    last_until = since_ms

    while True:
        _since = current_since
        async with semaphore:
            async def _do_page() -> Any:
                r = await client.get(
                    url,
                    params={"since": _since},
                    headers=headers,
                    timeout=30.0,
                )
                r.raise_for_status()
                return r.json()

            data = await retry_with_backoff(_do_page, max_retries=3)

        values = data.get("values", [])
        all_ids.extend(int(v["worklogId"]) for v in values)
        last_until = int(data.get("until", current_since))
        if data.get("lastPage", True):
            break
        current_since = last_until

    deduped = list(dict.fromkeys(all_ids))
    return deduped, last_until


async def fetch_worklog_deletes_since(
    client: httpx.AsyncClient,
    since_ms: int,
    semaphore: asyncio.Semaphore,
    headers: dict,
) -> tuple[list[int], int]:
    """Same shape as fetch_worklog_updates_since but hits /worklog/deleted."""
    base_url = settings.jira_base_url.rstrip("/")
    url = f"{base_url}/rest/api/3/worklog/deleted"
    all_ids: list[int] = []
    current_since = since_ms
    last_until = since_ms

    while True:
        _since = current_since
        async with semaphore:
            async def _do_page() -> Any:
                r = await client.get(
                    url,
                    params={"since": _since},
                    headers=headers,
                    timeout=30.0,
                )
                r.raise_for_status()
                return r.json()

            data = await retry_with_backoff(_do_page, max_retries=3)

        values = data.get("values", [])
        all_ids.extend(int(v["worklogId"]) for v in values)
        last_until = int(data.get("until", current_since))
        if data.get("lastPage", True):
            break
        current_since = last_until

    deduped = list(dict.fromkeys(all_ids))
    return deduped, last_until


async def fetch_worklogs_bulk(
    client: httpx.AsyncClient,
    worklog_ids: list[int],
    semaphore: asyncio.Semaphore,
    headers: dict,
    batch_size: int = 1000,
) -> list[dict]:
    """
    POST /rest/api/3/worklog/list in batches of up to 1000 IDs.
    Returns full worklog objects (with issueId, author, comment, etc.).
    """
    base_url = settings.jira_base_url.rstrip("/")
    url = f"{base_url}/rest/api/3/worklog/list"
    all_worklogs: list[dict] = []

    for i in range(0, len(worklog_ids), batch_size):
        chunk = worklog_ids[i : i + batch_size]
        async with semaphore:
            async def _do_batch() -> Any:
                r = await client.post(
                    url,
                    json={"ids": chunk},
                    headers=headers,
                    timeout=60.0,
                )
                r.raise_for_status()
                return r.json()

            data = await retry_with_backoff(_do_batch, max_retries=3)
        all_worklogs.extend(data if isinstance(data, list) else [])

    return all_worklogs


async def _fetch_one_ticket(
    client: httpx.AsyncClient,
    issue_key: str,
    semaphore: asyncio.Semaphore,
    headers: dict,
    include_worklogs: bool = True,
) -> Optional[dict]:
    """Fetch one ticket: issue + comments + assets (+ optional worklogs)."""
    base_url = settings.jira_base_url.rstrip("/")

    # 1. Main issue (expand changelog for resolved_at)
    async with semaphore:
        url = f"{base_url}/rest/api/3/issue/{issue_key}"

        async def _fetch_issue() -> Any:
            r = await client.get(url, params={"expand": "changelog"}, headers=headers, timeout=30.0)
            r.raise_for_status()
            return r.json()

        issue = await retry_with_backoff(_fetch_issue, max_retries=3)

    # 2. Comments (semaphore inside keeps concurrency bounded)
    comments = await _fetch_comments(client, issue_key, semaphore, headers)

    # 3. Asset hydration (sync calls offloaded to thread)
    raw_assets = (issue.get("fields") or {}).get("customfield_12173")
    if not isinstance(raw_assets, list):
        raw_assets = []
    asset_details = []
    for asset in raw_assets:
        det = await asyncio.to_thread(_fetch_asset_details_sync, asset or {})
        if det:
            asset_details.append(det)

    worklogs: list[dict] = []
    if include_worklogs:
        worklogs = await _fetch_issue_worklogs(client, issue_key, semaphore, headers)

    return _process_issue_to_ticket(issue, comments, asset_details, worklogs)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_project_jql(
    project: str,
    updated_since: Optional[datetime] = None,
    lookback_days: Optional[int] = None,
) -> str:
    """Build project-scoped JQL ordered by updated ASC for resumable backfill."""
    parts = [f"project = {project}"]
    if updated_since:
        iso = updated_since.strftime("%Y-%m-%d %H:%M")
        parts.append(f'updated >= "{iso}"')
    elif lookback_days:
        parts.append(f"updated >= -{lookback_days}d")
    return " AND ".join(parts) + " ORDER BY updated ASC"


async def fetch_ticket_batch(
    client: httpx.AsyncClient,
    keys: List[str],
    semaphore: asyncio.Semaphore,
    headers: dict,
    include_worklogs: bool = True,
) -> List[dict]:
    """Fetch a batch of tickets in parallel. Returns only successful, non-None results."""
    tasks = [
        _fetch_one_ticket(client, key, semaphore, headers, include_worklogs=include_worklogs)
        for key in keys
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    tickets = []
    for key, result in zip(keys, results):
        if isinstance(result, Exception):
            logger.error("Failed to fetch %s: %s", key, result)
        elif result is not None:
            tickets.append(result)
    return tickets
