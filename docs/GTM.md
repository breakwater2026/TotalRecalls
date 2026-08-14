# Go-to-market — TotalRecalls

## Offer (locked)

| Item | Decision |
|------|----------|
| Price | **$24** one-time |
| Payments | **Lemon Squeezy** (MoR) |
| Delivery | Digital zip (Windows) + thanks page |
| License keys in app | Deferred |
| Primary CTA | Buy TotalRecalls — $24 |
| Secondary | Already purchased? Download zip |

## Positioning

> Own every AI conversation — export ChatGPT, Claude, Perplexity, Gemini, and Grok to your PC.

## Site structure (shipped)

| URL | Role |
|-----|------|
| `/` | Marketing + buy |
| `/thanks.html` | Post-purchase download |
| `/support.html` | Help / SmartScreen |
| `/privacy.html` | Privacy |
| `/guides/` | SEO hub |
| `/guides/export-chatgpt-conversations.html` | SEO |
| `/guides/export-claude-chat-history.html` | SEO |
| `/guides/backup-perplexity-threads.html` | SEO |
| `/guides/gemini-takeout-archive.html` | SEO |
| `/guides/own-your-ai-chat-data.html` | SEO / thesis |

Config: `site/public/js/config.js`

## 90-day checklist

### Foundation
- [ ] Lemon product live + `lemonCheckoutUrl` set
- [ ] `totalrecalls.app` DNS → Cloud Run
- [ ] HTTP/2 end-to-end stays **off**
- [ ] Test purchase → thanks → zip
- [ ] Code signing plan (conversion)

### Content distribution
- [ ] Share ChatGPT export guide in relevant communities (value-first)
- [ ] 60–90s demo video embedded later
- [ ] Show HN / PH only after signing or clear SmartScreen copy

### Paid (only after funnel works)
- [ ] Google Ads on “export chatgpt conversations” style queries ($5–10/day test)

## Metrics
- Landing → Buy click rate
- Buy → successful payment
- Support tickets: SmartScreen / blocked EXE
- Which guide refers buyers (UTM or referrer)

## Do not
- AdSense on product pages
- Promise Mac before it exists
- Collect provider session tokens server-side
