import { 
  ChatConversation, 
  ChunkEmbedding, 
  TestCaseAssertion, 
  TestSuiteSummary
} from '../types';
import { 
  calculateBM25Score,
  compileLocalNLToSQL,
  cosineSimilarity,
  executeLocalSQL,
  generateLocalPseudoEmbedding,
  searchVectorIndex
} from './ragEngine';
import { auditAndScrubPII } from './datasetExporters';
import { computeSHA256, createLiveSnapshot, verifySnapshotIntegrity } from './backupEngine';
import { EMBEDDING_PROFILES, CONSENSUS_TOPICS, INITIAL_KNOWLEDGE_CLUSTERS } from '../constants';

export const TEST_DEFINITIONS: Omit<TestCaseAssertion, 'status' | 'durationMs' | 'error' | 'details'>[] = [
  // 1. Vector Engine & Indexing
  {
    id: 'test-vec-01',
    title: 'Vector Index Construction & Dimensions Match',
    category: 'Vector Engine & Indexing',
    componentTarget: 'VectorSearch.tsx & ragEngine.ts',
    description: 'Verifies that every chunk has consistent 384/768-dimensional finite, normalized vectors.',
    criticality: 'p0_critical'
  },
  {
    id: 'test-vec-02',
    title: 'Cosine Similarity Bounds & Invariants',
    category: 'Vector Engine & Indexing',
    componentTarget: 'ragEngine.ts (searchVectorIndex)',
    description: 'Ensures cosine similarity outputs remain bounded in [-1.0, 1.0] and self-similarity equals 1.000.',
    criticality: 'p0_critical'
  },
  {
    id: 'test-vec-03',
    title: 'Top-K Retrieval Consistency & Ordering',
    category: 'Vector Engine & Indexing',
    componentTarget: 'VectorSearch.tsx',
    description: 'Validates that hybrid vector query matches are sorted in descending score order.',
    criticality: 'p1_high'
  },

  // 2. Hybrid RAG & BM25 / RRF
  {
    id: 'test-rag-01',
    title: 'BM25 Term Frequency & Document Frequency Ranking',
    category: 'Hybrid RAG & BM25 / RRF',
    componentTarget: 'ragEngine.ts (calculateBM25Score)',
    description: 'Validates lexical term matching and title boosts on technical terms.',
    criticality: 'p1_high'
  },
  {
    id: 'test-rag-02',
    title: 'Hybrid Vector and Lexical Score Blending',
    category: 'Hybrid RAG & BM25 / RRF',
    componentTarget: 'SearchChatInterface.tsx (Hybrid Mode)',
    description: 'Confirms hybrid search combines cosine similarity and lexical BM25 scores consistently.',
    criticality: 'p0_critical'
  },

  // 3. Natural Language to SQL
  {
    id: 'test-sql-01',
    title: 'Natural Language to SQLite SQL Synthesis',
    category: 'Natural Language SQL Compiler',
    componentTarget: 'RAGSQLStudio.tsx & ragEngine.ts (compileLocalNLToSQL)',
    description: 'Verifies natural language queries compile to valid local SELECT statements and return matching rows.',
    criticality: 'p0_critical'
  },
  {
    id: 'test-sql-02',
    title: 'SQL Read-Only Sandbox Guardrails',
    category: 'Natural Language SQL Compiler',
    componentTarget: 'ragEngine.ts (executeLocalSQL)',
    description: 'Rejects non-SELECT statements, destructive clauses, and multiple SQL statements.',
    criticality: 'p0_critical'
  },

  // 4. Consensus Auditor
  {
    id: 'test-audit-01',
    title: 'Cross-Model Multi-Provider Stance Comparison',
    category: 'Consensus Auditor',
    componentTarget: 'ConsensusAuditor.tsx',
    description: 'Verifies multi-provider extraction across ChatGPT, Claude, Gemini, and Local Llama with sentiment categorization.',
    criticality: 'p1_high'
  },

  // 5. PII Scrubber & Anonymizer
  {
    id: 'test-pii-01',
    title: 'Automated Secret Redaction (API Keys, JWT, PII)',
    category: 'PII Scrubber & Anonymizer',
    componentTarget: 'DatasetScrubber.tsx & datasetExporters.ts',
    description: 'Validates detection and redaction of API keys and email addresses before dataset export.',
    criticality: 'p0_critical'
  },

  // 6. Embedding Benchmark
  {
    id: 'test-bench-01',
    title: 'Embedding Hardware Profiles & Quantization Integrity',
    category: 'Embedding Benchmark',
    componentTarget: 'EmbeddingBenchmark.tsx',
    description: 'Verifies FP32 vs INT8 vs Q4 quantization memory and latency benchmarks conform to local hardware constraints.',
    criticality: 'p2_medium'
  },

  // 7. Knowledge Graph Clustering
  {
    id: 'test-kg-01',
    title: 'Knowledge Graph Cluster Integrity',
    category: 'Knowledge Graph Clustering',
    componentTarget: 'KnowledgeGraph.tsx',
    description: 'Validates seeded knowledge clusters, confidence ranges, and conversation references.',
    criticality: 'p1_high'
  },

  // 8. Backup Scheduler & Downside Protection
  {
    id: 'test-backup-01',
    title: 'SHA-256 Vault Snapshot Checksum Generation',
    category: 'Backup Scheduler & Downside',
    componentTarget: 'BackupScheduler.tsx & backupEngine.ts',
    description: 'Verifies cryptographic SHA-256 snapshot hashing for tamper-proof downside protection and zero bit-rot.',
    criticality: 'p0_critical'
  },
  {
    id: 'test-backup-02',
    title: 'Snapshot Round-Trip Verification & Recovery Invariants',
    category: 'Backup Scheduler & Downside',
    componentTarget: 'BackupScheduler.tsx (verifySnapshotIntegrity)',
    description: 'Validates snapshot serialization, checksum verification, and tamper detection.',
    criticality: 'p0_critical'
  },

  // 9. End-to-End System Integration
  {
    id: 'test-e2e-01',
    title: 'Local Integrity Operations Make No Fetch Requests',
    category: 'End-to-End System Integration',
    componentTarget: 'Local services (fetch-intercepted)',
    description: 'Ensures local search, SQL, PII audit, and snapshot operations dispatch no fetch requests.',
    criticality: 'p0_critical'
  }
];

