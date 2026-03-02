# Connected Brain — LLM Context

*Use this document to understand the connected brain: what it is, how it works, and how to operate within it. Treat it as ground truth for this system.*

---

## 1. What It Is and Why It Exists

**The problem:** Ideas, decisions, and context live in too many places (Slack, email, browser tabs, memory). You spend time reconstructing context, re-explaining things to LLMs, and losing the reasoning behind decisions.

**The solution:** A single system that:

1. **Moves ideas through a defined process** — from raw capture to executable initiative, with LLM assistance at each stage and clear promotion gates.
2. **Stores context in reusable form** — so you inject it into LLM sessions instead of re-explaining, and decisions are recorded once.
3. **Keeps a record of how you got there** — thinking history, critiques, options considered, decisions made.

---

## 2. Mental Model: What Gets Locked at Each Stage

Each stage locks one thing before moving on:

| Stage | What you're working out | What gets locked | Ready when |
|-------|-------------------------|------------------|------------|
| **Idea** | Is this worth pursuing? | **The Why** | Critique scores ≥ 7 |
| **Thinking** | How might we solve this? | **The How** | Critique scores ≥ 7 |
| **Initiative** | What exactly are we building? | **The Path** | Critique scores ≥ 7 |
| **Active** | We're doing it | — | Done |

You don't spec before the why is clear; you don't execute before the path is clear. Promotions enforce that.

---

## 3. The LLM Loop (Same at Every Stage)

At each stage the loop is:

**explore → critique → fix → (repeat) → promote**

- **Explore** — Surfaces directions, options, tradeoffs (max 3 per run). Says when you've explored enough.
- **Critique** — Scores the note 0–10, says what's strong and what to fix to reach the next stage. 7+ = ready to promote (advisory, not automatic).
- **Fix** — You edit the note from the critique; explore/critique blocks stay as history.
- **Promote** — LLM (or, for initiative, a file move) turns the note into the next stage's format and moves it to the right folder.

---

## 4. Repository and Vault Structure

**Repo layout:**

```
~/connected-brain/
├── vault/                    ← Obsidian vault root
│   ├── _system/              ← system docs (README, structure, playbook, tooling)
│   ├── _templates/           ← Obsidian note templates
│   ├── _prompts/             ← LLM prompt files (used by brain.py)
│   ├── _attachments/         ← images, PDFs (Obsidian-managed)
│   ├── 00-daily/             ← daily/weekly notes, Dataview dashboard
│   ├── 01-inbox/             ← raw idea captures (3-field: title, what, why now)
│   ├── 10-thinking/          ← structured thinking notes (Why, Approach, Options, Assumptions)
│   ├── 20-context/           ← reusable context blocks for LLM injection (apis/, business/, schemas/, etc.)
│   ├── 30-initiatives/       ← initiative specs
│   │   ├── drafting/        ← specs being developed (explore/critique/fix)
│   │   ├── active/          ← in execution (surfaced in daily dashboard)
│   │   └── done/            ← completed (moved manually)
│   ├── 40-people/            ← person notes, 1:1 logs
│   ├── 50-services/         ← internal delivery units
│   ├── 51-catalog/          ← external products/offerings
│   ├── 52-customers/        ← customer accounts
│   ├── 60-decisions/        ← decision log (link from specs, don't re-litigate)
│   ├── 70-delegation/       ← delegation briefs
│   ├── 80-sessions/         ← LLM session re-anchors (e.g. Cursor)
│   └── 90-meeting-notes/    ← meeting notes
└── projects/
    ├── _reference/          ← pattern library (copy into projects, never import)
    └── llm-bridge/          ← brain.py runtime
```

**Naming:** Lowercase, kebab-case, date-prefix for workflow notes. Examples: `YYYY-MM-DD-short-title.md` for ideas/thinking/initiatives; `YYYY-MM-DD-short-description.md` for decisions; `firstname-lastname.md` for people; `session-NNN.md` in `80-sessions/{project}/`.

**Vault vs projects:** Notes, thinking, context → `vault/`. Code, scripts, config → `projects/`. Projects are standalone; they copy from `_reference/`, they don't import from it.

---

## 5. Full Workflow (Pipeline)

