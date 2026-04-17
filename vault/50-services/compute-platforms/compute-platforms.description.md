# Compute Platforms

**Service Manager:** Martin Tessier
**Function:** Architecture & Delivery (one-time delivery, not ongoing operations)
**Lifecycle:** Live
**Note:** Previously referred to as Provisioning Engineering, Hosting, and Product Engineering. Canonical name is Compute Platforms.
**Confluence Link**: [Compute Platform Service Description](https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045518349/Compute+Platform)

> We build the compute. We write the playbook once. Data Center Ops runs it for every deployment after that. From bare metal to OS -- documented, handed off clean, then we step back.

---

## Accountable For

- Configuration standards across all compute products -- what a correct environment looks like for each product type
- Provisioning playbooks, OS images, and automation packages maintained as product-level assets. Compute Platforms authors these once; Data Center Ops executes them for each customer deployment. The analogy: Compute Platforms is the software vendor who writes and maintains the installer. Data Center Ops is the technician who runs it on each machine.
- Private Cloud environment delivery: VMware ESXi, Proxmox (dedicated hardware, not through Apt Cloud portal)
- Shared Cluster and Dedicated Cluster platform build: Apache CloudStack -- cluster infrastructure, node configuration, platform standards
- **Internal infrastructure procurement model for IaaS products:** For Shared Cluster and Dedicated Cluster, Compute Platforms acts as the internal customer, drawing on Aptum-owned dedicated server capacity to build and scale cluster footprint. Compute Platforms is not procuring from an external vendor -- it is procuring from Aptum's own infrastructure, with Data Center Ops executing the physical layer as usual.
- Handoff documentation and runbooks at environment completion -- these are handed to Service Desk and Managed Cloud, who operate from them
- L3 escalation support on all environments this team has built

---

## Problems We Solve

- New customer environments need to be built correctly, consistently, and repeatably — manual provisioning does not scale
- Configuration drift from standards creates downstream operational problems for Service Desk and Managed Cloud
- Managed Cloud and Service Desk need clean, documented environments to do their jobs from day one
- AptCloud needs a platform engineering capability to build and mature shared-cluster infrastructure
- Physical-to-virtual and bare-metal-to-cloud migrations need a team that understands both layers

---

## Products and Services Supported

- Dedicated servers: Pro Dell PE R-660XS and full server catalog
- Private Cloud: VMware ESXi 7.0/8.0, Proxmox (dedicated hardware, not through Apt Cloud portal)
- Shared Cluster: Apache CloudStack, KVM, multi-tenant shared hosts (Alpha -- building toward Beta)
- Dedicated Cluster: Apache CloudStack, KVM, single-tenant dedicated hosts (Alpha -- building toward Beta)
- Guest virtual environments
- Storage platforms: NetApp FAS, SolidFire All-Flash

**Note on BMaaS:** Self-service bare metal provisioning through the Apt Cloud portal (Canonical MAAS via CloudStack Extensions Framework 4.22) is a roadmap capability owned by the Apt Cloud software/portal team, not Compute Platforms. Compute Platforms' role is to provide and maintain the provisioning playbooks and OS images that BMaaS will execute -- the portal team owns the self-service delivery mechanism.

---

## Scope Boundary — Compute Platforms vs. Data Center Ops

This is the key operational question for this service. The answer is a functional split, not a consolidation.

**Data Center Ops owns everything physical:** racking, cabling, powering, physical inventory, remote hands. They deliver a server that is powered, racked, cabled, and network-connected.

**Compute Platforms owns everything that runs on top of that hardware:** configuration standards, automation playbooks, OS deployment, monitoring agent installation, backup agent installation, config push. They receive powered hardware from Data Center Ops and deliver a complete, documented, running environment.

**The provisioning execution model:** Compute Platforms authors each playbook once -- for the first instance of that environment type. Data Center Ops then executes that same playbook for every subsequent deployment. This means Compute Platforms does not need to be hands-on for each kickoff. Data Center Ops runs the package. Compute Platforms' value is in the playbooks and standards, not in the repeated execution of them.

### Why This Split -- Not Consolidation Under Data Center Ops

Pushing all provisioning to Data Center Ops only works if that team can also run playbooks, push configs, and install monitoring agents. That requires software and platform skills that are different from physical operations skills. Data Center Ops is built for facilities and physical ops. Compute Platforms is -- or should become -- a configuration and automation team.

