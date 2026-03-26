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
<!-- These tags feed [[open-tasks]] in the sidebar automatically. -->


## Yesterday in Review
<!-- Do not edit below this line manually                               -->
<!-- ═══════════════════════════════════════════════════════════════════ -->

<!--
Pipeline injects a flat list. Each item rendered as:

#### [Short Title Summary](primary-url) `source`
One paragraph summary — enough context to understand, no more.
- [ ] Something I need to do #action
- [x] Something already done — [proof](url-to-completion-message) #action
- [ ] Something someone else needs to do that I need to track #tracking
Sources: [Re: Thread subject](url1) · [Teams: Channel name](url2)
`3 emails · 1 teams · 2026-03-25 14:22–17:05`

FORMATTING RULES:
  - Title is the link: [Title](url) not Title — [link](url)
  - Source tag after title: `email`, `teams`, `email` `teams` for multi-source
  - Completed actions use [x] with a link to the message proving completion
  - "Sources:" line only appears when item spans multiple emails/threads/channels
    (skip it for single-source items — the title link is sufficient)
  - Stats line at bottom of each item: count per source type · date range
  - Teams messages have linkable URLs — include them like email links

CATEGORIZATION — implicit, not structural:
  - Has #action → I need to act (feeds [[open-tasks]] sidebar)
  - Has #tracking → Someone else needs to act, I'm following
  - Neither → Informational, just awareness
-->