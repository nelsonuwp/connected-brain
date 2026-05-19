# Operational Maturity Assessment -- Delivery Guide

> **For Aptum delivery teams.** How to execute this assessment from kickoff to findings presentation.

---

## Delivery Team Composition

| Size | Lead | Supporting Architects | Executive Sponsor | Total Aptum Hours |
|------|------|----------------------|-------------------|------------------|
| **S** | Solution Architect | None | None | 20-30 hours |
| **M** | Solution Architect | 1 (Infrastructure or Operations specialist) | None | 50-70 hours |
| **L** | Solution Architect | 2 (Infrastructure + Operations) | None | 100-140 hours |
| **XL** | Solution Architect | 2-3 specialists | Yes | 170-250+ hours |

---

## Phase-by-Phase Delivery Plan

### Phase 1: Kickoff & Data Collection (Days 1-3)

**Activities**:

1. **Kickoff meeting** (1 hour)
   - Confirm scope and objectives
   - Understand the business context (growth plans, budget pressure, strategic priorities)
   - Map the IT team structure and roles
   - Identify data sources (ticketing system, monitoring tools, documentation)

2. **Data collection request**:
   - Ticketing/incident data export (last 6-12 months)
   - Monitoring tool access or dashboards
   - Existing operational documentation (runbooks, procedures, escalation lists)
   - IT team roster with roles and responsibilities
   - IT operational budget (if available)
   - Any existing SLA documentation

3. **Schedule individual interviews** with each IT team member (30-60 min each)

---

### Phase 2: Operational Model Assessment (Days 3-10)

**Activities**:

#### Individual Interviews
Interview each IT team member separately (critical -- management perspective alone is not sufficient):
- What does your typical day look like?
- How much time do you spend on reactive work vs. planned work?
- What wakes you up at night (literally)?
- What tools do you use? What's missing?
- What processes are documented? What's in your head?
- What would you improve if you had time?
- What are the biggest risks you see?

#### Operational Domain Review
Assess maturity across each domain (score 1-5):

| Domain | What to Assess |
|--------|---------------|
| **Monitoring** | What's monitored? Alerting thresholds? Coverage gaps? |
| **Incident Management** | Process? Escalation? MTTR? Communication? |
| **Patching & Updates** | Frequency? Coverage? Testing? Scheduling? |
| **Backup & Recovery** | Backup frequency? Testing? RTO/RPO? |
| **Change Management** | Process? Approval? Testing? Rollback? |
| **Capacity Management** | Planning? Forecasting? Right-sizing? |
| **Security Operations** | Vulnerability management? Access control? |
| **Documentation** | Runbooks? Architecture diagrams? Knowledge base? |

#### Incident Pattern Analysis (M+)
From ticketing/incident data:
- Volume trends (increasing, decreasing, seasonal?)
- Categories (hardware, software, network, user error)
- MTTR (mean time to resolve) by category
- Repeat incidents (same issue recurring)
- After-hours incidents (burden on team)
- SLA compliance (if SLAs exist)

---

### Phase 3: Cost & Staffing Analysis (Days 8-14)

**Activities**:

#### Current State TCO
Calculate the true cost of the current self-managed model:
- **Staff costs**: Salary + benefits for IT team members allocated to infrastructure ops (use time allocation from interviews)
- **Tool costs**: Monitoring, ticketing, backup, security tools
- **Overhead**: Training, recruitment, turnover costs
- **Opportunity cost**: Time spent on ops vs. strategic projects (quantify in dollars)
- **Risk cost**: Estimated cost of unplanned downtime based on incident history
- **Total**: Annual cost of running infrastructure operations in-house

#### Managed Services TCO
Calculate what the same scope would cost under Aptum managed services:
- **Managed Cloud / OS & Above**: Monthly managed services fees
- **Tool consolidation**: Savings from standardized tooling (LogicMonitor, etc.)
- **Staff reallocation**: Value of IT team time freed up for strategic work
- **Risk reduction**: Reduced downtime, proactive management, 24/7 coverage
- **Total**: Annual cost under managed model

