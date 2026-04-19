-- v2 draft_log extensions (additive). Apply after 001:
--   docker compose -f ../jsm-sync/docker-compose.yml exec -T postgres \
--     psql -U jsm_sync -d jsm_sync < schema/002_draft_log_v2.sql

ALTER TABLE ops.draft_log
    ADD COLUMN IF NOT EXISTS draft_type TEXT,
    ADD COLUMN IF NOT EXISTS persona_slug TEXT,
    ADD COLUMN IF NOT EXISTS system_prompt_override TEXT;

ALTER TABLE ops.draft_log
    ALTER COLUMN pattern_slug DROP NOT NULL;
