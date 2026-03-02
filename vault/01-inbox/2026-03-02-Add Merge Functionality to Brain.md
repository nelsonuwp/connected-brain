---
type: idea
created: 2026-03-02
status: raw
---

# Add Merge Functionality to Brain

## The Idea
Need to add the ability to Merge 2 (or more) Ideas/Thoughts/Initiatives

## Why Now


## Context
Do I want to add the ability to _demote?_

This is in reference to the [[README]]

---

# Explore — 2026-03-02 09:00 ET

## Explore — 2026-03-02

### The Core Question
What does "merge" actually mean in this system, and where does the merged output land?

### Directions to Consider

**1. Same-stage merge (horizontal)**
Two ideas in `01-inbox/` combine into one stronger idea. Two thinking notes in `10-thinking/` synthesize into a unified approach. The inputs are peers; the output stays at the same stage but is more developed than either source.

This is the cleaner model — you're not skipping gates, just consolidating related work. The merged note inherits the best of both, goes through critique, promotes normally.

Open question: What happens to the source notes? Archive both with a `merged-into: [[new-note]]` backlink? Delete them? Leave them as stubs pointing to the merge?

**2. Cross-stage merge (vertical)**
An idea in `01-inbox/` has overlap with an initiative already in `drafting/`. You want to fold the idea's insight into the existing initiative without starting over.

This breaks the linear flow but matches real work. You don't always realize something is related until you're deeper in.

Open question: Does the idea get "consumed" (archived as merged) or does it need its own audit trail? If an initiative incorporates an idea, should that lineage be traceable?

**3. Merge as promotion shortcut**
Three related ideas are all circling the same problem. Instead of promoting each separately and merging the thinking notes, you promote-and-merge in one step — the output is a single thinking note synthesized from multiple ideas.

This saves effort but risks skipping the "is each idea worth pursuing" gate. Counter-argument: if you're confident enough to merge them, you've implicitly validated all three.

### Adjacent Questions

**Demote as inverse operation**
You asked about demotion. The interesting case: an initiative in `drafting/` turns out to have a flawed premise. The approach was wrong, not just underspecified. You want to demote it back to `10-thinking/` to rethink the how, preserving the work done but unlocking the locked stage.

This is different from merge but related — both are "the linear flow doesn't fit this situation" escape hatches.

**Merge scope**
Two notes in the same stage? Any two notes regardless of stage? Up to N notes? The answer shapes the implementation. Same-stage merge is simple. Cross-stage merge requires deciding which stage the output lands in.

### What I'd Surface

The simplest version that solves a real problem: `brain idea merge note1.md note2.md` — same stage only, output is a new note at that stage, sources archived with backlinks. No cross-stage, no three-way merge initially. Build the simple case, see if the complex cases actually arise.