# Compute Platforms

**Service Manager:** Martin Tessier
**Function:** Architecture & Delivery (one-time delivery, not ongoing operations)
**Lifecycle:** Live
**Note:** Previously referred to as Provisioning Engineering, Hosting, and Product Engineering. Canonical name is Compute Platforms.
**Confluence Link**: [Compute Platform Service Descriptio](https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5045518349/Compute+Platform)

> We build the compute. One time, to spec, automated where possible, documented, handed off clean. From bare metal to OS — then we step back.

---

## Accountable For

- Configuration standards across all compute products — what a correct environment looks like
- Automation playbooks for environment build: OS install, monitoring agent deployment, backup agent, config push
- Private cloud environment delivery: VMware ESXi, Proxmox
- AptCloud platform build and operations: Apache CloudStack, shared and dedicated clusters
- Handoff documentation and runbooks at environment completion
- L3 escalation support on all environments this team has built — they hold the deep technical knowledge

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
- Private cloud: VMware ESXi 7.0/8.0, Proxmox
- AptCloud: Apache CloudStack, shared and dedicated clusters (Alpha — building toward Beta)
- Guest Virtual environments
- Storage platforms: NetApp FAS, SolidFire All-Flash

---

## Scope Boundary — Martin's Team vs. George's Team

This is the key operational question for this service. The answer is a functional split, not a consolidation.

**George's team owns everything physical:** racking, cabling, powering, physical inventory, remote hands. They deliver a server that is powered, racked, cabled, and network-connected.

**Martin's team owns everything that runs on top of that hardware:** configuration standards, automation playbooks, OS deployment, monitoring agent installation, backup agent installation, config push. They receive powered hardware from George and deliver a complete, documented, running environment.

### Why This Split — Not Consolidation Under George

Pushing all provisioning to George only works if George's team can also run playbooks, push configs, and install monitoring agents. That requires software and platform skills that are different from physical operations skills. George's team is built for facilities and physical ops. Martin's team is — or should become — a configuration and automation team.

### The Direction of Travel for Martin's Team

As the environment matures, the manual provisioning work shrinks. The target state is:

```
George's team racks and cables hardware → hardware registered in system
        ↓
Martin's automation runs against the registered device
(OS deploy, config push, monitoring agent, backup agent — automated)
        ↓
Validation runs → environment checked against standards
        ↓
Documentation generated → handoff triggered to Service Desk or Managed Cloud
```

This is also what makes AptCloud operationally viable at scale. Shared cluster nodes cannot be manually provisioned — automation is not optional for that product.

**Martin's team's value is in the playbooks and standards, not in the manual execution of them.**

---

## What This Team Does NOT Do

- Day 2 operational management of any environment after handoff — that is Service Desk or Managed Cloud
- Physical facilities, power, cabling, or remote hands — that is Data Center Ops
- Network configuration or logical network management — that is Network
- Customer relationship management or SOW ownership — that is HSDM
- OS-level support tickets on running environments — that is Service Desk

---

## AptCloud Specifics

- Platform: Apache CloudStack
- Infrastructure: Aptum-owned excess server inventory
- Cluster types: shared and dedicated
- Current status: Alpha — being prototyped on existing hardware
- Commercial intent: lower-cost public cloud alternative for customers who don't need hyperscaler scale
- Risk profile: shared clusters mean one misconfiguration affects all tenants on that cluster — qualitatively different from dedicated hosting
- Day 2 operations post-handoff: Service Desk (basic) and Managed Cloud (platform layer)
- This team retains L3 escalation on all AptCloud infrastructure

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
| Data Center Ops | Inbound | Receives powered, racked, cabled, network-ready hardware |
| Network | Inbound | Network connectivity provisioned before build can begin |
| Service Desk | Outbound | Primary handoff destination for dedicated environments |
| Managed Cloud | Outbound | Handoff destination for private cloud and AptCloud environments |
| HSDM | Lateral | Provisioning timelines are SOW milestones — coordination required |

---

## Open Questions / Flags

- **Automation tooling ownership:** Who owns the playbook tooling (Ansible, Terraform, or equivalent) — Compute Platforms, Operational Intelligence, or a future platform engineering function — is an open question. The tooling is operational but also a shared infrastructure asset.
- **AptCloud Beta readiness:** Shared-cluster operations require change management discipline not required for dedicated work. Operational readiness review required before exiting Alpha.
