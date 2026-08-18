from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.helpers import git, init_repo, read_toon, run_cli


class WorkflowTests(unittest.TestCase):
    def test_tc004_tc005_specify_is_deterministic_and_sensitive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            run_cli(repo, "specify", "--feature", "demo", "--request", "  Add   greeting ", "--allow", "app.txt")
            spec_path = repo / ".ai-sdlc-loop/demo/spec.toon"
            first = read_toon(spec_path)["fingerprint"]
            run_cli(repo, "specify", "--feature", "demo", "--request", "Add greeting", "--allow", "app.txt")
            self.assertEqual(first, read_toon(spec_path)["fingerprint"])
            run_cli(repo, "specify", "--feature", "demo", "--request", "Add farewell", "--allow", "app.txt")
            self.assertNotEqual(first, read_toon(spec_path)["fingerprint"])

    def test_tc005_dot_prefixed_allowed_path_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            (repo / ".github").mkdir()
            run_cli(repo, "specify", "--feature", "demo", "--request", "Add workflow", "--allow", ".github/workflows")
            self.assertEqual(
                [".github/workflows"],
                read_toon(repo / ".ai-sdlc-loop/demo/spec.toon")["allowed_paths"],
            )

    def test_tc006_tc007_implement_approval_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            run_cli(repo, "specify", "--feature", "demo", "--request", "Change app", "--allow", "app.txt")
            before = git(repo, "status", "--porcelain")
            denied = run_cli(repo, "implement-check", "--feature", "demo", ok=False)
            self.assertNotEqual(0, denied.returncode)
            self.assertEqual(before, git(repo, "status", "--porcelain"))
            fp = read_toon(repo / ".ai-sdlc-loop/demo/spec.toon")["fingerprint"]
            run_cli(repo, "approve", "--feature", "demo", "--action", "implement", "--decision", "approve", "--fingerprint", fp, "--reviewer", "human")
            run_cli(repo, "implement-check", "--feature", "demo")

    def test_tc010_tc014_verify_and_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            run_cli(repo, "specify", "--feature", "demo", "--request", "Change app", "--allow", "app.txt")
            spec_fp = read_toon(repo / ".ai-sdlc-loop/demo/spec.toon")["fingerprint"]
            run_cli(repo, "approve", "--feature", "demo", "--action", "implement", "--decision", "approve", "--fingerprint", spec_fp, "--reviewer", "human")
            (repo / "app.txt").write_text("after\n", encoding="utf-8")
            run_cli(repo, "verify", "--feature", "demo", "--command", f"{__import__('sys').executable} -c pass")
            verified = read_toon(repo / ".ai-sdlc-loop/demo/evidence.toon")["verified_fingerprint"]
            run_cli(repo, "approve", "--feature", "demo", "--action", "commit", "--decision", "approve", "--fingerprint", verified, "--reviewer", "human")
            old_head = git(repo, "rev-parse", "HEAD")
            run_cli(repo, "commit", "--feature", "demo", "--message", "feat: update app")
            self.assertNotEqual(old_head, git(repo, "rev-parse", "HEAD"))
            self.assertIn("AI-SDLC-Loop-Feature: demo", git(repo, "show", "-s", "--format=%B"))

    def test_tc011_failed_command_blocks_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            run_cli(repo, "specify", "--feature", "demo", "--request", "Change app", "--allow", "app.txt")
            fp = read_toon(repo / ".ai-sdlc-loop/demo/spec.toon")["fingerprint"]
            run_cli(repo, "approve", "--feature", "demo", "--action", "implement", "--decision", "approve", "--fingerprint", fp, "--reviewer", "human")
            (repo / "app.txt").write_text("after\n", encoding="utf-8")
            result = run_cli(repo, "verify", "--feature", "demo", "--command", f"{__import__('sys').executable} -c 'raise SystemExit(3)'", ok=False)
            self.assertNotEqual(0, result.returncode)
            self.assertFalse(read_toon(repo / ".ai-sdlc-loop/demo/evidence.toon")["ready"])


if __name__ == "__main__":
    unittest.main()
