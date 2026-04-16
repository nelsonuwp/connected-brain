---
type: 1-1
date: 2026-04-16
person: martin-tessier
---

# 1:1 — Martin Tessier — 2026-04-16

---

## Carry-forward
*Open tracking items for Martin Tessier — updates live as items are completed*

```dataview
TASK FROM "40-people/martin-tessier/1-1s" OR "00-daily" OR "90-meeting-notes"
WHERE !completed AND contains(tags, "#tracking")
  AND (person = "martin-tessier" OR contains(file.path, "40-people/martin-tessier/1-1s"))
SORT file.mtime DESC
```

**Open items from Apr 1 (all overdue — need status on each):**
- [ ] Review Compute Platforms service description and circulate for feedback (was due Fri Apr 4) #tracking [person::martin-tessier]
- [ ] Produce first-pass compute capacity snapshot by type and location (was due Mon Apr 7) #tracking [person::martin-tessier]
- [ ] Written AptCloud platform status: current state, Beta readiness, needs, timeline (was due Fri Apr 4) #tracking [person::martin-tessier]

**Adam's open items:**
- [ ] Update martin-tessier.md with Compute Platforms service ownership (carried from Apr 1) #tracking [person::martin-tessier]

---

## Their agenda
<!-- What they want to cover — capture before or at start of meeting -->

## My agenda

### Framing: Return from Vacation + Accountability Check + Product Delivery Flow Debrief
First session back (pushed from yesterday). Martin had three deliverables for the window I was out. Need status on all three — honest, specific. He's carrying two major workstreams simultaneously (BAU provisioning + AptCloud build), which creates real capacity tension. I want to understand where the load is actually landing, not just what got done.

**New context from yesterday's meetings:** The [[2026-04-15-product-delivery-flow|Product Delivery Flow]] session with the full team explicitly defined Martin's scope: he delivers compute platform services (hypervisor, storage/SAN, backup infrastructure, OS images) but does NOT own day-2 operations. Jason's team owns all customer-facing support. This was agreed by the group. The backup ownership model was settled: Martin owns the product (provisioning, storage, capacity); Jason owns customer support. Martin needs to know this is now the operating model — not aspirational, but confirmed.

The [[2026-04-15-will-adam-sync|Will/Adam sync]] also pre-aligned on Martin's scope: Compute Platforms = Aptum IaaS + Private Cloud (hypervisor & orchestration layers). NOT bare metal, NOT AptCloud app layer.

### 1. Accountability Check: The Three Deliverables (15 min)
Go through each one. Specifics, not summaries.

**A. Compute Platforms Service Description**
- Reviewed and circulated? To George, Jason, Andrei at minimum?
- Confluence link: https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045518349/Compute+Platform
- Any feedback received? Anything that surprised him or revealed a grey area?
- **New hard deadline if not done: Fri Apr 18.**

**B. Compute Capacity Snapshot**
- First-pass view: servers/hosts by type and location. Dedicated vs. private cloud vs. AptCloud.
- What's in the provisioning queue right now?
- Even a rough cut is fine — this is about establishing a baseline, not perfection.
- If he doesn't have it: what would it take to produce it, and by when?

**C. AptCloud Platform Status Write-Up**
- Where does the platform stand today — cluster count, hardware footprint, customer onboarding status?
- What is actually blocking Beta? Technical, operational, or both?
- Is the shared-cluster change management discipline in place?

### 2. Service Description Review: Compute Platforms-Specific Talking Points (10 min)
Walk through the key flags from the service description:

**The scope boundary with George — is it clean in practice?**
The description is clear: George's team delivers powered, racked, cabled hardware. Martin's team takes over from there (OS, config, monitoring agents, backup agents, handoff). 
- In practice, are there grey areas? Cases where there's confusion about whose job it is?
- Does George's team agree with this framing?

**Direction of travel — automation team, not manual provisioning crew:**
The service description is explicit: Martin's team's value is in the playbooks and standards, not in manual execution. As the environment matures, manual provisioning work should shrink.
- Where is the team today on automation coverage? What percentage of environments are automated end-to-end?
- What's the bottleneck to higher automation coverage?
- Does Martin see his team this way — or are they still primarily executing manual builds?

