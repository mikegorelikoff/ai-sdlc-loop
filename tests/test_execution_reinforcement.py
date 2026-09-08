"""Integration regressions for current evidence at lifecycle boundaries."""

import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import create_quality_gate, init_repo, read_toon, run_cli, ROOT

sys.path.insert(0, str(ROOT / "skills/ai-sdlc-loop-shared-runtime/scripts"))
from toon import encode_toon


class VerificationBoundaryTests(unittest.TestCase):
    def prepare(self, root):
        repo = init_repo(root / "repo")
        run_cli(repo, "specify", "--feature", "demo", "--request", "Change app", "--allow", "app.txt")
        spec = read_toon(repo / ".ai-sdlc-loop/demo/spec.toon")
        run_cli(repo, "approve", "--feature", "demo", "--action", "implement",
                "--decision", "approve", "--fingerprint", spec["fingerprint"], "--reviewer", "human")
        (repo / "app.txt").write_text("after\n")
        create_quality_gate(repo)
        return repo

    def test_passing_command_that_changes_source_cannot_report_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.prepare(Path(directory))
            result = run_cli(repo, "verify", "--feature", "demo", "--command",
                             f'{sys.executable} -c "from pathlib import Path; Path(\'app.txt\').write_text(\'drift\')"', ok=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(read_toon(repo / ".ai-sdlc-loop/demo/evidence.toon")["ready"])

    def test_commit_approval_rejects_tampered_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.prepare(Path(directory))
            run_cli(repo, "verify", "--feature", "demo", "--command", f"{sys.executable} -c pass")
            path = repo / ".ai-sdlc-loop/demo/evidence.toon"
            evidence = read_toon(path)
            evidence["commands"][0]["exit_code"] = 9
            path.write_text(encode_toon(evidence))
            result = run_cli(repo, "approve", "--feature", "demo", "--action", "commit",
                             "--decision", "approve", "--fingerprint", evidence["verified_fingerprint"],
                             "--reviewer", "human", ok=False)
            self.assertNotEqual(result.returncode, 0)

    def test_commit_approval_rejects_drift_after_verification(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.prepare(Path(directory))
            run_cli(repo, "verify", "--feature", "demo", "--command", f"{sys.executable} -c pass")
            evidence = read_toon(repo / ".ai-sdlc-loop/demo/evidence.toon")
            (repo / "app.txt").write_text("later change\n")
            result = run_cli(repo, "approve", "--feature", "demo", "--action", "commit",
                             "--decision", "approve", "--fingerprint", evidence["verified_fingerprint"],
                             "--reviewer", "human", ok=False)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
