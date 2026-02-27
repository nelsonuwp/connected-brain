# Connected Brain — Playbook

## The Full Workflow

```
01-inbox/           Raw idea capture
                    ↓  explore → critique → fix (repeat until score ≥ 7)
                    ↓  brain idea promote
10-thinking/        Structured thinking note
                    ↓  explore → critique → fix (repeat until score ≥ 7)
                    ↓  brain thinking promote
30-initiatives/
  drafting/         Executable initiative spec
                    ↓  explore → critique → fix (repeat until score ≥ 7)
                    ↓  brain initiative promote
  active/           In execution → tracked in Jira
                    ↓  (manual when done)
  done/             Completed
```

---

## Stage 1 — Capture an Idea

**When:** You have a thought worth not losing. 30 seconds to capture.

**Step 1:** Hit `Cmd+Shift+I` from anywhere in Obsidian.

**Step 2:** A single modal appears with three fields. Fill them in:
- **Idea title** — short, specific. This becomes the filename.
- **What is it?** — one or two sentences. What's the idea?
- **Why now?** — why does this matter right now? OK to leave blank.

**Step 3:** Hit OK. A dated note lands in `01-inbox/` and opens automatically.

That's it. Don't develop it now. Capture and move on.

---

## Stage 2 — Develop the Idea

**When:** You're triaging your inbox and this idea is worth developing.

**Goal:** Lock the **Why**. By the time you promote, it should be clear why
this matters, what problem it solves, and whether it's worth building into
a full thinking note.

### The Loop

**Step 1 — Explore** (run first, before any critique):
```bash
brain idea explore 01-inbox/2026-02-22-my-idea.md
```
Optionally inject context if relevant:
```bash
brain idea explore 01-inbox/2026-02-22-my-idea.md \
  --context 20-context/business/osom-model.md
```
Output: 3 directions on why this matters, implications, tradeoffs of
doing vs not doing. Ends with what's been covered and when you're ready
to critique. Read it in Obsidian, update your note based on what resonates.

**Step 2 — Critique:**
```bash
brain idea critique 01-inbox/2026-02-22-my-idea.md
```
Output: score 0-10, what's strong, what's weak and specifically what to
fix. If score ≥ 7, you're ready to promote. If not, fix the specific
weaknesses and run critique again.

**Step 3 — Fix:**
Open the note in Obsidian. Edit the main content directly based on the
critique output. The `# Explore` and `# Critique` sections at the bottom
are your working history — leave them, don't edit them.

**Repeat** explore → critique → fix until critique scores ≥ 7.

### Promote the Idea
```bash
brain idea promote 01-inbox/2026-02-22-my-idea.md
```
The LLM reads your entire idea note — the original content plus all the
explore and critique history — and generates a structured thinking note.
The original is archived to `01-inbox/archive/`. The new note lands in
`10-thinking/`.

---

## Stage 3 — Develop the Thinking

**When:** You have a structured thinking note in `10-thinking/`.

**Goal:** Lock the **How**. By the time you promote, you've explored
multiple approaches, weighed the tradeoffs, and committed to a direction.

The thinking note has four defined sections written as a real document:
- **Why This Matters** — carried over and sharpened from the idea
- **The Approach** — the chosen direction (develops through the loop)
- **Options Considered** — alternatives that were weighed
- **Assumptions & Risks** — what you're betting on, what could go wrong

### The Loop

**Step 1 — Explore:**
```bash
brain thinking explore 10-thinking/2026-02-22-my-idea.md
```
Output: 3 approaches to solving the problem — different ways to skin the
cat, who can help, what data exists, tradeoffs between approaches. Ends
with what's been covered and when you're ready to critique.

Read it. Decide which direction to anchor on. Update your note — especially
**The Approach** and **Options Considered** sections.

**Step 2 — Critique:**
```bash
brain thinking critique 10-thinking/2026-02-22-my-idea.md
```
Output: score 0-10, is the approach defined, are options genuinely
considered, are assumptions surfaced. Fix what's weak, repeat until ≥ 7.

**Step 3 — Fix:**
Edit the four main sections directly. Leave explore/critique history at
the bottom untouched.

**Repeat** until critique scores ≥ 7.

### Promote the Thinking
```bash
brain thinking promote 10-thinking/2026-02-22-my-idea.md
```
The LLM synthesizes everything in the note — all four sections plus the
entire explore/critique history — into a clean, standalone initiative spec.
The original is archived to `10-thinking/archive/`. The spec lands in
`30-initiatives/drafting/`.

---

## Stage 4 — Develop the Initiative Spec

