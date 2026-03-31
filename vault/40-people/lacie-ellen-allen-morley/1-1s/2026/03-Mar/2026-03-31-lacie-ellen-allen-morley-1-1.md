---
type: 1-1
date: 2026-03-31
person: lacie-ellen-morley
---
 
# 1:1 — Lacie Ellen Morley — 2026-03-31
 
---
 
## Carry-forward
*Open tracking items for Lacie Ellen Morley — updates live as items are completed*
 
```dataview
TASK FROM "40-people/lacie-ellen-morley/1-1s" OR "00-daily" OR "90-meeting-notes"
WHERE !completed AND contains(tags, "#tracking")
  AND (person = "lacie-ellen-morley" OR contains(file.path, "40-people/lacie-ellen-morley/1-1s"))
SORT file.mtime DESC
```
 
---
 
## Their agenda
<!-- What they want to cover — capture before or at start of meeting -->
 
## My agenda
<!-- Coaching focus, delegation check, capability push for this session -->
 
### Framing: Reset Conversation
This is effectively our first real 1:1. I need to set the tone: I'm here to support her, give her clarity, and help her prioritize. She appears to be drowning in scope. The goal today is not to pile more on, it's to take things OFF and give her a clear, achievable week.
 
I'm going on vacation, so she needs to leave this meeting with a short list of objectives she can own and deliver against while I'm out. No ambiguity, no "when you get to it." Concrete, time-boxed, winnable.
 
