
Here's both deliverables — exact copy fixes and the technical checklist to resolve the charset bug.

Technical Checklist: Fixing UTF-8 Encoding on Cloud Run/Astro
The root cause is that your server response header shows Content-Type: text/html with no charset directive, even though your HTML meta tag declares UTF-8. Browsers fall back to Latin-1/ISO-8859-1 when the HTTP header omits charset, overriding the meta tag in many cases — this is exactly the mismatch causing the â and Â· artifacts.

If served via Astro's built-in server/adapter: Check your astro.config.mjs output adapter (Node/Cloud Run standalone). Ensure the adapter explicitly sets Content-Type: text/html; charset=utf-8 on all HTML responses — Astro's default should do this, so if it isn't, something in your Docker/Express layer is stripping it.

If using an Express/Node server in front of Astro: Add explicit middleware:

js
app.use((req, res, next) => {
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  next();
});
Or set it per-route right before sending HTML responses.

If using serve-static or a static file server for the built Astro output: Confirm it's configured to append charset=utf-8 for .html files specifically — some static servers only default this for .txt or .json.

Check your Dockerfile/Cloud Run service: Verify no reverse proxy, CDN, or Cloud Run ingress config is rewriting/stripping the Content-Type header. Test with curl -I against your deployed URL to see the raw header Cloud Run is actually sending versus what your app code sets.

Verify source file encoding: Ensure your .astro and .md content files are saved as UTF-8 (not UTF-8 with BOM or Windows-1252) in your editor/VS Code — check the encoding indicator in VS Code's bottom status bar.

Fix the canonical tag bug in parallel: <link rel="canonical" href="https://totalrecalls.appundefined"> indicates a JavaScript template variable (likely Astro.site or an env variable) is resolving to undefined at build time. Check your astro.config.mjs for a missing or misconfigured site: property, and check any component computing the canonical URL for a broken string concatenation.

Test after fix: Re-run curl -I and confirm the header reads Content-Type: text/html; charset=utf-8, then hard-refresh the live page and confirm em-dashes and middle-dots render correctly.

Copy Fixes
1. Refund/Guarantee Statement (place directly under primary buy button)
Current gap: no refund policy visible near the purchase decision point.

Suggested addition, right under the hero CTA and the footer CTA:

text
14-day money-back guarantee. If TotalRecalls doesn't work for you, email us and we'll refund it — no questions asked.
Keep this short and place it directly beneath both instances of "Buy TotalRecalls — $24" so it's visible exactly when the buyer hesitates.

2. Gemini Clarification (surface before checkout, not buried in Straight Talk)
Current: buried as a single line under "Supported Providers."

Suggested rewrite for that section:

text
Supported Providers
ChatGPT · Claude · Perplexity · Gemini · Grok

ChatGPT, Claude, Perplexity, and Grok export directly through TotalRecalls.
Gemini works a little differently: Google doesn't allow direct chat export, 
so TotalRecalls converts your Google Takeout JSON into the same clean 
Markdown format — takes about 5 extra minutes the first time.
This reframes the Gemini limitation as a solved problem rather than a hidden caveat, which builds more trust than omission.

3. Encoding-Safe Copy Rewrite (replace all garbled characters)
Once the charset fix is deployed, confirm these render correctly. As a reference, here is the corrected copy with proper UTF-8 characters spelled out safely:

Title: TotalRecalls — Own every AI conversation.

Meta description: A small Windows app that saves your ChatGPT, Claude, Perplexity, Gemini, and Grok chats into a private folder on your computer — readable Markdown + JSON you keep forever.

Price note: One-time purchase · Windows app · Local files only

Card 1: Your AI history shouldn't vanish (use a straight apostrophe or proper curly ’, not a raw byte)

How It Works steps: Buy once — Checkout via Lemon Squeezy. / Install — Unzip and run the Windows app. / Pick a provider — ChatGPT, Claude, Perplexity, Gemini, or Grok. / Export — Chats land as Markdown + JSON under a Library folder.

Footer pricing note: One-time purchase · No subscription · Local files only

The fix here is purely at the encoding/header level — once UTF-8 is correctly served, your existing em-dashes and middle-dots in the source will render properly without needing to rewrite the actual characters, provided your source files are genuinely saved as UTF-8.

4. Version Badge / Beta Narrative Reconciliation
Pick one of two consistent framings:

Option A — Lean into "early access" honesty:

text
TotalRecalls v1.3.0 (Early Access)
Add a line near the buy button: Early access build. Actively improving based on user feedback.

Option B — Drop the version badge from public view entirely until code-signing is complete and remove "beta" language from the SmartScreen caveat, positioning it as a finished v1.3 product with a known, temporary installation quirk.

Given the SmartScreen and Smart App Control warnings already disclosed, Option A is more consistent with your existing "Straight Talk" transparency strategy and lower-risk from a trust standpoint.

5. Lightweight Social Proof (add to hero or Why section)
Since no user count or testimonial exists yet, use an honest, low-commitment placeholder that still signals momentum:

text
Built by a solo developer who was tired of losing months of AI conversations to broken exports and shifting UIs.
This works as an authentic founder-story trust signal without fabricating numbers you don't have yet — appropriate for a beta stage, and consistent with the direct tone of your "Straight Talk" section.

Once the charset header is fixed and these copy blocks are added, I'd recommend a second-pass visual review with real screenshots to replace the CSS mockups — happy to help draft that screenshot brief next if useful.

