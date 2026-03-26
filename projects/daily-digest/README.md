# Daily Digest

Multi-source communication summarizer. Ingests email, Teams, and Slack, normalizes into a canonical schema, clusters related items across sources, LLM-triages into a flat digest, and renders to an Obsidian daily note.

## Architecture

```
email ──→ ingest ──→ normalize ──┐
teams ──→ ingest ──→ normalize ──┼──→ process ──→ summarize ──→ render
slack ──→ ingest ──→ normalize ──┘   (filter +    (LLM        (Obsidian
                                      embed +     triage)      daily note)
                                      cluster)
```

| # | Stage | File | What it does | LLM? |
|---|-------|------|-------------|------|
| 1 | Ingest | `ingestors/{email,teams,slack}.py` | Fetch raw data from APIs | No |
| 2 | Normalize | `normalize.py` | Source-specific → `InboundItem[]` | No |
| 3 | Process | `process.py` | Discard filter + embed + cluster | No |
| 4 | Summarize | `summarize.py` | LLM categorizes items | Yes |
| 5 | Render | `render.py` | Markdown → Obsidian daily note | No |

### Data Flow

```
outputs/source_email.json    ─┐
outputs/source_teams.json    ─┼──→ items_normalized.json ──→ items_processed.json ──→ daily_summary.json
outputs/source_slack.json    ─┘
```

## InboundItem Schema

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

## Output Format

Items render as a flat list under `## Yesterday in Review`. No bucket headers — tags drive the sidebar.

```markdown
## Yesterday in Review

#### [Board Deck — Ian's Task Assignments](https://outlook.office365.com/...) `email`
Ian assigned tasks: summarize critical incidents for Q2 Board deck, review and comment on what he missed.
- [ ] Summarize critical incidents for Q2 Board deck #action
- [ ] Review Ian's draft and comment on gaps #action
- Ian is preparing the full board package for April — waiting on multiple contributors #tracking
Sources: [Re: Q2 Board Deck — Draft](url1) · [Re: COE Operating Update](url2)
`4 emails · 2026-03-25 09:14–16:42`

#### [Centrilogic Numbers — Sarah Blanchard](https://outlook.office365.com/...) `email`
Sarah forwarding Centrilogic financial numbers originally sent by Marc Pare in December 2025.
`1 email · 2026-03-25 11:03`

#### [Sprint Capacity Discussion](https://teams.microsoft.com/...) `teams`
Team agreed to reduce scope for next sprint given upcoming holidays.
- [x] Erik confirmed scope reduction with delivery leads — [message](url) #action
- [ ] Confirm sprint backlog updated to reflect reduced scope #tracking
`2 teams · 2026-03-25 10:30–14:15`

> 14 items · 12 emails · 27 teams · 36 discarded
```

### Format Rules

1. **Title IS the link:** `#### [Title Summary](primary-url) \`source\`` — not `Title — [link](url)`
2. **Source tag** after title: `` `email` ``, `` `teams` ``, `` `email` `teams` `` for multi-source
3. **Actions inline** — no `##### My Actions` sub-header. Just `- [ ] action #action` directly after the summary paragraph
4. **Tracking inline** — no `##### Tracking` sub-header. Just `- item #tracking` directly after actions
5. **Completed actions** — `- [x] Description — [proof](url) #action` when someone already did a requested action
6. **Sources line** — only when item spans multiple emails/threads/channels: `Sources: [label](url) · [label](url)`
7. **Stats line** at bottom of every item: `` `{N} emails · {M} teams · {date_range}` ``
8. **Summary stats** as blockquote at very end: `> {N} items · {N} emails · {N} teams · {N} discarded`
9. **No bucket headers** — no `### Waiting on Me`, `### Tracking`, `### New Information`
10. **No suggested reply** — removed from output

### Categorization

Tags drive the sidebar, not section headers:
- `#action` on a checkbox → surfaces in `open-tasks.md` under "My Actions"
- `#tracking` on a bullet → surfaces in `open-tasks.md` under "Waiting On Others"
- Neither → informational awareness, no sidebar presence

## LLM Prompt

System prompt for `summarize.py`:

