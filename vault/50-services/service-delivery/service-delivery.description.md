# Hybrid Service Delivery Management (HSDM)

**Service Manager:** Lacie Allen-Morley
**Function:** Architecture & Delivery
**Lifecycle:** Live
**Confluence Link**: [Hybrid Service Delivery Management Service Description](https://aptum.atlassian.net/wiki/spaces/svcnet/pages/5044076554/Hybrid+Service+Delivery+Management)

> We own the project. Every SOW, every engagement, every non-recurring delivery — from scope approval to operational handoff. The single accountability point for project execution.

---

## What This Function Is

HSDM is the **project delivery function** for non-recurring work. It manages the Execute motion — taking what HSA has scoped and sold, coordinating the cross-functional resources to deliver it, and handing off to operational teams with full documentation.

Account operations (customer queues, orders, renewals, credits, cancellations) have been separated into a dedicated **Customer Success Manager (CSM)** function, also under Lacie's org. That split lets each function run with a distinct trigger model: HSDM fires on a signed SOW; CSM fires on an inbound customer need or account event.

---

## Accountable For

- Statement of Work ownership, profitability, and on-time delivery
- Coordinating Professional Services resource draws from home teams (dotted-line engagement model)
- PM overhead on all project engagements — schedule, milestone tracking, risk management
- Escalation management and stakeholder alignment during active engagements
- Post-project handoff to operational teams with full documentation and runbooks
- Ensuring projects transition cleanly to either Managed Cloud (platform-layer customers) or Service Desk (infrastructure-layer customers)

---

## Problems We Solve

- Projects slip because nobody owns the schedule
- SOW scope creep goes unmanaged
- Multiple technical teams operate in parallel without coordination
- Post-project environments are undocumented and unsupportable
- Home team SMs cannot track their seconded resources without a formal PM layer

---

## Products and Services Supported

- All Professional Services Execute engagements: cloud migrations, hardware refreshes, VMware migrations, private cloud implementations, Aptum IaaS onboarding, security remediations, repatriation projects, platform builds, DR design and implementation
- Internal PS coordination model — resource draws from contributing home teams with SM approval gate

---

## What This Team Does NOT Do

- Define technical scope or write hour estimates — that is HSA (SDMs own the SOW document; HSA owns the scope bullets and the hours)
- Execute technical deliverables — PS contributing teams do this under dotted-line coordination
- New commercial negotiations, new pricing, new logo acquisition — that is Fred's team and Marc Alex's team
- Day 2 operational ticket management — that is Service Desk
- Ongoing customer relationship management between projects — that is CSM
- Account administration: order entry, renewals, credits, cancellations — that is CSM

---

## Professional Services Operating Model

HSDM coordinates but does not own dedicated delivery headcount. Every PS engagement works as follows:

1. HSA defines technical scope and estimates; HSDM adds PM overhead to produce the SOW
2. HSDM identifies required skills and requests resources from relevant home team SMs
3. Each home team SM formally approves before their team member is seconded
4. Seconded resources work under HSDM coordination for the duration of the engagement
5. Home team SM retains quality accountability for their seconded team member
6. HSDM owns overall engagement quality and delivery accountability end to end
7. At project close, HSDM manages handoff to Managed Cloud or Service Desk with documentation
8. Customer relationship continuity (post-handoff) transitions to CSM

---

## Relationship to CSM

HSDM and CSM are two distinct functions under the same leader (Lacie). They operate on different triggers and different timelines:

| Dimension | HSDM | CSM |
|---|---|---|
| Trigger | Signed SOW | Customer queue, order, or account event |
| State of business | Non-recurring (project) | Recurring (ongoing) |
| Customer touchpoint | Active during the engagement | Always-on between engagements |
| Success metric | On-time, on-budget delivery | Retention, satisfaction, account health |

At project close, HSDM hands the customer to CSM. At the start of a new engagement, CSM hands the customer back to HSDM.

---

## Financial Model

### Revenue Touch
- Owns PS revenue: ~$738K YTD (F26)
- Directly accountable for project gross margin

### Direct Cost Driver
- Lacie plus SDMs — labor is the primary cost
- PS resource costs flow through contributing team cost centers, not HSDM

### Margin Profile
- PS gross margin: 29.2% — second-highest in the portfolio
- Margin at risk if projects slip due to resource contention with BAU operations
- Scope creep that exceeds SOW hours without a change order is direct margin erosion

### How We Are Measured
| Metric | Target |
|---|---|
| Project delivery on-time | ≥95% |
| Revenue variance vs. SOW | ≤5% |
| Customer satisfaction score (post-project) | ≥4.5/5.0 |
| Escalation rate | ≤2% of total interactions |
| SOW turnaround time | To be defined |
| Estimate accuracy | To be defined |

---

## Key Dependencies

| Dependency | Direction | Notes |
|---|---|---|
| Hybrid Solution Architecture | Inbound | Receives scope and budget for every SOW |
| CSM | Lateral | Hands customer to CSM at project close; receives back at new engagement start |
| Service Desk | Outbound | Target handoff destination for infrastructure-layer customers |
| Managed Cloud | Outbound | Target handoff destination for platform/cloud customers |
| Compute Platforms | Outbound | Buys provisioning capacity at agreed project milestones |
| Data Center Ops | Outbound | Buys physical facility and remote hands capacity |
| Network | Outbound | Buys connectivity capacity |
| Commercial (Fred's team) | Lateral | Receives customer handoffs at project close; hands back commercial signals |
| Finance | Lateral | Project cost tracking and profitability reporting |
