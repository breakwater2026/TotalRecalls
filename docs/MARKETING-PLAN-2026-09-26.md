# TotalRecalls Marketing Plan

**Date:** 2026-09-26 · **Status:** v1.0.0 launch day · **Trigger:** checkout approval cleared (per your note: Plaid)
**Scope:** one operator, low budget, Windows-only product. Everything below is built from the LIVE site as verified on 2026-09-26 (URLs listed in §14).

---

## 1. Product snapshot (verified on live site, 2026-09-26)

| Fact | Value | Source |
|---|---|---|
| Positioning | "Recall every AI conversation." | Home H1 |
| What it does | Downloads ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, Qwen chats → local Markdown + JSON | Home / About / FAQ |
| Privacy posture | 100% local, no cloud, no telemetry, no account, "verify with Wireshark" claim | Home / About / FAQ |
| Platform | Windows 10/11 portable ZIP (~17.8 MB, SHA-256 published); Mac/Linux "on the way" | Download / FAQ |
| Free tier | 3 providers (Perplexity, ChatGPT, Claude), 5 conversations per download | Download / Pricing |
| Price | **$24 one-time** (launch, discounted), normal **$48 USD**, Paddle checkout, license key by email, in-app activation | Home / Pricing / `js/config.js` (price id `pri_01m37q…`, discount `dsc_01m398…` live) |
| Content assets | 9 provider guides, 9 compare pages, FAQ, press kit, roadmap, release notes, feature requests, demo video (R2: `video.totalrecalls.app`) | Site crawl |
| Refund posture | No standard refunds; free tier as try-before-you-buy; Quebec statutory rights preserved | Pricing / FAQ |

**Marketing-relevant defects found during verification (fix in Phase 0):**
1. **`www.totalrecalls.app` does not resolve** (curl → 000). Apex works. Anyone typing `www.` gets a dead end — a real conversion leak and a credibility problem.
2. **Version-date inconsistency:** About page says v1.0.0 = September 12, 2026; Download page says September 26, 2026. Single source of truth should be `site/src/data/config.json` (per the site skill).
3. **Press kit and roadmap pages are near-empty shells** — pitching press with an empty kit wastes the one shot a new app gets.
4. **No email capture anywhere on the site** — no owned audience mechanism.
5. **No analytics** — nothing measures visitors→downloads→purchases.
6. **No social profiles linked** in the live footer/hero (the site sells a tool, but the plan needs at least one active social home).

---

## 2. Market context (sourced 2026-09-26)

- **ChatGPT:** ~700M weekly active users per OpenAI's own usage study (PCMag, 2025); crossed **1B monthly active users in May 2026 — fastest app ever to that milestone** (Reuters/Sensor Tower, 2026-06-02); on the verge of **1B weekly** by mid-2026 (The Information via TNW, 2026-07-29).
- **Claude:** 56M MAU in Q2 2026, **+640% YoY** (Sensor Tower via Reuters). Users installing the Claude app spent 5% less time on ChatGPT — multi-provider usage is now the norm, not the exception.
- **The pain is structural:** history lives in 8 companies' accounts; Perplexity is documented (on our own site) to delete history after ~30 days; UI revisions orphan threads (the home page's "Live Feed" dramatizes exactly this); Gemini requires Google Takeout; OpenAI's native export is a raw JSON dump.
- **Incumbent/adjacent tools (free):** Chrome extensions (ExportGPT, ChatGPT Exporter), browser-console one-liners (a "TIL" Reddit thread proves demand), ChatKeeper (ChatGPT-only), OpenAI's native export, Google Takeout. **None of them do all 8 providers, full history, as a durable local library.** That gap is the product.
- **Timing tailwind:** data-ownership / "own your data" is a mainstream 2026 theme (portability, lock-in backlash, both OpenAI and Anthropic heading to IPO — the stakes of whose cloud holds your work are now real).

**Implication:** the audience is enormous, the demand is proven (free tools already get traction), and differentiation is clear but must be *stated in every asset*: **8 providers, full history, local files, one-time price.**

---

## 3. Target audience (ICP)

Ranked by purchase likelihood:

