---
type: thinking
created: 2026-02-23
status: raw
promoted-from: 01-inbox
---

# Service Guides Updates (Intermediate)

### The Raw Idea
I am creating a baseline, machine-readable representation of our current service landscape.

This work will align to the [[OSOM Model]] structure (service contracts, lifecycle, evolution), but this phase is not about producing finalized OSOM-compliant service contracts.

Instead, I am capturing each service’s **declared current state** in a normalized Markdown format. These will act as _pre-contract artifacts_ that:
- Surface inconsistencies across services
- Provide raw input for future alignment
- Seed the eventual OSOM service contracts

The output of this phase is a **set of normalized, service-level artifacts representing declared current state**.

These artifacts are intentionally incomplete, potentially contradictory, and not authoritative.
They serve as the input for future phases:
- Cross-service alignment
- Boundary definition
- OSOM-aligned service contract creation

Current Service Owners:
- Hybrid Service Delivery Management - [[Lacie-Ellen Morley]]
- Hybrid Solution Architecture - [[Pat Wolthausen]]
- Data Center Operations - [[George Revie]]
- Hosting - [[Martin Tessier]]
- Network - [[Ben Kennedy]]
- Service Desk (L2/L3/NOC) - [[Jason Auer]]
- Managed Cloud - [[Andrei Ianouchkevitch]]
- Data - [[Jorge Quintero]]
*Note:  Security & Compliance lives outside of the network discussions for now.*

### **Scope of This Phase**

This initiative is explicitly limited to **baseline capture of declared service state**.

This phase will:
- Capture each service owner’s description of their service in a consistent Markdown format
- Centralize all service documentation in `vault/50-services`
- Allow conflicting, overlapping, or incomplete definitions to exist without resolution

This phase will not:
- Reconcile conflicting service definitions
- Enforce service boundaries or ownership
- Produce finalized service contracts
- Fully implement the Organised Services Operating Model
- Define governance, lifecycle enforcement, or evolution paths

Conflicts and inconsistencies are expected and treated as **primary outputs**, not issues to resolve.

### **Method**

1. I will take existing service guides and convert them into a normalized Markdown format
	1. Where no guide exists or content is incomplete, I will capture the service via lightweight input from the owner
2. The guide reflects their **declared understanding of:**
    - Responsibilities
    - Dependencies
    - Boundaries
3. Optional follow-up interviews fill gaps or clarify ambiguity
4. All outputs are stored as-is, including conflicting definitions

---

### Why This Matters

We currently lack a unified, machine-readable view of our service network.

Without that, every discussion about services is subjective, fragmented, and dependent on individual perspectives. That makes alignment slow and inconsistent.

By centralizing the current state:
- We create a shared reference point for all service owners
- We remove ambiguity during cross-service discussions
- We enable LLM-assisted analysis grounded in actual operational context

This is less about documentation and more about **establishing a shared reference point for discussing reality**.

---

### What I Think I Want

- A complete set of **baseline service guides** in Markdown representing the current, declared state of:
    - Hybrid Service Delivery Management
    - Hybrid Solution Architecture
    - Data Center Operations
    - Hosting
    - Network
    - Service Desk (L2/L3/NOC)
    - Managed Cloud
    - Data
- Each service guide loosely aligned to the structure of an OSOM service contract (from [[OSOM Model]]), but:
    - Fields are **descriptive, not authoritative**
    - Conflicts and ambiguity are explicitly allowed
    - Lifecycle and evolution sections are captured only if they reflect current reality
- All documentation centralized in `vault/50-services`
- A minimal, consistent structure across services to allow comparison, not enforcement
- A high-level Mermaid diagram representing **perceived current interactions**, not validated 
- Clear mapping of **current ownership as stated by each service**, even if conflicting
- A **lightweight, consistent structure** across all service guides:
	- Inspired by OSOM service contracts, lifecycle, and evolution
	- Not all sections are required or expected to be complete
	- Structure is optimized for **speed of capture and comparison**, not completeness

---
### **Minimum Viable Structure**

Each service guide must include:
- Service Name
- Owner
- One-paragraph description of purpose
- Declared responsibilities (what this service believes it owns)
- Declared dependencies:
    - Upstream (what it depends on)
    - Downstream (what depends on it)

All other fields (lifecycle, evolution, measures, etc.) are optional in this phase. Fields may be incomplete, ambiguous, or internally inconsistent. This is acceptable in this phase.

---
### What I Don't Know Yet

- How far current services deviate from a clean OSOM-aligned model (service boundaries, lifecycle maturity, evolution paths)
- Whether existing services map cleanly to single OSOM services or represent bundled/misaligned capabilities
- The minimum structure required for LLM reasoning vs. future OSOM contract completeness

---

### **LLM Use (Phase 1)**

The captured service guides will be used to:
- Compare how services describe responsibilities and dependencies
- Identify overlaps, gaps, and conflicting boundary definitions
- Summarize cross-service inconsistencies to support alignment discussions

This phase does not optimize for full programmatic parsing or automation.

---
### What I'm Conflating

- **Baseline vs. Contract:** These documents resemble service contracts but are not yet validated, agreed, or enforceable
- **OSOM Alignment vs. OSOM Compliance:** Referencing OSOM does not mean the current state adheres to it
- **Capture vs. Reconciliation:** This phase captures conflicting perspectives but does not attempt to resolve them

---

### Who Else Is Involved

- **Service Owners (source of truth for current state):**  
    Ben, George, Martin, Lacie, Pat, Jason, Andrei, Jorge
- **Adjacent Stakeholders (context providers, not primary authors):**  
    Infrastructure, Professional Services

Their role in this phase is to
- Describe their service as it operates today
- Declare perceived boundaries, dependencies, and responsibilities

Not to:
- Resolve overlaps
- Redesign services
- Fully conform to OSOM structures

**This is:**
- A structured capture of each service’s declared current state
- A precursor to OSOM-aligned service contracts
- A tool to surface misalignment across the service network

**This is not:**
- A finalized service contract
- A validated or agreed service model
- An implementation of the Organised Services Operating Model

After initial creation, each service owner is responsible for maintaining their service guide.  
No governance or enforcement model is defined in this phase.

---
### **Output of This Phase**

- 8 Markdown-based service guides in `vault/50-services`
- Each guide reflects a **declared, unvalidated view** of the service
- A comparable structure across all services
- A visible set of overlaps, gaps, and conflicting definitions across the network

---
