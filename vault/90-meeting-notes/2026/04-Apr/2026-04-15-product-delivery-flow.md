---
type: meeting
date: 2026-04-15
attendees:
  - "[[Adam Nelson]]"
  - "[[Will Stevens]]"
  - "[[Martin Tessier]]"
  - "[[Jason Auer]]"
  - "[[Patrick Wolthausen]]"
  - "[[Andrei Ianouchkevitch]]"
  - "[[Ben Kennedy]]"
  - "[[George Revie]]"
initiative: Product Delivery Flow & Service Ownership
---

# 2026-04-15 — Product Delivery Flow

**Date:** Tuesday, April 15, 2026 — 3:00 PM ET
**Duration:** ~74 minutes
**Attendees:** Adam Nelson, Will Stevens, Martin Tessier, Jason Auer, Patrick Wolthausen, Andrei Ianouchkevitch, Ben Kennedy, George Revie
**Related:** [[50-services/Service Network]], [[2026-04-15-will-adam-sync]]

---

## Context

Adam and Will had a pre-meeting sync earlier in the day ([[2026-04-15-will-adam-sync]]) to align on product architecture and service delivery layers. This meeting brought the full ops leadership team together to establish a clear ownership model: who delivers what service, who supports what, and how revenue flows. The underlying problem was that accountabilities had drifted — particularly between Martin's team (infrastructure/compute) and Jason's team (day-2 operations/support) — and the group needed first principles before proceeding with service descriptions, pricing, and product strategy.

Will Stevens facilitated most of the discussion.

---

## Notes

### The Layered Service Ownership Model

The group aligned on a layered responsibility model for how infrastructure services are delivered and supported:

**Layer 1 — Physical Provisioning (George & Ben):** George's team racks, cables, and powers hardware. Ben's team provisions networking. They deliver infrastructure to the point where it's physically ready. They don't have ongoing customer-facing relationships for these services.

**Layer 2 — Compute Platform Services (Martin):** Martin's team owns the OS images, hypervisor layer, storage (SAN/external), backup infrastructure, and one-time configuration. He delivers the *capability* — the service itself — but does not own day-2 operations. His team prepares patches; Jason's team applies them. His team provisions backup infrastructure; Jason's team manages the customer's use of it.

**Layer 3 — Day-2 Operations & Customer Support (Jason):** Jason's team owns all ongoing customer-facing support across all services that Martin, Ben, and George deliver. This includes monitoring customer systems, responding to tickets, troubleshooting, backup monitoring/testing/restores, and operational maintenance. He escalates to Martin (infrastructure/image issues) or George (physical issues) as needed.

**Layer 4 — Managed Cloud (Andrei):** Managed cloud sits on top of the infrastructure stack. Andrei's team manages customer consumption of services (VMware patching, cloud operations, etc.) but leverages Martin's services (backup, storage) for the underlying capability. When a managed cloud customer needs backup provisioned, that's Martin's service — Andrei's team manages the customer's use of it.

### Backup Service Ownership — The Defining Discussion

This was the longest topic (~25 min) and the one that clarified the ownership model for everything else.

**Consensus:** Martin owns the Aptum Backup Service as a product. He owns provisioning, storage infrastructure, capacity management, service definition, and profitability of the backup product. Jason owns the customer-facing support: monitoring backups, testing restores, handling customer tickets, and managing the customer's experience of using the service.

**Revenue model:** Customer pays Martin for storage consumed (the physical service). Jason's support cost is a fixed allocation per device — it's a baseline cost of managed hosting, not an add-on. Andrei's managed cloud customers who need backup still use Martin's service; Andrei manages the customer relationship.

**Key quote from Will:** "Martin is delivering a backup service. How that service is consumed and whether there are services around the consumption of that backup is an entirely different thing."

**Key quote from Ben:** "If there's 'managed' in the name, then a baked-in subcomponent of it should be the management of that service." This principle was agreed to apply across all services (firewalls, storage, backups, etc.).

### Storage as a Service

Storage built into the physical server is transparent — not a separate service. SAN or external storage is a separate service delivered by Martin's team. Jason supports the customer's use of it. Same ownership model as backups.

### Support is Baseline, Not a Discount Mechanism

Adam's position (agreed by the group): Every list-priced server includes Jason's support as a baseline cost. If a customer wants a discount, the margin on hardware gets reduced — support is never the thing that gets removed.

**Math example discussed:** If a server is $1,000/mo and $150 of that is people costs (Jason, George, Ben), then a 30% discount applies to the $850 margin portion, not to the full $1,000. The $150 is a fixed cost that funds the support function regardless of discounting.

