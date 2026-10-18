// Permanently gone: an LS-era orphan demo asset removed from the site on
// 2026-10-18. A stale edge copy kept answering 200 for this exact URL even
// though every deployment 404s it, so this Function makes the origin's answer
// explicit and uncacheable: 410 + no-store, for this path only.
// (The other files under /demo/ — result.png, poster_chatgpt.png — are live.)
export async function onRequest() {
  return new Response("This resource has been removed.\n", {
    status: 410,
    headers: {
      "content-type": "text/plain; charset=utf-8",
      "cache-control": "no-store, max-age=0",
      "x-robots-tag": "noindex, nofollow",
    },
  });
}
