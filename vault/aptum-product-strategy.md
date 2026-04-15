# Aptum Product Strategy
## From Commodity Hosting to Hybrid Cloud Managed Services
**Version 2.0 | April 1, 2026**

---

## The Position

Aptum is a hybrid cloud managed services provider. The aspiration is to be the company that makes infrastructure disappear into the background for mid-market organizations, so they can focus on their business instead of managing servers, patching operating systems, and arguing about firewall rules.

The company has two core assets that make this possible:

1. Apt Cloud (the portal, the control plane, the customer experience). Powered by CloudOps Software (formerly CloudMC). This is what the customer sees and touches. It delivers self-service provisioning, cost visibility, lifecycle management, and will increasingly surface the managed services the customer is paying for.

2. Aptum IaaS (the infrastructure). Compute, storage, networking on Apache CloudStack 4.22 with KVM virtualization. Delivered as VPC (multi-tenant shared hosts), Dedicated Cloud (single-tenant dedicated hosts, KVM/CloudStack), and Private Cloud (dedicated hosts with VMware or Proxmox, not necessarily through Apt Cloud portal). This is the foundation that replaces commodity dedicated hosting and offers an alternative to hyperscaler infrastructure at better economics.

These two assets, combined with operational teams that manage everything from the physical rack to the application layer, are what lets Aptum sell managed outcomes rather than just infrastructure components.

---

## Where We Are Today: The Revenue Picture

The current portfolio (dimServices extract, April 1, 2026) reveals the gap between where the revenue is and where the strategy says it should be.

### Revenue by Line of Business

| Line of Business | USD MRC | Share |
|---|---|---|
| Hosting | $2,171,402 | 75.16% |
| Colocation | $642,193 | 22.23% |
| Cloud Services | $74,168 | 2.57% |
| Professional Services | $1,138 | 0.04% |
| **Total** | **$2,888,901** | **100%** |

75% of revenue is hosting. Most of that is commodity dedicated servers with minimal managed services layered on top. Cloud services are 2.57%. Professional services are 0.04%, which is a direct reflection of the fact that the advisory and project delivery motions have not been formalized or measured as a strategic function.

The strategy requires inverting this ratio over time, not by abandoning hosting, but by stacking managed services on top of it and growing new-logo cloud revenue. The assessment framework described in this document is the mechanism that starts that stacking conversation.

### Revenue by Service Type

| Service Type | USD MRC | Share |
|---|---|---|
| Servers | $1,579,279 | 54.67% |
| Colocation | $433,168 | 14.99% |
| Connectivity | $209,625 | 7.26% |
| SAN/Storage | $154,020 | 5.33% |
| Firewall | $87,907 | 3.04% |
| Security | $83,198 | 2.88% |

Servers dominate. Connectivity, storage, firewall, and security are present but underweight relative to the managed services catalog's potential.

### Managed Services Penetration

6.5% of services have a managed service attached. Industry norm for mid-market MSPs is 15 to 20%. The gap represents the single largest revenue expansion opportunity in the portfolio: taking existing infrastructure customers and layering managed services on top.

Using the managed services catalog revenue stacking model, if the top 50 hosting-only customers (currently generating approximately $659K/mo in commodity revenue) were upsold to Layer 2 (Managed OS) alone, incremental MRC would be approximately $100K to $250K/mo. Full stacking through Layer 5 would multiply that further.

The assessment framework is the mechanism that initiates that stacking. A customer who has been through an Infrastructure Risk Assessment or an Operational Maturity Assessment has a documented gap analysis and a remediation roadmap that points directly at Aptum managed services. The assessment converts a generic "you should buy managed patching" pitch into a specific, evidence-based "here are the 14 unpatched servers running EOL operating systems that showed up in your assessment" conversation.

---

## The Strategic Model: Three Motions

The product discussion on March 31, 2026 (with Ian Rae, Marc Pare, Marc Alex Forget, Frederic Gingras, Will Stevens) confirmed the strategy rests on two revenue pillars: multi-cloud managed services and private cloud infrastructure. Everything else is the mechanism that starts relationships and leads to one or both of those pillars.

This strategy formalizes those mechanisms into three distinct motions that operate as a funnel:

**Motion 1: Advisory (Assess)** -- Structured assessments that diagnose the customer's environment, quantify risk, and produce a roadmap. These are the tip of the spear. They build trust, create technical intimacy, and generate the evidence base that justifies the investment in Motions 2 and 3.

**Motion 2: Execute (Implement)** -- Project-based professional services that act on the assessment findings. Migrations, hardware refreshes, architecture redesigns, security remediations, platform builds. These are scoped by HSA, delivered by cross-functional teams, and handed off to operational teams.

**Motion 3: Operate (Manage)** -- Recurring managed services stacked on infrastructure commodities. This is where the margin lives. This is what makes the customer sticky. Every advisory engagement and every execution project should have a clear line of sight to an operate outcome.

The three motions are not independent business lines. They are a funnel:

