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

Absorb can be performed **across any stages**, with no restrictions enforced by the system.

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
    
- Multiple absorbs of the same note are allowed (no enforcement or blocking)
    
- Existing links and backlinks are not modified
    
- All absorbed content is placed under a **single, consistent section** (e.g. `## Inputs / Absorbed Ideas`)
    

---

## What I Don't Know

- How consistent or high-quality the **Key Points summarization** will be in practice
    
- At what point a root note becomes **too large to be useful**, and how often that will occur
    
- Whether absorbing across stages will create confusion in more complex workflows
    
- Whether I will reliably choose absorb vs. link vs. leave separate without second-guessing
    
- How often previously absorbed notes will need to be revisited directly
    

---

## Assumptions I'm Making

- I will manually decide what to absorb and when, without needing automation or enforcement
    
- Simplicity is more valuable than correctness in edge cases
    
- Archived notes remain accessible via search and backlinks if needed
    
- Copying content (vs. transclusion) is acceptable and easier to manage
    
- I will use absorb primarily when a note no longer needs to stand alone
    
- Occasional duplication or re-absorption is acceptable and not worth preventing
    

---

## Risks and Constraints

- Root notes may become **bloated and harder to navigate** over time
    
- Absorb could be overused as a shortcut, leading to **premature consolidation**
    
- Inconsistent summarization may reduce the usefulness of absorbed sections
    
- Lack of constraints may lead to **messy or non-obvious lineage**
    
- Archived notes may accumulate without a clear retrieval pattern