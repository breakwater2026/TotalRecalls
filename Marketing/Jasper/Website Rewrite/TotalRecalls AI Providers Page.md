# TotalRecalls AI Providers Page

**Page URL:** `/providers/` (confirm against the current route for the Current AI Models & Providers page)\
**Page goal:** Show exactly which AI providers TotalRecalls supports and what it saves from each. Then send visitors to a free download or to the pricing page.\
**Primary keyword:** download AI chat history\
**Secondary terms:** supported AI providers, save ChatGPT conversations, Claude chat backup, Gemini Takeout to Markdown, DeepSeek chat download, Markdown and JSON

**Meta title:** Supported AI Providers: Download Your AI Chat History | TotalRecalls\
**Meta description:** TotalRecalls saves chats from ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen as Markdown and JSON files on your Windows PC. See what each provider saves.

---

## Page Copy

### 1. Hero

`SUPPORTED PROVIDERS · V1.0.0`

# Download your AI chat history from eight providers.

TotalRecalls saves your conversations from ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen into one folder on your Windows PC. Each chat becomes a Markdown file and a JSON file you can open, search, and keep.

Seven providers download directly. Gemini comes through Google Takeout, which TotalRecalls converts for you.

- **Primary CTA:** Download free
- **Tertiary CTA:** Find your provider ↓

`8 PROVIDERS` · `7 DIRECT · 1 TAKEOUT` · `.MD + .JSON` · `WINDOWS 10/11`

---

### 2. Provider Index

*Anchor: `id="index"`*

`AT A GLANCE`

## Every supported AI provider, in one list

Find your provider, see how its chats reach your Library, and check which tier includes it.

| Provider   | ID        | Method                    | Saved as        | Tier         |
| ---------- | --------- | ------------------------- | --------------- | ------------ |
| ChatGPT    | `OAI-001` | Direct download           | `.MD` + `.JSON` | Free and Pro |
| Claude     | `ANT-002` | Direct download           | `.MD` + `.JSON` | Free and Pro |
| Perplexity | `PPL-003` | Direct download           | `.MD` + `.JSON` | Free and Pro |
| Gemini     | `GEM-004` | Google Takeout → Markdown | `.MD` + `.JSON` | Pro          |
| Grok       | `GRK-005` | Direct download           | `.MD` + `.JSON` | Pro          |
| DeepSeek   | `DSK-006` | Direct download           | `.MD` + `.JSON` | Pro          |
| Mistral    | `MST-007` | Direct download           | `.MD` + `.JSON` | Pro          |
| Qwen       | `QWN-008` | Direct download           | `.MD` + `.JSON` | Pro          |

