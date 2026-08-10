# Lemon Squeezy setup — TotalRecalls ($24 one-time)

## Locked decisions

| Item | Value |
|------|--------|
| Provider | **Lemon Squeezy** |
| Price | **$24 USD** one-time |
| Product | TotalRecalls for Windows |
| License keys in app | **Not required for v1** (paid download first) |
| Site config | `site/js/config.js` → `lemonCheckoutUrl` |

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
