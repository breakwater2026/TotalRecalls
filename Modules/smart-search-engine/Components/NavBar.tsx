import React, { useState } from 'react';
import { 
  Network, 
  Sparkles, 
  Tag, 
  Layers, 
  ExternalLink, 
  HardDrive, 
  Database, 
  TrendingUp, 
  Clock, 
  CheckCircle2,
  BookOpen,
  Filter
} from 'lucide-react';
import { INITIAL_KNOWLEDGE_CLUSTERS } from '../constants';
import { KnowledgeTopicCluster, ChatConversation } from '../types';

interface KnowledgeGraphProps {
  conversations: ChatConversation[];
  onOpenConversation?: (id: string) => void;
  onSelectConversation?: (id: string) => void;
}

export const KnowledgeGraph: React.FC<KnowledgeGraphProps> = ({
  conversations,
  onOpenConversation,
  onSelectConversation
}) => {
  const handleOpenConversation = (id: string) => {
    if (onOpenConversation) onOpenConversation(id);
    else if (onSelectConversation) onSelectConversation(id);
  };

  const [clusters] = useState<KnowledgeTopicCluster[]>(INITIAL_KNOWLEDGE_CLUSTERS);
  const [selectedClusterId, setSelectedClusterId] = useState<string>(INITIAL_KNOWLEDGE_CLUSTERS[0].id);
  const [activeCategory, setActiveCategory] = useState<string>('ALL');

  const activeCluster = clusters.find(c => c.id === selectedClusterId) || clusters[0];

  const filteredClusters = clusters.filter(c => 
    activeCategory === 'ALL' || c.category === activeCategory
  );

  const clusterConversations = conversations.filter(conv => 
    activeCluster.conversationIds.includes(conv.id)
  );

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#0c1f30] via-[#091524] to-[#070c16] border border-cyan-500/30 p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5 max-w-2xl">
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-teal-500/15 text-teal-300 border border-teal-500/40 flex items-center gap-1.5">
                <Network className="w-3.5 h-3.5 text-teal-400" />
                TotalRecalls Market-Leader Enhancement #5
              </span>
              <span className="text-xs text-slate-400 font-mono">Automated Vault Insights</span>
            </div>
            <h2 className="text-2xl font-bold text-white tracking-tight">
              Knowledge Graph & Vault Topic Discovery
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed">
              As TotalRecalls downloads hundreds of chat sessions across providers, this engine automatically structures, categorizes, and extracts underlying thematic cards and technical concept clusters.
            </p>
          </div>

          <div className="flex items-center gap-4 bg-[#080d19] border border-slate-800 rounded-xl p-3 px-4">
            <div>
              <div className="text-xs text-slate-400">Thematic Clusters</div>
              <div className="text-xl font-bold font-mono text-cyan-400">{clusters.length} Domains</div>
            </div>
            <div className="h-8 w-px bg-slate-800"></div>
            <div>
              <div className="text-xs text-slate-400">Total Tokens Mapped</div>
              <div className="text-sm font-semibold text-teal-400 font-mono">9,090 Tokens</div>
            </div>
          </div>
        </div>
      </div>

      {/* Category selector */}
      <div className="flex items-center justify-between bg-[#0c1424] border border-slate-800 rounded-xl p-3 text-xs">
        <div className="flex items-center gap-2">
          <span className="text-slate-400 font-semibold uppercase tracking-wider flex items-center gap-1">
            <Filter className="w-3.5 h-3.5 text-cyan-400" />
            Knowledge Domain:
          </span>
          <div className="flex gap-1">
            {['ALL', 'Data & Search', 'Infrastructure', 'Security & Commerce', 'Analytics'].map(cat => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`px-2.5 py-1 rounded-md font-semibold transition-colors ${
                  activeCategory === cat
                    ? 'bg-gradient-to-r from-cyan-600 to-teal-600 text-white shadow-sm'
                    : 'bg-[#070b14] text-slate-400 hover:text-slate-200'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
        <span className="text-slate-400 font-mono hidden sm:inline">
          Automatic Latent Topic Inference
        </span>
      </div>

      {/* Main 2-column layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-[560px]">
        {/* Left: Topic Cards */}
        <div className="lg:col-span-5 space-y-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center justify-between">
            <span>Thematic Clusters ({filteredClusters.length})</span>
            <span className="text-cyan-400 font-mono">Click to inspect</span>
          </div>

          <div className="space-y-3">
            {filteredClusters.map(cluster => {
              const isSelected = cluster.id === selectedClusterId;
              return (
                <div
                  key={cluster.id}
                  onClick={() => setSelectedClusterId(cluster.id)}
                  className={`p-4 rounded-xl cursor-pointer transition-all border ${
                    isSelected
                      ? 'bg-cyan-950/40 border-cyan-500/80 shadow-lg shadow-cyan-950/30'
                      : 'bg-[#0c1424] border-slate-800 hover:border-slate-700 hover:bg-[#0e172a]'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#070b14] text-cyan-300 border border-slate-800">
                      {cluster.category}
                    </span>
                    <span className="text-[11px] font-mono text-teal-400 font-semibold">
                      {cluster.confidenceScore}% Coherence
                    </span>
                  </div>

                  <h4 className="text-sm font-bold text-white mb-1">
                    {cluster.name}
                  </h4>

                  <p className="text-xs text-slate-300 line-clamp-2 mb-3">
                    {cluster.summary}
                  </p>

                  <div className="flex flex-wrap gap-1 mb-2">
                    {cluster.topKeywords.slice(0, 3).map((kw, i) => (
                      <span key={i} className="px-1.5 py-0.5 rounded bg-[#070b14] text-[10px] text-slate-400 font-mono">
                        #{kw}
                      </span>
                    ))}
                  </div>

                  <div className="flex items-center justify-between text-[11px] text-slate-500 pt-2 border-t border-slate-800/80">
                    <span>{cluster.conversationIds.length} Linked Chats • {cluster.turnCount} turns</span>
                    <span className="font-mono text-cyan-400">{cluster.totalTokens.toLocaleString()} tokens</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right: Topic Inspector & Linked Conversations */}
        <div className="lg:col-span-7 bg-[#0c1424] border border-slate-800 rounded-2xl p-6 space-y-6 flex flex-col justify-between shadow-xl">
          <div className="space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <span className="text-xs font-mono text-cyan-400 uppercase tracking-wider">
                  {activeCluster.category} • {activeCluster.id}
                </span>
                <h3 className="text-xl font-bold text-white mt-1">
                  {activeCluster.name}
                </h3>
              </div>
              <div className="text-right font-mono text-xs text-slate-400">
                <div>Updated: {activeCluster.lastUpdated}</div>
                <div className="text-teal-400 font-bold">{activeCluster.confidenceScore}% Confidence</div>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-[#070b14] border border-slate-800 space-y-2 text-xs">
              <span className="font-semibold text-slate-300 uppercase tracking-wider text-[11px]">
                Synthesized Executive Summary:
              </span>
              <p className="text-slate-300 leading-relaxed">
                {activeCluster.summary}
              </p>
            </div>

            {/* Keyword Entity Badges */}
            <div className="space-y-1.5">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Extracted Concept Keywords:
              </span>
              <div className="flex flex-wrap gap-1.5">
                {activeCluster.topKeywords.map((kw, i) => (
                  <span
                    key={i}
                    className="px-2.5 py-1 rounded-lg bg-cyan-950/40 border border-cyan-800/40 text-cyan-300 font-mono text-xs"
                  >
                    #{kw}
                  </span>
                ))}
              </div>
            </div>

            {/* Linked Conversations */}
            <div className="space-y-3 pt-2">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <BookOpen className="w-3.5 h-3.5 text-teal-400" />
                Linked Chat Sessions ({clusterConversations.length})
              </span>

              <div className="space-y-2">
                {clusterConversations.map(conv => (
                  <div
                    key={conv.id}
                    className="p-3.5 rounded-xl bg-[#070b14] border border-slate-800 flex items-center justify-between hover:border-cyan-500/50 transition-colors"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-[#0c1424] text-cyan-300 border border-slate-700">
                          {conv.provider}
                        </span>
                        <h5 className="text-xs font-bold text-slate-200 hover:text-cyan-300 cursor-pointer"
                          onClick={() => handleOpenConversation(conv.id)}
                        >
                          {conv.title}
                        </h5>
                      </div>
                      <div className="text-[11px] text-slate-400 font-mono">
                        {conv.messageCount} turns • {conv.totalTokens.toLocaleString()} tokens • {conv.createdAt.slice(0, 10)}
                      </div>
                    </div>

                    <button
                      onClick={() => handleOpenConversation(conv.id)}
                      className="px-3 py-1.5 bg-[#0c1424] hover:bg-cyan-950/50 text-cyan-400 rounded-lg text-xs font-medium flex items-center gap-1 transition-colors"
                    >
                      <span>Open Turn</span>
                      <ExternalLink className="w-3 h-3" />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="p-3 rounded-xl bg-teal-950/30 border border-teal-500/30 text-xs text-teal-300 flex items-center justify-between">
            <span>Knowledge Graph automatically updates upon new TotalRecalls sync runs.</span>
            <span className="font-mono text-cyan-400">Zero Cloud Egress</span>
          </div>
        </div>
      </div>
    </div>
  );
};
