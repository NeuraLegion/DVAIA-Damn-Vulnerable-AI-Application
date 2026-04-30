"""
LangChain LLM factory: get_llm(model_id) returns a BaseChatModel for simple or agentic use.

Use for:
  - Simple: llm.invoke(messages) or use core.models.generate()
  - Agentic: llm.bind_tools(tools), create_react_agent(), RAG chains, etc.

Backend: OpenAI API (OPENAI_API_KEY from env).

Examples: gpt-4o-mini, gpt-4o, gpt-3.5-turbo
"""
import warnings
from typing import Any, Optional

# Suppress LangChain/Pydantic v1 warning on Python 3.14+ (langchain_core still uses pydantic.v1)
warnings.filterwarnings(
    "ignore",
    message=".*Pydantic V1.*Python 3.14.*",
)

from core.config import get_default_model_id, get_openai_api_key

OPENAI_PREFIX = "openai:"


def _openai_model_name(model_id: str) -> str:
    """Extract OpenAI model name (strip openai: prefix if present)."""
    if not model_id or not str(model_id).strip():
        return "gpt-4o-mini"
    s = model_id.strip()
    if s.lower().startswith(OPENAI_PREFIX):
        s = s[len(OPENAI_PREFIX):].strip()
    return s or "gpt-4o-mini"


def get_llm(
    model_id: Optional[str] = None,
    *,
    timeout: Optional[int] = 120,
    **kwargs: Any,
) -> Any:
    """
    Return a LangChain ChatOpenAI model for the given model_id.

    Uses DEFAULT_MODEL from env when model_id is not passed.
    Requires OPENAI_API_KEY to be set in the environment.
    """
    resolved = (model_id or get_default_model_id()).strip()
    if not resolved:
        resolved = get_default_model_id()

    name = _openai_model_name(resolved)
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=name,
        api_key=get_openai_api_key(),
        timeout=timeout,
        **kwargs,
    )
