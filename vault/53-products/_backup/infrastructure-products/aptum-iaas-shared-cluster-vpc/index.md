# Aptum IaaS — Shared Cluster (VPC)

Aptum IaaS Shared Cluster, also referred to as VPC (Virtual Private Cloud), is multi-tenant shared compute on KVM with Apache CloudStack 4.22 orchestration, delivered self-service via Aptum Portal. It is the lowest-cost Aptum IaaS option, trading dedicated hardware for shared physical hosts with logical isolation.

## What it is (and what it is not)

VPC provides logically isolated compute on shared physical hosts. Multiple customers' VMs run on the same physical servers, separated by VLANs. It is not dedicated hardware — physical isolation requires Dedicated Cloud or Private Cloud. Because physical hosts are shared, change management on the cluster is critical: a misconfiguration at the hypervisor or network layer can affect all tenants on that host. This shared-cluster operational discipline is a requirement before scaling VPC customer onboarding.

## What's always included (Fundamental guarantee)

Platform available, VMs in running state, CloudStack and KVM layers healthy, storage connected, and baseline platform triage included in the product floor.

## How it's delivered

Self-service via Aptum Portal at portal.aptum.com. Live. Customers provision VMs, configure networks, manage storage, and set firewall rules through the portal without operator intervention. Compute Platforms builds and maintains the CloudStack clusters. Service Desk responds to platform-layer incidents.

## Technical specifications

KVM hypervisor on Apache CloudStack 4.22. Two storage tiers: Standard SSD (2 IOPS/GB, general-purpose workloads) and Performance SSD (6 IOPS/GB, databases and high-traffic applications). NVMe is on the roadmap. Internal network: 10Gbps redundant links per host. External: 10Gbps or 100Gbps uplinks. VLAN isolation for network separation (VXLAN support under validation). Public IP blocks are self-manageable via portal. L4 TCP load balancing is self-service via portal. L7 managed load balancing is a managed addon.

## Pricing model

Per vCPU per month, per GB RAM per month, per GB storage per month. No IOPS transaction fees, no egress charges — predictable monthly billing is a key differentiator versus hyperscaler pricing. Reference pricing from Ignite launch: $28/vCPU, $7/GB RAM, $0.28/GB standard storage, $0.56/GB performance storage (CAD). Infrastructure gross margins: approximately 74% on compute and RAM, 89% on performance storage. Go-forward pricing follows a premium positioning with selective discounting.

## When this fits (and when it doesn't)

VPC fits dev/test environments, cost-optimized general-purpose workloads, and customers evaluating Aptum IaaS before committing to dedicated infrastructure. It is not the right fit for compliance-sensitive workloads requiring physical isolation, high-performance production systems requiring guaranteed compute, or customers whose regulatory environment mandates single-tenant hardware. Those customers belong on Dedicated Cloud or Private Cloud.

## Managed services available on top

Reactive and Proactive engagement tiers are both available. All addon categories are compatible with VPC. VPC is the lowest-cost entry point for the full managed services stack.
