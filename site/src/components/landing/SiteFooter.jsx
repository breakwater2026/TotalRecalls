const COLS = [
  { 
    h: "Product", 
    links: [
      { l: "How It Works", href: "/#resolution" },
      { l: "Providers", href: "/#matrix" },
      { l: "Pricing", href: "/#pricing" },
      { l: "Download", href: "/download/" },
      { l: "Release Notes", href: "/release-notes/" }
    ] 
  },
  { 
    h: "Guides", 
    links: [
      { l: "Download ChatGPT conversations", href: "/guides/export-chatgpt-conversations/" },
      { l: "Download your Claude history", href: "/guides/export-claude-chat-history/" },
      { l: "Backup Perplexity threads", href: "/guides/backup-perplexity-threads/" },
      { l: "Gemini Takeout → Markdown", href: "/guides/gemini-takeout-archive/" },
      { l: "Download DeepSeek chats", href: "/guides/deepseek/" },
      { l: "Download Mistral (Le Chat) conversations", href: "/guides/mistral/" },
      { l: "Download Qwen Chat conversations", href: "/guides/qwen/" },
      { l: "Downloading Grok conversations", href: "/guides/grok/" },
      { l: "Own your AI chat data", href: "/guides/own-your-ai-chat-data/" }
    ] 
  },
  { 
    h: "Legal", 
    links: [
      { l: "Privacy Policy", href: "/privacy/" },
      { l: "Terms of Service", href: "/terms/" },
      { l: "Refund Policy", href: "/legals/#refund" }
    ] 
  },
];

export default function SiteFooter() {
  return (
    <footer className="border-t border-border bg-background">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-14 text-center">
        <div className="grid md:grid-cols-4 gap-10 text-center items-start justify-items-center">
          <div className="flex flex-col items-center text-center">
            <div className="flex items-center gap-2.5">
              <img src="/logo.png" alt="TotalRecalls logo" className="h-[39px] w-auto object-contain" />
              <span className="font-heading text-[17px] font-bold">TotalRecalls</span>
            </div>
            <p className="font-body text-muted-foreground text-[14px] mt-4 max-w-xs leading-relaxed text-center">
              A Windows app that saves your AI conversations from eight providers as Markdown + JSON you keep forever.
            </p>
          </div>
          {COLS.map((c) => (
            <div key={c.h} className="flex flex-col items-center text-center">
              <span className="font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground">{c.h}</span>
              <ul className="mt-4 space-y-2.5 text-center">
                {c.links.map((link) => (
                  <li key={link.l}>
                    <a href={link.href} className="font-body text-[14px] text-foreground/80 hover:text-primary transition-colors">
                      {link.l}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-6 pt-4 border-t border-border/40 flex flex-col sm:flex-row items-center justify-center gap-4 md:gap-8 font-mono text-[11px] text-muted-foreground text-center">
          <span>© 2026 TotalRecalls v1.0.0</span>
          <span>·</span>
          <span>
            <a href="/privacy/" className="hover:text-primary transition-colors">Privacy Policy</a>
          </span>
          <span>·</span>
          <span>
            <a href="/terms/" className="hover:text-primary transition-colors">Terms of Service</a>
          </span>
          <span>·</span>
          <span>
            <a href="/legals/#refund" className="hover:text-primary transition-colors">Refund Policy</a>
          </span>
        </div>
      </div>
    </footer>
  );
}