**When:** You have a spec in `30-initiatives/drafting/`.

**Goal:** Lock the **Path**. By the time you promote, the spec is
executable — clear success criteria, ownership defined, work broken down,
path to implementation specific enough to hand to Cursor or a developer.

The initiative spec has defined sections:
- **One-Line Purpose**
- **Why This Matters**
- **Success Looks Like** — numbered, specific, testable outcomes
- **The Approach**
- **Constraints**
- **Open Questions**
- **Work Breakdown**
- **Delegation State**

### The Loop

**Step 1 — Explore:**
```bash
brain initiative explore 30-initiatives/drafting/2026-02-22-my-idea.md
```
Output: 3 implementation paths — sequencing options, dependency risks,
tradeoffs between paths. Ends with what's covered and when you're ready
to critique.

**Step 2 — Critique:**
```bash
brain initiative critique 30-initiatives/drafting/2026-02-22-my-idea.md
```
Output: score 0-10, is it executable, are success criteria testable, is
ownership clear. Fix what's weak, repeat until ≥ 7.

**Step 3 — Fix:**
Edit the spec sections directly. Leave explore/critique history at bottom.

**Repeat** until critique scores ≥ 7.

### Promote the Initiative
```bash
brain initiative promote 30-initiatives/drafting/2026-02-22-my-idea.md
```
File moves from `drafting/` to `active/`. No LLM call. No content change.
This is a status change. The spec is now live and surfaced in your daily
note Dataview dashboard.

---

## Stage 5 — Execute

**When:** The initiative is in `30-initiatives/active/`.

Execution tracking lives in Jira. The initiative spec in Obsidian is the
source of truth for **what** you decided to build and **why**. Jira tracks
the tasks.

**For Cursor sessions:**
Open `vault/_prompts/execute-session.md` (if it exists), or start a
Composer session and paste the initiative spec directly. At the end of
every Cursor session, generate a re-anchor:

```
[paste re-anchor-prompt.md contents into the LLM session]
```

Save the output to `80-sessions/{initiative-name}/session-NNN.md`.

**When done:**
Move the file manually from `30-initiatives/active/` to
`30-initiatives/done/`. It disappears from the dashboard.

---

## Working With Context Blocks

Context blocks in `20-context/` are reference documents you inject into
LLM sessions so you don't re-explain things. Use them with any brain.py
command via `--context`:

```bash
# Inject one context block
brain thinking explore 10-thinking/my-note.md \
  --context 20-context/business/osom-model.md

# Inject multiple
brain thinking explore 10-thinking/my-note.md \
  --context 20-context/business/osom-model.md \
  --context 20-context/schemas/db-schema.md
```

**Creating a new context block:**
1. Create a note in `20-context/` appropriate sub-folder
2. Write it as a self-contained reference — assume no other context
3. Run `brain context` on it to generate a summary:
   ```bash
   brain context 20-context/business/osom-model.md
   ```
4. The summary appended to the file tells you when to inject it

---

## Manual LLM Workflows

Some workflows happen outside brain.py — paste into a Claude session directly.

### Meeting Summary
1. Open a new Claude session
2. Paste contents of `vault/_prompts/meeting-summary.md`
3. Paste your raw meeting notes
4. Copy output → create note in `90-meeting-notes/`

### 1:1 Prep
1. Open a new Claude session
2. Paste contents of `vault/_prompts/one-on-one-prep.md`
3. Paste contents of the person's note from `40-people/`
4. Use output to prepare for the meeting

### Re-anchor (End of Session)
1. At end of any long Cursor or Claude session
2. Paste contents of `vault/_prompts/re-anchor-prompt.md`
3. Copy output → save to `80-sessions/{project}/session-NNN.md`
4. Next session: paste the re-anchor file as first message

---

## Dry Run — Testing Without Calling the LLM

Every brain.py command supports `--dry-run`. It prints the exact JSON
payload that would be sent to OpenRouter without making the call and
without writing anything.

```bash
brain idea critique 01-inbox/2026-02-22-my-idea.md --dry-run
```

Use this to verify context is being assembled correctly before spending
tokens on a real call.

---

## Quick Reference — Commands by Stage

| Stage | Explore | Critique | Promote |
|---|---|---|---|
| Idea (`01-inbox/`) | `brain idea explore` | `brain idea critique` | `brain idea promote` |
| Thinking (`10-thinking/`) | `brain thinking explore` | `brain thinking critique` | `brain thinking promote` |
| Initiative (`drafting/`) | `brain initiative explore` | `brain initiative critique` | `brain initiative promote` |
| Context (`20-context/`) | — | — | `brain context` |
