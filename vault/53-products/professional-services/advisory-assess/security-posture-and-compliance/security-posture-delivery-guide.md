# Security Posture & Compliance Assessment -- Delivery Guide

> **For Aptum delivery teams.** How to execute this assessment from kickoff to findings presentation.

---

## Delivery Team Composition

| Size | Lead | Supporting Architects | Executive Sponsor | Total Aptum Hours |
|------|------|----------------------|-------------------|------------------|
| **S** | Solution Architect | None | None | 20-30 hours |
| **M** | Solution Architect | 1 (Security or Network Architect) | None | 50-75 hours |
| **L** | Solution Architect | 2 (Security + Network Architect) | None | 100-150 hours |
| **XL** | Solution Architect | 2-3 (Security, Network, Infrastructure) | Yes | 170-250+ hours |

**Specialist architect roles**:
- **Security Architect**: Vulnerability analysis, pen testing, compliance gap analysis, remediation design
- **Network Architect**: Firewall rule audit, network segmentation review, attack surface analysis
- **Infrastructure Architect**: EOL hardware assessment, OS lifecycle review (overlap with Infra Risk)

---

## Phase-by-Phase Delivery Plan

### Phase 1: Kickoff & Authorization (Days 1-3)

**Activities**:

1. **Kickoff meeting** (1 hour)
   - Confirm scope, compliance frameworks in play, and devices in scope
   - Review timeline and get stakeholder buy-in
   - Discuss penetration testing scope and rules of engagement (L/XL)
   - Confirm data access and authorization

2. **Obtain written authorization**
   - Scanning authorization from customer (all sizes)
   - Penetration testing authorization with defined scope, rules of engagement, and testing windows (L/XL)
   - Notify customer IT team of testing schedule

3. **Data collection request**:
   - Existing asset inventory / network diagrams
   - Prior audit reports or compliance assessments
   - Firewall configurations (for rule audit)
   - Current security tooling inventory
   - Incident history (if available)

**CRITICAL**: Never begin scanning or pen testing without written authorization.

---

### Phase 2: Vulnerability Assessment & EOL Inventory (Days 3-8)

**Activities**:

#### EOL / End-of-Support Inventory
- Catalog all hardware with make, model, firmware version
- Cross-reference against vendor EOL databases
- Flag all devices with known CVEs (especially high/critical severity)
- Specific items to check:
  - **Firewalls**: Juniper SRX 300 series (extremely common in our customer base), Cisco ASA, Palo Alto
  - **Operating systems**: CentOS 5/7, RHEL 7, Windows Server 2008 R2/2012 R2, Debian 8
  - **Network gear**: Switches, load balancers, wireless controllers

#### Automated Vulnerability Scanning
- Run authenticated vulnerability scan across all in-scope devices
- Scan types:
  - Network vulnerability scan (all sizes)
  - OS vulnerability scan (all sizes)
  - Web application scan (if public-facing, M+)
- Categorize findings by severity: Critical / High / Medium / Low / Informational
- Map findings to CVE database entries

**Tools**:
- Qualys, Nessus, or OpenVAS for vulnerability scanning
- Vendor EOL databases (Juniper, Cisco, Dell, Microsoft, Red Hat)
- NVD (National Vulnerability Database) for CVE correlation

---

### Phase 3: Firewall & Policy Audit (Days 6-12, M+)

**Activities**:

#### Firewall Rule Review
- Export and analyze firewall rule sets
- Identify overly permissive rules (any/any, broad source/destination)
- Flag unused or redundant rules
- Check for proper segmentation between zones
- Review NAT configurations
- Assess logging and alerting configuration

#### Security Policy Assessment
- Review access control policies
- Assess password/authentication policies
- Review change management processes for security configs
- Evaluate backup and recovery procedures for security infrastructure

---

### Phase 4: Compliance Gap Analysis (Days 8-18, M+)

**Activities** (framework-specific):

#### SOC 2
- Review controls against Trust Service Criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy)
- Identify gaps in evidence and documentation
- Assess monitoring and alerting against SOC 2 requirements

#### HIPAA
- Review technical safeguards: access controls, audit controls, integrity controls, transmission security
- Assess physical safeguards as they relate to infrastructure
- Review administrative safeguards related to IT operations
- Evaluate BAA coverage for hosting providers

#### PCI-DSS
- Review network segmentation and cardholder data environment
- Assess encryption for data at rest and in transit
- Review access control and authentication
- Evaluate vulnerability management program

#### For each framework:
- Create gap matrix: requirement | current state | gap | remediation effort
- Prioritize gaps by severity and audit impact

---

### Phase 5: Penetration Testing (Days 10-22, L/XL only)

**Activities**:

#### Scope Definition (confirmed in Phase 1)
- External pen test: public-facing IPs, websites, APIs
- Internal pen test: from within the network (if authorized)
- Rules of engagement: testing windows, out-of-bounds systems, escalation procedures

