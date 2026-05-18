# Aptum Managed Services Catalog

## Value-Added Products Layered on Aptum Portal Commodities

**Version 2.2 | May 18, 2026**

---

## How this catalog is organized

Every customer relationship has three layers.

**Infrastructure Commodities** are the base products: compute, storage, networking, and cloud access. Every commodity includes a Fundamental guarantee that the infrastructure works as sold. This cannot be removed or priced out separately.

**Engagement Tiers** sit on top of the commodity and determine the support relationship. Every customer is on one of three tiers:

- **Dedicated**: infrastructure only, no managed services, break-fix via billable Professional Services.
- **Reactive**: Aptum operates the environment on a reactive basis; customer stays in the decision loop.
- **Proactive**: Aptum owns and operates the environment; customer is not in the routine operational loop.

The tier determines the support floor the customer receives, which addons are available, and how much of the day-to-day Aptum holds.

**Managed Service Addons** are purchasable services that stack on top of any commodity. Each addon is one product with two modes of operation, determined by tier. On Reactive, Aptum runs the tooling and keeps the customer in the loop on results and decisions. On Proactive, Aptum owns the outcome and acts without pulling the customer into routine decisions. The addon is the same product either way. What changes is who holds responsibility for it.

Dedicated customers have no addon access. The addon detail tables in this catalog show what Aptum does at each tier for every service.

