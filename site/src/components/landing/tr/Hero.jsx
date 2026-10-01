import React from "react";
import { Container, Eyebrow, Btn } from "./ui";

const TRUST = ["No cloud", "No account", "One-time $24", "Windows 10/11"];

const TREE = [
  { d: "chatgpt\\", n: "3 files" },
  { d: "claude\\", n: "4 files" },
  { d: "perplexity\\", n: "2 files" },
  { d: "gemini\\", n: "1 file" },
];

export default function Hero() {
  return (
    <div id="top" className="bg-tr-obsidian pt-16 pb-16 md:pt-32 md:pb-24">
      <Container>
        <div className="grid lg:grid-cols-2 gap-10 lg:gap-16 items-start">
          {/* Left: promise */}
          <div>
            <Eyebrow mono>Windows app · Local-first</Eyebrow>

            <h1 className="mt-3 font-heading text-[40px] md:text-[64px] font-bold leading-[1.05] tracking-[-0.02em] text-tr-paper">
              Recall every AI conversation, kept on your own PC.
            </h1>

            <p className="mt-6 max-w-[680px] font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-mist">
              Save chats from ChatGPT, Claude, and six more AI tools as Markdown and JSON
              files in one private folder you control.
            </p>

            <div className="mt-8 flex flex-col sm:flex-row sm:items-center gap-4">
              <Btn href="/download/" large>Download free</Btn>
              <Btn href="#resolution" variant="secondary" large>See how it works</Btn>
            </div>

            <p className="mt-5 hidden sm:block max-w-[680px] font-body text-[14px] leading-[1.5] text-tr-dust">
              Free Tier covers ChatGPT, Claude, and Perplexity, 5 conversations each. Pro
              unlocks all 8 providers for $24 one-time (launch price).
            </p>
            <p className="mt-5 sm:hidden max-w-[680px] font-body text-[14px] leading-[1.5] text-tr-dust">
              Windows app. Visit from your desktop to download.
            </p>

            <div className="mt-8 flex flex-wrap gap-2">
              {TRUST.map((t) => (
                <span key={t} className="inline-flex whitespace-nowrap rounded-chip bg-tr-slate px-2 py-1 font-mono text-[12px] font-medium uppercase tracking-[0.02em] text-tr-dust">
                  {t}
                </span>
              ))}
            </div>
          </div>

          {/* Right: product visual — app panel, files landing in the Library folder */}
          <div className="rounded-card border border-tr-slate bg-tr-graphite p-4 md:p-5">
            <div className="flex items-center gap-2 border-b border-tr-slate pb-3">
              <span className="h-2 w-2 rounded-full bg-tr-slate" />
              <span className="h-2 w-2 rounded-full bg-tr-slate" />
              <span className="h-2 w-2 rounded-full bg-tr-slate" />
              <span className="ml-2 font-mono text-[12px] text-tr-dust">TotalRecalls — Windows</span>
            </div>

            <div className="mt-4 grid grid-cols-1 sm:grid-cols-[1fr_220px] gap-4">
              {/* Provider list */}
              <div>
                <p className="font-body text-[12px] font-medium uppercase tracking-[0.12em] text-tr-dust">Providers</p>
                <ul className="mt-3 space-y-1.5">
                  {["ChatGPT", "Claude", "Perplexity", "Gemini", "Grok", "DeepSeek", "Mistral", "Qwen"].map((p, i) => (
                    <li
                      key={p}
                      className={`flex items-center justify-between rounded-btn border px-3 py-2 ${
                        i < 3 ? "border-tr-slate bg-tr-obsidian" : "border-tr-slate/60"
                      }`}
                    >
                      <span className="font-body text-[14px] text-tr-paper">{p}</span>
                      {i < 3 ? (
                        <span className="inline-flex items-center gap-1.5 font-mono text-[12px] text-tr-green">
                          <span className="h-1.5 w-1.5 rounded-full bg-tr-green" /> Saved
                        </span>
                      ) : (
                        <span className="font-mono text-[12px] text-tr-dust">—</span>
                      )}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Library folder */}
              <div className="rounded-card border border-tr-slate bg-tr-obsidian p-3">
                <p className="font-mono text-[12px] text-tr-steel break-all">C:\TotalRecalls\Library\</p>
                <ul className="mt-2.5 space-y-1.5">
                  {TREE.map((r) => (
                    <li key={r.d} className="flex items-center justify-between gap-2">
                      <span className="font-mono text-[12px] text-tr-steel">{r.d}</span>
                      <span className="font-mono text-[11px] text-tr-dust whitespace-nowrap">{r.n}</span>
                    </li>
                  ))}
                  <li className="font-mono text-[12px] text-tr-dust">└── …</li>
                </ul>
                <div className="mt-3 border-t border-tr-slate pt-3">
                  <p className="font-mono text-[12px] leading-relaxed text-tr-steel break-all select-all">
                    claude\2026-07-28-refactor-plan.md
                  </p>
                  <div className="mt-2 flex items-center gap-1.5">
                    <span className="rounded-chip border border-tr-slate px-2 py-0.5 font-mono text-[12px] font-medium uppercase tracking-[0.02em] text-tr-steel">.md</span>
                    <span className="rounded-chip border border-tr-slate px-2 py-0.5 font-mono text-[12px] font-medium uppercase tracking-[0.02em] text-tr-steel">.json</span>
                    <span className="rounded-chip border border-tr-slate px-2 py-0.5 font-mono text-[12px] font-medium uppercase tracking-[0.02em] text-tr-green">
                      <span className="text-[10px] leading-none">●</span> Saved locally
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Container>
    </div>
  );
}
