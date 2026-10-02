# TotalRecalls 3 Card Section

## Section Copy

**Eyebrow**\
`WHY OWN YOUR AI CHATS`

**Section Headline**

## Your best thinking deserves a better home than a sidebar.

**Intro**\
Your AI chats hold research, drafts, code, and decisions. When you own your AI chats, that work lives on your own PC as files you control.

---

**Card 1: Find it again.**\
A saved file is one quick search away, not 400 threads down a sidebar.\
`SEARCHABLE · LOCAL FILES`

**Card 2: Keep it through redesigns.**\
A Markdown file opens the same way in Notepad next year, whatever the chat interface looks like.\
`.MD + .JSON`

**Card 3: Take it anywhere.**\
Copy the folder to a new PC or a backup drive, and your library comes with you, no login needed.\
`COPY FOLDER · NO LOGIN`

---

**Evidence Strip**\
`C:\TotalRecalls\Library\claude\2026-07-28-refactor-plan.md` · `● SAVED LOCALLY`

**Closing Line**\
Start free with ChatGPT, Claude, and Perplexity, 5 conversations each. Pro unlocks all 8 providers for $24 one-time (launch price).

**CTAs**

- **Primary:** Download free
- **Tertiary:** Compare Free and Pro →

**Visible word count:** About 125 words, including chips and CTAs

---

## Layout

1. **Header block:** The eyebrow, headline, and intro are left-aligned and stacked. The intro is capped at 680px.
2. **Card row:** Three equal-width, equal-height cards in one row on desktop. They stack into a single column on tablet and mobile.
3. **Evidence strip:** One static row directly on Obsidian, framed by 1px Slate rules above and below.
4. **Close:** The closing line and CTAs are left-aligned at the bottom of the section.

---

## Implementation Spec

| Element            | Copy                                                            | Style                                                                                                                                          |
| ------------------ | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Section background | —                                                               | Obsidian `#111315`, 96px vertical padding desktop / 64px mobile                                                                                |
| Eyebrow            | WHY OWN YOUR AI CHATS                                           | IBM Plex Mono Medium, 12px, uppercase, +0.12em tracking, Steel Blue `#7A8FA6`                                                                  |
| Headline           | Your best thinking deserves…                                    | `h2`: Inter Semibold, 36px desktop / 28px mobile, 1.15 line height, −0.01em, Paper `#F3EFE7`                                                   |
| Intro              | Your AI chats hold research…                                    | `body-lg`: Inter Regular, 20px / 18px, 1.55 line height, Mist `#D9D4CB`, max 680px                                                             |
| Card               | —                                                               | Graphite `#1A1D21` fill, 1px Slate `#2A2F36` border, 12px radius, 24px padding, no shadow, no hover state                                      |
| Card lead          | Find it again. / Keep it through redesigns. / Take it anywhere. | `h4`: Inter Semibold, 18px desktop / 17px mobile, 1.35 line height, Paper                                                                      |
| Card follow-up     | One sentence                                                    | `body`: Inter Regular, 16px, 1.6 line height, Mist                                                                                             |
| Card chip          | e.g., `.MD + .JSON`                                             | `mono-sm`: IBM Plex Mono Medium, 12px, uppercase, +0.02em, Steel Blue text on Slate fill, 6px radius, 4px × 8px padding, pinned to card bottom |
| File path chip     | C:\TotalRecalls\Library\claude\…                                | `mono`: IBM Plex Mono Regular, 14px desktop / 13px mobile, Steel Blue, selectable                                                              |
| Local chip         | ● SAVED LOCALLY                                                 | `mono-sm`, Local Green `#5E8A68` text and dot, transparent fill, 1px Slate border, 6px radius. The section's only green element.               |
| Strip rules        | —                                                               | 1px Slate top and bottom borders, 16px vertical padding                                                                                        |
| Closing line       | Start free with…                                                | `body`: Inter Regular, 16px, Mist. Tabular figures for "5," "8," and "$24."                                                                    |
| Primary CTA        | Download free                                                   | Default button, 40px height, Archive Amber `#C88A2B` fill, Obsidian text, 8px radius, links to `/download/`. The section's only Amber element. |
| Tertiary CTA       | Compare Free and Pro →                                          | Inter Semibold, 15px, Steel Blue, no border, links to `/pricing/#compare`                                                                      |

### Spacing

| Gap                       | Value        |
| ------------------------- | ------------ |
| Eyebrow → headline        | 12px         |
| Headline → intro          | 16px         |
| Intro → card row          | 48px         |
| Between cards             | 24px         |
| Lead → follow-up          | 8px          |
| Follow-up → chip          | 16px minimum |
| Card row → evidence strip | 48px         |
| Strip → closing line      | 32px         |
| Closing line → CTAs       | 16px         |
| Between CTAs              | 16px         |

### Behavior

- **Static by default.** No carousel, ticker, or looping motion.
- **Optional reveal:** Cards fade in with an 8px upward slide over 200ms, staggered 60ms apart, triggered once on scroll. Disable under `prefers-reduced-motion`.
- **Mobile file path:** Wrap at backslashes or truncate the middle (`C:\TotalRecalls\…\2026-07-28-refactor-plan.md`). Never shrink mono text below 12px.
- **Icons:** Optional 24px line icons in Mist (magnifying glass, file with lines, folder). No cloud, shield, or lock icons.

---

## Accuracy Checks

- **No cloud icons.** Don't use cloud imagery, even with a strike-through, in this section. The file path and local chip carry the message.
- **Windows only.** "Your own PC" means Windows 10 or 11. Don't add Mac or Linux icons. If the section stands alone outside the homepage, add a small `WINDOWS 10/11` chip to the header.
- **Free Tier limits.** ChatGPT, Claude, and Perplexity, 5 conversations each. Confirm this matches the current build and the rest of the site.
- **Launch price label.** Keep "(launch price)" beside $24. Update the closing line when the launch price ends.
- **"No login needed" refers to the files.** Copied Markdown and JSON files open without any account. The Pro app itself allows up to three device activations, so don't write "install on unlimited PCs."
- **Search claim.** Card 1 says "one quick search away" on purpose. Only name Windows Search if saved files in the Library folder are indexed by default.
- **Folder path.** `C:\TotalRecalls\Library\` and the `claude\` subfolder must match the current build exactly.
- **Chip contrast.** Steel Blue on Slate sits close to the 4.5:1 AA line at 12px. Verify it in the browser. If it falls short, switch card chips to a transparent fill with a 1px Slate border on an Obsidian well.
- **Privacy point.** The former fourth point ("Keep it private") is covered by the hero trust strip. If this section runs without the hero, add "not sent to our servers" to the intro rather than a fourth card.
