# Apt Cloud + Aptum IaaS - Board Presentation

## The Story Arc

This isn't a product update. This is a pitch for why Aptum is sitting on a platform business that doesn't exist anywhere else in the Canadian market, at the exact moment the market needs it most. The VMware data isn't a problem slide - it's the proof that the opportunity is real and the window is open right now.

## Flow

1. The opportunity (why this moment matters)
2. What we built (the thing nobody else has)
3. Our VMware base - the case study in real time
4. Live demo
5. Where this goes (the vision at scale)
6. Why nobody can copy this easily
7. What we need from the board


---


## 1. The Opportunity

### The $54B market is being reshuffled right now

Broadcom's VMware acquisition is the largest forced migration event in enterprise infrastructure in a decade. This isn't speculation - it's happening:

- 300-1,050% price increases on VMware licensing (AT&T publicly accused Broadcom of a 1,050% hike)
- VMware operating margins went from 13-22% to 77% under Broadcom. That margin comes directly from customers.
- Gartner: 35% of VMware workloads will migrate to alternatives by 2028
- Forrester: VMware's largest 2,000 customers will shrink deployments by 40%
- Scale Computing: 140% increase in new customers Q1 2025, directly from VMware departures
- vSphere 7 end-of-support hit October 2025. Everyone still on it has to move.

This is not a slow shift. Companies are making infrastructure decisions right now, and those decisions lock in for 3-5 years.

### Simultaneously: cloud repatriation is mainstream

- 21% of migrated workloads are being rebalanced back from public cloud to private infrastructure
- 89% of organizations now operate multi-cloud
- A customer paying $15K/mo in Azure for 50 predictable VMs can repatriate to Aptum IaaS at materially lower cost, keep Azure for what needs hyperscale, and manage both through one portal

### The Canadian piece

Canadian cloud computing market: $54.8B in 2025, growing at 17.3% CAGR to $121.6B by 2030. IaaS is the fastest-growing segment at 21.8% CAGR. Regulated industries (healthcare, finance, government, legal) increasingly require Canadian data residency. Aptum has Toronto data centers with SOC 2 Type II and 15+ carrier-neutral connections.

### The gap in the market

Every company being squeezed by Broadcom needs the same thing: a way to run their infrastructure without VMware licensing overhead, with managed services so they don't have to hire a team, with a portal so they can see and control what they're buying, with the flexibility to keep Azure/AWS for what makes sense there.

Nobody provides all of that today. That's what we built.


---


## 2. What We Built - And Why It's a Differentiator, Not Catch-Up

### The two-layer architecture

**Apt Cloud** is the control plane. One portal, one bill, one governance model across private cloud, bare metal, and hyperscalers. Self-service provisioning. RBAC. Cost visibility. Activity logging. Monetization engine with white-label capability and per-reseller pricing. This is the software layer - powered by CloudOps Software (formerly CloudMC), accessed at portal.aptum.com.

**Aptum IaaS** is the infrastructure. Our own compute, storage, and networking on Apache CloudStack 4.22 + KVM, running on Dell hardware in Aptum data centers. Zero VMware licensing overhead. 74-89% gross margins. This is infrastructure we own, operate, and control the pricing on.

### Why this is different from everything else in the market

The market has three camps. None of them do what we do:

**Camp 1: Cloud Management Platforms (HPE Morpheus, CloudBolt, VMware Aria)**
Software only. No infrastructure. Designed for Fortune 500 internal IT teams to govern their existing environments. None support CloudStack. None are built to deliver commercial IaaS to external paying customers. None have white-label MSP billing. We evaluated every one of them. The "buy" option does not exist for our use case.

**Camp 2: Infrastructure Providers (ThinkOn, Rackspace, OVHcloud, DigitalOcean)**
Infrastructure, but locked to specific hypervisors. No self-service portal with white-label MSP capability. ThinkOn is VMware-dependent (structural cost disadvantage). Rackspace filed for bankruptcy. OVHcloud has no managed services. DigitalOcean has no enterprise ops.

