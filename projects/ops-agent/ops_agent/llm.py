"""
Async OpenRouter wrapper for ops-agent.
Ported from projects/_reference/clients/openrouter.py — async httpx instead of requests.

Uses MODEL_WORKHORSE + TEMPERATURE_WORKHORSE from the root .env via settings.
"""

import logging
import time
from typing import Optional

import httpx

from .config import settings

logger = logging.getLogger(__name__)

_OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
_RETRY_STATUSES = (429, 500, 502, 503, 504)


async def generate_draft(system_prompt: str, user_prompt: str) -> dict:
    """
    Call OpenRouter with the workhorse model.

    Returns:
        {text, input_tokens, output_tokens, model}

    Raises:
        RuntimeError on unrecoverable failure after all retries.
    """
    payload = {
        "model": settings.model_workhorse,
        "temperature": settings.temperature_workhorse,
        "max_tokens": 1024,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/connected-brain/ops-agent",
        "X-Title": "ops-agent",
    }

    last_error: Optional[str] = None

    async with httpx.AsyncClient(timeout=60.0) as client:
        for attempt in range(settings.llm_max_retries):
            try:
                resp = await client.post(_OPENROUTER_URL, json=payload, headers=headers)
            except httpx.RequestError as e:
                last_error = str(e)
                if attempt < settings.llm_max_retries - 1:
                    await _sleep(attempt)
                continue

            if resp.status_code == 200:
                data = resp.json()
                choices = data.get("choices") or []
                if not choices:
                    raise RuntimeError("OpenRouter returned empty choices")
                content = (choices[0].get("message") or {}).get("content", "")
                usage = data.get("usage") or {}
                return {
                    "text": str(content).strip(),
                    "input_tokens": int(usage.get("prompt_tokens", 0)),
                    "output_tokens": int(usage.get("completion_tokens", 0)),
                    "model": data.get("model", settings.model_workhorse),
                }

            if resp.status_code in _RETRY_STATUSES:
                last_error = f"HTTP {resp.status_code}"
                logger.warning(
                    "OpenRouter %s on attempt %d/%d — retrying",
                    last_error, attempt + 1, settings.llm_max_retries,
                )
                if attempt < settings.llm_max_retries - 1:
                    await _sleep(attempt)
                continue

            body = resp.text[:300] if resp.text else ""
            raise RuntimeError(f"OpenRouter HTTP {resp.status_code}: {body}")

    raise RuntimeError(
        f"OpenRouter failed after {settings.llm_max_retries} attempts: {last_error}"
    )


async def _sleep(attempt: int) -> None:
    import asyncio
    await asyncio.sleep(2 ** attempt)
