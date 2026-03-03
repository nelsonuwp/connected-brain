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
3. Aggregate override rate across all types is <30%. Initiative ships regardless of outcome. Testing dataset: minimum 50 total invocations (5 notes per type × 2 commands = 30 base invocations, plus 20+ repeat invocations for consistency). Post-ship: if any single type shows ≥40% override rate, document subdivision plan for follow-up initiative.
4. Missing or invalid type prints to stderr: [WARN] Note has no type specified — proceeding without type-specific context or [WARN] Note has invalid type '{value}' — proceeding without type-specific context. Execution continues in both cases. Command executes using only generic context. Exit code is 0. Warnings appear in stderr only.

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
- Injected block is inserted into system context immediately before the command-specific prompt, after any existing generic context
- brain.py currently uses static prompt templates loaded at startup. Dynamic loading requires adding frontmatter parsing and runtime block lookup. Assume additive unless 30-minute spike reveals restructuring needed — if restructuring required, halt and re-scope.
- Step 0 spike is a go/no-go gate. If restructuring required, halt and create new initiative. Proceed to step 1 only if additive confirmed. Spike documents current context structure in spike-report.md.

## Non-Goals
- No type taxonomy beyond the initial 3 for v1
- No custom user-defined types
- No context injection for commands other than explore and critique
- No audience or constraint layering

## Open Questions
- Is "business" coherent or a catch-all? Testing will answer this. If >40% override rate per invocation, flag for subdivision in a follow-up initiative.
- Override rate measured per invocation — single problematic note shouldn't skew results.

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
0. 30-minute spike: confirm brain.py prompt loading is additive (not requiring restructure). Document current context structure in spike-report.md. If restructuring required, halt and create new initiative. Proceed to step 1 only if additive confirmed.
1. Draft all 6 type × command blocks using the partial drafts as starting points
2. Audit existing notes for type: frontmatter. Produce audit-report.md: count of notes by type, list of notes needing type added. Add type to any notes used in testing. Create testing-log.md documenting each test: note path, type, command, whether override was needed, why. Minimum 5 notes per type × command pair (30 invocations minimum). Add 20+ repeat invocations for consistency. Target 50+ total.
3. Analyze testing-log.md. Calculate aggregate override rate. If <30%, proceed to step 4. If ≥30%, document in analysis-report.md and proceed anyway — initiative ships regardless. If any single type ≥40%, document subdivision plan for follow-up initiative.
4. Implement dynamic loading: (a) parse frontmatter for type: field, (b) construct path 20-context/types/{type}-{command}.md, (c) read file if exists, (d) inject into system context immediately before command prompt. Test with one note per type confirming block content appears in LLM input. Verification: add temporary debug logging to print full system message to stderr. Confirm block text appears between generic context and command prompt. Remove debug logging after verification.
5. Add warning behavior. Test: (a) note with type: invalid produces invalid-type warning, (b) note with no type: produces missing-type warning, (c) both cases proceed without injected block. Verify for both cases: (a) warning prints to stderr with correct text, (b) exit code 0, (c) output generated, (d) output uses generic context only.

## Decisions Made
- Type × command matrix (6 blocks) over type-only (3 blocks)—explore needs expansive thinking while critique needs checklists, these are fundamentally different lenses
- Injection over substitution—simpler implementation, blocks remain static
- Warning on missing type rather than default block—surfacing data quality issues is better than masking them
- No fallback to generic block—untyped notes should produce generic output, not pretend to be typed
- Warning on missing type rather than silent fallback — user notified via stderr, execution continues with generic context. Surfaces data quality gap without blocking workflow.

## Delegation State
| Person | Owns | By When | Level | Status |
| ------ | ---- | ------- | ----- | ------ |
| Solo | All steps | 2026-03-16 | Full ownership | Not started |
| Solo | All steps | 2026-03-16 | Full ownership | Not started — Step 0: 0.5d, Step 1: 2d, Step 2: 4d, Step 3: 0.5d, Step 4: 4d, Step 5: 1d = 12d + 2d buffer |

## Definition of Done
- All 6 block files exist in 20-context/types/ and are under 200 tokens each
- brain.py parses frontmatter and injects matching block per type × command
- testing-log.md documents 50+ invocations with <30% aggregate override rate
- Warnings print to stderr for missing/invalid type; execution continues with exit 0
- spike-report.md documents context structure and confirms additive approach
- Warnings for missing/invalid type print to stderr and do not change exit code (remains 0)


---

# Critique — 2026-03-02 20:03 ET

## Score: 6/10
Rework suggested — execution would stall on ambiguous success criteria and missing implementation details.

## Section Breakdown

### One-Line Purpose
**Strong:** Clear value proposition — type-aware context improves domain relevance without manual intervention.

