import os
from google import genai

# Load environment variables manually to test if your .env file is mapped correctly
# (Aider does this automatically, but we'll do it explicitly here for verification)
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value.replace('"', '').replace("'", "")

project_id = os.environ.get("VERTEXAI_PROJECT", "tmtwebsite-501119")
location = os.environ.get("VERTEXAI_LOCATION", "us-central1")

print(f"--- Vertex AI Connection Test ---")
print(f"Targeting Project ID : {project_id}")
print(f"Targeting Region     : {location}")

try:
    # 1. Initialize client using Vertex AI credentials
    client = genai.Client(
        vertexai=True,
        project=project_id,
        location=location
    )
    
    print("Sending test prompt to Gemini (gemini-2.5-flash)...")
    
    # 2. Make a fast call to verify the API pipeline
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='Respond with only the words: Connection Successful!'
    )
    
    print("\n[RESULT]")
    print(response.text.strip())
    print("\nSuccess! Your local VS Code environment is communicating perfectly with Vertex AI.")
    print("Any refactoring tasks you perform here will successfully consume your promotional credits.")

except Exception as e:
    print("\n[ERROR] Connection failed.")
    print(f"Details: {e}")
    print("\nTroubleshooting Checklist:")
    print("1. Ensure you ran: gcloud auth application-default login")
    print("2. Ensure the 'Vertex AI API' is enabled in the Google Cloud Console for project tmtwebsite-501119.")
    print("3. Run 'pip install google-genai' to make sure you have the required library.")
