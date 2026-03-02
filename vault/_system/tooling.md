# Connected Brain — Tooling

## brain.py

The CLI that runs all LLM operations against vault notes. Lives in
`projects/llm-bridge/`. All paths are vault-relative unless prefixed
with `vault/` (repo-relative also accepted).

### Installation & Setup

```bash
cd ~/connected-brain/projects/llm-bridge
pip install -r requirements.txt
cp .env.example .env
# Add OPENROUTER_API_KEY to .env
```

### Model Tiers

| Alias | Model | Used for |
|---|---|---|
| `reasoning` | claude-opus-4-5 | Promote operations (high stakes transforms) |
| `workhorse` | claude-sonnet-4-5 | Explore and critique (quality + speed) |
| `nano` | claude-haiku-4-5 | Context describe (fast, cheap) |

Model and temperature are set per-prompt in frontmatter. Override with
`--temperature` flag if needed.

---

### Command Reference

#### `brain idea`

Operates on notes in `01-inbox/`.

```bash
# Expand the why — surfaces 3 directions, tells you when to stop
brain idea explore 01-inbox/2026-02-22-my-idea.md
brain idea explore 01-inbox/2026-02-22-my-idea.md --context 20-context/business/osom-model.md

# Score and audit — 0-10, what's strong, what to fix
brain idea critique 01-inbox/2026-02-22-my-idea.md

# Transform idea → thinking note, archive original
brain idea promote 01-inbox/2026-02-22-my-idea.md

# Mark complete and move to 30-initiatives/completed/
brain idea complete 01-inbox/2026-02-22-my-idea.md
```

**promote behavior:** LLM reads the full idea note (including all
`# Explore` and `# Critique` sections), generates a structured thinking
note with sections populated from the idea content, writes to
`10-thinking/{filename}`, moves original to `01-inbox/archive/{filename}`.

---

#### `brain thinking`

Operates on notes in `10-thinking/`.

```bash
# Expand the how — surfaces 3 approaches, tradeoffs, who can help
brain thinking explore 10-thinking/2026-02-22-my-idea.md
brain thinking explore 10-thinking/2026-02-22-my-idea.md --context 20-context/business/osom-model.md

# Score and audit — 0-10, what's solid, what needs more thinking
brain thinking critique 10-thinking/2026-02-22-my-idea.md

# Transform thinking → initiative spec, archive original
brain thinking promote 10-thinking/2026-02-22-my-idea.md

# Mark complete and move to 30-initiatives/completed/
brain thinking complete 10-thinking/2026-02-22-my-idea.md
```

**promote behavior:** LLM reads the full thinking note (including all
accumulated `# Explore` and `# Critique` sections), synthesizes everything
into a clean executable initiative spec, writes to
`30-initiatives/drafting/{filename}`, moves original to
`10-thinking/archive/{filename}`.

---

#### `brain initiative`

Operates on notes in `30-initiatives/drafting/`.

```bash
# Explore implementation paths — surfaces 3 paths, sequencing, dependencies
brain initiative explore 30-initiatives/drafting/2026-02-22-my-idea.md

# Score and audit — 0-10, is it executable, are success criteria testable
brain initiative critique 30-initiatives/drafting/2026-02-22-my-idea.md

# Move from drafting/ to active/ — file move only, no LLM
brain initiative promote 30-initiatives/drafting/2026-02-22-my-idea.md

# Mark complete and move to 30-initiatives/completed/ (works from drafting/ or active/)
brain initiative complete 30-initiatives/active/2026-02-22-my-idea.md
```

**promote behavior:** Moves file from `30-initiatives/drafting/` to
`30-initiatives/active/`. No LLM call. No content change. This is a
status change, not a transformation.

**complete behavior:** Sets `status: complete` in frontmatter, writes to
`30-initiatives/completed/{filename}`, removes source. No LLM call.

---

#### `brain context`

Operates on notes in `20-context/`. Generates a summary of the context
block and appends it to the file.

```bash
brain context 20-context/business/osom-model.md
```

Useful after writing or updating a context block — the summary tells you
what the block covers and when to inject it.

---

#### `brain absorb`

