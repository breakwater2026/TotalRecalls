import React from "react";
import { Container, Section, Eyebrow, EvidenceStrip, LocalChip } from "./ui";

const PROBLEMS = [
  { lead: "Tabs close.", body: "Conversations sink under hundreds of newer ones." },
  { lead: "Interfaces change.", body: "Old chats get harder to reach." },
  { lead: "Nobody keeps a backup.", body: "Until they need one." },
];

export default function Why() {
  return (
    <Section id="why" className="border-t border-tr-slate bg-tr-obsidian">
      <Container>
        <Eyebrow>Why this matters</Eyebrow>

        <h2 className="mt-3 max-w-[680px] font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
          AI chat history drifts. Files stay put.
        </h2>

        <div className="mt-12 grid md:grid-cols-3">
          {PROBLEMS.map((p, i) => (
            <div key={p.lead} className={`px-0 py-6 md:px-8 md:py-0 ${i > 0 ? "md:border-l md:border-tr-slate" : ""} ${i > 0 ? "border-t md:border-t-0 border-tr-slate" : ""}`}>
              <h4 className="font-heading text-[17px] md:text-[18px] font-semibold leading-[1.35] text-tr-paper">
                {p.lead}
              </h4>
              <p className="mt-2 font-body text-[16px] leading-[1.6] text-tr-mist">{p.body}</p>
            </div>
          ))}
        </div>

        <p className="mt-10 max-w-[680px] font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-paper">
          TotalRecalls saves each chat as a plain file on your own PC.
        </p>

        <div className="mt-8">
          <EvidenceStrip
            path={<>C:\TotalRecalls\Library\claude\2026-07-28-refactor-plan.md</>}
            chips={
              <>
                <span className="rounded-chip border border-tr-slate px-2 py-1 font-mono text-[12px] font-medium uppercase tracking-[0.02em] text-tr-steel">.md</span>
                <span className="rounded-chip border border-tr-slate px-2 py-1 font-mono text-[12px] font-medium uppercase tracking-[0.02em] text-tr-steel">.json</span>
                <LocalChip />
              </>
            }
          />
        </div>
      </Container>
    </Section>
  );
}
