---
type: 1-1
date: 2026-03-31
person: george-revie
---

# 1:1 -- George Revie -- 2026-03-31

---

## Carry-forward
*Open tracking items for George Revie -- updates live as items are completed*

```dataview
TASK FROM "40-people/george-revie/1-1s" OR "00-daily" OR "90-meeting-notes"
WHERE !completed AND contains(tags, "#tracking")
  AND (person = "george-revie" OR contains(file.path, "40-people/george-revie/1-1s"))
SORT file.mtime DESC
```

---

## Their agenda
<!-- What they want to cover -- capture before or at start of meeting -->

## My agenda
<!-- Coaching focus, delegation check, capability push for this session -->

### Framing: First Real 1:1 + Vacation Prep
First structured 1:1 with George. He owns Data Center Ops, one of the most tangible and financially significant functions in the org. The board meeting last week featured his work prominently (eStruxture lease, DC strategy, Centrilogic onboarding, operational resilience). This meeting needs to: (1) connect his work to board-level priorities, (2) get clear on H2 execution status, (3) introduce the capacity framework, and (4) give him a focused week while I'm out.

### 1. Board Debrief: DC Was a Bright Spot (5 min)
Quick summary of what landed well at the board:
- eStruxture 5-year lease negotiated: $8.1M of the $10.6M 5-year DC plan locked in. $161K/mo savings, $1.9M annualized. Financial impact begins May 1.
- H1 Operational Resilience: 6 Major / 15 Minor incidents, all resolved, zero SLA credits. Herndon DH2 water event contained in 40 min, no customer impact. Miami: 4 generator failovers from FPL grid instability, all by design.
- DC portfolio efficiency assessment complete: ATL->Herndon ($1.5M 5-yr savings), LA->DataBank (NPV $681K), Portsmouth sublease pursuit.
- C$4.8M annualized cost reduction across H1 (his DC portion is significant).

The message: the board sees DC as executing. That's good. Now the question is sustaining it through H2.

### 2. Service Description Status (5 min)
George owns the Data Center Ops service description (https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045747729/Data+Center+Operations).

Same ask as all service managers: the description needs to be reviewed by his team and adjacent stakeholders, then approved. This is the accountability contract for his function.

Ask him:
- Has he read the current version? Does it accurately reflect what his team does and doesn't do?
- Who needs to review it? (Compute Platforms/Martin, Network/Ben, Service Desk/Jason at minimum)
- Can it be circulated for review by end of week?

### 3. Capacity Framework: The Big Ask (15 min)
I sent the capacity framework to the team. For George, the DC dimensions are the most directly relevant:

**Space:**
- We have X sellable sqft
- We've allocated Y sqft (to colo cages, our own racks, etc.)
- We have Z sqft available to sell without spending more

**Power:**
- We have X kW provisioned
- We've committed Y kW to customers and our own gear
- We have Z kW available to sell without spending more

**Racks:**
- We own X racks installed on the floor
- We've sold/filled Y racks (colo + our hosting)
- We have Z racks available to sell without buying more

This data is foundational for the board's "double market value" goal. You can't sell what you don't know you have, and you can't plan capital if you don't know where you're full.

Ask him:
- Can he produce this by location? Even directionally?
- Where is this data today? CMDB? Spreadsheets? Tribal knowledge?
- What are the blockers to getting a first pass? (If it's CMDB accuracy, that's a known issue from the service description.)
- Target: first draft of the space/power/racks snapshot by end of next week (Apr 7).

Context from Ben's feedback on the network capacity piece: "For X and Z, it would be like x1, x2, etc. and z1, z2, etc. given the number of different capacity elements." Same will likely be true for George on power density per rack vs. aggregate power, etc. That's fine. Start with the headline numbers, refine later.

### 4. H2 Execution: Status Check on the Big Rocks (10 min)
Walk through the H2 items from the board deck. Don't deep-dive, just pulse check:

