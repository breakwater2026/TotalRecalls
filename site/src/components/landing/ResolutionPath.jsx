/* ============================================================================
 * LOCKED COMPONENT — DO NOT MODIFY WITHOUT EXPLICIT USER DIRECTIVE
 * File: site/src/components/landing/ResolutionPath.jsx
 * Status: LOCKED & FROZEN (Ownership Path · 01, Step 3 "Pick your providers", single-line headline)
 *   USER DIRECTIVE 083126: rename eyebrow to "Ownership Path", add "Simple as ABCD",
 *   label squares A–D, and the path is now the Ownership Path. In force 2026-08-31.
 * ============================================================================
 */

import DriveTree from "./DriveTree";
import { ArrowRight } from "lucide-react";
import React from "react";

const STEPS = [
  { letter: "A", t: "Buy once", d: <>Checkout via order processor. One-time $24<span className="tr-usd">USD</span>, no subscription.</> },
  { letter: "B", t: "Install", d: "Unzip and run the Windows app. Local sign-in only." },
  { letter: "C", t: "Pick your providers", d: "ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, or Qwen." },
  { letter: "D", t: "Download", d: "Chats land as Markdown + JSON under your Library folder." },
];

export default function ResolutionPath() {
  return (
    <section id="resolution" className="border-t border-border">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-20 md:py-28">
        <header className="mb-12 max-w-4xl">
          <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Ownership Path</span>
          <h2 className="font-heading text-3xl md:text-5xl font-bold tracking-tight mt-3">From concern to ownership in a minute.</h2>
        </header>
        <div className="grid lg:grid-cols-[1fr_440px] gap-12">
          <div>
            <p className="font-heading text-lg md:text-2xl font-semibold tracking-tight mb-6">Simple as ABCD.</p>
            <div className="grid sm:grid-cols-2 gap-px bg-border border border-border">
              {STEPS.map((s) => (
                <div key={s.letter} className="bg-card p-6">
                  <span className="inline-flex items-center justify-center w-8 h-8 border border-primary text-primary font-mono text-[12px] uppercase tracking-wide">{s.letter}</span>
                  <h3 className="font-heading text-2xl font-semibold mt-3">{s.t}</h3>
                  <p className="font-body text-muted-foreground text-[14px] leading-relaxed mt-2">{s.d}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="lg:sticky lg:top-24 h-fit">
            <div className="border border-border bg-card">
              <DriveTree />
              <div className="p-6">
                <span className="font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground">Action Command Center</span>
                <p className="font-heading text-xl font-semibold mt-2">Local storage. Your drive. Your files.</p>
                <a href="#pricing" data-tr-buy className="mt-5 w-full inline-flex items-center justify-center gap-2 bg-primary text-white px-5 py-3.5 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:opacity-90 transition-opacity">
                  Begin Ownership <ArrowRight className="w-4 h-4" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
