---
type: 1-1
date: 2026-03-31
person: jorge-quintero
---

# 1:1 -- Jorge Quintero -- 2026-03-31

---

## Carry-forward
*Open tracking items for Jorge Quintero -- updates live as items are completed*

```dataview
TASK FROM "40-people/jorge-quintero/1-1s" OR "00-daily" OR "90-meeting-notes"
WHERE !completed AND contains(tags, "#tracking")
  AND (person = "jorge-quintero" OR contains(file.path, "40-people/jorge-quintero/1-1s"))
SORT file.mtime DESC
```

---

## Their agenda
<!-- What they want to cover -- capture before or at start of meeting -->

## My agenda
<!-- Coaching focus, delegation check, capability push for this session -->

### Framing: First Real 1:1 + Org Move + Vacation Prep
This is the first structured 1:1 with Jorge. He is transitioning from Sarah's Finance team into Operations, and his function is being renamed from "Business Intelligence" to "Operational Intelligence." This was presented at the board meeting last week. He needs to understand: (1) the board saw his function as a strategic investment, not a reporting team, (2) his scope is larger than dashboards, and (3) he needs to get out of Discovery.

I'm going on vacation, so he needs clear, achievable priorities for the week.

### 1. Board Debrief: OI Was Positioned as Strategic (5 min)
What the board heard about Jorge's function:
- He was called out by name on slide 40: "Moving Jorge from Sarah's Finance team to Operations to create a new Operations Intelligence function."
- Scope as presented: data pipelines, unified data views, monitoring consolidation (the two-Zabbix problem), data strategy.
- Explicitly framed as "beyond creating BI dashboards for sales."
- The MCP cost allocation correction (~$466K margin swing) was referenced as proof of value: this is what happens when someone owns the data layer.
- AI Account Intelligence (35 customer reports from 8 data sources) was presented as "art of the possible" for what unified data enables.
- Data architecture assessment (124 tables, ~65GB, 9 versions of the same revenue table, abandoned staging artifacts in production) was presented as evidence for why this investment is necessary.

The message: the board sees you as the org's data architect, not a dashboard builder. That's the bar.

### 2. Role Clarity: He Owns Operational Intelligence (5 min)
Name it explicitly. Jorge is the service manager for Operational Intelligence. This is his function. The service description is the contract for what OI does and doesn't do.

Key points from the service description to reinforce:
- OI does NOT own source data (each service team owns their operational data; OI makes it accessible and usable).
- OI does NOT replace Finance reporting.
- OI DOES own: data pipeline design, unified customer view, metrics infrastructure for all service managers, monitoring platform consolidation decisions.
- The recommended model is: IT owns the platform, OI owns the monitoring stack decisions, each operational team owns their configuration.

Ask him: "Do you feel like you own this function? Where are the edges unclear?"

(Note to self: update his main .md file to reflect OI ownership formally.)

### 3. Service Description Status (5 min)
Jorge owns the OI service description (https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045223434/Operations+Intelligence).

Same ask as all service managers: review, circulate for feedback, get approval.

The OI service description has a unique challenge: it touches every other service team. It describes what OI provides TO them (data pipelines, dashboards, unified views) and what it needs FROM them (data access, source system ownership). Every service manager needs to validate this.

Ask him:
- Has he read the current version? Does it reflect his understanding of the mandate?
- Can he circulate it to the other service managers for review by end of week?
- Specific flag: the "Tooling Ownership" section is politically sensitive (who owns Zabbix, JSM config, Datadog, LogicMonitor). Does he agree with the recommended model? Is he ready to own that conversation?

### 4. Capacity Framework: OI's Role (10 min)
I sent the capacity framework to the team. The full framework covers:

