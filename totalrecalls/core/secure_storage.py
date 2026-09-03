"""Small, dependency-free protected JSON storage for local secrets.

Windows uses the current user's DPAPI key. Other platforms use a private
file, since this application currently has no cross-platform key-management
dependency. Callers should treat read failures as an unavailable/expired
session rather than trusting unprotected input.
"""

from __future__ import annotations

import base64
import binascii
import ctypes
import json
import os
import uuid
from typing import Any


class SecureStorageError(RuntimeError):
    """Raised when protected local state cannot be read or written."""


def protection_backend() -> str:
    """Return the storage protection used on this host."""
    return "windows-dpapi" if os.name == "nt" else "private-file"


if os.name == "nt":
    class _DataBlob(ctypes.Structure):
        _fields_ = [
            ("cbData", ctypes.c_uint32),
            ("pbData", ctypes.POINTER(ctypes.c_ubyte)),
        ]


def _dpapi_transform(payload: bytes, protect: bool) -> bytes:
    if os.name != "nt":
        raise SecureStorageError("Windows DPAPI is not available on this host.")

    try:
        crypt32 = ctypes.WinDLL("Crypt32", use_last_error=True)
        kernel32 = ctypes.WinDLL("Kernel32", use_last_error=True)
        function = crypt32.CryptProtectData if protect else crypt32.CryptUnprotectData
        function.argtypes = [
            ctypes.POINTER(_DataBlob),
            ctypes.c_wchar_p,
            ctypes.POINTER(_DataBlob),
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.POINTER(_DataBlob),
        ]
        function.restype = ctypes.c_bool
        kernel32.LocalFree.argtypes = [ctypes.c_void_p]
        kernel32.LocalFree.restype = ctypes.c_void_p

        source = ctypes.create_string_buffer(payload)
        input_blob = _DataBlob(
            len(payload),
            ctypes.cast(source, ctypes.POINTER(ctypes.c_ubyte)),
        )
        output_blob = _DataBlob()
        if not function(
            ctypes.byref(input_blob),
            "TotalRecalls local state",
            None,
            None,
            None,
            0x1,  # CRYPTPROTECT_UI_FORBIDDEN
            ctypes.byref(output_blob),
        ):
            error = ctypes.get_last_error()
            raise SecureStorageError(f"Windows protected storage failed (error {error}).")
        try:
            return ctypes.string_at(output_blob.pbData, output_blob.cbData)
        finally:
            kernel32.LocalFree(output_blob.pbData)
    except SecureStorageError:
        raise
    except (AttributeError, OSError, TypeError, ValueError) as exc:
        raise SecureStorageError("Windows protected storage is unavailable.") from exc


def _encode(payload: bytes) -> bytes:
    if os.name == "nt":
        try:
            protected = _dpapi_transform(payload, protect=True)
            protection = "windows-dpapi"
        except SecureStorageError:
            # A locked-down Windows image can lack usable DPAPI.  Keep state
            # private and recoverable rather than silently writing plaintext.
            protected = payload
            protection = "private-file"
        envelope = {
            "version": 1,
            "protection": protection,
            "data": base64.b64encode(protected).decode("ascii"),
        }
        return json.dumps(envelope, separators=(",", ":")).encode("utf-8")
    envelope = {
        "version": 1,
        "protection": "private-file",
        "data": base64.b64encode(payload).decode("ascii"),
    }
    return json.dumps(envelope, separators=(",", ":")).encode("utf-8")


def _decode(raw: bytes) -> bytes:
    try:
        envelope = json.loads(raw.decode("utf-8"))
        if not isinstance(envelope, dict) or envelope.get("version") != 1:
            raise ValueError("invalid protection envelope")
        data = envelope.get("data")
        protection = envelope.get("protection")
        if not isinstance(data, str):
            raise ValueError("invalid protection envelope")
        if protection == "private-file":
            return base64.b64decode(data, validate=True)
        if protection == "windows-dpapi" and os.name == "nt":
            protected = base64.b64decode(data, validate=True)
            return _dpapi_transform(protected, protect=False)
        raise ValueError("unsupported protection envelope")
    except SecureStorageError:
        raise
    except (binascii.Error, ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        if os.name != "nt":
            # Read state written by versions before the private-file envelope.
            return raw
        raise SecureStorageError("Local state is not protected by Windows DPAPI.") from exc


def save_json(path: str, value: dict[str, Any]) -> None:
    """Atomically save a JSON object using the strongest local protection."""
    if not isinstance(value, dict):
        raise SecureStorageError("Protected local state must be a JSON object.")
    directory = os.path.dirname(os.path.abspath(path))
    temporary = None
    try:
        os.makedirs(directory, exist_ok=True)
        encoded = _encode(json.dumps(value, separators=(",", ":")).encode("utf-8"))
        temporary = f"{path}.{uuid.uuid4().hex}.tmp"
        with open(temporary, "wb") as handle:
            handle.write(encoded)
        if os.name != "nt":
            try:
                os.chmod(temporary, 0o600)
            except OSError:
                pass
        os.replace(temporary, path)
    except SecureStorageError:
        raise
    except (OSError, TypeError, ValueError) as exc:
        raise SecureStorageError(f"Unable to save protected local state: {exc}") from exc
    finally:
        try:
            if temporary and os.path.exists(temporary):
                os.remove(temporary)
        except OSError:
            pass


def load_json(path: str) -> dict[str, Any] | None:
    """Load a protected JSON object, or return ``None`` when it is absent."""
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
        value = json.loads(_decode(raw).decode("utf-8"))
    except FileNotFoundError:
        return None
    except SecureStorageError:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, TypeError) as exc:
        raise SecureStorageError("Local state is unreadable.") from exc
    if not isinstance(value, dict):
        raise SecureStorageError("Local state must contain a JSON object.")
    # The existing desktop bridge annotates session.json after it is written.
    # Preserve that non-secret metadata without exposing the encrypted payload.
    if os.name == "nt":
        try:
            envelope = json.loads(raw.decode("utf-8"))
            if isinstance(envelope, dict) and "provider" in envelope:
                value["provider"] = envelope["provider"]
        except (UnicodeDecodeError, json.JSONDecodeError):
            pass
    return value


def delete(path: str) -> None:
    """Delete local state and report failures other than a missing file."""
    try:
        os.remove(path)
    except FileNotFoundError:
        return
    except OSError as exc:
        raise SecureStorageError(f"Unable to remove local state: {exc}") from exc
