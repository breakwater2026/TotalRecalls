LongCat 2.5 · PreviewXHigh
1Full-Stack & Content Strategist
2Review TotalRecalls landing page changes
3Microsoft Store-TotalRecalls
4Demo videos
5Thorough live site review of totalrecalls.app
Show earlier messages
please perform a thorough review of every element of the live site totalrecalls.app. Rely only on the live website, not its code base. Generate a list of deficiencies that we will address after my review.
11:36:32.554 AM
Thought11:36:37.556 AM → 11:36:47.376 AM
Loaded skill: website-audit, performed 1 browser action11:36:47.353 AM → 11:37:12.693 AM
Thought11:37:16.011 AM → 11:37:19.882 AM
Read skill resource: website-audit → references/deterministic-checks.md, read skill resource: website-audit → scripts/crawl_site.py, ran 1 command11:37:19.857 AM → 11:37:24.005 AM
Thought11:37:27.210 AM → 11:37:32.007 AM
Ran mkdir -p audit + 7 commands11:37:31.982 AM → 11:37:33.182 AM
Thought11:37:35.185 AM → 11:37:37.891 AM
Ran curl -sS -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AuditBot/1.0" https://totalrecalls.app/sitemap.xml -o sitemap.xml + 8 commands11:37:37.869 AM → 11:37:39.042 AM
Thought11:37:40.896 AM → 11:38:08.002 AM
Ran python3 crawl_site.py --sitemap https://totalrecalls.app/sitemap.xml --host https://totalrecalls.app --out ./out --workers 811:38:14.082 AM → 11:38:15.027 AM
Thought11:38:16.963 AM → 11:38:20.052 AM
Ran python3 crawl_site.py --sitemap https://totalrecalls.app/sitemap.xml --host https://totalrecalls.app --out ./out --workers 811:38:20.022 AM → 11:38:23.459 AM
Thought11:38:25.160 AM → 11:38:52.919 AM
Ran python3 analyze.py11:38:58.725 AM → 11:39:01.295 AM
Thought11:39:07.264 AM → 11:39:12.596 AM
Ran python3 analyze.py | grep -v "img missing width/height" | sed -n '/==== FINDINGS ====/,$p'11:39:12.508 AM → 11:39:15.238 AM
Thought11:39:17.844 AM → 11:39:19.555 AM
Ran python3 analyze.py | grep -v "img missing width/height" | sed -n '/## metadata/,$p'11:39:19.522 AM → 11:39:22.124 AM
Thought11:39:24.959 AM → 11:39:51.728 AM
Ran echo "=== files ===" + 15 commands11:39:51.677 AM → 11:39:52.810 AM
Thought11:39:55.241 AM → 11:40:00.869 AM
Ran echo "=== SmartScreen mentions ===" + 18 commands11:40:00.802 AM → 11:40:02.688 AM
Thought11:40:06.715 AM → 11:40:19.745 AM
Ran python3 - <<'PY' + 16 commands11:40:19.683 AM → 11:40:23.825 AM
Thought11:40:26.641 AM → 11:40:43.189 AM
Ran echo "=== independent curl jsonld ===" + 31 commands11:40:43.117 AM → 11:40:47.171 AM
Thought11:40:49.292 AM → 11:40:55.817 AM
Ran for u in /pricing/ /microsoft-warning/ /buy/ /download/ /legals/ /privacy/ /terms/ + 4 commands11:40:55.764 AM → 11:41:00.183 AM
Thought11:41:02.470 AM → 11:41:15.473 AM
Ran python3 - <<'PY' + 26 commands11:41:15.408 AM → 11:41:16.812 AM
Thought11:41:22.289 AM → 11:42:00.215 AM
Ran python3 deep.py11:42:07.903 AM → 11:42:09.186 AM
Thought11:42:11.828 AM → 11:42:27.873 AM
Ran python3 - <<'PY' + 22 commands11:42:27.797 AM → 11:42:28.951 AM
Thought11:42:31.672 AM → 11:42:43.788 AM
Ran echo "=== fragment hrefs ===" + 18 commands11:42:43.728 AM → 11:42:45.336 AM
Thought11:42:47.705 AM → 11:43:01.629 AM
Ran echo "=== same-page fragment hrefs ===" + 16 commands11:43:01.547 AM → 11:43:03.058 AM
Thought11:43:05.587 AM → 11:43:13.114 AM
Ran echo "=== full config.js ===" + 12 commands11:43:13.043 AM → 11:43:15.824 AM
Thought11:43:18.392 AM → 11:43:40.443 AM
Ran python3 - <<'PY' + 39 commands11:43:40.373 AM → 11:43:41.770 AM
Thought11:43:45.046 AM → 11:44:02.932 AM
Ran python3 - <<'PY' + 15 commands3 files11:44:02.852 AM → 11:44:04.190 AM
Thought11:44:08.783 AM → 11:44:46.799 AM
Ran mkdir -p dl + 11 commands2 files11:44:46.700 AM → 11:44:48.761 AM
Thought11:44:53.223 AM → 11:44:56.812 AM
Ran unzip -o -q tr.zip -d tr + 15 commands11:44:56.731 AM → 11:44:58.504 AM
Thought11:45:01.501 AM → 11:45:22.115 AM
Ran for u in /guides/smartscreen/ /install-sse.sh /api/licenses/verify /api/subscribe /guides/microsoft-warning/ /microsoft-warning/ /smart-search/ /compare/pricin…11:45:22.046 AM → 11:45:26.629 AM
Thought11:45:29.200 AM → 11:45:45.575 AM
Ran curl -sS -A "Mozilla/5.0" -o thanks.html https://totalrecalls.app/thanks/ + 27 commands11:45:45.486 AM → 11:45:47.638 AM
Thought11:45:51.026 AM → 11:46:09.067 AM
Ran python3 - <<'PY' + 26 commands11:46:08.986 AM → 11:46:10.640 AM
Thought11:46:14.217 AM → 11:46:21.958 AM
Ran python3 - <<'PY' + 10 commands11:46:21.869 AM → 11:46:22.909 AM
Thought11:46:25.922 AM → 11:46:44.025 AM
Ran echo "=== Set-Cookie on site ===" + 21 commands11:46:43.931 AM → 11:46:46.413 AM
Thought11:46:49.022 AM → 11:46:58.199 AM
Ran python3 - <<'PY' + 27 commands11:46:58.109 AM → 11:46:59.408 AM
Thought11:47:02.255 AM → 11:47:19.385 AM
Ran echo "=== footer refund link ===" + 27 commands11:47:19.353 AM → 11:47:25.398 AM
Thought11:47:28.189 AM → 11:47:49.023 AM
Live-checking homepage analytics beacon, form wiring, and mobile overflow11:47:48.937 AM → 11:47:55.141 AM
Thought11:47:58.025 AM → 11:48:26.409 AM
Performed 1 browser action, ran 1 command11:48:26.327 AM → 11:48:33.645 AM
Thought11:48:37.265 AM → 11:48:59.644 AM
Ran echo "=== astro-island tags on home ===" + 25 commands11:48:59.567 AM → 11:49:02.088 AM
Thought11:49:04.872 AM → 11:49:20.956 AM
Ran echo "=== Footer component JS ===" + 16 commands11:49:20.864 AM → 11:49:22.733 AM
Thought11:49:25.683 AM → 11:49:57.183 AM
Ran echo "=== /api/subscribe headers ===" + 17 commands11:49:57.089 AM → 11:50:01.224 AM
Thought11:50:04.708 AM → 11:50:26.986 AM
Performed 1 browser action, ran 1 command11:50:26.835 AM → 11:50:40.632 AM
Thought11:50:44.002 AM → 11:51:03.480 AM
Ran echo "=== context of /pricing/ links ===" + 27 commands11:51:03.393 AM → 11:51:05.573 AM
Thought11:51:12.815 AM → 11:51:30.376 AM
Ran python3 - <<'PY' + 22 commands11:51:30.285 AM → 11:51:32.138 AM
Thought11:51:35.235 AM → 11:51:45.080 AM
Ran echo "=== footer Pricing href distribution ===" + 20 commands11:51:44.990 AM → 11:51:46.357 AM
Thought11:51:50.192 AM → 11:52:08.246 AM
Ran python3 - <<'PY' + 14 commands11:52:08.142 AM → 11:52:09.794 AM
Thought11:52:13.571 AM → 11:53:09.715 AM
Ran echo "=== folder-name claims on site ===" + 10 commands11:53:09.686 AM → 11:53:10.945 AM
Thought11:53:14.804 AM → 11:53:21.925 AM
Ran python3 - <<'PY' + 9 commands11:53:21.817 AM → 11:53:22.807 AM
Thought11:53:25.891 AM → 11:53:45.382 AM
11:54:25.679 AM
Live review complete. I crawled all 57 sitemap URLs, every linked internal asset, the two shipped ZIPs, and the post-purchase/404/legacy routes — everything below is reproducible against the live site as of 2026-11-12.
TotalRecalls.app — deficiency list
Critical (legal / trust / delivery)
1. Privacy Policy contradicts the live site's own analytics.
/privacy/ §6 says verbatim: "No cookies are set by totalrecalls.app. No analytics, tracking pixels, or advertising scripts run on it." Every page instead loads Cloudflare Insights:
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js/…" data-cf-beacon='{"token": "d811c3...687b","r":1,"spa":2}'> — and a live GET https://totalrecalls.app/cdn-cgi/rum? beacon fires on page load. Either remove the beacon or amend §6. This is a disclosure-accuracy defect, not a perf nit.
2. Missing security headers, site-wide (all 57 responses).
Only x-content-type-options: nosniff and referrer-policy: strict-origin-when-cross-origin are present. Missing: Strict-Transport-Security, Content-Security-Policy, X-Frame-Options, Permissions-Policy. One-line Cloudflare/server-layer fix.
3. Shipped SSE app breaks its own privacy contract.
Inside /downloads/TotalRecalls-Smart-Search-Engine-1.0.0.zip, TotalRecalls-Smart-Search-Engine/index.html loads <script src="https://cdn.tailwindcss.com"></script> at runtime — a third-party CDN call with no SRI, in a product whose README claims "100% Local PC Runtime — Zero Cloud Egress" and whose Privacy Policy §4/§5 lists only the model download + license check as external services. The same bundle also ships the Google Generative AI SDK (generativelanguage.googleapis.com) with no disclosure. The README references https://totalrecalls.app/install-sse.sh, which is 404.
4. Shipped TotalRecalls README is stale.
tr.zip → README.txt points SmartScreen help at https://totalrecalls.app/guides/smartscreen/, which 301-redirects to /download/ (the guide is gone). It also tells users to verify TotalRecalls-1.0.0-free-tier.zip, but the real file is TotalRecalls-1.0.0.zip. The README's certutil instructions otherwise match the published SHA-256 (595b8300…), which I confirmed against the live ZIP.
5. "Mobile" activation claim is false — and it's in structured data.
/help/: "The key covers up to 3 activations (desktop, laptop, mobile)". /compare/pricing/: table "Up to 3 (desktop, laptop, mobile)" and FAQ JSON-LD "a desktop, a laptop and a mobile device are covered." The product is Windows-only — /faq/ says "No. Windows only." and /download/ says "No Mac or mobile build yet." Because the claim sits in FAQPage JSON-LD, Google can surface it as a rich result.
6. /guides/ has no H1.
Zero <h1> tags; the page opens on an H2. Affects crawl understanding and screen-reader navigation.
High
7. Access-Control-Allow-Origin: * on /api/subscribe. Any origin can POST signups (confirmed on the 405 response headers). /api/licenses/verify needs CORS for the local app, but the subscribe endpoint does not — restrict it to the site origin.
8. /buy/ checkout is a no-JS dead end. The only buy button is <a href="#" data-tr-buy class="buy-button buy-lg">; Paddle opens via JS. config.js also looks for #checkout-pending, which does not exist on /buy/. A buyer with JS/Paddle blocked has no path to purchase.
9. Footer "Pricing" link is inconsistent and redirects. 42 pages link /pricing/ → 301 → /#pricing; the other 15 link /#pricing directly. /pricing/ is absent from the sitemap. Pick one target.
10. Seven /see-it-work/* meta descriptions are 272–338 chars (e.g. Qwen 338, Claude 322, Gemini 305) — guaranteed SERP truncation. Also over: /smart-search/ 211, /compare/claude/ 206, /compare/mistral/ 206.
11. Thin pages. /release-notes/ 282 words (one release, no history), /support/ 279 words, /guides/library-format/ 313, /guides/troubleshooting/ 350, /guides/grok/ 365, /why-this-matters/ 361.
12. Heading-order skips. /library/ and /providers/ jump h2→h4; /demo/ jumps h1→h3.
13. Images: no dimensions, no lazy loading, heavy. Every /logo.png lacks width/height (CLS risk); no <img> on the site has loading="lazy". Files: /images/search-results-window.jpg 563 KB, /demo/result.png 612 KB, /demo/poster_chatgpt.png 589 KB, /logo.png 106 KB.
14. Demo videos are 50–73 MB each (TR_website_chatgpt.mp4 73.2 MB, perplexity 70.0 MB, qwen 58.5 MB, etc.), with no <track>/transcript, and only the ChatGPT/see-it-work pages set a poster — the seven provider pages render a black frame until played.
Medium
15. Step-count inconsistency. Homepage and /demo/: "Five steps from scattered chats to one local folder". /how-it-works/: "Four steps, start to finish." /download/: "How to Use the App (4 steps)".
16. /ownership/ shows a PowerShell CLI session (totalrecalls export --provider chatgpt) that is documented nowhere and is not in the shipped ZIP (only TotalRecalls.exe + README.txt). Either ship/document it or label it as concept.
17. /download/ "Get from Microsoft Store (Free)" is ambiguous for a $24 product, and the page's "zero security prompts" claim applies only to the Store build — the portable ZIP is unsigned (README confirms SmartScreen will appear), yet the site now has no SmartScreen guidance since /microsoft-warning/ and /guides/smartscreen/ both redirect to /download/.
18. Sitemap lastmod is 2026-11-12 for all 57 URLs — it's the build date, not per-page modification, so it provides no crawl-prioritization signal.
19. Short titles (<30 chars) on 18 pages — Release Notes (13), TotalRecalls FAQ (16), About (18), Help (19), Press (20), Compare (22), Support (22), How TotalRecalls Works (22), Roadmap (22), Guides (21), Previews (23), Claude vs (23), Gemini vs (23), ChatGPT vs (24), Mistral vs (24), Why Local (24), See It Work (26), The Library (26), Download (27). /smart-search/ is 64 chars (over).
20. Short meta descriptions (<60 chars): /support/ 27, /why-this-matters/ 34, /legals/ 53, /compare/ 51, /guides/library-format/ 42, /guides/troubleshooting/ 45, /guides/own-your-ai-chat-data/ 59, /guides/grok/ 59, /how-it-works/ 56.
21. Default Library folder name is inconsistent. Site: C:\TotalRecalls\Library\. Privacy Policy §3: C:/Users/<user>/TotalRecalls-downloads/Library/. tr README: TotalRecalls-download\. SSE README: C:\Users\<user>\TotalRecalls-download\Library\.
22. /support/ (279 words) overlaps /help/ and /faq/ — three separate support entrances with duplicated Free Tier/Pro content.
23. Shipped SSE UI advertises paid upgrades the website never mentions (PII Scrubber, Fine-Tuning Pipeline, Consensus Auditor, Knowledge Graph, Embedding Benchmark) and an "export to … cloud models" dataset feature — buyers of the $29 add-on see upsells with no corresponding site page.
24. No apple-touch-icon.png or web app manifest (both 404; only /favicon.svg and /favicon.ico exist).
25. Two different signup-form implementations. 41 pages: server-rendered form + inline vanilla handler + action="/api/subscribe". 15 pages: React island (/_astro/Footer.BCZ_gPxR.js), JS-only, no action. Both work (I submitted the homepage form live and got the success state), but the split is a maintenance/consistency risk.
Low / design observations
•	Hero <h1> computes to 29 px desktop / 19 px mobile — small for the primary headline.
•	/previews/ and its two child pages are indexable and in the sitemap; they are explicitly "planned, not shipped" design notes. Decide whether they should rank.
•	Hashed /_astro/*.js assets cache for only max-age=14400 (4 h); they can be immutable, max-age=31536000.
•	The 404 page is noindex,nofollow with only a "Return to Home" link — functional but bare.
•	/press/ says "No installation required" while the Store build does install — minor.
What's already good (don't regress)
•	57/57 sitemap URLs return 200, no redirect chains except the intentional /pricing/, /microsoft-warning/, /guides/smartscreen/ legacy redirects.
•	Canonicals are self-referential on every page; no noindex on any indexable page; /thanks/ is correctly noindex, follow.
•	JSON-LD is valid on all 15 pages that have it (SoftwareApplication, FAQPage, Product, Organization) — I parsed each block.
•	Open Graph/Twitter tags complete; og-image.png is a valid 1200×630 PNG.
•	SHA-256 checksums on /download/ match the actual ZIPs (verified by download).
•	Signup form works end-to-end (live POST → success state).
•	Brotli compression active; no horizontal overflow at 390 px; robots.txt clean and /api/ correctly disallowed.
•	Privacy Policy is unusually specific and accurate about the app's data handling — the gaps are the website analytics and the SSE shipped artifacts.
Want me to turn this into a phased fix plan (with exact files/lines and a PR-ready patch list), or save it as a markdown report you can annotate?
11:36:37.556 AM → 11:54:26.192 AM
Thought11:40:26.641 AM → 11:40:43.189 AM
Ran echo "=== independent curl jsonld ===" + 31 commands11:40:43.117 AM → 11:40:47.171 AM
Thought11:40:49.292 AM → 11:40:55.817 AM
Ran for u in /pricing/ /microsoft-warning/ /buy/ /download/ /legals/ /privacy/ /terms/ + 4 commands11:40:55.764 AM → 11:41:00.183 AM
Thought11:41:02.470 AM → 11:41:15.473 AM
Ran python3 - <<'PY' + 26 commands11:41:15.408 AM → 11:41:16.812 AM
Thought11:41:22.289 AM → 11:42:00.215 AM
Ran python3 deep.py11:42:07.903 AM → 11:42:09.186 AM
Thought11:42:11.828 AM → 11:42:27.873 AM
Ran python3 - <<'PY' + 22 commands11:42:27.797 AM → 11:42:28.951 AM
Thought11:42:31.672 AM → 11:42:43.788 AM
Ran echo "=== fragment hrefs ===" + 18 commands11:42:43.728 AM → 11:42:45.336 AM
Thought11:42:47.705 AM → 11:43:01.629 AM
Ran echo "=== same-page fragment hrefs ===" + 16 commands11:43:01.547 AM → 11:43:03.058 AM
Thought11:43:05.587 AM → 11:43:13.114 AM
Ran echo "=== full config.js ===" + 12 commands11:43:13.043 AM → 11:43:15.824 AM
Thought11:43:18.392 AM → 11:43:40.443 AM
Ran python3 - <<'PY' + 39 commands11:43:40.373 AM → 11:43:41.770 AM
Thought11:43:45.046 AM → 11:44:02.932 AM
Ran python3 - <<'PY' + 15 commands3 files11:44:02.852 AM → 11:44:04.190 AM
Thought11:44:08.783 AM → 11:44:46.799 AM
Ran mkdir -p dl + 11 commands2 files11:44:46.700 AM → 11:44:48.761 AM
Thought11:44:53.223 AM → 11:44:56.812 AM
Ran unzip -o -q tr.zip -d tr + 15 commands11:44:56.731 AM → 11:44:58.504 AM
Thought11:45:01.501 AM → 11:45:22.115 AM
Ran for u in /guides/smartscreen/ /install-sse.sh /api/licenses/verify /api/subscribe /guides/microsoft-warning/ /microsoft-warning/ /smart-search/ /compare/pricin…11:45:22.046 AM → 11:45:26.629 AM
Thought11:45:29.200 AM → 11:45:45.575 AM
Ran curl -sS -A "Mozilla/5.0" -o thanks.html https://totalrecalls.app/thanks/ + 27 commands11:45:45.486 AM → 11:45:47.638 AM
Thought11:45:51.026 AM → 11:46:09.067 AM
Ran python3 - <<'PY' + 26 commands11:46:08.986 AM → 11:46:10.640 AM
Thought11:46:14.217 AM → 11:46:21.958 AM
Ran python3 - <<'PY' + 10 commands11:46:21.869 AM → 11:46:22.909 AM
Thought11:46:25.922 AM → 11:46:44.025 AM
Ran echo "=== Set-Cookie on site ===" + 21 commands11:46:43.931 AM → 11:46:46.413 AM
Thought11:46:49.022 AM → 11:46:58.199 AM
Ran python3 - <<'PY' + 27 commands11:46:58.109 AM → 11:46:59.408 AM
Thought11:47:02.255 AM → 11:47:19.385 AM
Ran echo "=== footer refund link ===" + 27 commands11:47:19.353 AM → 11:47:25.398 AM
Thought11:47:28.189 AM → 11:47:49.023 AM
Live-checking homepage analytics beacon, form wiring, and mobile overflow11:47:48.937 AM → 11:47:55.141 AM
Thought11:47:58.025 AM → 11:48:26.409 AM
Performed 1 browser action, ran 1 command11:48:26.327 AM → 11:48:33.645 AM
Thought11:48:37.265 AM → 11:48:59.644 AM
Ran echo "=== astro-island tags on home ===" + 25 commands11:48:59.567 AM → 11:49:02.088 AM
Thought11:49:04.872 AM → 11:49:20.956 AM
Ran echo "=== Footer component JS ===" + 16 commands11:49:20.864 AM → 11:49:22.733 AM
Thought11:49:25.683 AM → 11:49:57.183 AM
Ran echo "=== /api/subscribe headers ===" + 17 commands11:49:57.089 AM → 11:50:01.224 AM
Thought11:50:04.708 AM → 11:50:26.986 AM
Performed 1 browser action, ran 1 command11:50:26.835 AM → 11:50:40.632 AM
Thought11:50:44.002 AM → 11:51:03.480 AM
Ran echo "=== context of /pricing/ links ===" + 27 commands11:51:03.393 AM → 11:51:05.573 AM
Thought11:51:12.815 AM → 11:51:30.376 AM
Ran python3 - <<'PY' + 22 commands11:51:30.285 AM → 11:51:32.138 AM
Thought11:51:35.235 AM → 11:51:45.080 AM
Ran echo "=== footer Pricing href distribution ===" + 20 commands11:51:44.990 AM → 11:51:46.357 AM
Thought11:51:50.192 AM → 11:52:08.246 AM
Ran python3 - <<'PY' + 14 commands11:52:08.142 AM → 11:52:09.794 AM
Thought11:52:13.571 AM → 11:53:09.715 AM
Ran echo "=== folder-name claims on site ===" + 10 commands11:53:09.686 AM → 11:53:10.945 AM
Thought11:53:14.804 AM → 11:53:21.925 AM
Ran python3 - <<'PY' + 9 commands11:53:21.817 AM → 11:53:22.807 AM
Thought11:53:25.891 AM → 11:53:45.382 AM
11:54:25.679 AM
Live review complete. I crawled all 57 sitemap URLs, every linked internal asset, the two shipped ZIPs, and the post-purchase/404/legacy routes — everything below is reproducible against the live site as of 2026-11-12.
TotalRecalls.app — deficiency list
Critical (legal / trust / delivery)
1. Privacy Policy contradicts the live site's own analytics.
/privacy/ §6 says verbatim: "No cookies are set by totalrecalls.app. No analytics, tracking pixels, or advertising scripts run on it." Every page instead loads Cloudflare Insights:
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js/…" data-cf-beacon='{"token": "d811c3...687b","r":1,"spa":2}'> — and a live GET https://totalrecalls.app/cdn-cgi/rum? beacon fires on page load. Either remove the beacon or amend §6. This is a disclosure-accuracy defect, not a perf nit.
2. Missing security headers, site-wide (all 57 responses).
Only x-content-type-options: nosniff and referrer-policy: strict-origin-when-cross-origin are present. Missing: Strict-Transport-Security, Content-Security-Policy, X-Frame-Options, Permissions-Policy. One-line Cloudflare/server-layer fix.
3. Shipped SSE app breaks its own privacy contract.
Inside /downloads/TotalRecalls-Smart-Search-Engine-1.0.0.zip, TotalRecalls-Smart-Search-Engine/index.html loads <script src="https://cdn.tailwindcss.com"></script> at runtime — a third-party CDN call with no SRI, in a product whose README claims "100% Local PC Runtime — Zero Cloud Egress" and whose Privacy Policy §4/§5 lists only the model download + license check as external services. The same bundle also ships the Google Generative AI SDK (generativelanguage.googleapis.com) with no disclosure. The README references https://totalrecalls.app/install-sse.sh, which is 404.
4. Shipped TotalRecalls README is stale.
tr.zip → README.txt points SmartScreen help at https://totalrecalls.app/guides/smartscreen/, which 301-redirects to /download/ (the guide is gone). It also tells users to verify TotalRecalls-1.0.0-free-tier.zip, but the real file is TotalRecalls-1.0.0.zip. The README's certutil instructions otherwise match the published SHA-256 (595b8300…), which I confirmed against the live ZIP.
5. "Mobile" activation claim is false — and it's in structured data.
/help/: "The key covers up to 3 activations (desktop, laptop, mobile)". /compare/pricing/: table "Up to 3 (desktop, laptop, mobile)" and FAQ JSON-LD "a desktop, a laptop and a mobile device are covered." The product is Windows-only — /faq/ says "No. Windows only." and /download/ says "No Mac or mobile build yet." Because the claim sits in FAQPage JSON-LD, Google can surface it as a rich result.
6. /guides/ has no H1.
Zero <h1> tags; the page opens on an H2. Affects crawl understanding and screen-reader navigation.
High
7. Access-Control-Allow-Origin: * on /api/subscribe. Any origin can POST signups (confirmed on the 405 response headers). /api/licenses/verify needs CORS for the local app, but the subscribe endpoint does not — restrict it to the site origin.
8. /buy/ checkout is a no-JS dead end. The only buy button is <a href="#" data-tr-buy class="buy-button buy-lg">; Paddle opens via JS. config.js also looks for #checkout-pending, which does not exist on /buy/. A buyer with JS/Paddle blocked has no path to purchase.
9. Footer "Pricing" link is inconsistent and redirects. 42 pages link /pricing/ → 301 → /#pricing; the other 15 link /#pricing directly. /pricing/ is absent from the sitemap. Pick one target.
10. Seven /see-it-work/* meta descriptions are 272–338 chars (e.g. Qwen 338, Claude 322, Gemini 305) — guaranteed SERP truncation. Also over: /smart-search/ 211, /compare/claude/ 206, /compare/mistral/ 206.
11. Thin pages. /release-notes/ 282 words (one release, no history), /support/ 279 words, /guides/library-format/ 313, /guides/troubleshooting/ 350, /guides/grok/ 365, /why-this-matters/ 361.
12. Heading-order skips. /library/ and /providers/ jump h2→h4; /demo/ jumps h1→h3.
13. Images: no dimensions, no lazy loading, heavy. Every /logo.png lacks width/height (CLS risk); no <img> on the site has loading="lazy". Files: /images/search-results-window.jpg 563 KB, /demo/result.png 612 KB, /demo/poster_chatgpt.png 589 KB, /logo.png 106 KB.
14. Demo videos are 50–73 MB each (TR_website_chatgpt.mp4 73.2 MB, perplexity 70.0 MB, qwen 58.5 MB, etc.), with no <track>/transcript, and only the ChatGPT/see-it-work pages set a poster — the seven provider pages render a black frame until played.
Medium
15. Step-count inconsistency. Homepage and /demo/: "Five steps from scattered chats to one local folder". /how-it-works/: "Four steps, start to finish." /download/: "How to Use the App (4 steps)".
16. /ownership/ shows a PowerShell CLI session (totalrecalls export --provider chatgpt) that is documented nowhere and is not in the shipped ZIP (only TotalRecalls.exe + README.txt). Either ship/document it or label it as concept.
17. /download/ "Get from Microsoft Store (Free)" is ambiguous for a $24 product, and the page's "zero security prompts" claim applies only to the Store build — the portable ZIP is unsigned (README confirms SmartScreen will appear), yet the site now has no SmartScreen guidance since /microsoft-warning/ and /guides/smartscreen/ both redirect to /download/.
18. Sitemap lastmod is 2026-11-12 for all 57 URLs — it's the build date, not per-page modification, so it provides no crawl-prioritization signal.
19. Short titles (<30 chars) on 18 pages — Release Notes (13), TotalRecalls FAQ (16), About (18), Help (19), Press (20), Compare (22), Support (22), How TotalRecalls Works (22), Roadmap (22), Guides (21), Previews (23), Claude vs (23), Gemini vs (23), ChatGPT vs (24), Mistral vs (24), Why Local (24), See It Work (26), The Library (26), Download (27). /smart-search/ is 64 chars (over).
20. Short meta descriptions (<60 chars): /support/ 27, /why-this-matters/ 34, /legals/ 53, /compare/ 51, /guides/library-format/ 42, /guides/troubleshooting/ 45, /guides/own-your-ai-chat-data/ 59, /guides/grok/ 59, /how-it-works/ 56.
21. Default Library folder name is inconsistent. Site: C:\TotalRecalls\Library\. Privacy Policy §3: C:/Users/<user>/TotalRecalls-downloads/Library/. tr README: TotalRecalls-download\. SSE README: C:\Users\<user>\TotalRecalls-download\Library\.
22. /support/ (279 words) overlaps /help/ and /faq/ — three separate support entrances with duplicated Free Tier/Pro content.
23. Shipped SSE UI advertises paid upgrades the website never mentions (PII Scrubber, Fine-Tuning Pipeline, Consensus Auditor, Knowledge Graph, Embedding Benchmark) and an "export to … cloud models" dataset feature — buyers of the $29 add-on see upsells with no corresponding site page.
24. No apple-touch-icon.png or web app manifest (both 404; only /favicon.svg and /favicon.ico exist).
25. Two different signup-form implementations. 41 pages: server-rendered form + inline vanilla handler + action="/api/subscribe". 15 pages: React island (/_astro/Footer.BCZ_gPxR.js), JS-only, no action. Both work (I submitted the homepage form live and got the success state), but the split is a maintenance/consistency risk.
Low / design observations
•	Hero <h1> computes to 29 px desktop / 19 px mobile — small for the primary headline.
•	/previews/ and its two child pages are indexable and in the sitemap; they are explicitly "planned, not shipped" design notes. Decide whether they should rank.
•	Hashed /_astro/*.js assets cache for only max-age=14400 (4 h); they can be immutable, max-age=31536000.
•	The 404 page is noindex,nofollow with only a "Return to Home" link — functional but bare.
•	/press/ says "No installation required" while the Store build does install — minor.
What's already good (don't regress)
•	57/57 sitemap URLs return 200, no redirect chains except the intentional /pricing/, /microsoft-warning/, /guides/smartscreen/ legacy redirects.
•	Canonicals are self-referential on every page; no noindex on any indexable page; /thanks/ is correctly noindex, follow.
•	JSON-LD is valid on all 15 pages that have it (SoftwareApplication, FAQPage, Product, Organization) — I parsed each block.
•	Open Graph/Twitter tags complete; og-image.png is a valid 1200×630 PNG.
•	SHA-256 checksums on /download/ match the actual ZIPs (verified by download).
•	Signup form works end-to-end (live POST → success state).
•	Brotli compression active; no horizontal overflow at 390 px; robots.txt clean and /api/ correctly disallowed.
•	Privacy Policy is unusually specific and accurate about the app's data handling — the gaps are the website analytics and the SSE shipped artifacts.
Want me to turn this into a phased fix plan (with exact files/lines and a PR-ready patch list), or save it as a markdown report you can annotate?
11:36:37.556 AM → 11:54:26.192 AM
Self-improvement reviewSkill 'website-audit' patched · Skill 'website-audit' patched (references/deterministic-checks.md) · Skill 'astro-marketing-pages' patched
Please generate a phased fix plan with exact files/line
1:25:56.004 PM
Thought1:26:04.374 PM → 1:26:12.039 PM
Explored site, ran 1 command, 1 tool call failed1:26:11.919 PM → 1:26:15.607 PM
Thought1:26:22.218 PM → 1:26:25.607 PM
Explored TotalRecalls-Source Code, ran 1 command1:26:25.503 PM → 1:26:42.346 PM
Thought1:26:46.047 PM → 1:26:51.757 PM
Explored BaseLayout.astro, ran 1 command1:26:51.688 PM → 1:26:54.136 PM
Thought1:26:57.672 PM → 1:27:06.402 PM
Explored 2 files, ran 1 command1:27:06.278 PM → 1:27:08.719 PM
Thought1:27:13.427 PM → 1:27:24.168 PM
Explored gen-sitemap.mjs, ran 1 command1:27:24.108 PM → 1:27:26.616 PM
Thought1:27:31.116 PM → 1:27:50.075 PM
Ran echo "=== landing/tr ===" + 11 commands1:27:49.999 PM → 1:27:52.514 PM
Thought1:27:55.858 PM → 1:28:07.090 PM
Explored 4 files1:28:07.003 PM → 1:28:08.744 PM
Thought1:28:12.479 PM → 1:28:21.183 PM
Explored 2 files, ran 1 command1:28:21.116 PM → 1:28:23.970 PM
Thought1:28:31.222 PM → 1:28:38.522 PM
Explored index.astro, ran 1 command1:28:38.461 PM → 1:28:40.849 PM
Thought1:28:44.697 PM → 1:28:59.371 PM
Explored 2 files, ran 1 command1:28:59.312 PM → 1:30:29.329 PM
Thought1:30:33.283 PM → 1:30:42.496 PM
Ran 2 commands1:30:42.460 PM → 1:30:44.641 PM
Thought1:30:48.492 PM → 1:31:03.432 PM
Explored serve.py, ran 1 command1:31:03.394 PM → 1:31:08.952 PM
Thought1:31:13.637 PM → 1:31:34.127 PM
Ran echo "=== public/downloads ===" + 16 commands1:31:34.101 PM → 1:31:37.459 PM
Thought1:31:41.458 PM → 1:31:59.771 PM
Ran echo "=== _headers honored? probe demo mp4 ===" + 13 commands1:31:59.739 PM → 1:32:01.598 PM
Thought1:32:05.166 PM → 1:32:17.799 PM
Ran 2 commands1:32:17.654 PM → 1:32:19.883 PM
Thought1:32:24.260 PM → 1:32:48.631 PM
Ran echo "=== functions dir ===" + 7 commands1:32:48.577 PM → 1:33:45.234 PM
Thought1:33:49.524 PM → 1:33:50.526 PM
Read subscribe.js1:33:50.420 PM → 1:33:51.750 PM
Thought1:33:55.873 PM → 1:34:06.611 PM
1:34:06.611 PM → 1:35:46.211 PM
Repo is at C:\Users\break\Projects\TotalRecalls-Source Code (branch main, tip 340bfd0). Paths below are relative to that root. Line numbers are current as of that commit.
Platform note that determines where fixes go: the live site honors site/public/_redirects and site/public/_headers (verified: /previews/notion/ → /smart-search/, and /demo/totalrecalls-lemon-squeezy-demo.mp4 returns Cache-Control: no-store, max-age=0 + 410), and the 404 body matches site/dist/404.html. So production is Cloudflare Pages serving site/dist, not the Cloud Run/serve.py path. The Cloudflare analytics beacon is not in the repo (grep for cloudflareinsights/cf-beacon over src/, public/, astro.config.mjs returns nothing) — it is injected at the edge by the zone's Web Analytics setting. That is why the privacy policy contradicts it.
Phase 0 — Preconditions (no code change)
#	Action	Why
0.1	Confirm the Pages project's build command is npm run build and that the deploy is from main	site/package.json:18 build = astro build && node scripts/gen-sitemap.mjs
0.2	Cut a branch fix/launch-defects-2026-11-12 from main	main is clean except untracked dist/TotalRecalls/, dist/TotalRecalls_1.0.1.0_x64.msix
0.3	Snapshot the live baseline (already captured): 57 sitemap URLs, headers, ZIP hashes	Rollback point
Phase 1 — Trust & legal (do first; independent of everything else)
1.1 Analytics vs Privacy Policy
Evidence: live pages load https://static.cloudflareinsights.com/beacon.min.js/… with data-cf-beacon token d811c3c4e4b043f5be8d4bf5ce97687b, and GET /cdn-cgi/rum? fires. site/src/pages/privacy/index.astro:95 says "No analytics, tracking pixels, or advertising scripts run on it." site/src/pages/legals/index.astro:33 says "No telemetry. No analytics… No cookies on this website."
Fix (choose one):
•	A (recommended): Cloudflare dashboard → zone totalrecalls.app → Analytics & Logs → Web Analytics → turn off (or remove the site token). No repo change. Re-deploy not required.
•	B: keep analytics, amend the copy: 
o	site/src/pages/privacy/index.astro:92-97 (§6) → disclose Cloudflare Web Analytics + the tr-theme localStorage key.
o	site/src/pages/legals/index.astro:33 → drop "No cookies on this website" only if a cookie is actually set (we observed no Set-Cookie, so the cookie claim is fine; the analytics claim is not).
•	C (compromise): keep analytics but strip the injected script at the edge with a Transform Rule, and keep the policy as-is.
Verify: curl -s https://totalrecalls.app/ | grep -c cloudflareinsights → 0, or the policy text matches reality.
1.2 Security headers
File: site/public/_headers (currently 7 lines, only the demo no-store rule).
Fix: append:
/*
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  X-Frame-Options: DENY
  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.paddle.com https://static.cloudflareinsights.com; frame-src https://cdn.paddle.com; connect-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; font-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'
(X-Content-Type-Options and Referrer-Policy are already set at the edge; repeat them in _headers so they survive an origin move.)
Caveat: 'unsafe-inline' is required by the inline theme script (BaseLayout.astro:29-68), the JSON-LD blocks, and the Astro island runtime. A nonce-based CSP is the proper fix but needs templating — do it in Phase 5 if desired.
Verify: curl -D - -o /dev/null https://totalrecalls.app/ | grep -iE 'strict-transport|content-security|frame-options|permissions-policy'.
1.3 False "mobile" activation claim (also in structured data)
•	site/src/pages/help/index.astro:39 — (desktop, laptop, mobile) → (desktop, laptop, or work PC).
•	site/src/pages/compare/pricing/index.astro:7 — FAQ answer "a desktop, a laptop and a mobile device are covered" → drop "mobile". This same array generates the FAQPage JSON-LD (:16-24, rendered at :27), so the fix propagates to the rich result.
•	site/src/pages/compare/pricing/index.astro:44 — table cell Up to 3 (desktop, laptop, mobile) ×2 → Up to 3 (e.g. desktop, laptop, work PC).
•	Cross-check: site/src/pages/compare/claude/index.astro:53 and site/src/pages/faq/index.astro ("No. Windows only.") are correct; keep them.
1.4 Shipped SSE app breaks its own privacy contract
•	Modules/smart-search-engine/index.html:7 — <script src="https://cdn.tailwindcss.com"></script> (runtime third-party CDN, no SRI). Fix: vendor a compiled Tailwind CSS into the module (the site already builds Tailwind via @astrojs/tailwind), or ship a static stylesheet. This is the "Zero Cloud Egress" claim in Modules/smart-search-engine/README-SSE.md (line 5) and site/src/pages/privacy/index.astro:73-75.
•	Modules/smart-search-engine/README-SSE.md — references https://totalrecalls.app/install-sse.sh (404). Remove or create the file.
•	site/src/pages/privacy/index.astro:84-90 (§5 Third-party services) — add the Tailwind CDN and the Google Generative AI SDK shipped in dist/bundle.js if either can be invoked from the UI; otherwise state they are bundled-but-inert.
•	Also fix Modules/smart-search-engine/index.html:5 title (TotalRecalls - Local AI Chat Downloader, Vector Search & RAG SQL) — it describes the Downloader, not the SSE add-on.
Verify: unzip the rebuilt SSE ZIP, confirm no cdn.tailwindcss.com reference and no 404 URLs in the README.
1.5 Shipped TotalRecalls ZIP is stale
•	Live /downloads/TotalRecalls-1.0.0.zip (built 2026-11-07) contains the old README; site/public/downloads/README.txt was updated 2026-11-10 and says "FIRST RUN (WINDOWS)" with Microsoft Store wording, while the ZIP says "FIRST RUN (WINDOWS SMARTSCREEN)" and links https://totalrecalls.app/guides/smartscreen/ (which 301s to /download/).
•	Fix: 
o	site/public/downloads/README.txt:47 (VERIFYING) — certutil -hashfile TotalRecalls-1.0.0-free-tier.zip SHA256 → TotalRecalls-1.0.0.zip.
o	site/public/downloads/README.txt QUICK START step 3 — TotalRecalls-download\ → C:\TotalRecalls\Library\ (match the site; see 4.6).
o	tools/_repackage_free_zip.py:8 — output name TotalRecalls-1.0.0-free-tier.zip → TotalRecalls-1.0.0.zip (the URL linked at site/src/pages/download/index.astro:12).
o	tools/release_gate.py:26 — same filename correction.
o	Re-run tools/_repackage_free_zip.py, then update site/src/pages/download/index.astro:14 (SHA256) and :13 (ZIP_SIZE_MB) from the script output.
Verify: sha256sum of the new ZIP equals the constant at download/index.astro:14; unzip -p … README.txt matches site/public/downloads/README.txt.
1.6 /guides/ has no H1
•	site/src/pages/guides/index.astro:14 renders <main id="guides"> → site/src/components/landing/Guides.jsx, which opens with an Eyebrow/h2 and has zero <h1>.
•	Fix: add an <h1> in Guides.jsx (e.g. "Guides — download and back up your AI chats") and demote the existing top heading to h2. Keep site/src/pages/guides/index.astro:9 title as-is.
Phase 2 — Checkout & conversion
2.1 /buy/ buy button is a no-JS dead end
•	site/src/pages/buy/index.astro:22 — <a href="#" data-tr-buy class="buy-button buy-lg">. data-tr-buy is handled in site/public/js/config.js (the IIFE at the end) which calls Paddle.Checkout.open.
•	site/public/js/config.js also does document.getElementById("checkout-pending") — that element does not exist on /buy/ (or anywhere).
•	Fix: give the anchor a real fallback href="/buy/#checkout" is pointless; instead point it at /download/ is wrong. Correct fix: add a <div id="checkout-pending" hidden> plus a <noscript> block with a mailto/support path, and make the JS handler fall back to window.location = "/thanks/" only after a successful Paddle event. Minimum viable: add id="checkout-pending" and a <noscript>Checkout needs JavaScript — email support@totalrecalls.app…</noscript>.
•	Same pattern at site/src/pages/compare/index.astro:62 and site/src/pages/guides/*/index.astro (grep data-tr-buy).
2.2 CORS wildcard on the subscribe endpoint
•	functions/api/subscribe.js:14-18 sets Access-Control-Allow-Origin: * on every response (confirmed live on the 405).
•	Fix: replace "*" with the site origin, e.g.: 
•	const origin = request.headers.get("Origin");
•	const ALLOWED = new Set(["https://totalrecalls.app", "https://www.totalrecalls.app"]);
•	const CORS = {
•	  "Access-Control-Allow-Origin": origin && ALLOWED.has(origin) ? origin : "https://totalrecalls.app",
•	  "Access-Control-Allow-Methods": "POST, OPTIONS",
•	  "Access-Control-Allow-Headers": "Content-Type",
•	  "Vary": "Origin",
•	};
(/api/licenses/verify legitimately needs CORS for the local browser-based SSE app — leave that one.)
•	Also note functions/api/subscribe.js:56 stores Referer — fine, but the source field is never used; harmless.
2.3 Two divergent signup forms
•	site/src/components/Footer.astro:91-121 + inline script :393-434 (41 pages) vs site/src/components/landing/tr/Footer.jsx:60-161 (15 pages). Both POST to /api/subscribe; both work (verified live). The React version has no action (JS-only); the Astro version has a no-JS fallback.
•	Fix: pick one. Cheapest: leave both but add action="/api/subscribe" method="post" to Footer.jsx:99 so it degrades. Effort S.
Phase 3 — SEO metadata & structure
3.1 Footer "Pricing" link inconsistency
•	site/src/components/Footer.astro:10 → href: "/pricing/" (42 pages) → 301 → /#pricing.
•	site/src/components/landing/tr/Footer.jsx:16 → href: "/#pricing" (15 pages).
•	Fix: change Footer.astro:10 to "/#pricing". Keep site/public/_redirects /pricing /#pricing 301 for legacy/bookmarked URLs. Effort XS.
3.2 Over-long meta descriptions (SERP truncation)
•	site/src/pages/see-it-work/[provider].astro:17 builds description = \demo.introArealscreenrecordingof… —‘demo.intro‘livesin‘site/src/components/landing/tr/SeeItWorkDemos.js‘;resultsare272–338chars(Qwen338,Claude322,Gemini305,Grok303,Mistral287,Perplexity275,DeepSeek272).∗∗Fix:∗∗truncateto≤155in‘[provider].astro:17‘(e.g.‘constdescription=(demo.intro+"Arealscreenrecording…").slice(0,155).replace(/\s+§∗{demo.intro} A real screen recording of …\ — `demo.intro` lives in `site/src/components/landing/tr/SeeItWorkDemos.js`; results are 272–338 chars (Qwen 338, Claude 322, Gemini 305, Grok 303, Mistral 287, Perplexity 275, DeepSeek 272). **Fix:** truncate to ≤155 in `[provider].astro:17` (e.g. `const description = (demo.intro + " A real screen recording…").slice(0,155).replace(/\s+\S*demo.introArealscreenrecordingof… —‘demo.intro‘livesin‘site/src/components/landing/tr/SeeItWorkDemos.js‘;resultsare272–338chars(Qwen338,Claude322,Gemini305,Grok303,Mistral287,Perplexity275,DeepSeek272).∗∗Fix:∗∗truncateto≤155in‘[provider].astro:17‘(e.g.‘constdescription=(demo.intro+"Arealscreenrecording…").slice(0,155).replace(/\s+§∗/,"")`).
•	site/src/pages/smart-search/index.astro:26 (211) → shorten.
•	site/src/pages/compare/claude/index.astro:26 (206), compare/mistral/index.astro:25 (206), compare/perplexity/index.astro:26 (189), compare/grok/index.astro:25 (181), compare/deepseek/index.astro:25 (225), compare/chatgpt/index.astro:25 (173), compare/gemini/index.astro:25 (175), compare/qwen/index.astro:25 (169), compare/why-local/index.astro:23 (163), compare/why-multi-assistant/index.astro:23 (173).
•	site/src/pages/about/index.astro:18 (163) → trim.
3.3 Short titles (<30 chars) / over-long (64)
File:line	Current
site/src/pages/release-notes/index.astro:6	Release Notes (13)
site/src/pages/faq/index.astro:167	TotalRecalls FAQ (16)
site/src/pages/about/index.astro:17	About TotalRecalls (18)
site/src/pages/help/index.astro:4	Help — TotalRecalls (19)
site/src/pages/press/index.astro:4	Press — TotalRecalls (20)
site/src/pages/compare/index.astro:4	Compare — TotalRecalls (22)
site/src/pages/support/index.astro:4	Support — TotalRecalls (22)
site/src/pages/how-it-works/index.astro:4	How TotalRecalls Works (22)
site/src/pages/roadmap/index.astro:4	Roadmap — TotalRecalls (22)
site/src/pages/guides/index.astro:9	Guides · TotalRecalls (21)
site/src/pages/previews/index.astro:4	Previews — TotalRecalls (23)
site/src/pages/compare/chatgpt/index.astro:25	ChatGPT vs. TotalRecalls (24)
site/src/pages/compare/claude/index.astro:26	Claude vs. TotalRecalls (23)
site/src/pages/compare/gemini/index.astro:25	Gemini vs. TotalRecalls (23)
site/src/pages/compare/grok/index.astro:25	Grok vs. TotalRecalls (21)
site/src/pages/compare/mistral/index.astro:25	Mistral vs. TotalRecalls (24)
site/src/pages/compare/qwen/index.astro:25	Qwen vs. TotalRecalls (21)
site/src/pages/compare/why-local/index.astro:23	Why Local — TotalRecalls (24)
site/src/pages/library/index.astro:9	The Library · TotalRecalls (26)
site/src/pages/see-it-work/index.astro:9	See It Work · TotalRecalls (26)
site/src/pages/download/index.astro:20	Download TotalRecalls 1.0.0 (27)
site/src/pages/compare/perplexity/index.astro:26	Perplexity vs. TotalRecalls (27)
site/src/pages/privacy/index.astro:5	Privacy Policy — TotalRecalls (29)
site/src/pages/smart-search/index.astro:25	64 chars (over)
These are all brand-prefixed and descriptive; the win is adding the keyword (e.g. Release Notes — TotalRecalls, Download TotalRecalls 1.0.0 for Windows 10/11). Effort S each.
3.4 Short meta descriptions (<60)
support/index.astro:4 (27), why-this-matters/index.astro:4 (34), legals/index.astro:10 (53), compare/index.astro:4 (51), guides/library-format/index.astro:4 (42), guides/troubleshooting/index.astro:4 (45), guides/own-your-ai-chat-data/index.astro:7 (59), guides/grok/index.astro:4 (59), how-it-works/index.astro:4 (56).
3.5 Heading-order skips
•	site/src/components/landing/tr/LibraryPage.jsx:226 (h2) → :264 (h4) — insert h3s or change :264 to h3.
•	site/src/components/landing/tr/ProvidersPage.jsx:243 (h2) → :293,:307 (h4) and :331 (h2) → :343 (h4).
•	site/src/components/landing/tr/DemoPage.jsx:27 (h1) → :40 (h3) — insert an h2 or change :40 to h2.
3.6 Sitemap lastmod is identical for all 57 URLs
•	site/scripts/gen-sitemap.mjs:28-48 is correct in principle (git dates), but the deployed sitemap has 2026-11-12 for every URL — the build environment is resolving only the tip commit (or all page sources were touched by 340bfd0).
•	Fix: in gitDates(), if the resolved set of dates has fewer than ~2 distinct values, fall back to statSync(file).mtime for that page; or ensure the Pages build checks out full history. Add a guard so a single-date history doesn't stamp every URL.
•	Verify: curl -s https://totalrecalls.app/sitemap.xml | grep -o '<lastmod>[^<]*' | sort -u shows >1 date.
Phase 4 — Content accuracy & depth
4.1 Step-count inconsistency
•	site/src/components/landing/tr/HowItWorks.jsx:22 — "Five steps…"
•	site/src/components/landing/tr/DemoPage.jsx:32 — "Five steps…"
•	site/src/pages/how-it-works/index.astro:6 — "Four steps, start to finish."
•	site/src/pages/download/index.astro — "How to Use the App (4 steps)".
Fix: standardise on five (Buy, Install, Pick, Download, Search) and change how-it-works/index.astro:6 + the download page's 4-step list to five, or standardise on four and drop step 05 from the homepage/demo. Pick one.
4.2 /ownership/ PowerShell CLI mockup
•	site/src/components/landing/tr/OwnershipPage.jsx:11 — totalrecalls export --provider chatgpt. Not documented anywhere and not in the shipped ZIP (site/public/downloads/TotalRecalls-1.0.0.zip contains only TotalRecalls.exe + README.txt).
Fix: either ship/document the CLI or change the mockup to a GUI action. Effort S.
4.3 /download/ Store label + missing SmartScreen guidance
•	site/src/pages/download/index.astro:57 — Get from Microsoft Store (Free) → Get from Microsoft Store (the "(Free)" reads as "the app is free").
•	site/src/pages/download/index.astro:45 — "zero security prompts" is Store-only; the portable ZIP is unsigned (site/src/pages/roadmap/index.astro:27 confirms). Add a short SmartScreen note for the portable path, or restore a guide page. The assets exist at site/public/smartscreen/*.png (4 files, currently orphaned).
•	site/public/_redirects:13-14 sends /guides/smartscreen/ → /download/; if you restore the guide, remove those two lines.
4.4 Thin pages
•	site/src/pages/release-notes/index.astro:17-25 + site/src/data/releases.json (one release, 4 bullets, 282 words). Add the pre-launch history or a "what's next" section.
•	site/src/pages/support/index.astro (279 words, 14 lines) — merge with /help/ or expand with the most common tickets.
•	site/src/pages/guides/troubleshooting/index.astro, guides/grok/index.astro, guides/library-format/index.astro, why-this-matters/index.astro — expand beyond 300–400 words.
4.5 /support/ overlaps /help/ and /faq/
Three support entrances. Either differentiate clearly (support = contact, help = how-to, faq = answers) and cross-link, or merge /support/ into /help/. Effort M.
4.6 Default Library folder name is inconsistent
•	site/src/pages/privacy/index.astro:48 — C:/Users/<your user name>/TotalRecalls-downloads/Library/<provider>/home/
•	site/public/downloads/README.txt QUICK START step 3 — TotalRecalls-download\
•	Modules/smart-search-engine/README-SSE.md:14 — C:\Users\<YourUsername>\TotalRecalls-download\Library\
•	Site default shown to buyers: C:\TotalRecalls\Library\ (e.g. site/src/components/landing/tr/Hero.jsx, LibraryPage.jsx)
Fix: pick one canonical default and make all four agree. Note the privacy policy's "historical folder name we kept" wording may be accurate for the state folder vs the download folder — if so, say which is which explicitly.
4.7 SSE bundle advertises undisclosed paid upgrades
Modules/smart-search-engine/dist/bundle.js contains UI for PII Scrubber, Fine-Tuning Pipeline, Consensus Auditor, Knowledge Graph, Embedding Benchmark (all "separate purchases, not included") and an "export to … cloud models" dataset feature. None are described on site/src/pages/smart-search/index.astro. Either document them or remove the upsell copy from the shipped build.
Phase 5 — Performance & accessibility polish
5.1 Images: no dimensions, no lazy loading, heavy
•	site/src/components/landing/Nav.jsx:52 — <img src="/logo.png" …> no width/height.
•	site/src/components/landing/tr/Footer.jsx:170 — same.
•	site/src/components/Footer.astro:58 — same.
•	site/src/components/landing/tr/SearchSection.jsx:43-48 — /images/search-results-window.jpg (563 KB) no dimensions/lazy.
•	site/src/pages/smart-search/index.astro:94-99 and :205-210 — same image twice.
•	site/src/components/landing/tr/SeeItWorkPage.jsx:192-197 — /demo/result.png (612 KB).
Fix: add width/height (or style aspect) and loading="lazy" decoding="async" to all except the above-the-fold logo; recompress search-results-window.jpg, result.png, poster_chatgpt.png (588 KB) with sharp (already a dependency) or squoosh. Effort M.
5.2 Videos: 50–73 MB, no captions, inconsistent poster
•	site/src/components/landing/tr/SeeItWorkPage.jsx:123-131 — poster={demo.poster || undefined}; only ChatGPT has a poster (SeeItWorkDemos.js), so 7 provider pages render a black frame.
•	site/src/components/landing/tr/DemoPage.jsx:156-165 and DemoSection.jsx:20-29 — poster present.
•	No <track>/transcript anywhere.
Fix: add a poster per provider in SeeItWorkDemos.js; re-encode the eight MP4s (50–73 MB each) to a sane bitrate (they're 1080p screen recordings — target 8–15 MB); add a text transcript per video (the videos have no audio, so a transcript is the only accessible text). Effort L.
5.3 Hero H1 size
•	site/src/components/landing/tr/Hero.jsx:32 — text-[19px] md:text-[29px]. The section H2 at HowItWorks.jsx:22 is text-[28px] md:text-[36px], so the H1 is smaller than the H2. Fix: raise the hero to text-[34px] md:text-[52px] or lower the section headings. Design call — flag for your approval.
5.4 Favicons / manifest
•	site/src/layouts/BaseLayout.astro:88 links only /favicon.svg. /favicon.png, /apple-touch-icon.png, /site.webmanifest all 404. Add an apple-touch-icon (180×180) and optionally a web manifest. Effort XS.
5.5 Asset caching
•	site/public/_headers — add /_astro/* → Cache-Control: public, max-age=31536000, immutable (hashed assets; currently 4 h).
5.6 /previews/ indexability
•	site/src/pages/previews/index.astro:4 and the two children are indexable and in the sitemap, but the page says "planned, not shipped". Decide: keep indexable (fine for SEO) or add robots="noindex, follow" to previews/index.astro:4 and children.
Phase 6 — Suggested execution order
1.	Phase 1.1 + 1.2 (edge config + _headers) — highest risk, no deploy needed for 1.1A.
2.	Phase 1.3, 1.5, 1.6 — small, verifiable, one deploy.
3.	Phase 2.1, 2.2 — checkout + CORS.
4.	Phase 3.1–3.6 — one metadata/SEO deploy.
5.	Phase 4 — content pass.
6.	Phase 5 — polish; 5.2 is the big one.
Two decisions I need from you before writing patches:
•	1.1: disable Cloudflare analytics (A) or amend the policy (B)?
•	4.1: standardise on four steps or five?
Say the word and I'll start with Phase 1.1/1.2 + 1.3

