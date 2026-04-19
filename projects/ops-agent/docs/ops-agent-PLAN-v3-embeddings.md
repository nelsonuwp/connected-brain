# ops-agent v3 — Semantic Similarity Implementation Plan

> **For Composer 2 (executing agent):** Work task-by-task, top to bottom. Do **not** skip the commit step at the end of each task. Do **not** batch multiple tasks together. Verify the "Expected" output after every command. If a verification step fails, stop and report — do not "fix forward" past a red signal. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the "all customer tickets" / "all tickets on neighbor hardware" sidebar panels with **semantic-similarity-ranked** lists so that, for a ticket about "firewall firmware upgrade", the related panels show *other firmware upgrade tickets* — not unrelated IP whitelist rules, DNS entries, billing requests, or ping-loss alerts.

**Architecture:** Add **pgvector** to the local `jsm_sync` Postgres. Embed every ticket's `summary + description` locally with **`BAAI/bge-base-en-v1.5`** on Apple Silicon MPS (no API keys, no network at query time). Store 768-dim vectors in a new `ticket_embeddings` table with an HNSW index. Backfill all 55,683 existing tickets in a one-shot script (~15-25 min). Hook new/updated tickets into the existing `jsm_sync.incremental` run so the cron job keeps embeddings fresh. In `ops-agent`, load the same model once at FastAPI startup (lifespan), embed the current ticket on page load, and rank candidate tickets by cosine distance — filtered by `ocean_client_id` (vertical panel) or by neighbor-service membership (horizontal panel). Fall back to recency ordering when an embedding is missing (e.g. a brand-new ticket the cron hasn't embedded yet).

**Tech Stack:**
- Postgres 16 via Docker, image `pgvector/pgvector:pg16` (was `postgres:16`)
- Python 3.14 (`/opt/homebrew/bin/python3`) — no venv, system install (user preference)
- `sentence-transformers==2.7.0` (already installed)
- `torch==2.11.0` with MPS (already installed)
- `pgvector` Python client for asyncpg (to be installed)
- `asyncpg>=0.29` (already installed in both projects)
- Model: `BAAI/bge-base-en-v1.5` (768 dims, ~440MB, MIT license, retrieval-tuned)

**Scope:** This plan touches two projects cooperatively. Both already exist and are running:
- `projects/jsm-sync/` — owns the DB, the schema, the backfill, the cron incremental.
- `projects/ops-agent/` — owns the sidebar UI, the T-context builder, the FastAPI app.

**Out of scope (do NOT do):**
- Do not add a virtualenv. The user explicitly forbids it; use system Python 3.14.
- Do not refactor or "clean up" unrelated code (e.g. the Paramiko TripleDES warning suppression, dash-vs-underscore folder pair `ops-agent/ops_agent/`, OpenRouter wrapper). Leave them alone.
- Do not change the MSSQL or Fusion connection logic. Do not change the persona YAML. Do not change the draft flows.
- Do not delete the existing `list_customer_tickets()` / `list_tickets_for_service_ids()` helpers — keep them as the fallback path.
- Do not commit `projects/jsm-sync/postgres_data/` — these are Docker volume files and must stay ignored (Task 1 makes sure they are).

---

## File map (what gets created / touched)

**jsm-sync (owns embedding generation):**
- Modify: `projects/jsm-sync/docker-compose.yml` — image swap.
- Modify: `projects/jsm-sync/.gitignore` (create if absent) — ignore `postgres_data/`.
- Create: `projects/jsm-sync/schema/002_embeddings.sql` — extension + table + HNSW index.
- Modify: `projects/jsm-sync/requirements.txt` — add `sentence-transformers`, `torch`, `pgvector`, `numpy`.
- Create: `projects/jsm-sync/jsm_sync/embedder.py` — bge-base loader + `embed_texts()`.
- Create: `projects/jsm-sync/jsm_sync/embed_db.py` — asyncpg helpers for `ticket_embeddings`.
- Create: `projects/jsm-sync/jsm_sync/embed_backfill.py` — one-shot script with `python3 -m jsm_sync.embed_backfill`.
- Modify: `projects/jsm-sync/jsm_sync/incremental.py` — embed new/updated tickets at end of run.
- Create: `projects/jsm-sync/scripts/verify_embeddings.py` — smoke test (coverage, basic similarity sanity).

**ops-agent (consumes embeddings):**
- Modify: `projects/ops-agent/requirements.txt` — add `sentence-transformers`, `torch`, `pgvector`, `numpy`.
- Create: `projects/ops-agent/ops_agent/embedder.py` — copy of the embedder (per project-routing rule; no cross-project imports).
- Modify: `projects/ops-agent/ops_agent/main.py` — load embedder in `lifespan`, store on `app.state`.
- Create: `projects/ops-agent/ops_agent/context/semantic.py` — vector-query helpers for the two panels.
- Modify: `projects/ops-agent/ops_agent/context/t_context.py` — use vector queries with recency fallback, add `similarity_score` + `ranked_by` fields to ticket rows.
- Modify: `projects/ops-agent/ops_agent/templates/related_panel.html` — show similarity score + "ranked by" badge.

---

## Pre-flight: environment sanity (Composer 2 — run this before Task 1)

- [ ] Open a terminal and run each of these. If any of them fail, STOP and report to the user before proceeding:

```bash
# Python 3.14 available
/opt/homebrew/bin/python3 --version
# Expected: Python 3.14.x

# Docker + Postgres container up
cd /Users/anelson-macbook-air/connected-brain/projects/jsm-sync
docker compose ps
# Expected: jsm-sync-postgres  ...  Up (healthy)

# Current image (will change in Task 1)
docker compose exec -T postgres psql -U jsm_sync -d jsm_sync -c "SELECT version();"
# Expected: PostgreSQL 16.x ... (Debian ...)

# Sync state — backfill should have finished
docker compose exec -T postgres psql -U jsm_sync -d jsm_sync -c \
  "SELECT source, status FROM sync_state WHERE source='jira_tickets';"
# Expected: status = 'completed'

# Ticket count — sanity, ~55k expected
docker compose exec -T postgres psql -U jsm_sync -d jsm_sync -c "SELECT COUNT(*) FROM tickets;"
# Expected: around 55000-56000

# MPS available
/opt/homebrew/bin/python3 -c "import torch; print('mps:', torch.backends.mps.is_available())"
# Expected: mps: True

# sentence-transformers + torch versions
/opt/homebrew/bin/python3 -c "import sentence_transformers, torch; print(sentence_transformers.__version__, torch.__version__)"
# Expected: 2.7.0 2.11.0 (or newer patch versions — either is fine)

# ops-agent process not holding a DB connection exclusively (so we can restart postgres)
# If ops-agent is running on :8080 you do NOT need to stop it — the image swap will briefly
# drop connections and the pool will reconnect. But save any in-flight UI work first.
lsof -iTCP:8080 -sTCP:LISTEN -nP 2>/dev/null || echo "ops-agent not running on 8080"
```

---

## Task 1: Pin down `.gitignore` and swap Postgres image to pgvector/pgvector:pg16

**Files:**
- Create or modify: `projects/jsm-sync/.gitignore`
- Modify: `projects/jsm-sync/docker-compose.yml`

- [ ] **Step 1.1: Ensure `projects/jsm-sync/.gitignore` ignores the Docker data volume**

Check if the file exists:

```bash
ls projects/jsm-sync/.gitignore 2>/dev/null || echo "missing"
```

If `missing`, create `projects/jsm-sync/.gitignore` with this exact content:

```
# Docker bind-mount volume — never commit
postgres_data/

# Logs
logs/

# Python
__pycache__/
*.pyc

# Local env
.env
```

If the file exists, `cat` it and confirm that `postgres_data/` appears as an ignore rule. If it is not there, append these two lines at the end:

```
# Docker bind-mount volume — never commit
postgres_data/
```

Then run:

```bash
cd /Users/anelson-macbook-air/connected-brain
git rm -rf --cached projects/jsm-sync/postgres_data 2>/dev/null || true
git status --short | head -30
```

Expected: any tracked `postgres_data/*` entries are now removed from the index. The working-tree files remain.

- [ ] **Step 1.2: Update `docker-compose.yml` to use pgvector image**

