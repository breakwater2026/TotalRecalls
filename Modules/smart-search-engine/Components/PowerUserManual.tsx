import React from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  ResponsiveContainer, 
  PieChart, 
  Pie, 
  Cell 
} from 'recharts';
import { 
  Sparkles, 
  Search, 
  Terminal, 
  HardDrive, 
  ShieldCheck, 
  ArrowRight, 
  Database,
  Cpu,
  MessageSquare,
  CheckCircle2,
  GitCompare,
  Lock,
  Network,
  Video,
  Clock,
  FileCheck
} from 'lucide-react';
import { ChatConversation, ChunkEmbedding, AIProvider } from '../types';
import { AppTabType } from './Navbar';

interface OverviewHubProps {
  conversations: ChatConversation[];
  chunks: ChunkEmbedding[];
  onSelectTab?: (tab: AppTabType) => void;
  onNavigate?: (tab: AppTabType) => void;
  onOpenConversation?: (id: string) => void;
  onSelectConversation?: (id: string) => void;
  onAddNewChat?: () => void;
}

export const OverviewHub: React.FC<OverviewHubProps> = ({
  conversations,
  chunks,
  onSelectTab,
  onNavigate,
  onOpenConversation,
  onSelectConversation,
  onAddNewChat
}) => {
  const navigateTo = (tab: AppTabType) => {
    if (onSelectTab) onSelectTab(tab);
    else if (onNavigate) onNavigate(tab);
  };

  const handleOpenConversation = (id: string) => {
    if (onOpenConversation) onOpenConversation(id);
    else if (onSelectConversation) onSelectConversation(id);
  };

  // Compute chart aggregates
  const providerStats = conversations.reduce((acc, conv) => {
    acc[conv.provider] = (acc[conv.provider] || 0) + conv.totalTokens;
    return acc;
  }, {} as Record<AIProvider, number>);

  const barData = Object.entries(providerStats).map(([provider, tokens]) => ({
    name: provider,
    tokens: tokens
  }));

  const pieData = Object.entries(
    conversations.reduce((acc, conv) => {
      acc[conv.provider] = (acc[conv.provider] || 0) + 1;
      return acc;
    }, {} as Record<string, number>)
  ).map(([name, value]) => ({ name, value }));

  const COLORS = ['#06b6d4', '#14b8a6', '#0ea5e9', '#10b981', '#f59e0b', '#8b5cf6'];

  return (
    <div className="space-y-8">
      {/* Hero Product Banner with TotalRecalls brand accent */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-[#0e1f2f] via-[#0c1626] to-[var(--tr-bg)] border border-[var(--tr-accent)]/30 p-8 shadow-2xl">
        <div className="relative z-10 max-w-3xl space-y-4">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-[var(--tr-accent)]/15 border border-[var(--tr-accent)]/40 text-[var(--tr-accent)] text-xs font-semibold">
            <span className="w-2 h-2 rounded-full bg-[var(--tr-accent)] animate-ping"></span>
            <span>TotalRecalls Smart Search Engine: Complete Local Chat Intelligence</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-black text-[var(--tr-text)] tracking-tight leading-tight">
            Universal AI Chat Downloader <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[var(--tr-accent)] via-[var(--tr-accent)] to-sky-400">
              + TotalRecalls Smart Search Engine
            </span>
          </h1>

          <p className="text-[var(--tr-muted)] text-sm sm:text-base leading-relaxed">
            TotalRecalls (<a href="https://totalrecalls.app" target="_blank" rel="noopener noreferrer" className="text-[var(--tr-accent)] font-semibold underline underline-offset-2">totalrecalls.app</a>) combines continuous local chat downloads with the new <strong>Smart Search Engine</strong>—featuring local vector retrieval, multi-model consensus auditing, automated knowledge graphs, PII scrubbing, downside protection backup scheduling, and regression code integrity tests.
          </p>

          <div className="flex flex-wrap items-center gap-3 pt-2">
            <button
              onClick={() => navigateTo('searchChat')}
              className="inline-flex items-center space-x-2 bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] hover:from-[var(--tr-accent)] hover:to-[var(--tr-accent2)] text-[var(--tr-text)] font-bold px-6 py-3 rounded-xl shadow-lg shadow transition-all text-sm"
            >
              <Sparkles className="w-4 h-4 text-[var(--tr-text)]" />
              <span>Launch Unified Search Chat</span>
            </button>

            <button
              onClick={() => navigateTo('backup')}
              className="inline-flex items-center space-x-2 bg-[var(--tr-bg)] hover:bg-[var(--tr-panel)] text-[var(--tr-good)] border border-[var(--tr-good)]/40 font-semibold px-5 py-3 rounded-xl text-sm transition-colors"
            >
              <Clock className="w-4 h-4 text-[var(--tr-good)]" />
              <span>Downside Backup Vault</span>
            </button>

            <button
              onClick={() => navigateTo('integrityTests')}
              className="inline-flex items-center space-x-2 bg-[var(--tr-bg)] hover:bg-[var(--tr-panel)] text-[var(--tr-accent)] border border-[var(--tr-accent)]/40 font-semibold px-5 py-3 rounded-xl text-sm transition-colors"
            >
              <FileCheck className="w-4 h-4 text-[var(--tr-accent)]" />
              <span>Run Code Integrity Suite</span>
            </button>

            {onAddNewChat && (
              <button
                onClick={onAddNewChat}
                className="inline-flex items-center space-x-2 bg-[var(--tr-bg)] hover:bg-[var(--tr-panel)] text-[var(--tr-muted)] border border-[var(--tr-border)] font-semibold px-4 py-3 rounded-xl text-sm transition-colors"
              >
                <span>+ Simulate Chat Sync</span>
              </button>
            )}
          </div>
        </div>

        {/* Ambient background glow */}
        <div className="absolute right-0 top-0 -mr-20 -mt-20 w-96 h-96 bg-[var(--tr-accent)]/10 rounded-full blur-3xl pointer-events-none"></div>
      </div>

      {/* Downside Protection & Security Highlights */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div 
          onClick={() => navigateTo('backup')}
          className="p-5 rounded-2xl bg-gradient-to-br from-[#0a1826] to-[var(--tr-bg)] border border-[var(--tr-good)]/30 hover:border-[var(--tr-good)]/60 transition-all cursor-pointer shadow-lg group"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-[var(--tr-good)]/20 flex items-center justify-center text-[var(--tr-good)]">
                <Clock className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-bold text-[var(--tr-text)] text-sm group-hover:text-[var(--tr-good)] transition-colors">
                  Downside Protection & Backup Scheduler
                </h3>
                <p className="text-xs text-[var(--tr-muted)]">Autonomous snapshots, SHA-256 checks & cold storage</p>
              </div>
            </div>
            <ArrowRight className="w-4 h-4 text-[var(--tr-good)] group-hover:translate-x-1 transition-transform" />
          </div>
        </div>

        <div 
          onClick={() => navigateTo('integrityTests')}
          className="p-5 rounded-2xl bg-gradient-to-br from-[#0c1a2e] to-[var(--tr-bg)] border border-[var(--tr-accent)]/30 hover:border-[var(--tr-accent)]/60 transition-all cursor-pointer shadow-lg group"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-[var(--tr-accent)]/20 flex items-center justify-center text-[var(--tr-accent)]">
                <FileCheck className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-bold text-[var(--tr-text)] text-sm group-hover:text-[var(--tr-accent)] transition-colors">
                  SSE Code Integrity Test Suite
                </h3>
                <p className="text-xs text-[var(--tr-muted)]">12 component unit & regression invariant tests</p>
              </div>
            </div>
            <ArrowRight className="w-4 h-4 text-[var(--tr-accent)] group-hover:translate-x-1 transition-transform" />
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-[var(--tr-panel)] border border-[var(--tr-border)] p-5 rounded-2xl shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-[var(--tr-muted)]">Total Conversations</span>
            <MessageSquare className="w-4 h-4 text-[var(--tr-accent)]" />
          </div>
          <div className="mt-2 text-2xl font-black text-[var(--tr-text)]">{conversations.length}</div>
          <div className="mt-1 text-xs text-[var(--tr-good)] flex items-center space-x-1">
            <CheckCircle2 className="w-3 h-3" />
            <span>Downloader synced locally</span>
          </div>
        </div>

        <div className="bg-[var(--tr-panel)] border border-[var(--tr-border)] p-5 rounded-2xl shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-[var(--tr-muted)]">Vector Embeddings</span>
            <Search className="w-4 h-4 text-[var(--tr-accent)]" />
          </div>
          <div className="mt-2 text-2xl font-black text-[var(--tr-text)]">{chunks.length} Chunks</div>
          <div className="mt-1 text-xs text-[var(--tr-accent)]">
            <span>384-dim HNSW indexed</span>
          </div>
        </div>

        <div className="bg-[var(--tr-panel)] border border-[var(--tr-border)] p-5 rounded-2xl shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-[var(--tr-muted)]">Corpus Tokens</span>
            <Cpu className="w-4 h-4 text-amber-400" />
          </div>
          <div className="mt-2 text-2xl font-black text-[var(--tr-text)]">
            {conversations.reduce((acc, c) => acc + c.totalTokens, 0).toLocaleString()}
          </div>
          <div className="mt-1 text-xs text-[var(--tr-muted)]">
            <span>Across 5 AI providers</span>
          </div>
        </div>

        <div className="bg-[var(--tr-panel)] border border-[var(--tr-border)] p-5 rounded-2xl shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-[var(--tr-muted)]">Local-Only Security</span>
            <Lock className="w-4 h-4 text-[var(--tr-good)]" />
          </div>
          <div className="mt-2 text-2xl font-black text-[var(--tr-good)]">Runs on your PC</div>
          <div className="mt-1 text-xs text-[var(--tr-muted)]">
            <span>Nothing uploaded</span>
          </div>
        </div>
      </div>

      {/* Visual Analytics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Token Distribution by Provider */}
        <div className="lg:col-span-8 bg-[var(--tr-panel)] border border-[var(--tr-border)] p-6 rounded-2xl shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-[var(--tr-border)] pb-3">
            <div>
              <h3 className="font-bold text-[var(--tr-text)] text-base">Token Distribution by AI Provider</h3>
              <p className="text-xs text-[var(--tr-muted)]">Aggregated token volume across your local chat archives</p>
            </div>
            <button 
              onClick={() => navigateTo('ragSQL')}
              className="text-xs text-[var(--tr-accent)] hover:text-[var(--tr-accent)] flex items-center space-x-1"
            >
              <span>Query via SQL</span>
              <ArrowRight className="w-3 h-3" />
            </button>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData} margin={{ top: 10, right: 10, left: 0, bottom: 20 }}>
                <XAxis dataKey="name" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'var(--tr-bg)', borderColor: 'var(--tr-border)', borderRadius: '12px' }}
                  labelStyle={{ color: '#ffffff' }}
                />
                <Bar dataKey="tokens" fill="#06b6d4" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Provider Share Pie */}
        <div className="lg:col-span-4 bg-[var(--tr-panel)] border border-[var(--tr-border)] p-6 rounded-2xl shadow-sm space-y-4">
          <div className="border-b border-[var(--tr-border)] pb-3">
            <h3 className="font-bold text-[var(--tr-text)] text-base">Conversation Share</h3>
            <p className="text-xs text-[var(--tr-muted)]">Provider chat distribution</p>
          </div>

          <div className="h-52 w-full flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={75}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {pieData.map((_entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: 'var(--tr-bg)', borderColor: 'var(--tr-border)', borderRadius: '12px' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-3 text-xs">
            {pieData.map((entry, index) => (
              <div key={entry.name} className="flex items-center space-x-1.5">
                <span 
                  className="w-2.5 h-2.5 rounded-full" 
                  style={{ backgroundColor: COLORS[index % COLORS.length] }}
                />
                <span className="text-[var(--tr-muted)] font-medium">{entry.name}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
