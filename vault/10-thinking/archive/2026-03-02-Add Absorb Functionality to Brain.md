---
type: thinking
status: raw
---
## The Idea

Introduce an **“Absorb” operation** that allows a root note to incorporate one or more source notes by:

- extracting and summarizing key points from each source
    
- inserting both **Key Points** and **Raw Context** under a structured section (`## Absorbed — [[source]]`)
    
- marking the source note as `absorbed to [[root]]` and moving it to its stage-specific archive
    

This is a **directional operation** applied per source note. The root evolves, the source is archived.

Absorb can be performed **across any stages**, with no restrictions enforced by the system, because useful context often originates in earlier or parallel stages and needs to be consolidated into a more developed note without restructuring the system.

---

## Why This Matters

The system currently breaks down when ideas overlap or evolve non-linearly.

In practice:

- related ideas emerge at different times and in different stages
    
- useful context gets stranded in earlier notes
    
- consolidation is manual, inconsistent, and loses traceability
    

Without a defined mechanism, this leads to:

- duplicated or competing notes
    
- fragmented thinking across files
    
- hesitation to consolidate due to friction
    

This is already happening regularly — I encounter this consolidation problem **multiple times per week** when moving from idea → thinking or enriching existing notes.

Absorb provides a **repeatable, low-friction way to consolidate** while preserving where ideas came from.

---

## What I Know

- Absorb is **directional and per-source**: one root, one or more sources
    
- The root note **remains in place and continues evolving**
    
- Source notes are:
    
    - updated to `status: absorbed to [[root]]`
        
    - moved to their **existing stage archive folder**
        
- Absorbed content is inserted into the root as:
    
    - `## Absorbed — [[source]]`
        
    - `### Key Points` (summarized)
        
    - `### Raw Context` (full content)
        
- Absorb works **across any stage → any stage**, with no system constraints
    
- A note can be absorbed **multiple times**, including from archive (manually referenced if needed); no enforcement or blocking exists
    
- Existing links and backlinks are not modified
    
- All absorbed content is placed under a **single, consistent section** (e.g. `## Inputs / Absorbed Ideas`)
    

---

## What I Don't Know

- How consistent or high-quality the **Key Points summarization** will be in practice
    
    - Will evaluate after ~10–15 absorbs
        
- At what point a root note becomes **too large to be useful**
    
    - Will observe when navigation or scanning slows down
        
- Whether absorbing across stages will create confusion in more complex workflows
    
    - Will monitor during real usage rather than pre-optimizing
        
- Whether I will reliably choose absorb vs. link vs. leave separate without second-guessing
    
    - Will revisit after repeated hesitation or inconsistency shows up
        

---

## Assumptions I'm Making

- I will manually decide what to absorb and when, without needing automation or enforcement
    
- Simplicity is more valuable than correctness in edge cases
    
- Archived notes remain accessible via search and backlinks if needed
    
- Copying content (vs. transclusion) is acceptable and easier to manage
    
- I will use absorb primarily when a note no longer needs to stand alone
    
- My judgment on when to absorb may not be consistent initially, and I will refine heuristics after repeated use
    

---

## Risks and Constraints

- Root notes may become **bloated and harder to navigate**
    
    - Will split or refactor if absorbed sections become difficult to scan
        
- Absorb could be overused as a shortcut, leading to **premature consolidation**
    
    - Will avoid absorbing notes that are still actively evolving or uncertain
        
- Inconsistent summarization may reduce usefulness
    
    - Accepted for now; will refine format after repeated use
        
- Lack of constraints may lead to **messy lineage**
    
    - Accepted as tradeoff for simplicity and speed
        
- Archived notes may accumulate without a clear retrieval pattern
    
    - Accepted; primary access path is through the root note
        

---

## Success Criteria

I’ll know this is working if:

- I stop creating duplicate or overlapping notes for the same idea space
    
- Consolidation takes **less than 5 minutes per source note**
    
- I regularly rely on absorbed content when revisiting root notes
    
- I feel less friction when combining ideas across stages