#!/usr/bin/env python3
"""Tests for ai-sdlc-loop-security-testing security_review_matrix.py CLI and journal recording."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "security_review_matrix.py"
_SHARED = SKILL_ROOT.parent / "ai-sdlc-loop-shared-runtime" / "scripts"
if _SHARED.is_dir() and str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))
import usage_journal


class SecurityTestingScriptTests(unittest.TestCase):
    def test_help_exposes_flags(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("--feature", result.stdout)
        self.assertIn("--quick-flow", result.stdout)
        self.assertIn("--full-flow", result.stdout)

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
            skill_events = [e for e in events if e.get("skill") == "ai-sdlc-loop-security-testing"]
            self.assertTrue(any(e["type"] == "skill.start" for e in skill_events))
            self.assertTrue(any(e["type"] == "skill.end" for e in skill_events))


if __name__ == "__main__":
    unittest.main()
