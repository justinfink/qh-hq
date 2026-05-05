"""Embeddings service. Tries Voyage AI first; falls back to local FastEmbed (BGE-large)
if no API key is configured. Both produce 1024-dim vectors so the schema is invariant.
"""
from __future__ import annotations

import asyncio
import hashlib
import logging
from functools import lru_cache
from typing import Literal

from app.config import settings

logger = logging.getLogger(__name__)

EMBEDDING_DIM = 1024
VOYAGE_MODEL = "voyage-3-large"
FASTEMBED_MODEL = "BAAI/bge-large-en-v1.5"  # 1024 dim


@lru_cache(maxsize=1)
def _fastembed_model():
    from fastembed import TextEmbedding
    logger.info("Loading FastEmbed model: %s (this may take a moment on first run)", FASTEMBED_MODEL)
    return TextEmbedding(model_name=FASTEMBED_MODEL)


_voyage_client = None


def _get_voyage():
    global _voyage_client
    if _voyage_client is None:
        import voyageai
        _voyage_client = voyageai.AsyncClient(api_key=settings.voyage_api_key)
    return _voyage_client


_cache: dict[str, list[float]] = {}


def _key(text: str, input_type: str) -> str:
    return hashlib.sha256(f"{input_type}::{text}".encode()).hexdigest()


async def embed_text(
    text: str,
    input_type: Literal["document", "query"] = "document",
) -> list[float]:
    import os as _os
    if _os.getenv("SKIP_EMBEDDINGS") == "1":
        return [0.0] * EMBEDDING_DIM
    if not text or not text.strip():
        return [0.0] * EMBEDDING_DIM

    key = _key(text, input_type)
    if key in _cache:
        return _cache[key]

    if settings.voyage_api_key:
        client = _get_voyage()
        result = await client.embed(
            texts=[text],
            model=VOYAGE_MODEL,
            input_type=input_type,
        )
        vec = result.embeddings[0]
    else:
        # Local FastEmbed fallback — synchronous; run in thread pool
        model = _fastembed_model()
        loop = asyncio.get_running_loop()
        embeddings = await loop.run_in_executor(None, lambda: list(model.embed([text])))
        vec = embeddings[0].tolist() if hasattr(embeddings[0], "tolist") else list(embeddings[0])

    _cache[key] = vec
    return vec


async def embed_batch(
    texts: list[str],
    input_type: Literal["document", "query"] = "document",
    batch_size: int = 64,
) -> list[list[float]]:
    import os as _os
    if _os.getenv("SKIP_EMBEDDINGS") == "1":
        return [[0.0] * EMBEDDING_DIM for _ in texts]
    if not texts:
        return []

    if settings.voyage_api_key:
        client = _get_voyage()
        results: list[list[float]] = []
        for i in range(0, len(texts), batch_size):
            chunk = texts[i : i + batch_size]
            res = await client.embed(
                texts=chunk,
                model=VOYAGE_MODEL,
                input_type=input_type,
            )
            results.extend(res.embeddings)
            if i + batch_size < len(texts):
                await asyncio.sleep(0.1)
        return results

    # FastEmbed local
    model = _fastembed_model()
    loop = asyncio.get_running_loop()
    embeddings = await loop.run_in_executor(None, lambda: list(model.embed(texts)))
    return [e.tolist() if hasattr(e, "tolist") else list(e) for e in embeddings]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
