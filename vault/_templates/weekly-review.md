---
type: weekly
week: <% tp.date.now("[W]ww") %>
date-range: <% tp.date.now("MMM D") %> – <% tp.date.now("MMM D", 6) %>
---

# Week <% tp.date.now("ww") %> Review

## What Moved This Week
<!-- Initiatives that progressed, closed, or got stuck -->


## Delegation Health
```dataview
TABLE owner, status, risk
FROM "70-delegation"
WHERE status != "done"
SORT risk DESC
```

## Stale Context Blocks
```dataview
TABLE last-verified
FROM "20-context"
WHERE date(last-verified) < date(today) - dur(45 days)
SORT last-verified ASC
```

## Service State Updates
<!-- Quick pass — update current state in each 50-services note -->
- [ ] Services reviewed

## Decisions to Log
<!-- Anything decided this week not yet in 60-decisions -->


## Thinking Notes to Promote or Kill
<!-- Anything in 10-thinking older than 2 weeks -->
```dataview
TABLE file.mtime
FROM "10-thinking"
WHERE file.mtime < date(today) - dur(14 days)
SORT file.mtime ASC
```

## Next Week's Focus
<!-- Three outcomes, not tasks -->
1. 
2. 
3. 
