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
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#0c1f30] via-[#091524] to-[#070c16] border border-cyan-500/30 p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5 max-w-2xl">
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-teal-500/15 text-teal-300 border border-teal-500/40 flex items-center gap-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-teal-400" />
                Market-Leader Feature: PII Scrubber & Fine-Tuning Pipeline
              </span>
              <span className="text-xs text-slate-400 font-mono">Air-Gapped Data Sanitization</span>
            </div>
            <h2 className="text-2xl font-bold text-white tracking-tight">
              PII Air-Gap Scrubber & Dataset Exporter
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed">
              Export your local AI chat archives into ready-to-train datasets for local Ollama, vLLM, or cloud models. Automatically detects and redacts API keys, secret credentials, internal IP addresses, and emails before export.
            </p>
          </div>

          <div className="flex items-center gap-4 bg-[#080d19] border border-slate-800 rounded-xl p-3 px-4">
            <div>
              <div className="text-xs text-slate-400">Redacted Secrets</div>
              <div className="text-xl font-bold font-mono text-teal-400">{auditResult.totalRedactions} Items</div>
            </div>
            <div className="h-8 w-px bg-slate-800"></div>
            <div>
              <div className="text-xs text-slate-400">Sanitization</div>
              <div className="text-sm font-semibold text-cyan-400 flex items-center gap-1">
                <Lock className="w-3.5 h-3.5" />
                Active Local Guard
              </div>
            </div>
          </div>
        </div>
      </div>

      {copiedNotice && (
        <div className="p-3 bg-teal-950/60 border border-teal-500/40 rounded-xl text-teal-300 text-xs flex items-center gap-2 animate-fadeIn">
          <Check className="w-4 h-4 text-teal-400" />
          <span>{copiedNotice}</span>
        </div>
      )}

      {/* Scrubber Diagnostics & Redaction Audit */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-xl bg-[#0c1424] border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="font-semibold text-slate-300">Air-Gap Redaction Engine</span>
            <input
              type="checkbox"
              checked={enableScrubber}
              onChange={(e) => setEnableScrubber(e.target.checked)}
              className="accent-cyan-500 cursor-pointer w-4 h-4"
            />
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            {enableScrubber 
              ? 'Active: Replaces all detected credentials, emails, and IPs with safe anonymization tokens.'
              : 'Disabled: Export raw original text (WARNING: May contain internal API keys).'}
          </p>
        </div>

        <div className="p-4 rounded-xl bg-[#0c1424] border border-slate-800 space-y-2">
          <div className="text-xs font-semibold text-slate-300">Detected Secret Patterns</div>
          <div className="flex flex-wrap gap-1.5 text-[11px]">
            {auditResult.matchesFound.map((m, i) => (
              <span key={i} className="px-2 py-0.5 rounded bg-[#070b14] border border-slate-700 text-cyan-300 font-mono">
                {m.type} ({m.count})
              </span>
            ))}
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#0c1424] border border-slate-800 space-y-2">
          <div className="text-xs font-semibold text-slate-300">Target Training Frameworks</div>
          <div className="text-xs text-slate-400">
            Export directly to Ollama Modelfiles, Llama-Factory, HuggingFace TRL, or OpenAI fine-tuning endpoints.
          </div>
        </div>
      </div>

      {/* Dataset Generation Studio */}
      <div className="bg-[#0c1424] border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800">
          <div className="flex items-center space-x-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Format:</span>
            <div className="flex bg-[#070b14] border border-slate-800 rounded-lg p-1 text-xs">
              <button
                onClick={() => setActiveFormat('openai')}
                className={`px-3 py-1 rounded font-semibold transition-all ${
                  activeFormat === 'openai'
                    ? 'bg-gradient-to-r from-cyan-600 to-teal-600 text-white'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                OpenAI JSONL (`messages` array)
              </button>
              <button
                onClick={() => setActiveFormat('alpaca')}
                className={`px-3 py-1 rounded font-semibold transition-all ${
                  activeFormat === 'alpaca'
                    ? 'bg-gradient-to-r from-cyan-600 to-teal-600 text-white'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                Alpaca / ShareGPT (`instruction/output`)
              </button>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="px-3.5 py-1.5 bg-[#070b14] hover:bg-slate-800 text-slate-200 border border-slate-700 rounded-xl text-xs font-medium transition-colors flex items-center gap-1.5"
            >
              <span>Copy Dataset</span>
            </button>
            <button
              onClick={handleDownload}
              className="px-4 py-1.5 bg-gradient-to-r from-cyan-600 to-teal-600 hover:from-cyan-500 hover:to-teal-500 text-white rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 shadow-md shadow-cyan-600/20"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Download Dataset</span>
            </button>
          </div>
        </div>

        {/* Code Preview Box */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="font-mono">
              Dataset Preview ({datasetText.split('\n').length} lines • {targetDataset.length} conversations)
            </span>
            <span className="text-teal-400 font-mono">
              {enableScrubber ? '✓ PII Redacted' : '⚠ Raw Unmasked'}
            </span>
          </div>

          <pre className="p-4 bg-[#070b14] border border-slate-800/90 rounded-xl text-cyan-300 font-mono text-xs overflow-x-auto max-h-[360px] leading-relaxed shadow-inner">
            {datasetText}
          </pre>
        </div>
      </div>
    </div>
  );
};
