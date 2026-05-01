# Aptum Managed Services Catalog
## Value-Added Products Layered on Aptum Portal Commodities
**Version 2.1 | April 28, 2026**

---

## The Reframe

The old tiering model mixed infrastructure products with managed services in a vertical stack. This model separates them into three distinct tiers:

- **Infrastructure Commodities** are the base products — hardware, connectivity, compute, and cloud access that Aptum provisions. Included with every commodity is a **Fundamental** layer: the baseline guarantee that the product works as sold. This is non-negotiable and cannot be removed or purchased separately.
- **Machine Managed** addons activate automated tooling on the customer's environment. The machine does the work — scheduling, executing, reporting, exposing data. The customer or Aptum's Service Desk is in the decision loop and reacts when something needs attention. The customer retains control over decisions.
- **Expert Managed** addons put Aptum's expert team in the driver's seat proactively. The expert team prevents problems rather than reacting to them — installing the fire suppression system, not just responding to the fire. The customer does not need to be involved in routine decisions.

Every customer's environment sits on an infrastructure commodity with its Fundamental guarantee included. Machine Managed and Expert Managed addons are purchased on top. Some addons offer both tiers independently; a customer can buy Machine Managed without Expert Managed.

The assessment framework (see `/53-products/aptum-product-strategy.md` v2.1) defines how customers enter this catalog. Structured advisory assessments diagnose the customer's environment and produce findings that map directly to specific layers. The assessment report becomes the evidence base that justifies each layer's investment. The table below summarizes the assessment-to-layer mapping; detailed onboarding paths appear at the end of this document.

---

## Naming convention: products vs. implementation

Customer-facing product names in this catalog are vendor-neutral. The customer buys "Managed Backup," not the underlying tool. The implementation detail (which platform delivers the service) is captured in the description column where it informs delivery teams. This is a deliberate choice: vendor neutrality in product names protects flexibility (Aptum can change implementations without changing product SKUs) and aligns with the brand promise of tech-agnostic guidance. Service guides for delivery teams may reference specific vendor tooling; customer-facing materials should not.

---

## Infrastructure Commodities

These are the "base products." Customers can consume them self-service (where available) or have Aptum provision them. The infrastructure itself is not the margin story; it is the entry point.

| Core Product | Technology | Provisioning & Portal | Fundamental (Always Included) |
|---|---|---|---|
| **Colocation** | Physical data center space: rack units, power (kW), cooling, physical security | Manual (Data Center Ops); Portal: future — power and bandwidth visibility | Power on, temperature within range, physical security maintained, rack space available. Network connectivity is a separate purchase. |
| **Connectivity** | MPLS, internet ports, BGP, transit, cross-connects, fiber | Manual (Networking); Portal: future — bandwidth utilization and uptime visibility | BGP and routing healthy, 99.999% uptime SLA maintained. SD receives monitoring alerts, escalates to Network team for resolution. |
| **Bare Metal** | Aptum-owned single-tenant physical servers | Manual today (Compute Platforms + Data Center Ops); Portal: roadmap via BMaaS (self-service provisioning) | Server powered and network-connected, Zabbix monitoring active, failed hardware components (PSU, disk, CMOS) replaced within SLA, OS deployed per standard build, L2 triage included. SD Day 2 mandatory and non-removable. |
| **Private Cloud** | VMware or Proxmox on dedicated hardware, built per-customer | Manual (SA specs, Compute Platforms builds); Portal: not applicable (Phase 1) | All Bare Metal fundamentals plus VMware/Proxmox hypervisor healthy, vCenter/cluster operational, storage connected. Service Desk owns the hypervisor layer. |
| **Shared Cluster (VPC)** | CloudStack/KVM on Aptum-owned shared hosts, multi-tenant | Self-service via Aptum Portal — live | Platform available, VMs in running state, CloudStack/KVM layer healthy, storage functioning, baseline platform triage priced into product floor. |
| **Dedicated Cluster** | CloudStack/KVM on Aptum-owned dedicated hosts, single-tenant | Aptum Portal — live (SA involved for initial sizing) | Dedicated cluster available, VMs in running state, CloudStack/KVM cluster healthy, storage functioning, baseline platform triage priced into product floor. |
| **Public Cloud** | Azure, AWS, GCP via Aptum CSP/partner agreements | Hyperscaler portals (self-service); Aptum Portal: cost and consumption visibility — live | CSP subscription active, billing consolidated through Aptum, Aptum communicates hyperscaler outages and relevant status to customers proactively. |

