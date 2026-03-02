---
type: thinking
status: raw
---

# Add Merge Functionality to Brain

## The Idea
Introduce an "Absorb" operation as a first-class primitive in the Brain system, allowing a root note to directionally consume one or more source notes by incorporating their content under a structured section while archiving the sources with backlinks to the root.

## Why This Matters
The current system assumes linear idea evolution, but real thinking produces overlap, fragments, and late-discovered connections. Without a consolidation mechanism, this leads to duplicated ideas across stages, fragmented context, and manual copy/paste with no traceability. Absorb enables progressive consolidation while preserving lineage and system integrity.

## What I Know
- Absorb is directional: one root survives and evolves, sources are consumed and archived
- Stage integrity is preserved — root stays in its stage, sources are archived (not promoted)
- Absorbed content appears under a dedicated section (e.g., `## Inputs / Absorbed Ideas`)
- Sources are marked with `status: absorbed`, `absorbed-into`, and `absorbed-at` metadata
- Initial CLI shape: `brain absorb root.md source1.md source2.md`
- Two potential modes: full absorb (includes raw context) vs. light absorb (key insights only)
- The author has already encountered this problem with overlapping ideas across inbox, thinking, and beyond

## What I Don't Know
- How should conflicts be handled if a source has already been absorbed elsewhere?
- What happens if someone tries to absorb a note that is upstream of the root (e.g., absorbing an initiative into an idea)?
- Should absorb support cross-stage operations or strictly same-stage?
- How does absorb interact with existing `## Inputs` sections that may already exist on the root?
- What triggers the decision to absorb vs. link vs. leave separate?
- How will absorbed content be rendered or collapsed in practice to avoid bloat?

## Assumptions I'm Making
- Archived notes remain accessible and searchable, not truly deleted
- The structured insertion format (`## Absorbed — [[source]]`) is flexible enough for all note types
- Users will manually identify which notes to absorb rather than relying on automated detection
- Light absorb summarization would be manual or delegated to a separate AI step, not built into the absorb command itself

## Risks and Constraints
- Absorb could become a dumping ground, creating bloated root notes that are harder to work with than the original fragments
- If not carefully scoped, absorb might blur the line between consolidation and premature synthesis
- The lack of automated overlap detection means absorb depends on user vigilance to identify candidates
- Archiving without clear UI/UX for "absorbed notes" could create a graveyard that's never revisited

## Next Step
Run thinking explore on this note to clarify the open questions around conflict handling, cross-stage rules, and the interaction with existing `## Inputs` sections.