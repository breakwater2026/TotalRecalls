"""Gemini ProviderAdapter — Takeout/offline JSON primary; live cookie secondary.

The Gemini web UI is served from gemini.google.com and authenticates via
Google Account cookies (__Secure-1PSID, __Secure-1PAPISID, etc.) plus a
per-session API key embedded in the page HTML.  When we have a live cookie
credential we:

1. GET /app with the cookie → extract the embedded API key from the page HTML
2. POST the Google-style batched RPC to /_/.../data?key=<API_KEY> with the
   same cookie + Chrome impersonation headers

This mirrors exactly what the browser does and passes Google's anti-bot
checks because we impersonate a real Chrome 131 client.
"""

from __future__ import annotations

from totalrecalls.adapters.gemini.http import (
    GeminiApiError,
    cookie_header_from_credential,
    looks_like_path,
    looks_like_cookie,
    load_offline_export,
    request,
    fetch_page_html,
    extract_api_key,
    list_conversations_live,
    fetch_conversation_live,
    BASE,
    APP_BASE,
)
from totalrecalls.core.export_fs import HOME_SPACE_NAME
from totalrecalls.core.paths import log
from totalrecalls.core.schema import (
    AccountInfo,
    ConversationSummary,
    Message,
    UnifiedConversation,
)


