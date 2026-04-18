"""
Jira client: async fetch with Scout (total count) -> Plan (offsets) -> Gather (semaphore 5, retry on 429/5xx).
Writes Unified Source Artifact via save_source_artifact (single write, no silent failure).
"""

import asyncio
import logging
import base64
import json
import os
from datetime import datetime, timezone, date
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Optional, TypeVar

import httpx
import pandas as pd
from dateutil import parser

from core.utils import (
    log,
    make_source_object,
    record_count_from_data,
    save_source_artifact,
)

T = TypeVar("T")


async def retry_with_backoff(
    func: Callable[[], Awaitable[T]],
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
) -> T:
    """
    Retry async function with exponential backoff for rate limits and transient errors.
    Handles: 429 (respects Retry-After if numeric), 5xx, timeout, network errors.
    """
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
                    log("⚠️", f"Rate limited (429), retrying in {wait_time:.1f}s (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(wait_time)
                    delay = min(delay * backoff_factor, max_delay)
                    continue
                log("✗", f"All {max_retries} retry attempts exhausted (429)")
                raise
            elif 500 <= e.response.status_code < 600:
                if attempt < max_retries:
                    wait_time = min(delay, max_delay)
                    log("⚠️", f"Server error {e.response.status_code}, retrying in {wait_time:.1f}s (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(wait_time)
                    delay = min(delay * backoff_factor, max_delay)
                    continue
                log("✗", f"All {max_retries} retry attempts exhausted ({e.response.status_code})")
                raise
            raise
        except (httpx.TimeoutException, httpx.NetworkError) as e:
            last_exception = e
            if attempt < max_retries:
                wait_time = min(delay, max_delay)
                log("⚠️", f"Network/timeout error, retrying in {wait_time:.1f}s (attempt {attempt + 1}/{max_retries})")
                await asyncio.sleep(wait_time)
                delay = min(delay * backoff_factor, max_delay)
                continue
            log("✗", f"All {max_retries} retry attempts exhausted (network/timeout)")
            raise

    log("✗", f"All {max_retries} retry attempts exhausted")
    raise last_exception  # type: ignore[misc]

# --- CONFIGURATION ---
logger = logging.getLogger(__name__)
jira_base_url = os.getenv("JIRA_BASE_URL")
jira_username = os.getenv("JIRA_USERNAME")
jira_api_token = os.getenv("JIRA_API_TOKEN")

if jira_base_url:
    jira_base_url = jira_base_url.rstrip("/")

JQL_FIELD_ALIAS = '"CustomerID[Number]"'
PAGE_SIZE = 100
# Reduced from 10 to lower request rate and avoid Jira 429 rate limits.
SEMAPHORE_LIMIT = 5

# Asset API (JSM) - sync session for fetch_organization_users
try:
    basic_auth_string = f"{jira_username}:{jira_api_token}"
    basic_auth_b64 = (
        base64.b64encode(basic_auth_string.encode("utf-8")).decode("utf-8")
        if jira_username
        else ""
    )
except Exception:
    basic_auth_b64 = ""
jsm_assets_headers = {
    "Accept": "application/json",
    "Authorization": f"Basic {basic_auth_b64}",
}


def _auth_headers() -> Dict[str, str]:
    if not jira_username or not jira_api_token:
        return {}
    b64 = base64.b64encode(f"{jira_username}:{jira_api_token}".encode()).decode()
    return {"Authorization": f"Basic {b64}", "Content-Type": "application/json"}


# --- HELPERS (sync, used from async after fetch) ---
def parse_adf_to_text(adf):
    if not adf or not isinstance(adf, dict) or "content" not in adf:
        return str(adf) if adf else ""
    parts = []
    for node in adf["content"]:
        if node.get("type") == "text":
            parts.append(node.get("text", ""))
        elif "content" in node:
            parts.append(parse_adf_to_text(node))
    return " ".join(parts)


# --- AUTOMATION CONFIG LOADER ---
_AUTOMATION_CONFIG = None


def _load_automation_config():
    """
    Load automation users config from JSON file (cached after first load).
    Config file is in project root: config/jira_automation_users.json
    """
    global _AUTOMATION_CONFIG

    if _AUTOMATION_CONFIG is not None:
        return _AUTOMATION_CONFIG

    project_root = Path(__file__).resolve().parent.parent.parent
    config_path = project_root / "config" / "jira_automation_users.json"

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            _AUTOMATION_CONFIG = json.load(f)
            log("   ", f"Loaded automation config from {config_path}")
    except FileNotFoundError:
        log("   ", f"Config file not found at {config_path}, using defaults")
        _AUTOMATION_CONFIG = {
            "email_patterns": [
                "noreply@", "no-reply@", "-scraper@", "automation@",
                "notifications.", "alerts@", "monitoring@", "veeam", "alertlogic",
            ],
            "specific_users": {
                "by_email": [],
                "by_display_name": [],
            },
        }
    except json.JSONDecodeError as e:
        log("   ", f"Invalid JSON in config file: {e}, using defaults")
        _AUTOMATION_CONFIG = {
            "email_patterns": [
                "noreply@", "no-reply@", "-scraper@", "automation@",
                "notifications.", "alerts@", "monitoring@", "veeam", "alertlogic",
            ],
            "specific_users": {
                "by_email": [],
                "by_display_name": [],
            },
        }

    return _AUTOMATION_CONFIG


def determine_role(author_obj):
    """
    Determine role (Automation, Customer, or Aptum) based on:
    1. Email substring patterns (e.g., noreply@, automation@)
    2. Specific emails from config (e.g., bu10atl@cogecopeer1.net)
    3. Display names from config (e.g., "PagerDuty", "Automation for Jira")
    4. Jira accountType as final fallback

    Returns: "Automation", "Customer", "Aptum", or "Unknown"
    """
    if not author_obj or not isinstance(author_obj, dict):
        return "Unknown"

    config = _load_automation_config()

    email = (author_obj.get("emailAddress") or "").strip().lower()
    email_patterns = config.get("email_patterns", [])
    if email and any(pattern in email for pattern in email_patterns):
        return "Automation"

    specific_emails = config.get("specific_users", {}).get("by_email", [])
    normalized_emails = [e.strip().lower() for e in specific_emails]
    if email and email in normalized_emails:
        return "Automation"

    display_name = (author_obj.get("displayName") or "").strip()
    specific_names = config.get("specific_users", {}).get("by_display_name", [])
    normalized_names = {name.strip().lower() for name in specific_names}
    if display_name and display_name.lower() in normalized_names:
        return "Automation"

    acc_type = author_obj.get("accountType", "unknown")
    return "Customer" if acc_type == "customer" else "Aptum"


def create_history_trail(issue, comments):
    events = []
    for comment in comments:
        try:
            created = parser.parse(comment.get("created"))
        except (ValueError, TypeError):
            created = datetime.min.replace(tzinfo=timezone.utc)
        author = comment.get("author", {})
        role = determine_role(author)
        text = " ".join(parse_adf_to_text(comment.get("body")).split())
        if len(text) > 800:
            text = text[:800] + "... (truncated)"
        events.append({
            "date": created.strftime("%Y-%m-%d"),
            "role": role,
            "author": author.get("displayName", "Unknown"),
            "id": author.get("accountId"),
            "type": "Comment",
            "details": text,
        })
    return events


def extract_sla_details(sla_field):
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


_CLOSED_STATUSES = {"Done", "Resolved", "Closed", "Complete", "Completed"}


def _get_closure_info(changelog: dict) -> dict:
    """
    Extract closure info from issue changelog: who closed and when.
    Walks changelog.histories in reverse, finds first status change to a closed status.
    Returns dict with closed_date, closed_by (user object), previous_status, closure_status.
    """
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


def _process_issue_to_ticket(issue: dict, comments: list, time_entries: list, asset_details: list) -> Optional[dict]:
    """Build one ticket dict from raw issue + comments + worklog + assets."""
    key = issue.get("key")
    fields = issue.get("fields") or {}
    jira_org_id = None
    jira_org_name = None
    org_field = fields.get("customfield_11100")
    if org_field and isinstance(org_field, list) and len(org_field) > 0:
        first_org = org_field[0]
        if isinstance(first_org, dict):
            jira_org_id = first_org.get("id")
            jira_org_name = first_org.get("name")

    req_type_field = fields.get("customfield_11200")
    request_type = "Unknown Request Type"
    if isinstance(req_type_field, dict):
        rt_obj = req_type_field.get("requestType")
        if isinstance(rt_obj, dict):
            request_type = rt_obj.get("name", "Unknown")
    elif isinstance(req_type_field, str):
        request_type = req_type_field

    creator_field = fields.get("creator") or {}
    reporter_field = fields.get("reporter") or {}
    assignee_field = fields.get("assignee") or {}
    status_field = fields.get("status") or {}

    closure = _get_closure_info(issue.get("changelog") or {})

    return {
        "issue_key": key,
        "summary": fields.get("summary", ""),
        "description": parse_adf_to_text(fields.get("description")),
        "history_trail": create_history_trail(issue, comments),
        "status": status_field.get("name", "Unknown"),
        "priority": (fields.get("priority") or {}).get("name", "Unknown"),
        "current_assignee": assignee_field.get("displayName", "Unassigned"),
        "request_type": request_type,
        "creator": {
            "name": creator_field.get("displayName"),
            "email": creator_field.get("emailAddress"),
            "role": determine_role(creator_field),
            "id": creator_field.get("accountId"),
        },
        "reporter": {
            "name": reporter_field.get("displayName"),
            "email": reporter_field.get("emailAddress"),
            "role": determine_role(reporter_field),
            "id": reporter_field.get("accountId"),
        },
        "created_date_time": fields.get("created"),
        "updated_date_time": fields.get("updated"),
        "closed_date_time": closure.get("closed_date"),
        "closed_by": closure.get("closed_by"),
        "time_entries": time_entries,
        "asset_service_ids": asset_details,
        "sla_resolution": extract_sla_details(fields.get("customfield_11311")),
        "sla_first_response": extract_sla_details(fields.get("customfield_11312")),
        "jira_org_id": jira_org_id,
        "jira_org_name": jira_org_name,
    }


# --- ASYNC SCOUT / PLAN / GATHER ---
# Jira Cloud deprecated POST /rest/api/3/search (410 Gone). Use /rest/api/3/search/jql.
# New API uses nextPageToken for pagination (no startAt).
_JIRA_SEARCH_URL = "/rest/api/3/search/jql"


async def _fetch_all_keys_jql(
    client: httpx.AsyncClient,
    jql: str,
    semaphore: asyncio.Semaphore,
    headers: dict,
) -> List[str]:
    """Fetch all issue keys matching JQL using nextPageToken pagination (no startAt)."""
    url = f"{jira_base_url}{_JIRA_SEARCH_URL}"
    all_keys: List[str] = []
    next_token: Optional[str] = None
    while True:
        async with semaphore:
            async def _do_page() -> Any:
                payload: Dict[str, Any] = {"jql": jql, "maxResults": PAGE_SIZE, "fields": ["key"]}
                if next_token:
                    payload["nextPageToken"] = next_token
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


async def _fetch_comments(client: httpx.AsyncClient, issue_key: str, semaphore: asyncio.Semaphore, headers: dict) -> list:
    async with semaphore:
        url = f"{jira_base_url}/rest/api/3/issue/{issue_key}/comment"
        all_comments = []
        start_at = 0
        while True:
            async def _do_page() -> Any:
                r = await client.get(
                    url,
                    params={"startAt": start_at, "maxResults": 100, "orderBy": "created"},
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


async def _fetch_worklog(client: httpx.AsyncClient, issue_key: str, semaphore: asyncio.Semaphore, headers: dict) -> list:
    async with semaphore:
        url = f"{jira_base_url}/rest/api/3/issue/{issue_key}/worklog"

        async def _do_fetch() -> Any:
            r = await client.get(url, headers=headers, timeout=30.0)
            r.raise_for_status()
            return r.json()

        data = await retry_with_backoff(_do_fetch, max_retries=3)
        worklogs = data.get("worklogs", [])
        agg_map = {}
        for log_entry in worklogs:
            author = log_entry.get("author")
            if not author:
                continue
            account_id = author.get("accountId") or author.get("displayName")
            seconds = log_entry.get("timeSpentSeconds", 0)
            if account_id not in agg_map:
                agg_map[account_id] = {
                    "name": author.get("displayName", "Unknown"),
                    "email": author.get("emailAddress", ""),
                    "total_seconds": 0,
                }
            agg_map[account_id]["total_seconds"] += seconds
        return [
            {"name": v["name"], "email": v["email"], "total_seconds": v["total_seconds"], "total_hours": round(v["total_seconds"] / 3600, 2)}
            for v in agg_map.values()
        ]


def _fetch_asset_details_sync(asset_data: dict) -> Optional[dict]:
    """JSM Assets: sync request (external Atlassian API). Keep simple."""
    import requests
    workspace_id = asset_data.get("workspaceId")
    object_id = asset_data.get("objectId")
    if not workspace_id or not object_id:
        return None
    url = f"https://api.atlassian.com/jsm/assets/workspace/{workspace_id}/v1/object/{object_id}"
    try:
        r = requests.get(url, headers=jsm_assets_headers, timeout=15)
        r.raise_for_status()
        data = r.json()
        asset_name = data.get("label", "Unknown Asset")
        for attr in data.get("attributes", []):
            name = attr.get("objectTypeAttribute", {}).get("name")
            if name == "Service ID":
                vals = attr.get("objectAttributeValues", [])
                if vals:
                    return {"id": str(vals[0].get("value")), "name": asset_name}
        return {"id": object_id, "name": asset_name, "is_service_id": False}
    except Exception:
        return None


async def _fetch_one_ticket(
    client: httpx.AsyncClient,
    issue_key: str,
    semaphore: asyncio.Semaphore,
    headers: dict,
) -> Optional[dict]:
    # 1. Get the main issue data first (expand=changelog for closed_date / closed_by)
    async with semaphore:
        url = f"{jira_base_url}/rest/api/3/issue/{issue_key}"

        async def _fetch_issue() -> Any:
            r = await client.get(url, params={"expand": "changelog"}, headers=headers, timeout=30.0)
            r.raise_for_status()
            return r.json()

        issue = await retry_with_backoff(_fetch_issue, max_retries=3)

    # 2. Fire comments and worklogs IN PARALLEL (semaphore inside each keeps concurrency bounded)
    comments_task = _fetch_comments(client, issue_key, semaphore, headers)
    worklog_task = _fetch_worklog(client, issue_key, semaphore, headers)
    comments, time_entries = await asyncio.gather(comments_task, worklog_task)

    raw_assets = (issue.get("fields") or {}).get("customfield_12173")
    if not isinstance(raw_assets, list):
        raw_assets = []
    asset_details = []
    for asset in raw_assets:
        det = await asyncio.to_thread(_fetch_asset_details_sync, asset or {})
        if det:
            asset_details.append(det)

    return _process_issue_to_ticket(issue, comments, time_entries, asset_details)


async def fetch_jira_data(
    client: httpx.AsyncClient,
    run_id: str,
    company_id: str,
    start_date: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Async fetch: Scout total -> Plan offsets -> Gather pages + issue details.
    Writes source_jira.json via save_source_artifact in finally (single write).
    Returns { "objects", "status", "error", "collected_at" } for _map_to_legacy_envelope.
    """
    objects: Optional[Dict[str, Any]] = None
    status = "fail"
    error: Optional[Dict[str, Any]] = None
    collected_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    if not jira_base_url:
        status = "skipped"
        error = {"type": "ConfigError", "message": "Missing JIRA_BASE_URL", "retryable": False}
        save_source_artifact(run_id, "jira", company_id, None, status, error)
        return {"objects": None, "status": status, "error": error, "collected_at": collected_at}

    if not jira_username or not jira_api_token:
        status = "skipped"
        error = {"type": "ConfigError", "message": "Missing JIRA_USERNAME/JIRA_API_TOKEN", "retryable": False}
        save_source_artifact(run_id, "jira", company_id, None, status, error)
        return {"objects": None, "status": status, "error": error, "collected_at": collected_at}

    headers = _auth_headers()
    # Lookback from env (default 365 for trend analysis); minimum 90 days
    try:
        days = int(os.getenv("JIRA_LOOKBACK_DAYS", "365"))
        if days < 90:
            logger.warning("JIRA_LOOKBACK_DAYS=%s too low, using 90", days)
            days = 90
    except (ValueError, TypeError):
        logger.warning("Invalid JIRA_LOOKBACK_DAYS, using default 365")
        days = 365
    if start_date:
        if isinstance(start_date, str) and start_date.strip().endswith("d"):
            try:
                days = int(start_date.strip()[:-1])
            except ValueError:
                pass
        elif hasattr(start_date, "strftime"):
            try:
                from datetime import timedelta
                delta = datetime.now(timezone.utc) - start_date
                days = max(1, delta.days)
            except Exception:
                pass
    jql = f'{JQL_FIELD_ALIAS} = {company_id} AND createdDate >= -{days}d ORDER BY created DESC'

    try:
        semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)
        all_keys = await _fetch_all_keys_jql(client, jql, semaphore, headers)

        log("   ", f"Jira: found {len(all_keys)} tickets. Fetching details...")
        # Optional: small delay to avoid immediate rate limit after key listing when many tickets
        if len(all_keys) > 100:
            await asyncio.sleep(0.5)
        tasks = [_fetch_one_ticket(client, key, semaphore, headers) for key in all_keys]
        results = await asyncio.gather(*tasks)
        tickets = [t for t in results if t]

        jira_org_id = tickets[0].get("jira_org_id") if tickets else None
        record_count = record_count_from_data(tickets)
        objects = {
            "tickets": make_source_object("success", record_count, None, tickets),
            "meta": make_source_object("success", 1 if jira_org_id else 0, None, jira_org_id),
        }
        status = "success"
        error = None
    except httpx.HTTPStatusError as e:
        status = "fail"
        error = {
            "type": "HTTPStatusError",
            "message": f"HTTP {e.response.status_code}: {str(e)}",
            "retryable": e.response.status_code in (429, 500, 502, 503, 504),
        }
        objects = None
        log("✗", f"Jira fetch failed: {error['message']}")
    except Exception as e:
        status = "fail"
        error = {"type": type(e).__name__, "message": str(e), "retryable": True}
        objects = None
        log("✗", f"Jira fetch failed: {error['message']}")
    finally:
        save_source_artifact(run_id, "jira", company_id, objects, status, error)

    return {"objects": objects, "status": status, "error": error, "collected_at": collected_at}


def fetch_jira_data_sync(client_id, start_date=None):
    """
    Legacy sync entrypoint for callers that do not use the async pipeline.
    Uses requests and ThreadPoolExecutor (no artifact write).
    """
    import requests
    from requests.auth import HTTPBasicAuth
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from urllib3.util.retry import Retry
    from requests.adapters import HTTPAdapter

    def create_session():
        if not jira_username or not jira_api_token:
            return None
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1), pool_connections=50, pool_maxsize=50)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.auth = HTTPBasicAuth(jira_username, jira_api_token)
        return session

    session = create_session()
    extracted_at = datetime.now(timezone.utc).isoformat()
    if not jira_base_url:
        return {"source": "jira", "status": "skipped", "extracted_at": extracted_at, "data": {}, "error": "Missing JIRA_BASE_URL"}
    if not session:
        return {"source": "jira", "status": "skipped", "extracted_at": extracted_at, "data": {}, "error": "Missing credentials"}

    if not start_date:
        try:
            lookback_days = int(os.getenv("JIRA_LOOKBACK_DAYS", "365"))
            if lookback_days < 90:
                lookback_days = 90
        except (ValueError, TypeError):
            lookback_days = 365
        start_date_str = (datetime.now() - pd.Timedelta(days=lookback_days)).strftime("%Y-%m-%d")
    else:
        start_date_str = start_date.strftime("%Y-%m-%d") if hasattr(start_date, "strftime") else str(start_date)
    formatted_date = start_date_str.replace("-", "/")
    jql = f'{JQL_FIELD_ALIAS} = {client_id} AND (created >= "{formatted_date}" OR updated >= "{formatted_date}") ORDER BY created DESC'
    url = f"{jira_base_url}/rest/api/3/search/jql"
    all_keys = []
    next_token = None
    while True:
        payload = {"jql": jql, "fields": ["key"], "maxResults": 100}
        if next_token:
            payload["nextPageToken"] = next_token
        try:
            r = session.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
            r.raise_for_status()
            data = r.json()
        except Exception:
            break
        issues = data.get("issues", [])
        if not issues:
            break
        all_keys.extend([i["key"] for i in issues])
        next_token = data.get("nextPageToken")
        if not next_token:
            break

    def make_request_with_retry(method, u, **kwargs):
        try:
            return session.request(method, u, **kwargs)
        except Exception:
            return None

    def get_issue_comments(issue_key):
        comments = []
        start_at = 0
        comment_url = f"{jira_base_url}/rest/api/3/issue/{issue_key}/comment"
        while True:
            resp = make_request_with_retry("GET", comment_url, params={"startAt": start_at, "maxResults": 100, "orderBy": "created"})
            if not resp:
                return []
            d = resp.json()
            comments.extend(d.get("comments", []))
            if d.get("total", 0) <= start_at + len(d.get("comments", [])):
                break
            start_at += 100
        return comments

    def get_worklog_aggregated(issue_key):
        resp = make_request_with_retry("GET", f"{jira_base_url}/rest/api/3/issue/{issue_key}/worklog")
        if not resp:
            return []
        worklogs = resp.json().get("worklogs", [])
        agg_map = {}
        for log_entry in worklogs:
            author = log_entry.get("author")
            if not author:
                continue
            aid = author.get("accountId") or author.get("displayName")
            sec = log_entry.get("timeSpentSeconds", 0)
            if aid not in agg_map:
                agg_map[aid] = {"name": author.get("displayName", "Unknown"), "email": author.get("emailAddress", ""), "total_seconds": 0}
            agg_map[aid]["total_seconds"] += sec
        return [{"name": v["name"], "email": v["email"], "total_seconds": v["total_seconds"], "total_hours": round(v["total_seconds"] / 3600, 2)} for v in agg_map.values()]

    results = []
    if all_keys:
        def process_one(key):
            resp = make_request_with_retry("GET", f"{jira_base_url}/rest/api/3/issue/{key}", params={"expand": "changelog"})
            if not resp:
                return None
            issue = resp.json()
            comments = get_issue_comments(key)
            time_entries = get_worklog_aggregated(key)
            raw_assets = (issue.get("fields") or {}).get("customfield_12173") or []
            asset_details = []
            for asset in raw_assets:
                det = _fetch_asset_details_sync(asset or {})
                if det:
                    asset_details.append(det)
            return _process_issue_to_ticket(issue, comments, time_entries, asset_details)

        with ThreadPoolExecutor(max_workers=20) as executor:
            for fut in as_completed(executor.submit(process_one, k) for k in all_keys):
                try:
                    res = fut.result()
                    if res:
                        results.append(res)
                except Exception:
                    pass

    jira_org_id = results[0].get("jira_org_id") if results else None
    return {
        "source": "jira",
        "status": "success",
        "extracted_at": extracted_at,
        "data": {"tickets": results, "jira_org_id": jira_org_id},
        "error": None,
    }


def fetch_organization_users(org_id: str) -> dict:
    """Sync: fetch Jira Service Management org users (uses requests session)."""
    import requests
    extracted_at = datetime.now(timezone.utc).isoformat()
    if not jira_base_url:
        return {"source": "jira_org_users", "status": "skipped", "extracted_at": extracted_at, "data": {}, "error": "Missing JIRA_BASE_URL"}
    if not jira_username or not jira_api_token:
        return {"source": "jira_org_users", "status": "skipped", "extracted_at": extracted_at, "data": {}, "error": "Missing credentials"}
    session = requests.Session()
    session.auth = (jira_username, jira_api_token)
    users = []
    start = 0
    limit = 50
    headers = {"X-ExperimentalApi": "true"}
    while True:
        url = f"{jira_base_url}/rest/servicedeskapi/organization/{org_id}/user"
        r = session.get(url, params={"start": start, "limit": limit}, headers=headers)
        if not r.ok:
            break
        data = r.json()
        users.extend(data.get("values", []))
        if data.get("isLastPage", True):
            break
        start += limit
    return {"source": "jira_org_users", "status": "success", "extracted_at": extracted_at, "data": {"org_id": org_id, "users": users}, "error": None}
