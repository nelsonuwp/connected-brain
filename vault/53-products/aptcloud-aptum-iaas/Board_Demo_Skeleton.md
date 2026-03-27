# Apt Cloud + Aptum IaaS - Board Demo & Discussion

## Flow

1. What we built and why
2. Live demo - what works today
3. Where the platform is going (roadmap)
4. Competitive landscape - honest look
5. How this makes customers sticky
6. What we still need to figure out


---


## 1. What We Built and Why

- Two distinct products that work together: Apt Cloud (the portal / control plane) and Aptum IaaS (the infrastructure)
- Apt Cloud is the single pane of glass - one login, one bill, one governance model across private cloud, bare metal, and hyperscalers
- Aptum IaaS is our own compute, storage, and networking on CloudStack + KVM on hardware we own in our own data centers
- Why now: Broadcom's VMware acquisition created forced migration (300-1,050% price increases, 35% of workloads expected to move by 2028). We're positioned on the right side of that.
- We already have the data centers, the ops teams, the hardware. The missing piece was the platform. That's what Apt Cloud is.


---


## 2. Live Demo - What Works Today

### Apt Cloud Portal (portal.aptum.com)
- Walk through the portal as a customer would see it
- Org hierarchy: Aptum (operator) > Reseller (e.g., ES Williams) > End customer (e.g., Fleet Stop)
- Self-service VM provisioning: pick compute, storage, network, see real-time cost estimate, deploy
- Lifecycle management: start, stop, scale, snapshot, destroy
- RBAC: show different permission levels (Operator, Reseller, Admin, User, Guest)
- Activity logging: every action tracked across all services

### Aptum IaaS (CloudStack)
- Show a live customer environment (SCADAcore or an ES Williams sub-customer)
- VPC: multi-tenant shared compute with logical isolation
- Private Cloud: dedicated hosts, single-tenant
- Networking: VLANs, virtual routers, security groups (firewall rules)
- Storage: standard and performance tiers

### Hyperscaler Integrations (Live)
- Microsoft Azure plugin: show Azure resources managed through Apt Cloud alongside CloudStack resources
- Cloudflare DNS: domain and DNS record management through the same portal

### Hyperscaler Integrations (Built, Not Yet Configured)
- AWS plugin: built by CloudOps Software team, ready to configure
- GCP plugin: same status

### Monetization Engine
- Product catalogs, pricing configuration, utility pricing
- Cost visibility and usage reporting
- Credit card integration, tax integration
- This is the billing backbone for both direct customers and the reseller channel

### MTC (ThinkOn - Live Through Apt Cloud)
- Show MTC customers accessing VMware-based private cloud through the same Apt Cloud portal
- Same UX, same governance, different infrastructure backend


---


## 3. Where the Platform Is Going

### Near-Term (Q2 2026 - Foundation)
- Finish reseller billing + per-reseller pricing (highest ROI item - unlocks the channel)
- White-label portal branding per reseller
- Complete Ignite customer migrations to Pullman DC
- Define go-forward pricing (not legacy Ignite rates)
- Publish self-service VPC pricing on aptum.com
- Operational readiness review for multi-tenant

### Mid-Term (Q3-Q4 2026 - Catalog Expansion)
- Bare Metal as a Service via MAAS extension (CloudStack 4.22 ready, needs testing + operationalization). Customer self-provisions a dedicated physical server through the portal the same way they provision a VM today.
- Proxmox VE orchestration via CloudStack extension (ops capability exists, needs testing). Opens the door for customers migrating off VMware to Proxmox with Aptum managing the environment.
- Kubernetes service offering (CKS + Apt Cloud plugin, CSI tested)
- Recruit first 5 MSP resellers
- Second DC scoping: US (Herndon) or UK (Portsmouth)

### Longer-Term (H1 2027 - Scale)
- Multi-region: deploy CloudStack cluster in second DC
- Scale to 20+ MSP resellers
- AWS/GCP plugin activation
- GPU/AI infrastructure evaluation
- Government cloud certification pursuit


---


## 4. Competitive Landscape - Honest Look

### The question: "Who competes with Apt Cloud?"

Short answer: nobody does exactly what we do. The market breaks into three camps, and none of them combine all three of infrastructure + self-service portal + managed operations.

