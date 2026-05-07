---
type: 1-1
date: 2026-05-07
person: george-revie
---

# 1:1 — George Revie — 2026-05-07

---

## Carry-forward
*Open tracking items for George Revie — updates live as items are completed*

```dataview
TASK FROM "40-people/george-revie/1-1s" OR "00-daily" OR "90-meeting-notes"
WHERE !completed AND contains(tags, "#tracking")
  AND (person = "george-revie" OR contains(file.path, "40-people/george-revie/1-1s"))
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
<!-- Example: - [ ] Jorge to update BI report filter by Friday #tracking [person::george-revie] -->

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->

## Next session focus
<!-- One sentence on what to prioritize next time -->

---

## 1-1 Outline — 2026-05-07

### 1. Ian transition + Jeremy intro
- "Want to start with yesterday's announcement — Ian leaving, Jeremy joining. How are you sitting with it?"
- "I did a deep dive with Jeremy on DC Ops these last two days — anything you want me to circle back and re-emphasize?"
- "Heads up — Jeremy is going to want your input on the strategic OKRs early. Want to set that expectation now."

- [ ] "The sooner we  get direction the better" - george on Jeremy. "company wide" - put together something that says here's our direction. What are we doing with Managed Hosting, Colo, Data Centers, everything. 
- [ ] Enhance customer experience by getting an n+1 superserver 
- [ ] 7/24 in Herdon - Basis/Illumin (no flexiblity of remote hands there because it's our own DC)
### 2. Their open items waiting on me
- **eStruxture migration approval — APTUM-38811.** George forwarded 2026-05-06: "I am looking to approve the migrations below. These are required to achieve our eStruxture agreement. Please let me know your thoughts." Direct ask sitting in my inbox. *Source: email "Fw: Aptum Managed Services (Canada) Inc.: Follow-Up on Required Server Migration (Ticket: APTUM-38811)" 2026-05-06.*
- **Megaport On-Ramp — utility feed economics.** Marc Alex pushing the opportunity; George replied 2026-05-05 that the upgrade is technically possible but would require a new utility feed and the economics are "certainly a challenge." Needs my take on whether to push commercial harder or table it. *Source: email "Re: Connecting your customers via Megaport On Ramp as a Service" 2026-05-05.*
- **PUE target definition.** Service guide marks PUE as "to be defined" — direct margin lever, can't OKR it without setting the line. *Source: Confluence "Data Center Operations" SLA table.*
- **MTTR for physical incidents.** Also "to be defined" in service guide — ditto. *Source: Confluence "Data Center Operations" SLA table.*
- **UK and LA/Malibu local coverage audit.** Service guide explicitly flags UK (~1,091 services) and LA/Malibu (~551 services) as needing explicit local-coverage clarity vs. third-party remote hands. *Source: Confluence "Data Center Operations" Open Questions.*

### 3. Service health snapshot
- ~768 direct colo services + facility layer for the rest of the estate (~5,491 total across all sites).
- Largest non-labor cost in the org sits here (lease + power + cooling).
- Centrilogic divestiture — George handed commercial conversation to Marc Alex on 2026-05-05.
- Hyperview Review (Apr 29) — DCIM tooling activity, ongoing.
- COE meeting accepted 2026-05-06.

### 4. Strategic OKR input *(strategic OKR contributor)*
- "If Jeremy asks 'what's the single biggest DC Ops OKR for FY27', is it utilization (rack + power), PUE definition + improvement, or CMDB accuracy? Which has the best margin / risk lever?"
- "Lease runway tracking is in the SLA table but not as a hard OKR — should that move up given how concentrated our spend is in 3rd-party DCs?"

### 5. Questions I should ask
- "How is the team taking the Ian news? Anyone on flight risk, particularly in the UK or Toronto?"
- "On UK and LA — do we actually have the local hands we need, or are we one outage away from finding out we don't?"
- "What's your single biggest worry on lease runway in the next 18 months?"
- "If I cleared one decision off your desk in the next two weeks, what would it be?"

### 6. Items I owe George
- Decision on the eStruxture/APTUM-38811 migration approval.
- Direction on the Megaport On-Ramp — pursue with new utility feed, or pass.
- Set the PUE target with him so we can put it into an OKR.
- Set MTTR target for physical incidents.