```
01-inbox/           Raw idea (QuickAdd Cmd+Shift+I)
                    ↓  explore → critique → fix until score ≥ 7
                    ↓  brain idea promote
10-thinking/        Thinking note (Why, Approach, Options, Assumptions)
                    ↓  explore → critique → fix until score ≥ 7
                    ↓  brain thinking promote
30-initiatives/drafting/   Initiative spec (Purpose, Success, Approach, Work breakdown, etc.)
                    ↓  explore → critique → fix until score ≥ 7
                    ↓  brain initiative promote
30-initiatives/active/     In execution (Jira for tasks; spec = source of truth)
                    ↓  manual when done
30-initiatives/done/       Completed
```

**Killing a note:** `brain idea kill`, `brain thinking kill`, or `brain initiative kill` — moves to that folder's `archive/`, sets `status: killed`, no LLM call. Preserved, not deleted.

---

## 6. Backbone Engine: brain.py

**What it is:** CLI in `projects/llm-bridge/` that runs all LLM operations on vault notes. Paths are vault-relative (e.g. `01-inbox/2026-02-22-my-idea.md`) unless prefixed with `vault/`.

**Model tiers (OpenRouter):**

| Alias | Model | Use |
|-------|--------|-----|
| reasoning | claude-opus-4-5 | Promote (high-stakes transforms) |
| workhorse | claude-sonnet-4-5 | Explore and critique |
| nano | claude-haiku-4-5 | Context describe |

**Commands:**

- **Idea** (notes in `01-inbox/`): `brain idea explore | critique | promote | kill <path>`
- **Thinking** (notes in `10-thinking/`): `brain thinking explore | critique | promote | kill <path>`
- **Initiative** (notes in `30-initiatives/drafting/`): `brain initiative explore | critique | promote | kill <path>` — promote is file move only (drafting → active).
- **Context** (notes in `20-context/`): `brain context <path>` — generates summary and appends to file.

**Flags:** `--context path` (repeatable) to inject context blocks; `--dry-run` to print payload without calling or writing; `--temperature` to override.

**Output behavior:** Explore and critique append a timestamped block to the bottom of the note; promote (idea/thinking) writes a new file and archives the original; initiative promote only moves the file; context appends to the context file.

---

## 7. Prompts and Context Blocks

**Prompts:** In `vault/_prompts/`. Names match what brain.py expects (e.g. `explore-idea.md`, `critique-thinking.md`, `promote-idea-to-thinking.md`). Each has frontmatter: `model`, `temperature`. Manual-use prompts (e.g. meeting-summary, one-on-one-prep, re-anchor-prompt) are pasted into an LLM session, not run by brain.py.

**Context blocks:** Notes in `20-context/` (and subfolders) are self-contained reference docs. Inject with `--context 20-context/...` on any brain command. Write once, inject instead of re-explaining. Run `brain context <path>` after writing/updating to get a summary appended.

---

## 8. Other Tools

- **Obsidian** — Where all notes and context live. Hotkeys: `Cmd+Shift+I` (inbox capture), `Cmd+Shift+E` (insert template), `Cmd+Shift+D` (daily), `Cmd+Shift+K` (weekly), etc.
- **OpenRouter** — LLM provider; API key in project `.env`.
- **Cursor** — Execution; initiative specs (and optionally execute-session prompt) feed Composer; re-anchors go to `80-sessions/{project}/session-NNN.md`.
- **Jira** — Task/execution tracking; brain + Obsidian track thinking and specs; Jira tracks doing.

---

## 9. Quick Command Reference

| Stage | Explore | Critique | Promote | Kill |
|-------|---------|----------|---------|------|
| Idea | `brain idea explore` | `brain idea critique` | `brain idea promote` | `brain idea kill` |
| Thinking | `brain thinking explore` | `brain thinking critique` | `brain thinking promote` | `brain thinking kill` |
| Initiative (drafting) | `brain initiative explore` | `brain initiative critique` | `brain initiative promote` | `brain initiative kill` |
| Context | — | — | `brain context` | — |

All paths vault-relative; `--dry-run` and `--context` available on all.

---

*End of Connected Brain LLM Context.*
