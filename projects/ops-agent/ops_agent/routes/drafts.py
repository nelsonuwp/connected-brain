import logging
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..db import get_pool, mark_draft_used
from ..drafter import draft_for_ticket

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[1] / "templates"))


@router.post("/tickets/{issue_key}/draft", response_class=HTMLResponse)
async def generate_draft(request: Request, issue_key: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        try:
            result = await draft_for_ticket(conn, issue_key)
        except Exception as e:
            logger.exception("Draft generation failed for %s", issue_key)
            return templates.TemplateResponse(
                "draft_preview.html",
                {
                    "request": request,
                    "status": "error",
                    "issue_key": issue_key,
                    "message": f"Draft generation failed: {e}",
                },
            )

    return templates.TemplateResponse(
        "draft_preview.html",
        {"request": request, **result},
    )


@router.post("/drafts/{draft_id}/used", response_class=HTMLResponse)
async def mark_used(draft_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await mark_draft_used(conn, draft_id)
    return HTMLResponse("", status_code=204)
