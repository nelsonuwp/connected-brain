# Aptum Product Strategy

## From Commodity Hosting to Hybrid Cloud Managed Services

**Version 2.1 | April 28, 2026**

---

## Vision and Mission

Aptum's vision is a future where businesses have the freedom to innovate, grow, thrive, and own their destiny in the cloud. The mission is to help customers run their cloud, their way, with the right platforms and right expertise, right when they need them.

This strategy is the operating realization of that brand promise. The brand commits to three things: the right workload on the right platform, the right expertise at the right time, and your cloud, your way. The job of product strategy is to make those promises true at the level of services, motions, and revenue.

---

## The Position

Aptum is a hybrid cloud managed services provider built on the principle that the right workload runs on the right platform. Aptum is truly cloud agnostic. Customers can run on any of the major hyperscalers (Azure, AWS, GCP), on Aptum-delivered virtual or dedicated infrastructure (VPC, Dedicated Cloud), on dedicated VMware or Proxmox stacks, or on bare metal. Aptum's job is to help the customer figure out which of these is right for which workload, deliver it, manage it, and remove the complexity of running it across more than one place.

The aspiration is to be the company that makes infrastructure disappear into the background for mid-market organizations, so they can focus on their business instead of managing servers, patching operating systems, and arguing about firewall rules.

The company has two core assets that make this possible:

1. **Aptum Portal** (the customer-facing control plane). The Aptum Portal is how customers consume Aptum's products and services. It delivers self-service provisioning, cost visibility, lifecycle management, and will increasingly surface the managed services the customer is paying for. The underlying software (CloudMC, also branded CloudOps Software) is mature, in production with anchor tenants, and capable of presenting a single pane of glass across Aptum infrastructure and the hyperscalers. The portal's strategic purpose is to make Aptum's own products easier to consume, not to be sold as a standalone B2B2B platform. We eat our own dogfood.
1. **Aptum IaaS** (the infrastructure). Compute, storage, networking on Apache CloudStack 4.22 with KVM virtualization. Delivered as VPC (multi-tenant shared hosts), Dedicated Cloud (single-tenant dedicated hosts, KVM/CloudStack), and Private Cloud (dedicated hosts with VMware or Proxmox, not necessarily through the Aptum Portal). This is the foundation that replaces commodity dedicated hosting and offers an alternative to hyperscaler infrastructure at better economics.

These two assets, combined with operational teams that manage everything from the physical rack to the application layer, and with deep technical expertise in hyperscaler MSP delivery, Kubernetes, DevOps, and platform engineering, are what lets Aptum sell managed outcomes rather than just infrastructure components.

### Brand promise and the forever-operate goal

The Identity & Values brand promise commits that customer solutions are designed to be maintained "with or without us, so you can grow on your own terms." The strategy commits that every engagement should funnel toward an Operate outcome and that recurring management is where the margin lives. These are not in tension. The customer is always free to leave; the goal is to operate the customer's environment so much better than they could in-house that staying is the obvious choice. The freedom to leave is real and is part of the brand promise. The way Aptum earns forever is by being better than DIY, not by lock-in.

Build-Operate-Transfer (BOT) is therefore not a strategic motion. It is a customer-onboarding narrative for skeptics who need reassurance that they can bring operations home if they want to. The product goal is Assess to Build to Operate, forever.

---

## Where We Are Today: The Revenue Picture

The current portfolio (dimServices extract, April 1, 2026) reveals the gap between where the revenue is and where the strategy says it should be.

### Revenue by Line of Business

| Line of Business | USD MRC | Share |
| --- | --- | --- |
| Hosting | $2,171,402 | 75.16% |
| Colocation | $642,193 | 22.23% |
| Cloud Services | $74,168 | 2.57% |
| Professional Services | $1,138 | 0.04% |
| **Total** | **$2,888,901** | **100%** |

75% of revenue is hosting. Most of that is commodity dedicated servers with minimal managed services layered on top. Cloud services are 2.57%. Professional services are 0.04%, which is a direct reflection of the fact that the advisory and project delivery motions have not been formalized or measured as a strategic function.

