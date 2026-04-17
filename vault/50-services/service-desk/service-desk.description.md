# Service Desk / NOC

**Service Manager:** Jason Auer
**Team Size:** ~17 people
**Function:** Operations
**Lifecycle:** Live
**Confluence Link**: [Service Desk Service Description](https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045223425/Service+Desk+NOC)

> We are the first call for every managed customer. We own Day 2 operations -- and what Day 2 means is different by product. Dedicated Server customers get it included. Private Cloud customers get hypervisor management included. Everyone else chooses what they need. The ticket stays with us until it is closed.

---

## Accountable For

- Day 2 operations for all dedicated and managed hosting customers -- scope varies by product type (see Day 2 Operations by Product below)
- First response on all inbound tickets -- customer-submitted and monitoring-generated
- Infrastructure-layer incident ownership (L2/L3)
- Hardware health alert receipt and routing to Data Center Ops for physical remediation
- Hyperscaler and cloud platform triage, escalation to Managed Cloud
- SLA/SLO compliance across all managed customers by priority level
- Customer portal and real-time ticket status visibility
- Shift coverage across NA and UK time zones (3 shifts, including 2-person graveyard)
- L3 resource contribution to PS engagements (with SM approval)
- **Private Cloud hypervisor layer management** -- Service Desk owns Day 2 operations at the VMware ESXi and Proxmox hypervisor layer for all Private Cloud customers. This includes hypervisor host health, vCenter management, storage management, and monitoring at the platform level. Compute Platforms provides the runbooks and standards; Service Desk executes them.
- **Internal infrastructure operations for IaaS cluster nodes** -- the dedicated servers that underpin Shared Cluster and Dedicated Cluster are Aptum-owned hardware. Service Desk monitors their hardware health as an internal operational function, the same way it does for customer-facing Dedicated Servers.

---

## Problems We Solve

- Customers need someone available 24/7 when things break
- Hardware faults need to be caught and resolved before the customer notices — the car needs an oil change, not the driver
- Cloud incidents need to reach the right technical team without customer involvement
- Customers with hybrid environments (dedicated + cloud) need one number, one owner
- SLA breach risk needs proactive management, not reactive response

---

## Products and Services Supported

- Managed Hosting: ~2,949 services — primary operational home
- Dedicated Hosting: ~1,620 services — day 2 operations
- Physical server estate: ~2,526 servers across Dell PE R-660XS, Pro Series 5.0, Advanced Series 5.0, and full catalog
- Firewall management: 417 Juniper SRX devices (L2 ops; policy escalation to Managed Cloud)
- Managed backup: Veeam
- OS support: Debian 12.x, Windows Server (2016/2019/2022), Ubuntu, CentOS, RHEL, Alma Linux, Rocky Linux
- Hardware health monitoring: power supply, CMOS, disk health, temperature, physical sensors
- Private Cloud environments (VMware ESXi / Proxmox): ~126 hypervisor hosts -- Service Desk owns Day 2 management of the hypervisor layer. Compute Platforms provides runbooks and configuration standards; Service Desk executes them. Escalation to Compute Platforms is for genuine L3 issues beyond runbook scope -- not for routine operations.

---

## What This Team Does NOT Do

- Cloud platform operations above the OS layer — that is Managed Cloud
- Physical hardware remediation — that is Data Center Ops (tickets routed there; DC Ops dispatches the fix)
- Network infrastructure configuration — that is Network
- Provisioning new environments — that is Compute Platforms
- Own the customer relationship — that is HSDM
- Make tickets unassigned when status changes — tickets stay assigned to the owning engineer at all times

---

## Operating Model — Ticket Ownership

**Tickets are never unassigned.** Ownership does not transfer to the pool when status changes to Waiting on Customer, when a shift ends, or when an engineer goes on leave. "If someone leaves for the night the ticket will go unattended" is a coverage gap problem, not a ticket ownership problem. Coverage gaps are solved with scheduling and shift handoff — not by removing ownership.

### Assignment Model
Every customer is assigned to a named primary engineer. New tickets from that customer route to their primary engineer if on shift, or to a named pod colleague if off shift.

Customers are organized into three pods (~140 customers each):
- Each pod has engineers distributed across shifts
- Two graveyard engineers cover all pods overnight — they are caretakers, not owners

### Graveyard Shift Protocol
The two graveyard engineers have a specific and bounded job:
- **Monitor** — watch for P1/P2 tickets across all customers
- **Stabilize** — stop the bleeding; do not resolve unless straightforward
- **Document** — structured note on every ticket touched before shift end
- **Escalate** — wake the on-call primary engineer for genuine criticals

### Shift Handoff
At shift end, graveyard engineers update every touched ticket with a structured handoff note: what happened, what was done, what is pending. JSM automation flags all graveyard-touched tickets at the top of the primary owner's queue at shift start.