---

## Managed Service Addons

These are the purchasable addons that stack on top of any infrastructure commodity. Each addon is independently sellable, priced per asset or endpoint per month, and has a defined owner from the Aptum service network. Each addon is available as **Machine Managed** (automated tooling, customer in decision loop), **Expert Managed** (proactive expert ownership), or both. *Note: "Machine Managed" and "Expert Managed" are working internal terms. Customer-facing naming to be finalised.*

---

## Compatibility Matrix

**MM** = Machine Managed available. **EM** = Expert Managed available. **MM+EM** = both available independently. **—** = not applicable to this product.

| Addon | Colo | Connectivity | Bare Metal | Private Cloud | IaaS (VPC / Dedicated) | Public Cloud |
|---|---|---|---|---|---|---|
| Infrastructure Monitoring (visibility) | — | MM | MM | MM | MM | MM |
| Advanced Monitoring / APM | — | — | MM+EM | MM+EM | MM+EM | MM+EM |
| OS Patching | — | — | MM+EM | MM+EM | MM+EM | MM+EM |
| Application Platform Patching | — | — | MM+EM | MM+EM | MM+EM | MM+EM |
| Managed Backup | EM | — | MM+EM | MM+EM | MM+EM | MM+EM |
| DRaaS | — | — | MM+EM | MM+EM | MM+EM | MM+EM |
| BCP Planning | — | — | EM | EM | EM | EM |
| Managed Firewall | — | MM+EM | MM+EM | MM+EM | MM+EM | MM+EM |
| Antivirus / EDR | — | — | MM+EM | MM+EM | MM+EM | MM+EM |
| WAF | — | — | MM+EM | MM+EM | MM+EM | MM+EM |
| DDoS Protection | — | MM | MM+EM | MM+EM | MM+EM | MM+EM |
| Load Balancing (L7) | — | — | MM+EM | MM+EM | MM+EM | MM+EM |
| MDR | — | — | MM+EM | MM+EM | MM+EM | MM+EM |
| Vulnerability Scanning | — | — | MM+EM | MM+EM | MM+EM | MM+EM |
| Compliance Reporting | — | — | EM | EM | EM | EM |
| Hybrid Interconnects | — | MM+EM | MM+EM | MM+EM | MM+EM | MM+EM |
| FinOps / Cost Optimization | — | — | — | — | MM | MM+EM |
| Operational Logging | — | — | MM+EM | MM+EM | MM+EM | MM+EM |
| Reviews & Touchpoints | EM | EM | EM | EM | EM | EM |
| Managed DNS | — | — | MM | MM | MM | MM |
| Managed Productivity (M365) | — | — | MM+EM | MM+EM | MM+EM | MM+EM |
| Database Tuning | — | — | MM+EM | MM+EM | MM+EM | MM+EM |
| DevOps Monitoring & Maintenance | — | — | MM+EM | MM+EM | MM+EM | MM+EM |

---

## Bare Metal -- Cost Structure and Contract Pricing

The Bare Metal product price reflects six components. **Only the margin component is discountable.** The cost base is not negotiable below cost.

