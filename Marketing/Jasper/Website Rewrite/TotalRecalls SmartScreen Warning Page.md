# TotalRecalls SmartScreen Warning Page

**Page URL:** `/smartscreen/` (update every `/#smartscreen` link on the homepage to point here)\
**Page goal:** Help first-time installers understand the prompt, continue safely, and return to the download.\
**Primary keyword:** "Windows protected your PC"\
**Secondary terms:** SmartScreen warning, Microsoft Defender SmartScreen, More info, Run anyway, new Windows app

---

## Page Copy

### Hero

`SUPPORT · WINDOWS 10/11`

# "Windows protected your PC." Here's what that means for TotalRecalls.

When you first open TotalRecalls, Windows may show a blue "Windows protected your PC" prompt. It's a routine reputation check that Windows runs on new apps, and it takes two clicks to continue.

`WINDOWS 10/11` · `2 CLICKS` · `DOWNLOAD ONLY FROM TOTALRECALLS.APP`

[Skip to the steps ↓](#steps)

---

### What SmartScreen Is

`WHAT YOU'RE SEEING`

## A reputation check, not a verdict

Microsoft Defender SmartScreen is built into Windows 10 and 11. It looks at how many people have already downloaded and run an app. When an app is new, Windows hasn't seen it often enough to recognize it, so it pauses and asks you to confirm.

- **It measures familiarity.** SmartScreen asks, "Have enough people run this app yet?"
- **It doesn't scan for harm.** A new app and an unknown app look the same to this check.
- **It fades over time.** As more people install TotalRecalls, Windows builds reputation for it, and the prompt should appear less often.

TotalRecalls is a newly launched app, so you may see this prompt on your first launch.

---

### Not a Malware Warning

`THE SHORT ANSWER`

## This prompt doesn't mean Windows found a problem

"Windows protected your PC" is **not** a malware warning. It doesn't mean Windows found a virus, a threat, or anything harmful in TotalRecalls. It means the app is still new to Windows.

A real threat detection looks different. It comes from Microsoft Defender Antivirus and names a specific threat. If you ever see that kind of alert, don't run the file. Email us instead.

---

### How to Continue

*Anchor: `id="steps"`*

`HOW TO CONTINUE`

## Two clicks to open TotalRecalls

### 01 · Click "More info"

On the blue "Windows protected your PC" window, click the **More info** link under the message. This reveals the app name and a new button.

`LOOK FOR: APP NAME · TOTALRECALLS`

*\[Annotated screenshot: SmartScreen prompt with "More info" highlighted]*

### 02 · Click "Run anyway"

Check that the app name matches TotalRecalls, then click **Run anyway**. TotalRecalls opens, and you can pick your first provider.

`USUALLY ONCE PER DOWNLOADED FILE`

*\[Annotated screenshot: expanded prompt with "Run anyway" highlighted]*

Once you're in, everything runs on your own PC. Your chats save as Markdown and JSON files in your local Library folder.

`C:\TotalRecalls\Library\` · `● SAVED LOCALLY`

---

### Check Your Source

`BEFORE YOU CLICK RUN ANYWAY`

## Only run TotalRecalls downloaded from totalrecalls.app

SmartScreen can't tell a new app from a copied one. That part is up to you, and it takes a few seconds:

- **Check the address bar.** Download only from `totalrecalls.app`. We don't distribute TotalRecalls through file-sharing sites, app mirrors, or email attachments.
- **Check the file.** The file should come straight from the download button on our site, not from a link someone sent you.
- **Check the name.** After you click More info, the app name should read TotalRecalls.

If anything doesn't match, stop and email us before you run it.

`DOWNLOAD ONLY FROM TOTALRECALLS.APP`

---

### Common Questions

`FAQ`

## Questions about the SmartScreen prompt

### Why does Windows show this for TotalRecalls?

TotalRecalls is a new app, and SmartScreen relies on download history to recognize software. Until enough people have installed it, Windows asks you to confirm before it opens. The prompt reflects how new the app is, not what the app does.

### Is it safe to click "Run anyway"?

Yes, when your file came from totalrecalls.app. The prompt means Windows doesn't recognize the app yet. If your file came from any other source, don't run it. Download a fresh copy from our site instead.

### I don't see a "Run anyway" button. What now?

Make sure you clicked **More info** first, since the button stays hidden until you do. On some PCs, a work administrator or a Windows 11 setting called Smart App Control can remove the button entirely. If that happens, email us and we'll help you find the right next step.

### Will I see this every time I open TotalRecalls?

Usually not. The prompt normally appears once per downloaded file. You may see it again after you download a new version, until that version builds its own reputation.

### Does clicking "Run anyway" change my security settings?

No. It lets this one app open. SmartScreen stays on and keeps checking every other app you download.

---

### Support

`STILL STUCK?`

## Email a real person

If the prompt looks different from the screenshots above, or something doesn't feel right, write to us. Include your Windows version and a screenshot if you can.

[`support@totalrecalls.app`](mailto:support@totalrecalls.app)

---

### Closing CTA

## Ready to install?

Download TotalRecalls, click More info, then Run anyway. Your first chats can be on your PC a few minutes from now.

[**Back to download**](/download/)

Free Tier includes ChatGPT, Claude, and Perplexity, 5 conversations each. Windows 10 and 11.

---

## Layout

1. **Hero:** Left-aligned eyebrow, headline, and intro, capped at 680px. The chip row and the "Skip to the steps" link sit below.
2. **Explainer and "not malware" sections:** Single-column text on Obsidian. The "not malware" section sits inside one Graphite callout panel so it stands out without alarm styling.
3. **Steps:** Two Graphite step cards side by side on desktop, stacked on mobile. Each card holds its number, title, body, metadata chip, and annotated screenshot.
4. **Check your source:** A Graphite panel with the three checks as a list and the source chip at the bottom.
5. **FAQ:** Accordion, collapsed by default.
6. **Support and closing CTA:** Support block, then a Graphite band with the final CTA.

---

## Implementation Spec

| Element               | Copy                                           | Style                                                                                                                                                                                                           |
| --------------------- | ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Page background       | —                                              | Obsidian `#111315`. Hero padding 128px desktop / 64px mobile. Sections 96px desktop / 64px mobile.                                                                                                              |
| Eyebrows              | SUPPORT · WINDOWS 10/11, etc.                  | `eyebrow`: Inter Medium 12px, uppercase, +0.12em tracking, Steel Blue `#7A8FA6`                                                                                                                                 |
| H1                    | "Windows protected your PC." Here's what…      | `h1`: Inter Bold, 48px desktop / 34px mobile, 1.1 line height, −0.02em, Paper `#F3EFE7`. Set the quoted phrase in Paper, not Amber.                                                                             |
| Intro                 | When you first open TotalRecalls…              | `body-lg`: Inter Regular, 20px / 18px, Mist `#D9D4CB`, max 680px                                                                                                                                                |
| H2                    | Section headings                               | `h2`: Inter Semibold, 36px / 28px, Paper                                                                                                                                                                        |
| H3                    | Step titles, FAQ questions                     | `h3`: Inter Semibold, 24px / 20px, Paper (FAQ questions use `h4`, 18px)                                                                                                                                         |
| Body                  | Paragraphs and lists                           | `body`: Inter Regular 16px, 1.6 line height, Mist                                                                                                                                                               |
| Hero chips            | WINDOWS 10/11 · 2 CLICKS · DOWNLOAD ONLY…      | `mono-sm`: IBM Plex Mono Medium 12px, uppercase, Steel Blue text, Slate `#2A2F36` fill, 6px radius, 4px × 8px padding                                                                                           |
| Skip link             | Skip to the steps ↓                            | Tertiary: Inter Semibold 15px, Steel Blue, links to `#steps`                                                                                                                                                    |
| "Not malware" callout | —                                              | Graphite `#1A1D21` panel, 1px Slate border, 12px radius, 24px padding. Info-circle icon, 24px, Mist. No red, no warning triangle.                                                                               |
| Step cards            | 01 / 02                                        | Graphite fill, 1px Slate border, 12px radius, 24px padding, no shadow, no hover                                                                                                                                 |
| Step number           | 01 / 02                                        | IBM Plex Mono Medium 14px, Steel Blue                                                                                                                                                                           |
| Button names in steps | More info / Run anyway                         | Inter Semibold, Paper. Not styled as buttons, so they don't look clickable.                                                                                                                                     |
| Screenshots           | Annotated SmartScreen prompts                  | 8px radius, 1px Slate border. Annotation rings and arrows in Archive Amber `#C88A2B`, 2px stroke. Alt text: "SmartScreen prompt with More info highlighted" / "SmartScreen prompt with Run anyway highlighted." |
| Evidence strip        | `C:\TotalRecalls\Library\` · `● SAVED LOCALLY` | Path in `mono` 14px, Steel Blue, selectable. Local chip in Local Green `#5E8A68`, placed on an Obsidian well inside the card, never directly on Graphite.                                                       |
| Source panel          | Check your source                              | Graphite panel, 12px radius. List checks use a Mist check icon, not green (they're instructions, not completed states).                                                                                         |
| Source chip           | DOWNLOAD ONLY FROM TOTALRECALLS.APP            | `mono-sm`, Steel Blue on Slate                                                                                                                                                                                  |
| FAQ                   | 5 items                                        | Accordion, chevron icon, 150ms ease-out expand, 1px Slate dividers                                                                                                                                              |
| Support email         | <support@totalrecalls.app>                     | `mono` 14px, Steel Blue, `mailto:` link, selectable                                                                                                                                                             |
| Closing band          | Ready to install?                              | Graphite band, 1px Slate top border                                                                                                                                                                             |
| Primary CTA           | Back to download                               | Large button, 48px, Archive Amber fill, Obsidian text, 8px radius, links to `/download/`. The page's only Amber button.                                                                                         |
| CTA microcopy         | Free Tier includes…                            | `body-sm`: Inter Regular 14px, Dust `#B5AEA3`                                                                                                                                                                   |

### Spacing

| Gap                  | Value                      |
| -------------------- | -------------------------- |
| Eyebrow → heading    | 12px                       |
| Heading → intro/body | 16px                       |
| Intro → chip row     | 24px                       |
| Between chips        | 8px                        |
| Between step cards   | 24px                       |
| Step body → chip     | 16px                       |
| Chip → screenshot    | 16px                       |
| Between sections     | 96px desktop / 64px mobile |
| CTA → microcopy      | 12px                       |

### Behavior

- **Static page.** No motion beyond an optional one-time 200ms fade-in per section. Disable it under `prefers-reduced-motion`.
- **Deep linking:** Add `id="steps"` to the How to Continue section, so support replies can link straight to the instructions.
- **Mobile:** Stack the step cards and let screenshots scale to full width. Below the CTA, add *"Windows app. Visit from your desktop to download."* in `body-sm`, Dust.
- **Icons:** Info circle (callout), external-link-free mail icon (support), and chevron (FAQ). No shield icons, no lock, no warning triangles, and no Windows or Microsoft logos.
- **Links:** Redirect the old `/#smartscreen` anchor to `/smartscreen/`, or update every homepage link.

---

## Accuracy Checks Before Publishing

- **Match the real prompt.** Capture fresh screenshots on current Windows 10 and 11 builds. If the prompt wording has changed, update the headline, the steps, and the alt text to match it exactly.
- **Confirm the app name and publisher line.** After "More info," Windows shows the app name and a publisher field. If the build isn't code-signed, that field reads "Unknown publisher." Consider adding one line to Step 02 that says so, so users aren't surprised. If you add a code-signing certificate later, update the copy and screenshots.
- **Don't promise the prompt will disappear.** Keep "should appear less often." Don't give a timeline.
- **Keep the malware distinction precise.** SmartScreen is a reputation check. Microsoft Defender Antivirus detections are a different alert. Don't claim that TotalRecalls "can never" trigger any Windows security alert.
- **Smart App Control and managed PCs.** Both can hide "Run anyway." Keep the FAQ answer general and route those users to support. Don't give instructions for turning off Smart App Control or any other Windows protection.
- **File checks only if real.** If you publish a SHA-256 checksum or a digital signature, add a "verify your file" step. If you don't, leave verification out.
- **Distribution claim.** "We don't distribute TotalRecalls through file-sharing sites, app mirrors, or email attachments" must stay true. Remove it if you ever list the app in a store or directory.
- **Free Tier wording.** The CTA microcopy says "5 conversations each." Confirm this matches the current build and the homepage.
- **No absolute safety language.** Use "when your file came from totalrecalls.app" as the condition every time the page says it's safe to continue.
