"""
Model router: generate(prompt, model_id) for OpenAI models.

Uses LangChain under the hood (core.llm.get_llm) so simple and agentic flows share one stack.
model_id format:
  - "gpt-4o-mini" or "openai:gpt-4o-mini" → OpenAI API
"""
from __future__ import annotations

import warnings
from typing import Any, Dict, List, Optional

# Suppress LangChain/Pydantic v1 warning on Python 3.14+ (before first langchain import)
warnings.filterwarnings(
    "ignore",
    message=".*Pydantic V1.*Python 3.14.*",
)

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from core.config import DEFAULT_MODEL
from core.llm import get_llm


def _options_to_llm_kwargs(options: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Map request options to get_llm kwargs for OpenAI."""
    if not options:
        return {}
    out: Dict[str, Any] = {}
    num = options.get("max_tokens")
    if num is not None:
        try:
            out["max_tokens"] = int(num)
        except (TypeError, ValueError):
            pass
    if "temperature" in options and options["temperature"] is not None:
        try:
            out["temperature"] = float(options["temperature"])
        except (TypeError, ValueError):
            pass
    if "top_p" in options and options["top_p"] is not None:
        try:
            out["top_p"] = float(options["top_p"])
        except (TypeError, ValueError):
            pass
    return out


def _messages_to_lc(messages: List[Dict[str, str]]) -> List[BaseMessage]:
    """Convert [{"role": "user", "content": "..."}, ...] to LangChain message list."""
    lc: List[BaseMessage] = []
    for m in messages:
        role = (m.get("role") or "user").strip().lower()
        content = (m.get("content") or "").strip()
        if not content:
            continue
        if role == "system":
            lc.append(SystemMessage(content=content))
        elif role == "assistant":
            lc.append(AIMessage(content=content))
        else:
            lc.append(HumanMessage(content=content))
    return lc


def generate(
    prompt: Optional[str] = None,
    model_id: Optional[str] = DEFAULT_MODEL,
    options: Optional[Dict[str, Any]] = None,
    messages: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, str]:
    """
    Send prompt or messages to OpenAI model.
    - prompt: single turn (optional if messages is set).
    - messages: multi-turn list of {role, content}; used instead of prompt when set.
    - options: generation options (max_tokens, temperature, top_p) to cap output length.
    Returns {"text": str, "thinking": ""}.
    """
    model_id = model_id or DEFAULT_MODEL
    
    llm_kwargs = _options_to_llm_kwargs(options)
    llm = get_llm(model_id, **llm_kwargs)

    if messages:
        lc_messages = _messages_to_lc(messages)
        if not lc_messages:
            return {"text": "No text returned.", "thinking": ""}
        msg = llm.invoke(lc_messages)
    else:
        prompt = prompt or ""
        msg = llm.invoke([HumanMessage(content=prompt)])

    text = getattr(msg, "content", None) or ""
    text = (text if isinstance(text, str) else "").strip() or "No text returned."
    
    return {"text": text, "thinking": ""}