| Component | Description |
|---|---|
| Physical server | CapEx amortized over the contract term. Residual value at term end: 40% (12mo), 20% (24mo), 0% (36mo). |
| Power | Per-kW cost varies by data center location (illustrative: Herndon $110/kW, Atlanta $337/kW, Miami $48/kW, Los Angeles $457/kW, Toronto/Montreal $253/kW, Portsmouth $46/kW). |
| Data Center Ops | Data Center Ops labor allocated per server -- facilities, rack, physical ops. |
| Network | Network team cost allocated per server (~$59/server). |
| **Service Desk (mandatory managed layer)** | **Service Desk labor. Included in every Bare Metal server. Not optional, not removable.** (~$40 CAD/asset/month fully loaded across 3,982 managed assets). |
| Licensing | OS and software licensing where applicable. |

**Contract term pricing -- illustrative example (Pro Series 6.0, Herndon DC):**

| Term | Residual Value | List MRC | Effective MRC |
|---|---|---|---|
| 12 months | 40% | $1,521.39 | $1,521.39 |
| 24 months | 20% | $1,521.39 | $1,182.99 |
| 36 months | 0% | $1,521.39 | $1,013.79 |
| Month-to-month | n/a | Full list | Full list |

*Pricing varies by server spec and data center location. The above is illustrative for one server configuration at one location. The margin component -- the difference between cost base and list MRC -- is the only component that can be discounted in commercial conversations.*

---

## Addon Detail

Each addon below shows what it is, what it is not (where there is room for confusion), how Machine Managed and Expert Managed tiers differ, which service network team owns it, and real costs for both tiers. Costs in CAD unless noted. USD conversions approximate at current rates.

### Monitoring & Observability

| Addon | What It Is | Machine Component | Machine Cost (CAD/mo) | Human Component | Human Add-On Cost | Status |
|---|---|---|---|---|---|---|
| **Infrastructure Monitoring** | 24/7 monitoring of hardware health, availability, and connectivity. Automated alerting and ticket creation on threshold breaches. Hardware replacement dispatched on failure. | LogicMonitor/Zabbix agent + automated alert routing + automated ticket creation | Included in SD floor (~$40 CAD/asset fully loaded) | Alert threshold tuning, pattern analysis, proactive incident response | Included in MC endpoint fee | Live |
| **Advanced Monitoring (APM)** | Full-stack observability: application performance, container health, infrastructure metrics, and custom dashboards. | Datadog agent + automated dashboards + anomaly detection + automated alerting | ~$35 CAD/host (Datadog ~$25 USD) | Dashboard configuration, alert rule design, incident response, performance review cadence | Included in MC endpoint fee | Live (MC customers) |

### OS & Platform Management

| Addon | What It Is | Machine Component | Machine Cost (CAD/mo) | Human Component | Human Add-On Cost | Status |
|---|---|---|---|---|---|---|
| **OS Patching** | Scheduled deployment of OS and security patches across supported platforms (Windows Server, Linux: Debian, Ubuntu, RHEL, Alma, Rocky). Compliance reporting. | Automox agent + automated patch scheduling and deployment + compliance reporting | ~$7 CAD/endpoint (Automox ~$5 USD) | Patch policy definition, pre-deployment testing, maintenance window coordination, post-patch validation, exception handling | MC team time (within endpoint pricing) | Live |
| **Application Platform Patching** | Updates and patches to application platform components: middleware, runtime environments, platform services. | Platform-specific tooling where automated patching is supported | TBD per platform | Platform patch testing, staged rollout coordination, compatibility validation, customer sign-off | MC team time (MCP tier) | Live (MCP customers) |

### Data Protection & Recovery

