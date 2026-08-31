# TotalRecalls — Proposed Site Changes (FOR REVIEW)

Comparison target: **ai-chat-importer.com** (competitor). Our advantage = **8 AI providers** vs their 4.
Status: **PROPOSAL ONLY — no locked file has been touched.** Each change below shows exact OLD → NEW copy/code so you can approve precisely.

> ⚠️ LOCKED per `AGENTS.md`: `Nav.jsx`, `SentinelHero.jsx`, `ConvergenceDiagram.jsx`, `ResolutionPath.jsx`, `RiskMatrix.jsx`, `LibraryPreview.jsx`, `Guides.jsx`, `PricingSection.jsx`, `SiteFooter.jsx`, and `pages/index.astro`. **Nothing is edited until you say go.**
> ⚠️ **Stale note in AGENTS.md:** it says `RiskMatrix.jsx` is frozen at "Five AI providers" — the live site now says **"Eight AI providers"** (RiskMatrix.jsx:21). The memo is outdated and should be updated so a future session doesn't "fix" it back to five.

Canonical provider order used everywhere below (matches the RiskMatrix/library grid):
`ChatGPT · Claude · Perplexity · Gemini · Grok · DeepSeek · Mistral · Qwen Chat` (8)

---

## Change 1 — Align the provider count to 8 everywhere  🔴 HIGH IMPACT (copy only)

The pitch is "double the scope," but three surfaces still say **five**. Fix all three.

### 1A. `site/src/components/landing/SentinelHero.jsx` — line 21 (hero subtext)

**OLD:**
```jsx
              A Windows app that exports your ChatGPT, Claude, Perplexity, Gemini, and Grok chats into a private folder of Markdown + JSON you keep forever — long after the tab closes and the UI changes.
```
**NEW:**
```jsx
              A Windows app that exports your ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen chats into a private folder of Markdown + JSON you keep forever — long after the tab closes and the UI changes.
```

### 1B. `site/src/components/landing/PricingSection.jsx` — lines 41–47 ("Includes providers" list)

**OLD:**
```jsx
                <li className="text-foreground/90 font-medium">Perplexity</li>
                <li className="text-foreground/90 font-medium">ChatGPT</li>
                <li className="text-foreground/90 font-medium">Claude</li>
                <li className="text-foreground/90 font-medium">Gemini (Takeout)</li>
                <li className="text-foreground/90 font-medium">Grok</li>
```
**NEW:**
```jsx
                <li className="text-foreground/90 font-medium">ChatGPT</li>
                <li className="text-foreground/90 font-medium">Claude</li>
                <li className="text-foreground/90 font-medium">Perplexity</li>
                <li className="text-foreground/90 font-medium">Gemini (Takeout)</li>
                <li className="text-foreground/90 font-medium">Grok</li>
                <li className="text-foreground/90 font-medium">DeepSeek</li>
                <li className="text-foreground/90 font-medium">Mistral</li>
                <li className="text-foreground/90 font-medium">Qwen Chat</li>
```

### 1C. `site/src/pages/index.astro` — **both** JSON-LD descriptions (lines 14 and 43)

**OLD (appears twice):**
```
"A Windows app that exports your AI chat history from ChatGPT, Claude, Perplexity, Gemini, and Grok into local Markdown + JSON files you own forever."
```
**NEW (both occurrences):**
```
"A Windows app that exports your AI chat history from ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen into local Markdown + JSON files you own forever."
```

### 1D. (optional, for consistency) `site/src/components/landing/SiteFooter.jsx` — line 43 tagline

**OLD:** `A Windows app that saves your AI conversations as Markdown + JSON you keep forever.`
**NEW (optional):** `A Windows app that saves your AI conversations from eight providers as Markdown + JSON you keep forever.`

---

## Change 2 — Enrich the pricing card  🔴 HIGH IMPACT

Competitor's card = eyebrow label → headline → price → feature grid → platform line → dual CTA. Ours is `$24USD` + a bare list + an empty-looking column. Rebuild `PricingSection.jsx` (keeps `id="pricing"`, the `Relief · 06` eyebrow, and the Straight-talk trust bullets on the right).

