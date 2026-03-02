---
status: active
type: initiative
---

## One-Line Purpose
Enable low-friction, traceable consolidation of overlapping notes into a single root note, with sources automatically archived.

## Context
Ideas and thoughts emerge non-linearly. A new inbox capture often overlaps with an existing thinking note; two ideas cover the same ground from different angles. The current system has no mechanism for this — the only options are manual copy-paste (lossy, slow, breaks traceability) or letting the fragments sit unconnected. Absorb solves this with a single CLI command: point it at a root and one or more sources, and it pulls the content in, summarizes it, and archives the sources cleanly.

## Success Looks Like
1. Running `brain absorb` requires no mental overhead — one command, done.
2. Every absorbed section is traceable back to its source note by name.
3. Source notes are archived with updated frontmatter — not left floating in their original folders.
4. The LLM-generated Key Points are accurate enough that I don't need to re-read the source note to understand what was absorbed.

## Constraints
- **Directional:** One root note, one or more source notes per operation. Root note is always the first argument.
- **Top-level command:** `brain absorb <root_path> <source_path_1> [<source_path_2> ...]`
- **Root note is append-only:** No changes to root note frontmatter, status, or existing content — only new `## Absorbed` sections are appended at the end.
- **Enforced section structure per source:**
```
  ## Absorbed — [[source_stem]]
  ### Key Points
  <LLM-generated bullet list>
  ### Raw Context
  <verbatim source note content>
```
- **Source archiving:** Each source note gets `status: absorbed to [[root_stem]]` written into its frontmatter, then moved to its stage-appropriate `archive/` folder using the existing `archive_file` helper.
- **No stage restrictions:** Any note can be absorbed into any other note regardless of stage. User is responsible for whether this makes sense.
- **No transclusion:** Content is physically copied for portability.
- **No link modification:** Existing wikilinks and backlinks are untouched.
- **User error is permitted:** The command will not prevent absorbing already-absorbed notes or circular references. Simplicity over safety rails.
- **Critical errors fail hard:** Missing root or source files raise an immediate fatal error and exit.
- **Error handling:** If the LLM call fails, fall back to appending Raw Context only with a `[WARNING: LLM failed, Key Points skipped]` line in place of the Key Points section. No crash.

## Open Questions
- **Summarization quality:** How consistent will the Key Points be? Decision trigger: if 3 out of 10 absorbs produce Key Points that miss a decision or constraint visible in Raw Context (judged by Self), switch the prompt to be more directive or downgrade to Raw Context only.
- **Root note bloat:** No hard size limit enforced by the tool, but if any root note becomes unwieldy after absorbs, Self will manually split it and document the criteria in a new note.
- **Idempotency:** Running absorb twice on the same source will duplicate the `## Absorbed` section. The command will print a `[WARNING: source already appears absorbed]` notice if it detects an existing `## Absorbed — [[source_stem]]` block in the root note, but will proceed anyway.

## Work Breakdown
### Files / Deliverables
- **CLI command:** `@app.command("absorb")` in `brain.py` with positional Typer arguments (root + variadic sources).
- **Prompt file:** `vault/_prompts/summarize-absorbed.md` — model: workhorse, system prompt: "Summarize the provided note into 3–5 bullet points highlighting key insights, constraints, and decisions. Output markdown bullet list only, no preamble."
- **Frontmatter helper:** `_set_absorbed_frontmatter(content: str, root_stem: str) -> str` — sets `status: absorbed to [[root_stem]]` in source frontmatter.

### Sequence
1. **Scaffold CLI:** Build `@app.command("absorb")` with argument parsing. Testable outcome: command parses args and raises `FileNotFoundError` with exit code 1 if any file is missing.
2. **Build Raw Context assembly:** Read each source and assemble the `## Absorbed` + `### Raw Context` block. Testable outcome: running on dummy files appends correctly-structured raw sections to the root note.
3. **Add LLM summarization:** Call `ai_client.call` with MODEL_WORKHORSE to generate `### Key Points`. Testable outcome: output is valid markdown with 3–5 bullet points and no preamble; on simulated failure, fallback Warning line appears instead.
4. **Source archiving:** Apply `_set_absorbed_frontmatter` and call `archive_file` for each source. Testable outcome: source notes move to their `/archive/` folder with correct frontmatter.
5. **End-to-end test:** Run on 2 overlapping idea notes absorbed into a single thinking note. Testable outcome: root note has exactly 2 new `## Absorbed` sections; both source notes are in `01-inbox/archive/` with `status: absorbed to [[root]]`; root note frontmatter is unchanged.