Every row lands in the same place: `C:\TotalRecalls\Library\`, with one subfolder per provider.

---

### 3. Two Ways In

`HOW CHATS REACH YOUR LIBRARY`

## Direct download or Google Takeout: what's the difference?

Most providers take a pick and a click. One takes a short detour through Google.

**Direct download · 7 providers**\
You sign in to the provider locally, inside the app. Pick it, click download, and your chats land in your Library folder. TotalRecalls handles the rest.\
`DIRECT · LOCAL SIGN-IN`

**Google Takeout · Gemini only**\
Google doesn't offer a direct route for Gemini history. You request a Takeout archive from Google, extract the ZIP, and point TotalRecalls to the folder. It converts your chats to Markdown and saves them next to everything else.\
`TAKEOUT → MD · A FEW EXTRA STEPS`

Both paths end the same way: plain files on your own drive, not sent to our servers.

---

### 4. Provider by Provider

*Anchor: `id="providers"`*

`WHAT GETS SAVED`

## What TotalRecalls saves from each provider

Every conversation becomes one Markdown file for reading and one JSON file for structure. Here's what that looks like for each provider.

#### ChatGPT

`OAI-001` · `DIRECT` · `FREE + PRO`

Your ChatGPT conversations save as dated, readable files instead of one hard-to-browse export bundle. Long threads stay together in a single file, ready for any text editor.

`Library\chatgpt\` · [ChatGPT guide →](/guides/export-chatgpt-conversations/)

#### Claude

`ANT-002` · `DIRECT` · `FREE + PRO`

Long Claude threads and Project conversations save as files you can reread without scrolling. Your drafts, plans, and code reviews sit in one folder, sorted by date.

`Library\claude\` · [Claude guide →](/guides/export-claude-chat-history/)

#### Perplexity

`PPL-003` · `DIRECT` · `FREE + PRO`

Perplexity research threads save before the tab trail disappears. Each thread keeps your questions and answers together, so you can pick up the research where you left off.

`Library\perplexity\` · [Perplexity guide →](/guides/backup-perplexity-threads/)

#### Gemini

`GEM-004` · `TAKEOUT → MD` · `PRO`

**Gemini isn't a direct download.** Your history comes from a Google Takeout archive, which TotalRecalls converts into Markdown conversations. Once converted, your Gemini chats sit in the same Library as every other provider.

`Library\gemini\` · [Gemini Takeout guide →](/guides/gemini-takeout-archive/)

#### Grok

`GRK-005` · `DIRECT` · `PRO`

Grok chats from xAI save as local Markdown and JSON, including references to X posts that appear in your conversations. Quick prompts and long debug sessions both get kept.

`Library\grok\` · [Grok guide →](/guides/grok/)

#### DeepSeek

`DSK-006` · `DIRECT` · `PRO`

DeepSeek conversations save with R1 thinking traces included, so you keep the reasoning, not just the final answer. Useful when you want to see how a result was reached.

`Library\deepseek\` · [DeepSeek guide →](/guides/deepseek/)

#### Mistral

`MST-007` · `DIRECT` · `PRO`

Le Chat conversations save with UTF-8 fidelity, so accents and non-English text come through intact. That makes it a good fit for multilingual research and translation work.

`Library\mistral\` · [Mistral guide →](/guides/mistral/)

#### Qwen

`QWN-008` · `DIRECT` · `PRO`

Your Qwen Chat history from chat.qwen.ai saves as local files, with multilingual text preserved. TotalRecalls works with the consumer chat app, never the DashScope developer API.

`Library\qwen\` · [Qwen guide →](/guides/qwen/)

---

### 5. In Development

`WHAT'S NEXT`

## More providers in development

We're building support for more AI providers and new capabilities. We'll list them here when they're ready, not before.

New providers arrive through app updates. Pro includes free updates to the core app for the life of the product.

`+ MORE PROVIDERS IN DEVELOPMENT`

---

### 6. FAQ

`FAQ`

## Questions about providers and models

**Does it matter which AI model I chatted with?**\
No. TotalRecalls saves conversations from your chat history in each provider, whichever model you used in them.

**Does TotalRecalls use my API keys?**\
No. It saves the chats in your consumer account, the same ones you see in each provider's app. You sign in locally, inside TotalRecalls.

**Why does Gemini take extra steps?**\
Google makes Gemini history available through Takeout rather than a direct route. TotalRecalls converts that archive for you, so the result matches every other provider.

**What happens if a provider changes its interface?**\
Your saved files don't change. They're plain Markdown and JSON on your drive. If a provider change affects new downloads, we fix it in an app update.

**Can I request a provider?**\
Yes. Email <support@totalrecalls.app> and tell us which one you use.

---

### 7. Access Summary and Final CTA

*Anchor: `id="access"`*

`FREE AND PRO`

## Start with three providers. Unlock all eight with one payment.

|                                 | Free Tier                   | Pro                         |
| ------------------------------- | --------------------------- | --------------------------- |
| **Providers**                   | ChatGPT, Claude, Perplexity | All 8                       |
| **Conversations**               | 5 per provider              | Unlimited                   |
| **Gemini (Takeout → Markdown)** | —                           | ✓                           |
| **Price**                       | $0                          | $24 one-time (launch price) |

Try TotalRecalls on your own ChatGPT, Claude, and Perplexity chats first. When you want every provider and no download cap, Pro is one payment with no subscription.

- **Primary CTA:** Download free
- **Tertiary CTA:** Compare Free and Pro →

Windows 10 and 11. Visiting on mobile? Open totalrecalls.app on your desktop to download.

**Visible word count:** About 960 words, including chips, tables, and CTAs

---

## Layout

