---
type: reference
created: 2026-04-16
source: "APTUM DBRG FY26 Q2 Board Deck (March 25, 2026)"
---

# FY26 Operations OKRs

*Extracted from the Q2 Board Deck presented March 25, 2026. These are the board-visible targets Adam's service network is measured against.*

---

## Data Center Operations (George Revie)

**Objective:** Realize the 5-year DC strategy, mitigate infrastructure risks, optimize direct costs.

| OKR Target | Metric | Status (as of Q2 Board) |
|------------|--------|------------------------|
| FY26 cost reduction | $680K | $646K in-year committed; $1.9M annualized run-rate |
| Uptime | 99.999% | H1: 6 Major / 15 Minor incidents, all resolved, zero SLA credits |
| SLA adherence | 98% | On track — zero SLA credits in H1 |
| R&M reduction | ↓ 10% | Tracking (no specific number reported at board) |

**5-Year DC Plan:** $10.6M total savings (F26: $646K · F27–28: $2.8M · F29–30: $7.1M)

**H2 Key Deliverables:**
- Portsmouth strategy & capacity optimization (~1,091 services)
- Centrilogic customer onboarding: 15 UK colo customers, ~C$70K/mo MRC (~C$846K annualized), 48% on expired contracts
- Basis migration (begins Q3, execution Q4)
- eStruxture consolidation (financial impact began May 1 — $161K/mo savings, $1.9M annualized)
- Q4: ATL→Herndon ($1.5M 5-yr savings), LAX→DataBank (NPV $681K), Heathrow renewal

---

## Networking (Ben Kennedy)

**Objective:** Reliable network, efficient operations, clearly defined services.

| OKR Target | Metric | Status (as of Q2 Board) |
|------------|--------|------------------------|
| Uptime | 99.999% | On track |
| Vendor support costs | ↓ 60% | Tracking |
| Backbone costs | ↓ 10% | 14/16 circuits replaced |
| POPs reduction | ↓ 75% | Miami + Ashburn eliminated ($30K/mo → $0) |
| Annualized savings | C$761K budgeted | Tracking at C$994K actual (+$172K ahead) |

**H2 Key Deliverables:**
- Equinix UK POP elimination (same playbook as US POPs)
- PCI software upgrades: 15% → 70% on current software; PCI/ISO audit targeted Q3
- Connectivity changes complete; NA legacy SKU migration final step
- Q4: Router refresh (~$850K capital, eliminates recurring maintenance), network service datasheets, FY27 budget

---

## Hosting / Compute (Martin Tessier)

**Objective:** Reliable infrastructure, enhance margins by managing COGS, grow new product offering.

| OKR Target | Metric | Status (as of Q2 Board) |
|------------|--------|------------------------|
| Ignite customer margin | ~74% compute margin (vs ~37% hosting avg) | 7 new logos, C$39K MRR committed |
| VMware→Proxmox savings | C$339K/yr annualized | Internal migration complete |
| AptCloud maturity | Move toward Beta | Alpha on excess server inventory |

**H2 Key Deliverables:**
- AptCloud rollout + Aptum IaaS GTM (CloudStack/KVM, zero VMware licensing)
- Ignite + Centrilogic compute opportunities migration
- Q3: Imperva renewal, Alert Logic renewal (evaluate consolidation & cost reduction)
- Q4: Dell OMSA (server lifecycle management), DataDomain refresh (storage), AptCloud operational readiness review before exiting Alpha
- Deferred from H1: EOL DCC, ESXi 9 (pending testing), Next Gen Linux (Rocky/RHEL/Alma 10)

**Board Context:** Ignite customers at C$39K MRR and ~74% margin = ~C$346K gross profit annualized. SCADAcore: $25K/mo, 36-month contract. This is the proof point that the CloudStack/KVM platform works commercially.

---

## Expert Services — Service Desk & Managed Services (Jason Auer / Andrei / Lacie)

**Objective:** Profitability through service excellence, customer trust & retention, enable growth via hybrid cloud.

| OKR Target | Metric | Status (as of Q2 Board) |
|------------|--------|------------------------|
| Cost savings | $500K | H1 savings on track; Tivoli→Veeam, LogicMonitor, Edgio |
| SLA/SLO adherence | 90% | H1: zero SLA credits |
| Customer revenue retention | ≥95% | Renewals workflow being operationalized |
| Business Reviews | Top 30 accounts | Targeting 100% of top 20 by revenue + 10 strategic growth |

**H2 Key Deliverables:**
- Azure specialization: 3 certifications in progress (Security Engineer, DevOps Expert, DB Admin); need 3 net new Azure customers
- Standardized Business Reviews + CSAT program operationalized
- Revenue retention: 90-day pre-renewal reviews, revenue-based escalation tiers
- Service guide refresh: consistent "what we do" documentation across all offerings
- Shift/on-call model redesign to maintain SLAs while reducing overtime
- AWS margin improvement: 3%→8% effective April 1 (~C$121K annualized)

**Note:** "Expert Services" in the board deck spans Service Desk (Jason), Managed Cloud (Andrei), and HSDM (Lacie). The $500K savings target and 90% SLA/SLO are shared across these teams. Jason's team is specifically accountable for: operational SLA performance, shift model optimization, and customer-facing support quality. The business review and CSAT targets are shared with Lacie's HSDM function.

---

## Cross-Cutting: Service Network Context

From the board deck (Slide 40): 9 service nodes with explicit accountability chains.
- George = physical infrastructure
- Martin = configuration/compute platforms
- Ben = network
- Andrei = managed cloud
- Jason = service desk/NOC
- Pat = architecture/professional services
- Jorge = operational intelligence (data)
- Lacie = HSDM/customer success

**Board-level principle:** "People can be responsible across teams, but accountability lies within the team."

---

*Source: vault/32-okrs/q3fy23/Final-APTUM_ March Q2 Board deck_INTERNAL.pptx — Slides 24-27 (H1 results), 40-46 (H2 look forward)*
