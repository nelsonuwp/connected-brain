---
type: idea
created: 2026-03-03
status: raw
---

# Standardize Hardware Lifecycle and EOL Management

## The Idea
We currently lack a defined, enforceable strategy for managing hardware lifecycles. Once customer hardware is fully depreciated (typically after 3 years), it remains in our data centers indefinitely at "zero" equipment cost. While this appears to generate 100% margin on monthly recurring revenue, it creates a massive, hidden operational debt.

Because we do not have a hard cutoff for End of Sale, End of Updates, End of Support, or End of Parts, customers are deeply disincentivized to upgrade. We are left acting as both the service provider and the life-support system for dangerously obsolete equipment.

**Case Study: Winston Data** The recent incidents with Winston Data perfectly encapsulate this systemic issue. We manage 10 services for them, many comprising components provisioned over a decade ago.

- **Service 2036467 (Juniper SSG 5 Firewall):** Provisioned in April 2009. This hardware reached End of Life in 2014 and End of Support in January 2020. Because it runs in a deprecated "Transparent Mode," modern configurations are nearly impossible.
    
    - _The Impact:_ In ticket APTUM-37423, setting up a standard Site-to-Site VPN resulted in months of back-and-forth. Network Engineers spent over 2 hours on a single troubleshooting call, experienced unintended production impacts due to legacy policy-based routing rules, and required Account Management to step in repeatedly to explain why their 17-year-old firewall couldn't handle modern architectures.
        
- **Service 2433647 (Web1 Server):** Provisioned in September 2011, running Windows Server 2008 R2.
    
    - _The Impact:_ In ticket APTUM-51205, this server experienced a P1 outage on a Saturday night due to a dead power supply. We had absolutely no replacement parts in inventory. The _only_ reason the customer's server was brought back online was the sheer luck that another customer had recently deprovisioned the exact same obsolete chassis, allowing DCOPS to scavenge parts.
        

Between NOC monitoring, DCOPS physical labor, senior network engineering troubleshooting, and Account Management escalations, we burned dozens of highly-paid staff hours supporting gear that should have been retired a decade ago.

## Why Now
We need to clearly define our identity: Are we delivering a guaranteed **service** (where we cycle the hardware to ensure SLA delivery), or are we simply renting out **hardware** (where the customer dictates the lifecycle)? Leaving this unaddressed creates severe risks:

- **Exploding OpEx Costs:** The "free" hardware is actually costing us thousands of dollars in wasted engineering and support time. High-tier resources are acting as mechanics for vintage equipment rather than building and supporting scalable, modern solutions.
    
- **SLA and Reputation Risk:** We cannot honor Service Level Agreements when replacement parts literally do not exist. We are one dead power supply away from permanently losing a customer's environment and taking the blame for the downtime, even when we've warned them (as Account Management heavily documented with Winston Data).
    
- **Security and Compliance Liabilities:** Housing servers running Windows Server 2008 and firewalls that haven't received firmware updates in over 6 years introduces massive security vulnerabilities to our network and our clients' environments.
    
- **Stagnation of Service Delivery:** Legacy hardware blocks our ability to modernize. We cannot efficiently manage our IP space or roll out modern networking features (like Routed Mode VPNs) when we are forced to cater to 15-year-old transparent bridge configurations.
    

By defining a strict lifecycle policy—where equipment is proactively refreshed or heavily penalized with legacy support fees—we can protect our margins, reduce burnout among our technical staff, and ensure our customers are running on stable, secure, and supportable infrastructure.