Consolidates one or more source notes into a root note: appends ## Absorbed
sections (LLM Key Points + verbatim Raw Context), then archives each source.

```bash
brain absorb 10-thinking/2026-02-22-my-thinking.md 01-inbox/overlap-a.md 01-inbox/overlap-b.md
```

**Signature:** `brain absorb <root_path> <source_path_1> [<source_path_2> ...]`
Root is always first; one or more sources. Paths vault-relative or `vault/...`.

**Behavior:** Root is append-only. For each source: LLM summarizes into Key
Points (or fallback line if LLM fails); block is `## Absorbed — [[source_stem]]`,
`### Key Points`, `### Raw Context` (verbatim). Then each source gets
`status: absorbed to [[root_stem]]` in frontmatter and is moved to
`{parent}/archive/`. No stage restrictions — any note can absorb any other.

**Errors:** Missing root or any source → exit 1. No sources provided → exit 1
with "No source notes provided". If root already contains `## Absorbed — [[source_stem]]`
for a source, a dimmed warning is printed but the command proceeds (duplicate
section will be appended).

**Prompt:** `summarize-absorbed.md` (workhorse).

---

### Critique Output Format

All three critique commands produce the same output structure:

```
## Score: X/10
[≥8: strong, consider promoting] [5-7: rework suggested] [≤4: significant gaps]
Score is advisory — you decide when to promote.

## Section Breakdown
### [Section Name]
Strong: ...
Weak: ...
Fix: specifically what to add, change, or explore to address the weakness

### [Section Name]
...
```

The aggregate score gives you a quick read. The per-section breakdown
tells you exactly what to fix. Not all sections will be flagged — only
the ones with real issues.

---

### Kill Commands

Move a note to local `archive/` and mark it as killed. No LLM call.

```bash
brain idea kill 01-inbox/2026-02-22-my-idea.md
brain thinking kill 10-thinking/2026-02-22-my-idea.md
brain initiative kill 30-initiatives/drafting/2026-02-22-my-idea.md
```

Adds `status: killed` to frontmatter, moves file to `{parent}/archive/`.
Preserved for reference but gone from active folders.

### Complete commands

Mark a note complete and move it to `30-initiatives/completed/`. No LLM call.
Works from any stage (idea, thinking, initiative). If a file with the same
name already exists in `completed/`, it is overwritten.

```bash
brain idea complete 01-inbox/2026-02-22-my-idea.md
brain thinking complete 10-thinking/2026-02-22-my-idea.md
brain initiative complete 30-initiatives/active/2026-02-22-my-idea.md
```

Sets `status: complete` in frontmatter, writes to
`30-initiatives/completed/{filename}`, removes the source file.

### Flags Available on All Commands

| Flag | What it does |
|---|---|
| `--context path` | Inject a context block into the user message. Repeatable. |
| `--dry-run` | Print the exact JSON payload that would be sent. Nothing is called or written. |
| `--temperature 0.7` | Override the temperature set in the prompt frontmatter. |

### Console output (dimmed)

Diagnostic lines help confirm what ran: each context file loaded shows
"Context loaded: path (N chars)"; before every LLM call, model, temperature,
and prompt name are printed; for absorb, "Summarizing path (1/N)...",
per-source token lines, "Tokens total: prompt=..., completion=..., total=...",
and "Appended N block(s) to path".

---

### How Output Gets Written

**Explore and critique** → appended to the bottom of the existing note as a
`# Section — timestamp ET` block. The original note content is never touched.

**Promote (idea and thinking)** → original is updated with `status: promoted`
in frontmatter and written back, then moved to `archive/` so the archived copy
has the correct status. New file is written to the target folder. Atomic write
via temp file + `os.replace()`.

**Promote (initiative)** → moves file between folders. No write operation.

**Complete (idea, thinking, initiative)** → sets `status: complete`, writes to
`30-initiatives/completed/{filename}`, removes source.

**Context** → appended to the context block file itself.

---

### Path Formats Accepted

```bash
# Vault-relative (preferred)
brain idea critique 01-inbox/2026-02-22-my-idea.md

# Repo-relative (also works)
brain idea critique vault/01-inbox/2026-02-22-my-idea.md
```

