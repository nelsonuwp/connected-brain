# 20-context/schemas  ·  Reference → Schemas

Data structure definitions in human-readable markdown.

**Contains:**
- Database table structures (fields, types, constraints, what things actually mean)
- Parsed API response shapes (what a Jira issue looks like after you process it)
- Field name mappings and semantic definitions

**Rules:**
- This is the "what and why" — Python dataclass lives in projects/_reference/schemas/
- Inject when an LLM needs to understand a data shape to generate useful code
- If a real schema changes: update here first, then update the code
