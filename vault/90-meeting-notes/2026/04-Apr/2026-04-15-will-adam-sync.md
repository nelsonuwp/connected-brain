---
type: meeting
date: 2026-04-15
attendees:
  - "[[Adam Nelson]]"
  - "[[Will Stevens]]"
initiative: Product Architecture & Tooling Alignment
---

# 2026-04-15 — Will / Adam Sync

**Date:** Tuesday, April 15, 2026
**Duration:** ~54 minutes
**Attendees:** Adam Nelson, Will Stevens
**Related:** [[2026-04-15-product-delivery-flow]], [[50-services/compute-platforms/compute-platforms.description]]

---

## Context

Pre-meeting sync between Adam and Will before the [[2026-04-15-product-delivery-flow|Product Delivery Flow]] session with the full ops team at 3 PM. Covered tooling strategy, product architecture alignment, and service delivery scope clarity — particularly around Martin's team and the AptCloud/IaaS stack.

---

## Notes

### Confluencer — Git-to-Confluence Two-Way Sync Tool

Will has designed and built a tool called "Confluencer" — git hooks that enable two-way sync between markdown files in a git repository and Confluence pages.

How it works: You run `confluencer install` in a git repo, configure the parent page in Confluence you want to track. On `git push`, markdown changes automatically publish to Confluence. On `git pull`, Confluence edits merge back into the local working directory.

Formatting: Standard markdown primitives (headings, bold, lists, tables) sync cleanly. Confluence-specific macros are base64-encoded and stored as comments in the markdown file, then rehydrated on push — so macros are preserved but don't pollute the markdown.

Status: Built across 8 phases (blew through two Claude context limits building it). Not yet tested — Will switched to the order approval automation work and hasn't circled back. Needs testing before deployment.

Why it matters: Enables Adam and Will to manage operational documentation (job descriptions, service descriptions, products) as markdown files in git, use them as context for Claude/AI work, and still have everything published to Confluence for the rest of the org to comment on and collaborate with. Avoids dependency on MCP servers or live API calls to Confluence.

### AI Strategy Alignment

Both Adam and Will share the same philosophy but from different angles:

**Will's position:** Use AI to build tools and deliver functionality, but don't embed AI into operational day-to-day transactional processes. Build programs that work independently of AI availability. Concern about "enshittification of AI" — if we build tools that don't depend on AI for the transactional back-and-forth, we're insulated when pricing/quality changes.

**Adam's position:** Leaning in heavily right now because the value-per-token is extremely high at current pricing. Anthropic is still essentially a startup, no one's been acquired by BlackRock/SoftBank yet. Strike while the iron is hot. Focused on: how to squeeze maximum value per token — which means putting less tokens in and getting more meaningful output. Seeing parallels between how you ask people for things and how you ask LLMs — context matters, specificity matters.

**Shared priority:** Get job descriptions, products/services, and service network definitions into markdown files. Then these become context for AI to optimize operations, service delivery flow, product design.

### Job Descriptions & HR

Nikki Thind (HR) has job descriptions staged and ready to go, but some are missing. Will has been upgrading her access from view-only to editor as she requests it. Plan: convert all JDs to markdown, put in a repo, sync via Confluencer to Confluence. This becomes the source of truth that both Adam and Will can use as context.

### Service Architecture — Product Layer Clarity

Adam and Will aligned on how the product stack layers before talking to the team:

```
Application Services (AptCloud portal / control plane)
    ↓
Orchestration (CloudStack / VMware Cloud Director)
    ↓
Hypervisor (VMware / KVM-Proxmox / Zen Server)
    ↓
Physical Hardware (servers, storage, networking)
```

**Martin's team (Compute Platforms) owns:** Aptum IaaS + Private Cloud — the hypervisor and orchestration layers. He delivers the service/capability. His team is opinionated about hardware specs for clusters (homogeneous chipsets per cluster, capacity management, N+1).

**Martin's team does NOT own:** Bare metal/dedicated hosting (that's just selling servers), AptCloud application layer (that's Will's software team), public cloud.

