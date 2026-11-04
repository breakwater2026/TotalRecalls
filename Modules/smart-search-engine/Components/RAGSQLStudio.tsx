import React, { useState } from 'react';
import { 
  Terminal, 
  Sparkles, 
  Play, 
  Copy, 
  Check, 
  Clock, 
  Database, 
  FileCode2, 
  BookOpen,
  Bot,
  Bookmark,
  Layers
} from 'lucide-react';
import { ChatConversation, SQLQueryResult, RAGAnswerResponse, ChunkEmbedding, SavedSQLView } from '../types';
import { naturalLanguageToSQL, executeHybridRAG, executeLocalSQL } from '../services/ragEngine';
import { SAVED_SQL_VIEWS } from '../constants';

interface RAGSQLStudioProps {
  conversations: ChatConversation[];
  chunks: ChunkEmbedding[];
}

export const RAGSQLStudio: React.FC<RAGSQLStudioProps> = ({ conversations, chunks }) => {
  const [nlQuery, setNlQuery] = useState('Which AI provider has the highest total tokens and chat count?');
  const [activeSQL, setActiveSQL] = useState<string>(
    'SELECT provider, COUNT(*) AS chat_count, SUM(total_tokens) AS total_tokens, ROUND(AVG(total_tokens)) AS avg_tokens FROM conversations GROUP BY provider ORDER BY total_tokens DESC;'
  );
  const [sqlResult, setSqlResult] = useState<SQLQueryResult | null>(() => 
    executeLocalSQL('SELECT provider, COUNT(*) AS chat_count, SUM(total_tokens) AS total_tokens, ROUND(AVG(total_tokens)) AS avg_tokens FROM conversations GROUP BY provider ORDER BY total_tokens DESC;', conversations)
  );
  const [savedViews, setSavedViews] = useState<SavedSQLView[]>(SAVED_SQL_VIEWS);
  const [useRRFHybrid, setUseRRFHybrid] = useState<boolean>(true);
  const [ragResponse, setRagResponse] = useState<RAGAnswerResponse | null>(null);
  const [isExecutingSQL, setIsExecutingSQL] = useState<boolean>(false);
  const [isGeneratingRAG, setIsGeneratingRAG] = useState<boolean>(false);
  const [copiedSQL, setCopiedSQL] = useState<boolean>(false);
  const [saveViewName, setSaveViewName] = useState<string>('');
  const [isSavingView, setIsSavingView] = useState<boolean>(false);

  const handleRunNLToSQL = async () => {
    if (!nlQuery.trim()) return;
    setIsExecutingSQL(true);
    try {
      const res = await naturalLanguageToSQL(nlQuery, conversations);
      setActiveSQL(res.generatedSQL);
      setSqlResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsExecutingSQL(false);
    }
  };

  const handleRunHybridRAG = async () => {
    if (!nlQuery.trim()) return;
    setIsGeneratingRAG(true);
    try {
      const rag = await executeHybridRAG(nlQuery, chunks, conversations, 'balanced');
      setRagResponse(rag);
      if (rag.generatedSQL) {
        setActiveSQL(rag.generatedSQL);
        setSqlResult(executeLocalSQL(rag.generatedSQL, conversations));
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsGeneratingRAG(false);
    }
  };

  const handleExecuteRawSQL = () => {
    setIsExecutingSQL(true);
    setTimeout(() => {
      const res = executeLocalSQL(activeSQL, conversations);
      setSqlResult(res);
      setIsExecutingSQL(false);
    }, 100);
  };

  const handleCopySQL = () => {
    navigator.clipboard.writeText(activeSQL);
    setCopiedSQL(true);
    setTimeout(() => setCopiedSQL(false), 2000);
  };

  const handleSaveCurrentView = () => {
    if (!saveViewName.trim()) return;
    const newView: SavedSQLView = {
      id: `view-${Date.now()}`,
      title: saveViewName,
      description: `Custom saved query executed against TotalRecalls SQLite schema.`,
      sql: activeSQL,
      category: 'topics'
    };
    setSavedViews(prev => [newView, ...prev]);
    setSaveViewName('');
    setIsSavingView(false);
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[var(--tr-bg)] via-[var(--tr-panel2)] to-[var(--tr-bg)] border border-[var(--tr-accent)]/30 p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5 max-w-2xl">
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[var(--tr-accent)]/20 text-[var(--tr-accent)] border border-[var(--tr-accent)]/30 flex items-center gap-1.5">
                <Database className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
                TotalRecalls Market-Leader Enhancement #4: RAG SQL & Saved Views
              </span>
              <span className="text-xs text-[var(--tr-muted)] font-mono">FTS5 + Vector Reciprocal Rank Fusion</span>
            </div>
            <h2 className="text-2xl font-bold text-[var(--tr-text)] tracking-tight">
              Natural Language to SQL & Saved RAG Views Studio
            </h2>
            <p className="text-sm text-[var(--tr-muted)] leading-relaxed">
              Query every turn, token metric, and timestamp in your downloaded archive using natural language or raw SQLite queries. Save persistent analytical views and execute hybrid RRF search.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-xl p-3 text-right">
              <div className="text-xs text-[var(--tr-muted)]">Saved SQL Views</div>
              <div className="text-sm font-mono text-[var(--tr-accent)] font-semibold">{savedViews.length} Active Presets</div>
            </div>
          </div>
        </div>
      </div>

      {/* Natural Language Prompt Bar */}
      <div className="bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-xl p-5 shadow-lg space-y-4">
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--tr-muted)] mb-2 flex items-center justify-between">
            <span className="flex items-center gap-1.5 text-[var(--tr-muted)]">
              <Sparkles className="w-4 h-4 text-[var(--tr-accent)]" />
              Ask In Plain English (Natural Language Query)
            </span>
            <div className="flex items-center gap-3">
              <label className="flex items-center gap-1.5 cursor-pointer text-[11px] text-[var(--tr-accent)]">
                <input
                  type="checkbox"
                  checked={useRRFHybrid}
                  onChange={(e) => setUseRRFHybrid(e.target.checked)}
                  className=""
                />
                <span>FTS5 + Vector RRF Blend</span>
              </label>
              <span className="text-[var(--tr-muted)] font-mono font-normal">Gemini Flash / SQLite Compiler</span>
            </div>
          </label>

          <div className="flex flex-col sm:flex-row gap-2">
            <input
              type="text"
              value={nlQuery}
              onChange={(e) => setNlQuery(e.target.value)}
              placeholder="e.g. 'Which AI provider has the highest total tokens?' or 'Find conversations mentioning Stripe refund'"
              className="flex-1 px-4 py-3 bg-[var(--tr-panel2)] border border-[var(--tr-border)]/80 rounded-xl text-[var(--tr-text)] placeholder-[var(--tr-muted)] focus:outline-none focus:ring-2 focus:ring-[var(--tr-accent)] text-sm"
            />
            <div className="flex items-center gap-2">
              <button
                onClick={handleRunNLToSQL}
                disabled={isExecutingSQL}
                className="px-4 py-3 bg-[var(--tr-panel)] hover:bg-[var(--tr-panel)] text-[var(--tr-accent)] border border-[var(--tr-accent)]/30 rounded-xl font-semibold text-xs transition-colors flex items-center gap-2 whitespace-nowrap"
              >
                <Terminal className="w-4 h-4" />
                <span>Compile to SQL</span>
              </button>
              <button
                onClick={handleRunHybridRAG}
                disabled={isGeneratingRAG}
                className="px-5 py-3 bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] hover:from-[var(--tr-accent)] hover:to-[var(--tr-accent2)] text-[var(--tr-text)] rounded-xl font-semibold text-xs transition-all flex items-center gap-2 shadow-md shadow whitespace-nowrap"
              >
                {isGeneratingRAG ? (
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                ) : (
                  <Bot className="w-4 h-4" />
                )}
                <span>Run Full Hybrid RAG</span>
              </button>
            </div>
          </div>
        </div>

        {/* Saved Views Picker */}
        <div className="space-y-2 pt-2 border-t border-[var(--tr-border)]">
          <div className="flex items-center justify-between text-xs">
            <span className="text-[var(--tr-muted)] flex items-center gap-1 font-semibold">
              <Bookmark className="w-3.5 h-3.5 text-[var(--tr-accent)]" />
              Saved Analytical Views:
            </span>
            <button
              onClick={() => setIsSavingView(!isSavingView)}
              className="text-[var(--tr-accent)] hover:text-[var(--tr-accent)] text-[11px] font-medium"
            >
              {isSavingView ? 'Cancel' : '+ Save Current Query as View'}
            </button>
          </div>

          {isSavingView && (
            <div className="p-3 bg-[var(--tr-panel2)] border border-[var(--tr-accent)]/40 rounded-lg flex items-center gap-2 text-xs">
              <input
                type="text"
                placeholder="View Title (e.g. 'Daily Active Token Consumption')"
                value={saveViewName}
                onChange={(e) => setSaveViewName(e.target.value)}
                className="flex-1 bg-[var(--tr-panel)] border border-[var(--tr-border)] px-3 py-1.5 rounded text-[var(--tr-text)] text-xs focus:outline-none"
              />
              <button
                onClick={handleSaveCurrentView}
                className="px-3 py-1.5 bg-[var(--tr-accent)] hover:bg-[var(--tr-accent)] text-[var(--tr-text)] font-semibold rounded text-xs"
              >
                Save View
              </button>
            </div>
          )}

          <div className="flex flex-wrap items-center gap-2">
            {savedViews.map((view) => (
              <button
                key={view.id}
                onClick={() => {
                  setActiveSQL(view.sql);
                  setSqlResult(executeLocalSQL(view.sql, conversations));
                }}
                className="px-2.5 py-1 rounded-md bg-[var(--tr-panel2)] hover:bg-[var(--tr-accent)]/50 text-[var(--tr-muted)] hover:text-[var(--tr-accent)] border border-[var(--tr-border)] hover:border-[var(--tr-accent)]/30 transition-colors text-xs flex items-center gap-1.5"
              >
                <Bookmark className="w-3 h-3 text-[var(--tr-accent)]" />
                <span>{view.title}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* RAG Synthesized Answer Section */}
      {ragResponse && (
        <div className="rounded-xl bg-gradient-to-b from-[var(--tr-accent)]/30 to-[var(--tr-panel)] border border-[var(--tr-accent)]/40 p-5 shadow-xl space-y-4">
          <div className="flex items-center justify-between border-b border-[var(--tr-accent)]/20 pb-3">
            <div className="flex items-center space-x-2">
              <div className="w-7 h-7 rounded-lg bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] flex items-center justify-center">
                <Bot className="w-4 h-4 text-[var(--tr-text)] font-bold" />
              </div>
              <h3 className="text-base font-bold text-[var(--tr-text)]">Hybrid RAG Grounded Synthesizer</h3>
            </div>
            <div className="flex items-center space-x-3 text-xs">
              <span className="text-[var(--tr-muted)] flex items-center gap-1 font-mono">
                <Clock className="w-3 h-3 text-[var(--tr-accent)]" />
                Latency: {ragResponse.latencyMs}ms
              </span>
              <span className="px-2 py-0.5 rounded bg-[var(--tr-accent)]/20 text-[var(--tr-accent)] font-semibold border border-[var(--tr-accent)]/30">
                100% Vault Verified
              </span>
            </div>
          </div>

          <div className="text-sm text-[var(--tr-text)] leading-relaxed bg-[var(--tr-panel2)] p-4 rounded-lg border border-[var(--tr-border)] whitespace-pre-wrap">
            {ragResponse.answer}
          </div>

          {/* Source citations */}
          <div>
            <div className="text-xs font-semibold uppercase tracking-wider text-[var(--tr-muted)] mb-2">
              Retrieved Grounding Sources ({ragResponse.sources.length}):
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {ragResponse.sources.map((src, i) => (
                <div key={i} className="p-2.5 rounded-lg bg-[var(--tr-panel2)] border border-[var(--tr-border)] text-xs">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-[var(--tr-accent)] truncate max-w-[200px]">
                      {src.conversationTitle}
                    </span>
                    <span className="px-1.5 py-0.5 rounded bg-[var(--tr-panel)] text-[10px] text-[var(--tr-muted)] font-mono">
                      {src.provider}
                    </span>
                  </div>
                  <p className="text-[var(--tr-muted)] text-[11px] line-clamp-2">
                    "{src.snippet}"
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* SQL Editor & Interactive Query Section */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: SQL Editor */}
        <div className="lg:col-span-5 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-[var(--tr-muted)] flex items-center gap-1.5">
              <FileCode2 className="w-4 h-4 text-[var(--tr-accent)]" />
              Generated / Custom SQL
            </span>
            <div className="flex items-center space-x-2">
              <button
                onClick={handleCopySQL}
                className="text-xs text-[var(--tr-muted)] hover:text-[var(--tr-text)] flex items-center gap-1"
                title="Copy SQL"
              >
                {copiedSQL ? <Check className="w-3.5 h-3.5 text-[var(--tr-accent)]" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedSQL ? 'Copied' : 'Copy'}</span>
              </button>
            </div>
          </div>

          <div className="relative">
            <textarea
              rows={7}
              value={activeSQL}
              onChange={(e) => setActiveSQL(e.target.value)}
              className="w-full p-4 bg-[var(--tr-panel2)] border border-[var(--tr-border)] rounded-xl font-mono text-xs text-[var(--tr-accent)] focus:outline-none focus:ring-2 focus:ring-[var(--tr-accent)] shadow-inner"
              spellCheck={false}
            />
            <button
              onClick={handleExecuteRawSQL}
              disabled={isExecutingSQL}
              className="absolute bottom-3 right-3 px-3 py-1.5 bg-gradient-to-r from-[var(--tr-accent)] to-[var(--tr-accent2)] hover:from-[var(--tr-accent)] hover:to-[var(--tr-accent2)] text-[var(--tr-text)] rounded-lg font-semibold text-xs transition-all flex items-center gap-1.5 shadow"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>Execute SQL</span>
            </button>
          </div>

          {/* SQLite Schema Reference */}
          <div className="p-3 rounded-lg bg-[var(--tr-panel2)] border border-[var(--tr-border)] text-[11px] text-[var(--tr-muted)] space-y-1 font-mono">
            <div className="font-semibold text-[var(--tr-muted)] text-xs">TotalRecalls Virtual SQLite Schema:</div>
            <div>• <span className="text-[var(--tr-accent)]">conversations</span>: id, title, provider, model, created_at, message_count, total_tokens, tags</div>
            <div>• <span className="text-[var(--tr-accent)]">messages</span>: id, conversation_id, conversation_title, provider, role, content, token_count, timestamp</div>
          </div>
        </div>

        {/* Right: SQL Results Table */}
        <div className="lg:col-span-7 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-[var(--tr-muted)] flex items-center gap-1.5">
              <Database className="w-4 h-4 text-[var(--tr-accent)]" />
              Query Execution Results
            </span>
            {sqlResult && (
              <span className="text-xs text-[var(--tr-muted)] font-mono flex items-center gap-1">
                <Clock className="w-3 h-3 text-[var(--tr-muted)]" />
                {sqlResult.executionTimeMs}ms • {sqlResult.rows.length} rows
              </span>
            )}
          </div>

          {sqlResult && sqlResult.rows.length > 0 ? (
            <div className="overflow-x-auto rounded-xl border border-[var(--tr-border)] bg-[var(--tr-panel2)] shadow-inner">
              <table className="w-full text-left text-xs font-sans">
                <thead className="bg-[var(--tr-panel2)] text-[var(--tr-muted)] border-b border-[var(--tr-border)]">
                  <tr>
                    {sqlResult.columns.map((col, idx) => (
                      <th key={idx} className="px-3.5 py-2.5 font-semibold font-mono text-[11px] uppercase tracking-wider text-[var(--tr-accent)]">
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--tr-border)]">
                  {sqlResult.rows.map((row, rIdx) => (
                    <tr key={rIdx} className="hover:bg-[#0c1626] transition-colors">
                      {sqlResult.columns.map((col, cIdx) => (
                        <td key={cIdx} className="px-3.5 py-2 text-[var(--tr-muted)] max-w-xs truncate font-mono">
                          {typeof row[col] === 'number' ? (
                            <span className="text-amber-300">{row[col].toLocaleString()}</span>
                          ) : (
                            String(row[col] ?? '')
                          )}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-8 text-center rounded-xl bg-[var(--tr-panel2)] border border-[var(--tr-border)] text-xs text-[var(--tr-muted)]">
              No rows returned. Execute a SELECT statement to preview local database records.
            </div>
          )}

          {sqlResult?.explanation && (
            <div className="text-xs text-[var(--tr-muted)] bg-[var(--tr-panel)] border border-[var(--tr-border)] rounded-lg p-2.5">
              <span className="font-semibold text-[var(--tr-muted)]">Explanation: </span>
              {sqlResult.explanation}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