```
You are a personal assistant preparing a daily communication digest for a senior technology executive. You will receive a JSON array of communication items (emails, Teams messages, Slack messages) from the previous business day. Some items are grouped into clusters — these are related conversations across different platforms about the same topic.

For each item or cluster, produce a digest entry with:

1. **title**: A short, descriptive title that summarizes the topic (5-10 words). This will become a clickable link — make it scannable and informative. Examples: "AWS Marketplace — TDSynnex Program Docs", "Credit Review Board — Items for Tomorrow", "CPQ v28 Pricing Bug Resolved"

2. **summary**: 1-3 sentences of context. Enough to understand without opening the source. Include key names, numbers, dates, and decisions. Do NOT pad with filler.

3. **actions**: Things the executive needs to do. Each action is an object:
   - "text": clear, specific action description
   - "completed": true if evidence shows someone already fulfilled this (e.g., a reply confirming it's done)
   - "completed_proof_url": URL to the message proving completion (null if not completed)

4. **tracked_items**: Things others are doing that the executive should monitor. Each is a plain string. Examples: "Marc Pare to get AWS program language for amendment", "Jorge to fix BI report filter"

5. **source_stats**: Object with counts per source type and a date range:
   - "email_count": number of emails in this item/cluster
   - "teams_count": number of Teams messages
   - "slack_count": number of Slack messages
   - "date_range": "YYYY-MM-DD HH:MM" for single timestamp, or "YYYY-MM-DD HH:MM–HH:MM" for a range (in ET)

6. **individual_sources**: Array of individual source links when an item spans multiple threads/channels. Each has:
   - "label": Human-readable label (e.g., "Re: Q2 Board Deck — Draft", "Teams: Project Delivery")
   - "url": Direct link to the message/thread
   Only include this when there are 2+ distinct threads or channels. Omit (empty array) for single-source items.

Context about the user:
- If is_from_me is true on the most recent message, they already responded — actions are less likely
- If mentions_me or am_in_to is true and is_from_me is false, they probably need to act
- Items in CC only (am_in_cc=true, am_in_to=false) are more likely informational
- The user is Adam Nelson, a senior technology executive at Aptum

Discard items that are pure noise the deterministic filter missed (automated notifications, marketing, system alerts with no action needed). Set discard: true on these.

Respond with a JSON object. No markdown fences, no preamble:
{
  "items": [
    {
      "id": "item_id or cluster_id",
      "item_ids": ["id1", "id2"],
      "discard": false,
      "title": "Short Descriptive Title",
      "summary": "1-3 sentence summary.",
      "actions": [
        {"text": "Review the attachment before tomorrow's call", "completed": false, "completed_proof_url": null}
      ],
      "tracked_items": ["Jorge to amend the BI report filter"],
      "source_stats": {
        "email_count": 3,
        "teams_count": 1,
        "slack_count": 0,
        "date_range": "2026-03-25 09:14–16:42"
      },
      "individual_sources": [
        {"label": "Re: AWS Cloud Marketplace — Gina Tammo", "url": "https://..."},
        {"label": "Teams: Basis Discussion", "url": "https://..."}
      ]
    }
  ]
}
```

## LLM Output Schema

```json
{
  "type": "object",
  "properties": {
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "string"},
          "item_ids": {"type": "array", "items": {"type": "string"}},
          "discard": {"type": "boolean"},
          "title": {"type": "string"},
          "summary": {"type": "string"},
          "actions": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "text": {"type": "string"},
                "completed": {"type": "boolean"},
                "completed_proof_url": {"type": ["string", "null"]}
              },
              "required": ["text", "completed"]
            }
          },
          "tracked_items": {"type": "array", "items": {"type": "string"}},
          "source_stats": {
            "type": "object",
            "properties": {
              "email_count": {"type": "integer"},
              "teams_count": {"type": "integer"},
              "slack_count": {"type": "integer"},
              "date_range": {"type": "string"}
            }
          },
          "individual_sources": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "label": {"type": "string"},
                "url": {"type": "string"}
              }
            }
          }
        },
        "required": ["id", "item_ids", "discard", "title", "summary", "actions", "tracked_items", "source_stats"]
      }
    }
  },
  "required": ["items"]
}
```

## Pipeline Output Schema

The LLM returns a flat items list. After merge, the pipeline wraps it:

```json
{
  "output": {
    "items": [...],
    "discard_count": 5
  }
}
```

Each item carries enriched fields added by `_merge_llm_output()`: `urls` (array of source URLs with metadata) and `sources` (deduplicated list of source types).

## Render Logic

