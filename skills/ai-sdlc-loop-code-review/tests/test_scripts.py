#!/usr/bin/env python3
"""Tests for ai-sdlc-loop-code-review review_readiness.py CLI and journal recording."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "review_readiness.py"
_SHARED = SKILL_ROOT.parent / "ai-sdlc-loop-shared-runtime" / "scripts"
if _SHARED.is_dir() and str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))
import usage_journal


class CodeReviewScriptTests(unittest.TestCase):
    def test_help_exposes_flags(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("--quick-flow", result.stdout)
        self.assertIn("--full-flow", result.stdout)
        self.assertIn("--spec", result.stdout)

    def test_conflicting_flags_fail(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--base", "main", "--full-repo"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("--base and --full-repo cannot be used together", result.stderr)

    def test_journal_tracking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            (tmp_root / ".git").mkdir()
            env = os.environ.copy()

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--help"],
                capture_output=True,
                text=True,
                cwd=str(tmp_root),
                env=env,
            )
            self.assertEqual(0, result.returncode)

            sessions = usage_journal.scan_sessions(root=tmp_root)
            self.assertTrue(len(sessions) >= 1)
            raw_events = sessions[0]["events"]
            events = list(raw_events.values()) if isinstance(raw_events, dict) else list(raw_events)
            skill_events = [e for e in events if e.get("skill") == "ai-sdlc-loop-code-review"]
            self.assertTrue(any(e["type"] == "skill.start" for e in skill_events))
            self.assertTrue(any(e["type"] == "skill.end" for e in skill_events))


if __name__ == "__main__":
    unittest.main()
