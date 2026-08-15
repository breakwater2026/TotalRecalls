import { Folder, ArrowDownToLine } from "lucide-react";

const PROVIDERS = [
  { name: "ChatGPT", code: "OAI-001" },
  { name: "Claude", code: "ANT-002" },
  { name: "Perplexity", code: "PPL-003" },
  { name: "Gemini", code: "GEM-004" },
  { name: "Grok", code: "GRK-005" },
];

const YS = [36, 96, 156, 216, 276];

export default function ConvergenceDiagram() {
  return (
    <div className="relative aspect-[4/3] border border-border overflow-hidden bg-card">
      <div className="absolute top-0 left-0 right-0 h-px bg-primary tr-scanline z-20" />
      <div className="absolute top-3 left-3 font-mono text-[10px] text-muted-foreground bg-card/90 px-2 py-1 z-20">CONVERGENCE · LIVE</div>
      <div className="absolute top-3 right-3 font-mono text-[10px] text-primary bg-card/90 px-2 py-1 z-20">5 SOURCES → 1 FOLDER</div>

      <svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid meet" className="absolute inset-0 w-full h-full">
        {YS.map((y, i) => {
          const d = `M150,${y} C195,${y} 195,150 240,150`;
          return (
            <g key={i}>
              <path d={d} fill="none" stroke="hsl(var(--border))" strokeWidth="1" />
              <path d={d} fill="none" stroke="hsl(var(--primary))" strokeWidth="1.5" strokeDasharray="4 6" className="tr-flow" />
              <rect x="-3.5" y="-2.5" width="7" height="5" rx="1" fill="hsl(var(--primary))">
                <animateMotion dur="2.4s" repeatCount="indefinite" begin={`${i * 0.4}s`} path={d} />
              </rect>
            </g>
          );
        })}
      </svg>

      {PROVIDERS.map((p, i) => (
        <div key={p.name} className="absolute left-[2.5%] w-[33%] flex items-center gap-2 z-10" style={{ top: `${(YS[i] / 300) * 100}%`, transform: "translateY(-50%)" }}>
          <span className="grid place-items-center w-6 h-6 bg-foreground text-background shrink-0">
            <ArrowDownToLine className="w-3.5 h-3.5" />
          </span>
          <div className="min-w-0">
            <p className="font-heading text-[13px] font-semibold leading-none truncate">{p.name}</p>
            <p className="font-mono text-[9px] text-muted-foreground mt-0.5">{p.code}</p>
          </div>
        </div>
      ))}

      <div className="absolute z-10 flex flex-col items-center justify-center text-center px-3 border border-primary/40 bg-background" style={{ left: "58%", top: "33%", width: "34%", height: "34%" }}>
        <Folder className="w-7 h-7 text-primary" strokeWidth={1.75} />
        <p className="font-mono text-[11px] mt-2 leading-tight">C:\TotalRecalls<br /><span className="text-muted-foreground">Library\</span></p>
        <p className="font-mono text-[9px] text-primary mt-2">797 files · secured</p>
      </div>
    </div>
  );
}