```python
def render_markdown(summary: dict) -> List[str]:
    items = summary["output"]["items"]
    discard_count = summary["output"]["discard_count"]

    lines = ["## Yesterday in Review", ""]

    for item in items:
        primary_url = item["urls"][0]["url"] if item.get("urls") else ""
        source_tag = _source_tag(item["sources"])

        if primary_url:
            lines.append(f'#### [{item["title"]}]({primary_url}) `{source_tag}`')
        else:
            lines.append(f'#### {item["title"]} `{source_tag}`')

        lines.append(item["summary"])

        for action in item.get("actions", []):
            if action.get("completed") and action.get("completed_proof_url"):
                lines.append(f'- [x] {action["text"]} — [proof]({action["completed_proof_url"]}) #action')
            elif action.get("completed"):
                lines.append(f'- [x] {action["text"]} #action')
            else:
                lines.append(f'- [ ] {action["text"]} #action')

        for tracked in item.get("tracked_items", []):
            lines.append(f'- {tracked} #tracking')

        ind_sources = item.get("individual_sources", [])
        if len(ind_sources) > 1:
            source_links = " · ".join(f'[{s["label"]}]({s["url"]})' for s in ind_sources)
            lines.append(f'Sources: {source_links}')

        stats = item.get("source_stats", {})
        parts = []
        if stats.get("email_count"): parts.append(f'{stats["email_count"]} emails')
        if stats.get("teams_count"): parts.append(f'{stats["teams_count"]} teams')
        if stats.get("slack_count"): parts.append(f'{stats["slack_count"]} slack')
        date_range = stats.get("date_range", "")
        lines.append(f'`{" · ".join(parts)} · {date_range}`')
        lines.append("")

    total_items = len(items)
    email_total = sum(i.get("source_stats", {}).get("email_count", 0) for i in items)
    teams_total = sum(i.get("source_stats", {}).get("teams_count", 0) for i in items)
    lines.append(f'> {total_items} items · {email_total} emails · {teams_total} teams · {discard_count} discarded')

    return lines
```

## Merge Logic

`_merge_llm_output()` enriches LLM items with source URLs and metadata from the original pipeline items:

```python
def _merge_llm_output(items: list, llm_items: list) -> list:
    id_to_item = {item["id"]: item for item in items}
    enriched = []

    for llm_item in llm_items:
        if llm_item.get("discard"):
            continue

        item_ids = llm_item.get("item_ids", [])
        urls = []
        sources_set = set()
        for iid in item_ids:
            orig = id_to_item.get(iid)
            if orig and orig.get("url"):
                urls.append({"source": orig["source"], "url": orig["url"], "subject": orig.get("subject")})
                sources_set.add(orig["source"])

        enriched.append({
            **llm_item,
            "urls": urls,
            "sources": list(sources_set),
        })

    return enriched
```

## Slim Item Payload

`_slim_item()` reduces each item for LLM context efficiency:

```python
def _slim_item(item: dict) -> dict:
    return {
        "id": item["id"],
        "source": item["source"],
        "subject": item.get("subject"),
        "body_snippet": (item.get("body_snippet") or "")[:600],
        "message_count": item.get("message_count", 1),
        "first_timestamp": item.get("first_timestamp", ""),
        "last_timestamp": item.get("last_timestamp", ""),
        "author": {
            "name": (item.get("author") or {}).get("name", ""),
            "handle": (item.get("author") or {}).get("handle", ""),
        },
        "participant_count": item.get("participant_count", 0),
        "is_from_me": item.get("is_from_me", False),
        "mentions_me": item.get("mentions_me", False),
        "am_in_to": item.get("am_in_to", False),
        "am_in_cc": item.get("am_in_cc", False),
        "is_direct_message": item.get("is_direct_message", False),
        "is_forwarded": item.get("is_forwarded", False),
        "has_attachments": item.get("has_attachments", False),
        "url": item.get("url", ""),
    }
```

## Injection

`inject_digest()` finds the `## Yesterday in Review` section in the daily note and replaces it. Falls back to checking for `## Daily Digest` for compatibility with older notes.

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

## Key Files

| File | Role |
|------|------|
| `schemas/inbound_item.py` | Canonical schema — changes here cascade downstream |
| `normalize.py` | One normalizer per source; add source = add normalizer + register in `NORMALIZERS` |
| `process.py` | Deterministic only (no LLM). Embedding uses `all-MiniLM-L6-v2` with TF-IDF fallback |
| `summarize.py` | Single LLM call via OpenRouter. System prompt is the most tunable part |
| `render.py` | Markdown renderer + daily note injection |
| `run_pipeline.py` | Orchestrator. Date logic derives fetch window from note date |
| `config/discard_rules.yaml` | Deterministic discard patterns |
| `config/user.yaml` | User identity for is_from_me detection |

## Adding a New Source

1. Create `ingestors/{source}.py` following the `slack.py` pattern
2. Add `_normalize_{source}()` in `normalize.py`
3. Register in `NORMALIZERS` dict in `normalize.py`
4. Add source-specific discard rules to `config/discard_rules.yaml`
5. Register in `INGESTORS` dict in `run_pipeline.py`
