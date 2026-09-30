import React from "react";
import { Plus } from "lucide-react";
import { Container, Section, Eyebrow } from "./ui";

const FAQS = [
  {
    q: "Which providers does it work with?",
    a: "Eight: ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen. One app downloads your conversations from all of them.",
  },
  {
    q: "What's the refund policy?",
    a: "We don't run a standard refund policy — we have better. A Free Tier is available so that you can test-drive the app before committing to buy it: download it and test it to your liking. The Free Tier has limited features — the goal is to make you comfortable with the product — so downloads are limited to only 3 providers and to only 5 conversations per download. The Pro version, a one-time launch purchase price of $24 USD, unlocks all the features, expanding your downloads to the top 8 AI providers without limit on the number of conversations you can download. If you do have a refund request, contact us and we'll handle it on a case-by-case basis. Your statutory consumer rights — including the right of cancellation for online purchases that Quebec consumers enjoy — always apply and are never excluded.",
  },
  {
    q: "Is there a subscription?",
    a: "No. It's a one-time $24 USD purchase — discounted launch price. You pay once and keep receiving free updates to the core app for the life of the product. New features (add-ons) are separate purchases; add-ons you own keep getting updates.",
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

export default function Faq() {
  return (
    <Section id="faq" className="border-t border-tr-slate bg-tr-obsidian">
      <Container>
        <div className="grid lg:grid-cols-[1fr_1.6fr] gap-12 items-start">
          <div>
            <Eyebrow>FAQ</Eyebrow>
            <h2 className="mt-3 font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
              The last few objections, answered.
            </h2>
            <p className="mt-4 max-w-sm font-body text-[16px] leading-[1.6] text-tr-mist">
              A few things people ask before they download. Still curious? There&apos;s more
              on the FAQ page.
            </p>
            <a
              href="/faq/"
              className="mt-6 inline-flex items-center gap-2 font-body text-[15px] font-semibold text-tr-steel transition-colors hover:text-tr-paper"
            >
              See all questions →
            </a>
          </div>

          <div className="border-t border-tr-slate">
            {FAQS.map((f) => (
              <details key={f.q} className="group border-b border-tr-slate py-4">
                <summary className="flex items-center justify-between gap-4 cursor-pointer list-none">
                  <span className="font-heading text-[16.5px] font-semibold text-tr-paper">{f.q}</span>
                  <Plus className="w-4 h-4 text-tr-steel shrink-0 transition-transform group-open:rotate-45" />
                </summary>
                <p className="mt-3 max-w-2xl font-body text-[15px] leading-[1.6] text-tr-mist">{f.a}</p>
              </details>
            ))}
          </div>
        </div>
      </Container>
    </Section>
  );
}
