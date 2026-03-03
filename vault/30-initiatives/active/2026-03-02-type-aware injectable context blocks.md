---
status: active
type: initiative
---

# type-aware injectable context blocks

## One-Line Purpose
Auto-inject domain-specific context into brain.py commands based on note type, so code/business/content notes get evaluated against appropriate criteria without requiring manual --context flags for standard cases.

## Context
Currently all notes receive identical generic context regardless of domain — a code architecture note gets the same critique framing as a blog post. With tasks entering the pipeline, this is the right moment to add type awareness before prompts proliferate. The design uses a type × command matrix (6 blocks total) where type sets the domain and command sets the lens.

## Success Looks Like
0. Step 0 spike confirms brain.py context loading supports additive dynamic loading (documented in spike-report.md). If restructuring required, initiative halts here.
1. Notes with `type: code|business|content` in frontmatter automatically receive the matching context block when running explore or critique commands.
2. Each of the 6 blocks (3 types × 2 commands) stays under 200 tokens.
3. Aggregate override rate measured across minimum 50 invocations (5 notes × 3 types × 2 commands = 30 base + 20 repeat). Override = any invocation where user manually adds --context flags because the injected block was insufficient. Measured per invocation. Initiative ships regardless of rate. Post-ship: if aggregate >30% OR any single type ≥40%, document findings in analysis-report.md and create follow-up initiative for type subdivision.
4. Missing or invalid type (any value other than code|business|content) prints to stderr: `[WARN] Note has no type specified — proceeding without type-specific context` or `[WARN] Note has invalid type '{value}' — proceeding without type-specific context`. Command executes using only generic context (no type block injected). Exit code 0. Warnings appear in stderr only, not in command output.

## Constraints
- Three types only for v1: code, business, content
- No audience or constraint layering in v1
- Injection adds to system context; does not substitute existing context
- Blocks are static per type × command pair
- 200 token budget per block
- Block file path convention: `20-context/types/{type}-{command}.md` — direct lookup, no registry for v1
- Injection order: [generic context] → [type block] → [command prompt]
- Invalid type = any value other than code|business|content. Malformed YAML is a parse error handled by existing brain.py error behavior, not a type warning.
- brain.py currently uses static prompt templates loaded at startup. Dynamic loading requires adding frontmatter parsing and runtime block lookup. Assumed additive — confirmed or denied by step 0 spike.
- Step 0 spike is a go/no-go gate. If brain.py requires >4 hours of refactoring (e.g., rewriting the prompt system), halt this initiative and create a new one scoping the restructure.

## Non-Goals
- No type taxonomy beyond the initial 3 for v1
- No custom user-defined types
- No context injection for commands other than explore and critique
- No audience or constraint layering

## Open Questions
- Is "business" coherent or a catch-all? Testing will answer this. If ≥40% override rate post-ship, flag for subdivision in follow-up initiative.

## Work Breakdown

### Files / Deliverables
- `20-context/types/code-explore.md`
- `20-context/types/code-critique.md`
- `20-context/types/business-explore.md`
- `20-context/types/business-critique.md`
- `20-context/types/content-explore.md`
- `20-context/types/content-critique.md`
- `spike-report.md` — current brain.py context structure + additive confirmation
- `audit-report.md` — count of notes by type, list of notes needing type added
- `testing-log.md` — 50+ invocations: note path, type, command, override (yes/no), reason
- `analysis-report.md` — override rate breakdown, subdivision plan if needed
- `cursor-prompt.md` — implementation prompt for Cursor Composer covering steps 4 and 5
- Modified `brain.py` with dynamic context loading based on frontmatter type field

### Sequence
0. **Spike (0.5d):** Confirm brain.py prompt loading is additive. Document current context structure in spike-report.md. Decision rule: if additive, proceed to step 1. If >4 hours of refactoring required, halt and create new initiative. Step 0 time counts toward this initiative either way.
1. **Draft blocks (2d):** Write all 6 type × command blocks using partial drafts as starting points. Count tokens on each — must stay under 200.
2. **Audit + test (4d):** Audit existing notes for type: frontmatter. Produce audit-report.md. Add type to notes used in testing — if uncertain about correct type, flag in testing-log.md and exclude from override rate calculation. Run minimum 5 notes per type × 2 commands (30 base invocations) plus 20+ repeat invocations. Log each in testing-log.md.
3. **Analyze (0.5d):** Calculate aggregate override rate from testing-log.md. If <30% aggregate and no type ≥40%, proceed. If aggregate ≥30% or any type ≥40%, document subdivision plan in analysis-report.md. Initiative proceeds to step 4 regardless.
4. **Implement (4d):** Draft cursor-prompt.md covering: (a) parse frontmatter for type field, (b) construct path `20-context/types/{type}-{command}.md`, (c) read file if exists, (d) inject into system context in order: [generic context] → [type block] → [command prompt]. Feed cursor-prompt.md + this initiative note to Cursor Composer. Verification: add temporary debug logging to print full system message to stderr. Confirm block text appears between generic context and command prompt. Remove debug logging after verification.
5. **Warning behavior + final test (1d):** Implement and verify warnings. For both missing and invalid type: (a) warning prints to stderr with correct text, (b) exit code 0 (`$? = 0`), (c) command output generated, (d) output uses generic context only (no type-specific criteria referenced).

## Decisions Made
- Type × command matrix (6 blocks) over type-only (3 blocks) — explore needs expansive thinking while critique needs checklists; these are fundamentally different lenses
- Injection over substitution — simpler implementation, blocks remain static
- Warning on missing/invalid type rather than silent fallback — user notified via stderr, execution continues with generic context; surfaces data quality gap without blocking workflow
- No default type block — untyped notes get generic output, not masked type output
- Quarterly review cadence for block staleness — first review 2026-06-01, solo owner

## Delegation State
| Person | Owns | By When | Level | Status |
| ------ | ---- | ------- | ----- | ------ |
| Solo | All steps | 2026-03-16 | Full ownership | Not started — Step 0: 0.5d, Step 1: 2d, Step 2: 4d, Step 3: 0.5d, Step 4: 4d, Step 5: 1d = 12d + 2d buffer |

## Definition of Done
- spike-report.md confirms additive approach
- All 6 block files exist in `20-context/types/` and are under 200 tokens each
- cursor-prompt.md drafted and used as Composer input
- brain.py parses frontmatter and injects matching block per type × command in correct order
- testing-log.md documents 50+ invocations with calculated override rate (ships regardless of rate)
- Warnings for missing/invalid type print to stderr, do not appear in command output, and do not change exit code (verified: `$? = 0`)
- analysis-report.md exists with override rate breakdown (and subdivision plan if any type ≥40%)