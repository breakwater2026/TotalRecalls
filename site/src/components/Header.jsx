import { ReactNode } from "react";

export default function Header() {
  return (
    <header className="w-full border-b bg-white">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="text-xl font-semibold">TotalRecalls</div>
        <nav className="flex space-x-6 text-gray-700">
          <a href="#home" className="hover:text-black">Home</a>
          <a href="#how" className="hover:text-black">How It Works</a>
          <a href="#guides" className="hover:text-black">Guides</a>
          <a href="#compare" className="hover:text-black">Compare</a>
          <a href="#pricing" className="hover:text-black">Pricing</a>
          <a href="#download" className="hover:text-black">Download</a>
        </nav>
      </div>
    </header>
  );
}
