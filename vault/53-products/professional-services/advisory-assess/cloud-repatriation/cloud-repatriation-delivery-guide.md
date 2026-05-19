# Cloud Repatriation Assessment -- Delivery Guide

> **For Aptum delivery teams.** How to execute this assessment from kickoff to findings presentation.

---

## Delivery Team Composition

| Size | Lead | Supporting Architects | Executive Sponsor | Total Aptum Hours |
|------|------|----------------------|-------------------|------------------|
| **S** | Solution Architect | None | None | 20-30 hours |
| **M** | Solution Architect | 1 (Cloud Architect) | None | 50-80 hours |
| **L** | Solution Architect | 2 (Cloud + Infrastructure Architect) | None | 110-160 hours |
| **XL** | Solution Architect | 2-3 (Cloud, Infrastructure, Network) | Yes | 200-300+ hours |

**Specialist roles**:
- **Cloud Architect**: Cloud spend analysis, service-by-service portability assessment, cloud-native alternatives
- **Infrastructure Architect**: Target infrastructure design, hardware sizing, colo/private cloud architecture
- **Network Architect**: Connectivity design for hybrid state, latency analysis, bandwidth requirements

---

## Phase-by-Phase Delivery Plan

### Phase 1: Discovery & Alignment (Days 1-5)

**Activities**:

1. **Kickoff meeting** (1 hour)
   - Confirm scope: which cloud accounts, which workloads, which scenarios to model
   - Understand business drivers (cost reduction target, contract renewal timing, board pressure)
   - Identify stakeholders for interviews (engineering, ops, finance)
   - Confirm data access

2. **Cloud billing data access**
   - AWS: Cost Explorer, Billing Dashboard, Reserved Instance reports
   - Azure: Cost Management, Advisor recommendations, Reserved Instance reports
   - GCP: Billing Console, Recommender
   - Export detailed billing CSV for analysis (minimum 3 months, ideally 12 months)

3. **Stakeholder interviews**
   - Engineering: Which workloads are critical? What are the dependencies? What would break if we moved things?
   - Operations: How are things managed today? What tooling is in place? What's the operational model?
   - Finance: What's the budget pressure? What's the target savings? When is the contract renewal?

---

### Phase 2: Cloud Spend Analysis (Days 3-10)

**Activities**:

#### Spend Breakdown
- Total monthly/annual spend by provider
- Spend by service type (compute, storage, database, networking, other)
- Spend by region
- Spend trend over last 6-12 months (is it growing? stable? seasonal?)
- Reserved Instances / Savings Plans utilization and waste
- Egress costs (often a hidden driver)

#### Cost Attribution
- Map spend to workloads/applications where possible
- Identify the top 10 cost drivers
- Flag anomalies or unexpected spend

#### Quick Win Identification
- Unused resources (stopped instances still billing, orphaned volumes)
- Over-provisioned resources (running large instances at low utilization)
- Missed reservation opportunities
- These are "free savings" that can be recommended immediately

**Tools**:
- AWS Cost Explorer / Azure Cost Management / GCP Billing
- CloudHealth, Spot.io, or equivalent (if customer has)
- Custom analysis spreadsheets

---

### Phase 3: Workload Analysis & Portability Assessment (Days 8-18)

**Activities**:

#### Workload Profiling
For each in-scope workload:
- **Resource consumption**: CPU, memory, storage, network
- **Usage pattern**: Steady/predictable vs. bursty/elastic
- **Cloud services used**: Generic (VMs, block storage) vs. proprietary (RDS, Lambda, DynamoDB, etc.)
- **Data characteristics**: Volume, residency requirements, integration points
- **Dependencies**: What does it talk to? What talks to it?

#### Portability Scoring
Rate each workload on portability:
- **Highly portable**: Running on generic compute/storage (VMs, containers), standard databases (PostgreSQL, MySQL). Easy to move.
- **Moderately portable**: Using some managed services that have open-source equivalents. Requires some refactoring.
- **Low portability**: Deeply integrated with proprietary cloud services (Lambda, DynamoDB, Cosmos DB, Cloud Functions). Significant effort to move.
- **Not recommended**: Cloud-native workloads where the cloud service IS the value (e.g., ML training on cloud GPUs, CDN, global load balancing).

#### Repatriation Candidacy
For each workload, recommend:
- **Repatriate**: Steady, predictable, portable, cost savings are clear
- **Optimize in cloud**: Bursty, elastic, or proprietary -- optimize rather than move
- **Evaluate further**: Borderline cases that need more analysis
- **Keep in cloud**: Cloud-native value proposition outweighs cost

---

### Phase 4: TCO Modeling (Days 12-22)

**Activities**:

#### Build Scenarios
1. **Status quo**: What does staying in cloud cost over 3 years (include growth)?
2. **Selective repatriation**: Move top repatriation candidates to private infrastructure. Keep the rest in cloud.
3. **Aggressive repatriation**: Move everything portable. Only keep cloud-native workloads.
4. **Hybrid optimized**: Right-place every workload (may be same as #2 with more nuance).

#### For Each Scenario, Calculate:
- **Compute costs**: VMs/instances or bare metal
- **Storage costs**: Block, object, file storage
- **Network costs**: Bandwidth, egress, cross-connects
- **Software licensing**: OS, databases, middleware
- **Management costs**: Staff time or managed services fees
- **Migration costs** (one-time): Planning, execution, testing, cutover
- **Facility costs** (if applicable): Colo space, power, cooling
- **Risk costs**: Downtime risk during migration, staff ramp-up

#### Financial Summary
- Annual cost comparison across scenarios
- 3-year TCO comparison
- Migration investment vs. annual savings = payback period
- Sensitivity analysis: what if growth is faster/slower? What if cloud prices change?

---

### Phase 5: Target Architecture & Roadmap (Days 18-28)

**Activities**:

1. **Design target architecture** for repatriated workloads
   - Aptum Managed CloudStack / Private Cloud as the landing zone
   - Connectivity between cloud (remaining workloads) and private infrastructure
   - Consider: compute, storage, networking, monitoring, backup, DR

2. **Define migration approach** per workload
   - Lift-and-shift (for VMs)
   - Re-platform (for managed services with open-source equivalents)
   - Phased cutover vs. big-bang
   - Testing and validation approach

3. **Create phased roadmap**
   - Phase 1: Quick wins (right-sizing, RI optimization) -- immediate
   - Phase 2: Easy repatriations (portable VMs, standard databases) -- 1-3 months
   - Phase 3: Complex moves (services with dependencies, data migrations) -- 3-6 months
   - Phase 4: Optimization (fine-tuning, decommissioning cloud resources) -- ongoing

4. **Write the report and prepare presentation**

---

### Phase 6: Findings Presentation (Final Days)

**Presentation structure** (60-90 minutes):
1. Cloud spend overview: "Here's what you're spending and where it's going"
2. The savings opportunity: "Here's what you could save" (the money slide)
3. Workload-by-workload recommendation: stay, move, or optimize
4. TCO comparison across scenarios (visual: bar chart or table)
5. Recommended target architecture
6. Phased roadmap with timeline and milestones
7. Recommended next steps: repatriation execution project

**Key presentation tip**: Lead with the financial story. The CFO/CIO cares about the number. The engineering team cares about the "how." Present to both in the room.

---

## Timeline by Size

| Phase | S (1 wk) | M (2-3 wk) | L (3-5 wk) | XL (6-8 wk) |
|-------|---------|-----------|-----------|------------|
| Discovery & alignment | Day 1-2 | Day 1-4 | Day 1-5 | Day 1-7 |
| Cloud spend analysis | Day 2-4 | Day 3-8 | Day 3-12 | Day 5-15 |
| Workload analysis | Day 3-5 | Day 6-12 | Day 8-18 | Day 10-25 |
| TCO modeling | Day 4-5 | Day 10-15 | Day 12-22 | Day 18-32 |
| Target architecture & roadmap | -- | Day 13-17 | Day 18-28 | Day 25-40 |
| Findings presentation | Day 5 | Day 17-19 | Day 28-32 | Day 40-45 |

---

## Tools & Access Required

| Tool | Purpose | Required For |
|------|---------|-------------|
| AWS Cost Explorer / Azure Cost Management | Spend analysis | All (per provider) |
| Cloud billing CSV export | Detailed cost analysis | All |
| AWS Pricing Calculator / Azure TCO Calculator | Scenario modeling | All |
| Custom TCO model (Aptum spreadsheet) | Multi-scenario comparison | All |
| Cloud console (read-only) | Resource inventory | M+ |
| CloudHealth / Spot.io (if available) | Advanced cost analytics | M+ (optional) |
| Diagramming tool | Architecture diagrams | M+ |

---

## Quality Checkpoints

| Checkpoint | When | Who Reviews |
|-----------|------|------------|
| Cloud billing data received | Day 3-5 | SA confirms completeness |
| Spend analysis complete | End of Phase 2 | SA + Cloud Architect review |
| Workload portability matrix | End of Phase 3 | SA + Cloud Architect |
| TCO model draft | Mid Phase 4 | SA + Aptum delivery lead |
| Target architecture | End of Phase 5 | SA + Infrastructure Architect |
| Report draft | Before presentation | SA + Aptum leadership (XL) |

---

## Risk & Escalation

| Risk | Mitigation |
|------|-----------|
| Customer can't provide cloud billing data | Assessment cannot proceed without billing data. Escalate to Aptum AE. |
| Cloud spend is too low to justify repatriation | Honest finding. Present as "optimize in cloud" rather than repatriate. The assessment still has value. |
| Customer has no landing zone for repatriated workloads | Include Aptum infrastructure (Managed CloudStack, colo) in the target architecture. This is actually an upsell opportunity. |
| Contract penalties for early cloud exit | Include contract penalties in TCO model. Model the break-even point. |
| Engineering team resistant to repatriation | Address in stakeholder interviews. Provide evidence from peer companies. Frame as hybrid, not anti-cloud. |

---

*Last updated: 2026-02-06*