| Addon | What It Is | Machine Component | Machine Cost (CAD/mo) | Human Component | Human Add-On Cost | Status |
|---|---|---|---|---|---|---|
| **Managed Backup** | Automated backup job execution with monitoring, failure alerting, reporting, and restore capability. Policy-based retention. | Veeam automated job scheduling, monitoring, failure alerting, and success/failure reporting | Per block commitment | Backup policy design, failure investigation, restore operations, retention management, recovery testing | MC team time (within endpoint pricing) | Live |
| **DRaaS** | Defined RPO/RTO with maintained failover environment and tested recovery runbooks. Quarterly DR tests. | Backup replication to secondary site + automated failover environment maintenance | Secondary site compute + storage (scoped per engagement) | DR plan design, quarterly DR tests, failover coordination, runbook development and maintenance | MC team + PS for initial design | Live (select customers) |
| **BCP Planning & Testing** | Business Continuity Plan development, tabletop exercises, and annual review. | Automated reporting inputs for plan status and test schedule | Included | BCP document development, tabletop facilitation, annual review | Advisory/PS-led | Live |

### Security Services

| Addon | What It Is | Machine Component | Machine Cost (CAD/mo) | Human Component | Human Add-On Cost | Status |
|---|---|---|---|---|---|---|
| **Managed Firewall** | Ongoing firewall policy management, rule changes, and compliance auditing for physical (Juniper SRX) and virtual firewalls. | Automated config backup + health monitoring + automated alerting on policy violations | Included in monitoring infrastructure | Security policy management, rule creation and removal, audit log review, change management, compliance evidence collection | SD L2 (day-to-day ops) + MC (policy escalation) | Live |
| **Antivirus / EDR** | Managed antivirus and endpoint detection and response on customer servers. Alert triage and response included. | AV/EDR agent + automated definition updates + automated threat alerting and quarantine | AV/EDR license (per endpoint, TBD) | Alert triage, threat investigation, response actions, policy configuration, exclusion management | MC team time | Live |
| **WAF** | HTTP/HTTPS inspection, OWASP rule enforcement, and custom security policy management as a service. | WAF engine + automated OWASP rule updates + automated blocking of known threats + event reporting | Per WAF service guide | Policy tuning, custom rule creation, false positive management, PCI/compliance reviews | MC team time | Evolving (see WAF service guide) |
| **DDoS Protection** | Volumetric scrubbing at network edge (always-on) plus optional managed enhanced scrubbing. | BGP-level edge protection + automated scrubbing + automated attack alerting | Edge included in network infrastructure; enhanced scrubbing scoped separately | Attack response coordination, post-attack review, enhanced scrubbing policy configuration | MC + Network team | Live |
| **MDR** | 24/7 threat monitoring, SOC-as-a-service, and compliance reporting via managed SOC partner. | Alert Logic (or equivalent) automated threat detection, alerting, and reporting platform | Alert Logic license (TBD) | SOC analyst response, threat investigation, escalation management, compliance evidence collection | MC + SOC partner | IN DEVELOPMENT |
| **Vulnerability Scanning** | Scheduled vulnerability scans with remediation tracking, posture scoring, and compliance reporting. | Automated scan scheduling, automated execution, automated posture and compliance reporting | Scanning tool license (TBD) | Scan result review, remediation prioritization, posture reporting, customer guidance | MC team time | Not built |
| **Compliance Reporting** | SOC 2, PCI-DSS, HIPAA evidence collection and reporting. Leverages Aptum's own SOC 2 Type II. | Automated evidence collection tooling where available | Included where tooling exists | Evidence curation, gap analysis, customer-facing report preparation | MC + PS for initial setup | Not built; PS-led today |

### Cloud & Hybrid Connectivity

| Addon | What It Is | Machine Component | Machine Cost (CAD/mo) | Human Component | Human Add-On Cost | Status |
|---|---|---|---|---|---|---|
| **Hybrid Cloud Interconnects** | Private connectivity between Aptum infrastructure and hyperscalers (ExpressRoute for Azure, Direct Connect for AWS, Partner Interconnect for GCP). | Physical circuit (Network team) + automated circuit health monitoring | Circuit MRC (~$500–$1,500/mo, scoped per engagement) | Logical configuration, ongoing monitoring, failover management, change management | MC team (logical); Network team (physical) | Live |
| **FinOps / Cost Optimization** | Cloud spend visibility, anomaly detection, budget governance, and expert-led cost optimization recommendations. | Aptum Portal cost insights tool: automated reporting, budget alerts, anomaly detection, utilization tracking | Included in Foundation / Aptum Portal | Rightsizing analysis, reserved instance strategy, governance framework, monthly optimization reviews | MC team time | Live (MC/Foundation customers) |

