-- ============================================================
-- jsm-sync initial schema
-- Runs automatically on first Postgres boot via docker-entrypoint-initdb.d
-- ============================================================

-- === Reference tables ===

CREATE TABLE jira_users (
    account_id          TEXT PRIMARY KEY,
    display_name        TEXT NOT NULL,
    email               TEXT,
    role                TEXT NOT NULL CHECK (role IN ('Customer','Aptum','Automation','Unknown')),
    account_type        TEXT,
    first_seen_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX jira_users_role ON jira_users (role);

CREATE TABLE organizations (
    jira_org_id         TEXT PRIMARY KEY,
    name                TEXT NOT NULL,
    ocean_client_id     INTEGER,
    first_seen_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX organizations_ocean_client ON organizations (ocean_client_id);
CREATE INDEX organizations_name ON organizations (name);

-- === Tickets ===

CREATE TABLE tickets (
    issue_key           TEXT PRIMARY KEY,
    summary             TEXT NOT NULL,
    description         TEXT NOT NULL DEFAULT '',
    status              TEXT NOT NULL,
    priority            TEXT,
    issue_type          TEXT,
    request_type        TEXT,
    is_customer_originated BOOLEAN NOT NULL DEFAULT FALSE,

    creator_account_id  TEXT REFERENCES jira_users(account_id),
    reporter_account_id TEXT REFERENCES jira_users(account_id),
    assignee_account_id TEXT REFERENCES jira_users(account_id),
    jira_org_id         TEXT REFERENCES organizations(jira_org_id),
    ocean_client_id     INTEGER,

    labels              TEXT[] NOT NULL DEFAULT '{}',

    sla_first_response_breached   BOOLEAN,
    sla_first_response_elapsed_s  INTEGER,
    sla_first_response_threshold_s INTEGER,
    sla_resolution_breached       BOOLEAN,
    sla_resolution_elapsed_s      INTEGER,
    sla_resolution_threshold_s    INTEGER,

    created_at          TIMESTAMPTZ NOT NULL,
    updated_at          TIMESTAMPTZ NOT NULL,
    resolved_at         TIMESTAMPTZ,

    synced_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at          TIMESTAMPTZ
);

CREATE INDEX tickets_org           ON tickets (jira_org_id);
CREATE INDEX tickets_ocean_client  ON tickets (ocean_client_id);
CREATE INDEX tickets_status        ON tickets (status) WHERE deleted_at IS NULL;
CREATE INDEX tickets_updated       ON tickets (updated_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX tickets_created       ON tickets (created_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX tickets_customer_orig ON tickets (is_customer_originated) WHERE deleted_at IS NULL;
CREATE INDEX tickets_creator       ON tickets (creator_account_id);
CREATE INDEX tickets_assignee      ON tickets (assignee_account_id) WHERE deleted_at IS NULL;

-- === Thread events (comments, later: changelog) ===

CREATE TABLE thread_events (
    id                  TEXT PRIMARY KEY,
    issue_key           TEXT NOT NULL REFERENCES tickets(issue_key) ON DELETE CASCADE,
    kind                TEXT NOT NULL CHECK (kind IN ('comment','changelog')),
    author_account_id   TEXT REFERENCES jira_users(account_id),
    is_public           BOOLEAN,
    body                TEXT NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL,
    synced_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at          TIMESTAMPTZ
);

CREATE INDEX thread_events_issue   ON thread_events (issue_key, created_at);
CREATE INDEX thread_events_author  ON thread_events (author_account_id);
CREATE INDEX thread_events_public  ON thread_events (issue_key, is_public) WHERE kind = 'comment';

-- === Assets ===

CREATE TABLE assets (
    object_id           TEXT PRIMARY KEY,
    workspace_id        TEXT NOT NULL,
    asset_name          TEXT,
    service_id          TEXT,
    last_hydrated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX assets_service_id ON assets (service_id);
CREATE INDEX assets_workspace ON assets (workspace_id);

CREATE TABLE ticket_assets (
    issue_key           TEXT NOT NULL REFERENCES tickets(issue_key) ON DELETE CASCADE,
    object_id           TEXT NOT NULL REFERENCES assets(object_id),
    PRIMARY KEY (issue_key, object_id)
);

CREATE INDEX ticket_assets_object ON ticket_assets (object_id);

-- === Sync state ===

CREATE TABLE sync_state (
    source              TEXT PRIMARY KEY,
    last_sync_at        TIMESTAMPTZ,
    last_cursor         TEXT,
    status              TEXT NOT NULL DEFAULT 'idle'
                            CHECK (status IN ('idle','running','error','completed')),
    last_error          TEXT,
    metadata            JSONB NOT NULL DEFAULT '{}'::jsonb,
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Seed the sync_state row for the Jira ticket sync
INSERT INTO sync_state (source, status) VALUES ('jira_tickets', 'idle')
ON CONFLICT (source) DO NOTHING;
