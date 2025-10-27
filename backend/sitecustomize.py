"""Runtime compatibility shims for third-party dependencies."""
from __future__ import annotations

import importlib
import sys
import types
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import only for type checking
    from llama_index.core.base.llms.types import ChatMessage  # noqa: F401


def _ensure_llama_index_llms_alias() -> None:
    """Expose ``llama_index.llms.ChatMessage`` for legacy import paths."""

    try:
        from llama_index.core.base.llms.types import ChatMessage  # type: ignore
    except Exception:  # pragma: no cover - defensive fallback
        try:
            from llama_index.core.chat_engine.types import ChatMessage  # type: ignore
        except Exception:
            return

    try:
        module = importlib.import_module("llama_index.llms")
    except Exception:
        module = types.ModuleType("llama_index.llms")
        sys.modules.setdefault("llama_index.llms", module)
        try:
            package = importlib.import_module("llama_index")
        except Exception:  # pragma: no cover - the base package is missing
            return
        setattr(package, "llms", module)

    if not hasattr(module, "ChatMessage"):
        module.ChatMessage = ChatMessage  # type: ignore[attr-defined]


_ensure_llama_index_llms_alias()
