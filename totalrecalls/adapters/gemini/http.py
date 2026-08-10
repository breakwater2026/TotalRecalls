"""Gemini adapter transport helpers.

Supports:
  1) Offline Google Takeout / exported JSON (preferred, stable)
  2) Browser cookie credential (best-effort against gemini.google.com)
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from pathlib import Path

from totalrecalls.core.paths import log

BASE = "https://gemini.google.com"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)

try:
    from curl_cffi import requests as _cffi_requests
    _HAS_CFFI = True
except Exception:
    _cffi_requests = None  # type: ignore
    _HAS_CFFI = False


class GeminiApiError(Exception):
    pass


def looks_like_path(credential: str) -> bool:
    c = (credential or "").strip().strip('"')
    if not c:
        return False
    p = Path(c)
    return p.exists() or c.lower().endswith((".json", ".zip")) or "takeout" in c.lower()


def cookie_header_from_credential(credential: str) -> str:
    raw = (credential or "").strip()
    if not raw:
        raise GeminiApiError("auth-failed")
    if "PSID=" in raw or "Cookie:" in raw or "__Secure-" in raw:
        return raw.split(":", 1)[-1].strip() if raw.lower().startswith("cookie:") else raw
    # bare SAPISID / PSID value is insufficient alone; still wrap as SID-ish
    return raw if "=" in raw else f"__Secure-1PSID={raw}"


def request_json(url: str, cookie: str, *, delay: float = 1.0) -> dict | list | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json,text/plain,*/*",
        "Cookie": cookie,
        "Referer": BASE + "/app",
        "Origin": BASE,
    }
    if delay:
        time.sleep(delay)

    def _one():
        if _HAS_CFFI and _cffi_requests is not None:
            try:
                resp = _cffi_requests.get(
                    url, headers=headers, timeout=60, impersonate="chrome131", allow_redirects=True,
                )
                if resp.status_code in (401, 403):
                    raise urllib.error.HTTPError(url, resp.status_code, "auth", {}, None)
                if resp.status_code >= 400:
                    raise urllib.error.HTTPError(url, resp.status_code, "http", {}, None)
                raw = resp.content
                if not raw:
                    return None
                try:
                    return json.loads(raw.decode("utf-8", "replace"))
                except Exception:
                    return None
            except (UnicodeEncodeError, UnicodeDecodeError, ValueError) as e:
                log(f"gemini cffi fail: {e}")
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
            return json.loads(raw.decode("utf-8", "replace")) if raw else None

    try:
        return _one()
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            raise GeminiApiError("auth-failed")
        raise GeminiApiError(f"http-{e.code}")
    except GeminiApiError:
        raise
    except Exception as e:
        raise GeminiApiError("network") from e


def load_offline_export(path_str: str) -> list[dict]:
    """Load conversations from a Takeout-like JSON file or directory."""
    path = Path(path_str.strip().strip('"')).expanduser()
    if not path.exists():
        raise GeminiApiError("auth-failed")

    candidates: list[Path] = []
    if path.is_file():
        candidates = [path]
    else:
        # Search common Takeout layouts
        for pattern in (
            "**/Gemini/**/*.json",
            "**/My Activity/**/Gemini*.json",
            "**/*gemini*.json",
            "**/*Gemini*.json",
            "**/conversations.json",
            "**/*.json",
        ):
            candidates.extend(list(path.glob(pattern))[:50])
        # de-dupe preserve order
        seen = set()
        uniq = []
        for c in candidates:
            s = str(c.resolve())
            if s not in seen:
                seen.add(s)
                uniq.append(c)
        candidates = uniq[:80]

    conversations: list[dict] = []
    for fp in candidates:
        try:
            if fp.suffix.lower() != ".json" or fp.stat().st_size > 80_000_000:
                continue
            data = json.loads(fp.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        conversations.extend(_normalize_offline_payload(data, source=str(fp)))
    if not conversations:
        raise GeminiApiError("auth-failed")
    log(f"gemini offline: loaded {len(conversations)} conversation(s) from {path}")
    return conversations


def _normalize_offline_payload(data, *, source: str) -> list[dict]:
    out: list[dict] = []
    if isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, dict):
                out.append(_coerce_offline_item(item, fallback_id=f"{Path(source).stem}-{i}"))
        return [x for x in out if x]
    if isinstance(data, dict):
        # single conversation
        if any(k in data for k in ("messages", "turns", "chat", "conversation")):
            item = _coerce_offline_item(data, fallback_id=Path(source).stem)
            return [item] if item else []
        for key in ("conversations", "chats", "items", "activities"):
            val = data.get(key)
            if isinstance(val, list):
                for i, item in enumerate(val):
                    if isinstance(item, dict):
                        c = _coerce_offline_item(item, fallback_id=f"{key}-{i}")
                        if c:
                            out.append(c)
        return out
    return []


def _coerce_offline_item(item: dict, *, fallback_id: str) -> dict | None:
    cid = str(item.get("id") or item.get("conversation_id") or item.get("uuid") or fallback_id)
    title = str(item.get("title") or item.get("name") or item.get("prompt") or "Gemini conversation")
    messages = item.get("messages") or item.get("turns") or item.get("chat") or []
    # My Activity style: title + HTML body fragments
    if not messages and (item.get("title") or item.get("html")):
        messages = []
        if item.get("title"):
            messages.append({"role": "user", "content": str(item.get("title"))})
        body = item.get("html") or item.get("content") or item.get("text")
        if body:
            messages.append({"role": "assistant", "content": str(body)})
    if not messages and not title:
        return None
    return {
        "id": cid,
        "title": title[:200],
        "messages": messages if isinstance(messages, list) else [],
        "updated_at": str(item.get("updated_at") or item.get("time") or item.get("timestamp") or ""),
        "created_at": str(item.get("created_at") or ""),
        "_source": "offline",
        "raw": item,
    }
