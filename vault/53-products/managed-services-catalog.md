# Aptum Managed Services Catalog
## Value-Added Products Layered on Apt Cloud Commodities
**Version 2.0 | April 1, 2026**

---

## The Reframe

The old tiering model (Tier 0-3) mixed infrastructure products with managed services in a vertical stack. This model separates them into two dimensions:

- **Horizontal: Infrastructure Commodities** — what the customer provisions through Apt Cloud (or what Aptum provisions on their behalf). These are the base products. They are increasingly self-service and increasingly commoditized.
- **Vertical: Managed Service Layers** — what Aptum operates on top of the commodity. These are the margin multipliers. They require human expertise. They are what makes Aptum different from a VPS provider.

Every customer picks an infrastructure commodity and then stacks managed service layers on top. The more layers, the higher the MRR, the lower the churn.

The assessment framework (see Product Strategy) defines how customers enter this catalog. Structured advisory assessments diagnose the customer's environment and produce findings that map directly to specific layers. The assessment report becomes the evidence base that justifies each layer's investment. The table below summarizes the assessment-to-layer mapping; detailed onboarding paths appear at the end of this document.

---

## Infrastructure Commodities (Provisioned via Apt Cloud)

These are the "base products." Customers can consume them self-service (where available) or have Aptum provision them. The infrastructure itself is not the margin story — it's the entry point.

