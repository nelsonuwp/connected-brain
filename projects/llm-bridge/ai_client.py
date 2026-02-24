"""
OpenRouter transport only. model, temperature, messages in; transport dict or None out.
No alias handling, no console output on success. Retries 429, 5xx with exponential backoff.
"""
import time
import requests

from config import Config

RETRY_STATUSES = (429, 500, 502, 503, 504)
URL = "https://openrouter.ai/api/v1/chat/completions"


def call(
    model: str,
    temperature: float,
    messages: list[dict],
) -> dict | None:
    """
    Call OpenRouter chat completions. Returns transport dict with content + tokens, or None on failure.
    Does not print or log on success.
    """
    payload = {
        "model": model,
        "temperature": temperature,
        "messages": messages,
        "max_tokens": 4096,
    }
    headers = {
        "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    last_error: str | None = None
    for attempt in range(Config.LLM_MAX_RETRIES):
        try:
            resp = requests.post(URL, json=payload, headers=headers, timeout=120)
        except requests.RequestException as e:
            last_error = str(e)
            if attempt < Config.LLM_MAX_RETRIES - 1:
                time.sleep(2**attempt)
            continue

        if resp.status_code == 200:
            try:
                data = resp.json()
            except ValueError:
                last_error = "Invalid JSON response"
                continue
            choices = data.get("choices")
            if not choices or not isinstance(choices, list):
                last_error = "Missing or invalid choices"
                continue
            msg = choices[0].get("message") if choices else None
            if not msg or not isinstance(msg, dict):
                last_error = "Missing or invalid message"
                continue
            content = msg.get("content")
            if content is None:
                last_error = "Empty content"
                continue
            text = str(content).strip()
            if not text:
                return None

            usage = data.get("usage") or {}
            tokens = {
                "prompt": int(usage.get("prompt_tokens", 0)),
                "completion": int(usage.get("completion_tokens", 0)),
                "total": int(usage.get("total_tokens", 0)),
            }
            return {"content": text, "tokens": tokens}

        if resp.status_code in RETRY_STATUSES:
            last_error = f"HTTP {resp.status_code}"
            if attempt < Config.LLM_MAX_RETRIES - 1:
                time.sleep(2**attempt)
            continue

        last_error = f"HTTP {resp.status_code}"
        try:
            body = resp.text[:500] if resp.text else ""
            print(f"Error: {last_error} — {body}")
        except Exception:
            print(f"Error: {last_error}")
        return None

    if last_error:
        print(f"Error: {last_error} (max retries exceeded)")
    return None
