import { ArrowUpRight } from "lucide-react";

const GUIDES = [
  { 
    t: "Export ChatGPT conversations", 
    d: "Official export vs a local library you can actually use", 
    tag: "guide · 01",
    href: "/guides/export-chatgpt-conversations/",
    bullets: ["Why HTML bundles are hard to browse", "How TotalRecalls creates Markdown", "Folder structure examples", "Troubleshooting"]
  },
  { 
    t: "Download your Claude history", 
    d: "Keep Projects and long threads as files", 
    tag: "guide · 02",
    href: "/guides/export-claude-chat-history/",
    bullets: ["Projects vs conversations", "Markdown + JSON output", "Handling long threads", "Folder structure"]
  },
  { 
    t: "Backup Perplexity threads", 
    d: "Save research threads before you lose the tab trail", 
    tag: "guide · 03",
    href: "/guides/backup-perplexity-threads/",
    bullets: ["Why Perplexity history expires", "How TotalRecalls extracts threads", "Research workflows", "Troubleshooting"]
  },
  { 
    t: "Gemini Takeout → Markdown", 
    d: "Turn Google Takeout dumps into Markdown conversations", 
    tag: "guide · 04",
    href: "/guides/gemini-takeout-archive/",
    bullets: ["How to request a Takeout", "Extracting the ZIP", "Pointing TotalRecalls to folder", "JSON → Markdown conversion", "Troubleshooting"]
  },
  { 
    t: "Own your AI chat data", 
    d: "Why multi-assistant export matters in 2026", 
    tag: "guide · 05",
    href: "/guides/own-your-ai-chat-data/",
    bullets: ["Switching providers", "Cross-assistant research", "Unified library", "Long-term durability"]
  },
];

export default function Guides() {
  return (
    <section id="guides" className="border-t border-border">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-20 md:py-28">
        <header className="mb-10 flex flex-col md:flex-row md:items-end md:justify-between gap-6">
          <div>
            <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Guides · 04</span>
            <h2 className="font-heading text-3xl md:text-5xl font-bold tracking-tight mt-3">Reading.</h2>
          </div>
          <p className="font-mono text-[11px] text-muted-foreground uppercase tracking-[0.14em]">No email gate · No AdSense</p>
        </header>
        <div className="border-t border-border">
          {GUIDES.map((g) => (
            <a key={g.t} href={g.href} className="group flex items-center gap-6 border-b border-border py-6 hover:bg-muted/30 transition-colors px-2 -mx-2">
              <span className="font-mono text-[11px] text-muted-foreground w-20 shrink-0">{g.tag}</span>
              <div className="flex-1">
                <h3 className="font-heading text-xl md:text-2xl font-semibold group-hover:text-primary transition-colors">{g.t}</h3>
                <p className="font-body text-muted-foreground text-[14px] mt-1">{g.d}</p>
                <div className="flex flex-wrap gap-x-3 gap-y-1.5 mt-3">
                  {g.bullets.map((b) => (
                    <span key={b} className="font-mono text-[10.5px] text-muted-foreground bg-muted/30 px-2.5 py-0.5 border border-border/20">
                      {b}
                    </span>
                  ))}
                </div>
              </div>
              <ArrowUpRight className="w-5 h-5 text-muted-foreground group-hover:text-primary transition-colors shrink-0" />
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}
