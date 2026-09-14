"""Probe v2: pin down WHAT breaks order=created, and confirm order=updated
paginates all the way through (so order=created is redundant)."""
import sys, os, time, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from totalrecalls.core.paths import load_session
from totalrecalls.adapters.chatgpt.http import _headers
BASE = "https://chatgpt.com"

def one(tok, path, tag):
    req = urllib.request.Request(BASE + path, headers=_headers(access_token=tok), method="GET")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            b = r.read(); return (r.status, len(b), time.time()-t0, None)
    except urllib.error.HTTPError as e:
        b = e.read() if e.fp else b""
        return (e.code, len(b), time.time()-t0, b[:200].decode("utf-8","replace"))
    except Exception as e:
        return (0, 0, time.time()-t0, f"{type(e).__name__}: {e}")

def main():
    tok = load_session().get("token")
    print(f"token_len={len(tok)}\n")
    tests = [
        ("order=created limit=10  off=0",  "/backend-api/conversations?offset=0&limit=10&order=created"),
        ("order=created limit=28  off=28", "/backend-api/conversations?offset=28&limit=28&order=created"),
        ("order=created limit=5   off=0",  "/backend-api/conversations?offset=0&limit=5&order=created"),
        ("order=updated limit=28  off=0",  "/backend-api/conversations?offset=0&limit=28&order=updated"),
        ("order=updated limit=28  off=224","/backend-api/conversations?offset=224&limit=28&order=updated"),
        ("order=updated limit=28  off=500","/backend-api/conversations?offset=500&limit=28&order=updated"),
        ("order=updated limit=100 off=0",  "/backend-api/conversations?offset=0&limit=100&order=updated"),
    ]
    for tag, path in tests:
        st, ln, dt, err = one(tok, path, tag)
        line = f"  {st}  {ln:>6}b  {dt:.2f}s  {tag}"
        if err: line += f"   {err}"
        print(line)
        time.sleep(2.0)
    return 0
if __name__ == "__main__":
    sys.exit(main())
