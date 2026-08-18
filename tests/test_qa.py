from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import ROOT, read_toon


SCRIPT = ROOT / "skills/ai-sdlc-qa/scripts/qa_plan.py"


class QaPlanTests(unittest.TestCase):
    def test_tc027_qa_plan_is_canonical_toon(self) -> None:
        command = [
            sys.executable,
            str(SCRIPT),
            "--feature",
            "qa-demo",
            "--summary",
            "Protect the install flow",
            "--acceptance",
            "QA-001|maintainer|clean project|install package|all skills exist|automated|high",
            "--regression",
            "unrelated skills remain unchanged",
            "--validation",
            "python3 -m unittest: passed",
            "--manual-check",
            "inspect the install receipt",
            "--status",
            "ready",
        ]
        first = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True).stdout
        second = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True).stdout
        self.assertEqual(first, second)
        artifact = read_toon_text(first)
        self.assertEqual("ai-sdlc-loop-qa/v1", artifact["schema"])
        self.assertEqual("QA-001", artifact["acceptance"][0]["id"])

    def test_tc027_qa_output_rejects_non_toon_and_escape(self) -> None:
        base = [
            sys.executable,
            str(SCRIPT),
            "--feature",
            "qa-demo",
            "--summary",
            "Demo",
            "--acceptance",
            "QA-001|user|ready|act|observe|manual|low",
        ]
        for output in ("qa.json", "../qa.toon"):
            result = subprocess.run(base + ["--output", output], cwd=ROOT, text=True, capture_output=True)
            self.assertNotEqual(0, result.returncode)

    def test_tc027_qa_output_writes_toon_atomically(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            command = [
                sys.executable,
                str(SCRIPT),
                "--feature",
                "qa-demo",
                "--summary",
                "Demo",
                "--acceptance",
                "QA-001|user|ready|act|observe|manual|low",
                "--output",
                "evidence/qa.toon",
            ]
            subprocess.run(command, cwd=temporary, text=True, capture_output=True, check=True)
            artifact = read_toon(Path(temporary) / "evidence/qa.toon")
            self.assertEqual("qa-demo", artifact["feature"])


def read_toon_text(content: str):
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / "artifact.toon"
        path.write_text(content, encoding="utf-8")
        return read_toon(path)


if __name__ == "__main__":
    unittest.main()