- **Space/Power/Racks** (George's domain)
- **Network** (Ben's domain, with complexity per Ben's feedback: "it would be like x1, x2, etc. and z1, z2, etc. given the number of different capacity elements")
- **Compute** (Martin's domain)
- **People** (managed services headcount, cross-team)

Jorge's role in this is critical but indirect. He doesn't own any of these capacity numbers. He owns the data layer that makes them visible, comparable, and trustworthy.

Ask him:
- Where does this data live today? Is any of it in the pipelines he's already building?
- Can OI become the single place where capacity data is consolidated and published?
- What would it take to build a "capacity dashboard" that pulls space/power/rack data from George, network data from Ben, compute data from Martin?
- Is this a Q3 project or a Q4 project? What would need to be true to start?

This is the kind of work that makes OI indispensable. Frame it as an opportunity, not an assignment.

### 5. Accelerating Out of Discovery (10 min)
The service description flags this explicitly: "Every month in Discovery is another month of decisions made without data. This is the highest-leverage investment in the org at this stage."

The board deck presented OI as "Discovery phase, team size TBD." That needs to change. The scope is significant: pipelines from 8+ services, unified monitoring, customer health view, financial accuracy, and now potentially a capacity visibility layer.

Ask him:
- What does he need to move from Discovery to Alpha?
- Is it headcount? Tooling access? A mandate he doesn't have yet?
- What can he deliver in the next 30 days that would demonstrate OI is operational, not just planned?
- Specific deliverable idea: Can he produce a "state of the data" document that maps every data source, pipeline status (live/planned/blocked), and owner? This would be his equivalent of the service description, but for the data layer itself.

### 6. Active Work: Quick Check (5 min)
Pulse check on items he's likely working on:

**AccountIntel pipeline**
- 35 customer reports generated for STG. Is he getting feedback? Are the reports being used?
- Any data source gaps he's hitting?

**Monday Morning Reports**
- He's currently producing these. Is this sustainable, or is it consuming too much of his time?

**Financial data accuracy**
- The MCP cost correction was a big win. Are there other known cost allocation issues he's tracking?

**Two-Zabbix problem**
- Per the service description: "VP of Operations owns the decision. Operational Intelligence owns the execution." I need to give him the mandate. Flag this for a deeper conversation post-vacation, but ask: has he started scoping what consolidation would look like?

### 7. Priorities for the Week (5 min)
Three things for the week while I'm out:

1. **Service description:** Review it, circulate to all service managers for feedback by Friday Apr 4. This is politically important because OI touches everyone.
2. **State of the data map:** First draft. Every data source, pipeline status (live/planned/blocked), owner, and gaps. By Monday Apr 7.
3. **Capacity framework input:** Think through how OI could consolidate capacity data across the service teams. Come back with a rough proposal (not a build, just a "here's what it would take").

Everything else continues as BAU. The message: you're building a function, not running a reporting desk. These three things establish the foundation.

---

## Discussion Notes
<!-- Raw capture -- don't over-format in real time, just get it down -->

---

## Decisions & Actions

| Action | Owner | By When |
|--------|-------|---------|
| Review OI service description and circulate to all service managers for feedback | Jorge | Fri Apr 4 |
| Produce first draft "state of the data" map (sources, pipeline status, owners, gaps) | Jorge | Mon Apr 7 |
| Draft rough proposal for capacity data consolidation via OI | Jorge | Mon Apr 7 |
| Give Jorge explicit VP mandate on Zabbix consolidation (deeper conversation) | Adam | Post-vacation |
| Update jorge-quintero.md with OI service ownership | Adam | Before vacation |
| | | |

<!-- Inline tracking tasks -- tag with #tracking so they surface on the hub -->
- [ ] Jorge to review and circulate OI service description to all service managers by Fri Apr 4 #tracking [person::jorge-quintero]
- [ ] Jorge to produce first draft "state of the data" map by Mon Apr 7 #tracking [person::jorge-quintero]
- [ ] Jorge to draft rough proposal for capacity data consolidation via OI by Mon Apr 7 #tracking [person::jorge-quintero]
- [ ] Adam to give Jorge explicit VP mandate on Zabbix consolidation post-vacation #tracking [person::jorge-quintero]
- [ ] Adam to update jorge-quintero.md with OI service ownership #tracking [person::jorge-quintero]

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->
<!-- Watch for: Does Jorge think of himself as a function owner or a report builder? Can he articulate what OI needs to move out of Discovery, or does he wait for direction? Does the capacity framework opportunity excite him or overwhelm him? How does he react to the "circulate to all service managers" ask (this requires cross-org influence, not just technical skill). -->

## Next session focus
<!-- After vacation: Did the service description get circulated? Did the data map land? If yes, Jorge can operate as a function owner. If the data map is good, it becomes the OI roadmap. Start planning the Zabbix consolidation mandate conversation. Begin scoping headcount needs to get OI out of Discovery. -->
