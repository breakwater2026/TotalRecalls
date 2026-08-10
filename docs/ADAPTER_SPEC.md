# Adapter specification (Phase 3)

## ProviderAdapter (data plane)

Login/UI stay in the desktop shell. Adapters receive an already-captured
**credential string** (e.g. Perplexity session token).

```python
class ProviderAdapter(Protocol):
    id: str                 # "perplexity", "chatgpt", ...
    display_name: str

    def validate(self, credential: str) -> AccountInfo: ...
    def list_conversations(self, credential: str, *, deep: bool = False) -> list[ConversationSummary]: ...
    def fetch_conversation(self, credential: str, conv_id: str) -> UnifiedConversation: ...
```

Registry:

```python
from totalrecalls.adapters.base import get_adapter, list_provider_ids
a = get_adapter("perplexity")
```

## Implementing a new provider

1. Create `totalrecalls/adapters/<name>/` with HTTP + auth + mapping.
2. Implement `XAdapter` with `id`, `display_name`, `validate`, `list_conversations`, `fetch_conversation`.
3. Map provider payloads → `UnifiedConversation` (`totalrecalls.core.schema`).
4. Register in `totalrecalls.adapters.base._ensure_builtins` (or call `register_provider`).
5. Add unit tests that mock HTTP and assert unified shape.

## Export

`export_via_adapter(adapter, credential, outdir, ...)` writes:

```
outdir/
  Library/<provider>/Home|Spaces/.../<Title -- shortid>/
    conversation.md
    conversation.json   # unified schema
    thread.md           # alias of conversation.md
  README.md
  manifest.json         # layout: library-v1
  uuid_index.json
```

Desktop Bridge default export uses this path. Set env
`TOTALRECALLS_CLASSIC_EXPORT=1` to force the pre-Phase-3 Spaces/Home-at-root layout.