### Logging & Compliance

| Addon | What It Is | Machine Component | Machine Cost (CAD/mo) | Human Component | Human Add-On Cost | Status |
|---|---|---|---|---|---|---|
| **Operational Logging** | Centralized log collection and retention for infrastructure and platform components. 3-month default retention. | Log collection agents + automated log ingestion + automated retention management | Log storage and tooling cost (TBD) | Log analysis, alert rule configuration, compliance log management, custom retention policy | MC team time; PS required for custom application logging | Live (infrastructure logging); PS for application logging |

### Engagement & Governance

| Addon | What It Is | Machine Component | Machine Cost (CAD/mo) | Human Component | Human Add-On Cost | Status |
|---|---|---|---|---|---|---|
| **Reviews & Touchpoints** | Regular cadence reviews to assess environment health, review ticket patterns, and plan ahead. Monthly or quarterly. | Automated reporting inputs: ticket summaries, patch compliance, backup status, system inventory | Included | Cadence meeting facilitation, proactive issue identification, best practice guidance, roadmap planning | Included in MC endpoint fee | Live |
| **Managed DNS** | DNS management with proxy mode and edge DDoS protection. Cloudflare-backed. | Self-service via Aptum Portal + automated DNS propagation and health monitoring | Included | Configuration assistance on request | Included | **Live in portal** |
| **Load Balancing (L7)** | Application-layer load balancing with SSL termination, health checks, and routing policies. L4 is self-service in portal. | L7 load balancer appliance/service running continuously once configured | Appliance/license cost (TBD) | L7 policy configuration, SSL termination setup, health check tuning, routing rule management | MC team time | L4 live; L7 managed tier roadmap |
| **Database Tuning** | Database performance optimization: query analysis, index recommendations, capacity planning. | Automated monitoring of DB availability and response time | Included in infrastructure monitoring | DBA analysis, query optimization, capacity planning, performance reviews | MC or PS engagement | Available as PS |
| **DevOps Monitoring & Maintenance** | CI/CD pipeline health, container monitoring, infrastructure-as-code drift detection. | Automated pipeline health checks and drift detection tooling | TBD | Pipeline design review, container monitoring configuration, IaC remediation | MC team | Roadmap |
| **Managed Productivity (M365)** | Exchange Online, SharePoint, and Teams administration including user provisioning, security configuration, and license management. | Microsoft M365 admin tooling (Microsoft-provided automation) | M365 licensing (customer-supplied) | User provisioning, security policy configuration, license management, governance | MC team time | Live |

---

### Professional Services: Advisory (Assess) and Execute (Implement)

Professional services are organized into two distinct motions with different delivery models, commercial structures, and success metrics.

#### Advisory: Structured Assessments

The advisory motion consists of seven structured assessments that diagnose the customer's environment, quantify risk, and produce a roadmap. Each assessment is a fixed-fee, t-shirt-sized engagement (S/M/L/XL) led by a Solution Architect. The assessment deliverable is the business case for the Execute and Operate motions that follow.

