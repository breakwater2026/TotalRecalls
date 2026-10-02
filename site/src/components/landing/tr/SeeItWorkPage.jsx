import React, { useRef } from "react";
import { Play, ChevronDown } from "lucide-react";
import { Container, Section, Eyebrow, Btn, Chip, EvidenceStrip, LocalChip } from "./ui";

/* ============================================================================
 * /see-it-work/ — "See It Work" (Jasper rewrite, tr/ design system).
 * Copy + spec from: Marketing/Jasper/Website Rewrite/See It Work Page.md
 *
 * DEMO VIDEO NOTE (placeholder state):
 *   The two See-It-Work videos (the 60s ChatGPT demo + the Pro upgrade
 *   walkthrough) are still in production ("heavier load"). Until they land,
 *   the demo slot keeps the currently-embedded walkthrough:
 *     https://video.totalrecalls.app/TR_website_claude_hero.mp4
 *   Swap the <video src> below (and the poster) when the ChatGPT cut ships.
 * ========================================================================== */

const DEMO_SRC = "https://video.totalrecalls.app/TR_website_claude_hero.mp4";
const POSTER = "/demo/poster.png";
const RESULT_IMG = "/demo/result.png";

const STEPS = [
  { t: "0:00", title: "Open the app", body: "TotalRecalls runs from its own folder on your PC. There's no installer and no TotalRecalls account." },
  { t: "0:08", title: "Choose your provider", body: "The provider list shows what your tier includes. ChatGPT is part of the Free Tier." },
  { t: "0:15", title: "Sign in", body: "You sign in inside the app, on your own PC. Your conversations aren't sent to our servers." },
  { t: "0:27", title: "Pick a conversation", body: "Your history loads as a list. Select the conversation you want to keep." },
  { t: "0:36", title: "Download", body: "TotalRecalls saves the conversation. A confirmation shows exactly where the files went." },
  { t: "0:45", title: "Open the Library folder", body: "The chat sits in the provider subfolder as one Markdown file and one JSON file. The video ends with the file open." },
];

function Step({ t, title, body }) {
  return (
    <div className="flex flex-col gap-2 py-5 md:flex-row md:gap-6">
      <code className="shrink-0 font-mono text-[14px] font-medium text-tr-steel md:pt-0.5 md:text-right md:w-[72px]">{t}</code>
      <div className="min-w-0 flex-1">
        <h3 className="font-heading text-[18px] font-semibold text-tr-paper">{title}</h3>
        <p className="mt-1.5 font-body text-[16px] leading-[1.6] text-tr-mist">{body}</p>
      </div>
    </div>
  );
}

function MarkerNote({ n, title, body }) {
  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center gap-2.5">
        <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-tr-steel font-mono text-[12px] font-medium text-tr-obsidian">{n}</span>
        <h3 className="font-heading text-[16px] font-semibold text-tr-paper">{title}</h3>
      </div>
      <p className="pl-8.5 font-body text-[14px] leading-[1.6] text-tr-mist">{body}</p>
    </div>
  );
}

