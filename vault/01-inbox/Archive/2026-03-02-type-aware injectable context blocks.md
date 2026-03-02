---
created: 2026-03-02
status: promoted
type: idea
---

# type-aware injectable context blocks

## The Idea
Add a type field (code | business | content) to note frontmatter across idea, thinking, task, and initiative. brain.py reads this field and auto-injects the matching context block from 20-context/types/ on every command. For v1, type affects system context only. Output structure and command availability are out of scope.

## What is it 
Today, type-specific criteria (security, maintainability, narrative flow) have to be manually added via --context flags or are missing entirely. A code task gets critiqued the same as a content piece. Add a type field (code | business | content) to note frontmatter so brain.py auto-injects the matching context block from 20-context/types/ on every command. For v1, type affects system context only.

## Why Now
Tasks are being added to the pipeline and they need type-aware explore and critique behavior. Without it, a task to refactor auth logic gets critiqued the same way as a content piece — generic output that misses the real criteria. Rather than duplicate type logic into every prompt file, one injectable block per type works across the whole pipeline. Tasks don't exist yet, so now is the right time to design this before the prompts are written.

## Proposed Design
- Type lives in frontmatter — explicit and portable. Folder inference breaks when a project mixes types. Content analysis is fragile. Frontmatter wins.
- Three types for v1: code, business, content — maps to the three kinds of work in the pipeline: technical implementation, strategic decisions, written output. Finer splits wait until there's evidence they're needed.
- Injection not substitution — simpler to implement, sufficient because type blocks are static and don't need per-command variation
- Type × command matrix is out of scope — type block is static per note. If tasks prove this wrong, revisit.
- Code thinking vs code task using same block: acceptable for v1. If tasks get too much exploratory framing in practice, split the blocks then.
- Audience and constraint layering is out of scope — separate idea, worth noting if type alone proves insufficient
- Type affects system context only. Output structure and command availability are separate ideas.
- Risk: type blocks get stale and auto-injection becomes auto-pollution. Mitigation: keep blocks under 200 tokens, review quarterly
- Blocker: brain.py doesn't currently support dynamic context loading. Estimate 2–4 hours to implement

---

# Explore — 2026-03-02 18:40 ET

## Explore — 2026-03-02

### Possibilities

**Type granularity**
- Three types may be too coarse. Code splits into architecture vs. implementation vs. debugging. Business splits into strategy vs. operations vs. financials. Content splits into writing vs. design vs. research.
- Alternatively, three types may be too fine. Maybe there are really only two modes: analytical (code, business) vs. generative (content, idea).
- Type could be hierarchical: `type: code/architecture` with fallback to `code` if no subtype block exists.

**Inheritance vs. injection**
- Instead of injecting a whole block, types could modify base prompts through variable substitution: `{{TYPE_FRAMING}}`, `{{TYPE_CRITERIA}}`.
- Types could stack: a note could be `type: [code, business]` for something like "technical architecture decision with budget implications."

**Where type lives**
- Frontmatter on the note (your current proposal).
- Inferred from folder location (everything in `projects/api-redesign/` is code).
- Inferred from content analysis (presence of code blocks, financial figures, etc.).
- Set once at project level, inherited by all notes in that project.

**What type affects**
- Just the system context (your current scope).
- Also the output structure (code gets implementation considerations, business gets stakeholder mapping).
- Also the default commands available (code notes get `--test-scenarios`, business notes get `--stakeholder-lens`).
- Also validation rules (code initiatives require dependency analysis, business requires success metrics).

### Adjacent ideas

**Context layering beyond type**
- Audience context: `audience: technical | executive | cross-functional`
- Constraint context: `constraints: [time-bound, resource-limited, regulatory]`
- These could combine with type: code + executive audience = different framing than code + technical audience.

**Dynamic context based on command, not just note**
- `explore` on a code note might need different context than `critique` on the same code note.
- Matrix of type × command rather than just type.

**Context blocks as composable primitives**
- Rather than three monolithic type blocks, a library of small context primitives that get assembled: `rigor-mode.md`, `implementation-focus.md`, `strategic-framing.md`.
- Type becomes a shorthand for a default bundle of primitives.

### Tensions to name

- Convenience of auto-injection vs. transparency of what's being injected (will you forget what's in the type blocks?).
- Standardization across note types vs. the reality that "code thinking" and "code task" might need different type context.
- Designing for current needs (tasks) vs. designing for flexibility you may not need.

---

# Critique — 2026-03-02 18:52 ET

## Score: 6/10
Rework suggested

## Section Breakdown

### The Idea
**Weak:** The mechanism is described but the actual problem is not. What goes wrong today without this? What manual step is painful or error-prone?
**Fix:** Add one sentence describing the current state pain: "Today I manually add --context flags to every task command, which means I forget to do it 40% of the time and get generic output" or "I'm copy-pasting the same context block into 12 different prompt files."

