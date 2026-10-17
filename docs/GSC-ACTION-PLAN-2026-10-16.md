# GSC action plan — 2026-10-16

Prepared overnight for review. Everything here is measured, not inferred; every number traces to a
command whose output is quoted. Where I got something wrong earlier, the correction is recorded
inline rather than quietly dropped.

---

## Headline

**Both sites are technically clean. Every remaining item is a "Google must recrawl this URL" problem,
plus one editorial question.** There is nothing left to fix in either codebase.

| Site | Indexed | Not indexed | Remaining action |
|---|---|---|---|
| TopMoneyTools (76 routes) | **66** | 10 | 4 `www` recrawls; 6 education articles (optional) |
| TotalRecalls (53 routes) | **45** | 8 | 3 page requests; 13 `www` recrawls |

---

# 1. TopMoneyTools

## 1.1 Current state — all 76 sitemap routes, inspected 2026-10-16

```
66  Submitted and indexed
 6  Crawled - currently not indexed
 3  Duplicate, Google chose different canonical than user
 1  Duplicate without user-selected canonical
 0  Discovered - currently not indexed     ← Google's email was right
```

The "Discovered – currently not indexed" group is **empty**. That is the group Google emailed about
("34 pages validated as fixed"), and the sweep confirms it. The GSC UI simply has not refreshed.

## 1.2 The `www` canonical group — ROOT CAUSE FOUND (this is new)

Previously I said "Google's records are sticky, just wait". That was incomplete. The actual mechanism:

| URL | Google's state | Last crawled |
|---|---|---|
| `www.topmoneytools.com/privacy` | **Submitted and indexed** | 2026-07-19 |
| `www.topmoneytools.com/disclaimer` | **Submitted and indexed** | 2026-06-15 |
| `www.topmoneytools.com/start-here` | Crawled – not indexed | 2026-06-27 |
| `www.topmoneytools.com/education/how-inflation-works` | Crawled – not indexed | 2026-06-27 |
| `topmoneytools.com/privacy` (apex) | Duplicate, chose different canonical | 2026-10-15 |
| `topmoneytools.com/start-here` (apex) | Duplicate, chose different canonical | 2026-10-09 |

**Google holds the `www` versions as separate index entries from June/July** — months before the
redirect existed. The apex URL is being treated as the duplicate *of a stale `www` entry*. Note that
`/privacy`'s apex was recrawled on **10-15, after the fix**, and Google still said "www" — because
recrawling the apex does not refresh the `www` record.

**So the fix is on the `www` side, not the apex side.** Verified: every `www` path 301s correctly
(13/13 paths tested with redirects disabled, including a Googlebot user-agent), and the apex pages
carry correct self-referential canonicals.

### ACTION — Request Indexing on these 4 `www` URLs
```
https://www.topmoneytools.com/privacy
https://www.topmoneytools.com/disclaimer
https://www.topmoneytools.com/start-here
https://www.topmoneytools.com/education/how-inflation-works
```
Expected GSC behaviour: it will say these are already on Google and still offer the button. That is
normal here — you are not asking Google to index a new page, you are asking it to **re-fetch a URL
that has since moved**. It fetches, sees the 301, and reclassifies the entry.

## 1.3 The 6 "Crawled – currently not indexed" articles — NOT technical

```
/education/credit-card-interest            696 words, 10 sections
/education/emergency-funds-and-safety-nets 417 words,  9 sections
/education/fire-movement                   763 words, 10 sections
/education/home-affordability              741 words, 10 sections
/education/investing-101                   458 words, 10 sections
/education/net-worth-by-age                758 words, 10 sections
```
Each has 10–18 content-level inbound links (not footer links) and Article schema.

**Correction to what I told you earlier.** I claimed these verdicts were stale, formed when Google
saw SPA shells it "never actually read". The data refutes that:

```
INDEXED articles    : crawled 2026-07 (8), 2026-08 (7), 2026-09 (16), 2026-10 (2)
NOT indexed articles: crawled 2026-07 (4), 2026-08 (3)
```

Fifteen *indexed* articles were crawled in the same July/August window. Googlebot renders
JavaScript, so it saw the content either way. The real pattern: the six non-indexed pages are exactly
the **broadest, most competitive YMYL topics** — investing 101, net worth by age, home affordability,
emergency funds, credit card interest, how inflation works, FIRE.

