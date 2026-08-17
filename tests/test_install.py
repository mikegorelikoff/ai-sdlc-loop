from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import ROOT


class InstallProfileTests(unittest.TestCase):
    def test_tc001_all_profiles_install_exactly_one_skill(self) -> None:
        profiles = {
            "codex-project": Path(".agents/skills"),
            "claude-code-project": Path(".claude/skills"),
            "agent-project": Path(".agent/skills"),
        }
        for profile, target in profiles.items():
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as tmp:
                args = [sys.executable, str(ROOT / "install.py"), profile, "--project-root", tmp]
                if profile == "agent-project":
                    args += ["--skills-root", str(target)]
                subprocess.run(args, check=True, text=True, capture_output=True)
                installed = Path(tmp) / target
                self.assertEqual(["ai-sdlc"], sorted(p.name for p in installed.iterdir()))
                subprocess.run(
                    [sys.executable, str(ROOT / "install.py"), "verify", profile, "--project-root", tmp]
                    + (["--skills-root", str(target)] if profile == "agent-project" else []),
                    check=True,
                    text=True,
                    capture_output=True,
                )
                subprocess.run(
                    [sys.executable, str(Path(tmp) / ".ai-sdlc-loop/install/install.py"), "verify", profile, "--project-root", tmp]
                    + (["--skills-root", str(target)] if profile == "agent-project" else []),
                    check=True,
                    text=True,
                    capture_output=True,
                )

    def test_tc001_existing_unrelated_skill_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unrelated = Path(tmp) / ".agents/skills/existing"
            unrelated.mkdir(parents=True)
            (unrelated / "SKILL.md").write_text("existing\n", encoding="utf-8")
            subprocess.run(
                [sys.executable, str(ROOT / "install.py"), "codex-project", "--project-root", tmp],
                check=True,
                text=True,
                capture_output=True,
            )
            self.assertEqual("existing\n", (unrelated / "SKILL.md").read_text(encoding="utf-8"))
            self.assertTrue((Path(tmp) / ".agents/skills/ai-sdlc/SKILL.md").is_file())

    def test_tc002_unsafe_custom_root_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(ROOT / "install.py"), "agent-project", "--project-root", tmp, "--skills-root", "../escape"],
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertFalse((Path(tmp).parent / "escape" / "ai-sdlc").exists())
            for protected in (".git/skills", ".ai-sdlc-loop/skills"):
                result = subprocess.run(
                    [sys.executable, str(ROOT / "install.py"), "agent-project", "--project-root", tmp, "--skills-root", protected],
                    text=True,
                    capture_output=True,
                )
                self.assertNotEqual(0, result.returncode)

    def test_tc002_install_state_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            project.mkdir()
            outside = Path(tmp) / "outside"
            outside.mkdir()
            try:
                (project / ".ai-sdlc-loop").symlink_to(outside, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("directory symlinks are unavailable")
            result = subprocess.run(
                [sys.executable, str(ROOT / "install.py"), "codex-project", "--project-root", project],
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertEqual([], list(outside.iterdir()))

    def test_tc003_drift_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            args = [sys.executable, str(ROOT / "install.py"), "codex-project", "--project-root", tmp]
            subprocess.run(args, check=True, text=True, capture_output=True)
            skill = Path(tmp) / ".agents/skills/ai-sdlc/SKILL.md"
            skill.write_text("local edit\n", encoding="utf-8")
            result = subprocess.run(args, text=True, capture_output=True)
            self.assertNotEqual(0, result.returncode)
            self.assertEqual("local edit\n", skill.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
