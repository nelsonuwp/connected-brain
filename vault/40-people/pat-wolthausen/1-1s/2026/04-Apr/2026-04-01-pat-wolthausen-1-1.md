---
type: 1-1
date: 2026-04-01
person: pat-wolthausen
---

# 1:1 — Pat Wolthausen — 2026-04-01

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

### Framing: First Real 1:1 + Vacation Prep
First structured 1:1 with Pat. He owns Hybrid Solution Architecture (HSA) — the team that defines the technical scope and budget inside every SOW. Four people total (Pat + Rob, Marcus, Andy). They operate in two modes: pre-sales (designing solutions with Commercial) and delivery (billable architecture on PS engagements). The target is ≥50% billable utilization. This meeting needs to: (1) establish ownership, (2) align on service description review, (3) understand current utilization and pipeline, and (4) set focused priorities for the week while I'm out.

### 1. Board Context (5 min)
Key takeaways relevant to Pat's world:
- PS revenue and delivery quality were board topics. HSA's estimates directly drive PS margin (~29.2%).
- Every hour below 50% billable utilization is a direct margin drag. The board sees PS as a growth lever.
- Pre-sales win rate matters — solutions designed but not closed are sunk cost.
- DGI Travel RFP (GSE-270) is due Apr 8 with F2F presentation Apr 16. This is active pipeline that may involve HSA.

The message: the board cares about PS profitability. Your estimates are the foundation of that.

### 2. Service Description Review — PARAMOUNT (10 min)
Pat owns the HSA service description: https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045747720/Hybrid+Solution+Architecture

This is the #1 deliverable. Same ask as all service managers.

Ask him:
- Has he read the current version? Does it accurately reflect what his team does and doesn't do?
- The two operating modes (pre-sales vs. delivery) — is this how they actually work, or is the split muddier?
- Budget ownership inside SOWs — does he feel he truly owns the hours, or does HSDM override?
- Who needs to review it? (HSDM/Lacie, Commercial/Fred's team, Managed Cloud/Andrei at minimum)
- Can it be circulated for review by end of week (Fri Apr 4)?

Key flags from the service description:
1. **HSA owns the hours; HSDM adds PM overhead on top.** Is this division clean? Or is there scope creep where HSDM is influencing the technical estimate?
2. **Pre-sales time is non-billable overhead.** How much time is the team spending in pre-sales mode vs. delivery mode?
3. **Technical feasibility validation:** "Nothing gets sold that cannot be delivered." Is this actually happening, or are deals getting committed without HSA sign-off?

### 3. Utilization and Pipeline Check (10 min)
This is the financial health check for his function.

Ask him:
- What's the team's current billable utilization? Is it above or below 50%?
- How many active engagements is the team on right now?
- How many pre-sales pursuits are in flight?
- What's the estimate-to-actual variance looking like on recent projects? Are estimates holding, or are projects running over?
- Any SOWs in flight that he's concerned about (scope creep, technical risk)?

If utilization is below 50%, the question is whether it's a pipeline problem (not enough work) or an allocation problem (too much pre-sales, not enough delivery).

### 4. Active Engagements: Quick Pulse (5 min)
Check in on anything active:
- **DGI Travel (GSE-270):** RFP due Apr 8, F2F Apr 16. Is HSA involved? What's Pat's role?
- **Apt Cloud (GSE-155) / Ignite Migration (GSE-247):** Are any of his architects on these?
- **Any other active SOWs** where Pat or his team are the named architect?

For anything not on fire: "keep doing what you're doing, we'll deep-dive next session."

### 5. Priorities for the Week (5 min)
Three things for the week while I'm out (Apr 2–10, back Apr 13):

1. **Service description:** Review it, circulate for feedback by Fri Apr 4. Get Lacie and Fred's team to validate the SOW/scope boundaries.
2. **Utilization report:** Current billable vs. non-billable split for each team member. Estimate-to-actual variance on last 3 completed projects. By Mon Apr 7.
3. **Pipeline status:** Active pre-sales pursuits and their status. Any that need escalation or decision while I'm out.

Additionally:
- **Review your emails, Jira, Slack, Teams, and calendar** for anything you're accountable for that needs attention while I'm out. Update your 1-1 notes with anything flagged.

Everything else continues as BAU.

---

## Discussion Notes
<!-- Raw capture — don't over-format in real time, just get it down -->

---

## Decisions & Actions

| Action | Owner | By When |
|--------|-------|---------|
| Review HSA service description and circulate for feedback | Pat | Fri Apr 4 |
| Produce utilization report (billable vs. non-billable per person) | Pat | Mon Apr 7 |
| Provide estimate-to-actual variance on last 3 completed projects | Pat | Mon Apr 7 |
| Pipeline status: active pre-sales pursuits and decisions needed | Pat | Fri Apr 4 |
| Review emails/Jira/Slack/Teams/calendar for open accountabilities | Pat | Wed Apr 2 |
| Update pat-wolthausen.md with HSA service ownership | Adam | Before vacation |
| | | |

<!-- Inline tracking tasks — tag with #tracking so they surface on the hub -->
- [ ] Pat to review and circulate HSA service description by Fri Apr 4 #tracking [person::pat-wolthausen]
- [ ] Pat to produce utilization report (billable/non-billable per person) by Mon Apr 7 #tracking [person::pat-wolthausen]
- [ ] Pat to provide estimate-to-actual variance on last 3 projects by Mon Apr 7 #tracking [person::pat-wolthausen]
- [ ] Pat to document active pre-sales pipeline status by Fri Apr 4 #tracking [person::pat-wolthausen]
- [ ] Pat to review all channels for open accountabilities by Wed Apr 2 #tracking [person::pat-wolthausen]
- [ ] Adam to update pat-wolthausen.md with HSA service ownership #tracking [person::pat-wolthausen]

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->
<!-- Watch for: Can he articulate utilization off the top of his head? Does he own the estimate quality, or does he blame scope creep? Is the pre-sales/delivery split something he manages actively, or does he just react to what comes in? Does he see himself as a function owner or as a senior architect who happens to have reports? -->

## Next session focus
<!-- After vacation: Did the service description get circulated? Did the utilization data land? If estimate variance is high, dig into root cause. If utilization is low, discuss pipeline development with Commercial. -->