| Commodity | Technology | Provisioning | Portal Status | Infra Ops (Jason) |
|---|---|---|---|---|
| **Colocation** | Customer-owned hardware in Aptum DC | Manual (George's team) | Future: power/bandwidth visibility | Facility only — customer owns everything above the rack |
| **Dedicated Server** | Aptum-owned bare metal, single-tenant | Manual (Martin builds, George racks) | Future: inventory/status | Hardware health monitoring, replacement |
| **BMaaS** | Canonical MAAS via CloudStack Extensions | Self-service (roadmap) | Roadmap | Hardware health, MAAS platform ops |
| **VPC** | CloudStack VMs, multi-tenant shared hosts | **Self-service (live)** | **Live** | CloudStack cluster ops, hypervisor health, network |
| **Private Cloud** | CloudStack VMs, single-tenant dedicated hosts | Semi-automated | Platform capable | Dedicated host management, hypervisor, storage |
| **Proxmox** | Proxmox VE via CloudStack Extensions | Roadmap | Roadmap | Proxmox cluster ops (Jason's team, new skill) |
| **Public Cloud** | Azure (live), AWS/GCP (roadmap) | **Self-service (live — Azure)** | **Live** | N/A — hyperscaler owns infra |
| **Kubernetes** | K8s via CSI integration | Roadmap | Roadmap | Cluster infrastructure ops |

**Who operates the infrastructure commodity:** Jason's Service Desk (L2/L3 infra engineers) + Martin's Compute Platforms (builds, standards, L3 escalation) + George's DC Ops (physical layer) + Ben's Network (connectivity).

---

## Managed Service Layers (The Revenue Multipliers)

These are the products that stack on top of any infrastructure commodity. Each layer is independently sellable, priced as a monthly add-on, and has a defined delivering team and portal visibility target.

### Layer 1: Infrastructure Monitoring & Response
*"We watch the hardware so you don't have to."*

| Service | What It Is | Delivering Team | Applies To | Portal Visibility | Status |
|---|---|---|---|---|---|
| **24/7 Infrastructure Monitoring** | Zabbix/LogicMonitor alerting on hardware health, ping, availability. Alert → ticket → triage → resolve. | Service Desk (Jason) | All physical infra: Dedicated, BMaaS, VPC hosts, Private Cloud | Uptime dashboard, alert history | Not built (portal) |
| **Hardware Replacement SLA** | Failed component replaced within defined window (4hr/8hr/NBD). PSU, disk, CMOS, memory. | DC Ops (George) dispatched by Service Desk | All physical infra | Incident status tracking | Not built (portal) |
| **Network Monitoring** | 99.999% uptime SLA on connectivity. BGP, transit, switching health. | Network (Ben) | All customers with Aptum connectivity | Bandwidth utilization, uptime | Not built (portal) |

**Included with:** Every managed hosting and dedicated server product. This is the baseline — customers paying for Aptum infrastructure get this by default. For colo customers, this is an add-on.

**Margin note:** This layer is largely covered by existing Service Desk labor. The cost is already incurred. The revenue opportunity is making it explicit, priced, and visible in the portal.

---

### Layer 2: Managed OS
*"We are your sysadmin team."*

| Service | What It Is | Delivering Team | Applies To | Portal Visibility | Status |
|---|---|---|---|---|---|
| **OS Patching** | Scheduled patch cycles for Windows Server and Linux (Debian, Ubuntu, RHEL, Alma, Rocky). Patch compliance reporting. | Managed Cloud (Andrei) | Any infra commodity where Aptum manages the OS | Patch compliance dashboard, schedule, history | Not built (portal); delivered today via runbook |
| **Managed Backup — Veeam** | Backup job scheduling, monitoring, and restore operations. Policy-based retention. Backup success/failure reporting. | Managed Cloud (Andrei) | All infra commodities (Veeam supports physical, virtual, and cloud) | Backup job status, success rate, storage consumption, restore requests | Not built (portal); delivered today via tickets |
| **Managed Firewall** | Security policy management on Juniper SRX (physical) or virtual firewall (pfSense, FortiGate VM). Rule changes, audit, compliance. | Service Desk (L2 ops) + Managed Cloud (policy escalation) | Dedicated, Private Cloud, VPC (advanced tier) | Firewall rule audit log, policy status | Not built (portal); Advanced/Managed tiers near-term roadmap |
| **Endpoint Security (AV/EDR)** | Managed antivirus and endpoint detection on customer servers. Alert triage and response. | Managed Cloud (Andrei) | Any infra where Aptum manages OS | Agent status, threat detection log | Not built (portal) |

**ICP for this layer:** Overwhelmed IT teams of 2-5 people drowning in tickets. They need a safety net.

**Revenue uplift:** +$2,000–$5,000/mo depending on estate size.

**The hook:** *"We handle Patching, Backups, and Perimeter Security so your team can sleep."*

---

### Layer 3: Application & Cloud Platform Services
*"We watch the transaction, not just the server."*

| Service | What It Is | Delivering Team | Applies To | Portal Visibility | Status |
|---|---|---|---|---|---|
| **App Performance Monitoring — Datadog** | Full-stack observability. APM, infrastructure metrics, log management, custom dashboards. Proactive alerting and incident response. | Managed Cloud (Andrei) | Any infra commodity; strongest fit with VPC, Private Cloud, Public Cloud | Datadog dashboard embedded/linked in portal | Not built (portal); delivered today for CUST-* customers |
| **App Security — WAF** | Web Application Firewall. HTTP/HTTPS inspection, OWASP rule sets, custom policies. Managed as a service, not a network device. | Managed Cloud (Andrei) | Any customer with web-facing applications | WAF event log, policy status, block rate | Not built (portal) |
| **DDoS Protection** | Volumetric scrubbing service. Always-on at network edge (included) + managed scrubbing appliance (add-on). | Managed Cloud (Andrei) + Network (Ben) for edge | All customers (basic included); enhanced scrubbing is add-on | Attack history, scrubbing status | Not built (portal) |
| **Load Balancing — L7/SSL** | Application-layer load balancing. SSL termination, health checks, routing policies. (L4 is self-service in portal today.) | Managed Cloud (Andrei) | VPC, Private Cloud, Public Cloud | LB health, backend pool status | L4 self-service live; L7 managed tier roadmap |
| **DB Tuning** | Database performance optimization. Query analysis, index recommendations, capacity planning. | Managed Cloud (Andrei) or PS engagement | Any infra with managed databases | N/A — advisory/PS model | Available as PS |
| **DevOps Monitoring & Maintenance** | CI/CD pipeline health, container monitoring, infrastructure-as-code drift detection. | Managed Cloud (Andrei) | Kubernetes, Public Cloud, VPC | Future | Roadmap |

**ICP for this layer:** CTOs, DevOps leads, Product Leads at SaaS/eCommerce companies where "slow = lost revenue."

**Revenue uplift:** +$3,000–$8,000/mo depending on scope.

**The hook:** *"We don't just watch the server; we watch the Transaction. We ensure your Checkout Page loads in <2 seconds."*

---

### Layer 4: Security & Compliance
*"We prove you're protected."*

| Service | What It Is | Delivering Team | Applies To | Portal Visibility | Status |
|---|---|---|---|---|---|
| **Alert Logic MDR** | Managed Detection & Response. 24/7 threat monitoring, SOC-as-a-service, compliance reporting. | Managed Cloud (Andrei) + Alert Logic (partner) | Any infra commodity | Threat dashboard, compliance reports | IN DEVELOPMENT |
| **Compliance Reporting** | SOC 2, PCI-DSS, HIPAA evidence collection and reporting. Leverages Aptum's own SOC 2 Type II. | Managed Cloud (Andrei) + PS for initial setup | Regulated industries on any infra | Compliance status dashboard | Not built; PS-led today |
| **Vulnerability Scanning** | Scheduled scans, remediation tracking, posture scoring. | Managed Cloud (Andrei) | Any infra where Aptum manages OS | Scan results, remediation status | Not built |

**ICP for this layer:** Regulated industries — healthcare, financial services, government. Companies where an audit failure is a business-ending event.

**Revenue uplift:** +$2,000–$5,000/mo for MDR; compliance reporting often bundled with PS engagement.

---

### Layer 5: Business Continuity & Hybrid Connectivity
*"When things go wrong, we've already planned for it."*

| Service | What It Is | Delivering Team | Applies To | Portal Visibility | Status |
|---|---|---|---|---|---|
| **DRaaS — Disaster Recovery as a Service** | Defined RPO/RTO. Failover environment (secondary site or cloud). Runbook-based recovery. Quarterly DR tests. | Managed Cloud (Andrei) + PS for design | Private Cloud, VPC, Public Cloud | DR plan status, last test date/result, RPO/RTO targets | Not built (portal); delivered today for some CUST-* customers |
| **BCP Planning & Testing** | Business Continuity Plan development, tabletop exercises, annual review. | Managed Cloud (Andrei) | All managed customers | Plan status, test schedule | Advisory/PS-led today |
| **Hybrid Cloud Interconnects** | ExpressRoute (Azure), Direct Connect (AWS). Managed logical config, monitoring, failover. Physical circuit by Ben's team. | Managed Cloud (Andrei) + Network (Ben) for physical | Customers with hybrid (private + public cloud) | Interconnect status (up/down), bandwidth utilization | Not built (portal) |
| **M365 Managed Services** | Exchange Online, SharePoint, Teams administration. Licensing, user provisioning, security configuration. | Managed Cloud (Andrei) | Any customer using M365 | N/A — managed via M365 admin center | Delivered today |
| **Managed DNS — Cloudflare** | DNS management, Cloudflare proxy mode, DDoS at edge. | Self-service via Apt Cloud | Any customer | **Live in portal** | Live |

**Revenue uplift:** DRaaS = +$1,500–$5,000/mo; ExpressRoute = +$500–$1,500/mo.

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

The execute motion acts on assessment findings. These are SOW-scoped, milestone-based engagements delivered by cross-functional teams coordinated by HSDM (Lacie Allen-Morley) and scoped by HSA (Pat Wolthausen).

| Service | What It Is | Typical Assessment Origin | Delivering Team | Typical Revenue |
|---|---|---|---|---|
| **Cloud Migration** | Workload migration (P2V, V2V, on-prem to cloud) | Hybrid Cloud Assessment | HSA + contributing teams via HSDM | $25K–$200K |
| **Repatriation Project** | Selective workload move from hyperscaler to Aptum IaaS | Cloud Repatriation Assessment | HSA + contributing teams via HSDM | $50K–$300K |
| **Hardware Refresh** | EOL server replacement, spec, procure, build, migrate, decommission | Infrastructure Risk Assessment | Compute Platforms (Martin) + HSA | $5K–$50K |
| **Security Remediation** | Firewall replacement, OS upgrades, hardening, compliance alignment | Security Posture Assessment | Managed Cloud (Andrei) + HSA | $20K–$100K |
| **Platform Build** | Kubernetes implementation, CI/CD pipeline, container platform | Platform Modernization Assessment | Managed Cloud (Andrei) + HSA | $30K–$150K |
| **Architecture Redesign** | Well-architected remediation, cost optimization, governance | Well-Architected Review | Managed Cloud (Andrei) + HSA | $20K–$80K |
| **Managed Services Transition** | Operational handoff from customer IT to Aptum ops teams | Operational Maturity Assessment | Managed Cloud (Andrei) + HSDM | $15K–$50K |
| **DR Design & Implementation** | Failover architecture, runbook development, first DR test | Infrastructure Risk, Hybrid Cloud | Managed Cloud (Andrei) + HSA | $10K–$30K |

---

## The Stacking Model — Revenue Per Customer

The infrastructure commodity is the entry point. Each managed service layer multiplies MRR.

```
Example: Mid-market company, 20 VMs on VPC + Azure hybrid

Infrastructure Commodity:
  VPC (20 VMs, ~$7K/mo compute + storage)              $7,000
  Azure managed through Apt Cloud (~$8K/mo spend)       included in management fee

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

Compare to the same customer buying unmanaged VPC only: $7,000/mo at ~80% margin.
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

**Operate destination:** L3 App Platform (ongoing monitoring, WAF, performance optimization) + Public Cloud Management (continued optimization, governance enforcement, cost reporting through Apt Cloud).

**Expected MRC uplift:** $6K–$15K/mo

---

## Portal Visibility Roadmap — What Apt Cloud Should Surface Per Layer

This is the gap. The portal delivers Layer 0 (self-service provisioning) well today. Layers 1-5 are operationally delivered but invisible in the portal. Making them visible is what turns Apt Cloud from a provisioning tool into a retention engine.

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

## Team Responsibility Summary — Who Delivers What

| Managed Service | Jason (Service Desk) | Andrei (Managed Cloud) | Martin (Compute) | George (DC Ops) | Ben (Network) | Pat/Lacie (HSA/HSDM) |
|---|---|---|---|---|---|---|
| Infra Monitoring | **Operates** | | | | | |
| Hardware Replacement | Dispatches | | | **Executes** | | |
| Network Monitoring | Escalation | | | | **Operates** | |
| OS Patching | | **Operates** | | | | |
| Managed Backup | | **Operates** | | | | |
| Managed Firewall | **L2 ops** | Policy escalation | | | | |
| Endpoint Security | | **Operates** | | | | |
| App Monitoring (Datadog) | | **Operates** | | | | |
| WAF | | **Operates** | | | | |
| DDoS | | **Manages** | | | Edge protection | |
| L7 Load Balancing | | **Operates** | | | | |
| Alert Logic MDR | | **Manages** (+ partner) | | | | |
| DRaaS | | **Operates** | | | | PS designs |
| Hybrid Interconnects | | **Manages** logical | | | **Operates** physical | |
| M365 | | **Operates** | | | | |
| Advisory (Assessments) | Data collection support | SME support | Environment docs | Asset inventory | Network topology | **SA leads delivery** |
| Execute (Projects) | Contributes | Contributes | Contributes | Contributes | Contributes | **HSA scopes, HSDM delivers** |
