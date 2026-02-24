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


---

# Explore — 2026-02-24 12:37 UTC

## Explore — 2026-02-23

### The Central Tension

You want a machine-readable operational canon that serves as LLM context for strategic decision-making. But you're building this on top of a service network where the boundaries themselves are contested or undefined. The tension: **you cannot create a definitive schema for services whose definitions aren't yet stable.** You risk encoding organizational ambiguity into your "source of truth," making the LLM confidently reason over fiction.

The deeper version: you have authority to dictate boundaries, but you're planning to "meet with service owners to force alignment" *after* building the scaffolding. That's backwards. The Markdown structure will shape what questions you ask and what gets captured. If you scaffold first, you'll either (a) rework everything post-alignment, or (b) subtly constrain the alignment conversations to fit what you already built.

### What I'd Push On

**1. The sequencing is inverted.** You're treating the Markdown conversion as the forcing function for alignment. But the schema you choose (frontmatter fields, dependency syntax, input/output definitions) embeds assumptions about how services relate. If you haven't resolved the overlaps between Data Center, Network, and Infrastructure, what exactly are you encoding in the `dependencies` field? You'll either leave it vague (defeating the LLM parsing goal) or make it up (creating authoritative-looking fiction).

**2. "Current state first" might be a trap.** You say you'll map current state to identify overlaps, then fix them. But your goal isn't documentation—it's LLM-usable context for strategic reasoning. A current-state map full of legacy silos and broken interdependencies is *worse* than no map, because the LLM will treat it as canonical. You need to decide: are you documenting what exists, or defining what should exist? These produce different artifacts.

**3. The OSOM model is aspirational here, not descriptive.** Your mermaid diagram shows a clean service network with clear flows. Your note reveals a different reality: contested boundaries, legacy documentation showing "heavy interdependent loops," no agreed product/service list. Calling this an OSOM implementation doesn't make it one. The gap between diagram and reality is your actual problem—and the Markdown conversion won't close it.

**4. "Machine-readable" isn't a solved problem for your use case.** You mention needing a data structure (Zod schema, YAML frontmatter) for LLM parsing. But what queries will you actually run? "Feed situational data and get strategic feedback" is too vague to design a schema for. If you can't enumerate the top 5 questions you'll ask the LLM about your service network, you can't know what data needs to be structured vs. prose.

**5. The service owners are being handed a fait accompli.** You're building the scaffolding, then meeting to "force alignment." That's a power move, not a collaborative definition. It might work—you have authority—but expect resistance to manifest as nitpicking the schema, disputing boundary definitions, or passive non-compliance with updates. Have you gamed out what happens when Ben and George disagree about where Network ends and Data Center begins, and your Markdown already assumes an answer?

### Questions You Need to Answer

1. **What are the actual LLM queries you want to run?** Not "strategic feedback"—specific questions. "If we launch Product X, which services are affected and in what order?" or "Where are we under-resourced relative to service dependencies?" The queries determine the schema.

2. **What happens when two service owners claim the same product/function?** You say you have authority to dictate. Will you? What's the escalation path if someone refuses the boundary you set?

3. **Should the Markdown encode current-state reality or target-state architecture?** If current, how do you prevent the LLM from optimizing for a broken model? If target, how do you handle the gap between what's documented and what actually happens?

4. **What's the minimal viable schema?** You might be over-engineering. Could you start with: service name, owner, one-line purpose, explicit dependencies (upstream/downstream), and primary user—then iterate? The Zod schema might be premature optimization.

5. **How will you keep this updated?** You're creating a living document system. Who's accountable for keeping each service's Markdown current? What triggers an update? Without this, you're building a snapshot that decays immediately.

6. **What's the forcing function for the alignment meetings?** If you show up with a draft schema and say "fill this out," you'll get compliance. If you show up and say "define your service boundary against these neighbors," you'll get the argument you actually need. Which meeting are you running?