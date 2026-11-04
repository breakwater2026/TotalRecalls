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
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[var(--tr-bg)] via-[var(--tr-panel2)] to-[var(--tr-bg)] border border-[var(--tr-accent)]/30 p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5 max-w-2xl">
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[var(--tr-accent)]/15 text-[var(--tr-accent)] border border-[var(--tr-accent)]/40 flex items-center gap-1.5">
                <Network className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
                TotalRecalls Market-Leader Enhancement #5
              </span>
              <span className="text-xs text-[var(--tr-muted)] font-mono">Automated Vault Insights</span>
            </div>
            <h2 className="text-2xl font-bold text-[var(--tr-text)] tracking-tight">
              Knowledge Graph & Vault Topic Discovery
            </h2>
            <p className="text-sm text-[var(--tr-muted)] leading-relaxed">
              As TotalRecalls downloads hundreds of chat sessions across providers, this engine automatically structures, categorizes, and extracts underlying thematic cards and technical concept clusters.
            </p>
          </div>

          <div className="flex items-center gap-4 bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-xl p-3 px-4">
            <div>
              <div className="text-xs text-[var(--tr-muted)]">Thematic Clusters</div>
              <div className="text-xl font-bold font-mono text-[var(--tr-accent)]">{clusters.length} Domains</div>
            </div>
            <div className="h-8 w-px bg-[var(--tr-panel)]"></div>
            <div>
              <div className="text-xs text-[var(--tr-muted)]">Total Tokens Mapped</div>
              <div className="text-sm font-semibold text-[var(--tr-accent)] font-mono">9,090 Tokens</div>
            </div>
          </div>
        </div>
      </div>

      {/* Category selector */}
      <div className="flex items-center justify-between bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-xl p-3 text-xs">
        <div className="flex items-center gap-2">
          <span className="text-[var(--tr-muted)] font-semibold uppercase tracking-wider flex items-center gap-1">
            <Filter className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
            Knowledge Domain:
          </span>
          <div className="flex gap-1">
            {['ALL', 'Data & Search', 'Infrastructure', 'Security & Commerce', 'Analytics'].map(cat => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`px-2.5 py-1 rounded-md font-semibold transition-colors ${
                  activeCategory === cat
                    ? 'bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] text-[var(--tr-text)] shadow-sm'
                    : 'bg-[var(--tr-panel2)] text-[var(--tr-muted)] hover:text-[var(--tr-text)]'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
        <span className="text-[var(--tr-muted)] font-mono hidden sm:inline">
          Automatic Latent Topic Inference
        </span>
      </div>

      {/* Main 2-column layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-[560px]">
        {/* Left: Topic Cards */}
        <div className="lg:col-span-5 space-y-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-[var(--tr-muted)] flex items-center justify-between">
            <span>Thematic Clusters ({filteredClusters.length})</span>
            <span className="text-[var(--tr-accent)] font-mono">Click to inspect</span>
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
                      ? 'bg-[var(--tr-accent)]/40 border-[var(--tr-accent)]/80 shadow-lg shadow'
                      : 'bg-[var(--tr-panel)] border-[var(--tr-border)] hover:border-[var(--tr-border)] hover:bg-[var(--tr-panel2)]'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[var(--tr-panel2)] text-[var(--tr-accent)] border border-[var(--tr-border)]">
                      {cluster.category}
                    </span>
                    <span className="text-[11px] font-mono text-[var(--tr-accent)] font-semibold">
                      {cluster.confidenceScore}% Coherence
                    </span>
                  </div>

                  <h4 className="text-sm font-bold text-[var(--tr-text)] mb-1">
                    {cluster.name}
                  </h4>

                  <p className="text-xs text-[var(--tr-muted)] line-clamp-2 mb-3">
                    {cluster.summary}
                  </p>

                  <div className="flex flex-wrap gap-1 mb-2">
                    {cluster.topKeywords.slice(0, 3).map((kw, i) => (
                      <span key={i} className="px-1.5 py-0.5 rounded bg-[var(--tr-panel2)] text-[10px] text-[var(--tr-muted)] font-mono">
                        #{kw}
                      </span>
                    ))}
                  </div>

                  <div className="flex items-center justify-between text-[11px] text-[var(--tr-muted)] pt-2 border-t border-[var(--tr-border)]">
                    <span>{cluster.conversationIds.length} Linked Chats • {cluster.turnCount} turns</span>
                    <span className="font-mono text-[var(--tr-accent)]">{cluster.totalTokens.toLocaleString()} tokens</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right: Topic Inspector & Linked Conversations */}
        <div className="lg:col-span-7 bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-2xl p-6 space-y-6 flex flex-col justify-between shadow-xl">
          <div className="space-y-4">
            <div className="flex items-center justify-between border-b border-[var(--tr-border)] pb-3">
              <div>
                <span className="text-xs font-mono text-[var(--tr-accent)] uppercase tracking-wider">
                  {activeCluster.category} • {activeCluster.id}
                </span>
                <h3 className="text-xl font-bold text-[var(--tr-text)] mt-1">
                  {activeCluster.name}
                </h3>
              </div>
              <div className="text-right font-mono text-xs text-[var(--tr-muted)]">
                <div>Updated: {activeCluster.lastUpdated}</div>
                <div className="text-[var(--tr-accent)] font-bold">{activeCluster.confidenceScore}% Confidence</div>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-[var(--tr-panel2)] border border-[var(--tr-border)] space-y-2 text-xs">
              <span className="font-semibold text-[var(--tr-muted)] uppercase tracking-wider text-[11px]">
                Synthesized Executive Summary:
              </span>
              <p className="text-[var(--tr-muted)] leading-relaxed">
                {activeCluster.summary}
              </p>
            </div>

            {/* Keyword Entity Badges */}
            <div className="space-y-1.5">
              <span className="text-xs font-semibold text-[var(--tr-muted)] uppercase tracking-wider">
                Extracted Concept Keywords:
              </span>
              <div className="flex flex-wrap gap-1.5">
                {activeCluster.topKeywords.map((kw, i) => (
                  <span
                    key={i}
                    className="px-2.5 py-1 rounded-lg bg-[var(--tr-accent)]/40 border border-[var(--tr-accent)]/40 text-[var(--tr-accent)] font-mono text-xs"
                  >
                    #{kw}
                  </span>
                ))}
              </div>
            </div>

            {/* Linked Conversations */}
            <div className="space-y-3 pt-2">
              <span className="text-xs font-semibold text-[var(--tr-muted)] uppercase tracking-wider flex items-center gap-1.5">
                <BookOpen className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
                Linked Chat Sessions ({clusterConversations.length})
              </span>

              <div className="space-y-2">
                {clusterConversations.map(conv => (
                  <div
                    key={conv.id}
                    className="p-3.5 rounded-xl bg-[var(--tr-panel2)] border border-[var(--tr-border)] flex items-center justify-between hover:border-[var(--tr-accent)]/50 transition-colors"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-[var(--tr-panel)] text-[var(--tr-accent)] border border-[var(--tr-border)]">
                          {conv.provider}
                        </span>
                        <h5 className="text-xs font-bold text-[var(--tr-text)] hover:text-[var(--tr-accent)] cursor-pointer"
                          onClick={() => handleOpenConversation(conv.id)}
                        >
                          {conv.title}
                        </h5>
                      </div>
                      <div className="text-[11px] text-[var(--tr-muted)] font-mono">
                        {conv.messageCount} turns • {conv.totalTokens.toLocaleString()} tokens • {conv.createdAt.slice(0, 10)}
                      </div>
                    </div>

                    <button
                      onClick={() => handleOpenConversation(conv.id)}
                      className="px-3 py-1.5 bg-[var(--tr-panel)] hover:bg-[var(--tr-accent)]/50 text-[var(--tr-accent)] rounded-lg text-xs font-medium flex items-center gap-1 transition-colors"
                    >
                      <span>Open Turn</span>
                      <ExternalLink className="w-3 h-3" />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="p-3 rounded-xl bg-[var(--tr-accent)]/30 border border-[var(--tr-accent)]/30 text-xs text-[var(--tr-accent)] flex items-center justify-between">
            <span>Knowledge Graph automatically updates upon new TotalRecalls sync runs.</span>
            <span className="font-mono text-[var(--tr-accent)]">Zero Cloud Egress</span>
          </div>
        </div>
      </div>
    </div>
  );
};
