# Monitoring and Observability

Aptum offers three monitoring products at different layers and with different visibility models. They are complementary, not redundant — each monitors a different layer of the stack.

## Aptum Essentials Monitoring (Zabbix)

Infrastructure-layer monitoring built into the Service Desk floor. Zabbix agents run on all managed infrastructure and feed alerts to the Service Desk team. This is not a customer-facing addon — it is the monitoring Aptum runs internally to keep the infrastructure operational. Customers on a Reactive or Proactive tier benefit from this monitoring automatically. It is included in the Service Desk pricing and cannot be separately purchased or removed.

## Aptum Advanced Monitoring (LogicMonitor)

Customer-facing visibility into infrastructure monitoring data. Customers get access to dashboards showing alert history, uptime reporting, and bandwidth reports — the same data Aptum's Service Desk sees. At Reactive tier, Aptum runs standard monitoring with customer dashboard access. At Proactive tier, Aptum tunes thresholds, performs anomaly detection, and conducts monthly monitoring health reviews. Owner: Compute Platforms for infrastructure devices, Networking for network devices, Managed Cloud for cloud and virtual environments. Tooling: LogicMonitor customer portal (contracted rate TBD). Cost: approximately $11 to $20 per device per month at market rates.

## Aptum Application Monitoring (Datadog)

Full-stack observability above the OS into the application layer. Covers application performance, container health, custom dashboards, and anomaly detection. This product catches application-layer degradation that infrastructure monitoring misses — infrastructure can show healthy while application performance degrades. At Reactive tier, Datadog agent is deployed and the customer has access to their Datadog environment with automated dashboards. At Proactive tier, Managed Cloud configures custom dashboards, tunes alert rules, and proactively investigates performance anomalies, with monthly performance reviews. Owner: Managed Cloud. Cost: Datadog Infrastructure approximately $35 CAD per host; Datadog APM approximately $45 CAD per host.
