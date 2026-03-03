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