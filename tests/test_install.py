from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import ROOT

LOOP_SKILLS = [
    "ai-sdlc-loop-approvals-sandbox",
    "ai-sdlc-loop-branching",
    "ai-sdlc-loop-code-review",
    "ai-sdlc-loop-commit",
    "ai-sdlc-loop-commit-prep",
    "ai-sdlc-loop-conventional-commit",
    "ai-sdlc-loop-doctor",
    "ai-sdlc-loop-flow",
    "ai-sdlc-loop-implement",
    "ai-sdlc-loop-orchestrate",
    "ai-sdlc-loop-qa",
    "ai-sdlc-loop-release-readiness",
    "ai-sdlc-loop-requirements-review",
    "ai-sdlc-loop-security-testing",
    "ai-sdlc-loop-shared-runtime",
    "ai-sdlc-loop-specify",
    "ai-sdlc-loop-test-cases",
    "ai-sdlc-loop-validation",
    "ai-sdlc-loop-verify",
]


class InstallProfileTests(unittest.TestCase):
    def test_tc001_all_profiles_install_exact_loop_skill_set(self) -> None:
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
                self.assertEqual(LOOP_SKILLS, sorted(p.name for p in installed.iterdir()))
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
                self.assertTrue((Path(tmp) / f".ai-sdlc-loop/install/{profile}.toon").is_file())
                self.assertEqual([], list((Path(tmp) / ".ai-sdlc-loop/install").glob("*." + "json")))
                selector = installed / "ai-sdlc-loop-shared-runtime/scripts/ai_sdlc_steps.py"
                selected = subprocess.run(
                    [sys.executable, str(selector), "--skill", "ai-sdlc-loop-validation", "--phase", "prepare", "--quick-flow"],
                    cwd=tmp,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, selected.returncode, selected.stderr)
                self.assertIn("schema: ai-sdlc-skill-step-selection/v2", selected.stdout)

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
            self.assertTrue((Path(tmp) / ".agents/skills/ai-sdlc-loop-orchestrate/SKILL.md").is_file())
            self.assertEqual(LOOP_SKILLS + ["existing"], sorted(p.name for p in unrelated.parent.iterdir()))

    def test_tc002_unsafe_custom_root_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(ROOT / "install.py"), "agent-project", "--project-root", tmp, "--skills-root", "../escape"],
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertFalse((Path(tmp).parent / "escape" / "ai-sdlc-loop-orchestrate").exists())
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
            skill = Path(tmp) / ".agents/skills/ai-sdlc-loop-orchestrate/SKILL.md"
            skill.write_text("local edit\n", encoding="utf-8")
            result = subprocess.run(args, text=True, capture_output=True)
            self.assertNotEqual(0, result.returncode)
            self.assertEqual("local edit\n", skill.read_text(encoding="utf-8"))

    def test_tc003_linked_skill_content_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            args = [sys.executable, str(ROOT / "install.py"), "codex-project", "--project-root", tmp]
            subprocess.run(args, check=True, text=True, capture_output=True)
            skill = Path(tmp) / ".agents/skills/ai-sdlc-loop-orchestrate"
            outside = Path(tmp) / "outside.txt"
            outside.write_text("outside\n", encoding="utf-8")
            link = skill / "linked.txt"
            try:
                link.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("file symlinks are unavailable")
            result = subprocess.run(args, text=True, capture_output=True)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("symlink", result.stderr)


if __name__ == "__main__":
    unittest.main()
