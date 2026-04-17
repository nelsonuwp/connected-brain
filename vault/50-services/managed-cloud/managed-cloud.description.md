# Managed Cloud

**Service Manager:** Andrei Ianouchkevitch
**Function:** Operations
**Lifecycle:** Live
**Note:** Source PDF is archived. Content reflects confirmed current state. Cost allocation correction in progress — see financial model.
**Confluence Link**: [Managed Cloud Service Description](https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5044273167/Managed+Cloud)

> We manage the hyperscaler layer and the application layer. Azure, AWS, GCP -- plus the services that run on top, regardless of whether the underlying infrastructure is public cloud or Aptum-hosted. The OS upward, where the customer has bought managed services.

---

## Accountable For

- Hyperscaler managed layer: Azure, AWS, GCP -- management from the OS upward on customer workloads running in public cloud
- Optional managed OS layer for Aptum-hosted products: patching (Debian, Windows Server, Ubuntu, RHEL, Alma Linux), Veeam backup, managed firewall policy -- applied on top of Service Desk's infrastructure management when the customer purchases this layer
- Application platform services: Datadog APM and monitoring, WAF, DDoS scrubbing management, application-layer load balancing (L7/SSL)
- Security services: Alert Logic MDR, compliance reporting, vulnerability scanning
- Business continuity: DRaaS design and testing, BCP planning
- Hybrid cloud interconnects: logical config and monitoring for ExpressRoute (Azure) and Direct Connect (AWS) -- physical circuit is Network
- M365 managed services
- **Apt Cloud portal application layer:** The Apt Cloud portal (portal.aptum.com) runs on Aptum-owned Dedicated Servers. Service Desk manages the infrastructure layer (the servers themselves). Managed Cloud manages the application layer of the portal -- monitoring, patching, and operational management of the portal application.
- L3 escalation receipt from Service Desk for hyperscaler and application-layer incidents
- Runbook ownership for all managed cloud environments (public cloud and application-layer services)
- BCP/DRaaS planning and testing for cloud customers

**What Managed Cloud does NOT manage at the hypervisor layer:** For Private Cloud customers (VMware/Proxmox), Service Desk owns the hypervisor layer. Managed Cloud's role in Private Cloud is as an optional add-on for the guest OS and application layers above the hypervisor -- not for the platform itself.

---

## Problems We Solve

- Customers lack internal expertise to manage cloud platforms at the OS and application layer
- Public cloud environments drift, degrade, and surprise customers without active management
- Private cloud environments need patching, backup, and monitoring that customers cannot self-manage
- Cloud incidents stall in Service Desk without a resolution path — Managed Cloud is that path
- AptCloud shared clusters need a managed operations layer before customers can consume them

---

## Products and Services Supported

- Managed Cloud Platform (MCP): Azure, AWS, GCP managed layer
- Optional managed OS layer: patching, Veeam backup, managed firewall policy -- applies to any Aptum-hosted product where the customer purchases this layer (Dedicated Server, Shared Cluster, Dedicated Cluster, Private Cloud guest OS)
- Application performance monitoring: Datadog (APM, infrastructure metrics, log management)
- Application security: WAF, DDoS scrubbing management
- Security and compliance: Alert Logic MDR, compliance reporting (SOC 2, PCI-DSS, HIPAA), vulnerability scanning
- Business continuity: DRaaS, BCP planning
- Hybrid interconnects: ExpressRoute (Azure), Direct Connect (AWS) -- logical config and monitoring; physical circuit by Network
- M365 managed services
- Apt Cloud portal application layer management

### Private Cloud -- Who Owns What

The Private Cloud product (VMware/Proxmox on dedicated hosts) has distinct management layers with distinct owners.

| Layer | Owner | Notes |
|---|---|---|
| Physical hardware | Data Center Ops | Rack, power, physical remediation |
| Network connectivity | Network | Physical and logical network layer |
| Hypervisor (ESXi hosts, vCenter, storage, Proxmox cluster) | Service Desk | Day 2 management of the platform layer. Included in Private Cloud. |
| Guest OS on VMs (patching, backup, firewall policy) | Managed Cloud -- optional | Available as an add-on; not included by default |
| Application layer (Datadog, WAF, DDoS, L7 LB) | Managed Cloud -- optional | Available as an add-on; not included by default |

**Practical test:** If it is the VMware host, vCenter, or Proxmox cluster -- that is Service Desk. If it is a guest VM's operating system or anything running inside it -- that is Managed Cloud (if purchased).

