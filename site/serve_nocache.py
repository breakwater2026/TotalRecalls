import http.server
import socketserver
import os

PORT = 4321
DIST_DIR = os.path.join(os.path.dirname(__file__), "dist")

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

if __name__ == "__main__":
    handler = NoCacheHTTPRequestHandler
    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        print(f"Serving HTTP on 0.0.0.0 port {PORT} from {DIST_DIR}...")
        httpd.serve_forever()
