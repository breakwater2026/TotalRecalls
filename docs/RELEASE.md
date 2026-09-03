# TotalRecalls — Release checklist (commercialization)

**Version:** 1.3.0 (`all-providers-v1`)  
**Domain:** totalrecalls.app  
**Repo:** https://github.com/breakwater2026/TotalRecalls

## Providers

| Provider | Auth | Notes |
|----------|------|--------|
| Perplexity | Embedded login / session cookie | Full multi-index discovery |
| ChatGPT | Embedded login / Bearer or cookie | backend-api list+fetch |
| Claude | Embedded login / sessionKey | org conversations |
| Gemini | **Google Takeout path** (paste folder/JSON) | Live cookie list deferred (RPC fragility) |
| Grok | Embedded login / Bearer or cookie | Best-effort endpoints; may need refresh if xAI changes APIs |

## Ship steps

1. **Tests**
   ```bash
   python -m unittest discover -s tests -q
   python app.py --selftest
   ```

2. **Website build**
   ```bash
   cd site
   npm ci
   npm run build
   ```

3. **Desktop EXE**
   ```bash
   .venv\Scripts\python.exe tools\build_exe.py --edition free
   ```
   PyInstaller is native: build Windows artifacts on Windows, macOS artifacts
   on macOS, and Linux artifacts on Linux.  See
   [`PLATFORM_SUPPORT.md`](PLATFORM_SUPPORT.md) for state paths, folder
   opening, and platform-specific process commands.

4. **Marketing site**
   - **Primary:** GitHub Pages workflow `.github/workflows/pages.yml` deploys `site/` on push
   - Custom domain: `site/CNAME` = `totalrecalls.app` (point DNS CNAME to `breakwater2026.github.io`)
   - Optional: Cloudflare Pages via `wrangler.toml` if preferred later

5. **Code signing (Windows)**
   - OV/EV cert → sign `TotalRecalls.exe` + installer
   - Required for SmartScreen reputation; SP8 Smart App Control blocks unsigned

6. **Payments**
   - Gumroad / Lemon Squeezy / Paddle one-time ~$19–29
   - Deliver signed installer download; no cloud token collection

## Legal posture (product copy)

- User-driven, on-device export of the user’s own chats  
- Not a hosted scraper; session tokens stay on the PC  
- Official provider data-export links remain the compliance fallback  

## Smoke test matrix

- [ ] Perplexity login + export → `Library/perplexity/`  
- [ ] ChatGPT login/paste + export → `Library/chatgpt/`  
- [ ] Claude login/paste + export → `Library/claude/`  
- [ ] Gemini Takeout path paste + export → `Library/gemini/`  
- [ ] Grok login/paste + export → `Library/grok/`  
- [ ] Provider switch clears prior session  
- [ ] App restart restores last session+provider  
