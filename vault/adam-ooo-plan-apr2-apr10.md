# Adam Nelson — Out of Office Plan

**Out:** Wednesday April 2 through Friday April 10, 2026
**Back:** Monday April 13, 2026

---

## Things Adam MUST Do Before Leaving (April 1)

These are actions only Adam can take. They cannot be delegated and must happen today.

1. **Update all 8 people profile .md files** with service ownership designations:
   - andrei-ianouchkevitch.md → Managed Cloud service manager
   - martin-tessier.md → Compute Platforms service manager
   - jason-auer.md → Service Desk / NOC service manager
   - pat-wolthausen.md → Hybrid Solution Architecture service manager
   - ben-kennedy.md → Networking service manager
   - george-revie.md → Data Center Operations service manager
   - jorge-quintero.md → Operational Intelligence service manager
   - lacie-ellen-morley.md → Hybrid Service Delivery Management service manager

2. **Send a consolidated "Adam OOO" message** to the full team (Slack/Teams/email) with:
   - Dates: Out Apr 2–10, back Apr 13
   - The #1 priority while I'm out: **service description reviews** — every service manager must review their description and circulate for teammate/stakeholder feedback by Fri Apr 4
   - The #2 priority: capacity snapshot first pass by Mon Apr 7
   - Escalation path while I'm out (see below)

3. **Confirm no open P1/P2 incidents** with Jason before EOD today

4. **Confirm Lacie's queue triage** is on track for Wed Apr 2 (SDM queue and SD board — flag anything red)

5. **Confirm DGI Travel (GSE-270) RFP** ownership — due Apr 8, F2F presentation Apr 16. Confirm who is running point (Lacie/Pat) and whether they need anything from Adam before he leaves.

6. **Set out-of-office** on email, Slack, Teams, calendar

7. **Approve Pat Wolthausen's time-off requests in ADP** — 3 pending requests from Mar 31. Unread.

8. **Approve Charles Rutledge Jr's time-off request in ADP** — escalated to Adam due to inaction (originally submitted Mar 23). Unread.

9. **Respond to Ikram Nagdawala re: Leadership page update on aptum.com** — needs Adam's bio/headshot input by end of week (email Mar 31). Sarah is also on this.

10. **Review Megaport Agreement** — Vicki Patten sent the agreement (HIGH importance, Mar 30) asking Adam and Ben to review for resell of Megaport services. Nedim's comments need Supply Chain or Product review. Ben should also review. Unread.

11. **Smart Scale SQL licensing decision** — active Teams thread today with Andy Petterson and Jason. Adam told Jason to "get on top of this." Need documentation that Aptum is compliant from an MS licensing perspective stored in an easily retrievable location. Confirm Jason has this before leaving.

12. **Roger Gonzales: Managed Cloud Details** — forwarded customer communication (Mar 26). Unread. Determine if action needed or can be deferred.

13. **Fix Jira automation failure** — "Assign Activities to Service Delivery Manager Queue" rule failed (Mar 31). Lacie or Jason should look at this.

14. **BI Report: Pending Customer Approval orders** — Matthew Carter asking Adam's team to take over this report. Adam replied Mar 31. Confirm handoff to Lacie/Jorge is complete.

---

## Escalation Path While Adam Is Out

| Situation | First Contact | Escalate To |
|-----------|---------------|-------------|
| P1/P2 operational incident | Jason Auer (NOC owns all incidents) | If customer-facing and political: Lacie (HSDM) |
| Customer escalation / relationship issue | Lacie Allen-Morley (HSDM) | — |
| Pre-sales / SOW urgency | Pat Wolthausen (HSA) | — |
| DC facility emergency | George Revie (DC Ops) | — |
| Network outage / circuit issue | Ben Kennedy (Networking) | — |
| Financial / cost allocation question | Defer to Adam's return (non-urgent) | — |
| Anything truly critical | Contact Adam directly — phone/text only | — |

---

