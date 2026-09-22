import { Folder } from "lucide-react";
import { LOGOS } from "./RiskMatrix";
import React from "react";

const PROVIDERS = [
  // NOTE: glyph (`color`) must contrast with the tile (`bg`). The first three
  // were drawing the logo path in the SAME color as its own tile (fill == bg),
  // so the mark rendered invisible — only the solid brand square showed
  // (reported 2026-09-13: "first three have no icon, just colors"). Fixed by
  // white glyph on the brand-color tile; the other five already had a
  // contrasting fill/bg and are unchanged.
  { name: "ChatGPT", code: "OAI-001", logo: "ChatGPT", color: "#FFFFFF", bg: "bg-[#10A37F]" },
  { name: "Claude", code: "ANT-002", logo: "Claude", color: "#FFFFFF", bg: "bg-[#D97757]" },
  { name: "Perplexity", code: "PPL-003", logo: "Perplexity", color: "#FFFFFF", bg: "bg-[#20B8CD]" },
  { name: "Gemini", code: "GEM-004", logo: "Gemini", color: "#4285F4", bg: "bg-[#000000]" },
  { name: "Grok", code: "GRK-005", logo: "Grok", color: "#FFFFFF", bg: "bg-[#0F172A]" },
  { name: "DeepSeek", code: "DSK-006", logo: "DeepSeek", color: "#4F8CFF", bg: "bg-[#1E40AF]" },
  { name: "Mistral", code: "MST-007", logo: "Mistral", color: "#FF7000", bg: "bg-[#FFF3E8]" },
  { name: "Qwen Chat", code: "QWN-008", logo: "Qwen", color: "#615CED", bg: "bg-[#F0EFFF]" },
];

const YS = [20, 58, 96, 134, 172, 210, 248, 286];

export default function ConvergenceDiagram() {
  return (
    <div className="relative aspect-[4/3] border border-border overflow-hidden bg-card">
      <div className="absolute top-0 left-0 right-0 h-px bg-primary tr-scanline z-20" />
      <div className="absolute top-3 left-1/2 -translate-x-1/2 font-mono text-[10px] text-muted-foreground bg-card px-2.5 py-1 z-20 whitespace-nowrap tracking-wider">
        CONVERGENCE · LIVE
      </div>
      <div className="absolute top-3 right-3 font-mono text-[10px] text-primary bg-card px-2 py-1 z-20">
        8 SOURCES → 1 FOLDER
      </div>

      <svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid meet" className="absolute inset-0 w-full h-full z-0">
        {YS.map((y, i) => {
          const d = `M90,${y} C170,${y} 185,150 232,150`;
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

      {PROVIDERS.map((p, i) => {
        const logo = LOGOS[p.logo];
        return (
          <div
            key={p.name}
            className="absolute left-[2.5%] w-[35%] flex items-center gap-1.5 z-10 bg-card p-1 rounded-sm border border-border/50 shadow-sm"
            style={{ top: `${(YS[i] / 300) * 100}%`, transform: "translateY(-50%)" }}
          >
            <span className={`grid place-items-center w-6 h-6 ${p.bg} shrink-0 rounded-sm shadow-sm`}>
              <svg viewBox={logo.vb} className="w-3.5 h-3.5" fill={p.color} aria-hidden="true">
                <path d={logo.d} />
              </svg>
            </span>
            <div className="min-w-0">
              <p className="font-heading text-[12px] font-semibold leading-none truncate">{p.name}</p>
              <p className="font-mono text-[8px] text-muted-foreground mt-0.5">{p.code}</p>
            </div>
          </div>
        );
      })}

      <div className="absolute z-10 flex flex-col items-center justify-center text-center px-3 border border-primary/40 bg-background" style={{ left: "58%", top: "33%", width: "34%", height: "34%" }}>
        <Folder className="w-7 h-7 text-primary" strokeWidth={1.75} />
        <p className="font-mono text-[11px] mt-2 leading-tight">C:\TotalRecalls<br /><span className="text-muted-foreground">Library\</span></p>
        <p className="font-mono text-[9px] text-primary mt-2">797 files · secured</p>
      </div>
    </div>
  );
}
