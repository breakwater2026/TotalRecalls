import React from "react";
import { Plus } from "lucide-react";
import { Container, Section, Eyebrow, Btn } from "./ui";

/* ============================================================================
 * /library/ — "The Library" (Jasper rewrite, tr/ design system).
 * Copy + spec from: Marketing/Jasper/Website Rewrite/TotalRecalls Library Page.md
 * ========================================================================== */

const FOLDERS = [
  {
    name: "chatgpt",
    sub: "12,847 files · 6.2 GB",
    files: [
      { f: "2026-09-28-1505-python-list-comprehensions.md", j: true },
      { f: "2026-09-28-1440-react-hook-debug.md", j: true },
      { f: "2026-09-28-0905-sql-query-help.md", j: true },
      { f: "2026-09-27-1120-project-roadmap-draft.md", j: true },
    ],
  },
  {
    name: "claude",
    sub: "3,102 files · 1.4 GB",
    files: [
      { f: "2026-09-29-1922-project-naming.md", j: true },
      { f: "2026-09-29-1640-api-architecture-review.md", j: true },
      { f: "2026-09-29-1105-python-asyncio-tutorial.md", j: true },
      { f: "2026-09-29-0815-customer-reply-draft.md", j: true },
    ],
  },
  {
    name: "perplexity",
    sub: "964 files · 812 MB",
    files: [
      { f: "2026-09-29-2130-quantum-computing-explained.md", j: true },
      { f: "2026-09-29-2015-competitive-landscape-ai.md", j: true },
      { f: "2026-09-29-1544-market-trends-2026.md", j: true },
      { f: "2026-09-29-1320-llm-evaluation-methods.md", j: true },
    ],
  },
  {
    name: "gemini",
    sub: "2,310 files · 1.1 GB",
    files: [
      { f: "2026-09-29-2205-workout-plan-6am.md", j: true },
      { f: "2026-09-29-1830-product-launch-ideas.md", j: true },
      { f: "2026-09-29-1415-recipe-italian-dinner.md", j: true },
      { f: "2026-09-29-1200-garden-planning-fall.md", j: true },
    ],
  },
  {
    name: "grok",
    sub: "688 files · 504 MB",
    files: [
      { f: "2026-09-29-2340-tesla-earnings-analysis.md", j: true },
      { f: "2026-09-29-2055-tech-today-summaries.md", j: true },
      { f: "2026-09-29-1720-xai-model-comparison.md", j: true },
      { f: "2026-09-29-1410-ai-news-briefing.md", j: true },
    ],
  },
];

function FileRow({ file }) {
  return (
    <div className="flex items-center gap-3 rounded px-3 py-2 text-left transition-colors hover:bg-tr-slate/30">
      <svg className="h-3.5 w-3.5 shrink-0 text-tr-dust" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
        <path d="M4.5 1.5H9l3 3v8a.5.5 0 0 1-.5.5h-7a.5.5 0 0 1-.5-.5v-11z" strokeLinejoin="round" />
        <path d="M9 1.5v3h3" strokeLinejoin="round" />
      </svg>
      <code className="min-w-0 flex-1 truncate font-mono text-[12px] text-tr-mist">{file.f}</code>
      {file.j && (
        <code className="hidden sm:inline font-mono text-[10px] text-tr-dust">+.json</code>
      )}
    </div>
  );
}

