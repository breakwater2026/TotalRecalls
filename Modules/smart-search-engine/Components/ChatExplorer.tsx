import React, { useState } from 'react';
import { 
  DownloadCloud, 
  RefreshCw, 
  FolderDown, 
  ExternalLink, 
  CheckCircle2, 
  Clock, 
  Tag, 
  Search, 
  MessageSquare,
  FileJson,
  FileText,
  Check
} from 'lucide-react';
import { ChatConversation, AIProvider } from '../types';

interface ChatExplorerProps {
  conversations: ChatConversation[];
  selectedConvId: string | null;
  onSelectConversation: (id: string) => void;
  onAddNewMockChat: () => void;
}

export const ChatExplorer: React.FC<ChatExplorerProps> = ({
  conversations,
  selectedConvId,
  onSelectConversation,
  onAddNewMockChat
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProvider, setSelectedProvider] = useState<string>('ALL');
  const [isExporting, setIsExporting] = useState<boolean>(false);
  const [exportNotice, setExportNotice] = useState<string | null>(null);

  const activeConversation = conversations.find(c => c.id === selectedConvId) || conversations[0];

  const filteredConversations = conversations.filter(conv => {
    const matchesProvider = selectedProvider === 'ALL' || conv.provider === selectedProvider;
    const matchesSearch = 
      conv.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      conv.tags.some(t => t.toLowerCase().includes(searchTerm.toLowerCase())) ||
      conv.messages.some(m => m.content.toLowerCase().includes(searchTerm.toLowerCase()));
    return matchesProvider && matchesSearch;
  });

  const handleExportJSON = () => {
    setIsExporting(true);
    setTimeout(() => {
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(conversations, null, 2));
      const downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", `totalrecalls_export_${new Date().toISOString().slice(0, 10)}.json`);
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
      setIsExporting(false);
      setExportNotice('Export complete: Local JSON chat history archive generated.');
      setTimeout(() => setExportNotice(null), 3500);
    }, 400);
  };

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
      {/* TotalRecalls Pro status banner with TotalRecalls brand colors */}
      <div className="rounded-2xl bg-gradient-to-r from-[var(--tr-bg)] via-[var(--tr-panel2)] to-[var(--tr-bg)] border border-[var(--tr-accent)]/30 p-6 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
        <div>
          <div className="flex items-center space-x-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[var(--tr-accent)]/15 text-[var(--tr-accent)] border border-[var(--tr-accent)]/30 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5" />
              TotalRecalls Pro: Local Chat Downloader
            </span>
            <span className="text-xs text-[var(--tr-accent)] font-mono">totalrecalls.app</span>
          </div>
          <h2 className="text-2xl font-bold text-[var(--tr-text)] tracking-tight">
            Universal AI Chat Downloader & Local Vault
          </h2>
          <p className="text-sm text-[var(--tr-muted)] mt-1">
            Continuous local backup for ChatGPT, Claude, Gemini, Perplexity, and Mistral conversations. 
            All files are stored in your private local directory with encrypted local storage.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={onAddNewMockChat}
            className="px-3.5 py-2 bg-[var(--tr-panel)] hover:bg-[var(--tr-panel)] text-[var(--tr-text)] border border-[var(--tr-border)] rounded-xl font-medium text-xs transition-colors flex items-center gap-2"
          >
            <RefreshCw className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
            <span>Simulate Sync Run</span>
          </button>
          <button
            onClick={handleExportJSON}
            disabled={isExporting}
            className="px-4 py-2 bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] hover:from-[var(--tr-accent)] hover:to-[var(--tr-accent2)] text-[var(--tr-text)] rounded-xl font-semibold text-xs transition-all flex items-center gap-2 shadow-md shadow"
          >
            <DownloadCloud className="w-4 h-4" />
            <span>Export Archive</span>
          </button>
        </div>
      </div>

      {exportNotice && (
        <div className="p-3 bg-[var(--tr-accent)]/15 border border-[var(--tr-accent)]/40 rounded-xl text-[var(--tr-accent)] text-xs flex items-center gap-2 animate-fadeIn">
          <Check className="w-4 h-4 text-[var(--tr-accent)]" />
          <span>{exportNotice}</span>
        </div>
      )}

      {/* Main 2-column view: List & Conversation reader */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-[640px]">
        {/* Left Sidebar: Conversations List */}
        <div className="lg:col-span-5 bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-2xl p-4 space-y-4 flex flex-col shadow-lg">
          {/* Filter and search */}
          <div className="space-y-3">
            <div className="relative">
              <Search className="w-4 h-4 text-[var(--tr-accent)] absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Filter by keyword, title, tag..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-3 py-2 bg-[var(--tr-panel2)] border border-[var(--tr-border)] focus:border-[var(--tr-accent)] rounded-lg text-xs text-[var(--tr-text)] placeholder-[var(--tr-muted)] focus:outline-none"
              />
            </div>

            {/* Provider tags */}
            <div className="flex flex-wrap gap-1">
              {['ALL', 'ChatGPT', 'Claude', 'Gemini', 'Perplexity', 'Mistral'].map((p) => (
                <button
                  key={p}
                  onClick={() => setSelectedProvider(p)}
                  className={`px-2 py-0.5 rounded text-[11px] font-semibold transition-colors ${
                    selectedProvider === p
                      ? 'bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] text-[var(--tr-text)]'
                      : 'bg-[var(--tr-panel2)] text-[var(--tr-muted)] hover:text-[var(--tr-text)]'
                  }`}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>

          {/* List */}
          <div className="flex-1 overflow-y-auto space-y-2 pr-1 max-h-[560px]">
            {filteredConversations.map((conv) => {
              const isSelected = conv.id === activeConversation?.id;
              return (
                <div
                  key={conv.id}
                  onClick={() => onSelectConversation(conv.id)}
                  className={`p-3.5 rounded-xl cursor-pointer transition-all border ${
                    isSelected
                      ? 'bg-[var(--tr-accent)]/40 border-[var(--tr-accent)]/60 shadow-md shadow'
                      : 'bg-[var(--tr-panel2)] border-[var(--tr-border)] hover:border-[var(--tr-border)] hover:bg-[var(--tr-panel2)]'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-semibold border ${providerColors[conv.provider]}`}>
                      {conv.provider}
                    </span>
                    <span className="text-[11px] text-[var(--tr-muted)] font-mono">
                      {conv.createdAt.slice(0, 10)}
                    </span>
                  </div>

                  <h4 className="text-xs font-semibold text-[var(--tr-text)] line-clamp-2 mb-2">
                    {conv.title}
                  </h4>

                  <div className="flex items-center justify-between text-[11px] text-[var(--tr-muted)]">
                    <span>{conv.messageCount} turns • {conv.totalTokens.toLocaleString()} tokens</span>
                    {conv.isIndexed && (
                      <span className="text-[var(--tr-accent)] flex items-center gap-1 text-[10px] font-medium">
                        <CheckCircle2 className="w-3 h-3" />
                        Vector Indexed
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Reader: Conversation content */}
        <div className="lg:col-span-7 bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-2xl p-6 flex flex-col shadow-lg">
          {activeConversation ? (
            <div className="space-y-6 flex-1 flex flex-col">
              {/* Header */}
              <div className="border-b border-[var(--tr-border)] pb-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-0.5 rounded text-xs font-semibold border ${providerColors[activeConversation.provider]}`}>
                      {activeConversation.provider}
                    </span>
                    <span className="text-xs font-mono text-[var(--tr-accent)]">
                      Model: {activeConversation.model}
                    </span>
                  </div>
                  <span className="text-xs text-[var(--tr-muted)] font-mono">
                    ID: {activeConversation.id}
                  </span>
                </div>

                <h3 className="text-xl font-bold text-[var(--tr-text)] mb-2">
                  {activeConversation.title}
                </h3>

                <div className="flex flex-wrap items-center gap-1.5 text-xs">
                  {activeConversation.tags.map((tag, i) => (
                    <span key={i} className="px-2 py-0.5 rounded bg-[var(--tr-panel2)] border border-[var(--tr-border)] text-[var(--tr-accent)] font-mono">
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>

              {/* Message turns */}
              <div className="space-y-4 flex-1 overflow-y-auto max-h-[500px] pr-2">
                {activeConversation.messages.map((msg) => {
                  const isUser = msg.role === 'user';
                  return (
                    <div
                      key={msg.id}
                      className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}
                    >
                      <div className="flex items-center space-x-2 mb-1 px-1">
                        <span className="text-[11px] font-semibold text-[var(--tr-muted)] uppercase tracking-wider">
                          {isUser ? 'You' : activeConversation.provider}
                        </span>
                        <span className="text-[10px] text-[var(--tr-muted)] font-mono">
                          {msg.timestamp}
                        </span>
                      </div>

                      <div
                        className={`max-w-[85%] rounded-2xl p-4 text-xs leading-relaxed whitespace-pre-wrap font-sans ${
                          isUser
                            ? 'bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] text-[var(--tr-text)] rounded-tr-none shadow-md shadow'
                            : 'bg-[var(--tr-panel2)] text-[var(--tr-text)] border border-[var(--tr-border)] rounded-tl-none'
                        }`}
                      >
                        {msg.content}
                      </div>

                      {msg.tokenCount && (
                        <span className="text-[10px] text-[var(--tr-muted)] mt-1 px-1 font-mono">
                          {msg.tokenCount} tokens
                        </span>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center text-[var(--tr-muted)] text-sm">
              Select a conversation to read archived turn history.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};