"""
schemas/inbound_item.py
-----------------------
Canonical intermediate representation for all inbound communication items.

Every source (email, Teams, Slack, Jira, etc.) normalizes into this shape.
Everything downstream of normalization is source-agnostic.

Design decisions:
  - One InboundItem per *thread*, not per message.
    Email threads grouped by conversationId, Teams by chatId, Slack by thread_ts.
  - body_text is the concatenated, de-duped, plain-text content of the thread.
  - source_meta preserves anything source-specific (e.g. email's conversationId,
    Teams chatId) for debugging and deeplinks.
  - Deterministic fields (is_from_me, mentions_me) are set during normalization.
    LLM-dependent fields (category, summary) are added by summarize.py.
"""

from typing import TypedDict, Optional, Literal
from datetime import datetime, timezone
import hashlib
import json


# ── Source types ──────────────────────────────────────────────────────────────

SourceType = Literal["email", "teams", "slack", "jira"]


# ── Participant ───────────────────────────────────────────────────────────────

class Participant(TypedDict):
    name: str
    handle: str                     # email address, Slack handle, Teams UPN
    role: Literal["from", "to", "cc", "mention", "channel_member"]


# ── Attachment stub ───────────────────────────────────────────────────────────

class Attachment(TypedDict):
    name: str
    content_type: Optional[str]
    size_bytes: Optional[int]


# ── InboundItem ───────────────────────────────────────────────────────────────

class InboundItem(TypedDict):
    """
    The canonical unit of work for the daily digest pipeline.

    One item = one conversation thread from one source.
    Cross-source grouping happens in process.py via embedding similarity.
    """

    # ── Identity ──────────────────────────────────────────────────────────
    id: str                         # deterministic hash (source + thread_key)
    source: SourceType              # "email" | "teams" | "slack"

    # ── Content ───────────────────────────────────────────────────────────
    subject: Optional[str]          # email subject, Teams chat topic, Slack channel
    body_text: str                  # plain text, concatenated thread, HTML stripped
    body_snippet: str               # first ~500 chars for embedding / LLM context

    # ── Threading ─────────────────────────────────────────────────────────
    thread_key: str                 # source-native thread ID
    message_count: int              # how many messages in this thread

    # ── Timing ────────────────────────────────────────────────────────────
    first_timestamp: str            # ISO 8601 UTC — earliest message in thread
    last_timestamp: str             # ISO 8601 UTC — most recent message in thread

    # ── People ────────────────────────────────────────────────────────────
    author: Participant             # who sent the last (or only) message
    participants: list[Participant] # everyone in the thread
    participant_count: int

    # ── My relationship to this item ──────────────────────────────────────
    is_from_me: bool                # I sent the most recent message
    mentions_me: bool               # I'm @mentioned (Teams/Slack) or in To: (email)
    am_in_to: bool                  # email: I'm in the To line (not just CC)
    am_in_cc: bool                  # email: I'm in CC only
    is_direct_message: bool         # 1:1 chat (Teams DM, Slack DM, sole recipient email)
    is_forwarded: bool              # email: subject starts with Fw:/Fwd:

    # ── Attachments ───────────────────────────────────────────────────────
    attachments: list[Attachment]
    has_attachments: bool

    # ── Deeplinks ─────────────────────────────────────────────────────────
    url: Optional[str]              # link back to source (Outlook webLink, Teams URL, etc.)

    # ── Source-specific metadata ──────────────────────────────────────────
    source_meta: dict               # anything source-specific, for debugging


# ── Processed item (after process.py adds grouping info) ─────────────────────

class ProcessedItem(TypedDict):
    """InboundItem + processing metadata added by process.py."""
    item: InboundItem
    cluster_id: Optional[str]       # cross-source group ID (None = standalone)
    cluster_items: list[str]        # IDs of other items in this cluster
    is_discarded: bool              # matched a discard rule
    discard_reason: Optional[str]   # which rule matched


# ── Summarized item (after summarize.py adds LLM output) ─────────────────────

class SummarizedItem(TypedDict):
    """ProcessedItem + LLM-generated triage output."""
    item: InboundItem
    cluster_id: Optional[str]
    cluster_items: list[str]
    category: Literal["waiting_on_me", "tracking", "new_information", "discard"]
    summary: str                    # 1-2 sentence summary
    my_actions: list[str]           # things I need to do
    tracked_actions: list[str]      # things others are doing that I should track
    suggested_reply: Optional[str]  # optional draft reply


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_item_id(source: str, thread_key: str) -> str:
    """Deterministic ID from source + thread key."""
    raw = f"{source}::{thread_key}"
    return hashlib.sha256(raw.encode()).hexdigest()[:12]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def snippet(text: str, max_len: int = 500) -> str:
    """First max_len chars of text, stripped."""
    text = (text or "").strip()
    return text[:max_len] if len(text) > max_len else text