| Assessment | Price Range | What It Produces | Primary Layer Destination |
|---|---|---|---|
| **Infrastructure Risk & Readiness** | $5K–$30K+ | EOL inventory, capacity baseline, remediation roadmap | L1 + L2 (Monitoring + Managed OS) |
| **Hybrid Cloud** | $7.5K–$40K+ | Workload inventory, TCO modeling, placement roadmap | L2 + L3 + L5 (Managed OS + App Platform + Hybrid Connectivity) |
| **Security Posture & Compliance** | $5K–$30K+ | Vulnerability assessment, compliance gap analysis, remediation matrix | L2 + L4 (Managed Firewall + Security & Compliance) |
| **Cloud Repatriation** | $5K–$35K+ | Cloud spend analysis, portability scoring, repatriation business case | L1 + L2 + L5 (Monitoring + Managed OS + Business Continuity/Hybrid) |
| **Operational Maturity** | $5K–$30K+ | OpEx analysis, maturity scoring, managed services transition plan | L2 + L3 + L4 (full ops handoff) |
| **App & Platform Modernization** | $5K–$35K+ | Architecture review, container/K8s readiness, CI/CD maturity | L2 + L3 (Managed OS + App Platform) |
| **Well-Architected Review** | $7.5K–$40K+ | 6-pillar cloud review, cost optimization, governance gaps | L3 + Public Cloud Management |

#### Execute: Project-Based Implementation

The execute motion acts on assessment findings. These are SOW-scoped, milestone-based engagements delivered by cross-functional teams coordinated by HSDM and scoped by HSA.

| Service | What It Is | Typical Assessment Origin | Delivering Team | Typical Revenue |
|---|---|---|---|---|
| **Cloud Migration** | Workload migration (P2V, V2V, on-prem to cloud) | Hybrid Cloud Assessment | HSA + contributing teams via HSDM | $25K–$200K |
| **Repatriation Project** | Selective workload move from hyperscaler to Aptum IaaS | Cloud Repatriation Assessment | HSA + contributing teams via HSDM | $50K–$300K |
| **Hardware Refresh** | EOL server replacement, spec, procure, build, migrate, decommission | Infrastructure Risk Assessment | Compute Platforms + HSA | $5K–$50K |
| **Security Remediation** | Firewall replacement, OS upgrades, hardening, compliance alignment | Security Posture Assessment | Managed Cloud + HSA | $20K–$100K |
| **Platform Build** | Kubernetes implementation, CI/CD pipeline, container platform | Platform Modernization Assessment | Managed Cloud + HSA | $30K–$150K |
| **Architecture Redesign** | Well-architected remediation, cost optimization, governance | Well-Architected Review | Managed Cloud + HSA | $20K–$80K |
| **Managed Services Transition** | Operational handoff from customer IT to Aptum ops teams | Operational Maturity Assessment | Managed Cloud + HSDM | $15K–$50K |
| **DR Design & Implementation** | Failover architecture, runbook development, first DR test | Infrastructure Risk, Hybrid Cloud | Managed Cloud + HSA | $10K–$30K |

---

## The Stacking Model: Revenue Per Customer

The infrastructure commodity is the entry point. Each managed service layer multiplies MRR.

```
Example: Mid-market company, 20 VMs on Shared Cluster (VPC) + Azure hybrid

Infrastructure Commodity:
  Shared Cluster (20 VMs, ~$7K/mo compute + storage)    $7,000
  Azure managed through Aptum Portal (~$8K/mo spend)       included in management fee

Managed Service Layers:
  Layer 1: 24/7 Infra Monitoring & Response             included
  Layer 2: Managed OS (patching + Veeam backup)        +$3,500
  Layer 2: Managed Firewall                            +$  500
  Layer 3: App Monitoring (Datadog, 20 hosts)          +$2,500
  Layer 3: WAF (2 web apps)                            +$1,000
  Layer 4: Alert Logic MDR                             +$2,500
  Layer 5: DRaaS (8-hour RTO, 1-hour RPO)              +$3,000
  Layer 5: ExpressRoute to Azure                       +$  800
                                                       ───────
  Total Monthly Revenue                                ~$20,800

  Infrastructure margin: ~70-80%
  Managed services margin: ~35-50%
  Blended margin: ~50-60%
```

Compare to the same customer buying unmanaged Shared Cluster only: $7,000/mo at ~80% margin.
The managed services layers nearly triple revenue and the customer is deeply embedded.

---

## Assessment-Driven Onboarding Paths

