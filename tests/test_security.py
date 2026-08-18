from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.helpers import git, init_repo, read_toon, run_cli


class SecurityTests(unittest.TestCase):
    def test_tc009_path_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            result = run_cli(repo, "specify", "--feature", "demo", "--request", "escape", "--allow", "../outside", ok=False)
            self.assertNotEqual(0, result.returncode)
            self.assertFalse((repo / ".ai-sdlc-loop/demo").exists())

    def test_tc009_state_symlink_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            outside = Path(tmp) / "outside"
            outside.mkdir()
            try:
                (repo / ".ai-sdlc-loop").symlink_to(outside, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("directory symlinks are unavailable")
            result = run_cli(repo, "specify", "--feature", "demo", "--request", "escape", "--allow", "app.txt", ok=False)
            self.assertNotEqual(0, result.returncode)
            self.assertEqual([], list(outside.iterdir()))

    def test_tc012_evidence_redacts_secrets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            run_cli(repo, "specify", "--feature", "demo", "--request", "Change app", "--allow", "app.txt")
            fp = read_toon(repo / ".ai-sdlc-loop/demo/spec.toon")["fingerprint"]
            run_cli(repo, "approve", "--feature", "demo", "--action", "implement", "--decision", "approve", "--fingerprint", fp, "--reviewer", "human")
            (repo / "app.txt").write_text("after\n", encoding="utf-8")
            run_cli(repo, "verify", "--feature", "demo", "--command", f"{__import__('sys').executable} -c 'print(\"TOKEN=synthetic-secret\")'")
            raw = (repo / ".ai-sdlc-loop/demo/evidence.toon").read_text(encoding="utf-8")
            self.assertNotIn("synthetic-secret", raw)
            self.assertIn("[REDACTED]", raw)

    def test_tc013_commit_denial_preserves_head_and_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            run_cli(repo, "specify", "--feature", "demo", "--request", "Change app", "--allow", "app.txt")
            fp = read_toon(repo / ".ai-sdlc-loop/demo/spec.toon")["fingerprint"]
            run_cli(repo, "approve", "--feature", "demo", "--action", "implement", "--decision", "approve", "--fingerprint", fp, "--reviewer", "human")
            (repo / "app.txt").write_text("after\n", encoding="utf-8")
            run_cli(repo, "verify", "--feature", "demo", "--command", f"{__import__('sys').executable} -c pass")
            head = git(repo, "rev-parse", "HEAD")
            index = git(repo, "write-tree")
            result = run_cli(repo, "commit", "--feature", "demo", "--message", "feat: denied", ok=False)
            self.assertNotEqual(0, result.returncode)
            self.assertEqual(head, git(repo, "rev-parse", "HEAD"))
            self.assertEqual(index, git(repo, "write-tree"))

    def test_tc015_commit_approval_is_invalid_after_change_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            run_cli(repo, "specify", "--feature", "demo", "--request", "Change app", "--allow", "app.txt")
            fp = read_toon(repo / ".ai-sdlc-loop/demo/spec.toon")["fingerprint"]
            run_cli(repo, "approve", "--feature", "demo", "--action", "implement", "--decision", "approve", "--fingerprint", fp, "--reviewer", "human")
            (repo / "app.txt").write_text("verified\n", encoding="utf-8")
            run_cli(repo, "verify", "--feature", "demo", "--command", f"{__import__('sys').executable} -c pass")
            verified = read_toon(repo / ".ai-sdlc-loop/demo/evidence.toon")["verified_fingerprint"]
            run_cli(repo, "approve", "--feature", "demo", "--action", "commit", "--decision", "approve", "--fingerprint", verified, "--reviewer", "human")
            (repo / "app.txt").write_text("drifted\n", encoding="utf-8")
            head = git(repo, "rev-parse", "HEAD")
            result = run_cli(repo, "commit", "--feature", "demo", "--message", "feat: stale", ok=False)
            self.assertNotEqual(0, result.returncode)
            self.assertEqual(head, git(repo, "rev-parse", "HEAD"))


if __name__ == "__main__":
    unittest.main()