---

## Prompt Files

All prompts live in `vault/_prompts/`. Named exactly as brain.py expects.

### Prompts Used by brain.py

| File | Used by | Model |
|---|---|---|
| `critique-idea.md` | `brain idea critique` | workhorse |
| `critique-thinking.md` | `brain thinking critique` | workhorse |
| `critique-initiative.md` | `brain initiative critique` | workhorse |
| `explore.md` | `brain idea explore`, `brain thinking explore`, `brain initiative explore` | reasoning |
| `normalize.md` | `brain idea normalize`, `brain thinking normalize`, `brain initiative normalize` | workhorse |
| `promote-idea-to-thinking.md` | `brain idea promote` | reasoning |
| `promote-thinking-to-initiative.md` | `brain thinking promote` | reasoning |
| `specify-mode.md` | `brain thinking spec` | reasoning |
| `summarize-absorbed.md` | `brain absorb` | workhorse |
| `describe-context.md` | `brain context` | nano |

### Manual-Use Prompts (Not Called by brain.py)

These are pasted directly into a Claude or other LLM session. They follow
the same frontmatter format as brain.py prompts so model and temperature
intent is documented, but brain.py never reads them.

| File | When to use |
|---|---|
| `one-on-one-prep.md` | Before a 1:1 — paste with person note content |
| `re-anchor-prompt.md` | End of any long session — paste to generate re-anchor |
| `meeting-summary.md` | After a meeting — paste with raw notes |

### Prompt Frontmatter Format

Every prompt file (including manual-use) starts with:

```yaml
---
model: reasoning | workhorse | nano
temperature: reasoning | workhorse | nano
---
```

This documents intent even for manual-use prompts. For brain.py prompts,
these values drive model and temperature selection automatically.

---

## Obsidian Hotkeys

| Hotkey | Action |
|---|---|
| `Cmd+Shift+I` | Inbox capture — QuickAdd 3-field idea form |
| `Cmd+Shift+M` | Promote to thinking — QuickAdd macro |
| `Cmd+Shift+E` | Insert template into current note |
| `Cmd+Shift+V` | Move current file to another folder |
| `Cmd+Shift+D` | Open today's daily note |
| `Cmd+Shift+K` | Open this week's weekly note |
| `Cmd+O` | Quick switcher |
| `Cmd+Shift+P` | Command palette |

---

## QuickAdd Macros

### Inbox Capture (`Cmd+Shift+I`)
Type: Capture
Creates a dated note in `01-inbox/` with three fields in a single modal:
- Idea title (used in filename and note heading)
- What is it?
- Why now?

File format: `01-inbox/{{DATE:YYYY-MM-DD}}-{{VALUE:Idea title}}`
One-page input: Always

### Promote to Thinking (`Cmd+Shift+M`)
Type: Template
Creates a dated note in `10-thinking/` using the `thinking-note` template.
Use this when you want to start a thinking note fresh from a title rather
than promoting an existing idea note via brain.py.

File format: `10-thinking/{{DATE:YYYY-MM-DD}}-{{VALUE:Note title}}`

---

## Templater Folder Mappings

| Folder | Template applied on new file creation |
|---|---|
| `00-daily/` | `_templates/daily-briefing` |
| `10-thinking/` | `_templates/thinking-note` |
| `30-initiatives/` | `_templates/initiative-spec` |
| `40-people/` | `_templates/person-note` |
| `90-meeting-notes/` | `_templates/meeting-note` |

Note: template auto-applies only on file **creation**, not on file **move**.
Use `Cmd+Shift+E` to insert a template into an existing note after moving it.

---

## Dataview Dashboard

The daily note (`00-daily/YYYY-MM-DD.md`) contains a Dataview query that
surfaces active initiatives:

```dataview
TABLE owner, file.mtime as "Last Updated"
FROM "30-initiatives/active"
SORT file.mtime DESC
```

Frontmatter fields required on initiative specs:
- `type: initiative`
- `owner: "[[Person Name]]"`

Status is implicit from folder location — files in `active/` are active,
no separate status field needed.