```
ADVISORY (Assess)           EXECUTE (Implement)           OPERATE (Manage)
$5K-$40K one-time    -->    $5K-$300K project      -->    $15K-$48K/mo recurring
                                                          (The Margin. The Retention.)
```

Every $1 spent in assessment revenue generates $2-3 in follow-on revenue within 12 months. The highest-ROI assessments (Cloud Repatriation, Operational Maturity) generate 10-20x follow-on multipliers.

---

## Motion 1: Advisory -- The Assessment Framework

Professional services historically operated as an undifferentiated bucket. The STG Assessment Playbook formalizes the advisory motion into seven structured assessments, each designed to answer a specific customer pain point and funnel toward specific managed services and infrastructure outcomes.

### The Seven Assessments

| # | Assessment | Price Range | Customer Trigger | Primary Funnel Destination |
|---|---|---|---|---|
| 1 | Infrastructure Risk & Readiness | $5K-$30K+ | EOL hardware, unsupported OS, deferred maintenance, "when did we last patch?" | Hardware refresh (Execute) then Managed OS L2 (Operate) |
| 2 | Hybrid Cloud | $7.5K-$40K+ | Workload placement uncertainty, rising cloud costs, "hybrid by accident" | Architecture consulting (Execute) then Managed CloudStack + App Platform (Operate) |
| 3 | Security Posture & Compliance | $5K-$30K+ | EOL firewalls, CVE exposure, audit findings, compliance gaps | Security remediation (Execute) then Security & Compliance L4 (Operate) |
| 4 | Cloud Repatriation | $5K-$35K+ | Cloud overspend, flat usage with rising bills, "we moved 5 years ago and our bill doubled" | Repatriation project (Execute) then Private Cloud + Managed Services (Operate) |
| 5 | Operational Maturity | $5K-$30K+ | IT team of 3-10 spending 80%+ time on lights-on, "we can't innovate because we're firefighting" | Managed services transition (Execute) then full Managed OS/App/Security stack (Operate) |
| 6 | App & Platform Modernization | $5K-$35K+ | Legacy infrastructure under modern apps, immature CI/CD, container gaps | K8s/platform build (Execute) then Managed Platform (Operate) |
| 7 | Well-Architected Review | $7.5K-$40K+ | Production AWS/Azure never formally reviewed, cost overruns, security concerns | Remediation project (Execute) then Public Cloud Management (Operate) |

### Assessment-to-Funnel Mapping

Each assessment is explicitly designed to produce findings that point at specific Aptum services. This is not accidental. The assessments are scoped so that the deliverable (the report, the roadmap, the business case) becomes the sales tool for the next motion.

| Assessment | Execute Follow-On | Operate Follow-On | Expected Follow-On TCV |
|---|---|---|---|
| Infrastructure Risk | Hardware refresh, OS upgrades ($25K-$150K) | Managed OS L2 ($2K-$10K/mo) | $50K-$300K |
| Hybrid Cloud | Architecture design, migration ($30K-$200K) | Managed CloudStack + App Platform ($5K-$30K/mo) | $100K-$500K |
| Security Posture | Firewall replacement, hardening, remediation ($20K-$100K) | Alert Logic MDR L4, Managed Firewall L2 ($3K-$12K/mo) | $75K-$250K |
| Cloud Repatriation | Repatriation execution ($50K-$300K) | Dedicated Cloud or Private Cloud + full stack ($8K-$50K/mo) | **$200K-$1M+** |
| Operational Maturity | Managed services transition ($15K-$50K) | L2 + L3 + L4 stack ($3K-$15K/mo) | $50K-$200K/yr recurring |
| Platform Modernization | K8s implementation, CI/CD build ($30K-$150K) | Managed Platform ($5K-$25K/mo) | $100K-$400K |
| Well-Architected Review | Remediation, architecture redesign ($20K-$100K) | Public Cloud Management ($3K-$15K/mo) | $75K-$250K |

### Assessment Delivery Model

Every assessment follows a standardized engagement workflow:

1. **Identify** -- AE spots pain signals using StoryLeader methodology. Maps to one of three narrative questions: "What are you dealing with right now?" (Infrastructure Risk, Security Posture), "Where do you want to be?" (Hybrid Cloud, Repatriation, Platform Modernization, Well-Architected), "What's holding you back?" (Operational Maturity, Infrastructure Risk, Security Posture).

2. **Qualify** -- AE uses sell sheet sizing questions to estimate t-shirt size (S/M/L/XL). Each size has a defined scope, team composition, timeline, and deliverable set.

3. **Scope** -- SA joins scoping call, refines scope, confirms deliverables, prepares SOW language from deliverable scope templates.

4. **Deliver** -- SA leads execution. For S engagements, SA works solo (20-40 hours). For M, SA + 1 specialist (50-90 hours). For L, SA + 2 specialists (100-170 hours). For XL, SA + 2-3 specialists + executive sponsor (200-300+ hours).

5. **Present** -- SA presents findings to customer. AE is in the room to identify follow-on signals. The assessment report becomes the business case for the Execute and Operate motions.

6. **Convert** -- AE proposes follow-on engagement using the assessment as the evidence base. The assessment-to-service mapping above defines the natural next step.

