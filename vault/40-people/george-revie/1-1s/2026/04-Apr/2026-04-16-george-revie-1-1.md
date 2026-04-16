---
type: 1-1
date: 2026-04-16
person: george-revie
---

# 1:1 — George Revie — 2026-04-16

---

## Carry-forward
*Open tracking items for George Revie — updates live as items are completed*

```dataview
TASK FROM "40-people/george-revie/1-1s" OR "00-daily" OR "90-meeting-notes"
WHERE !completed AND contains(tags, "#tracking")
  AND (person = "george-revie" OR contains(file.path, "40-people/george-revie/1-1s"))
SORT file.mtime DESC
```

**Open items from Mar 31 (all overdue — need status on each):**
- [ ] Review DC Ops service description and circulate for feedback (was due Fri Apr 4) #tracking [person::george-revie]
- [ ] Produce first-pass capacity snapshot — space/power/racks by location (was due Mon Apr 7) #tracking [person::george-revie]
- [ ] Written status on Centrilogic onboarding: plan, needs, timeline (was due Fri Apr 4) #tracking [person::george-revie]
- [ ] Document UK staffing model — own staff vs. contracted remote hands (was due Fri Apr 11) #tracking [person::george-revie]
- [ ] Confirm LA/Malibu local coverage adequacy (was due Fri Apr 11) #tracking [person::george-revie]

**Adam's open items:**
- [ ] Update george-revie.md with DC Ops service ownership (carried from Mar 31) #tracking [person::george-revie]

---

## Their agenda
<!-- What they want to cover — capture before or at start of meeting -->

## My agenda

### Framing: Return from Vacation + Accountability Check + OKR Deep-Dive + Product Delivery Flow Debrief
First session back. George had three deliverables for the window I was out (service description, capacity snapshot, Centrilogic status) plus two open items on UK staffing and LA/Malibu coverage. Need status on all five — honest, specific.

**New context from yesterday's meetings:** The [[2026-04-15-product-delivery-flow|Product Delivery Flow]] session confirmed George's role as **Layer 1 — Physical Provisioning**: his team racks, cables, and powers hardware. Ben's team provisions networking. They deliver infrastructure to the point where it's physically ready. George confirmed he owns Hyperview (infrastructure visualization tool). The monitoring/tool ownership conversation (Zabbix "Guardian" instance) was not resolved — that's an org-wide follow-up.

**OKR focus:** George's function has the most concrete, board-visible OKR targets in the org. The [[fy26-operations-okrs|FY26 OKRs]] from the Q2 Board Deck are explicit about what DC Ops is measured against. This session should ground every conversation in those targets.

### 1. Accountability Check: The Five Open Items (15 min)
Go through each one with specifics.

**A. DC Ops Service Description**
- Reviewed and circulated? To Martin, Ben, Jason at minimum?
- Confluence link: https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045747729/Data+Center+Operations
- Any feedback received? Any boundary disputes with Martin's team on handoff points?
- **New hard deadline if not done: Fri Apr 18.**
- **Key update from Product Delivery Flow:** The layered model is now explicit and agreed. George = Layer 1 (physical provisioning). Martin takes over from there. Does the service description align?

**B. Capacity Snapshot — Space/Power/Racks**
- First-pass view by location? Even directional numbers?
- This is foundational for the board's "double market value" goal. You can't sell what you don't know you have.
- If he doesn't have it: what would it take to produce it, and by when? Is it a CMDB accuracy problem, a data collection problem, or an ownership problem?

**C. Centrilogic Onboarding Status**
- 15 UK colo customers migrating to Portsmouth. ~C$70K/mo MRC (~C$846K annualized).
- 48% on expired contracts. Migration cost ~GBP 3,275/customer (~C$86K total), avg payback ~1.7 months.
- Where does this stand? Has migration planning started? Who's running point on his side?

**D. UK Staffing Model**
- Portsmouth/Croydon/Horner = ~1,091 services. Own staff or contracted remote hands?
- Particularly important with Centrilogic customers incoming.

**E. LA/Malibu Coverage**
- 551 services. Equivalent local coverage to other locations?
- Relevant with LAX→DataBank migration on Q4 roadmap.

### 2. Board OKR Targets: Data Center Operations — Deep Dive (15 min)
This is the main event. Walk through every OKR target from the [[fy26-operations-okrs|FY26 OKRs]] and get status:

**FY26 Cost Reduction: $680K target**
- As of Q2 Board (March 25): $646K in-year committed; $1.9M annualized run-rate.
- Where does this stand now? Any risk to hitting $680K?
- eStruxture financial impact begins May 1 ($161K/mo savings, $1.9M annualized). Is everything on track operationally?

**Uptime: 99.999% target**
- H1: 6 Major / 15 Minor incidents, all resolved, zero SLA credits.
- How has April been? Any incidents since Mar 31?
- Herndon DH2 water event, Miami generator failovers — any recurrence or follow-up?

