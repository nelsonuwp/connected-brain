# Network

**Service Manager:** Ben Kennedy
**Function:** Operations
**Lifecycle:** Live

> We connect everything. MPLS, internet, IP, cloud connect. If data moves between a customer and their environment, it moves on our network.

---

## Accountable For

- Network infrastructure design, implementation, and operations
- MPLS and internet connectivity across all data center locations
- IP address management, allocation, and monetization
- Cloud Connect and direct links to hyperscalers (physical circuit and port provisioning)
- Network access control and security boundaries across segments
- Network performance monitoring and incident response
- Compliance evidence for network-layer regulatory requirements
- Providing network-ready infrastructure to Data Center Ops and Compute Platforms

---

## Problems We Solve

- Customers need reliable, performant connectivity to their hosted environments
- Hybrid environments need seamless network connectivity across physical and cloud
- Security boundaries need to be enforced at the network layer
- IP address assets need to be managed accurately and monetized correctly
- Network incidents need to be resolved before they become customer-visible outages

---

## Products and Services Supported

- MPLS connectivity: Off-Net and On-Net ports (100Mbps, 1GigE, fiber)
- Internet access ports
- Fiber cross-connects and patch panel connections
- Cloud Connect / Direct Links (physical circuit — logical config handed to Managed Cloud)
- Bandwidth blocks
- IP address blocks
- Network switching: Juniper EX-4300T (48 ports, 81 units in estate)

---

## Scope Boundary — Network vs. Managed Cloud

This boundary is defined by the OSI model and by whether a service requires physical infrastructure or service configuration.

| Service | Owner | Reasoning |
|---|---|---|
| MPLS circuits, internet ports, routing, BGP peering | Network (Ben) | Physical and logical network infrastructure — OSI Layer 1–3 |
| Switching, patching, physical cable | Network (Ben) | Physical layer |
| Cloud Connect physical circuit and port | Network (Ben) | The physical pipe is Network's; provisioning the port |
| WAF (Web Application Firewall) | Managed Cloud (Andrei) | Service configuration and policy, not a network device |
| DDoS protection | Managed Cloud (Andrei) | Managed scrubbing service — cloud or managed appliance |
| ExpressRoute / Direct Connect logical config | Managed Cloud (Andrei) | Configuration, monitoring, and managed service wrapper |
| Juniper SRX firewall — physical connectivity | Network (Ben) escalation | When the physical port or circuit is the issue |
| Juniper SRX firewall — security policy | Managed Cloud (Andrei) escalation | When firewall rules or policy is the issue |
| Juniper SRX firewall — L2 ops and ticket response | Service Desk (Jason) | Day-to-day management and ticket response |

**Practical test:** If it requires a Juniper CLI or a physical cable, it is Network. If it requires a portal, a policy, or a service configuration, it is Managed Cloud.

---

## What This Team Does NOT Do

- Cloud networking security services (WAF, DDoS, hybrid interconnects) — that is Managed Cloud
- Physical cabling inside racks beyond standard patch work — that is Data Center Ops
- OS-level or application-layer configuration — that is Compute Platforms or Managed Cloud
- Customer relationship management — that is HSDM
- Firewall security policy management — that is Managed Cloud for escalations

---

## Financial Model

### Revenue Touch
- Connectivity services direct MRC: ~395 services
- Enables all hosted and colo revenue by providing the connectivity layer
- IP address assets: managed inventory with sale and lease monetization value
- Bandwidth blocks: ~51 services with direct MRC

### Direct Cost Driver
- Labor: Ben's team
- Transit costs: upstream network provider fees are a direct COGS
- Hardware depreciation: Juniper switching estate (EX-4300T, SRX series)

### Margin Profile
- Connectivity margin is a function of transit cost efficiency and utilization
- 99.999% uptime SLA — breach is a direct financial liability
- IP address assets are balance sheet items; accurate inventory management is a financial prerequisite

### How We Are Measured
| Metric | Target |
|---|---|
| Network uptime / availability | 99.999% |
| Network throughput | To be defined |
| Network latency | To be defined |
| Packet loss | To be defined |
| Average available capacity | To be defined |
| MTTR for network incidents | To be defined |
| Security incident frequency | To be defined |
| Compliance report | Met / not met per audit |
| IP addresses managed and accounted for | 100% inventory accuracy |

---

## Key Dependencies

| Dependency | Direction | Notes |
|---|---|---|
| Data Center Ops | Lateral | Physical layer interfaces at the data center — cabling, cross-connects |
| Compute Platforms | Outbound | Network must be provisioned before compute build can begin |
| Managed Cloud | Lateral | Cloud Connect logical config handed off after physical circuit is live |
| Service Desk | Inbound | Escalation path for network-layer incidents |
| IT Operations & Engineering | Lateral | Network management tooling |
