import React, { useState, useRef } from "react";
import { Container, Section, Eyebrow } from "./ui";

export default function DemoSection() {
  const [isPlaying, setIsPlaying] = useState(false);
  const videoRef = useRef(null);

  const handlePlay = () => {
    if (videoRef.current) {
      videoRef.current.play();
    }
  };

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
