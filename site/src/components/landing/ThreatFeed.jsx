const EVENTS = [
  "2026-08-15 · chatgpt · download failed · thread lost",
  "2026-08-15 · claude · ui revision · 4 threads orphaned",
  "2026-08-14 · perplexity · session expired · research trail gone",
  "2026-08-14 · gemini · takeout parse error · 2 archives unreadable",
  "2026-08-13 · grok · tab closed · debug session lost",
  "2026-08-13 · chatgpt · 9 months of prompts · no backup",
];

export default function ThreatFeed() {
  const row = [...EVENTS, ...EVENTS];
  return (
    <div className="bg-foreground text-background h-9 flex items-center overflow-hidden">
      <span className="shrink-0 flex items-center gap-2 px-3 h-full bg-destructive text-white font-mono text-[10px] uppercase tracking-[0.18em] font-medium">
        <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse" /> Live Feed
      </span>
      <div className="relative flex-1 overflow-hidden">
        <div className="flex whitespace-nowrap animate-tr-ticker will-change-transform">
          {row.map((e, i) => (
            <span key={i} className="font-mono text-[11px] tracking-tight text-background/80 px-6 flex items-center gap-2">
              <span className="text-destructive">▍</span>{e}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
