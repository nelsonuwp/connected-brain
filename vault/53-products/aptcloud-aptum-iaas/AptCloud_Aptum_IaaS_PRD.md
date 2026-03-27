# Apt Cloud & Aptum IaaS — Product Requirements Document (v8)

*Last Updated: March 2026 — Incorporates review feedback from Will Stevens and Stefan*

---

## 1. Executive Summary

Aptum operates two related but **distinct** products that are frequently conflated:

**Apt Cloud** is a cloud operations platform and customer control plane — NOT infrastructure. It delivers self-service provisioning, unified governance, cost/usage visibility, lifecycle automation, and a consistent operating model across private, virtual private, and hyperscale environments. It is powered by CloudOps Software (formerly CloudMC) and accessed at **portal.aptum.com**.

**Aptum IaaS** is infrastructure — compute, storage, and networking services delivered as Virtual Private Cloud (VPC) or Private Cloud. It runs on **Apache CloudStack 4.22** on **Aptum-owned Dell servers** in Aptum data centres. Aptum IaaS is delivered through Apt Cloud; Apt Cloud is the enabling platform that makes the self-service, customer management, permissions, products, and pricing possible. The infrastructure catalog is expanding via CloudStack's Extensions Framework (4.21+) to include self-service bare metal provisioning (via Canonical MAAS), Proxmox VE orchestration, and Kubernetes (via CloudStack CKS) — see Section 4.9 for roadmap details.

Together, they replace Aptum's legacy "Aptum Cloud" managed virtualization platform (VMware/Dell, 38 customers, ~$27K MRC). The first Aptum IaaS customers — **7 new logos** totaling **~$39K MRR** (SCADAcore, Alberta New Home Warranty, and five ES Williams sub-customers) — have signed transition agreements (Feb–Mar 2026) via the Ignite program. Note: Apt Cloud (portal.aptum.com) already has existing customers via MTC (ThinkOn) and Azure services.

> **Naming note:** "Aptum IaaS" is a new product. Aptum has historically used the term "IaaS" in other contexts, but the historical usage is not an accurate representation of this product and should not be used in customer-facing materials to describe the legacy service.

---

## 2. Product Boundary

| Capability | Apt Cloud | Aptum IaaS |
|---|---|---|
| Compute / Storage / Networking | Enabled Through | **Yes** |
| Portal / UX / Customer Control Plane | **Yes** | Delivered Via Apt Cloud |
| Self-Service Provisioning | **Yes** | Delivered Via Apt Cloud |
| Lifecycle Automation (Self-Service) | **Yes** | Delivered Via Apt Cloud |
| Lifecycle Automation (Operator) | Integrates | Manual operations by Aptum teams |
| Governance / RBAC / Cost Visibility | **Yes** | Delivered Via Apt Cloud |
| Managed Operations | Integrates with | Delivers |

**The one-line distinction:**
- Apt Cloud = the **how** (how you manage, provision, and govern)
- Aptum IaaS = the **what** (what runs your workloads)

Aptum IaaS is delivered through Apt Cloud. All customer management, permissions, products, pricing, and self-service capabilities require Apt Cloud.

---

## 3. Product Definitions

### 3.1 Apt Cloud (The Platform)

> *"Apt" conveys capability, precision, and readiness — a cloud that is tailored to needs, not one-size-fits-all. Apt Cloud ties directly to Aptum's identity as a hybrid cloud managed services provider.*

Apt Cloud is Aptum's next-generation cloud operations platform, accessed at **portal.aptum.com**. It is a white-labeled instance of **CloudOps Software** that acts as the single control plane for Aptum-delivered cloud services.

