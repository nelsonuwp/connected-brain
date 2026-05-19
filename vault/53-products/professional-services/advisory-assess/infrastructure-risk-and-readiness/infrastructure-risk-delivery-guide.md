# Infrastructure Risk & Readiness Assessment -- Delivery Guide

> **For Aptum delivery teams.** How to actually execute this assessment from kickoff to findings presentation.

---

## Delivery Team Composition

| Size | Lead | Supporting Architects | Executive Sponsor | Total Aptum Hours |
| --- | --- | --- | --- | --- |
| **S** | Solution Architect | None | None | 20-30 hours |
| **M** | Solution Architect | 1 (Network or Infrastructure) | None | 50-70 hours |
| **L** | Solution Architect | 2 (Network + Infrastructure or Security) | None | 90-130 hours |
| **XL** | Solution Architect | 2-3 (Network, Infrastructure, Security) | Yes (for exec presentation) | 150-200+ hours |

**Specialist architect roles**:

- **Network Architect**: Firewall audit, network topology, switch/router EOL review
- **Infrastructure Architect**: Server hardware audit, SAN/storage review, capacity analysis
- **Security Architect**: CVE exposure mapping, firmware vulnerability review (L/XL only)

---

## Phase-by-Phase Delivery Plan

### Phase 1: Kickoff & Data Collection (Days 1-3)

**Participants**: Aptum SA + Aptum AE + Customer technical POC + Customer stakeholders

**Activities**:

1. **Kickoff meeting** (1 hour)
   - Confirm scope and objectives
   - Review timeline and milestones
   - Identify customer stakeholders for interviews
   - Confirm data access and credentials
   - Set expectations for customer time commitment
1. **Data collection request** (send within 24 hours of kickoff):
   - Existing asset inventory / CMDB export (if available)
   - Network diagrams (if available)
   - Monitoring tool access (LogicMonitor, Nagios, PRTG, etc.)
   - Ticketing system access or export (recent 6-12 months)
   - Any existing audit or compliance reports
1. **Infrastructure discovery** (if no asset inventory exists):
   - Network scanning to identify active devices
   - SNMP/WMI data collection
   - Manual inventory via management interfaces

**Tools required**:

- LogicMonitor (Aptum standard) or customer's monitoring platform
- Network scanning tools (Nmap, Qualys, or equivalent)
- Spreadsheet for asset tracking
- Access to customer ticketing system

---

### Phase 2: Technical Assessment (Days 3-10, varies by size)

**Activities**:

#### Hardware Age Audit

