# Aptum Product Strategy
## From Commodity Hosting to Hybrid Cloud Managed Services
**Version 1.0 | April 1, 2026**

---

## The Position

Aptum is a hybrid cloud managed services provider. The aspiration is to be the company that makes infrastructure disappear into the background for mid-market organizations, so they can focus on their business instead of managing servers, patching operating systems, and arguing about firewall rules.

The company has two core assets that make this possible:

1. Apt Cloud (the portal, the control plane, the customer experience). Powered by CloudOps Software (formerly CloudMC). This is what the customer sees and touches. It delivers self-service provisioning, cost visibility, lifecycle management, and will increasingly surface the managed services the customer is paying for.

2. Aptum IaaS (the infrastructure). Compute, storage, networking on Apache CloudStack 4.22 with KVM virtualization. Delivered as VPC (multi-tenant) and Private Cloud (single-tenant). This is the foundation that replaces commodity dedicated hosting and offers an alternative to hyperscaler infrastructure at better economics.

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

75% of revenue is hosting. Most of that is commodity dedicated servers with minimal managed services layered on top. Cloud services are 2.57%. The strategy requires inverting this ratio over time, not by abandoning hosting, but by stacking managed services on top of it and growing new-logo cloud revenue.

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

---

## The Two Pillars

The product discussion on March 31, 2026 (with Ian Rae, Marc Pare, Marc Alex Forget, Frederic Gingras, Will Stevens) confirmed the strategy rests on two pillars. Marc Alex Forget stated it directly: the two things that generate monthly recurring revenue are (1) multi-cloud managed services and (2) private cloud infrastructure.

Everything else, consulting, professional services, assessments, migrations, is the tip of the spear that starts relationships and leads to one or both of those pillars.

### Pillar 1: Managed Services (The Margin Multiplier)

Managed services are what differentiate Aptum from a VPS provider. They require human expertise. They create stickiness. They are the reason a customer stays when someone offers cheaper compute.

The managed services catalog defines five layers that stack on top of any infrastructure commodity:

| Layer | What It Delivers | ICP Trigger | Revenue Uplift | Delivering Team |
|---|---|---|---|---|
| L1: Infrastructure Monitoring | 24/7 hardware monitoring, alert triage, hardware replacement SLA, network monitoring | Included with all managed infra | Included (cost already incurred) | Service Desk (Jason), DC Ops (George), Network (Ben) |
| L2: Managed OS | OS patching, Veeam backup, managed firewall, endpoint security | IT teams of 2 to 15 drowning in tickets | +$2K to $5K/mo | Managed Cloud (Andrei) + Service Desk (firewall L2 ops) |
| L3: App Platform | Datadog APM, WAF, DDoS protection, L7 load balancing, DB tuning | CTOs/DevOps at SaaS/eCommerce where slow = lost revenue | +$3K to $8K/mo | Managed Cloud (Andrei) |
| L4: Security & Compliance | Alert Logic MDR, compliance reporting, vulnerability scanning | Regulated industries (healthcare, finance, government) | +$2K to $5K/mo | Managed Cloud (Andrei) + Alert Logic (partner) |
| L5: Business Continuity | DRaaS, BCP planning, hybrid interconnects (ExpressRoute/Direct Connect), M365, managed DNS | Any customer with uptime requirements or hybrid architecture | +$1.5K to $5K/mo | Managed Cloud (Andrei) + Network (Ben) |

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

Compare to the same customer buying unmanaged VPC only: $7,000/mo. Managed services nearly triple revenue per customer.

### Pillar 2: Aptum IaaS / Private Cloud (The Infrastructure Foundation)

Aptum IaaS, delivered through Apt Cloud, is the new infrastructure product. It replaces the legacy dedicated hosting model with a modern, self-service, software-defined infrastructure platform.

Two delivery models:

| Model | Tenancy | Target Customer | Use Case |
|---|---|---|---|
| VPC | Multi-tenant (shared compute) | Cost-conscious workloads, dev/test, general purpose | The "french fries," as Marc Pare described it. Not the lead product for new logos, but a cost-effective option that complements managed services. |
| Private Cloud | Single-tenant (dedicated hosts) | Production workloads, compliance-sensitive, performance-critical | The lead product for new logo hunting. Repatriation and rebalancing conversations. Dedicated compute managed through the same portal. |

The board demo on March 31 confirmed production readiness. Dave Pistacchio called it "true private cloud" and directed the team to determine a fast-follow GTM timeline.

Pre-launch validation: 7 Ignite customers, $39,119/mo CAD MRC, 36-month contracts. Gross margins of 74 to 89%.