**What it delivers:**
- Self-service provisioning (VMs, networks, storage, DNS, bare metal — roadmap)
- Role-based access control (RBAC) with granular permissions
- Cost and usage visibility with real-time cost estimator
- Lifecycle management (create, scale, snapshot, decommission)
- Activity logging (visible activity logs across all services; note: not traditional monitoring/push alerts at this layer today)
- Unified governance across private and hyperscale clouds
- Integration with Aptum managed services workflows
- Multi-tenant organizations with white-label branding (per-reseller)
- Full REST API (API-first design)
- **Monetization engine:** Product catalogs, **pricing**, **commitments**, **utility pricing**, **revenue reporting**, *invoicing*, **discounts**, **credits**, CC integration, tax integration (bold = already set up; italic = available, could be using)
- Link to support / ticketing system (planned)

**What it is NOT:**
- Apt Cloud does NOT provide physical infrastructure
- Apt Cloud does NOT replace hyperscale provider consoles (Azure Portal, AWS Console)
- Apt Cloud does NOT bypass managed services engagement

**Services available within Apt Cloud (portal.aptum.com) today:**
- **Aptum IaaS** — VMs on CloudStack (new)
- **MTC** — VMs on ThinkOn / VMware Cloud Director (legacy MTC customers)
- **Microsoft Azure** — Instances, disks, networks, **Azure Kubernetes Service (AKS)**
- **Cloudflare DNS** — Domains and DNS records (replaces SuperDNS; built and plan developed, rollout pending customer communication)
- **Available to adopt (functionality built, not yet configured):** AWS, GCP, Kubernetes (standalone)

### 3.2 Aptum IaaS (The Infrastructure)

Aptum IaaS consists of compute, storage, and networking services running on Aptum-owned hardware in Aptum data centres, orchestrated by Apache CloudStack 4.22. It is delivered in two models today, with additional models on the roadmap:

**Virtual Private Cloud (VPC):**
- Multi-tenant shared compute infrastructure
- Logical isolation with private networking (VLANs; VXLAN support TBD — needs validation with KVM implementation)
- Dedicated resource quotas
- Predictable performance within a pooled system

**Private Cloud:**
- Single-tenant dedicated compute nodes
- Enhanced security, compliance, and customization
- Custom networking and storage configurations
- Same operational model and automation layer as VPC
- Combines technical infrastructure with managed services (people + technology)
- Note: Bare Metal as a Service (BMaaS) integration is not yet implemented. The platform has a 5c/Hypertec BMaaS integration (Canonical MaaS at the CloudStack layer, built by CloudOps Inc) which could be leveraged. Currently, "Private Cloud" means dedicated physical hosts delivered through the virtual orchestration layer — not direct bare metal provisioning.

### 3.3 Tenancy Model

**Platform tenancy (Apt Cloud):** Always multi-tenant. One instance of CloudOps Software serves all customers, resellers, and their end users. Isolation is logical — through organizations, sub-organizations, environments, and RBAC.

**Infrastructure tenancy:** Varies by service type.

| | Physical Hardware | Hypervisor Layer | Network Isolation | Data Commingling |
|---|---|---|---|---|
| **VPC** | Shared hosts — multiple customers' VMs on same physical server | KVM — shared | VLANs (VXLAN support TBD) | Yes — logically isolated but physically colocated |
| **Private Cloud (Virtual)** | Dedicated hosts — one customer per physical server | KVM — dedicated | VLANs / dedicated | No — customer's VMs only on their hosts |
| **Bare Metal (MAAS)** | Dedicated server — one customer per physical machine | None | Dedicated NICs or VLANs | No — customer has direct hardware |
| **Azure / AWS / GCP** | Hyperscaler's model | Hyperscaler's model | Hyperscaler's model | Hyperscaler's model |

A Private Cloud or Bare Metal customer still logs into the same shared Apt Cloud portal. A reseller's customers on VPC are multi-tenant at the infrastructure level but isolated at the platform level through org hierarchy. The tenancy boundaries differ at each layer; the platform normalizes the operational experience regardless of underlying tenancy.

---

## 4. Technical Specifications

### 4.1 Infrastructure Stack

