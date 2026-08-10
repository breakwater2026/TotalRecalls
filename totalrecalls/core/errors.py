"""User-facing error messages."""

from __future__ import annotations


def friendly_error(e: Exception) -> str:
    msg = str(e)
    if msg == "auth-failed":
        return (
            "Your session was rejected or has expired. Please reconnect "
            "(Disconnect, then Log in again — or paste a fresh session token)."
        )
    if msg == "network":
        return "Could not reach the provider. Check your internet connection and try again."
    if msg.startswith("http-"):
        code = msg.split("-", 1)[-1]
        return f"The provider returned an error (HTTP {code}). Please try again."
    return f"Something went wrong: {msg}"
