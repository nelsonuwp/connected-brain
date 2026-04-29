# Aptum Ideal Customer Profile

## Single Unified ICP, Grounded in Portfolio Data

**Version 2.1 | April 28, 2026**

---

## Why a Single ICP

The earlier Product Strategy v1.3.1 ([Confluence page](https://aptum.atlassian.net/wiki/spaces/Product/pages/3376513043/Product+Strategy+v1.3.1)) defined two ICPs: one for infrastructure buyers and one for digital natives with 7+ developers. The board directed the team to consolidate to a single ICP. Ian Rae put it simply in the March 31, 2026 product discussion: "We're a mid-market company selling to mid-market."

This document defines one Ideal Customer Profile. It also defines what an ideal customer is not, using real portfolio data to show where the current customer base aligns and where it diverges. It integrates the assessment framework as the qualification and onboarding mechanism: the way Aptum determines whether a prospect fits the ICP, builds the relationship, and funnels the customer into the managed services and infrastructure stack.

The ICP also reflects the brand promise that anchors product strategy. Aptum's brand commits to the right workload on the right platform, the right expertise at the right time, and your cloud, your way. The ideal customer is one who values that proposition: someone with workloads that genuinely belong on different platforms, the operational maturity to want a partner instead of a single vendor, and the willingness to pay for managed services that are demonstrably better than what they could do in-house.

---

## The Ideal Customer

### Company Profile

The ideal Aptum customer is a mid-market organization, typically between 50 and 2,000 employees, generating $10M to $500M in annual revenue. They are digitally dependent (their revenue flows through technology) but technology is not their core business. They are running a mix of workloads across on-premises infrastructure and at least one hyperscaler, and they are feeling the pain of managing that complexity.

They are most commonly found in these verticals: SaaS/digital platforms, eCommerce, financial services, healthcare/life sciences, professional services, and media/content delivery. They are headquartered in or have meaningful operations in North America (Canada and US East Coast especially), with secondary presence in the UK.

### Firmographic Anchors


| Attribute            | Ideal Range                                 | Why                                                                                                                      |
| -------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Employee count       | 50 to 2,000                                 | Large enough to have real infrastructure needs, small enough that their IT team (2 to 15 people) needs a partner         |
| Annual revenue       | $10M to $500M                               | Budget exists for managed services, but they aren't large enough to build everything internally                          |
| IT team size         | 2 to 15 people                              | This is the sweet spot. Overwhelmed, stretched thin, doing too many things. They need a safety net.                      |
| Infrastructure spend | $10K to $100K/mo MRC                        | Below $10K the economics don't work for managed services stacking. Above $100K they typically have in-house capability.  |
| Cloud maturity       | Hybrid (on-prem + at least one hyperscaler) | Pure cloud-native companies won't need Aptum's infrastructure. Pure on-prem companies aren't ready for the conversation. |


### Behavioral Indicators

The ideal customer exhibits one or more these patterns:

They have workloads they cannot or will not move to a hyperscaler. This could be for cost reasons (they've done the math and repatriation makes sense), regulatory reasons (data sovereignty, compliance requirements), performance reasons (latency-sensitive applications), or inertia reasons (legacy applications that would cost more to re-architect than to host).

They are running a VMware estate and feeling Broadcom's licensing pressure. The 300 to 1,050% price increases validated by Gartner are real, and these customers are actively looking for alternatives. Aptum's CloudStack and Proxmox options are directly relevant.

They consume multiple product types. The portfolio data is clear on this: multi-product customers generate 94.46% of Aptum's revenue while representing 63.9% of the customer base. The average multi-LOB customer generates 2.8x the revenue of a single-LOB customer and churns at a materially lower rate.

They value the relationship over the commodity. They want a partner who understands their environment, not just a provider who racks a server. The consulting engagement is the start of the relationship, not the end of it.

### The Buyer

The primary buyer is the VP of IT, Director of Infrastructure, or CTO. In smaller organizations, this might be the sole IT leader reporting to a CFO or COO. They are not a developer (although their teams include developers). They are an infrastructure and operations person who is being asked to do more with less.

The secondary influencer is the CFO or finance leader. Aptum's single-bill, single-portal value proposition resonates here because it simplifies vendor management and provides cost visibility.

---

## Assessment-Based Qualification

The assessment framework replaces the traditional qualification checklist with a structured diagnostic that simultaneously validates ICP fit and builds the relationship. Instead of asking "does this prospect fit our ICP?" in the abstract, the AE offers a specific assessment that tests the hypothesis while delivering value.

### ICP Signals and Assessment Mapping

Each behavioral indicator maps to a specific assessment. The assessment validates the signal, quantifies the opportunity, and produces the evidence base for the commercial conversation.


| ICP Signal                         | What You Hear                                                                                            | Assessment to Offer             | What It Validates                                                                                  |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------- | -------------------------------------------------------------------------------------------------- |
| Aging infrastructure               | "Our servers are 7 years old," "We haven't patched in months," "Our SAN is at 85% capacity"              | Infrastructure Risk & Readiness | Whether the customer has enough technical debt to justify hardware refresh + managed services      |
| Cloud cost pressure                | "Our AWS bill doubled but usage is flat," "We're paying for stuff we don't use"                          | Cloud Repatriation              | Whether workloads are portable and whether the savings justify repatriation to Aptum IaaS          |
| Hybrid sprawl                      | "We have stuff everywhere and no one knows what's where," "We're hybrid by accident"                     | Hybrid Cloud                    | Whether the customer has enough workload complexity to benefit from Aptum Portal consolidation     |
| Security/compliance gaps           | "Our auditor flagged us," "Our firewalls are EOL," "We're not sure we'd pass a SOC 2 audit"              | Security Posture & Compliance   | Whether the customer has compliance obligations that require ongoing managed security services     |
| Overwhelmed IT team                | "My team spends 80% of their time keeping the lights on," "We can't innovate because we're firefighting" | Operational Maturity            | Whether the customer's operational burden is large enough to justify a managed services transition |
| Platform ambitions on legacy infra | "We want to do Kubernetes but we're running on 7-year-old hardware," "Our CI/CD is manual"               | App & Platform Modernization    | Whether the customer's application architecture is ready for platform modernization on Aptum infra |
| Unreviewed cloud estate            | "We built our AWS environment fast and never went back to check," "Performance is inconsistent"          | Well-Architected Review         | Whether the customer's cloud estate has optimization and governance opportunities                  |


### The Assessment as Qualification Tool

The assessment does three things simultaneously:

1. It validates ICP fit. A customer who pays $5K to $40K for a structured assessment of their environment is demonstrating willingness to invest, recognition that they need help, and trust in Aptum's expertise. These are the behavioral markers of an ICP-fit customer.
2. It maps the environment. The assessment deliverable is a detailed picture of the customer's infrastructure, applications, security posture, operational model, or cloud estate. This is the information the commercial team needs to scope the Execute and Operate phases. It replaces weeks of free pre-sales discovery with a paid engagement.
3. It produces the business case. The assessment report includes findings, risk scores, and a remediation roadmap with cost estimates. This is the sales tool for the next motion. The customer doesn't need to be "sold" on managed services; the assessment has already demonstrated why they need them.

### Qualification Questions by Assessment Type

**Infrastructure Risk & Readiness (broadest entry point, fits nearly all ICP accounts):**

1. How old is your server estate? When was the last hardware refresh?
2. What operating systems are you running? Are any end-of-life or unsupported?
3. Who handles patching today? How often does it actually happen?
4. What would a 4-hour outage cost your business?
5. Do you have a capacity plan for the next 12 months?

**Cloud Repatriation (highest follow-on value, $200K-$1M+ TCV):**

1. What is your monthly cloud spend? Which providers?
2. Has your cloud bill grown faster than your usage?
3. Which workloads have predictable, steady-state resource consumption?
4. What cloud-native services are you using that would need to be replaced?
5. When does your current cloud contract renew?

**Hybrid Cloud (broadest cloud-related entry point):**

1. How many applications do you run? Where do they live?
2. Are you "hybrid by accident" or "hybrid by design"?
3. What compliance or data sovereignty requirements apply?
4. Have you done a TCO comparison of your current hybrid setup?
5. How many IT teams manage different parts of the environment?

**Security Posture & Compliance (regulated industry entry point):**

1. What compliance frameworks apply to your business? (SOC 2, PCI, HIPAA, etc.)
2. When was your last security assessment or penetration test?
3. Are any of your firewalls or security appliances end-of-life?
4. Who monitors for security incidents today? Do you have 24/7 coverage?
5. Have you had any audit findings in the last 12 months?

**Operational Maturity (stickiest recurring revenue outcome):**

1. How many people are on your IT team?
2. What percentage of their time goes to reactive operations vs. planned work?
3. Who gets the 2 AM call when something goes down?
4. Do you have documented runbooks for your critical processes?
5. What monitoring and ticketing tools are you using?

**App & Platform Modernization (developer-adjacent entry point):**

1. How many applications do you maintain? How do you deploy them?
2. Are you using containers or Kubernetes today?
3. How many development teams do you have? Do they share tooling and practices?
4. What is your biggest deployment frustration?
5. How long does it take to go from code commit to production?

**Well-Architected Review (cloud-native entry point):**

1. When was the last time your AWS/Azure environment was formally reviewed?
2. What are your biggest cloud cost concerns?
3. Have you experienced performance issues or outages related to architecture?
4. How do you manage IAM and access control?
5. Do you have a disaster recovery plan that has been tested?

---

## What the Ideal Customer Buys: The Full Journey

The ideal customer does not arrive as a managed services buyer. They arrive with a problem. The assessment framework defines the entry points and the journey from problem to long-term relationship.

### The Customer Journey

```
AWARENESS                    ASSESSMENT                   EXECUTE                      OPERATE
(Pain signal)         -->    (Advisory engagement)  -->   (Implementation project) --> (Managed services)
"Our servers are old"        Infrastructure Risk          Hardware refresh             L1+L2: Monitoring
"Cloud bill is insane"       Cloud Repatriation           Repatriation project         + Managed OS
"We failed our audit"        Security Posture             Security remediation         L4: Security
"Team is drowning"           Operational Maturity         Managed services transition  L2-L5: Full stack
```

### Revenue by Journey Stage


| Stage                      | Revenue Type        | Typical Value   | Margin                                            |
| -------------------------- | ------------------- | --------------- | ------------------------------------------------- |
| Assessment (Advisory)      | One-time, fixed-fee | $5K to $40K     | 50-65% (SA labor + specialist time)               |
| Implementation (Execute)   | One-time, SOW-based | $5K to $300K    | 25-35% (cross-functional labor, partner services) |
| Managed Services (Operate) | Monthly recurring   | $15K to $48K/mo | 50-60% blended                                    |


A fully engaged ideal customer generates $15,000 to $48,000/mo in MRC. The blended margin is 50 to 60%, compared to 70 to 80% for infrastructure-only, but the absolute margin dollars are 2 to 3x higher and the customer is deeply embedded.

### What They Buy by Layer


| Layer                        | What They Buy                                                                                                  | Assessment That Drives It                                     | Monthly Value     |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | ----------------- |
| Infrastructure commodity     | VPC, Dedicated Cloud, Private Cloud, or hyperscaler subscription through Aptum Portal                          | Hybrid Cloud, Cloud Repatriation, Infrastructure Risk         | $7,000 to $25,000 |
| Layer 2: Managed OS          | OS patching, managed backup, managed firewall, endpoint security                                               | Infrastructure Risk, Operational Maturity, Security Posture   | +$2,000 to $5,000 |
| Layer 3: App Platform        | Application performance monitoring, web application firewall, DDoS protection, load balancing, database tuning | Platform Modernization, Well-Architected Review, Hybrid Cloud | +$3,000 to $8,000 |
| Layer 4: Security            | Managed detection and response, compliance reporting, vulnerability scanning                                   | Security Posture                                              | +$2,000 to $5,000 |
| Layer 5: Business Continuity | DRaaS, hybrid interconnects, managed productivity (M365), managed DNS                                          | Hybrid Cloud, Cloud Repatriation                              | +$1,500 to $5,000 |


---

## Where We Are Now: The Portfolio Reality

The dimServices extract (April 1, 2026) tells an honest story about the current customer base.

### Portfolio Summary


| Metric                          | Value               |
| ------------------------------- | ------------------- |
| Total monthly revenue (USD MRC) | $2,888,901          |
| Total services                  | 5,581               |
| Unique customers                | 773                 |
| Datacenters                     | 26 across 21 cities |


### Revenue Composition


| Line of Business      | USD MRC    | Share  |
| --------------------- | ---------- | ------ |
| Hosting               | $2,171,402 | 75.16% |
| Colocation            | $642,193   | 22.23% |
| Cloud Services        | $74,168    | 2.57%  |
| Professional Services | $1,138     | 0.04%  |


Three quarters of revenue comes from hosting, which is predominantly commodity dedicated servers. Cloud services represent just 2.57% of the portfolio. This is the gap the product strategy needs to close.

### Customer Concentration


| Segment                                             | Revenue    | Share  |
| --------------------------------------------------- | ---------- | ------ |
| Top 10 customers                                    | $1,229,170 | 42.55% |
| Top 20 customers                                    | $1,500,979 | 51.96% |
| Top 50 customers                                    | $1,913,545 | 66.24% |
| Single largest customer (Basis Global Technologies) | $425,740   | 14.74% |


This concentration is a structural risk. One customer walking would remove nearly 15% of total MRC.

### Managed Services Penetration

Only 6.5% of services have any managed service attached. This compares to an industry norm of 15 to 20% for MSPs in the mid-market. The managed services revenue is approximately $187,639/mo out of $2.89M total. The stacking opportunity is massive and largely untapped.

### Customer Segmentation by Stickiness and Assessment Opportunity


| Segment                            | Customers | Revenue    | Share  | Churn Risk | Primary Assessment Play                                                                  |
| ---------------------------------- | --------- | ---------- | ------ | ---------- | ---------------------------------------------------------------------------------------- |
| Multi-LOB (hosting + colo + cloud) | 135       | $1,810,044 | 62.66% | Low        | Security Posture or Hybrid Cloud (deepen the relationship, add layers)                   |
| Hosting-only                       | 429       | $659,075   | 22.81% | High       | Infrastructure Risk or Operational Maturity (create stickiness through managed services) |
| Colocation-only                    | 93        | $401,994   | 13.92% | Medium     | Infrastructure Risk (assess what they're running in our racks, offer to manage it)       |
| Cloud-only                         | ~116      | $17,788    | 0.62%  | Medium     | Well-Architected Review (optimize their cloud, open managed services conversation)       |


The 135 multi-LOB customers are the closest to the ideal ICP. They buy across product lines, generate 62.66% of revenue, and have multiple integration points that make switching costly. The assessment play for this segment is about deepening: adding the security layer, adding the app platform layer, adding business continuity.

The 429 hosting-only customers represent the honest conversation the team needs to have. Many of these are legacy Peer One customers who have stayed because inertia is cheaper than migration. They are paying for commodity infrastructure without managed services layered on top. They are price-sensitive and will leave when they find something cheaper. The assessment play for this segment is triage: use Infrastructure Risk or Operational Maturity assessments on accounts that have the profile to become ICP-fit, and accept that the remainder will attrit over time.

### The Honest Assessment: Customers Who Don't Fit the ICP

The portfolio includes a meaningful number of customers who do not fit the ideal profile. This is not a judgment on those customers. It is a recognition that chasing retention on commodity-only accounts is a different motion than building deep managed services relationships.

Examples of customers who sit outside the ICP:


| Customer                  | MRC      | Profile                                                 | Why They Don't Fit                                                                                                                    |
| ------------------------- | -------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Basis Global Technologies | $425,740 | Single product (dedicated hosting), no managed services | Largest single customer by far, but zero stickiness. If they find dedicated hosting cheaper elsewhere, there is nothing binding them. |
| ResearchGATE GmbH         | $226,038 | Single product (dedicated hosting), no managed services | Same pattern. High revenue, low integration, high flight risk.                                                                        |


There are 320 legacy-only customers generating $1,279,974/mo (44.31% of the portfolio) with zero managed services attached. This revenue is structurally at risk.

The response is not to abandon these customers. It is to:

1. Run Infrastructure Risk or Operational Maturity assessments on the accounts that have the profile to become ideal customers (overwhelmed IT teams, hybrid workloads, compliance needs). The assessment produces the evidence that justifies the managed services investment.
2. Accept that some portion of this base will attrit over time as they find commodity infrastructure cheaper elsewhere.
3. Build the new logo pipeline against the ICP using the assessment framework so that as legacy accounts attrit, they are backfilled with customers who fit the profile and buy across the stack.

This is what "it wasn't meant to be forever" looks like operationally.

---

## Customer Origins and Assessment Entry Points

The ICP describes who the customer is. The assessment framework defines how they enter the relationship. Customers arrive from different origins, and each origin maps to a different assessment entry point.

### Origin 1: On-Premises (Non-Aptum Infrastructure)

These are organizations running their own servers, either in their own facilities or in third-party colocation. They have aging hardware, overwhelmed IT teams, and deferred maintenance. They are not yet Aptum customers or they are Aptum colo customers whose equipment Aptum does not manage.

**Entry assessments:** Infrastructure Risk & Readiness, Operational Maturity

**What the assessment reveals:** EOL hardware inventory, unsupported OS versions, single points of failure, capacity constraints, the true cost of self-managed operations (staff time, downtime risk, opportunity cost).

**Funnel path:** Assessment findings justify hardware refresh or migration to Aptum IaaS (VPC or Private Cloud). The migration project (Execute) moves the workloads. Managed services (Operate) take over day-2 operations. The customer moves from self-managed on-prem to Aptum-managed hybrid.

**Expected journey revenue:** $5K-$20K assessment, $25K-$150K migration project, $5K-$15K/mo ongoing managed services.

### Origin 2: Hyperscaler (Pulled Back to Aptum Services)

These are organizations that moved to AWS, Azure, or GCP and are now experiencing cost pressure, complexity, or regret. Their cloud bills have grown faster than their usage. They have workloads with predictable resource consumption that don't benefit from hyperscaler elasticity. They may have data sovereignty concerns.

**Entry assessments:** Cloud Repatriation, Well-Architected Review

**What the assessment reveals:** Cloud spend breakdown by service/region/workload, workload portability scores (highly portable, moderately portable, low portability, not recommended for repatriation), TCO comparison across scenarios (status quo, selective repatriation, aggressive repatriation, hybrid optimized), break-even analysis.

**Funnel path:** Assessment builds the financial business case. The repatriation project (Execute) moves selected workloads to Aptum Private Cloud. Managed services (Operate) provide the operational capability the customer would lose by leaving the hyperscaler. The customer retains hyperscaler for workloads that genuinely benefit from it (managed through Aptum Portal) and runs cost-predictable workloads on Aptum IaaS.

**Expected journey revenue:** $10K-$35K assessment, $50K-$300K repatriation project, $10K-$50K/mo ongoing managed services. This is the highest-value customer journey in the portfolio ($200K-$1M+ TCV).

### Origin 3: Hybrid-by-Accident (Rationalization)

These are organizations that have sprawled across on-prem, colo, and one or more hyperscalers without a deliberate strategy. They have workloads in multiple places, multiple management planes, inconsistent security posture, and no single view of their estate. They are "hybrid by accident, not by design."

**Entry assessments:** Hybrid Cloud, Security Posture & Compliance

**What the assessment reveals:** Complete workload inventory with dependency mapping, suitability scoring for each workload (best fit: on-prem, private cloud, public cloud, SaaS), TCO modeling across placement scenarios, security and compliance gaps across environments.

**Funnel path:** Assessment produces a rationalization roadmap. Architecture consulting (Execute) designs the target state. Migration projects move workloads to optimal placement. Managed services (Operate) provide consistent operational coverage across all environments through Aptum Portal.

**Expected journey revenue:** $7.5K-$40K assessment, $30K-$200K architecture + migration, $8K-$25K/mo ongoing managed services.

### Origin 4: Compliance-Driven

These are organizations in regulated industries (healthcare, financial services, government, education) that have compliance obligations driving their infrastructure decisions. They may have received audit findings, experienced a security incident, or simply recognized that their security posture is inadequate.

**Entry assessments:** Security Posture & Compliance

**What the assessment reveals:** EOL/EOS device inventory with CVE mapping, firewall rule audit, compliance gap analysis against specific frameworks (SOC 2, HIPAA, PCI-DSS), penetration testing results (L/XL engagements), remediation priority matrix with cost/effort estimates.

**Funnel path:** Assessment findings drive security remediation project (Execute): firewall replacement, OS upgrades, hardening, compliance alignment. Managed security services (Operate) provide ongoing protection: managed detection and response, managed firewall, compliance reporting, vulnerability scanning. The customer can't go back to self-managed security because the assessment demonstrated the gap.

**Expected journey revenue:** $5K-$30K assessment, $20K-$100K remediation project, $5K-$17K/mo ongoing managed security services.

### Origin 5: Platform Modernizers

These are organizations with modern application ambitions on legacy infrastructure. They want containers, Kubernetes, CI/CD pipelines, and modern deployment patterns, but they are running on aging hardware with manual processes. Their development teams are productive, but their infrastructure and deployment tooling are holding them back.

**Entry assessments:** App & Platform Modernization

**What the assessment reveals:** Application architecture review, container/K8s readiness evaluation per application, CI/CD maturity assessment (with DORA metrics where possible), platform architecture review, technology stack recommendations.

**Funnel path:** Assessment produces a modernization roadmap. Platform build project (Execute) implements Kubernetes, CI/CD pipeline, and container platform on Aptum infrastructure. Managed platform services (Operate) provide ongoing cluster management, monitoring, and DevOps support.

**Expected journey revenue:** $5K-$35K assessment, $30K-$150K platform build, $8K-$25K/mo managed platform services.

---

## Geographic Focus

### Where the Revenue Is Today


| City           | Services | USD MRC  | Share  |
| -------------- | -------- | -------- | ------ |
| Toronto        | 1,040    | $601,775 | 20.83% |
| Herndon (IAD2) | 1,307    | $592,257 | 20.50% |
| Portsmouth     | 927      | $547,787 | 18.96% |
| Miami          | 547      | $300,870 | 10.41% |
| Los Angeles    | 529      | $300,823 | 10.41% |
| Atlanta        | 554      | $279,354 | 9.67%  |
| London         | 109      | $69,572  | 2.41%  |
| Vancouver      | 88       | $49,076  | 1.70%  |


The top three cities represent 60.29% of revenue. Toronto and Herndon/Virginia are the strongest bases. Portsmouth has capacity but the facility has a known end-of-life constraint (the building owner plans to redevelop). Miami has recently been extended and is the strongest candidate for regional growth, particularly for the Latitude.sh and Megaport partnership.

### Where to Hunt

For new logo acquisition against the ICP:


| Region                                   | Rationale                                                                                                  | Assessment Entry Point                                                    |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Greater Toronto / Southern Ontario       | Largest existing base, Canadian data sovereignty, proximity to Pullman DC (Aptum Portal/IaaS primary site) | Infrastructure Risk, Cloud Repatriation (Canadian data sovereignty angle) |
| US East Coast (Virginia, Atlanta, Miami) | Existing DC presence, large mid-market population, Miami specifically for LatAm-adjacent demand            | Hybrid Cloud, Cloud Repatriation, Operational Maturity                    |
| UK (Portsmouth + London)                 | Existing customer base, but constrained by facility situation. Selective.                                  | Infrastructure Risk (existing base renewal + upsell)                      |


For MSP/reseller channel (secondary):


| Region                               | Rationale                                                                                              |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| Regional MSPs in DC footprint cities | MSPs squeezed by Broadcom who need a private cloud partner. ES Williams/Ignite pattern validates this. |
| LatAm-adjacent via Miami             | Latitude.sh + Megaport intersection, as discussed in product discussion                                |


---

## Contract Risk Context

The portfolio has a near-term contract renewal concentration that requires attention:


| Contract Window          | Services | Revenue    | Share  |
| ------------------------ | -------- | ---------- | ------ |
| Expiring within 6 months | 4,340    | $2,101,324 | 72.74% |
| Expiring 6 to 12 months  | 151      | $135,147   | 4.68%  |
| Expiring 12 to 24 months | 348      | $259,615   | 8.99%  |
| 24+ months remaining     | 735      | $382,521   | 13.24% |


72.74% of revenue by value is within 6 months of contract expiration. This is the window during which every renewal conversation should include an assessment offer. Each renewal is an opportunity to move a customer closer to (or further from) the ICP.

The assessment framework makes this operationally concrete: every renewal in the pipeline should be tagged with a primary assessment recommendation. The assessment offer at renewal shifts the conversation from "here's your renewal pricing" to "before we renew, let us show you what we found in your environment and what we can do about it."

---

## Market Tailwinds Supporting This ICP

Several market forces are pulling mid-market companies toward exactly the profile described above:

The Broadcom/VMware disruption is real and ongoing. Gartner estimates 35% of VMware workloads will migrate by 2028. Forrester projects VMware's largest 2,000 customers will shrink deployments by 40%. These organizations need somewhere to go, and Aptum's CloudStack and Proxmox alternatives, delivered through Aptum Portal with managed services layered on top, are a direct answer. The Hybrid Cloud Assessment and Cloud Repatriation Assessment are the specific tools that start this conversation.

Cloud repatriation is accelerating. Andreessen Horowitz's "Cost of Cloud" research and the 37signals case study ($7M savings over 5 years from their cloud exit) have given mid-market CFOs permission to question their hyperscaler bills. 21% of surveyed organizations have repatriated workloads. Aptum's ability to provide private cloud with a public-cloud-like portal experience (through Aptum Portal) positions it as the repatriation destination. The Cloud Repatriation Assessment is designed to capitalize on this trend with a structured business case methodology.

The Canadian cloud market is growing at 17.3% CAGR, reaching an estimated $121.6B by 2030. Canadian data sovereignty requirements continue to tighten. Aptum's Toronto DC presence and Canadian identity are meaningful differentiators.

The global managed services market is projected at $400B by 2025, growing at 10 to 15% CAGR. The specific segment Aptum operates in (hybrid cloud managed services for mid-market) is growing faster than the market average.

---

## Using This ICP

### For Sales (New Logo)

The ideal first conversation is an assessment. This is the tip of the spear. It builds trust, maps the customer's environment, and creates the technical intimacy that leads to infrastructure and managed services revenue. It is the start of the relationship, not the end.

The StoryLeader methodology maps to three narrative questions that guide assessment selection:


| StoryLeader Question                   | Customer Pain                                                     | Assessment to Offer                                                               |
| -------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| "What are you dealing with right now?" | Aging infra, security gaps, operational burden                    | Infrastructure Risk, Security Posture                                             |
| "Where do you want to be?"             | Cloud strategy, platform modernization, architecture optimization | Hybrid Cloud, Cloud Repatriation, Platform Modernization, Well-Architected Review |
| "What's holding you back?"             | IT team capacity, operational immaturity, technical debt          | Operational Maturity, Infrastructure Risk, Security Posture                       |


Qualification questions for new opportunities:

1. How many people are on your IT team? (Target: 2 to 15)
2. Where are your workloads running today? (Target: hybrid, on-prem + at least one hyperscaler)
3. Are you running VMware? When is your next renewal? (Broadcom pressure = urgency)
4. Who manages your backups, patching, and security monitoring today? (If "we do, barely," they fit the ICP)
5. Do you have compliance requirements? (SOC 2, PCI, HIPAA = Security Posture Assessment opportunity)
6. What is your monthly cloud spend? Is it growing faster than your usage? (Cloud Repatriation opportunity)
7. What would it cost your business if your infrastructure went down for 4 hours? (Infrastructure Risk framing)

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

*Sources: dimServices extract (April 1, 2026), Aptum Identity & Values (Confluence, Marketing space), Aptum Messaging (Confluence, Marketing space), Product Strategy v1.3.1 (Confluence, treated as historical), Product Discussion transcript (March 31, 2026), `/53-products/aptum-product-strategy.md` v2.1, `/53-products/managed-services-catalog.md`, `/53-products/aptcloud-aptum-iaas/AptCloud_Aptum_IaaS_Strategy.md` (file path pending rename), Service Team descriptions, STG Assessment & Commercial Playbook v1.0 (7 assessments, engagement workflow, revenue model, success metrics, post-assessment pathways, customer-to-assessment matrix).*