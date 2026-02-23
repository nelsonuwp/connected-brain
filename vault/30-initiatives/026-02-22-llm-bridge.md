---
type: initiative
status: drafting
owner: 
jira-epic: 
created: <% tp.date.now("YYYY-MM-DD") %>
last-updated: <% tp.date.now("YYYY-MM-DD") %>
---

# LLM Bridge (Project: Brain)

## One-Line Purpose
Python CLI (`brain.py`) that reads an Obsidian note plus optional context files, calls OpenRouter, and appends the response back into the same note automatically — no copy-paste, no tool switching.

## Context
I'm building an "Adam in the loop" workflow for my daily work — a system where technology enhances my thinking rather than replacing it. The flow I'm building toward is:

raw idea → templated questions → LLM think mode → I answer → LLM specify mode → initiative spec → I tweak → execute in Cursor (if it's a coding project -- 30%) or other tooling like Google Sheets, Word, Jira, Confluence, etc. (if it's a "business" project -- 70%)

This project (`brain.py`) is the technical foundation that makes that flow possible. Without it, every LLM interaction requires copy-pasting between tools and context gets lost between sessions.

The bridge started as "just send a note to an LLM" but has expanded to support injecting context files alongside the note — for example, sending a problem statement about data access AND the database schema so the LLM has the full picture, not just the raw idea.

The "junior developer" on this is Cursor/Composer. Code must be readable and extendable by an LLM — clear naming, no cleverness, no magic.

This is also the first real project running through the connected-brain workflow — inbox → thinking → initiative → execute — so it validates the system as much as it delivers the tool.

## Success Looks Like
1. I am able to more quickly go from raw idea to developed plan, consistently
2. I have a workflow that works for me vs. me working for it
3. I am leveraging LLMs to enhance the quality of my thinking and output
4. `python brain.py thinking think 10-thinking/2026-02-22-llm-bridge.md` runs end to end seamlessly
5. LLM response is appended back into the same note automatically with a timestamp — zero copy-paste
6. Context files injectable alongside the note using a clean flag: `--context 20-context/schemas/db-schema.md`
7. Multiple context files supported in one call
8. Failure prints an error to terminal and leaves the note completely untouched

## Constraints
- OpenRouter API only — no Gemini SDK, no other provider SDKs
- Python 3.14+
- Subcommand architecture (Noun -> Verb -> File) using the `Typer` library
- system/user role split — prompt template from `_prompts/` is system role, note + context files are user role
- Failure = print error, do not write anything to the note (atomic: all or nothing)
- Minimal dependencies — `requests`, `python-dotenv`, and `typer` only
- Lives in `projects/llm-bridge/` following the standalone project pattern
- Code must be readable by Cursor/Composer — clear naming, no cleverness

## Open Questions
- Should `--context` accept multiple files in one flag or repeated flags?
  *(Resolved in specify mode: repeated flags are standard for Typer `List[str]`, e.g., `--context file1.md --context file2.md`)*
- Does the script resolve note paths relative to vault root, or does the user pass full paths?
  *(Resolved: Vault relative)*

## Delegation State

| Person | Owns | By When | Level | Status |
| ------ | ---- | ------- | ----- | ------ |
| Cursor/Composer | Build `brain.py` and `ai_client.py` | This week | L4 | Not started |

## Linked Context Blocks
- [[20-context/schemas/llm-io]]

## Decisions Made
- **CLI Architecture:** Shifted from generic flags (`--mode`, `--note`) to a state-based subcommand routing (`noun verb file`) for lower cognitive load.
- **Output Destination:** Goes back into the same note, not a new file — note is the canonical record.
- **Tech Stack:** Python over Obsidian plugin — terminal access from Cursor is sufficient, plugin complexity not worth it.
- **Separation of Concerns:** Transport layer (`ai_client.py`) and vault I/O layer (`brain.py`) are separate files — not one script.
- **"Jr dev":** Cursor/Composer, not a human — affects how code must be written.

## LLM Work Log

