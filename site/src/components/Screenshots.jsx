import { Section } from "./ui/Section";

export default function Screenshots() {
  return (
    <Section bg="gray-50">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-16">
        <div className="space-y-4">
          <h3 className="text-2xl font-semibold">Your Library, organized</h3>
          <p className="text-gray-700">Clean folder structure you can browse, search, and back up.</p>
          <img src="/img/library.png" className="rounded shadow" alt="Library screenshot" />
        </div>
        <div className="space-y-4">
          <h3 className="text-2xl font-semibold">Readable Markdown</h3>
          <p className="text-gray-700">Predictable formatting. Easy to diff, annotate, or feed into your own tools.</p>
          <img src="/img/markdown.png" className="rounded shadow" alt="Markdown screenshot" />
        </div>
      </div>
    </Section>
  );
}
