---
type: thinking
created: 2026-02-23
status: raw
promoted-from: 01-inbox
---

# Service Guides Updates (Intermediate)

### The Raw Idea

I need to establish the definitive operational canon of our organization. To do this, I am converting our fragmented service network into a machine-readable format (Markdown) to serve as context for LLMs. This will allow me to feed the LLM situational data (like delivering a new product) and get strategic feedback based on how our services actually interconnect.

I have the authority to dictate the final boundaries. We will define the current state first to identify overlaps and underlaps, build the scaffolding in Markdown, and then meet with the service owners to force alignment and solidify the operational architecture.

Current Service Owners:
- Hybrid Service Delivery Management - [[Lacie-Ellen Morley]]
- Hybrid Solution Architecture - [[Pat Wolthausen]]
- Data Center Operations - [[George Revie]]
- Hosting / Security & Compliance - [[Martin Tessier]]
- Network - [[Ben Kennedy]]
- Service Desk (L2/L3/NOC) - [[Jason Auer]]
- Managed Cloud - [[Andrei Ianouchkevitch]]
- Data - [[Jorge Quintero]]
---

### Why This Matters

There is no machine-readable source of truth for our services. Digitizing this context allows me to leverage LLMs to rapidly evaluate new products, identify operational bottlenecks, and make data-driven architectural decisions. Having a strictly defined, unified operational model is also critical for demonstrating a highly efficient, packaged business model as we prepare operations for our upcoming milestones next year.

---

### What I Think I Want

- The Service Guide Template filled out for the core delivery network:
    - Hybrid Service Delivery Management
    - Hybrid Solution Architecture
    - Data Center Operations
    - Hosting
    - Network
    - Service Desk (L2/L3/NOC)
    - Managed Cloud
    - Data
- These services follow the [[OSOM Model]] (and the mermaid diagram [[OSOM Mermaid]])
- All documentation living as Markdown files in `vault/50-services`. These are the service contract. Not currently created in markdown.
- A clear visual map of how services fit together and flow via a Mermaid diagram.
- A definitive, signed-off list of products and services that each team is responsible and accountable for.

---

### What I Don't Know Yet

- We don't have a 100% agreed-upon list of products and services yet.
- The exact data structure (e.g., Zod schema or YAML frontmatter) the LLM will need within the Markdown files to reliably parse dependencies without a formal relational database.
- How to handle legacy documentation discrepancies during the transition (e.g., historical documents showing heavy interdependent loops between Data Center, Network, and Infrastructure that may not reflect today's reality).    

---

### What I'm Conflating

- **Formatting vs. Fixing:** I am conflating the act of converting documents to Markdown with the act of fixing broken organizational logic. Formatting a bad process just creates a well-formatted bad process.
- **Current State vs. Future Canon:** I want to map the "current state," but the ultimate goal is the clean, streamlined "canon" of the business. I need to be careful not to hardcode legacy silos into our new LLM scaffolding.

---

### Who Else Is Involved

- **Core Owners:** Ben, George, Martin, Lacie, Pat, Jason, Andrei, Jorge.
- **Potential Adjacencies:** Based on the existing service charts, there may be touch-points with Infrastructure and Professional Services that need to be accounted for in the inputs/outputs, even if those specific owners aren't directly authoring this initial batch.




---

# Explore — 2026-02-24 02:15 UTC

## Explore — 2026-02-23

### The Central Tension

You're building infrastructure for machine reasoning about your organization, but the organization itself hasn't finished reasoning about its own structure. The LLM context layer assumes clean boundaries that don't exist yet—you're creating a representation layer for a reality that's still contested. The risk isn't just "well-formatted bad process"; it's that the Markdown scaffolding becomes the forcing function for organizational decisions that should be made on operational merit, not documentation convenience.

### What I'd Push On

**The authority question cuts both ways.** You say you have authority to dictate final boundaries. But dictating boundaries into Markdown and getting service owners to actually operate within those boundaries are different things. What happens when George and Ben both claim ownership of something, you pick one, and the other continues operating as before? The Markdown says one thing; reality says another. Your LLM now has confident wrong context.

**The "current state first" sequencing may be backwards.** If the goal is the clean canon, documenting current state in machine-readable format creates an artifact that immediately needs to be deprecated. You'll have invested effort in precisely capturing ambiguity. Consider whether you actually want "aspirational state with current-state annotations" instead.

**The LLM use case is underspecified in a way that matters.** "Feed situational data and get strategic feedback" is doing a lot of work. What's the actual interaction pattern? Are you querying for routing decisions ("who handles this?"), dependency analysis ("what breaks if X changes?"), or something else? The schema design depends heavily on what questions you're asking. Zod vs. YAML frontmatter is a downstream decision from this.

**Signed-off accountability lists have a half-life.** Products and services shift. Owners change. The static Markdown file problem is that it decays silently. What's the maintenance model? Who updates when reality drifts?

### Questions You Need to Answer

1. When you "force alignment" in owner meetings, what's your actual move when two owners have incompatible claims and neither will yield? Do you have the organizational capital to impose, or will this surface a fight you can't finish?

2. What's the minimum viable schema that lets you start querying before full coverage? Can you get value from three services documented while the other five are in progress, or does partial coverage produce misleading outputs?

3. The legacy documentation showing "heavy interdependent loops"—is that documentation wrong, or is the current org chart wrong? Which one reflects how work actually flows today?

4. If the upcoming milestones require demonstrating a "highly efficient, packaged business model," is the deliverable the Markdown files themselves, or the organizational clarity they're supposed to represent? Because you can have one without the other.

---

# Critique — 2026-02-24 02:17 UTC

### What's Solid

- Clear identification of the core problem: no machine-readable source of truth for services
- Specific list of service owners and services to document
- Recognition that formatting ≠ fixing organizational problems
- Awareness of the current state vs. future canon tension
- Concrete deliverable format (Markdown in `vault/50-services`)

### What's Weak or Missing

- **Authority claim (Raw Idea):** "I have the authority to dictate final boundaries" is asserted but not validated. No evidence of organizational capital to enforce when owners disagree.
- **LLM use case (What I Think I Want):** "Feed situational data and get strategic feedback" is too vague to drive schema design. No specific query patterns defined.
- **Sequencing logic (What I Think I Want):** "Define current state first" contradicts the goal of building clean canon. Creates throwaway work.
- **Maintenance model (entire note):** No plan for keeping Markdown current as reality drifts. Static files decay silently.
- **Conflict resolution (Who Else Is Involved):** No mechanism specified for when service owners have incompatible ownership claims.
- **Value threshold (What I Think I Want):** Unclear if partial coverage (3 of 8 services) produces useful LLM outputs or misleading ones.
- **Legacy documentation (What I Don't Know Yet):** Question raised about historical interdependencies but not answered—is old documentation wrong or is current org chart wrong?

### Unanswered Questions in the Note

- How to handle legacy documentation discrepancies during transition? (explicitly raised in What I Don't Know Yet)
- What exact data structure will LLMs need to reliably parse dependencies? (explicitly raised in What I Don't Know Yet)
- What happens when the Mermaid diagram reveals overlaps/underlaps—who decides the resolution?
- Are the "upcoming milestones next year" requiring the Markdown artifacts themselves or the organizational clarity they represent?
- Which reflects actual work flow today: legacy docs showing interdependent loops, or current org chart showing clean separation?

### Ready to Spec?

No. The note conflates documentation infrastructure with organizational restructuring but hasn't resolved which problem to solve first. The authority to enforce boundaries, conflict resolution mechanism, and minimum viable schema all need validation before speccing deliverables.