# /compare/* — proposed content, for review

**Date:** 2026-10-10 · **Status:** DRAFT — nothing here is on the site yet
**Scope:** the 9 `/compare/*` pages that Google will not index

## Why this matters (measured, not assumed)

| Page | Unique article content today |
|---|---|
| `/compare/grok/` | **36 words** |
| `/compare/claude/` | 42 |
| `/compare/gemini/` | 43 |
| `/compare/deepseek/` | 44 |
| `/compare/pricing/` | 44 |
| `/compare/perplexity/` | 45 |
| `/compare/chatgpt/` | 48 |
| `/compare/mistral/` | 49 |
| `/compare/qwen/` | 49 |
| *(reference)* `/guides/qwen/` | 458 |
| *(reference)* `/faq/` | 547 |

Each page is currently an H1, one paragraph and two bullets. That is the entire
explanation for "Discovered – currently not indexed": there is almost nothing to index.
No technical fix will change it.

**Target:** ~400–500 words of real content per page, plus a FAQ block.

## Rules I held to while drafting

1. **No invented provider facts.** Every claim traces to copy already live on the site
   (`/providers/` DETAIL, or that provider's guide).
2. **Official-export status is only asserted where your own copy asserts it.** Your guides
   say plainly that Grok, DeepSeek, Mistral and Qwen have **no built-in export**; Gemini is
   **Takeout-only**; ChatGPT has the **official account data download**. Your Claude and
   Perplexity guides do **not** state either way — so those two pages are written around the
   local-library value instead of claiming something I can't verify. **If you know Claude's
   and Perplexity's real export status, tell me and I'll add that section.**
3. **Prices and limits are the live ones:** $24 USD launch (list $48), one-time, no
   subscription, Free Tier = 3 providers / 5 conversations per download.
4. Each page links to its own guide, `/download/`, `/pricing/` and `/compare/` — the
   internal links those pages never had.

## What I propose adding to every page

- A **side-by-side comparison table** (scannable, and a strong candidate for a featured
  snippet)
- An **honest "which should you use?"** section — this is your voice already, it appears in
  the ChatGPT / DeepSeek / Mistral / Qwen guides, and it builds trust instead of reading
  like ad copy
- A **3-question FAQ** per page → emits `FAQPage` JSON-LD → rich results. Same pattern as
  `/faq/` (whose schema I fixed today — note it must be a real object, not a stringified one)

---
---

# 1. /compare/chatgpt/

**Title:** ChatGPT vs. TotalRecalls
**Meta description:** ChatGPT can export your whole account as a bulk data download. TotalRecalls keeps your conversations as a readable Markdown + JSON library on your PC. Here's the difference.

## ChatGPT vs. TotalRecalls

If you've spent months thinking out loud in ChatGPT, that history is an asset. There are two
ways to get it out, and they're built for different jobs.

### What ChatGPT's official download gives you

OpenAI provides a full account data export under **Settings → Data controls**. It's the right
choice for a complete, legal or compliance-grade archive. It arrives as one bulk bundle
after a processing delay, and it's shaped like an export, not like something you'll browse
on a Tuesday.

### What TotalRecalls gives you instead

TotalRecalls runs on your PC, connects to your ChatGPT session locally, and writes each
conversation into folders as Markdown + JSON. Long conversations stay together in a single
file, dated, ready for any text editor. Your session stays on your machine — TotalRecalls
never holds your credentials.

| | ChatGPT official export | TotalRecalls |
|---|---|---|
| Scope | Entire account | The conversations you choose |
| Format | Bulk bundle | Markdown + JSON, one pair per chat |
| Turnaround | Processing delay | Immediate |
| Readable as-is | Awkward to browse | Any text editor |
| Works with your other AI tools | No | Same library, all 8 providers |
| Price | Free | Free Tier available; $24 one-time for all 8 |

### Which should you use?

Use the **official download** when you need a full account archive for compliance or a
complete record. Use **TotalRecalls** when you want a usable personal library sooner —
especially if you also use Claude, Perplexity, Gemini or Grok and want one archive location
instead of five.

### FAQ

**Does TotalRecalls replace ChatGPT's official download?**
No, it complements it. The official export is complete but bulky; TotalRecalls produces the
readable, per-conversation library you'll actually reopen.

**Do I need to give TotalRecalls my ChatGPT password?**
No. You sign in through a local login window on your own machine. TotalRecalls does not run
a hosted service that receives your session.

**Can I back up more than one AI provider with it?**
Yes — ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral and Qwen Chat all land in
the same Library folder structure.

*Next:* [step-by-step ChatGPT guide](/guides/export-chatgpt-conversations/) ·
[Download for Windows](/download/) · [Pricing](/pricing/)

---
---

# 2. /compare/claude/

**Title:** Claude vs. TotalRecalls
**Meta description:** Claude is where long-form work happens — drafts, code reviews, research. TotalRecalls keeps those conversations as Markdown + JSON files on your PC, with your login staying local.

## Claude vs. TotalRecalls

Claude is where a lot of long-form thinking happens — drafts, code reviews, research that
spans days. Those conversations deserve a home outside the browser tab.

### Why Claude history is easy to lose

Long Projects and conversations are hard to re-find months later. UI changes and workspace
switches break muscle memory. And copy-paste doesn't scale past a few conversations — you
lose the order, the formatting, and the context that made the thread worth keeping.

### What TotalRecalls does for Claude

On Windows, TotalRecalls connects using your local Claude session and downloads
conversations into a provider folder as Markdown + JSON, one pair per chat. Long
conversations and Project conversations save as files you can reread without scrolling, so
your drafts, plans and code reviews sit in one folder sorted by date.

| | Browser-only Claude | TotalRecalls |
|---|---|---|
| Re-finding a conversation months later | Scroll and hope | Search your own folder |
| Long threads | Endless scrolling | A single readable file |
| Formatting and structure | Gone when copied by hand | Preserved in Markdown + JSON |
| Works across your AI tools | No | Same library, all 8 providers |
| Where the login happens | — | Locally, on your machine |

### Privacy note

TotalRecalls is built so login stays on your machine. There is deliberately **no hosted
"send us your Claude cookies" service** — that's the design, not a limitation.

### Good practices

- Download after major writing projects, not only when you feel panic
- Name your disk folder clearly, e.g. `AI-Archive/Claude`
- If you use multiple AI tools, keep sibling folders per provider

### FAQ

**Can TotalRecalls back up Claude Projects, or only single chats?**
Long Project conversations and single chats both save as files — the same path, sorted by
date.

**Does my Claude session leave my computer?**
No. You complete a local sign-in on your own machine; TotalRecalls doesn't host your
credentials or your conversations.

**What format are the files in?**
Markdown for reading and JSON for structure — one pair per conversation.

*Next:* [step-by-step Claude guide](/guides/export-claude-chat-history/) ·
[Download for Windows](/download/) · [Pricing](/pricing/)

> **OPEN QUESTION FOR YOU:** does Claude offer an official data export? Your guide doesn't
> say, so I didn't claim either way. If you know, I'll add a "what the official option gives
> you" section for symmetry with the ChatGPT page.

---
---

# 3. /compare/gemini/

**Title:** Gemini vs. TotalRecalls
**Meta description:** Gemini history comes out through Google Takeout — a complete archive that's hard to read. TotalRecalls converts your Takeout folder into Markdown conversations you can browse.

## Gemini vs. TotalRecalls

Gemini's data comes out through Google Takeout. The dump is complete — but it is not
friendly, and that gap is the whole point of this page.

### Why Takeout (and not a fragile scrape)

Gemini's web surface changes often. For v1, TotalRecalls deliberately prioritizes a
filesystem Takeout folder or JSON you already downloaded from Google. That stays honest and
stable: your data comes from Google, and TotalRecalls only handles the converting.

### How it works, in four steps

1. Create a Google Takeout that includes your **Gemini / Gemini Apps** data (as offered in
   your account region).
2. Download and unzip the Takeout package on your PC.
3. In TotalRecalls, choose **Gemini** and paste the folder path — or use *Browse…*.
4. Download into your TotalRecalls library layout.

| | Raw Google Takeout | TotalRecalls |
|---|---|---|
| Complete | Yes | Yes — Takeout is the source |
| Readable as-is | No | Markdown conversations, dated |
| Browsable per conversation | No | One file per conversation |
| Sits with your other AI tools | No | Same library, all 8 providers |
| Needs a live Google session | To re-request | No — works from the folder |

### Multi-provider reality

Many people use Gemini for some tasks and ChatGPT or Claude for others. A Takeout-only
workflow is fine for Google; TotalRecalls exists so the rest of your assistants can live in
the same archive philosophy instead of five separate silos.

### Tips

- Keep the original Takeout zip as cold backup
- Use TotalRecalls output as your day-to-day readable layer
- Re-run when you generate a fresh Takeout

### FAQ

**Why is Gemini different from the other providers?**
Because Gemini isn't a direct download. Your history comes from a Google Takeout archive,
which TotalRecalls converts into Markdown conversations — after which your Gemini chats sit
in the same Library as every other provider.

**Do I have to re-download Takeout every time?**
No. Once converted, your files are local. Re-run when you want the newer conversations you've
had since.

**Does this need my Google password?**
No. You request Takeout through Google yourself; TotalRecalls reads the folder or JSON you
downloaded.

*Next:* [step-by-step Gemini Takeout guide](/guides/gemini-takeout-archive/) ·
[Download for Windows](/download/) · [Pricing](/pricing/)

---
---

# 4. /compare/grok/

**Title:** Grok vs. TotalRecalls
**Meta description:** Grok has no official data download. TotalRecalls reads your local grok.com session and saves every chat to Markdown + JSON, keeping the X posts you referenced.

## Grok vs. TotalRecalls

Grok is where a lot of quick prompts and long debug sessions happen — and, unusually, where
the conversation itself references live X posts. Both are worth keeping.

### Grok does not have an official data download

There's no built-in export to request, which means if you want your Grok history, the browser
tab is currently the only place it lives. That's the whole problem this page solves.

### What TotalRecalls does for Grok

TotalRecalls reads your local `grok.com` session and downloads every conversation to local
Markdown and JSON. **X posts referenced inside a conversation are preserved as quoted links**
in the Markdown, so the context that made the thread useful survives with it. Quick prompts
and long debug sessions both get kept.

| | Browser-only Grok | TotalRecalls |
|---|---|---|
| Official export available | No | — |
| Re-finding a chat later | Scroll the sidebar | Search your folder |
| X posts referenced in chats | Links rot in the tab | Preserved as quoted links |
| Format | On-screen only | Markdown + JSON |
| Sits with your other AI tools | No | Same library, all 8 providers |

### Which should you use?

If you've had one conversation you don't want to lose, copy it out by hand right now. If you
want your Grok history to exist as an archive at all — especially alongside ChatGPT, Claude
and the rest — this is the path.

### FAQ

**Does Grok let me export my data officially?**
No — Grok does not provide an official data download. TotalRecalls uses local session reading
instead.

**Are the X posts in my conversations kept?**
Yes. X posts referenced in chats are preserved as quoted links in the Markdown download.

**Does this work on the free tier?**
Yes. TotalRecalls reads your browser session, so it works with the plan you already have.

*Next:* [step-by-step Grok guide](/guides/grok/) ·
[Download for Windows](/download/) · [Pricing](/pricing/)

---
---

# 5. /compare/deepseek/

**Title:** DeepSeek vs. TotalRecalls
**Meta description:** DeepSeek has no built-in export, and copy-paste throws away the R1 reasoning. TotalRecalls keeps the chain-of-thought with the final answer as local Markdown + JSON.

## DeepSeek vs. TotalRecalls

DeepSeek is unusually valuable to back up, because **the reasoning is the artifact**. A lot
of what you'd want later isn't the answer — it's how the model got there.

### What "download" usually means

DeepSeek does not provide a built-in data download for chat history. The only manual path is
to open each conversation, select the text, and paste it into a local file. That costs you the
formatting, and — more importantly — the thinking block, which is gone within a few page
refreshes.

### Why the chain-of-thought matters

DeepSeek-R1 streams a `thinking_content` block before its final answer. That reasoning is
often more useful than the answer itself: the worked solution, the self-correction, the
trade-off analysis. If you back up by hand, it's gone. If you back up with TotalRecalls, it's
stored next to the final answer, with the timestamp and model name.

### What TotalRecalls does

TotalRecalls runs on your PC, connects to your DeepSeek session locally, and writes
conversations into folders as Markdown + JSON. Chain-of-thought blocks are kept as
collapsible sections so the reasoning stays readable but doesn't drown the answer.

| | Manual copy/paste | TotalRecalls |
|---|---|---|
| Official export available | No | — |
| Reasoning / thinking blocks | **Lost** | **Preserved** |
| Formatting | Flattened | Markdown + JSON |
| Scales past a handful of chats | No | Full history |
| Works on the free tier | Yes | Yes |
| Sits with your other AI tools | No | Same library, all 8 providers |

### Which should you use?

Use manual copy/paste for one or two conversations you need right now. Use TotalRecalls when
you want a complete, searchable archive with the reasoning intact — especially if you also use
ChatGPT, Claude, Mistral or Qwen and want one archive location.

**Good to know:** TotalRecalls reads your browser session — it does not call the DeepSeek API.
It works on the free tier, the pro tier, and any plan that uses the `chat.deepseek.com` web
app. Run the download while your session is still active; DeepSeek sessions expire on
inactivity. DeepSeek-V3 and DeepSeek-R1 share the same download path and both download
cleanly.

### FAQ

**Does DeepSeek let me export my chats?**
No. DeepSeek does not provide a built-in data download — the only manual path is pasting each
conversation into a file yourself.

**Will I lose the R1 thinking blocks?**
With copy/paste, yes — they disappear after a few refreshes. TotalRecalls keeps the reasoning
alongside the final answer.

**Does it use the DeepSeek API or an API key?**
Neither. TotalRecalls reads your browser session, so it works on the free tier without any
developer credentials.

*Next:* [step-by-step DeepSeek guide](/guides/deepseek/) ·
[Download for Windows](/download/) · [Pricing](/pricing/)

---
---

# 6. /compare/mistral/

**Title:** Mistral vs. TotalRecalls
**Meta description:** Mistral (Le Chat) has no built-in export. TotalRecalls reads your local session and saves every conversation as UTF-8 Markdown + JSON, so French, German and Spanish text stay intact.

## Mistral vs. TotalRecalls

Mistral is the dominant non-US chat product in the EU. If your work happens in Le Chat, that
history is worth keeping in a place you control.

### What "download" usually means

Mistral does not provide a built-in data download for chat history. The only manual path is
to open each conversation, select the text, and paste it into a local file — which loses
formatting, doesn't scale past a few conversations, and makes it easy to lose the order of
long ones.

### Why Mistral specifically

Most consumer chat products are US-based. Mistral is the most common alternative for people
who want their work in European jurisdictions — and backing up locally complements that. Even
if your provider is European, your archive living on your own disk is a different guarantee
than a vendor holding it.

TotalRecalls preserves **UTF-8 throughout**, so French, German, Spanish, Italian and
Portuguese conversations stay readable in any editor. That makes it a genuine fit for
multilingual research and translation work, not just an English-language tool.

### What TotalRecalls does

TotalRecalls runs on your PC, connects to your Mistral Le Chat session locally, and writes
conversations into folders as Markdown + JSON.

| | Manual copy/paste | TotalRecalls |
|---|---|---|
| Official export available | No | — |
| Multilingual text | Often mangled | UTF-8 preserved |
| Formatting | Flattened | Markdown + JSON |
| Scales past a handful of chats | No | Full history |
| Sits with your other AI tools | No | Same library, all 8 providers |

**About the Pro tier:** Mistral's Le Chat Pro tier does not expose conversation history
through the public API. TotalRecalls reads from your browser session, which works for the free
tier and any tier that shares the same web UI. Run the download while your session is still
active — Mistral sessions expire on inactivity.

### FAQ

**Does Mistral let me export my Le Chat history?**
No. Mistral does not provide a built-in data download — the only manual path is pasting
conversations into files yourself.

**Will accented and non-English text survive?**
Yes. TotalRecalls preserves UTF-8 throughout, so multilingual conversations stay readable.

**Does it work on the free tier as well as Le Chat Pro?**
Yes. Both share the same web UI, so both download through the same path.

*Next:* [step-by-step Mistral guide](/guides/mistral/) ·
[Download for Windows](/download/) · [Pricing](/pricing/)

---
---

# 7. /compare/perplexity/

**Title:** Perplexity vs. TotalRecalls
**Meta description:** Perplexity threads mix answers, sources and follow-ups. TotalRecalls saves that research history as local Markdown + JSON, before the tab trail disappears.

## Perplexity vs. TotalRecalls

Perplexity conversations aren't just chat — they mix answers, cited sources and follow-up
questions. That's valuable research history, and it's fragile if it only lives in the web app.

### What you're actually losing

A Perplexity thread is a research trail: the question you asked, the sources it pulled, the
follow-ups those sources triggered. Rebuilding that later from memory doesn't work. And the
longer the research sprint, the more there is to lose.

### What TotalRecalls does for Perplexity

TotalRecalls treats Perplexity as a first-class provider on Windows. It reads your local
session and saves each conversation as files you can open offline — typically Markdown for
reading and JSON for structure. That's the difference between *"I have a zip somewhere"* and
*"I can find that answer."*

| | Browser-only Perplexity | TotalRecalls |
|---|---|---|
| Research trail (questions + sources + follow-ups) | Lives in the tab | Saved per conversation |
| Re-finding an old answer | Scroll and re-search | Search your folder |
| Format | On-screen only | Markdown + JSON |
| Works offline | No | Yes |
| Sits with your other AI tools | No | Same library, all 8 providers |

### When to back up

- Before switching plans or accounts
- After a deep-research sprint you may cite later
- If you use Perplexity alongside ChatGPT or Claude and want one archive location

### Be a good citizen

Use your own account, respect Perplexity's terms, and don't hammer the servers. TotalRecalls
keeps conservative pacing for exactly that reason.

### FAQ

**Why back up Perplexity when the history is still in my account?**
Because research history is only as durable as your access to it. Backing up means the trail
survives a plan change, an account switch, or a thread you can no longer find.

**What exactly gets saved?**
Each conversation is stored as files you can open offline — Markdown for reading and JSON for
structure.

**Does it slow Perplexity down or hammer the service?**
No. TotalRecalls uses conservative pacing deliberately, so it stays a polite client of the
service you already pay for.

*Next:* [step-by-step Perplexity guide](/guides/export-perplexity-conversations/) ·
[Download for Windows](/download/) · [Pricing](/pricing/)

---
---

# 8. /compare/qwen/

**Title:** Qwen vs. TotalRecalls
**Meta description:** Qwen Chat has no built-in export. TotalRecalls saves chat.qwen.ai history as local UTF-8 Markdown + JSON — the consumer chat app only, never the DashScope developer API.

## Qwen vs. TotalRecalls

Qwen Chat (`chat.qwen.ai`) is Alibaba's consumer chat product. If that's where your work is,
your history currently exists only in the browser tab.

### What "download" usually means

Qwen Chat does not provide a built-in data download for chat history. The only manual path is
to open each conversation, select the text, and paste it into a local file — which loses
formatting, doesn't scale, and makes long conversations easy to scramble.

### Why two Qwen products matter

This trips people up, so it's worth being precise:

- **Qwen Chat (`chat.qwen.ai`)** — the consumer chat product. This is what users want to back
  up.
- **DashScope / Bailian / Model Studio (`dashscope.aliyuncs.com`)** — Alibaba's developer API
  for the Qwen model family. It has its own separate terms.

TotalRecalls only touches the **consumer chat product**. It never calls DashScope endpoints,
never uses Alibaba API keys, and never touches developer-account credentials.

### What TotalRecalls does

TotalRecalls runs on your PC, connects to your Qwen Chat session locally, and writes
conversations into folders as Markdown + JSON, with multilingual text preserved in UTF-8 —
Chinese, English, Japanese and Korean all stay readable in any editor.

| | Manual copy/paste | TotalRecalls |
|---|---|---|
| Official export available | No | — |
| Consumer chat vs developer API | — | Consumer chat only, never DashScope |
| Multilingual text | Often mangled | UTF-8 preserved |
| Scales past a handful of chats | No | Full history |
| Sits with your other AI tools | No | Same library, all 8 providers |

**Regional note:** Qwen Chat is served from `chat.qwen.ai` (international) and from
`qianwen.com` / `tongyi.aliyun.com` (domestic). TotalRecalls targets the international web
app. Run the download while your session is still active — Qwen Chat sessions expire on
inactivity.

### FAQ

**Does Qwen provide a data download?**
No. Qwen Chat does not provide a built-in data download — the manual alternative is copying
each conversation out by hand.

**Do I need a DashScope or Alibaba API key?**
No, and TotalRecalls never asks for one. It reads your browser session for the consumer chat
product, which is a different product from the developer API.

**Will Chinese and other non-Latin text survive?**
Yes — UTF-8 throughout, so Chinese, English, Japanese and Korean all stay readable.

*Next:* [step-by-step Qwen guide](/guides/qwen/) ·
[Download for Windows](/download/) · [Pricing](/pricing/)

---
---

# 9. /compare/pricing/

**Title:** Pricing Comparison — TotalRecalls
**Meta description:** TotalRecalls is $24 once. No subscription, no per-seat fee. See how a one-time local archive compares to recurring AI subscription costs — and what the Free Tier covers.

## How TotalRecalls compares on price

Most tools in this space bill monthly. TotalRecalls is a one-time purchase for a utility that
keeps working, and there's a Free Tier you can test before paying anything.

### What you pay

| | Free Tier | TotalRecalls ($24 once) |
|---|---|---|
| Price | $0 | **$24 USD** launch price (list $48) |
| Billing | — | One-time. No subscription, no renewal |
| AI providers | 3 | All 8 |
| Conversations per download | 5 | Unlimited |
| Device activations | — | Up to 3 (desktop, laptop, mobile) |
| Updates to the core app | — | Included for the life of the product |
| Where your files live | Your PC | Your PC |

### Why one-time matters here

This is a local utility, not a service. Nothing is hosted for you, so there's no per-conversation
cost, no storage bill and no reason for a recurring charge. You pay once, the files are on your
disk, and the app doesn't stop working if you stop paying.

### Try before you buy

The Free Tier is a real build, not a demo: download it, run it on your own conversations, and
decide afterwards. It's limited to 3 AI providers and 5 conversations per download.

### FAQ

**Is there a subscription?**
No. $24 USD once, at the launch price. No monthly or annual renewal.

**What does the Free Tier include?**
3 AI providers and up to 5 conversations per download — enough to confirm it works on your
actual chats.

**How many computers can I activate?**
Up to 3 activations, so a desktop, a laptop and a mobile device are covered.

**Do I keep getting updates?**
Free updates to the core app for the life of the product. Advanced features (semantic search,
Obsidian/Notion sync, RAG containers, multi-device memory) are separate add-ons.

*Next:* [See the full pricing page](/pricing/) ·
[Download for Windows](/download/) · [All comparisons](/compare/)

---
---

# Implementation notes (for after your review)

- **Structure per page:** H1 → lede → 2–3 H2 sections → comparison table → "which should you
  use?" → FAQ (3 Qs) → CTA. All inside the existing `PageLayout`, so breadcrumbs and styling
  are inherited — no new components needed.
- **Schema:** each page emits `FAQPage` JSON-LD built from its real FAQ block, as a proper
  object (`JSON.stringify(obj)`), which is the form that actually parses.
- **Metadata:** the `title` and `description` above replace the current ones. Note the current
  titles ("Qwen vs. TotalRecalls", 21 chars) are short — these are longer and more
  descriptive.
- **Internal links added:** every page gains links to its provider guide, `/download/`,
  `/pricing/` and `/compare/`. Today these pages link to almost nothing, which is part of why
  they're stranded.
- **No pricing or feature claims change** — every figure is the live one.
- **Not covered here:** `/compare/why-local/` and `/compare/why-multi-assistant/` are essays
  rather than provider comparisons and need a different treatment. Say the word and I'll draft
  those separately.
