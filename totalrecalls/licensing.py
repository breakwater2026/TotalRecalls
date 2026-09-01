"""Free vs Pro entitlement.

The free tier (trial) lets users test the app on a limited set of providers
and conversations before paying. A one-time purchase unlocks Pro.

  Free: 3 providers, 5 conversations per download.
  Pro ($24 one-time): all 8 providers, unlimited downloads.

Pro is unlocked with a license key (issued by Lemon Squeezy on purchase). The
key is validated and stored locally; :func:`is_pro` reflects the stored
entitlement. The app stays local-first — there is no cloud check on every run.
"""

from __future__ import annotations

import json
import os
import re
import time

from totalrecalls.core.paths import appdata_dir

# Free-tier limits (mirrored in the UI and on the website).
FREE_PROVIDER_LIMIT = 3
FREE_CONVERSATION_LIMIT = 5
PRO_PRICE = "$24"

# The first FREE_PROVIDER_LIMIT provider ids are included free; the rest need Pro.
FREE_PROVIDER_IDS = ("perplexity", "chatgpt", "claude")

# Lemon Squeezy license keys are UUIDs. This regex only checks the *shape* so
# the free/pro gating can be exercised before the store is live. Replace
# validate_license_key() with the real Lemon Squeezy license API before launch.
_LICENSE_KEY_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)

_LICENSE_FILE = os.path.join(appdata_dir(), "license.json")


def _load_state() -> dict:
    try:
        with open(_LICENSE_FILE, encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save_state(state: dict) -> None:
    os.makedirs(os.path.dirname(_LICENSE_FILE), exist_ok=True)
    with open(_LICENSE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def is_pro() -> bool:
    """True when a Pro license has been activated on this machine."""
    return bool(_load_state().get("pro"))


def license_key() -> str:
    """The stored license key (or empty string)."""
    return str(_load_state().get("key") or "")


def tier_name() -> str:
    """Human-readable tier label: 'Pro' or 'Free'."""
    return "Pro" if is_pro() else "Free"


def validate_license_key(key: str) -> bool:
    """Validate a license key.

    TODO(launch): call Lemon Squeezy's license API instead of the shape check::

        POST https://api.lemonsqueezy.com/v1/licenses/activate
        {"license_key": key, "instance_name": "TotalRecalls-<machine-id>"}

    The product is still in draft, so no real keys exist yet — this accepts any
    UUID-shaped key purely so the free/pro gating can be smoke-tested end to end.
    """
    return bool(_LICENSE_KEY_RE.match((key or "").strip()))


def activate_license(key: str) -> dict:
    """Validate `key` and persist Pro. Returns ``{"ok": bool, "message": str}``."""
    key = (key or "").strip()
    if not key:
        return {"ok": False, "message": "Enter a license key."}
    if not validate_license_key(key):
        return {"ok": False, "message": "That license key is not valid."}
    _save_state({"pro": True, "key": key, "activated_at": int(time.time())})
    return {"ok": True, "message": "Pro unlocked — all 8 providers, unlimited downloads."}


def deactivate_license() -> dict:
    """Clear the local entitlement (support / moving machines)."""
    try:
        if os.path.exists(_LICENSE_FILE):
            os.remove(_LICENSE_FILE)
    except Exception:
        pass
    return {"ok": True, "message": "License removed."}


def provider_is_free(provider_id: str) -> bool:
    """True when `provider_id` is part of the free tier."""
    return provider_id in FREE_PROVIDER_IDS


def provider_is_pro_only(provider_id: str) -> bool:
    """True when `provider_id` requires a Pro license."""
    return provider_id not in FREE_PROVIDER_IDS
