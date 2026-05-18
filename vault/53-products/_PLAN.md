# 53-products Rewrite Plan
**Status:** Ready to execute on "go"
**Goal:** Completely restructure `53-products/` to match the Confluence hierarchy defined in `_confluence-hierarchy.html`, so every page is written and positioned correctly for the bridge to sync via gfl.

---

## How the bridge works (critical constraints)

- `_bridge.py` maps `53-products/` → `product-strategy-gfl/docs/` → Confluence via gfl
- Any file or folder whose name starts with `_` is excluded from sync (safe scratchpad)
- `index.md` inside a folder = content for that folder's Confluence parent page
- Standalone `.md` files = individual Confluence leaf pages
- Folder/file names are slugified (lowercased, spaces/underscores → hyphens)
- **The bridge does not delete Confluence pages** — orphaned old pages need manual cleanup after push

## Confluence pages to manually delete after push

These currently exist in the PRD space but will be superseded by the new structure:

| Current Confluence page | ID | Action |
|---|---|---|
| AptCloud - Aptum IaaS | 5257330696 | Delete (replaced by `aptum-portal/`) |
| AptCloud - Aptum IaaS PRD | 5257560073 | Delete (replaced by `aptum-portal/aptum-portal-prd.md`) |
| AptCloud - Aptum IaaS Strategy | 5257494536 | Delete (replaced by `aptum-portal/aptum-portal-strategy-and-roadmap.md`) |
| Managed Services Catalog | 5257560095 | Delete (replaced by `managed-services/index.md`) |
| Aptum Product Strategy | 5257461765 | Delete (replaced by `strategy-and-icp/aptum-product-strategy.md`) |
| Aptum ICP | 5257363460 | Delete (replaced by `strategy-and-icp/aptum-icp.md`) |

---

## Source key

| Symbol | Meaning |
|---|---|
| `MOVE` | File already exists — copy to new path, delete old |
| `RENAME+MOVE` | File exists — copy with new filename to new path, delete old |
| `SYNTH` | Write by extracting/rewriting from an existing source doc |
| `CLEANSE` | File exists in STG folder — copy and remove all STG brand references |
| `NEW` | Write from scratch |

---

## Target folder structure

```
53-products/
├── _bridge.py                              (leave as-is)
├── _confluence-hierarchy.html             (leave as-is)
├── _PLAN.md                               (leave as-is)
├── _supplemental-data/                    (leave as-is)
├── index.md                               (PRD Space root — leave/update)
├── strategy-and-icp/
│   ├── index.md
│   ├── aptum-product-strategy.md
│   └── aptum-icp.md
├── infrastructure-products/
│   ├── index.md
│   ├── colocation/
│   │   └── index.md
│   ├── bare-metal-servers/
│   │   └── index.md
│   ├── connectivity/
│   │   └── index.md
│   ├── aptum-iaas-shared-cluster-vpc/
│   │   └── index.md
│   ├── aptum-iaas-dedicated-cloud/
│   │   └── index.md
│   ├── aptum-iaas-private-cloud/
│   │   └── index.md
│   └── public-cloud/
│       ├── index.md
│       ├── azure/
│       │   └── index.md
│       ├── aws/
│       │   └── index.md
│       └── gcp/
│           └── index.md
├── aptum-portal/
│   ├── index.md
│   ├── aptum-portal-strategy-and-roadmap.md
│   └── aptum-portal-prd.md
├── managed-services/
│   ├── index.md
│   └── addons/
│       ├── index.md
│       ├── monitoring-and-observability/
│       │   └── index.md
│       ├── os-and-platform-management/
│       │   └── index.md
│       ├── data-protection-and-recovery/
│       │   └── index.md
│       ├── security-services/
│       │   └── index.md
│       ├── cloud-and-hybrid-connectivity/
│       │   └── index.md
│       ├── logging/
│       │   └── index.md
│       ├── network-and-delivery/
│       │   └── index.md
│       ├── application-services/
│       │   └── index.md
│       └── managed-productivity/
│           └── index.md
└── professional-services/
    ├── index.md
    ├── execute.md
    └── advisory-assess/
        ├── index.md
        ├── infrastructure-risk-and-readiness/
        │   ├── index.md
        │   ├── deliverable-scope.md
        │   └── delivery-guide.md
        ├── hybrid-cloud/
        │   ├── index.md
        │   ├── deliverable-scope.md
        │   └── delivery-guide.md
        ├── security-posture-and-compliance/
        │   ├── index.md
        │   ├── deliverable-scope.md
        │   └── delivery-guide.md
        ├── cloud-repatriation/
        │   ├── index.md
        │   ├── deliverable-scope.md
        │   └── delivery-guide.md
        ├── operational-maturity/
        │   ├── index.md
        │   ├── deliverable-scope.md
        │   └── delivery-guide.md
        ├── app-and-platform-modernization/
        │   ├── index.md
        │   ├── deliverable-scope.md
        │   └── delivery-guide.md
        └── well-architected-review/
            ├── index.md
            ├── deliverable-scope.md
            └── delivery-guide.md
```

