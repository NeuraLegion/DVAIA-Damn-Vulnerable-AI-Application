"""
Core service layer: model routing, config, and LangChain LLM factory.
Config is imported eagerly; models and llm are lazy so run_tests.py works without LangChain.
"""
from core.config import DEFAULT_MODEL, get_default_model_id, get_openai_api_key

__all__ = [
    "DEFAULT_MODEL",
    "get_default_model_id",
    "get_openai_api_key",
    "get_llm",
    "generate",
]


def __getattr__(name: str):
    """Lazy load models/llm so runner (core.config only) does not require LangChain."""
    if name == "generate":
        from core import models
        return getattr(models, name)
    if name == "get_llm":
        from core import llm
        return getattr(llm, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
