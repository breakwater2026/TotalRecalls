# TotalRecalls YouTube Channel Style

**Version 1.0 · Visual Identity: Private Archive + Calm Utility**

This guide shows how the TotalRecalls look carries over to YouTube: the banner, channel icon, thumbnails, playlist covers, watermark, end screens, and the overall feel of the channel page. Every spec works with free or low-cost tools, so one person can build, update, and keep the system consistent.

The goal is simple. Someone scrolling past a TotalRecalls thumbnail, or landing on the channel page, should sense **order, privacy, and permanence** before they read a word.

---

## 1. Channel Aesthetic at a Glance

### The Feeling

> **A calm, well-kept archive for important AI work.**

Viewers should feel they've found a quiet, competent corner of YouTube. It shouldn't feel like another loud AI hype channel.

### Aesthetic Pillars

| Pillar            | What It Looks Like on YouTube                                                    |
| ----------------- | -------------------------------------------------------------------------------- |
| **Dark and warm** | Obsidian and Graphite backgrounds with Paper text. No pure black, no pure white. |
| **Evidence-led**  | File paths, folders, `.md` and `.json` chips, and real app footage               |
| **Restrained**    | One Archive Amber highlight per graphic. Plenty of empty space.                  |
| **Consistent**    | Same layout, same chip position, same type, every time                           |
| **Honest**        | Visuals match the real product: Windows only, accurate tiers, labeled pricing    |

### Core Palette for YouTube

| Name              | Hex       | YouTube Role                                                     |
| ----------------- | --------- | ---------------------------------------------------------------- |
| **Obsidian**      | `#111315` | Banner base, thumbnail backgrounds, icon background, end screens |
| **Graphite**      | `#1A1D21` | Panels, cards, lower thirds, subtle banner bands                 |
| **Archive Amber** | `#C88A2B` | One highlight word, icon mark, key chip, CTA button graphic      |
| **Paper**         | `#F3EFE7` | Headlines, wordmark, primary text                                |

**Supporting colors (use sparingly):**

- **Slate** `#2A2F36`: borders, chip fills, dividers
- **Mist** `#D9D4CB`: secondary text
- **Steel Blue** `#7A8FA6`: file paths, metadata chips, diagram lines
- **Local Green** `#5E8A68`: "saved" or "complete" states only

### What the Channel Should Never Look Like

- Neon outlines, glows, scanlines, or glitch effects
- Cyberpunk, gamer, or "hacker" styling
- Red arrows, circled objects, shocked faces, or emoji-heavy thumbnails
- Glowing brains, sparkles, robots, or other AI clichés
- Official provider logos, brand colors, or sharp interface screenshots
- Rainbow or purple "AI" gradients

---

## 2. Channel Banner

### 2.1 Specs

| Item                    | Spec                                                        |
| ----------------------- | ----------------------------------------------------------- |
| **Upload size**         | 2560 × 1440px                                               |
| **Minimum upload size** | 2048 × 1152px                                               |
| **File size**           | 6MB or smaller                                              |
| **Format**              | PNG preferred for crisp text; JPG at high quality works too |
| **Color profile**       | sRGB                                                        |

### 2.2 Display Zones

YouTube crops the banner differently on each device. Design for the smallest zone first.

| Zone                        | Size          | What Shows There                                   |
| --------------------------- | ------------- | -------------------------------------------------- |
| **TV (full image)**         | 2560 × 1440px | Everything, including the top and bottom bands     |
| **Desktop (max width)**     | 2560 × 423px  | The full-width horizontal strip through the center |
| **Tablet**                  | 1855 × 423px  | A narrower center strip                            |
| **Text and logo safe area** | 1546 × 423px  | The center strip visible on every device           |

**Rule:** All text, the wordmark, and any meaningful graphic must sit inside the **1546 × 423px safe area**, centered in the canvas. Everything outside it is background texture only.

### 2.3 Layout

```
┌──────────────────────────────────────────────────────────────┐
│                  Obsidian (TV-only area)                     │
│              Faint folder grid texture, 4–6% opacity         │
│                                                              │
│        ┌────────────── SAFE AREA 1546 × 423 ─────────────┐   │
│  Graph │  [Wordmark]                                     │   │
│  -ite  │  Your AI chats. Your PC.                        │   │
│  band  │  Save ChatGPT, Claude, and 6 more AI tools      │   │
│        │  as local files.                                │   │
│        │  C:\TotalRecalls\Library\     ● SAVED LOCALLY   │   │
│        └─────────────────────────────────────────────────┘   │
│                                                              │
│                  Obsidian (TV-only area)                     │
└──────────────────────────────────────────────────────────────┘
```

