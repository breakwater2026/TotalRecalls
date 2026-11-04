import React, { useState } from 'react';
import { 
  ShieldCheck, 
  FileCode2, 
  Download, 
  Check, 
  Sparkles, 
  Eye, 
  EyeOff, 
  Lock, 
  Database,
  Layers,
  ArrowRight
} from 'lucide-react';
import { ChatConversation } from '../types';
import { auditAndScrubPII, exportToOpenAIJSONL, exportToAlpacaJSON } from '../services/datasetExporters';

interface DatasetScrubberProps {
  conversations: ChatConversation[];
}

export const DatasetScrubber: React.FC<DatasetScrubberProps> = ({ conversations }) => {
  const [activeFormat, setActiveFormat] = useState<'openai' | 'alpaca'>('openai');
  const [enableScrubber, setEnableScrubber] = useState<boolean>(true);
  const [showPreview, setShowPreview] = useState<boolean>(true);
  const [copiedNotice, setCopiedNotice] = useState<string | null>(null);

  // Compute scrub results
  const auditResult = auditAndScrubPII(conversations);
  const targetDataset = enableScrubber ? auditResult.scrubbedConversations : conversations;

  const datasetText = activeFormat === 'openai' 
    ? exportToOpenAIJSONL(targetDataset)
    : exportToAlpacaJSON(targetDataset);

  const handleCopy = () => {
    navigator.clipboard.writeText(datasetText);
    setCopiedNotice('Copied dataset to clipboard!');
    setTimeout(() => setCopiedNotice(null), 2500);
  };

  const handleDownload = () => {
    const filename = activeFormat === 'openai' ? 'totalrecalls_fine_tuning.jsonl' : 'totalrecalls_alpaca.json';
    const mime = activeFormat === 'openai' ? 'application/x-jsonlines' : 'application/json';
    const blob = new Blob([datasetText], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    setCopiedNotice(`Downloaded ${filename} successfully!`);
    setTimeout(() => setCopiedNotice(null), 2500);
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[var(--tr-bg)] via-[var(--tr-panel2)] to-[var(--tr-bg)] border border-[var(--tr-accent)]/30 p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5 max-w-2xl">
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[var(--tr-accent)]/15 text-[var(--tr-accent)] border border-[var(--tr-accent)]/40 flex items-center gap-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
                Market-Leader Feature: PII Scrubber & Fine-Tuning Pipeline
              </span>
              <span className="text-xs text-[var(--tr-muted)] font-mono">Air-Gapped Data Sanitization</span>
            </div>
            <h2 className="text-2xl font-bold text-[var(--tr-text)] tracking-tight">
              PII Air-Gap Scrubber & Dataset Exporter
            </h2>
            <p className="text-sm text-[var(--tr-muted)] leading-relaxed">
              Export your local AI chat archives into ready-to-train datasets for local Ollama, vLLM, or cloud models. Automatically detects and redacts API keys, secret credentials, internal IP addresses, and emails before export.
            </p>
          </div>

          <div className="flex items-center gap-4 bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-xl p-3 px-4">
            <div>
              <div className="text-xs text-[var(--tr-muted)]">Redacted Secrets</div>
              <div className="text-xl font-bold font-mono text-[var(--tr-accent)]">{auditResult.totalRedactions} Items</div>
            </div>
            <div className="h-8 w-px bg-[var(--tr-panel)]"></div>
            <div>
              <div className="text-xs text-[var(--tr-muted)]">Sanitization</div>
              <div className="text-sm font-semibold text-[var(--tr-accent)] flex items-center gap-1">
                <Lock className="w-3.5 h-3.5" />
                Active Local Guard
              </div>
            </div>
          </div>
        </div>
      </div>

      {copiedNotice && (
        <div className="p-3 bg-[var(--tr-accent)]/60 border border-[var(--tr-accent)]/40 rounded-xl text-[var(--tr-accent)] text-xs flex items-center gap-2 animate-fadeIn">
          <Check className="w-4 h-4 text-[var(--tr-accent)]" />
          <span>{copiedNotice}</span>
        </div>
      )}

      {/* Scrubber Diagnostics & Redaction Audit */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-xl bg-[var(--tr-panel)] border border-[var(--tr-border)] space-y-2">
          <div className="flex items-center justify-between text-xs text-[var(--tr-muted)]">
            <span className="font-semibold text-[var(--tr-muted)]">Air-Gap Redaction Engine</span>
            <input
              type="checkbox"
              checked={enableScrubber}
              onChange={(e) => setEnableScrubber(e.target.checked)}
              className=" cursor-pointer w-4 h-4"
            />
          </div>
          <p className="text-xs text-[var(--tr-muted)] leading-relaxed">
            {enableScrubber 
              ? 'Active: Replaces all detected credentials, emails, and IPs with safe anonymization tokens.'
              : 'Disabled: Export raw original text (WARNING: May contain internal API keys).'}
          </p>
        </div>

        <div className="p-4 rounded-xl bg-[var(--tr-panel)] border border-[var(--tr-border)] space-y-2">
          <div className="text-xs font-semibold text-[var(--tr-muted)]">Detected Secret Patterns</div>
          <div className="flex flex-wrap gap-1.5 text-[11px]">
            {auditResult.matchesFound.map((m, i) => (
              <span key={i} className="px-2 py-0.5 rounded bg-[var(--tr-panel2)] border border-[var(--tr-border)] text-[var(--tr-accent)] font-mono">
                {m.type} ({m.count})
              </span>
            ))}
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[var(--tr-panel)] border border-[var(--tr-border)] space-y-2">
          <div className="text-xs font-semibold text-[var(--tr-muted)]">Target Training Frameworks</div>
          <div className="text-xs text-[var(--tr-muted)]">
            Export directly to Ollama Modelfiles, Llama-Factory, HuggingFace TRL, or OpenAI fine-tuning endpoints.
          </div>
        </div>
      </div>

      {/* Dataset Generation Studio */}
      <div className="bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-2xl p-6 space-y-4 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[var(--tr-border)]">
          <div className="flex items-center space-x-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-[var(--tr-muted)]">Format:</span>
            <div className="flex bg-[var(--tr-panel2)] border border-[var(--tr-border)] rounded-lg p-1 text-xs">
              <button
                onClick={() => setActiveFormat('openai')}
                className={`px-3 py-1 rounded font-semibold transition-all ${
                  activeFormat === 'openai'
                    ? 'bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] text-[var(--tr-text)]'
                    : 'text-[var(--tr-muted)] hover:text-[var(--tr-text)]'
                }`}
              >
                OpenAI JSONL (`messages` array)
              </button>
              <button
                onClick={() => setActiveFormat('alpaca')}
                className={`px-3 py-1 rounded font-semibold transition-all ${
                  activeFormat === 'alpaca'
                    ? 'bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] text-[var(--tr-text)]'
                    : 'text-[var(--tr-muted)] hover:text-[var(--tr-text)]'
                }`}
              >
                Alpaca / ShareGPT (`instruction/output`)
              </button>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="px-3.5 py-1.5 bg-[var(--tr-panel2)] hover:bg-[var(--tr-panel)] text-[var(--tr-text)] border border-[var(--tr-border)] rounded-xl text-xs font-medium transition-colors flex items-center gap-1.5"
            >
              <span>Copy Dataset</span>
            </button>
            <button
              onClick={handleDownload}
              className="px-4 py-1.5 bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] hover:from-[var(--tr-accent)] hover:to-[var(--tr-accent2)] text-[var(--tr-text)] rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 shadow-md shadow"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Download Dataset</span>
            </button>
          </div>
        </div>

        {/* Code Preview Box */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs text-[var(--tr-muted)]">
            <span className="font-mono">
              Dataset Preview ({datasetText.split('\n').length} lines • {targetDataset.length} conversations)
            </span>
            <span className="text-[var(--tr-accent)] font-mono">
              {enableScrubber ? '✓ PII Redacted' : '⚠ Raw Unmasked'}
            </span>
          </div>

          <pre className="p-4 bg-[var(--tr-panel2)] border border-[var(--tr-border)]/90 rounded-xl text-[var(--tr-accent)] font-mono text-xs overflow-x-auto max-h-[360px] leading-relaxed shadow-inner">
            {datasetText}
          </pre>
        </div>
      </div>
    </div>
  );
};
