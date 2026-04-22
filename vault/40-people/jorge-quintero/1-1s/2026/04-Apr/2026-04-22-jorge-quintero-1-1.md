---
type: 1-1
date: 2026-04-22
person: jorge-quintero
---

# 1:1 — Jorge Quintero — 2026-04-22

---

## Carry-forward
*Open tracking items for Jorge Quintero — manually reviewed 2026-04-22*

**From Mar 31:**
- [ ] Jorge to review and circulate OI service description to all service managers — **page at v4 (Apr 9); good content, unclear if formally circulated** #tracking [person::jorge-quintero]
- [x] Jorge to produce first draft "state of the data" map — **Data Strategy page (v8, updated Apr 21) covers this substantively; call it done** #tracking [person::jorge-quintero]
- [ ] Jorge to draft rough proposal for capacity data consolidation via OI — **not as a standalone doc, though Data Strategy roadmap references it; clarify verbally** #tracking [person::jorge-quintero]
- [ ] Adam to update jorge-quintero.md with OI service ownership — **still open** #tracking [person::jorge-quintero]

**From Apr 16:**
- [ ] Jorge to circulate OI service description to all service managers by Fri Apr 18 — **page not updated since Apr 9; unclear if circulated** #tracking [person::jorge-quintero]
- [x] Jorge to deliver first draft state of the data map — **Data Strategy page qualifies; checking off** #tracking [person::jorge-quintero]
- [ ] Jorge to work with Chameleon on consulting vs. PS tagging in Salesforce — **status unknown; verify** #tracking [person::jorge-quintero]
- [ ] Adam to update jorge-quintero.md with OI service ownership — **still open** #tracking [person::jorge-quintero]

**New — from Slack conversation (week of Apr 14):**
- [ ] Inventory page fleshed out with framework content — **stub created Apr 17 (v1) but empty; needs filling** #tracking [person::jorge-quintero]

---

## Their agenda
<!-- What they want to cover — capture before or at start of meeting -->

## My agenda

### Framing: Different Conversation Than the Others — Acknowledge the Work, Then Go Deep on Inventory
Jorge has actually been shipping. The Data Strategy page is at v8 and was updated yesterday (Apr 21) — that's real, substantive work. Salesforce deployment shipped. The Inventory page was started. He's operating like a function owner. This 1-1 is less of an accountability conversation and more of a briefing and mandate-setting conversation — specifically answering the questions he raised over the weekend on inventory, and establishing clearly that he owns the data layer across the org, including the inventory data model.

---

### 1. Acknowledge What's Been Shipped (3 min)
Name it specifically:
- **Salesforce deployment (Apr 12):** Shipped while I was out, confirmed working. That's execution.
- **Data Strategy page (v8, updated Apr 21):** This is the "state of the data map" deliverable from Mar 31. It has current state, data flows, architecture options, ETL tooling recommendation, AI readiness section, and a roadmap. It's a real document. Call it done.
- **Inventory page (Apr 17):** He started it in direct response to the Slack conversation — that's the right behavior even if it's still a stub.

---

### 2. Inventory — Answer His Questions Directly (20 min)
Jorge asked two specific questions over the weekend that need clear answers before he can go further.

**Q1: "What is the goal? What would that visibility give Aptum?"**

The goal is not just a list of hardware. It's a decision-support instrument built on three numbers across six dimensions:

| Dimension | Owned                                            | Sold                              | Available to Sell         |
| --------- | ------------------------------------------------ | --------------------------------- | ------------------------- |
| Space     | Sellable sqft per DC                             | Allocated to cages, racks         | Immediately monetizable   |
| Power     | kW provisioned per DC                            | Committed to customers + internal | Without new capex         |
| Racks     | Racks installed on floor                         | Sold/filled                       | Ready to sell today       |
| Network   | Bandwidth, ports, cross-connects, IPs, firewalls | Deployed to customers             | Caveats apply (see below) |
| Compute   | Servers owned (deployed + shelf) + storage       | Customer committed + IaaS         | Without new procurement   |
| People    | Managed services hours available                 | Committed to active delivery      | Capacity left to sell     |

