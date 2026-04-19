-- ============================================================
-- ops-agent's own tables, in a separate schema to keep
-- jsm_sync's tables untouched.
--
-- Apply once:
--   docker compose -f ../jsm-sync/docker-compose.yml exec -T postgres \
--     psql -U jsm_sync -d jsm_sync < schema/001_ops_agent_tables.sql
-- ============================================================

CREATE SCHEMA IF NOT EXISTS ops;

-- Log every draft generated, for analysis and iteration
CREATE TABLE IF NOT EXISTS ops.draft_log (
    id                  SERIAL PRIMARY KEY,
    issue_key           TEXT NOT NULL,
    pattern_slug        TEXT NOT NULL,
    engineer_account_id TEXT,
    prompt_tokens       INTEGER,
    completion_tokens   INTEGER,
    model               TEXT,
    system_prompt       TEXT,
    user_prompt         TEXT,
    generated_text      TEXT NOT NULL,
    generated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    was_used            BOOLEAN
);

CREATE INDEX IF NOT EXISTS draft_log_issue        ON ops.draft_log (issue_key);
CREATE INDEX IF NOT EXISTS draft_log_pattern      ON ops.draft_log (pattern_slug);
CREATE INDEX IF NOT EXISTS draft_log_generated_at ON ops.draft_log (generated_at DESC);
