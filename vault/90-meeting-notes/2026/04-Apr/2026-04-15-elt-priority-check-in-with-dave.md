---
type: meeting
date: 2026-04-15
attendees:
  - "[[Ian Rae]]"
  - "[[Dave Pistacchio]]"
  - "[[Sarah Blanchard]]"
  - "[[Marc-Alex Forget]]"
  - "[[JP Rosato]]"
initiative: DBRG Post-Board Priorities
---

# 2026-04-15 — ELT Priority Check-in with Dave

**Date:** Tuesday, April 15, 2026 — 8:30 AM ET
**Attendees:** [[Ian Rae]], [[Dave Pistacchio]], [[Sarah Blanchard]], [[Marc-Alex Forget]], [[JP Rosato]], [[Adam Nelson]]
**Related:** [[2026-04-10-dbrg-aptum-weekly-sync]] · [[2026-03-30-internal-aptcloud-demo]]

---

## Prep — Dave's Priorities Where I'm Named or Implicated

> [!info] Source
> Ian sent the "Update on DBRG priorities" tracker to Dave last night (April 14) with status updates. Dave kicked this off at 9:54 AM asking "what will be accomplished this week." Ian invited Dave to review at 8:30 AM. This is that meeting.

### Critical Items — Be Ready to Speak to These First

#### DBRG #4 — Assess and Act on Operations Team Underperformers
**Priority:** Critical · **Owner:** Me
**Dave's ask:** Evaluate ops employees for performance and skill breadth. Evolve or replace those with siloed/limited capabilities.
**My position:**
- Last re-org already removed underperformers + some good performers
- Some people I'd like to "step up" but no objective underperformance criteria exist yet
- **Next step I committed to:** Update PIP framework with [[Nikki]] — current version reads like "Document and Fire" not "Performance Improve"
- Current plan: 
	- Get the PIP framework from Nikki - I'd rather we tweak this to be an "improvement"/"alignment" plan vs. document to fire plan.
	- Get all the Managers to identify current roles and ensure there is an objective framework these people can be measured against
	- Review w/ each of the managers individually.

> [!warning] Watch out
> Dave wants action, not just process. Be prepared to say who specifically needs to step up and what the timeline is. He may push for names.

#### DBRG #2 — Replace Underperforming Sales Reps (supporting role)
**Priority:** Critical · **Owner:** Sales Leadership
**My role:** Transition planning with [[Fred]] — meeting scheduled for today (April 15)
**Status:** Initial assessment complete. MA doing outreach for backfills. Coordination with me (SDM) and Sarah (HR) for transition support.

> [!note] Backup
> I don't own this but Dave may ask about my involvement. Keep it simple: "Fred and I are meeting today to confirm the transition plan, coordinating with Sarah on HR side."

#### DBRG #3 — Link Advisory → Execute → MRR in Salesforce
**Priority:** Critical · **Owner:** Ops / Chameleon
**My role:** Jorge (now in my org, Operational Intelligence) supports data pipelines. I left a comment on the doc saying PS should go into the Expert Services LOB with delineators for advisory vs. execute. Sarah should own LOB attribution.
**Status:** Jorge engaged with Chameleon. Creating weighted backlog in JIRA. SF cleanup first step completed last weekend.

> [!note] Backup — from April 10 sync
> Ian called out "consulting and professional services properly swimlaned" — this is exactly the advisory vs. execution tracking. Sarah sent Chameleon scope/findings to MA on April 1. Jorge is the data execution arm here.

### High Priority Items — Likely Discussion Topics

#### DBRG #9 — Evaluate CloudMC / Apt Cloud Readiness + Launch Plan
**Priority:** High · **Owner:** Product/Engineering — but Dave asked me, Will, and MA specifically
**Dave's ask:** Commercial plan — efforts, timeline, incremental spend, LAUNCH PLAN for Apt Cloud, plus an indicative representative customer.
**My position:**
- Demo on March 30 went well. Dave called it "true private cloud" and a competitive advantage
- $39K MRR already closed via Ignite before formal launch
- 7 new logos signed, ~74% compute margin vs ~37% hosting avg
- SCADAcore = flagship ($25K/mo, 36-month)
- Platform runs on CloudStack/KVM, zero VMware licensing cost
- **Representative customer profile:** Mid-market, 50-500 employees, hybrid infra complexity, 1-5 IT staff, VMware renewal shock or cloud bill surprise
- **Roadmap items to reference:** Ignite customer migrations → Canonical MaaS bare metal → Proxmox VE orchestration → K8s service → 2nd DC install → nested reseller billing

> [!tip] This is the highest-visibility new ask
> Dave wants a go-to-market timeline as a "fast follow." Be ready with at least a rough phasing: what's live now, what's Q3, what's Q4. Will and MA need to be aligned on this.

**What I already have in flight that supports this:**
- AptCloud Strategy v1.2 doc (updated post-demo with board feedback)
- Product Strategy v2.0 with assessment framework and three-motion funnel
- Competitive landscape analysis already drafted (HPE Morpheus, CloudBolt, VMware Aria, ThinkOn, Opti9, OVH, DigitalOcean, OpenMetal, Rackspace)