---

## Git

Repository: `github.com/nelsonuwp/connected-brain`

```bash
# Manual commit after significant work
cd ~/connected-brain
git add -A
git commit -m "brief description"
git push
```

Obsidian Git plugin auto-pulls on boot. Auto-push is not enabled — commit
manually so you control what goes up.

**Never commit:** `.env` files (contain API keys). These are in `.gitignore`.
Always commit: `.env.example` files (no real values).

---

## Shell Commands Plugin (Obsidian)

Eliminates having to type file paths in the terminal. The Shell Commands
plugin lets you run brain.py commands against the currently open note
directly from Obsidian via hotkey or command palette.

### Setup

**1.** Install Shell Commands plugin via Settings → Community Plugins →
Browse → search "Shell Commands"

**2.** Settings → Shell Commands → Add new command for each operation:

| Command name | Shell command |
|---|---|
| Brain: Idea Explore | `cd ~/connected-brain/projects/llm-bridge && python brain.py idea explore "vault/{{file_path}}"` |
| Brain: Idea Critique | `cd ~/connected-brain/projects/llm-bridge && python brain.py idea critique "vault/{{file_path}}"` |
| Brain: Idea Promote | `cd ~/connected-brain/projects/llm-bridge && python brain.py idea promote "vault/{{file_path}}"` |
| Brain: Idea Complete | `cd ~/connected-brain/projects/llm-bridge && python brain.py idea complete "vault/{{file_path}}"` |
| Brain: Idea Kill | `cd ~/connected-brain/projects/llm-bridge && python brain.py idea kill "vault/{{file_path}}"` |
| Brain: Thinking Explore | `cd ~/connected-brain/projects/llm-bridge && python brain.py thinking explore "vault/{{file_path}}"` |
| Brain: Thinking Critique | `cd ~/connected-brain/projects/llm-bridge && python brain.py thinking critique "vault/{{file_path}}"` |
| Brain: Thinking Promote | `cd ~/connected-brain/projects/llm-bridge && python brain.py thinking promote "vault/{{file_path}}"` |
| Brain: Thinking Complete | `cd ~/connected-brain/projects/llm-bridge && python brain.py thinking complete "vault/{{file_path}}"` |
| Brain: Thinking Kill | `cd ~/connected-brain/projects/llm-bridge && python brain.py thinking kill "vault/{{file_path}}"` |
| Brain: Initiative Explore | `cd ~/connected-brain/projects/llm-bridge && python brain.py initiative explore "vault/{{file_path}}"` |
| Brain: Initiative Critique | `cd ~/connected-brain/projects/llm-bridge && python brain.py initiative critique "vault/{{file_path}}"` |
| Brain: Initiative Promote | `cd ~/connected-brain/projects/llm-bridge && python brain.py initiative promote "vault/{{file_path}}"` |
| Brain: Initiative Complete | `cd ~/connected-brain/projects/llm-bridge && python brain.py initiative complete "vault/{{file_path}}"` |
| Brain: Initiative Kill | `cd ~/connected-brain/projects/llm-bridge && python brain.py initiative kill "vault/{{file_path}}"` |
| Brain: Context | `cd ~/connected-brain/projects/llm-bridge && python brain.py context "vault/{{file_path}}"` |

**3.** For each command, set output to: **Show in notification** (so you
see token counts and success/error without switching to terminal)

**4.** Assign hotkeys via Settings → Hotkeys → search "Shell Commands"
Suggested additions:

| Hotkey | Command |
|---|---|
| `Cmd+Shift+1` | Brain: Idea Critique |
| `Cmd+Shift+2` | Brain: Thinking Critique |
| `Cmd+Shift+3` | Brain: Initiative Critique |

For explore and promote, use the command palette (`Cmd+Shift+P`) →
type "Brain:" to see all commands. Less frequent, don't need dedicated hotkeys.

### How {{file_path}} Works

`{{file_path}}` is a Shell Commands built-in variable that resolves to
the vault-relative path of the currently open note. Example:
`01-inbox/2026-02-22-my-idea.md`. brain.py accepts this format directly.