**Centrilogic Customer Onboarding (Q3)**
- 15 UK colo customers migrating to Portsmouth. ~C$70K/mo MRC (~C$846K annualized).
- Perforce Software removed (~GBP 22k), no longer in projections.
- 48% on expired contracts (retention risk but also conversion opportunity).
- Migration cost: ~GBP 3,275/customer (~C$86K total), avg payback ~1.7 months.
- Where is this at? Has migration planning started? Who's running point on his side?

**eStruxture Consolidation (May 1 activation)**
- Financial impact starts May 1. Is everything on track operationally?
- Barrie decommissioned. Any loose ends?

**Portsmouth Strategy**
- Define long-term consolidation plan for third-largest location (~1,091 services).
- Sublease opportunities. Any progress on this?

**Q4 Planning (flag, don't solve)**
- ATL->Herndon, LAX->DataBank, Heathrow renewal. Are planning activities started?

### 5. Open Questions from the Service Description (5 min)
Two flags I left in his service description that need answers:

1. **UK physical presence:** Portsmouth/Croydon/Horner accounts for ~1,091 services. Does George's team have adequate local staffing for remote hands and hardware remediation, or does he rely on contracted third-party remote hands? This needs to be explicit and documented, especially with Centrilogic customers coming in.

2. **LA/Malibu:** 551 services, comparable scale to Atlanta and Miami. Does this location have equivalent local coverage? Especially relevant since LAX->DataBank migration is on the Q4 roadmap.

### 6. Priorities for the Week (5 min)
Three things for the week while I'm out:

1. **Service description:** Review it, circulate for feedback by Friday Apr 4.
2. **Capacity snapshot first pass:** Space/Power/Racks by location. Even a rough cut. Target Apr 7.
3. **Centrilogic onboarding status:** Written summary of where migration planning stands, what's needed, and timeline. By Friday Apr 4.

Everything else continues as BAU. The message: these three things are your focus deliverables.

---

## Discussion Notes
<!-- Raw capture -- don't over-format in real time, just get it down -->

---

## Decisions & Actions

| Action | Owner | By When |
|--------|-------|---------|
| Review DC Ops service description and circulate for teammate feedback | George | Fri Apr 4 |
| Produce first-pass capacity snapshot (space/power/racks by location) | George | Mon Apr 7 |
| Written status on Centrilogic onboarding: plan, needs, timeline | George | Fri Apr 4 |
| Document UK staffing model (own staff vs. contracted remote hands) | George | Fri Apr 11 |
| Confirm LA/Malibu local coverage adequacy | George | Fri Apr 11 |
| Update george-revie.md with DC Ops service ownership | Adam | Before vacation |
| | | |

<!-- Inline tracking tasks -- tag with #tracking so they surface on the hub -->
- [ ] George to review and circulate DC Ops service description by Fri Apr 4 #tracking [person::george-revie]
- [ ] George to produce first-pass capacity snapshot (space/power/racks by location) by Mon Apr 7 #tracking [person::george-revie]
- [ ] George to deliver written Centrilogic onboarding status by Fri Apr 4 #tracking [person::george-revie]
- [ ] George to document UK staffing model (own staff vs. contracted) by Fri Apr 11 #tracking [person::george-revie]
- [ ] George to confirm LA/Malibu local coverage adequacy by Fri Apr 11 #tracking [person::george-revie]
- [ ] Adam to update george-revie.md with DC Ops service ownership #tracking [person::george-revie]

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->
<!-- Watch for: Can he articulate the capacity picture off the top of his head, or does he need to go dig? Does he have a handle on Centrilogic onboarding, or is it vague? How does he react to the service description ask (ownership mindset or compliance mindset)? -->

## Next session focus
<!-- After vacation: Did the capacity snapshot land? If it did, George can produce structured data on demand, which is critical for his role. If not, dig into whether it's a data problem (CMDB gaps) or an ownership problem (he doesn't think it's his job). Deep-dive on Centrilogic onboarding plan. -->
