---
type: 1-1
date: 2026-04-01
person: martin-tessier
---

# 1:1 — Martin Tessier — 2026-04-01

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

### Framing: First Real 1:1 + Vacation Prep
First structured 1:1 with Martin. He owns Compute Platforms — everything from bare metal to OS. His team builds environments: configuration standards, automation playbooks, OS deployment, monitoring/backup agent installation. They hand off clean, documented environments to Service Desk or Managed Cloud. He also co-owns AptCloud platform engineering (the build side). This meeting needs to: (1) establish ownership, (2) align on service description review, (3) clarify the direction of travel for his team (automation, not manual provisioning), and (4) set focused priorities for the week while I'm out.

### 1. Board Context (5 min)
Key takeaways relevant to Martin's world:
- AptCloud was presented to the board as Alpha, built on excess server inventory. The board expects a maturation path.
- The capacity framework was presented — Martin's compute capacity dimensions are part of that picture.
- H2 execution emphasis: provisioning speed and quality directly protect hosting margin.
- The board heard about the DC portfolio efficiency work. Martin's environments are what get deployed into those optimized locations.

The message: the board cares about your output quality because it underpins every revenue-generating environment.

### 2. Service Description Review — PARAMOUNT (10 min)
Martin owns the Compute Platforms service description: https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045518349/Compute+Platform

This is the #1 deliverable. Same ask as all service managers.

Ask him:
- Has he read the current version? Does it accurately reflect what his team does and doesn't do?
- The boundary with George's DC Ops team (George owns physical, Martin owns everything that runs on top) — is that clean in practice, or are there grey areas?
- The handoff to Service Desk and Managed Cloud — is documentation quality consistent?
- Who needs to review it? (DC Ops/George, Service Desk/Jason, Managed Cloud/Andrei at minimum)
- Can it be circulated for review by end of week (Fri Apr 4)?

Key flags from the service description:
1. **Scope boundary with George:** The "functional split, not consolidation" framing. Does Martin agree this is the right model?
2. **Automation tooling ownership:** Who owns the playbook tooling (Ansible, Terraform, etc.) — Compute Platforms, Operational Intelligence, or a future platform engineering function? This is an open question.
3. **Direction of travel:** His team's value is in the playbooks and standards, not manual execution. Does he see it that way?

### 3. Capacity Framework: Compute Dimensions (10 min)
For Martin, the relevant capacity questions:

**Compute capacity:**
- How many servers/hosts can we provision with current inventory?
- What's the split: dedicated vs. private cloud vs. AptCloud?
- How many environments are in the provisioning queue right now?

**Provisioning throughput:**
- How many environments per week/month can his team deliver?
- What's the automation coverage — what percentage is automated vs. manual?
- Where are the bottlenecks?

Ask him:
- Can he produce a first-pass view of compute capacity by type and location?
- What's the provisioning backlog look like?
- Target: first draft by Mon Apr 7.

### 4. AptCloud Platform Status (5 min)
Martin co-owns AptCloud with Andrei (Martin builds it, Andrei operates it post-handoff).

Quick pulse:
- How many clusters are deployed? What's the hardware footprint?
- What's blocking Beta readiness? Is it technical, operational, or both?
- Is the change management discipline for shared clusters in place?
- Does he feel adequately staffed for both BAU provisioning AND AptCloud build?

### 5. Provisioning Metrics (5 min)
The service description has several "To be defined" metrics:
- Provisioning accuracy (to spec, first time)
- Provisioning turnaround time
- Config validation pass rate
- Documentation completeness at handoff

Ask him:
- Does he have any of these measured today, even informally?
- What would it take to start tracking turnaround time and first-time accuracy?
- This isn't about perfection — it's about knowing where you stand so you can improve.

### 6. Priorities for the Week (5 min)
Three things for the week while I'm out (Apr 2–10, back Apr 13):

1. **Service description:** Review it, circulate for feedback by Fri Apr 4. Get George, Jason, and Andrei to validate the boundaries.
2. **Capacity snapshot first pass:** Compute capacity by type and location. Provisioning backlog status. Target Mon Apr 7.
3. **AptCloud status write-up:** Where the platform stands, what's needed for Beta, timeline. By Fri Apr 4.

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
| Review Compute Platforms service description and circulate for feedback | Martin | Fri Apr 4 |
| Produce first-pass compute capacity snapshot (by type and location) | Martin | Mon Apr 7 |
| Written AptCloud status: current state, Beta readiness, needs, timeline | Martin | Fri Apr 4 |
| Review emails/Jira/Slack/Teams/calendar for open accountabilities | Martin | Wed Apr 2 |
| Update martin-tessier.md with Compute Platforms service ownership | Adam | Before vacation |
| | | |

<!-- Inline tracking tasks — tag with #tracking so they surface on the hub -->
- [ ] Martin to review and circulate Compute Platforms service description by Fri Apr 4 #tracking [person::martin-tessier]
- [ ] Martin to produce first-pass compute capacity snapshot by Mon Apr 7 #tracking [person::martin-tessier]
- [ ] Martin to deliver written AptCloud platform status by Fri Apr 4 #tracking [person::martin-tessier]
- [ ] Martin to review all channels for open accountabilities by Wed Apr 2 #tracking [person::martin-tessier]
- [ ] Adam to update martin-tessier.md with Compute Platforms service ownership #tracking [person::martin-tessier]

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->
<!-- Watch for: Does he see his team as an automation/standards team, or as a manual provisioning crew? Can he articulate the George boundary cleanly? Does he have a handle on AptCloud maturity? How does he react to the metrics ask — does he see measurement as useful or as overhead? -->

## Next session focus
<!-- After vacation: Did the service description get circulated? Did the capacity snapshot land? If AptCloud status write-up is good, use it as the basis for a Beta readiness review. Start defining provisioning metrics baseline. -->
