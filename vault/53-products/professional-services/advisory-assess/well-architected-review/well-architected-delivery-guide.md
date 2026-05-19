# Well-Architected Review (AWS/Azure) -- Delivery Guide

> **For Aptum delivery teams.** How to execute this assessment from kickoff to findings presentation.

---

## Delivery Team Composition

| Size | Lead | Supporting Architects | Executive Sponsor | Total Aptum Hours |
|------|------|----------------------|-------------------|------------------|
| **S** | Solution Architect | None | None | 25-40 hours |
| **M** | Solution Architect | 1 (Cloud Architect) | None | 60-90 hours |
| **L** | Solution Architect | 2 (Cloud + Security Architect) | None | 120-170 hours |
| **XL** | Solution Architect | 2-3 (Cloud, Security, Infrastructure) | Yes | 200-300+ hours |

**Specialist roles**:
- **Cloud Architect**: Architecture review, service evaluation, cost optimization, reliability patterns
- **Security Architect**: Security pillar deep-dive, IAM review, encryption, compliance alignment
- **Infrastructure Architect**: Network architecture, connectivity, hybrid integration points

---

## Phase-by-Phase Delivery Plan

### Phase 1: Discovery & Scoping (Days 1-5)

**Activities**:

1. **Kickoff meeting** (1 hour)
   - Confirm scope: which accounts/subscriptions, which workloads, which pillars (S may focus on specific pillars)
   - Understand business context and drivers for the review
   - Identify stakeholders for each pillar
   - Confirm access and credentials

2. **Environment discovery**
   - Inventory all AWS accounts / Azure subscriptions in scope
   - Map organizational structure (AWS Organizations / Azure Management Groups)
   - Identify workloads and their criticality
   - Catalog cloud services in use
   - Pull billing data for cost analysis

3. **Schedule stakeholder interviews**
   - Cloud engineering team
   - Security/compliance team
   - Operations/DevOps team
   - Finance/FinOps (for cost pillar)

---

### Phase 2: Pillar-by-Pillar Assessment (Days 3-20)

For each pillar, follow the review framework below. Adjust depth based on size (S = high level or single pillar, M = standard, L/XL = deep).

#### Pillar 1: Operational Excellence

**Review areas**:
- How do you deploy and manage workloads? (IaC, manual, hybrid)
- Monitoring and alerting: CloudWatch / Azure Monitor / third-party tools
- Incident response process and escalation
- Runbooks and automation
- Change management and deployment practices
- Operational health dashboards

**Key questions for customer**:
- How do you know when something is wrong?
- What does your deployment process look like?
- How do you handle incidents?

#### Pillar 2: Security

**Review areas**:
- IAM: users, roles, policies, least privilege
- Network security: security groups, NACLs, VPC/VNET design
- Encryption: at rest (KMS/Key Vault) and in transit (TLS/SSL)
- Logging and monitoring: CloudTrail / Azure Activity Log, GuardDuty / Defender
- Secrets management: AWS Secrets Manager / Azure Key Vault
- Compliance controls relevant to the customer's industry

**Key tools**:
- AWS Security Hub / Azure Security Center / Defender for Cloud
- IAM Access Analyzer
- Config rules / Azure Policy

#### Pillar 3: Reliability

**Review areas**:
- High availability design: multi-AZ, multi-region, auto-scaling
- Backup and recovery: RTO/RPO alignment, backup testing
- Fault tolerance: single points of failure, blast radius
- Disaster recovery strategy and testing
- Service limits and quotas

**Key questions**:
- What happens if an AZ goes down?
- When did you last test recovery?
- What's your documented RTO/RPO?

#### Pillar 4: Performance Efficiency

**Review areas**:
- Compute right-sizing (instance types, utilization)
- Storage optimization (tier selection, lifecycle policies)
- Database performance (instance sizing, read replicas, caching)
- Network optimization (CDN, edge, latency)
- Architecture patterns (serverless, containers, event-driven)

**Key tools**:
- AWS Compute Optimizer / Azure Advisor
- CloudWatch metrics / Azure Monitor
- Trusted Advisor / Azure Advisor recommendations

#### Pillar 5: Cost Optimization

**Review areas**:
- Spend trends (month-over-month, year-over-year)
- Reserved Instance / Savings Plan coverage and utilization
- Unused resources (stopped instances, orphaned volumes, unused EIPs)
- Over-provisioned resources (right-sizing opportunities)
- Storage tiering opportunities
- Egress cost optimization
- Tagging strategy (cost allocation)

**Key tools**:
- AWS Cost Explorer / Azure Cost Management
- AWS Trusted Advisor / Azure Advisor
- Custom analysis of detailed billing CSV

