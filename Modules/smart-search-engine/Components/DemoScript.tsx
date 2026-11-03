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

Need to share or train a local model? Our built-in Air-Gap PII Scrubber automatically wipes out API keys, private passwords, and customer emails with one click, letting you export sanitized training datasets in standard JSONL format.`,
      onScreenText: 'Cross-AI Peer Review • Automated PII & Secret Redaction',
      highlightTab: 'consensus'
    },
    {
      id: 'scene-5',
      timestamp: '2:05 - 2:30',
      durationSec: 25,
      actTitle: 'Act 5: The Air-Gap Guarantee — 100% Private & Offline',
      visualCue: 'Host on camera holding laptop. Visual icon of Wi-Fi turning OFF (Airplane mode), yet TotalRecalls continues searching locally with sub-millisecond response. Quick glimpse of the User Manuals (.PDF, .DOCX, .MD).',
      audioVoiceover: `Here's the best part: TotalRecalls is 100% private and air-gapped. Not a single word, vector, or token ever leaves your laptop.

It works completely offline—on an airplane, in a remote cabin, or in a secure enterprise environment. Your conversations are yours. Forever.`,
      onScreenText: 'Zero Cloud Data Egress • 100% Offline Vault',
      highlightTab: 'manual'
    },
    {
      id: 'scene-6',
      timestamp: '2:30 - 2:50',
      durationSec: 20,
      actTitle: 'Act 6: Call to Action — Founder\'s Season Pass & Weekly Drops',
      visualCue: 'Commercial Pricing card animates in: Core Downloader $29, Founder\'s Season Pass Launch Week Special $49 (down from $140 sum-of-parts value). Weekly drop calendar animates: Week 1 Live, Week 2 PII Scrubber, Week 3 Fine-Tuner, Week 4 Consensus, Week 5 Topic Graph, Week 6 Benchmark. URL: https://totalrecalls.app prominently displayed with cyan glow. Music swells to crescendo.',
      audioVoiceover: `We are rolling out the Smart Search Engine in 6 weekly feature drops. You can purchase each module individually—or grab the early-bird Founder's Season Pass for just $49 this week, saving 65% and unlocking every drop for life.