### JSM Configuration
- Customer organization mapped to pod in JSM
- Assignee automation based on shift schedule (Opsgenie integration)
- SLA clock runs regardless of status or assignee — does not pause for shift changes
- Waiting on Customer status: ticket stays assigned; JSM automation sends follow-up reminder to assignee after defined interval

---

## Day 2 Operations by Product

The scope of Service Desk's managed layer is not uniform across products. Each product has a defined baseline and a defined set of optional add-ons.

| Product | Service Desk Baseline | Notes |
|---|---|---|
| **Dedicated Server** | **Mandatory -- included in every engagement** | 24/7 Zabbix monitoring, hardware health alerting, baseline OS management. This layer is not optional. Every Dedicated Server customer receives it. **This is a change from prior operations and must be explicitly communicated during onboarding and in customer-facing documentation.** |
| **Shared Cluster (VPC)** | Internal cluster infrastructure monitoring | Service Desk monitors the underlying cluster nodes as an internal operational function. Customer-facing managed services are purchased separately. |
| **Dedicated Cluster** | Internal cluster infrastructure monitoring | Same as Shared Cluster. Service Desk monitors Aptum's cluster hardware internally. Customer Day 2 is optional. |
| **Private Cloud (VMware/Proxmox)** | Hypervisor layer included | Service Desk owns the hypervisor: ESXi hosts, vCenter, storage management per the service plan, and platform-level monitoring. The guest OS and application layer above the hypervisor are optional Managed Cloud add-ons. |
| **Colocation** | Not included by default | Colo customers own their hardware and the management responsibility above the physical facility layer. Service Desk monitoring and management are available as add-ons. |
| **Connectivity** | Network monitoring included | 99.999% uptime SLA on all Aptum-managed connectivity. Network incidents route through Service Desk to Network for resolution. |

---

## Hardware Health Alert Flow

Customers renting dedicated environments are not responsible for underlying hardware health. That is Aptum's obligation.

```
Zabbix alert fires (CMOS, PSU, disk, temperature, physical sensor)
        ↓
Service Desk receives → creates ticket → remains assigned to Service Desk engineer
        ↓
Ticket dispatched to Data Center Ops for physical remediation
        ↓
DC Ops fixes hardware → updates ticket
        ↓
Service Desk closes ticket → customer sees restored service
Customer never interacts with the physical layer
```

---

## Financial Model

### Revenue Touch
- Enables Legacy Managed: ~$514K YTD (100% gross margin)
- Enables Foundation: ~$128K YTD (100% gross margin)
- Enables all Managed and Dedicated Hosting MRC across ~4,569 services
- ~17 of 25 people previously misallocated to Managed Cloud cost center belong here — correction in progress

### Direct Cost Driver
- ~17 people — largest team in the org, appropriate for ~4,569 services supported
- Labor distributed across 3 shifts including 2-person graveyard
- Previously misallocated to the Managed Cloud cost center — being corrected

### Margin Profile
- Legacy Managed and Foundation run at 100% gross margin; Service Desk labor is the primary COGS
- Graveyard coverage model (2 people vs. full shift) is the key overnight cost efficiency lever
- SLA breach carries financial liability — margin erosion risk on SLA-governed contracts

### How We Are Measured
| Metric | Target |
|---|---|
| Ticket acknowledgement within SLA/SLO | By priority tier — to be defined |
| MTTA | To be defined |
| MTTR | To be defined |
| Unplanned downtime across managed estate | To be defined |
| Escalation routing accuracy | To be defined |
| Customer satisfaction score | To be defined |
| Total capacity (hours) | Monthly |
| Contractual commitment (hours) | Monthly |
| Overages (billable and non-billable) | Monthly |

---

## Key Dependencies

| Dependency | Direction | Notes |
|---|---|---|
| Managed Cloud | Outbound escalation | Hyperscaler and cloud platform triage |
| Compute Platforms | Outbound escalation | L3 for deep technical issues on built environments |
| Data Center Ops | Outbound dispatch | Physical hardware remediation |
| Network | Outbound escalation | Network-layer incidents |
| HSDM | Lateral | HSDM owns the customer; Service Desk owns the ticket |
| Operational Intelligence | Inbound | Unified monitoring, ticket health, customer view |

---

## Open Questions / Flags

- **UK coverage:** ~1,091 services in Portsmouth/UK. Whether UK customers receive adequate response during UK business hours from a North American NOC needs explicit confirmation. A UK team lead or UK-based headcount is likely required.
- **Two Zabbix systems:** One internal-facing, one customer-facing. Consolidation decision sits with VP of Operations; execution with Operational Intelligence.
- **Tooling ownership:** Who owns the Zabbix configuration, thresholds, and routing schema is an open organizational question pending the broader tooling ownership decision.
- **Mandatory managed layer activation for Dedicated Server:** The decision to make the managed layer mandatory for all Dedicated Server customers represents a change from how some accounts have historically been operated. A transition plan is needed for any Dedicated Server customers currently on a no-management model to bring them into compliance with the baseline standard.
