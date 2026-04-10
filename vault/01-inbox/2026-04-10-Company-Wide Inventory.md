---
type: idea
created: 2026-04-10
status: idea
---

# Company-Wide Inventory

## The Idea

A structured capacity accounting model — not just an inventory — that expresses Aptum's available infrastructure across six dimensions: Space, Power, Racks, Network, Compute, and People. Each dimension is measured as:

- **X** = total capacity provisioned/owned
- **Y** = committed or deployed (to customers or internal operations)
- **Z** = available to sell or deploy without additional spend

This gives a **revenue-ready picture of the business** — what can be monetized today, per DC, per region — and serves as the foundational input for Private Cloud build decisions in UK and US.

The framing is deliberately CFO-level: Z answers "what can we sell before we need capex?" That's a different and more powerful question than "what do we own?"

## Why Now

[[Dave Pistacchio]] (DigitalBridge consultant) pushed [[Ian Rae]] on 2026-04-09 to do a full equipment inventory — deployed and shelf — to plan Private Cloud and Cloud MC buildout in the UK and US, including where to site them. Ian looped in Adam to coordinate across four owners:

- **Matt Carter** — server inventory (assets relevant to Aptum IaaS)
- **George** — DC capacity (space and power per DC)
- **Martin** — APT Cloud roadmap (IaaS rollout plan, legacy Aptum Cloud / MTC migration timeline)
- **Will** — APT Cloud Azure and AWS customer roadmap (bonus)

Ian's framing: Dave will see this as his initiative — think about how to coordinate and follow up with him directly. The window to shape *how* this is done (vs. just producing a list) is open now, before it collapses into a simple inventory exercise.

## Supplemental Data

Adam's framework draft:
```
Space
- We have X sellable sqft
- We've allocated Y sqft (to colo cages, our own racks, etc.)
- We have Z sqft available to sell without spending more

Power
- We have X kW provisioned
- We've committed Y kW to customers and our own gear
- We have Z kW available to sell without spending more

Racks
- We own X racks installed on the floor
- We've sold/filled Y racks (colo + our hosting)
- We have Z racks available to sell without buying more

Network
- We have X capacity in connectivity (bandwidth, cross-connects, transit/peering) and infrastructure devices (switches, firewalls, load balancers)
- We've sold/deployed Y to customers and current operations
- We have Z capacity available to sell or deploy without spending more

Compute
- We own X servers (deployed + on the shelf)
- We've sold Y servers to hosting customers
- We have Z servers available to sell without buying more

People
- We have X capacity in managed services headcount
- We're delivering Y in active managed services
- We have Z capacity available to sell without hiring
```

Ben's notes on Network:
```
For X and Z, it would be like x1, x2, etc and z1, z2, etc — given the number of different capacity elements.

Firewalls and load balancers are tricky for X. We have inventory of firewalls, so you could call that X capacity. For load balancers we are at Citrix's whims. Traditionally it's an incremental cost, not a fixed cost for X capacity. This year we are using a loophole to only pay for 5 licenses, 1 of which is licensing all our managed hosting load balancers as that license gives us access to a 1TB pool. So this year we could call that "x" capacity.
```
