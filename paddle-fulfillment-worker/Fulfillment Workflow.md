# TotalRecalls — Fulfillment Workflow

**Complete end-to-end path from a Paddle sale to an activated desktop app.**

Last rewritten **2026-09-26** against the deployed system, after a real live
purchase (txn `txn_01m3fh0prrrbtqz0t43xh8zdh4`, USD 1.14 incl. GST) ran the whole
chain. Every claim here was executed and observed, not inferred. It supersedes the
earlier version of this file, which described a **Courier**-based design and an
in-memory `Map` store that were both removed.

> Status/evidence companion: `PADDLE_COURIER_FULFILLMENT_STATUS.md` (repo root).

---

## 0. The chain in one line

```
Paddle checkout  →  webhook (HMAC)  →  Cloudflare Worker  →  mint TR- key in D1
                 →  Resend email (licenses@totalrecalls.app)  →  buyer activates app
                                                 ↘  seller gets a sale notice
```

## 1. Paddle — Merchant of Record

Paddle is the **only** distributor (FastSpring never approved; Lemon Squeezy
rejected the app). It is the merchant of record, so it owns tax and the buyer
relationship.

| Item | ID / value |
|---|---|
| Product | `pro_01m37qgm5hgzv7tfrg519884ds` ("TotalRecalls") |
| Price | `pri_01m37qpx77bst2w1gnf3zkf4zd` — **4800** minor units = $48.00 USD |
| Launch discount | `dsc_01m39879ga7pv9zg0gsvzqsmjw` — 50%, `enabled_for_checkout: true`, **expires 2026-10-30** |
| Notification destination | `ntfset_01m39f0thgb00rgdfpwdw9hs9k` → `https://totalrecalls.app/webhook/paddle`, `include_sensitive_fields: true` |
| Subscribed events | `transaction.created`, `completed`, `updated` |
| Fee | **5% + $0.50 per checkout transaction**, applied to the tax-inclusive total |
| Effective fee at $24 / $48 | $1.70 (7.08%) / $2.90 (6.04%) |

**What Paddle does:** hosts the checkout (Paddle.js), charges the card, calculates
and **remits sales tax** in every jurisdiction, issues the invoice/receipt, handles
fraud and chargebacks, provides localized checkout and billing support.

**What Paddle does NOT do:** generate license keys, send fulfillment email, or know
anything about the app's licensing. That is what the Worker exists for.

### Two dashboard settings that gate selling entirely

1. **Default payment link** (`vendors.paddle.com/checkout-settings`) = `https://totalrecalls.app/buy`.
   Without it, *nothing* works: `POST /transactions` returns
   `transaction_default_checkout_url_not_set` and the overlay cannot open. It must be
   a page that **includes Paddle.js**, so not the bare homepage.
2. **Domain verification** for `totalrecalls.app`, same screen.

### Gotchas learned the hard way

- **Paddle enforces a minimum charge of 70 minor units (USD 0.70).** A $0.99 price
  with a 50% discount resolves to 49 → the transaction is refused outright
  (`transaction_balance_less_than_charge_limit`). Retail below ~$1.40 with the
  discount *enabled* is impossible.
- **Discount rounding goes down.** 50% of 99 minor units = 49.5 → Paddle charged 49.
- Products priced **under $10** fall outside Paddle's standard rate and require a
  custom-pricing conversation — don't build a promo in that band without asking.
- Paddle redelivers webhooks. Fulfillment must be idempotent (it is: see §4).

## 2. Cloudflare Worker — the fulfillment handler

| | |
|---|---|
| Script | `paddle-webhook` |
| Account | `348a35e76cee14de8028300ab71de1d1` |
| Zone | `totalrecalls.app` = `f6d50a1793dd64423f5a3663971e2f` |
| Source | `paddle-fulfillment-worker/src/worker.js` (deployed; `src/index.ts` is the retired original) |
| D1 | `tr-website-db` = `903321ec-7dcf-4d9b-ae66-edeb76954311` |
| KV | `EMAILS_KV` = `14c867f2677c453b85b2c2d2e0cba711` (legacy, unused) |

### Routes

| Pattern | Purpose | Verified |
|---|---|---|
| `/health` | Liveness + which bindings are present (never returns secret values) | `200 {\"status\":\"ok\",…}` |
| `/api/licenses/*` | License verification (the app) + admin-only support lookups | `200` (app) / `401` (unauth lookups) |
| `/webhook/paddle` | Paddle webhook receiver | `200` signed / `401` unsigned |

