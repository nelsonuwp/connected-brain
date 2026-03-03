---
type: idea
created: 2026-03-02
status: raw
---

# salesforce email ingestion for account intel

## The Idea
Pull Salesforce activity history and EmailMessage records for each account and feed them into the 
AccountIntel pipeline as a new signal source. ActivityHistories (logged emails, calls, meetings) 
come back nested on the Account object. EmailMessage records (Enhanced Email / Email-to-Case) 
require a separate query via Contact and Case IDs. Both streams get extracted, filtered by recency, 
and passed to signal extraction — surfacing relationship context, risks, commitments, and sentiment 
that structured sources miss.

## Why Now
Working extraction code already exists and has been tested against a real account. The current 
pipeline pulls structured data (Jira, Ocean, ZoomInfo) but misses unstructured relationship signals 
that live in Salesforce activity. The absorbed note confirms the report already needs an 
"Emails & Activities" surface. The extraction pattern matches the existing salesforceClient 
conventions — this is integration work, not research.

## What I Know
- Working extraction code confirmed (OAuth2 + httpx, no simple_salesforce, matches existing client pattern)
- Two data streams: ActivityHistories (Tasks/Events nested on Account) and EmailMessage (separate query via Contact/Case IDs)
- ActivityType field distinguishes email/call/meeting within ActivityHistories
- Sample data confirmed for a real account
- Scope: all activity types, not emails only — ActivityType used to filter/weight signals
- Delivery surface: signals pipeline (unified_signals.json) AND report (Roll-In Emails & Activities section)
- Recency window already handled in extraction script (LAST_N_DAYS:60, Python-side fallback filter)
- Volume risk: enterprise accounts may have hundreds of activities — extraction already caps at 500