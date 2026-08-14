"""Static file server for the TotalRecalls site container.

Serves /var/www with explicit charset=utf-8 on HTML/CSS/JS/JSON responses.
Python's default SimpleHTTPRequestHandler omits the charset directive for
text/html, which makes browsers fall back to Latin-1 and garble em-dashes /
middle-dots — exactly the mojibake the V4 review flagged.
"""
import http.server
import os

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


class CharsetHandler(http.server.SimpleHTTPRequestHandler):
    def guess_type(self, path):
        base = super().guess_type(path)
        ext = os.path.splitext(path)[1].lower()
        return CHARSET_TEXT_TYPES.get(ext, base)


def main():
    port = int(os.environ.get("PORT", "8080"))
    server = http.server.ThreadingHTTPServer(
        ("0.0.0.0", port),
        lambda *args, **kwargs: CharsetHandler(*args, directory="/var/www", **kwargs),
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
