"""
Source Artifact Schema — Agnostic Python Implementation
Reference: vault/20-context/schemas/source-artifact.md

Copy this file into your project. Do not import from _reference directly.
Your project owns its copy — add domain-specific fields at the project level.
"""
from typing import TypedDict, Optional, Any, Union, Literal
from datetime import datetime, timezone
from pathlib import Path
import json
import uuid


# ── Type Definitions ──────────────────────────────────────────────────────────

class SourceObject(TypedDict):
    status: Literal["success", "partial", "fail", "skipped"]
    record_count: int
    error: Union[str, dict, None]
    data: Any  # Unmodified vendor payload — never reshape here


class SourceArtifact(TypedDict):
    source: str                     # provider name — matches filename suffix
    collected_at: str               # ISO 8601 UTC — when this data was fetched
    status: Literal["success", "partial", "fail", "skipped"]
    objects: Optional[dict[str, SourceObject]]  # null = total failure
    error: Optional[dict]           # present when status == "fail"


class RunArtifact(TypedDict):
    """Wraps multiple SourceArtifacts from a single extraction run."""
    run_id: str                     # unique run identifier
    started_at: str                 # ISO 8601 UTC — before first API call
    completed_at: str               # ISO 8601 UTC — after finally block
    status: Literal["success", "partial", "fail"]
    sources: dict[str, SourceArtifact]


# ── Helpers ───────────────────────────────────────────────────────────────────

def utc_now() -> str:
    """Current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def record_count(data: Any) -> int:
    """
    Consistent record count across all extractors.
    list  -> len(data)
    dict  -> 1
    None  -> 0
    """
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        return 1
    return 0


def derive_run_status(
    sources: dict[str, SourceArtifact],
) -> Literal["success", "partial", "fail"]:
    """Derive overall run status from individual source statuses."""
    statuses = {s["status"] for s in sources.values()}
    if statuses == {"success"}:
        return "success"
    if "success" in statuses or "partial" in statuses:
        return "partial"
    return "fail"


def write_artifact(artifact: Union[SourceArtifact, RunArtifact], path: Path) -> None:
    """
    Mandatory write. Always call in finally block.
    Never let a script exit without writing its artifact.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(artifact, f, indent=2, ensure_ascii=False)


# ── Initializers ──────────────────────────────────────────────────────────────

def make_source_artifact(source: str) -> SourceArtifact:
    """
    Initialize a SourceArtifact in default failure state.
    Populate objects and set status in the try block.
    Always write in the finally block.
    """
    return {
        "source": source,
        "collected_at": utc_now(),
        "status": "fail",
        "objects": None,
        "error": None,
    }


def make_run_artifact() -> tuple[RunArtifact, str]:
    """
    Initialize a RunArtifact. Returns (artifact, run_id).
    Set completed_at and final status in the finally block.
    """
    run_id = str(uuid.uuid4())[:8]
    return {
        "run_id": run_id,
        "started_at": utc_now(),
        "completed_at": "",
        "status": "fail",
        "sources": {},
    }, run_id
