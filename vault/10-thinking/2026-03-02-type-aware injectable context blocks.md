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