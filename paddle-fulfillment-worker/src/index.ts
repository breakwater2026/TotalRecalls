export interface Env {
  COURIER_API_KEY: string;
  PADDLE_WEBHOOK_SECRET: string;
  COURIER_TEMPLATE_ID: string;
  LICENSE_ENDPOINT: string;
  LICENSE_KV: KVNamespace;
}

const ALPHANUM = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';

function randomAlphaNumeric(length: number): string {
  let result = '';
  const bytes = new Uint8Array(length);
  crypto.getRandomValues(bytes);
  for (let i = 0; i < length; i++) {
    result += ALPHANUM[bytes[i] % ALPHANUM.length];
  }
  return result;
}

function generateLicenseKey(): string {
  return `TR-${randomAlphaNumeric(8)}-${randomAlphaNumeric(4)}-${randomAlphaNumeric(4)}`;
}

async function timingSafeEqual(a: string, b: string): Promise<boolean> {
  // Constant-time string comparison to prevent timing attacks
  const encoder = new TextEncoder();
  const aBytes = encoder.encode(a);
  const bBytes = encoder.encode(b);
  if (aBytes.length !== bBytes.length) {
    // Compare anyway and discard result to maintain constant time
    const dummy = new Uint8Array(aBytes.length);
    crypto.getRandomValues(dummy);
    crypto.timingSafeEqual(dummy, dummy);
    return false;
  }
  return crypto.timingSafeEqual(aBytes, bBytes);
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    // Health check
    if (url.pathname === '/health') {
      return new Response(JSON.stringify({ status: 'ok', timestamp: new Date().toISOString() }), {
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // License verification API — checks if a license key is valid (for TotalRecalls desktop app)
    if (url.pathname === '/api/licenses/verify' && request.method === 'GET') {
      const licenseKey = url.searchParams.get('key');
      if (!licenseKey) {
        return new Response(JSON.stringify({ valid: false, error: 'Missing license key' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' },
        });
      }

      const stored = await env.LICENSE_KV.get(licenseKey, { type: 'json' });
      if (!stored) {
        return new Response(JSON.stringify({ valid: false }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        });
      }

      return new Response(JSON.stringify({
        valid: true,
        licenseKey,
        email: stored.email,
        productId: stored.product_id,
        createdAt: stored.created_at,
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // License lookup by email (for support/admin)
    if (url.pathname === '/api/licenses/lookup' && request.method === 'GET') {
      const email = url.searchParams.get('email');
      if (!email) {
        return new Response(JSON.stringify({ error: 'Missing email parameter' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' },
        });
      }

      // Note: KV doesn't support reverse lookup natively.
      // In production, you'd also store an email -> licenseKey index.
      return new Response(JSON.stringify({ error: 'Lookup by email requires secondary index' }), {
        status: 501,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Webhook endpoint — Paddle posts transaction.completed here
    if (url.pathname === '/webhook/paddle' && request.method === 'POST') {
      const signature = request.headers.get('Paddle-Signature');
      const payload = await request.text();

      if (!signature) {
        return new Response('Missing Paddle-Signature header', { status: 401 });
      }

      // Verify HMAC signature
      const isValid = await verifyPaddleSignature(payload, signature, env.PADDLE_WEBHOOK_SECRET);
      if (!isValid) {
        return new Response('Invalid signature', { status: 401 });
      }

      let event: any;
      try {
        event = JSON.parse(payload);
      } catch (e) {
        return new Response('Invalid JSON payload', { status: 400 });
      }

      console.log('Received Paddle event:', event.event_type);

      // Handle transaction.completed (payment succeeded)
      if (event.event_type === 'transaction.completed') {
        const customerEmail = event.data?.customer?.email_address;
        const productId = event.data?.product?.id || event.data?.items?.[0]?.product?.id;
        const productName = event.data?.name || 'TotalRecalls';

        if (customerEmail) {
          try {
            // Generate license key
            const licenseKey = generateLicenseKey();

            // Store license in KV namespace (persistent across cold starts)
            const licenseRecord = {
              email: customerEmail,
              product_id: productId,
              created_at: new Date().toISOString(),
              purchase_id: event.data?.id,
              source: 'paddle-webhook',
            };
            await env.LICENSE_KV.put(licenseKey, JSON.stringify(licenseRecord));

            // Send license email via Courier
            const emailSent = await sendLicenseViaCourier(
              customerEmail,
              licenseKey,
              productName,
              env,
            );

            if (emailSent) {
              console.log(`License sent to ${customerEmail}: ${licenseKey}`);

              // Optionally notify TotalRecalls license verification endpoint
              if (env.LICENSE_ENDPOINT) {
                ctx.wait(
                  fetch(env.LICENSE_ENDPOINT, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                      licenseKey,
                      email: customerEmail,
                      productId,
                      source: 'paddle-webhook',
                      purchaseId: event.data?.id,
                    }),
                  }).catch((e) => console.error('License endpoint error:', e)),
                );
              }

              return new Response(
                JSON.stringify({ status: 'success', licenseKey, email: customerEmail }),
                { status: 200, headers: { 'Content-Type': 'application/json' } },
              );
            }

            // Courier failed — roll back the KV entry and return error
            await env.LICENSE_KV.delete(licenseKey);
            return new Response('Courier email failed', { status: 502 });
          } catch (error: any) {
            console.error('Error processing webhook:', error);
            return new Response(
              JSON.stringify({ error: error.message }),
              { status: 500, headers: { 'Content-Type': 'application/json' } },
            );
          }
        }
      }

      return new Response(JSON.stringify({ status: 'processed' }), { status: 200 });
    }

    return new Response('Not found', { status: 404 });
  },
};

async function verifyPaddleSignature(payload: string, signature: string, secret: string): Promise<boolean> {
  // Paddle sends: ts=<timestamp>;hmac=<hex_hmac_sha256_of(timestamp.payload)>
  // Extract the hmac value from the signature
  const match = signature.match(/hmac=([a-f0-9]+)/);
  if (!match) {
    return false;
  }
  const expectedHmac = match[1];

  // Paddle computes HMAC over "{timestamp}.{payload}"
  const tsMatch = signature.match(/ts=(\d+)/);
  if (!tsMatch) {
    return false;
  }
  const timestamp = tsMatch[1];
  const signedPayload = `${timestamp}.${payload}`;

  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw',
    encoder.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign'],
  );
  const sig = await crypto.subtle.sign('HMAC', key, encoder.encode(signedPayload));
  const computedHmac = Array.from(new Uint8Array(sig))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');

  // Use timing-safe comparison
  return timingSafeEqual(computedHmac, expectedHmac);
}

async function sendLicenseViaCourier(
  email: string,
  licenseKey: string,
  productName: string,
  env: Env,
): Promise<boolean> {
  const response = await fetch('https://api.courier.com/send', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${env.COURIER_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: {
        template: env.COURIER_TEMPLATE_ID,
        to: { email: email },
        data: {
          licenseKey,
          productName,
          timestamp: new Date().toISOString(),
        },
      },
    }),
  });

  return response.ok;
}
