"""Provider adapter protocol and registry."""

from __future__ import annotations

from typing import Callable, Protocol, runtime_checkable

from totalrecalls.core.schema import AccountInfo, ConversationSummary, UnifiedConversation


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
