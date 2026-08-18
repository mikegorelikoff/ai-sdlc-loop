from __future__ import annotations

import subprocess
import sys
import unittest

from tests.helpers import CLI, ROOT, read_toon


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

    def test_tc020_stage_skills_have_toon_manifests_and_steps(self) -> None:
        for name in (
            "ai-sdlc",
            "ai-sdlc-specify",
            "ai-sdlc-implement",
            "ai-sdlc-verify",
            "ai-sdlc-commit",
            "ai-sdlc-approvals-sandbox",
            "ai-sdlc-branching",
            "ai-sdlc-test-cases",
            "ai-sdlc-qa",
            "ai-sdlc-validation",
            "ai-sdlc-code-review",
            "ai-sdlc-security-testing",
            "ai-sdlc-commit-prep",
            "ai-sdlc-conventional-commit",
        ):
            skill = ROOT / "skills" / name
            self.assertTrue((skill / "SKILL.md").is_file(), name)
            manifest = skill / "steps" / "manifest.toon"
            self.assertTrue(manifest.is_file(), name)
            step_files = list((skill / "steps").glob("*.md"))
            self.assertNotEqual([], step_files, name)
            contract = read_toon(manifest)
            expected_schema = (
                "ai-sdlc-loop-skill-steps/v1"
                if name in {"ai-sdlc", "ai-sdlc-specify", "ai-sdlc-implement", "ai-sdlc-verify", "ai-sdlc-commit"}
                else "ai-sdlc-skill-steps/v2"
            )
            self.assertEqual(expected_schema, contract["schema"])
            self.assertEqual(name, contract["skill"])
            self.assertEqual(len(step_files), len(contract["steps"]))

    def test_tc025_durable_contracts_are_toon_only(self) -> None:
        forbidden = []
        for path in ROOT.rglob("*.py"):
            if ".git" not in path.parts:
                text = path.read_text(encoding="utf-8")
                forbidden_suffix = "." + "json"
                if any(stem + forbidden_suffix in text for stem in ("spec", "state", "evidence", "promoted")):
                    forbidden.append(str(path.relative_to(ROOT)))
        self.assertEqual([], forbidden)

    def test_tc026_delivery_control_scripts_are_loadable(self) -> None:
        scripts = {
            "ai-sdlc-approvals-sandbox": "approval_plan.py",
            "ai-sdlc-branching": "branch_plan.py",
            "ai-sdlc-test-cases": "case_matrix.py",
            "ai-sdlc-qa": "qa_plan.py",
            "ai-sdlc-validation": "validation_plan.py",
            "ai-sdlc-code-review": "review_readiness.py",
            "ai-sdlc-security-testing": "security_review_matrix.py",
            "ai-sdlc-commit-prep": "check_commit_ready.py",
            "ai-sdlc-conventional-commit": "validate_commit_msg.py",
        }
        for skill, script in scripts.items():
            with self.subTest(skill=skill):
                result = subprocess.run(
                    [sys.executable, str(ROOT / "skills" / skill / "scripts" / script), "--help"],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)

    def test_tc026_delivery_control_step_graphs_are_selectable(self) -> None:
        selector = ROOT / "skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py"
        for skill in (
            "ai-sdlc-approvals-sandbox",
            "ai-sdlc-branching",
            "ai-sdlc-test-cases",
            "ai-sdlc-qa",
            "ai-sdlc-validation",
            "ai-sdlc-code-review",
            "ai-sdlc-security-testing",
            "ai-sdlc-commit-prep",
            "ai-sdlc-conventional-commit",
        ):
            with self.subTest(skill=skill):
                result = subprocess.run(
                    [sys.executable, str(selector), "--skill", skill, "--phase", "prepare", "--quick-flow"],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn("schema: ai-sdlc-skill-step-selection/v2", result.stdout)

    def test_tc026_delivery_control_script_contracts_pass(self) -> None:
        contract = ROOT / "skills/ai-sdlc-shared-runtime/scripts/skill_script_contract.py"
        for skill in (
            "ai-sdlc-approvals-sandbox",
            "ai-sdlc-branching",
            "ai-sdlc-test-cases",
            "ai-sdlc-qa",
            "ai-sdlc-validation",
            "ai-sdlc-code-review",
            "ai-sdlc-security-testing",
            "ai-sdlc-commit-prep",
            "ai-sdlc-conventional-commit",
        ):
            with self.subTest(skill=skill):
                result = subprocess.run(
                    [sys.executable, str(contract), str(ROOT / "skills" / skill)],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)

    def test_tc026_validation_plan_omits_absent_sdd_runtime(self) -> None:
        planner = ROOT / "skills/ai-sdlc-validation/scripts/validation_plan.py"
        result = subprocess.run(
            [sys.executable, str(planner), "--full-flow", "specs/123-example/tasks.md"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertNotIn("ai-sdlc-sdd", result.stdout)


if __name__ == "__main__":
    unittest.main()
