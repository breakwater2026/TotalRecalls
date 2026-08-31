import { Plus } from "lucide-react";

const FAQS = [
  {
    q: "Which providers does it work with?",
    a: "Eight: ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen. One app exports your conversations from all of them.",
  },
  {
    q: "Is there a subscription?",
    a: "No. It's a one-time $24 purchase — discounted launch price. You pay once and keep every future update.",
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
    q: "What's the refund policy?",
    a: "There isn't one — and you won't need it. Download it free first, run it on your own chats, and only pay if it's right for you.",
  },
  {
    q: "Which platforms are supported?",
    a: "Windows 10 and 11. The app is a portable desktop tool you download and run locally.",
  },
  {
    q: "Do I get updates?",
    a: "Yes. Every future update is included in the one-time purchase.",
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
