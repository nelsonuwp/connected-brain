---
type: thinking
created: 2026-04-10
status: raw
---

# Company-Wide Inventory

## The Idea
A capacity accounting model across six dimensions of the business — Space, Power, Racks, Network, Compute, and People — where each dimension is expressed as three numbers:

- **Owned** — what we have (physical assets provisioned/owned, or people hours available)
- **Sold** — what's been committed to or deployed for customers (or internally consumed)
- **Available to Sell** — how much more we can monetize before we need to buy more (or hire more)

The "Available to Sell" number is the strategic output. It answers: *what can we take to a customer or a business case today, without a capex conversation?*

## Why This Matters
This reframes a routine equipment inventory into a decision-support instrument. Without this framing, the exercise produces a list. With it, it produces a number that directly governs Private Cloud siting decisions in the UK and US — and eventually a living operational metric for the business.

## History
- **2026-03-19** — Adam raised this internally with the Service Network team, proposing the Owned / Sold / Available-to-Sell framework across the six dimensions. Ben Kennedy responded to clarify the Network dimension (see below).
- **2026-04-09** — Dave Pistacchio (DigitalBridge consultant) independently pushed Ian Rae for a company-wide equipment inventory to plan Private Cloud and Cloud MC buildouts in UK and US. Ian looped Adam in to coordinate.
- **2026-04-10** — The two threads are the same initiative. Adam was already ahead of it. The external pressure from Dave creates a timeline and a forcing function.

## Dimension Owners

| Dimension | What "Owned" Means | What "Sold" Means | Owner |
|---|---|---|---|
| Space | Sellable sqft in each DC | Allocated to colo cages, our own racks, etc. | George Revie (DC Ops) |
| Power | kW provisioned in each DC | Committed to customers and internal gear | George Revie (DC Ops) |
| Racks | Racks installed on floor | Sold/filled (colo + our hosting) | George Revie (DC Ops) |
| Network | Connectivity capacity: bandwidth, cross-connects, IP blocks, switches (81x Juniper EX-4300T), firewalls | Sold/deployed to customers and current ops | Ben Kennedy (Network) |
| Compute | Servers owned (deployed + shelf) + storage (NetApp FAS, SolidFire) | Sold to hosting customers / deployed to IaaS | George Revie (physical) + Martin Tessier (logical/IaaS) |
| People | Managed services headcount capacity (hours) | Committed to active managed services delivery | Andrei Ianouchkevitch (Managed Cloud) + Will (Azure/AWS) |

## Complications Ben Flagged (Network)
Network is not a single number in any column. It has discrete sub-elements that each need their own Owned / Sold / Available row:
- Bandwidth (transit/peering)
- Cross-connects
- IP address blocks
- Switching ports
- Firewalls — these have a physical inventory (Owned is knowable)
- Load balancers — **not fixed inventory**. Currently using a Citrix licensing loophole: 5 licenses, one of which covers all managed hosting load balancers via a 1TB pool. This year's "Owned" figure is an artifact of that arrangement, not a durable capacity number.

## What I Don't Know
- What level of granularity Dave actually needs for the Private Cloud siting decision (per-DC or aggregate?)
- Whether existing asset tracking systems (CMDB — George's responsibility per service description) can produce Owned/Sold/Available directly, or whether manual reconciliation is required
- How People capacity should be measured — headcount is too coarse. What's the assumed utilization rate at "Sold"? Skills gaps within the available headcount?
- Whether Martin's team (Compute Platforms) tracks deployed server inventory separately from George's physical inventory — and whether those two numbers align
- The timeline Dave expects for delivery
- Whether the Managed Cloud team's cost misallocation (17 Service Desk people previously attributed to Andrei's org) affects how People capacity is counted

## Assumptions I'm Making
- The six dimensions are the right ones for a Private Cloud planning decision — licensing/software and IP blocks may deserve their own rows
- Each owner has access to the data needed (CMDB accuracy is a known target metric for George's team, but actual accuracy is not confirmed)
- Dave and Ian will accept this structured framing rather than expecting a simple asset list
- The "Available to Sell without additional spend" framing is the right constraint — but some "Available" capacity may still require operational spend to activate (e.g., network provisioning, rack prep)

## Risks
- The Citrix load balancer loophole makes part of the Network "Available to Sell" figure temporary — any model built on it has a shelf life
- CMDB discrepancy vs. physical audit is a stated George metric with a target of 0% — which implies current accuracy is not 0%
- George's team serves Space, Power, Racks, and Compute (physical) — the single biggest data dependency in this model is concentrated in one team
- People capacity is qualitatively different from physical capacity: it shrinks with utilization, attrition, and redeployment — it won't wait for the model to be ready
