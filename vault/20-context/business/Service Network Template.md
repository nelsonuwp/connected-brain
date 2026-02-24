---
Service Name: [Enter Service Name]
Service Manager: [Enter Manager Name]
Lifecycle: [Discovery | Alpha | Beta | Live | Decommissioned]
Evolution: [Novelties | Bespoke/Custom | Product | Commodity]
---
## Service Description
*[Write description here]*

**Overview:** 
[Provide a brief overview of what the service is]

**Business Benefit:** 
[Explain the business benefit and value this service provides]

**How the Service is Used:** 
[Describe how consumers interact with or utilize the service day-to-day]

**Customer Engagement (On-board / Off-board):** 
[Describe at a high level how customers engage, request access, get onboarded, and how they are offboarded]

**Expectations of Success and Failure:** 
[Define what a customer can expect when the service is working perfectly (success) and what they should expect when it fails or degrades (failure)]

**Getting Help:** 
[Explain how to get help when the service isn't performing as expected, e.g., links to support portals, Slack channels, or ticketing systems]

---

## User Needs
*[Note: Keep these high-level, not fine-grained requirements. Avoid writing out steps in a process. Do not write out onboarding/offboarding needs. If the service meets specific targets (e.g., availability ≥ 99.999%), write that as a need.]*

**Need 1:**
* **As a** [User A or User B]
* **I need** [some activity or thing]
* **so that I can** [achieve outcome XYZ]
* **Metrics:** [Define metrics that show how this outcome is met]

**Need 2:**
* **As a** [User A or User B]
* **I need** [some activity or thing]
* **so that I can** [achieve outcome XYZ]
* **Metrics:** [Define metrics that show how this outcome is met]

---

## Service Metrics
*[Aggregated list of outcome metrics the service reports on based on the user needs above]*

* **Outcome Metrics:** 
  * [Metric 1: e.g., Uptime percentage - Target: 99.99%]
  * [Metric 2: e.g., Average response time - Target: <200ms]
* **Cost Reporting:** [How are the costs of running this service reported? e.g., Cost per transaction, monthly cloud spend dashboard]
* **Consumption Measurement:** [How is consumption measured? e.g., API calls per minute, active daily users, storage used in GB]

---

## Service Dependencies
*[List any internal or external services you need to operate this service]*

* [Dependency 1: e.g., Internal Identity & Access Management Service]
* [Dependency 2: e.g., Centralized Logging Service]
* [Dependency 3: e.g., Cloud Hosting Provider]

---

# BELOW ARE THE DEFINITIONS OF LIFECYCLE AND EVOLUTION -- THIS SECTION IS NOT PART OF THE SERVICE CONTRACT
## Lifecycle

| Discovery | Alpha | Beta | Live | Decommissioned |
| :--- | :--- | :--- | :--- | :--- |

**Lifecycle Definitions:**
* **Discovery:** Understanding the problem that needs to be solved. User needs are tested with future consumers to see if it is a problem worth solving.
* **Alpha:** Testing and validating potential implementations to understand the most suitable approach. 
* **Beta:** Actively building the service to serve the user needs identified in discovery, preparing to operate as if it were live.
* **Live:** The service is actively used by its target audience and meets operational goals.
* **Decommissioned:** The service is no longer needed and is being/has been retired.

---

## Evolution

| Novelties | Bespoke, or custom | Product | Commodity |
| :--- | :--- | :--- | :--- |

**Evolution of Services:**
An important concept from Wardley mapping that OSOM is built upon heavily is the idea of service evolution. Evolution and lifecycle are not the same; whereas lifecycle is the stage of development a service is at, evolution refers to the relationship between the organisation and the way it regards a service.

Novel services are new and have never been done before. However, they are frequently composed of other services, some of which will be built around bespoke components, some around products, and still others that use commodities.

* **Novelties:**
Novelties are services that are unique. They've rarely been considered before, or they may have some new approach that has not been attempted. In other cases, they represent a service that no other organisation offers due to statutory, or regulatory. For example, only HMRC is able to collect income tax in the United Kingdom. Novelties should be relatively uncommon in any organisation, and frequently represent a point of interaction with a customer.

* **Bespoke, or custom:**
Services that have been developed with a particular organisation in mind, but can be found in other organisations are bespoke. An example of a bespoke component might be an IVR system for a call centre.

*(More information about evolution of services will be documented soon...)*