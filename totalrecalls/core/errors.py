"""User-facing error messages + the shared auth-rejection classifier.

The classifier (``is_auth_rejected``) is the single source of truth for "is
this error a dead/expired credential?" across every provider. Historically
each provider's http layer raised the literal string ``auth-failed`` on 401/403
and the desktop bridge grepped for that exact substring. That worked for 7 of
the 8 providers, but DeepSeek signals a dead session differently (its JSON
envelope returns business codes ``api-40002`` Missing Token / ``api-40003``
Invalid Token, or a raw ``http-401``/``http-403``), so a dead DeepSeek token
slipped past the string gate and read as "Connected, 0 conversations."

Centralizing the recognition here makes the detection uniform and immune to
wording: any provider that surfaces a definitive session-death signal — under
any of the known markers — is treated the same way (prompt a re-auth) instead
of degrading to a silent zero.
"""

from __future__ import annotations


class AuthRejected(Exception):
    """Raised when a provider definitively rejects a credential as dead/expired.

    Distinct from a transient failure (network blip, 5xx, an API shape change)
    so callers can fail closed on a dead session while still tolerating a
    momentary hiccup. ``str(e)`` carries the underlying detail (e.g.
    ``"api-40002: Missing Token"``) for logging; the user never sees that raw
    form — see :func:`friendly_error`.
    """


# Definitive session-death markers, per provider:
#   "auth-failed"     — the shared string every http layer raises on 401/403
#                       (Perplexity, ChatGPT, Claude, Gemini, Grok, Mistral, Qwen).
#   "api-40002"       — DeepSeek envelope business code "Missing Token".
#   "api-40003"       — DeepSeek envelope business code "Invalid Token".
#   "http-401"/"http-403" — transport-level 401/403 (DeepSeek's request(), and any
#                       future provider that surfaces a raw 4xx auth reject).
# Deliberately NOT "http-400" (a bad request is not a dead session) and not 5xx
# (transient) — those must degrade to "0", never a false "expired" prompt.
_AUTH_REJECT_MARKERS = (
    "auth-failed",
    "api-40002",
    "api-40003",
    "http-401",
    "http-403",
)


def is_auth_rejected(e: Exception | str) -> bool:
    """Return True if ``e`` is a definitive session-death signal.

    Accepts an exception or a raw message string. True for the shared
    ``auth-failed`` string, an :class:`AuthRejected` instance, DeepSeek's
    ``api-40002``/``api-40003`` business codes, and raw ``http-401``/``http-403``
    rejections. False for transient failures (``network: …``, 5xx, a shape
    change) so those degrade to "0 conversations" rather than a false "expired".
    """
    if isinstance(e, AuthRejected):
        return True
    if isinstance(e, str):
        msg = e
    else:
        msg = str(e)
    for marker in _AUTH_REJECT_MARKERS:
        if marker in msg:
            return True
    return False


def friendly_error(e: Exception) -> str:
    if is_auth_rejected(e):
        return (
            "Your session was rejected or has expired. Please reconnect "
            "(Disconnect, then Log in again — or paste a fresh session token)."
        )
    msg = str(e)
    if msg == "network":
        return "Could not reach the provider. Check your internet connection and try again."
    if msg.startswith("http-"):
        code = msg.split("-", 1)[-1]
        return f"The provider returned an error (HTTP {code}). Please try again."
    return f"Something went wrong: {msg}"
