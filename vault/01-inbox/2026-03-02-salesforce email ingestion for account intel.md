---
type: idea
created: 2026-03-02
status: raw
---

# salesforce email ingestion for account intel

## The Idea
Add the ability to pull emails from Salesforce activity history for a given account and include them as a signal source in the AccountIntel pipeline. Emails would surface relationship context, risks, commitments, and sentiment that aren't captured in tickets or firmographics.

## Why Now
The current pipeline pulls structured data (Jira, Ocean, ZoomInfo) but misses unstructured relationship signals that live in email threads. Account managers and sales have context in Salesforce emails that never makes it into the intel brief. Adding this would meaningfully improve signal quality for existing customers where email history exists.




## Absorbed — [[2026-03-02-AI Report Updates]]

### Key Points

- **Update Requirements**: AI report needs three new data points: Account Owners, Last Touched date, and Roll-In Emails & Activities
- **Status**: Marked as "absorbed" (already implemented or integrated into workflow)
- **Context**: Created March 2026 as an idea-type note, suggesting these were feature requests rather than bugs
- **Scope**: Enhancements focused on account management visibility and activity tracking
- **No Constraints Mentioned**: No technical limitations, deadlines, or dependencies documented

### Raw Context

---
created: 2026-03-02
status: absorbed
type: idea
---

# AI Report Updates

## The Idea
Need to make updates to the AI report to show:
* Account Owners
* Last Touched
* Roll-In Emails & Activities

## Why Now


## What I Now Know
- Working extraction code exists (salesforceTestAccountActivities.py) — OAuth2 + httpx, no simple_salesforce dependency, matches existing salesforceClient pattern
- Two data streams: ActivityHistories (Tasks/Events — logged emails, calls, meetings) and EmailMessage (Enhanced Email / Email-to-Case object)
- ActivityHistories come back nested on the Account object; EmailMessage requires separate query via Contact/Case IDs
- Sample data confirmed for account 0018000000ufgnjAAA
- Scope answer: all activity history, not emails only — ActivityType field distinguishes email/call/meeting
- Delivery surface: signals pipeline (feed into unified_signals.json) AND report surface (Roll-In Emails & Activities section)

---