```
┌────────────────────────────────────────────────┐
│  Apt Cloud Portal (CloudOps Software)           │  Customer-facing
│  portal.aptum.com                               │
│  CloudStack Plugin                              │  API integration
├────────────────────────────────────────────────┤
│  Apache CloudStack 4.22                         │  Cloud orchestration
│  (Zones, Pods, Clusters, VMs, Networking,       │
│   Storage, Templates)                           │
├────────────────────────────────────────────────┤
│  KVM Hypervisor                                 │  Virtualization
├────────────────────────────────────────────────┤
│  Dell Enterprise Servers / Intel Xeon           │  Aptum-owned hardware
│  Pullman Data Centre (Toronto)                  │
└────────────────────────────────────────────────┘
```

**Budget (Internal SOW GSE-155):** ~$52K USD (CloudStack Design $22K, Hardware $20K, Training $10K)

**Initial Capacity Sizing (Compute Calculation v0.1):**
- Target workload: 316 vCPU, 1,389 GB RAM, ~67 TB standard storage (Ignite VMs)
- vCPU:pCPU overcommit ratio: 4:1
- Operational headroom: 10% CPU, 20% memory/storage
- Compute node spec: 32 cores, 768 GB RAM per node

### 4.2 Primary Site: Pullman Data Center, Toronto

| Specification | Detail |
|---|---|
| **Address** | 20 Pullman Court (TOR-4), Toronto, ON |
| **Tier Rating** | Tier II Design standards |
| **Compliance** | SOC 2 Type II for datacenter operations |
| **Power Redundancy** | N+1 on all electrical/mechanical (UPS, switchgear, generators) |
| **Backup Power** | On-site diesel generators, 48-hour fuel runtime, live refueling contracts |
| **Cooling** | N+1 redundant CRAC units, ASHRAE-compliant temperature/humidity |

### 4.3 Compute

- **Hardware:** Dell enterprise-grade servers with Intel Xeon processors
- **Virtual Machines:** Shared compute pool. Multiple VMs per host. Resizable (requires restart). Based on pre-defined images (OS templates or ISOs).
- **Sizes:** Bundles of vCPU + memory. Changeable after deployment.
- **Batch Creation:** Deploy multiple identical instances simultaneously.
- **Automation:** Post-launch configuration hooks.
- **Affinity Groups:** Control VM placement across physical hosts.

> **Note on Bare Metal:** BMaaS is not currently implemented. A 5c/Hypertec integration exists (Canonical MaaS at the CloudStack layer) that could be adopted. For now, dedicated physical hosts are delivered as "Private Cloud" through the virtual orchestration layer.

### 4.4 Storage

| Tier | Technology | Performance | Use Case | Status |
|---|---|---|---|---|
| **Performance** | Enterprise SSD (SAS/SATA) | 6 IOPS per GB | Databases, high-traffic websites, app servers | Available |
| **Standard** | Enterprise SSD (SAS/SATA) | 2 IOPS per GB | General purpose, web servers, moderate I/O | Available |
| **NVMe** | Premium NVMe | Highest IOPS | High I/O workloads | Roadmap |

**Pricing model:** Billed on allocated capacity (GB/month). **No transaction costs** (IOPS charges) or throughput fees — predictable monthly billing unlike public clouds.

### 4.5 Networking

| Specification | Detail |
|---|---|
| **East-West (Internal)** | 10 Gbps redundant links per host (VM-to-VM) |
| **North-South (External)** | Dedicated uplinks at 10 Gbps or 100 Gbps |
| **Carrier Neutrality** | 15+ carriers via on-site Meet-Me-Room |
| **Latency** | <2ms to major Toronto internet exchanges (TorIX) and hyperscale on-ramps |
| **DDoS Protection** | Always-on volumetric DDoS at network edge (included) |
| **Private Networking** | VLANs for isolation (VXLAN support TBD) |
| **Public IPs** | Manageable blocks via portal |
| **VPN** | User-configurable VPN via portal |
| **Port Forwarding** | Configurable via portal (important feature) |