### Assessment Revenue Projections (Year 1)

Based on 36 priority accounts pre-mapped in the customer-to-assessment matrix:

| Metric | Year 1 Target |
|---|---|
| Assessments pitched | 14-18 |
| Assessments sold (40-50% close rate) | 11-14 |
| Assessment revenue (weighted by t-shirt mix) | $140K-$207K |
| Follow-on conversion (60-70%) | 8-9 opportunities |
| Follow-on deals closed (50-60%) | 4-5 deals |
| Follow-on revenue (PS + partial-year recurring) | $190K-$600K |
| **Total Year 1 (assessment + follow-on)** | **$330K-$807K** |

The assessment revenue itself ($140K-$207K) is not the point. The point is the $190K-$600K in follow-on revenue and the recurring managed services relationships that persist for years.

### How Assessments Funnel Customers to Aptum

The assessments serve as the structured entry point for customers coming from two primary origins:

**From on-premises (non-Aptum infrastructure):** Infrastructure Risk Assessment and Operational Maturity Assessment are the primary entry points. These customers have aging hardware, overwhelmed IT teams, and deferred maintenance. The assessment documents the risk, the remediation roadmap points at Aptum infrastructure (VPC, Private Cloud) with managed services stacked on top. The customer moves from self-managed on-prem to Aptum-managed hybrid.

**From hyperscalers (pulled back to Aptum services):** Cloud Repatriation Assessment and Well-Architected Review are the primary entry points. These customers have rising cloud bills, flat usage, and workloads that don't need to be in a hyperscaler. The assessment builds the financial business case for selective repatriation to Aptum Dedicated Cloud (KVM/CloudStack through Apt Cloud) or Private Cloud (VMware/Proxmox, for customers with existing VMware requirements), with managed services providing the operational capability they would lose by leaving the hyperscaler's managed offerings.

**From hybrid-by-accident (rationalization):** Hybrid Cloud Assessment catches customers who have sprawled across on-prem, colo, and one or more hyperscalers without a deliberate strategy. The assessment maps workloads to optimal placement and builds a rationalization plan that typically consolidates through Apt Cloud.

**Security-driven entry:** Security Posture Assessment catches customers with compliance obligations, audit findings, or simply aging security infrastructure. The assessment documents the gap, and the remediation path includes both infrastructure upgrades (Execute) and ongoing managed security services (Operate).

**Platform-driven entry:** App & Platform Modernization Assessment catches customers whose application ambitions have outgrown their infrastructure. They want containers, CI/CD, and modern deployment patterns but are running on 7-year-old hardware with no platform strategy. The assessment defines the target platform and the path to get there, landing on Aptum-managed Kubernetes and CloudStack.

---

## The Two Revenue Pillars

The advisory motion opens doors. The two revenue pillars are what generate the monthly recurring revenue that sustains the business. Marc Alex Forget stated it directly in the March 31 product discussion: the two things that generate monthly recurring revenue are (1) multi-cloud managed services and (2) private cloud infrastructure.

### Pillar 1: Managed Services (The Margin Multiplier)

Managed services are what differentiate Aptum from a VPS provider. They require human expertise. They create stickiness. They are the reason a customer stays when someone offers cheaper compute.

The managed services catalog defines five layers that stack on top of any infrastructure commodity:

| Layer | What It Delivers | Assessment That Drives It | Revenue Uplift | Delivering Team |
|---|---|---|---|---|
| L1: Infrastructure Monitoring | 24/7 hardware monitoring, alert triage, hardware replacement SLA, network monitoring | Infrastructure Risk Assessment | Included (cost already incurred) | Service Desk (Jason), DC Ops (George), Network (Ben) |
| L2: Managed OS | OS patching, Veeam backup, managed firewall, endpoint security | Infrastructure Risk, Operational Maturity, Security Posture | +$2K to $5K/mo | Managed Cloud (Andrei) + Service Desk (firewall L2 ops) |
| L3: App Platform | Datadog APM, WAF, DDoS protection, L7 load balancing, DB tuning | Platform Modernization, Hybrid Cloud, Well-Architected Review | +$3K to $8K/mo | Managed Cloud (Andrei) |
| L4: Security & Compliance | Alert Logic MDR, compliance reporting, vulnerability scanning | Security Posture Assessment | +$2K to $5K/mo | Managed Cloud (Andrei) + Alert Logic (partner) |
| L5: Business Continuity | DRaaS, BCP planning, hybrid interconnects, M365, managed DNS | Hybrid Cloud, Cloud Repatriation | +$1.5K to $5K/mo | Managed Cloud (Andrei) + Network (Ben) |

The stacking math is compelling. A mid-market customer with 20 VMs on VPC + Azure hybrid:

| Component | Monthly Revenue |
|---|---|
| Infrastructure commodity (VPC + Azure) | $7,000 |
| L2: Managed OS (patching + Veeam) | $3,500 |
| L2: Managed Firewall | $500 |
| L3: Datadog APM (20 hosts) | $2,500 |
| L3: WAF (2 web apps) | $1,000 |
| L4: Alert Logic MDR | $2,500 |
| L5: DRaaS (8hr RTO, 1hr RPO) | $3,000 |
| L5: ExpressRoute | $800 |
| **Total MRR** | **$20,800** |

