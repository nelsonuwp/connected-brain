---
type: context-block
domain: schema
tags: [data, extraction, output-format, multi-source]
last-verified: 2026-02-22
---

# Source Artifact Schema

## Summary
All data extraction scripts produce a vendor-agnostic SourceArtifact JSON file.
One file per source, written unconditionally in a finally block — no silent failures.
A single source can have multiple API calls (objects). Multiple sources get wrapped in a RunArtifact.
No domain-specific identifiers in the base schema — extend at the project level.

## Structure

### Single Source (SourceArtifact)
- source         str       — provider name, matches filename suffix
- collected_at   str       — ISO 8601 UTC, when data was fetched
- status         str       — success | partial | fail | skipped
- objects        dict|null — null=total failure, {}=ran but nothing found
- error          dict|null — present when status==fail

### Per-Object (SourceObject) — each key under objects
- status         str       — success | partial | fail | skipped
- record_count   int       — len(data) if list, 1 if dict, 0 if None
- error          any|null  — pass API error through; Python: {type, message, retryable}
- data           any       — raw vendor payload, unmodified

### Multi-Source Wrapper (RunArtifact)
- run_id         str       — unique run identifier (uuid short)
- started_at     str       — ISO 8601 UTC, before first API call
- completed_at   str       — ISO 8601 UTC, set in finally block
- status         str       — derived from all source statuses
- sources        dict      — keyed by source name, each is a SourceArtifact

## Timestamp Strategy
- collected_at  → on SourceArtifact: when this specific source's data was fetched
- started_at    → on RunArtifact only: when the whole run began
- completed_at  → on RunArtifact only: when the finally block ran

## Key Rules
- objects: null  → total source failure (auth down, timeout, unrecoverable)
- objects: {}    → source ran successfully, nothing found — NOT a failure
- data: null     → that specific object failed or was skipped
- Always write the file. The finally block is mandatory. No silent failures.
- Never normalize or reshape data in the extractor — raw payload only
- Domain-specific fields (account_id, billing_period, etc.) added at project level

## Record Count Logic
- isinstance(data, list) → len(data)
- isinstance(data, dict) → 1
- data is None           → 0
