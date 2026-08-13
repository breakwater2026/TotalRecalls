import { Section } from "./ui/Section";
import { SectionTitle } from "./ui/SectionTitle";
import { GuideCard } from "./ui/GuideCard";

export default function Guides() {
  return (
    <Section id="guides" bg="white">
      <SectionTitle>Guides</SectionTitle>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
        <GuideCard title="Export ChatGPT conversations" text="Official export vs a library you control." />
        <GuideCard title="Download your Claude history" text="Keep Projects and long threads." />
        <GuideCard title="Backup Perplexity threads" text="Save research before you lose the tab trail." />
        <GuideCard title="Gemini Takeout → Markdown" text="Turn JSON dumps into conversations." />
        <GuideCard title="Own your AI chat data" text="Why multi-assistant export matters." />
      </div>
    </Section>
  );
}