**Full replacement for `site/src/components/landing/PricingSection.jsx`:**
```jsx
import { Check, ArrowRight, Download, ShieldCheck } from "lucide-react";

const FEATURES = [
  { t: "Eight AI providers", d: "ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral & Qwen — all in one library." },
  { t: "Unlimited exports", d: "No caps on conversations or file size. Export everything, as many times as you like." },
  { t: "100% local files", d: "Markdown + JSON on your own drive. Nothing leaves your machine — no cloud, no account." },
  { t: "Lifetime updates", d: "One-time purchase, free updates forever. 14-day money-back guarantee." },
];

const PROVIDERS = [
  "ChatGPT", "Claude", "Perplexity", "Gemini (Takeout)", "Grok", "DeepSeek", "Mistral", "Qwen Chat",
];

const STRAIGHT = [
  "Windows 10/11 now.",
  "SmartScreen warning explained — what it means and how to proceed.",
  "No AdSense clutter. This site sells a tool, not pageviews.",
];

export default function PricingSection() {
  return (
    <section id="pricing" className="border-t border-border bg-background text-foreground">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-16 md:py-24">
        <header className="mb-12">
          <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Relief · 06</span>
          <h2 className="font-heading text-3xl md:text-5xl font-bold tracking-tight mt-3">
            One price. Every conversation. Yours forever.
          </h2>
          <p className="font-body text-muted-foreground text-[15.5px] leading-relaxed mt-4 max-w-2xl">
            A one-time purchase — no subscription, no cloud fees. Export from eight AI providers into local Markdown + JSON you own.
          </p>
        </header>

        <div className="grid lg:grid-cols-[1.15fr_0.85fr] gap-6 items-start">
          {/* Pricing card */}
          <div className="bg-card border border-border/80 p-8 md:p-10">
            <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Desktop App — Windows 10/11</span>
            <div className="mt-6 flex items-end gap-3">
              <span className="font-heading text-5xl md:text-6xl font-bold tracking-tight text-foreground">$24USD</span>
              <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary mb-2">one-time · lifetime</span>
            </div>
            <p className="font-body text-muted-foreground text-[14.5px] leading-relaxed mt-4">
              14-day money-back guarantee — if it doesn't work for your setup, email us and we'll refund it, no questions asked.
            </p>

            <div className="grid sm:grid-cols-2 gap-px bg-border border border-border mt-8">
              {FEATURES.map((f) => (
                <div key={f.t} className="bg-background p-5">
                  <p className="font-heading text-[15px] font-semibold flex items-center gap-2">
                    <Check className="w-4 h-4 text-primary shrink-0" /> {f.t}
                  </p>
                  <p className="font-body text-muted-foreground text-[13.5px] leading-relaxed mt-2">{f.d}</p>
                </div>
              ))}
            </div>

            <div className="mt-8 flex flex-col sm:flex-row gap-3">
              <a href="/buy/" data-tr-buy aria-label="Buy TotalRecalls for $24" className="inline-flex items-center justify-center gap-2 bg-primary text-white px-7 py-4 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:opacity-90 transition-opacity shadow-sm">
                Buy TotalRecalls — $24USD <ArrowRight className="w-4 h-4" />
              </a>
              <a href="/download/" className="inline-flex items-center justify-center gap-2 border border-border bg-card text-foreground px-6 py-4 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:bg-muted/50 transition-colors">
                <Download className="w-4 h-4" /> Try the free download
              </a>
            </div>
            <p className="font-mono text-[11px] uppercase tracking-[0.16em] text-muted-foreground mt-4">
              Available now for Windows 10/11 · Mac coming soon
            </p>
          </div>

          {/* Straight talk */}
          <div className="lg:border-l lg:border-border lg:pl-8">
            <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary font-medium">Straight talk</span>
            <ul className="mt-6 space-y-3.5">
              {STRAIGHT.map((s) => (
                <li key={s} className="flex items-start gap-3.5 bg-card/60 border border-border/80 p-4 rounded-sm hover:border-primary/40 transition-colors">
                  <ShieldCheck className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                  <span className="font-body text-[14.5px] text-foreground font-medium leading-relaxed">{s}</span>
                </li>
              ))}
            </ul>
            <div className="mt-6 font-mono text-[11px] text-muted-foreground">
              <span className="font-semibold text-foreground uppercase tracking-wider block mb-2.5">Includes providers:</span>
              <ul className="space-y-1.5 border-l-2 border-primary/30 pl-3">
                {PROVIDERS.map((p) => (
                  <li key={p} className="text-foreground/90 font-medium">{p}</li>
                ))}
              </ul>
              <span className="block mt-3 text-[10.5px] opacity-70">Version v1.0.0</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
```

---