Current contents of `projects/jsm-sync/docker-compose.yml`:

```yaml
services:
  postgres:
    image: postgres:16
    container_name: jsm-sync-postgres
    ...
```

Change ONLY the `image:` line so it reads:

```yaml
    image: pgvector/pgvector:pg16
```

Leave everything else (container_name, environment, ports, volumes, healthcheck) exactly as it is. The `./postgres_data` bind mount is preserved — this is a binary-only change.

- [ ] **Step 1.3: Pull the new image and restart the container**

```bash
cd /Users/anelson-macbook-air/connected-brain/projects/jsm-sync
docker compose pull postgres
docker compose up -d postgres
```

Expected output (abbreviated):
```
[+] Pulling ...
[+] Running 1/1
 ✔ Container jsm-sync-postgres  Started
```

- [ ] **Step 1.4: Wait for Postgres to become healthy, then verify version string mentions pgvector image**

```bash
cd /Users/anelson-macbook-air/connected-brain/projects/jsm-sync
for i in 1 2 3 4 5 6 7 8 9 10; do
  sleep 1
  docker compose exec -T postgres pg_isready -U jsm_sync -d jsm_sync && break
done

docker compose exec -T postgres psql -U jsm_sync -d jsm_sync -c "SELECT version();"
docker compose exec -T postgres psql -U jsm_sync -d jsm_sync -c "SELECT COUNT(*) FROM tickets;"
```

Expected:
- `pg_isready` prints `accepting connections`.
- `version()` still shows PostgreSQL 16.x (data survived the image swap; the pgvector image is just Postgres 16 + the extension binaries).
- `COUNT(*) FROM tickets` shows the same ~55k count as pre-flight.

If `COUNT(*)` is different from pre-flight, STOP and report — something went wrong with the data volume.

- [ ] **Step 1.5: Commit**

```bash
cd /Users/anelson-macbook-air/connected-brain
git add projects/jsm-sync/.gitignore projects/jsm-sync/docker-compose.yml
git commit -m "chore(jsm-sync): swap postgres:16 → pgvector/pgvector:pg16 and ignore postgres_data/"
```

---

## Task 2: Add the `vector` extension and the `ticket_embeddings` table

**Files:**
- Create: `projects/jsm-sync/schema/002_embeddings.sql`

- [ ] **Step 2.1: Create the schema file**

Create `projects/jsm-sync/schema/002_embeddings.sql` with this exact content:

```sql
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
```

- [ ] **Step 2.2: Apply the schema to the running container**

```bash
cd /Users/anelson-macbook-air/connected-brain/projects/jsm-sync
docker compose exec -T postgres psql -U jsm_sync -d jsm_sync -f /docker-entrypoint-initdb.d/002_embeddings.sql
```

Note: the container bind-mounts `./schema` → `/docker-entrypoint-initdb.d` read-only (see `docker-compose.yml` line 14), so the new file is already visible inside the container at that path.

Expected output:
```
CREATE EXTENSION
CREATE TABLE
CREATE INDEX
CREATE INDEX
```

- [ ] **Step 2.3: Verify extension + table**

```bash
cd /Users/anelson-macbook-air/connected-brain/projects/jsm-sync
docker compose exec -T postgres psql -U jsm_sync -d jsm_sync -c "\dx vector" -c "\d ticket_embeddings"
```

Expected:
- `\dx vector` shows the `vector` extension installed.
- `\d ticket_embeddings` lists the four columns, the PK on `(issue_key, model)`, and the two indexes (one btree on `model`, one HNSW on `embedding`).

- [ ] **Step 2.4: Commit**

```bash
cd /Users/anelson-macbook-air/connected-brain
git add projects/jsm-sync/schema/002_embeddings.sql
git commit -m "feat(jsm-sync): add pgvector extension and ticket_embeddings table (HNSW cosine)"
```

---

## Task 3: Update `requirements.txt` files and install the new packages

**Files:**
- Modify: `projects/jsm-sync/requirements.txt`
- Modify: `projects/ops-agent/requirements.txt`

- [ ] **Step 3.1: Append embedding dependencies to `projects/jsm-sync/requirements.txt`**

Read the current file:

```bash
cat projects/jsm-sync/requirements.txt
```

Append these lines (do not reorder or touch existing entries):

```
# Semantic embeddings (Task: v3 embeddings)
sentence-transformers>=2.7
torch>=2.2
pgvector>=0.3
numpy>=1.26
```

- [ ] **Step 3.2: Append the SAME four lines to `projects/ops-agent/requirements.txt`**

Read the current file, then append the same block as 3.1. Both projects are standalone bubbles per the project-routing rule — duplicating dep declarations is correct.

- [ ] **Step 3.3: Install**

The user's system already has `torch 2.11.0` and `sentence-transformers 2.7.0` — the install should be a no-op for those, and will add `pgvector` + confirm `numpy`:

```bash
/opt/homebrew/bin/python3 -m pip install --break-system-packages \
    "sentence-transformers>=2.7" \
    "torch>=2.2" \
    "pgvector>=0.3" \
    "numpy>=1.26"
```

Expected: `Requirement already satisfied` for torch and sentence-transformers. `pgvector` and `numpy` either install or already satisfied.

- [ ] **Step 3.4: Smoke-test the new `pgvector` asyncpg adapter is importable**

```bash
/opt/homebrew/bin/python3 -c "from pgvector.asyncpg import register_vector; print('pgvector.asyncpg OK')"
```

Expected: `pgvector.asyncpg OK`

- [ ] **Step 3.5: Commit**

```bash
cd /Users/anelson-macbook-air/connected-brain
git add projects/jsm-sync/requirements.txt projects/ops-agent/requirements.txt
git commit -m "chore: add sentence-transformers/torch/pgvector/numpy to both projects"
```

---

## Task 4: Create the embedder module in jsm-sync

**Files:**
- Create: `projects/jsm-sync/jsm_sync/embedder.py`

- [ ] **Step 4.1: Create the embedder**

Create `projects/jsm-sync/jsm_sync/embedder.py` with this exact content:

```python
"""
Local sentence-transformer embedder for ticket text.

Model: BAAI/bge-base-en-v1.5 (768 dims). Runs on Apple Silicon MPS when
available, falls back to CPU otherwise.

BGE-v1.5 is symmetric for short-passage similarity (no query/document
prefix needed) — we feed the same text transformation on both sides.

This module is intentionally dependency-light and process-safe to import
twice (once in jsm-sync's backfill/incremental, once in ops-agent's
FastAPI lifespan). The model is loaded lazily on first call.
"""
from __future__ import annotations

import hashlib
import logging
import os
import threading
from typing import Iterable, Sequence

import numpy as np

logger = logging.getLogger(__name__)

MODEL_NAME = "BAAI/bge-base-en-v1.5"
MODEL_DIM = 768
SUMMARY_MAX = 500
DESCRIPTION_MAX = 2000

_model = None
_model_lock = threading.Lock()


def _resolve_device() -> str:
    """Prefer MPS on Apple Silicon; fall back to CPU."""
    try:
        import torch  # local import so module import is cheap if torch missing at lint time
    except Exception:
        return "cpu"
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def get_model():
    """Lazily construct the SentenceTransformer (thread-safe, idempotent)."""
    global _model
    if _model is not None:
        return _model
    with _model_lock:
        if _model is not None:
            return _model
        from sentence_transformers import SentenceTransformer
        device = _resolve_device()
        logger.info("Loading embedder %s on device=%s", MODEL_NAME, device)
        # trust_remote_code=False (default) is correct for bge-base-en-v1.5.
        _model = SentenceTransformer(MODEL_NAME, device=device)
        return _model


def build_embed_text(summary: str | None, description: str | None) -> str:
    """
    Canonical text-to-embed for a ticket.

    - summary is truncated to SUMMARY_MAX (covers >99% of tickets — max seen is 251).
    - description is truncated to DESCRIPTION_MAX chars (long tail capped for speed).
    - A single blank line separates them so the model sees them as related segments.
    - Whitespace is collapsed / stripped.
    """
    s = (summary or "").strip()[:SUMMARY_MAX]
    d = (description or "").strip()[:DESCRIPTION_MAX]
    if s and d:
        return f"{s}\n\n{d}"
    return s or d


def text_hash(text: str) -> str:
    """SHA-256 hex digest of the exact bytes fed to the encoder."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def embed_texts(texts: Sequence[str], batch_size: int = 64) -> np.ndarray:
    """
    Encode a batch of strings to unit-normalized float32 vectors, shape (N, 768).

    Normalization makes cosine similarity == dot product, which plays nicely
    with pgvector's `vector_cosine_ops` index.
    """
    if not texts:
        return np.zeros((0, MODEL_DIM), dtype=np.float32)
    model = get_model()
    arr = model.encode(
        list(texts),
        batch_size=batch_size,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    # encode() returns float32 already when convert_to_numpy=True, but be defensive.
    if arr.dtype != np.float32:
        arr = arr.astype(np.float32)
    return arr


def embed_one(text: str) -> np.ndarray:
    """Encode a single string. Returns a (768,) float32 array."""
    arr = embed_texts([text])
    return arr[0]
```

