"""
connectors/openrouter.py
------------------------
OpenRouter transport.

Key additions vs previous version:
  - call_structured()  → uses response_format: json_schema (strict) + response-healing plugin
                         + assistant prefill to guarantee clean JSON output
  - verbosity param    → maps to Anthropic output_config.effort; "low" = concise
  - call_json()        → kept for models that don't support json_schema; uses json_object

Env vars:
    OPENROUTER_API_KEY      required
    LLM_MAX_RETRIES         optional, default 3
    MODEL_SEARCH            optional, default perplexity/sonar-pro
    TEMPERATURE_SEARCH      optional, default 0.1
"""

import json
import os
import time
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------
_ROOT = Path(__file__).parent.parent.parent.parent  # connected-brain/
load_dotenv(_ROOT / ".env")

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
# Model capability flags
# ---------------------------------------------------------------------------

# Models that support response_format: json_schema (strict structured outputs)
# Anthropic Sonnet 4.5 + Opus 4.1, OpenAI GPT-4o+, most Gemini, most OSS
_JSON_SCHEMA_MODELS = {
    "anthropic/claude-sonnet-4-5",
    "anthropic/claude-opus-4-1",
    "openai/gpt-4o",
    "openai/gpt-4o-mini",
    "google/gemini-2.0-flash-001",
}

# Models that support the simpler json_object mode (broader support)
_JSON_OBJECT_MODELS = {
    "anthropic/", "openai/", "meta-llama/", "mistralai/", "x-ai/",
}

# Models that support the verbosity parameter
# (Anthropic maps it to output_config.effort; OpenAI Responses API native)
_VERBOSITY_MODELS = {"anthropic/", "openai/"}

def _supports_json_schema(model: str) -> bool:
    return model in _JSON_SCHEMA_MODELS

def _supports_json_object(model: str) -> bool:
    return any(model.startswith(p) for p in _JSON_OBJECT_MODELS)

def _supports_verbosity(model: str) -> bool:
    return any(model.startswith(p) for p in _VERBOSITY_MODELS)


# ---------------------------------------------------------------------------
# Core transport
# ---------------------------------------------------------------------------

def call(
    model: str,
    messages: list,
    temperature: float = 0.1,
    max_tokens: int = 2048,
    response_format: dict = None,
    plugins: list = None,
    verbosity: str = None,          # "low" | "medium" | "high"
    seed: int = None,
    stop: list = None,
    frequency_penalty: float = None,
    presence_penalty: float = None,
) -> dict:
    """
    Call OpenRouter chat completions.

    Returns:
        {"content": str, "tokens": {...}, "source_urls": [...], "model": str}
        or None on unrecoverable failure.

    Parameters that are unsupported by the chosen model are silently dropped
    by OpenRouter — no need to guard them here.
    """
    payload: dict[str, Any] = {
        "model":       model,
        "temperature": temperature,
        "messages":    messages,
        "max_tokens":  max_tokens,
    }
    if response_format:
        payload["response_format"] = response_format
    if plugins:
        payload["plugins"] = plugins
    if verbosity and _supports_verbosity(model):
        payload["verbosity"] = verbosity
    if seed is not None:
        payload["seed"] = seed
    if stop:
        payload["stop"] = stop
    if frequency_penalty is not None:
        payload["frequency_penalty"] = frequency_penalty
    if presence_penalty is not None:
        payload["presence_penalty"] = presence_penalty

    headers = {
        "Authorization": f"Bearer {_api_key()}",
        "Content-Type":  "application/json",
        "HTTP-Referer":  "https://github.com/connected-brain",
        "X-Title":       "Connected Brain",
    }

    last_error = None
    for attempt in range(_max_retries()):
        try:
            resp = requests.post(URL, json=payload, headers=headers, timeout=120)
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
        print(f"  [openrouter] Error: {last_error} — {body}")
        return None

    print(f"  [openrouter] Failed after {_max_retries()} attempts: {last_error}")
    return None


# ---------------------------------------------------------------------------
# Structured output  (preferred — json_schema + strict + response-healing)
# ---------------------------------------------------------------------------

def call_structured(
    model: str,
    messages: list,
    schema: dict,
    schema_name: str = "output",
    temperature: float = 0.1,
    max_tokens: int = 2048,
    verbosity: str = "low",
    seed: int = None,
    frequency_penalty: float = None,
):
    """
    Call OpenRouter with strict JSON schema enforcement.

    Uses:
      - response_format: json_schema (strict: true) — API-level schema enforcement
      - response-healing plugin                     — auto-repairs malformed JSON
      - assistant prefill '{'                        — eliminates preamble risk
      - verbosity: "low"                             — concise output by default

    Falls back to call_json() automatically if the model doesn't support json_schema.

    Returns (parsed_dict, raw_response). parsed_dict is None on parse failure.

    Args:
        schema:      A JSON Schema object (properties, required, additionalProperties)
        schema_name: Identifier sent to the API (used in error messages)
    """
    if not _supports_json_schema(model):
        # Graceful fallback for models without json_schema support
        print(f"  [openrouter] {model} doesn't support json_schema — falling back to json_object")
        return call_json(model=model, messages=messages,
                         temperature=temperature, max_tokens=max_tokens)

    # Assistant prefill: forces the model to begin its response mid-JSON,
    # eliminating any risk of preamble text before the opening brace.
    messages_with_prefill = list(messages) + [
        {"role": "assistant", "content": "{"}
    ]

    raw = call(
        model=model,
        messages=messages_with_prefill,
        temperature=temperature,
        max_tokens=max_tokens,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name":   schema_name,
                "strict": True,
                "schema": {
                    **schema,
                    "additionalProperties": False,  # no hallucinated extra fields
                },
            },
        },
        plugins=[
            {"id": "response-healing"},  # auto-repairs malformed JSON
        ],
        verbosity=verbosity,
        seed=seed,
        frequency_penalty=frequency_penalty,
    )

    if raw is None:
        return None, None

    # Prepend the prefill character the model didn't echo back
    content = "{" + raw["content"] if not raw["content"].startswith("{") else raw["content"]

    # Strip any accidental markdown fences (response-healing should prevent this,
    # but keep as belt-and-suspenders)
    if content.startswith("```"):
        lines   = content.splitlines()
        content = "\n".join(l for l in lines if not l.strip().startswith("```")).strip()

    try:
        return json.loads(content), raw
    except json.JSONDecodeError as e:
        print(f"  [openrouter] Structured parse failed: {e}")
        print(f"  [openrouter] Raw: {content[:300]}")
        return None, raw


# ---------------------------------------------------------------------------
# JSON object mode  (broader model support, less strict)
# ---------------------------------------------------------------------------

def call_json(
    model: str,
    messages: list,
    temperature: float = 0.1,
    max_tokens: int = 2048,
    plugins: list = None,
    verbosity: str = "low",
):
    """
    Like call() but parses the response as JSON using json_object mode.
    Less strict than call_structured() — use when json_schema isn't supported.
    Returns (parsed_dict, raw_response). parsed_dict is None on parse failure.
    """
    raw = call(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        response_format={"type": "json_object"} if _supports_json_object(model) else None,
        plugins=plugins,
        verbosity=verbosity,
    )
    if raw is None:
        return None, None

    content = raw["content"]
    if content.startswith("```"):
        lines   = content.splitlines()
        content = "\n".join(l for l in lines if not l.strip().startswith("```")).strip()

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
    return call_json(
        model=model or _default_search_model(),
        messages=messages,
        temperature=temperature if temperature is not None else _default_search_temperature(),
        max_tokens=max_tokens,
        plugins=[{"id": "web"}],
    )