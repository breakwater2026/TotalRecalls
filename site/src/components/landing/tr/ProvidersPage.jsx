import React from "react";
import { Plus, ArrowRight } from "lucide-react";
import { Container, Section, Eyebrow, Btn, EvidenceStrip, LocalChip } from "./ui";

/* ============================================================================
 * /providers/ — "Supported AI Providers" (Jasper rewrite, tr/ design system).
 * Copy + spec from: Marketing/Jasper/Website Rewrite/TotalRecalls AI Providers Page.md
 * ========================================================================== */

const ROWS = [
  { name: "ChatGPT", id: "OAI-001", direct: true, tier: "free" },
  { name: "Claude", id: "ANT-002", direct: true, tier: "free" },
  { name: "Perplexity", id: "PPL-003", direct: true, tier: "free" },
  { name: "Gemini", id: "GEM-004", direct: false, tier: "pro" },
  { name: "Grok", id: "GRK-005", direct: true, tier: "pro" },
  { name: "DeepSeek", id: "DSK-006", direct: true, tier: "pro" },
  { name: "Mistral", id: "MST-007", direct: true, tier: "pro" },
  { name: "Qwen", id: "QWN-008", direct: true, tier: "pro" },
];

function TierChip({ tier }) {
  if (tier === "free") {
    return (
      <span className="inline-flex items-center rounded-chip bg-tr-slate px-2 py-1 font-mono text-[12px] font-medium uppercase tracking-[0.02em] text-tr-mist">
        Free + Pro
      </span>
    );
  }
  return (
    <span className="inline-flex items-center rounded-chip bg-tr-amber/12 px-2 py-1 font-mono text-[12px] font-medium uppercase tracking-[0.02em] text-tr-amber">
      Pro
    </span>
  );
}

function MethodChip({ direct }) {
  if (direct) {
    return (
      <span className="inline-flex items-center rounded-chip border border-tr-slate px-2 py-1 font-mono text-[12px] font-medium uppercase tracking-[0.02em] text-tr-steel">
        Direct
      </span>
    );
  }
  return (
    <span className="inline-flex items-center rounded-chip border border-dashed border-tr-slate px-2 py-1 font-mono text-[12px] font-medium uppercase tracking-[0.02em] text-tr-dust">
      Takeout &rarr; MD
    </span>
  );
}

const DETAIL = [
  {
    name: "ChatGPT",
    id: "OAI-001",
    direct: true,
    tier: "free",
    body: "Your ChatGPT conversations save as dated, readable files instead of one hard-to-browse export bundle. Long threads stay together in a single file, ready for any text editor.",
    folder: "Library\\chatgpt\\",
    guide: "/guides/export-chatgpt-conversations/",
    guideLabel: "ChatGPT guide",
  },
  {
    name: "Claude",
    id: "ANT-002",
    direct: true,
    tier: "free",
    body: "Long Claude threads and Project conversations save as files you can reread without scrolling. Your drafts, plans, and code reviews sit in one folder, sorted by date.",
    folder: "Library\\claude\\",
    guide: "/guides/export-claude-chat-history/",
    guideLabel: "Claude guide",
  },
  {
    name: "Perplexity",
    id: "PPL-003",
    direct: true,
    tier: "free",
    body: "Perplexity research threads save before the tab trail disappears. Each thread keeps your questions and answers together, so you can pick up the research where you left off.",
    folder: "Library\\perplexity\\",
    guide: "/guides/backup-perplexity-threads/",
    guideLabel: "Perplexity guide",
  },
  {
    name: "Gemini",
    id: "GEM-004",
    direct: false,
    tier: "pro",
    body: "Gemini isn't a direct download. Your history comes from a Google Takeout archive, which TotalRecalls converts into Markdown conversations. Once converted, your Gemini chats sit in the same Library as every other provider.",
    folder: "Library\\gemini\\",
    guide: "/guides/gemini-takeout-archive/",
    guideLabel: "Gemini Takeout guide",
  },
  {
    name: "Grok",
    id: "GRK-005",
    direct: true,
    tier: "pro",
    body: "Grok chats from xAI save as local Markdown and JSON, including references to X posts that appear in your conversations. Quick prompts and long debug sessions both get kept.",
    folder: "Library\\grok\\",
    guide: "/guides/grok/",
    guideLabel: "Grok guide",
  },
  {
    name: "DeepSeek",
    id: "DSK-006",
    direct: true,
    tier: "pro",
    body: "DeepSeek conversations save with R1 thinking traces included, so you keep the reasoning, not just the final answer. Useful when you want to see how a result was reached.",
    folder: "Library\\deepseek\\",
    guide: "/guides/deepseek/",
    guideLabel: "DeepSeek guide",
  },
  {
    name: "Mistral",
    id: "MST-007",
    direct: true,
    tier: "pro",
    body: "Le Chat conversations save with UTF-8 fidelity, so accents and non-English text come through intact. That makes it a good fit for multilingual research and translation work.",
    folder: "Library\\mistral\\",
    guide: "/guides/mistral/",
    guideLabel: "Mistral guide",
  },
  {
    name: "Qwen",
    id: "QWN-008",
    direct: true,
    tier: "pro",
    body: "Your Qwen Chat history from chat.qwen.ai saves as local files, with multilingual text preserved. TotalRecalls works with the consumer chat app, never the DashScope developer API.",
    folder: "Library\\qwen\\",
    guide: "/guides/qwen/",
    guideLabel: "Qwen guide",
  },
];

