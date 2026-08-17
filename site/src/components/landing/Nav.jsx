/* ============================================================================
 * LOCKED COMPONENT — DO NOT MODIFY WITHOUT EXPLICIT USER DIRECTIVE
 * File: site/src/components/landing/Nav.jsx
 * Status: LOCKED (Base44 Navigation Header with 39px scaled logo, single-row layout)
 * ============================================================================
 */

import { useState } from "react";
import { Menu, X, ArrowRight } from "lucide-react";

const LINKS = [
  { label: "How It Works", href: "/#resolution" },
  { label: "Providers", href: "/#matrix" },
  { label: "Library", href: "/#library" },
  { label: "Guides", href: "/#guides" },
  { label: "Pricing", href: "/#pricing" },
  { label: "Legals", href: "/legals/" },
];

export default function Nav() {
  const [open, setOpen] = useState(false);
  return (
    <header className="sticky top-0 z-40 bg-background/95 backdrop-blur border-b border-border py-2.5">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 flex items-center justify-between">
        <a href="/#top" className="flex items-center gap-2.5">
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
          <a href="/download/" className="font-mono text-[11px] uppercase tracking-[0.18em] text-muted-foreground hover:text-foreground transition-colors">Download</a>
          <div className="flex flex-col items-center">
            <a href="/#pricing" data-tr-buy className="inline-flex items-center gap-2 bg-primary text-white px-4 py-1.5 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:opacity-90 transition-opacity">
              Buy — $24USD <ArrowRight className="w-3.5 h-3.5" />
            </a>
            <span className="font-mono text-[9px] uppercase tracking-[0.12em] text-primary mt-1 font-semibold whitespace-nowrap">
              discounted launch price
            </span>
          </div>
        </div>
        <button className="md:hidden p-1" onClick={() => setOpen(!open)} aria-label="Menu">
          {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>
      {open && (
        <div className="md:hidden border-t border-border bg-background relative overflow-hidden mt-2.5">
          <span className="absolute left-0 top-0 h-full w-px bg-primary tr-scanline" />
          <nav className="px-5 py-4 flex flex-col gap-3.5">
            {LINKS.concat([{ label: "Download", href: "/download/" }]).map((l) => (
              <a key={l.label} href={l.href} onClick={() => setOpen(false)} className="font-mono text-[12px] uppercase tracking-[0.16em] text-muted-foreground">
                {l.label}
              </a>
            ))}
            <a href="/#pricing" data-tr-buy onClick={() => setOpen(false)} className="mt-1 inline-flex flex-col items-center justify-center gap-0.5 bg-primary text-white px-4 py-2 font-mono text-[12px] uppercase tracking-[0.14em]">
              <span>Buy — $24USD</span>
              <span className="text-[9px] opacity-85 font-normal">discounted launch price</span>
            </a>
          </nav>
        </div>
      )}
    </header>
  );
}
