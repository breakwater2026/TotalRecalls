"""Gemini ProviderAdapter — Takeout/offline JSON primary; cookie secondary."""

from __future__ import annotations

from totalrecalls.adapters.gemini.http import (
    GeminiApiError,
    cookie_header_from_credential,
    load_offline_export,
    looks_like_path,
    request_json,
    BASE,
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
        # Cookie path — best-effort reachability probe
        cookie = cookie_header_from_credential(credential)
        try:
            # Hitting the app root; JSON may be empty HTML — network/auth errors matter
            request_json(BASE + "/app", cookie, delay=0)
        except GeminiApiError as e:
            # Some responses aren't JSON; only hard-fail auth/network codes
            if str(e) == "auth-failed":
                raise
            log(f"gemini cookie probe soft-fail: {e}")
        self._mode = "cookie"
        self._offline_cache = {}
        return AccountInfo(
            email="gemini-session@local",
            external_id="cookie",
            display_name="Gemini session",
        )

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
        # Live cookie listing is unstable (RPC batchexecute). Be honest.
        raise GeminiApiError(
            "Gemini live list requires Google Takeout JSON/folder path for now. "
            "Paste the path to your Takeout export (Gemini data) instead of cookies."
        )

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
        raise GeminiApiError(
            "Gemini live fetch not available; use Takeout export path as credential."
        )

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
            if not text:
                continue
            messages.append(Message(role=role, content_md=text, external_id=str(m.get("id") or "")))
        return UnifiedConversation(
            provider=self.id,
            account=account or AccountInfo(),
            id=cid,
            title=title,
            created_at=str(detail.get("created_at") or ""),
            updated_at=str(detail.get("updated_at") or ""),
            folder=HOME_SPACE_NAME,
            messages=messages,
            raw={"detail": detail.get("raw") or detail},
        )


ApiError = GeminiApiError
