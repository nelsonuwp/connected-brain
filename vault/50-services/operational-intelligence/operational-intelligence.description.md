# Operational Intelligence

**Service Manager:** Jorge Quintero
**Function:** Enablement
**Lifecycle:** Discovery
**Confluence Link**: [Operations Intelligence Service Description](https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045223434/Operations+Intelligence)

> We make the org's data usable. Every team generates operational signals. We turn those signals into decisions.

---

## Accountable For

- Data pipeline design and build across all services
- Unified customer view: ticket health, service footprint, consumption patterns
- Metrics infrastructure for all service managers
- Operational dashboards for management reporting
- Financial data accuracy support — cost center validation and correction
- Monitoring platform consolidation (the two-Zabbix problem — see below)

---

## Problems We Solve

- Service managers are making decisions without reliable data
- Two Zabbix systems create inconsistent alert routing and the risk of duplicate tickets
- No unified customer view means hybrid customer health is invisible to anyone
- Cost misallocations like the MCP/Service Desk issue go undetected without a cross-service data layer
- PS engagement profitability cannot be measured because costs are not tracked per engagement
- Management cannot see cross-service performance without manually compiling from multiple sources

---

## Products and Services Supported

This is a pure internal enablement function. No external customer-facing product.

- Data pipelines from: JSM, Zabbix (both instances), Ocean, financial systems
- Operational dashboards per service manager
- Unified customer health view (foundation for the CEM function when built)
- Financial accuracy reporting: cost center validation, per-team margin visibility
- Alert schema design and routing logic for consolidated monitoring

---

## What This Team Does NOT Do

- Own source data — each service team owns their operational data; OI makes it accessible and usable
- Replace Finance reporting — this is operational intelligence, not financial accounting
- Customer-facing reporting or portal development — that is a product decision
- IT infrastructure management — that is IT Operations & Engineering
- Make tooling decisions unilaterally — see ownership question below

---

## On the Two-Zabbix Problem

### Who Owns This

There are two distinct responsibilities:

**VP of Operations owns the decision:** Consolidation to a single monitoring platform requires a mandate that overrides each team's preference for their current tool. Ben, Andrei, and Jason each have reasons to prefer what they have. Without a VP-level mandate, this stays fragmented indefinitely. The decision is not Jorge's to make.

**Operational Intelligence owns the execution:** Once the decision is made, Jorge's team designs the unified alert schema, builds the routing rules, manages the migration plan, and validates that all alert coverage is preserved. This is technical work that sits naturally in OI as the data layer owner.

### Target State
```
Single monitoring platform (Zabbix consolidated or replacement)
        ↓
Normalized alert schema:
  Hardware health alerts → Service Desk queue
  Network alerts → Network queue
  Cloud platform alerts → Managed Cloud queue
  OS/application alerts → Service Desk queue → Managed Cloud if cloud
        ↓
Single routing ruleset into JSM
        ↓
One view per customer across all alert types
```

---

## Tooling Ownership — Broader Question

The org currently has no explicit owner for the operational tooling stack. This affects monitoring, automation, and service management tooling:

| Tool | Current Perceived Owner | Gap |
|---|---|---|
| JSM / Jira | IT | IT owns the platform; no one owns the operational configuration (routing rules, SLA clocks, automation) |
| Zabbix (internal) | Unclear | No named owner |
| Zabbix (customer-facing) | Unclear | No named owner |
| Datadog | Managed Cloud (Andrei) | Used by MC team; broader integration with OI data layer undefined |
| LogicMonitor | Unclear | Owner and integration path undefined |
| Ansible / automation playbooks | Compute Platforms (Martin) | Operational tooling but also a shared infrastructure asset |

### Recommended Ownership Model
- **IT owns the platform** (licensing, access management, corporate SSO integration, uptime of the tool itself)
- **Operational Intelligence owns the monitoring stack decisions** (which tools, how they integrate, what the data model looks like, consolidated alert schema)
- **Each operational team owns their configuration** within the agreed platform (what they monitor, their thresholds, their runbooks)

This model means Jorge's team is the decision-maker for the monitoring stack — not as an IT function but as the org's data layer owner. The monitoring stack *is* the source of operational data. Whoever owns the data layer should own the tools that generate it.

---

## Financial Model

### Revenue Touch
- Pure cost center — no direct revenue
- Value is indirect: better decisions, faster issue detection, accurate margin visibility
- Enabling correct cost allocation has already recovered a material margin misstatement (MCP correction: ~$466K swing in reported gross margin)

### Direct Cost Driver
- Jorge plus team (Discovery phase — team size TBD)
- Data infrastructure and tooling costs
- Investment phase: ROI realized through margin improvement, churn prevention, and operational efficiency

### Margin Impact (Indirect)
| Value Driver | Estimated Impact |
|---|---|
| 1% churn reduction on $13.5M revenue | ~$135K recovered |
| MCP cost allocation correction already completed | ~$466K margin swing |
| PS engagement profitability visibility | Enables higher-margin project selection |
| Unified monitoring → faster incident resolution | SLA breach prevention |

### How We Are Measured
| Metric | Target |
|---|---|
| Data pipeline availability | To be defined |
| Data freshness / latency | To be defined |
| Service coverage (active pipelines) | To be defined |
| Data accuracy vs. source systems | To be defined |
| Monitoring consolidation progress | Milestone-based |

---

## Key Dependencies

| Dependency | Direction | Notes |
|---|---|---|
| All operational services | Inbound data | Every service is a data source |
| Finance | Lateral | Cost center accuracy and financial data validation |
| IT Operations & Engineering | Lateral | Tooling platform access and integration |
| VP of Operations | Inbound mandate | Monitoring consolidation and tooling decisions require VP mandate to override team preferences |

---

## Open Questions / Flags

- **Acceleration out of Discovery:** Every month in Discovery is another month of decisions made without data. This is the highest-leverage investment in the org at this stage. What does OI need to move to Alpha?
- **Team size:** Discovery phase means team size is TBD. The scope (pipelines from 8 services, unified monitoring, customer health view, financial accuracy) is significant for an org of this scale.
- **CEM dependency:** The Customer Experience Management function, when built, is directly dependent on OI providing the customer health data layer. CEM cannot operate without OI being operational first.
