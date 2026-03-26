---
type: daily
date: <% tp.date.now("YYYY-MM-DD") %>
week: <% tp.date.now("[W]ww") %>
---

# <% tp.date.now("dddd, MMMM D, YYYY") %>

## Priority Focus
<!-- Max 3 OUTCOMES for today. Not tasks — what moves forward? -->
1.
2.
3.

## Today's Schedule
<!-- Manual: paste from Outlook each morning. Each line = one meeting. -->
<!-- Wikilink creates the meeting note in 90-meeting-notes when clicked. -->
<!-- Format: - HH:MM–HH:MM [[meeting-short-name]] — attendees -->
<!-- Example: - 09:00–09:30 [[aws-migration-sync]] — Lacie, Erik, Andrei -->

| Time | Meeting | Attendees | Prep |
|------|---------|-----------|------|
| | [[]] | | |
| | [[]] | | |
| | [[]] | | |
| | [[]] | | |

<!-- Prep column: link to an initiative, person note, or context block you should review before the meeting -->

## Active Work

### Initiatives & Tasks: In Flight
<!-- What you're actively driving — these are in execution -->
```dataview
TABLE status, owner
FROM "30-initiatives/active" OR "31-tasks/active"
SORT file.mtime desc
```

### Initiatives & Tasks: Drafting
<!-- Being developed — explore/critique loop, not yet in execution -->
```dataview
TABLE status
FROM "30-initiatives/drafting" OR "31-tasks/drafting"
SORT file.mtime desc
```

### Ideas & Thinking to Explore
<!-- Inbox items and thinking notes that need your attention -->
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
<!-- Quick notes, things captured during the day. Route later. -->
<!-- Tag with #action for tasks, #tracking for things to follow up on -->


## Open Actions & Tracking
<!-- Pulled from all daily and meeting notes — powered by open-tasks.md -->
<!-- Link: [[open-tasks]] -->

---
<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- DAILY DIGEST — injected below by the daily-digest pipeline    -->
<!-- Do not edit below this line manually                          -->
<!-- ═══════════════════════════════════════════════════════════════ -->