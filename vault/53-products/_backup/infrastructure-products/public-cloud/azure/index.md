# Azure

Aptum delivers Microsoft Azure as a CSP partner through Aptum Portal. Azure is the most mature hyperscaler integration in the portal and is live in production with active customer workloads.

## What it is (and what it is not)

Aptum Azure delivery means consolidated billing, portal visibility, and managed services on top of Microsoft Azure subscriptions. It is not a replacement for the Azure portal — customers can still access Azure directly. Aptum adds the CSP billing layer, the Aptum Portal cost visibility, and the managed operations layer that Microsoft's own commercial relationship does not provide.

## What Aptum manages vs. what Azure owns

Azure owns the physical infrastructure, global network, and platform SLAs. Aptum manages the CSP subscription, consolidates billing, surfaces cost data in Aptum Portal, and operates managed services (OS patching, backup, security, FinOps) on top of customer Azure workloads.

## How it's delivered

Self-service Azure resource management via Aptum Portal (instances, disks, networks, AKS). Azure is the first hyperscaler to go live. Demonstrated at the March 2026 board demo with a production customer (Vergent) running approximately $100,000 per month in Azure spend through the portal. Azure Kubernetes Service (AKS) is supported.

## Technical specifications

Azure instances, managed disks, virtual networks, AKS clusters, and Cloudflare DNS are all manageable through Aptum Portal. Azure plugin uses the standard Azure Resource Manager API. ExpressRoute private circuits for dedicated connectivity to Aptum infrastructure are available via the Hybrid Interconnects addon.

## Pricing model

Passthrough of Microsoft Azure pricing plus CSP margin. Aptum does not markup egress — Microsoft's standard egress rates apply. Managed services addons are priced independently per endpoint per month.

## When this fits (and when it doesn't)

Azure through Aptum fits customers already on Azure who want consolidated billing, a single portal across their Azure and Aptum IaaS workloads, and managed services layered on top of their Azure environment. It fits customers coming through the Hybrid Cloud Assessment (workload placement and optimization) and the Well-Architected Review (governance and cost optimization). It does not replace Azure for customers who are running cloud-native PaaS services deeply integrated with the Azure ecosystem — Aptum adds management and visibility on top, not a migration off Azure.

## Managed services available on top

Full addon catalog compatible with Azure workloads. FinOps and OS Patching are the most common first addons for Azure customers. Compliance Reporting (Proactive tier) is relevant for customers with SOC 2 or PCI requirements on Azure workloads.
