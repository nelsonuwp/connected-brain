import asyncio
import json
import logging
from datetime import timezone
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from ..db import get_distinct_statuses, get_pool, get_thread, get_ticket, get_ticket_assets, list_tickets
from ..jinja_tools import familiarity_ring_filter, sla_remaining_filter
from ..personas import load_personas, persona_system_prompt
from ..context.t_context import _fusion_service_labels, _parse_service_ids

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[1] / "templates"))


def _localtime(dt) -> str:
    if dt is None:
        return "—"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone().strftime("%b %d %H:%M")


templates.env.filters["localtime"] = _localtime
templates.env.filters["familiarity_ring"] = familiarity_ring_filter
templates.env.filters["sla_remaining"] = sla_remaining_filter


@router.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/tickets")


@router.get("/tickets", response_class=HTMLResponse)
async def ticket_list(
    request: Request,
    status: Optional[str] = None,
    customer_originated: Optional[str] = None,
    q: Optional[str] = None,
):
    pool = await get_pool()
    async with pool.acquire() as conn:
        customer_bool: Optional[bool] = None
        if customer_originated == "1":
            customer_bool = True
        elif customer_originated == "0":
            customer_bool = False

        tickets = await list_tickets(
            conn,
            limit=100,
            customer_originated=customer_bool,
            status=status or None,
            search=q or None,
        )
        statuses = await get_distinct_statuses(conn)

    return templates.TemplateResponse(
        request,
        "ticket_list.html",
        {
            "tickets": tickets,
            "statuses": statuses,
            "filter_status": status or "",
            "filter_customer": customer_originated or "",
            "filter_q": q or "",
        },
    )


@router.get("/tickets/{issue_key}", response_class=HTMLResponse)
async def ticket_detail(request: Request, issue_key: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        ticket = await get_ticket(conn, issue_key)
        if not ticket:
            return HTMLResponse("<h2>Ticket not found</h2>", status_code=404)
        thread = await get_thread(conn, issue_key)
        assets = await get_ticket_assets(conn, issue_key)

    # Enrich assets with Fusion service labels (nickname, product name, line of business).
    # Best-effort: if Fusion is unavailable the assets still render with Postgres-only data.
    service_ids = _parse_service_ids(assets)
    if service_ids:
        try:
            label_map = await asyncio.to_thread(_fusion_service_labels, service_ids)
            for a in assets:
                sid = a.get("service_id")
                if sid is None:
                    continue
                info = label_map.get(int(sid))
                if not info:
                    continue
                a["product_name"] = info.get("product_name") or None
                a["product_nickname"] = info.get("product_nickname") or None
                a["pl_name"] = info.get("pl_name") or None
                a["pl_abbr"] = info.get("pl_abbr") or None
                a["fusion_company_name"] = info.get("fusion_company_name") or None
        except Exception:
            logger.exception("Fusion asset label enrichment failed (non-fatal) for %s", issue_key)

    personas = load_personas()
    persona_rows = [{"slug": p.slug, "label": p.label} for p in personas.values()]
    defaults = {p.slug: persona_system_prompt(p) for p in personas.values()}
    default_slug = persona_rows[0]["slug"] if persona_rows else "l2_support"

    return templates.TemplateResponse(
        request,
        "ticket_detail.html",
        {
            "ticket": ticket,
            "thread": thread,
            "assets": assets,
            "persona_rows": persona_rows,
            "personas_json": json.dumps(defaults),
            "default_persona_slug": default_slug,
        },
    )
