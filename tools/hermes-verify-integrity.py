import os
import tempfile

# --- Ad-hoc verification script for query_service & ingest_service ---
VERIFY_OK = True
SUMMARY = []

def log(msg):
    SUMMARY.append(msg)
    print(msg)

# Fix the file-read bug: read content *before* closing.
file_content = "This is a test document for Hermes verification."
tmp_path = r"C:\Users\break\AppData\Local\Temp\hermes-verify-test.txt"
with open(tmp_path, "w", encoding="utf-8") as tmp:
    tmp.write(file_content)

try:
    log("[VERIFY] Checking query_service (standard Search API)...")
    from query_service import query_data_store

    snippets = query_data_store("test")
    if isinstance(snippets, list):
        log(f"[VERIFY]   Query returned {len(snippets)} snippet(s). Wiring confirmed.")
    else:
        log(f"[VERIFY-BLOCKER] Unexpected query output type: {type(snippets)}")
        VERIFY_OK = False

    log("[VERIFY] Checking ingest_service with a temporary document...")
    from ingest_service import ingest_file_to_datastore

    try:
        ingest_file_to_datastore(tmp_path, file_content)
        log("[VERIFY]   Temporary document ingestion call completed.")
    except Exception as e:
        err = str(e)
        if "ALREADY_EXISTS" in err or "already exists" in err.lower():
            log("[VERIFY]   Document already exists (expected on re-runs).")
        elif "INVALID_ARGUMENT" in err or "id" in err.lower():
            log("[VERIFY-BLOCKER] Document ID format rejected.")
            log(f"[VERIFY-BLOCKER] Error: {e}")
            VERIFY_OK = False
        else:
            log(f"[VERIFY-BLOCKER] Ingestion raised an error: {e}")
            VERIFY_OK = False

    log("\n=== VERIFICATION SUMMARY ===")
    if VERIFY_OK:
        log("SUCCESS: query_service and ingest_service paths verified.")
        log("NOTE: Standard search works. Conversational LLM requires explicit Vertex AI add-on enablement.")
    else:
        log("FAILURE: One or more code paths failed.")

finally:
    try:
        os.unlink(tmp_path)
    except OSError:
        pass
