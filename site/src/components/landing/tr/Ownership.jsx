import React from "react";
import { Search, FileText, FolderOpen } from "lucide-react";
import { Container, Section, Eyebrow, Btn, EvidenceStrip, LocalChip } from "./ui";

const PILLARS = [
  {
    icon: Search,
    lead: "Find it again.",
    problem: "Tabs close. Chats sink under hundreds of newer ones.",
    body: "A saved file on your PC is one quick search away in Windows Explorer, Notion, or Obsidian — not 400 conversations buried down a web sidebar.",
    chip: "Searchable · Local files",
  },
  {
    icon: FileText,
    lead: "Survive redesigns.",
    problem: "Interfaces change. Old chats get harder to reach.",
    body: "Plain Markdown and JSON files open the same way in Notepad or any editor in ten years, whatever the cloud chat interface looks like.",
    chip: ".md + .json",
  },
  {
    icon: FolderOpen,
    lead: "Take it anywhere.",
    problem: "Nobody keeps a backup. Until they need one.",
    body: "Copy your Library folder to a backup drive or migrate to a new PC in seconds. Your work stays with you, with no login or cloud dependency.",
    chip: "Copy folder · No login",
  },
];

export default function Ownership() {
  return (
    <Section id="why" className="border-t border-tr-slate bg-tr-graphite">
      <Container>
        <Eyebrow mono>Why own your AI chats</Eyebrow>

        <h2 className="mt-3 max-w-[850px] font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
          AI chat history drifts. Files stay put.
        </h2>

        <p className="mt-4 max-w-[840px] font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-mist">
          Your AI chats hold your most sensitive personal info — medical questions, financial planning, psychological reflections, relationships, and private drafts. But interfaces change, tabs close, and cloud histories drift. TotalRecalls saves each conversation as a plain file you control forever — keeping your chats private on your own PC, away from prying eyes.
        </p>

        <div className="mt-12 grid md:grid-cols-3 gap-6">
          {PILLARS.map((p) => (
            <div key={p.lead} className="flex flex-col rounded-card border border-tr-slate bg-tr-obsidian p-6">
              <p.icon className="h-6 w-6 text-tr-mist" strokeWidth={1.5} />
              <h3 className="mt-4 font-heading text-[18px] md:text-[20px] font-semibold leading-[1.3] text-tr-paper">
                {p.lead}
              </h3>
              <p className="mt-2 font-mono text-[13px] text-tr-steel leading-[1.4]">
                {p.problem}
              </p>
              <p className="mt-3 font-body text-[15px] leading-[1.6] text-tr-mist">
                {p.body}
              </p>
              <div className="mt-auto pt-5">
                <span className="inline-flex rounded-chip border border-tr-slate px-2 py-1 font-mono text-[12px] font-medium uppercase tracking-[0.02em] text-tr-steel">
                  {p.chip}
                </span>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-12">
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

        <div className="mt-8 flex flex-wrap items-center gap-6">
          <Btn href="#pricing" variant="tertiary">Compare Free and Pro ↓</Btn>
          <a
            href="/library/"
            className="text-[14px] font-mono font-medium text-tr-steel hover:text-tr-amber transition-colors inline-flex items-center gap-1.5"
          >
            Explore Library folder structure & formats &rarr;
          </a>
        </div>
      </Container>
    </Section>
  );
}
