/**
 * TotalRecalls fulfillment worker (live script name: `paddle-webhook`).
 *
 * Chain: Paddle `transaction.completed` → verify HMAC → mint a TR-… key →
 * email it via Resend → record it in D1 → the desktop app validates it at
 * `POST /api/licenses/verify`.
 *
 * Mail delivery goes straight to Resend's API. An earlier revision relayed
 * through Courier (api.courier.com), which needed a per-environment provider
 * integration to be configured in Courier's dashboard before the email
 * channel could route at all; that integration never took, and Courier
 * answered every send with `UNROUTABLE / "None of provider(s) courier is
 * configured for channel email"`. Resend is a single credential with no
 * per-environment plumbing, and was verified delivering end to end.
 *
 * Required secrets:
 *   PADDLE_WEBHOOK_SECRET  notification destination's endpoint_secret_key
 *   RESEND_API_KEY         Resend key (re_…), "sending access"
 *   MAIL_FROM              e.g. "TotalRecalls <licenses@totalrecalls.app>".
 *                          Until the Resend domain is verified, the only
 *                          sender that delivers is onboarding@resend.dev and
 *                          the only recipient is the Resend signup address.
 *   PADDLE_API_KEY         Paddle API key, to resolve the buyer email when the
 *                          webhook payload omits it
 * Bindings: DB (D1 tr-website-db), EMAILS_KV (KV, retained)
 */

const RESEND_SEND_URL = 'https://api.resend.com/emails';
const PADDLE_API = 'https://api.paddle.com';
const MAX_INSTANCES = 3;
const DEFAULT_FROM = 'TotalRecalls <onboarding@resend.dev>';
const DOWNLOAD_URL = 'https://totalrecalls.app/download';

// Resend `last_event` values that decide whether the buyer actually got mail.
const MAIL_FAILURES = ['bounced', 'failed', 'complained', 'rejected', 'blocked', 'suppressed'];
const MAIL_SUCCESS = ['delivered', 'sent', 'opened', 'clicked'];
const MAIL_TERMINAL = [...MAIL_FAILURES, ...MAIL_SUCCESS];

// Entitlement follows the KEY, not the mail: a buyer whose email bounced still
// paid, and locking them out over our delivery problem is worse than a
// support-side resend. Only a key that was never minted fails verification.
const ENTITLED_STATUSES = ['pending', 'fulfilled', 'email_failed'];

const ORDER_EVENT_TYPES = [
  'transaction.completed',
  'transaction.paid',
  'transaction.ready',
  'order.created',
  'order.paid',
  'order.ready',
  'payment_succeeded',
];

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Paddle-Signature, X-Paddle-Signature',
};

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS_HEADERS },
  });
}

