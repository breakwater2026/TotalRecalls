Review complete — TotalRecalls website
Scope: local site/ source (the changes under review), the built dist/ (65 pages), the live totalrecalls.app, the downloader UI (app_ui.html), and the SSE module (Modules/smart-search-engine/). Build passes: 65 pages, 0 errors, 63 sitemap URLs. Work is committed as 905def4 — not pushed.

Done in this pass (your two explicit asks)
Removed every launch end-date reference. [DATE] is gone from the FAQ, /smart-search/, /search/, and the SSE guide; "Early-buyer price … for the first 30 days after launch" is now "$31 at launch".
Added the price-change statement — "Prices may change at any time without advance notice." — to the home pricing component, /pricing/, /buy/, /compare/pricing/, /faq/, /smart-search/, /search/, and the guide (9 occurrences).
Fixed the hero asterisk $29 → $39 (contradicted the documented $39 launch price).
Rebuilt the FAQ JSON-LD from the visible FAQ: it had only 18 of 32 questions and still called semantic search a separate add-on. It is now valid and mirrors all 32 visible Q&As.
Moved Handoff Note 110426.md out of src/pages/ into docs/ — Astro was building it as a public page full of internal paths and commit hashes.
Pricing presentation proposal
One shared ladder everywhere — Free → Pro → Pro + SSE bundle — with launch price always beside the regular price, no "% off" against a price never charged, and the price-change line in the fine print. The downloader gets a real 3-tier card instead of the bare "Buy Pro — $24" button; the SSE module drops the Founder's Pass / 6-week drops model for the same ladder.


Corrections required (not applied — need your call)
Factual / high-impact

SSE module pricing contradicts the website. WebsitePresentation.tsx, SpecsAndPricing.tsx, DemoScript.tsx, constants.ts, manualExporters.ts still sell "Core Downloader $29", "Founder's Season Pass $49 (was $140)", "Enterprise $149", "65% off", 6-week drops at $19–$25. The site sells Pro $24/$48, SSE $39/$59, bundle $55/$89, Pro owners $31. This is the biggest inaccuracy on the product.
SSE module makes forbidden privacy claims. "100% Offline", "100% Air-Gapped Security", "Zero cloud uploads, zero network leaks" — the copy doc explicitly bans "fully offline"/"100% local" because setup downloads the search model once. Use "Runs on your PC. Nothing you write or save is uploaded."
SSE module provider list is wrong. It lists 5–6 providers and invents "LocalLlama"; it omits Grok, DeepSeek, and Qwen. The product supports eight.
/pricing/ shows no SSE pricing at all. The copy doc requires the price table mirrored on /pricing/; it currently stops at Pro $24.
Bundle/SSE buttons are dead ends. Every "Get the bundle, $55" and "Add SSE to Pro, $39" button site-wide points to /buy/, which only sells Pro $24. Either add bundle/SSE checkout (new Paddle price IDs) or relabel the buttons.
Refund policy contradiction. FAQ says SSE is "30 days, no questions asked"; /pricing/, /legals/, /terms/, and the home FAQ say "case-by-case". Pick one (the copy doc suggests 30 days, marked DECIDE).
Naming / consistency

