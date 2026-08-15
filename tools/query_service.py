import os
from google.cloud import discoveryengine_v1 as de

# Constants
PROJECT_NUMBER = "96283906207"       # numeric; API returned name uses this form
LOCATION = "us"
# Real Engine ID surfaced by list_engines2.py (fronts the Website data store)
ENGINE_ID = "d8f11aa3-683c-4f06-b015-3e6d9b97f81c-chat-1786557476"

# Per Google's error, standard edition must be addressed at the engine level.
ENGINE_NAME = (
    f"projects/{PROJECT_NUMBER}/locations/{LOCATION}/"
    f"collections/default_collection/engines/{ENGINE_ID}"
)
SERVING_CONFIG = f"{ENGINE_NAME}/servingConfigs/default_search"

def get_client():
    client_options = {"api_endpoint": f"{LOCATION}-discoveryengine.googleapis.com"}
    return de.SearchServiceClient(client_options=client_options)

def query_data_store(user_query):
    """
    Queries the Vertex AI Search *engine* (which fronts your standard
    Website data store) for snippets. Returns a list of text snippets
    you can render in your app.

    Uses the standard Search API on the engine-level serving config so it
    works with the standard (non-enterprise) edition of your data store.
    """
    client = get_client()
    request = de.SearchRequest(
        serving_config=SERVING_CONFIG,
        query=user_query,
        page_size=5,
    )
    response = client.search(request=request)
    return [r.snippet for r in response.results if r.snippet]

# --- Example of your API usage (e.g., in /api/export) ---
# @app.post("/api/export")
# def handle_export():
#     user_prompt = request.json.get("query")
#     answer = query_data_store(user_prompt)
#     return {"response": answer}
