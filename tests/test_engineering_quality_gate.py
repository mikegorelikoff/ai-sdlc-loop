from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from tests.helpers import (
    create_quality_gate,
    init_repo,
    read_toon,
    run_cli,
    write_toon,
)
from toon import decode_toon


def prepare_change(repo: Path) -> None:
    run_cli(
        repo,
        "specify",
        "--feature",
        "demo",
        "--request",
        "Change app",
        "--allow",
        "app.txt",
    )
    fingerprint = read_toon(repo / ".ai-sdlc-loop/demo/spec.toon")["fingerprint"]
    run_cli(
        repo,
        "approve",
        "--feature",
        "demo",
        "--action",
        "implement",
        "--decision",
        "approve",
        "--fingerprint",
        fingerprint,
        "--reviewer",
        "human",
    )
    (repo / "app.txt").write_text("after\n", encoding="utf-8")


class EngineeringQualityGateTests(unittest.TestCase):
    def test_tc038_missing_gate_blocks_verify_without_partial_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            prepare_change(repo)
            result = run_cli(
                repo,
                "verify",
                "--feature",
                "demo",
                "--command",
                f"{__import__('sys').executable} -c pass",
                ok=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("quality-gate evidence is required", result.stderr)
            self.assertFalse((repo / ".ai-sdlc-loop/demo/evidence.toon").exists())

    def test_tc038_pass_and_pass_with_findings_are_eligible(self) -> None:
        for status in ("PASS", "PASS_WITH_FINDINGS"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as tmp:
                repo = init_repo(Path(tmp) / "repo")
                prepare_change(repo)
                create_quality_gate(repo, status=status)
                run_cli(
                    repo,
                    "verify",
                    "--feature",
                    "demo",
                    "--command",
                    f"{__import__('sys').executable} -c pass",
                )
                self.assertTrue(read_toon(repo / ".ai-sdlc-loop/demo/evidence.toon")["ready"])

    def test_tc038_failed_gate_blocks_verify(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            prepare_change(repo)
            create_quality_gate(repo, status="FAIL")
            result = run_cli(
                repo,
                "verify",
                "--feature",
                "demo",
                "--command",
                f"{__import__('sys').executable} -c pass",
                ok=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("not ready", result.stderr)

    def test_tc038_stale_gate_blocks_verify(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            prepare_change(repo)
            create_quality_gate(repo)
            (repo / "app.txt").write_text("drifted after review\n", encoding="utf-8")
            result = run_cli(
                repo,
                "verify",
                "--feature",
                "demo",
                "--command",
                f"{__import__('sys').executable} -c pass",
                ok=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("invalid or stale", result.stderr)
            self.assertFalse((repo / ".ai-sdlc-loop/demo/evidence.toon").exists())

    @unittest.skipIf(os.name == "nt", "Windows chmod does not implement POSIX executable bits")
    def test_tc038_file_mode_drift_blocks_verify(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            prepare_change(repo)
            create_quality_gate(repo)
            app = repo / "app.txt"
            app.chmod(app.stat().st_mode | 0o111)
            result = run_cli(
                repo,
                "verify",
                "--feature",
                "demo",
                "--command",
                f"{__import__('sys').executable} -c pass",
                ok=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("invalid or stale", result.stderr)
            self.assertFalse((repo / ".ai-sdlc-loop/demo/evidence.toon").exists())

    def test_tc038_tampered_gate_blocks_verify(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            prepare_change(repo)
            create_quality_gate(repo)
            report_path = repo / ".ai-sdlc-loop/demo/quality-gate.toon"
            report = read_toon(report_path)
            report["summary"] = "Tampered after finalization."
            write_toon(report_path, report)
            result = run_cli(
                repo,
                "verify",
                "--feature",
                "demo",
                "--command",
                f"{__import__('sys').executable} -c pass",
                ok=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("fingerprint is invalid", result.stderr)

    def test_tc038_status_includes_quality_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            prepare_change(repo)
            report = create_quality_gate(repo)
            result = run_cli(repo, "status", "--feature", "demo")
            status = decode_toon(result.stdout)
            self.assertEqual(report["report_fingerprint"], status["quality_gate"]["report_fingerprint"])


if __name__ == "__main__":
    unittest.main()
