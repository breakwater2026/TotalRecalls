# Paddle + mail fulfillment — VERIFIED STATUS

Last verified live: **2026-09-26** — Paddle API, Cloudflare Workers/D1 API, Resend API, and a full
signed-webhook end-to-end test (key minted → email **delivered** → D1 recorded → key activates).
Every claim below was executed, not assumed. Supersedes all earlier versions of this file.

---

## 1. Paddle (live) — WORKING

| Item | ID | Value |
|---|---|---|
| Product | `pro_01m37qgm5hgzv7tfrg519884ds` | TotalRecalls |
| Price | `pri_01m37qpx77bst2w1gnf3zkf4zd` | one-time, 3 installations, **$48.00 USD**, active |
| Launch discount | `dsc_01m39879ga7pv9zg0gsvzqsmjw` | **50% off**, active, no start/end → **$24** |

### Notification destination `ntfset_01m39f0thgb00rgdfpwdw9hs9k` — REPOINTED 2026-09-26
- Destination: `https://totalrecalls.app/webhook/paddle` (was a dead `workers.dev` subdomain)
- `include_sensitive_fields: **true**` (so the payload carries the buyer's email)
- Updated in place via `PATCH /notification-settings/{id}` — not recreated, so the endpoint secret
  survived. Secret lives in the Worker's `PADDLE_WEBHOOK_SECRET` binding and in
  `$HERMES_HOME/.env` on the Mini-PC — **never in this repo** (redacted here 2026-09-26 after a
  pre-commit scan caught it in plain text).
- Subscribed: `transaction.created`, `transaction.completed`, `transaction.updated`

## 2. Cloudflare Worker `paddle-webhook` — LIVE, REWRITTEN

Source of truth: `paddle-fulfillment-worker/src/worker.js` (the repo's older `src/index.ts` is a
stale alternate design targeting `LICENSE_KV`).
Account `348a35e76cee14de8028300ab71de1d1`, zone `totalrecalls.app`.
Bindings preserved: **DB** (D1 `tr-website-db`, `903321ec-7dcf-4d9b-ae66-edeb76954311`),
**EMAILS_KV** (`14c867f2677c453b85b2c2d2e0cba711`).
Secrets: `PADDLE_WEBHOOK_SECRET`, `PADDLE_API_KEY`, `RESEND_API_KEY`, `MAIL_FROM`
(plus the retired `COURIER_*`, now unused).
Routes: `POST /webhook/paddle`, `POST /api/licenses/verify`, `GET /api/licenses/{email}`,
`GET /api/licenses/order/{id}`, `GET /health`.

### Defects found and fixed in the revision deployed before this one
1. **Key minting was outsourced to a service that does not exist** — the code POSTed orders to
   `COURIERS_API_URL` (default `couriers.gadget.app/api/licenses`, invented) and expected
   `{license_key}` back. No email API mints keys.
2. **The buyer email was never found** — it read `data.customer_email` / `data.customer.email`;
   a Paddle transaction carries `customer_id`. So `customer_email` was always `''` and the
   `&& customer_email` guard skipped fulfillment entirely.
3. **Every D1 write was a silent no-op** — `await db.prepare(...).bind(...)` builds a statement
   without running it. `.run()` is required. This is why the tables were empty while the worker
   cheerfully returned `200 fulfilled`.
4. **`/api/licenses/verify` did not exist** — the app's activation POST fell into the email-lookup
   branch and returned `{"licenses":[]}`.
5. **HMAC verification was inert** — the check was skipped when the secret was unset.

### Mail delivery: Resend, called directly (Courier REMOVED)
Courier was dropped on 2026-09-26. It needed a per-environment provider integration configured in
its dashboard, and no SMTP integration ever became visible to any environment we held a key for:
sends answered `UNROUTABLE` with `"None of provider(s) courier is configured for channel email"`
(and, under the other key, `"No provider(s) courier-email…"`). Its default routing scheme also sent
to **In-App**, so an email template with `routing: null` could never select the email channel.
The worker now posts straight to `https://api.resend.com/emails` with `{from, to, subject, html, text}`
— one credential, no environment axis, no routing schemes. `MAIL_FROM` is a **worker secret**, so
moving from the sandbox sender to the verified domain is a secret update, not a redeploy.

### Verification evidence (all run 2026-09-26)
| Check | Result |
|---|---|
| Unsigned / bad-signature POST | `401 {"error":"Invalid signature"}` |
| Validly signed `transaction.completed` | `200 {"status":"fulfilled","license_key":"TR-TKAEDYFC-RDUZ-EZFG","mail_status":200}` |
| D1 write | `webhook_events` row + `license_keys` row |
| **Delivery** | `status=fulfilled`, `email_status=**delivered**` |
| Activation contract | activate → `valid:true`+`instance_id`; re-activate → **same slot**; re-validate → valid; deactivate → valid then **invalid**; unknown key → invalid |
| 3-install limit | 4th machine → `activation_limit_reached`; seat freed on deactivate |

### D1 schema
- `license_keys`: id, order_id, customer_email, customer_name, product_name, license_key, status,
  raw_event, created_at, updated_at, **courier_request_id** *(historical name — now holds the mail
  provider's message id: Resend `id`)*, **email_status** (`accepted` / `delivered` / `bounced` …)
- `webhook_events`: id, event_type, event_id, raw_body, processed
- `license_instances`: id, license_key, instance_name, created_at, active, deactivated_at

**Entitlement follows the KEY, not the mail** (`ENTITLED_STATUSES = pending|fulfilled|email_failed`):
a buyer whose email bounces still paid, so a delivery failure must never lock them out.

### How to deploy (the two traps)
`PUT /accounts/{acct}/workers/scripts/paddle-webhook` with a hand-built multipart body:
the file part needs **`filename="index.js"` as well as `name="index.js"`**, and content type
**`application/javascript+module`**. Name alone → `10021 No such module`; plain
`application/javascript` → `10021 Unexpected token 'export'`. `curl -F` mis-parses it — build the
body byte-exactly (CRLF) and send with `--data-binary` + an explicit boundary. **Re-send all
bindings in the `metadata` part** or the worker loses D1/KV. Cloudflare edge-caches responses, so
cache-bust query strings when reading back; account-scoped `cfat_` tokens return
`1000 Invalid API Token` from `/user/tokens/verify` yet work fine on account endpoints.

## 3. Resend — WORKING (sandbox sender)

- Account `totalrecalls.app@gmail.com`; key `re_…` in `$HERMES_HOME/.env` as `RESEND_API_KEY`
  and as the worker secret of the same name.
- **SMTP credentials verified by real authentication**: `smtp.resend.com`, username literal
  `resend`, password = the `re_…` key — AUTH OK on 465 (implicit TLS) *and* 587 (STARTTLS), and a
  message was sent and reported **delivered**.
- **Domain `totalrecalls.app` registered with Resend** (`ceeb0707-9049-4b6a-9a25-9846a767532f`,
  region us-east-1) but **DNS records are not yet added**, so it is `not_started`.
- Until verification, Resend delivers **only** to `totalrecalls.app@gmail.com`, and only from
  `onboarding@resend.dev` — which is what the `MAIL_FROM` secret currently holds.

### Records to add in Cloudflare for `totalrecalls.app` (names are relative to the zone)
| Type | Name | Value | Priority | Proxy |
|---|---|---|---|---|
| TXT | `resend._domainkey` | `p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCkcSTsbrti/06sTfTHphotoNYRm9Fg2qwJKhuEEUhq4bXXLhbYTGZGkdehyPZQRqTolFZW8mcLkXkZoDF2wXwH4YNq4MMzqCIz9lal2Oqrocb5+vJeT2Hd/z6Ddme9NyCjhX8NOtxmyjpNT4Hv/o6Q3CBE6iBjNAP4FFeQaYkuVQIDAQAB` | — | DNS only |
| MX | `send` | `feedback-smtp.us-east-1.amazonses.com` | 10 | — |
| TXT | `send` | `v=spf1 include:amazonses.com ~all` | — | DNS only |
| CNAME | `rsend` | `send.forge.rmta.net` | — | **DNS only (grey cloud)** |

Then: Resend → Domains → **Restart verification** → once verified, update the worker secret
`MAIL_FROM` to `TotalRecalls <licenses@totalrecalls.app>`. **No redeploy needed.**

## 4. Application side — ENDPOINT FIXED, REBUILT, VERIFIED

`totalrecalls/licensing.py` → `LICENSE_VERIFY_ENDPOINT` = `https://totalrecalls.app/api/licenses/verify`
(was the dead `workers.dev/verify`). Contract matches the worker: POST
`{license_key, instance_name|instance_id, action}` → `{valid, instance_id}`.
Rebuilt 2026-09-26 in the clean venv — `dist/TotalRecalls.exe` sha `350961d4…`, PYZ-verified
(`tools/_verify_paddle_build.py`: Paddle endpoint present, no Lemon Squeezy leftovers,
`edition=free`, buy URL = `totalrecalls.app/buy`). `dist/stage/TotalRecalls-free-verified.exe`
refreshed to the same build. **`docs/TotalRecalls.exe` is still a stale Sep-13 copy — don't run it.**
Rebuild from a tree whose `edition.py` reads `free`, and always re-run the verifier: EXE size and
mtime prove nothing about which code shipped.

## 5. Purchase path — WAS BROKEN IN FOUR PLACES, NOW WIRED TO PADDLE

**Paddle is the only distributor** (FastSpring never approved; Lemon Squeezy rejected). Paddle
Billing has **no "checkout link" entity at all** — `GET /checkout-links` returns `404 invalid_url`,
which is why every `pay.paddle.io/checkout/hsc_…` URL on the site and in the app was dead. A
checkout is opened **client-side by Paddle.js** from a price (+ optional discount), or from a
server-created transaction's `checkout.url`.

| Path | Was | Now |
|---|---|---|
| ZIP `README.txt` | `https://totalrecalls.lemonsqueezy.com` | `https://totalrecalls.app/buy` |
| Site `/buy` button | `totalrecalls.order processor.com/checkout/buy/03e11a51-…` (placeholder host) | Paddle.js overlay (price + discount) |
| Site `/pricing` buttons (×2) | same placeholder host | Paddle.js overlay |
| `site/public/js/config.js` | `paddleCheckoutUrl` = dead `hsc_…` stub | `paddleClientToken` + `paddlePriceId` + `paddleDiscountId`, loads Paddle.js v2 and opens checkout |
| App Buy button (`bridge.py::openBuyPage`) | dead `hsc_…` URL | `https://totalrecalls.app/buy` |

Also fixed in the same pass:
- **The launch discount was not redeemable**: `dsc_01m39879ga7pv9zg0gsvzqsmjw` had
  `enabled_for_checkout: false`, so the checkout would have charged **$48** while the site
  advertised **$24**. Set to `true` (verified by read-back). It **expires 2026-10-30T23:59Z** —
  after that the price is $48 and the site copy must change.
- `normalPriceLabel` `$49` → **$48**.
- Every "order processor" placeholder across the site (buy, pricing, privacy, terms, thanks,
  how-it-works, landing components) now names **Paddle**.
- The privacy/legal pages claimed the app sends the licence key to *"the store's public licence
  API"* — it calls **our own worker**. Corrected, along with a "deactivate from your billing-area
  Licenses tab" instruction for a portal and an in-app control that both don't exist (now: email
  support to free a slot).

**The app's Buy button opens the site, so the 404 gate must be lifted for purchase to work**, and
Paddle must have approved `totalrecalls.app` as a checkout domain.

---

## Remaining to launch

1. **Resend DNS records → domain verified → update `MAIL_FROM`** (mail currently reaches only
   `totalrecalls.app@gmail.com`).
2. **Lift the 404 gate** so `/buy` and `/download` resolve, and confirm **Paddle domain approval**
   for `totalrecalls.app` — checkout cannot open on an unapproved domain.
3. **Rebuild + repackage already done** (EXE `350961d4…`, ZIP `d6ca7b01…`, page SHA matches) —
   re-run `tools/_verify_paddle_build.py` after any future build.
4. **Test the real purchase end to end**: Paddle checkout ($24 with the discount applied) →
   webhook → key emailed → activate in the app. This is the last unexercised path; a simulation
   event or a 100%-off test purchase also confirms whether the live payload carries
   `customer.email` or only `customer_id` (the worker's Paddle-API fallback handles the latter and
   is implemented but untested).
5. Roll the credentials that passed through chat (Paddle API key, Courier key).
