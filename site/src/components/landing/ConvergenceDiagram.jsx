import { Folder } from "lucide-react";

const ChatGptIcon = () => (
  <svg viewBox="0 0 24 24" fill="#FFFFFF" className="w-3.5 h-3.5 text-white">
    <path d="M22.28 9.82a5.98 5.98 0 0 0-.52-4.91 6.05 6.05 0 0 0-6.42-2.88 5.99 5.99 0 0 0-4.63-2.03 6.05 6.05 0 0 0-5.77 4.19 6 6 0 0 0-4.15 2.99 6.06 6.05 0 0 0 .73 7.03 5.98 5.98 0 0 0 .52 4.9 6.05 6.05 0 0 0 6.42 2.89 5.99 5.99 0 0 0 4.63 2.03 6.05 6.05 0 0 0 5.77-4.19 6 6 0 0 0 4.15-2.99 6.06 6.06 0 0 0-.73-7.03zm-7.1 10.37a4.28 4.28 0 0 1-2.58-.29l.13-.08 3.58-2.07c.18-.1.29-.31.29-.52v-5.02l1.5 1.5v4.21a4.28 4.28 0 0 1-2.92 2.27zm-8.8-2.14a4.28 4.28 0 0 1-1.07-2.37l.13.08 3.58 2.07c.18.1.42.1.6 0l4.35-2.51v1.73l-3.65 2.11a4.28 4.28 0 0 1-3.94-.11zm-1.7-8.23a4.28 4.28 0 0 1 1.51-2.08l-.01.15v4.14a.59.59 0 0 0 .29.52l4.35 2.51-1.5 1.5-3.65-2.11a4.28 4.28 0 0 1-.99-4.63zm9.1-5.17a4.28 4.28 0 0 1 2.58.29l-.13.08-3.58 2.07a.59.59 0 0 0-.29.52v5.02l-1.5-1.5v-4.21a4.28 4.28 0 0 1 2.92-2.27zm8.8 2.14a4.28 4.28 0 0 1 1.07 2.37l-.13-.08-3.58-2.07a.59.59 0 0 0-.6 0l-4.35 2.51v-1.73l3.65-2.11a4.28 4.28 0 0 1 3.94.11zm1.7 8.23a4.28 4.28 0 0 1-1.51 2.08l.01-.15v-4.14a.59.59 0 0 0-.29-.52l-4.35-2.51 1.5-1.5 3.65 2.11a4.28 4.28 0 0 1 .99 4.63z"/>
  </svg>
);

const ClaudeIcon = () => (
  <svg viewBox="0 0 24 24" fill="#FFFFFF" className="w-3.5 h-3.5 text-white">
    <path d="M12 1.5a1 1 0 0 1 1 1V5a1 1 0 1 1-2 0V2.5a1 1 0 0 1 1-1zm0 16a1 1 0 0 1 1 1v2.5a1 1 0 1 1-2 0V18.5a1 1 0 0 1 1-1zM22.5 12a1 1 0 0 1-1 1H19a1 1 0 1 1 0-2h2.5a1 1 0 0 1 1 1zM5 12a1 1 0 0 1-1 1H1.5a1 1 0 1 1 0-2H4a1 1 0 0 1 1 1zm14.435-7.435a1 1 0 0 1 0 1.414L17.668 7.747a1 1 0 1 1-1.414-1.414l1.767-1.768a1 1 0 0 1 1.414 0zm-11.313 11.314a1 1 0 0 1 0 1.414L6.355 19.06a1 1 0 0 1-1.414-1.414l1.768-1.768a1 1 0 0 1 1.414 0zm11.313 0a1 1 0 0 1-1.414 0l-1.768-1.768a1 1 0 1 1 1.414-1.414l1.768 1.768a1 1 0 0 1 0 1.414zM6.355 4.935a1 1 0 0 1 1.414 0l1.768 1.768a1 1 0 1 1-1.414 1.414L6.355 6.349a1 1 0 0 1 0-1.414zM12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10z"/>
  </svg>
);