Key differentiators vs. hyperscalers:
- Predictable pricing (per vCPU/GB, no transaction costs, no surprise egress)
- Data sovereignty (Canadian-owned, Toronto DC with SOC 2 Type II)
- Single portal for private + public cloud (Apt Cloud manages both Aptum IaaS and Azure/AWS/GCP)
- Managed services layered on top (hyperscalers don't do this, that's the customer's problem)

Key differentiators vs. commodity hosting providers (OVH, Hetzner, DigitalOcean):
- Managed services stack (they sell infrastructure, Aptum sells outcomes)
- Enterprise-grade portal with RBAC, multi-tenant governance, cost visibility
- MSP/reseller white-label capability (ES Williams/Ignite model)
- Consulting and professional services to design and migrate

---

## The Tip of the Spear: Consulting and Professional Services

Professional services are not a pillar. They are the opening move. Every long-term customer relationship (Canderel, Clear Destination, Woodwell Climate Research Center) started with a consulting engagement.

The goal is for every PS engagement to have a clear line of sight to one or both pillars:

| PS Engagement | What It Produces | Where It Leads |
|---|---|---|
| Cloud Migration | Workload assessment, migration plan, execution | Customer lands on Aptum IaaS or Apt Cloud-managed Azure/AWS, buys managed services |
| Repatriation Assessment | Business case for moving workloads off hyperscalers | Customer lands on VPC or Private Cloud |
| Security Audit | Posture assessment, gap analysis, remediation roadmap | Customer buys Alert Logic MDR, compliance reporting, managed firewall |
| FinOps Assessment | Cloud spend analysis, right-sizing, optimization | Customer consolidates through Apt Cloud, buys managed cloud |
| Hardware Refresh | EOL server replacement | Customer moves from legacy dedicated to VPC or Private Cloud |
| DR Design | Failover architecture, runbook, first test | Customer buys DRaaS, hybrid interconnects |

PS engagement revenue: $5K to $75K per engagement. But the real value is the $15K to $48K/mo in recurring managed services revenue that follows.

Marc Pare was clear: "The consulting is the start of the relationship, not the end. You're doing it to build trust, get acquainted, understand their problems, and then position longer-term solutions."

---

## The Service Teams That Deliver This

Each managed service layer is delivered by specific operational teams. The organizational model does not require a reorg. The product tier defines ticket routing, not the org chart.

### Team Domain Map

| Team | Leader | Domain | Role in Strategy |
|---|---|---|---|
| Service Desk / NOC | Jason Auer | Infrastructure operations (24/7), all commodity types | Operates L1 monitoring, dispatches hardware replacement, L2 firewall ops. 17 people, 3 shifts. Owns day-2 for ~4,569 services. |
| Managed Cloud | Andrei Ianouchkevitch | OS layer and above, all cloud platforms | Operates L2 through L5 managed services. Patching, backup, Datadog, WAF, DDoS, DRaaS, hybrid interconnects. Enables ~$7.6M hyperscale revenue. |
| Compute Platforms | Martin Tessier | Server builds, configuration standards, automation | Builds compute environments from bare metal to OS. CloudStack, Proxmox, ESXi. Hands off to Service Desk or Managed Cloud. |
| Data Center Ops | George Revie | Physical infrastructure across 8 locations | Racks, cabling, power, cooling, physical security, colocation. Remote hands and hardware remediation. ~5,491 services. |
| Networking | Ben Kennedy | MPLS, internet, cloud connects, IP management | OSI Layer 1 to 3. Juniper switching estate (81 units). 15+ carriers via meet-me-rooms. |
| HSA (Hybrid Solution Architecture) | Pat Wolthausen + 3 architects | Pre-sales design, SOW scoping, architectural delivery | Defines technical scope for every SOW. Target: 50%+ billable utilization. |
| HSDM (Service Delivery) | Lacie Allen-Morley | Customer relationship, SOW execution, renewals | Single point of contact across engagements. Owns ~$13.5M customer revenue. |
| Professional Services | (Open, no defined manager) | Project-based execution | Cross-functional delivery, contributing teams from all service areas. $738K YTD, 29.2% margin. |
| Operational Intelligence | Jorge Quintero | Data pipelines, unified customer view, metrics | Discovery phase. Already recovered ~$466K margin correction. Addresses "two-Zabbix problem." |

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

Target: Move managed services penetration from 6.5% to 15% within 12 months. At current portfolio size, that represents approximately $100K to $250K in incremental MRC from upsell alone.

Execution:
- Assign managed services stacking targets to every renewal in the pipeline
- Arm sales with the managed services catalog (Layers 2 to 5 with pricing)
- Use the portal visibility roadmap to show customers what they're getting
- Prioritize the 135 multi-LOB customers (they already buy across product lines)

### Engine 2: New Logo Acquisition on Aptum IaaS (Grow)

The Ignite program proved the model: 7 new logos, $39K/mo MRC, 74 to 89% gross margins. The board has directed a fast-follow GTM timeline.

Target: Phase 1 (Q2 2026) focuses on revenue enablement and operational readiness. Phase 2 (Q3 to Q4 2026) expands the catalog (MAAS, Proxmox, Kubernetes) and recruits MSP resellers. Phase 3 (H1 2027) scales to multi-region and activates AWS/GCP through the portal.

The Broadcom disruption is the market catalyst. 35% of VMware workloads migrating by 2028 per Gartner. Aptum's CloudStack and Proxmox alternatives, delivered through Apt Cloud with managed services stacking, are a direct answer.

New logo qualification should filter against the ICP: mid-market, 50 to 2,000 employees, hybrid workloads, overwhelmed IT team, $10K to $100K/mo MRC potential.

### Engine 3: MSP/Reseller Channel (Scale)

ES Williams (Ignite customer) is already being explored as an early reseller model beta customer. The Apt Cloud white-label capability, combined with the monetization engine, lets MSPs build their own branded infrastructure and managed services offerings on top of Aptum's platform.

Target MSP profile: Regional MSPs with 50 to 500 end customers, currently running VMware Cloud Director, squeezed by Broadcom pricing, looking for an alternative infrastructure partner. These are the MSPs Marc Pare described in the product discussion: "They've been so squeezed by Broadcom and other stuff that they can't operate and run it themselves and are looking for a partner who can."

The Latitude.sh and Megaport intersection in Miami, as discussed in the March 31 product meeting, is a test point for this model. Latitude provides commodity bare metal (the "Model T Ford, you want it, it's black"), Megaport provides the channel relationships, and Aptum provides the managed services and consulting layer on top.

### Engine 4: Professional Services (Open Doors)

Not a growth engine in isolation, but the mechanism that opens the door to Engines 1 through 3.

Current state: $738K YTD revenue, 29.2% gross margin. The PS organization lacks a defined service manager (noted in the team descriptions). This is a gap that needs to be filled.

Every PS engagement should have a defined "land to" outcome: which pillar (managed services or private cloud infrastructure) does this engagement lead the customer toward? If the answer is "neither," the engagement doesn't align with the strategy.

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

We stop building service guides around vendor names. Adam's direction: service guides should be void of other companies' products unless explicitly necessary. The customer buys "Managed Backup," not "Veeam." They buy "App Performance Monitoring," not "Datadog." The vendor is the implementation detail, not the product.

We stop chasing large enterprise accounts as sustainable managed services customers. Telesat, CN, Bell: these are consulting engagements, not managed services relationships. Ian Rae: "An organization that has 10,000 employees and has an IT department that is 3 times the size of Aptum is not going to be like, Aptum, we want you to manage all of our public cloud stuff."

---

## Roadmap Summary

| Phase | Timeline | Focus | Key Milestones |
|---|---|---|---|
| Phase 1 | Q2 2026 | Revenue enablement, GTM for Aptum IaaS, managed services stacking on existing base | Ignite customer migrations complete, pricing validated with finance, commercial team armed with managed services catalog, portal L1+L2 visibility scoped |
| Phase 2 | Q3 to Q4 2026 | Catalog expansion, MSP channel recruitment | MAAS integration, Proxmox via CloudStack Extensions, second DC scoping, first MSP reseller signed, managed services penetration from 6.5% to 15% |
| Phase 3 | H1 2027 | Multi-region, channel scale | AWS/GCP activation in Apt Cloud, multi-region infrastructure (Miami or second Toronto), channel revenue exceeding $100K MRC |

---

## Open Items Requiring Resolution

1. Apt Cloud needs a new name. The current name creates confusion with "App Cloud" in conversation and is not differentiated in market. This is a known issue without a resolution date.

2. Professional Services needs a service manager. The operating model has a gap. No single owner coordinates PS delivery, resource allocation, and margin accountability.

3. Alert Logic MDR timeline and commercial model are undefined. Listed as "IN DEVELOPMENT" in service guides. Is it partner-delivered (Alert Logic SOC) or Aptum-operated with Alert Logic tooling?

4. Pricing for managed service layers is placeholder. The catalog uses ranges ($2K to $5K, $3K to $8K). These need validation with Sarah Blanchard (finance) and Fred's commercial team before the sales team can quote.

5. Portal integration engineering effort is unknown. 15+ integration points identified in the catalog (Zabbix, Veeam, Datadog, JSM, Alert Logic, etc.) with no LOE estimates from Will's team.

6. Jason's team needs CloudStack/KVM/Proxmox training plan. The decision that Service Desk owns infrastructure ops for new commodities depends on this investment.

7. The "two-Zabbix problem" (internal monitoring vs. customer-facing monitoring consolidation) needs a VP-level mandate. Jorge's Operational Intelligence team has flagged it but cannot resolve it without organizational authority.

---

*Sources: dimServices extract (April 1, 2026), Product Strategy v1.3.1 (Confluence), CloudOps SW Product Strategy 1.0 (Confluence), Service Guides (Confluence), Product Discussion VTT (March 31, 2026), AptCloud/Aptum IaaS Strategy v1.2, AptCloud/Aptum IaaS PRD, Managed Services Catalog, Service Team descriptions (all 9 teams), Reanchor session notes (April 1, 2026).*