Compare to the same customer buying unmanaged VPC only: $7,000/mo. Managed services nearly triple revenue per customer. The assessment is what produces the evidence that justifies each layer.

### Pillar 2: Aptum IaaS / Private Cloud (The Infrastructure Foundation)

Aptum IaaS, delivered through Apt Cloud, is the new infrastructure product. It replaces the legacy dedicated hosting model with a modern, self-service, software-defined infrastructure platform.

**Taxonomy clarification (April 15, 2026):** Based on alignment with Will Stevens and the product team, Aptum offers three distinct infrastructure delivery models. These had previously been conflated under the "Private Cloud" label — that conflation is resolved here. All teams should use these definitions consistently.

Three delivery models:

| Model | Tenancy | Hypervisor / Stack | Delivered via Apt Cloud? | Target Customer | Assessment Entry Point |
|---|---|---|---|---|---|
| VPC | Multi-tenant (shared physical hosts) | KVM / Apache CloudStack | Yes — self-service via Apt Cloud portal | Cost-conscious workloads, dev/test, general purpose | Hybrid Cloud Assessment (workload placement), Operational Maturity (infrastructure transition) |
| Dedicated Cloud | Single-tenant (dedicated physical hosts) | KVM / Apache CloudStack | Yes — delivered through Apt Cloud control plane | Production workloads requiring dedicated compute, compliance-sensitive, performance-critical, cost-predictable | Cloud Repatriation Assessment (the business case), Infrastructure Risk (the hardware refresh path) |
| Private Cloud | Single-tenant (dedicated physical hosts) | VMware or Proxmox | No — not necessarily through Apt Cloud; direct infrastructure layer | Customers with existing VMware estates, Broadcom displacement candidates, workloads requiring VMware feature parity (vMotion, vSAN, etc.) | Cloud Repatriation Assessment, Infrastructure Risk Assessment (VMware refresh path) |

**Key distinctions:**
- VPC and Dedicated Cloud both run KVM/CloudStack and are delivered through the Apt Cloud portal. The difference is tenancy: VPC shares physical hosts, Dedicated Cloud gets dedicated hardware.
- Private Cloud uses VMware or Proxmox on dedicated hardware and does not require the Apt Cloud control plane. It is infrastructure with managed services on top, not a cloud portal product.
- "Private Cloud" as used in earlier documentation often referred to what is now called Dedicated Cloud. When referencing infrastructure delivered through Apt Cloud on dedicated hosts, the correct term going forward is **Dedicated Cloud**.

The board demo on March 31 confirmed production readiness of VPC and Dedicated Cloud. Dave Pistacchio called it "true private cloud" and directed the team to determine a fast-follow GTM timeline.

Pre-launch validation: 7 Ignite customers, $39,119/mo CAD MRC, 36-month contracts. Gross margins of 74 to 89%.

