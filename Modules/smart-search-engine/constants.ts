import { ChatConversation, AIProvider, ConsensusTopic, EmbeddingEngineProfile, PersonaConfig, SavedSQLView, KnowledgeTopicCluster, PricingTier } from './types';

export const INITIAL_CONVERSATIONS: ChatConversation[] = [
  {
    id: 'tr-conv-101',
    title: 'PostgreSQL Vector Extension (pgvector) Schema Design & Indexing',
    provider: 'ChatGPT',
    model: 'gpt-4o',
    createdAt: '2024-10-14 09:30',
    updatedAt: '2024-10-14 10:15',
    tags: ['database', 'vector-search', 'postgres', 'hnsw'],
    messageCount: 4,
    totalTokens: 1420,
    isIndexed: true,
    messages: [
      {
        id: 'm-101-1',
        role: 'user',
        content: 'How should I structure a local SQLite or PostgreSQL table to store embeddings alongside conversation chunks with HNSW or IVFFlat indexes? Contact dev-admin@totalrecalls.app with the db secret sk_live_94820af7b823e4',
        timestamp: '2024-10-14 09:30',
        tokenCount: 42
      },
      {
        id: 'm-101-2',
        role: 'assistant',
        content: `To build an efficient local RAG vector store, define a \`chat_chunks\` table with schema:
\`\`\`sql
CREATE TABLE chat_embeddings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id VARCHAR(64) NOT NULL,
  provider VARCHAR(32) NOT NULL,
  chunk_text TEXT NOT NULL,
  embedding vector(768),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_chat_hnsw ON chat_embeddings USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);
\`\`\`
For SQLite, use the sqlite-vec extension or in-memory cosine array calculations for zero-dependency local speed.`,
        timestamp: '2024-10-14 09:31',
        tokenCount: 480
      },
      {
        id: 'm-101-3',
        role: 'user',
        content: 'What is the memory footprint and latency difference between cosine distance vs inner product on 1536-dim or 768-dim embeddings?',
        timestamp: '2024-10-14 09:42',
        tokenCount: 38
      },
      {
        id: 'm-101-4',
        role: 'assistant',
        content: '768-dimensional float32 vectors take 3.072 KB per row. For 100,000 chunks, that is ~307 MB RAM. Inner product (dot product) runs 1.8x faster on SIMD AVX2 architectures when vectors are pre-normalized to unit length (L2 norm = 1.0), as it avoids computing square root denominators during query time.',
        timestamp: '2024-10-14 09:44',
        tokenCount: 860
      }
    ]
  },
  {
    id: 'tr-conv-102',
    title: 'Stripe Billing Webhook Idempotency & Refund Architecture',
    provider: 'Claude',
    model: 'claude-3-5-sonnet',
    createdAt: '2024-10-18 14:10',
    updatedAt: '2024-10-18 15:02',
    tags: ['stripe', 'webhooks', 'security', 'payments', 'idempotency'],
    messageCount: 4,
    totalTokens: 2150,
    isIndexed: true,
    messages: [
      {
        id: 'm-102-1',
        role: 'user',
        content: 'Design an idempotent webhook handler in Node.js for Stripe checkout.session.completed and customer.subscription.deleted events. Ensure no duplicate license keys are generated if Stripe retries delivery.',
        timestamp: '2024-10-18 14:10',
        tokenCount: 36
      },
      {
        id: 'm-102-2',
        role: 'assistant',
        content: `Store received \`event.id\` in an ACID transactions table with a \`processed_at\` timestamp and UNIQUE constraint:
\`\`\`sql
CREATE TABLE processed_webhook_events (
  event_id VARCHAR(64) PRIMARY KEY,
  event_type VARCHAR(64) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
\`\`\`
Before granting the lifetime or annual license in your DB, perform \`INSERT INTO processed_webhook_events(event_id, event_type) VALUES (?, ?) ON CONFLICT DO NOTHING RETURNING event_id;\`. If no row is returned, return an immediate HTTP 200 to Stripe without executing the issuance logic again.`,
        timestamp: '2024-10-18 14:12',
        tokenCount: 650
      },
      {
        id: 'm-102-3',
        role: 'user',
        content: 'How should 7-day money-back guarantee refunds be handled for desktop app licenses that validate offline?',
        timestamp: '2024-10-18 14:35',
        tokenCount: 28
      },
      {
        id: 'm-102-4',
        role: 'assistant',
        content: 'For offline desktop apps, use short-lived cryptographically signed license leases (e.g., 14-day signed JWTs). When a refund occurs (charge.refunded webhook), record the revoked license key on a lightweight public revocation CRL / OCSP endpoint. When the app connects to check for updates or scrape new chats, it refreshes the lease. If revoked, the app gracefully degrades to the free read-only viewer.',
        timestamp: '2024-10-18 14:38',
        tokenCount: 1436
      }
    ]
  },
  {
    id: 'tr-conv-103',
    title: 'Local LLM Inference Optimization: Ollama, Docker, & GPU Passthrough',
    provider: 'Gemini',
    model: 'gemini-1.5-pro',
    createdAt: '2024-10-22 11:00',
    updatedAt: '2024-10-22 11:45',
    tags: ['ollama', 'docker', 'gpu', 'docker-compose', 'cuda'],
    messageCount: 4,
    totalTokens: 1890,
    isIndexed: true,
    messages: [
      {
        id: 'm-103-1',
        role: 'user',
        content: 'Write a docker-compose.yml file to spin up Ollama with NVIDIA GPU acceleration alongside Open-WebUI and an embedding microservice for nomic-embed-text.',
        timestamp: '2024-10-22 11:00',
        tokenCount: 34
      },
      {
        id: 'm-103-2',
        role: 'assistant',
        content: `Here is the production Docker Compose setup with NVIDIA container toolkit reservation:
\`\`\`yaml
services:
  ollama:
    image: ollama/ollama:latest
    container_name: totalrecalls-ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_storage:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
\`\`\`
This enables local embeddings at 800+ tokens/second with zero external API calls.`,
        timestamp: '2024-10-22 11:02',
        tokenCount: 520
      },
      {
        id: 'm-103-3',
        role: 'user',
        content: 'Can nomic-embed-text run directly in WebAssembly or WebGPU in modern Chromium browsers without a native backend daemon?',
        timestamp: '2024-10-22 11:20',
        tokenCount: 26
      },
      {
        id: 'm-103-4',
        role: 'assistant',
        content: 'Yes! Using ONNX Runtime Web with the WebGPU execution provider, quantized Q4 or Q8 models of all-MiniLM-L6-v2 and nomic-embed-text-v1.5 can execute in-browser at 45ms per query chunk, requiring zero external terminal daemon or background Python service.',
        timestamp: '2024-10-22 11:22',
        tokenCount: 1310
      }
    ]
  },
  {
    id: 'tr-conv-104',
    title: 'TotalRecalls Q3 Growth Metrics, Conversion Rates & Scraper Telemetry',
    provider: 'Perplexity',
    model: 'sonar-medium',
    createdAt: '2024-10-28 16:15',
    updatedAt: '2024-10-28 16:50',
    tags: ['metrics', 'telemetry', 'analytics', 'conversion', 'q3-figures'],
    messageCount: 4,
    totalTokens: 1650,
    isIndexed: true,
    messages: [
      {
        id: 'm-104-1',
        role: 'user',
        content: 'Compile the TotalRecalls Q3 export telemetry. What percentage of users export from ChatGPT vs Claude vs Gemini, and what is the median vault size?',
        timestamp: '2024-10-28 16:15',
        tokenCount: 32
      },
      {
        id: 'm-104-2',
        role: 'assistant',
        content: 'Based on sanitized opt-in release telemetry from totalrecalls.app:\n- ChatGPT accounts for 58.4% of all local archive volume\n- Claude represents 24.1% of volume (with the highest avg tokens per conversation at 3,840)\n- Gemini accounts for 11.2%\n- Perplexity accounts for 6.3%\nMedian local user vault contains 420 conversations, 4.8 million tokens, occupying approximately 32 MB of disk in compressed SQLite storage.',
        timestamp: '2024-10-28 16:17',
        tokenCount: 480
      },
      {
        id: 'm-104-3',
        role: 'user',
        content: 'What is our trial-to-paid conversion rate for TotalRecalls Pro vs the Smart Search Engine add-on?',
        timestamp: '2024-10-28 16:30',
        tokenCount: 25
      },
      {
        id: 'm-104-4',
        role: 'assistant',
        content: 'The downloader converts at 4.2% from free download to TotalRecalls Pro ($24 launch price). In user surveys, 78% of active users stated they would pay an additional $29 for the Smart Search Engine add-on if they could instantly search across all providers using semantic vectors and natural language SQL, projecting a 2.1x expansion in Average Revenue Per User (ARPU).',
        timestamp: '2024-10-28 16:32',
        tokenCount: 1113
      }
    ]
  },
  {
    id: 'tr-conv-105',
    title: 'Local-Only Architecture & Local SQLite Vector Extensions',
    provider: 'Mistral',
    model: 'mistral-large-2',
    createdAt: '2024-11-01 08:45',
    updatedAt: '2024-11-01 09:20',
    tags: ['local-only', 'sqlite-vec', 'privacy', 'c-extension', 'local-models'],
    messageCount: 4,
    totalTokens: 1980,
    isIndexed: true,
    messages: [
      {
        id: 'm-105-1',
        role: 'user',
        content: 'How does TotalRecalls keep my chats local so security teams can audit network sockets?',
        timestamp: '2024-11-01 08:45',
        tokenCount: 30
      },
      {
        id: 'm-105-2',
        role: 'assistant',
        content: 'TotalRecalls runs on your PC. Nothing you write or save is uploaded. The only internet use is a one-time search-model download during setup; once your conversations are downloaded, search works without an internet connection.\n\nFor security audits:\n1. Run the embedding generator in-process using embedded C/C++ or WebAssembly bindings\n2. Use SQLite in local single-file mode (`totalrecalls_vault.db`) with PRAGMA key encryption\n3. Provide Wireshark / Little Snitch verification steps in the Power User documentation to confirm no chat content is transmitted during search and RAG synthesis.',
        timestamp: '2024-11-01 08:47',
        tokenCount: 560
      },
      {
        id: 'm-105-3',
        role: 'user',
        content: 'How does sqlite-vec compare with chromadb or milvus for single-user local storage on macOS and Windows?',
        timestamp: '2024-11-01 09:05',
        tokenCount: 24
      },
      {
        id: 'm-105-4',
        role: 'assistant',
        content: 'Chroma and Milvus require Python runtimes, background daemon processes, and large memory allocations (often 400MB+ idle). SQLite-vec is a pure compiled C dynamic extension that embeds directly into the existing database file. It has zero daemon overhead, instant cold start (<5ms), and transactional ACID safety alongside standard SQL tables.',
        timestamp: '2024-11-01 09:07',
        tokenCount: 1366
      }
    ]
  }
];

