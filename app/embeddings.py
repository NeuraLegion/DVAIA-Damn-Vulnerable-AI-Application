"""
Embedding service for RAG using OpenAI-compatible embeddings endpoint.
Documents and chunks are embedded when added; search uses similarity over vectors.
"""
from typing import List

from core.config import (
    get_embedding_model_id,
    get_openai_api_key,
    get_openai_base_url,
)

_embeddings_client = None


def _get_embeddings():
    """Lazy init OpenAI embeddings."""
    global _embeddings_client
    if _embeddings_client is None:
        try:
            from langchain_openai import OpenAIEmbeddings
        except ImportError:
            raise RuntimeError(
                "OpenAI embeddings require langchain-openai. pip install langchain-openai"
            )
        api_key = get_openai_api_key()
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required")
        model = get_embedding_model_id()
        base_url = get_openai_base_url()
        _embeddings_client = OpenAIEmbeddings(
            model=model,
            openai_api_key=api_key,
            openai_api_base=base_url,
        )
    return _embeddings_client


def embed_text(text: str) -> List[float]:
    """Embed a single string; returns list of floats."""
    if not (text or "").strip():
        return []
    emb = _get_embeddings()
    return emb.embed_query(text.strip())


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed multiple strings; returns list of vectors."""
    if not texts:
        return []
    stripped = [t.strip() for t in texts if (t or "").strip()]
    if not stripped:
        return []
    emb = _get_embeddings()
    return emb.embed_documents(stripped)


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Cosine similarity between two vectors. Assumes non-zero."""
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
