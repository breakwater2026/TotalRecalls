import React from "react";
import { Container, Section, Eyebrow, Btn, Chip, LocalChip } from "./ui";

const STEPS = [
  {
    n: "01",
    title: "Buy once",
    body: "Check out for $24, one time, at the launch price. Your license key arrives by email. Prefer to test first? Skip this step and start on the Free Tier.",
    chips: [
      { text: "$24", tone: "mist" },
      { text: "One-time", tone: "slate" },
      { text: "No subscription", tone: "slate" },
    ],
  },
  {
    n: "02",
    title: "Install",
    body: "Unzip the download and run TotalRecalls on your Windows PC. You don't create an account or sign up for anything.",
    chips: [
      { text: "Windows 10/11", tone: "slate" },
      { text: "No account", tone: "slate" },
    ],
  },
  {
    n: "03",
    title: "Pick your providers",
    body: "Choose from ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen. You sign in to each provider locally, inside the app.",
    chips: [
      { text: "8 providers", tone: "slate" },
      { text: "Local sign-in", tone: "slate" },
    ],
  },
  {
    n: "04",
    title: "Download",
    body: "Your chats land in your Library folder as Markdown and JSON files. Search them, open them offline, and keep them.",
    chips: [
      { text: ".md + .json", tone: "slate" },
      { text: "Saved locally", tone: "local" },
    ],
  },
];

const PROVIDERS = [
  { name: "ChatGPT", id: "OAI-001" },
  { name: "Claude", id: "ANT-002" },
  { name: "Perplexity", id: "PPL-003" },
  { name: "Gemini", id: "GEM-004" },
  { name: "Grok", id: "GRK-005" },
  { name: "DeepSeek", id: "DSK-006" },
  { name: "Mistral", id: "MST-007" },
  { name: "Qwen", id: "QWN-008" },
];

export default function HowItWorks() {
  return (
    <Section id="resolution" className="bg-tr-graphite">
      <Container>
        <Eyebrow>How it works</Eyebrow>

        <h2 className="mt-3 max-w-[680px] font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
          Four steps from scattered chats to one local folder.
        </h2>

        <p className="mt-4 max-w-[680px] font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-mist">
          Setup takes a few minutes. After that, each download is a pick and a click.
        </p>

        {/* Step cards — Obsidian on the Graphite band, no hover */}
        <div className="mt-12 grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {STEPS.map((s) => (
            <div key={s.n} className="flex flex-col rounded-card border border-tr-slate bg-tr-obsidian p-6">
              <span className="font-mono text-[14px] font-medium text-tr-steel">{s.n}</span>
              <h3 className="mt-3 font-heading text-[20px] md:text-[24px] font-semibold leading-[1.25] text-tr-paper">
                {s.title}
              </h3>
              <p className="mt-2 font-body text-[16px] leading-[1.6] text-tr-mist">{s.body}</p>
              <div className="mt-auto flex flex-wrap gap-1.5 pt-4">
                {s.chips.map((c) => (
                  <Chip key={c.text} tone={c.tone}>
                    {c.text === "Saved locally" && <span className="text-[10px] leading-none">●</span>}
                    {c.text}
                  </Chip>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Provider-to-folder diagram — one Obsidian panel */}
        <div className="mt-12 rounded-card border border-tr-slate bg-tr-obsidian p-6 md:p-12">
          <div className="grid lg:grid-cols-[1fr_260px_1fr] gap-6 md:gap-10 items-center">
            {/* Left: provider nodes */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 lg:grid-cols-1 min-w-0">
              {PROVIDERS.map((p) => (
                <div key={p.id} className="flex items-center justify-between gap-2 rounded-chip border border-tr-slate px-3 py-2">
                  <span className="font-body text-[14px] font-medium text-tr-paper">{p.name}</span>
                  <span className="font-mono text-[12px] text-tr-steel">{p.id}</span>
                </div>
              ))}
            </div>

            {/* Middle: connectors */}
            <div className="hidden lg:flex flex-col items-center gap-1">
              <span className="font-mono text-[12px] text-tr-dust">direct</span>
              <svg width="10" height="320" viewBox="0 0 10 320" aria-hidden="true">
                <line x1="5" y1="0" x2="5" y2="140" stroke="#7A8FA6" strokeWidth="1.5" />
                <line x1="5" y1="148" x2="5" y2="300" stroke="#7A8FA6" strokeWidth="1.5" strokeDasharray="4 4" />
                <circle cx="5" cy="312" r="5" fill="#7A8FA6" />
              </svg>
              <span className="font-mono text-[12px] text-tr-dust">takeout → md</span>
            </div>
            <div className="flex lg:hidden justify-center">
              <svg width="10" height="64" viewBox="0 0 10 64" aria-hidden="true">
                <line x1="5" y1="0" x2="5" y2="52" stroke="#7A8FA6" strokeWidth="1.5" />
                <path d="M1 48 L5 58 L9 48 Z" fill="#7A8FA6" />
              </svg>
            </div>

            {/* Right: Library folder panel */}
            <div className="rounded-card border border-tr-slate bg-tr-graphite p-4 min-w-0">
              <p className="font-mono text-[13px] text-tr-steel break-all select-all md:text-[14px]">
                C:\TotalRecalls\Library\
              </p>
              <pre className="mt-2.5 overflow-x-auto font-mono text-[13px] leading-relaxed text-tr-steel select-all md:text-[14px]">{`├── chatgpt\
├── claude\
├── perplexity\
├── gemini\
└── …`}</pre>
              <div className="mt-4 flex flex-wrap items-center gap-1.5">
                <span className="rounded-chip border border-tr-slate px-2 py-1 font-mono text-[12px] font-medium uppercase tracking-[0.02em] text-tr-steel">.md</span>
                <span className="rounded-chip border border-tr-slate px-2 py-1 font-mono text-[12px] font-medium uppercase tracking-[0.02em] text-tr-steel">.json</span>
                <LocalChip />
              </div>
            </div>
          </div>

          <p className="mt-6 text-center font-body text-[14px] text-tr-dust">
            Eight sources. One folder on your own drive.
          </p>
        </div>

        {/* SmartScreen helper + close */}
        <p className="mt-8 font-body text-[14px] leading-[1.5] text-tr-dust">
          First launch may show a Windows SmartScreen prompt.{" "}
          <a href="/microsoft-warning/" className="text-tr-steel transition-colors hover:text-tr-paper">
            Here&apos;s why
          </a>
          , and how to continue.
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
