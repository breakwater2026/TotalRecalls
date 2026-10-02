# TotalRecalls Pricing Section

## Section Copy

**Eyebrow**\
`PRICING`

**Section Headline**

## Start free. Pay once. That's the whole plan.

**Intro**\
Try TotalRecalls on your own chats with no card and no account. If you want every provider and no limits, Pro is one payment.

---

### Card 1: Free Tier

**Chip**\
`FREE TIER`

**Plan Name**\
Free

**Price**\
`$0`

**Price Note**\
No payment required

**Card Line**\
Enough to see it work. Not quite enough for nine months of prompts.

**Includes**

- ✓ ChatGPT, Claude, and Perplexity
- ✓ 5 conversations per provider
- ✓ Markdown and JSON files saved on your PC
- ✓ No TotalRecalls account, no card
- – Gemini, Grok, DeepSeek, Mistral, and Qwen
- – Unlimited downloads

**CTA**\
Download free

**Card Footer**\
`WINDOWS 10/11`

---

### Card 2: Pro

**Chips**\
`PRO` · `50% OFF · LAUNCH PRICE`

**Plan Name**\
Pro

**Price**\
`$24 USD`

**Price Note**\
One-time. No subscription. Discounted launch price.

**Card Line**\
Every provider. Every conversation. Paid for once.

**Includes**

- ✓ All 8 providers: ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen
- ✓ Unlimited downloads
- ✓ Up to 3 device activations
- ✓ Free updates to the core app
- ✓ License key delivered by email
- ✓ Markdown and JSON files saved on your PC

**CTA**\
Get Pro for $24

**Card Footer**\
`WINDOWS 10/11 · LICENSE KEY BY EMAIL`

**Gemini Helper (below Pro list)**\
Gemini chats come through Google Takeout, and TotalRecalls converts them to Markdown.

---

### Feature Comparison

| Feature                               | Free | Pro            |
| ------------------------------------- | ---- | -------------- |
| ChatGPT, Claude, Perplexity           | ✓    | ✓              |
| Gemini, Grok, DeepSeek, Mistral, Qwen | –    | ✓              |
| Conversations per provider            | `5`  | `UNLIMITED`    |
| Markdown + JSON files                 | ✓    | ✓              |
| Saved locally on your PC              | ✓    | ✓              |
| TotalRecalls account required         | No   | No             |
| Device activations                    | –    | `UP TO 3`      |
| Free core app updates                 | –    | ✓              |
| Price                                 | `$0` | `$24 ONE-TIME` |

---

### Closing Trust Line

Both plans run entirely on your Windows PC. Your conversations never leave your machine, so there's no cloud library for anyone to lose.

**Trust Strip**\
`NO SUBSCRIPTION` · `NO ACCOUNT` · `100% LOCAL` · `WINDOWS 10/11`

**Mobile Clarifier (mobile only)**\
Windows app. Visit from your desktop to download.

**Visible word count:** About 230 words, including chips, table, and CTAs

---

## Layout

1. **Header block:** The eyebrow, headline, and intro are left-aligned at the top. The intro is capped at 680px.
2. **Pricing cards:** Two equal-height cards sit side by side on desktop and tablet. Free is on the left and Pro is on the right. On mobile, the cards stack with **Free first**, so the lowest-friction option leads.
3. **Feature comparison:** A compact table spans the full content width below the cards. On mobile, it collapses into a two-column list grouped by plan.
4. **Close:** The trust line and trust strip sit left-aligned at the bottom, with open space above.

---

## Implementation Spec

