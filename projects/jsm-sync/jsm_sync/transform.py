"""
Transform layer: converts a processed Jira ticket dict (from jira_client._process_issue_to_ticket)
into DB-ready records for db.py upsert functions.

No side effects. Fully testable without hitting Jira or Postgres.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TransformedTicket:
    ticket_row: dict
    users: list[dict]
    organization: Optional[dict]
    thread_events: list[dict]
    assets: list[dict]
    ticket_asset_links: list[tuple[str, str]]


def transform_ticket(raw: dict) -> TransformedTicket:
    """Convert a processed Jira ticket dict into DB-ready records."""
    issue_key = raw["issue_key"]

    # --- ticket_row ---
    sla_fr = raw.get("sla_first_response")
    sla_res = raw.get("sla_resolution")

    ticket_row = {
        "issue_key": issue_key,
        "summary": raw.get("summary", ""),
        "description": raw.get("description", ""),
        "status": raw.get("status", "Unknown"),
        "priority": raw.get("priority"),
        "issue_type": raw.get("issue_type"),
        "request_type": raw.get("request_type"),
        "is_customer_originated": raw.get("is_customer_originated", False),
        "creator_account_id": (raw.get("creator") or {}).get("account_id"),
        "reporter_account_id": (raw.get("reporter") or {}).get("account_id"),
        "assignee_account_id": (raw.get("assignee") or {}).get("account_id"),
        "jira_org_id": raw.get("jira_org_id"),
        "ocean_client_id": raw.get("ocean_client_id"),
        "labels": raw.get("labels") or [],
        "sla_first_response_breached": sla_fr["breached"] if sla_fr else None,
        "sla_first_response_elapsed_s": sla_fr["elapsed_seconds"] if sla_fr else None,
        "sla_first_response_threshold_s": sla_fr["threshold_seconds"] if sla_fr else None,
        "sla_resolution_breached": sla_res["breached"] if sla_res else None,
        "sla_resolution_elapsed_s": sla_res["elapsed_seconds"] if sla_res else None,
        "sla_resolution_threshold_s": sla_res["threshold_seconds"] if sla_res else None,
        "created_at": raw["created_at"],
        "updated_at": raw["updated_at"],
        "resolved_at": raw.get("resolved_at"),
    }

    # --- users (creator + reporter + assignee + comment authors, deduplicated) ---
    users_by_id: dict[str, dict] = {}
    for person_key in ("creator", "reporter", "assignee"):
        person = raw.get(person_key)
        if person and person.get("account_id"):
            aid = person["account_id"]
            if aid not in users_by_id:
                users_by_id[aid] = person
    for event in raw.get("thread_events", []):
        aid = event.get("author_account_id")
        if aid and aid not in users_by_id:
            users_by_id[aid] = {
                "account_id": aid,
                "display_name": event.get("author") or "",
                "email": event.get("author_email"),
                "role": event.get("role", "Unknown"),
                "account_type": event.get("account_type"),
            }
    users = list(users_by_id.values())

    # --- organization ---
    organization = None
    if raw.get("jira_org_id"):
        organization = {
            "jira_org_id": raw["jira_org_id"],
            "name": raw.get("jira_org_name") or raw["jira_org_id"],
            "ocean_client_id": raw.get("ocean_client_id"),
        }

    # --- thread_events ---
    thread_events = []
    for event in raw.get("thread_events", []):
        event_id = event.get("id")
        if not event_id:
            continue
        thread_events.append({
            "id": str(event_id),
            "issue_key": issue_key,
            "kind": event.get("kind", "comment"),
            "author_account_id": event.get("author_account_id"),
            "is_public": event.get("is_public"),
            "body": event.get("body", ""),
            "created_at": event["created_at"],
        })

    # --- assets + ticket_asset_links ---
    assets = []
    ticket_asset_links = []
    for asset in raw.get("assets", []):
        oid = asset.get("object_id")
        if not oid:
            continue
        assets.append({
            "object_id": oid,
            "workspace_id": asset.get("workspace_id", ""),
            "asset_name": asset.get("asset_name"),
            "service_id": asset.get("service_id"),
        })
        ticket_asset_links.append((issue_key, oid))

    return TransformedTicket(
        ticket_row=ticket_row,
        users=users,
        organization=organization,
        thread_events=thread_events,
        assets=assets,
        ticket_asset_links=ticket_asset_links,
    )
