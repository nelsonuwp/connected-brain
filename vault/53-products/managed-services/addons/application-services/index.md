# Application Services

Two products at the application operations layer — above the OS and platform, below the customer's application code. Neither product ever touches the customer's application code, schema changes, or business data — those remain the customer's responsibility.

## Aptum Database Tuning

Query analysis, index recommendations, and capacity planning for customer database environments. Not database administration — Aptum makes recommendations; the customer implements them. Aptum never manages schema changes, application code changes, or customer data. Managed Backup is a separate addon that protects the data; Database Tuning optimizes the database's performance. At Reactive tier, automated monitoring of database availability and query response time generates performance alerting. At Proactive tier, Managed Cloud conducts DBA-level analysis, provides query optimization recommendations, develops capacity plans, and runs periodic performance review sessions. Commercial model: currently delivered as a PS engagement; evolving toward a managed addon. Owner: Managed Cloud.

## Aptum DevOps Monitoring

CI/CD pipeline health monitoring, container monitoring, and IaC drift detection. Aptum monitors and maintains the DevOps infrastructure — not the application development process. Aptum never touches the customer's application code, pipeline logic, or build dependencies. At Reactive tier, automated pipeline health checks, container monitoring, and IaC drift detection alerts are configured and running. At Proactive tier, Managed Cloud configures monitoring, proactively responds to pipeline failures, and manages IaC drift remediation. Tooling: Datadog CI Visibility or equivalent. Status: roadmap. Owner: Managed Cloud.