function escapeHtml(value) {
  return String(value == null ? '' : value)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

/* ------------------------------------------------------------------ *
 * Paddle webhook signature (header: `Paddle-Signature: ts=…;h1=…`)
 * ------------------------------------------------------------------ */
async function verifyPaddleSignature(rawBody, signatureHeader, secret) {
  if (!signatureHeader || !secret) return false;
  let ts = null;
  let h1 = null;
  for (const part of signatureHeader.split(';')) {
    const [key, val] = part.split('=');
    if (!key || val === undefined) continue;
    if (key.trim() === 'ts') ts = val.trim();
    if (key.trim() === 'h1') h1 = val.trim();
  }
  if (!ts || !h1) return false;
  // Reject replays outside a 5-minute window.
  if (Math.abs(Math.floor(Date.now() / 1000) - parseInt(ts, 10)) > 300) return false;
  const key = await crypto.subtle.importKey(
    'raw', new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign'],
  );
  const sig = await crypto.subtle.sign(
    'HMAC', key, new TextEncoder().encode(`${ts}:${rawBody}`),
  );
  const computed = Array.from(new Uint8Array(sig))
    .map((b) => b.toString(16).padStart(2, '0')).join('');
  // Constant-time comparison.
  if (computed.length !== h1.length) return false;
  let diff = 0;
  for (let i = 0; i < computed.length; i++) {
    diff |= computed.charCodeAt(i) ^ h1.charCodeAt(i);
  }
  return diff === 0;
}

/* ------------------------------------------------------------------ *
 * License keys: TR-XXXXXXXX-XXXX-XXXX (matches the app's regex).
 * Ambiguous glyphs (I, O, 0, 1) excluded so keys survive being retyped.
 * ------------------------------------------------------------------ */
const KEY_ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';

function randomBlock(len) {
  const bytes = new Uint8Array(len);
  crypto.getRandomValues(bytes);
  let out = '';
  for (let i = 0; i < len; i++) out += KEY_ALPHABET[bytes[i] % KEY_ALPHABET.length];
  return out;
}

function generateLicenseKey() {
  return `TR-${randomBlock(8)}-${randomBlock(4)}-${randomBlock(4)}`;
}

/* ------------------------------------------------------------------ *
 * Order extraction
 * ------------------------------------------------------------------ */
function extractOrderData(payload) {
  const data = payload.data || {};
  const items = Array.isArray(data.items) ? data.items : [];
  const first = items[0] || {};
  return {
    event_type: payload.event_type || payload.alert_name || '',
    order_id: String(data.id || data.order_id || data.transaction_id || ''),
    customer_id: String(data.customer_id || (data.customer && data.customer.id) || ''),
    customer_email: String(
      (data.customer && data.customer.email) || data.customer_email || '',
    ),
    customer_name: String(
      (data.customer && data.customer.name) || data.customer_name || '',
    ),
    product_id: String(first.product_id || (first.product && first.product.id) || ''),
    product_name: String(
      (first.product && first.product.name) || (first.price && first.price.name)
      || data.product_name || 'TotalRecalls',
    ),
    price_ids: items.map((i) => String(i.price_id || '')).filter(Boolean),
  };
}

/**
 * A Paddle transaction payload carries `customer_id`, not the buyer's email
 * (the email lives on the customer object). Fall back to the Paddle API so
 * fulfillment never silently no-ops on an empty address.
 */
async function resolveCustomerEmail(order, env) {
  if (order.customer_email) return { email: order.customer_email, source: 'payload' };
  if (!order.customer_id || !env.PADDLE_API_KEY) {
    return { email: '', source: 'unavailable' };
  }
  try {
    const resp = await fetch(`${PADDLE_API}/customers/${order.customer_id}`, {
      headers: { Authorization: `Bearer ${env.PADDLE_API_KEY}` },
    });
    if (!resp.ok) return { email: '', source: `paddle-api-${resp.status}` };
    const body = await resp.json();
    const customer = body.data || {};
    return {
      email: String(customer.email || ''),
      source: 'paddle-api',
      name: String(customer.name || order.customer_name || ''),
    };
  } catch (err) {
    return { email: '', source: `paddle-api-error:${err.message}` };
  }
}

/* ------------------------------------------------------------------ *
 * Resend delivery
 * ------------------------------------------------------------------ */
function licenseEmailHtml({ licenseKey, productName, timestamp }) {
  const key = escapeHtml(licenseKey);
  return `<!doctype html><html><body style="margin:0;padding:0;background:#fafafa">
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;max-width:560px;margin:0 auto;padding:28px 24px;color:#18181b">
  <h1 style="font-size:20px;line-height:1.3;margin:0 0 16px">Your TotalRecalls license key</h1>
  <p style="font-size:15px;line-height:1.55;margin:0 0 18px">Thanks for buying TotalRecalls. Here is your license key:</p>
  <p style="font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:20px;font-weight:600;letter-spacing:0.5px;background:#f4f4f5;border:1px solid #e4e4e7;border-radius:8px;padding:16px;margin:0 0 20px;text-align:center">${key}</p>
  <p style="font-size:15px;line-height:1.55;margin:0 0 22px">To activate: open TotalRecalls, click <strong>Activate</strong>, and paste the key exactly as shown.</p>
  <p style="margin:0 0 24px"><a href="${DOWNLOAD_URL}" style="background:#18181b;color:#ffffff;text-decoration:none;padding:12px 22px;border-radius:8px;display:inline-block;font-weight:600;font-size:15px">Download TotalRecalls</a></p>
  <hr style="border:none;border-top:1px solid #e4e4e7;margin:24px 0">
  <p style="font-size:13px;line-height:1.6;color:#71717a;margin:0">
    Product: ${escapeHtml(productName)}<br>Purchased: ${escapeHtml(timestamp)}
  </p>
  <p style="font-size:12px;line-height:1.6;color:#a1a1aa;margin:16px 0 0">
    Keep this key — it unlocks all 8 providers and unlimited downloads on up to 3 devices.
  </p>
</div></body></html>`;
}

function licenseEmailText({ licenseKey, productName, timestamp }) {
  return [
    'Thanks for buying TotalRecalls.',
    '',
    `License key: ${licenseKey}`,
    '',
    'To activate: open TotalRecalls, click Activate, and paste the key exactly as shown.',
    `Download: ${DOWNLOAD_URL}`,
    '',
    `Product: ${productName}`,
    `Purchased: ${timestamp}`,
    '',
    'Keep this key — it unlocks all 8 providers and unlimited downloads on up to 3 devices.',
  ].join('\n');
}

async function sendLicenseEmail({ email, licenseKey, productName }, env) {
  if (!env.RESEND_API_KEY) {
    return { ok: false, status: 0, body: 'RESEND_API_KEY not set', emailId: '' };
  }
  const from = env.MAIL_FROM || DEFAULT_FROM;
  const timestamp = new Date().toISOString();
  const resp = await fetch(RESEND_SEND_URL, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
      // One send per key: Paddle redelivers webhooks, mail must not duplicate.
      'Idempotency-Key': `totalrecalls-license-${licenseKey}`,
    },
    body: JSON.stringify({
      from,
      to: [email],
      subject: 'Your TotalRecalls license key',
      html: licenseEmailHtml({ licenseKey, productName, timestamp }),
      text: licenseEmailText({ licenseKey, productName, timestamp }),
    }),
  });
  const raw = await resp.text();
  let emailId = '';
  try {
    emailId = (JSON.parse(raw) || {}).id || '';
  } catch { /* non-JSON error body */ }
  return { ok: resp.ok, status: resp.status, body: raw.slice(0, 400), emailId };
}

