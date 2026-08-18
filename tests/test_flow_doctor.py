from __future__ import annotations

import subprocess
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import ROOT, read_toon

FLOW = ROOT / "skills/ai-sdlc-loop-flow/scripts/flow.py"
DOCTOR = ROOT / "skills/ai-sdlc-loop-doctor/scripts/doctor.py"


def read_toon_text(text: str) -> dict[str, object]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "value.toon"
        path.write_text(text, encoding="utf-8")
        return read_toon(path)


class FlowTests(unittest.TestCase):
    def test_tc032_explore_is_deterministic_and_apply_revalidates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            command = [
                sys.executable, str(FLOW), "explore", "--root", str(root),
                "--feature", "parser-fix", "--intent", "fix the parser",
                "--full-flow", "--format", "toon",
            ]
            first = subprocess.run(command, text=True, capture_output=True, check=True)
            second = subprocess.run(command, text=True, capture_output=True, check=True)
            self.assertEqual(first.stdout, second.stdout)
            card = root / "card.toon"
            card.write_text(first.stdout, encoding="utf-8")
            value = read_toon(card)
            self.assertEqual("ai-sdlc-loop-flow/v1", value["schema"])
            self.assertEqual("ai-sdlc-loop-specify", value["owning_skill"])
            applied = subprocess.run(
                [sys.executable, str(FLOW), "apply", "--root", str(root), "--card", str(card), "--execute", "--approve"],
                text=True, capture_output=True, check=True,
            )
            result = read_toon_text(applied.stdout)
            self.assertEqual("selected", result["status"])
            self.assertFalse(result["owner_action_executed"])

    def test_tc033_apply_rejects_route_drift_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            explored = subprocess.run(
                [sys.executable, str(FLOW), "explore", "--root", str(root), "--feature", "docs", "--intent", "review the diff"],
                text=True, capture_output=True, check=True,
            )
            card = root / "card.toon"
            card.write_text(explored.stdout.replace("review the diff", "commit the diff"), encoding="utf-8")
            denied = subprocess.run(
                [sys.executable, str(FLOW), "apply", "--root", str(root), "--card", str(card), "--execute", "--approve"],
                text=True, capture_output=True,
            )
            self.assertNotEqual(0, denied.returncode)
            self.assertFalse((root / ".ai-sdlc-loop").exists())

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            outside = Path(tmp) / "outside"
            root.mkdir()
            outside.mkdir()
            state_root = root / ".ai-sdlc-loop"
            state_root.mkdir()
            try:
                (state_root / "docs").symlink_to(outside, target_is_directory=True)
            except (OSError, NotImplementedError):
                return
            denied = subprocess.run(
                [sys.executable, str(FLOW), "explore", "--root", str(root), "--feature", "docs", "--intent", "fix docs"],
                text=True, capture_output=True,
            )
            self.assertNotEqual(0, denied.returncode)
            self.assertIn("symlink", denied.stderr)


class DoctorTests(unittest.TestCase):
    def test_tc034_installed_package_is_healthy_and_plan_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [sys.executable, str(ROOT / "install.py"), "codex-project", "--project-root", tmp],
                text=True, capture_output=True, check=True,
            )
            checked = subprocess.run(
                [sys.executable, str(DOCTOR), "check", "--project-root", tmp, "--profile", "codex-project"],
                text=True, capture_output=True, check=True,
            )
            report = read_toon_text(checked.stdout)
            self.assertEqual("healthy", report["status"])
            planned = subprocess.run(
                [sys.executable, str(DOCTOR), "upgrade-plan", "--project-root", tmp, "--profile", "codex-project", "--package-root", str(ROOT)],
                text=True, capture_output=True, check=True,
            )
            plan = read_toon_text(planned.stdout)
            self.assertFalse(plan["apply_authorized"])
            self.assertTrue(all(item["action"] == "unchanged" for item in plan["changes"]))

    def test_tc035_doctor_reports_drift_without_repair(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [sys.executable, str(ROOT / "install.py"), "codex-project", "--project-root", tmp],
                text=True, capture_output=True, check=True,
            )
            target = Path(tmp) / ".agents/skills/ai-sdlc-loop-flow/SKILL.md"
            target.write_text("local edit\n", encoding="utf-8")
            checked = subprocess.run(
                [sys.executable, str(DOCTOR), "check", "--project-root", tmp, "--profile", "codex-project"],
                text=True, capture_output=True,
            )
            self.assertEqual(2, checked.returncode)
            self.assertEqual("local edit\n", target.read_text(encoding="utf-8"))

        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [sys.executable, str(ROOT / "install.py"), "codex-project", "--project-root", tmp],
                text=True, capture_output=True, check=True,
            )
            skill = Path(tmp) / ".agents/skills/ai-sdlc-loop-flow"
            outside = Path(tmp) / "outside-skill"
            outside.mkdir()
            (outside / "SKILL.md").write_text("outside\n", encoding="utf-8")
            shutil.rmtree(skill)
            try:
                skill.symlink_to(outside, target_is_directory=True)
            except (OSError, NotImplementedError):
                return
            checked = subprocess.run(
                [sys.executable, str(DOCTOR), "check", "--project-root", tmp, "--profile", "codex-project"],
                text=True, capture_output=True,
            )
            self.assertEqual(2, checked.returncode)
            self.assertIn("ai-sdlc-loop-flow:symlink", checked.stdout)


if __name__ == "__main__":
    unittest.main()
