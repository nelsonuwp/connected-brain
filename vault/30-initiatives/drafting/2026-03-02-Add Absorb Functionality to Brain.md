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