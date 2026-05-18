# Connectivity

Aptum connectivity covers MPLS, internet ports, BGP transit, cross-connects, and fiber circuits. It is the networking layer that connects customers to the internet, to hyperscalers, and to each other across Aptum's data center footprint.

## What it is (and what it is not)

Connectivity is the physical and logical network circuit. It is not hardware management, not a firewall, and not DDoS protection (the DDoS Protection addon is a separate purchase). A connectivity circuit does not include managed routing policy — that falls under the Managed Firewall addon. BGP configuration and routing health are included in the Fundamental guarantee; policy design and rule changes are not.

## What's always included (Fundamental guarantee)

BGP and routing healthy, 99.999% uptime SLA maintained. Service Desk receives monitoring alerts from the Network team and escalates incidents for resolution. Network connectivity issues are escalated to the Networking team as the owning team.

## How it's delivered

Manual provisioning by the Networking team. Portal visibility into bandwidth utilization and uptime reporting is on the roadmap. Cross-connects require physical cabling in the meet-me-room by Data Center Ops.

## Technical specifications

MPLS and internet port options from 10Mbps to 10Gbps and above. BGP transit with full routing table. Cross-connects to 15+ carriers at major sites (Toronto Pullman, Herndon). Sub-2ms latency to TorIX from Toronto. Private MPLS connectivity available between Aptum data center locations.

## Pricing model

Per port, per Mbps committed, or per circuit depending on service type. Contract-based with burst pricing available on internet ports. Cross-connect pricing varies by carrier and cage location.

## When this fits (and when it doesn't)

Connectivity fits any customer requiring network access through Aptum's infrastructure. It is commonly purchased alongside colocation, bare metal, or IaaS products. It also enables the Hybrid Interconnects addon for private circuit connections to Azure, AWS, or GCP. It is not a managed network service — customers who need Aptum to actively manage routing policy and firewall rules need the Managed Firewall addon.

## Managed services available on top

DDoS Protection (always-on volumetric scrubbing at the network edge) is available on connectivity circuits at all engagement tiers. The Hybrid Interconnects addon uses connectivity circuits as the physical layer for private hyperscaler connections. Managed Firewall is available for policy management on top of the physical circuit.