## Change 3 — Hero trust-bar upgrade  🟠 MEDIUM IMPACT

Add the competitor's trust signals without touching the diagram or the brand palette. Edits to `SentinelHero.jsx`:

1. **Badge above the headline** — `100% LOCAL · ZERO CLOUD UPLOAD`.
2. **Secondary outline CTA** after the buy button — `See how it works →` (links `/#resolution`).
3. **Provider chip strip** under the subtext — the 8 provider names as small mono chips (no logo assets exist yet, so text chips; swap in SVGs later if you add them).

**Full replacement for `site/src/components/landing/SentinelHero.jsx`:**
```jsx
import ConvergenceDiagram from "./ConvergenceDiagram";
import { ArrowRight, ShieldCheck, Lock, Database } from "lucide-react";

const TRUST = [
  { Icon: Lock, l: "Private by design", s: "Local sign-in · no cloud" },
  { Icon: Database, l: "One library", s: "Every AI provider, one local folder" },
  { Icon: ShieldCheck, l: "Yours forever", s: "" },
];

const PROVIDERS = ["ChatGPT", "Claude", "Perplexity", "Gemini", "Grok", "DeepSeek", "Mistral", "Qwen Chat"];

export default function SentinelHero() {
  return (
    <section id="top" className="relative border-b border-border overflow-hidden">
      <div className="absolute inset-0 tr-grid-bg opacity-60 pointer-events-none" />
      <div className="relative mx-auto max-w-[1400px] px-5 md:px-10 pt-16 md:pt-24 pb-20 md:pb-28">
        <div className="grid lg:grid-cols-[1.1fr_0.9fr] gap-12 lg:gap-16 items-center">
          <div>
            <span className="inline-flex items-center gap-2 border border-primary/40 text-primary font-mono text-[10px] uppercase tracking-[0.18em] px-3 py-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-primary" /> 100% local · zero cloud upload
            </span>
            <h1 className="font-heading text-[44px] md:text-[68px] leading-[0.98] font-bold tracking-tight mt-6">
              Recall every AI conversation.
            </h1>
            <p className="font-body text-muted-foreground text-[16px] md:text-[18px] leading-relaxed mt-6 max-w-xl">
              A Windows app that exports your ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen chats into a private folder of Markdown + JSON you keep forever — long after the tab closes and the UI changes.
            </p>

            <div className="mt-5 flex flex-wrap gap-2">
              {PROVIDERS.map((p) => (
                <span key={p} className="font-mono text-[10px] uppercase tracking-[0.12em] border border-border rounded-sm px-2.5 py-1 text-muted-foreground">{p}</span>
              ))}
            </div>

            <div className="mt-9 flex flex-col sm:flex-row gap-3">
              <a href="#pricing" data-tr-buy className="inline-flex items-center justify-center gap-2 bg-primary text-white px-6 py-3.5 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:opacity-90 transition-opacity">
                Buy TotalRecalls — $24USD <ArrowRight className="w-4 h-4" />
              </a>
              <a href="#resolution" className="inline-flex items-center justify-center gap-2 border border-border bg-card text-foreground px-6 py-3.5 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:bg-muted/50 transition-colors">
                See how it works
              </a>
            </div>
            <p className="font-mono text-[11px] uppercase tracking-[0.18em] text-muted-foreground mt-3">
              Discounted launch price · One-time · Download link sent after checkout
            </p>

            <div className="mt-10 grid grid-cols-3 gap-6 border-t border-border pt-6">
              {TRUST.map((x) => (
                <div key={x.l}>
                  <x.Icon className="w-4 h-4 text-primary" />
                  <p className="font-heading text-[14px] font-semibold mt-2">{x.l}</p>
                  {x.s && <p className="font-mono text-[10px] text-muted-foreground mt-0.5">{x.s}</p>}
                </div>
              ))}
            </div>
          </div>

          <div className="relative">
            <ConvergenceDiagram />
          </div>
        </div>
      </div>
    </section>
  );
}
```

---

## Change 4 — Product visuals  🟠 MEDIUM IMPACT (needs an asset)

Competitor leads with a real product mockup (laptop + phone). Our hero is abstract (diagram). Add a dedicated product showcase section that shows the actual archive/export UI.

**Asset needed:** a clean screenshot of the app's library/export interface (or use the demo video as an autoplay poster). Existing demo footage:
`C:\Users\break\Videos\TR-demo-shoot\Video v4\TotalRecalls_demo_v3.mp4`

