import React from "react";
import { Container, Section, Eyebrow, Btn, Chip } from "./ui";

const PROVIDERS_LIST = [
  { name: "ChatGPT", pro: false },
  { name: "Claude", pro: false },
  { name: "Perplexity", pro: false },
  { name: "Gemini", pro: true },
  { name: "Grok", pro: true },
  { name: "DeepSeek", pro: true },
  { name: "Mistral", pro: true },
  { name: "Qwen", pro: true },
];

export default function HowItWorks() {
  return (
    <Section id="resolution" className="bg-tr-graphite">
      <Container>
        <Eyebrow>How it works</Eyebrow>

        <h2 className="mt-3 max-w-[680px] font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
          Five steps from scattered chats<br />
          to one local folder onto your C:\ drive.
        </h2>

        <p className="mt-4 max-w-[780px] font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-mist">
          Setup takes a few minutes. After that, each download is a pick and a&nbsp;click.
        </p>

        {/* Step cards — Obsidian on the Graphite band, no hover */}
        <div className="mt-12 grid sm:grid-cols-2 lg:grid-cols-5 gap-6 items-stretch">
          {/* Box 01 */}
          <div className="flex flex-col rounded-card border border-tr-slate bg-tr-obsidian p-6">
            <span className="font-mono text-[14px] font-medium text-tr-steel">01</span>
            <h3 className="mt-3 font-heading text-[20px] md:text-[24px] font-semibold leading-[1.25] text-tr-paper">
              Buy once
            </h3>
            <p className="mt-2 font-body text-[14.5px] leading-[1.6] text-tr-mist">
              $24, one time, at the launch price. Your license key arrives by email.
            </p>
            <p className="mt-3 font-body text-[14.5px] leading-[1.6] text-tr-mist">
              Prefer to test first? Skip this step and start on the Free Tier.
            </p>
            <div className="mt-auto flex flex-wrap gap-1.5 pt-4">
              <a
                href="/#pricing"
                className="inline-flex items-center gap-1.5 whitespace-nowrap rounded-chip px-2 py-1 font-mono text-[12px] font-medium uppercase tracking-[0.02em] bg-tr-amber text-tr-on-amber hover:bg-tr-amber-hover transition-colors"
              >
                $24
              </a>
              <Chip tone="slate">One-time</Chip>
              <Chip tone="slate">No subscription</Chip>
            </div>
          </div>

          {/* Box 02 */}
          <div className="flex flex-col rounded-card border border-tr-slate bg-tr-obsidian p-6">
            <span className="font-mono text-[14px] font-medium text-tr-steel">02</span>
            <h3 className="mt-3 font-heading text-[20px] md:text-[24px] font-semibold leading-[1.25] text-tr-paper">
              Install
            </h3>
            <p className="mt-2 font-body text-[14.5px] leading-[1.6] text-tr-mist">
              Unzip the download and run TotalRecalls on your Windows PC.
            </p>
            <p className="mt-3 font-body text-[14.5px] leading-[1.6] text-tr-mist">
              You don&apos;t create an account or sign up for anything.
            </p>
            <div className="mt-auto flex flex-wrap gap-1.5 pt-4">
              <Chip tone="slate">Windows 10/11</Chip>
            </div>
          </div>

          {/* Box 03 */}
          <div className="flex flex-col rounded-card border border-tr-slate bg-tr-obsidian p-6">
            <span className="font-mono text-[14px] font-medium text-tr-steel">03</span>
            <h3 className="mt-3 font-heading text-[20px] md:text-[24px] font-semibold leading-[1.25] text-tr-paper">
              Pick your providers
            </h3>
            <ul className="mt-2 space-y-1 font-body text-[14px] leading-[1.5] text-tr-mist">
              {PROVIDERS_LIST.map((p) => (
                <li key={p.name} className="flex items-center gap-2">
                  <span className="text-tr-steel leading-none">•</span> {p.name}{p.pro ? "*" : ""}
                </li>
              ))}
            </ul>
            <p className="mt-3 font-body text-[14px] leading-[1.6] text-tr-mist">
              You sign in to each provider locally, inside the app.
            </p>
            <p className="mt-2 font-mono text-[11px] text-tr-dust">
              * with Downloader Pro
            </p>
            <div className="mt-auto pt-3">
              <a href="/providers/" className="text-[12px] font-mono font-medium text-tr-steel hover:text-tr-amber transition-colors inline-flex items-center gap-1">
                See all 8 supported providers &rarr;
              </a>
              <div className="flex flex-wrap gap-1.5 pt-2">
                <Chip tone="slate">8 providers</Chip>
                <Chip tone="slate">Local sign-in</Chip>
              </div>
            </div>
          </div>

          {/* Box 04 */}
          <div className="flex flex-col rounded-card border border-tr-slate bg-tr-obsidian p-6">
            <span className="font-mono text-[14px] font-medium text-tr-steel">04</span>
            <h3 className="mt-3 font-heading text-[20px] md:text-[24px] font-semibold leading-[1.25] text-tr-paper">
              Download
            </h3>
            <p className="mt-2 font-body text-[14.5px] leading-[1.6] text-tr-mist">
              Your chats save as Markdown and JSON files on your PC.
            </p>
            <p className="mt-3 font-body text-[14.5px] leading-[1.6] text-tr-mist">
              Open them anywhere, offline.
            </p>
            <div className="mt-auto pt-3">
              <a href="/library/" className="text-[12px] font-mono font-medium text-tr-steel hover:text-tr-amber transition-colors inline-flex items-center gap-1">
                Explore Library folder format &rarr;
              </a>
              <div className="flex flex-wrap gap-1.5 pt-2">
                <Chip tone="slate">.md + .json</Chip>
                <Chip tone="local">
                  <span className="text-[10px] leading-none">●</span> Saved locally
                </Chip>
              </div>
            </div>
          </div>

          {/* Box 05 */}
          <div className="flex flex-col rounded-card border border-tr-slate bg-tr-obsidian p-6">
            <span className="font-mono text-[14px] font-medium text-tr-steel">05</span>
            <h3 className="mt-3 font-heading text-[20px] md:text-[24px] font-semibold leading-[1.25] text-tr-paper">
              Search (regular)
            </h3>
            <p className="mt-2 font-body text-[14px] leading-[1.55] text-tr-mist">
              Windows Explorer, Notion, Obsidian and others.
            </p>
            <hr className="my-3.5 border-tr-slate" />
            <h4 className="font-heading text-[16px] md:text-[18px] font-semibold leading-[1.25] text-tr-paper">
              Smart Search Engine (SSE) add on
            </h4>
            <p className="mt-2 font-body text-[14px] leading-[1.55] text-tr-mist">
              Ask via chat in plain English to find any word, topic, conversation across all 8 providers.
            </p>
            <div className="mt-auto flex flex-wrap gap-1.5 pt-4">
              <a
                href="/#pricing"
                className="inline-flex items-center gap-1.5 whitespace-nowrap rounded-chip px-2 py-1 font-mono text-[12px] font-medium uppercase tracking-[0.02em] bg-tr-amber text-tr-on-amber hover:bg-tr-amber-hover transition-colors"
              >
                $29
              </a>
              <Chip tone="slate">Add-on</Chip>
              <Chip tone="slate">Smart Search Engine (SSE)</Chip>
            </div>
          </div>
        </div>

        {/* Microsoft Store certified + close */}
        <p className="mt-8 font-body text-[14px] leading-[1.5] text-tr-dust">
          Certified and distributed through the official <a href="https://apps.microsoft.com/detail/9PP1KKD5X2D6" className="text-tr-steel transition-colors hover:text-tr-paper" target="_blank" rel="noopener noreferrer">Microsoft Store</a> — zero warnings, one-click install.
        </p>

        <p className="mt-8 font-body text-[16px] leading-[1.6] text-tr-paper">
          Start free with ChatGPT, Claude, and Perplexity. Upgrade to Pro when you want all eight.
        </p>

        <div className="mt-4 flex flex-col items-start gap-3">
          <Btn href="/download/">Download free</Btn>
          <Btn href="#pricing" variant="tertiary">Compare Free and Pro ↓</Btn>
        </div>
      </Container>
    </Section>
  );
}
