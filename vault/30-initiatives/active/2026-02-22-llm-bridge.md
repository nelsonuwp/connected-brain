---
created: 2026-02-22
jira-epic: null
last-updated: 2026-02-23
owner: null
status: active
type: initiative
---

# LLM Bridge (Project: Brain)

## One-Line Purpose
Python CLI (`brain.py`) that owns the entire connected-brain workflow — promoting notes between stages, calling OpenRouter with assembled context, and appending responses back into the note automatically. No Obsidian macros. No Templater. No copy-paste.

## Context
I'm building an "Adam in the loop" workflow for my daily work — a system where technology enhances my thinking rather than replacing it. The flow I'm building toward is:

raw idea → templated questions → LLM think mode → I answer → LLM specify mode → initiative spec → I tweak → execute in Cursor (if it's a coding project -- 30%) or other tooling like Google Sheets, Word, Jira, Confluence, etc. (if it's a "business" project -- 70%)

`brain.py` is the **sole mechanism** for moving notes between stages. Obsidian is the reading and writing surface only. Python owns all workflow operations.

The bridge started as "just send a note to an LLM" but has expanded to support injecting context files alongside the note — for example, sending a problem statement about data access AND the database schema so the LLM has the full picture, not just the raw idea.

The "junior developer" on this is Cursor/Composer. Code must be readable and extendable by an LLM — clear naming, no cleverness, no magic.

This is also the first real project running through the connected-brain workflow — inbox → thinking → initiative → execute — so it validates the system as much as it delivers the tool.

## Success Looks Like
1. I am able to more quickly go from raw idea to developed plan, consistently
2. I have a workflow that works for me vs. me working for it
3. I am leveraging LLMs to enhance the quality of my thinking and output
4. Every workflow transition (promote, think, refine, spec) is a single terminal command
5. LLM response is appended back into the same note automatically with a timestamp — zero copy-paste
6. Context files injectable alongside the note: `--context 20-context/schemas/db-schema.md`
7. Multiple context files supported in one call
8. Failure prints an error to terminal and leaves the note completely untouched
9. `--dry-run` flag prints the assembled payload to terminal without calling the API or touching the note
10. Obsidian has zero workflow responsibilities — it is a viewer and editor only

## Constraints
- OpenRouter API only — no Gemini SDK, no other provider SDKs
- Python 3.14+
- Subcommand architecture (Noun → Verb → File) using the `Typer` library
- system/user role split — prompt template from `_prompts/` is system role, note + context files are user role
- Failure = print error, do not write anything to the note (atomic: all or nothing)
- Minimal dependencies — `requests`, `python-dotenv`, `typer`, `rich` only
- Lives in `projects/llm-bridge/` following the standalone project pattern
- Code must be readable by Cursor/Composer — clear naming, no cleverness
- **Templater is not used for promotion, moving, or template injection — Python owns all of this**

## Open Questions
- Should `--context` accept multiple files in one flag or repeated flags?
  *(Resolved: repeated flags — standard Typer `List[str]`, e.g. `--context file1.md --context file2.md`)*
- Does the script resolve note paths relative to vault root, or does the user pass full paths?
  *(Resolved: vault-relative)*
- Where does `OPENROUTER_API_KEY` live — project `.env` or a parent one?
  *(Resolved: parent `~/connected-brain/.env` — see .env Hierarchy below)*
- Who owns promote / move / template injection?
  *(Resolved: Python only. Obsidian macros and Templater have no role in workflow transitions.)*

## Delegation State

| Person | Owns | By When | Level | Status |
| ------ | ---- | ------- | ----- | ------ |
| Cursor/Composer | Build `config.py`, `ai_client.py`, `brain.py` | This week | L4 | Not started |

## Linked Context Blocks
- [[20-context/schemas/llm-io]]

---

## Complete Command Reference

There are two types of commands. **File operations** move and scaffold notes — they never call the API. **LLM operations** assemble a payload, call OpenRouter, and append the response to the note.

---

### FILE OPERATIONS — No API Call

These are pure Python file operations. They read a template skeleton from `_templates/` (plain Markdown files, not Obsidian/Templater templates), inject it into the note, update the frontmatter, and move the file to the correct folder.

---

**`python brain.py idea promote 01-inbox/<file>`**

Goal: Graduate a raw idea into the thinking stage. Inserts the thinking skeleton so there's structure to fill in before calling `thinking think`.

