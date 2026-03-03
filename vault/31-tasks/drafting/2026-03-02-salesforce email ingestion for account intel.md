---
type: code
status: drafting
created: 2026-03-02
source-idea: [[2026-03-02-salesforce email ingestion for account intel]]
---

# salesforce email ingestion for account intel

## What
Add activity history and email message fetching to salesforceClient.py 
so source_salesforce.json gains two new object keys (activity_histories, 
email_messages), map them through the legacy envelope in gather.py, and 
add a dedicated activity signal extractor that feeds unified_signals.json.

## Done When
1. source_salesforce.json contains activity_histories and email_messages 
   keys in objects, each a valid SourceObject (status/record_count/error/data)
2. gather.py _map_to_legacy_envelope maps them to 
   raw_data["salesforce"]["data"]["ActivityHistories"] and ["EmailMessages"]
3. A new extract_salesforce_activity_signals() function in 
   signal_primitives.py (or signals.py) produces signal primitives from 
   activity data and merges into unified_signals.json
4. email_messages status is "skipped" (not "fail") when Enhanced Email 
   is not enabled in the org
5. Existing Account/Opportunities/Contacts behavior is unchanged — 
   verified by running pipeline against a test account

## Notes

### Architecture decisions (resolved)
- Fetch inside salesforceClient.fetch_data() — Option A from flow doc. 
  Account Id is already resolved by the existing Client_ID__c query; 
  use that Id for the ActivityHistories subquery and EmailMessage lookup
- Single artifact — activity_histories and email_messages go into the 
  existing source_salesforce.json objects dict alongside account, 
  opportunities, contacts. No new artifact file.
- Legacy envelope — add to _map_to_legacy_envelope in gather.py:
    data["ActivityHistories"] = (objects.get("activity_histories") or {}).get("data") or []
    data["EmailMessages"] = (objects.get("email_messages") or {}).get("data") or []
- Signal strategy — new function extract_salesforce_activity_signals() 
  (Option 2 from flow doc), called from _extract_deterministic_signals() 
  in signals.py, merged into all_signals

### Extraction spec
- ActivityHistories: subquery on Account, LAST_N_DAYS:60, ORDER BY 
  ActivityDate DESC, LIMIT 500. Fallback pattern required (some orgs 
  reject WHERE in subquery — omit WHERE, filter by date in Python).
  Strip attributes recursively. Data = flat list of records.
- EmailMessage: fetch Contact IDs first (already queried in existing 
  flow for contacts object), then query EmailMessage WHERE 
  RelatedToId IN (contact_ids) AND MessageDate = LAST_N_DAYS:60. 
  Paginate via nextRecordsUrl. Cap at 200 records. TextBody only 
  (not HtmlBody — PII surface reduction). Strip attributes.
  On any exception: status = "skipped", error message explains org 
  lacks Enhanced Email, data = null.

### Signal extraction spec
Deterministic only for v1. extract_salesforce_activity_signals(sf_data) 
reads raw_data["salesforce"]["data"]["ActivityHistories"] and produces:
- last_touched signal: most recent ActivityDate as a signal primitive
- activity_velocity: count per type (Call/Email/Meeting) in last 30 days
- open_threads: subjects appearing 2+ times = unresolved item signal
- escalation flag: "critical"/"asap"/"urgent"/"personal intervention" 
  keyword match on Subject or Description
- bot_ratio: count of bot records / total (for quality signal)

