import React from "react";
import useReveal from "./useReveal";

/* Shared primitives for the Jasper landing rewrite — Brand Style Guide v1.0.
 * Sans (Inter) for meaning, mono (IBM Plex Mono) for evidence.
 * One Amber element per section. Radii: 6px chips / 8px buttons / 12px cards. */

export function Container({ className = "", children }) {
  return <div className={`mx-auto max-w-[1400px] px-5 md:px-10 ${className}`}>{children}</div>;
}

// Section shell: 96px desktop / 64px mobile vertical padding (hero: 128px top).
// Optional one-time 200ms reveal, off under prefers-reduced-motion.
export function Section({ id, className = "", pad = "normal", children }) {
  const ref = useReveal();
  const padding = pad === "hero" ? "pt-16 pb-16 md:pt-32 md:pb-24" : "py-16 md:py-24";
  return (
    <section id={id} ref={ref} className={`tr-reveal ${padding} ${className}`}>
      {children}
    </section>
  );
}

export function Eyebrow({ mono = false, children }) {
  return (
    <span className={`text-[12px] font-medium uppercase tracking-[0.12em] text-tr-steel ${mono ? "font-mono" : "font-body"}`}>
      {children}
    </span>
  );
}

// Primary = Archive Amber fill / Obsidian text. Secondary = transparent, 1px Slate border, Paper text.
// Tertiary = Steel Blue text link.
export function Btn({ href, variant = "primary", large = false, className = "", children }) {
  if (variant === "tertiary") {
    return (
      <a href={href} className={`text-[15px] font-semibold text-tr-steel transition-colors hover:text-tr-paper ${className}`}>
        {children}
      </a>
    );
  }
  const base = `inline-flex items-center justify-center gap-2 rounded-btn text-[15px] font-semibold tracking-[0.01em] transition-colors ${
    large ? "h-12 px-7" : "h-10 px-5"
  }`;
  if (variant === "secondary") {
    return (
      <a href={href} className={`${base} border border-tr-slate bg-transparent text-tr-paper hover:bg-tr-slate/40 ${className}`}>
        {children}
      </a>
    );
  }
  return (
    <a href={href} className={`${base} bg-tr-amber text-tr-obsidian hover:bg-tr-amber-hover active:bg-tr-amber-press ${className}`}>
      {children}
    </a>
  );
}

// Mono chips: 12px, uppercase, +0.02em, 6px radius, 4px×8px padding.
// Tones: slate = Steel on Slate fill · mist = Mist on Slate fill ·
//        amber = Amber on Amber Tint · local = Local Green, transparent, 1px Slate border ·
//        dust = Dust on Slate fill.
export function Chip({ tone = "slate", className = "", children }) {
  const tones = {
    slate: "bg-tr-slate text-tr-steel",
    mist: "bg-tr-slate text-tr-mist",
    amber: "bg-tr-amber/12 text-tr-amber",
    local: "border border-tr-slate text-tr-green",
    dust: "bg-tr-slate text-tr-dust",
  };
  return (
    <span className={`inline-flex items-center gap-1.5 whitespace-nowrap rounded-chip px-2 py-1 font-mono text-[12px] font-medium uppercase tracking-[0.02em] ${tones[tone]} ${className}`}>
      {children}
    </span>
  );
}

export function LocalChip({ className = "" }) {
  return (
    <Chip tone="local" className={className}>
      <span className="text-[10px] leading-none">●</span>
      Saved locally
    </Chip>
  );
}

// Static evidence row on Obsidian between 1px Slate rules.
// path = mono 14px Steel, selectable; chips appended after.
export function EvidenceStrip({ path, chips = [] }) {
  return (
    <div className="border-t border-b border-tr-slate py-4">
      <div className="flex flex-wrap items-center gap-3">
        {path ? (
          <code className="font-mono text-[13px] text-tr-steel select-all break-all md:text-[14px]">{path}</code>
        ) : null}
        {chips}
      </div>
    </div>
  );
}
