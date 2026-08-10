"""User-facing error messages."""

from __future__ import annotations


def friendly_error(e: Exception) -> str:
    msg = str(e)
    if msg == "auth-failed":
        return ("Your Perplexity session has expired. Please reconnect "
                "(click Disconnect, then Log in again).")
    if msg == "network":
        return "Could not reach Perplexity. Check your internet connection and try again."
    if msg.startswith("http-"):
        return f"Perplexity returned an error (HTTP {msg.split('-')[1]}). Please try again."
    return f"Something went wrong: {msg}"

