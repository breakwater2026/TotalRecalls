import React, { useState } from 'react';
import { 
  Archive, 
  Download, 
  Terminal, 
  FileText, 
  CheckCircle2, 
  ShieldCheck, 
  Key, 
  FolderCheck, 
  FileCode, 
  HardDrive, 
  ArrowRight, 
  Copy, 
  Sparkles, 
  Layers, 
  ExternalLink, 
  RefreshCw,
  Cpu,
  Monitor,
  Printer,
  FileCheck
} from 'lucide-react';
import { downloadManualDocx, downloadManualMarkdown } from '../services/manualExporters';

interface DistributionFile {
  name: string;
  size: string;
  type: 'script' | 'executable' | 'doc' | 'source' | 'license' | 'config';
  description: string;
  recommendedRole: string;
}

const PACKAGE_CONTENTS: DistributionFile[] = [
  {
    name: 'install.bat',
    size: '4.2 KB',
    type: 'script',
    description: 'Windows 10/11 1-Click Installer (Auto-detects TotalRecalls Core directory, creates desktop shortcut, registers sqlite-vec engine)',
    recommendedRole: 'Windows Users'
  },
  {
    name: 'install.sh',
    size: '3.8 KB',
    type: 'script',
    description: 'macOS & Linux terminal installer with Gatekeeper/chmod bypass, symlinking to /usr/local/bin/totalrecalls-sse',
    recommendedRole: 'macOS / Linux Users'
  },
  {
    name: 'app/totalrecalls-sse.wasm.bin',
    size: '14.8 MB',
    type: 'executable',
    description: 'Pre-compiled self-contained WebAssembly vector runtime (HNSW + Reciprocal Rank Fusion) requiring zero Python or pip installs',
    recommendedRole: 'Zero-Dependency Binary'
  },
  {
    name: 'docs/TOTALRECALLS_POWER_USER_MANUAL.pdf',
    size: '840 KB',
    type: 'doc',
    description: 'Complete 30+ page Power User Manual covering RAG SQL schema, HNSW tuning, Ollama bridge, and PII regex engines',
    recommendedRole: 'Engineers / Architects'
  },
  {
    name: 'docs/TOTALRECALLS_USER_MANUAL_LAYMAN.pdf',
    size: '520 KB',
    type: 'doc',
    description: 'Plain-English everyday handbook with visual walkthroughs, conversational queries, and non-technical troubleshooting',
    recommendedRole: 'All Users / Laymen'
  },
  {
    name: 'docs/QUICKSTART_GUIDE_3_MINUTES.pdf',
    size: '280 KB',
    type: 'doc',
    description: '3-minute visual foldout: Drop Zip -> Click Activate -> Search 100,000+ AI messages offline immediately',
    recommendedRole: 'Quick Setup'
  },
  {
    name: 'docs/DEMO_VIDEO_SCRIPT_AND_TELEPROMPTER.md',
    size: '18 KB',
    type: 'doc',
    description: 'Full 2.5-minute video script with timed b-roll cues, voiceover lines, and key takeaway slides',
    recommendedRole: 'Marketing / Reviewers'
  },
  {
    name: 'src/ (Full TypeScript Source Code)',
    size: '1.2 MB',
    type: 'source',
    description: '100% unminified, air-gap auditable React 19 + TypeScript source tree with no obfuscation or phone-home telemetry',
    recommendedRole: 'Enterprise Audit / Devs'
  },
  {
    name: 'licenses/FOUNDERS_PASS_PERPETUAL.key',
    size: '1.1 KB',
    type: 'license',
    description: 'Cryptographically signed offline ECDSA perpetual license token unlocking all 6 drops with zero recurring subscriptions',
    recommendedRole: 'Commercial Entitlement'
  },
  {
    name: 'checksums.sha256',
    size: '2.4 KB',
    type: 'config',
    description: 'NIST-compliant SHA-256 signatures for every file in the archive to prove complete tamper-proofing and supply-chain integrity',
    recommendedRole: 'Security Verification'
  }
];

