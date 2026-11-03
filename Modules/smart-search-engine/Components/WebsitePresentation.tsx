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
import { ROADMAP_DROPS, TOTALRECALLS_SPECS } from '../constants';

interface WebsitePresentationProps {
  onSelectTab: (tab: AppTabType) => void;
}

export const WebsitePresentation: React.FC<WebsitePresentationProps> = ({ onSelectTab }) => {
  // 3-page presentation tabs
  const [currentPage, setCurrentPage] = useState<1 | 2 | 3>(1);
  const [selectedDropIdx, setSelectedDropIdx] = useState<number>(0);

  return (
    <div className="space-y-8">
      {/* Presentation Navigation Header Bar */}
      <div className="rounded-2xl bg-[#0c1424] border border-cyan-500/30 p-4 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 to-teal-500 flex items-center justify-center text-slate-950 font-bold shadow-md shadow-cyan-500/20">
            <Sparkles className="w-5 h-5 text-slate-950" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-base font-bold text-white tracking-tight">Website Showcase: Smart Search Engine</h2>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-cyan-500/15 text-cyan-300 border border-cyan-500/30">
                Ready for totalrecalls.app
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Interactive 3-page product landing & feature presentation with 6-Week Staged Drop & Founder's Season Pass launch model.
            </p>
          </div>
        </div>

        {/* 3 Page Switcher Pills */}
        <div className="flex items-center bg-[#070b14] border border-slate-800 rounded-xl p-1 text-xs">
          <button
            onClick={() => setCurrentPage(1)}
            className={`px-3 py-1.5 rounded-lg font-semibold transition-all flex items-center gap-1.5 ${
              currentPage === 1
                ? 'bg-gradient-to-r from-cyan-600 to-teal-600 text-white shadow-md shadow-cyan-500/20'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <span>Page 1: Product Overview</span>
          </button>
          <button
            onClick={() => setCurrentPage(2)}
            className={`px-3 py-1.5 rounded-lg font-semibold transition-all flex items-center gap-1.5 ${
              currentPage === 2
                ? 'bg-gradient-to-r from-cyan-600 to-teal-600 text-white shadow-md shadow-cyan-500/20'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <span>Page 2: Core Features & Benefits</span>
          </button>
          <button
            onClick={() => setCurrentPage(3)}
            className={`px-3 py-1.5 rounded-lg font-semibold transition-all flex items-center gap-1.5 ${
              currentPage === 3
                ? 'bg-gradient-to-r from-cyan-600 to-teal-600 text-white shadow-md shadow-cyan-500/20'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <span>Page 3: Staged Drops & Pricing</span>
          </button>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* PAGE 1: WHAT IT IS — THE SMART SEARCH REVOLUTION                         */}
      {/* ========================================================================= */}
      {currentPage === 1 && (
        <div className="space-y-8 animate-fadeIn">
          {/* Hero Section */}
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-b from-[#0c182b] via-[#091120] to-[#070c16] border border-cyan-500/30 p-8 sm:p-12 text-center space-y-6 shadow-2xl">
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-40 bg-cyan-500/10 blur-[100px] pointer-events-none" />

            <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-semibold">
              <Sparkles className="w-4 h-4 text-cyan-400" />
              <span>Introducing TotalRecalls Smart Search Engine (SSE)</span>
            </div>

            <h1 className="text-3xl sm:text-5xl font-black text-white tracking-tight leading-tight max-w-4xl mx-auto">
              Your Entire AI Chat History.<br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-teal-500">
                Instantly Searchable, Audited, and 100% Offline.
              </span>
            </h1>

            <p className="text-sm sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed">
              Stop digging through endless browser tabs. TotalRecalls unites all your conversations from <strong>ChatGPT, Claude, Gemini, Perplexity, and Mistral</strong> into a private, local knowledge base that answers your questions in milliseconds.
            </p>

            <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
              <button
                onClick={() => onSelectTab('searchChat')}
                className="px-6 py-3 rounded-xl font-bold text-xs sm:text-sm bg-gradient-to-r from-cyan-500 to-teal-600 hover:from-cyan-400 hover:to-teal-500 text-slate-950 flex items-center gap-2 transition-all shadow-lg shadow-cyan-500/25"
              >
                <span>Try Search Chat Interactive Demo</span>
                <ArrowRight className="w-4 h-4" />
              </button>
              <button
                onClick={() => setCurrentPage(3)}
                className="px-6 py-3 rounded-xl font-semibold text-xs sm:text-sm bg-[#0c1424] hover:bg-slate-800 text-slate-200 border border-slate-700 transition-colors flex items-center gap-2"
              >
                <Calendar className="w-4 h-4 text-cyan-400" />
                <span>View 6-Week Drop Roadmap & Pass</span>
              </button>
            </div>

            {/* Launch Callout Banner */}
            <div className="pt-4 max-w-xl mx-auto">
              <div className="p-3 rounded-xl bg-cyan-950/40 border border-cyan-500/30 text-xs text-cyan-200 flex items-center justify-between">
                <span className="flex items-center gap-2 font-medium">
                  <Tag className="w-4 h-4 text-cyan-400" />
                  <strong>Launch Special:</strong> Founder's Season Pass — $49 (All 6 Weekly Drops Included)
                </span>
                <span className="text-slate-400 line-through">$140</span>
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
              <ul className="space-y-3 text-xs sm:text-sm text-slate-300">
                <li className="flex items-start gap-2">
                  <span className="text-rose-400 font-bold">✕</span>
                  <span><strong>Scattered Knowledge:</strong> Your best ideas, code, and strategies are trapped in separate tabs across 5 different AI services.</span>
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

            <div className="rounded-2xl bg-gradient-to-br from-cyan-950/40 via-[#0c1424] to-[#0c1424] border border-cyan-500/40 p-6 space-y-4">
              <div className="flex items-center space-x-2 text-cyan-400">
                <span className="w-2 h-2 rounded-full bg-cyan-400" />
                <h3 className="text-base font-bold uppercase tracking-wider">The TotalRecalls Breakthrough</h3>
              </div>
              <ul className="space-y-3 text-xs sm:text-sm text-slate-200">
                <li className="flex items-start gap-2">
                  <Check className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
                  <span><strong>Unified Intelligence Vault:</strong> Seamlessly pulls chats from ChatGPT, Claude, Gemini, Perplexity, and Mistral into one local hub.</span>
                </li>
                <li className="flex items-start gap-2">
                  <Check className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
                  <span><strong>Meaning-Based Semantic Search:</strong> Finds answers based on concepts and ideas, even when the wording is totally different.</span>
                </li>
                <li className="flex items-start gap-2">
                  <Check className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
                  <span><strong>AI Consensus & Peer Review:</strong> Automatically compares answers from different models to flag contradictions and verify accuracy.</span>
                </li>
                <li className="flex items-start gap-2">
                  <Check className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
                  <span><strong>100% Air-Gapped Security:</strong> Runs entirely on your computer's hard drive. Zero cloud uploads, zero network leaks.</span>
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
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
              Six Game-Changing Innovations
            </h2>
            <p className="text-slate-400 text-xs sm:text-sm">
              Discover how the Smart Search Engine upgrades TotalRecalls from a simple downloader into the market-leading local AI operating system.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Feature 1 */}
            <div className="p-6 rounded-2xl bg-[#0c1424] border border-slate-800 hover:border-cyan-500/50 transition-all space-y-3 group">
              <div className="w-10 h-10 rounded-xl bg-cyan-500/15 border border-cyan-500/30 flex items-center justify-center text-cyan-400 group-hover:scale-110 transition-transform">
                <Search className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-white">1. Smart Semantic Search</h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                Understands meaning, not just exact keywords. Search for <em>"database speedups"</em> and it instantly surfaces discussions on <em>"indexing PostgreSQL with pgvector"</em>.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="p-6 rounded-2xl bg-[#0c1424] border border-slate-800 hover:border-teal-500/50 transition-all space-y-3 group">
              <div className="w-10 h-10 rounded-xl bg-teal-500/15 border border-teal-500/30 flex items-center justify-center text-teal-400 group-hover:scale-110 transition-transform">
                <Terminal className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-white">2. Ask in English, Query with SQL</h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                Ask questions like <em>"Which AI did I talk to most last month?"</em> and watch it automatically generate and run structured SQLite queries without writing code.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="p-6 rounded-2xl bg-[#0c1424] border border-slate-800 hover:border-cyan-500/50 transition-all space-y-3 group">
              <div className="w-10 h-10 rounded-xl bg-cyan-500/15 border border-cyan-500/30 flex items-center justify-center text-cyan-400 group-hover:scale-110 transition-transform">
                <GitCompare className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-white">3. Cross-AI Consensus Auditor</h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                Your personal AI Peer Review Board. Pit ChatGPT, Claude, and Gemini against each other on the same question to pinpoint contradictions and verified facts.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="p-6 rounded-2xl bg-[#0c1424] border border-slate-800 hover:border-teal-500/50 transition-all space-y-3 group">
              <div className="w-10 h-10 rounded-xl bg-teal-500/15 border border-teal-500/30 flex items-center justify-center text-teal-400 group-hover:scale-110 transition-transform">
                <Lock className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-white">4. Air-Gap Secret Scrubber</h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                Never accidentally leak a secret. Automatically detects and redacts Stripe keys, passwords, client emails, and AWS credentials right on your local machine.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="p-6 rounded-2xl bg-[#0c1424] border border-slate-800 hover:border-cyan-500/50 transition-all space-y-3 group">
              <div className="w-10 h-10 rounded-xl bg-cyan-500/15 border border-cyan-500/30 flex items-center justify-center text-cyan-400 group-hover:scale-110 transition-transform">
                <FileCode className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-white">5. 1-Click Fine-Tuning Pipeline</h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                Transform your saved conversations into clean, ready-to-train JSONL or Alpaca datasets to train your own specialized private AI models.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="p-6 rounded-2xl bg-[#0c1424] border border-slate-800 hover:border-teal-500/50 transition-all space-y-3 group">
              <div className="w-10 h-10 rounded-xl bg-teal-500/15 border border-teal-500/30 flex items-center justify-center text-teal-400 group-hover:scale-110 transition-transform">
                <Brain className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-white">6. Topic Graph & Dimension Benchmarks</h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                Visualize all your discussions as interactive knowledge topic cards, and benchmark local embedding speeds on your specific CPU/GPU hardware.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* PAGE 3: 6-WEEK STAGED DROPS, FOUNDER'S SEASON PASS & PRICING             */}
      {/* ========================================================================= */}
      {currentPage === 3 && (
        <div className="space-y-10 animate-fadeIn">
          {/* Section 1: The 6-Week Feature Drop Schedule */}
          <div className="space-y-4">
            <div className="text-center max-w-3xl mx-auto space-y-2">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-500/15 border border-cyan-500/40 text-cyan-300 text-xs font-semibold">
                <Calendar className="w-3.5 h-3.5 text-cyan-400" />
                <span>6-Week Staged Release & Constant Innovation Stream</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
                Weekly Feature Drops & Modular A-La-Carte Pricing
              </h2>
              <p className="text-slate-400 text-xs sm:text-sm">
                To guarantee steady innovation and keep pricing accessible, each major capability can be unlocked individually—or bundled together with our massive Launch Week Founder's Pass discount.
              </p>
            </div>

            {/* Interactive Timeline Tabs */}
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
              {ROADMAP_DROPS.map((drop, idx) => (
                <button
                  key={drop.week}
                  onClick={() => setSelectedDropIdx(idx)}
                  className={`p-3 rounded-xl border text-left transition-all relative ${
                    selectedDropIdx === idx
                      ? 'bg-cyan-950/60 border-cyan-500 text-white shadow-lg shadow-cyan-500/15'
                      : 'bg-[#0c1424] border-slate-800 text-slate-400 hover:border-slate-700 hover:text-slate-200'
                  }`}
                >
                  <div className="flex items-center justify-between text-[11px] font-mono mb-1">
                    <span className="text-cyan-400 font-bold">Week {drop.week}</span>
                    <span className={`px-1.5 py-0.2 rounded text-[9px] font-bold ${
                      drop.status === 'live' ? 'bg-teal-500/20 text-teal-300' :
                      drop.status === 'next_up' ? 'bg-cyan-500/20 text-cyan-300' : 'bg-slate-800 text-slate-400'
                    }`}>
                      {drop.status === 'live' ? 'LIVE' : drop.status === 'next_up' ? 'NEXT' : 'SOON'}
                    </span>
                  </div>
                  <div className="text-xs font-bold line-clamp-1 text-slate-100">{drop.title.split('(')[0]}</div>
                  <div className="text-[11px] font-semibold text-slate-300 mt-1">{drop.standalonePrice} a-la-carte</div>
                </button>
              ))}
            </div>

            {/* Selected Drop Detail Card */}
            {(() => {
              const activeDrop = ROADMAP_DROPS[selectedDropIdx];
              return (
                <div className="rounded-2xl bg-[#0c1424] border border-cyan-500/40 p-6 space-y-4 shadow-xl">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800/80 pb-4">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                          {activeDrop.releaseDate}
                        </span>
                        <span className="text-xs text-slate-400 uppercase tracking-wider">{activeDrop.category}</span>
                      </div>
                      <h3 className="text-xl font-extrabold text-white mt-1">{activeDrop.title}</h3>
                      <p className="text-xs text-cyan-300 mt-0.5">{activeDrop.tagline}</p>
                    </div>

                    <div className="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center">
                      <div className="text-xs text-slate-400">Standalone A-La-Carte:</div>
                      <div className="text-2xl font-black text-white">{activeDrop.standalonePrice}</div>
                      <span className="text-[10px] text-teal-400 font-medium">Included in Founder's Pass</span>
                    </div>
                  </div>

                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                    {activeDrop.description}
                  </p>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                    {activeDrop.features.map((feat, fIdx) => (
                      <div key={fIdx} className="flex items-center gap-2 text-xs text-slate-200">
                        <Check className="w-3.5 h-3.5 text-cyan-400 flex-shrink-0" />
                        <span>{feat}</span>
                      </div>
                    ))}
                  </div>

                  <div className="pt-3 border-t border-slate-800/80 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs">
                    <span className="text-slate-400">
                      <strong>Best For:</strong> {activeDrop.targetAudience}
                    </span>
                    <button
                      onClick={() => onSelectTab('searchChat')}
                      className="px-4 py-2 rounded-xl bg-[#070b14] hover:bg-slate-800 text-cyan-300 border border-cyan-500/30 font-semibold transition-colors flex items-center gap-1.5"
                    >
                      <span>Explore this feature live in demo</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              );
            })()}
          </div>

          {/* Section 2: Pricing Matrix with Founder's Season Pass vs Core */}
          <div className="space-y-6 pt-4">
            <div className="text-center max-w-2xl mx-auto space-y-1">
              <h3 className="text-2xl font-bold text-white tracking-tight">Commercial Packaging & Launch Tiers</h3>
              <p className="text-xs text-slate-400">
                A-la-carte sum-of-parts value: <strong className="text-slate-200">$140</strong>. Save big with the early-bird Founder's Season Pass.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Tier 1: Core Downloader */}
              <div className="rounded-2xl p-6 bg-[#0c1424] border border-slate-800 flex flex-col justify-between space-y-6">
                <div className="space-y-3">
                  <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Baseline Unit</span>
                  <h4 className="text-xl font-bold text-white">Core Downloader</h4>
                  <div className="flex items-baseline space-x-1">
                    <span className="text-3xl font-extrabold text-white">$29</span>
                    <span className="text-xs text-slate-400">/ one-time lifetime</span>
                  </div>
                  <p className="text-xs text-slate-400">
                    Never lose a conversation. Automated local chat export across all providers.
                  </p>
                  <div className="space-y-2 pt-3 border-t border-slate-800 text-xs text-slate-300">
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-teal-400" /><span>Scrapers for ChatGPT, Claude, Gemini, Perplexity, Mistral</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-teal-400" /><span>JSON, Markdown, Raw HTML, PDF local exports</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-teal-400" /><span>Encrypted offline storage vault</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-teal-400" /><span>Basic full-text keyword search</span></div>
                  </div>
                </div>
                <a
                  href="https://totalrecalls.app"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full py-2.5 rounded-xl font-bold text-xs bg-[#070b14] hover:bg-slate-800 text-slate-200 border border-slate-700 text-center block transition-colors"
                >
                  Get Core Downloader ($29)
                </a>
              </div>

              {/* Tier 2: Founder's Season Pass */}
              <div className="rounded-2xl p-6 bg-gradient-to-b from-cyan-950/70 via-[#0c1424] to-[#0c1424] border-2 border-cyan-400 flex flex-col justify-between space-y-6 relative shadow-2xl shadow-cyan-500/20">
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full bg-gradient-to-r from-cyan-400 to-teal-400 text-slate-950 font-bold text-[10px] uppercase tracking-wider shadow">
                  Launch Week Special • 65% Off
                </div>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-cyan-400 uppercase tracking-wider">Smart Search Engine Bundle</span>
                    <span className="text-xs text-slate-400 line-through">$140</span>
                  </div>
                  <h4 className="text-xl font-bold text-white">Founder's Season Pass</h4>
                  <div className="flex items-baseline space-x-1.5">
                    <span className="text-3xl font-black text-white">$49</span>
                    <span className="text-xs text-cyan-300 font-medium">Launch Special</span>
                    <span className="text-xs text-slate-400">/ then $59</span>
                  </div>
                  <p className="text-xs text-slate-300">
                    Immediate unlock of Week 1 Tri-Mode Search + automatic lifetime access to all 6 upcoming weekly feature drops.
                  </p>
                  <div className="space-y-2 pt-3 border-t border-slate-800 text-xs text-slate-200">
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-cyan-400" /><span><strong>Week 1 Live:</strong> Tri-Mode Vector + SQL + RRF Search ($39)</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-cyan-400" /><span><strong>Week 2 Drop:</strong> Air-Gap PII Redaction Scrubber ($19)</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-cyan-400" /><span><strong>Week 3 Drop:</strong> Fine-Tuning Pipeline (JSONL/Alpaca) ($19)</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-cyan-400" /><span><strong>Week 4 Drop:</strong> Cross-AI Consensus Auditor ($25)</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-cyan-400" /><span><strong>Week 5 Drop:</strong> Vault Knowledge Graph & Topic Cards ($19)</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-cyan-400" /><span><strong>Week 6 Drop:</strong> Embedding Benchmark & 2D PCA Map ($19)</span></div>
                  </div>
                </div>
                <a
                  href="https://totalrecalls.app"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full py-2.5 rounded-xl font-bold text-xs bg-gradient-to-r from-cyan-500 to-teal-600 hover:from-cyan-400 hover:to-teal-500 text-slate-950 text-center block transition-all shadow-md shadow-cyan-500/20"
                >
                  Claim Founder's Pass ($49)
                </a>
              </div>

              {/* Tier 3: Enterprise */}
              <div className="rounded-2xl p-6 bg-[#0c1424] border border-slate-800 flex flex-col justify-between space-y-6">
                <div className="space-y-3">
                  <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Enterprise & Teams</span>
                  <h4 className="text-xl font-bold text-white">Local Fleet License</h4>
                  <div className="flex items-baseline space-x-1">
                    <span className="text-3xl font-extrabold text-white">$149</span>
                    <span className="text-xs text-slate-400">/ per seat perpetual</span>
                  </div>
                  <p className="text-xs text-slate-400">
                    For engineering organizations, law firms, and research labs managing collective AI memory.
                  </p>
                  <div className="space-y-2 pt-3 border-t border-slate-800 text-xs text-slate-300">
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-teal-400" /><span>All 6 Feature Drops unlocked immediately</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-teal-400" /><span>Peer-to-peer encrypted knowledge sync</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-teal-400" /><span>Centralized compliance & PII audit reports</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-teal-400" /><span>Custom self-hosted Ollama fleets & models</span></div>
                    <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-teal-400" /><span>Dedicated engineering onboarding</span></div>
                  </div>
                </div>
                <a
                  href="https://totalrecalls.app"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full py-2.5 rounded-xl font-bold text-xs bg-[#070b14] hover:bg-slate-800 text-slate-200 border border-slate-700 text-center block transition-colors"
                >
                  Contact Enterprise Fleet
                </a>
              </div>
            </div>
          </div>

          {/* User Documentation Callout */}
          <div className="p-6 rounded-2xl bg-[#0c1424] border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="space-y-1">
              <span className="text-xs font-mono text-cyan-400">Included Documentation</span>
              <h4 className="text-base font-bold text-white">Complete Manuals in .PDF, .DOCX, and .MD Formats</h4>
              <p className="text-xs text-slate-400">
                Includes both our <strong>Everyday User Manual</strong> (for beginners) and our <strong>Power User Technical Reference</strong> with drop schedules.
              </p>
            </div>
            <button
              onClick={() => onSelectTab('manual')}
              className="px-4 py-2 bg-[#070b14] hover:bg-slate-800 text-cyan-400 border border-cyan-500/30 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors whitespace-nowrap"
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span>Read Manuals Now</span>
            </button>
          </div>
        </div>
      )}

      {/* Pagination Footer Controls */}
      <div className="pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
        <button
          disabled={currentPage === 1}
          onClick={() => setCurrentPage(prev => Math.max(1, prev - 1) as any)}
          className="px-3.5 py-1.5 rounded-lg bg-[#0c1424] border border-slate-800 text-slate-300 disabled:opacity-30 disabled:hover:bg-[#0c1424] hover:bg-slate-800 transition-colors"
        >
          ← Previous Page
        </button>

        <span className="font-mono text-slate-500">
          Page {currentPage} of 3 • TotalRecalls Presentation Showcase
        </span>

        <button
          disabled={currentPage === 3}
          onClick={() => setCurrentPage(prev => Math.min(3, prev + 1) as any)}
          className="px-4 py-1.5 rounded-lg bg-gradient-to-r from-cyan-600 to-teal-600 hover:from-cyan-500 hover:to-teal-500 disabled:opacity-30 text-white font-bold transition-all shadow"
        >
          Next Page →
        </button>
      </div>
    </div>
  );
};
