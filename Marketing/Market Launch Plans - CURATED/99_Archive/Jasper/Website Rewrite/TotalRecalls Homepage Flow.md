# TotalRecalls Homepage Flow

> **MASTER REFERENCE FOR IMPLEMENTATION**\
> This document is the single source of truth for the TotalRecalls homepage. It puts every rewritten section in final order, with approved copy, CTAs, brand styling, and handoff notes. If an earlier section draft conflicts with this document, **this document wins.**

**Version:** 1.0 · September 2026\
**Page:** `totalrecalls.app/` (homepage)\
**Visual identity:** Private Archive + Calm Utility\
**Primary CTA across the page:** Download free\
**Primary keyword:** save AI chats locally\
**Secondary terms:** AI chat history, download ChatGPT conversations, Markdown and JSON, own your AI chats

---

## Page at a Glance

| # | Section               | Anchor        | Background                   | Job on the Page                                  | Amber Element                |
| - | --------------------- | ------------- | ---------------------------- | ------------------------------------------------ | ---------------------------- |
| 1 | Hero                  | `#top`        | Obsidian                     | State the promise and offer the first step       | Download free                |
| 2 | Why This Matters      | `#why`        | Obsidian, 1px Slate top rule | Name the problem calmly                          | None                         |
| 3 | How It Works          | `#resolution` | Graphite band                | Show the four-step flow and the provider diagram | Download free                |
| 4 | Why Own Your AI Chats | `#ownership`  | Obsidian                     | Turn features into outcomes                      | None                         |
| 5 | Pricing               | `#pricing`    | Graphite band                | Compare Free Tier and Pro                        | Get Pro                      |
| 6 | Trust and SmartScreen | `#trust`      | Obsidian with Graphite cards | Remove install doubt                             | None                         |
| 7 | FAQ                   | `#faq`        | Obsidian, 1px Slate top rule | Answer the last objections                       | None                         |
| 8 | Footer                | `#footer`     | Graphite                     | Close, navigate, and offer one final CTA         | Download free (default size) |

**The page's story in one line:** Here's the promise → here's the problem → here's how it works → here's why it matters to you → here's what it costs → here's why you can trust it → here are your answers → start now.

---

## Global Rules for This Page

### Product Facts

Every section must match these facts exactly.

| Fact      | Approved Wording                                                                              |
| --------- | --------------------------------------------------------------------------------------------- |
| Platform  | Windows 10 and 11 only                                                                        |
| Free Tier | ChatGPT, Claude, and Perplexity, 5 conversations each                                         |
| Pro       | All 8 providers, unlimited downloads, $24 one-time (launch price)                             |
| Providers | ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, Qwen                            |
| Gemini    | Comes through Google Takeout, which TotalRecalls converts to Markdown. Not a direct download. |
| Output    | Markdown and JSON files                                                                       |
| Location  | `C:\TotalRecalls\Library\` with one subfolder per provider                                    |
| Account   | No TotalRecalls account. Users sign in to each AI provider locally, inside the app.           |
| Cloud     | No cloud upload. Conversations aren't sent to TotalRecalls servers.                           |
| Internet  | Downloading needs internet. Opening saved files works offline.                                |
| Devices   | Pro includes up to three device activations                                                   |
| Updates   | Free updates to the core app. Future add-ons are separate purchases.                          |

### CTA System

| CTA                              | Style                                      | Destination     | Where It Appears                                              |
| -------------------------------- | ------------------------------------------ | --------------- | ------------------------------------------------------------- |
| **Download free**                | Primary, Archive Amber fill, Obsidian text | `/download/`    | Hero, How It Works, Pricing (Free card, as Secondary), Footer |
| **Get Pro — $24**                | Primary, Archive Amber fill, Obsidian text | `/buy/`         | Pricing (Pro card only)                                       |
| **See how it works**             | Secondary, transparent, 1px Slate border   | `#resolution`   | Hero                                                          |
| **Compare Free and Pro ↓**       | Tertiary, Steel Blue text                  | `#pricing`      | How It Works, Why Own Your AI Chats                           |
| **Read the SmartScreen guide →** | Tertiary, Steel Blue text                  | `/smartscreen/` | How It Works helper, Trust section, FAQ                       |

**Rules:**

- One Amber button per section, never two side by side.
- Primary sits left of Secondary, or on top when stacked on mobile.
- On the homepage, every "Compare Free and Pro" link scrolls to `#pricing`. Don't send visitors to a separate page mid-scroll.

### Brand System Summary

