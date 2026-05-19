# Hybrid Cloud Assessment -- Delivery Guide

> **For Aptum delivery teams.** How to execute this assessment from kickoff to findings presentation.

---

## Delivery Team Composition

| Size | Lead | Supporting Architects | Executive Sponsor | Total Aptum Hours |
| --- | --- | --- | --- | --- |
| **S** | Solution Architect | None | None | 25-40 hours |
| **M** | Solution Architect | 1 (Cloud or Infrastructure Architect) | None | 60-90 hours |
| **L** | Solution Architect | 2 (Cloud + Network or Security) | None | 120-170 hours |
| **XL** | Solution Architect | 2-3 (Cloud, Network, Security) | Yes | 200-300+ hours |

**Specialist architect roles**:

- **Cloud Architect**: Cloud environment analysis, TCO modeling, migration path design
- **Network Architect**: Connectivity design, hybrid networking, latency analysis
- **Security Architect**: Compliance review, data residency analysis, security architecture
- **Infrastructure Architect**: On-prem/colo environment assessment, capacity planning

---

## Phase-by-Phase Delivery Plan

### Phase 1: Discovery & Alignment (Days 1-5)

**Participants**: Aptum SA + Aptum AE + Customer stakeholders (IT, Engineering, Finance, Compliance)

**Activities**:

1. **Kickoff meeting** (1 hour)
   - Confirm scope, objectives, and success criteria
   - Review timeline and milestones
   - Identify all stakeholder groups for interviews
   - Confirm data access requirements
1. **Discovery workshop** (S: 1 hour, M: half day, L: 1-2 days, XL: 2-3 days)
   - Define business goals and constraints
   - Map organizational priorities (cost, performance, compliance, agility)
   - Identify critical applications and their business importance
   - Understand current pain points and desired future state
   - Identify compliance and regulatory requirements
1. **Data collection request**:
   - Application/service inventory (or start building one)
   - Current architecture diagrams
   - Cloud billing data (AWS Cost Explorer, Azure Cost Management)
   - On-prem infrastructure inventory (from Infra Risk if already done)
   - Existing SLAs and performance requirements
   - Compliance documentation

**Workshop facilitation tips**:

- Use a whiteboard/virtual board to map applications visually
- For each application, capture: name, function, current hosting, criticality, data sensitivity, usage pattern (steady vs. bursty)
- Don't try to be exhaustive in the workshop -- aim for the 80% picture. Fill gaps in interviews.

---

### Phase 2: Infrastructure & Workload Analysis (Days 5-15)

**Activities**:

#### Workload Inventory & Profiling

For each in-scope workload, document:

- **What it is**: Application name, function, technology stack
- **Where it runs**: Current environment (on-prem, colo, AWS, Azure, etc.)
- **How it behaves**: Usage pattern (steady, bursty, seasonal), resource consumption
- **What it depends on**: Dependencies (databases, APIs, other apps)
- **How critical it is**: Business criticality (Tier 1/2/3)
- **What data it handles**: Data classification, residency requirements
- **How portable it is**: Proprietary dependencies, lock-in factors

#### Environment Analysis

- Inventory current infrastructure across all environments
- Assess current utilization and capacity
- Review cloud spend by service, region, and workload
- Identify over-provisioned and under-utilized resources

#### Suitability Assessment

For each workload, evaluate fit across environments:

- **Public cloud**: Best for bursty, elastic, experiment-heavy workloads
- **Private cloud / Managed CloudStack**: Best for steady, predictable, compliance-sensitive workloads
- **On-prem / Dedicated hosting**: Best for high-performance, data-intensive, low-latency workloads
- **Hybrid**: Split architecture (e.g., frontend in cloud, database on-prem)

**Suitability scoring criteria**:

- Performance requirements (latency, throughput)
- Cost optimization (steady workloads cheaper on-prem/private cloud)
- Compliance and data residency
- Elasticity requirements
- Portability (lock-in risk)
- Operational complexity

---

### Phase 3: TCO & Suitability Modeling (Days 10-20)

**Activities**:

#### Build TCO Models

For each scenario, calculate total 3-year cost including:

- Compute (VMs, containers, bare metal)
- Storage (block, object, file)
- Networking (bandwidth, cross-connects, egress)
- Software licensing (OS, databases, middleware)
- Management and operations (staff time, managed services)
- Migration costs (one-time)
- Facilities (power, space, cooling)

#### Define Scenarios

Typical scenarios to model:

1. **Status quo**: Stay where you are. What does it cost over 3 years?
1. **Cloud-first**: Move everything to public cloud. What does it cost?
1. **Hybrid optimized**: Place each workload in its best-fit environment. What does it cost?
1. **Repatriation** (if applicable): Bring cloud workloads back on-prem/private. What does it cost?

