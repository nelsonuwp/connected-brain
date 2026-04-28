# Strategy Review: Ian Transition Materials + Dave Feedback
## Differing opinions and proposed changes to the 53-products ICP and Strategy
**Date: April 28, 2026**

---

## Purpose

Review the materials Ian flagged as "important" in his transition document, plus Dave's email feedback on the strategy draft, and identify where they suggest changes to the current `aptum-product-strategy.md` and `aptum-icp.md`. No edits made yet. Treat this as input for the joint workshop Dave proposed (Sarah, Adam, Dave, Marc-Alex, Will).

---

## Sources reviewed

Strategy-relevant only, per the filter on this review.

| Source | Last touched | Relevance |
|---|---|---|
| Ian's Transition document 1.1 (DRAFT) | Apr 27, 2026 | Index of authoritative materials Ian wants the next leader anchored on |
| Aptum Identity & Values (Confluence, Marketing space) | Jul 28, 2025 | Vision, mission, values, brand promises, strategic focus |
| Aptum Messaging (Confluence, Marketing space) | Mar 7, 2025 | Why/How/What positioning, story, short and long-form messaging |
| Product Workshop Final Draft (PPTX, Marc Pare's drive) | Jul 2, 2024 | Board-level product strategy review including ICP, "Drawn and Quartered" framework, "Spear(s) lead to Cake" |
| Product Strategy v1.3.1 (Confluence, Product space) | Apr 7, 2025 | Two-ICP version that the board has since collapsed; still the live page |
| CloudOps SW Product Strategy 1.0 (Confluence, Product space) | Apr 20, 2026 | CloudMC/CloudOps positioning as B2B2B for service providers |
| Cloud Platform Revenue & Growth Strategy (Confluence, CLP space) | Dec 2, 2024 | Win-with-partners objectives (Expedient, ThinkOn, Hypertec) |
| Managed Cloud Platform - Private/Hybrid/Public (Confluence, Product) | Nov 13, 2024 | Reminds that Managed Cloud Platform was designed to support all clouds including private |

Skipped per scope: shared services (finance, HR, legal), governance, banking authorities, customer relationship handoffs, cadences, individual partner onboarding details. The transition doc treats these as operational items rather than strategy items.

---

## Headline takeaway

The current 53-products v2.0 documents are stronger than what they replace on financial honesty, motion clarity, and assessment-led pipeline mechanics. They are weaker than the source materials on three things: (1) the brand promise of "your cloud, your way," (2) the breadth of the cloud-agnostic story including Networking and Edge, and (3) how the software platform itself is a differentiator, not just a delivery channel. Dave's email lands directly on (2) and (3).

The biggest single tension is between the brand promise that customers can "grow on your own terms... maintained with or without us" and the strategy's thesis that managed services stickiness is where the margin lives. This is reconcilable but the current draft does not reconcile it. It needs to.

---

## Proposed changes, organized by theme

### 1. Reconcile the brand promise with the operate-is-the-margin thesis

The Identity page commits Aptum to three brand promises, with the third being "Your cloud, your way: Tech-agnostic guidance so your cloud fits you. Plus full visibility, control, and the freedom to self-serve or call us in. Your tools, your pace, your rules, we're here when you need." The Messaging page reinforces this: "Our solutions are designed to be maintained with or without us, so you can grow on your own terms."

The current strategy says the opposite, repeatedly. "Every advisory engagement and every execution project should have a clear line of sight to an operate outcome. If the answer to 'where does this lead in terms of recurring managed services?' is 'nowhere,' the engagement does not align with the strategy." Operate "is what makes the customer sticky." The portal visibility roadmap is explicitly framed as "increases switching cost."

A reader of both documents would conclude either that the brand promise is marketing fiction or that the strategy is fighting the brand. Both readings damage credibility.

The reconciliation that exists in the older Product Strategy v1.3.1 is the **Build, Operate, Transfer (BOT)** model: Aptum builds and operates an environment, then transfers it back to the customer with documentation, automation, and training, with optional Augmented Support. BOT is mentioned nowhere in the current 53-products strategy.

**Proposed change to `aptum-product-strategy.md`:** Either add BOT as an explicit fourth motion or articulate that the Operate motion includes a Transfer option for customers who want optionality. Either way, name the brand promise tension and resolve it. The lever that makes this work commercially is that customers who choose Transfer typically buy Augmented Support, which is recurring but lighter than full managed services. The strategy currently has no place for this.

### 2. Elevate cloud agnosticism from a feature to the headline

This is the same point Dave makes (see Section 9 below for the Dave-specific framing). The Identity brand promise #1 reads "The right workload on the right platform: Ensuring the right balance of on-prem, private, public **and edge cloud**, built to fit your business need, not the other way round." The Messaging page says "We take an agnostic approach, balancing on-prem, private, public, and edge cloud solutions to match the right workloads with the right platforms."

The current strategy mentions cloud agnosticism only obliquely: "Apt Cloud manages both Aptum IaaS and Azure/AWS/GCP" and "Single portal for private + public cloud." It is not a top-line organizing principle. It also drops "edge" entirely.

This understates the differentiation that Dave, the Identity page, and the June 2024 deck all claim. The June 2024 "Drawn and Quartered" framing is more aligned with the brand: Right Platform / Right Expertise / Right Way, all anchored on agnostic delivery.

**Proposed change to both docs:** Move "truly cloud agnostic" into the Position section of the strategy and into the differentiation language of the ICP. It is structurally different from competitors (who pick a hyperscaler or pick VMware) and the brand has been making this promise for over a year. The strategy should match.

### 3. The software platform is a differentiator, not just a control plane

The current strategy treats Apt Cloud as the customer-facing layer that delivers the managed services experience. That is true but understates what CloudMC/CloudOps actually is. The CloudOps SW Product Strategy 1.0 positions it as a **B2B2B SaaS platform** that lets a service provider connect, integrate, define, price, and monetize disparate cloud services into a cohesive menu for their distinct markets. It is in production with Akamai, ThinkOn, ShapeBlue, and others. The Apache CloudStack community is recommending it.

In other words, the software is not just Aptum's portal. It is a product line. The current strategy mentions this only as the "MSP/Reseller Channel" engine and treats it as nascent ("ES Williams... already being explored as an early reseller model beta customer"). That is wrong. CloudMC has been operating as a B2B2B product for years, with paying anchor tenants.

**Proposed change to `aptum-product-strategy.md`:** Either add a third revenue pillar (Software, sold to service providers) or explicitly carve "Service Provider Channel" out of Engine 3 as a more mature, distinct revenue motion than the strategy currently implies. The downstream consequence is that the ICP also needs to acknowledge this segment, which it currently does not (see Section 7).

### 4. Networking deserves first-class treatment, or an explicit decision not to

The June 2024 deck is explicit: "Networking becomes a first-class citizen of the hybrid cloud." Cloud Networking & Security is its own product line in the channel route table. The Megaport/Latitude.sh play in Miami in Ian's transition doc is fundamentally a networking partnership (public cloud gateway services, hybrid connectivity).

The current strategy treats Networking as a layer in the managed services stack (L1 monitoring, L5 hybrid interconnects). It is not absent, but it is not elevated. Given the Megaport partnership opportunity and the "multi-cloud networking growing at 23% CAGR" data point in Product Strategy v1.3.1, this might be a deliberate de-prioritization or it might be an oversight.

**Proposed change:** Either elevate Cloud Networking & Security as a third pillar or as an explicit cross-cutting capability, or add Networking to the "What We Stop Doing" list (i.e., we will only do networking as a service component of managed cloud, not as a standalone offer). Currently it is in neither place, which leaves the field confused about whether Megaport-style plays are strategic or tactical.

### 5. Edge and AI infrastructure are missing entirely

The Identity brand promise mentions edge. Product Strategy v1.3.1 dedicates significant space to edge ("Edging out bets... addressing the multiple sides of the edge market along with the hybrid multi-cloud") and to AI/GPU/LLM trends. Ian's transition doc flags 5C.ai (AI private clouds) as the "next thrust for our infrastructure offerings to provide relevant solutions in the fast growing market for AI platforms" and notes this was supposed to be on the DBRG strategy offsite.

The current 53-products strategy says nothing about edge or AI workloads. The MAAS section is the closest thing to an AI-adjacent capability and it is framed around Broadcom displacement rather than AI.

**Proposed change to `aptum-product-strategy.md`:** Either add Edge and AI Infrastructure as Phase 3 roadmap items with deliberate scoping, or add them to "What We Stop Doing" with a stated reason. Silence is the worst option because it leaves the door open for ad-hoc opportunism (Cirion, 5C.ai, Megaport) that does not roll up to anything.

### 6. The ThinkOn dependency is invisible in the current taxonomy

The Strategy's three-delivery-model taxonomy (VPC / Dedicated Cloud / Private Cloud) is clean, but it omits the partnership reality. The June 2024 deck is explicit: "Managed VMware Private Cloud is delivered via our partner ThinkOn." Ian's transition doc reinforces this: ThinkOn provides the post-Broadcom VMware license path and has been used to "re-platform negative margin customers from MTC."

The current strategy's "Private Cloud (VMware/Proxmox, not necessarily through Apt Cloud)" line conceals that the VMware delivery model is partner-led, not Aptum-built. That matters for capacity planning, margin modeling, and how Sales positions the offering. It also affects whether VMware Private Cloud is reliably available (depends on the ThinkOn relationship) versus structurally Aptum's.

**Proposed change to `aptum-product-strategy.md`:** Add a sentence to the Private Cloud row in the delivery model table: "Delivered in partnership with ThinkOn (white-label) for VMware; Proxmox is Aptum-delivered." Add a corresponding open item: "ThinkOn relationship status and commercial terms" alongside the other open items.

### 7. The single-ICP creates a B2B2B blind spot

Ian directed the collapse from two ICPs to one ("we're a mid-market company selling to mid-market"). The current ICP doc honors that. But CloudMC's customer base, by design and by the CloudOps SW Product Strategy, is service providers, not end customers. ES Williams via Ignite is one example. ThinkOn, Akamai, and the ShapeBlue/CloudStack community are others.

The ICP's "What This ICP Excludes" section addresses MSPs only as an exception ("MSP/reseller customers who aggregate many small businesses into a single Aptum relationship (the ES Williams/Ignite model)"). That is not enough. The Service Provider segment has its own buyer (the service provider's own product or commercial leadership), its own qualification criteria (multi-cloud workload, monetization needs, distinct end customers), and its own revenue model.

