import React, { useState } from 'react';
import { 
  Search, 
  Sparkles, 
  SlidersHorizontal, 
  Tag, 
  ExternalLink, 
  Cpu, 
  Zap, 
  Layers, 
  MessageSquare,
  ShieldCheck,
  CheckCircle2,
  Clock,
  Filter
} from 'lucide-react';
import { ChunkEmbedding, AIProvider } from '../types';
import { searchVectorIndex } from '../services/ragEngine';

interface VectorSearchProps {
  chunks: ChunkEmbedding[];
  onOpenConversation?: (conversationId: string) => void;
  conversations?: ChatConversation[];
}

export const VectorSearch: React.FC<VectorSearchProps> = ({ chunks, onOpenConversation }) => {
  const [searchQuery, setSearchQuery] = useState('How to configure postgres vector indexes or sqlite local rag?');
  const [providerFilter, setProviderFilter] = useState<string>('ALL');
  const [similarityThreshold, setSimilarityThreshold] = useState<number>(0.15);
  const [topK, setTopK] = useState<number>(6);
  const [useRRF, setUseRRF] = useState<boolean>(true);
  const [isSearching, setIsSearching] = useState<boolean>(false);
  const [searchResults, setSearchResults] = useState<ChunkEmbedding[]>(() => 
    searchVectorIndex('postgres vector indexes sqlite local rag', chunks, 6, 0.15, 'ALL', true)
  );

  const handleSearch = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!searchQuery.trim()) return;

    setIsSearching(true);
    setTimeout(() => {
      const results = searchVectorIndex(
        searchQuery,
        chunks,
        topK,
        similarityThreshold,
        providerFilter,
        useRRF
      );
      setSearchResults(results);
      setIsSearching(false);
    }, 180);
  };

  const sampleQueries = [
    'Postgres pgvector schema and HNSW indexes',
    'Stripe refund policy and webhook verification',
    'Docker Ollama with GPU acceleration for local LLMs',
    'Microservices vs local embedded SQLite decision',
    'Conversion rate and quarterly chat exports'
  ];

  const providerColors: Record<AIProvider, string> = {
    ChatGPT: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    Claude: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
    Gemini: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30',
    Perplexity: 'bg-teal-500/10 text-teal-400 border-teal-500/30',
    Mistral: 'bg-orange-500/10 text-orange-400 border-orange-500/30',
    LocalLlama: 'bg-sky-500/10 text-sky-400 border-sky-500/30'
  };

  return (
    <div className="space-y-6">
      {/* Top Banner with TotalRecalls cyan/teal theme */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#0c1f30] via-[#0b1626] to-[#070c16] border border-cyan-500/30 p-6 shadow-xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5 max-w-2xl">
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
                TotalRecalls Add-on: Semantic Vector & RRF Engine
              </span>
              <span className="text-xs text-slate-400 font-mono">100% Local / Zero Cloud Latency</span>
            </div>
            <h2 className="text-2xl font-bold text-white tracking-tight">
              Cross-Provider Semantic Vector Search & Hybrid RRF
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed">
              Find ideas, code snippets, and design decisions across all your downloaded conversations 
              from ChatGPT, Claude, Gemini, Perplexity, and Mistral using Reciprocal Rank Fusion (BM25 + Cosine).
            </p>
          </div>
          
          <div className="flex items-center gap-4 bg-[#080d19] border border-slate-800 rounded-xl p-3 px-4">
            <div>
              <div className="text-xs text-slate-400">Embedded Chunks</div>
              <div className="text-xl font-bold font-mono text-cyan-400">{chunks.length} Vectors</div>
            </div>
            <div className="h-8 w-px bg-slate-800"></div>
            <div>
              <div className="text-xs text-slate-400">Search Fusion</div>
              <div className="text-sm font-semibold text-teal-400 flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                {useRRF ? 'RRF Hybrid' : 'Cosine Only'}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Search Input Bar */}
      <form onSubmit={handleSearch} className="relative">
        <div className="relative flex items-center">
          <div className="absolute left-4 pointer-events-none text-cyan-400">
            <Search className="w-5 h-5" />
          </div>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search your conversations conceptually (e.g. 'how did we resolve webhook signature verification?')"
            className="w-full pl-12 pr-32 py-3.5 bg-[#0c1424] border border-slate-800 focus:border-cyan-500 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/30 transition-all shadow-inner"
          />
          <button
            type="submit"
            disabled={isSearching}
            className="absolute right-2 px-5 py-2 bg-gradient-to-r from-cyan-600 to-teal-600 hover:from-cyan-500 hover:to-teal-500 text-white rounded-lg font-semibold text-sm transition-all flex items-center gap-2 shadow-md shadow-cyan-600/30"
          >
            {isSearching ? (
              <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
            ) : (
              <Zap className="w-4 h-4" />
            )}
            <span>Vector Match</span>
          </button>
        </div>

        {/* Quick query pills */}
        <div className="flex flex-wrap items-center gap-2 mt-3 text-xs">
          <span className="text-slate-400 flex items-center gap-1">
            <SlidersHorizontal className="w-3.5 h-3.5 text-cyan-400" />
            Try conceptual prompts:
          </span>
          {sampleQueries.map((query, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => {
                setSearchQuery(query);
                const results = searchVectorIndex(query, chunks, topK, similarityThreshold, providerFilter, useRRF);
                setSearchResults(results);
              }}
              className="px-2.5 py-1 rounded-md bg-[#0c1424] hover:bg-cyan-950/60 text-slate-300 hover:text-cyan-300 border border-slate-800 hover:border-cyan-500/40 transition-colors"
            >
              "{query}"
            </button>
          ))}
        </div>
      </form>

      {/* Filter controls with RRF Toggle */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-xl bg-[#0c1424] border border-slate-800 text-sm">
        <div className="flex items-center space-x-2">
          <span className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Provider:</span>
          <div className="flex flex-wrap gap-1">
            {['ALL', 'ChatGPT', 'Claude', 'Gemini', 'Perplexity', 'Mistral'].map((p) => (
              <button
                key={p}
                onClick={() => {
                  setProviderFilter(p);
                  const results = searchVectorIndex(searchQuery, chunks, topK, similarityThreshold, p, useRRF);
                  setSearchResults(results);
                }}
                className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-all ${
                  providerFilter === p
                    ? 'bg-gradient-to-r from-cyan-600 to-teal-600 text-white shadow-sm'
                    : 'bg-[#080d19] text-slate-400 hover:text-slate-200'
                }`}
              >
                {p}
              </button>
            ))}
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-4">
          {/* RRF Hybrid Toggle (Enhancement #4) */}
          <label className="flex items-center gap-2 cursor-pointer text-xs text-slate-300 bg-[#080d19] px-2.5 py-1 rounded border border-slate-800">
            <input
              type="checkbox"
              checked={useRRF}
              onChange={(e) => {
                const val = e.target.checked;
                setUseRRF(val);
                setSearchResults(searchVectorIndex(searchQuery, chunks, topK, similarityThreshold, providerFilter, val));
              }}
              className="accent-cyan-500 cursor-pointer"
            />
            <span className="font-semibold text-teal-400">Reciprocal Rank Fusion (RRF)</span>
          </label>

          <div className="flex items-center space-x-2 text-xs">
            <span className="text-slate-400">Min Score:</span>
            <input
              type="range"
              min="0.05"
              max="0.80"
              step="0.05"
              value={similarityThreshold}
              onChange={(e) => {
                const val = parseFloat(e.target.value);
                setSimilarityThreshold(val);
                setSearchResults(searchVectorIndex(searchQuery, chunks, topK, val, providerFilter, useRRF));
              }}
              className="w-20 accent-cyan-500 cursor-pointer"
            />
            <span className="font-mono text-cyan-400">{Math.round(similarityThreshold * 100)}%</span>
          </div>

          <div className="flex items-center space-x-2 text-xs">
            <span className="text-slate-400">Top K:</span>
            <select
              value={topK}
              onChange={(e) => {
                const val = parseInt(e.target.value);
                setTopK(val);
                setSearchResults(searchVectorIndex(searchQuery, chunks, val, similarityThreshold, providerFilter, useRRF));
              }}
              className="bg-[#080d19] border border-slate-700 rounded px-2 py-1 text-slate-200 text-xs"
            >
              <option value="3">3</option>
              <option value="5">5</option>
              <option value="8">8</option>
              <option value="12">12</option>
            </select>
          </div>
        </div>
      </div>

      {/* Results Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
            <Layers className="w-4 h-4 text-cyan-400" />
            Ranked Semantic Results ({searchResults.length} matches)
          </h3>
          <span className="text-xs text-slate-500 font-mono">
            {useRRF ? 'Weighted: 60% Cosine + 40% BM25 keyword' : 'Cosine Distance Metric Only'}
          </span>
        </div>

        {searchResults.length === 0 ? (
          <div className="p-12 text-center rounded-xl bg-[#0c1424] border border-dashed border-slate-800">
            <Search className="w-8 h-8 text-slate-600 mx-auto mb-3" />
            <h4 className="text-base font-medium text-slate-300">No semantic matches found</h4>
            <p className="text-sm text-slate-500 mt-1">
              Try lowering the minimum similarity threshold or using broader semantic search terms.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {searchResults.map((result) => {
              const scorePercent = Math.round(((useRRF ? result.rrfScore : result.similarityScore) ?? 0) * 100);
              return (
                <div
                  key={result.id}
                  className="group relative rounded-xl bg-[#0c1424] border border-slate-800 hover:border-cyan-500/50 p-5 transition-all hover:shadow-lg hover:shadow-cyan-500/5"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className={`px-2 py-0.5 rounded text-xs font-semibold border ${providerColors[result.provider]}`}>
                        {result.provider}
                      </span>
                      <span className="text-sm font-semibold text-slate-100 hover:text-cyan-300 transition-colors cursor-pointer"
                        onClick={() => onOpenConversation && onOpenConversation(result.conversationId)}
                      >
                        {result.conversationTitle}
                      </span>
                      <span className="text-xs text-slate-500 flex items-center gap-1 font-mono">
                        <Clock className="w-3 h-3" />
                        {result.timestamp}
                      </span>
                    </div>

                    {/* Similarity score bar with RRF details */}
                    <div className="flex items-center gap-2 self-start sm:self-auto bg-[#070b14] px-2.5 py-1 rounded-lg border border-slate-800">
                      <div className="text-[11px] text-slate-400">Match:</div>
                      <div className="w-16 h-2 bg-slate-800 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-cyan-500 to-teal-400 rounded-full"
                          style={{ width: `${scorePercent}%` }}
                        ></div>
                      </div>
                      <div className="text-xs font-mono font-bold text-cyan-400">
                        {scorePercent}%
                      </div>
                      {useRRF && result.bm25Score !== undefined && (
                        <div className="text-[10px] text-teal-400 font-mono hidden md:inline">
                          (BM25: {Math.round(result.bm25Score * 100)}%)
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="text-sm text-slate-300 leading-relaxed font-sans bg-[#080d19] p-3.5 rounded-lg border border-slate-800/80 whitespace-pre-wrap">
                    {result.content}
                  </div>

                  <div className="mt-3 flex items-center justify-between text-xs text-slate-500">
                    <span className="flex items-center gap-1.5 font-mono">
                      <Cpu className="w-3.5 h-3.5 text-cyan-400" />
                      Chunk ID: {result.id} • Role: {result.role}
                    </span>
                    <button
                      onClick={() => onOpenConversation && onOpenConversation(result.conversationId)}
                      className="text-cyan-400 hover:text-cyan-300 font-medium flex items-center gap-1 group-hover:translate-x-0.5 transition-transform"
                    >
                      <span>Jump to full conversation</span>
                      <ExternalLink className="w-3 h-3" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
