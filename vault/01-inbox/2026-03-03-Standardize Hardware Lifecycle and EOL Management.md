---
type: idea
created: 2026-03-03
status: raw
---
# Standardize Hardware Lifecycle and EOL Management
## 1. The What (The Initiative)

We are transitioning Aptum from a passive hardware host into an actively managed service provider by establishing a strict, enforceable hardware lifecycle policy. This initiative consists of two core pillars that the organization needs to define and implement:

- **Pillar 1: Define & Implement Commercial Enforcement (Operationalizing Section 5.5)** We already have the legal framework in Section 5.5 of our Terms of Business to stop providing "free" life-support for obsolete equipment. What we lack are the business rules to execute it. This initiative will align Product, Support, Legal, and Account Management to figure out and define a standardized enforcement playbook. Key deliverables for the organization to determine include:
    
    - **The Notification Playbook:** Defining the exact automated workflows, communication templates, and timelines (e.g., a standard 30-day EOL Notice).
        
    - **Liability & Support:** Standardizing the procedures for officially voiding SLAs and dropping support to "as-is" for non-compliant hardware.
        
    - **The "Legacy Support Surcharge":** Determining the appropriate pricing adjustment legally permitted under Section 5.5 to accurately cover excessive engineering overhead (e.g., discussing a 20-30% MRC surcharge to offset unbillable professional services time).
        
- **Pillar 2: The Source of Truth (Centralized Lifecycle Database)** To execute Pillar 1 at scale, we must discuss and build the internal infrastructure. We propose the creation of a Product-owned, centralized Component Lifecycle Database. This will bridge the current gap in our data architecture by mapping our billing identifiers (`fusion_id` in _dimServices_ and `component_id` in _dimComponents_) directly to vendor lifecycle dates. Defining this system will allow us to automate proactive 90-day EOL flags and trigger Account Management workflows.
    

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
    

**B. The Enforcement Mechanics (Section 5.5 Playbook)** Our Terms of Business already give us the power to fix this. The enforcement steps to be defined by the working group should cover:

1. **The Formal Notice:** Sending automated notices to void SLAs and drop support to "as-is" without warranty.
    
2. **Forced Upgrade:** Mandating a transition to modern hardware (which often actually _saves_ the customer money while restoring their SLA).
    
3. **Legacy Surcharge:** If they refuse the upgrade, applying an agreed-upon MRC surcharge to bill for the "Professional Services" time ($230/hr value) we waste troubleshooting their gear.
    
4. **Discontinuation:** Terminating the service if the security/operational risk to our network is too high.
    

**C. The Data Architecture & Lifecycle Definitions** To build the "Source of Truth" database, Product must track three critical ITAM (IT Asset Management) vendor dates against our internal IDs:

1. **End of Sale (EoSale):** The product can no longer be quoted/sold to new customers.
    
2. **End of Support (EoST):** The vendor stops providing standard tech support, bug fixes, and security patches. _Context constraint: This is the legal trigger for sending our Section 5.5 EOL Notice and voiding the SLA._
    
3. **End of Service Life (EOSL):** The vendor completely abandons the product and stops manufacturing spare parts. _Context constraint: This is the "Danger Zone." No customer should reach EOSL without paying a massive Legacy Support fee, or facing network disconnection._
    

## 4. Contractual Context (Verbatim)

**5.5. End of Life Support:**

When a necessary component of the Services, including hardware, software, licensing, etc. (each a **“Service Component”**) is for any reason no longer supported (including software updates and patching) by Aptum or the applicable third-party supplier (the **“Supplier”**), or the Supplier discontinues or adversely alters the program or policy under which it makes a Service Component available, Aptum will identify that Service Component to the Customer as being “End-of-Life” (each, an **“EOL Product”**).

Once the Customer has been notified by Aptum in writing of the EOL Product (**“EOL Product Notice”**), Aptum may, at its discretion do the following:

**(a) If the EOL Product is owned and/or operated by Aptum in connection with the Service**, Aptum may:

- **(i)** Discontinue the Service or affected part thereof upon thirty (30) days written notice to the Customer; or
    
- **(ii)** Replace the EOL Product with an alternative Service Component and pass-through to the Customer any associated cost increase therefor as a one-time Fee or as an increase to the monthly Fees of the Services for the remainder of the Term; or
    

**(b) If the EOL Product is owned and/or operated by Customer in connection with the Service**, Aptum may require the Customer to replace EOL Product within thirty (30) days after written notice to the Customer or as otherwise agreed to the Parties in writing. After the date the EOL Product Notice is provided to the Customer and for any duration thereafter that such EOL Product continues to be used by the Customer in connection with the Services for any reason:

- **(i)** Aptum’s Service Level Agreements and performance guarantees will cease to apply to the Service;
    
- **(ii)** Aptum may only be able to provide limited support with respect to the EOL Product and to the extent that such support is provided, it will be done so on an “as-is” basis and without warranty of any kind;
    
- **(iii)** Aptum will not be liable to Customer or any other User for any loss or damage that may be suffered from any impact to the Services arising in connection with the EOL Product even if Aptum consented to the Customer’s continued use of such EOL product; and
    
- **(iv)** Aptum may, once per calendar year, conduct a pricing review and adjust the monthly Fees of the Services in respect of the EOL Product to account for the additional cost to Aptum associated with provisioning of the Services during the Customer’s continued use of the EOL Product.