**Proposed change to `aptum-icp.md`:** Add a short "Service Provider Channel" section that defines the secondary ICP for B2B2B sales, ideally pulling from the CloudMC ICP definition (100-1000 employees, $10M-$500M revenue, MSPs/CSPs/telcos with VMware Cloud Director or Apache CloudStack tech stacks). Frame it as a channel ICP rather than a primary ICP, but make it visible. The current doc reads as if Aptum sells only to end customers, which is not accurate.

### 8. The vision and mission are not echoed anywhere in the strategy

The Identity page Vision is "A future where businesses have the freedom to innovate, grow, thrive, and **own their destiny in the cloud**." The Mission is "Help you run your cloud, your way." These are good. They do not appear anywhere in the current strategy doc, which opens with "Aptum is a hybrid cloud managed services provider" and proceeds to financial breakdowns.

This is the easiest gap to close and probably should be closed. The Position section of `aptum-product-strategy.md` should connect the operating thesis back to the brand language. The current opening is correct but unmoored from the rest of the company's stated identity. Marketing has been telling customers "freedom to own your cloud destiny" for over a year. The product strategy should at least acknowledge the same vocabulary.

**Proposed change:** Add a Vision/Mission anchor at the top of `aptum-product-strategy.md` that ties the operating model to the Identity page language. Then the rest of the doc reads as the operating realization of the brand, not as a separate document that lives next to it.

