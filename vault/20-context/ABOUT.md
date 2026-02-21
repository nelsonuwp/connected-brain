# 20-context  ·  Reference

Reusable LLM context blocks. The most important folder in the vault.

**Purpose:**
Explain something once. Inject it everywhere. Every file here is designed
to be attached to an LLM prompt so you never re-explain the same API,
schema, or business concept again.

**Subfolders:**
- apis/      → API reference blocks (auth, endpoints, gotchas, examples)
- schemas/   → Data structure definitions (fields, types, relationships, meanings)
- patterns/  → Reusable approaches (code patterns, process patterns, prompt patterns)
- business/  → Business model context (OSOM, strategy, org structure, glossary)

**Rules:**
- If you explained the same thing to an LLM twice → it belongs here before the third time
- Each file follows _templates/context-block.md structure
- Keep every file reference-grade: verified, compressed, no fluff
- Tag with last-verified date — stale context produces bad LLM outputs
- Max 3 context blocks per LLM prompt — if you need more, the task is too large