**Background:**

- Obsidian `#111315` fills the full canvas.
- A Graphite `#1A1D21` horizontal band, 423px tall, runs through the vertical center. It gives the desktop view quiet depth.
- Optional texture: a very faint grid of folder or file-line icons in Slate, 4–6% opacity, placed **outside** the safe area only. It should read as "archive shelving," not as a pattern you notice.

**Left side of the safe area (text block, left-aligned):**

- **Wordmark:** TotalRecalls in Paper, around 56–64px tall
- **Headline:** Inter Bold, Paper, around 88–100px
- **Subline:** Inter Regular, Mist, around 36–40px
- **Evidence line:** IBM Plex Mono, Steel Blue, around 28–32px

**Right side of the safe area (optional proof visual):**

- A cropped, simplified product visual: a folder with file rows showing `.md` and `.json` chips, or a real TotalRecalls screenshot on a Graphite card with a 1px Slate border.
- Keep it to about 35% of the safe area's width so the text stays dominant.

### 2.4 Banner Copy Options

Pick one headline and keep it for at least three months. Changing the banner often weakens recognition.

| Option              | Headline                       | Subline                                                   | Evidence Line              |
| ------------------- | ------------------------------ | --------------------------------------------------------- | -------------------------- |
| **A (recommended)** | Your AI chats. Your PC.        | Save ChatGPT, Claude, and 6 more AI tools as local files. | `C:\TotalRecalls\Library\` |
| **B**               | Keep the AI work that matters. | A local, searchable library for your AI conversations.    | `.MD · .JSON · OFFLINE`    |
| **C**               | One folder. Every AI chat.     | 8 AI tools, saved to your own Windows PC.                 | `8 PROVIDERS → 1 LIBRARY`  |

**Amber use:** Highlight a single word at most, such as "**Your PC.**" in Archive Amber. Alternatively, keep all text in Paper and use Amber only for one small chip.

### 2.5 What to Leave Off the Banner

- **Prices.** The $24 launch price will change. Put pricing in video end screens, descriptions, and pinned comments, where it's easy to update.
- **Upload schedule**, unless you're sure you can keep it.
- **Provider logos.** Name providers in text only.
- **The URL.** YouTube shows your channel links in the header, so a URL on the banner is redundant and gets cropped on mobile.
- **Arrows pointing to the Subscribe button.** They clash with the calm tone.

### 2.6 Header Links and Details

Set these in YouTube Studio under **Customization → Basic info**:

- **Primary link:** totalrecalls.app, labeled "Try TotalRecalls free"
- **Secondary link (optional):** Download or FAQ page
- **Channel description, first line:** Put the promise up front, since it shows in the header preview. For example: "TotalRecalls saves your AI chats to your own Windows PC as searchable Markdown and JSON files."

---

## 3. Channel Icon (Profile Picture)

### 3.1 Specs

| Item            | Spec                                                                                                  |
| --------------- | ----------------------------------------------------------------------------------------------------- |
| **Upload size** | 800 × 800px                                                                                           |
| **Display**     | Cropped to a circle, shown as small as about 98 × 98px, and far smaller beside comments and in search |
| **File size**   | 4MB or smaller                                                                                        |
| **Format**      | PNG                                                                                                   |

### 3.2 Design

The icon has to work at thumbnail-in-a-comment size. That means one shape, high contrast, and no text beyond one or two letters.

**Recommended build:**

- **Background:** Solid Obsidian `#111315`, filling the full square
- **Mark:** The TotalRecalls symbol simplified to a single line-style folder, built on the brand's icon style (rounded joins, even stroke), in Archive Amber `#C88A2B`
- **Size:** The mark fills about 50–55% of the circle's diameter, centered
- **Stroke weight:** Thicken the stroke well beyond the 1.5px UI spec. At 800px, use around 40–48px so the shape survives tiny sizes.

**Alternative:** A "TR" monogram in Inter Bold, Paper, with a small Amber folder tab above the letters. Use this only if the folder mark doesn't read clearly when tested small.

### 3.3 Icon Rules

- **Keep a clear circle margin.** Nothing important within 80px of the square's edges, because the circular crop removes the corners.
- **No full wordmark.** "TotalRecalls" becomes unreadable in a circle this small.
- **No founder photo as the channel icon.** The channel represents the product. The founder appears in videos and on the Founder Notes playlist.
- **Match the app.** If the app's Windows icon uses a different mark, align them. Viewers should recognize the same symbol on YouTube, the website, and their taskbar.

