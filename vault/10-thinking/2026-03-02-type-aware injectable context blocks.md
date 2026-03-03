---
type: thinking
status: raw
---

# type-aware injectable context blocks

## The Idea
Add a `type` field (code | business | content) to note frontmatter so brain.py auto-injects the matching context block from `20-context/types/` on every command, ensuring type-specific criteria are always present without manual `--context` flags.

## Why This Matters
Without type awareness, a code task gets critiqued the same way as a content piece—generic output that misses the real criteria (security, maintainability for code; narrative flow for content). Tasks are being added to the pipeline now, making this the right time to design type-aware behavior before the prompts are written. One injectable block per type works across the whole pipeline without duplicating type logic into every prompt file.

## What I Know
- Three types for v1: code, business, content—mapping to technical implementation, strategic decisions, and written output.
- Type lives in frontmatter (explicit and portable; folder inference breaks when projects mix types; content analysis is fragile).
- Injection not substitution—simpler to implement, sufficient because type blocks are static and don't need per-command variation.
- Type affects system context only for v1; output structure and command availability are separate ideas.
- Type blocks should stay under 200 tokens to avoid auto-pollution.
- Implementation estimate: 2–4 hours to add dynamic context loading to brain.py.

## What I Don't Know
- Whether three types will prove too coarse in practice (code splits into architecture vs. implementation vs. debugging; business splits into strategy vs. operations).
- Whether "code thinking" and "code task" using the same type block will cause tasks to get too much exploratory framing.
- Whether type × command variation will become necessary (e.g., `explore` on a code note needing different context than `critique` on the same note).

## Assumptions I'm Making
- Type is primary and command is secondary—static type blocks per note are sufficient without command-specific variation.
- Code thinking and code task can share a type block for v1 without degrading task output quality.
- Audience and constraint layering (technical vs. executive, time-bound vs. resource-limited) are not needed for v1.

## Risks and Constraints
- Type blocks could get stale and auto-injection becomes auto-pollution; mitigation is keeping blocks under 200 tokens and reviewing quarterly.
- brain.py doesn't currently support dynamic context loading—this is a blocker requiring implementation work.
- If three types prove too coarse, the system may need hierarchical types (e.g., `type: code/architecture`) with fallback, adding complexity.

## Next Step
Run `thinking explore` on this note to stress-test the type granularity decision and the assumption that command-specific variation isn't needed.

## Working Answers

**Q2 — Code type block draft:**
Evaluate for: correctness and edge case coverage, security and auth implications, test coverage, documentation impact, dependency risk. Avoid: narrative flow, audience framing, persuasion criteria.

**Q3 — Explore vs critique on same code note:**
Explore on code: needs expansive thinking — architecture options, tradeoffs, unknowns.
Critique on code: needs a checklist — security, maintainability, test coverage, docs.
These are not the same context. Type × command is probably necessary, not optional.

**Implication:** If Q3 is true, static type blocks are wrong. The right design is a small matrix: type sets the domain (what kind of work), command sets the lens (what to look for). 6 blocks (3 types × explore/critique) not 3. Implementation difference is probably 30 minutes, not 4 hours.


---

# Explore — 2026-03-02 18:57 ET

## Explore — 2025-03-02

### The Central Tension

You're betting that **type is stable and command-agnostic** — that a note's category (code/business/content) determines what criteria matter, regardless of what you're doing with that note. But your own uncertainty list suggests the opposite: "code thinking" vs. "code task" might need different framing, and `explore` vs. `critique` on the same note might need different context.

The design assumes type is the dominant axis. But the actual quality degradation you're trying to prevent (generic output missing real criteria) might be driven more by **what you're asking for** than **what the note is about**. A code note being explored needs expansive architectural thinking; the same note being critiqued needs security/maintainability checklists. Those aren't the same context block.

### What I'd Push On

**The "injection not substitution" decision hides the real question.** You chose injection because "type blocks are static and don't need per-command variation" — but that's the assumption under examination, not a known fact. If type × command variation becomes necessary, injection becomes insufficient and you've built infrastructure that needs rework.

