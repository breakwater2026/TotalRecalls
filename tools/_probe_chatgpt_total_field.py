"""Probe the ChatGPT count badge: what does the `total` field actually return?

Fires the EXACT request count_conversations makes (order=updated, limit=1) and
a few variants, dumping the top-level JSON shape (NOT the item bodies) so we
can see whether `total` is a real count or garbage.
"""
import sys, os, json, time, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from totalrecalls.core.paths import load_session
from totalrecalls.adapters.chatgpt.http import _headers
BASE = "https://chatgpt.com"

def fields(tok, path):
    req = urllib.request.Request(BASE + path, headers=_headers(access_token=tok))
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read())
            if isinstance(d, dict):
                items = d.get("items") or d.get("conversations") or []
                # print all top-level keys except the items array, plus len(items)
                shape = {k: v for k, v in d.items() if k not in ("items", "conversations")}
                return f"HTTP 200  items_on_page={len(items) if isinstance(items, list) else '?'}  shape={shape}"
            return f"HTTP 200 (non-dict: {type(d).__name__})"
    except urllib.error.HTTPError as e:
        b = e.read() if e.fp else b""
        return f"HTTP {e.code}  body={b[:120].decode('utf-8','replace')}"

def main():
    tok = load_session()["token"]
    print(f"token_len={len(tok)}\n")
    probes = [
        ("COUNT  (limit=1, updated)  <- what the badge uses", "/backend-api/conversations?offset=0&limit=1&order=updated"),
        ("limit=28, updated",        "/backend-api/conversations?offset=0&limit=28&order=updated"),
        ("limit=1, updated, offset=100", "/backend-api/conversations?offset=100&limit=1&order=updated"),
        ("limit=28, updated, offset=84", "/backend-api/conversations?offset=84&limit=28&order=updated"),
    ]
    for tag, path in probes:
        print(f"  {fields(tok, path)}")
        print(f"      ^ {tag}")
        time.sleep(2.5)
    return 0
if __name__ == "__main__":
    sys.exit(main())
