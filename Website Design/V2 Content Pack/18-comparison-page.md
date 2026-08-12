# 18 — Product Comparison Page (overview + per-provider)

**Source:** Thread "Product Comparison Page" (L2245–2452). Curated final copy. This is the canonical comparison content; the micro-site structure (L2577–2684) defines the per-provider pages.

## Page intro

**H1:** TotalRecalls vs Official AI Exports

AI assistants give you powerful conversations — but their export tools are inconsistent, limited, or incomplete. TotalRecalls provides a single, predictable way to save your chats across all major assistants.

Below is a clear comparison of TotalRecalls vs the official export options from ChatGPT, Claude, Perplexity, Gemini, and Grok.

## Overview Table

| Feature | TotalRecalls | ChatGPT Export | Claude Export | Perplexity Export | Gemini Takeout | Grok Export |
|---|---|---|---|---|---|---|
| Multi-assistant export | ✔ Yes | ✖ No | ✖ No | ✖ No | ✖ No | ✖ No |
| Local Markdown files | ✔ Yes | ✖ No (HTML bundle) | ✔ Partial | ✖ No | ✖ No | ✖ No |
| Local JSON files | ✔ Yes | ✔ Yes | ✔ Yes | ✖ No | ✔ Yes | ✖ No |
| Clean folder structure | ✔ Yes | ✖ No | ✖ No | ✖ No | ✖ No | ✖ No |
| Private, local-only | ✔ Yes | ✖ Cloud export | ✖ Cloud export | ✖ Cloud history | ✔ Local ZIP | ✖ Cloud export |
| Multi-assistant library | ✔ Yes | ✖ No | ✖ No | ✖ No | ✖ No | ✖ No |
| One-time purchase | ✔ Yes | Free | Free | Free | Free | Free |
| Export reliability | ✔ High | Medium | Medium | Low (history expires) | High | Medium |
| Export format usability | ✔ High | Medium | Medium | Low | Medium | Low |

## Per-provider sections (one per page in /compare/)

### TotalRecalls vs ChatGPT

**ChatGPT Official Export:** Produces a single HTML bundle · Hard to browse · No Markdown · No per-conversation files · No multi-assistant support · Requires cloud export · Slow for large histories

**TotalRecalls:** Markdown + JSON per conversation · Clean folder structure · Local-only · Multi-assistant · Fast incremental exports · No cloud dependency

**Verdict:** ChatGPT's export is fine for compliance dumps. TotalRecalls is for a usable personal archive.

### TotalRecalls vs Claude

**Claude Official Export:** Exports Projects · JSON only · No Markdown · No folder structure · No multi-assistant support · Requires cloud access

**TotalRecalls:** Markdown + JSON · Preserves Projects and long threads · Clean folder structure · Local-only · Multi-assistant

**Verdict:** Claude's export is functional but not user-friendly. TotalRecalls makes Claude Projects readable and durable.

### TotalRecalls vs Perplexity

**Perplexity Official Export:** No official bulk export · History expires after ~30 days · Threads are hard to find · No Markdown · No JSON · No local archive

**TotalRecalls:** Full Perplexity thread export · Markdown + JSON · Local folder structure · Permanent archive · Multi-assistant

**Verdict:** Perplexity has no real export. TotalRecalls is the only practical way to save Perplexity research.

### TotalRecalls vs Gemini (Google Takeout)

**Gemini Takeout:** Requires Google Takeout · Produces a large ZIP · JSON only · No Markdown · No folder structure · Manual extraction required · Slow for large accounts

**TotalRecalls:** Reads Takeout automatically · Converts JSON → Markdown · Clean folder structure · Multi-assistant · Local-only

**Verdict:** Takeout is reliable but inconvenient. TotalRecalls turns Gemini dumps into readable conversations.

### TotalRecalls vs Grok

**Grok Official Export:** Limited export options · No Markdown · No JSON · No folder structure · Cloud-only · No multi-assistant support

**TotalRecalls:** Markdown + JSON · Clean folder structure · Local-only · Multi-assistant · Durable archive

**Verdict:** Grok's export is minimal. TotalRecalls provides a complete local archive.

## Why TotalRecalls Wins

1. **Multi-assistant** — One tool for ChatGPT, Claude, Perplexity, Gemini, and Grok.
2. **Local-only** — Your chats stay on your disk — not ours.
3. **Markdown + JSON** — Readable, portable, durable.
4. **Clean folder structure** — Predictable, searchable, easy to back up.
5. **One-time purchase** — ~~$49~~ $24 launch price. No subscription. No monthly "AI archive" fee.
6. **Usable today** — Official exports are built for compliance. TotalRecalls is built for actual use.

## Bottom CTA

Ready to own your AI conversations?
Buy TotalRecalls — $24 launch price
Windows · local files · one-time purchase

## Curation notes

- The comparison micro-site structure (thread L2577–2684) splits this into `/compare/` (overview), `/compare/chatgpt/`, `/compare/claude/`, `/compare/perplexity/`, `/compare/gemini/`, `/compare/grok/`, `/compare/why-local/`, `/compare/why-multi-assistant/`, `/compare/pricing/` — matches implementation plan §4. Use this file's content per page.
- "Local JSON files: Claude ✔ Yes" is per the thread's table — keep as concluded.
- One-time purchase rows: official exports are free — table says "Free" — do not spin as a cost advantage, honesty is the brand.
