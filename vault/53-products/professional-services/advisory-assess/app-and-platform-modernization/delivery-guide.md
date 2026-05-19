# App & Platform Modernization Assessment -- Delivery Guide

> **For Aptum delivery teams.** How to execute this assessment from kickoff to findings presentation.

---

## Delivery Team Composition

| Size | Lead | Supporting Architects | Executive Sponsor | Total Aptum Hours |
| --- | --- | --- | --- | --- |
| **S** | Solution Architect | None | None | 20-30 hours |
| **M** | Solution Architect | 1 (DevOps/Platform Engineer) | None | 50-80 hours |
| **L** | Solution Architect | 2 (DevOps/Platform + Cloud Architect) | None | 110-160 hours |
| **XL** | Solution Architect | 2-3 (DevOps, Cloud, Infrastructure) | Yes | 200-300+ hours |

**Specialist roles**:

- **DevOps/Platform Engineer**: CI/CD pipeline review, container orchestration assessment, deployment practices
- **Cloud Architect**: Cloud-native architecture, managed services evaluation, infrastructure design
- **Infrastructure Architect**: Platform hosting, compute/storage sizing, networking

---

## Phase-by-Phase Delivery Plan

### Phase 1: Discovery & Architecture Review (Days 1-7)

**Activities**:

1. **Kickoff meeting** (1 hour)
   - Confirm scope: which applications, which teams, what's the modernization goal
   - Understand business drivers (speed to market, reliability, scale, cost)
   - Map the current technology stack and tooling
   - Identify stakeholders for interviews
1. **Architecture discovery**
   - Review existing architecture diagrams and documentation
   - Map application architecture: monolith vs. microservices vs. hybrid
   - Identify technology stack per application (languages, frameworks, databases, messaging)
   - Map dependencies between applications and external services
   - Understand data flows and integration points
1. **Team interviews** (1 hour each)
   - Dev team lead: architecture decisions, pain points, ambitions
   - DevOps/platform engineer (if exists): current tooling, deployment process, operational challenges
   - Infra/ops team: hosting environment, capacity, monitoring

---

### Phase 2: CI/CD & Deployment Assessment (Days 5-12)

**Activities**:

#### CI/CD Maturity Evaluation

Assess across dimensions:

| Dimension | Level 1 (Manual) | Level 2 (Basic) | Level 3 (Automated) | Level 4 (Optimized) |
| --- | --- | --- | --- | --- |
| Source control | Ad hoc | Central repo | Branching strategy | Trunk-based with feature flags |
| Build | Manual | Scheduled | Automated on commit | Parallel, cached, \< 10 min |
| Test | Manual/none | Some unit tests | Automated test suite | Full pyramid (unit, integration, e2e) |
| Deploy | Manual (SSH, FTP) | Scripted | Automated pipeline | Blue/green, canary, progressive |
| Environments | Prod only | Dev + Prod | Dev + Staging + Prod | Ephemeral environments per PR |
| Monitoring | None / reactive | Basic uptime | APM + logging | Observability (traces, metrics, logs) |
| Rollback | Manual, painful | Scripted | Automated | Instant, automated on failure |

#### Deployment Process Walkthrough

- Walk through a real deployment end-to-end
- Document the current process step by step
- Identify bottlenecks, manual steps, and failure points
- Measure deployment frequency, lead time, failure rate, recovery time (DORA metrics where possible)

---

### Phase 3: Container & Platform Assessment (Days 8-18)

**Activities**:

#### Container Readiness (per application)

- Can it run in a container? What changes are needed?
- Dependencies: OS-level, file system, networking
- State management: stateless vs. stateful
- Configuration: environment variables vs. hardcoded
- Logging: stdout/stderr vs. file-based
- Health checks: does it expose liveness/readiness?

#### Kubernetes Readiness (if K8s is in use or planned)

