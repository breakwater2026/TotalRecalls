TotalRecalls — Request Indexing list (verified 2026-10-11 07:18 EDT via the URL Inspection API)
Source of truth: 53 sitemap routes inspected individually. State at time of writing:
  33 Submitted and indexed | 18 Discovered - currently not indexed | 2 URL is unknown to Google

The ~10/day cap applies per property, so this is a 2-sitting job.
Work top to bottom — highest commercial intent first.


=== SITTING 1 (10 URLs) — the /compare/ cluster ===

https://totalrecalls.app/compare/claude/
https://totalrecalls.app/compare/gemini/
https://totalrecalls.app/compare/grok/
https://totalrecalls.app/compare/mistral/
https://totalrecalls.app/compare/perplexity/
https://totalrecalls.app/compare/qwen/
https://totalrecalls.app/compare/pricing/
https://totalrecalls.app/compare/why-local/
https://totalrecalls.app/compare/why-multi-assistant/
https://totalrecalls.app/compare/deepseek/          <- already indexed, but Google holds the
                                                      pre-rewrite crawl from 2026-10-03


=== SITTING 2 (6 URLs) — guides and support pages ===

https://totalrecalls.app/guides/qwen/
https://totalrecalls.app/guides/deepseek/
https://totalrecalls.app/guides/library-format/
https://totalrecalls.app/guides/own-your-ai-chat-data/
https://totalrecalls.app/how-it-works/
https://totalrecalls.app/release-notes/


=== DECIDED 2026-10-11 — NOT REQUESTED (5 URLs) ===

https://totalrecalls.app/previews/
https://totalrecalls.app/previews/notion/
https://totalrecalls.app/previews/obsidian/
https://totalrecalls.app/previews/semantic-search/
https://totalrecalls.app/previews/multi-device-memory/

Owner decided 2026-10-11: leave them out of the request queue (thin pages describing
features that are not built yet; each would cost a slot in the ~10/day cap that a real
page can use). No site change was made.

Consequence worth remembering: skipping the request does NOT keep these out of Google.
They are still in the sitemap and Google already knows 4 of the 5 ("Discovered"), so
they may be indexed on their own at any time. If genuine exclusion is ever wanted, that
requires noindex on each page PLUS removing them from scripts/gen-sitemap.mjs — a
different change from this decision, and not one we made.


=== DO NOT REQUEST ===

https://totalrecalls.app/thanks/     Absent from Google entirely, now noindexed, and
                                    removed from the sitemap. Requesting it would ask
                                    Google to crawl a page we deliberately keep out.


=== ALREADY RESOLVED SINCE THE AUDIT (no action) ===

/faq/            recrawled 2026-10-11 01:50Z — the FAQPage JSON-LD fix is now picked up
/help/           now indexed
/compare/chatgpt/  recrawled 2026-10-10 19:15Z — POST-rewrite crawl, so the new content landed
/guides/smartscreen/  indexed (a transient API 500 during the sweep, not a site issue)


=== HOW TO DO EACH ONE ===

1. GSC -> the URL Inspection box at the top of the page
2. Paste the full URL, press Enter
3. Wait for it to report
4. Click REQUEST INDEXING
5. Confirm the toast reads "Indexing requested"

Do NOT click "Validate fix" on the Indexing report groups — a premature validation
fails and resets the clock. Those resolve on their own as Google recrawls.