### 1. Board Context (5 min)
Brief her on key takeaways from last week's board meeting. Not a full debrief, just what matters for her world:
- Revenue trajectory and retention emphasis (the board cares about churn/risk, which is her lane)
- PS revenue and delivery quality (she's accountable for SOW delivery and project health)
- Any signals about headcount, investment, or strategic shifts she should be aware of
 
The point: connect her work to what the board sees. She should understand why the things I'm about to prioritize actually matter.
 
### 2. Role Clarity: She Owns HSDM (5 min)
Name it explicitly: Lacie is the service manager for Hybrid Service Delivery Management. This is her function. She is accountable for everything in the service description, and the service description is the contract between her team and the rest of the org.
 
Ask her: "Do you feel like you own this service?" Listen for where she feels unclear or unsupported.
 
(Note to self: update her main .md file to reflect this ownership formally.)
 
### 3. Priority #1 for the Week: Service Description (10 min)
The single most important deliverable right now is getting the HSDM service description finished, reviewed by her teammates, and approved.
- Confluence link: https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5044076554/Hybrid+Service+Delivery+Management
- This is her "constitution." Everything else flows from it: what her team does, what they don't do, how they're measured, who they depend on.
- She has it listed in her working doc but it's buried under 20+ other items with no clear priority signal.
 
Ask her:
- Where is it at? What's blocking final review?
- Who needs to review it? (likely her SDMs, HSA, and the ops teams she coordinates with)
- Can we get it circulated for review by end of week and approved by the following Monday?
 
This is the kind of deliverable that, once done, creates leverage for everything else. It forces clarity on scope, accountability, and boundaries.
 
### 4. Priority #2 for the Week: Risk/Cancellation Queue Health (10 min)
She owns the service delivery queue in Jira (https://aptum.atlassian.net/jira/servicedesk/projects/APTUM/queues/custom/1233) and the SD board (https://aptum.atlassian.net/jira/software/c/projects/SD/boards/206). These are operational queues that can't go unmanaged.
 
Her working doc shows she knows the churn/risk/cancellation process needs work:
- E2E process revisions still need to go to Matthew/Sarah
- Reporting gaps on known churn without formal cancellation requests
- Winback program undefined
- Cancellation form in Jira needs updates (asset field limit of 20)
 
For this week, don't try to solve all of it. Just ask:
- Are there any tickets in the queue right now that are at risk of falling through the cracks?
- Is anything customer-facing that needs immediate attention?
- Can you do a full triage of both queues and flag anything red to me by Wednesday?
 
The objective: no surprises while I'm away. Triage, flag, escalate if needed.
 
### 5. Priority #3 (Stretch): Azure Specialization Status Check (5 min)
She co-owns this with Melvin. Her own working doc has it listed with question marks ("Status?" "Requirements?" "Training/certs progress?"). That tells me she doesn't have a clear handle on where this stands.
 
Ask her:
- Can you get a status update from Melvin and document where we actually are?
- What's the next milestone, and when is it?
 
This isn't urgent for the week, but it's the kind of thing that drifts if nobody anchors it.
 
### 6. The "Not This Week" List (5 min)
This is the most important coaching moment. Her working doc is a wall of items with no prioritization. She needs permission (and direction) to deprioritize.
 
Things that are important but NOT this week:
- Order processing E2E documentation
- Renewals process documentation
- Sales call queue routing decision
- Aged pending orders >30 day cancellation initiative
- Cloud onboarding/offboarding process documentation
- Service delivery process flow and templates
- Changes of primary/entity approval process
- Super DNS internal project creation
 
These are all real work that needs to happen. But none of them are on fire this week, and trying to do them all at once is why she's drowning.
 
The message: "I'm not asking you to forget these. I'm asking you to park them. Your three deliverables this week are (1) service description circulated for review, (2) queue triage with anything red flagged to me, and (3) Azure specialization status documented. That's it. Everything else waits."
 
### 7. Ongoing Projects: Quick Check (5 min)
She has several active projects that are in motion. Don't deep-dive, just pulse-check:
- **DGI Travel (GSE-270):** RFP due April 8, F2F presentation April 16. Is she on track? Does she need anything from me?
- **Apt Cloud (GSE-155) and Ignite Migration (GSE-247):** These have daily syncs. Are they progressing or stuck?
- **AWS Transfer to TD Synnex:** I'm already involved in this. Where does she need help vs. what can she run?
- **Microsoft M365 change:** Impacted customer list, comms. What's the timeline pressure here?
 
For anything that isn't on fire, the answer is "keep doing what you're doing, we'll deep-dive next session."
 
### 8. Structure Going Forward (5 min)
Set expectations for our cadence:
- Weekly 1:1, same time, same structure
- She brings her agenda first (what's blocking her, what she needs from me)
- I bring coaching focus and priority alignment
- We use this template every time, decisions and actions get tracked with #tracking tags
- Her working doc is useful but needs to become a prioritized backlog, not a flat list. We'll work on that together over the next few sessions.
 
---
 
## Discussion Notes
<!-- Raw capture — don't over-format in real time, just get it down -->
 
---
 
## Decisions & Actions
 
| Action | Owner | By When |
|--------|-------|---------|
| Circulate HSDM service description for teammate review | Lacie | Fri Apr 4 |
| Full triage of SDM queue and SD board, flag anything red | Lacie | Wed Apr 2 |
| Get Azure specialization status from Melvin, document current state | Lacie | Fri Apr 4 |
| Update Lacie's main .md file to reflect HSDM ownership | Adam | Before vacation |
| | | |
 
<!-- Inline tracking tasks — tag with #tracking so they surface on the hub -->
- [ ] Lacie to circulate HSDM service description for review by Fri Apr 4 #tracking [person::lacie-ellen-morley]
- [ ] Lacie to triage SDM queue and SD board, flag red items by Wed Apr 2 #tracking [person::lacie-ellen-morley]
- [ ] Lacie to document Azure specialization status with Melvin by Fri Apr 4 #tracking [person::lacie-ellen-morley]
- [ ] Adam to update lacie-ellen-morley.md with HSDM service ownership #tracking [person::lacie-ellen-morley]
 
---
 
## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->
<!-- Watch for: Does she push back on the "not this week" list, or does she seem relieved? Does she have a clear sense of where the service description stands, or is it vague? Can she articulate the state of her queues without looking things up? These will tell you whether the gap is prioritization skill, operational grip, or both. -->
 
## Next session focus
<!-- After vacation: Review whether the three deliverables landed. If they did, she can execute when given focus. If they didn't, dig into why (capacity? clarity? confidence?) and adjust accordingly. Begin converting her working doc into a prioritized backlog. -->