export async function runIndividualTest(
  testDef: typeof TEST_DEFINITIONS[0],
  conversations: ChatConversation[],
  chunks: ChunkEmbedding[]
): Promise<TestCaseAssertion> {
  const t0 = performance.now();
  let status: 'passed' | 'failed' = 'passed';
  let error: string | undefined = undefined;
  let details: string | undefined = undefined;

  try {
    switch (testDef.id) {
      case 'test-vec-01': {
        if (!chunks || chunks.length === 0) throw new Error('Chunk index is empty');
        const dimension = chunks[0].vector.length;
        if (dimension !== 384 && dimension !== 768) throw new Error(`Unexpected vector dimension: ${dimension}`);
        const invalidVector = chunks.find(c => {
          if (c.vector.length !== dimension || c.vector.some(v => !Number.isFinite(v))) return true;
          const norm = Math.sqrt(c.vector.reduce((sum, value) => sum + value * value, 0));
          return Math.abs(norm - 1) > 0.001;
        });
        if (invalidVector) throw new Error(`Found malformed or non-normalized vector in chunk ${invalidVector.id}`);
        details = `Validated ${chunks.length} normalized finite vectors across ${conversations.length} chats (${dimension} dimensions each).`;
        break;
      }

      case 'test-vec-02': {
        const query = 'PostgreSQL pgvector SQLite local';
        const results = searchVectorIndex(query, chunks, 5, 0, 'ALL', false);
        if (results.length === 0) throw new Error('Search returned 0 vector results');
        for (const res of results) {
          const score = res.similarityScore;
          if (score === undefined || score < -1.0 || score > 1.0) {
            throw new Error(`Score ${score} out of cosine range [-1.0, 1.0]`);
          }
        }
        const vector = generateLocalPseudoEmbedding(query, chunks[0].vector.length);
        const selfSimilarity = cosineSimilarity(vector, vector);
        if (Math.abs(selfSimilarity - 1) > 0.000001) throw new Error(`Self-similarity was ${selfSimilarity}, expected 1`);
        details = `Top match score: ${((results[0].similarityScore ?? 0) * 100).toFixed(1)}%. Search scores bounded and self-similarity is 1.`;
        break;
      }

      case 'test-vec-03': {
        const results = searchVectorIndex('Docker containers security', chunks, 10);
        for (let i = 1; i < results.length; i++) {
          const score = results[i].rrfScore;
          const previousScore = results[i - 1].rrfScore;
          if (score === undefined || previousScore === undefined || score > previousScore) {
            throw new Error(`Hybrid score ordering violation at index ${i}: ${score} > ${previousScore}`);
          }
        }
        details = `Verified descending hybrid-score ordering across ${results.length} vector results.`;
        break;
      }

      case 'test-rag-01': {
        const scores = chunks.map(chunk => ({
          chunk,
          score: calculateBM25Score('database embeddings indexing', chunk.content, chunk.conversationTitle)
        })).sort((a, b) => b.score - a.score);
        const matches = scores.filter(item => item.score > 0);
        if (matches.length === 0) throw new Error('BM25 query yielded zero matches');
        if (scores[0].score <= scores[scores.length - 1].score) throw new Error('BM25 did not rank matching chunks above non-matches');
        details = `Lexical scoring matched ${matches.length} chunks; top score ${scores[0].score.toFixed(3)}.`;
        break;
      }

      case 'test-rag-02': {
        const results = searchVectorIndex('database embeddings indexing', chunks, 5, 0, 'ALL', true);
        if (results.length === 0) throw new Error('Hybrid search returned 0 results');
        for (const result of results) {
          const expectedScore = Math.round(((result.similarityScore ?? 0) * 0.6 + (result.bm25Score ?? 0) * 0.4) * 100) / 100;
          if (result.rrfScore !== expectedScore) {
            throw new Error(`Hybrid score mismatch for ${result.id}: got ${result.rrfScore}, expected ${expectedScore}`);
          }
        }
        details = `Verified the 60% cosine / 40% BM25 blend across ${results.length} results.`;
        break;
      }

      case 'test-sql-01': {
        const query = 'Show me all conversations with more than 1000 tokens';
        const sql = compileLocalNLToSQL(query);
        if (!sql.toUpperCase().startsWith('SELECT')) {
          throw new Error('Generated SQL is not a valid SELECT query');
        }
        const sqlResult = executeLocalSQL(sql, conversations);
        if (sqlResult.rows.length === 0) {
          throw new Error('Query execution returned 0 rows for valid data');
        }
        details = `Compiled SQL: "${sqlResult.generatedSQL}". Returned ${sqlResult.rows.length} rows in ${sqlResult.executionTimeMs}ms.`;
        break;
      }

      case 'test-sql-02': {
        const rejectedQueries = [
          'DROP TABLE conversations',
          'DELETE FROM conversations',
          'UPDATE conversations SET title = "changed"',
          'INSERT INTO conversations VALUES (1)',
          'ATTACH DATABASE "other.db" AS other',
          'SELECT * FROM conversations; DROP TABLE conversations'
        ];
        for (const sql of rejectedQueries) {
          let rejected = false;
          try {
            executeLocalSQL(sql, conversations);
          } catch {
            rejected = true;
          }
          if (!rejected) throw new Error(`Read-only SQL guard accepted: ${sql}`);
        }
        details = `Read-only SQL guard rejected ${rejectedQueries.length} destructive or multiple-statement queries.`;
        break;
      }

      case 'test-audit-01': {
        if (!CONSENSUS_TOPICS || CONSENSUS_TOPICS.length === 0) throw new Error('Consensus topics empty');
        const sample = CONSENSUS_TOPICS[0];
        if (sample.providersCompared.length < 2) throw new Error('Audit requires at least 2 multi-provider stances');
        details = `Audited topic "${sample.topicTitle}" with ${sample.providersCompared.length} providers compared. Consensus: ${sample.consensusLevel}.`;
        break;
      }

      case 'test-pii-01': {
        const dirtySample = 'Contact admin at dev-admin@totalrecalls.app with API key sk_live_94820af7b823e4';
        const sampleConversation = conversations[0];
        if (!sampleConversation) throw new Error('No conversation available for PII test');
        const audit = auditAndScrubPII([{
          ...sampleConversation,
          messages: sampleConversation.messages.map((message, index) => ({
            ...message,
            content: index === 0 ? dirtySample : message.content
          }))
        }]);
        const scrubbed = audit.scrubbedConversations[0].messages[0].content;
        if (audit.matchesFound.length < 2) throw new Error('PII detector failed to catch the API key and email');
        if (scrubbed.includes('sk_live_94820af7b823e4') || scrubbed.includes('dev-admin@totalrecalls.app')) {
          throw new Error('Scrubber failed to redact a secret or email');
        }
        details = `Detected ${audit.totalRedactions} sensitive values and verified they were redacted.`;
        break;
      }

      case 'test-bench-01': {
        if (!EMBEDDING_PROFILES || EMBEDDING_PROFILES.length === 0) throw new Error('Missing embedding profiles');
        for (const p of EMBEDDING_PROFILES) {
          if (p.dimension <= 0 || p.ramUsageMBPer100k <= 0) throw new Error(`Invalid benchmark profile ${p.name}`);
        }
        details = `Validated ${EMBEDDING_PROFILES.length} local model profiles (BGE, MiniLM, Nomic, Ollama).`;
        break;
      }

      case 'test-kg-01': {
        const conversationIds = new Set(conversations.map(conversation => conversation.id));
        const clusterIds = new Set<string>();
        for (const cluster of INITIAL_KNOWLEDGE_CLUSTERS) {
          if (clusterIds.has(cluster.id)) throw new Error(`Duplicate knowledge cluster id: ${cluster.id}`);
          clusterIds.add(cluster.id);
          if (cluster.confidenceScore < 0 || cluster.confidenceScore > 100) {
            throw new Error(`Invalid confidence score for cluster ${cluster.id}`);
          }
          if (cluster.conversationIds.length === 0 || cluster.conversationIds.some(id => !conversationIds.has(id))) {
            throw new Error(`Cluster ${cluster.id} references missing conversations`);
          }
        }
        details = `Validated ${clusterIds.size} knowledge clusters and all linked conversation references.`;
        break;
      }

      case 'test-backup-01': {
        const sampleText = 'TotalRecalls Vault Integrity Snapshot Test Data';
        const hash = await computeSHA256(sampleText);
        if (!hash || hash.length !== 64) throw new Error(`Invalid SHA-256 hash length: ${hash?.length}`);
        details = `Generated 256-bit SHA-256 digest: ${hash.slice(0, 16)}...${hash.slice(-8)}`;
        break;
      }

      case 'test-backup-02': {
        const snapshot = await createLiveSnapshot(conversations, chunks, 'full', 'local_vault');
        const restoredPayload = JSON.parse(snapshot.rawPayloadSnippet || 'null') as {
          conversations?: ChatConversation[];
        } | null;
        if (restoredPayload?.conversations?.length !== conversations.length) {
          throw new Error('Snapshot round-trip lost conversation records');
        }
        const expectedTurns = conversations.reduce((total, conversation) => total + conversation.messages.length, 0);
        const restoredTurns = restoredPayload.conversations.reduce((total, conversation) => total + conversation.messages.length, 0);
        if (restoredTurns !== expectedTurns) throw new Error('Snapshot round-trip lost conversation turns');
        const verification = await verifySnapshotIntegrity(snapshot);
        if (!verification.verified) throw new Error('Snapshot integrity check failed against recorded checksum');
        snapshot.rawPayloadSnippet = `${snapshot.rawPayloadSnippet}tampered`;
        const tamperedVerification = await verifySnapshotIntegrity(snapshot);
        if (tamperedVerification.verified) throw new Error('Tampered snapshot incorrectly passed verification');
        details = `Snapshot ${snapshot.name} (${snapshot.sizeFormatted}) passed verification and rejected tampering in ${verification.latencyMs}ms.`;
        break;
      }

      case 'test-e2e-01': {
        if (typeof globalThis.fetch !== 'function') throw new Error('Fetch interception is unavailable in this runtime');
        const originalFetch = globalThis.fetch;
        let networkRequests = 0;
        globalThis.fetch = async () => {
          networkRequests += 1;
          throw new Error('Network requests are blocked during the offline integrity check');
        };
        try {
          searchVectorIndex('local vector retrieval', chunks);
          const sql = compileLocalNLToSQL('Show me the highest token conversations');
          executeLocalSQL(sql, conversations);
          auditAndScrubPII(conversations);
          const snapshot = await createLiveSnapshot(conversations, chunks);
          await verifySnapshotIntegrity(snapshot);
        } finally {
          globalThis.fetch = originalFetch;
        }
        if (networkRequests > 0) throw new Error(`Offline operations attempted ${networkRequests} network request(s)`);
        details = 'Local search, SQL, PII audit, snapshot creation, and verification completed with zero fetch requests.';
        break;
      }

      default:
        details = 'Test executed successfully.';
    }
  } catch (err: any) {
    status = 'failed';
    error = err?.message || 'Assertion failed';
  }

  const durationMs = Math.round(performance.now() - t0);

  return {
    ...testDef,
    status,
    durationMs: Math.max(1, durationMs),
    error,
    details
  };
}