1. **Hero:** Left-aligned eyebrow, H1, intro, and Gemini line, capped at 680px. CTA pair and chip row below.
2. **Provider index:** One full-width Graphite panel holding the table. The Gemini row uses a dashed left border and a `TAKEOUT → MD` chip, so the difference shows at a glance. On mobile, the table collapses to Provider, ID, and Tier, with Method shown as a chip under each name.
3. **Two ways in:** Two equal cards side by side on desktop, stacked on mobile. The Direct card has a solid Slate border. The Takeout card has a dashed Slate border. The closing line spans the full width below.
4. **Provider by provider:** A 2-column grid of eight Graphite cards on desktop, one column on mobile. The order matches the index. Each card holds its name, chip row, description, and a footer with the folder path and guide link.
5. **In development:** A single Obsidian card with a dashed Slate border and a "+" mark, matching the live site's "more features to come" tile. No names, no dates.
6. **FAQ:** Accordion, collapsed by default.
7. **Access summary and final CTA:** Graphite band with the heading, compact table, line, CTA pair, and microcopy.

---

## Implementation Spec

| Element         | Copy                                                | Style                                                                                                                                                                                                             |
| --------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Page background | —                                                   | Obsidian `#111315`. Hero padding 128px desktop / 64px mobile. Sections 96px desktop / 64px mobile.                                                                                                                |
| Eyebrows        | SUPPORTED PROVIDERS · V1.0.0, etc.                  | IBM Plex Mono Medium 12px, uppercase, +0.12em tracking, Steel Blue `#7A8FA6`                                                                                                                                      |
| H1              | Download your AI chat history from eight providers. | Inter Bold 48px / 34px, 1.1 line height, −0.02em, Paper `#F3EFE7`                                                                                                                                                 |
| H2              | Section headings                                    | Inter Semibold 36px / 28px, 1.15 line height, Paper                                                                                                                                                               |
| H4              | Provider names, FAQ questions                       | Inter Semibold 18px, Paper                                                                                                                                                                                        |
| Intros          | Hero and section intros                             | Inter Regular 20px / 18px, 1.55 line height, Mist `#D9D4CB`, max 680px                                                                                                                                            |
| Body            | Descriptions, answers                               | Inter Regular 16px, 1.6 line height, Mist                                                                                                                                                                         |
| Hero chips      | 4 chips                                             | `mono-sm`: IBM Plex Mono Medium 12px, uppercase, Dust `#B5AEA3` on Slate `#2A2F36`, 6px radius, 4px × 8px padding                                                                                                 |
| Primary CTA     | Download free                                       | Large, 48px, Archive Amber `#C88A2B` fill, Obsidian text, 8px radius, links to `/download/`. One per section.                                                                                                     |
| Tertiary CTAs   | Find your provider ↓ / Compare Free and Pro →       | Inter Semibold 15px, Steel Blue, no border. Links to `#providers` and `/pricing/`.                                                                                                                                |
| Index panel     | —                                                   | Graphite `#1A1D21`, 1px Slate border, 12px radius, 24px padding                                                                                                                                                   |
| Index rows      | —                                                   | `body-sm` 14px, Mist, 1px Slate dividers, 48px rows. IDs in IBM Plex Mono 12px, Steel Blue. Provider names in Inter Medium 14px, Paper.                                                                           |
| Gemini row      | —                                                   | 2px dashed Steel Blue left border. Method cell in `mono-sm`, Dust.                                                                                                                                                |
| Path cards      | Direct / Takeout                                    | Graphite, 12px radius, 24px padding, no hover. Direct: 1px solid Slate. Takeout: 1px dashed Slate (4px dash, 4px gap).                                                                                            |
| Provider cards  | 8 cards                                             | Graphite fill, 1px Slate border, 12px radius, 24px padding, equal heights, no shadow, no hover                                                                                                                    |
| Provider chips  | ID · method · tier                                  | `mono-sm`. ID in Steel Blue on Slate. `DIRECT` in Steel Blue, transparent fill, 1px Slate border. `TAKEOUT → MD` in Dust, 1px dashed Slate border. `FREE + PRO` in Mist on Slate. `PRO` in Archive Amber on Amber |