What it does:
1. Reads `01-inbox/<file>`
2. Appends thinking template skeleton (from `_templates/thinking.md`) below existing idea content
3. Updates frontmatter: `type: thinking`, `status: raw`, `promoted: <today>`
4. Moves file → `10-thinking/<filename>`
5. Prints: `Promoted → 10-thinking/<filename>`

```bash
python brain.py idea promote 01-inbox/2026-02-22-new-idea.md
```

---

**`python brain.py thinking promote 10-thinking/<file>`**

Goal: Graduate a mature thinking note into the initiative stage. Inserts the initiative skeleton so there's structure to fill in before calling `thinking spec`.

What it does:
1. Reads `10-thinking/<file>`
2. Appends initiative template skeleton (from `_templates/initiative.md`) below existing thinking content
3. Updates frontmatter: `type: initiative`, `status: drafting`, `promoted: <today>`
4. Moves file → `30-initiatives/<filename>`
5. Prints: `Promoted → 30-initiatives/<filename>`

```bash
python brain.py thinking promote 10-thinking/2026-02-22-llm-bridge.md
```

---

### LLM OPERATIONS — Calls OpenRouter, Appends Response to Note

All LLM commands share the same optional flags:
- `--context <vault-relative-path>` — inject a context file alongside the note (repeatable)
- `--dry-run` — print assembled payload to terminal, do not call API, do not touch note

---

**`python brain.py idea refine 01-inbox/<file>`**

Goal: Sharpen a raw idea. The LLM clarifies what the idea actually is, what problem it solves, and whether it's worth pursuing — without expanding scope or writing a spec.

Model: workhorse | Prompt: `_prompts/refine-idea.md`

```bash
python brain.py idea refine 01-inbox/2026-02-22-new-idea.md
```

---

**`python brain.py thinking refine 10-thinking/<file>`**

Goal: Tighten a thinking note that's already been developed. The LLM identifies gaps, contradictions, and underdeveloped sections and asks targeted questions. It does not rewrite the note.

Model: workhorse | Prompt: `_prompts/refine-thinking.md`

```bash
python brain.py thinking refine 10-thinking/2026-02-22-llm-bridge.md
```

---

**`python brain.py thinking think 10-thinking/<file>`**

Goal: Deep thinking mode. The LLM works through the problem — explores implications, stress-tests assumptions, surfaces blind spots. This is the highest-value call in the workflow. You answer the output, then run it again, or promote when ready.

Model: reasoning | Prompt: `_prompts/think-mode.md`

```bash
python brain.py thinking think 10-thinking/2026-02-22-llm-bridge.md \
  --context 20-context/business/osom-model.md
```

---

**`python brain.py thinking spec 10-thinking/<file>`**

Goal: Convert a mature thinking note into a structured initiative spec — work breakdown, constraints, success criteria, open questions. Output is structured Markdown ready to paste into (or become) a `30-initiatives/` file. Distinct from `thinking promote` — that's the file move, this is the LLM call.

Model: reasoning | Prompt: `_prompts/specify-mode.md`

```bash
python brain.py thinking spec 10-thinking/2026-02-22-llm-bridge.md \
  --context 20-context/schemas/llm-io.md
```

---

**`python brain.py initiative refine 30-initiatives/<file>`**

Goal: Clean up and tighten an existing initiative spec. The LLM checks for internal consistency, missing constraints, vague success criteria, and unresolved open questions.

Model: workhorse | Prompt: `_prompts/refine-initiative.md`

```bash
python brain.py initiative refine 30-initiatives/026-02-22-llm-bridge.md
```

---

**`python brain.py context <file>`**

Goal: Summarize or explain a context block. Useful for understanding what a context file contains before injecting it into a real call. Output is appended to the context file itself.

Model: nano | Prompt: `_prompts/describe-context.md`

```bash
python brain.py context 20-context/business/osom-model.md
```

---

### Full Command Summary Table

| Noun | Verb | API Call? | Model | Goal |
|------|------|-----------|-------|------|
| idea | refine | ✓ | workhorse | Sharpen and clarify a raw idea |
| idea | promote | ✗ | — | Inject thinking skeleton, move to `10-thinking/` |
| thinking | refine | ✓ | workhorse | Tighten and identify gaps in a thinking note |
| thinking | think | ✓ | reasoning | Deep thinking — explore, stress-test, surface blind spots |
| thinking | spec | ✓ | reasoning | Convert thinking note into structured initiative spec |
| thinking | promote | ✗ | — | Inject initiative skeleton, move to `30-initiatives/` |
| initiative | refine | ✓ | workhorse | Check spec for consistency, gaps, vague criteria |
| context | (file) | ✓ | nano | Summarize/explain a context block |