**SLA Adherence: 98% target**
- H1: zero SLA credits. On track.
- Is he tracking this formally or is it "we haven't had a credit request"?

**R&M Reduction: ↓10% target**
- No specific number reported at board. Where does he think this stands?
- What's driving R&M spend — aging equipment? Specific locations?

### 3. 5-Year DC Plan Execution — H2 Status (10 min)
Walk through the big rocks from the board deck:

**eStruxture Consolidation (May 1 activation)**
- Financial impact starts in two weeks. Operationally ready?
- Barrie fully decommissioned? Any loose ends?

**Portsmouth Strategy & Capacity Optimization**
- ~1,091 services. Long-term consolidation plan?
- Sublease opportunities — any progress?

**Centrilogic Customer Onboarding (Q3)**
- Covered in Section 1C above. Key question: is this on track for Q3?

**Basis Migration (begins Q3, execution Q4)**
- Planning started? What's the scope?

**Q4 Moves:**
- ATL→Herndon ($1.5M 5-yr savings): planning started?
- LAX→DataBank (NPV $681K): planning started?
- Heathrow renewal: status?

### 4. Product Delivery Flow — George's Role Confirmed (5 min)
Quick confirmation from yesterday's session:
- George = Layer 1 physical provisioning. Martin takes over for compute/hypervisor. Jason handles customer-facing support. Andrei manages cloud customer consumption.
- George confirmed he owns Hyperview.
- Monitoring: George uses Zabbix (skinned as "Guardian") for physical systems monitoring. Ownership of this instance is unresolved org-wide. Does he have any concerns?
- Support is baseline cost, not a discount lever. George's team's cost is part of the fixed people cost ($150/server example) that is never discounted.

### 5. Priorities Going Forward (5 min)
1. **Service description:** Updated to reflect Product Delivery Flow layered model. Circulated and feedback collected. Deadline Fri Apr 18.
2. **Capacity snapshot:** Space/power/racks by location. This is the #1 deliverable for the board's visibility. This week.
3. **eStruxture May 1 readiness:** Confirm operational readiness for financial impact activation.
4. **Centrilogic onboarding:** Written plan with timeline. This week.
5. **OKR tracking:** Make sure he has a handle on all four targets ($680K savings, 99.999% uptime, 98% SLA, R&M ↓10%). If he's not tracking formally, start.
6. **UK staffing and LA/Malibu:** These are overdue from Mar 31. Need answers.

---

## Discussion Notes
<!-- Raw capture — don't over-format in real time, just get it down -->

---

## Decisions & Actions

| Action | Owner | By When |
|--------|-------|---------|
| Circulate DC Ops service description (updated for layered model) | George | Fri Apr 18 |
| Deliver first-pass capacity snapshot (space/power/racks by location) | George | Fri Apr 18 |
| Written Centrilogic onboarding plan with timeline | George | Fri Apr 18 |
| Confirm eStruxture May 1 operational readiness | George | Before May 1 |
| Document UK staffing model (own staff vs. contracted) | George | This week |
| Confirm LA/Malibu local coverage adequacy | George | This week |
| Provide current status on all 4 OKR targets | George | Next 1:1 |
| Update george-revie.md with DC Ops service ownership | Adam | This week |
| Schedule follow-up meeting on monitoring/tool ownership | Adam | This week |
| | | |

<!-- Inline tracking tasks -->
- [ ] George to circulate DC Ops service description (updated) by Fri Apr 18 #tracking [person::george-revie]
- [ ] George to deliver first-pass capacity snapshot (space/power/racks by location) by Fri Apr 18 #tracking [person::george-revie]
- [ ] George to deliver written Centrilogic onboarding plan with timeline by Fri Apr 18 #tracking [person::george-revie]
- [ ] George to confirm eStruxture May 1 operational readiness #tracking [person::george-revie]
- [ ] George to document UK staffing model (own staff vs. contracted) #tracking [person::george-revie]
- [ ] George to confirm LA/Malibu local coverage adequacy #tracking [person::george-revie]
- [ ] George to provide current status on all 4 DC OKR targets #tracking [person::george-revie]
- [ ] Adam to update george-revie.md with DC Ops service ownership #tracking [person::george-revie]

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->
<!-- Watch for: Can he recite his OKR targets without being prompted? Does he have the capacity numbers in his head or does he need to go dig? How does he talk about the Centrilogic onboarding — is there a plan or is it vague? Does he understand the layered model from Product Delivery Flow, or does he still think of his team's scope more broadly? How does he react to the five overdue items — accountability or excuses? -->

## Next session focus
<!-- OKR targets reviewed with real numbers. Capacity snapshot in hand — use it as the foundation for board-level capacity visibility. Centrilogic onboarding plan reviewed. eStruxture May 1 confirmed. Deep-dive on Basis migration planning (Q3). Start ATL→Herndon and LAX→DataBank planning. UK staffing and LA/Malibu resolved. -->
