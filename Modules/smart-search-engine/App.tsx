import React, { useState } from 'react';
import { Navbar, AppTabType } from './components/Navbar';
import { WebsitePresentation } from './components/WebsitePresentation';
import { DeliveryPackagingStudio } from './components/DeliveryPackagingStudio';
import { OverviewHub } from './components/OverviewHub';
import { SearchChatInterface } from './components/SearchChatInterface';
import { VectorSearch } from './components/VectorSearch';
import { RAGSQLStudio } from './components/RAGSQLStudio';
import { ConsensusAuditor } from './components/ConsensusAuditor';
import { DatasetScrubber } from './components/DatasetScrubber';
import { EmbeddingBenchmark } from './components/EmbeddingBenchmark';
import { KnowledgeGraph } from './components/KnowledgeGraph';
import { BackupScheduler } from './components/BackupScheduler';
import { IntegrityTestSuite } from './components/IntegrityTestSuite';
import { PowerUserManual } from './components/PowerUserManual';
import { DemoScript } from './components/DemoScript';
import { ChatExplorer } from './components/ChatExplorer';
import { SpecsAndPricing } from './components/SpecsAndPricing';
import { INITIAL_CONVERSATIONS } from './constants';
import { ChatConversation } from './types';
import { buildVectorIndex } from './services/ragEngine';

