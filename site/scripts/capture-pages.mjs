// Capture one full-page PNG per site page (52) for the Lemon Squeezy review pack.
// Usage: node scripts/capture-pages.mjs  (dev server must be up on 127.0.0.1:4321)
import { chromium } from "playwright-core";
import fs from "node:fs";
import path from "node:path";

const BASE = "http://127.0.0.1:4321";
const OUT = path.resolve("docs-screenshots"); // created next to site/
const EDGE = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe";

// (urlPath, label) — 52 entries, one per Astro page
const PAGES = [
  ["/", "home"],
  ["/about/", "about"],
  ["/buy/", "buy"],
  ["/compare/", "compare-index"],
  ["/compare/chatgpt/", "compare-chatgpt"],
  ["/compare/claude/", "compare-claude"],
  ["/compare/deepseek/", "compare-deepseek"],
  ["/compare/gemini/", "compare-gemini"],
  ["/compare/grok/", "compare-grok"],
  ["/compare/mistral/", "compare-mistral"],
  ["/compare/perplexity/", "compare-perplexity"],
  ["/compare/pricing/", "compare-pricing"],
  ["/compare/qwen/", "compare-qwen"],
  ["/compare/why-local/", "compare-why-local"],
  ["/compare/why-multi-assistant/", "compare-why-multi-assistant"],
  ["/download/", "download"],
  ["/faq/", "faq"],
  ["/feature-requests/", "feature-requests"],
  ["/guides/", "guides-index"],
  ["/guides/backup-perplexity-threads/", "guide-backup-perplexity-threads"],
  ["/guides/deepseek/", "guide-deepseek"],
  ["/guides/export-chatgpt-conversations/", "guide-export-chatgpt"],
  ["/guides/export-claude-chat-history/", "guide-export-claude"],
  ["/guides/gemini-takeout-archive/", "guide-gemini-takeout"],
  ["/guides/grok/", "guide-grok"],
  ["/guides/library-format/", "guide-library-format"],
  ["/guides/mistral/", "guide-mistral"],
  ["/guides/own-your-ai-chat-data/", "guide-own-your-ai-chat-data"],
  ["/guides/qwen/", "guide-qwen"],
  ["/guides/smartscreen/", "guide-smartscreen"],
  ["/guides/troubleshooting/", "guide-troubleshooting"],
  ["/help/", "help"],
  ["/how-it-works/", "how-it-works"],
  ["/legals/", "legals"],
  ["/microsoft-warning/", "microsoft-warning"],
  ["/press/", "press"],
  ["/previews/", "previews-index"],
  ["/previews/multi-device-memory/", "preview-multi-device-memory"],
  ["/previews/notion/", "preview-notion"],
  ["/previews/obsidian/", "preview-obsidian"],
  ["/previews/rag-containers/", "preview-rag-containers"],
  ["/previews/semantic-search/", "preview-semantic-search"],
  ["/pricing/", "pricing"],
  ["/privacy/", "privacy"],
  ["/release-notes/", "release-notes"],
  ["/roadmap/", "roadmap"],
  ["/support/", "support"],
  ["/terms/", "terms"],
  ["/thanks/", "thanks"],
  ["/why-this-matters/", "why-this-matters"],
  ["/windows-firewall/", "windows-firewall"],
  ["/__404__", "not-found-404"], // special: hit a bogus route
];

const results = [];
fs.mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch({ executablePath: EDGE, args: ["--no-first-run"] });
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();

for (let i = 0; i < PAGES.length; i++) {
  const [urlPath, label] = PAGES[i];
  const url = urlPath === "/__404__" ? BASE + "/definitely-not-a-real-page-xyz123" : BASE + urlPath;
  const file = path.join(OUT, `${String(i + 1).padStart(2, "0")}-${label}.png`);
  try {
    const resp = await page.goto(url, { waitUntil: "networkidle", timeout: 45000 });
    const status = resp ? resp.status() : "no-resp";
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(700); // let images/layout settle
    await page.screenshot({ path: file, fullPage: true });
    results.push({ n: i + 1, label, url, status, file });
    process.stdout.write(`[${i + 1}/${PAGES.length}] ${label}  http=${status}  ${Math.round(fs.statSync(file).size / 1024)}KB\n`);
  } catch (e) {
    results.push({ n: i + 1, label, url, error: String(e).slice(0, 200), file: null });
    process.stdout.write(`[${i + 1}/${PAGES.length}] ${label}  ERROR ${String(e).slice(0, 120)}\n`);
  }
}
await browser.close();
fs.writeFileSync(path.join(OUT, "_manifest.json"), JSON.stringify(results, null, 2));
const ok = results.filter(r => r.file).length;
console.log(`\nDONE: ${ok}/${PAGES.length} captured -> ${OUT}`);
console.log("manifest: " + path.join(OUT, "_manifest.json"));
