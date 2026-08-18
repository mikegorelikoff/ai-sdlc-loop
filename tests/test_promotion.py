from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.helpers import init_repo, read_toon, run_cli


class PromotionTests(unittest.TestCase):
    def test_tc016_valid_artifact_promotes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            run_cli(repo, "specify", "--feature", "demo", "--request", "Document", "--allow", "app.txt", "--trace", "REQ-001")
            output = repo / "promoted.toon"
            run_cli(repo, "promote", "--feature", "demo", "--output", str(output))
            promoted = read_toon(output)
            self.assertEqual("ai-sdlc-harness-promotion/v1", promoted["schema"])
            self.assertEqual(["REQ-001"], promoted["trace_ids"])

    def test_tc017_invalid_source_has_no_partial_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            state = repo / ".ai-sdlc-loop/demo"
            state.mkdir(parents=True)
            (state / "spec.toon").write_text("schema: unknown/v9\n", encoding="utf-8")
            output = repo / "promoted.toon"
            result = run_cli(repo, "promote", "--feature", "demo", "--output", str(output), ok=False)
            self.assertNotEqual(0, result.returncode)
            self.assertFalse(output.exists())

    def test_tc025_json_named_promotion_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            run_cli(repo, "specify", "--feature", "demo", "--request", "Document", "--allow", "app.txt")
            output = repo / ("promoted." + "json")
            result = run_cli(repo, "promote", "--feature", "demo", "--output", str(output), ok=False)
            self.assertNotEqual(0, result.returncode)
            self.assertIn(".toon", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