Each path is confirmed live by behaviour. The route **IDs** live in the Cloudflare
dashboard (the API's `/workers/routes` needs a scope this token doesn't carry), so
treat any ID written in older revisions of this file as unverified.

### Secrets

| Name | Purpose |
|---|---|
| `PADDLE_WEBHOOK_SECRET` | HMAC verification of inbound webhooks |
| `PADDLE_API_KEY` | Fetching the customer when a payload carries only `customer_id` |
| `RESEND_API_KEY` | Sending mail |
| `MAIL_FROM` | e.g. `TotalRecalls <licenses@totalrecalls.app>` |
| `NOTIFY_TO` | Where sale notices go (default `totalrecalls.app@gmail.com`) |
| `ADMIN_KEY` | Guards the support lookups (§6) |

`COURIER_API_KEY` / `COURIER_TEMPLATE_ID` are **retired leftovers** and can be deleted.

### Deploying — the two traps

```bash
# A Worker upload MUST be a byte-exact multipart body:
#   field name "index.js" WITH filename="index.js"
#   Content-Type: application/javascript+module
# curl -F mangles this; build the body in Python and --data-binary @file
PUT /accounts/<acct>/workers/scripts/paddle-webhook
```

1. Wrong content-type → `400 code 10021 Uncaught SyntaxError: Unexpected token 'export'`.
2. Secrets are set separately (`PUT .../scripts/paddle-webhook/secrets`) and **survive**
   a script upload — changing `MAIL_FROM` needs no redeploy.

## 3. Webhook handling, step by step

1. **Read the raw body first.** The signature is computed over the exact bytes.
2. **Verify HMAC — mandatory, fails closed.** If `PADDLE_WEBHOOK_SECRET` is unset the
   worker returns 503 rather than accepting anything.
   Header format is Paddle's real one:

   ```
   Paddle-Signature: ts=1727000000;h1=<hex HMAC-SHA256>
   signed payload  = "<ts>.<raw body>"
   ```
   *(The old doc said `hmac=`. Paddle sends `h1=`; parsing `hmac=` alone would 401
   every real webhook.)* Bad or absent signature → **401**.
3. **Store the event** in `webhook_events` before doing anything else, then mark
   `processed = 1`. This is the audit trail that proves a webhook arrived.
4. **Extract the order** (`extractOrderData`): `order_id`, `customer_id`,
   `customer_email`, product name, price ids, `total` + `currency_code`.
   The email may be absent — Paddle can send only `customer_id` — so the worker
   falls back to `GET /customers/{id}` on the Paddle API. (The old `data.customer_email`
   read always yielded `''`, silently skipping fulfillment.)
5. **Fulfill** (`fulfillOrder`, idempotent per `order_id`):
   - mint a key with `crypto.getRandomValues` → `TR-XXXXXXXX-XXXX-XXXX`,
   - insert (or reuse) the row in `license_keys`,
   - email the buyer via Resend,
   - return `{status: 'fulfilled' | 'already_fulfilled', license_key, mail_status}`.
6. **Seller notice** (only on `transaction.completed`, §5).
7. **Answer Paddle immediately** and track delivery in the background
   (`ctx.waitUntil`) — Resend accepting a send is not proof of delivery.

## 4. Data model (D1 `tr-website-db`)

| Table | Holds |
|---|---|
| `license_keys` | order id, buyer email/name, product, **the key**, status, `email_status`, timestamps |
| `webhook_events` | every delivered event: type, Paddle event id, raw body, `processed` |
| `license_instances` | one row per activated machine: key, `instance_name`, `active`, timestamps |
| `verify_attempts` | **every** verification call: key, instance name, result, User-Agent, time |

`verify_attempts` is the diagnostic that separates the two failure classes: **no row
means the request never reached us** (edge block, or the client never called), while a
row with `valid:false` means our own entitlement logic said no.

**Entitlement follows the KEY, not the mail.** A failed email still yields an
activatable license (`email_status` records the failure separately).

## 5. Email — Resend, called directly

Courier was removed entirely: it needed a per-environment provider integration that
never became visible to any key we held, and its default routing scheme sent to
*In-App*, so a template with `routing: null` could never select the email channel.
The worker now calls `POST https://api.resend.com/emails` itself — one credential,
no routing axis.

- **From:** `TotalRecalls <licenses@totalrecalls.app>` (a **secret**, so switchable
  without a redeploy).
- **Domain:** `totalrecalls.app`, Resend status **verified** (DKIM + both SPF records).
- **Idempotency:** `Idempotency-Key: totalrecalls-license-<key>`, so Paddle's
  redeliveries cannot double-send.
