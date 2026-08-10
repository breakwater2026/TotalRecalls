# Unified conversation schema v1

Machine-readable archive format for TotalRecalls multi-provider exports.

```json
{
  "schema_version": 1,
  "provider": "perplexity",
  "account": {
    "email": "user@example.com",
    "external_id": "",
    "display_name": ""
  },
  "conversation": {
    "id": "provider-native-id",
    "title": "Conversation title",
    "created_at": "ISO-8601 or provider stamp",
    "updated_at": "",
    "folder": "Home",
    "messages": [
      {
        "role": "user",
        "content_md": "Question text",
        "created_at": "",
        "model": "",
        "citations": [],
        "external_id": ""
      },
      {
        "role": "assistant",
        "content_md": "Answer markdown",
        "created_at": "",
        "model": "optional-model-id",
        "citations": [
          { "title": "Source", "url": "https://...", "snippet": "" }
        ],
        "external_id": "entry-id"
      }
    ]
  },
  "raw": { }
}
```

## Roles

- `user` — human turns
- `assistant` — model turns
- `system` / `tool` — reserved for future providers

## Python API

```python
from totalrecalls.core.schema import UnifiedConversation, Message, AccountInfo
conv = UnifiedConversation.from_dict(data)
payload = conv.to_dict()
```

On-disk file: `conversation.json` next to `conversation.md` under
`Library/<provider>/…`.
