-- 002_embeddings.sql — pgvector semantic similarity over tickets.
--
-- Depends on: pgvector/pgvector:pg16 Docker image (Task 1).
-- Model: BAAI/bge-base-en-v1.5 → 768 dimensions.
-- If the model ever changes, add a NEW row per issue_key with the new model
-- slug. The (issue_key, model) composite PK supports multi-model coexistence.

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS ticket_embeddings (
    issue_key    text NOT NULL REFERENCES tickets(issue_key) ON DELETE CASCADE,
    model        text NOT NULL,
    text_hash    text NOT NULL,              -- sha256 hex of the embedded text; re-embed only when hash changes
    embedding    vector(768) NOT NULL,
    embedded_at  timestamptz NOT NULL DEFAULT NOW(),
    PRIMARY KEY (issue_key, model)
);

CREATE INDEX IF NOT EXISTS ticket_embeddings_model
    ON ticket_embeddings (model);

-- HNSW index for fast approximate nearest-neighbor on cosine distance.
-- Parameters: m=16, ef_construction=64 are pgvector defaults and fine for
-- ~55k rows. Per-query recall can be tuned via SET hnsw.ef_search (default 40).
CREATE INDEX IF NOT EXISTS ticket_embeddings_vec_hnsw
    ON ticket_embeddings
    USING hnsw (embedding vector_cosine_ops);