- [ ] **Step 4.2: Smoke-test the embedder module**

```bash
cd /Users/anelson-macbook-air/connected-brain/projects/jsm-sync
/opt/homebrew/bin/python3 -c "
from jsm_sync.embedder import embed_texts, build_embed_text, text_hash, MODEL_DIM
import numpy as np

text = build_embed_text('Firewall Firmware Upgrade', 'We need a maintenance window to upgrade the SRX firmware.')
print('text_hash:', text_hash(text)[:16], '...')

vecs = embed_texts([text, 'Customer Credit Request for invoice 42'])
print('shape:', vecs.shape, 'dtype:', vecs.dtype)
print('dim match:', vecs.shape[1] == MODEL_DIM)
print('unit norm:', round(float(np.linalg.norm(vecs[0])), 4))

# Topical similarity sanity
sim_same = float(np.dot(vecs[0], embed_texts(['SRX firmware upgrade maintenance window'])[0]))
sim_diff = float(vecs[0] @ vecs[1])
print(f'sim(firmware, firmware-variant) = {sim_same:.4f}')
print(f'sim(firmware, billing-credit)   = {sim_diff:.4f}')
assert sim_same > sim_diff + 0.05, 'semantic ordering is wrong — did the wrong model load?'
print('SEMANTIC ORDERING OK')
"
```

Expected (first invocation downloads the model — one-time ~440MB; allow up to 2 minutes on first run):
- `shape: (2, 768) dtype: float32`
- `dim match: True`
- `unit norm: 1.0` (or 0.9999…)
- `sim(firmware, firmware-variant)` ~ 0.75–0.95
- `sim(firmware, billing-credit)` ~ 0.10–0.55
- `SEMANTIC ORDERING OK`

If the ordering assertion fails, STOP and report — the model is wrong.

- [ ] **Step 4.3: Commit**

```bash
cd /Users/anelson-macbook-air/connected-brain
git add projects/jsm-sync/jsm_sync/embedder.py
git commit -m "feat(jsm-sync): add local bge-base-en-v1.5 embedder (MPS/CPU)"
```

---

## Task 5: Create asyncpg embedding helpers in jsm-sync

**Files:**
- Create: `projects/jsm-sync/jsm_sync/embed_db.py`

- [ ] **Step 5.1: Create `projects/jsm-sync/jsm_sync/embed_db.py` with this exact content**

```python
"""
asyncpg helpers for the `ticket_embeddings` table.

Every connection that will pass `vector`-typed parameters must first have
`pgvector.asyncpg.register_vector(conn)` called on it. We use asyncpg's
`init` hook on the pool to do this once per acquired connection.
"""
from __future__ import annotations

import logging
from typing import Optional, Sequence

import asyncpg
import numpy as np
from pgvector.asyncpg import register_vector

from .embedder import MODEL_NAME

logger = logging.getLogger(__name__)


async def register_pgvector(conn: asyncpg.Connection) -> None:
    """Register the vector codec on a connection. Call this from pool `init=`."""
    await register_vector(conn)


async def list_issue_keys_needing_embedding(
    conn: asyncpg.Connection,
    model: str = MODEL_NAME,
    limit: Optional[int] = None,
) -> list[str]:
    """
    Return issue_keys whose embedding is missing OR stale.

    "Stale" = the tickets row has been updated more recently than the
    embedding was computed. We use `tickets.updated_at > ticket_embeddings.embedded_at`
    as the freshness predicate; cheap and good enough.
    """
    sql = """
        SELECT t.issue_key
        FROM tickets t
        LEFT JOIN ticket_embeddings e
               ON e.issue_key = t.issue_key AND e.model = $1
        WHERE t.deleted_at IS NULL
          AND (
                e.issue_key IS NULL
             OR t.updated_at > e.embedded_at
          )
        ORDER BY t.updated_at DESC
    """
    if limit is not None:
        sql += f" LIMIT {int(limit)}"
    rows = await conn.fetch(sql, model)
    return [r["issue_key"] for r in rows]


async def fetch_text_for_issue_keys(
    conn: asyncpg.Connection,
    issue_keys: Sequence[str],
) -> list[tuple[str, str, str]]:
    """Return a list of (issue_key, summary, description) for the given keys."""
    if not issue_keys:
        return []
    rows = await conn.fetch(
        """
        SELECT issue_key, summary, COALESCE(description, '') AS description
        FROM tickets
        WHERE issue_key = ANY($1::text[])
        """,
        list(issue_keys),
    )
    return [(r["issue_key"], r["summary"], r["description"]) for r in rows]


async def upsert_embeddings(
    conn: asyncpg.Connection,
    rows: Sequence[tuple[str, str, np.ndarray]],
    model: str = MODEL_NAME,
) -> int:
    """
    Upsert (issue_key, text_hash, vector) triples.

    Returns the number of rows written. Uses executemany for batch throughput.
    """
    if not rows:
        return 0
    await conn.executemany(
        """
        INSERT INTO ticket_embeddings (issue_key, model, text_hash, embedding, embedded_at)
        VALUES ($1, $2, $3, $4, NOW())
        ON CONFLICT (issue_key, model) DO UPDATE SET
            text_hash   = EXCLUDED.text_hash,
            embedding   = EXCLUDED.embedding,
            embedded_at = NOW()
        """,
        [(ik, model, h, vec) for (ik, h, vec) in rows],
    )
    return len(rows)


async def count_embeddings(conn: asyncpg.Connection, model: str = MODEL_NAME) -> int:
    row = await conn.fetchrow(
        "SELECT COUNT(*) AS c FROM ticket_embeddings WHERE model = $1",
        model,
    )
    return int(row["c"])
```

- [ ] **Step 5.2: Commit**

```bash
cd /Users/anelson-macbook-air/connected-brain
git add projects/jsm-sync/jsm_sync/embed_db.py
git commit -m "feat(jsm-sync): add asyncpg helpers for ticket_embeddings (pgvector codec)"
```

---

## Task 6: Write the one-shot backfill script

**Files:**
- Create: `projects/jsm-sync/jsm_sync/embed_backfill.py`

- [ ] **Step 6.1: Create the backfill script**

Create `projects/jsm-sync/jsm_sync/embed_backfill.py` with this exact content:

```python
"""
One-shot backfill of ticket_embeddings for every ticket that is missing
or stale. Idempotent — safe to re-run. Progress is logged every batch.

Run (takes ~15-25 min on M-series MPS for 55k tickets):
    /opt/homebrew/bin/python3 -m jsm_sync.embed_backfill

Optional flags:
    --batch-size N   (default 64)
    --limit N        (cap rows embedded this run; useful for testing)
    --dry-run        (log what would be embedded, write nothing)
"""
from __future__ import annotations

import argparse
import asyncio
import logging
import time
from typing import Optional

import asyncpg

from .config import settings
from .embedder import MODEL_NAME, build_embed_text, embed_texts, text_hash
from .embed_db import (
    count_embeddings,
    fetch_text_for_issue_keys,
    list_issue_keys_needing_embedding,
    register_pgvector,
    upsert_embeddings,
)

logger = logging.getLogger(__name__)


async def _make_pool() -> asyncpg.Pool:
    return await asyncpg.create_pool(
        dsn=settings.database_url,
        min_size=1,
        max_size=4,
        command_timeout=120,
        init=register_pgvector,  # register the vector codec on every connection
    )


async def run_backfill(batch_size: int, limit: Optional[int], dry_run: bool) -> None:
    pool = await _make_pool()
    try:
        async with pool.acquire() as conn:
            before = await count_embeddings(conn)
            keys = await list_issue_keys_needing_embedding(conn, MODEL_NAME, limit=limit)

        total_needed = len(keys)
        logger.info(
            "Embedding backfill: %d tickets need embedding (existing rows: %d, model=%s)",
            total_needed, before, MODEL_NAME,
        )
        if dry_run:
            logger.info("--dry-run set, exiting without writing.")
            return
        if total_needed == 0:
            logger.info("Nothing to do — every ticket already has a fresh embedding.")
            return

        t0 = time.perf_counter()
        done = 0
        written = 0
        for start in range(0, total_needed, batch_size):
            batch_keys = keys[start : start + batch_size]
            async with pool.acquire() as conn:
                rows = await fetch_text_for_issue_keys(conn, batch_keys)

            texts: list[str] = []
            prepared: list[tuple[str, str]] = []
            for ik, summary, description in rows:
                t = build_embed_text(summary, description)
                texts.append(t)
                prepared.append((ik, text_hash(t)))

            vectors = embed_texts(texts, batch_size=batch_size)

            write_rows = [
                (prepared[i][0], prepared[i][1], vectors[i]) for i in range(len(prepared))
            ]
            async with pool.acquire() as conn:
                wrote = await upsert_embeddings(conn, write_rows)
            written += wrote
            done += len(batch_keys)

            elapsed = time.perf_counter() - t0
            rate = done / elapsed if elapsed > 0 else 0.0
            eta_s = (total_needed - done) / rate if rate > 0 else 0.0
            logger.info(
                "batch %d: %d/%d (%.1f%%) written=%d rate=%.1f t/s eta=%.1fs",
                start // batch_size + 1,
                done,
                total_needed,
                100.0 * done / total_needed,
                written,
                rate,
                eta_s,
            )

        logger.info("Backfill complete: wrote %d rows in %.1fs", written, time.perf_counter() - t0)
    finally:
        await pool.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    )
    asyncio.run(run_backfill(args.batch_size, args.limit, args.dry_run))


if __name__ == "__main__":
    main()
```

- [ ] **Step 6.2: Dry-run — confirm the script sees the expected number of tickets**

```bash
cd /Users/anelson-macbook-air/connected-brain/projects/jsm-sync
/opt/homebrew/bin/python3 -m jsm_sync.embed_backfill --dry-run
```

Expected log line (numbers approximate):
```
Embedding backfill: 55683 tickets need embedding (existing rows: 0, model=BAAI/bge-base-en-v1.5)
--dry-run set, exiting without writing.
```

If the "tickets need embedding" count is zero, something is off — STOP and report.

- [ ] **Step 6.3: Smoke-embed a tiny slice (10 rows) to validate the write path**

```bash
cd /Users/anelson-macbook-air/connected-brain/projects/jsm-sync
/opt/homebrew/bin/python3 -m jsm_sync.embed_backfill --limit 10 --batch-size 10
```

Expected:
```
Embedding backfill: 10 tickets need embedding ...
batch 1: 10/10 (100.0%) written=10 rate=... eta=0.0s
Backfill complete: wrote 10 rows in ...s
```

Verify the table now has ten rows:

```bash
docker compose exec -T postgres psql -U jsm_sync -d jsm_sync -c \
  "SELECT COUNT(*) FROM ticket_embeddings;"
```

Expected: `10`.

- [ ] **Step 6.4: Run the real backfill (~15-25 min)**

```bash
cd /Users/anelson-macbook-air/connected-brain/projects/jsm-sync
mkdir -p logs
nohup /opt/homebrew/bin/python3 -m jsm_sync.embed_backfill --batch-size 64 \
  > logs/embed-backfill.log 2>&1 &

# Watch:
tail -f logs/embed-backfill.log
```

You'll see progress lines every batch. When you see `Backfill complete: wrote N rows` stop the `tail -f` (Ctrl-C) and proceed.

- [ ] **Step 6.5: Verify coverage**

```bash
docker compose exec -T postgres psql -U jsm_sync -d jsm_sync -c "
SELECT
  (SELECT COUNT(*) FROM tickets WHERE deleted_at IS NULL)              AS live_tickets,
  (SELECT COUNT(*) FROM ticket_embeddings WHERE model='BAAI/bge-base-en-v1.5') AS embedded,
  (SELECT COUNT(*) FROM tickets WHERE deleted_at IS NULL)
    - (SELECT COUNT(*) FROM ticket_embeddings WHERE model='BAAI/bge-base-en-v1.5') AS missing;
"
```

Expected: `missing = 0` (or within 1-2 tickets that were inserted mid-backfill by the cron; running the backfill again will clear it).

- [ ] **Step 6.6: Commit (the script, not the log)**

```bash
cd /Users/anelson-macbook-air/connected-brain
git add projects/jsm-sync/jsm_sync/embed_backfill.py
git commit -m "feat(jsm-sync): add embed_backfill.py (idempotent, MPS-accelerated, resumable)"
```

---

## Task 7: Wire embeddings into the incremental sync

**Files:**
- Modify: `projects/jsm-sync/jsm_sync/incremental.py`

The current incremental script (in `projects/jsm-sync/jsm_sync/incremental.py`) persists tickets and advances the cursor. After the last ticket is persisted, we want it to embed any rows that are missing/stale. If nothing changed, this is a cheap no-op.

- [ ] **Step 7.1: Add a helper function at the bottom of `incremental.py`**

Insert this function after the existing `run_incremental()` coroutine and before `def main()`. The file currently ends with:

```python
def main() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    )
    asyncio.run(run_incremental())


if __name__ == "__main__":
    main()
```

Change it so the file ends like this (new function + call from `main()`):

```python
async def _embed_pending(pool_init_required: bool = True) -> None:
    """
    Embed any tickets that are missing/stale for our current model.
    Opens its own short-lived pool (with pgvector codec registered) to keep
    the main sync pool free of vector-typed concerns.
    """
    import asyncpg

    from .embed_db import (
        fetch_text_for_issue_keys,
        list_issue_keys_needing_embedding,
        register_pgvector,
        upsert_embeddings,
    )
    from .embedder import MODEL_NAME, build_embed_text, embed_texts, text_hash

    pool = await asyncpg.create_pool(
        dsn=settings.database_url,
        min_size=1,
        max_size=2,
        command_timeout=120,
        init=register_pgvector,
    )
    try:
        async with pool.acquire() as conn:
            keys = await list_issue_keys_needing_embedding(conn, MODEL_NAME)
        if not keys:
            logger.info("Embedding catch-up: nothing to do")
            return
        logger.info("Embedding catch-up: %d ticket(s) need embedding", len(keys))

        BATCH = 64
        for start in range(0, len(keys), BATCH):
            batch_keys = keys[start : start + BATCH]
            async with pool.acquire() as conn:
                rows = await fetch_text_for_issue_keys(conn, batch_keys)
            texts = [build_embed_text(s, d) for (_, s, d) in rows]
            vectors = embed_texts(texts, batch_size=BATCH)
            write_rows = [
                (rows[i][0], text_hash(texts[i]), vectors[i])
                for i in range(len(rows))
            ]
            async with pool.acquire() as conn:
                await upsert_embeddings(conn, write_rows)
        logger.info("Embedding catch-up complete (%d tickets)", len(keys))
    finally:
        await pool.close()


def main() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    )

    async def _runner() -> None:
        await run_incremental()
        # Embedding is a best-effort side step; an exception here should
        # not mark the sync as failed.
        try:
            await _embed_pending()
        except Exception:
            logger.exception("Embedding catch-up failed (non-fatal)")

    asyncio.run(_runner())


if __name__ == "__main__":
    main()
```

- [ ] **Step 7.2: Run it end-to-end and verify**

```bash
cd /Users/anelson-macbook-air/connected-brain/projects/jsm-sync
/opt/homebrew/bin/python3 -m jsm_sync.incremental
```