| Element            | Spec                                                                             |
| ------------------ | -------------------------------------------------------------------------------- |
| Fonts              | Inter (400, 500, 600, 700) for meaning. IBM Plex Mono (400, 500) for evidence.   |
| Base background    | Obsidian `#111315`                                                               |
| Raised surfaces    | Graphite `#1A1D21`                                                               |
| Borders            | Slate `#2A2F36`, 1px                                                             |
| Text               | Paper `#F3EFE7` headings, Mist `#D9D4CB` body, Dust `#B5AEA3` captions           |
| CTA                | Archive Amber `#C88A2B` with Obsidian text                                       |
| Metadata and links | Steel Blue `#7A8FA6`                                                             |
| Saved states       | Local Green `#5E8A68`, on Obsidian only for small text                           |
| Radius             | 6px chips · 8px buttons · 12px cards                                             |
| Section padding    | 96px desktop / 64px mobile (Hero: 128px desktop)                                 |
| Motion             | Optional one-time 200ms fade-in per section. Off under `prefers-reduced-motion`. |

**Local Green placement:** Small green text fails contrast on Graphite. In the How It Works and Pricing sections, which sit on Graphite bands, place every green chip inside an Obsidian card or well.

---

## Section 1: Hero

**Anchor:** `#top` · **Background:** Obsidian · **Padding:** 128px desktop / 64px mobile

### Copy

**Eyebrow**\
`WINDOWS APP · LOCAL-FIRST`

**Headline (H1)**

# Every AI conversation, kept on your own PC.

**Subheadline**\
Save chats from ChatGPT, Claude, and six more AI tools\
as Markdown and JSON files in one private folder you control.

**CTAs**

- **Primary:** Download free
- **Secondary:** See how it works

**Clarifier (below CTAs)**\
Free Tier covers ChatGPT, Claude, and Perplexity, 5 conversations each. Pro unlocks all 8 providers for $24 one-time (launch price).

**Clarifier (mobile only, replaces the line above)**\
Windows app. Visit from your desktop to download.

**Trust Strip**\
`NO CLOUD` · `NO ACCOUNT` · `ONE-TIME $24` · `WINDOWS 10/11`

**Product Visual**\
A real app screenshot, or a short silent loop of files landing in `C:\TotalRecalls\Library\`. 8px radius, 1px Slate border, placed on Graphite.

### Style Notes

| Element       | Style                                                                          |
| ------------- | ------------------------------------------------------------------------------ |
| Eyebrow       | IBM Plex Mono Medium 12px, uppercase, +0.12em, Steel Blue                      |
| H1            | `display`: Inter Bold 64px / 40px mobile, 1.05 line height, −0.02em, Paper     |
| Subheadline   | `body-lg`: Inter Regular 20px / 18px, Mist, max 680px                          |
| Primary CTA   | Large, 48px, Archive Amber, links to `/download/`                              |
| Secondary CTA | Large, 48px, transparent, 1px Slate border, Paper text, links to `#resolution` |
| Clarifier     | `body-sm`: Inter Regular 14px, Dust                                            |
| Trust chips   | IBM Plex Mono Medium 12px, uppercase, Dust on Slate, 6px radius                |

### Placement and Handoff

The hero makes the promise and gives a low-risk first step. Visitors who aren't ready to download scroll into Section 2, which explains why the promise matters. Visitors who click "See how it works" jump to Section 3 and skip the problem statement.

---

## Section 2: Why This Matters

**Anchor:** `#why` · **Background:** Obsidian, 1px Slate top rule to separate it from the hero

### Copy

**Eyebrow**\
`WHY THIS MATTERS`

**Headline (H2)**

## AI chat history drifts. Files stay put.

**Problem Statements (three columns)**

**Tabs close.**\
Threads sink under hundreds of newer ones.

**Interfaces change.**\
Old chats get harder to reach.

**Nobody keeps a backup.**\
Until they need one.

**Pivot Line**\
TotalRecalls saves each chat as a plain file on your own PC.

**Evidence Strip (static)**\
`C:\TotalRecalls\Library\claude\2026-07-28-refactor-plan.md` · `.MD` · `.JSON` · `● SAVED LOCALLY`

**CTAs**\
None. This section explains. It doesn't sell.

### Style Notes

| Element            | Style                                                       |
| ------------------ | ----------------------------------------------------------- |
| H2                 | Inter Semibold 36px / 28px, Paper                           |
| Problem leads      | `h4`: Inter Semibold 18px, Paper                            |
| Problem follow-ups | `body`: Inter Regular 16px, Mist                            |
| Column dividers    | 1px Slate, vertical on desktop, horizontal on mobile        |
| Pivot line         | `body-lg`, Paper, max 680px                                 |
| File path          | IBM Plex Mono 14px, Steel Blue, selectable                  |
| Saved chip         | Local Green on Obsidian, transparent fill, 1px Slate border |

