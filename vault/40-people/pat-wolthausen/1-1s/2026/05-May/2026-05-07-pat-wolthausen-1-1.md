---
type: 1-1
date: 2026-05-07
person: pat-wolthausen
---

# 1:1 — Pat Wolthausen — 2026-05-07

---

## Carry-forward
*Open tracking items for Pat Wolthausen — updates live as items are completed*

```dataview
TASK FROM "40-people/pat-wolthausen/1-1s" OR "00-daily" OR "90-meeting-notes"
WHERE !completed AND contains(tags, "#tracking")
  AND (person = "pat-wolthausen" OR contains(file.path, "40-people/pat-wolthausen/1-1s"))
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
<!-- Example: - [ ] Jorge to update BI report filter by Friday #tracking [person::pat-wolthausen] -->

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->

## Next session focus
<!-- One sentence on what to prioritize next time -->

---

## 1-1 Outline — 2026-05-07

### 1. Ian transition + Jeremy intro
- "Want to start with yesterday's announcement — Ian leaving and Jeremy joining. How are you sitting with it?" *(Note: HSA service guide already shows previous SM Ian Crosby deactivated — this transition has been quietly underway in the data.)*
- "I did a deep dive with Jeremy on PS and HSA these last two days — anything you want me to circle back and re-emphasize?"
- "How is the PS contributing-team model holding up with the leadership change in flight?"

### 2. Their open items waiting on me
- **CPQ ownership — get Pat's feedback from our pre-1-1 call.** Pat is going to end up owning CPQ. Carter currently thinks he owns it; Tom actually owns it. We need to drive the transition. Open with "what landed for you on the call this morning?" and treat that as the agenda for the rest of the conversation. *Source: Adam pre-1-1 nuance + Confluence "HSA" closing notes ("Need to clearly define what is a CPQ request Vs Jira request — ALL GSE and CPQ requests must go through HSA team").*
- **Andy P scope concern (Darren's customer).** Pat flagged 2026-05-05 that Andy P's scope sheet has scope-creep risk; customer was "ready to sign Friday." Need a call: ship as-is or tighten. *Source: Slack #cloud-platform-pm 2026-05-05, [permalink](https://aptum.slack.com/archives/C054X8DKQ3G/p1778011101051209).*
- **PS Direct Labor Contradiction.** Service guide flags $485K of YTD direct labor in PS column despite "no dedicated headcount" model — needs reconciliation with Finance / cost-allocation model. *Source: Confluence "Professional Services" Identified Issues.*
- **PS Partner Services overrun.** $16K actual vs. $2K budget — service guide asks "Are 3rd-party contractors filling gaps because home-team SMs are rejecting internal resource requests?" Decision/visibility needed from me. *Source: Confluence "Professional Services" Identified Issues.*
- **PS vs. HSDM accountability overlap.** Service guide flags PS accountabilities heavily overlap with HSDM — needs me to ratify whether PS is a standalone function or financial/product category under HSDM. *Source: Confluence "Professional Services" Identified Issues.*

### 3. Service health snapshot

**Professional Services (Live):**
- ~$738K YTD F26 revenue; 29.2% gross margin (one of higher-margin segments).
- Direct cost contradiction (no dedicated HC vs. $485K direct labor in column) still unresolved.
- Most measurement metrics still TBD.

**Hybrid Solution Architecture (Live):**
- 4 people (Pat + 3 architects), labor-only cost stack.
- ≥80% sales-support utilization target; ≥50% billable utilization target.
- Currently active in heavy customer-facing terraform / Azure DevOps work (Triton/Polaris) — Pat hands-on through the dev/UAT/prod change cycle 2026-05-06.
- Service guide explicitly calls out "ALL GSE and CPQ requests must go through HSA team" — this is the on-ramp for the CPQ scope landing on Pat.

### 4. Strategic OKR input
*Not applicable — Pat is not on the strategic OKR list.* (HSA's billable-utilization and SOW estimate-accuracy targets are functional, not strategic OKRs.)

### 5. Questions I should ask
- "After the CPQ call this morning — does Tom understand the transition is happening, and is Carter going to fight it?"
- "On Triton/Polaris — is the change-management plan you're building with Ajai something we can lift into a template, or is it customer-specific?"
- "How is the team taking the Ian news — especially given HSA had Ian Crosby in the org structure recently?"
- "Of the three flagged accountability items (PS vs. HSDM overlap, the $485K labor contradiction, partner services overrun), which one would you most like me to clear first?"

### 6. Items I owe Pat
- Drive the CPQ ownership transition with Tom and Carter so Pat actually has the scope.
- Decision on the Andy P scope (loop with Andrei + Lacie).
- Resolve the PS direct-labor contradiction with Finance.
- Visibility on the partner-services overrun root cause (rejected internal resource requests?).
- Ratify or refactor the PS-vs-HSDM accountability boundary.
