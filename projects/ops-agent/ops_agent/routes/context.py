import logging
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..db import get_pool
from ..context.t_context import build_t_context

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[1] / "templates"))


@router.get("/tickets/{issue_key}/related", response_class=HTMLResponse)
async def related_panel(request: Request, issue_key: str):
    pool = await get_pool()
    try:
        ctx = await build_t_context(pool, issue_key)
    except Exception as e:
        logger.exception("related_panel failed for %s", issue_key)
        return templates.TemplateResponse(
            request,
            "related_panel.html",
            {"issue_key": issue_key, "error": str(e), "ctx": None},
        )

    if ctx.get("error") == "ticket_not_found":
        return HTMLResponse("<p class=\"muted\">Ticket not found.</p>", status_code=404)

    return templates.TemplateResponse(
        request,
        "related_panel.html",
        {"issue_key": issue_key, "error": None, "ctx": ctx},
    )