#### Testing Execution
- Reconnaissance and enumeration
- Vulnerability exploitation (within authorized scope)
- Privilege escalation attempts
- Lateral movement testing
- Data exfiltration simulation (if authorized)

#### Reporting
- Separate pen test report with:
  - Methodology
  - Findings with evidence (screenshots, logs)
  - Severity ratings
  - Remediation recommendations
  - Retest recommendations

**CRITICAL**: Immediately notify customer of any active compromise or critical exploitation discovered during testing.

---

### Phase 6: Report Writing & Remediation Roadmap (Days 15-25)

**Activities**:

1. **Compile all findings** into the assessment report
2. **Create remediation priority matrix**:
   - **Critical** (0-30 days): Active vulnerabilities being exploited in the wild, critical CVEs on public-facing systems
   - **High** (30-90 days): EOL devices with known high-severity CVEs, major compliance gaps
   - **Medium** (90-180 days): Approaching EOL, policy gaps, minor compliance findings
   - **Low** (180+ days): Best practice improvements, optimization
3. **Estimate cost and effort** for each remediation item
4. **Prepare executive risk briefing** (L/XL)
5. **Internal review** with Aptum security team

**Report structure**:
1. Executive Summary (risk posture score, critical findings count)
2. Scope and Methodology
3. Findings by Category:
   - EOL/EOS Inventory & CVE Exposure
   - Vulnerability Scan Results
   - Firewall & Policy Audit (M+)
   - Compliance Gap Analysis (M+)
   - Penetration Testing Results (L/XL -- may be separate report)
4. Risk Summary Matrix (heat map)
5. Prioritized Remediation Roadmap
6. Cost & Effort Estimates
7. Appendices

---

### Phase 7: Findings Presentation (Final Days)

**Participants**: Aptum SA + Aptum AE + Customer stakeholders (CISO/exec for L/XL)

**Presentation structure** (45-90 minutes):
1. Overall risk posture: "Here's where you stand"
2. Critical findings walkthrough (top 5-10)
3. Compliance status (if applicable)
4. Remediation roadmap: what to fix first, what it costs
5. Recommended next steps (managed services, remediation project)
6. Q&A

**Presentation tips**:
- Lead with the business impact, not the technical details
- Use the risk heat map as the anchor visual
- For regulated industries, frame findings in terms of audit readiness
- For non-regulated, frame in terms of breach probability and cost

---

## Timeline by Size

| Phase | S (1 wk) | M (2 wk) | L (3-4 wk) | XL (4-6 wk) |
|-------|---------|---------|-----------|------------|
| Kickoff & authorization | Day 1-2 | Day 1-3 | Day 1-3 | Day 1-5 |
| Vuln assessment & EOL | Day 2-4 | Day 3-7 | Day 3-10 | Day 3-12 |
| Firewall & policy audit | -- | Day 6-10 | Day 6-14 | Day 6-16 |
| Compliance gap analysis | -- | Day 8-12 | Day 8-18 | Day 8-22 |
| Penetration testing | -- | -- | Day 10-20 | Day 10-25 |
| Report & remediation roadmap | Day 4-5 | Day 10-13 | Day 18-25 | Day 22-32 |
| Findings presentation | Day 5 | Day 13-14 | Day 25-28 | Day 32-38 |

---

## Tools & Access Required

| Tool | Purpose | Required For |
|------|---------|-------------|
| Qualys / Nessus / OpenVAS | Vulnerability scanning | All sizes |
| Vendor EOL databases | Hardware/software lifecycle check | All sizes |
| NVD / CVE database | Vulnerability correlation | All sizes |
| Firewall management console | Rule export and analysis | M+ |
| Burp Suite / OWASP ZAP | Web application testing | L/XL (if web apps in scope) |
| Metasploit / manual tools | Penetration testing | L/XL |
| Compliance framework documentation | Gap analysis reference | M+ |

---

## Quality Checkpoints

| Checkpoint | When | Who Reviews |
|-----------|------|------------|
| Scanning authorization received | Before Phase 2 | SA confirms with customer |
| Vulnerability scan complete | End of Phase 2 | SA + Security Architect review |
| Compliance gap matrix draft | Mid Phase 4 | SA + Security Architect |
| Pen test complete (L/XL) | End of Phase 5 | Security Architect review |
| Report draft | End of Phase 6 | SA + Aptum security team |
| Presentation rehearsal | Day before Phase 7 | SA + Aptum AE |

---

## Risk & Escalation

| Risk | Mitigation |
|------|-----------|
| Customer delays authorization | Cannot proceed without written auth. Escalate to Aptum AE. Timeline shifts. |
| Critical vulnerability found during scanning | Immediate notification to customer. Document in report. |
| Active compromise discovered during pen testing | **STOP testing immediately.** Notify customer CISO/IT lead and Aptum AE. Follow incident response procedures. |
| Scope of pen test unclear | Confirm rules of engagement in writing before ANY testing begins. |
| Customer pushback on findings severity | Refer to CVE database, vendor advisories, and framework requirements. Findings are data-driven. |

---

*Last updated: 2026-02-06*
