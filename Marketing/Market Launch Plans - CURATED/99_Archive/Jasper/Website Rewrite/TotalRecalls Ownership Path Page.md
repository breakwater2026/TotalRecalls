# TotalRecalls Ownership Path Page

**Page URL:** `/ownership/` (confirm against the current route for the Ownership Path page)\
**Page goal:** Show the journey from scattered AI chats to a local library you keep, then send readers to a free download or to the pricing page.\
**Primary keyword:** own your AI chat history\
**Secondary terms:** local AI chat archive, save AI chats locally, AI chat backup, Markdown and JSON, portable AI chat library

**Meta title:** The Ownership Path: From Scattered AI Chats to a Library You Keep | TotalRecalls\
**Meta description:** Move your ChatGPT, Claude, and six more AI chats out of scattered sidebars and into plain files on your own Windows PC. Private, portable, and yours to keep.

---

## Page Copy

### 1. Hero

`THE OWNERSHIP PATH`

# From scattered chats to a library you keep.

Right now, your AI work is spread across eight different sidebars. Each one has its own search, its own layout, and its own rules. TotalRecalls moves that work into one folder on your PC, where it follows your rules instead.

- **Primary CTA:** Download free
- **Tertiary CTA:** Compare Free and Pro →

`WINDOWS 10/11` · `NO ACCOUNT` · `LOCAL FILES`

---

### 2. The Path

*Anchor: `id="path"`*

`FOUR STAGES`

## Where your chats are now, and where they can be

**01 · Scattered**\
Your chats live inside each AI tool. You find old threads by scrolling, and you hope the interface still works the way you remember.\
`8 SIDEBARS · 8 SEARCH BOXES`

**02 · Saved**\
Each conversation becomes a Markdown file and a JSON file on your own drive. The copy is yours, separate from the provider's app.\
`.MD + .JSON`

