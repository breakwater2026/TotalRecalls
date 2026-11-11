# TotalRecalls — Fulfillment Workflow

**Complete end-to-end path from a Paddle sale to an activated desktop app and SSE module.**

Last updated **2026-11-10** against the live production deployment. Every claim here reflects the live Cloudflare Worker (`paddle-webhook`), D1 database schema (`tr-website-db`), the multi-tier product catalog (Downloader Pro, SSE Add-On, and Bundle), and official Microsoft Store distribution.

---

## 0. The Chain in One Line

```
Paddle checkout (Paddle.js)
  → Webhook (HMAC-SHA256)
  → Cloudflare Worker (`paddle-webhook`)
  → Classify Tier ('pro' | 'sse' | 'bundle')
  → Mint TR- / SSE- key(s) in D1 (`tr-website-db`)
  → Resend email (`licenses@totalrecalls.app`) to buyer
  → Seller sale notice to `NOTIFY_TO`
  → Buyer enters key into Desktop App or SSE companion
  → Verification API (`POST /api/licenses/verify`)
```

---

## 1. Commercial Catalog & Paddle Products

Paddle Billing is the **Merchant of Record**, handling card processing, global sales tax calculation and remittance, receipts, fraud prevention, and chargebacks.

### Three Commercial Tiers

| Tier | Product ID | Price ID | Launch Price | Regular Price | Keys Minted |
|---|---|---|---|---|---|
| **Downloader Pro** | `pro_01m37qgm5hgzv7tfrg519884ds` | `pri_01m37qpx77bst2w1gnf3zkf4zd` | **$24.00** | $48.00 | Single `TR-` key |
| **Smart Search Engine (SSE) Add-On** | `pro_01m6qftveaczq3mzx0wnhnzwdr` | `pri_01m6qftvhs2yt7c0yrgr0xy5tg` | **$29.00** | $58.00 | Single `SSE-` key |
| **Pro + SSE Bundle** | `pro_01m6qftvphzpzatfz1661d0px3` | `pri_01m6w18jd6qtnr0e40b5kf7m0b` | **$49.00** | $98.00 | Dual keys: `TR-` + `SSE-` |

- **Universal Discount ID:** `dsc_01m39879ga7pv9zg0gsvzqsmjw` (50% launch discount).
- **Notification Destination:** `ntfset_01m39f0thgb00rgdfpwdw9hs9k` → `https://totalrecalls.app/webhook/paddle`.
- **Subscribed Events:** `transaction.created`, `transaction.completed`, `transaction.updated`.
- **Paddle Fee Structure:** 5% + $0.50 per checkout transaction on the tax-inclusive total.

---

## 2. Cloudflare Worker Infrastructure

| Component | Identifier / Value | Notes |
|---|---|---|
| **Script Name** | `paddle-webhook` | Production Cloudflare Worker |
| **Account ID** | `348a35e76cee14de8028300ab71de1d1` | Breakwater Cloudflare Account |
| **Zone** | `totalrecalls.app` (`f6d50a1793dd64423f5a3663971e2f`) | Cloudflare edge |
| **Primary Code** | `paddle-fulfillment-worker/src/worker.js` | Modular JavaScript worker |
| **Database (D1)** | `tr-website-db` (`903321ec-7dcf-4d9b-ae66-edeb76954311`) | Authoritative relational state |

### Endpoints & Routing

| Path | Purpose | Auth / Access |
|---|---|---|
| `GET /health` | Worker liveness & binding check | Public (`200 {"status":"ok"}`) |
| `POST /webhook/paddle` | Inbound Paddle webhook receiver | HMAC-SHA256 signature verification |
| `POST /api/licenses/verify` | Desktop App & SSE key verification & activation | Machine User-Agent validation |
| `GET /api/licenses/order/:order_id` | Support lookup: find key by Paddle order ID | Requires `X-Admin-Key` header |
| `GET /api/licenses/:email` | Support lookup: find keys by customer email | Requires `X-Admin-Key` header |