The strategy requires inverting this ratio over time, not by abandoning hosting, but by stacking managed services on top of it and growing new-logo cloud revenue. The assessment framework described in this document is the mechanism that starts that stacking conversation.

### Revenue by Service Type

| Service Type | USD MRC | Share |
| --- | --- | --- |
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

| Assessment | Customer Trigger | Primary Funnel Destination |
| --- | --- | --- | --- | --- |
| Infrastructure Risk & Readiness | EOL hardware, unsupported OS, deferred maintenance | Hardware refresh (Execute) then Reactive/Proactive managed services (Operate) |
| Hybrid Cloud | Workload placement uncertainty, rising cloud costs, hybrid sprawl | Architecture consulting (Execute) then Reactive or Proactive tier (Operate) |
| Security Posture & Compliance | EOL firewalls, CVE exposure, audit findings, compliance gaps | Security remediation (Execute) then Proactive tier with MDR and Compliance Reporting (Operate) |
| Cloud Repatriation | Cloud overspend, flat usage with rising bills | Repatriation project (Execute) then Proactive tier on Aptum IaaS (Operate) |
| Operational Maturity | Small IT team spending 80%+ time on reactive work | Managed services transition (Execute) then Proactive tier full stack (Operate) |
| App & Platform Modernization | Legacy infrastructure under modern apps, immature CI/CD | Platform build (Execute) then Proactive tier managed platform (Operate) |
| Well-Architected Review | Unreviewed cloud estate, cost overruns, security concerns | Remediation (Execute) then Reactive or Proactive tier with FinOps (Operate) |





---

## The Two Revenue Pillars

The advisory motion opens doors. The two revenue pillars are what generate the monthly recurring revenue that sustains the business. Marc Alex Forget stated it directly in the March 31 product discussion: the two things that generate monthly recurring revenue are (1) multi-cloud managed services and (2) private cloud infrastructure.

### Pillar 1: Managed Services (The Margin Multiplier)

Managed services are what differentiate Aptum from a VPS provider. They require human expertise. They create stickiness through superior operations, not lock-in. They are the reason a customer stays when someone offers cheaper compute.

The technical depth that makes managed services defensible is broader than commodity infrastructure ops. Aptum's operating teams cover the full stack: hyperscaler MSP delivery (Azure Expert MSP heritage, AWS competencies in migration, EKS, DevOps, Cloud Operations, GenAI in development, GCP), Kubernetes and platform engineering (the CloudOps team), CloudStack and KVM hypervisor expertise, VMware operations, and a security partnership stack. This combination is unusual in mid-market managed services. Most competitors lead with a single hyperscaler or with VMware. Aptum leads with the workload and matches the platform to it.

The managed services catalog defines five layers that stack on top of any infrastructure commodity:

| Layer | What It Delivers | Assessment That Drives It | Delivering Team |
| --- | --- | --- | --- | --- |
| L1: Infrastructure Monitoring | 24/7 hardware monitoring, alert triage, hardware replacement SLA, network monitoring | Infrastructure Risk Assessment | Service Desk, DC Ops, Networking |
| L2: Managed OS | OS patching, Veeam backup, managed firewall, endpoint security | Infrastructure Risk, Operational Maturity, Security Posture | Managed Cloud + Service Desk |
| L3: App Platform | Datadog APM, WAF, DDoS protection, L7 load balancing, DB tuning | Platform Modernization, Hybrid Cloud, Well-Architected Review | Managed Cloud |
| L4: Security & Compliance | Alert Logic MDR, compliance reporting, vulnerability scanning | Security Posture Assessment | Managed Cloud + Alert Logic |
| L5: Business Continuity | DRaaS, BCP planning, hybrid interconnects, M365, managed DNS | Hybrid Cloud, Cloud Repatriation | Managed Cloud + Networking |

The assessment is what produces the evidence that justifies each layer.

### Pillar 2: Aptum IaaS and the Cloud-Agnostic Stack (The Infrastructure Foundation)