---

## Decisions Made
- **CLI Architecture:** Noun → Verb → File subcommand routing for low cognitive load.
- **Output Destination:** Response appended to the same note — the note is the canonical record.
- **Tech Stack:** Python over Obsidian plugin — terminal access from Cursor is sufficient, plugin complexity not worth it.
- **Separation of Concerns:** Transport layer (`ai_client.py`) and vault I/O layer (`brain.py`) are separate files.
- **"Jr dev":** Cursor/Composer — affects how code must be written (clear naming, no magic).
- **Python owns all workflow transitions:** Promote, move, template injection — Obsidian and Templater have zero role. The only Obsidian automation that survives is QuickAdd Inbox Capture (idea creation only).
- **Templates become Python assets:** `_templates/thinking.md` and `_templates/initiative.md` are plain Markdown skeleton files that `brain.py` reads and injects. They are not Obsidian Templater templates.
- **`.env` Hierarchy:** `OPENROUTER_API_KEY` and `VAULT_ROOT` live in parent `~/connected-brain/.env`. Project `.env` holds overrides only. `config.py` loads parent first, project second — project wins on conflict.
- **Failure return value:** `ai_client.call()` returns `""` on unrecoverable failure — not `"{}"`. Empty string is an unambiguous sentinel.
- **`--dry-run`:** First-class flag on all LLM commands. Prints assembled payload. Does not call API. Does not write to note.
- **`thinking spec` vs `thinking promote`:** Separate commands intentionally. `spec` is the LLM call that produces initiative content. `promote` is the file move that graduates the note. You can run `spec` multiple times before you're ready to `promote`.

## .env Hierarchy

**Parent — `~/connected-brain/.env` (gitignored at root)**
```dotenv
OPENROUTER_API_KEY=sk-or-...
VAULT_ROOT=~/connected-brain/vault
MODEL_REASONING=anthropic/claude-opus-4-5
MODEL_WORKHORSE=anthropic/claude-sonnet-4-5
MODEL_NANO=anthropic/claude-haiku-4-5
LLM_MAX_RETRIES=3
```

**Child — `projects/llm-bridge/.env` (gitignored)**
```dotenv
# Override only what this project needs to be different.
# OPENROUTER_API_KEY is inherited from parent — do not duplicate here.
# Uncomment to override:
# MODEL_WORKHORSE=anthropic/claude-haiku-4-5
```

**Child — `projects/llm-bridge/.env.example` (committed, no real values)**
```dotenv
# project-level overrides — copy to .env and uncomment lines to change
# OPENROUTER_API_KEY is set in ~/connected-brain/.env — do not put it here
# MODEL_REASONING=anthropic/claude-opus-4-5
# MODEL_WORKHORSE=anthropic/claude-sonnet-4-5
# MODEL_NANO=anthropic/claude-haiku-4-5
# LLM_MAX_RETRIES=3
```

**`config.py` load order:**
```python
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path.home() / "connected-brain" / ".env")              # parent — establishes defaults
load_dotenv(Path(__file__).parent / ".env", override=True)         # child — project overrides win
```

## LLM Work Log

| Date | Mode | Context Used | Output | Where |
|------|------|-------------|--------|-------|
| 2026-02-22 | Think | none | Clarified scope, resolved 5 key questions | [[10-thinking/archive/2026-02-22-llm-bridge]] |
| 2026-02-22 | Specify | none | Full work breakdown, resolved open questions | [[30-initiatives/2026-02-22-llm-bridge]] |
| 2026-02-23 | Refine | CLI conventions | Integrated Typer subcommand architecture, renamed to brain.py | [[30-initiatives/2026-02-22-llm-bridge]] |
| 2026-02-23 | Refine | Session re-anchor | .env hierarchy, dry-run, promote as file op, full command table, Python owns promotion | [[30-initiatives/2026-02-22-llm-bridge]] |

## Work Breakdown

