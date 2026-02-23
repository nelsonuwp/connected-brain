"""
LLM I/O Schema — Agnostic Python Implementation
Reference: vault/20-context/schemas/llm-io.md

Copy into your project. Do not import from _reference directly.
"""
from typing import TypedDict, Optional, Any, Literal
from datetime import datetime, timezone
from pathlib import Path
import json


# ── Type Definitions ──────────────────────────────────────────────────────────

class LLMRequest(TypedDict):
    """
    Higher-level request envelope. NOT used by brain.py v1 — brain builds
    messages[] directly. Reserved for future multi-turn or session-aware callers.
    """
    model: str                      # openrouter model string
    mode: Literal["think", "spec", "refine", "promote", "describe-context"]
    note_path: str                  # vault-relative path to input note
    context_blocks: list[str]       # vault-relative paths (max 3)
    data_path: Optional[str]        # path to RunArtifact JSON if applicable
    session_path: Optional[str]     # path to previous re-anchor if continuing


class LLMResponse(TypedDict):
    run_id: str                     # matches RunArtifact.run_id if data was used
    model: str
    generated_at: str               # ISO 8601 UTC
    mode: str
    status: Literal["success", "fail"]
    output: Any                     # dict, list, or str depending on mode
    error: Optional[dict]
    sources_used: list[str]         # which source keys from RunArtifact were read
    tokens: dict                    # {"prompt": int, "completion": int, "total": int}


# ── Message Assembly ──────────────────────────────────────────────────────────

def build_user_message(
    note_content: str,
    context_blocks: dict[str, str],  # {vault-relative-path: file_contents}
    note_path: str,                  # vault-relative path, included in [NOTE:] label
    data: Optional[Any] = None,
    session_content: Optional[str] = None,
) -> str:
    """
    Assembles the user role message.
    System role (prompt template) is handled separately by the caller.
    Joins parts with "\\n\\n---\\n\\n". Emits [NOTE: note_path].

    Assembly order:
    1. Re-anchor (if resuming a session)
    2. Context blocks (injected reference material)
    3. Note content (the thing being processed)
    4. Data payload (RunArtifact JSON if applicable)
    """
    parts = []

    if session_content:
        parts.append(f"[RE-ANCHOR — previous session state]\n{session_content}")

    for label, content in context_blocks.items():
        parts.append(f"[CONTEXT: {label}]\n{content}")

    parts.append(f"[NOTE: {note_path}]\n{note_content}")

    if data is not None:
        parts.append(f"[DATA]\n{json.dumps(data, indent=2)}")

    return "\n\n---\n\n".join(parts)


def make_llm_response(model: str, mode: str, run_id: str = "") -> LLMResponse:
    """Initialize response in default failure state."""
    return {
        "run_id": run_id,
        "model": model,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "mode": mode,
        "status": "fail",
        "output": None,
        "error": None,
        "sources_used": [],
        "tokens": {"prompt": 0, "completion": 0, "total": 0},
    }


def write_llm_response(response: LLMResponse, path: Path) -> None:
    """Always write before returning — same finally pattern as SourceArtifact."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2, ensure_ascii=False)
