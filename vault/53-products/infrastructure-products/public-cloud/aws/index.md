# AWS

Aptum delivers Amazon Web Services as a CSP/partner through Aptum Portal. The AWS plugin is built and available in the portal but not yet configured for general customer use.

## What it is (and what it is not)

Aptum AWS delivery follows the same model as Azure: consolidated billing, portal visibility, and managed services on top of AWS subscriptions. The AWS plugin in CloudOps Software is built and tested. Configuration for production customer use is the remaining step.

## What Aptum manages vs. what AWS owns

AWS owns the physical infrastructure, global network, and platform SLAs. Aptum manages the CSP relationship, consolidated billing, portal cost visibility, and all managed services (OS patching, backup, security, FinOps) purchased as addons on top of customer AWS workloads.

## How it's delivered

Via Aptum Portal once the AWS plugin is configured for production use. AWS Direct Connect private circuits for dedicated connectivity to Aptum infrastructure are available via the Hybrid Interconnects addon.

## Technical specifications

AWS instances, EBS volumes, VPCs, and EKS clusters will be manageable through Aptum Portal once configured. Direct Connect integration available via the Hybrid Interconnects addon.

## Pricing model

Passthrough of AWS pricing plus CSP margin. Managed services addons priced independently per endpoint per month.

## When this fits (and when it doesn't)

AWS through Aptum fits customers already running AWS workloads who want consolidated billing and managed services on top. The primary assessment paths that lead here are the Hybrid Cloud Assessment (multi-cloud workload placement) and the Well-Architected Review (AWS cost and governance optimization). It does not displace AWS for cloud-native workloads integrated deeply with AWS-specific services.

## Managed services available on top

Full addon catalog compatible with AWS workloads once the plugin is configured. Same addon options as Azure.
