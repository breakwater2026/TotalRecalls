"""The licence verification endpoint must not be user-redirectable.

2026-10-18: the shipped binary honoured TR_LICENSE_VERIFY_ENDPOINT
unconditionally, so any user could point it at a local server and unlock Pro.
The gate is now APP_BUILD_TAG containing "demo". These tests pin that down.
"""
from __future__ import annotations

import importlib
import os
import unittest
from unittest import mock

import totalrecalls
import totalrecalls.licensing as licensing

PUBLIC = "https://totalrecalls.app/api/licenses/verify"
LOCAL = "http://127.0.0.1:8788/verify"


class VerifyEndpointTests(unittest.TestCase):
    def _endpoint(self, build_tag: str, env: dict) -> str:
        with mock.patch.object(totalrecalls, "APP_BUILD_TAG", build_tag), \
             mock.patch.dict(os.environ, env, clear=False):
            return importlib.reload(licensing).LICENSE_VERIFY_ENDPOINT
        # note: reload mutates the module in place; caller restores below

    def tearDown(self) -> None:
        os.environ.pop("TR_LICENSE_VERIFY_ENDPOINT", None)
        importlib.reload(licensing)

    def test_defaults_to_public_endpoint(self):
        os.environ.pop("TR_LICENSE_VERIFY_ENDPOINT", None)
        importlib.reload(licensing)
        self.assertEqual(licensing.LICENSE_VERIFY_ENDPOINT, PUBLIC)

    def test_shipping_build_ignores_the_override(self):
        """The bypass: a normal build must NOT honour the variable."""
        with mock.patch.object(totalrecalls, "APP_BUILD_TAG", "v1.0.0"), \
             mock.patch.dict(os.environ, {"TR_LICENSE_VERIFY_ENDPOINT": LOCAL}):
            self.assertEqual(importlib.reload(licensing).LICENSE_VERIFY_ENDPOINT, PUBLIC)

    def test_demo_build_honours_the_override(self):
        with mock.patch.object(totalrecalls, "APP_BUILD_TAG", "v1.0.0-demo"), \
             mock.patch.dict(os.environ, {"TR_LICENSE_VERIFY_ENDPOINT": LOCAL}):
            self.assertEqual(importlib.reload(licensing).LICENSE_VERIFY_ENDPOINT, LOCAL)

    def test_unrelated_tag_does_not_unlock_the_override(self):
        with mock.patch.object(totalrecalls, "APP_BUILD_TAG", "v1.0.0-rc1"), \
             mock.patch.dict(os.environ, {"TR_LICENSE_VERIFY_ENDPOINT": LOCAL}):
            self.assertEqual(importlib.reload(licensing).LICENSE_VERIFY_ENDPOINT, PUBLIC)


if __name__ == "__main__":
    unittest.main()