**Open question carried to 3 PM meeting:** Does Martin's team do ongoing operations (hypervisor patching, maintenance) after initial deployment, or does that hand off to Jason's team? This became a key topic in the Product Delivery Flow session.

### Hypervisor Deep-Dive: VMware vs. KVM/Proxmox vs. CloudStack

Will provided technical context:

**Type 1 hypervisors (VMware, Zen Server):** Run at hardware level with DOM0 (privileged domain) brokering hardware access.

**Type 2 hypervisors (KVM):** Handled in kernel; host OS and QEMU manage VM access to hardware. Proxmox is KVM + a management layer (vCenter-like interface).

**VMware's key advantage:** vMotion — live migration of VMs between hosts with zero downtime. Extremely valuable for maintenance windows. 20 years of market dominance means deep ecosystem integration (Zerto, etc.).

**CloudStack's key advantage:** Extensive orchestration capabilities — far more control over what you can expose to customers than VMware Cloud Director. Better customer experience for self-service provisioning, networking rules, etc.

**Open question:** Can KVM achieve vMotion-equivalent with shared storage architecture (NFS)? This is critical for feature parity. Will to investigate.

**Key insight from Will:** Feature availability is about ecosystem maturity and integration, not hypervisor type. VMware's perceived superiority is market dominance, not technical superiority.

### Private Cloud / VPC Definition Alignment

This was pre-alignment before the group discussion:

- **"Cloud" requires API orchestration** (NIST definition) — otherwise it's just virtualization
- **Shared VPC:** Multi-tenant, customer resources on shared physical hardware, fully managed by Aptum via CloudStack. Customer never sees hosts.
- **Dedicated Private Cloud:** Single-tenant physical cluster, fully managed. Same experience as VPC but with physical isolation.
- **Dedicated V-Host (current product):** Customer gets a server with VMware license — they manage the hypervisor. This is NOT private cloud. It's closer to colo with a VMware license.
- **Bare metal:** Customer does whatever they want on the hardware. Never cloud.

**Will's definition:** "If we're talking private cloud, we're managing the hypervisor layer for the customer. Otherwise we're just selling servers and giving them a VMware license."

### Order Flow / AI Opportunity

Adam outlined a vision: Customer call comes in → AI translates the need into a standard offering (pennies on the dollar vs. paying a person) → either goes through CPQ or directly to an order form → customer approves → George's team racks and stacks → or triggers equipment purchasing → customer self-provisions.

This requires all the documentation (products, services, service network, JDs) to be in machine-readable format — which is why the markdown + Confluencer work matters.

---

## Decisions Made

1. **Confluencer adoption:** Will to complete testing; will become the standard for managing documentation as markdown synced to Confluence
2. **AI strategy:** Use AI to build tools, not for operational dependency. Lean in now while costs are low
3. **Martin's scope pre-aligned:** Compute Platforms = Aptum IaaS + Private Cloud (hypervisor & orchestration). NOT bare metal, NOT AptCloud app layer
4. **JDs to markdown:** Convert all job descriptions, sync via Confluencer to Confluence

---

## Action Items

| Action | Owner | By When |
|--------|-------|---------|
| Complete Confluencer testing and validation | Will | TBD |
| Convert job descriptions to markdown and put in repo | Adam + Will | Ongoing |
| Confirm vMotion equivalence in KVM with shared storage | Will | TBD |
| Align Martin, Jason, Andrei on service delivery boundaries | Adam + Will | 3 PM meeting (same day) |

---

## Open Loops to Add

- Confluencer testing — not yet validated, could be blocked by edge cases
- vMotion KVM equivalence — critical for VMware migration path positioning
- Order flow automation vision — long-term, depends on markdown documentation being complete

---

*Source: Transcript — Will_Adam.vtt (April 15, 2026, ~54 min)*
*Route after meeting: tooling context → Will notes, product architecture → 53-products, service scope → 50-services*