**03 · Organized**\
Every provider gets its own subfolder inside one Library. Your ChatGPT research and your Claude drafts finally sit side by side.\
`C:\TotalRecalls\Library\`

**04 · Kept**\
Your files open with the tools you already use. Back them up, move them to a new PC, or open them years from now. They don't depend on a login.\
`COPY · BACK UP · OPEN ANYWHERE`

---

### 3. Sidebar vs Library

`THE DIFFERENCE`

## A chat app shows you your history. A folder lets you keep it.

|                                | In the chat app                   | In your Library               |
| ------------------------------ | --------------------------------- | ----------------------------- |
| **Finding an old thread**      | Scroll, or trust one app's search | Search every provider at once |
| **When the interface changes** | Old chats can get harder to reach | Files open the same way       |
| **Switching AI tools**         | Your history stays behind         | Your history comes with you   |
| **Changing PCs**               | Sign in and hope it's all there   | Copy one folder               |
| **Who holds the copy**         | The provider                      | You                           |

**Takeaway:** Providers are good at running AI. Your own drive is a better place to keep what you made with it.

---

### 4. Why Plain Files Last

`LONG-TERM ACCESS`

## Formats that outlive the apps that made them

Markdown is plain text with light formatting. JSON is plain structured data. Neither one needs special software or a subscription to open.

- **Readable today.** Open any chat in Notepad, VS Code, or your favorite notes app.
- **Readable later.** Plain text has stayed readable for decades. Your files don't rely on TotalRecalls staying installed.
- **Useful beyond reading.** Search, compare, or load your chats into other tools without asking anyone's permission.

`claude\2026-07-28-refactor-plan.md` · `● SAVED LOCALLY`

---

### 5. Private by Default

`YOUR DRIVE, YOUR FILES`

## What TotalRecalls does, and what it doesn't

**It does:**

- Run on your Windows PC
- Let you sign in to each AI provider locally, inside the app
- Save your chats to a folder you choose to keep

**It doesn't:**

- Send your conversations to our servers
- Ask you to create a TotalRecalls account
- Lock your files in a format only we can read

Downloading new chats connects directly to each provider, so it needs an internet connection. Once saved, your files open offline.

---

### 6. Questions About Ownership

`FAQ`

## What happens to my files?

**What if I stop using TotalRecalls?**\
Your files stay exactly where they are. They're ordinary Markdown and JSON, so any text editor can open them, with or without the app.

**Can I move my library to a new PC?**\
Yes. Copy the Library folder to the new machine or a backup drive. That's the whole move.

**Does Gemini work the same way?**\
Almost. Gemini history comes through Google Takeout, which TotalRecalls converts to Markdown and saves to the same Library.

**Do I own the files TotalRecalls creates?**\
The files live on your drive, and you control them. How you use each chat's content still follows each provider's own terms.

---

### 7. Final CTA

`START YOUR LIBRARY`

## Your first saved chat is a few minutes away.

Download TotalRecalls free, save your first conversations, and see your Library take shape. When you want every provider and no download cap, Pro is one payment.

- **Primary CTA:** Download free
- **Tertiary CTA:** Compare Free and Pro →

Windows 10 and 11. Visiting on mobile? Open totalrecalls.app on your desktop to download.

**Visible word count:** About 690 words, including chips, table, and CTAs

---

## Layout

1. **Hero:** Left-aligned eyebrow, H1, and intro, capped at 680px. CTA pair and chip row below.
2. **The Path:** Four stage cards in one row on desktop, joined by a thin Steel Blue connector line running left to right. Stacked vertically on mobile, with the connector running top to bottom.
3. **Sidebar vs Library:** One Graphite panel holding the comparison table. The "In your Library" column gets a subtle Obsidian well. Takeaway line below the panel.
4. **Why plain files last:** Single column, capped at 680px. List, then the evidence strip on Obsidian between 1px Slate rules.
5. **Private by default:** Two columns on desktop ("It does" / "It doesn't"), stacked on mobile. Connection note spans the width below.
6. **FAQ:** Accordion, collapsed by default.
7. **Final CTA:** Graphite band with headline, line, CTA pair, and microcopy.

---

## Implementation Spec

| Element              | Copy                                        | Style                                                                                                                                     |
| -------------------- | ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Page background      | —                                           | Obsidian `#111315`. Hero padding 128px desktop / 64px mobile. Sections 96px / 64px.                                                       |
| Eyebrows             | THE OWNERSHIP PATH, etc.                    | IBM Plex Mono Medium 12px, uppercase, +0.12em, Steel Blue `#7A8FA6`                                                                       |
| H1                   | From scattered chats to a library you keep. | Inter Bold 48px / 34px, 1.1 line height, −0.02em, Paper `#F3EFE7`                                                                         |
| H2                   | Section headings                            | Inter Semibold 36px / 28px, Paper                                                                                                         |
| Intros               | Hero and section intros                     | Inter Regular 20px / 18px, Mist `#D9D4CB`, max 680px                                                                                      |
| Primary CTA          | Download free                               | Large, 48px, Archive Amber `#C88A2B` fill, Obsidian text, 8px radius, links to `/download/`. One per screen.                              |
| Tertiary CTA         | Compare Free and Pro →                      | Inter Semibold 15px, Steel Blue, no border, links to `/pricing/`                                                                          |
| Stage cards          | 01–04                                       | Graphite `#1A1D21`, 1px Slate `#2A2F36` border, 12px radius, 24px padding, no hover                                                       |
| Stage numbers        | 01 · Scattered, etc.                        | Number in IBM Plex Mono Medium 14px, Steel Blue. Title in Inter Semibold 20px, Paper.                                                     |
| Stage 01 card        | Scattered                                   | Same card, but body text in Dust `#B5AEA3` to signal the "before" state. No red or alert styling.                                         |
| Stage chips          | e.g., `.MD + .JSON`                         | Mono 12px, Steel Blue, transparent fill, 1px Slate border, 6px radius, pinned to card bottom                                              |
| Connector line       | —                                           | 1.5px Steel Blue. Static, or drawn once over 600ms.                                                                                       |
| Comparison table     | Sidebar vs Library                          | `body-sm` 14px, Mist, 1px Slate dividers, 48px rows. Header in eyebrow style. No checkmarks or red X marks.                               |
| Takeaway             | Takeaway: …                                 | Inter Regular 16px, Paper. "Takeaway:" in Semibold.                                                                                       |
| Evidence strip       | File path + saved chip                      | Path in mono 14px, Steel Blue, selectable. `SAVED LOCALLY` in Local Green `#5E8A68`, directly on Obsidian. The page's only green element. |
| Does / doesn't lists | 3 + 3 items                                 | Inter Regular 16px, Mist. Mist check and dash icons, not green or red.                                                                    |
| FAQ                  | 4 items                                     | Accordion, chevron, 150ms ease-out, 1px Slate dividers                                                                                    |
| Final band           | —                                           | Graphite, 1px Slate top border, 96px vertical padding                                                                                     |
| Mobile microcopy     | Visiting on mobile?…                        | `body-sm` 14px, Dust                                                                                                                      |

### Behavior

- **Static by default.** Optional one-time 200ms fade-in per section, disabled under `prefers-reduced-motion`.
- **Icons:** Optional 24px line icons in Mist on stage cards (scattered pages, file, folder tree, arrows between drives). No cloud, shield, or lock icons. No provider logos.
- **Deep link:** Keep `id="path"` on the stages section for social and email links.

---

## Accuracy Checks Before Publishing

- **No pricing comparison.** This page mentions Pro once, in the final CTA. Keep tier details on `/pricing/`.
- **"Search every provider at once."** True for any desktop search across a single folder. Only name Windows Search if the Library folder is indexed by default.
- **"Plain text has stayed readable for decades."** Keep this about the format, not a promise about the app or updates.
- **Privacy wording.** Keep "not sent to our servers." Downloads connect to each provider, so never write "never touches the internet."
- **Content rights FAQ.** The last answer keeps users responsible for each provider's terms, which matches the Terms of Service. Keep it.
- **Folder path.** `C:\TotalRecalls\Library\` and the `claude\` subfolder must match the current build.
- **Gemini.** Always a Google Takeout conversion. Never a one-click download.
- **Platforms.** Windows 10 and 11 only. No Mac or Linux icons.
- **Distinct from the homepage.** Don't reuse "Files stay put" or "Your best thinking deserves a better home than a sidebar" here.
