"""Windows launcher policy and payload packaging without a Windows host."""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.helpers import ROOT
sys.path.insert(0, str(ROOT))


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


launcher = load("windows_launcher", "packaging/windows/launcher.py")
builder = load("windows_builder", "packaging/windows/build.py")


class WindowsInstallerTests(unittest.TestCase):
    def test_payload_is_complete_and_excludes_development_files(self):
        with tempfile.TemporaryDirectory() as folder:
            payload = Path(folder) / "payload"
            builder.stage(payload)
            self.assertEqual(sorted(p.name for p in (payload / "skills").iterdir()), sorted(builder.install.SKILLS))
            self.assertTrue((payload / "install.py").is_file())
            self.assertTrue((payload / "LICENSE").is_file())
            self.assertFalse(list(payload.rglob("__pycache__")))
            self.assertFalse(list(payload.rglob("tests")))

    def test_gui_entry_installs_and_verifies_using_existing_contract(self):
        with patch.object(launcher.install, "install") as install, patch.object(launcher.install, "verify") as verify:
            launcher.install_project("project path", "claude-code-project")
            install.assert_called_once()
            verify.assert_called_once_with(install.call_args.args[0])
            self.assertEqual(install.call_args.args[0].project_root, "project path")

    def test_failure_does_not_claim_verification(self):
        with patch.object(launcher.install, "install", side_effect=launcher.install.InstallError("occupied")), patch.object(launcher.install, "verify") as verify:
            with self.assertRaises(launcher.install.InstallError):
                launcher.install_project("project", "codex-project")
            verify.assert_not_called()

    def test_cli_is_forwarded_and_no_args_open_gui(self):
        with patch.object(sys, "argv", ["setup.exe", "verify", "codex-project"]), patch.object(launcher.install, "main", return_value=2) as cli:
            self.assertEqual(launcher.main(), 2)
            cli.assert_called_once()
        with patch.object(sys, "argv", ["setup.exe"]), patch.object(launcher, "gui", return_value=0) as gui:
            self.assertEqual(launcher.main(), 0)
            gui.assert_called_once()

    def test_bundle_version_is_consistent(self):
        self.assertEqual(launcher.VERSION, builder.VERSION)
        self.assertIn(launcher.VERSION, builder.NAME)


if __name__ == "__main__":
    unittest.main()
