---
type: schema
object: FuzionBridge API
updated: 2026-04-08
---

# FuzionBridge API

**Base URL:** `https://jsmintegrationtor01.corp.peer1.net`
**Spec:** OpenAPI 3.1.0 — `/openapi.json`
**Auth:** OAuth2 password flow — POST form credentials to `/auth/token`, use `Bearer` token in `Authorization` header
**Credentials:** `APTUM_USER` / `APTUM_PASS` (see `.env`)
**SSL:** Internal corp cert — disable SSL verification for local calls

---

## Authentication

### POST /auth/token

Authenticate and receive an access token. Token lifetime: 1800s (30 min).

**Request:** `application/x-www-form-urlencoded`

| Field | Type | Required |
|-------|------|----------|
| username | string | YES |
| password | string | YES |

**Response:**

```json
{
  "access_token": "...",
  "token_type": "bearer",
  "issued_at": "2026-04-08T11:55:37.707172",
  "expires_at": "2026-04-08T12:25:37.707172",
  "expires_in_seconds": 1800
}
```

> **Note:** Response does not include a `refresh_token`. The `/auth/refresh` endpoint exists but is not usable with this auth flow.

---

## GET /health/

No auth required. Returns API and dependency health status.

**Response:**
```json
{ "status": "ok" }
```

---

## Customers

### GET /v1/customer/

Retrieve customers with optional filters and embedded sub-resources.

**Query parameters:**

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| customer_ids | string | — | Comma-separated customer IDs to fetch specific customers |
| include_services | bool | false | Embed services array on each customer |
| include_contacts | bool | false | Embed contacts array on each customer |
| include_history | bool | false | Embed history array on each customer |
| page | int | 1 | Min: 1 |
| limit | int | 50 | Min: 1, Max: 100 |
| active | bool | — | Filter by active status |
| created_after | string | — | ISO datetime |
| created_before | string | — | ISO datetime |
| updated_after | string | — | ISO datetime |
| updated_before | string | — | ISO datetime |

**Response top-level keys:** `page`, `limit`, `total_customers` (inferred), `isLastPage`, `customers[]`

**Customer object fields:**

| Field | Type | Notes |
|-------|------|-------|
| customer_id | int | Primary key; maps to `client_id` in Ocean |
| company_name | string | |
| active | bool | |
| blacklisted | bool | |
| customer_type | string | |
| industry | string | |
| support_tier | string | |
| created | datetime | FuzionBridge record creation date — NOT meaningful as business date |
| last_updated | datetime | |
| inactive_since | datetime/null | |
| services | array/null | Present when `include_services=true` |
| contacts | array/null | Present when `include_contacts=true` |
| history | array/null | Present when `include_history=true` |

**Usage notes:**
- `customer_id` here = `client_id` in Ocean/dimServices — same integer, different column name
- `active=true` filters to currently active customers only
- Fetch a single customer with all includes: `?customer_ids=7013372&include_services=true&include_contacts=true&include_history=true`

---

## Services

### GET /v1/services/

Retrieve services with optional filters. Returns all statuses (Online + Deprovision) in a single call — no status filter needed.

**Query parameters:**

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| customer_id | int | — | Filter to one customer (recommended — always filter by customer) |
| include_status | string | — | Filter IN by status value |
| exclude_status | string | — | Filter OUT by status value |
| created_after | string | — | ISO datetime |
| created_before | string | — | ISO datetime |
| updated_after | string | — | ISO datetime |
| updated_before | string | — | ISO datetime |
| page | int | 1 | |
| limit | int | 50 | Max: 100 |

**Response top-level keys:** `page`, `limit`, `total_services`, `isLastPage`, `services[]`

**Service object fields:**

| Field | Type | Notes |
|-------|------|-------|
| service_id | int | Primary key; same value as Ocean `service_id` |
| status | string | "Online" \| "Deprovision" — "Reclaim" not yet confirmed in response |
| products_name | string | Maps to Ocean `dimServices.product` |
| product_line | string | Maps to Ocean `line_of_business` (NOT `adjusted_line_of_business`) |
| service_type | string | e.g. "server", "clustering", "SAN", "colocation" |
| nickname | string/null | |
| datacenter | string | Datacenter code e.g. "POR" — maps to Ocean `datacenter_code` |
| customer_id | int | |
| currency | string | Native billing currency e.g. "GBP", "USD", "CAD" |
| mrc | string (decimal) | Native currency MRC — live billing value; may diverge from Ocean snapshot |
| created | datetime | **FuzionBridge import date, not provision date** — all records show `2025-02-24`; use Ocean `provision_date` instead |
| last_updated | datetime | |
| options | array | Component breakdown — see below |

