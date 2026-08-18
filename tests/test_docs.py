from __future__ import annotations

import os
import re
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
            "ai-sdlc-loop-orchestrate",
            "ai-sdlc-loop-specify",
            "ai-sdlc-loop-implement",
            "ai-sdlc-loop-verify",
            "ai-sdlc-loop-commit",
            "ai-sdlc-loop-approvals-sandbox",
            "ai-sdlc-loop-branching",
            "ai-sdlc-loop-test-cases",
            "ai-sdlc-loop-qa",
            "ai-sdlc-loop-requirements-review",
            "ai-sdlc-loop-release-readiness",
            "ai-sdlc-loop-validation",
            "ai-sdlc-loop-code-review",
            "ai-sdlc-loop-security-testing",
            "ai-sdlc-loop-commit-prep",
            "ai-sdlc-loop-conventional-commit",
            "ai-sdlc-loop-flow",
            "ai-sdlc-loop-doctor",
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
                if name in {"ai-sdlc-loop-orchestrate", "ai-sdlc-loop-specify", "ai-sdlc-loop-implement", "ai-sdlc-loop-verify", "ai-sdlc-loop-commit"}
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
            "ai-sdlc-loop-approvals-sandbox": "approval_plan.py",
            "ai-sdlc-loop-branching": "branch_plan.py",
            "ai-sdlc-loop-test-cases": "case_matrix.py",
            "ai-sdlc-loop-qa": "qa_plan.py",
            "ai-sdlc-loop-requirements-review": "requirements_review.py",
            "ai-sdlc-loop-release-readiness": "release_readiness.py",
            "ai-sdlc-loop-validation": "validation_plan.py",
            "ai-sdlc-loop-code-review": "review_readiness.py",
            "ai-sdlc-loop-security-testing": "security_review_matrix.py",
            "ai-sdlc-loop-commit-prep": "check_commit_ready.py",
            "ai-sdlc-loop-conventional-commit": "validate_commit_msg.py",
            "ai-sdlc-loop-flow": "flow.py",
            "ai-sdlc-loop-doctor": "doctor.py",
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
        selector = ROOT / "skills/ai-sdlc-loop-shared-runtime/scripts/ai_sdlc_steps.py"
        for skill in (
            "ai-sdlc-loop-approvals-sandbox",
            "ai-sdlc-loop-branching",
            "ai-sdlc-loop-test-cases",
            "ai-sdlc-loop-qa",
            "ai-sdlc-loop-requirements-review",
            "ai-sdlc-loop-release-readiness",
            "ai-sdlc-loop-validation",
            "ai-sdlc-loop-code-review",
            "ai-sdlc-loop-security-testing",
            "ai-sdlc-loop-commit-prep",
            "ai-sdlc-loop-conventional-commit",
            "ai-sdlc-loop-flow",
            "ai-sdlc-loop-doctor",
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
        contract = ROOT / "skills/ai-sdlc-loop-shared-runtime/scripts/skill_script_contract.py"
        for skill in (
            "ai-sdlc-loop-approvals-sandbox",
            "ai-sdlc-loop-branching",
            "ai-sdlc-loop-test-cases",
            "ai-sdlc-loop-qa",
            "ai-sdlc-loop-requirements-review",
            "ai-sdlc-loop-release-readiness",
            "ai-sdlc-loop-validation",
            "ai-sdlc-loop-code-review",
            "ai-sdlc-loop-security-testing",
            "ai-sdlc-loop-commit-prep",
            "ai-sdlc-loop-conventional-commit",
            "ai-sdlc-loop-flow",
            "ai-sdlc-loop-doctor",
        ):
            with self.subTest(skill=skill):
                result = subprocess.run(
                    [sys.executable, str(contract), str(ROOT / "skills" / skill)],
                    cwd=ROOT,
                    env={**os.environ, "PYTHONIOENCODING": "cp1252"},
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)

    def test_tc026_validation_plan_omits_absent_sdd_runtime(self) -> None:
        planner = ROOT / "skills/ai-sdlc-loop-validation/scripts/validation_plan.py"
        result = subprocess.run(
            [sys.executable, str(planner), "--full-flow", "specs/123-example/tasks.md"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertNotIn("ai-sdlc-sdd", result.stdout)

    def test_tc030_all_distributed_skills_use_loop_namespace(self) -> None:
        skills = sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir())
        self.assertEqual(19, len(skills))
        for skill in skills:
            with self.subTest(skill=skill.name):
                self.assertRegex(skill.name, r"^ai-sdlc-loop-[a-z0-9]+(?:-[a-z0-9]+)*$")
                frontmatter = (skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(f"name: {skill.name}\n", frontmatter)
                manifest = read_toon(skill / "steps" / "manifest.toon")
                self.assertEqual(skill.name, manifest["skill"])

        superseded = (
            "ai-sdlc-approvals-sandbox",
            "ai-sdlc-branching",
            "ai-sdlc-code-review",
            "ai-sdlc-commit-prep",
            "ai-sdlc-commit",
            "ai-sdlc-conventional-commit",
            "ai-sdlc-implement",
            "ai-sdlc-qa",
            "ai-sdlc-release-readiness",
            "ai-sdlc-requirements-review",
            "ai-sdlc-security-testing",
            "ai-sdlc-shared-runtime",
            "ai-sdlc-specify",
            "ai-sdlc-test-cases",
            "ai-sdlc-validation",
            "ai-sdlc-verify",
        )
        targets = [ROOT / "README.md", ROOT / "install.py"]
        text_suffixes = {".md", ".py", ".toon", ".txt", ".yaml", ".yml"}
        targets.extend(
            path
            for skill in skills
            for path in skill.rglob("*")
            if path.is_file() and path.suffix in text_suffixes
        )
        for path in targets:
            text = path.read_text(encoding="utf-8")
            for old_name in superseded:
                with self.subTest(path=path.relative_to(ROOT), old_name=old_name):
                    pattern = rf"(?<![a-z0-9-]){re.escape(old_name)}(?!-[a-z0-9])"
                    self.assertIsNone(re.search(pattern, text))

    def test_tc031_mkdocs_surface_matches_source_contracts(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        expected_nav = ("Home:", "Start here:", "How it works:", "Guides:", "Reference:", "Project:")
        positions = [config.index(item) for item in expected_nav]
        self.assertEqual(sorted(positions), positions)

        for relative in (
            "docs/index.md",
            "docs/start-here.md",
            "docs/how-it-works.md",
            "docs/guides/index.md",
            "docs/reference/index.md",
            "docs/project/index.md",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

        reference = (ROOT / "docs/reference/index.md").read_text(encoding="utf-8")
        skill_names = sorted(path.name for path in (ROOT / "skills").iterdir() if path.is_dir())
        self.assertEqual(19, len(skill_names))
        for name in skill_names:
            self.assertIn(f"`{name}`", reference)

        install_command = (
            "curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/"
            "ai-sdlc-loop/v0.2.0/install.sh | sh -s -- codex-project"
        )
        for relative in ("README.md", "docs/index.md", "docs/start-here.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertEqual(1, text.count(install_command), relative)
        self.assertIn('ref="${AI_SDLC_LOOP_REF:-v0.2.0}"', (ROOT / "install.sh").read_text(encoding="utf-8"))

    def test_tc036_generated_catalog_and_source_docs_are_current(self) -> None:
        for script, arguments in (
            ("build_catalog.py", ["--check"]),
            ("validate_docs.py", []),
        ):
            with self.subTest(script=script):
                result = subprocess.run(
                    [sys.executable, str(ROOT / "docs/scripts" / script), *arguments],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
