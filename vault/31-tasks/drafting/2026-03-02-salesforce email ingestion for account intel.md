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