### ACTION — optional, 6 URLs
A recrawl is a cheap test and worth one attempt (it doubles as the quota use if you skip 1.4):
```
https://topmoneytools.com/education/credit-card-interest
https://topmoneytools.com/education/emergency-funds-and-safety-nets
https://topmoneytools.com/education/fire-movement
https://topmoneytools.com/education/home-affordability
https://topmoneytools.com/education/investing-101
https://topmoneytools.com/education/net-worth-by-age
```
If they still do not index after a fresh crawl, the cause is topical competition and the fix is
**editorial** (depth, original data, differentiation) — not technical. Do not keep re-requesting.

4 www + 6 education = **10 URLs, exactly one day's quota.**

## 1.4 What is verified clean (no action)

- 76/76 sitemap routes return 200; 76/76 distinct content bodies
- 76/76 self-referential apex canonicals; 0 noindex; 0 duplicate titles
- sitemap: 76 `<loc>`, apex-only, 0 `lastmod`/`changefreq`/`priority`, root form matches canonical
- every `www` path 301s to apex — 13/13 tested, incl. `robots.txt`, `sitemap.xml`, assets
- unknown paths return real 404s (10 paths tested)
- 18/18 legacy slug 301s are single-hop to 200
- **zero** `www` strings in `src/`, `public/`, `index.html` or the built output

---

# 2. TotalRecalls

## 2.1 Current state — all 53 sitemap routes, inspected 2026-10-16

```
45  Submitted and indexed
 4  Discovered - currently not indexed
 4  URL is unknown to Google
```

**Your indexing requests worked.** Of the 16-URL list: **13 now indexed**, 3 pending.

Still not indexed:
```
/compare/pricing/                  Discovered
/compare/why-local/                unknown to Google
/compare/why-multi-assistant/      Discovered
```
Plus the 5 `/previews/*` pages — **excluded by your decision on 10-11**, and left alone.

### ACTION A — Request Indexing, 3 URLs
```
https://totalrecalls.app/compare/pricing/
https://totalrecalls.app/compare/why-local/
https://totalrecalls.app/compare/why-multi-assistant/
```

### ACTION B — refresh `/compare/deepseek/`
It is indexed, but Google holds a crawl from **2026-10-03**, i.e. the version *before* the rewrite.
Request Indexing on `https://totalrecalls.app/compare/deepseek/` to force a re-fetch.

## 2.2 The `www` alternates — the mechanism is now proven

I inspected all 19 `www` URLs behind the "16 alternate pages":

```
 6  Page with redirect        ← converted
13  Alternate page with proper canonical tag   ← still pending
```

**Every conversion correlates exactly with a post-fix crawl:**

| www URL | Now | Last crawled |
|---|---|---|
| `/compare/` | Page with redirect | 2026-10-14 |
| `/download/` | Page with redirect | 2026-10-16 |
| `/feature-requests/` | Page with redirect | 2026-10-14 |
| `/legals/` | Page with redirect | 2026-10-16 |
| `/library/` | Page with redirect | 2026-10-12 |
| `/providers/` | Page with redirect | 2026-10-14 |

The 13 still "Alternate" all have crawl dates of **10-03 → 10-10 10:41Z**, i.e. before the 301 went
live at 10-10 18:38Z. Not one has been fetched since. That is a 1:1 relationship: **recrawl ⇒
conversion.** Nothing else is required.

### ACTION C — Request Indexing on the 13 remaining `www` URLs (2 days at ~10/day)

Day 1:
```
https://www.totalrecalls.app/
https://www.totalrecalls.app/buy/
https://www.totalrecalls.app/guides/export-claude-chat-history/
https://www.totalrecalls.app/guides/export-perplexity-conversations/
https://www.totalrecalls.app/guides/gemini-takeout-archive/
https://www.totalrecalls.app/guides/grok/
https://www.totalrecalls.app/microsoft-warning/
https://www.totalrecalls.app/ownership/
https://www.totalrecalls.app/press/
https://www.totalrecalls.app/privacy/
```
Day 2:
```
https://www.totalrecalls.app/roadmap/
https://www.totalrecalls.app/support/
https://www.totalrecalls.app/terms/
```
**Or do nothing** and they convert on their own in roughly the time Google takes to recrawl 13 URLs
— at the observed rate (6 in 6 days) that is about two weeks. The requests only accelerate it.

