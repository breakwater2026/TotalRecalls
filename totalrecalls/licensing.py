"""Free vs Pro entitlement.

The free tier (trial) lets users test the app on a limited set of providers
and conversations before paying. A one-time purchase unlocks Pro.

  Free: 3 providers, 5 conversations per download.
  Pro ($24 one-time): all 8 providers, unlimited downloads.

Pro is unlocked with a license key issued by Lemon Squeezy on purchase.
The key is verified against the public Lemon Squeezy License API at
activation time (``licensing.lemonsqueezy_verifier``); each activation
registers this machine as an instance, and the store is configured to allow
3 activations per purchase. The entitlement is stored locally
(``license.json``) so the app stays local-first: a periodic best-effort
re-validation (``check_entitlement``) only revokes on a definitive
``valid=False`` from the store — an offline machine keeps its Pro. The
baked-in Pro edition (``totalrecalls.edition``) remains as an internal
build flag; public distribution ships the single free build + key.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import time
import urllib.parse
import urllib.request
import uuid

from totalrecalls.core.paths import appdata_dir
from totalrecalls.core.secure_storage import (
    SecureStorageError,
    delete as delete_secure_state,
    load_json,
    save_json,
)

# Lemon Squeezy License API (public endpoints — no merchant secret required):
#   POST /v1/licenses/activate   (license_key + instance_name)
#   POST /v1/licenses/validate   (license_key [+ instance_id])
#   POST /v1/licenses/deactivate (license_key + instance_id)
LS_LICENSE_API = "https://api.lemonsqueezy.com/v1/licenses"
# Re-validate a stored entitlement at most once per hour, best-effort only:
# a stored Pro entitlement is never revoked because we are offline.
_REVALIDATE_INTERVAL = 3600

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
_MACHINE_ID_FILE = os.path.join(appdata_dir(), "machine-id.txt")


def _load_state() -> dict:
    try:
        return load_json(_LICENSE_FILE) or {}
    except SecureStorageError:
        return {}


def _save_state(state: dict) -> None:
    save_json(_LICENSE_FILE, state)


def _win32_query(name: str) -> str:
    """Best-effort WMI read of a single property (returns '' on any failure)."""
    if os.name != "nt":
        return ""
    try:
        out = subprocess.run(
            ["wmic", name, "get", "UUID"],
            capture_output=True, text=True, timeout=5,
        )
        for line in (out.stdout or "").splitlines():
            line = line.strip()
            if line and line.upper() != "UUID":
                return line
    except (OSError, subprocess.SubprocessError):
        pass
    return ""


def machine_identity() -> str:
    """A pseudonymous, stable-per-machine identifier used as the LS
    activation instance name.

    It is derived from hardware (motherboard UUID where available, MAC
    otherwise) and a per-install salt — no personal data, no account. The
    salt makes the value opaque to the store: Lemon Squeezy only ever sees
    an opaque instance name, never hardware details.
    """
    salt = ""
    try:
        if os.path.exists(_MACHINE_ID_FILE):
            with open(_MACHINE_ID_FILE, "r", encoding="utf-8") as f:
                salt = f.read().strip()
    except OSError:
        salt = ""
    if not salt:
        salt = uuid.uuid4().hex
        try:
            with open(_MACHINE_ID_FILE, "w", encoding="utf-8") as f:
                f.write(salt)
        except OSError:
            pass  # read-only home: identity is still stable via the salt
    base = ""
    if os.name == "nt":
        base = _win32_query("win32_computersystemproductid")
    if not base:
        try:
            base = uuid.getnode()
        except Exception:
            base = os.environ.get("COMPUTERNAME", "unknown")
    digest = hashlib.sha256(f"{base}:{salt}".encode("utf-8")).digest()
    return "TR-" + digest[:10].hex().upper()


def _ls_post(path: str, fields: dict, timeout: int = 12) -> dict:
    """POST to the public Lemon Squeezy License API. Returns the parsed JSON
    body. Raises ``OSError`` on network failure (distinct from a rejected
    key, which the API reports with valid=False)."""
    url = f"{LS_LICENSE_API}/{path}"
    data = urllib.parse.urlencode(fields).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def lemonsqueezy_verifier(key: str, activate: bool = True) -> bool:
    """Store verifier for the public Lemon Squeezy License API.

    ``activate=True`` registers this machine as an instance (the one-time
    activation on key entry); ``activate=False`` only validates (used for
    periodic best-effort re-checks of a stored entitlement). Returns True
    only on an explicit valid response; network failures raise.
    """
    if activate:
        fields = {"license_key": key, "instance_name": machine_identity()}
        resp = _ls_post("activate", fields)
        ok = resp.get("activated")
        # Per LS docs the activate response carries instance.id (a UUID string).
        instance = resp.get("instance") or {}
        instance_id = str(instance.get("id") or "")
    else:
        fields = {"license_key": key}
        instance_id = str(_load_state().get("instance_id") or "")
        if instance_id:
            fields["instance_id"] = instance_id
        resp = _ls_post("validate", fields)
        ok = resp.get("valid")
    if not isinstance(resp, dict) or not ok:
        return False
    if activate and instance_id:
        state = _load_state()
        state["instance_id"] = instance_id
        _save_state(state)
    return True


def is_pro() -> bool:
    """True when a Pro license has been activated on this machine — or when
    this build is the unlocked buyer (Pro) edition, baked in at packaging time.

    This is a fast local check (no network): entitlement is established at
    activation time via the store verifier, and re-checked best-effort at
    startup through :func:`check_entitlement` so this never blocks the UI.
    """
    from totalrecalls.edition import is_pro_edition
    if is_pro_edition():
        return True
    return bool(_load_state().get("pro"))


def check_entitlement() -> bool:
    """Best-effort re-check of a stored Pro entitlement at startup.

    Rate-limited to one network call per hour. Offline / unreachable keeps
    the stored entitlement (grace); an explicit ``valid=False`` from Lemon
    Squeezy revokes it. Returns the effective Pro status. Safe to call when
    there is no stored entitlement (returns False immediately).
    """
    state = _load_state()
    if not state.get("pro"):
        return False
    last = int(state.get("last_validated_at") or 0)
    if time.time() - last < _REVALIDATE_INTERVAL:
        return True
    try:
        ok = lemonsqueezy_verifier(str(state.get("key") or ""), activate=False)
    except (OSError, ValueError):
        ok = None  # offline / malformed response: keep the stored entitlement
    if ok is False:
        # The store says the key is not valid (disabled/expired). LS is the
        # source of truth — clear the stale local entitlement.
        try:
            delete_secure_state(_LICENSE_FILE)
        except SecureStorageError:
            pass
        return False
    try:
        state["last_validated_at"] = int(time.time())
        _save_state(state)
    except SecureStorageError:
        pass
    return True


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
    """Validate ``key`` and persist Pro, or explain why activation failed.

    With no explicit ``verifier`` this uses the Lemon Squeezy License API:
    a one-time activation that registers this machine as an instance
    (3 activations per purchase by store configuration). A network failure
    is reported as such so the user can retry; a key the store rejects is
    reported as unverified. An explicit ``verifier`` (tests or an
    alternative store) bypasses the network entirely.
    """
    key = (key or "").strip()
    if not key:
        return {"ok": False, "message": "Enter a license key."}
    if not validate_license_key_format(key):
        return {"ok": False, "message": "That license key is not a valid TotalRecalls key."}
    if verifier is not None:
        # Explicit verifier (tests / alternative store): no network.
        if not validate_license_key(key, verifier=verifier):
            return {"ok": False, "message": "That license key could not be verified."}
        try:
            _persist_pro(key)
        except SecureStorageError:
            return {
                "ok": False,
                "message": "Unable to securely save the license on this device.",
            }
        return {"ok": True, "message": "Pro unlocked — all 8 providers, unlimited downloads."}
    # Default: Lemon Squeezy activation (one-time, registers this machine).
    try:
        ok = lemonsqueezy_verifier(key, activate=True)
    except (OSError, ValueError):
        return {
            "ok": False,
            "message": "Could not reach the license server. Check your internet connection and try again.",
        }
    if not ok:
        return {"ok": False, "message": "That license key could not be verified."}
    try:
        _persist_pro(key)
    except SecureStorageError:
        return {
            "ok": False,
            "message": "Unable to securely save the license on this device.",
        }
    return {"ok": True, "message": "Pro unlocked — all 8 providers, unlimited downloads."}


def _persist_pro(key: str) -> None:
    """Persist a verified Pro entitlement (raises SecureStorageError)."""
    now = int(time.time())
    state = {
        "pro": True,
        "key": key,
        "activated_at": now,
        "last_validated_at": now,
    }
    instance_id = str(_load_state().get("instance_id") or "")
    if instance_id:
        state["instance_id"] = instance_id
    _save_state(state)


def deactivate_license() -> dict:
    """Clear the local entitlement and, best-effort, free this machine's
    Lemon Squeezy activation slot (support / moving machines).
    """
    state = _load_state()
    key = str(state.get("key") or "")
    instance_id = str(state.get("instance_id") or "")
    slot_result = "unknown"
    if key and instance_id:
        try:
            _ls_post("deactivate", {"license_key": key, "instance_id": instance_id})
            slot_result = "freed"
        except (OSError, ValueError):
            slot_result = "offline"
    try:
        delete_secure_state(_LICENSE_FILE)
    except SecureStorageError:
        return {"ok": False, "message": "Unable to remove the local license safely."}
    if slot_result == "freed":
        return {"ok": True, "message": "License removed. This machine's activation slot is freed."}
    if slot_result == "offline":
        return {
            "ok": True,
            "message": "License removed on this device. We could not reach the license "
                       "server to free the activation slot — email support if you need it back.",
        }
    return {"ok": True, "message": "License removed."}


def provider_is_free(provider_id: str) -> bool:
    """True when `provider_id` is part of the free tier."""
    return provider_id in FREE_PROVIDER_IDS


def provider_is_pro_only(provider_id: str) -> bool:
    """True when `provider_id` requires a Pro license."""
    return provider_id not in FREE_PROVIDER_IDS