**Camp 3: Hyperscalers (Azure, AWS, GCP)**
Unlimited scale, but no managed services for mid-market, no Canadian sovereignty guarantees, and customers are increasingly looking to reduce - not increase - their dependency.

**We sit in the middle of the Venn diagram.** Own infrastructure + self-service portal + managed operations + white-label MSP channel + hypervisor-agnostic + multi-cloud in one pane. That combination does not exist anywhere else.

### This is not catch-up. Here's why.

Catch-up means building a worse version of something that already exists. Nobody has built what we're building because it requires something nobody else has: the operational teams AND the data centers AND the hardware AND the software platform AND the managed services org all in the same company.

- ThinkOn has data centers and government relationships but is welded to VMware and has no self-service portal. Broadcom owns their margin.
- Rackspace has managed services but collapsed under its own weight. Enterprise pricing. No Canadian play.
- CloudBolt has portal software but no infrastructure. They're a tool, not a platform.
- HPE Morpheus is an internal IT governance tool. It's not built to run a commercial IaaS business.

We're creating a category: **the managed multi-cloud platform for the Canadian mid-market**. The reason it doesn't exist yet is that it requires assembling capabilities that normally sit in different companies. Aptum already has all the pieces. The platform connects them.

### What's live today

- 7 signed customers (Ignite program), ~$39K MRR
- Self-service VM provisioning, RBAC, lifecycle management, real-time cost estimator
- Azure plugin live - Azure resources managed alongside CloudStack in one portal
- Cloudflare DNS integration live
- Monetization engine operational (product catalogs, pricing, credit card + tax integration)
- MTC customers accessing VMware-based private cloud through Apt Cloud (same UX, different backend)
- AWS and GCP plugins built, ready to configure


---


## 3. Our VMware Base - The Case Study Happening in Real Time

This section isn't about a revenue problem. It's about proving that the market thesis is real, and that the platform works, using our own customer base as the test case.

### The headline

In January 2024, our 54 VMware managed hosting customers were generating **$970,763 CAD/mo** in Online MRC. As of February 2026, those same client IDs account for **$679,496 CAD/mo**. That is a **$291,267/mo decline (-30.0%)**, roughly **$3.5M/yr**.

But the story isn't the decline. The story is what happened underneath it.

### The real story: multi-product customers don't leave

**29 of 54 customers actually grew their total spend.** Despite VMware disruption, despite price pressure, despite alternatives being available. They grew because they buy more than vHosts from us - they buy compute, networking, managed services, the whole stack. Townsquare Media has one vHost but a $112K/mo dedicated footprint. Leek United, Kinetico, WeirFoulds, Currencies Direct - they're not going anywhere.

**12 customers left entirely.** They were overwhelmingly single-product (vHost-only) or had shallow relationships. Gogotech, Be the brand, StraighterLine, 20-20 Technologies - vHosts and not much else. Easy to leave because there was no stickiness.

**8 customers dropped all VMware vHosts but are still spending $62K/mo on other services.** They left VMware. They didn't leave Aptum. That's the stickiness model working.

**5 customers are mid-migration right now** with substantial pending work:
- **Heilind**: $41K online + $38K pending. Upgrading ESXi 7.0 to 8.0 on new Dell 650xs. Net growth when complete.
- **Blue Yonder**: $19K online + $36K pending. Came back after going to $0 vHosts. Migrating to Pro Series 6.0/ESXi 8.0.
- **HYTECK**: $14K online + $20K pending. Including **$9.2K in Google Cloud** - they're going multi-cloud through Aptum. This is the Apt Cloud value prop in action.
- **Chicken Farmers**: $24K online + $13K pending. 3 vHosts migrating to newer hardware.
- **Netintegrity**: $13K online + $7K upgrading. ESXi 7.0 to 8.0.

