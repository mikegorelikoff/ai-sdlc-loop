"""Adaptive Loop CLI preserves the authoritative quality and approval gates."""
import sys
import tempfile
import unittest
from pathlib import Path
from tests.helpers import create_quality_gate, init_repo, read_toon, run_cli

class AdaptiveLoopTests(unittest.TestCase):
    def prepare(self, root, full=False):
        repo = init_repo(root / "repo")
        args = ["specify", "--feature", "demo", "--request", "fix tiny bug", "--allow", "app.txt",
                "--signal", "familiar=true", "--signal", "covered=true", "--signal", "confident=true"]
        if full: args.append("--full-flow")
        run_cli(repo, *args)
        spec = read_toon(repo / ".ai-sdlc-loop/demo/spec.toon")
        run_cli(repo, "approve", "--feature", "demo", "--action", "implement", "--decision", "approve", "--fingerprint", spec["fingerprint"], "--reviewer", "authorized fixture")
        (repo / "app.txt").write_text("after\n")
        return repo

    def task(self, repo):
        return read_toon(repo / ".ai-sdlc-loop/demo/state.toon")["execution"]

    def test_fast_next_then_quality_verify_done(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.prepare(Path(tmp))
            self.assertEqual(self.task(repo)["decision"]["mode"], "FAST")
            self.assertIn("implement", run_cli(repo, "next", "--feature", "demo").stdout)
            run_cli(repo, "adapt", "--feature", "demo", "--complete-stage", "implement", "--evidence", "app.txt")
            self.assertIn("quality-gate", run_cli(repo, "next", "--feature", "demo").stdout)
            create_quality_gate(repo)
            command = f"{sys.executable} -c pass"
            run_cli(repo, "verify", "--feature", "demo", "--command", command)
            self.assertIn("next_stage: done", run_cli(repo, "next", "--feature", "demo").stdout)
            evidence = (repo / ".ai-sdlc-loop/demo/evidence.toon").read_bytes()
            run_cli(repo, "verify", "--feature", "demo", "--command", command)
            self.assertEqual((repo / ".ai-sdlc-loop/demo/evidence.toon").read_bytes(), evidence)
            self.assertEqual(self.task(repo)["metrics"]["verification_iterations"], 1)
            self.assertIsNone(self.task(repo)["metrics"]["model_calls"])

    def test_escalate_with_context_and_plan_without_reset(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.prepare(Path(tmp))
            original = self.task(repo)["context_pack"]["relevant_files"]
            run_cli(repo, "adapt", "--feature", "demo", "--signal", "dependency_change=true", "--plan-step", "Keep acceptance and check the affected dependency")
            self.assertEqual(self.task(repo)["decision"]["mode"], "STANDARD")
            self.assertTrue(self.task(repo)["plan"])
            run_cli(repo, "adapt", "--feature", "demo", "--signal", "architecture=true")
            task = self.task(repo)
            self.assertEqual(task["decision"]["mode"], "DEEP")
            self.assertEqual(set(original), set(task["context_pack"]["relevant_files"]))
            self.assertEqual(task["metrics"]["escalations"], 2)
            self.assertIn("planning", run_cli(repo, "next", "--feature", "demo").stdout)

    def test_failed_unchanged_stops_and_retries_are_bounded(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.prepare(Path(tmp)); create_quality_gate(repo)
            command = f"{sys.executable} -c 'raise SystemExit(3)'"
            args = ["verify", "--feature", "demo", "--command", command]
            self.assertNotEqual(run_cli(repo, *args, ok=False).returncode, 0)
            self.assertIn("unchanged failed", run_cli(repo, *args, ok=False).stderr)
            for condition in ["fixture environment repaired once", "fixture environment repaired twice"]:
                run_cli(repo, *args, "--retry-condition", condition, ok=False)
            self.assertIn("attempt limit", run_cli(repo, *args, "--retry-condition", "another change", ok=False).stderr)
            self.assertEqual(self.task(repo)["metrics"]["verification_iterations"], 3)
            run_cli(repo, "specify", "--feature", "demo", "--request", "fix tiny bug with clarified acceptance", "--allow", "app.txt")
            self.assertEqual(self.task(repo)["metrics"]["verification_iterations"], 3)

    def test_parallel_requires_independence_and_records_real_exits(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.prepare(Path(tmp)); create_quality_gate(repo)
            args = ["verify", "--feature", "demo", "--jobs", "2", "--command", f"{sys.executable} -c pass", "--command", f"{sys.executable} -c 'print(1)'"]
            self.assertIn("independent", run_cli(repo, *args, ok=False).stderr)
            run_cli(repo, *args, "--independent")
            evidence = read_toon(repo / ".ai-sdlc-loop/demo/evidence.toon")
            self.assertEqual([r["exit_code"] for r in evidence["commands"]], [0, 0])
            self.assertTrue(all(r["seconds"] >= 0 for r in evidence["commands"]))

    def test_full_flow_preserves_deep_and_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.prepare(Path(tmp), full=True)
            self.assertEqual(self.task(repo)["decision"]["mode"], "DEEP")
            self.assertIn("planning", run_cli(repo, "next", "--feature", "demo").stdout)
            result = run_cli(repo, "adapt", "--feature", "demo", "--complete-stage", "implement", "--evidence", "app.txt", ok=False)
            self.assertNotEqual(result.returncode, 0)
            result = run_cli(repo, "verify", "--feature", "demo", "--command", f"{sys.executable} -c pass", ok=False)
            self.assertIn("quality-gate", result.stderr)
            (repo / ".env").write_text("PRIVATE_FIXTURE_VALUE=do-not-pack\n")
            run_cli(repo, "specify", "--feature", "sensitive", "--request", "update local configuration", "--allow", ".env")
            state = read_toon(repo / ".ai-sdlc-loop/sensitive/state.toon")
            self.assertEqual(state["execution"]["decision"]["mode"], "DEEP")
            self.assertNotIn(".env", state["execution"]["context_pack"]["relevant_files"])
            self.assertNotIn("PRIVATE_FIXTURE_VALUE", str(state))

if __name__ == "__main__": unittest.main()
