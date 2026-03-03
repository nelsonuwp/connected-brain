---
created: 2026-03-02
source-idea:
- - 2026-03-02-salesforce email ingestion for account intel
status: active
type: code
---

# salesforce email ingestion for account intel

## What
Add activity history and email message fetching to salesforceClient.py 
so source_salesforce.json gains activity_histories and email_messages 
object keys. Map them through the legacy envelope in gather.py. Add a 
dedicated activity signal extractor (including Jira ticket cross-reference) 
that feeds unified_signals.json. Add Account Owner to the report context bar.

## Done When
1. source_salesforce.json contains activity_histories and email_messages 
   keys in objects, each a valid SourceObject (status/record_count/error/data)
2. gather.py _map_to_legacy_envelope maps them to 
   raw_data["salesforce"]["data"]["ActivityHistories"] and ["EmailMessages"]
3. extract_salesforce_activity_signals() produces signal primitives from 
   activity data and merges into unified_signals.json
4. Jira ticket references (APTUM-\d+) extracted from activity text and 
   emitted as signal primitives with ticket ID as evidence — downstream 
   Jira signals with matching ticket IDs are correlated in unified_signals
5. email_messages status is "skipped" (not "fail") when Enhanced Email 
   is not enabled or contacts fetch failed
6. Account Owner (Name from source_salesforce.json objects.account.data.Owner.Name) 
   appears in the report context bar alongside Client ID and ZoomInfo ID
7. Existing Account/Opportunities/Contacts behavior unchanged — verified 
   by running pipeline against a test account
8. Unit tests cover: bot detection patterns, signal extraction, 
   EmailMessage unavailable scenario, Jira ticket regex extraction
9. Docstrings on all new functions; CHANGELOG.md updated

## Notes

### Architecture decisions (resolved)
- Fetch inside salesforceClient.fetch_data() — Account Id already 
  resolved by Client_ID__c query; use that Id for activity queries
- Single artifact — all new keys go into existing source_salesforce.json
- Legacy envelope — add to _map_to_legacy_envelope in gather.py:
    data["ActivityHistories"] = (objects.get("activity_histories") or {}).get("data") or []
    data["EmailMessages"] = (objects.get("email_messages") or {}).get("data") or []
- Signal strategy — new extract_salesforce_activity_signals() called 
  from _extract_deterministic_signals() in signals.py

### Extraction spec
- ActivityHistories: subquery on Account. Window: LAST_N_DAYS:120 with 
  Python fallback filter. ORDER BY ActivityDate DESC. LIMIT: whichever 
  comes first — 120 days or 20 non-bot records (collect up to 500 raw, 
  then trim to first 20 non-bot by date). Fallback required for orgs 
  that reject WHERE in subquery. Strip attributes dict (type + url 
  metadata) recursively. Data = flat list.
- EmailMessage: use Contact IDs from existing contacts fetch. If contacts 
  missing/failed: status = "skipped", error = "contacts unavailable". 
  Otherwise: query WHERE RelatedToId IN (contact_ids) AND 
  MessageDate = LAST_N_DAYS:120. Paginate via nextRecordsUrl. Cap 200 
  records. TextBody only (not HtmlBody). Strip attributes.
  On any exception: status = "skipped".

### Signal extraction spec
extract_salesforce_activity_signals(sf_data) reads ActivityHistories:

- last_touched: most recent ActivityDate as signal primitive
- activity_velocity: count per type (Call/Email/Meeting) in last 30 days
- open_threads: subjects appearing 2+ times in last 30 days 
  (case-insensitive, null = empty string) = unresolved item signal
- escalation: case-insensitive keyword match on Subject + Description 
  for: critical, asap, urgent, personal intervention, priorit
- jira_references: regex APTUM-\d+ extracted from Subject + Description. 
  Each unique ticket ID emitted as a signal primitive with 
  source_type="salesforce_activity" and evidence=ticket ID. 
  Correlation with Jira signals happens in unified_signals merge — 
  if a signal with matching ticket ID exists from Jira source, 
  tag both with a shared jira_ticket_id field for synthesizer context.
- bot_ratio: flagged bot count / total

Example signal primitive:
```json
{
  "claim": "Customer escalated via email referencing open Jira ticket",
  "source_type": "salesforce_activity",
  "evidence": "APTUM-37903: 'This is critical for us, please personal intervention'",
  "confidence": "high",
  "signal_tag": "escalation",
  "jira_ticket_id": "APTUM-37903"
}
```

Bot detection (case-insensitive, before extraction):
- Patterns: "order \d+ confirmation", "\[peer1\.com #\d+\]", 
  "your aptum invoice is ready", "powered by jira service management"
- Test cases: "Order 279799 Confirmation" → bot; 
  "Order status update" → not bot; "[peer1.com #2410043]" → bot
- Bot records stay in artifact (is_bot=true); excluded from signal 
  extraction but counted for bot_ratio

### Report: Account Owner in context bar
- Source: source_salesforce.json → objects.account.data.Owner.Name
- Already in artifact via ACCOUNT_WHITELIST (Owner field)
- Add to report_generator.py context bar template alongside existing 
  Client ID and ZoomInfo ID items
- If Owner absent or null: omit the context-item entirely (no empty label)
- This is the only report_generator.py change in this task

### Error handling
- Activity fetch failure: source_salesforce.json status = "partial", 
  activity_histories object status = "fail". Set before single write.
