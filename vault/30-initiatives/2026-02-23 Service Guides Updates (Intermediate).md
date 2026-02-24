---
type: initiative
status: drafting
---

# Service Guides Updates (Intermediate)

## One-Line Purpose
Capture a baseline, machine-readable representation of our current service landscape as declared by each service owner.

## Context
We currently lack a unified view of our service network, making cross-service discussions subjective and fragmented. This initiative creates normalized Markdown artifacts for each service that capture declared current state—responsibilities, dependencies, and boundaries—without attempting to reconcile conflicts or enforce alignment. These pre-contract artifacts will surface inconsistencies and seed future OSOM-compliant service contracts.

## Success Looks Like
1. Eight Markdown service guides exist in `vault/50-services`, one for each service area
2. Each guide contains at minimum: service name, owner, one-paragraph purpose, declared responsibilities, and declared dependencies (upstream and downstream)
3. All guides follow a consistent structure that enables side-by-side comparison
4. Conflicting or overlapping definitions across services are explicitly visible in the documentation
5. Service owners can identify their service's declared state without external interpretation

## Constraints
- This phase captures only; it does not reconcile conflicting definitions
- Service boundaries and ownership disputes are documented as-is, not resolved
- No finalized service contracts will be produced
- No governance, lifecycle enforcement, or evolution paths will be defined
- Security & Compliance is explicitly out of scope for this phase
- OSOM structure is referenced for inspiration, not compliance

## Open Questions
- How far do current services deviate from clean OSOM-aligned boundaries? This determines the scale of future reconciliation work.
- Do existing services map to single OSOM services, or do they represent bundled/misaligned capabilities? This affects how contracts will eventually be structured.
- What is the minimum structure required for useful LLM reasoning versus future OSOM contract completeness? This balances capture speed against future utility.

## Work Breakdown

### Files / Deliverables
- `vault/50-services/hybrid-service-delivery-management.md`
- `vault/50-services/hybrid-solution-architecture.md`
- `vault/50-services/data-center-operations.md`
- `vault/50-services/hosting.md`
- `vault/50-services/network.md`
- `vault/50-services/service-desk.md`
- `vault/50-services/managed-cloud.md`
- `vault/50-services/data.md`
- High-level Mermaid diagram of perceived current interactions (not validated)

### Sequence
1. Convert existing service guides to normalized Markdown format (where guides exist)
2. For services without guides or with incomplete content, capture via lightweight owner input
3. Conduct optional follow-up interviews to fill gaps or clarify ambiguity
4. Store all outputs as-is, including conflicting definitions
5. Review full set for structural consistency across services

## Decisions Made
- Conflicts and inconsistencies are treated as primary outputs, not issues to resolve in this phase
- The minimum viable structure requires: service name, owner, one-paragraph description, declared responsibilities, declared upstream dependencies, declared downstream dependencies
- All other OSOM-inspired fields (lifecycle, evolution, measures) are optional
- After initial creation, each service owner is responsible for maintaining their guide—no governance model is defined in this phase
- LLM use will focus on comparing descriptions, identifying overlaps/gaps, and summarizing inconsistencies—not full programmatic parsing

## Delegation State
| Person | Owns | By When | Level | Status |
| ------ | ---- | ------- | ----- | ------ |
| Lacie-Ellen Morley | Hybrid Service Delivery Management guide | | | |
| Pat Wolthausen | Hybrid Solution Architecture guide | | | |
| George Revie | Data Center Operations guide | | | |
| Martin Tessier | Hosting guide | | | |
| Ben Kennedy | Network guide | | | |
| Jason Auer | Service Desk (L2/L3/NOC) guide | | | |
| Andrei Ianouchkevitch | Managed Cloud guide | | | |
| Jorge Quintero | Data guide | | | |