### 4.6 Firewall ("Edge Security" Model)

| Tier | Description | Status |
|---|---|---|
| **Standard** | Built-in Security Groups managed in Apt Cloud. Rules set at network tier by CIDR, ingress/egress, protocol, port (can target /32 for effective per-VM control). Technically delivered by Aptum IaaS through Apt Cloud. | Available |
| **Advanced** | Dedicated Virtual Firewalls (pfSense, FortiGate VM) at VPC edge — deep packet inspection, VPN termination, advanced routing | Near-term roadmap (testing needed) |
| **Managed** | Fully managed hardware firewall (HA pair) physically racked in front of private cloud | Near-term roadmap |

### 4.7 Load Balancing

| Tier | Capabilities | Self-Service? |
|---|---|---|
| **Standard** | Layer 4 (TCP) load balancing with sticky sessions and multiple routing algorithms | Yes (via portal) |
| **Advanced / Managed** | Layer 4 + Layer 7 (HTTP/HTTPS), SSL termination, health checks | Not self-service (yet) |

### 4.8 Supported Operating Systems

List OS families only (versions change regularly):

**Linux:** Ubuntu, RHEL, AlmaLinux, Rocky Linux, Debian
**Windows:** Windows Server (Standard & Datacenter editions)
**BYO Image:** Upload custom QCOW2 or ISO images via the portal

### 4.9 Infrastructure Catalog Roadmap (CloudStack Extensions Framework)

Apache CloudStack 4.21 introduced the Extensions Framework ("XaaS" / "Orchestrate Anything"), extended further in 4.22. This allows CloudStack to orchestrate external systems (Proxmox, MAAS, Hyper-V) via registered executables, while CloudStack handles networking, RBAC, billing, usage tracking, events, and UI.

| Service | Orchestration | Status | Notes |
|---|---|---|---|
| **VPC** (KVM) | CloudStack native | **Live** | Multi-tenant shared compute |
| **Private Cloud** (KVM) | CloudStack native | **Live** | Single-tenant dedicated hosts |
| **Bare Metal as a Service** | CloudStack → MAAS extension (4.22) | **Roadmap** | Self-service provisioning of pre-racked hardware through Apt Cloud. Needs testing + operationalization. |
| **Proxmox Managed** | CloudStack → Proxmox extension (4.21+) | **Roadmap** | Ops capability exists. Limitations: no live migration, no VM scaling, no capacity reporting to CloudStack. Needs testing. |
| **VMware Private Cloud** | Apt Cloud VCD plugin (ThinkOn) or CloudStack native ESXi | **Live** (via ThinkOn MTC) | Licensing via ThinkOn |
| **Kubernetes** | CloudStack CKS + Apt Cloud K8s plugin | **Near-term roadmap** | CSI tested; plugin exists |

Each new extension expands the infrastructure catalog without proportional engineering investment. The CloudOps Software team tests, operationalizes, and surfaces each extension through Apt Cloud.

---

## 5. Apt Cloud Portal Architecture (CloudOps Software)

### 5.1 Services in Apt Cloud (portal.aptum.com)

