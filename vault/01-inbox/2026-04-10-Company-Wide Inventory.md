---
type: idea
created: 2026-04-10
status: raw
---

# Company-Wide Inventory

## The Idea


## Why Now

Email from [[Dave Pistacchio]]:
```
**From:** David Pistacchio (Consultant) <David.Pistacchio@digitalbridge.com>  
**Sent:** Thursday, 09 April 2026 12:14:54  
**To:** Ian Rae <ian.rae@aptum.com>; Sarah Blanchard <sblanchard@cloudops.com>  
**Subject:** Inventory search and Data Center planning for Private Cloud.

On our call on Tuesday, I believe that we agreed that we will need to look at all of our available inventory of equipment including what's deployed and no longer used, and what's not yet deployed, and determine what we will need to build a Private Cloud and Cloud MC environment in the UK and the US.  We also need to determine where we should set them up. 

  

It seems to me that we should get George and his team as well as the Logistics guys in Sarah's team working on this ASAP.  Is there any reason why we can't? 

  

Dave
```

[[Ian Rae]] Response:
```
We have the server inventory (Matt C), as well as a map of free space and power per DC (George. Will get the team on it and loop in Adam (cc) and Martin who has the current deployment plans.
```

And then another email directly to me 
## Supplemental Data

Me:
```
Guys....need your input on something.... am I thinking about this correctly?

**Space**

- We have X sellable sqft
- We've allocated Y sqft (to colo cages, our own racks, etc.)
- We have Z sqft available to sell without spending more

**Power**

- We have X kW provisioned
- We've committed Y kW to customers and our own gear
- We have Z kW available to sell without spending more

**Racks**

- We own X racks installed on the floor
- We've sold/filled Y racks (colo + our hosting)
- We have Z racks available to sell without buying more

**Network**

- We have X capacity in connectivity (bandwidth, cross-connects, transit/peering) and infrastructure devices (switches, firewalls, load balancers)
- We've sold/deployed Y to customers and current operations
- We have Z capacity available to sell or deploy without spending more

**Compute**

- We own X servers (deployed + on the shelf)
- We've sold Y servers to hosting customers
- We have Z servers available to sell without buying more

**People**

- We have X capacity in managed services headcount
- We're delivering Y in active managed services
- We have Z capacity available to sell without hiring
```

Ben:
```
- We have X capacity in connectivity (bandwidth, cross-connects, transit/peering) and infrastructure devices (switches, firewalls, load balancers)
- We've sold/deployed Y to customers and current operations
- We have Z capacity available to sell or deploy without spending more  
      
    comments from me: I'd say this is mostly right. But for x and z, I mean it would be like x1, x2, etc and z1, z2, etc. Given the number of different capacity elements.  
      
    Firewalls and load balancers are tricky for X. We have inventory of firewalls, so you could call that X capacity. For load balancers we are at Citrix's whims. Traditionally it's an incremental cost, not a fixed cost for X capacity. This year we are use a loophole to only pay for 5 licenses, 1 of which is licensing all our managed hosting load balancers as that license gives as access to a 1TB pool. So this year we could call that "x" capacity
```