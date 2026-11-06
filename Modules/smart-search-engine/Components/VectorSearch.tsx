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
    ChatGPT: 'bg-[var(--tr-good)]/10 text-[var(--tr-good)] border-[var(--tr-good)]/30',
    Claude: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
    Gemini: 'bg-[var(--tr-accent)]/10 text-[var(--tr-accent)] border-[var(--tr-accent)]/30',
    Perplexity: 'bg-[var(--tr-accent)]/10 text-[var(--tr-accent)] border-[var(--tr-accent)]/30',
    Mistral: 'bg-orange-500/10 text-orange-400 border-orange-500/30',
    Grok: 'bg-[var(--tr-accent)]/10 text-[var(--tr-accent)] border-[var(--tr-accent)]/30',
    DeepSeek: 'bg-[var(--tr-accent)]/10 text-[var(--tr-accent)] border-[var(--tr-accent)]/30',
    Qwen: 'bg-[var(--tr-accent)]/10 text-[var(--tr-accent)] border-[var(--tr-accent)]/30',
   };

  return (
    <div className="space-y-6">
      {/* Top Banner with TotalRecalls brand accent */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[var(--tr-bg)] via-[var(--tr-panel2)] to-[var(--tr-bg)] border border-[var(--tr-accent)]/30 p-6 shadow-xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5 max-w-2xl">
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[var(--tr-accent)]/20 text-[var(--tr-accent)] border border-[var(--tr-accent)]/40 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
                TotalRecalls Add-on: Semantic Vector & RRF Engine
              </span>
              <span className="text-xs text-[var(--tr-muted)] font-mono">Runs on your PC — nothing uploaded</span>
            </div>
            <h2 className="text-2xl font-bold text-[var(--tr-text)] tracking-tight">
              Cross-Provider Semantic Vector Search & Hybrid RRF
            </h2>
            <p className="text-sm text-[var(--tr-muted)] leading-relaxed">
              Find ideas, code snippets, and design decisions across all your downloaded conversations 
              from ChatGPT, Claude, Gemini, Perplexity, and Mistral using Reciprocal Rank Fusion (BM25 + Cosine).
            </p>
          </div>
          
          <div className="flex items-center gap-4 bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-xl p-3 px-4">
            <div>
              <div className="text-xs text-[var(--tr-muted)]">Embedded Chunks</div>
              <div className="text-xl font-bold font-mono text-[var(--tr-accent)]">{chunks.length} Vectors</div>
            </div>
            <div className="h-8 w-px bg-[var(--tr-panel)]"></div>
            <div>
              <div className="text-xs text-[var(--tr-muted)]">Search Fusion</div>
              <div className="text-sm font-semibold text-[var(--tr-accent)] flex items-center gap-1">
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
          <div className="absolute left-4 pointer-events-none text-[var(--tr-accent)]">
            <Search className="w-5 h-5" />
          </div>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search your conversations conceptually (e.g. 'how did we resolve webhook signature verification?')"
            className="w-full pl-12 pr-32 py-3.5 bg-[var(--tr-panel)] border border-[var(--tr-border)] focus:border-[var(--tr-accent)] rounded-xl text-[var(--tr-text)] placeholder-[var(--tr-muted)] focus:outline-none focus:ring-2 focus:ring-[var(--tr-accent)]/30 transition-all shadow-inner"
          />
          <button
            type="submit"
            disabled={isSearching}
            className="absolute right-2 px-5 py-2 bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] hover:from-[var(--tr-accent)] hover:to-[var(--tr-accent2)] text-[var(--tr-text)] rounded-lg font-semibold text-sm transition-all flex items-center gap-2 shadow-md shadow"
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
          <span className="text-[var(--tr-muted)] flex items-center gap-1">
            <SlidersHorizontal className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
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
              className="px-2.5 py-1 rounded-md bg-[var(--tr-panel)] hover:bg-[var(--tr-accent)]/60 text-[var(--tr-muted)] hover:text-[var(--tr-accent)] border border-[var(--tr-border)] hover:border-[var(--tr-accent)]/40 transition-colors"
            >
              "{query}"
            </button>
          ))}
        </div>
      </form>

      {/* Filter controls with RRF Toggle */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-xl bg-[var(--tr-panel)] border border-[var(--tr-border)] text-sm">
        <div className="flex items-center space-x-2">
          <span className="text-[var(--tr-muted)] text-xs font-semibold uppercase tracking-wider">Provider:</span>
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
                    ? 'bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] text-[var(--tr-text)] shadow-sm'
                    : 'bg-[var(--tr-panel)] text-[var(--tr-muted)] hover:text-[var(--tr-text)]'
                }`}
              >
                {p}
              </button>
            ))}
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-4">
          {/* RRF Hybrid Toggle (Enhancement #4) */}
          <label className="flex items-center gap-2 cursor-pointer text-xs text-[var(--tr-muted)] bg-[var(--tr-panel)] px-2.5 py-1 rounded border border-[var(--tr-border)]">
            <input
              type="checkbox"
              checked={useRRF}
              onChange={(e) => {
                const val = e.target.checked;
                setUseRRF(val);
                setSearchResults(searchVectorIndex(searchQuery, chunks, topK, similarityThreshold, providerFilter, val));
              }}
              className=" cursor-pointer"
            />
            <span className="font-semibold text-[var(--tr-accent)]">Reciprocal Rank Fusion (RRF)</span>
          </label>

          <div className="flex items-center space-x-2 text-xs">
            <span className="text-[var(--tr-muted)]">Min Score:</span>
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
              className="w-20  cursor-pointer"
            />
            <span className="font-mono text-[var(--tr-accent)]">{Math.round(similarityThreshold * 100)}%</span>
          </div>

          <div className="flex items-center space-x-2 text-xs">
            <span className="text-[var(--tr-muted)]">Top K:</span>
            <select
              value={topK}
              onChange={(e) => {
                const val = parseInt(e.target.value);
                setTopK(val);
                setSearchResults(searchVectorIndex(searchQuery, chunks, val, similarityThreshold, providerFilter, useRRF));
              }}
              className="bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded px-2 py-1 text-[var(--tr-text)] text-xs"
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
          <h3 className="text-sm font-semibold uppercase tracking-wider text-[var(--tr-muted)] flex items-center gap-2">
            <Layers className="w-4 h-4 text-[var(--tr-accent)]" />
            Ranked Semantic Results ({searchResults.length} matches)
          </h3>
          <span className="text-xs text-[var(--tr-muted)] font-mono">
            {useRRF ? 'Weighted: 60% Cosine + 40% BM25 keyword' : 'Cosine Distance Metric Only'}
          </span>
        </div>

        {searchResults.length === 0 ? (
          <div className="p-12 text-center rounded-xl bg-[var(--tr-panel)] border border-dashed border-[var(--tr-border)]">
            <Search className="w-8 h-8 text-[var(--tr-muted)] mx-auto mb-3" />
            <h4 className="text-base font-medium text-[var(--tr-muted)]">No semantic matches found</h4>
            <p className="text-sm text-[var(--tr-muted)] mt-1">
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
                  className="group relative rounded-xl bg-[var(--tr-panel)] border border-[var(--tr-border)] hover:border-[var(--tr-accent)]/50 p-5 transition-all hover:shadow-lg hover:shadow"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className={`px-2 py-0.5 rounded text-xs font-semibold border ${providerColors[result.provider]}`}>
                        {result.provider}
                      </span>
                      <span className="text-sm font-semibold text-[var(--tr-text)] hover:text-[var(--tr-accent)] transition-colors cursor-pointer"
                        onClick={() => onOpenConversation && onOpenConversation(result.conversationId)}
                      >
                        {result.conversationTitle}
                      </span>
                      <span className="text-xs text-[var(--tr-muted)] flex items-center gap-1 font-mono">
                        <Clock className="w-3 h-3" />
                        {result.timestamp}
                      </span>
                    </div>

                    {/* Similarity score bar with RRF details */}
                    <div className="flex items-center gap-2 self-start sm:self-auto bg-[var(--tr-panel2)] px-2.5 py-1 rounded-lg border border-[var(--tr-border)]">
                      <div className="text-[11px] text-[var(--tr-muted)]">Match:</div>
                      <div className="w-16 h-2 bg-[var(--tr-panel)] rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] rounded-full"
                          style={{ width: `${scorePercent}%` }}
                        ></div>
                      </div>
                      <div className="text-xs font-mono font-bold text-[var(--tr-accent)]">
                        {scorePercent}%
                      </div>
                      {useRRF && result.bm25Score !== undefined && (
                        <div className="text-[10px] text-[var(--tr-accent)] font-mono hidden md:inline">
                          (BM25: {Math.round(result.bm25Score * 100)}%)
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="text-sm text-[var(--tr-muted)] leading-relaxed font-sans bg-[var(--tr-panel)] p-3.5 rounded-lg border border-[var(--tr-border)] whitespace-pre-wrap">
                    {result.content}
                  </div>

                  <div className="mt-3 flex items-center justify-between text-xs text-[var(--tr-muted)]">
                    <span className="flex items-center gap-1.5 font-mono">
                      <Cpu className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
                      Chunk ID: {result.id} • Role: {result.role}
                    </span>
                    <button
                      onClick={() => onOpenConversation && onOpenConversation(result.conversationId)}
                      className="text-[var(--tr-accent)] hover:text-[var(--tr-accent)] font-medium flex items-center gap-1 group-hover:translate-x-0.5 transition-transform"
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