## Team Deliverables While Adam Is Out

### PARAMOUNT: Service Description Reviews (Due Fri Apr 4)

Every service manager must review their service description on Confluence and circulate it to their team and adjacent stakeholders for feedback. This is the accountability contract for each function.

| Person | Service | Confluence Link | Review With |
|--------|---------|-----------------|-------------|
| George Revie | Data Center Operations | [Link](https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045747729/Data+Center+Operations) | Martin, Ben, Jason |
| Jorge Quintero | Operational Intelligence | [Link](https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045223434/Operations+Intelligence) | All service managers |
| Lacie Allen-Morley | Hybrid Service Delivery Mgmt | [Link](https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5044076554/Hybrid+Service+Delivery+Management) | SDMs, HSA, ops teams |
| Andrei Ianouchkevitch | Managed Cloud | [Link](https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5044273167/Managed+Cloud) | Ben, Jason, Martin |
| Martin Tessier | Compute Platforms | [Link](https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045518349/Compute+Platform) | George, Jason, Andrei |
| Jason Auer | Service Desk / NOC | [Link](https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045223425/Service+Desk+NOC) | Andrei, George, Ben, Lacie |
| Pat Wolthausen | Hybrid Solution Architecture | [Link](https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045747720/Hybrid+Solution+Architecture) | Lacie, Commercial/Fred |
| Ben Kennedy | Networking | [Link](https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045977089/Networking) | Andrei, Jason, George |

### Capacity Snapshots — First Pass (Due Mon Apr 7)

| Person | Capacity Dimensions | Notes |
|--------|---------------------|-------|
| George Revie | Space, Power, Racks by location | Even directional is fine. Start with headline numbers. |
| Ben Kennedy | Ports, Bandwidth, IP inventory by location | He already acknowledged complexity — start with headlines. |
| Martin Tessier | Compute capacity by type and location, provisioning backlog | Split: dedicated vs. private cloud vs. AptCloud |
| Jason Auer | People, hours, coverage by shift. Service-to-engineer ratio | Total hours, committed hours, actual hours |
| Andrei Ianouchkevitch | Managed environment count by type (public/private/AptCloud) | Data may be in tools or tribal knowledge — document either way |
| Jorge Quintero | State of the data map (sources, pipeline status, owners, gaps) | This is OI's equivalent of a capacity view |

### Additional Deliverables by Person

**George Revie:**
- Written Centrilogic onboarding status (plan, needs, timeline) — Fri Apr 4
- Document UK staffing model (own staff vs. contracted remote hands) — Fri Apr 11

**Jorge Quintero:**
- Draft rough proposal for capacity data consolidation via OI — Mon Apr 7
- Think through how OI becomes the single consolidation layer for capacity data

**Lacie Allen-Morley:**
- Full triage of SDM queue and SD board, flag anything red — Wed Apr 2
- Document Azure specialization status with Melvin — Fri Apr 4

**Martin Tessier:**
- Written AptCloud platform status (current state, Beta readiness, needs, timeline) — Fri Apr 4

**Andrei Ianouchkevitch:**
- Confirm cost allocation correction status with Finance/Jason — Fri Apr 4

**Jason Auer:**
- Confirm cost allocation correction alignment with Andrei and Finance — Fri Apr 4

**Pat Wolthausen:**
- Utilization report: billable vs. non-billable per person — Mon Apr 7
- Estimate-to-actual variance on last 3 completed projects — Mon Apr 7
- Active pre-sales pipeline status — Fri Apr 4

### Universal Ask: Channel Review (Due Wed Apr 2)

ALL team members must review their emails, Jira, Slack, Teams, and calendars for anything they are accountable for that needs attention while Adam is out. Update 1-1 notes with anything flagged.

---

## Open Items That May Need Attention While Adam Is Out

### From Email / Teams / Jira (sourced Apr 1)

