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
import { LibraryConnect } from './Components/LibraryConnect';
import {
  LibraryMeta,
  ScanResult,
  buildScan,
  readFilesFromInput,
  readFilesFromHandle,
  supportsDirectoryPicker,
  loadLibraryIndex,
  saveLibraryIndex,
  clearLibraryIndex
} from './Services/libraryLoader';
import {
  isSseActivated,
  sseLicenseKey,
  activateSseLicense,
  checkSseEntitlement,
  deactivateSseLicense
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

  /* ------------------------------------------------------------------ */
  /* Library connection                                                  */
  /* ------------------------------------------------------------------ */
  const [libMeta, setLibMeta] = useState<LibraryMeta | null>(null);
  const [libBusy, setLibBusy] = useState<string | null>(null);
  const [libError, setLibError] = useState<string | null>(null);

  // Swap the corpus in, then build vectors on the next tick so the header can
  // paint the new counts before the (blocking) embedding pass starts.
  const applyLibrary = (result: ScanResult) => {
    setConversations(result.conversations);
    setLibMeta(result.meta);
    setLibBusy(`Indexing ${result.meta.messageCount.toLocaleString()} messages…`);
    window.setTimeout(() => {
      setChunks(buildVectorIndex(result.conversations, activeDimension));
      setLibBusy(null);
    }, 16);
  };

  const ingestLibrary = async (files: FileList | File[], label: string) => {
    if (!sseActive) {
      setLibError('Activate your SSE license to index your own library.');
      setShowLicenseBox(true);
      return;
    }
    setLibError(null);
    setLibBusy('Reading library files…');
    try {
      const raw = await readFilesFromInput(files, (done, total) => {
        if (done % 25 === 0 || done === total) {
          setLibBusy(`Reading ${done.toLocaleString()} / ${total.toLocaleString()} files…`);
        }
      });
      if (raw.length === 0) {
        setLibBusy(null);
        setLibError('No conversation.json files in that folder. Pick the Library folder itself (the one containing the provider subfolders).');
        return;
      }
      const result = buildScan(raw, label);
      if (result.conversations.length === 0) {
        setLibBusy(null);
        setLibError('Files were found but no conversations could be parsed.');
        return;
      }
      applyLibrary(result);
      void saveLibraryIndex(result);
    } catch (e: any) {
      setLibBusy(null);
      setLibError(`Could not read that folder: ${e?.message || e}`);
    }
  };

  const handleLibraryFiles = (files: FileList) => {
    const first = files[0] as any;
    const rel: string = (first && first.webkitRelativePath) || '';
    const label = rel.split('/')[0] || 'Selected folder';
    void ingestLibrary(files, label);
  };

  const handleLibraryPicker = async () => {
    if (!sseActive) {
      setLibError('Activate your SSE license to index your own library.');
      setShowLicenseBox(true);
      return;
    }
    if (!supportsDirectoryPicker()) {
      setLibError('Folder-remembering mode needs the app served over http(s). Use "Connect Library folder…" instead.');
      return;
    }
    try {
      setLibError(null);
      setLibBusy('Waiting for folder access…');
      const handle = await (window as any).showDirectoryPicker({ mode: 'read' });
      setLibBusy('Reading library files…');
      const raw = await readFilesFromHandle(handle, (n) => setLibBusy(`Reading ${n.toLocaleString()} files…`));
      if (raw.length === 0) {
        setLibBusy(null);
        setLibError('No conversation.json files in that folder.');
        return;
      }
      const result = buildScan(raw, handle.name || 'Library');
      if (result.conversations.length === 0) {
        setLibBusy(null);
        setLibError('Files were found but no conversations could be parsed.');
        return;
      }
      applyLibrary(result);
      void saveLibraryIndex(result);
    } catch (e: any) {
      setLibBusy(null);
      if (e?.name !== 'AbortError') setLibError(`Could not read that folder: ${e?.message || e}`);
    }
  };

  const handleForgetLibrary = async () => {
    await clearLibraryIndex();
    setLibMeta(null);
    setLibError(null);
    setLibBusy(null);
    setConversations(INITIAL_CONVERSATIONS);
    setChunks(buildVectorIndex(INITIAL_CONVERSATIONS, activeDimension));
  };

  // A saved library is only usable while entitlement is valid: the licence is
  // the gate on the paid capability, so deactivating (or being revoked) drops
  // back to sample data without deleting the stored index.
  useEffect(() => {
    if (!sseActive) {
      setLibMeta(null);
      setLibBusy(null);
      setLibError(null);
      setConversations(INITIAL_CONVERSATIONS);
      setChunks(buildVectorIndex(INITIAL_CONVERSATIONS, activeDimension));
      return;
    }
    let cancelled = false;
    loadLibraryIndex().then((saved) => {
      if (cancelled || !saved || !saved.conversations.length) return;
      setConversations(saved.conversations);
      setLibMeta(saved.meta);
      window.setTimeout(() => setChunks(buildVectorIndex(saved.conversations, activeDimension)), 16);
    });
    return () => {
      cancelled = true;
    };
  }, [sseActive]);

  const handleActivateSse = async () => {
    setActivating(true);
    setLicenseStatus('Verifying SSE license key...');
    const res = await activateSseLicense(licenseInput);
    setActivating(false);
    setLicenseStatus(res.message);
    if (res.ok) {
      setSseActive(true);
      setShowLicenseBox(false);
      setLicenseStatus('');
    }
  };

  const handleDeactivateSse = async () => {
    const res = await deactivateSseLicense();
    setSseActive(false);
    setLicenseInput('');
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
              Until activated, only the five bundled sample conversations are searchable — connecting your own Library requires a licence.
              Activating needs an internet connection once; after that, Smart Search Engine runs on your PC without an internet connection.
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
            </div>
            {licenseStatus && (
              <div className="text-xs text-[var(--tr-muted)] pt-1">{licenseStatus}</div>
            )}
          </div>
        )}
      </div>

      <LibraryConnect
        meta={libMeta}
        busy={libBusy}
        error={libError}
        licensed={sseActive}
        onFiles={handleLibraryFiles}
        onConnectPicker={handleLibraryPicker}
        onForget={handleForgetLibrary}
        onRequestLicense={() => setShowLicenseBox(true)}
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
