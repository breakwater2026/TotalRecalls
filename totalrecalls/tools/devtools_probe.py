"""DevTools probe: record, replay, and diff provider HTTP fixtures.

Three commands:

  record   Make a real HTTP GET against a provider endpoint (using a
           cookie/bearer captured from your browser DevTools) and save
           the raw JSON response to a fixture file. The fixture is
           what the adapter would have seen if it had a real account.

  replay   Load a fixture and run it through the adapter's parsing
           logic in dry-run mode (no real network calls). Prints
           the parsed ConversationSummary list / UnifiedConversation
           to stdout as JSON so you can see whether the adapter
           correctly handles this real response.

  diff     Compare the parsed output from a fixture against a
           snapshot file (a previous "good" parse). Useful after
           an adapter code change to see if the parsing has
           shifted for known-real input.

This lets a developer who has a real account (or a friend who does)
record the actual endpoint responses once, commit them to tests/fixtures/,
and then the entire adapter test suite can run offline with the same
real data.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

# Windows-friendly User-Agent (matches the other adapters)
DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)

PROVIDER_HINTS: dict[str, dict[str, str]] = {
    "deepseek": {"base": "https://chat.deepseek.com", "list_path": "/api/v0/chat_session/fetch_page?lte_cursor.pinned=false"},
    "qwen":     {"base": "https://chat.qwen.ai",     "list_path": "/api/v2/chats/?page=1&exclude_project=true"},
    "mistral":  {"base": "https://chat.mistral.ai",  "list_path": "/api/trpc/chat.last?input=%7B%22json%22%3A%7B%7D%7D"},
}


def _fetch_once(url: str, headers: dict) -> tuple[int, str]:
    """One GET; returns (status, body). HTTP errors return their status/body."""
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
        return e.code, body


def _record(args: argparse.Namespace) -> int:
    url = args.url
    if not url.startswith("http"):
        base = PROVIDER_HINTS.get(args.provider, {}).get("base")
        if not base:
            print(f"ERROR: unknown provider {args.provider!r}; provide --url", file=sys.stderr)
            return 2
        url = base + url
    headers = {"User-Agent": DEFAULT_UA, "Accept": "application/json"}
    if args.cookie:
        headers["Cookie"] = args.cookie
    elif args.bearer:
        headers["Authorization"] = f"Bearer {args.bearer}"
    else:
        print("ERROR: provide --cookie or --bearer (or both for robustness)", file=sys.stderr)
        return 2

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    pages_n = int(getattr(args, "pages", 1) or 1)
    page_param = getattr(args, "page_param", None)
    page_start = int(getattr(args, "page_start", 1) or 1)
    page_step = int(getattr(args, "page_step", 1) or 1)

    captured: list[dict] = []
    for i in range(pages_n):
        page_url = url
        if page_param and pages_n > 1:
            val = page_start + i * page_step
            sep = "&" if "?" in url else "?"
            page_url = f"{url}{sep}{page_param}={val}"
        print(f"GET {page_url}", file=sys.stderr)
        t0 = time.time()
        try:
            status, body = _fetch_once(page_url, headers)
        except Exception as e:
            print(f"ERROR page {i + 1}: {e}", file=sys.stderr)
            return 1
        elapsed = time.time() - t0
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = body
        captured.append({"url": page_url, "status": status, "data": data})
        print(f"  page {i + 1}/{pages_n} status={status} bytes={len(body)} elapsed={elapsed:.2f}s",
              file=sys.stderr)

    meta = {
        "provider": args.provider,
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    if page_param and pages_n > 1:
        meta["page_param"] = page_param
        meta["page_start"] = page_start
        meta["page_step"] = page_step
    if len(captured) == 1:
        payload = {
            "_meta": {**meta, "url": captured[0]["url"], "status": captured[0]["status"]},
            "response": captured[0]["data"],
        }
    else:
        payload = {
            "_meta": meta,
            "responses": [{"url": c["url"], "status": c["status"], "data": c["data"]} for c in captured],
        }
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  saved -> {out} ({len(captured)} page(s))", file=sys.stderr)
    return 0


def _load_fixture(path: Path) -> tuple[dict, list]:
    """Return (meta, pages). `pages` is a list of raw response bodies (length 1
    for a single-response fixture, longer for a captured pagination sequence)."""
    raw = path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}, [raw]  # text fixture
    if isinstance(data, dict) and "_meta" in data:
        meta = data["_meta"]
        if "responses" in data:
            pages = [
                r.get("data", r) if isinstance(r, dict) else r
                for r in data["responses"]
            ]
            return meta, pages
        if "response" in data:
            return meta, [data["response"]]
        return meta, [data]
    return {}, [data]  # bare JSON


def _sequence(pages: list):
    """Return a callable that yields captured pages in order; the last page
    repeats if the adapter over-fetches (so replay never crashes)."""
    if not pages:
        return lambda: {}
    it = iter(pages)
    last = pages[-1]
    return lambda: next(it, last)


def _replay(args: argparse.Namespace) -> int:
    fx = Path(args.list_fixture)
    if not fx.exists():
        print(f"ERROR: fixture not found: {fx}", file=sys.stderr)
        return 2
    meta, pages = _load_fixture(fx)
    next_page = _sequence(pages)
    print(f"fixture={fx}", file=sys.stderr)
    if meta:
        print(f"  captured_at={meta.get('captured_at')} url={meta.get('url')} status={meta.get('status')}", file=sys.stderr)

    # Dispatch to the right adapter.
    # We monkey-patch the *adapter module's* `request` binding (not the
    # http module's) because adapters do `from .http import request`,
    # which creates a local binding that the http-module patch misses.
    if args.provider == "deepseek":
        from totalrecalls.adapters.deepseek import adapter as ds_adapter
        from totalrecalls.adapters.deepseek import http as ds_http
        a = ds_adapter.DeepSeekAdapter()
        orig = ds_adapter.request

        def fake_request(path, *, cookie, access_token=None, delay=None):
            if "chat_session/fetch_page" in path:
                return 200, next_page()
            return orig(path, access_token=access_token, cookie=cookie, delay=delay)

        ds_adapter.request = fake_request
        try:
            results = a.list_conversations("session=dummy", deep=True)
        finally:
            ds_adapter.request = orig
    elif args.provider == "qwen":
        from totalrecalls.adapters.qwen import adapter as qwen_adapter
        from totalrecalls.adapters.qwen import http as qwen_http
        a = qwen_adapter.QwenChatAdapter()
        orig = qwen_adapter.request

        def fake_request(path, *, cookie, base=qwen_http.BASE, delay=None):
            if "chats/" in path and "page" in path:
                return 200, next_page()
            return orig(path, cookie=cookie, base=base, delay=delay)

        qwen_adapter.request = fake_request
        try:
            results = a.list_conversations("session=dummy", deep=True)
        finally:
            qwen_adapter.request = orig
    elif args.provider == "mistral":
        from totalrecalls.adapters.mistral import adapter as m_adapter
        from totalrecalls.adapters.mistral import http as m_http
        a = m_adapter.MistralAdapter()
        orig = m_http.request

        def fake_request(path, *, cookie, delay=None):
            if "/api/trpc/chat.last" in path:
                return 200, next_page()
            return orig(path, cookie=cookie, delay=delay)

        m_http.request = fake_request
        try:
            results = a.list_conversations("session=dummy", deep=True)
        finally:
            m_http.request = orig
    else:
        print(f"ERROR: replay not implemented for provider {args.provider!r}", file=sys.stderr)
        return 2

    out = {
        "fixture": str(fx),
        "parsed_count": len(results),
        "items": [
            {
                "id": s.id,
                "title": s.title,
                "created_at": s.created_at,
                "updated_at": s.updated_at,
                "folder": s.folder,
            }
            for s in results
        ],
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


def _diff(args: argparse.Namespace) -> int:
    fx = Path(args.list_fixture)
    snap = Path(args.snapshot)
    if not fx.exists() or not snap.exists():
        print(f"ERROR: missing fixture ({fx}) or snapshot ({snap})", file=sys.stderr)
        return 2
    # Replay fresh
    parsed = _replay_args(args.provider, fx)
    current = json.loads(parsed)
    expected = json.loads(snap.read_text(encoding="utf-8"))
    # Compare items only (the `fixture` field is path-dependent and
    # naturally differs between the replay that built the snapshot and
    # the replay we just ran).
    if current.get("items") == expected.get("items"):
        print("DIFF: identical to snapshot ✓", file=sys.stderr)
        return 0
    # Show only item-level differences
    cur_ids = {it["id"] for it in current.get("items", [])}
    exp_ids = {it["id"] for it in expected.get("items", [])}
    print(f"DIFF: parsed={len(cur_ids)} expected={len(exp_ids)}", file=sys.stderr)
    print(f"  added:   {sorted(cur_ids - exp_ids)}", file=sys.stderr)
    print(f"  removed: {sorted(exp_ids - cur_ids)}", file=sys.stderr)
    return 1


def _replay_args(provider: str, fx: Path) -> str:
    """Internal helper: replay a fixture and return the JSON string."""
    meta, pages = _load_fixture(fx)
    next_page = _sequence(pages)
    if provider == "deepseek":
        from totalrecalls.adapters.deepseek import adapter as ad
        from totalrecalls.adapters.deepseek import http as h
        a = ad.DeepSeekAdapter()
        orig = ad.request

        def fake(p, *, cookie, access_token=None, delay=None):
            if "chat_session/fetch_page" in p:
                return 200, next_page()
            return orig(p, access_token=access_token, cookie=cookie, delay=delay)

        ad.request = fake
        try:
            results = a.list_conversations("session=dummy", deep=True)
        finally:
            ad.request = orig
    elif provider == "qwen":
        from totalrecalls.adapters.qwen import adapter as ad
        from totalrecalls.adapters.qwen import http as h
        a = ad.QwenChatAdapter()
        orig = ad.request

        def fake(p, *, cookie, base=h.BASE, delay=None):
            if "chats/" in p and "page" in p:
                return 200, next_page()
            return orig(p, cookie=cookie, base=base, delay=delay)

        ad.request = fake
        try:
            results = a.list_conversations("session=dummy", deep=True)
        finally:
            ad.request = orig
    elif provider == "mistral":
        from totalrecalls.adapters.mistral import adapter as ad
        from totalrecalls.adapters.mistral import http as h
        a = ad.MistralAdapter()
        orig = h.request

        def fake(p, *, cookie, delay=None):
            if "/api/trpc/chat.last" in p:
                return 200, next_page()
            return orig(p, cookie=cookie, delay=delay)

        h.request = fake
        try:
            results = a.list_conversations("session=dummy", deep=True)
        finally:
            h.request = orig
    else:
        raise ValueError(provider)
    return json.dumps({
        "items": [
            {"id": s.id, "title": s.title, "created_at": s.created_at, "updated_at": s.updated_at, "folder": s.folder}
            for s in results
        ]
    }, indent=2, ensure_ascii=False)



def _synthesize(args: argparse.Namespace) -> int:
    """Build a believable list response for a provider, with no network call.

    The shape mirrors what each provider's web app typically returns,
    based on the most common documented patterns. Use this to:
      - smoke-test the adapter parsing code
      - bootstrap the fixtures directory before real data is available
      - demonstrate the parser in the README without exposing real sessions
    """
    import time as _t
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    now = _t.time()
    items = []
    for i in range(args.count):
        ts = now - (i * 86400)  # one day apart
        if args.provider == "deepseek":
            items.append({
                "id": f"synth-{i:04d}",
                "title": f"Synthetic DeepSeek conversation #{i+1}",
                "pinned": False,
                "model_type": "default",
                "inserted_at": ts,
                "updated_at": ts + 3600,
            })
        elif args.provider == "qwen":
            items.append({
                "id": f"synth-{i:04d}",
                "title": f"Synthetic Qwen conversation #{i+1}",
                "created_at": str(int(ts)),
                "updated_at": str(int(ts + 3600)),
            })
        elif args.provider == "mistral":
            iso = _t.strftime("%Y-%m-%dT%H:%M:%S.000Z", _t.gmtime(ts))
            items.append({
                "id": f"synth-{i:04d}",
                "title": "New chat",
                "generatedTitle": f"Synthetic Mistral conversation #{i+1}",
                "userTitle": None,
                "createdAt": iso,
                "updatedAt": iso,
                "pinned": False,
                "projectId": None,
            })
    if args.provider == "deepseek":
        body = {
            "code": 0, "msg": "",
            "data": {
                "biz_code": 0, "biz_msg": "",
                "biz_data": {"chat_sessions": items, "has_more": False},
            },
        }
    elif args.provider == "qwen":
        body = {"success": True, "data": items}
    elif args.provider == "mistral":
        # Raw tRPC httpLink response: the adapter's trpc_query() unwraps
        # result.data.json to reach {"items": [...], "nextCursor": ...}.
        body = {"result": {"data": {"json": {"items": items, "nextCursor": None}}}}
    else:
        body = items
    payload = {
        "_meta": {
            "provider": args.provider,
            "synthetic": True,
            "captured_at": _t.strftime("%Y-%m-%dT%H:%M:%SZ", _t.gmtime()),
        },
        "response": body,
    }
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"synthetic fixture -> {out} ({args.count} items)", file=sys.stderr)
    return 0

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="totalrecalls-devtools",
        description="Probe provider endpoints, replay fixtures through adapters.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("record", help="Capture a live HTTP response as a fixture")
    pr.add_argument("--provider", required=True, choices=["deepseek", "qwen", "mistral"])
    pr.add_argument("--url", help="Absolute URL or path (joined with --provider base)")
    pr.add_argument("--cookie", help="Cookie header value (from DevTools)")
    pr.add_argument("--bearer", help="Bearer token (from DevTools)")
    pr.add_argument("--out", required=True, help="Output fixture path (.json)")
    pr.add_argument("--pages", type=int, default=1,
                    help="Capture N pages as a pagination sequence")
    pr.add_argument("--page-param", default=None,
                    help="Query param to vary per page (e.g. offset, page)")
    pr.add_argument("--page-start", type=int, default=1, help="Value for page 1")
    pr.add_argument("--page-step", type=int, default=1, help="Increment per page")
    pr.set_defaults(func=_record)

    py = sub.add_parser("replay", help="Run a captured fixture through the adapter parser")
    py.add_argument("--provider", required=True, choices=["deepseek", "qwen", "mistral"])
    py.add_argument("--list-fixture", required=True, help="Fixture path")
    py.set_defaults(func=_replay)

    pd = sub.add_parser("diff", help="Compare a fixture parse against a saved snapshot")
    pd.add_argument("--provider", required=True, choices=["deepseek", "qwen", "mistral"])
    pd.add_argument("--list-fixture", required=True)
    pd.add_argument("--snapshot", required=True)
    pd.set_defaults(func=_diff)

    ps = sub.add_parser("synthesize", help="Generate a synthetic fixture (for offline testing)")
    ps.add_argument("--provider", required=True, choices=["deepseek", "qwen", "mistral"])
    ps.add_argument("--out", required=True, help="Output fixture path")
    ps.add_argument("--count", type=int, default=3, help="Number of fake conversations")
    ps.set_defaults(func=_synthesize)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
