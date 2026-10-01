// /api/subscribe — footer email sign-up (Cloudflare Pages Function).
// Spec: Marketing/Jasper/Website Rewrite/Footer Email Signup HTML Placement.md
//
// Payload: { email: string, website?: string }   (website = honeypot)
// Success: { ok: true }
// Failure: { ok: false, error: "..." }
//
// Storage: KV namespace TOTALRECALLS_SIGNUPS (create in the Pages dashboard;
// each subscriber is a key = sha1(email), value = JSON record). Duplicates are
// idempotent: re-subscribing refreshes the record instead of erroring.
export async function onRequest(context) {
  const { request, env, next } = context;

  const CORS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };

  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS });
  }
  if (request.method !== "POST") {
    return json({ ok: false, error: "Method not allowed" }, 405, CORS);
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: "Invalid request" }, 400, CORS);
  }

  const email = String(body.email || "").trim().toLowerCase();
  const valid = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) && email.length <= 254;
  if (!valid) {
    return json({ ok: false, error: "Please enter a valid email address." }, 400, CORS);
  }

  // Honeypot filled → bot. Accept silently so bots learn nothing.
  if (body.website) {
    return json({ ok: true }, 200, CORS);
  }

  const key = crypto.subtle
    ? await sha1hex(email)
    : btoa(email).replace(/[^a-zA-Z0-9]/g, "");

  try {
    if (env && env.SIGNUPS) {
      const existing = await env.SIGNUPS.get(key, "json");
      const record = {
        email,
        first_subscribed_at: existing?.first_subscribed_at || new Date().toISOString(),
        last_subscribed_at: new Date().toISOString(),
        source: request.headers.get("Referer") || null,
      };
      await env.SIGNUPS.put(key, JSON.stringify(record));
    }
    // No KV namespace configured: still accept (degrade gracefully).
  } catch (e) {
    console.error("signup storage error:", e);
  }

  return json({ ok: true }, 200, CORS);
}

function json(obj, status, headers) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...headers },
  });
}

async function sha1hex(input) {
  const buf = await crypto.subtle.digest("SHA-1", new TextEncoder().encode(input));
  return Array.from(new Uint8Array(buf))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}
