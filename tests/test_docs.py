from __future__ import annotations

import subprocess
import sys
import unittest

from tests.helpers import CLI, ROOT


class DocumentedCommandTests(unittest.TestCase):
    def test_tc018_public_parsers_match_documented_profiles(self) -> None:
        help_text = subprocess.run(
            [sys.executable, str(ROOT / "install.py"), "--help"],
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        for token in ("codex-project", "claude-code-project", "agent-project", "verify"):
            self.assertIn(token, help_text)
        loop_help = subprocess.run(
            [sys.executable, str(CLI), "--help"], text=True, capture_output=True, check=True
        ).stdout
        for token in ("specify", "approve", "implement-check", "verify", "commit", "promote", "status"):
            self.assertIn(token, loop_help)

    def test_tc019_repository_trust_files_exist(self) -> None:
        for name in ("LICENSE", "SECURITY.md", "CONTRIBUTING.md", ".github/workflows/ci.yml"):
            self.assertTrue((ROOT / name).is_file(), name)
        self.assertIn("Apache License", (ROOT / "LICENSE").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