Expected log lines (order, abbreviated):
```
... Incremental sync from cursor ...
... Scout found 0 tickets since last cursor   (OR: N tickets)
... No new tickets — incremental sync complete   (OR: persist logs)
... Embedding catch-up: nothing to do           (OR: N ticket(s) need embedding → Embedding catch-up complete)
```

- [ ] **Step 7.3: Commit**

```bash
cd /Users/anelson-macbook-air/connected-brain
git add projects/jsm-sync/jsm_sync/incremental.py
git commit -m "feat(jsm-sync): embed new/stale tickets at end of incremental run (non-fatal)"
```

---

## Task 8: Smoke-test script — verify query-time semantic retrieval

**Files:**
- Create: `projects/jsm-sync/scripts/verify_embeddings.py`

This is a runnable sanity check. It picks two known tickets (one firmware/maintenance, one monitoring), runs a vector-kNN against the whole corpus, and prints the top 10 results so a human can eyeball whether the ranking looks sane.

- [ ] **Step 8.1: Create the script directory if absent**

```bash
mkdir -p projects/jsm-sync/scripts
```

- [ ] **Step 8.2: Create `projects/jsm-sync/scripts/verify_embeddings.py`**

```python
"""
Manual verification: for a given ticket, print the top-K most semantically
similar tickets (any customer, any hardware).

Usage:
    /opt/homebrew/bin/python3 -m scripts.verify_embeddings APTUM-38273
    /opt/homebrew/bin/python3 -m scripts.verify_embeddings APTUM-57415 --k 20
"""
from __future__ import annotations

import argparse
import asyncio
import sys

import asyncpg

# Support both `python3 -m scripts.verify_embeddings` and plain `python3 scripts/verify_embeddings.py`.
# When run as a script, the package parent isn't on sys.path — fix that.
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
if _PROJ not in sys.path:
    sys.path.insert(0, _PROJ)

from jsm_sync.config import settings  # noqa: E402
from jsm_sync.embed_db import register_pgvector  # noqa: E402
from jsm_sync.embedder import MODEL_NAME  # noqa: E402


async def topk(issue_key: str, k: int) -> None:
    pool = await asyncpg.create_pool(
        dsn=settings.database_url,
        min_size=1, max_size=2,
        init=register_pgvector,
    )
    try:
        async with pool.acquire() as conn:
            src = await conn.fetchrow(
                """
                SELECT t.issue_key, t.summary, e.embedding
                FROM tickets t
                JOIN ticket_embeddings e
                     ON e.issue_key = t.issue_key AND e.model = $2
                WHERE t.issue_key = $1
                """,
                issue_key, MODEL_NAME,
            )
            if src is None:
                print(f"no embedding for {issue_key} (yet)")
                return

            rows = await conn.fetch(
                """
                SELECT t.issue_key, t.summary, t.status,
                       1 - (e.embedding <=> $1) AS cosine_sim
                FROM ticket_embeddings e
                JOIN tickets t ON t.issue_key = e.issue_key
                WHERE e.model = $3 AND t.issue_key <> $2 AND t.deleted_at IS NULL
                ORDER BY e.embedding <=> $1
                LIMIT $4
                """,
                src["embedding"], issue_key, MODEL_NAME, k,
            )

        print(f"Source: {src['issue_key']}  {src['summary']}\n")
        for i, r in enumerate(rows, 1):
            sim = float(r["cosine_sim"])
            s = (r["summary"] or "")[:90]
            print(f"{i:2d}. {r['issue_key']}  sim={sim:.4f}  {r['status']:<18}  {s}")
    finally:
        await pool.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("issue_key")
    ap.add_argument("--k", type=int, default=10)
    args = ap.parse_args()
    asyncio.run(topk(args.issue_key, args.k))


if __name__ == "__main__":
    main()
```

- [ ] **Step 8.3: Run it against two known-different tickets**

```bash
cd /Users/anelson-macbook-air/connected-brain/projects/jsm-sync
/opt/homebrew/bin/python3 -m scripts.verify_embeddings APTUM-38273 --k 10
echo "---"
/opt/homebrew/bin/python3 -m scripts.verify_embeddings APTUM-57415 --k 10
```

Expected:
- For `APTUM-38273` ("Firewall Firmware Upgrade – Maintenance Window Request"):
  - Top hits should include tickets whose summaries mention "firmware upgrade", "SRX upgrade", "maintenance window", "firewall upgrade" — not random DNS/SPF/billing tickets.
  - `APTUM-51673` (the known-good peer "Firewall Firmware Upgrade – Maintenance Window Request") should appear high.
- For `APTUM-57415` ("IP Aliases monitoring alerts possibly causing downtime"):
  - Top hits should include monitoring-alert or downtime tickets — not Customer Credit Requests or Veeam billing tickets.

If the top results look *nothing* like the source ticket topic, STOP and report — the backfill may have embedded the wrong text, or the model failed to load the right weights.

- [ ] **Step 8.4: Commit**

```bash
cd /Users/anelson-macbook-air/connected-brain
git add projects/jsm-sync/scripts/verify_embeddings.py
git commit -m "feat(jsm-sync): add scripts/verify_embeddings.py for manual semantic-retrieval sanity"
```

---

## Task 9: Copy the embedder module into ops-agent

**Files:**
- Create: `projects/ops-agent/ops_agent/embedder.py`

Per the project-routing rule, ops-agent must own its own copy — no cross-project imports.

- [ ] **Step 9.1: Copy the file**

Create `projects/ops-agent/ops_agent/embedder.py` with **exactly the same content** as `projects/jsm-sync/jsm_sync/embedder.py`. Do not modify, do not refactor. The file is small and duplicating it is the architectural choice.

(If you prefer to do it with a shell command: `cp projects/jsm-sync/jsm_sync/embedder.py projects/ops-agent/ops_agent/embedder.py` — then verify the file compare matches.)

- [ ] **Step 9.2: Verify equality**

```bash
cd /Users/anelson-macbook-air/connected-brain
diff -u projects/jsm-sync/jsm_sync/embedder.py projects/ops-agent/ops_agent/embedder.py
```

Expected: no output (files are identical).

- [ ] **Step 9.3: Commit**

```bash
git add projects/ops-agent/ops_agent/embedder.py
git commit -m "feat(ops-agent): copy bge-base embedder module from jsm-sync (per project-routing rule)"
```

---

## Task 10: Load the embedder once in ops-agent's FastAPI lifespan

**Files:**
- Modify: `projects/ops-agent/ops_agent/main.py`

The current `main.py` has a `lifespan` context that starts the DB pool and the Fusion SSH tunnel. We add one line to warm the embedder at startup so the first user request doesn't pay the model-load cost.

- [ ] **Step 10.1: Edit `projects/ops-agent/ops_agent/main.py`**

Current `lifespan` (lines 22-30):

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool()
    start_fusion()
    logger.info("ops-agent started at http://%s:%d", settings.ops_agent_host, settings.ops_agent_port)
    yield
    stop_fusion()
    await close_pool()
    logger.info("ops-agent shut down")
```

Replace it with:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool()
    start_fusion()
    # Warm the sentence-transformer so first user request isn't slow.
    # This downloads ~440MB on the very first run of this process; from then on
    # it's a local disk cache (~/.cache/huggingface/…).
    from .embedder import get_model, MODEL_NAME
    try:
        get_model()
        logger.info("Embedder warm (%s)", MODEL_NAME)
    except Exception:
        logger.exception("Embedder failed to warm — sidebar will fall back to recency ordering")
    logger.info("ops-agent started at http://%s:%d", settings.ops_agent_host, settings.ops_agent_port)
    yield
    stop_fusion()
    await close_pool()
    logger.info("ops-agent shut down")
```

- [ ] **Step 10.2: Restart ops-agent and verify the warm log line appears**

If ops-agent is running via `./run.sh` with uvicorn `--reload`, the file change will auto-restart the process. Otherwise:

```bash
cd /Users/anelson-macbook-air/connected-brain/projects/ops-agent
./run.sh
```

