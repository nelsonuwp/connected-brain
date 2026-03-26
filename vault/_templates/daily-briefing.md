---
type: daily
date: <% tp.date.now("YYYY-MM-DD") %>
week: <% tp.date.now("[W]ww") %>
---

# <% tp.date.now("dddd, MMMM D, YYYY") %>

## Priority Focus
1.
2.
3.

## Today's Schedule
<%*
/* Copy a row and replace meeting-short-name:
   | HH:MM–HH:MM | [[90-meeting-notes/YYYY/MM-MMM/YYYY-MM-DD-name\|name]] | attendees | [[prep]] |
*/
-%>

| Time | Meeting | Attendees | Prep |
|------|---------|-----------|------|
| | | | |
| | | | |
| | | | |
| | | | |

## Active Work

### Initiatives & Tasks: In Flight
```dataview
TABLE status, owner
FROM "30-initiatives/active" OR "31-tasks/active"
SORT file.mtime desc
```

### Initiatives & Tasks: Drafting
```dataview
TABLE status
FROM "30-initiatives/drafting" OR "31-tasks/drafting"
SORT file.mtime desc
```

### Ideas & Thinking to Explore
```dataview
LIST
FROM "01-inbox" OR "10-thinking"
WHERE file.folder = "01-inbox" OR file.folder = "10-thinking"
SORT file.mtime desc
LIMIT 10
```

## Load Check
- Active initiatives: `$= dv.pages('"30-initiatives/active"').length`
- Active tasks: `$= dv.pages('"31-tasks/active"').length`
- Drafting: `$= dv.pages('"30-initiatives/drafting"').length + dv.pages('"31-tasks/drafting"').length`
- Inbox items: `$= dv.pages('"01-inbox"').where(p => p.file.folder === "01-inbox").length`
- Open thinking notes: `$= dv.pages('"10-thinking"').where(p => p.file.folder === "10-thinking").length`
- Active delegations: `$= dv.pages('"70-delegation"').where(p => p.status === "active").length`
- Open loops: (check [[open-loops]])

## Captures Today


## Yesterday in Review