**Options (component) array fields:**

| Field | Type | Notes |
|-------|------|-------|
| id | int | Maps to `dimComponents.integer_key` — confirmed join key |
| option | string | Component name; maps to `dimComponents.component` |
| type | string | Maps to `dimComponents.service_option_type` e.g. "os", "processor", "hdd", "ram", "backup" |
| quantity | int | |
| capacity | string/null | e.g. "300" (GB), "2000" (MB) |
| rate | null | Not populated in observed data |
| mrc | string (decimal) | Component MRC in service's native currency |

**Usage notes:**
- **No separate MRC call needed** — component MRC is embedded in `options[].mrc`. Skip `/v1/mrc/service` unless you specifically need the `total_mrc` rollup.
- `product_line` ≠ `adjusted_line_of_business`. FuzionBridge has no equivalent of `adjusted_lob`.
- `created` is always the FuzionBridge data import date (`2025-02-24`). Use Ocean `provision_date` for actual provisioning date.
- CAD MRC is not available — use Ocean `dimServices.cad_mrc`.
- `server_name`, `os` (clean field), `fusion_id`, `adjusted_lob`, `provision_date` are **not available** — fetch from Ocean.

---

## Client Relations

### GET /v1/client-relations/relations

Returns relationship data for a customer.

**Required:** `customer_id` (int)

### GET /v1/client-relations/tams

Returns TAM (Technical Account Manager) assignments for a customer.

**Required:** `customer_id` (int)

### GET /v1/client-relations/

Returns full client relations summary including both relations and TAMs.

**Required:** `customer_id` (int)

---

## Contacts

### GET /v1/contacts/

Retrieve contacts with optional filters.

**Query parameters:**

| Parameter | Type | Notes |
|-----------|------|-------|
| customer_id | int | Filter to one customer |
| contact_id | int | Fetch a specific contact |
| created_after / created_before | string | ISO datetime |
| updated_after / updated_before | string | ISO datetime |
| page | int | Default: 1 |
| limit | int | Default: 50 |

**Response top-level keys:** `page`, `limit`, `total_contacts` (inferred), `isLastPage`, `contacts[]`

---

## MRC (Monthly Recurring Charges)

### GET /v1/mrc/service

Per-service MRC with optional component breakdown.

**Required:** `service_id` (int)
**Optional:** `detailed` (bool) — include per-option MRC breakdown

**Response:**
```json
{
  "type": "service_id",
  "service_id": 4487195,
  "currency": "GBP",
  "total_mrc": "357.22",
  "details": {
    "top_level_mrc": "164.02",
    "options": [
      { "id": 10522749, "description": "8GB 1600 Mhz DDR3 ECC RDIMM", "mrc": "38.89", "currency": "GBP" }
    ]
  }
}
```

> **Note:** This is largely redundant with the `options[]` embedded in `/v1/services/`. The options array in `/v1/services/` has more fields (`type`, `quantity`, `capacity`) and should be preferred. Use this endpoint only if you need `total_mrc` as a pre-computed rollup.

### GET /v1/mrc/customer

Total MRC for a customer, broken down by currency.

**Required:** `customer_id` (int)
**Optional:** `datacenter` (string), `statuses` (string)

**Response:**
```json
{
  "customer_id": 7013372,
  "datacenter": "All",
  "currency_breakdown": { "GBP": "21652.41" }
}
```

### GET /v1/mrc/datacenter

Datacenter-level MRC rollup across all customers.

**Optional:** `datacenter` (string), `global_currency` (string), `include_customers` (bool), `statuses` (string)

---

## Search

### GET /v1/search/

Cross-collection search.

**Required:** `collections` (string) — collection name(s) to search; e.g. `"customers"`, `"services"`, `"contacts"`

**Optional query parameters:**