| Date | Mode | Context Used | Output | Where |
|------|------|-------------|--------|-------|
| 2026-02-22 | Think | none | Clarified scope, resolved 5 key questions | [[10-thinking/2026-02-22-llm-bridge]] |
| 2026-02-22 | Specify | none | Full work breakdown, resolved open questions | [[30-initiatives/026-02-22-llm-bridge]] |
| <% tp.date.now("YYYY-MM-DD") %> | Refine | CLI conventions | Integrated Typer subcommand architecture, renamed to brain.py, updated to Python 3.14 | [[30-initiatives/026-02-22-llm-bridge]] |

## Work Breakdown

### Files to Build
```text
projects/llm-bridge/
├── .env                  ← OPENROUTER_API_KEY, LLM_MAX_RETRIES, model overrides
├── .env.example          ← committed, no real values
├── requirements.txt      ← requests, python-dotenv, typer
├── config.py             ← loads .env, exposes Config class
├── ai_client.py          ← OpenRouter transport only, no file I/O
└── brain.py              ← vault file I/O, prompt assembly, Typer CLI routing
```

### config.py
Loads `.env`. Exposes one `Config` class.
- `Config.OPENROUTER_API_KEY`
- `Config.LLM_MAX_RETRIES` (default 3)
- `Config.MODEL_REASONING` (default anthropic/claude-opus-4)
- `Config.MODEL_WORKHORSE` (default anthropic/claude-sonnet-4-5)
- `Config.MODEL_NANO` (default anthropic/claude-haiku-4-5-20251001)
- `Config.VAULT_ROOT` (default ~/connected-brain/vault)

### ai_client.py
Transport only. Takes strings in, returns string out. Knows nothing about files.

`call(model_alias, system_prompt, user_message, verbose=True) → str`

- `MODEL_MAP` maps alias to model string from Config
- Retry loop with exponential backoff on transient errors (429, 503, 500, 502, 504)
- Strips markdown code fences from response
- Returns "{}" on unrecoverable failure — never raises

### brain.py
Vault I/O, Typer CLI routing, and prompt assembly. Calls `ai_client.call()`. Knows nothing about HTTP.

**CLI Interface (Typer Subcommands):**
```bash
python brain.py thinking think 10-thinking/2026-02-22-llm-bridge.md \
  --context 20-context/schemas/db-schema.md \
  --context 20-context/business/osom-model.md
```

**Path resolution:** all paths relative to `Config.VAULT_ROOT`

**Functions:**
- `read_file(vault_relative_path) → str`
- `build_user_message(note, context_files) → str`
- `append_to_note(note_path, output, mode) → None`
- Typer command decorators (`@idea_app.command()`, `@thinking_app.command()`, etc.) to map Nouns/Verbs to specific prompt templates and models.

**Atomic write pattern:**
1. Write output to `note_path.tmp`
2. Append new section to original note content
3. Write combined content to `note_path.tmp`
4. `os.replace(tmp, note_path)` ← atomic
5. If anything fails before step 4 → note is untouched

**User message assembly order:**
```text
[CONTEXT: filename]
<contents>

[NOTE]
<note contents>
```

**Output appended to note looks like:**
```markdown
---
## LLM Output — Think Mode — <% tp.date.now("YYYY-MM-DD HH:mm") %> UTC
<response>
```

**Verb → Model → Prompt mapping:**

| Noun | Verb | Model alias | Prompt file |
| ---- | ---- | ----------- | ----------- |
| idea | refine | workhorse | _prompts/refine-idea.md |
| thinking | refine | workhorse | _prompts/refine-thinking.md |
| thinking | think | reasoning | _prompts/think-mode.md |
| thinking | promote | reasoning | _prompts/specify-mode.md |
| initiative | refine | workhorse | _prompts/refine-initiative.md |

### Decisions Made in Specify Mode
- `--context` accepts multiple files via repeated flags natively supported by Typer (`List[str]`).
- All paths are vault-relative, `Config.VAULT_ROOT` is the base.
- Build order: `config.py` first, then `ai_client.py`, then `brain.py`.