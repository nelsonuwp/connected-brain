---
type: thinking
status: raw
---

# type-aware injectable context blocks

## The Idea
Add a type field (code | business | content) to note frontmatter so brain.py auto-injects the matching context block from 20-context/types/ — 6 blocks (3 types × 2 commands: explore/critique), ensuring type-specific criteria are always present without manual --context flags.

## Why This Matters
Without type awareness, a code task gets critiqued the same way as a content piece—generic output that misses the real criteria (security, maintainability for code; narrative flow for content). Tasks are being added to the pipeline now, making this the right time to design type-aware behavior before the prompts are written. One injectable block per type × command pair works across the whole pipeline.

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
- Is "business" one coherent type or a catch-all? Write the business blocks and see if they hold.

## Assumptions I'm Making
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

**content-explore:** Surface angle and framing options. Identify audience assumptions. Flag gaps in argument or narrative structure. Do not evaluate polish or correctness.

**content-critique:** Evaluate clarity of core message, audience fit, and whether the argument holds. Flag structural gaps or unsupported claims. Do not reopen framing options.

## Fallback Behavior
If type is missing or invalid, brain.py should warn and proceed without injection — not fail silently or halt. A default type block would mask missing frontmatter, which is worse than generic output. Untyped notes are a data quality problem, not a runtime error.