### Why Now
**Strong:** Clear trigger (tasks being added) and good timing logic (design before implementation).
**Weak:** "Need type-aware explore and critique behavior" is vague. What specifically breaks or degrades without type awareness?
**Fix:** Give one concrete example: "A task to refactor auth logic needs to be critiqued for security and maintainability, not narrative flow. Without type context, critique.md treats it like a content piece."

### Explore — Possibilities — Type granularity
**Weak:** Lists options but doesn't evaluate them. Which of these is actually a risk to your proposal?
**Fix:** Pick the one that matters most (likely "three types too coarse") and say whether you think it's a real blocker or acceptable for v1. If it's a blocker, what's the minimum viable alternative?

### Explore — Possibilities — Inheritance vs. injection
**Strong:** Variable substitution is a concrete alternative mechanism.
**Weak:** No evaluation of tradeoffs. Why would you choose injection over substitution or vice versa?
**Fix:** Add one line: "Injection is simpler to implement but less flexible. Substitution allows mixing but requires more template design upfront. For v1, injection is enough because..."

### Explore — Possibilities — Where type lives
**Weak:** Four options with no position. This is the core design question and you haven't taken a stance.
**Fix:** State which option you're proposing and why. If you're unsure, say "Frontmatter is the default but folder inference is worth prototyping because..." Don't leave this open-ended.

### Explore — Possibilities — What type affects
**Weak:** Scope creep listed without boundaries. This could balloon into a type system overhaul.
**Fix:** Draw a line. Say "For this idea, type affects system context only. Output structure and command availability are separate ideas to consider later if context injection proves useful."

