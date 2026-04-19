import logging
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..context.familiarity import build_familiarity_tooltip_context
from ..db import get_pool
from ..jinja_tools import familiarity_ring_filter

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[1] / "templates"))
templates.env.filters["familiarity_ring"] = familiarity_ring_filter


@router.get("/tickets/{issue_key}/familiarity/tooltip", response_class=HTMLResponse)
async def familiarity_tooltip(request: Request, issue_key: str):
    pool = await get_pool()
    try:
        ctx = await build_familiarity_tooltip_context(pool, issue_key.upper())
    except Exception as e:
        logger.exception("familiarity_tooltip failed for %s", issue_key)
        return HTMLResponse(
            f'<p class="related-warn small">Could not load familiarity: {e}</p>',
            status_code=500,
        )

    if ctx.get("error") == "not_found":
        return HTMLResponse("<p class=\"muted\">Ticket not found.</p>", status_code=404)

    return templates.TemplateResponse(
        request,
        "familiarity_tooltip.html",
        {"ctx": ctx},
    )
