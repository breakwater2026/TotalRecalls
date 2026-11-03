import React, { useCallback, useEffect, useRef, useState } from 'react';
import { AlertCircle, CheckCircle2, Circle, Clock3, Loader2, Play, RotateCcw, ShieldCheck, XCircle } from 'lucide-react';
import { TEST_DEFINITIONS, runAllTests } from '../services/testRunner';
import { ChatConversation, ChunkEmbedding, TestCaseAssertion, TestSuiteSummary } from '../types';

interface IntegrityTestSuiteProps {
  conversations: ChatConversation[];
  chunks: ChunkEmbedding[];
  onSelectTab?: (tab: 'backup') => void;
}

const createPendingResults = (): TestCaseAssertion[] => TEST_DEFINITIONS.map(test => ({
  ...test,
  status: 'pending',
  durationMs: 0
}));

const criticalityLabels = {
  p0_critical: 'P0 · Critical',
  p1_high: 'P1 · High',
  p2_medium: 'P2 · Medium'
} as const;

const statusStyles = {
  passed: {
    icon: CheckCircle2,
    label: 'Passed',
    className: 'text-emerald-400'
  },
  failed: {
    icon: XCircle,
    label: 'Failed',
    className: 'text-rose-400'
  },
  running: {
    icon: Loader2,
    label: 'Running',
    className: 'text-cyan-400'
  },
  pending: {
    icon: Circle,
    label: 'Pending',
    className: 'text-slate-500'
  }
} as const;

