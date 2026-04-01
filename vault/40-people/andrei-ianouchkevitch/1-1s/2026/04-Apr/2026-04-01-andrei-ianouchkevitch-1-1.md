---
type: 1-1
date: 2026-04-01
person: andrei-ianouchkevitch
---

# 1:1 — Andrei Ianouchkevitch — 2026-04-01

---

## Carry-forward
*Open tracking items for Andrei Ianouchkevitch — updates live as items are completed*

```dataview
TASK FROM "40-people/andrei-ianouchkevitch/1-1s" OR "00-daily" OR "90-meeting-notes"
WHERE !completed AND contains(tags, "#tracking")
  AND (person = "andrei-ianouchkevitch" OR contains(file.path, "40-people/andrei-ianouchkevitch/1-1s"))
SORT file.mtime DESC
```

---

## Their agenda
<!-- What they want to cover — capture before or at start of meeting -->

## My agenda
<!-- Coaching focus, delegation check, capability push for this session -->

### Framing: First Real 1:1 + Vacation Prep
First structured 1:1 with Andrei. He owns Managed Cloud — everything from the OS upward across public cloud, private cloud, and AptCloud. This function is one of the highest-margin products in the portfolio when correctly stated (~+35% vs. the reported -49.8% caused by the Service Desk cost misallocation). This meeting needs to: (1) establish his ownership, (2) align him on the service description review, (3) set focused priorities for the week while I'm out Apr 2–10.

### 1. Board Context (5 min)
Key takeaways relevant to Andrei's world:
- The MCP cost allocation correction (~$466K margin swing) was presented to the board. The 17-of-25 misallocation from Managed Cloud to Service Desk is being fixed. He needs to understand this is now visible at the board level.
- Managed Cloud's corrected margin is ~+35%. That's a strong product. The narrative is "this product is performing; the reporting was wrong."
- AptCloud was presented as Alpha with "team size TBD." The board expects a maturation path.
- H1 operational resilience record was strong — zero SLA credits. That includes his managed environments.

The message: the board sees Managed Cloud as a high-value function. His job is to keep it there and mature AptCloud toward Beta.

### 2. Service Description Review — PARAMOUNT (10 min)
Andrei owns the Managed Cloud service description: https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5044273167/Managed+Cloud

This is the #1 deliverable. Same ask as all service managers: review the description with his team and adjacent stakeholders, then get it approved.

Ask him:
- Has he read the current version? Does it accurately reflect what his team does and doesn't do?
- The boundary with Ben's Network team (the "Juniper CLI vs. portal" test) — does he agree with that delineation?
- The boundary with Jason's Service Desk (L2 ops vs. L3 cloud escalation) — is that working in practice?
- Who needs to review it? (Network/Ben, Service Desk/Jason, Compute Platforms/Martin at minimum)
- Can it be circulated for review by end of week (Fri Apr 4)?

Key flags from the service description to discuss:
1. **Cloud networking boundary:** WAF, DDoS, and hybrid interconnects are his. Physical circuits and routing are Ben's. Is this clear operationally or creating confusion?
2. **AptCloud operational readiness:** Shared-cluster operations require more rigorous change management than dedicated hosting. Is his team ready for that?
3. **Datadog ownership:** Who owns the contract, configuration standards, and integration with the broader monitoring stack? This is an open org question.

### 3. Cost Allocation Correction Status (5 min)
The financial model shows ~17 of 25 people previously allocated to Managed Cloud actually belong to Service Desk (Jason's org). This correction is "in progress."

Ask him:
- Where does this stand? Has the correction been submitted to Finance?
- Is Jason aligned on the 17-person attribution?
- Any blockers on getting this finalized?

This matters because his team's actual size is ~8, not 25. The reported margin flips from -49.8% to +35% when corrected. He needs to be able to articulate this.

### 4. Capacity Framework: Cloud Capacity Dimensions (10 min)
I sent the capacity framework to the team. For Andrei, the relevant dimensions:

**Managed Cloud instances:**
- How many managed environments (VMs, instances) does the team operate today?
- What's the split: public cloud (Azure/AWS/GCP) vs. private cloud (VMware/Proxmox) vs. AptCloud?

**AptCloud capacity:**
- How many shared-cluster nodes are deployed?
- How many tenants can each cluster support?
- What's the available capacity before we need more hardware?

Ask him:
- Can he produce a first-pass view of managed environment count by type?
- Where does this data live? Is it in a tool, or tribal knowledge?
- Target: first draft by Mon Apr 7.

### 5. AptCloud Status Check (5 min)
Quick pulse check on AptCloud (Alpha):
- Where does the platform stand? How many clusters running?
- Has any customer workload been deployed?
- What's the path from Alpha to Beta? What needs to be true?
- Is the operational readiness concern from the service description being addressed?

### 6. Priorities for the Week (5 min)
Three things for the week while I'm out (Apr 2–10, back Apr 13):

1. **Service description:** Review it, circulate for feedback by Fri Apr 4. Get Ben, Jason, and Martin to validate the boundaries.
2. **Cost allocation:** Confirm status with Finance/Jason. Written summary of where the correction stands.
3. **Capacity snapshot first pass:** Managed environment count by type (public/private/AptCloud). Even directional. Target Mon Apr 7.

Additionally:
- **Review your emails, Jira, Slack, Teams, and calendar** for anything you're accountable for that needs attention while I'm out. Update your 1-1 notes with anything flagged.

Everything else continues as BAU. The message: service description is paramount, the rest supports it.

---

## Discussion Notes
<!-- Raw capture — don't over-format in real time, just get it down -->

---

## Decisions & Actions

| Action | Owner | By When |
|--------|-------|---------|
| Review Managed Cloud service description and circulate for feedback | Andrei | Fri Apr 4 |
| Confirm cost allocation correction status with Finance/Jason | Andrei | Fri Apr 4 |
| Produce first-pass capacity snapshot (managed environments by type) | Andrei | Mon Apr 7 |
| Review emails/Jira/Slack/Teams/calendar for open accountabilities | Andrei | Wed Apr 2 |
| Update andrei-ianouchkevitch.md with Managed Cloud service ownership | Adam | Before vacation |
| | | |

<!-- Inline tracking tasks — tag with #tracking so they surface on the hub -->
- [ ] Andrei to review and circulate Managed Cloud service description by Fri Apr 4 #tracking [person::andrei-ianouchkevitch]
- [ ] Andrei to confirm cost allocation correction status by Fri Apr 4 #tracking [person::andrei-ianouchkevitch]
- [ ] Andrei to produce first-pass capacity snapshot (managed environments by type) by Mon Apr 7 #tracking [person::andrei-ianouchkevitch]
- [ ] Andrei to review all channels for open accountabilities by Wed Apr 2 #tracking [person::andrei-ianouchkevitch]
- [ ] Adam to update andrei-ianouchkevitch.md with Managed Cloud service ownership #tracking [person::andrei-ianouchkevitch]

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->
<!-- Watch for: Does he understand the cost allocation issue and can he articulate it? Does he have a handle on AptCloud maturity, or is it vague? How does he react to the service description ask — ownership mindset or compliance mindset? Can he articulate team boundaries without hesitation? -->

## Next session focus
<!-- After vacation: Did the service description get circulated? Did the cost allocation correction land? If the capacity snapshot is good, Andrei can produce structured data on demand. Deep-dive on AptCloud Beta readiness and Datadog ownership decision. -->
