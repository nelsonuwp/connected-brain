---
type: initiative
status: drafting
---

# Add Absorb Functionality to Brain

## One-Line Purpose
Enable directional consolidation of source notes into a root note while preserving traceability and archiving sources.

## Context
The current system breaks down when ideas overlap or evolve non-linearly across stages. Related ideas emerge at different times, useful context gets stranded in earlier notes, and manual consolidation is inconsistent and loses traceability. This consolidation problem occurs multiple times per week when moving from idea → thinking or enriching existing notes. Absorb provides a repeatable, low-friction mechanism to consolidate while preserving where ideas came from.

## Success Looks Like
1. Duplicate or overlapping notes for the same idea space stop being created
2. Consolidation takes less than 5 minutes per source note
3. Absorbed content is regularly relied upon when revisiting root notes
4. Reduced friction when combining ideas across stages

## Constraints
- Absorb is directional: one root note, one or more source notes per operation
- Root note remains in place and continues evolving
- Source notes must be updated to `status: absorbed to [[root]]` and moved to their stage-specific archive folder
- Absorbed content must be inserted under a consistent section structure (`## Absorbed — [[source]]` with `### Key Points` and `### Raw Context` subsections)
- No system-enforced restrictions on cross-stage absorption
- Existing links and backlinks are not modified
- Content is copied, not transcluded

## Open Questions
- **Summarization quality**: How consistent or high-quality will Key Points summarization be in practice? Matters because poor summaries reduce the value of the absorbed section. Will evaluate after 10–15 absorbs.
- **Root note size limits**: At what point does a root note become too large to be useful? Matters because bloated notes defeat the purpose. Will observe when navigation or scanning slows down.
- **Cross-stage confusion**: Will absorbing across stages create confusion in complex workflows? Matters for maintainability. Will monitor during real usage.
- **Decision consistency**: Will I reliably choose absorb vs. link vs. leave separate without second-guessing? Matters for workflow predictability. Will revisit after repeated hesitation shows up.

## Work Breakdown

### Files / Deliverables
- Absorb command/script that processes source notes and updates root notes
- Section template for absorbed content (`## Absorbed — [[source]]`, `### Key Points`, `### Raw Context`)
- Archive move logic that respects stage-specific archive folders
- Status update logic to set `status: absorbed to [[root]]` on source notes

### Sequence
1. Define the absorbed section template structure — establishes the format before any automation
2. Build the status update and archive move logic — ensures sources are properly marked and relocated
3. Build the content extraction and insertion logic — handles reading source content and placing it in root
4. Implement Key Points summarization — can start with manual or simple extraction, refine after usage
5. Integrate into a single absorb command — combines all steps into repeatable operation

## Decisions Made
- Absorb operates per-source note, not in bulk — keeps each consolidation traceable
- Content is copied, not transcluded — simpler to manage and more portable
- No system-enforced stage restrictions — useful context comes from anywhere
- Notes can be absorbed multiple times, including from archive — no blocking or enforcement
- All absorbed content goes under a single consistent section — predictable structure
- Archived notes remain accessible via search and backlinks — no special retrieval mechanism needed
- Simplicity is prioritized over correctness in edge cases — will refine heuristics after repeated use
- Root notes will be split or refactored if absorbed sections become difficult to scan — not pre-optimized

## Delegation State
| Person | Owns | By When | Level | Status |
| ------ | ---- | ------- | ----- | ------ |

---

# Critique — 2026-03-02 09:37 ET

## Score: 6/10
Rework suggested — spec is conceptually clear but lacks executable detail and testable success criteria.

## Section Breakdown

### One-Line Purpose
**Strong:** Clear and specific — directional consolidation with traceability is well-defined.

### Context
**Strong:** Problem is concrete and frequency-based ("multiple times per week").
**Weak:** No baseline measurement of current consolidation time or failure rate.
**Fix:** Add: "Current consolidation takes X minutes and loses source attribution Y% of the time" to establish improvement targets.

