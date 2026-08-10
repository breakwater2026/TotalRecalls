"""ChatGPT credential resolution and session validation."""

from __future__ import annotations

from totalrecalls.adapters.chatgpt.http import ChatGptApiError, request
from totalrecalls.core.schema import AccountInfo


def looks_like_bearer_token(value: str) -> bool:
    v = (value or "").strip()
    if not v:
        return False
    # JWT-ish access tokens used by ChatGPT web often start with eyJ
    if v.startswith("eyJ") and v.count(".") >= 2:
        return True
    # Some captures include "Bearer "
    if v.lower().startswith("bearer ") and len(v) > 20:
        return True
    return False


def normalize_bearer(value: str) -> str:
    v = (value or "").strip()
    if v.lower().startswith("bearer "):
        return v[7:].strip()
    return v


def cookie_header_from_session_token(session_token: str) -> str:
    """Build a Cookie header from a pasted session-token value."""
    tok = (session_token or "").strip()
    if "session-token=" in tok or "__Secure-next-auth" in tok:
        # User pasted a full Cookie header fragment
        return tok if "Cookie:" not in tok else tok.split(":", 1)[-1].strip()
    return f"__Secure-next-auth.session-token={tok}"


def fetch_session(*, access_token: str | None = None, cookie: str | None = None) -> dict:
    status, data = request(
        "/api/auth/session",
        access_token=access_token,
        cookie=cookie,
        delay=0,
    )
    if not isinstance(data, dict):
        return {}
    return data


def resolve_access_token(credential: str) -> tuple[str, dict]:
    """Return (access_token, session_dict) from bearer or session-cookie credential."""
    cred = (credential or "").strip()
    if not cred:
        raise ChatGptApiError("auth-failed")

    if looks_like_bearer_token(cred):
        token = normalize_bearer(cred)
        session = fetch_session(access_token=token)
        # Session may be empty when only bearer works for backend-api; still OK
        if session.get("error"):
            raise ChatGptApiError("auth-failed")
        # Prefer refreshed accessToken if present
        at = session.get("accessToken") or token
        return str(at), session

    # Treat as session cookie / cookie header
    cookie = cookie_header_from_session_token(cred)
    session = fetch_session(cookie=cookie)
    at = session.get("accessToken")
    if not at:
        raise ChatGptApiError("auth-failed")
    return str(at), session


def account_from_session(session: dict) -> AccountInfo:
    user = session.get("user") if isinstance(session.get("user"), dict) else {}
    user = user or {}
    email = str(user.get("email") or session.get("email") or "")
    return AccountInfo(
        email=email,
        external_id=str(user.get("id") or user.get("email") or ""),
        display_name=str(user.get("name") or user.get("email") or ""),
    )


def validate_credential(credential: str) -> tuple[AccountInfo, str]:
    """Validate and return (account, access_token)."""
    access_token, session = resolve_access_token(credential)
    account = account_from_session(session)
    # backend-api often works with bearer even if session user missing —
    # require *some* identity signal OR a non-empty token
    if not access_token:
        raise ChatGptApiError("auth-failed")
    if not account.email and not account.external_id:
        # Still accept bare bearer: use truncated token as id for manifests
        account = AccountInfo(email="", external_id=access_token[:12] + "…", display_name="ChatGPT user")
    return account, access_token