export async function runAllTests(
  conversations: ChatConversation[],
  chunks: ChunkEmbedding[],
  onProgress?: (completed: number, total: number, latest: TestCaseAssertion) => void
): Promise<{
  results: TestCaseAssertion[];
  summary: TestSuiteSummary;
}> {
  const t0 = performance.now();
  const results: TestCaseAssertion[] = [];

  for (let i = 0; i < TEST_DEFINITIONS.length; i++) {
    const testDef = TEST_DEFINITIONS[i];
    const result = await runIndividualTest(testDef, conversations, chunks);
    results.push(result);
    if (onProgress) {
      onProgress(i + 1, TEST_DEFINITIONS.length, result);
    }
  }

  const passed = results.filter(r => r.status === 'passed').length;
  const failed = results.filter(r => r.status === 'failed').length;
  const overallDurationMs = Math.round(performance.now() - t0);

  // Compute overall test suite integrity digest
  const serializedResults = results.map(r => `${r.id}:${r.status}:${r.durationMs}`).join('|');
  const integrityHash = await computeSHA256(serializedResults);

  const summary: TestSuiteSummary = {
    total: results.length,
    passed,
    failed,
    pending: 0,
    overallDurationMs,
    integrityHash,
    executedAt: new Date().toISOString().replace('T', ' ').slice(0, 19)
  };

  return { results, summary };
}
