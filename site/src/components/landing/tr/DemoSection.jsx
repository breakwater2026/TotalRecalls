import React from "react";
import { Container, Section, Eyebrow } from "./ui";

export default function DemoSection() {
  return (
    <Section id="demo" className="border-t border-tr-slate bg-tr-obsidian">
      <Container>
        <div className="max-w-[960px]">
          <Eyebrow mono>Demo</Eyebrow>
          <h2 className="mt-3 font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
            Watch TotalRecalls (Pro + SSE) in&nbsp;action.
          </h2>
          <p className="mt-4 font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-mist">
            A real screen recording of the owner&apos;s own 8,135 conversations spanning over two years downloaded via the app into Markdown and JSON files in your local C:\ drive Library&nbsp;folder.
          </p>
        </div>

        <div className="mt-10 max-w-[960px]">
          <div className="relative overflow-hidden rounded-xl border border-tr-slate bg-tr-graphite">
            <video
              className="aspect-video w-full rounded-lg border border-tr-slate/60 bg-black"
              src="https://demo-video.totalrecalls.app/TR_website_chatgpt.mp4"
              poster="/demo/poster_chatgpt.png"
              controls
              preload="metadata"
              playsInline
              title="TotalRecalls demo walkthrough"
            />
          </div>
          <p className="mt-3 font-body text-[14px] text-tr-dust">
            Full walkthrough recorded on Windows. Conversations stay on your PC — nothing is sent to our servers.
          </p>
          <div className="mt-4">
            <a href="/see-it-work/" className="inline-flex items-center gap-1 font-mono text-[13px] font-semibold uppercase tracking-[0.08em] text-tr-steel hover:text-tr-amber transition-colors">
              Try interactive on-screen provider walkthroughs &rarr;
            </a>
          </div>
        </div>
      </Container>
    </Section>
  );
}