Stop losing your best ideas. Visit totalrecalls.app and claim your Founder's Pass today!`,
      onScreenText: 'Founder\'s Season Pass $49 (Launch Week Special) • totalrecalls.app',
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
      <div className="rounded-2xl bg-[#0c1424] border border-cyan-500/30 p-5 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-teal-500 flex items-center justify-center text-slate-950 font-bold shadow-md shadow-cyan-500/20">
            <Tv className="w-5 h-5 text-slate-950" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-base font-bold text-white tracking-tight">Demo Video Script & Teleprompter</h2>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 font-mono">
                2 min 45 sec
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Commercial-grade 6-act promotional video script with Founder's Season Pass call to action.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleCopyFullScript}
            className="px-3 py-1.5 rounded-lg bg-[#070b14] hover:bg-slate-800 text-slate-300 border border-slate-700 text-xs font-semibold flex items-center gap-1.5 transition-colors"
          >
            {copiedScript ? <Check className="w-3.5 h-3.5 text-teal-400" /> : <Copy className="w-3.5 h-3.5 text-cyan-400" />}
            <span>{copiedScript ? 'Copied Full Script!' : 'Copy Script (.MD)'}</span>
          </button>
          <button
            onClick={handleDownloadScript}
            className="px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-cyan-600 to-teal-600 hover:from-cyan-500 hover:to-teal-500 text-white text-xs font-bold flex items-center gap-1.5 transition-all shadow"
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
          <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center justify-between">
            <span>Video Scene Breakdown</span>
            <span className="font-mono text-cyan-400">6 Acts • 165s</span>
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
                  ? 'bg-cyan-950/40 border-cyan-500 shadow-md shadow-cyan-500/10'
                  : 'bg-[#0c1424] border-slate-800/80 hover:border-slate-700'
              }`}
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${
                    activeSceneIdx === idx ? 'bg-cyan-500 text-slate-950 font-bold' : 'bg-slate-800 text-slate-400'
                  }`}>
                    {scene.timestamp}
                  </span>
                  <span className="text-[11px] font-medium text-slate-300">
                    {scene.durationSec}s
                  </span>
                </div>
                <div className="text-xs font-bold text-slate-100 line-clamp-1">{scene.actTitle}</div>
              </div>
              <ChevronRight className={`w-4 h-4 mt-1 transition-transform ${
                activeSceneIdx === idx ? 'text-cyan-400 translate-x-1' : 'text-slate-600'
              }`} />
            </button>
          ))}
        </div>

        {/* Right: Teleprompter View */}
        <div className="lg:col-span-2 space-y-4">
          <div className="rounded-2xl bg-[#0c1424] border border-cyan-500/30 p-6 space-y-6 shadow-xl">
            {/* Teleprompter Controls Header */}
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
              <div className="space-y-0.5">
                <span className="text-[10px] font-mono font-bold text-cyan-400 uppercase tracking-wider">
                  Active Scene {activeSceneIdx + 1} of {scenes.length}
                </span>
                <h3 className="text-base font-bold text-white">{currentScene.actTitle}</h3>
              </div>

              {/* Font Sizer */}
              <div className="flex items-center space-x-1 bg-[#070b14] border border-slate-800 rounded-lg p-1 text-xs">
                <button
                  onClick={() => setTeleprompterFont('normal')}
                  className={`px-2 py-1 rounded text-xs ${teleprompterFont === 'normal' ? 'bg-slate-700 text-white font-bold' : 'text-slate-400'}`}
                >
                  A
                </button>
                <button
                  onClick={() => setTeleprompterFont('large')}
                  className={`px-2 py-1 rounded text-sm ${teleprompterFont === 'large' ? 'bg-slate-700 text-white font-bold' : 'text-slate-400'}`}
                >
                  A+
                </button>
                <button
                  onClick={() => setTeleprompterFont('xlarge')}
                  className={`px-2 py-1 rounded text-base ${teleprompterFont === 'xlarge' ? 'bg-slate-700 text-white font-bold' : 'text-slate-400'}`}
                >
                  A++
                </button>
              </div>
            </div>

            {/* Visual Cue Card */}
            <div className="p-3.5 rounded-xl bg-cyan-950/30 border border-cyan-500/30 space-y-1">
              <div className="flex items-center gap-1.5 text-cyan-400 text-xs font-bold">
                <Tv className="w-3.5 h-3.5" />
                <span>Camera & Screen Visual Direction:</span>
              </div>
              <p className="text-xs text-slate-300 italic">{currentScene.visualCue}</p>
            </div>

            {/* Teleprompter Voiceover Text */}
            <div className="space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-bold text-teal-400 uppercase tracking-wider">
                <Volume2 className="w-3.5 h-3.5" />
                <span>Spoken Voiceover Script (Host Audio):</span>
              </div>
              <div className={`p-5 rounded-xl bg-[#070b14] border border-slate-800 leading-relaxed text-slate-100 font-sans tracking-wide select-all whitespace-pre-line ${
                teleprompterFont === 'normal' ? 'text-sm' :
                teleprompterFont === 'large' ? 'text-base sm:text-lg' : 'text-lg sm:text-xl'
              }`}>
                {currentScene.audioVoiceover}
              </div>
            </div>

            {/* On Screen Banner Graphic */}
            <div className="p-3 rounded-xl bg-[#0e1626] border border-slate-800 flex items-center justify-between text-xs">
              <span className="text-slate-400 font-mono">Lower-Third On-Screen Graphic:</span>
              <span className="font-bold text-cyan-300 font-mono">{currentScene.onScreenText}</span>
            </div>

            {/* Scene Navigation & Live Demo Link */}
            <div className="flex items-center justify-between pt-2 border-t border-slate-800">
              <button
                disabled={activeSceneIdx === 0}
                onClick={() => setActiveSceneIdx(prev => Math.max(0, prev - 1))}
                className="px-3 py-1.5 rounded-lg bg-[#070b14] hover:bg-slate-800 text-slate-300 disabled:opacity-30 text-xs font-semibold flex items-center gap-1"
              >
                <ChevronLeft className="w-3.5 h-3.5" />
                <span>Prev Act</span>
              </button>

              {currentScene.highlightTab && (
                <button
                  onClick={() => onSelectTab && onSelectTab(currentScene.highlightTab!)}
                  className="px-3.5 py-1.5 rounded-lg bg-cyan-950/60 hover:bg-cyan-900/60 text-cyan-300 border border-cyan-500/40 text-xs font-bold flex items-center gap-1.5 transition-colors"
                >
                  <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Open Demo View for this Scene</span>
                </button>
              )}

              <button
                disabled={activeSceneIdx === scenes.length - 1}
                onClick={() => setActiveSceneIdx(prev => Math.min(scenes.length - 1, prev + 1))}
                className="px-3 py-1.5 rounded-lg bg-gradient-to-r from-cyan-600 to-teal-600 hover:from-cyan-500 hover:to-teal-500 text-white disabled:opacity-30 text-xs font-bold flex items-center gap-1 shadow"
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
