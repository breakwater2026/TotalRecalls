import React, { useState } from 'react';
import { 
  Cpu, 
  Sparkles, 
  Zap, 
  Layers, 
  HardDrive, 
  BarChart2, 
  CheckCircle2, 
  ArrowRight,
  RefreshCw,
  SlidersHorizontal,
  Info
} from 'lucide-react';
import { EMBEDDING_PROFILES } from '../constants';
import { EmbeddingEngineProfile, ChunkEmbedding } from '../types';

interface EmbeddingBenchmarkProps {
  currentModelId: string;
  onSelectModel: (modelId: string, dimension: number) => void;
  chunksCount: number;
}

export const EmbeddingBenchmark: React.FC<EmbeddingBenchmarkProps> = ({
  currentModelId,
  onSelectModel,
  chunksCount
}) => {
  const [selectedProfileId, setSelectedProfileId] = useState<string>(currentModelId);
  const [targetCorpusSize, setTargetCorpusSize] = useState<number>(chunksCount > 0 ? chunksCount : 500);
  const [isReindexing, setIsReindexing] = useState<boolean>(false);
  const [benchmarkResult, setBenchmarkResult] = useState<{
    profile: EmbeddingEngineProfile;
    estimatedRAMMB: number;
    estimatedLatencyMs: number;
    throughputTokensSec: number;
    indexDiskSizeMB: number;
  } | null>(() => {
    const profile = EMBEDDING_PROFILES.find(p => p.id === currentModelId) || EMBEDDING_PROFILES[0];
    const estimatedRAMMB = Math.round((profile.ramUsageMBPer100k / 100000) * targetCorpusSize * 10) / 10;
    const indexDiskSizeMB = Math.round(((profile.dimension * 4 * targetCorpusSize) / (1024 * 1024)) * 100) / 100;
    const throughput = Math.round(1000 / (profile.latencyPer1kTokensMs / 1000));
    return {
      profile,
      estimatedRAMMB: Math.max(0.5, estimatedRAMMB),
      estimatedLatencyMs: profile.latencyPer1kTokensMs,
      throughputTokensSec: throughput,
      indexDiskSizeMB: Math.max(0.1, indexDiskSizeMB)
    };
  });

  const activeProfile = EMBEDDING_PROFILES.find(p => p.id === selectedProfileId) || EMBEDDING_PROFILES[0];

  const handleSimulateBenchmark = (profile: EmbeddingEngineProfile) => {
    setSelectedProfileId(profile.id);
    setIsReindexing(true);

    setTimeout(() => {
      const estimatedRAMMB = Math.round((profile.ramUsageMBPer100k / 100000) * targetCorpusSize * 10) / 10;
      const indexDiskSizeMB = Math.round(((profile.dimension * 4 * targetCorpusSize) / (1024 * 1024)) * 100) / 100;
      const throughput = Math.round(1000 / (profile.latencyPer1kTokensMs / 1000));
      
      setBenchmarkResult({
        profile,
        estimatedRAMMB: Math.max(0.5, estimatedRAMMB),
        estimatedLatencyMs: profile.latencyPer1kTokensMs,
        throughputTokensSec: throughput,
        indexDiskSizeMB: Math.max(0.1, indexDiskSizeMB)
      });
      setIsReindexing(false);
      onSelectModel(profile.id, profile.dimension);
    }, 350);
  };

  // Mock 2D projection scatter points for dimension visualizer
  const clusterPoints = [
    { x: 22, y: 35, category: 'DevOps / Docker', provider: 'Gemini', label: 'Docker Ollama CUDA' },
    { x: 28, y: 40, category: 'DevOps / Docker', provider: 'Gemini', label: 'nomic-embed-text' },
    { x: 68, y: 25, category: 'Database & Vectors', provider: 'ChatGPT', label: 'pgvector HNSW table' },
    { x: 74, y: 32, category: 'Database & Vectors', provider: 'Mistral', label: 'Embedded SQLite ADR' },
    { x: 71, y: 20, category: 'Database & Vectors', provider: 'ChatGPT', label: 'Inner product SIMD' },
    { x: 45, y: 75, category: 'Payments & Legal', provider: 'Claude', label: '30-day Stripe refund' },
    { x: 50, y: 80, category: 'Payments & Legal', provider: 'Claude', label: 'Webhook idempotency' },
    { x: 85, y: 70, category: 'Growth & Metrics', provider: 'Perplexity', label: 'Q3 download metrics' }
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#0c1f30] via-[#091524] to-[#070c16] border border-cyan-500/30 p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5 max-w-2xl">
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 flex items-center gap-1.5">
                <Cpu className="w-3.5 h-3.5 text-cyan-400" />
                TotalRecalls Market-Leader Enhancement #2
              </span>
              <span className="text-xs text-slate-400 font-mono">Local Dimension & RAM Profiler</span>
            </div>
            <h2 className="text-2xl font-bold text-white tracking-tight">
              Embedding Model Benchmark & Dimension Visualizer
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed">
              Test and compare vector embedding engines on the fly. Benchmark memory footprint, latency, and index sizes between 384-dimensional ultra-fast local models and 768-dimensional deep semantic architectures.
            </p>
          </div>

          <div className="flex items-center gap-4 bg-[#080d19] border border-slate-800 rounded-xl p-3 px-4">
            <div>
              <div className="text-xs text-slate-400">Current Vector Dim</div>
              <div className="text-xl font-bold font-mono text-cyan-400">{activeProfile.dimension}-D</div>
            </div>
            <div className="h-8 w-px bg-slate-800"></div>
            <div>
              <div className="text-xs text-slate-400">Active Engine</div>
              <div className="text-sm font-semibold text-teal-400 font-mono">{activeProfile.name.split(' ')[0]}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Model Selection Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {EMBEDDING_PROFILES.map((profile) => {
          const isSelected = profile.id === selectedProfileId;
          return (
            <div
              key={profile.id}
              onClick={() => handleSimulateBenchmark(profile)}
              className={`p-4 rounded-xl cursor-pointer transition-all border flex flex-col justify-between space-y-3 ${
                isSelected
                  ? 'bg-cyan-950/40 border-cyan-500/80 shadow-lg shadow-cyan-950/30'
                  : 'bg-[#0c1424] border-slate-800 hover:border-slate-700 hover:bg-[#0f1a2e]'
              }`}
            >
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-[#070b14] text-cyan-300 border border-slate-800">
                    {profile.dimension}-dim ({profile.quantization})
                  </span>
                  {isSelected && (
                    <span className="text-[10px] text-teal-400 font-semibold flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" />
                      Active
                    </span>
                  )}
                </div>

                <h4 className="text-xs font-bold text-white line-clamp-1">
                  {profile.name}
                </h4>

                <p className="text-[11px] text-slate-400 line-clamp-2">
                  {profile.description}
                </p>
              </div>

              <div className="pt-2 border-t border-slate-800/80 text-[11px] font-mono space-y-1 text-slate-400">
                <div className="flex justify-between">
                  <span>Latency:</span>
                  <span className="text-cyan-400">{profile.latencyPer1kTokensMs} ms/1k</span>
                </div>
                <div className="flex justify-between">
                  <span>RAM per 100k:</span>
                  <span className="text-teal-400">{profile.ramUsageMBPer100k} MB</span>
                </div>
                <div className="flex justify-between">
                  <span>Runtime:</span>
                  <span className="text-slate-300">{profile.provider}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Main 2-column: Benchmark Metrics & 2D PCA Cluster Visualizer */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Benchmark Profiler */}
        <div className="lg:col-span-5 bg-[#0c1424] border border-slate-800 rounded-2xl p-5 space-y-4 shadow-lg flex flex-col justify-between">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <BarChart2 className="w-4 h-4 text-cyan-400" />
                Live Engine Performance Profiler
              </h3>
              {isReindexing && (
                <span className="text-xs text-cyan-400 flex items-center gap-1 font-mono">
                  <RefreshCw className="w-3 h-3 animate-spin" />
                  Re-indexing...
                </span>
              )}
            </div>

            {/* Simulated Corpus slider */}
            <div className="p-3 rounded-xl bg-[#070b14] border border-slate-800 space-y-2">
              <div className="flex items-center justify-between text-xs text-slate-300">
                <span>Simulate Total Vault Size:</span>
                <span className="font-mono text-cyan-400 font-bold">{targetCorpusSize.toLocaleString()} Chunks</span>
              </div>
              <input
                type="range"
                min="100"
                max="50000"
                step="500"
                value={targetCorpusSize}
                onChange={(e) => {
                  const val = parseInt(e.target.value);
                  setTargetCorpusSize(val);
                  handleSimulateBenchmark(activeProfile);
                }}
                className="w-full accent-cyan-500 cursor-pointer"
              />
            </div>

            {/* KPI Cards */}
            {benchmarkResult && (
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="p-3 rounded-xl bg-[#070b14] border border-slate-800 space-y-1">
                  <div className="text-slate-400 text-[11px]">Est. RAM Overhead</div>
                  <div className="text-lg font-bold font-mono text-cyan-300">
                    {benchmarkResult.estimatedRAMMB} MB
                  </div>
                  <div className="text-[10px] text-slate-500">Zero cloud egress</div>
                </div>

                <div className="p-3 rounded-xl bg-[#070b14] border border-slate-800 space-y-1">
                  <div className="text-slate-400 text-[11px]">Query Latency</div>
                  <div className="text-lg font-bold font-mono text-teal-300">
                    {benchmarkResult.estimatedLatencyMs} ms
                  </div>
                  <div className="text-[10px] text-slate-500">Local SIMD dot product</div>
                </div>

                <div className="p-3 rounded-xl bg-[#070b14] border border-slate-800 space-y-1">
                  <div className="text-slate-400 text-[11px]">Throughput</div>
                  <div className="text-lg font-bold font-mono text-amber-300">
                    {benchmarkResult.throughputTokensSec.toLocaleString()} tok/s
                  </div>
                  <div className="text-[10px] text-slate-500">M-Series / RTX GPU</div>
                </div>

                <div className="p-3 rounded-xl bg-[#070b14] border border-slate-800 space-y-1">
                  <div className="text-slate-400 text-[11px]">Index Size on Disk</div>
                  <div className="text-lg font-bold font-mono text-sky-300">
                    {benchmarkResult.indexDiskSizeMB} MB
                  </div>
                  <div className="text-[10px] text-slate-500">SQLite sqlite-vec file</div>
                </div>
              </div>
            )}
          </div>

          <div className="p-3 rounded-xl bg-cyan-950/30 border border-cyan-500/30 text-xs text-slate-300 flex items-start gap-2">
            <Info className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
            <span>
              TotalRecalls automatically normalizes vectors to unit length so that cosine similarity reduces to raw dot product SIMD instructions.
            </span>
          </div>
        </div>

        {/* Right: 2D Semantic Cluster Map */}
        <div className="lg:col-span-7 bg-[#0c1424] border border-slate-800 rounded-2xl p-5 space-y-4 shadow-lg flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Layers className="w-4 h-4 text-teal-400" />
                2D Semantic Cluster Projection (PCA / UMAP)
              </h3>
              <p className="text-xs text-slate-400">
                Visualizing multi-dimensional chat separation across topic clusters
              </p>
            </div>
            <span className="text-[11px] font-mono text-cyan-400 bg-[#070b14] px-2 py-0.5 rounded border border-slate-800">
              {activeProfile.dimension}D → 2D Plane
            </span>
          </div>

          {/* Interactive Scatter Canvas representation */}
          <div className="relative h-64 bg-[#070b14] rounded-xl border border-slate-800 overflow-hidden p-4">
            {/* Grid overlay */}
            <div className="absolute inset-0 bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:20px_20px] pointer-events-none opacity-40"></div>
            
            {/* Center crosshairs */}
            <div className="absolute left-1/2 top-0 bottom-0 w-px bg-slate-800/60"></div>
            <div className="absolute top-1/2 left-0 right-0 h-px bg-slate-800/60"></div>

            {/* Plotted nodes */}
            {clusterPoints.map((pt, i) => {
              const colors: Record<string, string> = {
                'DevOps / Docker': 'bg-cyan-400 border-cyan-300 shadow-cyan-400/40',
                'Database & Vectors': 'bg-teal-400 border-teal-300 shadow-teal-400/40',
                'Payments & Legal': 'bg-amber-400 border-amber-300 shadow-amber-400/40',
                'Growth & Metrics': 'bg-purple-400 border-purple-300 shadow-purple-400/40'
              };

              return (
                <div
                  key={i}
                  style={{ left: `${pt.x}%`, top: `${pt.y}%` }}
                  className="absolute -translate-x-1/2 -translate-y-1/2 group cursor-pointer"
                >
                  <div className={`w-3.5 h-3.5 rounded-full border-2 ${colors[pt.category]} shadow-md transition-transform group-hover:scale-150`}></div>
                  
                  {/* Tooltip on hover */}
                  <div className="absolute bottom-5 left-1/2 -translate-x-1/2 hidden group-hover:block z-20 whitespace-nowrap bg-[#0b1322] border border-cyan-500/60 px-2.5 py-1 rounded text-[10px] text-white shadow-xl">
                    <span className="font-bold text-cyan-300">[{pt.provider}]</span> {pt.label}
                    <div className="text-[9px] text-slate-400">{pt.category}</div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Legend */}
          <div className="flex flex-wrap items-center justify-between text-[11px] text-slate-400 pt-1 border-t border-slate-800">
            <div className="flex items-center gap-3">
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-cyan-400"></span>
                <span>DevOps & Containers</span>
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-teal-400"></span>
                <span>Vector Databases</span>
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-400"></span>
                <span>Stripe & Billing</span>
              </span>
            </div>
            <span className="font-mono text-cyan-400 text-[10px]">
              Cosine Separation: High (0.84)
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
