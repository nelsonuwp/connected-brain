# Data Center Ops

**Service Manager:** George Revie
**Function:** Operations
**Lifecycle:** Live
**Confluence Link**: [Data Center Service Description](https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045747729/Data+Center+Operations)

> We own the physical layer. The building, the power, the hardware in the rack. Everything Compute Platforms builds sits on what we provide.

---

## Accountable For

- Physical data center operations across all locations
- Rack and stack, cabling, decommissioning, remote hands
- Power, cooling, physical security
- Colocation environment management for customer-owned hardware
- Lease management and real estate runway across all sites
- Space and power capacity planning
- Physical asset inventory and CMDB accuracy
- Hardware remediation dispatched from Service Desk tickets (CMOS, PSU, disk, physical sensors)
- Delivering powered, racked, cabled, network-connected hardware to Compute Platforms for environment build

---

## Problems We Solve

- Customers need their hardware in a secure, available, well-maintained physical environment
- Hardware health events need to be physically resolved without customer involvement
- Colocation customers need right-sized space and power without over-provisioning
- Lease runway needs proactive management — a capacity crisis from an expiring lease is avoidable
- CMDB accuracy is a prerequisite for operational decisions, financial reporting, and audit compliance

---

## Products and Services Supported

- Colocation: ~768 services across all locations — customer-owned hardware in Aptum facilities
- Facility services: space, power, cooling, physical security
- Connectivity services: physical layer (cross-connects, fiber, patch panels)
- Remote hands: all locations
- Physical asset management: servers, switches, firewalls, storage arrays across the estate

### Data Center Locations
| Location | City | Approximate Services |
|---|---|---|
| South Pointe | Herndon, VA (USA) | 1,339 |
| Toronto / Pullman / 151 Front / King St | Toronto, ON (Canada) | 1,203 |
| Portsmouth / Croydon / Horner | Portsmouth / London (UK) | 1,091 |
| Atlanta | Atlanta, GA (USA) | 591 |
| Miami | Miami, FL (USA) | 570 |
| Malibu | Los Angeles, CA (USA) | 551 |
| Vancouver | Vancouver, BC (Canada) | 97 |
| Montreal / Barrie / Kirkland | Canada (various) | 49 |

---

## What This Team Does NOT Do

- Install operating systems or run configuration playbooks — that is Compute Platforms
- Network configuration or logical network management — that is Network
- Own monitoring alerts — DC Ops receives tickets from Service Desk; it does not own alert intake
- Customer relationship management — that is HSDM
- Financial reporting or cost center allocation — that is Finance with Operational Intelligence support

---

## Physical Remediation Flow

```
Hardware health alert fires (Zabbix)
        ↓
Service Desk receives and creates ticket
        ↓
Ticket dispatched to Data Center Ops
        ↓
DC Ops dispatches technician for physical fix
(CMOS battery, PSU swap, disk replacement, etc.)
        ↓
DC Ops updates ticket with resolution
        ↓
Service Desk closes ticket
Customer sees restored service — never touches the physical layer
```

---

## Financial Model

### Revenue Touch
- Colocation direct MRC: ~768 services (per-cabinet and per-cage pricing)
- Enables all physical hosting revenue by providing the facility layer that hardware sits in
- Lease and power costs are a direct COGS for colocation margin

### Direct Cost Driver
- Facilities: lease, power, cooling — largest non-labor cost in the org
- Labor: George's team distributed across multiple physical locations
- Geographic spread means cost is inherently distributed and cannot be fully centralized

### Margin Profile
- Colocation margin is primarily a function of utilization — rack space and power sold vs. capacity leased
- Target: rack utilization and power allocation as close to 100% as possible
- PUE (Power Usage Effectiveness) is a direct margin lever — lower PUE = better margin per kW sold

### How We Are Measured
| Metric | Target |
|---|---|
| Rack space utilization | As close to 100% as possible |
| Power allocation utilization | As close to 100% as possible |
| PUE | To be defined |
| MTTR for physical incidents | To be defined |
| Internal Incident Report (IIR) issuance | Within 24–48 hours of major incident |
| CMDB discrepancy vs. physical audit | 0% |
| Cycle count accuracy | As close to 100% as possible |
| Lease runway | Tracked quarterly |

---

## Key Dependencies

| Dependency | Direction | Notes |
|---|---|---|
| Compute Platforms | Outbound | Delivers hardware-ready environments for build |
| Network | Lateral | Physical cabling interfaces with Network's logical infrastructure |
| Service Desk | Inbound | Receives hardware remediation tickets dispatched from Service Desk |
| IT Operations & Engineering | Lateral | Facilities tooling, CMDB system |

---

## Open Questions / Flags

- **UK physical presence:** Portsmouth/Croydon/Horner accounts for ~1,091 services. Whether George's team has adequate local staffing in the UK for remote hands and hardware remediation — or relies on contracted third-party remote hands — needs to be explicit and documented.
- **LA/Malibu:** 551 services — comparable scale to Atlanta and Miami. Whether this location has equivalent local coverage is worth auditing.