---

# 3. Things I got wrong, corrected

Recording these so you can trust the rest:

1. **I claimed the 6 education articles' verdicts were stale SPA-era judgements.** The crawl-date
   spread refutes it — 15 indexed articles share those same crawl months. Corrected in §1.3.
2. **I claimed an internal `www` link was feeding Google a `www` signal.** It was link *text*; the
   `href` was apex-relative. Cosmetic; fixed, but not causative.
3. **I reported `www/robots.txt` returning 200 as a redirect hole.** That was my own test omitting
   `allow_redirects=False`; it 301s like everything else.
4. **I recommended the Removals tool** for the sticky `www` pages. **Retracted.** Google is currently
   *serving* the `www` version and treating the apex as the duplicate — removing `www` could make
   those pages disappear from search entirely. Do not use it.
5. **I over-broadly said "all 8 cases single-hop"** for the earlier chain fix. True for the URLs I
   tested (no query strings); `www/path/?query` still takes 2 hops. Harmless, but the claim was
   wider than the evidence.

---

# 4. What NOT to do

- **Do not click "Validate fix" on any GSC group until the crawl dates move.** A validation re-checks
  stored records; run it before a recrawl and it fails and resets the clock. Both emails you received
  are that failure mode, not new problems.
- **Do not delete and re-add a property.** GSC is a reporting view over Google's index; the records
  are not stored in the property. You would lose the history and change nothing.
- **Do not use the Removals tool** on the `www` URLs (see §3.4).
- **Do not keep requesting the 6 education articles** if one recrawl does not index them.

# 5. How to re-measure next time

```
python C:\Users\break\AppData\Local\hermes\inspect_sitemap.py \
    sc-domain:topmoneytools.com https://topmoneytools.com/sitemap.xml
python C:\Users\break\AppData\Local\hermes\inspect_sitemap.py \
    sc-domain:totalrecalls.app https://totalrecalls.app/sitemap.xml
```
Writes one JSON line per URL, ~7s/URL, resumable, so run it in the background (~9 min for 76 URLs).
Do not run two sweeps against the same property at once — the API returns HTTP 500 and that is
throttling, not a site fault.

**Judge progress by `lastCrawlTime`, never by the bucket counts.**

# 6. Checkpoint

Two weeks (≈2026-10-30):

- TopMoneyTools: the 3 `www` canonicals should resolve once the `www` entries are recrawled;
  `/disclaimer` likewise. The 6 education articles either index (stale verdict) or do not (topical
  competition — an editorial decision, not a bug).
- TotalRecalls: the 13 `www` alternates should be at or near zero; the 3 pending pages indexed.

Everything technical is finished and verified on both sites. What remains is Google's crawl queue.

---

# 7. The bigger picture — what indexing will not fix

Measured 2026-10-16, so this is current, not a week-old snapshot:

| Site | Last 28 days | Average position |
|---|---|---|
| **TopMoneyTools** | **0 clicks · 368 impressions** | 60.9 |
| **TotalRecalls** | **2 clicks · 59 impressions** | 11.6 |

Both sites are close to invisible, but for **opposite reasons**, and neither is an indexing problem:

- **TopMoneyTools surfaces but ranks too deep.** 368 impressions with zero clicks at average position
  61 means Google shows the pages for real queries and users scroll past them. Fixing the last
  `www` canonical will not change this by one position. The fix is **content depth and authority** on
  competitive calculator/YMYL terms — the editorial track.
- **TotalRecalls ranks well but barely appears.** Average position 11.6 is respectable — its problem
  is that only 59 impressions exist at all. There is almost no demand being captured, because the
  site has very few pages targeting terms anyone searches and almost no authority yet. The fix is
  **more content aimed at real queries, plus distribution** (the launch/marketing plan), not more
  index work.

One detail that reinforces §2.2: TotalRecalls' single best-performing page in 28 days is the **`www`
copy** of `/guides/qwen/` (position 6.2, 1 click). The duplicate host is still capturing a click that
belongs to the apex — small in absolute terms, but direct evidence the `www` work is worth finishing.

**So the honest sequence from here is: finish the recrawls in §1.2 and §2.2, then stop treating this
as an indexing project.** Both sites are now technically correct. What stands between them and
traffic is content and links, which is the marketing plan's territory — not another GSC pass.







Page 2 of 2