1. **Multi-assistant power user (primary buyer).** Uses 2–3 of the 8 providers daily, has months/years of threads (pricing research, code reviews, legal drafts, research trails). Fear: losing work when a tab closes, a UI changes, or a provider purges. Buys the $24 without hesitation. Lives on Reddit (r/ChatGPT, r/claudeAI, r/perplexity_ai) and X.
2. **Researcher / knowledge worker.** Treats chat threads as work product. Wants searchable, greppable, versionable output — the Markdown+JSON library + roadmap (semantic search, RAG) speaks to them.
3. **Local-first / privacy-oriented user.** Overlaps r/selfhosted and r/LocalLLaMA. The "zero upload, no telemetry, no account, verify the traffic yourself" claim is the entire pitch for this segment.
4. **Developer.** Wants their prompt history as data (grep, diff, RAG over your own prompts). The roadmap add-ons are their upgrade path.

**Anti-ICP (don't chase):** single-provider casual users with <10 conversations — the free tier satisfies them; they rarely convert and consume support.

---

## 4. Positioning & message architecture

**Category:** AI data ownership / personal data portability for AI assistants. (Not "a backup tool" — that undersells it.)

**Message pyramid (every asset repeats this order):**

| Layer | Message |
|---|---|
| Hook | **Your AI conversations are disappearing.** Perplexity purges history in ~30 days. UIs change. Tabs close. 9 months of prompts, no backup. |
| Solution | **Recall every AI conversation.** One Windows app pulls all 8 providers into a local folder of Markdown + JSON you keep forever. |
| Differentiator | Not one chat, not one provider: **8 sources → 1 folder.** Full history, real files, zero upload, no account, no subscription. |
| Trust | Free tier first (3 providers / 5 convos). $24 one-time. SHA-256 on every ZIP. No telemetry — verify with Wireshark if you want. |
| CTA | Try the Free Tier → Upgrade to Pro for all 8 providers, unlimited. |

**Proof points (use everywhere available):** the demo video (Claude hero + 7 provider minis), 9 working guides, "you can watch its network traffic yourself," the home-page live feed of real failure modes, SHA-256 checksums, local sign-in only.

**Standing comparisons (always state these when the question is "why not the free extension?"):**
- Free extensions export **one conversation at a time** from **one provider** inside a browser.
- OpenAI's native export is an unstructured JSON dump (see our /compare/chatgpt page).
- TotalRecalls: full history, all 8 providers, one durable library, offline, one-time $24.

**Pricing message:** "$24 once. $48 later. No subscription, no monthly 'AI archive' fee." Decide and publish a **launch-price end date** (see §12 decision D1) — scarcity drives the launch window.

---

## 5. Funnel design

```
Discovery          Evaluation            Trial                Purchase            Retention
─────────          ──────────            ─────                ────────            ──────────
SEO guides    →   Home + demo video  →   Free Tier ZIP     →   Paddle $24     →   Release-notes
Reddit / HN     (compare pages,        (17.8 MB,            one-time,          email list
Press / X       FAQ, press kit)        SHA-256, free tier)   key by email       Roadmap + add-ons
Directories     "Why this matters"     cap: 3 providers /                    Semantic search /
YouTube 90s cut             5 convos → upgrade nudge          Obsidian/Notion sync
                                                                    (paid add-ons)
```

Leak points to protect:
- **Download friction:** SmartScreen warning on first launch (unsigned). The /guides/smartscreen/ page mitigates; **code-signing is the real fix** (Phase 0, D3).
- **Trust gap (new app):** mitigate with the SmartScreen guide, published SHA-256, no-telemetry claim, and the free tier — the cap is the trust gate, not a wall.
- **Free→paid conversion:** the cap (3 providers / 5 convos) must be hit *before* the user feels the value; the in-app upgrade prompt is the moment of maximum leverage.

---

## 6. Phase 0 — Fix the leaks (days 0–14, before/around launch)

| # | Action | Why | Effort |
|---|---|---|---|
| 0.1 | **Fix `www.totalrecalls.app`** (Cloudflare Pages alias + DNS record; verify both apex and www return 200 with `curl`) | Dead end for typed-in traffic + looks broken to journalists | ~30 min |
| 0.2 | **Single version/date source** in `config.json`; About page currently disagrees with Download page (Sep 12 vs Sep 26) | Accuracy is the brand; buyers check dates | ~30 min |
| 0.3 | **Fill the press kit:** fact sheet (positioning, price, providers, stats), 6–8 screenshots, demo video link (R2), founder bio, press contact, download link + SHA | Press pitches with empty kits get ignored | ~2 h |
| 0.4 | **Add email capture** on /release-notes/ and /thanks/ (Cloudflare native form/waitlist — first-party, no third-party SaaS, consistent with the no-telemetry brand) | No owned audience = every campaign starts from zero | ~1 h |
| 0.5 | **Add Cloudflare Web Analytics** (privacy-friendly, first-party) | Can't optimize what you can't measure; brand-safe | ~30 min |
| 0.6 | **Set the launch-price end date** and make it visible (banner on /buy and /pricing): "$24 through <DATE>, then $48" | Scarcity is the single highest-leverage copy element right now | ~30 min + Paddle |
| 0.7 | **Code-signing certificate** (start the order — CA turnaround is the long pole) | Kills the biggest first-run leak (SmartScreen); Windows Store listing also requires it | $150–600/yr + days |
| 0.8 | **Fill the roadmap page** with the real list (Mac/Linux, auto-update, code-signing, semantic search, Obsidian/Notion sync, RAG containers, multi-device memory) | Roadmap = retention + add-on pipeline + press credibility | ~1 h |
| 0.9 | **Create + link one social home** (X is the highest-fit for this audience; GitHub optional for the open-adjacent crowd) | A new app with zero social presence reads as a hobby project | ~1 h |

**Exit criteria:** www resolves; version dates consistent; kit, analytics, email capture, discount deadline live; cert order submitted.

---

## 7. Phase 1 — Launch (week 1–4)

v1.0.0 shipped **today (2026-09-26)** — launch this week.

### 7.1 Community (highest ROI for a utility like this)
| Channel | Play | Notes |
|---|---|---|
| **Hacker News** | **Show HN: TotalRecalls – download every AI chat (8 providers) to local Markdown** on a Monday/Tuesday morning US time. Follow-up in week 2: **Ask HN: Do you back up your AI chat history?** (seeds discussion without self-promo). | HN audience = exactly ICP #2/#4. One shot: make the title carry the 8-providers + local + one-time price. |
| **Reddit** | Value-first posts (no link-dump): (a) r/ChatGPT — "I built a local archive for my ChatGPT history (8 providers, free tier)" with screenshots of the library; (b) r/claudeAI — Claude Projects angle; (c) r/perplexity_ai — **the 30-day purge is the hook** ("your research trail gets deleted — here's how I keep it"); (d) r/selfhosted — local-first/zero-upload angle; (e) r/Windows. | Follow each sub's self-promo rules; answer every comment fast; the Reddit "TIL export" thread proves format works. Expect the r/perplexity_ai post to outperform. |
| **X/Twitter** | Launch thread: problem (feed of lost threads) → 8-sources→1-folder GIF (cut from Claude hero video) → free tier → $24. Then 3×/week: one provider pain-point post + one result screenshot (library view). | Engage AI-tool builders/newsletters directly. |
| **YouTube** | 90–120 s cut of the Claude hero video (no personal conversation displays — the hero take is already PII-safe per the shoot QC). Title: "Download every AI chat to local files (8 providers)". | The hero asset is done and QC'd; this is an edit, not a shoot. |

### 7.2 Press (week 1–2, after kit is full)
Pitch list (order = fit): **PCMag, The Verge, Ars Technica, 9to5Mac (no — skip), The Decoder, TLDR AI, The Rundown AI, Ben's Bites / Superhuman (newsletter placement).**

**Pitch angle (one paragraph, reuse for all):**
> TotalRecalls is a one-time $24 Windows app that downloads your full chat history from all 8 major AI assistants — ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, Qwen — into a local folder of Markdown + JSON. It exists because that history is fragile: Perplexity deletes threads after ~30 days, UI revisions orphan projects, and the official exports (OpenAI's JSON dump, Google Takeout) are incomplete or unusable. Everything runs locally: no cloud, no account, no telemetry — you can verify the traffic yourself. Free tier (3 providers, 5 conversations) available now.

Attach: fact sheet, screenshots, demo video, founder one-liner. Offer the free-tier ZIP to every editor (they will try it — the product demos itself).

**Why press now:** checkout approval means a working purchase flow exists for the first time — the story is complete ("you can buy it today").

### 7.3 Directories & listings (week 1–2, one-hour batch)
- **AlternativeTo** — create TotalRecalls; link against ExportGPT, ChatKeeper, ChatGPT Exporter, Google Takeout. (This is where "vs free extension" questions go.)
- **ToolFinder / Windows app directories.**
- Prepare **Microsoft Store** listing (blocked on code-signing — file it the week the cert lands; it's both a distribution and a trust channel).

### 7.4 Site work (week 1–2, small)
- `/why-this-matters/` gets a stat block (700M WAU ChatGPT, 1B MAU milestone, Perplexity purge) — sourced, dated, linked.
- Add JSON-LD (Product + FAQPage) on home/pricing/FAQ for rich results.
- Add UTM-friendly share links + a "share" affordance on /thanks/ (buyers are the best referral source at $24).

---

## 8. Phase 2 — Engine (months 2–3)

1. **SEO matrix (the compounding asset).** The 9 guides + 9 compare pages already target the long tail: "export ChatGPT conversations", "download Claude history", "backup Perplexity threads", "Gemini Takeout markdown", "download Grok/DeepSeek/Mistral/Qwen chats". Add the missing shapes: "how to back up AI chat history", "X vs Y provider switching", "your AI data ownership 2026". Goal: top-5 on 5+ long-tail keywords by month 3. Check rankings monthly; fix what doesn't move.
2. **Weekly email (release notes → list).** Every release + one "library of the week" style value note. Release-notes email is the natural opt-in: "get release notes" on /release-notes/.
3. **Partnerships (1/week):** AI newsletters (the list above, ongoing), 1–2 YouTubers who cover AI tools (send the 90s cut + free key), podcast clips for the "own your AI data" angle.
4. **Affiliate/ambassador (month 3, once volume exists):** 20% of the $24 for 12 months, or lifetime — cheap at this price, and it recruits the Reddit/developer crowd to evangelize.
5. **Mac/Linux waitlist page:** capture demand (the FAQ promises "on the way"); every waitlist signup is a future buyer + a data point for when to build.
6. **Add-on pipeline (the LTV story):** semantic search → Obsidian/Notion sync → RAG containers, each a separate purchase per the published roadmap. Marketing for v1.0 = "core for $24 forever; these are coming, and owners get them at the best price."

---

## 9. KPIs & instrumentation

Instrument (Phase 0): Cloudflare Web Analytics (visitors, pages), Cloudflare download counter on the R2-hosted ZIP (or Pages request logs), Paddle dashboard (checkout opened / completed / revenue), UTM per channel.

**Targets (assumptions stated, not forecasts):**

| Metric | Month 1 | Month 2 (cum.) | Month 3 (cum.) |
|---|---|---|---|
| Free ZIP downloads | 1,000 | 4,000 | 10,000 |
| Free→paid rate | 1.5–3% | 2–4% | 2–5% |
| Paid units | 15–30 | 80–160 | 250–400 |
| Revenue @ $24 | $360–720 | ~$2k–4k | ~$6k–9.6k |
| Email subscribers | 300 | 1,000 | 2,500 |
| SEO | baseline | 3 keywords top-10 | 5+ keywords top-5 |

Review cadence: weekly numbers while in Phase 1; monthly from Phase 2. Kill any channel with <0.1% download conversion after 500+ visits.

---

## 10. Budget (months 1–3)

| Item | Cost |
|---|---|
| Code-signing certificate | $150–600/yr |
| Cloudflare (analytics, forms, hosting, R2) | $0 (free tier) |
| Directories, press, community | $0 |
| Video (already shot + rendered) | $0 |
| Optional paid test (X or Microsoft Ads) — **only after organic conversion is validated** | $200–500 |
| **Total committed** | **≈ $150–600** |

This is a distribution problem, not a media-buy problem, for a $24 utility with a free tier.

---

## 11. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Provider breaks the download flow** (UI/cookie/API change) | High, recurring | Trust + support load | Fast patch cadence (robust-auth work already in flight), Release Notes as public status, FAQ transparency; market the "we fix it when they break it" as a feature |
| **Provider ToS friction** (web-session access vs official API) | Medium | Legal/reputation | Site already puts ToS responsibility on the user (Terms); Gemini uses the official Takeout path — use that as the trust anchor; never claim "official" in marketing |
| **SmartScreen "new app" friction** | High (until signed) | Conversion leak | Code-signing (Phase 0), annotated SmartScreen guide, SHA-256, "download only from totalrecalls.app" |
| **Windows-only TAM** | Certain | Growth ceiling | Mac/Linux waitlist now; build when the list justifies it |
| **Launch discount expiry surprise** (config.js price vs Paddle catalog drift) | Medium | Buyer distrust | Set explicit end date (D1); the site skill already mandates syncing `config.js` price strings with the catalog |
| **Single merchant of record dependency** (Paddle; checkout approval per your note — see D6) | Low | Checkout outage | Paddle dashboard monitoring; _ptxn fallback already shipped in config.js |
| **Press silence (nothing gets picked up)** | Medium | Slower top-of-funnel | Community + SEO carry the load; press is a multiplier, not the plan |

---

## 12. Decisions needed from you

| # | Decision | Options | Recommended |
|---|---|---|---|
| D1 | Launch-price end date ($24 → $48) | open-ended vs fixed | **Fixed date, ~60–90 days out** — visible scarcity converts; publish it on /buy + /pricing |
| D2 | Show HN + Reddit launch this week? | this week / next | **This week** — v1.0.0 shipped today; checkout now works end-to-end |
| D3 | Code-signing cert budget + CA | $150–600/yr | **Buy it in Phase 0** — CA turnaround is the long pole; also unblocks Microsoft Store |
| D4 | Social home to create + link | X / GitHub / both | **X** (audience fit) + GitHub repo card optional |
| D5 | Affiliate program in month 3? | 20% 12-mo / lifetime key / skip | **20% for 12 months** — cheap, self-liquidating |
| D6 | Checkout note check: you said **Plaid** approved — the live checkout runs on **Paddle** (price id / discount id verified in `js/config.js`). Was "Plaid" a slip for Paddle, or is Plaid a new element? | — | Confirm, so the plan's merchant assumptions are right |
| D7 | Mac/Linux waitlist page — build now? | yes / later | **Yes, week 2** — one page, feeds §8.5 |

---

## 13. 90-day execution summary

| Weeks | Focus |
|---|---|
| **0–2** | Phase 0 fixes (www, dates, kit, analytics, email capture, discount deadline, cert order, roadmap fill, X account) → **Show HN + Reddit launch week 1** → press pitches → directory listings → 90s YouTube cut |
| **3–6** | Community follow-through (Ask HN, second Reddit wave), newsletter placements, first ranking report, Mac waitlist page, first monthly KPI review |
| **7–13** | SEO matrix completion, affiliate launch, partnership cadence 1/week, Microsoft Store filing (post-cert), month-3 review: kill/keep channels, decide Mac build priority from waitlist data |

---

## 14. Sources (verified 2026-09-26)

- Live site crawl: totalrecalls.app home, /pricing, /download, /buy/, /compare/chatgpt, /why-this-matters, /about, /press, /roadmap, /faq, /js/config.js
- Market: Reuters 2026-06-02 (ChatGPT 1B MAU, Claude 56M MAU, Sensor Tower); PCMag (OpenAI usage study, 700M WAU); The Information via TNW 2026-07-29 (1B WAU trajectory)
- Competitive: Chrome Web Store (ExportGPT, ChatGPT Exporter), pionxzh/chatgpt-exporter (GitHub), ChatKeeper (martiansoftware.com), Tactiq guide, spchatgpt.com export tool, r/ChatGPTPromptGenius "TIL export" thread
