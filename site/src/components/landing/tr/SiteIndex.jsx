import React from "react";
import { Container, Section, Eyebrow } from "./ui";

const CATEGORIES = [
  {
    title: "Product Deep-Dives",
    description: "Detailed architectures, formats, and simulators.",
    links: [
      { label: "Smart Search Engine (SSE)", href: "/smart-search/" },
      { label: "The Library Format & Schemas", href: "/library/" },
      { label: "All 8 Supported Providers", href: "/providers/" },
      { label: "Interactive Download Simulator", href: "/see-it-work/" },
      { label: "Video Walkthrough Demo", href: "/demo/" },
      { label: "The Ownership Path", href: "/ownership/" },
    ],
  },
  {
    title: "Provider Export Guides",
    description: "Step-by-step guides for every AI assistant.",
    links: [
      { label: "ChatGPT Export Guide", href: "/guides/export-chatgpt-conversations/" },
      { label: "Claude History Guide", href: "/guides/export-claude-chat-history/" },
      { label: "Perplexity Threads Guide", href: "/guides/export-perplexity-conversations/" },
      { label: "Gemini Takeout Archive Guide", href: "/guides/gemini-takeout-archive/" },
      { label: "DeepSeek Chats Guide", href: "/guides/deepseek/" },
      { label: "Grok (xAI) History Guide", href: "/guides/grok/" },
      { label: "Mistral (Le Chat) Guide", href: "/guides/mistral/" },
      { label: "Qwen Chat Guide", href: "/guides/qwen/" },
      { label: "All Documentation Guides →", href: "/guides/" },
    ],
  },
  {
    title: "Technical Specs & Tools",
    description: "Data ownership, SmartScreen, and troubleshooting.",
    links: [
      { label: "Using Smart Search Engine (SSE)", href: "/guides/using-smart-search-engine/" },
      { label: "Library Folder Structure & Format", href: "/guides/library-format/" },
      { label: "Own Your AI Chat Data", href: "/guides/own-your-ai-chat-data/" },
      { label: "Windows SmartScreen Walkthrough", href: "/guides/smartscreen/" },
      { label: "Troubleshooting Downloads", href: "/guides/troubleshooting/" },
      { label: "Microsoft Store Listing", href: "https://apps.microsoft.com/detail/9PP1KKD5X2D6" },
    ],
  },
  {
    title: "Comparisons & Architecture",
    description: "How local ownership compares to cloud silos.",
    links: [
      { label: "Comparison Index Hub", href: "/compare/" },
      { label: "Why Local Files Matter", href: "/compare/why-local/" },
      { label: "Multi-Assistant vs Single Lock-in", href: "/compare/why-multi-assistant/" },
      { label: "One-Time vs SaaS Subscription", href: "/compare/pricing/" },
      { label: "ChatGPT vs TotalRecalls", href: "/compare/chatgpt/" },
      { label: "Claude vs TotalRecalls", href: "/compare/claude/" },
      { label: "Perplexity vs TotalRecalls", href: "/compare/perplexity/" },
      { label: "Gemini vs Raw Google Takeout", href: "/compare/gemini/" },
    ],
  },
  {
    title: "Support, Legal & Releases",
    description: "Downloads, key recovery, terms, and policies.",
    links: [
      { label: "Free Tier Download (Windows 10/11)", href: "/download/" },
      { label: "Buy Downloader Pro & SSE", href: "/buy/" },
      { label: "Help & Quick-Start Guide", href: "/help/" },
      { label: "Customer Support & Key Recovery", href: "/support/" },
      { label: "Comprehensive 30+ FAQ Archive", href: "/faq/" },
      { label: "Version Release Notes & Changelog", href: "/release-notes/" },
      { label: "Product Roadmap", href: "/roadmap/" },
      { label: "Feature Requests", href: "/feature-requests/" },
      { label: "Privacy Policy (Local-Only, Zero Servers)", href: "/privacy/" },
      { label: "Terms of Service", href: "/terms/" },
      { label: "Legal Portal & Refund Protections", href: "/legals/" },
      { label: "About TotalRecalls & Maker", href: "/about/" },
      { label: "Press Kit & Company Facts", href: "/press/" },
    ],
  },
];

export default function SiteIndex() {
  return (
    <Section id="site-index" className="relative border-t border-tr-slate bg-tr-obsidian">
      <Container>
        <div className="max-w-[760px]">
          <Eyebrow mono>Complete Resource & Documentation Index</Eyebrow>
          <h2 className="mt-3 font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
            Explore every guide, comparison, and technical reference.
          </h2>
          <p className="mt-4 font-body text-[16px] md:text-[18px] leading-[1.6] text-tr-mist">
            Everything outside the main landing page scroll — searchable, interlinked, and designed to help you verify and master your local AI archive.
          </p>
        </div>

        <div className="mt-12 grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-8 items-start">
          {CATEGORIES.map((cat) => (
            <div key={cat.title} className="flex flex-col">
              <h3 className="font-heading text-[16px] font-semibold text-tr-paper border-b border-tr-slate pb-2">
                {cat.title}
              </h3>
              <p className="mt-1.5 font-body text-[12.5px] leading-[1.4] text-tr-dust">
                {cat.description}
              </p>
              <ul className="mt-4 space-y-2">
                {cat.links.map((link) => (
                  <li key={link.href}>
                    <a
                      href={link.href}
                      className="font-body text-[13.5px] leading-[1.45] text-tr-mist hover:text-tr-amber transition-colors inline-block"
                    >
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </Container>
    </Section>
  );
}
