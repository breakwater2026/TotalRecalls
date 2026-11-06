import React from "react";
import { Container, Section, Eyebrow, Btn } from "./ui";

const POINTS = [
  "Ask, don’t remember. Search by meaning, by keyword, or both. Find the chat even if you never used those words.",
  "All eight providers, one search. No guessing which app you used.",
  "Your files, your PC. Click a result to open the original conversation. Nothing you write or save is uploaded.",
];

export default function SearchSection() {
  return (
    <Section id="search-addon" className="border-t border-tr-slate bg-tr-graphite">
      <Container>
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          <div className="max-w-[680px]">
            <Eyebrow mono>NEW ADD-ON</Eyebrow>
            <h2 className="mt-3 font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
              Hundreds of chats in folders is still a pile.
            </h2>
            <p className="mt-4 font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-mist">
              Smart Search Engine finds the one you need. Ask in plain English, and it looks through every conversation from every provider.
            </p>
            <ul className="mt-8 space-y-4 font-body text-[15px] leading-[1.6] text-tr-mist">
              {POINTS.map((p, i) => (
                <li key={i} className="flex gap-3">
                  <span className="shrink-0 text-tr-amber">{i + 1}.</span>
                  <span>{p}</span>
                </li>
              ))}
            </ul>
            <div className="mt-10 flex flex-wrap gap-4">
              <Btn href="/smart-search/">See Smart Search Engine</Btn>
              <Btn href="/buy/" variant="secondary" className="w-auto" data-tr-buy data-tr-price-id="bundle">
                Get the Pro + SSE bundle — $49.89
              </Btn>
            </div>
          </div>
          <div className="flex justify-center">
            <div className="rounded-card border border-tr-slate bg-tr-obsidian p-2 md:p-3">
              <img
                src="/images/search-results-window.jpg"
                alt="Smart Search Engine results window"
                className="rounded-sm block h-auto w-full max-w-[420px]"
              />
            </div>
          </div>
        </div>
      </Container>
    </Section>
  );
}
