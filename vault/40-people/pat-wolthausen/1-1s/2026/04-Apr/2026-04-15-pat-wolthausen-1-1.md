---
type: 1-1
date: 2026-04-15
person: pat-wolthausen
---

# 1:1 — Pat Wolthausen — 2026-04-15

---

## Carry-forward
*Open tracking items for Pat Wolthausen — updates live as items are completed*

```dataview
TASK FROM "40-people/pat-wolthausen/1-1s" OR "00-daily" OR "90-meeting-notes"
WHERE !completed AND contains(tags, "#tracking")
  AND (person = "pat-wolthausen" OR contains(file.path, "40-people/pat-wolthausen/1-1s"))
SORT file.mtime DESC
```

**Open items from Apr 1 (all overdue — need status on each):**
- [ ] Review HSA service description and circulate for feedback (was due Fri Apr 4) #tracking [person::pat-wolthausen]
- [ ] Produce utilization report — billable/non-billable per person (was due Mon Apr 7) #tracking [person::pat-wolthausen]
- [ ] Provide estimate-to-actual variance on last 3 completed projects (was due Mon Apr 7) #tracking [person::pat-wolthausen]
- [ ] Document active pre-sales pipeline status (was due Fri Apr 4) #tracking [person::pat-wolthausen]

**Adam's open items:**
- [ ] Update pat-wolthausen.md with HSA service ownership (carried from Apr 1) #tracking [person::pat-wolthausen]

---

## Their agenda
<!-- What they want to cover — capture before or at start of meeting -->

## My agenda

### Framing: Return from Vacation + Accountability Check
First session back. Pat had four deliverables for the vacation window. I need honest answers on each: done, partially done, or not started — and why. The pattern here will tell me whether Pat is operating as a function owner who manages his own output, or still functioning as a senior IC who needs external structure.

### 1. Accountability Check: The Four Deliverables (15 min)
Go through each one. Don't accept "mostly done" — get specifics.

**A. HSA Service Description**
- Reviewed and circulated? To whom? Any feedback received?
- Confluence link: https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045747720/Hybrid+Solution+Architecture
- This is the accountability contract for his function. If it hasn't been circulated to Lacie and Fred's team at minimum, it hasn't happened.
- **New hard deadline if not done: Fri Apr 18.**

**B. Utilization Report**
- Does he know his team's current billable vs. non-billable split?
- Per person: who is above 50%? Who is below?
- If he doesn't have this number off the top of his head, that's the first signal. A function owner knows their utilization.

**C. Estimate-to-Actual Variance**
- Last 3 completed projects: how did hours land vs. estimate?
- If variance is high, what was the driver — scope creep, under-estimation, rework?
- This is the core metric for HSA quality. If he hasn't looked, it's a gap.

**D. Pipeline Status**
- Active pre-sales pursuits right now: what are they, what stage, what's needed from Pat?
- Any pursuits that need a decision or escalation?

### 2. DGI Travel (GSE-270) — Today (5 min)
RFP was due Apr 8. F2F presentation is **today** (Apr 15).
- Was HSA involved in the RFP build?
- What's Pat's role in today's presentation?
- What's the deal size and how confident is the team?

### 3. Service Description Review: HSA-Specific Talking Points (10 min)
Whether or not it was circulated, walk through the key open questions:

**The two operating modes — is the split clean?**
The description separates pre-sales (non-billable, cost of sale) from delivery (billable, on the SOW). In practice:
- Is Pat tracking this split per person?
- Are his architects being pulled into delivery without being named on the SOW (untracked billable)?
- Are they doing pre-sales work for deals that never close — and how much time is that?

**Budget ownership — HSA owns the hours, HSDM adds PM overhead:**
- Is this actually how it works, or does Lacie's team push back on HSA estimates?
- Has there been scope creep where HSDM is influencing the technical hours?
- Does Pat feel he truly owns the accuracy of the budget, or does he hand it off and lose control?

**"Nothing gets sold that cannot be delivered":**
- Is HSA actually getting sign-off gates before deals close, or does Commercial sometimes commit without HSA validation?
- Any recent examples where a deal was sold that HSA then had to scramble to deliver?

**Metric gaps:**
Every metric in the HSA service description is "To be defined." Which one does Pat want to own first?
- Billable utilization is the obvious one — does he have a way to track it today?
- Estimate accuracy (budget vs. actual) is the quality signal — even one data point from a recent project is a start.

### 4. CloudOps On-Premise Discussion (Apr 13) — Quick Debrief (5 min)
Pat was in the CloudOps on-premise discussion with Alain and Will (Apr 13). 
- What came out of it?
- Any implications for HSA scope or pre-sales positioning?
- Does this create work for his team?

### 5. VMware and Proxmox Pricing (5 min)
There are active discussions on VMware P&L analysis and a Proxmox host pricing proposal ($150/host charge).
- Is HSA involved in the pricing decisions? Should they be?
- How do these pricing changes affect solution design — will architects need to change how they scope VMware vs. Proxmox environments?

### 6. Priorities Going Forward (5 min)
1. **Service description:** Circulated and feedback collected. Deadline Fri Apr 18.
2. **Utilization tracking:** Pat should have a live view of billable vs. non-billable. If he doesn't have a mechanism, we build one together.
3. **Pipeline discipline:** Weekly visibility on active pre-sales. Not a formal report — just Pat knowing it and being able to tell me in 60 seconds.

---

## Discussion Notes
<!-- Raw capture — don't over-format in real time, just get it down -->

---

## Decisions & Actions

| Action | Owner | By When |
|--------|-------|---------|
| Circulate HSA service description for review (if not yet done) | Pat | Fri Apr 18 |
| Deliver utilization report — billable/non-billable per person | Pat | This week |
| Provide estimate-to-actual variance on last 3 projects | Pat | This week |
| Update pat-wolthausen.md with HSA service ownership | Adam | This week |
| | | |

<!-- Inline tracking tasks -->
- [ ] Pat to circulate HSA service description for review by Fri Apr 18 #tracking [person::pat-wolthausen]
- [ ] Pat to deliver utilization report (billable/non-billable per person) #tracking [person::pat-wolthausen]
- [ ] Pat to deliver estimate-to-actual variance on last 3 projects #tracking [person::pat-wolthausen]
- [ ] Adam to update pat-wolthausen.md with HSA service ownership #tracking [person::pat-wolthausen]

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->
<!-- Watch for: Can he quote utilization off the top of his head? Does he own estimate quality, or does he point to scope creep? Does he see himself as a function owner or a senior architect with reports? How does he talk about the CloudOps discussion — is he thinking about HSA's strategic positioning, or just responding to what's in front of him? -->

## Next session focus
<!-- Service description feedback reviewed and incorporated. Utilization tracking mechanism in place. Estimate variance baseline established. If CloudOps on-premise has implications for pre-sales positioning, dig into that. -->
