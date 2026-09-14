import { Check } from "lucide-react";

const PROVIDERS = [
  "ChatGPT",
  "Claude",
  "Perplexity",
  "Gemini",
  "Grok",
  "DeepSeek",
  "Mistral",
  "Qwen",
];

const STRAIGHT = [
  "Windows 10/11 now. Linux and Apple apps are on the way.",
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
            <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Ownership</span>

            <h2 className="font-heading text-3xl md:text-4xl font-bold tracking-tight mt-4">
              One price. Every conversation. Yours forever.
            </h2>

            <p className="font-body text-muted-foreground text-[15.5px] leading-relaxed mt-4 max-w-lg">
              Try it free first. The Free Tier lets you test the app on your own chats —
              limited to 3 AI providers and 5 conversations per download, so you can get
              comfortable before you pay. A one-time $24 purchase unlocks Pro: all 8 providers
              and unlimited downloads.
            </p>

            <div className="mt-8 flex flex-col items-start gap-1">
              <div className="flex items-baseline gap-2">
                <span className="font-heading text-3xl md:text-4xl font-bold tracking-tight text-foreground">$24<span className="tr-usd">USD</span></span>
                <span className="font-body text-sm text-muted-foreground">· one-time · lifetime license</span>
              </div>
              <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary mt-1 font-semibold">discounted launch price</span>
            </div>

            <div className="mt-8 flex flex-col sm:flex-row gap-4">
              <a
                href="/buy/"
                data-tr-buy="true"
                aria-label="Buy TotalRecalls — $24 USD — discounted launch price"
                className="inline-flex flex-col items-center justify-center gap-0.5 bg-primary text-white px-7 py-3.5 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:opacity-90 transition-opacity shadow-sm w-full sm:w-auto"
                style={{ maxWidth: 300 }}
              >
                <span className="whitespace-nowrap">Buy TotalRecalls — $24<span className="tr-usd">USD</span></span>
                <span className="text-[10px] font-normal opacity-85 tracking-[0.12em] whitespace-nowrap">discounted launch price</span>
              </a>
              <a
                href="/download/"
                aria-label="Try the Free Tier"
                className="inline-flex items-center justify-center gap-2 border border-border bg-card text-foreground px-6 py-3.5 font-mono text-[12px] uppercase tracking-[0.14em] font-medium hover:bg-muted/50 transition-colors"
              >
                Try it free
              </a>
            </div>

            {/* Vertical Provider List */}
            <div className="mt-8 font-mono text-[11px] text-muted-foreground">
              <span className="font-semibold text-foreground uppercase tracking-wider block mb-2.5">Includes providers:</span>
              <ul className="space-y-1.5 border-l-2 border-primary/30 pl-3">
                {PROVIDERS.map((p) => (
                  <li key={p} className="text-foreground/90 font-medium">{p}</li>
                ))}
              </ul>
              <span className="block mt-3 text-[10.5px] opacity-70">Version v1.0.0</span>
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
