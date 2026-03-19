---
type: idea
created: 2026-03-19
status: raw
---

# Updates to Daily Cockpit - Meetings

# Meeting Note Automation

## What

Extend the existing email automation pipeline to also pull calendar events from Microsoft Graph API and pre-populate meeting note templates in Obsidian. Each meeting gets its own note, pre-filled with time, attendees, agenda (if available), and links to relevant context.

**Target folder structure:** `90-meeting-notes/YYYY/MM-MMM/DD/{meeting-short-name.md}`

Example: `90-meeting-notes/2026/03-Mar/19/aws-migration-sync.md`

The `DD/` subfolder groups all meetings for a given day, making it easy to see "what happened on March 19th" at a glance.

**Meeting note template should include:**

- Frontmatter: type, date, time, duration, attendees (as wikilinks to `40-people/` when matched), organizer, source (calendar event ID)
- Meeting title as H1
- Attendees list
- Agenda (pulled from event body if present)
- Empty sections for: Notes, Decisions, Action Items
- Action items section should use `#action` tags on checkboxes so they surface in the `open-tasks.md` sidebar

**Pipeline integration:**

- The existing email-agent pipeline uses Microsoft Graph OAuth with `Mail.Read` scope. Calendar events need `Calendars.Read` — this is an additional scope on the same auth flow, not a new app registration
- Graph API endpoint: `GET /users/{id}/calendarView?startDateTime=...&endDateTime=...`
- The `run_pipeline.py` orchestrator already supports staged execution (`--from`) — meeting capture could be a new stage or a parallel pipeline
- Meeting notes should be created BEFORE the day starts (or early morning) so they're ready when you sit down. This pairs with the daily brief creation sequence: create daily note → run email pipeline → run meeting pipeline → everything is populated

**Connection to daily brief:**

- The daily brief's "Today's Schedule" section should be auto-populated from the same calendar data, with wikilinks to each meeting note
- Example rendering in the daily brief:

```
  ## Today's Schedule
  - 09:00–09:30 [[aws-migration-sync]] — Lacie, Erik, Andrei, Kristina
  - 10:00–11:00 [[triple-jump-azure-review]] — Frederic, Darren, Andy
  - 14:00–14:30 [[1-on-1-matthew-carter]] — Matthew Carter
```

- This replaces the current manual "Populate from Outlook each morning" workflow

**Short name generation:**

- Strip common prefixes like "Meeting:", "RE:", "FW:", "[EXTERNAL]"
- Lowercase, kebab-case, truncate to ~50 chars
- Handle duplicates by appending `-2`, `-3` etc. within the same day folder
- Calendar events with no title → `untitled-0900` (using start time)

**Filtering:**

- Include: accepted meetings, tentative meetings (flag as tentative in template)
- Exclude: declined meetings, cancelled meetings, all-day events (unless explicitly flagged as important)
- Recurring meetings: create a fresh note each occurrence, not a single note

**People matching:**

- Attendee email addresses can be matched against `40-people/` notes if those notes have an email property in frontmatter
- Matched attendees render as `[[firstname-lastname]]` wikilinks
- Unmatched attendees render as plain text with email

## Why Now

The daily brief redesign (completed 2026-03-19) established the daily note as a cockpit. "Today's Schedule" is currently manual — it's the most obvious gap in the morning workflow. The email pipeline already authenticates against Microsoft Graph and follows the capture → process → render pattern. Calendar events are a second data source through the same vehicle (as confirmed during design discussion). Meeting notes are also a designated task source — the `open-tasks.md` sidebar is already configured to pull `#action` tagged checkboxes from `90-meeting-notes/`. Without meeting note automation, that sidebar section will stay empty.