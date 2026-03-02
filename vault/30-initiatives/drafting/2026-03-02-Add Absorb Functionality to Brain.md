---
type: initiative
status: drafting
---
## One-Line Purpose

Enable directional, programmatic consolidation of source notes into a root note while preserving traceability and automatically archiving sources.

## Context

The current system breaks down when ideas overlap or evolve non-linearly across stages. Related ideas emerge at different times, useful context gets stranded in earlier notes, and manual consolidation is inconsistent and loses traceability. Because manual copy-pasting breaks workflow and is highly annoying, the effort is often abandoned, leaving fragmented idea spaces. Absorb provides a repeatable, low-friction CLI mechanism to consolidate while enforcing programmatic flow and preserving exactly where ideas came from.

## Success Looks Like

1. **Zero duplicate notes** created for the same idea space over a 4-week observation period (measured by manual audit of the vault).
    
2. **Instant execution:** The absorb operation completes programmatically in < 1 minute per source note (compared to the manual copy-paste baseline which is annoying enough to cause 30%+ abandonment).
    
3. **High utility:** Absorbed sections are referenced in at least 3 subsequent edits to root notes within 2 weeks of being absorbed.
    
4. **Zero hesitation:** The decision to consolidate vs. link drops to zero hesitation over a 2-week period (tracked via mental check/decision log).
    

## Constraints

- **Directional:** One root note, one or more source notes per operation.
    
- **Top-level command:** Must be invoked via positional arguments: brain absorb <root_path> <source_path_1>[<source_path_2> ...]. First argument is the target, the rest are inputs.
    
- **Status update:** Source notes must be updated to status: absorbed to [[root]] and moved to their stage-specific archive folder.
    
- **Enforced structure:** The script must programmatically enforce the section structure: ## Absorbed — [[source]], containing ### Key Points (LLM-generated) and ### Raw Context (copied verbatim).
    
- **No linking changes:** Existing links and backlinks are not modified.
    
- **No transclusion:** Content is physically copied to ensure portability.
    

## Open Questions

- **Summarization quality:** How consistent or high-quality will the LLM-generated Key Points be? Decision trigger: If the summary is repeatedly inaccurate or misses context after 10 absorbs, we will downgrade the command to only paste Raw Context.
    
- **Root note size limits:** At what point does a root note become too bloated to be useful? Decision trigger: If scrolling/scanning the root note takes > 10 seconds, we will manually split the note and revisit the absorb UX.
    
- **Cross-stage confusion:** Will absorbing across stages create confusion? Decision trigger: Acceptable risk. Will monitor during real usage and add validation warnings later only if it breaks the mental model.
    

## Work Breakdown

### Files / Deliverables

- **CLI Command:** A new top-level Typer command in brain.py: @app.command("absorb") utilizing variable-length positional arguments.
    
- **Prompt File:** vault/_prompts/summarize-absorbed.md (configured to use MODEL_WORKHORSE / Sonnet 4.5 for Key Points generation).
    
- **Frontmatter update logic:** Extend _set_frontmatter_status in brain.py to support setting status: absorbed to [[parent_note_name]].
    
- **Archiving logic:** Reuse existing archive_file helper in brain.py to route to appropriate stage archives.
    

### Sequence

1. **Scaffold the CLI:** Build the @app.command("absorb") in brain.py with positional Typer arguments (first arg = root, rest = list of sources). Testable outcome: Command parses arguments and fails cleanly if any file does not exist.
    
2. **Build extraction & formatting:** Implement reading the source file(s) and assembling the ## Absorbed and ### Raw Context text. Testable outcome: Running on dummy files correctly appends the raw text to the parent note.
    
3. **Implement LLM Summarization:** Add the ai_client.call step using MODEL_WORKHORSE to generate the ### Key Points bullet list. Testable outcome: Verify the LLM correctly summarizes the source note in the final output.
    
4. **Build source archiving:** Implement the frontmatter update (absorbed to [[root]]) and trigger archive_file for each source note. Testable outcome: Source notes successfully move to their respective /archive/ folders with updated YAML.
    
5. **End-to-End Test:** Run the full flow on 2 overlapping idea notes into a thinking note. Testable outcome: Parent note has combined context, source notes are archived, and no critical errors occurred.
    

## Decisions Made

- **User Error is Permitted:** The command will allow you to do "stupid" things (like absorbing an already-absorbed note, or creating circular references). Simplicity and lack of friction are prioritized.
    
- **Critical Errors Fail Hard:** The script will throw an immediate fatal error if the target root note or any of the source files do not exist.
    
- **Automated Summaries from Day 1:** Using claude-sonnet-4-5 (MODEL_WORKHORSE) to generate summaries automatically, rather than leaving it blank for manual entry.
    
- **Bulk absorbing:** Supported out of the box via multiple positional arguments for source files, allowing rapid multi-file consolidation in one command.
    

## Delegation State

