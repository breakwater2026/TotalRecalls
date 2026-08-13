import { Section } from "./ui/Section";
import { SectionTitle } from "./ui/SectionTitle";

export default function Providers() {
  return (
    <Section bg="white">
      <SectionTitle>Supported Providers</SectionTitle>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-8 text-center text-gray-700">
        <div>ChatGPT</div>
        <div>Claude</div>
        <div>Perplexity</div>
        <div>Gemini</div>
        <div>Grok</div>
      </div>
    </Section>
  );
}
