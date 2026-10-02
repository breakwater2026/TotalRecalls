import React from "react";
import { Search, FileText, FolderOpen } from "lucide-react";
import { Container, Section, Eyebrow, Btn, EvidenceStrip, LocalChip } from "./ui";

const CARDS = [
  {
    icon: Search,
    lead: "Find it again.",
    body: "A saved file is one quick search away, not 400 conversations down a sidebar.",
    chip: "Searchable · Local files",
  },
  {
    icon: FileText,
    lead: "Keep it through redesigns.",
    body: "A Markdown file opens the same way in Notepad next year, whatever the chat interface looks like.",
    chip: ".md + .json",
  },
  {
    icon: FolderOpen,
    lead: "Take it anywhere.",
    body: "Copy the folder to a new PC or a backup drive, and your library comes with you, no login needed.",
    chip: "Copy folder · No login",
  },
];

export default function Ownership() {
  return (
    <Section id="ownership" className="bg-tr-obsidian">
      <Container>
        <Eyebrow>Why own your AI chats</Eyebrow>

        <h2 className="mt-3 max-w-[680px] font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
          Your best thinking deserves a better home than a sidebar.
        </h2>

        <p className="mt-4 max-w-[680px] font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-mist">
          Your AI chats hold research, drafts, code, and decisions. When you own your AI
          chats, that work lives on your own PC as files you control.
        </p>

        <div className="mt-12 grid md:grid-cols-3 gap-6">
          {CARDS.map((c) => (
            <div key={c.lead} className="flex flex-col rounded-card border border-tr-slate bg-tr-graphite p-6">
              <c.icon className="h-6 w-6 text-tr-mist" strokeWidth={1.5} />
              <h4 className="mt-4 font-heading text-[17px] md:text-[18px] font-semibold leading-[1.35] text-tr-paper">
                {c.lead}
              </h4>
              <p className="mt-2 font-body text-[16px] leading-[1.6] text-tr-mist">{c.body}</p>
              <div className="mt-auto pt-4">
                <span className="inline-flex rounded-chip border border-tr-slate px-2 py-1 font-mono text-[12px] font-medium uppercase tracking-[0.02em] text-tr-steel">
                  {c.chip}
                </span>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-12">
          <EvidenceStrip
            path={<>C:\TotalRecalls\Library\claude\2026-07-28-refactor-plan.md</>}
            chips={<LocalChip />}
          />
        </div>

        {/* Homepage version: tertiary link only — no Amber button, no Free Tier line. */}
        <div className="mt-8">
          <Btn href="#pricing" variant="tertiary">Compare Free and Pro ↓</Btn>
        </div>
      </Container>
    </Section>
  );
}
