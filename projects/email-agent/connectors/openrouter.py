"""
connectors/openrouter.py
------------------------
OpenRouter transport for the email-agent project.

Copied from projects/_reference/clients/openrouter.py.
Do not import from _reference directly — this project owns its copy.

Env vars (loaded from repo-root .env):
    OPENROUTER_API_KEY      required
    LLM_MAX_RETRIES         optional, default 3
    MODEL_SEARCH            optional, default perplexity/sonar-pro
    TEMPERATURE_SEARCH      optional, default 0.1

Model constants (use these instead of raw strings):
    PERPLEXITY_SONAR        perplexity/sonar
    PERPLEXITY_SONAR_PRO    perplexity/sonar-pro
    GEMINI_FLASH            google/gemini-2.0-flash-001
"""

import json
import os
import time
from pathlib import Path
from typing import Any

import requests

URL            = "https://openrouter.ai/api/v1/chat/completions"
RETRY_STATUSES = (429, 500, 502, 503, 504)

PERPLEXITY_SONAR     = "perplexity/sonar"
PERPLEXITY_SONAR_PRO = "perplexity/sonar-pro"
GEMINI_FLASH         = "google/gemini-2.0-flash-001"


def _api_key() -> str:
    key = os.getenv("OPENROUTER_API_KEY", "")
    if not key:
        raise EnvironmentError("OPENROUTER_API_KEY not set in .env")
    return key

def _max_retries() -> int:
    return int(os.getenv("LLM_MAX_RETRIES", "3"))

def _default_search_model() -> str:
    return os.getenv("MODEL_SEARCH", PERPLEXITY_SONAR_PRO)

def _default_search_temperature() -> float:
    return float(os.getenv("TEMPERATURE_SEARCH", "0.1"))


# ---------------------------------------------------------------------------
# Core transport
# ---------------------------------------------------------------------------

# Models that support OpenAI-style response_format: {"type": "json_object"}
# Perplexity and Gemini do NOT — they need prompt-based JSON instructions instead
_JSON_MODE_MODELS = {
    "openai/", "anthropic/", "meta-llama/", "mistralai/", "x-ai/",
}

def _supports_json_mode(model: str) -> bool:
    """Return True only for models known to accept response_format: json_object."""
    return any(model.startswith(prefix) for prefix in _JSON_MODE_MODELS)


def call(
    model: str,
    messages: list,
    temperature: float = 0.1,
    max_tokens: int = 2048,
    response_format: dict = None,
    plugins: list = None,
) -> dict:
    """
    Call OpenRouter chat completions.

    Returns:
        {"content": str, "tokens": {...}, "source_urls": [...], "model": str}
        or None on unrecoverable failure.
    """
    payload = {
        "model":       model,
        "temperature": temperature,
        "messages":    messages,
        "max_tokens":  max_tokens,
    }
    if response_format and _supports_json_mode(model):
        payload["response_format"] = response_format
    if plugins:
        payload["plugins"] = plugins

    headers = {
        "Authorization": f"Bearer {_api_key()}",
        "Content-Type":  "application/json",
        "HTTP-Referer":  "https://github.com/connected-brain",
        "X-Title":       "Email Agent",
    }

    last_error = None
    for attempt in range(_max_retries()):
        try:
            resp = requests.post(URL, json=payload, headers=headers, timeout=60)
        except requests.RequestException as e:
            last_error = str(e)
            if attempt < _max_retries() - 1:
                time.sleep(2 ** attempt)
            continue

        if resp.status_code == 200:
            try:
                data = resp.json()
            except ValueError:
                last_error = "Invalid JSON response"
                continue

            choices = data.get("choices") or []
            if not choices:
                last_error = "Empty choices"
                continue

            msg     = choices[0].get("message") or {}
            content = msg.get("content")
            if content is None:
                last_error = "Empty content"
                continue

            usage  = data.get("usage") or {}
            tokens = {
                "prompt":     int(usage.get("prompt_tokens",     0)),
                "completion": int(usage.get("completion_tokens", 0)),
                "total":      int(usage.get("total_tokens",      0)),
            }

            source_urls = []
            for c in (data.get("citations") or []):
                url = c if isinstance(c, str) else c.get("url", "")
                if url:
                    source_urls.append(url)

            return {
                "content":     str(content).strip(),
                "tokens":      tokens,
                "source_urls": source_urls,
                "model":       data.get("model", model),
            }

        if resp.status_code in RETRY_STATUSES:
            last_error = f"HTTP {resp.status_code}"
            if attempt < _max_retries() - 1:
                time.sleep(2 ** attempt)
            continue

        last_error = f"HTTP {resp.status_code}"
        body = resp.text[:500] if resp.text else ""
        print(f"  [openrouter] Error: {last_error} - {body}")
        return None

    print(f"  [openrouter] Failed after {_max_retries()} attempts: {last_error}")
    return None


# ---------------------------------------------------------------------------
# JSON mode
# ---------------------------------------------------------------------------

def call_json(
    model: str,
    messages: list,
    temperature: float = 0.1,
    max_tokens: int = 2048,
    plugins: list = None,
):
    """
    Like call() but parses the response as JSON.
    Returns (parsed_dict, raw_response). parsed_dict is None on parse failure.
    """
    raw = call(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        response_format={"type": "json_object"},
        plugins=plugins,
    )
    if raw is None:
        return None, None

    content = raw["content"]
    if content.startswith("```"):
        lines   = content.splitlines()
        content = "\n".join(
            line for line in lines if not line.strip().startswith("```")
        ).strip()

    try:
        return json.loads(content), raw
    except json.JSONDecodeError as e:
        print(f"  [openrouter] JSON parse failed: {e}")
        print(f"  [openrouter] Raw: {content[:300]}")
        return None, raw


# ---------------------------------------------------------------------------
# Search shorthands
# ---------------------------------------------------------------------------

def search_call(
    messages: list,
    model: str = None,
    temperature: float = None,
    max_tokens: int = 1024,
):
    """Perplexity web-search call using MODEL_SEARCH from env."""
    return call(
        model=model or _default_search_model(),
        messages=messages,
        temperature=temperature if temperature is not None else _default_search_temperature(),
        max_tokens=max_tokens,
        plugins=[{"id": "web"}],
    )


def search_call_json(
    messages: list,
    model: str = None,
    temperature: float = None,
    max_tokens: int = 1024,
):
    """search_call() but parses the response as JSON."""
    return call_json(
        model=model or _default_search_model(),
        messages=messages,
        temperature=temperature if temperature is not None else _default_search_temperature(),
        max_tokens=max_tokens,
        plugins=[{"id": "web"}],
    )
