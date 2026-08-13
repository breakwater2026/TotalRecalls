import { Section } from "./ui/Section";
import { SectionTitle } from "./ui/SectionTitle";

export default function Why() {
  return (
    <Section bg="white">
      <SectionTitle>Why TotalRecalls</SectionTitle>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
        <div className="space-y-4">
          <h3 className="text-xl font-semibold">Your AI history shouldn't vanish</h3>
          <p className="text-gray-700">
            Tabs close. Exports break. Interfaces change. A folder of Markdown on your PC still opens in ten years.
          </p>
        </div>
        <div className="space-y-4">
          <h3 className="text-xl font-semibold">One library for every assistant</h3>
          <p className="text-gray-700">
            Export everything into a single, predictable folder structure.
          </p>
        </div>
        <div className="space-y-4">
          <h3 className="text-xl font-semibold">Private by design</h3>
          <p className="text-gray-700">
            Local sign-in. No cloud locker. No account. No subscription.
          </p>
        </div>
      </div>
    </Section>
  );
}
