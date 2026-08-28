/* ============================================================================
 * LOCKED COMPONENT — DO NOT MODIFY WITHOUT EXPLICIT USER DIRECTIVE
 * File: site/src/components/landing/DriveTree.jsx
 * Status: LOCKED & FROZEN
 * ============================================================================
 */

import { Folder, FileText, HardDrive } from "lucide-react";

const PROVIDERS = [
  { name: "ChatGPT", count: "284 files" },
  { name: "Claude", count: "312 files" },
  { name: "Perplexity", count: "96 files" },
  { name: "Gemini", count: "47 files" },
  { name: "Grok", count: "58 files" },
  { name: "DeepSeek", count: "126 files" },
  { name: "Mistral", count: "84 files" },
  { name: "Qwen Chat", count: "47 files" },
];

export default function DriveTree() {
  return (
    <div className="relative bg-card overflow-hidden border-b border-border">
      <div className="absolute top-0 left-0 right-0 h-px bg-primary tr-scanline" />
      <div className="flex items-center gap-2 px-4 h-9 border-b border-border bg-muted/40">
        <HardDrive className="w-3.5 h-3.5 text-muted-foreground" />
        <span className="font-mono text-[11px] text-muted-foreground">C:\TotalRecalls\Library</span>
        <span className="ml-auto font-mono text-[9px] text-primary">writing…</span>
      </div>
      <div className="p-5 font-mono text-[12px]">
        <div className="flex items-center gap-2 text-foreground">
          <Folder className="w-4 h-4 text-primary" /> TotalRecalls
        </div>
        <div className="ml-4 mt-2 pl-3 border-l border-border space-y-2">
          {PROVIDERS.map((p) => (
            <div key={p.name} className="flex items-center justify-between">
              <span className="flex items-center gap-2">
                <Folder className="w-3.5 h-3.5 text-muted-foreground" /> {p.name}
              </span>
              <span className="text-[10px] text-muted-foreground">{p.count}</span>
            </div>
          ))}
          <div className="flex items-center gap-2 text-muted-foreground">
            <FileText className="w-3.5 h-3.5" /> 2026-08-01-pricing-research.md
          </div>
        </div>
      </div>
    </div>
  );
}
