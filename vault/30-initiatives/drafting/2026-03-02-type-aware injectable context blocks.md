---
type: initiative
status: drafting
---

# type-aware injectable context blocks

## One-Line Purpose
Auto-inject domain-specific context into brain.py commands based on note type, so code/business/content tasks get evaluated against appropriate criteria without manual flags.

## Context
Currently all notes receive identical generic context regardless of domain—a code architecture note gets the same critique framing as a blog post. With tasks entering the pipeline, this is the right moment to add type awareness before prompts proliferate. The design uses a type × command matrix (6 blocks total) where type sets the domain and command sets the lens.

## Success Looks Like
1. Notes with `type: code|business|content` in frontmatter automatically receive the matching context block when running explore or critique commands
2. Each of the 6 blocks (3 types × 2 commands) stays under 200 tokens
3. Fewer than 30% of notes in any single type require manual `--context` overrides during testing
4. Missing or invalid type produces a warning and proceeds without injection—no silent failures, no halts

## Constraints
- Three types only for v1: code, business, content
- No audience or constraint layering in v1
- Injection adds to system context; does not substitute existing context
- Blocks are static per type × command pair
- 200 token budget per block
- brain.py currently lacks dynamic context loading—implementation required

## Open Questions
- Is "business" a coherent single type or a catch-all that will need subdivision? Testing against real notes will reveal this.
- If testing shows >30% override rate for a type, what subdivision scheme works best (hierarchical like `code/architecture` with fallback, or flat expansion)?

## Work Breakdown

### Files / Deliverables
- `20-context/types/code-explore.md`
- `20-context/types/code-critique.md`
- `20-context/types/business-explore.md`
- `20-context/types/business-critique.md`
- `20-context/types/content-explore.md`
- `20-context/types/content-critique.md`
- Modified `brain.py` with dynamic context loading based on frontmatter type field

### Sequence
1. Draft all 6 type × command blocks using the partial drafts as starting points
2. Apply each block to 2–3 existing notes manually; document where blocks fail to add useful context
3. Analyze failure patterns to determine if type subdivision is needed before code changes
4. Implement dynamic context loading in brain.py (reads type from frontmatter, loads matching block from `20-context/types/`)
5. Add warning behavior for missing/invalid type

## Decisions Made
- Type × command matrix (6 blocks) over type-only (3 blocks)—explore needs expansive thinking while critique needs checklists, these are fundamentally different lenses
- Injection over substitution—simpler implementation, blocks remain static
- Warning on missing type rather than default block—surfacing data quality issues is better than masking them
- No fallback to generic block—untyped notes should produce generic output, not pretend to be typed
- Quarterly review cadence for block staleness

## Delegation State
| Person | Owns | By When | Level | Status |
| ------ | ---- | ------- | ----- | ------ |