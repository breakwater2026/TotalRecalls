import React, { useState } from 'react';
import { 
  GitCompare, 
  Sparkles, 
  CheckCircle2, 
  AlertTriangle, 
  Compass, 
  ExternalLink, 
  ShieldCheck, 
  Layers, 
  SlidersHorizontal,
  Bot,
  Brain,
  MessageSquare
} from 'lucide-react';
import { ConsensusTopic, ChatConversation, AIProvider } from '../types';
import { INITIAL_CONSENSUS_TOPICS } from '../constants';

interface ConsensusAuditorProps {
  conversations?: ChatConversation[];
  onOpenConversation?: (id: string) => void;
  onSelectConversation?: (id: string) => void;
}

export const ConsensusAuditor: React.FC<ConsensusAuditorProps> = ({
  conversations = [],
  onOpenConversation,
  onSelectConversation
}) => {
  const handleOpenConversation = (id: string) => {
    if (onOpenConversation) onOpenConversation(id);
    else if (onSelectConversation) onSelectConversation(id);
  };

  const [topics, setTopics] = useState<ConsensusTopic[]>(INITIAL_CONSENSUS_TOPICS);
  const [selectedTopicId, setSelectedTopicId] = useState<string>(INITIAL_CONSENSUS_TOPICS[0].id);
  const [activeCategoryFilter, setActiveCategoryFilter] = useState<string>('ALL');

  const activeTopic = topics.find(t => t.id === selectedTopicId) || topics[0];

  const filteredTopics = topics.filter(t => 
    activeCategoryFilter === 'ALL' || t.category === activeCategoryFilter
  );

  const providerColors: Record<AIProvider, string> = {
    ChatGPT: 'bg-[var(--tr-good)]/10 text-[var(--tr-good)] border-[var(--tr-good)]/30',
    Claude: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
    Gemini: 'bg-[var(--tr-accent)]/10 text-[var(--tr-accent)] border-[var(--tr-accent)]/30',
    Perplexity: 'bg-[var(--tr-accent)]/10 text-[var(--tr-accent)] border-[var(--tr-accent)]/30',
    Mistral: 'bg-orange-500/10 text-orange-400 border-orange-500/30',
    LocalLlama: 'bg-sky-500/10 text-sky-400 border-sky-500/30'
  };

  const getConsensusBadge = (level: ConsensusTopic['consensusLevel']) => {
    switch (level) {
      case 'High':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-[var(--tr-accent)]/15 text-[var(--tr-accent)] border border-[var(--tr-accent)]/40 flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" />
            High Consensus
          </span>
        );
      case 'Divergent':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/15 text-rose-300 border border-rose-500/40 flex items-center gap-1">
            <AlertTriangle className="w-3 h-3" />
            Divergent Stance
          </span>
        );
      case 'Complementary':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-[var(--tr-accent)]/15 text-[var(--tr-accent)] border border-[var(--tr-accent)]/40 flex items-center gap-1">
            <Sparkles className="w-3 h-3" />
            Complementary
          </span>
        );
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner with TotalRecalls brand accent */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[var(--tr-bg)] via-[var(--tr-panel2)] to-[var(--tr-bg)] border border-[var(--tr-accent)]/30 p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5 max-w-2xl">
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[var(--tr-accent)]/20 text-[var(--tr-accent)] border border-[var(--tr-accent)]/40 flex items-center gap-1.5">
                <GitCompare className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
                Market-Leader Feature: AI Consensus & Hallucination Auditor
              </span>
              <span className="text-xs text-[var(--tr-muted)] font-mono">Peer-Review Across Providers</span>
            </div>
            <h2 className="text-2xl font-bold text-[var(--tr-text)] tracking-tight">
              Cross-Provider Consensus & Discrepancy Matrix
            </h2>
            <p className="text-sm text-[var(--tr-muted)] leading-relaxed">
              Compare architectural recommendations, code snippets, and policies between ChatGPT, Claude, Gemini, and Mistral. Automatically detect where AI providers agree, contradict each other, or offer complementary insights.
            </p>
          </div>

          <div className="flex items-center gap-4 bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-xl p-3 px-4">
            <div>
              <div className="text-xs text-[var(--tr-muted)]">Audited Topics</div>
              <div className="text-xl font-bold font-mono text-[var(--tr-accent)]">{topics.length} Domains</div>
            </div>
            <div className="h-8 w-px bg-[var(--tr-panel)]"></div>
            <div>
              <div className="text-xs text-[var(--tr-muted)]">Consensus Rate</div>
              <div className="text-sm font-semibold text-[var(--tr-accent)] flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                67% Alignment
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main 2-column view */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-[580px]">
        {/* Left Topic Selector */}
        <div className="lg:col-span-5 bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-2xl p-4 space-y-3 flex flex-col shadow-lg">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-[var(--tr-muted)] flex items-center gap-1.5">
              <Compass className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
              Comparative Topics
            </span>
            <div className="flex gap-1 text-[10px]">
              {['ALL', 'Architecture', 'Local AI & DevOps'].map((cat) => (
                <button
                  key={cat}
                  onClick={() => setActiveCategoryFilter(cat)}
                  className={`px-2 py-0.5 rounded font-medium transition-colors ${
                    activeCategoryFilter === cat
                      ? 'bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] text-[var(--tr-text)]'
                      : 'bg-[var(--tr-panel2)] text-[var(--tr-muted)] hover:text-[var(--tr-text)]'
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-2 flex-1 overflow-y-auto pr-1">
            {filteredTopics.map((topic) => {
              const isSelected = topic.id === activeTopic.id;
              return (
                <div
                  key={topic.id}
                  onClick={() => setSelectedTopicId(topic.id)}
                  className={`p-3.5 rounded-xl cursor-pointer transition-all border ${
                    isSelected
                      ? 'bg-[var(--tr-accent)]/40 border-[var(--tr-accent)]/60 shadow-md shadow'
                      : 'bg-[var(--tr-panel2)] border-[var(--tr-border)] hover:border-[var(--tr-border)] hover:bg-[var(--tr-panel2)]'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[var(--tr-panel2)] text-[var(--tr-accent)] border border-[var(--tr-accent)]/40">
                      {topic.category}
                    </span>
                    {getConsensusBadge(topic.consensusLevel)}
                  </div>

                  <h4 className="text-xs font-semibold text-[var(--tr-text)] line-clamp-2 mb-1.5">
                    {topic.topicTitle}
                  </h4>

                  <p className="text-[11px] text-[var(--tr-muted)] line-clamp-2 mb-2">
                    {topic.summary}
                  </p>

                  <div className="flex items-center justify-between text-[10px] text-[var(--tr-muted)]">
                    <span className="font-mono">
                      {topic.providersCompared.map(p => p.provider).join(' vs ')}
                    </span>
                    <span className="text-[var(--tr-accent)] hover:underline">Inspect Stances →</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Detail Pane: Stances & Verdict */}
        <div className="lg:col-span-7 bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-2xl p-6 space-y-6 flex flex-col shadow-lg">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-mono text-[var(--tr-accent)] uppercase tracking-wider">
                {activeTopic.category} • Topic ID: {activeTopic.id}
              </span>
              {getConsensusBadge(activeTopic.consensusLevel)}
            </div>

            <h3 className="text-xl font-bold text-[var(--tr-text)] mb-2">
              {activeTopic.topicTitle}
            </h3>

            <p className="text-xs text-[var(--tr-muted)] leading-relaxed bg-[var(--tr-panel2)] p-3 rounded-lg border border-[var(--tr-border)]">
              {activeTopic.summary}
            </p>
          </div>

          {/* Stances Side-by-Side comparison */}
          <div className="space-y-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[var(--tr-muted)] flex items-center gap-1.5">
              <Brain className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
              Provider Perspectives & Stances ({activeTopic.providersCompared.length})
            </h4>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {activeTopic.providersCompared.map((providerComparison, idx) => (
                <div
                  key={idx}
                  className="p-4 rounded-xl bg-[var(--tr-panel2)] border border-[var(--tr-border)] space-y-2.5 flex flex-col justify-between"
                >
                  <div className="space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className={`px-2 py-0.5 rounded text-xs font-semibold border ${providerColors[providerComparison.provider]}`}>
                        {providerComparison.provider}
                      </span>
                      <div className="flex items-center gap-1 text-[11px] text-[var(--tr-accent)] font-mono">
                        <span>Confidence: {providerComparison.sentimentScore}%</span>
                      </div>
                    </div>

                    <p className="text-xs text-[var(--tr-text)] font-medium">
                      "{providerComparison.stance}"
                    </p>

                    <div className="p-2.5 rounded bg-[var(--tr-panel2)] border border-[var(--tr-border)] font-mono text-[11px] text-[var(--tr-accent)]">
                      {providerComparison.keySnippet}
                    </div>
                  </div>

                  <button
                    onClick={() => handleOpenConversation(providerComparison.conversationId)}
                    className="text-[11px] text-[var(--tr-accent)] hover:text-[var(--tr-accent)] font-medium flex items-center gap-1 self-start pt-1"
                  >
                    <span>Read source conversation</span>
                    <ExternalLink className="w-3 h-3" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Synthesis & Strategic Guidance */}
          <div className="rounded-xl bg-gradient-to-br from-[var(--tr-accent)]/30 to-[var(--tr-panel2)] border border-[var(--tr-accent)]/30 p-4 space-y-2">
            <div className="flex items-center gap-2 text-[var(--tr-accent)] text-xs font-bold">
              <Sparkles className="w-4 h-4 text-[var(--tr-accent)]" />
              <span>Divergence Analysis & Recommended Action</span>
            </div>
            <p className="text-xs text-[var(--tr-muted)]">
              <span className="font-semibold text-[var(--tr-text)]">Analysis: </span>
              {activeTopic.divergenceNotes}
            </p>
            <div className="text-xs text-[var(--tr-accent)] bg-[var(--tr-panel2)] p-2.5 rounded border border-[var(--tr-accent)]/30">
              <span className="font-semibold text-[var(--tr-accent)]">Recommended Resolution: </span>
              {activeTopic.recommendedAction}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
