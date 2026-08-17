import { Check, ArrowRight, Download } from "lucide-react";

const STRAIGHT = [
  "Windows 10/11 now.",
  "SmartScreen warning explained — what it means and how to proceed.",
  "No AdSense clutter. This site sells a tool, not pageviews.",
];

export default function PricingSection() {
  return (
    <section id="pricing" className="border-t border-border bg-background text-foreground">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-16 md:py-24">
        <div className="grid lg:grid-cols-2 gap-16 items-start">
          {/* Left Column: Pricing & CTAs */}
          <div>
            <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Relief · 06</span>
            
            <p className="font-body text-muted-foreground text-[15.5px] leading-relaxed mt-4 max-w-lg">
              One-time purchase. No subscription. Local files only.
              <br />
              14-day money-back guarantee — if it doesn't work for your setup, email us and we'll refund it, no questions asked.
            </p>
            
            <div className="mt-8 flex flex-col items-start gap-1">
              <span className="font-heading text-3xl md:text-4xl font-bold tracking-tight text-foreground">$24USD</span>
              <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary mt-1 font-semibold">discounted launch price</span>
            </div>

            <div className="mt-8 flex flex-col sm:flex-row gap-4">
              <a href="#pricing" data-tr-buy="true" class="inline-flex items-center justify-center gap-2 bg-primary text-white px-7 py-4 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:opacity-90 transition-opacity shadow-sm">
                Buy TotalRecalls — $24USD <ArrowRight className="w-4 h-4" />
              </a>
              <a href="/download/" class="inline-flex items-center justify-center gap-2 border border-border bg-card text-foreground px-6 py-4 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:bg-muted/50 transition-colors">
                <Download className="w-4 h-4" /> Download
              </a>
            </div>

            {/* Vertical Provider List */}
            <div className="mt-8 font-mono text-[11px] text-muted-foreground">
              <span className="font-semibold text-foreground uppercase tracking-wider block mb-2.5">Includes providers:</span>
              <ul className="space-y-1.5 border-l-2 border-primary/30 pl-3">
                <li className="text-foreground/90 font-medium">Perplexity</li>
                <li className="text-foreground/90 font-medium">ChatGPT</li>
                <li className="text-foreground/90 font-medium">Claude</li>
                <li className="text-foreground/90 font-medium">Gemini (Takeout)</li>
                <li className="text-foreground/90 font-medium">Grok</li>
              </ul>
              <span className="block mt-3 text-[10.5px] opacity-70">Version v1.0</span>
            </div>
          </div>

          {/* Right Column: Straight Talk & Checkmarks */}
          <div className="lg:border-l lg:border-border lg:pl-12">
            <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary font-medium">Straight talk</span>
            
            <ul className="mt-6 space-y-3.5">
              {STRAIGHT.map((s) => (
                <li key={s} className="flex items-start gap-3.5 bg-card/60 border border-border/80 p-4 rounded-sm hover:border-primary/40 transition-colors">
                  <Check className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                  <span className="font-body text-[14.5px] text-foreground font-medium leading-relaxed">{s}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
