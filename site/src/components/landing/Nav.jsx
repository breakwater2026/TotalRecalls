/* ============================================================================
 * LOCKED COMPONENT — DO NOT MODIFY WITHOUT EXPLICIT USER DIRECTIVE
 * File: site/src/components/landing/Nav.jsx
 * Status: LOCKED (Base44 Navigation Header with 39px scaled logo, single-row layout)
 * ============================================================================
 */

import { useState } from "react";
import { Menu, X, ArrowRight } from "lucide-react";

const LINKS = [
  { label: "How It Works", href: "#resolution" },
  { label: "Providers", href: "#matrix" },
  { label: "Library", href: "#library" },
  { label: "Guides", href: "#guides" },
  { label: "Pricing", href: "#pricing" },
];

export default function Nav() {
  const [open, setOpen] = useState(false);
  return (
    <header className="sticky top-0 z-40 bg-background/85 backdrop-blur border-b border-border">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 h-16 flex items-center justify-between">
        <a href="#top" className="flex items-center gap-2.5">
          <img src="/logo.png" alt="TotalRecalls" className="h-[39px] max-h-[39px] w-auto block object-contain" />
        </a>
        <nav className="hidden md:flex items-center gap-8">
          {LINKS.map((l) => (
            <a key={l.label} href={l.href} className="font-mono text-[11px] uppercase tracking-[0.18em] text-muted-foreground hover:text-foreground transition-colors">
              {l.label}
            </a>
          ))}
        </nav>
        <div className="hidden md:flex items-center gap-5">
          <a href="#pricing" data-tr-download className="font-mono text-[11px] uppercase tracking-[0.18em] text-muted-foreground hover:text-foreground">Download</a>
          <a href="#pricing" data-tr-buy className="inline-flex items-center gap-2 bg-primary text-white px-4 py-2 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:opacity-90 transition-opacity">
            Buy — $24USD <ArrowRight className="w-3.5 h-3.5" />
          </a>
        </div>
        <button className="md:hidden p-1" onClick={() => setOpen(!open)} aria-label="Menu">
          {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>
      {open && (
        <div className="md:hidden border-t border-border bg-background relative overflow-hidden">
          <span className="absolute left-0 top-0 h-full w-px bg-primary tr-scanline" />
          <nav className="px-5 py-4 flex flex-col gap-3.5">
            {LINKS.concat([{ label: "Download", href: "#pricing" }]).map((l) => (
              <a key={l.label} href={l.href} onClick={() => setOpen(false)} className="font-mono text-[12px] uppercase tracking-[0.16em] text-muted-foreground">
                {l.label}
              </a>
            ))}
            <a href="#pricing" data-tr-buy onClick={() => setOpen(false)} className="mt-1 inline-flex items-center justify-center gap-2 bg-primary text-white px-4 py-2.5 font-mono text-[12px] uppercase tracking-[0.14em]">
              Buy — $24USD
            </a>
          </nav>
        </div>
      )}
    </header>
  );
}
