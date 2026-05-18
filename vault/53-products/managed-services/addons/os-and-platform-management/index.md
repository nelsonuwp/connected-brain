# OS and Platform Management

Two patching products covering the OS layer and the application platform layer above it. Neither product touches application code — that is always the customer's responsibility.

## Aptum OS Patching (Automox)

Scheduled deployment of OS and security patches across Windows Server and Linux (Debian, Ubuntu, RHEL, AlmaLinux, Rocky Linux). At Reactive tier, Automox is deployed, patches are scheduled per an agreed policy, compliance reports are generated, and the customer approves patch windows. At Proactive tier, Managed Cloud reviews patch releases, tests compatibility, defines policy, coordinates maintenance windows, and validates post-patch environments — the customer is not in the routine decision loop. Owner: Managed Cloud for cloud and virtual OS layers; Compute Platforms for Aptum infrastructure OS layers. Cost: approximately $7 CAD per endpoint per month (Automox approximately $5 USD).

## Aptum Platform Patching

Updates to middleware and runtime environments: Node.js, Java, .NET, Python, and platform services. This product sits above the OS and below the application code. Aptum never touches the customer's application code or makes schema changes — those remain the customer's responsibility. At Reactive tier, automated patching is supported where tooling allows, with compliance reports generated. At Proactive tier, Managed Cloud tests platform updates, coordinates staged rollouts, validates application behavior post-patch, and handles major version changes with customer sign-off. Owner: Managed Cloud. Pricing TBD; currently delivered within the Managed Cloud Platform tier.