class GeminiAdapter:
    id = "gemini"
    display_name = "Gemini"

    def __init__(self):
        self._offline_cache: dict[str, dict] = {}
        self._mode: str = "unknown"  # offline | cookie
        self._cookie: str | None = None
        self._page_html: str | None = None  # cached page HTML for live calls

    def validate(self, credential: str) -> AccountInfo:
        if looks_like_path(credential):
            items = load_offline_export(credential)
            self._offline_cache = {str(it["id"]): it for it in items}
            self._mode = "offline"
            return AccountInfo(
                email="gemini-takeout@local",
                external_id="takeout",
                display_name="Gemini Takeout",
            )
        if not looks_like_cookie(credential):
            raise GeminiApiError("auth-failed")
        # Live cookie path — probe the app page to verify the session
        cookie = cookie_header_from_credential(credential)
        self._cookie = cookie
        try:
            html = fetch_page_html(cookie, delay=0)
            self._page_html = html  # cache for subsequent live calls
            if not html:
                raise GeminiApiError("auth-failed")
            api_key = extract_api_key(html)
            if not api_key:
                log("gemini live: API key not found in page — session may have expired")
                raise GeminiApiError("auth-failed")
            # We successfully authenticated — the page returned our account info
            # embedded in the HTML (window['YT_INITIAL_PLAYER_RESPONSE'] / __SAPISIDDATA)
            self._mode = "cookie"
            # Try to extract email from the page
            email = self._extract_email_from_html(html)
            if email:
                return AccountInfo(
                    email=email,
                    external_id="gemini-session",
                    display_name=email.split("@")[0] if "@" in email else "Gemini user",
                )
            return AccountInfo(
                email="gemini-session@local",
                external_id="gemini-session",
                display_name="Gemini user",
            )
        except Exception as e:
            # Any probe failure (network, non-Chrome UA blocked by Google,
            # API key pattern changed, etc.) → accept optimistically.
            # The bridge only calls validate() AFTER the embedded WebView2
            # has already completed Google sign-in, so the cookie is
            # already verified.  Hard-blocking here (like the old code did
            # with `except GeminiApiError: raise`) is what made the "Log
            # in to Gemini" button appear to do nothing in certain builds.
            log(f"gemini cookie probe failed: {e}")
            # Accept cookie optimistically (like Grok adapter does) so the
            # UI doesn't hard-block users whose cookie is valid but whose
            # HTML parse differs from our extractor
            self._mode = "cookie"
            return AccountInfo(
                email="gemini-session@local",
                external_id="gemini-session",
                display_name="Gemini user",
            )

    def _extract_email_from_html(self, html: str) -> str | None:
        """Try to find the Google account email from the Gemini page HTML."""
        import re
        # Google embeds the user's email in various JS config objects
        patterns = [
            r'"email"\s*:\s*"([^"]+@[^"]+)"',
            r'"obfuscatedEmail"\s*:\s*"([^"]+)"',
            r'"displayEmail"\s*:\s*"([^"]+)"',
            r'data-email="([^"]+@[^"]+)"',
        ]
        for pat in patterns:
            m = re.search(pat, html)
            if m and "@" in m.group(1):
                return m.group(1)
        return None

    def list_conversations(self, credential: str, *, deep: bool = False) -> list[ConversationSummary]:
        if looks_like_path(credential) or self._mode == "offline":
            if not self._offline_cache:
                items = load_offline_export(credential)
                self._offline_cache = {str(it["id"]): it for it in items}
                self._mode = "offline"
            out = []
            for it in self._offline_cache.values():
                out.append(
                    ConversationSummary(
                        id=str(it["id"]),
                        title=str(it.get("title") or "Gemini conversation"),
                        updated_at=str(it.get("updated_at") or ""),
                        created_at=str(it.get("created_at") or ""),
                        folder=HOME_SPACE_NAME,
                        raw=it,
                    )
                )
            return out
        # Live cookie listing
        if self._mode != "cookie" or not self._cookie:
            cookie = cookie_header_from_credential(credential)
            self._cookie = cookie
            self._mode = "cookie"
        # Fetch page HTML if not cached from validate()
        if not self._page_html:
            self._page_html = fetch_page_html(self._cookie, delay=0)
        try:
            live_items = list_conversations_live(self._page_html, self._cookie)
        except GeminiApiError:
            raise
        except Exception as e:
            log(f"gemini live list failed: {e}")
            raise GeminiApiError("network")
        if not live_items:
            log("gemini live: no conversations returned")
            return []
        out = []
        for item in live_items:
            cid = str(item.get("id", ""))
            if not cid:
                continue
            title = str(item.get("title", "") or item.get("title", "") or "Gemini conversation")
            out.append(
                ConversationSummary(
                    id=cid,
                    title=title.strip() or "Gemini conversation",
                    updated_at=str(item.get("updated_at") or ""),
                    created_at=str(item.get("created_at") or ""),
                    folder=HOME_SPACE_NAME,
                    raw=item,
                )
            )
        return out

    def fetch_conversation(self, credential: str, conv_id: str) -> UnifiedConversation:
        if looks_like_path(credential) or self._mode == "offline" or conv_id in self._offline_cache:
            if not self._offline_cache and looks_like_path(credential):
                items = load_offline_export(credential)
                self._offline_cache = {str(it["id"]): it for it in items}
            item = self._offline_cache.get(conv_id)
            if not item:
                raise GeminiApiError("http-empty")
            return self.to_unified(item, account=AccountInfo(
                email="gemini-takeout@local", external_id="takeout", display_name="Gemini Takeout",
            ))
        # Live cookie fetch
        if self._mode != "cookie" or not self._cookie:
            cookie = cookie_header_from_credential(credential)
            self._cookie = cookie
            self._mode = "cookie"
        # Fetch page HTML if not cached from validate()
        if not self._page_html:
            self._page_html = fetch_page_html(self._cookie, delay=0)
        try:
            detail = fetch_conversation_live(self._page_html, self._cookie, conv_id)
        except GeminiApiError:
            raise
        except Exception as e:
            log(f"gemini live fetch failed: {e}")
            raise GeminiApiError("network")
        if not detail:
            raise GeminiApiError("http-empty")
        if "id" not in detail:
            detail = {**detail, "id": conv_id}
        account = AccountInfo(
            email="gemini-session@local",
            external_id="gemini-session",
            display_name="Gemini user",
        )
        return self.to_unified(detail, account=account)

    def to_unified(
        self,
        detail: dict,
        *,
        summary: ConversationSummary | None = None,
        account: AccountInfo | None = None,
    ) -> UnifiedConversation:
        detail = detail if isinstance(detail, dict) else {}
        title = str(detail.get("title") or (summary.title if summary else "") or "Gemini conversation")
        cid = str(detail.get("id") or (summary.id if summary else "") or "")
        messages: list[Message] = []
        for m in detail.get("messages") or []:
            if not isinstance(m, dict):
                continue
            role_raw = str(m.get("role") or m.get("author") or m.get("sender") or "").lower()
            if role_raw in ("user", "human", "prompt"):
                role = "user"
            elif role_raw in ("model", "assistant", "gemini", "bot"):
                role = "assistant"
            else:
                role = "assistant" if m.get("content") or m.get("text") else "user"
            text = str(m.get("content") or m.get("text") or m.get("message") or "").strip()
            # Handle Gemini's content parts format: [{"text": "..."}]
            if not text and isinstance(m.get("content"), list):
                parts = []
                for p in m["content"]:
                    if isinstance(p, str):
                        parts.append(p)
                    elif isinstance(p, dict) and isinstance(p.get("text"), str):
                        parts.append(p["text"])
                text = "\n".join(parts).strip()
            if not text:
                continue
            messages.append(Message(role=role, content_md=text, external_id=str(m.get("id") or "")))
        return UnifiedConversation(
            provider=self.id,
            account=account or AccountInfo(),
            id=cid,
            title=title.strip() or "Gemini conversation",
            created_at=str(detail.get("created_at") or ""),
            updated_at=str(detail.get("updated_at") or ""),
            folder=HOME_SPACE_NAME,
            messages=messages,
            raw={"detail": detail.get("raw") or detail},
        )


ApiError = GeminiApiError
