# Aptum Ideal Customer Profile

## Single Unified ICP, Grounded in Portfolio Data

**Version 2.1 | April 28, 2026**

---

## Why a Single ICP

The earlier Product Strategy v1.3.1 ([Confluence page](https://aptum.atlassian.net/wiki/search?text=Product+Strategy+v1.3.1)) defined two ICPs: one for infrastructure buyers and one for digital natives with 7+ developers. The board directed the team to consolidate to a single ICP. Ian Rae put it simply in the March 31, 2026 product discussion: "We're a mid-market company selling to mid-market."

This document defines one Ideal Customer Profile. It also defines what an ideal customer is not, using real portfolio data to show where the current customer base aligns and where it diverges. It integrates the assessment framework as the qualification and onboarding mechanism: the way Aptum determines whether a prospect fits the ICP, builds the relationship, and funnels the customer into the managed services and infrastructure stack.

The ICP also reflects the brand promise that anchors product strategy. Aptum's brand commits to the right workload on the right platform, the right expertise at the right time, and your cloud, your way. The ideal customer is one who values that proposition: someone with workloads that belong on different platforms, the operational maturity to want a partner instead of a single vendor, and the willingness to pay for managed services that are demonstrably better than what they could do in-house.

---

## The Ideal Customer

### Company Profile

The ideal Aptum customer is a mid-market organization, typically between 50 and 2,000 employees, generating $10M to $500M in annual revenue. They are digitally dependent (their revenue flows through technology) but technology is not their core business. They are running a mix of workloads across on-premises infrastructure and at least one hyperscaler, and they are feeling the pain of managing that complexity.

They are most commonly found in these verticals: SaaS/digital platforms, eCommerce, financial services, healthcare/life sciences, professional services, and media/content delivery. They are headquartered in or have meaningful operations in North America (Canada and US East Coast especially), with secondary presence in the UK.

### Firmographic Anchors

| Attribute | Ideal Range | Why |
| --- | --- | --- |
| Employee count | 50 to 2,000 | Large enough to have real infrastructure needs, small enough that their IT team (2 to 15 people) needs a partner |
| Annual revenue | $10M to $500M | Budget exists for managed services, but they aren't large enough to build everything internally |
| IT team size | 2 to 15 people | This is the sweet spot. Overwhelmed, stretched thin, doing too many things. They need a safety net. |
| Infrastructure spend | $10K to $100K/mo MRC | Below $10K the economics don't work for managed services stacking. Above $100K they typically have in-house capability. |
| Cloud maturity | Hybrid (on-prem + at least one hyperscaler) | Pure cloud-native companies won't need Aptum's infrastructure. Pure on-prem companies aren't ready for the conversation. |

### Behavioral Indicators

These are signals to listen for, not a checklist to score. A prospect does not need to show all of them. One strong signal is enough to open the right conversation. Two or three in combination means you are almost certainly talking to the right person at the right time. Read these as patterns you will recognize when you hear them, not as qualifying criteria that must all be present.

**Their workloads have reasons to stay off a hyperscaler.**

The reason varies and does not matter as much as the signal itself. Some customers have done the TCO math and repatriation to private infrastructure makes financial sense. Some have regulatory or data sovereignty constraints that limit their hyperscaler options. Some have latency-sensitive applications that hyperscalers cannot serve cost-effectively. Some have legacy applications that would cost more to re-architect than to simply host.

The related variant worth listening for: they know their infrastructure situation needs attention, but their team does not have the internal capacity or expertise to act on it. The urgency is real. The problem is real. But there are three people in IT, all of them reactive, and no one has bandwidth to plan a migration. This is what "I need a partner, not just a vendor" sounds like before the customer has figured out how to say it.

**They are on VMware and their Broadcom renewal is coming.**

The 300 to 1,050% price increases are validated by Gartner and are not going away. When you hear this signal, there is almost always a renewal date attached, which creates urgency that is not manufactured. These customers are actively looking for alternatives. Aptum's CloudStack and Proxmox options through Aptum Portal are a direct answer to the problem they are trying to solve right now.

**Their IT team is overwhelmed and stretched thin.**

Small team, high reactive load, someone carrying a pager they resent. They are not doing planned work because they cannot get ahead of the unplanned work. The telling phrase is some version of "we spend all our time keeping the lights on." These customers are not shopping for a cheaper version of what they have. They are looking for someone who will actually take things off their plate, which is a fundamentally different and more durable conversation.

**They ask questions that signal they want a relationship, not a transaction.**

They want to know how Aptum's team is structured. They ask about experience with similar customers. They are not leading with price per GB in the first conversation. This signal often shows up in how they engage rather than in something they state directly. Customers who are shopping for commodity do not ask these questions.

> **On multi-product customers:** The portfolio data is clear that multi-product customers generate 94.46% of Aptum's revenue and churn at materially lower rates than single-product customers. This is not a qualifying signal for new logos; it is the target outcome. The goal of the assessment and Execute motion is to build customers who buy across the stack. Do not use this to pre-qualify prospects. Use it to remind yourself what you are building toward.

### The Buyer

The primary buyer is the VP of IT, Director of Infrastructure, or CTO. In smaller organizations, this might be the sole IT leader reporting to a CFO or COO. They are not a developer (although their teams include developers). They are an infrastructure and operations person who is being asked to do more with less.

The secondary influencer is the CFO or finance leader. Aptum's single-bill, single-portal value proposition resonates here because it simplifies vendor management and provides cost visibility.

---

## What the Ideal Customer Buys: The Full Journey

The ideal customer does not arrive as a managed services buyer. They arrive with a problem. The AM's job is to hear that problem clearly enough to play it back in a way that makes the customer feel understood, and then propose a structured first step from "something is wrong" to "here is exactly what to fix and why."

### The Story: How a Customer Relationship Actually Develops

A mid-market distribution company has been running a substantial on-premises environment for years. At the center of it is a legacy ERP system supported by roughly 15 virtual machines that touch everything from order processing to warehouse fulfillment. The broader environment spans about 100 VMs, with 300 users on the domain and two dedicated connectivity lines feeding into a warehouse floor where availability is not optional.

The business runs lean on IT, and recently it got leaner. Their most critical technical person left without leaving behind passwords, documentation, or a runbook for the environment. The ERP is still running, but the CIO is now managing an environment he cannot fully see. He knows what the system does. He is less certain about what holds it together. That uncertainty sits on top of a spring office move requiring a full network redesign across three locations, a busy season starting in March that makes major changes operationally impossible, and a DR posture that, if tested today, would not pass.

The departure of that one person made something visible that had probably been true for a while. The company was not operating an infrastructure strategy. They were operating a person. When that person left, the CIO and COO looked at what remained and agreed: this could not be how the business continued to run. Aptum was already a trusted provider for the parent company's infrastructure, and the reference held. The conversation became less about a specific project and more about building something that does not depend on who happens to be in the seat.

An Aptum AM, already familiar with the parent company relationship, reaches out. The conversation covers the full situation in 45 minutes. The AM sends a follow-up that plays the story back:

> You have built a distribution operation that moves product reliably, and your infrastructure has largely kept up with that. What is making this harder now is that the environment you built depends on knowledge that walked out the door. The ERP is running, but the team around it is thinner than it should be, and a spring office move is coming whether the infrastructure is ready or not. What the CIO and COO seem to have landed on is that this cannot keep running the way it has been. The question is what a more deliberate model looks like, and whether there is a partner who can help build it before March.

The CIO responds: "That's exactly where we are."

A Salesforce opportunity is created. The proposal is an Infrastructure Risk and Readiness Assessment.

**The Infrastructure Risk and Readiness Assessment (~$15,000)**

The assessment covers the full environment: all 100 VMs catalogued and risk-scored, the ERP environment dependency-mapped so the 15 machines that actually run the business are clearly identified, network architecture reviewed against the office move requirements, and a DR gap analysis tested against the two to three hour RTO. The documentation gap left by the departing engineer gets closed here too. Aptum produces the runbook that should have existed already.

What it produces: a prioritized remediation roadmap, a clear picture of what moves to Aptum infrastructure and what stays, and the evidence base for every commercial conversation that follows. The customer does not need to be convinced they have a problem. The assessment already proved it.

**Execute: Two Phases Driven by the Spring Deadline**

Phase 1 (before March): Migrate the ERP environment to Aptum Dedicated or Private Cloud, properly documented and redundant, with a managed handoff. Network design and hardware refresh across all three locations. DRaaS implemented and tested against the two to three hour RTO before the move happens. (~$75,000 to $150,000 SOW)

Phase 2 (post-move): The remaining VM estate gets rationalized. What moves to hosted infrastructure, what gets decommissioned, what gets backed up and left alone. (~$25,000 to $50,000 SOW)

**Operate: What the Relationship Looks Like Ongoing**

With the ERP environment on Aptum infrastructure, Managed Cloud wraps around it: 24/7 monitoring, OS patching, Managed Backup, and Managed Firewall across the ERP environment. DRaaS provides ongoing tested recovery with a defined RTO. Network management covers all three locations.

The CIO stops being the person who gets called at 2am. The business stops depending on who happens to be sitting in the IT chair.

What the relationship is worth at 12 months: approximately $15,000 in assessment revenue, $100,000 to $200,000 in project revenue, and approximately $8,000 to $9,000/month in managed services MRC across Managed Cloud, DRaaS, and network management.

The customer did not come to Aptum looking for any of this. They came because an AM listened well enough to play their story back to them.

---

### What a Relationship Is Worth

| Stage | Revenue Type | Typical Value |
| --- | --- | --- | --- |
| Assessment (Advisory) | One-time, fixed-fee | $5K to $40K |
| Implementation (Execute) | One-time, SOW-based | $5K to $300K |
| Managed Services (Operate) | Monthly recurring | $15K to $48K/mo |

---

### Quick Reference: What They Say, What to Offer, What They Might Buy

| What You Hear | Assessment to Offer | Products and Services |
| --- | --- | --- |
| "Our servers are 7 years old," "Haven't patched in months," "SAN at 85% capacity" | Infrastructure Risk & Readiness | 24/7 Infrastructure Monitoring, OS Patching, Managed Backup, Hardware Replacement |
| "Our AWS bill doubled but usage is flat," "Paying for stuff we don't use" | Cloud Repatriation | Private Cloud or Shared Cluster via Aptum Portal, OS Patching, Managed Backup, Hybrid Cloud Interconnects |
| "We have stuff everywhere and no one knows what's where," "Hybrid by accident" | Hybrid Cloud | Aptum Portal consolidation, OS Patching, Application Performance Monitoring, Hybrid Cloud Interconnects |
| "Our auditor flagged us," "Firewalls are EOL," "Not sure we'd pass a SOC 2" | Security Posture & Compliance | Managed Firewall, Managed Detection and Response, Compliance Reporting, Vulnerability Scanning |
| "My team spends 80% keeping the lights on," "Can't innovate, always firefighting" | Operational Maturity | OS Patching, Managed Backup, Managed Firewall, Application Performance Monitoring, Managed Detection and Response |
| "We want to do Kubernetes but running on old hardware," "Our CI/CD is manual" | App & Platform Modernization | Kubernetes platform build on Aptum infrastructure, DevOps Monitoring and Maintenance, Application Performance Monitoring |
| "We built our cloud fast and never went back to check," "Performance is inconsistent" | Well-Architected Review | Architecture remediation project, Application Performance Monitoring, Web Application Firewall, Managed Backup |

---

## Where We Are Now: The Portfolio Reality

The dimServices extract (April 1, 2026) tells an honest story about the current customer base.

### Portfolio Summary

| Metric | Value |
| --- | --- |
| Total monthly revenue (USD MRC) | $2,888,901 |
| Total services | 5,581 |
| Unique customers | 773 |
| Datacenters | 26 across 21 cities |

### Managed Services Penetration

Only 6.5% of services have any managed service attached. This compares to an industry norm of 15 to 20% for MSPs in the mid-market. The managed services revenue is approximately $187,639/mo out of $2.89M total. The stacking opportunity is massive and largely untapped.

### Customer Segmentation by Stickiness and Assessment Opportunity

| Segment | Customers | Churn Risk | Primary Assessment Play |
| --- | --- | --- | --- | --- | --- |
| Multi-LOB (hosting + colo + cloud) | 135 | Low | Security Posture or Hybrid Cloud |
| Hosting-only | 429 | High | Infrastructure Risk or Operational Maturity |
| Colocation-only | 93 | Medium | Infrastructure Risk |
| Cloud-only | ~116 | Medium | Well-Architected Review |

The 135 multi-LOB customers are the closest to the ideal ICP. They buy across product lines, generate 62.66% of revenue, and have multiple integration points that make switching costly. The assessment play for this segment is about deepening: adding the security layer, adding the app platform layer, adding business continuity.

The 429 hosting-only customers represent the honest conversation the team needs to have. Many of these are legacy Peer One customers who have stayed because inertia is cheaper than migration. They are paying for commodity infrastructure without managed services layered on top. They are price-sensitive and will leave when they find something cheaper. The assessment play for this segment is triage: use Infrastructure Risk or Operational Maturity assessments on accounts that have the profile to become ICP-fit, and accept that the remainder will attrit over time.

### The Honest Assessment: Customers Who Don't Fit the ICP

The portfolio includes a meaningful number of customers who do not fit the ideal profile. This is not a judgment on those customers. It is a recognition that chasing retention on commodity-only accounts is a different motion than building deep managed services relationships.

Examples of customers who sit outside the ICP:

A significant portion of the portfolio carries legacy-only customers with no managed services attached. This revenue is structurally at risk.

The response is not to abandon these customers. It is to:

1. Run Infrastructure Risk or Operational Maturity assessments on the accounts that have the profile to become ideal customers (overwhelmed IT teams, hybrid workloads, compliance needs). The assessment produces the evidence that justifies the managed services investment.
1. Accept that some portion of this base will attrit over time as they find commodity infrastructure cheaper elsewhere.
1. Build the new logo pipeline against the ICP using the assessment framework so that as legacy accounts attrit, they are backfilled with customers who fit the profile and buy across the stack.

This is what "it wasn't meant to be forever" looks like operationally.

---

## How Customers Enter the Relationship

Customers arrive from five origins: on-premises with aging hardware, hyperscaler with rising costs, hybrid sprawl, compliance pressure, and platform modernization needs. Each origin maps to a specific assessment entry point and lands on a specific engagement tier. For the full path detail, see the [Managed Services Catalog](https://aptum.atlassian.net/wiki/spaces/PRD/pages/5257560095/Managed+Services+Catalog).

---

## Geographic Focus

### Where to Hunt

For new logo acquisition against the ICP:

| Region | Rationale | Assessment Entry Point |
| --- | --- | --- |
| Greater Toronto / Southern Ontario | Largest existing base, Canadian data sovereignty, proximity to Pullman DC (Aptum Portal/IaaS primary site) | Infrastructure Risk, Cloud Repatriation (Canadian data sovereignty angle) |
| US East Coast (Virginia, Atlanta, Miami) | Existing DC presence, large mid-market population, Miami specifically for LatAm-adjacent demand | Hybrid Cloud, Cloud Repatriation, Operational Maturity |
| UK (Portsmouth + London) | Existing customer base, but constrained by facility situation. Selective. | Infrastructure Risk (existing base renewal + upsell) |

For MSP/reseller channel (secondary):

| Region | Rationale |
| --- | --- |
| Regional MSPs in DC footprint cities | MSPs squeezed by Broadcom who need a private cloud partner. ES Williams/Ignite pattern validates this. |
| LatAm-adjacent via Miami | Latitude.sh + Megaport intersection, as discussed in product discussion |

---

---

## Market Tailwinds Supporting This ICP

Several market forces are pulling mid-market companies toward exactly the profile described above:

The Broadcom/VMware disruption is real and ongoing. Gartner estimates 35% of VMware workloads will migrate by 2028. Forrester projects VMware's largest 2,000 customers will shrink deployments by 40%. These organizations need somewhere to go, and Aptum's CloudStack and Proxmox alternatives, delivered through Aptum Portal with managed services layered on top, are a direct answer. The Hybrid Cloud Assessment and Cloud Repatriation Assessment are the specific tools that start this conversation.

Cloud repatriation is accelerating. Andreessen Horowitz's "Cost of Cloud" research and the 37signals case study ($7M savings over 5 years from their cloud exit) have given mid-market CFOs permission to question their hyperscaler bills. 21% of surveyed organizations have repatriated workloads. Aptum's ability to provide private cloud with a public-cloud-like portal experience (through Aptum Portal) positions it as the repatriation destination. The Cloud Repatriation Assessment is designed to capitalize on this trend with a structured business case methodology.

---

## Using This ICP

### For Sales (New Logo)

The ideal first conversation is an assessment. It maps the customer's environment, builds the technical knowledge to have a credible follow-on conversation, and produces the evidence that justifies the investment in managed services. It starts the relationship.

The StoryLeader methodology maps to three narrative questions that guide assessment selection:

| StoryLeader Question | Customer Pain | Assessment to Offer |
| --- | --- | --- |
| "What are you dealing with right now?" | Aging infra, security gaps, operational burden | Infrastructure Risk, Security Posture |
| "Where do you want to be?" | Cloud strategy, platform modernization, architecture optimization | Hybrid Cloud, Cloud Repatriation, Platform Modernization, Well-Architected Review |
| "What's holding you back?" | IT team capacity, operational immaturity, technical debt | Operational Maturity, Infrastructure Risk, Security Posture |

Qualification questions for new opportunities:

1. How many people are on your IT team? (Target: 2 to 15)
1. Where are your workloads running today? (Target: hybrid, on-prem + at least one hyperscaler)
1. Are you running VMware? When is your next renewal? (Broadcom pressure = urgency)
1. Who manages your backups, patching, and security monitoring today? (If "we do, barely," they fit the ICP)
1. Do you have compliance requirements? (SOC 2, PCI, HIPAA = Security Posture Assessment opportunity)
1. What is your monthly cloud spend? Is it growing faster than your usage? (Cloud Repatriation opportunity)
1. What would it cost your business if your infrastructure went down for 4 hours? (Infrastructure Risk framing)

### For Account Management (Existing Base)

Use the managed services stacking model to score existing customers against the ICP. The assessment framework provides the mechanism for the upsell conversation:

- The 135 multi-LOB customers are the immediate targets for Security Posture and Hybrid Cloud assessments. They already buy across product lines; the assessment identifies the next layer to add.
- The 429 hosting-only customers should be triaged using Infrastructure Risk or Operational Maturity assessments on accounts with ICP-fit potential. The assessment either produces a roadmap to managed services (the customer becomes ICP-fit) or confirms that the account is a pure commodity buyer (accept future attrition).
- Every renewal conversation in the 72.74% expiring-within-6-months window should include an assessment offer as the conversation opener.

### For Product and Engineering

Everything that makes Aptum Portal more visible to the customer (monitoring dashboards, backup status, patch compliance, ticket integration) deepens the managed services relationship and increases switching cost. Portal visibility for Layers 1 and 2 is the highest-impact work for customer retention.

The assessment framework creates a secondary requirement: assessment findings should eventually be trackable in the Aptum Portal. When a customer completes a Security Posture Assessment and then purchases managed detection and response, the portal should show the connection between the finding and the remediation.

---

## What This ICP Excludes (And Why That's OK)

Large enterprises with 10,000+ employees and IT departments 3x the size of Aptum. They will engage for consulting but will not sustainably buy managed services from a company Aptum's size. Ian Rae was direct about this: "That's not gonna happen." Note: these customers may still be valid Advisory (assessment) customers, particularly for the executive dinner campaigns targeting high cloud spend. The assessment is valuable to them even if they don't become managed services customers.

Pure commodity buyers looking for the cheapest dedicated server. The portfolio has many of these. They generate revenue today but will leave when they find cheaper. The backfill strategy is to replace them with ICP-fit customers over time.

Hyperscaler-native companies with no on-premises footprint. If all their workloads are in AWS/Azure/GCP and they have no interest in private infrastructure, Aptum's core differentiation (hybrid cloud, infrastructure + managed services stacking) doesn't apply. Exception: if they are experiencing cloud cost pressure, the Cloud Repatriation Assessment may open the door.

Very small businesses below $5K/mo MRC potential. The economics of managed services delivery don't support full stacking at this scale. Exception: MSP/reseller customers who aggregate many small businesses into a single Aptum relationship (the ES Williams/Ignite model).

---

*Sources: dimServices extract (April 1, 2026), Aptum Identity & Values (Confluence, Marketing space), Aptum Messaging (Confluence, Marketing space), Product Strategy v1.3.1 (Confluence, treated as historical), Product Discussion transcript (March 31, 2026), [Aptum Product Strategy](https://aptum.atlassian.net/wiki/spaces/PRD/pages/5257461765/Aptum+Product+Strategy) v2.1, [Managed Services Catalog](https://aptum.atlassian.net/wiki/spaces/PRD/pages/5257560095/Managed+Services+Catalog), [AptCloud - Aptum IaaS Strategy](https://aptum.atlassian.net/wiki/spaces/PRD/pages/5257494536/AptCloud+-+Aptum+IaaS+Strategy), Service Team descriptions, STG Assessment & Commercial Playbook v1.0 (7 assessments, engagement workflow, revenue model, success metrics, post-assessment pathways, customer-to-assessment matrix).*
