import ConvergenceDiagram from "./ConvergenceDiagram";
import { ArrowRight, Download, ShieldCheck, Lock, Database } from "lucide-react";

const TRUST = [
  { Icon: Lock, l: "Private by design", s: "Local sign-in · no cloud" },
  { Icon: Database, l: "One library", s: "Every ai provider, one local folder" },
  { Icon: ShieldCheck, l: "Yours forever", s: "" },
];

export default function SentinelHero() {
  return (
    <section id="top" className="relative border-b border-border overflow-hidden">
      <div className="absolute inset-0 tr-grid-bg opacity-60 pointer-events-none" />
      <div className="relative mx-auto max-w-[1400px] px-5 md:px-10 pt-16 md:pt-24 pb-20 md:pb-28">
        <div className="grid lg:grid-cols-[1.1fr_0.9fr] gap-12 lg:gap-16 items-center">
          <div>
            <span className="inline-flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.18em] text-primary border border-primary/30 px-3 py-1.5">
              <ShieldCheck className="w-3.5 h-3.5" /> Forensic Guardian · v1.0
            </span>
            <h1 className="font-heading text-[44px] md:text-[68px] leading-[0.98] font-bold tracking-tight mt-6">
              Recall every AI conversation.
            </h1>
            <p className="font-body text-muted-foreground text-[16px] md:text-[18px] leading-relaxed mt-6 max-w-xl">
              A Windows app that exports your ChatGPT, Claude, Perplexity, Gemini, and Grok chats into a private folder of Markdown + JSON you keep forever — long after the tab closes and the UI changes.
            </p>

            <div className="mt-9 flex flex-col sm:flex-row gap-3">
              <a href="#pricing" data-tr-buy className="inline-flex items-center justify-center gap-2 bg-primary text-white px-6 py-3.5 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:opacity-90 transition-opacity">
                Buy TotalRecalls — $24USD <ArrowRight className="w-4 h-4" />
              </a>
              <a href="#pricing" data-tr-download className="inline-flex items-center justify-center gap-2 border border-border px-6 py-3.5 font-mono text-[12px] uppercase tracking-[0.14em] hover:bg-muted transition-colors">
                <Download className="w-4 h-4" /> Download ZIP
              </a>
            </div>
            <p className="font-mono text-[11px] uppercase tracking-[0.16em] text-primary mt-2.5 font-medium">
              discounted launch price · one-time
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