#### Financial Analysis

- Cost comparison across scenarios (bar charts, tables)
- Break-even analysis for migration investments
- Sensitivity analysis for key variables (growth rate, cloud pricing changes)

**Tools**:

- AWS Pricing Calculator / Azure TCO Calculator
- Custom TCO spreadsheet model (Aptum standard template)
- Cloud billing analysis tools (CloudHealth, Spot.io, or manual analysis)

---

### Phase 4: Architecture & Compliance Review (Days 15-22, L/XL)

**Activities** (M gets basic version, L/XL get full review):

#### Architecture Review

- Evaluate current architecture against best practices
- Identify single points of failure and resilience gaps
- Review network topology and connectivity between environments
- Assess disaster recovery and backup posture

#### Compliance Review

- Map data residency requirements to hosting locations
- Identify compliance gaps against relevant frameworks
- Review access controls and data protection measures
- Flag regulatory risks in proposed scenarios

---

### Phase 5: Target Architecture & Roadmap (Days 18-28)

**Activities**:

1. **Design target architecture**: Based on workload suitability analysis and TCO modeling, define the recommended future state
1. **Define migration/optimization path**: Which workloads move where, in what order
1. **Create phased roadmap**:
   - Phase 1: Quick wins (cost savings, easy migrations)
   - Phase 2: Strategic moves (major workload relocations)
   - Phase 3: Optimization (fine-tuning, governance implementation)
1. **Estimate effort and timeline** for each phase
1. **Write the report and prepare presentation**

---

### Phase 6: Findings Presentation (Final Days)

**Participants**: Aptum SA + Aptum AE + Customer stakeholders (executive sponsor for L/XL)

**Presentation structure** (60-90 minutes):

1. Executive summary: "Here's where you are, here's where you should be, here's how to get there"
1. Current state overview with key findings
1. TCO comparison across scenarios (the money slide)
1. Recommended target architecture
1. Phased roadmap with timeline and milestones
1. Recommended next steps (follow-on services)
1. Q&A

---

## Timeline by Size

| Phase | S (1-2 wk) | M (2-4 wk) | L (4-6 wk) | XL (6-8 wk) |
| --- | --- | --- | --- | --- |
| Discovery & alignment | Day 1-2 | Day 1-4 | Day 1-7 | Day 1-10 |
| Workload analysis | Day 2-5 | Day 4-10 | Day 5-18 | Day 7-25 |
| TCO modeling | Day 3-6 | Day 8-14 | Day 12-22 | Day 18-32 |
| Architecture review | -- | Day 10-14 | Day 15-25 | Day 22-38 |
| Roadmap & report | Day 5-8 | Day 14-18 | Day 22-30 | Day 32-42 |
| Findings presentation | Day 8-10 | Day 18-20 | Day 28-32 | Day 40-45 |

---

## Tools & Access Required

| Tool | Purpose | Required For |
| --- | --- | --- |
| AWS Cost Explorer / Azure Cost Management | Cloud spend analysis | All (if customer has cloud) |
| AWS Pricing Calculator / Azure TCO Calculator | Scenario cost modeling | All |
| Custom TCO model (spreadsheet) | Multi-environment cost comparison | All |
| LogicMonitor / monitoring tools | Utilization and performance data | M+ |
| Network scanning tools | Environment discovery | M+ (if no inventory) |
| Diagramming tool (Lucidchart, draw.io) | Architecture diagrams | M+ |
| Presentation tool | Executive presentation | L/XL |

---

## Quality Checkpoints

| Checkpoint | When | Who Reviews |
| --- | --- | --- |
| Workload inventory complete | End of Phase 2 | SA confirms with customer POC |
| TCO model draft | Mid Phase 3 | SA + Cloud Architect peer review |
| Architecture recommendation | End of Phase 4 | SA + specialist review |
| Report draft | End of Phase 5 | SA + Aptum delivery lead |
| Executive presentation rehearsal | Day before Phase 6 | SA + Aptum AE alignment |

---

## Risk & Escalation

| Risk | Mitigation |
| --- | --- |
| Customer can't provide cloud billing data | Use public pricing calculators + customer estimates. Note assumptions in report. |
| Workload count significantly exceeds estimate | Flag to Aptum AE. May require scope change / size adjustment. |
| Customer has no application inventory | Build one during discovery (adds effort to Phase 1-2). |
| Multiple teams with conflicting priorities | SA facilitates alignment; escalate to customer executive sponsor if needed. |
| Compliance requirements discovered mid-assessment | May require specialist architect addition or scope bump. Flag early. |

---

*Last updated: 2026-02-06*
