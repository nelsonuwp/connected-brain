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
1. Nine Markdown service guides exist in `vault/50-services`, one for each service area
2. Each guide contains at minimum: service name, owner, one-paragraph purpose, declared responsibilities, and declared dependencies (upstream and downstream)
3. All guides follow a consistent structure that enables side-by-side comparison
4. Conflicting or overlapping definitions across services are explicitly visible in the documentation
5. Service owners can identify their service's declared state without external interpretation
6. Each service guide follows an identical section structure and ordering (no deviations)
7. Each data point in a service guide is attributable to a source (owner or document), with no inferred content

## Constraints
- This phase captures only; it does not reconcile conflicting definitions
- Service boundaries and ownership disputes are documented as-is, not resolved
- No finalized service contracts will be produced
- No governance, lifecycle enforcement, or evolution paths will be defined
- Security & Compliance is explicitly out of scope for this phase
- OSOM structure is referenced for inspiration, not compliance
- No inferred, normalized, or “cleaned up” responsibilities may be added
- All ambiguity, duplication, and conflict must be preserved explicitly
- Structure is fixed; service owners cannot modify headings or format

## Template Enforcement
- All service guides must strictly follow the `Service Network Template.md`.
- No sections may be added, removed, or renamed.
- If a service does not have information for a section, it must still be included with: [Not Provided]
- This ensures full comparability across all services.

## Open Questions
- How far do current services deviate from clean OSOM-aligned boundaries? This determines the scale of future reconciliation work.
- Do existing services map to single OSOM services, or do they represent bundled/misaligned capabilities? This affects how contracts will eventually be structured.
- What is the minimum structure required for useful LLM reasoning versus future OSOM contract completeness? This balances capture speed against future utility.

## Work Breakdown

### Files / Deliverables
- `vault/50-services/hybrid-service-delivery-management.md`
- `vault/50-services/hybrid-solution-architecture.md`
- `vault/50-services/data-center-operations.md`
- `vault/50-services/professional-services.md`
- `vault/50-services/hosting.md`
- `vault/50-services/network.md`
- `vault/50-services/service-desk.md`
- `vault/50-services/managed-cloud.md`
- `vault/50-services/data.md`
- High-level Mermaid diagram of perceived current interactions (not validated)

### Sequence
1. Apply the standardized template to all existing service guides (no restructuring beyond template)
2. Capture missing services using direct owner input (written or interview)
3. Record all inputs exactly as declared (no normalization or interpretation)
4. Explicitly document overlaps and ambiguities in the designated section
5. Validate structural consistency only (not content accuracy)
6. Freeze initial baseline once all services are captured

## Decisions Made
- Conflicts and inconsistencies are treated as primary outputs, not issues to resolve in this phase
- The minimum viable structure requires: service name, owner, one-paragraph description, declared responsibilities, declared upstream dependencies, declared downstream dependencies
- All other OSOM-inspired fields (lifecycle, evolution, measures) are optional
- After initial creation, each service owner is responsible for maintaining their guide—no governance model is defined in this phase
- LLM use will focus on comparing descriptions, identifying overlaps/gaps, and summarizing inconsistencies—not full programmatic parsing
- “Declared state” is strictly enforced: no inferred or synthesized responsibilities
- Ambiguities and overlaps are first-class outputs and must be explicitly captured
- Template structure is fixed and non-negotiable across all services
- LLM usage is optimized for comparison and inconsistency detection, not automation or enforcement

## LLM Use (Explicit)
The captured service guides are intended to support:
- Cross-service comparison of responsibilities
- Identification of overlapping or conflicting ownership
- Detection of missing responsibilities or gaps in the service network
- Summarization of inconsistencies across the network
The structure is optimized for human-readable + LLM-assisted reasoning, not strict programmatic parsing.