Including all pending work ($117K/mo across 7 customers), the gap narrows to -18%.

### The generation cliff - the pipeline

80 active ESXi hosts remain across 32 customers ($241K/mo). But they're not all equal:

| Generation | Hosts | Customers | MRC | Avg contract left |
|---|---|---|---|---|
| Pre-5.0 (Legacy) | 5 | 2 | $10K | 3 months |
| Gen 5.0 | 46 | 22 | $142K | 6 months |
| Gen 6.0+ (New hardware) | 27 | 11 | $82K | 26 months |

**41 ESXi services across 19 customers ($124K/mo) have 6 months or less on contract.** Half the active VMware base is about to come up for renewal. Each one is a migrate-or-lose decision. This is the migration pipeline for Aptum IaaS - these are customers who already trust us and need to move.

### Why this matters for the board

This is not a problem to manage. It is a **live proof-of-concept for the entire platform thesis**:

1. **The Broadcom disruption is real.** 140 ESXi hosts deprovisioned in 2 years. 12 customers gone. The analyst forecasts are playing out in our own data.
2. **Multi-product relationships survive disruption.** 29 of 54 grew. The stickiness model works.
3. **The migration creates revenue, not just retention.** Heilind, Blue Yonder, HYTECK - they're spending more post-migration than pre. And HYTECK is adding Google Cloud through us.
4. **41 services expiring in 6 months = the pipeline.** We don't need to go find these customers. They're already here, already trust us, and have to make a decision.

### Note on methodology

Source: MRCTrend billing snapshots, Jan 31, 2024 vs Feb 28, 2026. Online services only. All figures in CAD (cad_mrc). 54 unique client IDs with at least one vHost service. Our Jan 2024 total ($970,763) aligns with the data team's figure ($1,006,517) within snapshot timing variance. Final numbers should be aligned with the data team before presenting.


---


## 4. Live Demo - What Works Today

### This is the slide that just says DEMO

Key things to walk through:

**Apt Cloud Portal (portal.aptum.com)**
- Walk through the portal as a customer would see it
- Org hierarchy: Aptum (operator) > Reseller (e.g., ES Williams) > End customer (e.g., Fleet Stop)
- Self-service VM provisioning: pick compute, storage, network, see real-time cost estimate, deploy
- Lifecycle management: start, stop, scale, snapshot, destroy
- RBAC: show different permission levels (Operator, Reseller, Admin, User, Guest)
- Activity logging: every action tracked across all services

**Aptum IaaS on CloudStack**
- Show a live customer environment
- VPC: multi-tenant shared compute with logical isolation
- Private Cloud: dedicated hosts, single-tenant
- Networking: VLANs, virtual routers, security groups

**Hyperscaler Integrations**
- Azure plugin: show Azure resources managed through Apt Cloud alongside CloudStack
- Cloudflare DNS: domain and DNS management through the same portal
- Point out AWS/GCP plugins are built and ready to configure

**Monetization Engine**
- Product catalogs, pricing configuration, utility pricing
- Cost visibility and usage reporting
- This is the billing backbone for both direct customers and the reseller channel

**MTC on ThinkOn - same portal, different backend**
- Show MTC customers accessing VMware-based private cloud through Apt Cloud
- This proves the platform is infrastructure-agnostic. Same UX whether the backend is CloudStack, VMware, or Azure.


---


## 5. Where This Goes - The Vision at Scale

### The near-term unlock (Q2 2026): the channel

The single highest-ROI item on the roadmap is finishing reseller billing + white-label portal branding. This is what turns Apt Cloud from a product into a platform business.

Here's what it looks like: An MSP with 50 clients signs up as an Aptum reseller. They get a white-labeled version of Apt Cloud under their own brand and domain. They set their own pricing for their customers. They provision infrastructure, manage billing, handle customer onboarding - all through the portal. Aptum provides the infrastructure, the managed ops, and the platform. The MSP provides the customer relationship and the last-mile support.