Each assessment produces findings that point at specific managed service layers. This is the mechanism that converts a generic upsell pitch into an evidence-based conversation. The customer does not hear "you should buy managed patching." The customer hears "your assessment found 14 servers running EOL operating systems with 47 unpatched CVEs. Here is what we do about that."

### Path 1: Infrastructure Risk --> L1 + L2

**Assessment finds:** EOL hardware, unsupported OS, deferred patching, single points of failure, capacity constraints.

**Execute step:** Hardware refresh (replace EOL servers with Aptum IaaS or new dedicated), OS upgrades.

**Operate destination:** L1 Infrastructure Monitoring (24/7 monitoring on new hardware) + L2 Managed OS (ongoing patching, backup, managed firewall). Optional L5 DRaaS if assessment identified single-site risk.

**Expected MRC uplift:** $5K–$15K/mo

### Path 2: Cloud Repatriation --> Private Cloud + L2 + L5

**Assessment finds:** Cloud overspend on predictable workloads, portable workloads suitable for repatriation, savings opportunity of 30-60% on repatriated workloads.

**Execute step:** Repatriation project (move selected workloads to Aptum Private Cloud, retain hyperscaler for workloads that benefit from elasticity).

**Operate destination:** Private Cloud infrastructure + L1 Infrastructure Monitoring (24/7 monitoring on Private Cloud hardware) + L2 Managed OS (patching, backup on repatriated workloads) + L5 Hybrid Connectivity (ExpressRoute/Direct Connect to retained hyperscaler workloads). Optional L3 App Platform for monitoring, L4 Security if compliance-driven.

**Expected MRC uplift:** $10K–$50K/mo (highest value path)

### Path 3: Hybrid Cloud --> L2 + L3 + L5

**Assessment finds:** Workload sprawl across environments, inconsistent management, suboptimal placement, TCO improvement opportunity.

**Execute step:** Architecture rationalization (move workloads to optimal placement), migration to Aptum IaaS for suitable workloads.

**Operate destination:** L2 Managed OS across all environments + L3 App Platform (unified monitoring via Datadog, WAF for web workloads) + L5 Hybrid Connectivity (interconnects between Aptum and retained hyperscaler environments).

**Expected MRC uplift:** $8K–$25K/mo

### Path 4: Security Posture --> L2 + L4

**Assessment finds:** EOL firewalls, unpatched CVEs, compliance gaps (SOC 2, HIPAA, PCI-DSS), inadequate security monitoring.

**Execute step:** Security remediation (firewall replacement, OS upgrades, hardening, compliance alignment).

**Operate destination:** L2 Managed Firewall (ongoing policy management, audit) + L4 Security & Compliance (Alert Logic MDR, compliance reporting, vulnerability scanning). Optional L2 Managed OS for patching.

**Expected MRC uplift:** $5K–$17K/mo

### Path 5: Operational Maturity --> L2 + L3 + L4

**Assessment finds:** IT team spending 80%+ on reactive operations, no structured monitoring/patching/incident management, operational model unsustainable at current scale.

**Execute step:** Managed services transition (structured handoff of operational domains from customer IT team to Aptum ops teams, runbook creation, tooling migration).

**Operate destination:** L2 Managed OS (patching, backup, firewall) + L3 App Platform (Datadog APM, WAF if web-facing) + L4 Security (MDR if regulated). This is the broadest managed services adoption path and the stickiest (once a customer hands off operations, they rarely take them back).

**Expected MRC uplift:** $8K–$30K/mo

### Path 6: Platform Modernization --> L2 + L3

**Assessment finds:** Legacy infrastructure under modern applications, immature CI/CD, container gaps, no platform strategy.

**Execute step:** Platform build (Kubernetes implementation, CI/CD pipeline, container platform on Aptum infrastructure).

**Operate destination:** L2 Managed OS (underlying infrastructure management) + L3 App Platform (container monitoring, DevOps maintenance, WAF). Aptum manages the platform so the customer's developers can focus on applications.

