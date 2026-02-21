# 20-context/apis  ·  Reference → APIs

API reference blocks. One file per external API or integration.

**Contains:**
- Authentication pattern
- Endpoints you actually use (not full docs)
- Pagination approach, rate limits, known gotchas

**Expected files:**
- jira-api.md, jsm-api.md, gitlab-api.md, slack-api.md, ms-graph-api.md

**Rules:**
- Inject into any LLM session where code will touch that API
- Update last-verified date after every session that uses this block
- Python implementations live in projects/_reference/clients/