- EmailMessage unavailable: status = "skipped". Not "fail".
- Logging: INFO for skipped, WARNING for partial/fail
- No retries — Salesforce client already retries; fetch failures terminal

### Files to touch
- data_sources/internal/salesforceClient.py — fetch_data() only
- core/pipeline/gather.py — _map_to_legacy_envelope() salesforce branch
- core/signal_primitives.py — extract_salesforce_activity_signals()
- core/pipeline/signals.py — call new extractor in _extract_deterministic_signals()
- core/report_generator.py — context bar: Account Owner (targeted, single addition)
- CHANGELOG.md

### Do not touch
- Opportunity LLM extractor
- Commercial posture aggregator
- people.py / contacts flow
- Synthesizer / ai_intel_brief schema
- All other report sections

### Cursor Composer prompt
```cursor
I need to integrate Salesforce activity history into the AccountIntel 
pipeline. Read the files listed before writing anything. Then produce 
an implementation plan only — no code yet.

## Files to read first
- data_sources/internal/salesforceClient.py
- core/pipeline/gather.py (focus: _map_to_legacy_envelope, salesforce branch)
- core/signal_primitives.py (focus: extract_salesforce_signals)
- core/pipeline/signals.py (focus: _extract_deterministic_signals)
- core/report_generator.py (focus: context bar / header section)
- salesforceTestAccountActivities.py (reference implementation)
- core/utils/io.py (focus: make_source_object, record_count_from_data, save_source_artifact)

## What to implement

### 1. salesforceClient.py — fetch_data() only
After fetching Account (which gives you the resolved Account Id), add:

ActivityHistories subquery on the Account record:
- LAST_N_DAYS:120, ORDER BY ActivityDate DESC, LIMIT 500
- Fallback pattern required: some orgs reject WHERE in ActivityHistories 
  subquery — omit WHERE and filter by date in Python
- After fetching, trim to first 20 non-bot records by date (bot = 
  subject matches "order \d+ confirmation", "\[peer1\.com #\d+\]", 
  "your aptum invoice is ready", "powered by jira service management")
- Strip attributes dict (type + url metadata) recursively from all records
- Write as activity_histories SourceObject: 
  make_source_object(status, record_count, error, data_list)

EmailMessage fetch:
- Use Contact IDs already fetched for the contacts object
- If contacts object failed/missing: activity_histories status = whatever 
  it is, email_messages = make_source_object("skipped", 0, 
  "contacts unavailable", None)
- Otherwise: query EmailMessage WHERE RelatedToId IN (contact_ids) 
  AND MessageDate = LAST_N_DAYS:120
- Paginate via nextRecordsUrl, cap at 200 records
- TextBody only (not HtmlBody)
- Strip attributes
- On any exception: status = "skipped" (not "fail") — Enhanced Email 
  may not be enabled in all orgs

Partial failure handling: if activity fetch fails, set 
activity_histories status = "fail" in objects dict. Set 
source_salesforce.json top-level status = "partial". 
Still write artifact in finally block (single-write rule).

### 2. gather.py — _map_to_legacy_envelope(), salesforce branch only
Add after existing Account/Opportunities/Contacts mapping:
  data["ActivityHistories"] = (objects.get("activity_histories") or {}).get("data") or []
  data["EmailMessages"] = (objects.get("email_messages") or {}).get("data") or []

Also add Account Owner to legacy data:
  data["AccountOwner"] = ((objects.get("account") or {}).get("data") or {}).get("Owner", {}).get("Name") or None

### 3. core/signal_primitives.py — new function
Add extract_salesforce_activity_signals(sf_data) that reads 
sf_data["data"]["ActivityHistories"] and produces signal primitives 
in the same schema as existing extract_salesforce_signals() output.

Signals to produce:
- last_touched: most recent ActivityDate
- activity_velocity: count per ActivityType in last 30 days
- open_threads: subjects appearing 2+ times in last 30 days 
  (case-insensitive, null treated as empty string)
- escalation: case-insensitive match for critical/asap/urgent/
  personal intervention/priorit in Subject + Description
- jira_references: regex APTUM-\d+ extracted from Subject + 
  Description — emit one signal primitive per unique ticket ID, 
  include ticket ID in evidence and as jira_ticket_id field

Bot records (is_bot=True) excluded from signal extraction but 
counted for a bot_ratio quality signal.

### 4. core/pipeline/signals.py — _extract_deterministic_signals() only
After existing extract_salesforce_signals() call, add:
  if raw_data.get("salesforce", {}).get("status") in ("success", "partial"):
      activity_signals = extract_salesforce_activity_signals(raw_data["salesforce"])
      all_signals.extend(activity_signals)

### 5. core/report_generator.py — context bar only
Add Account Owner as a context-item in the context bar, 
alongside existing Client ID and ZoomInfo ID.
Source: pass account_owner into the template context from 
raw_data["salesforce"]["data"].get("AccountOwner").
If None or empty string: omit the item entirely.

## Constraints
- Do not touch: opportunity extractor, commercial posture, people.py, 
  synthesizer, ai_intel_brief schema, any other report sections
- Match existing error handling pattern exactly (finally block, 
  make_source_object, save_source_artifact)
- No new dependencies

## Deliverable
An implementation plan covering exact function signatures, 
where each change goes in each file, and any edge cases. 
No code yet — plan only.
```