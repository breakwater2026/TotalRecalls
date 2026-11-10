# TotalRecalls Smart Search Engine (SSE) — Installation & Quick-Start Guide

**Product**: TotalRecalls Smart Search Engine (SSE) Add-On  
**Compatibility**: Windows 10 & Windows 11 (64-bit)  
**License Tier**: Add-on for TotalRecalls Downloader Pro  
**Privacy Contract**: 100% Local PC Runtime — Zero Cloud Egress, No Account Required

---

## 1. What You Need Before You Start

1. **TotalRecalls Downloader Pro**:  
   Smart Search Engine is an add-on that indexes your downloaded conversations. You should have TotalRecalls Downloader Pro activated and at least one provider's conversations downloaded.
2. **Your Local Library Folder**:  
   By default, Downloader Pro saves your conversations to:  
   `C:\Users\<YourUsername>\TotalRecalls-download\Library\` (or whatever custom destination folder you selected in TotalRecalls).  
   Inside, you will find dated Markdown (`.md`) and structured (`.json`) files organized by provider (`chatgpt`, `claude`, `perplexity`, etc.).
3. **Your SSE License Key**:  
   Format: `SSE-XXXXXXXX-XXXX-XXXX` (sent in your purchase email).

---

## 2. Quick-Start Installation (3 Steps)

### Step 1: Unzip the Package
Extract the Smart Search Engine archive to any folder on your computer (e.g. `C:\TotalRecalls\SmartSearchEngine\` or on your Desktop).

### Step 2: Launch Smart Search Engine
Launch the application by running the launcher script or executable:
- **Windows**: Double-click `run-smart-search.bat` (or open `index.html` in Microsoft Edge / Chrome).
- The application will initialize your local vector and relational database in memory.

### Step 3: Activate Your License Key
1. In the top-right corner of the interface, look at the license status bar.
2. Click **Activate SSE Key** (or **Manage SSE License**).
3. Paste your `SSE-XXXXXXXX-XXXX-XXXX` license key from your purchase email into the input field.
4. Click **Activate SSE**.
5. The status pill will switch to **`SSE Licensed`** (verified against `https://totalrecalls.app/api/licenses/verify`).
   *(Note: Activation contacts the license server once to register your machine; after that, all searches, vector indexing, and SQL queries run 100% offline on your PC).*

---

## 3. How to Use Smart Search Engine

### A. Tri-Mode Search
- **By Meaning (Semantic Vector)**: Finds conversations based on concepts, themes, and conceptual answers even if the exact keywords were never used.
- **By Keyword (Exact Lexical)**: Finds exact model names, code snippets, dates, error codes, and unique strings.
- **Hybrid (RAG)**: Blends vector similarity (60%) with lexical BM25 matching (40%) for the most accurate recall.

### B. Natural Language to SQL
Ask analytical questions in plain English, such as:
- *"Which provider did I talk to most in October?"*
- *"Show conversations with more than 50 messages about Python."*
The engine compiles your question into read-only SQLite SQL and renders the results as structured tables.

### C. Offline Privacy & Security Guarantee
- **No telemetry**: Your search queries, conversation excerpts, and embeddings never leave your device.
- **Direct file links**: Every result links straight to the underlying `.md` or `.json` file on your local disk.

---

## 4. Troubleshooting & Support

- **"Wrong Product" Error on Activation**:  
  Ensure you are using the `SSE-` key in the Smart Search Engine, and the `TR-` key in Downloader Pro. Keys are module-scoped.
- **Activation Limit**:  
  Each key permits activation on up to **3 of your own devices**. You can click **Deactivate (free slot)** before switching PCs to free an activation slot.
- **Need help or key recovery?**  
  Email **`support@totalrecalls.app`** with your Paddle transaction ID (`txn_...`) and we will assist you directly.
