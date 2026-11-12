import React, { useState, useRef } from "react";
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

export default function DemoPage() {
  const [isPlaying, setIsPlaying] = useState(false);
  const videoRef = useRef(null);

  const handlePlay = () => {
    if (videoRef.current) {
      videoRef.current.play();
    }
  };
  return (
    <Section pad="hero" className="bg-tr-graphite">
      <Container>
        <nav aria-label="Breadcrumb" className="mb-3">
          <span className="font-mono text-[11px] uppercase tracking-[0.14em] text-tr-steel">
            <a href="/" className="hover:text-tr-amber transition-colors">Home</a>
            {" / "}
            <span className="text-tr-paper font-medium">Demo</span>
          </span>
        </nav>

        <h1 className="mt-3 max-w-[850px] font-heading text-[32px] md:text-[44px] font-bold leading-[1.15] tracking-[-0.01em] text-tr-paper">
          Watch TotalRecalls (Pro + SSE) in&nbsp;action.
        </h1>

        <p className="mt-4 max-w-[850px] font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-mist">
          Five steps from scattered chats to one local folder. Watch how conversations download from the app directly to your drive.
        </p>

        {/* Step cards — Obsidian on the Graphite band */}
        <div className="mt-12 grid sm:grid-cols-2 lg:grid-cols-5 gap-6 items-stretch">
          {/* Box 01 */}
          <div className="flex flex-col rounded-card border border-tr-slate bg-tr-obsidian p-6">
            <span className="font-mono text-[14px] font-medium text-tr-steel">01</span>
            <h2 className="mt-3 font-heading text-[20px] md:text-[24px] font-semibold leading-[1.25] text-tr-paper">
              Buy once
            </h2>
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
            <h2 className="mt-3 font-heading text-[20px] md:text-[24px] font-semibold leading-[1.25] text-tr-paper">
              Install
            </h2>
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
            <h2 className="mt-3 font-heading text-[20px] md:text-[24px] font-semibold leading-[1.25] text-tr-paper">
              Pick your providers
            </h2>
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
            <div className="mt-auto flex flex-wrap gap-1.5 pt-4">
              <Chip tone="slate">8 providers</Chip>
              <Chip tone="slate">Local sign-in</Chip>
            </div>
          </div>

          {/* Box 04 */}
          <div className="flex flex-col rounded-card border border-tr-slate bg-tr-obsidian p-6">
            <span className="font-mono text-[14px] font-medium text-tr-steel">04</span>
            <h2 className="mt-3 font-heading text-[20px] md:text-[24px] font-semibold leading-[1.25] text-tr-paper">
              Download
            </h2>
            <p className="mt-2 font-body text-[14.5px] leading-[1.6] text-tr-mist">
              Your chats save as Markdown and JSON files on your PC.
            </p>
            <p className="mt-3 font-body text-[14.5px] leading-[1.6] text-tr-mist">
              Open them anywhere, offline.
            </p>
            <div className="mt-auto flex flex-wrap gap-1.5 pt-4">
              <Chip tone="slate">.md + .json</Chip>
              <Chip tone="local">
                <span className="text-[10px] leading-none">●</span> Saved locally
              </Chip>
            </div>
          </div>

          {/* Box 05 */}
          <div className="flex flex-col rounded-card border border-tr-slate bg-tr-obsidian p-6">
            <span className="font-mono text-[14px] font-medium text-tr-steel">05</span>
            <h2 className="mt-3 font-heading text-[20px] md:text-[24px] font-semibold leading-[1.25] text-tr-paper">
              Search (regular)
            </h2>
            <p className="mt-2 font-body text-[14px] leading-[1.55] text-tr-mist">
              Windows Explorer, Notion, Obsidian and others.
            </p>
            <hr className="my-3.5 border-tr-slate" />
            <h3 className="font-heading text-[16px] md:text-[18px] font-semibold leading-[1.25] text-tr-paper">
              Smart Search Engine (SSE) add on
            </h3>
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

        {/* Demo Video Section — replaces the graphical representation */}
        <div className="mt-12 rounded-card border border-tr-slate bg-tr-obsidian p-6 md:p-12">
          <div className="max-w-[960px] mx-auto">
            <div className="group relative overflow-hidden rounded-xl border border-tr-slate bg-tr-graphite">
              <video
                ref={videoRef}
                className="aspect-video w-full rounded-lg border border-tr-slate/60 bg-black block"
                src="https://demo-video.totalrecalls.app/TR_website_chatgpt.mp4"
                poster="/demo/poster_chatgpt.png"
                controls
                preload="metadata"
                playsInline
                title="TotalRecalls demo walkthrough"
                onPlay={() => setIsPlaying(true)}
                onPause={() => setIsPlaying(false)}
                onEnded={() => setIsPlaying(false)}
              />
              {!isPlaying && (
                <button
                  type="button"
                  onClick={handlePlay}
                  aria-label="Play TotalRecalls demo video"
                  className="absolute inset-0 flex flex-col items-center justify-center bg-black/40 backdrop-blur-[2px] transition-all hover:bg-black/30 cursor-pointer"
                >
                  <span className="flex h-16 w-16 md:h-20 md:w-20 items-center justify-center rounded-full bg-tr-amber text-tr-on-amber shadow-2xl transition-transform transform group-hover:scale-110">
                    <svg className="ml-1 h-8 w-8 md:h-10 md:w-10 fill-current" viewBox="0 0 24 24">
                      <path d="M8 5v14l11-7z" />
                    </svg>
                  </span>
                  <span className="mt-4 rounded-full bg-tr-obsidian/90 px-4 py-1.5 font-mono text-[13px] font-semibold tracking-wider text-tr-paper uppercase border border-tr-slate shadow-lg">
                    Play Demo Video (6:03 · Narration &amp; Music)
                  </span>
                </button>
              )}
            </div>
            <p className="mt-4 text-center font-body text-[14px] text-tr-dust">
              A real screen recording of the owner&apos;s own 8,135 conversations spanning over two years downloaded via the app into Markdown and JSON files in your local C:\ drive Library&nbsp;folder.
            </p>
          </div>
        </div>

        {/* Store trust beat */}
        <p className="mt-8 font-body text-[14px] leading-[1.5] text-tr-dust">
          Available on the official <a href="https://apps.microsoft.com/detail/9PP1KKD5X2D6" className="text-tr-steel transition-colors hover:text-tr-paper" target="_blank" rel="noopener noreferrer">Microsoft Store</a> — clean, verified, one-click install for Windows 10 and 11.
        </p>

        <p className="mt-8 font-body text-[16px] leading-[1.6] text-tr-paper">
          Start free with ChatGPT, Claude, and Perplexity. Upgrade to Pro when you want all eight.
        </p>

        <div className="mt-4 flex flex-col sm:flex-row items-start sm:items-center gap-4">
          <Btn href="/download/" large>Download free</Btn>
          <Btn href="/#pricing" variant="secondary" large>Compare Free and Pro</Btn>
        </div>
      </Container>
    </Section>
  );
}
