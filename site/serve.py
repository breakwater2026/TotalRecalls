"""Static file server + API proxy for the TotalRecalls site container.

Serves /var/www with explicit charset=utf-8 on HTML/CSS/JS/JSON responses,
and provides a native POST /api/chat endpoint backed by Dialogflow CX with full CORS support.
"""
import http.server
import os
import json
from google.auth import default
from google.cloud.dialogflowcx_v3.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3.types import session

CHARSET_TEXT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".htm": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".mjs": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".xml": "application/xml; charset=utf-8",
    ".svg": "image/svg+xml; charset=utf-8",
    ".md": "text/markdown; charset=utf-8",
}

def query_dialogflow(user_query, session_id="web-user-session"):
    try:
        creds, _ = default()
        agent_path = "projects/cs-poc-gw89wethbilefc1wrhgq7d7/locations/us-central1/agents/d8f11aa3-683c-4f06-b015-3e6d9b97f81c"
        session_path = f"{agent_path}/sessions/{session_id}"

        client_options = {"api_endpoint": "us-central1-dialogflow.googleapis.com"}
        client = SessionsClient(client_options=client_options, credentials=creds)

        query_input = session.QueryInput(text=session.TextInput(text=user_query), language_code="en")
        request = session.DetectIntentRequest(session=session_path, query_input=query_input)

        response = client.detect_intent(request=request)
        messages = response.query_result.response_messages
        if messages and messages[0].text.text:
            return messages[0].text.text[0]
        return "I'm here to help you own your AI conversations. How can I assist you today?"
    except Exception as e:
        return f"Support Assistant is currently connecting (Error: {str(e)[:60]})"


class CharsetHandler(http.server.SimpleHTTPRequestHandler):
    def guess_type(self, path):
        base = super().guess_type(path)
        ext = os.path.splitext(path)[1].lower()
        return CHARSET_TEXT_TYPES.get(ext, base)

    def do_OPTIONS(self):
        if self.path == "/api/chat":
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
        else:
            super().do_OPTIONS()

    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode("utf-8"))
                user_msg = data.get("message", "").strip()
                session_id = data.get("sessionId", "web-visitor")
                
                if not user_msg:
                    reply = "Please type a message or question."
                else:
                    reply = query_dialogflow(user_msg, session_id)

                response_data = json.dumps({"reply": reply}).encode("utf-8")
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(response_data)))
                self.end_headers()
                self.wfile.write(response_data)
                return
            except Exception as e:
                err_data = json.dumps({"reply": f"Error processing request: {str(e)}"}).encode("utf-8")
                self.send_response(500)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(err_data)))
                self.end_headers()
                self.wfile.write(err_data)
                return
        else:
            self.send_response(404)
            self.end_headers()


def main():
    port = int(os.environ.get("PORT", "8080"))
    server = http.server.ThreadingHTTPServer(
        ("0.0.0.0", port),
        lambda *args, **kwargs: CharsetHandler(*args, directory="/var/www", **kwargs),
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