In the startup log you should see:
```
... DB pool ready → postgresql://jsm_sync:localdev@localhost:5433/jsm_sync
... Fusion connection pool ready
... Loading embedder BAAI/bge-base-en-v1.5 on device=mps
... Embedder warm (BAAI/bge-base-en-v1.5)
... ops-agent started at http://127.0.0.1:8080
```

If you see "Embedder failed to warm" — STOP and report; the whole feature depends on this.

- [ ] **Step 10.3: Commit**

```bash
cd /Users/anelson-macbook-air/connected-brain
git add projects/ops-agent/ops_agent/main.py
git commit -m "feat(ops-agent): warm bge-base embedder at lifespan startup"
```

---

## Task 11: Create the semantic-query module in ops-agent

**Files:**
- Create: `projects/ops-agent/ops_agent/context/semantic.py`

This module has two public functions — one per sidebar panel — each returning ticket rows with a `similarity_score` column (float, cosine similarity) and a `ranked_by` column (`"semantic"` or `"recency"`).

- [ ] **Step 11.1: Create `projects/ops-agent/ops_agent/context/semantic.py` with this exact content**

```python
"""
Semantic-similarity queries for the related-panel sidebar.

Strategy:
  1. Embed the current ticket's (summary, description) once.
  2. For each panel, run a filtered KNN against ticket_embeddings with
     ORDER BY embedding <=> $query_vec.
  3. If the result set is smaller than the desired limit (few or no
     embeddings exist for the filter group — e.g. a brand-new ticket),
     top up with recency-ordered tickets that don't yet have an embedding.

Rows returned always carry:
  - similarity_score: float in [-1, 1] (cosine sim; ~1 = very similar), or None for recency-padded rows
  - ranked_by:        "semantic" | "recency"
"""
from __future__ import annotations

import logging
from typing import Any, Optional

import asyncpg
import numpy as np

from ..embedder import MODEL_NAME, build_embed_text, embed_one

logger = logging.getLogger(__name__)


SEMANTIC_LIMIT_CUSTOMER = 15
SEMANTIC_LIMIT_NEIGHBOR = 15


def embed_current_ticket(summary: str, description: str) -> np.ndarray:
    return embed_one(build_embed_text(summary, description))


async def similar_customer_tickets(
    conn: asyncpg.Connection,
    query_vec: np.ndarray,
    ocean_client_id: int,
    *,
    exclude_issue_key: str,
    limit: int = SEMANTIC_LIMIT_CUSTOMER,
) -> list[dict[str, Any]]:
    """
    Vertical panel: tickets from the SAME customer, ranked by semantic
    similarity to the current ticket.
    """
    rows = await conn.fetch(
        """
        SELECT
            t.issue_key, t.summary, t.status, t.ocean_client_id,
            t.updated_at, t.resolved_at,
            org.name AS jira_org_name,
            1 - (e.embedding <=> $1) AS similarity_score
        FROM tickets t
        JOIN ticket_embeddings e
             ON e.issue_key = t.issue_key AND e.model = $4
        LEFT JOIN organizations org ON org.jira_org_id = t.jira_org_id
        WHERE t.ocean_client_id = $2
          AND t.deleted_at IS NULL
          AND t.issue_key <> $3
        ORDER BY e.embedding <=> $1
        LIMIT $5
        """,
        query_vec, ocean_client_id, exclude_issue_key, MODEL_NAME, limit,
    )
    out = []
    for r in rows:
        d = dict(r)
        d["ranked_by"] = "semantic"
        out.append(d)
    return out


async def similar_neighbor_tickets(
    conn: asyncpg.Connection,
    query_vec: np.ndarray,
    service_ids: list[str],
    *,
    exclude_issue_key: str,
    limit: int = SEMANTIC_LIMIT_NEIGHBOR,
) -> list[dict[str, Any]]:
    """
    Horizontal panel: tickets on neighbor services (similar hardware),
    ranked by semantic similarity to the current ticket.
    """
    if not service_ids:
        return []
    rows = await conn.fetch(
        """
        SELECT
            t.issue_key, t.summary, t.status, t.ocean_client_id,
            t.updated_at, t.resolved_at,
            org.name AS jira_org_name,
            1 - (e.embedding <=> $1) AS similarity_score
        FROM tickets t
        JOIN ticket_embeddings e
             ON e.issue_key = t.issue_key AND e.model = $4
        LEFT JOIN organizations org ON org.jira_org_id = t.jira_org_id
        WHERE t.deleted_at IS NULL
          AND t.issue_key <> $3
          AND EXISTS (
                SELECT 1
                FROM ticket_assets ta
                JOIN assets a ON a.object_id = ta.object_id
                WHERE ta.issue_key = t.issue_key
                  AND a.service_id = ANY($2::text[])
          )
        ORDER BY e.embedding <=> $1
        LIMIT $5
        """,
        query_vec, service_ids, exclude_issue_key, MODEL_NAME, limit,
    )
    out = []
    for r in rows:
        d = dict(r)
        d["ranked_by"] = "semantic"
        out.append(d)
    return out


def merge_with_recency_fallback(
    semantic_rows: list[dict[str, Any]],
    recency_rows: list[dict[str, Any]],
    *,
    target: int,
) -> list[dict[str, Any]]:
    """
    Pad `semantic_rows` up to `target` using `recency_rows`, skipping any
    issue_keys already present. Preserves order: semantic first, then recency.

    Recency-padded rows are tagged ranked_by="recency", similarity_score=None.
    """
    seen = {r["issue_key"] for r in semantic_rows}
    out = list(semantic_rows)
    for r in recency_rows:
        if len(out) >= target:
            break
        if r["issue_key"] in seen:
            continue
        rr = dict(r)
        rr.setdefault("similarity_score", None)
        rr.setdefault("ranked_by", "recency")
        out.append(rr)
        seen.add(r["issue_key"])
    return out
```

- [ ] **Step 11.2: Commit**

```bash
cd /Users/anelson-macbook-air/connected-brain
git add projects/ops-agent/ops_agent/context/semantic.py
git commit -m "feat(ops-agent): add semantic.py with vector-KNN for customer + neighbor panels"
```

---

## Task 12: Switch `t_context.py` to semantic queries with recency fallback

**Files:**
- Modify: `projects/ops-agent/ops_agent/context/t_context.py`

This task changes the two lines that populate `customer_tickets` and `neighbor_tickets`. Everything else in `t_context.py` stays. Also: we need to make sure the asyncpg connection we use for vector queries has the pgvector codec registered.

The cleanest way is to register pgvector on every connection acquired from the ops-agent pool. We do that by modifying `projects/ops-agent/ops_agent/db.py`'s `init_pool()` to pass `init=register_vector` — but we'll do that via a small wrapper so we don't hard-import pgvector if torch/pgvector are ever missing.

- [ ] **Step 12.1: Modify `projects/ops-agent/ops_agent/db.py` — register pgvector on every connection**

Find this block (currently lines 24-34):

```python
async def init_pool() -> None:
    global _pool
    if _pool is not None:
        return
    _pool = await asyncpg.create_pool(
        dsn=settings.database_url,
        min_size=1,
        max_size=10,
        command_timeout=30,
    )
    logger.info("DB pool ready → %s", settings.database_url)
```

Replace it with:

```python
async def _register_pgvector_on_conn(conn: asyncpg.Connection) -> None:
    """Register pgvector codec on each acquired connection. Best-effort —
    if pgvector isn't installed yet (e.g. during initial migration) we
    log and continue."""
    try:
        from pgvector.asyncpg import register_vector
        await register_vector(conn)
    except Exception as e:
        logger.warning("pgvector.asyncpg.register_vector failed: %s", e)


async def init_pool() -> None:
    global _pool
    if _pool is not None:
        return
    _pool = await asyncpg.create_pool(
        dsn=settings.database_url,
        min_size=1,
        max_size=10,
        command_timeout=30,
        init=_register_pgvector_on_conn,
    )
    logger.info("DB pool ready → %s", settings.database_url)
```

- [ ] **Step 12.2: Modify the imports at the top of `projects/ops-agent/ops_agent/context/t_context.py`**

Current (lines 18-25):

```python
from ..config import settings
from ..fusion_conn import fusion_pool
from ..db import (
    get_ticket,
    get_ticket_assets,
    list_customer_tickets,
    list_tickets_for_service_ids,
)
```

