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
