"""Licensing: free/pro entitlement + license key validation."""

from __future__ import annotations

import os
import tempfile
import unittest
from unittest.mock import patch

from totalrecalls import licensing


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
    def test_valid_uuid_key(self):
        self.assertTrue(licensing.validate_license_key("03e11a51-8c63-4826-8b87-998b626285c3"))

    def test_invalid_keys(self):
        for bad in ("", "nope", "1234", "03e11a51-8c63-4826-8b87"):
            self.assertFalse(licensing.validate_license_key(bad), bad)


class EntitlementPersistenceTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._license_path = os.path.join(self._tmp.name, "license.json")
        self._patcher = patch.object(licensing, "_LICENSE_FILE", self._license_path)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()
        self._tmp.cleanup()

    def test_free_by_default(self):
        self.assertFalse(licensing.is_pro())
        self.assertEqual(licensing.tier_name(), "Free")

    def test_activate_valid_key(self):
        key = "03e11a51-8c63-4826-8b87-998b626285c3"
        res = licensing.activate_license(key)
        self.assertTrue(res["ok"])
        self.assertTrue(licensing.is_pro())
        self.assertEqual(licensing.tier_name(), "Pro")
        self.assertEqual(licensing.license_key(), key)

    def test_activate_invalid_key(self):
        res = licensing.activate_license("not-a-key")
        self.assertFalse(res["ok"])
        self.assertFalse(licensing.is_pro())

    def test_deactivate(self):
        licensing.activate_license("03e11a51-8c63-4826-8b87-998b626285c3")
        self.assertTrue(licensing.is_pro())
        licensing.deactivate_license()
        self.assertFalse(licensing.is_pro())


if __name__ == "__main__":
    unittest.main()