const PerplexityIcon = () => (
  <svg viewBox="0 0 24 24" fill="#FFFFFF" className="w-3.5 h-3.5 text-white">
    <path d="M12 2L4 6v12l8 4 8-4V6l-8-4zm0 2.2L18 7.5v9L12 19.5l-6-3v-9l6-3.3zM11 8h2v8h-2V8z" />
  </svg>
);

const GeminiIcon = () => (
  <svg viewBox="0 0 24 24" className="w-3.5 h-3.5">
    <defs>
      <linearGradient id="geminiSparkleGrad" x1="0" y1="0" x2="24" y2="24" gradientUnits="userSpaceOnUse">
        <stop offset="0%" stopColor="#EA4335" />
        <stop offset="35%" stopColor="#FBBC05" />
        <stop offset="65%" stopColor="#34A853" />
        <stop offset="100%" stopColor="#4285F4" />
      </linearGradient>
    </defs>
    <path
      style={{ fill: "url(#geminiSparkleGrad)" }}
      d="M12 2C12 7.52 7.52 12 2 12C7.52 12 12 16.48 12 22C12 16.48 16.48 12 22 12C16.48 12 12 7.52 12 2Z"
    />
  </svg>
);

const GrokIcon = () => (
  <svg viewBox="0 0 24 24" fill="#FFFFFF" className="w-3.5 h-3.5 text-white">
    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
  </svg>
);

const DeepSeekIcon = () => (
  <svg viewBox="0 0 24 24" fill="#FFFFFF" className="w-3.5 h-3.5 text-white">
    <circle cx="12" cy="12" r="10" fill="none" stroke="#FFFFFF" strokeWidth="1.5" />
    <path d="M7 9h4l3 4-3 4H7l3-4-3-4zm6 0h4l-3 4 3 4h-4l-3-4 3-4z" fill="#FFFFFF" />
  </svg>
);

const MistralIcon = () => (
  <svg viewBox="0 0 24 24" fill="#FFFFFF" className="w-3.5 h-3.5 text-white">
    <path d="M5 3h14v3h-3l-1 4 1 4h3v3H5v-3h3l1-4-1-4H5V3zm4 11h2v2H9v-2zm0 3h2v2H9v-2zm0 3h2v2H9v-2zm4-6h2v2h-2v-2zm0 3h2v2h-2v-2zm0 3h2v2h-2v-2z" />
  </svg>
);

const QwenIcon = () => (
  <svg viewBox="0 0 24 24" fill="#FFFFFF" className="w-3.5 h-3.5 text-white">
    <path d="M12 2L4 7v10l8 5 8-5V7L12 2zm0 2.5L18 8v8l-6 3.7L6 16V8l6-3.5zM9 10h6v1.5H9V10zm0 2.5h6V14H9v-1.5z" />
  </svg>
);

const PROVIDERS = [
  { name: "ChatGPT", code: "OAI-001", Icon: ChatGptIcon, bg: "bg-[#10A37F]" },
  { name: "Claude", code: "ANT-002", Icon: ClaudeIcon, bg: "bg-[#D97757]" },
  { name: "Perplexity", code: "PPL-003", Icon: PerplexityIcon, bg: "bg-[#1FA2B8]" },
  { name: "Gemini", code: "GEM-004", Icon: GeminiIcon, bg: "bg-[#000000]" },
  { name: "Grok", code: "GRK-005", Icon: GrokIcon, bg: "bg-[#0F172A]" },
  { name: "DeepSeek", code: "DSK-006", Icon: DeepSeekIcon, bg: "bg-[#1E40AF]" },
  { name: "Mistral", code: "MST-007", Icon: MistralIcon, bg: "bg-[#FF7000]" },
  { name: "Qwen Chat", code: "QWN-008", Icon: QwenIcon, bg: "bg-[#615CED]" },
];

const YS = [22, 64, 106, 148, 190, 232, 252, 268];

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

      {PROVIDERS.map((p, i) => (
        <div key={p.name} className="absolute left-[2.5%] w-[33%] flex items-center gap-2 z-10 bg-card p-1.5 rounded-sm border border-border/50 shadow-sm" style={{ top: `${(YS[i] / 300) * 100}%`, transform: "translateY(-50%)" }}>
          <span className={`grid place-items-center w-6 h-6 ${p.bg} shrink-0 rounded-sm shadow-sm`}>
            <p.Icon />
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
