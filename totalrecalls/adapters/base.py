"""Provider adapter protocol and registry."""

from __future__ import annotations

import inspect

from typing import Callable, Protocol, runtime_checkable

from totalrecalls.core.schema import AccountInfo, ConversationSummary, UnifiedConversation


def call_with_stop(fn, *args, stop_event=None, **kwargs):
    """Invoke ``fn``, injecting ``stop_event`` only when its signature accepts it.

    The desktop bridge owns a disconnect Event and wants every adapter call
    to abort mid-retry when the user disconnects. Only the ChatGPT adapter
    (so far) accepts ``stop_event``; every other adapter keeps its plain
    ``(credential, ...)`` signature. This wrapper keeps the bridge's
    provider-agnostic code path while letting cancellation-capable adapters
    receive the event.
    """
    if stop_event is None:
        return fn(*args, **kwargs)
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):
        return fn(*args, **kwargs)
    if "stop_event" in sig.parameters:
        kwargs["stop_event"] = stop_event
    return fn(*args, **kwargs)


@runtime_checkable
class ProviderAdapter(Protocol):
    """Data-plane interface for one AI chat provider.

    Login/UI stays in the desktop shell. Adapters only need a credential
    string (session token, etc.) already obtained by the host.
    """

    id: str
    display_name: str

    def validate(self, credential: str) -> AccountInfo:
        """Return account info or raise on invalid credential."""
        ...

    def list_conversations(
        self, credential: str, *, deep: bool = False
    ) -> list[ConversationSummary]:
        ...

    def fetch_conversation(
        self, credential: str, conv_id: str
    ) -> UnifiedConversation:
        ...


_REGISTRY: dict[str, Callable[[], ProviderAdapter]] = {}


def register_provider(provider_id: str, factory: Callable[[], ProviderAdapter]) -> None:
    _REGISTRY[provider_id] = factory


def list_provider_ids() -> list[str]:
    _ensure_builtins()
    return sorted(_REGISTRY.keys())


def get_adapter(provider_id: str) -> ProviderAdapter:
    _ensure_builtins()
    try:
        factory = _REGISTRY[provider_id]
    except KeyError as e:
        raise KeyError(f"Unknown provider: {provider_id!r}. Known: {list_provider_ids()}") from e
    return factory()


def _ensure_builtins() -> None:
    # Register each known adapter once (idempotent)
    if "perplexity" not in _REGISTRY:
        from totalrecalls.adapters.perplexity.adapter import PerplexityAdapter
        register_provider("perplexity", PerplexityAdapter)
    if "chatgpt" not in _REGISTRY:
        from totalrecalls.adapters.chatgpt.adapter import ChatGptAdapter
        register_provider("chatgpt", ChatGptAdapter)
    if "claude" not in _REGISTRY:
        from totalrecalls.adapters.claude.adapter import ClaudeAdapter
        register_provider("claude", ClaudeAdapter)
    if "gemini" not in _REGISTRY:
        from totalrecalls.adapters.gemini.adapter import GeminiAdapter
        register_provider("gemini", GeminiAdapter)
    if "grok" not in _REGISTRY:
        from totalrecalls.adapters.grok.adapter import GrokAdapter
        register_provider("grok", GrokAdapter)
    if "mistral" not in _REGISTRY:
        from totalrecalls.adapters.mistral.adapter import MistralAdapter
        register_provider("mistral", MistralAdapter)
    if "deepseek" not in _REGISTRY:
        from totalrecalls.adapters.deepseek.adapter import DeepSeekAdapter
        register_provider("deepseek", DeepSeekAdapter)
    if "qwen" not in _REGISTRY:
        from totalrecalls.adapters.qwen.adapter import QwenChatAdapter
        register_provider("qwen", QwenChatAdapter)
