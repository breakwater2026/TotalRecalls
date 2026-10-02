# See It Work Pro Upgrade Script

**Format:** Secondary demo embed for the See It Work page\
**Runtime:** About 60 seconds\
**Platform shown:** Windows 11, current Free Tier build upgrading to Pro\
**Voice:** Calm, plain, and unhurried. Read it like you're showing a friend what's on your screen.\
**Sound:** Voiceover only, or a very quiet ambient bed. No music cues, swells, or sound effects.\
**Captions:** On by default. Every step has its own on-screen caption, so the video makes sense muted.

---

## Scene 1: Hit the Free Tier Cap

**Time:** 0:00–0:08

**VISUAL**

- The TotalRecalls app is open with ChatGPT selected.
- Five conversations already show as saved.
- The cursor selects a sixth thread, "Client draft v3," and clicks **Download**.
- The app shows its Free Tier limit message. Capture the real message exactly as the build displays it.

**ON-SCREEN TEXT**\
`STEP 1 · FREE TIER LIMIT`\
5 of 5 ChatGPT conversations saved.

**VOICEOVER**\
This is the Free Tier. Five ChatGPT chats are saved, and that's the limit for this provider.

---

## Scene 2: Open the Pricing Page

**Time:** 0:08–0:16

**VISUAL**

- The cursor clicks the app's upgrade link, which opens the browser at `totalrecalls.app/pricing/`. If the app has no upgrade link, type the address into the browser instead.
- The page scrolls to the Free vs Pro table. Hold on the Pro column long enough to read "$24 one-time (launch price)."

**ON-SCREEN TEXT**\
`STEP 2 · OPEN THE PRICING PAGE`\
`totalrecalls.app/pricing/`\
Pro: $24 one-time, launch price.

**VOICEOVER**\
To save more, open the pricing page. Pro is twenty-four dollars, one time, at the launch price.

---

## Scene 3: Check Out

**Time:** 0:16–0:26

**VISUAL**

- The cursor clicks **Buy TotalRecalls — $24**.
- The checkout page loads. The email field, name, card details, and billing address are blurred.
- The purchase completes, and the confirmation screen appears. Blur the order number.

**ON-SCREEN TEXT**\
`STEP 3 · CHECK OUT`\
No TotalRecalls account. No subscription.

**VOICEOVER**\
Check out with your email. There's no TotalRecalls account to create, and nothing renews.

---

## Scene 4: Get Your License Key

**Time:** 0:26–0:33

**VISUAL**

- An inbox opens. The license email arrives within a few seconds. Trim any wait.
- The email opens. The license key is fully blurred.
- The cursor copies the key.

**ON-SCREEN TEXT**\
`STEP 4 · GET YOUR KEY`\
Your license key arrives by email after checkout.

**VOICEOVER**\
Your license key arrives by email right after checkout. Copy it.

---

## Scene 5: Enter the Key

**Time:** 0:33–0:42

**VISUAL**

- Back in the same TotalRecalls window. There is no new download and no reinstall.
- The cursor opens the license field, pastes the blurred key, and clicks **Activate**.
- The app confirms that Pro is active. If the build shows an activation count, keep it visible.

**ON-SCREEN TEXT**\
`STEP 5 · ENTER THE KEY`\
Same app. Pro activates on up to 3 PCs.

**VOICEOVER**\
Back in the same app, paste the key and activate. Pro works on up to three PCs.

---

## Scene 6: All Eight Providers, No Cap

**Time:** 0:42–0:54

**VISUAL**

