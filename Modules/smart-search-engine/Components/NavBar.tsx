import React from 'react';
import { 
  Search, 
  Database, 
  MessageSquare, 
  BookOpen, 
  Sparkles, 
  Layers, 
  Activity,
  HardDrive,
  GitCompare,
  Network
} from 'lucide-react';

export type AppTabType = 
  | 'searchChat'
  | 'vectorSearch'
  | 'ragSQL'
  | 'chatExplorer'
  | 'consensus'
  | 'scrubber'
  | 'benchmark'
  | 'knowledgeGraph'
  | 'overview'
  | 'delivery'
  | 'specsAndPricing'
  | 'backup'
  | 'integrity'
  | 'manual'
  | 'script'
  | 'website';

export interface NavbarProps {
  activeTab: AppTabType;
  setActiveTab: (tab: AppTabType) => void;
  indexedCount?: number;
  totalConversations?: number;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  indexedCount = 0,
  totalConversations = 0
}) => {
  const primaryTabs: { id: AppTabType; label: string; icon: React.ReactNode }[] = [
    { id: 'searchChat', label: 'Search & Chat', icon: <MessageSquare className="w-4 h-4" /> },
    { id: 'vectorSearch', label: 'Semantic Vector', icon: <Search className="w-4 h-4" /> },
    { id: 'ragSQL', label: 'SQL RAG', icon: <Database className="w-4 h-4" /> },
    { id: 'chatExplorer', label: 'Chat Explorer', icon: <Layers className="w-4 h-4" /> },
    { id: 'consensus', label: 'Consensus Auditor', icon: <GitCompare className="w-4 h-4" /> },
    { id: 'knowledgeGraph', label: 'Knowledge Graph', icon: <Network className="w-4 h-4" /> },
    { id: 'overview', label: 'Overview Hub', icon: <Activity className="w-4 h-4" /> },
    { id: 'manual', label: 'User Guide', icon: <BookOpen className="w-4 h-4" /> },
  ];

  return (
    <header className="border-b border-[var(--tr-border)] bg-[var(--tr-panel)]/80 backdrop-blur sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 gap-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-[var(--tr-accent)] flex items-center justify-center text-[var(--tr-on-amber)] font-bold text-base shadow-sm">
              TR
            </div>
            <div>
              <span className="font-bold text-sm tracking-tight text-[var(--tr-text)] flex items-center gap-1.5">
                TotalRecalls
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-[var(--tr-panel2)] text-[var(--tr-accent)] border border-[var(--tr-border)]">
                  SSE v1.0
                </span>
              </span>
              <span className="text-[11px] text-[var(--tr-muted)] block">
                Smart Search Engine &middot; 100% Local RAG
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3 text-xs text-[var(--tr-muted)] font-mono">
            <span className="hidden sm:inline-flex items-center gap-1 px-2 py-1 rounded bg-[var(--tr-panel2)] border border-[var(--tr-border)]">
              <HardDrive className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
              <span>{totalConversations} chats indexed</span>
            </span>
            <span className="hidden sm:inline-flex items-center gap-1 px-2 py-1 rounded bg-[var(--tr-panel2)] border border-[var(--tr-border)]">
              <Sparkles className="w-3.5 h-3.5 text-[var(--tr-accent2)]" />
              <span>{indexedCount} chunks (384d)</span>
            </span>
          </div>
        </div>

        {/* Tab Navigation */}
        <nav className="flex space-x-1 overflow-x-auto py-2 scrollbar-none border-t border-[var(--tr-border)]/50">
          {primaryTabs.map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all whitespace-nowrap ${
                  isActive
                    ? 'bg-[var(--tr-accent)] text-[var(--tr-on-amber)] shadow-sm'
                    : 'text-[var(--tr-muted)] hover:text-[var(--tr-text)] hover:bg-[var(--tr-panel2)]'
                }`}
              >
                {tab.icon}
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
};
