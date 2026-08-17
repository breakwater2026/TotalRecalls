// gen-sitemap.mjs — regenerates dist/sitemap.xml from the built pages.
// Run after `astro build` (wired in package.json "build").
// Excludes 404 pages. Writes lastmod = build date.
import { readdirSync, statSync, writeFileSync } from "node:fs";
import { join, relative, sep } from "node:path";

const dist = new URL("../dist/", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");
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

const files = walk(dist).filter((f) => !/404\.html$/.test(f));
const urls = files
  .map((f) => {
    let rel = relative(dist, f).split(sep).join("/");
    rel = rel === "index.html" ? "" : rel.replace(/\/index\.html$/, "/").replace(/\.html$/, "/");
    return `${site}/${rel}`;
  })
  .sort();

const today = new Date().toISOString().slice(0, 10);
const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((u) => `  <url>\n    <loc>${u}</loc>\n    <lastmod>${today}</lastmod>\n  </url>`).join("\n")}
</urlset>
`;

writeFileSync(join(dist, "sitemap.xml"), xml);
console.log(`sitemap: ${urls.length} URLs written to dist/sitemap.xml`);
