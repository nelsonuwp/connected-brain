---
type: context-block
domain: schema
tags: [llm, input-format, output-format, bridge]
last-verified: 2026-02-22
---

# LLM I/O Format

## Summary
Standard input/output format for all LLM interactions.
System role carries the prompt/instructions. User role carries the content.
Outputs are wrapped in an LLMResponse envelope and always written to disk.

## Input Format

### Role Split
- system role → prompt template from vault/_prompts/ (behavior, rules, output format)
- user role   → assembled content (note + context blocks + optional data)

### User Message Assembly Order
1. [RE-ANCHOR] — previous session state if resuming
2. [CONTEXT: label] — injected context blocks (max 3)
3. [NOTE] — the Obsidian note being processed
4. [DATA] — RunArtifact JSON if data processing is involved

### LLMRequest fields
- model          str       — openrouter model string
- mode           str       — think | specify | execute
- note_path      str       — vault-relative path to input note
- context_blocks list[str] — vault-relative paths to context blocks (max 3)
- data_path      str|None  — path to RunArtifact JSON if applicable
- session_path   str|None  — path to previous re-anchor if continuing

## Output Format

### LLMResponse fields
- run_id         str       — matches RunArtifact.run_id if data was used
- model          str       — model that produced this output
- generated_at   str       — ISO 8601 UTC
- mode           str       — which mode was active
- status         str       — success | fail
- output         any       — the actual content (str for think/specify, dict for execute)
- error          dict|None — present when status==fail
- sources_used   list[str] — which source keys from RunArtifact were consumed
- tokens         dict      — {prompt, completion, total} — always log these

## Rules
- System prompt is always the _prompts/ file — never inline instructions in user role
- Max 3 context blocks per call — more means the task needs splitting
- LLMResponse always written to disk before returning — same finally pattern as SourceArtifact
- Token counts always logged — how you detect prompt bloat over time