/**
 * Resend accepts the send, but acceptance is not delivery — the outcome
 * arrives as `last_event`. Poll briefly in the background and record it, so a
 * broken sender shows up in D1 instead of looking like success.
 */
async function trackDelivery(emailId, env, licenseUuid) {
  if (!emailId) return;
  let last = '';
  for (let i = 0; i < 4; i++) {
    await new Promise((resolve) => setTimeout(resolve, 2000));
    try {
      const resp = await fetch(`https://api.resend.com/emails/${emailId}`, {
        headers: { Authorization: `Bearer ${env.RESEND_API_KEY}` },
      });
      if (!resp.ok) continue;
      const body = await resp.json();
      last = String(body.last_event || '');
      // 'delivery_delayed' is not final; keep waiting on it.
      if (last && last !== 'delivery_delayed' && MAIL_TERMINAL.includes(last)) break;
    } catch { /* keep polling */ }
  }
  if (!last) return;
  const failed = MAIL_FAILURES.includes(last);
  try {
    await env.DB
      .prepare('UPDATE license_keys SET email_status = ?, status = ?, updated_at = datetime(?) WHERE id = ?')
      .bind(last, failed ? 'email_failed' : 'fulfilled', new Date().toISOString(), licenseUuid)
      .run();
  } catch (err) {
    console.error('Could not record delivery status:', err.message);
  }
}

/* ------------------------------------------------------------------ *
 * Fulfillment
 * ------------------------------------------------------------------ */