**"Code thinking and code task can share a type block" is testable now.** Write the code type block. Apply it mentally to a thinking note and a task note you've already run through the system. Does the same 200 tokens serve both? If you're hedging while writing it, that's data.

**Three types maps to your current work, not to the domain.** Code/business/content is how *you* currently use the system. But "business" is doing a lot of work — strategy, operations, process design, people decisions. These have wildly different evaluation criteria. "Is this operationally sound?" vs. "Is this strategically coherent?" are not the same question.

**The 200-token constraint may be doing your thinking for you.** You set it to prevent auto-pollution, but it also prevents type blocks from being genuinely useful. If a meaningful code context block needs 400 tokens, the constraint forces you toward generic criteria — which is the problem you're solving.

### Questions You Need to Answer

1. What specific criteria are missing from current outputs that type blocks would add? Name three examples where generic critique failed and what type-aware critique would have caught.

2. If you wrote the code type block today, what would it say? Write it. Does it apply equally well to architecture thinking, implementation tasks, and debugging notes?

3. When you imagine running `critique` vs. `explore` on the same code note, do you want the same type context injected? If not, type × command is already necessary.

4. Is "business" actually one type, or is it a bucket for "not code, not content"? What happens when you try to write a single business type block that serves strategy notes and operational notes?

5. What's the cost of starting with type × command (6-9 blocks) vs. type-only (3 blocks)? If the implementation difference is small, the "simpler" argument weakens.

---

# Critique — 2026-03-02 18:59 ET

## Score: 7/10
Rework suggested — approach is defined but key assumptions need testing before implementation.

## Section Breakdown

### The Idea
**Strong:** Type in frontmatter is the right choice — explicit, portable, avoids fragile inference.
**Weak:** "One injectable block per type works across the whole pipeline" is stated as fact but contradicted by your own uncertainty in Q3.
**Fix:** Reframe as hypothesis: "Static type blocks may be sufficient for v1" — then test it by writing the actual blocks.

### Why This Matters
**Weak:** "Tasks are being added to the pipeline now" creates false urgency. The timing argument doesn't validate the design.
**Fix:** Remove the timing justification. The real reason is: current outputs are too generic. State what specific quality problems you've observed that type blocks would solve.

### What I Know
**Strong:** Implementation estimate and token budget are concrete constraints.
**Weak:** "Type affects system context only for v1; output structure and command availability are separate ideas" — this separation may be artificial. If explore vs. critique need different context, they're not separate.
**Fix:** Test whether explore/critique on the same note actually need different type context. If yes, this bullet is wrong.

### What I Don't Know
**Strong:** You've identified the right uncertainties — type granularity and command variation are the core questions.
**Weak:** These aren't unknowns to explore later — they're testable now and should block implementation.
**Fix:** Move these to "What I Need to Test" and make them blockers, not future concerns.

### Assumptions I'm Making
**Strong:** You've surfaced the critical assumption: "Type is primary and command is secondary."
**Weak:** This assumption directly contradicts your Q3 working answer, but you haven't resolved the conflict.
**Fix:** Either defend why type-only is sufficient despite Q3, or accept that the assumption is wrong and redesign around type × command.

### Working Answers
**Strong:** Q3 is excellent — you've identified that explore and critique need different context, which invalidates static type blocks.
**Weak:** The implication stops at "6 blocks not 3" but doesn't explore what those blocks would contain or whether the matrix is the right structure.
**Fix:** Draft one explore block and one critique block for code. If they're 80% the same, maybe command variation is overkill. If they're fundamentally different, the matrix is necessary.

### Missing Section: Validation Plan
**Weak:** You have no concrete test for whether three types are sufficient or whether type × command is necessary.
**Fix:** Add a section that specifies: (1) Write all three type blocks. (2) Apply each to 2-3 existing notes of that type. (3) Identify where the block fails to provide useful context. (4) Use failures to decide if command variation or type subdivision is needed.

### Next Step
**Weak:** "Run explore to stress-test" is recursive — you just did that. The actual next step is to write the blocks and test them.
**Fix:** Change to: "Draft code/business/content type blocks. Apply each to three existing notes. Document where generic context fails. Decide type-only vs. type × command based on failure patterns."