### Explore — Adjacent ideas — Context layering beyond type
**Weak:** Introduces new dimensions (audience, constraints) without connecting them to the current proposal. Are these alternatives or extensions?
**Fix:** Either cut this (it's a separate idea) or explicitly say "This is out of scope for now but worth noting for future iteration."

### Explore — Adjacent ideas — Dynamic context based on command
**Weak:** This directly contradicts your proposal (type-based injection) but you don't acknowledge the conflict.
**Fix:** Say whether this replaces your idea or extends it. "If command matters more than type, then type-based injection is wrong. If type is primary and command is secondary, then..." Take a position.

### Explore — Tensions to name
**Strong:** "Transparency of what's being injected" is a real risk.
**Weak:** The other two tensions are underspecified. What does "code thinking vs. code task needing different context" actually mean in practice?
**Fix:** Make the second tension concrete: "A code thinking note explores tradeoffs broadly; a code task needs implementation constraints. If both use the same type block, does the task get too much exploratory framing?" Then say whether this is a real problem or theoretical.

### Missing: What You're Actually Proposing
**Weak:** The explore section lists options but never returns to "here's what I'm building."
**Fix:** Add a section after Explore called "Proposed Design" that says: type lives in frontmatter, affects system context only, three types for v1, injection not substitution, and here's why. Without this, the note is all questions and no direction.

### Missing: Risks or Blockers
**Weak:** No mention of implementation complexity, migration cost, or failure modes.
**Fix:** Add: "Risk: If type blocks get stale or inconsistent, auto-injection becomes auto-pollution. Mitigation: Keep type blocks under 200 tokens and review quarterly." Or: "Blocker: brain.py doesn't currently support dynamic context loading. Estimate 4 hours to add this."

---

# Critique — 2026-03-02 18:53 ET

## Score: 6/10
Rework suggested

## Section Breakdown

### The Idea
**Weak:** The mechanism is described but the actual problem is not. What goes wrong today without this? What manual step is painful or error-prone?
**Fix:** Add one sentence describing the current state pain: "Today I manually add --context flags to every task command, which means I forget to do it 40% of the time and get generic output" or "I'm copy-pasting the same context block into 12 different prompt files."

### Why Now
**Strong:** Clear trigger (tasks being added) and good timing logic (design before implementation).
**Weak:** "Need type-aware explore and critique behavior" is vague. What specifically breaks or degrades without type awareness?
**Fix:** Give one concrete example: "A task to refactor auth logic needs to be critiqued for security and maintainability, not narrative flow. Without type context, critique.md treats it like a content piece."

### Proposed Design
**Strong:** Clear boundaries (injection not substitution, system context only, v1 scope explicit). Risk mitigation is concrete (200 token limit, quarterly review). Blocker is identified with time estimate.
**Weak:** "Three types for v1" is stated but not justified. Why these three? What makes them the right level of granularity?
**Fix:** Add one line: "Code, business, content map to the three kinds of work in the current pipeline: technical implementation, strategic decisions, and written output. Finer splits (architecture vs. debugging) can wait until there's evidence they're needed."

### Explore — Possibilities — Type granularity
**Weak:** Lists options but doesn't evaluate them. Which of these is actually a risk to your proposal?
**Fix:** Pick the one that matters most (likely "three types too coarse") and say whether you think it's a real blocker or acceptable for v1. If it's a blocker, what's the minimum viable alternative?

### Explore — Possibilities — Inheritance vs. injection
**Strong:** Variable substitution is a concrete alternative mechanism.
**Weak:** No evaluation of tradeoffs. Why would you choose injection over substitution or vice versa?
**Fix:** Add one line: "Injection is simpler to implement but less flexible. Substitution allows mixing but requires more template design upfront. For v1, injection is enough because type blocks are static and don't need per-command variation."

### Explore — Possibilities — Where type lives
**Weak:** Four options with no position. This is the core design question and you haven't taken a stance.
**Fix:** State which option you're proposing and why. "Frontmatter is explicit and portable. Folder inference breaks when a project mixes types. Content analysis is fragile. Frontmatter wins for v1."

### Explore — Possibilities — What type affects
**Weak:** Scope creep listed without boundaries. This could balloon into a type system overhaul.
**Fix:** This is already handled in Proposed Design. Cut this subsection entirely or reduce to: "Output structure and command availability are out of scope for v1. Type affects system context only."

### Explore — Adjacent ideas — Context layering beyond type
**Weak:** Introduces new dimensions (audience, constraints) without connecting them to the current proposal. Are these alternatives or extensions?
**Fix:** Either cut this (it's a separate idea) or explicitly say "This is out of scope for now but worth noting if type alone proves insufficient."

### Explore — Adjacent ideas — Dynamic context based on command
**Weak:** This directly contradicts your proposal (type-based injection) but you don't acknowledge the conflict.
**Fix:** Say whether this replaces your idea or extends it. "If command matters more than type, then static type blocks are wrong. Current assumption: type is primary, command is secondary. If tasks prove this wrong, revisit."

### Explore — Tensions to name
**Strong:** "Transparency of what's being injected" is a real risk.
**Weak:** The other two tensions are underspecified. What does "code thinking vs. code task needing different context" actually mean in practice?
**Fix:** Make the second tension concrete: "A code thinking note explores tradeoffs broadly; a code task needs implementation constraints. If both use the same type block, does the task get too much exploratory framing?" Then say whether this is a real problem or theoretical.

---

# Critique — 2026-03-02 18:55 ET

## Score: 7/10
Rework suggested — one design question unresolved, otherwise ready to promote

## Section Breakdown

### The Idea
**Strong:** Mechanism is clear (type field → auto-inject context block). Scope is explicit (system context only, v1).
**Weak:** Missing the current-state pain. Why is manual context injection failing?
**Fix:** Add one sentence before "Add a type field": "Today, type-specific criteria have to be manually added via --context flags or are missing entirely. A code task gets critiqued the same as a content piece."

### Why Now
**Strong:** Clear trigger (tasks being added), good timing logic (design before implementation).
**Weak:** "Need type-aware explore and critique behavior" is abstract. What actually breaks?
**Fix:** Replace "need type-aware explore and critique behavior" with: "Without it, a task to refactor auth logic gets critiqued the same way as a content piece — generic output that misses the real criteria (security, maintainability)."

### Proposed Design
**Strong:** Boundaries are explicit (injection not substitution, system context only, v1 scope clear). Risk mitigation is concrete (200 token limit, quarterly review). Blocker identified with time estimate. The "code thinking vs code task using same block" acknowledgment is good.
**Weak:** "Three types for v1" is stated but not justified. Why code/business/content specifically?
**Fix:** After "Three types for v1," add: "These map to the three kinds of work in the pipeline: technical implementation, strategic decisions, written output. Finer splits (architecture vs. debugging) wait until there's evidence they're needed."

### Explore — Possibilities — Where type lives
**Weak:** Four options listed but your Proposed Design already chose frontmatter. This section now contradicts your decision.
**Fix:** Cut this subsection entirely. You've already decided. Or reduce to one line: "Frontmatter is explicit and portable. Folder inference breaks when a project mixes types. Content analysis is fragile."

### Explore — Possibilities — What type affects
**Weak:** This is already covered in Proposed Design ("type affects system context only"). Listing scope creep here creates confusion.
**Fix:** Cut this subsection. It's redundant with Proposed Design.

### Explore — Adjacent ideas — Context layering beyond type
**Weak:** Introduces audience and constraints without saying whether they're alternatives, extensions, or out of scope.
**Fix:** Add one line at the end: "Out of scope for v1 but worth noting if type alone proves insufficient."

### Explore — Adjacent ideas — Dynamic context based on command
**Weak:** This directly challenges your proposal (static type blocks) but you don't take a position. If command matters more than type, your whole design is wrong.
**Fix:** Add: "This would replace static type blocks with a type × command matrix. Current assumption: type block is static per note, command doesn't vary it. If tasks prove this wrong, revisit."

### Explore — Tensions to name — "code thinking vs code task"
**Weak:** "Code thinking and code task might need different type context" is vague. What does this mean in practice?
**Fix:** Make it concrete: "A code thinking note explores tradeoffs broadly; a code task needs implementation constraints. If both use the same type block, does the task get too much exploratory framing? Acceptable for v1. If tasks get polluted in practice, split the blocks then."