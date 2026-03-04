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

## Proposed Solution: The Section 5.5 Enforcement Strategy

We do not need to rewrite our contracts; we simply need to operationalize **Section 5.5 (End of Life Support)** of our Terms of Business. This clause provides a clear, legally sound framework to transition from passive hardware hosts back to actively managed service providers.

We propose launching a standardized "EOL Hardware Lifecycle Program" leveraging the explicit rights granted to us in Section 5.5. For any customer running EOL equipment (like Winston Data), we will implement a strict four-step enforcement playbook:

**1. The Formal EOL Notice (Triggering Section 5.5 Liability Protections)** Currently, Account Managers are pleading with customers to upgrade. Instead, we must send a formal, automated "EOL Product Notice." The moment this notice is sent, we immediately trigger the protections under **Section 5.5(b)**:

- Our SLAs and performance guarantees for that service are legally voided.
    
- Support drops to a limited, "as-is" basis with no warranty.
    
- Aptum is officially shielded from liability for any downtime (e.g., when their 15-year-old server loses a power supply and we have no parts).
    

**2. The Forced Upgrade & Cost Pass-Through (Leveraging Section 5.5.a)** Under Section 5.5(a)(ii), if Aptum owns/operates the equipment, we have the right to replace the EOL Product with an alternative and pass the cost through to the customer.

- _Winston Data Application:_ We will mandate the transition to the drafted hardware refresh (moving from the SSG 5 to the SRX 340, and upgrading the Web1/Web2 servers). Ironically, as demonstrated in the Winston Data quote, upgrading to modern, supported hardware will actually _save_ the customer $712.44 per month while returning them to a supported SLA.
    

**3. The "Legacy Support Fee" (Leveraging Section 5.5.b.iv)** If a customer absolutely refuses to upgrade and insists on keeping their EOL equipment, we must stop absorbing the cost of our engineering time. Section 5.5(b)(iv) gives us the right to conduct an annual pricing review and adjust monthly fees to account for the additional support costs.

- _Actionable Policy:_ If a customer ignores the 30-day EOL Notice, a standard **Legacy Support Surcharge** (e.g., 20-30% of MRC) will be automatically applied to their bill. This accurately reflects the "Professional Services" time (currently valued at $230/hour) that our senior engineers waste troubleshooting antiquated gear.
    

**4. Service Discontinuation (The Last Resort - Section 5.5.a.i)** If the EOL hardware poses a severe security risk to the Aptum network, or the customer refuses the upgrade and the legacy tax, we invoke our right to terminate the affected service with 30 days' written notice. We must be willing to fire customers who pose a disproportionate operational and security risk to our infrastructure.

## Immediate Action Plan

To resolve the Winston Data situation and roll this out company-wide, we propose the following steps:

1. **Audit:** Generate a report of all active services running on hardware/software that is 3+ years past its vendor End-of-Support date (e.g., SSG Firewalls, Windows 2008 OS).
    
2. **Standardize Communication:** Legal and Marketing to draft a standardized "Section 5.5 EOL Product Notice" template.
    
3. **Execute the Winston Data Pilot:** * Send Winston Data the formal Section 5.5 Notice.
    
    - Inform them that as of the P1 outage on Web1, their SLA is officially voided and we hold no liability for future hardware failures.
        
    - Present the hardware refresh quote as the _only_ path to restoring their SLA.
        
    - Inform them that failure to accept the refresh within 30 days will result in an automatic Legacy Support Surcharge being applied to their monthly invoice to cover our Network Engineering overhead.