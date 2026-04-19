import logging
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from ..classifier import classify
from ..db import get_distinct_statuses, get_pool, get_thread, get_ticket, get_ticket_assets, list_tickets

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[1] / "templates"))


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

    pattern_slug = classify(ticket)
    pattern_display = None
    if pattern_slug:
        from ..patterns import REGISTERED_PATTERNS
        p = next((p for p in REGISTERED_PATTERNS if p.slug == pattern_slug), None)
        if p:
            pattern_display = p.display_name

    return templates.TemplateResponse(
        request,
        "ticket_detail.html",
        {
            "ticket": ticket,
            "thread": thread,
            "assets": assets,
            "pattern_slug": pattern_slug,
            "pattern_display": pattern_display,
        },
    )
