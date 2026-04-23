---
type: 1-1
date: 2026-04-23
person: george-revie
---

# 1:1 — George Revie — 2026-04-23

---

## Carry-forward
*Open tracking items for George Revie — manually reviewed 2026-04-23*

**From Mar 31:**
- [x] George to review all channels for open accountabilities by Wed Apr 2 — *old, done* #tracking [person::george-revie]
- [ ] George to review and circulate DC Ops service description — **page last updated Feb 27 (created by Adam); George has never edited it** #tracking [person::george-revie]
- [ ] George to produce first-pass capacity snapshot (space/power/racks by location) — **no evidence; overdue since Apr 7** #tracking [person::george-revie]
- [ ] George to deliver written Centrilogic onboarding status — **no evidence** #tracking [person::george-revie]
- [ ] George to document UK staffing model (own staff vs. contracted) — **no evidence** #tracking [person::george-revie]
- [ ] George to confirm LA/Malibu local coverage adequacy — **no evidence** #tracking [person::george-revie]
- [ ] Adam to update george-revie.md with DC Ops service ownership — **still open** #tracking [person::george-revie]

**From Apr 16:**
- [ ] George to circulate DC Ops service description (updated for layered model) by Fri Apr 18 — **page still at Feb 27 original; not circulated** #tracking [person::george-revie]
- [ ] George to deliver first-pass capacity snapshot by Fri Apr 18 — **still no evidence** #tracking [person::george-revie]
- [ ] George to deliver written Centrilogic onboarding plan with timeline by Fri Apr 18 — **still no evidence** #tracking [person::george-revie]
- [ ] George to confirm eStruxture May 1 operational readiness — **⚠️ May 1 is in 9 days — status unknown** #tracking [person::george-revie]
- [ ] George to document UK staffing model — **still open** #tracking [person::george-revie]
- [ ] George to confirm LA/Malibu local coverage adequacy — **still open** #tracking [person::george-revie]
- [ ] George to provide current status on all 4 DC OKR targets — **not received** #tracking [person::george-revie]
- [ ] Adam to update george-revie.md with DC Ops service ownership — **still open** #tracking [person::george-revie]

---

## Their agenda
<!-- What they want to cover — capture before or at start of meeting -->

## My agenda

### Framing: The Page and the Pattern — Then Two Specific Additions
George's service description page has not been touched since the day it was created (Feb 27, by Adam). He's the only service manager where I haven't seen any edit from him. That's the pattern conversation — but keep it brief and constructive. The bigger need today is two specific additions to the page (inventory and team utilization), plus an urgent eStruxture May 1 check. And the capacity snapshot is now nearly three weeks overdue — if it's a data problem, that needs to surface; if it's a prioritization problem, that's a different conversation.

---

### 1. ⚠️ eStruxture May 1 — Urgent Status Check (5 min)
Financial impact starts in 9 days. $161K/month savings, $1.9M annualized — this is board-visible.

- Is everything operationally ready for May 1?
- Barrie fully decommissioned? Any loose ends?
- Any network dependencies (check with Ben) that aren't closed?
- Any customer-facing changes that need communication?

This cannot slip. Get a clear "yes, operationally ready" or surface the blocker immediately.

---

### 2. DC Ops Service Description — Two Additions Needed (15 min)
Page: https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045747729/Data+Center+Operations  
Last updated: **Feb 27, 2026 — the day it was created.** George has not edited his own service description.

This is the core accountability conversation: the service description is his contract with the rest of the org. Adam wrote the initial version; George needs to own it. Two additions to make in this session so he leaves with a clear, specific edit to make.

**A. Inventory section — add it**

George owns three dimensions of the org-wide capacity inventory: Space, Power, and Racks. He also owns physical hardware (servers, storage, networking gear) on the shelf. The format that Jorge is building the org-wide model around:

| Dimension | Owned | Sold | Available to Sell |
|---|---|---|---|
| Space | Sellable sqft per DC | Allocated to colo cages + Aptum racks | Immediately leasable without construction |
| Power | kW provisioned per DC | Committed to customers + internal gear | Without new power infrastructure |
| Racks | Racks installed on floor | Sold/filled (colo + hosting) | Available to fill today |
| Hardware (shelf stock) | Servers, drives, PSUs in stock | Deployed to customers | On shelf, ready to deploy |

This matters at an org level: Dave Pistacchio (DigitalBridge) and Ian Rae need this data for Private Cloud UK/US siting decisions. George's team is the primary source for three of the six dimensions. If he doesn't own the Owned/Sold/Available numbers for Space, Power, and Racks, no one does.

Note: his page already has utilization metrics ("rack space utilization: as close to 100%") and CMDB accuracy (0% target). The inventory section complements those — it's not redundant. The utilization metrics answer "how full are we?"; the inventory section answers "what do we have and what can we sell?"

**Action from this session:** George adds an Inventory section to the page with the four-row framework above. Numbers can be TBD placeholders to start — the structure is what matters. **Fri Apr 25.**

**B. Team utilization under "How We Are Measured" — add it**

The current metrics table covers rack/power utilization, PUE, MTTR, IIR issuance, CMDB accuracy, cycle count, and lease runway. What's missing: **how George's people are being used**.

George's team is geographically distributed (8 locations) and does reactive work (hardware remediation, physical tickets) and proactive work (Centrilogic onboarding, DC migrations, capacity projects). The split between these matters:
- Too much reactive = the team is running on dispatched tickets and can't run the migration and onboarding projects that are on the board-level H2 roadmap
- Understanding the balance tells you whether you need more headcount, better triage, or just better tracking