- **Delivery is tracked, not assumed:** after sending, the worker polls the Resend
  message and writes the outcome to `license_keys.email_status`.

### Seller notification (added 2026-09-26)

Fulfillment used to be silent from the owner's side — a sale happened and the only
evidence lived in D1, invisible without API access. Now, on `transaction.completed`
only (all five event types run through fulfillment, so per-event notices would send
five per sale), the worker emails the seller:

```
to       NOTIFY_TO (default totalrecalls.app@gmail.com)
subject  Sale: TotalRecalls — 24.00 USD — <buyer email>
body     order id · buyer · amount · product · license key · buyer-mail status · time
```
Sent via `ctx.waitUntil` with `Idempotency-Key: totalrecalls-sale-<order_id>`.
Verified: replaying the same event returned `already_fulfilled` and produced **0**
extra sends.

### DNS records (Cloudflare, names relative to the zone)

| Type | Name | Value | Notes |
|---|---|---|---|
| TXT | `resend._domainkey` | `p=MIGfMA0…` (218 chars) | DKIM, DNS only |
| MX | `send` | `feedback-smtp.us-east-1.amazonses.com` (prio 10) | |
| TXT | `send` | `v=spf1 include:amazonses.com ~all` | |
| CNAME | `rsend` | `send.forge.rmta.net` | **DNS only (grey cloud)** |
| TXT | `_dmarc` | `v=DMARC1; p=none;` | optional per Resend |

Root SPF is **merged**, because SPF permits only one record per name and the root
already carried Cloudflare Email Routing's:

```
v=spf1 include:_spf.mx.cloudflare.net include:amazonses.com ~all
```

**Resend's badge can lie.** The domain showed `pending` / "Missing SPF records" for
~3h while the records were already byte-exact and sending already worked. Verify the
DNS yourself with `tools/_probe_dns.py` (raw TXT strings, no quote-stripping — stripping
quotes is exactly how a quoting bug hides) before chasing their UI.

**Deliverability:** `delivered` means the receiving server accepted the message, not
that it reached the inbox. A new sending domain is unfiltered-but-untrusted, so the
first messages commonly land in spam; ask buyers to check and mark as not-spam.

## 6. The activation contract (app ↔ worker)

The **app calls the worker** — the reverse of the retired design, where the worker
posted to the app.

```
POST https://totalrecalls.app/api/licenses/verify
     { "license_key": "TR-…", "instance_name": "TR-<hex>" }        # activate
     { "license_key": "TR-…", "instance_id": "<uuid>" }            # revalidate
     { "license_key": "TR-…", "instance_id": "<uuid>", "action": "deactivate" }

→    { "valid": true,  "instance_id": "<uuid>" }
     { "valid": false, "instance_id": "" }        # bad key / deactivated
     { "valid": false, "error": "activation_limit_reached" }
```

- **3 activations per purchase** (`MAX_INSTANCES`), matching the invoice copy.
- **Re-activation on the same machine is idempotent** — it returns the existing
  `instance_id` instead of burning a second slot.
- Deactivating frees the seat; a new machine can then activate.

Two client-side rules that each broke activation on their own (both now guarded at
build time):