| Parameter | Type | Notes |
|-----------|------|-------|
| filters | string | Filter expression |
| projections | string | Fields to return |
| created_after / created_before | string | ISO datetime |
| updated_after / updated_before | string | ISO datetime |
| sort_by | string | Field to sort by |
| sort_order | int | **Integer:** `-1` = descending, `1` = ascending |
| page | int | Default: 1 |
| limit | int | Default: 50 |
| include_id | bool | Include internal `_id` field |

---

## History

### GET /v1/history/

Retrieve change history records.

**Query parameters:**

| Parameter | Type | Notes |
|-----------|------|-------|
| customer_id | int | Filter to one customer |
| sections | string | Filter by section type (e.g. "services") |
| timestamp_after / timestamp_before | string | ISO datetime |
| filter | string | Additional filter expression |
| sort_by | string | Field to sort by |
| sort_order | int | **Integer:** `-1` = descending, `1` = ascending |
| page | int | Default: 1 |
| limit | int | Default: 50 |

**Response top-level keys:** `page`, `limit`, `total_history`, `isLastPage`, `history_entries[]`

**History entry fields:**

| Field | Type | Notes |
|-------|------|-------|
| _id | string | MongoDB ObjectId — use as `objectid` for PUT /v1/history/update |
| customer_id | int | |
| timestamp | datetime | |
| section | string | e.g. "services" |
| changes | object | `{ added: [], removed: [], updated: [{ id, changes: { added, removed, updated } }] }` |
| tags | array | |

### PUT /v1/history/update/{objectid}

Merge additional data into an existing history record.

**Path:** `objectid` (string) — the `_id` from a history entry

**Body:** `application/json`
```json
{ "data": { "key": "value" } }
```

---

## Order Tickets

Maps FuzionBridge service IDs to JSM (Jira Service Management) ticket keys.

### GET /v1/order-tickets/

List order ticket mappings.

**Optional:** `customer_id` (int), `service_id` (int), `page` (int), `limit` (int)

**Response:** array of order ticket objects

### POST /v1/order-tickets/

Create a new order ticket mapping.

**Body:** `application/json`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| service_id | int | YES | FuzionBridge service ID |
| customer_id | int | YES | |
| jsm_ticket_key | string | YES | e.g. "OO-123" |
| jsm_ticket_id | string | YES | JSM internal ticket ID |
| status | string | YES | Initial status that triggered creation |

### GET /v1/order-tickets/{service_id}

Retrieve order ticket mapping by service ID. Returns 404 if none exists.

### PUT /v1/order-tickets/{service_id}

Update status and/or ticket key on an existing mapping.

**Body:** `application/json`

| Field | Type | Required |
|-------|------|----------|
| status | string | YES |
| jsm_ticket_key | string | NO |

### DELETE /v1/order-tickets/{service_id}

Delete an order ticket mapping. Returns 404 if none exists.

---

## Known Gotchas

| Issue | Detail |
|-------|--------|
| `created` ≠ `provision_date` | FuzionBridge `created` on services is the data import date (`2025-02-24` for all records). Use Ocean `dimServiceAttributes.provision_date`. |
| `mrc` diverges from Ocean | FuzionBridge reflects live billing; Ocean `dimServices.mrc` is a datamart snapshot. Use Ocean `cad_mrc` for CAD financials. |
| `product_line` ≠ `adjusted_line_of_business` | FuzionBridge `product_line` maps to Ocean `line_of_business` only. `adjusted_line_of_business` is Ocean-only. |
| No CAD conversion | FuzionBridge returns native currency only. All CAD amounts come from Ocean. |
| `sort_order` is an integer | `/v1/search/` and `/v1/history/` take `sort_order` as int (`-1`/`1`), not a string. Passing `"desc"` returns a 422. |
| `customer_id` vs `client_id` | FuzionBridge uses `customer_id`; Ocean uses `client_id`. Same integer value, different name. |
| Missing fields | `server_name`, `os` (clean), `fusion_id`, `provision_date`, `adjusted_lob`, `cad_mrc` are not in FuzionBridge — all require Ocean. |
| Reclaim status | Functionally identical to Deprovision for churn purposes (automated deprovisioning failed). Not yet confirmed as a distinct `status` value in FuzionBridge responses. |

---

## Reference

- Live spec: `https://jsmintegrationtor01.corp.peer1.net/openapi.json`
- Kitchen sink script: `docs/reference/code/fuzion/fuzion-kitchen-sink.py`
- Sample outputs: `docs/reference/code/fuzion/outputs/`
