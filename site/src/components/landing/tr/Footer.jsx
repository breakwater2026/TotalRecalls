import React from "react";
import { currentVersion } from "../../../data/releases.json";
import { Container, Btn } from "./ui";

const COLS = [
  {
    h: "Product",
    links: [
      { l: "How It Works", href: "/#resolution" },
      { l: "See It Work", href: "/see-it-work/" },
      { l: "AI Providers", href: "/providers/" },
      { l: "The Library", href: "/library/" },
      { l: "Ownership Path", href: "/ownership/" },
      { l: "Pricing", href: "/#pricing" },
      { l: "Download", href: "/download/" },
      { l: "Release Notes", href: "/release-notes/" },
    ],
  },
  {
    h: "Guides",
    links: [
      { l: "Download ChatGPT conversations", href: "/guides/export-chatgpt-conversations/" },
      { l: "Download your Claude history", href: "/guides/export-claude-chat-history/" },
      { l: "Backup Perplexity threads", href: "/guides/backup-perplexity-threads/" },
      { l: "Gemini Takeout → Markdown", href: "/guides/gemini-takeout-archive/" },
      { l: "Download DeepSeek chats", href: "/guides/deepseek/" },
      { l: "Download Mistral (Le Chat) conversations", href: "/guides/mistral/" },
      { l: "Download Qwen Chat conversations", href: "/guides/qwen/" },
      { l: "Downloading Grok conversations", href: "/guides/grok/" },
      { l: "Own your AI chat data", href: "/guides/own-your-ai-chat-data/" },
    ],
  },
  {
    h: "Legal",
    links: [
      { l: "Privacy Policy", href: "/privacy/" },
      { l: "Terms of Service", href: "/terms/" },
      { l: "Refund Policy", href: "/legals/#refund" },
    ],
  },
];

export default function Footer() {
  return (
    <footer id="footer" className="border-t border-tr-slate bg-tr-graphite">
      <Container>
        <div className="grid md:grid-cols-4 gap-10 items-start justify-items-center text-center md:justify-items-start md:text-left">
          <div className="flex flex-col items-center md:items-start text-center md:text-left">
            <div className="flex items-center gap-2.5">
              <img src="/logo.png" alt="TotalRecalls logo" className="h-[39px] w-auto object-contain" />
              <span className="font-heading text-[17px] font-bold text-tr-paper">TotalRecalls</span>
            </div>
            <p className="mt-4 max-w-xs font-body text-[14px] leading-[1.6] text-tr-mist">
              A private local archive for your AI work — eight providers, saved as Markdown
              and JSON on your own PC.
            </p>
          </div>

          {COLS.map((c) => (
            <div key={c.h} className="flex flex-col items-center md:items-start text-center md:text-left">
              <span className="font-mono text-[10px] uppercase tracking-[0.18em] text-tr-dust">{c.h}</span>
              <ul className="mt-4 space-y-2.5">
                {c.links.map((link) => (
                  <li key={link.l}>
                    <a
                      href={link.href}
                      className="font-body text-[14px] text-tr-mist transition-colors hover:text-tr-paper"
                    >
                      {link.l}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-10 flex flex-col items-center justify-center gap-3 border-t border-tr-slate pt-6">
          <Btn href="/download/">Download free</Btn>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-6 font-mono text-[11px] text-tr-dust text-center">
            <span>© {new Date().getFullYear()} TotalRecalls v{currentVersion}</span>
            <a href="/privacy/" className="transition-colors hover:text-tr-paper">Privacy Policy</a>
            <a href="/terms/" className="transition-colors hover:text-tr-paper">Terms of Service</a>
            <a href="/legals/#refund" className="transition-colors hover:text-tr-paper">Refund Policy</a>
          </div>
        </div>
      </Container>
    </footer>
  );
}
