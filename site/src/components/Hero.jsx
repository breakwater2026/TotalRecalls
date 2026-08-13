import { ButtonPrimary } from "./ui/ButtonPrimary";
import { ButtonSecondary } from "./ui/ButtonSecondary";

export default function Hero() {
  return (
    <section id="home" className="w-full bg-gray-50 py-20">
      <div className="max-w-6xl mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
        <div className="space-y-6">
          <h1 className="text-4xl font-bold leading-tight">
            Own every AI conversation.
          </h1>
          <p className="text-lg text-gray-700">
            A small Windows app that saves your ChatGPT, Claude, Perplexity, Gemini, and Grok chats into a private folder on your computer — readable Markdown + JSON you keep forever.
          </p>
          <div className="space-y-2">
            <div className="text-2xl font-semibold">$24 launch price</div>
            <div className="text-gray-600">One-time purchase · Windows app · Local files only</div>
          </div>
          <div className="flex space-x-4 pt-4">
            <ButtonPrimary href="#buy">Buy TotalRecalls — $24</ButtonPrimary>
            <ButtonSecondary href="#download">Download ZIP</ButtonSecondary>
          </div>
        </div>
        <div className="space-y-6">
          <div className="bg-white shadow rounded-lg p-4">
            <img src="/img/library.png" alt="Library screenshot" className="rounded" />
          </div>
          <div className="bg-white shadow rounded-lg p-4">
            <img src="/img/markdown.png" alt="Markdown screenshot" className="rounded" />
          </div>
        </div>
      </div>
    </section>
  );
}
