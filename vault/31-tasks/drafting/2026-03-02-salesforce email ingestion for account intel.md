---
type: code
status: drafting
created: 2026-03-02
source-idea: [[2026-03-02-salesforce email ingestion for account intel]]
---

# salesforce email ingestion for account intel

## What
Add activity history and email message fetching to salesforceClient.py so source_salesforce.json includes relationship signals alongside existing structured data.

## Done When
source_salesforce.json contains activity_histories and email_messages keys in the objects dict, populated from real Salesforce data using the tested extraction patterns, with email_messages gracefully absent when Enhanced Email is not enabled in the org.

## Notes
- Working extraction code exists in salesforceTestAccountActivities.py — integration only
- Two queries: ActivityHistories subquery on Account, EmailMessage via Contact/Case IDs
- 60-day window, 500 cap on activities
- EmailMessage requires try/except — not all orgs have it enabled
- Report consumption (Account Owner, Last Touched, Roll-In section) is downstream — this task is pipeline only
- Bot/automated activity filtering happens at report time, not gather time

---

# Explore — 2026-03-03 06:55 ET

## Feasibility

**Yes, this is buildable.** The working extraction code in `salesforceTestAccountActivities.py` demonstrates the exact queries and patterns needed. The existing `salesforceClient.py` already has the OAuth2 flow, query infrastructure, and artifact-writing patterns established. This is integration work, not greenfield development.

Key evidence from context:
- `salesforceTestAccountActivities.py` shows working ActivityHistories subquery and EmailMessage fetching
- The `_query_sync` and `_query_more_sync` patterns handle pagination
- The artifact schema (`source`, `company_id`, `collected_at`, `status`, `objects`) is already established in the codebase
- The `objects` dict pattern (per-endpoint status/data) is used by other clients

**Stack alignment confirmed:** Python3, httpx, OAuth2 password flow, JSON artifacts under `outputs/temp/<run_id>/`.

---

## Unknowns and Dependencies

1. **Salesforce Account ID resolution** — How does `salesforceClient.py` currently resolve account? Does it already query by client_id → SF Account lookup, or does it receive an Account ID? The test script hardcodes `ACCOUNT_ID`. Need to confirm the lookup path.

2. **Existing `source_salesforce.json` schema** — What keys currently exist in `objects`? Need to avoid collisions and understand if `activity_histories` / `email_messages` naming is consistent with existing patterns.

3. **Contact/Case ID availability** — The EmailMessage query requires Contact IDs (and optionally Case IDs). Are these already fetched in the current SF client flow, or does this require additional queries?

4. **ActivityHistories WHERE clause support** — The test script shows a fallback pattern because some orgs don't support WHERE in the subquery. This must be preserved in integration.

5. **Rate limits and query cost** — ActivityHistories subquery + EmailMessage query + Contact ID lookup = 3-4 SOQL queries per account. Is this within acceptable bounds for batch runs?

6. **Owner data** — The note mentions "Account Owner" for report consumption. Is Owner already fetched on the Account query, or does that need to be added here?

---

## Risks

1. **Silent EmailMessage failure mode** — The spec says "gracefully absent" but the test code uses try/except that prints a warning. If the exception handling silently fails and writes an empty object with `status: success`, downstream consumers won't know the org lacks Enhanced Email vs. had no messages. Should be `status: skipped` with explanation.

2. **Activity volume explosion** — 500-record cap at 60 days is reasonable, but some accounts may have heavy automated activity (email tracking, workflow triggers). The note says "bot filtering happens at report time" — but if 90% of 500 records are bot noise, the useful signal cap is effectively much lower.

3. **Pagination for EmailMessage** — The test script handles pagination via `nextRecordsUrl`. If email volume is high (e.g., Email-to-Case accounts), this could result in many API calls. No explicit limit on EmailMessage record count.

4. **PII exposure in artifacts** — Email bodies (`TextBody`, `HtmlBody`) contain full conversation threads with signatures, phone numbers, and confidential client info. These artifacts persist on disk. Is that acceptable given downstream LLM consumption and potential logging?

5. **Date filtering inconsistency** — ActivityHistories uses `LAST_N_DAYS:60` in SOQL (when supported) or Python-side filtering (when not). EmailMessage uses `LAST_N_DAYS:60` in SOQL. If the org doesn't support WHERE on ActivityHistories but does on EmailMessage, the date ranges could drift if cutoffs are calculated differently.

6. **No deduplication with existing signals** — If Salesforce logged emails duplicate information already captured via OSINT or news sources, the signal extraction step could double-count. This is a downstream concern but worth noting.

---

## Cursor Prompt

```cursor
I need to integrate Salesforce activity history and email message fetching into the existing AccountIntel pipeline.

## Context
- Working extraction code exists in `salesforceTestAccountActivities.py` — use these exact query patterns
- Target file: `data_sources/internal/salesforceClient.py`
- Artifact output: `source_salesforce.json` under `outputs/temp/<run_id>/`
- Must follow AccountIntel artifact conventions: `objects` dict with per-endpoint `status`, `record_count`, `error`, `data`

## Requirements
1. Add `activity_histories` key to the `objects` dict in `source_salesforce.json`
   - Use ActivityHistories subquery on Account with 60-day window, 500 record limit
   - Implement the fallback pattern (no WHERE in subquery → Python-side date filtering) as shown in test script
   - Strip `attributes` recursively from all records

2. Add `email_messages` key to the `objects` dict
   - Query Contact IDs for the Account first
   - Query EmailMessage WHERE RelatedToId IN (contact_ids) AND MessageDate = LAST_N_DAYS:60
   - Handle pagination via nextRecordsUrl
   - If EmailMessage query fails (org doesn't have Enhanced Email), set `status: skipped` with error message explaining why, NOT `status: fail`

3. Preserve existing functionality — do not break current Account/Opportunity queries

4. Match the error handling and artifact writing patterns already in the codebase (single-write, finally block, never exit without writing artifact)

## Questions to answer in implementation
- How is the Salesforce Account ID currently resolved? Adapt the activity/email queries to use the same lookup.
- What fields are currently fetched on Account? Add Owner.Name if not present.

## Do not
- Implement report-side consumption (downstream task)
- Filter bot/automated activities (that happens at report time)
- Add new dependencies
```