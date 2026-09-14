import { Plus } from "lucide-react";

const FAQS = [
  {
    q: "Which providers does it work with?",
    a: "Eight: ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen. One app downloads your conversations from all of them.",
  },
  {
    q: "What's the refund policy?",
    a: <>We don't run a standard refund policy — we have better. A Free Tier is available so that you can test-drive the app before committing to buy it: download it and test it to your liking. The Free Tier has limited features — the goal is to make you comfortable with the product — so downloads are limited to only 3 providers and to only 5 conversations per download. The Pro version, a one-time launch purchase price of $24<span className="tr-usd">USD</span>, unlocks all the features, expanding your downloads to the top 8 AI providers without limit on the number of conversations you can download. If you do have a refund request, contact us and we'll handle it on a case-by-case basis. Your statutory consumer rights — including the right of cancellation for online purchases that Quebec consumers enjoy — always apply and are never excluded.</>,
  },
  {
    q: "Is there a subscription?",
    a: <>No. It's a one-time $24<span className="tr-usd">USD</span> purchase — discounted launch price. You pay once and keep receiving free updates to the core app for the life of the product. New features (add-ons) are separate purchases; add-ons you own keep getting updates.</>,
  },
  {
    q: "Do I need to create an account?",
    a: "No. There's no account and no sign-up. Everything is saved locally as files on your own machine.",
  },
  {
    q: "Is my data uploaded anywhere?",
    a: "No. It runs 100% locally and never sends your conversations to a server.",
  },
  {
    q: "Which platforms are supported?",
    a: "Windows 10 and 11 today. The app is a portable desktop tool you download and run locally. Developing an application for Linux and Apple (macOS) is in the works.",
  },
  {
    q: "Do I get updates?",
    a: "Yes. The core app receives free updates for the life of the product — check the Release Notes on our website. New features (add-ons) will be developed on an ongoing basis and made available as separate purchases as we expand the product.",
  },
];

export default function FaqSection() {
  return (
    <section id="faq" className="border-t border-border bg-background text-foreground">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-16 md:py-24">
        <div className="grid lg:grid-cols-[1fr_1.6fr] gap-12 items-start">
          {/* Left heading */}
          <div>
            <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">FAQ</span>
            <h2 className="font-heading text-3xl md:text-4xl font-bold tracking-tight mt-4">
              Questions, answered.
            </h2>
            <p className="font-body text-muted-foreground text-[15.5px] leading-relaxed mt-4 max-w-sm">
              A few things people ask before they download. Still curious? There's more on the FAQ
              page.
            </p>
            <a
              href="/faq/"
              className="inline-flex items-center gap-2 text-primary font-mono text-[12px] uppercase tracking-[0.14em] font-medium mt-6 hover:opacity-80 transition-opacity"
            >
              See all questions →
            </a>
          </div>

          {/* Right accordion */}
          <div className="border-t border-border">
            {FAQS.map((f) => (
              <details key={f.q} className="group border-b border-border py-4">
                <summary className="flex items-center justify-between gap-4 cursor-pointer list-none">
                  <span className="font-heading text-[16.5px] font-semibold text-foreground">{f.q}</span>
                  <Plus className="w-4 h-4 text-primary shrink-0 transition-transform group-open:rotate-45" />
                </summary>
                <p className="font-body text-muted-foreground text-[15px] leading-relaxed mt-3 max-w-2xl">{f.a}</p>
              </details>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
