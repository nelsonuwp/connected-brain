"""
Source Artifact Schema — Python Implementation
Reference: vault/20-context/schemas/source-artifact.md

Copy this file into your project. Do not import from _reference directly.
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
    data: Any  # Unmodified vendor payload


class SourceArtifact(TypedDict):
    source: str
    company_id: str
    collected_at: str           # ISO 8601 UTC
    status: Literal["success", "partial", "fail", "skipped"]
    objects: Optional[dict[str, SourceObject]]  # None on total failure
    error: Optional[dict]       # Required when status == "fail"


class RunArtifact(TypedDict):
    """Wraps multiple SourceArtifacts from a single extraction run."""
    run_id: str
    company_id: str
    started_at: str             # ISO 8601 UTC
    completed_at: str           # ISO 8601 UTC
    status: Literal["success", "partial", "fail"]
    sources: dict[str, SourceArtifact]


# ── Helpers ───────────────────────────────────────────────────────────────────

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def record_count(data: Any) -> int:
    """Consistent record count logic across all extractors."""
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        return 1
    return 0


def derive_run_status(sources: dict[str, SourceArtifact]) -> Literal["success", "partial", "fail"]:
    """Derive overall run status from individual source statuses."""
    statuses = {s["status"] for s in sources.values()}
    if statuses == {"success"}:
        return "success"
    if "success" in statuses or "partial" in statuses:
        return "partial"
    return "fail"


def write_artifact(artifact: Union[SourceArtifact, RunArtifact], path: Path) -> None:
    """Mandatory write — always call in finally block."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(artifact, f, indent=2, ensure_ascii=False)


# ── Base Extractor Pattern ────────────────────────────────────────────────────

def make_source_artifact(source: str, company_id: str) -> SourceArtifact:
    """Initialize artifact in default failure state. Populate, then write."""
    return {
        "source": source,
        "company_id": company_id,
        "collected_at": utc_now(),
        "status": "fail",
        "objects": None,
        "error": None,
    }


def make_run_artifact(company_id: str) -> tuple[RunArtifact, str]:
    """Initialize a run artifact. Returns (artifact, run_id)."""
    run_id = str(uuid.uuid4())[:8]
    return {
        "run_id": run_id,
        "company_id": company_id,
        "started_at": utc_now(),
        "completed_at": "",      # set on completion
        "status": "fail",        # updated on completion
        "sources": {},
    }, run_id


# ── Example Extractor (copy and adapt) ───────────────────────────────────────

def extract_example(company_id: str, run_id: str, output_dir: Path) -> SourceArtifact:
    """
    Template for a single-source extractor.
    Copy this function. Replace 'example' with your source name.
    """
    artifact = make_source_artifact("example", company_id)
    path = output_dir / f"source_example.json"

    try:
        # Replace with actual API calls
        raw_items = []           # e.g. response.json()["items"]
        raw_detail = {}          # e.g. response.json()

        artifact["objects"] = {
            "items": {
                "status": "success",
                "record_count": record_count(raw_items),
                "error": None,
                "data": raw_items,
            },
            "detail": {
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
        write_artifact(artifact, path)  # Always runs. No silent failures.

    return artifact


# ── Multi-Source Runner Pattern ───────────────────────────────────────────────

def run_extraction(company_id: str, output_base: Path) -> RunArtifact:
    """
    Runs multiple extractors and wraps results in a RunArtifact.
    Add your extractors to the extractors list.
    """
    run, run_id = make_run_artifact(company_id)
    output_dir = output_base / run_id
    run_path = output_dir / "run.json"

    try:
        extractors = [
            # ("source_name", extractor_function),
            ("example", extract_example),
            # ("zoominfo", extract_zoominfo),
            # ("salesforce", extract_salesforce),
        ]

        for source_name, extractor_fn in extractors:
            result = extractor_fn(company_id, run_id, output_dir)
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
        write_artifact(run, run_path)  # Always runs.

    return run
