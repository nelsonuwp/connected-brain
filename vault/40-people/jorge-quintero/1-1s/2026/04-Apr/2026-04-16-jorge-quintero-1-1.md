---
type: 1-1
date: 2026-04-16
person: jorge-quintero
---

# 1:1 — Jorge Quintero — 2026-04-16

---

## Carry-forward
*Open tracking items for Jorge Quintero — updates live as items are completed*

```dataview
TASK FROM "40-people/jorge-quintero/1-1s" OR "00-daily" OR "90-meeting-notes"
WHERE !completed AND contains(tags, "#tracking")
  AND (person = "jorge-quintero" OR contains(file.path, "40-people/jorge-quintero/1-1s"))
SORT file.mtime DESC
```

**Open items from Mar 31 (all overdue — need status on each):**
- [ ] Review OI service description and circulate to all service managers for feedback (was due Fri Apr 4) #tracking [person::jorge-quintero]
- [ ] Produce first draft "state of the data" map: sources, pipeline status, owners, gaps (was due Mon Apr 7) #tracking [person::jorge-quintero]
- [ ] Draft rough proposal for capacity data consolidation via OI (was due Mon Apr 7) #tracking [person::jorge-quintero]

**Active items from vault:**
- [ ] Jorge to work with Chameleon on consulting vs. professional services tagging in Salesforce (DBRG Apr 10) #tracking [person::jorge-quintero]

**Adam's open items:**
- [ ] Update jorge-quintero.md with OI service ownership (carried from Mar 31) #tracking [person::jorge-quintero]

---

## Their agenda
<!-- What they want to cover — capture before or at start of meeting -->

## My agenda

### Framing: Return from Vacation + Big Acknowledgment + Accountability Check
Two things are true simultaneously: Jorge shipped the Salesforce deployment while I was out (Apr 12, confirmed working) — that's a real win and I need to name it. And he had three strategic deliverables that were due while I was out. I'll open with the win, then move to the accountability check.

**New context from yesterday's meetings:** The [[2026-04-15-product-delivery-flow|Product Delivery Flow]] session confirmed that monitoring/tool ownership (Zabbix, DataDog, LogicMonitor, Hyperview, Ocean, PagerDuty) is an org-wide problem that was NOT resolved. Multiple teams use multiple tools with no clear ownership model. This is relevant to OI's scope — but the decision about who owns what monitoring tool is an org-wide conversation, not something to drop on Jorge alone. His role is to own the data layer and monitoring stack *decisions* once the org is ready to make them.

### 1. Open With the Win: Salesforce Deployment (3 min)
Jorge completed the Salesforce deployment on April 12 and confirmed it's working. Users were asked to reach out if they encounter issues. This is the kind of thing I need to acknowledge explicitly:
- Name it: "You shipped this while I was out. That's exactly what I mean by operating as a function owner."
- Quick debrief: any issues since go-live? Any feedback from users?
- What's next on the Salesforce side — is there a follow-on piece of work?

### 2. Accountability Check: The Three Deliverables (15 min)
Go through each one with specifics.

**A. OI Service Description**
- Reviewed and circulated to all service managers?
- Confluence link: https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045223434/Operations+Intelligence
- This one is politically complex because OI touches every other service. Any feedback received? Any resistance from service managers about what OI does/doesn't own?
- **New hard deadline if not done: Fri Apr 18. This is the highest-priority deliverable.**

**B. State of the Data Map**
- First draft produced? Every data source, pipeline status (live/planned/blocked), owner, gaps?
- This is the OI equivalent of a service description — it tells me what the function actually owns and where the gaps are.
- Even a rough spreadsheet is a start. If it doesn't exist, why not?

**C. Capacity Data Consolidation Proposal**
- Rough proposal for how OI could consolidate capacity data across service teams?
- Not asking for a build — just: "here's what it would take, here's what we'd need from each team."
- This is the kind of work that makes OI indispensable to the org.

### 3. Service Description Review: OI-Specific Talking Points (10 min)
Walk through the key flags:

**OI does NOT own source data — but does own the data layer:**
Each service team owns their operational data; OI makes it accessible and usable. Is this framing landing with the other service managers? Or are they pushing back with "we'll handle our own reporting"?

**Tooling ownership model:**
The recommended model from the service description:
- IT owns the platform (licensing, access, SSO)
- OI owns monitoring stack decisions (which tools, how they integrate, the data model, alert schema)
- Each operational team owns their configuration within the agreed platform

