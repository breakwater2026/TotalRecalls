import React, { useState } from 'react';
import { 
  Sparkles, 
  Database, 
  Cpu, 
  ShieldCheck, 
  Search, 
  Terminal, 
  GitCompare, 
  Lock, 
  Layers, 
  ArrowRight, 
  CheckCircle2, 
  Zap, 
  HardDrive, 
  Check, 
  BookOpen, 
  ExternalLink,
  ChevronRight,
  TrendingUp,
  Brain,
  Download,
  Users,
  Shield,
  FileCode,
  Sliders,
  Award,
  Calendar,
  Gift,
  Clock,
  Tag
} from 'lucide-react';
import { AppTabType } from './Navbar';

interface WebsitePresentationProps {
  onSelectTab: (tab: AppTabType) => void;
}

export const WebsitePresentation: React.FC<WebsitePresentationProps> = ({ onSelectTab }) => {
  // 3-page presentation tabs
  const [currentPage, setCurrentPage] = useState<1 | 2 | 3>(1);

  return (
    <div className="space-y-8">
      {/* Presentation Navigation Header Bar */}
      <div className="rounded-2xl bg-[var(--tr-panel)] border border-[var(--tr-accent)]/30 p-4 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-[var(--tr-accent)] to-[var(--tr-accent2)] flex items-center justify-center text-[var(--tr-text)] font-bold shadow-md shadow">
            <Sparkles className="w-5 h-5 text-[var(--tr-text)]" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-base font-bold text-[var(--tr-text)] tracking-tight">Website Showcase: Smart Search Engine</h2>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-[var(--tr-accent)]/15 text-[var(--tr-accent)] border border-[var(--tr-accent)]/30">
                Ready for totalrecalls.app
              </span>
            </div>
            <p className="text-xs text-[var(--tr-muted)]">
              Interactive product presentation for TotalRecalls Pro and the Smart Search Engine add-on.
            </p>
          </div>
        </div>

        {/* 3 Page Switcher Pills */}
        <div className="flex items-center bg-[var(--tr-panel2)] border border-[var(--tr-border)] rounded-xl p-1 text-xs">
          <button
            onClick={() => setCurrentPage(1)}
            className={`px-3 py-1.5 rounded-lg font-semibold transition-all flex items-center gap-1.5 ${
              currentPage === 1
                ? 'bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] text-[var(--tr-text)] shadow-md shadow'
                : 'text-[var(--tr-muted)] hover:text-[var(--tr-text)]'
            }`}
          >
            <span>Page 1: Product Overview</span>
          </button>
          <button
            onClick={() => setCurrentPage(2)}
            className={`px-3 py-1.5 rounded-lg font-semibold transition-all flex items-center gap-1.5 ${
              currentPage === 2
                ? 'bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] text-[var(--tr-text)] shadow-md shadow'
                : 'text-[var(--tr-muted)] hover:text-[var(--tr-text)]'
            }`}
          >
            <span>Page 2: Core Features & Benefits</span>
          </button>
          <button
            onClick={() => setCurrentPage(3)}
            className={`px-3 py-1.5 rounded-lg font-semibold transition-all flex items-center gap-1.5 ${
              currentPage === 3
                ? 'bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] text-[var(--tr-text)] shadow-md shadow'
                : 'text-[var(--tr-muted)] hover:text-[var(--tr-text)]'
            }`}
          >
            <span>Page 3: What's Included & Pricing</span>
          </button>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* PAGE 1: WHAT IT IS — THE SMART SEARCH REVOLUTION                         */}
      {/* ========================================================================= */}
      {currentPage === 1 && (
        <div className="space-y-8 animate-fadeIn">
          {/* Hero Section */}
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-b from-[#0c182b] via-[#091120] to-[var(--tr-bg)] border border-[var(--tr-accent)]/30 p-8 sm:p-12 text-center space-y-6 shadow-2xl">
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-40 bg-[var(--tr-accent)]/10 blur-[100px] pointer-events-none" />

            <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-[var(--tr-accent)]/10 border border-[var(--tr-accent)]/30 text-[var(--tr-accent)] text-xs font-semibold">
              <Sparkles className="w-4 h-4 text-[var(--tr-accent)]" />
              <span>Introducing TotalRecalls Smart Search Engine (SSE)</span>
            </div>

            <h1 className="text-3xl sm:text-5xl font-black text-[var(--tr-text)] tracking-tight leading-tight max-w-4xl mx-auto">
              Your Entire AI Chat History.<br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[var(--tr-accent)] via-[var(--tr-accent)] to-[var(--tr-accent2)]">
                Instantly Searchable, Audited, and Private on Your PC.
              </span>
            </h1>

            <p className="text-sm sm:text-lg text-[var(--tr-muted)] max-w-2xl mx-auto leading-relaxed">
              Stop digging through endless browser tabs. TotalRecalls unites all your conversations from <strong>ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen</strong> into a private, local knowledge base that answers your questions in milliseconds.
            </p>

            <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
              <button
                onClick={() => onSelectTab('searchChat')}
                className="px-6 py-3 rounded-xl font-bold text-xs sm:text-sm bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] hover:from-[var(--tr-accent)] hover:to-[var(--tr-accent2)] text-[var(--tr-text)] flex items-center gap-2 transition-all shadow-lg shadow"
              >
                <span>Try Search Chat Interactive Demo</span>
                <ArrowRight className="w-4 h-4" />
              </button>
              <button
                onClick={() => setCurrentPage(3)}
                className="px-6 py-3 rounded-xl font-semibold text-xs sm:text-sm bg-[var(--tr-panel)] hover:bg-[var(--tr-panel)] text-[var(--tr-text)] border border-[var(--tr-border)] transition-colors flex items-center gap-2"
              >
                <Calendar className="w-4 h-4 text-[var(--tr-accent)]" />
                <span>View What's Included & Pricing</span>
              </button>
            </div>

            {/* Launch pricing banner */}
            <div className="pt-4 max-w-xl mx-auto">
              <div className="p-3 rounded-xl bg-[var(--tr-accent)]/40 border border-[var(--tr-accent)]/30 text-xs text-[var(--tr-accent)] flex items-center justify-between">
                <span className="flex items-center gap-2 font-medium">
                  <Tag className="w-4 h-4 text-[var(--tr-accent)]" />
                  <strong>Launch pricing:</strong>
                </span>
                <span>
                  Smart Search Engine $29 one-time (regular $58) &middot; Pro + SSE bundle $49.89.
                </span>
              </div>
            </div>
          </div>

          {/* The Problem vs Solution Dual Matrix */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="rounded-2xl bg-[#0e1422] border border-red-500/20 p-6 space-y-4">
              <div className="flex items-center space-x-2 text-rose-400">
                <span className="w-2 h-2 rounded-full bg-rose-500" />
                <h3 className="text-base font-bold uppercase tracking-wider">The Problem Today</h3>
              </div>
              <ul className="space-y-3 text-xs sm:text-sm text-[var(--tr-muted)]">
                <li className="flex items-start gap-2">
                  <span className="text-rose-400 font-bold">✕</span>
                  <span><strong>Scattered Knowledge:</strong> Your best ideas, code, and strategies are trapped in separate tabs across 8 AI services.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-rose-400 font-bold">✕</span>
                  <span><strong>Keyword Blindness:</strong> Standard search fails if you don't recall the exact word you typed two months ago.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-rose-400 font-bold">✕</span>
                  <span><strong>AI Disagreements & Hallucinations:</strong> You don't know if Claude or ChatGPT gave the right advice without tedious manual comparison.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-rose-400 font-bold">✕</span>
                  <span><strong>Privacy Risk:</strong> Uploading your confidential chats to another cloud service exposes passwords, API keys, and client secrets.</span>
                </li>
              </ul>
            </div>

            <div className="rounded-2xl bg-gradient-to-br from-[var(--tr-accent)]/40 via-[var(--tr-panel)] to-[var(--tr-panel)] border border-[var(--tr-accent)]/40 p-6 space-y-4">
              <div className="flex items-center space-x-2 text-[var(--tr-accent)]">
                <span className="w-2 h-2 rounded-full bg-[var(--tr-accent)]" />
                <h3 className="text-base font-bold uppercase tracking-wider">The TotalRecalls Breakthrough</h3>
              </div>
              <ul className="space-y-3 text-xs sm:text-sm text-[var(--tr-text)]">
                <li className="flex items-start gap-2">
                  <Check className="w-4 h-4 text-[var(--tr-accent)] flex-shrink-0 mt-0.5" />
                  <span><strong>Unified Intelligence Vault:</strong> Seamlessly pulls chats from ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen into one local hub.</span>
                </li>
                <li className="flex items-start gap-2">
                  <Check className="w-4 h-4 text-[var(--tr-accent)] flex-shrink-0 mt-0.5" />
                  <span><strong>Meaning-Based Semantic Search:</strong> Finds answers based on concepts and ideas, even when the wording is totally different.</span>
                </li>
                <li className="flex items-start gap-2">
                  <Check className="w-4 h-4 text-[var(--tr-accent)] flex-shrink-0 mt-0.5" />
                  <span><strong>AI Consensus & Peer Review:</strong> Automatically compares answers from different models to flag contradictions and verify accuracy.</span>
                </li>
                <li className="flex items-start gap-2">
                  <Check className="w-4 h-4 text-[var(--tr-accent)] flex-shrink-0 mt-0.5" />
                  <span><strong>Private on your PC:</strong> Runs on your computer. Nothing you write or save is uploaded.</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* PAGE 2: CORE FEATURES & BENEFITS                                         */}
      {/* ========================================================================= */}
      {currentPage === 2 && (
        <div className="space-y-8 animate-fadeIn">
          <div className="text-center max-w-3xl mx-auto space-y-3">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-[var(--tr-text)] tracking-tight">
              Six Game-Changing Innovations
            </h2>
            <p className="text-[var(--tr-muted)] text-xs sm:text-sm">
              Discover how the Smart Search Engine upgrades TotalRecalls from a simple downloader into the market-leading local AI operating system.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Feature 1 */}
            <div className="p-6 rounded-2xl bg-[var(--tr-panel)] border border-[var(--tr-border)] hover:border-[var(--tr-accent)]/50 transition-all space-y-3 group">
              <div className="w-10 h-10 rounded-xl bg-[var(--tr-accent)]/15 border border-[var(--tr-accent)]/30 flex items-center justify-center text-[var(--tr-accent)] group-hover:scale-110 transition-transform">
                <Search className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-[var(--tr-text)]">1. Smart Semantic Search</h3>
              <p className="text-xs text-[var(--tr-muted)] leading-relaxed">
                Understands meaning, not just exact keywords. Search for <em>"database speedups"</em> and it instantly surfaces discussions on <em>"indexing PostgreSQL with pgvector"</em>.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="p-6 rounded-2xl bg-[var(--tr-panel)] border border-[var(--tr-border)] hover:border-[var(--tr-accent)]/50 transition-all space-y-3 group">
              <div className="w-10 h-10 rounded-xl bg-[var(--tr-accent)]/15 border border-[var(--tr-accent)]/30 flex items-center justify-center text-[var(--tr-accent)] group-hover:scale-110 transition-transform">
                <Terminal className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-[var(--tr-text)]">2. Ask in English, Query with SQL</h3>
              <p className="text-xs text-[var(--tr-muted)] leading-relaxed">
                Ask questions like <em>"Which AI did I talk to most last month?"</em> and watch it automatically generate and run structured SQLite queries without writing code.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="p-6 rounded-2xl bg-[var(--tr-panel)] border border-[var(--tr-border)] hover:border-[var(--tr-accent)]/50 transition-all space-y-3 group">
              <div className="w-10 h-10 rounded-xl bg-[var(--tr-accent)]/15 border border-[var(--tr-accent)]/30 flex items-center justify-center text-[var(--tr-accent)] group-hover:scale-110 transition-transform">
                <GitCompare className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-[var(--tr-text)]">3. Cross-AI Consensus Auditor</h3>
              <p className="text-xs text-[var(--tr-muted)] leading-relaxed">
                Your personal AI Peer Review Board. Pit ChatGPT, Claude, and Gemini against each other on the same question to pinpoint contradictions and verified facts.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="p-6 rounded-2xl bg-[var(--tr-panel)] border border-[var(--tr-border)] hover:border-[var(--tr-accent)]/50 transition-all space-y-3 group">
              <div className="w-10 h-10 rounded-xl bg-[var(--tr-accent)]/15 border border-[var(--tr-accent)]/30 flex items-center justify-center text-[var(--tr-accent)] group-hover:scale-110 transition-transform">
                <Lock className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-[var(--tr-text)]">4. PII Secret Scrubber</h3>
              <p className="text-xs text-[var(--tr-muted)] leading-relaxed">
                Never accidentally leak a secret. Automatically detects and redacts Stripe keys, passwords, client emails, and AWS credentials right on your local machine.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="p-6 rounded-2xl bg-[var(--tr-panel)] border border-[var(--tr-border)] hover:border-[var(--tr-accent)]/50 transition-all space-y-3 group">
              <div className="w-10 h-10 rounded-xl bg-[var(--tr-accent)]/15 border border-[var(--tr-accent)]/30 flex items-center justify-center text-[var(--tr-accent)] group-hover:scale-110 transition-transform">
                <FileCode className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-[var(--tr-text)]">5. 1-Click Fine-Tuning Pipeline</h3>
              <p className="text-xs text-[var(--tr-muted)] leading-relaxed">
                Transform your saved conversations into clean, ready-to-train JSONL or Alpaca datasets to train your own specialized private AI models.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="p-6 rounded-2xl bg-[var(--tr-panel)] border border-[var(--tr-border)] hover:border-[var(--tr-accent)]/50 transition-all space-y-3 group">
              <div className="w-10 h-10 rounded-xl bg-[var(--tr-accent)]/15 border border-[var(--tr-accent)]/30 flex items-center justify-center text-[var(--tr-accent)] group-hover:scale-110 transition-transform">
                <Brain className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-[var(--tr-text)]">6. Topic Graph & Dimension Benchmarks</h3>
              <p className="text-xs text-[var(--tr-muted)] leading-relaxed">
                Visualize all your discussions as interactive knowledge topic cards, and benchmark local embedding speeds on your specific CPU/GPU hardware.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* PAGE 3: WHAT'S INCLUDED & PRICING                                        */}
      {/* ========================================================================= */}
      {currentPage === 3 && (
        <div className="space-y-10 animate-fadeIn">
          {/* Section 1: Included at launch vs coming as paid upgrades */}
          <div className="space-y-4">
            <div className="text-center max-w-3xl mx-auto space-y-2">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-[var(--tr-accent)]/15 border border-[var(--tr-accent)]/40 text-[var(--tr-accent)] text-xs font-semibold">
                <Calendar className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
                <span>Smart Search Engine — Included at Launch, Updates Free</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-[var(--tr-text)] tracking-tight">
                What's Included at Launch vs. Coming as Paid Upgrades
              </h2>
              <p className="text-[var(--tr-muted)] text-xs sm:text-sm">
                Smart Search Engine launches with Tri-Mode Search. The PII Scrubber, Fine-Tuning Pipeline, Consensus Auditor, Knowledge Graph, and Embedding Benchmark follow as paid upgrades for Smart Search Engine buyers &mdash; separate purchases, not included.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div className="rounded-2xl bg-[var(--tr-panel)] border border-[var(--tr-accent)]/40 p-6 space-y-4">
                <span className="px-2 py-0.5 rounded text-[10px] font-bold font-mono bg-[var(--tr-accent)]/20 text-[var(--tr-accent)] border border-[var(--tr-accent)]/30">
                  INCLUDED AT LAUNCH
                </span>
                <h3 className="text-lg font-bold text-[var(--tr-text)]">Tri-Mode Search</h3>
                <ul className="space-y-2 text-xs text-[var(--tr-muted)]">
                  <li className="flex items-start gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)] flex-shrink-0 mt-0.5" /><span>Search by meaning, keyword, or both together</span></li>
                  <li className="flex items-start gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)] flex-shrink-0 mt-0.5" /><span>Plain-English questions answered with SQL</span></li>
                  <li className="flex items-start gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)] flex-shrink-0 mt-0.5" /><span>Chat with your archive</span></li>
                  <li className="flex items-start gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)] flex-shrink-0 mt-0.5" /><span>Obsidian and Notion connections</span></li>
                  <li className="flex items-start gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)] flex-shrink-0 mt-0.5" /><span>Automatic re-indexing</span></li>
                </ul>
                <button
                  onClick={() => onSelectTab('searchChat')}
                  className="px-4 py-2 rounded-xl bg-[var(--tr-panel2)] hover:bg-[var(--tr-panel)] text-[var(--tr-accent)] border border-[var(--tr-accent)]/30 font-semibold transition-colors flex items-center gap-1.5 text-xs"
                >
                  <span>Explore this feature live in demo</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>

              <div className="rounded-2xl bg-[var(--tr-panel)] border border-[var(--tr-border)] p-6 space-y-4">
                <span className="px-2 py-0.5 rounded text-[10px] font-bold font-mono bg-[var(--tr-panel)] text-[var(--tr-muted)] border border-[var(--tr-border)]">
                  COMING AS PAID UPGRADES
                </span>
                <h3 className="text-lg font-bold text-[var(--tr-text)]">Paid upgrades for SSE buyers</h3>
                <ul className="space-y-2 text-xs text-[var(--tr-muted)]">
                  <li className="flex items-start gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)] flex-shrink-0 mt-0.5" /><span>PII Scrubber: finds keys, tokens, and emails before you share</span></li>
                  <li className="flex items-start gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)] flex-shrink-0 mt-0.5" /><span>Fine-tuning export (JSONL, Alpaca)</span></li>
                  <li className="flex items-start gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)] flex-shrink-0 mt-0.5" /><span>Consensus Auditor: compare what different AIs told you</span></li>
                  <li className="flex items-start gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)] flex-shrink-0 mt-0.5" /><span>Knowledge Graph: topic cards across providers</span></li>
                  <li className="flex items-start gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)] flex-shrink-0 mt-0.5" /><span>Embedding benchmark and cluster map</span></li>
                </ul>
              </div>
            </div>
          </div>

          {/* Section 2: Pricing Matrix */}
          <div className="space-y-6 pt-4">


            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Tier 1: Pro */}
              <div className="rounded-2xl p-6 bg-[var(--tr-panel)] border border-[var(--tr-border)] flex flex-col justify-between space-y-6">
                <div className="space-y-3">
                  <span className="text-xs font-semibold text-[var(--tr-muted)] uppercase tracking-wider">Downloader</span>
                  <h4 className="text-xl font-bold text-[var(--tr-text)]">TotalRecalls Pro</h4>
                  <div className="flex items-baseline space-x-1">
                    <span className="text-3xl font-extrabold text-[var(--tr-text)]">$24</span>
                    <span className="text-xs text-[var(--tr-muted)] line-through">$48</span>
                  </div>
                  <p className="text-xs text-[var(--tr-muted)]">
                    All 8 providers. Unlimited downloads. Markdown + JSON, saved locally.
                  </p>
                  <div className="space-y-2 pt-3 border-t border-[var(--tr-border)] text-xs text-[var(--tr-muted)]">
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)]" /><span>ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, Qwen</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)]" /><span>Unlimited downloads</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)]" /><span>Up to 3 device activations</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)]" /><span>Free updates (bug fixes) for the life of the product</span></div>
                  </div>
                </div>
                <a
                  href="https://totalrecalls.app/buy/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full py-2.5 rounded-xl font-bold text-xs bg-[var(--tr-panel2)] hover:bg-[var(--tr-panel)] text-[var(--tr-text)] border border-[var(--tr-border)] text-center block transition-colors"
                >
                  Get Pro — $24
                </a>
              </div>

              {/* Tier 2: Smart Search Engine */}
              <div className="rounded-2xl p-6 bg-gradient-to-b from-[var(--tr-accent)]/70 via-[var(--tr-panel)] to-[var(--tr-panel)] border-2 border-[var(--tr-accent)] flex flex-col justify-between space-y-6 relative shadow-2xl shadow">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-[var(--tr-accent)] uppercase tracking-wider">Pro Add-On</span>
                    <span className="text-xs text-[var(--tr-muted)] line-through">$58</span>
                  </div>
                  <h4 className="text-xl font-bold text-[var(--tr-text)]">Smart Search Engine</h4>
                  <div className="flex items-baseline space-x-1">
                    <span className="text-3xl font-black text-[var(--tr-text)]">$29</span>
                    <span className="text-xs text-[var(--tr-accent)] font-medium">Launch Special</span>
                  </div>
                  <p className="text-xs text-[var(--tr-muted)]">
                    Semantic search across your local archive. Requires Pro.
                  </p>
                  <div className="space-y-2 pt-3 border-t border-[var(--tr-border)] text-xs text-[var(--tr-text)]">
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)]" /><span><strong>Tri-Mode Search:</strong> Vector + SQL + RRF</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)]" /><span>Obsidian and Notion connections</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)]" /><span>Automatic re-indexing</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)]" /><span>Free updates (bug fixes) to SSE</span></div>
                  </div>
                </div>
                <a
                  href="https://totalrecalls.app/smart-search/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full py-2.5 rounded-xl font-bold text-xs bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] hover:from-[var(--tr-accent)] hover:to-[var(--tr-accent2)] text-[var(--tr-text)] text-center block transition-all shadow-md shadow"
                >
                  Add SSE to Pro — $29
                </a>
              </div>

              {/* Tier 3: Bundle */}
              <div className="rounded-2xl p-6 bg-[var(--tr-panel)] border border-[var(--tr-border)] flex flex-col justify-between space-y-6">
                <div className="space-y-3">
                  <span className="text-xs font-semibold text-[var(--tr-muted)] uppercase tracking-wider">Best Value</span>
                  <h4 className="text-xl font-bold text-[var(--tr-text)]">Pro + Smart Search Engine</h4>
                  <div className="flex items-baseline space-x-1">
                    <span className="text-3xl font-extrabold text-[var(--tr-text)]">$49.89</span>
                    <span className="text-xs text-[var(--tr-muted)] line-through">$99.89</span>
                  </div>
                  <p className="text-xs text-[var(--tr-muted)]">
                    Pro and Smart Search Engine together.
                  </p>
                  <div className="space-y-2 pt-3 border-t border-[var(--tr-border)] text-xs text-[var(--tr-muted)]">
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)]" /><span>All 8 providers, unlimited downloads</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)]" /><span>Smart Search Engine semantic search</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)]" /><span>Obsidian and Notion connections</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-[var(--tr-accent)]" /><span>Free updates (bug fixes) to both</span></div>
                  </div>
                </div>
                <a
                  href="https://totalrecalls.app/smart-search/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full py-2.5 rounded-xl font-bold text-xs bg-[var(--tr-panel2)] hover:bg-[var(--tr-panel)] text-[var(--tr-text)] border border-[var(--tr-border)] text-center block transition-colors"
                >
                  Buy the Bundle — $49.89
                </a>
              </div>
            </div>
          </div>

          {/* User Documentation Callout */}
          <div className="p-6 rounded-2xl bg-[var(--tr-panel)] border border-[var(--tr-border)] flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="space-y-1">
              <span className="text-xs font-mono text-[var(--tr-accent)]">Included Documentation</span>
              <h4 className="text-base font-bold text-[var(--tr-text)]">Complete Manuals in .PDF, .DOCX, and .MD Formats</h4>
              <p className="text-xs text-[var(--tr-muted)]">
                Includes both our <strong>Everyday User Manual</strong> (for beginners) and our <strong>Power User Technical Reference</strong> with technical reference material.
              </p>
            </div>
            <button
              onClick={() => onSelectTab('manual')}
              className="px-4 py-2 bg-[var(--tr-panel2)] hover:bg-[var(--tr-panel)] text-[var(--tr-accent)] border border-[var(--tr-accent)]/30 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors whitespace-nowrap"
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span>Read Manuals Now</span>
            </button>
          </div>
        </div>
      )}

      {/* Pagination Footer Controls */}
      <div className="pt-4 border-t border-[var(--tr-border)] flex items-center justify-between text-xs text-[var(--tr-muted)]">
        <button
          disabled={currentPage === 1}
          onClick={() => setCurrentPage(prev => Math.max(1, prev - 1) as any)}
          className="px-3.5 py-1.5 rounded-lg bg-[var(--tr-panel)] border border-[var(--tr-border)] text-[var(--tr-muted)] disabled:opacity-30 disabled:hover:bg-[var(--tr-panel)] hover:bg-[var(--tr-panel)] transition-colors"
        >
          ← Previous Page
        </button>

        <span className="font-mono text-[var(--tr-muted)]">
          Page {currentPage} of 3 • TotalRecalls Presentation Showcase
        </span>

        <button
          disabled={currentPage === 3}
          onClick={() => setCurrentPage(prev => Math.min(3, prev + 1) as any)}
          className="px-4 py-1.5 rounded-lg bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] hover:from-[var(--tr-accent)] hover:to-[var(--tr-accent2)] disabled:opacity-30 text-[var(--tr-text)] font-bold transition-all shadow"
        >
          Next Page →
        </button>
      </div>
    </div>
  );
};