#### Gap Analysis
- What are they paying for vs. what they're getting?
- What is the team not doing that they should be? (deferred maintenance, missed patches, no DR testing)
- What's the true cost of "we'll get to it when we have time"?

---

### Phase 4: Recommendations & Roadmap (Days 12-18)

**Activities**:

1. **Compile findings** into assessment report
2. **Build recommendation**:
   - Which operational domains should be managed (by Aptum)
   - Which should remain in-house (customer's core competency)
   - Phased transition approach
3. **Create transition roadmap**:
   - Phase 1: Quick wins (monitoring setup, critical patching) -- Month 1
   - Phase 2: Core managed services (OS management, backup, incident response) -- Months 2-3
   - Phase 3: Full operational handoff (all domains transitioned) -- Months 3-6
   - Phase 4: Optimization and continuous improvement -- Ongoing
4. **Prepare presentation**

**Report structure**:
1. Executive Summary
2. Current Operational Model Overview
3. Operational Maturity Scoring (by domain)
4. Incident Analysis & Trends
5. Staffing & Cost Analysis
6. TCO Comparison: Self-Managed vs. Managed
7. Risk Assessment
8. Recommendations
9. Transition Roadmap
10. Appendices

---

### Phase 5: Findings Presentation (Final Days)

**Participants**: Aptum SA + Aptum AE + Customer management + IT team

**Presentation structure** (45-60 minutes):
1. "Here's what your team is doing today" (operational model overview)
2. "Here's what it costs" (TCO breakdown -- often an eye-opener)
3. "Here's what's at risk" (deferred maintenance, single-person dependencies, unmonitored systems)
4. "Here's the alternative" (managed services model with cost comparison)
5. "Here's how to get there" (transition roadmap)
6. Q&A

**Key tip**: Be sensitive. This assessment is about the operational model, NOT about criticizing the team. Frame findings as "the model is unsustainable" not "the team is failing." The team is usually doing their best with too few resources.

---

## Timeline by Size

| Phase | S (1 wk) | M (2 wk) | L (3-4 wk) | XL (4-6 wk) |
|-------|---------|---------|-----------|------------|
| Kickoff & data collection | Day 1-2 | Day 1-3 | Day 1-5 | Day 1-7 |
| Operational assessment | Day 2-4 | Day 3-8 | Day 3-15 | Day 5-20 |
| Cost & staffing analysis | Day 3-4 | Day 8-11 | Day 10-18 | Day 15-28 |
| Recommendations & roadmap | Day 4-5 | Day 11-13 | Day 16-22 | Day 25-35 |
| Findings presentation | Day 5 | Day 13-14 | Day 22-25 | Day 35-40 |

---

## Tools & Access Required

| Tool | Purpose | Required For |
|------|---------|-------------|
| Ticketing system (Jira, ServiceNow, etc.) | Incident analysis | M+ |
| Monitoring platform (if exists) | Operational coverage assessment | All |
| LogicMonitor (Aptum) | Reference for managed services comparison | All |
| Interview notes template | Structured team interviews | All |
| TCO model spreadsheet | Cost comparison | All |

---

## Quality Checkpoints

| Checkpoint | When | Who Reviews |
|-----------|------|------------|
| All interviews completed | End of Phase 2 | SA confirms coverage |
| Operational maturity scores | Mid Phase 2 | SA + specialist review |
| TCO model draft | End of Phase 3 | SA + Aptum delivery lead |
| Report draft | End of Phase 4 | SA + Aptum managed services team |
| Presentation prep | Day before Phase 5 | SA + Aptum AE alignment |

---

## Risk & Escalation

| Risk | Mitigation |
|------|-----------|
| IT team feels threatened by the assessment | Emphasize: this is about the model, not the people. Their expertise is valued; the goal is to free them from operational burden. |
| Customer won't share financial data (salaries, budgets) | Use industry benchmarks and estimates. Note assumptions in report. |
| No ticketing/incident data available | Rely on interviews and observational assessment. Note the gap itself as a finding. |
| Management and team have different perspectives | Interview both. Present both views in findings. |

---

*Last updated: 2026-02-06*
