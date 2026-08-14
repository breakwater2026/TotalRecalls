# GCP Credit-Compliant Architecture Implementation

**Project ID:** `cs-poc-gw89wethbilefc1wrhgq7d7`  
**Region:** `us-central1`  
**Promotional Credit:** GenAI App Builder Trial Credit (Credit ID: `6b0ed804949b4d7aea4d9e7116fe67d469cbf24a6c28994288d1dc1ae632103b`)

---

## Architecture Overview (Approved Design)

To ensure all AI reasoning and retrieval operations draw 100% from your remaining GenAI App Builder credits (bypassing direct Gemini API studio charges), we implement the approved **Backend-for-Frontend (BFF) RAG Architecture**:

```
+--------------------------------------------------------------------------+
|                       Global HTTP(S) Load Balancer                       |
|                   (rag-ingress-lb-frontend / backend)                    |
+--------------------------------------------------------------------------+
                                     │
                                     ▼
+--------------------------------------------------------------------------+
|                               Cloud Run                                  |
|                            (rag-app-tier)                                |
|             - Hosts TotalRecalls Web Frontend & Backend API              |
+--------------------------------------------------------------------------+
                     │                                │
                     │ (Grounded Search / RAG)        │ (Asset Storage)
                     ▼                                ▼
+------------------------------------------+  +----------------------------+
|        Vertex AI Agent Engine            |  |    Cloud Storage Bucket    |
|            (rag-agent-engine)            |  |      (rag-gcs-bucket)      |
|    - Agent Builder / Search & Conv.      |  | - Markdown/JSON Doc Store  |
|    - Grounded Generation API             |  | - User Export Documents    |
+------------------------------------------+  +----------------------------+
```

---

## Credible SKUs & Activities
1. **Vertex AI Search / Data Store:** Indexing and querying documents stored in GCS.
2. **Vertex AI Conversation / Agent Builder:** Hosting agent runtimes and managing multi-turn session state.
3. **Grounded Generation API (RAG):** Anchoring Gemini model generations strictly to your indexed data source.

---

## Implementation Steps

### 1. Provision GCS Grounding Asset Bucket
```bash
python deploy/gcp-credit-architecture/setup_agent_engine.py
```

### 2. Configure Cloud Run Backend (`rag-app-tier`)
In your Cloud Run backend service, replace direct raw model calls with the **Vertex AI Discovery Engine / Agent Builder API** (`discoveryengine.googleapis.com`). This ensures the API call routes through the creditable Agent Engine RAG pipeline.

### 3. Verification
Verify in the Google Cloud Billing console that all AI operations log under **Vertex AI Search and Conversation** SKUs rather than Vertex AI Studio model predictions.
