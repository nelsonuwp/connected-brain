---
type: 1-1
date: 2026-05-07
person: jorge-quintero
---

# 1:1 — Jorge Quintero — 2026-05-07

---

## Carry-forward
*Open tracking items for Jorge Quintero — updates live as items are completed*

```dataview
TASK FROM "40-people/jorge-quintero/1-1s" OR "00-daily" OR "90-meeting-notes"
WHERE !completed AND contains(tags, "#tracking")
  AND (person = "jorge-quintero" OR contains(file.path, "40-people/jorge-quintero/1-1s"))
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
<!-- Example: - [ ] Jorge to update BI report filter by Friday #tracking [person::jorge-quintero] -->

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->

## Next session focus
<!-- One sentence on what to prioritize next time -->

---

## 1-1 Outline — 2026-05-07

### 1. Ian transition + Jeremy intro
- "Want to start with yesterday's announcement — Ian leaving and Jeremy joining. How are you sitting with it?"
- "I did a deep dive with Jeremy on Operations Intelligence these last two days — anything you want me to circle back and re-emphasize?"
- "Jeremy is going to lean on OI heavily for visibility — anything you want me to set him up to expect?"

### 2. Their open items waiting on me
- **Two-Zabbix consolidation decision (VP mandate).** Service guide is explicit: "The decision is not Jorge's to make" — it requires a VP-level mandate to override Ben/Andrei/Jason's tool preferences. I owe him this. *Source: Confluence "Operations Intelligence" Two-Zabbix Problem section.*
- **Broader tooling ownership decision.** JSM, Zabbix internal, Zabbix customer-facing, Datadog, LogicMonitor, Ansible — service guide proposes IT-platform / OI-stack-decisions / each-team-config split. I need to ratify or counter. *Source: Confluence "Operations Intelligence" Tooling Ownership section.*
- **Discovery → Alpha acceleration.** Service guide flags this as the "highest-leverage investment in the org at this stage." Needs team-size approval and a defined exit-from-Discovery date. *Source: Confluence "Operations Intelligence" Open Questions.*
- **VMWARE SKU repricing program.** Jorge laid out a 4-step process to put every customer on the VMWARE SKU at correct cost — and is manually tracking contract length + expiration per service ID. He needs the cost-source automated, and a sign-off to act on the price reductions. *Source: email "Re: VMWARE" 2026-04-24 and 2026-04-23.*
- **CEM dependency** — service guide states CEM cannot operate without OI being operational first. If we're committing to CEM, OI sequencing matters. *Source: Confluence "Operations Intelligence" Open Questions.*

### 3. Service health snapshot
- **Lifecycle: Discovery** — service guide last updated 2026-04-09, ~4 weeks old. Worth refreshing.
- Already delivered the MCP cost-allocation correction (~$466K margin swing) — concrete proof of value.
- Pure cost center, value indirect; current measures of success all "to be defined."
- Manual tracking still present in critical workflows (VMWARE service IDs, contract expiry).

### 4. Strategic OKR input
*Not applicable — Jorge is not on the strategic OKR list.* Worth noting OI is the data substrate for everyone else's OKRs, so plumbing matters.

### 5. Questions I should ask
- "How is the team taking the Ian news?"
- "If I gave you a structured plan today — sequenced milestones, team size, exit-from-Discovery date — what would unlock first?"
- "Of all the irons in the fire (Zabbix, tooling ownership, VMWARE pricing, CEM data layer, dashboards) which two should I clear out of your way first?"
- "What's the one piece of operational data nobody else realizes is fragile, that's going to bite us if we don't fix it?"

### 6. Items I owe Jorge — *priority commitment for me this session*
- **A structured OI plan with him.** He's got too many balls in the air without a sequenced roadmap; commit to a working session this week to land: Discovery exit criteria, team size, milestone calendar, and which "ball" gets dropped on purpose vs. picked up.
- VP mandate on the two-Zabbix consolidation.
- Decision on broader tooling ownership model.
- Sign-off path on the VMWARE SKU repricing.
