# TotalRecalls v1.3.0

**Own every AI conversation** — multi-provider local export desktop app.

## What's in 1.3.0

### Providers
| Provider | Auth |
|----------|------|
| **Perplexity** | Embedded login / session cookie |
| **ChatGPT** | Embedded login / Bearer or cookie |
| **Claude** | Embedded login / sessionKey |
| **Gemini** | Google Takeout folder or JSON path |
| **Grok** | Embedded login / Bearer or cookie |

### Product
- React + Vite desktop UI (`ui/`) hosted by Python + WebView2
- Unified export layout: `Library/<provider>/…/conversation.md` + `conversation.json`
- Provider picker; switching providers clears the prior session
- Marketing site scaffold in `site/` (totalrecalls.app)
- 54 unit tests + `--selftest`

### Downloads
- **TotalRecalls-windows-x64.zip** — unsigned Windows onefile EXE  
  SmartScreen may warn until we code-sign.

## Run from source
```bash
python app.py
```

## Notes
- Session tokens stay on your PC — no TotalRecalls cloud login.
- Gemini live cookie sync is deferred; Takeout is the stable path.
- Not affiliated with OpenAI, Perplexity, Anthropic, Google, or xAI.

## Ship checklist remaining
- [ ] Cloudflare Pages deploy for totalrecalls.app
- [ ] Code-signed installer
- [ ] Payment checkout (~$19–29 one-time)

See `docs/RELEASE.md` for the full matrix.
