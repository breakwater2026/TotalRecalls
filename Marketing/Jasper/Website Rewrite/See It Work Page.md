# TotalRecalls See It Work Page

**Page URL:** `/see-it-work/` (confirm against the current route)\
**Page goal:** Show one real ChatGPT download from start to finish so visitors trust that the app works as described. Then send them to a free download.\
**Primary keyword:** save ChatGPT chats to your PC\
**Secondary terms:** TotalRecalls demo, download ChatGPT conversations, ChatGPT to Markdown, local AI chat archive

**Meta title:** See It Work: Save a ChatGPT Chat to Your PC in One Minute | TotalRecalls\
**Meta description:** Watch a real ChatGPT conversation download to a Windows PC as Markdown and JSON files. One complete workflow, captioned, with no mockups.

---

## Page Copy

### 1. Hero

`SEE IT WORK`

# Watch a ChatGPT chat become files on your PC.

This page shows one complete download, recorded on a Windows 11 PC. A ChatGPT conversation starts in the sidebar and ends as two files in a folder on the drive. Nothing is mocked up.

`ABOUT 60 SECONDS` · `CAPTIONED` · `FREE TIER`

**Tertiary link:** Skip to the download ↓

---

### 2. The Demo

*Anchor: `id="demo"`*

`THE DEMO`

## One conversation, start to finish

Recorded on the Free Tier. Captions explain each step, so the video works with the sound off.

**\[Video embed: ChatGPT download workflow, about 60 seconds]**

Real screen recording, trimmed for length. Account details are blurred.

