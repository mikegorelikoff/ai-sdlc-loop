from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import ROOT, read_toon


REQUIREMENTS = ROOT / "skills/ai-sdlc-loop-requirements-review/scripts/requirements_review.py"
RELEASE = ROOT / "skills/ai-sdlc-loop-release-readiness/scripts/release_readiness.py"


def decode_stdout(content: str):
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / "artifact.toon"
        path.write_text(content, encoding="utf-8")
        return read_toon(path)


class ReviewArtifactTests(unittest.TestCase):
    def test_tc028_requirements_review_is_canonical_toon(self) -> None:
        command = [
            sys.executable,
            str(REQUIREMENTS),
            "--feature", "review-demo",
            "--source", "requirements.md",
            "--coverage", "actors",
            "--finding", "GAP-001|medium|acceptance|AC lacks error state|regression ambiguity|add negative outcome",
            "--status", "gaps",
        ]
        first = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True).stdout
        second = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True).stdout
        self.assertEqual(first, second)
        self.assertEqual("ai-sdlc-loop-requirements-review/v1", decode_stdout(first)["schema"])

    def test_tc028_requirements_ready_rejects_severe_gap(self) -> None:
        result = subprocess.run([
            sys.executable, str(REQUIREMENTS), "--feature", "review-demo",
            "--source", "requirements.md", "--status", "ready",
            "--finding", "GAP-001|high|scope|boundary absent|unsafe work|define paths",
        ], cwd=ROOT, text=True, capture_output=True)
        self.assertNotEqual(0, result.returncode)
        for output in ("review.json", "../review.toon"):
            denied = subprocess.run([
                sys.executable, str(REQUIREMENTS), "--feature", "review-demo",
                "--source", "requirements.md", "--status", "ready", "--output", output,
            ], cwd=ROOT, text=True, capture_output=True)
            self.assertNotEqual(0, denied.returncode)

    def test_tc029_release_readiness_is_canonical_toon(self) -> None:
        result = subprocess.run([
            sys.executable, str(RELEASE), "--feature", "release-demo",
            "--release", "v1.0.0", "--commit", "136ebb2",
            "--gate", "ci|passed|run 1", "--status", "ready",
        ], cwd=ROOT, text=True, capture_output=True, check=True)
        artifact = decode_stdout(result.stdout)
        self.assertEqual("ai-sdlc-loop-release-readiness/v1", artifact["schema"])
        self.assertEqual("136ebb2", artifact["commit"])

    def test_tc029_release_ready_rejects_incomplete_gate(self) -> None:
        result = subprocess.run([
            sys.executable, str(RELEASE), "--feature", "release-demo",
            "--release", "v1.0.0", "--commit", "136ebb2",
            "--gate", "windows|planned|queued", "--status", "ready",
        ], cwd=ROOT, text=True, capture_output=True)
        self.assertNotEqual(0, result.returncode)


if __name__ == "__main__":
    unittest.main()