**Proposed new component `site/src/components/landing/ProductShowcase.jsx`** (insert into `index.astro` right after `<SentinelHero />`):
```jsx
import { ArrowRight } from "lucide-react";

export default function ProductShowcase() {
  return (
    <section id="product" className="border-t border-border tr-grid-bg">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-20 md:py-28">
        <header className="mb-12 max-w-3xl">
          <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">The Archive · 02</span>
          <h2 className="font-heading text-3xl md:text-5xl font-bold tracking-tight mt-3">Your conversations, exported to your drive.</h2>
          <p className="font-body text-muted-foreground text-[15px] leading-relaxed mt-4">
            Every chat becomes a readable Markdown file plus a structured JSON mirror — browseable, searchable, and yours to keep.
          </p>
        </header>
        <div className="bg-card border border-border/80 p-6 md:p-8">
          {/* Replace with a real app screenshot or an autoplay muted loop of the demo video */}
          <video
            className="w-full rounded-sm border border-border/60"
            src="/demo/totalrecalls-demo.mp4"
            poster="/demo/totalrecalls-poster.png"
            controls
            muted
            loop
            playsInline
          />
          <div className="mt-6 flex items-center justify-between">
            <span className="font-mono text-[11px] uppercase tracking-[0.16em] text-muted-foreground">Local storage. Your drive. Your files.</span>
            <a href="/download/" className="group inline-flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.18em] text-primary hover:underline">
              Try it free <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
```
> Note: this introduces a "02" eyebrow and shifts the existing section numbering. See the renumbering note under Change 5 — if you'd rather not renumber, give it a non-sequential label or drop the eyebrow.

---

## Change 5 — FAQ accordion section  🟢 LOWER IMPACT

Competitor pre-empts objections with an on-page FAQ. You already have a full `/faq/` page — surface the key questions on the landing page with an accordion that links to the full page.

**Proposed new component `site/src/components/landing/FaqSection.jsx`** (insert into `index.astro` after `<PricingSection />`, before `<LegalSection />`):
```jsx
import { useState } from "react";
import { ChevronDown, ArrowUpRight } from "lucide-react";

const FAQ = [
  { q: "Does TotalRecalls upload my data to the cloud?", a: "No. Everything stays local — your chats are exported to Markdown + JSON folders on your own drive. No account, no servers, nothing leaves your machine." },
  { q: "Is it a subscription?", a: "No. It's a one-time $24USD purchase with lifetime updates and a 14-day money-back guarantee." },
  { q: "Which AI providers are supported?", a: "Eight: ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen Chat." },
  { q: "How do I export my conversations?", a: "Each provider has its own export flow. Follow the free guides on our site — or import the provider's official export once and TotalRecalls handles the rest." },
  { q: "What if a provider changes its export format?", a: "We actively maintain compatibility with all eight providers and ship updates when they change their data structure. Your existing archive is never affected." },
  { q: "Is there a free option?", a: "The guides are free, and you can download the app to try it. It's a one-time purchase when you're ready to own your full archive." },
];

export default function FaqSection() {
  const [open, setOpen] = useState(0);
  return (
    <section id="faq" className="border-t border-border">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-16 md:py-24">
        <header className="mb-10 max-w-3xl">
          <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Questions · 07</span>
          <h2 className="font-heading text-3xl md:text-5xl font-bold tracking-tight mt-3">Frequently asked questions.</h2>
        </header>
        <div className="divide-y divide-border border border-border">
          {FAQ.map((item, i) => (
            <div key={item.q}>
              <button
                onClick={() => setOpen(open === i ? -1 : i)}
                className="w-full flex items-center justify-between gap-4 px-6 py-5 text-left hover:bg-muted/30 transition-colors"
              >
                <span className="font-heading text-[16px] font-semibold">{item.q}</span>
                <ChevronDown className={`w-5 h-5 shrink-0 text-muted-foreground transition-transform ${open === i ? "rotate-180" : ""}`} />
              </button>
              {open === i && (
                <div className="px-6 pb-5 font-body text-[15px] text-muted-foreground leading-relaxed">{item.a}</div>
              )}
            </div>
          ))}
        </div>
        <a href="/faq/" className="mt-6 inline-flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.18em] text-primary hover:underline">
          Read the full FAQ <ArrowUpRight className="w-3.5 h-3.5" />
        </a>
      </div>
    </section>
  );
}
```