async function fulfillOrder(order, env, rawBody) {
  const { email, source, name } = await resolveCustomerEmail(order, env);
  if (!email) {
    return { status: 'no_customer_email', email_source: source, license_key: '' };
  }
  const customerName = name || order.customer_name || '';

  const existing = await env.DB
    .prepare('SELECT id, license_key, status FROM license_keys WHERE order_id = ?')
    .bind(order.order_id).first();

  if (existing && existing.license_key) {
    return {
      status: 'already_fulfilled',
      license_key: existing.license_key,
      email_source: source,
    };
  }

  const licenseUuid = existing ? existing.id : crypto.randomUUID();
  const licenseKey = generateLicenseKey();

  if (existing) {
    await env.DB
      .prepare('UPDATE license_keys SET license_key = ?, customer_email = ?, customer_name = ?, status = ?, updated_at = datetime(?) WHERE id = ?')
      .bind(licenseKey, email, customerName, 'pending', new Date().toISOString(), licenseUuid)
      .run();
  } else {
    await env.DB
      .prepare('INSERT INTO license_keys (id, order_id, customer_email, customer_name, product_name, license_key, status, raw_event) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
      .bind(licenseUuid, order.order_id, email, customerName, order.product_name, licenseKey, 'pending', rawBody)
      .run();
  }

  const send = await sendLicenseEmail(
    { email, licenseKey, productName: order.product_name }, env,
  );

  // The key is stored either way: a mail failure stays retryable instead of
  // losing the buyer's key.
  const finalStatus = send.ok ? 'fulfilled' : 'email_failed';
  await env.DB
    .prepare('UPDATE license_keys SET status = ?, courier_request_id = ?, email_status = ?, updated_at = datetime(?) WHERE id = ?')
    .bind(finalStatus, send.emailId || null, send.ok ? 'accepted' : 'send_failed',
          new Date().toISOString(), licenseUuid)
    .run();

  return {
    status: finalStatus,
    license_key: licenseKey,
    license_id: licenseUuid,
    email_source: source,
    mail_status: send.status,
    mail_id: send.emailId,
    mail_error: send.ok ? undefined : send.body,
  };
}

/* ------------------------------------------------------------------ *
 * License verification (app contract: {license_key, instance_name|
 * instance_id, action} → {valid, instance_id})
 * ------------------------------------------------------------------ */
/**
 * Record every verification attempt. Without this, a client that never reaches
 * us is indistinguishable from one whose key we rejected — and that ambiguity
 * cost a debugging session (the app hung on activation with nothing in its own
 * log, and no way to tell whether the request had arrived).
 */
async function logAttempt(env, fields) {
  try {
    await env.DB
      .prepare('INSERT INTO verify_attempts (id, license_key, instance_name, instance_id, action, result, user_agent, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
      .bind(crypto.randomUUID(), fields.key || '', fields.instanceName || '',
            fields.instanceId || '', fields.action || '', JSON.stringify(fields.result),
            fields.userAgent || '', new Date().toISOString())
      .run();
  } catch (err) {
    console.error('verify attempt log failed:', err.message);
  }
}

async function handleVerify(request, env) {
  const userAgent = request.headers.get('User-Agent') || '';
  let body;
  try {
    body = await request.json();
  } catch {
    const verdict = { valid: false, instance_id: '', error: 'invalid_json' };
    await logAttempt(env, { result: verdict, userAgent });
    return json(verdict, 400);
  }
  const key = String(body.license_key || '').trim().toUpperCase();
  const instanceName = String(body.instance_name || '').trim();
  const instanceId = String(body.instance_id || '').trim();
  const action = String(body.action || '').trim();

  const verdict = await decideVerify(env, { key, instanceName, instanceId, action });
  await logAttempt(env, { key, instanceName, instanceId, action, result: verdict, userAgent });
  return json(verdict);
}

async function decideVerify(env, { key, instanceName, instanceId, action }) {
  if (!key) return { valid: false, instance_id: '' };

  const row = await env.DB
    .prepare('SELECT id, license_key, status FROM license_keys WHERE license_key = ?')
    .bind(key).first();
  if (!row || !row.license_key || !ENTITLED_STATUSES.includes(row.status)) {
    return { valid: false, instance_id: '' };
  }

  if (action === 'deactivate') {
    if (instanceId) {
      await env.DB
        .prepare('UPDATE license_instances SET active = 0, deactivated_at = ? WHERE id = ? AND license_key = ?')
        .bind(new Date().toISOString(), instanceId, key)
        .run();
    }
    return { valid: true, instance_id: '' };
  }

  // Re-validation of an already-registered machine.
  if (instanceId) {
    const inst = await env.DB
      .prepare('SELECT id, active FROM license_instances WHERE id = ? AND license_key = ?')
      .bind(instanceId, key).first();
    if (inst && inst.active) return { valid: true, instance_id: inst.id };
    return { valid: false, instance_id: '' };
  }

  // Activation: a machine that already holds a slot keeps it (idempotent), so
  // re-entering the key on the same device never consumes another slot.
  if (instanceName) {
    const same = await env.DB
      .prepare('SELECT id FROM license_instances WHERE license_key = ? AND instance_name = ? AND active = 1')
      .bind(key, instanceName).first();
    if (same) return { valid: true, instance_id: same.id };
  }

  const count = await env.DB
    .prepare('SELECT COUNT(*) AS n FROM license_instances WHERE license_key = ? AND active = 1')
    .bind(key).first();
  const used = (count && count.n) || 0;

  if (used >= MAX_INSTANCES) {
    return { valid: false, instance_id: '', error: 'activation_limit_reached' };
  }

  const newId = crypto.randomUUID();
  await env.DB
    .prepare('INSERT INTO license_instances (id, license_key, instance_name, created_at, active) VALUES (?, ?, ?, ?, 1)')
    .bind(newId, key, instanceName, new Date().toISOString())
    .run();
  return { valid: true, instance_id: newId };
}

/* ------------------------------------------------------------------ *
 * Router
 * ------------------------------------------------------------------ */
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    if (url.pathname === '/health') {
      return json({
        status: 'ok',
        time: new Date().toISOString(),
        mail: {
          provider: 'resend',
          resend_api_key: Boolean(env.RESEND_API_KEY),
          from: env.MAIL_FROM || DEFAULT_FROM,
        },
        secrets: {
          paddle_webhook_secret: Boolean(env.PADDLE_WEBHOOK_SECRET),
          paddle_api_key: Boolean(env.PADDLE_API_KEY),
        },
      });
    }

    /* License verification — the desktop app's activation/re-check path. */
    if (url.pathname === '/api/licenses/verify' && request.method === 'POST') {
      return handleVerify(request, env);
    }

    /* Paddle webhook */
    if (url.pathname === '/webhook/paddle' && request.method === 'POST') {
      const rawBody = await request.text();
      const signature = request.headers.get('Paddle-Signature')
        || request.headers.get('X-Paddle-Signature');

      // Verification is mandatory: never fulfill an unauthenticated request.
      if (!env.PADDLE_WEBHOOK_SECRET) {
        return json({ error: 'PADDLE_WEBHOOK_SECRET not configured' }, 503);
      }
      if (!(await verifyPaddleSignature(rawBody, signature, env.PADDLE_WEBHOOK_SECRET))) {
        return json({ error: 'Invalid signature' }, 401);
      }

      let payload;
      try {
        payload = JSON.parse(rawBody);
      } catch {
        return json({ error: 'Invalid JSON' }, 400);
      }

      const eventType = payload.event_type || payload.alert_name || 'unknown';
      const eventId = payload.event_id || crypto.randomUUID();
      const eventUuid = crypto.randomUUID();
      try {
        await env.DB
          .prepare('INSERT INTO webhook_events (id, event_type, event_id, raw_body, processed) VALUES (?, ?, ?, ?, 0)')
          .bind(eventUuid, eventType, eventId, rawBody)
          .run();
      } catch (err) {
        console.error('Failed to store webhook event:', err.message);
      }

      if (ORDER_EVENT_TYPES.includes(eventType)) {
        const order = extractOrderData(payload);
        if (order.order_id) {
          try {
            const result = await fulfillOrder(order, env, rawBody);
            await env.DB
              .prepare('UPDATE webhook_events SET processed = 1 WHERE id = ?')
              .bind(eventUuid)
              .run();
            // Answer Paddle immediately; confirm real delivery in the
            // background so a failed send can't masquerade as success.
            if (result.mail_id && ctx) {
              ctx.waitUntil(trackDelivery(result.mail_id, env, result.license_id));
            }
            return json({
              status: result.status,
              order_id: order.order_id,
              license_key: result.license_key || undefined,
              email_source: result.email_source,
              mail_status: result.mail_status,
              mail_error: result.mail_error,
            });
          } catch (err) {
            console.error('Fulfillment failed:', err.message);
            return json({ status: 'error', order_id: order.order_id, error: err.message });
          }
        }
      }

      await env.DB
        .prepare('UPDATE webhook_events SET processed = 1 WHERE id = ?')
        .bind(eventUuid)
        .run();
      return json({ status: 'acknowledged', event_type: eventType });
    }

    /* Lookup by order id */
    if (url.pathname.startsWith('/api/licenses/order/') && request.method === 'GET') {
      const orderId = decodeURIComponent(url.pathname.split('/api/licenses/order/')[1]);
      const row = await env.DB
        .prepare('SELECT id, order_id, customer_email, customer_name, product_name, license_key, status, email_status, created_at, updated_at FROM license_keys WHERE order_id = ?')
        .bind(orderId).first();
      return json({ license: row || null });
    }

    /* Lookup by email */
    if (url.pathname.startsWith('/api/licenses/') && request.method === 'GET') {
      const email = decodeURIComponent(url.pathname.split('/api/licenses/')[1]);
      const rows = await env.DB
        .prepare('SELECT id, order_id, customer_email, customer_name, product_name, license_key, status, email_status, created_at, updated_at FROM license_keys WHERE customer_email = ? ORDER BY created_at DESC')
        .bind(email).all();
      return json({ licenses: rows.results || [] });
    }

    return json({ error: 'Not found' }, 404);
  },
};