export const CONSENSUS_TOPICS: ConsensusTopic[] = [
  {
    id: 'ct-vector-db',
    topicTitle: 'Optimal Local Vector Store Architecture (SQLite-vec vs pgvector)',
    category: 'Architecture',
    summary: 'Comparing lightweight in-process embedded storage against full relational servers for 100k+ conversation chunks.',
    consensusLevel: 'High',
    providersCompared: [
      {
        provider: 'ChatGPT',
        stance: 'Recommends SQLite with sqlite-vec or in-memory arrays for desktop apps; pgvector for team servers.',
        keySnippet: 'For single-user local speed, avoid background daemons. Use sqlite-vec or in-memory SIMD dot products.',
        conversationId: 'tr-conv-101',
        sentimentScore: 94
      },
      {
        provider: 'Mistral',
        stance: 'Firmly advocates embedded SQLite-vec over standalone Chroma/Milvus to eliminate Python daemon dependencies.',
        keySnippet: 'SQLite-vec is a pure compiled C extension: zero daemon overhead, <5ms cold start, and full ACID safety.',
        conversationId: 'tr-conv-105',
        sentimentScore: 98
      },
      {
        provider: 'Gemini',
        stance: 'Proposes ONNX Runtime Web with WebGPU in-browser for zero-native-daemon embedding generation.',
        keySnippet: 'ONNX Web with WebGPU executes at 45ms per chunk without requiring a local background daemon.',
        conversationId: 'tr-conv-103',
        sentimentScore: 88
      }
    ],
    divergenceNotes: 'All 3 models agree that heavy standalone vector services (Milvus, Pinecone, Chroma daemons) are wrong for local desktop tools. Slight nuance between pure C SQLite extension vs in-browser WebGPU runtime.',
    recommendedAction: 'Adopt SQLite with sqlite-vec as default local engine, with WebAssembly fallback for zero-install browser mode.'
  },
  {
    id: 'ct-license-refunds',
    topicTitle: 'Offline Desktop License Keys & Idempotent Webhook Processing',
    category: 'Security & Payments',
    summary: 'Balancing local-only user privacy with 7-day refund revocation and idempotent order fulfillment.',
    consensusLevel: 'Complementary',
    providersCompared: [
      {
        provider: 'Claude',
        stance: 'Suggests cryptographically signed 14-day JWT leases with CRL endpoints checked only on scrape refresh.',
        keySnippet: 'Use short-lived signed JWTs. Check revocation only when user scrapes new chats or checks updates.',
        conversationId: 'tr-conv-102',
        sentimentScore: 92
      },
      {
        provider: 'Perplexity',
        stance: 'Highlights user willingness to pay one-time ($24 Pro / $29 SSE add-on) over monthly subscriptions for local privacy tools.',
        keySnippet: 'Survey data shows 78% of privacy users prefer one-time licenses over monthly recurring SaaS.',
        conversationId: 'tr-conv-104',
        sentimentScore: 85
      }
    ],
    divergenceNotes: 'Claude focuses on the technical cryptographic CRL revocation; Perplexity focuses on customer psychology favoring one-time licenses.',
    recommendedAction: 'Implement asymmetric ED25519 offline license keys with opt-in lease refresh only when downloading new chats.'
  },
  {
    id: 'ct-privacy-local',
    topicTitle: 'Local-Only Verification & Network Socket Auditing',
    category: 'Local AI & DevOps',
    summary: 'Techniques for proving to enterprise security auditors that chat data stays on the local workstation.',
    consensusLevel: 'High',
    providersCompared: [
      {
        provider: 'Mistral',
        stance: 'Recommends OS-level socket sandboxing, PRAGMA key encryption, and publishing Wireshark packet capture guides.',
        keySnippet: 'Provide Wireshark and Little Snitch verification steps in Power User docs showing no chat content is transmitted.',
        conversationId: 'tr-conv-105',
        sentimentScore: 96
      },
      {
        provider: 'Gemini',
        stance: 'Emphasizes containerized isolation or purely local WebGPU models to ensure hardware-level isolation.',
        keySnippet: 'Quantized Q4/Q8 models run locally with no cloud dependency.',
        conversationId: 'tr-conv-103',
        sentimentScore: 90
      }
    ],
    divergenceNotes: 'Both reinforce local-only operation. Mistral gives concrete network inspection tools (Wireshark), Gemini gives execution runtime recommendations.',
    recommendedAction: 'Include the Wireshark and Little Snitch verification walkthrough directly in the Power User Manual.'
  }
];

