import React, { useState, useEffect } from 'react';
import { 
  Play, 
  Pause, 
  RotateCcw, 
  Copy, 
  Check, 
  Download, 
  Tv, 
  Clock, 
  FileText, 
  Sparkles, 
  ArrowRight, 
  ChevronRight, 
  ChevronLeft,
  Volume2,
  Calendar,
  Tag
} from 'lucide-react';
import { AppTabType } from './Navbar';

interface DemoScriptProps {
  onSelectTab?: (tab: AppTabType) => void;
}

interface ScriptScene {
  id: string;
  timestamp: string;
  durationSec: number;
  actTitle: string;
  visualCue: string;
  audioVoiceover: string;
  onScreenText: string;
  highlightTab?: AppTabType;
}

export const DemoScript: React.FC<DemoScriptProps> = ({ onSelectTab }) => {
  const [activeSceneIdx, setActiveSceneIdx] = useState<number>(0);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [elapsedSec, setElapsedSec] = useState<number>(0);
  const [teleprompterFont, setTeleprompterFont] = useState<'normal' | 'large' | 'xlarge'>('large');
  const [copiedScript, setCopiedScript] = useState<boolean>(false);

  // 2-3 minute comprehensive demo video script
  const scenes: ScriptScene[] = [
    {
      id: 'scene-1',
      timestamp: '0:00 - 0:25',
      durationSec: 25,
      actTitle: 'Act 1: The Frustration — Where Did That AI Conversation Go?',
      visualCue: 'Host speaking directly to camera, splitscreen to 20 cluttered browser tabs: ChatGPT, Claude, Gemini, Perplexity. Frantic typing in search bars returning zero results.',
      audioVoiceover: `Be honest: how many times have you asked ChatGPT, Claude, or Gemini for a brilliant piece of code, a legal draft, or a business plan... only to lose it three weeks later in an endless list of unsearchable chat history?

Every day, our most valuable thoughts get trapped inside five different cloud platforms. And finding them again is like searching for a needle in a digital haystack.`,
      onScreenText: '5 Fragmented AI Platforms • Millions of Lost Tokens • Zero Universal Search',
      highlightTab: 'chatExplorer'
    },
    {
      id: 'scene-2',
      timestamp: '0:25 - 0:55',
      durationSec: 30,
      actTitle: 'Act 2: Enter TotalRecalls & The Smart Search Engine',
      visualCue: 'High-tech transition to TotalRecalls Desktop App. Instant sync of 5 providers into one unified local vault. Smooth UI, deep space void slate aesthetic with glowing cyan accents.',
      audioVoiceover: `Meet TotalRecalls—and our breakthrough Smart Search Engine add-on.

TotalRecalls automatically downloads and archives your complete chat history from ChatGPT, Claude, Gemini, Perplexity, and Mistral. 

But it doesn't just store them. The Smart Search Engine transforms your static archives into a living, lightning-fast private intelligence vault.`,
      onScreenText: 'TotalRecalls Smart Search Engine • Universal Local AI Vault',
      highlightTab: 'overview'
    },
    {
      id: 'scene-3',
      timestamp: '0:55 - 1:30',
      durationSec: 35,
      actTitle: 'Act 3: Semantic Vector Search & Natural Language to SQL',
      visualCue: 'Host types in search box: "How did we optimize our database indexing?" In 18 milliseconds, relevant chunks appear from both ChatGPT and Mistral discussing PostgreSQL pgvector and HNSW. Host toggles to SQL query view.',
      audioVoiceover: `Watch this: I'll search for 'database indexing speedups'. Notice I never said the word 'pgvector' or 'HNSW'. 

Because TotalRecalls searches by semantic meaning, not just exact keywords, it instantly pulls the exact technical advice given across different models.

Want metrics? Ask in plain English: 'Which AI do I talk to most?' TotalRecalls compiles and executes native SQLite queries on the fly—giving you instant data without writing a line of code.`,
      onScreenText: 'Sub-20ms Semantic Vector Search • Natural Language to SQL Engine',
      highlightTab: 'searchChat'
    },
    {
      id: 'scene-4',
      timestamp: '1:30 - 2:05',
      durationSec: 35,
      actTitle: 'Act 4: AI Peer Review (Consensus) & Secret Scrubber',
      visualCue: 'Transition to Consensus Matrix tab: Side-by-side comparison of ChatGPT vs Mistral. Shows Divergent Stance badge and recommended resolution. Transition to PII Scrubber: live redaction of sk_live_ Stripe API key into [REDACTED_API_KEY].',
      audioVoiceover: `TotalRecalls doesn't just search—it’s your personal AI Peer Review Board. With the built-in Consensus Auditor, you can compare what Claude, Gemini, and ChatGPT recommended on the same topic. It instantly flags where they agree, and where their advice clashes.

Need to share or train a local model? Our built-in PII Scrubber automatically wipes out API keys, private passwords, and customer emails with one click, letting you export sanitized training datasets in standard JSONL format.`,
      onScreenText: 'Cross-AI Peer Review • Automated PII & Secret Redaction',
      highlightTab: 'consensus'
    },
    {
      id: 'scene-5',
      timestamp: '2:05 - 2:30',
      durationSec: 25,
      actTitle: 'Act 5: Private on Your PC — Nothing Uploaded',
      visualCue: 'Host on camera holding laptop. Visual icon of Wi-Fi turning OFF (Airplane mode) after the one-time setup download, yet TotalRecalls continues searching locally with sub-millisecond response. Quick glimpse of the User Manuals (.PDF, .DOCX, .MD).',
      audioVoiceover: `TotalRecalls runs entirely on your PC. Nothing you write or save is uploaded — not a word, vector, or token leaves your machine. The only internet use is a one-time search-model download at setup; after that it works without a connection. Your conversations are yours. Forever.`,
      onScreenText: 'Runs on your PC — nothing uploaded',
      highlightTab: 'manual'
    },
    {
      id: 'scene-6',
      timestamp: '2:30 - 2:50',
      durationSec: 20,
      actTitle: 'Act 6: Call to Action — Pricing',
      visualCue: 'Commercial Pricing card animates in: TotalRecalls Pro $24 at launch, Smart Search Engine $29, Pro + SSE bundle $49.89. URL: https://totalrecalls.app prominently displayed with cyan glow. Music swells to crescendo.',
      audioVoiceover: `TotalRecalls Pro is $24 at launch. Add the Smart Search Engine for $29 — or get both for $49.89. Visit totalrecalls.app. Stop losing your best ideas. Visit totalrecalls.app.`,
      onScreenText: 'Pro $24 · SSE $29 · Bundle $49.89 • totalrecalls.app',
      highlightTab: 'specs'
    }
  ];

  const fullScriptMarkdown = scenes.map(s => `### [${s.timestamp}] ${s.actTitle}\n**Visual:** ${s.visualCue}\n**Voiceover:** ${s.audioVoiceover}\n**On-Screen Banner:** ${s.onScreenText}\n`).join('\n---\n\n');

  const handleCopyFullScript = () => {
    navigator.clipboard.writeText(fullScriptMarkdown);
    setCopiedScript(true);
    setTimeout(() => setCopiedScript(false), 2500);
  };

  const handleDownloadScript = () => {
    const blob = new Blob([fullScriptMarkdown], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'TOTALRECALLS_SMART_SEARCH_DEMO_SCRIPT.md';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const currentScene = scenes[activeSceneIdx];

  // Auto-play timer
  useEffect(() => {
    let timer: any = null;
    if (isPlaying) {
      timer = setInterval(() => {
        setElapsedSec((prev) => {
          if (prev >= 170) {
            setIsPlaying(false);
            return 0;
          }
          return prev + 1;
        });
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [isPlaying]);

  return (
    <div className="space-y-8">
      {/* Header Bar */}
      <div className="rounded-2xl bg-[var(--tr-panel)] border border-[var(--tr-accent)]/30 p-5 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[var(--tr-accent)] to-[var(--tr-accent2)] flex items-center justify-center text-[var(--tr-text)] font-bold shadow-md shadow">
            <Tv className="w-5 h-5 text-[var(--tr-text)]" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-base font-bold text-[var(--tr-text)] tracking-tight">Demo Video Script & Teleprompter</h2>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-[var(--tr-accent)]/15 text-[var(--tr-accent)] border border-[var(--tr-accent)]/30 font-mono">
                2 min 45 sec
              </span>
            </div>
            <p className="text-xs text-[var(--tr-muted)]">
              Commercial-grade 6-act promotional video script with a pricing call to action.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleCopyFullScript}
            className="px-3 py-1.5 rounded-lg bg-[var(--tr-panel2)] hover:bg-[var(--tr-panel)] text-[var(--tr-muted)] border border-[var(--tr-border)] text-xs font-semibold flex items-center gap-1.5 transition-colors"
          >
            {copiedScript ? <Check className="w-3.5 h-3.5 text-[var(--tr-accent)]" /> : <Copy className="w-3.5 h-3.5 text-[var(--tr-accent)]" />}
            <span>{copiedScript ? 'Copied Full Script!' : 'Copy Script (.MD)'}</span>
          </button>
          <button
            onClick={handleDownloadScript}
            className="px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] hover:from-[var(--tr-accent)] hover:to-[var(--tr-accent2)] text-[var(--tr-text)] text-xs font-bold flex items-center gap-1.5 transition-all shadow"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download .MD</span>
          </button>
        </div>
      </div>

      {/* Interactive Teleprompter & Scene Navigator */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Act Navigator */}
        <div className="space-y-2">
          <div className="text-xs font-bold text-[var(--tr-muted)] uppercase tracking-wider mb-2 flex items-center justify-between">
            <span>Video Scene Breakdown</span>
            <span className="font-mono text-[var(--tr-accent)]">6 Acts • 165s</span>
          </div>

          {scenes.map((scene, idx) => (
            <button
              key={scene.id}
              onClick={() => {
                setActiveSceneIdx(idx);
                setIsPlaying(false);
              }}
              className={`w-full text-left p-3.5 rounded-xl border transition-all flex items-start justify-between gap-3 ${
                activeSceneIdx === idx
                  ? 'bg-[var(--tr-accent)]/40 border-[var(--tr-accent)] shadow-md shadow'
                  : 'bg-[var(--tr-panel)] border-[var(--tr-border)] hover:border-[var(--tr-border)]'
              }`}
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${
                    activeSceneIdx === idx ? 'bg-[var(--tr-accent)] text-[var(--tr-on-amber)] font-bold' : 'bg-[var(--tr-panel)] text-[var(--tr-muted)]'
                  }`}>
                    {scene.timestamp}
                  </span>
                  <span className="text-[11px] font-medium text-[var(--tr-muted)]">
                    {scene.durationSec}s
                  </span>
                </div>
                <div className="text-xs font-bold text-[var(--tr-text)] line-clamp-1">{scene.actTitle}</div>
              </div>
              <ChevronRight className={`w-4 h-4 mt-1 transition-transform ${
                activeSceneIdx === idx ? 'text-[var(--tr-accent)] translate-x-1' : 'text-[var(--tr-muted)]'
              }`} />
            </button>
          ))}
        </div>

        {/* Right: Teleprompter View */}
        <div className="lg:col-span-2 space-y-4">
          <div className="rounded-2xl bg-[var(--tr-panel)] border border-[var(--tr-accent)]/30 p-6 space-y-6 shadow-xl">
            {/* Teleprompter Controls Header */}
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[var(--tr-border)] pb-4">
              <div className="space-y-0.5">
                <span className="text-[10px] font-mono font-bold text-[var(--tr-accent)] uppercase tracking-wider">
                  Active Scene {activeSceneIdx + 1} of {scenes.length}
                </span>
                <h3 className="text-base font-bold text-[var(--tr-text)]">{currentScene.actTitle}</h3>
              </div>

              {/* Font Sizer */}
              <div className="flex items-center space-x-1 bg-[var(--tr-panel2)] border border-[var(--tr-border)] rounded-lg p-1 text-xs">
                <button
                  onClick={() => setTeleprompterFont('normal')}
                  className={`px-2 py-1 rounded text-xs ${teleprompterFont === 'normal' ? 'bg-[var(--tr-panel2)] text-[var(--tr-text)] font-bold' : 'text-[var(--tr-muted)]'}`}
                >
                  A
                </button>
                <button
                  onClick={() => setTeleprompterFont('large')}
                  className={`px-2 py-1 rounded text-sm ${teleprompterFont === 'large' ? 'bg-[var(--tr-panel2)] text-[var(--tr-text)] font-bold' : 'text-[var(--tr-muted)]'}`}
                >
                  A+
                </button>
                <button
                  onClick={() => setTeleprompterFont('xlarge')}
                  className={`px-2 py-1 rounded text-base ${teleprompterFont === 'xlarge' ? 'bg-[var(--tr-panel2)] text-[var(--tr-text)] font-bold' : 'text-[var(--tr-muted)]'}`}
                >
                  A++
                </button>
              </div>
            </div>

            {/* Visual Cue Card */}
            <div className="p-3.5 rounded-xl bg-[var(--tr-accent)]/30 border border-[var(--tr-accent)]/30 space-y-1">
              <div className="flex items-center gap-1.5 text-[var(--tr-accent)] text-xs font-bold">
                <Tv className="w-3.5 h-3.5" />
                <span>Camera & Screen Visual Direction:</span>
              </div>
              <p className="text-xs text-[var(--tr-muted)] italic">{currentScene.visualCue}</p>
            </div>

            {/* Teleprompter Voiceover Text */}
            <div className="space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-bold text-[var(--tr-accent)] uppercase tracking-wider">
                <Volume2 className="w-3.5 h-3.5" />
                <span>Spoken Voiceover Script (Host Audio):</span>
              </div>
              <div className={`p-5 rounded-xl bg-[var(--tr-panel2)] border border-[var(--tr-border)] leading-relaxed text-[var(--tr-text)] font-sans tracking-wide select-all whitespace-pre-line ${
                teleprompterFont === 'normal' ? 'text-sm' :
                teleprompterFont === 'large' ? 'text-base sm:text-lg' : 'text-lg sm:text-xl'
              }`}>
                {currentScene.audioVoiceover}
              </div>
            </div>

            {/* On Screen Banner Graphic */}
            <div className="p-3 rounded-xl bg-[var(--tr-panel)] border border-[var(--tr-border)] flex items-center justify-between text-xs">
              <span className="text-[var(--tr-muted)] font-mono">Lower-Third On-Screen Graphic:</span>
              <span className="font-bold text-[var(--tr-accent)] font-mono">{currentScene.onScreenText}</span>
            </div>

            {/* Scene Navigation & Live Demo Link */}
            <div className="flex items-center justify-between pt-2 border-t border-[var(--tr-border)]">
              <button
                disabled={activeSceneIdx === 0}
                onClick={() => setActiveSceneIdx(prev => Math.max(0, prev - 1))}
                className="px-3 py-1.5 rounded-lg bg-[var(--tr-panel2)] hover:bg-[var(--tr-panel)] text-[var(--tr-muted)] disabled:opacity-30 text-xs font-semibold flex items-center gap-1"
              >
                <ChevronLeft className="w-3.5 h-3.5" />
                <span>Prev Act</span>
              </button>

              {currentScene.highlightTab && (
                <button
                  onClick={() => onSelectTab && onSelectTab(currentScene.highlightTab!)}
                  className="px-3.5 py-1.5 rounded-lg bg-[var(--tr-accent)]/15 hover:bg-[var(--tr-accent)]/25 text-[var(--tr-accent)] border border-[var(--tr-accent)]/40 text-xs font-bold flex items-center gap-1.5 transition-colors"
                >
                  <Sparkles className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
                  <span>Open Demo View for this Scene</span>
                </button>
              )}

              <button
                disabled={activeSceneIdx === scenes.length - 1}
                onClick={() => setActiveSceneIdx(prev => Math.min(scenes.length - 1, prev + 1))}
                className="px-3 py-1.5 rounded-lg bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] hover:from-[var(--tr-accent)] hover:to-[var(--tr-accent2)] text-[var(--tr-text)] disabled:opacity-30 text-xs font-bold flex items-center gap-1 shadow"
              >
                <span>Next Act</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