**Cloud Management Platforms (software-only, no infrastructure)**
- HPE Morpheus: broadest integration library, enterprise IT governance tool. No CloudStack support. No white-label. Not built for external paying customers. Designed for Fortune 500 internal IT teams managing their own hybrid environments.
- CloudBolt: closest to what we need (MSP-oriented, white-label billing). Still no CloudStack support. Their MSP billing is designed for public cloud resale margin management, not private IaaS delivery. If we bought CloudBolt, we'd still need to build the CloudStack integration from scratch - at which point we've duplicated what CloudOps Software already does natively.
- VMware Aria (vRealize): locked to VMware/Broadcom stack. Adopting it would reintroduce the exact vendor dependency our strategy is built to avoid.

**Key point for the board:** We evaluated every major commercial CMP. None integrate with CloudStack. None are built for delivering commercial IaaS to external paying customers. They're all internal IT governance tools. The "buy" option doesn't exist for our use case.

**Infrastructure Providers (competitors for customer spend)**
- ThinkOn: our most direct Canadian competitor. VMware Sovereign Cloud partner. Government-approved (Shared Services Canada). Channel-only. But: deep Broadcom/VMware dependency (structural cost disadvantage), no self-service portal comparable to Apt Cloud.
- OVHcloud: aggressive pricing, global footprint. But: not a managed services provider, limited Canadian presence (Montreal, not Toronto), VMware licensing pressure post-Broadcom.
- Rackspace: deep managed services, "Fanatical Support" brand. But: enterprise pricing (significantly more expensive), no Canadian sovereignty play, filed for bankruptcy in 2023.
- DigitalOcean/Vultr/Hetzner: cheap VMs, great developer UX. But: no managed services, no white-label, no MSP channel. Different market entirely.
- OpenMetal: OpenStack + Ceph, good pricing. US-only, no managed services.

### The question: "How do we compare?"

