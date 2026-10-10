// gen-sitemap.mjs — regenerates dist/sitemap.xml from the built pages.
// Run after `astro build` (wired in package.json "build").
// Excludes 404 pages. Writes lastmod = build date.
import { readdirSync, statSync, writeFileSync } from "node:fs";
import { join, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";

// fileURLToPath (NOT URL.pathname) — pathname keeps percent-encoding, so a checkout
// in a folder with a space (e.g. "TotalRecalls-Source Code") made readdirSync throw
// ENOENT on "...Source%20Code/site/dist". Works either way on Cloudflare's builder.
const dist = fileURLToPath(new URL("../dist/", import.meta.url));
const site = "https://totalrecalls.app";

function walk(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) out.push(...walk(full));
    else if (name.endsWith(".html")) out.push(full);
  }
  return out;
}

// 404 has nothing to index. /thanks/ is a post-purchase conversion page that is
// meta-noindex'd (pages/thanks/index.astro) — listing it in the sitemap advertises a
// URL we deliberately keep out of the index and spends crawl budget on it.
const files = walk(dist).filter(
  (f) => !/404\.html$/.test(f) && !/[/\\]thanks[/\\]index\.html$/.test(f),
);
const urls = files
  .map((f) => {
    let rel = relative(dist, f).split(sep).join("/");
    rel = rel === "index.html" ? "" : rel.replace(/\/index\.html$/, "/").replace(/\.html$/, "/");
    return `${site}/${rel}`;
  })
  .sort();

// No <lastmod>: the previous code stamped the BUILD date on every URL, so every deploy told
// Google that all 53 pages had changed — a claim that is false, and which Google's own guidance
// says it will ignore when lastmod is unreliable. An absent lastmod is honest; a wrong one is noise.
const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((u) => `  <url>\n    <loc>${u}</loc>\n  </url>`).join("\n")}
</urlset>
`;

writeFileSync(join(dist, "sitemap.xml"), xml);
console.log(`sitemap: ${urls.length} URLs written to dist/sitemap.xml`);