| Element            | Copy                                         | Style                                                                                                                                                               |
| ------------------ | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Section background | —                                            | Obsidian `#111315`, 96px vertical padding desktop / 64px mobile. Anchor `id="pricing"` so "Compare Free and Pro →" in How It Works lands here.                      |
| Eyebrow            | PRICING                                      | IBM Plex Mono Medium, 12px, uppercase, +0.12em tracking, Steel Blue `#7A8FA6`                                                                                       |
| Headline           | Start free. Pay once. That's the whole plan. | `h2`: Inter Semibold, 36px desktop / 28px mobile, 1.15 line height, −0.01em, Paper `#F3EFE7`                                                                        |
| Intro              | Try TotalRecalls on your own chats…          | `body-lg`: Inter Regular, 20px desktop / 18px mobile, 1.55 line height, Mist `#D9D4CB`, max width 680px                                                             |
| Free card          | —                                            | Graphite `#1A1D21` fill, 1px Slate `#2A2F36` border, 12px radius, 32px padding, no shadow                                                                           |
| Pro card           | —                                            | Graphite fill, **1px Archive Amber `#C88A2B` border**, 12px radius, 32px padding, no shadow. No "Most Popular" banner.                                              |
| Card height        | —                                            | Equal heights. Use CSS grid `align-items: stretch`, and pin CTAs to the card bottom.                                                                                |
| Free chip          | FREE TIER                                    | `mono-sm`: IBM Plex Mono Medium, 12px, uppercase, +0.02em, Mist text, Slate fill, 6px radius, 4px × 8px padding                                                     |
| PRO chip           | PRO                                          | `mono-sm`, Archive Amber text on Amber Tint (`#C88A2B` at 12%), 6px radius                                                                                          |
| Launch chip        | 50% OFF · LAUNCH PRICE                       | `mono-sm`, Steel Blue text on Slate fill, 6px radius                                                                                                                |
| Plan name          | Free / Pro                                   | `h3`: Inter Semibold, 24px desktop / 20px mobile, Paper                                                                                                             |
| Price figure       | $0 / $24 USD                                 | IBM Plex Mono Medium, 48px desktop / 36px mobile, tabular figures, 1.1 line height, Paper. "USD" at 16px, Dust `#B5AEA3`.                                           |
| Price note         | No payment required / One-time…              | `body-sm`: Inter Regular, 14px, Mist                                                                                                                                |
| Card line          | Enough to see it work…                       | `body`: Inter Regular, 16px, 1.6 line height, Paper                                                                                                                 |
| Card divider       | —                                            | 1px Slate, between the card line and feature list                                                                                                                   |
| Included feature   | ✓ lines                                      | `body`: Inter Regular, 16px, Mist. 16px check-in-circle icon, Local Green `#5E8A68`.                                                                                |
| Excluded feature   | – lines                                      | `body`: Inter Regular, 16px, Dust. Dust dash, not a red X.                                                                                                          |
| Free CTA           | Download free                                | Large secondary button, 48px height, full card width, transparent fill, 1px Slate border, Paper text, 8px radius, links to `/download/`                             |
| Pro CTA            | Get Pro for $24                              | Large primary button, 48px height, full card width, Archive Amber fill, Obsidian text, 8px radius, links to `/buy/`. This is the section's only Amber fill.         |
| Card footer        | WINDOWS 10/11…                               | `mono-sm`, Dust, centered under the CTA                                                                                                                             |
| Gemini helper      | Gemini chats come through…                   | `body-sm`, Dust, with a Steel Blue inline link to the Gemini Takeout guide                                                                                          |
| Comparison table   | —                                            | Transparent fill, 1px Slate row dividers, 16px vertical cell padding. Header row in Inter Medium 13px uppercase, Dust. Row labels in `body-sm`, Mist.               |
| Table values       | ✓ / – / mono values                          | Checks in Local Green (16px icon). Dashes in Dust. Mono values (`5`, `UNLIMITED`, `UP TO 3`, `$24 ONE-TIME`) in IBM Plex Mono Medium, 13px, tabular figures, Paper. |
| Trust line         | Both plans run entirely…                     | `body-lg`: Inter Regular, 20px desktop / 18px mobile, Paper, max width 680px                                                                                        |
| Trust strip        | 4 chips                                      | `mono-sm`, Dust text, Slate fill, 6px radius, 4px × 8px padding                                                                                                     |
| Mobile clarifier   | Windows app…                                 | `body-sm`, Dust, shown below the Free CTA on screens under 768px                                                                                                    |

### Spacing

| Gap                            | Value                                    |
| ------------------------------ | ---------------------------------------- |
| Eyebrow → headline             | 12px                                     |
| Headline → intro               | 16px                                     |
| Intro → cards                  | 48px                                     |
| Between cards                  | 24px desktop / 16px stacked mobile       |
| Chip row → plan name           | 16px                                     |
| Plan name → price              | 8px                                      |
| Price → price note             | 4px                                      |
| Price note → card line         | 16px                                     |
| Card line → divider → features | 24px each side                           |
| Between feature lines          | 12px                                     |
| Features → CTA                 | 32px minimum (CTA pinned to card bottom) |
| CTA → card footer              | 12px                                     |
| Cards → comparison table       | 64px                                     |
| Table → trust line             | 48px                                     |
| Trust line → trust strip       | 16px                                     |
| Between trust chips            | 8px                                      |