The **"Available to Sell"** number is the strategic output. It answers: *what can we offer a customer today, without a capex conversation?* This is what governs Private Cloud siting decisions for UK and US buildouts — and it's what Dave Pistacchio (DigitalBridge) independently came to Ian Rae asking for, at the same time we were already working on this internally. That external pressure creates a real timeline and a real audience for this work.

**Q2: "Who would be the main users? Who would I need to understand this for?"**

- **Ian Rae and Dave Pistacchio** — the immediate forcing function. Private Cloud buildout decisions in UK and US need this data to make siting decisions.
- **All service managers** — capacity planning for their own dimensions. George knows racks and power; Martin knows compute; Ben knows network. They each own their slice. OI makes it unified and visible.
- **Finance** — asset valuation, depreciation, and cost allocation accuracy all require knowing what's deployed where.
- **Martin and Pat (pre-sales scoping)** — HSA needs to know what compute is available before committing in a SOW.
- **Adam (VP level)** — the unified view is what enables board-level capacity reporting.

**Jorge's specific role: own the data model, not the physical audit**

Jorge does not own the physical count of servers (that's George), the network port spreadsheet (that's Ben), or the compute deployment list (that's Martin). What he owns is:
- The schema — the Owned/Sold/Available-to-Sell data model that all six dimensions feed into
- The pipeline — pulling from each owner's source system (CMDB, Fusion, HyperView, etc.) into a unified view
- The unified view — a live, queryable representation of total inventory state across the org

This is exactly what OI is for. Inventory is not a one-time audit; it's a live data product. Jorge owns the live data product.

**"Should we call a meeting with Matt and George?"**

Yes — but after this session, not instead of it. The purpose of this 1-1 is to give Jorge the framework so he can *run* that meeting, not just attend it. He should go in with:
1. The six-dimension schema and a clear ask for each owner (what data do you have, in what system, at what freshness?)
2. A draft data model for what "Owned/Sold/Available-to-Sell" looks like in each dimension
3. A proposal for where the unified view lives (likely an OI pipeline feeding a dashboard)

After this 1-1, Jorge schedules the meeting with Matt and George. Adam will be there or not — Jorge's call.

**Known complications to flag before the meeting:**
- **Network (Ben):** Not a single number. Bandwidth, cross-connects, IPs, switching ports, firewalls, and load balancers are all discrete sub-elements. The Citrix load balancer situation (5 licenses covering managed hosting via a 1TB pool) means the "Available to Sell" figure for load balancers has a shelf life — don't build a model that assumes it's durable.
- **Compute:** George owns the physical inventory; Martin owns the logical/IaaS layer. These two numbers need to align. They may not today.
- **People:** Hours is the right unit, not headcount. Skills gaps within available headcount mean "Available to Sell" capacity is not just hours — it's the right hours for the right work.
- **CMDB accuracy:** George has a target of 0% discrepancy between CMDB and physical audit, which means current accuracy is not confirmed. The inventory model can only be as accurate as the source data.

---

### 3. OI Service Description — Circulate It (5 min)
Page: https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045223434/Operations+Intelligence
Last updated: Apr 9 (v4). This is a good page — probably the strongest service description in the network conceptually. The Zabbix section is thorough and honest, the tooling ownership model is well-reasoned, and the "Bottom Line" framing is exactly right. But it has now missed two circulation deadlines (Apr 4, Apr 18).

Why it matters right now: with today's inventory conversation, OI's scope is expanding. The other service managers need to understand what OI does and doesn't own before Jorge starts asking them for data. Circulating the service description is not a formality — it's the org communication that enables his work.

**Hard deadline: Fri Apr 25.** Send it to all service managers with a two-sentence note: here's OI's mandate, here's what I need from your team. Don't just share a link — make the ask explicit.

**One thing to clean up on the page:**
The Measures of Success section lists five qualitative outcomes (adoption, reduction in manual reporting, etc.) but no quantified targets. For a function in Discovery this is fine — but at least one of them should have a number attached. Suggest: "reduction in manual reporting" → target a specific number of recurring manual reports replaced by automated pipelines by end of H2.

---

### 4. Data Strategy Page — Good Work, Close the Open Sections (5 min)
Page: https://aptum.atlassian.net/wiki/spaces/~7120207a376168defa4e7abd9bf60c07b552ea/pages/5162303534/Data+Strategy
This is the real work — v8, updated Apr 21. The architecture, ETL tooling recommendation (Python over SSIS), AI readiness section, and data model analysis are solid. A few things still need to be filled in:

- **Section 3 (Data Governance):** Header only, no content. This is a gap — without governance, the data layer has no ownership model for who can change what.
- **Section 5 (Data Quality):** Header only. Even a brief statement of data quality standards belongs here.
- **Section 8 (Roles & Responsibilities):** Header only. Who owns each pipeline? Who approves schema changes?
- **Section 9 (Success Metrics):** Header only. What are the OI function's KPIs?
- **Roadmap timeline:** "Timeline TBD" — needs dates even if rough. What's Q2? What's Q3?

Ask Jorge: can he put draft content in sections 3, 8, and 9 by end of next week? Even bullet points are better than empty headers.

---

### 5. Path Out of Discovery — Agree on Alpha Criteria (5 min)
The OI service description explicitly flags: "Every month in Discovery is another month of decisions made without data." The inventory initiative is a forcing function — Dave Pistacchio needs this, and he's not going to wait for a TBD timeline.

What does Alpha look like for OI? Propose defining it as:
- At least 3 active data pipelines running on the new Python ETL stack (replacing SSIS)
- Inventory unified view live for at least two dimensions (e.g., Compute and Space/Power)
- OI service description formally circulated and acknowledged by all SMs
- Data Strategy governance section complete with named owners per pipeline

Ask Jorge: does this feel right? What would he add or change? Make the Alpha criteria a concrete list — same logic as Martin's AptCloud Beta criteria. Once it's a list, it's a plan.

---

### 6. Quick Pulse (5 min)
- **Chameleon consulting vs. PS tagging:** Status? Does he need anything from Adam to unblock it?
- **Monday Morning Reports:** Still sustainable? Or is manual reporting crowding out the strategic work?
- **Any new data pipeline requests** from other SMs since the service network conversations started?

---

## Discussion Notes
<!-- Raw capture — don't over-format in real time, just get it down -->

---

## Decisions & Actions

| Action | Owner | By When |
|--------|-------|---------|
| Circulate OI service description to all SMs (explicit ask, not just a link) | Jorge | Fri Apr 25 |
| Fill in inventory page framework: 6-dimension schema, dimension owners, data sources | Jorge | Fri Apr 25 |
| Schedule inventory meeting with Matt and George (Jorge leads) | Jorge | Next week |
| Draft content for Data Strategy sections 3 (Governance), 8 (Roles), 9 (Metrics) | Jorge | Next 1:1 |
| Add rough timeline to Data Strategy roadmap | Jorge | Next 1:1 |
| Confirm status of Chameleon consulting vs. PS tagging work | Jorge | This week |
| Define OI Alpha criteria (agreed in session) | Jorge + Adam | This session |
| Update jorge-quintero.md with OI service ownership | Adam | This week |
| | | |

<!-- Inline tracking tasks -->
- [ ] Jorge to circulate OI service description to all SMs by Fri Apr 25 #tracking [person::jorge-quintero]
- [ ] Jorge to fill in inventory page with 6-dimension framework by Fri Apr 25 #tracking [person::jorge-quintero]
- [ ] Jorge to schedule and lead inventory meeting with Matt and George #tracking [person::jorge-quintero]
- [ ] Jorge to draft Data Strategy sections 3, 8, 9 and add roadmap timeline #tracking [person::jorge-quintero]
- [ ] Jorge to confirm Chameleon PS tagging status #tracking [person::jorge-quintero]
- [ ] Adam to update jorge-quintero.md with OI service ownership #tracking [person::jorge-quintero]

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->
<!-- Watch for: Does he immediately understand the Owned/Sold/Available-to-Sell framing and see how to apply it, or does he need to work through it? Does he want to call the meeting with Matt and George himself, or does he want Adam in the room? Does he have a clear position on where the unified inventory view should live technically (which system, which pipeline)? How does he react to being handed the inventory data model mandate — energized or anxious? -->

## Next session focus
<!-- OI service description circulated and responses received. Inventory page has the framework filled in. Meeting with Matt and George has happened or is scheduled. Data Strategy open sections drafted. OI Alpha criteria defined — track progress against them. -->
