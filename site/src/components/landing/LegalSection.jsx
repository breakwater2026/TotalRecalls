/* Legal · 07 — anchors the legal page (/legals/) into the landing page scroll flow. */
import { ArrowRight } from "lucide-react";

const POLICIES = [
  {
    label: "Privacy Policy",
    href: "/legals/#privacy",
    blurb: "Local-first, privacy-by-design. We never collect, host, or transmit your AI conversations.",
  },
  {
    label: "Terms of Service",
    href: "/legals/#terms",
    blurb: "One-time purchase, single-user license, and your responsibility to follow each provider's terms.",
  },
  {
    label: "Pricing & Free Tier",
    href: "/legals/#pricing",
    blurb: "One-time $24 USD, lifetime license and updates. A free web tier is on the way — our answer to refunds.",
  },
];

export default function LegalSection() {
  return (
    <section id="legal" className="border-t border-border">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-20 md:py-28">
        <header className="flex flex-col md:flex-row md:items-end md:justify-between gap-6 mb-12">
          <div>
            <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Legal</span>
            <h2 className="font-heading text-3xl md:text-5xl font-bold tracking-tight mt-3">Policies, plainly stated.</h2>
          </div>
          <a
            href="/legals/"
            className="group inline-flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.18em] text-primary hover:underline"
          >
            Read all policies <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
          </a>
        </header>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-px bg-border border border-border">
          {POLICIES.map((p) => (
            <a
              key={p.label}
              href={p.href}
              className="group bg-card border-l-2 border-primary p-6 flex flex-col justify-between min-h-[160px] hover:bg-muted/40 transition-colors"
            >
              <span className="font-heading text-xl font-bold tracking-tight">{p.label}</span>
              <span className="font-body text-muted-foreground text-[13.5px] leading-relaxed mt-3">{p.blurb}</span>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}
