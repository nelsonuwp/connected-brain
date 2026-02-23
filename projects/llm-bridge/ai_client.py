"""
OpenRouter transport only. Strings in, string out. No file I/O.
Retries 429, 5xx with exponential backoff. Returns "" on unrecoverable failure.
"""
import time
import requests

from config import Config

MODEL_MAP: dict[str, str] = {
    "reasoning": Config.MODEL_REASONING,
    "workhorse": Config.MODEL_WORKHORSE,
    "nano": Config.MODEL_NANO,
}

TEMPERATURE_MAP: dict[str, float] = {
    "reasoning": Config.TEMPERATURE_REASONING,
    "workhorse": Config.TEMPERATURE_WORKHORSE,
    "nano": Config.TEMPERATURE_NANO,
}

RETRY_STATUSES = (429, 500, 502, 503, 504)
URL = "https://openrouter.ai/api/v1/chat/completions"


def call(
    model_alias: str,
    system_prompt: str,
    user_message: str,
    temperature: float | None = None,
    verbose: bool = True,
) -> str:
    """
    Call OpenRouter chat completions. Returns response content or "" on failure.
    Never raises. If temperature is None, uses config default for that alias.
    """
    if model_alias not in MODEL_MAP:
        if verbose:
            print(f"Error: unknown model alias '{model_alias}'")
        return ""

    model_string = MODEL_MAP[model_alias]
    temp = temperature if temperature is not None else TEMPERATURE_MAP[model_alias]

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]
    payload = {
        "model": model_string,
        "messages": messages,
        "max_tokens": 4096,
        "temperature": temp,
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
                return ""

            if verbose:
                usage = data.get("usage") or {}
                pt = usage.get("prompt_tokens", "?")
                ct = usage.get("completion_tokens", "?")
                tot = usage.get("total_tokens", "?")
                print(f"Model: {model_string}")
                print(f"Tokens: prompt={pt}, completion={ct}, total={tot}")
            return text

        if resp.status_code in RETRY_STATUSES:
            last_error = f"HTTP {resp.status_code}"
            if attempt < Config.LLM_MAX_RETRIES - 1:
                time.sleep(2**attempt)
            continue

        # 4xx (other than 429) or other status — do not retry
        last_error = f"HTTP {resp.status_code}"
        if verbose:
            try:
                body = resp.text[:500] if resp.text else ""
                print(f"Error: {last_error} — {body}")
            except Exception:
                print(f"Error: {last_error}")
        return ""

    if verbose and last_error:
        print(f"Error: {last_error} (max retries exceeded)")
    return ""