function FileBrowser() {
  return (
    <div className="min-w-0 rounded-card border border-tr-slate bg-tr-graphite p-2 md:p-4">
      {/* window title bar */}
      <div className="flex items-center gap-2 border-b border-tr-slate px-3 py-2.5">
        <span className="h-2.5 w-2.5 rounded-full bg-tr-slate" />
        <span className="h-2.5 w-2.5 rounded-full bg-tr-slate" />
        <span className="h-2.5 w-2.5 rounded-full bg-tr-steel" />
        <span className="ml-3 min-w-0 truncate font-mono text-[12px] text-tr-dust">
          C:\TotalRecalls\Library\
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-[220px_1fr]">
        {/* folder sidebar */}
        <div className="border-b border-tr-slate md:border-b-0 md:border-r min-w-0">
          {FOLDERS.map((fd, i) => (
            <div
              key={fd.name}
              className={`flex items-center gap-2.5 border-b border-tr-slate px-3 py-3 last:border-b-0 ${
                i === 0 ? "bg-tr-obsidian" : ""
              }`}
            >
              <svg className="h-3.5 w-3.5 shrink-0 text-tr-steel" viewBox="0 0 14 14" fill="currentColor" aria-hidden="true">
                <path d="M1 3.5A1.5 1.5 0 0 1 2.5 2H5l1.5 1.5h5A1.5 1.5 0 0 1 13 5v5.5A1.5 1.5 0 0 1 11.5 12h-9A1.5 1.5 0 0 1 1 10.5v-7z" />
              </svg>
              <div className="min-w-0">
                <div className="font-mono text-[12px] font-medium text-tr-paper">/{fd.name}</div>
                <div className="font-mono text-[10px] text-tr-dust">{fd.sub}</div>
              </div>
            </div>
          ))}
        </div>

        {/* file list (chatgpt) */}
        <div className="p-2 md:p-3 min-w-0">
          <div className="mb-1 px-3 pt-1 font-mono text-[10px] uppercase tracking-[0.16em] text-tr-dust">
            /chatgpt — recent
          </div>
          {FOLDERS[0].files.map((fl) => (
            <FileRow key={fl.f} file={fl} />
          ))}
          <div className="mt-2 px-3 pb-1">
            <span className="inline-flex items-center gap-2 rounded-chip bg-tr-slate px-2 py-1 font-mono text-[10px] uppercase tracking-[0.12em] text-tr-mist">
              Saved locally
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

const FEATURES = [
  {
    t: "Markdown you can read",
    b: "Every conversation saves as a .md file. Open it in Notepad, VS Code, Obsidian, or any text editor. No special software, no login wall.",
  },
  {
    t: "JSON for structure",
    b: "Each conversation also saves as .json, with the full structure: roles, timestamps, and metadata. If you build tools on top of your chats, this is the version for you.",
  },
  {
    t: "One folder per provider",
    b: "Your files organize themselves. One folder per provider under C:\\TotalRecalls\\Library\\. No tags to manage, no database to maintain.",
  },
  {
    t: "Dates in the filename",
    b: "Files are named with the conversation date and time, so sorting by name puts your history in chronological order. No metadata search required to find that conversation from last Tuesday.",
  },
  {
    t: "Search like a local file",
    b: "Your chats live on your drive as plain text. Windows Search, Everything, or grep all work on them the way they work on your other documents.",
  },
  {
    t: "UTF-8 throughout",
    b: "Accents, CJK characters, emoji, and code symbols stay intact from provider to file. What you typed is what you saved.",
  },
];

const FILE_TYPES = [
  { ext: ".md", what: "The readable copy", b: "Your conversation as plain text, with roles and timestamps. Opens in anything." },
  { ext: ".json", what: "The structured copy", b: "The same conversation with full metadata, for scripts, imports, or archives." },
];

const FAQS = [
  {
    q: "Where do my files go?",
    a: "C:\\TotalRecalls\\Library\\, with a subfolder for each provider. You can change the location in Settings if you want your files elsewhere.",
  },
  {
    q: "What's the difference between .md and .json?",
    a: "The .md file is for reading. The .json file is for structure. You can use one, both, or neither depending on your workflow.",
  },
  {
    q: "Can I delete files TotalRecalls saves?",
    a: "Yes. They're regular files on your drive. Delete, move, rename, or back them up however you manage the rest of your documents.",
  },
  {
    q: "Does TotalRecalls upload my files anywhere?",
    a: "No. Your Library is local. The app itself doesn't require an account, and your files don't leave your PC unless you send them somewhere.",
  },
  {
    q: "Can I open .md files on my phone?",
    a: "Yes. Transfer them to your phone through any file manager or cloud folder and open them in any text or Markdown reader.",
  },
];

export default function LibraryPage() {
  return (
    <div>
      {/* 1. Hero */}
      <div className="bg-tr-obsidian pt-16 pb-16 md:pt-32 md:pb-24">
        <Container>
          <div className="grid lg:grid-cols-[1.05fr_1fr] gap-10 items-center">
            <div>
              <Eyebrow mono>The Library</Eyebrow>
              <h1 className="mt-3 font-heading text-[34px] md:text-[48px] font-bold leading-[1.1] tracking-[-0.02em] text-tr-paper">
                Your AI chats, saved as files you actually use.
              </h1>
              <p className="mt-6 font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-mist">
                Every conversation TotalRecalls saves becomes two files on your drive: a Markdown
                file you can read in any text editor, and a JSON file with the full structure. Your
                chats stop being a thing you can only see in a provider&apos;s app and become
                documents in your own Library.
              </p>
              <div className="mt-8 flex flex-col sm:flex-row sm:items-center gap-4">
                <Btn href="/download/" large>Download free</Btn>
                <a href="#library" className="inline-flex items-center justify-center gap-2 border border-tr-slate bg-transparent px-6 py-3 font-body text-[15px] font-medium text-tr-mist hover:bg-tr-slate/40 hover:text-tr-paper transition-colors">
                  See the file browser &darr;
                </a>
              </div>
            </div>
            <FileBrowser />
          </div>
        </Container>
      </div>

      {/* 2. What you get */}
      <Section id="library" className="border-t border-tr-slate bg-tr-obsidian">
        <Container>
          <Eyebrow>Every chat becomes</Eyebrow>
          <h2 className="mt-3 max-w-[680px] font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
            Two files you can open, search, and keep
          </h2>
          <p className="mt-4 max-w-[680px] font-body text-[16px] leading-[1.6] text-tr-mist">
            One for reading, one for structure. Both plain text, both on your drive.
          </p>
          <div className="mt-10 grid md:grid-cols-2 gap-6">
            {FILE_TYPES.map((t) => (
              <div key={t.ext} className="rounded-card border border-tr-slate bg-tr-graphite p-6">
                <code className="font-mono text-[15px] font-semibold text-tr-amber">{t.ext}</code>
                <div className="mt-1 font-mono text-[12px] uppercase tracking-[0.08em] text-tr-dust">{t.what}</div>
                <p className="mt-4 font-body text-[16px] leading-[1.6] text-tr-mist">{t.b}</p>
              </div>
            ))}
          </div>
        </Container>
      </Section>

      {/* 3. How the Library works */}
      <Section className="border-t border-tr-slate bg-tr-graphite">
        <Container>
          <Eyebrow>How it&apos;s organized</Eyebrow>
          <h2 className="mt-3 max-w-[680px] font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
            The Library is just a folder, set up the way files should be
          </h2>
          <p className="mt-4 max-w-[680px] font-body text-[16px] leading-[1.6] text-tr-mist">
            No proprietary format, no lock-in. Here&apos;s what makes it easy to live with.
          </p>
          <div className="mt-10 grid gap-5 md:grid-cols-2">
            {FEATURES.map((f) => (
              <div key={f.t} className="rounded-card border border-tr-slate bg-tr-obsidian p-6">
                <h4 className="font-heading text-[17px] font-semibold text-tr-paper">{f.t}</h4>
                <p className="mt-3 font-body text-[15px] leading-[1.6] text-tr-mist">{f.b}</p>
              </div>
            ))}
          </div>
        </Container>
      </Section>

      {/* 4. What a saved file looks like */}
      <Section className="border-t border-tr-slate bg-tr-obsidian">
        <Container>
          <div className="grid lg:grid-cols-[1fr_1.1fr] gap-12 items-center">
            <div>
              <Eyebrow>In practice</Eyebrow>
              <h2 className="mt-3 font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
                What a saved chat looks like
              </h2>
              <p className="mt-4 font-body text-[16px] leading-[1.6] text-tr-mist">
                A .md file reads like the conversation you had, with the date and provider in the
                name and each message clearly labeled. The .json next to it carries the same content
                with roles and timestamps as structured data.
              </p>
              <div className="mt-8 flex flex-col sm:flex-row sm:items-center gap-4">
                <Btn href="/download/">Download free</Btn>
                <Btn href="/guides/" variant="tertiary">Browse the guides &rarr;</Btn>
              </div>
            </div>
            <pre className="overflow-x-auto rounded-card border border-tr-slate bg-tr-obsidian p-5 font-mono text-[12.5px] leading-[1.7] text-tr-mist min-w-0">
{`# Python list comprehensions — help with .md/.json
Saved: 2026-09-28 15:05
Provider: ChatGPT

## You
How do I filter a list of dicts where
the 'status' field is 'active'?

## ChatGPT
Use a comprehension with the condition
inside the brackets:

    active = [u for u in users
              if u["status"] == "active"]

This keeps only the entries whose
status matches, in the original order.`}
            </pre>
          </div>
        </Container>
      </Section>

      {/* 5. FAQ */}
      <Section className="border-t border-tr-slate bg-tr-graphite">
        <Container>
          <div className="grid lg:grid-cols-[1fr_1.6fr] gap-12 items-start">
            <div>
              <Eyebrow>FAQ</Eyebrow>
              <h2 className="mt-3 font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
                Questions about the Library
              </h2>
              <p className="mt-4 max-w-sm font-body text-[15px] leading-[1.6] text-tr-mist">
                Your files are yours. That&apos;s the whole point.
              </p>
            </div>
            <div className="border-t border-tr-slate">
              {FAQS.map((f) => (
                <details key={f.q} className="group border-b border-tr-slate py-4">
                  <summary className="flex items-center justify-between gap-4 cursor-pointer list-none">
                    <span className="font-heading text-[16.5px] font-semibold text-tr-paper">{f.q}</span>
                    <Plus className="w-4 h-4 text-tr-steel shrink-0 transition-transform group-open:rotate-45" />
                  </summary>
                  <p className="mt-3 max-w-2xl font-body text-[15px] leading-[1.6] text-tr-mist">{f.a}</p>
                </details>
              ))}
            </div>
          </div>
        </Container>
      </Section>

      {/* 6. CTA */}
      <Section className="border-t border-tr-slate bg-tr-obsidian">
        <Container>
          <div className="max-w-[680px]">
            <h2 className="font-heading text-[28px] md:text-[40px] font-bold leading-[1.1] tracking-[-0.02em] text-tr-paper">
              Save your first batch of chats and see the Library fill up.
            </h2>
            <p className="mt-5 font-body text-[18px] leading-[1.55] text-tr-mist">
              Download TotalRecalls, sign in to one of the free-tier providers, and pick a
              conversation. A few seconds later, the files are in C:\TotalRecalls\Library\.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row sm:items-center gap-4">
              <Btn href="/download/" large>Download free</Btn>
              <Btn href="/pricing/" variant="tertiary">Compare Free and Pro &rarr;</Btn>
            </div>
          </div>
        </Container>
      </Section>
    </div>
  );
}
