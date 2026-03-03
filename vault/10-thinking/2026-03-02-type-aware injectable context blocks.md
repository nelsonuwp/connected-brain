---
type: thinking
status: raw
---

# type-aware injectable context blocks

## The Idea
Add a type field (code | business | content) to note frontmatter so brain.py auto-injects the matching context block from 20-context/types/ — one block per type × command combination (explore vs. critique), ensuring type-specific criteria are always present without manual --context flags.

## Why This Matters
Without type awareness, a code task gets critiqued the same way as a content piece—generic output that misses the real criteria (security, maintainability for code; narrative flow for content). Tasks are being added to the pipeline now, making this the right time to design type-aware behavior before the prompts are written. One injectable block per type works across the whole pipeline without duplicating type logic into every prompt file.

## What I Know
- Three types for v1: code, business, content — technical implementation, strategic decisions, written output.
- Type lives in frontmatter — explicit and portable.
- Type × command is the correct model: 6 blocks (3 types × explore/critique). Type sets the domain, command sets the lens.
- Explore blocks: expansive — options, tradeoffs, unknowns. Critique blocks: checklist — security, maintainability, test coverage, docs (for code).
- Injection not substitution — simpler to implement, blocks are static per type × command pair.
- Type affects system context only for v1.
- Token budget: 200 per block. Implementation estimate: 2–4 hours.

## What I Need to Test
- Write code/business/content blocks for both explore and critique (6 blocks). Apply each to 2–3 existing notes. Where does the block fail to add useful context?
- Do code-thinking and code-task actually need different type blocks, or does the command split handle it?
- Is "business" one coherent type or a catch-all? Write the business blocks and see if they hold.

## Assumptions I'm Making
- ~~Type is primary and command is secondary~~ — Q3 invalidated this. Explore and critique need different context on the same note. Type × command is the correct model.
- Code thinking and code task can share a type block for v1 — still untested, but secondary to the explore/critique split.
- Audience and constraint layering are not needed for v1.

## Risks and Constraints
- Type blocks could get stale and auto-injection becomes auto-pollution; mitigation is keeping blocks under 200 tokens and reviewing quarterly.
- brain.py doesn't currently support dynamic context loading—this is a blocker requiring implementation work.
- If three types prove too coarse, the system may need hierarchical types (e.g., `type: code/architecture`) with fallback, adding complexity.

## Next Step
Draft the 6 type × command blocks (code/business/content × explore/critique). Apply each to existing notes. Document failures. Use failure patterns to decide if type subdivision is needed before implementing in brain.py.

## Working Answers

**Q2 — Code type block draft:**
Evaluate for: correctness and edge case coverage, security and auth implications, test coverage, documentation impact, dependency risk. Avoid: narrative flow, audience framing, persuasion criteria.

**Q3 — Explore vs critique on same code note:**
Explore on code: needs expansive thinking — architecture options, tradeoffs, unknowns.
Critique on code: needs a checklist — security, maintainability, test coverage, docs.
These are not the same context. Type × command is probably necessary, not optional.

**Implication:** If Q3 is true, static type blocks are wrong. The right design is a small matrix: type sets the domain (what kind of work), command sets the lens (what to look for). 6 blocks (3 types × explore/critique) not 3. Implementation difference is probably 30 minutes, not 4 hours.

## Draft Blocks (Partial)

**code-explore:** Surface architecture options and tradeoffs. Identify unknowns around dependencies, APIs, and edge cases. Flag integration risks. Do not evaluate correctness or completeness.

**code-critique:** Evaluate for correctness and edge case coverage, security and auth implications, test coverage, documentation impact. Do not explore alternatives — assess the proposal as stated.

**business-explore:** Surface strategic options and tradeoffs. Identify stakeholder dependencies and timing risks. Flag assumptions about resources or priorities.

**business-critique:** Evaluate for measurability of success criteria, clarity of ownership, and whether blockers are resolved. Do not reopen strategic options.


---

# Critique — 2026-03-02 19:45 ET

## Score: 7/10
Rework suggested — approach is defined and assumptions are surfaced, but options analysis is incomplete and several blocks remain unwritten.

## Section Breakdown

### The Idea
**Strong:** The core mechanism is clear — frontmatter type field triggers auto-injection of matching context blocks.
**Weak:** "one block per type × command combination" contradicts the earlier claim that "type is primary and command is secondary" — this tension is resolved later but creates confusion up front.
**Fix:** Remove the crossed-out assumption from "Assumptions I'm Making" and state clearly in The Idea that the design uses a 6-block matrix (3 types × 2 commands).

### Why This Matters
**Strong:** Clear motivation tied to current pipeline state.
**Weak:** "One injectable block per type works across the whole pipeline" is stated as fact but contradicts the type × command model you've already committed to.
**Fix:** Rewrite to say "One injectable block per type × command pair works across the whole pipeline" or remove the sentence entirely.

### What I Know
**Strong:** Type × command model is explicitly stated. Token budget and implementation estimate are concrete.
**Weak:** "Type affects system context only for v1" — what else could it affect in v2? This constraint is vague.
**Fix:** Either specify what v2 might add (e.g., "v2 may extend type to affect user context or output formatting") or remove the constraint if it's not load-bearing.

### What I Need to Test
**Strong:** All three test questions are specific and answerable.
**Weak:** "Do code-thinking and code-task actually need different type blocks" — this question is orthogonal to the type × command model. If command already splits explore/critique, what new split would thinking/task introduce?
**Fix:** Clarify what dimension thinking vs. task would add beyond explore vs. critique. If there's no clear answer, drop this test question.

### Assumptions I'm Making
**Weak:** The crossed-out assumption creates noise. The second assumption ("Code thinking and code task can share a type block for v1") is untested and potentially contradicts the type × command model.
**Fix:** Remove the crossed-out line entirely. Either test the thinking/task assumption or drop it — it's currently blocking clarity without adding value.

### Risks and Constraints
**Strong:** Stale block risk is identified with a concrete mitigation.
**Weak:** "brain.py doesn't currently support dynamic context loading" — is this actually a blocker or just implementation work? The note treats it as both.
**Fix:** Clarify whether this is a technical blocker (requires research or external dependency) or just unimplemented (requires 2–4 hours of work as stated earlier).

### Next Step
**Strong:** Clear action with a decision gate.
**Weak:** "Draft the 6 type × command blocks" but only 4 blocks are drafted below. The next step is incomplete.
**Fix:** Either draft all 6 blocks now or change Next Step to "Draft the remaining 2 blocks (content-explore and content-critique) and apply all 6 to existing notes."

### Draft Blocks (Partial)
**Strong:** The 4 drafted blocks are concrete and show clear differentiation between explore and critique.
**Weak:** Content type is entirely missing. Without content blocks, you cannot test whether the type × command model holds across all three types.
**Fix:** Draft content-explore and content-critique blocks before proceeding to testing. If you cannot write coherent content blocks, that's evidence the type model is wrong.

### Missing Section
**What's missing:** No section on "What happens if type is missing or invalid?" Does brain.py fail, warn, or fall back to a default block?
**Fix:** Add a brief section on fallback behavior — this will surface whether the system needs a default type or should reject untyped notes.