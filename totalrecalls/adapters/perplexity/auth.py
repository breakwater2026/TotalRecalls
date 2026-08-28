"""Perplexity session token extraction and validation."""

from __future__ import annotations

import json
import os

from totalrecalls.core.paths import appdata_dir, log
from totalrecalls.adapters.perplexity.http import COOKIE_NAME, ApiError, request, API_VERSION

def extract_session_token_from_cookie_header(cookie_header: str | None) -> str | None:
    if not cookie_header:
        return None
    for part in cookie_header.split(";"):
        part = part.strip()
        if not part:
            continue
        if part.startswith(COOKIE_NAME + "="):
            value = part[len(COOKIE_NAME) + 1:]
            return value or None
    return None


def extract_session_token_from_cookie_records(cookie_records) -> str | None:
    """Accept plain dicts OR WebView2 CoreWebView2Cookie COM objects (.Name/.Value)."""
    if not cookie_records:
        return None
    try:
        iterator = list(cookie_records)
    except Exception:
        iterator = cookie_records
    for record in iterator:
        try:
            if isinstance(record, dict):
                name = record.get("name") or record.get("Name")
                value = record.get("value") or record.get("Value")
            else:
                name = getattr(record, "Name", None) or getattr(record, "name", None)
                value = getattr(record, "Value", None) or getattr(record, "value", None)
            if name == COOKIE_NAME and value:
                return str(value)
        except Exception:
            continue
    return None


def extract_session_token_from_cdp_json(raw: str | None) -> str | None:
    """Parse JSON returned by CDP Network.getCookies / Network.getAllCookies."""
    if not raw:
        return None
    try:
        data = json.loads(raw)
    except Exception:
        return None
    cookies = data.get("cookies") if isinstance(data, dict) else None
    if not cookies:
        return None
    # Also remember Cloudflare cookies (cf_clearance / __cf_bm) so export
    # requests can present them — without them Cloudflare challenges the
    # bare session cookie after ~10 rapid thread fetches (HTTP 403).
    try:
        cf_parts = []
        for cookie in cookies:
            if isinstance(cookie, dict):
                nm = cookie.get("name") or ""
                val = cookie.get("value") or ""
                if nm in ("cf_clearance", "__cf_bm") and val:
                    cf_parts.append(f"{nm}={val}")
        if cf_parts:
            save_cf_cookies("; ".join(cf_parts))
    except Exception:
        pass
    for cookie in cookies:
        try:
            if not isinstance(cookie, dict):
                continue
            if cookie.get("name") == COOKIE_NAME and cookie.get("value"):
                return str(cookie["value"])
        except Exception:
            continue
    return None


def _cf_cookie_path() -> str:
    import os as _os
    from totalrecalls.core.paths import appdata_dir as _ad
    return _os.path.join(_ad(), "perplexity_cf_cookies.txt")


def save_cf_cookies(header: str):
    try:
        with open(_cf_cookie_path(), "w", encoding="utf-8") as f:
            f.write(header)
        from totalrecalls.core.paths import log as _log
        _log("auth: saved Cloudflare cookies for export requests")
    except Exception:
        pass


def load_cf_cookies() -> str:
    try:
        with open(_cf_cookie_path(), encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""


def validate_session(token: str) -> dict:
    status, data = request(f"/api/auth/session?version={API_VERSION}&source=default", token, delay=0)
    return data if isinstance(data, dict) else {}


def detect_session_token_from_browser_store() -> str | None:
    """Probe common Chromium/Edge browser cookie stores for an active Perplexity session."""
    try:
        import base64
        import ctypes
        import json
        import sqlite3
        import tempfile
        from ctypes import wintypes

        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except Exception as e:
        log(f"browser-store probe unavailable: {e}")
        return None

    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        return None

    user_data_roots = [
        os.path.join(local_appdata, "Google", "Chrome", "User Data"),
        os.path.join(local_appdata, "Microsoft", "Edge", "User Data"),
        os.path.join(local_appdata, "BraveSoftware", "Brave-Browser", "User Data"),
        os.path.join(local_appdata, "Chromium", "User Data"),
        os.path.join(local_appdata, "Programs", "Perplexity"),
        os.path.join(appdata_dir(), "login-webview"),
    ]

    appdata = os.environ.get("APPDATA")
    if appdata:
        user_data_roots.extend([
            os.path.join(appdata, "Perplexity"),
            os.path.join(appdata, "PerplexityExporter", "login-webview"),
        ])

    for user_data_root in user_data_roots:
        if not os.path.isdir(user_data_root):
            continue
        try:
            for root, _, _ in os.walk(user_data_root):
                if os.path.basename(root) != "Network":
                    continue
                cookie_db = os.path.join(root, "Cookies")
                if not os.path.exists(cookie_db):
                    continue
                state_path = os.path.join(user_data_root, "Local State")
                if not os.path.exists(state_path):
                    continue
                with open(state_path, encoding="utf-8") as fh:
                    state = json.load(fh)
                enc_key_b64 = (state.get("os_crypt") or {}).get("encrypted_key", "")
                if not enc_key_b64:
                    continue
                enc_key = base64.b64decode(enc_key_b64)
                if enc_key[:5] == b"DPAPI":
                    enc_key = enc_key[5:]
                else:
                    continue

                class DATA_BLOB(ctypes.Structure):
                    _fields_ = [("cbData", wintypes.DWORD),
                                ("pbData", ctypes.POINTER(ctypes.c_char))]

                crypt32 = ctypes.windll.crypt32
                kernel32 = ctypes.windll.kernel32
                in_blob = DATA_BLOB(len(enc_key), ctypes.cast(ctypes.create_string_buffer(enc_key), ctypes.POINTER(ctypes.c_char)))
                out_blob = DATA_BLOB()
                if not crypt32.CryptUnprotectData(ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob)):
                    continue
                try:
                    aes_key = ctypes.string_at(out_blob.pbData, out_blob.cbData)
                finally:
                    kernel32.LocalFree(out_blob.pbData)

                con = None
                try:
                    con = sqlite3.connect(f"file:{cookie_db}?mode=ro", uri=True)
                    rows = con.execute(
                        "SELECT host_key, name, value, encrypted_value FROM cookies WHERE name = ?",
                        (COOKIE_NAME,)
                    ).fetchall()
                except Exception:
                    try:
                        tmp_db = os.path.join(tempfile.gettempdir(), "px_browser_cookies.sqlite")
                        import shutil
                        shutil.copy2(cookie_db, tmp_db)
                        con = sqlite3.connect(tmp_db)
                        rows = con.execute(
                            "SELECT host_key, name, value, encrypted_value FROM cookies WHERE name = ?",
                            (COOKIE_NAME,)
                        ).fetchall()
                    except Exception:
                        rows = []
                finally:
                    if con is not None:
                        con.close()

                for _, name, value, enc_value in rows:
                    try:
                        blob = enc_value or value
                        if not blob:
                            continue
                        if isinstance(blob, bytes):
                            blob = blob.decode("utf-8", "replace")
                        if not isinstance(blob, str):
                            continue
                        if not blob.startswith("v10"):
                            return str(blob)
                        body = blob[3:]
                        raw = base64.b64decode(body)
                        nonce, ct = raw[:12], raw[12:]
                        token = AESGCM(aes_key).decrypt(nonce, ct, None).decode("utf-8", "replace")
                        if token:
                            return token
                    except Exception:
                        continue
        except Exception as e:
            log(f"browser-store probe error for {user_data_root}: {e}")
    return None

