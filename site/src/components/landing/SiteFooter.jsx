const COLS = [
  { h: "Product", links: ["How It Works", "Providers", "Pricing", "Download"] },
  { h: "Guides", links: ["Export ChatGPT", "Download Claude", "Backup Perplexity", "Gemini Takeout"] },
  { h: "Legal", links: ["Privacy", "Terms", "Refund Policy"] },
];

export default function SiteFooter() {
  return (
    <footer className="border-t border-border bg-background">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-14">
        <div className="grid md:grid-cols-[1.5fr_1fr_1fr_1fr] gap-10">
          <div>
            <div className="flex items-center gap-2.5">
              <span className="grid place-items-center w-7 h-7 bg-foreground text-background font-mono text-[13px]">TR</span>
              <span className="font-heading text-[17px] font-bold">TotalRecalls</span>
            </div>
            <p className="font-body text-muted-foreground text-[14px] mt-4 max-w-xs leading-relaxed">
              A Windows app that saves your AI conversations as Markdown + JSON you keep forever.
            </p>
          </div>
          {COLS.map((c) => (
            <div key={c.h}>
              <span className="font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground">{c.h}</span>
              <ul className="mt-4 space-y-2.5">
                {c.links.map((l) => (
                  <li key={l}><a href="#pricing" className="font-body text-[14px] text-foreground/80 hover:text-primary transition-colors">{l}</a></li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="mt-14 pt-6 border-t border-border flex flex-col md:flex-row md:items-center justify-between gap-3">
          <span className="font-mono text-[11px] text-muted-foreground">© 2026 TotalRecalls · Local files only</span>
          <span className="font-mono text-[11px] text-muted-foreground">Built solo · No cloud locker · No subscription</span>
        </div>
      </div>
    </footer>
  );
}