```
┌─────────────────────────────────────────────────────────────────┐
│                 APT CLOUD (portal.aptum.com)                    │
│         White-labeled CloudOps Software instance                │
│    Home · Orgs · Environments · RBAC · API · Monetization       │
│    Reporting · Activity Logging · Branding · Knowledge Base     │
├────────────┬────────────┬───────────────┬───────────────────────┤
│ Aptum IaaS │  MTC       │ Microsoft     │  Cloudflare DNS       │
│(CloudStack)│ (ThinkOn)  │ Azure         │  (DNS Mgmt)           │
│            │            │               │                       │
│ VMs (VPC)  │ VMs        │ Instances     │  Domains              │
│ Volumes    │            │ Disks         │  DNS Records          │
│ Networking │            │ Networks      │  Proxied Traffic      │
│ Snapshots  │            │ AKS (K8s)     │                       │
│ Images     │            │               │                       │
│ SSH Keys   │            │               │                       │
│ Affinity   │            │               │                       │
│ LB (L4)    │            │               │                       │
│ FW / SGs   │            │               │                       │
│ Port Fwd   │            │               │                       │
├────────────┴────────────┴───────────────┴───────────────────────┤
│    Available to adopt: AWS · GCP · Kubernetes (standalone)       │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 User Roles

| Role | Description | Notes |
|---|---|---|
| **Operator** | Aptum internal. Full access to CloudOps Software features (branding, plugins, monetization, global admin). Does NOT have access to customer resources (VMs, disks, networks). Not exposed to users. | |
| **Reseller** | Manages service connections and downstream organizations. Currently Aptum acts as the Reseller. A true multi-reseller model is WIP (ES Williams being explored as early beta). | Not yet implemented as designed |
| **Admin** | Organizational administrator. Manages users, environments, and cloud resources within their organization. | Does not manage service connections (Reseller only) |
| **User** | Provisions and manages resources within assigned environments. | Formally called "User" (not "End User") |
| **Guest** | Specialized limited access for particular users. | Useful for restricted visibility |

### 5.3 User Personas

**Apt Cloud Personas:**

| Persona | Primary Need |
|---|---|
| CIO / Head of IT | Control, governance, cost visibility |
| Platform / Cloud Ops | Automation, consistency, lifecycle |
| Finance | Cost transparency, forecasting |
| Security / Compliance | Policy, auditability |

**Aptum IaaS Target Segments:**

| Segment | Primary Use Case |
|---|---|
| SMB / Mid-Market | Predictable private cloud |
| Regulated Industries | Data sovereignty, compliance |
| Hyperscale-Fatigued | Repatriation from public cloud |
| Hybrid Adopters | Mixed workload placement |

### 5.4 Service Plugins

| Plugin | Status in Apt Cloud | Resources |
|---|---|---|
| **Apache CloudStack** | Active ("Aptum IaaS") | VMs, volumes, networking, snapshots, images, affinity groups, SSH keys, L4 LB, security groups, port forwarding |
| **VMware Cloud Director** | Active ("MTC" on ThinkOn) | VMs, networking, storage |
| **Microsoft Azure** | Active | Instances, disks, networks, **Azure Kubernetes Service (AKS)** |
| **Cloudflare DNS** | Active (replaces SuperDNS) | Domains, DNS records, proxy config |
| **AWS / GCP / K8s** | Available to adopt (built, not yet configured in Apt Cloud) | — |

### 5.5 Core Sub-Systems

| Sub-System | Function |
|---|---|
| **Service Orchestration** | Central engine communicating with backends via plugins |
| **Governance** | Policy enforcement, quotas, budgets, compliance, SOC 2 |
| **Multi-Tenancy Management** | Hierarchical orgs/sub-orgs |
| **Reports** | Usage reporting, cost breakdowns |
| **Metrics** | Real-time resource consumption tracking |
| **Monetization** | Product catalogs, pricings, utility billing, commitments, discounts/credits, tiered pricing, multi-currency, invoicing, revenue reporting, rollback |
| **Content Management** | Searchable multilingual knowledge base |
| **Branding** | Per-reseller white-label |
| **Trial Management** | Automated trial provisioning |
| **Logging** | Unified activity logging across all services/environments |
| **Security** | RBAC, authentication (OpenID Connect, native, 2FA) |

> **Not currently implemented:** Workflows (Temporal — tested but not deployed), Alerting/push notifications.

### 5.6 Entity Model

**Organization** → **Service Connection** → **Environment** → **Resources**

- Organizations can have sub-organizations (reseller/MSP structures)
- Environments map to CloudStack resources, Azure resource groups, Cloudflare accounts, etc. (Environments = groupings of people and resources for managing resources and their associated costs)
- Membership + RBAC at every level
- Chargeback data viewable per Organization; can also be viewed per-environment for internal chargeback

---

## 6. Self-Service Capabilities (via Apt Cloud)

What customers can do themselves through the portal:

**Provisioning:** Spin up/down VMs, allocate storage volumes, create snapshots.
**Networking:** Configure private networks (VLANs), manage public IP blocks, set up VPN users, configure port forwarding.
**Governance:** Manage environments (groupings of people and resources) for different teams, set resource quotas, view real-time billing data.
**Load Balancing:** L4 TCP load balancing with sticky sessions and routing algorithms (self-service). L7/SSL termination available in Advanced/Managed tiers (not self-service yet).
**Firewalls:** Manage Security Groups by CIDR, ingress/egress, protocol, port.
**Images:** Upload custom QCOW2 or ISO images.
**Cost Estimator:** Real-time pricing during provisioning, updates dynamically.
**API:** Full REST API for all operations. Terraform provider. Golang SDK.

### 6.1 Managed Service Tiers

Aptum IaaS and Apt Cloud are delivered across three service tiers. Infrastructure capabilities are the same; the tiers reflect the level of operational management Aptum provides.

| Tier | Who Manages What | Target Customer |
|---|---|---|
| **Self-Service** | Customer manages everything through Apt Cloud portal. Aptum keeps the platform running. | Developer teams, startups, cost-optimized workloads |
| **Managed Infrastructure** | Aptum manages hardware, hypervisor, network, and platform health. Customer manages OS and above. | SMB IT teams with some internal capability |
| **Fully Managed** | Aptum manages everything: hardware through application layer. Patching, backup, monitoring, security, DR. | Mid-market enterprises without internal IT depth. Regulated industries. |

The pricing delta between tiers is the managed services premium. See the Aptum Cloud Platform Strategy for full operational team structure and managed services detail.

---

## 7. Strategic Context

### 7.1 Why Apt Cloud Exists

- VMware licensing cost escalation post-Broadcom (10x+ increase)
- Margin erosion in legacy managed virtualization (~$27K MRC from 38 customers)
- Market expectation for true self-service and API-driven operations
- Need for a repeatable, scalable delivery platform across regions and clouds
- **Risk of not transitioning:** "Remaining on VMware will erode profitability and further limit market competitiveness"

### 7.2 Why Aptum IaaS Matters

Aptum IaaS is a **new product** — it is not a continuation of Aptum's historical "IaaS" usage.

- Infrastructure is the revenue-generating substrate
- Higher margins in private/shared compute vs. hyperscale resale
- Enables repatriation, hybrid, sovereignty, and compliance use cases
- Supports GTM motion around Broadcom alternatives
- No IOPS/throughput transaction fees (competitive advantage vs. public cloud)
- Folding MTC customers into Aptum IaaS over time will reduce costs and improve customer experience

### 7.3 The Name

> *"The name Apt Cloud was chosen to reflect both our brand and our intent. 'Apt' conveys capability, precision, and readiness, but also the idea of something custom and adapted to fit its environment."*

---

## 8. Migration Streams

Three distinct migration streams:

### Stream 1: MTC → ThinkOn (Completed, Delivered Through Apt Cloud)

Legacy MTC customers (Abiquo portal, VMware multi-tenant) have been migrated to **ThinkOn's MTC platform**. ThinkOn owns VMware licensing. However, MTC **is currently delivered through Apt Cloud** (portal.aptum.com). The future goal is to migrate MTC customers from ThinkOn (higher cost) to Aptum IaaS (lower cost, more features), still delivered through Apt Cloud.

### Stream 2: Ignite → Aptum IaaS (In Progress — First New Logos)

The first **new logo** customers onboarding to Aptum IaaS, migrating from Ignite Technology's Hyperbia infrastructure. This is the most important stream — it represents new business on the new platform. See Section 11.3 for details.

### Stream 3: Legacy Aptum Cloud → Aptum IaaS (Planned)

The 38 legacy "Aptum Cloud" customers (~$27K MRC) on VMware/Dell will be transitioned to Aptum IaaS. This will reduce operating costs by removing VMware licensing. Also targets legacy Private Cloud (vSphere) customers and any remaining managed virtualization customers.

### Stream 4 (Future): MTC → Aptum IaaS

Migrating MTC customers from ThinkOn infrastructure to Aptum-owned CloudStack infrastructure for cost reduction and improved customer experience. Still delivered through Apt Cloud.

### Stream 5 (Ongoing): Net-New Logos via GTM

New customer acquisition through three GTM motions: direct sales to VMware refugees and cloud repatriators, MSP channel recruitment, and migration/repatriation professional services engagements. See the Aptum Cloud Platform Strategy for full GTM detail.

---

## 9. Design Status (Phase 1)

Phase 1: **Strategy and Target State Definition** under SOW GSE-155.

**Deliverables:** Vision/objectives, product requirements, HLD, success criteria/KPIs, Phase 2 scope/risks/dependencies, risk register.

**Budget:** ~$52K USD | **Key Principle:** Prioritize existing Aptum assets.

---

## 10. Success Metrics

**Apt Cloud KPIs:** % of IaaS customers using portal, time-to-provision reduction, support ticket deflection, self-service adoption rate.

**Aptum IaaS KPIs:** Margin per deployment model (VPC vs. Private Cloud), churn reduction, average contract length, repatriation deal win-rate.

---

## 11. Historical Context

### 11.1 Legacy Products

| Product | What It Was | Revenue | Current Status |
|---|---|---|---|
| **Aptum Cloud (legacy)** | Managed VMs on VMware/Dell. No self-service. 38 customers. | ~$27K MRC | Stream 3: migration to Aptum IaaS planned |
| **MTC** | Self-service VMs via Abiquo → now on ThinkOn, delivered through Apt Cloud | ~$12K MRC | Active on ThinkOn; future migration to Aptum IaaS (Stream 4) |

### 11.2 ThinkOn MTC (Active — Delivered Through Apt Cloud)

MTC is currently delivered through **Apt Cloud (portal.aptum.com)** on ThinkOn infrastructure. ThinkOn owns VMware licensing (Cloud Director / VCF). This is a running service with existing customers. The future plan is to migrate these customers to Aptum IaaS (CloudStack) for lower cost and more features, still through Apt Cloud.

### 11.3 Ignite Program (First Aptum IaaS Customers — Contracts Signed)

**Ignite Technology** (operating as "Hyperbia") is an Alberta-based hosting provider. Ignite is offloading its customer base to Aptum — these are the **first Aptum IaaS customers** (Apt Cloud already has existing MTC and Azure customers). Workloads migrate from **Bell Maynard DC (Calgary) → Pullman DC (Toronto)**.

Ignite receives a **12% commission** on hosting revenue.

**Contract Structure:**
- "Service Continuation and Transfer Order"
- Signed by Ian Rae (CEO, Aptum)
- 6-month initial commitment for most customers; **SCADAcore has a 36-month (3-year) contract**
- Auto-renews month-to-month after initial term; 30-day notice to terminate
- Governed by Ignite's legacy T&Cs with Aptum substituted
- Pricing honors Ignite's existing pricing to customers

**Signed Transition Agreements — 7 New Logos (as of March 2026):**

| Client | Effective Date | MRR (CAD) | Term | Key SKUs |
|---|---|---|---|---|
| **SCADAcore** | 2026-03-18 | $24,868 | 36 months | 42 vCPU, 282 GB RAM, 24.4 TB perf storage, 8x SQL Ent |
| **ANHWP** | 2026-02-19 | $4,627 | 6 months | 32 vCPU, 107 GB RAM, 7.2 TB standard, 2x SQL Std |
| **ES Williams → Surerus Murphy JV** | 2026-02-23 | $5,283 | 6 months | |
| **ES Williams → Kings Energy** | 2026-02-23 | $2,726 | 6 months | |
| **ES Williams → Fleet Stop** | 2026-02-23 | $793 | 6 months | |
| **ES Williams → Island Tax** | 2026-02-23 | $479 | 6 months | |
| **ES Williams → Sharc Energy** | 2026-03-01 | $343 | 6 months | |
| **Signed Total** | | **$39,119/mo** | | **7 new logos** |

ES Williams is an MSP with multiple sub-customers, each with their own transition agreement. ES Williams is being explored as an early beta customer for the Reseller model within Apt Cloud.

**Customer-Facing Pricing (honoring Ignite pricing):**

| SKU | Unit Price (CAD) |
|---|---|
| vCPU (Compute) | $28.00/vCPU/mo |
| RAM (Memory) | $7.00–$7.25/GB/mo |
| Standard Storage | $0.28/GB/mo |
| Performance Storage | $0.56/GB/mo |
| IP Addresses | Included (committed quantity); overages at utility rates |
| Cloud Backup Repository | $30.00/TB/mo |
| SPLA SQL Standard (2-core) | $231.54/mo |
| SPLA SQL Enterprise (2-core) | $871.80/mo |
| SPLA Remote Desktop Services | $11.52/user/mo |

**Aptum Cost Basis (from margin calculator):**

| Resource | Customer Price | Aptum Cost | Margin |
|---|---|---|---|
| per vCPU | $28.00 | $7.31 | ~74% |
| per GB RAM | $7.00 | $1.83 | ~74% |
| per GB Flash Storage | $0.56 | $0.064 | ~89% |

---

## 12. Glossary

| Term | Definition |
|---|---|
| **Apt Cloud** | Cloud operations platform / control plane. NOT infrastructure. Powered by CloudOps Software. Accessed at portal.aptum.com. |
| **Aptum IaaS** | NEW infrastructure product (compute, storage, networking) on CloudStack/Aptum hardware. Delivered through Apt Cloud. |
| **Aptum Portal** | Alternate name for Apt Cloud / portal.aptum.com. |
| **VPC** | Virtual Private Cloud. Multi-tenant shared compute with isolation. |
| **Private Cloud** | Single-tenant dedicated compute. Combines technology + managed services. |
| **CloudOps Software** | SaaS orchestration platform (formerly CloudMC). The engine behind Apt Cloud. |
| **Apache CloudStack** | Open-source cloud orchestration. The orchestration layer for Aptum IaaS. |
| **Environment** | Grouping of people and resources for managing resources and their associated costs. |
| **Service Connection** | Configured link between CloudOps Software and a cloud backend. Managed by the Reseller role. |
| **Security Groups** | Firewall rules set at the network tier by CIDR, ingress/egress, protocol, port. |
| **QCOW2** | Disk image format for KVM. Customers can upload custom images. |
| **Cost Estimator** | Real-time pricing widget shown during provisioning. |
| **SOW GSE-155** | The design engagement for Apt Cloud architecture (Phase 1: ~$52K USD). |
| **ThinkOn MTC** | MTC on ThinkOn infrastructure, delivered through Apt Cloud. ~7 customers. Future: migrate to Aptum IaaS. |
| **Ignite / Ignite Technology** | Alberta-based hosting provider ("Hyperbia"). 7 customers (~$39K MRR) transitioning to Aptum IaaS. Signed Feb–Mar 2026. 12% commission. |
| **ES Williams** | MSP with multiple sub-customers transitioned under Ignite program. Early beta candidate for Reseller model. |

---

*Sources: [GSE-155] INT - SOW, [GSE-155] Fixed Bid SOW, Apt Cloud VPC Datasheet & FAQ, Apt Cloud UAT KB, CloudOps Software docs, internal CDOs, MTC pricing workbook, Ignite VM Details, Ignite Margin Calculator, signed Transition Agreements, Compute Calculation v0.1, Dell PowerEdge inventory, review feedback from Will Stevens and Stefan.*
