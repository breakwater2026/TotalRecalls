// gen-sitemap.mjs — regenerates dist/sitemap.xml from the built pages.
// Run after `astro build` (wired in package.json "build").
// Excludes 404 pages. Writes a real per-URL <lastmod>.
import { existsSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { dirname, join, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";

// fileURLToPath (NOT URL.pathname) — pathname keeps percent-encoding, so a checkout
// in a folder with a space (e.g. "TotalRecalls-Source Code") made readdirSync throw
// ENOENT on "...Source%20Code/site/dist". Works either way on Cloudflare's builder.
const dist = fileURLToPath(new URL("../dist/", import.meta.url));
const repoRoot = fileURLToPath(new URL("../../", import.meta.url));
const site = "https://totalrecalls.app";

// ---------------------------------------------------------------------------
// <lastmod> = the newest commit that actually touched the page's own source.
//
// An earlier version stamped the BUILD date on every URL, so each deploy claimed
// all pages had changed — false, and Google says it discards lastmod when it is
// unreliable. A later revision carried no lastmod at all. This is the honest
// middle: each URL gets the date of the last real change to the file that renders
// it (plus the content files it imports), taken from git history rather than from
// the build clock. A page whose source has not changed keeps its old date across
// deploys, and one git cannot resolve omits the element instead of inventing one.
// ---------------------------------------------------------------------------

function gitDates() {
  const dates = new Map();
  try {
    const out = execFileSync(
      "git", ["log", "--format=C %cs", "--name-only", "-n", "2000"],
      { cwd: repoRoot, encoding: "utf8", maxBuffer: 64 * 1024 * 1024 },
    );
    let stamp = null;
    for (const line of out.split("\n")) {
      if (line.startsWith("C ")) {
        stamp = line.slice(2).trim();
        continue;
      }
      const p = line.trim();
      if (stamp && p && !dates.has(p)) dates.set(p, stamp);
    }
  } catch {
    // No git (or a shallow export without history): every URL omits <lastmod>.
  }
  return dates;
}

const DATES = gitDates();

function resolveFile(base) {
  const cands = [
    base, base + ".astro", base + ".jsx", base + ".js", base + ".mjs",
    join(base, "index.astro"), join(base, "index.jsx"),
  ];
  return cands.find((c) => existsSync(c)) || null;
}

// dist/about/index.html -> site/src/pages/about/index.astro (or about.astro).
// A segment with no literal file is then matched against any [param] route in that
// directory, so dist/see-it-work/claude/index.html resolves to
// pages/see-it-work/[provider].astro rather than going undated.
function pageRepoPath(distFile) {
  let rel = relative(dist, distFile).split(sep).join("/");
  rel = rel === "index.html" ? "" : rel.replace(/\/index\.html$/, "/").replace(/\.html$/, "/");
  const base = rel === "" ? "index" : rel.replace(/\/$/, "");
  const segs = base.split("/");
  const cands = [`site/src/pages/${base}.astro`, `site/src/pages/${base}/index.astro`];
  for (let i = segs.length - 1; i >= 0; i--) {
    const dirAbs = join(repoRoot, "site", "src", "pages", ...segs.slice(0, i));
    if (!existsSync(dirAbs)) continue;
    for (const entry of readdirSync(dirAbs)) {
      if (!/^\[.+\]\.astro$/.test(entry)) continue;
      const joined = [...segs.slice(0, i), entry.replace(/\.astro$/, ""), ...segs.slice(i + 1)].join("/");
      cands.push(`site/src/pages/${joined}.astro`, `site/src/pages/${joined}/index.astro`);
    }
  }
  for (const cand of cands) {
    if (existsSync(join(repoRoot, cand))) return cand;
  }
  return null;
}

const FROM_RE = /\bfrom\s*["'](\.{1,2}\/[^"']+)["']/g;
const SIDE_RE = /\bimport\s*["'](\.{1,2}\/[^"']+)["']/g;

// One level of local imports: for the thin [provider].astro wrapper the real
// content lives in the demo data module, so the page file alone would under-report.
function localImports(repoPath) {
  const abs = join(repoRoot, repoPath);
  if (!existsSync(abs)) return [];
  const text = readFileSync(abs, "utf8");
  const specs = new Set();
  for (const re of [FROM_RE, SIDE_RE]) {
    re.lastIndex = 0;
    let m;
    while ((m = re.exec(text))) specs.add(m[1]);
  }
  const out = [];
  for (const spec of specs) {
    const resolved = resolveFile(join(dirname(abs), spec));
    if (resolved) out.push(relative(repoRoot, resolved).split(sep).join("/"));
  }
  return out;
}

// Chrome detection: a file most pages pull in (the shared layout, nav, footer) is
// not content, so a change to it must not restamp every URL — that is the same
// false "everything changed" signal the build-date stamp produced. Only files
// referenced by at most half the pages count toward a page's lastmod.
function lastmodFor(repoPath) {
  const dates = [repoPath, ...localImports(repoPath)]
    .filter((f) => (REF_COUNT.get(f) || 0) <= CHROME_LIMIT)
    .map((f) => DATES.get(f))
    .filter(Boolean);
  return dates.length ? dates.sort().at(-1) : null;
}

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

const PAGES = files
  .map((f) => ({ f, repoPath: pageRepoPath(f) }))
  .filter((p) => p.repoPath);

const REF_COUNT = new Map();
for (const p of PAGES) {
  for (const dep of [p.repoPath, ...localImports(p.repoPath)]) {
    REF_COUNT.set(dep, (REF_COUNT.get(dep) || 0) + 1);
  }
}
const CHROME_LIMIT = PAGES.length / 2;

const rows = PAGES
  .map((p) => {
    let rel = relative(dist, p.f).split(sep).join("/");
    rel = rel === "index.html" ? "" : rel.replace(/\/index\.html$/, "/").replace(/\.html$/, "/");
    return { url: `${site}/${rel}`, lastmod: lastmodFor(p.repoPath) };
  })
  .sort((a, b) => a.url.localeCompare(b.url));

const dated = rows.filter((r) => r.lastmod).length;
const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${rows
  .map(
    (r) =>
      `  <url>\n    <loc>${r.url}</loc>\n${r.lastmod ? `    <lastmod>${r.lastmod}</lastmod>\n` : ""}  </url>`,
  )
  .join("\n")}
</urlset>
`;

writeFileSync(join(dist, "sitemap.xml"), xml);
console.log(`sitemap: ${rows.length} URLs written to dist/sitemap.xml (${dated} with <lastmod>)`);