Pillar 2 is not just Aptum IaaS. It is the cloud-agnostic infrastructure stack that Aptum delivers and manages, with Aptum IaaS as the new core. Aptum is one of the few mid-market providers that can credibly say "we will help you place this workload on the right platform" and mean any of: hyperscaler, Aptum VPC, Aptum Dedicated Cloud, dedicated VMware, dedicated Proxmox, or bare metal. Most competitors are tied to a single hyperscaler or to the VMware stack. Aptum is not.

Aptum IaaS, delivered through the Aptum Portal, is the new infrastructure product. It replaces the legacy dedicated hosting model with a modern, self-service, software-defined infrastructure platform.

**Taxonomy clarification (April 15, 2026):** Aptum offers three distinct infrastructure delivery models. These had previously been conflated under the "Private Cloud" label. The conflation is resolved here.

| Model | Tenancy | Hypervisor / Stack | Delivered via Aptum Portal? | Target Customer | Assessment Entry Point |
| --- | --- | --- | --- | --- | --- |
| VPC | Multi-tenant (shared physical hosts) | KVM / Apache CloudStack | Yes, self-service via Aptum Portal | Cost-conscious workloads, dev/test, general purpose | Hybrid Cloud Assessment (workload placement), Operational Maturity (infrastructure transition) |
| Dedicated Cloud | Single-tenant (dedicated physical hosts) | KVM / Apache CloudStack | Yes, delivered through Aptum Portal | Production workloads requiring dedicated compute, compliance-sensitive, performance-critical, cost-predictable | Cloud Repatriation Assessment (the business case), Infrastructure Risk (the hardware refresh path) |
| Private Cloud | Single-tenant (dedicated physical hosts) | VMware or Proxmox | No, not necessarily through the Aptum Portal | Customers with existing VMware estates, Broadcom displacement candidates, workloads requiring VMware feature parity (vMotion, vSAN, etc.) | Cloud Repatriation Assessment, Infrastructure Risk Assessment (VMware refresh path) |

**Key distinctions:**

- VPC and Dedicated Cloud both run KVM/CloudStack and are delivered through the Aptum Portal. The difference is tenancy: VPC shares physical hosts, Dedicated Cloud gets dedicated hardware.
- Private Cloud uses VMware or Proxmox on dedicated hardware and does not require the Aptum Portal. It is infrastructure with managed services on top, not a portal product.
- "Private Cloud" as used in earlier documentation often referred to what is now called Dedicated Cloud. When referencing infrastructure delivered through the Aptum Portal on dedicated hosts, the correct term going forward is **Dedicated Cloud**.

The board demo on March 31 confirmed production readiness of VPC and Dedicated Cloud. Dave Pistacchio called it "true private cloud" and directed the team to determine a fast-follow GTM timeline.


Key differentiators vs. hyperscalers:

