---
type: idea
created: 2026-03-03
status: raw
---

# Standardize Hardware Lifecycle and EOL Management

## 1. The What (The Initiative)

We are transitioning Aptum from a passive hardware host into an actively managed service provider by establishing a strict, enforceable hardware lifecycle policy. This initiative consists of two core pillars:

- **Pillar 1: Legal & Commercial Enforcement (Operationalizing Section 5.5)** We will leverage Section 5.5 (End of Life Support) of our existing Terms of Business to stop providing "free" life-support for obsolete equipment. We will implement a standardized playbook that automatically issues 30-day (TBD) EOL Notices. If a customer refuses to upgrade, we will legally void their SLAs, drop support to "as-is", and apply a mandatory **Legacy Support Surcharge** (e.g., 20-30% of MRC) to cover the excessive engineering overhead.
    
- **Pillar 2: The Source of Truth (Centralized Lifecycle Database)** We will build a Product-owned, centralized Component Lifecycle Database. This will bridge the current gap in our data architecture by mapping our billing identifiers (`fusion_id` in _dimServices_ and `component_id` in _dimComponents_) directly to vendor lifecycle dates. This system will automate 90-day proactive EOL flags and trigger Account Management workflows.
    

## 2. The Why (Why it's Important Now)

Currently, once customer hardware is fully depreciated (typically after 3 years), it remains in our data centers at a supposed "zero" equipment cost. While this looks like 100% margin on paper, it is creating massive, hidden operational debt. Fixing this addresses four critical risks:

- **Exploding OpEx Costs:** Unbillable engineering time is bleeding our margins. High-tier Network Engineers, NOC, DCOPS, and Account Managers are burning dozens of hours acting as mechanics for vintage equipment rather than building modern solutions.
    
- **SLA & Liability Risk:** We cannot honor performance guarantees when replacement parts literally do not exist. We are absorbing the liability for outages caused by 15-year-old hardware.
    
- **Severe Security Vulnerabilities:** Housing servers running obsolete operating systems (e.g., Windows Server 2008) and firewalls that haven't received patches in over 6 years introduces immense compliance and security risks to our network.
    
- **Stagnant Modernization:** Legacy hardware blocks our ability to roll out modern networking features or efficiently manage our IP space (e.g., catering to deprecated "transparent bridge" firewall configurations).
    

## 3. Context & Information to Retain

**A. The Case Study: Winston Data** Winston Data perfectly encapsulates this systemic failure. We currently manage services for them provisioned over a decade ago:

- **Juniper SSG 5 Firewall (Service 2036467):** Provisioned in 2009 (Reached End of Support in Jan 2020). Setting up a standard Site-to-Site VPN required months of back-and-forth, 2+ hours of senior engineering troubleshooting on a single call, and unintended production impacts because the 17-year-old device couldn't handle modern architectures.
    
- **Web1 Server (Service 2433647):** Provisioned in 2011. Experienced a P1 weekend outage due to a dead power supply. We had zero replacement parts. DCOPS only brought it online through the sheer luck of scavenging parts from another customer's recently deprovisioned chassis.
    

**B. The Enforcement Mechanics (Section 5.5 Playbook)** Our Terms of Business already give us the power to fix this. The enforcement steps must be standard practice:

1. **The Formal Notice:** Sends automatically. Voids the SLA and drops support to "as-is" without warranty.
    
2. **Forced Upgrade:** Mandate a transition to modern hardware (which often actually _saves_ the customer money while restoring their SLA).
    
3. **Legacy Surcharge:** If they refuse the upgrade, automatically apply an MRC surcharge to bill for the "Professional Services" time ($230/hr value) we waste troubleshooting their gear.
    
4. **Discontinuation:** Terminate the service if the security/operational risk to our network is too high.
    

**C. The Data Architecture & Lifecycle Definitions** To build the "Source of Truth" database, Product must track three critical ITAM (IT Asset Management) vendor dates against our internal IDs:

1. **End of Sale (EoSale):** The product can no longer be quoted/sold to new customers.
    
2. **End of Support (EoST):** The vendor stops providing standard tech support, bug fixes, and security patches. _Context constraint: This is the legal trigger for sending our Section 5.5 EOL Notice and voiding the SLA._
    
3. **End of Service Life (EOSL):** The vendor completely abandons the product and stops manufacturing spare parts. _Context constraint: This is the "Danger Zone." No customer should reach EOSL without paying a massive Legacy Support fee, or facing network disconnection._