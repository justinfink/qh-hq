"""Embeddings service. Tries Voyage AI first, then OpenAI, then local FastEmbed,
then graceful zero-vector fallback. All produce 1024-dim vectors so the schema
is invariant.
"""
from __future__ import annotations

import asyncio
import hashlib
import logging
import os
from functools import lru_cache
from typing import Literal

from app.config import settings

logger = logging.getLogger(__name__)

EMBEDDING_DIM = 1024
VOYAGE_MODEL = "voyage-3-large"
OPENAI_MODEL = "text-embedding-3-small"  # supports custom dimensions
FASTEMBED_MODEL = "BAAI/bge-large-en-v1.5"


@lru_cache(maxsize=1)
def _fastembed_model():
    try:
        from fastembed import TextEmbedding
        logger.info("Loading FastEmbed model: %s", FASTEMBED_MODEL)
        return TextEmbedding(model_name=FASTEMBED_MODEL)
    except ImportError:
        logger.warning("fastembed not installed; trying other providers")
        return None


_voyage_client = None
_openai_client = None


def _get_voyage():
    global _voyage_client
    if _voyage_client is None:
        try:
            import voyageai
            _voyage_client = voyageai.AsyncClient(api_key=settings.voyage_api_key)
        except ImportError:
            logger.warning("voyageai not installed")
            return None
    return _voyage_client


def _get_openai():
    global _openai_client
    if _openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None
        try:
            import httpx
            _openai_client = httpx.AsyncClient(
                base_url="https://api.openai.com/v1",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=15.0,
            )
        except ImportError:
            return None
    return _openai_client


_cache: dict[str, list[float]] = {}


def _key(text: str, input_type: str) -> str:
    return hashlib.sha256(f"{input_type}::{text}".encode()).hexdigest()


def _zero_vector() -> list[float]:
    return [0.0] * EMBEDDING_DIM


async def _openai_embed(texts: list[str]) -> list[list[float]] | None:
    client = _get_openai()
    if client is None:
        return None
    try:
        resp = await client.post(
            "/embeddings",
            json={
                "input": texts,
                "model": OPENAI_MODEL,
                "dimensions": EMBEDDING_DIM,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return [item["embedding"] for item in data["data"]]
    except Exception as exc:
        logger.warning("OpenAI embedding failed: %s", exc)
        return None


async def embed_text(
    text: str,
    input_type: Literal["document", "query"] = "document",
) -> list[float]:
    if os.getenv("SKIP_EMBEDDINGS") == "1":
        return _zero_vector()
    if not text or not text.strip():
        return _zero_vector()

    key = _key(text, input_type)
    if key in _cache:
        return _cache[key]

    # Provider 1: Voyage (highest quality if available)
    if settings.voyage_api_key:
        client = _get_voyage()
        if client:
            try:
                result = await client.embed(
                    texts=[text], model=VOYAGE_MODEL, input_type=input_type,
                )
                vec = result.embeddings[0]
                _cache[key] = vec
                return vec
            except Exception as exc:
                logger.warning("Voyage embedding failed, falling through: %s", exc)

    # Provider 2: OpenAI (cheap, fast, serverless-friendly)
    openai_result = await _openai_embed([text])
    if openai_result:
        vec = openai_result[0]
        _cache[key] = vec
        return vec

    # Provider 3: Local FastEmbed (no key required, but heavy)
    model = _fastembed_model()
    if model is not None:
        loop = asyncio.get_running_loop()
        embeddings = await loop.run_in_executor(None, lambda: list(model.embed([text])))
        vec = embeddings[0].tolist() if hasattr(embeddings[0], "tolist") else list(embeddings[0])
        _cache[key] = vec
        return vec

    return _zero_vector()


async def embed_batch(
    texts: list[str],
    input_type: Literal["document", "query"] = "document",
    batch_size: int = 64,
) -> list[list[float]]:
    if os.getenv("SKIP_EMBEDDINGS") == "1":
        return [_zero_vector() for _ in texts]
    if not texts:
        return []

    if settings.voyage_api_key:
        client = _get_voyage()
        if client:
            try:
                results: list[list[float]] = []
                for i in range(0, len(texts), batch_size):
                    chunk = texts[i : i + batch_size]
                    res = await client.embed(
                        texts=chunk, model=VOYAGE_MODEL, input_type=input_type,
                    )
                    results.extend(res.embeddings)
                    if i + batch_size < len(texts):
                        await asyncio.sleep(0.1)
                return results
            except Exception as exc:
                logger.warning("Voyage batch embedding failed, falling through: %s", exc)

    # OpenAI: batch up to 64 per call
    openai_result = await _openai_embed(texts[:batch_size])
    if openai_result:
        results = list(openai_result)
        for i in range(batch_size, len(texts), batch_size):
            chunk = texts[i : i + batch_size]
            more = await _openai_embed(chunk)
            if more is None:
                break
            results.extend(more)
            await asyncio.sleep(0.05)
        if len(results) == len(texts):
            return results

    model = _fastembed_model()
    if model is None:
        return [_zero_vector() for _ in texts]

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
