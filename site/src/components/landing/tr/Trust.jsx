import React from "react";
import { Container, Section, Eyebrow, Btn } from "./ui";

const ANSWERS = [
  {
    lead: "No cloud, no account.",
    body: "Your conversations aren't sent to TotalRecalls servers. There's no account to create — you sign in to each AI provider locally, inside the app.",
  },
  {
    lead: "SmartScreen, explained.",
    body: "First launch may show a Windows SmartScreen prompt. It's a routine reputation check on new apps — two clicks to continue.",
    link: { label: "Read the SmartScreen guide", href: "/microsoft-warning/" },
  },
  {
    lead: "A straight answer.",
    body: "Windows 10 and 11 today. No AdSense clutter — this site sells a tool, not pageviews.",
  },
];

export default function Trust() {
  return (
    <Section id="trust" className="bg-tr-obsidian">
      <Container>
        <Eyebrow>Straight talk</Eyebrow>

        <h2 className="mt-3 max-w-[680px] font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
          Plain answers before you install.
        </h2>

        <p className="mt-4 max-w-[680px] font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-mist">
          You&apos;re giving a new app access to your AI conversations. Here&apos;s how
          TotalRecalls earns that trust.
        </p>

        <div className="mt-12 grid md:grid-cols-3 gap-6">
          {ANSWERS.map((a) => (
            <div key={a.lead} className="flex flex-col rounded-card border border-tr-slate bg-tr-graphite p-6">
              <h4 className="font-heading text-[17px] md:text-[18px] font-semibold leading-[1.35] text-tr-paper">
                {a.lead}
              </h4>
              <p className="mt-2 font-body text-[16px] leading-[1.6] text-tr-mist">{a.body}</p>
              {a.link && (
                <a
                  href={a.link.href}
                  className="mt-auto pt-4 font-body text-[15px] font-semibold text-tr-steel transition-colors hover:text-tr-paper"
                >
                  {a.link.label} →
                </a>
              )}
            </div>
          ))}
        </div>
      </Container>
    </Section>
  );
}
