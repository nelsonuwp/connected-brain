# Apt Cloud + Aptum IaaS — Board Presentation

## Flow

1. The Broadcom mess and why it matters
2. How it affected our customer base (our VMware numbers)
3. What we built and why (including competitive landscape)
4. Live demo
5. Why this is hard to copy
6. Where this goes
7. Appendix: What we need from the board

---

## 1. The Broadcom Mess and Why It Matters

### What happened

Broadcom completed its $61B acquisition of VMware in December 2023 and immediately restructured the licensing model. The changes hit mid-market customers hardest:

- Perpetual licenses were eliminated entirely. Every customer was forced onto subscription models. *(Source: [Broadcom Negotiations](https://broadcomnegotiations.com/vmware-licensing-cost-increases-under-broadcom-what-enterprises-should-expect/))*
- Minimum core requirements jumped from 16 cores to 72 cores, effective April 2025. A customer running a small 16-core host now pays for 72 cores whether they use them or not. *(Source: [Hystax analysis of Broadcom pricing changes](https://hystax.com/how-vmware-prices-and-policies-changed-after-broadcoms-acquisition/))*
- ~168 product bundles were consolidated into 4 offerings. Mid-market products like vSphere Essentials Plus were discontinued. *(Source: [IDC VMware Cost Analysis](https://www.idc.com/resource-center/blog/vmware-cost-increases-how-broadcom-vmware-product-offerings-are-evolving/))*
- Reported price increases range from 300% to 1,500% depending on customer size and geography. AT&T publicly accused Broadcom of a 1,050% increase. European customers have reported increases up to 1,500%. *(Sources: [Network World](https://www.networkworld.com/article/3994107/vmware-customers-in-europe-face-up-to-1500-price-increases-under-broadcom-ownership.html); [CIO Dive](https://www.ciodive.com/news/broadcom-vmware-vcf-adoption-second-phase/759406/))*

### Why it matters for infrastructure decisions

Gartner estimates 35% of VMware workloads will migrate to alternatives by 2028. A separate survey of 550+ enterprise IT leaders found 56% plan to decrease VMware usage within one year, and 74% are exploring or piloting non-VMware platforms. *(Sources: Gartner Peer Community survey; [Foundry/CIO.com enterprise survey](https://www.ciodive.com/news/broadcom-vmware-vcf-adoption-second-phase/759406/))*

vSphere 7 reached end of general support in October 2025. Customers still running it face a choice: pay Broadcom's new pricing for an upgrade, or move to a different platform entirely. These decisions lock in for 3–5 years.

### The Canadian context

The Canadian cloud computing market is valued at approximately $54.8B USD in 2025, with IaaS as the fastest-growing segment at roughly 21–23% CAGR. *(Sources: [Mordor Intelligence — Canada Cloud Computing Market](https://www.mordorintelligence.com/industry-reports/canada-cloud-computing-market); [KBV Research — North America IaaS Market](https://www.kbvresearch.com/north-america-infrastructure-as-a-service-market/))*

Regulated industries in Canada (healthcare, finance, government, legal) increasingly require or prefer Canadian data residency. Quebec mandates privacy assessments before sending data outside the province. British Columbia requires public bodies to store personal information in Canada. The federal government's Sovereign Cloud Initiative requires specific public sector contracts to use Canadian-owned infrastructure. *(Source: [Government of Canada — Data Sovereignty White Paper](https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/cloud-services/digital-sovereignty/gc-white-paper-data-sovereignty-public-cloud.html))*

Aptum has Toronto data centers with SOC 2 Type II certification and 15+ carrier-neutral connections.

### The parallel trend: cloud repatriation

Roughly 21% of workloads that moved to public cloud are being rebalanced back to private infrastructure, according to the Flexera 2025 State of Cloud Report. An 86% figure from a Barclays CIO survey indicates the proportion planning to move *some* workloads back — the distinction matters, because most organizations are selectively repatriating specific workloads, not abandoning public cloud wholesale. *(Sources: [Flexera State of Cloud 2025](https://www.infoworld.com/article/3842349/cloud-trends-2025-repatriation-and-sustainability-make-their-marks.html); [Barclays CIO Survey via ChannelNomics](https://www.channelnomics.com/insights/breaking-down-the-83-public-cloud-repatriation-number))*

A customer paying $15K/mo in Azure for 50 predictable VMs can repatriate those workloads to Aptum IaaS at materially lower cost, keep Azure for what genuinely needs hyperscale, and manage both through one portal.

### The gap

Every company being squeezed by Broadcom needs infrastructure without VMware licensing overhead, managed services so they don't need to hire a team, a portal for visibility and control, and the flexibility to keep Azure/AWS for what makes sense there. Nobody provides all of that today in the Canadian mid-market.

---

## 2. Our VMware Base — The Case Study Happening in Real Time

This section frames our own customer data as evidence that the Broadcom disruption is real and that multi-product customer relationships survive it.

### The headline numbers

In January 2024, our 54 VMware managed hosting customers were generating $970,763 CAD/mo in Online MRC. As of February 2026, those same client IDs account for $679,496 CAD/mo — a $291,267/mo decline (−30.0%), roughly $3.5M/yr.

The decline is real, but what happened underneath it is more interesting than the top-line number.

### Multi-product customers don't leave

29 of 54 customers grew their total spend despite the VMware disruption, despite price pressure, despite alternatives being available. They grew because they buy more than vHosts from us — compute, networking, managed services, the full stack. Townsquare Media has one vHost but a $112K/mo dedicated footprint. Leek United, Kinetico, WeirFoulds, Currencies Direct — they expanded during a period when the market was pushing them toward the exits.

12 customers left entirely. They were overwhelmingly single-product (vHost-only) or had shallow relationships. Gogotech, Be the Brand, StraighterLine, 20-20 Technologies — vHosts and not much else. There was no stickiness because there was no depth.

8 customers dropped all VMware vHosts but still spend $62K/mo on other Aptum services. They left VMware, not Aptum. The stickiness model held.

### The stickiness argument

This is worth pausing on because it directly connects to the demo and the platform thesis. The customers who stayed and grew are the ones with multi-product relationships. The ones who left had a single product and nothing tying them to us. Apt Cloud is designed to create exactly this kind of depth — when a customer provisions VMs, manages DNS, monitors costs, and views Azure resources through one portal, the switching cost goes up with every additional service they consume. The demo will show how this works in practice.

### Active migration pipeline

5 customers are mid-migration right now with substantial pending work:

- **Heilind**: $41K online + $38K pending. Upgrading ESXi 7.0 to 8.0 on new Dell 650xs. Net growth when complete.
- **Blue Yonder**: $19K online + $36K pending. Came back after going to $0 vHosts. Migrating to Pro Series 6.0/ESXi 8.0.
- **HYTECK**: $14K online + $20K pending. Including $9.2K in Google Cloud — they're going multi-cloud through Aptum. This is the Apt Cloud value prop working in practice.
- **Chicken Farmers**: $24K online + $13K pending. 3 vHosts migrating to newer hardware.
- **Netintegrity**: $13K online + $7K upgrading. ESXi 7.0 to 8.0.

Including all pending work ($117K/mo across 7 customers), the decline narrows from −30% to −18%.

### Contract expiry: the near-term pipeline

80 active ESXi hosts remain across 32 customers ($241K/mo). 41 of those services across 19 customers ($124K/mo) have 6 months or less remaining on contract. Half the active VMware base is about to come up for renewal. Each one is a migrate-or-lose decision — and these are customers who already trust us with production workloads.

### Data we should pull before the board meeting

The numbers above come from MRCTrend billing snapshots (Jan 31 2024 vs Feb 28 2026, Online services, cad_mrc). To sharpen the story further, here are SQL queries to run against the Ocean database that would give us richer detail:

**Query 1 — Renewal dates for all active ESXi services (correlated with MRC)**

This gives exact expiration dates rather than the "contract_months_remaining" estimate, so we can show which specific customers hit renewal in Q2/Q3 2026.

```sql
SELECT
    s.client_id,
    s.company_name,
    s.service_id,
    s.product,
    s.os,
    s.cad_mrc,
    s.contract_months_remaining,
    r.expiration_date,
    r.m2m,
    r.first_term
FROM [DM_BusinessInsights].[dbo].[dimServices] s
LEFT JOIN [DM_BusinessInsights].[renewals].[ocean_services_renewal_date] r
    ON s.service_id = r.service_id
WHERE s.service_status = 'Online'
    AND s.product LIKE '%vHost%'
ORDER BY r.expiration_date ASC
```

**Query 2 — Component-level breakdown of vHost services (what's actually on each host)**

This shows the hardware, RAM, CPU, storage, and add-ons attached to each ESXi service. Useful for understanding what customers are actually running and what an IaaS migration would need to replicate.

```sql
SELECT
    s.client_id,
    s.company_name,
    s.service_id,
    s.product,
    c.component_category,
    c.component_type,
    c.component,
    c.cad_component_mrc,
    c.is_online
FROM [DM_BusinessInsights].[dbo].[dimServices] s
LEFT JOIN [DM_BusinessInsights].[dbo].[dimComponents] c
    ON s.service_id = c.service_id
WHERE s.service_status = 'Online'
    AND s.product LIKE '%vHost%'
ORDER BY s.company_name, s.service_id, c.component_category
```

**Query 3 — Total customer footprint (all services, not just vHosts) for VMware customers**

This shows why multi-product customers are sticky. You can see the full service portfolio for each customer that has at least one vHost, including colo, dedicated servers, networking, etc.

```sql
SELECT
    s.client_id,
    s.company_name,
    s.product,
    s.service_type,
    s.adjusted_line_of_business,
    COUNT(*) AS service_count,
    SUM(s.cad_mrc) AS total_cad_mrc
FROM [DM_BusinessInsights].[dbo].[dimServices] s
WHERE s.service_status = 'Online'
    AND s.client_id IN (
        SELECT DISTINCT client_id
        FROM [DM_BusinessInsights].[dbo].[dimServices]
        WHERE product LIKE '%vHost%'
            AND service_status = 'Online'
    )
GROUP BY s.client_id, s.company_name, s.product, s.service_type, s.adjusted_line_of_business
ORDER BY s.company_name, total_cad_mrc DESC
```

**Query 4 — Churn detail: VMware services cancelled since Jan 2024 with cancel reason**

The Churn table has `cancel_reason` and `is_migration` fields that tell us whether departures were true churn vs. internal migrations. This helps separate "lost the customer" from "moved the workload."

```sql
SELECT
    client_id,
    client_id_company,
    service_id,
    product,
    os,
    cancel_reason,
    is_migration,
    cancel_date,
    cad_mrc,
    months_online,
    accounts_left,
    comments
FROM [DM_BusinessInsights].[dbo].[Churn]
WHERE product LIKE '%vHost%'
    AND cancel_date >= '2024-01-01'
ORDER BY cancel_date DESC
```

**Query 5 — Financial reconciliation: billed amounts vs. dimServices MRC for VMware customers**

This cross-references what dimServices says a customer's MRC is vs. what actually got billed in the most recent period. Useful for catching discrepancies before presenting to the board.

```sql
SELECT
    s.client_id,
    s.company_name,
    s.service_id,
    s.product,
    s.cad_mrc AS dimservices_mrc,
    SUM(f.xtndprce_period_nx) AS billed_amount,
    s.cad_mrc - SUM(f.xtndprce_period_nx) AS variance
FROM [DM_BusinessInsights].[dbo].[dimServices] s
LEFT JOIN [FinancialReporting].[dbo].[finance_revenue_mapping] f
    ON s.client_id = f.client_id
    AND CAST(s.service_id AS varchar) = f.service_id
    AND f.revenue_period = (
        SELECT MAX(revenue_period)
        FROM [FinancialReporting].[dbo].[finance_revenue_mapping]
        WHERE client_id = s.client_id
    )
WHERE s.service_status = 'Online'
    AND s.product LIKE '%vHost%'
GROUP BY s.client_id, s.company_name, s.service_id, s.product, s.cad_mrc
HAVING ABS(s.cad_mrc - SUM(f.xtndprce_period_nx)) > 1
ORDER BY ABS(s.cad_mrc - SUM(f.xtndprce_period_nx)) DESC
```

### Note on methodology

Source: MRCTrend billing snapshots, Jan 31 2024 vs Feb 28 2026. Online services only. All figures in CAD (cad_mrc column). 54 unique client IDs with at least one vHost service. Our Jan 2024 total ($970,763) aligns with the data team's figure ($1,006,517) within snapshot timing variance. Final numbers should be aligned with the data team before presenting.

---

## 3. What We Built and Why

### The two-layer architecture

**Apt Cloud** is the control plane — one portal, one bill, one governance model across private cloud, bare metal, and hyperscalers. Self-service provisioning, RBAC, cost visibility, activity logging, and a monetization engine with white-label capability. This is powered by CloudOps Software (formerly CloudMC) and accessed at portal.aptum.com.

**Aptum IaaS** is the infrastructure — our own compute, storage, and networking on Apache CloudStack 4.22 + KVM, running on Dell hardware in Aptum data centers. No VMware licensing overhead. 74–89% gross margins. We own, operate, and control the pricing.

### Our pricing model

Our per-core pricing on Aptum IaaS (the virtualization layer on top of the physical hardware):

- Monthly: $47.45/core
- 1-year commitment: $40.69/core
- 2-year commitment: $37.08/core
- 3-year commitment: $34.49/core

The underlying hardware is Dell servers with Intel Xeon processors ranging from 8-core Bronze/Silver (for smaller workloads) up to 48-core Platinum 8558U (for dense compute). A customer running, say, a 16-core Xeon Gold 6526Y host on a 1-year commitment pays $651/mo for the virtualization layer alone, plus storage and networking.

*[Note to self: I need to be able to explain clearly why customers need the virtualization layer — what problem it solves, why they can't just run on bare metal, and why VMware specifically became dominant. This is foundational context for the board. Worth a brief verbal explanation during the presentation, along the lines of: virtualization lets one physical server run multiple isolated workloads, which drives utilization from ~15% to 60–80%. VMware dominated because of reliability, tooling maturity, and enterprise support. The Broadcom acquisition made that dependency a liability.]*

### Why nobody else does all of this

The market breaks into three camps, and each has a gap:

**Cloud management platforms** (HPE Morpheus, CloudBolt, VMware Aria) are software only — no infrastructure. They're designed for Fortune 500 internal IT teams to govern existing environments. None support CloudStack. None are built to deliver commercial IaaS to external paying customers with white-label billing.

**Infrastructure providers** are locked to specific hypervisors and lack a self-service portal with multi-tenant billing:
- **ThinkOn** runs VMware Cloud Foundation (vCenter, Cloud Director, NSX, vSAN). They're a capable VMware shop and a partner of ours (providing VMware infrastructure for our MTC customers), but their entire stack depends on the licensing model that Broadcom just disrupted. They have no self-service portal with white-label MSP capability.
- **OVHcloud** provides commodity infrastructure but no managed services.
- **DigitalOcean** targets developers and small teams with no enterprise operations.
- **Rackspace** has managed services but has been under significant financial pressure — they completed a major debt restructuring in March 2024 to eliminate $375M in net debt and avoid default. Enterprise pricing and no meaningful Canadian presence. *(Source: [Rackspace investor relations — March 2024 refinancing](https://ir.rackspace.com/news-releases/news-release-details/rackspace-technology-announces-refinancing-transactions))*

**Hyperscalers** (Azure, AWS, GCP) have unlimited scale but no managed services for the mid-market, no Canadian sovereignty guarantees, and customers are increasingly looking to optimize their spend rather than increase their footprint.

**Where Aptum sits:** own infrastructure + self-service portal + managed operations + white-label MSP capability + hypervisor-agnostic + multi-cloud in one pane. That combination doesn't exist in the Canadian mid-market. The reason it hasn't been built before is that it requires data centers, hardware, an ops team, a software platform, and a managed services organization all in the same company.

### What's live today

- 7 signed customers (Ignite program), ~$39K MRR
- Self-service VM provisioning, RBAC, lifecycle management, real-time cost estimator
- Azure plugin live — Azure resources managed alongside CloudStack in one portal
- Cloudflare DNS integration live
- Monetization engine operational (product catalogs, pricing, credit card + tax integration)
- MTC customers accessing VMware-based private cloud through Apt Cloud (same UX, different backend)
- AWS and GCP plugins built, ready to configure

---

## 4. Live Demo — What Works Today

### DEMO

Key things to walk through:

**Apt Cloud Portal (portal.aptum.com)**

- Walk through the portal as a customer sees it
- Org hierarchy: Aptum (operator) > Reseller (e.g., ES Williams) > End customer (e.g., Fleet Stop)
- Self-service VM provisioning: pick compute, storage, network, see real-time cost estimate, deploy
- Lifecycle management: start, stop, scale, snapshot, destroy
- RBAC: different permission levels (Operator, Reseller, Admin, User, Guest)
- Activity logging: every action tracked across all services

**Aptum IaaS on CloudStack**

- Show a live customer environment
- VPC: multi-tenant shared compute with logical isolation
- Private Cloud: dedicated hosts, single-tenant
- Networking: VLANs, virtual routers, security groups

**Hyperscaler integrations**

- Azure plugin: Azure resources managed through Apt Cloud alongside CloudStack
- Cloudflare DNS: domain and DNS management through the same portal
- Point out AWS/GCP plugins are built and ready

**Monetization engine**

- Product catalogs, pricing configuration, utility pricing
- Cost visibility and usage reporting
- This is the billing backbone for both direct customers and the reseller channel

**MTC on ThinkOn — same portal, different backend**

- Show MTC customers accessing VMware-based private cloud through Apt Cloud
- This demonstrates that the platform is infrastructure-agnostic. Same UX whether the backend is CloudStack, VMware, or Azure.

**The stickiness point to make during the demo:** Every feature shown here — VMs, DNS, cost management, Azure resources, activity logs — adds another reason a customer stays. Show how a customer who started with one VM now has DNS, monitoring, and Azure resources all in the same portal. That depth of integration is what the VMware data in Section 2 proves matters.

---

## 5. Why This Is Hard to Copy

### Five things a competitor would need

**1. The integration work.** Any individual piece can be replicated — CloudStack is open-source, KVM is free, you can buy portal software, you can build a data center. Getting all of it to work together as a commercial platform with self-service provisioning, multi-tenant billing, multi-hypervisor orchestration, and hyperscaler integration is 18+ months of integration work. We're past that point with real customers on it.

**2. The operational team.** Managed services require people who know customer environments. Aptum's Service Desk and Managed Cloud teams already manage VMware, CloudStack, networking, storage, and security for production workloads. That institutional knowledge takes years to build.

**3. The existing customer base.** 42 VMware customers still billing. 41 ESXi services expiring within 6 months. These are warm leads who already trust Aptum with production workloads. A competitor starting from zero has to earn that trust first.

**4. CloudStack + Extensions Framework.** VMware-dependent providers (including ThinkOn) are structurally locked to the licensing model causing the disruption. CloudStack's Extensions Framework (4.21+) lets us orchestrate external systems — Proxmox, MAAS, Hyper-V — through the same platform. We're building on a foundation that can adapt. Competitors locked to VMware are building on the foundation causing the problem.

**5. Customer depth (the stickiness model).** When a customer's VMs, DNS, cost management, Azure resources, and billing all run through Apt Cloud, switching means rebuilding their operations. The VMware data in Section 2 shows this already works — multi-product customers survived the worst disruption in enterprise infrastructure in a decade. The platform is designed to create more of these relationships.

### The ThinkOn question

"Why isn't ThinkOn doing what we're doing?"

ThinkOn is a VMware Cloud Foundation shop. Their entire stack is VMware (vCenter, Cloud Director, NSX, vSAN). They don't need a CloudStack portal because they don't run CloudStack. They're a partner of ours, providing VMware infrastructure for MTC customers.

Could they use Apt Cloud? Architecturally yes — we have a VCD plugin. But ThinkOn has no incentive to adopt a portal from a company that is increasingly their competitor. And what ThinkOn cannot do is deliver VMware + KVM + Proxmox + bare metal + Azure + AWS through one portal with white-label MSP billing. They're a single-hypervisor shop, and Broadcom controls their cost structure.

---

## 6. Where This Goes

### Near-term: customer stickiness at scale (Q2–Q3 2026)

The highest-ROI work is deepening the product catalog so customers consume more through the portal — which is what makes them sticky. Every additional service a customer manages through Apt Cloud increases switching cost.

The catalog expansion roadmap, enabled by CloudStack 4.22's Extensions Framework:

- **Bare Metal as a Service (via MAAS)**: Customer self-provisions a dedicated physical server through the portal the same way they provision a VM. No tickets, no waiting. Aptum owns the hardware, customer gets root access on dedicated metal.
- **Proxmox VE orchestration**: For customers migrating off VMware who want an open-source hypervisor alternative. Aptum manages the Proxmox environment, customer accesses it through Apt Cloud.
- **Kubernetes service (CKS)**: Container orchestration as a self-service catalog item. Customers run K8s alongside their VMs and bare metal through the same portal.

The vision: a customer logs into Apt Cloud and sees their VMs, bare metal servers, Kubernetes clusters, Azure resources, AWS resources, and DNS — all in one place. One bill, one support team, one governance model. They can provision any of it self-service or have Aptum manage it.

### Channel as upside (Q3–Q4 2026)

Finishing reseller billing + white-label portal branding turns Apt Cloud from a product into a platform that MSPs can build practices on. ES Williams is already operating as a reseller with 5 sub-customers — the architecture works, the billing isn't white-labeled yet.

The previous CloudMC reseller product didn't gain traction when sold standalone. The difference now is that we're bundling the portal with infrastructure and managed ops — an MSP gets the platform as part of the package, not as a separate purchase. Whether this drives significant channel revenue remains to be proven, but the unit economics are attractive if it does: every MSP customer becomes an Aptum infrastructure customer without Aptum paying for acquisition.

### Scale plays (H1 2027+)

- **Multi-region**: Deploy CloudStack clusters in Herndon (US) and Portsmouth (UK). Same platform, multiple geographies. Opens US and UK regulated workloads.
- **AWS/GCP plugin activation**: Customers managing their entire multi-cloud footprint through Apt Cloud.
- **GPU/AI infrastructure**: Bare metal GPU as a service through the same portal when market demand warrants it. The MAAS extension makes this architecturally straightforward.
- **Government cloud certification**: Canadian government workloads require specific certifications. With Toronto DCs, SOC 2, and data sovereignty, this is a premium market segment.

### What this looks like at scale

Today: 7 customers, $39K MRR, one DC, direct sales only.

A reasonable mid-term model: 50 direct mid-market customers at $15K avg = $750K MRR. If the channel works and we get 10 MSP resellers each with 20 customers at $5K avg, that adds $1M MRR. Total: $1.75M MRR / $21M ARR at 74–89% gross margin ($15–19M gross profit).

The leverage comes from the platform: adding customers doesn't require proportional headcount growth because the portal handles provisioning, billing, and lifecycle management. Infrastructure margin funds platform development, the platform attracts customers, customers generate infrastructure revenue. Each cycle is cheaper than the last because the infrastructure and operational playbooks are already built.

---

## 7. Appendix: What We Need From the Board

These are investment decisions. The platform works and the market is moving.

- **Go-forward pricing**: Ignite prices ($28/vCPU, $7/GB RAM) honor legacy agreements. New customer pricing and wholesale reseller pricing need to be defined before real GTM activity. This determines market positioning.
- **Migration velocity**: 41 ESXi services across 19 customers ($124K/mo) expire within 6 months. Each is a migrate-or-lose decision. Do we invest in dedicated migration resources to capture these?
- **GTM ownership and investment**: All sales to date have been opportunistic (Ignite referrals). There is no GTM team or motion. The Strategy proposes trigger-based GTM (VMware renewal shock, cloud bill surprise, compliance events). Who owns this and what's the budget?
- **Channel investment priority**: Finishing reseller billing + white-label is what enables the MSP channel. Is the board aligned on this as a priority, given that the previous reseller product didn't gain traction?
- **Operational capacity**: Managed Cloud team is thin relative to expanding scope. Hiring ahead of demand is an investment. Hiring behind demand means dropping the ball on customers we just won.
- **Second DC timeline**: Multi-region is the scale unlock. US (Herndon) or UK (Portsmouth) first? Capital decision with long lead time.
- **ICP definition**: The Strategy proposes mid-market companies with hybrid complexity exceeding internal IT capacity. Is this the right target?

---

## Sources

| Claim | Source |
|-------|--------|
| Broadcom pricing changes (300–1,500%) | [Network World](https://www.networkworld.com/article/3994107/vmware-customers-in-europe-face-up-to-1500-price-increases-under-broadcom-ownership.html); [CIO Dive](https://www.ciodive.com/news/broadcom-vmware-vcf-adoption-second-phase/759406/) |
| Perpetual license elimination, 72-core min, bundle consolidation | [Broadcom Negotiations](https://broadcomnegotiations.com/vmware-licensing-cost-increases-under-broadcom-what-enterprises-should-expect/); [Hystax](https://hystax.com/how-vmware-prices-and-policies-changed-after-broadcoms-acquisition/); [IDC](https://www.idc.com/resource-center/blog/vmware-cost-increases-how-broadcom-vmware-product-offerings-are-evolving/) |
| 35% workload migration by 2028 | Gartner Peer Community survey |
| 56% plan to decrease VMware usage | [Foundry/CIO.com survey](https://www.ciodive.com/news/broadcom-vmware-vcf-adoption-second-phase/759406/) |
| Canadian cloud market ~$54.8B USD (2025) | [Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/canada-cloud-computing-market); [Grand View Research](https://www.grandviewresearch.com/horizon/outlook/cloud-computing-market/canada) |
| Canadian IaaS CAGR 21–23% | [KBV Research](https://www.kbvresearch.com/north-america-infrastructure-as-a-service-market/); [Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/canada-cloud-computing-market) |
| Canadian data sovereignty requirements | [Gov of Canada — Data Sovereignty White Paper](https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/cloud-services/digital-sovereignty/gc-white-paper-data-sovereignty-public-cloud.html) |
| Cloud repatriation (21% of workloads) | [Flexera State of Cloud 2025](https://www.infoworld.com/article/3842349/cloud-trends-2025-repatriation-and-sustainability-make-their-marks.html) |
| 86% of CIOs planning some repatriation | [Barclays CIO Survey via ChannelNomics](https://www.channelnomics.com/insights/breaking-down-the-83-public-cloud-repatriation-number) |
| Rackspace debt restructuring (March 2024) | [Rackspace Investor Relations](https://ir.rackspace.com/news-releases/news-release-details/rackspace-technology-announces-refinancing-transactions) |
| VMware MRC data (Aptum internal) | MRCTrend billing snapshots, Jan 31 2024 vs Feb 28 2026. Online services, cad_mrc column. |

### Claims removed from previous version

- ~~"Rackspace filed for bankruptcy"~~ — False. Rackspace restructured debt in March 2024 but did not file for bankruptcy. Corrected above.
- ~~"VMware operating margins went from 13–22% to 77%"~~ — Could not verify with a primary source. Removed.
- ~~"Forrester: VMware's largest 2,000 customers will shrink deployments by 40%"~~ — Could not locate this specific Forrester claim. Removed.
- ~~"Scale Computing: 140% increase in new customers Q1 2025"~~ — Could not verify with a primary source. Removed.
- ~~"$121.6B Canadian cloud market by 2030"~~ — The 2030 projection varies significantly by source (Mordor: $99.95B, Grand View: $152.3B). Rather than cite a specific 2030 number, the skeleton now uses the 2025 figure with CAGR range.