export default function SeeItWorkPage() {
  const videoRef = useRef(null);

  return (
    <>
      {/* 1. Hero */}
      <Section pad="hero" className="bg-tr-obsidian">
        <Container>
          <div className="max-w-[680px]">
            <Eyebrow mono>See It Work</Eyebrow>
            <h1 className="mt-3 font-heading text-[34px] font-bold leading-[1.1] tracking-[-0.02em] text-tr-paper md:text-[48px]">
              Watch a chat become files on your PC.
            </h1>
            <p className="mt-4 font-body text-[18px] leading-[1.55] text-tr-mist md:text-[20px]">
              This page shows one complete download, recorded on a Windows PC. A conversation
              starts in the app and ends as two files in a folder on the drive.
            </p>
            <div className="mt-6 flex flex-wrap gap-2.5">
              <Chip>Recorded on Windows</Chip>
              <Chip>Captioned</Chip>
              <Chip>Free Tier</Chip>
            </div>
            <a href="#download" className="mt-5 inline-block text-[15px] font-semibold text-tr-steel transition-colors hover:text-tr-paper">
              Skip to the download ↓
            </a>
          </div>
        </Container>
      </Section>

      {/* 2. The Demo */}
      <Section id="demo" className="bg-tr-obsidian">
        <Container>
          <div className="max-w-[680px]">
            <Eyebrow mono>The Demo</Eyebrow>
            <h2 className="mt-3 font-heading text-[28px] font-semibold leading-[1.15] text-tr-paper md:text-[36px]">
              One conversation, start to finish
            </h2>
            <p className="mt-4 font-body text-[18px] leading-[1.55] text-tr-mist">
              Recorded on the Free Tier. Captions explain each step, so the video works with the sound off.
            </p>
          </div>

          <div className="mt-8 max-w-[960px]">
            <div className="relative overflow-hidden rounded-xl border border-tr-slate bg-tr-graphite">
              <video
                ref={videoRef}
                className="aspect-video w-full rounded-lg border border-tr-slate/60 bg-black"
                src={DEMO_SRC}
                poster={POSTER}
                controls
                preload="metadata"
                playsInline
                title="TotalRecalls downloading a conversation to local Markdown and JSON files"
              />
            </div>
            <p className="mt-3 font-body text-[14px] text-tr-dust">
              Real screen recording, trimmed for length. Account details are blurred.
            </p>
            <p className="mt-1.5 font-body text-[13px] text-tr-dust">
              Showing the current full walkthrough. The dedicated 60-second ChatGPT demo and the
              Pro upgrade walkthrough are in production — they drop into this slot when cut.
            </p>
            <div className="mt-2">
              <a href="#transcript" className="text-[15px] font-semibold text-tr-steel transition-colors hover:text-tr-paper">
                Read the transcript →
              </a>
            </div>
          </div>
        </Container>
      </Section>

      {/* 3. What You're Seeing */}
      <Section id="steps" className="bg-tr-obsidian">
        <Container>
          <div className="max-w-[680px]">
            <Eyebrow mono>Step by Step</Eyebrow>
            <h2 className="mt-3 font-heading text-[28px] font-semibold leading-[1.15] text-tr-paper md:text-[36px]">
              What happens in the video
            </h2>
          </div>
          <div className="mt-8 max-w-[720px] divide-y divide-tr-slate border-t border-tr-slate">
            {STEPS.map((s) => (
              <Step key={s.t} {...s} />
            ))}
          </div>
        </Container>
      </Section>

      {/* 4. The Result */}
      <Section id="result" className="bg-tr-obsidian">
        <Container>
          <div className="max-w-[680px]">
            <Eyebrow mono>The Result</Eyebrow>
            <h2 className="mt-3 font-heading text-[28px] font-semibold leading-[1.15] text-tr-paper md:text-[36px]">
              What's on your drive afterward
            </h2>
          </div>

          <div className="mt-8 max-w-[960px]">
            <img
              src={RESULT_IMG}
              alt="File Explorer open to the TotalRecalls Library provider folder, showing a conversation saved as one Markdown file and one JSON file"
              className="w-full rounded-xl border border-tr-slate"
            />
          </div>

          {/* numbered legend */}
          <div className="mt-8 grid max-w-[960px] gap-8 md:grid-cols-3">
            <MarkerNote n={1} title="The folder" body="One Library, with a subfolder for each provider." />
            <MarkerNote n={2} title="The Markdown file" body="The full conversation in readable text, with headings and code blocks intact." />
            <MarkerNote n={3} title="The JSON file" body="The same chat as structured data, ready for search or other tools." />
          </div>

          <p className="mt-8 max-w-[720px] font-body text-[16px] leading-[1.6] text-tr-mist">
            These files open without TotalRecalls. Copy them, back them up, or search them like
            any other document on your PC.
          </p>

          <div className="mt-6 max-w-[960px]">
            <EvidenceStrip
              path="C:\TotalRecalls\Library\chatgpt\2026-09-14-pricing-research.md"
              chips={<><Chip>MD</Chip><Chip>JSON</Chip><LocalChip /></>}
            />
          </div>
        </Container>
      </Section>

      {/* 5. Try It Yourself (graphite band) */}
      <Section id="download" className="bg-tr-graphite border-t border-tr-slate">
        <Container>
          <div className="max-w-[680px]">
            <Eyebrow mono>Try It Yourself</Eyebrow>
            <h2 className="mt-3 font-heading text-[28px] font-semibold leading-[1.15] text-tr-paper md:text-[36px]">
              Run the same download on your own chats
            </h2>
            <p className="mt-4 font-body text-[18px] leading-[1.55] text-tr-mist">
              The Free Tier includes ChatGPT, Claude, and Perplexity, with up to 5 conversations each.
              You don't need a card or an account.
            </p>
          </div>
          <div className="mt-7">
            <Btn href="/download/" large>Download free</Btn>
          </div>
          <p className="mt-4 font-body text-[14px] text-tr-dust">
            Windows 10 and 11. Windows may show a SmartScreen prompt the first time you open the app.{" "}
            <a href="/guides/smartscreen/" className="text-tr-steel transition-colors hover:text-tr-paper">What it means →</a>
          </p>
        </Container>
      </Section>

      {/* 6. Pricing link (centered, on obsidian) */}
      <div className="bg-tr-obsidian py-12 md:py-16">
        <Container>
          <div className="mx-auto flex max-w-[720px] flex-col items-center gap-3 text-center">
            <p className="font-body text-[16px] text-tr-mist">Want every provider and no download cap?</p>
            <a href="/pricing/" className="text-[15px] font-semibold text-tr-steel transition-colors hover:text-tr-paper">
              Compare Free and Pro →
            </a>
          </div>
        </Container>
      </div>

      {/* 7. Transcript (collapsed accordion) */}
      <div className="border-t border-tr-slate bg-tr-obsidian pb-20">
        <Container>
          <details id="transcript" className="group max-w-[720px]">
            <summary className="flex cursor-pointer list-none items-center justify-between py-5 font-heading text-[16px] font-semibold text-tr-paper [&::-webkit-details-marker]:hidden">
              <span>Show transcript</span>
              <ChevronDown className="h-5 w-5 text-tr-steel transition-transform group-open:rotate-180" />
            </summary>
            <div className="border-t border-tr-slate pb-6 pt-4 font-body text-[15px] leading-[1.7] text-tr-mist">
              <p className="mb-3 text-tr-dust">
                Final caption text lands here once the dedicated 60-second cut is locked. The caption
                track below follows the step-by-step above.
              </p>
              <ol className="list-decimal space-y-2.5 pl-6">
                {STEPS.map((s) => (
                  <li key={s.t}><span className="font-mono text-[13px] text-tr-steel">{s.t}</span> — {s.title}. {s.body}</li>
                ))}
              </ol>
            </div>
          </details>
        </Container>
      </div>
    </>
  );
}
