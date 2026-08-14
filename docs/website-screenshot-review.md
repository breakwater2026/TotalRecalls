# TotalRecalls Website — Screenshot Review Pack

**For:** AI review model (e.g., Gemini 3.5 Flash)
**Source:** Live deployment of the RedesignV3 branch (Astro static site)
**URL reviewed:** https://totalrecalls-web-redesign-96283906207.us-central1.run.app
**Date:** 2026-08-13
**Screenshots:** 42 PNG files in `sections/` (also bundled as `totalrecalls-site-screenshots.zip`)

---

## How to use this pack

- Each section below lists one page and its screenshots in **top-to-bottom reading order**.
- Image paths are **relative to this document's folder** (`sections/<name>.png`).
- If your platform cannot load local image paths, use the HTTP mirror:
  `http://192.168.2.60:8790/sections/<name>.png`
  (served from the same machine; individual full URLs are listed in the appendix).
- Vision models with an image-count limit: review **one page at a time** — no page
  exceeds 8 images.

---

## Site context (read first)

TotalRecalls is a $24 one-time Windows desktop app that exports AI conversations
(ChatGPT, Claude, Perplexity, Gemini via Google Takeout, Grok) into local
Markdown + JSON files. The site is the consumer purchase front door: buy →
download → install. Built with Astro (static output), served from Google Cloud Run.

**This review round's changes (Claude Sonnet V4 review):**
1. UTF-8 charset header fix (Python http.server now serves `charset=utf-8`) — was
   causing mojibake (â / Â·) on em-dashes and middle-dots.
