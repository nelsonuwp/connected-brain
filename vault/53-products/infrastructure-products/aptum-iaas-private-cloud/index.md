# Aptum IaaS — Private Cloud (VMware / Proxmox)

Aptum Private Cloud is single-tenant dedicated hardware running VMware ESXi or Proxmox VE as the hypervisor. Unlike Dedicated Cloud (which runs KVM with CloudStack), Private Cloud uses the customer's preferred hypervisor on dedicated physical hosts. It is not necessarily delivered through Aptum Portal — the managed services layer sits on top of the infrastructure regardless.

## What it is (and what it is not)

Private Cloud is dedicated infrastructure with a choice of hypervisor: VMware for customers who need VMware-specific features (vMotion, vSAN, NSX, VMware licensing) or Proxmox for customers migrating away from VMware at lower cost. It is not Dedicated Cloud — the hypervisor and delivery model differ. It is not colocation — Aptum owns the hardware. Aptum Portal is not required to deliver Private Cloud, though it can be used where the CloudStack integration supports it.

## What's always included (Fundamental guarantee)

Dedicated hardware available, hypervisor (ESXi or Proxmox) healthy, storage connected, and Managed Cloud operating the environment at the OS layer and above.

## How it's delivered

Manual provisioning by Compute Platforms (VMware environment build or Proxmox cluster setup). Managed Cloud operates day-to-day. VMware is available via ThinkOn licensing (current MTC path) or CloudStack native ESXi integration. Proxmox is available via the CloudStack 4.21 Extensions Framework, with operational capability already in place.

## Technical specifications

VMware ESXi 7.0 or 8.0: supports vMotion, vSAN, HA, DRS, and NSX networking. VMware licensing sourced via ThinkOn (VCSP Pinnacle tier). Proxmox VE: KVM-based, open-source, built-in Ceph storage, no licensing overhead, integrated with CloudStack via Extensions Framework. Both run on Aptum-owned dedicated physical hosts. Proxmox extension limitations at current state: no live migration, no VM scaling via CloudStack, no CloudStack capacity reporting.

## Pricing model

Per vCPU per month, per GB RAM per month, or per dedicated host per month. VMware track carries VMware licensing cost overhead baked into the price. Proxmox track eliminates hypervisor licensing costs, providing structural cost advantage. Broadcom's 2024 VMware licensing restructuring increased costs 300 to 1,050% for many customers — this cost is passed through on VMware track. The Proxmox path removes this dependency.

## When this fits (and when it doesn't)

Private Cloud on VMware fits customers with existing VMware estates requiring feature continuity (vMotion, vSAN), customers under active Broadcom contracts who are not yet ready to migrate hypervisors, and workloads with VMware-specific application dependencies. Private Cloud on Proxmox fits customers actively displacing VMware who need a managed alternative without the CloudStack migration path. It is not the right fit for customers who are comfortable with KVM and want portal self-service — those customers belong on Dedicated Cloud.

## Managed services available on top

Reactive and Proactive tiers available. Managed Cloud has deep operational capability on both VMware ESXi and Proxmox. All security, monitoring, backup, and connectivity addons are compatible. Private Cloud is the natural landing zone for customers coming through the Hybrid Cloud Assessment (VMware displacement path) and the Cloud Repatriation Assessment.
