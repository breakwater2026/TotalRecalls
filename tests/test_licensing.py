"""Licensing: free/pro entitlement + Paddle-based license key validation."""

from __future__ import annotations

import os
import tempfile
import time
import unittest
from unittest.mock import patch

from totalrecalls import licensing
from totalrecalls.core.secure_storage import SecureStorageError

KEY = "TR-ABCD1234-EF56-7890"


class ProviderTierTests(unittest.TestCase):
    def test_free_tier_constants(self):
        self.assertEqual(licensing.FREE_PROVIDER_IDS, ("perplexity", "chatgpt", "claude"))
        self.assertEqual(licensing.FREE_PROVIDER_LIMIT, 3)
        self.assertEqual(licensing.FREE_CONVERSATION_LIMIT, 5)

    def test_provider_tier_helpers(self):
        self.assertTrue(licensing.provider_is_free("perplexity"))
        self.assertFalse(licensing.provider_is_free("gemini"))
        self.assertFalse(licensing.provider_is_pro_only("chatgpt"))
        self.assertTrue(licensing.provider_is_pro_only("grok"))


class LicenseKeyValidationTests(unittest.TestCase):
    def test_valid_key_shape_does_not_prove_entitlement(self):
        self.assertTrue(licensing.validate_license_key_format(KEY))
        self.assertFalse(licensing.validate_license_key(KEY))

    def test_explicit_verifier_is_required_and_used(self):
        verifier = lambda candidate: candidate == KEY
        self.assertTrue(licensing.validate_license_key(KEY, verifier=verifier))

    def test_invalid_keys(self):
        for bad in ("", "nope", "1234", "TR-ABCD", "tr-abcd1234-ef567890"):
            self.assertFalse(licensing.validate_license_key_format(bad), bad)


class EntitlementPersistenceTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._license_path = os.path.join(self._tmp.name, "license.json")
        self._machine_id_path = os.path.join(self._tmp.name, "machine-id.txt")
        self._patches = [
            patch.object(licensing, "_LICENSE_FILE", self._license_path),
            patch.object(licensing, "_MACHINE_ID_FILE", self._machine_id_path),
        ]
        for p in self._patches:
            p.start()

    def tearDown(self):
        for p in self._patches:
            p.stop()
        self._tmp.cleanup()

    def test_free_by_default(self):
        self.assertFalse(licensing.is_pro())
        self.assertEqual(licensing.tier_name(), "Free")

    def test_activate_with_explicit_verifier(self):
        res = licensing.activate_license(KEY, verifier=lambda candidate: candidate == KEY)
        self.assertTrue(res["ok"])
        self.assertTrue(licensing.is_pro())
        self.assertEqual(licensing.tier_name(), "Pro")
        self.assertEqual(licensing.license_key(), KEY)

    def test_default_path_reaches_verifier_offline(self):
        # No explicit verifier -> default Paddle verification path; with the
        # network unavailable the key must NOT activate, with a retry
        # message.
        with patch.object(licensing, "_verify_post", side_effect=OSError("no network")):
            res = licensing.activate_license(KEY)
        self.assertFalse(res["ok"])
        self.assertIn("license server", res["message"])
        self.assertFalse(licensing.is_pro())

    def test_activate_invalid_key(self):
        res = licensing.activate_license("not-a-key")
        self.assertFalse(res["ok"])
        self.assertFalse(licensing.is_pro())

    def test_activate_reports_secure_storage_failure(self):
        with patch.object(
            licensing,
            "_save_state",
            side_effect=SecureStorageError("unavailable"),
        ):
            res = licensing.activate_license(KEY, verifier=lambda _: True)
        self.assertFalse(res["ok"])
        self.assertIn("securely save", res["message"])
        self.assertFalse(licensing.is_pro())

    def test_deactivate(self):
        licensing.activate_license(KEY, verifier=lambda _: True)
        self.assertTrue(licensing.is_pro())
        licensing.deactivate_license()
        self.assertFalse(licensing.is_pro())

    def test_reset_local_clears_pro_without_server(self):
        licensing.activate_license(KEY, verifier=lambda _: True)
        self.assertTrue(licensing.is_pro())
        # reset_local_license must NOT touch the network (dev flow).
        with patch.object(licensing, "_verify_post", side_effect=AssertionError("server touched")):
            res = licensing.reset_local_license()
        self.assertTrue(res["ok"])
        self.assertFalse(licensing.is_pro())
        self.assertEqual(licensing.tier_name(), "Free")

    def test_reset_local_idempotent_when_free(self):
        self.assertFalse(licensing.is_pro())
        res = licensing.reset_local_license()
        self.assertTrue(res["ok"])
        self.assertIn("Free", res["message"])

    def test_reset_local_reports_secure_storage_failure(self):
        licensing.activate_license(KEY, verifier=lambda _: True)
        with patch.object(
            licensing, "delete_secure_state", side_effect=SecureStorageError("unavailable")
        ):
            res = licensing.reset_local_license()
        self.assertFalse(res["ok"])
        self.assertTrue(licensing.is_pro())


