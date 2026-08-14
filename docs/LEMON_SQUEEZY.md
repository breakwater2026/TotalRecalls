# Lemon Squeezy setup — TotalRecalls ($24 one-time)

## Locked decisions

| Item | Value |
|------|--------|
| Provider | **Lemon Squeezy** |
| Price | **$24 USD** one-time |
| Product | TotalRecalls for Windows |
| License keys in app | **Not required for v1** (paid download first) |
| Site config | `site/js/config.js` → `lemonCheckoutUrl` |

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

1. Edit `site/js/config.js`:

```js
lemonCheckoutUrl: "https://YOURSTORE.lemonsqueezy.com/checkout/buy/YOUR-ID",
```

2. In Lemon product settings, set **Confirmation / redirect** URL to:

```text
https://totalrecalls.app/thanks.html
```

(Use your live domain; `*.run.app` is fine until DNS is done.)

3. Commit + push `main` → Cloud Run rebuilds the static site.

4. Hard-refresh totalrecalls.app — Buy buttons should open Lemon; the operator warning banner hides automatically.

## Optional later

- Lemon **license keys** generation (still no app UI required until you add it)
- Discount codes for launch ($19)
- Overlay checkout script instead of hosted link

## Test checklist

- [ ] Test mode purchase completes
- [ ] Email delivers zip
- [ ] Redirect lands on `/thanks.html`
- [ ] Download button on thanks page works
- [ ] Live mode when ready
