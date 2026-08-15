import os
import google.auth
from google.cloud import discoveryengine_v1 as de

PROJECT_NUMBER = "96283906207"
LOCATION = "us"
ENGINE_ID = "d8f11aa3-683c-4f06-b015-3e6d9b97f81c-chat-1786557476"

ENGINE_NAME = (
    f"projects/{PROJECT_NUMBER}/locations/{LOCATION}/"
    f"collections/default_collection/engines/{ENGINE_ID}"
)

# Use ambient creds, forced to bill the correct project.
base, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
creds = base.with_quota_project("cs-poc-gw89wethbilefc1wrhgq7d7") if hasattr(base, "with_quota_project") else base

client_options = {"api_endpoint": f"{LOCATION}-discoveryengine.googleapis.com"}
conv_client = de.ConversationalSearchServiceClient(client_options=client_options, credentials=creds)

# The conversation resource path for a chat engine
conversation_name = f"{ENGINE_NAME}/conversations/default-conversation"

request = de.ConverseConversationRequest(
    name=conversation_name,
    query=de.TextInput(input="What is TotalRecalls?"),
    serving_config=f"{ENGINE_NAME}/servingConfigs/default_search",
)

print("=== Calling converse_conversation (chat API) ===")
try:
    response = conv_client.converse_conversation(request=request)
    print("OK. Reply:", response.reply.reply[:400])
except Exception as e:
    print("FAILED:", e)