### 9. Kubernetes and DevOps depth is buried

This is partly Dave's point (#3 in his email), partly an emergent observation from the June 2024 deck and the Cloud Platform v1.3.1 doc. K8s, DevOps, GitOps, FinOps, observability, CI/CD, and platform engineering were the top of the spear in the original Cloud Platforms positioning. AKS/EKS workshops, Octopus Deploy, KubeCost, CAST.ai are all named partners. AWS DevOps and EKS Service Delivery competencies are on the AWS roadmap.

The current strategy mentions Kubernetes briefly in Platform Modernization assessment and L3 App Platform. The AWS competencies do not appear at all. The CloudOps team's distinct expertise (acquired with the CloudOps acquisition) is not called out as a moat.

**Proposed change:** In `aptum-product-strategy.md`, the differentiation section under Pillar 1 should explicitly list the technical depth (multi-hyperscaler MSP competencies, Kubernetes/DevOps platform engineering, CloudStack expertise via the CloudOps team) as the credibility layer that lets Aptum sell managed services upmarket. Without this, the strategy reads as "we have software and we have ops people" without the specific expertise that makes Pillar 1 defensible.

### 10. Geographic and partner footprint reads thinner than reality

The ICP names "Greater Toronto / Southern Ontario, US East Coast (Virginia, Atlanta, Miami), UK (Portsmouth + London)." That is correct as a customer footprint. The partner footprint is materially larger and is not represented: ThinkOn (Canada), eStruxture (Canada), Megaport/Latitude (Miami/LATAM), Akamai (global), Apache CloudStack/ShapeBlue (UK/global), Pax8 (US/global). Cirion (LATAM) is in active conversation per the transition doc.

