import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from totalrecalls.core import platform
from totalrecalls.core import secure_storage


class PlatformPathTests(unittest.TestCase):
    def test_windows_path_keeps_existing_location(self):
        env = {"APPDATA": r"C:\Users\me\AppData\Roaming"}
        self.assertEqual(
            platform.app_state_dir(platform_name="nt", environ=env),
            r"C:\Users\me\AppData\Roaming\PerplexityExporter",
        )

    def test_xdg_state_path_is_used_on_linux(self):
        env = {"XDG_STATE_HOME": "/home/me/.state"}
        self.assertEqual(
            platform.app_state_dir(platform_name="posix", environ=env, home="/home/me"),
            os.path.join("/home/me/.state", "TotalRecalls"),
        )

    def test_macos_uses_application_support(self):
        with patch("totalrecalls.core.platform.sys.platform", "darwin"):
            self.assertEqual(
                platform.app_state_dir(environ={}, home="/Users/me"),
                os.path.join("/Users/me", "Library", "Application Support", "TotalRecalls"),
            )

    def test_override_is_expanded_and_preferred(self):
        env = {platform.APP_STATE_DIR_ENV: "~/portable-state"}
        expected = os.path.abspath(os.path.expanduser("~/portable-state"))
        self.assertEqual(platform.app_state_dir(environ=env), expected)


class PlatformCommandTests(unittest.TestCase):
    def test_folder_commands_are_argument_lists(self):
        self.assertEqual(
            platform.folder_open_command(r"C:\My Chats", platform_name="nt"),
            ["explorer.exe", r"C:\My Chats"],
        )
        self.assertEqual(
            platform.folder_open_command("/home/me/My Chats", platform_name="posix"),
            ["xdg-open", "/home/me/My Chats"],
        )
        self.assertEqual(
            platform.folder_open_command("/Users/me/My Chats", platform_name="darwin"),
            ["open", "/Users/me/My Chats"],
        )

    def test_process_commands_preserve_windows_taskkill_shape(self):
        self.assertEqual(
            platform.process_list_command("TotalRecalls.exe", platform_name="nt"),
            ["tasklist", "/FI", "IMAGENAME eq TotalRecalls.exe", "/FO", "CSV", "/NH"],
        )
        self.assertEqual(
            platform.process_terminate_command(42, force=True, platform_name="nt"),
            ["taskkill", "/PID", "42", "/F"],
        )
        self.assertEqual(
            platform.process_terminate_command(42, force=False, platform_name="posix"),
            ["kill", "-TERM", "42"],
        )

    def test_process_id_parser_handles_windows_csv_and_posix_lines(self):
        windows = '"TotalRecalls.exe","1234","Console","1","12,345 K"\n'
        self.assertEqual(platform.parse_process_ids(windows, platform_name="nt"), [1234])
        self.assertEqual(platform.parse_process_ids("123\n456\n", platform_name="posix"), [123, 456])

    def test_open_folder_rejects_missing_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("totalrecalls.core.platform.subprocess.Popen") as popen:
                platform.open_folder(directory, platform_name="posix")
                popen.assert_called_once()
            with self.assertRaises(NotADirectoryError):
                platform.open_folder(Path(directory) / "missing", platform_name="posix")


class SecureStorageFallbackTests(unittest.TestCase):
    def test_windows_dpapi_failure_uses_private_envelope(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            with patch.object(secure_storage.os, "name", "nt"), patch.object(
                secure_storage, "_dpapi_transform", side_effect=secure_storage.SecureStorageError("unavailable")
            ):
                secure_storage.save_json(path, {"token": "secret"})
                self.assertEqual(secure_storage.load_json(path), {"token": "secret"})
            envelope = path.read_text(encoding="utf-8")
            self.assertIn('"protection":"private-file"', envelope)


if __name__ == "__main__":
    unittest.main()
