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

---

# Critique — 2026-03-02 22:12 ET

## Score: 7/10
rework suggested

## Section Breakdown

### The Idea
**Strong:** Scope is clear — two data streams (ActivityHistories, EmailMessage), both feed signals pipeline and report. Extraction pattern matches existing salesforceClient conventions.
**Weak:** "feed them into the AccountIntel pipeline as a new signal source" is vague. Where exactly? What step? What artifact name? What schema?
**Fix:** Specify: (1) extraction writes `source_salesforce_activities.json` in gather step (step 1), (2) signals step (step 2) consumes it via new extractor (e.g. `salesforce_activity_signals.py`), (3) report step (step 8) consumes it directly for "Emails & Activities" section. State the artifact schema: `source`, `company_id`, `collected_at`, `status`, `objects` with keys `activity_histories` and `email_messages`, each with `status`, `record_count`, `data`.

### Why Now
**Strong:** Working extraction code exists and has been tested. Identifies a real gap (unstructured relationship signals). Report already needs the surface.
**Weak:** "The absorbed note confirms the report already needs an 'Emails & Activities' surface" — what note? Where is this requirement documented? Is this a new requirement or an existing placeholder?
**Fix:** State where the requirement lives (e.g. "report_generator.py TODO comment line 342" or "Jira ticket APTUM-1234"). If it's a new requirement, say so and justify why it's worth adding now (e.g. "customer feedback from last 3 reports flagged missing relationship context").

### What I Know
**Strong:** Volume risk acknowledged (500 cap). Recency window handled. Extraction code tested against real account. Delivery surface specified (signals + report).
**Weak:** "Scope: all activity types, not emails only — ActivityType used to filter/weight signals" — how? What's the filtering/weighting logic? What does "weight signals" mean in practice?
**Fix:** Specify: (1) which ActivityTypes are extracted (Email, Call, Meeting — any others?), (2) how they're weighted in signal extraction (e.g. "Email = high confidence for commitments, Call = medium confidence for sentiment, Meeting = high confidence for strategic direction"), (3) whether filtering happens in extraction (already done — only last 60 days) or in signal extraction (e.g. "ignore automated emails from known bots").

### Missing: Blockers / Risks
**Weak:** No blockers or risks identified.
**Fix:** Add:
- **Data quality risk:** ActivityHistories may include automated emails (e.g. system notifications, marketing). How do you filter these? (See `jira_automation_users.json` pattern — need equivalent for Salesforce.)
- **Schema risk:** EmailMessage object may not be enabled in all Salesforce orgs (Enhanced Email feature). Extraction script already handles this (try/except), but signal extraction must tolerate missing `email_messages` key.
- **Cost risk:** LLM signal extraction on 500 activities per account. What's the token cost? (Estimate: 500 activities × 200 tokens each = 100k tokens input per account. At $0.15/1M tokens = $0.015/account. Acceptable if batch size < 100 accounts/run.)
- **Integration risk:** Where does this fit in the gather step? Does it run in parallel with existing Salesforce extraction (account, opportunities) or sequentially? If parallel, does it share the same access token? If sequential, does it add latency?

### Missing: What to Do Next
**Weak:** No next steps.
**Fix:** Add:
1. **Extraction integration:** Add `_fetch_account_activities()` method to `salesforceClient.py`, called from `gather.py` after existing Salesforce extraction. Write `source_salesforce_activities.json` artifact.
2. **Signal extraction:** Create `salesforce_activity_signals.py` in `data_sources/internal/salesforce/`. Implement deterministic extraction (e.g. "commitment" if email contains "will deliver by", "risk" if email contains "delayed", "escalation" if subject contains "urgent"). Add LLM-based extraction for sentiment and strategic themes (use `prompts/salesforce_activity_signals.md`).
3. **Report integration:** Add "Emails & Activities" section to `report_generator.py`. Consume `source_salesforce_activities.json` directly (no signal extraction needed for display). Group by ActivityType, show most recent 10 per type, link to Salesforce record.
4. **Validation:** Add validator to `steps.py` for `source_salesforce_activities.json` (must have `status == "success"` or `status == "partial"` with at least 1 activity). Make it non-critical (pipeline continues if activities fail).
5. **Testing:** Run against 3 test accounts (low/medium/high activity volume). Verify signal extraction quality. Measure token cost. Verify report rendering.