- The provider list now shows all eight as available: ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen. Names appear as text only, with no logos.
- The cursor returns to ChatGPT and clicks **Download** on "Client draft v3." It saves with no limit message.
- File Explorer opens to `C:\TotalRecalls\Library\chatgpt\`. The sixth Markdown and JSON pair sits beside the first five. Hold on this frame.

**ON-SCREEN TEXT**\
`STEP 6 · ALL 8 PROVIDERS UNLOCKED`\
Unlimited downloads. Gemini uses a Google Takeout file.\
`chatgpt\2026-09-21-client-draft-v3.md`

**VOICEOVER**\
Now all eight providers are available. Gemini comes in through Google Takeout. The cap is gone, so that sixth chat saves right away.

---

## Scene 7: Close

**Time:** 0:54–1:00

**VISUAL**

- The Library frame from Scene 6 holds for a beat, then fades to Obsidian.
- The TotalRecalls wordmark appears in Paper, with the CTA below it in Archive Amber.

**ON-SCREEN TEXT**\
**Get Pro at totalrecalls.app**\
`$24 ONE-TIME · LAUNCH PRICE · WINDOWS 10/11`

**VOICEOVER**\
One payment, every provider. Get Pro at totalrecalls.app.

---

## Production Notes

- **Spoken word count:** About 115 words, which fits a calm pace inside 60 seconds.
- **Role on the page:** The ChatGPT Free Tier demo stays the primary video. Place this one as a secondary embed beside the "Compare Free and Pro →" link, below the Try It Yourself band. It should never compete with the main demo.
- **Player behavior:** Match the See It Work spec. No autoplay. Lazy-load the player behind a static poster. Use native or minimal controls, with no end screens and no sticky player. The play button is Paper on Obsidian, never Amber.
- **Poster frame:** Use the Scene 6 end state, the Library folder showing six ChatGPT file pairs. Export it at 2x resolution with no overlay text.
- **Real capture only.** Record the current build on a real Windows 11 machine, from Free Tier through activation. Don't recreate or mock up any screen. If anything is recreated, don't place this video under the page's "Nothing is mocked up" line.
- **Trimming:** Trim checkout loading and email delivery waits, and add a "Real screen recording, trimmed for length" caption under the embed. The video shouldn't suggest faster delivery than buyers will see.
- **Blur everything personal.** Blur the email address, name, card details, billing address, order number, license key, profile images, and any non-demo thread titles. Never show a session token.
- **Captions:** Burn them in or ship a default-on WebVTT track. Use the on-screen text wording above. Add a collapsed transcript below the embed with its own anchor, such as `id="pro-transcript"`.
- **Visual style:** Use straight cuts or short crossfades only. Avoid zoom punches, fast cuts, motion graphics, and flying logos. Caption cards use Obsidian backgrounds, Paper text, and Steel Blue mono for paths and URLs. The closing CTA is the only Archive Amber you add. The Amber on the real pricing page and checkout button is part of the recorded screen, so leave it as is.
- **Cursor:** Use a slightly enlarged cursor with a soft click highlight so viewers can follow each action.
- **Re-record trigger:** Re-record if the pricing page, checkout flow, license email, activation screen, or provider list changes in a visible way. Also re-record the day the launch price ends.

---

## Accuracy Checks Before Recording

- **In-place upgrade.** Scene 5 shows the Free Tier install unlocking with the key. Confirm the build works this way. If users must download a separate Pro build, add that step and change the "Same app" caption.
- **Free Tier limit wording.** The caption says "5 of 5 ChatGPT conversations saved," which follows the per-provider rule. The live site says "per download." Confirm the build, then match this script, the Pricing, Legals, and homepage wording, and the other two artifacts.
- **Limit message.** Record the app's real cap message. Don't invent or restyle one.
- **Upgrade link.** Confirm whether the app links to `/pricing/` or `/buy/`. Then match Scene 2.
- **Launch price.** Keep "launch price" beside every $24, in captions and in the closing chip. Don't add "50% off" or an end date unless both are published and real.
- **Checkout processor.** Paddle vs Lemon Squeezy is still unconfirmed. Don't name either one in the voiceover or captions. If the processor's branding appears on screen, confirm it's the live one before recording.
- **Test or live purchase.** Record a real live purchase, or a sandbox checkout that looks identical to the live one. If you use sandbox mode, make sure no "test mode" banner appears, or disclose it in the caption under the embed.
- **Taxes.** If sales tax or VAT appears at checkout, let it show. Don't crop the total to read exactly $24.
- **Key delivery.** "Arrives by email right after checkout" must match real delivery times. Trimming is fine, but note it in the caption under the embed.
- **Device activations.** "Up to 3 PCs" must match the license system. Never write "unlimited devices."
- **Gemini.** Always describe it as a Google Takeout conversion. The caption in Scene 6 must stay, so the expanded list doesn't imply a one-click Gemini download.
- **No account.** Confirm checkout doesn't create or require a TotalRecalls account before keeping that line.
- **Privacy wording.** If you add any privacy caption, keep "not sent to our servers." Downloads connect directly to each provider, so never write "never touches the internet."
- **Folder path and filenames.** `C:\TotalRecalls\Library\chatgpt\` and the `2026-09-21-client-draft-v3` filename pattern must match the current build exactly.
- **Platforms.** Windows 10 and 11 only. Show no Mac or Linux icons, and give no release dates.
- **Updates.** If updates come up anywhere, use "for the life of the product." Never say "forever" or "lifetime updates."
