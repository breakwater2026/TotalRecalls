function Window({ title, children }) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white shadow-lg overflow-hidden text-left">
      <div className="flex items-center gap-2 border-b border-gray-200 bg-gray-100 px-4 py-2">
        <span className="h-2.5 w-2.5 rounded-full bg-red-400"></span>
        <span className="h-2.5 w-2.5 rounded-full bg-yellow-400"></span>
        <span className="h-2.5 w-2.5 rounded-full bg-green-400"></span>
        <span className="ml-2 font-mono text-xs text-gray-500">{title}</span>
      </div>
      {children}
    </div>
  );
}

export function LibraryMock() {
  const rows = [
    ["chatgpt/2026-08-01-pricing-research.md", "Aug 1", "12 KB"],
    ["claude/2026-07-28-refactor-plan.md", "Jul 28", "31 KB"],
    ["perplexity/2026-07-21-market-scan.md", "Jul 21", "8 KB"],
    ["gemini/2026-07-14-takeout-thread.md", "Jul 14", "19 KB"],
    ["grok/2026-07-02-debug-session.md", "Jul 2", "6 KB"],
  ];
  return (
    <Window title="TotalRecalls — Library">
      <div className="flex text-xs">
        <div className="w-32 shrink-0 border-r border-gray-200 bg-gray-50 p-3 space-y-1.5">
          <div className="font-semibold text-gray-800">Library</div>
          {["ChatGPT", "Claude", "Perplexity", "Gemini", "Grok"].map((p) => (
            <div key={p} className="flex items-center gap-1.5 text-gray-600">
              <span className="h-1.5 w-1.5 rounded-sm bg-gray-400"></span>
              {p}
            </div>
          ))}
        </div>
        <div className="flex-1 p-3 space-y-1.5">
          {rows.map(([f, d, s]) => (
            <div key={f} className="flex items-center justify-between gap-2 rounded bg-gray-50 px-2 py-1.5">
              <span className="truncate font-mono text-gray-700">{f}</span>
              <span className="shrink-0 text-gray-400">{d} · {s}</span>
            </div>
          ))}
        </div>
      </div>
    </Window>
  );
}

export function MarkdownMock() {
  return (
    <Window title="2026-08-01-pricing-research.md">
      <div className="p-4 space-y-2 text-xs">
        <div className="font-mono text-sm font-semibold text-gray-900"># Pricing research</div>
        <div className="font-mono text-gray-400">exported 2026-08-01 · provider: chatgpt · 14 messages</div>
        <div className="rounded bg-gray-100 p-2 text-gray-700">
          <span className="font-semibold text-gray-900">You:</span> Compare one-time pricing for export tools.
        </div>
        <div className="rounded border border-gray-200 p-2 text-gray-700">
          <span className="font-semibold text-gray-900">Assistant:</span> Here is a table of the options I found, with
          links and caveats…
        </div>
        <div className="font-mono text-gray-400">+ attachments: sources.json</div>
      </div>
    </Window>
  );
}