### Success Looks Like
**Weak:** All four criteria are subjective or unmeasurable.
- "Duplicate notes stop being created" — how is this measured? Over what time period?
- "Less than 5 minutes per source" — compared to what baseline? How is this timed?
- "Regularly relied upon" — what does "regularly" mean? How is reliance verified?
- "Reduced friction" — no measurement method specified.

**Fix:** Rewrite each criterion to be verifiable:
1. "Zero duplicate notes created for the same idea space over 4-week observation period (measured by manual audit)"
2. "Absorb operation completes in <5 minutes per source note, measured from command invocation to archive move (baseline: current manual process takes X minutes)"
3. "Absorbed sections referenced in at least 3 subsequent edits to root notes within 2 weeks (tracked via git history or manual log)"
4. "Consolidation hesitation drops to zero instances over 2-week period (tracked via decision log)"

### Constraints
**Strong:** Directional flow, status updates, section structure, and content copying are all specific.
**Weak:** "Consistent section structure" is defined but not enforced — how is consistency verified?
**Fix:** Add: "Section structure compliance verified by automated check before archive move" or specify manual review cadence.

### Open Questions
**Strong:** Each question includes why it matters and a measurement plan.
**Weak:** No decision triggers — when does an open question become a blocker vs. acceptable risk?
**Fix:** For each question, add: "Will block further absorbs if [specific condition]" or "Acceptable to proceed if [threshold not exceeded]."

### Work Breakdown — Files / Deliverables
**Weak:** Missing file paths, formats, and integration points.
- "Absorb command/script" — what language? Where does it live? How is it invoked?
- "Section template" — is this a string constant, a separate file, or part of the command?
- "Archive move logic" — how are stage-specific archive folders determined? Hard-coded map? Frontmatter-driven?
- "Status update logic" — does this modify YAML frontmatter? Plain text replacement?

**Fix:** Specify:
- Command location: `scripts/absorb.sh` or `src/commands/absorb.ts`
- Template location: inline constant in absorb command or `templates/absorbed-section.md`
- Archive folder resolution: "Read `stage` from source frontmatter, move to `{stage}/archive/`"
- Status update mechanism: "YAML frontmatter update using [specific library/tool]"

### Work Breakdown — Sequence
**Weak:** Steps are logical but not independently testable or completable.
- Step 1: "Define template structure" — what is the acceptance test? A markdown file? A code constant?
- Step 2: "Build status update and archive move logic" — how is this tested without the full command?
- Step 4: "Implement Key Points summarization" — contradicts "can start with manual" — is manual acceptable for initial release or not?
- Step 5: "Integrate into single command" — no integration test specified.

**Fix:** Rewrite each step with a testable outcome:
1. "Template structure defined and committed to `templates/absorbed-section.md` — verified by manual inspection"
2. "Status update and archive move logic functional in isolation — tested by running on 3 sample notes and verifying YAML change + file move"
3. "Content extraction inserts raw source content under `### Raw Context` — tested by absorbing 2 notes and diff-checking root note"
4. "Key Points summarization produces 3–5 bullet points per source — initially manual, automated after 10 absorbs — tested by reviewing 5 absorbed sections"
5. "Full absorb command runs end-to-end — tested by absorbing 3 notes across 2 stages and verifying all constraints met"

### Decisions Made
**Strong:** Clear stance on bulk operations, transclude vs. copy, and stage restrictions.
**Weak:** "Simplicity prioritized over correctness in edge cases" — which edge cases? What breaks?
**Fix:** List 2–3 specific edge cases being ignored (e.g., "circular absorbs not prevented," "concurrent edits to root note may conflict") and state acceptable failure mode for each.

### Delegation State
**Weak:** Table is empty — no owner, no timeline, no accountability.
**Fix:** Assign owner (even if self), set "By When" date for each Work Breakdown step, set Level (e.g., "Inform" if solo work, "Approve" if review needed), and Status ("Not Started").

### Missing Sections
**Weak:** No "How We'll Know It's Working" or rollback plan.
**Fix:** Add section: "Validation Plan" — specify how you'll verify success criteria after 2 weeks of use and what triggers a rollback (e.g., "if consolidation time exceeds 10 minutes 3+ times, revert to manual process").