import { Section } from "./ui/Section";
import { SectionTitle } from "./ui/SectionTitle";

export default function StraightTalk() {
  return (
    <Section bg="gray-50">
      <SectionTitle>Straight Talk</SectionTitle>
      <ul className="list-disc pl-6 text-gray-700 space-y-2">
        <li>Windows app today (WebView2). Mac later if demand is real.</li>
        <li>Gemini uses your Google Takeout JSON.</li>
        <li>Unsigned builds may show SmartScreen until code-signing is complete.</li>
        <li>SP8 Smart App Control may block unsigned apps.</li>
        <li>You must follow each provider's terms.</li>
        <li>No AdSense clutter.</li>
      </ul>
    </Section>
  );
}
