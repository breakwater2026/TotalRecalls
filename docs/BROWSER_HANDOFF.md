# Browser conversation handoff

TotalRecalls supports a deliberately small, file-based browser companion
workflow. A companion or a provider's page can download the **current**
conversation as JSON; the user then imports that file locally. This avoids
browser credentials, a localhost server, and provider API calls.

## Import

```powershell
python tools\import_browser_handoff.py .\conversation.handoff.json `
  --output "$env:USERPROFILE\TotalRecalls"
```

The importer writes the conversation to the normal
`Library\<provider>\...` layout as `conversation.json`, `conversation.md`, and
the compatibility `thread.md`.

## Handoff format (version 1)

```json
{
  "protocol": "totalrecalls-browser-handoff",
  "version": 1,
  "provider": "chatgpt",
  "source": {
    "url": "https://chatgpt.com/c/...",
    "provider": "chatgpt"
  },
  "account": {"email": "optional@example.com"},
  "conversation": {
    "id": "provider-conversation-id",
    "title": "A useful title",
    "created_at": "2026-09-02T18:00:00Z",
    "updated_at": "2026-09-02T19:00:00Z",
    "folder": "Home",
    "messages": [
      {"role": "user", "content": "Question"},
      {"role": "assistant", "content": "Answer", "model": "model-name"}
    ]
  }
}
```

`content_md` may be used instead of `content`. `id` is optional; when absent,
the importer derives a stable id from the provider, source URL, title, and
messages. Message roles are preserved, and assistant citations may be supplied
using the standard `citations` array.

The importer is local-only and does not execute content in the handoff. Review
the downloaded JSON before importing it, especially when it contains sensitive
conversation data.

