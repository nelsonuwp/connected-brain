---
type: idea
created: 2026-03-02
status: raw
---

# Add Merge Functionality to Brain

## The Idea

Introduce an **“Absorb” operation** as a first-class primitive in the Brain system.

Absorb allows a **root note** (idea, thinking, or initiative) to pull in one or more other notes, incorporating their content directly while preserving attribution. The absorbed notes are then **archived with a reference** to the root.

Instead of merging symmetrically, this is a **directional consolidation**:

- One note survives and evolves
    
- Others are consumed and traced
    

The absorbed content is added under a structured section (e.g. `## Absorbed — [[note]]`) with optional summarization and full raw context.

---

## Why it’s important

The current system assumes ideas evolve linearly, but real thinking doesn’t work that way.

You frequently:

- discover overlap between ideas late
    
- want to enrich a thinking note with earlier fragments
    
- need to consolidate without losing origin or context
    

Without a clean mechanism, this leads to:

- duplicated ideas across stages
    
- fragmented context
    
- manual copy/paste with no traceability
    

Absorb solves this by:

- preserving **lineage**
    
- reducing **idea sprawl**
    
- enabling **progressive consolidation** without breaking the stage model
    

---

## Why now

As the volume of ideas increases, overlap becomes inevitable.

You’ve already hit the problem:

- multiple related ideas across `inbox`, `thinking`, and beyond
    
- need to combine them without forcing everything into the same stage
    
- desire to maintain system integrity while staying flexible
    

If this isn’t solved early, the system will degrade into:

- duplicated work
    
- unclear “source of truth” notes
    
- hesitation to consolidate due to fear of losing context
    

Absorb is a **low-complexity, high-leverage primitive** that prevents that drift before it compounds.

---

## Context / Detail

Key design decisions:

**1. Directional, not symmetrical**

- Absorb is not “merge”
    
- One **root note** absorbs one or more **source notes**
    

---

**2. Stage integrity is preserved**

- Root note stays in its current stage
    
- Absorbed notes are archived, not promoted or merged across stages
    

---

**3. Structured insertion format**

## Absorbed — [[source-note]]  
  
### Key Points  
- distilled insights (optional but recommended)  
  
### Raw Context  
> full original content

---

**4. Archival with traceability**

Absorbed notes are not deleted, but marked:

status: absorbed  
absorbed-into: [[root-note]]  
absorbed-at: <timestamp>

---

**5. Centralized placement in root note**

All absorbed content lives under a dedicated section:

## Inputs / Absorbed Ideas

This prevents the main thinking from becoming fragmented or bloated.

---

**6. Multiple absorb modes (optional)**

- **Full absorb**: includes raw context
    
- **Light absorb**: only key insights, no full dump
    

---

**7. CLI shape (initial simple version)**

brain absorb root.md source1.md source2.md

- Appends structured sections to root
    
- Archives sources with backlinks
    
- No cross-stage logic required