**Needs action before Adam leaves:**
- **Megaport Agreement review** — Vicki Patten (HIGH importance). Ben also needs to review. Agreement for resell of Megaport services. Has legal/commercial comments from Nedim. Vicki says "we are on with this."
- **Smart Scale SQL licensing** — Andy Petterson laid out two options in Teams. Adam told Jason to own this. Need MS compliance documentation stored. Confirm Jason has it handled today.
- **ADP time-off approvals** — 3x Pat Wolthausen + 1x Charles Rutledge Jr (escalated). All pending.
- **Leadership page bio** — Ikram needs Adam's input by end of week for aptum.com update.
- **BI Report handoff** — Matthew Carter wants Lacie's team to own the "Pending Customer Approval orders" report. Confirm handoff is clean.

**Active threads that will continue while Adam is out:**
- **AWS/TD Synnex CTA transfer** — Distribution engagement executed Mar 31. Erik Tanguay is completing CTA per payer account. Matthew Carter running point. April timeline. This can proceed without Adam — Matthew has it.
- **Centrilogic customer list** — Marc-Alexandre Forget (SVP Sales) requested access to technical info. Active between Centrilogic (sbernardou) and Aptum. George should be tracking this alongside his onboarding status.
- **AptCloud demo/transcript** — Sarah Blanchard shared recording and document Mar 31. Non-urgent, review post-vacation.
- **Roger Gonzales: Managed Cloud Details** — forwarded customer comms (unread). May need Andrei's input.
- **Axios npm supply chain incident** — security advisory from Kobalt.io (Mar 31). IT/Engineering should be aware.

**Jira items assigned to Adam:**
- **APTUM-51645:** Approve Price Change Order 279889 (Open, P3). Needs approval — do this today or delegate.
- **APTUM-52738:** Service Delivery Management ticket (Open, P3). Check if this needs action or can wait.
- **APTUM-52907:** Test Cancellation Flow (Open). Likely a test ticket — verify.
- **RETRO-24:** Updated Pricing Sheet (In Progress). Check status.
- **PRESALES-3953:** Review and update PS effort (In Progress). Check if this is blocking anyone.

**Jira automation failure:**
- "Assign Activities to Service Delivery Manager Queue" rule failed Mar 31. Lacie or Jason should investigate.

### Calendar: Meetings Adam Will Miss (Apr 2–10)

**Thu Apr 2:**
- Three Musketeers Sync (12:30)
- [INT] Service Delivery - End of Sprint Review (1:00pm)
- CAB and customer weekend prep (3:00pm)
- [INT] SA Sync (3:00pm)
- The Weekly Update (3:30pm)
- SoW Review/Unblocking (5:30pm)

**Fri Apr 3 (Good Friday — CA, UK holiday):**
- Weeks Tweeks sans Dave (2:00pm)
- STG Aptum Cadence (3:30pm)

**Mon Apr 6 (UK Easter Monday):**
- Exec Sync (12:30pm) — **Adam should notify someone to cover or send regrets**
- Three Musketeers Sync (12:30pm)
- ESL Sync (2:05pm)
- Senior Leader Sync (3:00pm) — **Adam should notify**
- Sales Forecast & Pipeline Deep Dive (5:00pm)
- SoW Review/Unblocking (5:30pm)
- VMware P&L Analysis (6:00pm)

**Tue Apr 7:**
- Three Musketeers Sync (12:30pm)

**Key meetings requiring coverage or regrets:** Exec Sync (Apr 6), Senior Leader Sync (Apr 6), Sales Forecast & Pipeline Deep Dive (Apr 6), VMware P&L Analysis (Apr 6). These are leadership meetings — Adam should send regrets or ask someone to represent.