### Required Worker Secrets
* `PADDLE_WEBHOOK_SECRET`: Paddle notification destination secret (`endpoint_secret_key`).
* `PADDLE_API_KEY`: Resolves customer email via `GET /customers/{id}` if omitted in transaction payload.
* `RESEND_API_KEY`: Authenticates with Resend API for transactional email delivery.
* `MAIL_FROM`: Sender address (default: `TotalRecalls <licenses@totalrecalls.app>`).
* `NOTIFY_TO`: Destination for seller notifications (default: `totalrecalls.app@gmail.com`).
* `ADMIN_KEY`: Constant-time comparison secret guarding support lookups.

---

## 3. Order Processing & Multi-Tier Key Minting

When a `transaction.completed` webhook arrives at `POST /webhook/paddle`:

1. **HMAC Verification:** Fails closed (HTTP 401) if signature header `Paddle-Signature: ts=...;h1=...` does not match HMAC-SHA256 over `<ts>.<rawBody>` using `PADDLE_WEBHOOK_SECRET`. Replays > 300 seconds are rejected.
2. **Audit Logging:** The raw payload is inserted into table `webhook_events`.
3. **Customer Resolution:** If the webhook omits `customer_email`, the worker calls `GET https://api.paddle.com/customers/{customer_id}` to retrieve the buyer's email.
4. **Order Tier Classification (`classifyOrderTier`):**
   * **`bundle`:** Product ID or Price ID matches `PADDLE_BUNDLE_IDS`, or name contains `"bundle"` / `"pro" + "sse"`.
   * **`sse`:** Product ID or Price ID matches `PADDLE_SSE_IDS`, or name contains `"smart search"` / `"sse"`.
   * **`pro`:** Default fall-through for Downloader Pro.
5. **Key Generation (`generateLicenseKey`):**
   * Character set: 32 unambiguous uppercase alphanumeric characters (`ABCDEFGHJKLMNPQRSTUVWXYZ23456789` — excludes `I`, `O`, `0`, `1`).
   * **Pro Keys:** Formatted as `TR-XXXXXXXX-XXXX-XXXX`.
   * **SSE Keys:** Formatted as `SSE-XXXXXXXX-XXXX-XXXX`.
6. **D1 Database Persistence:**
   * **Single Tier (Pro or SSE):** Inserts one row in `license_keys` tied to `order_id`.
   * **Bundle Tier:** Inserts two distinct rows:
     * `order_id` → `TR-XXXXXXXX-XXXX-XXXX` (Downloader Pro)
     * `order_id:sse` → `SSE-XXXXXXXX-XXXX-XXXX` (Smart Search Engine)
   * **Idempotency:** If `order_id` is already fulfilled, returns existing keys immediately without minting duplicates.
7. **Email Dispatch (Resend):**
   * Automatically formats custom transactional HTML & plain-text templates based on tier:
     * Bundle email displays both keys clearly labeled (1. Downloader Pro, 2. Smart Search Engine).
     * Single tier email displays its specific key and setup instructions.
   * Dispatched with `Idempotency-Key: totalrecalls-license-<key>`.
8. **Seller Notification:**
   * An instant summary is dispatched to `NOTIFY_TO` detailing buyer email, order amount, product, and issued keys.
9. **Delivery Tracking (`trackDelivery`):**
   * Worker polls Resend background status up to 4 times and updates `license_keys.email_status` (`delivered`, `opened`, `bounced`).

---

## 4. Activation & Verification Protocol

Both the desktop application and the Smart Search Engine module verify entitlements against:
`POST https://totalrecalls.app/api/licenses/verify`

### Request Payload

```json
{
  "license_key": "TR-XXXXXXXX-XXXX-XXXX",
  "instance_name": "TR-3D4F1E2A8C7B"
}
```

### Protocol Mechanics

