"""
Embedding service for RAG using Ollama local models only.
Documents and chunks are embedded when added; search uses similarity over vectors.
"""
from typing import List

from core.config import (
    get_embedding_model_id,
    get_ollama_host,
)

_embeddings_ollama = None


def _get_embeddings():
    """Lazy init Ollama embeddings."""
    global _embeddings_ollama
    if _embeddings_ollama is None:
        try:
            from langchain_ollama import OllamaEmbeddings
        except ImportError:
            raise RuntimeError(
                "Ollama embeddings require langchain-ollama. pip install langchain-ollama"
            )
        model = get_embedding_model_id()
        base_url = get_ollama_host()
        _embeddings_ollama = OllamaEmbeddings(model=model, base_url=base_url)
    return _embeddings_ollama


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
