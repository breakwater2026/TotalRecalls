import React from "react";
import { ArrowRight } from "lucide-react";
import { Container, Section, Eyebrow, Btn } from "./ui";

/* ============================================================================
 * /ownership/ — "The Ownership Path" (Jasper rewrite, tr/ design system).
 * Copy + spec from: Marketing/Jasper/Website Rewrite/TotalRecalls Ownership Path Page.md
 * ========================================================================== */

const TERMINAL = [
  { t: "PS C:\\TotalRecalls> totalrecalls export --provider chatgpt", c: "" },
  { t: "Signing in to ChatGPT... ok", c: "dim" },
  { t: "Found 142 conversations", c: "" },
  { t: "  [1] 2026-09-28 python-list-comprehensions   (saved)", c: "dim" },
  { t: "  [2] 2026-09-28 react-hook-debug             (saved)", c: "dim" },
  { t: "  [3] 2026-09-27 sql-query-help               (saved)", c: "dim" },
  { t: "Export complete: 142 files -> C:\\TotalRecalls\\Library\\chatgpt\\", c: "amber" },
  { t: "PS C:\\TotalRecalls>", c: "" },
];

const STEPS = [
  {
    n: "01",
    t: "Download TotalRecalls",
    b: "One installer for Windows 10 and 11. No account required to start. Free tier includes ChatGPT, Claude, and Perplexity.",
    chip: "Free to start",
    link: { label: "Download free", href: "/download/" },
  },
  {
    n: "02",
    t: "Pick your providers",
    b: "Sign in locally, inside the app. TotalRecalls talks to each provider on your machine; your credentials never leave your PC.",
    chip: "8 providers",
    link: { label: "See supported providers", href: "/providers/" },
  },
  {
    n: "03",
    t: "Save to your Library",
    b: "Every conversation becomes a .md and a .json in C:\\TotalRecalls\\Library\\. One folder per provider, dated filenames, ready for any text editor.",
    chip: "Saved locally",
    link: { label: "Learn how the Library works", href: "/library/" },
  },
];

const COMPARE = [
  { cap: "ChatGPT", tr: "Full thread as dated, readable files", o: "One zip of raw JSON" },
  { cap: "Claude", tr: "Projects and threads as .md/.json", o: "Project export (limited)" },
  { cap: "Perplexity", tr: "Threads saved before the tab trail vanishes", o: "None" },
  { cap: "Gemini", tr: "Takeout archive converted to Markdown", o: "Raw Takeout zip" },
  { cap: "Grok", tr: "Chats + X-post references, local", o: "None" },
  { cap: "DeepSeek", tr: "Conversations with R1 thinking traces", o: "None" },
  { cap: "Mistral", tr: "Le Chat, UTF-8 intact", o: "None" },
  { cap: "Qwen", tr: "chat.qwen.ai history, multilingual", o: "None" },
];

const CHECKS = [
  "Read your chats in Notepad, VS Code, or Obsidian",
  "Search your history with Windows Search or Everything",
  "Back up your conversations with any file backup",
  "Move to a new PC and keep everything",
  "Hand a thread to a colleague as a file",
  "Know exactly where every conversation lives",
];