### Cloud Networking -- Boundary Clarification

This team owns the **security and application delivery layer** on top of network infrastructure. Network owns the physical and logical network pipes. The practical delineation:

| Service | Owner | Why |
|---|---|---|
| WAF (Web Application Firewall) | Managed Cloud | Configured as a managed service policy, not a network device. Inspects HTTP/HTTPS traffic against customer application. |
| DDoS protection | Managed Cloud | Scrubbing service — cloud or managed appliance. Service configuration, not network infrastructure. |
| Hybrid cloud interconnects (ExpressRoute, Direct Connect) | Managed Cloud | The managed service wrapper and configuration. Physical circuit provisioned by Network; logical config and monitoring owned here. |
| MPLS, internet ports, routing, BGP | Network | Physical and logical network infrastructure -- OSI Layer 1-3. |
| Juniper SRX firewall (physical appliance) | Service Desk (L2 ops) + Network (connectivity escalation) + Managed Cloud (security policy escalation) | L2 ticket response: Service Desk. Physical connectivity issue: Network. Security policy / rule issue: Managed Cloud. |

**Practical test:** If it requires a Juniper CLI or a physical cable, it is Network. If it requires a portal, a policy, or a service configuration, it is Managed Cloud.

---

## What This Team Does NOT Do

- Own the physical or hypervisor build layer — that is Compute Platforms
- Perform L1/L2 ticket response for infra-layer incidents — that is Service Desk
- Provision new environments — that is Compute Platforms
- Own data center facilities or dispatch remote hands — that is Data Center Ops
- Manage network infrastructure, routing, or physical connectivity — that is Network

---

## Financial Model

### Revenue Touch
- MCP direct revenue: ~$625K YTD (F26 Actual)
- Enables ~$7.6M hyperscale revenue by providing the managed layer that justifies the margin
- AptCloud: pre-revenue (Alpha); target pricing and margin to be defined at Beta

### Direct Cost Driver
- ~8 people (Andrei's direct team)
- **Important:** 25 people were previously allocated to this cost center in financial reporting. Approximately 17 of those belong to Service Desk (Jason's org). This misallocation is being corrected.
- Corrected direct labor: ~$249K (8/25 of the reported $777K)
- Tooling: Datadog licenses, cloud management platform costs

### Margin Profile
| | As Reported | Corrected (8/25 labor) |
|---|---|---|
| Revenue | $625K | $625K |
| Direct Labor | $777K | ~$249K |
| Partner Services | $143K | $143K |
| Other Direct Costs | $16K | $16K |
| **Gross Margin** | **-$311K / -49.8%** | **~+$217K / ~+35%** |

Managed Cloud is one of the highest-margin products in the portfolio when correctly stated. The reported loss is a cost allocation artifact, not a product performance problem.

### How We Are Measured
| Metric | Target |
|---|---|
| Unplanned downtime per customer | Zero |
| Customer-created tickets | Zero |
| Total monitoring-generated tickets | Zero |
| Unplanned actions outside runbook | Zero |
| Baseline performance deviation | Zero |
| Price delta month-over-month | Zero |
| Runbook coverage | Met / not met per customer |
| BCP successfully exercised | Met / not met per test |
| Security standards compliance | Met / not met per review |

---

## Key Dependencies

| Dependency | Direction | Notes |
|---|---|---|
| Compute Platforms | Inbound | Receives provisioned environments at handoff |
| Service Desk | Inbound | Receives hyperscaler and platform triage escalations |
| Network (Ben) | Lateral | Physical network layer underneath cloud networking services |
| IT Operations & Engineering | Lateral | Corporate tooling and infrastructure support |
| Commercial (Fred's team) | Inbound | Customer onboarding and commercial context |

---

## Open Questions / Flags

- **AptCloud operational readiness:** Shared-cluster operations require more rigorous change management than dedicated hosting. One misconfiguration affects all tenants on that cluster. The team needs to be at operational readiness before AptCloud exits Alpha. Growth investment should happen before Beta, not after the first incident.
- **Team sizing:** 8 people carrying public cloud managed operations, private cloud operations, AptCloud build, and cloud networking services is thin. As AptCloud matures, build work will cannibalize BAU operational capacity without additional headcount.
- **Tooling ownership:** Datadog is currently used by this team. Who owns the Datadog contract, configuration standards, and integration with the broader monitoring stack is an open org question — see Tooling section in operational gaps.