Every MSP customer becomes an Aptum customer without Aptum paying for acquisition. The MSP's business is built on the platform. Their billing, their pricing, their customer management - all on Apt Cloud. Switching means rebuilding their entire practice. That's the stickiness model at the channel level.

**ES Williams is already operating as a reseller with 5 sub-customers.** The billing isn't white-labeled yet, but the architecture works. Finishing this is the difference between 7 direct customers and potentially hundreds through the channel.

### The catalog expansion (Q3-Q4 2026): everything through one portal

The CloudStack 4.22 Extensions Framework is the key architectural enabler. It allows CloudStack to orchestrate external systems (Proxmox, MAAS, Hyper-V) via registered executables. This means:

- **Bare Metal as a Service (MAAS)**: Customer self-provisions a dedicated physical server through the portal the same way they provision a VM today. No tickets, no waiting. The hardware is Aptum's. The customer gets root access on dedicated metal, managed by Aptum.
- **Proxmox VE orchestration**: For customers migrating off VMware who want an open-source hypervisor alternative without going full CloudStack. Aptum manages the Proxmox environment, customer accesses it through Apt Cloud.
- **Kubernetes service (CKS)**: Container orchestration as a self-service catalog item. CSI tested. Customers run K8s alongside their VMs and bare metal through the same portal.

The vision: a customer logs into Apt Cloud and sees their VMs, their bare metal servers, their Kubernetes clusters, their Azure resources, their AWS resources, their DNS - all in one place. One bill. One support team. One governance model. They can provision any of it self-service or have Aptum manage it for them.

**Nobody else can do this** because nobody else has the infrastructure + the portal + the ops team + the multi-hypervisor orchestration in one company.

### The scale play (H1 2027 and beyond)

- **Multi-region**: Deploy CloudStack clusters in Herndon (US) and Portsmouth (UK). Same platform, multiple geographies. Opens up US and UK regulated workloads.
- **20+ MSP resellers**: Each with their own customer base on the platform. Network effects kick in - the more MSPs on the platform, the more the catalog improves, the more data we have on pricing and utilization.
- **AWS/GCP plugin activation**: Customers managing their entire multi-cloud footprint through Apt Cloud. This is the long game - become the control plane for everything, regardless of where it runs.
- **GPU/AI infrastructure**: When the market is ready, bare metal GPU as a service through the same portal. The MAAS extension makes this architecturally straightforward.
- **Government cloud certification**: Canadian government workloads require specific certifications. With Toronto DCs, SOC 2, and data sovereignty - this is a premium market segment that plays to Aptum's strengths.

### What this looks like at scale - the math

Today: 7 customers, $39K MRR, one DC, direct sales only.

The model with channel:
- 10 MSP resellers, each with 20 customers, avg $5K MRR per customer = $1M MRR from channel alone
- Plus 50 direct mid-market customers at $15K avg = $750K MRR
- Total: $1.75M MRR / $21M ARR
- At 74-89% gross margin, that's $15-19M in gross profit
- With two DCs and the full catalog, those numbers have room to grow significantly

This is not a services business that grows linearly with headcount. The platform is the leverage. Every MSP reseller multiplies revenue without multiplying operations proportionally.

### The flywheel

Infrastructure margin funds platform development. Platform attracts MSPs. MSPs bring customers. Customers generate infrastructure revenue. Infrastructure margin funds more platform development. Each turn of the wheel is cheaper than the last because the platform, the ops playbooks, and the infrastructure are already built.


---


## 6. Why Nobody Can Copy This Easily

### The question the board should ask: "What's the moat?"

**1. The integration is the moat.**
Any individual piece can be replicated. CloudStack is open-source. KVM is free. You can buy portal software. You can build a data center. But getting all of it to work together as a commercial platform - self-service provisioning, multi-tenant billing, white-label MSP channel, managed services, multi-hypervisor orchestration, hyperscaler integration - that's years of integration work. We're 18+ months into it with real customers on it.

