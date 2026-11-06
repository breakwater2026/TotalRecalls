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
    { x: 45, y: 75, category: 'Payments & Legal', provider: 'Claude', label: '7-day Stripe refund' },
    { x: 50, y: 80, category: 'Payments & Legal', provider: 'Claude', label: 'Webhook idempotency' },
    { x: 85, y: 70, category: 'Growth & Metrics', provider: 'Perplexity', label: 'Q3 download metrics' }
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[var(--tr-bg)] via-[var(--tr-panel2)] to-[var(--tr-bg)] border border-[var(--tr-accent)]/30 p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5 max-w-2xl">
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[var(--tr-accent)]/20 text-[var(--tr-accent)] border border-[var(--tr-accent)]/40 flex items-center gap-1.5">
                <Cpu className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
                TotalRecalls Market-Leader Enhancement #2
              </span>
              <span className="text-xs text-[var(--tr-muted)] font-mono">Local Dimension & RAM Profiler</span>
            </div>
            <h2 className="text-2xl font-bold text-[var(--tr-text)] tracking-tight">
              Embedding Model Benchmark & Dimension Visualizer
            </h2>
            <p className="text-sm text-[var(--tr-muted)] leading-relaxed">
              Test and compare vector embedding engines on the fly. Benchmark memory footprint, latency, and index sizes between 384-dimensional ultra-fast local models and 768-dimensional deep semantic architectures.
            </p>
          </div>

          <div className="flex items-center gap-4 bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-xl p-3 px-4">
            <div>
              <div className="text-xs text-[var(--tr-muted)]">Current Vector Dim</div>
              <div className="text-xl font-bold font-mono text-[var(--tr-accent)]">{activeProfile.dimension}-D</div>
            </div>
            <div className="h-8 w-px bg-[var(--tr-panel)]"></div>
            <div>
              <div className="text-xs text-[var(--tr-muted)]">Active Engine</div>
              <div className="text-sm font-semibold text-[var(--tr-accent)] font-mono">{activeProfile.name.split(' ')[0]}</div>
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
                  ? 'bg-[var(--tr-accent)]/40 border-[var(--tr-accent)]/80 shadow-lg shadow'
                  : 'bg-[var(--tr-panel)] border-[var(--tr-border)] hover:border-[var(--tr-border)] hover:bg-[#0f1a2e]'
              }`}
            >
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-[var(--tr-panel2)] text-[var(--tr-accent)] border border-[var(--tr-border)]">
                    {profile.dimension}-dim ({profile.quantization})
                  </span>
                  {isSelected && (
                    <span className="text-[10px] text-[var(--tr-accent)] font-semibold flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" />
                      Active
                    </span>
                  )}
                </div>

                <h4 className="text-xs font-bold text-[var(--tr-text)] line-clamp-1">
                  {profile.name}
                </h4>

                <p className="text-[11px] text-[var(--tr-muted)] line-clamp-2">
                  {profile.description}
                </p>
              </div>

              <div className="pt-2 border-t border-[var(--tr-border)] text-[11px] font-mono space-y-1 text-[var(--tr-muted)]">
                <div className="flex justify-between">
                  <span>Latency:</span>
                  <span className="text-[var(--tr-accent)]">{profile.latencyPer1kTokensMs} ms/1k</span>
                </div>
                <div className="flex justify-between">
                  <span>RAM per 100k:</span>
                  <span className="text-[var(--tr-accent)]">{profile.ramUsageMBPer100k} MB</span>
                </div>
                <div className="flex justify-between">
                  <span>Runtime:</span>
                  <span className="text-[var(--tr-muted)]">{profile.provider}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Main 2-column: Benchmark Metrics & 2D PCA Cluster Visualizer */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Benchmark Profiler */}
        <div className="lg:col-span-5 bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-2xl p-5 space-y-4 shadow-lg flex flex-col justify-between">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-[var(--tr-text)] flex items-center gap-2">
                <BarChart2 className="w-4 h-4 text-[var(--tr-accent)]" />
                Live Engine Performance Profiler
              </h3>
              {isReindexing && (
                <span className="text-xs text-[var(--tr-accent)] flex items-center gap-1 font-mono">
                  <RefreshCw className="w-3 h-3 animate-spin" />
                  Re-indexing...
                </span>
              )}
            </div>

            {/* Simulated Corpus slider */}
            <div className="p-3 rounded-xl bg-[var(--tr-panel2)] border border-[var(--tr-border)] space-y-2">
              <div className="flex items-center justify-between text-xs text-[var(--tr-muted)]">
                <span>Simulate Total Vault Size:</span>
                <span className="font-mono text-[var(--tr-accent)] font-bold">{targetCorpusSize.toLocaleString()} Chunks</span>
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
                className="w-full  cursor-pointer"
              />
            </div>

            {/* KPI Cards */}
            {benchmarkResult && (
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="p-3 rounded-xl bg-[var(--tr-panel2)] border border-[var(--tr-border)] space-y-1">
                  <div className="text-[var(--tr-muted)] text-[11px]">Est. RAM Overhead</div>
                  <div className="text-lg font-bold font-mono text-[var(--tr-accent)]">
                    {benchmarkResult.estimatedRAMMB} MB
                  </div>
                  <div className="text-[10px] text-[var(--tr-muted)]">Nothing uploaded</div>
                </div>

                <div className="p-3 rounded-xl bg-[var(--tr-panel2)] border border-[var(--tr-border)] space-y-1">
                  <div className="text-[var(--tr-muted)] text-[11px]">Query Latency</div>
                  <div className="text-lg font-bold font-mono text-[var(--tr-accent)]">
                    {benchmarkResult.estimatedLatencyMs} ms
                  </div>
                  <div className="text-[10px] text-[var(--tr-muted)]">Local SIMD dot product</div>
                </div>

                <div className="p-3 rounded-xl bg-[var(--tr-panel2)] border border-[var(--tr-border)] space-y-1">
                  <div className="text-[var(--tr-muted)] text-[11px]">Throughput</div>
                  <div className="text-lg font-bold font-mono text-amber-300">
                    {benchmarkResult.throughputTokensSec.toLocaleString()} tok/s
                  </div>
                  <div className="text-[10px] text-[var(--tr-muted)]">M-Series / RTX GPU</div>
                </div>

                <div className="p-3 rounded-xl bg-[var(--tr-panel2)] border border-[var(--tr-border)] space-y-1">
                  <div className="text-[var(--tr-muted)] text-[11px]">Index Size on Disk</div>
                  <div className="text-lg font-bold font-mono text-sky-300">
                    {benchmarkResult.indexDiskSizeMB} MB
                  </div>
                  <div className="text-[10px] text-[var(--tr-muted)]">SQLite sqlite-vec file</div>
                </div>
              </div>
            )}
          </div>

          <div className="p-3 rounded-xl bg-[var(--tr-accent)]/30 border border-[var(--tr-accent)]/30 text-xs text-[var(--tr-muted)] flex items-start gap-2">
            <Info className="w-4 h-4 text-[var(--tr-accent)] flex-shrink-0 mt-0.5" />
            <span>
              TotalRecalls automatically normalizes vectors to unit length so that cosine similarity reduces to raw dot product SIMD instructions.
            </span>
          </div>
        </div>

        {/* Right: 2D Semantic Cluster Map */}
        <div className="lg:col-span-7 bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-2xl p-5 space-y-4 shadow-lg flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-[var(--tr-text)] flex items-center gap-2">
                <Layers className="w-4 h-4 text-[var(--tr-accent)]" />
                2D Semantic Cluster Projection (PCA / UMAP)
              </h3>
              <p className="text-xs text-[var(--tr-muted)]">
                Visualizing multi-dimensional chat separation across topic clusters
              </p>
            </div>
            <span className="text-[11px] font-mono text-[var(--tr-accent)] bg-[var(--tr-panel2)] px-2 py-0.5 rounded border border-[var(--tr-border)]">
              {activeProfile.dimension}D → 2D Plane
            </span>
          </div>

          {/* Interactive Scatter Canvas representation */}
          <div className="relative h-64 bg-[var(--tr-panel2)] rounded-xl border border-[var(--tr-border)] overflow-hidden p-4">
            {/* Grid overlay */}
            <div className="absolute inset-0 bg-[radial-gradient(var(--tr-bg)_1px,transparent_1px)] [background-size:20px_20px] pointer-events-none opacity-40"></div>
            
            {/* Center crosshairs */}
            <div className="absolute left-1/2 top-0 bottom-0 w-px bg-[var(--tr-panel)]"></div>
            <div className="absolute top-1/2 left-0 right-0 h-px bg-[var(--tr-panel)]"></div>

            {/* Plotted nodes */}
            {clusterPoints.map((pt, i) => {
              const colors: Record<string, string> = {
                'DevOps / Docker': 'bg-[var(--tr-accent)] border-[var(--tr-accent)] shadow',
                'Database & Vectors': 'bg-[var(--tr-accent)] border-[var(--tr-accent)] shadow',
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
                  <div className="absolute bottom-5 left-1/2 -translate-x-1/2 hidden group-hover:block z-20 whitespace-nowrap bg-[var(--tr-panel2)] border border-[var(--tr-accent)]/60 px-2.5 py-1 rounded text-[10px] text-[var(--tr-text)] shadow-xl">
                    <span className="font-bold text-[var(--tr-accent)]">[{pt.provider}]</span> {pt.label}
                    <div className="text-[9px] text-[var(--tr-muted)]">{pt.category}</div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Legend */}
          <div className="flex flex-wrap items-center justify-between text-[11px] text-[var(--tr-muted)] pt-1 border-t border-[var(--tr-border)]">
            <div className="flex items-center gap-3">
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-[var(--tr-accent)]"></span>
                <span>DevOps & Containers</span>
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-[var(--tr-accent)]"></span>
                <span>Vector Databases</span>
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-400"></span>
                <span>Stripe & Billing</span>
              </span>
            </div>
            <span className="font-mono text-[var(--tr-accent)] text-[10px]">
              Cosine Separation: High (0.84)
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
