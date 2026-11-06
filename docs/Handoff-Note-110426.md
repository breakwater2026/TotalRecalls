Handoff Note — TotalRecalls Website + SSE Add-on Work
Date: November 4, 2026
Workspace: C:\Users\break\Projects\TotalRecalls-Source Code\
Build status: 65 pages, zero errors (astro build passes)
Preview server: localhost:4321 (running as background process)

Summary of Work Completed
1. Website Palette Extraction & Application
Extracted the full color palette from totalrecalls.app (both dark and light modes) and applied it to two targets:

Downloader GUI (site/src/components/landing/tr/Hero.jsx + app_ui.html):

Replaced arbitrary dark slate palette with website colors
Dark mode: #101113 bg, #18181b panel, #2b2c31 border, #e8eaed text, #2e7ff blue accent
Light mode: #ffffff bg, #f8fafc panel, #e2e8f0 border, #020817 text
Added dark/light theme toggle button (🌓/☀️) with localStorage persistence (tr-theme)
Smart Search Engine (site/src/components/landing/tr/*.tsx):

17 component files converted from hardcoded dark/cyan/teal/emerald colors to --tr-* CSS variables
~1,900 color replacements across components
Zero cyan/teal/emerald references remain in component files
2. Smart Search Engine Website Copy (docx v2)
Applied all changes from Marketing/Website/TotalRecalls-SSE_website_copy_v2.docx:

Pricing: SSE $39 launch / $59 regular; Bundle $55 launch / $89 regular; Pro owners add SSE for $31
Renaming: "TotalRecalls Search" → "Smart Search Engine" everywhere
New page: src/pages/smart-search/index.astro (hero, 3-step how-it-works, 3 ways to search, results window, private by design, launch/coming table, pricing, requirements, closing)
FAQs: 11 SSE-related FAQs updated with new pricing and naming
Nav: Added "Smart Search" tab between Library and Search
Footer: Added "Smart Search" product link + "Using Smart Search Engine" guide link
Previews/roadmap: SSE moved from "planned" to "available today"; semantic-search preview page re-themed as shipped product page
Guides: using-totalrecalls-search updated with new pricing ($39/$59/$31/$55)
3. Homepage Hero Changes (current state)
4-line headline: Recall every AI conversation / From the Top 8 AI providers / Download them all on your PC / Search them with no restrictions
Font: text-[19px] md:text-[29px], no punctuation
3 chips above hero: New Windows 10/11 App | Take control of your personal info | Located on your PC
Asterisk line below: * Optional Smart Search Engine (SSE) sold separately - \$29 launch price.
4. Nav Bar (current state)
Logo flush left (pl-0)
First tab has ml-8 margin from logo
Tabs: HOW IT WORKS | SEE IT WORK | PROVIDERS | LIBRARY | SMART SEARCH ENGINE / (SSE) | SEARCH | GUIDES | PRICING | SUPPORT | LEGALS | DOWNLOAD
whitespace-nowrap removed from links (tabs wrap at word boundaries, no hyphenation)
hyphens: none on nav container
Download link before theme toggle; ml-6 between Legals and Download
Files Modified
Website source (site/src/):

components/landing/tr/Hero.jsx — hero text, chips, accent colors, navbar spacing
components/landing/tr/Pricing.jsx — SSE strip pricing, features, buttons, bundle card
components/landing/tr/SearchSection.jsx — SSE naming, points, buttons
components/landing/tr/Hero.jsx — hero headline (4-line), chip colors
components/landing/tr/Footer.jsx — Smart Search link
components/landing/tr/HowItWorks.jsx — step 05 chip
components/landing/tr/ProvidersPage.jsx — removed semantic search from planned
components/landing/Nav.jsx — Smart Search Engine tab with (SSE), logo spacing
components/landing/tr/SearchSection.jsx — NEW ADD-ON eyebrow, points, buttons
pages/smart-search/index.astro — NEW landing page
pages/search/index.astro — re-themed to SSE pricing/naming
pages/faq/index.astro — all SSE FAQs updated
pages/pricing/index.astro — SSE available now note
pages/roadmap/index.astro — SSE in Available today
pages/previews/index.astro — removed semantic search from previews
pages/previews/semantic-search/index.astro — rewritten as shipped product page
pages/compare/pricing/index.astro — SSE available now note
pages/guides/using-totalrecalls-search/index.astro — renamed, new pricing
src/styles/main.css — .tr-reveal opacity fix (0 → 1 so content shows without JS)
Downloader (site/ root):

app_ui.html — dark/light CSS variables, theme toggle button, persistence
Smart Search Engine (Modules/smart-search-engine/):

Components/*.tsx (17 files) — all hardcoded dark/cyan/teal/emerald → --tr-* CSS vars
App.tsx — root/footer theming, theme toggle state
index.html — CSS custom properties, darkMode class, theme init script
Open Items / Business Decisions Pending
[DATE] placeholder — launch price end date appears throughout pricing/FAQ pages; needs a real date
Refund FAQ wording — still says "case-by-case" on /pricing/ and FAQ; docx marks as DECIDE
How to Rebuild / Preview
cd C:\Users\break\Projects\TotalRecalls-Source Code\site
npx astro build          # builds to dist/
npx astro preview --port 4321 --host  # serves at localhost:4321
Preview server was running as background process when session ended. Restart with the command above if needed.


Commit but do not push.

4:39:37.553 PM
4:39:40.789 PM → 4:39:41.481 PM
4:39:41.456 PM → 4:39:43.412 PM
4:39:47.484 PM → 4:39:49.003 PM
4:39:49.003 PM → 4:39:50.761 PM
I'll stage only the files I changed, not the unrelated pre-existing untracked files:

4:39:50.707 PM → 4:39:51.743 PM
4:39:54.819 PM → 4:39:55.819 PM
4:39:55.819 PM → 4:39:57.912 PM
Build successful — 65 pages, zero errors. Restarting preview server:

4:39:57.857 PM → 4:39:59.856 PM
4:40:04.194 PM → 4:40:04.868 PM
4:40:04.681 PM → 4:40:05.618 PM
4:40:09.420 PM → 4:40:09.632 PM
4:40:09.632 PM → 4:40:10.618 PM
Committed successfully. Working tree is clean — nothing left unstaged or uncommitted.

Commit: 70ce59f Apply TotalRecalls website palette + Smart Search Engine add-on copy

48 files changed, 2629 insertions, 1294 deletions
Not pushed to origin
Everything in site/src/, Modules/smart-search-engine/, and app_ui.html is committed. The preview server is still running on localhost:4321 if you want to do a final visual check.