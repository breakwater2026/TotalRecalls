import DriveTree from "./DriveTree";
import { ArrowRight } from "lucide-react";

const STEPS = [
  { n: "01", t: "Buy once", d: "Checkout via Lemon Squeezy. One-time $24, no subscription." },
  { n: "02", t: "Install", d: "Unzip and run the Windows app. Local sign-in only." },
  { n: "03", t: "Pick a provider", d: "ChatGPT, Claude, Perplexity, Gemini, or Grok." },
  { n: "04", t: "Export", d: "Chats land as Markdown + JSON under your Library folder." },
];

export default function ResolutionPath() {
  return (
    <section id="resolution" className="border-t border-border">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-20 md:py-28">
        <header className="mb-12 max-w-2xl">
          <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Resolution Path · 01</span>
          <h2 className="font-heading text-3xl md:text-5xl font-bold tracking-tight mt-3">From concern to resolution in under a minute.</h2>
        </header>
        <div className="grid lg:grid-cols-[1fr_440px] gap-12">
          <div className="grid sm:grid-cols-2 gap-px bg-border border border-border">
            {STEPS.map((s) => (
              <div key={s.n} className="bg-card p-6">
                <span className="font-mono text-[11px] text-primary tracking-[0.16em]">STEP {s.n}</span>
                <h3 className="font-heading text-2xl font-semibold mt-3">{s.t}</h3>
                <p className="font-body text-muted-foreground text-[14px] leading-relaxed mt-2">{s.d}</p>
              </div>
            ))}
          </div>
          <div className="lg:sticky lg:top-24 h-fit">
            <div className="border border-border bg-card">
              <DriveTree />
              <div className="p-6">
                <span className="font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground">Action Command Center</span>
                <p className="font-heading text-xl font-semibold mt-2">Local storage. Your drive. Your files.</p>
                <a href="#pricing" className="mt-5 w-full inline-flex items-center justify-center gap-2 bg-primary text-white px-5 py-3.5 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:opacity-90 transition-opacity">
                  Begin Resolution <ArrowRight className="w-4 h-4" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