---

## Phase 1 — Restructure (file moves, no writing)

Create all folders. Move existing files. Delete old locations.

```
CREATE  strategy-and-icp/
MOVE    aptum-product-strategy.md          → strategy-and-icp/aptum-product-strategy.md
MOVE    aptum-icp.md                       → strategy-and-icp/aptum-icp.md

CREATE  aptum-portal/
MOVE    aptcloud-aptum-iaas/aptcloud-aptum-iaas-strategy.md  → aptum-portal/aptum-portal-strategy-and-roadmap.md
MOVE    aptcloud-aptum-iaas/aptcloud-aptum-iaas-prd.md       → aptum-portal/aptum-portal-prd.md
DELETE  aptcloud-aptum-iaas/  (whole folder, including empty index.md)

CREATE  infrastructure-products/
CREATE  infrastructure-products/colocation/
CREATE  infrastructure-products/bare-metal-servers/
CREATE  infrastructure-products/connectivity/
CREATE  infrastructure-products/aptum-iaas-shared-cluster-vpc/
CREATE  infrastructure-products/aptum-iaas-dedicated-cloud/
CREATE  infrastructure-products/aptum-iaas-private-cloud/
CREATE  infrastructure-products/public-cloud/
CREATE  infrastructure-products/public-cloud/azure/
CREATE  infrastructure-products/public-cloud/aws/
CREATE  infrastructure-products/public-cloud/gcp/

CREATE  managed-services/
CREATE  managed-services/addons/
CREATE  managed-services/addons/monitoring-and-observability/
CREATE  managed-services/addons/os-and-platform-management/
CREATE  managed-services/addons/data-protection-and-recovery/
CREATE  managed-services/addons/security-services/
CREATE  managed-services/addons/cloud-and-hybrid-connectivity/
CREATE  managed-services/addons/logging/
CREATE  managed-services/addons/network-and-delivery/
CREATE  managed-services/addons/application-services/
CREATE  managed-services/addons/managed-productivity/

CREATE  professional-services/
CREATE  professional-services/advisory-assess/
CREATE  professional-services/advisory-assess/infrastructure-risk-and-readiness/
CREATE  professional-services/advisory-assess/hybrid-cloud/
CREATE  professional-services/advisory-assess/security-posture-and-compliance/
CREATE  professional-services/advisory-assess/cloud-repatriation/
CREATE  professional-services/advisory-assess/operational-maturity/
CREATE  professional-services/advisory-assess/app-and-platform-modernization/
CREATE  professional-services/advisory-assess/well-architected-review/

NOTE: managed-services-catalog.md stays at root temporarily as a source — delete at end of Phase 5
```

---

## Phase 2 — Intro / landing pages (SYNTH, short)

These are lightweight section intros. Write each from the sources noted.

| File | Source | Notes |
|---|---|---|
| `index.md` | Current `index.md` | Update or replace with brief PRD space landing |
| `strategy-and-icp/index.md` | `aptum-product-strategy.md` (Vision & Mission, The Position — first 2 sections) | 2-3 para intro pointing to the two sub-pages |
| `professional-services/index.md` | `aptum-product-strategy.md` (Motion 1 + 2, Advisory/Execute Distinction table, Evolve SOW) | Cover both motions + 3 commercial types (Fixed, T&M, Evolve) |

