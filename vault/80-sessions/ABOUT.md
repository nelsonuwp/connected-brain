# 80-sessions  ·  Sessions

LLM session re-anchors. Solves session amnesia.

**Structure:**
  80-sessions/project-name/session-001.md

**Contains:**
- State at end of session (what's working, what isn't)
- Decisions made during the session
- Context blocks used
- What the next session should start with
- Open questions

**Rules:**
- Create at end of any LLM session that took >30 minutes
- Have the LLM generate it using _prompts/re-anchor.md — you review, don't write
- Start every follow-on session by injecting the previous re-anchor
- Significant decisions get promoted to 60-decisions for permanent record
