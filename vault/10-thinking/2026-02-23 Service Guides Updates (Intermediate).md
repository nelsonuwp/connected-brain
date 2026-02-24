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
- **Potential Adjacencies:** Based on the existing service charts, there may be touchpoints with Infrastructure and Professional Services that need to be accounted for in the inputs/outputs, even if those specific owners aren't directly authoring this initial batch.


## Ready to Promote?
<!-- A thinking note is ready for 30-initiatives when you can answer YES to all three: -->
- [ ] I know who owns this
- [ ] I can describe a measurable outcome
- [ ] I have a rough timeline

---
## Think Mode Output
<!-- Paste LLM think-mode response here after running it -->


## My Answers
<!-- Answer the questions the LLM raised before promoting to initiative -->