export const EMBEDDING_PROFILES: EmbeddingEngineProfile[] = [
  {
    id: 'nomic-embed-text',
    name: 'Nomic Embed Text v1.5 (Local)',
    dimension: 768,
    quantization: 'INT8',
    latencyPer1kTokensMs: 42,
    ramUsageMBPer100k: 78,
    provider: 'Local / Ollama',
    description: 'High-accuracy general semantic embedding optimized for technical code, Markdown, and conversational text. Runs locally via Ollama or llama.cpp.'
  },
  {
    id: 'all-minilm-l6-v2',
    name: 'All-MiniLM-L6-v2 (WASM / In-Browser)',
    dimension: 384,
    quantization: 'Q4',
    latencyPer1kTokensMs: 18,
    ramUsageMBPer100k: 32,
    provider: 'WASM / Browser',
    description: 'Ultralight embedded model executing in pure WebAssembly or WebGPU. Zero native binary dependencies, runs on any laptop or browser tab.'
  },
  {
    id: 'bge-small-en-v1.5',
    name: 'BAAI BGE Small EN v1.5 (Local CPU)',
    dimension: 512,
    quantization: 'FP16',
    latencyPer1kTokensMs: 29,
    ramUsageMBPer100k: 54,
    provider: 'Local / Ollama',
    description: 'Leader on the MTEB retrieval benchmark for query-to-chunk matching. Ideal balance of compact vector size and nuanced conceptual recall.'
  },
  {
    id: 'gemini-text-embedding-004',
    name: 'Gemini Text-Embedding-004 (Cloud Opt-In)',
    dimension: 768,
    quantization: 'FP32',
    latencyPer1kTokensMs: 110,
    ramUsageMBPer100k: 96,
    provider: 'Cloud Gemini',
    description: 'Cloud API option for users desiring frontier Google embedding precision without running local GPU hardware. Requires user API key.'
  }
];