- Current K8s architecture (if exists): cluster topology, namespaces, resource management
- Helm charts / manifests: quality, consistency, best practices
- GitOps readiness (ArgoCD, Flux, etc.)
- Monitoring and observability: Prometheus, Grafana, etc.
- Security: RBAC, network policies, secrets management
- If not yet on K8s: readiness assessment for adoption

#### Platform Architecture

- Hosting: where do workloads run? (bare metal, VMs, cloud, managed K8s)
- Networking: service mesh, ingress, DNS
- Storage: persistent storage strategy
- Security: container scanning, runtime security
- Developer experience: how easy is it for devs to work with the platform?

---

### Phase 4: Recommendations & Roadmap (Days 15-25)

**Activities**:

1. **Technology stack recommendations**
   - Container runtime and orchestration (Docker, Kubernetes, managed K8s)
   - CI/CD tooling (GitHub Actions, GitLab CI, ArgoCD, etc.)
   - Observability stack (Prometheus, Grafana, Loki, Jaeger)
   - Platform hosting (Aptum Managed CloudStack, cloud-managed K8s, hybrid)
1. **Modernization roadmap** (phased):
   - **Phase 1** (1-3 months): Quick wins -- CI/CD improvements, basic containerization, monitoring setup
   - **Phase 2** (3-6 months): Core modernization -- container migration for top workloads, platform setup
   - **Phase 3** (6-12 months): Full platform -- all workloads on platform, GitOps, full observability
   - **Phase 4** (ongoing): Optimization -- developer experience, advanced patterns, self-service
1. **Write report and prepare presentation**

**Report structure**:

1. Executive Summary
1. Current Architecture Overview
1. CI/CD Maturity Assessment (with scores)
1. Container/Platform Readiness
1. Technology Stack Evaluation
1. Gap Analysis & Opportunities
1. Modernization Roadmap
1. Cost & Effort Estimates
1. Appendices

---

### Phase 5: Findings Presentation (Final Days)

**Presentation structure** (45-90 minutes):

1. Current state: "Here's your architecture and delivery pipeline today"
1. Maturity assessment: "Here's where you are on the maturity curve"
1. Key gaps and opportunities
1. Recommended platform architecture
1. Modernization roadmap (phased)
1. Recommended next steps (implementation engagement)

**Key tip**: Frame this in business terms -- deployment speed, reliability, developer productivity -- not just technology.

---

## Timeline by Size

| Phase | S (1 wk) | M (2-3 wk) | L (3-5 wk) | XL (6-8 wk) |
| --- | --- | --- | --- | --- |
| Discovery & architecture | Day 1-3 | Day 1-5 | Day 1-8 | Day 1-12 |
| CI/CD assessment | Day 2-4 | Day 5-10 | Day 5-14 | Day 8-20 |
| Container/platform assessment | Day 3-5 | Day 8-14 | Day 10-22 | Day 14-30 |
| Recommendations & roadmap | Day 4-5 | Day 12-17 | Day 18-28 | Day 25-40 |
| Findings presentation | Day 5 | Day 17-19 | Day 28-32 | Day 40-45 |

---

## Tools & Access Required

| Tool | Purpose | Required For |
| --- | --- | --- |
| Git repositories (read-only) | Architecture and code review | All |
| CI/CD platform access | Pipeline review | M+ |
| Container registries (if used) | Image analysis | M+ (if containerized) |
| K8s cluster access (read-only) | Platform assessment | M+ (if K8s in use) |
| Monitoring tools | Observability review | M+ |
| Diagramming tool | Architecture diagrams | All |

---

## Risk & Escalation

| Risk | Mitigation |
| --- | --- |
| Dev team resistant to assessment ("outsiders reviewing our work") | Frame as "learning from patterns across hundreds of orgs, not judging your work." Focus on enablement. |
| No documentation exists | Treat as a finding. Build understanding through interviews and code review. |
| Application architecture too complex for chosen size | Flag early. May need scope adjustment or size bump. |
| Customer expects implementation as part of assessment | Set clear expectations at kickoff. Assessment delivers the plan; implementation is Phase 2. |

---

*Last updated: 2026-02-06*