Proposed metric to add: **Technician time allocation — reactive (ticket-dispatched) vs. proactive (project/infrastructure) per period (% of hours)**. Even a rough cut is valuable. Ask George: what does the current split feel like? What would the right target be?

---

### 3. Accountability Check — Capacity Snapshot (10 min)
The capacity snapshot (Space/Power/Racks by location) has been on the list since Mar 31 — nearly four weeks. This is the single most foundational deliverable for George's function. It's also blocking the org-wide inventory model.

Ask directly: what is in the way?
- Is it a data problem (CMDB isn't accurate enough to trust)?
- Is it a tooling problem (Hyperview data isn't accessible in a usable format)?
- Is it a bandwidth problem (he's been running on BAU and projects)?
- Or is it a perception problem (he hasn't prioritized it because it doesn't feel urgent)?

The answer determines the solution. If it's CMDB accuracy, that's an OKR conversation (CMDB discrepancy target is 0% — if the CMDB can't produce this snapshot, that target isn't being met). If it's bandwidth, the conversation is about delegation or sequencing.

**Hard deadline: Fri Apr 25. No further extensions.** Jorge is now building the org-wide inventory pipeline around data from each dimension owner. George's dimensions are three of the six. If he can't provide directional numbers by Friday, the inventory initiative stalls.

---

### 4. Centrilogic Onboarding Status (5 min)
15 UK colo customers, ~C$70K/mo MRC, Q3 target. This has been on the list since Mar 31 with no written status.

- Has migration planning started? Is there a plan?
- Who's running point on George's side?
- What does the onboarding process actually look like for these customers — what does DCO need to do for each one?
- Any risks to the Q3 timeline?

---

### 5. OKR Targets — Quick Status (5 min)
The four board-visible DC OKR targets. Just a pulse check — no deep dive today unless something is off:

- **$680K cost reduction:** eStruxture is the biggest lever ($161K/mo from May 1). Any risk to the number?
- **99.999% uptime:** April so far — any incidents?
- **98% SLA adherence:** Any credits issued or at risk?
- **R&M ↓10%:** Is he tracking this? Where does it stand?

---

### 6. Open Items — Quick Confirm (3 min)
- **UK staffing model:** Own staff vs. contracted remote hands at Portsmouth/Croydon/Horner — still undocumented
- **LA/Malibu coverage:** 551 services, comparable to Atlanta/Miami — adequacy confirmed?

These two have been on the list since Mar 31. If he knows the answers, capture them now. If not, they're carry-forwards with a hard date.

---

## Discussion Notes
<!-- Raw capture — don't over-format in real time, just get it down -->

---

## Decisions & Actions

| Action | Owner | By When |
|--------|-------|---------|
| Confirm eStruxture May 1 operational readiness (verbal in session) | George | Today |
| Add Inventory section to DC Ops page (Space/Power/Racks/Hardware framework) | George | Fri Apr 25 |
| Add team utilization metric to "How We Are Measured" | George | Fri Apr 25 |
| Circulate DC Ops service description to Martin, Ben, Jason for review | George | Fri Apr 25 |
| Deliver first-pass capacity snapshot (space/power/racks by location) | George | Fri Apr 25 |
| Deliver written Centrilogic onboarding plan with timeline | George | Fri Apr 25 |
| Document UK staffing model (own staff vs. contracted) | George | Fri Apr 25 |
| Confirm LA/Malibu local coverage adequacy | George | Fri Apr 25 |
| Provide current status on all 4 DC OKR targets | George | Next 1:1 |
| Update george-revie.md with DC Ops service ownership | Adam | This week |
| | | |

<!-- Inline tracking tasks -->
- [ ] George to add Inventory section to DC Ops page by Fri Apr 25 #tracking [person::george-revie]
- [ ] George to add team utilization metric to "How We Are Measured" by Fri Apr 25 #tracking [person::george-revie]
- [ ] George to circulate DC Ops service description to Martin, Ben, Jason by Fri Apr 25 #tracking [person::george-revie]
- [ ] George to deliver first-pass capacity snapshot (space/power/racks) by Fri Apr 25 #tracking [person::george-revie]
- [ ] George to deliver written Centrilogic onboarding plan by Fri Apr 25 #tracking [person::george-revie]
- [ ] George to document UK staffing model by Fri Apr 25 #tracking [person::george-revie]
- [ ] George to confirm LA/Malibu local coverage adequacy by Fri Apr 25 #tracking [person::george-revie]
- [ ] George to confirm eStruxture May 1 operational readiness #tracking [person::george-revie]
- [ ] Adam to update george-revie.md with DC Ops service ownership #tracking [person::george-revie]

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->
<!-- Watch for: What's his explanation for the page never being touched? Does he engage with the inventory framework immediately — does he know his Space/Power/Rack numbers? Can he confirm eStruxture May 1 readiness confidently, or is there hesitation? Does he have a Centrilogic plan or is it still vague? Is the capacity snapshot a data problem or a prioritization problem — his answer tells you which conversation to have. -->

## Next session focus
<!-- eStruxture May 1 confirmed and activated. Inventory section in the page. Capacity snapshot in hand — use it to populate George's three dimensions of the org-wide inventory model. Centrilogic plan reviewed. DC Ops page circulated and feedback received. UK staffing documented. OKR targets tracked with real numbers. -->