### Active Customer Projects (Lacie / Pat to monitor)
- **DGI Travel (GSE-270):** RFP due Apr 8, F2F presentation Apr 16. Whoever is running point needs to be confirmed before Adam leaves.
- **Apt Cloud (GSE-155):** Daily syncs happening. Monitor for blockers.
- **Ignite Migration (GSE-247):** Daily syncs happening. Monitor for blockers.
- **AWS Transfer to TD Synnex:** Matthew Carter is running point. Distribution engagement executed. April timeline for CTA. Can proceed without Adam.
- **Microsoft M365 change:** Customer comms and impact tracking. Timeline pressure TBD.
- **OBDS-SQL Licenses (GSE-306):** Closed Won by Steve Rioux (Mar 31). Project creation at PMO-2054. Confirm handoff is clean.
- **Inspirata / Cofense / TownSuite:** Rob Station (Pat's team) updated and sent quotes. Monitor.

### Financial / Org Items (Defer unless urgent)
- Cost allocation correction (Andrei/Jason/Finance) — in progress, can continue without Adam
- Jorge's Zabbix consolidation mandate — Adam needs to give this post-vacation
- Professional Services manager role — Open/TBD, no action needed this week
- VMware P&L Analysis — Matthew Carter updated Confluence (Apr 1). Review post-vacation.

### DC Portfolio Moves (George / Ben to track)
- **eStruxture consolidation:** Financial impact starts May 1. Operational readiness on track? Any loose ends?
- **Centrilogic onboarding (Q3):** George is writing status by Fri Apr 4. Marc-Alexandre Forget is requesting customer list access.
- **ATL→Herndon, LA→DataBank, Portsmouth:** Planning stage. No decisions needed before Apr 13.

---

## Transition Candidates — Items That Can Be Owned by Others

These are items currently in Adam's orbit that can and should be run by the named person without Adam's involvement:

| Item | Transition To | Why |
|------|---------------|-----|
| Service description review process | Each service manager owns their own | Adam initiated; now each SM drives their review cycle independently |
| Capacity framework data collection | Jorge Quintero (OI) as consolidator | Jorge's function is built to aggregate operational data — this is his lane |
| Centrilogic onboarding operational planning | George Revie | George owns DC Ops; this is a DC migration at its core |
| DGI Travel RFP execution | Lacie (HSDM) + Pat (HSA) | Customer delivery + technical architecture — their combined lane |
| Cost allocation correction with Finance | Andrei + Jason jointly | They own the two cost centers involved; Finance is the counterparty |
| Queue/ticket health monitoring | Jason (operational) + Lacie (customer relationship) | These are their core functions |
| Pre-sales pipeline management | Pat Wolthausen | HSA owns the technical scope — Pat should manage pipeline visibility |
| Azure specialization tracking | Lacie + Melvin | This was already delegated; just needs anchoring |
| AptCloud platform status reporting | Martin (build) + Andrei (operations) | They co-own the platform; status should come from them jointly |

---

## What to Review When Adam Returns (April 13)

**Deliverables check:**
1. Did every service description get circulated for review by Apr 4?
2. Did capacity snapshots land by Apr 7?
3. Review all 1-1 notes for flagged items from channel reviews
4. Review Lacie's queue triage — any red items?
5. George's Centrilogic onboarding status — is migration planning real?
6. Martin's AptCloud status — what's needed for Beta?
7. Jason's SLA performance for the two weeks out
8. Pat's utilization data — above or below 50%?
9. Jorge's state of the data map — does OI have a roadmap now?
10. Ben's DC migration network impact assessment

**Decisions Adam needs to make post-vacation:**
11. Give Jorge the explicit VP mandate on Zabbix consolidation
12. Deep-dive on Professional Services manager role decision
13. Review Megaport Agreement (if not completed before leaving)
14. Review AptCloud demo/transcript from Sarah Blanchard
15. Review VMware P&L Analysis (Matthew Carter's Confluence updates)
16. Smart Scale SQL licensing — confirm final documentation is stored
17. Check Jira: RETRO-24 (Updated Pricing Sheet) and PRESALES-3953 (PS effort review) status
18. Review Roger Gonzales' Managed Cloud customer communication
19. Follow up on leadership page bio with Ikram if not submitted before leaving