---

## Phase 3 — Aptum Portal landing (SYNTH)

| File | Source |
|---|---|
| `aptum-portal/index.md` | `aptum-portal/aptum-portal-prd.md` Section 1 (Executive Summary) + `aptum-product-strategy.md` (Portal Strategy section) |

The two sub-pages (`aptum-portal-strategy-and-roadmap.md`, `aptum-portal-prd.md`) already have content from Phase 1.

---

## Phase 4 — Infrastructure product pages (SYNTH, use template)

Each `index.md` follows the infrastructure page template in `_confluence-hierarchy.html`.
Primary source for all: `managed-services-catalog.md` (Infrastructure Commodities table) + `aptum-product-strategy.md` (Pillar 2 taxonomy section) + `aptum-portal/aptum-portal-prd.md` (for IaaS/portal products).

Write in this order:

| File | Primary source sections | Key content |
|---|---|---|
| `infrastructure-products/index.md` | `managed-services-catalog.md` intro + Infrastructure Commodities table | Catalog overview, Fundamental guarantee concept, tenancy model, DC footprint |
| `infrastructure-products/colocation/index.md` | `managed-services-catalog.md` Colocation row | Rack units, power, cooling, Fundamental, provisioning, pricing |
| `infrastructure-products/bare-metal-servers/index.md` | `managed-services-catalog.md` Bare Metal row + Cost Structure section | Mandatory SD layer, 6-component cost model, contract terms |
| `infrastructure-products/connectivity/index.md` | `managed-services-catalog.md` Connectivity row | MPLS, internet, BGP, SLA, monitoring |
| `infrastructure-products/aptum-iaas-shared-cluster-vpc/index.md` | `aptum-portal-prd.md` VPC section + `managed-services-catalog.md` Shared Cluster row + `aptum-product-strategy.md` Pillar 2 | KVM/CloudStack, shared physical hosts, VLAN isolation, portal delivery, pricing |
| `infrastructure-products/aptum-iaas-dedicated-cloud/index.md` | `aptum-portal-prd.md` Private Cloud section + `managed-services-catalog.md` Dedicated Cluster row + `aptum-product-strategy.md` Pillar 2 | Single-tenant, dedicated hosts, "true private cloud" positioning, board validation |
| `infrastructure-products/aptum-iaas-private-cloud/index.md` | `aptum-product-strategy.md` Pillar 2 (Private Cloud definition) + `aptum-portal-strategy-and-roadmap.md` Section 3.2 VMware/Proxmox | VMware or Proxmox, no portal requirement, Broadcom displacement angle |
| `infrastructure-products/public-cloud/index.md` | `aptum-portal-prd.md` Section 3.1 (Azure/AWS/GCP plugins) + `managed-services-catalog.md` Public Cloud row | CSP role, Fundamental guarantee, passthrough + margin model, portal integration status |
| `infrastructure-products/public-cloud/azure/index.md` | `aptum-portal-prd.md` Azure plugin section + `aptum-portal-strategy-and-roadmap.md` | Live in production (Vergent), AKS support, ExpressRoute, most mature hyperscaler integration |
| `infrastructure-products/public-cloud/aws/index.md` | `aptum-portal-prd.md` AWS plugin | Built, not yet configured in portal; Direct Connect via Hybrid Interconnects |
| `infrastructure-products/public-cloud/gcp/index.md` | `aptum-portal-prd.md` GCP plugin | Built, not yet configured in portal; Partner Interconnect via Hybrid Interconnects |

---

## Phase 5 — Managed Services section (SYNTH from catalog)

The `managed-services-catalog.md` is the primary source for all of these. It is long and detailed — extract the relevant sections for each file.