export default function OwnershipPage() {
  return (
    <div>
      {/* 1. Hero */}
      <div className="bg-tr-obsidian pt-16 pb-16 md:pt-32 md:pb-24">
        <Container>
          <div className="max-w-[720px]">
            <Eyebrow mono>The ownership path</Eyebrow>
            <h1 className="mt-3 font-heading text-[34px] md:text-[48px] font-bold leading-[1.1] tracking-[-0.02em] text-tr-paper">
              Your AI chats should live on your drive, not in a provider&apos;s cloud.
            </h1>
            <p className="mt-6 font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-mist">
              Every provider keeps your conversations in its own app. Close the tab, change the
              plan, and the history is wherever that company puts it. TotalRecalls brings those
              chats home: plain Markdown and JSON files, in a Library on your own PC, that you can
              read, search, and back up like any other document.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row sm:items-center gap-4">
              <Btn href="/download/" large>Download free</Btn>
              <Btn href="/providers/" variant="tertiary">See supported providers &rarr;</Btn>
            </div>
            <div className="mt-8 flex flex-wrap gap-2">
              {["8 providers", ".md + .json", "C:\\TotalRecalls\\Library\\", "no account needed"].map((c) => (
                <span key={c} className="inline-flex whitespace-nowrap rounded-chip bg-tr-slate px-2 py-1 font-mono text-[12px] font-medium uppercase tracking-[0.02em] text-tr-dust">
                  {c}
                </span>
              ))}
            </div>
          </div>
        </Container>
      </div>

      {/* 2. What owning your chats means */}
      <Section className="border-t border-tr-slate bg-tr-obsidian">
        <Container>
          <div className="grid lg:grid-cols-[1.1fr_1fr] gap-12 items-center">
            <div>
              <Eyebrow>What owning your chats means</Eyebrow>
              <h2 className="mt-3 font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
                Owning your chats means they behave like your other documents
              </h2>
              <p className="mt-4 max-w-[560px] font-body text-[16px] leading-[1.6] text-tr-mist">
                Right now your AI history is a feature of someone else&apos;s product. TotalRecalls
                makes it your data: files you can open without logging in, search without a special
                tool, and keep when the provider&apos;s plan changes.
              </p>
              <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-3">
                {CHECKS.map((c) => (
                  <div key={c} className="flex items-start gap-2.5">
                    <svg className="mt-0.5 h-4 w-4 shrink-0 text-tr-green" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
                      <path d="M3 8.5 6.5 12 13 4.5" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                    <span className="font-body text-[15px] leading-[1.5] text-tr-mist">{c}</span>
                  </div>
                ))}
              </div>
            </div>
            {/* terminal mock */}
            <div className="rounded-card border border-tr-slate bg-tr-obsidian p-5 min-w-0">
              <div className="flex items-center gap-2 border-b border-tr-slate pb-3 mb-4">
                <span className="h-2.5 w-2.5 rounded-full bg-tr-slate" />
                <span className="h-2.5 w-2.5 rounded-full bg-tr-slate" />
                <span className="h-2.5 w-2.5 rounded-full bg-tr-steel" />
                <span className="ml-2 font-mono text-[11px] text-tr-dust">PowerShell — totalrecalls</span>
              </div>
              <div className="space-y-1.5 font-mono text-[12px] leading-[1.7]">
                {TERMINAL.map((l, i) => (
                  <div key={i} className={l.c === "dim" ? "text-tr-dust" : l.c === "amber" ? "text-tr-amber" : "text-tr-mist"}>
                    {l.t}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Container>
      </Section>

      {/* 3. The three steps */}
      <Section id="steps" className="border-t border-tr-slate bg-tr-graphite">
        <Container>
          <Eyebrow>The ownership path</Eyebrow>
          <h2 className="mt-3 max-w-[680px] font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
            Three steps from &ldquo;it&apos;s in the app&rdquo; to &ldquo;it&apos;s on my drive&rdquo;
          </h2>
          <div className="mt-10 grid gap-5 md:grid-cols-3">
            {STEPS.map((s) => (
              <div key={s.n} className="flex flex-col rounded-card border border-tr-slate bg-tr-obsidian p-6">
                <span className="font-mono text-[13px] text-tr-steel">{s.n}</span>
                <h3 className="mt-3 font-heading text-[18px] font-semibold text-tr-paper">{s.t}</h3>
                <p className="mt-3 flex-1 font-body text-[15px] leading-[1.6] text-tr-mist">{s.b}</p>
                <div className="mt-5 flex flex-wrap items-center gap-3 border-t border-tr-slate pt-4">
                  <span className="inline-flex items-center rounded-chip border border-tr-slate px-2 py-1 font-mono text-[11px] uppercase tracking-[0.06em] text-tr-dust">
                    {s.chip}
                  </span>
                  <a href={s.link.href} className="ml-auto inline-flex items-center gap-1.5 font-body text-[14px] font-semibold text-tr-steel transition-colors hover:text-tr-paper">
                    {s.link.label} <ArrowRight className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </Container>
      </Section>

      {/* 4. What providers give you vs what TotalRecalls gives you */}
      <Section id="compare" className="border-t border-tr-slate bg-tr-obsidian">
        <Container>
          <Eyebrow>Provider vs TotalRecalls</Eyebrow>
          <h2 className="mt-3 max-w-[680px] font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
            What each provider gives you &mdash; and what TotalRecalls gives you instead
          </h2>
          <p className="mt-4 max-w-[680px] font-body text-[16px] leading-[1.6] text-tr-mist">
            Most providers give you a view of your history, not the history itself. TotalRecalls
            gives you the files.
          </p>
          <div className="mt-10 overflow-x-auto rounded-card border border-tr-slate">
            <table className="w-full min-w-[640px] border-collapse text-left">
              <thead>
                <tr className="border-b border-tr-slate bg-tr-graphite font-mono text-[12px] uppercase tracking-[0.12em] text-tr-dust">
                  <th className="px-5 py-3.5 font-medium">Provider</th>
                  <th className="px-5 py-3.5 font-medium">What the provider gives you</th>
                  <th className="px-5 py-3.5 font-medium">What TotalRecalls gives you</th>
                </tr>
              </thead>
              <tbody className="font-body text-[15px]">
                {COMPARE.map((r) => (
                  <tr key={r.cap} className="border-b border-tr-slate last:border-b-0">
                    <td className="px-5 py-4 font-semibold text-tr-paper whitespace-nowrap">{r.cap}</td>
                    <td className="px-5 py-4 text-tr-dust">{r.o}</td>
                    <td className="px-5 py-4 text-tr-mist">{r.tr}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Container>
      </Section>

      {/* 5. Why it matters */}
      <Section id="why" className="border-t border-tr-slate bg-tr-graphite">
        <Container>
          <div className="max-w-[720px]">
            <Eyebrow>Why it matters</Eyebrow>
            <h2 className="mt-3 font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
              Your conversations are your record
            </h2>
            <div className="mt-6 space-y-5 font-body text-[16px] leading-[1.65] text-tr-mist">
              <p>
                The prompts you wrote, the drafts you iterated on, the research threads you built
                &mdash; that&apos;s a record of your work. Right now it only exists in whatever
                interface each provider ships today. If they redesign, merge, or retire a product,
                your history goes with it.
              </p>
              <p>
                Files don&apos;t care about product roadmaps. A Markdown file on your drive reads
                the same in ten years as it does today. TotalRecalls gives you that option, across
                eight providers, without making you learn eight different export menus.
              </p>
            </div>
            <div className="mt-8 flex flex-col sm:flex-row sm:items-center gap-4">
              <Btn href="/download/" large>Download free</Btn>
              <Btn href="/pricing/" variant="tertiary">Compare Free and Pro &rarr;</Btn>
            </div>
          </div>
        </Container>
      </Section>

      {/* 6. Final CTA band */}
      <Section className="border-t border-tr-slate bg-tr-obsidian">
        <Container>
          <div className="rounded-card border border-tr-slate bg-tr-graphite p-8 md:p-12 text-center">
            <h2 className="mx-auto max-w-[640px] font-heading text-[28px] md:text-[40px] font-bold leading-[1.1] tracking-[-0.02em] text-tr-paper">
              Bring your AI history home.
            </h2>
            <p className="mx-auto mt-4 max-w-[560px] font-body text-[16px] leading-[1.6] text-tr-mist">
              Free tier gets you started on ChatGPT, Claude, and Perplexity. Pro unlocks all eight
              providers and unlimited conversations, with a one-time payment.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row sm:items-center justify-center gap-4">
              <Btn href="/download/" large>Download free</Btn>
              <Btn href="/pricing/" variant="tertiary">See pricing &rarr;</Btn>
            </div>
            <p className="mt-6 font-body text-[14px] text-tr-dust">Windows 10 and 11. Your files stay on your drive.</p>
          </div>
        </Container>
      </Section>
    </div>
  );
}
