import React from "react";
import { Check } from "lucide-react";
import { Container, Section, Eyebrow, Btn, Chip } from "./ui";

export default function Pricing() {
  return (
    <Section id="pricing" className="bg-tr-graphite">
      <Container>
        <Eyebrow>Pricing</Eyebrow>

        <h2 className="mt-3 max-w-[680px] font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
          Start free. Pay once when you want all eight.
        </h2>

        <p className="mt-4 max-w-[680px] font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-mist">
          Test TotalRecalls on your own chats before you spend anything. When you're ready,
          one payment unlocks every provider. No subscription.
        </p>

        <div className="mt-12 grid lg:grid-cols-2 gap-6 lg:gap-8 items-stretch">
          {/* Free Tier */}
          <div className="flex flex-col rounded-card border border-tr-slate bg-tr-obsidian p-6 md:p-8">
            <div className="flex flex-wrap items-center gap-2">
              <Chip tone="mist">Free</Chip>
            </div>
            <div className="mt-6 flex items-baseline gap-2">
              <span className="font-heading text-[40px] md:text-[48px] font-bold tracking-[-0.02em] text-tr-paper tabular-nums">$0</span>
            </div>
            <p className="mt-2 font-body text-[16px] leading-[1.6] text-tr-mist">
              Try the app on your real conversations.
            </p>

            <ul className="mt-6 space-y-3">
              {[
                "ChatGPT, Claude, and Perplexity",
                "5 conversations per download",
                "Markdown and JSON files",
                "Saved locally to C:\\TotalRecalls\\Library\\",
              ].map((f) => (
                <li key={f} className="flex items-start gap-3">
                  <Check className="mt-0.5 h-4 w-4 shrink-0 text-tr-green" strokeWidth={2.5} />
                  <span className="font-body text-[15px] leading-[1.5] text-tr-mist">{f}</span>
                </li>
              ))}
              {["Gemini, Grok, DeepSeek, Mistral, and Qwen", "Unlimited downloads"].map((f) => (
                <li key={f} className="flex items-start gap-3">
                  <span className="mt-0.5 w-4 shrink-0 text-center font-body text-[15px] leading-[1.5] text-tr-dust">—</span>
                  <span className="font-body text-[15px] leading-[1.5] text-tr-dust">{f}</span>
                </li>
              ))}
            </ul>

            <div className="mt-8 pt-2">
              <Btn href="/download/" variant="secondary" className="w-full sm:w-auto">Download free</Btn>
            </div>
          </div>

          {/* Pro — 1px Amber border, the section's only Amber button */}
          <div className="flex flex-col rounded-card border border-tr-amber bg-tr-obsidian p-6 md:p-8">
            <div className="flex flex-wrap items-center gap-2">
              <Chip tone="amber">Pro</Chip>
              <Chip tone="slate">Launch price</Chip>
            </div>
            <div className="mt-6 flex items-baseline gap-2">
              <span className="font-heading text-[40px] md:text-[48px] font-bold tracking-[-0.02em] text-tr-amber tabular-nums">$24</span>
              <span className="font-body text-[16px] text-tr-mist">one-time</span>
            </div>
            <p className="mt-2 font-body text-[16px] leading-[1.6] text-tr-mist">
              Every provider. Every conversation. No subscription.
            </p>

            <ul className="mt-6 space-y-3">
              {[
                "All 8 providers: ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen",
                "Unlimited downloads",
                "Markdown and JSON files, saved locally",
                "Up to 3 device activations",
                "Free updates to the core app",
                "License key delivered by email",
              ].map((f) => (
                <li key={f} className="flex items-start gap-3">
                  <Check className="mt-0.5 h-4 w-4 shrink-0 text-tr-green" strokeWidth={2.5} />
                  <span className="font-body text-[15px] leading-[1.5] text-tr-mist">{f}</span>
                </li>
              ))}
            </ul>

            <div className="mt-8 pt-2">
              <Btn href="/buy/" className="w-full sm:w-auto">Get Pro — $24</Btn>
            </div>
          </div>
        </div>

        {/* TotalRecalls Search add-on strip */}
        <div className="mt-12 rounded-card border border-tr-slate bg-tr-graphite p-8 md:p-12">
          <div className="grid lg:grid-cols-2 gap-8 md:gap-12 items-start">
            <div className="max-w-[680px]">
              <div className="flex flex-wrap items-center gap-2 mb-3">
                <Chip tone="slate">Add-on for Pro</Chip>
                <span className="font-mono text-[14px] font-medium text-tr-dust tabular-nums">$19 one-time</span>
                <span className="font-mono text-[14px] text-tr-dust">· launch price (regular $39)</span>
              </div>
              <h3 className="mt-0 font-heading text-[24px] md:text-[28px] font-semibold leading-[1.2] text-tr-paper">Then make it searchable.</h3>
              <p className="mt-4 font-body text-[16px] leading-[1.6] text-tr-mist">
                Ask in plain English and find any conversation, from any of your eight providers.
              </p>
              <ul className="mt-6 space-y-3">
                {[
                  "Finds passages by meaning, not just exact words",
                  "Searches all eight providers at once",
                  "Opens the original Markdown or JSON file",
                  "Runs on your PC. Nothing you save is uploaded",
                  "Keeps itself up to date",
                ].map((b, i) => (
                  <li key={i} className="flex items-start gap-3">
                    <Check className="mt-0.5 h-4 w-4 shrink-0 text-tr-green" strokeWidth={2.5} />
                    <span className="font-body text-[15px] leading-[1.5] text-tr-mist">{b}</span>
                  </li>
                ))}
              </ul>
              <div className="mt-8">
                <Btn href="/buy/" className="w-full sm:w-auto">Add Search to Pro</Btn>
              </div>
              <p className="mt-5 font-body text-[15px] leading-[1.6] text-tr-mist">
                Or get Pro + Search together for $39. Already own Pro? Early-buyer price $14 for 30 days after launch.
              </p>
              <p className="mt-5 font-body text-[13px] leading-[1.5] text-tr-dust">
                Requires TotalRecalls Pro. Windows 10 and 11. About 8 GB RAM and 2 GB free disk. One-time internet connection to download the search model.
              </p>
            </div>
          </div>
        </div>

        <div className="mt-10 text-center">
          <p className="mx-auto max-w-[680px] font-body text-[14px] leading-[1.5] text-tr-dust">
            Windows 10 and 11. $24 is a discounted launch price. Add-ons, like Search, are sold
            separately. See below. Your core app updates stay free.
          </p>
          <div className="mt-5 flex flex-wrap justify-center gap-2">
            {["One-time", "No subscription", "No account", "Windows 10/11"].map((t) => (
              <Chip key={t} tone="slate">{t}</Chip>
            ))}
          </div>
        </div>
      </Container>
    </Section>
  );
}
