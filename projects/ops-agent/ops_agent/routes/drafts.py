import logging
from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..db import get_pool, mark_draft_used
from ..generators import draft_fix_suggestion, draft_internal_comment, draft_public_comment

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[1] / "templates"))


def _err(request: Request, issue_key: str, message: str):
    return templates.TemplateResponse(
        request,
        "draft_preview.html",
        {"status": "error", "issue_key": issue_key, "message": message, "draft_type": None},
    )


@router.post("/tickets/{issue_key}/draft/fix", response_class=HTMLResponse)
async def generate_fix(request: Request, issue_key: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        try:
            result = await draft_fix_suggestion(conn, pool, issue_key)
        except Exception as e:
            logger.exception("fix draft failed for %s", issue_key)
            return _err(request, issue_key, str(e))

    return templates.TemplateResponse(request, "draft_preview.html", result)


@router.post("/tickets/{issue_key}/draft/internal", response_class=HTMLResponse)
async def generate_internal(request: Request, issue_key: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        try:
            result = await draft_internal_comment(conn, pool, issue_key)
        except Exception as e:
            logger.exception("internal draft failed for %s", issue_key)
            return _err(request, issue_key, str(e))

    return templates.TemplateResponse(request, "draft_preview.html", result)


@router.post("/tickets/{issue_key}/draft/public", response_class=HTMLResponse)
async def generate_public(
    request: Request,
    issue_key: str,
    persona_slug: str = Form(...),
    system_prompt: str = Form(""),
):
    pool = await get_pool()
    async with pool.acquire() as conn:
        try:
            result = await draft_public_comment(
                conn,
                pool,
                issue_key,
                persona_slug.strip(),
                system_prompt_override=system_prompt.strip() or None,
            )
        except Exception as e:
            logger.exception("public draft failed for %s", issue_key)
            return _err(request, issue_key, str(e))

    return templates.TemplateResponse(request, "draft_preview.html", result)


@router.post("/drafts/{draft_id}/used", response_class=HTMLResponse)
async def mark_used(draft_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await mark_draft_used(conn, draft_id)
    return HTMLResponse("", status_code=204)