The assessment framework (see [Aptum Product Strategy](https://aptum.atlassian.net/wiki/spaces/PRD/pages/5257461765/Aptum+Product+Strategy) v2.2) defines how customers enter this catalog and which tier they belong on.

---

## Infrastructure Commodities

These are the "base products." Customers can consume them self-service (where available) or have Aptum provision them. The infrastructure itself is not the margin story; it is the entry point.

| Core Product | Technology | Provisioning & Portal | Fundamental (Always Included) |
| --- | --- | --- | --- |
| **Colocation** | Physical data center space: rack units, power (kW), cooling, physical security | Manual (Data Center Ops); Portal: future — power and bandwidth visibility | Power on, temperature within range, physical security maintained, rack space available. Network connectivity is a separate purchase. |
| **Connectivity** | MPLS, internet ports, BGP, transit, cross-connects, fiber | Manual (Networking); Portal: future — bandwidth utilization and uptime visibility | BGP and routing healthy, 99.999% uptime SLA maintained. SD receives monitoring alerts, escalates to Network team for resolution. |
| **Bare Metal** | Aptum-owned single-tenant physical servers | Manual today (Compute Platforms + Data Center Ops); Portal: roadmap via BMaaS (self-service provisioning) | Server powered and network-connected, Zabbix monitoring active, failed hardware components (PSU, disk, CMOS) replaced within SLA, OS deployed per standard build, L2 triage included. SD Day 2 mandatory and non-removable. |
| **Private Cloud** | VMware or Proxmox on dedicated hardware, built per-customer | Manual (SA specs, Compute Platforms builds); Portal: not applicable (Phase 1) | All Bare Metal fundamentals plus VMware/Proxmox hypervisor healthy, vCenter/cluster operational, storage connected. Service Desk owns the hypervisor layer. |
| **Shared Cluster (VPC)** | CloudStack/KVM on Aptum-owned shared hosts, multi-tenant | Self-service via Aptum Portal — live | Platform available, VMs in running state, CloudStack/KVM layer healthy, storage functioning, baseline platform triage priced into product floor. |
| **Dedicated Cluster** | CloudStack/KVM on Aptum-owned dedicated hosts, single-tenant | Aptum Portal — live (SA involved for initial sizing) | Dedicated cluster available, VMs in running state, CloudStack/KVM cluster healthy, storage functioning, baseline platform triage priced into product floor. |
| **Public Cloud** | Azure, AWS, GCP via Aptum CSP/partner agreements | Hyperscaler portals (self-service); Aptum Portal: cost and consumption visibility — live | CSP subscription active, billing consolidated through Aptum, Aptum communicates hyperscaler outages and relevant status to customers proactively. |

---

## Engagement Tiers

Every customer selects an engagement tier. The tier determines the support floor they receive, whether catalog addons are available, and how much operational ownership Aptum holds over their environment. Infrastructure commodities and their Fundamental guarantees are always included regardless of tier.

The three tiers are a deliberate ladder. Customers who start at Dedicated can move to Reactive or Proactive as trust and reliance on Aptum grows. This is the Assess to Build to Operate funnel made operational. The tier model is not a segment wall; it is a sales motion.

### Working names and customer-facing options

| Working name | Recommended customer-facing name | Alternate options |
| --- | --- | --- |
| **Dedicated** | Infrastructure | Foundational, Baseline, Self-Managed |
| **Reactive** | Co-Managed | Supported, Assisted, Responsive |
| **Proactive** | Fully Managed | Operated, Managed, Outcome |

*Rationale for recommendations: "Co-Managed" and "Fully Managed" are established market terms. Buyers researching MSPs use them. Co-Managed accurately describes the Reactive posture (customer stays in the decision loop; Aptum supplements). Fully Managed accurately describes the Proactive posture (Aptum owns operations). "Infrastructure" is honest about what Dedicated is: compute with no managed services engagement.*

---

### Tier 1: Dedicated

**Who this is for:** Non-ICP customers and customers with no interest in managed services. They are buying infrastructure for internal teams to operate. Also used as the entry point for early-relationship prospects not yet ready to commit to a managed posture.

**Support floor:** Infrastructure Fundamentals only (see Infrastructure Commodities table above). Customers receive Aptum Portal access and ticket submission capability. No SLA beyond the Fundamental guarantee for the infrastructure product.

**Addon access:** None. The managed services catalog is not available to Dedicated customers.

**Help beyond the floor:** Professional Services on a pay-as-you-go basis at standard rates. Customers submit requests via ticket; Aptum responds during business hours. No managed relationship.

**Infrastructure compatibility:** Available on Colocation, Shared Cluster (VPC), Dedicated Cluster, and Public Cloud. **Not available on Bare Metal or Private Cloud**, where the Service Desk layer is mandatory and non-removable (priced into the product floor at approximately $40 CAD/asset/month).

| Aptum's role | Customer's role |
| --- | --- |
| Keep the infrastructure running. Nothing more. | Everything above the infrastructure layer — OS, patching, security, backups, application management. |

---

### Tier 2: Reactive

**Who this is for:** ICP customers who want Aptum to operate their environment reactively — responding to events, executing tooling on their behalf, maintaining the OS and platform layer — while the customer retains oversight and decision-making. This is Aptum's co-managed posture: the customer stays in the loop on all decisions, but Aptum does the operational work.

This tier fits two customer profiles equally. Customers with an internal IT team (IT director or small ops team) use Reactive as augmentation — Aptum covers the tooling and after-hours load while their team focuses on institutional knowledge and strategic work. Customers without an internal IT team use Reactive as their IT function, staying in the approval loop. Same posture, different customer org.

**Support floor:** 24/7 Service Desk coverage. Standard monitoring with customer dashboard access (LogicMonitor: CPU, memory, performance). Reactive support of the OS, networking, and storage layer. L2 triage included. Customer receives alerts, approves patch windows, reviews job status, and requests changes via ticket. Aptum responds; customer decides.

**Addon access:** All **Reactive tier (Reactive tier)** addons in the catalog are available, purchased per endpoint per month. Aptum runs the tooling; the customer stays in the decision loop. See the Addon Detail section for per-addon Reactive tier behavior.

**Addons not available at Reactive:** BCP Planning, Compliance Reporting, and Reviews & Touchpoints are Proactive tier only by nature. They require the Proactive tier.

**Infrastructure compatibility:** Available on all infrastructure commodities.

| Aptum's role | Customer's role |
| --- | --- |
| Monitor, respond, and execute. Run the tooling. Alert the customer. Act on direction. Do not make decisions without customer approval. | Oversight, approval, and decision-making. Internal IT team (if present) handles strategy and application layer. Customer remains accountable for outcomes. |

---

### Tier 3: Proactive

**Who this is for:** ICP customers who want Aptum to own and operate their environment. The customer does not need to be in the routine operational loop. Aptum anticipates problems, designs policy, manages changes, and delivers outcomes. This is the Managed Cloud Platform (MCP) model applied to any infrastructure commodity.

**Support floor:** All Reactive floor features plus dedicated account engineering (named resource), scheduled environment reviews (monthly or quarterly cadence), anticipatory tuning, capacity planning, and proactive event management. Aptum identifies and resolves issues before the customer is aware of them.

**Addon access:** All catalog addons, operated in **Proactive tier (Proactive tier)** posture. Includes the three Proactive tier-only addons: BCP Planning, Compliance Reporting, and Reviews & Touchpoints. See the Addon Detail section for per-addon Proactive tier behavior.

**Infrastructure compatibility:** Available on all infrastructure commodities.

| Aptum's role | Customer's role |
| --- | --- |
| Own and operate the environment. Design policy, manage change, prevent problems, deliver outcomes. Customer is not in the routine operational loop. | Define business outcomes. Approve major architectural changes. Own applications and data. Attend scheduled reviews. |

---

### Addon behavior by tier

The table below shows what Aptum does for the key addons at each tier. Full addon descriptions, costs, and owners appear in the Addon Detail section.

| Addon | Dedicated | Reactive (Reactive tier) | Proactive (Proactive tier) |
| --- | --- | --- | --- |
| **Infrastructure Monitoring** | Not available | Customer dashboard access; alert history; uptime reports. SD reacts to alerts. | Threshold tuning; anomaly detection; proactive response before customer impact; monthly monitoring health reviews. |
| **Advanced Monitoring / APM** | Not available | Datadog agent deployed; automated dashboards; customer portal access; SD responds to alerts. | MC configures custom dashboards; tunes alert rules; proactively investigates performance anomalies; monthly performance reviews. |
| **OS Patching** | Billable PAYG per ticket | Automox deployed; patches scheduled per agreed policy; compliance reports generated. Customer approves patch windows. | MC reviews patch releases; tests compatibility; defines policy; coordinates maintenance windows; validates post-patch. Customer not in routine loop. |
| **Managed Backup** | Not available | Veeam runs scheduled jobs; failure alerts; success/failure reporting. Customer reviews status and requests restores via ticket. | MC designs backup policy; investigates failures proactively; manages restore operations; tests recoverability before the customer needs to. |
| **Antivirus / EDR** | Not available | Agent deployed; automated quarantine; customer reviews alerts. | MC triages alerts; investigates threats; coordinates response; configures exclusions and policies. |
| **Managed Firewall** | Billable per rule change | Config backup; health monitoring; policy violation alerting. SD handles L2 ticket ops; customer requests rule changes via ticket. | MC owns security policy; handles complex rule changes; compliance auditing. SD handles L2 under MC direction. |
| **MDR** | Not available | Alert Logic automated detection and alerting running continuously. Alerts surfaced to SD and customer. | SOC analysts actively investigate threats; manage escalations; produce compliance evidence; conduct proactive threat hunting. |
| **Vulnerability Scanning** | Not available | Automated scan scheduling; execution; posture scoring; reporting. Customer receives scan reports. | MC reviews results; prioritizes remediation by risk; provides guidance; tracks remediation progress proactively. |
| **FinOps / Cost Optimization** | Not available | Aptum Portal cost insights: automated spend reporting; budget alerts; anomaly detection; utilization tracking. Customer has dashboard access. | MC conducts rightsizing analysis; reserved instance strategy; governance framework design; monthly optimization reviews. |
| **BCP Planning** | Not available | **Not available at Reactive** | MC develops BCP document; supports tabletop exercises; conducts annual review. |
| **Compliance Reporting** | Not available | **Not available at Reactive** | MC curates evidence packages; identifies gaps; prepares customer-facing reports (SOC 2, PCI-DSS, HIPAA). |
| **Reviews & Touchpoints** | Not available | **Not available at Reactive** | MC supports monthly/quarterly reviews; analyses ticket patterns; identifies proactive improvements; plans upcoming activities. |

---

### Tier compatibility with the Assess to Build to Operate funnel

The tier model is the operational realization of the Operate motion. Assessment findings should map to a tier recommendation, not just to addon recommendations. A customer identified as overwhelmed, non-ICP, or infrastructure-only belongs at Dedicated. A customer with a small internal IT team and patching/monitoring gaps belongs at Reactive. A customer whose IT team is at capacity and who needs Aptum to own the outcome belongs at Proactive.

| Assessment | Likely tier outcome |
| --- | --- |
| Infrastructure Risk & Readiness | Reactive (monitoring + OS patching as starting addons) |
| Hybrid Cloud | Reactive to Proactive depending on internal IT maturity |
| Security Posture & Compliance | Proactive (compliance reporting is Proactive tier-only) |
| Cloud Repatriation | Proactive (full stack migration into MCP model) |
| Operational Maturity | Proactive (the customer's IT team is the pain signal) |
| App & Platform Modernization | Proactive (MC owns the platform) |
| Well-Architected Review | Reactive to Proactive depending on FinOps and compliance needs |

---

## Managed Service Addons

These are the purchasable addons that stack on top of any infrastructure commodity. Each addon is independently sellable, priced per asset or endpoint per month, and has a defined owner from the Aptum service network. How Aptum operates each addon depends on the customer's tier: at Reactive, Aptum runs the tooling and the customer stays in the decision loop; at Proactive, Aptum owns the outcome. For delivery mechanics and tooling details, see the relevant service guides.

---

## Compatibility Matrix

Which addons are available on which infrastructure products. Bare Metal, Private Cloud, VPC, and Dedicated Cluster behave identically for every addon and are shown as one column.

**Yes** = available at Reactive and Proactive tiers. **Proactive only** = requires Proactive tier. **Partial** = available on this product with restrictions noted. **—** = not applicable.

| Addon | Colo | Connectivity | Core Infrastructure | Public Cloud |
| --- | --- | --- | --- | --- |
| Infrastructure Monitoring | — | Yes | Yes | Yes |
| Advanced Monitoring / APM | — | — | Yes | Yes |
| OS Patching | — | — | Yes | Yes |
| Application Platform Patching | — | — | Yes | Yes |
| Managed Backup | Proactive only | — | Yes | Yes |
| DRaaS | — | — | Yes | Yes |
| BCP Planning | — | — | Proactive only | Proactive only |
| Managed Firewall | — | Yes | Yes | Yes |
| Antivirus / EDR | — | — | Yes | Yes |
| WAF | — | — | Yes | Yes |
| DDoS Protection | — | Yes | Yes | Yes |
| Load Balancing (L7) | — | — | Yes | Yes |
| MDR | — | — | Yes | Yes |
| Vulnerability Scanning | — | — | Yes | Yes |
| Compliance Reporting | — | — | Proactive only | Proactive only |
| Hybrid Interconnects | — | Yes | Yes | Yes |
| FinOps / Cost Optimization | — | — | Partial (IaaS only, not Bare Metal/Private Cloud) | Yes |
| Operational Logging | — | — | Yes | Yes |
| Reviews & Touchpoints | Proactive only | Proactive only | Proactive only | Proactive only |
| Managed DNS | — | — | Yes | Yes |
| Managed Productivity (M365) | — | — | Yes | Yes |
| Database Tuning | — | — | Yes | Yes |
| DevOps Monitoring & Maintenance | — | — | Yes | Yes |

---

## Bare Metal: Cost Structure and Contract Pricing

The Bare Metal product price reflects six components. **Only the margin component is discountable.** The cost base is not negotiable below cost.

| Component | Description |
| --- | --- |
| Physical server | CapEx amortized over the contract term. Residual value at term end: 40% (12mo), 20% (24mo), 0% (36mo). |
| Power | Per-kW cost varies by data center location (illustrative: Herndon $110/kW, Atlanta $337/kW, Miami $48/kW, Los Angeles $457/kW, Toronto/Montreal $253/kW, Portsmouth $46/kW). |
| Data Center Ops | Data Center Ops labor allocated per server (facilities, rack, physical ops). |
| Network | Network team cost allocated per server (~$59/server). |
| **Service Desk (mandatory managed layer)** | **Service Desk labor. Included in every Bare Metal server. Not optional, not removable.** (~$40 CAD/asset/month fully loaded across 3,982 managed assets). |
| Licensing | OS and software licensing where applicable. |

**Contract term pricing, illustrative example (Pro Series 6.0, Herndon DC):**

| Term | Residual Value | List MRC | Effective MRC |
| --- | --- | --- | --- |
| 12 months | 40% | $1,521.39 | $1,521.39 |
| 24 months | 20% | $1,521.39 | $1,182.99 |
| 36 months | 0% | $1,521.39 | $1,013.79 |
| Month-to-month | n/a | Full list | Full list |

*Pricing varies by server spec and data center location. The above is illustrative for one server configuration at one location. The margin component, the difference between cost base and list MRC, is the only component that can be discounted in commercial conversations.*

---

## Addon Detail

Each addon below shows what it is, what it is not (where there is room for confusion), how Reactive tier and Proactive tier tiers differ, which service network team owns it, and real costs for both tiers. Costs in CAD unless noted. USD conversions approximate at current rates.

### Monitoring & Observability

| Addon | What It Is / What It Isn't | Reactive tier | Proactive tier | Addon Owner | Reactive cost (CAD/mo) | Proactive cost (CAD/mo) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Infrastructure Monitoring (visibility)** | Customer-facing access to monitoring dashboards, alert history, and uptime reporting. **Not:** the baseline monitoring Aptum runs internally to keep the commodity working — that is Fundamental and always included. This addon gives the customer visibility into that data. | LogicMonitor dashboard access, alert history, uptime and bandwidth reports. Customer can view and react to their own monitoring data. | Threshold tuning, proactive pattern analysis, Aptum responds to anomalies before customer impact, monitoring health reviews. | Aptum infra: **Compute Platforms**; IaaS platform: **Compute Platforms**; Network devices: **Networking**; Cloud/virtual: **Managed Cloud** | Zabbix OSS: included in SD floor. LogicMonitor customer portal: ~$11–20/device (market rate; Aptum contracted rate TBD) | Included in MC endpoint fee ($160 USD/endpoint bundled) | Live (Zabbix SD-side); Customer portal TBD |
| **Advanced Monitoring / APM** | Full-stack observability: application performance, container health, infrastructure metrics, custom dashboards. **Not:** the same as infrastructure monitoring. APM goes above the OS into the application — infrastructure can show "OK" while app performance degrades. | Datadog agent deployed, automated dashboards, anomaly detection, customer has access to their Datadog environment. | MC configures custom dashboards, tunes alert rules, proactively responds to performance anomalies, delivers monthly performance reviews. | **Managed Cloud** | Datadog Infrastructure: ~$35/host ($25 USD). Datadog APM: ~$45/host ($31 USD). | Datadog $25 USD included in MC endpoint. MC labor within $135 USD/endpoint/month. | Live (MC customers) |

### OS & Platform Management

| Addon | What It Is / What It Isn't | Reactive tier | Proactive tier | Addon Owner | Reactive cost (CAD/mo) | Proactive cost (CAD/mo) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **OS Patching** | Scheduled deployment of OS and security patches. Supported: Windows Server, Linux (Debian, Ubuntu, RHEL, Alma, Rocky). Compliance reporting. **Not:** application patching, database updates, or platform component updates — those are separate addons. | Automox agent deployed, patches scheduled per agreed policy, compliance reports generated. Customer receives notifications and approves patch windows. | MC reviews patch releases, tests compatibility, defines policy, coordinates maintenance windows, validates post-patch environment. Customer not in routine decision loop. | Cloud/Virtual OS: **Managed Cloud**; Aptum Infra OS: **Compute Platforms** | ~$7/endpoint (Automox ~$5 USD) | Automox included + MC labor within $135 USD/endpoint/month | Live |
| **Application Platform Patching** | Updates to application platform components: middleware, runtime environments (Node.js, Java,.NET, Python), platform services. **Not:** OS patching (separate addon). Not application code — that is always the customer's responsibility. | Platform tooling where automated patching is supported, compliance reports generated. | MC tests platform updates, coordinates staged rollout, validates application behaviour post-patch, handles major version changes with customer sign-off. | **Managed Cloud** | TBD (platform-dependent tooling) | Within MCP tier pricing (TBD) | Live (MCP customers) |

### Data Protection & Recovery

| Addon | What It Is / What It Isn't | Reactive tier | Proactive tier | Addon Owner | Reactive cost (CAD/mo) | Proactive cost (CAD/mo) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Managed Backup** | Automated backup execution, monitoring, failure alerting, and restore capability with policy-based retention. **Not:** a DR solution. Backup protects data but does not guarantee a recovery time objective — DRaaS is the separate product for that. | Veeam automated job scheduling and execution, failure alerting, success/failure reporting. Customer can view job status and request restores via ticket. | MC designs backup policy, investigates failures proactively, manages restore operations, handles retention, tests recoverability before the customer needs to. | Policy & Management: **Managed Cloud**; Veeam Infrastructure & Runbooks: **Compute Platforms** | ~$14–20/workload (Veeam; Aptum block commitment — per-workload allocation TBD) | Veeam included + MC labor within $135 USD/endpoint/month | Live |
| **DRaaS** | Defined RPO/RTO with maintained failover environment, tested recovery runbooks, quarterly DR tests. **Not:** just backup. DRaaS requires active failover infrastructure and regular testing. Backup alone does not guarantee recovery within an RTO. | Backup replication to secondary site automated, failover environment maintained and monitored, status reporting accessible. | MC designs DR plan, conducts quarterly DR tests, manages failover coordination, maintains and updates runbooks proactively. | Plan & Management: **Managed Cloud**; Secondary Infrastructure: **Compute Platforms** | Secondary site compute + storage, scoped per engagement (TBD) | MC team + PS for initial design (TBD per engagement) | Live (select customers) |
| **BCP Planning** | Business Continuity Plan development, tabletop exercises, annual review. **Not:** DRaaS. BCP is the strategic plan; DRaaS is the technical execution. Effective together, but sold separately. | Automated plan status and test schedule reporting. | MC develops BCP document, supports tabletop exercises, conducts annual review. | **Managed Cloud** | N/A | Advisory/PS engagement (TBD) | Advisory/PS-led today |

### Security Services

| Addon | What It Is / What It Isn't | Reactive tier | Proactive tier | Addon Owner | Reactive cost (CAD/mo) | Proactive cost (CAD/mo) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Managed Firewall** | Security policy management, rule changes, and compliance auditing for Juniper SRX (physical) and virtual firewalls. **Not:** network infrastructure management — the physical device and connectivity is **Networking**'s responsibility. This addon is the security policy layer on top of the device. | Automated config backup, health monitoring, policy violation alerting, compliance reporting. | Managed Cloud manages security policy, complex rule changes, compliance auditing. Service Desk handles day-to-day L2 ticket operations. | Security Policy: **Managed Cloud**; Physical Device: **Networking** | Included in monitoring infrastructure | MC policy management (TBD/device) | Live |
| **Antivirus / EDR** | Managed endpoint protection including AV and endpoint detection and response on customer servers. **Not:** MDR. AV/EDR is the automated endpoint agent layer. MDR is a full SOC service with human analysts actively hunting threats. | AV/EDR agent deployed, automated definition updates, automated threat detection and quarantine, agent status reporting. | MC triages alerts, investigates threats, coordinates response, configures exclusions and policies. | **Managed Cloud** | Options: MS Defender for Business ~$4/endpoint ($3 USD); CrowdStrike Falcon Go ~$7–10/endpoint ($5–7 USD); SentinelOne ~$6–9/endpoint ($4–6 USD) | Agent cost included + MC labor (TBD/endpoint) | Live |
| **WAF** | HTTP/HTTPS traffic inspection with OWASP rule enforcement and custom security policies, managed as a service. **Not:** network-layer DDoS (separate addon). **Not:** a network firewall. WAF inspects application-layer (L7) traffic only. | WAF engine running, automated OWASP rule updates, automated blocking of known threats, event log accessible. | MC tunes policies, creates custom rules, manages false positives, conducts PCI/compliance reviews, proactively responds to attack patterns. | **Managed Cloud** | Imperva (Incapsula): ~$550/app ($400 USD) entry enterprise. Cloudflare WAF: ~$35–280/zone ($25–200 USD, plan-dependent). | WAF tooling included + MC labor (see WAF service guide) | Evolving (see WAF service guide) |
| **DDoS Protection** | Volumetric attack scrubbing at the network edge (always-on) with optional enhanced managed scrubbing. **Not:** WAF. DDoS is network-layer (L3/L4) volumetric protection. WAF inspects application-layer traffic. Not the same as firewall policy management. | BGP-level edge protection always-on, automated attack detection, scrubbing activation, attack event reporting. | MC coordinates attack response, conducts post-attack review, configures enhanced scrubbing policies for persistent threats. | Physical Edge: **Networking**; Scrubbing Management: **Managed Cloud** | Basic edge: included in network infrastructure. Enhanced scrubbing: TBD per engagement. | MC + Networking team time (TBD/engagement) | Live |
| **MDR** | 24/7 threat monitoring, SOC-as-a-service, and compliance reporting via managed SOC partner. **Not:** AV/EDR. MDR is a full SOC function with analysts actively investigating and hunting threats. AV/EDR feeds into MDR but does not replace it. | Alert Logic (or equivalent) automated threat detection, correlation, alerting, and reporting platform running continuously. | SOC analysts actively investigate threats, manage escalations, produce compliance evidence, conduct proactive threat hunting. | **Managed Cloud** + SOC partner | Alert Logic MDR Essentials: ~$20–35/asset ($15–25 USD market rate; Aptum contract TBD) | Included in Alert Logic service. MC coordination: TBD. | IN DEVELOPMENT |
| **Vulnerability Scanning** | Scheduled automated vulnerability scans with remediation tracking and posture scoring. **Not:** penetration testing. Automated scanning discovers known vulnerabilities. Pen testing is a PS engagement where skilled testers actively attempt exploitation. | Automated scan scheduling, execution, posture scoring, reporting. Customer receives scan reports. | MC reviews results, prioritizes remediation by risk, provides guidance, tracks remediation progress proactively. | **Managed Cloud** | Options: Qualys VMDR ~$7–14/asset ($5–10 USD); Tenable.io ~$10–18/asset ($7–13 USD); Rapid7 InsightVM ~$8–15/asset ($6–11 USD) | Tooling included + MC labor (TBD/asset) | Not built |
| **Compliance Reporting** | SOC 2, PCI-DSS, HIPAA evidence collection and ongoing reporting. uses Aptum's SOC 2 Type II. **Not:** a security audit. Compliance reporting is ongoing evidence documentation, not an independent assessment of controls. | Automated evidence collection tooling where available, automated compliance status dashboard. | MC curates evidence packages, identifies gaps, prepares customer-facing compliance reports. | **Managed Cloud** | TBD (framework-dependent tooling) | PS for initial setup. MC ongoing: TBD. | Not built; PS-led today |

### Cloud & Hybrid Connectivity

| Addon | What It Is / What It Isn't | Reactive tier | Proactive tier | Addon Owner | Reactive cost (CAD/mo) | Proactive cost (CAD/mo) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Hybrid Interconnects** | Dedicated private connectivity between Aptum infrastructure and hyperscalers (ExpressRoute/Azure, Direct Connect/AWS, Partner Interconnect/GCP). **Not:** standard internet connectivity. Hybrid interconnects are dedicated private circuits bypassing the public internet for security, performance, and predictable latency. | Physical circuit provisioned and monitored automatically, circuit health and uptime reporting. | MC manages logical configuration, ongoing circuit monitoring, failover setup and testing, change management. | Physical Circuit: **Networking**; Logical Config & Management: **Managed Cloud** | Azure ExpressRoute 50Mbps: ~$75/mo ($55 USD); 200Mbps: ~$200/mo ($145 USD). AWS Direct Connect hosted connection: ~$30–120/mo port fee. Data transfer charges additional. | MC logical config and management (TBD/engagement) | Live |
| **FinOps / Cost Optimization** | Cloud spend visibility, anomaly detection, budget governance, and cost optimization for public cloud and Aptum IaaS. **Not:** billing support — that is Fundamental for Public Cloud. FinOps is active optimization, not just receiving invoices. | Aptum Portal cost insights: automated spend reporting, budget alerts, anomaly detection, utilization tracking. Customer has dashboard access. | MC conducts rightsizing analysis, reserved instance strategy, governance framework design, monthly optimization reviews. | **Managed Cloud** + **Aptum Portal** | Included in Foundation / Aptum Portal | MC time (TBD — flat monthly fee or % of managed cloud spend) | Live (MC/Foundation customers) |

### Logging

| Addon | What It Is / What It Isn't | Reactive tier | Proactive tier | Addon Owner | Reactive cost (CAD/mo) | Proactive cost (CAD/mo) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Operational Logging** | Centralized log collection, retention, and access for infrastructure and platform operational logs. 3-month default retention. **Not:** application logging. Custom application log pipelines require a PS engagement. This covers infrastructure and platform logs only. | Log collection agents deployed, automated ingestion, retention managed, customer has log access. | MC configures alert rules on log patterns, manages compliance retention, conducts log analysis for incident investigation. | Log Management: **Managed Cloud**; Infrastructure Log Standards: **Compute Platforms** | Datadog Logs: ~$0.15/GB ingested ($0.10 USD) + ~$3.75/million log events ($2.50 USD). Elastic Cloud: ~$0.14/GB/month storage. | Tooling included + MC labor (TBD). PS required for custom application logging. | Live (infrastructure); PS for application logging |

### Engagement & Governance

| Addon | What It Is / What It Isn't | Reactive tier | Proactive tier | Addon Owner | Reactive cost (CAD/mo) | Proactive cost (CAD/mo) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Reviews & Touchpoints** | Scheduled cadence reviews (monthly or quarterly) to assess environment health, review ticket patterns, and plan proactively. **Not:** ad-hoc support tickets. Reviews are structured sessions scheduled in advance. | Automated reporting inputs generated: ticket summaries, patch compliance, backup status, system inventory. | MC supports the review, analyses patterns, identifies proactive improvements, advises on what works, plans upcoming activities. | **Managed Cloud** | Included (automated reporting) | Included in MC endpoint fee ($160 USD/endpoint/month bundled) | Live |
| **Managed DNS** | DNS management with proxy mode and edge DDoS protection via Aptum Portal. **Not:** full network management. DNS records only — does not cover routing, BGP, or network architecture. | Cloudflare-backed self-service DNS management via Aptum Portal, automated propagation and monitoring. | MC assists with complex DNS configuration and troubleshooting on request. | Reactive: **Aptum Portal**; Proactive tier: **Managed Cloud** | Included (Cloudflare ~$35/zone underlying, absorbed in platform cost) | Included for standard requests | **Live in portal** |
| **Load Balancing (L7)** | Application-layer load balancing with SSL termination, health checks, and custom routing policies. (L4 TCP/UDP is self-service in portal.) **Not:** network-layer routing. L7 requires application-aware configuration and is not a set-and-forget device. | L7 load balancer running continuously once configured, automated health checks enforced. | MC configures L7 policies, SSL termination, health check rules, and routing logic. Makes changes on request. | **Managed Cloud** | Appliance/license TBD (scale-dependent) | MC configuration time (TBD) | L4 self-service live; L7 managed tier roadmap |
| **Database Tuning** | Database performance optimization: query analysis, index recommendations, capacity planning. **Not:** database administration. Aptum does not manage schema changes, application code, or data. Backup is a separate addon. | Automated monitoring of DB availability and query response time, automated performance alerting. | DBA analysis, query optimization recommendations, capacity planning, periodic performance review sessions. | **Managed Cloud** | Included in infrastructure monitoring | PS engagement or MC time (TBD) | Available as PS |
| **DevOps Monitoring & Maintenance** | CI/CD pipeline health monitoring, container monitoring, and IaC drift detection. **Not:** application development support. Aptum monitors and maintains DevOps infrastructure, not the code or pipelines the customer builds. | Automated pipeline health checks, container monitoring, IaC drift detection alerts. | MC configures monitoring, proactively responds to pipeline failures, manages IaC drift remediation. | **Managed Cloud** | Datadog CI Visibility or equivalent: TBD | MC time (TBD) | Roadmap |
| **Managed Productivity (M365)** | Exchange Online, SharePoint, and Teams administration: user provisioning, security configuration, license management. **Not:** Azure infrastructure management (separate service). This covers the M365 SaaS layer only. | M365 admin centre automated tooling (Microsoft-provided). | MC manages user provisioning, security policies, license optimization, governance. | **Managed Cloud** | M365 licensing is customer-supplied. Management tooling included in M365 license. | MC time (TBD — per seat or flat monthly fee) | Live |

---

### Professional Services: Advisory (Assess) and Execute (Implement)

Professional services are organized into two distinct motions with different delivery models, commercial structures, and success metrics.

#### Advisory: Structured Assessments

The advisory motion consists of seven structured assessments that diagnose the customer's environment, quantify risk, and produce a roadmap. Each assessment is a fixed-fee, t-shirt-sized engagement (S/M/L/XL) led by a Solution Architect. The assessment deliverable is the business case for the Execute and Operate motions that follow.

| Assessment | What It Produces | Tier Destination |
| --- | --- | --- |
| **Infrastructure Risk & Readiness** | EOL inventory, capacity baseline, remediation roadmap | Reactive (monitoring + OS patching) |
| **Hybrid Cloud** | Workload inventory, TCO modeling, placement roadmap | Reactive to Proactive depending on IT maturity |
| **Security Posture & Compliance** | Vulnerability assessment, compliance gap analysis, remediation matrix | Proactive (compliance reporting is Proactive tier-only) |
| **Cloud Repatriation** | Cloud spend analysis, portability scoring, repatriation business case | Proactive (full migration to MCP model) |
| **Operational Maturity** | OpEx analysis, maturity scoring, managed services transition plan | Proactive (customer IT team is the pain signal) |
| **App & Platform Modernization** | Architecture review, container/K8s readiness, CI/CD maturity | Proactive (MC owns the platform) |
| **Well-Architected Review** | 6-pillar cloud review, cost optimization, governance gaps | Reactive to Proactive depending on FinOps and compliance needs |

#### Execute: Project-Based Implementation

The execute motion acts on assessment findings. These are SOW-scoped, milestone-based engagements delivered by cross-functional teams coordinated by HSDM and scoped by HSA.

| Service | What It Is | Typical Assessment Origin | Delivering Team |
| --- | --- | --- | --- |
| **Cloud Migration** | Workload migration (P2V, V2V, on-prem to cloud) | Hybrid Cloud Assessment | HSA + contributing teams via HSDM |
| **Repatriation Project** | Selective workload move from hyperscaler to Aptum IaaS | Cloud Repatriation Assessment | HSA + contributing teams via HSDM |
| **Hardware Refresh** | EOL server replacement, spec, procure, build, migrate, decommission | Infrastructure Risk Assessment | Compute Platforms + HSA |
| **Security Remediation** | Firewall replacement, OS upgrades, hardening, compliance alignment | Security Posture Assessment | Managed Cloud + HSA |
| **Platform Build** | Kubernetes implementation, CI/CD pipeline, container platform | Platform Modernization Assessment | Managed Cloud + HSA |
| **Architecture Redesign** | Well-architected remediation, cost optimization, governance | Well-Architected Review | Managed Cloud + HSA |
| **Managed Services Transition** | Operational handoff from customer IT to Aptum ops teams | Operational Maturity Assessment | Managed Cloud + HSDM |
| **DR Design & Implementation** | Failover architecture, runbook development, first DR test | Infrastructure Risk, Hybrid Cloud | Managed Cloud + HSA |

---

## Team Responsibility Summary: Who Delivers What

| Managed Service | Service Desk | Managed Cloud | Compute Platforms | Data Center Ops | Network | HSA / HSDM |
| --- | --- | --- | --- | --- | --- | --- |
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

*Sources: [Aptum Product Strategy](https://aptum.atlassian.net/wiki/spaces/PRD/pages/5257461765/Aptum+Product+Strategy) v2.2 (May 18, 2026), [Aptum ICP](https://aptum.atlassian.net/wiki/spaces/PRD/pages/5257363460/Aptum+ICP) v2.2 (May 18, 2026), Aptum Identity & Values (Confluence, Marketing space), STG Assessment & Commercial Playbook v1.0, dimServices extract (April 1, 2026), Service Team descriptions (all 9 teams), Reanchor session notes (April 1, 2026).*