|   |   |   |   |   |
|---|---|---|---|---|
|Person|Owns|By When|Level|Status|
|Self|Full Implementation|End of Week|Execute|Not Started|

## Validation Plan

- **Review Cadence:** Audit the results after 2 weeks of organic usage (approx. 10-15 operations).
    
- **Rollback Trigger:** If the programmatic flow takes longer than manual copying due to LLM latency, or if the vault becomes cluttered with broken archive links, we will disable the command and revert to manual consolidation until the UX is fixed.

---

# Critique — 2026-03-02 10:03 ET

## Score: 7/10
Rework suggested — execution would stall on ambiguities in the Work Breakdown and missing validation criteria.

## Section Breakdown

### One-Line Purpose
**Strong:** Clear directional flow (source → root), explicit preservation of traceability, automatic archiving.

### Context
**Strong:** Articulates the pain point (manual copy-paste abandonment) and positions Absorb as a programmatic solution.

### Success Looks Like
**Weak:** Criterion 1 ("Zero duplicate notes") is not testable — "duplicate" is undefined and "manual audit" is not a verification method. Criterion 3 ("referenced in at least 3 subsequent edits") has no measurement mechanism. Criterion 4 ("zero hesitation") relies on a "mental check/decision log" that doesn't exist in the spec.

**Fix:** 
- Criterion 1: Define "duplicate" (e.g., "two notes with identical ## One-Line Purpose or overlapping first 100 words") and specify the audit method (e.g., "run `brain list --duplicates` or grep for pattern X").
- Criterion 3: Specify how "referenced" is measured (e.g., "appears in git diff of root note within 2 weeks" or "backlink count increases by 3+").
- Criterion 4: Either drop this criterion or specify the log format and commit to maintaining it (e.g., "daily log entry in `_meta/absorb-decisions.md` with timestamp and choice").

### Constraints
**Strong:** Directional flow, positional CLI args, status update format, section structure enforcement, no linking changes, no transclusion.

### Open Questions
**Weak:** Decision triggers are vague. "Repeatedly inaccurate" (how many times?), "scrolling/scanning takes > 10 seconds" (measured how? by whom?), "breaks the mental model" (what does this look like?).

**Fix:** 
- Summarization quality: "If 3 out of 10 absorbs produce Key Points that omit critical context (as judged by manual review), downgrade to Raw Context only."
- Root note size: "If any root note exceeds 500 lines or 3000 words, manually split and revisit UX."
- Cross-stage confusion: "If 2+ users report confusion or if a post-mortem reveals a broken workflow, add validation warnings."

### Work Breakdown — Files / Deliverables
**Weak:** "Prompt File" deliverable is incomplete — no spec for what the prompt should contain or how it should be structured. "Extend _set_frontmatter_status" is vague — does this function already exist? If so, what exactly changes?

**Fix:** 
- Add: "Create `vault/_prompts/summarize-absorbed.md` with template: 'Summarize the following note into 3-5 bullet points highlighting key insights and decisions. Input: {{source_content}}. Output format: markdown bullet list.'"
- Clarify: "Modify `_set_frontmatter_status` to accept optional `parent_note_name` parameter and write `status: absorbed to [[parent_note_name]]` if provided."

### Work Breakdown — Sequence
**Weak:** Step 1 "fails cleanly if any file does not exist" contradicts Decisions Made ("Critical Errors Fail Hard"). Step 3 "verify the LLM correctly summarizes" has no pass/fail criteria. Step 5 "no critical errors occurred" is not specific.

**Fix:** 
- Step 1: Change to "Command parses arguments and raises FileNotFoundError with exit code 1 if any file does not exist."
- Step 3: Add pass criteria: "LLM output is valid markdown, contains 3-5 bullet points, and does not exceed 200 words."
- Step 5: Replace "no critical errors" with "root note contains exactly 2 new ## Absorbed sections, both source notes are in `/archive/`, and `git diff` shows expected changes only."

### Decisions Made
**Strong:** Clear stance on user error tolerance, critical error handling, automated summaries, bulk absorbing.

### Delegation State
**Weak:** "End of Week" is not a date. "Execute" level is correct but "Not Started" status will immediately be stale.

**Fix:** Replace "End of Week" with explicit date (e.g., "2026-03-07"). Consider changing status to "Scheduled" or removing the Status column entirely if it's not maintained programmatically.

### Validation Plan
**Weak:** "Audit the results after 2 weeks" has no owner, no specific audit method, and no pass/fail criteria. "10-15 operations" is an assumption, not a measurement. Rollback trigger "LLM latency" has no threshold.

**Fix:** 
- Add owner: "Self will audit on 2026-03-16 by reviewing git log for absorb operations and manually inspecting 5 random root notes."
- Replace "10-15 operations" with "at least 10 operations (tracked via `git log --grep='absorb'`)."
- Rollback trigger: "If any absorb operation takes > 2 minutes end-to-end, or if 3+ archive links are broken (verified by `brain validate-links`), disable command and revert."