**Automation tooling ownership (Ansible, Terraform, etc.):**
This is flagged as an open question: who owns the playbook tooling — Compute Platforms, OI, or a future platform engineering function?
- What's Martin's position? He should have a view.
- Is this causing any friction with Jorge's team?

**Metric gaps:**
All metrics in the service description are "To be defined." Start with two:
- Provisioning turnaround time: how long from powered hardware received to handoff completed?
- First-time accuracy: what percentage of builds require rework?
- Even informal tracking is better than nothing. Where would he start?

### 3. VMware P&L Analysis (Apr 13) — Debrief (5 min)
Martin was in the VMware P&L analysis session with Carlton, Jorge, Matthew, Noe, and Sarah.
- What was the headline finding?
- Any implications for Compute Platforms — are VMware environments becoming less commercially viable?
- Does this change how Martin is thinking about the VMware vs. Proxmox vs. AptCloud split going forward?

### 4. Proxmox Pricing — $150/Host Proposal (5 min)
There's a discussion about adding a $150/host charge for Proxmox environments.
- Is this driven by actual cost or is it a commercial positioning decision?
- Does Martin have a view on whether the $150 reflects the real cost of his team's provisioning effort for Proxmox?
- Any implications for AptCloud pricing when it exits Alpha?

### 5. Managed Private Cloud Service Guide — Carlton/Emma Meeting (Today) (5 min)
Martin relayed Adam's approval for service guide revisions. Carlton and Emma are meeting today (Apr 15) to review changes.
- Does Martin need to be involved in or aware of what comes out of that meeting?
- Any changes to the service guide that will affect Compute Platforms scope or standards?

### 6. AptCloud Beta Path — Clarity Check (5 min)
This was a board-level topic. Alpha on excess server inventory is a good start. But the board expects a maturation path.
- What specifically needs to be true before AptCloud can be called Beta-ready?
- Is it a technical threshold (stability, uptime, cluster coverage)?
- Is it an operational threshold (documented runbooks, change management process, Service Desk trained)?
- Is it a headcount/capacity question?
- Does Martin feel adequately staffed to run both BAU provisioning AND AptCloud build in parallel?

### 7. Priorities Going Forward (5 min)
1. **Service description:** Circulated and feedback collected. Deadline Fri Apr 18.
2. **Capacity snapshot:** Baseline view of compute by type and location. This week.
3. **AptCloud Beta criteria:** Give me a concrete list of what "Beta-ready" means. Not a date — a criteria list. That becomes the plan.
4. **Metrics baseline:** Pick one metric (provisioning turnaround time) and start tracking it informally. Even a spreadsheet is fine.

---

## Discussion Notes
<!-- Raw capture — don't over-format in real time, just get it down -->

---

## Decisions & Actions

| Action | Owner | By When |
|--------|-------|---------|
| Circulate Compute Platforms service description (if not yet done) | Martin | Fri Apr 18 |
| Deliver first-pass compute capacity snapshot (if not yet done) | Martin | Fri Apr 18 |
| Define AptCloud Beta readiness criteria (concrete list) | Martin | Next 1:1 |
| Start informal tracking of provisioning turnaround time | Martin | Ongoing |
| Update martin-tessier.md with Compute Platforms service ownership | Adam | This week |
| | | |

<!-- Inline tracking tasks -->
- [ ] Martin to circulate Compute Platforms service description by Fri Apr 18 #tracking [person::martin-tessier]
- [ ] Martin to deliver first-pass compute capacity snapshot #tracking [person::martin-tessier]
- [ ] Martin to produce AptCloud Beta readiness criteria list #tracking [person::martin-tessier]
- [ ] Adam to update martin-tessier.md with Compute Platforms service ownership #tracking [person::martin-tessier]

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->
<!-- Watch for: Does he see his team as an automation/standards function, or are they still a manual provisioning crew? Can he articulate what's blocking AptCloud Beta without hedging? Does he have a position on the automation tooling ownership question, or does he wait for someone else to decide? How does he talk about the dual workload — does he flag capacity tension proactively, or does he absorb it silently? -->

## Next session focus
<!-- Service description feedback reviewed. Capacity snapshot in hand — use it to start a proper capacity framework view. Dig into AptCloud Beta criteria list. Start the provisioning metrics baseline. Resolve automation tooling ownership question (with Jorge). -->
