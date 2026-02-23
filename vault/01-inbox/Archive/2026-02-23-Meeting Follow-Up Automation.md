---
type: idea
created: 2026-02-23
status: raw
---

# Meeting Follow-Up Automation

## The Idea
Automate the creation of follow-up tasks and summaries after meetings by connecting my calendar, meeting notes, and Jira.

## Why Now
I'm losing track of action items from back-to-back meetings. Things are falling through the cracks and I'm spending 20-30 minutes after every meeting manually creating Jira tickets and sending follow-up emails.

---

## LLM Output — refine-idea — 2026-02-23 21:09 UTC

## Unclear Scope & Mechanics

**What exactly triggers the automation?** Does it run after every calendar event ends, only meetings with certain keywords, only when you manually invoke it, or when notes are saved in a specific location? The difference between "all meetings" and "meetings where I took notes" is significant.

**What counts as an "action item"?** Are you relying on natural language processing to detect tasks in freeform notes, a specific syntax you'll use while note-taking (like `[ ]` or `TODO:`), or something else? If NLP, what's your tolerance for false positives/negatives?

**Where do meeting notes currently live?** You mention connecting notes but don't specify the system. Are these in Notion, Google Docs, Apple Notes, a voice recording that needs transcription, handwritten notes you'll scan? The integration complexity varies wildly.

**What information goes into the Jira tickets?** Just a task title, or do you need description, assignee, priority, labels, sprint assignment? If the latter, how does the system determine these fields — are you manually reviewing before creation, or is it fully automated?

**Who receives the "follow-up emails" and what do they contain?** Is this a summary to all attendees, task assignments to specific people, or something else? How does the system know who should get what?

## Missing Constraints

**What happens when the automation gets it wrong?** If it creates 5 Jira tickets from a brainstorming meeting where nothing was actually decided, or misses a critical action item, what's your recovery process?

**How many meetings per week are we talking about?** The ROI calculation for building this changes dramatically between 5 meetings/week and 25 meetings/week.

## My Answers

- **Trigger:** Manual invocation only for now — I run it after meetings where I took notes
- **Action items:** I'll use a specific syntax in notes (`ACTION:`) so there's no NLP guessing
- **Notes live in:** Obsidian, same vault as this system
- **Jira tickets:** Title + description only, I'll review before creation — not fully automated
- **Emails:** Not a priority, drop that scope. Focus is Jira only.
- **Volume:** ~10 meetings/week, maybe 4-5 that actually produce action items
- **Wrong automation:** Review step before any tickets are created — nothing fires without my approval