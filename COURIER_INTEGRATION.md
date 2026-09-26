# Courier Integration

## Overview
Paddle does not handle license key fulfillment. When a customer purchases
TotalRecalls via Paddle, the webhook fires to a Cloudflare Worker, which
extracts the customer email and generates a license key, then sends it
to the customer via Courier.

## Data Flow
```
Customer pays via Paddle Checkout
  ↓  (transaction.completed webhook)
Cloudflare Worker receives webhook
  ↓
Worker validates Paddle signature (PADDLE_WEBHOOK_SECRET)
Worker extracts: customer email, product, price
  ↓
Worker generates license key (stored in-memory KV)
  ↓
Worker calls Couriers API with template + email + license key
  ↓
Couriers delivers email with license key + download link
```

## Worker Secrets Required
| Secret              | Source                        |
|---------------------|-------------------------------|
| PADDLE_WEBHOOK_SECRET | Paddle notification setting   |
| COURIER_API_KEY     | Couriers → Settings → API Keys |
| COURIER_TEMPLATE_ID  | Couriers → Templates          |

## Couriers Template
The template should accept these variables:
- `{{license_key}}` — the generated license key
- `{{product_name}}` — "TotalRecalls"
- `{{download_url}}` — link to the installer

## License Key Generation
The worker generates keys as:
`TR-<random-6-chars>-<timestamp-epoch>`
Example: `TR-a4B9xY2-1727156420`

Keys are stored in worker-level memory (in-memory map) and survive
until the Worker instance is recycled. For production, move to
Cloudflare KV or Durable Objects for persistence.