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


# ── Extractor Template ────────────────────────────────────────────────────────

def extract_template(output_dir: Path) -> SourceArtifact:
    """
    Template for a single-source extractor.

    HOW TO USE:
    1. Copy this function into your project
    2. Rename it: extract_jira, extract_slack, extract_zoominfo, etc.
    3. Replace 'template' with your source name in make_source_artifact()
    4. Replace placeholder API calls with real ones
    5. Add as many keys under objects as you have endpoints
    6. Never remove the finally block

    ADDING DOMAIN FIELDS:
    If your project needs extra fields (e.g. account_id, billing_period),
    add them to the artifact dict after make_source_artifact() returns.
    Do not modify SourceArtifact TypedDict — extend at the project level.
    """
    artifact = make_source_artifact("template")
    path = output_dir / "source_template.json"

    try:
        raw_list = []
        raw_detail = {}

        artifact["objects"] = {
            "list_endpoint": {
                "status": "success",
                "record_count": record_count(raw_list),
                "error": None,
                "data": raw_list,
            },
            "detail_endpoint": {
                "status": "success",
                "record_count": record_count(raw_detail),
                "error": None,
                "data": raw_detail,
            },
        }
        artifact["status"] = "success"

    except Exception as e:
        artifact["status"] = "fail"
        artifact["error"] = {
            "type": type(e).__name__,
            "message": str(e),
            "retryable": False,
        }

    finally:
        write_artifact(artifact, path)

    return artifact


# ── Multi-Source Runner Template ──────────────────────────────────────────────

def run_extraction(output_base: Path) -> RunArtifact:
    """
    Runs multiple extractors and wraps results in a RunArtifact.

    HOW TO USE:
    1. Copy into your project
    2. Import your extractor functions at the top of the file
    3. Add them to the extractors list as ('source_name', function) tuples
    4. Never remove the finally block
    """
    run, run_id = make_run_artifact()
    output_dir = output_base / run_id
    run_path = output_dir / "run.json"

    try:
        extractors = [
            # ('jira',     extract_jira),
            # ('slack',    extract_slack),
            # ('zoominfo', extract_zoominfo),
            ("template", extract_template),
        ]

        for source_name, extractor_fn in extractors:
            result = extractor_fn(output_dir)
            run["sources"][source_name] = result

        run["status"] = derive_run_status(run["sources"])

    except Exception as e:
        run["status"] = "fail"
        run["error"] = {
            "type": type(e).__name__,
            "message": str(e),
            "retryable": False,
        }

    finally:
        run["completed_at"] = utc_now()
        write_artifact(run, run_path)

    return run