### Success Looks Like
**Weak:** Criterion 3 has contradictory logic. "Initiative ships regardless of outcome" conflicts with "if any single type shows ≥40% override rate, document subdivision plan." Does the initiative ship if business shows 45% override? The 30% aggregate vs 40% per-type thresholds create confusion about what blocks shipping.

**Fix:** Separate shipping criteria from post-ship analysis. Rewrite criterion 3 as: "Aggregate override rate measured across minimum 50 invocations (5 notes × 3 types × 2 commands = 30 base + 20 repeat). Initiative ships regardless of rate. Post-ship: if aggregate >30% OR any single type ≥40%, document findings in analysis-report.md and create follow-up initiative for refinement."

**Weak:** Criterion 4 specifies warning text but doesn't define what "proceeds without type-specific context" means for the output. Does the LLM receive a placeholder block? Generic context only? Nothing?

**Fix:** Add to criterion 4: "Command executes using only generic context (no type-specific block injected). LLM receives standard system prompt without type augmentation."

### Constraints
**Weak:** "Assume additive unless 30-minute spike reveals restructuring needed" creates a hidden dependency. If the spike fails, the entire initiative halts, but this isn't reflected in Success Looks Like or Definition of Done.

**Fix:** Move spike to Success Looks Like as criterion 0: "Step 0 spike confirms brain.py context loading is additive (documented in spike-report.md). If restructuring required, halt and create new initiative." Make it a go/no-go gate before step 1.

**Weak:** "Injected block lands before command-specific prompt" — where exactly? Before all system context? After generic context? Between two existing blocks?

**Fix:** Specify exact insertion point: "Injected block is inserted into system context immediately before the command-specific prompt, after any existing generic context. Order: [generic context] → [type block] → [command prompt]."

### Open Questions
**Weak:** "Override rate measured per invocation" is stated here but not defined in Success Looks Like. What constitutes an override? Manual flag addition? Block content rejection?

**Fix:** Move definition to Success Looks Like criterion 3: "Override = any invocation where user manually adds flags or edits block content before execution. Measured per invocation (not per note) to avoid skew from single problematic notes."

### Work Breakdown - Sequence
**Weak:** Step 0 says "halt and create new initiative" but doesn't specify who decides or what the decision criteria are. Is any restructuring a halt, or only major restructuring?

**Fix:** Add decision rule to step 0: "Spike is go/no-go gate. If brain.py requires >4 hours of refactoring to support dynamic loading (e.g., rewriting prompt system), halt and create new initiative. Proceed to step 1 only if additive changes confirmed. Spike documents current context structure in spike-report.md."

**Weak:** Step 2 says "Add type to any notes used in testing" — this modifies production data during testing. What if those types are wrong?

**Fix:** Clarify scope: "Add type: frontmatter only to notes lacking it that will be used in testing. Document additions in audit-report.md. If uncertain about correct type, flag note in testing-log.md and exclude from override rate calculation."

**Weak:** Step 4 says "Test with one note per type confirming block content appears in LLM input" but doesn't specify how to verify this. Does brain.py log the full prompt? Is this manual inspection?

**Fix:** Add verification method: "Verification: add temporary debug logging to print full system message to stderr. Confirm block text appears between generic context and command prompt. Remove debug logging after verification."

**Weak:** Step 5 says "Test: (a) note with type: invalid produces invalid-type warning" but Constraints say "Warning on invalid type (not just missing)" without defining what "invalid" means. Is `type: foo` invalid? Or only malformed YAML?

**Fix:** Define invalid in Constraints: "Invalid type = any value other than code|business|content. Malformed YAML (e.g., missing colon) is a parse error, not an invalid type — brain.py should handle per existing error behavior."

### Delegation State
**Weak:** "Step 0: 0.5d, Step 1: 2d, Step 2: 4d..." — these estimates don't account for the halt scenario in step 0. If spike fails, is 0.5d wasted or does it count toward a new initiative?

**Fix:** Clarify step 0 accounting: "Step 0: 0.5d (counts toward this initiative even if halt triggered). Remaining estimates assume additive path. If restructuring required, new initiative gets separate budget."

**Weak:** Two identical rows in the table — likely a copy-paste error.

**Fix:** Remove duplicate row. Keep single row: "Solo | All steps | 2026-03-16 | Full ownership | Not started — Step 0: 0.5d, Step 1: 2d, Step 2: 4d, Step 3: 0.5d, Step 4: 4d, Step 5: 1d = 12d + 2d buffer"

### Definition of Done
**Weak:** "testing-log.md documents 50+ invocations with <30% aggregate override rate" — this contradicts Success Looks Like criterion 3 which says "ships regardless of outcome."

**Fix:** Remove rate requirement from DoD: "testing-log.md documents 50+ invocations with calculated override rate (initiative ships regardless of rate)."

**Weak:** Missing verification that warnings actually print to stderr (not stdout) and don't change exit code.

**Fix:** Add: "Warnings for missing/invalid type print to stderr and do not change exit code (remains 0). Verified by testing both cases and checking $? = 0."