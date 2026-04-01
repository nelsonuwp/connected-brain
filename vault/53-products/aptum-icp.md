# Aptum Ideal Customer Profile
## Single Unified ICP, Grounded in Portfolio Data
**Version 1.0 | April 1, 2026**

---

## Why a Single ICP

Marc Pare's Product Strategy v1.3.1 defined two ICPs: one for infrastructure buyers and one for digital natives with 7+ developers. The board directed the team to consolidate to a single ICP. Ian Rae put it simply in the March 31 product discussion: "We're a mid-market company selling to mid-market."

This document defines one Ideal Customer Profile. It also defines what an ideal customer is not, using real portfolio data to show where the current customer base aligns and where it diverges. The goal is to give the commercial team a clear target for new logo acquisition, and to give operations a framework for honest conversations about existing customers who don't fit.

---

## The Ideal Customer

### Company Profile

The ideal Aptum customer is a mid-market organization, typically between 50 and 2,000 employees, generating $10M to $500M in annual revenue. They are digitally dependent (their revenue flows through technology) but technology is not their core business. They are running a mix of workloads across on-premises infrastructure and at least one hyperscaler, and they are feeling the pain of managing that complexity.

They are most commonly found in these verticals: SaaS/digital platforms, eCommerce, financial services, healthcare/life sciences, professional services, and media/content delivery. They are headquartered in or have meaningful operations in North America (Canada and US East Coast especially), with secondary presence in the UK.

### Firmographic Anchors

| Attribute | Ideal Range | Why |
|---|---|---|
| Employee count | 50 to 2,000 | Large enough to have real infrastructure needs, small enough that their IT team (2 to 15 people) needs a partner |
| Annual revenue | $10M to $500M | Budget exists for managed services, but they aren't large enough to build everything internally |
| IT team size | 2 to 15 people | This is the sweet spot. Overwhelmed, stretched thin, doing too many things. They need a safety net. |
| Infrastructure spend | $10K to $100K/mo MRC | Below $10K the economics don't work for managed services stacking. Above $100K they typically have in-house capability. |
| Cloud maturity | Hybrid (on-prem + at least one hyperscaler) | Pure cloud-native companies won't need Aptum's infrastructure. Pure on-prem companies aren't ready for the conversation. |

### Behavioral Indicators

The ideal customer exhibits these patterns:

They have workloads they cannot or will not move to a hyperscaler. This could be for cost reasons (they've done the math and repatriation makes sense), regulatory reasons (data sovereignty, compliance requirements), performance reasons (latency-sensitive applications), or inertia reasons (legacy applications that would cost more to re-architect than to host).

They are running a VMware estate and feeling Broadcom's licensing pressure. The 300 to 1,050% price increases validated by Gartner are real, and these customers are actively looking for alternatives. Aptum's CloudStack and Proxmox options are directly relevant.

They consume multiple product types. The portfolio data is clear on this: multi-product customers generate 94.46% of Aptum's revenue while representing 63.9% of the customer base. The average multi-LOB customer generates 2.8x the revenue of a single-LOB customer and churns at a materially lower rate.

They value the relationship over the commodity. They want a partner who understands their environment, not just a provider who racks a server. The consulting engagement is the start of the relationship, not the end of it.

### The Buyer

The primary buyer is the VP of IT, Director of Infrastructure, or CTO. In smaller organizations, this might be the sole IT leader reporting to a CFO or COO. They are not a developer (although their teams include developers). They are an infrastructure and operations person who is being asked to do more with less.

The secondary influencer is the CFO or finance leader. Aptum's single-bill, single-portal value proposition resonates here because it simplifies vendor management and provides cost visibility.

### What the Ideal Customer Buys

The ideal customer engages across the full stack. They start with an infrastructure commodity (VPC, Private Cloud, or Dedicated Server) and layer managed services on top:

| Layer | What They Buy | Monthly Value |
|---|---|---|
| Infrastructure commodity | VPC, Private Cloud, or Dedicated + Azure/AWS through Apt Cloud | $7,000 to $25,000 |
| Layer 2: Managed OS | Patching, Veeam backup, managed firewall, endpoint security | +$2,000 to $5,000 |
| Layer 3: App Platform | Datadog APM, WAF, DDoS, load balancing | +$3,000 to $8,000 |
| Layer 4: Security | Alert Logic MDR, compliance reporting, vulnerability scanning | +$2,000 to $5,000 |
| Layer 5: Business Continuity | DRaaS, hybrid interconnects, M365 managed services | +$1,500 to $5,000 |

A fully stacked ideal customer generates $15,000 to $48,000/mo in MRC. The blended margin is 50 to 60%, compared to 70 to 80% for infrastructure-only, but the absolute margin dollars are 2 to 3x higher and the customer is deeply embedded.

---

## Where We Are Now: The Portfolio Reality

The dimServices extract (April 1, 2026) tells an honest story about the current customer base.

### Portfolio Summary

| Metric | Value |
|---|---|
| Total monthly revenue (USD MRC) | $2,888,901 |
| Total services | 5,581 |
| Unique customers | 773 |
| Datacenters | 26 across 21 cities |

### Revenue Composition

| Line of Business | USD MRC | Share |
|---|---|---|
| Hosting | $2,171,402 | 75.16% |
| Colocation | $642,193 | 22.23% |
| Cloud Services | $74,168 | 2.57% |
| Professional Services | $1,138 | 0.04% |

Three quarters of revenue comes from hosting, which is predominantly commodity dedicated servers. Cloud services represent just 2.57% of the portfolio. This is the gap the product strategy needs to close.

### Customer Concentration

| Segment | Revenue | Share |
|---|---|---|
| Top 10 customers | $1,229,170 | 42.55% |
| Top 20 customers | $1,500,979 | 51.96% |
| Top 50 customers | $1,913,545 | 66.24% |
| Single largest customer (Basis Global Technologies) | $425,740 | 14.74% |

This concentration is a structural risk. One customer walking would remove nearly 15% of total MRC.

### Managed Services Penetration

Only 6.5% of services have any managed service attached. This compares to an industry norm of 15 to 20% for MSPs in the mid-market. The managed services revenue is approximately $187,639/mo out of $2.89M total. The stacking opportunity is massive and largely untapped.

### Customer Segmentation by Stickiness

| Segment | Customers | Revenue | Share | Churn Risk |
|---|---|---|---|---|
| Multi-LOB (hosting + colo + cloud) | 135 | $1,810,044 | 62.66% | Low |
| Hosting-only | 429 | $659,075 | 22.81% | High |
| Colocation-only | 93 | $401,994 | 13.92% | Medium |
| Cloud-only | ~116 | $17,788 | 0.62% | Medium |

The 135 multi-LOB customers are the closest to the ideal ICP. They buy across product lines, generate 62.66% of revenue, and have multiple integration points that make switching costly.

The 429 hosting-only customers represent the honest conversation the team needs to have. Many of these are legacy Peer One customers who have stayed because inertia is cheaper than migration. They are paying for commodity infrastructure without managed services layered on top. They are price-sensitive and will leave when they find something cheaper.

### The Honest Assessment: Customers Who Don't Fit the ICP

The portfolio includes a meaningful number of customers who do not fit the ideal profile. This is not a judgment on those customers. It is a recognition that chasing retention on commodity-only accounts is a different motion than building deep managed services relationships.

Examples of customers who sit outside the ICP:

| Customer | MRC | Profile | Why They Don't Fit |
|---|---|---|---|
| Basis Global Technologies | $425,740 | Single product (dedicated hosting), no managed services | Largest single customer by far, but zero stickiness. If they find dedicated hosting cheaper elsewhere, there is nothing binding them. |
| ResearchGATE GmbH | $226,038 | Single product (dedicated hosting), no managed services | Same pattern. High revenue, low integration, high flight risk. |

There are 320 legacy-only customers generating $1,279,974/mo (44.31% of the portfolio) with zero managed services attached. This revenue is structurally at risk.

The response is not to abandon these customers. It is to:

1. Pursue managed services upsell aggressively on the accounts that have the profile to become ideal customers (overwhelmed IT teams, hybrid workloads, compliance needs).
2. Accept that some portion of this base will attrit over time as they find commodity infrastructure cheaper elsewhere.
3. Build the new logo pipeline against the ICP so that as legacy accounts attrit, they are backfilled with customers who fit the profile and buy across the stack.

This is what "it wasn't meant to be forever" looks like operationally.

---

## Geographic Focus

### Where the Revenue Is Today

| City | Services | USD MRC | Share |
|---|---|---|---|
| Toronto | 1,040 | $601,775 | 20.83% |
| Herndon (IAD2) | 1,307 | $592,257 | 20.50% |
| Portsmouth | 927 | $547,787 | 18.96% |
| Miami | 547 | $300,870 | 10.41% |
| Los Angeles | 529 | $300,823 | 10.41% |
| Atlanta | 554 | $279,354 | 9.67% |
| London | 109 | $69,572 | 2.41% |
| Vancouver | 88 | $49,076 | 1.70% |

The top three cities represent 60.29% of revenue. Toronto and Herndon/Virginia are the strongest bases. Portsmouth has capacity but the facility has a known end-of-life constraint (the building owner plans to redevelop). Miami has recently been extended and is the strongest candidate for regional growth, particularly for the Latitude.sh and Megaport partnership that Marc Pare outlined.

### Where to Hunt

For new logo acquisition against the ICP:

| Region | Rationale |
|---|---|
| Greater Toronto / Southern Ontario | Largest existing base, Canadian data sovereignty, proximity to Pullman DC (Apt Cloud/IaaS primary site) |
| US East Coast (Virginia, Atlanta, Miami) | Existing DC presence, large mid-market population, Miami specifically for LatAm-adjacent demand |
| UK (Portsmouth + London) | Existing customer base, but constrained by facility situation. Selective. |

For MSP/reseller channel (secondary):

| Region | Rationale |
|---|---|
| Regional MSPs in DC footprint cities | MSPs squeezed by Broadcom who need a private cloud partner. ES Williams/Ignite pattern validates this. |
| LatAm-adjacent via Miami | Latitude.sh + Megaport intersection, as discussed in product discussion |

---

## Contract Risk Context

The portfolio has a near-term contract renewal concentration that requires attention:

| Contract Window | Services | Revenue | Share |
|---|---|---|---|
| Expiring within 6 months | 4,340 | $2,101,324 | 72.74% |
| Expiring 6 to 12 months | 151 | $135,147 | 4.68% |
| Expiring 12 to 24 months | 348 | $259,615 | 8.99% |
| 24+ months remaining | 735 | $382,521 | 13.24% |

72.74% of revenue by value is within 6 months of contract expiration. This is the window during which every renewal conversation should include a managed services stacking conversation. Each renewal is an opportunity to move a customer closer to (or further from) the ICP.

---

## Market Tailwinds Supporting This ICP

Several market forces are pulling mid-market companies toward exactly the profile described above:

The Broadcom/VMware disruption is real and ongoing. Gartner estimates 35% of VMware workloads will migrate by 2028. Forrester projects VMware's largest 2,000 customers will shrink deployments by 40%. These organizations need somewhere to go, and Aptum's CloudStack and Proxmox alternatives, delivered through Apt Cloud with managed services layered on top, are a direct answer.

Cloud repatriation is accelerating. Andreessen Horowitz's "Cost of Cloud" research and the 37signals case study ($7M savings over 5 years from their cloud exit) have given mid-market CFOs permission to question their hyperscaler bills. 21% of surveyed organizations have repatriated workloads. Aptum's ability to provide private cloud with a public-cloud-like portal experience (through Apt Cloud) positions it as the repatriation destination.

The Canadian cloud market is growing at 17.3% CAGR, reaching an estimated $121.6B by 2030. Canadian data sovereignty requirements continue to tighten. Aptum's Toronto DC presence and Canadian identity are meaningful differentiators.

The global managed services market is projected at $400B by 2025, growing at 10 to 15% CAGR. The specific segment Aptum operates in (hybrid cloud managed services for mid-market) is growing faster than the market average.

---

## Using This ICP

### For Sales (New Logo)

The ideal first conversation is a consulting or assessment engagement. This is the tip of the spear, as Marc Pare described it. It builds trust, maps the customer's environment, and creates the technical intimacy that leads to infrastructure and managed services revenue. It is the start of the relationship, not the end.

Qualification questions for new opportunities:

1. How many people are on your IT team? (Target: 2 to 15)
2. Where are your workloads running today? (Target: hybrid, on-prem + at least one hyperscaler)
3. Are you running VMware? When is your next renewal? (Broadcom pressure = urgency)
4. Who manages your backups, patching, and security monitoring today? (If "we do, barely," they fit the ICP)
5. Do you have compliance requirements? (SOC 2, PCI, HIPAA = Layer 4 opportunity)

### For Account Management (Existing Base)

Use the managed services stacking model to score existing customers against the ICP. The 135 multi-LOB customers are the immediate upsell targets. The 429 hosting-only customers should be triaged: which ones have the profile to become ICP-fit (overwhelmed IT teams, hybrid workloads) and which ones are pure commodity buyers who will eventually attrit?

### For Product and Engineering

Everything that makes Apt Cloud more visible to the customer (monitoring dashboards, backup status, patch compliance, ticket integration) deepens the managed services relationship and increases switching cost. Portal visibility for Layers 1 and 2 is the highest-impact work for customer retention.

---

## What This ICP Excludes (And Why That's OK)

Large enterprises with 10,000+ employees and IT departments 3x the size of Aptum. They will engage for consulting but will not sustainably buy managed services from a company Aptum's size. Ian Rae was direct about this: "That's not gonna happen."

Pure commodity buyers looking for the cheapest dedicated server. The portfolio has many of these. They generate revenue today but will leave when they find cheaper. The backfill strategy is to replace them with ICP-fit customers over time.

Hyperscaler-native companies with no on-premises footprint. If all their workloads are in AWS/Azure/GCP and they have no interest in private infrastructure, Aptum's core differentiation (hybrid cloud, infrastructure + managed services stacking) doesn't apply.

Very small businesses below $5K/mo MRC potential. The economics of managed services delivery don't support full stacking at this scale.

---

*Sources: dimServices extract (April 1, 2026), Product Strategy v1.3.1 (Confluence), Product Discussion transcript (March 31, 2026), AptCloud/Aptum IaaS Strategy v1.2, Managed Services Catalog, Service Team descriptions.*