Bot detection (deterministic, applied before signal extraction):
- Subject matches: order \d+ confirmation, \[peer1\.com #\d+\], 
  your aptum invoice is ready
- Do not exclude bots from artifact — flag them, filter in extractor

### Error handling
- Activity fetch failure = status "partial" on source_salesforce.json, 
  activity_histories object gets status "fail" with error. Pipeline 
  continues — activities are non-critical.
- EmailMessage unavailable = status "skipped" on email_messages object. 
  Not "fail". Downstream tolerates missing EmailMessages key.
- All writes in finally block per single-write rule.

### Files to touch
- data_sources/internal/salesforceClient.py — fetch_data() only
- core/pipeline/gather.py — _map_to_legacy_envelope() salesforce branch
- core/signal_primitives.py — new extract_salesforce_activity_signals()
- core/pipeline/signals.py — call new extractor in _extract_deterministic_signals()

### Do not touch
- Opportunity LLM extractor
- commercial posture aggregator  
- people.py / contacts flow
- Report rendering (downstream task)

---

# Critique — 2026-03-03 07:32 ET

## Score: 7/10
Ready for implementation with minor clarifications needed on test coverage and documentation updates.

## Section Breakdown

### Done When
**Strong:** 
- Criteria 1-4 are observable and verifiable (JSON keys exist, status values match expectations)
- Criterion 5 provides regression protection via explicit verification step
- "skipped" vs "fail" distinction for Enhanced Email shows thoughtful error handling

**Weak:** 
- No explicit test coverage requirement (e.g., "unit tests pass for bot detection regex" or "integration test confirms activity fetch with mock org")
- No documentation update requirement (README, API docs, or inline docstrings)

**Fix:** 
Add criteria 6-7:
- "6. Unit tests cover bot detection patterns, signal extraction logic, and EmailMessage unavailable scenario"
- "7. Docstrings added to new functions; CHANGELOG.md updated with new data sources"

---

### Notes - Implementation Plan
**Strong:**
- Cursor-ready implementation plan exists with file-by-file breakdown
- Architecture decisions explicitly resolved (Option A, single artifact, legacy envelope mapping)
- Extraction spec is detailed with SOQL fragments, fallback patterns, and field choices
- Signal extraction spec provides concrete primitives (last_touched, activity_velocity, etc.)
- Error handling strategy addresses both failure modes with status differentiation
- "Do not touch" section prevents scope creep

**Weak:**
- Bot detection regex patterns listed but no test cases provided (e.g., "order 12345 confirmation" should match, "Order status update" should not)
- Signal extraction spec lacks example output structure (what does `activity_velocity` signal primitive look like in JSON?)
- No mention of logging strategy for debugging fetch failures

**Fix:**
- Add 2-3 bot detection test cases to Notes
- Include example signal primitive JSON snippet for one signal type
- Specify log level for activity fetch errors (INFO for skipped, WARNING for partial)

---

### Notes - Extraction Spec
**Strong:**
- SOQL details are precise (LAST_N_DAYS:60, ORDER BY, LIMIT 500)
- Fallback pattern for orgs rejecting WHERE in subquery shows real-world awareness
- EmailMessage fetch strategy correctly chains from existing Contact query
- PII reduction choice (TextBody only) is justified
- Pagination and cap (200 records) prevent runaway queries

**Weak:**
- "Strip attributes recursively" mentioned twice but no definition of what attributes to strip (Salesforce metadata fields like `attributes.type`, `attributes.url`?)
- Contact ID fetch assumes contacts object succeeded — no handling if contacts fetch failed but account succeeded

**Fix:**
- Define "attributes" stripping: "Remove `attributes` dict from each record (contains `type` and `url` metadata)"
- Add to error handling: "If contacts object missing/failed, skip EmailMessage fetch entirely (status = skipped, error = 'contacts unavailable')"

---

### Notes - Signal Extraction Spec
**Strong:**
- Five distinct signal types with clear definitions
- Bot detection applied before extraction (correct order)
- Bot records flagged but not excluded from artifact (preserves data lineage)

**Weak:**
- "open_threads" logic ambiguous: subjects appearing 2+ times across all activities or within a time window?
- Escalation keywords listed but no case-sensitivity rule
- No handling for activities with null Subject/Description

**Fix:**
- Clarify: "open_threads: subjects appearing 2+ times in last 30 days (case-insensitive match)"
- Add: "Escalation keywords matched case-insensitively; null Subject/Description treated as empty string"

---

### Notes - Error Handling
**Strong:**
- Distinguishes "partial" (activity fail) from "skipped" (email unavailable)
- Pipeline continues on activity failure (correct priority)
- Single-write rule referenced (prevents partial artifact corruption)

**Weak:**
- "All writes in finally block" conflicts with existing SourceObject pattern where status is set before write
- No retry strategy mentioned (should activity fetch retry on transient Salesforce API errors?)

**Fix:**
- Clarify: "Write source_salesforce.json once after all fetches complete; set activity_histories status to 'fail' in objects dict before write"
- Add: "No retries for activity/email fetches (Salesforce client already retries API calls; fetch failures are terminal for this run)"

---

### Gate Rule Compliance
- ✅ Done When specifies observable outcomes (JSON keys, status values, unchanged behavior)
- ✅ Cursor implementation plan exists (file list, extraction spec, signal spec)
- ⚠️ Tests mentioned in extraction spec (bot detection) but not in Done When
- ⚠️ Documentation not addressed (no docstring/CHANGELOG requirement)

**Deductions:** -1 for missing test requirement in Done When, -1 for missing documentation requirement = **7/10**