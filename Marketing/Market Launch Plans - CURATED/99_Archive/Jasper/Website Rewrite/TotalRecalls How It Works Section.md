# TotalRecalls How It Works Section

## Section Copy

**Eyebrow**\
`HOW IT WORKS`

**Section Headline**

## Four steps from scattered chats to one local folder.

**Intro**\
Setup takes a few minutes. After that, each download is a pick and a click.

---

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

---

**Diagram Caption**\
Eight sources. One folder on your own drive.

**SmartScreen Helper**\
First launch may show a Windows SmartScreen prompt. Here's why, and how to continue.

**Closing Line**\
Start free with ChatGPT, Claude, and Perplexity. Upgrade to Pro when you want all eight.

**CTAs**

- **Primary:** Download free
- **Tertiary:** Compare Free and Pro →

**Visible word count:** About 165 words, including chips and CTAs

---

## Provider-to-Folder Diagram

### Concept

The diagram shows the section's promise in one glance. Many sources converge on one folder, and every line ends on your own PC.

### Desktop Layout (left to right)

1. **Provider nodes (left column):** Eight stacked nodes, each a small Obsidian chip with a 1px Slate border. Each shows the provider name in Inter Medium and a mono ID in Steel Blue:

   - ChatGPT `OAI-001`
   - Claude `ANT-002`
   - Perplexity `PPL-003`
   - Gemini `GEM-004`
   - Grok `GRK-005`
   - DeepSeek `DSK-006`
   - Mistral `MST-007`
   - Qwen `QWN-008`

2. **Connector lines (middle):** Thin 1.5px Steel Blue lines curve from each node into a single merge point. Seven lines are solid and labeled `DIRECT` at the node end. Gemini's line is **dashed** and labeled `TAKEOUT → MD`.

3. **Merge point:** A small Steel Blue node where the lines meet, with a 24px download-into-tray icon.

4. **Library folder (right):** An Obsidian panel with a 1px Slate border and a folder icon. It shows a short mono file tree:

```
C:\TotalRecalls\Library\
├── chatgpt\
├── claude\
├── perplexity\
├── gemini\
└── …
```

5. **Output chips (below the folder panel):** `.MD` · `.JSON` · `● SAVED LOCALLY`

### Mobile Layout (top to bottom)

- Provider nodes wrap into a 2 × 4 grid.
- Lines collapse into one short vertical connector with a down arrow.
- The Library folder panel sits below at full width, with the file tree trimmed to three subfolders and `…`.
- Gemini keeps a small `TAKEOUT → MD` chip beside its node, so the difference stays visible.

### Diagram Rules

- Use provider names as text only. No official logos, brand colors, or interface screenshots.
- No cloud icons anywhere in the diagram.
- Keep it static. An optional one-time animation can draw the lines left to right over 600ms, then stop.

---

## Layout

1. **Header block:** The eyebrow, headline, and intro sit left-aligned at the top, with the intro capped at 680px.
2. **Step row:** Four equal step cards in a single row on desktop. They become a 2 × 2 grid on tablet and a single stacked column on mobile.
3. **Diagram:** Full content width below the step row, framed as one Obsidian panel.
4. **Helper and close:** The SmartScreen helper appears as a small line under the diagram. The closing line and CTAs sit left-aligned at the bottom.

---

## Implementation Spec

| Element            | Copy                                                           | Style                                                                                                                                                     |
| ------------------ | -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Section background | —                                                              | Graphite `#1A1D21` band, 96px vertical padding desktop / 64px mobile. Anchor `id="resolution"` so the hero's "See how it works" button lands here.        |
| Eyebrow            | HOW IT WORKS                                                   | IBM Plex Mono Medium, 12px, uppercase, +0.12em tracking, Steel Blue `#7A8FA6`                                                                             |
| Headline           | Four steps from scattered chats to one local folder.           | `h2`: Inter Semibold, 36px desktop / 28px mobile, 1.15 line height, −0.01em, Paper `#F3EFE7`                                                              |
| Intro              | Setup takes a few minutes…                                     | `body-lg`: Inter Regular, 20px desktop / 18px mobile, 1.55 line height, Mist `#D9D4CB`, max width 680px                                                   |
| Step card          | —                                                              | Obsidian `#111315` fill, 1px Slate `#2A2F36` border, 12px radius, 24px padding, no shadow, equal heights                                                  |
| Step number        | 01 / 02 / 03 / 04                                              | IBM Plex Mono Medium, 14px, Steel Blue                                                                                                                    |
| Step icon          | Tray-download / folder-archive / nodes-merge / file-with-lines | 24px line icon, 1.5px stroke, Mist                                                                                                                        |
| Step title         | Buy once / Install / Pick your providers / Download            | `h3`: Inter Semibold, 24px desktop / 20px mobile, Paper                                                                                                   |
| Step body          | Two to three sentences                                         | `body`: Inter Regular, 16px, 1.6 line height, Mist                                                                                                        |
| Step metadata chip | e.g., `WINDOWS 10/11 · NO ACCOUNT`                             | `mono-sm`: IBM Plex Mono Medium, 12px, uppercase, +0.02em, Steel Blue text, Slate fill, 6px radius, 4px × 8px padding. Pinned to the card bottom.         |
| Step 04 chip       | `.MD + .JSON · SAVED LOCALLY`                                  | Same spec, but the `SAVED LOCALLY` segment uses Local Green `#5E8A68` text with a dot. This is the section's only green state signal outside the diagram. |
| Diagram panel      | —                                                              | Obsidian fill, 1px Slate border, 12px radius, 48px padding desktop / 24px mobile                                                                          |
| Provider node      | Name + mono ID                                                 | Obsidian chip, 1px Slate border, 6px radius. Name in Inter Medium 14px, Paper. ID in IBM Plex Mono 12px, Steel Blue.                                      |
| Connector lines    | —                                                              | 1.5px Steel Blue. Gemini line dashed (4px dash, 4px gap).                                                                                                 |
| Line labels        | `DIRECT` / `TAKEOUT → MD`                                      | `mono-sm`, Dust `#B5AEA3`                                                                                                                                 |
| File tree          | `C:\TotalRecalls\Library\…`                                    | `mono`: IBM Plex Mono Regular, 14px desktop / 13px mobile, Steel Blue, selectable                                                                         |
| Output chips       | `.MD` · `.JSON` · `● SAVED LOCALLY`                            | `mono-sm`, transparent fill, 1px Slate border, 6px radius. File chips in Steel Blue. Local chip in Local Green.                                           |
| Diagram caption    | Eight sources. One folder on your own drive.                   | `body-sm`: Inter Regular, 14px, Dust, centered under the panel                                                                                            |
| SmartScreen helper | First launch may show…                                         | `body-sm`, Dust, with "Here's why" as a Steel Blue inline link to the SmartScreen explainer                                                               |
| Closing line       | Start free with…                                               | `body`: Inter Regular, 16px, Paper                                                                                                                        |
| Primary CTA        | Download free                                                  | Default button, 40px height, Archive Amber `#C88A2B` fill, Obsidian text, 8px radius, links to `/download/`                                               |
| Tertiary CTA       | Compare Free and Pro →                                         | Inter Semibold, 15px, Steel Blue, no border, links to `#pricing`                                                                                          |

