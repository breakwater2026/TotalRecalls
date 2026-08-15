import { useState } from "react";
import ConvergenceDiagram from "@/components/landing/ConvergenceDiagram";
import { ArrowRight, Download, ShieldCheck, Lock, Database, ScanLine } from "lucide-react";

const TRUST = [
  { Icon: Lock, l: "Private by design", s: "Local sign-in · no cloud" },
  { Icon: Database, l: "One library", s: "Every assistant, one folder" },
  { Icon: ShieldCheck, l: "Yours forever", s: "Markdown opens in 10 yrs" },
];

export default function SentinelHero() {
  const [q, setQ] = useState("");
  const [result, setResult] = useState(null);
  const scan = (e) => {
    e.preventDefault();
    setResult("scan");
    setTimeout(() => setResult("clear"), 1400);
  };

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

            <form onSubmit={scan} className="mt-9 border border-border bg-card">
              <div className="flex items-center">
                <span className="font-mono text-[11px] text-muted-foreground pl-4 pr-2">▍</span>
                <input
                  value={q}
                  onChange={(e) => setQ(e.target.value)}
                  placeholder="Verify a conversation is safe — thread, date, or provider…"
                  className="flex-1 bg-transparent font-mono text-[13px] py-4 outline-none placeholder:text-muted-foreground/70 min-w-0"
                />
                <button type="submit" className="m-1 inline-flex items-center gap-2 bg-foreground text-background px-4 py-2.5 font-mono text-[11px] uppercase tracking-[0.14em] hover:bg-primary hover:text-white transition-colors shrink-0">
                  <ScanLine className="w-3.5 h-3.5" /> Scan
                </button>
              </div>
            </form>
            <div className="h-6 mt-2 font-mono text-[11px]">
              {result === "scan" && <span className="text-primary">▍ Scanning library…</span>}
              {result === "clear" && <span className="text-primary">✓ Scan complete · 0 active threats · library secure</span>}
            </div>

            <div className="mt-7 flex flex-col sm:flex-row gap-3">
              <a href="#pricing" className="inline-flex items-center justify-center gap-2 bg-primary text-white px-6 py-3.5 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:opacity-90 transition-opacity">
                Buy TotalRecalls — $24 <ArrowRight className="w-4 h-4" />
              </a>
              <a href="#pricing" className="inline-flex items-center justify-center gap-2 border border-border px-6 py-3.5 font-mono text-[12px] uppercase tracking-[0.14em] hover:bg-muted transition-colors">
                <Download className="w-4 h-4" /> Download ZIP
              </a>
            </div>

            <div className="mt-10 grid grid-cols-3 gap-6 border-t border-border pt-6">
              {TRUST.map((x) => (
                <div key={x.l}>
                  <x.Icon className="w-4 h-4 text-primary" />
                  <p className="font-heading text-[14px] font-semibold mt-2">{x.l}</p>
                  <p className="font-mono text-[10px] text-muted-foreground mt-0.5">{x.s}</p>
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