**Expected MRC uplift:** $8K–$25K/mo

### Path 7: Well-Architected Review --> L3 + Public Cloud Management

**Assessment finds:** Architecture gaps across 6 pillars (operational excellence, security, reliability, performance, cost, sustainability), cost optimization opportunities, governance gaps.

**Execute step:** Remediation project (architecture improvements, cost optimization implementation, governance framework).

**Operate destination:** L3 App Platform (ongoing monitoring, WAF, performance optimization) + Public Cloud Management (continued optimization, governance enforcement, cost reporting through Aptum Portal).

**Expected MRC uplift:** $6K–$15K/mo

---

## Portal Visibility Roadmap: What the Aptum Portal Should Surface Per Layer

This is the gap. The portal delivers Layer 0 (self-service provisioning) well today. Layers 1-5 are operationally delivered but invisible in the portal. Making them visible is what turns Aptum Portal from a provisioning tool into a retention engine.

| Layer | What the Portal Should Show | Priority | Complexity |
|---|---|---|---|
| **Commodity** | VM status, cost estimator, usage reports, quoting tool | **Live** | Done |
| **L1: Infra Monitoring** | Uptime dashboard, alert history, incident status | High | Requires Zabbix/LM → portal integration |
| **L2: Managed OS** | Patch compliance, backup success/failure, firewall audit | High | Requires Veeam + patching tool → portal integration |
| **L3: App Platform** | Datadog dashboards (embed/link), WAF events, LB health | Medium | Datadog API + Imperva API integration |
| **L4: Security** | MDR threat dashboard, compliance status, scan results | Medium | Alert Logic API integration |
| **L5: BCP/Hybrid** | DR plan status, last test result, interconnect up/down | Medium | Custom dashboard from runbook data |
| **Support** | Ticket status, SLA compliance, contact info | High | JSM → portal integration (link to CUST-* or APTUM project) |

**The priority call:** L1 + L2 portal visibility + Support ticket integration are the highest-impact items. They affect every managed customer and make the "managed" visible. L3-L5 are valuable but serve a smaller subset of customers.

---

## Team Responsibility Summary: Who Delivers What

| Managed Service | Service Desk | Managed Cloud | Compute Platforms | Data Center Ops | Network | HSA / HSDM |
|---|---|---|---|---|---|---|
| Infra Monitoring | **Operates** | | | | | |
| Hardware Replacement | Dispatches | | | **Executes** | | |
| Network Monitoring | Escalation | | | | **Operates** | |
| OS Patching | | **Operates** | | | | |
| Managed Backup | | **Operates** | | | | |
| Managed Firewall | **L2 ops** | Policy escalation | | | | |
| Endpoint Security | | **Operates** | | | | |
| Application Performance Monitoring | | **Operates** | | | | |
| Web Application Firewall | | **Operates** | | | | |
| DDoS | | **Manages** | | | Edge protection | |
| L7 Load Balancing | | **Operates** | | | | |
| Managed Detection and Response (MDR) | | **Manages** (+ partner) | | | | |
| DRaaS | | **Operates** | | | | PS designs |
| Hybrid Interconnects | | **Manages** logical | | | **Operates** physical | |
| Managed Productivity (M365) | | **Operates** | | | | |
| Advisory (Assessments) | Data collection support | SME support | Environment docs | Asset inventory | Network topology | **SA leads delivery** |
| Execute (Projects) | Contributes | Contributes | Contributes | Contributes | Contributes | **HSA scopes, HSDM delivers** |

---

*Sources: `/53-products/aptum-product-strategy.md` v2.1 (April 28, 2026), `/53-products/aptum-icp.md` v2.1 (April 28, 2026), Aptum Identity & Values (Confluence, Marketing space), STG Assessment & Commercial Playbook v1.0, dimServices extract (April 1, 2026), Service Team descriptions (all 9 teams), Reanchor session notes (April 1, 2026).*
