/* ============================================================================
 * LOCKED COMPONENT — DO NOT MODIFY WITHOUT EXPLICIT USER DIRECTIVE
 * File: site/src/components/landing/Nav.jsx
 * Status: LOCKED (Base44 Navigation Header with 39px scaled logo, single-row layout)
 * ============================================================================
 */

import { useState } from "react";
import { Menu, X, ArrowRight, Sun, Moon } from "lucide-react";

const LINKS = [
  { label: "How It Works", href: "/#resolution" },
  { label: "Providers", href: "/#matrix" },
  { label: "Library", href: "/#library" },
  { label: "Guides", href: "/#guides" },
  { label: "Pricing", href: "/#pricing" },
  { label: "Support", href: "/support/" },
  { label: "Legals", href: "/legals/" },
];

function toggleTheme(event) {
  event.stopPropagation();
  const root = document.documentElement;
  const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
  root.setAttribute("data-theme", next);
  try {
    localStorage.setItem("tr-theme", next);
  } catch {
    // Theme persistence is optional when storage is unavailable.
  }
  document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
    const sun = button.querySelector("[data-icon-sun]");
    const moon = button.querySelector("[data-icon-moon]");
    if (sun) sun.style.display = next === "dark" ? "none" : "inline-block";
    if (moon) moon.style.display = next === "dark" ? "inline-block" : "none";
    button.setAttribute("aria-label", next === "dark" ? "Switch to light mode" : "Switch to dark mode");
    button.setAttribute("title", next === "dark" ? "Switch to light mode" : "Switch to dark mode");
  });
}

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
          <button type="button" data-theme-toggle onClick={toggleTheme} className="p-1.5 rounded border border-border text-muted-foreground hover:text-foreground hover:bg-foreground/5 transition-colors" aria-label="Toggle theme">
            <span data-icon-sun className="inline-block"><Sun className="w-4 h-4" /></span>
            <span data-icon-moon className="hidden inline-block"><Moon className="w-4 h-4" /></span>
          </button>
          <a href="/download/" className="font-mono text-[11px] uppercase tracking-[0.18em] text-muted-foreground hover:text-foreground transition-colors">Download</a>
          <div className="flex flex-col items-center">
            <a href="/#pricing" data-tr-buy className="inline-flex items-center gap-2 bg-primary text-white px-4 py-1.5 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:opacity-90 transition-opacity">
              Buy — $24<span className="tr-usd">USD</span> <ArrowRight className="w-3.5 h-3.5" />
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
            <div className="flex items-center justify-between mb-1">
              <span className="font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground">Appearance</span>
              <button type="button" data-theme-toggle onClick={toggleTheme} className="p-1.5 rounded border border-border text-muted-foreground hover:text-foreground transition-colors" aria-label="Toggle theme">
                <span data-icon-sun className="inline-block"><Sun className="w-4 h-4" /></span>
                <span data-icon-moon className="hidden inline-block"><Moon className="w-4 h-4" /></span>
              </button>
            </div>
            {LINKS.concat([{ label: "Download", href: "/download/" }]).map((l) => (
              <a key={l.label} href={l.href} onClick={() => setOpen(false)} className="font-mono text-[12px] uppercase tracking-[0.16em] text-muted-foreground">
                {l.label}
              </a>
            ))}
            <a href="/#pricing" data-tr-buy onClick={() => setOpen(false)} className="mt-1 inline-flex flex-col items-center justify-center gap-0.5 bg-primary text-white px-4 py-2 font-mono text-[12px] uppercase tracking-[0.14em]">
              <span>Buy — $24<span className="tr-usd">USD</span></span>
              <span className="text-[9px] opacity-85 font-normal">discounted launch price</span>
            </a>
          </nav>
        </div>
      )}
    </header>
  );
}