export const PERSONA_CONFIGS: PersonaConfig[] = [
  {
    id: 'balanced',
    name: 'Balanced Synthesis',
    description: 'Comprehensive, accurate summary with provider attribution and key context.',
    instruction: 'Provide a structured, helpful synthesis of the retrieved chat chunks. Cite which AI said what.',
    icon: 'Sparkles'
  },
  {
    id: 'executive',
    name: 'Executive Briefing',
    description: 'High-level bullet points, bottom-line takeaways, and strategic action items.',
    instruction: 'Be concise, executive, and decisive. Extract bottom-line takeaways, key metrics, and recommended decisions.',
    icon: 'TrendingUp'
  },
  {
    id: 'code_extractor',
    name: 'Code & Schema Extractor',
    description: 'Filters out chat commentary to surface exact code snippets, SQL schemas, and config files.',
    instruction: 'Extract only clean, runnable code blocks, configuration files, and SQL schemas from the retrieved chunks. Omit polite conversational prose.',
    icon: 'FileCode'
  },
  {
    id: 'fact_checker',
    name: 'Fact-Check & Discrepancies',
    description: 'Audits conflicting advice, hallucinations, or divergent parameters between models.',
    instruction: 'Act as a skeptical technical reviewer. Explicitly compare answers across AI models and highlight contradictions, outdated advice, or unverified claims.',
    icon: 'ShieldCheck'
  }
];