export const DeliveryPackagingStudio: React.FC = () => {
  const [activeInstallerTab, setActiveInstallerTab] = useState<'overview' | 'installer_sim' | 'pdf_center' | 'manifest'>('overview');
  const [simulatedInstallStep, setSimulatedInstallStep] = useState<number>(0);
  const [isInstalling, setIsInstalling] = useState<boolean>(false);
  const [copiedBash, setCopiedBash] = useState<boolean>(false);
  const [licenseKeyInput, setLicenseKeyInput] = useState<string>('TR-FOUNDER-PASS-8849-V25-AIRGAP');

  const handleStartSimulatedInstall = () => {
    setIsInstalling(true);
    setSimulatedInstallStep(1);
    setTimeout(() => setSimulatedInstallStep(2), 1200);
    setTimeout(() => setSimulatedInstallStep(3), 2400);
    setTimeout(() => setSimulatedInstallStep(4), 3600);
    setTimeout(() => {
      setSimulatedInstallStep(5);
      setIsInstalling(false);
    }, 4800);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedBash(true);
    setTimeout(() => setCopiedBash(false), 2000);
  };

  const handlePrintPDF = (type: 'power' | 'layman') => {
    window.print();
  };

  return (
    <div className="space-y-10">
      {/* Header Banner */}
      <div className="relative rounded-3xl bg-gradient-to-br from-[var(--tr-bg)] via-[var(--tr-panel2)] to-[var(--tr-bg)] border border-[var(--tr-accent)]/60 p-8 sm:p-10 shadow-2xl overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-[var(--tr-accent)]/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[var(--tr-accent)]/80 border border-[var(--tr-accent)]/60 text-[var(--tr-accent)] text-xs font-semibold mb-3">
              <Archive className="w-3.5 h-3.5" />
              <span>Commercial Distribution & Delivery Architecture</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-[var(--tr-text)] tracking-tight">
              Smart Search Engine <span className="bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] bg-clip-text text-transparent">Installer & Packaging Hub</span>
            </h1>
            <p className="mt-3 text-[var(--tr-muted)] text-sm sm:text-base leading-relaxed">
              Addressing the <strong className="text-[var(--tr-text)]">".zip delivery problem"</strong>: A dual-distribution pipeline delivering a 1-click zero-friction executable for laymen, full air-gap auditable TypeScript source for developers, and vector-grade PDF manuals bundled inside.
            </p>
          </div>

          <div className="flex flex-wrap lg:flex-col gap-3">
            <button 
              onClick={() => setActiveInstallerTab('installer_sim')}
              className="inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] hover:from-[var(--tr-accent)] hover:to-[var(--tr-accent2)] text-[var(--tr-text)] font-bold text-sm shadow-lg shadow transition-all hover:scale-[1.02]"
            >
              <Terminal className="w-4 h-4" />
              <span>Test 1-Click Installer</span>
            </button>
            <button 
              onClick={() => setActiveInstallerTab('pdf_center')}
              className="inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-[var(--tr-panel)] hover:bg-[var(--tr-panel2)] border border-[var(--tr-border)] text-[var(--tr-text)] font-semibold text-sm transition-all"
            >
              <Printer className="w-4 h-4 text-[var(--tr-accent)]" />
              <span>Export Vector PDFs</span>
            </button>
          </div>
        </div>

        {/* Navigation Sub-tabs */}
        <div className="flex items-center gap-2 mt-8 border-t border-[var(--tr-border)] pt-6 overflow-x-auto pb-1">
          <button
            onClick={() => setActiveInstallerTab('overview')}
            className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all whitespace-nowrap ${
              activeInstallerTab === 'overview'
                ? 'bg-[var(--tr-accent)]/10 text-[var(--tr-accent)] border border-[var(--tr-accent)]/30'
                : 'text-[var(--tr-muted)] hover:text-[var(--tr-text)] hover:bg-[var(--tr-panel)]/50'
            }`}
          >
            1. Strategy: The Frictionless Delivery Model
          </button>
          <button
            onClick={() => setActiveInstallerTab('installer_sim')}
            className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all whitespace-nowrap ${
              activeInstallerTab === 'installer_sim'
                ? 'bg-[var(--tr-accent)]/10 text-[var(--tr-accent)] border border-[var(--tr-accent)]/30'
                : 'text-[var(--tr-muted)] hover:text-[var(--tr-text)] hover:bg-[var(--tr-panel)]/50'
            }`}
          >
            2. Interactive Installer Simulation
          </button>
          <button
            onClick={() => setActiveInstallerTab('pdf_center')}
            className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all whitespace-nowrap ${
              activeInstallerTab === 'pdf_center'
                ? 'bg-[var(--tr-accent)]/10 text-[var(--tr-accent)] border border-[var(--tr-accent)]/30'
                : 'text-[var(--tr-muted)] hover:text-[var(--tr-text)] hover:bg-[var(--tr-panel)]/50'
            }`}
          >
            3. PDF Bundler & Export Center
          </button>
          <button
            onClick={() => setActiveInstallerTab('manifest')}
            className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all whitespace-nowrap ${
              activeInstallerTab === 'manifest'
                ? 'bg-[var(--tr-accent)]/10 text-[var(--tr-accent)] border border-[var(--tr-accent)]/30'
                : 'text-[var(--tr-muted)] hover:text-[var(--tr-text)] hover:bg-[var(--tr-panel)]/50'
            }`}
          >
            4. Complete .ZIP Archive Manifest
          </button>
        </div>
      </div>

      {/* Tab 1: Strategy & Delivery Architecture */}
      {activeInstallerTab === 'overview' && (
        <div className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-2xl p-6 relative overflow-hidden group hover:border-[var(--tr-accent)]/40 transition-colors">
              <div className="w-12 h-12 rounded-xl bg-[var(--tr-accent)]/80 border border-[var(--tr-accent)]/60 flex items-center justify-center text-[var(--tr-accent)] mb-4">
                <HardDrive className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-[var(--tr-text)] mb-2">1. In-App Core Drop (Zero Friction)</h3>
              <p className="text-[var(--tr-muted)] text-sm leading-relaxed mb-4">
                If the user already has the TotalRecalls Core Downloader, they don't even need terminal scripts. They simply drag-and-drop the <code className="text-[var(--tr-accent)] text-xs">TotalRecalls-SSE-v2.5.zip</code> file right onto the Core app window.
              </p>
              <div className="text-xs text-[var(--tr-accent)] font-medium flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-[var(--tr-accent)]" />
                Unpacks automatically into <code className="text-[var(--tr-muted)]">~/.totalrecalls/modules/</code>
              </div>
            </div>

            <div className="bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-2xl p-6 relative overflow-hidden group hover:border-[var(--tr-accent)]/40 transition-colors">
              <div className="w-12 h-12 rounded-xl bg-[var(--tr-accent)]/80 border border-[var(--tr-accent)]/60 flex items-center justify-center text-[var(--tr-accent)] mb-4">
                <Terminal className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-[var(--tr-text)] mb-2">2. Dual Self-Extracting Installers</h3>
              <p className="text-[var(--tr-muted)] text-sm leading-relaxed mb-4">
                The .zip includes double-clickable <strong className="text-[var(--tr-text)]">install.bat</strong> (Windows) and <strong className="text-[var(--tr-text)]">install.sh</strong> (macOS/Linux). These verify Node.js/WASM prerequisites, configure local SQLite vector tables, and set up desktop launcher icons.
              </p>
              <div className="text-xs text-[var(--tr-accent)] font-medium flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-[var(--tr-accent)]" />
                Auto-signs Gatekeeper & UAC permissions
              </div>
            </div>

            <div className="bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-2xl p-6 relative overflow-hidden group hover:border-amber-500/40 transition-colors">
              <div className="w-12 h-12 rounded-xl bg-amber-950/80 border border-amber-800/60 flex items-center justify-center text-amber-400 mb-4">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-[var(--tr-text)] mb-2">3. Unminified Source + Manuals</h3>
              <p className="text-[var(--tr-muted)] text-sm leading-relaxed mb-4">
                For enterprise defense, banking, and security auditors, the zip bundles the complete unminified TypeScript/React source code alongside high-fidelity PDF, DOCX, and Markdown manuals for total air-gapped compliance.
              </p>
              <div className="text-xs text-amber-400 font-medium flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-amber-400" />
                Zero external CDNs or analytics scripts
              </div>
            </div>
          </div>

          {/* Deep Strategic Architecture Card */}
          <div className="bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-3xl p-8 space-y-6">
            <h2 className="text-xl font-bold text-[var(--tr-text)] flex items-center gap-3">
              <Layers className="w-5 h-5 text-[var(--tr-accent)]" />
              Solving the "Source Code vs. Everyday User" Packaging Dilemma
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 text-sm">
              <div className="space-y-4">
                <h4 className="font-semibold text-rose-300 flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-rose-500" />
                  The Pitfall of Shipping Raw Source Code Alone
                </h4>
                <p className="text-[var(--tr-muted)] leading-relaxed">
                  Shipping only raw TypeScript/Node.js files in a zip guarantees a 40%+ customer support churn rate from non-technical buyers who encounter errors like <code className="text-rose-300 bg-rose-950/40 px-1 py-0.5 rounded">npm: command not found</code>, missing Python build chains, or Xcode CLT requirements.
                </p>
                <div className="bg-[var(--tr-bg)]/80 p-4 rounded-xl border border-[var(--tr-border)] text-[var(--tr-muted)] space-y-2">
                  <div className="text-[var(--tr-text)] font-medium">What everyday users say:</div>
                  <blockquote className="italic border-l-2 border-rose-500 pl-3">
                    "I bought this for $29, unzipped it, and saw a bunch of .ts files and a package.json. I don't know what a terminal is. How do I turn it on?"
                  </blockquote>
                </div>
              </div>

              <div className="space-y-4">
                <h4 className="font-semibold text-[var(--tr-accent)] flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-[var(--tr-accent)]" />
                  The Recommended Hybrid .ZIP Solution
                </h4>
                <p className="text-[var(--tr-muted)] leading-relaxed">
                  TotalRecalls packages the archive in three clear tiers that satisfy every customer persona simultaneously:
                </p>
                <ul className="space-y-2.5 text-[var(--tr-muted)]">
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-[var(--tr-accent)] mt-0.5 shrink-0" />
                    <span><strong className="text-[var(--tr-text)]">Tier A (Laymen):</strong> Double-click <code className="text-[var(--tr-accent)]">install.bat</code> / <code className="text-[var(--tr-accent)]">install.sh</code> or drop the zip onto TotalRecalls Core.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-[var(--tr-accent)] mt-0.5 shrink-0" />
                    <span><strong className="text-[var(--tr-text)]">Tier B (Self-Learners):</strong> Instant access to <code className="text-[var(--tr-accent)]">/docs/</code> containing pre-rendered PDF and Word manuals with visual diagrams.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-[var(--tr-accent)] mt-0.5 shrink-0" />
                    <span><strong className="text-[var(--tr-text)]">Tier C (Engineers & Auditors):</strong> Access to <code className="text-[var(--tr-accent)]">/src/</code> with full TypeScript definitions and zero obfuscation.</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Interactive Installer Simulation */}
      {activeInstallerTab === 'installer_sim' && (
        <div className="space-y-8">
          <div className="bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-3xl p-8 space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <h2 className="text-xl font-bold text-[var(--tr-text)] flex items-center gap-2">
                  <Terminal className="w-5 h-5 text-[var(--tr-accent)]" />
                  Smart Search Engine Zero-Friction Installer Simulation
                </h2>
                <p className="text-[var(--tr-muted)] text-sm mt-1">
                  Demonstrates the automated double-click onboarding experience that executes when the user runs the installer.
                </p>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-xs text-[var(--tr-muted)]">License Verification:</span>
                <span className="px-2.5 py-1 rounded bg-[var(--tr-accent)]/80 border border-[var(--tr-accent)]/80 text-[var(--tr-accent)] text-xs font-mono font-semibold">
                  OFFLINE VALID
                </span>
              </div>
            </div>

            {/* License Input Simulation */}
            <div className="bg-[var(--tr-bg)] border border-[var(--tr-border)] rounded-2xl p-5 flex flex-col sm:flex-row items-center gap-4">
              <div className="w-10 h-10 rounded-xl bg-[var(--tr-accent)]/80 border border-[var(--tr-accent)]/60 flex items-center justify-center text-[var(--tr-accent)] shrink-0">
                <Key className="w-5 h-5" />
              </div>
              <div className="flex-1 w-full">
                <label className="text-xs font-semibold text-[var(--tr-muted)] uppercase tracking-wider block mb-1">
                  Founder's Season Pass / Standalone Add-on Key
                </label>
                <input
                  type="text"
                  value={licenseKeyInput}
                  onChange={(e) => setLicenseKeyInput(e.target.value)}
                  className="w-full bg-[var(--tr-bg)] border border-[var(--tr-border)] rounded-xl px-4 py-2.5 text-sm font-mono text-[var(--tr-accent)] focus:outline-none focus:border-[var(--tr-accent)]"
                />
              </div>
              <button
                disabled={isInstalling}
                onClick={handleStartSimulatedInstall}
                className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] hover:from-[var(--tr-accent)] hover:to-[var(--tr-accent2)] text-[var(--tr-text)] font-bold text-sm shadow-lg shadow disabled:opacity-50 transition-all shrink-0"
              >
                {isInstalling ? 'Installing Add-on...' : simulatedInstallStep === 5 ? 'Re-run Installer' : 'Execute install.sh / .bat'}
              </button>
            </div>

            {/* Terminal Console Output */}
            <div className="bg-[var(--tr-bg)] border border-[var(--tr-border)] rounded-2xl p-6 font-mono text-xs sm:text-sm text-[var(--tr-muted)] space-y-3 shadow-inner">
              <div className="flex items-center justify-between pb-3 border-b border-[var(--tr-border)] text-[var(--tr-muted)]">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-rose-500/80" />
                  <div className="w-3 h-3 rounded-full bg-amber-500/80" />
                  <div className="w-3 h-3 rounded-full bg-[var(--tr-accent)]/80" />
                  <span className="ml-2 font-mono text-xs text-[var(--tr-muted)]">TotalRecalls SSE Installer v2.5.0</span>
                </div>
                <button
                  onClick={() => copyToClipboard(`curl -sSL https://totalrecalls.app/install-sse.sh | bash`)}
                  className="hover:text-[var(--tr-accent)] flex items-center gap-1 transition-colors"
                >
                  <Copy className="w-3.5 h-3.5" />
                  <span>{copiedBash ? 'Copied' : 'Copy Command'}</span>
                </button>
              </div>

              <div className="space-y-2 pt-2">
                <div className="text-[var(--tr-accent)] font-bold">
                  $ ./install.sh --license="{licenseKeyInput}"
                </div>

                {simulatedInstallStep >= 1 && (
                  <div className="text-[var(--tr-muted)] animate-fadeIn">
                    [1/5] Inspecting local host environment... <span className="text-[var(--tr-accent)] font-semibold">[PASS]</span>
                    <div className="text-[var(--tr-muted)] text-xs pl-4">Found existing TotalRecalls core data directory at ~/.totalrecalls/</div>
                  </div>
                )}

                {simulatedInstallStep >= 2 && (
                  <div className="text-[var(--tr-muted)] animate-fadeIn">
                    [2/5] Initializing local SQLite vector schema & WASM runtime... <span className="text-[var(--tr-accent)] font-semibold">[OK]</span>
                    <div className="text-[var(--tr-muted)] text-xs pl-4">Created table `chat_embeddings` (HNSW M=16, efSearch=64, 384/768-dim)</div>
                  </div>
                )}

                {simulatedInstallStep >= 3 && (
                  <div className="text-[var(--tr-muted)] animate-fadeIn">
                    [3/5] Bundling offline PDF documentation & quickstart manuals... <span className="text-[var(--tr-accent)] font-semibold">[DONE]</span>
                    <div className="text-[var(--tr-muted)] text-xs pl-4">Exported TOTALRECALLS_POWER_USER_MANUAL.pdf & USER_MANUAL_LAYMAN.pdf to ~/Documents/TotalRecalls/</div>
                  </div>
                )}

                {simulatedInstallStep >= 4 && (
                  <div className="text-[var(--tr-muted)] animate-fadeIn">
                    [4/5] Verifying air-gap cryptographic covenant & license hash... <span className="text-[var(--tr-accent)] font-semibold">[VERIFIED]</span>
                    <div className="text-[var(--tr-muted)] text-xs pl-4">Perpetual offline entitlement confirmed: All 6 Staged Drops unlocked. Zero network telemetry active.</div>
                  </div>
                )}

                {simulatedInstallStep >= 5 && (
                  <div className="text-[var(--tr-accent)] font-semibold bg-[var(--tr-accent)]/40 p-3 rounded-lg border border-[var(--tr-accent)]/60 mt-3 animate-fadeIn">
                    🎉 SUCCESS: TotalRecalls Smart Search Engine is fully installed and linked to your Core Downloader!
                    <div className="text-[var(--tr-muted)] font-normal text-xs mt-1">
                      You can now search, ask conversational questions, and run natural-language SQL across all your offline AI chats.
                    </div>
                  </div>
                )}

                {simulatedInstallStep === 0 && (
                  <div className="text-[var(--tr-muted)] italic">
                    Press "Execute install.sh / .bat" above to test the automated setup workflow...
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: PDF Bundler & Export Center */}
      {activeInstallerTab === 'pdf_center' && (
        <div className="space-y-8">
          <div className="bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-3xl p-8 space-y-6">
            <div>
              <h2 className="text-xl font-bold text-[var(--tr-text)] flex items-center gap-2">
                <Printer className="w-5 h-5 text-[var(--tr-accent)]" />
                Comprehensive Manuals: PDF, Word (.DOCX), and Markdown (.MD)
              </h2>
              <p className="text-[var(--tr-muted)] text-sm mt-1">
                Every customer gets both the <strong>Layman / Everyday Handbook</strong> and the <strong>Power User Technical Reference</strong> pre-packaged inside the <code className="text-[var(--tr-accent)] text-xs">/docs/</code> folder of their .zip.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Power User Manual Card */}
              <div className="bg-[var(--tr-bg)] border border-[var(--tr-border)] rounded-2xl p-6 flex flex-col justify-between hover:border-[var(--tr-accent)]/40 transition-colors">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="px-3 py-1 rounded-full bg-[var(--tr-accent)]/80 border border-[var(--tr-accent)]/60 text-[var(--tr-accent)] text-xs font-semibold">
                      For Developers & Architects
                    </span>
                    <span className="text-[var(--tr-muted)] text-xs font-mono">30+ Pages</span>
                  </div>

                  <div>
                    <h3 className="text-lg font-bold text-[var(--tr-text)]">Power User & Technical Specification Manual</h3>
                    <p className="text-[var(--tr-muted)] text-sm mt-1">
                      Covers SQLite vector schema, HNSW vs. IVFFlat indexing, RRF ranking mathematics, local Ollama embedding bridging, and regex-based PII scrubbing.
                    </p>
                  </div>

                  <div className="space-y-2 text-xs text-[var(--tr-muted)]">
                    <div className="flex items-center gap-2">
                      <FileCheck className="w-4 h-4 text-[var(--tr-accent)]" />
                      <span>Mathematical formulations for Cosine Distance & BM25</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <FileCheck className="w-4 h-4 text-[var(--tr-accent)]" />
                      <span>Direct natural language to SQL translation prompts</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <FileCheck className="w-4 h-4 text-[var(--tr-accent)]" />
                      <span>Automated LoRA & Alpaca fine-tuning dataset generation</span>
                    </div>
                  </div>
                </div>

                <div className="pt-6 border-t border-[var(--tr-border)] flex flex-wrap gap-2 mt-4">
                  <button
                    onClick={() => handlePrintPDF('power')}
                    className="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl bg-[var(--tr-accent)] hover:bg-[var(--tr-accent)] text-[var(--tr-text)] font-bold text-xs shadow-md transition-colors"
                  >
                    <Printer className="w-3.5 h-3.5" />
                    <span>Print / Save as PDF</span>
                  </button>
                  <button
                    onClick={downloadManualDocx}
                    className="inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl bg-[var(--tr-panel)] hover:bg-[var(--tr-panel2)] text-[var(--tr-text)] font-medium text-xs transition-colors"
                  >
                    <Download className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
                    <span>.DOCX</span>
                  </button>
                  <button
                    onClick={downloadManualMarkdown}
                    className="inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl bg-[var(--tr-panel)] hover:bg-[var(--tr-panel2)] text-[var(--tr-text)] font-medium text-xs transition-colors"
                  >
                    <Download className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
                    <span>.MD</span>
                  </button>
                </div>
              </div>

              {/* Layman Manual Card */}
              <div className="bg-[var(--tr-bg)] border border-[var(--tr-border)] rounded-2xl p-6 flex flex-col justify-between hover:border-[var(--tr-accent)]/40 transition-colors">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="px-3 py-1 rounded-full bg-[var(--tr-accent)]/80 border border-[var(--tr-accent)]/60 text-[var(--tr-accent)] text-xs font-semibold">
                      For Everyday Layman Users
                    </span>
                    <span className="text-[var(--tr-muted)] text-xs font-mono">15+ Pages</span>
                  </div>

                  <div>
                    <h3 className="text-lg font-bold text-[var(--tr-text)]">Everyday User Handbook (Plain English)</h3>
                    <p className="text-[var(--tr-muted)] text-sm mt-1">
                      No code, no terminal commands, no jargon. Explains how to search past ChatGPT & Claude chats, ask questions in your own words, and keep confidential info private.
                    </p>
                  </div>

                  <div className="space-y-2 text-xs text-[var(--tr-muted)]">
                    <div className="flex items-center gap-2">
                      <FileCheck className="w-4 h-4 text-[var(--tr-accent)]" />
                      <span>"How do I find that recipe or flight confirmation?"</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <FileCheck className="w-4 h-4 text-[var(--tr-accent)]" />
                      <span>Understanding the "Smart Search" vs "Word Search" difference</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <FileCheck className="w-4 h-4 text-[var(--tr-accent)]" />
                      <span>One-click automatic security redactor for credit cards & passwords</span>
                    </div>
                  </div>
                </div>

                <div className="pt-6 border-t border-[var(--tr-border)] flex flex-wrap gap-2 mt-4">
                  <button
                    onClick={() => handlePrintPDF('layman')}
                    className="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl bg-[var(--tr-accent)] hover:bg-[var(--tr-accent)] text-[var(--tr-text)] font-bold text-xs shadow-md transition-colors"
                  >
                    <Printer className="w-3.5 h-3.5" />
                    <span>Print / Save as PDF</span>
                  </button>
                  <button
                    onClick={downloadManualDocx}
                    className="inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl bg-[var(--tr-panel)] hover:bg-[var(--tr-panel2)] text-[var(--tr-text)] font-medium text-xs transition-colors"
                  >
                    <Download className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
                    <span>.DOCX</span>
                  </button>
                  <button
                    onClick={downloadManualMarkdown}
                    className="inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl bg-[var(--tr-panel)] hover:bg-[var(--tr-panel2)] text-[var(--tr-text)] font-medium text-xs transition-colors"
                  >
                    <Download className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
                    <span>.MD</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 4: Archive Manifest */}
      {activeInstallerTab === 'manifest' && (
        <div className="space-y-8">
          <div className="bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-3xl p-8 space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <h2 className="text-xl font-bold text-[var(--tr-text)] flex items-center gap-2">
                  <Archive className="w-5 h-5 text-[var(--tr-accent)]" />
                  Official Distribution Bundle: TotalRecalls-SSE-Suite-v2.5.0.zip
                </h2>
                <p className="text-[var(--tr-muted)] text-sm mt-1">
                  Total archive payload: <strong>18.4 MB</strong> (Self-contained, includes WebAssembly vector engine, dual installers, and all manuals).
                </p>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-xs text-[var(--tr-muted)] font-mono">SHA-256: 7f3a8b9e...01c4</span>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-[var(--tr-border)] text-xs font-semibold text-[var(--tr-muted)] uppercase tracking-wider">
                    <th className="pb-3 pl-2">File Path in .ZIP</th>
                    <th className="pb-3">Type</th>
                    <th className="pb-3">File Size</th>
                    <th className="pb-3">Purpose & Target Audience</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--tr-border)] font-sans">
                  {PACKAGE_CONTENTS.map((item, idx) => (
                    <tr key={idx} className="hover:bg-[var(--tr-panel)]/30 transition-colors">
                      <td className="py-3 pl-2 font-mono text-[var(--tr-accent)] font-medium flex items-center gap-2">
                        {item.type === 'script' && <Terminal className="w-4 h-4 text-[var(--tr-accent)] shrink-0" />}
                        {item.type === 'executable' && <Cpu className="w-4 h-4 text-[var(--tr-accent)] shrink-0" />}
                        {item.type === 'doc' && <FileText className="w-4 h-4 text-amber-400 shrink-0" />}
                        {item.type === 'source' && <FileCode className="w-4 h-4 text-indigo-400 shrink-0" />}
                        {item.type === 'license' && <Key className="w-4 h-4 text-[var(--tr-good)] shrink-0" />}
                        {item.type === 'config' && <ShieldCheck className="w-4 h-4 text-[var(--tr-muted)] shrink-0" />}
                        <span>{item.name}</span>
                      </td>
                      <td className="py-3 text-xs text-[var(--tr-muted)] capitalize">{item.type}</td>
                      <td className="py-3 text-xs font-mono text-[var(--tr-muted)]">{item.size}</td>
                      <td className="py-3 text-xs text-[var(--tr-muted)]">
                        <div>{item.description}</div>
                        <span className="inline-block mt-1 px-2 py-0.5 rounded bg-[var(--tr-panel)] text-[10px] text-[var(--tr-accent)] font-medium">
                          {item.recommendedRole}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