class PaddleVerifierTests(unittest.TestCase):
    """Paddle license verification integration, with the network mocked out."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._license_path = os.path.join(self._tmp.name, "license.json")
        self._machine_id_path = os.path.join(self._tmp.name, "machine-id.txt")
        self._patches = [
            patch.object(licensing, "_LICENSE_FILE", self._license_path),
            patch.object(licensing, "_MACHINE_ID_FILE", self._machine_id_path),
        ]
        for p in self._patches:
            p.start()

    def tearDown(self):
        for p in self._patches:
            p.stop()
        self._tmp.cleanup()

    def _seed_pro(self, last_validated_at=None, instance_id=None):
        state = {"pro": True, "key": KEY, "activated_at": int(time.time())}
        if last_validated_at is not None:
            state["last_validated_at"] = last_validated_at
        if instance_id is not None:
            state["instance_id"] = instance_id
        licensing._save_state(state)

    def test_machine_identity_is_stable_and_pseudonymous(self):
        a = licensing.machine_identity()
        b = licensing.machine_identity()
        self.assertEqual(a, b)
        self.assertTrue(a.startswith("TR-"))
        self.assertNotIn(KEY, a)  # never contains the key
        self.assertLessEqual(len(a), 23)

    def test_activate_via_verifier_success(self):
        # Paddle verifier response shape: {"valid": bool, "instance_id": str}
        resp = {"valid": True, "instance_id": "inst-abc123"}
        with patch.object(licensing, "_verify_post", return_value=resp) as mock_post:
            res = licensing.activate_license(KEY)
        self.assertTrue(res["ok"])
        self.assertTrue(licensing.is_pro())
        # activation sends license_key + machine identity
        args, _ = mock_post.call_args
        payload = args[0] if args else {}
        self.assertEqual(payload.get("license_key"), KEY)
        self.assertIn("instance_name", payload)
        # instance id captured for future validate/deactivate
        self.assertEqual(
            licensing._load_state().get("instance_id"),
            "inst-abc123",
        )

    def test_activate_rejected_by_store(self):
        with patch.object(licensing, "_verify_post", return_value={"valid": False}):
            res = licensing.activate_license(KEY)
        self.assertFalse(res["ok"])
        self.assertIn("could not be verified", res["message"])
        self.assertFalse(licensing.is_pro())

    def test_activate_network_failure_is_distinct_from_rejection(self):
        with patch.object(licensing, "_verify_post", side_effect=OSError("timeout")):
            res = licensing.activate_license(KEY)
        self.assertFalse(res["ok"])
        self.assertIn("license server", res["message"])
        self.assertFalse(licensing.is_pro())

    def test_check_entitlement_offline_grace(self):
        self._seed_pro(last_validated_at=0)  # stale -> re-check fires
        with patch.object(licensing, "_verify_post", side_effect=OSError("offline")):
            self.assertTrue(licensing.check_entitlement())
        self.assertTrue(licensing.is_pro())  # offline keeps Pro

    def test_check_entitlement_revokes_on_definitive_invalid(self):
        self._seed_pro(last_validated_at=0)
        with patch.object(licensing, "_verify_post", return_value={"valid": False}):
            self.assertFalse(licensing.check_entitlement())

    def test_check_entitlement_rate_limited_within_interval(self):
        self._seed_pro(last_validated_at=int(time.time()))  # fresh
        with patch.object(licensing, "_verify_post") as mock_post:
            self.assertTrue(licensing.check_entitlement())
            mock_post.assert_not_called()

    def test_check_entitlement_noop_when_free(self):
        with patch.object(licensing, "_verify_post") as mock_post:
            self.assertFalse(licensing.check_entitlement())
            mock_post.assert_not_called()

    def test_check_entitlement_validates_stored_instance(self):
        self._seed_pro(last_validated_at=0, instance_id="inst-1")
        with patch.object(licensing, "_verify_post", return_value={"valid": True}) as mock_post:
            self.assertTrue(licensing.check_entitlement())
        args, _ = mock_post.call_args
        payload = args[0] if args else {}
        self.assertEqual(payload.get("instance_id"), "inst-1")

    def test_deactivate_frees_activation_slot(self):
        self._seed_pro(instance_id="inst-1")
        with patch.object(licensing, "_verify_post", return_value={}) as mock_post:
            res = licensing.deactivate_license()
        self.assertTrue(res["ok"])
        self.assertIn("freed", res["message"])
        args, _ = mock_post.call_args
        payload = args[0] if args else {}
        self.assertEqual(payload.get("license_key"), KEY)
        self.assertEqual(payload.get("instance_id"), "inst-1")
        self.assertIn("action", payload)
        self.assertEqual(payload["action"], "deactivate")
        self.assertFalse(licensing.is_pro())

    def test_deactivate_offline_still_removes_locally(self):
        self._seed_pro(instance_id="inst-1")
        with patch.object(licensing, "_verify_post", side_effect=OSError("offline")):
            res = licensing.deactivate_license()
        self.assertTrue(res["ok"])
        self.assertIn("email support", res["message"])
        self.assertFalse(licensing.is_pro())


if __name__ == "__main__":
    unittest.main()