Change to (add three new imports):

```python
from ..config import settings
from ..fusion_conn import fusion_pool
from ..db import (
    get_ticket,
    get_ticket_assets,
    list_customer_tickets,
    list_tickets_for_service_ids,
)
from .semantic import (
    SEMANTIC_LIMIT_CUSTOMER,
    SEMANTIC_LIMIT_NEIGHBOR,
    embed_current_ticket,
    merge_with_recency_fallback,
    similar_customer_tickets,
    similar_neighbor_tickets,
)
```

- [ ] **Step 12.3: Replace the two population blocks inside `build_t_context()`**

Find this block inside `async def build_t_context(...)` (currently lines 467-480 approximately):

```python
        customer_tickets: list[dict] = []
        if resolved_client is not None:
            customer_tickets = await list_customer_tickets(
                conn, resolved_client, exclude_issue_key=issue_key, limit=CUSTOMER_TICKET_LIMIT
            )

        neighbor_sids = [n["service_id"] for n in mssql_data.get("neighbor_services") or []]
        neighbor_sid_strs = [str(x) for x in neighbor_sids]
        neighbor_tickets: list[dict] = []
        if neighbor_sid_strs:
            neighbor_tickets = await list_tickets_for_service_ids(
                conn, neighbor_sid_strs, exclude_issue_key=issue_key, limit=NEIGHBOR_TICKET_LIMIT
            )
```

Replace it with:

```python
        # Build query vector from the current ticket.
        query_vec = await asyncio.to_thread(
            embed_current_ticket,
            ticket.get("summary") or "",
            ticket.get("description") or "",
        )

        # Vertical panel — semantic first, recency fallback to pad.
        customer_tickets: list[dict] = []
        if resolved_client is not None:
            sem_rows = await similar_customer_tickets(
                conn,
                query_vec,
                resolved_client,
                exclude_issue_key=issue_key,
                limit=SEMANTIC_LIMIT_CUSTOMER,
            )
            if len(sem_rows) < SEMANTIC_LIMIT_CUSTOMER:
                rec_rows = await list_customer_tickets(
                    conn,
                    resolved_client,
                    exclude_issue_key=issue_key,
                    limit=CUSTOMER_TICKET_LIMIT,
                )
                customer_tickets = merge_with_recency_fallback(
                    sem_rows, rec_rows, target=SEMANTIC_LIMIT_CUSTOMER
                )
            else:
                customer_tickets = sem_rows

        # Horizontal panel — semantic first, recency fallback to pad.
        neighbor_sids = [n["service_id"] for n in mssql_data.get("neighbor_services") or []]
        neighbor_sid_strs = [str(x) for x in neighbor_sids]
        neighbor_tickets: list[dict] = []
        if neighbor_sid_strs:
            sem_rows = await similar_neighbor_tickets(
                conn,
                query_vec,
                neighbor_sid_strs,
                exclude_issue_key=issue_key,
                limit=SEMANTIC_LIMIT_NEIGHBOR,
            )
            if len(sem_rows) < SEMANTIC_LIMIT_NEIGHBOR:
                rec_rows = await list_tickets_for_service_ids(
                    conn,
                    neighbor_sid_strs,
                    exclude_issue_key=issue_key,
                    limit=NEIGHBOR_TICKET_LIMIT,
                )
                neighbor_tickets = merge_with_recency_fallback(
                    sem_rows, rec_rows, target=SEMANTIC_LIMIT_NEIGHBOR
                )
            else:
                neighbor_tickets = sem_rows
```

- [ ] **Step 12.4: Restart ops-agent and check for startup errors**

If `./run.sh` is running with `--reload`, it will auto-restart. Watch the log. Expected: the process restarts cleanly; no ImportError; no unclosed-connection warnings.

Then open a ticket in the browser (e.g. `http://127.0.0.1:8080/tickets/APTUM-38273`) and confirm the sidebar still renders. We have NOT yet updated the template, so the new `similarity_score` and `ranked_by` fields are ignored by Jinja — that's fine.

- [ ] **Step 12.5: Commit**

```bash
cd /Users/anelson-macbook-air/connected-brain
git add projects/ops-agent/ops_agent/db.py projects/ops-agent/ops_agent/context/t_context.py
git commit -m "feat(ops-agent): swap customer + neighbor panels to semantic ranking with recency fallback"
```

---

## Task 13: Show the similarity score in the sidebar template

**Files:**
- Modify: `projects/ops-agent/ops_agent/templates/related_panel.html`

We want each ticket row to display:
- its percent similarity (two decimal places × 100, e.g. `87%`)
- a small badge when the row was recency-padded instead of semantically ranked

- [ ] **Step 13.1: Modify `projects/ops-agent/ops_agent/templates/related_panel.html`**

In the "Customer ticket history" section, find this `<li>` block (currently ~lines 23-33):

```html
        {% for t in ctx.customer_tickets[:15] %}
        <li>
            <a href="/tickets/{{ t.issue_key }}">{{ t.issue_key }}</a>
            <span class="muted">{{ t.status }}</span>
            {% if t.fusion_company_name or t.jira_org_name %}
            <span class="related-entity">{{ t.fusion_company_name or t.jira_org_name }}</span>
            {% endif %}
            {% set summ = t.summary or '' %}
            <div class="related-summary">{{ summ[:140] }}{% if summ|length > 140 %}…{% endif %}</div>
        </li>
        {% endfor %}
```

Replace with:

```html
        {% for t in ctx.customer_tickets[:15] %}
        <li>
            <a href="/tickets/{{ t.issue_key }}">{{ t.issue_key }}</a>
            <span class="muted">{{ t.status }}</span>
            {% if t.similarity_score is not none %}
            <span class="sim-badge" title="cosine similarity to current ticket">
                {{ (t.similarity_score * 100) | round(0, 'floor') | int }}%
            </span>
            {% elif t.ranked_by == 'recency' %}
            <span class="sim-badge sim-badge-recency" title="no embedding yet — showing by recency">recent</span>
            {% endif %}
            {% if t.fusion_company_name or t.jira_org_name %}
            <span class="related-entity">{{ t.fusion_company_name or t.jira_org_name }}</span>
            {% endif %}
            {% set summ = t.summary or '' %}
            <div class="related-summary">{{ summ[:140] }}{% if summ|length > 140 %}…{% endif %}</div>
        </li>
        {% endfor %}
```

In the "Tickets on similar hardware" section, find this `<li>` block (currently ~lines 86-97):

```html
        {% for t in ctx.neighbor_tickets[:12] %}
        <li>
            <a href="/tickets/{{ t.issue_key }}">{{ t.issue_key }}</a>
            <span class="muted">{{ t.status }}</span>
            {% if t.fusion_company_name or t.jira_org_name %}
            <span class="related-entity">{{ t.fusion_company_name or t.jira_org_name }}</span>
            {% elif t.ocean_client_id %}
            <span class="muted">client {{ t.ocean_client_id }}</span>
            {% endif %}
            {% set summ2 = t.summary or '' %}
            <div class="related-summary">{{ summ2[:120] }}{% if summ2|length > 120 %}…{% endif %}</div>
        </li>
        {% endfor %}
```

Replace with:

```html
        {% for t in ctx.neighbor_tickets[:12] %}
        <li>
            <a href="/tickets/{{ t.issue_key }}">{{ t.issue_key }}</a>
            <span class="muted">{{ t.status }}</span>
            {% if t.similarity_score is not none %}
            <span class="sim-badge" title="cosine similarity to current ticket">
                {{ (t.similarity_score * 100) | round(0, 'floor') | int }}%
            </span>
            {% elif t.ranked_by == 'recency' %}
            <span class="sim-badge sim-badge-recency" title="no embedding yet — showing by recency">recent</span>
            {% endif %}
            {% if t.fusion_company_name or t.jira_org_name %}
            <span class="related-entity">{{ t.fusion_company_name or t.jira_org_name }}</span>
            {% elif t.ocean_client_id %}
            <span class="muted">client {{ t.ocean_client_id }}</span>
            {% endif %}
            {% set summ2 = t.summary or '' %}
            <div class="related-summary">{{ summ2[:120] }}{% if summ2|length > 120 %}…{% endif %}</div>
        </li>
        {% endfor %}
```

