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
      {/* Hero Product Banner with TotalRecalls cyan/teal gradient */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-[#0e1f2f] via-[#0c1626] to-[#070c16] border border-cyan-500/30 p-8 shadow-2xl">
        <div className="relative z-10 max-w-3xl space-y-4">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-500/15 border border-cyan-500/40 text-cyan-300 text-xs font-semibold">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span>
            <span>TotalRecalls Smart Search Engine: Complete Local Chat Intelligence</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-black text-white tracking-tight leading-tight">
            Universal AI Chat Downloader <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-sky-400">
              + TotalRecalls Smart Search Engine
            </span>
          </h1>

          <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
            TotalRecalls (<a href="https://totalrecalls.app" target="_blank" rel="noopener noreferrer" className="text-cyan-400 font-semibold underline underline-offset-2">totalrecalls.app</a>) combines continuous local chat downloads with the new <strong>Smart Search Engine</strong>—featuring air-gapped vector retrieval, multi-model consensus auditing, automated knowledge graphs, PII scrubbing, downside protection backup scheduling, and regression code integrity tests.
          </p>

          <div className="flex flex-wrap items-center gap-3 pt-2">
            <button
              onClick={() => navigateTo('searchChat')}
              className="inline-flex items-center space-x-2 bg-gradient-to-r from-cyan-500 to-teal-500 hover:from-cyan-400 hover:to-teal-400 text-slate-950 font-bold px-6 py-3 rounded-xl shadow-lg shadow-cyan-500/25 transition-all text-sm"
            >
              <Sparkles className="w-4 h-4 text-slate-950" />
              <span>Launch Unified Search Chat</span>
            </button>

            <button
              onClick={() => navigateTo('backup')}
              className="inline-flex items-center space-x-2 bg-slate-900/90 hover:bg-slate-800 text-emerald-300 border border-emerald-500/40 font-semibold px-5 py-3 rounded-xl text-sm transition-colors"
            >
              <Clock className="w-4 h-4 text-emerald-400" />
              <span>Downside Backup Vault</span>
            </button>

            <button
              onClick={() => navigateTo('integrityTests')}
              className="inline-flex items-center space-x-2 bg-slate-900/90 hover:bg-slate-800 text-cyan-300 border border-cyan-500/40 font-semibold px-5 py-3 rounded-xl text-sm transition-colors"
            >
              <FileCheck className="w-4 h-4 text-cyan-400" />
              <span>Run Code Integrity Suite</span>
            </button>

            {onAddNewChat && (
              <button
                onClick={onAddNewChat}
                className="inline-flex items-center space-x-2 bg-slate-900/90 hover:bg-slate-800 text-slate-300 border border-slate-700 font-semibold px-4 py-3 rounded-xl text-sm transition-colors"
              >
                <span>+ Simulate Chat Sync</span>
              </button>
            )}
          </div>
        </div>

        {/* Ambient background glow */}
        <div className="absolute right-0 top-0 -mr-20 -mt-20 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>
      </div>

      {/* Downside Protection & Security Highlights */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div 
          onClick={() => navigateTo('backup')}
          className="p-5 rounded-2xl bg-gradient-to-br from-[#0a1826] to-[#070c16] border border-emerald-500/30 hover:border-emerald-500/60 transition-all cursor-pointer shadow-lg group"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/20 flex items-center justify-center text-emerald-400">
                <Clock className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-bold text-white text-sm group-hover:text-emerald-300 transition-colors">
                  Downside Protection & Backup Scheduler
                </h3>
                <p className="text-xs text-slate-400">Autonomous snapshots, SHA-256 checks & cold storage</p>
              </div>
            </div>
            <ArrowRight className="w-4 h-4 text-emerald-400 group-hover:translate-x-1 transition-transform" />
          </div>
        </div>

        <div 
          onClick={() => navigateTo('integrityTests')}
          className="p-5 rounded-2xl bg-gradient-to-br from-[#0c1a2e] to-[#070c16] border border-cyan-500/30 hover:border-cyan-500/60 transition-all cursor-pointer shadow-lg group"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-cyan-500/20 flex items-center justify-center text-cyan-400">
                <FileCheck className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-bold text-white text-sm group-hover:text-cyan-300 transition-colors">
                  SSE Code Integrity Test Suite
                </h3>
                <p className="text-xs text-slate-400">12 component unit & regression invariant tests</p>
              </div>
            </div>
            <ArrowRight className="w-4 h-4 text-cyan-400 group-hover:translate-x-1 transition-transform" />
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-[#0e1626] border border-slate-800 p-5 rounded-2xl shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Total Conversations</span>
            <MessageSquare className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="mt-2 text-2xl font-black text-white">{conversations.length}</div>
          <div className="mt-1 text-xs text-emerald-400 flex items-center space-x-1">
            <CheckCircle2 className="w-3 h-3" />
            <span>Downloader synced locally</span>
          </div>
        </div>

        <div className="bg-[#0e1626] border border-slate-800 p-5 rounded-2xl shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Vector Embeddings</span>
            <Search className="w-4 h-4 text-teal-400" />
          </div>
          <div className="mt-2 text-2xl font-black text-white">{chunks.length} Chunks</div>
          <div className="mt-1 text-xs text-cyan-400">
            <span>384-dim HNSW indexed</span>
          </div>
        </div>

        <div className="bg-[#0e1626] border border-slate-800 p-5 rounded-2xl shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Corpus Tokens</span>
            <Cpu className="w-4 h-4 text-amber-400" />
          </div>
          <div className="mt-2 text-2xl font-black text-white">
            {conversations.reduce((acc, c) => acc + c.totalTokens, 0).toLocaleString()}
          </div>
          <div className="mt-1 text-xs text-slate-400">
            <span>Across 5 AI providers</span>
          </div>
        </div>

        <div className="bg-[#0e1626] border border-slate-800 p-5 rounded-2xl shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Air-Gap Security</span>
            <Lock className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="mt-2 text-2xl font-black text-emerald-400">Zero Cloud Egress</div>
          <div className="mt-1 text-xs text-slate-400">
            <span>100% Private on Device</span>
          </div>
        </div>
      </div>

      {/* Visual Analytics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Token Distribution by Provider */}
        <div className="lg:col-span-8 bg-[#0e1626] border border-slate-800 p-6 rounded-2xl shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
            <div>
              <h3 className="font-bold text-white text-base">Token Distribution by AI Provider</h3>
              <p className="text-xs text-slate-400">Aggregated token volume across your local chat archives</p>
            </div>
            <button 
              onClick={() => navigateTo('ragSQL')}
              className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center space-x-1"
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
                  contentStyle={{ backgroundColor: '#070c16', borderColor: '#334155', borderRadius: '12px' }}
                  labelStyle={{ color: '#ffffff' }}
                />
                <Bar dataKey="tokens" fill="#06b6d4" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Provider Share Pie */}
        <div className="lg:col-span-4 bg-[#0e1626] border border-slate-800 p-6 rounded-2xl shadow-sm space-y-4">
          <div className="border-b border-slate-800/80 pb-3">
            <h3 className="font-bold text-white text-base">Conversation Share</h3>
            <p className="text-xs text-slate-400">Provider chat distribution</p>
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
                  contentStyle={{ backgroundColor: '#070c16', borderColor: '#334155', borderRadius: '12px' }}
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
                <span className="text-slate-300 font-medium">{entry.name}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