| | Apt Cloud + Aptum IaaS | ThinkOn | Rackspace | OVHcloud | DigitalOcean |
|---|---|---|---|---|---|
| Self-service portal | Yes | Limited | Yes | Yes | Yes |
| Managed services (24/7) | Yes | Moderate | Yes (premium) | No | No |
| Canadian sovereignty | Yes (Toronto) | Yes (multi-CA) | No | Partial (Montreal) | Partial (Toronto) |
| White-label / MSP channel | Yes (architectural) | No | No | No | No |
| Hypervisor-agnostic | Yes (KVM, Proxmox, VMware, bare metal) | No (VMware only) | Partial | Partial | No |
| VMware licensing overhead | None (CloudStack/KVM) | Yes (structural cost) | Yes | Yes | N/A |
| Public pricing page | Not yet | No | No | Yes | Yes |
| Customer base / references | Early-stage (7 logos) | Established (gov't) | Thousands | Millions | Millions |

### The question: "How far are we from the competition / our ideal state?"

**What's working:**
- Portal is live with real customers on it
- Self-service provisioning, RBAC, lifecycle management, cost estimator all functional
- Azure and Cloudflare integrations live
- Monetization engine operational
- 7 signed customers, ~$39K MRR
- 74-89% gross margins on infrastructure

**What's not done yet (the honest gaps):**
- Reseller white-label branding and per-reseller pricing: architecturally supported, not yet configured. This is the channel unlock and the highest-ROI item on the roadmap.
- Billing integration depth: multi-currency pricing, custom SKUs, invoicing pipeline need completion
- No public pricing page. Every competitor that serves self-service customers has one. We can't do inbound without it.
- Managed services automation layer: backup orchestration, patch workflows, remediation runbooks not yet built into the platform (these are done manually by the ops team today)
- Monitoring/SLA dashboards: need Prometheus, Grafana, PagerDuty integration for customer-facing visibility
- ITSM/ticketing integration not wired in
- Self-service catalog limited to VM/network SKUs today. Storage tiers, managed add-ons, bare metal, Proxmox, K8s all roadmap.
- Operational readiness for multi-tenant: Managed Cloud team has flagged that shared-cluster ops need more rigorous change management than dedicated hosting. Team is thin for the expanding scope.
- Small customer base. No case studies. No references beyond the Ignite logos. Enterprise buyers will ask for proof of scale we don't have yet.
- No GPU/AI infrastructure play (known gap, not immediate priority for our target customer)

### The question: "Why isn't ThinkOn using our software?"

ThinkOn is a VMware Cloud Foundation (VCF) shop. Their entire stack is VMware. They deliver managed VMware private cloud through VMware's native tooling (vCenter, Cloud Director, NSX, vSAN). They don't need a CloudStack portal because they don't run CloudStack.

ThinkOn's relationship with Aptum today: they provide the VMware-licensed infrastructure for our MTC customers, delivered through Apt Cloud. They are a partner, not a customer of the Apt Cloud software.

Could ThinkOn use Apt Cloud? Architecturally, yes - Apt Cloud has a VCD plugin. But ThinkOn has no incentive to adopt a portal layer they don't control from a company that is increasingly their competitor (as we migrate MTC customers off their infrastructure onto ours). The relationship will get more complex as Aptum IaaS matures.

What ThinkOn does NOT have that we do: a multi-cloud, hypervisor-agnostic self-service portal. ThinkOn can deliver VMware. They can't deliver VMware + KVM + Proxmox + bare metal + Azure + AWS through one portal with white-label and MSP billing. That's the product gap we're filling.


---


## 5. How This Makes Customers Sticky

### The multi-product stickiness model

Single-product customers churn easily. Multi-product customers don't. Every additional integration point increases switching cost. The platform is designed to pull customers deeper over time:

| Phase | What they're buying | Typical MRR | Switching difficulty |
|---|---|---|---|
| Entry | VPC or Private Cloud (infra only) | $2K-$8K | Easy to replace |
| Foundation | + Managed OS / patching / monitoring | $5K-$15K | Would need to find new ops team |
| Established | + Backup + firewall/WAF + hybrid Azure/AWS | $10K-$30K | Unwinding requires a project |
| Embedded | + ExpressRoute/Direct Connect + DR + PS | $15K-$50K | Aptum IS their IT department |

### What makes this work
- One portal across private cloud, bare metal, and hyperscalers. Once a customer's Azure and CloudStack resources are both in Apt Cloud, moving means re-platforming everything.
- Managed services on top. They're not just buying VMs. They're buying 24/7 ops, patching, backup, monitoring, firewall management. Replacing that means hiring 2-3 people.
- Reseller channel multiplies this: an MSP with 50 customers on Apt Cloud has even less reason to move. Their billing, their customer management, their pricing is all built on the platform.
- No VMware licensing overhead means we can be the lowest-cost managed provider while maintaining strong margins, or invest that margin into service quality and channel incentives.

### Real example (early signal)
- SCADAcore: 42 vCPU, 282 GB RAM, 24 TB storage, 8x SQL Enterprise. $24,868/mo. 36-month contract. They signed because they needed a managed environment they didn't have to think about. That's the value prop.
- ES Williams: MSP with 5 sub-customers. If we finish the reseller billing + white-label, they become a channel partner selling Aptum IaaS under their own brand. Each of their customers becomes an Aptum customer without us paying for acquisition.


---


## 6. What We Still Need to Figure Out

These are open items, not weaknesses. Putting them on the table because the board should weigh in.

- **ICP definition:** The Strategy proposes a single ICP: mid-market company (or MSP serving them) with hybrid complexity that exceeds their internal IT capacity. This is the thesis. It's not locked in. The board should pressure-test whether this is too narrow, too broad, or right.
- **Go-forward pricing:** Ignite prices ($28/vCPU, $7/GB RAM in CAD) honor legacy agreements. What's the pricing for new customers? For the reseller wholesale tier? This needs to be defined before any real GTM activity.
- **GTM ownership:** All sales to date have been opportunistic (Ignite referrals). There is no GTM team or motion yet. The Strategy proposes trigger-based GTM (VMware renewal shock, cloud bill surprise, compliance events, IT staff departure, MSP channel). Who owns this? What's the investment?
- **Reseller model priority:** Finishing reseller billing + white-label is identified as the highest-ROI item. Is the board aligned on prioritizing channel over direct sales in the near term?
- **Operational readiness:** Managed Cloud team is thin relative to the expanding service catalog. Hiring before scaling, or scaling and hoping? This is a real risk.
- **ShapeBlue relationship:** Formal support/consulting engagement for CloudStack, or self-supporting? Formalizing provides risk mitigation and roadmap intelligence.
- **Professional services ownership:** No named Service Manager for PS. Accountability gap affects migration stream execution.
