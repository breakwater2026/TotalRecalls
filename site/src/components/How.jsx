import { Section } from "./ui/Section";
import { SectionTitle } from "./ui/SectionTitle";

export default function How() {
  return (
    <Section id="how" bg="gray-50">
      <SectionTitle>How It Works</SectionTitle>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
        <div className="space-y-3">
          <div className="text-xl font-semibold">1. Buy once</div>
          <p className="text-gray-700">Checkout via Lemon Squeezy.</p>
        </div>
        <div className="space-y-3">
          <div className="text-xl font-semibold">2. Install</div>
          <p className="text-gray-700">Unzip and run the Windows app.</p>
        </div>
        <div className="space-y-3">
          <div className="text-xl font-semibold">3. Pick a provider</div>
          <p className="text-gray-700">ChatGPT, Claude, Perplexity, Gemini, or Grok.</p>
        </div>
        <div className="space-y-3">
          <div className="text-xl font-semibold">4. Export</div>
          <p className="text-gray-700">Chats land as Markdown + JSON.</p>
        </div>
      </div>
    </Section>
  );
}