- Predictable pricing (per vCPU/GB, no transaction costs, no surprise egress)
- Data sovereignty (Canadian-owned, Toronto DC with SOC 2 Type II)
- Single portal for private and public cloud (Aptum Portal manages both Aptum IaaS and Azure/AWS/GCP)
- Managed services layered on top (hyperscalers don't do this, that's the customer's problem)
- Assessment-driven onboarding (the customer arrives with a documented environment, a business case, and a roadmap, not a cold signup)

Key differentiators vs. commodity hosting providers (OVH, Hetzner, DigitalOcean):

- Managed services stack (they sell infrastructure, Aptum sells outcomes)
- Enterprise-grade portal with RBAC, multi-tenant governance, cost visibility
- Advisory and professional services to design, migrate, and manage

### What cloud agnosticism looks like for a real customer

The agnostic story is best told concretely, not abstractly. A representative example:

A mid-market customer is spending $40,000/month on Azure. Their bill has grown faster than their usage. They engage Aptum for a Cloud Repatriation Assessment. The assessment finds three categories of workload:

- **Workload A (cloud-native, bursty, integrated with Azure-only services):** stays on Azure. The assessment identifies $10,000/month of right-sized Azure spend. Aptum manages this through the Aptum Portal as part of the multi-cloud managed services pillar.
- **Workload B (predictable production VMs, compliance-friendly, Aptum sovereignty an advantage):** moves to Aptum IaaS Dedicated Cloud. Steady-state cost: $2,000/month.
- **Workload C (database tier with high IO, latency-sensitive, fits a tuned dedicated server better than a virtualized environment):** moves to Aptum dedicated servers. Steady-state cost: $6,000/month.

Pre-Aptum: $40,000/month on Azure, with the customer carrying the operational burden.

Post-Aptum: $18,000/month total ($10K Azure + $2K Aptum IaaS + $6K dedicated server) plus managed services layered on top of all three. The customer saves money, the workloads are placed where they belong, and Aptum has three service relationships where Azure had one. This is what "the right workload on the right platform" looks like operationally, and it is the kind of outcome the strategy is organized to produce.

---

## Motion 2: Execute -- Professional Services Delivery

The Execute motion sits between Advisory and Operate. It is the project-based work that acts on assessment findings and prepares the customer's environment for ongoing managed services.

### The Advisory/Execute Distinction

This is a critical organizational and commercial distinction:

| Dimension | Advisory (Assess) | Execute (Implement) |
| --- | --- | --- |
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
| --- | --- | --- | --- |
| Cloud Migration | Workload assessment, migration plan, execution | Hybrid Cloud Assessment, Cloud Repatriation Assessment | Customer lands on Aptum IaaS or Aptum Portal-managed Azure/AWS, buys managed services |
| Repatriation Project | Workload moved from hyperscaler to Aptum Dedicated Cloud or Private Cloud | Cloud Repatriation Assessment | Customer on Dedicated Cloud (KVM/Aptum Portal) or Private Cloud (VMware/Proxmox) with full managed services stack |
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
1. Assessment-driven pipeline. Today, PS engagements arrive ad hoc. With the advisory motion formalized, every Execute engagement should trace back to an assessment that produced the findings and the business case. This makes scoping faster (the assessment already mapped the environment), delivery more predictable (the assessment already identified the risks), and conversion more likely (the customer has already invested in understanding the problem).

---

## Motion 3: Operate -- The Managed Services Destination

Every advisory engagement and every execution project should have a clear line of sight to an operate outcome. If the answer to "where does this lead in terms of recurring managed services?" is "nowhere," the engagement does not align with the strategy.

The managed services catalog (see separate document) defines the five layers in detail. The assessment framework adds a new dimension: assessment-driven onboarding paths that connect specific assessment findings to specific managed service layers.

### Assessment-Driven Onboarding Paths

Every assessment produces findings that map to a specific engagement tier and addon stack. For the full path detail, see the [Managed Services Catalog](https://aptum.atlassian.net/wiki/spaces/PRD/pages/5257560095/Managed+Services+Catalog).


---

## The Service Teams That Deliver This

Each motion is delivered by specific operational teams. The organizational model does not require a reorg. The motion determines ticket routing and resource allocation, not the org chart.


---

## Aptum Portal: The Portal Strategy

The Aptum Portal today does provisioning well. VPC self-service is live. Azure subscription management is live. Cloudflare DNS is live. The monetization engine (catalogs, pricing, billing) works.

The portal's strategic role is to make Aptum's products and services easier for Aptum's customers to consume. The underlying software (CloudMC, also called CloudOps Software) was originally built and sold as a B2B2B SaaS for service providers. That motion has had limited traction over multiple years and is no longer a primary GTM focus. The pivot is to use the portal to sell Aptum's own products and services more effectively. The standalone B2B2B sale remains possible for the existing anchor tenants and inbound demand, but new investment is organized around in-Aptum use, not outbound resale.

What the Aptum Portal does not yet do is surface the managed services layers. A customer paying for Managed OS, application performance monitoring, managed backup, and managed detection and response cannot see any of that in the portal. The managed services are operationally delivered but invisible.

This is the highest-priority product gap. Making managed services visible in the portal converts the Aptum Portal from a provisioning tool into a retention engine.

Making managed services visible in the portal is the highest-priority product gap. L1 and L2 visibility (monitoring dashboards, patch compliance, backup status) affect every managed customer and should be the engineering priority. See the [Managed Services Catalog](https://aptum.atlassian.net/wiki/spaces/PRD/pages/5257560095/Managed+Services+Catalog) for the full integration roadmap.

---

## Revenue Engines and Growth Path

### Engine 1: Managed Services Stacking on Existing Base (Defend and Expand)

The immediate opportunity. 773 existing customers, 6.5% managed services penetration. The contract renewal wave (72.74% of revenue within 6 months) is both a risk and an opportunity because every renewal conversation is a stacking conversation.

The assessment framework supercharges this engine. Instead of a generic upsell pitch at renewal, the AE offers an assessment. The assessment produces evidence. The evidence justifies the investment.

Recommended assessment plays for existing base:

- Hosting-only customers (429 accounts, $659K/mo): Infrastructure Risk Assessment or Operational Maturity Assessment. These customers are sitting on aging infrastructure with no managed services. The assessment quantifies the risk they are carrying.
- Multi-LOB customers (135 accounts, $1.8M/mo): Security Posture Assessment or Hybrid Cloud Assessment. These customers already buy across product lines. The assessment identifies the next layer of managed services to stack.
- Cloud-only customers (~116 accounts, $18K/mo): Well-Architected Review. These customers are on hyperscaler infrastructure managed through Aptum Portal. The review identifies optimization opportunities and opens the managed services conversation.

The contract renewal concentration (72% of revenue expiring within 6 months) makes every renewal conversation an assessment opportunity.

### Engine 2: New Logo Acquisition on Aptum IaaS (Grow)

The Ignite program proved the model: 7 new logos, $39K/mo MRC, 74 to 89% gross margins. The board has directed a fast-follow GTM timeline.

For new logos, the assessment is the first engagement. The customer does not start by signing a managed services contract. The customer starts by paying $5K to $40K for an assessment that maps their environment, quantifies their pain, and produces a roadmap that happens to land on Aptum infrastructure and services.

Recommended assessment plays for new logos:

- VMware customers feeling Broadcom pressure: Hybrid Cloud Assessment or Cloud Repatriation Assessment. The assessment builds the business case for moving to Dedicated Cloud (KVM/CloudStack via Aptum Portal) or Private Cloud (Proxmox on dedicated hardware) on Aptum IaaS.
- Cloud-fatigued mid-market: Cloud Repatriation Assessment. The assessment documents the overspend and models the savings from selective repatriation.
- Compliance-driven organizations: Security Posture Assessment. The assessment documents the compliance gaps and positions Aptum's managed security stack as the remediation path.

The Broadcom disruption is the market catalyst. 35% of VMware workloads migrating by 2028 per Gartner. Aptum's CloudStack and Proxmox alternatives, delivered through Aptum Portal with managed services stacking, are a direct answer.

### Engine 3: MSP/Reseller Channel (Scale)

ES Williams (Ignite customer) is already being explored as an early reseller model beta customer. The Aptum Portal white-label capability, combined with the monetization engine, lets MSPs build their own branded infrastructure and managed services offerings on top of Aptum's platform.

Target MSP profile: Regional MSPs with 50 to 500 end customers, currently running VMware Cloud Director, squeezed by Broadcom pricing, looking for an alternative infrastructure partner. These are the MSPs Marc Pare described: "They've been so squeezed by Broadcom and other stuff that they can't operate and run it themselves and are looking for a partner who can."

The Latitude.sh and Megaport intersection in Miami, as discussed in the March 31 product meeting, is a test point for this model. Latitude provides commodity bare metal, Megaport provides the channel relationships, and Aptum provides the managed services and consulting layer on top.

### Engine 4: Assessment-Led Pipeline (Open Doors)

This is the new engine, formalized by the STG Assessment Playbook. It is the mechanism that feeds Engines 1 through 3.


---

## The MAAS Differentiator

The CloudStack 4.22 Extensions Framework enables integration with Canonical MAAS (Metal as a Service) without core Java development. When MAAS is implemented, Aptum will be able to offer bare-metal provisioning through the same Aptum Portal portal that handles VMs, public cloud, and managed services.

This is a market differentiator because no other mid-market MSP offers self-service bare metal + VPC + private cloud + hyperscaler management through a single portal with managed services layered on top. The closest competitors (OVH, Hetzner) offer bare metal but not managed services. The managed services competitors (Rackspace, Navisite) offer managed services but not self-service bare metal.

MAAS is on the Phase 2 roadmap (Q3 to Q4 2026) alongside Proxmox and Kubernetes.

---

## What We Stop Doing

Strategic clarity requires saying no to some things:

We stop positioning VPC as a lead product for new logos. Marc Pare was explicit: VPC is the "french fries, not the hamburger." It is a cost management and margin play for existing workloads, not a go-to-market product. New logo hunting leads with Dedicated Cloud, Private Cloud, and managed services.

We stop reselling hyperscaler subscriptions at a loss. Ian Rae identified this directly for Azure: "We have to get out of the mindset of I'm going to resell Azure and support at a loss." The principle is the same for AWS and GCP. Hyperscaler subscription revenue is a vehicle for managed services revenue, not an end in itself. The margin is in the management layer, not the resell.

We stop building service guides around vendor names. Service guides describe outcomes, not implementations. The customer buys "Managed Backup," not the underlying tool. They buy "App Performance Monitoring," not the specific platform. Vendors and tools are implementation details that the delivery teams care about; they are not the product the customer is buying. This also creates the freedom to swap implementation vendors without breaking the customer-facing product.

We stop hiding the agnostic guidance behind a managed-services-first reflex. The brand promises tech-agnostic guidance: the customer should expect Aptum to recommend the right answer for their situation, even when that answer is "stay on AWS, here is how to optimize." The advisory motion is built to do this honestly. The downstream conversion to Aptum-stack services depends on the credibility of the upstream advice, not on steering it.

We stop selling the Aptum Portal (or its underlying software, CloudMC/CloudOps Software) as a primary B2B2B product. Existing anchor tenants are honored; the standalone B2B2B sales motion is no longer a primary GTM focus. The portal exists to make Aptum's own products and services easier to consume.

We stop chasing large enterprise accounts as sustainable managed services customers. Telesat, CN, Bell: these are consulting engagements, not managed services relationships. Ian Rae: "An organization that has 10,000 employees and has an IT department that is 3 times the size of Aptum is not going to be like, Aptum, we want you to manage all of our public cloud stuff."

We stop running professional services as an undifferentiated bucket. The advisory/execute distinction is now formalized. Assessments are advisory. Migrations, builds, and remediations are execute. They have different delivery models, different commercial models, different success metrics, and different team structures. Treating them as one blended "PS" line masks both the strategic value of advisory and the operational discipline required for execute.

We do not adopt Build-Operate-Transfer (BOT) as a strategic motion. BOT remains useful as a customer-facing reassurance ("yes, you can bring this back in-house if you want to") that is consistent with the brand promise of "maintained with or without us." It is not a goal. The product goal is Assess to Build to Operate, forever, where forever is earned by operating better than DIY.

---

## Roadmap Summary

| Phase | Timeline | Focus | Key Milestones |
| --- | --- | --- | --- |
| Phase 1 | Q2 2026 | Revenue enablement, GTM for Aptum IaaS, assessment pipeline activation, advisory/execute PS split | Ignite customer migrations complete, pricing validated with finance, commercial team armed with managed services catalog + assessment sell sheets, portal L1+L2 visibility scoped, first 3-5 assessments pitched |
| Phase 2 | Q3 to Q4 2026 | Catalog expansion, MSP channel recruitment, assessment pipeline scaling | MAAS integration, Proxmox via CloudStack Extensions, second DC scoping, first MSP reseller signed, managed services penetration from 6.5% to 15%, 8-10 assessments delivered, PS service manager hired |
| Phase 3 | H1 2027 | Multi-region, channel scale, assessment framework maturity | AWS/GCP activation in Aptum Portal, multi-region infrastructure (Miami or second Toronto), channel revenue exceeding $100K MRC, assessment-to-operate conversion rate exceeding 60% |

---

## Open Items Requiring Resolution

1. Aptum Portal naming is resolved (the previous placeholder was the old name). The supporting Confluence pages ([AptCloud - Aptum IaaS Strategy](https://aptum.atlassian.net/wiki/spaces/PRD/pages/5257494536/AptCloud+-+Aptum+IaaS+Strategy), [AptCloud - Aptum IaaS PRD](https://aptum.atlassian.net/wiki/spaces/PRD/pages/5257560073/AptCloud+-+Aptum+IaaS+PRD)) still carry the old AptCloud prefix in their titles and should be renamed in a separate housekeeping pass.
1. AI and GPU positioning is undecided. Aptum sits at the server level and does not buy GPUs. There is real customer demand and partner interest (5C.ai for AI private clouds, the broader market for AI infrastructure), and there are partner conversations in flight. The strategy does not currently take a position on whether AI infrastructure becomes a Phase 3 roadmap item, a partner-led offering, or a deliberate "stop doing." A decision is needed; until then, opportunistic engagement is acceptable but should not drive product commitments.
1. Professional Services needs a service manager. The operating model has a gap. No single owner coordinates PS delivery (both advisory and execute), resource allocation, and margin accountability. With the advisory/execute formalization, this role becomes even more critical: the PS service manager needs to own assessment pipeline tracking, delivery quality, and follow-on conversion metrics.\
   **Update (April 15, 2026):** The CEM/customer relationship gap previously noted has been resolved by splitting Lacie's org into two distinct functions: HSDM (project delivery / Execute motion, non-recurring) and a new Customer Success Management (CSM) function (recurring customer ops, queues, orders, renewals, proactive retention). Both report to Lacie Allen-Morley. HSDM hands to CSM at project close; CSM hands back to HSDM at new engagement start.
1. Alert Logic MDR timeline and commercial model are undefined. Listed as "IN DEVELOPMENT" in service guides. Is it partner-delivered (Alert Logic SOC) or Aptum-operated with Alert Logic tooling? This directly affects the Security Posture Assessment follow-on path.
1. Pricing for managed service layers is placeholder. The catalog uses ranges ($2K to $5K, $3K to $8K). These need validation with Sarah Blanchard (finance) and Fred's commercial team before the sales team can quote. Assessment follow-on conversion depends on having firm pricing to present alongside assessment findings.
1. Portal integration engineering effort is unknown. 15+ integration points identified in the catalog (Zabbix, Veeam, Datadog, JSM, Alert Logic, etc.) with no LOE estimates from Will's team.
1. Jason's team needs CloudStack/KVM/Proxmox training plan. The decision that Service Desk owns infrastructure ops for new commodities depends on this investment.
1. The "two-Zabbix problem" (internal monitoring vs. customer-facing monitoring consolidation) needs a VP-level mandate. Jorge's Operational Intelligence team has flagged it but cannot resolve it without organizational authority.
1. Assessment sell sheets and delivery guides need commercial team enablement. The STG playbook materials exist but have not been trained into the AE and SA teams. Phase 1 (Q2 2026) must include enablement sessions covering the assessment portfolio, t-shirt sizing, discovery questions, and follow-on mapping.
1. The 36-account customer-to-assessment matrix needs validation with the commercial team. The pre-mapping of accounts to primary and secondary assessments should be reviewed by AEs who own those relationships.

---

*Sources: dimServices extract (April 1, 2026), Aptum Identity & Values (Confluence, Marketing space), Aptum Messaging (Confluence, Marketing space), Product Strategy v1.3.1 (Confluence, treated as historical), CloudOps SW Product Strategy 1.0 (Confluence, B2B2B framing now superseded), Service Guides (Confluence), Product Discussion VTT (March 31, 2026), [AptCloud - Aptum IaaS Strategy](https://aptum.atlassian.net/wiki/spaces/PRD/pages/5257494536/AptCloud+-+Aptum+IaaS+Strategy), [AptCloud - Aptum IaaS PRD](https://aptum.atlassian.net/wiki/spaces/PRD/pages/5257560073/AptCloud+-+Aptum+IaaS+PRD), [Managed Services Catalog](https://aptum.atlassian.net/wiki/spaces/PRD/pages/5257560095/Managed+Services+Catalog), Service Team descriptions (all 9 teams), STG Assessment & Commercial Playbook v1.0 (7 assessments, engagement workflow, revenue model, success metrics, post-assessment pathways), Reanchor session notes (April 1, 2026), Ian Rae Transition document 1.1 DRAFT (April 27, 2026), Dave Pistacchio review email (April 28, 2026).*