Key differentiators vs. hyperscalers:
- Predictable pricing (per vCPU/GB, no transaction costs, no surprise egress)
- Data sovereignty (Canadian-owned, Toronto DC with SOC 2 Type II)
- Single portal for private + public cloud (Apt Cloud manages both Aptum IaaS and Azure/AWS/GCP)
- Managed services layered on top (hyperscalers don't do this, that's the customer's problem)
- Assessment-driven onboarding (the customer arrives with a documented environment, a business case, and a roadmap, not a cold signup)

Key differentiators vs. commodity hosting providers (OVH, Hetzner, DigitalOcean):
- Managed services stack (they sell infrastructure, Aptum sells outcomes)
- Enterprise-grade portal with RBAC, multi-tenant governance, cost visibility
- MSP/reseller white-label capability (ES Williams/Ignite model)
- Advisory and professional services to design, migrate, and manage

---

## Motion 2: Execute -- Professional Services Delivery

The Execute motion sits between Advisory and Operate. It is the project-based work that acts on assessment findings and prepares the customer's environment for ongoing managed services.

### The Advisory/Execute Distinction

This is a critical organizational and commercial distinction:

| Dimension | Advisory (Assess) | Execute (Implement) |
|---|---|---|
| What it is | Structured assessments that diagnose, quantify, and recommend | Project-based work that builds, migrates, remediates, and transitions |
| Deliverable | Report with findings, risk scores, and roadmap | Working environment, migrated workloads, hardened infrastructure, documented handoff |
| Team model | SA-led, lightweight (20-300 hours) | Cross-functional, heavier (varies, typically 200-2,000+ hours) |
| Commercial model | Fixed-fee, t-shirt sized (S/M/L/XL) | SOW-scoped, milestone-based |
| Revenue range | $5K-$40K per engagement | $5K-$300K per project |
| Success metric | Follow-on conversion rate | On-time/on-budget delivery, clean handoff to Operate |
| Who scopes it | SA using assessment sell sheets and deliverable scope templates | HSA (Pat Wolthausen) architects |
| Who delivers it | SA + specialists from home teams | HSDM (Lacie Allen-Morley) coordinating cross-functional resources |
| Who owns the customer | AE throughout; CSM for ongoing relationship | AE throughout; HSDM for project delivery; CSM between projects |

### Execute Engagement Types

| Engagement | What It Produces | Typical Assessment Origin | Where It Leads (Operate) |
|---|---|---|---|
| Cloud Migration | Workload assessment, migration plan, execution | Hybrid Cloud Assessment, Cloud Repatriation Assessment | Customer lands on Aptum IaaS or Apt Cloud-managed Azure/AWS, buys managed services |
| Repatriation Project | Workload moved from hyperscaler to Aptum Dedicated Cloud or Private Cloud | Cloud Repatriation Assessment | Customer on Dedicated Cloud (KVM/Apt Cloud) or Private Cloud (VMware/Proxmox) with full managed services stack |
| Hardware Refresh | EOL server replacement, spec, procure, build, migrate, decommission | Infrastructure Risk Assessment | Customer moves from legacy dedicated to VPC or Private Cloud |
| Security Remediation | Firewall replacement, OS upgrades, hardening, compliance alignment | Security Posture Assessment | Customer buys Alert Logic MDR, managed firewall, compliance reporting |
| Platform Build | Kubernetes implementation, CI/CD pipeline, container platform | Platform Modernization Assessment | Customer on managed Kubernetes/CloudStack with DevOps monitoring |
| Architecture Redesign | Well-architected remediation, cost optimization, governance implementation | Well-Architected Review | Customer buys ongoing public cloud management |
| Managed Services Transition | Operational handoff from customer IT team to Aptum ops teams | Operational Maturity Assessment | Customer on full L2-L5 managed services stack |
| DR Design & Implementation | Failover architecture, runbook development, first test | Infrastructure Risk, Hybrid Cloud | Customer buys DRaaS, hybrid interconnects |

### Execute Financial Model

Current state: $738K YTD revenue, 29.2% gross margin, $485K direct labor, $16K partner services.

The Execute motion needs two things to scale:

1. A defined service manager. The operating model has a gap. No single owner coordinates PS delivery, resource allocation, and margin accountability. This role must be filled.

2. Assessment-driven pipeline. Today, PS engagements arrive ad hoc. With the advisory motion formalized, every Execute engagement should trace back to an assessment that produced the findings and the business case. This makes scoping faster (the assessment already mapped the environment), delivery more predictable (the assessment already identified the risks), and conversion more likely (the customer has already invested in understanding the problem).

---

## Motion 3: Operate -- The Managed Services Destination

Every advisory engagement and every execution project should have a clear line of sight to an operate outcome. If the answer to "where does this lead in terms of recurring managed services?" is "nowhere," the engagement does not align with the strategy.

The managed services catalog (see separate document) defines the five layers in detail. The assessment framework adds a new dimension: assessment-driven onboarding paths that connect specific assessment findings to specific managed service layers.

### Assessment-Driven Onboarding Paths

| Customer Origin | Entry Assessment | Execute Step | Operate Destination | Expected MRC |
|---|---|---|---|---|
| On-prem with aging hardware | Infrastructure Risk | Hardware refresh or migration to VPC/Private Cloud | L1 + L2 (Monitoring + Managed OS) | $5K-$15K/mo |
| Hyperscaler with rising costs | Cloud Repatriation | Selective repatriation to Dedicated Cloud (KVM/Apt Cloud) or Private Cloud (VMware/Proxmox) | L1 + L2 + L5 (Monitoring + Managed OS + Hybrid Connectivity) | $10K-$50K/mo |
| Hybrid-by-accident | Hybrid Cloud | Architecture rationalization, workload placement | L2 + L3 + L5 (Managed OS + App Platform + Hybrid Connectivity) | $8K-$25K/mo |
| Compliance-driven | Security Posture | Security remediation, firewall upgrades | L2 + L4 (Managed Firewall + Security & Compliance) | $5K-$17K/mo |
| Overwhelmed IT team | Operational Maturity | Managed services transition | L2 + L3 + L4 (full ops handoff) | $8K-$30K/mo |
| Modern app on legacy infra | Platform Modernization | K8s/platform build | L2 + L3 (Managed OS + App Platform) | $8K-$25K/mo |
| Unreviewed cloud estate | Well-Architected Review | Remediation project | L3 + Public Cloud Management | $6K-$15K/mo |

---

## The Service Teams That Deliver This

Each motion is delivered by specific operational teams. The organizational model does not require a reorg. The motion determines ticket routing and resource allocation, not the org chart.

### Team Domain Map

| Team | Leader | Domain | Advisory Role | Execute Role | Operate Role |
|---|---|---|---|---|---|
| Service Desk / NOC | Jason Auer | Infrastructure operations (24/7) | Data collection support for assessments | Contributing resource for infrastructure projects | Operates L1 monitoring, dispatches hardware, L2 firewall ops |
| Managed Cloud | Andrei Ianouchkevitch | OS layer and above, all cloud platforms | Subject matter expertise for assessments | Contributing resource for migrations, remediations | Operates L2 through L5 managed services |
| Compute Platforms | Martin Tessier | Server builds, configuration standards | Environment documentation for assessments | Builds compute environments for Execute projects | Hands off to Service Desk or Managed Cloud |
| Data Center Ops | George Revie | Physical infrastructure across 8 locations | Physical asset inventory for Infrastructure Risk assessments | Hardware deployment for refresh projects | Racks, cabling, power, remote hands |
| Networking | Ben Kennedy | MPLS, internet, cloud connects | Network topology documentation for assessments | Connectivity implementation for Execute projects | OSI Layer 1 to 3 operations |
| HSA | Pat Wolthausen + 3 architects | Pre-sales design, SOW scoping | **Leads assessment delivery** (SA role) | Defines technical scope for Execute SOWs | Target: 50%+ billable utilization |
| HSDM | Lacie Allen-Morley | Project delivery (non-recurring / Execute motion) | AE coordination during assessment delivery | **Owns Execute project delivery** and timeline | Hands to CSM at project close |
| CSM | Lacie Allen-Morley | Recurring customer relationship, account ops | — | Supports customer continuity between Execute engagements | Inbound queues, orders, renewals, credits, cancellations; proactive retention |
| Professional Services | (Open, no defined manager) | Project-based execution | Assessment framework ownership (to be assigned) | Cross-functional Execute delivery | Handoff to operational teams |
| Operational Intelligence | Jorge Quintero | Data pipelines, unified customer view | Assessment data analysis support | Metrics and reporting for project outcomes | Unified monitoring and customer view |

### The Routing Model

The JSM project structure already implements the domain split:

- APTUM project (56,381+ tickets): Infrastructure-layer tickets. Zabbix alerts, LogicMonitor, hardware health, Veeam reports, customer firewall/port requests. Jason's team triages and resolves.
- CUST-* projects (21 projects, active customers): Platform-layer tickets. Datadog incidents, Azure platform requests, app-level issues, TLS/SSL, SQL outages. Andrei's team owns.

No reorg needed. The product tier determines whether a customer gets an APTUM ticket flow (L1 infrastructure ops) or a CUST-* ticket flow (L2+ managed services). The model extends naturally to new commodities (CloudStack, Proxmox, BMaaS) because the skill split is the same: Jason's team has hypervisor and bare-metal expertise, Andrei's team has cloud-platform and application expertise.

---

## Apt Cloud: The Portal Strategy

Apt Cloud today does provisioning well. VPC self-service is live. Azure subscription management is live. Cloudflare DNS is live. The monetization engine (catalogs, pricing, billing) works.

What Apt Cloud does not yet do is surface the managed services layers. A customer paying for Managed OS, Datadog monitoring, Veeam backup, and Alert Logic MDR cannot see any of that in the portal. The managed services are operationally delivered but invisible.

This is the highest-priority product gap. Making managed services visible in the portal converts Apt Cloud from a provisioning tool into a retention engine.

### Portal Visibility Roadmap

| Layer | What Should Be Visible | Priority | Dependencies |
|---|---|---|---|
| Commodity (L0) | VM status, cost estimator, usage reports | Live | Done |
| L1: Infra Monitoring | Uptime dashboard, alert history, incident status | High | Zabbix/LogicMonitor API integration |
| L2: Managed OS | Patch compliance, backup success/failure, firewall audit log | High | Veeam + patching tool API integration |
| L3: App Platform | Datadog dashboards (embed/link), WAF events, LB health | Medium | Datadog API + Imperva API integration |
| L4: Security | MDR threat dashboard, compliance status, scan results | Medium | Alert Logic API integration |
| L5: BCP/Hybrid | DR plan status, last test result, interconnect up/down | Medium | Custom dashboard from runbook data |
| Support | Ticket status, SLA compliance, contact info | High | JSM API integration |

L1 + L2 portal visibility and support ticket integration are the highest-impact items. They affect every managed customer and should be the engineering priority.

---

## Revenue Engines and Growth Path

### Engine 1: Managed Services Stacking on Existing Base (Defend and Expand)

The immediate opportunity. 773 existing customers, 6.5% managed services penetration. The contract renewal wave (72.74% of revenue within 6 months) is both a risk and an opportunity because every renewal conversation is a stacking conversation.

The assessment framework supercharges this engine. Instead of a generic upsell pitch at renewal, the AE offers an assessment. The assessment produces evidence. The evidence justifies the investment.

Recommended assessment plays for existing base:
- Hosting-only customers (429 accounts, $659K/mo): Infrastructure Risk Assessment or Operational Maturity Assessment. These customers are sitting on aging infrastructure with no managed services. The assessment quantifies the risk they are carrying.
- Multi-LOB customers (135 accounts, $1.8M/mo): Security Posture Assessment or Hybrid Cloud Assessment. These customers already buy across product lines. The assessment identifies the next layer of managed services to stack.
- Cloud-only customers (~116 accounts, $18K/mo): Well-Architected Review. These customers are on hyperscaler infrastructure managed through Apt Cloud. The review identifies optimization opportunities and opens the managed services conversation.

Target: Move managed services penetration from 6.5% to 15% within 12 months. At current portfolio size, that represents approximately $100K to $250K in incremental MRC from upsell alone.

### Engine 2: New Logo Acquisition on Aptum IaaS (Grow)

The Ignite program proved the model: 7 new logos, $39K/mo MRC, 74 to 89% gross margins. The board has directed a fast-follow GTM timeline.

For new logos, the assessment is the first engagement. The customer does not start by signing a managed services contract. The customer starts by paying $5K to $40K for an assessment that maps their environment, quantifies their pain, and produces a roadmap that happens to land on Aptum infrastructure and services.

Recommended assessment plays for new logos:
- VMware customers feeling Broadcom pressure: Hybrid Cloud Assessment or Cloud Repatriation Assessment. The assessment builds the business case for moving to Dedicated Cloud (KVM/CloudStack via Apt Cloud) or Private Cloud (Proxmox on dedicated hardware) on Aptum IaaS.
- Cloud-fatigued mid-market: Cloud Repatriation Assessment. The assessment documents the overspend and models the savings from selective repatriation.
- Compliance-driven organizations: Security Posture Assessment. The assessment documents the compliance gaps and positions Aptum's managed security stack as the remediation path.

Target: Phase 1 (Q2 2026) focuses on revenue enablement and operational readiness. Phase 2 (Q3 to Q4 2026) expands the catalog (MAAS, Proxmox, Kubernetes) and recruits MSP resellers. Phase 3 (H1 2027) scales to multi-region and activates AWS/GCP through the portal.

The Broadcom disruption is the market catalyst. 35% of VMware workloads migrating by 2028 per Gartner. Aptum's CloudStack and Proxmox alternatives, delivered through Apt Cloud with managed services stacking, are a direct answer.

### Engine 3: MSP/Reseller Channel (Scale)

ES Williams (Ignite customer) is already being explored as an early reseller model beta customer. The Apt Cloud white-label capability, combined with the monetization engine, lets MSPs build their own branded infrastructure and managed services offerings on top of Aptum's platform.

Target MSP profile: Regional MSPs with 50 to 500 end customers, currently running VMware Cloud Director, squeezed by Broadcom pricing, looking for an alternative infrastructure partner. These are the MSPs Marc Pare described: "They've been so squeezed by Broadcom and other stuff that they can't operate and run it themselves and are looking for a partner who can."

The Latitude.sh and Megaport intersection in Miami, as discussed in the March 31 product meeting, is a test point for this model. Latitude provides commodity bare metal, Megaport provides the channel relationships, and Aptum provides the managed services and consulting layer on top.

### Engine 4: Assessment-Led Pipeline (Open Doors)

This is the new engine, formalized by the STG Assessment Playbook. It is the mechanism that feeds Engines 1 through 3.

The assessment framework maps to three marketing campaigns targeting specific customer pain points:

| Campaign | Target | Primary Assessment CTA | Expected Yield |
|---|---|---|---|
| "The Cloud You Can't Escape" (Executive Dinners) | Whales with $5M-$20M+ cloud spend | Cloud Repatriation Assessment | 3-5 assessment opportunities per event, 1-3 high-margin repatriation projects |
| "Time to Grow Up" (Content-Led Outbound) | Post-scale companies ($50M-$300M revenue, PE/VC-backed) | Hybrid Cloud Assessment | Awareness to assessment conversion over 60-90 day nurture |
| "The Cloud Hangover" (Physical Mailer + White Paper) | Cloud-fatigued mid-market | Hybrid Cloud or Cloud Repatriation Assessment | Physical touchpoint drives digital engagement, assessment is the conversion point |

Year 1 pipeline target: 14-18 assessments pitched, 11-14 sold, $330K-$807K total revenue (assessment + follow-on).

---

## The MAAS Differentiator

The CloudStack 4.22 Extensions Framework enables integration with Canonical MAAS (Metal as a Service) without core Java development. When MAAS is implemented, Aptum will be able to offer bare-metal provisioning through the same Apt Cloud portal that handles VMs, public cloud, and managed services.

This is a market differentiator because no other mid-market MSP offers self-service bare metal + VPC + private cloud + hyperscaler management through a single portal with managed services layered on top. The closest competitors (OVH, Hetzner) offer bare metal but not managed services. The managed services competitors (Rackspace, Navisite) offer managed services but not self-service bare metal.

MAAS is on the Phase 2 roadmap (Q3 to Q4 2026) alongside Proxmox and Kubernetes.

---

## What We Stop Doing

Strategic clarity requires saying no to some things:

We stop positioning VPC as a lead product for new logos. Marc Pare was explicit: VPC is the "french fries, not the hamburger." It's a cost management and margin play for existing workloads, not a go-to-market product. New logo hunting leads with Private Cloud and managed services.

We stop reselling Azure at a loss. Ian Rae identified this directly: "We have to get out of the mindset of I'm going to resell Azure and support at a loss." Azure subscription revenue should be a vehicle for managed services revenue, not an end in itself. The margin is in the management layer, not the resell.

We stop building service guides around vendor names. Service guides should be void of other companies' products unless explicitly necessary. The customer buys "Managed Backup," not "Veeam." They buy "App Performance Monitoring," not "Datadog." The vendor is the implementation detail, not the product.

We stop chasing large enterprise accounts as sustainable managed services customers. Telesat, CN, Bell: these are consulting engagements, not managed services relationships. Ian Rae: "An organization that has 10,000 employees and has an IT department that is 3 times the size of Aptum is not going to be like, Aptum, we want you to manage all of our public cloud stuff."

We stop running professional services as an undifferentiated bucket. The advisory/execute distinction is now formalized. Assessments are advisory. Migrations, builds, and remediations are execute. They have different delivery models, different commercial models, different success metrics, and different team structures. Treating them as one blended "PS" line masks both the strategic value of advisory and the operational discipline required for execute.

---

## Roadmap Summary

| Phase | Timeline | Focus | Key Milestones |
|---|---|---|---|
| Phase 1 | Q2 2026 | Revenue enablement, GTM for Aptum IaaS, assessment pipeline activation, advisory/execute PS split | Ignite customer migrations complete, pricing validated with finance, commercial team armed with managed services catalog + assessment sell sheets, portal L1+L2 visibility scoped, first 3-5 assessments pitched |
| Phase 2 | Q3 to Q4 2026 | Catalog expansion, MSP channel recruitment, assessment pipeline scaling | MAAS integration, Proxmox via CloudStack Extensions, second DC scoping, first MSP reseller signed, managed services penetration from 6.5% to 15%, 8-10 assessments delivered, PS service manager hired |
| Phase 3 | H1 2027 | Multi-region, channel scale, assessment framework maturity | AWS/GCP activation in Apt Cloud, multi-region infrastructure (Miami or second Toronto), channel revenue exceeding $100K MRC, assessment-to-operate conversion rate exceeding 60% |

---

## Open Items Requiring Resolution

1. Apt Cloud needs a new name. The current name creates confusion with "App Cloud" in conversation and is not differentiated in market. This is a known issue without a resolution date.

2. Professional Services needs a service manager. The operating model has a gap. No single owner coordinates PS delivery (both advisory and execute), resource allocation, and margin accountability. With the advisory/execute formalization, this role becomes even more critical: the PS service manager needs to own assessment pipeline tracking, delivery quality, and follow-on conversion metrics.

   **Update (April 15, 2026):** The CEM/customer relationship gap previously noted has been resolved by splitting Lacie's org into two distinct functions: HSDM (project delivery / Execute motion, non-recurring) and a new Customer Success Management (CSM) function (recurring customer ops, queues, orders, renewals, proactive retention). Both report to Lacie Allen-Morley. HSDM hands to CSM at project close; CSM hands back to HSDM at new engagement start.

3. Alert Logic MDR timeline and commercial model are undefined. Listed as "IN DEVELOPMENT" in service guides. Is it partner-delivered (Alert Logic SOC) or Aptum-operated with Alert Logic tooling? This directly affects the Security Posture Assessment follow-on path.

4. Pricing for managed service layers is placeholder. The catalog uses ranges ($2K to $5K, $3K to $8K). These need validation with Sarah Blanchard (finance) and Fred's commercial team before the sales team can quote. Assessment follow-on conversion depends on having firm pricing to present alongside assessment findings.

5. Portal integration engineering effort is unknown. 15+ integration points identified in the catalog (Zabbix, Veeam, Datadog, JSM, Alert Logic, etc.) with no LOE estimates from Will's team.

6. Jason's team needs CloudStack/KVM/Proxmox training plan. The decision that Service Desk owns infrastructure ops for new commodities depends on this investment.

7. The "two-Zabbix problem" (internal monitoring vs. customer-facing monitoring consolidation) needs a VP-level mandate. Jorge's Operational Intelligence team has flagged it but cannot resolve it without organizational authority.

8. Assessment sell sheets and delivery guides need commercial team enablement. The STG playbook materials exist but have not been trained into the AE and SA teams. Phase 1 (Q2 2026) must include enablement sessions covering the assessment portfolio, t-shirt sizing, discovery questions, and follow-on mapping.

9. The 36-account customer-to-assessment matrix needs validation with the commercial team. The pre-mapping of accounts to primary and secondary assessments should be reviewed by AEs who own those relationships.

---

*Sources: dimServices extract (April 1, 2026), Product Strategy v1.3.1 (Confluence), CloudOps SW Product Strategy 1.0 (Confluence), Service Guides (Confluence), Product Discussion VTT (March 31, 2026), AptCloud/Aptum IaaS Strategy v1.2, AptCloud/Aptum IaaS PRD, Managed Services Catalog, Service Team descriptions (all 9 teams), STG Assessment & Commercial Playbook v1.0 (7 assessments, engagement workflow, revenue model, success metrics, post-assessment pathways), Reanchor session notes (April 1, 2026).*
