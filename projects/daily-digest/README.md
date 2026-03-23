# Daily Digest

Multi-source communication summarizer. Ingests email, Teams, and Slack → normalizes into a canonical schema → clusters related items across sources → LLM-triages into action categories → renders to Obsidian daily note.

## Architecture

```
email ──→ ingest ──→ normalize ──┐
teams ──→ ingest ──→ normalize ──┼──→ process ──→ summarize ──→ render
slack ──→ ingest ──→ normalize ──┘   (filter +    (LLM        (Obsidian
                                      embed +     triage)      daily note)
                                      cluster)
```

## Pipeline Stages

| # | Stage | File | What it does | LLM? |
|---|-------|------|-------------|------|
| 1 | Ingest | `ingestors/{email,teams,slack}.py` | Fetch raw data from APIs | No |
| 2 | Normalize | `normalize.py` | Source-specific → `InboundItem[]` | No |
| 3 | Process | `process.py` | Discard filter + embed + cluster | No |
| 4 | Summarize | `summarize.py` | LLM categorizes items | Yes |
| 5 | Render | `render.py` | Markdown → Obsidian daily note | No |

## Data Flow

```
outputs/source_email.json    ─┐
outputs/source_teams.json    ─┼──→ items_normalized.json ──→ items_processed.json ──→ daily_summary.json
outputs/source_slack.json    ─┘
```

## Key Schema: InboundItem

The canonical intermediate representation. Every source normalizes into this shape. Everything downstream is source-agnostic.

```python
{
    "id":               "a1b2c3d4e5f6",          # deterministic hash
    "source":           "email|teams|slack",
    "subject":          "OKRs",                   # nullable for Teams/Slack
    "body_text":        "full thread content...",
    "body_snippet":     "first 500 chars...",
    "thread_key":       "conversationId|chatId|thread_ts",
    "message_count":    3,
    "first_timestamp":  "2026-03-18T21:55:27Z",
    "last_timestamp":   "2026-03-19T12:20:50Z",
    "author":           {"name": "...", "handle": "...", "role": "from"},
    "participants":     [...],
    "is_from_me":       false,
    "mentions_me":      true,
    "am_in_to":         true,
    "am_in_cc":         false,
    "is_direct_message": false,
    "is_forwarded":     false,
    "url":              "https://outlook.office365.com/...",
    "source_meta":      {}
}
```

## Cross-Source Clustering

Uses `all-MiniLM-L6-v2` (384-dim sentence embeddings) with cosine similarity to find related items across sources. Falls back to TF-IDF when the model isn't available.

Example: An Adobe Sign email "Signature requested for Agile Fleet SOW" and a Teams message "sent [the SOW]" / "thanks, I'll sign soon" cluster together as one item.

## Usage

```bash
# Full pipeline — today's note, yesterday's messages
python run_pipeline.py

# Specific date
python run_pipeline.py --date 2026-03-17

# Skip ingest, reprocess existing captures
python run_pipeline.py --from normalize

# Only ingest email (skip Teams/Slack)
python run_pipeline.py --sources email

# Re-run just LLM + render
python run_pipeline.py --from summarize
```

## Setup

### 1. Copy connectors
```bash
cp ../email-agent/connectors/openrouter.py connectors/
cp ../email-agent/connectors/source_artifact.py connectors/
cp ../email-agent/connectors/llm_io.py connectors/
```

### 2. Add env vars
Copy the contents of `env_additions.txt` to your root `.env`.

### 3. Update Azure App Registration
Add API permissions: `Chat.Read`, `Chat.ReadBasic` (for Teams).

### 4. Install dependencies
```bash
pip install requests pyyaml numpy scikit-learn sentence-transformers
```

### 5. (Optional) Slack setup
See `ingestors/slack.py` header for setup instructions.

---

## Development Plan

### Phase 1: Core Framework ✅
- [x] InboundItem schema
- [x] Email ingestor (adapted from email-agent)
- [x] Teams ingestor
- [x] Slack ingestor (stub)
- [x] Normalize pipeline
- [x] Process pipeline (discard + embedding)
- [x] Summarize pipeline (LLM triage)
- [x] Render pipeline (Obsidian)
- [x] Orchestrator

### Phase 2: Validate & Tune
- [ ] Run with real email data — verify InboundItem schema matches actual Graph output
- [ ] Run with real Teams data — verify chat grouping and message concatenation
- [ ] Tune discard_rules.yaml — check false positives/negatives
- [ ] Tune merge_threshold — test cross-source clustering quality
- [ ] Tune LLM prompt — validate category accuracy vs your email-agent results
- [ ] Test Obsidian injection — verify idempotent section replacement

### Phase 3: Harden
- [ ] Error handling for partial API failures (e.g. Teams 403 on some chats)
- [ ] Token budget management — ensure LLM payload stays within context limits
- [ ] Add `--dry-run` flag to run_pipeline.py (process but don't write to vault)
- [ ] Add timing/cost logging per stage
- [ ] Handle pagination edge cases (>1000 emails, >200 messages per chat)

### Phase 4: Extend
- [ ] Wire up Slack ingestor (when bot token is ready)
- [ ] Add Jira ingestor (for ticket notifications — replace email signal detection)
- [ ] Calendar integration (today's meetings as context for the digest)
- [ ] Interactive HTML output (like the React to-do list)
- [ ] Embedding cache (don't re-embed unchanged items across runs)

### Phase 5: Optimize
- [ ] Evaluate cheaper models for triage (Gemini Flash, Haiku)
- [ ] Pre-compute embeddings during normalize (avoid recomputing on re-process)
- [ ] Investigate HDBSCAN for clustering (currently using greedy cosine — may want
      density-based for better cluster quality at scale)
