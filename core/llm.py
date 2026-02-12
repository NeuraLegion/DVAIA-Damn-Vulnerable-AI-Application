"""
LangChain LLM factory: get_llm(model_id) returns a BaseChatModel for simple or agentic use.

Use for:
  - Simple: llm.invoke(messages) or use core.models.generate()
  - Agentic: llm.bind_tools(tools), create_react_agent(), RAG chains, etc.

Backend: Ollama local models only (OLLAMA_HOST from env).

Examples: ollama:llama3.2, llama3.2, llama3.1
"""
import warnings
from typing import Any, Optional

# Suppress LangChain/Pydantic v1 warning on Python 3.14+ (langchain_core still uses pydantic.v1)
warnings.filterwarnings(
    "ignore",
    message=".*Pydantic V1.*Python 3.14.*",
)

from core.config import get_default_model_id, get_ollama_host

OLLAMA_PREFIX = "ollama:"


def _ollama_model_name(model_id: str) -> str:
    """Extract Ollama model name (strip ollama: prefix if present)."""
    if not model_id or not str(model_id).strip():
        return "llama3.2"
    s = model_id.strip()
    if s.lower().startswith(OLLAMA_PREFIX):
        s = s[len(OLLAMA_PREFIX) :].strip()
    return s or "llama3.2"


def get_llm(
    model_id: Optional[str] = None,
    *,
    timeout: Optional[int] = 120,
    **kwargs: Any,
) -> Any:
    """
    Return a LangChain ChatOllama model for the given model_id.

    Uses DEFAULT_MODEL from env when model_id is not passed.
    All models run via Ollama local instance.
    """
    resolved = (model_id or get_default_model_id()).strip()
    if not resolved:
        resolved = get_default_model_id()

    name = _ollama_model_name(resolved)
    from langchain_ollama import ChatOllama

    return ChatOllama(
        model=name,
        base_url=get_ollama_host().rstrip("/"),
        timeout=timeout,
        **kwargs,
    )
