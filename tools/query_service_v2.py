import os
# Force the SDK to use the correct project before any import loads creds
os.environ["GOOGLE_CLOUD_PROJECT"] = "cs-poc-gw89wethbilefc1wrhgq7d7"
os.environ["GCLOUD_PROJECT"] = "cs-poc-gw89wethbilefc1wrhgq7d7"

import google.auth
from google.cloud.dialogflowcx_v3.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3.types import session

def query_agent(user_query, session_id="default-test-session"):
    agent_path = "projects/cs-poc-gw89wethbilefc1wrhgq7d7/locations/us-central1/agents/d8f11aa3-683c-4f06-b015-3e6d9b97f81c"
    session_path = f"{agent_path}/sessions/{session_id}"
    
    client_options = {"api_endpoint": "us-central1-dialogflow.googleapis.com"}
    client = SessionsClient(client_options=client_options)
    
    text_input = session.TextInput(text=user_query)
    query_input = session.QueryInput(text=text_input, language_code="en")
    request = session.DetectIntentRequest(session=session_path, query_input=query_input)
    
    try:
        response = client.detect_intent(request=request)
        response_text = response.query_result.response_messages[0].text.text[0]
        return response_text
    except Exception as e:
        return f"Agent API Error: {e}"

if __name__ == "__main__":
    print("Testing Agent API...")
    print("Result:", query_agent("Hello"))
