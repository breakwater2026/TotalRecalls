import React, { useState, useEffect } from 'react';
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
import {
  isSseActivated,
  sseLicenseKey,
  activateSseLicense,
  checkSseEntitlement,
  deactivateSseLicense,
  resetLocalSseLicense
} from './Services/licensing';

export function App() {
  const [conversations, setConversations] = useState<ChatConversation[]>(INITIAL_CONVERSATIONS);
  const [activeModelId, setActiveModelId] = useState<string>('bge-small-en-v15');
  const [activeDimension, setActiveDimension] = useState<number>(384);
  const [chunks, setChunks] = useState(() => buildVectorIndex(INITIAL_CONVERSATIONS, 384));
  const [activeTab, setActiveTab] = useState<AppTabType>('searchChat');
  const [selectedConvId, setSelectedConvId] = useState<string | null>(null);
  const [isDark, setIsDark] = useState(true);
  const [sseActive, setSseActive] = useState<boolean>(() => isSseActivated());
  const [showLicenseBox, setShowLicenseBox] = useState<boolean>(false);
  const [licenseInput, setLicenseInput] = useState<string>(() => sseLicenseKey());
  const [licenseStatus, setLicenseStatus] = useState<string>('');
  const [activating, setActivating] = useState<boolean>(false);

  useEffect(() => {
    checkSseEntitlement().then((ok) => setSseActive(ok));
  }, []);

  const handleActivateSse = async () => {
    setActivating(true);
    setLicenseStatus('Verifying SSE license key...');
    const res = await activateSseLicense(licenseInput);
    setActivating(false);
    setLicenseStatus(res.message);
    if (res.ok) {
      setSseActive(true);
    }
  };

  const handleDeactivateSse = async () => {
    const res = await deactivateSseLicense();
    setSseActive(false);
    setLicenseInput('');
    setLicenseStatus(res.message);
  };

  const handleResetLocalSse = () => {
    const res = resetLocalSseLicense();
    setSseActive(false);
    setLicenseStatus(res.message);
  };

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
    <div className="min-h-screen bg-[var(--tr-bg)] text-[var(--tr-text)] flex flex-col font-sans selection:bg-[var(--tr-accent)] selection:text-[var(--tr-on-amber)]">
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        indexedCount={chunks.length}
        totalConversations={conversations.length}
      />

      {/* Module License Bar & Collapsible Activation Box (mirrors app_ui.html #license-box) */}
      <div className="max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-4">
        <div className="flex items-center justify-end gap-3">
          <span
            className={`px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider border ${
              sseActive
                ? 'bg-[var(--tr-accent)]/15 text-[var(--tr-accent)] border-[var(--tr-accent)]/45'
                : 'bg-[var(--tr-panel)] text-[var(--tr-muted)] border-[var(--tr-border)]'
            }`}
          >
            {sseActive ? 'SSE Licensed' : 'SSE Unactivated'}
          </span>
          <button
            onClick={() => setShowLicenseBox(!showLicenseBox)}
            className="text-xs font-semibold text-[var(--tr-accent2)] hover:underline"
          >
            {sseActive ? 'Manage SSE License' : 'Activate SSE Key'}
          </button>
        </div>

        {showLicenseBox && (
          <div className="mt-3 rounded-2xl bg-[var(--tr-panel)] border border-[var(--tr-border)] p-5 space-y-3">
            <h2 className="text-sm font-bold text-[var(--tr-accent2)]">
              Unlock Smart Search Engine (SSE)
            </h2>
            <p className="text-xs text-[var(--tr-muted)] leading-relaxed">
              Paste the <code className="font-mono text-[var(--tr-text)]">SSE-XXXXXXXX-XXXX-XXXX</code> license key from your purchase email.
              Activating requires an internet connection once — after that, Smart Search Engine runs on your PC without an internet connection.
              (Note: Downloader Pro uses its own <code className="font-mono text-[var(--tr-text)]">PRO-XXXXXXXX-XXXX-XXXX</code> key.)
            </p>
            <div className="flex flex-wrap items-center gap-2.5">
              <input
                type="text"
                value={licenseInput}
                onChange={(e) => setLicenseInput(e.target.value)}
                placeholder="SSE-XXXXXXXX-XXXX-XXXX"
                className="flex-1 min-w-[240px] bg-[var(--tr-panel2)] border border-[var(--tr-border)] rounded-lg px-3.5 py-2 text-sm font-mono text-[var(--tr-text)] focus:outline-none focus:border-[var(--tr-accent)]"
              />
              <button
                disabled={activating}
                onClick={handleActivateSse}
                className="px-4 py-2 rounded-lg bg-[var(--tr-accent)] hover:bg-[var(--tr-accent2)] text-[var(--tr-on-amber)] font-semibold text-sm disabled:opacity-50"
              >
                {activating ? 'Activating…' : 'Activate SSE'}
              </button>
              <a
                href="https://totalrecalls.app/smart-search/#pricing"
                target="_blank"
                rel="noreferrer"
                className="px-4 py-2 rounded-lg bg-[var(--tr-panel2)] border border-[var(--tr-border)] text-[var(--tr-text)] font-semibold text-xs hover:border-[var(--tr-accent)]"
              >
                Buy SSE — $29
              </a>
              {sseActive && (
                <button
                  onClick={handleDeactivateSse}
                  className="px-3 py-2 rounded-lg border border-[var(--tr-border)] text-[var(--tr-muted)] text-xs hover:text-[var(--tr-text)]"
                >
                  Deactivate (free slot)
                </button>
              )}
              <button
                onClick={handleResetLocalSse}
                title="Dev helper: clear the SSE entitlement locally without contacting the server."
                className="px-3 py-2 rounded-lg bg-[var(--tr-panel2)] border border-[var(--tr-border)] text-[var(--tr-muted)] text-xs hover:text-[var(--tr-text)]"
              >
                Reset local state
              </button>
            </div>
            {licenseStatus && (
              <div className="text-xs text-[var(--tr-muted)] pt-1">{licenseStatus}</div>
            )}
          </div>
        )}
      </div>

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
            <span>Downside Protection Vault & Local Code Integrity Tests</span>
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