| File | Source section in managed-services-catalog.md | Notes |
|---|---|---|
| `managed-services/index.md` | Intro ("How this catalog is organized"), all three tier sections, Addon behavior by tier table, Compatibility Matrix, assessment-to-tier mapping table | Also describe Reviews & Touchpoints as part of what Proactive means (not a separate addon) |
| `managed-services/addons/index.md` | Managed Service Addons intro paragraph + Compatibility Matrix | Overview, pricing model, point to category pages |
| `managed-services/addons/monitoring-and-observability/index.md` | Monitoring & Observability table (both rows) | Name the 3 products: Aptum Essentials Monitoring (Zabbix), Aptum Advanced Monitoring (LogicMonitor), Aptum Application Monitoring (Datadog) |
| `managed-services/addons/os-and-platform-management/index.md` | OS & Platform Management table (both rows) | Aptum OS Patching (Automox), Aptum Platform Patching |
| `managed-services/addons/data-protection-and-recovery/index.md` | Data Protection & Recovery table (all 3 rows) | Aptum Managed Backup (Veeam), Aptum DRaaS, Aptum BCP Planning — and the hierarchy between them |
| `managed-services/addons/security-services/index.md` | Security Services table (all 7 rows) | Name all 7 products, clarify layer each operates at |
| `managed-services/addons/cloud-and-hybrid-connectivity/index.md` | Cloud & Hybrid Connectivity table (both rows) | Aptum Hybrid Interconnects, Aptum FinOps |
| `managed-services/addons/logging/index.md` | Operational Logging row | Aptum Operational Logging — only product here |
| `managed-services/addons/network-and-delivery/index.md` | Managed DNS row + Load Balancing (L7) row | Aptum Managed DNS (Cloudflare), Aptum Load Balancing (L7) |
| `managed-services/addons/application-services/index.md` | Database Tuning row + DevOps Monitoring & Maintenance row | Aptum Database Tuning, Aptum DevOps Monitoring — scope boundaries critical |
| `managed-services/addons/managed-productivity/index.md` | Managed Productivity (M365) row | Aptum Managed M365 — M365 SaaS layer only, not Azure infra |

After all catalog pages are written: **delete `managed-services-catalog.md` from the root**.

---

## Phase 6 — STG assessment cleanse and placement (CLEANSE)

For each assessment, read the 3 STG source files. Apply cleansing rules:
- Replace "STG" (as brand) → "Aptum"
- Replace "StoryLeader" → "structured discovery conversation" (first use) / "discovery conversation" (thereafter)
- Remove all named customer lists (SmartBear, LiquidIce, etc.) → replace "Applicable Customer Segments" section with a generic segment description based on the personas and pain signals already in the file
- Replace "STG Assessment & Commercial Playbook" → "Aptum Assessment Playbook"
- Replace "priority account set" → "target account set"
- Do NOT change pricing, t-shirt sizing, or scope content

Cleanse and write in this order. `index.md` = sell sheet content.