Patrick reinforced: "Jason's team support is just a baseline. When we count up costs, it's baseline added to the CapEx, the power, the space. These are costs that come with managed hosting. They are not add-ons."

### Patching Responsibility

Martin's team prepares patches (testing, staging, validation). Jason's team applies patches and is responsible for ongoing operations. Customer may be responsible for actual deployment depending on service level. This was agreed without significant debate.

### Monitoring & Tool Ownership — NOT Resolved

Multiple monitoring tools are in use (Zabbix, DataDog, LogicMonitor, Hyperview, Ocean, PagerDuty) with no clear ownership model. The group discussed but did not finalize:

- **Internal shared tools (Jira, PagerDuty, internal Zabbix):** Should be owned by IT as shared services
- **Customer-facing tools:** Should be owned by the service team delivering to that customer
- **Tension:** Patrick argued IT should support tools they don't deeply understand (uptime + patching); Will argued IT can't support tools they don't know and it's too risky
- **George confirmed he owns Hyperview** (infrastructure visualization)
- **Andrei owns/wants to own DataDog** (for managed cloud)
- **Zabbix:** Currently two instances, no clear owner. Jason uses it for customer-facing monitoring. George uses it (skinned as "Guardian") for physical systems monitoring. Consolidation and ownership is an open org-wide question — not assigned to any individual

### Private Cloud / VPC Definitions

Will pushed hard on terminology clarity:
- **Cloud requires API orchestration** (NIST definition) — otherwise it's just virtualization
- **Shared VPC:** Multi-tenant virtual infrastructure, fully managed by Aptum via CloudStack
- **Dedicated Private Cloud:** Single-tenant physical cluster, fully managed — customer never touches hosts, resources available only through orchestration layer
- **Bare metal / dedicated hosting:** Customer manages hardware directly. Not cloud, regardless of whether a hypervisor is installed
- **"Dedicated V-Host" (current product):** Customer installs their own VMware on Aptum servers — closer to colo/hosting than cloud

This distinction matters for how Martin's team and Will's software team scope their work.

### Ben's Firewall Analogy — Applies Everywhere

Ben noted that managed firewalls follow the exact same model: "My team delivers firewalls. My team isn't supporting them when a customer calls in. But we're the ones that create the base configs, pick the models, do the proof of concepts, approve the features, and create the documentation." Jason's team handles the customer-facing support. This pattern was agreed to be the universal model.

---

## Decisions Made

1. **Service ownership model adopted:** Deliver (Martin/Ben/George) vs. Support (Jason) vs. Manage customer consumption (Andrei) as three distinct accountability layers
2. **Backup product ownership:** Martin owns the product and infrastructure. Jason owns customer support of it. Revenue: Martin gets storage/service revenue; Jason's support is a fixed allocation per device
3. **Storage as a service:** External/SAN storage is Martin's service to deliver; Jason supports customer use
4. **Support is baseline cost:** Never removed as a discount mechanism. Fixed people costs are excluded from margin discounting
5. **Patching model:** Martin prepares; Jason applies and maintains
6. **Monitoring/tool ownership:** NOT decided — needs a follow-up meeting

---

## Action Items

| Action | Owner | By When |
|--------|-------|---------|
| Formalize discount/pricing model with deal desk (Kathy/Tom) to separate people costs from margin | Adam | This quarter |
| Document backup service ownership and support model boundaries | Martin + Jason | Next 1:1s |
| Clarify team's day-2 operational involvement in backups (what to keep vs. hand off) | Martin | Next 1:1 |
| Document service offerings with explicit delivery vs. support boundaries | Jason | Ongoing |
| Schedule follow-up meeting on monitoring/tool ownership | Adam | This week |
| Schedule follow-up on AptCloud/private cloud/VPC product definitions | Will + Adam | TBD |

---

## Open Loops to Add

- Monitoring/tool ownership (Zabbix, DataDog, LogicMonitor, Hyperview, Ocean) — org-wide, unresolved
- Revenue allocation model for multi-component services — needs finance alignment
- Can customers opt out of support? (Currently no, but the "discount by removing support" practice needs to stop)
- AptCloud / Proxmox / VMware product definition alignment with Will's software team

---

*Source: Transcript — Product delivery flow.docx (April 15, 2026, 74 min)*
*Route after meeting: actions → 40-people (Martin, Jason, George), decisions → pricing/service model, context → 50-services, loops → open-loops*
