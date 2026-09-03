"""Free vs Pro entitlement.

The free tier (trial) lets users test the app on a limited set of providers
and conversations before paying. A one-time purchase unlocks Pro.

  Free: 3 providers, 5 conversations per download.
  Pro ($24 one-time): all 8 providers, unlimited downloads.

Pro is unlocked with a license key (issued by Lemon Squeezy on purchase). The
key must be verified by an explicit store integration before it is stored;
:func:`is_pro` reflects the stored entitlement. The app stays local-first —
there is no cloud check on every run.
"""

from __future__ import annotations

import os
import re
import time

from totalrecalls.core.paths import appdata_dir
from totalrecalls.core.secure_storage import (
    SecureStorageError,
    delete as delete_secure_state,
    load_json,
    save_json,
)

# Free-tier limits (mirrored in the UI and on the website).
FREE_PROVIDER_LIMIT = 3
FREE_CONVERSATION_LIMIT = 5
PRO_PRICE = "$24"

# The first FREE_PROVIDER_LIMIT provider ids are included free; the rest need Pro.
FREE_PROVIDER_IDS = ("perplexity", "chatgpt", "claude")

# Lemon Squeezy license keys are UUIDs. This regex checks only the shape;
# entitlement still requires an explicitly wired store verifier.
_LICENSE_KEY_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)

_LICENSE_FILE = os.path.join(appdata_dir(), "license.json")


def _load_state() -> dict:
    try:
        return load_json(_LICENSE_FILE) or {}
    except SecureStorageError:
        return {}


def _save_state(state: dict) -> None:
    save_json(_LICENSE_FILE, state)


def is_pro() -> bool:
    """True when a Pro license has been activated on this machine — or when
    this build is the unlocked buyer (Pro) edition, baked in at packaging time.
    """
    from totalrecalls.edition import is_pro_edition
    if is_pro_edition():
        return True
    return bool(_load_state().get("pro"))


def license_key() -> str:
    """The stored license key (or empty string)."""
    return str(_load_state().get("key") or "")


def tier_name() -> str:
    """Human-readable tier label: 'Pro' or 'Free'."""
    return "Pro" if is_pro() else "Free"


def validate_license_key_format(key: str) -> bool:
    """Check only the documented UUID shape; this does not prove entitlement."""
    return bool(_LICENSE_KEY_RE.match((key or "").strip()))


def validate_license_key(key: str, verifier=None) -> bool:
    """Validate a key with an explicitly supplied store verifier.

    Lemon Squeezy credentials and an API contract are intentionally not
    embedded here. Without a verifier this returns ``False`` so a UUID-shaped
    string cannot unlock production builds by itself.
    """
    key = (key or "").strip()
    if not validate_license_key_format(key) or verifier is None:
        return False
    try:
        return bool(verifier(key))
    except Exception:
        return False


def activate_license(key: str, verifier=None) -> dict:
    """Validate `key` and persist Pro, or explain why activation is unavailable."""
    key = (key or "").strip()
    if not key:
        return {"ok": False, "message": "Enter a license key."}
    if not validate_license_key_format(key):
        return {"ok": False, "message": "That license key is not valid."}
    if verifier is None:
        return {
            "ok": False,
            "message": "License validation is not configured yet; no license was activated.",
        }
    try:
        if not validate_license_key(key, verifier=verifier):
            return {"ok": False, "message": "That license key could not be verified."}
        _save_state({"pro": True, "key": key, "activated_at": int(time.time())})
    except SecureStorageError:
        return {
            "ok": False,
            "message": "Unable to securely save the license on this device.",
        }
    return {"ok": True, "message": "Pro unlocked — all 8 providers, unlimited downloads."}


def deactivate_license() -> dict:
    """Clear the local entitlement (support / moving machines)."""
    try:
        delete_secure_state(_LICENSE_FILE)
    except SecureStorageError:
        return {"ok": False, "message": "Unable to remove the local license safely."}
    return {"ok": True, "message": "License removed."}


def provider_is_free(provider_id: str) -> bool:
    """True when `provider_id` is part of the free tier."""
    return provider_id in FREE_PROVIDER_IDS


def provider_is_pro_only(provider_id: str) -> bool:
    """True when `provider_id` requires a Pro license."""
    return provider_id not in FREE_PROVIDER_IDS
