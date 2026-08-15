import os
from google.auth import default
from google.cloud.dialogflowcx_v3.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3.types import session

def query_agent_adc(user_query, session_id="default-test-session"):
    # 1. Automatically load the environment's credentials (no file needed!)
    # This works in Cloud Shell and Cloud Run automatically.
    creds, _ = default()

    agent_path = "projects/cs-poc-gw89wethbilefc1wrhgq7d7/locations/us-central1/agents/d8f11aa3-683c-4f06-b015-3e6d9b97f81c"
    session_path = f"{agent_path}/sessions/{session_id}"

    client_options = {"api_endpoint": "us-central1-dialogflow.googleapis.com"}
    client = SessionsClient(client_options=client_options, credentials=creds)

    query_input = session.QueryInput(text=session.TextInput(text=user_query), language_code="en")
    request = session.DetectIntentRequest(session=session_path, query_input=query_input)

    try:
        response = client.detect_intent(request=request)
        return response.query_result.response_messages[0].text.text[0]
    except Exception as e:
        return f"Agent API Error: {e}"

if __name__ == "__main__":
    print("Testing Agent API (ADC Auth)...")
    print("Result:", query_agent_adc("Hello"))