This is not a critique of the geographic prioritization in the ICP. It is an observation that the partner ecosystem is the GTM mechanism in several of these regions, and the strategy should make that explicit in Engine 3 or as a separate "Partner Ecosystem" section.

**Proposed change to `aptum-product-strategy.md`:** Add a brief Partner Ecosystem section under Engine 3 that names the key partners and the role each plays (white-label private cloud, channel marketplace, infrastructure capacity, hyperscaler relationships). The current Engine 3 reads as if the channel is aspirational; the partner relationships in Ian's transition doc say it is already operational, just not formalized.

### 11. Stop-doing list could be tightened

The current list is good. Two adjustments worth considering:

- "We stop reselling Azure at a loss" should be "We stop reselling hyperscaler subscriptions at a loss." The same pathology exists in AWS and GCP. Ian quoted it as Azure because that was the dominant case, but the principle is broader.
- "We stop building service guides around vendor names" is correct as a principle but the Identity brand promise commits to "tech-agnostic guidance," which means Aptum should not just hide the vendor name on the SKU but actually be willing to recommend the right vendor for the customer's situation. This implies that Service Guides should describe outcomes, AND the underlying advisory motion should be willing to recommend non-Aptum-stack solutions when appropriate. The current strategy is silent on whether Aptum's advisors will tell a customer "the answer for you is to stay on AWS, here's how to optimize." That is the brand-promise behavior. Worth deciding explicitly whether it is the strategy behavior.

---

## Dave's email feedback: what's Dave-specific

Dave's email contained four substantive points and a process ask. Here is how I would tag each.

### Dave-specific (not echoed strongly in the source materials)

- **Workshop with Sarah, Adam, Dave, Marc-Alex, Will.** This is Dave's own ask to align before the messaging cascades. Worth scheduling regardless of whether his other points land.
- **The framing "we cover all of the compute bases except customer premise" with BMaaS included.** This is a Dave-specific synthesis. The source docs touch on BMaaS (June 2024 deck mentions bare-metal cloud; current strategy has the "MAAS Differentiator" section in Phase 2) but no source document frames it as Dave does, with BMaaS completing the compute-coverage taxonomy. If accepted, this changes the strategy's MAAS section from "future market differentiator" to "current pillar of the agnostic story."
- **"The Software is proprietary and unique (assuming we can get it quickly brought up to speed on the API front)."** Dave is the only voice making the API-readiness conditional explicit. The source materials assume CloudMC's APIs are sufficient. The current strategy has it as Open Item #5 ("Portal integration engineering effort is unknown. 15+ integration points identified... with no LOE estimates from Will's team"). Dave is right that the differentiation claim depends on closing this gap, which makes API roadmap a strategic risk, not just an engineering item.

### Corroborated by the source materials (Dave is restating something the brand and earlier strategy already say)

