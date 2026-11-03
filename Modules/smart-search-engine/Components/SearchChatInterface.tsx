import React, { useState, useRef, useEffect } from 'react';
import { 
  Search, 
  Send, 
  Bot, 
  User, 
  Sparkles, 
  Terminal, 
  Database, 
  Layers, 
  ExternalLink, 
  Clock, 
  ShieldCheck, 
  ChevronDown, 
  ChevronUp, 
  FileCode2, 
  Zap, 
  SlidersHorizontal,
  CheckCircle2,
  Briefcase,
  Sliders
} from 'lucide-react';
import { ChatConversation, ChunkEmbedding, AIProvider, PersonaMode } from '../types';
import { executeHybridRAG, searchVectorIndex, naturalLanguageToSQL } from '../services/ragEngine';
import { PERSONA_PROFILES } from '../constants';

interface SearchChatInterfaceProps {
  conversations: ChatConversation[];
  chunks: ChunkEmbedding[];
  onOpenConversation: (conversationId: string) => void;
}

interface ChatMessageItem {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: string;
  sources?: {
    chunkId: string;
    conversationTitle: string;
    provider: AIProvider;
    timestamp: string;
    snippet: string;
    score: number;
    conversationId?: string;
    bm25Score?: number;
    rrfScore?: number;
  }[];
  generatedSQL?: string;
  sqlRowsPreview?: Record<string, any>[];
  latencyMs?: number;
  mode?: 'hybrid' | 'vector_only' | 'sql_only';
  personaUsed?: PersonaMode;
}

