-- ============================================================
-- 003_worklogs.sql — per-entry worklog storage + sync cursor
-- ============================================================

-- Add issue_id to tickets so we can resolve /worklog/list results
-- (which key off numeric issueId, not issueKey) back to issue_key.
ALTER TABLE tickets
    ADD COLUMN IF NOT EXISTS issue_id BIGINT;

CREATE UNIQUE INDEX IF NOT EXISTS tickets_issue_id
    ON tickets (issue_id)
    WHERE issue_id IS NOT NULL;

-- Per-entry worklog rows. Mirrors thread_events structure.
CREATE TABLE IF NOT EXISTS ticket_worklogs (
    worklog_id           BIGINT PRIMARY KEY,
    issue_key            TEXT NOT NULL REFERENCES tickets(issue_key) ON DELETE CASCADE,
    issue_id             BIGINT NOT NULL,
    author_account_id    TEXT REFERENCES jira_users(account_id),
    time_spent_seconds   INTEGER NOT NULL CHECK (time_spent_seconds >= 0),
    started_at           TIMESTAMPTZ NOT NULL,
    comment_adf          JSONB,
    visibility           JSONB,
    jira_created_at      TIMESTAMPTZ NOT NULL,
    jira_updated_at      TIMESTAMPTZ NOT NULL,
    synced_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at           TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ticket_worklogs_issue_key
    ON ticket_worklogs (issue_key) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS ticket_worklogs_issue_id
    ON ticket_worklogs (issue_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS ticket_worklogs_author
    ON ticket_worklogs (author_account_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS ticket_worklogs_started
    ON ticket_worklogs (started_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS ticket_worklogs_updated
    ON ticket_worklogs (jira_updated_at DESC) WHERE deleted_at IS NULL;

-- Seed a second sync_state row for the worklog-updated cursor.
-- Keeps the existing jira_tickets row untouched.
INSERT INTO sync_state (source, status)
VALUES ('jira_worklogs', 'idle')
ON CONFLICT (source) DO NOTHING;