export function App() {
  const [conversations, setConversations] = useState<ChatConversation[]>(INITIAL_CONVERSATIONS);
  const [activeModelId, setActiveModelId] = useState<string>('bge-small-en-v15');
  const [activeDimension, setActiveDimension] = useState<number>(384);
  const [chunks, setChunks] = useState(() => buildVectorIndex(INITIAL_CONVERSATIONS, 384));
  const [activeTab, setActiveTab] = useState<AppTabType>('website');
  const [selectedConvId, setSelectedConvId] = useState<string | null>(null);
  const [isDark, setIsDark] = useState(true);

  const toggleTheme = () => {
    const next = !isDark;
    setIsDark(next);
    document.documentElement.classList.toggle('dark', next);
    try { localStorage.setItem('tr-theme', next ? 'dark' : 'light'); } catch (e) {}
  };

  const handleSelectModel = (modelId: string, dimension: number) => {
    setActiveModelId(modelId);
    setActiveDimension(dimension);
    setChunks(buildVectorIndex(conversations, dimension));
  };

  const handleAddNewMockChat = () => {
    const newId = `tr-conv-${Date.now().toString().slice(-4)}`;
    const newChat: ChatConversation = {
      id: newId,
      title: 'Kubernetes Pod Security & Local Offline RAG Clusters',
      provider: 'ChatGPT',
      model: 'gpt-4o',
      createdAt: new Date().toISOString().slice(0, 16).replace('T', ' '),
      updatedAt: new Date().toISOString().slice(0, 16).replace('T', ' '),
      tags: ['kubernetes', 'security', 'rag', 'offline'],
      messageCount: 2,
      totalTokens: 980,
      isIndexed: true,
      messages: [
        {
          id: `m-${newId}-1`,
          role: 'user',
          content: 'How do we enforce non-root user containers and local vector search in an air-gapped Kubernetes pod?',
          timestamp: new Date().toISOString().slice(0, 16).replace('T', ' '),
          tokenCount: 30
        },
        {
          id: `m-${newId}-2`,
          role: 'assistant',
          content: 'Set `runAsNonRoot: true` in your pod securityContext and mount a local emptyDir or persistent volume with SQLite sqlite-vec. TotalRecalls operates completely in-cluster without external egress.',
          timestamp: new Date().toISOString().slice(0, 16).replace('T', ' '),
          tokenCount: 950
        }
      ]
    };

    const updated = [newChat, ...conversations];
    setConversations(updated);
    setChunks(buildVectorIndex(updated, activeDimension));
  };

  return (
    <div className="min-h-screen bg-[var(--tr-bg)] text-[var(--tr-text)] flex flex-col font-sans selection:bg-[var(--tr-accent)] selection:text-[var(--tr-text)]">
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        indexedCount={chunks.length}
        totalConversations={conversations.length}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === 'website' && (
          <WebsitePresentation 
            onSelectTab={(tab) => setActiveTab(tab)} 
          />
        )}

        {activeTab === 'delivery' && (
          <DeliveryPackagingStudio 
            conversations={conversations}
            chunks={chunks}
            onSelectTab={(tab) => setActiveTab(tab)}
          />
        )}

        {activeTab === 'overview' && (
          <OverviewHub 
            conversations={conversations} 
            chunks={chunks}
            onSelectTab={(tab) => setActiveTab(tab)}
            onOpenConversation={(id) => {
              setSelectedConvId(id);
              setActiveTab('chatExplorer');
            }}
            onAddNewChat={handleAddNewMockChat}
          />
        )}

        {activeTab === 'searchChat' && (
          <SearchChatInterface 
            chunks={chunks}
            conversations={conversations}
            onOpenConversation={(id) => {
              setSelectedConvId(id);
              setActiveTab('chatExplorer');
            }}
          />
        )}

        {activeTab === 'vectorSearch' && (
          <VectorSearch 
            chunks={chunks} 
            conversations={conversations}
            onOpenConversation={(id) => {
              setSelectedConvId(id);
              setActiveTab('chatExplorer');
            }}
          />
        )}

        {activeTab === 'ragSQL' && (
          <RAGSQLStudio 
            conversations={conversations}
            chunks={chunks}
          />
        )}

        {activeTab === 'consensus' && (
          <ConsensusAuditor 
            conversations={conversations}
            onOpenConversation={(id) => {
              setSelectedConvId(id);
              setActiveTab('chatExplorer');
            }}
          />
        )}

        {activeTab === 'scrubber' && (
          <DatasetScrubber 
            conversations={conversations}
          />
        )}

        {activeTab === 'backup' && (
          <BackupScheduler 
            conversations={conversations}
            chunks={chunks}
            onSelectTab={(tab) => setActiveTab(tab)}
          />
        )}

        {activeTab === 'integrityTests' && (
          <IntegrityTestSuite 
            conversations={conversations}
            chunks={chunks}
            onSelectTab={(tab) => setActiveTab(tab)}
          />
        )}

        {activeTab === 'benchmarks' && (
          <EmbeddingBenchmark 
            activeModelId={activeModelId}
            onSelectModel={handleSelectModel}
          />
        )}

        {activeTab === 'knowledge' && (
          <KnowledgeGraph 
            conversations={conversations}
            onSelectConversation={(id) => {
              setSelectedConvId(id);
              setActiveTab('chatExplorer');
            }}
          />
        )}

        {activeTab === 'chatExplorer' && (
          <ChatExplorer 
            conversations={conversations}
            initialSelectedId={selectedConvId}
          />
        )}

        {activeTab === 'manual' && (
          <PowerUserManual onSelectTab={(tab) => setActiveTab(tab)} />
        )}

        {activeTab === 'demoScript' && (
          <DemoScript onSelectTab={(tab) => setActiveTab(tab)} />
        )}

        {activeTab === 'specs' && (
          <SpecsAndPricing onSelectTab={(tab) => setActiveTab(tab)} />
        )}
      </main>

      <footer className="border-t border-[var(--tr-border)] bg-[var(--tr-bg)] py-8 text-center text-xs text-[var(--tr-muted)]">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="font-semibold text-[var(--tr-text)]">TotalRecalls Smart Search Engine</span>
            <span>•</span>
            <span>Downside Protection Vault & Air-Gapped Code Integrity Tests</span>
          </div>
          <div className="flex items-center space-x-4">
            <button onClick={() => setActiveTab('backup')} className="hover:text-[var(--tr-accent)] transition-colors">
              Backup Vault
            </button>
            <span>•</span>
            <button onClick={() => setActiveTab('integrityTests')} className="hover:text-[var(--tr-accent)] transition-colors">
              Code Integrity Tests
            </button>
            <span>•</span>
            <button onClick={() => setActiveTab('delivery')} className="hover:text-[var(--tr-accent)] transition-colors">
              .ZIP & Installer
            </button>
            <span>•</span>
            <button onClick={() => setActiveTab('website')} className="hover:text-[var(--tr-accent)] transition-colors">
              Website Showcase
            </button>
            <span>•</span>
            <button onClick={toggleTheme} className="hover:text-[var(--tr-accent)] transition-colors" title="Toggle dark/light theme">
              {isDark ? '☀️' : '🌙'}
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
