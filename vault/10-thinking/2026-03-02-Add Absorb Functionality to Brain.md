---
type: thinking
status: raw
---

# Add Absorb Functionality to Brain

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

---

# Explore — 2026-03-02 09:11 ET

## Explore — 2026-03-02

### The Central Tension

You're building a consolidation primitive, but the deeper question is whether "absorb" is actually one operation or several wearing the same name. Merging two ideas in the same stage is fundamentally different from pulling fragments up into a more mature note, which is different again from collapsing duplicates. Each implies different rules about what content transfers, what metadata survives, and what the resulting note's "integrity" even means.

The risk is building a general-purpose "absorb" that's technically flexible but semantically ambiguous—users won't know when to use it versus link, and the archived sources will accumulate without clear meaning.

### What I'd Push On

**The directionality assumption may be too clean.** You've framed this as root-consumes-sources, but real consolidation often reveals that neither note should be the survivor—both are partial views of something that needs to be written fresh. Does absorb need a "synthesize into new" variant, or does that belong to a different operation entirely?

**"Absorbed" as a status creates a third state.** You have active notes and archived notes. Now you're proposing absorbed-and-archived, which is archived-but-with-lineage. What's the actual retrieval story? When would someone navigate *to* an absorbed note versus *through* it via the root? If the answer is "rarely," you're building traceability infrastructure that serves the system's integrity more than the user's workflow.

**The bloat problem is architectural, not cosmetic.** Collapsing absorbed content in the UI doesn't solve the underlying issue—if a root note has absorbed four sources, it now carries the cognitive load of five notes regardless of rendering. Is the right model actually *transclusion* (absorbed content lives elsewhere but renders inline) rather than *insertion* (content is copied into root)?

**Stage-crossing is where the real complexity lives.** You've flagged this but not resolved it. If absorb is strictly same-stage, you need a different mechanism for "this inbox fragment actually belongs to that existing initiative." If absorb is cross-stage, you're implicitly saying that stage boundaries are about *primary* notes, not about what content can appear where—which is a meaningful policy decision.

### Questions You Need to Answer

1. What is the *retrieval* use case for an absorbed note? If you can't articulate when someone would want to find it directly, the archiving scheme is serving auditability, not usability.

2. When two notes overlap but neither is clearly "root," what should the user do? If the answer is "pick one arbitrarily," the directionality model is a convenient simplification, not a reflection of how consolidation actually works.

3. Is absorbed content first-class or reference? Meaning: can the root note's absorbed section be edited, or is it a frozen snapshot? If editable, you've just copied content. If frozen, you have a hybrid document with two different editing modes.

4. What's the failure mode you're most worried about—fragmentation (too many notes, no consolidation) or premature synthesis (ideas collapsed before they're ready)? Absorb addresses the first but may accelerate the second.

5. How does this interact with the existing linking model? If I link note A from note B, then later absorb A into B, what happens to the link? What happens to *other* notes that linked to A?