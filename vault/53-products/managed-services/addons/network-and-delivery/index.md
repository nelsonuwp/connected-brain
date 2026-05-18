# Network and Delivery

Two products managing traffic delivery and DNS at the edge. Both sit above the physical network layer (covered under Connectivity) and operate at the application and DNS layers.

## Aptum Managed DNS (Cloudflare)

DNS management with proxy mode and edge DDoS protection via Aptum Portal, powered by Cloudflare. DNS records only — this is not routing, BGP, or network architecture management. At Reactive tier, customers manage DNS fully self-service through Aptum Portal with automated propagation and monitoring. At Proactive tier, Managed Cloud assists with complex DNS configuration and troubleshooting on request. Status: live in portal. Owner at Reactive: Aptum Portal. Owner at Proactive: Managed Cloud. Cost: included in the platform (Cloudflare approximately $35 per zone underlying, absorbed into platform cost).

## Aptum Load Balancing (L7)

Application-layer load balancing with SSL termination, health checks, and custom routing policies. L4 TCP load balancing is separately available as a self-service feature in Aptum Portal (not this addon). L7 requires application-aware configuration and active management — it is not self-service. At Reactive tier, the L7 load balancer runs continuously once configured, with automated health checks enforced. At Proactive tier, Managed Cloud configures L7 policies, SSL termination, health check rules, and routing logic, and makes changes on request. Status: L4 self-service live; L7 managed tier is roadmap. Owner: Managed Cloud.
