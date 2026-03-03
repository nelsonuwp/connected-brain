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
- Injected block is inserted into system context immediately before the command-specific prompt, after any existing generic context
- brain.py currently uses static prompt templates loaded at startup. Dynamic loading requires adding frontmatter parsing and runtime block lookup. Assume additive unless 30-minute spike reveals restructuring needed — if restructuring required, halt and re-scope.

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
| ------ | ---- | ------- | ----- | ------ |
| Solo | All steps | 2026-03-16 | Full ownership | Not started |



---

# Critique — 2026-03-02 19:56 ET

## Score: 6/10
Rework suggested — execution would stall on vague success criteria and missing implementation details.

## Section Breakdown

### One-Line Purpose
**Strong:** Clear scope — type-aware injection for specific commands only.
**Weak:** "domain-specific context" and "appropriate criteria" are abstract. What makes code context different from business context?
**Fix:** Add one concrete example: "e.g., code notes get evaluated against architectural principles and maintainability; business notes against strategic alignment and resource constraints."

### Success Looks Like
**Weak:** Criterion 3 has contradictory logic. "Fewer than 30% require overrides" is the success threshold, but "if any single type exceeds 40%" triggers flagging. Which number gates shipping? Also, "50+ invocations spanning 20+ notes (minimum 5 per type)" — does this mean 5 notes per type (15 total) or 5 invocations per type (15 invocations minimum, contradicting "50+ invocations")?
**Fix:** Clarify: "Success = aggregate override rate <30% across all types. Ship regardless. Post-ship: if any single type shows >40% override rate in that same dataset, create follow-up initiative to subdivide that type." Specify: "Minimum 50 invocations total, distributed as: at least 15 notes (5 per type), each tested with both explore and critique (30 invocations minimum), plus 20+ additional invocations on repeat notes to test consistency."

**Weak:** Criterion 4 specifies warning messages but not where they print or whether they block execution. "Execution continues" is stated but not whether the command runs with generic context or no context.
**Fix:** Add: "Warnings print to stderr before command execution. Command proceeds using only generic context (no type-specific block injected). Exit code remains 0."

### Constraints
**Strong:** Token budget per block is testable. Three-type limit is clear.
**Weak:** "Assume additive unless 30-minute spike reveals restructuring needed — if restructuring required, halt and re-scope" — this makes the initiative conditional on a spike outcome, but the spike isn't in the work breakdown. When does the spike happen? Who decides "restructuring needed"?
**Fix:** Move spike to Work Breakdown step 0: "Conduct 30-minute spike on brain.py prompt loading. If current architecture allows additive dynamic loading, proceed. If restructuring required (e.g., prompt system rewrite), halt and create new initiative scoping the restructure. Document spike findings in spike-report.md before proceeding to step 1."

**Weak:** "Injected block is inserted into system context immediately before the command-specific prompt, after any existing generic context" — what is "generic context"? Is this documented somewhere? If brain.py changes its context structure, does this spec break?
**Fix:** Reference the actual context structure: "Injected block is inserted into the system message after [specific existing context file/section] and before [specific command prompt file/section]. Document current context structure in spike-report.md to establish baseline."

### Work Breakdown
**Weak:** Step 2 says "Minimum 2 notes per type × command pair (12 total invocations)" but Success Looks Like says "50+ invocations spanning 20+ notes (minimum 5 per type)." These numbers don't align.
**Fix:** Reconcile with Success criterion 3 fix above. Step 2 should say: "Test each type × command pair on at least 5 notes (30 invocations minimum). Add 20+ invocations on repeat notes. Target 50+ total invocations. Log each in testing-log.md: note path, type, command, override needed (yes/no), reason if yes."

**Weak:** Step 3 says "decide whether to proceed or re-scope" but Delegation State says "Full ownership" for solo execution. Who makes the re-scope decision if override rate fails?
**Fix:** Either: (a) add decision criteria: "If override rate >30%, solo decides: ship with flagging plan documented, or halt and re-scope. Document decision in analysis-report.md." Or (b) remove re-scope option: "If override rate >30%, ship anyway and document subdivision plan for follow-up initiative."

**Weak:** Step 4 says "Test with one note per type confirming block content appears in LLM input" — how do you confirm this? Does brain.py log the full system message? Is there a --debug flag?
**Fix:** Specify verification method: "Add --debug flag to brain.py that prints full system message to stderr, or manually inspect LLM API call logs. Confirm each type's block text appears verbatim in system message."

**Weak:** Step 5 tests warning behavior but doesn't test that warnings don't break execution. "Both cases proceed without injected block" — does this mean the command runs successfully and produces output?
**Fix:** Add to step 5: "Verify both warning cases: (a) command completes successfully (exit 0), (b) output is generated using generic context only, (c) warning appears in stderr but not in command output."

### Decisions Made
**Strong:** Rationale for type × command matrix is clear and defensible.
**Weak:** "Warning on missing type rather than default block — surfacing data quality issues is better than masking them" contradicts the behavior in Success criterion 4 and step 5, which say execution continues. If execution continues with generic context, you ARE using a default (generic context), not surfacing a blocking issue.
**Fix:** Clarify the decision: "Warning on missing type rather than silent fallback — user sees data quality issue but execution continues with generic context. This surfaces the gap without blocking workflow."

### Delegation State
**Weak:** "By When: 2026-03-16" is 14 days away. Work breakdown has 5 steps including drafting 6 blocks, auditing all notes, 50+ test invocations, implementation, and testing. No time estimates per step. Is 14 days realistic?
**Fix:** Add time estimates: "Step 1: 3 days. Step 2: 4 days. Step 3: 1 day. Step 4: 4 days. Step 5: 2 days. Total: 14 days. If spike in step 0 reveals restructuring needed, timeline invalid — re-scope before proceeding."

### Missing Sections
**Fix:** Add "Definition of Done" section:
- All 6 block files exist in 20-context/types/ and are under 200 tokens each
- brain.py parses frontmatter and injects blocks per spec
- testing-log.md documents 50+ invocations with <30% aggregate override rate
- Warnings print correctly for missing/invalid type
- spike-report.md documents current context structure and confirms additive approach