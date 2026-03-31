---
type: person
role:
delegation-level: L1
created: <% tp.date.now("YYYY-MM-DD") %>
---

# <% tp.file.title %>

**Role:**
**Current delegation level:** L
**Building toward:** L by

---

## Active Delegations
| What | Brief | Level | Status | Risk |
|------|-------|-------|--------|------|
| | | L | | |

## Capability Map
| Area | Current | Target | Development Path |
|------|---------|--------|-----------------|
| Structured thinking | | | |
| Communication & influence | | | |
| Escalation hygiene | | | |
| Ownership & initiative | | | |
| Technical/domain depth | | | |

## Open Tracking Items
```dataview
TASK FROM "<% tp.file.folder(true) %>/1-1s"
WHERE !completed AND contains(tags, "#tracking")
SORT file.mtime DESC
```

## 1:1 History
```dataview
TABLE file.mtime AS "Date"
FROM "<% tp.file.folder(true) %>/1-1s"
SORT file.mtime DESC
LIMIT 10
```
