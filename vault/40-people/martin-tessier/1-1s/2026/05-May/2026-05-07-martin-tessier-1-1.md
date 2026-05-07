---
type: 1-1
date: 2026-05-07
person: martin-tessier
---

# 1:1 — Martin Tessier — 2026-05-07

---

## Carry-forward
*Open tracking items for Martin Tessier — updates live as items are completed*

```dataview
TASK FROM "40-people/martin-tessier/1-1s" OR "00-daily" OR "90-meeting-notes"
WHERE !completed AND contains(tags, "#tracking")
  AND (person = "martin-tessier" OR contains(file.path, "40-people/martin-tessier/1-1s"))
SORT file.mtime DESC
```

---

## Their agenda
<!-- What they want to cover — capture before or at start of meeting -->

## My agenda
<!-- Coaching focus, delegation check, capability push for this session -->

---

## Discussion Notes
<!-- Raw capture — don't over-format in real time, just get it down -->

---

## Decisions & Actions

| Action | Owner | By When |
|--------|-------|---------|
| | | |

<!-- Inline tracking tasks — tag with #tracking so they surface on the hub -->
<!-- Example: - [ ] Jorge to update BI report filter by Friday #tracking [person::martin-tessier] -->

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->

## Next session focus
<!-- One sentence on what to prioritize next time -->

---

## 1-1 Outline — 2026-05-07

### 1. Ian transition + Jeremy intro
- "Want to start with yesterday's announcement — Ian leaving, Jeremy joining. How are you sitting with it?"
- "I did a deep dive with Jeremy on Compute Platform these last two days, and especially Aptum IaaS — anything you want me to circle back and re-emphasize?"
- "Heads up — Jeremy is going to want your input on the strategic OKRs early, and Aptum IaaS is the obvious one. Want to set that expectation now so you can start lining up your thinking."

### 2. Their open items waiting on me
- **Aptum IaaS structured plan — top of my list.** I need an actual plan from Martin, not bullets: when does development "done" mean done, when does it transition to sustaining, what does the product roadmap look like beyond that. Aim to leave today with a commitment on the plan deliverable. *Source: Adam pre-1-1 nuance + Confluence "Compute Platform" Aptum IaaS Specifics + Open Questions.*
- **Aptum IaaS Day-2 ops transition to Jason's Customer Care team.** Per the service guide today, post-handoff Day-2 sits with Service Desk (basic) and Managed Cloud (platform layer). I need Martin to formally hand the day-2 ops of those servers to Jason — and we need a date. *Source: Adam pre-1-1 nuance + Confluence "Compute Platform" Aptum IaaS Specifics.*
- **Sellable Aptum IaaS sizing.** I need Martin to categorize how much capacity we could actually sell — inventory model on the excess server fleet. Today the service guide says "Aptum-owned excess server inventory" with no sizing. *Source: Adam pre-1-1 nuance + Confluence "Compute Platform" Aptum IaaS Specifics.*
- **Broadcom / VMware renewal — risk identification.** Martin flagged 2026-04-24 to Jorge that Broadcom is introducing additional partner-program changes; renewal is one year out and we need options + risks documented. *Source: email "Re: VMWARE" 2026-04-24 from Martin to Jorge.*
- **Automation tooling ownership.** Service guide flags Ansible/Terraform/equivalent ownership as "open question" — Compute Platforms vs. OI vs. future platform engineering. Decision sits with me. *Source: Confluence "Compute Platform" Open Questions.*

### 3. Service health snapshot
- **Aptum IaaS still Alpha** — being prototyped on existing hardware, building toward Beta. Shared-cluster ops require change-management discipline they don't have today.
- Hosting revenue ~$4M/month, 30-35% margin on third-party license resale.
- Provisioning measurement is mostly TBD (accuracy, turnaround, validation pass rate, L3 escalation response, AptCloud cluster availability).
- Service guide last modified 2026-04-10 — ~4 weeks old, may be stale on IaaS progress.
- ESL Sync (May 4) and Product Deep Dive (Apr 29) recently attended.

### 4. Strategic OKR input *(strategic OKR contributor)*
- "If Jeremy asks 'what's the FY27 Aptum IaaS OKR', what's the answer? Beta exit + sellable capacity, or operational readiness + first revenue, or both? What's the milestone you'd actually commit to?"
- "Outside IaaS — is provisioning automation maturity (config validation pass rate, build time per environment) a 'real' OKR for the team, or is it sub-objective level?"

### 5. Questions I should ask
- "How is the team taking the Ian news?"
- "Where do you actually need investment most — IaaS Beta, automation tooling, or the Broadcom hedge?"
- "What's the realistic earliest date you'd be comfortable handing day-2 of the IaaS servers to Jason?"
- "When you look at the excess server inventory — what's the rough sellable capacity number we should be talking about with Commercial?"

### 6. Items I owe Martin
- Drive the automation tooling ownership decision.
- Backstop on the Broadcom/VMware renewal options work.
- Help him land the IaaS day-2 transition with Jason (be the broker if needed).
- Direction on the right OKR shape for Aptum IaaS so he can plan to it.