### 3.4 Test Before You Upload

1. Export the icon at 800 × 800px.
2. Shrink a copy to 48px and 24px.
3. Place both on a dark background and a light background, since viewers use both YouTube themes.
4. If the folder shape turns into a blob at 24px, thicken the stroke or simplify the shape.

---

## 4. Thumbnail Design System

### 4.1 Specs

| Item              | Spec                                                                               |
| ----------------- | ---------------------------------------------------------------------------------- |
| **Size**          | 1280 × 720px (16:9)                                                                |
| **File size**     | Under 2MB                                                                          |
| **Format**        | JPG or PNG                                                                         |
| **Safe margin**   | 40px on all sides                                                                  |
| **Reserved area** | Bottom-right corner, about 200 × 90px, where YouTube places the video length stamp |

### 4.2 The Master Grid

Every thumbnail uses the same underlying grid, so the channel page looks like a tidy, indexed shelf.

```
┌────────────────────────────────────────────────┐
│ [SERIES CHIP]                                  │  ← top-left, 40px in
│                                                │
│  HEADLINE                     [FOCAL ELEMENT]  │
│  3–5 WORDS                    face, folder,    │
│  one amber word               or app screen    │
│                                                │
│ [FILE PATH / EVIDENCE CHIP]        [KEEP CLEAR]│  ← bottom-left / bottom-right
└────────────────────────────────────────────────┘
```

| Element             | Position                       | Spec                                                                                                                  |
| ------------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| **Series chip**     | Top-left, 40px from edges      | IBM Plex Mono Medium, 32–36px, uppercase, Steel Blue text on Slate, 6px radius (scaled up to about 12px at this size) |
| **Headline**        | Left half, vertically centered | Inter Bold, 120–160px, Paper, tight line height (1.0–1.05), 2 lines maximum                                           |
| **Amber word**      | Inside the headline            | One word only, in Archive Amber                                                                                       |
| **Focal element**   | Right 45% of the frame         | One subject only                                                                                                      |
| **Evidence chip**   | Bottom-left, 40px from edges   | IBM Plex Mono, 32–40px, Steel Blue, such as `C:\TotalRecalls\Library\` or `.MD · .JSON`                               |
| **Keep-clear zone** | Bottom-right                   | No text, chips, or faces                                                                                              |

### 4.3 Typography in Thumbnails

**The rule still applies: sans for meaning, mono for evidence.**

- **Inter Bold** carries the headline. Always uppercase or strong sentence case, chosen once and used on every thumbnail. Uppercase is recommended for readability at small sizes.
- **IBM Plex Mono** carries proof: file paths, file types, series numbers, and counts.
- **Word count:** 3–5 words in the headline. If it needs more, the idea isn't sharp enough yet.
- **Don't repeat the title.** The thumbnail headline should add to the video title, not copy it. If the title is "How to Save Your ChatGPT Chats as Local Files," the thumbnail might read "YOUR CHATS. **LOCAL.**"
- **No outlines, drop shadows, or gradient text.** Contrast comes from Paper on Obsidian, which is already very strong.

### 4.4 Backgrounds

- **Default:** Solid Obsidian `#111315`
- **With a card:** Obsidian background with a Graphite `#1A1D21` panel behind the focal element, 1px Slate border
- **Texture (optional):** A faint folder grid in Slate at 4–6% opacity. Use the same texture on the banner so the channel feels connected.
- **Problem-focused videos:** You may add a subtle cool Steel Blue tint to the focal element, matching the "problem" grade used in videos. Keep the background Obsidian.
- **Never:** Busy photos, bright colors, blurred screenshots of provider interfaces, or gradients

### 4.5 Recurring Motifs

These small details make thumbnails recognizably TotalRecalls:

