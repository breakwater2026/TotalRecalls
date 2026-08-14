# Lemon Squeezy setup — TotalRecalls ($24 one-time)

## Locked decisions

| Item | Value |
|------|--------|
| Provider | **Lemon Squeezy** |
| Price | **$24 USD** one-time |
| Product | TotalRecalls for Windows |
| License keys in app | **Not required for v1** (paid download first) |
| Payouts | **Wise USD balance — hold USD**, no auto-conversion (Wise has none on arrival; convert to CAD manually or via rate-triggered Auto Conversion when desired) |
| Site config | `site/public/js/config.js` → `lemonCheckoutUrl` (Astro build path; the V1 `site/js/config.js` copy was deleted) |

## API access (tested 2026-08-14)

| Item | Value |
|------|-------|
| Store | TotalRecalls Corporation · id `451756` |
| Storefront | https://totalrecalls.lemonsqueezy.com |
| Product | TotalRecalls · id `1288944` · $24 · **status: DRAFT** (publish before launch) |
| Checkout URL | https://totalrecalls.lemonsqueezy.com/checkout/buy/03e11a51-8c63-4826-8b87-998b626285c3 |
| API base | `https://api.lemonsqueezy.com/v1/` |
| Auth | `Authorization: Bearer <API_KEY>` |
| Required headers | `Accept: application/vnd.api+json` · `Content-Type: application/vnd.api+json` |
| Rate limit | 300 req/min |

### Create an API key

1. https://app.lemonsqueezy.com → **Settings → API**
2. Click **Create API key**, name it clearly (names are permanent)
3. Copy the key immediately — it's shown **once** (a ~1035-char RS256 JWT)
4. Store it in `.env` (gitignored) as `LEMON_SQUEEZY_API_KEY=…`
5. Optional: create a **Test mode** key (toggle Test mode at top of API page) for safe integration testing

### Verified working calls (key tested live)

```text
GET /v1/stores                 → 200, store list
GET /v1/products/<id>          → 200, product + buy_now_url
GET /v1/orders                 → 200, empty (0 orders)
```

Notes:
- Key `scopes: []` = full merchant access.
- `.env` at repo root holds the key; **never commit it** (gitignored).
- If the key ever leaks (chat, screenshot, transcript), rotate it: Settings → API → delete old, create new.
- Long-key chat transmission quirk: Hermes desktop compacts long unbroken strings — paste keys as multi-line chunks or attach a text file.

## Create the product

1. Sign up / log in at [lemonsqueezy.com](https://lemonsqueezy.com)
2. Create store (e.g. TotalRecalls)
3. **Products → New product**
   - Name: `TotalRecalls for Windows`
   - Price: **$24** · One-time
   - Tax category: Software (follow Lemon’s prompts)
4. **Digital files:** upload  
   `TotalRecalls-windows-x64-v1.3.0.zip`  
   (same file as GitHub Release)
5. Description (short):

```text
Windows app to export AI chats from ChatGPT, Claude, Perplexity, Gemini (Takeout), and Grok into a private folder on your PC. One-time purchase. We don't host your session tokens.
```

6. After save, open **Share** / **Checkout link** and copy the full URL  
   (looks like `https://YOURSTORE.lemonsqueezy.com/checkout/buy/…`)

## Wire the website

1. Edit `site/public/js/config.js` (Astro build uses this path; the stale V1 copy `site/js/config.js` was deleted 2026-08-14):

```js
lemonCheckoutUrl: "https://YOURSTORE.lemonsqueezy.com/checkout/buy/YOUR-ID",
```

> ✅ Done 2026-08-14: real checkout URL wired on `RedesignV4` (`192968e`).

2. In Lemon product settings, set **Confirmation / redirect** URL to:

```text
https://totalrecalls.app/thanks.html
```

(Use your live domain; `*.run.app` is fine until DNS is done.)

3. Commit + push → Cloud Run rebuilds the static site.

4. Hard-refresh totalrecalls.app — Buy buttons should open Lemon; the operator warning banner hides automatically.

## Launch checklist (audited via API 2026-08-14)

| # | Item | State |
|---|------|-------|
| 1 | Payout method (bank) | ✅ done (user-confirmed) |
| 2 | Tax profile / W-8 | ✅ done (user-confirmed) |
| 3 | Publish product: switch from Test mode to **Live**, set status **Published** | ❌ product is `draft`, `test_mode: true` |
| 4 | Attach digital file `TotalRecalls-windows-x64-v1.3.0.zip` to the variant | ❌ 0 files attached |
| 5 | Store email (support@totalrecalls.app) in Store Settings | ❌ API shows `email: None` |
| 6 | Confirmation redirect → thanks page | ❌ not set |
| 7 | Rotate API key at launch (new live-mode key; update `.env`) | 🔜 at launch |
| 8 | Full test purchase before going live | ❌ |

### Webhook decision (open item)

A webhook already exists (`test_mode: true`, 20 events incl. `order_created`,
`order_refunded`) pointing at:

```text
https://totalrecalls.app/api/webhooks/lemonsqueezy
```

**Problem:** the V1 site is static HTML — nothing listens at that URL. With 0
orders today it's inert, but at launch it must be one of:

- **Option A — standalone webhook handler.** A small serverless handler (Cloud
  Run function or Node route) that receives `order_created` and emails the
  download link / stores the order. ~100 lines.
- **Option B — drop the webhook.** Lemon's own receipt email already delivers
  the attached zip; a webhook is only needed for custom post-purchase logic
  (license keys, dashboards). For v1 (paid download first), this is acceptable.
- **Option C — repoint it to a placeholder that 200s.** Keep the webhook slot
  but avoid error noise until a real handler exists.

**Recommendation:** Option B for v1 launch; revisit when license keys ship
(v1.1+). If B, delete the webhook in Settings → Webhooks before going live.

## Test checklist

- [ ] Test mode purchase completes
- [ ] Email delivers zip
- [ ] Redirect lands on `/thanks.html`
- [ ] Download button on thanks page works
- [ ] Live mode when ready
