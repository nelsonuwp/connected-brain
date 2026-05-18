# Security Services

Seven security products operating at different layers of the stack. They are complementary, not redundant — each addresses a distinct threat surface. A customer with MDR but no WAF has endpoint protection and threat hunting but no application-layer traffic inspection. A customer with a WAF but no MDR has L7 filtering but no human analysts investigating threats.

## Aptum Managed Firewall (Juniper SRX)

Security policy management, rule changes, and compliance auditing for Juniper SRX physical firewalls and virtual firewall instances. This is the policy layer on top of the device — the physical device and connectivity are Networking's responsibility. At Reactive tier, Aptum runs automated config backup, health monitoring, policy violation alerting, and Service Desk handles L2 ticket operations. At Proactive tier, Managed Cloud owns security policy, handles complex rule changes, and conducts compliance auditing. Owners: Managed Cloud (policy); Networking (physical device).

## Aptum Endpoint Protection (EDR)

AV and endpoint detection and response on customer servers. Not MDR — EDR is automated endpoint protection; MDR adds human SOC analysts on top. At Reactive tier, the agent is deployed, automated quarantine is active, and alert status is reported to the customer. At Proactive tier, Managed Cloud triages alerts, investigates threats, coordinates response, and configures exclusions and policies. Agent options: Microsoft Defender for Business (approximately $4 CAD/endpoint), CrowdStrike Falcon Go (approximately $7 to $10 CAD/endpoint), SentinelOne (approximately $6 to $9 CAD/endpoint). Owner: Managed Cloud.

## Aptum WAF

HTTP and HTTPS application-layer traffic inspection with OWASP rule enforcement and custom security policies. Layer 7 only — this is not DDoS protection (volumetric L3/L4) and not a network firewall. At Reactive tier, the WAF engine runs with automated OWASP rule updates and blocks known threats. At Proactive tier, Managed Cloud tunes policies, creates custom rules, manages false positives, and conducts PCI and compliance reviews. Tooling options: Imperva (Incapsula), Cloudflare WAF. Owner: Managed Cloud.

## Aptum DDoS Protection

Always-on volumetric attack scrubbing at the network edge (L3/L4). Not WAF — DDoS protection handles volumetric network-layer attacks, while WAF handles application-layer (L7) threats. At Reactive tier, BGP-level edge protection is always on, with automated attack detection, scrubbing activation, and attack event reporting. At Proactive tier, Managed Cloud coordinates attack response, conducts post-attack reviews, and configures enhanced scrubbing policies for persistent threats. Owners: Networking (physical edge protection); Managed Cloud (scrubbing management and customer coordination).

## Aptum MDR (Alert Logic)

24/7 threat monitoring, SOC-as-a-service, and compliance reporting via Alert Logic. Not EDR — MDR is a full SOC function with human analysts actively investigating and hunting threats. EDR feeds into MDR but does not replace it. At Reactive tier, Alert Logic automated detection and alerting runs continuously; alerts are surfaced to Service Desk and the customer. At Proactive tier, SOC analysts actively investigate threats, manage escalations, produce compliance evidence, and conduct proactive threat hunting. Status: IN DEVELOPMENT. Alert Logic timeline and commercial model are being finalized. Owner: Managed Cloud plus Alert Logic SOC partner.

## Aptum Vulnerability Scanning

Scheduled automated vulnerability scans with remediation tracking and posture scoring. Not penetration testing — automated scanning identifies known CVEs from public databases; pen testing involves skilled testers actively attempting exploitation. At Reactive tier, scans are scheduled and executed automatically, posture scoring is generated, and reports are delivered to the customer. At Proactive tier, Managed Cloud reviews results, prioritizes remediation by risk, provides guidance, and tracks remediation progress. Tooling options: Qualys VMDR, Tenable.io, Rapid7 InsightVM. Status: not yet built. Owner: Managed Cloud.

## Aptum Compliance Reporting

SOC 2, PCI-DSS, and HIPAA evidence collection and ongoing reporting using Aptum's SOC 2 Type II as the operational foundation. Not an independent security audit — ongoing evidence documentation and reporting. Proactive tier only. At Proactive tier, Managed Cloud curates evidence packages, identifies gaps, and prepares customer-facing compliance reports. Commercial model: PS engagement for initial setup; Managed Cloud handles ongoing reporting. Status: not yet built as a managed addon; PS-led today. Owner: Managed Cloud.