### The Direction of Travel

As the environment matures, the manual provisioning work shrinks. The target state is:

```
Data Center Ops racks and cables hardware → hardware registered in system
        ↓
Data Center Ops executes Compute Platforms' provisioning package against the registered device
(OS deploy, config push, monitoring agent, backup agent -- from Compute Platforms-maintained playbooks)
        ↓
Validation runs → environment checked against Compute Platforms' standards
        ↓
Documentation generated → handoff triggered to Service Desk or Managed Cloud
```

This is also what makes Shared Cluster and Dedicated Cluster operationally viable at scale. Cluster nodes cannot be manually provisioned -- automation is not optional for those products.

---

## What This Team Does NOT Do

- Day 2 operational management of any environment after handoff — that is Service Desk or Managed Cloud
- Physical facilities, power, cabling, or remote hands — that is Data Center Ops
- Network configuration or logical network management — that is Network
- Customer relationship management or SOW ownership — that is HSDM
- OS-level support tickets on running environments — that is Service Desk

---

## IaaS Platform Specifics (Shared Cluster and Dedicated Cluster)

- Platform: Apache CloudStack with KVM hypervisor, accessed via Apt Cloud portal (portal.aptum.com)
- Cluster types: Shared Cluster (multi-tenant shared hosts) and Dedicated Cluster (single-tenant dedicated hosts)
- Infrastructure: Aptum-owned server capacity, internally procured through the IaaS procurement model described above
- Current status: Alpha -- building toward Beta
- Commercial intent: lower-cost public cloud alternative for customers who do not need hyperscaler scale
- Risk profile: shared cluster nodes mean one misconfiguration affects all tenants on that cluster -- qualitatively different from dedicated hosting. Change management discipline is non-negotiable.
- Day 2 operations post-handoff: Service Desk owns cluster node infrastructure health (hypervisor-layer). Managed Cloud provides optional managed service layers above the OS. The Apt Cloud portal application layer is managed by Managed Cloud.
- Compute Platforms retains L3 escalation on all cluster infrastructure

---

## Financial Model

### Revenue Touch
- Provisioning is a one-time cost of sale, not a recurring revenue line
- Enables all dedicated and managed hosting MRC by making environments exist
- AptCloud will generate recurring revenue when it exits Alpha — margin target to be defined at Beta pricing

### Direct Cost Driver
- Team labor: primary cost
- Provisioning time per environment is the key efficiency metric — automation reduces this directly
- AptCloud build is an investment cost against future recurring revenue

### Margin Profile
- Margin is indirect: quality and speed of provisioning protects hosting margin
- Rework after a bad provisioning job is a direct cost hit to the engagement
- Automation investment reduces per-environment cost over time — the leverage point for this team

### How We Are Measured
| Metric | Target |
|---|---|
| Provisioning accuracy (to spec, first time) | To be defined |
| Provisioning turnaround time | To be defined |
| Config validation pass rate (no remediation required) | To be defined |
| Documentation completeness at handoff | Met / not met |
| Runbook completeness at handoff | Met / not met |
| L3 escalation response time | To be defined |
| AptCloud cluster availability | To be defined (Alpha stage) |

---

## Key Dependencies

| Dependency | Direction | Notes |
|---|---|---|
| Data Center Ops | Inbound | Receives powered, racked, cabled, network-ready hardware; executes Compute Platforms' provisioning packages |
| Network | Inbound | Network connectivity provisioned before build can begin |
| Service Desk | Outbound | Receives runbooks at handoff; owns Day 2 execution of Compute Platforms' operational standards |
| Managed Cloud | Outbound | Receives handoff for optional managed OS and application layer services |
| HSDM | Lateral | Provisioning timelines are SOW milestones -- coordination required |

---

## Open Questions / Flags

- **Automation tooling ownership:** Who owns the playbook tooling (Ansible, Terraform, or equivalent) -- Compute Platforms, Operational Intelligence, or a future platform engineering function -- is an open question. The tooling is operational but also a shared infrastructure asset.
- **IaaS Beta readiness:** Shared Cluster operations require change management discipline not required for dedicated work. Operational readiness review required before exiting Alpha.
- **Internal procurement model documentation:** No formal process currently documents how Compute Platforms requests server capacity from Data Center Ops to expand Shared Cluster and Dedicated Cluster footprint. This needs to be defined before either product exits Alpha.