[Read the transcript →](#transcript)

---

### 3. What You're Seeing

*Anchor: `id="steps"`*

`STEP BY STEP`

## What happens in the video

**0:00 · Open the app**\
TotalRecalls runs from its own folder on your PC. There's no installer and no TotalRecalls account.

**0:08 · Choose ChatGPT**\
The provider list shows what your tier includes. ChatGPT is part of the Free Tier.

**0:15 · Sign in to ChatGPT**\
You sign in inside the app, on your own PC. Your conversations aren't sent to our servers.

**0:27 · Pick a conversation**\
Your ChatGPT history loads as a list. Select the thread you want to keep.

**0:36 · Download**\
TotalRecalls saves the conversation. A confirmation shows exactly where the files went.

**0:45 · Open the Library folder**\
The chat sits in the `chatgpt` subfolder as one Markdown file and one JSON file. The video ends with the Markdown file open in Notepad.

---

### 4. The Result

*Anchor: `id="result"`*

`THE RESULT`

## What's on your drive afterward

**\[Screenshot: File Explorer open to `C:\TotalRecalls\Library\chatgpt\`, with the Markdown file open in Notepad beside it]**

**① The folder**\
One Library, with a subfolder for each provider.

**② The Markdown file**\
The full conversation in readable text, with headings and code blocks intact.

**③ The JSON file**\
The same chat as structured data, ready for search or other tools.

These files open without TotalRecalls. Copy them, back them up, or search them like any other document on your PC.

`C:\TotalRecalls\Library\chatgpt\2026-09-14-pricing-research.md` · `.MD` · `.JSON` · `● SAVED LOCALLY`

---

### 5. Try It Yourself

*Anchor: `id="download"`*

`TRY IT YOURSELF`

## Run the same download on your own chats

The Free Tier includes ChatGPT, Claude, and Perplexity, with up to 5 conversations each. You don't need a card or an account.

- **Primary CTA:** Download free

Windows 10 and 11. Windows may show a SmartScreen prompt the first time you open the app. [What it means →](/smartscreen/)

---

### 6. Pricing Link

Want every provider and no download cap?\
**Tertiary link:** Compare Free and Pro →

---

### Transcript

*Anchor: `id="transcript"`. Collapsed by default.*

**Show transcript**

*(Paste the final caption text here once the video is locked.)*

**Visible word count:** About 540 words, including chips, step labels, and links. The transcript is collapsed and not counted.

---

## Layout

1. **Hero:** Left-aligned eyebrow, H1, and intro, capped at 680px. Chip row below, then the "Skip to the download" link. No button in the hero.
2. **Demo:** Heading block capped at 680px. The video sits below at full content width (max 960px) in a 16:9 frame. The caption line and transcript link sit directly under the frame.
3. **Step by step:** Six steps in a vertical list, capped at 720px. On desktop, timestamps sit in a narrow left column (72px) and text sits on the right. On mobile, the timestamp stacks above each title.
4. **The result:** Screenshot at full content width (max 960px) with three numbered markers placed on the image. The matching ①②③ notes sit below in a three-column row on desktop, stacked on mobile. The closing line and evidence strip follow.
5. **Try it yourself:** Graphite band with heading, line, the single primary button, and microcopy.
6. **Pricing link:** One centered line below the band, on Obsidian.
7. **Transcript:** Accordion at the bottom of the page, collapsed by default.

---

## Implementation Spec

| Element              | Copy                                          | Style                                                                                                                                                                          |
| -------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Page background      | —                                             | Obsidian `#111315`. Hero padding 128px desktop / 64px mobile. Sections 96px / 64px.                                                                                            |
| Eyebrows             | SEE IT WORK, etc.                             | IBM Plex Mono Medium 12px, uppercase, +0.12em, Steel Blue `#7A8FA6`                                                                                                            |
| H1                   | Watch a ChatGPT chat become files on your PC. | Inter Bold 48px / 34px, 1.1 line height, −0.02em, Paper `#F3EFE7`                                                                                                              |
| H2                   | Section headings                              | Inter Semibold 36px / 28px, 1.15 line height, Paper                                                                                                                            |
| Intros               | Hero and section intros                       | Inter Regular 20px / 18px, 1.55 line height, Mist `#D9D4CB`, max 680px                                                                                                         |
| Body text            | Step and result copy                          | Inter Regular 16px, 1.6 line height, Mist                                                                                                                                      |
| Hero chips           | 3 chips                                       | `mono-sm` 12px, Dust `#B5AEA3` on Slate `#2A2F36`, 6px radius                                                                                                                  |
| Skip link            | Skip to the download ↓                        | Tertiary: Inter Semibold 15px, Steel Blue, smooth-scrolls to `#download`                                                                                                       |
| Video frame          | —                                             | 16:9, max 960px, 12px radius, 1px Slate border, Graphite `#1A1D21` letterbox                                                                                                   |
| Poster frame         | —                                             | Still of the finished Library folder (the end state), not the app's opening screen. No overlay text.                                                                           |
| Play button          | —                                             | 64px circle, Paper icon on Obsidian at 80% opacity. Not Amber.                                                                                                                 |
| Video caption        | Real screen recording…                        | `body-sm` 14px, Dust                                                                                                                                                           |
| Transcript link      | Read the transcript →                         | Tertiary, Steel Blue. Opens and scrolls to the transcript accordion.                                                                                                           |
| Timestamps           | 0:00, 0:08, etc.                              | IBM Plex Mono Medium 14px, Steel Blue. Clicking one seeks the video and scrolls back to it.                                                                                    |
| Step titles          | Open the app, etc.                            | Inter Semibold 18px, Paper                                                                                                                                                     |
| Step dividers        | —                                             | 1px Slate between steps, 20px vertical padding per step                                                                                                                        |
| Inline code          | `chatgpt`                                     | IBM Plex Mono 14px, Steel Blue, Graphite fill, 4px radius                                                                                                                      |
| Screenshot           | Library folder + Notepad                      | Max 960px, 12px radius, 1px Slate border. Real capture at 2x resolution. Alt text describes the folder path and both files.                                                    |
| Screenshot markers   | ① ② ③                                         | 24px circles, Steel Blue fill, Obsidian numerals, IBM Plex Mono Medium 12px                                                                                                    |
| Marker notes         | The folder, etc.                              | Number and title in Inter Semibold 16px, Paper. Body in Mist.                                                                                                                  |
| Evidence strip       | Path + chips                                  | Path in mono 14px, Steel Blue, selectable. File chips in Steel Blue with 1px Slate border. `SAVED LOCALLY` in Local Green `#5E8A68`. Sits on Obsidian between 1px Slate rules. |
| CTA band             | —                                             | Graphite, 1px Slate top border, 96px vertical padding                                                                                                                          |
| Primary CTA          | Download free                                 | Large, 48px, Archive Amber `#C88A2B` fill, Obsidian text, 8px radius, links to `/download/`. **The only Amber element on the page.**                                           |
| CTA microcopy        | Windows 10 and 11…                            | `body-sm` 14px, Dust. SmartScreen link in Steel Blue, links to `/smartscreen/`.                                                                                                |
| Pricing line         | Want every provider…                          | `body` 16px, Mist                                                                                                                                                              |
| Pricing link         | Compare Free and Pro →                        | Tertiary: Inter Semibold 15px, Steel Blue, no border, links to `/pricing/#compare`                                                                                             |
| Transcript accordion | Show transcript                               | Chevron, 150ms ease-out, 1px Slate dividers. Text in `body` Mist, max 720px.                                                                                                   |

### Spacing

| Gap                           | Value                      |
| ----------------------------- | -------------------------- |
| Eyebrow → heading             | 12px                       |
| Heading → intro               | 16px                       |
| Intro → chip row              | 24px                       |
| Chip row → skip link          | 16px                       |
| Heading block → video         | 32px                       |
| Video → caption               | 12px                       |
| Caption → transcript link     | 8px                        |
| Heading block → steps         | 48px                       |
| Screenshot → marker notes     | 32px                       |
| Marker notes → closing line   | 32px                       |
| Closing line → evidence strip | 24px                       |
| Band line → primary CTA       | 24px                       |
| CTA → microcopy               | 12px                       |
| CTA band → pricing line       | 48px                       |
| Between sections              | 96px desktop / 64px mobile |

### Behavior

- **No autoplay.** The video plays only when clicked. Load the player lazily, with the poster frame as a static image until then.
- **Captions on by default.** Use a burned-in caption track or a default-on WebVTT track. The video must make sense muted.
- **Player controls:** Native or minimal controls. No related-video end screens, no sticky floating player.
- **Clickable timestamps:** Each timestamp seeks the video to that point. If the player doesn't support seeking, render timestamps as plain text.
- **Static page.** No fade-ins, counters, or scroll-triggered animation. This page is evidence, so everything appears immediately.
- **One Amber element.** Only the "Download free" button uses Archive Amber. The play button, markers, and chips stay neutral.
- **Mobile:** Keep the video inline at full width. Under the primary CTA, replace the microcopy with *"Windows app. Visit from your desktop to download."* in `body-sm`, Dust.
- **Icons:** None beyond the play button and accordion chevron. No provider logos, no shields, no cloud icons.
- **Deep links:** Keep `id="demo"`, `id="steps"`, `id="result"`, `id="download"`, and `id="transcript"` for support replies and social posts.
- **Accessibility:** Provide a full transcript, a descriptive `title` on the video iframe, and alt text on the screenshot naming the path and both file types.

---

## Accuracy Checks Before Publishing

- **Timestamps.** The six timestamps are placeholders. Match them to the final cut before launch, and update them whenever the video is re-edited.
- **"Nothing is mocked up."** Only keep this line if the video and screenshot are real captures of the current build. If any screen is recreated, remove the line.
- **"Trimmed for length."** If the recording cuts out loading time, keep this caption so the demo doesn't imply faster speeds than users will see.
- **Sign-in screen.** Blur the email, password field, and profile image. Never show a real session token or license key.
- **Conversation content.** Use a non-sensitive demo thread. The filename `2026-09-14-pricing-research.md` must match what's shown in the video and screenshot.
- **Folder path.** `C:\TotalRecalls\Library\chatgpt\` and the filename pattern must match the current build exactly.
- **"No installer."** Confirm the app still ships as a portable unzip-and-run build. Change the step if an installer is added.
- **"Up to 5 conversations each."** The live site says "per download." Confirm the build, then match the Pricing, Legals, and homepage wording.
- **Privacy wording.** Keep "aren't sent to our servers." Downloads connect directly to ChatGPT, so never write "never touches the internet."
- **Headings and code blocks intact.** Confirm the Markdown output preserves both for the demo thread before publishing that claim.
- **Windows version.** The hero says the demo was recorded on Windows 11. Change it if the recording machine runs Windows 10.
- **Re-record trigger.** If ChatGPT's sign-in flow or the TotalRecalls interface changes visibly, re-record the demo so the page stays literal.
