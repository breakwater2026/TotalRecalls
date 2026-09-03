import ConvergenceDiagram from "./ConvergenceDiagram";
import { LOGOS, PROVIDER_COLORS } from "./RiskMatrix";
import { ArrowRight, ShieldCheck, Lock, Database } from "lucide-react";

const TRUST = [
  { Icon: Lock, l: "Private by design", s: "Local sign-in · no cloud" },
  { Icon: Database, l: "One library", s: "Every AI provider, one local folder" },
  { Icon: ShieldCheck, l: "Yours forever", s: "" },
];

const PROVIDERS = [
  { name: "ChatGPT", logo: "ChatGPT" },
  { name: "Claude", logo: "Claude" },
  { name: "Perplexity", logo: "Perplexity" },
  { name: "Gemini", logo: "Gemini" },
  { name: "Grok", logo: "Grok" },
  { name: "DeepSeek", logo: "DeepSeek" },
  { name: "Mistral", logo: "Mistral" },
  { name: "Qwen Chat", logo: "Qwen" },
];

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
              A Windows app that downloads your ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen chats into a private folder of Markdown + JSON you keep forever — long after the tab closes and the UI changes.
            </p>

            <div className="mt-5 grid grid-cols-2 sm:grid-cols-4 gap-2">
              {PROVIDERS.map((p) => (
                <span
                  key={p.name}
                  className="inline-flex items-center justify-center gap-1.5 font-mono text-[10px] uppercase tracking-[0.12em] border rounded-sm px-2.5 py-1"
                  style={{ color: PROVIDER_COLORS[p.logo], borderColor: PROVIDER_COLORS[p.logo] }}
                >
                  <svg
                    role="img"
                    aria-label={`${p.name} logo`}
                    viewBox={LOGOS[p.logo].vb}
                    className="h-3 w-3 shrink-0"
                    fill="currentColor"
                    preserveAspectRatio="xMidYMid meet"
                  >
                    <path d={LOGOS[p.logo].d} />
                  </svg>
                  {p.name}
                </span>
              ))}
            </div>

            <div className="mt-9 flex flex-col sm:flex-row gap-3">
              <a href="/buy/" data-tr-buy="true" aria-label="Buy TotalRecalls — $24 USD — discounted launch price" className="inline-flex flex-col items-center justify-center gap-0.5 bg-primary text-white px-6 py-3 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:opacity-90 transition-opacity w-full sm:w-auto" style={{ maxWidth: 300 }}>
                <span className="whitespace-nowrap">Buy TotalRecalls — $24 USD</span>
                <span className="text-[10px] font-normal opacity-85 tracking-[0.12em] whitespace-nowrap">discounted launch price</span>
              </a>
              <a href="#resolution" className="inline-flex items-center justify-center gap-2 border border-border bg-card text-foreground px-6 py-3.5 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:bg-muted/50 transition-colors">
                See how it works
              </a>
            </div>
            <p className="font-mono text-[11px] uppercase tracking-[0.18em] text-muted-foreground mt-3">
              Try the Free Tier today · One-time $24 · No subscription
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
