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
3. Across 50+ invocations spanning 20+ notes (minimum 5 per type), fewer than 30% of invocations require --context overrides. If any single type exceeds 40% override rate, that type is flagged for subdivision in a follow-up initiative — this initiative still ships with 3 types.
4. Missing or invalid type prints to stderr: [WARN] Note has no type specified — proceeding without type-specific context or [WARN] Note has invalid type '{value}' — proceeding without type-specific context. Execution continues in both cases.

## Constraints
- Three types only for v1: code, business, content
- No audience or constraint layering in v1
- Injection adds to system context; does not substitute existing context
- Blocks are static per type × command pair
- 200 token budget per block
- brain.py currently lacks dynamic context loading—implementation required
- - Block file path convention: 20-context/types/{type}-{command}.md — direct lookup, no registry for v1
- Injected block lands before command-specific prompt in system context
- Warning on invalid type (not just missing) — different message than missing, same behavior (proceed without injection)
- - Injected block is inserted into system context immediately before the command-specific prompt, after any existing generic context
- brain.py currently uses static prompt templates loaded at startup. Dynamic loading requires adding frontmatter parsing and runtime block lookup. Assume additive unless 30-minute spike reveals restructuring needed — if restructuring required, halt and re-scope.

## Non-Goals
- No type taxonomy beyond the initial 3 for v1
- No custom user-defined types
- No context injection for commands other than explore and critique
- No audience or constraint layering

## Open Questions
- Is "business" a coherent single type or a catch-all that will need subdivision? Testing against real notes will reveal this.
- If testing shows >30% override rate for a type, what subdivision scheme works best (hierarchical like `code/architecture` with fallback, or flat expansion)?
- Is "business" coherent or a catch-all? Testing will answer this. If >40% override rate, flag for subdivision in follow-up.
- Override rate measured per note or per invocation? Recommend per invocation — single problematic note skews note-based metrics.

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
2. Audit existing notes for type: frontmatter. Produce audit-report.md: count of notes by type, list of notes needing type added. Add type to any notes used in testing. Create testing-log.md documenting each test: note path, type, command, whether override was needed, why. Minimum 2 notes per type × command pair (12 total invocations).
3. Analyze testing-log.md. Analysis complete when: (a) override rate <30% for all types → proceed to step 4, or (b) override rate >30% for any type → document subdivision plan and decide whether to proceed or re-scope.
4. Implement dynamic loading: (a) parse frontmatter for type: field, (b) construct path 20-context/types/{type}-{command}.md, (c) read file if exists, (d) inject into system context immediately before command prompt. Test with one note per type confirming block content appears in LLM input.
5. Add warning behavior. Test: (a) note with type: invalid produces invalid-type warning, (b) note with no type: produces missing-type warning, (c) both cases proceed without injected block.

## Decisions Made
- Type × command matrix (6 blocks) over type-only (3 blocks)—explore needs expansive thinking while critique needs checklists, these are fundamentally different lenses
- Injection over substitution—simpler implementation, blocks remain static
- Warning on missing type rather than default block—surfacing data quality issues is better than masking them
- No fallback to generic block—untyped notes should produce generic output, not pretend to be typed

## Delegation State
| Person | Owns | By When | Level | Status |
| Solo | All steps | 2026-03-16 | Full ownership | Not started |

