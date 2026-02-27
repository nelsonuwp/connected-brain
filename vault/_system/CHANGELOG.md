# Connected Brain — Changelog

Structural decisions with rationale. When something is the way it is for
a non-obvious reason, it belongs here. Don't duplicate content from the
other docs — link to them. This is the "why" record, not the "what" record.

---

## 2026-02-23

### Removed normalize command
**Decision:** `brain idea normalize`, `brain thinking normalize`, and
`brain initiative normalize` removed from brain.py.
**Rationale:** Low return, high complexity. Normalize rewrote the
"Current Version" section for clarity, but with critique now acting as
a coach (telling you specifically what to fix), manual editing based on
critique output produces better results with less friction. The
`extract_current_version()` parsing logic it required was the most
complex code in brain.py for the least value.

### Removed specify-mode.md, absorbed into promote-thinking-to-initiative.md
**Decision:** `specify-mode.md` deleted. Its behavior merged into
`promote-thinking-to-initiative.md`.
**Rationale:** Specify and promote were doing the same job — generating
an initiative spec from a thinking note. Having two separate commands
(`brain thinking spec` and `brain thinking promote`) created confusion
about which to run and when. Promote now does the full transformation
in one step, producing a complete executable spec directly.

### Replaced single explore.md with three stage-specific prompts
**Decision:** `explore.md` (stage-aware via `[STAGE:]` injection) replaced
by `explore-idea.md`, `explore-thinking.md`, `explore-initiative.md`.
**Rationale:** The three explore behaviors are genuinely different jobs —
expanding the why (idea), exploring the how (thinking), and narrowing
the implementation path (initiative). A single file with stage-switching
logic obscured this and made the prompt harder to maintain. Three files
is more code but clearer intent.

### Added explore limit — max 3 directions per run
**Decision:** All explore prompts produce exactly 3 directions, no more.
Each ends with an explicit "Explore Limit" signal stating what was
covered and when you're ready to critique.
**Rationale:** Explore without a constraint becomes procrastination.
The 3-direction limit forces prioritization. The explicit limit signal
tells you when you've genuinely explored enough vs. when you're avoiding
the critique.

### Critique rewritten with 0-10 scoring
**Decision:** All three critique prompts now produce a 0-10 score,
anchored at 7 (ready to promote), with what's strong and specifically
what to fix.
**Rationale:** Original critique was purely a judge — it found problems
but didn't tell you how to fix them. The scoring gives a clear promotion
gate. The "what to fix" section makes critique a coach, not just a
verdict. Each stage has its own rubric baked in, but all anchor at 7.

### Removed NOT READY blocker from promote-thinking-to-initiative.md
**Decision:** The prompt no longer outputs `NOT READY: reason` to block
promotion. Promotion is always the user's decision.
**Rationale:** The blocker added code complexity (brain.py would need
to detect and handle the signal) for a case the user can manage
themselves. Critique's score already tells you if something is ready.
If you choose to promote a note with a score of 4, that's your call.

### 30-initiatives split into drafting/active/done subfolders
**Decision:** Initiative specs live in `30-initiatives/drafting/`,
`30-initiatives/active/`, or `30-initiatives/done/` based on stage.
**Rationale:** Status-as-folder makes the pipeline visible in the
Obsidian sidebar without any plugins. Dataview can query a specific
folder (`FROM "30-initiatives/active"`) without needing frontmatter
status fields. The tradeoff is that file paths change on promote —
Obsidian's "automatically update internal links" setting handles this.

### brain initiative promote is a file move only
**Decision:** `brain initiative promote` moves the file from `drafting/`
to `active/` with no LLM call.
**Rationale:** By the time a spec scores ≥ 7 on critique, it's done.
There's nothing for the LLM to transform — it's already in its final
format. A promote that triggers an LLM call at this stage would change
a document that doesn't need changing. Execution tracking moves to Jira.

### Execution tracking in Jira, not Obsidian
**Decision:** Once an initiative is in `active/`, task-level tracking
happens in Jira. Obsidian holds the spec (the why and what). Jira holds
the tasks (the doing).
**Rationale:** Obsidian is a thinking tool, not a project management tool.
Building task tracking in Obsidian (Kanban plugin, Tasks plugin for
execution) duplicates Jira and creates two sources of truth for task
status. The initiative spec in Obsidian stays clean and doesn't become
a project board.

### Projects are standalone bubbles
**Decision:** Each project in `projects/` copies patterns from
`projects/_reference/` — never imports from it.
**Rationale:** Enables clean handoff to Cursor or a developer. Each
project is self-contained with its own `.env`, `requirements.txt`, and
copies of any shared code. If `_reference/` changes, existing projects
are unaffected. Eliminates import path complexity.

### Credentials never committed
**Decision:** `.env` files are in `.gitignore` and never committed.
`.env.example` files (no real values) are always committed.
**Rationale:** Credentials were accidentally committed in the initial
push (commit eaff67f). Four credentials were exposed: Atlassian API
token, Azure AD app secret, Salesforce consumer key, Salesforce consumer
secret. git filter-branch fix was applied. All four credentials should
be rotated. This entry exists so the incident is not forgotten.

### ABOUT.md files removed from all folders
**Decision:** Individual `ABOUT.md` files in each vault folder deleted.
Replaced by `_system/structure.md` which covers all folders in one place.
**Rationale:** ABOUT files created clutter in the sidebar and were
duplicating information that belongs in a single reference document.
A reader looking for folder definitions has one place to go.

---

## 2026-02-27

### Critique output format changed to aggregate + per-section
**Decision:** All three critique prompts now produce an aggregate score
followed by a per-section breakdown (strong/weak/fix for each section).
**Rationale:** Original format gave an overall verdict but didn't tell
you which specific sections needed work. Per-section breakdown makes
critique actionable — you know exactly what to fix without re-reading
the whole note to figure it out.

### Score framing changed from gate to advisory
**Decision:** Score ≥ 7 now "suggests readiness" rather than "means
ready to promote." All docs and prompts updated to reflect this.
**Rationale:** LLM scoring is inherently inconsistent. A 7 from one run
may be a 6 from the next. Framing the score as a gate incentivizes
gaming it rather than improving the actual thinking. You always decide
when to promote — the score is a signal, not a blocker.

### Kill command added
**Decision:** `brain idea kill`, `brain thinking kill`, and
`brain initiative kill` added. Moves file to local `archive/`, sets
`status: killed` in frontmatter. No LLM call.
**Rationale:** Ideas die, initiatives stall, things become irrelevant.
Without an explicit kill path, dead notes accumulate guilt and clutter.
Archive preserves them for reference without keeping them in active view.

### last-edited added to context block template
**Decision:** Context block frontmatter now includes `last-edited: YYYY-MM-DD`.
No automated audit command — just a visible field.
**Rationale:** Context blocks (OKRs, schemas, team structures) go stale.
A visible last-edited date lets you notice when something hasn't been
touched in months and decide whether it's still authoritative. Kept
simple — no new commands, no automated flagging.

### Shell Commands plugin adopted for Obsidian → brain.py integration
**Decision:** Shell Commands plugin replaces manual terminal entry for
brain.py operations. Commands pass `{{file_path}}` of current note.
**Rationale:** Retyping full file paths in terminal every time is friction.
Shell Commands lets you run any brain.py command against the current note
from Obsidian's command palette or a hotkey. Output shown in notification.