const FAQS = [
  {
    q: "Does it matter which AI model I chatted with?",
    a: "No. TotalRecalls saves conversations from your chat history in each provider, whichever model you used in them.",
  },
  {
    q: "Does TotalRecalls use my API keys?",
    a: "No. It saves the chats in your consumer account, the same ones you see in each provider's app. You sign in locally, inside TotalRecalls.",
  },
  {
    q: "Why does Gemini take extra steps?",
    a: "Google makes Gemini history available through Takeout rather than a direct route. TotalRecalls converts that archive for you, so the result matches every other provider.",
  },
  {
    q: "What happens if a provider changes its interface?",
    a: "Your saved files don't change. They're plain Markdown and JSON on your drive. If a provider change affects new downloads, we fix it in an app update.",
  },
  {
    q: "Can I request a provider?",
    a: "Yes. Email support@totalrecalls.app and tell us which one you use.",
  },
];

function AccessTable() {
  return (
    <div className="overflow-x-auto rounded-card border border-tr-slate bg-tr-obsidian">
      <table className="w-full border-collapse text-left">
        <thead>
          <tr className="border-b border-tr-slate font-mono text-[12px] uppercase tracking-[0.12em] text-tr-dust">
            <th className="px-4 py-3 font-medium"> </th>
            <th className="px-4 py-3 font-medium">Free Tier</th>
            <th className="px-4 py-3 font-medium">Pro</th>
          </tr>
        </thead>
        <tbody className="font-body text-[14px] text-tr-mist">
          <tr className="border-b border-tr-slate">
            <td className="px-4 py-3 font-semibold text-tr-paper">Providers</td>
            <td className="px-4 py-3">ChatGPT, Claude, Perplexity</td>
            <td className="px-4 py-3">All 8</td>
          </tr>
          <tr className="border-b border-tr-slate">
            <td className="px-4 py-3 font-semibold text-tr-paper">Conversations</td>
            <td className="px-4 py-3">5 per provider</td>
            <td className="px-4 py-3">Unlimited</td>
          </tr>
          <tr className="border-b border-tr-slate">
            <td className="px-4 py-3 font-semibold text-tr-paper">Gemini (Takeout &rarr; Markdown)</td>
            <td className="px-4 py-3 text-tr-dust">&mdash;</td>
            <td className="px-4 py-3 text-tr-green">&check;</td>
          </tr>
          <tr>
            <td className="px-4 py-3 font-semibold text-tr-paper">Price</td>
            <td className="px-4 py-3">$0</td>
            <td className="px-4 py-3">$24 one-time (launch price)</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default function ProvidersPage() {
  return (
    <div>
      {/* 1. Hero */}
      <div className="bg-tr-obsidian pt-16 pb-16 md:pt-32 md:pb-24">
        <Container>
          <div className="max-w-[680px]">
            <Eyebrow mono>Supported providers &middot; V1.0.0</Eyebrow>
            <h1 className="mt-3 font-heading text-[34px] md:text-[48px] font-bold leading-[1.1] tracking-[-0.02em] text-tr-paper">
              Download your AI chat history from eight providers.
            </h1>
            <p className="mt-6 font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-mist">
              TotalRecalls saves your conversations from ChatGPT, Claude, Perplexity, Gemini, Grok,
              DeepSeek, Mistral, and Qwen into one folder on your Windows PC. Each chat becomes a
              Markdown file and a JSON file you can open, search, and keep.
            </p>
            <p className="mt-4 font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-mist">
              Seven providers download directly. Gemini comes through Google Takeout, which
              TotalRecalls converts for you.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row sm:items-center gap-4">
              <Btn href="/download/" large>Download free</Btn>
              <Btn href="#providers" variant="tertiary">Find your provider &darr;</Btn>
            </div>
            <div className="mt-8 flex flex-wrap gap-2">
              {["8 providers", "7 direct · 1 takeout", ".md + .json", "windows 10/11"].map((c) => (
                <span key={c} className="inline-flex whitespace-nowrap rounded-chip bg-tr-slate px-2 py-1 font-mono text-[12px] font-medium uppercase tracking-[0.02em] text-tr-dust">
                  {c}
                </span>
              ))}
            </div>
          </div>
        </Container>
      </div>

      {/* 2. Evidence strip */}
      <EvidenceStrip path="C:\TotalRecalls\Library\{provider}\{YYYY-MM-DD}-{HHMM}-{title}.md" chips={<LocalChip />} />

      {/* 3. Provider index */}
      <Section id="index" className="border-t border-tr-slate bg-tr-obsidian">
        <Container>
          <Eyebrow>At a glance</Eyebrow>
          <h2 className="mt-3 max-w-[680px] font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
            Every supported AI provider, in one list
          </h2>
          <p className="mt-4 max-w-[680px] font-body text-[16px] leading-[1.6] text-tr-mist">
            Find your provider, see how its chats reach your Library, and check which tier includes it.
          </p>

          <div className="mt-10 rounded-card border border-tr-slate bg-tr-graphite p-2 md:p-0 md:overflow-hidden">
            {/* Desktop header */}
            <div className="hidden md:grid md:grid-cols-[1.1fr_0.9fr_1.5fr_1fr_1fr] gap-4 border-b border-tr-slate px-6 py-3 font-mono text-[12px] uppercase tracking-[0.12em] text-tr-dust">
              <span>Provider</span><span>ID</span><span>Method</span><span>Saved as</span><span>Tier</span>
            </div>
            {ROWS.map((p) => (
              <div
                key={p.id}
                className={`grid grid-cols-1 gap-2 border-b border-tr-slate px-4 py-4 md:grid-cols-[1.1fr_0.9fr_1.5fr_1fr_1fr] md:gap-4 md:px-6 ${
                  !p.direct ? "border-l-2 border-l-dashed border-l-tr-steel bg-tr-obsidian/40" : ""
                }`}
              >
                <span className="font-body text-[15px] font-medium text-tr-paper">{p.name}</span>
                <code className="font-mono text-[12px] text-tr-steel">{p.id}</code>
                <span className="font-body text-[14px] text-tr-mist">{p.direct ? "Direct download" : "Google Takeout → Markdown"}</span>
                <span className="font-mono text-[13px] text-tr-steel">.md + .json</span>
                <span><TierChip tier={p.tier} /></span>
              </div>
            ))}
          </div>

          <p className="mt-6 font-body text-[15px] leading-[1.6] text-tr-mist">
            Every row lands in the same place:{" "}
            <code className="font-mono text-[13px] text-tr-steel select-all">C:\\TotalRecalls\\Library\\</code>,
            with one subfolder per provider.
          </p>
        </Container>
      </Section>

      {/* 3. Two ways in */}
      <Section className="border-t border-tr-slate bg-tr-obsidian">
        <Container>
          <Eyebrow>How chats reach your Library</Eyebrow>
          <h2 className="mt-3 max-w-[680px] font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
            Direct download or Google Takeout: what&apos;s the difference?
          </h2>
          <p className="mt-4 max-w-[680px] font-body text-[16px] leading-[1.6] text-tr-mist">
            Most providers take a pick and a click. One takes a short detour through Google.
          </p>

          <div className="mt-10 grid md:grid-cols-2 gap-6">
            <div className="rounded-card border border-tr-slate bg-tr-graphite p-6">
              <div className="flex items-center justify-between gap-3">
                <h4 className="font-heading text-[18px] font-semibold text-tr-paper">Direct download</h4>
                <span className="inline-flex items-center rounded-chip border border-tr-slate px-2 py-1 font-mono text-[12px] uppercase tracking-[0.02em] text-tr-steel">7 providers</span>
              </div>
              <p className="mt-4 font-body text-[16px] leading-[1.6] text-tr-mist">
                You sign in to the provider locally, inside the app. Pick it, click download, and your
                chats land in your Library folder. TotalRecalls handles the rest.
              </p>
              <div className="mt-5">
                <MethodChip direct={true} />
              </div>
            </div>

            <div className="rounded-card border border-dashed border-tr-slate bg-tr-graphite p-6">
              <div className="flex items-center justify-between gap-3">
                <h4 className="font-heading text-[18px] font-semibold text-tr-paper">Google Takeout</h4>
                <span className="inline-flex items-center rounded-chip border border-dashed border-tr-slate px-2 py-1 font-mono text-[12px] uppercase tracking-[0.02em] text-tr-dust">Gemini only</span>
              </div>
              <p className="mt-4 font-body text-[16px] leading-[1.6] text-tr-mist">
                Google doesn&apos;t offer a direct route for Gemini history. You request a Takeout
                archive from Google, extract the ZIP, and point TotalRecalls to the folder. It converts
                your chats to Markdown and saves them next to everything else.
              </p>
              <div className="mt-5">
                <MethodChip direct={false} />
              </div>
            </div>
          </div>

          <p className="mt-8 max-w-[680px] font-body text-[16px] leading-[1.6] text-tr-mist">
            Both paths end the same way: plain files on your own drive, not sent to our servers.
          </p>
        </Container>
      </Section>

      {/* 4. Provider by provider */}
      <Section id="providers" className="border-t border-tr-slate bg-tr-obsidian">
        <Container>
          <Eyebrow>What gets saved</Eyebrow>
          <h2 className="mt-3 max-w-[680px] font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
            What TotalRecalls saves from each provider
          </h2>
          <p className="mt-4 max-w-[680px] font-body text-[16px] leading-[1.6] text-tr-mist">
            Every conversation becomes one Markdown file for reading and one JSON file for structure.
            Here&apos;s what that looks like for each provider.
          </p>

          <div className="mt-10 grid gap-5 md:grid-cols-2">
            {DETAIL.map((d) => (
              <div key={d.id} className="flex flex-col rounded-card border border-tr-slate bg-tr-graphite p-6">
                <div className="flex flex-wrap items-center gap-2">
                  <h4 className="mr-auto font-heading text-[18px] font-semibold text-tr-paper">{d.name}</h4>
                </div>
                <div className="mt-2 flex flex-wrap items-center gap-2">
                  <code className="font-mono text-[12px] text-tr-steel">{d.id}</code>
                  <MethodChip direct={d.direct} />
                  <TierChip tier={d.tier} />
                </div>
                <p className="mt-4 flex-1 font-body text-[16px] leading-[1.6] text-tr-mist">{d.body}</p>
                <div className="mt-5 flex flex-wrap items-center gap-x-3 gap-y-2 border-t border-tr-slate pt-4">
                  <code className="font-mono text-[13px] text-tr-steel select-all">{d.folder}</code>
                  <a href={d.guide} className="ml-auto inline-flex items-center gap-1.5 font-body text-[14px] font-semibold text-tr-steel transition-colors hover:text-tr-paper">
                    {d.guideLabel} <ArrowRight className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </Container>
      </Section>

      {/* 5. In development */}
      <Section className="border-t border-tr-slate bg-tr-obsidian">
        <Container>
          <Eyebrow>What&apos;s next</Eyebrow>
          <h2 className="mt-3 max-w-[680px] font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
            More providers in development
          </h2>
          <div className="mt-8 grid gap-6 md:grid-cols-[1.4fr_1fr] md:items-center">
            <p className="max-w-[560px] font-body text-[16px] leading-[1.6] text-tr-mist">
              We&apos;re building support for more AI providers and new capabilities. We&apos;ll list
              them here when they&apos;re ready, not before. New providers arrive through app updates.
              Pro includes free updates to the core app for the life of the product.
            </p>
            <div className="flex items-center justify-center rounded-card border border-dashed border-tr-slate bg-tr-graphite px-6 py-12">
              <span className="inline-flex items-center gap-3 font-mono text-[13px] uppercase tracking-[0.12em] text-tr-dust">
                <Plus className="h-4 w-4" /> More providers in development
              </span>
            </div>
          </div>
        </Container>
      </Section>

      {/* 6. FAQ */}
      <Section className="border-t border-tr-slate bg-tr-obsidian">
        <Container>
          <div className="grid lg:grid-cols-[1fr_1.6fr] gap-12 items-start">
            <div>
              <Eyebrow>FAQ</Eyebrow>
              <h2 className="mt-3 font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
                Questions about providers and models
              </h2>
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

      {/* 7. Access summary + final CTA */}
      <Section id="access" className="border-t border-tr-slate bg-tr-graphite">
        <Container>
          <div className="grid lg:grid-cols-[1fr_1fr] gap-12 items-start">
            <div>
              <Eyebrow>Free and Pro</Eyebrow>
              <h2 className="mt-3 font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
                Start with three providers. Unlock all eight with one payment.
              </h2>
              <p className="mt-4 max-w-md font-body text-[16px] leading-[1.6] text-tr-mist">
                Try TotalRecalls on your own ChatGPT, Claude, and Perplexity chats first. When you want
                every provider and no download cap, Pro is one payment with no subscription.
              </p>
              <div className="mt-8 flex flex-col sm:flex-row sm:items-center gap-4">
                <Btn href="/download/" large>Download free</Btn>
                <Btn href="/pricing/" variant="tertiary">Compare Free and Pro &rarr;</Btn>
              </div>
              <p className="mt-6 hidden sm:block font-body text-[14px] leading-[1.5] text-tr-dust">
                Windows 10 and 11.
              </p>
              <p className="mt-6 sm:hidden font-body text-[14px] leading-[1.5] text-tr-dust">
                Windows 10 and 11. Visiting on mobile? Open totalrecalls.app on your desktop to download.
              </p>
            </div>
            <div>
              <AccessTable />
            </div>
          </div>
        </Container>
      </Section>
    </div>
  );
}