1. **User-Agent Requirement:** Client must provide User-Agent starting with `TotalRecalls/` or `TotalRecalls-SSE/` to prevent Cloudflare edge blocking (WAF Rule 1010).
2. **Entitlement Check:** Key must exist in `license_keys` with status `pending`, `fulfilled`, or `email_failed`.
3. **Seat Limit (`MAX_INSTANCES = 3`):**
   * Each license permits activation on up to **3 individual personal machines**.
   * Re-activating an existing `instance_name` returns the existing `instance_id` (idempotent, does not consume extra seats).
   * If an unactivated machine attempts activation and 3 seats are already active, returns:  
     `{"valid": false, "error": "activation_limit_reached"}`.
4. **Deactivation:**
   * Client sends `{"action": "deactivate", "instance_id": "<uuid>"}`.
   * Frees the machine seat in `license_instances` (`active = 0`), allowing transfer to another computer.
5. **Audit Logging:** Every verification attempt is logged in `verify_attempts` recording timestamp, license key, machine instance name, User-Agent, and result.

---

## 5. Client Applications & Distribution

### A. TotalRecalls Downloader Pro
* **Distribution (Primary):** Official **Microsoft Store** (`TotalRecalls.TotalRecalls`, Store ID `9PP1KKD5X2D6`, MSIX package v1.0.1.0). Certified, zero SmartScreen warnings, one-click install.
* **Distribution (Plan B):** Standalone portable ZIP (`TotalRecalls-1.0.0-free-tier.zip`).
* **Activation:** Runs in Free Tier out of the box (3 providers, 5 chats each). User clicks "Pro" or "Activate" in the UI header and pastes their `TR-XXXXXXXX-XXXX-XXXX` key to unlock all 8 providers and unlimited exports.

### B. Smart Search Engine (SSE) Add-On
* **Distribution:** Standalone portable package (`TotalRecalls-Smart-Search-Engine-1.0.0.zip`) with `run-smart-search.bat` launcher.
* **Default Index Path:** Automatically mounts and indexes `%USERPROFILE%\TotalRecalls-download\Library\`.
* **Activation:** User clicks "Activate SSE Key" in the webview interface and enters their `SSE-XXXXXXXX-XXXX-XXXX` key. Activates offline semantic search, BGE-small vector embeddings, and SQLite RAG engine.

---

## 6. Database Schema (`tr-website-db`)

```sql
CREATE TABLE license_keys (
    id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    customer_email TEXT,
    customer_name TEXT,
    product_name TEXT,
    license_key TEXT UNIQUE,
    status TEXT DEFAULT 'pending',
    courier_request_id TEXT,
    email_status TEXT,
    raw_event TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE license_instances (
    id TEXT PRIMARY KEY,
    license_key TEXT NOT NULL,
    instance_name TEXT NOT NULL,
    active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (license_key) REFERENCES license_keys(license_key)
);

CREATE TABLE webhook_events (
    id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    paddle_event_id TEXT,
    raw_body TEXT,
    processed INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE verify_attempts (
    id TEXT PRIMARY KEY,
    license_key TEXT,
    instance_name TEXT,
    result TEXT,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 7. Operational Troubleshooting & CLI Commands

```bash
# Check recent webhook events and processing status
wrangler d1 execute tr-website-db --remote --command="SELECT event_type, processed, created_at FROM webhook_events ORDER BY created_at DESC LIMIT 5"

# Search issued keys by customer email
wrangler d1 execute tr-website-db --remote --command="SELECT order_id, product_name, license_key, status, email_status FROM license_keys WHERE customer_email = 'buyer@example.com'"

# Check machine activation seats for a key
wrangler d1 execute tr-website-db --remote --command="SELECT instance_name, active, updated_at FROM license_instances WHERE license_key = 'TR-Q6WXAGPE-3MHS-BYLE'"

# View recent verification attempts
wrangler d1 execute tr-website-db --remote --command="SELECT created_at, license_key, instance_name, result, user_agent FROM verify_attempts ORDER BY created_at DESC LIMIT 5"

# Clean test / probe activation seats
wrangler d1 execute tr-website-db --remote --command="DELETE FROM license_instances WHERE instance_name LIKE 'TR-PROBE%'"
```

---
*Authoritative Documentation • TotalRecalls Engineering Team*
