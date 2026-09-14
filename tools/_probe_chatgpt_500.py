"""Probe the deterministic ChatGPT 500.

Reads the saved ChatGPT session token from session.json (NEVER prints it) and
fires the exact failing request (order=created) plus the control (order=updated)
a few times each, capturing the FULL raw response body + headers on a 500.
This answers: is the 500 a deterministic server-side exception triggered by the
request (our side), or random load?

Run:  .venv/Scripts/python.exe tools/_probe_chatgpt_500.py
"""
import json, os, sys, time
import urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from totalrecalls.core.paths import SESSION_FILE, appdata_dir
from totalrecalls.adapters.chatgpt.http import _headers, USER_AGENT

BASE = "https://chatgpt.com"

def get_token():
    from totalrecalls.core.paths import load_session
    d = load_session()
    if not d:
        print("load_session() returned None — no usable session")
        return None
    tok = d.get("token") or d.get("access_token") or d.get("credential")
    print(f"session provider={d.get('provider')!r} keys={list(d.keys())} "
          f"token_present={bool(tok)} token_len={len(tok) if tok else 0}")
    return tok

def fire(tok, path, tag, tries=3):
    print(f"\n=== {tag} :: GET {path} ===")
    hdrs = _headers(access_token=tok)
    results = []
    for i in range(tries):
        req = urllib.request.Request(BASE + path, headers=hdrs, method="GET")
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
                dt = time.time() - t0
                print(f"  attempt {i+1}: HTTP {r.status} in {dt:.1f}s, "
                      f"{len(body)} bytes, content-type={r.headers.get('content-type')!r}")
                if r.status != 200:
                    print("  BODY:", body[:2000].decode("utf-8", "replace"))
                results.append(("ok", r.status, dt, len(body)))
        except urllib.error.HTTPError as e:
            dt = time.time() - t0
            body = e.read() if e.fp else b""
            txt = body.decode("utf-8", "replace")
            print(f"  attempt {i+1}: HTTP {e.code} in {dt:.1f}s, {len(body)} bytes")
            print("  HEADERS:", {k: e.headers.get(k) for k in
                  ("content-type","server","x-request-id","cf-ray","x-envoy-upstream-service-time")
                  if e.headers.get(k)})
            print("  BODY:", txt[:3000] if txt else "(empty body)")
            results.append(("err", e.code, dt, len(body)))
        except Exception as e:
            dt = time.time() - t0
            print(f"  attempt {i+1}: EXC {type(e).__name__} in {dt:.1f}s: {e}")
            results.append(("exc", 0, dt, 0))
        time.sleep(2.0)
    return results

def main():
    tok = get_token()
    if not tok:
        return 1
    # control: the pass that SUCCEEDS (order=updated offset=0 limit=28)
    fire(tok, "/backend-api/conversations?offset=0&limit=28&order=updated", "CONTROL order=updated")
    # the deterministic 500: the pass that always fails (order=created offset=0 limit=28)
    fire(tok, "/backend-api/conversations?offset=0&limit=28&order=created", "FAILING order=created")
    return 0

if __name__ == "__main__":
    sys.exit(main())
