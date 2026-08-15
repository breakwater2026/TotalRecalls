import { Check, ArrowRight, Download } from "lucide-react";

const STRAIGHT = [
  "Windows app today (WebView2). Mac later if demand is real.",
  "Gemini uses your Google Takeout JSON.",
  "Unsigned builds may show SmartScreen until code-signing is complete.",
  "Windows 11 Smart App Control may block unsigned apps.",
  "You must follow each provider's terms.",
  "No AdSense clutter.",
];

export default function PricingSection() {
  return (
    <section id="pricing" className="border-t border-border bg-foreground text-background">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-20 md:py-28">
        <div className="grid lg:grid-cols-2 gap-16">
          <div>
            <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Resolution · 05</span>
            <h2 className="font-heading text-4xl md:text-6xl font-bold tracking-tight mt-3">Begin resolution.</h2>
            <p className="font-body text-background/70 text-[15px] leading-relaxed mt-5 max-w-md">
              One-time purchase. No subscription. Local files only. 14-day money-back guarantee — if it doesn't work for you, email us and we'll refund it, no questions asked.
            </p>
            <div className="mt-10 flex items-end gap-4">
              <span className="font-heading text-7xl font-bold">$24</span>
              <span className="font-mono text-[11px] uppercase tracking-[0.16em] text-background/50 mb-3">launch price · one-time</span>
            </div>
            <div className="mt-8 flex flex-col sm:flex-row gap-3">
              <a href="#pricing" className="inline-flex items-center justify-center gap-2 bg-primary text-white px-6 py-3.5 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:opacity-90 transition-opacity">
                Buy TotalRecalls — $24 <ArrowRight className="w-4 h-4" />
              </a>
              <a href="#pricing" className="inline-flex items-center justify-center gap-2 border border-background/20 text-background px-6 py-3.5 font-mono text-[12px] uppercase tracking-[0.14em] hover:bg-background/10 transition-colors">
                <Download className="w-4 h-4" /> Download ZIP
              </a>
            </div>
            <p className="font-mono text-[11px] text-background/40 mt-5">Early access build · actively improving on feedback</p>
          </div>
          <div className="lg:border-l lg:border-background/10 lg:pl-12">
            <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-background/50">Straight talk</span>
            <ul className="mt-6 space-y-4">
              {STRAIGHT.map((s) => (
                <li key={s} className="flex gap-3 font-body text-[14px] text-background/80 leading-relaxed">
                  <Check className="w-4 h-4 text-primary shrink-0 mt-1" /> {s}
                </li>
              ))}
            </ul>
            <p className="font-body text-background/50 text-[13px] mt-8 leading-relaxed italic">
              Built by a solo developer who was tired of losing months of AI conversations to broken exports and shifting UIs.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