### Files to Build
```text
~/connected-brain/
├── .env                              ← OPENROUTER_API_KEY, VAULT_ROOT, global model defaults (gitignored)
├── _templates/
│   ├── thinking.md                   ← plain Markdown skeleton injected by `idea promote`
│   └── initiative.md                 ← plain Markdown skeleton injected by `thinking promote`
└── projects/llm-bridge/
    ├── .env                          ← project-level overrides only (gitignored)
    ├── .env.example                  ← committed, shows what can be overridden, no real values
    ├── requirements.txt              ← requests, python-dotenv, typer, rich
    ├── config.py                     ← loads parent then child .env, exposes Config dataclass
    ├── ai_client.py                  ← OpenRouter transport only, no file I/O
    └── brain.py                      ← vault file I/O, template injection, file moves, Typer CLI routing
```

### config.py
Loads parent `.env` then child `.env` (child wins). Exposes one `Config` dataclass. Validates `OPENROUTER_API_KEY` on import — fails fast with a readable message rather than a cryptic 401.

- `Config.OPENROUTER_API_KEY` — no default, raises on missing
- `Config.VAULT_ROOT` — default `~/connected-brain/vault`
- `Config.TEMPLATES_ROOT` — default `~/connected-brain/_templates`
- `Config.PROMPTS_ROOT` — default `~/connected-brain/vault/_prompts`
- `Config.LLM_MAX_RETRIES` — default `3`
- `Config.MODEL_REASONING` — default `anthropic/claude-opus-4-5`
- `Config.MODEL_WORKHORSE` — default `anthropic/claude-sonnet-4-5`
- `Config.MODEL_NANO` — default `anthropic/claude-haiku-4-5`

### ai_client.py
Transport only. Strings in, string out. Knows nothing about files.

`call(model_alias: str, system_prompt: str, user_message: str, verbose: bool = True) → str`

- `MODEL_MAP` maps alias (`"reasoning"`, `"workhorse"`, `"nano"`) to full model string from Config
- Retry loop with exponential backoff on: `429, 500, 502, 503, 504`
- If `verbose=True`, prints model name and token counts after each call
- Returns `""` on unrecoverable failure — never raises

### brain.py
Vault I/O, template injection, file moves, Typer CLI routing. Calls `ai_client.call()`. Knows nothing about HTTP.

**File operation functions:**
- `read_file(vault_relative_path: str) → str`
- `move_file(src_relative: str, dest_relative: str) → None` — uses `shutil.move`, prints confirmation
- `inject_template(note_path: str, template_name: str) → None` — reads from `_templates/`, appends skeleton to note, updates frontmatter
- `update_frontmatter(note_path: str, updates: dict) → None` — parses YAML front matter, applies key/value updates, rewrites file

**LLM operation functions:**
- `build_user_message(note_content: str, context_files: list[str]) → str`
- `append_to_note(note_path: str, llm_output: str, mode: str) → None` — atomic write

**Atomic write pattern:**
1. Read original note content into memory
2. Build output section string in memory
3. Concatenate: `new_content = original + "\n\n---\n\n## LLM Output — {mode} — {timestamp} UTC\n\n" + llm_output`
4. Write `new_content` to `note_path + ".tmp"`
5. `os.replace(note_path + ".tmp", note_path)` ← atomic on all POSIX systems
6. If anything fails before step 5 → clean up `.tmp` in except block, original note is untouched

**User message assembly format:**
```text
[CONTEXT: 20-context/schemas/db-schema.md]
<file contents>

[CONTEXT: 20-context/business/osom-model.md]
<file contents>

[NOTE: 10-thinking/2026-02-22-llm-bridge.md]
<note contents>
```

**Timestamp generation (Python runtime, not Templater):**
```python
from datetime import datetime, timezone
timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
```

### Build Order
1. `config.py`
2. `ai_client.py`
3. `brain.py` — file operations first (`promote`, `move`, `inject_template`), then LLM operations
4. `_templates/thinking.md` and `_templates/initiative.md` — plain Markdown skeletons (no Templater syntax)

### Decisions Made in Specify Mode
- `--context` accepts repeated flags natively supported by Typer (`List[str]`)
- All note and context paths are vault-relative; `Config.VAULT_ROOT` is the base
- `_templates/` lives at `~/connected-brain/` level — it's a vault asset, not a project asset
- `thinking spec` is the LLM call; `thinking promote` is the file move — separate commands, intentionally
- `_templates/thinking.md` and `_templates/initiative.md` contain zero Templater syntax — they are static Markdown skeletons that Python reads and appends verbatim (with the exception of the `created:` frontmatter field, which Python fills at inject time)
