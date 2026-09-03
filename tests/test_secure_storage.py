import json
import os
import tempfile
import unittest

from totalrecalls.core import secure_storage
from totalrecalls.core.paths import (
    clear_session,
    consume_signin_callback,
    load_session,
    save_session,
    write_signin_callback,
)
from unittest.mock import patch


class SecureStorageTests(unittest.TestCase):
    def test_round_trip_and_protection_envelope(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "state.json")
            secret = "session-secret-value"
            secure_storage.save_json(path, {"token": secret, "email": "user@example.com"})
            self.assertEqual(
                secure_storage.load_json(path),
                {"token": secret, "email": "user@example.com"},
            )
            with open(path, "rb") as handle:
                raw = handle.read()
            if os.name == "nt":
                self.assertNotIn(secret.encode("utf-8"), raw)
                envelope = json.loads(raw.decode("utf-8"))
                self.assertEqual(envelope["protection"], "windows-dpapi")

    def test_windows_plaintext_state_is_rejected(self):
        if os.name != "nt":
            self.skipTest("Windows-only protection boundary")
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "legacy.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump({"token": "legacy-secret"}, handle)
            with self.assertRaises(secure_storage.SecureStorageError):
                secure_storage.load_json(path)


class SessionPersistenceTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._session = os.path.join(self._tmp.name, "session.json")
        self._callback = os.path.join(self._tmp.name, "callback.json")
        self._patchers = [
            patch("totalrecalls.core.paths.SESSION_FILE", self._session),
            patch("totalrecalls.core.paths.SIGNIN_CALLBACK_FILE", self._callback),
        ]
        for patcher in self._patchers:
            patcher.start()

    def tearDown(self):
        for patcher in reversed(self._patchers):
            patcher.stop()
        self._tmp.cleanup()

    def test_session_round_trip_and_clear(self):
        save_session("secret-token", "user@example.com")
        self.assertEqual(load_session()["token"], "secret-token")
        if os.name == "nt":
            with open(self._session, "rb") as handle:
                self.assertNotIn(b"secret-token", handle.read())
            # The desktop bridge adds provider metadata to the outer envelope.
            with open(self._session, encoding="utf-8") as handle:
                envelope = json.load(handle)
            envelope["provider"] = "perplexity"
            with open(self._session, "w", encoding="utf-8") as handle:
                json.dump(envelope, handle)
            self.assertEqual(load_session()["provider"], "perplexity")
        clear_session()
        self.assertIsNone(load_session())

    def test_signin_callback_is_one_time(self):
        write_signin_callback("callback-secret")
        self.assertEqual(consume_signin_callback(), "callback-secret")
        self.assertIsNone(consume_signin_callback())
