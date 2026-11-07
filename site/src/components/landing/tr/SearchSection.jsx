import React from "react";
import { Container, Section, Eyebrow, Btn } from "./ui";

const POINTS = [
  "Ask, don’t remember. Search by meaning, by keyword, or both. Find the chat you want even if you never used those words. It is called Semantic Vector search and RAG storage.",
  "All your conversations downloaded from 8 providers in one folder on your computer at C:\\TotalRecalls\\Library. With our SSE, you don't have to guess as to from which provider the information you are searching for comes from.",
  "Your files, your PC. Click a result to open the original conversation.",
];

export default function SearchSection() {
  return (
    <Section id="search-addon" className="border-t border-tr-slate bg-tr-obsidian">
      <Container>
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          <div className="max-w-[680px]">
            <Eyebrow mono>SSE ADD-ON</Eyebrow>
            <h2 className="mt-3 font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
              Thousands of chats in folders is still a pile.
            </h2>
            <p className="mt-4 font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-mist">
              Smart Search Engine (SSE) finds the one you need. Ask via plain English chat, and it looks through every conversation downloaded via our Downloader onto your local TotalRecalls Library from every provider.
            </p>
            <ul className="mt-8 space-y-4 font-body text-[15px] leading-[1.6] text-tr-mist">
              {POINTS.map((p, i) => (
                <li key={i} className="flex gap-3">
                  <span className="shrink-0 text-tr-amber">{i + 1}.</span>
                  <span>{p}</span>
                </li>
              ))}
            </ul>
            <div className="mt-10 flex flex-wrap items-center gap-5">
              <Btn href="/#pricing">See Smart Search Engine (SSE) pricing</Btn>
              <a
                href="/smart-search/"
                className="text-[14px] font-mono font-medium text-tr-steel hover:text-tr-amber transition-colors inline-flex items-center gap-1.5"
              >
                Explore full SSE capabilities & specs &rarr;
              </a>
            </div>
          </div>
          <div className="flex justify-center">
            <div className="rounded-card border border-tr-slate bg-tr-graphite p-2 md:p-3">
              <img
                src="/images/search-results-window.jpg"
                alt="Smart Search Engine (SSE) results window"
                className="rounded-sm block h-auto w-full max-w-[420px]"
              />
            </div>
          </div>
        </div>
      </Container>
    </Section>
  );
}