- [ ] **Step 13.2: Add styles for `.sim-badge` to `projects/ops-agent/ops_agent/static/styles.css`**

Append this block to the existing CSS (do not replace — append at end):

```css
/* Semantic similarity badges in the related-panel sidebar (Task v3). */
.sim-badge {
    display: inline-block;
    padding: 1px 6px;
    margin-left: 4px;
    font-size: 11px;
    font-weight: 600;
    border-radius: 10px;
    background: #e3f2fd;
    color: #0d47a1;
    vertical-align: middle;
}
.sim-badge-recency {
    background: #f5f5f5;
    color: #616161;
    font-weight: 500;
}
```

- [ ] **Step 13.3: Reload the page and verify the badges render**

Open `http://127.0.0.1:8080/tickets/APTUM-38273` (or whichever ticket you're testing). Every ticket row in the two affected panels should now have a `NN%` badge next to the status.

- [ ] **Step 13.4: Commit**

```bash
cd /Users/anelson-macbook-air/connected-brain
git add projects/ops-agent/ops_agent/templates/related_panel.html \
        projects/ops-agent/ops_agent/static/styles.css
git commit -m "feat(ops-agent): show semantic similarity % + recency badge in related panels"
```

---

## Task 14: End-to-end visual verification

**Files:** (none — verification only)

- [ ] **Step 14.1: Restart ops-agent cleanly if it hasn't auto-reloaded**

```bash
cd /Users/anelson-macbook-air/connected-brain/projects/ops-agent
# If something already owns :8080:
PID=$(lsof -iTCP:8080 -sTCP:LISTEN -nP -t 2>/dev/null | head -1)
if [ -n "$PID" ]; then kill "$PID" && sleep 2; fi
./run.sh >/tmp/ops-agent-v3.log 2>&1 &
sleep 6
tail -n 30 /tmp/ops-agent-v3.log
```

Expected final log lines:
```
... Embedder warm (BAAI/bge-base-en-v1.5)
... ops-agent started at http://127.0.0.1:8080
INFO:     Application startup complete.
```

- [ ] **Step 14.2: Open two known tickets and eyeball the sidebar**

Open in a browser:
1. `http://127.0.0.1:8080/tickets/APTUM-38273` ("Firewall Firmware Upgrade – Maintenance Window Request")
2. `http://127.0.0.1:8080/tickets/APTUM-57415` ("IP Aliases monitoring alerts possibly causing downtime")

Acceptance criteria (human judgement):

**Ticket APTUM-38273 — "Customer ticket history" panel:**
- Rows should display a `%` badge on each.
- Rows near the top should be about firmware/upgrades/maintenance/firewall if SPORTS INC has any such tickets. If none exist, the badges on top rows will simply be the best available — that's fine; the signal is "highest available semantic match", not "perfect match".

**Ticket APTUM-38273 — "Tickets on similar hardware" panel:**
- `APTUM-51673 "Firewall Firmware Upgrade – Maintenance Window Request"` MUST appear in the top 5 with a high similarity badge (80%+).
- `APTUM-51630 "Upgrade SRX Firewalls"` should also appear in the top half.
- Billing questions, non-renewal notices, IP whitelist rules — if they appear at all — should be below the topically-similar hits, and carry visibly lower similarity scores.

**Ticket APTUM-57415 — "Customer ticket history" panel:**
- `APTUM-46617`, `APTUM-43398`, `APTUM-43755`, and other "Zabbix Alert: DLS-P4 Ping Loss" tickets MUST rank in the top 5.
- "Customer Credit Request", "Veeam backup charges", "Invoice for SID..." must NOT be in the top 5. If they appear at all, they should be near the bottom with a visibly low score.

If any of those acceptance bullets fails, STOP and report before closing out. Possible causes to investigate:
- Embedding text is being built from the wrong columns.
- Vector codec registration did not happen (the KNN query silently returns nothing, and you're seeing the recency fallback entirely).
- Model did not load (log will say "Embedder failed to warm").

- [ ] **Step 14.3: Final commit (only if you made fixups in 14.2)**

If no fixups needed, nothing to commit — proceed to Task 15.

---

## Task 15: Update docs + re-anchor so the next session knows this shipped

**Files:**
- Modify: `vault/80-sessions/ops-agent/session-001.md`

- [ ] **Step 15.1: Add a short addendum to the bottom of the re-anchor**

Open `vault/80-sessions/ops-agent/session-001.md` and append this block at the very end of the file (after the existing "Context blocks used" section):

```markdown
---

## Addendum — v3 embeddings shipped (YYYY-MM-DD)

The sidebar panels now rank tickets by **semantic similarity** to the current ticket, not recency.

- pgvector is enabled on the local Postgres (image `pgvector/pgvector:pg16`).
- `ticket_embeddings` table holds 768-dim `BAAI/bge-base-en-v1.5` vectors; HNSW cosine index.
- `jsm_sync.embed_backfill` is idempotent (`python3 -m jsm_sync.embed_backfill`).
- `jsm_sync.incremental` embeds new/stale tickets at the end of each cron run (non-fatal on failure).
- ops-agent loads the same model once in `lifespan`. Query path in
  `ops_agent/context/semantic.py`; recency fallback in `merge_with_recency_fallback`.
- Sidebar rows carry `similarity_score` (0-1) and `ranked_by` (`semantic` | `recency`);
  the template shows a `NN%` badge.

**DO NOT replace the recency fallback without thinking.** It is what keeps the sidebar
from ever being empty for a brand-new ticket the cron hasn't embedded yet.

**To add a new model later:** pick a new `MODEL_NAME` in `embedder.py`, re-run
`embed_backfill.py` — rows are keyed by `(issue_key, model)` so old + new coexist.
```

Replace `YYYY-MM-DD` with today's date.

- [ ] **Step 15.2: Commit**

```bash
cd /Users/anelson-macbook-air/connected-brain
git add vault/80-sessions/ops-agent/session-001.md
git commit -m "docs(re-anchor): note v3 semantic similarity shipped"
```

---

## Appendix A — rollback

If any task goes wrong and you need to revert the Postgres image:

```bash
cd /Users/anelson-macbook-air/connected-brain/projects/jsm-sync
# Edit docker-compose.yml: change image back to postgres:16
docker compose up -d postgres
```

The vector extension and `ticket_embeddings` rows remain on disk. The base `postgres:16` image doesn't have the `vector` binary, so queries that cast to `vector` will fail. Either re-apply the pgvector image, or drop the embedding artifacts:

```bash
docker compose exec -T postgres psql -U jsm_sync -d jsm_sync -c \
  "DROP TABLE IF EXISTS ticket_embeddings; DROP EXTENSION IF EXISTS vector;"
```

The application code in `t_context.py` degrades gracefully — if no rows are returned from the semantic queries, `merge_with_recency_fallback` fills entirely from `list_customer_tickets` / `list_tickets_for_service_ids`, which is the old behavior.

## Appendix B — throughput sanity

On an M-series Mac with MPS, expect roughly:
- Backfill of 55k tickets at batch=64: 15-25 min elapsed (first run includes ~2 min for model download).
- Incremental catch-up of ~5 changed tickets at the end of a cron run: sub-second.
- Query-time on-the-fly embed for the current ticket: 20-60 ms.
- HNSW kNN over 55k rows: sub-10 ms per panel.

If backfill is dramatically slower than this, check `_resolve_device()` returned `mps` (log line appears on first embed call). Running on CPU instead of MPS drops throughput 5-10×.

## Appendix C — model upgrade path (future work — do NOT do now)

The table is already `(issue_key, model)` PK and has a btree index on `model`, so adding `BAAI/bge-large-en-v1.5` (1024 dims) or `mixedbread-ai/mxbai-embed-large-v1` later is straightforward:

1. Update `MODEL_NAME` + `MODEL_DIM` in both `embedder.py` copies.
2. Add a new `CREATE INDEX … USING hnsw` on the new-dim vectors *before* backfilling.
3. Re-run `embed_backfill`.
4. Once coverage is 100%, either delete the old-model rows or keep them for A/B eval.

---

**End of plan.**
