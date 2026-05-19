# Data Protection and Recovery

Three products organized as a hierarchy: backup protects data but does not guarantee recovery time; DRaaS adds a defined recovery time objective with tested failover infrastructure; BCP Planning is the strategic continuity plan that governs both. Selling Managed Backup alone does not mean the customer can recover within an SLA — that requires DRaaS.

## Aptum Managed Backup (Veeam)

Automated backup execution, monitoring, failure alerting, and restore capability with policy-based retention. At Reactive tier, Veeam runs scheduled jobs, alerts on failures, generates success and failure reports, and customers can request restores via ticket. At Proactive tier, Managed Cloud designs backup policy, proactively investigates failures, manages restore operations, and tests recoverability before the customer needs it. Owners: Managed Cloud (policy and management); Compute Platforms (Veeam infrastructure and runbooks). Cost: approximately $14 to $20 CAD per workload per month.

## Aptum DRaaS

Defined RPO and RTO with a maintained failover environment, tested recovery runbooks, and quarterly DR tests. This product requires active secondary infrastructure — it is not just replication. At Reactive tier, backup replication to a secondary site is automated, the failover environment is maintained and monitored, and status reporting is accessible. At Proactive tier, Managed Cloud designs the DR plan, conducts quarterly DR tests, manages failover coordination, and maintains and updates runbooks proactively. Owners: Managed Cloud (plan and management); Compute Platforms (secondary infrastructure). Cost: secondary site compute and storage scoped per engagement.

## Aptum BCP Planning

Business continuity plan development, tabletop exercise facilitation, and annual review. This is the strategic plan — not the technical execution, which is DRaaS. BCP Planning is Proactive tier only. At Proactive tier, Managed Cloud develops the BCP document, supports tabletop exercises, and conducts the annual review. Owner: Managed Cloud. Commercial model: advisory and PS engagement priced per engagement.