1. **The app must send its own `User-Agent`.** Cloudflare answers urllib's default
   `Python-urllib/3.x` with **403 error 1010** ("the owner of this website has banned
   your browser"), so *every* verification was rejected at the edge before the Worker
   ran. `licensing._verify_post` sends `TotalRecalls/1.0 (+https://totalrecalls.app)`.
2. **`main.py` exposes `JsApi`, not `Bridge`.** pywebview only exposes that facade's
   public methods; a method present on `Bridge` but missing from `js_api.py` is
   `undefined` in the webview, the handler throws `not a function` after setting
   "Activating…", and the UI hangs forever with no log line and no request. Run
   `tools/_check_ui_bridge_contract.py` before packaging.

### Admin-only support lookups

These return the key **and** the buyer's email, so they require an `X-Admin-Key`
header (`ADMIN_KEY` secret, constant-time compare). They shipped open to the world
and were closed on 2026-09-26:

```bash
curl -H "X-Admin-Key: $TR_ADMIN_KEY" https://totalrecalls.app/api/licenses/order/<txn_id>
curl -H "X-Admin-Key: $TR_ADMIN_KEY" https://totalrecalls.app/api/licenses/<buyer email>
```

## 7. Website side

- **Checkout is Paddle.js**, not a link. Paddle Billing has **no checkout-link
  entity** (`GET /checkout-links` → 404 `invalid_url`), so the old
  `pay.paddle.io/checkout/hsc_…` URLs were never real and dead-ended every buyer.
  `site/public/js/config.js` holds the client token, `paddlePriceId` and
  `paddleDiscountId`; the `/buy` and `/pricing` buttons call
  `Paddle.Checkout.open({items, discountId, settings:{displayMode:'overlay', successUrl:'/thanks/'}})`.
- The **client-side token is public by design** (it ships in the page). The **secret
  API key** (`pdl_live_apikey_…`) must never appear in the site, the repo or memory.
- **Hosting:** the site is a Cloudflare **Pages** project
  (`totalrecalls`), git-connected to `main`, built by
  `cd site && npm ci --legacy-peer-deps && npm run build` → `site/dist`. A push
  deploys. **Do not add an `[assets]` block to the root `wrangler.toml`** — that is a
  Workers-only key and the Pages validator rejects the whole file
  (`Configuration file for Pages projects does not support "assets"`), failing the
  build ~2s in and silently leaving production on the previous deployment.
- **Pages caps files at 25 MiB.** A 58 MB hero video in `site/public/` can never
  deploy; large media lives in R2 (`video.totalrecalls.app`) instead.
- **Payment links:** Paddle builds `checkout.url` as
  `<default payment link>?_ptxn=<txn_id>`; `config.js` initialises Paddle.js eagerly
  when `_ptxn` is present so payment-method updates and invoice links resume the
  right transaction.
- The **download ZIP** (`site/public/downloads/TotalRecalls-1.0.0-free-tier.zip`) is
  the shipping artifact; its SHA-256 is quoted on `/download`. Any rebuild changes the
  hash, so update that page in the same commit.

## 8. Operations cheatsheet

```bash
# Was a webhook received, and what did we answer? (no row = it never arrived)
POST /accounts/<acct>/d1/database/<db>/query
  {"sql":"SELECT event_type, processed, created_at FROM webhook_events ORDER BY created_at DESC LIMIT 10"}

# Who activated, on how many seats?
  {"sql":"SELECT instance_name, active FROM license_instances"}
  {"sql":"SELECT license_key, customer_email, status, email_status FROM license_keys ORDER BY created_at DESC"}

# Every activation the app attempted, with its User-Agent
  {"sql":"SELECT created_at, license_key, instance_name, result, user_agent FROM verify_attempts ORDER BY created_at DESC LIMIT 10"}

# Paddle's own delivery log for webhooks
GET https://api.paddle.com/notifications

# Build guards (both must pass before packaging)
python tools/_check_ui_bridge_contract.py     # UI calls ⊆ JsApi facade
python tools/_verify_paddle_build.py          # Paddle endpoint + Buy URL + UA + edition=free in the PYZ
python tools/_probe_dns.py                    # byte-exact DKIM/SPF/MX
```

**Seat hygiene:** probe activations consume real slots. Clear them before handing an
account to a buyer:
`DELETE FROM license_instances WHERE instance_name LIKE 'TR-PROBE%'`.

## 9. Flow diagram

```
Buyer → /buy  (Paddle.js overlay: price + 50% discount → $24)
   │
   ▼  card charged, tax calculated, invoice issued  (all Paddle)
Paddle ──webhook (HMAC sha256, ts=…;h1=…)──▶ totalrecalls.app/webhook/paddle
   │                                              │  verify signature (401 if bad)
   │                                              │  store event in webhook_events
   │                                              ▼
   │                                        fulfillOrder (idempotent per order id)
   │                                              ├─ mint TR-XXXXXXXX-XXXX-XXXX
   │                                              ├─ INSERT license_keys (D1)
   │                                              ├─ Resend → buyer's inbox
   │                                              │    (idempotency key = license key)
   │                                              └─ Resend → seller notice
   │                                                   (only on transaction.completed)
   │                                              ▼
   │                                        trackDelivery → email_status in D1
   ▼
Buyer runs TotalRecalls.exe → pastes key → Activate
   │
   ▼  POST /api/licenses/verify {license_key, instance_name}
Worker ── key entitled? seat free? ──▶ {valid:true, instance_id} + license_instances row
   ▼
Pro unlocked: 8 providers, unlimited downloads (3 machines per purchase)
```

## 10. Still open

- **Launch discount expires 2026-10-30** — after that buyers pay $48 and the
  "50% OFF / discounted launch price" copy on the site needs updating.
- **Sub-$10 pricing** would need Paddle custom pricing (§1 gotcha).
- **Monitoring layer** (X230 15-minute cron) for fulfillment health — not built.
- `src/index.ts`, `COURIER_*` secrets, and the KV namespace are dead remnants kept
  only for history.
