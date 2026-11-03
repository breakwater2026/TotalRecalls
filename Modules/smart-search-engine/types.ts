export type AIProvider = 'ChatGPT' | 'Claude' | 'Gemini' | 'Perplexity' | 'Mistral' | 'LocalLlama';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  tokenCount?: number;
}

export interface ChatConversation {
  id: string;
  title: string;
  provider: AIProvider;
  model: string;
  createdAt: string;
  updatedAt: string;
  tags: string[];
  messageCount: number;
  totalTokens: number;
  messages: ChatMessage[];
  isIndexed?: boolean;
}

export interface ChunkEmbedding {
  id: string;
  conversationId: string;
  messageId: string;
  provider: AIProvider;
  conversationTitle: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: string;
  vector: number[];
  similarityScore?: number;
  bm25Score?: number;
  rrfScore?: number;
}

export interface SQLQueryResult {
  columns: string[];
  rows: Record<string, any>[];
  executionTimeMs: number;
  generatedSQL: string;
  explanation: string;
}

export interface RAGAnswerResponse {
  answer: string;
  sources: {
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
  latencyMs: number;
  modeUsed: 'semantic_vector' | 'hybrid_rag' | 'nl_to_sql' | 'rrf_hybrid';
}

export interface BenchmarkStat {
  provider: AIProvider;
  chatsCount: number;
  avgTokens: number;
  topTopic: string;
}

export interface ConsensusTopic {
  id: string;
  topicTitle: string;
  category: 'Architecture' | 'Security & Payments' | 'Local AI & DevOps' | 'Business & Metrics';
  summary: string;
  consensusLevel: 'High' | 'Divergent' | 'Complementary';
  providersCompared: {
    provider: AIProvider;
    stance: string;
    keySnippet: string;
    conversationId: string;
    sentimentScore: number; // 0-100
  }[];
  divergenceNotes: string;
  recommendedAction: string;
}

export interface PIIRuleMatch {
  type: 'API_KEY' | 'EMAIL' | 'IP_ADDRESS' | 'JWT_SECRET' | 'CREDIT_CARD';
  originalText: string;
  redactedText: string;
  count: number;
}

export interface EmbeddingEngineProfile {
  id: string;
  name: string;
  dimension: number;
  quantization: 'FP32' | 'FP16' | 'INT8' | 'Q4';
  latencyPer1kTokensMs: number;
  ramUsageMBPer100k: number;
  provider: 'Local / Ollama' | 'WASM / Browser' | 'Cloud Gemini';
  description: string;
}

export interface KnowledgeTopicCluster {
  id: string;
  name: string;
  category: string;
  conversationIds: string[];
  totalTokens: number;
  turnCount: number;
  topKeywords: string[];
  lastUpdated: string;
  confidenceScore: number;
  summary: string;
}

export type PersonaMode = 'balanced' | 'executive' | 'code_extractor' | 'fact_checker';

export interface PersonaConfig {
  id: PersonaMode;
  name: string;
  description: string;
  instruction: string;
  icon: string;
}

export interface SavedSQLView {
  id: string;
  title: string;
  description: string;
  sql: string;
  category: 'performance' | 'tokens' | 'topics' | 'security';
}

export interface RoadmapDrop {
  week: number;
  title: string;
  category: string;
  tagline: string;
  description: string;
  standalonePrice: string;
  standalonePriceNum: number;
  releaseDate: string;
  status: 'live' | 'next_up' | 'upcoming';
  features: string[];
  targetAudience: string;
  includedInPass: boolean;
}

// Downside Protection & Backup Scheduler Types
export type BackupFrequency = 'hourly' | 'daily' | 'weekly' | 'on_sync';
export type BackupDestination = 'local_vault' | 'external_drive' | 'cold_archive_zip';
export type BackupType = 'full' | 'differential';

export interface BackupScheduleConfig {
  enabled: boolean;
  frequency: BackupFrequency;
  timeOfDay: string; // e.g. "03:00"
  type: BackupType;
  destination: BackupDestination;
  customPath: string;
  retentionCopies: number; // e.g. 7, 30
  compressZip: boolean;
  encryptLocal: boolean;
  verifyChecksumOnCreate: boolean;
  pauseOnBattery: boolean;
}

export interface BackupSnapshot {
  id: string;
  timestamp: string;
  name: string;
  type: BackupType;
  destination: BackupDestination;
  totalConversations: number;
  totalChunks: number;
  totalTokens: number;
  sizeBytes: number;
  sizeFormatted: string;
  sha256Checksum: string;
  integrityStatus: 'verified' | 'unverified' | 'corrupt';
  verifiedAt?: string;
  rawPayloadSnippet?: string;
}

// Code Integrity Test Types
export type TestCategory = 
  | 'Vector Engine & Indexing'
  | 'Hybrid RAG & BM25 / RRF'
  | 'Natural Language SQL Compiler'
  | 'Consensus Auditor'
  | 'PII Scrubber & Anonymizer'
  | 'Knowledge Graph Clustering'
  | 'Embedding Benchmark'
  | 'Backup Scheduler & Downside'
  | 'End-to-End System Integration';

export interface TestCaseAssertion {
  id: string;
  title: string;
  category: TestCategory;
  componentTarget: string;
  description: string;
  status: 'pending' | 'running' | 'passed' | 'failed';
  durationMs: number;
  error?: string;
  details?: string;
  criticality: 'p0_critical' | 'p1_high' | 'p2_medium';
}

export interface TestSuiteSummary {
  total: number;
  passed: number;
  failed: number;
  pending: number;
  overallDurationMs: number;
  integrityHash: string;
  executedAt: string;
}