Does Jorge agree with this model? Is he ready to own the monitoring stack decisions — not just execute them, but make them?

**Still in Discovery — what needs to change:**
The board deck called OI out by name as a strategic investment. The service description says: "Every month in Discovery is another month of decisions made without data." What does OI need to move from Discovery to Alpha?
- Is it headcount?
- Is it tooling access?
- Is it a mandate he doesn't have yet? (Some of that closes with the Zabbix decision today.)
- What can he show in the next 30 days that proves OI is operational?

**CEM dependency:**
The HSDM service description calls out a CEM gap (no one owns proactive customer health monitoring). The OI service description is explicit: CEM can't operate without OI providing the customer health data layer. Is Jorge aware of this dependency? Is it motivating to him or does it feel like scope creep?

**Team size:**
The org is pushing OI toward Alpha on a "Discovery phase, team size TBD" budget. The scope is significant: 8+ service pipelines, unified monitoring, customer health view, financial accuracy, capacity visibility, Salesforce integration. What does Jorge think he actually needs?

### 4. DBRG: Consulting vs. Professional Services Tagging (5 min)
From the April 10 DBRG notes: Jorge is on the hook to work with Chameleon on consulting vs. professional services tagging in Salesforce.
- What's the scope of this? Is it a data pipeline change, a Salesforce config change, or something else?
- Does this conflict with other priorities, or can it run in parallel?
- Timeline?

Note: The DBRG also clarified that PS attribution moves to Sarah Blanchard for the LOB financial reporting, but Jorge stays involved from a data pipeline coherence perspective. Does he understand that distinction?

### 5. AI Huddle (Apr 14) — Quick Debrief (3 min)
Jorge was in the AI huddle with Brett, Fred, and Will yesterday.
- Anything actionable that affects OI's work?
- Any AI tooling or data pipeline use cases that surfaced?

### 6. VMware P&L Analysis (Apr 13) — OI Angle (3 min)
Jorge was in the VMware P&L session.
- Was his role providing data, or was he there to learn context?
- Does this surface a new data pipeline need (VMware P&L visibility)?

### 7. Priorities Going Forward (5 min)
1. **Service description:** Circulated to all SMs, feedback collected. Deadline Fri Apr 18.
2. **State of the data map:** This is Jorge's north star document for the function. If it doesn't exist, everything else is noise.
3. **Chameleon tagging work:** Get a timeline and make sure it doesn't crowd out the above.
4. **Monitoring landscape awareness:** The Product Delivery Flow session surfaced that monitoring/tool ownership is unresolved org-wide. Jorge should be thinking about what OI's role is in that conversation — but it's not his sole mandate to execute. Frame it as: "When the org is ready to consolidate, OI will own the data layer and standards. Start thinking about what that looks like."

---

## Discussion Notes
<!-- Raw capture — don't over-format in real time, just get it down -->

---

## Decisions & Actions

| Action | Owner | By When |
|--------|-------|---------|
| Circulate OI service description to all service managers (if not yet done) | Jorge | Fri Apr 18 |
| Deliver first draft state of the data map (if not yet done) | Jorge | Next 1:1 |
| Chameleon consulting vs. PS tagging — timeline defined | Jorge | This week |
| Update jorge-quintero.md with OI service ownership | Adam | This week |
| | | |

<!-- Inline tracking tasks -->
- [ ] Jorge to circulate OI service description to all service managers by Fri Apr 18 #tracking [person::jorge-quintero]
- [ ] Jorge to deliver first draft state of the data map #tracking [person::jorge-quintero]
- [ ] Jorge to work with Chameleon on consulting vs. PS tagging — timeline to be confirmed #tracking [person::jorge-quintero]
- [ ] Adam to update jorge-quintero.md with OI service ownership #tracking [person::jorge-quintero]

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->
<!-- Watch for: Does he have a view on what OI needs to exit Discovery, or does he wait for me to tell him? How does he talk about the state of the data map — does he have a clear picture in his head, or is it still fuzzy? Does the Salesforce deployment tell you he can ship, or was it a one-off? When monitoring ownership comes up, does he see OI's role clearly, or does he try to take on the whole problem? -->

## Next session focus
<!-- Service description feedback reviewed. State of the data map in hand — use it as the OI roadmap. Begin scoping headcount needs to move OI out of Discovery. Check Chameleon tagging progress. Monitoring/tool ownership is org-wide — revisit OI's role once the broader conversation happens. -->
