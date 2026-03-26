# PRD: Daily Digest Pipeline v2 — Flat List with Tag-Based Categorization

**Date:** 2026-03-26
**Owner:** Adam Nelson
**Status:** Ready for implementation

---

## 1. Problem Statement

The daily-digest pipeline currently renders items into three bucketed sections (`### Waiting on Me`, `### Tracking`, `### New Information`) under a `## Daily Digest` header. This structural categorization is redundant — the Obsidian vault already uses `#action` and `#tracking` tags to feed the `open-tasks.md` sidebar. The bucket headers add visual noise without functional value.

Additionally, the current render format uses a `Title — [link](url)` pattern where the link is appended after the title. The link should BE the title: `[Title](url)`.

The pipeline also lacks calendar integration for the Today's Schedule section, and the LLM prompt doesn't produce the metadata needed for the new format (source stats, individual source links, completed action detection).

## 2. Desired Outcome

A single flat list injected under `## Yesterday in Review` where each item self-categorizes through inline tags. The sidebar (`open-tasks.md`) consumes these tags — the daily note creates them, the sidebar displays them.

## 3. What Changes

### 3.1 Section Header

| Current | New |
|---------|-----|
| `## Daily Digest` | `## Yesterday in Review` |

### 3.2 Render Format — Current vs. New

**CURRENT:**
```markdown
## Daily Digest
> 12 items · email, teams · 3 discarded · 8,432 tokens

### Waiting on Me (5)

#### [Subject](link) `email`
Summary text here.
- [email: Subject](url)

##### My Actions
- [ ] action 1 #action

##### Tracking
- tracked_action #tracking

> "Suggested reply"

`2026-03-19 12:20`

### Tracking (4)
...
### New Information (3)
...
```

**NEW:**
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

### 3.3 Format Rules

