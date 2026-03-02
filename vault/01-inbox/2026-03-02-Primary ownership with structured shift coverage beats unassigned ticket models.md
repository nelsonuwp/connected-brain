---
type: idea
created: 2026-03-02
status: raw
---

# Primary ownership with structured shift coverage beats unassigned ticket models

## The Idea
A support model where every ticket and customer always has a named primary owner, combined with structured shift-based coverage (instead of unassigning tickets), preserves accountability while still enabling 24/7 operations.

## Why Now
You’re actively debating operating models. Choosing an unassigned system will erode ownership and customer experience in ways that are hard to reverse. This is a foundational design decision that will shape how support scales.

## Context

The conversation with Jason is really about whether the team is designed around engineer convenience or customer outcomes. The unassign model is engineer convenience dressed up as operational flexibility.  
  
Let's work with the actual numbers first because the graveyard shift is the crux of the problem.  
  
**The real math:**  
- ~700 customers across 15 people = ~47 customers per person if you did pure assignment  
- But you have 3 shifts, so at any given time you have maybe 5-6 people on a "normal" shift and 2 on graveyard  
- Graveyard with 2 people is a coverage model, not an ownership model — those 2 cannot own 700 customers  
  
So the architecture needs two distinct concepts that JSM can support:  
  
---  
  
**Primary Owner vs. Shift Coverage**  
  
Every ticket and every customer has a **Primary Owner** — the named engineer who owns that relationship and that ticket to resolution. This never changes unless there's a formal handoff.  
  
Separate from that, **Shift Coverage** exists for when the primary owner is off. This is not unassigning — it's a structured escalation path baked into JSM.  
  
In JSM this looks like:  

Ticket fields:  
Assignee = Primary Owner (never blanked)  
On-Call Coverage = Shift Lead (auto-populated by schedule)  
Status = Waiting on Customer / In Progress / Escalated

  
When a primary owner goes off shift, the ticket stays assigned to them. The incoming shift lead gets a **shift handoff queue** — a saved filter in JSM showing every open ticket whose primary owner is currently off shift, sorted by priority and last activity. The 2 graveyard people work from that queue. They are not the owner — they are the overnight caretaker. Any action they take gets logged. When the primary owner comes back on, they pick up with full context.  
  
---  
  
**The Graveyard Shift Specifically**  
  
Two people cannot own anything at scale. Their job is explicitly different:  
  
- **Monitor** — watch for new P1/P2 tickets from any customer  
- **Stabilize** — take immediate action to stop bleeding, not to resolve  
- **Document** — log everything they touch so the primary owner has full context at handover  
- **Escalate** — wake up the on-call primary owner if it's genuinely critical  
  
In JSM you solve this with:  
  
**A graveyard handoff ritual.** End of each graveyard shift, the two people update every ticket they touched with a structured note — what happened, what they did, what's pending. JSM automation can enforce this by requiring a comment before status changes during graveyard hours.  
  
**An automatic morning flag.** JSM automation rule: any ticket touched by a graveyard shift engineer gets a label or flag that puts it at the top of the primary owner's queue when they log in. The primary owner's first 15 minutes of shift is reviewing what happened overnight on their tickets.

---