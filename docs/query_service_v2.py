import os
from google.auth import default
from google.cloud.dialogflowcx_v3.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3.types import session
from google.api_core.client_options import ClientOptions

# Force the ambient credentials to resolve to the correct project
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "cs-poc-gw89wethbilefc1wrhgq7d7")
os.environ.setdefault("GCLOUD_PROJECT", "cs-poc-gw89wethbilefc1wrhgq7d7")

def query_agent_adc(user_query, session_id="default-test-session"):
    # Load ADC but pin to the correct project to avoid billing scoping issues
    creds, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

    agent_path = "projects/cs-poc-gw89wethbilefc1wrhgq7d7/locations/us-central1/agents/d8f11aa3-683c-4f06-b015-3e6d9b97f81c"
    session_path = f"{agent_path}/sessions/{session_id}"

    # Pin the client to the us-central1 regional endpoint
    client_options = ClientOptions(
        api_endpoint="us-central1-dialogflow.googleapis.com",
        universe_domain="googleapis.com"
    )
    client = SessionsClient(
        client_options=client_options,
        credentials=creds.with_quota_project("cs-poc-gw89wethbilefc1wrhgq7d7")
        if hasattr(creds, "with_quota_project") else creds,
    )

    query_input = session.QueryInput(
        text=session.TextInput(text=user_query),
        language_code="en"
    )
    request = session.DetectIntentRequest(
        session=session_path,
        query_input=query_input
    )

    try:
        response = client.detect_intent(request=request)
        return response.query_result.response_messages[0].text.text[0]
    except Exception as e:
        return f"Agent API Error: {e}"

if __name__ == "__main__":
    print("Testing Agent API (ADC Auth)...")
    print("Result:", query_agent_adc("Hello"))
