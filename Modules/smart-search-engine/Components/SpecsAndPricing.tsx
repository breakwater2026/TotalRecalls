import React, { useState } from 'react';
import { 
  Check, 
  Sparkles, 
  Database, 
  Cpu, 
  ShieldCheck, 
  Terminal, 
  HardDrive, 
  ArrowRight, 
  ExternalLink,
  GitCompare,
  Lock,
  Network,
  Calendar,
  Tag,
  Clock,
  Layers
} from 'lucide-react';
import { TOTALRECALLS_SPECS, ROADMAP_DROPS } from '../constants';
import { AppTabType } from './Navbar';

interface SpecsAndPricingProps {
  onSelectTab?: (tab: AppTabType) => void;
}

export const SpecsAndPricing: React.FC<SpecsAndPricingProps> = ({ onSelectTab }) => {
  const [activeTab, setActiveTab] = useState<'tiers' | 'drops'>('tiers');

  return (
    <div className="space-y-10">
      {/* Product launch announcement */}
      <div className="text-center max-w-3xl mx-auto space-y-4">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-500/15 border border-cyan-500/40 text-cyan-300 text-xs font-semibold">
          <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
          <span>Market-Leader Dual Launch: Core Downloader + Smart Search Engine v2.5.0</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Commercial Packaging & Staged Feature Drops
        </h2>
        <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
          In strict accordance with the TotalRecalls product roadmap (<a href="https://totalrecalls.app" target="_blank" rel="noopener noreferrer" className="text-cyan-400 underline underline-offset-4">totalrecalls.app</a>): pairing the $29 core chat downloader with a modular 6-week feature drop schedule ($9–$25 each) or an all-inclusive <strong>Founder's Season Pass ($49 Launch Week / $59 standard)</strong>.
        </p>
      </div>

      {/* Switcher: Pricing Tiers vs 6-Week Roadmap Drops */}
      <div className="flex justify-center">
        <div className="inline-flex items-center bg-[#070b14] border border-slate-800 rounded-xl p-1 text-xs">
          <button
            onClick={() => setActiveTab('tiers')}
            className={`px-4 py-2 rounded-lg font-bold transition-all flex items-center gap-2 ${
              activeTab === 'tiers'
                ? 'bg-gradient-to-r from-cyan-600 to-teal-600 text-white shadow-md shadow-cyan-500/20'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Tag className="w-3.5 h-3.5" />
            <span>Commercial Pricing Tiers</span>
          </button>
          <button
            onClick={() => setActiveTab('drops')}
            className={`px-4 py-2 rounded-lg font-bold transition-all flex items-center gap-2 ${
              activeTab === 'drops'
                ? 'bg-gradient-to-r from-cyan-600 to-teal-600 text-white shadow-md shadow-cyan-500/20'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Calendar className="w-3.5 h-3.5" />
            <span>6-Week Staged Drops Schedule ($140 Value)</span>
          </button>
        </div>
      </div>

      {activeTab === 'tiers' && (
        <>
          {/* Pricing and Packaging Matrix */}
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {TOTALRECALLS_SPECS.pricingTiers.map((tier, idx) => (
                <div
                  key={idx}
                  className={`rounded-2xl p-6 flex flex-col justify-between space-y-6 relative transition-all ${
                    tier.featured
                      ? 'bg-gradient-to-b from-cyan-950/60 via-[#0c1424] to-[#0c1424] border-2 border-cyan-400 shadow-2xl shadow-cyan-500/15'
                      : 'bg-[#0c1424] border border-slate-800'
                  }`}
                >
                  {tier.featured && (
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full bg-gradient-to-r from-cyan-400 to-teal-400 text-slate-950 font-bold text-[10px] uppercase tracking-wider shadow">
                      Early-Bird Founder's Pass • 65% Savings
                    </div>
                  )}

                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-semibold text-cyan-400 uppercase tracking-wider">
                        {tier.badge}
                      </span>
                      {tier.featured && (
                        <span className="text-xs text-slate-400 line-through">
                          {TOTALRECALLS_SPECS.sumOfPartsPrice}
                        </span>
                      )}
                    </div>

                    <h4 className="text-xl font-bold text-white">{tier.name}</h4>
                    <p className="text-xs text-slate-400">{tier.subtitle}</p>

                    <div className="flex items-baseline space-x-1">
                      <span className="text-3xl font-black text-white">{tier.price}</span>
                      <span className="text-xs text-slate-400">/ {tier.period}</span>
                    </div>

                    {tier.featured && (
                      <div className="p-2.5 rounded-lg bg-cyan-950/40 border border-cyan-500/30 text-[11px] text-cyan-300">
                        {tier.savings}
                      </div>
                    )}

                    <div className="space-y-2 pt-4 border-t border-slate-800 text-xs">
                      {tier.features.map((feat, fIdx) => (
                        <div key={fIdx} className="flex items-start gap-2 text-slate-300">
                          <Check className="w-4 h-4 text-teal-400 flex-shrink-0 mt-0.5" />
                          <span>{feat}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <button
                    onClick={() => onSelectTab && onSelectTab(tier.featured ? 'searchChat' : 'chatExplorer')}
                    className={`w-full py-2.5 rounded-xl font-bold text-xs transition-all flex items-center justify-center gap-1.5 ${
                      tier.featured
                        ? 'bg-gradient-to-r from-cyan-500 to-teal-600 hover:from-cyan-400 hover:to-teal-500 text-slate-950 shadow-lg shadow-cyan-500/20'
                        : 'bg-[#070b14] hover:bg-slate-800 text-slate-200 border border-slate-700'
                    }`}
                  >
                    <span>{tier.featured ? 'Claim Founder\'s Pass & Test Demo' : 'Explore Feature Set'}</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </>
      )}

      {activeTab === 'drops' && (
        <div className="space-y-6">
          <div className="rounded-2xl bg-gradient-to-r from-cyan-950/40 via-[#0c1424] to-teal-950/30 border border-cyan-500/30 p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div>
              <span className="text-xs font-mono text-cyan-400">The 6-Week Feature Drop Engine</span>
              <h3 className="text-lg font-bold text-white">Why Modular Weekly Releases?</h3>
              <p className="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
                A staged rollout provides steady innovation, giving you a fresh reason to return each week. Buy only what you need a-la-carte ($9–$25 each), or lock in every drop for life with the <strong>$49 Founder's Season Pass</strong>.
              </p>
            </div>
            <div className="p-3 rounded-xl bg-[#070b14] border border-cyan-500/40 text-center min-w-[140px]">
              <div className="text-[11px] text-slate-400">Sum of Parts:</div>
              <div className="text-xl font-black text-white">{TOTALRECALLS_SPECS.sumOfPartsPrice}</div>
              <div className="text-[10px] text-teal-400 font-semibold">Pass: $49 (Save $91)</div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {ROADMAP_DROPS.map((drop) => (
              <div key={drop.week} className="p-5 rounded-2xl bg-[#0c1424] border border-slate-800 hover:border-cyan-500/40 transition-all flex flex-col justify-between space-y-4">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold font-mono bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                      WEEK {drop.week}
                    </span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                      drop.status === 'live' ? 'bg-teal-500/20 text-teal-300' :
                      drop.status === 'next_up' ? 'bg-cyan-500/20 text-cyan-300' : 'bg-slate-800 text-slate-400'
                    }`}>
                      {drop.status === 'live' ? '● LIVE TODAY' : drop.status === 'next_up' ? '⚡ UPCOMING' : 'PLANNED'}
                    </span>
                  </div>

                  <h4 className="text-base font-bold text-white">{drop.title}</h4>
                  <p className="text-xs text-cyan-400/90 font-medium">{drop.tagline}</p>
                  <p className="text-xs text-slate-300 leading-relaxed pt-1">{drop.description}</p>

                  <div className="space-y-1.5 pt-3 border-t border-slate-800 text-xs">
                    {drop.features.map((f, i) => (
                      <div key={i} className="flex items-start gap-1.5 text-slate-400">
                        <Check className="w-3.5 h-3.5 text-teal-400 flex-shrink-0 mt-0.5" />
                        <span>{f}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between">
                  <div>
                    <span className="text-[10px] text-slate-500 block">Standalone:</span>
                    <span className="text-base font-black text-white">{drop.standalonePrice}</span>
                  </div>
                  <span className="text-[11px] font-semibold text-teal-300 bg-teal-950/40 px-2 py-1 rounded border border-teal-500/30">
                    Included in $49 Pass
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Side-by-side Architectural Specs */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4">
        {/* Core Downloader Unit */}
        <div className="rounded-2xl bg-[#0c1424] border border-slate-800 p-6 space-y-4 shadow-lg">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-[#070b14] border border-slate-700 flex items-center justify-center">
              <HardDrive className="w-5 h-5 text-cyan-400" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">Unit 1: The Core Chat Downloader</h3>
              <p className="text-xs text-slate-400">TotalRecalls Baseline Foundation (totalrecalls.app)</p>
            </div>
          </div>

          <p className="text-xs text-slate-300 leading-relaxed">
            Automates the export of conversational histories across all major web LLM providers into a local, 
            zero-cloud disk vault. Prevents vendor lock-in and vendor data loss.
          </p>

          <div className="space-y-2 pt-2 border-t border-slate-800/80 text-xs">
            <div className="flex items-center gap-2 text-slate-300">
              <Check className="w-4 h-4 text-teal-400 flex-shrink-0" />
              <span>Multi-Provider Scrapers: ChatGPT, Claude, Gemini, Perplexity, Mistral</span>
            </div>
            <div className="flex items-center gap-2 text-slate-300">
              <Check className="w-4 h-4 text-teal-400 flex-shrink-0" />
              <span>Format Parsers: JSON, Markdown, Raw HTML, PDF exports</span>
            </div>
            <div className="flex items-center gap-2 text-slate-300">
              <Check className="w-4 h-4 text-teal-400 flex-shrink-0" />
              <span>AES-256 local encrypted filesystem vault</span>
            </div>
            <div className="flex items-center gap-2 text-slate-300">
              <Check className="w-4 h-4 text-teal-400 flex-shrink-0" />
              <span>Incremental background sync without re-downloading duplicates</span>
            </div>
          </div>
        </div>

        {/* Vector Search & RAG SQL Add-On */}
        <div className="rounded-2xl bg-gradient-to-br from-cyan-950/40 via-[#0c1424] to-[#0c1424] border border-cyan-500/40 p-6 space-y-4 shadow-xl">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-teal-500 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <Database className="w-5 h-5 text-slate-950 font-bold" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-lg font-bold text-white">Unit 2: Smart Search Engine Suite</h3>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-cyan-500 text-slate-950">MARKET LEADER</span>
              </div>
              <p className="text-xs text-cyan-300">High-Performance Semantic, Analytical & Auditing Layer</p>
            </div>
          </div>

          <p className="text-xs text-slate-300 leading-relaxed">
            Turns static chat archives into an active, verified intelligence hub. 
            Employs local HNSW vector indexing, natural language to SQLite compilation, peer-review consensus auditing, knowledge graph clustering, and automated PII scrubbing.
          </p>

          <div className="space-y-2 pt-2 border-t border-slate-800/80 text-xs">
            <div className="flex items-center gap-2 text-slate-200">
              <Check className="w-4 h-4 text-cyan-400 flex-shrink-0" />
              <span>Reciprocal Rank Fusion (RRF): Combines BM25 keyword matching with Cosine vectors</span>
            </div>
            <div className="flex items-center gap-2 text-slate-200">
              <Check className="w-4 h-4 text-cyan-400 flex-shrink-0" />
              <span>Embedding Engine Profiler & 2D PCA Cluster Map for local dimension benchmarking</span>
            </div>
            <div className="flex items-center gap-2 text-slate-200">
              <Check className="w-4 h-4 text-cyan-400 flex-shrink-0" />
              <span>Automated Knowledge Graph & Entity Topic Cards across all archived sessions</span>
            </div>
            <div className="flex items-center gap-2 text-slate-200">
              <Check className="w-4 h-4 text-cyan-400 flex-shrink-0" />
              <span>Cross-Provider Consensus & Hallucination Auditor with Persona Q&A Modes</span>
            </div>
          </div>
        </div>
      </div>

      {/* Embedding Model Support Matrix */}
      <div className="rounded-2xl bg-[#0c1424] border border-slate-800 p-6 space-y-4">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <Cpu className="w-4 h-4 text-cyan-400" />
          Supported Local & Cloud Embedding Engines
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {TOTALRECALLS_SPECS.embeddingModels.map((em) => (
            <div key={em.id} className="p-4 rounded-xl bg-[#070b14] border border-slate-800/80 space-y-2">
              <div className="text-xs font-semibold text-slate-200">{em.name}</div>
              <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
                <span>{em.dimension} Dimensions</span>
                <span className="text-cyan-400">{em.provider}</span>
              </div>
              <div className="flex items-center justify-between text-[11px] text-slate-500 font-mono pt-1 border-t border-slate-800">
                <span>Latency: {em.latencyPer1kTokensMs}ms</span>
                <span>RAM: {em.ramUsageMBPer100k} MB/100k</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