1. **Title IS the link:** `#### [Title Summary](primary-url) \`source\`` — not `Title — [link](url)`
2. **Source tag** after title: `` `email` ``, `` `teams` ``, `` `email` `teams` `` for multi-source
3. **Actions inline** — no `##### My Actions` sub-header. Just `- [ ] action #action` directly after the summary paragraph
4. **Tracking inline** — no `##### Tracking` sub-header. Just `- item #tracking` directly after actions
5. **Completed actions** — `- [x] Description — [proof](url) #action` when someone already did a requested action
6. **Sources line** — only when item spans multiple emails/threads/channels: `Sources: [label](url) · [label](url)`
7. **Stats line** at bottom of every item: `` `{N} emails · {M} teams · {date_range}` ``
8. **Summary stats** as blockquote at very end: `> {N} items · {N} emails · {N} teams · {N} discarded`
9. **No bucket headers** — no `### Waiting on Me`, `### Tracking`, `### New Information`
10. **No suggested reply** — remove from output (Adam doesn't use this)

### 3.4 Categorization (Implicit)

Tags drive the sidebar, not section headers:
- `#action` on a checkbox → surfaces in `open-tasks.md` under "My Actions"
- `#tracking` on a bullet → surfaces in `open-tasks.md` under "Waiting On Others"
- Neither → informational awareness, no sidebar presence

## 4. Files to Change

### 4.1 `summarize.py` — LLM Prompt Rewrite

**What changes:**
- System prompt asks for flat list output (not three-bucket classification)
- Each item produces: `title`, `summary`, `sources_detail`, `actions` (with completed flag), `tracked` items
- New fields: `message_count_by_source`, `date_range`, `individual_source_links`
- Remove `suggested_reply` from schema
- Remove `category` field (no longer needed — actions/tracked items implicitly categorize)

**New system prompt:** See Section 6.1

**New LLM output schema:** See Section 6.2

**What stays the same:**
- `_build_llm_payload()` — grouping by cluster_id, sending clusters together
- `_slim_item()` — stripping items for token efficiency
- `_call_llm()` — OpenRouter transport
- Single LLM call for all items (not per-item)

### 4.2 `render.py` — Flat List Renderer

**What changes:**
- `render_markdown()` → single flat loop over all items (no bucket iteration)
- `_render_item_block()` → new format with embedded title links, inline actions/tracking, stats line
- Section header: `## Yesterday in Review` (not `## Daily Digest`)
- `inject_digest()` → look for `## Yesterday in Review` instead of `## Daily Digest`
- Remove `_source_badge()` (replaced by inline source tags)
- Remove `##### My Actions` and `##### Tracking` sub-headers

**New render logic:** See Section 6.3

### 4.3 `summarize.py` — Output Schema Change

**Current output structure:**
```json
{
  "output": {
    "waiting_on_me": [...],
    "tracking": [...],
    "new_information": [...],
    "discard_count": 5
  }
}
```

**New output structure:**
```json
{
  "output": {
    "items": [...],
    "discard_count": 5
  }
}
```

Items are a flat list. Each item has actions and tracked items inline — no category bucket.

### 4.4 `config/discard_rules.yaml` — Minor Additions

Add any new discard patterns discovered during testing. No structural changes.

### 4.5 Calendar Integration (New Feature — Phase 2)

Add an `ingestors/calendar.py` that fetches today's calendar events via MS Graph and populates the Today's Schedule table. This is a separate feature and should be implemented after the digest format change is stable.

**Scope:**
- Fetch events for the target note date
- Filter out personal blocks (Blocked, Busy, Power Hour, No meetings after 4)
- Convert UTC → ET
- Generate table rows with full-path wikilinks: `[[90-meeting-notes/YYYY/MM-MMM/YYYY-MM-DD-meeting-short-name\|meeting-short-name]]`
- Inject into the `## Today's Schedule` section (find table, replace rows)

## 5. Files NOT to Change

- `normalize.py` — no changes needed
- `process.py` — no changes needed (discard filtering + clustering stays the same)
- `ingestors/*` — no changes needed
- `connectors/*` — no changes needed
- `schemas/inbound_item.py` — no changes needed (downstream schema is fine)
- `run_pipeline.py` — no changes needed (stage orchestration stays the same)

## 6. Prompts and Schemas

### 6.1 New System Prompt (`summarize.py`)

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

### 6.2 New LLM Output Schema (for `call_json` / `call_structured`)

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

### 6.3 New `render_markdown()` Logic (Pseudocode)

```python
def render_markdown(summary: dict) -> List[str]:
    items = summary["output"]["items"]
    discard_count = summary["output"]["discard_count"]
    sources = summary.get("sources", [])

    lines = ["## Yesterday in Review", ""]

    for item in items:
        # Title line: #### [Title](primary_url) `source_tag`
        primary_url = item["urls"][0]["url"] if item.get("urls") else ""
        source_tag = _source_tag(item["sources"])  # "email", "teams", "email` `teams"

        if primary_url:
            lines.append(f'#### [{item["title"]}]({primary_url}) `{source_tag}`')
        else:
            lines.append(f'#### {item["title"]} `{source_tag}`')

        # Summary paragraph
        lines.append(item["summary"])

        # Actions (inline, no sub-header)
        for action in item.get("actions", []):
            if action.get("completed") and action.get("completed_proof_url"):
                lines.append(f'- [x] {action["text"]} — [proof]({action["completed_proof_url"]}) #action')
            elif action.get("completed"):
                lines.append(f'- [x] {action["text"]} #action')
            else:
                lines.append(f'- [ ] {action["text"]} #action')

        # Tracked items (inline, no sub-header)
        for tracked in item.get("tracked_items", []):
            lines.append(f'- {tracked} #tracking')

        # Individual sources (only for multi-source items)
        ind_sources = item.get("individual_sources", [])
        if len(ind_sources) > 1:
            source_links = " · ".join(f'[{s["label"]}]({s["url"]})' for s in ind_sources)
            lines.append(f'Sources: {source_links}')

        # Stats line
        stats = item.get("source_stats", {})
        parts = []
        if stats.get("email_count"): parts.append(f'{stats["email_count"]} emails')
        if stats.get("teams_count"): parts.append(f'{stats["teams_count"]} teams')
        if stats.get("slack_count"): parts.append(f'{stats["slack_count"]} slack')
        date_range = stats.get("date_range", "")
        lines.append(f'`{" · ".join(parts)} · {date_range}`')
        lines.append("")  # blank line between items

    # Summary footer
    total_items = len(items)
    email_total = sum(i.get("source_stats", {}).get("email_count", 0) for i in items)
    teams_total = sum(i.get("source_stats", {}).get("teams_count", 0) for i in items)
    lines.append(f'> {total_items} items · {email_total} emails · {teams_total} teams · {discard_count} discarded')

    return lines
```

### 6.4 Updated `inject_digest()` — Section Marker

```python
# Change injection marker from "## Daily Digest" to "## Yesterday in Review"
# Look for existing section to replace:
if line.strip().startswith("## Yesterday in Review"):
    start_idx = i
    break
```

### 6.5 Updated `_merge_llm_output()` — Flat List

The merge function should produce a flat list instead of categorized buckets:

```python
def _merge_llm_output(items: list, llm_items: list) -> list:
    id_to_item = {item["id"]: item for item in items}
    enriched = []

    for llm_item in llm_items:
        if llm_item.get("discard"):
            continue  # Skip discarded items

        item_ids = llm_item.get("item_ids", [])

        # Build source URLs
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

## 7. Slim Item Payload Enhancement

The `_slim_item()` function needs to pass URLs through to the LLM so it can reference them in `individual_sources` and `completed_proof_url`:

```python
def _slim_item(item: dict) -> dict:
    return {
        "id": item["id"],
        "source": item["source"],
        "subject": item.get("subject"),
        "body_snippet": (item.get("body_snippet") or "")[:600],  # bump from 400 to 600
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
        "url": item.get("url", ""),  # NEW: pass through for source linking
    }
```

## 8. Testing Plan

1. **Unit test `render_markdown()`** — feed a mock `daily_summary.json` with the new schema, verify markdown output matches format spec
2. **Unit test `_merge_llm_output()`** — verify flat list output, URL preservation, source deduplication
3. **Integration test** — run full pipeline with `--from summarize` on existing `items_processed.json`, verify daily note injection
4. **Idempotency test** — run render twice, verify section is replaced not duplicated
5. **Edge cases:**
   - Item with no actions and no tracking (pure informational)
   - Item with completed action
   - Single-source item (no Sources line)
   - Multi-source cluster (Sources line appears)
   - Empty pipeline (no items after discard)

## 9. Migration Notes

- The section marker changes from `## Daily Digest` to `## Yesterday in Review`. Existing daily notes with `## Daily Digest` won't be found by the new injection logic. This is fine — old notes keep their format, new runs use the new section.
- If re-running on an old note, manually change the section header first, or add a fallback in `inject_digest()` that also checks for `## Daily Digest`.

## 10. Implementation Order

1. **`summarize.py`** — Update system prompt and output schema
2. **`render.py`** — Rewrite `render_markdown()` and `_render_item_block()`, update injection marker
3. **Test with `--from summarize`** on cached `items_processed.json`
4. **Full pipeline test** with `--date 2026-03-26`
5. **Calendar integration** (Phase 2, separate PR)
