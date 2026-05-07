---
type: 1-1
date: 2026-05-07
person: andrei-ianouchkevitch
---

# 1:1 — Andrei Ianouchkevitch — 2026-05-07

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

---

## Discussion Notes
<!-- Raw capture — don't over-format in real time, just get it down -->

---

## Decisions & Actions

| Action | Owner | By When |
|--------|-------|---------|
| | | |

<!-- Inline tracking tasks — tag with #tracking so they surface on the hub -->
<!-- Example: - [ ] Jorge to update BI report filter by Friday #tracking [person::andrei-ianouchkevitch] -->

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->

## Next session focus
<!-- One sentence on what to prioritize next time -->

---

## 1-1 Outline — 2026-05-07

### 1. Ian transition + Jeremy intro
- "Want to start with yesterday's announcement — Ian leaving and Jeremy joining. How are you sitting with it?"
- "I did a deep dive with Jeremy on Managed Cloud these last two days — is there anything you want me to circle back and re-emphasize?"
- "How's the team taking the Ian news? Anything you want me to address with them directly?"

### 2. Their open items waiting on me
- **ClearD/Costco Netscaler exit — commercial change order needed.** ClearD dropping Netscalers, Marcus stood up two nginx instances; need to remove Netscaler from contract and add the two nginx (plus possible 3 DR endpoints) to Managed Cloud contract. Steve Rioux + Barb working it; needs commercial sign-off. *Source: Slack #cleard-internal 2026-04-30, [permalink](https://aptum.slack.com/archives/G012ZCUTXT8/p1777558260641079).*
- **Cost-center reallocation (17 HC out of MC → Customer Care).** Service guide flags this as in flight; the corrected GM picture (-49.8% → +35%) only lands when allocation is fixed. Confirm what's blocked on me. *Source: Confluence "Managed Cloud" Financial Model section.*
- **Datadog tooling ownership.** Service guide flags ownership of the Datadog contract / config standards / integration as an "open org question" — that decision sits with me. *Source: Confluence "Managed Cloud" Open Questions / Tooling Ownership.*
- **AptCloud growth investment ahead of Beta.** Service guide states clearly: "Growth investment should happen before Beta — not after the first incident." Need a sizing conversation. *Source: Confluence "Managed Cloud" Open Questions.*
- **Andy P quote / scope review (the customer Darren is chasing).** Andy P scoped, Pat is uncomfortable with scope creep, customer "ready to sign Friday." Need to call shot on whether to push out a cleaner scope or accept and ship. *Source: Slack #cloud-platform-pm 2026-05-05, [permalink](https://aptum.slack.com/archives/C054X8DKQ3G/p1778010780565319).*

### 3. Service health snapshot
- **Live customer crisis — ClearD Netscaler/Citrix:** Apr 30 Citrix support crisis on the ClearD/Costco Netscalers; Marcus migrated production traffic to nginx same day. Andrei flagged Citrix support as effectively non-existent (had to use Ian's old contact to even reach them). *Source: Slack #cleard-internal thread 2026-04-30.*
- **Hypertec/Canderel backup retirement** — emergency meeting 2026-05-04 with Taha + Barb to discuss backups Hypertec retired and next steps before relaying to customer. *Source: Slack #canderel-internal-cloudops 2026-05-04.*
- **Team thin** — 8 people carrying public cloud, private cloud, AptCloud build, and cloud networking; service guide flags AptCloud build will cannibalize BAU without more headcount.
- **Utilization** ~74% cloud operator hours, ~64% allocated; service guide notes 160hr/m incoming headcount.
- **AptCloud (CloudStack)** still Alpha; operational readiness gating Beta.

### 4. Strategic OKR input
*Not applicable — Andrei is not flagged as a strategic OKR contributor.*

### 5. Questions I should ask
- "How is the team taking the Ian news? Anything I should address directly?"
- "Where do you actually need headcount most — AptCloud build, BAU coverage, or platform layer (K8s/Kafka)?"
- "If we got the Datadog ownership decision tomorrow, what would you want it to land?"
- "What's the realistic path to AptCloud Beta — and what would have to be true for you to feel ops-ready?"
- "On the Citrix support situation — anything we should escalate up the vendor management chain?"

### 6. Items I owe Andrei
- Drive the cost-center reallocation through Finance.
- Sign off / direction on the ClearD Netscaler → nginx contract change.
- Decision on Datadog tooling ownership.
- Direction on AptCloud pre-Beta investment sizing.
- Backstop on Andy P scope (loop with Pat).