### Spacing

| Gap                          | Value                                     |
| ---------------------------- | ----------------------------------------- |
| Eyebrow → headline           | 12px                                      |
| Headline → intro             | 16px                                      |
| Intro → step row             | 48px                                      |
| Between step cards           | 24px                                      |
| Step number → icon → title   | 12px each                                 |
| Title → body                 | 8px                                       |
| Body → metadata chip         | 16px minimum (chip pinned to card bottom) |
| Step row → diagram           | 48px                                      |
| Diagram → caption            | 12px                                      |
| Caption → SmartScreen helper | 24px                                      |
| Helper → closing line        | 32px                                      |
| Closing line → CTAs          | 16px                                      |
| Between CTAs                 | 16px                                      |

### Behavior

- **Static by default.** No carousel, auto-advance, or looping motion.
- **Optional reveal:** Step cards fade in with an 8px upward slide over 200ms, staggered 60ms apart, triggered once on scroll. The diagram lines draw once over 600ms. Disable both under `prefers-reduced-motion`.
- **Card hover:** None. Step cards aren't interactive, so they shouldn't look clickable.
- **Mobile file path:** Let the path wrap at backslashes. Never shrink mono text below 12px.

### Contrast Check

- Steel Blue on Obsidian (≈5.6:1) and Local Green on Obsidian (≈4.7:1) pass WCAG AA at 12px.
- Local Green appears only inside Obsidian cards and panels, never directly on the Graphite band, where it would fail at small sizes.
- Dust captions on Graphite pass comfortably for body-sm text.

---

## Why This Section Works

- **The headline states the before and after.** "Scattered chats" names the problem from Section 2. "One local folder" names the outcome. "Four steps" sets expectations before the reader scans.
- **Step 01 removes the biggest objection.** Buying first can feel like a commitment, so the step immediately points to the Free Tier. That keeps the flow honest and matches the hero's "Download free" button.
- **Each step ends with evidence.** The mono chips turn every step into a checkable fact: one-time price, Windows 10/11, eight providers, Markdown and JSON.
- **The diagram tells the truth about Gemini.** A dashed line and a `TAKEOUT → MD` label show the difference plainly, without hiding it in fine print.
- **Green appears only at the finish.** "Saved locally" shows up only at the end of the flow, so the eye lands on the result.
- **SmartScreen is handled calmly.** One small helper line prepares first-time installers without adding alarm to the section.

---

## Accuracy Checks Before Publishing

- **Gemini is not a direct download.** Gemini chats come through Google Takeout, which TotalRecalls converts to Markdown. Keep the dashed line and label, and never describe Gemini as a one-click download.
- **Windows 10 and 11 only.** Don't add Mac or Linux icons. If you mention those platforms, say they're "in development," not "coming soon" with a date.
- **"No account" means no TotalRecalls account.** Users still sign in to each AI provider locally. Step 03 says this directly. Keep that sentence.
- **Confirm the checkout processor.** The current site says Paddle, and the business description says Lemon Squeezy. Step 01 avoids naming either one. Confirm which is live before adding a processor name anywhere.
- **Free Tier limits:** ChatGPT, Claude, and Perplexity, with 5 conversations per provider. Confirm this matches the current build.
- **Pricing label:** Keep "at the launch price" beside $24. Update Step 01 and the step chip when the launch price ends.
- **Downloads need internet.** Opening saved files works offline. Downloading doesn't. Don't imply the whole flow runs offline.
- **Device activations:** Pro includes up to three device activations. Don't write "install on any PC" or "unlimited devices" in this section.
- **Match the real folder structure.** The path `C:\TotalRecalls\Library\` and the provider subfolder names must match the current build exactly.
- **"Setup takes a few minutes" is conservative on purpose.** Don't swap in a specific time claim unless you've timed it on a clean Windows install.