export const IntegrityTestSuite: React.FC<IntegrityTestSuiteProps> = ({
  conversations,
  chunks,
  onSelectTab
}) => {
  const [results, setResults] = useState<TestCaseAssertion[]>(createPendingResults);
  const [summary, setSummary] = useState<TestSuiteSummary | null>(null);
  const [completedCount, setCompletedCount] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [executionError, setExecutionError] = useState<string | null>(null);
  const isRunningRef = useRef(false);

  const executeSuite = useCallback(async () => {
    if (isRunningRef.current) return;

    isRunningRef.current = true;
    setIsRunning(true);
    setExecutionError(null);
    setSummary(null);
    setCompletedCount(0);
    setResults(createPendingResults());

    try {
      const outcome = await runAllTests(conversations, chunks, (completed, _total, latest) => {
        setCompletedCount(completed);
        setResults(current => current.map(result => result.id === latest.id ? latest : result));
      });
      setResults(outcome.results);
      setSummary(outcome.summary);
      setCompletedCount(outcome.summary.total);
    } catch (error) {
      setExecutionError(error instanceof Error ? error.message : String(error));
    } finally {
      isRunningRef.current = false;
      setIsRunning(false);
    }
  }, [chunks, conversations]);

  useEffect(() => {
    void executeSuite();
  }, [executeSuite]);

  const progressPercent = Math.round((completedCount / TEST_DEFINITIONS.length) * 100);
  const categories = [...new Set(TEST_DEFINITIONS.map(test => test.category))];

  return (
    <div className="space-y-6">
      <section className="rounded-2xl border border-cyan-500/30 bg-gradient-to-r from-[#0c1f30] via-[#091524] to-[#070c16] p-6 shadow-xl">
        <div className="flex flex-col justify-between gap-5 md:flex-row md:items-center">
          <div className="max-w-3xl space-y-2">
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-cyan-300">
              <ShieldCheck className="h-4 w-4" />
              System integrity
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-white">Code Integrity Test Suite</h1>
            <p className="text-sm leading-relaxed text-slate-300">
              Run component and integration assertions against the current conversation and vector data.
              Results include test details, timing, and a digest of the completed run.
            </p>
            <p className="text-xs text-slate-400">
              Input data: {conversations.length.toLocaleString()} conversations · {chunks.length.toLocaleString()} indexed chunks
            </p>
          </div>
          <div className="flex shrink-0 flex-col gap-2 sm:flex-row">
            {onSelectTab && (
              <button
                type="button"
                onClick={() => onSelectTab('backup')}
                className="rounded-lg border border-slate-700 px-4 py-2 text-sm font-semibold text-slate-200 transition-colors hover:border-slate-500 hover:bg-slate-800/60"
              >
                Backup snapshots
              </button>
            )}
            <button
              type="button"
              onClick={() => void executeSuite()}
              disabled={isRunning}
              className="inline-flex items-center justify-center gap-2 rounded-lg bg-cyan-600 px-4 py-2 text-sm font-bold text-white transition-colors hover:bg-cyan-500 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isRunning ? <Loader2 className="h-4 w-4 animate-spin" /> : summary ? <RotateCcw className="h-4 w-4" /> : <Play className="h-4 w-4" />}
              {isRunning ? 'Running tests…' : summary ? 'Run again' : 'Run all tests'}
            </button>
          </div>
        </div>

        <div className="mt-6 space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-300">
            <span>{isRunning ? `Running ${completedCount} of ${TEST_DEFINITIONS.length}` : `${completedCount} of ${TEST_DEFINITIONS.length} tests completed`}</span>
            <span className="font-mono text-cyan-300">{progressPercent}%</span>
          </div>
          <div
            role="progressbar"
            aria-label="Integrity test progress"
            aria-valuemin={0}
            aria-valuemax={TEST_DEFINITIONS.length}
            aria-valuenow={completedCount}
            className="h-2 overflow-hidden rounded-full bg-slate-800"
          >
            <div className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-teal-400 transition-all" style={{ width: `${progressPercent}%` }} />
          </div>
        </div>
      </section>

      {executionError && (
        <div role="alert" className="flex items-start gap-3 rounded-xl border border-rose-500/40 bg-rose-950/30 p-4 text-sm text-rose-200">
          <AlertCircle className="mt-0.5 h-5 w-5 shrink-0" />
          <div>
            <div className="font-semibold">The test suite could not complete.</div>
            <div className="mt-1 text-rose-200/80">{executionError}</div>
          </div>
        </div>
      )}

      {summary && (
        <section aria-label="Test suite summary" className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <SummaryCard label="Passed" value={`${summary.passed} / ${summary.total}`} valueClass="text-emerald-300" />
          <SummaryCard label="Failed" value={String(summary.failed)} valueClass={summary.failed ? 'text-rose-300' : 'text-slate-100'} />
          <SummaryCard label="Duration" value={`${summary.overallDurationMs.toLocaleString()} ms`} valueClass="text-cyan-300" />
          <SummaryCard label="Completed" value={summary.executedAt} valueClass="text-slate-100" />
          <div className="rounded-xl border border-slate-800 bg-[#0c1424] p-4 sm:col-span-2 lg:col-span-4">
            <div className="text-xs font-semibold uppercase tracking-wider text-slate-400">Run integrity digest · SHA-256</div>
            <code className="mt-2 block break-all font-mono text-xs text-cyan-300">{summary.integrityHash}</code>
          </div>
        </section>
      )}

      <div className="space-y-5">
        {categories.map(category => {
          const categoryResults = results.filter(result => result.category === category);
          const passedCount = categoryResults.filter(result => result.status === 'passed').length;
          const failedCount = categoryResults.filter(result => result.status === 'failed').length;

          return (
            <section key={category} className="overflow-hidden rounded-xl border border-slate-800 bg-[#0c1424]">
              <header className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 px-4 py-3">
                <h2 className="text-sm font-bold text-white">{category}</h2>
                <span className="text-xs text-slate-400">
                  {passedCount} passed{failedCount ? ` · ${failedCount} failed` : ''} · {categoryResults.length} tests
                </span>
              </header>
              <div className="divide-y divide-slate-800/80">
                {categoryResults.map(result => {
                  const status = statusStyles[result.status];
                  const StatusIcon = status.icon;

                  return (
                    <article key={result.id} className="p-4">
                      <div className="flex items-start gap-3">
                        <StatusIcon className={`mt-0.5 h-5 w-5 shrink-0 ${status.className} ${result.status === 'running' ? 'animate-spin' : ''}`} />
                        <div className="min-w-0 flex-1">
                          <div className="flex flex-wrap items-center gap-x-2 gap-y-1">
                            <h3 className="text-sm font-semibold text-slate-100">{result.title}</h3>
                            <span className={`text-xs ${status.className}`}>{status.label}</span>
                          </div>
                          <p className="mt-1 text-xs leading-relaxed text-slate-400">{result.description}</p>
                          <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-[11px] text-slate-500">
                            <span>{result.id}</span>
                            <span>{criticalityLabels[result.criticality]}</span>
                            <span>{result.componentTarget}</span>
                            {result.durationMs > 0 && (
                              <span className="inline-flex items-center gap-1">
                                <Clock3 className="h-3 w-3" />
                                {result.durationMs} ms
                              </span>
                            )}
                          </div>
                          {result.details && <p className="mt-3 rounded-lg bg-slate-950/60 p-3 text-xs leading-relaxed text-slate-300">{result.details}</p>}
                          {result.error && <p role="alert" className="mt-3 rounded-lg border border-rose-500/30 bg-rose-950/20 p-3 text-xs text-rose-200">{result.error}</p>}
                        </div>
                      </div>
                    </article>
                  );
                })}
              </div>
            </section>
          );
        })}
      </div>
    </div>
  );
};

const SummaryCard: React.FC<{ label: string; value: string; valueClass: string }> = ({ label, value, valueClass }) => (
  <div className="rounded-xl border border-slate-800 bg-[#0c1424] p-4">
    <div className="text-xs font-semibold uppercase tracking-wider text-slate-400">{label}</div>
    <div className={`mt-2 font-mono text-lg font-bold ${valueClass}`}>{value}</div>
  </div>
);