2. Canonical URL bug fix (`totalrecalls.appundefined` → correct per-page URLs).
3. 14-day money-back guarantee added under every buy button.
4. Gemini clarification rewritten as trust-forward copy ("Google doesn't allow
   direct chat export… Takeout JSON… 5 extra minutes first time").
5. Version badge changed to `v1.3.0 (Early Access)` + early-access line near buy
   buttons.
6. Solo-developer founder line added to the hero.

**Review questions to answer:**
- Do the new trust elements (guarantee, early-access, founder note) read well in
  context, or do they clutter the hero/CTA areas?
- Does the Gemini clarification read as solved, not hidden?
- Any layout regressions vs. the pre-review design?
- Any remaining copy inconsistencies (price, refund, version framing) across pages?
- Roadmap and Help pages appear to have empty bodies (heading only) — flag if
  that's the case in the captures.

---

## 1. Homepage (8 sections)

Read top to bottom:

1. ![Home — Hero](sections/home-01-hero.png)
2. ![Home — Why](sections/home-02-why.png)
3. ![Home — How](sections/home-03-how.png)
4. ![Home — Providers](sections/home-04-providers.png)
5. ![Home — Library](sections/home-05-library.png)
6. ![Home — Guides](sections/home-06-guides.png)
7. ![Home — Straight Talk](sections/home-07-straight.png)
8. ![Home — CTA + Footer](sections/home-08-cta-footer.png)

## 2. Pricing (4 sections)

1. ![Pricing — Launch](sections/pricing-01-launch.png)
2. ![Pricing — What You Get](sections/pricing-02-whatget.png)
3. ![Pricing — One-Time](sections/pricing-03-onetime.png)
4. ![Pricing — CTA](sections/pricing-04-cta.png)

## 3. How It Works (7 sections)

1. ![HIW — Top](sections/how-it-works-top.png)
2. ![HIW — Steps](sections/how-it-works-steps.png)
3. ![HIW — Data Lives](sections/how-it-works-data-lives.png)
4. ![HIW — Per Provider](sections/how-it-works-per-provider.png)
5. ![HIW — Questions](sections/how-it-works-questions.png)
6. ![HIW — CTA](sections/how-it-works-cta.png)
7. ![HIW — Footer](sections/how-it-works-footer.png)

## 4. Guides (4 sections)

1. ![Guides — Header](sections/guides-header.png)
2. ![Guides — Cards](sections/guides-cards.png)
3. ![Guides — CTA](sections/guides-cta.png)
4. ![Guides — Footer](sections/guides-footer.png)

## 5. Compare

![Compare](sections/compare.png)

## 6. Download

![Download](sections/download.png)

## 7. FAQ

![FAQ](sections/faq.png)

## 8. Support

![Support](sections/support.png)

## 9. Privacy Policy

![Privacy](sections/privacy.png)

## 10. Terms of Use

![Terms](sections/terms.png)

## 11. Release Notes

![Release Notes](sections/release-notes.png)

## 12. Help & Troubleshooting

![Help](sections/help.png)

## 13. Why This Matters

![Why This Matters](sections/why-this-matters.png)

## 14. Roadmap

![Roadmap](sections/roadmap.png)

## 15. Press Kit

![Press](sections/press.png)

## 16. Feature Requests

![Feature Requests](sections/feature-requests.png)

## 17. Thanks (post-purchase)

![Thanks](sections/thanks.png)

## 18. Previews index

![Previews](sections/previews-index.png)

## 19. Preview subpages (5)

1. ![Semantic Search](sections/preview-semantic-search.png)
2. ![Obsidian](sections/preview-obsidian.png)
3. ![Notion](sections/preview-notion.png)
4. ![RAG Containers](sections/preview-rag-containers.png)
5. ![Multi-Device Memory](sections/preview-multi-device-memory.png)

---

## Appendix A — full HTTP mirror URLs

Base: `http://192.168.2.60:8790/sections/`

| File | URL |
|---|---|
| home-01-hero.png | http://192.168.2.60:8790/sections/home-01-hero.png |
| home-02-why.png | http://192.168.2.60:8790/sections/home-02-why.png |
| home-03-how.png | http://192.168.2.60:8790/sections/home-03-how.png |
| home-04-providers.png | http://192.168.2.60:8790/sections/home-04-providers.png |
| home-05-library.png | http://192.168.2.60:8790/sections/home-05-library.png |
| home-06-guides.png | http://192.168.2.60:8790/sections/home-06-guides.png |
| home-07-straight.png | http://192.168.2.60:8790/sections/home-07-straight.png |
| home-08-cta-footer.png | http://192.168.2.60:8790/sections/home-08-cta-footer.png |
| pricing-01-launch.png | http://192.168.2.60:8790/sections/pricing-01-launch.png |
| pricing-02-whatget.png | http://192.168.2.60:8790/sections/pricing-02-whatget.png |
| pricing-03-onetime.png | http://192.168.2.60:8790/sections/pricing-03-onetime.png |
| pricing-04-cta.png | http://192.168.2.60:8790/sections/pricing-04-cta.png |
| how-it-works-*.png (7) | http://192.168.2.60:8790/sections/how-it-works-<label>.png |
| guides-*.png (4) | http://192.168.2.60:8790/sections/guides-<label>.png |
| compare.png | http://192.168.2.60:8790/sections/compare.png |
| download.png | http://192.168.2.60:8790/sections/download.png |
| faq.png | http://192.168.2.60:8790/sections/faq.png |
| support.png | http://192.168.2.60:8790/sections/support.png |
| privacy.png | http://192.168.2.60:8790/sections/privacy.png |
| terms.png | http://192.168.2.60:8790/sections/terms.png |
| release-notes.png | http://192.168.2.60:8790/sections/release-notes.png |
| help.png | http://192.168.2.60:8790/sections/help.png |
| why-this-matters.png | http://192.168.2.60:8790/sections/why-this-matters.png |
| roadmap.png | http://192.168.2.60:8790/sections/roadmap.png |
| press.png | http://192.168.2.60:8790/sections/press.png |
| feature-requests.png | http://192.168.2.60:8790/sections/feature-requests.png |
| thanks.png | http://192.168.2.60:8790/sections/thanks.png |
| previews-index.png | http://192.168.2.60:8790/sections/previews-index.png |
| preview-semantic-search.png | http://192.168.2.60:8790/sections/preview-semantic-search.png |
| preview-obsidian.png | http://192.168.2.60:8790/sections/preview-obsidian.png |
| preview-notion.png | http://192.168.2.60:8790/sections/preview-notion.png |
| preview-rag-containers.png | http://192.168.2.60:8790/sections/preview-rag-containers.png |
| preview-multi-device-memory.png | http://192.168.2.60:8790/sections/preview-multi-device-memory.png |

Zip bundle: http://192.168.2.60:8790/totalrecalls-site-screenshots.zip

## Appendix B — expected review output

Return findings as a numbered list grouped by page, each item marked:
- `[BLOCKER]` — must fix before launch
- `[POLISH]` — should fix
- `[NIT]` — optional

End with an overall launch-readiness verdict for the website.