### Behavior

- **Static by default.** No toggles, sliders, countdown timers, or animated price counters.
- **Optional reveal:** Cards fade in with an 8px upward slide over 200ms, 60ms apart, triggered once on scroll. Disable under `prefers-reduced-motion`.
- **Card hover:** None. Only the buttons are interactive.
- **Button states:** The primary shifts to Amber Hover `#D69A3D` and pressed to `#AE7722`. The secondary border shifts to Mist on hover. Focus is a 2px Amber ring with a 2px offset. Transitions run for 150ms on color only.
- **Mobile Pro CTA:** Keep it active. Visitors can buy on a phone and receive the license key by email. The mobile clarifier reminds them to install from a Windows desktop.

### Contrast Check

- Paper, Mist, and Dust on Graphite all pass WCAG AA for body text.
- Local Green appears only as 16px check icons on Graphite, which is approved for icons.
- Obsidian on Archive Amber (≈6.3:1) passes for the Pro button label.
- The 1px Amber border is decorative, so it doesn't carry text and isn't held to text contrast.

---

## Why This Section Works

- **The headline sums up the business model in six words.** "Start free. Pay once." answers the two biggest pricing questions before anyone reads a card. "That's the whole plan" adds the dry turn and signals there's no fine print.
- **Free leads, Pro wins the accent.** Free sits first to match the hero's "Download free" path. Pro gets the only Amber fill, so the eye knows where the full product lives.
- **The card lines are honest about limits.** "Not quite enough for nine months of prompts" admits the Free Tier is a trial and makes the upgrade case with a smile instead of pressure.
- **Mono prices read as facts.** Setting `$0` and `$24 USD` in IBM Plex Mono treats them as evidence, like a file path or timestamp, rather than a sales flourish.
- **Dashes, not red X's.** Missing Free features look calm and neutral, which keeps the section in line with the brand's calm-over-alarm rule.
- **Gemini is handled up front.** One helper line explains the Takeout step, so Pro buyers aren't surprised later.
- **The close returns to the core promise.** Pricing ends on privacy and ownership, not urgency. That's the reason people buy.

---

## Accuracy Checks Before Publishing

- **Free Tier wording differs between sources.** The live site says "5 conversations per download," and the business description says "up to five conversations per provider." This section uses "per provider." Confirm which matches the current build, then use the same phrase everywhere.
- **Launch price label.** Keep "50% off · launch price" beside $24 on every surface. Don't show a crossed-out $48 unless that regular price is confirmed. Don't add a deadline or timer unless the end date is real and published.
- **Update everything when the launch price ends.** That includes the price figure, the launch chip, the Pro CTA label, the comparison table, and matching copy in the hero and How It Works sections.
- **Free updates cover the core app only.** Future add-ons are separate purchases. Don't write "all future features included" or "lifetime access to everything."
- **Device activations.** Pro allows up to 3 device activations. Never write "unlimited devices" or "install anywhere."
- **Checkout processor.** The site names Paddle, and the business description names Lemon Squeezy. This section says only "license key delivered by email." Confirm which processor is live before naming one.
- **Refund language stays out of this section.** The site describes case-by-case handling, and the business description says no refunds. Keep refund terms on the FAQ and legal pages, and align those sources first.
- **"No account" means no TotalRecalls account.** Users still sign in to each AI provider locally. The How It Works section already explains this.
- **Gemini is not a direct download.** Keep the Takeout helper line and never describe Gemini as one-click.
- **Windows 10 and 11 only.** Don't add Mac or Linux icons to the cards. If you mention them elsewhere, call them "in development" with no date.
- **"Never leave your machine" applies to conversations.** Downloads still need an internet connection to reach each provider. Opening saved files works offline.
- **Link targets.** Confirm `/download/` and `/buy/` resolve correctly and that `id="pricing"` matches the anchor used by earlier sections.
