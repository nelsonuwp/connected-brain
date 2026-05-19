# Bare Metal / Servers

Aptum bare metal servers are Aptum-owned, single-tenant physical servers delivered with a mandatory Service Desk management layer. At $1.58M USD MRC, servers are the largest revenue line in the Aptum portfolio (54.67% of total MRC). The Service Desk layer is non-negotiable and non-removable — it is priced into the product floor.

## What it is (and what it is not)

A bare metal server is a dedicated physical machine provisioned for a single customer, with no hypervisor or virtualization overhead. It is not Aptum IaaS — there is no CloudStack or KVM orchestration layer, and no portal self-service (today). The Service Desk layer that monitors and triages the server is mandatory; it cannot be removed or priced out. This is not a colocation arrangement — Aptum owns the hardware.

## What's always included (Fundamental guarantee)

Server powered and network-connected, Zabbix monitoring active on the infrastructure layer, failed hardware components (PSU, disk, CMOS battery) replaced within SLA, OS deployed per standard build, and L2 triage handled by Service Desk. The Service Desk layer is included in every bare metal server and cannot be removed.

## How it's delivered

Manual provisioning by Compute Platforms (specification and build) and Data Center Ops (rack and cable). Service Desk owns day-2 operations. No portal self-service today. Bare Metal as a Service (BMaaS) via the CloudStack 4.22 MAAS integration is on the roadmap and will enable self-service provisioning through Aptum Portal when live.

## Technical specifications

Dell enterprise-grade servers with Intel Xeon processors, enterprise SSD storage (Standard and Performance tiers), 10Gbps or 100Gbps uplinks, and carrier-neutral connectivity at primary sites.

## Pricing model

Six components make up the bare metal price. Only the margin component is discountable — the cost base is not negotiable below cost.

The six components are: (1) CapEx amortized over the contract term, with residual values of 40% at 12 months, 20% at 24 months, and 0% at 36 months; (2) power, billed per kW at the data center rate (illustrative: Herndon $110/kW, Atlanta $337/kW, Miami $48/kW, Los Angeles $457/kW, Toronto and Montreal $253/kW, Portsmouth $46/kW); (3) Data Center Ops labor allocated per server; (4) Network team cost allocated per server (approximately $59 per server); (5) Service Desk mandatory managed layer, approximately $40 CAD per asset per month fully loaded and non-removable; (6) OS and software licensing where applicable.

## When this fits (and when it doesn't)

Bare metal fits customers with dedicated single-tenant requirements, high-IO workloads (databases, high-frequency computing), compliance requirements mandating physical isolation, or workloads that perform poorly on shared virtualized infrastructure. It is not the right fit for customers who need VM flexibility, self-service scaling, or lower unit costs — those customers belong on Aptum IaaS VPC or Dedicated Cloud.

## Managed services available on top

Bare metal customers are eligible for Reactive and Proactive engagement tiers. The Dedicated tier is not available on bare metal — the mandatory Service Desk layer means every bare metal customer is at minimum on a Reactive-equivalent posture for the infrastructure layer. All addon categories are compatible with bare metal.