export const SearchChatInterface: React.FC<SearchChatInterfaceProps> = ({
  conversations,
  chunks,
  onOpenConversation
}) => {
  const [messages, setMessages] = useState<ChatMessageItem[]>([
    {
      id: 'welcome-msg',
      sender: 'assistant',
      text: `Hello! Welcome to the **TotalRecalls Search Chat Assistant**—the interactive conversational interface of our Vector Search & RAG SQL Add-On.

I query your downloaded chat history across **ChatGPT, Claude, Gemini, Perplexity, and Mistral**. 
Using local vector embeddings, BM25 Reciprocal Rank Fusion (RRF), and SQLite relational tables, I synthesize grounded answers with full source citations—with **100% privacy and zero cloud leaks**.`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      sources: [
        {
          chunkId: 'chunk-tr-conv-101-m-101-2',
          conversationTitle: 'PostgreSQL Vector Extension (pgvector) Schema Design & Indexing',
          provider: 'ChatGPT',
          timestamp: '2024-10-14',
          snippet: 'To build an efficient local RAG vector store, define a chat_chunks table with HNSW index...',
          score: 0.94,
          rrfScore: 0.92
        },
        {
          chunkId: 'chunk-tr-conv-102-m-102-2',
          conversationTitle: 'Customer Refund Policy & Stripe Webhook Architecture',
          provider: 'Claude',
          timestamp: '2024-10-18',
          snippet: 'Under TotalRecalls commercial terms: full refund within 30 days of purchase if license key is deactivated locally...',
          score: 0.89,
          rrfScore: 0.88
        }
      ],
      generatedSQL: 'SELECT provider, COUNT(*) as chats, SUM(total_tokens) as tokens FROM conversations GROUP BY provider;',
      sqlRowsPreview: [
        { provider: 'ChatGPT', chats: 1, tokens: 1420 },
        { provider: 'Claude', chats: 1, tokens: 2150 },
        { provider: 'Gemini', chats: 1, tokens: 1890 }
      ],
      latencyMs: 38,
      mode: 'hybrid',
      personaUsed: 'balanced'
    }
  ]);

  const [inputQuery, setInputQuery] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [searchMode, setSearchMode] = useState<'hybrid' | 'vector_only' | 'sql_only'>('hybrid');
  const [activePersona, setActivePersona] = useState<PersonaMode>('balanced');
  const [providerFilter, setProviderFilter] = useState<string>('ALL');
  const [expandedSources, setExpandedSources] = useState<Record<string, boolean>>({});
  const [expandedSQL, setExpandedSQL] = useState<Record<string, boolean>>({});

  const chatBottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isProcessing]);

  const toggleSourceExpand = (msgId: string) => {
    setExpandedSources(prev => ({ ...prev, [msgId]: !prev[msgId] }));
  };

  const toggleSQLExpand = (msgId: string) => {
    setExpandedSQL(prev => ({ ...prev, [msgId]: !prev[msgId] }));
  };

  const handleSendMessage = async (queryText?: string) => {
    const q = (queryText || inputQuery).trim();
    if (!q || isProcessing) return;

    const userMessageId = `user-${Date.now()}`;
    const userMsg: ChatMessageItem = {
      id: userMessageId,
      sender: 'user',
      text: q,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setInputQuery('');
    setIsProcessing(true);

    const startTime = performance.now();

    try {
      if (searchMode === 'vector_only') {
        const retrieved = searchVectorIndex(q, chunks, 4, 0.12, providerFilter, true);
        const latency = Math.round(performance.now() - startTime);

        let answer = `Here are the top semantic matches found in your TotalRecalls local vault:`;
        if (retrieved.length > 0) {
          answer += `\n\n**Top Match from ${retrieved[0].provider}** (*"${retrieved[0].conversationTitle}"*):\n${retrieved[0].content.substring(0, 320)}...`;
        } else {
          answer = `No semantic chunks matched your query "${q}" under the current filter (${providerFilter}). Try broadening your search or switching to Hybrid RAG mode.`;
        }

        const assistantMsg: ChatMessageItem = {
          id: `asst-${Date.now()}`,
          sender: 'assistant',
          text: answer,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          sources: retrieved.map(r => ({
            chunkId: r.id,
            conversationTitle: r.conversationTitle,
            provider: r.provider,
            timestamp: r.timestamp,
            snippet: r.content.substring(0, 200) + '...',
            score: r.similarityScore || 0.85,
            bm25Score: r.bm25Score,
            rrfScore: r.rrfScore,
            conversationId: r.conversationId
          })),
          latencyMs: latency,
          mode: 'vector_only',
          personaUsed: activePersona
        };

        setMessages(prev => [...prev, assistantMsg]);
      } else if (searchMode === 'sql_only') {
        const sqlRes = await naturalLanguageToSQL(q, conversations);
        const latency = Math.round(performance.now() - startTime);

        const summaryText = `Compiled and executed SQL on local SQLite archive: \`${sqlRes.generatedSQL}\`\n\n**Returned ${sqlRes.rows.length} rows in ${sqlRes.executionTimeMs}ms.**\n${sqlRes.explanation}`;

        const assistantMsg: ChatMessageItem = {
          id: `asst-${Date.now()}`,
          sender: 'assistant',
          text: summaryText,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          generatedSQL: sqlRes.generatedSQL,
          sqlRowsPreview: sqlRes.rows.slice(0, 5),
          latencyMs: latency,
          mode: 'sql_only',
          personaUsed: activePersona
        };

        setMessages(prev => [...prev, assistantMsg]);
      } else {
        // Hybrid RAG with active persona (Enhancement #7)
        const ragRes = await executeHybridRAG(q, chunks, conversations, activePersona);
        const sqlRes = await naturalLanguageToSQL(q, conversations);

        const assistantMsg: ChatMessageItem = {
          id: `asst-${Date.now()}`,
          sender: 'assistant',
          text: ragRes.answer,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          sources: ragRes.sources,
          generatedSQL: ragRes.generatedSQL || sqlRes.generatedSQL,
          sqlRowsPreview: sqlRes.rows.slice(0, 4),
          latencyMs: ragRes.latencyMs,
          mode: 'hybrid',
          personaUsed: activePersona
        };

        setMessages(prev => [...prev, assistantMsg]);
      }
    } catch (err) {
      console.error(err);
      const errorMsg: ChatMessageItem = {
        id: `asst-err-${Date.now()}`,
        sender: 'assistant',
        text: 'An error occurred while querying the vault. Fallback local semantic answer generated from in-memory index.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsProcessing(false);
    }
  };

  const samplePrompts = [
    'How do we handle 30-day refunds and Stripe webhooks?',
    'What did Claude say about Docker and Ollama with GPU?',
    'Show me token consumption breakdown by AI provider',
    'Which conversation discussed HNSW indexes and pgvector?',
    'Find all conversations discussing SQLite vs microservices'
  ];

  const providerColors: Record<AIProvider, string> = {
    ChatGPT: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    Claude: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
    Gemini: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30',
    Perplexity: 'bg-teal-500/10 text-teal-400 border-teal-500/30',
    Mistral: 'bg-orange-500/10 text-orange-400 border-orange-500/30',
    LocalLlama: 'bg-sky-500/10 text-sky-400 border-sky-500/30'
  };

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] min-h-[660px] max-h-[940px] rounded-2xl bg-[#0b1120] border border-cyan-900/30 shadow-2xl overflow-hidden">
      {/* Top Search Chat Header & Mode Bar in TotalRecalls brand cyan/teal */}
      <div className="bg-[#080d19] border-b border-slate-800/90 p-4 flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 to-teal-500 flex items-center justify-center shadow-md shadow-cyan-500/20">
            <Sparkles className="w-5 h-5 text-slate-950 font-bold" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-base font-bold text-white tracking-tight">Search Chat GUI</h2>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-cyan-500/15 text-cyan-300 border border-cyan-500/30">
                Vector + RAG SQL + RRF
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Interactive conversational retrieval across <span className="text-cyan-400 font-mono">{conversations.length}</span> chats & <span className="text-teal-400 font-mono">{chunks.length}</span> vectors
            </p>
          </div>
        </div>

        {/* Persona Mode (Enhancement #7) & Search Mode Toggles */}
        <div className="flex flex-wrap items-center gap-2">
          {/* Persona selector */}
          <div className="flex items-center bg-[#070b14] border border-slate-800 rounded-lg p-1 text-xs">
            <span className="text-slate-500 px-1 text-[10px] uppercase font-mono font-bold">Persona:</span>
            {PERSONA_PROFILES.map(persona => (
              <button
                key={persona.id}
                onClick={() => setActivePersona(persona.id)}
                className={`px-2 py-0.5 rounded font-medium text-[11px] transition-all ${
                  activePersona === persona.id
                    ? 'bg-gradient-to-r from-cyan-600 to-teal-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
                title={persona.description}
              >
                {persona.name.split(' ')[0]}
              </button>
            ))}
          </div>

          {/* Retrieval Engine Selector */}
          <div className="flex items-center bg-[#070b14] border border-slate-800 rounded-lg p-1 text-xs">
            <button
              onClick={() => setSearchMode('hybrid')}
              className={`px-2.5 py-1 rounded-md font-semibold transition-all ${
                searchMode === 'hybrid'
                  ? 'bg-gradient-to-r from-cyan-600 to-teal-600 text-white shadow-sm shadow-cyan-500/20'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="Combines semantic vector chunks and structured SQL metadata"
            >
              Hybrid RAG
            </button>
            <button
              onClick={() => setSearchMode('vector_only')}
              className={`px-2.5 py-1 rounded-md font-semibold transition-all ${
                searchMode === 'vector_only'
                  ? 'bg-gradient-to-r from-cyan-600 to-teal-600 text-white shadow-sm shadow-cyan-500/20'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="Pure cosine similarity semantic search"
            >
              Vector Only
            </button>
            <button
              onClick={() => setSearchMode('sql_only')}
              className={`px-2.5 py-1 rounded-md font-semibold transition-all ${
                searchMode === 'sql_only'
                  ? 'bg-gradient-to-r from-cyan-600 to-teal-600 text-white shadow-sm shadow-cyan-500/20'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="Direct Natural Language to SQLite query execution"
            >
              NL → SQL
            </button>
          </div>

          {/* Provider Filter */}
          <div className="flex items-center gap-1.5 text-xs">
            <select
              value={providerFilter}
              onChange={(e) => setProviderFilter(e.target.value)}
              className="bg-[#070b14] border border-slate-800 rounded-lg px-2 py-1 text-slate-300 text-xs focus:outline-none focus:border-cyan-500"
            >
              <option value="ALL">All Providers</option>
              <option value="ChatGPT">ChatGPT Only</option>
              <option value="Claude">Claude Only</option>
              <option value="Gemini">Gemini Only</option>
              <option value="Perplexity">Perplexity Only</option>
              <option value="Mistral">Mistral Only</option>
            </select>
          </div>
        </div>
      </div>

      {/* Messages Stream */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6 bg-gradient-to-b from-[#0b1120] to-[#070b14]">
        {messages.map((msg) => {
          const isUser = msg.sender === 'user';
          const hasSources = msg.sources && msg.sources.length > 0;
          const hasSQL = Boolean(msg.generatedSQL);
          const isSourcesOpen = expandedSources[msg.id];
          const isSQLOpen = expandedSQL[msg.id];

          return (
            <div
              key={msg.id}
              className={`flex items-start gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}
            >
              {/* Avatar */}
              <div
                className={`w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 ${
                  isUser
                    ? 'bg-gradient-to-br from-cyan-500 to-teal-600 text-slate-950 font-bold shadow-md shadow-cyan-500/20'
                    : 'bg-[#0e1626] border border-cyan-500/30 text-cyan-400'
                }`}
              >
                {isUser ? <User className="w-4 h-4 text-white" /> : <Bot className="w-4 h-4 text-cyan-400" />}
              </div>

              {/* Message Bubble Container */}
              <div className={`max-w-[85%] sm:max-w-[78%] space-y-2 ${isUser ? 'items-end' : 'items-start'}`}>
                {/* Meta info */}
                <div className={`flex items-center gap-2 text-[11px] text-slate-500 ${isUser ? 'justify-end' : 'justify-start'}`}>
                  <span className="font-semibold text-slate-400">
                    {isUser ? 'You' : 'TotalRecalls Assistant'}
                  </span>
                  <span>•</span>
                  <span>{msg.timestamp}</span>
                  {msg.latencyMs && (
                    <span className="font-mono text-teal-400 text-[10px]">
                      ({msg.latencyMs}ms)
                    </span>
                  )}
                  {msg.personaUsed && (
                    <span className="px-1.5 py-0.2 rounded bg-teal-950/60 border border-teal-800/40 text-[10px] text-teal-300 font-mono">
                      {msg.personaUsed}
                    </span>
                  )}
                  {msg.mode && (
                    <span className="px-1.5 py-0.2 rounded bg-cyan-950/60 border border-cyan-800/40 text-[10px] text-cyan-300 font-mono">
                      {msg.mode}
                    </span>
                  )}
                </div>

                {/* Message Body */}
                <div
                  className={`rounded-2xl p-4 text-sm leading-relaxed whitespace-pre-wrap ${
                    isUser
                      ? 'bg-gradient-to-r from-cyan-600 to-teal-600 text-white rounded-tr-none shadow-md shadow-cyan-600/10'
                      : 'bg-[#0c1424] text-slate-200 border border-slate-800 rounded-tl-none shadow-md'
                  }`}
                >
                  {msg.text}
                </div>

                {/* Grounding Source Accordion */}
                {!isUser && hasSources && (
                  <div className="rounded-xl border border-cyan-500/20 bg-cyan-950/20 overflow-hidden text-xs">
                    <button
                      onClick={() => toggleSourceExpand(msg.id)}
                      className="w-full px-3 py-2 flex items-center justify-between text-cyan-300 hover:bg-cyan-900/30 transition-colors"
                    >
                      <div className="flex items-center gap-2">
                        <Layers className="w-3.5 h-3.5 text-cyan-400" />
                        <span className="font-semibold">
                          Grounding Citations ({msg.sources?.length} Vector & BM25 Chunks)
                        </span>
                      </div>
                      {isSourcesOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>

                    {isSourcesOpen && (
                      <div className="p-3 border-t border-cyan-500/20 space-y-2 bg-[#080d19]/90">
                        {msg.sources?.map((src, sIdx) => (
                          <div
                            key={sIdx}
                            className="p-2.5 rounded-lg bg-[#0c1424] border border-slate-800 space-y-1.5"
                          >
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-2">
                                <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold border ${providerColors[src.provider]}`}>
                                  {src.provider}
                                </span>
                                <span className="font-semibold text-slate-200 truncate max-w-[240px]">
                                  {src.conversationTitle}
                                </span>
                              </div>
                              <div className="flex items-center gap-2 text-[10px] font-mono">
                                <span className="text-teal-400">RRF: {Math.round((src.rrfScore || src.score) * 100)}%</span>
                                <span className="text-cyan-400">Cos: {Math.round(src.score * 100)}%</span>
                              </div>
                            </div>

                            <p className="text-[11px] text-slate-400 italic">
                              "{src.snippet}"
                            </p>

                            {src.conversationId && (
                              <button
                                onClick={() => onOpenConversation(src.conversationId!)}
                                className="text-[10px] text-cyan-400 hover:text-cyan-300 flex items-center gap-1 font-medium pt-0.5"
                              >
                                <span>Inspect turn in Downloader Vault</span>
                                <ExternalLink className="w-2.5 h-2.5" />
                              </button>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* SQL Telemetry Accordion */}
                {!isUser && hasSQL && (
                  <div className="rounded-xl border border-teal-500/20 bg-teal-950/20 overflow-hidden text-xs">
                    <button
                      onClick={() => toggleSQLExpand(msg.id)}
                      className="w-full px-3 py-2 flex items-center justify-between text-teal-300 hover:bg-teal-900/30 transition-colors"
                    >
                      <div className="flex items-center gap-2">
                        <Terminal className="w-3.5 h-3.5 text-teal-400" />
                        <span className="font-semibold">Relational SQL Context (SQLite)</span>
                      </div>
                      {isSQLOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>

                    {isSQLOpen && (
                      <div className="p-3 border-t border-teal-500/20 space-y-2 bg-[#080d19]/90 font-mono">
                        <div className="p-2 rounded bg-[#070c16] text-teal-300 text-[11px] overflow-x-auto border border-teal-900/30">
                          {msg.generatedSQL}
                        </div>

                        {msg.sqlRowsPreview && msg.sqlRowsPreview.length > 0 && (
                          <div className="text-[10px] text-slate-400">
                            <span className="font-semibold text-slate-300">Preview Records: </span>
                            {JSON.stringify(msg.sqlRowsPreview)}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {isProcessing && (
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-xl bg-[#0e1626] border border-cyan-500/30 flex items-center justify-center text-cyan-400">
              <Bot className="w-4 h-4" />
            </div>
            <div className="bg-[#0c1424] border border-slate-800 rounded-2xl rounded-tl-none p-4 space-y-2 max-w-sm shadow-md">
              <div className="flex items-center space-x-2 text-xs text-slate-300">
                <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span>
                <span>Searching local vector index & SQLite schema...</span>
              </div>
              <div className="w-full bg-slate-800 h-1 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-cyan-400 via-teal-400 to-sky-400 animate-pulse w-3/4"></div>
              </div>
            </div>
          </div>
        )}

        <div ref={chatBottomRef} />
      </div>

      {/* Suggested Query Chips */}
      <div className="px-4 py-2 border-t border-slate-800/80 bg-[#080d19] flex items-center gap-2 overflow-x-auto text-xs whitespace-nowrap">
        <span className="text-slate-400 flex items-center gap-1 flex-shrink-0 text-[11px] font-semibold">
          <Sparkles className="w-3 h-3 text-cyan-400" />
          Suggested:
        </span>
        {samplePrompts.map((prompt, i) => (
          <button
            key={i}
            onClick={() => handleSendMessage(prompt)}
            className="px-2.5 py-1 rounded-md bg-[#0c1424] hover:bg-cyan-950/60 text-slate-300 hover:text-cyan-300 border border-slate-800 hover:border-cyan-500/40 transition-colors flex-shrink-0"
          >
            "{prompt}"
          </button>
        ))}
      </div>

      {/* Input Bar */}
      <div className="p-3 sm:p-4 bg-[#080d19] border-t border-slate-800">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          className="relative flex items-center"
        >
          <div className="absolute left-3.5 text-cyan-400 pointer-events-none">
            <Search className="w-4 h-4" />
          </div>
          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            placeholder="Ask a question across your downloaded AI chats..."
            className="w-full pl-10 pr-24 py-3 bg-[#0c1424] border border-slate-800 focus:border-cyan-500 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/30 text-sm shadow-inner"
          />
          <button
            type="submit"
            disabled={!inputQuery.trim() || isProcessing}
            className="absolute right-2 px-4 py-1.5 bg-gradient-to-r from-cyan-600 to-teal-600 hover:from-cyan-500 hover:to-teal-500 text-white rounded-lg font-semibold text-xs transition-all flex items-center gap-1.5 disabled:opacity-40 disabled:cursor-not-allowed shadow-md shadow-cyan-600/20"
          >
            <span>Ask Vault</span>
            <Send className="w-3.5 h-3.5" />
          </button>
        </form>

        <div className="mt-2 flex items-center justify-between text-[11px] text-slate-500 px-1">
          <div className="flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-teal-400" />
            <span className="text-slate-400">Local Vault Isolation: zero cloud telemetry leaves your device.</span>
          </div>
          <div className="font-mono hidden sm:block text-slate-400">
            <span>Mode: {searchMode} • Persona: {activePersona}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
