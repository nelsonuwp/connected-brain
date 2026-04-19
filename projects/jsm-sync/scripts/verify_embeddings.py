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
import os
import sys

import asyncpg

# Support both `python3 -m scripts.verify_embeddings` and plain `python3 scripts/verify_embeddings.py`.
# When run as a script, the package parent isn't on sys.path — fix that.
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
        min_size=1,
        max_size=2,
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
                issue_key,
                MODEL_NAME,
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
                src["embedding"],
                issue_key,
                MODEL_NAME,
                k,
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