| Motif               | How to Use It                                                                   |
| ------------------- | ------------------------------------------------------------------------------- |
| **File path**       | `C:\TotalRecalls\Library\chatgpt\` in mono, Steel Blue, as the evidence chip    |
| **File-type chips** | `.MD` and `.JSON` side by side                                                  |
| **Saved chip**      | `● SAVED LOCALLY` in Local Green, only when the video shows a completed save    |
| **Folder shape**    | The same line-style folder from the channel icon, used large as a focal element |
| **Series number**   | `EP 06 / 10` or `GUIDE · CLAUDE` in the top-left chip                           |

Use **one or two motifs per thumbnail**, not all of them.

### 4.6 Thumbnail Templates

Build these four templates once, then duplicate them for every video.

#### Template 1: Founder

**Best for:** Founder story videos, opinion pieces, Shorts series openers

- Founder photo on the right, from mid-chest up, looking at the camera or toward the headline
- Calm, confident expression. A small half-smile or raised eyebrow fits the dry tone. No shocked faces.
- Background removed, with the founder placed on Obsidian and lit neutrally
- Headline on the left, evidence chip bottom-left

**Example:**

- Chip: `FOUNDER NOTES`
- Headline: "WHY I BUILT **THIS**"
- Evidence: `C:\TotalRecalls\`

#### Template 2: Product Proof

**Best for:** Tutorials, provider guides, feature walkthroughs

- A real TotalRecalls screenshot or File Explorer view on a Graphite card, on the right
- Crop tightly to one readable detail, such as a folder filling with `.md` files
- Slight 8–12px corner radius and 1px Slate border on the screenshot
- Blur any account names or personal details

**Example:**

- Chip: `GUIDE · CHATGPT`
- Headline: "SAVE EVERY **CHAT**"
- Evidence: `.MD · .JSON`

#### Template 3: Concept

**Best for:** Local-first explainers, privacy, ownership, "why it matters" videos

- One large line-style icon on the right: folder, lock, desktop monitor, or provider nodes merging into one point
- Icon in Paper or Mist, with one part in Archive Amber (for example, the folder tab)
- No photo, no screenshot

**Example:**

- Chip: `WHY LOCAL-FIRST`
- Headline: "WHO OWNS YOUR **CHATS**?"
- Evidence: `NO CLOUD · NO ACCOUNT`

#### Template 4: Before and After

**Best for:** Comparison videos and export-problem explainers

- Split the right side into two stacked or side-by-side panels
- Left or top panel: abstract "messy" graphic, such as a wall of bracketed raw text in Steel Blue, slightly desaturated
- Right or bottom panel: a clean Markdown file or organized folder
- Thin 1px Slate divider between them. No red X, no green check overlay.

**Example:**

- Chip: `EXPORTS, EXPLAINED`
- Headline: "RAW ZIP VS **READABLE**"
- Evidence: `.JSON → .MD`

### 4.7 Series Consistency

For the 10-video series, add a consistent episode marker:

- Chip text: `EP 01 / 10` through `EP 10 / 10`
- Same position, size, and color on every episode
- The chip is the only thing that changes position-wise. Headline and focal element change by topic.

When all 10 appear in a row on the channel page, they should look like labeled files in the same drawer.

### 4.8 Shorts Cover Frames

Shorts use a vertical cover frame, not a standard 1280 × 720 thumbnail, and YouTube's options for custom Short covers vary by upload method. Plan for it in the edit:

- **Pick a designed cover frame.** Choose a clean frame from the video in the YouTube app when uploading, or place a still title card in the first half-second of the edit so it's available to select.
- **Canvas:** 1080 × 1920px
- **Text zone:** Keep the headline in the vertical center of the frame. Shorts shelves often crop to a near-square or 4:5 view, so text near the top or bottom may disappear.
- **Style:** Same rules as thumbnails. Obsidian background or founder shot, Inter Bold headline, one Amber word, one mono chip.
- **Loop-friendly scripts:** If a Short opens on a founder pose, pick a cover frame from a different moment so the cover doesn't spoil the hook.

### 4.9 Thumbnail Checklist

Before uploading, confirm every item:

- [ ] 1280 × 720px, under 2MB
- [ ] 3–5 headline words, Inter Bold
- [ ] One Amber word maximum
- [ ] One focal element
- [ ] One or two mono evidence details
- [ ] Bottom-right corner clear for the length stamp
- [ ] No provider logos or sharp provider interfaces
- [ ] No personal details visible in screenshots
- [ ] Readable at mobile size (see Section 9.3)
- [ ] Matches the template used for this video type

---

## 5. Playlist and Section Cover Art

### 5.1 How YouTube Handles This

YouTube's channel page is organized into **sections**, and most sections display a **playlist**. Sections themselves don't take uploaded artwork. The playlist shows the thumbnail of a video inside it, and where YouTube Studio allows it, you can choose which video's thumbnail represents the playlist.

The practical approach: **make each playlist's first or featured video carry a strong series-branded thumbnail**, so the playlist cover looks designed on the channel page.

### 5.2 Suggested Playlists and Their Visual Codes

Each playlist gets a fixed chip label and one recurring focal motif. Colors stay within the brand palette. Distinction comes from the label and motif, not from new colors.

| Playlist                 | Chip Label           | Recurring Motif                               | Purpose                                                 |
| ------------------------ | -------------------- | --------------------------------------------- | ------------------------------------------------------- |
| **Start Here**           | `START HERE`         | App screenshot, Download step                 | New viewers: what TotalRecalls does and how to try it   |
| **Provider Guides**      | `GUIDE · [PROVIDER]` | Folder labeled with the provider name in mono | One video per AI tool                                   |
| **Why Local-First**      | `WHY LOCAL-FIRST`    | Line icon: desktop monitor or lock            | Ownership, privacy, and portability explainers          |
| **Your Library at Work** | `LIBRARY`            | Markdown file open, or search result          | Using saved chats for research, reuse, and organization |
| **Founder Notes**        | `FOUNDER NOTES`      | Founder photo                                 | Build story, updates, honest lessons                    |
| **Shorts**               | `SHORT`              | Founder pose or single bold line              | Quick hooks and demos                                   |

### 5.3 Playlist Cover Card Design

If you create a dedicated cover for a playlist (for example, a short channel trailer or intro video that sits first in the list), use this layout:

- **Background:** Obsidian with a Graphite panel filling the right 45%
- **Top-left chip:** Playlist label in mono, Steel Blue on Slate
- **Headline:** The playlist name in Inter Bold, Paper, 130–150px
- **Evidence line:** A short mono detail, such as `8 PROVIDERS · 1 LIBRARY` or `EP 01–10`
- **Right panel:** The playlist's recurring motif, large and centered

### 5.4 Section Order on the Channel Page

Arrange sections under **Customization → Layout** in this order:

1. **Channel trailer** (for non-subscribers): the clearest, shortest product explanation you have
2. **Featured video** (for returning subscribers): the newest main upload
3. **Start Here** playlist
4. **Provider Guides** playlist
5. **Why Local-First** playlist
6. **Shorts**
7. **Your Library at Work** playlist
8. **Founder Notes** playlist

This order moves visitors from "What is this?" to "Does it work with my AI tool?" to "Why should I trust it?"

---

## 6. Watermark and Logo Placement

### 6.1 YouTube Branding Watermark

YouTube lets you add a watermark that appears on every video. Viewers on desktop can click it to subscribe.

| Item            | Spec                                                        |
| --------------- | ----------------------------------------------------------- |
| **Upload size** | 150 × 150px minimum; square                                 |
| **File size**   | Under 1MB                                                   |
| **Format**      | PNG with transparency                                       |
| **Placement**   | Fixed by YouTube, bottom-right of the player                |
| **Setup**       | YouTube Studio → Customization → Branding → Video watermark |

**Design:**

- Use the channel icon mark: the Amber line-folder on an Obsidian circle
- Keep the Obsidian circle solid, not transparent, so the mark stays readable over bright screen recordings
- Don't use the full wordmark. It's too small to read.

**Display timing:** Choose **"Entire video"** for tutorials and guides, where viewers are most likely to want more. If it distracts during screen recordings, switch to **"Custom start time"** and begin it after the first 30 seconds, once the hook has landed.

### 6.2 In-Video Logo Use

Because YouTube's watermark already sits in the bottom-right, avoid adding a second burned-in logo.

| Moment               | Logo Treatment                                                                                                              |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Opening seconds**  | No logo. Start cold on the first spoken word or the first action.                                                           |
| **During the video** | No burned-in logo. Let the watermark do the work.                                                                           |
| **Lower thirds**     | Founder name in Inter Semibold, role in IBM Plex Mono. No logo needed.                                                      |
| **End screen**       | Wordmark in Paper, small, centered or top-left of the end card                                                              |
| **Shorts**           | No watermark appears on Shorts. Place a small wordmark on the final CTA frame only, clear of the right-side action buttons. |

### 6.3 End Screen Template

End screens run for the final 5–20 seconds of a long-form video. Build one 1920 × 1080px template and reuse it.

```
┌──────────────────────────────────────────────────────┐
│ TotalRecalls (wordmark, small)                        │
│                                                      │
│   ┌──────────────┐        ┌──────────────┐           │
│   │  NEXT VIDEO  │        │  PLAYLIST    │  (●)      │
│   │  (element)   │        │  (element)   │ Subscribe │
│   └──────────────┘        └──────────────┘           │
│                                                      │
│   [ Try it free ]  Windows app — visit from desktop  │
│   totalrecalls.app                                   │
└──────────────────────────────────────────────────────┘
```

- **Background:** Obsidian, with faint folder-grid texture if you use it elsewhere
- **Video and playlist elements:** Two placeholders, framed with 1px Sl
