---
type: thinking
status: raw
---

# Company-Wide Inventory

## The Idea
A six-dimension capacity accounting model (Space, Power, Racks, Network, Compute, People) that measures each dimension as total capacity (X), committed/deployed (Y), and available-to-sell-without-capex (Z), providing a CFO-level view of revenue-ready infrastructure across Aptum's data centers.

## Why This Matters
This reframes a routine equipment inventory into a strategic planning tool. The Z dimension directly answers "what can we sell before we need capex?" — which is the constraint that governs Private Cloud build decisions in UK and US. Without this framing, the exercise collapses into a list rather than a decision-support model.

## What I Know
- Dave Pistacchio (DigitalBridge consultant) initiated this on 2026-04-09 as an equipment inventory request
- Ian Rae is coordinating and has looped in Adam
- Four owners are involved: Matt Carter (servers), George (DC capacity), Martin (APT Cloud roadmap), Will (Azure/AWS customer roadmap)
- The window to shape the methodology is open now, before it defaults to a simple inventory list
- Ben has flagged that Network capacity has multiple sub-elements requiring x1, x2, z1, z2 notation
- Load balancer capacity is complicated by licensing models (Citrix loophole this year)
- Firewalls have inventory that could count as X capacity

## What I Don't Know
- Whether the four owners will accept the X/Y/Z framework or push back
- What level of granularity Dave actually needs for the Private Cloud siting decision
- How frequently this data would need to be refreshed to remain useful
- Whether existing asset tracking systems can produce X/Y/Z numbers or if manual reconciliation is required
- The timeline Dave expects for delivery

## Assumptions I'm Making
- The X/Y/Z framing adds enough value over a flat inventory to justify the additional coordination complexity
- Each of the four owners has access to the data needed for their dimension
- Dave and Ian will see the strategic framing as additive rather than scope creep
- The six dimensions are comprehensive enough for Private Cloud planning purposes

## Risks and Constraints
- Dave may view the expanded scope as Adam overcomplicating his request
- Network and People dimensions are harder to quantify than physical assets
- Coordination across four owners creates scheduling and handoff friction
- Data quality varies by dimension — some may require significant cleanup before X/Y/Z is calculable
- The "loophole" in load balancer licensing is temporary, making that Z figure unstable

## Next Step
Run thinking explore on this note to stress-test whether the X/Y/Z framework survives contact with each owner's data reality.