#### Pillar 6: Sustainability

**Review areas**:
- Resource efficiency (utilization rates)
- Right-sizing impact on energy consumption
- Region selection for sustainability
- Managed services vs. self-managed (efficiency gains)
- Lifecycle policies for storage and data

---

### Phase 3: Analysis & Report Writing (Days 15-28)

**Activities**:

1. **Consolidate findings** across all pillars
2. **Classify each finding**:
   - **Severity**: High Risk / Medium Risk / Low Risk / Informational
   - **Pillar**: Which pillar it belongs to
   - **Effort to remediate**: Low / Medium / High
   - **Expected impact**: Cost savings, risk reduction, performance improvement
3. **Build remediation roadmap**:
   - **Quick wins** (0-30 days): Low effort, high impact (right-sizing, unused resources, policy fixes)
   - **Short-term** (30-90 days): Medium effort (RI purchases, architecture changes, security hardening)
   - **Medium-term** (90-180 days): Higher effort (re-architecture, multi-AZ deployment, DR implementation)
   - **Long-term** (180+ days): Transformational (governance framework, organizational changes)
4. **Write W-AR Report** using Aptum template (AWS or Azure variant)
5. **Internal review**

**Report structure** (per Aptum W-AR template):
1. Executive Summary
2. Review Scope and Methodology
3. Environment Overview
4. Pillar-by-Pillar Findings:
   - For each pillar: current state, findings, recommendations
5. Finding Summary (severity matrix / heat map)
6. Cost Optimization Opportunities (specific savings)
7. Remediation Roadmap
8. Appendices (detailed findings, service inventory)

---

### Phase 4: Findings Presentation (Final Days)

**Participants**: Aptum SA + Aptum AE + Customer cloud team + executive sponsor (L/XL)

**Presentation structure** (60-90 minutes):
1. Executive summary: overall score across pillars
2. Pillar-by-pillar highlights (top findings per pillar)
3. Critical risks that need immediate attention
4. Cost optimization opportunities (the money slide)
5. Remediation roadmap
6. Recommended next steps
7. Q&A

---

## Timeline by Size

| Phase | S (1-2 wk) | M (2-4 wk) | L (4-6 wk) | XL (6-8 wk) |
|-------|-----------|------------|------------|-------------|
| Discovery & scoping | Day 1-3 | Day 1-5 | Day 1-7 | Day 1-10 |
| Pillar assessment | Day 2-7 | Day 3-15 | Day 5-25 | Day 7-35 |
| Analysis & report | Day 5-9 | Day 12-20 | Day 20-32 | Day 28-42 |
| Findings presentation | Day 9-10 | Day 20-22 | Day 32-35 | Day 42-48 |

---

## Tools & Access Required

| Tool | Purpose | Required For |
|------|---------|-------------|
| AWS Console / Azure Portal (read-only) | Architecture review | All |
| AWS Cost Explorer / Azure Cost Management | Cost analysis | All |
| AWS Trusted Advisor / Azure Advisor | Best practice recommendations | All |
| AWS Security Hub / Azure Defender | Security assessment | M+ |
| AWS Config / Azure Policy | Compliance and governance review | M+ |
| IAM Access Analyzer | IAM review | M+ |
| CloudWatch / Azure Monitor | Performance and operational review | M+ |
| AWS Well-Architected Tool (optional) | Structured questionnaire | M+ |
| Aptum W-AR Report Template (AWS or Azure) | Report generation | All |

---

## Quality Checkpoints

| Checkpoint | When | Who Reviews |
|-----------|------|------------|
| Environment access confirmed | Day 2-3 | SA confirms all access working |
| Pillar assessments complete | End of Phase 2 | SA + Cloud Architect peer review |
| Cost analysis complete | Mid Phase 3 | SA + Cloud Architect validation |
| Report draft | End of Phase 3 | SA + Aptum cloud team |
| Findings presentation rehearsal | Day before Phase 4 | SA + Aptum AE alignment |

---

## Risk & Escalation

| Risk | Mitigation |
|------|-----------|
| Customer can't provide required cloud access | Assessment cannot proceed without access. Escalate to Aptum AE. |
| Environment too complex for chosen size | Flag early. Recommend scope increase or size bump. |
| Critical security finding during review | Immediate notification to customer security team. |
| Customer has multiple accounts with no organizational structure | Treat as a finding. Review scope may need to focus on critical accounts. |
| Findings overlap with other assessments (Hybrid Cloud, Security Posture) | Note cross-references. Recommend complementary assessments where appropriate. |

---

*Last updated: 2026-02-06*
