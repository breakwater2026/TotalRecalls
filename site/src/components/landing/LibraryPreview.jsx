import { Folder, FileText } from "lucide-react";

const PROVIDERS = ["Library", "ChatGPT", "Claude", "Perplexity", "Gemini", "Grok", "DeepSeek", "Mistral", "Qwen Chat"];
const FILES = [
  { path: "chatgpt/2026-08-01-pricing-research.md", occurred: "2026-08-01 09:14" },
  { path: "claude/2026-07-28-refactor-plan.md", occurred: "2026-07-28 22:41" },
  { path: "perplexity/2026-07-21-market-scan.md", occurred: "2026-07-21 14:07" },
  { path: "gemini/2026-07-14-takeout-thread.md", occurred: "2026-07-14 18:52" },
  { path: "grok/2026-07-02-debug-session.md", occurred: "2026-07-02 11:30" },
  { path: "deepseek/2026-08-15-r1-thinking-trace.md", occurred: "2026-08-15 16:23" },
  { path: "mistral/2026-08-12-le-chat-translation.md", occurred: "2026-08-12 11:48" },
  { path: "qwen/2026-08-14-qwen-multilingual-thread.md", occurred: "2026-08-14 09:02" },
];

export default function LibraryPreview() {
  return (
    <section id="library" className="border-t border-border tr-grid-bg">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-20 md:py-28">
        <header className="mb-12 max-w-3xl">
          <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Library</span>
          <h2 className="font-heading text-3xl md:text-5xl font-bold tracking-tight mt-3">Your library, organized.</h2>
          <p className="font-body text-muted-foreground text-[15px] leading-relaxed mt-4">
            Clean folder structure you can browse, search, and back up.
          </p>
          <p className="font-body text-muted-foreground text-[15px] leading-relaxed mt-4">
            Predictable formatting (.MD and .JSON formats) giving you the full flexibility to work with on <span className="whitespace-nowrap">your own tools.</span>
          </p>
        </header>
        <div className="grid lg:grid-cols-2 gap-px bg-border border border-border">
          <div className="bg-card">
            <div className="flex items-center gap-2 px-4 h-9 border-b border-border bg-muted/40">
              <span className="w-2.5 h-2.5 rounded-full bg-border" />
              <span className="w-2.5 h-2.5 rounded-full bg-border" />
              <span className="w-2.5 h-2.5 rounded-full bg-border" />
              <span className="ml-3 font-mono text-[11px] text-muted-foreground">TotalRecalls — Library</span>
            </div>
            <div className="grid grid-cols-[140px_1fr]">
              <div className="border-r border-border py-3">
                {PROVIDERS.map((p, i) => (
                  <div key={p} className={`px-4 py-1.5 font-mono text-[11px] flex items-center gap-2 ${i === 0 ? "text-foreground font-medium" : "text-muted-foreground"}`}>
                    <Folder className="w-3.5 h-3.5" /> {p}
                  </div>
                ))}
              </div>
              <div className="py-3">
                {FILES.map((f) => (
                  <div key={f.path} className="px-4 py-2 flex items-center justify-between hover:bg-muted/40">
                    <span className="font-mono text-[11px] truncate"><FileText className="w-3.5 h-3.5 inline mr-2 text-muted-foreground" />{f.path}</span>
                    <span className="font-mono text-[10px] text-muted-foreground shrink-0 ml-3">{f.occurred}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="bg-card">
            <div className="flex items-center px-4 h-9 border-b border-border bg-muted/40">
              <span className="font-mono text-[11px] text-muted-foreground">2026-08-01-pricing-research.md</span>
            </div>
            <div className="p-6 font-mono text-[12px] leading-relaxed space-y-3">
              <p className="font-heading text-foreground text-lg"># Pricing research</p>
              <p className="text-muted-foreground">exported 2026-08-01 · provider: chatgpt · 14 messages</p>
              <div className="border-l-2 border-primary pl-3">
                <p className="text-foreground"><span className="text-primary">You:</span> Compare one-time pricing for export tools.</p>
              </div>
              <div className="border-l-2 border-border pl-3">
                <p className="text-foreground/80"><span className="text-muted-foreground">Assistant:</span> Here is a table of the options I found, with links and caveats…</p>
              </div>
              <p className="text-muted-foreground text-[11px]">+ attachments: sources.json</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