## Decisions Made
- **Any stage into any stage:** No restrictions enforced. User decides what makes sense.
- **Root note append-only:** Absorb never modifies existing root note content or metadata.
- **LLM summary always on:** Key Points are always generated; no flag to skip.
- **Bulk absorbing supported:** Multiple source paths in one command.
- **User error is permitted:** No guards against duplicates or circular absorbs — friction kept minimal.

## Delegation State
| Person | Owns | By When | Level |
|--------|------|---------|-------|
| Self | Working `brain absorb` command passing all 5 testable outcomes | 2026-03-07 | Execute |

## Validation Plan
Self will review on 2026-03-16: check git log for absorb operations, manually inspect root notes from those operations, and confirm Key Points quality held up. Rollback trigger: if any absorb takes > 2 minutes end-to-end or leaves broken wikilinks (verified by `obsidian-link-checker`), disable and revert to manual consolidation.

---

# Critique — 2026-03-02 11:30 ET

## Score: 9/10
Strong — consider promoting

## Section Breakdown

### One-Line Purpose
**Strong:** Clear, specific, and matches the actual command behavior described later.

### Context
**Strong:** Explains the problem concretely (overlapping notes, no consolidation mechanism) and positions Absorb as the solution.

### Success Looks Like
**Strong:** All four criteria are testable and specific.
**Weak:** Criterion 4 ("accurate enough that I don't need to re-read") is subjective and conflicts with the Open Questions section, which acknowledges summarization quality is unknown.
**Fix:** Either remove criterion 4 or reframe it as "Key Points capture the main decision/constraint from each source note" and tie it to the decision trigger already defined in Open Questions (3 out of 10 threshold).

### Constraints
**Strong:** Exceptionally detailed. Section structure is specified character-for-character. Error handling is explicit. Fallback behavior for LLM failure is defined. The "user error is permitted" stance is clear and intentional.

### Open Questions
**Strong:** Each question has a concrete decision trigger or resolution path. The 3-out-of-10 threshold for summarization quality is testable.

### Work Breakdown — Files / Deliverables
**Weak:** The prompt file specifies "3–5 bullet points" but Success Looks Like criterion 4 and the LLM fallback in Constraints don't enforce this range — if the LLM returns 2 bullets or 7 bullets, is that a failure?
**Fix:** Either remove the bullet count from the prompt spec or add a validation step in sequence step 3 that checks bullet count and logs a warning if out of range.

### Work Breakdown — Sequence
**Strong:** Each step has a specific testable outcome. Step 5 end-to-end test is concrete and verifiable.
**Weak:** Step 4 says "call `archive_file` for each source" but does not specify what happens if `archive_file` fails partway through (e.g., source 1 archives successfully, source 2 fails due to filesystem error). Does the command roll back? Does it leave source 1 archived and source 2 in place?
**Fix:** Add to step 4 testable outcome: "If any archive operation fails, command exits with error code 1 and prints which source failed — no rollback of prior sources."

### Decisions Made
**Strong:** Each decision directly addresses a potential design fork and commits to a specific path.

### Delegation State
**Strong:** Single owner, specific deadline, clear deliverable tied to the 5 testable outcomes in Sequence.

### Validation Plan
**Strong:** Specific date, specific checks (git log, manual inspection, link checker), and a concrete rollback trigger (>2 minutes or broken links).
**Weak:** The rollback trigger "broken wikilinks" is not caused by anything in the spec — Constraints explicitly say "No link modification: Existing wikilinks and backlinks are untouched." This is an internal contradiction.
**Fix:** Remove "broken wikilinks" from the rollback trigger, or clarify what scenario would cause them (e.g., if archiving a source note breaks a link *to* that note from elsewhere, which is expected behavior and not a bug).

---

**Missing Section:** None — all expected sections are present.

**Internal Contradictions:**
1. Success criterion 4 vs. Open Questions on summarization quality (flagged above).
2. Validation Plan rollback trigger mentions broken wikilinks, but Constraints say links are untouched (flagged above).