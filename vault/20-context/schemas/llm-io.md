---
type: context-block
domain: schema
tags: [llm, input-format, output-format, bridge]
last-verified: 2026-02-22
---

# LLM I/O Format

## Summary
Defines the standard input and output format for LLM interactions in the bridge script.
System role carries the prompt/instructions. User role carries the data.
All LLM outputs are structured JSON wrapped in an LLMResponse envelope.

## Input Format (what we send)

### Message Structure
```
system role  → prompt template from vault/_prompts/
               sets behavior, persona, output rules
user role    → the actual content to process
               note content + injected context blocks + data payload
```

### User Message Assembly
```
[CONTEXT: filename]
<contents of context block>

[NOTE]
<contents of obsidian note>

[DATA]
<source artifact or run artifact JSON if applicable>
```

### LLMRequest (TypedDict)
```
model           str        — openrouter model string
mode            str        — "think" | "specify" | "execute"
note_path       str        — vault-relative path to input note
context_blocks  list[str]  — vault-relative paths to context blocks (max 3)
data_path       str|None   — path to RunArtifact JSON if data is involved
session_path    str|None   — path to previous re-anchor if continuing work
```

## Output Format (what we expect back)

### For think/specify modes — structured markdown
The LLM returns markdown that gets appended to the note under a dated section header.
No JSON wrapper needed — output is human-readable prose/structure.

### For execute mode — code + assumptions
Returns code block followed by a brief assumptions section.
Gets written to a new file in the project, not appended to the note.

### For data processing — LLMResponse envelope
When processing SourceArtifact or RunArtifact data:

```python
class LLMResponse(TypedDict):
    run_id: str              # matches input RunArtifact.run_id
    company_id: str
    model: str               # model that produced this
    generated_at: str        # ISO 8601 UTC
    mode: str                # which prompt mode was used
    status: str              # "success" | "fail"
    output: Any              # the actual LLM output (dict, list, or str)
    error: Optional[dict]    # if status == "fail"
    sources_used: list[str]  # which source keys from RunArtifact were consumed
    tokens: dict             # {"prompt": int, "completion": int, "total": int}
```

## Rules

- System prompt is always the _prompts/ file — never inline instructions
- Max 3 context blocks per call — if you need more, split the task
- Data passed to LLMs should be the RunArtifact, not raw API responses
- LLMResponse always written to outputs/ before returning — same finally pattern as SourceArtifact
- Token counts always logged — they're how you detect prompt bloat
