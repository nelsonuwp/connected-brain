"""
LLM I/O Schema — Python Implementation
Reference: vault/20-context/schemas/llm-io.md

Defines input and output types for LLM interactions via the bridge script.
Copy into your project. Do not import from _reference directly.
"""
from typing import TypedDict, Optional, Any, Literal
from datetime import datetime, timezone
from pathlib import Path
import json


# ── Type Definitions ──────────────────────────────────────────────────────────

class LLMRequest(TypedDict):
    model: str                      # openrouter model string
    mode: Literal["think", "specify", "execute"]
    note_path: str                  # vault-relative path to input note
    context_blocks: list[str]       # vault-relative paths (max 3)
    data_path: Optional[str]        # path to RunArtifact JSON if applicable
    session_path: Optional[str]     # path to previous re-anchor if continuing


class LLMResponse(TypedDict):
    run_id: str                     # matches RunArtifact.run_id if data was used
    company_id: Optional[str]
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
    context_blocks: dict[str, str],  # {label: content}
    data: Optional[Any] = None,
    session_content: Optional[str] = None,
) -> str:
    """
    Assembles the user role message from note, context blocks, and optional data.
    System role (prompt template) is handled separately.
    """
    parts = []

    if session_content:
        parts.append(f"[RE-ANCHOR — previous session state]\n{session_content}")

    for label, content in context_blocks.items():
        parts.append(f"[CONTEXT: {label}]\n{content}")

    parts.append(f"[NOTE]\n{note_content}")

    if data is not None:
        parts.append(f"[DATA]\n{json.dumps(data, indent=2)}")

    return "\n\n---\n\n".join(parts)


def make_llm_response(
    model: str,
    mode: str,
    run_id: str = "",
    company_id: Optional[str] = None,
) -> LLMResponse:
    """Initialize response in default failure state."""
    return {
        "run_id": run_id,
        "company_id": company_id,
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
    """Always write response before returning — same pattern as SourceArtifact."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2, ensure_ascii=False)
