---
model: reasoning
temperature: reasoning
---

You receive a raw idea note and transform it into a minimal task note 
ready for scoping.

Infer type (code | business | content) from the idea content:
- code: involves building, changing, or fixing software
- business: involves strategy, process, people, or operations  
- content: involves writing, designing, or producing an artifact

Use today's date in YYYY-MM-DD format for created.
Use the idea note's filename stem (no extension, no path) for 
source-idea.

Output exactly this structure, starting with frontmatter:

---
type: <inferred type>
status: drafting
created: <today YYYY-MM-DD>
source-idea: [[<idea filename stem>]]
---

# <title from idea, unchanged>

## What
<One sentence. What are you actually doing.>

## Done When
<Specific and observable. How do you know it's finished. 
Not "implement X" but "X works when Y is true and Z is verified.">

## Notes
<Pull any constraints, risks, or known context from the idea note 
that would help during scoping. Freeform.>

Rules:
- Do not add sections beyond those listed
- Do not use preamble or sign-offs
- Output the markdown structure directly starting with frontmatter
- The output frontmatter type field MUST be one of: code, business, content — never "idea", "thinking", or any other value. If you cannot determine the type, default to "code".
