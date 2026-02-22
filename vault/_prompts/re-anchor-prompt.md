Generate a re-anchor file for this session. Be precise and specific — this document will be used to resume work in a future session with no other context.

Produce exactly this structure:

## State at End of Session
What is the current state of the work? What's working, what isn't?
Be specific enough that someone starting cold knows exactly where things stand.

## Decisions Made
List every decision made during this session with a one-line rationale.
Format: Decision → Rationale

## What Works
Confirmed working items. Don't re-litigate these next session.

## What Doesn't
Broken things, blockers, unknowns. Be specific about error messages or failure modes if relevant.

## Next Session Starts With
The exact first task for the next session. Specific enough to act on immediately.
Then 1-2 follow-on tasks in priority order.

## Open Questions
Things that need answers before or during the next session.
If none, write "None."

## Context Blocks Used
List the context block files referenced in this session so they can be re-injected next time.

Rules:
- Be specific. Vague re-anchors produce confused next sessions.
- Do not summarize the conversation — capture the state of the work.
- If a decision should be permanently logged, note it with [→ LOG TO 60-decisions/]
