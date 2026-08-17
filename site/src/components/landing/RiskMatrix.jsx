import { ShieldCheck, ArrowUpRight } from "lucide-react";

const PROVIDERS = [
  { name: "ChatGPT", code: "OAI-001", status: "Direct Export", grade: "SECURED", count: "284 files", paths: ["chatgpt/2026-08-01-pricing-research.md", "chatgpt/2026-07-19-architecture-review.md", "chatgpt/2026-06-30-refactor-debug.md"] },
  { name: "Claude", code: "ANT-002", status: "Direct Export", grade: "SECURED", count: "312 files", paths: ["claude/2026-07-28-refactor-plan.md", "claude/2026-07-02-legal-draft.md", "claude/2026-05-11-research-thread.md"] },
  { name: "Perplexity", code: "PPL-003", status: "Direct Export", grade: "SECURED", count: "96 files", paths: ["perplexity/2026-07-21-market-scan.md", "perplexity/2026-06-04-source-trail.md"] },
  { name: "Gemini", code: "GEM-004", status: "Takeout → Markdown", grade: "CONVERTED", count: "47 files", paths: ["gemini/2026-07-14-takeout-thread.md", "gemini/2026-03-22-takeout-dump.md"] },
  { name: "Grok", code: "GRK-005", status: "Direct Export", grade: "SECURED", count: "58 files", paths: ["grok/2026-07-02-debug-session.md", "grok/2026-06-18-quick-prompts.md"] },
];

export default function RiskMatrix() {
  return (
    <section id="matrix" className="border-t border-border">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-20 md:py-28">
        <header className="flex flex-col md:flex-row md:items-end md:justify-between gap-6 mb-12">
          <div>
            <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Current AI Models Providers · 02</span>
            <h2 className="font-heading text-3xl md:text-5xl font-bold tracking-tight mt-3">Five AI providers. All in one library on your computer. Instant Relief.</h2>
          </div>

        </header>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-px bg-border border border-border max-h-[70vh] overflow-y-auto">
          {PROVIDERS.map((p) => (
            <div key={p.name} className="group relative bg-card border-l-2 border-primary overflow-hidden min-h-[220px]">
              <div className="p-6 transition-opacity duration-200 group-hover:opacity-0">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-[10px] tracking-[0.16em] text-muted-foreground">{p.code}</span>
                  <span className={`font-mono text-[9px] uppercase tracking-[0.18em] px-2 py-1 ${p.grade === "SECURED" ? "bg-primary/10 text-primary" : "bg-muted text-muted-foreground"}`}>{p.grade}</span>
                </div>
                <h3 className="font-heading text-3xl font-bold mt-6">{p.name}</h3>
                <p className="font-mono text-[12px] text-muted-foreground mt-2">{p.status}</p>
                <div className="mt-8 flex items-center justify-between">
                  <span className="font-mono text-[12px]">{p.count}</span>
                  <ArrowUpRight className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
                </div>
              </div>
              <div className="absolute inset-0 p-6 bg-card opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex flex-col">
                <div className="flex items-center gap-2 mb-4">
                  <ShieldCheck className="w-4 h-4 text-primary" />
                  <span className="font-mono text-[10px] uppercase tracking-[0.16em] text-primary">Forensic View · {p.code}</span>
                </div>
                <div className="flex-1 flex flex-col justify-center gap-1.5">
                  {p.paths.map((path) => (
                    <div key={path} className="font-mono text-[11px] text-foreground/80 truncate">
                      <span className="text-muted-foreground">▍</span> {path}
                    </div>
                  ))}
                </div>
                <span className="font-mono text-[10px] text-muted-foreground mt-3">Library/{p.name.toLowerCase()}/</span>
              </div>
            </div>
          ))}
          <div className="bg-card border-l-2 border-primary p-6 flex flex-col items-center justify-center text-center">
            <p className="font-heading text-2xl font-semibold leading-tight">many more to come</p>
          </div>
        </div>
      </div>
    </section>
  );
}