- **"Aptum is truly cloud agnostic."** This matches the Identity brand promise #1 and #3, the Messaging page's "agnostic approach," and the June 2024 deck's "Drawn and Quartered" framing. Dave is pulling a thread that is already present in the brand voice but is missing from the current strategy. See Section 2 above.
- **"The software platform... can and should be able to provide visibility, and management services on top of any of these clouds."** This matches the CloudOps SW Product Strategy 1.0 framing and the Managed Cloud Platform Confluence page ("Managed Cloud Platform was designed to be able to support all clouds including private"). Dave is restating CloudMC's design intent. See Section 3 above.
- **"Expertise and certification depth in all of these areas, and people who know this space. Including the Kubernetes and DEVOPS space which is somewhat unique."** This matches the Cloud Platform v1.3.1 positioning and the AWS competencies list in the June 2024 deck. The depth claim is real. See Section 9 above.
- **"Clean ICE (Ideal Customer Engagement) path from Advisory to Execution to management."** This matches the current strategy's three-motion model. Dave is endorsing it.

### How to use Dave's feedback

The Dave-specific items (BMaaS-as-current-pillar, API-readiness as strategic risk) are net-new and warrant addition to the strategy. The corroborated items are not new individually, but the **pattern** Dave is naming is real: the strategy under-tells the agnostic-software-expertise story that the brand has been telling for over a year. That pattern is worth fixing systematically (Sections 2, 3, 9 above) rather than as a one-off response to Dave.

---

## Where the current 53-products docs are stronger than the source materials

Worth saying explicitly so that any revision does not dilute the gains.

- **Single ICP, anchored in dimServices data.** Product Strategy v1.3.1 had two ICPs and a lot of qualitative aspiration. The current ICP doc has one, with portfolio data showing where the customer base aligns and diverges. This is a real improvement. Ian directed the collapse and the current doc honored it.
- **The Three Motions formalized with handoffs.** Product Strategy v1.3.1 mentioned BOT and "tip of the spear" but did not specify motion handoffs, t-shirt sizing, success metrics, or revenue ranges. The current strategy does. This is the most operationally useful addition.
- **The Seven Assessments framework with revenue projections.** None of the source docs has this. It is the mechanism that converts the vague "advisory motion" into a sales play.
- **Honest portfolio diagnosis.** "75% hosting, 6.5% managed services penetration, 72.74% of revenue expiring within 6 months." The June 2024 deck shows aspiration. The current strategy shows the gap. This is more useful for prioritization.
- **Stop-doing list with attribution.** Quoting Marc Pare ("french fries, not the hamburger") and Ian ("get out of the mindset of reselling Azure at a loss") makes the strategy harder to drift from. Worth keeping.

---

## Recommended next steps

1. Schedule Dave's proposed workshop (Sarah, Adam, Dave, Marc-Alex, Will). Use this review as the pre-read. The decisions that need agreement are: (a) Sections 1 and 2 above (brand reconciliation and agnosticism elevation) for messaging consistency, (b) Section 3 (software as a pillar), (c) Section 5 (edge/AI in or out of scope), and (d) Section 7 (B2B2B segment in the ICP).
2. Before that workshop, get a position from Will on Section 3's API-readiness gap. Dave's challenge is conditional on this. The answer changes whether the software differentiation is a current claim or a 2027 claim.
3. Get a position from Marc-Alex on Section 6 (ThinkOn dependency). If the ThinkOn relationship is renewing, the strategy should name it. If it is uncertain, the strategy should hedge.
4. Once those positions are in, the proposed changes can be drafted as a v2.1 of `aptum-product-strategy.md` and `aptum-icp.md`. Most of these are additions and reframings rather than rewrites.

---

## Open questions surfaced by this review

These are not differing opinions, just things the source documents do not resolve and the current strategy also does not resolve.

- Is the Service Provider channel a primary GTM motion or a tertiary one? The CloudOps SW Strategy treats it as primary. The current 53-products strategy treats it as Engine 3 of 4. The actual revenue mix would tell us which is correct.
- Is BOT (Build-Operate-Transfer) still a real offer, or has it quietly been retired in favor of the assessment framework? Product Strategy v1.3.1 features it. June 2024 deck features it. Current strategy is silent.
- The Identity Mission says "Help you run your cloud, your way." The current strategy says "every engagement should funnel to managed services." If a customer says "we want to run our own cloud, just help us set it up," what does Aptum do? Today the strategy says decline the engagement. The brand says embrace it. The board has not made this call explicit and probably should.
