---
type: idea
created: 2026-03-02
status: raw
---

# salesforce email ingestion for account intel

## The Idea
Add activity history and email fetching to salesforceClient.py so that
ActivityHistories and EmailMessage records are included in
source_salesforce.json alongside the existing account, opportunities,
and contacts objects. Activities surface relationship context, risks,
commitments, and sentiment that structured sources miss. The report
gains a "Roll-In Emails & Activities" section consuming this data
directly.

## Why Now
The current pipeline pulls structured Salesforce data (account,
opportunities, contacts) but misses unstructured relationship signals
in activity history. Working extraction code already exists and has
been tested against a real account. The "AI Report Updates" note
(now absorbed) confirmed the report already needs Account Owners,
Last Touched, and Roll-In Emails & Activities — this is the
implementation. No new dependencies required; the pattern matches
existing salesforceClient.py conventions exactly.

## What I Know
- Two data streams to add to source_salesforce.json objects:
  - activity_histories: ActivityHistories subquery on Account
    (Tasks/Events — logged emails, calls, meetings), last 60 days,
    capped at 500, ActivityType distinguishes email/call/meeting
  - email_messages: EmailMessage object queried via Contact and Case
    IDs, last 60 days (Enhanced Email / Email-to-Case; may not be
    enabled in all orgs — handle with try/except, tolerate missing)
- Both go into the existing objects dict in fetch_data() alongside
  account, opportunities, contacts — no new artifact file
- source_salesforce.json schema is unchanged; objects just gains two
  new keys using the existing make_source_object() pattern
- Account Owner (Name + Email) is already in source_salesforce.json
  via the account object — report just needs to surface it
- Last Touched = most recent ActivityDate from activity_histories —
  derived at report time, no new field needed
- Extraction code already written (salesforceTestAccountActivities.py)
  — integration work only, not research
- Recency window: LAST_N_DAYS:60 with Python-side fallback filter
  already implemented in test script
- EmailMessage query requires Contact and Case IDs — fetched first,
  same pattern as existing contacts query

## Risks
- EmailMessage may not be enabled in all orgs — try/except already
  in test script, must tolerate missing email_messages in consumers
- Volume: capped at 500 activities, 60-day window keeps this
  manageable
- Bot/automated activity noise — filter in signal extraction, not
  in gather (preserve raw data)

## Absorbed
- AI Report Updates (2026-03-02): Account Owners, Last Touched,
  Roll-In Emails & Activities — all addressed by this implementation