# Aptum IaaS — Dedicated Cloud

Aptum IaaS Dedicated Cloud is single-tenant dedicated compute on KVM with Apache CloudStack 4.22 orchestration, delivered via Aptum Portal. Dedicated physical hosts mean one customer's VMs only — no physical sharing with other tenants. The board validated this product at the March 2026 demo and characterized it as "true private cloud" commanding a premium valuation.

## What it is (and what it is not)

Dedicated Cloud provides the same CloudStack and KVM orchestration and the same portal self-service as VPC, but on dedicated physical hardware. The key distinction from VPC is physical tenancy: one customer's VMs on their dedicated hosts. The key distinction from Private Cloud is the hypervisor: Dedicated Cloud runs KVM with CloudStack, while Private Cloud runs VMware or Proxmox. Dedicated Cloud is not bare metal — there is a KVM hypervisor layer and CloudStack manages the VM lifecycle.

## What's always included (Fundamental guarantee)

All VPC Fundamentals plus dedicated cluster always available and customer's VMs exclusively on their hosts. No sharing of physical compute or storage with other customers.

## How it's delivered

Via Aptum Portal, with SA involvement for initial sizing and cluster specification. Live. Compute Platforms builds the dedicated cluster. Service Desk and Managed Cloud operate it. Dedicated infrastructure can be sold through the platform today via product catalog configuration — confirmed at the March 2026 board demo.

## Technical specifications

KVM hypervisor on Apache CloudStack 4.22 on dedicated physical hosts. Same storage tiers as VPC: Standard SSD (2 IOPS/GB) and Performance SSD (6 IOPS/GB). NVMe on roadmap. Network architecture identical to VPC with the addition of dedicated host-level isolation. Pricing available per vCPU/GB or per dedicated host.

## Pricing model

Per vCPU per month, per GB RAM per month, per GB storage per month — or per dedicated host per month for larger configurations. Premium over VPC pricing reflecting dedicated hardware costs. No IOPS transaction fees, no egress charges. Board direction on pricing: start at a premium with selective discounting, reflecting the 74 to 89% gross margins on the underlying infrastructure. Go-forward pricing is defined in the commercial pricing model.

## When this fits (and when it doesn't)

Dedicated Cloud fits production workloads requiring dedicated compute, compliance-sensitive environments (physical isolation without hyperscaler data residency complexity), performance-critical applications where shared-host performance variability is unacceptable, and customers migrating from VMware who are comfortable moving to KVM. It is the primary new-logo acquisition product. It is not the right fit for customers who need VMware-specific features such as vMotion or vSAN — those customers belong on Private Cloud.

## Managed services available on top

Reactive and Proactive engagement tiers available. All addon categories compatible. Dedicated Cloud is the natural landing zone for customers coming through the Cloud Repatriation Assessment and the Infrastructure Risk Assessment (hardware refresh path).
