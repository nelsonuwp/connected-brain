---
type: idea
created: 2026-03-02
status: raw
---

# type-aware injectable context blocks

## The Idea
Add a type field (code | business | content) to note frontmatter across idea, thinking, task, and initiative. brain.py reads this field and auto-injects the matching context block from 20-context/types/ on every command, without requiring a manual --context flag.

## Why Now
Tasks are being added to the pipeline and they need type-aware explore and critique behavior. Rather than duplicate this logic into every prompt file, a single injectable block per type works across the whole pipeline. This is the right time to design it because the task prompts don't exist yet.

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