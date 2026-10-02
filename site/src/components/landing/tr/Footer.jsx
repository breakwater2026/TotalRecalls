import React, { useState } from "react";
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
      { l: "Export Perplexity conversations", href: "/guides/export-perplexity-conversations/" },
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

function SignupForm() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState("idle"); // idle | sending | success | error
  const [message, setMessage] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    const value = email.trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) {
      setStatus("error");
      setMessage("Please enter a valid email address.");
      return;
    }
    setStatus("sending");
    setMessage("");
    try {
      const res = await fetch("/api/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: value }),
      });
      const data = await res.json().catch(() => ({}));
      if (res.ok && data.ok) {
        setStatus("success");
        setEmail("");
      } else {
        setStatus("error");
        setMessage(data.error || "Something went wrong. Please try again.");
      }
    } catch {
      setStatus("error");
      setMessage("Something went wrong. Please try again.");
    }
  }

  const busy = status === "sending";

  return (
    <>
      <form onSubmit={onSubmit} data-footer-signup novalidate>
        <label htmlFor="footer-signup-email" className="block font-body text-[14px] font-medium text-tr-mist mb-2">
          Email address
        </label>
        <div className="flex flex-col md:flex-row gap-2">
          <input
            id="footer-signup-email"
            type="email"
            name="email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              if (status === "error") {
                setStatus("idle");
                setMessage("");
              }
            }}
            placeholder="you@example.com"
            autoComplete="email"
            inputMode="email"
            autoCapitalize="off"
            spellCheck={false}
            disabled={status === "success" || busy}
            aria-required="true"
            aria-invalid={status === "error" ? "true" : "false"}
            aria-describedby="footer-signup-error footer-signup-privacy"
            className="flex-1 h-10 px-3.5 rounded-lg border border-tr-slate bg-tr-graphite font-body text-[16px] text-tr-paper placeholder:text-tr-dust focus:border-tr-steel focus:outline-2 focus:outline-offset-2 focus:outline-tr-steel disabled:opacity-60"
          />
          <button
            type="submit"
            disabled={status === "success" || busy}
            className="h-10 px-5 rounded-lg border border-tr-slate bg-transparent font-body text-[15px] font-semibold text-tr-paper whitespace-nowrap transition-colors hover:bg-tr-slate/50 disabled:opacity-60"
          >
            {busy ? "Sending…" : "Get updates"}
          </button>
        </div>
        <p
          id="footer-signup-error"
          aria-live="assertive"
          aria-atomic="true"
          data-footer-signup-error
          className={status === "error" ? "mt-2 font-body text-[14px] text-tr-error" : "hidden"}
        >
          {message}
        </p>
      </form>

      <div role="status" aria-atomic="true" className="mt-2">
        {status === "success" && (
          <p className="font-body text-[14px] text-tr-mist">
            You're on the list. We'll only email when there's real news, your address stays private,
            and you can unsubscribe anytime.
          </p>
        )}
      </div>

      <p id="footer-signup-privacy" className="mt-3 font-body text-[14px] leading-[1.5] text-tr-dust">
        We use your email only to send these updates. It's never shared with or used by any third party.
        Unsubscribe anytime.
      </p>
    </>
  );
}

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

        {/* Email signup — sits above the legal links and copyright line (spec: Footer Email Signup HTML Placement V2) */}
        <div className="mt-10 border-t border-tr-slate pt-10">
          <div className="grid md:grid-cols-[1.2fr_1fr] gap-8 md:gap-12">
            <div className="text-center md:text-left">
              <p className="font-mono text-[12px] font-medium uppercase tracking-[0.12em] text-tr-dust">Product Updates</p>
              <h2 className="mt-3 font-heading text-[20px] md:text-[24px] font-semibold leading-[1.2] text-tr-paper">
                Follow what we build next
              </h2>
              <p className="mt-3 max-w-[560px] font-body text-[16px] leading-[1.65] text-tr-mist md:text-left">
                Get product updates and development news from TotalRecalls, including new providers,
                new features, and progress on macOS and Linux.
              </p>
            </div>
            <div className="md:pt-1">
              <SignupForm />
            </div>
          </div>
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