Nav is ragged. "SMART SEARCH ENGINE (SSE)" wraps to 4 lines, "HOW IT WORKS" and "SEE IT WORK" to 3; the doc says the label should be "Smart Search". There are also two tabs — "SMART SEARCH ENGINE (SSE)" and "SEARCH" — pointing at two near-duplicate pages.
/search/ is a stale clone of /smart-search/. It still says "Demo video in production … goes live at launch", "What a Search result shows", alt text "TotalRecalls Search results window", and its "Watch the 75-second demo" button is an anchor, not a video. Recommend redirecting /search/ → /smart-search/.
/smart-search/ "Watch the demo" links to /search/ — the stale page, not a demo.
Guide page identity mismatch. Title and breadcrumb say "Using TotalRecalls Search" while the H1 says "Using Smart Search Engine"; URL is /guides/using-totalrecalls-search/; and it is not listed on /guides/ (Guides.jsx).
/previews/semantic-search/ is a shipped product page filed under "Previews" (planned work) and still uses planned framing ("Keyword search that works immediately, with semantic ranking layered on once the index is built").
"Planned" language that is no longer true: Providers page ("Planned integrations — … semantic search …"), /compare/ ("Full-text search across providers — Planned"), roadmap ("Keyword search … before semantic ranking").
Obsidian/Notion contradiction. Roadmap/preview pages list Notion and Obsidian as planned, and /pricing/ + FAQ + /compare/pricing/ list "Obsidian/Notion sync" as a future advanced feature — while SSE includes Obsidian and Notion connections at launch.
Two different footers. Home (tr/Footer.jsx) has both "Search" and "Smart Search"; subpages (Footer.astro) have "Search" but no "Smart Search", and their "Providers" link points to /#matrix, which does not exist on the home page — broken on every subpage.
/legals/#pricing anchor does not exist (legals has #privacy, #terms, #refund) — linked from /about/, /buy/, /support/.
Download page duplicate link: "read the full Privacy Policy or the standalone privacy page" — both hrefs are /privacy/.
\$24USD vs \$24 USD: public/js/config.js injects priceLabel: "\$24USD" via textContent, flattening the styled <span class="tr-usd">USD</span> and dropping the space on every JS-injected price.
Minor: legals "Last updated" uses new Date() at build time (rolls forward every deploy); about page typo "for an download request"; download page footer CTA shows a price with no buy button; /compare/pricing/ lacks SSE pricing; docs manuals still say $29.
Button / link audit
0 broken internal file links, 0 broken same-page anchors across all 65 pages.
Cross-page anchor breaks: /legals/#pricing (3 pages) and /#matrix (every subpage footer).
All CTAs resolve to real pages except the bundle/SSE buttons that route to /buy/ (Pro-only checkout).
Footer signup posts to /api/subscribe; live returns 200 {"ok":true}, so it works against the deployed backend.
Live site / domain
totalrecalls.app is stale. It still serves the pre-SSE build: /smart-search/ is 404, naming is still "TotalRecalls Search", and /search/ shows the old $19 / $39 / $14 pricing. None of the local changes are deployed.
totalrecalls.com is a parked "for sale" domain (redirects to /lander), not the product site. If that's meant to be the public URL, it needs to point at the site.
Testing notes
Verified by static crawl of the built HTML (links, anchors, price/naming greps), a full astro build, and visual inspection of the home page, pricing section, /pricing/, /faq/, /smart-search/, and the downloader UI. Not exercised: the live Paddle checkout, theme-toggle persistence, and the mobile menu.

Open decisions for you: refund window (30 days vs case-by-case), whether to add bundle/SSE checkout, nav label + /search/ consolidation, and whether to apply the pricing-presentation redesign to the downloader and SSE module. Say the word and I'll implement any of them.

9:59:30.831 PM → 9:59:37.028 PM
9:59:49.788 PM
9:59:49.788 PM → 10:00:01.607 PM
10:00:14.343 PM
10:00:14.343 PM → 10:00:17.548 PM
10:00:25.704 PM
10:00:25.704 PM → 10:01:47.523 PM
10:02:03.798 PM
10:02:03.798 PM → 10:02:33.570 PM
10:02:42.753 PM
10:02:42.753 PM → 10:02:52.449 PM
10:03:01.871 PM
10:03:01.871 PM → 10:03:11.251 PM
10:03:19.145 PM
10:03:19.145 PM → 10:04:40.525 PM
10:04:52.524 PM
10:04:52.524 PM → 10:05:35.756 PM
10:05:50.095 PM
10:05:50.095 PM → 10:06:01.526 PM
10:06:09.406 PM
10:06:09.406 PM → 10:06:36.851 PM
10:06:55.173 PM
10:06:55.173 PM → 10:08:00.218 PM
10:08:16.224 PM
10:08:16.224 PM → 10:08:25.060 PM
10:08:32.065 PM
10:08:32.065 PM → 10:09:26.378 PM
10:10:21.337 PM
10:10:21.337 PM → 10:10:23.511 PM
10:10:31.370 PM
10:10:31.370 PM → 10:10:32.857 PM
10:11:12.032 PM
10:11:12.032 PM
Now I have a full picture. Let me implement the two explicit changes (end-date removal + price-change statement) and fix the one outright price typo I found.