// Alias exports for backward compatibility across modules
export const PERSONA_PROFILES = PERSONA_CONFIGS;
export const INITIAL_CONSENSUS_TOPICS = CONSENSUS_TOPICS;

export const SAVED_SQL_VIEWS: SavedSQLView[] = [
  {
    id: 'v-provider-summary',
    title: 'Provider Token & Chat Volume Summary',
    description: 'Total token consumption and conversation count aggregated across every synced AI provider.',
    category: 'performance',
    sql: 'SELECT provider, COUNT(*) AS chat_count, SUM(total_tokens) AS total_tokens, ROUND(AVG(total_tokens)) AS avg_tokens FROM conversations GROUP BY provider ORDER BY total_tokens DESC;'
  },
  {
    id: 'v-largest-chats',
    title: 'Top 5 Most Expensive Conversations',
    description: 'Rank conversations with the highest token count to identify dense knowledge threads.',
    category: 'tokens',
    sql: 'SELECT title, provider, model, total_tokens, message_count FROM conversations ORDER BY total_tokens DESC LIMIT 5;'
  },
  {
    id: 'v-code-heavy',
    title: 'Chats with Code Blocks & SQL Schemas',
    description: 'Finds conversations discussing databases, docker, or payment integrations.',
    category: 'topics',
    sql: "SELECT id, title, provider, model, tags FROM conversations WHERE tags LIKE '%postgres%' OR tags LIKE '%docker%' OR tags LIKE '%stripe%';"
  },
  {
    id: 'v-recent-turns',
    title: 'Relational Message Turn Inspection',
    description: 'Foreign-key join linking individual message turns with their parent conversation title.',
    category: 'performance',
    sql: 'SELECT id, conversation_title, provider, role, token_count, timestamp FROM messages ORDER BY timestamp DESC LIMIT 8;'
  }
];

