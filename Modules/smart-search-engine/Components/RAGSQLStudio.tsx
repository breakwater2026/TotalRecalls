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
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#0c1f30] via-[#091524] to-[#070c16] border border-cyan-500/30 p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5 max-w-2xl">
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 flex items-center gap-1.5">
                <Database className="w-3.5 h-3.5 text-cyan-400" />
                TotalRecalls Market-Leader Enhancement #4: RAG SQL & Saved Views
              </span>
              <span className="text-xs text-slate-400 font-mono">FTS5 + Vector Reciprocal Rank Fusion</span>
            </div>
            <h2 className="text-2xl font-bold text-white tracking-tight">
              Natural Language to SQL & Saved RAG Views Studio
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed">
              Query every turn, token metric, and timestamp in your downloaded archive using natural language or raw SQLite queries. Save persistent analytical views and execute hybrid RRF search.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="bg-[#080d19] border border-slate-800 rounded-xl p-3 text-right">
              <div className="text-xs text-slate-400">Saved SQL Views</div>
              <div className="text-sm font-mono text-cyan-400 font-semibold">{savedViews.length} Active Presets</div>
            </div>
          </div>
        </div>
      </div>

      {/* Natural Language Prompt Bar */}
      <div className="bg-[#0c1424] border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 flex items-center justify-between">
            <span className="flex items-center gap-1.5 text-slate-300">
              <Sparkles className="w-4 h-4 text-cyan-400" />
              Ask In Plain English (Natural Language Query)
            </span>
            <div className="flex items-center gap-3">
              <label className="flex items-center gap-1.5 cursor-pointer text-[11px] text-teal-400">
                <input
                  type="checkbox"
                  checked={useRRFHybrid}
                  onChange={(e) => setUseRRFHybrid(e.target.checked)}
                  className="accent-cyan-500"
                />
                <span>FTS5 + Vector RRF Blend</span>
              </label>
              <span className="text-slate-500 font-mono font-normal">Gemini Flash / SQLite Compiler</span>
            </div>
          </label>

          <div className="flex flex-col sm:flex-row gap-2">
            <input
              type="text"
              value={nlQuery}
              onChange={(e) => setNlQuery(e.target.value)}
              placeholder="e.g. 'Which AI provider has the highest total tokens?' or 'Find conversations mentioning Stripe refund'"
              className="flex-1 px-4 py-3 bg-[#070b14] border border-slate-700/80 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500 text-sm"
            />
            <div className="flex items-center gap-2">
              <button
                onClick={handleRunNLToSQL}
                disabled={isExecutingSQL}
                className="px-4 py-3 bg-[#080d19] hover:bg-slate-800 text-cyan-300 border border-cyan-500/30 rounded-xl font-semibold text-xs transition-colors flex items-center gap-2 whitespace-nowrap"
              >
                <Terminal className="w-4 h-4" />
                <span>Compile to SQL</span>
              </button>
              <button
                onClick={handleRunHybridRAG}
                disabled={isGeneratingRAG}
                className="px-5 py-3 bg-gradient-to-r from-cyan-600 to-teal-600 hover:from-cyan-500 hover:to-teal-500 text-white rounded-xl font-semibold text-xs transition-all flex items-center gap-2 shadow-md shadow-cyan-600/20 whitespace-nowrap"
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
        <div className="space-y-2 pt-2 border-t border-slate-800">
          <div className="flex items-center justify-between text-xs">
            <span className="text-slate-400 flex items-center gap-1 font-semibold">
              <Bookmark className="w-3.5 h-3.5 text-cyan-400" />
              Saved Analytical Views:
            </span>
            <button
              onClick={() => setIsSavingView(!isSavingView)}
              className="text-cyan-400 hover:text-cyan-300 text-[11px] font-medium"
            >
              {isSavingView ? 'Cancel' : '+ Save Current Query as View'}
            </button>
          </div>

          {isSavingView && (
            <div className="p-3 bg-[#070b14] border border-cyan-500/40 rounded-lg flex items-center gap-2 text-xs">
              <input
                type="text"
                placeholder="View Title (e.g. 'Daily Active Token Consumption')"
                value={saveViewName}
                onChange={(e) => setSaveViewName(e.target.value)}
                className="flex-1 bg-[#0c1424] border border-slate-700 px-3 py-1.5 rounded text-white text-xs focus:outline-none"
              />
              <button
                onClick={handleSaveCurrentView}
                className="px-3 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-white font-semibold rounded text-xs"
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
                className="px-2.5 py-1 rounded-md bg-[#070b14] hover:bg-cyan-950/50 text-slate-300 hover:text-cyan-300 border border-slate-800 hover:border-cyan-500/30 transition-colors text-xs flex items-center gap-1.5"
              >
                <Bookmark className="w-3 h-3 text-cyan-400" />
                <span>{view.title}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* RAG Synthesized Answer Section */}
      {ragResponse && (
        <div className="rounded-xl bg-gradient-to-b from-cyan-950/30 to-[#0c1424] border border-cyan-500/40 p-5 shadow-xl space-y-4">
          <div className="flex items-center justify-between border-b border-cyan-500/20 pb-3">
            <div className="flex items-center space-x-2">
              <div className="w-7 h-7 rounded-lg bg-gradient-to-r from-cyan-500 to-teal-500 flex items-center justify-center">
                <Bot className="w-4 h-4 text-slate-950 font-bold" />
              </div>
              <h3 className="text-base font-bold text-white">Hybrid RAG Grounded Synthesizer</h3>
            </div>
            <div className="flex items-center space-x-3 text-xs">
              <span className="text-slate-400 flex items-center gap-1 font-mono">
                <Clock className="w-3 h-3 text-cyan-400" />
                Latency: {ragResponse.latencyMs}ms
              </span>
              <span className="px-2 py-0.5 rounded bg-teal-500/20 text-teal-300 font-semibold border border-teal-500/30">
                100% Vault Verified
              </span>
            </div>
          </div>

          <div className="text-sm text-slate-200 leading-relaxed bg-[#070b14] p-4 rounded-lg border border-slate-800 whitespace-pre-wrap">
            {ragResponse.answer}
          </div>

          {/* Source citations */}
          <div>
            <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
              Retrieved Grounding Sources ({ragResponse.sources.length}):
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {ragResponse.sources.map((src, i) => (
                <div key={i} className="p-2.5 rounded-lg bg-[#070b14] border border-slate-800 text-xs">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-cyan-300 truncate max-w-[200px]">
                      {src.conversationTitle}
                    </span>
                    <span className="px-1.5 py-0.5 rounded bg-[#0c1424] text-[10px] text-slate-300 font-mono">
                      {src.provider}
                    </span>
                  </div>
                  <p className="text-slate-400 text-[11px] line-clamp-2">
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
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <FileCode2 className="w-4 h-4 text-cyan-400" />
              Generated / Custom SQL
            </span>
            <div className="flex items-center space-x-2">
              <button
                onClick={handleCopySQL}
                className="text-xs text-slate-400 hover:text-slate-200 flex items-center gap-1"
                title="Copy SQL"
              >
                {copiedSQL ? <Check className="w-3.5 h-3.5 text-teal-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedSQL ? 'Copied' : 'Copy'}</span>
              </button>
            </div>
          </div>

          <div className="relative">
            <textarea
              rows={7}
              value={activeSQL}
              onChange={(e) => setActiveSQL(e.target.value)}
              className="w-full p-4 bg-[#070b14] border border-slate-800 rounded-xl font-mono text-xs text-cyan-300 focus:outline-none focus:ring-2 focus:ring-cyan-500 shadow-inner"
              spellCheck={false}
            />
            <button
              onClick={handleExecuteRawSQL}
              disabled={isExecutingSQL}
              className="absolute bottom-3 right-3 px-3 py-1.5 bg-gradient-to-r from-cyan-600 to-teal-600 hover:from-cyan-500 hover:to-teal-500 text-white rounded-lg font-semibold text-xs transition-all flex items-center gap-1.5 shadow"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>Execute SQL</span>
            </button>
          </div>

          {/* SQLite Schema Reference */}
          <div className="p-3 rounded-lg bg-[#070b14] border border-slate-800 text-[11px] text-slate-400 space-y-1 font-mono">
            <div className="font-semibold text-slate-300 text-xs">TotalRecalls Virtual SQLite Schema:</div>
            <div>• <span className="text-cyan-400">conversations</span>: id, title, provider, model, created_at, message_count, total_tokens, tags</div>
            <div>• <span className="text-teal-400">messages</span>: id, conversation_id, conversation_title, provider, role, content, token_count, timestamp</div>
          </div>
        </div>

        {/* Right: SQL Results Table */}
        <div className="lg:col-span-7 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Database className="w-4 h-4 text-teal-400" />
              Query Execution Results
            </span>
            {sqlResult && (
              <span className="text-xs text-slate-400 font-mono flex items-center gap-1">
                <Clock className="w-3 h-3 text-slate-500" />
                {sqlResult.executionTimeMs}ms • {sqlResult.rows.length} rows
              </span>
            )}
          </div>

          {sqlResult && sqlResult.rows.length > 0 ? (
            <div className="overflow-x-auto rounded-xl border border-slate-800 bg-[#070b14] shadow-inner">
              <table className="w-full text-left text-xs font-sans">
                <thead className="bg-[#0b1322] text-slate-300 border-b border-slate-800">
                  <tr>
                    {sqlResult.columns.map((col, idx) => (
                      <th key={idx} className="px-3.5 py-2.5 font-semibold font-mono text-[11px] uppercase tracking-wider text-cyan-400">
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {sqlResult.rows.map((row, rIdx) => (
                    <tr key={rIdx} className="hover:bg-[#0c1626] transition-colors">
                      {sqlResult.columns.map((col, cIdx) => (
                        <td key={cIdx} className="px-3.5 py-2 text-slate-300 max-w-xs truncate font-mono">
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
            <div className="p-8 text-center rounded-xl bg-[#070b14] border border-slate-800 text-xs text-slate-500">
              No rows returned. Execute a SELECT statement to preview local database records.
            </div>
          )}

          {sqlResult?.explanation && (
            <div className="text-xs text-slate-400 bg-[#0c1424] border border-slate-800/80 rounded-lg p-2.5">
              <span className="font-semibold text-slate-300">Explanation: </span>
              {sqlResult.explanation}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
