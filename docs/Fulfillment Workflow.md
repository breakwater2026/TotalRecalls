Here is the complete end-to-end workflow for a sale from Paddle through Cloudflare to Courier, based on the actual deployed code and the Cloudflare dashboard data captured during the CDP session.



1. Paddle (Merchant of Record)

What Paddle does:
- Hosts the checkout page via Paddle.js (card input UI, tax calculation, fraud prevention)
- Charges the customer's card and settles funds to your Paddle account
- Handles invoicing: automatically generates invoice numbers and sends receipts to the customer
- Acts as the merchant of record for tax/VAT compliance

What Paddle does NOT do:
- Does NOT generate license keys
- Does NOT send fulfillment emails
- Does NOT know about your software's licensing system

The sale event: When a payment clears, Paddle fires a transaction.completed webhook to your configured endpoint. This is the only signal your fulfillment system receives from Paddle.



2. Cloudflare Worker (Fulfillment Handler)

The Worker is deployed at account 348a35e76cee14de8028300ab71de1d1 and routes on zone totalrecalls.app (f6d50a1793dd64423f5a3663971e2f), deployed on September 24, 2026. The Cloudflare dashboard captured three routes:

Route Pattern: /health*
Route ID: 39b3e71ffa294a0492c80e508feb6612
Purpose: Health checks (Cloudflare dashboard monitors this for uptime)
────────────────────────────────────────
Route Pattern: /api/licenses*
Route ID: e1aebc236f094e6e8f8639c593060e00
Purpose: License verification API (called by the TotalRecalls desktop app)
────────────────────────────────────────
Route Pattern: /webhook/paddle*
Route ID: 19af4e58846b4d14bdcdce9e05dc17ac
Purpose: Paddle webhook receiver (the main trigger)

How the Worker processes a webhook:

1. Signature verification (lines 131-164 of src/index.ts):

   Paddle sends the HMAC signature in the Paddle-Signature header in the format:

   ts=1727000000;hmac=a1b2c3d4e5f6...

   The Worker:
   - Extracts the ts (Unix timestamp) and hmac (hex-encoded SHA256 HMAC) from the header
   - Reconstructs the signed payload as {timestamp}.{raw_request_body}
   - Computes HMAC-SHA256 over this string using the PADDLE_WEBHOOK_SECRET
   - Compares the computed hash with the received hash

   typescript
   const signedPayload = ${timestamp}.${payload};
   const sig = await crypto.subtle.sign('HMAC', key, encoder.encode(signedPayload));


2. Event routing (line 62):

   typescript
   if (event.event_type === 'transaction.completed') {
       const customerEmail = event.data?.customer?.email_address;
       const productId = event.data?.product?.id || event.data?.items?.[0]?.product?.id;


   The Worker only processes transaction.completed events. The payload structure from Paddle's transaction.completed contains:
   - data.customer.email_address — the buyer's email
   - data.product.id or data.items[0].product.id — product identifier
   - data.name — product name (fallback: "TotalRecalls")
   - data.id — Paddle transaction ID (used as purchaseId for license registration)

3. License key generation (lines 22-24):

   typescript
   function generateLicenseKey(): string {
     return TR-${randomAlphaNumeric(8)}-${randomAlphaNumeric(4)}-${randomAlphaNumeric(4)};
   }

   Produces keys like TR-A1B2C3D4-E5F6-7890. Uses crypto.getRandomValues for cryptographic randomness.

4. In-memory storage (lines 8, 73-77):

   typescript
   const LICENSE_STORE = new Map<string, { email: string; product_id: string; created_at: string }>();

   Stores the license key -> customer mapping in a Map(). This is ephemeral (reset on each cold start). The code comments say "use KV for production" — in production you'd want persistent storage here.

5. Courier email dispatch (lines 166-192):

   typescript
   const response = await fetch('https://api.courier.com/send', {
       method: 'POST',
       headers: { 'Authorization: *** ${env.COURIER_API_KEY}', 'Content-Type': 'application/json' },
       body: JSON.stringify({
           message: {
               template: env.COURIER_TEMPLATE_ID,
               to: { email: email },
               data: { licenseKey, productName, timestamp: new Date().toISOString() }
           }
       })
   });

   The Worker calls Courier's /send API with:
   - The customer's email as the to address
   - Your pre-configured email template ID (COURIER_TEMPLATE_ID)
   - The license key injected as a template variable (data.licenseKey)

6. License registration with TotalRecalls app (lines 90-105):

   If the fulfillment succeeds, the Worker asynchronously POSTs to your app's license verification endpoint (LICENSE_ENDPOINT, which maps to totalrecalls.app/api/licenses*):
   typescript
   fetch(env.LICENSE_ENDPOINT, {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({
           licenseKey, email: customerEmail, productId,
           source: 'paddle-webhook', purchaseId: event.data?.id
       })
   });

   This runs fire-and-forget via ctx.wait() — the Worker doesn't wait for a response before returning to Paddle.



3. Courier (Email Delivery)

Courier receives the API call from the Worker and:

1. Looks up your email template (COURIER_TEMPLATE_ID)
2. Merges the template variables (licenseKey, productName, timestamp) into the email body
3. Routes the email via Courier's email provider integration (SMTP/SendGrid/etc.)
4. Delivers the license key email directly to the customer's inbox

Courier handles the actual email infrastructure — deliverability, SMTP providers, retries — you only interact with their simple REST API.



4. Invoicing Flow (Paddle Only)

Invoicing is entirely handled by Paddle. There is no involvement from the Cloudflare Worker or Courier in the invoicing process. Paddle automatically:

1. Generates an invoice number for each successful transaction
2. Associates it with the transaction.completed webhook event
3. Sends a receipt/email to the customer from Paddle's own email system

The Cloudflare dashboard data shows the billing account is active with:
- Account created: 2026-05-21
- R2 Paid plan subscription (r2_paid, ID fb757f9ba27a4722a738aad4f51a633f)
- No open billing issues (billing/history?status=OPEN returns empty)
- Payment method on file



Summary Flow Diagram


Customer Checkout
       |
       v
   Paddle (Merchant of Record)
   - Charges card
   - Issues invoice/receipt
       |
       | webhook (transaction.completed)
       v
  Cloudflare Worker (totalrecalls.app/webhook/paddle*)
   1. Verify Paddle-Signature (HMAC-SHA256)
   2. Extract customer email + product
   3. Generate TR-XXXXXXXX-XXXX-XXXX key
   4. Call Courier /send API with license key
   5. Async POST to /api/licenses (app registration)
       |
       | HTTP POST
       v
  Courier
   - Template merge (license key inserted)
   - Email delivery to customer
       |
       v
   Customer receives license key email


Key point: Paddle handles everything up to the webhook. The Cloudflare Worker handles fulfillment (license generation + email dispatch). Courier handles delivery. Invoicing is Paddle's responsibility and happens independently — the Worker never touches invoice numbers, billing cycles, or receipts.