export const INITIAL_KNOWLEDGE_CLUSTERS: KnowledgeTopicCluster[] = [
  {
    id: 'kc-vector-dbs',
    name: 'Local Vector Stores & Indexing',
    category: 'Data & Search',
    conversationIds: ['tr-conv-101', 'tr-conv-105'],
    totalTokens: 3400,
    turnCount: 8,
    topKeywords: ['hnsw', 'sqlite-vec', 'pgvector', 'inner product', 'cosine'],
    lastUpdated: '2024-11-01',
    confidenceScore: 96,
    summary: 'Detailed implementation guides comparing SQLite sqlite-vec zero-daemon local operation versus PostgreSQL pgvector for enterprise concurrency.'
  },
  {
    id: 'kc-devops-gpu',
    name: 'Dockerized Local LLMs & WebGPU',
    category: 'Infrastructure',
    conversationIds: ['tr-conv-103'],
    totalTokens: 1890,
    turnCount: 4,
    topKeywords: ['ollama', 'docker', 'cuda', 'nomic-embed-text', 'llama-3.2'],
    lastUpdated: '2024-10-22',
    confidenceScore: 91,
    summary: 'Containerized Ollama setups with NVIDIA GPU passthrough for local embedding generation at 800 tokens/sec.'
  },
  {
    id: 'kc-billing-stripe',
    name: 'SaaS Billing & Webhook Idempotency',
    category: 'Security & Commerce',
    conversationIds: ['tr-conv-102'],
    totalTokens: 2150,
    turnCount: 4,
    topKeywords: ['stripe', 'webhooks', 'idempotency', 'refunds', 'jwt-seats'],
    lastUpdated: '2024-10-18',
    confidenceScore: 98,
    summary: 'Idempotent webhook handlers, HMAC signature verification, and automated 7-day refund license deactivation logic.'
  },
  {
    id: 'kc-telemetry-sales',
    name: 'Product Growth & Export Metrics',
    category: 'Analytics',
    conversationIds: ['tr-conv-104'],
    totalTokens: 1650,
    turnCount: 4,
    topKeywords: ['q3-figures', 'mac-dmg', 'conversion', 'chatgpt-share', 'arr'],
    lastUpdated: '2024-10-28',
    confidenceScore: 89,
    summary: 'Quarterly download distributions showing 62% macOS DMG vs 38% Windows MSI, with ChatGPT being the #1 exported chat source.'
  }
];

export const TOTALRECALLS_SPECS = {
  version: '2.5.0-MarketLeader',
  productName: 'TotalRecalls Local AI Chat Suite',
  proUnit: 'TotalRecalls Pro — Universal AI Chat Downloader (ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, Qwen)',
  addonUnit: 'Smart Search Engine add-on',
  supportedProviders: ['ChatGPT', 'Claude', 'Perplexity', 'Gemini', 'Grok', 'DeepSeek', 'Mistral', 'Qwen'] as AIProvider[],
  embeddingModels: EMBEDDING_PROFILES,
  pricingTiers: [
    {
      name: 'Downloader Pro',
      price: '$24',
      regularPrice: '$48',
      period: 'one-time (regular $48)',
      badge: 'Downloader',
      cta: 'Explore feature set',
      subtitle: 'All 8 providers · unlimited downloads · Markdown + JSON, saved locally',
      features: [
        'All 8 providers: ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, Qwen',
        'Unlimited downloads',
        'Markdown and JSON files, saved locally',
        'Up to 3 device activations',
        'Free updates (bug fixes) for the life of the product',
        'License key delivered by email',
      ],
    },
    {
      name: 'Smart Search Engine',
      price: '$29',
      regularPrice: '$58',
      period: 'one-time (regular $58)',
      badge: 'SSE add-on',
      featured: true,
      cta: 'Open Smart Search demo',
      subtitle: 'Semantic search across your local archive · Obsidian and Notion connections',
      features: [
        'Search by meaning, keyword, or both together',
        'Plain-English questions answered with SQL',
        'Every result links to the original file',
        'Obsidian and Notion connections',
        'Automatic re-indexing',
        'Free updates (bug fixes) to SSE',
        'New modules and upgrades are separate purchases',
      ],
    },
    {
      name: 'Pro + SSE bundle',
      price: '$49.89',
      regularPrice: '$99.89',
      period: 'one-time (regular $99.89)',
      badge: 'Best value',
      cta: 'Open Smart Search demo',
      subtitle: 'TotalRecalls Pro and the Smart Search Engine together',
      features: [
        'All 8 providers, unlimited downloads',
        'Smart Search Engine semantic search',
        'Obsidian and Notion connections',
        'Up to 3 device activations',
        'Free updates (bug fixes) to both',
      ],
    },
  ] as PricingTier[]
};