### Placement and Handoff

This section replaces the old Live Feed. It keeps the evidence-ticker idea as one static file entry, with no red, no motion, and no alert language. The pivot line promises a plain file on your PC, and Section 3 shows exactly how you get one.

---

## Section 3: How It Works

**Anchor:** `#resolution` (the hero's "See how it works" button lands here) · **Background:** Graphite band

### Copy

**Eyebrow**\
`HOW IT WORKS`

**Headline (H2)**

## Four steps from scattered chats to one local folder.

**Intro**\
Setup takes a few minutes. After that, each download is a pick and a click.

**Step 01: Buy once**\
Check out for $24, one time, at the launch price. Your license key arrives by email. Prefer to test first? Skip this step and start on the Free Tier.\
`$24 · ONE-TIME · NO SUBSCRIPTION`

**Step 02: Install**\
Unzip the download and run TotalRecalls on your Windows PC. You don't create an account or sign up for anything.\
`WINDOWS 10/11 · NO ACCOUNT`

**Step 03: Pick your providers**\
Choose from ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen. You sign in to each provider locally, inside the app.\
`8 PROVIDERS · LOCAL SIGN-IN`

**Step 04: Download**\
Your chats land in your Library folder as Markdown and JSON files. Search them, open them offline, and keep them.\
`.MD + .JSON · SAVED LOCALLY`

**Provider-to-Folder Diagram**

- Eight provider nodes on the left, each with its mono ID: ChatGPT `OAI-001`, Claude `ANT-002`, Perplexity `PPL-003`, Gemini `GEM-004`, Grok `GRK-005`, DeepSeek `DSK-006`, Mistral `MST-007`, Qwen `QWN-008`
- Seven solid Steel Blue lines labeled `DIRECT`
- Gemini's line is dashed and labeled `TAKEOUT → MD`
- All lines merge into one folder panel showing:

```
C:\TotalRecalls\Library\
├── chatgpt\
├── claude\
├── perplexity\
├── gemini\
└── …
```

- Output chips under the folder: `.MD` · `.JSON` · `● SAVED LOCALLY`

**Diagram Caption**\
Eight sources. One folder on your own drive.

**SmartScreen Helper**\
First launch may show a Windows SmartScreen prompt. Here's why, and how to continue.

**Closing Line**\
Start free with ChatGPT, Claude, and Perplexity. Upgrade to Pro when you want all eight.

**CTAs**

- **Primary:** Download free
- **Tertiary:** Compare Free and Pro ↓

### Style Notes

| Element          | Style                                                                                     |
| ---------------- | ----------------------------------------------------------------------------------------- |
| Step cards       | Obsidian fill on the Graphite band, 1px Slate border, 12px radius, 24px padding, no hover |
| Step numbers     | IBM Plex Mono Medium 14px, Steel Blue                                                     |
| Step titles      | `h3`: Inter Semibold 24px / 20px, Paper                                                   |
| Step chips       | Mono 12px, Steel Blue on Slate, pinned to card bottom. `SAVED LOCALLY` in Local Green.    |
| Diagram panel    | Obsidian, 1px Slate border, 12px radius. Provider names as text only. No logos.           |
| SmartScreen link | "Here's why" in Steel Blue, links to `/smartscreen/`                                      |
| Tertiary CTA     | Steel Blue, links to `#pricing`                                                           |

### Placement and Handoff

This is the page's first mid-scroll conversion point. Step 01 names the price but points straight to the Free Tier, so the section never pressures a first-time visitor. The SmartScreen helper plants a calm expectation that Section 6 will fully resolve. The closing line hands off to Section 4, which explains what owning those files actually gets you.

---

## Section 4: Why Own Your AI Chats

**Anchor:** `#ownership` · **Background:** Obsidian

### Copy

**Eyebrow**\
`WHY OWN YOUR AI CHATS`

**Headline (H2)**

## Your best thinking deserves a better home than a sidebar.

**Intro**\
Your AI chats hold research, drafts, code, and decisions. When you own your AI chats, that work lives on your own PC as files you control.

**Card 1: Find it again.**\
A saved file is one quick search away, not 400 threads down a sidebar.\
`SEARCHABLE · LOCAL FILES`

**Card 2: Keep it through redesigns.**\
A Markdown file opens the same way in Notepad next year, whatever the chat interface looks like.\
`.MD + .JSON`

**Card 3: Take it anywhere.**\
Copy the folder to a new PC or a backup drive, and your library comes with you, no login needed.\
`COPY FOLDER · NO LOGIN`

**Evidence Strip**\
`C:\TotalRecalls\Library\claude\2026-07-28-refactor-plan.md` · `● SAVED LOCALLY`

**CTAs (homepage version)**

- **Tertiary only:** Compare Free and Pro ↓

### Homepage Adjustment

The standalone 3-card section ends with a Free Tier line and a "Download free" button. On the homepage, **remove both.** Pricing sits directly below, so repeating the tier details and a third Amber button here would slow the page. The tertiary link carries the reader into Section 5.

### Style Notes

| Element         | Style                                                                                                                              |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Cards           | Graphite fill, 1px Slate border, 12px radius, 24px padding, three equal columns on desktop, stacked on tablet and mobile           |
| Card leads      | `h4`: Inter Semibold 18px, Paper                                                                                                   |
| Card follow-ups | `body`: Inter Regular 16px, Mist                                                                                                   |
| Card chips      | Mono 12px, Steel Blue. Verify contrast on Slate in the browser. If it falls short, use a transparent fill with a 1px Slate border. |
| Evidence strip  | Directly on Obsidian between 1px Slate rules. `SAVED LOCALLY` in Local Green.                                                      |
| Optional icons  | 24px line icons in Mist: magnifying glass, file with lines, folder. No cloud, shield, or lock icons.                               |

### Placement and Handoff

Section 3 explained the mechanics. This section explains the payoff in plain outcomes. By the end, the reader knows what they'd own and why it matters, so the natural next question is cost. Section 5 answers it immediately.

---

## Section 5: Pricing

**Anchor:** `#pricing` · **Background:** Graphite band

### Copy

**Eyebrow**\
`PRICING`

**Headline (H2)**

## Start free. Pay once when you want all eight.

**Intro**\
Test TotalRecalls on your own chats before you spend anything. When you're ready, one payment unlocks every provider. No subscription.

---

**Card A: Free Tier**

`FREE`

**$0**

Try the app on your real conversations.

- ✓ ChatGPT, Claude, and Perplexity
- ✓ 5 conversations per provider
- ✓ Markdown and JSON files
- ✓ Saved locally to `C:\TotalRecalls\Library\`
- — Gemini, Grok, DeepSeek, Mistral, and Qwen
- — Unlimited downloads

**CTA (Secondary):** Download free

---

**Card B: Pro**

`PRO` · `LAUNCH PRICE`

**$24** one-time

Every provider. Every conversation. No subscription.

- ✓ All 8 providers: ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen
- ✓ Unlimited downloads
- ✓ Markdown and JSON files, saved locally
- ✓ Up to 3 device activations
- ✓ Free updates to the core app
- ✓ License key delivered by email

**CTA (Primary):** Get Pro — $24

---

**Microcopy (below both cards)**\
Windows 10 and 11. $24 is a discounted launch price. Future add-ons are sold separately. Your core app updates stay free.

`ONE-TIME` · `NO SUBSCRIPTION` · `NO ACCOUNT` · `WINDOWS 10/11`

### Style Notes

| Element           | Style                                                                                                                                                           |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Cards             | Obsidian fill on the Graphite band, 1px Slate border, 12px radius, 32px padding, equal height, side by side on desktop, stacked on mobile (Pro first on mobile) |
| Pro card border   | 1px Archive Amber. No oversized "Most Popular" banner.                                                                                                          |
| Tier chips        | `FREE`: Mist on Slate. `PRO`: Archive Amber on Amber Tint. `LAUNCH PRICE`: Steel Blue on Slate.                                                                 |
| Price             | `h1` size, Inter Bold, tabular figures. Pro price in Archive Amber. Free price in Paper.                                                                        |
| Checks            | Local Green check icons (safe on Obsidian cards)                                                                                                                |
| Unavailable items | Dust dash and Dust text. No red X.                                                                                                                              |
| Free CTA          | Secondary: transparent, 1px Slate border, Paper text, links to `/download/`                                                                                     |
| Pro CTA           | Primary: Archive Amber fill, Obsidian text, links to `/buy/`. The section's only Amber button.                                                                  |
| Microcopy         | `body-sm`, Dust, centered under the cards                                                                                                                       |

### Placement and Handoff

This section is where intent peaks. The Free card lets cautious visitors start without risk, and the Pro card gives ready buyers a clear, single action. Both cards say "Saved locally," which hands off to Section 6 for visitors who still wonder whether they can trust a new Windows app.

---

## Section 6: Trust and SmartScreen

**Anchor:** `#trust` · **Background:** Obsidian with Graphite cards

### Copy

**Eyebrow**\
`STRAIGHT TALK`

**Headline (H2)**

## Plain answers before you install.

**Intro**\
You're giving a new app access to your A