**2. The operational team is the moat.**
Managed services require people who know the customer environments. Aptum's Service Desk and Managed Cloud teams already manage VMware, CloudStack, networking, storage, and security for production workloads. Replicating that takes years of hiring, training, and institutional knowledge. ThinkOn doesn't have it. OVHcloud doesn't have it. DigitalOcean doesn't have it.

**3. The existing customer base is the moat.**
42 VMware customers still billing. 41 ESXi services expiring in 6 months. These are warm leads who already trust Aptum with production workloads. A competitor starting from zero has to earn that trust from scratch.

**4. CloudStack + Extensions Framework is the moat.**
VMware-dependent providers (ThinkOn, most of the market) are structurally locked in. They can't offer VMware-free alternatives without rebuilding their entire stack. CloudStack's Extensions Framework lets us orchestrate anything - Proxmox, MAAS, Hyper-V, future hypervisors - through the same platform. We're building on the right foundation while the competition is locked to the foundation that's causing the problem.

**5. The white-label MSP channel is the moat.**
Once an MSP builds their practice on Apt Cloud - their pricing, their customer management, their billing - switching means rebuilding their business. That's structural lock-in at the channel level. No competitor in the Canadian mid-market offers this.

### The ThinkOn question

"Why isn't ThinkOn using our software?"

ThinkOn is a VMware Cloud Foundation shop. Their entire stack is VMware (vCenter, Cloud Director, NSX, vSAN). They don't need a CloudStack portal because they don't run CloudStack. They are a partner (providing VMware infrastructure for our MTC customers), not a customer.

Could they use Apt Cloud? Architecturally yes - we have a VCD plugin. But ThinkOn has no incentive to adopt a portal from a company that is increasingly their competitor.

What ThinkOn cannot do: deliver VMware + KVM + Proxmox + bare metal + Azure + AWS through one portal with white-label MSP billing. They're a single-hypervisor shop in a multi-hypervisor world. Broadcom owns their margin. That's not a position of strength.


---


## 7. Live Demo - What Works Today

*(Demo section - same as Section 4 above, positioned here if the flow works better with vision before demo)*


---


## 8. What We Need From the Board

These aren't problems. They're investment decisions. The platform works. The market is moving. The question is how aggressively to move.

- **Channel investment priority:** Finishing reseller billing + white-label is the highest-ROI item. It's the difference between a product and a platform business. Is the board aligned on prioritizing channel over direct sales in the near term?

- **Go-forward pricing:** Ignite prices ($28/vCPU, $7/GB RAM) honor legacy agreements. New customer pricing and wholesale reseller pricing need to be defined before real GTM activity. This is a strategic decision, not just a finance exercise - it determines positioning.

- **GTM ownership and investment:** All sales to date have been opportunistic (Ignite referrals). There is no GTM team or motion yet. The Strategy proposes trigger-based GTM (VMware renewal shock, cloud bill surprise, compliance events, MSP channel). Who owns this? What's the budget?

- **Migration velocity:** 41 ESXi services across 19 customers ($124K/mo) expire within 6 months. Each is a migrate-or-lose decision. Do we invest in dedicated migration resources to capture these, or risk losing them to inertia?

- **Operational capacity:** Managed Cloud team is thin relative to expanding scope. Hiring ahead of demand is an investment. Hiring behind demand means dropping the ball on the customers we just won. What's the appetite?

- **Second DC timeline:** Multi-region is the scale unlock. US (Herndon) or UK (Portsmouth) first? This is a capital decision with long lead time.

- **ICP definition:** The Strategy proposes mid-market companies (or MSPs serving them) with hybrid complexity exceeding internal IT capacity. Is this the right target? Too narrow? Too broad?