#### DBRG #10 — Competitive Analysis: Apt Cloud vs. Market
**Priority:** High · **Owner:** Product / Sales Engineering
**Status:** Ian shared the product strategy docs with Dave including hybrid cloud opportunity. Next step is to work with Dave to clarify approach.

> [!note] Backup
> The competitive landscape table exists in both the AptCloud demo deck (slide 6) and the AptCloud Strategy doc (Section 4). The main differentiator: no other platform in the Canadian mid-market does CloudStack + white-label portal + managed services in one stack.

#### DBRG #12 — Rethink Churn / Cancellation / Loss Reason Data Codes
**Priority:** High · **Owner:** Operations / CX — me, Lacie, Fred
**Dave's ask:** Better granularity on why customers cancel, why we lose sales, which equipment causes problems. Improve decision-making and trend analysis.
**Status:** Churn program underway. Jorge completing SF cleanup.
**Next step committed to:** Proposed improvements + implementation timeline "by end of week" — this may already be overdue.

**What I already have in flight that supports this:**
- Dark Matter analysis: 415+ silent customers, 43 actively shopping (ZoomInfo intent >=80)
- AI Account Intelligence: 35 customer reports from 8 data sources
- Renewals process: 90-day pre-renewal reviews, revenue-based escalation tiers

#### DBRG #6 — Develop ICE (Ideal Customer Engagement) Framework
**Priority:** High · **Owner:** Sales / Marketing — but "@Adam has an operations centric view"
**My angle:** The product strategy docs already describe the three-motion funnel (Advisory → Execute → Operate) and the assessment-to-service mapping. That IS the operations view of customer engagement. MA is connecting with JP.

#### DBRG #5 — Define Single Unified ICP
**Priority:** Critical · **Owner:** Marketing / Sales — but I did the synthesis work
**Status:** Aptum-ICP.md complete. Ian sent to Dave with full product strategy docs.
**Next step:** Review with broader team.

> [!note] Backup
> If Dave asks: "The ideal Aptum customer is a mid-market org, 50-2,000 employees, $10M-$500M revenue, digitally dependent but tech isn't their core business, running hybrid workloads, feeling the pain of managing complexity. Found in SaaS, eCommerce, financial services, healthcare, professional services, media. HQ'd in North America (Canada + US East Coast) with secondary UK presence."

### Medium Priority — Probably Won't Come Up, But Have an Answer

#### DBRG #20 — CPQ Tool Evaluation
**Owner:** Sales Ops — I raised this
**Status:** H1 goal met (sales largely off CPQ for order entry), but 80% of server quotes need mods to the standard tool. More time fighting the tool than quoting. Framed as an org-level rethink, not a patch.

#### DBRG #16-19 — PS Packaging, Rates, Utilization, Performance Reporting
**Owner:** PS / Product / Finance
**My angle:** These all connect to the Expert Services vision I commented about on the doc — extracting Expert Services from Cloud Platform. Three LOBs: Infrastructure (commodity physical), Cloud (hyperscaler or private), Expert Services (management tiers + PM + PS).

---

## Part B Crosswalk — My Existing Q3 Commitments That Support Dave's Asks

If any of these come up in discussion, here's how they tie back:

| My H2 Board Commitment | Supports DBRG # | Connection |
|---|---|---|
| eStruxture savings ($161K/mo, May 1) | General EBITDA | Committed savings, just needs to land |
| Centrilogic onboarding (15 customers, ~C$846K ann.) | #9 (growth story) | New revenue directly via service delivery team |
| Ignite customer migrations (7 logos, C$39K MRR) | #9 (Apt Cloud proof) | These ARE the Apt Cloud proof points |
| Jorge → Operational Intelligence | #3, #8, #12 | Data pipelines for SF, churn codes, unified views |
| Dark Matter program (415+ silent customers) | #12, #14 | Churn prediction + proactive outreach |
| AI Account Intelligence (35 reports) | #14, #15 | Already piloted with STG, Dave, JP |
| PCI software upgrades (15% → 70%) | Compliance | Q3 audit target |
| Network savings (C$994K vs C$761K budget) | General EBITDA | $172K ahead of budget — good news to mention |
| VMware → Proxmox (C$339K/yr saved) | #9, #10 | Powers the VMware-alternative GTM |
| AWS margin improvement (3% → 8%, April 1) | General margin | ~C$121K annualized |
| Renewals process + customer risk program | #12 | 90-day pre-renewal reviews, escalation tiers |
| Business reviews for top 30 accounts | #6 (ICE) | Customer intimacy = engagement framework in action |
| Data architecture cleanup (124 tables, 9 revenue versions) | #3, #11 | Can't track advisory→MRR without clean data |
| Service Network (9 nodes, accountability chains) | #4 | Objective structure for performance expectations |
| Quoting ease / CPQ rethink | #20 | Problem defined, evaluation needed |

---

## Notes
<!-- Raw — don't over-format in real time, just capture -->


## Decisions Made
<!-- Anything decided here that needs a record -->


## Action Items
| Action | Owner | By When |
|--------|-------|---------|
| | | |

## Open Loops to Add
<!-- Things to copy to [[open-loops]] after the meeting -->


---
*Route after meeting: actions → 40-people, decisions → 60-decisions, context → 20-context, loops → open-loops*
