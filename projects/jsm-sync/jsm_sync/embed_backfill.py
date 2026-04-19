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
