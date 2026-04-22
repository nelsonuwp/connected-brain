---
type: 1-1
date: 2026-04-22
person: martin-tessier
---

# 1:1 — Martin Tessier — 2026-04-22

---

## Carry-forward
*Open tracking items for Martin Tessier — manually reviewed 2026-04-22*

**From Apr 1:**
- [x] Martin to review all channels for open accountabilities by Wed Apr 2 — *old, done* #tracking [person::martin-tessier]
- [x] Martin to review and circulate Compute Platforms service description — page updated Apr 10 (by Martin, v3); partial credit, after the Apr 4 deadline and not re-touched since Apr 16 session #tracking [person::martin-tessier]
- [ ] Martin to produce first-pass compute capacity snapshot by type and location — **no evidence; three weeks overdue** #tracking [person::martin-tessier]
- [ ] Martin to deliver written AptCloud platform status (current state, Beta readiness, timeline) — **no evidence in Confluence** #tracking [person::martin-tessier]
- [ ] Adam to update martin-tessier.md with Compute Platforms service ownership — **still open** #tracking [person::martin-tessier]

**From Apr 16:**
- [ ] Martin to circulate Compute Platforms service description by Fri Apr 18 — **page not updated since Apr 10; unclear if formally circulated** #tracking [person::martin-tessier]
- [ ] Martin to deliver first-pass compute capacity snapshot — **still no evidence** #tracking [person::martin-tessier]
- [ ] Martin to produce AptCloud Beta readiness criteria list — **no evidence** #tracking [person::martin-tessier]
- [ ] Adam to update martin-tessier.md with Compute Platforms service ownership — **still open** #tracking [person::martin-tessier]

---

## Their agenda
<!-- What they want to cover — capture before or at start of meeting -->

## My agenda

### Framing: Accountability + Page Gaps + Two Decisions That Need to Come from Martin
Martin's accountability picture is similar to Pat's: the capacity snapshot and AptCloud status write-up have been on the list since Apr 1 with no evidence of delivery. The Compute Platform page is at version 3 and hasn't been touched since before the Apr 16 session that set a new Apr 18 deadline. The bigger conversation today is that two things from the Apr 15 Product Delivery Flow session need to be reflected in his page — the backup ownership model and the patching model — and two open questions on the page need Martin's position, not just flags. He needs to own the resolution, not wait for someone else to decide.

---

### 1. Accountability Check (10 min)

**A. Compute Platform service description — circulated?**
Page (https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045518349/Compute+Platform) is at v3, last touched Apr 10. The Apr 16 session set a hard deadline of Apr 18. Has he:
- Updated the page to reflect the Apr 15 Product Delivery Flow decisions?
- Sent it to George, Jason, and Andrei for review?
- **Hard deadline: Fri Apr 25.**

**B. Compute capacity snapshot — three weeks overdue**
The ask was a first-pass view: servers/hosts by type and location, dedicated vs. private cloud vs. AptCloud, current provisioning queue. Does he have this?
- Even a rough spreadsheet is fine. The goal is a baseline — not a perfect picture.
- If he doesn't have it: is the data available and he hasn't compiled it, or is it genuinely hard to pull?

**C. AptCloud Beta readiness criteria**
A written criteria list — what "Beta-ready" actually means. Not a date, a list of conditions. Still not landed. Get it in this session if possible: name the criteria live and write them down together.

---

### 2. Confluence Page Review — Compute Platform (15 min)
Page: https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045518349/Compute+Platform

**What's working well:**
- The Martin/George scope boundary is the best-articulated boundary in the service network — the functional split (George = physical; Martin = everything that runs on top) is clear, and the direction of travel (automation team, not manual crew) is explicit and correct.
- The AptCloud Specifics section is specific and appropriately flags the Alpha risk profile (shared cluster, multi-tenant risk).
- Aptum IaaS commercial intent is clear.

**Issues to fix:**

**A. The function framing is now inaccurate**
The page header says: *"Function: Architecture & Delivery (one-time delivery, not ongoing operations)."* But Martin does ongoing operations — he runs the AptCloud/IaaS platform continuously. This framing made sense for provisioning, but not for IaaS. Needs to be updated to reflect both the one-time provisioning function AND the ongoing platform operations function.

**B. Apr 15 Product Delivery Flow decisions not reflected**
Two things were formally agreed at the Apr 15 session and need to appear in this page:

*Backup ownership model:* Martin owns the backup product — provisioning, storage, capacity (Veeam infrastructure). Jason owns customer-facing backup support (monitoring, restore testing, customer tickets). This split should be explicit in the Accountable For section, not just listed as "Backups" in the products list.

*Patching model:* Martin prepares patches (testing, staging, validation via WSUS/Red Hat Satellite). Jason applies them. This handoff should be described explicitly — it's a real operational boundary that needs to be on paper.

**C. All metrics are "To be defined"**
Seven metrics on the page, zero targets. Provisioning accuracy, turnaround time, config validation pass rate, L3 escalation response, AptCloud availability — all TBD. In this session: agree on two metrics Martin will start tracking informally. Provisioning turnaround time is the obvious first one.

