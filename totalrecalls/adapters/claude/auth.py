"""Claude.ai account + org discovery."""

from __future__ import annotations

from totalrecalls.adapters.claude.http import ClaudeApiError, cookie_header_from_credential, request
from totalrecalls.core.schema import AccountInfo


def validate_credential(credential: str) -> tuple[AccountInfo, str, str]:
    """Return (account, cookie_header, organization_uuid)."""
    cookie = cookie_header_from_credential(credential)
    # bootstrap account
    status, me = request("/api/bootstrap", cookie, delay=0)
    # shapes vary; also try /api/account
    email = ""
    name = ""
    uid = ""
    if isinstance(me, dict):
        acc = me.get("account") if isinstance(me.get("account"), dict) else me
        email = str(acc.get("email") or acc.get("email_address") or "")
        name = str(acc.get("display_name") or acc.get("full_name") or "")
        uid = str(acc.get("uuid") or acc.get("id") or "")
    if not email:
        try:
            _s, acc2 = request("/api/account", cookie, delay=0)
            if isinstance(acc2, dict):
                email = str(acc2.get("email") or acc2.get("email_address") or email)
                name = str(acc2.get("display_name") or name)
                uid = str(acc2.get("uuid") or acc2.get("id") or uid)
        except ClaudeApiError:
            pass

    org_id = _first_org_id(cookie)
    if not org_id:
        raise ClaudeApiError("auth-failed")
    if not email and not uid:
        # session worked enough to list orgs
        email = name or "Claude user"
    return AccountInfo(email=email, external_id=uid, display_name=name), cookie, org_id


def _first_org_id(cookie: str) -> str:
    try:
        _s, data = request("/api/organizations", cookie, delay=0)
    except ClaudeApiError:
        return ""
    # list or {organizations: [...]}
    items = data if isinstance(data, list) else (data.get("organizations") if isinstance(data, dict) else None)
    if not isinstance(items, list):
        return ""
    for it in items:
        if isinstance(it, dict) and (it.get("uuid") or it.get("id")):
            return str(it.get("uuid") or it.get("id"))
    return ""
