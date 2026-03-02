Customer context has to be accessible at first touch. If a generalist picks up a ticket from a hybrid customer and has to go hunting for what products they have, what their environment looks like, and who their account manager is — that's where hybrid customer experience falls apart. This is actually an Operational Intelligence problem as much as an org problem. Jorge's team building a unified customer view is directly load-bearing for this.

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

```
Ticket fields:
  Assignee = Primary Owner (never blanked)
  On-Call Coverage = Shift Lead (auto-populated by schedule)
  Status = Waiting on Customer / In Progress / Escalated
```

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

**Customer Assignment Model**

Rather than 47 customers per person (unmanageable context), structure it as **pods**:

```
Pod A (5 engineers across shifts) — ~140 customers
Pod B (5 engineers across shifts) — ~140 customers  
Pod C (5 engineers across shifts) — ~140 customers
Graveyard (2 engineers) — covers all pods overnight
```

Each pod has at least one engineer on each of the two main shifts. Graveyard covers all pods but works from a triage-first queue, not pod ownership.

Within each pod, individual engineers own specific accounts. When their account has a ticket, it routes to them. When they're off shift, it routes to their pod colleague on the current shift — not to the general pool, not unassigned. Pod colleague is named, not random.

---

**JSM Configuration to Make This Work**

- **Customer Organization field** — every customer mapped to a pod in JSM
- **Assignee automation** — new ticket from a customer auto-assigns to that customer's primary engineer if they're on shift; routes to pod coverage if they're off
- **On-call schedule integration** — JSM has native on-call scheduling (Opsgenie is now part of the Atlassian stack); plug shift schedules in and let the routing rules do the work
- **SLA clocks** — SLA timer runs regardless of who is assigned; it doesn't pause because someone went off shift. This is the forcing function that makes shift handoff a real operational discipline rather than optional
- **"Waiting on Customer" status** — ticket stays assigned, SLA pauses, but a JSM automation fires a follow-up reminder to the assignee after X hours of no customer response. The engineer doesn't have to remember — the system reminds them

---

The bottom line for the conversation with Jason: the graveyard coverage problem is real and valid, but the answer is **pod coverage + named shift handoff**, not unassignment. The system does the routing. Engineers don't have to manually grab tickets. Ownership is preserved. The 2 graveyard people have a clear, bounded job. And when a customer calls for an update at 2am, the graveyard engineer can pull up the ticket, see the full history, and give an intelligent answer — because the ticket was never orphaned.

---

Within the service network as defined, the answer is neither Jason nor George — it's **Lacie.**

Here's why. You already have a service that owns the customer relationship end to end — it's called **Hybrid Service Delivery Management**. That's not just a PMO for PS engagements. That's the function whose entire purpose is to be the single point of contact, own the customer relationship, and coordinate across the service network on the customer's behalf.

The internal economy question you're asking — who pays whom — is really a **transfer pricing model** between services. It would work like this:

```
HSDM owns the customer
    ↓
HSDM "buys" capacity from:
  → Service Desk (Jason)  — for day 2 operations and ticket management
  → Data Center Ops (George) — for physical infrastructure and facilities
  → Network (Ben) — for connectivity
  → Compute Platforms (Martin) — for provisioning
  → Managed Cloud (Andrei) — for cloud managed layer
    ↓
Each service has an internal rate card
HSDM aggregates and is accountable for the margin
```

This actually solves several problems you've already identified:

**The PS headcount problem** — if HSDM owns the customer and buys capacity from home teams, PS is just a higher-intensity version of the same model. The same internal economy applies. Lacie isn't borrowing resources ad hoc, she's purchasing committed capacity.

**The hybrid customer problem** — a customer with dedicated hosting and Azure resell has one relationship owner (HSDM) who buys the right mix of services on their behalf. The customer doesn't care what the internal economy looks like. They have one throat.

**The cost allocation problem** — instead of 17 Service Desk people accidentally sitting on Managed Cloud's books, each service has clean internal billing. Jason's cost sits on Jason's service. HSDM's P&L reflects what they paid for and what margin they generated on top.

**The graveyard/ticket ownership question** — Jason's team owns ticket execution but HSDM owns the customer. Jason reports ticket health to HSDM. Lacie knows if a customer's tickets are trending badly before it becomes an escalation.

The one thing this requires that doesn't exist yet is **Lacie's team having enough customer visibility to actually own that relationship** — which is exactly what Jorge's Operational Intelligence function is supposed to provide. A unified customer view, ticket health by customer, service consumption, margin per customer. That's not a nice-to-have in this model — it's load-bearing.

So the org structure question resolves to: does Lacie's mandate extend from PS project delivery to ongoing customer relationship ownership across all services? Because if it does, you have your answer. And it fits cleanly within the service network as defined.

# Updates to Report
- last touch
- account rep