- Catalog all physical hardware: servers, firewalls, switches, load balancers, SANs
- Record make, model, serial number, purchase/install date
- Cross-reference against vendor EOL/EOS databases:
  - **Dell**: [Dell Product Lifecycle](https://www.dell.com/support/home/)
  - **Juniper**: [Juniper EOL Policy](https://support.juniper.net/support/eol/)
  - **Cisco**: [Cisco EOL Portal](https://www.cisco.com/c/en/us/products/eos-eol-listing.html)
- Flag all EOL, EOS (End of Support), and approaching-EOL devices (within 12 months)

#### OS Lifecycle Assessment

- Inventory all operating systems and versions across servers
- Cross-reference against vendor lifecycle databases:
  - **Microsoft**: Windows Server lifecycle dates
  - **Red Hat**: RHEL lifecycle dates
  - **Canonical**: Ubuntu LTS lifecycle dates
  - **CentOS/Debian**: community support dates
- Flag: unsupported (red), approaching EOL within 12 months (amber), supported (green)

#### Operational Risk Scoring

- Analyze ping loss patterns over the last 30-90 days (from monitoring)
- Review ticket history: volume, categories, repeat incidents, MTTR
- Calculate incident frequency per device/service
- Identify single points of failure
- Score each device/service: Critical / High / Medium / Low risk

#### Capacity & Performance Baseline (M+ only)

- CPU, memory, disk utilization trends over 30-90 days
- Storage capacity and growth rate
- Network bandwidth utilization
- Identify bottlenecks and over/under-provisioned resources

---

### Phase 3: Analysis & Report Writing (Days 8-14, varies by size)

**Activities**:

1. Compile findings into the assessment report template
1. Create prioritized remediation roadmap:
   - **Critical** (0-30 days): Active security vulnerabilities, failed/failing hardware
   - **High** (30-90 days): EOL devices with no support, unsupported OSes
   - **Medium** (90-180 days): Approaching EOL, capacity constraints
   - **Low** (180+ days): Optimization opportunities, future planning
1. Develop cost estimates for each remediation item
1. Prepare executive summary (L/XL)
1. Internal review with Aptum specialists (L/XL: also with Aptum leadership)

**Report structure**:

1. Executive Summary
1. Scope and Methodology
1. Current State Overview (inventory, topology)
1. Findings by Category:
   - Hardware EOL Status
   - OS Lifecycle Status
   - Operational Risk Assessment
   - Capacity & Performance (M+)
1. Risk Summary Matrix
1. Prioritized Remediation Roadmap
1. Cost Estimates
1. Appendices (detailed device inventory, raw data)

---

### Phase 4: Findings Presentation (Final Day)

**Participants**: Aptum SA + Aptum AE + Customer stakeholders (including executive sponsor for L/XL)

**Activities**:

1. Present findings to customer (45-90 minutes depending on size)
1. Walk through the remediation roadmap
1. Q&A
1. Discuss recommended next steps (this is where follow-on opportunities surface)
1. Deliver final report (PDF)

**Presentation tips**:

- Lead with the "so what" -- biggest risks and their business impact
- Use visuals: risk heat maps, timeline charts for EOL dates
- Don't overwhelm with data -- save detail for the appendix
- End with clear next steps and the follow-on service recommendation

---

## Timeline by Size

| Phase | S (1 week) | M (2 weeks) | L (3-4 weeks) | XL (4-6 weeks) |
| --- | --- | --- | --- | --- |
| Kickoff & data collection | Day 1-2 | Day 1-3 | Day 1-5 | Day 1-7 |
| Technical assessment | Day 2-4 | Day 3-8 | Day 5-15 | Day 7-25 |
| Analysis & report writing | Day 4-5 | Day 8-12 | Day 15-22 | Day 25-35 |
| Findings presentation | Day 5 | Day 12-14 | Day 22-25 | Day 35-40 |

---

## Tools & Access Required

| Tool | Purpose | Required For |
| --- | --- | --- |
| LogicMonitor | Performance monitoring, ping loss analysis | All sizes |
| Nmap or equivalent | Network discovery and device identification | M+ (if no asset inventory) |
| Qualys / Nessus | Vulnerability scanning (if included) | L/XL |
| Customer ticketing system | Incident history analysis | M+ |
| Vendor EOL databases | Hardware/software lifecycle lookup | All sizes |
| Excel/Google Sheets | Asset inventory compilation | All sizes |
| PowerPoint/Google Slides | Executive presentation | L/XL |

---

## Quality Checkpoints

| Checkpoint | When | Who Reviews |
| --- | --- | --- |
| Data collection complete | End of Phase 1 | SA confirms all inputs received |
| Assessment findings draft | Mid Phase 3 | SA + specialist peer review |
| Report draft complete | End of Phase 3 | SA + Aptum delivery lead review |
| Executive summary review | Before Phase 4 | Aptum leadership (XL only) |
| Final presentation rehearsal | Day before Phase 4 | SA + Aptum AE alignment call |

---

## Risk & Escalation

| Risk | Mitigation |
| --- | --- |
| Customer delays providing access/data | Set clear expectations at kickoff. Escalate to Aptum AE if access is delayed \> 3 business days. Timeline shifts accordingly. |
| Scope creep (customer adds devices/sites mid-assessment) | Refer to SOW. Additional scope = additional cost. SA flags to Aptum AE for commercial conversation. |
| Critical finding mid-assessment (active security breach, imminent failure) | Immediately notify customer and Aptum AE. Document finding. Do not wait for report completion. |
| Customer stakeholder unavailable for interviews | SA works with customer POC to reschedule. Escalate to Aptum AE if delays exceed 1 week. |

---

*Last updated: 2026-02-06*