| Assessment folder | Source files |
|---|---|
| `advisory-assess/index.md` | `/STG/docs/engagement-workflow.md` + `/STG/docs/post-assessment-pathways.md` + `/STG/docs/README.md` |
| `advisory-assess/infrastructure-risk-and-readiness/index.md` | `/STG/docs/assessments/01-infrastructure-risk/sell-sheet.md` |
| `advisory-assess/infrastructure-risk-and-readiness/deliverable-scope.md` | `/STG/docs/assessments/01-infrastructure-risk/deliverable-scope.md` |
| `advisory-assess/infrastructure-risk-and-readiness/delivery-guide.md` | `/STG/docs/assessments/01-infrastructure-risk/delivery-guide.md` |
| `advisory-assess/hybrid-cloud/index.md` | `/STG/docs/assessments/02-hybrid-cloud/sell-sheet.md` |
| `advisory-assess/hybrid-cloud/deliverable-scope.md` | `/STG/docs/assessments/02-hybrid-cloud/deliverable-scope.md` |
| `advisory-assess/hybrid-cloud/delivery-guide.md` | `/STG/docs/assessments/02-hybrid-cloud/delivery-guide.md` |
| `advisory-assess/security-posture-and-compliance/index.md` | `/STG/docs/assessments/03-security-posture/sell-sheet.md` |
| `advisory-assess/security-posture-and-compliance/deliverable-scope.md` | `/STG/docs/assessments/03-security-posture/deliverable-scope.md` |
| `advisory-assess/security-posture-and-compliance/delivery-guide.md` | `/STG/docs/assessments/03-security-posture/delivery-guide.md` |
| `advisory-assess/cloud-repatriation/index.md` | `/STG/docs/assessments/04-cloud-repatriation/sell-sheet.md` |
| `advisory-assess/cloud-repatriation/deliverable-scope.md` | `/STG/docs/assessments/04-cloud-repatriation/deliverable-scope.md` |
| `advisory-assess/cloud-repatriation/delivery-guide.md` | `/STG/docs/assessments/04-cloud-repatriation/delivery-guide.md` |
| `advisory-assess/operational-maturity/index.md` | `/STG/docs/assessments/05-operational-maturity/sell-sheet.md` |
| `advisory-assess/operational-maturity/deliverable-scope.md` | `/STG/docs/assessments/05-operational-maturity/deliverable-scope.md` |
| `advisory-assess/operational-maturity/delivery-guide.md` | `/STG/docs/assessments/05-operational-maturity/delivery-guide.md` |
| `advisory-assess/app-and-platform-modernization/index.md` | `/STG/docs/assessments/06-platform-modernization/sell-sheet.md` |
| `advisory-assess/app-and-platform-modernization/deliverable-scope.md` | `/STG/docs/assessments/06-platform-modernization/deliverable-scope.md` |
| `advisory-assess/app-and-platform-modernization/delivery-guide.md` | `/STG/docs/assessments/06-platform-modernization/delivery-guide.md` |
| `advisory-assess/well-architected-review/index.md` | `/STG/docs/assessments/07-well-architected-review/sell-sheet.md` |
| `advisory-assess/well-architected-review/deliverable-scope.md` | `/STG/docs/assessments/07-well-architected-review/deliverable-scope.md` |
| `advisory-assess/well-architected-review/delivery-guide.md` | `/STG/docs/assessments/07-well-architected-review/delivery-guide.md` |

---

## Phase 7 — Execute page (NEW)

| File | Content |
|---|---|
| `professional-services/execute.md` | Write from `aptum-product-strategy.md` (Motion 2 section) + Evolve SOW template knowledge. Cover: Fixed SOW model (bounded scope, milestones, $5K–$300K), T&M (hourly, smaller tasks/change requests), Evolve (monthly MMF retainer, cross-functional squad in 2-week Scrum sprints). List types of work Aptum delivers. Every engagement must trace to an assessment and have a clear Operate outcome. |

---

## Phase 8 — Final checks before bridge push

- [ ] No `.md` files remain at the `53-products/` root except `index.md` (all others moved to subfolders)
- [ ] `managed-services-catalog.md` deleted from root after Phase 5 complete
- [ ] `aptcloud-aptum-iaas/` folder deleted after Phase 1
- [ ] All folders have an `index.md`
- [ ] No `_` files outside of `_bridge.py`, `_PLAN.md`, `_confluence-hierarchy.html`, `_supplemental-data/`
- [ ] All STG customer names confirmed removed from assessment files
- [ ] All "STG", "StoryLeader" references confirmed removed
- [ ] Infrastructure page template applied to all 11 infra product pages (spot-check 3)
- [ ] Run: `python3 _bridge.py push "rewrite: full 53-products restructure to new hierarchy"`

---

## Page count summary

| Phase | Pages | Type |
|---|---|---|
| Phase 1 (moves) | 5 files moved/renamed | MOVE |
| Phase 2 (landing pages) | 3 | SYNTH |
| Phase 3 (portal landing) | 1 | SYNTH |
| Phase 4 (infra products) | 11 | SYNTH + template |
| Phase 5 (managed services + addons) | 11 | SYNTH |
| Phase 6 (STG assessments) | 22 | CLEANSE |
| Phase 7 (execute) | 1 | NEW |
| **Total pages written** | **49** | |

Service guides are intentionally excluded from this run. They will be a separate engagement.