**Section-numbering ripple (cosmetic):** the landing page uses hard-coded eyebrows (`· 02` … `· 07`). Adding Showcase (02) and FAQ (07) means renumbering: Matrix 02→03, Library 03→04, Guides 04→05, Microsoft Warning 05→06, Pricing 06→07, FAQ 07→08, Legal 07→08. **Do you want me to renumber, or keep the new sections on neutral labels?** (Cheapest: don't number the new sections, or number FAQ as 07 and bump only Legal to 08.)

---

## Change 6 — Mobile / portability angle  🟢 LOWER IMPACT (choices)

**Honest note up front:** the competitor's "Works on Mobile — No App Store Required" works because they ship a *free web app*. We are a Windows desktop app with no web tier, so an identical "mobile" section would be misleading. Two options:

- **Option 6a (recommended, copy-only):** Reframe as **portability** — "Your library travels with you." Markdown + JSON are plain files: back them up to any cloud drive, open them in any editor, sync them across devices. Matches our real product and answers the same "is it locked to one machine" worry.
- **Option 6b (strategic, bigger scope):** Add a free web/importer tier to truly match the competitor's free + paid funnel. Out of scope for a visual copy pass — flagging it as the single biggest *commercial* gap, separate from visual polish.

**Proposed new component `site/src/components/landing/PortabilitySection.jsx` for 6a** (insert after `<FaqSection />`, before `<LegalSection />`):
```jsx
import { FolderSync, HardDrive, FileText } from "lucide-react";

const PORTS = [
  { Icon: HardDrive, t: "Plain files, not silos", d: "Every chat is a readable .md file plus a structured .json mirror. No proprietary database, no lock-in." },
  { Icon: FolderSync, t: "Back up anywhere", d: "Drop your library folder into OneDrive, Google Drive, or a USB drive — it's just files." },
  { Icon: FileText, t: "Open in any tool", d: "Work with your conversations in Obsidian, Notion, any editor, or your own scripts." },
];

export default function PortabilitySection() {
  return (
    <section id="portability" className="border-t border-border tr-grid-bg">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-20 md:py-28">
        <header className="mb-12 max-w-3xl">
          <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Portability</span>
          <h2 className="font-heading text-3xl md:text-5xl font-bold tracking-tight mt-3">Your library travels with you.</h2>
          <p className="font-body text-muted-foreground text-[15px] leading-relaxed mt-4">
            No proprietary database and no cloud. Your archive is plain Markdown + JSON — back it up anywhere and open it anywhere.
          </p>
        </header>
        <div className="grid md:grid-cols-3 gap-px bg-border border border-border">
          {PORTS.map((p) => (
            <div key={p.t} className="bg-card p-7">
              <p.Icon className="w-5 h-5 text-primary" />
              <p className="font-heading text-[16px] font-semibold mt-4">{p.t}</p>
              <p className="font-body text-muted-foreground text-[14px] leading-relaxed mt-2">{p.d}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

---

## Where new sections go in `site/src/pages/index.astro`

Current order: `<ThreatFeed /> … <Nav /> <SentinelHero /> <ResolutionPath /> <RiskMatrix /> <LibraryPreview /> <Guides /> <MicrosoftWarningSection /> <PricingSection /> <LegalSection /> <SiteFooter />`

Proposed insertion (and the import lines to add at the top):
- `<ProductShowcase />` after `<SentinelHero />`  (Change 4)
- `<FaqSection />` after `<PricingSection />`  (Change 5)
- `<PortabilitySection />` after `<FaqSection />`  (Change 6a)
- Add imports: `import ProductShowcase from "../components/landing/ProductShowcase.jsx";` etc.

---

## Suggested review order & risk

| # | Change | Risk | Effort |
|---|--------|------|--------|
| 1 | Provider count → 8 (copy) | None (copy only) | ~10 min |
| 2 | Pricing card rebuild | Low (self-contained component) | ~30 min |
| 3 | Hero trust signals | Low (additive; diagram untouched) | ~20 min |
| 4 | Product visuals | Needs screenshot/video asset | varies |
| 5 | FAQ accordion | Low; **decide renumbering** | ~20 min |
| 6a | Portability section | Low | ~15 min |
| 6b | Free web tier | **Strategic** — separate decision | large |

**Recommended:** approve **1 + 2 + 3** first (pure win, no asset dependency, closes the biggest gap). Then decide on 4 (asset), 5 (numbering), 6a/6b (strategy).