**D. Two open questions need Martin's position, not just flags**

*Automation tooling ownership:* The page flags that who owns playbook tooling (Ansible/Terraform/etc.) — Compute Platforms, OI, or a future platform engineering function — is unresolved. This has been on the page since at least Apr 10 with no movement. Martin needs a position. He uses these tools daily. What does he think the right ownership model is? This needs an answer, not a continued flag.

*AptCloud Beta readiness:* Same — flagged but no criteria. Get the criteria list in this session.

**E. Service Guides product language — confirmation needed**
The Service Guides page (https://aptum.atlassian.net/wiki/spaces/Product/pages/4667736066/Service+Guides) has a note: *"Compute owns the hardware catalog (will replace with 'Owns the Product' once Pat and Martin are ok with the change)."* Has Martin reviewed the Dedicated Server, Shared Cluster, Dedicated Cluster, and Private Cloud flow descriptions on that page? Does the language accurately reflect how his team operates? His confirmation is needed before that language is updated.

---

### 3. AptCloud Beta — Define the Criteria List (5 min)
The board expects a maturation path from Alpha to Beta. The Apr 16 session asked for a concrete criteria list — not a date, a list of conditions. What has to be true before AptCloud can be called Beta-ready? Name them in this session:

Suggested starting dimensions (push Martin to own the specifics):
- Technical threshold: what stability/uptime/cluster coverage?
- Operational threshold: runbooks documented, change management process in place, Service Desk trained?
- Headcount/capacity: adequately staffed to run BAU provisioning AND AptCloud build in parallel?

This list becomes the plan. Once it exists, track progress against it.

---

### 4. Ongoing Board-Visible Items — Quick Alignment (5 min)

**Ignite / CloudStack-KVM pipeline:**
- 7 new logos, C$39K MRR is the board target. Is the pipeline growing? Are there Ignite opportunities in the queue that Martin needs to prep for?

**VMware → Proxmox migration:**
- C$339K/yr annualized savings from internal migration is done. Any further VMware environments in scope for migration?

**Q3/Q4 deferred items:**
- Imperva renewal, Alert Logic renewal (evaluate consolidation) — Q3
- Dell OMSA, DataDomain refresh — Q4
- ESXi 9 (pending testing), Next Gen Linux (Rocky/RHEL/Alma 10) — still deferred
- Does Martin have a view on when these come off the deferred list?

---

### 5. Operational Pulse (5 min)
- Any provisioning queue backlog or blocked environments right now?
- Any issues with the AptCloud Alpha that could affect customers or the Beta timeline?
- Any capacity tension between BAU provisioning and AptCloud build — is the team managing, or is it becoming a problem?

---

## Discussion Notes
<!-- Raw capture — don't over-format in real time, just get it down -->

---

## Decisions & Actions

| Action | Owner | By When |
|--------|-------|---------|
| Update Compute Platform page: fix function framing, add backup/patching model, open questions | Martin | Fri Apr 25 |
| Circulate Compute Platform page to George, Jason, Andrei for review | Martin | Fri Apr 25 |
| Deliver compute capacity snapshot (by type and location) | Martin | Fri Apr 25 |
| Produce AptCloud Beta readiness criteria list | Martin | Fri Apr 25 |
| Confirm Service Guides product flow language for Compute | Martin | Fri Apr 25 |
| Take a position on automation tooling ownership (Compute vs. OI) | Martin | Next 1:1 |
| Define 2 provisional metric targets (agreed in session) | Martin | Next 1:1 |
| Update martin-tessier.md with Compute Platforms service ownership | Adam | This week |
| | | |

<!-- Inline tracking tasks -->
- [ ] Martin to update Compute Platform page (framing, backup/patching model, open questions) by Fri Apr 25 #tracking [person::martin-tessier]
- [ ] Martin to circulate Compute Platform page for review by Fri Apr 25 #tracking [person::martin-tessier]
- [ ] Martin to deliver compute capacity snapshot by Fri Apr 25 #tracking [person::martin-tessier]
- [ ] Martin to produce AptCloud Beta readiness criteria list by Fri Apr 25 #tracking [person::martin-tessier]
- [ ] Martin to confirm Service Guides product language #tracking [person::martin-tessier]
- [ ] Martin to take a position on automation tooling ownership #tracking [person::martin-tessier]
- [ ] Adam to update martin-tessier.md with Compute Platforms service ownership #tracking [person::martin-tessier]

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->
<!-- Watch for: Does he have the Beta criteria list ready, or is he still hedging? Does he own a position on automation tooling ownership, or does he wait for Adam/Jorge to decide? Can he articulate the capacity tension between BAU and AptCloud build — or does he minimize it? Does he see the function framing error ("one-time delivery") and correct it proactively, or does he need it pointed out? -->

## Next session focus
<!-- Compute Platform page updated and circulated. Capacity snapshot in hand — use it to assess staffing adequacy. AptCloud Beta criteria list as the working plan. Automation tooling ownership decision made. Two metrics being tracked. -->