10:11:12.032 PM → 10:11:18.117 PM
              Windows app. Visit from your desktop to download.
            </p>
            <p className="mt-5 font-mono text-[11px] text-tr-dust">
              * Optional Smart Search Engine (SSE) sold separately - $29 launch price.
              * Optional Smart Search Engine (SSE) sold separately - $39 launch price.
            </p>
          </div>
10:11:12.032 PM → 10:11:18.144 PM
        <div className="mt-10 text-center">
          <p className="mx-auto max-w-[680px] font-body text-[14px] leading-[1.5] text-tr-dust">
            Windows 10 and 11. $24 is a discounted launch price. Add-ons, like Smart Search Engine, are sold
            separately. See below. Your core app updates stay free.
            separately. See below. Your core app updates stay free. Prices may change at any time without
            advance notice.
          </p>
          <div className="mt-5 flex flex-wrap justify-center gap-2">
            {["One-time", "No subscription", "No account", "Windows 10/11"].map((t) => (
10:11:12.032 PM → 10:11:18.165 PM
    <dt>Is there a bundle?</dt>
    <dd>Yes. Pro + Smart Search Engine is $55 at launch (regular $89). If you already own Pro, add Smart Search Engine for $31 at launch.</dd>
    <dt>When do the launch prices end?</dt>
    <dd>On [DATE]. After that, Pro is $48, Smart Search Engine is $59 and the bundle is $89.</dd>
    <dt>Can prices change?</dt>
    <dd>Yes. Prices may change at any time without advance notice. The price you pay is the price shown at checkout when you buy.</dd>
    <dt>What’s your refund policy for Smart Search Engine?</dt>
    <dd>30 days, no questions asked.</dd>
10:11:12.032 PM → 10:11:18.191 PM
          Already own Pro? <strong>$31</strong> at launch.
        </p>
        <p class="mt-3 max-w-[680px] font-body text-[13px] leading-[1.5] text-tr-dust">
          Launch prices end on [DATE]. After that, Pro is $48, Smart Search Engine is $59 and the bundle is $89.
          Prices may change at any time without advance notice.
        </p>
      </div>
    </section>
10:11:37.372 PM
10:11:37.372 PM → 10:11:43.684 PM
          </div>
        </div>
        <p class="mt-5 max-w-[680px] font-body text-[15px] leading-[1.6] text-tr-mist">
          Already own Pro? Early-buyer price <strong>$31</strong> for the first 30 days after launch.
          Already own Pro? <strong>$31</strong> at launch.
        </p>
        <p class="mt-3 max-w-[680px] font-body text-[13px] leading-[1.5] text-tr-dust">
          Launch prices end on [DATE]. After that, Smart Search Engine is $59 and Pro is $48.
          Prices may change at any time without advance notice.
        </p>
      </div>
    </section>
10:11:37.372 PM → 10:11:43.698 PM
  <ul>
    <li>Smart Search Engine add-on: <strong>$39 launch price</strong> (regular $59), one-time purchase. Requires Pro.</li>
    <li>Pro + Smart Search Engine bundle: <strong>$55 at launch</strong>.</li>
    <li>Already own Pro? Early-buyer price of <strong>$31</strong> for the first 30 days after launch.</li>
    <li>Launch prices end on <strong>[DATE]</strong>. After that, Smart Search Engine is $59 and Pro is $48.</li>
    <li>Already own Pro? <strong>$31</strong> at launch.</li>
    <li>Prices may change at any time without advance notice.</li>
  </ul>
  <p>
    Ready to add it? <a href="/smart-search/">Go to the Smart Search Engine page</a> or
10:11:37.372 PM → 10:11:43.722 PM
      <span class="price-current" data-tr-price>$24<span class="tr-usd">USD</span></span>
      <span class="price-badge">launch price</span>
    </div>
    <p class="price-note">One-time purchase · Windows app · Local files only</p>
    <p class="price-note">One-time purchase &middot; Windows app &middot; Local files only</p>
    <p class="price-note">Prices may change at any time without advance notice.</p>
    <p>Pay once by card via Paddle. Your license key arrives by email immediately after purchase — enter it in the app (top-right &ldquo;Pro&rdquo; badge &rarr; paste the key &rarr; Activate) to unlock all 8 providers and unlimited downloads.</p>
    <a href="#" data-tr-buy class="buy-button buy-lg">Buy TotalRecalls — <span data-tr-price>$24<span class="tr-usd">USD</span></span></a>
    <p class="guarantee-note">A Free Tier is available now — 3 providers (Perplexity, ChatGPT, Claude) and up to 5 conversations per download — so you can test a real download on your own chats before paying a cent.</p>
10:11:37.372 PM → 10:11:43.738 PM
      <span class="price-badge">launch price</span>
    </div>
    <p class="price-note">One-time purchase &middot; Windows app &middot; Local files only</p>
    <p class="price-note">Prices may change at any time without advance notice.</p>
    <p>Pay once by card via <strong>Paddle</strong> &mdash; our merchant of record, which handles payment, tax and your receipt. Your license key arrives by email immediately after purchase. Enter the key in the app (top-right &ldquo;Pro&rdquo; badge &rarr; paste the key &rarr; Activate) to unlock all 8 providers and unlimited downloads. The app ships as a single free build &mdash; the key is what unlocks Pro, on up to 3 of your devices.</p>
    <a href="#" data-tr-buy class="buy-button buy-lg">Buy TotalRecalls &mdash; <span data-tr-price>$24<span class="tr-usd">USD</span></span></a>
    <p class="guarantee-note">Not ready to buy? A Free Tier is available now &mdash; download the app and test it on your own chats before paying.</p>
10:12:00.143 PM
10:12:00.143 PM → 10:12:01.166 PM
10:12:24.921 PM
10:12:24.921 PM → 10:12:26.291 PM
10:12:38.806 PM
10:12:45.571 PM → 10:12:46.520 PM
10:13:05.461 PM
10:13:05.461 PM → 10:13:09.154 PM
  <h2>Try before you buy</h2>
  <p>The Free Tier is a real build, not a demo: download it, run it on your own conversations, and decide afterwards. It&rsquo;s limited to 3 AI providers and 5 conversations per download.</p>
  <p><em>Prices may change at any time without advance notice.</em></p>
  <h2>FAQ</h2>
  <dl class="faq" set:html={faqHtml} />
10:13:19.134 PM
10:13:19.134 PM → 10:13:20.254 PM
10:13:28.532 PM
10:13:28.532 PM → 10:13:45.197 PM
10:13:58.477 PM
10:13:58.477 PM → 10:13:59.400 PM
10:14:16.651 PM
10:14:16.651 PM → 10:14:20.351 PM
10:14:28.697 PM
10:14:35.520 PM → 10:14:36.257 PM
10:14:55.874 PM
10:14:55.874 PM → 10:14:56.872 PM
10:15:06.492 PM
10:15:15.400 PM → 10:15:16.308 PM
10:16:20.711 PM
10:16:32.569 PM
10:16:32.569 PM → 10:16:33.486 PM
10:16:40.121 PM
10:16:40.121 PM → 10:16:43.462 PM
};"""
# 3. Replace the old jsonLd literal with the new frontmatter block
s2 = re.sub(r"const jsonLd = '[\s\S]*?';", front, s, count=1)
s2 = re.sub(r"const jsonLd = '[\s\S]*?';", lambda m: front, s, count=1)
assert s2 != s, "jsonLd literal not replaced"
# 4. Replace the visible <dl> block
10:16:49.889 PM
10:16:49.889 PM → 10:16:50.838 PM
10:16:57.116 PM
10:16:57.116 PM → 10:17:13.869 PM
10:17:24.527 PM
10:17:24.527 PM → 10:17:26.262 PM
10:17:32.451 PM
10:17:32.451 PM → 10:17:33.448 PM
10:17:44.091 PM
10:17:44.091 PM → 10:18:15.008 PM
10:19:35.209 PM
10:19:35.209 PM
Now let me build a visual mockup of the proposed pricing presentation for the downloader and SSE.

10:19:51.018 PM
10:19:51.018 PM → 10:19:55.226 PM
10:20:01.967 PM
10:20:01.967 PM → 10:20:58.350 PM
10:21:08.004 PM
10:21:08.004 PM → 10:21:08.915 PM
10:21:30.391 PM
10:21:30.391 PM → 10:21:31.931 PM
10:21:53.212 PM
10:21:53.212 PM → 10:21:53.317 PM
10:22:03.977 PM
10:22:03.977 PM → 10:22:16.384 PM
10:22:24.888 PM
10:22:24.888 PM → 10:23:44.057 PM
10:24:02.287 PM
10:24:02.287 PM → 10:24:03.231 PM
10:24:41.470 PM
10:24:41.470 PM → 10:24:42.456 PM
10:25:24.364 PM
10:25:24.364 PM
Review complete — TotalRecalls website
Scope: local site/ source (the changes under review), the built dist/ (65 pages), the live totalrecalls.app, the downloader UI (app_ui.html), and the SSE module (Modules/smart-search-engine/). Build passes: 65 pages, 0 errors, 63 sitemap URLs. Work is committed as 905def4 — not pushed.

Done in this pass (your two explicit asks)
Removed every launch end-date reference. [DATE] is gone from the FAQ, /smart-search/, /search/, and the SSE guide; "Early-buyer price … for the first 30 days after launch" is now "$31 at launch".
Added the price-change statement — "Prices may change at any time without advance notice." — to the home pricing component, /pricing/, /buy/, /compare/pricing/, /faq/, /smart-search/, /search/, and the guide (9 occurrences).
Fixed the hero asterisk $29 → $39 (contradicted the documented $39 launch price).
Rebuilt the FAQ JSON-LD from the visible FAQ: it had only 18 of 32 questions and still called semantic search a separate add-on. It is now valid and mirrors all 32 visible Q&As.
Moved Handoff Note 110426.md out of src/pages/ into docs/ — Astro was building it as a public page full of internal paths and commit hashes.
Pricing presentation proposal
One shared ladder everywhere — Free → Pro → Pro + SSE bundle — with launch price always beside the regular price, no "% off" against a price never charged, and the price-change line in the fine print. The downloader gets a real 3-tier card instead of the bare "Buy Pro — $24" button; the SSE module drops the Founder's Pass / 6-week drops model for the same ladder.


Corrections required (not applied — need your call)
Factual / high-impact

SSE module pricing contradicts the website. WebsitePresentation.tsx, SpecsAndPricing.tsx, DemoScript.tsx, constants.ts, manualExporters.ts still sell "Core Downloader $29", "Founder's Season Pass $49 (was $140)", "Enterprise $149", "65% off", 6-week drops at $19–$25. The site sells Pro $24/$48, SSE $39/$59, bundle $55/$89, Pro owners $31. This is the biggest inaccuracy on the product.
SSE module makes forbidden privacy claims. "100% Offline", "100% Air-Gapped Security", "Zero cloud uploads, zero network leaks" — the copy doc explicitly bans "fully offline"/"100% local" because setup downloads the search model once. Use "Runs on your PC. Nothing you write or save is uploaded."
SSE module provider list is wrong. It lists 5–6 providers and invents "LocalLlama"; it omits Grok, DeepSeek, and Qwen. The product supports eight.
/pricing/ shows no SSE pricing at all. The copy doc requires the price table mirrored on /pricing/; it currently stops at Pro $24.
Bundle/SSE buttons are dead ends. Every "Get the bundle, $55" and "Add SSE to Pro, $39" button site-wide points to /buy/, which only sells Pro $24. Either add bundle/SSE checkout (new Paddle price IDs) or relabel the buttons.
Refund policy contradiction. FAQ says SSE is "30 days, no questions asked"; /pricing/, /legals/, /terms/, and the home FAQ say "case-by-case". Pick one (the copy doc suggests 30 days, marked DECIDE).
Naming / consistency

Nav is ragged. "SMART SEARCH ENGINE (SSE)" wraps to 4 lines, "HOW IT WORKS" and "SEE IT WORK" to 3; the doc says the label should be "Smart Search". There are also two tabs — "SMART SEARCH ENGINE (SSE)" and "SEARCH" — pointing at two near-duplicate pages.
/search/ is a stale clone of /smart-search/. It still says "Demo video in production … goes live at launch", "What a Search result shows", alt text "TotalRecalls Search results window", and its "Watch the 75-second demo" button is an anchor, not a video. Recommend redirecting /search/ → /smart-search/.
/smart-search/ "Watch the demo" links to /search/ — the stale page, not a demo.
Guide page identity mismatch. Title and breadcrumb say "Using TotalRecalls Search" while the H1 says "Using Smart Search Engine"; URL is /guides/using-totalrecalls-search/; and it is not listed on /guides/ (Guides.jsx).
/previews/semantic-search/ is a shipped product page filed under "Previews" (planned work) and still uses planned framing ("Keyword search that works immediately, with semantic ranking layered on once the index is built").
"Planned" language that is no longer true: Providers page ("Planned integrations — … semantic search …"), /compare/ ("Full-text search across providers — Planned"), roadmap ("Keyword search … before semantic ranking").
Obsidian/Notion contradiction. Roadmap/preview pages list Notion and Obsidian as planned, and /pricing/ + FAQ + /compare/pricing/ list "Obsidian/Notion sync" as a future advanced feature — while SSE includes Obsidian and Notion connections at launch.
Two different footers. Home (tr/Footer.jsx) has both "Search" and "Smart Search"; subpages (Footer.astro) have "Search" but no "Smart Search", and their "Providers" link points to /#matrix, which does not exist on the home page — broken on every subpage.
/legals/#pricing anchor does not exist (legals has #privacy, #terms, #refund) — linked from /about/, /buy/, /support/.
Download page duplicate link: "read the full Privacy Policy or the standalone privacy page" — both hrefs are /privacy/.
\$24USD vs \$24 USD: public/js/config.js injects priceLabel: "\$24USD" via textContent, flattening the styled <span class="tr-usd">USD</span> and dropping the space on every JS-injected price.
Minor: legals "Last updated" uses new Date() at build time (rolls forward every deploy); about page typo "for an download request"; download page footer CTA shows a price with no buy button; /compare/pricing/ lacks SSE pricing; docs manuals still say $29.
Button / link audit
0 broken internal file links, 0 broken same-page anchors across all 65 pages.
Cross-page anchor breaks: /legals/#pricing (3 pages) and /#matrix (every subpage footer).
All CTAs resolve to real pages except the bundle/SSE buttons that route to /buy/ (Pro-only checkout).
Footer signup posts to /api/subscribe; live returns 200 {"ok":true}, so it works against the deployed backend.
Live site / domain
totalrecalls.app is stale. It still serves the pre-SSE build: /smart-search/ is 404, naming is still "TotalRecalls Search", and /search/ shows the old $19 / $39 / $14 pricing. None of the local changes are deployed.
totalrecalls.com is a parked "for sale" domain (redirects to /lander), not the product site. If that's meant to be the public URL, it needs to point at the site.
Testing notes
Verified by static crawl of the built HTML (links, anchors, price/naming greps), a full astro build, and visual inspection of the home page, pricing section, /pricing/, /faq/, /smart-search/, and the downloader UI. Not exercised: the live Paddle checkout, theme-toggle persistence, and the mobile menu.

Open decisions for you: refund window (30 days vs case-by-case), whether to add bundle/SSE checkout, nav label + /search/ consolidation, and whether to apply the pricing-presentation redesign to the downloader and SSE module. Say the word and I'll implement any of them.


